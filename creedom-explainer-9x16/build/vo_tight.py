"""Tighten the ElevenLabs voiceover (take 1): every pause longer than KEEP is cut down to KEEP (half each side), with
10 ms fades so nothing clicks; the word timings (Scribe) are mapped onto the tight clock.
Writes assets/audio/vo.wav and plan/vo_tight.json.  python3 build/vo_tight.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "audio", "vo_take1.mp3")
KEEP = .28
log = subprocess.run(["ffmpeg", "-v", "info", "-i", SRC, "-af", "silencedetect=noise=-35dB:d=0.15", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC],
                           capture_output=True, text=True).stdout)
rem = [(a + KEEP / 2, b - KEEP / 2) for a, b in zip(st, en) if b - a > KEEP + .05]
segs, cur = [], 0.0
for a, b in rem:
    segs.append((cur, a))
    cur = b
segs.append((cur, dur))
cuts, t = [], 0.0
for a, b in segs:
    cuts.append((a, b, t))
    t += b - a


def tt(x):
    for a, b, at in cuts:
        if x <= b:
            return round(at + max(0.0, x - a), 3)
    return round(t, 3)


W = [w for w in json.load(open(os.path.join(ROOT, "plan", "vo_words.json")))["words"] if not w["text"].startswith("[")]
words = [{"text": w["text"], "s": tt(w["start"]), "e": tt(w["end"])} for w in W]
json.dump(words, open(os.path.join(ROOT, "plan", "vo_tight.json"), "w"), indent=0)
parts = "".join(f"[0]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b - a - .01:.3f}:d=0.01[p{k}];"
                for k, (a, b, _) in enumerate(cuts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex",
                parts + "".join(f"[p{k}]" for k in range(len(cuts))) + f"concat=n={len(cuts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=9[o]",
                "-map", "[o]", "-ar", "48000", "-ac", "1", os.path.join(ROOT, "assets", "audio", "vo.wav")], check=True)
print(f"{len(cuts)} pieces, {dur:.2f} -> {t:.2f} s")
