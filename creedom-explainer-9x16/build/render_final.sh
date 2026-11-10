#!/usr/bin/env bash
# Final render: picture + the voice/music bed (build/bed.py), then the CC0 sound effects (build/sfx_sheet.py + the
# real-sfx mixer), then the whole mix levelled to -14 LUFS. Run detached:
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
D=37.5
BASE=renders/nxtlvl_creedom-explainer_reels_9x16_v6_bed.mp4
OUT=renders/nxtlvl_creedom-explainer_reels_9x16_v6.mp4
npx --yes hyperframes@0.8.203 render --quality high -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/bed.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 18 -maxrate 8M -bufsize 16M -pix_fmt yuv420p \
  -c:a aac -b:a 192k -t $D -movflags +faststart "$BASE" >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
python3 build/sfx_sheet.py "$BASE" --out "$PWD/renders/cues_final.json" >> renders/final.log 2>&1
(cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_final.json" --out "$OLDPWD/renders/mix_final.mp4") >> renders/final.log 2>&1
ffmpeg -v error -y -i renders/mix_final.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$OUT" >> renders/final.log 2>&1
echo "SFX EXIT $?" >> renders/final.log
