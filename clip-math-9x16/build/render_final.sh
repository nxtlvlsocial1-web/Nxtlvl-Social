#!/bin/bash
# Final render of clip-math-9x16, fully detached (setsid nohup + held-open stdin + HYPERFRAMES_RENDER_DETACHED=1),
# then the ffmpeg delivery encode to out/reel.mp4 (H.264 High, yuv420p, 30 fps CFR, AAC 48 kHz, faststart).
# Launch:  setsid nohup bash build/render_final.sh > /dev/null 2>&1 &     Writes DONE or FAILED to $S/render.status
cd "$(dirname "$0")/.." || exit 1
S=/tmp/clip-math-render; mkdir -p $S renders out
rm -f renders/clip-math_master.mp4 out/reel.mp4 $S/render.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 npx --yes hyperframes@0.9.72 render "$PWD" --quality delivery --fps 30 --workers 3 -o renders/clip-math_master.mp4 < <(sleep infinity) > $S/render.log 2>&1 \
  && ffmpeg -v error -y -i renders/clip-math_master.mp4 -t 40 -c:v libx264 -preset slow -crf 17 -maxrate 14M -bufsize 28M -profile:v high -level 4.2 \
       -pix_fmt yuv420p -r 30 -fps_mode cfr -g 60 -movflags +faststart -c:a aac -b:a 192k -ar 48000 -ac 2 out/reel.mp4 >> $S/render.log 2>&1; then
  echo DONE > $S/render.status
else
  echo FAILED > $S/render.status
fi
