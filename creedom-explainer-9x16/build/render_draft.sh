#!/usr/bin/env bash
# Draft render: picture + the voice/music bed (build/bed.py), then the CC0 sound effects (build/sfx_sheet.py + the
# real-sfx mixer), then the whole mix levelled to -14 LUFS. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
D=37.5
BASE=renders/preview_creedom-explainer_reels_9x16_v6_bed.mp4
OUT=renders/preview_creedom-explainer_reels_9x16_v6.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/bed.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -t $D -movflags +faststart "$BASE" >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
python3 build/sfx_sheet.py "$BASE" --out "$PWD/renders/cues_draft.json" >> renders/draft.log 2>&1
(cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_draft.json" --out "$OLDPWD/renders/mix_draft.mp4") >> renders/draft.log 2>&1
ffmpeg -v error -y -i renders/mix_draft.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$OUT" >> renders/draft.log 2>&1
echo "SFX EXIT $?" >> renders/draft.log
