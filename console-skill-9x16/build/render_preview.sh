#!/usr/bin/env bash
# The draft preview for approval. Run it detached (never as a time-limited background job):
#   setsid nohup bash build/render_preview.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/nxtlvl_console-skill_reels_9x16_preview.mp4 > renders/preview.log 2>&1
echo "EXIT $?" >> renders/preview.log
