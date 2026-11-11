#!/bin/bash
# full final render of secret-store-9x16, fully detached; then the upload copy (H.264 + AAC, faststart); writes DONE or FAILED
cd /home/user/Nxtlvl-Social/secret-store-9x16 || exit 1
S=/tmp/secret-store-render; mkdir -p $S renders
F=renders/nxtlvl_secret-store_reels_9x16_final.mp4; U=renders/nxtlvl_secret-store_reels_9x16_v1.mp4
rm -f $F $U $S/render.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=300 npx --yes hyperframes@0.8.203 render "$PWD" --quality delivery --workers 4 --fps 30 -o $F < <(sleep infinity) > $S/render.log 2>&1 \
  && ffmpeg -v error -y -i $F -c:v libx264 -preset veryfast -crf 19 -maxrate 12M -bufsize 24M -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 256k $U >> $S/render.log 2>&1; then
  echo DONE > $S/render.status
else
  echo FAILED > $S/render.status
fi
