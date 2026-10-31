"""Spin Bout U (Drake & 21 Savage) lyric edit, 1:1, 60 s from the 2:13 bass drop: writes index.html.

python3 build/generate.py      (from the project root; after build/align.py and build/assets.py)

Built on the owner's two references: a Spin Bout U edit (square, black / maroon / magenta / off-white, hard halftone
B&W photos and cut-outs, giant condensed caps layered behind the subject, magenta starburst badges, tag boxes, a script
accent, a rounded photo card, corner credits typed on, zoom-blur and white-flash cuts, photo collages sliding into a
grid) and an MJ "Smooth Criminal" edit (red scribble strokes, neon outline on the cut-out, slanted colour bands,
directional smears, inverted flash frames). Frame pacing as in both: everything moves on a 20 fps step and the video is
rendered at 20 fps. Captions are the owner's lyrics word for word (two n-words shown as N*GGA), each group appearing on
its sung word (plan/lines.json). The owner's images map to the lines in plan/assets.md; the globe is drawn here.
"""
import json
import math
import os
import random

from PIL import Image, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, DUR, FPS = 1080, 60.0, 20
STEP = 1 / FPS
L = json.load(open(os.path.join(ROOT, "plan", "lines.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats.json")))["beats"]
INK, MAR, MAG, WHT, GRY = "#191919", "#5f1b30", "#a3214c", "#f0f2f2", "#8a8487"
ANTON = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Anton.ttf"), 100)
A, HIDE, BODY = [], [], []
R = random.Random(7)
NID = [0]
CUR = [None]


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def q(t):
    """Snap a time to the 20 fps grid."""
    return round(t * FPS) / FPS


def word(li, k):
    w, s, e = L[li]["words"][k]
    return w, s


def text(li, i0, i1):
    t = " ".join(w for w, s, e in L[li]["words"][i0:i1 + 1])
    for a, b in (("niggas", "n*ggas"), ("nigga", "n*gga")):
        t = t.replace(a, b)
    return t


def at(li, k):
    return q(L[li]["words"][k][1])


def tw(t, size):
    return ANTON.getlength(t) * size / 100


def fit(t, maxw, size):
    return min(size, maxw / max(1, tw(t, 100)) * 100)


# ------------------------------------------------------------------------------------------------ primitives
def put(html):
    CUR[0].append(html)


def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {q(t0):.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {q(t1):.3f});')


def enter(sel, t, how, n=3):
    t = q(t)
    d = n * STEP
    if how == "pop":
        js(f'tl.fromTo("{sel}", {{scale: 1.6}}, {{scale: 1, duration: {d:.3f}, ease: "steps({n})", immediateRender: false}}, {t:.3f});')
    elif how in ("left", "right", "up", "down"):
        dx, dy = {"left": (-420, 0), "right": (420, 0), "up": (0, 420), "down": (0, -420)}[how]
        js(f'tl.fromTo("{sel}", {{x: {dx}, y: {dy}, filter: "blur(10px)"}}, {{x: 0, y: 0, filter: "blur(0px)", duration: {d:.3f}, '
           f'ease: "steps({n})", immediateRender: false}}, {t:.3f});')
    elif how == "zoom":
        js(f'tl.fromTo("{sel}", {{scale: 1.25, filter: "blur(14px)"}}, {{scale: 1, filter: "blur(0px)", duration: {d:.3f}, '
           f'ease: "steps({n})", immediateRender: false}}, {t:.3f});')
    elif how == "rise":
        js(f'tl.fromTo("{sel}", {{y: 520}}, {{y: 0, duration: {d * 2:.3f}, ease: "steps({n * 2})", immediateRender: false}}, {t:.3f});')


def drift(sel, t0, t1, s=.06, x=0, y=0):
    """Slow push while it holds, stepped at 20 fps."""
    n = max(1, round((q(t1) - q(t0)) * FPS))
    js(f'tl.fromTo("{sel}", {{scale: 1, xPercent: 0, yPercent: 0}}, {{scale: {1 + s:.3f}, xPercent: {x}, yPercent: {y}, '
       f'duration: {n * STEP:.3f}, ease: "steps({n})", immediateRender: false}}, {q(t0):.3f});')


def photo(src, x, y, w, h=None, rot=0, t0=0, t1=DUR, kind="cut", frame="", how="pop", z=3, glow=False, push=.05, cls="", pos=""):
    i = nid("ph")
    path = f"assets/img/{'cut' if kind == 'cut' else 'print'}/{src}.{'png' if kind == 'cut' else 'jpg'}"
    if h is None:
        iw, ih = Image.open(os.path.join(ROOT, path)).size
        h = w * ih / iw
    style = f"left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;transform:rotate({rot}deg);z-index:{z}"
    c = f"ph {frame} {'glow' if glow else ''} {cls}".strip()
    put(f'<div class="{c}" id="{i}" style="{style}"><div class="in"><img src="{path}" alt="" style="{pos}"></div></div>')
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how)
    if push:
        drift(f"#{i} .in", t0, t1, push)
    return i


def panel(x, y, w, h, color, t0, t1=DUR, rot=0, how="left", z=1, clip=""):
    i = nid("pn")
    put(f'<i class="pn" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};'
        f'transform:rotate({rot}deg);z-index:{z};{f"clip-path:{clip};" if clip else ""}"></i>')
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how, 2)
    return i


def cap(t, x, y, size, t0, t1=DUR, font="anton", color=WHT, how="letters", align="left", z=4, rot=0, box=None, stroke=None,
        upper=True, ls=0):
    """A caption. how: letters (snap on one per frame), slide-l/r, pop, drop (letters fall), none."""
    i = nid("tx")
    y = max(y, 84)                     # keep clear of the corner credits
    s = t.upper() if upper else t
    fam = {"anton": "Anton", "script": "Kaushan Script", "marker": "Permanent Marker", "sans": "Inter Display"}[font]
    sty = (f"left:{x:.0f}px;top:{y:.0f}px;font-family:'{fam}';font-size:{size:.0f}px;color:{color};z-index:{z};"
           f"transform:rotate({rot}deg);letter-spacing:{ls}px;")
    if align == "center":
        sty += "translate:-50% 0;"
    elif align == "right":
        sty += "translate:-100% 0;"
    if box:
        sty += f"background:{box};padding:.02em .16em 0;"
    if stroke:
        sty += f"-webkit-text-stroke:{stroke};color:{INK};"      # outline type, filled with the background ink
    chars = "".join(f'<span class="c">{c if c != " " else "&nbsp;"}</span>' for c in s)
    put(f'<div class="tx" data-layout-allow-overlap id="{i}" style="{sty}">{chars}</div>')
    show(f"#{i}", t0, t1)
    t0 = q(t0)
    if how == "letters":
        js(f'tl.set("#{i} .c", {{opacity: 0}}, {t0 - .001:.3f});')
        n = len(s)
        per = 1 if n <= 8 else 2
        for k in range(0, n, per):
            js(f'tl.set("#{i} .c:nth-child(-n+{min(n, k + per)})", {{opacity: 1}}, {t0 + (k // per) * STEP:.3f});')
    elif how == "drop":
        for k in range(len(s)):
            js(f'tl.fromTo("#{i} .c:nth-child({k + 1})", {{y: -620}}, {{y: 0, duration: {3 * STEP:.3f}, ease: "steps(3)", '
               f'immediateRender: false}}, {t0 + k * STEP:.3f});')
    elif how.startswith("slide"):
        enter(f"#{i}", t0, "left" if how.endswith("l") else "right")
    elif how == "pop":
        enter(f"#{i}", t0, "pop")
    return i


def burst(lines, x, y, r, t0, t1=DUR, z=5, color=MAG, size=None):
    i = nid("bu")
    g = random.Random(int(x * 7 + y))
    pts = []
    for k in range(36):
        rr = r * (1 if k % 2 == 0 else .82 + g.uniform(-.03, .03))
        a = k / 36 * math.tau
        pts.append(f"{50 + 50 * rr / r * math.cos(a):.1f}% {50 + 50 * rr / r * math.sin(a):.1f}%")
    size = size or r * .62 / max(1, len(lines)) * 1.6
    inner = "<br>".join(lines)
    put(f'<div class="bu" id="{i}" style="left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r:.0f}px;height:{2 * r:.0f}px;'
        f'background:{color};clip-path:polygon({",".join(pts)});z-index:{z};font-size:{size:.0f}px">{inner}</div>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i}", {{scale: 0, rotation: -30}}, {{scale: 1, rotation: 0, duration: {3 * STEP:.3f}, ease: "steps(3)", '
       f'immediateRender: false}}, {q(t0):.3f});')
    return i


def scribble(pts, t0, t1=DUR, color="#e0242f", width=7, dur=.3, z=6):
    """A hand-drawn stroke tracing round the subject (the MJ reference's red strokes), drawn on in steps."""
    i = nid("sb")
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    put(f'<svg class="sb" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}"><path d="{d}" pathLength="1000" '
        f'style="stroke:{color};stroke-width:{width}"/></svg>')
    show(f"#{i}", t0, t1)
    n = max(2, round(dur * FPS))
    js(f'tl.fromTo("#{i} path", {{strokeDashoffset: 1000}}, {{strokeDashoffset: 0, duration: {n * STEP:.3f}, ease: "steps({n})", '
       f'immediateRender: false}}, {q(t0):.3f});')


def jag(cx, cy, rx, ry, seed, n=16, wob=.22, turns=1.0):
    g = random.Random(seed)
    return [(cx + rx * (1 + g.uniform(-wob, wob)) * math.cos(k / n * math.tau * turns),
             cy + ry * (1 + g.uniform(-wob, wob)) * math.sin(k / n * math.tau * turns)) for k in range(n + 1)]


def phone_card(x, y, w, caller, t0, t1, press=None, accept=True, z=3, how="up"):
    """The owner's incoming-call screen in a phone frame, the caller's name set on it; press = when a button is hit."""
    i = nid("call")
    h = w * 1792 / 828
    put(f'<div class="call" id="{i}" style="left:{x}px;top:{y}px;width:{w:.0f}px;height:{h:.0f}px;z-index:{z}">'
        f'<img src="assets/img/src/incoming_call.jpg" alt=""><b>{caller}</b><small>mobile</small>'
        f'<i class="hit" style="left:{(79 if accept else 21)}%;top:77%;background:{"#3fd25c" if accept else "#ff3b30"}"></i></div>')
    show(f"#{i}", t0, t1)
    enter(f"#{i}", t0, how, 3)
    k = 0
    tt = q(t0) + .3
    while tt < (press or t1) - .1:                     # the button pulses until it is hit
        js(f'tl.set("#{i} .hit", {{opacity: {.5 if k % 2 == 0 else 0}, scale: {1.6 if k % 2 == 0 else 1}}}, {tt:.3f});')
        tt += .2
        k += 1
    if press:
        js(f'tl.set("#{i} .hit", {{opacity: .95, scale: 1}}, {q(press):.3f});')
        js(f'tl.to("#{i} .hit", {{scale: 30, opacity: 1, duration: {4 * STEP:.3f}, ease: "steps(4)"}}, {q(press) + STEP:.3f});')
    return i


def globe(cx, cy, r, t0, t1, z=3):
    """Our own globe (the supplied one carried a stock watermark): a turning wireframe, dashed orbit, three planes."""
    i = nid("gl")
    par = "".join(f'<ellipse cx="{cx}" cy="{cy + r * math.sin(a):.0f}" rx="{r * math.cos(a):.0f}" ry="{r * .08 * math.cos(a):.0f}"/>'
                  for a in (-1.0, -.5, 0, .5, 1.0))
    mer = "".join(f'<ellipse class="m{k}" cx="{cx}" cy="{cy}" rx="{r}" ry="{r}"/>' for k in range(6))
    plane = ('<path d="M0 -14 L4 -4 L22 4 L22 8 L4 4 L3 14 L9 18 L9 21 L0 18 L-9 21 L-9 18 L-3 14 L-4 4 L-22 8 L-22 4 L-4 -4 Z" '
             'fill="#f0f2f2"/>')
    planes = "".join(f'<g class="pl" id="{i}p{k}">{plane}</g>' for k in range(3))
    put(f'<svg class="gl" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}"><circle cx="{cx}" cy="{cy}" r="{r}" class="rim"/>'
        f'{par}{mer}<ellipse class="orb" cx="{cx}" cy="{cy}" rx="{r * 1.55:.0f}" ry="{r * .5:.0f}" '
        f'transform="rotate(-18 {cx} {cy})"/>{planes}</svg>')
    show(f"#{i}", t0, t1)
    enter(f"#{i}", t0, "zoom")
    n = round((q(t1) - q(t0)) * FPS)
    for f in range(n + 1):
        tt = q(t0) + f * STEP
        ph = f * .09
        for k in range(6):
            rx = abs(r * math.cos(ph + k * math.pi / 6))
            js(f'tl.set("#{i} .m{k}", {{attr: {{rx: {rx:.0f}}}}}, {tt:.3f});')
        for k in range(3):
            a = ph * .9 + k * math.tau / 3
            px, py = r * 1.55 * math.cos(a), r * .5 * math.sin(a)
            c, s_ = math.cos(math.radians(-18)), math.sin(math.radians(-18))
            X, Y = cx + px * c - py * s_, cy + px * s_ + py * c
            ang = math.degrees(math.atan2(r * .5 * math.cos(a) * c + r * 1.55 * -math.sin(a) * s_ * 0,
                                          -r * 1.55 * math.sin(a))) + 90
            js(f'tl.set("#{i}p{k}", {{attr: {{transform: "translate({X:.0f} {Y:.0f}) rotate({ang:.0f}) scale({.9 + .4 * math.sin(a):.2f})"}}, '
               f'opacity: {1 if math.sin(a) > -.3 else .35}}}, {tt:.3f});')


def road(t0, t1, z=2):
    """Perspective road lines rushing to a vanishing point (end of the road)."""
    i = nid("rd")
    vx, vy = 540, 430
    lines = "".join(f'<line x1="{vx}" y1="{vy}" x2="{x}" y2="1080"/>' for x in (-300, 180, 900, 1380))
    dashes = "".join(f'<line class="d{k}" x1="{vx}" y1="{vy}" x2="{vx}" y2="1080"/>' for k in range(1))
    put(f'<svg class="rd" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}">{lines}{dashes}</svg>')
    show(f"#{i}", t0, t1)
    n = round((q(t1) - q(t0)) * FPS)
    for f in range(n):
        js(f'tl.set("#{i} .d0", {{attr: {{"stroke-dashoffset": {-f * 26}}}}}, {q(t0) + f * STEP:.3f});')


# ------------------------------------------------------------------------------------------------ scenes
SCENES = []        # (t0, t1, id)


def scene(t0, t1, bg=INK):
    i = f"sc{len(SCENES)}"
    CUR[0] = []
    SCENES.append([q(t0), q(t1), i, bg, CUR[0]])
    return i


def lt(li):
    return q(L[li]["start"])


def build():
    E = [lt(k) for k in range(len(L))] + [DUR]

    # S0 intro: the drop. Rounded halftone card, tags, script title.
    scene(0, E[0])
    panel(0, 0, S, S, INK, 0, E[0], how="")
    put('<svg class="rays" style="z-index:1" viewBox="0 0 1080 1080">' + "".join(
        f'<polygon points="540,540 {540 + 900 * math.cos(a - .05):.0f},{540 + 900 * math.sin(a - .05):.0f} '
        f'{540 + 900 * math.cos(a + .05):.0f},{540 + 900 * math.sin(a + .05):.0f}"/>' for a in [k * math.tau / 18 for k in range(18)]) + '</svg>')
    photo("drake_back_jacket", 230, 150, 620, 780, 0, 0, E[0], kind="print", frame="round", how="zoom", push=.08,
          pos="object-position:50% 100%;transform:scale(1.9);transform-origin:50% 92%")
    cap("Drake", 170, 210, 96, .25, E[0], box=MAG, rot=-5, how="pop")
    cap("21 Savage", 650, 800, 80, .6, E[0], box=MAG, rot=-4, how="pop")
    cap("Spin", 540, 360, 230, 1.05, E[0], font="script", color=MAG, align="center", upper=False, how="pop", rot=-8)
    cap("Bout U", 540, 560, 190, 1.25, E[0], align="center", how="letters")
    scribble(jag(540, 520, 400, 190, 3, 24, .05, 1.06), 1.6, E[0], color=WHT, width=6, dur=.35, z=1)

    # S1 Jealous-ass hoes, yeah: maroon field, giant JEALOUS behind him, tag, marker yeah.
    li = 0
    scene(E[0], E[1])
    panel(0, 0, S, S, MAR, E[0], E[1], how="")
    panel(560, 0, 520, S, MAG, E[0], E[1], how="right", clip="polygon(18% 0,100% 0,100% 100%,0 100%)")
    cap("JEALOUS", 40, 40, fit("JEALOUS", 1000, 360), at(li, 0), E[1], how="letters")
    photo("drake_laugh_hands", 250, 250, 620, None, 0, at(li, 0), E[1], how="rise", push=.07)
    cap("ass hoes,", 620, 830, 110, at(li, 1), E[1], box=WHT, color=MAG, rot=-4, how="pop", z=5)
    cap("yeah", 120, 790, 150, at(li, 3), E[1], font="marker", color=WHT, upper=False, rot=-10, how="pop", z=5)
    scribble(jag(560, 520, 360, 430, 11, 18, .18), at(li, 3), E[1], dur=.35)

    # S2 ...'bout bein' in Vogue: the cat Vogue cover slides in, script VOGUE.
    li = 1
    scene(E[1], E[2])
    photo("vogue_cat_cover", 330, 70, 640, 905, 4, lt(li), E[2], kind="print", how="right", push=.05, z=2)
    cap(text(li, 0, 2), 50, 140, 96, at(li, 0), E[2])
    cap(text(li, 3, 5), 50, 260, 96, at(li, 3), E[2])
    cap(text(li, 6, 8), 50, 380, 96, at(li, 6), E[2], color=MAG)
    cap("Vogue", 360, 760, 250, at(li, 9), E[2], font="script", color=MAG, upper=False, rot=-10, how="pop", z=6)
    scribble(jag(560, 860, 300, 110, 5, 18, .08, 1.08), at(li, 9) + .15, E[2], color=WHT, width=6)

    # S3 like that R&B group from the '90s: En Vogue in a rounded card, R&B GROUP, '90s burst.
    li = 2
    scene(E[2], E[3])
    panel(0, 0, S, S, MAR, E[2], E[3], how="")
    cap(text(li, 0, 3), 540, 40, 92, at(li, 0), E[3], align="center")
    photo("envogue_funky_divas", 230, 170, 620, 620, -3, lt(li), E[3], kind="print", frame="round", how="zoom", push=.06, z=3)
    cap("R&B group", 540, 760, fit("R&B GROUP", 1000, 250), at(li, 4), E[3], align="center", z=4)
    burst(["'90s"], 900, 230, 150, at(li, 8), E[3], size=110)
    cap("from the", 120, 270, 70, at(li, 6), E[3], box=WHT, color=MAG, rot=-6, how="pop", z=5)

    # S4 Girl, one call, I'll get you in Vogue: hand with phone, the incoming call (VOGUE), accepted on "Vogue".
    li = 3
    scene(E[3], E[4])
    panel(0, 0, S, S, INK, E[3], E[4], how="")
    panel(0, 640, S, 440, MAG, E[3], E[4], how="up", clip="polygon(0 22%,100% 0,100% 100%,0 100%)")
    cap("Girl,", 60, 60, 150, at(li, 0), E[4], font="marker", upper=False, rot=-8, how="pop")
    cap("ONE CALL", 60, 230, fit("ONE CALL", 560, 260), at(li, 1), E[4])
    phone_card(640, 90, 360, "Vogue", lt(li), E[4], press=at(li, 7))
    photo("hand_phone_sticker", 40, 520, 520, None, -8, at(li, 1), E[4], how="rise", push=.04, z=4)
    cap(text(li, 3, 6), 560, 880, 86, at(li, 3), E[4], z=6, align="center")
    cap("Vogue", 820, 640, 170, at(li, 7), E[4], font="script", color=WHT, upper=False, rot=-10, how="pop", z=7)

    # S5 One call, you in runway shows: the pearl cat (runway), magenta runway band, RUNWAY / SHOWS.
    li = 4
    scene(E[4], E[5], bg=WHT)
    panel(0, 0, S, S, WHT, E[4], E[5], how="")
    panel(-100, 380, 1300, 260, MAG, E[4], E[5], rot=-12, how="left")
    photo("rolex_cat_ad", 300, 40, 700, 956, 0, lt(li), E[5], kind="print", how="zoom", push=.05, z=3, cls="mult")
    cap(text(li, 0, 1), 60, 60, 110, at(li, 0), E[5], color=INK)
    cap(text(li, 2, 3), 60, 190, 110, at(li, 2), E[5], color=INK)
    cap("RUNWAY", 30, 600, fit("RUNWAY", 760, 300), at(li, 4), E[5], color=WHT, z=5, rot=-12, how="slide-l")
    cap("SHOWS", 520, 840, 200, at(li, 5), E[5], color=INK, z=5, how="letters")

    # S6 One call, I'm sittin' front row: Drake in Chanel with a neon outline, FRONT ROW stacked behind.
    li = 5
    scene(E[5], E[6])
    panel(0, 0, S, S, INK, E[5], E[6], how="")
    for k in range(4):
        cap("FRONT ROW", 40, 90 + k * 230, 250, at(li, 4) + k * STEP, E[6], z=2,
            stroke=f"3px {WHT}" if k else None, color=MAG if k == 0 else WHT, how="none")
    photo("drake_chanel_night", 380, 160, 700, None, 0, lt(li), E[6], how="right", glow=True, push=.06, z=3)
    cap(text(li, 0, 1), 50, 40, 120, at(li, 0), E[6], box=MAG, z=5, how="pop")
    cap(text(li, 2, 3), 60, 900, 120, at(li, 2), E[6], z=5)

    # S7 One wrong call from your ex ... sent home: the EX calls and gets declined, then the dumb cat, SENT HOME.
    li = 6
    mid = at(li, 8)
    scene(E[6], E[7])
    panel(0, 0, S, S, MAR, E[6], E[7], how="")
    cap(text(li, 0, 2), 50, 60, fit(text(li, 0, 2).upper(), 600, 170), at(li, 0), mid)
    phone_card(660, 80, 340, "Ex", lt(li), mid, press=at(li, 5), accept=False)
    cap(text(li, 3, 6), 50, 300, 110, at(li, 3), mid, color=WHT, box=MAG, rot=-3)
    scribble([(640, 60), (1040, 820)], at(li, 5) + .1, mid, color="#ff3b30", width=16, dur=.15, z=8)
    scribble([(1040, 60), (640, 820)], at(li, 5) + .2, mid, color="#ff3b30", width=16, dur=.15, z=8)
    photo("cat_white_dumb", 250, 230, 580, 540, 3, mid, E[7], kind="print", frame="round", how="zoom", push=.08, z=3)
    burst(["DUMB"], 250, 260, 150, mid, E[7], size=96)
    cap(text(li, 7, 7), 60, 60, 110, at(li, 7), E[7], z=5)
    cap(text(li, 9, 11), 540, 60, 110, at(li, 9), E[7], z=5, color=MAG, box=WHT)
    cap("SENT HOME", 540, 770, fit("SENT HOME", 1000, 260), at(li, 12), E[7], align="center", z=5)

    # S8 One call and my n*ggas ten toes: Drake in Nocta, TEN TOES behind him.
    li = 7
    scene(E[7], E[8], bg=WHT)
    panel(0, 0, S, S, WHT, E[7], E[8], how="")
    cap("TEN", 30, 130, 430, at(li, 5), E[8], color=MAG, z=2)
    cap("TOES", 30, 560, 340, at(li, 6), E[8], color=INK, z=2)
    photo("drake_nocta_red", 540, 120, 540, None, 0, lt(li), E[8], how="zoom", push=.05, z=3)
    cap(text(li, 0, 2), 40, 40, 110, at(li, 0), E[8], color=WHT, box=INK, z=5, how="pop")
    cap(text(li, 3, 4), 640, 930, 100, at(li, 3), E[8], color=WHT, box=MAG, z=5, rot=-3, how="pop")

    # S9 Down to go wherever I say go: Drake points, a stroke and GO burst where he points.
    li = 8
    scene(E[8], E[9])
    panel(0, 0, S, S, INK, E[8], E[9], how="")
    panel(0, 0, S, 360, MAR, E[8], E[9], how="down")
    photo("drake_boat_sunset", 120, 260, 640, None, 0, lt(li), E[9], how="left", push=.05, z=3)
    cap(text(li, 0, 2), 60, 60, 120, at(li, 0), E[9], z=4)
    cap("WHEREVER", 40, 800, fit("WHEREVER", 1000, 250), at(li, 3), E[9], z=5, color=WHT, how="slide-r")
    scribble([(700, 300), (800, 250), (880, 220), (960, 210)], at(li, 4), E[9], color=WHT, width=8, dur=.2, z=6)
    burst(["I SAY", "GO"], 900, 230, 170, at(li, 5), E[9], size=84)

    # S10 Even if we gotta travel 'cross the globe: our globe turning, planes on the orbit.
    li = 9
    scene(E[9], E[10])
    panel(0, 0, S, S, INK, E[9], E[10], how="")
    globe(540, 560, 300, lt(li), E[10])
    cap(text(li, 0, 3), 540, 40, 96, at(li, 0), E[10], align="center")
    cap("TRAVEL", 540, 140, fit("TRAVEL", 900, 240), at(li, 4), E[10], align="center", color=MAG, z=2)
    cap("'cross the globe", 540, 900, 120, at(li, 5), E[10], align="center", box=MAG, how="pop", z=5)

    # S11 Down to take you to the end of the road, for real: the boat at sunset, the road rushing, FOR REAL.
    li = 10
    scene(E[10], E[11])
    photo("drake_boat_sunset", 0, 0, S, S, 0, lt(li), E[11], kind="print", how="zoom", push=.12, z=1)
    panel(0, 0, S, S, "rgba(25,25,25,.58)", lt(li), E[11], how="", z=1)
    road(lt(li), E[11])
    cap(text(li, 0, 3), 540, 60, 100, at(li, 0), E[11], align="center", z=4, box=INK)
    cap("TO THE END", 540, 260, 180, at(li, 4), E[11], align="center", z=4)
    cap("OF THE ROAD", 540, 470, 180, at(li, 7), E[11], align="center", z=4, color=MAG)
    cap("for real", 540, 760, 220, at(li, 10), E[11], font="marker", upper=False, align="center", rot=-8, how="pop", z=5)

    # S12 / S16 hook: The way you make me feel these days (collage builds a panel per word, script THESE DAYS)
    def hook(li, pics, bgcol):
        t0, t1 = lt(li), E[li + 1]
        scene(t0, t1)
        panel(0, 0, S, S, bgcol, t0, t1, how="")
        slots = [(30, 30, 500, 500), (550, 30, 500, 500), (30, 550, 500, 500), (550, 550, 500, 500)]
        words = [(0, 1), (2, 2), (3, 4), (5, 5)]
        for k, ((x, y, w, h), (i0, i1), (src, kind)) in enumerate(zip(slots, words, pics)):
            tt = at(li, i0)
            photo(src, x, y, w, h, R.choice([-2, 2, -1]), tt, t1, kind=kind, frame="tile", how=["left", "down", "up", "right"][k], push=.08, z=2)
            cap(text(li, i0, i1), x + w / 2, y + h - 190, fit(text(li, i0, i1).upper(), w - 40, 200), tt + STEP, t1, align="center",
                z=4, color=WHT if k % 2 == 0 else MAG)
        tdays = at(li, 6)
        panel(0, 380, S, 320, MAG, tdays, t1, rot=-6, how="left", z=5)
        cap("these days", 540, 400, 230, tdays, t1, font="script", upper=False, align="center", z=6, rot=-6, how="pop")
        burst(["THESE", "DAYS"], 880, 230, 120, at(li, 7), t1, z=7, color=INK, size=60)

    hook(11, [("drake_chanel_night", "print"), ("drake_nocta_red", "print"), ("drake_laugh_hands", "print"),
              ("drake_back_jacket", "print")], INK)

    # S13 Somethin' gettin' dropped for you, baby girl: the black cat (baby girl), DROPPED falls in.
    li = 12
    scene(E[12], E[13])
    panel(0, 0, S, S, MAR, E[12], E[13], how="")
    cap(text(li, 0, 1), 60, 60, 110, at(li, 0), E[13])
    cap("DROPPED", 40, 200, fit("DROPPED", 1000, 330), at(li, 2), E[13], how="drop", z=2)
    photo("cat_black_collar", 300, 380, 520, None, 0, lt(li), E[13], how="rise", glow=True, push=.05, z=3)
    cap(text(li, 3, 4), 60, 880, 110, at(li, 3), E[13], box=WHT, color=MAG, how="pop", z=5)
    burst(["BABY", "GIRL"], 860, 760, 170, at(li, 5), E[13], size=84)

    # S14 Smoke a n*gga top for you, baby girl: Drake in Chanel close up, SMOKE blurs in.
    li = 13
    scene(E[13], E[14])
    photo("drake_chanel_night", 0, 0, S, S, 0, lt(li), E[14], kind="print", how="zoom", push=.14, z=1)
    panel(0, 640, S, 440, INK, E[13], E[14], how="up", z=2, clip="polygon(0 30%,100% 0,100% 100%,0 100%)")
    sm = cap("SMOKE", 40, 40, fit("SMOKE", 1000, 380), at(li, 0), E[14], how="none", z=3)
    js(f'tl.fromTo("#{sm}", {{filter: "blur(30px)", opacity: 0}}, {{filter: "blur(0px)", opacity: 1, duration: {6 * STEP:.3f}, '
       f'ease: "steps(6)", immediateRender: false}}, {at(li, 0):.3f});')
    cap(text(li, 1, 3), 60, 780, 130, at(li, 1), E[14], z=4)
    cap(text(li, 4, 5), 640, 640, 110, at(li, 4), E[14], z=4, color=MAG, box=WHT)
    cap("baby girl", 540, 900, 160, at(li, 6), E[14], font="script", color=WHT, upper=False, align="center", rot=-6, how="pop", z=5)

    # S15 Burn somebody block for you: Drake from behind, BURN flickers, BLOCK stamps.
    li = 14
    scene(E[14], E[15])
    photo("drake_back_jacket", 0, 0, S, S, 0, lt(li), E[15], kind="print", how="zoom", push=.06, z=1,
          pos="object-position:50% 100%;transform:scale(1.7);transform-origin:50% 95%")
    b = cap("BURN", 40, 40, fit("BURN", 1000, 420), at(li, 0), E[15], z=3, how="none")
    tt, k = at(li, 0), 0
    while tt < E[15] - STEP:
        js(f'tl.set("#{b}", {{color: "{[MAG, WHT, "#e0242f"][k % 3]}"}}, {tt:.3f});')
        tt, k = tt + STEP, k + 1
    cap(text(li, 1, 1), 60, 520, 130, at(li, 1), E[15], z=3)
    cap("BLOCK", 540, 640, 300, at(li, 2), E[15], align="center", z=3, box=MAG, how="pop")
    cap(text(li, 3, 4), 760, 960, 90, at(li, 3), E[15], z=4)

    hook(15, [("cat_black_collar", "print"), ("vogue_cat_cover", "print"), ("envogue_funky_divas", "print"),
              ("drake_boat_sunset", "print")], MAR)

    # S17 Comin' out my body for you, baby girl: Drake laughing, neon outline, MY BODY.
    li = 16
    scene(E[16], E[17])
    panel(0, 0, S, S, MAG, E[16], E[17], how="")
    cap(text(li, 0, 1), 40, 40, 150, at(li, 0), E[17], z=2)
    cap("MY BODY", 40, 220, fit("MY BODY", 1000, 330), at(li, 2), E[17], z=2, color=INK)
    photo("drake_laugh_hands", 260, 300, 600, None, 0, lt(li), E[17], how="rise", glow=True, push=.06, z=3)
    cap(text(li, 4, 5), 60, 900, 110, at(li, 4), E[17], box=INK, z=5, how="pop")
    burst(["BABY", "GIRL"], 860, 800, 160, at(li, 6), E[17], color=INK, size=80)

    # S18 Wipe him like he snotty for you, baby girl: a magenta wipe, the dumb cat, SNOTTY in marker.
    li = 17
    scene(E[17], E[18])
    panel(0, 0, S, S, INK, E[17], E[18], how="")
    w_ = panel(-60, 0, 1200, S, MAG, at(li, 0), E[18], how="", z=6)
    js(f'tl.fromTo("#{w_}", {{x: -1300}}, {{x: 1300, duration: {6 * STEP:.3f}, ease: "steps(6)", immediateRender: false}}, {at(li, 0):.3f});')
    photo("cat_white_dumb", 300, 380, 520, 470, -4, at(li, 0) + .1, E[18], kind="print", frame="round", how="zoom", push=.08, z=3)
    cap(text(li, 0, 1), 60, 40, 180, at(li, 0) + .15, E[18], z=4)
    cap(text(li, 2, 3), 60, 250, 110, at(li, 2), E[18], z=4, color=MAG)
    cap("snotty", 540, 770, 210, at(li, 4), E[18], font="marker", upper=False, align="center", rot=-7, how="pop", z=5)
    cap(text(li, 5, 6), 700, 250, 100, at(li, 5), E[18], box=WHT, color=MAG, z=5, how="pop")
    burst(["BABY", "GIRL"], 920, 560, 150, at(li, 7), E[18], size=72)

    # S19 Comin' out my body for you: Drake in Nocta with a neon outline, mirrored SPIN BOUT U, end card.
    li = 18
    scene(E[18], DUR)
    panel(0, 0, S, S, INK, E[18], DUR, how="")
    cap("SPIN BOUT U", 540, 610, fit("SPIN BOUT U", 1040, 260), lt(li), DUR, align="center", z=2, color=MAG, how="letters")
    m = cap("SPIN BOUT U", 540, 800, fit("SPIN BOUT U", 1040, 260), lt(li), DUR, align="center", z=2, stroke=f"3px {WHT}", how="none")
    js(f'tl.set("#{m}", {{scaleY: -1}}, {lt(li):.3f});')
    photo("drake_nocta_red", 300, 90, 480, None, 0, lt(li), DUR, how="zoom", glow=True, push=.05, z=3)
    cap(text(li, 0, 1), 40, 40, 120, at(li, 0), DUR, z=4)
    cap(text(li, 2, 3), 640, 40, 120, at(li, 2), DUR, z=4, color=MAG, box=WHT)
    cap(text(li, 4, 5), 60, 420, 110, at(li, 4), DUR, z=4, box=MAG, how="pop")


def corners():
    """Corner credits typed on after the drop (the reference's frame furniture)."""
    items = [("SPIN\nBOUT U", "left:34px;top:26px;text-align:left"), ("EDITED BY\nNXTLVL SOCIAL", "left:50%;top:26px;translate:-50% 0;text-align:center"),
             ("DRAKE\n21 SAVAGE", "right:34px;top:26px;text-align:right"), ("HER\nLOSS", "left:34px;bottom:26px;text-align:left"),
             ("ONE\nCALL", "left:50%;bottom:26px;translate:-50% 0;text-align:center"), ("IN\nVOGUE", "right:34px;bottom:26px;text-align:right")]
    html = ""
    for k, (t, pos) in enumerate(items):
        i = f"cr{k}"
        chars = "".join(f'<span class="c">{"<br>" if c == chr(10) else c}</span>' for c in t)
        html += f'<div class="cr" id="{i}" style="{pos}">{chars}</div>'
        js(f'tl.set("#{i} .c", {{opacity: 0}}, 0);')
        for j in range(len(t)):
            js(f'tl.set("#{i} .c:nth-child(-n+{j + 1})", {{opacity: 1}}, {q(.9 + k * .05 + j * STEP):.3f});')
    return html


def transitions():
    """At every scene change, one of the references' cuts: zoom blur, white flash, horizontal smear, invert, magenta sweep."""
    kinds = ["zoom", "flash", "smear", "zoom", "invert", "sweep", "zoom", "smear", "flash"]
    for k in range(1, len(SCENES)):
        t = SCENES[k][0]
        prev, cur = SCENES[k - 1][2], SCENES[k][2]
        kind = kinds[k % len(kinds)]
        if kind == "zoom":
            js(f'tl.fromTo("#{cur}", {{scale: 1.3, filter: "blur(16px)"}}, {{scale: 1, filter: "blur(0px)", duration: {3 * STEP:.3f}, '
               f'ease: "steps(3)", immediateRender: false}}, {t:.3f});')
            js(f'tl.to("#{prev}", {{scale: 1.35, filter: "blur(16px)", duration: {2 * STEP:.3f}, ease: "steps(2)"}}, {t - 2 * STEP:.3f});')
        elif kind == "flash":
            js(f'tl.set("#flash", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#flash", {{opacity: .5}}, {t + STEP:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {t + 2 * STEP:.3f});')
        elif kind == "smear":
            js(f'tl.fromTo("#{cur}", {{x: 260, filter: "url(#hblur)"}}, {{x: 0, filter: "none", duration: {3 * STEP:.3f}, ease: "steps(3)", '
               f'immediateRender: false}}, {t:.3f});')
            js(f'tl.to("#{prev}", {{x: -300, duration: {2 * STEP:.3f}, ease: "steps(2)"}}, {t - 2 * STEP:.3f});')
            js(f'tl.set("#{prev}", {{filter: "url(#hblur)"}}, {t - 2 * STEP:.3f});')
        elif kind == "invert":
            js(f'tl.set("#stage", {{filter: "invert(1)"}}, {t:.3f});')
            js(f'tl.set("#stage", {{filter: "none"}}, {t + 2 * STEP:.3f});')
        elif kind == "sweep":
            js(f'tl.set("#sweep", {{opacity: 1}}, {t - 2 * STEP:.3f});')
            js(f'tl.fromTo("#sweep", {{x: -1300}}, {{x: 1300, duration: {4 * STEP:.3f}, ease: "steps(4)", immediateRender: false}}, {t - 2 * STEP:.3f});')
            js(f'tl.set("#sweep", {{opacity: 0}}, {t + 2 * STEP:.3f});')
    js(f'tl.set("#flash", {{opacity: 1}}, {q(L[-1]["end"] + .3):.3f});')     # end: white flash out
    js(f'tl.to("#flash", {{opacity: 0, duration: {4 * STEP:.3f}, ease: "steps(4)"}}, {q(L[-1]["end"] + .35):.3f});')


def camera():
    """The frame bumps on every beat (half-time) and shakes a little, stepped at 20 fps."""
    g = random.Random(4)
    for f in range(int(DUR * FPS)):
        t = f * STEP
        lb = max([b for b in BEATS[::2] if b <= t + 1e-6] or [-9])
        bump = math.exp(-(t - lb) / .08)
        js(f'tl.set("#cam", {{scale: {1 + .03 * bump:.4f}, x: {g.uniform(-2, 2) * (1 + 3 * bump):.1f}, y: {g.uniform(-2, 2) * (1 + 3 * bump):.1f}}}, {t:.3f});')


CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Kaushan Script"; src: url("assets/fonts/KaushanScript.ttf"); }}
@font-face {{ font-family: "Permanent Marker"; src: url("assets/fonts/PermanentMarker.ttf"); }}
@font-face {{ font-family: "Inter Display"; font-weight: 600; src: url("assets/fonts/InterDisplay-SemiBold.otf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {S}px; height: {S}px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: {S}px; height: {S}px; overflow: hidden; background: {INK}; }}
#stage, #cam {{ position: absolute; inset: 0; }}
.sc {{ position: absolute; inset: 0; overflow: hidden; opacity: 0; }}
.pn {{ position: absolute; display: block; }}
.ph {{ position: absolute; }}
.ph .in {{ width: 100%; height: 100%; overflow: hidden; }}
.ph img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ph.round .in {{ border-radius: 40px; box-shadow: 0 20px 40px rgba(0,0,0,.45); }}
.ph.tile .in {{ border: 6px solid {WHT}; box-shadow: 0 14px 30px rgba(0,0,0,.5); }}
.ph.glow img {{ filter: drop-shadow(0 0 0 #fff) drop-shadow(0 0 3px #fff) drop-shadow(0 0 3px #fff) drop-shadow(0 0 14px rgba(255,255,255,.7)); }}
.ph.mult img {{ mix-blend-mode: multiply; }}
.tx {{ position: absolute; white-space: nowrap; line-height: .95; text-transform: none; }}
.bu {{ position: absolute; display: flex; align-items: center; justify-content: center; text-align: center; color: {WHT};
  font-family: "Anton"; line-height: .95; }}
.sb {{ position: absolute; inset: 0; width: {S}px; height: {S}px; overflow: visible; }}
.sb path {{ fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1000; }}
.rays {{ position: absolute; inset: 0; width: {S}px; height: {S}px; }}
.rays polygon {{ fill: {MAR}; }}
.call {{ position: absolute; border-radius: 46px; overflow: hidden; border: 9px solid #2b2b2b; box-shadow: 0 20px 40px rgba(0,0,0,.5); }}
.call img {{ width: 100%; height: 100%; display: block; }}
.call b {{ position: absolute; left: 0; right: 0; top: 13%; text-align: center; font: 600 54px/1 "Inter Display"; color: #fff; }}
.call small {{ position: absolute; left: 0; right: 0; top: 21%; text-align: center; font: 600 22px/1 "Inter Display"; color: #bbb; }}
.call .hit {{ position: absolute; width: 22.5%; aspect-ratio: 1; border-radius: 50%; translate: -50% -50%; opacity: 0; }}
.gl {{ position: absolute; inset: 0; width: {S}px; height: {S}px; overflow: visible; }}
.gl circle, .gl ellipse {{ fill: none; stroke: {MAG}; stroke-width: 4; }}
.gl .rim {{ stroke: {WHT}; stroke-width: 6; }}
.gl .orb {{ stroke: {WHT}; stroke-width: 3; stroke-dasharray: 14 12; }}
.rd {{ position: absolute; inset: 0; width: {S}px; height: {S}px; }}
.rd line {{ stroke: {WHT}; stroke-width: 6; opacity: .85; }}
.rd .d0 {{ stroke-width: 14; stroke-dasharray: 34 26; }}
.cr {{ position: absolute; z-index: 30; font: 600 15px/1.15 "Inter Display"; color: {WHT}; letter-spacing: .5px; }}
#flash {{ position: absolute; inset: 0; z-index: 40; background: {WHT}; opacity: 0; }}
#sweep {{ position: absolute; left: -60px; top: 0; width: 1200px; height: {S}px; z-index: 39; background: {MAG}; opacity: 0; }}
#grain {{ position: absolute; inset: -40px; z-index: 35; pointer-events: none; opacity: .07; mix-blend-mode: overlay;
  background: url(assets/img/grain.png); }}
"""


def main():
    build()
    cr = corners()
    transitions()
    camera()
    g = random.Random(2)
    for f in range(int(DUR * FPS)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f * STEP:.3f});')
    scenes = ""
    for k, (t0, t1, i, bg, parts) in enumerate(SCENES):
        scenes += f'<div class="sc" id="{i}" style="z-index:{k + 1};background:{bg}">{"".join(parts)}</div>'
        js(f'tl.set("#{i}", {{opacity: 1}}, {t0:.3f});')
        if t1 < DUR:
            js(f'tl.set("#{i}", {{opacity: 0}}, {t1:.3f});')
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
      <feGaussianBlur stdDeviation="28 0"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{S}" data-height="{S}">
      <div id="stage"><div id="cam">
        <div id="scenes" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2">{scenes}</div>
      </div></div>
      {cr}
      <div id="sweep"></div>
      <div id="flash"></div>
      <div id="grain"></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(list(dict.fromkeys(HIDE)))}, {{opacity: 0}});
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
