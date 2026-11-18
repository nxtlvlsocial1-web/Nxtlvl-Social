"""Tight cut of Dr S Kokila's "children / prejudice" take (footage/IMG_0601.mov, 4K iPhone, 1:56 with long pauses and a
repeated line) into the reel's spoken line-up. Same method as kokila-peace-9x16 (approved there): the clean take of each
line, speech edges from silencedetect, pauses inside a line cut to 0.1-0.18 s, two frames between lines, 1.08x with pitch
kept, cut once from the 4K original. Writes assets/video/tight.mp4, plan/cuts.json, plan/words_tight.json.
python3 build/tight.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "footage", "IMG_0601.mov")
# one scale from 4K to 1080x1920 (full-range iPhone video converted to TV range properly), a light sharpen
VF = "scale=1080:1920:flags=lanczos:in_range=full:out_range=tv,unsharp=5:5:0.45:5:5:0.0,format=yuv420p"
SPEED = 1.08
THRESH, MINSIL, KEEP = -32, .16, .1
GAP = .06                                   # v4 (owner: "only the part where she speaks, not her looking left or right
                                            # in between"): two frames between lines, not 0.22 s of her looking away
W = json.load(open(os.path.join(ROOT, "plan", "words_raw.json")))
# (id, first word, last word) or (id, "silent", start, end)
LINES = [("L1", 0, 6),         # Have you seen two children playing together?
         ("L2", 7, 13),        # One is Hindu, the other is Muslim.
         ("L3", 14, 20),       # One is black, the other is white.
         ("L4", 21, 27),       # But do you know what they see?
         ("L5", 28, 29),       # A friend.
         ("L6", 30, 39),       # They don't ask which God the other child prays to.
         ("L7", 40, 48),       # They don't ask which country their parents are from.
         ("L8", 49, 53, 28.0), # They just laugh, enjoy, share. (Whisper puts "They" on the tail of "from.")
         ("L9", 54, 63),       # But somewhere along the way, we adults begin teaching them
         ("L10", 64, 68),      # who is different, who belongs
         ("L11", 69, 73),      # and sometimes who to fear.
         ("L12", 74, 82),      # And that's how our brain learns fear and prejudice.
         ("L13", 83, 87),      # But here's a beautiful part:
         ("L14", 88, 93),      # our brain can learn empathy too.
         ("L15", 101, 107, 87.38),  # Children can be taught compassion before discrimination. (second take; the first,
                                    # 82.7-86.5, is dropped)
         ("L16", 108, 120),    # They can be taught a little more kindness and a little more compassion.
         ("L17", 121, 132)]    # And that's how, when we begin healing ourselves, we begin healing humanity.


def silences(a, b):
    log = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", RAW, "-vn", "-af",
                          f"highpass=f=90,silencedetect=noise={THRESH}dB:d={MINSIL}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) + a for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    en = [float(x) + a for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(st, en))


def speech_edges(a, b, pre=.05, post=.1):
    """v4: trim a range to her voice: from just before the first sound to just after the last (silencedetect at THRESH)"""
    sil = silences_fine(a, b)
    if sil and sil[0][0] <= a + .02:
        a = max(a, sil[0][1] - pre)
    if sil and sil[-1][1] >= b - .02:
        b = min(b, sil[-1][0] + post)
    return a, b


def silences_fine(a, b):
    log = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", RAW, "-vn", "-af",
                          f"highpass=f=90,silencedetect=noise={THRESH}dB:d=0.05", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) + a for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    en = [float(x) + a for x in re.findall(r"silence_end: ([\d.]+)", log)]
    if len(en) < len(st):
        en.append(b)
    return list(zip(st, en))


pieces = []           # (line, src a, src b, mute)
for ln in LINES:
    if ln[1] == "silent":
        pieces.append((ln[0], ln[2], ln[3], True))
        continue
    lid, i, j = ln[:3]
    a = ln[3] if len(ln) > 3 else W[i]["s"] - .08
    a, b0 = speech_edges(a, W[j]["e"] + .4 if j + 1 >= len(W) else min(W[j]["e"] + .4, W[j + 1]["s"] - .03))
    b = b0                                             # v4: the line ends where her voice ends (+ a short tail), not on Whisper's guess
    if ln is LINES[-1]:
        b += .3                                        # end on her face, a beat after "humanity."
    cur = a
    for s, e in silences(a, b):
        keep = min(.18, KEEP + .04 * (e - s))          # v4: short, so no glance away survives a pause (v2 kept up to 0.3 s)
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
                        "-af", "volume=0.15", "-vf", VF, "-r", "30", "-c:v", "libx264", "-crf", "10", "-preset", "fast", "-pix_fmt", "yuv420p",
                        "-c:a", "pcm_s16le", "-ar", "48000", gp], check=True)
        lst.append(f"file '{gp}'")
        t += GAP
    d = b - a
    out = os.path.join(tmp, f"p{k:03d}.mov")
    af = f"afade=t=in:d=0.008,afade=t=out:st={d - .012:.3f}:d=0.008,apad=whole_dur={d:.4f},atrim=0:{d:.4f}"
    if mute:
        af = "volume=0.12," + af
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", RAW, "-frames:v", str(round(d * 30)), "-t", f"{d:.4f}",
                    "-af", af, "-vf", VF, "-r", "30", "-c:v", "libx264", "-crf", "10", "-preset", "fast", "-pix_fmt", "yuv420p",
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
                "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
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
