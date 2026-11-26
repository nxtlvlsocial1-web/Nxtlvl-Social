#!/usr/bin/env bash
# Rebuild everything this project keeps out of git (a cloud machine reset wipes it): the speech stack, the footage,
# the music, the sound effects, the fonts, the voice and its word timings. About 15 minutes. Run from anywhere:
#   bash klap-gta6-9x16/build/recover.sh [path/to/klap-screen-recording.mp4]
# The Klap screen recording is the brand's own upload and is not downloadable: pass its path to rebuild the rec_* clips.
set -e
cd "$(dirname "$0")/.."; P=$PWD; REPO=$(cd .. && pwd)
mkdir -p assets/audio assets/video assets/sfx sfx/music footage/pexels cache renders ../gta6-playbook-9x16/footage/rockstar
enc="-an -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -g 10 -r 30"
V="scale=1080:1920:flags=lanczos,setsar=1,fps=30"

# 1. speech stack: Kokoro-82M + faster-whisper on Python 3.12 (kokoro needs < 3.13)
if [ ! -x /root/tts/.venv/bin/python ]; then
  mkdir -p /root/tts && cd /root/tts && (which uv >/dev/null || pip3 install -q uv)
  uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python kokoro soundfile librosa numpy faster-whisper "misaki[en]"
  cd "$P"
fi
export HF_HOME=/root/tts/hf

# 2. fonts (Fontshare licence, kept out of git)
curl -sL --max-time 30 -o cache/fs.css "https://api.fontshare.com/v2/css?f[]=clash-display@600,700" && python3 - <<'EOF'
import re, subprocess
css = open("cache/fs.css").read()
for b in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
    if "italic" in b.lower(): continue
    fam = re.search(r"font-family:\s*'([^']+)'", b).group(1); w = re.search(r"font-weight:\s*(\d+)", b).group(1)
    u = re.search(r"url\('(//[^']+\.woff2)'\)", b).group(1)
    subprocess.run(["curl", "-sL", "--max-time", "30", "-o", f"assets/fonts/{fam.replace(' ', '')}-{w}.woff2", "https:" + u], check=True)
EOF

# 3. footage. Rockstar's official GTA VI "Extended Look" vertical clips (owner's standing exception: muted footage only):
#    the chase reel and the scooter/airboat reel from Rockstar's TikTok, the skydive reel from Rockstar's Instagram.
R=../gta6-playbook-9x16/footage/rockstar
Y=/root/tools/ytdlp/bin/yt-dlp
[ -x $Y ] || python3 ../tools/see_link.py --help >/dev/null 2>&1 || true
[ -f $R/r3.mp4 ] || $Y -q --no-warnings -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" -o "$R/r3.%(ext)s" "https://www.tiktok.com/@rockstargames/video/7679254944112807182"
[ -f $R/r4.mp4 ] || $Y -q --no-warnings -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" -o "$R/r4.%(ext)s" "https://www.tiktok.com/@rockstargames/video/7679255084114496782"
[ -f $R/DcmuTFvAapk.mp4 ] || { python3 ../tools/see_link.py "https://www.instagram.com/reel/DcmuTFvAapk/" --out cache/ig_sky >/dev/null 2>&1 && cp cache/ig_sky/video.mp4 $R/DcmuTFvAapk.mp4; }
#    Pexels 6878208 (cottonbro studio, Pexels licence): the streamer facecam
[ -f footage/pexels/px_6878208.mp4 ] || curl -sL --max-time 600 -o footage/pexels/px_6878208.mp4 https://videos.pexels.com/video-files/6878208/6878208-uhd_4096_2160_25fps.mp4
O=assets/video
cut() { ffmpeg -v error -y -ss $2 -t $3 -i $1 -vf "$4" $enc $O/$5.mp4; }
cut $R/r3.mp4 4.0 2.4 "$V" c_heli; cut $R/r3.mp4 7.0 2.7 "$V" c_truck; cut $R/r3.mp4 9.7 2.0 "$V" c_flip; cut $R/r3.mp4 12.4 2.3 "$V" c_cops; cut $R/r3.mp4 15.3 1.6 "$V" c_shoot
C="crop=870:1546:210:0,$V"   # the rating badge sits bottom-left in r4's first seconds
cut $R/r4.mp4 0.2 3.4 "$C" c_scoot; cut $R/r4.mp4 4.0 2.9 "$C" c_boat; cut $R/r4.mp4 7.0 2.8 "$V" c_ball; cut $R/r4.mp4 10.0 1.8 "$V" c_dive
cut $R/DcmuTFvAapk.mp4 0 7.4 "$V" r_sky
ffmpeg -v error -y -ss 9 -i footage/pexels/px_6878208.mp4 -t 12 -vf "crop=2400:1500:1000:120,scale=960:600:flags=lanczos,eq=contrast=1.06:saturation=1.08" $enc $O/facecam.mp4
for s in "r_sky 22 -0.22 r_sky_blur" "r_sky 14 -0.3 r_sky_blur2" "c_boat 14 -0.3 c_boat_blur"; do set -- $s
  ffmpeg -v error -y -i $O/$1.mp4 -vf "boxblur=$2:2,eq=brightness=$3:saturation=1.1" -an -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -g 10 -r 30 $O/$4.mp4; done
mkdir -p cache/band && rm -f cache/band/*; i=0
for spec in "$R/DcmuTFvAapk.mp4 0 5.0 .33" "$O/c_flip.mp4 0 2.0 .45" "$O/c_heli.mp4 0 2.4 .40"; do set -- $spec
  ffmpeg -v error -y -ss $2 -i "$1" -t $3 -an -vf "scale=1080:-2:flags=lanczos,crop=1080:608:0:(ih-608)*$4,fps=30,setsar=1,format=yuv420p" -c:v libx264 -crf 16 -preset slow cache/band/$i.mp4; i=$((i+1)); done
ls cache/band/*.mp4 | sort -V | sed "s#^#file '$P/#;s#\$#'#" > cache/band/list.txt
ffmpeg -v error -y -f concat -safe 0 -i cache/band/list.txt $enc $O/stream.mp4
ffmpeg -v error -y -i $O/c_truck.mp4 -vf "crop=1080:608:0:560" $enc $O/stream_chase.mp4
ffmpeg -v error -y -i $O/c_cops.mp4 -vf "crop=1080:608:0:700" $enc $O/stream_cops.mp4
for s in stream_chase stream_cops; do ffmpeg -v error -y -stream_loop 3 -i $O/$s.mp4 -t 8 $enc $O/${s}_l.mp4; done
for c in cops flip heli boat scoot truck ball dive; do ffmpeg -v error -y -stream_loop 4 -i $O/c_$c.mp4 -t 9 -vf "scale=360:640" -an -c:v libx264 -crf 22 -preset fast -pix_fmt yuv420p -g 10 -r 30 $O/t_$c.mp4; done
printf "file '%s'\n" $P/$O/c_cops.mp4 $P/$O/c_truck.mp4 $P/$O/c_flip.mp4 $P/$O/c_cops.mp4 > cache/game_l.txt && ffmpeg -v error -y -f concat -safe 0 -i cache/game_l.txt $enc $O/game_l.mp4
for spec in "c_flip 2.0" "c_heli 2.4" "c_cops 2.3" "c_truck 2.7" "c_shoot 1.6" "c_boat 2.9" "c_scoot 3.4"; do set -- $spec; k=$(python3 -c "print(round($2-0.6,3))")
  ffmpeg -v error -y -i $O/$1.mp4 -filter_complex "[0:v]trim=0:$k,setpts=PTS-STARTPTS[a];[0:v]trim=$k,setpts=(PTS-STARTPTS)/3[b];[a][b]concat=n=2:v=1:a=0,fps=30" $enc $O/h_${1#c_}.mp4; done
#    Klap's screen recording (the brand's upload): the browser window cropped out of the wallpaper
if [ -n "$1" ] && [ -f "$1" ]; then
  W="crop=2043:966:114:54,scale=1080:510:flags=lanczos"
  ffmpeg -v error -y -ss 3.3 -t 2.05 -i "$1" -vf "$W,tpad=stop_mode=clone:stop_duration=2.5" $enc $O/rec_paste.mp4
  ffmpeg -v error -y -ss 5.35 -t 4.55 -i "$1" -vf "$W,setpts=PTS/1.5,tpad=stop_mode=clone:stop_duration=2.5" $enc $O/rec_gen.mp4
  ffmpeg -v error -y -ss 14.70 -t 0.05 -i "$1" -vf "crop=1000:714:626:196,scale=980:700:flags=lanczos,tpad=stop_mode=clone:stop_duration=3.9" $enc $O/rec_edit2.mp4
fi

# 4. music: "Miami" by Lyvo (Jamendo 1440523, CC BY 3.0); the beat grid is in git
[ -s sfx/music/m3_miami.mp3 ] || curl -sL --max-time 600 -o sfx/music/m3_miami.mp3 "https://prod-1.storage.jamendo.com/?trackid=1440523&format=mp32&from=app-devsite"

# 5. sound effects: the Openverse/Freesound CC0 set (plan/sfx_library.json + three extras) and the OpenGameArt CC0 packs
python3 - <<'EOF'
import json, subprocess, os
lib = json.load(open("plan/sfx_library.json"))
extra = {"typing": "https://cdn.freesound.org/previews/250/250390_10476-hq.mp3", "sparkle": "https://cdn.freesound.org/previews/351/351408_4067257-hq.mp3",
         "msg": "https://cdn.freesound.org/previews/592/592772_13171056-hq.mp3"}
for name, url in [(e["name"], e["audio"]) for e in lib] + list(extra.items()):
    out = f"assets/sfx/{name}.mp3"
    if not os.path.exists(out): subprocess.run(["curl", "-sL", "--max-time", "60", "-o", out, url], check=True)
EOF
[ -d assets/sfx/oga/interface-sounds ] || python3 build/oga_sfx.py
G=assets/sfx/oga; conv() { ffmpeg -v error -y -i "$1" -ac 1 -ar 48000 -b:a 160k assets/sfx/$2.mp3; }
conv "$G/interface-sounds/Audio__tick_001.ogg" g_tick; conv "$G/interface-sounds/Audio__pluck_001.ogg" g_pop; conv "$G/interface-sounds/Audio__drop_001.ogg" g_drop
conv "$G/7-assorted-sound-effects-menu-level-up/Item Pickup.mp3" g_pickup; conv "$G/7-assorted-sound-effects-menu-level-up/Level Up.mp3" g_levelup
conv "$G/completion-sound/completetask_0.mp3" g_complete; conv "$G/swishes-sound-pack/swishes__swish-3.wav" g_swish

# 6. the voice (Kokoro is deterministic: the same words and timings every time) and the build
export HF_HUB_OFFLINE=0
/root/tts/.venv/bin/python build/vo_kok.py af_heart
VO_TAKES=assets/audio/vo_takes/af_heart VO_TAG=af_heart VO_TEMPO=1.0 /root/tts/.venv/bin/python build/vo_pick.py
cp assets/audio/vo_af_heart.wav assets/audio/vo.wav && cp plan/words_af_heart.json plan/words.json
python3 build/generate.py && python3 build/music.py
echo "RECOVERED: $(ls assets/video | wc -l) clips, $(ls assets/sfx/*.mp3 | wc -l) sounds"
