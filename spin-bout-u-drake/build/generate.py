"""Spin Bout U (Drake & 21 Savage) lyric edit, 1:1, 60 s from the 2:13 bass drop, v3: writes index.html.

python3 build/generate.py      (from the project root; after build/align.py, build/assets.py and build/anime.py)

v3 follows the owner's MJ "Smooth Criminal" reference (sushiismissing), read frame by frame (186 frames, 18 fps):
black / white / red only; hard B&W subjects with a cream outline and a red offset rim; red energy slashes boiling
around the subject; huge condensed red type stacked behind the subject, fat italic type on diagonal red and black
bands, cream brush script written on with a light spark in front of the subject; white brush X marks. Its cuts, each
2-6 frames: sideways smear, zoom-out blur into a red ink burst and an inverted frame, a red paint smear into a white
radial burst, a slice glitch on the subject, red blooms flooding the frame into a white negative and a light flare,
a light burst with a red band sweeping across, a vertical scroll blur, defocus into a white washed-out negative, a
smoke burst, and single inverted or white frames on the beat. No camera shake: each scene only drifts in slowly
(three depth layers at different rates); beats land as punch-ins and flashes instead.

Story: the opening keeps the owner's pictures (two Drake photos, the Vogue cat, En Vogue, the phone, the pearl cat,
the dumb white cat); from "ten toes" on, every line is its own anime illustration of one couple (Canva-generated
art, plan/anime.json, treated by build/anime.py), with motion on top (slashes, sparks, embers, smoke, diamonds,
swirls). Captions are the owner's lyrics on their sung words, every cuss word shown only as a blurred ****.
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
INK, WHT, RED, CRM, DRK = "#0d0d0d", "#f2f0eb", "#d7192a", "#f3e6cf", "#1c1c1c"
F = {k: ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", f), 100) for k, f in
     (("anton", "Anton.ttf"), ("marker", "PermanentMarker.ttf"), ("script", "KaushanScript.ttf"))}
CURSE = {"ass", "hoes", "nigga", "niggas", "shitll", "shit"}
A, HIDE = [], []
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


def fit(t, maxw, size, font="anton", sy=1.0):
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


def tween(sel, frm, to, t, n):
    js(f'tl.fromTo("{sel}", {json.dumps(frm)}, {{...{json.dumps(to)}, duration: {n * STEP:.3f}, ease: "steps({n})", '
       f'immediateRender: false}}, {q(t):.3f});')


def enter(sel, t, how, n=3):
    if how == "pop":
        tween(sel, {"scale": 1.5}, {"scale": 1}, t, n)
    elif how in ("left", "right", "up", "down"):
        dx, dy = {"left": (-460, 0), "right": (460, 0), "up": (0, 460), "down": (0, -460)}[how]
        tween(sel, {"x": dx, "y": dy, "filter": "blur(14px)"}, {"x": 0, "y": 0, "filter": "blur(0px)"}, t, n)
    elif how == "settle":        # out of a soft blur, a little large (the reference's arrivals)
        tween(sel, {"scale": 1.12, "filter": "blur(12px)"}, {"scale": 1, "filter": "blur(0px)"}, t, n)
    elif how == "scroll":        # vertical blur scroll (the reference's stacked type)
        tween(sel, {"y": -520, "filter": "url(#vblur)"}, {"y": 0, "filter": "blur(0px)"}, t, n + 1)
    elif how == "rise":
        tween(sel, {"y": 560}, {"y": 0}, t, n + 2)
    elif how == "tilt":
        tween(sel, {"rotationY": 55, "rotationX": -12, "scale": .75, "transformPerspective": 900},
              {"rotationY": 0, "rotationX": 0, "scale": 1}, t, n + 2)


def photo(src, x, y, w, h=None, rot=0, t0=0, t1=DUR, kind="cut", how="settle", z=3, push=.05, outline=True, rim=True,
          reveal=False, slices=(), punches=(), card=False, pos="", ly=1):
    """kind: cut / print (the owner's photos, build/assets.py), acut / afull (the anime art, build/anime.py).
    outline: a cream outline; rim: a red offset rim; reveal: the subject arrives as a white glowing silhouette
    (reference 4.3-4.6 s); slices: times of a slice glitch; punches: (time, scale) punch-ins on the beat."""
    i = nid("ph")
    path = {"cut": f"assets/img/cut/{src}.png", "print": f"assets/img/print/{src}.jpg", "src": f"assets/img/src/{src}.jpg",
            "acut": f"assets/img/anime/cut/{src}.png", "afull": f"assets/img/anime/full/{src}.jpg"}[kind]
    if h is None:
        iw, ih = Image.open(os.path.join(ROOT, path)).size
        h = w * ih / iw
    filt = []
    if outline and kind in ("cut", "acut"):
        filt += [f"drop-shadow({dx}px {dy}px 0 {CRM})" for dx, dy in ((5, 0), (-5, 0), (0, 5), (0, -5))]
    if rim and kind in ("cut", "acut"):
        filt.append(f"drop-shadow(16px 6px 0 {RED})")
    cls = "ph card" if card else "ph"
    img = f'<img src="{path}" alt="" style="{pos}">'
    sl = ""
    if slices:
        sl = '<div class="slc">' + "".join(f'<div style="clip-path:inset({k * 100 / 7:.1f}% 0 {100 - (k + 1) * 100 / 7:.1f}% 0)">{img}</div>'
                                         for k in range(7)) + "</div>"
    put(f'<div class="{cls}" id="{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;transform:rotate({rot}deg);'
        f'z-index:{z}"><div class="pu" style="{"filter:" + " ".join(filt) if filt else ""}"><div class="in">{img}</div>{sl}</div></div>', ly)
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how)
    if push:
        n = max(1, round((q(t1) - q(t0)) * FPS))
        tween(f"#{i} .in", {"scale": 1}, {"scale": 1 + push}, t0, n)
    if reveal:
        seq = ["brightness(0) invert(1) blur(6px)", "brightness(0) invert(1) drop-shadow(0 0 14px #fff)",
               "grayscale(1) brightness(2.6) contrast(.6) drop-shadow(0 0 10px #fff)", "brightness(1.7) drop-shadow(0 0 8px #fff)",
               "brightness(1.25)", "none"]
        for k, f_ in enumerate(seq):
            js(f'tl.set("#{i} .in img", {{filter: "{f_}"}}, {q(t0) + k * STEP:.3f});')
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


def panel(x, y, w, h, color, t0, t1=DUR, rot=0, how="left", z=1, ly=0, extra=""):
    i = nid("pn")
    put(f'<i class="pn" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};transform:rotate({rot}deg);'
        f'z-index:{z};{extra}"></i>', ly)
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how, 2)
    return i


def bg_spot(t0, t1, cx=50, cy=42, ly=0):
    """Black with a soft white spotlight and a dot screen (the reference's stage frames)."""
    i = nid("sp")
    put(f'<i class="spot" id="{i}" style="background:radial-gradient(ellipse 46% 40% at {cx}% {cy}%, #f4f4f4 0%, #9a9a9a 38%, '
        f'#1a1a1a 72%, {INK} 100%)"></i>', ly)
    show(f"#{i}", t0, t1)


def tone(t0, t1, op=.35, ly=0, z=2):
    i = nid("tn")
    put(f'<i class="tone" id="{i}" style="opacity:{op};z-index:{z}"></i>', ly)
    show(f"#{i}", t0, t1)


FAM = {"anton": "Anton", "marker": "Permanent Marker", "script": "Kaushan Script"}


def cap(t, x, y, size, t0, t1=DUR, font="anton", color=WHT, how="letters", align="left", z=6, rot=0, box=None, sy=1.0,
        skew=0, upper=True, glow=False, ly=2, outline=True):
    """A caption. Light type carries a dark outline and dark type a light one, so it reads on any background."""
    i = nid("tx")
    s = t.upper() if upper else t
    w_ = tw(s, size, font) + (size * .28 if box else 0)
    xl = x - (w_ / 2 if align == "center" else (w_ if align == "right" else 0))
    sty = f"left:{xl:.0f}px;top:{y:.0f}px;font-family:'{FAM[font]}';font-size:{size:.0f}px;color:{color};z-index:{z};"
    tr = f"rotate({rot}deg) skewX({skew}deg) scaleY({sy})"
    sty += f"transform:{tr};"
    if box:
        sty += f"background:{box};padding:.04em .14em 0;"
    elif outline:
        sty += f"-webkit-text-stroke:{max(4, size * .03):.0f}px {WHT if color == INK else INK};paint-order:stroke fill;"
    if glow:
        sty += f"text-shadow:0 0 18px {color}, 0 0 4px #fff;"
    chars = "".join(f'<span class="c{" cz" if c == "*" else ""}">{c if c != " " else "&nbsp;"}</span>' for c in s)
    put(f'<div class="tx" data-layout-allow-overlap id="{i}" style="{sty}">{chars}</div>', ly)
    show(f"#{i}", t0, t1)
    t0 = q(t0)
    n = len(s)
    if how in ("letters", "write"):
        js(f'tl.set("#{i} .c", {{opacity: 0}}, {t0 - .001:.3f});')
        per = 1 if n <= 9 else 2
        for k in range(0, n, per):
            js(f'tl.set("#{i} .c:nth-child(-n+{min(n, k + per)})", {{opacity: 1}}, {t0 + (k // per) * STEP:.3f});')
        if how == "write":     # a light spark rides the pen, the word glows then cools (reference "Struck you")
            sp = nid("spk")
            x0 = xl
            put(f'<i class="spark" id="{sp}" style="left:{x0:.0f}px;top:{y + size * .45:.0f}px;z-index:{z + 1}"></i>', ly)
            steps = max(1, (n + per - 1) // per)
            show(f"#{sp}", t0, t0 + (steps + 1) * STEP)
            for k in range(steps + 1):
                js(f'tl.set("#{sp}", {{x: {w_ * min(1, (k + 1) / steps):.0f}, y: {(-1) ** k * size * .12:.0f}}}, {t0 + k * STEP:.3f});')
            js(f'tl.fromTo("#{i}", {{textShadow: "0 0 26px #fff, 0 0 8px #fff"}}, {{textShadow: "0 0 0px rgba(255,255,255,0)", '
               f'duration: {(steps + 4) * STEP:.3f}, ease: "steps({steps + 4})", immediateRender: false}}, {t0:.3f});')
    elif how == "blocks":
        for k in range(n):
            tween(f"#{i} .c:nth-child({k + 1})", {"rotationX": 90, "opacity": 0, "transformPerspective": 600},
                  {"rotationX": 0, "opacity": 1}, t0 + k * STEP, 2)
    elif how == "drop":
        for k in range(n):
            tween(f"#{i} .c:nth-child({k + 1})", {"y": -640, "filter": "url(#vblur)"}, {"y": 0, "filter": "blur(0px)"}, t0 + k * STEP, 3)
    elif how.startswith("slide"):
        enter(f"#{i}", t0, "left" if how.endswith("l") else "right")
    elif how in ("pop", "settle", "scroll", "rise"):
        enter(f"#{i}", t0, how)
    return i


def slashes(cx, cy, rx, ry, t0, t1, seed, n=7, every=2, z=9, ly=2, color=RED):
    """Red energy slashes boiling round the subject (the reference's signature): a new set every other frame."""
    i = nid("sl")
    g = random.Random(seed)
    K = 4
    groups = []
    for v in range(K):
        polys = []
        for _ in range(n):
            a = g.uniform(0, math.tau)
            px, py = cx + rx * math.cos(a) * g.uniform(.75, 1.1), cy + ry * math.sin(a) * g.uniform(.75, 1.1)
            d = a + g.choice([1, -1]) * g.uniform(.6, 1.4) + math.pi * g.choice([0, 1])
            ln, wd = g.uniform(70, 210), g.uniform(5, 13)
            ux, uy = math.cos(d), math.sin(d)
            nx, ny = -uy, ux
            k1 = g.uniform(.35, .6)
            pts = [(px + nx * wd, py + ny * wd), (px + ux * ln * k1 + nx * wd * 2.2, py + uy * ln * k1 + ny * wd * 2.2),
                   (px + ux * ln * (k1 - .08), py + uy * ln * (k1 - .08)), (px + ux * ln, py + uy * ln),
                   (px - nx * wd, py - ny * wd)]
            polys.append('<polygon points="' + " ".join(f"{a_:.0f},{b_:.0f}" for a_, b_ in pts) + '"/>')
        groups.append(f'<g style="opacity:0">{"".join(polys)}</g>')
    put(f'<svg class="sls" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z};fill:{color}">{"".join(groups)}</svg>', ly)
    show(f"#{i}", t0, t1)
    for k, t in enumerate(frames(t0, t1, every)):
        v = k % K
        js(f'tl.set("#{i} g", {{opacity: 0}}, {t:.3f});')
        if g.random() < .85:
            js(f'tl.set("#{i} g:nth-child({v + 1})", {{opacity: 1}}, {t:.3f});')


def xmarks(pts, t0, t1, size=70, color=WHT, ly=2, z=8):
    for k, (x, y) in enumerate(pts):
        i = nid("xm")
        put(f'<div class="xm" id="{i}" style="left:{x}px;top:{y}px;font-size:{size}px;color:{color};z-index:{z}">x</div>', ly)
        show(f"#{i}", t0 + k * STEP * 2, t1)
        enter(f"#{i}", t0 + k * STEP * 2, "pop", 2)
        for j, t in enumerate(frames(t0 + k * STEP * 2 + 3 * STEP, t1, 4)):
            js(f'tl.set("#{i}", {{rotation: {(-1) ** (j + k) * 8}}}, {t:.3f});')


def scribble(pts, t0, t1=DUR, color=CRM, width=8, dur=.3, z=8, ly=2):
    i = nid("sb")
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    put(f'<svg class="sb" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}"><path d="{d}" pathLength="1000" '
        f'style="stroke:{color};stroke-width:{width}"/></svg>', ly)
    show(f"#{i}", t0, t1)
    n = max(2, round(dur * FPS))
    tween(f"#{i} path", {"strokeDashoffset": 1000}, {"strokeDashoffset": 0}, t0, n)


def swoosh(x, y, w, t0, t1, color=CRM, z=8, ly=2):
    """The scribbled underline under a script word (reference "Us")."""
    pts, g = [], random.Random(int(x + y))
    for k in range(9):
        pts.append((x + w * k / 8, y + (14 if k % 2 else -14) * (1 - k / 10) + g.uniform(-4, 4)))
    scribble(pts, t0, t1, color=color, width=6, dur=.25, z=z, ly=ly)


def particles(kind, t0, t1, n, seed, z=7, ly=2, box=(0, 0, S, S)):
    """Motion on the art: embers rise, sparkles blink, diamonds fall, smoke drifts, petals float."""
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
                nn = max(2, round(per * FPS))
                tween(f"#{i}", {"y": 0, "x": 0}, {"y": -(y1 - y0) * g.uniform(.6, 1), "x": g.uniform(-90, 90)}, max(t0, st), nn)
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
                nn = max(2, round(per * FPS))
                tween(f"#{i}", {"y": 0, "rotation": 0}, {"y": S + 160, "rotation": g.uniform(-200, 200)}, max(t0, st), nn)
                st += per
        elif kind == "smoke":
            sz = g.uniform(260, 520)
            put(f'<i class="pt smk" id="{i}" style="left:{x - sz / 2:.0f}px;top:{y - sz / 2:.0f}px;width:{sz:.0f}px;height:{sz:.0f}px;'
                f'z-index:{z};opacity:{g.uniform(.08, .16):.2f}"></i>', ly)
            show(f"#{i}", t0, t1)
            nn = max(2, round((t1 - t0) * FPS))
            tween(f"#{i}", {"x": 0, "y": 0, "scale": .8}, {"x": g.uniform(-160, 160), "y": g.uniform(-260, -90), "scale": 1.35}, t0, nn)
        elif kind == "petal":
            sz = g.uniform(18, 34)
            put(f'<i class="pt petal" id="{i}" style="left:{x:.0f}px;top:-60px;width:{sz:.0f}px;height:{sz * .6:.0f}px;z-index:{z}"></i>', ly)
            show(f"#{i}", t0, t1)
            per = g.uniform(2.2, 3.4)
            st = t0 - g.uniform(0, per)
            while st < t1:
                nn = max(2, round(per * FPS))
                tween(f"#{i}", {"y": 0, "x": 0, "rotation": 0}, {"y": S + 120, "x": g.uniform(-260, 260), "rotation": g.uniform(-360, 360)},
                      max(t0, st), nn)
                st += per


def swirl(cx, cy, t0, t1, z=1, ly=0, color=INK):
    """Rings that turn behind the spinning couple."""
    i = nid("sw")
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke-dasharray="{r * .9:.0f} {r * .35:.0f}" stroke-width="{w}"/>'
                    for r, w in ((180, 14), (290, 10), (400, 18), (520, 8), (640, 22)))
    put(f'<svg class="swl" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z};stroke:{color}">{rings}</svg>', ly)
    show(f"#{i}", t0, t1)
    for k, r in enumerate((180, 290, 400, 520, 640)):
        nn = max(2, round((t1 - t0) * FPS))
        tween(f"#{i} circle:nth-child({k + 1})", {"rotation": 0, "svgOrigin": f"{cx} {cy}"},
              {"rotation": (1 if k % 2 else -1) * 260 * (t1 - t0) / 5}, t0, nn)


def phone_card(x, y, w, caller, t0, t1, press, button="accept", z=4, ly=1):
    i = nid("call")
    h = w * 1792 / 828
    bx, col = ("79%", "#3fd25c") if button == "accept" else ("21%", "#ff3b30")
    put(f'<div class="call" id="{i}" style="left:{x}px;top:{y}px;width:{w:.0f}px;height:{h:.0f}px;z-index:{z}">'
        f'<img src="assets/img/src/incoming_call.jpg" alt=""><b>{caller}</b><small>mobile</small>'
        f'<i class="hit" style="left:{bx};top:77%;background:{col}"></i></div>', ly)
    show(f"#{i}", t0, t1)
    enter(f"#{i}", t0, "tilt")
    tt, k = q(t0) + .3, 0
    while tt < press - .1:
        js(f'tl.set("#{i} .hit", {{opacity: {.5 if k % 2 == 0 else 0}, scale: {1.6 if k % 2 == 0 else 1}}}, {tt:.3f});')
        tt, k = tt + .2, k + 1
    js(f'tl.set("#{i} .hit", {{opacity: .95, scale: 1}}, {q(press):.3f});')
    js(f'tl.to("#{i} .hit", {{scale: 30, opacity: 1, duration: {4 * STEP:.3f}, ease: "steps(4)"}}, {q(press) + STEP:.3f});')
    return i


# ------------------------------------------------------------------------------------------------ in-scene beat hits
def invert(t, n=1):
    js(f'tl.set("#stage", {{filter: "invert(1) grayscale(1)"}}, {q(t):.3f});')
    js(f'tl.set("#stage", {{filter: "none"}}, {q(t) + n * STEP:.3f});')


def white(t, n=1):
    js(f'tl.set("#flash", {{opacity: 1}}, {q(t):.3f});')
    js(f'tl.set("#flash", {{opacity: 0}}, {q(t) + n * STEP:.3f});')


def beats_in(t0, t1, every=4, off=0):
    return [q(b) for b in BEATS[off::every] if t0 + .2 < b < t1 - .25]


# ------------------------------------------------------------------------------------------------ scenes
SCENES = []        # [t0, t1, id, bg, layers, drift, transition-in]


def scene(t0, t1, bg=INK, drift=(0, 0), trans="smear"):
    i = f"sc{len(SCENES)}"
    CUR["ly"] = [[], [], []]
    SCENES.append([q(t0), q(t1), i, bg, CUR["ly"], drift, trans])


def build():
    E = [lt(k) for k in range(len(L))] + [DUR]

    # S0 the drop: Drake from behind under a spotlight, slashes boiling; red ink burst into the title (reference 0-1.6 s).
    scene(0, E[0])
    bg_spot(0, E[0], cy=36)
    tone(0, E[0])
    photo("drake_back_jacket", 250, 170, 580, None, 0, 0, E[0], how="settle", push=.08)
    slashes(540, 560, 300, 380, 0, E[0], 1)
    js(f'tl.set("#ink", {{opacity: 1, scale: .35}}, {q(.9):.3f});')
    tween("#ink", {"scale": .35}, {"scale": 1.9}, .9, 2)
    js(f'tl.set("#ink path", {{fill: "#bdbdbd"}}, {q(1.0):.3f});')
    js(f'tl.set("#ink", {{opacity: 0}}, {q(1.05):.3f});')
    js(f'tl.set("#ink path", {{fill: "{RED}"}}, {q(1.1):.3f});')
    invert(1.05)
    cap("Spin", 520, 250, 300, 1.1, E[0], font="script", color=RED, align="center", rot=-7, upper=False, how="settle", glow=True)
    cap("Bout U", 560, 540, 250, 1.25, E[0], font="script", color=RED, align="center", rot=-7, upper=False, how="settle", glow=True)
    xmarks([(150, 820), (880, 200), (900, 860)], 1.4, E[0])

    # S1 Jealous-**** ****, yeah: the whispering girls on a red field and a black band, JEALOUS fat italic behind them.
    li = 0
    scene(E[0], E[1], bg=RED, drift=(-14, 0), trans="inkburst")
    photo("jealous", -40, -40, 1160, 1160, 0, E[0], E[1], kind="afull", how="settle", push=.06, z=1, ly=0, slices=(at(li, 3),),
          punches=((at(li, 2), 1.12),))
    panel(-200, -120, 1500, 380, INK, E[0], E[1], rot=-6, how="left", z=2, ly=1)
    cap("JEALOUS", 540, 20, fit("JEALOUS", 940, 260), at(li, 0), E[1], color=RED, skew=-10, align="center", how="blocks", ly=1, z=3)
    panel(-200, 860, 1500, 300, RED, at(li, 1), E[1], rot=-6, how="right", z=2, ly=1)
    cap(text(li, 1, 2) + ",", 60, 890, 130, at(li, 1), E[1], color=WHT, skew=-10, how="pop")
    cap("yeah", 830, 760, 180, at(li, 3), E[1], font="marker", color=CRM, upper=False, rot=-8, how="write", align="center")
    xmarks([(90, 300), (930, 420), (520, 990)], at(li, 2), E[1])
    slashes(540, 560, 380, 360, E[0], E[1], 2)

    # S2 ...'bout bein' in Vogue: the cat Vogue cover as a tilted card on black, the words stacked in red.
    li = 1
    scene(E[1], E[2], drift=(10, 0), trans="smear")
    tone(E[1], E[2], .25)
    photo("vogue_cat_cover", 590, 130, 440, 620, 5, lt(li), E[2], kind="print", how="tilt", z=2, card=True)
    for k, (a_, b_, c_) in enumerate(((0, 2, RED), (3, 5, RED), (6, 8, WHT))):
        t_ = text(li, a_, b_)
        cap(t_, 50, 110 + k * 165, fit(t_.upper(), 500, 130), at(li, a_), E[2], color=c_, sy=1.2, how="slide-l")
    cap("Vogue", 300, 720, 260, at(li, 9), E[2], font="marker", color=CRM, upper=False, rot=-9, how="write", z=9)
    swoosh(260, 980, 520, at(li, 9) + .2, E[2])

    # S3 that R&B group from the '90s: En Vogue as a card on a red field, R&B GROUP on a black band, '90s.
    li = 2
    scene(E[2], E[3], bg=RED, drift=(0, 10), trans="redsmear")
    panel(-200, 700, 1500, 300, INK, E[2], E[3], rot=-7, how="right", z=3, ly=1)
    cap(text(li, 0, 3), 540, 70, 110, at(li, 0), E[3], color=INK, sy=1.2, align="center", how="settle", outline=False)
    photo("envogue_funky_divas", 230, 220, 620, 560, -3, lt(li), E[3], kind="print", how="settle", z=2, card=True)
    cap("R&B GROUP", 540, 735, fit("R&B GROUP", 980, 230), at(li, 4), E[3], color=WHT, skew=-10, align="center", how="blocks", ly=1, z=4)
    cap(text(li, 6, 7), 60, 980, 70, at(li, 6), E[3], color=CRM)
    cap("'90s", 1010, 180, 220, at(li, 8), E[3], font="marker", color=CRM, align="right", upper=False, rot=-10, how="write")

    # S4 Girl, one call, I'll get you in Vogue: the hand and the phone under a spotlight, the call answered on "Vogue".
    li = 3
    scene(E[3], E[4], drift=(-12, 0), trans="slice")
    bg_spot(E[3], E[4], cx=62, cy=40)
    tone(E[3], E[4])
    cap("ONE", 40, 160, 300, at(li, 1), E[4], color=RED, sy=1.25, how="blocks", ly=0, z=3, outline=False)
    cap("CALL", 40, 520, 300, at(li, 2), E[4], color=RED, sy=1.25, how="blocks", ly=0, z=3, outline=False)
    phone_card(640, 110, 360, "Vogue", lt(li), E[4], press=at(li, 7))
    photo("hand_phone_sticker", 60, 520, 500, None, -8, at(li, 1), E[4], how="rise", push=0, z=5, slices=(lt(li),))
    cap("Girl,", 60, 60, 160, at(li, 0), E[4], font="marker", color=CRM, upper=False, rot=-8, how="write")
    cap(text(li, 3, 6), 820, 900, 90, at(li, 3), E[4], align="center", color=WHT)
    slashes(760, 480, 260, 380, at(li, 7), E[4], 4)

    # S5 One call, you in runway shows: the pearl cat page full height, RUNWAY in red on a black band, shows in script.
    li = 4
    scene(E[4], E[5], drift=(0, -12), trans="lightband")
    photo("rolex_cat_ad", 240, 0, 600, S, 0, lt(li), E[5], kind="print", how="settle", z=2, push=.07)
    panel(-200, 640, 1500, 260, INK, E[4], E[5], rot=-8, how="left", z=3, ly=1)
    cap(text(li, 0, 3), 540, 40, 100, at(li, 0), E[5], color=WHT, align="center", how="settle")
    cap("RUNWAY", 540, 640, fit("RUNWAY", 980, 260), at(li, 4), E[5], color=RED, skew=-10, align="center", how="blocks", ly=1, z=4)
    cap("shows", 760, 860, 190, at(li, 5), E[5], font="marker", color=CRM, upper=False, rot=-8, how="write", align="center")

    # S6 One call, I'm sittin' front row: Drake in Chanel, FRONT ROW huge in red behind him, sittin' in script.
    li = 5
    scene(E[5], E[6], drift=(-14, 0), trans="defocus")
    bg_spot(E[5], E[6], cy=38)
    tone(E[5], E[6])
    cap("FRONT", 540, 90, fit("FRONT", 1020, 420), at(li, 4), E[6], color=RED, sy=1.1, align="center", how="blocks", ly=1, z=2, outline=False)
    cap("ROW", 540, 520, fit("ROW", 1020, 460), at(li, 5), E[6], color=RED, sy=1.1, align="center", how="blocks", ly=1, z=2, outline=False)
    photo("drake_chanel_night", 300, 170, 560, None, 0, lt(li), E[6], how="settle", push=.06, z=3)
    cap(text(li, 0, 1), 50, 60, 100, at(li, 0), E[6], color=WHT, box=RED)
    cap("sittin'", 640, 840, 180, at(li, 2), E[6], font="marker", color=CRM, upper=False, rot=-8, how="write", align="center", z=9)
    slashes(580, 600, 320, 380, at(li, 4), E[6], 6)

    # S7 One wrong call from your ex ****...: the same phone, the ex declined; then the dumb cat, SENT HOME.
    li = 6
    mid = at(li, 8)
    scene(E[6], E[7], drift=(0, 0), trans="redflood")
    bg_spot(E[6], mid, cx=50, cy=45)
    tone(E[6], mid)
    cap("WRONG", 40, 70, fit("WRONG", 600, 260), at(li, 1), mid, color=RED, sy=1.2, how="blocks", ly=0, z=3, outline=False)
    cap("CALL", 40, 380, fit("CALL", 600, 260), at(li, 2), mid, color=RED, sy=1.2, how="blocks", ly=0, z=3, outline=False)
    phone_card(620, 120, 380, "Ex", lt(li), mid, press=at(li, 5), button="decline")
    cap(text(li, 3, 6), 40, 900, 110, at(li, 3), mid, color=WHT, skew=-10)
    scribble([(660, 180), (980, 880)], at(li, 5) + .1, mid, color=RED, width=22, dur=.15, z=9)
    scribble([(980, 180), (660, 880)], at(li, 5) + .2, mid, color=RED, width=22, dur=.15, z=9)
    panel(0, 0, S, S, RED, mid, E[7], how="", z=0)
    panel(-200, 700, 1500, 280, INK, mid, E[7], rot=-7, how="left", z=3, ly=1)
    photo("cat_white_dumb", 250, 170, 580, 540, 3, mid, E[7], kind="print", how="settle", push=.08, z=2, card=True, slices=(mid,))
    cap(text(li, 7, 7), 60, 60, 120, at(li, 7), E[7], color=INK, sy=1.2, outline=False)
    cap(text(li, 9, 11), 1020, 60, 100, at(li, 9), E[7], color=WHT, align="right", how="pop")
    cap("SENT HOME", 540, 740, fit("SENT HOME", 980, 230), at(li, 12), E[7], color=WHT, skew=-10, align="center", how="blocks", ly=1, z=4)
    cap("dumb", 790, 560, 170, at(li, 8), E[7], font="marker", color=CRM, upper=False, rot=-12, how="write", align="center", z=9)

    # S8 One call and my **** ten toes: the crew, TEN TOES in black behind them on red, the band under their feet.
    li = 7
    scene(E[7], E[8], bg=RED, drift=(0, -10), trans="inkburst")
    panel(-200, 820, 1500, 400, INK, E[7], E[8], rot=-5, how="up")
    cap("TEN TOES", 540, 20, fit("TEN TOES", 1020, 330), at(li, 5), E[8], color=INK, sy=1.15, align="center", how="blocks", ly=1, z=2, outline=False)
    photo("crew", 220, 400, 640, None, 0, E[7], E[8], kind="acut", how="", reveal=True, push=.05)
    cap(text(li, 0, 4), 540, 985, 70, at(li, 0), E[8], color=WHT, align="center", how="settle")
    slashes(540, 560, 430, 380, at(li, 5), E[8], 8)

    # S9 Down to go wherever I say go: he points straight down the lens, she looks; WHEREVER sweeps on a red band, GO.
    li = 8
    scene(E[8], E[9], drift=(0, 0), trans="smear")
    photo("point", -40, -40, 1160, 1160, 0, E[8], E[9], kind="afull", how="settle", push=.04, z=1, ly=0,
          punches=((at(li, 3), 1.12), (at(li, 6), 1.24)))
    cap(text(li, 0, 2), 50, 50, 110, at(li, 0), E[9], color=WHT, box=RED)
    panel(-200, 760, 1500, 220, RED, at(li, 3), E[9], rot=-6, how="left", z=3, ly=1)
    cap("WHEREVER", 540, 760, fit("WHEREVER", 980, 210), at(li, 3), E[9], color=WHT, skew=-10, align="center", how="slide-r", ly=1, z=4)
    cap("I say go", 790, 150, 120, at(li, 4), E[9], font="marker", color=CRM, upper=False, rot=-10, how="write", align="center", z=9)
    white(at(li, 6))

    # S10 Even if we gotta travel 'cross the globe: the two of them at the jet window; travel in script.
    li = 9
    scene(E[9], E[10], drift=(0, 12), trans="vscroll")
    photo("jet", -40, -40, 1160, 1160, 0, E[9], E[10], kind="afull", how="", push=.07, z=1, ly=0)
    cap(text(li, 0, 3), 540, 50, 96, at(li, 0), E[10], color=WHT, align="center", how="settle")
    cap("'CROSS THE GLOBE", 540, 860, fit("'CROSS THE GLOBE", 1000, 170), at(li, 5), E[10], color=RED, sy=1.2, align="center", how="blocks")
    cap("travel", 300, 640, 190, at(li, 4), E[10], font="marker", color=CRM, upper=False, rot=-10, how="write", align="center", z=9)
    particles("sparkle", E[9], E[10], 8, 10)

    # S11 Down to take you to the end of the road, for real: the red stack with the road picture set in it, then the
    # picture full frame on "for real".
    li = 10
    fr = at(li, 9)
    scene(E[10], E[11], drift=(0, -8), trans="defocus")
    cap("TO THE", 540, 40, fit("TO THE", 640, 250), at(li, 4), fr, color=RED, sy=1.2, align="center", how="scroll", ly=1, outline=False)
    cap("END", 230, 330, 250, at(li, 6), fr, color=RED, sy=1.2, align="center", how="scroll", ly=1, outline=False)
    photo("road", 400, 340, 300, 270, 0, at(li, 6), fr, kind="afull", how="settle", push=.1, z=3)
    cap("OF", 850, 330, 250, at(li, 7), fr, color=RED, sy=1.2, align="center", how="scroll", ly=1, outline=False)
    cap("THE ROAD", 540, 640, fit("THE ROAD", 980, 260), at(li, 8), fr, color=RED, sy=1.2, align="center", how="scroll", ly=1, outline=False)
    cap(text(li, 0, 3), 540, 960, 70, at(li, 0), fr, color=WHT, align="center")
    photo("road", -40, -40, 1160, 1160, 0, fr, E[11], kind="afull", how="settle", push=.06, z=5, ly=1)
    cap("for real", 540, 820, 220, at(li, 10), E[11], font="marker", color=CRM, upper=False, rot=-8, how="write", align="center")
    white(fr)

    # S12 hook 1: her, blushing, on red and black (THE WAY / YOU / MAKE ME); him, smitten, under the spotlight on "feel"
    # (FEEL huge behind him, these days in script). Inverted frames on every bar.
    li = 11
    fe = at(li, 5)
    scene(E[11], E[12], bg=RED, drift=(0, -10), trans="redflood")
    panel(-200, 600, 1500, 700, INK, E[11], fe, rot=-10, how="left")
    cap("THE WAY", 40, 40, fit("THE WAY", 1000, 300), at(li, 0), fe, color=INK, sy=1.15, how="blocks", ly=1, z=2, outline=False)
    photo("her_blush", 250, 210, 640, 640, 4, E[11], fe, kind="afull", how="", reveal=True, push=.08, card=True, z=3,
          punches=((at(li, 2), 1.1), (at(li, 3), 1.0)))
    cap("YOU", 60, 560, 220, at(li, 2), fe, color=WHT, skew=-10, how="pop")
    cap("MAKE ME", 980, 880, 140, at(li, 3), fe, color=WHT, skew=-10, align="right", how="slide-r")
    particles("sparkle", E[11], fe, 7, 12, box=(150, 150, 950, 800))
    particles("petal", E[11], fe, 10, 13)
    slashes(600, 560, 380, 380, at(li, 2), fe, 12)
    bg_spot(fe, E[12], cy=40, ly=0)
    tone(fe, E[12])
    cap("FEEL", 540, 120, fit("FEEL", 1020, 560), fe, E[12], color=RED, sy=1.15, align="center", how="blocks", ly=1, z=2, outline=False)
    photo("him_smitten", 230, 250, 620, 620, -4, fe, E[12], kind="afull", how="", reveal=True, push=.08, card=True, z=3, slices=(at(li, 6),))
    cap("these days", 540, 820, 190, at(li, 6), E[12], font="marker", color=CRM, upper=False, rot=-7, how="write", align="center", z=9)
    swoosh(300, 1010, 480, at(li, 7) + .1, E[12])
    particles("sparkle", fe, E[12], 6, 14, box=(150, 150, 950, 800))
    for b in beats_in(E[11], E[12], 4, 0):
        if abs(b - fe) > .15:
            invert(b)

    # S13 Somethin' gettin' dropped for you, baby girl: diamonds pour into her hands; DROPPED falls in; diamonds rain.
    li = 12
    scene(E[12], E[13], drift=(0, 12), trans="lightband")
    bg_spot(E[12], E[13], cy=34)
    tone(E[12], E[13])
    cap("DROPPED", 540, 60, fit("DROPPED", 1020, 360), at(li, 2), E[13], color=RED, sy=1.2, align="center", how="drop", ly=1, z=2, outline=False)
    photo("diamonds", 230, 260, 620, 620, 3, lt(li), E[13], kind="afull", how="", reveal=True, push=.08, card=True, z=3)
    cap(text(li, 0, 1), 50, 960, 80, at(li, 0), E[13], color=WHT)
    cap(text(li, 3, 4), 1030, 520, 130, at(li, 3), E[13], color=WHT, skew=-10, align="right", how="slide-r")
    cap("baby girl", 540, 760, 170, at(li, 5), E[13], font="marker", color=CRM, upper=False, rot=-7, how="write", align="center", z=9)
    particles("diamond", at(li, 2), E[13], 16, 15)
    particles("sparkle", E[12], E[13], 6, 16)

    # S14 Smoke a **** top for you, baby girl: his face in the smoke, red eyes; smoke drifting across; SMOKE in red.
    li = 13
    scene(E[13], E[14], drift=(10, -8), trans="smoke")
    photo("smoke", -40, -40, 1160, 1160, 0, E[13], E[14], kind="afull", how="settle", push=.08, z=1, ly=0,
          punches=((at(li, 3), 1.15), (at(li, 6), 1.0)))
    cap("SMOKE", 40, 40, fit("SMOKE", 700, 300), at(li, 0), E[14], color=RED, sy=1.2, how="blocks")
    cap(text(li, 1, 3), 40, 390, 120, at(li, 1), E[14], color=WHT, skew=-10, how="slide-l")
    cap(text(li, 4, 5), 1030, 760, 110, at(li, 4), E[14], color=WHT, box=RED, align="right", how="pop")
    cap("baby girl", 540, 880, 170, at(li, 6), E[14], font="marker", color=CRM, upper=False, rot=-7, how="write", align="center")
    white(at(li, 3))

    # S15 Burn somebody block for you: he walks out of the burning block, embers rising, BURN flickering.
    li = 14
    scene(E[14], E[15], drift=(0, -10), trans="redsmear")
    photo("fire", -40, -40, 1160, 1160, 0, E[14], E[15], kind="afull", how="settle", push=.1, z=1, ly=0)
    particles("ember", E[14], E[15], 22, 18, z=3, ly=1)
    b = cap("BURN", 540, 30, fit("BURN", 1000, 380), at(li, 0), E[15], color=RED, sy=1.15, align="center", how="blocks")
    for k, t in enumerate(frames(at(li, 0), E[15], 2)):
        js(f'tl.set("#{b}", {{color: "{[RED, WHT][k % 2]}"}}, {t:.3f});')
    panel(-200, 780, 1500, 210, INK, at(li, 1), E[15], rot=-6, how="left", z=3, ly=1)
    cap("SOMEBODY BLOCK", 540, 790, fit("SOMEBODY BLOCK", 980, 180), at(li, 1), E[15], color=WHT, skew=-10, align="center",
        how="slide-r", ly=1, z=4)
    cap(text(li, 3, 4), 60, 980, 70, at(li, 3), E[15], color=CRM)
    invert(at(li, 2))

    # S16 hook 2: he spins her, the rings turning behind them, the words stacked; punch-ins and inverted frames on the bars.
    li = 15
    scene(E[15], E[16], bg=RED, drift=(0, 0), trans="zoomwhite")
    swirl(540, 560, E[15], E[16])
    cap("THE WAY", 40, 40, fit("THE WAY", 600, 200), at(li, 0), E[16], color=INK, sy=1.15, how="blocks", ly=1, z=2, outline=False)
    cap("YOU", 1030, 60, 200, at(li, 2), E[16], color=WHT, skew=-10, align="right", how="pop")
    pb = beats_in(E[15], E[16], 4, 2)
    photo("spin", 150, 170, 780, None, 0, E[15], E[16], kind="acut", how="", reveal=True, push=.05,
          punches=[(t, [1.12, 1.0][k % 2]) for k, t in enumerate(pb)])
    cap("MAKE ME FEEL", 540, 840, fit("MAKE ME FEEL", 1000, 200), at(li, 3), E[16], color=WHT, skew=-10, align="center", how="slide-l")
    cap("these days", 540, 640, 170, at(li, 6), E[16], font="marker", color=CRM, upper=False, rot=-7, how="write", align="center", z=9)
    particles("sparkle", E[15], E[16], 8, 19)
    slashes(540, 560, 420, 400, at(li, 5), E[16], 16)
    for b in beats_in(E[15], E[16], 4, 0):
        invert(b)

    # S17 Comin' out my body for you, baby girl: his spirit rising out of him, glowing; BODY in red.
    li = 16
    scene(E[16], E[17], drift=(0, -14), trans="defocus")
    bg_spot(E[16], E[17], cy=40)
    tone(E[16], E[17])
    cap("COMIN' OUT", 540, 40, fit("COMIN' OUT", 1000, 200), at(li, 0), E[17], color=WHT, skew=-10, align="center", how="slide-l")
    cap("MY BODY", 540, 300, fit("MY BODY", 1020, 380), at(li, 2), E[17], color=RED, sy=1.2, align="center", how="blocks", ly=1, z=2, outline=False)
    sp = photo("spirit", 170, 200, 740, None, 0, lt(li), E[17], kind="acut", how="", reveal=True, push=.06)
    js(f'tl.fromTo("#{sp}", {{filter: "drop-shadow(0 0 0px #fff)"}}, {{filter: "drop-shadow(0 0 30px #fff)", duration: {6 * STEP:.3f}, '
       f'ease: "steps(6)", yoyo: true, repeat: 1, immediateRender: false}}, {at(li, 1):.3f});')
    cap(text(li, 4, 5), 60, 960, 80, at(li, 4), E[17], color=WHT)
    cap("baby girl", 760, 860, 170, at(li, 6), E[17], font="marker", color=CRM, upper=False, rot=-7, how="write", align="center", z=9)
    slashes(540, 520, 360, 420, at(li, 1), E[17], 17)

    # S18 Wipe him like he snotty for you, baby girl: the crying rival wiped down; a red wipe on "Wipe"; snotty in script.
    li = 17
    scene(E[17], E[18], bg=WHT, drift=(0, 8), trans="slice")
    panel(0, 0, S, S, RED, E[17], E[18], how="", z=0, extra="clip-path:polygon(0 70%,100% 52%,100% 100%,0 100%)")
    cap("WIPE HIM", 540, 40, fit("WIPE HIM", 1000, 300), at(li, 0), E[18], color=INK, sy=1.15, align="center", how="blocks", ly=1, z=2, outline=False)
    photo("snotty", 380, 260, 580, None, 0, lt(li), E[18], kind="acut", how="settle", push=.06, outline=False, rim=False)
    w_ = panel(-60, 0, 1200, S, RED, at(li, 0), at(li, 0) + .4, how="", z=9, ly=2)
    tween(f"#{w_}", {"x": -1300}, {"x": 1300}, at(li, 0), 6)
    cap(text(li, 2, 3), 60, 380, 110, at(li, 2), E[18], color=INK, skew=-10, how="slide-l")
    cap("snotty", 540, 760, 200, at(li, 4), E[18], font="marker", color=RED, upper=False, rot=-7, how="write", align="center", z=9)
    cap(text(li, 5, 6), 60, 520, 90, at(li, 5), E[18], color=WHT, box=INK, how="pop")
    cap("baby girl", 540, 985, 80, at(li, 7), E[18], font="marker", color=WHT, upper=False, rot=-3, how="write", align="center", z=9)

    # S19 Comin' out my body for you: the two of them back to back in the red aura; the end zooms out to white.
    li = 18
    scene(E[18], DUR, bg=RED, drift=(0, -10), trans="inkburst")
    panel(-200, 720, 1500, 600, INK, E[18], DUR, rot=-8, how="left")
    cap("MY BODY", 540, 40, fit("MY BODY", 1000, 330), at(li, 2), DUR, color=INK, sy=1.15, align="center", how="blocks", ly=1, z=2, outline=False)
    photo("finale", 170, 190, 740, None, 0, E[18], DUR, kind="acut", how="", reveal=True, push=.06)
    cap(text(li, 0, 1), 50, 880, 110, at(li, 0), DUR, color=WHT, skew=-10, how="slide-l")
    cap("for you", 830, 930, 150, at(li, 4), DUR, font="marker", color=CRM, upper=False, rot=-8, how="write", align="center", z=9)
    slashes(540, 560, 400, 400, E[18], DUR, 19)
    particles("ember", E[18], DUR, 14, 20)


def transitions():
    """The reference's cuts. t = the cut; the outgoing scene gets the frames before it, the incoming the frames after."""
    for k in range(1, len(SCENES)):
        t, _, cur, _, _, _, kind = SCENES[k]
        prev = SCENES[k - 1][2]
        p1, p2, p3 = t - STEP, t - 2 * STEP, t - 3 * STEP
        if kind == "smear":         # sideways smear out and in (reference 0.28-0.39 s)
            tween(f"#{prev}", {"x": 0, "filter": "blur(0px)"}, {"x": -520, "filter": "url(#hblur)"}, p2, 2)
            tween(f"#{cur}", {"x": 440, "filter": "url(#hblur)"}, {"x": 0, "filter": "blur(0px)"}, t, 3)
        elif kind == "inkburst":    # zoom-out blur, a red ink burst on black, a grey burst, an inverted frame, settle (0.67-1.06 s)
            tween(f"#{prev}", {"scale": 1, "filter": "blur(0px)"}, {"scale": .8, "filter": "blur(18px)"}, p2, 2)
            js(f'tl.set("#blk", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#ink", {{opacity: 1}}, {t:.3f});')
            tween("#ink", {"scale": .3}, {"scale": 1.0}, t, 2)
            js(f'tl.set("#ink path", {{fill: "#bdbdbd"}}, {t + 2 * STEP:.3f});')
            js(f'tl.set("#ink", {{scale: 1.9}}, {t + 2 * STEP:.3f});')
            js(f'tl.set("#ink", {{opacity: 0}}, {t + 3 * STEP:.3f});')
            js(f'tl.set("#ink path", {{fill: "{RED}"}}, {t + 3 * STEP:.3f});')
            js(f'tl.set("#blk", {{opacity: 0}}, {t + 3 * STEP:.3f});')
            invert(t + 3 * STEP)
            tween(f"#{cur}", {"scale": 1.12, "filter": "blur(14px)"}, {"scale": 1, "filter": "blur(0px)"}, t + 3 * STEP, 3)
        elif kind == "redsmear":    # red paint smears across, a full red streaked frame, a white radial burst, settle (1.61-1.78 s)
            js(f'tl.set("#redf", {{opacity: 1}}, {p2:.3f});')
            tween("#redf", {"x": -1100, "filter": "url(#hblur)"}, {"x": 0, "filter": "url(#hblur)"}, p2, 2)
            js(f'tl.set("#redf", {{opacity: 0}}, {t + STEP:.3f});')
            js(f'tl.set("#burst", {{opacity: 1, scale: 1.3}}, {t + STEP:.3f});')
            js(f'tl.set("#burst", {{opacity: .6, scale: 1.1}}, {t + 2 * STEP:.3f});')
            js(f'tl.set("#burst", {{opacity: 0, scale: 1}}, {t + 3 * STEP:.3f});')
            tween(f"#{cur}", {"scale": 1.45, "filter": "blur(16px) brightness(1.8)"}, {"scale": 1, "filter": "blur(0px) brightness(1)"}, t + STEP, 3)
        elif kind == "slice":       # a quick smear out; the incoming subject arrives sliced (2.33 s); a white frame
            tween(f"#{prev}", {"x": 0, "filter": "blur(0px)"}, {"x": -300, "filter": "url(#hblur)"}, p1, 1)
            white(t)
            tween(f"#{cur}", {"x": 120}, {"x": 0}, t + STEP, 2)
        elif kind == "redflood":    # red blooms flood the frame, a red smear, a white negative, a dark blur, a flare (2.83-3.5 s)
            for j in range(5):
                js(f'tl.set("#bl{j}", {{opacity: 1}}, {p3 + j % 3 * STEP:.3f});')
                tween(f"#bl{j}", {"scale": 0}, {"scale": 3.2}, p3 + j % 3 * STEP, 3)
                js(f'tl.set("#bl{j}", {{opacity: 0}}, {t + STEP:.3f});')
            js(f'tl.set("#redf", {{opacity: 1, x: 0, filter: "url(#hblur)"}}, {t:.3f});')
            js(f'tl.set("#redf", {{opacity: 0}}, {t + STEP:.3f});')
            js(f'tl.set("#stage", {{filter: "invert(1) grayscale(1) brightness(1.5)"}}, {t + STEP:.3f});')
            js(f'tl.set("#stage", {{filter: "brightness(.45) blur(10px)"}}, {t + 2 * STEP:.3f});')
            js(f'tl.set("#stage", {{filter: "none"}}, {t + 3 * STEP:.3f});')
            js(f'tl.set("#flare", {{opacity: 1}}, {t + 3 * STEP:.3f});')
            tween("#flare", {"x": -900}, {"x": 900}, t + 3 * STEP, 3)
            js(f'tl.set("#flare", {{opacity: 0}}, {t + 6 * STEP:.3f});')
            tween(f"#{cur}", {"scale": 1.1, "filter": "blur(10px)"}, {"scale": 1, "filter": "blur(0px)"}, t + 3 * STEP, 3)
        elif kind == "lightband":   # to black, a light burst, a red band sweeps across onto the new scene (4.0-4.33 s)
            js(f'tl.set("#blk", {{opacity: 1}}, {p1:.3f});')
            js(f'tl.set("#blk", {{opacity: 0}}, {t + STEP:.3f});')
            js(f'tl.set("#glow", {{opacity: 1}}, {t:.3f});')
            tween("#glow", {"scale": .4}, {"scale": 1.6}, t, 2)
            js(f'tl.set("#glow", {{opacity: 0}}, {t + 2 * STEP:.3f});')
            js(f'tl.set("#band", {{opacity: 1}}, {t + STEP:.3f});')
            tween("#band", {"x": -1500}, {"x": 1500}, t + STEP, 4)
            js(f'tl.set("#band", {{opacity: 0}}, {t + 5 * STEP:.3f});')
            tween(f"#{cur}", {"x": -160, "filter": "url(#hblur)"}, {"x": 0, "filter": "blur(0px)"}, t + STEP, 4)
        elif kind == "vscroll":     # vertical scroll blur (5.33-5.8 s)
            tween(f"#{prev}", {"y": 0, "filter": "blur(0px)"}, {"y": 600, "filter": "url(#vblur)"}, p2, 2)
            tween(f"#{cur}", {"y": -700, "filter": "url(#vblur)"}, {"y": 0, "filter": "blur(0px)"}, t, 4)
        elif kind == "defocus":     # defocus, a white frame, the new scene as a washed-out negative, then clean (7.0-7.2 s)
            tween(f"#{prev}", {"filter": "blur(0px)"}, {"filter": "blur(18px)"}, p2, 2)
            white(t)
            js(f'tl.set("#{cur}", {{filter: "invert(1) grayscale(1) brightness(1.6) contrast(.55) blur(6px)"}}, {t + STEP:.3f});')
            js(f'tl.set("#{cur}", {{filter: "invert(1) grayscale(1) brightness(1.3) contrast(.7) blur(2px)"}}, {t + 2 * STEP:.3f});')
            js(f'tl.set("#{cur}", {{filter: "none"}}, {t + 3 * STEP:.3f});')
        elif kind == "zoomwhite":   # radial zoom blur out to white, the next scene zooms down out of it (9.2 s)
            tween(f"#{prev}", {"scale": 1, "filter": "blur(0px) brightness(1)"}, {"scale": 1.5, "filter": "blur(20px) brightness(2)"}, p2, 2)
            js(f'tl.set("#burst", {{opacity: 1}}, {p1:.3f});')
            js(f'tl.set("#burst", {{opacity: 0}}, {t + STEP:.3f});')
            white(t)
            tween(f"#{cur}", {"scale": 1.35, "filter": "blur(16px)"}, {"scale": 1, "filter": "blur(0px)"}, t + STEP, 3)
        elif kind == "smoke":       # a smoke burst covers the cut and clears (7.89 s)
            for j in range(6):
                js(f'tl.set("#sm{j}", {{opacity: .95}}, {p2:.3f});')
                tween(f"#sm{j}", {"scale": .2}, {"scale": 1.6}, p2, 3)
                tween(f"#sm{j}", {"opacity": .95}, {"opacity": 0}, t + 2 * STEP, 4)
            tween(f"#{cur}", {"scale": 1.08}, {"scale": 1}, t, 4)
    end = q(59.45)              # the end: zoom out to white and hold (reference 9.2-9.4 s)
    tween("#stage", {"scale": 1, "filter": "blur(0px) brightness(1)"}, {"scale": 1.5, "filter": "blur(20px) brightness(2.2)"}, end - 2 * STEP, 2)
    js(f'tl.set("#flash", {{opacity: 1}}, {end:.3f});')


def drifts():
    """Slow, smooth drift per scene (no shake): background, subject and overlay type at different rates."""
    for t0, t1, i, bg, lys, (dx, dy), _ in SCENES:
        n = max(1, round((t1 - t0) * FPS)) + 4
        for k, (f, z) in enumerate(((.4, .015), (1.0, .03), (1.4, .045))):
            js(f'tl.fromTo("#{i} .ly{k}", {{x: 0, y: 0, scale: 1}}, {{x: {dx * f:.0f}, y: {dy * f:.0f}, scale: {1 + z:.3f}, '
               f'duration: {n * STEP:.3f}, ease: "steps({n})", immediateRender: false}}, {t0:.3f});')


def ink_path():
    g = random.Random(9)
    pts = []
    for k in range(28):
        a = k / 28 * math.tau
        r = 380 * (1 + g.uniform(-.25, .25) + (.45 if k % 5 == 0 else 0))
        pts.append((540 + r * math.cos(a), 540 + r * math.sin(a)))
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f} " + " ".join(
        f"Q{pts[k % 28][0]:.0f} {pts[k % 28][1]:.0f} {(pts[k % 28][0] + pts[(k + 1) % 28][0]) / 2:.0f} {(pts[k % 28][1] + pts[(k + 1) % 28][1]) / 2:.0f}"
        for k in range(1, 29)) + " Z"
    return d


def burst_svg():
    return "".join(f'<polygon points="540,540 {540 + 1100 * math.cos(a - .03):.0f},{540 + 1100 * math.sin(a - .03):.0f} '
                   f'{540 + 1100 * math.cos(a + .03):.0f},{540 + 1100 * math.sin(a + .03):.0f}"/>'
                   for a in [k * math.tau / 40 + random.Random(k).uniform(-.04, .04) for k in range(40)])


CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Kaushan Script"; src: url("assets/fonts/KaushanScript.ttf"); }}
@font-face {{ font-family: "Permanent Marker"; src: url("assets/fonts/PermanentMarker.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {S}px; height: {S}px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: {S}px; height: {S}px; overflow: hidden; background: {INK}; }}
#stage {{ position: absolute; inset: 0; }}
.sc {{ position: absolute; inset: 0; overflow: hidden; opacity: 0; }}
.ly0, .ly1, .ly2 {{ position: absolute; inset: 0; }}
.ly1 {{ z-index: 2; }} .ly2 {{ z-index: 3; }}
.pn {{ position: absolute; display: block; }}
.spot {{ position: absolute; inset: -60px; display: block; z-index: 0; }}
.tone {{ position: absolute; inset: 0; display: block; pointer-events: none; mix-blend-mode: multiply;
  background: radial-gradient(circle, #000 0 32%, transparent 36%) 0 0 / 8px 8px; }}
.ph {{ position: absolute; }}
.ph .pu, .ph .in, .ph .slc, .ph .slc > div {{ position: absolute; inset: 0; }}
.ph .slc {{ opacity: 0; }}
.ph img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ph.card .pu {{ box-shadow: 0 0 0 8px {CRM}, 18px 18px 0 8px {RED}; }}
.tx {{ position: absolute; white-space: nowrap; line-height: .9; transform-origin: 50% 30%; }}
.tx .c {{ display: inline-block; }}
.tx .cz {{ filter: blur(6px); }}
.xm {{ position: absolute; font-family: "Permanent Marker"; line-height: 1; -webkit-text-stroke: 3px {INK}; paint-order: stroke fill; }}
.spark {{ position: absolute; width: 30px; height: 30px; margin: -15px 0 0 -15px; border-radius: 50%; background: #fff;
  box-shadow: 0 0 22px 12px rgba(255,255,255,.85), 0 0 60px 26px rgba(255,240,210,.5); display: block; }}
.sls, .sb, .swl {{ position: absolute; inset: 0; width: {S}px; height: {S}px; overflow: visible; }}
.sb path {{ fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1000; }}
.swl circle {{ fill: none; opacity: .55; }}
.pt {{ position: absolute; display: block; }}
.ember {{ border-radius: 50%; background: #ffb347; box-shadow: 0 0 10px 4px #ff5a1a; }}
.star {{ background: #fff; clip-path: polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%);
  filter: drop-shadow(0 0 6px #fff); }}
.dia {{ background: linear-gradient(135deg, #fff 0 30%, #bfc6cc 31% 60%, #fff 61%); clip-path: polygon(50% 0,100% 35%,50% 100%,0 35%);
  filter: drop-shadow(0 0 8px #fff); }}
.smk {{ border-radius: 50%; background: radial-gradient(circle, #efe3c8 0%, rgba(230,215,185,.6) 40%, rgba(200,185,160,0) 70%);
  filter: blur(16px); }}
.petal {{ border-radius: 60% 0 60% 0; background: {RED}; }}
.call {{ position: absolute; border-radius: 46px; overflow: hidden; border: 9px solid #2b2b2b; box-shadow: 0 0 0 6px {CRM}, 16px 16px 0 6px {RED}; }}
.call img {{ width: 100%; height: 100%; display: block; }}
.call b {{ position: absolute; left: 0; right: 0; top: 13%; text-align: center; font: 400 64px/1 "Anton"; color: #fff; }}
.call small {{ position: absolute; left: 0; right: 0; top: 23%; text-align: center; font: 400 24px/1 "Anton"; color: #bbb; letter-spacing: .1em; }}
.call .hit {{ position: absolute; width: 22.5%; aspect-ratio: 1; border-radius: 50%; translate: -50% -50%; opacity: 0; }}
#blk {{ position: absolute; inset: 0; z-index: 40; background: {INK}; opacity: 0; }}
#ink {{ position: absolute; inset: 0; width: {S}px; height: {S}px; z-index: 41; opacity: 0; overflow: visible; filter: url(#rough); }}
.bloom {{ position: absolute; width: 520px; height: 520px; border-radius: 50%; z-index: 41; opacity: 0;
  background: radial-gradient(circle, {RED} 0 45%, rgba(215,25,42,.7) 60%, rgba(215,25,42,0) 72%); filter: blur(6px); }}
#redf {{ position: absolute; inset: -40px; z-index: 42; opacity: 0;
  background: repeating-linear-gradient(0deg, {RED} 0 46px, #b3101e 46px 60px, {RED} 60px 120px, #e8323f 120px 128px); }}
#burst {{ position: absolute; inset: 0; width: {S}px; height: {S}px; z-index: 43; opacity: 0; fill: #fff; overflow: visible;
  filter: blur(3px); }}
#glow {{ position: absolute; inset: 0; z-index: 43; opacity: 0;
  background: radial-gradient(ellipse 50% 40% at 30% 60%, #fff 0 25%, rgba(240,235,220,.85) 45%, rgba(0,0,0,0) 75%); }}
#band {{ position: absolute; left: -200px; top: 260px; width: 1480px; height: 520px; z-index: 43; opacity: 0; background: {RED};
  transform: rotate(-12deg); filter: url(#hblur); }}
#flare {{ position: absolute; left: 200px; top: -200px; width: 160px; height: 1480px; z-index: 44; opacity: 0; background: #fff;
  transform: rotate(62deg); box-shadow: 0 0 80px 50px rgba(255,255,255,.8); filter: blur(8px); }}
.smb {{ position: absolute; width: 900px; height: 900px; border-radius: 50%; z-index: 44; opacity: 0;
  background: radial-gradient(circle, #f2f2f2 0 30%, rgba(220,220,220,.85) 50%, rgba(200,200,200,0) 70%); filter: blur(14px); }}
#flash {{ position: absolute; inset: 0; z-index: 46; background: {WHT}; opacity: 0; }}
#grain {{ position: absolute; inset: -40px; z-index: 35; pointer-events: none; opacity: .08; mix-blend-mode: overlay;
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
    blooms = "".join(f'<i class="bloom" id="bl{j}" style="left:{x}px;top:{y}px"></i>'
                     for j, (x, y) in enumerate(((-80, -60), (600, 80), (240, 420), (700, 620), (-60, 640))))
    smokes = "".join(f'<i class="smb" id="sm{j}" style="left:{x}px;top:{y}px"></i>'
                     for j, (x, y) in enumerate(((-300, 300), (400, 400), (100, -200), (500, -100), (-200, -300), (300, 100))))
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
      <feGaussianBlur stdDeviation="0 34"/></filter><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="3" seed="4"/>
      <feDisplacementMap in="SourceGraphic" scale="90"/><feGaussianBlur stdDeviation="3"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{S}" data-height="{S}">
      <div id="stage">
        <div id="scenes">{scenes}</div>
      </div>
      <div id="blk"></div>
      <svg id="ink" viewBox="0 0 1080 1080"><path d="{ink_path()}" fill="{RED}"/></svg>
      {blooms}
      <div id="redf"></div>
      <svg id="burst" viewBox="0 0 1080 1080">{burst_svg()}</svg>
      <div id="glow"></div>
      <div id="band"></div>
      <div id="flare"></div>
      {smokes}
      <div id="flash"></div>
      <div id="grain"></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
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
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SCENES)} scenes")


if __name__ == "__main__":
    main()
