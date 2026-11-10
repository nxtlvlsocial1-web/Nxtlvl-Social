#!/usr/bin/env bash
# Draft render: the overlay composition over the footage, then the footage's own audio (his music) muxed back
# on, unchanged. Run detached:  setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_workout-overlay_reels_9x16_v1.mp4
LOG=renders/draft.log
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > $LOG 2>&1
echo "EXIT $?" >> $LOG
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/orig.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$OUT" >> $LOG 2>&1
echo "MUX EXIT $?" >> $LOG
