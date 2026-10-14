---
name: broll-select
description: Stage 4. Use to pick supporting footage (b-roll) for lines where neither face nor screen fits - from the creator's own clips first, then free stock libraries on the internet (Pexels, Pixabay, Mixkit, Coverr), and AI-generated clips only as a last resort.
---
# broll-select (stage 4)

**In plain words:** b-roll is the extra footage shown while the voice keeps talking, like hands typing or a city street. This skill picks it.

## Where to look, in this order
1. The creator's own clips in `raw/extra/` (placed in the asset plan). Use these wherever they fit before searching anywhere.
2. Free stock libraries on the internet. Search each with 2 or 3 different wordings of what the line shows:
   - Pexels Videos (pexels.com/videos)
   - Pixabay (pixabay.com/videos)
   - Mixkit (mixkit.co/free-stock-video)
   - Coverr (coverr.co)
   - Videvo (videvo.net) - free-licence clips only, some need credit
3. genvideo - ONLY for rows where step 2 found nothing that shows the line. Say which searches failed.

## Steps
1. Take the `broll` rows from the asset plan.
2. For each row, search in the order above with the browser. Prefer vertical clips for reels, 1080p or higher.
3. Open the clip's page and read its licence line. Do not assume from the site name.
4. Show the creator the picks in one table: `line · clip link · site · length · licence`, with up to 2 alternatives per line. WAIT for their yes before downloading anything.
5. Download the approved clips to `assets/broll/`, and record `file · page URL · site · licence · date` in `assets/broll/SOURCES.md`.
6. Sample frames (learn-style/scripts/sample_frames.sh) to confirm the clip shows what the thumbnail promised, then trim to the line it covers.

## Rules
- Real stock footage first, generated clips last. *Why: real footage is free and looks real; AI clips cost credits and often look off.*
- Only clips free for commercial use without payment. Skip anything marked premium, editorial-only or watermarked.
- Never download from YouTube, Instagram or another creator's video.
- A b-roll clip must show what the line says. Decorative footage that says nothing is cut.
- 1.5 to 4 seconds per clip. Shorter flickers, longer bores.
- No recognisable private person as the main subject, no visible brand logo.
- No licence recorded, no use.
