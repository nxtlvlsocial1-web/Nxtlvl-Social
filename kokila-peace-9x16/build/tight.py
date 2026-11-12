"""Tight cut of Dr S Kokila's take (footage/face_1080.mp4, 2:40 with retakes) into the reel's spoken line-up.

Lines are word ranges of plan/words_raw.json (build/words.py), the clean take of each: the first "So let me tell you
of a tracker" take has a long stall, so take 2 is used; of the four "our social environment" attempts only the last
is whole ("the people in our environment affect our peace of mind and mental health the most"). Two silent pieces of
her looking into the lens are kept too: HOOK (under Deepinder's own soundbite, which plays in the top half) and BEAT
(v2: the text beat she did not record is gone, owner: "remove the things that she is not speaking").

Inside every line, pauses quieter than THRESH for MINSIL or longer (silencedetect after a 90 Hz high-pass) are cut to
KEEP (half each side). Pieces carry PCM audio (AAC pieces each add encoder padding and drifted the voice ~1 s
behind the picture over 50 joins) and are joined with 8 ms audio fades, then the whole is sped to SPEED (pitch kept).
Writes assets/video/tight.mp4, plan/cuts.json, plan/words_tight.json (words on the tight clock, with their line).
python3 build/tight.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "footage", "face_1080.mp4")
SPEED = 1.08
THRESH, MINSIL, KEEP = -32, .16, .1
GAP = .22                                   # pause left between two lines
W = json.load(open(os.path.join(ROOT, "plan", "words_raw.json")))
# (id, first word, last word) or (id, "silent", start, end)
LINES = [("HOOK", "silent", .5, 3.4),
         ("L1", 0, 39),       # Deepinder Goyal's Temple costs 85,000 rupees ... Does it work? We don't know yet.
         ("L2", 65, 90),      # So let me tell you of a tracker that is completely free. It does not need ... your time.
         ("L3", 91, 98),      # And that tracker is the people around you.
         ("L4", 99, 118),     # Just ask yourself, are the people in your life ... constantly complaining, criticizing and disrespecting you
         ("L5", 119, 144),    # or are the people in your life ... loving you, supporting you and inspiring you ... best version of yourself?
         ("L6", 187, 202),    # because the people in our environment affect our peace of mind and mental health the most.
         ("L7", 203, 213),    # So surround yourself with people that make your life more beautiful
         ("L8", 214, 236)]    # because sometimes the greatest upgrade ... may not be a device, it is simply the beautiful people in your life.


def silences(a, b):
    log = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", RAW, "-vn", "-af",
                          f"highpass=f=90,silencedetect=noise={THRESH}dB:d={MINSIL}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) + a for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    en = [float(x) + a for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(st, en))


pieces = []           # (line, src a, src b, mute)
for ln in LINES:
    if ln[1] == "silent":
        pieces.append((ln[0], ln[2], ln[3], True))
        continue
    lid, i, j = ln
    a = W[i]["s"] - .08
    b = W[j]["e"] + .15
    if j + 1 < len(W):
        b = min(b, W[j + 1]["s"] - .03)
    if ln is LINES[-1]:
        b += .55                                       # v2: end on her face, half a second after "life."
    cur = a
    for s, e in silences(a, b):
        keep = min(.3, KEEP + .12 * (e - s))           # v2 (owner: "bad cuts"): a long pause keeps more of itself
        s2, e2 = s + keep / 2, e - keep / 2
        if e2 - s2 > .03 and s2 > cur:
            if s2 - cur >= .18 or not pieces or pieces[-1][0] != lid:
                pieces.append((lid, cur, s2, False))
            else:                                      # a sliver between two pauses: join it to the piece before
                pl = pieces.pop()
                pieces.append((lid, pl[1], s2, False))
            cur = e2
    pieces.append((lid, cur, b, False))
pieces = [(l, round(a * 30) / 30, round(b * 30) / 30, m) for l, a, b, m in pieces]
pieces = [p for p in pieces if p[2] - p[1] > .05]

tmp = os.path.join(ROOT, "cache", "pieces")
os.makedirs(tmp, exist_ok=True)
lst, cuts, t, prev = [], [], 0.0, None
for k, (lid, a, b, mute) in enumerate(pieces):
    if prev is not None and lid != prev:          # a short real pause between lines (room tone from just after the line)
        gp = os.path.join(tmp, f"g{k:03d}.mov")
        ga = cuts[-1]["src"][1]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ga:.4f}", "-i", RAW, "-frames:v", str(round(GAP * 30)), "-t", f"{GAP:.4f}",
                        "-af", "volume=0.15", "-r", "30", "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-pix_fmt", "yuv420p",
                        "-c:a", "pcm_s16le", "-ar", "48000", gp], check=True)
        lst.append(f"file '{gp}'")
        t += GAP
    d = b - a
    out = os.path.join(tmp, f"p{k:03d}.mov")
    af = f"afade=t=in:d=0.008,afade=t=out:st={d - .012:.3f}:d=0.008,apad=whole_dur={d:.4f},atrim=0:{d:.4f}"
    if mute:
        af = "volume=0.12," + af
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", RAW, "-frames:v", str(round(d * 30)), "-t", f"{d:.4f}",
                    "-af", af, "-r", "30", "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", out], check=True)
    lst.append(f"file '{out}'")
    cuts.append({"line": lid, "src": [a, b], "at": round(t, 3), "mute": mute})
    t += d
    prev = lid
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst) + "\n")
one = os.path.join(tmp, "tight_1x.mov")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-c", "copy", one], check=True)
os.makedirs(os.path.join(ROOT, "assets", "video"), exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", one, "-vf", f"setpts=PTS/{SPEED}", "-af", f"atempo={SPEED}", "-r", "30",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                os.path.join(ROOT, "assets", "video", "tight.mp4")], check=True)


def to_tight(x):
    for c in cuts:
        a, b = c["src"]
        if a - .02 <= x <= b + .02:
            return round((c["at"] + max(0.0, x - a)) / SPEED, 3)
    return None


lines = {}
for c in cuts:
    lines.setdefault(c["line"], [c["at"] / SPEED, 0])
    lines[c["line"]][1] = (c["at"] + c["src"][1] - c["src"][0]) / SPEED
words = []
for ln in LINES:
    if ln[1] == "silent":
        continue
    for i in range(ln[1], ln[2] + 1):
        s, e = to_tight(W[i]["s"]), to_tight(W[i]["e"])
        if s is None:
            s = to_tight(W[i]["s"] + .1) or (words[-1]["e"] if words else 0)
        if e is None:
            e = s + .2
        words.append({"line": ln[0], "i": i, "w": W[i]["w"], "s": s, "e": max(e, s + .08)})
json.dump(cuts, open(os.path.join(ROOT, "plan", "cuts.json"), "w"), indent=0)
json.dump({"speed": SPEED, "dur": round(t / SPEED, 3), "lines": {k: [round(a, 3), round(b, 3)] for k, (a, b) in lines.items()}, "words": words},
          open(os.path.join(ROOT, "plan", "words_tight.json"), "w"), indent=0)
print(f"{len(pieces)} pieces, {t:.2f} s at 1x -> {t / SPEED:.2f} s at {SPEED}x")
for k, (a, b) in lines.items():
    print(f"  {k}: {a:6.2f} - {b:6.2f}")
