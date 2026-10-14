#!/bin/bash
# Pull still frames from a video so they can be looked at one by one.
# usage: sample_frames.sh <video> <out-dir> [frames-per-second, default 2]
set -euo pipefail
video="$1"; out="$2"; fps="${3:-2}"
mkdir -p "$out"
ffmpeg -hide_banner -loglevel error -y -i "$video" -vf "fps=${fps},scale=480:-2" -q:v 4 "$out/f_%05d.jpg"
count=$(ls "$out" | wc -l | tr -d ' ')
echo "$count frames at ${fps} fps in $out (frame N is at (N-1)/${fps} seconds)"
