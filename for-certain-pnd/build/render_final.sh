#!/usr/bin/env bash
# For Certain 3:4 final render: the picture, the song's first minute (fading across the logo), then the light CC0
# sound-effect layer (build/sfx_sheet.py + the real-sfx skill's mixer). Run detached:
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_for-certain_3x4_v1.mp4
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/section.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 17 -maxrate 11M -bufsize 22M -profile:v high -pix_fmt yuv420p -c:a aac -b:a 320k -shortest -movflags +faststart "$OUT" >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 build/sfx_sheet.py "$OUT" --out "$PWD/renders/cues_final.json" >> renders/final.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_final.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/final.log 2>&1
  echo "SFX EXIT $?" >> renders/final.log
fi
