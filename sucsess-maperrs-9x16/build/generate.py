"""Sucsess Maperrs talking-head ad. 1080x1920, 30 fps, cut by build/edl.py.

python3 -I build/generate.py      (run from the project root, after build/edl.py)

Format from the reference reel: the presenter switches between three framings, FULL (close, captions on her),
SPLIT (small and low, with the app's UI up top) and FOCUS (she steps out and the UI fills the frame), and the end is a
glowing CTA on a dark vignette. Her matte (assets/video/talk_fg.webm from hyperframes remove-background, edge choked 2 px and feathered into talk_fg_clean.webm so no wall fringe shows) sits on the app's own
world: near-black #15110E, gold #DAB66A, cream #F2EADD, sage #839172, plum #261F2F; Fraunces (display, gold italic accents),
Manrope (body), JetBrains Mono (spaced labels). A slowly turning compass rose from the logo, gold dust and a halo behind
her head keep the backdrop alive; big words can sit behind her (between backdrop and matte). Captions are English
translations of the Hinglish speech (client requirement), in phrase chunks timed across each spoken line. The brand is
always spelled Sucsess Maperrs.
"""
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDL = json.load(open(os.path.join(ROOT, "build", "edl.json")))
VO = EDL["duration"]
HOLD = 1.5                                   # CTA held after the last word
DUR = round(VO + HOLD, 2)
L = [(l["start"], l["end"]) for l in EDL["lines"]]
BG, PANEL, CARD, CARD2, BORDER = "#15110E", "#211C18", "#2E2717", "#38301D", "#615230"
GOLD, CREAM, SAGE, PLUM, LAV, MUTED, RED = "#DAB66A", "#F2EADD", "#839172", "#261F2F", "#B7A8E0", "#A89F8E", "#C8323A"

T = []
EV = []          # (time, kind[, length]) — audio.py gives every visual event its sound


def add(js):
    T.append("      " + js)


def ev(t, kind, d=0):
    EV.append((round(t, 3), kind, round(d, 3)))


def clip(cid, a, z, inner, track=3, cls="scene"):
    return (f'<div id="{cid}" class="clip {cls}" data-start="{a:.3f}" data-duration="{z - a:.3f}" data-track-index="{track}" '
            f'data-layout-allow-overflow>{inner}</div>')


def pop(sel, t, frm="opacity:0,y:40,scale:.92", d=.5, ease="expo.out", sound="pop"):
    if sound:
        ev(t, sound)
    add(f'tl.fromTo("{sel}",{{{frm}}},{{opacity:1,x:0,y:0,scale:1,rotation:0,rotationX:0,rotationY:0,duration:{d},ease:"{ease}"}},{t:.2f});')


def out(sel, t, to="opacity:0,y:-30", d=.3):
    add(f'tl.to("{sel}",{{{to},duration:{d},ease:"power2.in"}},{t:.2f});')


def words_in(sel, t, stagger=.06, d=.55):
    add(f'tl.fromTo("{sel}",{{opacity:0,y:50,rotationX:-60}},{{opacity:1,y:0,rotationX:0,duration:{d},stagger:{stagger},'
        f'ease:"expo.out"}},{t:.2f});')


def counter(sel, a, z, t, d, prefix="", suffix=""):
    ev(t, "count", d * .85)
    add(f'(()=>{{const o={{v:{a}}};tl.to(o,{{v:{z},duration:{d},ease:"expo.out",onUpdate:()=>{{'
        f'document.querySelectorAll("{sel}").forEach(e=>e.textContent="{prefix}"+Math.round(o.v).toLocaleString("en-IN")+"{suffix}");}}}},{t:.2f});}})();')


def draw(sel, t, d=.8, ease="power2.inOut"):
    add(f'tl.fromTo("{sel}",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:{d},ease:"{ease}"}},{t:.2f});')


# ------------------------------------------------------------------ art
def star4(s, col=RED):
    return (f'<svg viewBox="-50 -50 100 100" width="{s}" height="{s}"><path d="M0 -50 C5 -8 8 -5 50 0 C8 5 5 8 0 50 '
            f'C-5 8 -8 5 -50 0 C-8 -5 -5 -8 0 -50 Z" fill="{col}"/></svg>')


def compass_rose(size=1500, op=1):
    ticks = "".join(f'<line x1="0" y1="{-r1}" x2="0" y2="{-r1 - (14 if k % 6 else 30)}" transform="rotate({k * 5})" stroke="{GOLD}" '
                    f'stroke-width="{1.5 if k % 6 else 3}"/>' for k in range(72) for r1 in [560])
    pts = "".join(f'<path d="M0 -500 L22 -22 L0 0 L-22 -22 Z" transform="rotate({k * 45})" fill="{GOLD}" opacity="{.5 if k % 2 else .9}"/>'
                  for k in range(8))
    return (f'<svg viewBox="-700 -700 1400 1400" width="{size}" height="{size}" style="opacity:{op}">'
            f'<circle r="600" fill="none" stroke="{GOLD}" stroke-width="2"/><circle r="560" fill="none" stroke="{GOLD}" stroke-width="1"/>'
            f'<circle r="380" fill="none" stroke="{GOLD}" stroke-width="1" stroke-dasharray="6 14"/>{ticks}{pts}'
            f'<circle r="180" fill="none" stroke="{GOLD}" stroke-width="1.5"/></svg>')


def compass_dial(size=420):
    """The logo's compass: gold ring, cross arms, a red needle that can swing (.needle)."""
    arms = "".join(f'<path d="M0 -190 L10 -10 L0 0 L-10 -10 Z" transform="rotate({k * 90})" fill="{GOLD}"/>' for k in range(4))
    small = "".join(f'<path d="M0 -120 L6 -8 L0 0 L-6 -8 Z" transform="rotate({45 + k * 90})" fill="{GOLD}" opacity=".7"/>' for k in range(4))
    return (f'<svg class="dial" viewBox="-210 -210 420 420" width="{size}" height="{size}">'
            f'<circle class="dring" r="200" fill="none" stroke="{GOLD}" stroke-width="6" pathLength="1"/>'
            f'<circle r="186" fill="rgba(30,58,30,.35)" stroke="{GOLD}" stroke-width="1.5" opacity=".7"/>{small}{arms}'
            f'<g class="needle"><path d="M0 -170 L16 0 L0 22 L-16 0 Z" fill="{RED}"/><path d="M0 170 L16 0 L0 -6 L-16 0 Z" fill="{GOLD}"/></g>'
            f'<circle r="18" fill="#c9b37a" stroke="#7a6a3a" stroke-width="3"/></svg>')


def phone(img, cls, w=360):
    return (f'<div class="phone {cls}" style="width:{w}px;height:{w * 2576 / 1186:.0f}px"><div class="scr">'
            f'<img src="assets/img/{img}" alt=""></div><i class="pglare"></i></div>')


def icon(name, s=56, col=GOLD, sw=3):
    p = {
        "check": f'<circle cx="24" cy="24" r="21" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M14 24.5 L21 31 L34 17" '
                 f'fill="none" stroke="{col}" stroke-width="{sw + .6}" stroke-linecap="round" stroke-linejoin="round"/>',
        "hour": f'<path d="M12 6 H36 M12 42 H36 M14 6 C14 18 34 22 34 42 M34 6 C34 18 14 22 14 42" fill="none" stroke="{col}" '
                f'stroke-width="{sw}" stroke-linecap="round"/><path d="M18 38 H30 L24 31 Z" fill="{col}"/>',
        "family": f'<circle cx="16" cy="13" r="6" fill="{col}"/><circle cx="33" cy="13" r="6" fill="{col}"/><circle cx="24.5" cy="27" r="4.5" fill="{col}"/>'
                  f'<path d="M6 40 C6 28 26 28 26 40 M23 40 C23 28 43 28 43 40" fill="none" stroke="{col}" stroke-width="{sw}"/>',
        "report": f'<rect x="9" y="5" width="30" height="38" rx="4" fill="none" stroke="{col}" stroke-width="{sw}"/>'
                  f'<path d="M15 15 H33 M15 22 H33 M15 29 H26" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>',
        "dice": f'<rect x="7" y="7" width="34" height="34" rx="8" fill="none" stroke="{col}" stroke-width="{sw}"/>'
                f'<circle cx="17" cy="17" r="3" fill="{col}"/><circle cx="31" cy="31" r="3" fill="{col}"/><circle cx="24" cy="24" r="3" fill="{col}"/>',
        "spark": f'<path d="M24 4 C26 18 30 22 44 24 C30 26 26 30 24 44 C22 30 18 26 4 24 C18 22 22 18 24 4 Z" fill="{col}"/>',
        "brain": f'<circle cx="24" cy="24" r="18" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M24 8 V40 M12 18 C18 18 18 26 24 26 '
                 f'M36 18 C30 18 30 26 24 26 M14 32 C20 30 22 34 24 34 M34 32 C28 30 26 34 24 34" fill="none" stroke="{col}" stroke-width="2.6"/>',
        "heart": f'<path d="M24 41 C12 32 5 25 5 16 C5 10 10 6 15 6 C19 6 22 8 24 12 C26 8 29 6 33 6 C38 6 43 10 43 16 C43 25 36 32 24 41 Z" '
                 f'fill="none" stroke="{col}" stroke-width="{sw}"/>',
        "target": f'<circle cx="24" cy="24" r="19" fill="none" stroke="{col}" stroke-width="{sw}"/><circle cx="24" cy="24" r="11" fill="none" '
                  f'stroke="{col}" stroke-width="{sw}"/><circle cx="24" cy="24" r="4" fill="{col}"/>',
        "user": f'<circle cx="24" cy="16" r="8" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M8 42 C8 30 40 30 40 42" fill="none" '
                f'stroke="{col}" stroke-width="{sw}"/>',
        "cap": f'<path d="M2 18 L24 8 L46 18 L24 28 Z" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>'
               f'<path d="M11 22 V33 C11 37 37 37 37 33 V22" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M44 19 V31" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>',
        "flask": f'<path d="M18 5 H30 M20 5 V18 L8 40 C7 42 8 44 11 44 H37 C40 44 41 42 40 40 L28 18 V5" fill="none" stroke="{col}" '
                 f'stroke-width="{sw}" stroke-linejoin="round"/><path d="M13 32 H35" stroke="{col}" stroke-width="{sw}"/>',
        "calc": f'<rect x="10" y="5" width="28" height="38" rx="4" fill="none" stroke="{col}" stroke-width="{sw}"/><rect x="15" y="10" width="18" height="8" '
                f'fill="{col}"/><circle cx="17" cy="26" r="2.4" fill="{col}"/><circle cx="24" cy="26" r="2.4" fill="{col}"/><circle cx="31" cy="26" r="2.4" fill="{col}"/>'
                f'<circle cx="17" cy="35" r="2.4" fill="{col}"/><circle cx="24" cy="35" r="2.4" fill="{col}"/><circle cx="31" cy="35" r="2.4" fill="{col}"/>',
        "palette": f'<path d="M24 5 C12 5 4 14 4 24 C4 35 13 43 23 43 C27 43 27 39 25 37 C23 35 24 31 28 31 H34 C40 31 44 27 44 21 C44 12 35 5 24 5 Z" '
                   f'fill="none" stroke="{col}" stroke-width="{sw}"/><circle cx="14" cy="22" r="3" fill="{col}"/><circle cx="21" cy="13" r="3" fill="{col}"/>'
                   f'<circle cx="32" cy="14" r="3" fill="{col}"/>',
        "briefcase": f'<rect x="5" y="14" width="38" height="27" rx="5" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M17 14 V9 C17 7 18 6 20 6 H28 '
                     f'C30 6 31 7 31 9 V14 M5 25 H43" fill="none" stroke="{col}" stroke-width="{sw}"/>',
        "lock": f'<rect x="10" y="21" width="28" height="22" rx="5" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M16 21 V15 C16 6 32 6 32 15 V21" '
                f'fill="none" stroke="{col}" stroke-width="{sw}"/><circle cx="24" cy="32" r="3" fill="{col}"/>',
        "badge": f'<rect x="6" y="12" width="36" height="24" rx="6" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M13 21 H35 M13 28 H27" '
                 f'stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>',
        "route": f'<circle cx="11" cy="38" r="5" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M15 34 C26 26 12 18 24 12 L34 8" fill="none" '
                 f'stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="4 5"/><path d="M30 4 L40 7 L34 15" fill="none" stroke="{col}" '
                 f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>',
        "moon": f'<path d="M31 6 C20 9 14 20 18 30 C22 40 34 44 43 38 C30 40 21 28 25 17 C26 12 28 9 31 6 Z" fill="none" stroke="{col}" stroke-width="{sw}" '
                f'stroke-linejoin="round"/><circle cx="12" cy="12" r="2" fill="{col}"/><circle cx="8" cy="26" r="1.6" fill="{col}"/>',
        "orb": f'<circle cx="24" cy="21" r="15" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M14 40 H34 L31 34 H17 Z" fill="none" stroke="{col}" '
               f'stroke-width="{sw}" stroke-linejoin="round"/><path d="M17 16 C19 12 23 11 26 12" fill="none" stroke="{col}" stroke-width="2"/>',
        "seal": f'<circle cx="24" cy="19" r="13" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M17 30 L13 44 L19 40 L24 45 L24 33 M31 30 L35 44 '
                f'L29 40 L24 45" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/><path d="M18 19 L22 23 L30 15" fill="none" '
                f'stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>',
        "smile": f'<circle cx="24" cy="24" r="19" fill="none" stroke="{col}" stroke-width="{sw}"/><circle cx="17" cy="19" r="2.6" fill="{col}"/>'
                 f'<circle cx="31" cy="19" r="2.6" fill="{col}"/><path d="M15 29 C19 35 29 35 33 29" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>',
        "compass": f'<circle cx="24" cy="24" r="19" fill="none" stroke="{col}" stroke-width="{sw}"/><path d="M31 13 L27 27 L17 35 L21 21 Z" fill="none" '
                   f'stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>',
        "numbers": f'<text x="24" y="31" text-anchor="middle" font-family="Fraunces" font-style="italic" font-weight="700" font-size="22" fill="{col}">1·7·9</text>',
    }[name]
    return f'<svg viewBox="0 0 48 48" width="{s}" height="{s}">{p}</svg>'


def tile(name, s=150, col=GOLD, cls=""):
    """An app-style icon tile: gold-tinted card, border, glow."""
    return f'<div class="tile {cls}" style="width:{s}px;height:{s}px">{icon(name, s * .52, col)}</div>'


def coin(s):
    return (f'<div class="coin" style="width:{s}px;height:{s}px;font-size:{s * .55:.0f}px">₹</div>')


# ------------------------------------------------------------------ framings
# Three framings, as in the reference: FULL (close-up, the whole frame), SPLIT (the frame divides at y 960: visuals on
# top, her head and shoulders filling the bottom half edge to edge, a gold seam between) and FOCUS (she steps out and
# the visual fills the frame).
FACE_X, FACE_Y = 540, 720      # face centre in the source frame
SEAM = 960


def framing(scale, face_y):
    return dict(x=round(FACE_X - FACE_X * scale), y=round(face_y - FACE_Y * scale), scale=scale)


FULL = framing(1.18, 900)
FULL2 = framing(1.26, 905)
WIDE = framing(1.0, 720)
SPLIT = framing(1.04, 1330)
SHOT = {"full": FULL, "full2": FULL2, "split": SPLIT, "focus": SPLIT, "cta": WIDE}
# (time, shot): one per line, plus the brand reveal handing over to a split
SHOTS = sorted([(L[i][0], s) for i, s in enumerate(["full", "split", "focus", "full2", "split", "focus", "focus", "full", "full2",
                                                    "split", "focus", "split", "focus", "full", "split", "cta"])] +
               [(L[5][0] + 2.6, "split")])


def shot_at(t):
    return [s for a, s in SHOTS if a <= t + 1e-6][-1]


def frame_tl():
    f = SHOT[SHOTS[0][1]]
    add(f'tl.set("#spkw",{{x:{f["x"]},y:{f["y"]},scale:{f["scale"]},opacity:1}},0);')
    add('tl.set("#spkcrop",{clipPath:"inset(0px 0px 0px 0px)"},0);tl.set(".seam, #panelbg",{opacity:0},0);')
    prev = SHOTS[0][1]
    for t, s in SHOTS[1:]:
        f = SHOT[s]
        if s == prev:
            # the same framing across a cut: a small punch-in hides the jump
            add(f'tl.set("#spkw",{{scale:{f["scale"] * 1.06:.3f},x:{f["x"] - 32},y:{f["y"] - 40}}},{t:.2f});')
            continue
        st = t - .22
        vis = 0 if s == "focus" else 1
        add(f'tl.to("#spkw",{{x:{f["x"]},y:{f["y"]},scale:{f["scale"]},opacity:{vis},duration:.55,ease:"expo.inOut"}},{st:.2f});')
        crop = f"inset({SEAM}px 0px 0px 0px)" if s == "split" else "inset(0px 0px 0px 0px)"
        add(f'tl.to("#spkcrop",{{clipPath:"{crop}",duration:.55,ease:"expo.inOut"}},{st:.2f});')
        add(f'tl.to(".seam, #panelbg",{{opacity:{1 if s == "split" else 0},duration:.4}},{st + .1:.2f});')
        ev(st, "whoosh")
        prev = s
    # cuts inside a line keep the framing: punch them
    for c in EDL["cuts"]:
        if not any(abs(c - a) < .05 for a, _ in L):
            f = SHOT[shot_at(c)]
            add(f'tl.set("#spkw",{{scale:{f["scale"] * 1.05:.3f},x:{f["x"] - 20},y:{f["y"] - 30}}},{c:.2f});')


# ------------------------------------------------------------------ captions (the only words on screen that echo her)
EMPH = {"lakhs", "strengths", "interests", "marks.", "family", "one", "direction", "Sucsess", "Maperrs.", "personality,",
        "aptitude", "optional,", "reflective", "not", "guaranteed", "alignment", "informed", "satisfaction.", "2-minute",
        "90%", "2,300.", "guesswork.", "yourself,", "future.", "free."}


def chunks(text, n=4):
    ws = text.split()
    out_, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= n or w[-1] in ".,?":
            if len(cur) >= 2 or w[-1] in ".?":
                out_.append(cur)
                cur = []
    if cur:
        if out_ and len(cur) == 1:
            out_[-1] += cur
        else:
            out_.append(cur)
    return out_


def caption_plan():
    plan = []
    for li, (a, z) in enumerate(L):
        if li == 15:
            continue                       # the end card carries the last line
        ch = chunks(EDL["lines"][li]["text"])
        wts = [sum(len(w) for w in c) + 3 for c in ch]
        tot, t = sum(wts), a + .05
        for c, w in zip(ch, wts):
            d = (z - a - .1) * w / tot
            plan.append((round(t, 3), round(t + d, 3), c))
            t += d
    return plan


def captions_html():
    h = []
    for k, (a, _, c) in enumerate(caption_plan()):
        top = 832 if shot_at(a + .2) == "split" else 1400     # in a split the caption sits on the seam, above her
        ws = "".join(f'<span class="cw{" em" if w in EMPH else ""}">{w}</span> ' for w in c)
        h.append(f'<div class="cap cap{k}" style="top:{top}px">{ws}</div>')
    return "".join(h)


def captions_tl():
    for k, (a, z, c) in enumerate(caption_plan()):
        add(f'tl.fromTo(".cap{k} .cw",{{opacity:0,y:26,scale:.9}},{{opacity:1,y:0,scale:1,duration:.32,stagger:.05,ease:"back.out(2.2)",'
            f'immediateRender:false}},{a:.2f});')
        add(f'tl.set(".cap{k}",{{opacity:1}},{a:.2f});tl.set(".cap{k}",{{opacity:0}},{z:.2f});')


# ------------------------------------------------------------------ scenes: visuals only, no words that repeat her
def scenes():
    r = random.Random(7)
    h = []
    # 0 full — investing lakhs in education: coins pour into a graduation cap
    a, z = L[0]
    coins = "".join(f'<div class="cn cn{i}" style="left:{r.uniform(40, 980):.0f}px">{coin(r.choice([70, 90, 120]))}</div>' for i in range(14))
    drops = "".join(f'<div class="cd cd{i}">{coin(60)}</div>' for i in range(5))
    h.append(clip("s0", a, L[1][0] + .3, f'<div class="capw">{tile("cap", 190)}<div class="capglow"></div>{drops}</div>'))
    h.append(clip("s0b", a, L[1][0] + .3, f'<div class="coins">{coins}</div>', track=1, cls="behind"))
    # 1 split — have you mapped their strengths and interests? a child, two dim orbs that light up, time turning
    a, z = L[1]
    h.append(clip("s1", a, z + .2, (
        f'<div class="kid"><div class="kring"></div>{icon("user", 170, CREAM, 2.4)}</div>'
        f'<div class="orbx ox1">{tile("target", 150, GOLD)}<b class="qq">?</b></div>'
        f'<div class="orbx ox2">{tile("heart", 150, GOLD)}<b class="qq">?</b></div>'
        f'<div class="hglass">{icon("hour", 96, MUTED)}</div>')))
    # 2 focus — marks pick the stream, family picks the career
    a, z = L[2]
    h.append(clip("s2", a, z + .2, (
        f'<div class="flow f1"><div class="rep">{tile("report", 170)}<div class="grade">92%</div></div><i class="farr"></i>'
        f'<div class="fork">{tile("flask", 120, CREAM, "fk fk0")}{tile("calc", 120, CREAM, "fk fk1")}{tile("palette", 120, CREAM, "fk fk2")}</div></div>'
        f'<div class="flow f2">{tile("family", 170)}<i class="farr"></i>{tile("briefcase", 170, CREAM, "bc")}<div class="lk">{icon("lock", 70, GOLD)}</div></div>')))
    # 3 full — one formula for every student: five different students, one mould comes down, they all turn the same
    a, z = L[3]
    studs = "".join(f'<div class="stu su{i}">{icon("user", 74, c)}</div>' for i, c in enumerate([SAGE, GOLD, LAV, "#E08A6A", "#7FB3C9"]))
    h.append(clip("s3", a, z + .2, f'<div class="studs">{studs}</div><div class="mold"></div>'))
    # 4 split — not just a job title, a direction: the compass needle swings from the badge to the path
    a, z = L[4]
    h.append(clip("s4", a, z + .2, (
        f'<div class="dialw">{compass_dial(400)}</div>'
        f'<div class="side4 sa">{tile("badge", 150, MUTED)}<i class="xline"></i></div>'
        f'<div class="side4 sb">{tile("route", 150, GOLD)}</div>')))
    # 5 brand — the logo reveal, then the app and its four dimensions as icon tiles
    a, z = L[5]
    dims = "".join(tile(n, 170, GOLD, f"dim dm{i}") for i, n in enumerate(["user", "heart", "brain", "target"]))
    h.append(clip("s5", a, z + .2, (
        '<div class="intro"><div class="halo"></div><img class="logo" src="assets/img/logo.png" alt="">'
        '<div class="wm">Sucsess Maperrs</div></div>' +
        phone("app1.jpg", "ph5", 220) + f'<div class="dims">{dims}</div>')))
    # 6 focus — numerology and the cosmic life cycle, an optional lens: orbits, a switch that is optional, the Inner Pattern
    a, z = L[6]
    stars = "".join(f'<i class="cs" style="left:{r.uniform(40, 1040):.0f}px;top:{r.uniform(260, 1500):.0f}px;'
                    f'width:{r.choice([3, 4, 6])}px;height:{r.choice([3, 4, 6])}px"></i>' for _ in range(60))
    h.append(clip("s6", a, z + .2, (
        f'<div class="cosmos">{stars}</div>'
        f'<div class="orbits"><div class="orb o1"><div class="och">{icon("numbers", 92, GOLD)}</div></div>'
        f'<div class="orb o2"><div class="och lv">{icon("moon", 70, LAV)}</div></div><div class="gem"></div></div>'
        '<div class="toggle"><i class="knob"></i></div>' + phone("app6.jpg", "ph6", 440))))
    # 7 full — no prediction, no guarantee: a crystal ball and a seal, both struck through
    a, z = L[7]
    h.append(clip("s7", a, z + .2, (
        f'<div class="nog ng1">{tile("orb", 170, LAV)}<i class="xl"></i></div>'
        f'<div class="nog ng2">{tile("seal", 170, LAV)}<i class="xl"></i></div>')))
    # 8 full2 — more than picking a career: the briefcase opens out into the compass
    a, z = L[8]
    h.append(clip("s8", a, z + .2, f'<div class="bigger"><div class="bring"></div>{tile("briefcase", 150)}<div class="bcomp">{icon("compass", 120, GOLD)}</div></div>'))
    # 9 split — strengths, possibilities, direction come into alignment
    a, z = L[9]
    h.append(clip("s9", a, z + .2, (
        f'<div class="venn"><div class="vc v1">{icon("target", 70, CREAM)}</div><div class="vc v2">{icon("spark", 70, CREAM)}</div>'
        f'<div class="vc v3">{icon("route", 70, CREAM)}</div><div class="vcore">{icon("spark", 110, "#fff6d8")}</div></div>')))
    # 10 focus — informed decisions and satisfaction: the app's home, two ticks
    a, z = L[10]
    h.append(clip("s10", a, z + .2, (
        phone("app7.jpg", "ph10", 430) +
        f'<div class="tick t1">{tile("brain", 130, SAGE)}<div class="tk">{icon("check", 54, SAGE)}</div></div>'
        f'<div class="tick t2">{tile("smile", 130, SAGE)}<div class="tk">{icon("check", 54, SAGE)}</div></div>')))
    # 11 split — the 2-minute scan: two screens and a two-minute timer
    a, z = L[11]
    h.append(clip("s11", a, z + .2, (
        phone("app2.jpg", "ph11a", 230) + phone("app3.jpg", "ph11b", 230) +
        '<div class="timer"><svg viewBox="0 0 200 200" width="250" height="250"><circle cx="100" cy="100" r="86" fill="none" '
        f'stroke="{CARD2}" stroke-width="14"/><circle class="tring" cx="100" cy="100" r="86" fill="none" stroke="{GOLD}" '
        'stroke-width="14" stroke-linecap="round" pathLength="1" transform="rotate(-90 100 100)"/></svg><div class="tnum">2:00</div></div>')))
    # 12 focus — the full assessment, 90% off, Rs 2,300
    a, z = L[12]
    h.append(clip("s12", a, z + .2, (
        phone("app4.jpg", "ph12", 420) +
        '<div class="offer"><img class="ologo" src="assets/img/logo.png" alt=""><div class="ostamp">90% OFF</div>'
        '<div class="oprice"><span class="cnt-price">₹0</span></div><i class="shine"></i></div>')))
    # 13 full — not guesswork: dice tumble in and are swept away, a compass lands
    a, z = L[13]
    dice = "".join(f'<div class="die dc{i}">{icon("dice", 96, GOLD)}</div>' for i in range(4))
    h.append(clip("s13", a, z + .2, dice + f'<div class="sweep"></div><div class="land">{tile("compass", 170)}</div>'))
    # 14 split — the brand, as she says the tagline
    a, z = L[14]
    h.append(clip("s14", a, z + .2, (
        '<div class="intro i14"><div class="halo"></div><img class="logo" src="assets/img/logo.png" alt=""><div class="wm">Sucsess Maperrs</div></div>')))
    # 15 cta — the end card carries the last line
    a = L[15][0]
    h.append(clip("s15", a, DUR, (
        '<div class="ctav"></div>'
        '<div class="cta"><img class="logo" src="assets/img/logo.png" alt="">'
        '<div class="ctab"><span>Instant Success Scan</span></div><div class="ctaf">FREE</div></div>')))
    return "".join(h)


def scenes_tl():
    # 0
    a, z = L[0]
    pop(".capw .tile", a + .02, "opacity:0,scale:.4,rotation:-20", .6, "back.out(2)")
    add(f'tl.fromTo(".capglow",{{opacity:0,scale:.5}},{{opacity:1,scale:1.1,duration:1.6,ease:"sine.inOut",yoyo:true,repeat:1}},{a:.2f});')
    add(f'document.querySelectorAll(".cd").forEach((e,i)=>{{tl.fromTo(e,{{x:(i-2)*90,y:-260,opacity:0,scale:.7}},{{x:0,y:20,opacity:1,scale:.5,'
        f'duration:.55,ease:"power2.in",immediateRender:false}},{a + .6:.2f}+i*.45);tl.to(e,{{opacity:0,duration:.08}},{a + 1.15:.2f}+i*.45);}});')
    add(f'tl.to(".capw .tile",{{scale:1.08,duration:.12,yoyo:true,repeat:9,ease:"power1.out"}},{a + 1.1:.2f});')
    ev(a + .6, "coins")
    add('document.querySelectorAll(".cn").forEach((e,i)=>{tl.fromTo(e,{y:-200,rotation:-30,opacity:0},{y:2100,rotation:200,opacity:1,'
        f'duration:2.4,ease:"power1.in",immediateRender:false}},{a + .3:.2f}+i*.16);}});')
    out(".capw", L[1][0] - .15, "opacity:0,y:-40,scale:.9")
    # 1
    a, z = L[1]
    pop(".kid", a + .1, "opacity:0,scale:.5", .6, "back.out(2)")
    draw(".kring", a + .1, .1)
    for k, tk in enumerate((a + .5, a + .7)):
        pop(f".ox{k + 1}", tk, f"opacity:0,x:{-160 if k == 0 else 160},scale:.6", .6, "back.out(2)", None)
    add(f'tl.set(".orbx .tile",{{filter:"grayscale(1) brightness(.6)"}},{a:.2f});')
    add(f'tl.fromTo(".qq",{{scale:.6}},{{scale:1.15,duration:.45,ease:"sine.inOut",yoyo:true,repeat:5}},{a + .9:.2f});')
    for k, tk in enumerate((a + 2.2, a + 3.6)):
        add(f'tl.to(".ox{k + 1} .tile",{{filter:"grayscale(0) brightness(1)",boxShadow:"0 0 70px rgba(218,182,106,.7)",duration:.4}},{tk:.2f});')
        add(f'tl.to(".ox{k + 1} .qq",{{opacity:0,scale:.3,duration:.25}},{tk:.2f});')
        ev(tk, "ping")
    add(f'tl.fromTo(".hglass svg",{{rotation:0}},{{rotation:180,duration:.7,ease:"power3.inOut",repeat:3,repeatDelay:.6}},{a + .4:.2f});')
    # 2
    a, z = L[2]
    pop(".f1 .rep .tile", a + .1, "opacity:0,x:-160,scale:.7", .55, "back.out(2)")
    add(f'tl.fromTo(".grade",{{opacity:0,scale:2.6,rotation:-16}},{{opacity:1,scale:1,rotation:-8,duration:.4,ease:"back.out(2.6)"}},{a + .7:.2f});')
    ev(a + .7, "stamp")
    add(f'tl.fromTo(".f1 .farr",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power2.out"}},{a + 1.2:.2f});')
    add(f'tl.fromTo(".fk",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.4,stagger:.1,ease:"back.out(2)"}},{a + 1.4:.2f});')
    add(f'tl.to(".fk0",{{boxShadow:"0 0 0 4px #DAB66A, 0 0 50px rgba(218,182,106,.6)",scale:1.1,duration:.3}},{a + 1.9:.2f});')
    add(f'tl.to(".fk1, .fk2",{{opacity:.3,duration:.3}},{a + 1.9:.2f});')
    ev(a + 1.9, "tick")
    pop(".f2 > .tile:first-child", a + 2.1, "opacity:0,x:-160,scale:.7", .55, "back.out(2)")
    add(f'tl.fromTo(".f2 .farr",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power2.out"}},{a + 2.6:.2f});')
    pop(".bc", a + 2.8, "opacity:0,x:120,scale:.7", .5, "back.out(2)", None)
    add(f'tl.fromTo(".lk",{{opacity:0,y:-60,scale:1.6}},{{opacity:1,y:0,scale:1,duration:.4,ease:"bounce.out"}},{a + 3.3:.2f});')
    ev(a + 3.4, "stamp")
    # 3
    a, z = L[3]
    add(f'tl.fromTo(".stu",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,stagger:.08,ease:"back.out(2)"}},{a + .2:.2f});')
    ev(a + .2, "ping")
    add(f'tl.fromTo(".mold",{{opacity:0,y:-260}},{{opacity:1,y:0,duration:.35,ease:"power3.in"}},{a + 1.5:.2f});')
    ev(a + 1.85, "thud")
    add(f'tl.to(".stu",{{scale:.86,filter:"grayscale(1)",duration:.25}},{a + 1.85:.2f});')
    add(f'tl.to(".stu svg",{{opacity:.35,duration:.25}},{a + 1.85:.2f});')
    # 4
    a, z = L[4]
    pop(".dialw", a + .05, "opacity:0,scale:.5,rotation:-90", .8)
    draw(".dring", a + .05, .9)
    add(f'tl.fromTo(".needle",{{rotation:-150}},{{rotation:-70,duration:1.2,ease:"elastic.out(1,.5)"}},{a + .3:.2f});')
    pop(".sa", a + .5, "opacity:0,x:-120", .5, "back.out(2)", None)
    pop(".sb", a + .7, "opacity:0,x:120", .5, "back.out(2)", None)
    add(f'tl.set(".sb .tile",{{filter:"grayscale(1) brightness(.6)"}},{a:.2f});')
    add(f'tl.fromTo(".sa .xline",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power3.out"}},{a + 3.0:.2f});')
    add(f'tl.to(".sa",{{opacity:.4,duration:.3}},{a + 3.0:.2f});')
    ev(a + 3.0, "swish")
    add(f'tl.to(".needle",{{rotation:70,duration:1.0,ease:"elastic.out(1,.45)"}},{a + 3.3:.2f});')
    add(f'tl.to(".sb .tile",{{filter:"grayscale(0) brightness(1)",boxShadow:"0 0 70px rgba(218,182,106,.7)",scale:1.08,duration:.4}},{a + 3.5:.2f});')
    ev(a + 3.4, "ping")
    add(f'tl.to(".dialw",{{rotation:6,duration:2.5,ease:"sine.inOut"}},{a + 4:.2f});')
    # 5
    a, z = L[5]
    add(f'tl.fromTo("#s5 .intro .logo",{{opacity:0,scale:.3,rotation:-120}},{{opacity:1,scale:1,rotation:0,duration:1.1,ease:"expo.out"}},{a + .05:.2f});')
    ev(a + .05, "reveal")
    add(f'tl.fromTo("#s5 .halo",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:1.4,ease:"expo.out"}},{a + .05:.2f});')
    add(f'tl.fromTo("#s5 .wm",{{opacity:0,y:30,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,y:0,clipPath:"inset(0 0% 0 0)",duration:.9,'
        f'ease:"power3.out"}},{a + .5:.2f});')
    out("#s5 .intro", a + 2.35, "opacity:0,scale:.8,y:-80", .35)
    pop(".ph5", a + 2.8, "opacity:0,x:-160,rotationY:35", .7)
    for k, tk in enumerate((a + 3.2, a + 4.3, a + 5.6, a + 6.6)):
        pop(f".dm{k}", tk, "opacity:0,scale:.4,rotation:-15", .5, "back.out(2.4)", "ping")
    add(f'tl.to(".dim",{{boxShadow:"0 0 60px rgba(218,182,106,.55)",duration:.5,stagger:.1}},{a + 7.2:.2f});')
    # 6
    a, z = L[6]
    mid = a + 6.4
    add(f'tl.fromTo(".cosmos",{{opacity:0}},{{opacity:1,duration:.8}},{a:.2f});')
    add(f'tl.fromTo(".cs",{{opacity:.15}},{{opacity:1,duration:.6,stagger:{{each:.04,repeat:9,yoyo:true}},ease:"sine.inOut"}},{a:.2f});')
    pop(".orbits", a + .1, "opacity:0,scale:.4", 1.0, "expo.out", "reveal")
    add(f'tl.fromTo(".orb.o1",{{rotation:0}},{{rotation:200,duration:6.6,ease:"none"}},{a:.2f});')
    add(f'tl.fromTo(".orb.o2",{{rotation:180}},{{rotation:20,duration:6.6,ease:"none"}},{a:.2f});')
    add(f'tl.fromTo(".orb.o1 .och",{{rotation:0}},{{rotation:-200,duration:6.6,ease:"none"}},{a:.2f});')
    add(f'tl.fromTo(".orb.o2 .och",{{rotation:-180}},{{rotation:-20,duration:6.6,ease:"none"}},{a:.2f});')
    # "optional": a switch that flicks on and off
    pop(".toggle", a + 3.4, "opacity:0,y:40,scale:.8", .5, "back.out(2)")
    add(f'tl.to(".knob",{{x:76,duration:.3,ease:"power3.inOut",yoyo:true,repeat:3,repeatDelay:.45}},{a + 3.9:.2f});')
    add(f'tl.to(".toggle",{{backgroundColor:"#4a3f5e",duration:.3,yoyo:true,repeat:3,repeatDelay:.45}},{a + 3.9:.2f});')
    ev(a + 3.9, "tick")
    out(".orbits, .toggle", mid - .3, "opacity:0,scale:.85", .4)
    pop(".ph6", mid, "opacity:0,y:300,rotationX:30", .8)
    add(f'tl.fromTo(".ph6 .scr img",{{y:0}},{{y:-430,duration:5.6,ease:"sine.inOut"}},{mid + .6:.2f});')
    # 7
    a, z = L[7]
    pop(".ng1", a + .1, "opacity:0,scale:.5,y:-40", .55, "back.out(2)")
    pop(".ng2", a + .4, "opacity:0,scale:.5,y:-40", .55, "back.out(2)", None)
    for k, tk in enumerate((a + 1.4, a + 2.8)):
        add(f'tl.fromTo(".ng{k + 1} .xl",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power3.out"}},{tk:.2f});')
        add(f'tl.to(".ng{k + 1} .tile",{{opacity:.45,duration:.3}},{tk:.2f});')
        ev(tk, "swish")
    # 8
    a, z = L[8]
    pop(".bigger .tile", a + .05, "opacity:0,scale:.4", .5, "back.out(2)")
    add(f'tl.fromTo(".bring",{{scale:.3,opacity:0}},{{scale:1,opacity:1,duration:1.2,ease:"expo.out"}},{a + .9:.2f});')
    add(f'tl.to(".bigger .tile",{{scale:.6,opacity:.5,duration:.6,ease:"power2.inOut"}},{a + .9:.2f});')
    add(f'tl.fromTo(".bcomp",{{opacity:0,rotation:-90,scale:.5}},{{opacity:1,rotation:0,scale:1,duration:.9,ease:"back.out(2)"}},{a + 1.3:.2f});')
    ev(a + .9, "swell")
    # 9
    a, z = L[9]
    for k, (dx, dy) in enumerate([(-300, -40), (300, -40), (0, 260)]):
        add(f'tl.fromTo(".v{k + 1}",{{opacity:0,x:{dx},y:{dy},scale:.6}},{{opacity:1,x:{dx * .55:.0f},y:{dy * .55:.0f},scale:1,'
            f'duration:.7,ease:"expo.out"}},{a + .3 + k * 1.3:.2f});')
        ev(a + .3 + k * 1.3, "ping")
    for k, (fx, fy) in enumerate([(-95, -45), (95, -45), (0, 80)]):
        add(f'tl.to(".v{k + 1}",{{x:{fx},y:{fy},duration:1.2,ease:"expo.inOut"}},{a + 4.6:.2f});')
    ev(a + 4.6, "swell")
    add(f'tl.fromTo(".vcore",{{opacity:0,scale:.3,rotation:-90}},{{opacity:1,scale:1,rotation:0,duration:.7,ease:"back.out(2.4)"}},{a + 5.6:.2f});')
    add(f'tl.to(".vcore",{{scale:1.15,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{a + 6.3:.2f});')
    ev(a + 5.6, "reveal")
    # 10
    a, z = L[10]
    pop(".ph10", a + .05, "opacity:0,y:260,rotationX:25", .8)
    add(f'tl.fromTo(".ph10 .scr img",{{y:0}},{{y:-260,duration:6,ease:"sine.inOut"}},{a + 1.2:.2f});')
    pop(".tick.t1", a + 1.8, "opacity:0,x:-120,scale:.7", .55, "back.out(2)", None)
    pop(".tick.t1 .tk", a + 2.3, "opacity:0,scale:.3", .4, "back.out(3)", "tick")
    pop(".tick.t2", a + 5.0, "opacity:0,x:120,scale:.7", .55, "back.out(2)", None)
    pop(".tick.t2 .tk", a + 5.5, "opacity:0,scale:.3", .4, "back.out(3)", "tick")
    # 11
    a, z = L[11]
    pop(".ph11a", a + .05, "opacity:0,x:-200,rotationY:30", .6)
    pop(".ph11b", a + 1.6, "opacity:0,x:200,rotationY:-30", .6)
    pop(".timer", a + .4, "opacity:0,scale:.5", .6, "back.out(2)", None)
    draw(".tring", a + .5, 1.2, "power2.out")
    ev(a + .5, "count", 1.0)
    # 12
    a, z = L[12]
    pop(".ph12", a + .05, "opacity:0,y:300,rotationX:25", .8)
    add(f'tl.fromTo(".ph12 .scr img",{{y:0}},{{y:-500,duration:3.6,ease:"sine.inOut"}},{a + .8:.2f});')
    out(".ph12", a + 4.4, "opacity:0,scale:.8,y:-80", .4)
    pop(".offer", a + 4.6, "opacity:0,scale:.8,rotationX:30", .7)
    add(f'tl.fromTo(".ostamp",{{opacity:0,scale:2.6,rotation:-18}},{{opacity:1,scale:1,rotation:-6,duration:.45,ease:"back.out(2.4)"}},{a + 5.5:.2f});')
    ev(a + 5.5, "stamp")
    counter(".cnt-price", 0, 2300, a + 7.0, 1.4, "₹")
    add(f'tl.fromTo(".offer .shine",{{xPercent:-160}},{{xPercent:300,duration:.9,ease:"power2.inOut"}},{a + 8.3:.2f});')
    ev(a + 8.4, "glint")
    # 13
    a, z = L[13]
    add(f'tl.fromTo(".die",{{opacity:0,y:-300,rotation:-120}},{{opacity:1,y:0,rotation:(i)=>[-20,15,-10,25][i],duration:.6,stagger:.12,'
        f'ease:"bounce.out"}},{a + .1:.2f});')
    ev(a + .3, "dice")
    add(f'tl.fromTo(".sweep",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power3.out"}},{a + 2.4:.2f});')
    add(f'tl.to(".die",{{opacity:0,x:300,rotation:"+=200",scale:.4,duration:.4,stagger:.05,ease:"power2.in"}},{a + 2.5:.2f});')
    add(f'tl.to(".sweep",{{opacity:0,duration:.3}},{a + 2.8:.2f});')
    ev(a + 2.4, "swish")
    pop(".land", a + 2.9, "opacity:0,scale:.3,y:-60", .55, "back.out(2.6)", "reveal")
    # 14
    a, z = L[14]
    add(f'tl.fromTo(".i14 .logo",{{opacity:0,scale:.3,rotation:120}},{{opacity:1,scale:1,rotation:0,duration:1,ease:"expo.out"}},{a + .05:.2f});')
    add(f'tl.fromTo(".i14 .halo",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:1.4,ease:"expo.out"}},{a + .05:.2f});')
    ev(a + .05, "reveal")
    add(f'tl.fromTo(".i14 .wm",{{opacity:0,y:30,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,y:0,clipPath:"inset(0 0% 0 0)",duration:.8,'
        f'ease:"power3.out"}},{a + .4:.2f});')
    # 15
    a = L[15][0]
    add(f'tl.fromTo(".ctav",{{opacity:0}},{{opacity:1,duration:.6}},{a:.2f});')
    add(f'tl.to("#spkw",{{opacity:.3,duration:.8}},{a + 2.4:.2f});')
    pop(".cta .logo", a + .1, "opacity:0,scale:.4", .7)
    pop(".ctab", a + .5, "opacity:0,scale:.7,y:40", .7, "back.out(1.8)", "reveal")
    add(f'tl.fromTo(".ctab",{{boxShadow:"0 0 0px rgba(218,182,106,0)"}},{{boxShadow:"0 0 90px rgba(218,182,106,.75)",duration:.9,'
        f'yoyo:true,repeat:5,ease:"sine.inOut"}},{a + 1.2:.2f});')
    add(f'tl.fromTo(".ctaf",{{opacity:0,scale:2.4}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2.4)"}},{a + 2.4:.2f});')
    ev(a + 2.4, "stamp")


def backdrop():
    r = random.Random(3)
    dust = "".join(f'<i class="du du{i}" style="left:{r.uniform(0, 1080):.0f}px;top:{r.uniform(0, 1920):.0f}px;'
                   f'width:{r.choice([3, 4, 5, 7])}px;height:{r.choice([3, 4, 5, 7])}px"></i>' for i in range(46))
    sparks = "".join(f'<div class="sp4" style="left:{x}px;top:{y}px">{star4(s, c)}</div>'
                     for x, y, s, c in [(120, 330, 26, RED), (930, 420, 20, GOLD), (80, 1180, 18, GOLD), (980, 1290, 24, RED)])
    return (f'<div id="bgbase"></div><div id="rose">{compass_rose(1500)}</div><div id="dust">{dust}</div>{sparks}'
            f'<div id="vig"></div>')


def backdrop_tl():
    add(f'tl.fromTo("#rose",{{rotation:0}},{{rotation:40,duration:{DUR},ease:"none"}},0);')
    add(f'document.querySelectorAll(".du").forEach((e,i)=>tl.fromTo(e,{{y:0,opacity:0}},{{y:-260-(i%5)*60,opacity:.9,duration:6,'
        f'ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 6)}}},(i%9)*.7));')
    add(f'tl.fromTo(".sp4",{{scale:.6,rotation:0}},{{scale:1.15,rotation:45,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 2.4)},stagger:.6}},0);')
    add(f'tl.fromTo("#halo",{{scale:.95,opacity:.8}},{{scale:1.06,opacity:1,duration:3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 3)}}},0);')


CSS = """
@font-face { font-family: "Fraunces"; font-weight: 100 900; src: url("assets/fonts/fraunces.ttf"); }
@font-face { font-family: "Fraunces"; font-style: italic; font-weight: 100 900; src: url("assets/fonts/fraunces-italic.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 100 800; src: url("assets/fonts/jbmono.ttf"); }
:root { --bg: #15110E; --panel: #211C18; --card: #2E2717; --card2: #38301D; --border: #615230; --gold: #DAB66A; --cream: #F2EADD;
  --sage: #839172; --plum: #261F2F; --lav: #B7A8E0; --muted: #A89F8E; }
* { margin: 0; padding: 0; box-sizing: border-box; }
i, em { font-style: normal; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }
body { font-family: "Manrope", sans-serif; color: var(--cream); }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }
.clip { position: absolute; inset: 0; }
.mono { font: 600 26px "JBMono"; letter-spacing: 7px; color: var(--muted); }
.mono.gold { color: var(--gold); }
.mono.lav { color: var(--lav); }
/* backdrop: the app's dark world, a gold halo, the logo's compass rose turning slowly, gold dust */
#bgbase { position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 42%, #33291a 0%, #1d1812 48%, #15110E 85%); }
#rose { position: absolute; left: -210px; top: 10px; width: 1500px; height: 1500px; opacity: .1; }
#dust { position: absolute; inset: 0; }
.du { position: absolute; border-radius: 50%; background: var(--gold); box-shadow: 0 0 10px rgba(218,182,106,.8); opacity: 0; }
.sp4 { position: absolute; opacity: .7; }
#vig { position: absolute; inset: 0; background: radial-gradient(120% 80% at 50% 45%, rgba(0,0,0,0) 55%, rgba(5,4,3,.65) 100%); }
/* the speaker */
#spkw { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
#halo { position: absolute; left: 240px; top: 300px; width: 600px; height: 600px; border-radius: 50%;
  background: radial-gradient(circle, rgba(218,182,106,.42) 0%, rgba(218,182,106,.12) 45%, rgba(218,182,106,0) 70%); }
#talk { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
/* the bottom panel of a split: a slightly lifted warm backdrop under her, a gold seam on top */
#spkcrop { position: absolute; inset: 0; }
#panelbg { position: absolute; left: 0; top: 960px; width: 1080px; height: 960px;
  background: radial-gradient(80% 70% at 50% 45%, #3a2f1c 0%, #221c15 55%, #17130f 100%); }
.seam { position: absolute; left: 0; top: 957px; width: 1080px; height: 6px; z-index: 4;
  background: linear-gradient(90deg, rgba(218,182,106,0), #DAB66A 20%, #fff1c4 50%, #DAB66A 80%, rgba(218,182,106,0));
  box-shadow: 0 0 30px rgba(218,182,106,.7); }
/* layer order: backdrop < things behind her < speaker < visuals < captions */
#bg { z-index: 0; }
.behind { z-index: 1; }
#spk { z-index: 2; }
.scene { z-index: 3; }
.coins { position: absolute; inset: 0; }
.cn { position: absolute; top: 0; opacity: 0; }
.coin { border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: "Manrope"; font-weight: 800; color: #6b521d;
  background: radial-gradient(circle at 35% 30%, #fff1c4, #DAB66A 45%, #9a7a32 100%); box-shadow: 0 10px 30px rgba(0,0,0,.4), inset 0 0 0 4px rgba(255,240,200,.4); }
/* app-style icon tile */
.tile { position: relative; display: flex; align-items: center; justify-content: center; border-radius: 30%;
  background: linear-gradient(160deg, var(--card2), var(--card) 60%, #241e14); border: 2px solid var(--border);
  box-shadow: 0 24px 60px rgba(0,0,0,.55); }
/* 0 */
.capw { position: absolute; left: 445px; top: 290px; width: 190px; height: 190px; }
.capglow { position: absolute; left: -90px; top: -90px; width: 370px; height: 370px; border-radius: 50%; z-index: -1;
  background: radial-gradient(circle, rgba(218,182,106,.5), rgba(218,182,106,0) 65%); }
.cd { position: absolute; left: 65px; top: -10px; opacity: 0; }
/* 1 */
.kid { position: absolute; left: 400px; top: 330px; width: 280px; height: 280px; display: flex; align-items: center; justify-content: center;
  border-radius: 50%; background: radial-gradient(circle, #2c2418, #1a1511); }
.kring { position: absolute; inset: -10px; border-radius: 50%; border: 4px solid var(--gold); box-shadow: 0 0 50px rgba(218,182,106,.4); }
.orbx { position: absolute; top: 400px; }
.ox1 { left: 110px; } .ox2 { left: 820px; }
.qq { position: absolute; right: -18px; top: -26px; font: italic 700 72px "Fraunces"; color: var(--gold); text-shadow: 0 0 20px rgba(0,0,0,.8); }
.hglass { position: absolute; left: 492px; top: 640px; }
/* 2 */
.flow { position: absolute; left: 0; width: 1080px; display: flex; align-items: center; justify-content: center; gap: 40px; }
.f1 { top: 420px; } .f2 { top: 900px; }
.rep { position: relative; }
.grade { position: absolute; left: 110px; top: -34px; font: 800 52px "Manrope"; color: #1d1812; background: var(--gold); padding: 4px 18px; border-radius: 14px; z-index: 2; }
.farr { display: block; width: 110px; height: 8px; border-radius: 4px; background: var(--gold); transform-origin: 0 50%; position: relative; }
.farr::after { content: ""; position: absolute; right: -14px; top: -11px; border: 15px solid transparent; border-left-color: var(--gold); }
.fork { display: flex; flex-direction: column; gap: 22px; }
.lk { position: absolute; left: 790px; top: -40px; }
/* 3 */
.studs { position: absolute; left: 0; width: 1080px; top: 330px; display: flex; justify-content: center; gap: 40px; }
.stu { width: 130px; height: 130px; border-radius: 34px; background: rgba(33,28,24,.9); border: 2px solid var(--border); display: flex;
  align-items: center; justify-content: center; }
.mold { position: absolute; left: 150px; top: 300px; width: 780px; height: 190px; border-radius: 40px; border: 6px solid var(--gold);
  box-shadow: 0 0 40px rgba(218,182,106,.45); }
/* 4 */
.dialw { position: absolute; left: 340px; top: 290px; width: 400px; height: 400px; filter: drop-shadow(0 0 40px rgba(218,182,106,.35)); }
.side4 { position: absolute; top: 420px; }
.sa { left: 110px; } .sb { left: 820px; }
.xline { position: absolute; left: -10px; top: 70px; width: 170px; height: 8px; background: #E07A6A; transform: rotate(-35deg); transform-origin: 0 50%;
  border-radius: 4px; }
.sa .xline { transform-origin: 0 50%; }
/* 5 */
.intro { position: absolute; left: 0; width: 1080px; top: 460px; text-align: center; z-index: 6; }
.intro .logo { position: relative; width: 340px; height: auto; z-index: 2; }
.intro .wm { position: relative; z-index: 2; margin-top: 10px; font: italic 600 124px/1.05 "Fraunces"; color: var(--gold); letter-spacing: -2px;
  text-shadow: 0 0 50px rgba(218,182,106,.35); }
.intro .halo { position: absolute; left: 190px; top: -150px; width: 700px; height: 700px; border-radius: 50%; z-index: 1;
  background: radial-gradient(circle, rgba(218,182,106,.38), rgba(218,182,106,0) 65%); }
.phone { position: absolute; border-radius: 40px; padding: 9px; background: #0b0907; box-shadow: 0 0 0 2px #3a3126, 0 40px 90px rgba(0,0,0,.6),
  0 0 70px rgba(218,182,106,.18); overflow: hidden; }
.scr { position: relative; width: 100%; height: 100%; border-radius: 32px; overflow: hidden; background: var(--bg); }
.scr img { width: 100%; display: block; }
.pglare { position: absolute; inset: 0; border-radius: 40px; background: linear-gradient(125deg, rgba(255,255,255,.10), rgba(255,255,255,0) 40%); }
.ph5 { left: 110px; top: 290px; }
.dims { position: absolute; left: 430px; top: 300px; width: 540px; display: grid; grid-template-columns: 170px 170px; gap: 40px 60px;
  justify-content: center; }
/* 6 */
.cosmos { position: absolute; inset: 0; }
.cs { position: absolute; border-radius: 50%; background: #fff6d8; box-shadow: 0 0 8px #fff; }
.orbits { position: absolute; left: 540px; top: 740px; width: 0; height: 0; }
.orb { position: absolute; border-radius: 50%; border: 2px dashed rgba(218,182,106,.5); }
.orb.o1 { left: -250px; top: -250px; width: 500px; height: 500px; }
.orb.o2 { left: -380px; top: -380px; width: 760px; height: 760px; border-color: rgba(183,168,224,.45); }
.och { position: absolute; left: 50%; top: -60px; margin-left: -60px; width: 120px; height: 120px; border-radius: 34px; display: flex;
  align-items: center; justify-content: center; background: var(--card); border: 2px solid var(--border); box-shadow: 0 0 40px rgba(218,182,106,.3); }
.och.lv { background: var(--plum); border-color: #4a3f5e; box-shadow: 0 0 40px rgba(183,168,224,.3); }
.gem { position: absolute; left: -90px; top: -90px; width: 180px; height: 180px; border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #8fb0ff, #1e3a8a 55%, #0b1638); box-shadow: 0 0 0 10px rgba(218,182,106,.6), 0 0 90px rgba(80,120,255,.55); }
.toggle { position: absolute; left: 460px; top: 1190px; width: 160px; height: 84px; border-radius: 42px; background: #2a2333; border: 2px solid #4a3f5e; }
.knob { position: absolute; left: 6px; top: 6px; width: 68px; height: 68px; border-radius: 50%; background: var(--lav); box-shadow: 0 0 24px rgba(183,168,224,.8); }
.ph6 { left: 320px; top: 270px; }
/* 7 */
.nog { position: absolute; top: 290px; }
.ng1 { left: 290px; } .ng2 { left: 620px; }
.xl { position: absolute; left: -20px; top: 80px; width: 210px; height: 9px; border-radius: 5px; background: #E07A6A; transform: rotate(-40deg);
  transform-origin: 0 50%; box-shadow: 0 0 20px rgba(224,122,106,.6); }
.ng1 .xl, .ng2 .xl { transform-origin: 0 50%; }
/* 8 */
.bigger { position: absolute; left: 465px; top: 300px; width: 150px; height: 150px; }
.bring { position: absolute; left: -80px; top: -80px; width: 310px; height: 310px; border-radius: 50%; border: 4px solid var(--gold);
  box-shadow: 0 0 60px rgba(218,182,106,.5), inset 0 0 40px rgba(218,182,106,.3); }
.bcomp { position: absolute; left: 15px; top: 15px; }
/* 9 */
.venn { position: absolute; left: 540px; top: 520px; width: 0; height: 0; }
.vc { position: absolute; left: -170px; top: -170px; width: 340px; height: 340px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; mix-blend-mode: screen; }
.v1 { background: radial-gradient(circle, rgba(131,145,114,.65), rgba(131,145,114,.25)); border: 3px solid var(--sage); justify-content: flex-start; padding-left: 50px; align-items: flex-start; padding-top: 90px; }
.v2 { background: radial-gradient(circle, rgba(218,182,106,.6), rgba(218,182,106,.22)); border: 3px solid var(--gold); justify-content: flex-end; padding-right: 50px; align-items: flex-start; padding-top: 90px; }
.v3 { background: radial-gradient(circle, rgba(183,168,224,.55), rgba(183,168,224,.2)); border: 3px solid var(--lav); align-items: flex-end; padding-bottom: 50px; }
.vcore { position: absolute; left: -55px; top: -45px; filter: drop-shadow(0 0 30px rgba(255,230,160,.95)); }
/* 10 */
.ph10 { left: 325px; top: 250px; }
.tick { position: absolute; }
.tick.t1 { left: 60px; top: 560px; } .tick.t2 { left: 890px; top: 900px; }
.tk { position: absolute; right: -16px; bottom: -16px; background: var(--bg); border-radius: 50%; }
/* 11 */
.ph11a { left: 90px; top: 290px; transform: rotate(-4deg); }
.ph11b { left: 760px; top: 300px; transform: rotate(4deg); }
.timer { position: absolute; left: 415px; top: 400px; width: 250px; height: 250px; }
.timer svg { position: absolute; inset: 0; }
.tnum { position: absolute; left: 0; width: 250px; top: 82px; text-align: center; font: 700 76px "Manrope"; }
/* 12 */
.ph12 { left: 330px; top: 260px; }
.offer { position: absolute; left: 140px; top: 330px; width: 800px; height: 760px; border-radius: 40px; text-align: center; overflow: hidden;
  background: linear-gradient(160deg, var(--card2), var(--card) 60%, #241e14); border: 2px solid var(--border); box-shadow: 0 30px 80px rgba(0,0,0,.55); }
.ologo { width: 150px; margin-top: 50px; }
.ostamp { display: block; width: 560px; margin: 40px auto 0; font: 800 120px/1 "Manrope"; color: #1d1812; background: var(--gold); padding: 18px 0;
  border-radius: 26px; box-shadow: 0 0 60px rgba(218,182,106,.5); }
.oprice { margin-top: 70px; font: italic 700 190px/1 "Fraunces"; color: var(--cream); }
.shine { position: absolute; top: -20%; left: 0; width: 30%; height: 140%; transform: rotate(18deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,240,200,.28), rgba(255,255,255,0)); }
/* 13 */
.die { position: absolute; top: 330px; }
.dc0 { left: 170px; } .dc1 { left: 390px; top: 360px; } .dc2 { left: 600px; } .dc3 { left: 810px; top: 350px; }
.sweep { position: absolute; left: 100px; top: 380px; width: 880px; height: 12px; border-radius: 6px; background: var(--gold); transform-origin: 0 50%;
  box-shadow: 0 0 40px rgba(218,182,106,.8); }
.land { position: absolute; left: 455px; top: 300px; }
/* 14 */
.i14 { top: 300px; }
.i14 .logo { width: 260px; }
.i14 .wm { font-size: 104px; }
.i14 .halo { left: 240px; top: -170px; width: 600px; height: 600px; }
/* 15 */
.ctav { position: absolute; inset: 0; background: radial-gradient(90% 60% at 50% 40%, rgba(21,17,14,.55), rgba(10,8,6,.92)); }
.cta { position: absolute; left: 0; width: 1080px; top: 380px; text-align: center; }
.cta .logo { display: block; margin: 0 auto; width: 260px; height: auto; }
.ctab { display: block; width: max-content; margin: 50px auto 0; padding: 34px 60px; border-radius: 80px; background: var(--gold); color: #1d1812;
  font: 800 62px "Manrope"; letter-spacing: -1px; }
.ctaf { margin-top: 50px; font: italic 700 210px/1 "Fraunces"; color: var(--gold); text-shadow: 0 0 40px rgba(218,182,106,.9), 0 0 120px rgba(218,182,106,.6); }
/* captions */
#caps { z-index: 30; }
.cap { position: absolute; left: 40px; width: 1000px; top: 1400px; text-align: center; opacity: 0; font: 800 56px/1.15 "Manrope"; word-spacing: 4px; }
.cw { display: inline-block; font: 800 56px/1.15 "Manrope"; letter-spacing: -1px; color: var(--cream);
  text-shadow: 0 4px 18px rgba(0,0,0,.85), 0 0 2px rgba(0,0,0,.9); }
.cw.em { font: italic 600 66px/1.1 "Fraunces"; color: var(--gold); }
#flash { position: absolute; inset: 0; background: #fff3d6; opacity: 0; }
"""


# the speaker's grade: Natural Portrait seed (skin-soft 0.6), a touch of contrast and warmth toward the brand gold,
# highlights held, the red top tamed; validated with `hyperframes media-treatment` (build/grade.json is its normalized form)
GRADE = __import__("html").escape(json.dumps(json.load(open(os.path.join(ROOT, "build", "grade.json"))), separators=(",", ":")), quote=True)


def main():
    edlv = json.dumps([[a, b] for a, b in L])
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Sucsess Maperrs 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-allow-overflow>{backdrop()}</div>
      <div id="spk" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2" data-layout-allow-overflow><div id="spkcrop"><div id="panelbg"></div><div id="spkw"><div id="halo"></div>
        <video id="talk" data-color-grading="{GRADE}" src="assets/video/{os.environ.get("SPK_SRC", "talk_fg_clean.webm")}" data-start="0" data-duration="{VO}" data-track-index="2" muted playsinline></video></div></div><div class="seam"></div></div>
      {scenes()}
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{captions_html()}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8"><div id="flash"></div></div>
      <audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{VO}" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // lines on the cut timeline: {edlv}
{TL()}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(sorted(EV), open(os.path.join(ROOT, "build", "sfx_events.json"), "w"))
    print("wrote index.html", len(html) // 1024, "KB,", DUR, "s")


def TL():
    backdrop_tl()
    frame_tl()
    scenes_tl()
    # the flash on the two brand reveals
    for t in (L[5][0], L[14][0]):
        add(f'tl.fromTo("#flash",{{opacity:.5}},{{opacity:0,duration:.5,ease:"power2.out",immediateRender:false}},{t:.2f});')
    captions_tl()
    return "\n".join(T)


if __name__ == "__main__":
    main()
