---
name: mg-kit
description: The motion-graphics kit. Use whenever an edit needs animation - how cards enter, how text pops, timing and easing values, brand colours and fonts. Every format skill builds on this.
---
# mg-kit (motion-graphics kit)

**In plain words:** the box of ready-made moves. Instead of inventing a new animation each time, every video uses the same small set, so all of the creator's videos feel like one family.

## Tokens
- `design.md` (from the reel-edit brief: their own file, their reference pictures, or a theme from reel-edit/themes.md) wins over every default below.
- Colours and fonts: read them from the creator's brand kit (`brand.md` in the edit folder or project root; see brand.example.md). Do not hard-code new ones.
- Frame rate 30. Reel 1080x1920. Long-form 1920x1080.

## Moves (the only ones allowed)
| Move | Use for | Timing |
|---|---|---|
| pop-in | a word or sticker | 6 frames, slight overshoot |
| slide-up | a card entering | 10 frames, ease-out |
| wipe | changing a full screen | 8 frames |
| push-in | slow emphasis on face | 2 to 4% over the whole cut |
| highlight | underline or box on a word | 8 frames, drawn left to right |
| ghost-then-fill | a value on a board (board-build-edit) | empty dashed box 15 frames before the value pops in. *Why: measured in the reference; the eye is already there when the number lands.* |
| file-away | a finished point moving into its summary slot (board-build-edit) | 12 to 15 frames, blur + sideways wipe out, slot fills with a pop-in. *Why: keeps one take moving without a cut.* |

## Rules
- Never zoom AT a cut. Zooms start and end inside one cut. *Why: a zoom on the cut point advertises the cut.*
- Different registers (face → screen → card) hard-cut. Never crossfade. *Why: a crossfade between two different kinds of picture looks like a mistake.*
- Things enter with motion and leave with a cut.
- Build in the editor chosen in the brief: HyperFrames (default; use the hyperframes skills, keep one element kind per track so the Studio timeline stays editable), Remotion (use the remotion skills), or Palmier Pro (through its MCP tools). Animate from frame numbers or a paused timeline, never free-running CSS transitions.
- New move needed? Add it here first, with its reason, then use it.
