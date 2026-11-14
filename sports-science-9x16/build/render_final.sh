#!/usr/bin/env bash
# v2 final (owner asked for final render quality directly): generate, picture in delivery quality (11 Mb/s), sound, verify.
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
LOG=renders/final.log
OUT=renders/sports-science-technology_no-fixed-body-type_reels_9x16_v2.mp4
: > $LOG
PREVIEW=0 python3 build/generate.py >> $LOG 2>&1 || { echo "GEN FAILED" >> $LOG; exit 1; }
rm -f renders/master_final.mp4
npx --yes hyperframes@0.8.203 render --quality high --video-bitrate 11M --sdr -w 3 -o renders/master_final.mp4 >> $LOG 2>&1
echo "RENDER EXIT $?" >> $LOG
[ -s renders/master_final.mp4 ] || { echo "MIX skipped (render failed)" >> $LOG; exit 1; }
python3 build/sfx_mix.py renders/master_final.mp4 "$OUT" >> $LOG 2>&1
echo "MIX EXIT $?" >> $LOG
python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py "$OUT" --target -14 --outdir renders/verify_v2 >> $LOG 2>&1
echo "ALL DONE" >> $LOG
