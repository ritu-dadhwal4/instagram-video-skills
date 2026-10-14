#!/bin/bash
# Measure, or fix, how loud a finished video is. Target: -14 LUFS, peak -1.5 dB.
# usage: loudness.sh measure <file>
#        loudness.sh fix <file>      (writes <file>-14lufs.mp4, video untouched)
set -euo pipefail
mode="$1"; file="$2"
measure() {
  ffmpeg -hide_banner -nostats -i "$1" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 \
    | awk '/^\{/,/^\}/'
}
case "$mode" in
  measure)
    json=$(measure "$file")
    i=$(echo "$json" | sed -n 's/.*"input_i" : "\(.*\)".*/\1/p')
    tp=$(echo "$json" | sed -n 's/.*"input_tp" : "\(.*\)".*/\1/p')
    echo "loudness: $i LUFS   true peak: $tp dB   (target -14 LUFS, peak <= -1.5)"
    awk -v i="$i" 'BEGIN { if (i >= -15 && i <= -13) print "PASS"; else print "FAIL - run: loudness.sh fix <file>" }'
    ;;
  fix)
    json=$(measure "$file")
    g() { echo "$json" | sed -n "s/.*\"$1\" : \"\(.*\)\".*/\1/p"; }
    out="${file%.*}-14lufs.mp4"
    ffmpeg -hide_banner -loglevel error -y -i "$file" -c:v copy \
      -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" \
      -c:a aac -b:a 192k -ar 48000 "$out"
    echo "wrote $out"; "$0" measure "$out"
    ;;
  *) echo "usage: loudness.sh measure|fix <file>"; exit 1;;
esac
