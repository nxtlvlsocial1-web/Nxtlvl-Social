#!/bin/bash
# final render of creedom-i-wish-9x16 (35 fps, delivery quality), fully detached; then the upload copy; writes DONE or FAILED
cd /home/user/Nxtlvl-Social/creedom-i-wish-9x16 || exit 1
mkdir -p /tmp/creedom-final renders
rm -f /home/user/Nxtlvl-Social/creedom-i-wish-9x16/renders/nxtlvl_creedom-i-wish_reels_9x16_final.mp4 /home/user/Nxtlvl-Social/creedom-i-wish-9x16/renders/nxtlvl_creedom-i-wish_reels_9x16_final_upload.mp4 /tmp/creedom-final/render.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=300 npx --yes hyperframes@0.8.203 render "$PWD" --quality delivery --workers 4 --fps 35 -o renders/nxtlvl_creedom-i-wish_reels_9x16_final.mp4 < <(sleep infinity) > /tmp/creedom-final/render.log 2>&1 \
  && ffmpeg -v error -y -i renders/nxtlvl_creedom-i-wish_reels_9x16_final.mp4 -c:v libx264 -preset veryfast -crf 20 -maxrate 10M -bufsize 20M -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 256k renders/nxtlvl_creedom-i-wish_reels_9x16_final_upload.mp4 >> /tmp/creedom-final/render.log 2>&1; then
  echo DONE > /tmp/creedom-final/render.status
else
  echo FAILED > /tmp/creedom-final/render.status
fi
