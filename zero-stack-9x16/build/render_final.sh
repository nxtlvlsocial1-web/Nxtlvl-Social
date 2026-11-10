#!/bin/bash
# full final render of zero-stack-9x16, fully detached; then the upload copy; writes DONE or FAILED
cd /home/user/Nxtlvl-Social/zero-stack-9x16 || exit 1
S=/tmp/zero-stack-render; mkdir -p $S renders
rm -f renders/nxtlvl_zero-stack_reels_9x16_final.mp4 renders/nxtlvl_zero-stack_reels_9x16_final_upload.mp4 $S/render.status
if HYPERFRAMES_NO_TELEMETRY=1 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=300 npx --yes hyperframes@0.8.203 render "$PWD" --quality delivery --workers 4 --fps 30 -o renders/nxtlvl_zero-stack_reels_9x16_final.mp4 < <(sleep infinity) > $S/render.log 2>&1 \
  && ffmpeg -v error -y -i renders/nxtlvl_zero-stack_reels_9x16_final.mp4 -c:v libx264 -preset veryfast -crf 20 -maxrate 10M -bufsize 20M -pix_fmt yuv420p -profile:v high -movflags +faststart -c:a aac -b:a 256k renders/nxtlvl_zero-stack_reels_9x16_final_upload.mp4 >> $S/render.log 2>&1; then
  echo DONE > $S/render.status
else
  echo FAILED > $S/render.status
fi
