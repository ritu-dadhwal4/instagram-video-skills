---
name: board-build-edit
description: Edit format - one unbroken take in a small window at the top, with a board underneath that draws what is said piece by piece and files each finished point into a numbered slot. Use for explainers that list features, compare options or walk through numbers.
---
# board-build-edit (edit format)

**In plain words:** The creator stays in a small window at the top and the video never cuts away. Underneath, a board fills in as they talk, like a teacher writing on a whiteboard. Each finished point shrinks into a numbered row, so by the end the whole video is summarised on screen.

**Use when:** one continuous take lists several things (features of a tool, options with prices, steps with numbers) and there is no screen recording to show.

Measured from two reference shorts with learn-style; the notes in brackets say where in each reference a number was read.

## Layout (1080x1920)
- Face window: 80% of the width, top edge about 4% down, landscape crop. White 3 px border, square corners. On screen 100% of the time. *(ref A 17.2 s)*
- Subtitle inside the window, one centred line on its bottom edge. *(ref A 17.2 s)*
- Board under the window, 12% side margins: numbered dashed slots first (one per point the video will make), then the working area with a bold title and the pictures. *(ref A 4.0 s, 17.2 s)*
- Background: `--ink` at the top fading to one warm colour at the bottom, slow drift. One colour per video. *(ref A 1.0 s, ref B 6.0 s)*

## Pacing
- Zero cuts. If the take needs cuts, hide them under a board change, or use another format.
- Something on the board changes every 1.0 to 1.2 s. Each change takes 0.35 to 0.6 s. Nothing sits still longer than 1.8 s. *(frame-difference measurement, both refs)*
- First motion inside the first 0.2 s.

## Moves (added to mg-kit for this format)
- **ghost-then-fill:** an empty dashed box or blank card appears about 0.5 s before its value. *(ref A 9.0 s, ref B 2.0 s)*
- **file-away:** a finished point blurs and wipes sideways in about 0.5 s and lands as a filled row in the next slot, with one white pill holding the one number or phrase that matters. *(ref A 12.0 s)*
- **question-then-answer:** plant a question in the first second; answer it in the same spot at the end. *(ref B 0.5 s and 18.0 s)*

## Captions
- English, one clause at a time, 2 to 8 words, held for the clause, hard swap. No word-by-word highlight. *(ref A 0 to 8 s)*
- This replaces caption-align's 2-to-4-word chunks for this format only; its spelling, digits and timing rules still apply.

## Sound
- Voice first. Low soft pad 15 to 20 dB under the voice, energy under 300 Hz, no bright melody. *(quiet-window measurement, both refs)*
- Effects sit at or under the pad level. Final file -14 LUFS (render-ops).

## Rules
- Every word and number on the board comes from the checked asset plan.
- One idea per board element, 7 words or fewer, 44 px minimum. *Why: the references use 36 px; the kit's minimum wins.*
- No text below 78% of the height. *Why: the references run to 86%; the kit's safe zone wins.*
- The window crop comes from take-geometry; the subtitle must clear the face box.
- Motion timing, colours and fonts come from mg-kit and `brand.md`. Never the reference's colours, products or graphics.
