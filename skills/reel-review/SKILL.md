---
name: reel-review
description: Stage 9 review gate. Use after every render and before showing the creator - a separate reviewer on a different model watches frames from every section and lists what is broken. The editor never reviews its own work.
---
# reel-review (stage 9, the gate)

**In plain words:** a second pair of eyes. The one who made the video will always think it is fine, so a different model checks it first. The creator only sees a video that passed.

## Steps
1. Sample the render: `learn-style/scripts/sample_frames.sh out/<file> work/review 2`.
2. Start a fresh reviewer with the Agent tool on a DIFFERENT model from the one that edited (for example `model: sonnet` if the edit ran on Opus). Give it only: the frames folder, the transcript, the asset plan and the checklist below. Do not give it the edit history or your opinion.
3. Reviewer returns a list: `time · what is wrong · how sure`.
4. Fix everything it is sure about, re-render, review again. Pass = zero sure problems.

## Reviewer checklist
- Text over a face, or outside safe zones
- Caption words wrong, misspelt, or lingering after the line
- A cut that jumps the head position
- A zoom starting on a cut; a crossfade between face and screen
- Blank, black or frozen frames
- Card facts that differ from the asset plan
- Unreadable screen recordings

## Rules
- A model grading its own work passes its own work. Never skip the second model.
- Frames cannot judge sound; cut-audit and render-ops cover audio and must also be green.
- Tell the creator what the reviewer found and what was fixed, not only "passed".
