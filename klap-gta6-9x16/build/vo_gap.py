"""Klap reel: a 0.22 s beat before the brand name, cut into the K's own closure (17.40 s, the quiet point between
"called" and "Klap"). Without it the voice runs "called" into "Klap" and, under any music, it reads as "called a clap".
Shifts plan/words.json to match. Runs after build/vo_pick.py (build/vo_run.sh). Idempotent: works from vo_picked.wav.
"""
import json
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets", "audio")
AT, GAP = 17.40, .22
src, out = os.path.join(A, "vo_picked.wav"), os.path.join(A, "vo.wav")
wp, wsrc = os.path.join(ROOT, "plan", "words.json"), os.path.join(ROOT, "plan", "words_picked.json")
if not os.path.exists(src) or os.path.getmtime(out) > os.path.getmtime(src) + 5 and not os.path.exists(wsrc):
    shutil.copy(out, src); shutil.copy(wp, wsrc)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex",
                f"[0:a]atrim=0:{AT},asetpts=PTS-STARTPTS[a];[0:a]atrim={AT},asetpts=PTS-STARTPTS[b];"
                f"anullsrc=r=48000:cl=mono,atrim=0:{GAP}[z];[a][z][b]concat=n=3:v=0:a=1", "-ar", "48000", "-ac", "1", out], check=True)
W = json.load(open(wsrc))
for w in W:
    if w["t0"] >= AT - .06:
        w["t0"] = round(w["t0"] + GAP, 3); w["t1"] = round(w["t1"] + GAP, 3)
json.dump(W, open(wp, "w"), indent=0)
print(f"vo.wav: {GAP} s beat at {AT} s; words shifted")
