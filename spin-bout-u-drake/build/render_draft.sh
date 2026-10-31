#!/usr/bin/env bash
# Draft preview for approval (fast, lower quality), with the song. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/section.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 26 \
  -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart renders/preview_spin-bout-u_1x1_v8.mp4 >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
