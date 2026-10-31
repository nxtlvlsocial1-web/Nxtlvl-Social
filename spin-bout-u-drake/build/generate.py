"""Spin Bout U (Drake & 21 Savage) lyric edit, 1:1, 60 s from the 2:13 bass drop, v4: writes index.html.

python3 build/generate.py      (from the project root; after build/align.py, build/assets.py, build/anime.py and
build/animaps.py)

v4 takes its type and cuts from the owner's Spin Bout U reference (Video-97924, 720x720, 20 fps), read frame by
frame (261 frames): black / maroon / magenta / off-white; giant heavy white letters behind the subject that pop in
one by one, grey then white; wide block words (PRAY / MORE / THAN); heavy words with a magenta block shadow
(WAS / YOU / WHEN); sticker labels (magenta box, white frame); words inside magenta starbursts; the magenta brush
script "Spin"; magenta panels, trapezoid spotlight cones, sunburst rays, a white squiggle pattern; mirrored floor
type. Its cuts: a card swinging in in perspective; a whip smear onto a maroon frame with a white light line, the
next shot sliding in as a tilted panel; zoom blur into a white frame; a smear onto black and the subject swinging
in; a push; a drop blur; sliding strips; a white frame, a stripe glitch, then a small turned card zooming up; a
diagonal scroll; a slide up. Everything drifts and grows slowly; nothing shakes.

The anime illustrations (Canva, 1990s TV-anime cels, plan/anime.json) move: hair, clothes and outlines sway in the
wind through an SVG displacement map per picture (build/animaps.py), cut-out figures breathe, smoke and flames
flow through a drifting noise field limited to their area, light sweeps across the figures, and sparkles, petals,
embers and diamonds ride on top. The opening keeps the owner's pictures (two Drake photos, the cats, En Vogue, the
phone). Captions are the owner's lyrics on their sung words; every cuss word shows only as a blurred ****.
Everything steps at 20 fps and renders at 20 fps.
"""
import json
import math
import os
import random
import re

from PIL import Image, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, DUR, FPS = 1080, 60.0, 20
STEP = 1 / FPS
L = json.load(open(os.path.join(ROOT, "plan", "lines.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats.json")))["beats"]
INK, MAR, MAG, WHT, GRY, DRD = "#191919", "#5f1b30", "#b0194f", "#f2f1ec", "#8c8c8c", "#7a1d2e"
F = {k: ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", f), 100) for k, f in
     (("anton", "Anton.ttf"), ("archivo", "ArchivoBlack.ttf"), ("dela", "DelaGothicOne.ttf"),
      ("script", "KaushanScript.ttf"), ("marker", "PermanentMarker.ttf"))}
FAM = {"anton": "Anton", "archivo": "Archivo Black", "dela": "Dela Gothic One", "script": "Kaushan Script",
       "marker": "Permanent Marker"}
CURSE = {"ass", "hoes", "nigga", "niggas", "shitll", "shit"}
A, HIDE, FILTERS = [], [], []
CLIPN = [0]
NID = [0]
CUR = {}


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def q(t):
    return round(t * FPS) / FPS


def text(li, i0, i1):
    out = []
    for w, s, e in L[li]["words"][i0:i1 + 1]:
        core = re.sub(r"[^a-z]", "", w.lower())
        out.append("****" + w[len(w.rstrip(",.")):] if core in CURSE else w)
    return " ".join(out)


def at(li, k):
    return q(L[li]["words"][k][1])


def lt(li):
    return q(L[li]["start"])


def tw(t, size, font="anton"):
    return F[font].getlength(t) * size / 100


def fit(t, maxw, size, font="anton"):
    return min(size, maxw / max(1, tw(t, 100, font)) * 100)


def frames(t0, t1, every=1):
    t, out = q(t0), []
    while t < t1 - 1e-6:
        out.append(round(t, 3))
        t = q(t + every * STEP)
    return out


# ------------------------------------------------------------------------------------------------ primitives
def put(html, ly=1):
    CUR["ly"][ly].append(html)


def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{display: "block", opacity: 1}}, {q(t0):.3f});')
    if t1 < DUR:      # out of the render tree when not on screen (keeps the capture light)
        js(f'tl.set("{sel}", {{display: "none", opacity: 0}}, {q(t1):.3f});')


def tween(sel, frm, to, t, n, ease=None):
    e = ease or f"steps({n})"
    js(f'tl.fromTo("{sel}", {json.dumps(frm)}, {{...{json.dumps(to)}, duration: {n * STEP:.3f}, ease: "{e}", '
       f'immediateRender: false}}, {q(t):.3f});')


def enter(sel, t, how, n=3):
    if how == "pop":
        tween(sel, {"scale": 1.5}, {"scale": 1}, t, n)
    elif how in ("left", "right", "up", "down"):
        dx, dy = {"left": (-520, 0), "right": (520, 0), "up": (0, 560), "down": (0, -560)}[how]
        tween(sel, {"x": dx, "y": dy, "filter": "blur(14px)"}, {"x": 0, "y": 0, "filter": "blur(0px)"}, t, n)
    elif how == "settle":
        tween(sel, {"scale": 1.12, "filter": "blur(12px)"}, {"scale": 1, "filter": "blur(0px)"}, t, n)
    elif how == "rise":
        tween(sel, {"y": 640, "filter": "url(#vblur)"}, {"y": 0, "filter": "blur(0px)"}, t, n + 1)
    elif how == "tilt":      # the card swinging in in perspective (reference 0.0-0.4 s)
        tween(sel, {"rotationY": 62, "rotationX": -10, "scale": .7, "transformPerspective": 900, "filter": "brightness(.4)"},
              {"rotationY": 0, "rotationX": 0, "scale": 1, "filter": "brightness(1)"}, t, n + 3)
    elif how == "swing":     # the subject swinging in out of a blur (reference 2.5-2.7 s)
        tween(sel, {"rotationY": -45, "x": 160, "scale": .9, "transformPerspective": 900, "filter": "blur(10px)"},
              {"rotationY": 0, "x": 0, "scale": 1, "filter": "blur(0px)"}, t, n + 1)


def osc(sel, prop, amp, t0, t1, period, attr=False, base=0.0):
    """A back-and-forth (sine) of one property, the wind and the breathing, held on threes: a new drawing every
    0.15 s (about 8 a second), like hand-drawn 90s anime rather than smooth AI motion."""
    t = q(t0)
    while t < t1 - 1e-6:
        v = base + amp * math.sin((t - t0) / period * math.tau)
        js(f'tl.set("{sel}", {{attr: {{{prop}: {v:.4f}}}}}, {t:.3f});' if attr else f'tl.set("{sel}", {{{prop}: {v:.4f}}}, {t:.3f});')
        t = q(t + 3 * STEP)


def photo(src, x, y, w, h=None, rot=0, t0=0, t1=DUR, kind="cut", how="settle", z=3, push=.05, outline=False,
          card=False, round_=False, wind=0.0, breathe=False, flow=None, sweeps=(), reveal=False, slices=(), punches=(),
          pos="", ly=1, clip=None):
    """kind: cut / print (the owner's photos), acut / afull (the anime art). wind: displacement amount (fraction of
    the picture); flow: 'smoke' or 'fire' (that area flows); breathe: a slow rise and fall; sweeps: times a light
    sweeps across; reveal: arrives as a white glowing silhouette; slices: slice-glitch times; punches: (t, scale)."""
    i = nid("ph")
    if CUR.get("idx", 0) > 0 and abs(q(t0) - CUR["t0"]) < .16:
        how, reveal = "", False
        t0 = CUR["t0"]
    path = {"cut": f"assets/img/cut/{src}.png", "print": f"assets/img/print/{src}.jpg", "src": f"assets/img/src/{src}.jpg",
            "acut": f"assets/img/anime/cut/{src}.png", "afull": f"assets/img/anime/full/{src}.jpg"}[kind]
    if h is None:
        iw, ih = Image.open(os.path.join(ROOT, path)).size
        h = w * ih / iw
    filt = ""
    if wind or flow:
        fid = f"w{i}"
        parts = [f'<filter id="{fid}" x="-8%" y="-8%" width="116%" height="116%" color-interpolation-filters="sRGB" '
                 f'primitiveUnits="objectBoundingBox">']
        cur = "SourceGraphic"
        if wind:
            parts.append(f'<feImage href="assets/img/anime/map/{src}.png" x="0" y="0" width="1" height="1" preserveAspectRatio="none" result="m"/>'
                         f'<feDisplacementMap id="wd{i}" in="SourceGraphic" in2="m" scale="0" xChannelSelector="R" yChannelSelector="G" result="d1"/>')
            cur = "d1"
        if flow:
            parts.append(f'<feTurbulence type="fractalNoise" baseFrequency="5 4" numOctaves="2" seed="{len(FILTERS) + 3}" result="t"/>'
                         f'<feOffset id="fo{i}" in="t" dx="0" dy="0" result="t2"/>'
                         f'<feImage href="assets/img/anime/flow/{src}.png" x="0" y="0" width="1" height="1" preserveAspectRatio="none" result="mk"/>'
                         f'<feComposite in="t2" in2="mk" operator="in" result="tm"/>'
                         f'<feFlood flood-color="rgb(128,128,128)" result="nu"/>'
                         f'<feMerge result="fm"><feMergeNode in="nu"/><feMergeNode in="tm"/></feMerge>'
                         f'<feDisplacementMap in="{cur}" in2="fm" scale="{.05 if flow == "smoke" else .035}" xChannelSelector="R" yChannelSelector="G"/>')
        parts.append("</filter>")
        FILTERS.append("".join(parts))
        filt = f"filter:url(#{fid});"
    pf = f"filter:drop-shadow(4px 0 0 {WHT}) drop-shadow(-4px 0 0 {WHT}) drop-shadow(0 4px 0 {WHT}) drop-shadow(0 -4px 0 {WHT});" if outline else ""
    cls = "ph" + (" card" if card else "") + (" rnd" if round_ else "")
    img = f'<img src="{path}" alt="" style="{pos}">'
    vid = ""
    if clip:    # the owner's animated clip (build/clips90.py) plays over the still
        cp = os.path.join(ROOT, "assets", "video", "anime", f"{clip}.mp4")
        ln = float(os.popen(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{cp}"').read() or 0)
        CLIPN[0] += 1
        vid = (f'<video id="vc{CLIPN[0]}" class="clip" src="assets/video/anime/{clip}.mp4" data-start="{q(t0):.3f}" '
               f'data-duration="{min(ln, q(t1) - q(t0) + 6 * STEP):.3f}" data-track-index="{2 + CLIPN[0]}" muted playsinline></video>')
    sl = ""
    if slices:
        sl = '<div class="slc">' + "".join(f'<div style="clip-path:inset({k * 100 / 7:.1f}% 0 {100 - (k + 1) * 100 / 7:.1f}% 0)">{img}</div>'
                                         for k in range(7)) + "</div>"
    sw = ""
    if sweeps:
        mask = f"-webkit-mask-image:url({path});mask-image:url({path});" if kind in ("cut", "acut") else ""
        sw = f'<div class="sw" style="{mask}"><i></i></div>'
    put(f'<div class="{cls}" id="{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;transform:rotate({rot}deg);'
        f'z-index:{z}"><div class="pu" style="{pf}"><div class="br"><div class="in" style="{filt}">{img}{vid}</div>{sl}{sw}</div></div></div>', ly)
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how)
    if push:
        n = max(1, round((q(t1) - q(t0)) * FPS))
        tween(f"#{i} .in", {"scale": 1}, {"scale": 1 + push}, t0, n, "none")
    if wind:
        osc(f"#wd{i}", "scale", wind, t0, t1, 1.9, attr=True)
    if flow:
        n = max(1, round((q(t1) - q(t0)) * FPS))
        tween(f"#fo{i}", {"attr": {"dx": 0, "dy": 0}}, {"attr": {"dx": -.18 * (t1 - t0), "dy": -.25 * (t1 - t0)}}, t0, n, "none")
    if breathe:
        osc(f"#{i} .br", "scaleY", .008, t0, t1, 2.6, base=1.0)
    for ts in sweeps:
        tween(f"#{i} .sw i", {"x": -1.2 * w}, {"x": 1.2 * w}, ts, 8, "power1.inOut")
    if reveal:
        seq = ["brightness(0) invert(1) blur(6px)", "brightness(0) invert(1) drop-shadow(0 0 14px #fff)",
               "grayscale(1) brightness(2.6) contrast(.6)", "brightness(1.6)", "brightness(1.2)", "none"]
        for k, f_ in enumerate(seq):
            js(f'tl.set("#{i} .in > *", {{filter: "{f_}"}}, {q(t0) + k * STEP:.3f});')
    for ts in slices:
        g = random.Random(int(ts * 100))
        js(f'tl.set("#{i} .in", {{opacity: 0}}, {q(ts):.3f});')
        js(f'tl.set("#{i} .slc", {{opacity: 1}}, {q(ts):.3f});')
        for f_ in range(3):
            for k in range(7):
                js(f'tl.set("#{i} .slc > div:nth-child({k + 1})", {{x: {g.choice([-1, 1]) * g.uniform(10, 90) * (1 - f_ / 3):.0f}}}, {q(ts) + f_ * STEP:.3f});')
        js(f'tl.set("#{i} .in", {{opacity: 1}}, {q(ts) + 3 * STEP:.3f});')
        js(f'tl.set("#{i} .slc", {{opacity: 0}}, {q(ts) + 3 * STEP:.3f});')
    for tp, sc in punches:
        js(f'tl.set("#{i} .pu", {{scale: {sc}}}, {q(tp):.3f});')
    return i


def panel(x, y, w, h, color, t0, t1=DUR, rot=0, how="left", z=1, ly=0, clip="", extra=""):
    i = nid("pn")
    put(f'<i class="pn" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};transform:rotate({rot}deg);'
        f'z-index:{z};{f"clip-path:{clip};" if clip else ""}{extra}"></i>', ly)
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how, 2)
    return i


def cone(t0, t1, cx=540, top=360, color=MAG, ly=0, z=1):
    """The magenta trapezoid spotlight cone (reference 6.9-7.4 s)."""
    return panel(0, 0, S, S, color, t0, t1, how="down", z=z, ly=ly,
                 clip=f"polygon({(cx - top / 2) / S * 100:.1f}% 100%, {(cx + top / 2) / S * 100:.1f}% 100%, 100% 0, 0 0)")


def para(x, y, w, h, color, t0, t1, skew=-12, how="right", z=1, ly=0):
    """A tilted magenta panel behind the subject."""
    return panel(x, y, w, h, color, t0, t1, how=how, z=z, ly=ly, extra=f"transform:skewX({skew}deg);")


def rays(t0, t1, cx=1080, cy=0, color=MAG, ly=0, z=1, n=22):
    i = nid("ry")
    put(f'<svg class="rays" id="{i}" style="z-index:{z}" viewBox="0 0 1080 1080">' + "".join(
        f'<polygon fill="{color}" points="{cx},{cy} {cx + 1500 * math.cos(a - .025):.0f},{cy + 1500 * math.sin(a - .025):.0f} '
        f'{cx + 1500 * math.cos(a + .025):.0f},{cy + 1500 * math.sin(a + .025):.0f}"/>' for a in [k * math.tau / n for k in range(n)]) + '</svg>', ly)
    show(f"#{i}", t0, t1)
    tween(f"#{i} polygon", {"rotation": 0, "svgOrigin": f"{cx} {cy}"}, {"rotation": 10}, t0, max(1, round((t1 - t0) * FPS)), "none")


def squiggles(t0, t1, ly=0, z=1):
    """The white squiggle-loop pattern on maroon (reference 8.3 s)."""
    i = nid("sq")
    g = random.Random(5)
    paths = []
    for k in range(9):
        cx, cy = g.uniform(0, 1080), g.uniform(0, 1080)
        r = g.uniform(90, 170)
        paths.append(f'<path d="M{cx - r * 1.6:.0f} {cy + r:.0f} C {cx - r * 1.6:.0f} {cy - r * 1.4:.0f}, {cx + r * 1.4:.0f} {cy - r * 1.4:.0f}, '
                     f'{cx + r * .9:.0f} {cy:.0f} S {cx - r * .2:.0f} {cy + r * 1.1:.0f}, {cx:.0f} {cy + r * .1:.0f}"/>')
    put(f'<svg class="sqg" id="{i}" viewBox="0 0 1080 1080" style="z-index:{z}">{"".join(paths)}</svg>', ly)
    show(f"#{i}", t0, t1)


def cap(t, x, y, size, t0, t1=DUR, font="anton", color=WHT, how="pop1", align="left", z=6, rot=0, style="plain", sy=1.0,
        skew=0, upper=True, ly=2):
    """A caption. style: plain (thin dark outline), giant (no outline), block (magenta block shadow), sticker
    (magenta box, white frame), script (magenta brush script with a white outline), marker (dark red scribble).
    how: pop1 (letters pop in one by one, grey then their colour: the reference's signature), letters, blocks, slide-l,
    slide-r, pop, settle, rise, write (script, a light spark rides the pen), drop."""
    i = nid("tx")
    if style == "giant" and CUR.get("idx", 0) > 0 and 0 < q(t0) - CUR["t0"] < 1.5:
        t0 = CUR["t0"] + 4 * STEP
    s = t.upper() if upper else t
    pad = .28 if style == "sticker" else 0
    w_ = tw(s, size, font) + size * pad
    xl = x - (w_ / 2 if align == "center" else (w_ if align == "right" else 0))
    sty = f"left:{xl:.0f}px;top:{y:.0f}px;font-family:'{FAM[font]}';font-size:{size:.0f}px;color:{color};z-index:{z};"
    sty += f"transform:rotate({rot}deg) skewX({skew}deg) scaleY({sy});"
    if style == "plain":
        sty += f"-webkit-text-stroke:{max(3, size * .025):.0f}px {INK if color != INK else WHT};paint-order:stroke fill;"
    elif style == "block":
        k = max(4, round(size * .07))
        sty += "text-shadow:" + ",".join(f"{j}px {j}px 0 {MAG}" for j in range(1, k + 1)) + ";"
    elif style == "sticker":
        sty += (f"background:{MAG};padding:.06em .14em 0;outline:{max(4, size * .05):.0f}px solid {WHT};"
                f"-webkit-text-stroke:{max(3, size * .03):.0f}px {DRD};paint-order:stroke fill;")
    elif style == "script":
        sty += f"-webkit-text-stroke:{max(6, size * .06):.0f}px {WHT};paint-order:stroke fill;"
    elif style == "marker":
        sty += "opacity:.85;"
    chars = "".join(f'<span class="c{" cz" if c == "*" else ""}">{c if c != " " else "&nbsp;"}</span>' for c in s)
    put(f'<div class="tx" data-layout-allow-overlap id="{i}" style="{sty}">{chars}</div>', ly)
    show(f"#{i}", t0, t1)
    t0 = q(t0)
    n = len(s)
    if how == "pop1":         # one letter a frame, grey and a little large, then its own colour
        js(f'tl.set("#{i} .c", {{opacity: 0}}, {t0 - .001:.3f});')
        for k in range(n):
            tk = t0 + k * STEP
            js(f'tl.set("#{i} .c:nth-child({k + 1})", {{opacity: 1, color: "{GRY}", scale: 1.18}}, {tk:.3f});')
            js(f'tl.set("#{i} .c:nth-child({k + 1})", {{color: "{color}", scale: 1}}, {tk + 2 * STEP:.3f});')
    elif how in ("letters", "write"):
        js(f'tl.set("#{i} .c", {{opacity: 0}}, {t0 - .001:.3f});')
        per = 1 if n <= 9 else 2
        steps = max(1, (n + per - 1) // per)
        for k in range(0, n, per):
            js(f'tl.set("#{i} .c:nth-child(-n+{min(n, k + per)})", {{opacity: 1}}, {t0 + (k // per) * STEP:.3f});')
        if how == "write":
            sp = nid("spk")
            put(f'<i class="spark" id="{sp}" style="left:{xl:.0f}px;top:{y + size * .45:.0f}px;z-index:{z + 1}"></i>', ly)
            show(f"#{sp}", t0, t0 + (steps + 1) * STEP)
            for k in range(steps + 1):
                js(f'tl.set("#{sp}", {{x: {w_ * min(1, (k + 1) / steps):.0f}, y: {(-1) ** k * size * .12:.0f}}}, {t0 + k * STEP:.3f});')
    elif how == "blocks":
        for k in range(n):
            tween(f"#{i} .c:nth-child({k + 1})", {"rotationX": 90, "opacity": 0, "transformPerspective": 600},
                  {"rotationX": 0, "opacity": 1}, t0 + k * STEP, 2)
    elif how == "drop":
        for k in range(n):
            tween(f"#{i} .c:nth-child({k + 1})", {"y": -640, "filter": "url(#vblur)"}, {"y": 0, "filter": "blur(0px)"}, t0 + k * STEP, 3)
    elif how.startswith("slide"):
        enter(f"#{i}", t0, "left" if how.endswith("l") else "right")
    elif how in ("pop", "settle", "rise"):
        enter(f"#{i}", t0, how)
    if style in ("block", "giant") and n > 3:
        nn = max(2, round((t1 - t0) * FPS))
        sgn = 1 if (NID[0] % 2) else -1
        tween(f"#{i}", {"rotationY": sgn * 34, "rotationX": 12, "transformPerspective": 900, "z": -120},
              {"rotationY": sgn * 8, "rotationX": 3, "z": 0}, t0, min(nn, 16), "power3.out")
    return i


def floor_type(word, cy, t0, t1, size=330, color=WHT, ly=1, z=2):
    """Letters standing on a floor with their mirror image lying in perspective below (reference 9.3 s)."""
    up = cap(word, 540, cy - size * .95, size, t0, t1, color=color, align="center", style="giant", how="pop1", ly=ly, z=z, sy=1.1)
    i = nid("fl")
    w_ = tw(word.upper(), size)
    put(f'<div class="flr" id="{i}" style="left:{540 - w_ / 2:.0f}px;top:{cy:.0f}px;font-size:{size:.0f}px;z-index:{z}">'
        f'{word.upper()}</div>', ly)
    show(f"#{i}", t0 + len(word) * STEP, t1)
    return up


def burst(lines, x, y, r, t0, t1=DUR, z=7, color=MAG, size=None, ly=2, spin=True):
    i = nid("bu")
    g = random.Random(int(x * 7 + y))
    pts = []
    for k in range(44):
        rr = 1 if k % 2 == 0 else .84 + g.uniform(-.03, .03)
        a = k / 44 * math.tau
        pts.append(f"{50 + 50 * rr * math.cos(a):.1f}% {50 + 50 * rr * math.sin(a):.1f}%")
    size = size or r * .62 / max(1, len(lines)) * 1.6
    put(f'<div class="bu" id="{i}" style="left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r:.0f}px;height:{2 * r:.0f}px;z-index:{z}">'
        f'<b style="background:{color};clip-path:polygon({",".join(pts)})"></b>'
        f'<span style="font-size:{size:.0f}px">{"<br>".join(lines)}</span></div>', ly)
    show(f"#{i}", t0, t1)
    tween(f"#{i}", {"scale": 0, "rotation": -60}, {"scale": 1, "rotation": 0}, t0, 3)
    if spin:
        tween(f"#{i} b", {"rotation": 0}, {"rotation": 25}, t0, max(1, round((t1 - t0) * FPS)), "none")
    return i


def shards(cx, cy, rx, ry, t0, t1, seed, n=9, z=8, ly=2):
    i = nid("sh")
    g = random.Random(seed)
    groups = []
    for v in range(4):
        polys = []
        for _ in range(n):
            a = g.uniform(0, math.tau)
            px, py = cx + rx * math.cos(a) * g.uniform(.8, 1.15), cy + ry * math.sin(a) * g.uniform(.8, 1.15)
            d = a + math.pi / 2 + g.uniform(-.5, .5)
            ln, wd = g.uniform(50, 150), g.uniform(8, 20)
            ux, uy = math.cos(d), math.sin(d)
            pts = [(px - ux * ln / 2, py - uy * ln / 2), (px + uy * wd, py - ux * wd), (px + ux * ln / 2, py + uy * ln / 2)]
            col = MAG if g.random() < .7 else WHT
            polys.append(f'<polygon fill="{col}" points="' + " ".join(f"{a_:.0f},{b_:.0f}" for a_, b_ in pts) + '"/>')
        groups.append(f'<g style="opacity:0">{"".join(polys)}</g>')
    put(f'<svg class="sls" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}">{"".join(groups)}</svg>', ly)
    show(f"#{i}", t0, t1)
    for k, t in enumerate(frames(t0, t1, 3)):
        js(f'tl.set("#{i} g", {{opacity: 0}}, {t:.3f});')
        js(f'tl.set("#{i} g:nth-child({k % 4 + 1})", {{opacity: 1}}, {t:.3f});')


def swoosh_line(pts, t0, t1, width=9, z=8, ly=2, dur=.35):
    """A white curved swoosh line drawing across (reference 6.0-6.7 s)."""
    i = nid("sl")
    d = f"M{pts[0][0]} {pts[0][1]} " + " ".join(f"C {a[0]} {a[1]}, {b[0]} {b[1]}, {c[0]} {c[1]}" for a, b, c in pts[1:])
    put(f'<svg class="sb" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}"><path d="{d}" pathLength="1000" '
        f'style="stroke:{WHT};stroke-width:{width}"/></svg>', ly)
    show(f"#{i}", t0, t1)
    tween(f"#{i} path", {"strokeDashoffset": 1000}, {"strokeDashoffset": 0}, t0, max(2, round(dur * FPS)))


def scribble(pts, t0, t1=DUR, color=MAG, width=8, dur=.3, z=8, ly=2):
    i = nid("sb")
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    put(f'<svg class="sb" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}"><path d="{d}" pathLength="1000" '
        f'style="stroke:{color};stroke-width:{width}"/></svg>', ly)
    show(f"#{i}", t0, t1)
    tween(f"#{i} path", {"strokeDashoffset": 1000}, {"strokeDashoffset": 0}, t0, max(2, round(dur * FPS)))


def particles(kind, t0, t1, n, seed, z=7, ly=2, box=(0, 0, S, S)):
    """Motion on the art: embers rise, sparkles blink, diamonds fall, petals float."""
    g = random.Random(seed)
    x0, y0, x1, y1 = box
    for k in range(n):
        i = nid("pt")
        x, y = g.uniform(x0, x1), g.uniform(y0, y1)
        if kind == "ember":
            sz = g.uniform(6, 16)
            put(f'<i class="pt ember" id="{i}" style="left:{x:.0f}px;top:{y1:.0f}px;width:{sz:.0f}px;height:{sz:.0f}px;z-index:{z}"></i>', ly)
            show(f"#{i}", t0, t1)
            per = g.uniform(1.0, 1.8)
            st = t0 - g.uniform(0, per)
            while st < t1:
                tween(f"#{i}", {"y": 0, "x": 0}, {"y": -(y1 - y0) * g.uniform(.6, 1), "x": g.uniform(-90, 90)}, max(t0, st),
                      max(2, round(per * FPS)), "none")
                st += per
        elif kind == "sparkle":
            sz = g.uniform(30, 70)
            put(f'<i class="pt star" id="{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{sz:.0f}px;height:{sz:.0f}px;z-index:{z}"></i>', ly)
            show(f"#{i}", t0, t1)
            for j, t in enumerate(frames(t0 + g.uniform(0, .5), t1, g.choice([3, 4, 5]))):
                js(f'tl.set("#{i}", {{scale: {[0, .6, 1.1, .4][j % 4]}, rotation: {j * 15}}}, {t:.3f});')
        elif kind == "diamond":
            sz = g.uniform(26, 60)
            put(f'<i class="pt dia" id="{i}" style="left:{x:.0f}px;top:-80px;width:{sz:.0f}px;height:{sz * 1.2:.0f}px;z-index:{z}"></i>', ly)
            show(f"#{i}", t0, t1)
            per = g.uniform(.9, 1.5)
            st = t0 - g.uniform(0, per)
            while st < t1:
                tween(f"#{i}", {"y": 0, "rotation": 0}, {"y": S + 160, "rotation": g.uniform(-200, 200)}, max(t0, st),
                      max(2, round(per * FPS)), "none")
                st += per
        elif kind == "petal":
            sz = g.uniform(18, 34)
            put(f'<i class="pt petal" id="{i}" style="left:{x:.0f}px;top:-60px;width:{sz:.0f}px;height:{sz * .6:.0f}px;z-index:{z}"></i>', ly)
            show(f"#{i}", t0, t1)
            per = g.uniform(2.2, 3.4)
            st = t0 - g.uniform(0, per)
            while st < t1:
                tween(f"#{i}", {"y": 0, "x": 0, "rotation": 0}, {"y": S + 120, "x": g.uniform(-260, 260), "rotation": g.uniform(-360, 360)},
                      max(t0, st), max(2, round(per * FPS)), "none")
                st += per


def phone_card(x, y, w, caller, t0, t1, press, button="accept", z=4, ly=1):
    i = nid("call")
    h = w * 1792 / 828
    bx, col = ("79%", "#3fd25c") if button == "accept" else ("21%", "#ff3b30")
    put(f'<div class="call" id="{i}" style="left:{x}px;top:{y}px;width:{w:.0f}px;height:{h:.0f}px;z-index:{z}">'
        f'<img src="assets/img/src/incoming_call.jpg" alt=""><b>{caller}</b><small>mobile</small>'
        f'<i class="hit" style="left:{bx};top:77%;background:{col}"></i></div>', ly)
    show(f"#{i}", t0, t1)
    if not (CUR.get("idx", 0) > 0 and abs(q(t0) - CUR["t0"]) < .16):
        enter(f"#{i}", t0, "tilt")
    tt, k = q(t0) + .3, 0
    while tt < press - .1:
        js(f'tl.set("#{i} .hit", {{opacity: {.5 if k % 2 == 0 else 0}, scale: {1.6 if k % 2 == 0 else 1}}}, {tt:.3f});')
        tt, k = tt + .2, k + 1
    js(f'tl.set("#{i} .hit", {{opacity: .9, scale: 1.35}}, {q(press):.3f});')     # the press: a flash on the button, then it settles
    js(f'tl.set("#{i} .hit", {{opacity: .55, scale: 1.1}}, {q(press) + 2 * STEP:.3f});')
    js(f'tl.set("#{i} .hit", {{opacity: 0, scale: 1}}, {q(press) + 4 * STEP:.3f});')
    return i


def white(t, n=1):
    js(f'tl.set("#flash", {{opacity: 1}}, {q(t):.3f});')
    js(f'tl.set("#flash", {{opacity: 0}}, {q(t) + n * STEP:.3f});')


def beats_in(t0, t1, every=4, off=0):
    return [q(b) for b in BEATS[off::every] if t0 + .2 < b < t1 - .25]


# ------------------------------------------------------------------------------------------------ scenes
SCENES = []        # [t0, t1, id, bg, layers, drift, transition-in]


def scene(t0, t1, bg=INK, drift=(0, 0), trans="whip"):
    i = f"sc{len(SCENES)}"
    CUR["ly"] = [[], [], []]
    CUR["t0"], CUR["idx"] = q(t0), len(SCENES)
    SCENES.append([q(t0), q(t1), i, bg, CUR["ly"], drift, trans])


def build():
    E = [lt(k) for k in range(len(L))] + [DUR]

    # S0 the drop: Drake from behind on a rounded card that swings in over a magenta starburst; sunburst rays;
    # DRAKE / 21 SAVAGE stickers; the brush "Spin" and BOUT U popping in.
    scene(0, E[0], trans="")
    rays(0, E[0])
    burst([""], 800, 330, 330, .1, E[0], z=1, ly=0)
    photo("drake_back_jacket", 230, 170, 620, 760, -2, 0, E[0], kind="print", how="tilt", card=True, round_=True, push=.08,
          pos="object-position:50% 100%;transform:scale(1.9);transform-origin:50% 92%", z=2)
    cap("Drake", 70, 90, 92, .35, E[0], style="sticker", how="pop", rot=-4, ly=1)
    cap("21 Savage", 620, 880, 70, .6, E[0], style="sticker", how="pop", rot=-3, ly=1)
    cap("Spin", 540, 260, 280, 1.1, E[0], font="script", color=MAG, align="center", style="script", rot=-8, upper=False, how="settle")
    cap("Bout U", 540, 560, 190, 1.3, E[0], font="archivo", align="center", style="block", how="pop1")

    # S1 Jealous-**** ****, yeah: the whispering girls on a tilted rounded card over JEALOUS (giant, behind).
    li = 0
    scene(E[0], E[1], bg=MAR, drift=(-12, 0), trans="whip")
    cap("JEALOUS", 540, 300, fit("JEALOUS", 1050, 420), at(li, 0), E[1], align="center", style="giant", how="pop1", ly=0, z=2, sy=1.15)
    para(650, 120, 380, 820, MAG, E[0], E[1], z=1)
    photo("jealous", 200, 170, 680, 680, -3, E[0] + .1, E[1], kind="afull", how="tilt", card=True, round_=True, clip="jealous",
          sweeps=(at(li, 2),), punches=((at(li, 3), 1.08),), z=3)
    cap(text(li, 1, 2) + ",", 70, 890, 96, at(li, 1), E[1], style="sticker", how="pop", rot=-4)
    cap("yeah", 840, 830, 180, at(li, 3), E[1], font="script", color=MAG, style="script", upper=False, rot=-8, how="write", align="center")

    # S2 And I know what I said 'bout bein' in Vogue: the cat Vogue cover swings in on a magenta cone; the words
    # stack with magenta block shadows; Vogue in brush.
    li = 1
    scene(E[1], E[2], drift=(10, 0), trans="zoomwhite")
    cone(E[1], E[2], cx=800, top=420)
    photo("vogue_cat_cover", 590, 120, 440, 620, 5, lt(li), E[2], kind="print", how="tilt", card=True, z=2)
    for k, (a_, b_) in enumerate(((0, 2), (3, 5), (6, 8))):
        t_ = text(li, a_, b_)
        cap(t_, 50, 110 + k * 160, fit(t_.upper(), 500, 110, "archivo"), at(li, a_), E[2], font="archivo", style="block", how="pop1")
    cap("Vogue", 380, 740, 260, at(li, 9), E[2], font="script", color=MAG, style="script", upper=False, rot=-9, how="write", align="center", z=9)

    # S3 But just like that R&B group from the '90s: R&B giant behind En Vogue's card, GROUP with a block shadow,
    # a '90s starburst.
    li = 2
    scene(E[2], E[3], bg=MAR, drift=(0, 10), trans="badge")
    cap("R&B", 540, 120, fit("R&B", 1000, 520), at(li, 4), E[3], align="center", style="giant", how="pop1", ly=0, z=2, sy=1.1)
    photo("envogue_funky_divas", 240, 250, 600, 540, -3, lt(li), E[3], kind="print", how="swing", card=True, z=3)
    cap(text(li, 0, 3), 540, 30, 64, at(li, 0), E[3], font="archivo", align="center", style="block", how="pop1", z=8)
    cap("GROUP", 540, 800, 170, at(li, 5), E[3], font="archivo", align="center", style="block", how="pop1")
    burst(["'90S"], 880, 270, 150, at(li, 8), E[3], size=96)
    cap(text(li, 6, 7), 80, 760, 64, at(li, 6), E[3], style="sticker", how="pop", rot=-5)

    # S4 Girl, one call, I'll get you in Vogue: ONE CALL giant behind the hand and the phone; Girl in brush; the call
    # answered on "Vogue".
    li = 3
    scene(E[3], E[4], drift=(-12, 0), trans="push")
    cap("ONE", 40, 120, 330, at(li, 1), E[4], style="giant", how="pop1", ly=0, z=2, sy=1.2)
    cap("CALL", 40, 480, 330, at(li, 2), E[4], style="giant", how="pop1", ly=0, z=2, sy=1.2)
    para(560, 60, 420, 900, MAG, E[3], E[4], z=1)
    phone_card(640, 110, 360, "Vogue", lt(li), E[4], press=at(li, 7))
    photo("hand_phone_sticker", 60, 520, 500, None, -8, at(li, 1), E[4], how="rise", push=0, z=5)
    cap("Girl,", 60, 40, 170, at(li, 0), E[4], font="script", color=MAG, style="script", upper=False, rot=-8, how="write")
    cap(text(li, 3, 6), 820, 940, 60, at(li, 3), E[4], style="sticker", how="pop", align="center")

    # S5 One call, you in runway shows: the pearl cat page on a magenta cone, RUNWAY wide with a block shadow,
    # shows in brush.
    li = 4
    scene(E[4], E[5], bg=MAR, drift=(0, -12), trans="drop")
    cone(E[4], E[5], cx=540, top=520)
    photo("rolex_cat_ad", 300, 40, 480, 1000, 0, lt(li), E[5], kind="print", how="settle", z=2, push=.07)
    cap(text(li, 0, 3), 540, 40, 70, at(li, 0), E[5], font="archivo", align="center", how="pop1")
    cap("RUNWAY", 540, 610, fit("RUNWAY", 1000, 240, "archivo"), at(li, 4), E[5], font="archivo", align="center", style="block",
        rot=-6, how="pop1", ly=2)
    cap("shows", 800, 830, 190, at(li, 5), E[5], font="script", color=MAG, style="script", upper=False, rot=-8, how="write", align="center")

    # S6 One call, I'm sittin' front row: Drake in Chanel on a magenta panel, FRONT ROW giant behind him.
    li = 5
    scene(E[5], E[6], drift=(-14, 0), trans="strips")
    para(220, 140, 640, 860, MAG, E[5], E[6], z=1)
    cap("FRONT", 540, 70, fit("FRONT", 1040, 440), at(li, 4), E[6], align="center", style="giant", how="pop1", ly=1, z=2, sy=1.1)
    cap("ROW", 540, 520, fit("ROW", 1040, 480), at(li, 5), E[6], align="center", style="giant", how="pop1", ly=1, z=2, sy=1.1)
    photo("drake_chanel_night", 300, 170, 560, None, 0, lt(li), E[6], how="swing", push=.06, z=3)
    cap(text(li, 0, 1), 50, 50, 90, at(li, 0), E[6], style="sticker", how="pop", rot=-3)
    cap("sittin'", 640, 860, 180, at(li, 2), E[6], font="script", color=MAG, style="script", upper=False, rot=-8, how="write", align="center", z=9)

    # S7 One wrong call from your ex ****...: the same phone, the ex declined; then the dumb cat, SENT HOME.
    li = 6
    mid = at(li, 8)
    scene(E[6], E[7], drift=(0, 0), trans="glitchcard")
    cap("WRONG", 40, 70, fit("WRONG", 600, 270), at(li, 1), mid, style="giant", how="pop1", ly=0, z=3, sy=1.2)
    cap("CALL", 40, 400, fit("CALL", 600, 270), at(li, 2), mid, style="giant", how="pop1", ly=0, z=3, sy=1.2)
    phone_card(620, 120, 380, "Ex", lt(li), mid, press=at(li, 5), button="decline")
    cap(text(li, 3, 6), 40, 900, 76, at(li, 3), mid, style="sticker", how="pop", rot=-3)
    scribble([(660, 180), (980, 880)], at(li, 5) + .1, mid, width=22, dur=.15, z=9)
    scribble([(980, 180), (660, 880)], at(li, 5) + .2, mid, width=22, dur=.15, z=9)
    panel(0, 0, S, S, MAR, mid, E[7], how="", z=0)
    para(560, 120, 440, 760, MAG, mid, E[7], z=1)
    photo("cat_white_dumb", 220, 190, 600, 560, 3, mid, E[7], kind="print", how="tilt", push=.08, z=2, card=True, slices=(mid + .5,))
    cap(text(li, 7, 7), 60, 50, 100, at(li, 7), E[7], font="archivo", how="pop1")
    cap(text(li, 9, 11), 1020, 60, 84, at(li, 9), E[7], style="sticker", align="right", how="pop")
    burst(["DUMB"], 880, 600, 150, at(li, 8), E[7], size=96)
    cap("SENT HOME", 540, 790, fit("SENT HOME", 900, 180), at(li, 12), E[7], align="center", style="sticker", how="pop", rot=-4)

    # S8 One call and my **** ten toes: the crew on a magenta panel, TEN TOES giant behind them.
    li = 7
    scene(E[7], E[8], bg=MAR, drift=(0, -10), trans="whip")
    cap("TEN", 540, 10, 430, at(li, 5), E[8], align="center", style="giant", how="pop1", ly=1, z=2, sy=1.12)
    cap("TOES", 540, 420, 400, at(li, 6), E[8], align="center", style="giant", how="pop1", ly=1, z=2, sy=1.12)
    para(250, 380, 580, 600, MAG, E[7], E[8], z=1)
    shards(540, 640, 380, 300, at(li, 5), E[8], 21)
    photo("crew", 220, 400, 640, None, 0, E[7], E[8], kind="acut", how="", push=.05, wind=.03, breathe=True,
          sweeps=(at(li, 5),), z=3)
    cap(text(li, 0, 4), 540, 990, 56, at(li, 0), E[8], style="sticker", align="center", how="pop")

    # S9 Down to go wherever I say go: he points down the lens, she looks; WHEREVER with a block shadow, I say go.
    li = 8
    scene(E[8], E[9], drift=(0, 0), trans="slideup")
    photo("point", -40, -40, 1160, 1160, 0, E[8], E[9], kind="afull", how="settle", push=.05, z=1, ly=0, wind=.02,
          punches=((at(li, 3), 1.1), (at(li, 6), 1.2)))
    cap(text(li, 0, 2), 50, 50, 90, at(li, 0), E[9], style="sticker", how="pop", rot=-3)
    cap("WHEREVER", 540, 780, fit("WHEREVER", 980, 200, "archivo"), at(li, 3), E[9], font="archivo", align="center", style="block",
        rot=-6, how="pop1")
    cap("I say go", 790, 150, 130, at(li, 4), E[9], font="script", color=MAG, style="script", upper=False, rot=-10, how="write", align="center", z=9)
    white(at(li, 6))

    # S10 Even if we gotta travel 'cross the globe: the jet window, city lights twinkling; 'CROSS THE GLOBE.
    li = 9
    scene(E[9], E[10], drift=(0, 12), trans="diag")
    photo("jet", -40, -40, 1160, 1160, 0, E[9], E[10], kind="afull", how="", push=.08, z=1, ly=0, wind=.015)
    particles("sparkle", E[9], E[10], 10, 10, box=(640, 120, 1040, 640))
    cap(text(li, 0, 3), 540, 40, 70, at(li, 0), E[10], font="archivo", align="center", how="pop1")
    cap("'CROSS THE GLOBE", 540, 860, fit("'CROSS THE GLOBE", 1000, 150, "archivo"), at(li, 5), E[10], font="archivo",
        align="center", style="block", how="pop1")
    cap("travel", 300, 640, 190, at(li, 4), E[10], font="script", color=MAG, style="script", upper=False, rot=-10, how="write", align="center", z=9)

    # S11 Down to take you to the end of the road, for real: wide block words pop in letter by letter with white
    # swoosh lines (reference PRAY / MORE / THAN), the road picture set in the stack; then the road full frame.
    li = 10
    fr = at(li, 9) + .7
    scene(E[10], E[11], drift=(-20, 0), trans="zoomwhite")
    cap("TO THE", 60, 90, 150, at(li, 4), fr, font="dela", color=MAG, how="pop1", ly=1)
    cap("END", 60, 300, 230, at(li, 6), fr, font="dela", how="pop1", ly=1)
    photo("road", 600, 300, 420, 300, 4, at(li, 6), fr, kind="afull", how="tilt", push=.1, z=3, card=True)
    cap("OF THE", 60, 600, 150, at(li, 7), fr, font="dela", color=MAG, how="pop1", ly=1)
    cap("ROAD", 60, 790, 230, at(li, 9), fr, font="dela", how="pop1", ly=1)
    cap(text(li, 0, 3), 60, 30, 50, at(li, 0), fr, font="archivo", how="pop1", ly=1)
    swoosh_line([(-40, 80), ((300, -60), (700, 260), (1120, 40))], at(li, 4), fr)
    swoosh_line([(-40, 1000), ((260, 760), (520, 1100), (700, 860)), ((820, 700), (980, 900), (1120, 760))], at(li, 7), fr)
    photo("road", -40, -40, 1160, 1160, 0, fr, E[11], kind="afull", how="settle", push=.06, z=5, ly=1, clip="road")
    cap("for real", 540, 800, 220, at(li, 10), E[11], font="script", color=MAG, style="script", upper=False, rot=-8, how="write", align="center")
    white(fr)

    # S12 hook 1: her card swings in over THE WAY (giant); YOU in a starburst; MAKE ME sticker; on "feel" his card
    # pushes in beside hers (the reference's collage build), FEEL giant, these days in brush.
    li = 11
    fe = at(li, 5)
    scene(E[11], E[12], bg=MAR, drift=(0, -10), trans="glitchcard")
    cap("THE WAY", 540, 40, fit("THE WAY", 1040, 330), at(li, 0), fe, align="center", style="giant", how="pop1", ly=0, z=2, sy=1.1)
    her = photo("her_blush", 220, 230, 640, 640, -4, E[11] + .1, E[12], kind="afull", how="tilt", card=True, round_=True,
                clip="her_blush", push=.05, z=3)
    tween(f"#{her}", {"x": 0, "scale": 1}, {"x": -230, "scale": .82}, fe, 4)
    particles("sparkle", E[11], E[12], 8, 12, box=(150, 150, 950, 800))
    particles("petal", E[11], E[12], 12, 13)
    burst(["YOU"], 870, 760, 160, at(li, 2), fe, size=110)
    cap("MAKE ME", 80, 900, 90, at(li, 3), fe, style="sticker", how="pop", rot=-4)
    cap("FEEL", 540, 40, fit("FEEL", 1040, 520), fe, E[12], align="center", style="giant", how="pop1", ly=0, z=2, sy=1.1)
    photo("him_smitten", 470, 250, 560, 560, 5, fe, E[12], kind="afull", how="right", card=True, round_=True, clip="him_smitten",
          push=.05, z=4)
    cap("these days", 540, 850, 180, at(li, 6), E[12], font="script", color=MAG, style="script", upper=False, rot=-7, how="write", align="center", z=9)
    for b in beats_in(fe, E[12], 4, 0):
        white(b)

    # S13 Somethin' gettin' dropped for you, baby girl: diamonds pour into her hands; DROPPED falls in; diamonds rain;
    # BABY GIRL starburst.
    li = 12
    scene(E[12], E[13], drift=(0, 12), trans="push")
    rays(E[12], E[13], cx=1080, cy=0)
    cap("DROPPED", 540, 50, fit("DROPPED", 1040, 380), at(li, 2), E[13], align="center", style="giant", how="drop", ly=1, z=2, sy=1.15)
    photo("diamonds", 230, 280, 600, 600, 3, lt(li), E[13], kind="afull", how="swing", card=True, round_=True, wind=.02, push=.08,
          sweeps=(at(li, 2),), z=3)
    cap(text(li, 0, 1), 50, 960, 64, at(li, 0), E[13], font="archivo", how="pop1")
    cap(text(li, 3, 4) + ",", 1030, 560, 90, at(li, 3), E[13], style="sticker", align="right", how="pop", rot=4)
    burst(["BABY", "GIRL"], 860, 860, 170, at(li, 5), E[13], size=86)
    particles("diamond", at(li, 2), E[13], 16, 15)
    particles("sparkle", E[12], E[13], 6, 16)

    # S14 Smoke a **** top for you, baby girl: his face in the smoke, the smoke flowing, red eyes; SMOKE giant.
    li = 13
    scene(E[13], E[14], drift=(10, -8), trans="drop")
    photo("smoke", -40, -40, 1160, 1160, 0, E[13], E[14], kind="afull", how="settle", push=.08, z=1, ly=0, flow="smoke", wind=.012,
          punches=((at(li, 3), 1.12), (at(li, 6), 1.0)))
    cap("SMOKE", 40, 40, fit("SMOKE", 720, 320), at(li, 0), E[14], style="giant", how="pop1", sy=1.15)
    cap(text(li, 1, 3), 40, 420, 96, at(li, 1), E[14], style="sticker", how="pop", rot=-3)
    cap(text(li, 4, 5), 1030, 760, 90, at(li, 4), E[14], font="archivo", style="block", align="right", how="pop1")
    cap("baby girl", 540, 880, 170, at(li, 6), E[14], font="script", color=MAG, style="script", upper=False, rot=-7, how="write", align="center")

    # S15 Burn somebody block for you: he walks out of the burning block, the flames flowing, embers rising.
    li = 14
    scene(E[14], E[15], drift=(0, -10), trans="whip")
    photo("fire", -40, -40, 1160, 1160, 0, E[14], E[15], kind="afull", how="settle", push=.1, z=1, ly=0, flow="fire", wind=.012)
    particles("ember", E[14], E[15], 24, 18, z=3, ly=1)
    b = cap("BURN", 540, 30, fit("BURN", 1000, 380), at(li, 0), E[15], align="center", style="giant", how="pop1", sy=1.15)
    for k, t in enumerate(frames(at(li, 0) + .3, E[15], 2)):
        js(f'tl.set("#{b} .c", {{color: "{[WHT, MAG][k % 2]}"}}, {t:.3f});')
    cap("SOMEBODY BLOCK", 540, 790, fit("SOMEBODY BLOCK", 980, 150, "archivo"), at(li, 1), E[15], font="archivo", align="center",
        style="block", rot=-5, how="pop1")
    cap(text(li, 3, 4), 60, 980, 64, at(li, 3), E[15], style="sticker", how="pop")

    # S16 hook 2: he spins her on the squiggle pattern, THE WAY black behind them; punch-ins on the bars.
    li = 15
    scene(E[15], E[16], bg=MAR, drift=(0, 0), trans="badge")
    squiggles(E[15], E[16])
    panel(60, 120, 960, 330, INK, E[15], E[16], how="left", z=2, ly=0)
    cap("THE WAY", 540, 140, fit("THE WAY", 920, 300), at(li, 0), E[16], align="center", style="giant", how="pop1", ly=0, z=3, sy=1.05)
    pb = beats_in(E[15], E[16], 4, 2)
    photo("spin", 170, 210, 740, 740, -3, E[15], E[16], kind="afull", how="tilt", card=True, round_=True, clip="spin", push=.04,
          punches=[(t, [1.08, 1.0][k % 2]) for k, t in enumerate(pb)], z=4)
    burst(["YOU"], 930, 400, 120, at(li, 2), E[16], size=84)
    shards(540, 580, 420, 380, at(li, 5), E[16], 25)
    cap("MAKE ME FEEL", 540, 860, fit("MAKE ME FEEL", 1000, 170, "archivo"), at(li, 3), E[16], font="archivo", align="center",
        style="block", rot=-4, how="pop1")
    cap("these days", 720, 680, 130, at(li, 6), E[16], font="script", color=MAG, style="script", upper=False, rot=-7, how="write", align="center", z=9)
    particles("sparkle", E[15], E[16], 8, 19)

    # S17 Comin' out my body for you, baby girl: his spirit rising out of him on a magenta cone, MY BODY giant behind.
    li = 16
    scene(E[16], E[17], drift=(0, -14), trans="strips")
    cone(E[16], E[17], cx=540, top=440)
    cap("COMIN' OUT", 540, 40, fit("COMIN' OUT", 1000, 150, "dela"), at(li, 0), E[17], font="dela", align="center", how="pop1")
    cap("MY BODY", 540, 280, fit("MY BODY", 1040, 380), at(li, 2), E[17], align="center", style="giant", how="pop1", ly=1, z=2, sy=1.15)
    shards(540, 560, 400, 420, at(li, 1), E[17], 22)
    sp = photo("spirit", 170, 220, 740, None, 0, lt(li), E[17], kind="acut", how="", push=.06, wind=.05, breathe=True, z=3)
    js(f'tl.fromTo("#{sp}", {{filter: "drop-shadow(0 0 0px #fff)"}}, {{filter: "drop-shadow(0 0 34px #fff)", duration: {6 * STEP:.3f}, '
       f'ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, {at(li, 1):.3f});')
    cap(text(li, 4, 5), 60, 960, 64, at(li, 4), E[17], style="sticker", how="pop")
    cap("baby girl", 780, 860, 170, at(li, 6), E[17], font="script", color=MAG, style="script", upper=False, rot=-7, how="write", align="center", z=9)

    # S18 Wipe him like he snotty for you, baby girl: the crying rival wiped down; a magenta wipe on "Wipe".
    li = 17
    scene(E[17], E[18], bg=MAR, drift=(0, 8), trans="slideup")
    cap("WIPE HIM", 540, 40, fit("WIPE HIM", 1040, 330), at(li, 0), E[18], align="center", style="giant", how="pop1", ly=0, z=2, sy=1.12)
    para(330, 300, 600, 700, MAG, E[17], E[18], z=1)
    shards(670, 560, 320, 320, at(li, 4), E[18], 24)
    photo("snotty", 380, 270, 580, None, 0, lt(li), E[18], kind="acut", how="swing", push=.06, wind=.03, breathe=True, z=3)
    w_ = panel(-60, 0, 1200, S, MAG, at(li, 0), at(li, 0) + .4, how="", z=9, ly=2)
    tween(f"#{w_}", {"x": -1300}, {"x": 1300}, at(li, 0), 6)
    cap(text(li, 2, 3), 50, 400, 100, at(li, 2), E[18], style="sticker", how="pop", rot=-4)
    cap("snotty", 560, 780, 210, at(li, 4), E[18], font="script", color=MAG, style="script", upper=False, rot=-7, how="write", align="center", z=9)
    cap(text(li, 5, 6), 50, 560, 64, at(li, 5), E[18], font="archivo", style="block", how="pop1")
    burst(["BABY", "GIRL"], 180, 870, 150, at(li, 7), E[18], size=76)

    # S19 Comin' out my body for you: the two of them back to back standing on MY BODY floor type, sunburst rays;
    # the end flashes white, glitches and cuts to black.
    li = 18
    scene(E[18], DUR, drift=(0, -10), trans="zoomwhite")
    rays(E[18], DUR, cx=1080, cy=0)
    floor_type("MY BODY", 760, at(li, 2), DUR, size=fit("MY BODY", 1040, 300))
    shards(540, 500, 330, 340, E[18], DUR, 23)
    photo("finale", 290, 250, 500, None, 0, E[18], DUR, kind="acut", how="", push=.05, wind=.035, breathe=True,
          sweeps=(at(li, 3),), z=3)
    cap(text(li, 0, 1), 40, 40, 110, at(li, 0), DUR, font="archivo", style="block", rot=-6, how="pop1")
    cap("for you", 820, 900, 150, at(li, 4), DUR, font="script", color=MAG, style="script", upper=False, rot=-8, how="write", align="center", z=9)


# The anime-edit reference (Video-15991, 12 fps) cuts every 0.7-1 s in 1-2 frames: radial zoom-blur punches, a
# negative silhouette frame, spin blurs, a white frame with lightning bolts, a zoom into a speed-line tunnel; every
# cut lands on a whip swoosh. These keep the Spin Bout U reference's whip panel and glitch card in the rotation.
TRANS = ["zoom", "neg", "spin", "whip", "bolt", "zoom", "glitchcard", "neg", "tunnel", "spin", "zoom", "bolt", "whip", "neg",
         "spin", "tunnel", "zoom", "bolt", "neg"]
SFX = []


def bolts(t, n=2):
    """Lightning bolts across the frame for n frames (reference 3.08 s and 7.2 s)."""
    js(f'tl.set("#bolt", {{opacity: 1}}, {q(t):.3f});')
    for k in range(n):
        js(f'tl.set("#bolt g", {{opacity: 0}}, {q(t) + k * STEP:.3f});')
        js(f'tl.set("#bolt g:nth-child({k % 3 + 1})", {{opacity: 1}}, {q(t) + k * STEP:.3f});')
    js(f'tl.set("#bolt", {{opacity: 0}}, {q(t) + n * STEP:.3f});')


def streaks(t, n=3, op=.9):
    for k in range(n):            # stepped: bright, then expanding and fading
        js(f'tl.set("#streaks", {{opacity: {op * (1 - k / n):.2f}, scale: {.8 + .8 * k / max(1, n - 1):.2f}}}, {q(t) + k * STEP:.3f});')
    js(f'tl.set("#streaks", {{opacity: 0}}, {q(t) + n * STEP:.3f});')


def transitions():
    """Fast cuts (2-4 frames at 20 fps). t = the cut: the old scene gets the frames before it, the new one after."""
    for k in range(1, len(SCENES)):
        t, _, cur, _, _, _, _ = SCENES[k]
        prev = SCENES[k - 1][2]
        kind = TRANS[(k - 1) % len(TRANS)]
        p1, p2 = t - STEP, t - 2 * STEP
        SFX.append({"t": round(t, 3), "kind": "whip", "gain": .34})
        if kind == "zoom":          # radial zoom-blur punch into the old shot, the new one snaps out of the blur
            tween(f"#{prev}", {"scale": 1, "filter": "blur(0px)"}, {"scale": 1.7, "filter": "blur(16px)"}, p2, 2, "power2.in")
            streaks(p1, 4)
            tween(f"#{cur}", {"scale": 1.55, "filter": "blur(16px) brightness(1.4)"}, {"scale": 1, "filter": "blur(0px) brightness(1)"}, t, 3, "power3.out")
        elif kind == "neg":         # a punch-in, one negative silhouette frame of the new shot, then the shot
            tween(f"#{prev}", {"scale": 1}, {"scale": 1.25}, p2, 2, "power2.in")
            js(f'tl.set("#{cur}", {{filter: "invert(1) grayscale(1) contrast(5) brightness(1.1)"}}, {t:.3f});')
            js(f'tl.set("#{cur}", {{filter: "invert(1) grayscale(1) contrast(2) blur(3px)"}}, {t + STEP:.3f});')
            js(f'tl.set("#{cur}", {{filter: "none"}}, {t + 2 * STEP:.3f});')
            tween(f"#{cur}", {"scale": 1.18}, {"scale": 1}, t, 4, "power3.out")
        elif kind == "spin":        # spin blur out and back in the other way
            tween(f"#{prev}", {"rotation": 0, "scale": 1, "filter": "blur(0px)"}, {"rotation": 24, "scale": 1.45, "filter": "blur(14px)"}, p2, 2, "power2.in")
            tween(f"#{cur}", {"rotation": -24, "scale": 1.45, "filter": "blur(14px)"}, {"rotation": 0, "scale": 1, "filter": "blur(0px)"}, t, 4, "power3.out")
            streaks(t, 3, .6)
        elif kind == "whip":        # smear out; maroon streak frame with a light line; the new shot slides in as a tilted panel
            tween(f"#{prev}", {"x": 0, "filter": "blur(0px)"}, {"x": -700, "filter": "url(#hblur)"}, p2, 2, "power2.in")
            js(f'tl.set("#streak", {{opacity: 1}}, {t:.3f});')
            tween("#streak .ln", {"x": -100}, {"x": 1180}, t, 2)
            tween("#streak .sp", {"x": 400}, {"x": -900}, t, 2)
            js(f'tl.set("#streak", {{opacity: 0}}, {t + 2 * STEP:.3f});')
            js(f'tl.set("#mbg", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#mbg", {{opacity: 0}}, {t + 5 * STEP:.3f});')
            tween(f"#{cur}", {"clipPath": "polygon(100% 0%, 100% 0%, 100% 100%, 92% 100%)", "x": 160},
                  {"clipPath": "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)", "x": 0}, t + STEP, 3, "power3.out")
        elif kind == "bolt":        # white frame with lightning bolts and the new shot as a black silhouette, then the shot
            tween(f"#{prev}", {"scale": 1, "filter": "blur(0px)"}, {"scale": 1.3, "filter": "blur(10px)"}, p2, 2, "power2.in")
            js(f'tl.set("#{cur}", {{filter: "grayscale(1) brightness(2.2) contrast(6)"}}, {t:.3f});')
            js(f'tl.set("#{cur}", {{filter: "none"}}, {t + 2 * STEP:.3f});')
            bolts(t, 2)
            tween(f"#{cur}", {"scale": 1.2}, {"scale": 1}, t, 4, "power3.out")
            SFX.append({"t": round(t, 3), "kind": "boom", "gain": .3})
        elif kind == "tunnel":      # the old shot zooms into a speed-line tunnel, the new shot flies out of it
            tween(f"#{prev}", {"scale": 1, "filter": "blur(0px)"}, {"scale": 2.2, "filter": "blur(20px)"}, t - 3 * STEP, 3, "power2.in")
            js(f'tl.set("#tunnel", {{opacity: 1}}, {p1:.3f});')
            tween("#tunnel", {"scale": 1, "rotation": 0}, {"scale": 2.4, "rotation": 14}, p1, 3, "power2.in")
            js(f'tl.set("#tunnel", {{opacity: 0}}, {t + 2 * STEP:.3f});')
            tween(f"#{cur}", {"scale": .25, "filter": "blur(10px)"}, {"scale": 1, "filter": "blur(0px)"}, t + STEP, 4, "power3.out")
            SFX.append({"t": round(t, 3), "kind": "riser", "gain": .26})
            SFX.append({"t": round(t, 3), "kind": "drop", "len": .14})
        elif kind == "glitchcard":  # white, the old shot sliced into shifted grey bands, a small turned card zooms up on white
            white(p2)
            js(f'tl.set("#stage", {{filter: "url(#gslice) grayscale(1) contrast(1.5)"}}, {p1:.3f});')
            js(f'tl.set("#stage", {{filter: "none"}}, {t:.3f});')
            js(f'tl.set("#{prev}", {{display: "none"}}, {t:.3f});')
            js(f'tl.set("#wbg", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#wbg", {{opacity: 0}}, {t + 5 * STEP:.3f});')
            tween(f"#{cur}", {"scale": .3, "rotation": -24, "borderRadius": 60, "filter": "blur(4px)"},
                  {"scale": 1, "rotation": 0, "borderRadius": 0, "filter": "blur(0px)"}, t, 5, "power3.out")
        # beat punches inside long scenes: a quick zoom snap with streaks and a tick, every other bar
        t1 = SCENES[k][1]
        for b in beats_in(t + .6, t1 - .4, 8, 4):
            streaks(b, 2, .45)
            SFX.append({"t": round(b, 3), "kind": "snap", "gain": .16})
    end = q(59.45)              # the end: a white frame, a slice glitch, black
    white(end)
    js(f'tl.set("#stage", {{filter: "url(#gslice) grayscale(1) contrast(1.5)"}}, {end + STEP:.3f});')
    js(f'tl.set("#flash", {{opacity: 0}}, {end + STEP:.3f});')
    js(f'tl.set("#blk", {{opacity: 1}}, {end + 2 * STEP:.3f});')
    SFX.append({"t": round(end, 3), "kind": "whip", "gain": .34})
    json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx.json"), "w"), indent=0)


def drifts():
    """Slow, smooth drift per scene (no shake): background, subject and overlay type at different rates."""
    for k_, (t0, t1, i, bg, lys, (dx, dy), _) in enumerate(SCENES):
        if not dx and not dy:          # every scene travels (the reference never sits still)
            dx = 14 if k_ % 2 else -14
        n = max(1, round((t1 - t0) * FPS)) + 6
        for k, (f, z) in enumerate(((1.2, .03), (3.0, .07), (4.5, .1))):
            rr = (2.5 if k_ % 2 else -2.5) * (k / 2)
            js(f'tl.fromTo("#{i} .ly{k}", {{x: 0, y: 0, scale: 1, rotation: 0}}, {{x: {dx * f:.0f}, y: {dy * f:.0f}, scale: {1 + z:.3f}, rotation: {rr:.2f}, '
               f'duration: {n * STEP:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')


def bolt_svg():
    g = random.Random(11)
    out = []
    for v in range(3):
        paths = []
        for k in range(3):
            x, y = g.uniform(-100, 300), g.uniform(-80, 1080)
            pts = [(x, y)]
            for j in range(7):
                x += g.uniform(110, 190)
                y += g.uniform(-170, 170)
                pts.append((x, y))
            d = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts)
            paths.append(f'<path d="{d}" stroke="{INK}" stroke-width="34"/><path d="{d}" stroke="{MAG}" stroke-width="18"/>')
        out.append(f"<g>{''.join(paths)}</g>")
    return "".join(out)


CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Archivo Black"; src: url("assets/fonts/ArchivoBlack.ttf"); }}
@font-face {{ font-family: "Dela Gothic One"; src: url("assets/fonts/DelaGothicOne.ttf"); }}
@font-face {{ font-family: "Kaushan Script"; src: url("assets/fonts/KaushanScript.ttf"); }}
@font-face {{ font-family: "Permanent Marker"; src: url("assets/fonts/PermanentMarker.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {S}px; height: {S}px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: {S}px; height: {S}px; overflow: hidden; background: {INK}; }}
#stage {{ position: absolute; inset: 0; }}
#wbg {{ position: absolute; inset: 0; background: {WHT}; opacity: 0; z-index: 0; }}
#mbg {{ position: absolute; inset: 0; background: {MAR}; opacity: 0; z-index: 0; }}
.sc {{ position: absolute; inset: 0; overflow: hidden; opacity: 0; }}
.ly0, .ly1, .ly2 {{ position: absolute; inset: 0; }}
.ly1 {{ z-index: 2; }} .ly2 {{ z-index: 3; }}
.pn {{ position: absolute; display: block; }}
.sls {{ position: absolute; inset: 0; width: {S}px; height: {S}px; overflow: visible; }}
.rays, .sqg {{ position: absolute; inset: 0; width: {S}px; height: {S}px; }}
.sqg path {{ fill: none; stroke: {WHT}; stroke-width: 46; stroke-linecap: round; opacity: .9; }}
.ph {{ position: absolute; }}
.ph .pu, .ph .br, .ph .in, .ph .slc, .ph .slc > div, .ph .sw {{ position: absolute; inset: 0; }}
.ph .br {{ transform-origin: 50% 100%; }}
.ph .slc {{ opacity: 0; }}
.ph img, .ph video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ph .in video {{ position: absolute; inset: 0; }}
.ph.card .pu {{ box-shadow: 0 0 0 7px {WHT}, 16px 16px 0 7px {MAG}; }}
.ph.rnd .pu, .ph.rnd .in, .ph.rnd .sw {{ border-radius: 34px; overflow: hidden; }}
.ph .sw {{ overflow: hidden; pointer-events: none; mix-blend-mode: screen; -webkit-mask-size: 100% 100%; mask-size: 100% 100%; }}
.ph .sw i {{ position: absolute; top: -20%; left: 0; width: 34%; height: 140%; transform: translateX(-200%) rotate(16deg); display: block;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0)); }}
.tx {{ position: absolute; white-space: nowrap; line-height: .9; transform-origin: 50% 30%; }}
.tx .c {{ display: inline-block; }}
.tx .cz {{ filter: blur(6px); }}
.flr {{ position: absolute; font-family: "Anton"; color: {WHT}; line-height: .9; white-space: nowrap; transform-origin: 50% 0;
  transform: perspective(700px) rotateX(62deg) scaleY(-1.1); opacity: .55;
  -webkit-mask-image: linear-gradient(0deg, rgba(0,0,0,.9), rgba(0,0,0,0)); mask-image: linear-gradient(0deg, rgba(0,0,0,.9), rgba(0,0,0,0)); }}
.spark {{ position: absolute; width: 30px; height: 30px; margin: -15px 0 0 -15px; border-radius: 50%; background: #fff;
  box-shadow: 0 0 22px 12px rgba(255,255,255,.85), 0 0 60px 26px rgba(255,220,235,.5); display: block; }}
.bu {{ position: absolute; display: flex; align-items: center; justify-content: center; text-align: center; color: {WHT};
  font-family: "Anton"; line-height: .95; }}
.bu b {{ position: absolute; inset: 0; display: block; }}
.bu span {{ position: relative; }}
.sb {{ position: absolute; inset: 0; width: {S}px; height: {S}px; overflow: visible; }}
.sb path {{ fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1000; }}
.pt {{ position: absolute; display: block; }}
.ember {{ border-radius: 50%; background: #ffb347; box-shadow: 0 0 10px 4px #ff5a1a; }}
.star {{ background: #fff; clip-path: polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%);
  filter: drop-shadow(0 0 6px #fff); }}
.dia {{ background: linear-gradient(135deg, #fff 0 30%, #bfc6cc 31% 60%, #fff 61%); clip-path: polygon(50% 0,100% 35%,50% 100%,0 35%);
  filter: drop-shadow(0 0 8px #fff); }}
.petal {{ border-radius: 60% 0 60% 0; background: {MAG}; }}
.call {{ position: absolute; border-radius: 46px; overflow: hidden; border: 9px solid #2b2b2b; box-shadow: 0 0 0 6px {WHT}, 16px 16px 0 6px {MAG}; }}
.call img {{ width: 100%; height: 100%; display: block; }}
.call b {{ position: absolute; left: 0; right: 0; top: 13%; text-align: center; font: 400 64px/1 "Anton"; color: #fff; }}
.call small {{ position: absolute; left: 0; right: 0; top: 23%; text-align: center; font: 400 24px/1 "Anton"; color: #bbb; letter-spacing: .1em; }}
.call .hit {{ position: absolute; width: 22.5%; aspect-ratio: 1; border-radius: 50%; translate: -50% -50%; opacity: 0; }}
#blk {{ position: absolute; inset: 0; z-index: 40; background: {INK}; opacity: 0; }}
#streak {{ position: absolute; inset: 0; z-index: 41; background: rgba(95,27,48,.82); opacity: 0; overflow: hidden; mix-blend-mode: normal; }}
#streak .ln {{ position: absolute; top: -40px; left: 0; width: 18px; height: 1160px; background: {WHT}; transform: rotate(3deg);
  box-shadow: 0 0 30px 12px rgba(255,255,255,.5); display: block; }}
#streak .sp {{ position: absolute; inset: 0; display: block;
  background: repeating-linear-gradient(0deg, rgba(255,255,255,0) 0 60px, rgba(255,255,255,.35) 60px 64px, rgba(255,255,255,0) 64px 150px,
  rgba(220,90,130,.5) 150px 156px); filter: blur(2px); }}
.strip {{ position: absolute; top: -100px; width: 420px; height: 1280px; z-index: 42; opacity: 0; transform: rotate(8deg); display: block; }}
#glitch {{ position: absolute; inset: 0; z-index: 45; opacity: 0;
  background: repeating-linear-gradient(0deg, {INK} 0 22px, {WHT} 22px 40px, {GRY} 40px 52px, {INK} 52px 90px); }}
#flash {{ position: absolute; inset: 0; z-index: 46; background: {WHT}; opacity: 0; }}
#streaks {{ position: absolute; inset: 0; width: {S}px; height: {S}px; z-index: 44; opacity: 0; pointer-events: none; }}
#tunnel {{ position: absolute; inset: -200px; width: 1480px; height: 1480px; z-index: 43; opacity: 0; filter: blur(3px); }}
#bolt {{ position: absolute; inset: 0; width: {S}px; height: {S}px; z-index: 47; opacity: 0; overflow: visible; }}
#bolt g {{ opacity: 0; }}
#bolt path {{ fill: none; stroke-linejoin: miter; }}
#grain {{ position: absolute; inset: -40px; z-index: 35; pointer-events: none; opacity: .09; mix-blend-mode: overlay;
  background: url(assets/img/grain.png); }}
"""


def main():
    build()
    transitions()
    drifts()
    g = random.Random(2)
    for f in range(int(DUR * FPS)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f * STEP:.3f});')
    scenes = ""
    for k, (t0, t1, i, bg, lys, drift, _) in enumerate(SCENES):
        layers = "".join(f'<div class="ly{j}">{"".join(lys[j])}</div>' for j in range(3))
        scenes += f'<div class="sc" id="{i}" style="z-index:{k + 1};background:{bg}">{layers}</div>'
        js(f'tl.set("#{i}", {{display: "block", opacity: 1}}, {t0:.3f});')
        if t1 < DUR:
            js(f'tl.set("#{i}", {{display: "none", opacity: 0}}, {t1 + 6 * STEP:.3f});')     # under the next scene while its cut plays
    strips = "".join(f'<i class="strip" id="st{j}" style="left:{j * 340}px;background:{[INK, MAG, WHT][j]}"></i>' for j in range(3))
    html = f"""<!doctype html>
<html lang="en" data-resolution="square">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={S}, height={S}" />
    <title>Spin Bout U lyric edit 1x1</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><filter id="hblur" x="-20%" y="-5%" width="140%" height="110%">
      <feGaussianBlur stdDeviation="34 0"/></filter><filter id="vblur" x="-5%" y="-20%" width="110%" height="140%">
      <feGaussianBlur stdDeviation="0 34"/></filter><filter id="gslice" x="-10%" y="0" width="120%" height="100%" color-interpolation-filters="sRGB">
      <feImage href="assets/img/glitchmap.png" x="0" y="0" width="1080" height="1080" preserveAspectRatio="none" result="gm"/>
      <feDisplacementMap in="SourceGraphic" in2="gm" scale="260" xChannelSelector="R" yChannelSelector="G"/></filter>{"".join(FILTERS)}</svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{S}" data-height="{S}">
      <div id="stage"><div id="wbg"></div><div id="mbg"></div>
        <div id="scenes">{scenes}</div>
      </div>
      <div id="blk"></div>
      <div id="streak"><i class="sp"></i><i class="ln"></i></div>
      {strips}
      <div id="glitch"></div>
      <img id="streaks" src="assets/img/streaks.png" alt="">
      <img id="tunnel" src="assets/img/tunnel.jpg" alt="">
      <svg id="bolt" viewBox="0 0 1080 1080">{bolt_svg()}</svg>
      <div id="flash"></div>
      <div id="grain"></div>
      <audio id="song" src="assets/audio/section_sfx.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(list(dict.fromkeys(HIDE)))}, {{opacity: 0, display: "none"}});
      gsap.set(".sc", {{display: "none"}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SCENES)} scenes, {len(FILTERS)} living pictures")


if __name__ == "__main__":
    main()
