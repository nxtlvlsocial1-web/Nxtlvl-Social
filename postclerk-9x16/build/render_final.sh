#!/bin/bash
# final render of postclerk-9x16 (30 fps, delivery quality), fully detached; then an upload copy; writes DONE or FAILED
cd /home/user/Nxtlvl-Social/postclerk-9x16 || exit 1
mkdir -p /tmp/postclerk-final renders
rm -rf /home/user/Nxtlvl-Social/postclerk-9x16/renders/.hf-segments
rm -f /home/user/Nxtlvl-Social/postclerk-9x16/renders/postclerk_metricool-alt_reels_9x16_v1.mp4 /tmp/postclerk-final/render.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 npx --yes hyperframes@0.8.203 render "$PWD" --quality delivery --workers 4 --fps 30 -o renders/postclerk_metricool-alt_reels_9x16_v1.mp4 < <(sleep infinity) > /tmp/postclerk-final/render.log 2>&1 \
  && ffmpeg -v error -y -i renders/postclerk_metricool-alt_reels_9x16_v1.mp4 -c:v libx264 -preset veryfast -crf 19 -maxrate 10M -bufsize 20M -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 256k renders/postclerk_metricool-alt_reels_9x16_v1_upload.mp4 >> /tmp/postclerk-final/render.log 2>&1; then
  echo DONE > /tmp/postclerk-final/render.status
else
  echo FAILED > /tmp/postclerk-final/render.status
fi
