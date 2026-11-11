#!/usr/bin/env bash
# Final render: picture (--quality high), then sound (build/sfx_mix.py), then the openverse-sfx skill's verify_mix.py.
# Run detached:  setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_gta6-claude_reels_9x16_v1.mp4
npx --yes hyperframes@0.8.203 render --quality high -w 3 -o renders/master.mp4 > renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
python3 build/sfx_mix.py renders/master.mp4 "$OUT" >> renders/final.log 2>&1
python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py "$OUT" --outdir renders/verify_high >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
