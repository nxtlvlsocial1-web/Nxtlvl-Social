"""Tight cut of the talking head (owner: "make necessary trims if there is gaps"). Based on surrender-ad-9x16/build/tight.py.

Every pause quieter than THRESH for at least MINSIL (silencedetect after a 90 Hz high-pass) is cut down to KEEP
seconds, half on each side, so breaths and word tails stay. Two word ranges are cut outright: the breath before the
first word and the stumble "बहन--" near the end. Pieces are cut on whole frames with 8 ms audio fades and joined.
No speed change, no music. The voice comes from VOICE (the cleaned track) when it exists, else the camera audio.
Writes:
  assets/video/tight.mov   (720x1280, 30 fps, PCM audio)
  plan/cuts.json           (kept source ranges and where each starts on the tight clock)
  plan/words_tight.json    (every Scribe word mapped onto the tight clock)
python3 build/tight.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets", "video", "raw.mp4")
VOICE = os.path.join(ROOT, "cache", "voice_clean.wav")
THRESH, MINSIL, KEEP = -30, .1, .08
SPEED = 1.4143         # v7 (owner: "fast forward the whole video to 1:37"): picture and voice 1.4143x of the take, pitch kept, 96 s + the 1 s end hold
CUT_WORDS = [(0, 0),        # [breath] before the first word
             (361, 361)]    # "बहन--" (the stumble before "भाइयों बहनों")

AUD = VOICE if os.path.exists(VOICE) else RAW
log = subprocess.run(["ffmpeg", "-v", "info", "-i", AUD, "-af", f"highpass=f=90,silencedetect=noise={THRESH}dB:d={MINSIL}",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", RAW],
                           capture_output=True, text=True).stdout)
W = [w for s in json.load(open(os.path.join(ROOT, "plan", "transcript_scribe.json")))["segments"] for w in s["words"] if w["text"].strip()]
first = min(i for i in range(len(W)) if not any(a <= i <= b for a, b in CUT_WORDS))
last = max(i for i in range(len(W)) if not any(a <= i <= b for a, b in CUT_WORDS))
start, end = max(0, W[first]["start_time"] - .06), min(dur, W[last]["end_time"] + .25)
rem = [(a + KEEP / 2, b - KEEP / 2) for a, b in zip(st, en) if b - a - KEEP > .02]
for a, b in CUT_WORDS:
    ra = W[a]["start_time"] - .03
    rb = W[b + 1]["start_time"] - .03 if b + 1 < len(W) else end
    rem.append((ra, rb))
rem = sorted((max(start, a), min(end, b)) for a, b in rem if b > start and a < end)
merged = []
for a, b in rem:
    if merged and a <= merged[-1][1]:
        merged[-1] = (merged[-1][0], max(merged[-1][1], b))
    else:
        merged.append((a, b))
segs, cur = [], start
for a, b in merged:
    segs.append((cur, a))
    cur = b
segs.append((cur, end))
segs = [(round(a * 30) / 30, round(b * 30) / 30) for a, b in segs]
segs = [(round(a, 4), round(b, 4)) for a, b in segs if b - a > .05]
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


words = [{"i": i, "text": w["text"], "s": round(to_tight(w["start_time"]) / SPEED, 3), "e": round(to_tight(w["end_time"]) / SPEED, 3),
          "cut": any(a <= i <= b for a, b in CUT_WORDS)} for i, w in enumerate(W)]
json.dump(cuts, open(os.path.join(ROOT, "plan", "cuts.json"), "w"), indent=0)
json.dump(words, open(os.path.join(ROOT, "plan", "words_tight.json"), "w"), ensure_ascii=False, indent=0)

tmp = os.path.join(ROOT, "cache", "pieces")
os.makedirs(tmp, exist_ok=True)
lst = []
for k, (a, b) in enumerate(segs):
    d = b - a
    out = os.path.join(tmp, f"p{k:03d}.mov")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", RAW, "-ss", f"{a:.4f}", "-i", AUD,
                    "-map", "0:v", "-map", "1:a", "-frames:v", str(round(d * 30)), "-t", f"{d:.4f}",
                    "-af", f"afade=t=in:d=0.008,afade=t=out:st={d - .012:.3f}:d=0.008,apad=whole_dur={d:.4f},atrim=0:{d:.4f}",
                    "-r", "30", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", out], check=True)
    lst.append(f"file '{out}'")
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst) + "\n")
one = os.path.join(tmp, "tight_1x.mov")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-c", "copy", one], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", one, "-vf", f"setpts=PTS/{SPEED}", "-af", f"atempo={SPEED}", "-r", "30",
                "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000",
                os.path.join(ROOT, "assets", "video", "tight.mov")], check=True)
print(f"{len(segs)} pieces, {t:.2f} s at 1x, {t / SPEED:.2f} s at {SPEED}x (raw {dur:.2f} s), voice from {os.path.basename(AUD)}")
