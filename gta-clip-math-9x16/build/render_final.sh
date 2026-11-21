#!/bin/bash
# Full render of gta-clip-math-9x16, fully detached; then the final ffmpeg encode (H.264 + AAC, 1080x1920, 30 fps).
# Launch:  setsid nohup bash build/render_final.sh > /dev/null 2>&1 &      Writes renders/reel.mp4 and renders/render.status
cd "$(dirname "$0")/.." || exit 1
S=renders; mkdir -p $S
rm -f $S/raw.mp4 $S/reel.mp4 $S/render.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=300 npx --yes hyperframes@0.9.72 render "$PWD" --quality delivery --workers 4 --fps 30 -o $S/raw.mp4 < <(sleep infinity) > $S/render.log 2>&1 \
  && ffmpeg -v error -y -i $S/raw.mp4 -i assets/audio/mix.wav -map 0:v:0 -map 1:a:0 \
       -c:v libx264 -preset slow -crf 20 -maxrate 14M -bufsize 28M -profile:v high -level 4.2 -pix_fmt yuv420p -r 30 -movflags +faststart \
       -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -ac 2 -t 38.7 $S/reel.mp4 >> $S/render.log 2>&1; then
  echo DONE > $S/render.status
else
  echo FAILED > $S/render.status
fi
