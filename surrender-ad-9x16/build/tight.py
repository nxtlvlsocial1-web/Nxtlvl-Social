"""Tight cut of the talking head (owner: "make sure the words and scripting are tight, remove all the gaps").

The speaker barely pauses, and Scribe's word ends run into the pauses, so the cut follows the audio itself: every
pause quieter than THRESH for at least MINSIL (silencedetect, after a 90 Hz high-pass for room rumble) is cut down to
KEEP seconds (half on each side, so breaths and word tails are not clipped). The kept pieces are joined with 8 ms
audio fades so no cut clicks. Writes:
  assets/video/tight.mov  (1280x720, 30 fps, PCM audio)
  plan/cuts.json          (kept source ranges and where each starts on the tight clock)
  plan/words_tight.json   (every Scribe word mapped onto the tight clock)
python3 build/tight.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets", "video", "raw.mp4")
THRESH, MINSIL, KEEP = -30, .1, .08

log = subprocess.run(["ffmpeg", "-v", "info", "-i", RAW, "-af", f"highpass=f=90,silencedetect=noise={THRESH}dB:d={MINSIL}",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", RAW],
                           capture_output=True, text=True).stdout)
W = [w for w in json.load(open(os.path.join(ROOT, "plan", "transcript_scribe.json")))["segments"][0]["words"] if w["text"].strip()]
start, end = max(0, W[0]["start_time"] - .05), min(dur, W[-1]["end_time"] + .15)
segs, cur = [], start
for a, b in zip(st, en):
    if b <= start or a >= end:
        continue
    cut_a, cut_b = a + KEEP / 2, b - KEEP / 2
    if cut_b - cut_a > .02:
        segs.append((cur, cut_a))
        cur = cut_b
segs.append((cur, end))
segs = [(round(a, 3), round(b, 3)) for a, b in segs if b - a > .05]

cuts, t = [], 0.0
for a, b in segs:
    cuts.append({"src": [a, b], "at": round(t, 3)})
    t += b - a


def to_tight(x):
    for c in cuts:
        a, b = c["src"]
        if x <= b:
            return round(c["at"] + max(0.0, x - a), 3)
    return round(t, 3)


words = [{"text": w["text"], "s": to_tight(w["start_time"]), "e": to_tight(w["end_time"])} for w in W]
json.dump(cuts, open(os.path.join(ROOT, "plan", "cuts.json"), "w"), indent=0)
json.dump(words, open(os.path.join(ROOT, "plan", "words_tight.json"), "w"), ensure_ascii=False, indent=0)

fc = []
for k, (a, b) in enumerate(segs):
    d = b - a
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{k}];"
              f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d - .008:.3f}:d=0.008[a{k}];")
fc.append("".join(f"[v{k}][a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", RAW, "-filter_complex", "".join(fc), "-map", "[v]", "-map", "[a]",
                "-r", "30", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "pcm_s16le", "-ar", "48000", os.path.join(ROOT, "assets", "video", "tight.mov")], check=True)
print(f"{len(segs)} pieces, {t:.2f} s (raw {dur:.2f} s, speech {start:.2f}-{end:.2f})")
