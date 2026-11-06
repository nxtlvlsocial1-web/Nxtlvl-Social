#!/usr/bin/env bash
# Surrender ad 9:16, final render. The voice (tight cut) over the music bed from 0:46 (build/music_bed.py), ducked under
# the voice by a sidechain compressor, then the real CC0 sound effects (build/sfx_sheet.py + the real-sfx mixer).
# Run detached: setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_surrender-ad_reels_9x16_v2.mp4
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/voice.wav -i assets/audio/music_bed.wav -filter_complex \
  "[1:a]aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-2:LRA=9,asplit=2[v][sc];[2:a]volume=-19dB[m0];[m0][sc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=320[m];[v][m]amix=inputs=2:normalize=0:duration=first,atrim=0:117.1,afade=t=out:st=115.9:d=1.2[a]" \
  -map 0:v -map "[a]" -c:v libx264 -preset slow -crf 18 -maxrate 9M -bufsize 18M -profile:v high -pix_fmt yuv420p -c:a aac -b:a 320k -shortest -movflags +faststart "$OUT" >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 build/sfx_sheet.py "$OUT" --out "$PWD/renders/cues_final.json" >> renders/final.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_final.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/final.log 2>&1
  echo "SFX EXIT $?" >> renders/final.log
fi
