#!/usr/bin/env bash
# v2 clip library (owner: "use the best of the best scenes from all of the videos"): Rockstar's official GTA 6 reels
# (CLAUDE.md exception: footage only, audio muted), each cut once to 1080x1920. The rating badge in the first seconds of
# r3/r4 sits in the bottom-left corner, so those cuts are cropped from x=140 (the badge never shows).
cd "$(dirname "$0")/.." || exit 1
R=footage/rockstar; O=assets/video; mkdir -p $O
V="scale=1080:1920:flags=lanczos,setsar=1,fps=30"
C="crop=580:1031:140:0,$V"
cut() { ffmpeg -v error -y -ss $2 -t $3 -i $1 -an -vf "$4" -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p $O/$5.mp4; }
cut $R/r3.mp4 1.0 2.4  "$C" c_heli_badge    # helicopter over the tower, shootout below
cut $R/r3.mp4 4.0 2.4  "$V" c_heli          # helicopter, wide
cut $R/r3.mp4 7.0 2.7  "$V" c_truck         # police truck charges, sparks
cut $R/r3.mp4 9.7 2.0  "$V" c_flip          # the truck flips
cut $R/r3.mp4 12.4 2.3 "$V" c_cops          # cop cars round the corner
cut $R/r3.mp4 15.3 1.6 "$V" c_shoot         # close: firing
cut $R/r4.mp4 0.2 3.4  "$C" c_scoot         # scooters past the murals
cut $R/r4.mp4 4.0 2.9  "$C" c_boat          # airboat in the swamp
cut $R/r4.mp4 7.0 2.8  "$V" c_ball          # basketball
cut $R/r4.mp4 10.0 1.8 "$V" c_dive          # diving
cut $R/r4.mp4 12.0 3.6 "$V" c_gym           # Lucia, bench press
