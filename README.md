# Instagram Video Skills for Claude

Edit a whole Instagram reel (or a YouTube video) by talking to Claude. You film. Claude cuts the footage, removes the silences and fumbles, finds b-roll, designs the cards, adds captions and sound, exports the file, and has a second model check it before you see it.

This is not one skill. It is **28 small skills that work as a team**. One of them is the "front door" that calls the others in the right order. You only ever say one sentence:

> edit this reel

> **Status: v0.1, early.** The three helper scripts are tested. The full pipeline has not yet been run end to end on real footage in public; a dry run is coming and this page will be updated with what it found. Expect to give notes.

---

## Contents
1. [What is a skill?](#what-is-a-skill)
2. [What you need](#what-you-need)
3. [Install](#install)
4. [How one edit goes, step by step](#how-one-edit-goes-step-by-step)
5. [The seven questions it asks you](#the-seven-questions-it-asks-you)
6. [Editing styles you can pick](#editing-styles-you-can-pick)
7. [Caption styles you can pick](#caption-styles-you-can-pick)
8. [Where b-roll comes from](#where-b-roll-comes-from)
9. [Every skill, explained](#every-skill-explained)
10. [Teach it a style you like](#teach-it-a-style-you-like)
11. [Giving notes](#giving-notes-this-is-how-it-gets-better)
12. [What it cannot do](#what-it-cannot-do)
13. [Credits](#credits)

---

## What is a skill?

A skill is a folder with one text file in it, `SKILL.md`. The file is a checklist with rules, written in plain English. When you give Claude a task that matches, Claude reads the file and follows it. Some skills also carry a small script.

Claude is already clever. What it lacks is your taste and a memory of past mistakes. A skill is where both are written down. Every rule in these files has its reason next to it, like:

> Never zoom at a cut. *Why: a zoom on the cut point advertises the cut.*

Open any `SKILL.md` here. Each one starts with a line called **In plain words** that says what it does without jargon.

## What you need

| Thing | Why | Cost |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) (desktop app or terminal) | Runs the skills | Claude Pro subscription |
| `ffmpeg` | Cuts video, reads audio, exports | Free |
| `python3` | Runs the cut checker | Free (already on a Mac) |
| `whisperx` | Hears each word and the exact moment it is spoken | Free |
| Node.js | Lets Claude build the edit in [HyperFrames](https://github.com/heygen-com/hyperframes) or [Remotion](https://www.remotion.dev) | Free |
| HyperFrames skills (recommended) | So the edit opens in HyperFrames Studio, where you can trim and drag clips: `npx skills add heygen-com/hyperframes` | Free |
| [Palmier Pro](https://palmier.io) (optional) | A regular Mac video editor Claude can drive. Needs **macOS 26 or newer on an Apple Silicon Mac** (no Windows or Intel version). See [Connect Palmier Pro](#connect-palmier-pro-optional) | Free to start |

On a Mac:

```bash
brew install ffmpeg node
```

```bash
pip3 install whisperx
```

## Install

Skills live in a folder called `.claude/skills` inside the folder where you keep your videos.

```bash
git clone https://github.com/ritu-dadhwal4/instagram-video-skills.git
```

```bash
mkdir -p ~/Videos/reels/.claude && cp -R instagram-video-skills/skills ~/Videos/reels/.claude/skills
```

```bash
cp instagram-video-skills/brand.example.md ~/Videos/reels/brand.md
```

Open `brand.md` and fill in the spellings of your brand and product names (colours and fonts go in `design.md`, which Claude can write for you on the first reel). Then open Claude Code in `~/Videos/reels`. Type `/skills` and you should see `reel-edit` and the others listed.

### Connect Palmier Pro (optional)

Palmier Pro runs a small editor server on your own Mac while the app is open. With Palmier Pro open, connect Claude Code to it once:

```bash
claude mcp add --transport http --scope user palmier-pro http://127.0.0.1:19789/mcp
```

Then `claude mcp list` should show `palmier-pro` as connected. If you use the Claude desktop app's chat instead, Palmier Pro ships a one-click connector (`palmier-pro.mcpb`) inside the app. If it is not connected, the skills still offer Palmier Pro but say it isn't connected, and you can pick HyperFrames or Remotion.

## How one edit goes, step by step

Put your raw footage in a folder, then say **"edit this reel"** and point to the file. From there:

| When | What happens | Skill | Do you do anything? |
|---|---|---|---|
| Start | Claude asks seven questions, in two quick rounds | `reel-edit` | **Yes: answer them** (style and captions are chosen here) |
| Stage 0 | Lists every visual the video needs and fact-checks what you said | `asset-plan` | **Yes: read the plan, say yes** |
| Stage 1 | Rough cut: best take of each line, silences and fumbles out | `shortform-cutaway` | No |
| Stage 2 | Checks the real audio at every cut so no word is chopped | `cut-audit` | No |
| Stage 3 | Finds your face in every shot so text never covers it | `take-geometry` | No |
| Stage 4 | Records screens, searches free b-roll, designs cards | `screen-capture` `broll-select` `design-asset` | **Yes: approve the b-roll picks** |
| Stage 5 | Builds the look you picked | your format skill + `mg-kit` | No |
| Stage 6 | Captions, in the style you picked, on the exact frame | `caption-align` | No |
| Stage 7 | Sound effects and music | `sfx-design` | No |
| Stage 8 | Final polish, export, loudness check | `shortform-finish` `render-ops` | No |
| Stage 9 | A different model watches the draft and lists problems; Claude fixes them | `reel-review` | No |
| Stage 10 | The edit opens in your editor (HyperFrames Studio, Remotion Studio or Palmier Pro). Change anything by hand, or type notes. The final file is made only when you say **final** | `editor-handoff` | **Yes: review, tweak, say final** |

So you are needed four times: the questions, the plan with the clip map, the b-roll picks, and your review at the end. Nothing is final until you say so. Everything between runs by itself.

Files for each edit are kept tidy:

```
edits/my-video/
  raw/      your footage, never changed (extra clips in raw/extra/)
  work/     transcript, cut list, the plan, your answers
  assets/   cards, b-roll, sounds (with their sources)
  out/      the renders, numbered v1, v2, v3
```

## The seven questions it asks you

They arrive in two quick rounds, before any work starts. The first one is about the look.

0. **Look (design file).** Do you have a `design.md`, reference pictures (Pinterest saves, screenshots of reels you like) or brand colour codes? Give any of them and Claude writes a `design.md` and shows it to you. Have nothing? It offers three or four ready themes from [themes.md](skills/reel-edit/themes.md) (Clean White, Midnight Tech, Paper Craft, Pastel Pop, Bold Mono, Soft Earth), each with its colours, and you pick one. The file is saved next to your videos, so the next reel skips this question. Template: [design.example.md](skills/reel-edit/design.example.md).


1. **Footage.** Your main video, plus any extra clips you want used: screen recordings, product shots, other takes, phone b-roll. Just attach them. You don't have to say where each one goes.

Claude then matches your clips to the script itself and shows you a **clip map**:

```
Your clips
1. laptop typing       -> L2 "I just typed: edit this reel"
2. GitHub page scroll  -> L6 "28 skills, all free on GitHub"
3. coffee cup          -> not used (nothing in the script fits)

Reply "ok", or change any line like:  "1 -> L3"  ·  "3 -> L5"  ·  "drop 2"
```

Reply **ok**, or move a clip with one short line. Tip: name a file after the word it belongs to (`github.mp4`) and it lands there automatically.
2. **Where it goes.** Instagram reel (tall), YouTube (wide), or both. How long?
3. **Editing style.** Claude offers the two or three styles that suit your footage, says how each looks, and recommends one. You pick.
4. **Caption style.** Two picks: how the words arrive, and how the letters look.
5. **Sound.** None, sound effects only, or effects plus music.
6. **Editor.** Which app you want to open and tweak the edit in afterwards:
   - **HyperFrames**: free, open source; Studio timeline to trim, split and drag clips.
   - **Remotion**: free for individuals; preview with a settings panel, bigger changes are code.
   - **Palmier Pro**: a regular Mac video editor; needs macOS 26+ and the connection above.

If you already said some of this in your message, it skips those.

## Editing styles you can pick

| Style | How it looks | Good for | File |
|---|---|---|---|
| Split screen | You in one half, the screen in the other | Tutorials, tool demos | [split-screen](skills/split-screen/SKILL.md) |
| Captions | Just you, with big captions doing the work | Opinions, stories, quick tips | [caption-edit](skills/caption-edit/SKILL.md) |
| Layered head | You cut out, standing in front of the content | When you should stay on screen | [layered-head-edit](skills/layered-head-edit/SKILL.md) |
| Card list | One card per item, with a counter | "5 tools", "7 tips" | [card-list-edit](skills/card-list-edit/SKILL.md) |
| B-roll | Your voice over footage, no face | Faceless explainers | [broll-style-edit](skills/broll-style-edit/SKILL.md) |
| Paper drawer | Paper cards slide in like a drawer | Points, steps, comparisons | [paper-drawer-edit](skills/paper-drawer-edit/SKILL.md) |
| Whiteout | Plain white canvas, big words and numbers | Concepts, numbers | [whiteout-edit](skills/whiteout-edit/SKILL.md) |
| Board build | You in a small window on top; a board below fills in as you talk | One-take explainers | [board-build-edit](skills/board-build-edit/SKILL.md) |
| Vlog | A day told as a story, music underneath | Vlogs, travel, behind the scenes | [vlog-edit](skills/vlog-edit/SKILL.md) |
| Long form | Wide video in chapters | YouTube, over 3 minutes | [longform-edit](skills/longform-edit/SKILL.md) |

Most layouts here are sensible starting numbers, not measurements. Use [learn-style](#teach-it-a-style-you-like) on a reel you love to replace them with real ones.

## Caption styles you can pick

**Pick one: how the words arrive**

| Style | How it looks | Good for |
|---|---|---|
| Word pop | 1 to 3 big words in the centre, popping in as you say them | Fast reels, hooks |
| Karaoke line | A whole line; the spoken word lights up | Explainers |
| Subtitle bar | Small plain line at the bottom | Long videos |
| Boxed | Words on a solid rounded box | Busy footage |
| Keywords only | Only the important word or number | Styles that already have cards |
| None | No captions | Clean look |

**Pick one: the Instagram look**

| Look | How it looks |
|---|---|
| Classic | Clean rounded letters; the safest |
| Modern | All capitals, wide spacing |
| Neon | Glowing handwriting; one or two words only |
| Typewriter | Typewriter letters on a box |
| Strong | Very heavy italic; best over busy video |
| Elegant | Fine serif |
| Directional | Plain narrow letters; long lines |
| Signature | Handwritten script; names only |
| Bubble | Fat rounded letters; playful |
| Deco | Decorative capitals; titles only |
| Instagram's own sticker | Claude adds nothing; you add the Captions sticker in the app |

These are lookalikes made from open fonts. Instagram's own fonts cannot be downloaded. Instagram publishes no official list of its styles and the app changes often, so this list will grow.

## Where b-roll comes from

B-roll is the extra footage shown while your voice keeps going. Claude looks in this order:

1. Your own extra clips, the ones you attached at the start. Always first.
2. Free stock libraries: [Pexels](https://www.pexels.com/videos/), [Pixabay](https://pixabay.com/videos/), [Mixkit](https://mixkit.co/free-stock-video/), [Coverr](https://coverr.co), [Videvo](https://www.videvo.net) (free-licence clips only).
3. An AI-generated clip, only if the searches found nothing, and only after you agree to the cost.

Before downloading, it shows you a table of picks with links and the licence of each. Every clip used is logged in `assets/broll/SOURCES.md` so you can always prove where it came from.

## Every skill, explained

### The front door
| Skill | In plain words |
|---|---|
| [reel-edit](skills/reel-edit/SKILL.md) | Asks the seven questions, then calls every other skill in order. The only one you talk to. |

### The pipeline, in order
| Stage | Skill | In plain words |
|---|---|---|
| 0 | [asset-plan](skills/asset-plan/SKILL.md) | A shopping list before cooking: every picture and graphic needed, and every fact you said checked against the live page. Stops for your yes. |
| 1 | [shortform-cutaway](skills/shortform-cutaway/SKILL.md) | Throws away the bad bits. You said a line three times; it keeps the cleanest. |
| 2 | [cut-audit](skills/cut-audit/SKILL.md) | Listens instead of reading. A transcript can look perfect while a word is cut in half. Comes with a script that checks every cut. |
| 3 | [take-geometry](skills/take-geometry/SKILL.md) | Finds where your face is, so text goes in the empty space. |
| 4 | [screen-capture](skills/screen-capture/SKILL.md) | Records the real site or app you are talking about. |
| 4 | [broll-select](skills/broll-select/SKILL.md) | Finds supporting footage from free libraries and shows you before downloading. |
| 4 | [genvideo](skills/genvideo/SKILL.md) | Last resort: makes a short AI clip when no real footage exists. Asks before spending. |
| 4 | [design-asset](skills/design-asset/SKILL.md) | The designer. Makes title cards, number cards, tool cards in your brand colours. |
| 4 | [omni-restyle](skills/omni-restyle/SKILL.md) | Same clip, new paint: turns footage into a sketch or clay look so everything matches. Optional. |
| 5 | [mg-kit](skills/mg-kit/SKILL.md) | The box of ready-made animations, so all your videos feel like one family. |
| 6 | [caption-align](skills/caption-align/SKILL.md) | Puts each word on screen on the exact frame you say it. |
| 7 | [sfx-design](skills/sfx-design/SKILL.md) | A small sound for each thing that moves, kept quieter than your voice. |
| 8 | [shortform-finish](skills/shortform-finish/SKILL.md) | The last look: is the first second interesting, does anything drag, do colours match? |
| 8 | [render-ops](skills/render-ops/SKILL.md) | Exports the file and proves it is right, including loudness (−14 LUFS, what Instagram and YouTube expect). |
| 9 | [reel-review](skills/reel-review/SKILL.md) | A second pair of eyes. A different model watches the render first, because whoever made a video always thinks it is fine. |
| 10 | [editor-handoff](skills/editor-handoff/SKILL.md) | Nothing is final until you say so. Opens the edit in a real editor so you can change anything by hand, takes your notes, and only then makes the final file. |

### The editing styles
Ten format skills, listed [above](#editing-styles-you-can-pick).

### The teacher
| Skill | In plain words |
|---|---|
| [learn-style](skills/learn-style/SKILL.md) | Show it a reel you love; it works out the recipe and saves it as a new style. |

### The three scripts
| Script | What it does |
|---|---|
| [check_cut_edges.py](skills/cut-audit/scripts/check_cut_edges.py) | Reads the audio around every cut and flags any cut that lands in the middle of a word, with the nearest quiet moment to move it to. |
| [loudness.sh](skills/render-ops/scripts/loudness.sh) | Measures how loud the finished file is and fixes it to −14 LUFS. |
| [sample_frames.sh](skills/learn-style/scripts/sample_frames.sh) | Pulls still frames out of a video so Claude can look at it. |

## Teach it a style you like

Give Claude a reel and say **"learn this edit"**. It looks at two frames every second, labels what is on screen, and measures: how often the face shows, how long each cut lasts, where the text sits, how things enter and leave. It writes those numbers into a new format skill and adds it to the list of styles it offers you.

It learns the **structure** of an edit: timing, layout, proportions. It does not copy anyone's footage, music, logo or graphics, and you should not ask it to.

## Giving notes (this is how it gets better)

After the first version, talk like you would to an editor:

> the cut at 0:14 is abrupt · move the card a little right · sound effects are too loud

Claude fixes the video **and writes the note into the skill as a rule with its reason**. That second part is the whole trick. After a few weeks your skills have your taste in them and you correct less and less.

## What it cannot do

- It does not film. You shoot everything.
- It is an assistant editor, not a button. Expect two or three rounds of notes.
- It cannot post to Instagram for you.
- It will not copy another creator's video, download from YouTube or Instagram, or use clips without a licence.
- Fact-checking covers what can be checked on a live page. Opinions are yours.

## Credits

Built by [Ritu Dadhwal](https://github.com/ritu-dadhwal4) with Claude. MIT licence: use it, change it, share it.
