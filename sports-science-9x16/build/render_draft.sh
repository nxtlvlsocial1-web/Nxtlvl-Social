#!/usr/bin/env bash
# Preview render for approval (draft quality), then the sound mix. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
LOG=renders/draft.log
: > $LOG
PREVIEW=1 python3 build/generate.py >> $LOG 2>&1 || { echo "GEN FAILED" >> $LOG; exit 1; }
rm -f renders/master_draft.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/master_draft.mp4 >> $LOG 2>&1
echo "RENDER EXIT $?" >> $LOG
[ -s renders/master_draft.mp4 ] || { echo "MIX skipped (render failed)" >> $LOG; exit 1; }
python3 build/sfx_mix.py renders/master_draft.mp4 renders/preview_sports-science_reels_9x16_v1.mp4 >> $LOG 2>&1
echo "MIX EXIT $?" >> $LOG
echo "ALL DONE" >> $LOG
