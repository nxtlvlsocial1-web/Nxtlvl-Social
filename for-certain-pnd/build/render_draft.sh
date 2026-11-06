#!/usr/bin/env bash
# For Certain 3:4 draft render: the picture, the song's first minute (fading across the logo), then the light CC0
# sound-effect layer (build/sfx_sheet.py + the real-sfx skill's mixer). Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_for-certain_3x4_v1.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/section.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT" >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 build/sfx_sheet.py "$OUT" --out "$PWD/renders/cues_preview.json" >> renders/draft.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_preview.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/draft.log 2>&1
  echo "SFX EXIT $?" >> renders/draft.log
fi
