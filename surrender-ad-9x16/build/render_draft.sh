#!/usr/bin/env bash
# Surrender ad 9:16, draft render. The voice (tight cut) over the music bed from 0:46 (build/music_bed.py), ducked under
# the voice by a sidechain compressor, then the real CC0 sound effects (build/sfx_sheet.py + the real-sfx mixer).
# Run detached: setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_surrender-ad_9x16_v3.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/voice.wav -i assets/audio/music_bed.wav -filter_complex \
  "[1:a]aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-2:LRA=9,asplit=2[v][sc];[2:a]volume=-19dB[m0];[m0][sc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=320[m];[v][m]amix=inputs=2:normalize=0:duration=first,atrim=0:106.5,afade=t=out:st=105.4:d=1.1[a]" \
  -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT" >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 build/sfx_sheet.py "$OUT" --out "$PWD/renders/cues_preview.json" >> renders/draft.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_preview.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/draft.log 2>&1
  echo "SFX EXIT $?" >> renders/draft.log
fi
