#!/usr/bin/env bash
# Final render (delivery quality), then the sound mix. Fully detached (CLAUDE.md):
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_RENDER_DETACHED=1
rm -f renders/master.mp4
mkdir -p renders
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 < <(sleep infinity) > renders/final.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/final.log
if [ $RC -ne 0 ] || [ ! -s renders/master.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/final.log; exit 1; fi
python3 build/sfx_mix.py renders/master.mp4 renders/sst_the-journey-continues_reels_9x16_v6_final.mp4 >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
