#!/bin/bash
# preview render of postclerk-9x16 (30 fps, draft quality), fully detached; then an upload copy; writes DONE or FAILED
cd /home/user/Nxtlvl-Social/postclerk-9x16 || exit 1
mkdir -p /tmp/postclerk-preview renders
rm -rf /home/user/Nxtlvl-Social/postclerk-9x16/renders/.hf-segments
rm -f /home/user/Nxtlvl-Social/postclerk-9x16/renders/postclerk_metricool-alt_reels_9x16_preview.mp4 /tmp/postclerk-preview/render.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 npx --yes hyperframes@0.8.203 render "$PWD" --quality draft --workers 4 --fps 30 -o renders/postclerk_metricool-alt_reels_9x16_preview.mp4 < <(sleep infinity) > /tmp/postclerk-preview/render.log 2>&1 \
  && ffmpeg -v error -y -i renders/postclerk_metricool-alt_reels_9x16_preview.mp4 -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k renders/postclerk_metricool-alt_reels_9x16_preview_upload.mp4 >> /tmp/postclerk-preview/render.log 2>&1; then
  echo DONE > /tmp/postclerk-preview/render.status
else
  echo FAILED > /tmp/postclerk-preview/render.status
fi
