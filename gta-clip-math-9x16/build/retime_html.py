"""Rewrites the clip windows in index.html from build/timing.json (the voice timeline).

python3 build/retime_html.py      (after build/voice.py)
Scene clips keep their old (authored) windows in OLD_WINDOWS below; their data-start / data-duration become the warped
times. Full-length layers (canvas, vignette, captions, effects, grain, progress, audio) and the root get the new length.
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "timing.json")))
W, END = T["warp"], T["newEnd"]
OLD_WINDOWS = {"s1": (0, 3), "s2": (3, 5), "s3": (5, 7), "s4": (7, 11), "s5": (11, 15), "s6": (15, 18), "s7": (18, 21), "s9": (23, 28),
               "s10": (28, 32), "s11": (32, 34), "s12": (34, 37), "s13": (37, 39.62), "le": (39.62, 40)}
FULL = ["root", "gl", "vg", "caps", "fx", "grain", "prog", "sfx"]

def o2n(t):
    for (a, an), (b, bn) in zip(W, W[1:]):
        if t <= b: return an + (bn - an) * (t - a) / (b - a)
    return W[-1][1]

p = os.path.join(ROOT, "index.html"); s = open(p).read()
def set_window(s, el_id, start, dur):
    pat = re.compile(r'(id="%s"[^>]*?data-start=")[^"]*("[^>]*?data-duration=")[^"]*(")' % re.escape(el_id))
    s2, n = pat.subn(lambda m: f'{m.group(1)}{start:g}{m.group(2)}{dur:g}{m.group(3)}', s, count=1)
    assert n == 1, el_id
    return s2
for k, (a, b) in OLD_WINDOWS.items():
    na, nb = round(o2n(a), 3), round(o2n(b), 3)
    s = set_window(s, k, na, round(nb - na, 3))
for k in FULL:
    s = set_window(s, k, 0, END)
open(p, "w").write(s)
print("retimed; reel", END, "s")
