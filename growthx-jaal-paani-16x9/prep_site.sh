#!/usr/bin/env bash
# Builds assets/site.mp4 from the client's screen recording: skips the 0.68 s loading frame,
# crops the 148 px letterbox, swaps the nav logo for the GrowthX mark + name, 30 fps, 1280 wide, silent.
# Usage: ./prep_site.sh path/to/recording.mov
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -hide_banner -loglevel error -y -ss 0.68 -i "$1" -i brand/logo-mark.png -filter_complex \
  "[0:v]crop=1920:932:0:148,drawbox=x=312:y=18:w=140:h=46:color=0x080618@1:t=fill,drawtext=fontfile=fonts/InterDisplay-Bold.otf:text='GrowthX':fontsize=28:fontcolor=white:x=362:y=28[bg];[1:v]scale=36:36[lg];[bg][lg]overlay=x=318:y=23,fps=30,scale=1280:-2" \
  -an -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -movflags +faststart assets/site.mp4
echo "wrote assets/site.mp4"
