---
name: trial-reels-studio
description: Plan Instagram Trial Reels for one reel idea by varying only the hook, and track it on a zoomable whiteboard (FigJam-style) - a top-to-bottom journey from idea to script, hook phone mockups showing the face/product layout and text-overlay position, filming, editing with the instagram-video-skills pipeline, posting and the winning hook. A home board lists every reel board with its status. Use when the user says "trial reels", "trial reels studio", "plan trial reels for <idea>", "which hooks should I test", or reports progress on a reel ("script approved", "filmed", "H3 final", "H3 won").
---

# Trial Reels Studio

An add-on to [instagram-video-skills](https://github.com/ritu-dadhwal4/instagram-video-skills). You share an idea, and this skill writes the script and suggests several **hooks** for the same video. Each trial reel is one hook + the same body + the same CTA. Instagram shows trial reels to non-followers first, so you can test openings without spamming your followers, then share the winner.

The skill plans **hooks only**. The body and CTA come from the script and get no visuals.

## 0. Settings (first run only)

Read `~/.claude/trial-reels-studio/settings.md`. It holds:
- `Hooks folder:` a Google Drive folder link with screenshots of hooks the user likes
- `Home board:` the link to the home board (see step 9)

If the file is missing, ask the user for their Hooks folder link. Tell them to share the folder as **Anyone with the link**. Create the home board, then write both links to the file. Never put one user's links into the skill itself.

## 1. Idea → board

The user brings the idea, so the Idea step starts as done. Create a **new Whiteboard artifact for each reel**: run a quickstart with intent `other`, then publish with the Whiteboard `type_url` and `auto_open: "after_first_write"`. Name it after the reel. Add the reel to the home board with the status **running**.

## 2. Script

Write the script, using the `content-studio` skill if it's installed, or use the user's own. It has a hook placeholder, a body and a CTA. Facts must stay true to the source, because the creator posts publicly. Ask the user to approve it.

## 3. Read the reference hooks

The Drive connector can't list a folder, so open the Hooks folder's public link in the built-in browser:
1. Collect the file ids: `[...document.querySelectorAll('[data-id]')].map(e=>e.getAttribute('data-id'))`. Skip the folder's own id.
2. View each image at `https://drive.google.com/thumbnail?id=<id>&sz=w800` and take a screenshot. View them; don't download them.
3. Note the patterns: the format (table below), where the face sits, the headline's position and style (for example one highlighted word), and the hook angle and language.
4. Tell the user in one line what most of the references have in common.

If the folder is empty or won't open, say so and use the format table. Videos are for body work later, not for this skill.

## 4. Setup questions

Use AskUserQuestion. Name the reel in each question, because the user may only see the dialog. Don't ask what the conversation already answers.
1. **How many hooks?** 2–3, 4–5, 6, 7–10. Ten is the maximum. If they pick a range, choose a number inside it and say which one.
2. **Hook formats** (multi-select, at most 4 options). Offer the formats the references use most first.
3. **CTA line:** offer 2 written from the topic. They can write their own with Other. The CTA is fixed and never tested.

| format id | Looks like | Overlay sits |
|---|---|---|
| `split` | **Visual top, face bottom** (the default split) | on the middle seam |
| `split-top` | Face top, visual bottom (only when asked) | on the middle seam |
| `circle` | Visual full screen, face in a small circle | top 15% |
| `box` | Visual full screen, face in a small rectangle | top 15% |
| `face` | Talking head only | top 15% |
| `face-prop` | Talking head holding a laptop, tablet or phone | top 15% |
| `greenscreen` | Face cut out in front of a screenshot | top 15% |
| `product` | Screen recording or slides only, voice over | top 15% |
| `text` | Big text on a plain colour for the first 2 s | centre |

## 5. Write the hooks

The angles must really differ: problem, before/after, myth-bust, POV, authority, contrarian, result, question, pain. Talking hooks go to split, face or face-prop. Demo hooks go to circle, box, greenscreen or product. For each hook write:
- the spoken line, 12 words or fewer
- the overlay text, 6 words or fewer, in the references' style
- the format
- one scene

**Scenes:** `plain-slides`, `before-after`, `chart-edit`, `chat-screenshot`, `github`, `designed-deck`, `three-decks`, `code-to-file`, `cloud-upload`, `rules-doc`, `messy-slide`, `comment-bubble`. To add one, write an `sc_<name>` function in `scripts/build_board.py`. Use plain shapes only, and never draw people: the face is a purple area with a camera icon.

Don't over-promise. Never claim "one prompt" or a number the source doesn't support.

## 6. The edit prompt (stop 5 on the board)

Fill this in and put it on the board, leaving `H_` for the user to swap per trial reel:

```
edit this reel

Attachments, in this order:
1. Raw video: my main take.
2. Reference video: copy its editing style (layout, pacing and captions).
3. Hook image: the approved hook style. Build the first 3 seconds to match it.
4. Clips (everything after the image): screen recordings and b-roll for the edit.

Open with hook H_: "<hook line>", text overlay "<overlay>", format: <format>.
After the hook, follow my script: the same body and the CTA "<CTA>".
Instagram reel, 9:16, about 30 seconds.
```

The hook image can be a screenshot of that hook's phone mockup on the board, or the reference screenshot it was based on.

## 7. Build the board

1. Write a spec JSON shaped like `examples/example-reel.json`. Save it as `~/.claude/trial-reels-studio/<reel-slug>/spec.json`.
2. Run `python3 <this skill>/scripts/build_board.py spec.json <out_dir> <first_id_number>`. Use 1 for a new board, or the highest existing `e` number + 1 for an existing one. The script checks every drawing and prints the ids in order.
3. Write with `ArtifactData` `batch`, at most 50 writes per call: `board/meta` first, then the elements in the printed order.
4. Save the output as `~/.claude/trial-reels-studio/<reel-slug>/last/`, with a `board.json` holding the board URL and the first id.
5. Don't screenshot or read back the board to check it.

**Board layout:** a journey read top to bottom. A spine of circles joins seven stops: 1 Idea → 2 Script → 3 Hooks → 4 Film → 5 Edit → 6 Post → 7 Winner. Green ✓ = done, yellow = now, white = next.

## 8. Keep the reel board up to date

The spec is the board's state. When something happens, change the spec, re-run the script **with the same first id**, and write only the files that differ from `last/`, as `update` writes with each element's `if_version`. Then replace `last/`.

| User says | Change in the spec |
|---|---|
| "script approved" | `stops.script = "done"`, `stops.hooks = "now"` |
| "I'll film H1, H3, H8" | `picked: true` on those, `false` on the rest, `stops.hooks = "done"`, `stops.film = "now"` |
| "filmed" | `stops.film = "done"`, `stops.edit = "now"` |
| HyperFrames Studio opens for a hook | that hook's `link` = the Studio address (for example `http://localhost:3002`), `edit = "in review"` |
| "H3 final" | that hook's `edit = "final ✓"`. When every picked hook is final: `stops.edit = "done"`, `stops.post = "now"` |
| "posted" | `stops.post = "done"`, `stops.winner = "now"` |
| "H3 won" | the `winner` text names H3, `stops.winner = "done"` |

Localhost addresses show as text to copy. The board can't make `http://` links clickable, and they only open on the user's computer while Studio is running.

## 9. The home board

One Whiteboard lists every reel. Each row has a link card that opens that reel's board, a status (**planned**, **running** or **complete**) and the current step. Its spec lives at `~/.claude/trial-reels-studio/home.json`. Build it with `python3 <this skill>/scripts/build_home.py home.json <out_dir> <first_id_number>` and keep it in sync the same way:
- a new reel → add a row with status `running` and step `2 · Script`
- each stop change on a reel board → update that row's step
- the Winner stop done → status `complete`, step `Winner: H_`

## 10. Reply

In two or three sentences, say what changed on the board, which references shaped the hooks, and what you assumed. Then give the reel board link and the home board link.
