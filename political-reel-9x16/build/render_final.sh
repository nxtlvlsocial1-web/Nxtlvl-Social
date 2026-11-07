#!/usr/bin/env bash
# Final render: picture, then the cleaned voice (no music, no sound effects). Run detached:
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_diwali-opinion_reels_9x16_v3.mp4
npx --yes hyperframes@0.8.203 render --quality high -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/voice.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 19 -maxrate 6M -bufsize 12M -pix_fmt yuv420p \
  -c:a aac -b:a 192k -af "apad=whole_dur=124.467" -t 124.467 -movflags +faststart "$OUT" >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
