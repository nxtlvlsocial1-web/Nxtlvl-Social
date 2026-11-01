#!/usr/bin/env bash
# Delivery render at the composition's 20 fps (the references' frame pacing). Run detached:
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/section.wav -filter_complex "[0:v]split[a][b];[b]lut3d=assets/lut/MoodyGloss.cube[l];[a][l]blend=all_mode=normal:all_opacity=0.75,format=yuv420p[v]" -map "[v]" -map 1:a -c:v libx264 -preset slow -crf 17 -maxrate 10M -bufsize 20M \
  -pix_fmt yuv420p -profile:v high -c:a aac -b:a 320k -shortest -movflags +faststart renders/nxtlvl_spin-bout-u_reels_1x1_v17.mp4 >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
# Sound design (real CC0 recordings, build/sfx_sheet.py) on top of the graded master, through the real-sfx skill's
# mixer: the song stays as it is, the SFX layer sits under it. Skip quietly if the skill is not installed here.
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  OUT=renders/nxtlvl_spin-bout-u_reels_1x1_v17.mp4
  python3 build/sfx_sheet.py "$OUT" --out cache/sfx/cues_final.json >> renders/final.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/cache/sfx/cues_final.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/final.log 2>&1
  echo "SFX EXIT $?" >> renders/final.log
fi
