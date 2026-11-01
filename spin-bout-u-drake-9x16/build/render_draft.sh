#!/usr/bin/env bash
# Spin Bout U 9:16 (built by ../spin-bout-u-drake/build/collage.py with SPIN_FORMAT=9x16), draft render: MoodyGloss LUT at 75%
# up to the cut, the song fading across the logo, then the real CC0 sound effects (../spin-bout-u-drake/build/sfx_sheet.py
# with plan/sfx_events_9x16.json, mixed by the real-sfx skill). Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
OUT=renders/preview_spin-bout-u_9x16_v1.mp4
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/section_9x16.wav -filter_complex "[0:v]split[a][b];[b]lut3d=assets/lut/MoodyGloss.cube[l];[a][l]blend=all_expr='if(lt(T\,43.40)\,A*0.25+B*0.75\,A)',format=yuv420p[v]" -map "[v]" -map 1:a -af "afade=t=out:st=43.40:d=1.65" -c:v libx264 -preset veryfast -crf 24 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT" >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
SFX_SKILL=$(ls -d /root/.claude/skills/synced/*/real-sfx 2>/dev/null | head -1)
if [ -n "$SFX_SKILL" ]; then
  python3 ../spin-bout-u-drake/build/sfx_sheet.py "$OUT" --events ../spin-bout-u-drake/plan/sfx_events_9x16.json --out "$PWD/renders/cues_preview.json" >> renders/draft.log 2>&1
  (cd "$SFX_SKILL" && python3 scripts/mix.py "$OLDPWD/renders/cues_preview.json" --out "$OLDPWD/${OUT%.mp4}_sfx.mp4") >> renders/draft.log 2>&1
  echo "SFX EXIT $?" >> renders/draft.log
fi
