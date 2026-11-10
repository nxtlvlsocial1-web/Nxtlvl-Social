#!/usr/bin/env bash
# Final render: the overlay composition over the footage, then the footage's own audio (his music) muxed back
# on, unchanged. Run detached:  setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_workout-overlay_reels_9x16_v1.mp4
LOG=renders/high.log
npx --yes hyperframes@0.8.203 render --quality high -w 3 -o renders/high_master.mp4 > $LOG 2>&1
echo "EXIT $?" >> $LOG
ffmpeg -v error -y -i renders/high_master.mp4 -i assets/audio/orig.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$OUT" >> $LOG 2>&1
echo "MUX EXIT $?" >> $LOG
