---
name: take-geometry
description: Stage 3. Use to measure where the face sits in each take (position, size, which way they are looking) so that captions, cards and crops never cover it. Writes work/geometry.json.
---
# take-geometry (stage 3)

**In plain words:** find where the face is. If the video knows where the creator's face is in every shot, text and graphics can be placed in the empty space instead of on their forehead.

## Steps
1. For each cut, pull 3 frames (start, middle, end) with ffmpeg.
2. Look at them and record: face box as fractions of the frame (x, y, w, h), eye line height, gaze direction (left / right / camera), and the largest empty area.
3. Write `work/geometry.json`: one entry per cut id.
4. For 9:16 crops from 16:9 footage, choose the crop window from the face box, not the frame centre.

## Rules
- Text never overlaps the face box plus a 6% margin.
- Face goes on the side opposite their gaze: looking right, face on the left. *Why: the creator should look INTO the content, not off the edge.*
- Keep the eye line at the same height across neighbouring cuts, or the head appears to jump.
- Platform safe zones for reels: keep text out of the top 12% and bottom 22% (buttons and caption cover them).
- If the face moves a lot inside one cut, measure it every second instead of 3 times.
