#!/usr/bin/env bash
# Draft render: picture, then the cleaned voice (no music, no sound effects). Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_diwali-opinion_reels_9x16_v1.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/voice.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -af "apad=whole_dur=136.767" -t 136.767 -movflags +faststart "$OUT" >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
