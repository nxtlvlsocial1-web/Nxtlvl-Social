"""Shared timeline helpers (word times, GSAP tween writers, sfx cues), trimmed from the Creedom reels' fx.py.
generate.py imports from here; JS and SFX are the shared output lists."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.environ.get("WORDS", os.path.join(ROOT, "plan", "words.json"))))
PINK, MAG, ROSE, INK = "#EE688B", "#F343A2", "#B1476B", "#0B0B0B"
LINES = {}
for w in W:
    LINES.setdefault(w["line"], []).append(w)
L0 = {k: v[0]["t0"] for k, v in LINES.items()}
L1 = {k: v[-1]["t1"] for k, v in LINES.items()}
JS, SFX, HTML = [], [], []


def T(line, word, n=0):
    k = word.lower()
    hits = [w for w in LINES[line] if w["w"].lower().strip('.,:!?"').startswith(k)]
    return hits[min(n, len(hits) - 1)]["t0"]


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def ft(sel, t, d, frm, to, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


