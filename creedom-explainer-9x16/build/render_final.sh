#!/usr/bin/env bash
# Final render: the picture, then the sound with the openverse-sfx skill's recipes (build/sfx_mix.py: CC0 effects peak-
# normalised by measurement, music at -20 LUFS ducked under the voice, two-pass master to -16 LUFS / -4.5 dBTP), then the
# skill's verify_mix.py on the exported MP4. Run detached:
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_creedom-explainer_reels_9x16_v10.mp4
npx --yes hyperframes@0.8.203 render --quality high -w 3 -o renders/master.mp4 > renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
python3 build/sfx_mix.py renders/master.mp4 "$OUT" >> renders/final.log 2>&1
python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py "$OUT" --outdir renders/verify_high >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
