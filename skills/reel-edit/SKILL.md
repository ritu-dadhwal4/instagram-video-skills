---
name: reel-edit
description: Router for all video editing. Use when the creator says "edit this reel", "edit this video", "cut this footage", or drops raw footage and asks for a finished video. Picks the edit format and runs the 10-stage pipeline in order.
---
# reel-edit (the router)

**In plain words:** this is the front door. The creator says "edit this reel"; this skill decides which look to use and then calls the other skills one by one, in a fixed order, so no step is skipped.

## Folder for every edit
`edits/<video-name>/` with `raw/` (main footage, untouched), `raw/extra/` (the creator's own extra clips, untouched), `work/` (transcript.json, cuts.json, asset-plan.md, geometry.json), `assets/` (graphics, b-roll, sfx), `out/` (renders). Never modify files in `raw/`.

## Ask first: the brief (one message, before any work)
The creator does not call the skills one by one. They say "edit this reel" and answers these seven questions once; then the pipeline runs on its own. Ask them with AskUserQuestion (it takes 4 questions per call, so use two calls back to back), with the recommended option first. Skip any already answered in their message.
1. **Footage** - the main video, and any extra clips (screen recordings, product shots, other takes, phone b-roll). Ask only: "Any other clips you want in this reel? Just attach them." Do NOT ask where each goes; asset-plan matches them and shows a clip map to confirm.
2. **Where it goes** - Instagram reel (9:16), YouTube long (16:9), or both; target length.
3. **Editing style** - offer the 2 or 3 formats from the table below that fit this footage, each with a one-line description of how it looks, and name the one you recommend. They pick.
4. **Caption style** - two picks from caption-align: how the words arrive (word pop, karaoke...) and the Instagram look (Classic, Strong, Typewriter...). They pick both.
5. **Music and sound effects** - none / effects only / effects + music.
6. **Editor to open it in afterwards** - HyperFrames (recommended: a timeline they can drag and trim in), Remotion, or Palmier Pro (needs macOS 26 or newer and its MCP connected). Before offering Palmier Pro, check that its tools are available in this session; if not, still list it but mark it "not connected on this Mac" and explain in one line. The edit is built in this editor, so it can be changed by hand later.
7. **Look (design file)** - ask this FIRST, before the style questions, because it decides the colours of cards, captions and highlights. "Do you have a design file for your reels (`design.md`), reference pictures (Pinterest saves, screenshots of reels you like) or brand colour codes?" Three ways in:
   - a `design.md` → use it as is;
   - reference images or hex codes → read them, write `design.md` from [design.example.md](design.example.md) (colours as hex, fonts, caption look, card shape), show it in one short block and get a yes;
   - nothing → offer 3 or 4 themes from [themes.md](themes.md) that suit this footage, each with its colours in one line, recommended first. They pick one; write it out as `design.md`.
   Save `design.md` next to their videos so the next reel skips this question. *Why: a reel with no agreed look gets random colours, and every later reel looks different.*
   When a design file exists, offer only caption looks that fit it (its fonts and colours), still as options.
If there is no `brand.md` yet, also ask for the name spellings (brand, product, tools) and create it from brand.example.md.
Copy attached clips into `raw/` (main) and `raw/extra/` (extras). Save the answers in `work/brief.md`. After this they are asked only twice more: the yes on the asset plan (stage 0), and the yes on the b-roll picks (stage 4).

## Pick the format
| They say / footage is | Format skill |
|---|---|
| talking head + screen recording | split-screen |
| talking head, captions only, fast | caption-edit |
| cut-out head over graphics | layered-head-edit |
| list of tools / tips / steps | card-list-edit |
| voice-over, no face | broll-style-edit |
| explainer with paper cards sliding in | paper-drawer-edit |
| clean white canvas explainer | whiteout-edit |
| day-in-life, many locations | vlog-edit |
| YouTube, over 3 minutes, 16:9 | longform-edit |
| one take listing features / options / numbers, no screen to show | board-build-edit |
Use this table to choose which formats to OFFER in question 3. Never start an edit on a format the creator has not picked.

## The order (never reorder, never skip 0, 2, 9, 10)
0. asset-plan → STOP and wait for the creator's yes
1. shortform-cutaway (rough cut)
2. cut-audit
3. take-geometry
4. screen-capture, broll-select (free stock from the internet first; genvideo only for what stock cannot supply), design-asset
5. the format skill + mg-kit
6. caption-align
7. sfx-design
8. shortform-finish, then render-ops
9. reel-review → only then show the draft
10. editor-handoff → opens the project in the chosen editor for human review; the final file is made only when the creator says "final"

## After the notes
Fix the video AND add the note as a rule (with its reason) to the skill that owns that stage. A note that is fixed but not written down will come back.
