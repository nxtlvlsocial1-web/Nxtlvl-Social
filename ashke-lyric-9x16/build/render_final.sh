#!/usr/bin/env bash
# Delivery render. Run detached: setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/section.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 16 -maxrate 16M -bufsize 32M \
  -pix_fmt yuv420p -profile:v high -c:a aac -b:a 320k -shortest -movflags +faststart renders/nxtlvl_ashke-lyric_reels_9x16_v2.mp4 >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
