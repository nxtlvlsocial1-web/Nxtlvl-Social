#!/usr/bin/env bash
# GTA 6 footage for the reel: Rockstar Games' official promo clips (owner's standing exception: footage only, audio
# muted), from ../gta6-playbook-9x16. stream.mp4 = a 16:9 band cut from the vertical clips, joined into one "live
# stream" for the mascot's monitor; the vertical clips are reused as the tool's output clips.
set -e
cd "$(dirname "$0")/.."
S=../gta6-playbook-9x16
mkdir -p assets/video cache/band
i=0
for spec in "assets/video/c_cops.mp4 0 2.3 .52" "assets/video/c_flip.mp4 0 2.0 .45" "assets/video/c_heli.mp4 0 2.4 .40" \
            "footage/rockstar/DcmuTFvAapk.mp4 0.5 6.5 .45" "assets/video/c_boat.mp4 0 2.9 .55" "footage/rockstar/r4.mp4 0.3 9.5 .5" \
            "assets/video/c_scoot.mp4 0 3.4 .5" "assets/video/c_truck.mp4 0 2.7 .5"; do
  set -- $spec
  ffmpeg -v error -y -ss $2 -i "$S/$1" -t $3 -an -vf "scale=1280:-2,crop=1280:720:0:(ih-720)*$4,fps=30,setsar=1,format=yuv420p" -c:v libx264 -crf 20 cache/band/$i.mp4
  i=$((i+1))
done
ls cache/band/*.mp4 | sort -V | sed "s#^#file '$PWD/#;s#\$#'#" > cache/band/list.txt
ffmpeg -v error -y -f concat -safe 0 -i cache/band/list.txt -c:v libx264 -crf 20 -g 10 assets/video/stream.mp4
for c in cops flip heli boat scoot truck ball dive; do
  ffmpeg -v error -y -i $S/assets/video/c_$c.mp4 -an -vf "scale=360:640,fps=30" -c:v libx264 -crf 22 -g 10 assets/video/v_$c.mp4
done
echo "stream.mp4 $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/video/stream.mp4) s"
