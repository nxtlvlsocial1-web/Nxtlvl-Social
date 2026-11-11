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
def scene_in(sid, t, d=.38, dy=220):
    js(f'tl.fromTo("#{sid}", {{opacity: 0, y: {dy}}}, {{opacity: 1, y: 0, duration: {d}, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    blur_pulse(sid, t, 26, .02, d)


def scene_out(sid, t, d=.3, dy=-220):
    js(f'tl.to("#{sid}", {{opacity: 0, y: {dy}, duration: {d}, ease: "expo.in"}}, {t:.3f});')
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
        plain = "".join(c for c in text if c not in "*^_~")
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
            word = word.strip("*^_~")
            wid = f"{pid}_{r}_{j}"
            inner = f'{word}<i class="stk" id="{pid}_s"></i>' if stk else word
            vis = first_visible and k == start
            out.append(f'<span class="wm"><span class="{cls}" id="{wid}"{" style=opacity:1" if vis else ""}>{inner}</span></span>')
            if not vis:
                t = ws[k]["t0"]
                js(f'tl.fromTo("#{wid}", {{yPercent: 110, opacity: 0}}, {{yPercent: 0, opacity: 1, duration: .42, ease: "expo.out", immediateRender: false}}, {t - .05:.3f});')
            k += 1
        out.append("</div>")
    out.append("</div>")
    if t_out:
        js(f'tl.to("#{pid}", {{opacity: 0, y: -60, duration: .26, ease: "expo.in"}}, {t_out:.3f});')
    return "".join(out)


# ---------------------------------------------------------------- the picker wheel
class Wheel:
    """A vertical list; the item at the centre is full size and lit with its gradient, neighbours dark, outer ones
    smaller and faded. move() rolls it item by item (decelerating) with vertical motion blur."""
    SP = [0, 1.08, 1.9, 2.55, 3.05, 3.4]          # distance from centre, in item heights
    SC = [1, .86, .62, .5, .42, .38]
    OP = [1, .9, .32, .14, .05, 0]

    def __init__(self, wid, items, top, size, left=LEFT, start=0, grads=None, maxw=MAXW, weight=800):
        self.wid, self.items, self.top, self.left, self.p = wid, items, top, left, start
        widest = max(text_w(s, 1, weight, -.03) for s in items)
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
            out.append(f'<div class="wi" id="{self.wid}_{i}" style="left:{self.left}px;top:{self.top - self.size * .6:.0f}px;font-size:{self.size}px;font-weight:{self.weight}">'
                       f'<span class="b">{s}</span><span class="g {self.grads[i]}" id="{self.wid}_{i}g">{s}</span></div>')
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



# ================================================================= the reel
def scenes():
    H = []

    # ---- A: cold open. "This reel is about to lose you." Big words rise in; "lose" glitches; the frame whips away
    t_a_out = L("l00", 6, "t1") + .02
    rows = [("xl", "This reel"), ("xl", "is about to"), ("xl", "*lose* *you.*")]
    ph = phrase("pA", "l00", rows, 700, first_visible=True)
    glitch = ('<div class="glx" id="glxR">lose you.</div><div class="glx c" id="glxC">lose you.</div>')
    H.append(scene("sA", ph + glitch, shown=True))
    t_lose = L("l00", 5)
    for k, (dx, op) in enumerate([(14, .85), (-10, .7), (8, .9), (-16, .6), (0, 0)]):
        tt = t_lose + .03 + k * .05
        js(f'tl.set("#glxR", {{x: {dx}, opacity: {op}}}, {tt:.3f}); tl.set("#glxC", {{x: {-dx}, opacity: {op}}}, {tt:.3f});')
        js(f'tl.set("#pA_2_0, #pA_2_1", {{x: {R.choice([-6, 6, 0])}}}, {tt:.3f});')
    sfx("glitch", t_lose)
    js(f'tl.fromTo("#sA", {{scale: 1}}, {{scale: 1.06, duration: {t_a_out:.2f}, ease: "none", immediateRender: false}}, 0);')
    scene_out("sA", t_a_out, d=.26, dy=-420)
    sfx("hit", 0)

    # ---- B: "Your reel didn't flop because of the algorithm." A wheel of excuses lands on "the algorithm", struck through
    excuses = ["the hashtags", "your audio", "posting time", "shadowbans", "the algorithm", "the caption", "the thumbnail",
               "your niche", "trends", "the first 3 seconds"]
    gr = ["gr2"] * len(excuses)
    gr[-1] = "gr1"
    t_b = t_a_out + .12
    wB = Wheel("wB", excuses, 1120, 116, start=0, grads=gr)
    phB = phrase("pB", "l01", [("m", "Your reel didn't"), ("m", "flop because of")], 560, t_out=L("l02", 0) - .12)
    sw_ = text_w("the algorithm", wB.size, 800, -.03)
    strike = f'<i class="wstk" id="wBstk" style="width:{sw_ + 16:.0f}px;top:{1120 - wB.size * .05:.0f}px;height:{wB.size * .09:.0f}px"></i>'
    H.append(scene("sB", phB + wB.html() + strike))
    scene_in("sB", t_b)
    wB.appear(t_b + .05)
    # it rolls gently while she speaks, landing on "the algorithm" exactly when she says it
    t_alg = L("l01", 7) - .02
    wB.move(t_b + .5, 2, 1.0, tick=False)
    wB.move(t_alg - .5, 4, .5)
    a_end = L("l01", 7, "t1")
    js(f'tl.fromTo("#wBstk", {{scaleX: 0, opacity: 1}}, {{scaleX: 1, opacity: 1, duration: .24, ease: "power3.inOut", immediateRender: false}}, {a_end - .12:.3f});')
    js(f'tl.to("#wB_4", {{opacity: .45, duration: .2}}, {a_end:.3f});')
    sfx("scratch", a_end - .1)

    # ---- C: "It flopped in the first three seconds." The wheel spins hard to "the first 3 seconds" (red)
    t_c = L("l02", 0) - .1
    phC = phrase("pC", "l02", [("m", "It flopped in")], 560, t_out=L("l02", 5) - .3)
    H.append(scene("sC", phC, shown=False))
    js(f'tl.set("#sC", {{opacity: 1}}, {t_c - .02:.3f});')
    js(f'tl.to("#wBstk", {{opacity: 0, duration: .12}}, {t_c:.3f});')
    t_first = L("l02", 3)
    wB.move(t_c + .15, 9, t_first - t_c - .1, final_ease="back.out(2)")
    js(f'tl.fromTo("#wB_9", {{scale: 1}}, {{keyframes: {{scale: [1, 1.12, 1]}}, duration: .35, ease: "power2.out", immediateRender: false}}, {t_first + .05:.3f});')
    sfx("hit", t_first)
    t_cd = L("l02", 5) - .25
    scene_out("sB", t_cd, d=.24, dy=-300)
    js(f'tl.to("#sC", {{opacity: 0, duration: .2}}, {t_cd:.3f});')

    # ---- giant slot-machine digit: 3, 2, 1, 0 (red, on a dark flash) as the beat drops
    flip_t = L("l02", 6, "t1") + .06
    c3 = t_cd + .12
    c2 = L("l02", 6) - .05
    c1 = (c2 + flip_t) / 2
    H.append(scene("sD", '<div class="bigm"><div class="bigs" id="bigs">' + "".join(f'<b class="bd{d}">{d}</b>' for d in (3, 2, 1, 0)) + '</div></div>'))
    js(f'tl.fromTo("#sD", {{opacity: 0, scale: .8}}, {{opacity: 1, scale: 1, duration: .3, ease: "expo.out", immediateRender: false}}, {c3:.3f});')
    sfx("hit", c3)
    for k, t in enumerate([c2, c1, flip_t]):
        js(f'tl.fromTo("#bigs", {{y: {-k * 900}}}, {{y: {-(k + 1) * 900}, duration: .2, ease: "back.out(1.4)", immediateRender: false}}, {t - .1:.3f});')
        blur_pulse("sD", t - .1, 30, .06, .14)
        sfx("count" if k < 2 else "glitch", t)
    js(f'tl.set("#flash", {{opacity: 1}}, {flip_t - .02:.3f}); tl.to("#flash", {{opacity: 0, duration: .45, ease: "power2.in"}}, {flip_t + .32:.3f});')
    js(f'tl.fromTo("#sD", {{scale: 1}}, {{scale: 1.1, duration: .5, ease: "power2.out", immediateRender: false}}, {flip_t:.3f});')
    t_e = L("l03", 0) - .14
    scene_out("sD", t_e - .05, d=.25, dy=-400)

    # ---- E: "Here are three mistakes killing your views."
    phE = phrase("pE", "l03", [("s", "_Here _are"), ("xl", "*3 mistakes"), ("m", "*killing your views.")], 760, t_out=None)
    H.append(scene("sE", phE))
    scene_in("sE", t_e)
    t_f = L("l04", 0) - .14
    scene_out("sE", t_f - .04)

    # ---- F: the mistakes wheel. "One: your hook is a greeting."
    mistakes = ["The greeting", "A still frame", "Explaining first"]
    wF = Wheel("wF", mistakes, 1120, 120, start=0, grads=["gr1", "gr1", "gr1"])
    lab = '<div class="lab" id="labF"><span id="labN">01</span> / 03</div>'
    phF = phrase("pF", "l04", [("s", "_One:"), ("m", "your hook is"), ("m", "a greeting.")], 560, t_out=L("l05", 0) - .12)
    H.append(scene("sF", lab + phF + wF.html()))
    scene_in("sF", t_f)
    wF.appear(t_f + .05)
    js(f'tl.fromTo("#labF", {{opacity: 0, x: -30}}, {{opacity: 1, x: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {t_f + .1:.3f});')
    # "Nobody stays for 'Hey guys.'" : the wheel steps aside, the quote takes the centre
    t_q = L("l05", 0) - .12
    phF2 = phrase("pF2", "l05", [("m", "Nobody stays for")], 560, t_out=L("l06", 0) - .12)
    quote = '<div class="quote" id="quote"><span id="qt">“Hey guys.”</span><i class="qstk" id="qstk"></i></div>'
    H.append(scene("sF2", phF2 + quote))
    js(f'tl.set("#sF2", {{opacity: 1}}, {t_q:.3f});')
    js(f'tl.to("#wF", {{opacity: 0, y: 160, duration: .3, ease: "expo.in"}}, {t_q:.3f});')
    blur_pulse("wF", t_q, 24, .3, .05)
    js(f'tl.fromTo("#quote", {{opacity: 0, scale: 1.3}}, {{opacity: 1, scale: 1, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l05", 3) - .08:.3f});')
    sfx("hit", L("l05", 3) - .05)
    js(f'tl.fromTo("#qstk", {{scaleX: 0}}, {{scaleX: 1, duration: .25, ease: "power3.inOut", immediateRender: false}}, {L("l05", 4, "t1") - .05:.3f});')
    js(f'tl.to("#qt", {{color: "#b9b9b9", duration: .2}}, {L("l05", 4, "t1"):.3f});')
    sfx("scratch", L("l05", 4, "t1") - .05)

    # "Start with the result." : the quote scrambles into the result (decode effect)
    t_r = L("l06", 0) - .1
    phF3 = phrase("pF3", "l06", [("m", "Start with the ^result.")], 560, t_out=L("l07", 0) - .14)
    H.append(scene("sF3", phF3))
    js(f'tl.set("#sF3", {{opacity: 1}}, {t_r:.3f});')
    js(f'tl.to("#qstk", {{opacity: 0, duration: .1}}, {t_r:.3f});')
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
    js(f'tl.set("#qres", {{opacity: 1}}, {t_r + .05 + n * .045:.3f});')
    H.append('<div class="quote res" id="qres" style="opacity:0"><span class="gr2">1M views in 3 days.</span></div>')
    js(f'tl.set("#qt", {{opacity: 0}}, {t_r + .05 + n * .045:.3f});')
    js(f'tl.fromTo("#qres", {{scale: 1.08}}, {{scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false}}, {t_r + .05 + n * .045:.3f});')
    sfx("ding", t_r + .05 + n * .045)
    t_g = L("l07", 0) - .14
    js(f'tl.to("#quote, #qres", {{opacity: 0, y: -120, duration: .26, ease: "expo.in"}}, {t_g - .04:.3f});')
    blur_pulse("sF2", t_g - .04, 24, .26, .05)

    # ---- G: "Two: your first frame is still." The wheel comes back and rolls to item 2
    phG = phrase("pG", "l07", [("s", "_Two:"), ("m", "your first frame"), ("m", "is still.")], 560, t_out=L("l08", 0) - .12)
    H.append(scene("sG", phG))
    js(f'tl.set("#sG", {{opacity: 1}}, {t_g:.3f});')
    js(f'tl.to("#wF", {{opacity: 1, y: 0, duration: .4, ease: "expo.out"}}, {t_g:.3f});')
    wF.move(t_g + .2, 1, .45)
    js(f'tl.set("#labN", {{textContent: "02"}}, {t_g + .4:.3f});')
    # "If nothing moves," everything holds dead still (the music drops out too), then the wheel whips away on "scrolling"
    t_h = L("l08", 0) - .1
    phH = phrase("pH", "l08", [("m", "If nothing moves,"), ("m", "thumbs keep scrolling.")], 560, t_out=L("l09", 0) - .12)
    H.append(scene("sH", phH))
    js(f'tl.set("#sH", {{opacity: 1}}, {t_h:.3f});')
    t_sc = L("l08", 3)
    js(f'tl.to("#wF", {{y: -900, opacity: 0, duration: .5, ease: "power3.in"}}, {t_sc:.3f});')
    blur_pulse("wF", t_sc, 40, .4, .1)
    sfx("whoosh", t_sc + .05)

    # ---- I: "Three: you explain before you show." then "Show the result first, then explain how you got it."
    t_i = L("l09", 0) - .12
    phI = phrase("pI", "l09", [("s", "_Three:"), ("m", "you explain"), ("m", "before you show.")], 560, t_out=L("l10", 0) - .12)
    sw = vblur("swp")
    swap = (f'<div id="swp" style="filter:{sw}"><div class="sw2" id="swE"><span class="n">1</span>EXPLAIN</div>'
            f'<div class="sw2" id="swS"><span class="n">2</span><span class="t">SHOW<span class="g gr1" id="swSg">SHOW</span></span></div></div>')
    H.append(scene("sI", phI + swap))
    js(f'tl.set("#sI", {{opacity: 1}}, {t_i:.3f});')
    js(f'tl.set("#labN", {{textContent: "03"}}, {t_i:.3f});')
    js(f'tl.fromTo("#swE", {{opacity: 0, yPercent: 60}}, {{opacity: 1, yPercent: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l09", 2) - .05:.3f});')
    js(f'tl.fromTo("#swS", {{opacity: 0, yPercent: 60}}, {{opacity: .35, yPercent: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {L("l09", 5) - .05:.3f});')
    sfx("tick", L("l09", 2))
    sfx("tick", L("l09", 5))
    t_sw = L("l10", 0) - .05
    phI2 = phrase("pI2", "l10", [("m", "Show the result"), ("m", "first,"), ("s", "_then _explain _how _you _got _it.")], 560)
    H.append(scene("sI2", phI2))
    js(f'tl.set("#sI2", {{opacity: 1}}, {t_sw - .05:.3f});')
    js(f'tl.to("#swS", {{y: -190, opacity: 1, duration: .5, ease: "expo.inOut"}}, {t_sw:.3f});')
    js(f'tl.to("#swE", {{y: 190, opacity: .35, duration: .5, ease: "expo.inOut"}}, {t_sw:.3f});')
    js(f'tl.set("#swS .n", {{textContent: "1"}}, {t_sw + .25:.3f}); tl.set("#swE .n", {{textContent: "2"}}, {t_sw + .25:.3f});')
    js(f'tl.to("#swSg", {{opacity: 1, duration: .25}}, {t_sw + .3:.3f});')
    blur_pulse("swp", t_sw, 22, .2, .3)
    sfx("swish", t_sw)
    sfx("success", t_sw + .5)
    t_j = L("l11", 0) - .14
    scene_out("sI", t_j - .04)
    js(f'tl.to("#sI2, #sF", {{opacity: 0, duration: .2}}, {t_j - .04:.3f});')

    # ---- J: "Fix these three and watch your next reel." Fixes roll by with checks; the views odometer
    fixes = ["Result first", "Move in frame 1", "Show, then explain"]
    wJ = Wheel("wJ", fixes, 1120, 116, start=0, grads=["gr2"] * 3)
    phJ = phrase("pJ", "l11", [("m", "*Fix these three"), ("s", "_and _watch _your _next _reel.")], 560)
    od = Odometer("odo", "  ,312", "48,200", 1280, 210, 0)
    H.append(scene("sJ", phJ + wJ.html() + od.html() + '<div class="odl" id="odl">views on your next reel</div>'))
    scene_in("sJ", t_j)
    wJ.appear(t_j + .05)
    wJ.move(L("l11", 1), 1, .3)
    wJ.move(L("l11", 2) + .05, 2, .3)
    for k in range(3):
        sfx("pop", [t_j + .3, L("l11", 1) + .3, L("l11", 2) + .35][k])
    t_o = L("l11", 4) - .1
    js(f'tl.to("#wJ", {{opacity: 0, y: -120, duration: .3, ease: "expo.in"}}, {t_o - .1:.3f});')
    blur_pulse("wJ", t_o - .1, 24, .3, .05)
    js(f'tl.fromTo("#odo, #odl", {{opacity: 0, y: 80}}, {{opacity: 1, y: -330, duration: .45, ease: "expo.out", immediateRender: false}}, {t_o:.3f});')
    od.roll(t_o + .2, 1.1)
    sfx("rise", t_o + .2)
    sfx("ding", t_o + 1.3)

    # ---- K: CTA. "Save this so you don't forget, and comment HOOK for my list of twenty hooks that work."
    t_k = L("l12", 0) - .14
    scene_out("sJ", t_k - .04)
    kw = ["GUIDE", "LINK", "TIPS", "SEND", "HOOK"]
    wK = Wheel("wK", kw, 1200, 170, start=0, grads=["gr1"] * 5)
    phK = phrase("pK", "l12", [("m", "Save this so you"), ("m", "don't forget,")], 560, t_out=L("l12", 6) - .1)
    phK2 = phrase("pK2", "l12", [("m", "and comment")], 560, start=6)
    phK3 = phrase("pK3", "l12", [("s", "_for _my _list _of _20 _hooks _that _work.")], 1440, start=9)
    bk = '<div class="bkm" id="bkm"><svg viewBox="0 0 24 24"><path d="M6 3.5h12v17l-6-4.2-6 4.2z"/></svg></div>'
    H.append(scene("sK", phK + phK2 + wK.html() + phK3 + bk))
    scene_in("sK", t_k)
    js(f'tl.fromTo("#bkm", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .4, ease: "back.out(2)", immediateRender: false}}, {L("l12", 0):.3f});')
    js(f'tl.to("#bkp", {{fill: "{INK}", duration: .15}}, {L("l12", 1):.3f});')
    js(f'tl.to("#bkm", {{opacity: 0, duration: .2}}, {L("l12", 6) - .1:.3f});')
    sfx("pop", L("l12", 0))
    wK.appear(L("l12", 6) - .05)
    wK.move(L("l12", 7) - .05, 4, L("l12", 8) - L("l12", 7) + .05, final_ease="back.out(2.2)")
    js(f'tl.fromTo("#wK_4", {{scale: 1}}, {{keyframes: {{scale: [1, 1.1, 1]}}, duration: .4, ease: "power2.out", immediateRender: false}}, {L("l12", 8) + .05:.3f});')
    sfx("hit", L("l12", 8))
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
.glx {{ position: absolute; left: {LEFT}px; top: 1010px; font-size: 160px; font-weight: 800; letter-spacing: -.035em; color: rgba(255,0,60,.7); mix-blend-mode: multiply; opacity: 0; white-space: nowrap; }}
.glx.c {{ color: rgba(0,200,255,.7); }}
/* wheels */
.whl {{ position: absolute; inset: 0; }}
.wi {{ position: absolute; white-space: nowrap; line-height: 1.2; letter-spacing: -.03em; transform-origin: left center; opacity: 0; }}
.wi .b {{ color: {INK}; }}
.wi .g {{ position: absolute; left: 0; top: 0; opacity: 0; }}
.wstk {{ left: {LEFT - 8}px; z-index: 5; opacity: 0; }}
.lab {{ position: absolute; left: {LEFT}px; top: 470px; font-size: 34px; font-weight: 700; letter-spacing: .14em; color: #66665f; opacity: 0; }}
.lab span {{ color: {INK}; }}
/* the big digit */
.bigm {{ position: absolute; left: 0; right: 0; top: 520px; height: 900px; overflow: hidden; }}
.bigs {{ position: absolute; left: 0; right: 0; top: 0; }}
.bigs b {{ display: block; height: 900px; line-height: 900px; text-align: center; font-size: 820px; font-weight: 800; letter-spacing: -.05em; color: {INK}; }}
.bigs .bd2 {{ color: {INK}; }} .bigs .bd0 {{ color: {RED}; }}
/* quote */
.quote {{ position: absolute; left: {LEFT}px; right: 60px; top: 1060px; font-size: 128px; font-weight: 800; letter-spacing: -.035em; white-space: nowrap; opacity: 0; }}
.quote.res {{ font-size: {int(MAXW / text_w("1M views in 3 days.", 1, 800, -.035))}px; z-index: 4; }}
.quote .qstk {{ width: 760px; left: -10px; top: 55%; height: 14px; }}
/* explain / show */
#swp {{ position: absolute; left: 0; right: 0; top: 1000px; z-index: 3; }}
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
.odl {{ position: absolute; left: 0; right: 0; top: 1510px; text-align: center; font-size: 50px; font-weight: 600; color: #66665f; opacity: 0; }}
/* CTA */
.bkm {{ position: absolute; left: 900px; top: 300px; width: 100px; height: 120px; opacity: 0; }}
.bkm svg {{ width: 100%; height: 100%; overflow: visible; }}
.bkm path {{ fill: none; stroke: {INK}; stroke-width: 1.8; stroke-linejoin: round; }}
"""


def main():
    body, od = scenes()
    # the glows drift the whole time
    js(f'tl.to(".g1", {{x: 220, y: 160, duration: {DUR / 2:.2f}, ease: "sine.inOut", repeat: 1, yoyo: true}}, 0);')
    js(f'tl.to(".g2", {{x: -240, y: -140, duration: {DUR / 3:.2f}, ease: "sine.inOut", repeat: 2, yoyo: true}}, 0);')
    js(f'tl.to(".g3", {{x: -200, y: 260, duration: {DUR / 2:.2f}, ease: "sine.inOut", repeat: 1, yoyo: true}}, 0);')
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
      <svg class="fx"><defs>{"".join(DEFS)}</defs></svg>
      <div id="bg"><i class="glow g1"></i><i class="glow g2"></i><i class="glow g3"></i></div>
      <div id="flash"></div>
      {body}
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
