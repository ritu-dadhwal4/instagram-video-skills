---
name: render-ops
description: Stage 8. Use to export the final video file and verify it - resolution, frame rate, codec, and loudness of -14 LUFS measured on the finished file with scripts/loudness.sh.
---
# render-ops (stage 8)

**In plain words:** press export, then prove the file is right. LUFS is simply "how loud the whole video is"; Instagram and YouTube expect about -14.

## Steps
1. Render to `out/<name>-v<N>.mp4`: H.264, 30 fps, AAC 48 kHz. Reel 1080x1920, long-form 1920x1080.
2. Measure: `.claude/skills/render-ops/scripts/loudness.sh measure out/<file>`.
3. If not within -14 ±1 LUFS: `loudness.sh fix out/<file>` and measure the new file.
4. Confirm with ffprobe: size, fps, duration, and that audio and video lengths match within 1 frame.

## Rules
- Measure the FINAL file, not the project. *Why: loudness set inside the editor is not what the export contains.*
- Never overwrite a render; bump the version number.
- True peak at or below -1.5 dB.
- A render is not "done" until reel-review passes.
