"""Open a held breath in the voiceover after a line, so a beat can play out without speeding the voice.

Gives the reel check room to read (the theater reel set the pattern, 2026-11-20). The line
"It scored her next reel before she hit post." only lasts about 2.5 s, so this inserts silence between it (g5) and the next
line (g6) and shifts every later word time.

Keeps the untouched voice and word times as assets/audio/vo_base.wav and plan/words_base.json (made on first run), so
re-running with another length starts from the original each time.
python3 build/vo_insert.py [AFTER_LINE] [SECONDS]      # defaults: g5 1.8
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO, VO_BASE = os.path.join(ROOT, "assets", "audio", "vo.wav"), os.path.join(ROOT, "assets", "audio", "vo_base.wav")
WJ, WJ_BASE = os.path.join(ROOT, "plan", "words.json"), os.path.join(ROOT, "plan", "words_base.json")
after = sys.argv[1] if len(sys.argv) > 1 else "g5"
gap = float(sys.argv[2]) if len(sys.argv) > 2 else 1.8

for src, base in ((VO, VO_BASE), (WJ, WJ_BASE)):
    if not os.path.exists(base):
        shutil.copy(src, base)
words = json.load(open(WJ_BASE))
last = max(i for i, w in enumerate(words) if w["line"] == after)
at = round((words[last]["t1"] + words[last + 1]["t0"]) / 2, 3)          # middle of the breath between the two lines
sr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", VO_BASE],
                    capture_output=True, text=True).stdout.strip() or "44100"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO_BASE, "-filter_complex",
                f"[0:a]atrim=0:{at},asetpts=N/SR/TB[a];[0:a]atrim={at},asetpts=N/SR/TB[b];"
                f"anullsrc=r={sr}:cl=mono,atrim=0:{gap}[s];[a][s][b]concat=n=3:v=0:a=1,aformat=channel_layouts=mono", VO], check=True)
for w in words[last + 1:]:
    w["t0"], w["t1"] = round(w["t0"] + gap, 3), round(w["t1"] + gap, 3)
json.dump(words, open(WJ, "w"), indent=0)
print(f"inserted {gap:.2f} s of silence at {at:.2f} s (after {after}); later words shifted")
