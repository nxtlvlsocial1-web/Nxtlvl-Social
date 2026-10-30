#!/usr/bin/env bash
# The draft preview for approval. Run it detached (never as a time-limited background job):
#   setsid nohup bash build/render_preview.sh > /dev/null 2>&1 < /dev/null &
# The renderer lowers the audio, so the mastered mix is put back in afterwards.
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
OUT=renders/nxtlvl_console-continue_reels_9x16_preview.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/raw_preview.mp4 > renders/preview.log 2>&1
ffmpeg -v error -y -i renders/raw_preview.mp4 -i assets/audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$OUT" >> renders/preview.log 2>&1
echo "EXIT $?" >> renders/preview.log
