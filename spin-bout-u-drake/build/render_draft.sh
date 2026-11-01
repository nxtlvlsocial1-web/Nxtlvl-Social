#!/usr/bin/env bash
# Graded with the MoodyGloss LUT from the owner's editing pack at 75%.
# Draft preview for approval (fast, lower quality), with the song. Run detached:
#   setsid nohup bash build/render_draft.sh > /dev/null 2>&1 < /dev/null &
cd "$(dirname "$0")/.." || exit 1
export HYPERFRAMES_NO_TELEMETRY=1
mkdir -p renders
npx --yes hyperframes@0.8.203 render --quality draft -w 3 -o renders/draft_master.mp4 > renders/draft.log 2>&1
ffmpeg -v error -y -i renders/draft_master.mp4 -i assets/audio/section.wav -filter_complex "[0:v]split[a][b];[b]lut3d=assets/lut/MoodyGloss.cube[l];[a][l]blend=all_expr='if(lt(T\,44.28)\,A*0.25+B*0.75\,A)',format=yuv420p[v]" -map "[v]" -map 1:a -af "afade=t=out:st=44.28:d=1.65" -c:v libx264 -preset veryfast -crf 26 \
  -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart renders/preview_spin-bout-u_1x1_v20.mp4 >> renders/draft.log 2>&1
echo "EXIT $?" >> renders/draft.log
