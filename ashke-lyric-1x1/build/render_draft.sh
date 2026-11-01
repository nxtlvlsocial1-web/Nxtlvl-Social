#!/usr/bin/env bash
# v2 preview for approval (draft quality), with the song and the real CC0 sound effects from 3 s on (built by
# ../ashke-lyric-9x16/build/sfx_sheet.py, mixed by the real-sfx skill). Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_ashke-lyric_1x1_v2.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/section.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 24 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT" >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 ../ashke-lyric-9x16/build/sfx_sheet.py "$OUT" --out "$PWD/renders/cues_preview.json" >> renders/draft.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_preview.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/draft.log 2>&1
  echo "SFX EXIT $?" >> renders/draft.log
fi
