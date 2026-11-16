#!/bin/bash
# final render of creators100x-plan-9x16 (30 fps, high quality), fully detached; then an upload copy; writes DONE or FAILED
cd /home/user/Nxtlvl-Social/creators100x-plan-9x16 || exit 1
LOGD=/tmp/claude-0/-home-user-Nxtlvl-Social/e31f97b8-b375-54da-91f5-cccc2674e3c4/scratchpad/c100x-final
mkdir -p "$LOGD" renders
rm -rf /home/user/Nxtlvl-Social/creators100x-plan-9x16/renders/.hf-segments
rm -f renders/creators100x_30-days-1-prompt_reels_9x16_final.mp4 renders/creators100x_30-days-1-prompt_reels_9x16_final_upload.mp4 "$LOGD/render.status"
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 npx --yes hyperframes@0.8.203 render "$PWD" --quality high --workers 4 --fps 30 -o renders/creators100x_30-days-1-prompt_reels_9x16_final.mp4 < <(sleep infinity) > "$LOGD/render.log" 2>&1 \
  && ffmpeg -v error -y -i renders/creators100x_30-days-1-prompt_reels_9x16_final.mp4 -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 256k renders/creators100x_30-days-1-prompt_reels_9x16_final_upload.mp4 >> "$LOGD/render.log" 2>&1; then
  echo DONE > "$LOGD/render.status"
else
  echo FAILED > "$LOGD/render.status"
fi
