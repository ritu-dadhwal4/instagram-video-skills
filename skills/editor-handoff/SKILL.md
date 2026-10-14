---
name: editor-handoff
description: Stage 10, the human review. Use after reel-review passes - opens the edit as a project in HyperFrames Studio, Remotion Studio or Palmier Pro so the creator can watch it and change anything by hand, collects their notes, and only exports the final file when they say "final".
---
# editor-handoff (stage 10, your review)

**In plain words:** nothing is final until a person says so. The edit opens in a real video editor, so the creator can watch it, drag a clip, trim a cut or change a caption by hand, or just type notes. Only when they say "final" is the finished file made.

## Steps
1. Render a DRAFT (`out/<name>-draft-v<N>.mp4`) and open the project in the editor chosen in the brief:
   | Editor | Open with | the creator can change by hand |
   |---|---|---|
   | HyperFrames (default) | `npx hyperframes preview` in the project folder; it opens HyperFrames Studio | trim, split, move and retime clips on a timeline; edit text; volume |
   | Remotion | `npx remotion studio` | play and scrub; change text, colours and timings from the props panel; deeper changes are code |
   | Palmier Pro | through Palmier Pro's MCP tools (Mac with macOS 26+, Palmier Pro open, MCP connected) | the full Palmier Pro timeline |
   If Palmier Pro's MCP tools are not available in this session, say so and open HyperFrames instead. Never claim the project is open without seeing the editor start.
2. Tell the creator, in 4 lines or fewer: where it opened, that they can change anything there, that they can also just type notes ("cut at 0:14 is abrupt"), and to say **final** when happy.
3. Wait. Do not render the final file on your own.
4. On each round of notes: FIRST re-read the project files (and in HyperFrames, `npx hyperframes preview --context --json --context-fields selection` to see what they selected). Keep every hand edit they made. Apply the notes, re-run cut-audit if any cut moved and caption-align if timing moved, and show the new draft.
5. On **final**: render-ops on the full-quality export, reel-review once more, then save `out/final.mp4` and say what was checked.

## Rules
- A hand edit in the editor always beats Claude's version. Never overwrite it, never "tidy" it back. *Why: they changed it on purpose.*
- Every note becomes a rule in the skill that owns it (see reel-edit "After the notes").
- Notes on the final file are a new round, not a re-export of the old one.
