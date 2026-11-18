#!/usr/bin/env bash
# Preview render: picture (--quality draft), then sound (build/sfx_mix.py), then the openverse-sfx skill's verify_mix.py.
# Run detached:  setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_kokila-peace_reels_9x16_v3.mp4
rm -f renders/draft_master.mp4
npx --yes hyperframes@0.8.203 render --quality draft --sdr -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/draft.log
# a failed picture render must not be mixed onto an older master
if [ $RC -ne 0 ] || [ ! -s renders/draft_master.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/draft.log; exit 1; fi
python3 build/sfx_mix.py renders/draft_master.mp4 "$OUT" >> renders/draft.log 2>&1
python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py "$OUT" --target -14 --outdir renders/verify_draft >> renders/draft.log 2>&1
echo "SFX EXIT $?" >> renders/draft.log
