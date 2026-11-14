#!/bin/bash
# preview render of creedom-i-wish-9x16 (24 fps, draft quality: enough to judge the flying), fully detached; then an upload copy; writes DONE or FAILED
cd /home/user/Nxtlvl-Social/creedom-i-wish-9x16 || exit 1
mkdir -p /tmp/creedom-preview renders
rm -f /home/user/Nxtlvl-Social/creedom-i-wish-9x16/renders/nxtlvl_creedom-i-wish_reels_9x16_preview.mp4 /tmp/creedom-preview/render.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=300 npx --yes hyperframes@0.8.203 render "$PWD" --quality draft --workers 4 --fps 24 -o renders/nxtlvl_creedom-i-wish_reels_9x16_preview.mp4 < <(sleep infinity) > /tmp/creedom-preview/render.log 2>&1 \
  && ffmpeg -v error -y -i renders/nxtlvl_creedom-i-wish_reels_9x16_preview.mp4 -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k renders/nxtlvl_creedom-i-wish_reels_9x16_preview_upload.mp4 >> /tmp/creedom-preview/render.log 2>&1; then
  echo DONE > /tmp/creedom-preview/render.status
else
  echo FAILED > /tmp/creedom-preview/render.status
fi
