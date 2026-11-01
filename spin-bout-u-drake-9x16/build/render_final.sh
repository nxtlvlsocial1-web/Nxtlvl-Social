#!/usr/bin/env bash
# Spin Bout U 9:16 (built by ../spin-bout-u-drake/build/collage.py with SPIN_FORMAT=9x16), final render: MoodyGloss LUT at 75%
# up to the cut, the song fading across the logo, then the real CC0 sound effects (../spin-bout-u-drake/build/sfx_sheet.py
# with plan/sfx_events_9x16.json, mixed by the real-sfx skill). Run detached:
#   setsid nohup bash build/render_final.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/nxtlvl_spin-bout-u_reels_9x16_v1.mp4
npx --yes hyperframes@0.8.203 render --quality delivery -w 3 -o renders/master.mp4 > renders/final.log 2>&1
ffmpeg -v error -y -i renders/master.mp4 -i assets/audio/section_9x16.wav -filter_complex "[0:v]split[a][b];[b]lut3d=assets/lut/MoodyGloss.cube[l];[a][l]blend=all_expr='if(lt(T\,43.40)\,A*0.25+B*0.75\,A)',format=yuv420p[v]" -map "[v]" -map 1:a -af "afade=t=out:st=43.40:d=1.65" -c:v libx264 -preset slow -crf 18 -maxrate 13M -bufsize 26M -profile:v high \
  -pix_fmt yuv420p -c:a aac -b:a 320k -shortest -movflags +faststart "$OUT" >> renders/final.log 2>&1
echo "EXIT $?" >> renders/final.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 ../spin-bout-u-drake/build/sfx_sheet.py "$OUT" --events ../spin-bout-u-drake/plan/sfx_events_9x16.json --out "$PWD/renders/cues_final.json" >> renders/final.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_final.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/final.log 2>&1
  echo "SFX EXIT $?" >> renders/final.log
fi
