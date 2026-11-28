#!/usr/bin/env bash
# Delivery render, then the sound mix. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_RENDER_DETACHED=1
rm -f renders/master_final.mp4
npx --yes hyperframes@0.8.203 render -w 3 --quality delivery -o renders/master_final.mp4 > renders/final.log 2>&1 < <(sleep infinity)
RC=$?
echo "EXIT $RC" >> renders/final.log
if [ $RC -ne 0 ] || [ ! -s renders/master_final.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/final.log; exit 1; fi
python3 build/sfx_mix.py renders/master_final.mp4 renders/nxtlvl_claude-plugins_reels_9x16_v1_final.mp4 >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
