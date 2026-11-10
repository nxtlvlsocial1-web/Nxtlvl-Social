#!/usr/bin/env bash
# Draft render: the picture, then the sound with the openverse-sfx skill's recipes (build/sfx_mix.py: CC0 effects peak-
# normalised by measurement, music at -20 LUFS ducked under the voice, two-pass master to -16 LUFS / -4.5 dBTP), then the
# skill's verify_mix.py on the exported MP4. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_creedom-explainer_reels_9x16_v7.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
python3 build/sfx_mix.py renders/draft_master.mp4 "$OUT" >> renders/draft.log 2>&1
python3 ~/.claude/skills/openverse-sfx/scripts/verify_mix.py "$OUT" --outdir renders/verify_draft >> renders/draft.log 2>&1
echo "SFX EXIT $?" >> renders/draft.log
