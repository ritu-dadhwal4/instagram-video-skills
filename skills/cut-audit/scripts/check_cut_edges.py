#!/usr/bin/env python3
"""Check the audio at every cut edge: is a word being chopped in half?

usage: check_cut_edges.py work/cuts.json
cuts.json: [{"id": 1, "src": "raw/a.mp4", "in": 12.48, "out": 15.91, "text": "..."}]

An edge is flagged when speech is still running through it: loud just inside
the cut AND loud just outside it. For each flag the nearest quiet moment is
suggested. Needs ffmpeg; nothing else.
"""
import array, json, math, subprocess, sys
from pathlib import Path

RATE = 16000
FRAME = 0.02          # 20 ms loudness frames
EDGE = 0.08           # how far each side of the edge to listen
SEARCH = 0.6          # how far to look for a quiet moment
MARGIN_DB = 12        # "speech" = this much above the file's quiet level


def load_levels(src):
    """Loudness in dB of every 20 ms frame of the file."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", str(RATE), "-f", "s16le", "-"],
        capture_output=True, check=True).stdout
    samples = array.array("h"); samples.frombytes(raw[: len(raw) // 2 * 2])
    n = int(RATE * FRAME)
    levels = []
    for i in range(0, len(samples) - n + 1, n):
        rms = math.sqrt(sum(s * s for s in samples[i:i + n]) / n)
        levels.append(20 * math.log10(max(rms, 1) / 32768))
    return levels


def window(levels, start, end):
    a, b = max(0, int(start / FRAME)), min(len(levels), max(int(end / FRAME), int(start / FRAME) + 1))
    return max(levels[a:b]) if a < b else -96.0


def quiet_near(levels, t, direction, threshold):
    """First quiet frame walking away from t (direction +1 later, -1 earlier)."""
    i = int(t / FRAME)
    for step in range(int(SEARCH / FRAME)):
        j = i + direction * step
        if 0 <= j < len(levels) and levels[j] < threshold:
            return round(j * FRAME + (FRAME if direction > 0 else 0), 2)
    return None


def main():
    cuts_path = Path(sys.argv[1])
    cuts = json.loads(cuts_path.read_text())
    cache, flagged = {}, 0
    for cut in cuts:
        src = cut["src"]
        if src not in cache:
            path = src if Path(src).exists() else str(cuts_path.parent.parent / src)
            levels = load_levels(path)
            floor = sorted(levels)[len(levels) // 10]      # 10th percentile = room tone
            cache[src] = (levels, floor + MARGIN_DB)
        levels, threshold = cache[src]
        for edge, t, direction in (("in", cut["in"], -1), ("out", cut["out"], 1)):
            inside = window(levels, t - EDGE, t) if edge == "out" else window(levels, t, t + EDGE)
            outside = window(levels, t, t + EDGE) if edge == "out" else window(levels, t - EDGE, t)
            if inside > threshold and outside > threshold:
                flagged += 1
                fix = quiet_near(levels, t, direction, threshold)
                hint = f"move to {fix}" if fix is not None else f"no quiet moment within {SEARCH}s - listen by hand"
                print(f"FLAG cut {cut['id']} {edge}-point {t:.2f}s: speech runs through the edge -> {hint}   \"{cut.get('text', '')[-40:]}\"")
    print(f"{len(cuts)} cuts checked, {flagged} flagged")
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
