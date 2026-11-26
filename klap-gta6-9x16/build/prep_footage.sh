#!/usr/bin/env bash
# Footage for the Klap reel. GTA 6: Rockstar Games' official promo clips (owner's standing exception: footage only,
# audio muted, never re-uploaded whole), prepared in ../gta6-playbook-9x16 and ../gta6-chat-clipper-9x16.
# Facecam: Pexels 6878208 (cottonbro studio, Pexels licence: free for commercial use, no attribution needed).
set -e
cd "$(dirname "$0")/.."
PB=../gta6-playbook-9x16/assets/video
CC=../gta6-chat-clipper-9x16/assets/video
mkdir -p assets/video
enc="-an -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -g 10 -r 30"
for c in flip heli cops truck boat scoot dive shoot; do ffmpeg -v error -y -i $PB/c_$c.mp4 $enc assets/video/c_$c.mp4; done
ffmpeg -v error -y -i $PB/r_sky.mp4 $enc assets/video/r_sky.mp4
for c in cops flip heli boat scoot truck ball dive; do ffmpeg -v error -y -i $CC/v_$c.mp4 $enc assets/video/v_$c.mp4; done
# the "stream" (16:9): the chat-clipper band (skydive, flip, heli) and a chase band cut from the truck clip
ffmpeg -v error -y -i $CC/stream.mp4 $enc assets/video/stream.mp4
ffmpeg -v error -y -i $PB/c_truck.mp4 -vf "crop=1080:608:0:560" $enc assets/video/stream_chase.mp4
ffmpeg -v error -y -i $PB/c_cops.mp4 -vf "crop=1080:608:0:700" $enc assets/video/stream_cops.mp4
# facecam: 16:10 window on the talker's face, 9-21 s
ffmpeg -v error -y -ss 9 -i footage/pexels/px_6878208.mp4 -t 12 -vf "crop=2400:1500:1000:120,scale=960:600:flags=lanczos,eq=contrast=1.06:saturation=1.08" $enc assets/video/facecam.mp4
ls -la assets/video
# v3: Klap's own screen recording (the brand's file, 2272x1080 60 fps), the browser window cropped out of the wallpaper
# (x 114-2157, y 54-1020). rec_paste 3.3-5.35 s, rec_gen 5.35-9.9 s at 1.5x, rec_edit2 = the zoomed editor frame at
# 14.70 s held (the recorder zooms back out at 15 s); each padded with its last frame.
# ffmpeg -ss 3.3 -t 2.05 -i klap.mp4 -vf "crop=2043:966:114:54,scale=1080:510,tpad=stop_mode=clone:stop_duration=2.5" ... rec_paste.mp4
# ffmpeg -ss 5.35 -t 4.55 -i klap.mp4 -vf "crop=2043:966:114:54,scale=1080:510,setpts=PTS/1.5,tpad=stop_mode=clone:stop_duration=2.5" ... rec_gen.mp4
# ffmpeg -ss 14.70 -t 0.05 -i klap.mp4 -vf "crop=1000:714:626:196,scale=980:700,tpad=stop_mode=clone:stop_duration=3.9" ... rec_edit2.mp4
