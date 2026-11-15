#!/usr/bin/env bash
# GTA 6 footage for the reel: Rockstar Games' official promo clips (owner's standing exception: footage only, audio
# muted), from ../gta6-playbook-9x16. stream.mp4 = a 16:9 band cut from the vertical clips, joined into one "live
# stream" for the mascot's monitor; the vertical clips are reused as the tool's output clips.
set -e
cd "$(dirname "$0")/.."
S=../gta6-playbook-9x16
mkdir -p assets/video cache/band && rm -f cache/band/*
# v3 (owner: "fix this clip, make sure it shows the in-game cinematics better"): the stream card now opens on Rockstar's
# extended-look skydive over the Vice City skyline (native 1080 wide, no upscaling; she leaps at 1.75 s), then the car
# flip and the helicopter for the cut shot. Bands are 1080x608 (16:9) cut at native width.
i=0
for spec in "footage/rockstar/DcmuTFvAapk.mp4 0 5.0 .33" "assets/video/c_flip.mp4 0 2.0 .45" "assets/video/c_heli.mp4 0 2.4 .40"; do
  set -- $spec
  ffmpeg -v error -y -ss $2 -i "$S/$1" -t $3 -an -vf "scale=1080:-2:flags=lanczos,crop=1080:608:0:(ih-608)*$4,fps=30,setsar=1,format=yuv420p" -c:v libx264 -crf 16 -preset slow cache/band/$i.mp4
  i=$((i+1))
done
ls cache/band/*.mp4 | sort -V | sed "s#^#file '$PWD/#;s#\$#'#" > cache/band/list.txt
ffmpeg -v error -y -f concat -safe 0 -i cache/band/list.txt -c:v libx264 -crf 16 -preset slow -g 10 assets/video/stream.mp4
for c in cops flip heli boat scoot truck ball dive; do
  ffmpeg -v error -y -i $S/assets/video/c_$c.mp4 -an -vf "scale=360:640,fps=30" -c:v libx264 -crf 22 -g 10 assets/video/v_$c.mp4
done
echo "stream.mp4 $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/video/stream.mp4) s"
