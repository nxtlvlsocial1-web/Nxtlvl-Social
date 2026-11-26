"""Klap reel: the music bed. "Miami" by Lyvo (Jamendo 1440523, CC BY 3.0, 129 BPM, instrumental: Demucs put its vocal
stem ~52 dB under the mix, see ../gta6-claude-9x16/sfx/music/check.json). Two segments on one beat grid
(plan/music_plan.json from build/generate.py): full energy under the hook, its breakdown from "The hard part", then the
end of the build so the kick slams back (track 120.024 s) exactly on "Klap". 40 ms crossfade on a beat.
Writes assets/audio/music.wav. python3 build/music.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "plan", "music_plan.json")))
SRC = os.path.join(ROOT, P["track"])
o1, o2, cut, dur, xf = P["o1"], P["o2"], P["cut"], P["dur"], .04
g0, g1 = P["gap"]   # silence before the drop, under "called Klap"
fc = (f"[0:a]atrim={o1:.4f}:{o1 + cut + xf:.4f},asetpts=PTS-STARTPTS[a];"
      f"[1:a]atrim={o2 + cut:.4f}:{o2 + dur + .1:.4f},asetpts=PTS-STARTPTS[b];"
      f"[a][b]acrossfade=d={xf}:c1=tri:c2=tri,atrim=0:{dur:.3f},afade=t=in:d=0.03,afade=t=out:st={dur - .8:.3f}:d=0.8,"
      f"volume='1-0.94*clip((t-{g0:.3f})/0.06,0,1)*clip(({g1:.3f}-t)/0.02,0,1)':eval=frame,aresample=48000[m]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-i", SRC, "-filter_complex", fc, "-map", "[m]", "-ac", "2",
                "-c:a", "pcm_f32le", os.path.join(ROOT, "assets", "audio", "music.wav")], check=True)
print(f"music.wav: track {o1:.2f}+ to {cut:.2f} s, then track {o2 + cut:.2f}+ (kick at video {120.024 - o2:.2f} s), {dur} s")
