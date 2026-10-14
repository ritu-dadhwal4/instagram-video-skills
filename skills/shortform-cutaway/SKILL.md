---
name: shortform-cutaway
description: Stage 1 rough cut. Use to turn raw talking footage into a clean cut - transcribe with word timings, keep the best take of each line, remove dead air, fumbles and repeats. Produces work/cuts.json.
---
# shortform-cutaway (stage 1, the rough cut)

**In plain words:** throw away the bad bits. The creator says a line three times; keep the cleanest one. Remove the silences and the "umm". What is left is the skeleton of the video.

## Steps
1. Transcribe with word-level timings: `whisperx raw/<file> --model small --output_format json --output_dir work/`. If whisperx is missing, tell the creator the install command (`pip3 install whisperx`) and do not guess timings.
2. Group words into lines. Where a line is repeated, keep the LAST complete take unless an earlier one is clearly cleaner.
3. Drop fillers, false starts and any silence longer than 0.35 s.
4. Write `work/cuts.json`: `[{"id":1,"src":"raw/a.mp4","in":12.48,"out":15.91,"text":"..."}]`.
5. Build a preview with ffmpeg (trim + concat) into `out/rough.mp4`.

## Rules
- The out-point is where the last word RELEASES (sound has died), not where it starts. Add 0.08 s after the word's end time. *Why: a cut placed at the start of the last word drops that word; "edited using AI" plays as "edited using".*
- The in-point sits 0.04 s before the first word, so the first consonant is not clipped.
- Never cut inside a word to save time.
- Keep their meaning: do not remove a line that a later line refers to.
- Then run cut-audit. A rough cut is not done until the audit passes.
