#!/usr/bin/env bash
# Final render: picture (--quality high at a fixed 11 Mb/s: about 88 MB, under the 100 MB delivery cap with no second encode), then sound (build/sfx_mix.py), then the openverse-sfx skill's verify_mix.py.
# Run detached:  setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_kokila-peace_reels_9x16_v1.mp4
rm -f renders/master.mp4
npx --yes hyperframes@0.8.203 render --quality high --video-bitrate 11M --sdr -w 3 -o renders/master.mp4 > renders/final.log 2>&1
RC=$?
echo "EXIT $RC" >> renders/final.log
# a failed picture render must not be mixed onto an older master
if [ $RC -ne 0 ] || [ ! -s renders/master.mp4 ]; then echo "SFX EXIT skipped (render failed)" >> renders/final.log; exit 1; fi
python3 build/sfx_mix.py renders/master.mp4 "$OUT" >> renders/final.log 2>&1
python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py "$OUT" --target -14 --outdir renders/verify_high >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
