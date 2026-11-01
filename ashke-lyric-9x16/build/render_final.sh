#!/usr/bin/env bash
# v9 (build v11) final render, 9:16: the song runs into the logo and fades across it (assets/audio/section_outro.wav,
# build/audio_outro.py), then the real CC0 sound effects from 3 s on (build/sfx_sheet.py + the real-sfx skill's mixer).
# Run detached: setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_ashke-lyric_reels_9x16_v9.mp4
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/section_outro.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 18 -maxrate 11M -bufsize 22M -profile:v high \
  -pix_fmt yuv420p -c:a aac -b:a 320k -shortest -movflags +faststart "$OUT" >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 build/sfx_sheet.py "$OUT" --events plan/sfx_events.json --out "$PWD/renders/cues_final.json" >> renders/final.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_final.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/final.log 2>&1
  echo "SFX EXIT $?" >> renders/final.log
fi
