#!/usr/bin/env bash
# Builds assets/site.mp4 from the website screen recording (branding kept as recorded):
# crops the 156 px top letterbox, 30 fps, 1280 wide, silent.
# Usage: ./prep_site.sh path/to/recording.mov
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -hide_banner -loglevel error -y -ss 0.05 -i "$1" -vf "crop=1920:924:0:156,fps=30,scale=1280:-2" \
  -an -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -movflags +faststart assets/site.mp4
echo "wrote assets/site.mp4"
