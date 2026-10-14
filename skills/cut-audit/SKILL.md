---
name: cut-audit
description: Stage 2. Use after any rough cut or re-cut to check the audio itself at every cut edge - words chopped in half, repeated phrases the transcript hid, clicks. Runs scripts/check_cut_edges.py.
---
# cut-audit (stage 2)

**In plain words:** listen, do not read. The transcript can look perfect while the sound is broken. This step checks the real sound at the start and end of every cut.

## Steps
1. Run `python3 .claude/skills/cut-audit/scripts/check_cut_edges.py work/cuts.json`.
   It reads the audio around each in/out point and flags an edge when speech is still running through it, and suggests the nearest quiet moment.
2. Move each flagged edge to the suggested time, rebuild the preview, run again. Repeat until it prints `0 flagged`.
3. Repeats check: compare each line's text with the two lines before it; if 3+ words in a row repeat, one take was left in by mistake.
4. Join check: where two cuts meet, the loudness on both sides should be within 6 dB; a bigger jump sounds like a jolt.

## Rules
- The transcript is not evidence. Speech recognition merges a repeated phrase into one. *Why: the question is not "is there speech at the edge?" but "is a word cut in half?".*
- Never mark the audit passed without the script's output in front of you.
- Re-run after ANY change to cuts.json, however small.
