#!/usr/bin/env bash
# Final render (owner approved v7), delivery quality, then the sound mix (voice + SFX, no music). Run detached:
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
rm -f renders/master_final.mp4
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master_final.mp4 > renders/final.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/final.log
if [ $RC -ne 0 ] || [ ! -s renders/master_final.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/final.log; exit 1; fi
python3 build/sfx_mix.py renders/master_final.mp4 renders/creators100x_creedom-postmortem_reels_9x16_final.mp4 --no-music >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
