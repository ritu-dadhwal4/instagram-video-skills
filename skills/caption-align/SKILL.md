---
name: caption-align
description: Stage 6. Use to offer the creator the caption style options and then add captions that appear on the exact frame each word is spoken, after cuts are final. Re-times the transcript to the edited timeline.
---
# caption-align (stage 6)

**In plain words:** the words on screen must land exactly when they are spoken. Even 3 frames late looks sloppy.

## Caption styles to offer (the creator picks one in the brief)
| Style | How it looks | Best for |
|---|---|---|
| **Word pop** | 1 to 3 big bold words in the centre, each popping in as it is spoken, keyword in the accent colour | fast reels, hooks |
| **Karaoke line** | a full line shown at once, the spoken word lights up as the line is spoken | explainers, tutorials |
| **Subtitle bar** | small plain line at the bottom, like film subtitles | long-form, calm videos |
| **Boxed** | words on a solid rounded box so they read over busy footage | b-roll and vlog shots |
| **Keywords only** | no full captions; only the important word or number appears | formats where cards already carry the text |
| **None** | no captions | when they ask |
## Instagram looks to offer (second pick: how the letters look)
The table above is how the words ARRIVE. This one is how they LOOK, matching the text styles in Instagram's own editor. Any look works with any arrival style.
| Look | How it looks | Good for |
|---|---|---|
| **Classic** | clean rounded sans, optional solid box behind | anything; the safest |
| **Modern** | all capitals, wide spacing, thin and tidy | brand and product reels |
| **Neon** | glowing handwriting, like a neon sign | one or two words only; hard to read in lines |
| **Typewriter** | typewriter letters on a box | storytime, diary, text-post reels |
| **Strong** | very heavy italic sans | captions over busy video; hooks |
| **Elegant** | fine serif | calm, premium, quotes |
| **Directional** | plain narrow sans | long lines, tutorials |
| **Signature** | handwritten script | a name or sign-off, never full captions |
| **Bubble** | fat rounded letters | playful, kids, fun lists |
| **Deco** | decorative display capitals | titles only |
| **Instagram's own sticker** | we add NO captions; the creator adds the Captions sticker in the Instagram app when posting | when they want the exact native look |
Each look can also have: plain / solid box behind / outline-and-shadow, as Instagram's "A" button does.

- These are lookalikes built from open fonts. Instagram's real fonts (Instagram Sans and the editor faces) are not downloadable and must not be copied from the app.
- This list is the named styles confirmed in October 2026 from third-party guides; Instagram publishes no official list and its Edits app has 125+ fonts. When the creator sends screenshots of their own caption and text panels, add the missing ones here.
- Colours still come from `brand.md`, whatever the look.

Show both tables with a one-line recommendation for the chosen editing style (caption-edit → Word pop; split-screen, paper-drawer, whiteout, board-build → Keywords only or Karaoke line; longform → Subtitle bar; vlog, b-roll → Boxed). If the brief has no caption answer, ask before building; never choose silently.

## Steps
When `design.md` names a caption look and colours, offer that first and build captions in its fonts and accent colour.

1. Re-map each word's time from the raw file to the edited timeline using `work/cuts.json` (subtract the removed parts).
2. Convert to frames: `frame = round(seconds * 30)`.
3. Group words to suit the chosen style (Word pop 1 to 3 words, Karaoke and Subtitle one line, Boxed 2 to 4 words); break at natural pauses, never mid-phrase.
4. Place using `work/geometry.json`: away from the face, inside safe zones.
5. Check 5 random words: pull the frame where the word should first appear and the frame before it.

## Rules
- Captions are built AFTER the cut is final. Any re-cut means re-align.
- Fix spellings of brand and tool names by hand, using the list in `brand.md`.
- Max 2 lines. Highlight only the one keyword per chunk.
- A caption never stays on screen across a cut to a different sentence.
- Numbers as digits ($9, not "two forty nine").
