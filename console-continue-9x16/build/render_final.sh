#!/usr/bin/env bash
# The final, delivery-quality render. Run it detached (never as a time-limited background job):
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
# The renderer lowers the audio, so the mastered mix is muxed back in with the delivery encode.
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 16 -maxrate 14M -bufsize 28M \
  -pix_fmt yuv420p -profile:v high -c:a aac -b:a 320k -shortest -movflags +faststart renders/nxtlvl_console-continue_reels_9x16_v1.mp4 >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
