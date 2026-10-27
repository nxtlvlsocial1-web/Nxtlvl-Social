"""Sucsess Maperrs talking-head ad. 1080x1920, 30 fps, cut by build/edl.py.

python3 -I build/generate.py      (run from the project root, after build/edl.py)

Two modes, cut on the rhythm of the speech. TALK: the real take, full frame, cropped from the top (the bare wall above
her head goes; her face sits high, a slow push-in runs under every beat and each jump cut lands on a punch-in), with app
icon stickers popping in the free corners beside her head. MOTION: a full-screen scene on the app's own dark world. A
transition screen carries every change (iris from her face, a gold-edged wipe, or a push), and scene-to-scene changes
inside a motion run slide across. After the reference reels: a giant faint word drifting behind each scene, a brand label
and progress bar on top, cards, step circles, meters, caution tape, count-ups and coin bursts; the captions show the
active word on a gold pill.

Palette from the app UI: near-black #15110E, gold #DAB66A, cream #F2EADD, sage #839172, plum #261F2F; Fraunces (display,
gold italic accents), Manrope (body), JetBrains Mono (labels). Captions are English translations of the Hinglish speech
(client requirement) and are the only words that echo her. The brand is always spelled Sucsess Maperrs.
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


BURSTS = []      # (x, y, t, colour): a ring flashes out from a reveal


def burst(x, y, t, col=GOLD):
    k = len(BURSTS)
    BURSTS.append((x, y, t, col))
    add(f'tl.fromTo(".br{k}",{{scale:.2,opacity:.95}},{{scale:2.6,opacity:0,duration:.8,ease:"power2.out",immediateRender:false}},{t:.2f});')
    add(f'tl.fromTo(".br{k} i",{{scale:0,opacity:1}},{{scale:1.6,opacity:0,duration:.6,ease:"power3.out",immediateRender:false}},{t:.2f});')


def bursts_html():
    return "".join(f'<div class="br br{k}" style="left:{x - 110}px;top:{y - 110}px;border-color:{c}"><i style="background:{c}"></i></div>'
                   for k, (x, y, _, c) in enumerate(BURSTS))


def tap(sel, t):
    """A finger tap on an app screen: ripple + press."""
    ev(t, "click")
    add(f'tl.fromTo("{sel}",{{scale:.3,opacity:.9}},{{scale:2.2,opacity:0,duration:.55,ease:"power2.out",immediateRender:false}},{t:.2f});')


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


def phone(img, cls, w=360, taps=()):
    tp = "".join(f'<i class="tp tp{k}" style="left:{x}%;top:{y}%"></i>' for k, (x, y) in enumerate(taps))
    return (f'<div class="phone {cls}" style="width:{w}px;height:{w * 2576 / 1186:.0f}px"><div class="scr">'
            f'<img src="assets/img/{img}" alt="">{tp}</div><i class="pglare"></i></div>')


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


# ------------------------------------------------------------------ the edit: when she is on screen, when a scene is
# (start, mode). TALK shows her; MOTION opens the stage of full-screen scenes over her through a transition screen.
STAGE = [(0, "talk"), (L[0][0] + 2.2, "motion"), (L[1][0] + .07, "talk"), (L[1][0] + 2.7, "motion"),
         (L[3][0], "talk"), (L[3][0] + 1.6, "motion"), (L[4][0], "talk"), (L[4][0] + 2.7, "motion"),
         (L[6][0], "talk"), (L[6][0] + 2.5, "motion"), (L[6][0] + 7.9, "talk"), (L[6][0] + 9.9, "motion"),
         (L[8][0], "talk"), (L[9][0] + 1.6, "motion"), (L[10][0], "talk"), (L[10][0] + 2.2, "motion"),
         (L[11][0], "talk"), (L[11][0] + 1.4, "motion"), (L[12][0], "talk"), (L[12][0] + 1.6, "motion"),
         (L[14][0] + 2.25, "talk"), (L[15][0], "motion")]
KINDS = ["iris", "wipe", "push"]


def runs(mode):
    out_ = []
    for k, (t, m) in enumerate(STAGE):
        if m == mode:
            out_.append((t, STAGE[k + 1][0] if k + 1 < len(STAGE) else DUR))
    return out_


def mode_at(t):
    return [m for a, m in STAGE if a <= t + 1e-6][-1]


# the take is scaled around her face (source 540, 800) and lifted 100 px: at 1.22 her head top sits near y 310 and her
# chin near 990, and every edge of the frame stays covered for any scale over 1.09
WIDE, CLOSE, PUSH = 1.22, 1.36, .05
TALKSCALE = []   # (start, end, scale at start)


def talk_pieces():
    """Talk runs split at every jump cut inside them; each piece alternates wide / close so a cut lands on a punch-in."""
    k = 0
    for a, b in runs("talk"):
        cuts = [c for c in EDL["cuts"] if a + .3 < c < b - .3]
        edges = [a] + cuts + [b]
        for pa, pb in zip(edges, edges[1:]):
            s = (WIDE, CLOSE)[k % 2]
            k += 1
            TALKSCALE.append((pa, pb, s, pa == a, pb == b))
    return TALKSCALE


def to_motion(t, kind, s_end):
    st = t - .28
    if kind == "iris":
        add(f'tl.fromTo("#stage",{{clipPath:"circle(0% at 50% 40%)",x:0}},{{clipPath:"circle(86% at 50% 40%)",duration:.6,'
            f'ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.fromTo("#iring",{{scale:0,opacity:1}},{{scale:1.34,opacity:1,duration:.6,ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.set("#iring",{{opacity:0}},{st + .6:.2f});')
        add(f'tl.to("#spkw",{{scale:{s_end + .25:.3f},duration:.6,ease:"power3.in"}},{st:.2f});')
    elif kind == "wipe":
        add(f'tl.fromTo("#stage",{{clipPath:"inset(100% 0% 0% 0%)",x:0}},{{clipPath:"inset(0% 0% 0% 0%)",duration:.6,'
            f'ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.fromTo("#wbar",{{y:1940,opacity:1}},{{y:-40,opacity:1,duration:.6,ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.set("#wbar",{{opacity:0}},{st + .6:.2f});')
    else:
        add(f'tl.set("#stage",{{clipPath:"inset(0% 0% 0% 0%)"}},{st:.2f});')
        add(f'tl.fromTo("#stage",{{x:1080}},{{x:0,duration:.6,ease:"expo.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.fromTo("#spk",{{x:0}},{{x:-380,duration:.6,ease:"expo.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.fromTo("#pedge",{{x:1080,opacity:1}},{{x:0,opacity:1,duration:.6,ease:"expo.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.set("#pedge",{{opacity:0}},{st + .6:.2f});')
    add(f'tl.fromTo("#sweepfx",{{xPercent:-120,opacity:1}},{{xPercent:120,opacity:1,duration:.7,ease:"power2.inOut",immediateRender:false}},{st:.2f});')
    ev(st, "whoosh")
    ev(t, "sweep")


def to_talk(t, kind):
    st = t - .28
    if kind == "iris":
        add(f'tl.set("#spk",{{x:0}},{st:.2f});')
        add(f'tl.fromTo("#stage",{{clipPath:"circle(86% at 50% 40%)",x:0}},{{clipPath:"circle(0% at 50% 40%)",duration:.6,'
            f'ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.fromTo("#iring",{{scale:1.34,opacity:1}},{{scale:0,opacity:1,duration:.6,ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.set("#iring",{{opacity:0}},{st + .6:.2f});')
    elif kind == "wipe":
        add(f'tl.set("#spk",{{x:0}},{st:.2f});')
        add(f'tl.fromTo("#stage",{{clipPath:"inset(0% 0% 0% 0%)",x:0}},{{clipPath:"inset(0% 0% 100% 0%)",duration:.6,'
            f'ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.fromTo("#wbar",{{y:1940,opacity:1}},{{y:-40,opacity:1,duration:.6,ease:"power3.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.set("#wbar",{{opacity:0}},{st + .6:.2f});')
    else:
        add(f'tl.fromTo("#stage",{{x:0}},{{x:-1080,duration:.6,ease:"expo.inOut",immediateRender:false}},{st:.2f});')
        add(f'tl.fromTo("#spk",{{x:380}},{{x:0,duration:.6,ease:"expo.inOut",immediateRender:false}},{st:.2f});')
    ev(st, "swish")


def frame_tl():
    add(f'tl.set("#stage",{{clipPath:"inset(0% 0% 100% 0%)",x:0}},0);tl.set("#spk",{{x:0}},0);')
    add(f'tl.set("#spkw",{{scale:{WIDE},x:0,y:-100}},0);')
    ends = {}
    for pa, pb, s, first, last in talk_pieces():
        a0 = max(0, pa - (.3 if first else 0))
        b0 = pb + (.3 if last else 0)
        add(f'tl.fromTo("#spkw",{{scale:{s}}},{{scale:{s + PUSH:.3f},duration:{b0 - a0:.2f},ease:"none",immediateRender:false}},{a0:.2f});')
        if not first:
            ev(pa, "punch")
        ends[round(pb, 3)] = s + PUSH
    m = 0
    for k, (t, mode) in enumerate(STAGE[1:], 1):
        if mode == "motion":
            to_motion(t, KINDS[m % 3], ends.get(round(t, 3), WIDE))
        else:
            to_talk(t, KINDS[m % 3])
            m += 1


# ------------------------------------------------------------------ captions (the only words on screen that echo her)
EMPH = {"lakhs", "strengths", "interests", "marks.", "family", "one", "direction", "Sucsess", "Maperrs.", "personality,",
        "aptitude", "optional,", "reflective", "not", "guaranteed", "alignment", "informed", "satisfaction.", "2-minute",
        "90%", "2,300.", "guesswork.", "yourself,", "future.", "free."}
CAPTOP = 1330


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
        ws = "".join(f'<span class="cw w{j}{" em" if w in EMPH else ""}">{w}</span> ' for j, w in enumerate(c))
        h.append(f'<div class="cap cap{k}" style="top:{CAPTOP}px">{ws}</div>')
    return "".join(h)


def captions_tl():
    for k, (a, z, c) in enumerate(caption_plan()):
        add(f'tl.fromTo(".cap{k} .cw",{{opacity:0,y:26,scale:.9}},{{opacity:1,y:0,scale:1,duration:.32,stagger:.05,ease:"back.out(2.2)",'
            f'immediateRender:false}},{a:.2f});')
        add(f'tl.set(".cap{k}",{{opacity:1}},{a:.2f});tl.set(".cap{k}",{{opacity:0}},{z:.2f});')
        # the active word rides a gold pill, word by word through the chunk
        wts = [len(w) + 2 for w in c]
        t = a
        for j, (w, wt) in enumerate(zip(c, wts)):
            d = (z - a) * wt / sum(wts)
            col = GOLD if w in EMPH else CREAM
            add(f'tl.set(".cap{k} .w{j}",{{backgroundColor:"{GOLD}",color:"#1d1812"}},{t:.2f});'
                f'tl.set(".cap{k} .w{j}",{{backgroundColor:"rgba(218,182,106,0)",color:"{col}"}},{t + d:.2f});')
            t += d


# ------------------------------------------------------------------ stickers: app icons beside her head while she talks
STK = []


def sticker(a, z, name, side, col=GOLD, extra=""):
    k = len(STK)
    x = 70 if side == "l" else 840
    STK.append(clip(f"st{k}", a, z, f'<div class="stk" style="left:{x}px;top:250px">{tile(name, 170, col)}{extra}</div>', track=4, cls="ov"))
    pop(f"#st{k} .stk", a + .12, f"opacity:0,scale:.3,rotation:{-25 if side == 'l' else 25}", .55, "back.out(2.4)")
    add(f'tl.fromTo("#st{k} .stk .tile",{{y:0}},{{y:-16,duration:.9,ease:"sine.inOut",yoyo:true,repeat:{max(1, int((z - a) / .9))}}},{a + .7:.2f});')
    out(f"#st{k} .stk", z - .32, "opacity:0,scale:.6", .25)
    return f"#st{k}"


def stickers():
    r = random.Random(5)
    coins = "".join(f'<div class="cn cn{i}" style="left:{r.uniform(20, 960):.0f}px">{coin(r.choice([70, 90, 120]))}</div>' for i in range(16))
    STK.append(clip("ov0", 0, L[0][0] + 2.5, f'<div class="coins">{coins}</div>', track=4, cls="ov"))
    add('document.querySelectorAll("#ov0 .cn").forEach((e,i)=>{tl.fromTo(e,{y:-260,rotation:-30,opacity:1},{y:2100,rotation:200,opacity:1,'
        'duration:1.9,ease:"power1.in",immediateRender:false},.05+i*.11);});')
    ev(0, "boom")
    ev(.15, "coins")
    t = runs("talk")
    hid = sticker(t[1][0], t[1][1], "hour", "r")
    add(f'tl.fromTo("{hid} svg",{{rotation:0}},{{rotation:180,duration:.6,ease:"power3.inOut",repeat:2,repeatDelay:.5}},{t[1][0] + .6:.2f});')
    sticker(t[2][0], t[2][1], "calc", "l", CREAM, '<b class="qq">?</b>')
    sticker(t[3][0], t[3][1], "badge", "l", MUTED)
    sticker(t[3][0] + 1.3, t[3][1], "route", "r")
    sticker(t[4][0], t[4][1], "numbers", "l")
    sticker(t[4][0] + .9, t[4][1], "moon", "r", LAV)
    sticker(t[5][0], t[5][1], "compass", "r")
    sticker(t[6][0], t[6][1], "briefcase", "l")
    sticker(L[9][0] + .1, t[6][1], "route", "r")
    sticker(t[7][0], t[7][1], "brain", "r", SAGE)
    sticker(t[8][0], t[8][1], "hour", "r")
    sticker(t[9][0], t[9][1], "report", "l")
    sticker(t[10][0], t[10][1], "compass", "l")
    return "".join(STK)


# ------------------------------------------------------------------ scenes: full screen, visuals only
def ghost(word):
    return f'<div class="ghost">{word}</div>'


SC = {}          # scene id -> (start, end) of the stretch it is on screen


def scene(sid, a, z, inner, word=None):
    SC[sid] = (a, z, bool(word))
    return clip(sid, a - .35, z + .35, f'<div class="sw">{ghost(word) if word else ""}{inner}</div>')


def swap(prev, nxt, t):
    """Scene to scene inside a motion run: the old one slides out left, the new one in from the right."""
    add(f'tl.to("#{prev} .sw",{{x:-260,opacity:0,duration:.3,ease:"power2.in"}},{t - .3:.2f});')
    add(f'tl.fromTo("#{nxt} .sw",{{x:260,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"expo.out"}},{t - .05:.2f});')
    add(f'tl.fromTo("#sweepfx",{{xPercent:-120,opacity:1}},{{xPercent:120,opacity:1,duration:.7,ease:"power2.inOut",immediateRender:false}},{t - .3:.2f});')
    ev(t - .3, "whoosh")


def M(i):
    """The i-th motion run (start, end)."""
    return runs("motion")[i]


def scenes():
    r = random.Random(7)
    h = []
    # 0 — lakhs invested in education: coins drop into a graduation cap and stack up
    a, z = M(0)
    drops = "".join(f'<div class="cd cd{i}">{coin(70)}</div>' for i in range(5))
    stacks = "".join(f'<div class="stkc sc{i}"><i></i></div>' for i in range(3))
    h.append(scene("s0", a, z, f'<div class="capw">{tile("cap", 280)}<div class="capglow"></div>{drops}</div><div class="stacks">{stacks}</div>', "LAKHS"))
    # 1 — have you discovered their strengths and interests? a child linked to two dim orbs that light up
    a, z = M(1)
    h.append(scene("s1", a, L[2][0], (
        '<svg class="links" viewBox="0 0 1080 1920" width="1080" height="1920"><path class="cl" d="M480 560 C360 700 260 760 225 905" '
        f'fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" pathLength="1"/><path class="cl" d="M600 560 C720 700 820 760 855 905" '
        f'fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" pathLength="1"/></svg>'
        f'<div class="kid"><div class="kring"></div>{icon("user", 200, CREAM, 2.4)}</div>'
        f'<div class="orbx ox1">{tile("target", 190, GOLD)}<b class="qq">?</b></div>'
        f'<div class="orbx ox2">{tile("heart", 190, GOLD)}<b class="qq">?</b></div>'
        f'<div class="hglass">{icon("hour", 110, MUTED)}</div>'), "STRENGTHS"))
    # 2 — marks pick the stream, family picks the career: two numbered cards
    a = L[2][0]
    h.append(scene("s2", a, M(1)[1], (
        f'<div class="card2 ca"><b class="num">1</b><div class="rep">{tile("report", 170)}<div class="grade">92%</div></div><i class="farr"></i>'
        f'<div class="fork">{tile("flask", 100, CREAM, "fk fk0")}{tile("calc", 100, CREAM, "fk fk1")}{tile("palette", 100, CREAM, "fk fk2")}</div></div>'
        f'<div class="card2 cb"><b class="num">2</b>{tile("family", 170, GOLD, "fam")}<i class="farr"></i><div class="bcw">{tile("briefcase", 170, CREAM, "bc")}'
        f'<div class="lk">{icon("lock", 80, GOLD)}</div></div></div>'), "MARKS"))
    # 3 — one formula for every student: five different students go into one funnel and come out identical
    a, z = M(2)
    studs = "".join(f'<div class="stu su{i}">{icon("user", 74, c)}</div>' for i, c in enumerate([SAGE, GOLD, LAV, "#E08A6A", "#7FB3C9"]))
    same = "".join(f'<div class="same sm{i}">{icon("user", 60, "#8a8172")}</div>' for i in range(5))
    h.append(scene("s3", a, z, (
        f'<div class="studs">{studs}</div>'
        f'<svg class="funnel" viewBox="0 0 640 400" width="640" height="400"><path d="M20 20 H620 L380 250 V370 H260 V250 Z" fill="rgba(218,182,106,.12)" '
        f'stroke="{GOLD}" stroke-width="6" stroke-linejoin="round"/><path d="M60 60 H580" stroke="{GOLD}" stroke-width="2" opacity=".5"/></svg>'
        f'<div class="sames">{same}</div>'), "FORMULA"))
    # 4 — not a job title, a direction: the compass needle swings from the badge to the path
    a, z = M(3)
    h.append(scene("s4", a, L[5][0], (
        f'<div class="dialw">{compass_dial(580)}</div>'
        f'<div class="side4 sa">{tile("badge", 180, MUTED)}<i class="xline"></i></div>'
        f'<div class="side4 sb">{tile("route", 180, GOLD)}</div>'), "DIRECTION"))
    # 5 — the brand: logo reveal with rays, then the app and its four dimensions as numbered step cards with meters
    a = L[5][0]
    steps = "".join(f'<div class="stp sp{i}"><b class="num">{i + 1}</b>{tile(n, 110, GOLD)}<div class="mtr"><i></i></div></div>'
                    for i, n in enumerate(["user", "heart", "brain", "target"]))
    h.append(scene("s5", a, M(3)[1], (
        '<div class="intro"><div class="rays"></div><div class="halo"></div><img class="logo" src="assets/img/logo.png" alt="">'
        '<div class="wm">Sucsess Maperrs</div></div>' +
        phone("app1.jpg", "ph5", 340, [(50, 78)]) + f'<div class="steps">{steps}</div>'), "MAPERRS"))
    # 6a — numerology and the cosmic life cycle, an optional lens: orbits, and a switch that is optional
    a, z = M(4)
    stars = "".join(f'<i class="cs" style="left:{r.uniform(40, 1040):.0f}px;top:{r.uniform(200, 1500):.0f}px;'
                    f'width:{r.choice([3, 4, 6])}px;height:{r.choice([3, 4, 6])}px"></i>' for _ in range(70))
    h.append(scene("s6", a, z, (
        f'<div class="cosmos">{stars}</div>'
        f'<div class="orbits"><div class="orb o1"><div class="och">{icon("numbers", 92, GOLD)}</div></div>'
        f'<div class="orb o2"><div class="och lv">{icon("moon", 70, LAV)}</div></div><div class="gem"></div></div>'
        '<div class="toggle"><i class="knob"></i></div>'), "COSMIC"))
    # 6b — the Inner Pattern screen, an optional reflective lens
    a, z = M(5)
    sp = "".join(f'<div class="lsp ls{i}" style="left:{x}px;top:{y}px">{star4(s, LAV)}</div>'
                 for i, (x, y, s) in enumerate([(200, 420, 46), (850, 330, 34), (180, 1050, 30), (880, 980, 50)]))
    h.append(scene("s6b", a, L[7][0], (
        '<div class="chip lavc"><span>✦ OPTIONAL · REFLECTIVE</span></div>' + phone("app6.jpg", "ph6", 440) + sp), "PATTERN"))
    # 7 — no prediction, no guarantee: caution tape, a crystal ball and a seal, both struck through
    a = L[7][0]
    tape = "REFLECTIVE PERSPECTIVE · NOT A PREDICTION · " * 4
    h.append(scene("s7", a, M(5)[1], (
        f'<div class="tape tp1"><div class="tin"><div class="ttrack">{tape}</div></div></div><div class="tape tp2"><div class="tin"><div class="ttrack">{tape}</div></div></div>'
        f'<div class="nog ng1">{tile("orb", 220, LAV)}<i class="xl"></i></div>'
        f'<div class="nog ng2">{tile("seal", 220, LAV)}<i class="xl"></i></div>')))
    # 9 — strengths, possibilities and direction come into alignment
    a, z = M(6)
    h.append(scene("s9", a, z, (
        f'<div class="venn"><div class="vc v1">{icon("target", 80, CREAM)}</div><div class="vc v2">{icon("spark", 80, CREAM)}</div>'
        f'<div class="vc v3">{icon("route", 80, CREAM)}</div><div class="vcore">{icon("spark", 130, "#fff6d8")}</div></div>'), "ALIGN"))
    # 10 — informed decisions and real satisfaction: the app's home, two ticks and a satisfaction meter
    a, z = M(7)
    h.append(scene("s10", a, z, (
        phone("app7.jpg", "ph10", 400, [(50, 60)]) +
        f'<div class="tick t1">{tile("brain", 150, SAGE)}<div class="tk">{icon("check", 60, SAGE)}</div></div>'
        f'<div class="tick t2">{tile("smile", 150, SAGE)}<div class="tk">{icon("check", 60, SAGE)}</div></div>'
        '<div class="stars">' + "".join(star4(56, GOLD) for _ in range(5)) + '</div><div class="gauge"><svg viewBox="0 0 440 250" width="440" height="250"><path d="M30 230 A190 190 0 0 1 410 230" fill="none" '
        f'stroke="{CARD2}" stroke-width="26" stroke-linecap="round"/><path class="garc" d="M30 230 A190 190 0 0 1 410 230" fill="none" '
        f'stroke="{SAGE}" stroke-width="26" stroke-linecap="round" pathLength="1"/></svg><i class="gneedle"></i><i class="ghub"></i></div>'), "INFORMED"))
    # 11 — the 2-minute scan: a two-minute timer and two screens
    a, z = M(8)
    h.append(scene("s11", a, z, (
        phone("app2.jpg", "ph11a", 230, [(50, 91)]) + phone("app3.jpg", "ph11b", 230, [(40, 40)]) +
        '<div class="timer"><svg viewBox="0 0 200 200" width="400" height="400"><circle cx="100" cy="100" r="86" fill="none" '
        f'stroke="{CARD2}" stroke-width="12"/><circle class="tring" cx="100" cy="100" r="86" fill="none" stroke="{GOLD}" '
        'stroke-width="12" stroke-linecap="round" pathLength="1" transform="rotate(-90 100 100)"/></svg><div class="tnum">2:00</div></div>'), "2 MIN"))
    # 12a — the full assessment's result screen
    a, z = M(9)
    off = L[12][0] + 4.45
    h.append(scene("s12", a, off, phone("app4.jpg", "ph12", 440) + '<div class="chip"><span>✦ SUCCESS MAP PRO</span></div>', "PRO"))
    # 12b — 90% off, Rs 2,300, with coins bursting out from behind the card
    burstc = "".join(f'<div class="ob ob{i}">{coin(80)}</div>' for i in range(10))
    h.append(scene("s12b", off, L[13][0], (
        f'<div class="obs">{burstc}</div>'
        '<div class="offer"><img class="ologo" src="assets/img/logo.png" alt=""><div class="ostamp">90% OFF</div>'
        '<div class="oprice"><span class="cnt-price">₹0</span></div><i class="shine"></i></div>'), "90%"))
    # 13 — not guesswork: dice tumble in and are swept away, a compass lands
    a = L[13][0]
    dice = "".join(f'<div class="die dc{i}">{icon("dice", 120, GOLD)}</div>' for i in range(4))
    h.append(scene("s13", a, L[14][0], dice + f'<div class="sweep"></div><div class="land">{tile("compass", 240)}</div>', "GUESSWORK"))
    # 14 — the brand, as she says the tagline
    a = L[14][0]
    h.append(scene("s14", a, M(9)[1], (
        '<div class="intro i14"><div class="rays"></div><div class="halo"></div><img class="logo" src="assets/img/logo.png" alt=""><div class="wm">Sucsess Maperrs</div></div>'), "FUTURE"))
    # 15 — the end card carries the last line: a tap on the free scan
    a = M(10)[0]
    SC["s15"] = (a, DUR, True)
    h.append(clip("s15", a - .35, DUR, (
        '<div class="sw">' + ghost("FREE") + '<div class="cta"><div class="halo"></div><img class="logo" src="assets/img/logo.png" alt="">'
        '<div class="ctab"><span>Instant Success Scan</span></div><div class="ctaf">FREE</div></div><i class="cursor"></i></div>')))
    return "".join(h)


def scenes_tl():
    for sid, (a, z, g) in SC.items():
        if g:
            add(f'tl.fromTo("#{sid} .ghost",{{x:140}},{{x:-300,duration:{z - a + .7:.2f},ease:"none",immediateRender:false}},{a - .35:.2f});')
    # 0
    a, z = M(0)
    pop("#s0 .capw .tile", a + .02, "opacity:0,scale:.4,rotation:-20", .6, "back.out(2)")
    burst(540, 470, a + .1)
    add(f'tl.fromTo("#s0 .capglow",{{opacity:0,scale:.5}},{{opacity:1,scale:1.1,duration:.8,ease:"sine.inOut",yoyo:true,repeat:1}},{a:.2f});')
    add(f'document.querySelectorAll("#s0 .cd").forEach((e,i)=>{{tl.fromTo(e,{{x:(i-2)*120,y:-420,opacity:0,scale:.8}},{{x:0,y:40,opacity:1,scale:.5,'
        f'duration:.42,ease:"power2.in",immediateRender:false}},{a + .2:.2f}+i*.22);tl.to(e,{{opacity:0,duration:.06}},{a + .62:.2f}+i*.22);}});')
    add(f'tl.to("#s0 .capw .tile",{{scale:1.08,duration:.11,yoyo:true,repeat:7,ease:"power1.out"}},{a + .6:.2f});')
    ev(a + .3, "coins")
    for k, hgt in enumerate((.42, .7, 1)):
        add(f'tl.fromTo("#s0 .sc{k}",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset({(1 - hgt) * 100:.0f}% 0% 0% 0%)",duration:.7,'
            f'ease:"expo.out"}},{a + .35 + k * .18:.2f});')
        ev(a + .35 + k * .18, "tick")
    # 1
    a, _ = M(1)
    pop("#s1 .kid", a + .05, "opacity:0,scale:.5", .6, "back.out(2)")
    draw("#s1 .kring", a + .1, .5)
    draw("#s1 .cl", a + .35, .6)
    for k, tk in enumerate((a + .5, a + .65)):
        pop(f"#s1 .ox{k + 1}", tk, f"opacity:0,y:120,scale:.6", .6, "back.out(2)", None)
    add(f'tl.set("#s1 .orbx .tile",{{filter:"grayscale(1) brightness(.6)"}},{a - .4:.2f});')
    add(f'tl.fromTo("#s1 .qq",{{scale:.6}},{{scale:1.15,duration:.4,ease:"sine.inOut",yoyo:true,repeat:3}},{a + .9:.2f});')
    for k, tk in enumerate((a + 1.1, a + 2.0)):
        add(f'tl.to("#s1 .ox{k + 1} .tile",{{filter:"grayscale(0) brightness(1)",boxShadow:"0 0 80px rgba(218,182,106,.7)",duration:.4}},{tk:.2f});')
        add(f'tl.to("#s1 .ox{k + 1} .qq",{{opacity:0,scale:.3,duration:.25}},{tk:.2f});')
        ev(tk, "ping")
        burst(225 if k == 0 else 855, 915, tk)
    add(f'tl.fromTo("#s1 .hglass svg",{{rotation:0}},{{rotation:180,duration:.6,ease:"power3.inOut",repeat:2,repeatDelay:.4}},{a + .4:.2f});')
    # 2
    a = L[2][0]
    swap("s1", "s2", a)
    pop("#s2 .ca", a + .0, "opacity:0,x:200", .5, "expo.out", None)
    pop("#s2 .ca .rep .tile", a + .2, "opacity:0,scale:.6", .5, "back.out(2)")
    add(f'tl.fromTo("#s2 .grade",{{opacity:0,scale:2.6,rotation:-16}},{{opacity:1,scale:1,rotation:-8,duration:.4,ease:"back.out(2.6)"}},{a + .7:.2f});')
    ev(a + .7, "stamp")
    add(f'tl.fromTo("#s2 .ca .farr",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power2.out"}},{a + 1.1:.2f});')
    add(f'tl.fromTo("#s2 .fk",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.4,stagger:.1,ease:"back.out(2)"}},{a + 1.3:.2f});')
    add(f'tl.to("#s2 .fk0",{{boxShadow:"0 0 0 4px #DAB66A, 0 0 50px rgba(218,182,106,.6)",scale:1.1,duration:.3}},{a + 1.8:.2f});')
    add(f'tl.to("#s2 .fk1, #s2 .fk2",{{opacity:.3,duration:.3}},{a + 1.8:.2f});')
    ev(a + 1.8, "tick")
    pop("#s2 .cb", a + 1.9, "opacity:0,x:200", .5, "expo.out", "whoosh")
    pop("#s2 .fam", a + 2.1, "opacity:0,scale:.6", .5, "back.out(2)")
    add(f'tl.fromTo("#s2 .cb .farr",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power2.out"}},{a + 2.6:.2f});')
    pop("#s2 .bc", a + 2.8, "opacity:0,x:120,scale:.7", .5, "back.out(2)", None)
    add(f'tl.fromTo("#s2 .lk",{{opacity:0,y:-80,scale:1.6}},{{opacity:1,y:0,scale:1,duration:.4,ease:"bounce.out"}},{a + 3.2:.2f});')
    ev(a + 3.3, "stamp")
    burst(830, 1000, a + 3.35, "#E07A6A")
    # 3
    a, z = M(2)
    add(f'tl.fromTo("#s3 .stu",{{opacity:0,y:-80}},{{opacity:1,y:0,duration:.35,stagger:.06,ease:"back.out(2)"}},{a + .02:.2f});')
    ev(a + .05, "ping")
    pop("#s3 .funnel", a + .1, "opacity:0,scale:.7,y:60", .45, "back.out(1.8)", None)
    add(f'tl.to("#s3 .stu",{{x:(i)=>340-170*i,y:300,scale:.35,opacity:0,duration:.45,stagger:.07,ease:"power2.in"}},{a + .55:.2f});')
    ev(a + .6, "swish")
    add(f'tl.fromTo("#s3 .funnel",{{rotation:0}},{{rotation:3,duration:.07,yoyo:true,repeat:5,ease:"sine.inOut"}},{a + 1.0:.2f});')
    ev(a + 1.05, "thud")
    add(f'tl.fromTo("#s3 .same",{{opacity:0,y:-120,scale:.5}},{{opacity:1,y:0,scale:1,duration:.4,stagger:.08,ease:"back.out(2)"}},{a + 1.3:.2f});')
    ev(a + 1.3, "dice")
    burst(540, 1020, a + 1.35, "#E07A6A")
    # 4
    a, _ = M(3)
    pop("#s4 .dialw", a + .02, "opacity:0,scale:.5,rotation:-90", .8, "expo.out")
    draw("#s4 .dring", a + .05, .9)
    add(f'tl.fromTo("#s4 .needle",{{rotation:-150}},{{rotation:-70,duration:1.1,ease:"elastic.out(1,.5)"}},{a + .25:.2f});')
    pop("#s4 .sa", a + .4, "opacity:0,x:-140", .5, "back.out(2)", None)
    pop("#s4 .sb", a + .55, "opacity:0,x:140", .5, "back.out(2)", None)
    add(f'tl.set("#s4 .sb .tile",{{filter:"grayscale(1) brightness(.6)"}},{a - .4:.2f});')
    add(f'tl.fromTo("#s4 .sa .xline",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power3.out"}},{a + 1.3:.2f});')
    add(f'tl.to("#s4 .sa",{{opacity:.4,duration:.3}},{a + 1.3:.2f});')
    ev(a + 1.3, "swish")
    add(f'tl.to("#s4 .needle",{{rotation:70,duration:1.0,ease:"elastic.out(1,.45)"}},{a + 1.6:.2f});')
    add(f'tl.to("#s4 .sb .tile",{{filter:"grayscale(0) brightness(1)",boxShadow:"0 0 70px rgba(218,182,106,.7)",scale:1.08,duration:.4}},{a + 1.8:.2f});')
    ev(a + 1.7, "ping")
    burst(910, 1050, a + 1.8)
    add(f'tl.to("#s4 .dialw",{{rotation:8,duration:2.2,ease:"sine.inOut"}},{a + 2.2:.2f});')
    # 5
    a = L[5][0]
    swap("s4", "s5", a)
    add(f'tl.fromTo("#s5 .intro .logo",{{opacity:0,scale:.3,rotation:-120}},{{opacity:1,scale:1,rotation:0,duration:1.1,ease:"expo.out"}},{a + .05:.2f});')
    ev(a + .05, "reveal")
    ev(a, "boom")
    add(f'tl.fromTo("#s5 .halo",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:1.4,ease:"expo.out"}},{a + .05:.2f});')
    add(f'tl.fromTo("#s5 .rays",{{opacity:0,rotation:0,scale:.6}},{{opacity:1,rotation:60,scale:1,duration:2.4,ease:"power2.out"}},{a + .05:.2f});')
    add(f'tl.fromTo("#s5 .wm",{{opacity:0,y:30,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,y:0,clipPath:"inset(0 0% 0 0)",duration:.9,'
        f'ease:"power3.out"}},{a + .5:.2f});')
    burst(540, 560, a + .15)
    out("#s5 .intro", a + 2.35, "opacity:0,scale:.8,y:-80", .35)
    ev(a + 2.35, "swish")
    pop("#s5 .ph5", a + 2.6, "opacity:0,x:-200,rotationY:35", .7, "expo.out", "whoosh")
    add(f'tl.fromTo("#s5 .ph5 .scr img",{{scale:1}},{{scale:1.1,duration:5.6,ease:"sine.inOut"}},{a + 2.8:.2f});')
    tap("#s5 .ph5 .tp0", a + 3.6)
    for k, tk in enumerate((a + 3.2, a + 4.3, a + 5.6, a + 6.6)):
        pop(f"#s5 .sp{k}", tk, "opacity:0,x:160,scale:.8", .5, "back.out(2)", "ping")
        add(f'tl.fromTo("#s5 .sp{k} .mtr i",{{scaleX:0}},{{scaleX:{[.82, .64, .9, .74][k]},duration:.8,ease:"expo.out"}},{tk + .3:.2f});')
        burst(565, 375 + k * 190, tk + .1)
    add(f'tl.to("#s5 .stp .tile",{{boxShadow:"0 0 50px rgba(218,182,106,.55)",duration:.5,stagger:.1}},{a + 7.2:.2f});')
    # 6a
    a, z = M(4)
    add(f'tl.fromTo("#s6 .cosmos",{{opacity:0}},{{opacity:1,duration:.6}},{a - .3:.2f});')
    add(f'tl.fromTo("#s6 .cs",{{opacity:.15}},{{opacity:1,duration:.6,stagger:{{each:.04,repeat:7,yoyo:true}},ease:"sine.inOut"}},{a - .3:.2f});')
    pop("#s6 .orbits", a + .05, "opacity:0,scale:.4", 1.0, "expo.out", "reveal")
    burst(540, 720, a + .15, LAV)
    for sel, r0, r1 in (("#s6 .orb.o1", 0, 200), ("#s6 .orb.o2", 180, 20), ("#s6 .orb.o1 .och", 0, -200), ("#s6 .orb.o2 .och", -180, -20)):
        add(f'tl.fromTo("{sel}",{{rotation:{r0}}},{{rotation:{r1},duration:{z - a + .7:.2f},ease:"none"}},{a - .35:.2f});')
    pop("#s6 .toggle", a + .7, "opacity:0,y:60,scale:.8", .5, "back.out(2)")
    add(f'tl.to("#s6 .knob",{{x:76,duration:.3,ease:"power3.inOut",yoyo:true,repeat:5,repeatDelay:.45}},{a + 1.2:.2f});')
    add(f'tl.to("#s6 .toggle",{{backgroundColor:"#4a3f5e",duration:.3,yoyo:true,repeat:5,repeatDelay:.45}},{a + 1.2:.2f});')
    for k in range(3):
        ev(a + 1.2 + k * 1.5, "click")
    add(f'tl.fromTo("#s6 .gem",{{scale:1}},{{scale:1.12,duration:.9,ease:"sine.inOut",yoyo:true,repeat:5}},{a:.2f});')
    # 6b
    a, _ = M(5)
    pop("#s6b .ph6", a + .02, "opacity:0,y:300,rotationX:30", .8, "expo.out")
    add(f'tl.fromTo("#s6b .ph6 .scr img",{{scale:1}},{{scale:1.12,duration:{L[7][0] - a + .3:.2f},ease:"sine.inOut"}},{a + .3:.2f});')
    pop("#s6b .chip", a + .5, "opacity:0,y:-30,scale:.8", .45, "back.out(2)", "tick")
    add(f'tl.fromTo("#s6b .lsp",{{scale:0,rotation:0}},{{scale:1,rotation:90,duration:.6,stagger:.15,ease:"back.out(2)"}},{a + .4:.2f});')
    ev(a + .5, "glint")
    # 7
    a = L[7][0]
    swap("s6b", "s7", a)
    add(f'tl.fromTo("#s7 .tp1 .tin",{{x:-1600}},{{x:0,duration:.5,ease:"expo.out"}},{a + .05:.2f});')
    add(f'tl.fromTo("#s7 .tp2 .tin",{{x:1600}},{{x:0,duration:.5,ease:"expo.out"}},{a + .2:.2f});')
    ev(a + .05, "stamp")
    ev(a + .2, "stamp")
    add(f'tl.fromTo("#s7 .tp1 .ttrack",{{x:0}},{{x:-900,duration:5,ease:"none"}},{a:.2f});')
    add(f'tl.fromTo("#s7 .tp2 .ttrack",{{x:-900}},{{x:0,duration:5,ease:"none"}},{a:.2f});')
    pop("#s7 .ng1", a + .4, "opacity:0,scale:.5,y:-40", .55, "back.out(2)")
    pop("#s7 .ng2", a + .6, "opacity:0,scale:.5,y:-40", .55, "back.out(2)", None)
    for k, tk in enumerate((a + 1.4, a + 2.8)):
        add(f'tl.fromTo("#s7 .ng{k + 1} .xl",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power3.out"}},{tk:.2f});')
        add(f'tl.to("#s7 .ng{k + 1} .tile",{{opacity:.45,duration:.3}},{tk:.2f});')
        ev(tk, "swish")
        burst(360 if k == 0 else 720, 760, tk + .1, "#E07A6A")
    # 9
    a, z = M(6)
    for k, (dx, dy) in enumerate([(-320, -60), (320, -60), (0, 300)]):
        add(f'tl.fromTo("#s9 .v{k + 1}",{{opacity:0,x:{dx},y:{dy},scale:.6}},{{opacity:1,x:{dx * .55:.0f},y:{dy * .55:.0f},scale:1,'
            f'duration:.7,ease:"expo.out"}},{a + .1 + k * .9:.2f});')
        ev(a + .1 + k * .9, "ping")
    for k, (fx, fy) in enumerate([(-110, -55), (110, -55), (0, 95)]):
        add(f'tl.to("#s9 .v{k + 1}",{{x:{fx},y:{fy},duration:1.2,ease:"expo.inOut"}},{a + 3.0:.2f});')
    ev(a + 3.0, "swell")
    add(f'tl.fromTo("#s9 .vcore",{{opacity:0,scale:.3,rotation:-90}},{{opacity:1,scale:1,rotation:0,duration:.7,ease:"back.out(2.4)"}},{a + 4.0:.2f});')
    add(f'tl.to("#s9 .vcore",{{scale:1.15,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{a + 4.7:.2f});')
    ev(a + 4.0, "reveal")
    burst(540, 720, a + 4.05, "#fff1c4")
    # 10
    a, z = M(7)
    pop("#s10 .ph10", a + .02, "opacity:0,y:260,rotationX:25", .8, "expo.out")
    add(f'tl.fromTo("#s10 .ph10 .scr img",{{scale:1}},{{scale:1.1,duration:{z - a:.2f},ease:"sine.inOut"}},{a + .3:.2f});')
    tap("#s10 .ph10 .tp0", a + 4.4)
    pop("#s10 .tick.t1", a + .5, "opacity:0,x:160,scale:.7", .55, "back.out(2)", None)
    pop("#s10 .tick.t1 .tk", a + 1.0, "opacity:0,scale:.3", .4, "back.out(3)", "tick")
    pop("#s10 .gauge", a + 1.6, "opacity:0,y:80", .5, "expo.out", "whoosh")
    add(f'tl.fromTo("#s10 .garc",{{strokeDasharray:"0 1"}},{{strokeDasharray:"0.88 1",duration:1.6,ease:"expo.out"}},{a + 2.0:.2f});')
    add(f'tl.fromTo("#s10 .gneedle",{{rotation:-90}},{{rotation:68,duration:1.6,ease:"expo.out"}},{a + 2.0:.2f});')
    ev(a + 2.0, "count", 1.2)
    pop("#s10 .tick.t2", a + 2.8, "opacity:0,x:160,scale:.7", .55, "back.out(2)", None)
    pop("#s10 .tick.t2 .tk", a + 3.3, "opacity:0,scale:.3", .4, "back.out(3)", "tick")
    burst(875, 385, a + 3.4, SAGE)
    add(f'tl.fromTo("#s10 .stars svg",{{opacity:0,scale:0,rotation:-90}},{{opacity:1,scale:1,rotation:0,duration:.45,stagger:.12,ease:"back.out(2.6)"}},{a + 3.8:.2f});')
    for k in range(5):
        ev(a + 3.8 + k * .12, "pop")
    # 11
    a, z = M(8)
    pop("#s11 .timer", a + .02, "opacity:0,scale:.5", .6, "back.out(2)", "pop")
    draw("#s11 .tring", a + .1, 1.0, "power2.out")
    burst(540, 500, a + .1)
    pop("#s11 .ph11a", a + .3, "opacity:0,x:-220,rotationY:30", .6, "expo.out", None)
    pop("#s11 .ph11b", a + .5, "opacity:0,x:220,rotationY:-30", .6, "expo.out", "whoosh")
    tap("#s11 .ph11a .tp0", a + 1.0)
    tap("#s11 .ph11b .tp0", a + 1.8)
    for k in range(1, 4):
        add(f'tl.set("#s11 .tnum",{{textContent:"1:{60 - k:02d}"}},{a + .4 + k * .6:.2f});')
        ev(a + .4 + k * .6, "clock")
    # 12a
    a, _ = M(9)
    pop("#s12 .ph12", a + .02, "opacity:0,y:300,rotationX:25", .8, "expo.out")
    add(f'tl.fromTo("#s12 .ph12 .scr img",{{scale:1}},{{scale:1.12,duration:3,ease:"sine.inOut"}},{a + .3:.2f});')
    pop("#s12 .chip", a + .5, "opacity:0,y:-30,scale:.8", .45, "back.out(2)", "tick")
    # 12b
    a = SC["s12b"][0]
    swap("s12", "s12b", a)
    add(f'tl.fromTo("#flash",{{opacity:.35}},{{opacity:0,duration:.5,ease:"power2.out",immediateRender:false}},{a:.2f});')
    ev(a, "boom")
    s = a + 1.05                                     # "90% off"
    add(f'tl.fromTo("#s12b .ostamp",{{opacity:0,scale:2.6,rotation:-18}},{{opacity:1,scale:1,rotation:-6,duration:.45,ease:"back.out(2.4)"}},{s:.2f});')
    ev(s, "stamp")
    burst(540, 660, s)
    add(f'document.querySelectorAll("#s12b .ob").forEach((e,i)=>{{const g=i/10*Math.PI*2;tl.fromTo(e,{{x:0,y:0,scale:.3,opacity:0}},'
        f'{{x:Math.cos(g)*520,y:Math.sin(g)*640,scale:1,opacity:1,rotation:220,duration:.9,ease:"expo.out",immediateRender:false}},{s + .05:.2f});'
        f'tl.to(e,{{opacity:0,duration:.3}},{s + .8:.2f});}});')
    ev(s + .05, "coins")
    counter("#s12b .cnt-price", 0, 2300, a + 2.6, 1.4, "₹")
    burst(540, 960, a + 4.0)
    add(f'tl.fromTo("#s12b .offer .shine",{{xPercent:-160}},{{xPercent:300,duration:.9,ease:"power2.inOut"}},{a + 3.9:.2f});')
    ev(a + 4.0, "glint")
    # 13
    a = L[13][0]
    swap("s12b", "s13", a)
    add(f'tl.fromTo("#s13 .die",{{opacity:0,y:-360,rotation:-120}},{{opacity:1,y:0,rotation:(i)=>[-20,15,-10,25][i],duration:.6,stagger:.12,'
        f'ease:"bounce.out"}},{a + .1:.2f});')
    ev(a + .3, "dice")
    add(f'tl.fromTo("#s13 .sweep",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power3.out"}},{a + 2.4:.2f});')
    add(f'tl.to("#s13 .die",{{opacity:0,x:340,rotation:"+=200",scale:.4,duration:.4,stagger:.05,ease:"power2.in"}},{a + 2.5:.2f});')
    add(f'tl.to("#s13 .sweep",{{opacity:0,duration:.3}},{a + 2.8:.2f});')
    ev(a + 2.4, "swish")
    pop("#s13 .land", a + 2.9, "opacity:0,scale:.3,y:-60", .55, "back.out(2.6)", "reveal")
    burst(540, 620, a + 3.0)
    # 14
    a = L[14][0]
    swap("s13", "s14", a)
    add(f'tl.fromTo("#s14 .logo",{{opacity:0,scale:.3,rotation:120}},{{opacity:1,scale:1,rotation:0,duration:1,ease:"expo.out"}},{a + .05:.2f});')
    add(f'tl.fromTo("#s14 .halo",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:1.4,ease:"expo.out"}},{a + .05:.2f});')
    add(f'tl.fromTo("#s14 .rays",{{opacity:0,rotation:0,scale:.6}},{{opacity:1,rotation:-60,scale:1,duration:2.4,ease:"power2.out"}},{a + .05:.2f});')
    ev(a + .05, "reveal")
    burst(540, 560, a + .15)
    add(f'tl.fromTo("#s14 .wm",{{opacity:0,y:30,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,y:0,clipPath:"inset(0 0% 0 0)",duration:.8,'
        f'ease:"power3.out"}},{a + .4:.2f});')
    # 15
    a = SC["s15"][0]
    pop("#s15 .cta .logo", a + .05, "opacity:0,scale:.4", .7, "expo.out")
    add(f'tl.fromTo("#s15 .halo",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:1.2,ease:"expo.out"}},{a:.2f});')
    pop("#s15 .ctab", a + .45, "opacity:0,scale:.7,y:40", .7, "back.out(1.8)", "reveal")
    add(f'tl.fromTo("#s15 .ctab",{{boxShadow:"0 0 0px rgba(218,182,106,0)"}},{{boxShadow:"0 0 90px rgba(218,182,106,.75)",duration:.9,'
        f'yoyo:true,repeat:5,ease:"sine.inOut"}},{a + 1.2:.2f});')
    # a finger taps the button
    add(f'tl.fromTo("#s15 .cursor",{{x:300,y:420,opacity:0}},{{x:0,y:0,opacity:1,duration:.7,ease:"expo.out"}},{a + 1.1:.2f});')
    add(f'tl.to("#s15 .cursor",{{scale:.8,duration:.1,yoyo:true,repeat:1}},{a + 1.85:.2f});')
    add(f'tl.to("#s15 .ctab",{{scale:.94,duration:.1,yoyo:true,repeat:1}},{a + 1.85:.2f});')
    ev(a + 1.85, "click")
    burst(540, 745, a + 1.9)
    add(f'tl.fromTo("#s15 .ctaf",{{opacity:0,scale:2.4}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2.4)"}},{a + 2.4:.2f});')
    ev(a + 2.4, "stamp")
    ev(a, "boom")
    burst(540, 970, a + 2.45)
    add(f'tl.fromTo("#flash",{{opacity:.4}},{{opacity:0,duration:.6,ease:"power2.out",immediateRender:false}},{a:.2f});')


def backdrop():
    r = random.Random(3)
    dust = "".join(f'<i class="du du{i}" style="left:{r.uniform(0, 1080):.0f}px;top:{r.uniform(0, 1920):.0f}px;'
                   f'width:{r.choice([3, 4, 5, 7])}px;height:{r.choice([3, 4, 5, 7])}px"></i>' for i in range(46))
    sparks = "".join(f'<div class="sp4" style="left:{x}px;top:{y}px">{star4(s, c)}</div>'
                     for x, y, s, c in [(120, 330, 26, RED), (930, 420, 20, GOLD), (80, 1180, 18, GOLD), (980, 1290, 24, RED)])
    return (f'<div id="bgbase"></div><div id="grid"></div><div class="aur au1"></div><div class="aur au2"></div><div id="rose">{compass_rose(1500)}</div>'
            f'<div id="dust">{dust}</div>{sparks}<div id="vig"></div>')


def backdrop_tl():
    add(f'tl.fromTo("#rose",{{rotation:0}},{{rotation:40,duration:{DUR},ease:"none"}},0);')
    add(f'tl.fromTo("#grid",{{y:0}},{{y:-360,duration:{DUR},ease:"none"}},0);')
    add(f'tl.fromTo(".au1",{{x:-120,y:0}},{{x:160,y:120,duration:9,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 9)}}},0);')
    add(f'tl.fromTo(".au2",{{x:140,y:60}},{{x:-160,y:-80,duration:11,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 11)}}},0);')
    add(f'document.querySelectorAll(".du").forEach((e,i)=>tl.fromTo(e,{{y:0,opacity:0}},{{y:-260-(i%5)*60,opacity:.9,duration:6,'
        f'ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 6)}}},(i%9)*.7));')
    add(f'tl.fromTo(".sp4",{{scale:.6,rotation:0}},{{scale:1.15,rotation:45,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 2.4)},stagger:.6}},0);')
    # the warm light leak over her and the progress bar
    add(f'tl.fromTo("#leak",{{x:-260,opacity:.22}},{{x:260,opacity:.42,duration:7,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 7)}}},0);')
    add(f'tl.fromTo("#hud .pfill",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none"}},0);')
    add(f'tl.fromTo("#hud .dot",{{opacity:1}},{{opacity:.25,duration:.6,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .6)}}},0);')


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
/* layer order: speaker < talk overlays < stage of scenes < transition screens < hud < captions < fx */
#spk { position: absolute; inset: 0; z-index: 1; }
.ov { z-index: 2; }
#stage { position: absolute; inset: 0; z-index: 3; overflow: hidden; }
#trans { position: absolute; inset: 0; z-index: 4; pointer-events: none; }
#hud { z-index: 5; }
#caps { z-index: 6; }
#fx { z-index: 7; }
/* the speaker: the take scaled around her face, the wall above her head cropped off */
#spkw { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 800px; }
#talk { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#leak { position: absolute; left: -200px; top: -380px; width: 1480px; height: 1300px; mix-blend-mode: screen;
  background: radial-gradient(closest-side, rgba(255,186,104,.55), rgba(218,140,70,.18) 55%, rgba(218,140,70,0)); }
.shade { position: absolute; left: 0; width: 1080px; }
.shade.top { top: 0; height: 420px; background: linear-gradient(rgba(10,8,6,.55), rgba(10,8,6,0)); }
.shade.bot { bottom: 0; height: 760px; background: linear-gradient(rgba(10,8,6,0), rgba(10,8,6,.62)); }
.stk { position: absolute; }
.stk .qq { position: absolute; right: -18px; top: -30px; }
.coins { position: absolute; inset: 0; }
.cn { position: absolute; top: 0; opacity: 0; }
/* transition screens */
#iring { position: absolute; left: -460px; top: -232px; width: 2000px; height: 2000px; border-radius: 50%; border: 10px solid var(--gold);
  box-shadow: 0 0 60px rgba(218,182,106,.8), inset 0 0 60px rgba(218,182,106,.6); opacity: 0; }
#wbar { position: absolute; left: 0; top: 0; width: 1080px; height: 16px; opacity: 0;
  background: linear-gradient(90deg, #9a7a32, #DAB66A 30%, #fff1c4 50%, #DAB66A 70%, #9a7a32); box-shadow: 0 0 40px 8px rgba(218,182,106,.75); }
#pedge { position: absolute; left: -8px; top: 0; width: 16px; height: 1920px; opacity: 0;
  background: linear-gradient(#9a7a32, #DAB66A 30%, #fff1c4 50%, #DAB66A 70%, #9a7a32); box-shadow: 0 0 40px 8px rgba(218,182,106,.75); }
/* hud: brand label and progress, after the reference */
.brand { position: absolute; left: 44px; top: 84px; display: flex; align-items: center; gap: 14px; font: 700 28px "JBMono"; letter-spacing: 5px;
  color: var(--gold); padding: 10px 22px; border-radius: 30px; background: rgba(21,17,14,.78); border: 1px solid rgba(97,82,48,.8); }
.brand .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--gold); box-shadow: 0 0 14px rgba(218,182,106,.9); }
.ptrack { position: absolute; left: 820px; top: 106px; width: 204px; height: 10px; border-radius: 5px; background: rgba(242,234,221,.2); overflow: hidden; }
.pfill { position: absolute; inset: 0; background: var(--gold); transform-origin: 0 50%; border-radius: 5px; }
/* backdrop: the app's dark world, a faint gold grid, a gold halo, the logo's compass rose turning slowly, gold dust */
#bgbase { position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 40%, #3a2e1b 0%, #1d1812 50%, #120f0c 88%); }
#grid { position: absolute; left: 0; top: 0; width: 1080px; height: 2400px; opacity: .55;
  background-image: linear-gradient(rgba(218,182,106,.07) 2px, transparent 2px), linear-gradient(90deg, rgba(218,182,106,.07) 2px, transparent 2px);
  background-size: 90px 90px; -webkit-mask-image: radial-gradient(70% 50% at 50% 35%, #000, transparent); }
#rose { position: absolute; left: -210px; top: 10px; width: 1500px; height: 1500px; opacity: .1; }
#dust { position: absolute; inset: 0; }
.du { position: absolute; border-radius: 50%; background: var(--gold); box-shadow: 0 0 10px rgba(218,182,106,.8); opacity: 0; }
.sp4 { position: absolute; opacity: .7; }
#vig { position: absolute; inset: 0; background: radial-gradient(120% 80% at 50% 45%, rgba(0,0,0,0) 55%, rgba(5,4,3,.65) 100%); }
.aur { position: absolute; border-radius: 50%; opacity: .55; }
.au1 { left: -200px; top: 80px; width: 900px; height: 700px; background: radial-gradient(closest-side, rgba(218,182,106,.32), rgba(218,182,106,0)); }
.au2 { left: 380px; top: 420px; width: 900px; height: 800px; background: radial-gradient(closest-side, rgba(46,94,52,.45), rgba(46,94,52,0)); }
.scene { z-index: 1; }
.sw { position: absolute; inset: 0; }
.ghost { position: absolute; left: -40px; top: 1080px; white-space: nowrap; font: 800 300px/1 "Manrope"; letter-spacing: -8px; color: transparent;
  -webkit-text-stroke: 3px rgba(218,182,106,.16); }
#sweepfx { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0;
  background: linear-gradient(105deg, rgba(255,241,196,0) 38%, rgba(255,241,196,.22) 47%, rgba(255,255,255,.45) 50%, rgba(255,241,196,.22) 53%, rgba(255,241,196,0) 62%); }
.br { position: absolute; width: 220px; height: 220px; border-radius: 50%; border: 5px solid; opacity: 0; }
.br i { position: absolute; left: 90px; top: 90px; width: 40px; height: 40px; border-radius: 50%; filter: blur(6px); }
.tp { position: absolute; width: 70px; height: 70px; margin: -35px 0 0 -35px; border-radius: 50%; border: 4px solid #fff;
  background: rgba(255,255,255,.35); opacity: 0; }
.coin { border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: "Manrope"; font-weight: 800; color: #6b521d;
  background: radial-gradient(circle at 35% 30%, #fff1c4, #DAB66A 45%, #9a7a32 100%); box-shadow: 0 10px 30px rgba(0,0,0,.4), inset 0 0 0 4px rgba(255,240,200,.4); }
/* app-style icon tile, cards, chips */
.tile { position: relative; display: flex; align-items: center; justify-content: center; border-radius: 30%;
  background: linear-gradient(160deg, var(--card2), var(--card) 60%, #241e14); border: 2px solid var(--border);
  box-shadow: 0 24px 60px rgba(0,0,0,.55); }
.num { display: flex; align-items: center; justify-content: center; width: 76px; height: 76px; border-radius: 50%; flex: none;
  background: var(--cream); color: #1d1812; font: italic 700 44px/1 "Fraunces"; box-shadow: 0 10px 30px rgba(0,0,0,.5); }
.chip { position: absolute; left: 0; top: 180px; width: 1080px; text-align: center; }
.chip span { display: inline-block; padding: 14px 30px; border-radius: 40px; font: 700 26px "JBMono"; letter-spacing: 4px; color: var(--gold);
  background: rgba(46,39,23,.9); border: 2px solid var(--border); box-shadow: 0 0 40px rgba(218,182,106,.25); }
.chip.lavc span { color: var(--lav); background: rgba(38,31,47,.92); border-color: #4a3f5e; box-shadow: 0 0 40px rgba(183,168,224,.3); }
.qq { position: absolute; right: -18px; top: -26px; font: italic 700 80px "Fraunces"; color: var(--gold); text-shadow: 0 0 20px rgba(0,0,0,.8); }
.phone { position: absolute; border-radius: 40px; padding: 9px; background: #0b0907; box-shadow: 0 0 0 2px #3a3126, 0 40px 90px rgba(0,0,0,.6),
  0 0 80px rgba(218,182,106,.22); overflow: hidden; }
.scr { position: relative; width: 100%; height: 100%; border-radius: 32px; overflow: hidden; background: var(--bg); }
.scr img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 0; display: block; transform-origin: 50% 0; }
.pglare { position: absolute; inset: 0; border-radius: 40px; background: linear-gradient(125deg, rgba(255,255,255,.10), rgba(255,255,255,0) 40%); }
/* 0 */
.capw { position: absolute; left: 400px; top: 330px; width: 280px; height: 280px; }
.capglow { position: absolute; left: -110px; top: -110px; width: 500px; height: 500px; border-radius: 50%; z-index: -1;
  background: radial-gradient(circle, rgba(218,182,106,.5), rgba(218,182,106,0) 65%); }
.cd { position: absolute; left: 105px; top: -20px; opacity: 0; }
.stacks { position: absolute; left: 0; width: 1080px; top: 700px; height: 440px; display: flex; justify-content: center; align-items: flex-end; gap: 70px; }
.stkc { width: 150px; height: 420px; }
.stkc i { display: block; width: 100%; height: 100%; border-radius: 18px; box-shadow: 0 0 50px rgba(218,182,106,.35);
  background: repeating-linear-gradient(0deg, #8a6a28 0 5px, #DAB66A 5px 24px, #fff1c4 24px 27px); }
/* 1 */
.links { position: absolute; left: 0; top: 0; }
.kid { position: absolute; left: 370px; top: 290px; width: 340px; height: 340px; display: flex; align-items: center; justify-content: center;
  border-radius: 50%; background: radial-gradient(circle, #2c2418, #1a1511); }
.kring { position: absolute; inset: -10px; border-radius: 50%; border: 5px solid var(--gold); box-shadow: 0 0 60px rgba(218,182,106,.45); }
.orbx { position: absolute; top: 820px; }
.ox1 { left: 130px; } .ox2 { left: 760px; }
.hglass { position: absolute; left: 485px; top: 1060px; }
/* 2 */
.card2 { position: absolute; left: 80px; width: 920px; height: 400px; border-radius: 40px; display: flex; align-items: center; justify-content: center;
  gap: 40px; background: linear-gradient(160deg, var(--card2), var(--card) 60%, #241e14); border: 2px solid var(--border);
  box-shadow: 0 30px 80px rgba(0,0,0,.55); }
.card2 > .num { position: absolute; left: -22px; top: -22px; }
.ca { top: 300px; } .cb { top: 790px; }
.rep, .bcw { position: relative; }
.grade { position: absolute; left: 110px; top: -34px; font: 800 52px "Manrope"; color: #1d1812; background: var(--gold); padding: 4px 18px; border-radius: 14px; z-index: 2; }
.farr { display: block; width: 110px; height: 8px; border-radius: 4px; background: var(--gold); transform-origin: 0 50%; position: relative; }
.farr::after { content: ""; position: absolute; right: -14px; top: -11px; border: 15px solid transparent; border-left-color: var(--gold); }
.fork { display: flex; flex-direction: column; gap: 14px; }
.lk { position: absolute; right: -40px; top: -44px; }
/* 3 */
.studs { position: absolute; left: 0; width: 1080px; top: 260px; display: flex; justify-content: center; gap: 40px; }
.stu { width: 130px; height: 130px; border-radius: 34px; background: rgba(33,28,24,.95); border: 2px solid var(--border); display: flex;
  align-items: center; justify-content: center; }
.funnel { position: absolute; left: 220px; top: 470px; transform-origin: 50% 0; filter: drop-shadow(0 0 30px rgba(218,182,106,.4)); }
.sames { position: absolute; left: 0; width: 1080px; top: 960px; display: flex; justify-content: center; gap: 30px; }
.same { width: 110px; height: 110px; border-radius: 30px; background: #26211c; border: 2px solid #4a4238; display: flex; align-items: center; justify-content: center; }
/* 4 */
.dialw { position: absolute; left: 250px; top: 290px; width: 580px; height: 580px; filter: drop-shadow(0 0 50px rgba(218,182,106,.4)); }
.side4 { position: absolute; top: 960px; }
.sa { left: 100px; } .sb { left: 800px; }
.xline { position: absolute; left: -10px; top: 86px; width: 200px; height: 9px; background: #E07A6A; transform: rotate(-35deg); transform-origin: 0 50%;
  border-radius: 5px; }
/* 5 */
.intro { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; }
.intro .logo { position: relative; width: 400px; height: auto; z-index: 2; }
.intro .wm { position: relative; z-index: 2; margin-top: 10px; font: italic 600 130px/1.05 "Fraunces"; color: var(--gold); letter-spacing: -2px;
  text-shadow: 0 0 50px rgba(218,182,106,.35); }
.intro .halo { position: absolute; left: 140px; top: -180px; width: 800px; height: 800px; border-radius: 50%; z-index: 1;
  background: radial-gradient(circle, rgba(218,182,106,.42), rgba(218,182,106,0) 65%); }
.rays { position: absolute; left: 40px; top: -300px; width: 1000px; height: 1000px; border-radius: 50%; z-index: 0;
  background: repeating-conic-gradient(rgba(218,182,106,.16) 0deg 6deg, rgba(218,182,106,0) 6deg 18deg);
  -webkit-mask-image: radial-gradient(closest-side, #000 20%, transparent); }
.ph5 { left: 60px; top: 300px; }
.steps { position: absolute; left: 450px; top: 290px; width: 570px; display: flex; flex-direction: column; gap: 30px; }
.stp { display: flex; align-items: center; gap: 22px; height: 160px; padding: 0 26px; border-radius: 34px;
  background: linear-gradient(160deg, var(--card2), var(--card) 60%, #241e14); border: 2px solid var(--border); box-shadow: 0 20px 50px rgba(0,0,0,.5); }
.stp .num { width: 64px; height: 64px; font-size: 38px; }
.mtr { flex: 1; height: 14px; border-radius: 7px; background: rgba(0,0,0,.35); overflow: hidden; }
.mtr i { display: block; width: 100%; height: 100%; background: linear-gradient(90deg, #9a7a32, var(--gold)); transform-origin: 0 50%; border-radius: 7px; }
/* 6 */
.cosmos { position: absolute; inset: 0; }
.cs { position: absolute; border-radius: 50%; background: #fff6d8; box-shadow: 0 0 8px #fff; }
.orbits { position: absolute; left: 540px; top: 700px; width: 0; height: 0; }
.orb { position: absolute; border-radius: 50%; border: 2px dashed rgba(218,182,106,.5); }
.orb.o1 { left: -250px; top: -250px; width: 500px; height: 500px; }
.orb.o2 { left: -400px; top: -400px; width: 800px; height: 800px; border-color: rgba(183,168,224,.45); }
.och { position: absolute; left: 50%; top: -60px; margin-left: -60px; width: 120px; height: 120px; border-radius: 34px; display: flex;
  align-items: center; justify-content: center; background: var(--card); border: 2px solid var(--border); box-shadow: 0 0 40px rgba(218,182,106,.3); }
.och.lv { background: var(--plum); border-color: #4a3f5e; box-shadow: 0 0 40px rgba(183,168,224,.3); }
.gem { position: absolute; left: -100px; top: -100px; width: 200px; height: 200px; border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #8fb0ff, #1e3a8a 55%, #0b1638); box-shadow: 0 0 0 10px rgba(218,182,106,.6), 0 0 90px rgba(80,120,255,.55); }
.toggle { position: absolute; left: 460px; top: 1150px; width: 160px; height: 84px; border-radius: 42px; background: #2a2333; border: 2px solid #4a3f5e; }
.knob { position: absolute; left: 6px; top: 6px; width: 68px; height: 68px; border-radius: 50%; background: var(--lav); box-shadow: 0 0 24px rgba(183,168,224,.8); }
.ph6 { left: 320px; top: 270px; }
.lsp { position: absolute; filter: drop-shadow(0 0 14px rgba(183,168,224,.8)); }
/* 7 */
.tape { position: absolute; left: -210px; width: 1500px; height: 120px; }
.tp1 { top: 270px; transform: rotate(-7deg); } .tp2 { top: 1100px; transform: rotate(6deg); }
.tin { position: absolute; inset: 0; display: flex; align-items: center; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,.6);
  background: repeating-linear-gradient(-45deg, #DAB66A 0 40px, #1a1511 40px 80px); }
.ttrack { white-space: nowrap; padding: 6px 0; width: max-content; background: #15110E; font: 700 34px "JBMono"; letter-spacing: 4px; color: var(--gold); }
.nog { position: absolute; top: 640px; }
.ng1 { left: 250px; } .ng2 { left: 610px; }
.xl { position: absolute; left: -20px; top: 110px; width: 270px; height: 10px; border-radius: 5px; background: #E07A6A; transform: rotate(-40deg);
  transform-origin: 0 50%; box-shadow: 0 0 20px rgba(224,122,106,.6); }
/* 9 */
.venn { position: absolute; left: 540px; top: 700px; width: 0; height: 0; }
.vc { position: absolute; left: -210px; top: -210px; width: 420px; height: 420px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; mix-blend-mode: screen; }
.v1 { background: radial-gradient(circle, rgba(131,145,114,.65), rgba(131,145,114,.25)); border: 3px solid var(--sage); justify-content: flex-start; padding-left: 60px; align-items: flex-start; padding-top: 110px; }
.v2 { background: radial-gradient(circle, rgba(218,182,106,.6), rgba(218,182,106,.22)); border: 3px solid var(--gold); justify-content: flex-end; padding-right: 60px; align-items: flex-start; padding-top: 110px; }
.v3 { background: radial-gradient(circle, rgba(183,168,224,.55), rgba(183,168,224,.2)); border: 3px solid var(--lav); align-items: flex-end; padding-bottom: 60px; }
.vcore { position: absolute; left: -65px; top: -65px; filter: drop-shadow(0 0 30px rgba(255,230,160,.95)); }
/* 10 */
.ph10 { left: 70px; top: 290px; }
.tick { position: absolute; top: 310px; }
.tick.t1 { left: 560px; } .tick.t2 { left: 800px; }
.tk { position: absolute; right: -16px; bottom: -16px; background: var(--bg); border-radius: 50%; }
.gauge { position: absolute; left: 545px; top: 600px; width: 440px; height: 250px; }
.gneedle { position: absolute; left: 216px; top: 70px; width: 8px; height: 160px; border-radius: 4px; background: var(--cream); transform-origin: 50% 100%;
  box-shadow: 0 0 12px rgba(242,234,221,.6); }
.ghub { position: absolute; left: 204px; top: 214px; width: 32px; height: 32px; border-radius: 50%; background: var(--gold); }
.stars { position: absolute; left: 545px; top: 910px; width: 440px; display: flex; justify-content: center; gap: 20px;
  filter: drop-shadow(0 0 12px rgba(218,182,106,.7)); }
/* 11 */
.timer { position: absolute; left: 340px; top: 270px; width: 400px; height: 400px; filter: drop-shadow(0 0 40px rgba(218,182,106,.35)); }
.timer svg { position: absolute; inset: 0; }
.tnum { position: absolute; left: 0; width: 400px; top: 130px; text-align: center; font: 700 120px/1 "Manrope"; }
.ph11a { left: 90px; top: 760px; transform: rotate(-6deg); }
.ph11b { left: 760px; top: 760px; transform: rotate(6deg); }
/* 12 */
.ph12 { left: 320px; top: 270px; }
.obs { position: absolute; left: 540px; top: 700px; width: 0; height: 0; }
.ob { position: absolute; left: -40px; top: -40px; opacity: 0; }
.offer { position: absolute; left: 130px; top: 300px; width: 820px; height: 880px; border-radius: 40px; text-align: center; overflow: hidden;
  background: linear-gradient(160deg, var(--card2), var(--card) 60%, #241e14); border: 2px solid var(--border); box-shadow: 0 30px 80px rgba(0,0,0,.55); }
.ologo { width: 170px; margin-top: 60px; }
.ostamp { display: block; width: 580px; margin: 40px auto 0; font: 800 124px/1 "Manrope"; color: #1d1812; background: var(--gold); padding: 20px 0;
  border-radius: 26px; box-shadow: 0 0 60px rgba(218,182,106,.5); }
.oprice { margin-top: 80px; font: italic 700 200px/1 "Fraunces"; color: var(--cream); }
.shine { position: absolute; top: -20%; left: 0; width: 30%; height: 140%; transform: rotate(18deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,240,200,.28), rgba(255,255,255,0)); }
/* 13 */
.die { position: absolute; top: 560px; }
.dc0 { left: 140px; } .dc1 { left: 370px; top: 600px; } .dc2 { left: 590px; } .dc3 { left: 820px; top: 590px; }
.sweep { position: absolute; left: 100px; top: 640px; width: 880px; height: 14px; border-radius: 7px; background: var(--gold); transform-origin: 0 50%;
  box-shadow: 0 0 40px rgba(218,182,106,.8); }
.land { position: absolute; left: 420px; top: 500px; }
/* 14 */
.i14 { top: 360px; }
.i14 .logo { width: 360px; }
.i14 .wm { font-size: 120px; }
/* 15 */
.cta { position: absolute; left: 0; width: 1080px; top: 320px; text-align: center; }
.cta .halo { position: absolute; left: 190px; top: -200px; width: 700px; height: 700px; border-radius: 50%;
  background: radial-gradient(circle, rgba(218,182,106,.4), rgba(218,182,106,0) 65%); }
.cta .logo { position: relative; display: block; margin: 0 auto; width: 300px; height: auto; }
.ctab { position: relative; display: block; width: max-content; margin: 50px auto 0; padding: 34px 60px; border-radius: 80px; background: var(--gold); color: #1d1812;
  font: 800 62px "Manrope"; letter-spacing: -1px; }
.ctaf { position: relative; margin-top: 50px; font: italic 700 210px/1 "Fraunces"; color: var(--gold); text-shadow: 0 0 40px rgba(218,182,106,.9), 0 0 120px rgba(218,182,106,.6); }
.cursor { position: absolute; left: 885px; top: 800px; width: 70px; height: 70px; border-radius: 50%; background: rgba(255,255,255,.9);
  border: 6px solid rgba(255,255,255,.4); background-clip: padding-box; box-shadow: 0 10px 30px rgba(0,0,0,.5); opacity: 0; }
/* captions: the active word on a gold pill */
.cap { position: absolute; left: 30px; width: 1020px; top: 1330px; text-align: center; opacity: 0; font: 800 58px/1.3 "Manrope"; word-spacing: 2px; }
.cw { display: inline-block; padding: 0 12px; border-radius: 14px; font: 800 58px/1.2 "Manrope"; letter-spacing: -1px; color: var(--cream); }
.cw.em { font: italic 600 66px/1.1 "Fraunces"; color: var(--gold); }
#flash { position: absolute; inset: 0; background: #fff3d6; opacity: 0; }
"""


# the speaker's grade: Natural Portrait seed (skin-soft 0.6) pushed for punch: more contrast and vibrance, deeper blacks,
# highlights held on the white wall, warmth toward the brand gold, a vignette, light bloom and fine grain; validated with
# `hyperframes media-treatment --dry-run` (build/grade.json is its normalized form)
GRADE = __import__("html").escape(json.dumps(json.load(open(os.path.join(ROOT, "build", "grade.json"))), separators=(",", ":")), quote=True)


def main():
    tl_js = TL()
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
      <div id="spk" data-layout-allow-overflow><div id="spkw">
        <video id="talk" data-color-grading="{GRADE}" src="assets/video/{os.environ.get("SPK_SRC", "talk.mp4")}" data-start="0" data-duration="{VO}" data-track-index="2" muted playsinline></video></div></div>
      <div id="look" class="clip ov" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow><div id="leak"></div><div class="shade top"></div><div class="shade bot"></div></div>
      {STICKERS}
      <div id="stage" data-layout-allow-overflow>
        <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-allow-overflow>{backdrop()}</div>
        {SCENES}
      </div>
      <div id="trans"><div id="iring"></div><div id="wbar"></div><div id="pedge"></div></div>
      <div id="hud" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6"><div class="brand"><i class="dot"></i>SUCSESS MAPERRS</div><div class="ptrack"><i class="pfill"></i></div></div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{captions_html()}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8"><div id="sweepfx"></div>{bursts_html()}<div id="flash"></div></div>
      <audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{VO}" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // lines on the cut timeline: {edlv}
{tl_js}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(sorted(EV), open(os.path.join(ROOT, "build", "sfx_events.json"), "w"))
    print("wrote index.html", len(html) // 1024, "KB,", DUR, "s")


STICKERS = SCENES = ""


def TL():
    global STICKERS, SCENES
    backdrop_tl()
    frame_tl()
    STICKERS = stickers()
    SCENES = scenes()
    scenes_tl()
    # the flash on the two brand reveals
    for t in (L[5][0], L[14][0]):
        add(f'tl.fromTo("#flash",{{opacity:.5}},{{opacity:0,duration:.5,ease:"power2.out",immediateRender:false}},{t:.2f});')
    captions_tl()
    return "\n".join(T)


if __name__ == "__main__":
    main()
