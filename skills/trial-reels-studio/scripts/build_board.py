#!/usr/bin/env python3
"""Turn a Trial Reels Studio spec into Whiteboard element files.

Usage: build_board.py spec.json out_dir first_id_number [origin_y]
Writes out_dir/meta.json and out_dir/e<N>.json, prints the ids in write order.
"""
import json, os, sys, math, urllib.parse
from xml.dom import minidom

CC = "currentColor"
BLUE, BLUEm = "%239CCDE8", "%232F7CC4"
PEACH, PEACHm = "%23F6BD78", "%23D97757"
YEL, YELm = "%23F7DD72", "%23D97757"
GRN, GRNm = "%23B7DFA4", "%232E8B57"
PUR, PURm = "%23CDB6EC", "%237C5CBF"   # purple = you on camera
GRY, GRYm = "%23D1D1D1", "%23878787"
WHITE = "%23FFFFFF"

FMT_NAMES = {"product": "Product only", "face": "Face only", "face-prop": "Face + prop in hand",
             "split": "Split, face bottom", "split-top": "Split, face top",
             "circle": "Face circle on product", "box": "Face box on product",
             "greenscreen": "Green screen", "text": "Text-only opener"}

def f(v): return f"{v:.1f}".rstrip("0").rstrip(".")

def rect(x, y, w, h, fill, stroke, rx=0, sw=2, dash=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<rect x='{f(x)}' y='{f(y)}' width='{f(w)}' height='{f(h)}' rx='{f(rx)}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'{d}/>"
def line(x1, y1, x2, y2, sw=1.5, dash=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<line x1='{f(x1)}' y1='{f(y1)}' x2='{f(x2)}' y2='{f(y2)}' stroke='{CC}' stroke-width='{sw}' stroke-linecap='round'{d}/>"
def circ(cx, cy, r, fill="none", stroke=CC, sw=1.5):
    return f"<circle cx='{f(cx)}' cy='{f(cy)}' r='{f(r)}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'/>"
def poly(pts, fill, stroke, sw=2, closed=True):
    p = " ".join(f"{f(a)},{f(b)}" for a, b in pts)
    tag = "polygon" if closed else "polyline"
    return f"<{tag} points='{p}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' stroke-linejoin='round' stroke-linecap='round'/>"

class Box:
    """Maps a 0..100 scene grid onto a box."""
    def __init__(s, x, y, w, h): s.x, s.y, s.w, s.h = x, y, w, h
    def X(s, u): return s.x + u * s.w / 100
    def Y(s, v): return s.y + v * s.h / 100
    def W(s, u): return u * s.w / 100
    def H(s, v): return v * s.h / 100
    def R(s, r): return r * min(s.w, s.h) / 100
    def rect(s, u, v, uw, vh, fill, stroke, rx=2, sw=2, dash=None):
        return rect(s.X(u), s.Y(v), s.W(uw), s.H(vh), fill, stroke, rx, sw, dash)
    def line(s, u1, v1, u2, v2, sw=1.5, dash=None): return line(s.X(u1), s.Y(v1), s.X(u2), s.Y(v2), sw, dash)
    def circ(s, u, v, r, fill="none", stroke=CC, sw=1.5): return circ(s.X(u), s.Y(v), s.R(r), fill, stroke, sw)
    def poly(s, pts, fill, stroke, sw=2, closed=True): return poly([(s.X(a), s.Y(b)) for a, b in pts], fill, stroke, sw, closed)
    def arrow(s, u1, v1, u2, v2):
        ang = math.atan2(s.Y(v2) - s.Y(v1), s.X(u2) - s.X(u1)); L = 5
        hx, hy = s.X(u2), s.Y(v2)
        a = (hx - L * math.cos(ang - .5), hy - L * math.sin(ang - .5)); b = (hx - L * math.cos(ang + .5), hy - L * math.sin(ang + .5))
        return s.line(u1, v1, u2, v2, 2) + poly([a, (hx, hy), b], "none", CC, 2, closed=False)

def slide_plain(b, u, v, w, h, spill=False):
    s = b.rect(u, v, w, h, BLUE, BLUEm) + b.line(u + w * .1, v + h * .2, u + w * .6, v + h * .2, 2.5)
    for k in range(3):
        y = v + h * (.42 + k * .18)
        s += b.line(u + w * .14, y, (u + w * 1.3) if (spill and k == 2) else (u + w * .85), y, 1.5)
    return s

def sc_plain_slides(b):
    return (slide_plain(b, 2, 4, 46, 44) + slide_plain(b, 52, 4, 46, 44) +
            slide_plain(b, 2, 52, 46, 44) + slide_plain(b, 52, 52, 40, 44, spill=True))
def sc_before_after(b):
    s = slide_plain(b, 2, 6, 42, 88) + b.line(50, 2, 50, 98, 1.5, "5 4") + b.rect(56, 6, 42, 88, PEACH, PEACHm)
    s += b.circ(77, 24, 9, YEL, YELm, 2)
    for k, hh in enumerate([22, 34, 48]): s += b.rect(61 + k * 12, 88 - hh, 8, hh, GRN, GRNm, rx=1)
    return s
def sc_chart_edit(b):
    s = b.line(8, 94, 96, 94, 2) + b.line(8, 4, 8, 94, 2)
    for k, hh in enumerate([22, 36, 50]): s += b.rect(14 + k * 20, 94 - hh, 14, hh, GRN, GRNm, rx=1)
    s += b.rect(74, 10, 14, 84, "none", CC, rx=1, sw=1.5, dash="4 3") + b.rect(74, 50, 14, 44, GRN, GRNm, rx=1)
    cx, cy = 84, 22
    s += b.poly([(cx, cy), (cx, cy + 22), (cx + 5, cy + 17), (cx + 9, cy + 26), (cx + 13, cy + 24), (cx + 9, cy + 15), (cx + 16, cy + 15)], YEL, YELm, 1.5)
    return s
def sc_chat_screenshot(b):
    s = b.rect(4, 2, 66, 22, YEL, YELm, rx=4) + b.poly([(14, 24), (12, 32), (24, 24)], YEL, YELm)
    s += b.line(10, 10, 56, 10, 2) + b.line(10, 17, 44, 17, 1.5)
    s += b.rect(4, 36, 92, 60, "none", CC, rx=0, sw=1.5, dash="5 4") + slide_plain(b, 9, 41, 82, 50)
    return s
def sc_github(b):
    s = b.rect(2, 4, 96, 92, BLUE, BLUEm, rx=3) + b.line(2, 16, 98, 16, 1.5)
    for k in range(3): s += b.circ(8 + k * 6, 10, 1.8, "none", CC, 1.2)
    s += b.rect(5, 59, 90, 13, PEACH, PEACHm, rx=2)
    for k in range(5):
        y = 22 + k * 13
        s += b.rect(9, y + 2, 9, 7, YEL, YELm, rx=1, sw=1.5) + b.line(24, y + 5.5, 24 + [40, 30, 46, 26, 36][k], y + 5.5, 1.5)
    return s
def sc_designed_deck(b):
    s = b.rect(2, 8, 96, 80, PEACH, PEACHm, rx=3) + b.circ(24, 46, 14, YEL, YELm, 2)
    s += b.line(46, 30, 88, 30, 2.5) + b.line(46, 44, 82, 44, 1.5) + b.line(46, 56, 76, 56, 1.5)
    for k, hh in enumerate([10, 16, 22]): s += b.rect(60 + k * 10, 80 - hh, 7, hh, GRN, GRNm, rx=1, sw=1.5)
    return s
def sc_three_decks(b):
    s = ""
    for k, (fl, st) in enumerate([(PEACH, PEACHm), (GRN, GRNm), (YEL, YELm)]):
        u = 2 + k * 33
        s += b.rect(u, 16, 30, 66, fl, st, rx=2) + b.line(u + 5, 28, u + 22, 28, 2.5) + b.line(u + 5, 40, u + 18, 40, 1.5)
    return s
def sc_code_to_file(b):
    s = b.rect(2, 8, 56, 84, BLUE, BLUEm, rx=3)
    for k, ln in enumerate([30, 22, 36, 18, 28, 24]):
        ind = 8 + (k % 3) * 5
        s += b.line(ind, 20 + k * 11, ind + ln, 20 + k * 11, 1.5)
    s += b.arrow(62, 50, 74, 50)
    s += b.poly([(78, 26), (90, 26), (98, 36), (98, 74), (78, 74)], YEL, YELm)
    return s
def sc_cloud_upload(b):
    s = b.circ(18, 28, 12, BLUE, BLUEm, 2) + b.circ(32, 20, 15, BLUE, BLUEm, 2) + b.circ(46, 30, 11, BLUE, BLUEm, 2)
    s += b.arrow(40, 46, 52, 58)
    s += b.rect(46, 58, 52, 38, PEACH, PEACHm, rx=2) + b.line(46, 68, 98, 68, 1.5) + b.rect(52, 74, 18, 16, GRN, GRNm, rx=1, sw=1.5)
    return s
def sc_rules_doc(b):
    s = b.rect(2, 6, 40, 88, YEL, YELm, rx=2)
    for k in range(4):
        y = 18 + k * 18
        s += b.rect(7, y, 7, 7, "none", CC, rx=1, sw=1.2) + b.poly([(8, y + 4), (10, y + 6), (13, y + 1)], "none", CC, 1.5, closed=False)
        s += b.line(18, y + 3.5, 36, y + 3.5, 1.5)
    s += b.arrow(46, 50, 56, 50)
    s += b.rect(58, 24, 40, 52, PEACH, PEACHm, rx=2) + b.circ(70, 50, 8, YEL, YELm, 2) + b.line(82, 42, 94, 42, 2) + b.line(82, 54, 92, 54, 1.5)
    return s
def sc_messy_slide(b):
    s = b.rect(2, 4, 96, 92, BLUE, BLUEm, rx=2)
    s += b.rect(10, 14, 36, 20, PEACH, PEACHm, rx=1) + b.rect(34, 26, 40, 16, GRN, GRNm, rx=1)
    s += b.line(10, 56, 112, 56, 2) + b.line(10, 66, 70, 66, 1.5)
    s += b.rect(52, 72, 32, 18, "none", CC, rx=1, sw=1.5, dash="4 3")
    s += b.poly([(70, 34), (70, 54), (75, 49), (79, 58), (83, 56), (79, 47), (86, 47)], YEL, YELm, 1.5)
    return s
def sc_comment_bubble(b):
    s = b.rect(4, 14, 92, 56, YEL, YELm, rx=8) + b.poly([(20, 70), (16, 88), (36, 70)], YEL, YELm)
    for k in range(3): s += b.circ(32 + k * 18, 42, 5, CC, CC, 1)
    return s

SCENES = {k[3:].replace("_", "-"): v for k, v in globals().items() if k.startswith("sc_")}

def camera(x, y, w, h, shape="rect"):
    if shape == "circle":
        r = min(w, h) / 2; cx, cy = x + w / 2, y + h / 2
        s = circ(cx, cy, r, PUR, PURm, 2.5)
    else:
        s = rect(x, y, w, h, PUR, PURm, rx=8 if w > 60 else 5, sw=2)
        cx, cy = x + w / 2, y + h / 2
    k = min(w, h) * .2
    s += rect(cx - k, cy - k * .62, 2 * k, k * 1.3, "none", CC, rx=k * .2, sw=1.5)
    s += circ(cx, cy + k * .03, k * .42, "none", CC, 1.5) + rect(cx - k * .35, cy - k * .9, k * .7, k * .28, "none", CC, rx=1, sw=1.2)
    return s

OVERLAY_Y = {"product": .13, "face": .13, "face-prop": .13, "split": .43, "split-top": .43,
             "circle": .13, "box": .13, "greenscreen": .13, "text": .36}
OVERLAY_H = {"text": .22}

def phone(w, h, fmt, scene, hi=None, overlay_in_svg=False):
    s = rect(3, 3, w - 6, h - 6, GRY, GRYm, rx=24 if w > 170 else (20 if w > 120 else 14))
    draw = SCENES.get(scene, sc_designed_deck)
    if fmt == "face":
        s += camera(10, 10, w - 20, h - 20)
    elif fmt == "face-prop":
        s += camera(10, 10, w - 20, h - 20)
        s += rect(w * .3, h * .6, w * .4, h * .17, BLUE, BLUEm, rx=4, sw=2) + line(w * .36, h * .65, w * .62, h * .65, 1.5) + line(w * .36, h * .7, w * .56, h * .7, 1.5)
    elif fmt == "split":
        s += draw(Box(14, h * .1, w - 44, h * .3))
        s += line(10, h * .5, w - 10, h * .5, 1.5) + camera(10, h * .5, w - 20, h * .5 - 10)
    elif fmt == "split-top":
        s += camera(10, 10, w - 20, h * .5 - 12) + line(10, h * .5, w - 10, h * .5, 1.5)
        s += draw(Box(14, h * .6, w - 44, h * .24))
    elif fmt == "greenscreen":
        s += draw(Box(12, h * .3, w - 36, h * .34))
        s += f"<path d='M{f(w*.22)} {f(h-10)} L{f(w*.22)} {f(h*.8)} Q{f(w*.5)} {f(h*.62)} {f(w*.78)} {f(h*.8)} L{f(w*.78)} {f(h-10)} Z' fill='{PUR}' stroke='{PURm}' stroke-width='2'/>"
        k = w * .07; cx, cy = w * .5, h * .86
        s += rect(cx - k, cy - k * .6, 2 * k, k * 1.3, "none", CC, rx=2, sw=1.5) + circ(cx, cy, k * .42, "none", CC, 1.5)
    elif fmt == "text":
        s += rect(10, 10, w - 20, h - 20, YEL, YELm, rx=16 if w > 120 else 10, sw=2)
    else:
        s += draw(Box(14, h * .32, w - 44, h * (.32 if fmt in ("circle", "box") else .44)))
        if fmt == "circle": s += camera(w * .1, h * .67, w * .3, w * .3, "circle")
        if fmt == "box": s += camera(w * .08, h * .67, w * .36, h * .16)
    ix = w - 19 if w > 120 else w - 12
    for k, fy in enumerate([.6, .685, .77, .855]):
        on = hi == k
        s += circ(ix, h * fy, 6 if w > 170 else (5 if w > 120 else 3.5), PEACH if on else "none", PEACHm if on else CC, 2 if on else 1.2)
    if w > 120:
        s += line(w * .2, h - 34, w * .55, h - 34, 2) + line(w * .1, h - 20, w * .7, h - 20, 2)
    else:
        s += line(w * .14, h - 18, w * .64, h - 18, 1.5)
    if overlay_in_svg:
        oy = OVERLAY_Y[fmt] * h
        s += rect(w * .12, oy, w * .76, h * OVERLAY_H.get(fmt, .1), WHITE, GRYm, rx=3, sw=1.2)
    return s

def svg_src(w, h, body):
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' data-look='clean'>{body}</svg>"
    minidom.parseString(urllib.parse.unquote(svg))  # fail loudly on broken markup
    assert "#" not in svg and len(svg) < 36000
    return "data:image/svg+xml," + svg

STATUS_COLOR = {"done": "green", "now": "yellow", "next": "white"}
STATUS_WORD = {"done": "done", "now": "now", "next": "next"}

def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; nid = [int(sys.argv[3])]
    oy = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out): os.remove(os.path.join(out, fn))
    E = {}; containers = []
    def add(d, container=False):
        k = f"e{nid[0]}"; nid[0] += 1; E[k] = d
        if container: containers.append(k)
        return k
    def text(x, y, t, size="body", wrap=None):
        d = {"type": "text", "x": x, "y": y + oy, "text": t, "size": size}
        if wrap: d["wrap"] = wrap
        return add(d)
    def box(x, y, w, h, t, color="white", size="small", align="left", kind="rounded"):
        return add({"type": "shape", "kind": kind, "x": x, "y": y + oy, "w": w, "h": h, "color": color, "size": size, "text": t, "textAlign": align})
    def section(x, y, w, h, t): return add({"type": "container", "x": x, "y": y + oy, "w": w, "h": h, "text": t, "color": "white"}, True)
    def image(x, y, w, h, src): return add({"type": "image", "x": x, "y": y + oy, "w": w, "h": h, "by": "claude", "src": src})

    st = spec["stops"]; hooks = spec["hooks"]
    def mark(h):
        p = h.get("picked")
        return "✓ picked" if p is True else ("skipped" if p is False else "☐ to pick")
    text(140, -250, spec["title"], "title")
    text(140, -178, spec["takeaway"], "large")

    stops = []
    X, W, GAP = 140, 1100, 110
    y = 0
    def stop(key, num, name, h):
        nonlocal y
        s = st.get(key, "next")
        sec = section(X, y, W, h, f"{num} · {name} · {STATUS_WORD[s]}")
        label = "✓" if s == "done" else str(num)
        node = box(0, y + h / 2 - 45, 90, 90, f"**{label}**", color=STATUS_COLOR[s], size="large", align="center", kind="ellipse")
        stops.append(node); top = y; y += h + GAP
        return top

    # 1 Idea
    t = stop("idea", 1, "Idea", 158)
    box(X + 24, t + 24, W - 48, 110, f"**Your idea**\n{spec['idea']}", size="body")

    # 2 Script
    t = stop("script", 2, "Script", 298)
    box(X + 24, t + 24, W - 48, 250, "**Script** · body and CTA stay the same in every trial reel\n" + spec["script"])

    # 3 Hooks
    n = len(hooks); cols = n if n <= 4 else math.ceil(n / 2); rows = math.ceil(n / cols)
    PW, PH, PITCH = 200, 356, 560
    hh = 24 + 70 + 24 + rows * PITCH
    t = stop("hooks", 3, "Hooks · pick the ones to film", hh)
    box(X + 24, t + 24, W - 48, 70, f"**{n} hooks, each drawn in its format.** White box = where the text overlay goes. Purple = you on camera.\nReferences: [your Hooks folder]({spec['folder_url']}) · " + " · ".join(spec["references"]), size="small")
    labels = []
    gx = X + 24 + (W - 48 - (cols * PW + (cols - 1) * 48)) / 2
    for i, hk in enumerate(hooks):
        x = gx + (i % cols) * (PW + 48); yy = t + 24 + 70 + 24 + (i // cols) * PITCH
        image(x, yy, PW, PH, svg_src(PW, PH, phone(PW, PH, hk["format"], hk["scene"])))
        labels.append((x, yy, hk))
    for x, yy, hk in labels:
        oh = round(OVERLAY_H.get(hk["format"], .146) * PH)
        box(x + 12, yy + OVERLAY_Y[hk["format"]] * PH, 176, oh, f"**{hk['overlay']}**", align="center")
        text(x, yy + PH + 12, f"**{hk['id']} · {hk['angle']}**  {mark(hk)}\n*{FMT_NAMES[hk['format']]}*\n“{hk['say']}”", "small", PW)

    # 4 Film
    t = stop("film", 4, "Film", 198)
    box(X + 24, t + 24, W - 48, 150, "**Record in one session**\n" + "\n".join("- " + s for s in spec["film"]), size="body")

    # 5 Edit
    rows_t = {"r0": {"at": 0, "c1": "Hook", "c2": "Status", "c3": "HyperFrames Studio preview"}}
    for i, hk in enumerate(hooks):
        if hk.get("picked") is False: continue
        rows_t[f"r{i + 1}"] = {"at": i + 1, "c1": f"{hk['id']} · {hk['angle']}", "c2": hk.get("edit", "waiting"), "c3": hk.get("link", "—")}
    th = 40 * len(rows_t) + 20
    eh = 24 + 330 + 24 + th + 24
    t = stop("edit", 5, "Edit with your video skills", eh)
    box(X + 24, t + 24, 300, 330, "**Attach in this order**\n1. **Raw video**, your main take\n2. **Reference video**, the editing style to copy\n3. **Hook image**, the approved hook style\n4. **Clips**, everything else\n\n[instagram-video-skills](" + spec["skills_url"] + ")", size="body")
    box(X + 348, t + 24, W - 372, 330, "**Prompt** · once per picked hook, swap H_\n" + spec["edit_prompt"])
    add({"type": "table", "x": X + 24, "y": t + 24 + 330 + 24 + oy,
         "cols": {"c1": {"at": 1, "w": 260}, "c2": {"at": 2, "w": 200}, "c3": {"at": 3, "w": 360}}, "rows": rows_t})

    # 6 Post
    t = stop("post", 6, "Post as trial reels", 138)
    box(X + 24, t + 24, W - 48, 90, spec["post"], size="body")

    # 7 Winner
    t = stop("winner", 7, "Winner", 158)
    box(X + 24, t + 24, W - 48, 110, spec["winner"], size="body")

    for a, b2 in zip(stops, stops[1:]):
        add({"type": "arrow", "from": a, "to": b2, "fromSide": "bottom", "toSide": "top"})
    order = containers + [k for k in E if k not in containers]
    json.dump({"v": 1, "title": spec.get("board_title", "Trial Reels Studio"), "order": order}, open(os.path.join(out, "meta.json"), "w"), ensure_ascii=False)
    for k, v in E.items(): json.dump(v, open(os.path.join(out, f"{k}.json"), "w"), ensure_ascii=False)
    print(json.dumps(order))

if __name__ == "__main__":
    main()
