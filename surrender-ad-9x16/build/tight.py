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
RAW = os.path.join(ROOT, "assets", "video", "drive2", "raw_hq.mp4")   # v3: the owner's 1080p original (not in git)
OFFSET = .048          # the 1080p file runs 0.048 s later than the 720p copy Scribe transcribed (audio cross-correlation)
THRESH, MINSIL, KEEP = -30, .1, .08
# v2 (owner: "find any repetitive pattern in the script, if the same thing is said twice cut it out"): word ranges
# (Scribe indices, inclusive) cut from the take. Each says again what the script already said, or is a filler.
CUT_WORDS = [(18, 18),      # "Guys," (filler into the body)
             (56, 60),      # "hum bahut mehnat karte hain" (said one line earlier)
             (147, 154),    # "yaar ye toh maine pehle kar rakha hai" (one of three like ego lines)
             (227, 234),    # "yahan surrender karne ka matlab ye hai ki" (repeats "surrender karne ka matlab")
             (258, 258),    # "guys" (mid-sentence filler)
             (278, 291),    # "maine bahut courses, bahut YouTube content ... try ki hain aur" (repeats the opening list)
             (321, 332),    # "aur main har ek cheez ko bilkul naye perspective se dekhta tha" (repeats the definition)
             (398, 411),    # "aur aapko ek naye perspective ke saath aapke business ko live karne wala hoon"
             (468, 468)]    # "guys." (the last word)

log = subprocess.run(["ffmpeg", "-v", "info", "-i", RAW, "-af", f"highpass=f=90,silencedetect=noise={THRESH}dB:d={MINSIL}",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", RAW],
                           capture_output=True, text=True).stdout)
W = [w for w in json.load(open(os.path.join(ROOT, "plan", "transcript_scribe.json")))["segments"][0]["words"] if w["text"].strip()]
for _w in W:
    _w["start_time"] += OFFSET
    _w["end_time"] += OFFSET
last = max(i for i in range(len(W)) if not any(a <= i <= b for a, b in CUT_WORDS))
start, end = max(0, W[0]["start_time"] - .05), min(dur, W[last]["end_time"] + .12)
rem = [(a + KEEP / 2, b - KEEP / 2) for a, b in zip(st, en) if b - a - KEEP > .02]
for a, b in CUT_WORDS:                     # a cut runs from just before its first word to just before the next kept word
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
segs = [(round(a * 30) / 30, round(b * 30) / 30) for a, b in segs]      # whole frames: picture and sound stay locked
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
    return round(t, 3)                     # a removed word lands on the next kept moment


words = [{"text": w["text"], "s": to_tight(w["start_time"]), "e": to_tight(w["end_time"]),
          "cut": any(a <= i <= b for a, b in CUT_WORDS)} for i, w in enumerate(W)]
json.dump(cuts, open(os.path.join(ROOT, "plan", "cuts.json"), "w"), indent=0)
json.dump(words, open(os.path.join(ROOT, "plan", "words_tight.json"), "w"), ensure_ascii=False, indent=0)

# each piece encoded on its own (one 50-branch filter graph on the 1080p file ran out of memory), then joined
tmp = os.path.join(ROOT, "cache", "pieces")
os.makedirs(tmp, exist_ok=True)
lst = []
for k, (a, b) in enumerate(segs):
    d = b - a
    out = os.path.join(tmp, f"p{k:03d}.mov")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", RAW, "-frames:v", str(round(d * 30)), "-t", f"{d:.4f}",
                    "-af", f"afade=t=in:d=0.008,afade=t=out:st={d - .012:.3f}:d=0.008,apad=whole_dur={d:.4f},atrim=0:{d:.4f}", "-r", "30",
                    "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000",
                    out], check=True)
    lst.append(f"file '{out}'")
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-c", "copy",
                os.path.join(ROOT, "assets", "video", "tight.mov")], check=True)
print(f"{len(segs)} pieces, {t:.2f} s (raw {dur:.2f} s, speech {start:.2f}-{end:.2f})")
