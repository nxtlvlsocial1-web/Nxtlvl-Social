"""Reel-flop explainer, 9:16 (1080x1920, 30 fps), v5: professional kinetic typography ("After Effects feel").

Owner: the papercraft look "looks weird, go with professional After Effects type of feel for the motion graphics and
texts", with a reference screen recording (reference/ref2.mov, kept out of git): a clean picker-wheel list of names
rolling vertically with heavy vertical motion blur, the centre item lit with a colour gradient, neighbours dark, the
outer ones small and faded; a bold static phrase beside it; a soft white ground with drifting pastel glows; one clean
semibold sans. The whole reel is built in that language (stacked vertically for 9:16: the phrase above, the wheel below):
  * cold open: big words rise in through line masks with motion blur, a colour-split glitch on "lose", a whip;
  * a wheel of excuses lands on "the algorithm" (struck through), then spins hard to "the first 3 seconds";
  * a giant slot-machine digit rolls 3-2-1-0, the 0 red on a dark flash as the music's beat drops;
  * a wheel of the three mistakes rolls to each one as it is spoken; "Hey guys." scrambles into the result; the wheel
    whips away on "thumbs keep scrolling"; SHOW / EXPLAIN swap places;
  * the fixes roll by with checks, the views count is an odometer of digit wheels; a keyword wheel lands on HOOK.
Script, voice, word timings and music are unchanged. Earlier looks: cache/generate_v3_backup.py (minimal black/white),
cache/generate_v4_papercraft.py.

/root/tts/.venv/bin/python build/generate.py  ->  index.html, plan/sfx_events.json
"""
import json
import math
import os
import random

from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
DUR = round(WORDS[-1]["t1"] + 2.1, 2)
INK, RED = "#121212", "#ff2a2a"
A, SFX, DEFS = [], [], []
R = random.Random(5)
LEFT = 80
MAXW = 920


def js(s):
    A.append("      " + s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def words_of(line):
    return [w for w in WORDS if w["line"] == line]


def L(line, i, key="t0"):
    return words_of(line)[i][key]


_F = {}


def text_w(s, size, weight=700, ls=-.02):
    if weight not in _F:
        _F[weight] = TTFont(os.path.join(ROOT, "assets", "fonts", f"inter-latin-{weight}-normal.woff2"))
    f = _F[weight]
    cmap, hm, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    return sum(hm[cmap.get(ord(c), cmap[ord("n")])][0] for c in s) / upm * size + ls * size * max(0, len(s) - 1)


def vblur(name):
    """A vertical motion-blur filter (SVG gaussian with a 0 x-deviation) whose amount the timeline animates."""
    DEFS.append(f'<filter id="vb_{name}" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur id="vbg_{name}" stdDeviation="0 0"/></filter>')
    return f"url(#vb_{name})"


def blur_pulse(name, t, peak, d_in, d_out):
    js(f'tl.fromTo("#vbg_{name}", {{attr: {{stdDeviation: "0 0"}}}}, {{attr: {{stdDeviation: "0 {peak}"}}, duration: {d_in:.3f}, ease: "power2.in", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#vbg_{name}", {{attr: {{stdDeviation: "0 0"}}, duration: {d_out:.3f}, ease: "power2.out"}}, {t + d_in:.3f});')


# ---------------------------------------------------------------- scenes: enter / exit with a vertical whip + blur
def scene_in(sid, t, d=.45, dy=220):
    js(f'tl.fromTo("#{sid}", {{opacity: 0, y: {dy * .5:.0f}, scale: .82}}, {{opacity: 1, y: 0, scale: 1, duration: {d}, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    blur_pulse(sid, t, 26, .02, d)


def scene_out(sid, t, d=.3, dy=-220):
    js(f'tl.to("#{sid}", {{opacity: 0, y: {dy * .4:.0f}, scale: 1.22, duration: {d}, ease: "expo.in"}}, {t:.3f});')
    blur_pulse(sid, t, 30, d, .05)
    sfx("swish", t)


def scene(sid, inner, shown=False):
    f = vblur(sid)
    return f'<div class="scn" id="{sid}" style="filter:{f};{"opacity:1" if shown else ""}">{inner}</div>'


# ---------------------------------------------------------------- the phrase: words rise through line masks as spoken
STY = {"xl": (160, 800, -.035), "l": (110, 800, -.03), "m": (88, 700, -.025), "s": (60, 600, -.01)}


def phrase(pid, line, rows, top, start=0, t_out=None, left=LEFT, first_visible=False):
    """rows: [(style, "text")]; words pair with the line's spoken words from `start`. Markup: *word* red gradient,
    ^word^ blue gradient, _word_ grey, ~word~ struck later (id pid_s)."""
    ws = words_of(line)
    k = start
    out = [f'<div class="ph" id="{pid}" style="top:{top}px;left:{left}px">']
    for r, (sty, text) in enumerate(rows):
        size, wt, ls = STY[sty]
        plain = "".join(c for c in text if c not in "*^_~=+")
        size = min(size, int(MAXW / max(1, text_w(plain, 1, wt, ls))))
        out.append(f'<div class="ln {sty}" style="font-size:{size}px;font-weight:{wt}">')
        for j, word in enumerate(text.split(" ")):
            cls = "w"
            if word.startswith("*"):
                cls += " gr1"
            elif word.startswith("^"):
                cls += " gr2"
            elif word.startswith("_"):
                cls += " grey"
            stk = word.startswith("~")
            mark = "r" if word.startswith("=") else ("b" if word.startswith("+") else "")
            word = word.strip("*^_~=+")
            wid = f"{pid}_{r}_{j}"
            vis = first_visible and k == start
            chars = sty == "xl" and not vis and " gr" not in cls and not mark and not stk
            if chars:
                inner = "".join(f'<span class="ch" id="{wid}c{c}">{ch}</span>' for c, ch in enumerate(word))
            else:
                inner = f'{word}<i class="stk" id="{pid}_s"></i>' if stk else word
            if mark:
                cls += " hlw"
                inner = f'<i class="mkr {mark}" id="{wid}m"></i><span class="hlt" id="{wid}t">{inner}</span>'
            out.append(f'<span class="wm{" wmh" if mark else ""}"><span class="{cls}" id="{wid}"{" style=opacity:1" if vis else ""}>{inner}</span></span>')
            if not vis:
                t = ws[k]["t0"]
                if chars:
                    js(f'tl.set("#{wid}", {{opacity: 1}}, {t - .06:.3f});')
                    for c in range(len(word)):
                        js(f'tl.fromTo("#{wid}c{c}", {{yPercent: 105, rotationX: -85, opacity: 0, transformPerspective: 600}}, {{yPercent: 0, rotationX: 0, opacity: 1, transformPerspective: 600, duration: .5, ease: "back.out(1.7)", immediateRender: false}}, {t - .05 + c * .028:.3f});')
                else:
                    js(f'tl.fromTo("#{wid}", {{yPercent: 110, opacity: 0}}, {{yPercent: 0, opacity: 1, duration: .42, ease: "expo.out", immediateRender: false}}, {t - .05:.3f});')
                if mark:
                    js(f'tl.fromTo("#{wid}m", {{scaleX: 0}}, {{scaleX: 1, duration: .32, ease: "expo.out", immediateRender: false}}, {t + .1:.3f});')
                    js(f'tl.to("#{wid}t", {{color: "#ffffff", duration: .15}}, {t + .16:.3f});')
            k += 1
        out.append("</div>")
    out.append("</div>")
    if t_out:
        js(f'tl.to("#{pid}", {{opacity: 0, y: -60, duration: .26, ease: "expo.in"}}, {t_out:.3f});')
    return "".join(out)


# ---------------------------------------------------------------- icons (24 px line icons, drawn here)
ICONS = {
    "hash": '<path d="M4 9h16M4 15h16M10 3L8 21M16 3l-2 18"/>',
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    "eyeoff": '<path d="M3 3l18 18M10.6 10.6a2 2 0 0 0 2.8 2.8M9.9 4.2A10 10 0 0 1 12 4c6 0 10 8 10 8a17 17 0 0 1-3 3.8M6.6 6.6C3.9 8.3 2 12 2 12s4 8 10 8a9.7 9.7 0 0 0 5.4-1.6"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>',
    "lines": '<path d="M3 6h18M3 12h12M3 18h16"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "trend": '<path d="M22 7l-8.5 8.5-5-5L2 17M16 7h6v6"/>',
    "timer": '<circle cx="12" cy="14" r="8"/><path d="M12 10v4M9 2h6M12 2v2"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8A8.5 8.5 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5z"/>',
    "pause": '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/>',
    "play": '<path d="M6 3l14 9-14 9z"/>',
    "send": '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
    "bookmark": '<path d="M6 3.5h12v17l-6-4.2-6 4.2z"/>',
    "heart": '<path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"/>',
}


def icon(name, cls="ic", style=""):
    return f'<svg class="{cls}" viewBox="0 0 24 24"{f" style={chr(34)}{style}{chr(34)}" if style else ""}>{ICONS[name]}</svg>'


# ---------------------------------------------------------------- the picker wheel
class Wheel:
    """A vertical list; the item at the centre is full size and lit with its gradient, neighbours dark, outer ones
    smaller and faded. move() rolls it item by item (decelerating) with vertical motion blur."""
    SP = [0, 1.08, 1.9, 2.55, 3.05, 3.4]          # distance from centre, in item heights
    SC = [1, .86, .62, .5, .42, .38]
    OP = [1, .9, .32, .08, .03, 0]

    def __init__(self, wid, items, top, size, left=LEFT, start=0, grads=None, maxw=MAXW, weight=800, icons=None):
        self.wid, self.items, self.top, self.left, self.p = wid, items, top, left, start
        self.icons = icons
        widest = max(text_w(s, 1, weight, -.03) for s in items) + (1.15 if icons else 0)
        self.size = min(size, int(maxw / widest))
        self.grads = grads or ["gr1"] * len(items)
        self.weight = weight
        self.filter = vblur(wid)
        self.busy = 0.0           # a move never starts before the previous one (and its blur, its light) has finished

    def state(self, d):
        a = min(abs(d), len(self.SP) - 1)
        lo, hi = int(math.floor(a)), min(int(math.floor(a)) + 1, len(self.SP) - 1)
        f = a - lo
        sp = self.SP[lo] + (self.SP[hi] - self.SP[lo]) * f
        sc = self.SC[lo] + (self.SC[hi] - self.SC[lo]) * f
        op = self.OP[lo] + (self.OP[hi] - self.OP[lo]) * f
        y = math.copysign(sp * self.size, d) if d else 0
        return {"y": round(y, 1), "scale": round(sc, 3), "opacity": round(op, 3)}

    def html(self):
        out = [f'<div class="whl" id="{self.wid}" style="filter:{self.filter}">']
        for i, s in enumerate(self.items):
            ib = ig = ""
            if self.icons:
                path = ICONS[self.icons[i]]
                grad = "ig1" if self.grads[i] == "gr1" else "ig2"
                ib = f'<svg class="ic" viewBox="0 0 24 24">{path}</svg>'
                ig = f'<svg class="ic" viewBox="0 0 24 24" style="stroke:url(#{grad})">{path}</svg>'
            out.append(f'<div class="wi" id="{self.wid}_{i}" style="left:{self.left}px;top:{self.top - self.size * .6:.0f}px;font-size:{self.size}px;font-weight:{self.weight}">'
                       f'<span class="b">{ib}{s}</span><span class="g" id="{self.wid}_{i}g">{ig}<span class="{self.grads[i]}">{s}</span></span></div>')
        out.append("</div>")
        return "".join(out)

    @staticmethod
    def fmt(st):
        return ", ".join(f"{k}: {v}" for k, v in st.items())

    def appear(self, t, d=.4):
        """The items take their places, rising in."""
        self.busy = t + d + .03 * len(self.items) + .25
        for i in range(len(self.items)):
            st = self.state(i - self.p)
            fr = dict(st, y=st["y"] + 160, opacity=0)
            js(f'tl.fromTo("#{self.wid}_{i}", {{{self.fmt(fr)}}}, {{{self.fmt(st)}, duration: {d}, ease: "expo.out", immediateRender: false}}, {t + abs(i - self.p) * .03:.3f});')
        blur_pulse(self.wid, t, 18, .02, d)
        self.light(t + .2)

    def light(self, t, on=True):
        i = round(self.p)
        js(f'tl.fromTo("#{self.wid}_{i}g", {{opacity: {0 if on else 1}}}, {{opacity: {1 if on else 0}, duration: .22, immediateRender: false}}, {t:.3f});')

    def move(self, t, to, dur, final_ease="back.out(1.6)", tick=True):
        n = abs(to - self.p)
        if n == 0:
            return
        if t < self.busy:
            dur = max(.18, dur - (self.busy - t))
            t = self.busy
        self.light(t, on=False)
        s = 1 if to > self.p else -1
        # step boundaries follow a decelerating curve (quadratic ease-out): fast first, settling into the last item
        bounds = [t + dur * (1 - math.sqrt(1 - k / n)) for k in range(n + 1)]
        for k in range(n):
            p0, p1 = self.p + s * k, self.p + s * (k + 1)
            last = k == n - 1
            for i in range(len(self.items)):
                st0, st1 = self.state(i - p0), self.state(i - p1)
                if st0["opacity"] == 0 and st1["opacity"] == 0:
                    continue
                d = bounds[k + 1] - bounds[k]
                js(f'tl.fromTo("#{self.wid}_{i}", {{{self.fmt(st0)}}}, {{{self.fmt(st1)}, duration: {d:.3f}, ease: "{final_ease if last else "none"}", immediateRender: false}}, {bounds[k]:.3f});')
        peak = min(26, 7 + 3 * n)
        blur_pulse(self.wid, t, peak, min(.12, dur * .3), max(.1, dur * .6))
        if tick:
            sfx("swish" if n > 2 else "tick", t)
            sfx("tick", t + dur - .02)
        self.p = to
        self.light(t + dur - .06)
        if self.icons:
            js(f'tl.fromTo("#{self.wid}_{to} .ic", {{rotation: 0, scale: 1, transformOrigin: "50% 50%"}}, {{keyframes: {{rotation: [0, -18, 14, -6, 0], scale: [1, 1.25, 1.1, 1]}}, duration: .5, ease: "power1.out", immediateRender: false}}, {t + dur - .05:.3f});')
        self.busy = t + dur + .2
        return t + dur


class Odometer:
    """Digit wheels in masks: each strip rolls to its digit (with extra turns), left to right, with motion blur."""

    def __init__(self, oid, digits_from, digits_to, top, size, left):
        self.oid, self.top, self.size, self.left = oid, top, size, left
        self.fr, self.to = digits_from, digits_to
        self.filter = vblur(oid)

    def html(self):
        out = [f'<div class="odo" id="{self.oid}" style="top:{self.top}px;left:{self.left}px;font-size:{self.size}px;filter:{self.filter}">']
        seq = [" "] + [str(d) for d in range(10)] * 3
        self.seq = seq
        for i, ch in enumerate(self.to):
            if ch == ",":
                out.append(f'<span class="oc" id="{self.oid}_c">,</span>')
                continue
            top = -seq.index(self.fr[i]) * self.size
            out.append(f'<span class="om"><span class="os" id="{self.oid}_{i}" style="top:{top}px">' + "".join(f"<b>{c}</b>" for c in seq) + "</span></span>")
        out.append("</div>")
        return "".join(out)

    def roll(self, t, dur):
        for k, (a, b) in enumerate(zip(self.fr, self.to)):
            if b == ",":
                continue
            i0 = self.seq.index(a)
            i1 = 21 + int(b)            # land in the third loop: every digit turns at least once
            d = dur * (.6 + .4 * k / len(self.to))
            js(f'tl.fromTo("#{self.oid}_{k}", {{y: 0}}, {{y: {-(i1 - i0) * self.size:.0f}, duration: {d:.2f}, ease: "power3.inOut", immediateRender: false}}, {t:.3f});')
        js(f'tl.fromTo("#{self.oid}_c", {{opacity: 0}}, {{opacity: 1, duration: .2, immediateRender: false}}, {t + dur * .5:.3f});')
        blur_pulse(self.oid, t, 22, dur * .3, dur * .6)



# ---------------------------------------------------------------- v8: chapter swipes, colour themes, the camera
WIPES = []
WP = []


def wipe(t, label, sub="", grad=("#ff2a2a", "#ff3d7f", "#d02cff")):
    """A diagonal gradient panel sweeps across the frame carrying a chapter title; the scene swaps under it at t."""
    wid = f"wp{len(WIPES)}"
    WIPES.append(t)
    WP.append(f'<div class="wp" id="{wid}" style="background:linear-gradient(120deg, {grad[0]}, {grad[1]} 55%, {grad[2]})">'
              f'<div class="wpl" id="{wid}l"><b style="font-size:{min(300, int(860 / text_w(label, 1, 800, -.05)))}px">{label}</b>{f"<span>{sub}</span>" if sub else ""}</div></div>')
    js(f'tl.fromTo("#{wid}", {{x: 1900, rotation: -12}}, {{x: 0, rotation: -12, duration: .26, ease: "expo.in", immediateRender: false}}, {t - .26:.3f});')
    js(f'tl.to("#{wid}", {{x: -2000, duration: .3, ease: "expo.in"}}, {t + .16:.3f});')
    js(f'tl.fromTo("#{wid}l", {{x: 90, scale: .9}}, {{x: -160, scale: 1.05, duration: .72, ease: "none", immediateRender: false}}, {t - .26:.3f});')
    sfx("whoosh_big", t - .26)


def theme(t, cols, d=.6):
    for k, c in enumerate(cols):
        js(f'tl.to(".g{k + 1}", {{backgroundColor: "{c}", duration: {d}, ease: "power1.inOut"}}, {t:.3f});')


WARM = ("rgba(255,120,110,.55)", "rgba(255,170,120,.5)", "rgba(255,90,140,.3)")
COOL = ("rgba(120,150,255,.55)", "rgba(150,120,255,.5)", "rgba(110,200,255,.3)")
PINK = ("rgba(255,140,190,.55)", "rgba(200,120,255,.5)", "rgba(255,180,200,.3)")


# ---------------------------------------------------------------- v7 lively motion: FX layer, illustrated creator, 3D phone
FXH = []          # elements of the FX layer (bursts, confetti, hearts), above the scenes
PAL = ["#ff2a2a", "#ff3d7f", "#d02cff", "#6a1fe0", "#3346ff", "#2a7bff", "#ffb800", "#2fd28a"]
_fxn = [0]


def _fid(p):
    _fxn[0] += 1
    return f"{p}{_fxn[0]}"


def burst(x, y, t, color=RED, n=12, r0=40, r1=170, sfx_kind=None):
    """Radial speed lines + a shockwave ring + a few dots flying out."""
    bid = _fid("bu")
    lines = "".join(f'<line x1="{math.cos(a) * r0:.0f}" y1="{math.sin(a) * r0:.0f}" x2="{math.cos(a) * r1:.0f}" y2="{math.sin(a) * r1:.0f}" pathLength="100"/>'
                    for a in [i * 2 * math.pi / n + .2 for i in range(n)])
    FXH.append(f'<svg class="bur" id="{bid}" style="left:{x - 200}px;top:{y - 200}px;stroke:{color}" viewBox="-200 -200 400 400">{lines}'
               f'<circle class="shw" id="{bid}r" r="60"/></svg>')
    js(f'tl.fromTo("#{bid}", {{opacity: 1}}, {{opacity: 0, duration: .5, ease: "power2.in", immediateRender: false}}, {t + .15:.3f});')
    js(f'tl.set("#{bid}", {{opacity: 1}}, {t:.3f});')
    js(f'tl.fromTo("#{bid} line", {{strokeDashoffset: 100, scale: .6, transformOrigin: "0px 0px"}}, {{strokeDashoffset: -100, scale: 1.25, transformOrigin: "0px 0px", duration: .55, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#{bid}r", {{scale: .2, opacity: .9, transformOrigin: "0px 0px"}}, {{scale: 3, opacity: 0, transformOrigin: "0px 0px", duration: .6, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    if sfx_kind:
        sfx(sfx_kind, t)


def confetti(x, y, t, n=26, spread=520, seed=0):
    rnd = random.Random(seed + int(t * 100))
    for k in range(n):
        cid = _fid("cf")
        w, h = rnd.randint(14, 24), rnd.randint(8, 14)
        col = rnd.choice(PAL)
        shape = "border-radius:50%;" if rnd.random() < .3 else "border-radius:3px;"
        FXH.append(f'<i class="cf" id="{cid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{col};{shape}"></i>')
        ang = rnd.uniform(-math.pi * .95, -math.pi * .05)
        sp = rnd.uniform(.35, 1) * spread
        ex, ey = math.cos(ang) * sp, math.sin(ang) * sp
        rot = rnd.uniform(-540, 540)
        js(f'tl.fromTo("#{cid}", {{opacity: 1, x: 0, y: 0, rotation: 0, scale: .4}}, {{opacity: 1, x: {ex:.0f}, y: {ey:.0f}, rotation: {rot * .4:.0f}, scale: 1, duration: .45, ease: "expo.out", immediateRender: false}}, {t:.3f});')
        js(f'tl.to("#{cid}", {{x: {ex * 1.25:.0f}, y: {ey + rnd.uniform(380, 640):.0f}, rotation: {rot:.0f}, opacity: 0, duration: {rnd.uniform(.9, 1.3):.2f}, ease: "power1.in"}}, {t + .45:.3f});')
    sfx("sparkle", t)


def hearts(x, y, t0, t1, n=6, seed=1):
    """Hearts rising from a like button, one after another, while the reel plays."""
    rnd = random.Random(seed)
    k = 0
    t = t0
    while t < t1:
        hid = _fid("ht")
        col = rnd.choice(["#ff2a2a", "#ff3d7f", "#ff6b9a", "#d02cff"])
        FXH.append(f'<svg class="hrt" id="{hid}" style="left:{x}px;top:{y}px" viewBox="0 0 24 24"><path fill="{col}" d="M12 21s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 8.1a4.3 4.3 0 0 1 7.5 2.7C19.5 16.4 12 21 12 21z"/></svg>')
        dx = rnd.uniform(-70, 30)
        js(f'tl.fromTo("#{hid}", {{opacity: 0, y: 0, x: 0, scale: .4, rotation: 0}}, {{keyframes: {{opacity: [0, 1, 1, 0], y: [0, -90, -200, -300], x: [0, {dx * .4:.0f}, {dx:.0f}, {dx * .6:.0f}], scale: [.4, 1.1, 1, .9], rotation: [0, -10, 12, -6]}}, duration: 1.3, ease: "none", immediateRender: false}}, {t:.3f});')
        t += rnd.uniform(.22, .38)
        k += 1


def float_idle(sel, t, dur=10, amp=14, tilt=4, period=1.8):
    reps = max(1, int(dur / period))
    js(f'tl.fromTo("{sel}", {{y: 0, rotationX: {-tilt * .6:.1f}, rotationY: {-tilt:.1f}, transformPerspective: 1200}}, {{y: {-amp}, rotationX: {tilt * .6:.1f}, rotationY: {tilt:.1f}, transformPerspective: 1200, duration: {period}, repeat: {reps}, yoyo: true, ease: "sine.inOut", immediateRender: false}}, {t:.3f});')


def creator(cid, shirt=("#ff7a8a", "#ff3d7f"), wave=False, bg=None):
    """A flat illustrated creator (head, hair, blinking eyes, talking mouth, cheeks, shirt, a waving arm)."""
    g = f'<linearGradient id="{cid}sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shirt[0]}"/><stop offset="1" stop-color="{shirt[1]}"/></linearGradient>'
    arm = (f'<g id="{cid}_arm"><path d="M232 330 C250 300 268 262 278 222" stroke="url(#{cid}sh)" stroke-width="40" stroke-linecap="round" fill="none"/>'
           f'<circle cx="280" cy="200" r="25" fill="#f2b896"/><path d="M262 185 l-6 -22 M276 178 l-2 -24 M290 180 l4 -22" stroke="#f2b896" stroke-width="11" stroke-linecap="round"/></g>') if wave else ""
    return (f'<svg class="crt" id="{cid}" viewBox="0 0 300 420" preserveAspectRatio="xMidYMax meet"><defs>{g}</defs>'
            f'<path d="M30 420 C30 330 85 292 150 292 C215 292 270 330 270 420 Z" fill="url(#{cid}sh)"/>'
            f'<rect x="133" y="250" width="34" height="52" rx="14" fill="#e9a987"/>'
            f'<circle cx="80" cy="205" r="15" fill="#f2b896"/><circle cx="220" cy="205" r="15" fill="#f2b896"/>'
            f'<ellipse cx="150" cy="200" rx="70" ry="80" fill="#f6c3a1"/>'
            f'<path d="M76 210 C66 122 118 104 152 106 C206 104 238 140 226 210 C214 168 190 150 150 152 C112 152 90 168 76 210Z" fill="#2b2140"/>'
            f'<g id="{cid}_eyes"><ellipse cx="125" cy="206" rx="8" ry="11" fill="#2b2140"/><ellipse cx="175" cy="206" rx="8" ry="11" fill="#2b2140"/></g>'
            f'<path d="M112 186 q12 -8 24 -2 M164 184 q12 -6 24 2" stroke="#2b2140" stroke-width="5" stroke-linecap="round" fill="none"/>'
            f'<circle cx="108" cy="234" r="11" fill="#ff8fa0" opacity=".55"/><circle cx="192" cy="234" r="11" fill="#ff8fa0" opacity=".55"/>'
            f'<ellipse id="{cid}_mouth" cx="150" cy="246" rx="16" ry="9" fill="#8a2b3b"/>{arm}</svg>')


def creator_live(cid, t0, t1, talk=True, wave=False, seed=0):
    rnd = random.Random(seed)
    t = t0 + rnd.uniform(.3, .9)
    while t < t1:
        js(f'tl.fromTo("#{cid}_eyes", {{scaleY: 1, transformOrigin: "50% 50%"}}, {{keyframes: {{scaleY: [1, .08, 1]}}, duration: .16, ease: "none", immediateRender: false}}, {t:.3f});')
        t += rnd.uniform(1.4, 2.4)
    if talk:
        reps = max(1, int((t1 - t0) / .18))
        js(f'tl.fromTo("#{cid}_mouth", {{scaleY: .5, scaleX: 1, transformOrigin: "50% 50%"}}, {{scaleY: 1.6, scaleX: .85, transformOrigin: "50% 50%", duration: .09, repeat: {reps}, yoyo: true, ease: "sine.inOut", immediateRender: false}}, {t0:.3f});')
    if wave:
        reps = max(1, int((t1 - t0) / .28))
        js(f'tl.fromTo("#{cid}_arm", {{rotation: -14, svgOrigin: "232 330"}}, {{rotation: 16, svgOrigin: "232 330", duration: .28, repeat: {reps}, yoyo: true, ease: "sine.inOut", immediateRender: false}}, {t0:.3f});')


def shapes_html():
    """Glossy floating shapes behind everything: spheres, rings, squiggles, sparkles; they drift and spin in parallax."""
    items = [("sph", 120, 160, 150, "#ff9ab0", "#d02cff"), ("ring", 880, 120, 150, "#6a1fe0", "#2a7bff"), ("sqg", 560, 1640, 220, "#ff3d7f", "#ffb800"),
             ("spk", 170, 1420, 90, "#ffb800", "#ff3d7f"), ("sph", 900, 1180, 110, "#8fd0ff", "#3346ff"), ("spk", 930, 620, 70, "#d02cff", "#ff3d7f"),
             ("ring", 40, 1640, 120, "#ff3d7f", "#ffb800"), ("sph", 520, 1700, 90, "#b6f0a0", "#2fd28a"), ("sqg", 840, 1500, 170, "#6a1fe0", "#ff3d7f")]
    out = []
    for k, (kind, x, y, s, c1, c2) in enumerate(items):
        sid = f"shp{k}"
        if kind == "sph":
            out.append(f'<i class="shp sph" id="{sid}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:radial-gradient(circle at 32% 28%, #fff 0%, {c1} 34%, {c2} 100%)"></i>')
        elif kind == "ring":
            out.append(f'<svg class="shp" id="{sid}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px" viewBox="0 0 100 100"><defs><linearGradient id="{sid}g"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
                       f'<circle cx="50" cy="50" r="38" fill="none" stroke="url(#{sid}g)" stroke-width="13"/></svg>')
        elif kind == "sqg":
            out.append(f'<svg class="shp" id="{sid}" style="left:{x}px;top:{y}px;width:{s}px;height:{s * .5:.0f}px" viewBox="0 0 200 100"><defs><linearGradient id="{sid}g"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
                       f'<path d="M10 60 Q35 10 60 55 T110 55 T160 55 T190 40" fill="none" stroke="url(#{sid}g)" stroke-width="16" stroke-linecap="round"/></svg>')
        else:
            out.append(f'<svg class="shp" id="{sid}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px" viewBox="0 0 100 100"><defs><linearGradient id="{sid}g"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
                       f'<path d="M50 0 C54 36 64 46 100 50 C64 54 54 64 50 100 C46 64 36 54 0 50 C36 46 46 36 50 0Z" fill="url(#{sid}g)"/></svg>')
        rnd = random.Random(k)
        per = rnd.uniform(3.2, 5.5)
        reps = int(DUR / per) + 1
        js(f'tl.fromTo("#{sid}", {{x: 0, y: 0, rotation: 0}}, {{x: {rnd.uniform(-60, 60):.0f}, y: {rnd.uniform(-90, -40):.0f}, rotation: {rnd.choice([-1, 1]) * rnd.uniform(40, 120):.0f}, duration: {per:.2f}, repeat: {reps}, yoyo: true, ease: "sine.inOut", immediateRender: false}}, 0);')
    return f'<div id="shapes">{"".join(out)}</div>'


# ================================================================= the reel
PH, WY, VY = 330, 800, 1060      # phrase top, wheel centre, visual zone top (to ~1500)


def card(cid, x, y, w, h, inner, cls="", extra=""):
    return (f'<div class="cw" id="{cid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">'
            f'<div class="card {cls}" id="{cid}_c">{inner}<i class="sheen" id="{cid}_sh"></i></div></div>')


def card_in(sel, t, d=.6, dy=140):
    js(f'tl.fromTo("{sel}", {{opacity: 0, y: {dy}, scale: .7, rotation: {R.choice([-6, 6])}}}, {{opacity: 1, y: 0, scale: 1, rotation: 0, duration: {d}, ease: "back.out(1.5)", immediateRender: false}}, {t:.3f});')
    float_idle(f"{sel}_c", t + .2)
    js(f'tl.fromTo("{sel}_sh", {{xPercent: -180, opacity: 1}}, {{xPercent: 320, opacity: 1, duration: .9, ease: "power2.inOut", immediateRender: false}}, {t + .35:.3f});')
    js(f'tl.set("{sel}_sh", {{opacity: 0}}, {t + 1.27:.3f});')
    sfx("pop", t + .05)


def card_out(sel, t, d=.3):
    js(f'tl.to("{sel}", {{opacity: 0, y: -70, duration: {d}, ease: "expo.in"}}, {t:.3f});')


def draw(sel, t, d, ease="power2.inOut"):
    js(f'tl.fromTo("{sel}", {{strokeDashoffset: 1000}}, {{strokeDashoffset: 0, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def popin(sel, t, d=.35, sc=.6):
    js(f'tl.fromTo("{sel}", {{opacity: 0, scale: {sc}}}, {{opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.2)", immediateRender: false}}, {t:.3f});')


def person(cls=""):
    return f'<div class="person {cls}"><i class="hd"></i><i class="bd"></i></div>'


def reel_ui(rid, cls="", caption=True, side=True, bar=True, extra="", crt=None):
    side_ = ('<div class="side">' + "".join(f'<span>{icon(n, "sic")}<b>{c}</b></span>' for n, c in [("heart", "1.2K"), ("chat", "86"), ("send", "41")]) + "</div>") if side else ""
    cap = '<div class="capl"><i class="av"></i><i class="cl1"></i><i class="cl2"></i></div>' if caption else ""
    br = f'<div class="pbar"><i class="pfill" id="{rid}pb"></i></div>' if bar else ""
    who = crt if crt is not None else person()
    return f'<div class="reel {cls}" id="{rid}">{who}{extra}{side_}{cap}{br}</div>'


def scenes():
    H = []

    # ---- A: cold open. "This reel is about to lose you." + a phone playing a reel that gets flicked away
    t_a_out = L("l00", 6, "t1") + .02
    rows = [("xl", "This reel"), ("xl", "is about to"), ("xl", "*lose* *you.*")]
    ph = phrase("pA", "l00", rows, PH, first_visible=True)
    glitch = '<div class="glx" id="glxR">lose you.</div><div class="glx c" id="glxC">lose you.</div>'
    phone = (f'<div class="phone" id="phA"><div class="scr">{reel_ui("rA", crt=creator("crA"))}{reel_ui("rA2", "nx", crt=creator("crA2", ("#8fd0ff", "#3346ff")))}'
             f'<i class="gloss"></i><div class="thumb" id="thA"></div></div><i class="notch"></i><i class="btn b1"></i><i class="btn b2"></i></div>'
             f'<div class="vbub" id="vbA">{icon("play", "vbi")}<b id="vbAn">1,204</b><span>views</span><em>&#8595;</em></div>')
    H.append(scene("sA", ph + glitch + phone, shown=True))
    # the phone floats in 3D, turning slowly; the creator talks and blinks; hearts rise from the like button
    js(f'tl.fromTo("#phA", {{rotationY: -24, rotationX: 10, rotation: -6, y: 40, transformPerspective: 1400}}, {{rotationY: 14, rotationX: 4, rotation: 3, y: -10, transformPerspective: 1400, duration: {L("l00", 6) + .24:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#rApb", {{scaleX: .05}}, {{scaleX: .4, duration: {t_a_out:.2f}, ease: "none", immediateRender: false}}, 0);')
    creator_live("crA", 0, t_a_out, talk=True, seed=1)
    hearts(670, 1180, .1, L("l00", 5), seed=3)
    js(f'tl.fromTo("#vbA", {{opacity: 0, scale: .4, x: 60, rotation: 10}}, {{opacity: 1, scale: 1, x: 0, rotation: -4, duration: .45, ease: "back.out(2.4)", immediateRender: false}}, {L("l00", 2):.3f});')
    for i, v in enumerate(["1,204", "980", "702", "511", "388", "312"]):
        js(f'tl.set("#vbAn", {{textContent: "{v}"}}, {L("l00", 2) + .25 + i * .12:.3f});')
    sfx("pop", L("l00", 2))
    t_lose = L("l00", 5)
    for k, (dx, op) in enumerate([(14, .85), (-10, .7), (8, .9), (-16, .6), (0, 0)]):
        tt = t_lose + .03 + k * .05
        js(f'tl.set("#glxR", {{x: {dx}, opacity: {op}}}, {tt:.3f}); tl.set("#glxC", {{x: {-dx}, opacity: {op}}}, {tt:.3f});')
        js(f'tl.set("#pA_2_0, #pA_2_1", {{x: {R.choice([-6, 6, 0])}}}, {tt:.3f});')
    sfx("glitch", t_lose)
    popin("#thA", t_lose + .05, d=.2)
    t_fl = L("l00", 6) + .05
    js(f'tl.to("#thA", {{y: -330, opacity: 0, duration: .26, ease: "power3.in"}}, {t_fl - .1:.3f});')
    js(f'tl.to("#rA", {{yPercent: -100, duration: .28, ease: "power3.in"}}, {t_fl - .06:.3f});')
    js(f'tl.fromTo("#rA2", {{yPercent: 100, opacity: 1}}, {{yPercent: 0, opacity: 1, duration: .28, ease: "power3.in", immediateRender: false}}, {t_fl - .06:.3f});')
    # ...and the whole phone is flicked away, spinning off with a motion trail
    js(f'tl.to("#phA", {{x: 760, y: -520, rotation: 38, rotationY: 50, transformPerspective: 1400, duration: .42, ease: "power3.in"}}, {t_fl + .2:.3f});')
    js(f'tl.to("#vbA", {{x: -500, y: -300, rotation: -30, opacity: 0, duration: .38, ease: "power3.in"}}, {t_fl + .2:.3f});')
    burst(540, 1220, t_fl + .2, color="#ff3d7f")
    sfx("whoosh", t_fl)
    scene_out("sA", t_a_out, d=.26, dy=-420)
    sfx("hit", 0)

    # ---- B: "Your reel didn't flop because of the algorithm." Excuses wheel (with icons) + a post-insights card
    excuses = ["the hashtags", "your audio", "posting time", "shadowbans", "the algorithm", "the caption", "the thumbnail",
               "your niche", "trends", "the first 3 seconds"]
    icons_ = ["hash", "music", "clock", "eyeoff", "cpu", "lines", "image", "target", "trend", "timer"]
    gr = ["gr2"] * len(excuses)
    gr[-1] = "gr1"
    t_b = t_a_out + .12
    wB = Wheel("wB", excuses, WY, 104, start=0, grads=gr, icons=icons_)
    phB = phrase("pB", "l01", [("m", "Your reel didn't"), ("m", "=flop because of")], PH, t_out=L("l02", 0) - .12)
    sw_ = text_w("the algorithm", wB.size, 800, -.03) + 1.15 * wB.size
    strike = f'<i class="wstk" id="wBstk" style="width:{sw_ + 16:.0f}px;top:{WY - wB.size * .05:.0f}px;height:{wB.size * .09:.0f}px"></i>'
    spark = ('<svg class="spark" viewBox="0 0 300 120"><path class="sp-a" id="spBa" d="M0 12 C40 14 50 90 90 104 S200 112 300 114 L300 120 L0 120Z"/>'
             '<path class="sp-l" id="spBl" pathLength="1000" d="M0 12 C40 14 50 90 90 104 S200 112 300 114"/></svg>')
    ins = card("insB", 110, VY, 860, 380,
               f'<div class="ct">Post insights</div><div class="big"><b id="insBn">1,204</b><span>views</span></div>'
               f'<div class="pill red">&#8595; 97%</div>{spark}<div class="row"><span>Avg. watch time</span><b>0.9s</b></div>')
    H.append(scene("sB", phB + wB.html() + strike + ins))
    scene_in("sB", t_b)
    wB.appear(t_b + .05)
    card_in("#insB", t_b + .35)
    for i, v in enumerate(["1,204", "1,020", "840", "655", "480", "390", "312"]):
        js(f'tl.set("#insBn", {{textContent: "{v}"}}, {t_b + .55 + i * .09:.3f});')
    draw("#spBl", t_b + .6, 1.1)
    js(f'tl.fromTo("#spBa", {{opacity: 0}}, {{opacity: 1, duration: .8, immediateRender: false}}, {t_b + .9:.3f});')
    t_alg = L("l01", 7) - .02
    wB.move(t_b + .5, 2, 1.0, tick=False)
    wB.move(t_alg - .5, 4, .5)
    a_end = L("l01", 7, "t1")
    js(f'tl.fromTo("#wBstk", {{scaleX: 0, opacity: 1}}, {{scaleX: 1, opacity: 1, duration: .24, ease: "power3.inOut", immediateRender: false}}, {a_end - .12:.3f});')
    js(f'tl.to("#wB_4", {{opacity: .45, duration: .2}}, {a_end:.3f});')
    sfx("scratch", a_end - .1)

    # ---- C: "It flopped in the first three seconds." The wheel spins hard to "the first 3 seconds" (red)
    t_c = L("l02", 0) - .1
    phC = phrase("pC", "l02", [("m", "It flopped in")], PH, t_out=L("l02", 5) - .3)
    H.append(scene("sC", phC))
    js(f'tl.set("#sC", {{opacity: 1}}, {t_c - .02:.3f});')
    js(f'tl.to("#wBstk", {{opacity: 0, duration: .12}}, {t_c:.3f});')
    t_first = L("l02", 3)
    wB.move(t_c + .15, 9, t_first - t_c - .1, final_ease="back.out(2)")
    js(f'tl.fromTo("#wB_9", {{scale: 1}}, {{keyframes: {{scale: [1, 1.12, 1]}}, duration: .35, ease: "power2.out", immediateRender: false}}, {t_first + .05:.3f});')
    sfx("hit", t_first)
    t_cd = L("l02", 5) - .25
    scene_out("sB", t_cd, d=.24, dy=-300)
    js(f'tl.to("#sC", {{opacity: 0, duration: .2}}, {t_cd:.3f});')

    # ---- giant slot-machine digit inside a draining stopwatch ring: 3, 2, 1, 0 (red, dark flash, beat drop)
    flip_t = L("l02", 6, "t1") + .06
    c3 = t_cd + .12
    c2 = L("l02", 6) - .05
    c1 = (c2 + flip_t) / 2
    ring = ('<svg class="ring" viewBox="0 0 1000 1000"><circle class="rt" cx="500" cy="500" r="440"/>'
            '<circle class="rf" id="rfD" cx="500" cy="500" r="440" pathLength="1000" transform="rotate(-90 500 500)"/>'
            + "".join(f'<line class="tk" x1="500" y1="40" x2="500" y2="{70 if i % 5 else 90}" transform="rotate({i * 6} 500 500)"/>' for i in range(60))
            + '</svg>')
    H.append(scene("sD", ring + '<div class="bigm"><div class="bigs" id="bigs">' + "".join(f'<b class="bd{d}">{d}</b>' for d in (3, 2, 1, 0)) + '</div></div>'))
    js(f'tl.fromTo("#sD", {{opacity: 0, scale: .8}}, {{opacity: 1, scale: 1, duration: .3, ease: "expo.out", immediateRender: false}}, {c3:.3f});')
    js(f'tl.fromTo("#rfD", {{strokeDashoffset: 0}}, {{strokeDashoffset: 1000, duration: {flip_t - c3:.2f}, ease: "none", immediateRender: false}}, {c3:.3f});')
    js(f'tl.set("#rfD, .ring .rt", {{stroke: "{RED}"}}, {flip_t:.3f}); tl.set(".ring .tk", {{stroke: "rgba(255,255,255,.35)"}}, {flip_t:.3f});')
    sfx("hit", c3)
    for k, t in enumerate([c2, c1, flip_t]):
        js(f'tl.fromTo("#bigs", {{y: {-k * 900}}}, {{y: {-(k + 1) * 900}, duration: .2, ease: "back.out(1.4)", immediateRender: false}}, {t - .1:.3f});')
        blur_pulse("sD", t - .1, 30, .06, .14)
        sfx("count" if k < 2 else "glitch", t)
    burst(540, 970, flip_t, color=RED, n=16, r0=420, r1=620)
    js(f'tl.set("#flash", {{opacity: 1}}, {flip_t - .02:.3f}); tl.to("#flash", {{opacity: 0, duration: .45, ease: "power2.in"}}, {flip_t + .32:.3f});')
    js(f'tl.fromTo("#sD", {{scale: 1}}, {{scale: 1.08, duration: .3, ease: "power2.out", immediateRender: false}}, {flip_t:.3f});')
    t_e = L("l03", 0) - .14
    scene_out("sD", t_e - .05, d=.25, dy=-400)

    # ---- E: "Here are three mistakes killing your views." + a retention graph that falls off a cliff at 0:03
    phE = phrase("pE", "l03", [("s", "_Here _are"), ("xl", "*3 mistakes"), ("m", "*killing your views.")], PH, t_out=None)
    curve = "M40 40 C70 42 90 60 110 210 C125 300 150 318 220 322 S600 330 780 334"
    chart = (f'<svg class="chart" viewBox="0 0 820 380"><defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity=".35"/>'
             f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient></defs>'
             + "".join(f'<line class="gl" x1="40" y1="{y}" x2="780" y2="{y}"/>' for y in (40, 140, 240, 340))
             + f'<line class="m3" id="m3E" x1="110" y1="20" x2="110" y2="350"/>'
             f'<path class="ar" id="arE" d="{curve} L780 340 L40 340Z" fill="url(#ga)"/>'
             f'<path class="ln" id="lnE" pathLength="1000" d="{curve}"/>'
             f'<circle class="dot" id="dotE" cx="110" cy="210" r="14"/>'
             + "".join(f'<text class="ax" x="{x}" y="376">{s}</text>' for x, s in [(40, "0s"), (110, "3s"), (300, "10s"), (540, "20s"), (760, "30s")])
             + '</svg>')
    gcard = card("grE", 110, 760, 860, 600, f'<div class="ct">Audience retention</div><div class="pill red tr" id="pillE">&#8595; 97% by 0:03</div>{chart}'
                 f'<div class="callout" id="coE"><i class="dotr"></i>viewers gone at 0:03</div>')
    H.append(scene("sE", phE + gcard))
    scene_in("sE", t_e)
    card_in("#grE", t_e + .2)
    draw("#lnE", t_e + .45, 1.0, "power1.inOut")
    js(f'tl.fromTo("#arE", {{opacity: 0}}, {{opacity: 1, duration: .6, immediateRender: false}}, {t_e + .9:.3f});')
    popin("#dotE", L("l03", 4) - .05)
    burst(240, 1080, L("l03", 4) - .05, color=RED, n=10, r0=20, r1=110)
    popin("#coE", L("l03", 4) + .05)
    popin("#pillE", L("l03", 6) - .05)
    js(f'tl.fromTo("#m3E", {{opacity: 0}}, {{opacity: 1, duration: .3, immediateRender: false}}, {L("l03", 4) - .1:.3f});')
    sfx("drop", L("l03", 4))
    t_f = L("l04", 0) - .14
    theme(t_e, WARM)
    wipe(t_f, "01", "THE GREETING")
    scene_out("sE", t_f - .04)

    # ---- F: the mistakes wheel + a reel card. "One: your hook is a greeting."
    mistakes = ["The greeting", "A still frame", "Explaining first"]
    wF = Wheel("wF", mistakes, WY, 112, start=0, grads=["gr1"] * 3, icons=["chat", "pause", "list"])
    lab = '<div class="lab" id="labF"><span id="labN">01</span> / 03</div>'
    phF = phrase("pF", "l04", [("s", "_One:"), ("m", "your hook is"), ("m", "a =greeting.")], PH, t_out=L("l05", 0) - .12)
    thumb = f'<div class="thn">{creator("crF", wave=True)}</div>'
    rc = card("rcF", 110, VY, 860, 400,
              f'{thumb}<div class="rcr"><div class="bub" id="bubF"><span id="bubFt"></span></div>'
              f'<div class="pbar2"><i class="pf2" id="pbF"></i><i class="mk3"></i><em>0:03</em></div>'
              f'<div class="row"><span>Watch time</span><b class="redt">0.4s</b></div></div><div class="thumb2" id="thF"></div>')
    H.append(scene("sF", lab + phF + wF.html() + rc))
    scene_in("sF", t_f)
    wF.appear(t_f + .05)
    card_in("#rcF", t_f + .3)
    creator_live("crF", t_f + .3, L("l05", 3) + .5, talk=True, wave=True, seed=4)
    js(f'tl.fromTo("#labF", {{opacity: 0, x: -30}}, {{opacity: 1, x: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {t_f + .1:.3f});')
    t_cap = L("l04", 5) - .15
    popin("#bubF", t_cap - .1)
    cap = "Hey guys, so today..."
    for i in range(1, len(cap) + 1):
        js(f'tl.set("#bubFt", {{textContent: {json.dumps(cap[:i])}}}, {t_cap + i * .03:.3f});')
        if i % 4 == 1:
            sfx("type", t_cap + i * .03)
    js(f'tl.fromTo("#pbF", {{scaleX: 0}}, {{scaleX: .04, duration: 2.0, ease: "none", immediateRender: false}}, {t_f + .5:.3f});')
    # "Nobody stays for 'Hey guys.'" : the wheel steps aside, the quote takes the middle, the thumb swipes the card away
    t_q = L("l05", 0) - .12
    phF2 = phrase("pF2", "l05", [("m", "Nobody stays for")], PH, t_out=L("l06", 0) - .12)
    quote = '<div class="quote" id="quote"><span id="qt">“Hey guys.”</span><i class="qstk" id="qstk"></i></div>'
    skip = '<div class="pill red big2" id="skipF">Skipped at 0:01</div>'
    H.append(scene("sF2", phF2 + quote + skip))
    js(f'tl.set("#sF2", {{opacity: 1}}, {t_q:.3f});')
    js(f'tl.to("#wF", {{opacity: 0, y: 160, duration: .3, ease: "expo.in"}}, {t_q:.3f});')
    blur_pulse("wF", t_q, 24, .3, .05)
    js(f'tl.fromTo("#quote", {{opacity: 0, scale: 1.3}}, {{opacity: 1, scale: 1, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l05", 3) - .08:.3f});')
    sfx("hit", L("l05", 3) - .05)
    js(f'tl.fromTo("#qstk", {{scaleX: 0}}, {{scaleX: 1, duration: .25, ease: "power3.inOut", immediateRender: false}}, {L("l05", 4, "t1") - .05:.3f});')
    js(f'tl.to("#qt", {{color: "#b9b9b9", duration: .2}}, {L("l05", 4, "t1"):.3f});')
    sfx("scratch", L("l05", 4, "t1") - .05)
    t_sw = L("l05", 3) + .1
    popin("#thF", t_sw - .25, d=.2)
    js(f'tl.to("#thF", {{y: -300, opacity: 0, duration: .3, ease: "power3.in"}}, {t_sw:.3f});')
    js(f'tl.to("#rcF", {{y: -260, opacity: 0, rotation: -4, duration: .38, ease: "power3.in"}}, {t_sw + .04:.3f});')
    blur_pulse("sF", t_sw + .04, 30, .3, .08)
    sfx("whoosh", t_sw)
    popin("#skipF", t_sw + .4)
    burst(540, 1270, t_sw + .4, color=RED, n=12, r0=200, r1=320)
    sfx("error", t_sw + .4)

    # "Start with the result." : the quote decodes into the result; a new reel card with the result and rising bars
    t_r = L("l06", 0) - .1
    theme(t_r, COOL)
    phF3 = phrase("pF3", "l06", [("m", "Start with the +result.")], PH, t_out=L("l07", 0) - .14)
    bars = "".join(f'<i class="bar" id="brF{k}" style="left:{k * 66}px;height:{h}px"></i>' for k, h in enumerate([60, 96, 140, 190, 250]))
    rc2 = card("rc2F", 110, VY, 860, 400,
               f'<div class="thn dark">{creator("crF2", ("#ffd29e", "#ff9fb2"))}<div class="thres">1M<br><small>views</small></div></div>'
               f'<div class="rcr"><div class="ct">Views</div><div class="bars">{bars}</div>'
               f'<div class="pill blue" id="keptF">{icon("check", "pic")}still watching past 0:03</div></div>')
    H.append(scene("sF3", phF3 + rc2))
    js(f'tl.set("#sF3", {{opacity: 1}}, {t_r:.3f});')
    js(f'tl.to("#qstk, #skipF", {{opacity: 0, duration: .15}}, {t_r:.3f});')
    target = "1M views in 3 days."
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&"
    n = 14
    for k in range(n + 1):
        f = k / n
        s_ = "".join(c if (i / len(target) < f or c == " ") else R.choice(chars) for i, c in enumerate(target))
        js(f'tl.set("#qt", {{textContent: {json.dumps(s_)}}}, {t_r + .05 + k * .045:.3f});')
        if k % 3 == 0:
            sfx("type", t_r + .05 + k * .045)
    js(f'tl.to("#qt", {{color: "{INK}", duration: .15}}, {t_r:.3f});')
    t_res = t_r + .05 + n * .045
    H.append('<div class="quote res" id="qres" style="opacity:0"><span class="gr2">1M views in 3 days.</span></div>')
    js(f'tl.set("#qres", {{opacity: 1}}, {t_res:.3f}); tl.set("#qt", {{opacity: 0}}, {t_res:.3f});')
    js(f'tl.fromTo("#qres", {{scale: 1.08}}, {{scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false}}, {t_res:.3f});')
    sfx("ding", t_res)
    card_in("#rc2F", t_r + .15)
    for k in range(5):
        js(f'tl.fromTo("#brF{k}", {{scaleY: 0}}, {{scaleY: 1, duration: .45, ease: "back.out(1.6)", immediateRender: false}}, {t_r + .4 + k * .07:.3f});')
    popin("#keptF", t_res + .1)
    creator_live("crF2", t_r + .15, t_res + 1.2, talk=True, seed=6)
    confetti(560, 1180, t_res, n=28)
    t_g = L("l07", 0) - .14
    js(f'tl.to("#quote, #qres", {{opacity: 0, y: -120, duration: .22, ease: "expo.in"}}, {t_g - .3:.3f});')
    blur_pulse("sF2", t_g - .3, 24, .22, .05)
    card_out("#rc2F", t_g - .3)

    # ---- G: "Two: your first frame is still. If nothing moves, thumbs keep scrolling." A still photo, then a feed whips past
    wipe(t_g, "02", "A STILL FRAME")
    theme(t_g, WARM)
    phG = phrase("pG", "l07", [("s", "_Two:"), ("m", "your first frame"), ("m", "is =still.")], PH, t_out=L("l08", 0) - .12)
    photo = ('<div class="fcard photo"><i class="sun"></i><i class="h1"></i><i class="h2"></i>'
             f'<div class="pz" id="pzG">{icon("pause", "pzi")}</div><div class="chip" id="chG">frame 1</div>'
             '<div class="pill red nm" id="nmG">nothing moves</div></div>')
    shirts = {1: ("#ffd29e", "#ff9f43"), 2: ("#8fd0ff", "#3346ff"), 3: ("#c9a7ff", "#6a1fe0")}
    others = "".join(f'<div class="fcard o{k}">{creator(f"crG{k}", shirts[k])}</div>' for k in (1, 2, 3))
    feed = card("feedG", 110, VY, 860, 420, f'<div class="fstrip" id="fsG">{photo}{others}</div>', cls="feed")
    H.append(scene("sG", phG + feed))
    js(f'tl.set("#sG", {{opacity: 1}}, {t_g:.3f});')
    js(f'tl.to("#wF", {{opacity: 1, y: 0, duration: .4, ease: "expo.out"}}, {t_g + .05:.3f});')
    card_in("#feedG", t_g + .1)
    wF.move(t_g + .2, 1, .45)
    js(f'tl.set("#labN", {{textContent: "02"}}, {t_g + .4:.3f});')
    popin("#pzG", L("l07", 5) - .05)
    popin("#chG", L("l07", 3))
    sfx("click", L("l07", 5))
    t_h = L("l08", 0) - .1
    phH = phrase("pH", "l08", [("m", "If nothing moves,"), ("m", "thumbs keep =scrolling.")], PH, t_out=L("l09", 0) - .12)
    H.append(scene("sH", phH))
    js(f'tl.set("#sH", {{opacity: 1}}, {t_h:.3f});')
    popin("#nmG", L("l08", 1))
    sfx("alert", L("l08", 1))
    t_sc = L("l08", 3)
    js(f'tl.to("#wF", {{y: -900, opacity: 0, duration: .5, ease: "power3.in"}}, {t_sc:.3f});')
    blur_pulse("wF", t_sc, 40, .4, .1)
    js(f'tl.to("#fsG", {{y: -3 * 440, duration: .9, ease: "expo.inOut"}}, {t_sc:.3f});')
    blur_pulse("sG", t_sc + .1, 36, .3, .4)
    sfx("whoosh", t_sc + .05)
    sfx("swish", t_sc + .4)

    # ---- I: "Three: you explain before you show." / "Show the result first, then explain how you got it."
    t_i = L("l09", 0) - .12
    wipe(t_i, "03", "EXPLAINING FIRST")
    card_out("#feedG", t_i - .02)
    phI = phrase("pI", "l09", [("s", "_Three:"), ("m", "you explain"), ("m", "before you =show.")], PH, t_out=L("l10", 0) - .12)
    sw = vblur("swp")
    swap = (f'<div id="swp" style="filter:{sw}"><div class="sw2" id="swE"><span class="n">1</span>{icon("list", "ic2")}EXPLAIN</div>'
            f'<div class="sw2" id="swS"><span class="n">2</span>{icon("play", "ic2")}<span class="t">SHOW<span class="g gr1" id="swSg">SHOW</span></span></div></div>')
    tl_ = (f'<div class="tlt"><i class="z3"></i><em class="zl">first 3 seconds</em>'
           f'<div class="blk ex" id="bkE">EXPLAIN</div><div class="blk sh" id="bkS">SHOW</div>'
           f'<i class="lv" id="lvI"></i><div class="lvl" id="lvlI"><i class="dotr"></i>viewer leaves</div>'
           + "".join(f'<span class="tx" style="left:{40 + x * 26}px">{x}s</span>' for x in (0, 3, 10, 20, 30)) + '</div>')
    tcard = card("tlI", 110, 1110, 860, 360, f'<div class="ct">Your first 30 seconds</div>{tl_}')
    H.append(scene("sI", phI + swap + tcard))
    js(f'tl.set("#sI", {{opacity: 1}}, {t_i:.3f});')
    js(f'tl.set("#labN", {{textContent: "03"}}, {t_i:.3f});')
    card_in("#tlI", t_i + .1)
    js(f'tl.fromTo("#swE", {{opacity: 0, yPercent: 60}}, {{opacity: 1, yPercent: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l09", 2) - .05:.3f});')
    js(f'tl.fromTo("#swS", {{opacity: 0, yPercent: 60}}, {{opacity: .35, yPercent: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l09", 5) - .05:.3f});')
    js(f'tl.fromTo("#bkE", {{scaleX: 0, opacity: 1}}, {{scaleX: 1, opacity: 1, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l09", 2):.3f});')
    js(f'tl.fromTo("#bkS", {{scaleX: 0, opacity: 1}}, {{scaleX: 1, opacity: 1, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l09", 5):.3f});')
    popin("#lvI", L("l09", 5) + .15)
    popin("#lvlI", L("l09", 5) + .2)
    sfx("tick", L("l09", 2))
    sfx("error", L("l09", 5) + .2)
    t_sw = L("l10", 0) - .05
    theme(t_sw, COOL)
    phI2 = phrase("pI2", "l10", [("m", "Show the result"), ("m", "+first,"), ("s", "_then _explain _how _you _got _it.")], PH)
    H.append(scene("sI2", phI2))
    js(f'tl.set("#sI2", {{opacity: 1}}, {t_sw - .05:.3f});')
    js(f'tl.to("#swS", {{y: -190, opacity: 1, duration: .5, ease: "expo.inOut"}}, {t_sw:.3f});')
    js(f'tl.to("#swE", {{y: 190, opacity: .35, duration: .5, ease: "expo.inOut"}}, {t_sw:.3f});')
    js(f'tl.set("#swS .n", {{textContent: "1"}}, {t_sw + .25:.3f}); tl.set("#swE .n", {{textContent: "2"}}, {t_sw + .25:.3f});')
    js(f'tl.to("#swSg", {{opacity: 1, duration: .25}}, {t_sw + .3:.3f});')
    # on the timeline the blocks swap: SHOW now sits inside the first 3 seconds, the viewer stays
    js(f'tl.to("#bkS", {{x: -234, duration: .55, ease: "expo.inOut"}}, {t_sw + .1:.3f});')
    js(f'tl.to("#bkE", {{x: 130, duration: .55, ease: "expo.inOut"}}, {t_sw + .1:.3f});')
    js(f'tl.to("#lvI, #lvlI", {{opacity: 0, duration: .2}}, {t_sw + .1:.3f});')
    blur_pulse("swp", t_sw, 22, .2, .3)
    sfx("swish", t_sw)
    sfx("success", t_sw + .5)
    burst(330, 760, t_sw + .5, color="#ff3d7f", n=12, r0=120, r1=260)
    t_j = L("l11", 0) - .14
    scene_out("sI", t_j - .04)
    js(f'tl.to("#sI2, #sF", {{opacity: 0, duration: .2}}, {t_j - .04:.3f});')

    # ---- J: "Fix these three and watch your next reel." Fixes wheel with checks; a rising chart; the odometer
    wipe(t_j, "THE FIX", "", grad=("#3346ff", "#6a1fe0", "#d02cff"))
    fixes = ["Result first", "Move in frame 1", "Show, then explain"]
    wJ = Wheel("wJ", fixes, WY, 112, start=0, grads=["gr2"] * 3, icons=["check"] * 3)
    phJ = phrase("pJ", "l11", [("m", "*Fix these three"), ("s", "_and _watch _your _next _reel.")], PH)
    up = "M40 330 C140 320 200 300 280 250 S440 150 540 120 S700 50 780 40"
    upc = (f'<svg class="chart" viewBox="0 0 820 380"><defs><linearGradient id="gb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3346ff" stop-opacity=".3"/>'
           f'<stop offset="1" stop-color="#3346ff" stop-opacity="0"/></linearGradient></defs>'
           + "".join(f'<line class="gl" x1="40" y1="{y}" x2="780" y2="{y}"/>' for y in (40, 140, 240, 340))
           + f'<path id="arJ" d="{up} L780 340 L40 340Z" fill="url(#gb)"/><path class="ln blue" id="lnJ" pathLength="1000" d="{up}"/></svg>')
    od = Odometer("odo", "  ,312", "48,200", 1000, 200, 0)
    ccard = card("chJ", 110, VY, 860, 430, f'<div class="ct">Your next reel</div><div class="pill blue tr">&#8593; views</div>{upc}')
    H.append(scene("sJ", phJ + wJ.html() + od.html() + '<div class="odl" id="odl">views</div>' + ccard))
    scene_in("sJ", t_j)
    wJ.appear(t_j + .05)
    card_in("#chJ", t_j + .3)
    wJ.move(L("l11", 1), 1, .3)
    wJ.move(L("l11", 2) + .05, 2, .3)
    for k in range(3):
        sfx("pop", [t_j + .3, L("l11", 1) + .3, L("l11", 2) + .35][k])
    t_o = L("l11", 4) - .1
    js(f'tl.to("#wJ", {{opacity: 0, y: -120, duration: .3, ease: "expo.in"}}, {t_o - .1:.3f});')
    blur_pulse("wJ", t_o - .1, 24, .3, .05)
    js(f'tl.fromTo("#odo, #odl", {{opacity: 0, y: 60}}, {{opacity: 1, y: -280, duration: .45, ease: "expo.out", immediateRender: false}}, {t_o:.3f});')
    od.roll(t_o + .2, 1.1)
    draw("#lnJ", t_o + .2, 1.1)
    js(f'tl.fromTo("#arJ", {{opacity: 0}}, {{opacity: 1, duration: .8, immediateRender: false}}, {t_o + .6:.3f});')
    sfx("rise", t_o + .2)
    sfx("ding", t_o + 1.3)
    confetti(540, 760, t_o + 1.25, n=30, seed=9)

    # ---- K: CTA. "Save this so you don't forget, and comment HOOK for my list of twenty hooks that work."
    t_k = L("l12", 0) - .14
    wipe(t_k, "SAVE THIS", "", grad=("#ff3d7f", "#d02cff", "#6a1fe0"))
    theme(t_k, PINK)
    scene_out("sJ", t_k - .04)
    kw = ["GUIDE", "LINK", "TIPS", "SEND", "HOOK"]
    wK = Wheel("wK", kw, WY + 110, 150, start=0, grads=["gr1"] * 5)
    phK = phrase("pK", "l12", [("m", "=Save this so you"), ("m", "don't forget,")], PH, t_out=L("l12", 6) - .1)
    phK2 = phrase("pK2", "l12", [("m", "and comment")], PH, start=6)
    phK3 = phrase("pK3", "l12", [("s", "_for _my _list _of _20 _hooks _that _work.")], 1400, start=9)
    bk = f'<div class="bkm" id="bkm">{icon("bookmark", "bki")}</div>'
    cbox = card("cbK", 110, 1190, 860, 170,
                f'<i class="av2"></i><div class="inp"><span id="cbph">Add a comment...</span><span id="cbk"></span><i id="caret"></i></div>'
                f'<div class="snd" id="sndK">{icon("send", "sdi")}</div>')
    H.append(scene("sK", phK + phK2 + wK.html() + cbox + phK3 + bk))
    scene_in("sK", t_k)
    js(f'tl.fromTo("#bkm", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .4, ease: "back.out(2)", immediateRender: false}}, {L("l12", 0):.3f});')
    js(f'tl.to("#bkm .bki", {{fill: "{INK}", duration: .15}}, {L("l12", 1):.3f});')
    js(f'tl.to("#bkm", {{opacity: 0, duration: .2}}, {L("l12", 6) - .1:.3f});')
    sfx("pop", L("l12", 0))
    card_in("#cbK", L("l12", 2))
    wK.appear(L("l12", 6) - .05)
    t_hook = L("l12", 8)
    wK.move(L("l12", 7) - .05, 4, t_hook - L("l12", 7) + .05, final_ease="back.out(2.2)")
    js(f'tl.fromTo("#wK_4", {{scale: 1}}, {{keyframes: {{scale: [1, 1.1, 1]}}, duration: .4, ease: "power2.out", immediateRender: false}}, {t_hook + .05:.3f});')
    sfx("hit", t_hook)
    burst(330, WY + 110, t_hook + .02, color="#ff3d7f", n=14, r0=150, r1=300)
    confetti(330, WY + 110, t_hook + .05, n=34, seed=12)
    hearts(880, 1250, t_hook + .5, DUR - .6, seed=8)
    js(f'tl.set("#cbph", {{display: "none"}}, {t_hook - .05:.3f});')
    for i, s_ in enumerate(["H", "HO", "HOO", "HOOK"]):
        js(f'tl.set("#cbk", {{textContent: "{s_}"}}, {t_hook + i * .08:.3f});')
        sfx("type", t_hook + i * .08)
    js(f'tl.to("#sndK", {{backgroundColor: "{RED}", duration: .2}}, {t_hook + .4:.3f}); tl.to("#sndK .sdi", {{stroke: "#ffffff", duration: .2}}, {t_hook + .4:.3f});')
    return "".join(H), od



CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #f4f4f1; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter"; color: {INK}; background: #f4f4f1; }}
.fx {{ position: absolute; width: 0; height: 0; }}
/* the ground: soft white with drifting pastel glows, like the reference */
#bg {{ position: absolute; inset: 0; background: radial-gradient(120% 80% at 50% 40%, #fbfbf9 0%, #f2f2ee 60%, #e9e9e4 100%); }}
.glow {{ position: absolute; border-radius: 50%; filter: blur(110px); }}
.g1 {{ width: 900px; height: 900px; left: -380px; top: -260px; background: rgba(176,206,120,.55); }}
.g2 {{ width: 980px; height: 980px; left: 420px; top: 1160px; background: rgba(240,150,170,.5); }}
.g3 {{ width: 700px; height: 700px; left: 560px; top: 260px; background: rgba(255,190,200,.28); }}
#grain {{ position: absolute; inset: 0; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: multiply; }}
#flash {{ position: absolute; inset: 0; background: radial-gradient(90% 60% at 50% 50%, #1d1d1d, #050505); opacity: 0; z-index: 2; }}
.scn {{ position: absolute; inset: 0; opacity: 0; z-index: 3; }}
/* phrases */
.ph {{ position: absolute; right: 80px; }}
.ln {{ white-space: nowrap; line-height: 1.08; }}
.ln.xl, .ln.l {{ letter-spacing: -.035em; line-height: 1.0; }}
.ln.m {{ letter-spacing: -.025em; }}
.wm {{ display: inline-block; overflow: hidden; vertical-align: top; padding: 0 .02em .1em; margin: 0 .2em -.1em 0; }}
.w {{ display: inline-block; opacity: 0; position: relative; }}
.grey {{ color: #66665f; }}
.gr1, .gr2 {{ background-clip: text; -webkit-background-clip: text; color: transparent; -webkit-text-fill-color: transparent; }}
.gr1 {{ background-image: linear-gradient(90deg, #ff2a2a, #ff3d7f 70%, #d02cff); }}
.gr2 {{ background-image: linear-gradient(90deg, #6a1fe0, #3346ff 75%, #2a7bff); }}
.stk, .wstk, .qstk {{ position: absolute; left: -2%; width: 104%; top: 52%; height: .09em; border-radius: .05em; background: {RED}; transform-origin: left center; transform: scaleX(0); }}
.glx {{ position: absolute; left: {LEFT}px; top: 650px; font-size: 160px; font-weight: 800; letter-spacing: -.035em; color: rgba(255,0,60,.7); mix-blend-mode: multiply; opacity: 0; white-space: nowrap; }}
.glx.c {{ color: rgba(0,200,255,.7); }}
/* wheels */
.whl {{ position: absolute; inset: 0; }}
.wi {{ position: absolute; white-space: nowrap; line-height: 1.2; letter-spacing: -.03em; transform-origin: left center; opacity: 0; }}
.wi .b {{ color: {INK}; }}
.wi .g {{ position: absolute; left: 0; top: 0; opacity: 0; }}
.wstk {{ left: {LEFT - 8}px; z-index: 5; opacity: 0; }}
.lab {{ position: absolute; left: {LEFT}px; top: 262px; font-size: 34px; font-weight: 700; letter-spacing: .14em; color: #66665f; opacity: 0; }}
.lab span {{ color: {INK}; }}
/* the big digit */
.bigm {{ position: absolute; left: 0; right: 0; top: 520px; height: 900px; overflow: hidden; }}
.bigs {{ position: absolute; left: 0; right: 0; top: 0; }}
.bigs b {{ display: block; height: 900px; line-height: 900px; text-align: center; font-size: 820px; font-weight: 800; letter-spacing: -.05em; color: {INK}; }}
.bigs .bd2 {{ color: {INK}; }} .bigs .bd0 {{ color: {RED}; }}
/* quote */
.quote {{ position: absolute; left: {LEFT}px; right: 60px; top: 720px; font-size: 128px; font-weight: 800; letter-spacing: -.035em; white-space: nowrap; opacity: 0; }}
.quote.res {{ font-size: {int(MAXW / text_w("1M views in 3 days.", 1, 800, -.035))}px; z-index: 4; }}
.quote .qstk {{ width: 760px; left: -10px; top: 55%; height: 14px; }}
/* explain / show */
#swp {{ position: absolute; left: 0; right: 0; top: 690px; z-index: 3; }}
.sw2 {{ position: absolute; left: {LEFT}px; display: flex; align-items: center; gap: 34px; font-size: 150px; font-weight: 800; letter-spacing: -.04em; line-height: 1; opacity: 0; }}
#swE {{ top: 0; }} #swS {{ top: 190px; }}
.sw2 .n {{ width: 110px; height: 110px; border-radius: 50%; border: 6px solid currentColor; display: grid; place-items: center; font-size: 58px; letter-spacing: 0; }}
/* odometer */
.odo {{ position: absolute; right: 0; display: flex; justify-content: center; font-weight: 800; letter-spacing: -.04em; line-height: 1; opacity: 0; width: {FW}px; }}
.om {{ display: inline-block; height: 1em; overflow: hidden; position: relative; width: .62em; }}
.os {{ position: absolute; left: 0; top: 0; display: flex; flex-direction: column; }}
.os b {{ display: block; height: 1em; text-align: center; }}
.oc {{ display: inline-block; width: .3em; opacity: 0; }}
.sw2 .t {{ position: relative; }}
.sw2 .g {{ position: absolute; left: 0; top: 0; opacity: 0; }}
.odl {{ position: absolute; left: 0; right: 0; top: 1225px; text-align: center; font-size: 50px; font-weight: 600; color: #66665f; opacity: 0; }}

/* ---- v6 visuals: icons, glass cards, phone, charts, ring, feed, timeline, comment box */
.ic {{ width: .82em; height: .82em; margin-right: .3em; vertical-align: -.08em; fill: none; stroke: {INK}; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }}
.ic2 {{ width: 110px; height: 110px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
.card {{ position: absolute; opacity: 0; border-radius: 44px; background: rgba(255,255,255,.66); border: 1.5px solid rgba(255,255,255,.9);
  box-shadow: 0 40px 90px rgba(70,40,60,.14), 0 6px 18px rgba(0,0,0,.05); backdrop-filter: blur(22px); -webkit-backdrop-filter: blur(22px); overflow: hidden; z-index: 3; }}
.ct {{ position: absolute; left: 40px; top: 32px; font-size: 32px; font-weight: 700; color: #66665f; letter-spacing: -.01em; }}
.big {{ position: absolute; left: 40px; top: 84px; display: flex; align-items: baseline; gap: 14px; }}
.big b {{ font-size: 150px; font-weight: 800; letter-spacing: -.05em; line-height: 1; }}
.big span {{ font-size: 40px; font-weight: 700; color: #66665f; }}
.pill {{ position: absolute; display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px; border-radius: 999px; font-size: 30px; font-weight: 800; white-space: nowrap; }}
.pill.red {{ background: rgba(255,42,42,.12); color: {RED}; }}
.pill.blue {{ background: rgba(51,70,255,.1); color: #3346ff; }}
.insB .pill, #insB .pill {{ left: 44px; top: 260px; }}
.pill.tr {{ right: 36px; top: 26px; }}
.spark {{ position: absolute; right: 40px; top: 110px; width: 420px; height: 170px; overflow: visible; }}
.sp-l {{ fill: none; stroke: {RED}; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 1000; stroke-dashoffset: 1000; }}
.sp-a {{ fill: rgba(255,42,42,.12); opacity: 0; }}
.row {{ position: absolute; left: 40px; right: 40px; bottom: 28px; display: flex; justify-content: space-between; font-size: 30px; font-weight: 600; color: #66665f; }}
.row b {{ color: {INK}; font-weight: 800; }}
.redt {{ color: {RED} !important; }}
/* phone */
.phone {{ position: absolute; left: 320px; top: 870px; width: 440px; height: 650px; border-radius: 64px; background: linear-gradient(145deg, #2c2c2c, #0d0d0d); padding: 14px;
  box-shadow: 0 50px 100px rgba(40,20,40,.3); z-index: 3; }}
.scr {{ position: relative; width: 100%; height: 100%; border-radius: 52px; overflow: hidden; background: #333; }}
.notch {{ position: absolute; left: 50%; top: 26px; width: 120px; height: 34px; margin-left: -60px; border-radius: 20px; background: #000; z-index: 6; }}
.reel {{ position: absolute; inset: 0; background: linear-gradient(170deg, #ffb3c3 0%, #c9a7ff 55%, #8fa3ff 100%); }}
.reel.nx {{ background: linear-gradient(170deg, #c9e6a3, #8fd0c4 60%, #6aa6d9); opacity: 0; }}
.person .hd {{ position: absolute; left: 50%; top: 28%; width: 30%; height: 22%; margin-left: -15%; border-radius: 50%; background: rgba(255,255,255,.75); }}
.person .bd {{ position: absolute; left: 50%; top: 52%; width: 66%; height: 60%; margin-left: -33%; border-radius: 50% 50% 0 0; background: rgba(255,255,255,.6); }}
.side {{ position: absolute; right: 18px; bottom: 120px; display: flex; flex-direction: column; gap: 22px; align-items: center; }}
.side span {{ display: flex; flex-direction: column; align-items: center; gap: 2px; }}
.side b {{ font-size: 20px; color: #fff; font-weight: 800; text-shadow: 0 1px 6px rgba(0,0,0,.45); }}
.sic {{ width: 46px; height: 46px; fill: none; stroke: #fff; stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }}
.capl {{ position: absolute; left: 22px; bottom: 50px; width: 70%; }}
.capl .av {{ display: block; width: 44px; height: 44px; border-radius: 50%; background: #fff; margin-bottom: 10px; }}
.capl .cl1, .capl .cl2 {{ display: block; height: 14px; border-radius: 7px; background: rgba(255,255,255,.85); margin-bottom: 8px; }}
.capl .cl1 {{ width: 80%; }} .capl .cl2 {{ width: 55%; }}
.pbar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 8px; background: rgba(255,255,255,.35); }}
.pfill {{ position: absolute; inset: 0; background: #fff; transform-origin: left center; transform: scaleX(0); }}
.thumb, .thumb2 {{ position: absolute; width: 96px; height: 96px; border-radius: 50%; background: rgba(255,255,255,.9);
  box-shadow: 0 0 0 12px rgba(255,255,255,.25), 0 14px 30px rgba(0,0,0,.25); opacity: 0; z-index: 7; }}
.thumb {{ left: 160px; top: 430px; }}
.thumb2 {{ left: 140px; top: 250px; }}
/* graphs */
.chart {{ position: absolute; left: 20px; top: 110px; width: 820px; height: 380px; overflow: visible; }}
#chJ .chart {{ top: 70px; height: 340px; }}
.gl {{ stroke: rgba(0,0,0,.07); stroke-width: 2; }}
.ln {{ fill: none; stroke: {RED}; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 1000; stroke-dashoffset: 1000; }}
.ln.blue {{ stroke: #3346ff; }}
.ar {{ opacity: 0; }} #arJ {{ opacity: 0; }}
.m3 {{ stroke: {RED}; stroke-width: 3; stroke-dasharray: 10 10; opacity: 0; }}
.dot {{ fill: {RED}; stroke: #fff; stroke-width: 6; opacity: 0; transform-box: fill-box; transform-origin: center; }}
.ax {{ font-family: Inter; font-size: 24px; font-weight: 700; fill: #5f5f5a; }}
.callout {{ position: absolute; left: 190px; top: 300px; display: flex; align-items: center; gap: 12px; padding: 12px 22px; border-radius: 999px;
  background: #fff; color: {RED}; font-size: 30px; font-weight: 800; box-shadow: 0 10px 30px rgba(0,0,0,.08); opacity: 0; white-space: nowrap; }}
.dotr {{ display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: {RED}; }}
/* the stopwatch ring around the big digit */
.ring {{ position: absolute; left: 70px; top: 500px; width: 940px; height: 940px; overflow: visible; }}
.ring .rt {{ fill: none; stroke: rgba(0,0,0,.08); stroke-width: 14; }}
.ring .rf {{ fill: none; stroke: {INK}; stroke-width: 14; stroke-linecap: round; stroke-dasharray: 1000; stroke-dashoffset: 0; }}
.ring .tk {{ stroke: rgba(0,0,0,.25); stroke-width: 4; stroke-linecap: round; }}
/* reel cards */
.thn {{ position: absolute; left: 24px; top: 24px; width: 200px; height: 352px; border-radius: 28px; overflow: hidden;
  background: linear-gradient(170deg, #ffb3c3 0%, #c9a7ff 55%, #8fa3ff 100%); }}
.thn.dark {{ background: linear-gradient(170deg, #3346ff, #6a1fe0 60%, #ff3d7f); }}
.thres {{ position: absolute; left: 0; right: 0; top: 26px; text-align: center; color: #fff; font-size: 64px; font-weight: 800; letter-spacing: -.04em; line-height: .9; }}
.thres small {{ font-size: 26px; font-weight: 700; letter-spacing: 0; }}
.rcr {{ position: absolute; left: 260px; right: 30px; top: 0; bottom: 0; }}
.bub {{ position: absolute; left: 0; top: 40px; padding: 22px 30px; border-radius: 34px 34px 34px 8px; background: #fff; box-shadow: 0 10px 30px rgba(0,0,0,.06);
  font-size: 40px; font-weight: 700; white-space: nowrap; opacity: 0; min-width: 120px; min-height: 92px; }}
.pbar2 {{ position: absolute; left: 0; right: 0; top: 230px; height: 14px; border-radius: 7px; background: rgba(0,0,0,.08); }}
.pf2 {{ position: absolute; inset: 0; border-radius: 7px; background: {RED}; transform-origin: left center; transform: scaleX(0); }}
.mk3 {{ position: absolute; left: 10%; top: -12px; width: 4px; height: 38px; background: {RED}; border-radius: 2px; }}
.pbar2 em {{ position: absolute; left: 10%; top: 30px; margin-left: -26px; font-style: normal; font-size: 24px; font-weight: 700; color: {RED}; }}
.rcr .row {{ left: 0; right: 0; }}
.pill.big2 {{ left: 50%; top: 1230px; transform: none; margin-left: -230px; font-size: 44px; padding: 18px 36px; opacity: 0; z-index: 4; }}
.bars {{ position: absolute; left: 0; bottom: 110px; width: 330px; height: 260px; }}
.bar {{ position: absolute; bottom: 0; width: 48px; border-radius: 12px 12px 4px 4px; background: linear-gradient(180deg, #3346ff, #9aa6ff); transform-origin: bottom; transform: scaleY(0); }}
#keptF {{ left: 0; bottom: 30px; opacity: 0; font-size: 28px; }}
.pic {{ width: 32px; height: 32px; fill: none; stroke: currentColor; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }}
/* the still photo + feed */
.feed {{ overflow: hidden; }}
.fstrip {{ position: absolute; left: 0; top: 0; width: 100%; }}
.fcard {{ position: relative; height: 420px; margin-bottom: 20px; border-radius: 44px; overflow: hidden; }}
.fcard.o1 {{ background: linear-gradient(170deg, #c9e6a3, #8fd0c4 60%, #6aa6d9); }}
.fcard.o2 {{ background: linear-gradient(170deg, #ffd29e, #ff9fb2 60%, #c48bff); }}
.fcard.o3 {{ background: linear-gradient(170deg, #a7c8ff, #8f9bff 60%, #b58bff); }}
.photo {{ background: linear-gradient(180deg, #dfe8f4, #bccbe0 60%, #a9b9d3); }}
.photo .sun {{ position: absolute; left: 610px; top: 60px; width: 110px; height: 110px; border-radius: 50%; background: #fff6d6; box-shadow: 0 0 60px rgba(255,240,190,.9); }}
.photo .h1 {{ position: absolute; left: -100px; top: 220px; width: 640px; height: 640px; border-radius: 50%; background: #7f93b3; }}
.photo .h2 {{ position: absolute; left: 330px; top: 260px; width: 700px; height: 700px; border-radius: 50%; background: #5f7397; }}
.pz {{ position: absolute; left: 50%; top: 50%; width: 140px; height: 140px; margin: -70px 0 0 -70px; border-radius: 50%; background: rgba(18,18,18,.55);
  backdrop-filter: blur(10px); display: grid; place-items: center; opacity: 0; }}
.pzi {{ width: 64px; height: 64px; fill: #fff; stroke: none; }}
.chip {{ position: absolute; left: 30px; top: 30px; padding: 10px 22px; border-radius: 999px; background: rgba(255,255,255,.8); font-size: 28px; font-weight: 700; opacity: 0; }}
.pill.nm {{ right: 30px; top: 30px; background: {RED}; color: #fff; opacity: 0; }}
/* explain / show timeline */
.sw2 .ic2 {{ margin-right: -10px; }}
.tlt {{ position: absolute; left: 0; right: 0; top: 0; bottom: 0; }}
.z3 {{ position: absolute; left: 40px; top: 120px; width: 78px; height: 150px; border-radius: 16px; background: rgba(255,42,42,.12); }}
.zl {{ position: absolute; left: 40px; top: 90px; font-style: normal; font-size: 22px; font-weight: 700; color: {RED}; white-space: nowrap; }}
.blk {{ position: absolute; top: 160px; height: 76px; border-radius: 18px; display: grid; place-items: center; font-size: 28px; font-weight: 800; letter-spacing: .04em;
  transform-origin: left center; opacity: 0; }}
.blk.ex {{ left: 40px; width: 234px; background: rgba(0,0,0,.08); color: #55554f; }}
.blk.sh {{ left: 274px; width: 78px; background: linear-gradient(90deg, #ff2a2a, #ff3d7f); color: #fff; font-size: 20px; }}
.lv {{ position: absolute; left: 116px; top: 110px; width: 4px; height: 170px; background: {RED}; opacity: 0; }}
.lvl {{ position: absolute; left: 130px; top: 260px; display: flex; align-items: center; gap: 10px; font-size: 26px; font-weight: 800; color: {RED}; opacity: 0; white-space: nowrap; }}
.tx {{ position: absolute; top: 300px; font-size: 22px; font-weight: 700; color: #5f5f5a; }}
/* comment box */
.av2 {{ position: absolute; left: 34px; top: 45px; width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #ffb3c3, #8fa3ff); }}
.inp {{ position: absolute; left: 140px; right: 140px; top: 40px; height: 90px; border-radius: 999px; background: rgba(0,0,0,.05); display: flex; align-items: center;
  padding: 0 34px; font-size: 44px; font-weight: 800; letter-spacing: .04em; }}
#cbph {{ font-weight: 600; letter-spacing: 0; color: #8d8d89; }}
#caret {{ width: 4px; height: 50px; margin-left: 6px; background: {INK}; border-radius: 2px; }}
.snd {{ position: absolute; right: 30px; top: 40px; width: 90px; height: 90px; border-radius: 50%; background: rgba(0,0,0,.06); display: grid; place-items: center; }}
.sdi {{ width: 46px; height: 46px; fill: none; stroke: {INK}; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }}

/* ---- v7 lively motion */
#shapes {{ position: absolute; inset: 0; }}
.shp {{ position: absolute; display: block; overflow: visible; filter: drop-shadow(0 18px 30px rgba(80,40,90,.18)); }}
.sph {{ border-radius: 50%; }}
#fxl {{ position: absolute; inset: 0; z-index: 6; pointer-events: none; }}
.bur {{ position: absolute; width: 400px; height: 400px; overflow: visible; opacity: 0; fill: none; stroke-width: 9; stroke-linecap: round; }}
.bur line {{ stroke-dasharray: 100; }}
.bur .shw {{ fill: none; stroke-width: 6; }}
.cf {{ position: absolute; opacity: 0; }}
.hrt {{ position: absolute; width: 58px; height: 58px; opacity: 0; filter: drop-shadow(0 6px 10px rgba(255,40,90,.35)); }}
.cw {{ position: absolute; opacity: 0; z-index: 3; }}
.cw .card {{ left: 0; top: 0; width: 100%; height: 100%; opacity: 1; }}
.crt {{ position: absolute; left: 0; bottom: 0; width: 100%; height: 92%; overflow: visible; }}
.gloss {{ position: absolute; inset: 0; background: linear-gradient(115deg, rgba(255,255,255,.38) 0%, rgba(255,255,255,0) 32%, rgba(255,255,255,0) 70%, rgba(255,255,255,.12) 100%); z-index: 5; pointer-events: none; }}
.btn {{ position: absolute; width: 8px; border-radius: 4px; background: #2a2a2a; }}
.btn.b1 {{ right: -6px; top: 160px; height: 90px; }} .btn.b2 {{ left: -6px; top: 140px; height: 60px; }}
.vbub {{ position: absolute; left: 120px; top: 1010px; display: flex; align-items: center; gap: 12px; padding: 16px 26px; border-radius: 26px; background: #fff;
  box-shadow: 0 24px 50px rgba(70,30,60,.2); font-size: 40px; font-weight: 800; opacity: 0; z-index: 4; }}
.vbub span {{ font-size: 28px; color: #66665f; font-weight: 700; }}
.vbub em {{ font-style: normal; color: {RED}; font-size: 42px; }}
.vbi {{ width: 34px; height: 34px; fill: {INK}; stroke: none; }}

/* ---- v8 */
#stage {{ position: absolute; inset: 0; transform-origin: 50% 48%; z-index: 3; }}
#dots {{ position: absolute; left: 0; top: 0; width: 1080px; height: 2010px; }}
#wps {{ position: absolute; inset: 0; z-index: 9; pointer-events: none; overflow: hidden; }}
.wp {{ position: absolute; left: -420px; top: -360px; width: 1920px; height: 2640px; display: grid; place-items: center; transform: translateX(1900px) rotate(-12deg); }}
.wpl {{ display: flex; flex-direction: column; align-items: center; transform: rotate(12deg); color: #fff; text-align: center; }}
.wpl b {{ font-size: 300px; font-weight: 800; letter-spacing: -.05em; line-height: .95; text-shadow: 0 20px 60px rgba(0,0,0,.18); white-space: nowrap; }}
.wpl span {{ font-size: 64px; font-weight: 800; letter-spacing: .12em; margin-top: 18px; white-space: nowrap; }}
.wm.wmh {{ padding: 0 .1em .12em; margin: 0 .1em -.12em -.1em; }}
.hlw {{ position: relative; }}
.mkr {{ position: absolute; left: -.08em; right: -.08em; top: .1em; bottom: -.02em; border-radius: .14em; transform-origin: left center; transform: scaleX(0); z-index: 0; }}
.mkr.r {{ background: linear-gradient(90deg, #ff2a2a, #ff3d7f); }}
.mkr.b {{ background: linear-gradient(90deg, #3346ff, #6a1fe0); }}
.hlt {{ position: relative; z-index: 1; }}
.ch {{ display: inline-block; opacity: 0; transform-origin: 50% 100%; }}
.sheen {{ position: absolute; top: -20%; bottom: -20%; left: 0; width: 34%; background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.75), rgba(255,255,255,0)); transform: translateX(-180%) skewX(-18deg); pointer-events: none; z-index: 8; opacity: 0; }}
/* CTA */
.bkm {{ position: absolute; left: 880px; top: 330px; width: 110px; height: 130px; opacity: 0; }}
.bki {{ width: 100%; height: 100%; overflow: visible; fill: none; stroke: {INK}; stroke-width: 1.8; stroke-linejoin: round; }}
"""


def main():
    body, od = scenes()
    # the glows drift the whole time
    js(f'tl.to(".g1", {{x: 220, y: 160, duration: {DUR / 2:.2f}, ease: "sine.inOut", repeat: 1, yoyo: true}}, 0);')
    js(f'tl.to(".g2", {{x: -240, y: -140, duration: {DUR / 3:.2f}, ease: "sine.inOut", repeat: 2, yoyo: true}}, 0);')
    js(f'tl.to(".g3", {{x: -200, y: 260, duration: {DUR / 2:.2f}, ease: "sine.inOut", repeat: 1, yoyo: true}}, 0);')
    # the camera: a slow push-in on the whole stage, reset under each chapter swipe (where nobody can see it)
    cuts = [0.0] + WIPES + [DUR]
    for a, b in zip(cuts, cuts[1:]):
        js(f'tl.fromTo("#stage", {{scale: 1}}, {{scale: 1.05, duration: {b - a:.3f}, ease: "none", immediateRender: false}}, {a:.3f});')
    js(f'tl.fromTo("#dots", {{y: 0}}, {{y: -45 * 6, duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
    css = CSS
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Reel flop explainer 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <svg class="fx"><defs>{"".join(DEFS)}<linearGradient id="ig1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff2a2a"/><stop offset="1" stop-color="#d02cff"/></linearGradient>
        <linearGradient id="ig2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6a1fe0"/><stop offset="1" stop-color="#2a7bff"/></linearGradient></defs></svg>
      <div id="bg"><i class="glow g1"></i><i class="glow g2"></i><i class="glow g3"></i>
        <svg id="dots" viewBox="0 0 1080 2010"><defs><pattern id="dp" width="45" height="45" patternUnits="userSpaceOnUse"><circle cx="22" cy="22" r="2.4" fill="rgba(40,30,50,.13)"/></pattern>
        <radialGradient id="dm"><stop offset="0" stop-color="#fff"/><stop offset=".75" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
        <mask id="dmk"><rect width="1080" height="2010" fill="url(#dm)"/></mask></defs><rect width="1080" height="2010" fill="url(#dp)" mask="url(#dmk)"/></svg></div>
      <div id="flash"></div>
      <div id="stage">{body}</div>
      <div id="fxl">{"".join(FXH)}</div>
      <div id="wps">{"".join(WP)}</div>
      <div id="grain"></div>
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(sorted(SFX, key=lambda e: e["t"]), open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html, {len(A)} timeline lines, {len(SFX)} sfx cues, {DUR} s")


if __name__ == "__main__":
    main()
