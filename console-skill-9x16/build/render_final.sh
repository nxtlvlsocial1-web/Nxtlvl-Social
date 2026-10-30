#!/usr/bin/env bash
# The final, delivery-quality render. Run it detached (never as a time-limited background job):
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/nxtlvl_console-skill_reels_9x16_v1_master.mp4 > renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
