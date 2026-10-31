"""Spin Bout U (Drake & 21 Savage) lyric edit, 1:1, 60 s from the 2:13 bass drop, v2: writes index.html.

python3 build/generate.py      (from the project root; after build/align.py, build/assets.py and build/glyphs.py)

Built on the owner's two references, read frame by frame: a Spin Bout U edit (square; black / maroon / magenta /
off-white; hard halftone B&W photos and cut-outs; giant condensed caps layered behind the subject; magenta starbursts
and tag boxes; a script accent; a photo card that tilts in in perspective; cuts by sideways whip-smear with a light
streak, zoom blur to a white frame, a circle reveal, a vertical drop blur, sliding strips, a small spinning card that
zooms up to full frame, a white swoosh line) and an MJ "Smooth Criminal" edit (red scribbles, neon outlines, inverted
frames). Motion tracking: every scene is three depth layers (background, subject with the words attached to it,
overlay type) moved by one camera path at different rates. Everything steps at 20 fps and renders at 20 fps.
Each of the owner's photos is used once; every other line has its own 3D render (assets/js/g3d.js, Three.js).
Captions are the owner's lyrics on their sung words, with every cuss word shown only as a blurred ****.
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
INK, MAR, MAG, WHT = "#191919", "#5f1b30", "#a3214c", "#f0f2f2"
ANTON = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Anton.ttf"), 100)
CURSE = {"ass", "hoes", "nigga", "niggas", "shitll", "shit"}
A, HIDE, G3D = [], [], []
R = random.Random(7)
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


def tw(t, size):
    return ANTON.getlength(t) * size / 100


def fit(t, maxw, size):
    return min(size, maxw / max(1, tw(t, 100)) * 100)


# ------------------------------------------------------------------------------------------------ primitives
def put(html, ly=1):
    CUR["ly"][ly].append(html)


def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {q(t0):.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {q(t1):.3f});')


def enter(sel, t, how, n=3):
    t, d = q(t), n * STEP
    imm = "immediateRender: false"
    if how == "pop":
        js(f'tl.fromTo("{sel}", {{scale: 1.6}}, {{scale: 1, duration: {d:.3f}, ease: "steps({n})", {imm}}}, {t:.3f});')
    elif how in ("left", "right", "up", "down"):
        dx, dy = {"left": (-460, 0), "right": (460, 0), "up": (0, 460), "down": (0, -460)}[how]
        js(f'tl.fromTo("{sel}", {{x: {dx}, y: {dy}, filter: "blur(12px)"}}, {{x: 0, y: 0, filter: "blur(0px)", duration: {d:.3f}, '
           f'ease: "steps({n})", {imm}}}, {t:.3f});')
    elif how == "zoom":
        js(f'tl.fromTo("{sel}", {{scale: 1.3, filter: "blur(16px)"}}, {{scale: 1, filter: "blur(0px)", duration: {d:.3f}, '
           f'ease: "steps({n})", {imm}}}, {t:.3f});')
    elif how == "rise":
        js(f'tl.fromTo("{sel}", {{y: 560}}, {{y: 0, duration: {d * 2:.3f}, ease: "steps({n * 2})", {imm}}}, {t:.3f});')
    elif how == "tilt":       # perspective tilt-in, like the reference's photo card and block letters
        js(f'tl.fromTo("{sel}", {{rotationY: 62, rotationX: -14, scale: .72, transformPerspective: 900}}, {{rotationY: 0, rotationX: 0, '
           f'scale: 1, duration: {(n + 2) * STEP:.3f}, ease: "steps({n + 2})", {imm}}}, {t:.3f});')
    elif how == "flip":
        js(f'tl.fromTo("{sel}", {{rotationX: 85, transformPerspective: 700, transformOrigin: "50% 100%"}}, {{rotationX: 0, '
           f'duration: {d:.3f}, ease: "steps({n})", {imm}}}, {t:.3f});')


def photo(src, x, y, w, h=None, rot=0, t0=0, t1=DUR, kind="cut", frame="", how="pop", z=3, glow=False, push=.04, pos="", ly=1):
    i = nid("ph")
    path = f"assets/img/{'cut' if kind == 'cut' else ('print' if kind == 'print' else 'src')}/{src}.{'png' if kind == 'cut' else 'jpg'}"
    if h is None:
        iw, ih = Image.open(os.path.join(ROOT, path)).size
        h = w * ih / iw
    c = f"ph {frame} {'glow' if glow else ''}".strip()
    put(f'<div class="{c}" id="{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;transform:rotate({rot}deg);'
        f'z-index:{z}"><div class="in"><img src="{path}" alt="" style="{pos}"></div></div>', ly)
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how)
    if push:
        n = max(1, round((q(t1) - q(t0)) * FPS))
        js(f'tl.fromTo("#{i} .in", {{scale: 1}}, {{scale: {1 + push:.3f}, duration: {n * STEP:.3f}, ease: "steps({n})", '
           f'immediateRender: false}}, {q(t0):.3f});')
    return i


def panel(x, y, w, h, color, t0, t1=DUR, rot=0, how="left", z=1, clip="", ly=0):
    i = nid("pn")
    put(f'<i class="pn" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};transform:rotate({rot}deg);'
        f'z-index:{z};{f"clip-path:{clip};" if clip else ""}"></i>', ly)
    show(f"#{i}", t0, t1)
    if how:
        enter(f"#{i}", t0, how, 2)
    return i


def cap(t, x, y, size, t0, t1=DUR, font="anton", color=WHT, how="letters", align="left", z=6, rot=0, box=None, stroke=None,
        upper=True, ly=2):
    """A caption; white or magenta type always carries a dark outline so it reads on any background."""
    i = nid("tx")
    s = t.upper() if upper else t
    fam = {"anton": "Anton", "script": "Kaushan Script", "marker": "Permanent Marker"}[font]
    sty = f"left:{x:.0f}px;top:{y:.0f}px;font-family:'{fam}';font-size:{size:.0f}px;color:{color};z-index:{z};transform:rotate({rot}deg);"
    if align == "center":
        sty += "translate:-50% 0;"
    elif align == "right":
        sty += "translate:-100% 0;"
    if box:
        sty += f"background:{box};padding:.02em .16em 0;"
    elif stroke:
        sty += f"-webkit-text-stroke:{stroke};color:{INK};"
    else:                      # an outline in the opposite tone keeps every caption readable on light or dark
        sty += f"-webkit-text-stroke:{max(4, size * .035):.0f}px {WHT if color == INK else INK};paint-order:stroke fill;"
    chars = "".join(f'<span class="c{" cz" if c == "*" else ""}">{c if c != " " else "&nbsp;"}</span>' for c in s)
    put(f'<div class="tx" data-layout-allow-overlap id="{i}" style="{sty}">{chars}</div>', ly)
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
            js(f'tl.fromTo("#{i} .c:nth-child({k + 1})", {{y: -640}}, {{y: 0, duration: {3 * STEP:.3f}, ease: "steps(3)", '
               f'immediateRender: false}}, {t0 + k * STEP:.3f});')
    elif how == "blocks":     # letters arrive as tilted blocks, one per frame (the reference's PRAY)
        for k in range(len(s)):
            js(f'tl.fromTo("#{i} .c:nth-child({k + 1})", {{rotationX: 90, opacity: 0, transformPerspective: 600}}, {{rotationX: 0, opacity: 1, '
               f'duration: {2 * STEP:.3f}, ease: "steps(2)", immediateRender: false}}, {t0 + k * STEP:.3f});')
    elif how.startswith("slide"):
        enter(f"#{i}", t0, "left" if how.endswith("l") else "right")
    elif how in ("pop", "tilt", "flip"):
        enter(f"#{i}", t0, how)
    return i


def burst(lines, x, y, r, t0, t1=DUR, z=7, color=MAG, size=None, ly=2):
    i = nid("bu")
    g = random.Random(int(x * 7 + y))
    pts = []
    for k in range(36):
        rr = 1 if k % 2 == 0 else .82 + g.uniform(-.03, .03)
        a = k / 36 * math.tau
        pts.append(f"{50 + 50 * rr * math.cos(a):.1f}% {50 + 50 * rr * math.sin(a):.1f}%")
    size = size or r * .62 / max(1, len(lines)) * 1.6
    put(f'<div class="bu" id="{i}" style="left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r:.0f}px;height:{2 * r:.0f}px;background:{color};'
        f'clip-path:polygon({",".join(pts)});z-index:{z};font-size:{size:.0f}px">{"<br>".join(lines)}</div>', ly)
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i}", {{scale: 0, rotation: -40}}, {{scale: 1, rotation: 0, duration: {3 * STEP:.3f}, ease: "steps(3)", '
       f'immediateRender: false}}, {q(t0):.3f});')


def scribble(pts, t0, t1=DUR, color="#e0242f", width=7, dur=.3, z=8, ly=2):
    i = nid("sb")
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    put(f'<svg class="sb" id="{i}" viewBox="0 0 {S} {S}" style="z-index:{z}"><path d="{d}" pathLength="1000" '
        f'style="stroke:{color};stroke-width:{width}"/></svg>', ly)
    show(f"#{i}", t0, t1)
    n = max(2, round(dur * FPS))
    js(f'tl.fromTo("#{i} path", {{strokeDashoffset: 1000}}, {{strokeDashoffset: 0, duration: {n * STEP:.3f}, ease: "steps({n})", '
       f'immediateRender: false}}, {q(t0):.3f});')


def jag(cx, cy, rx, ry, seed, n=16, wob=.22, turns=1.0):
    g = random.Random(seed)
    return [(cx + rx * (1 + g.uniform(-wob, wob)) * math.cos(k / n * math.tau * turns),
             cy + ry * (1 + g.uniform(-wob, wob)) * math.sin(k / n * math.tau * turns)) for k in range(n + 1)]


def rays(t0, t1, color=MAR, ly=0, z=1):
    put('<svg class="rays" style="z-index:%d" viewBox="0 0 1080 1080">' % z + "".join(
        f'<polygon fill="{color}" points="540,540 {540 + 900 * math.cos(a - .05):.0f},{540 + 900 * math.sin(a - .05):.0f} '
        f'{540 + 900 * math.cos(a + .05):.0f},{540 + 900 * math.sin(a + .05):.0f}"/>' for a in [k * math.tau / 18 for k in range(18)]) + '</svg>', ly)


def phone_card(x, y, w, caller, t0, t1, press, z=4, ly=1):
    i = nid("call")
    h = w * 1792 / 828
    put(f'<div class="call" id="{i}" style="left:{x}px;top:{y}px;width:{w:.0f}px;height:{h:.0f}px;z-index:{z}">'
        f'<img src="assets/img/src/incoming_call.jpg" alt=""><b>{caller}</b><small>mobile</small>'
        f'<i class="hit" style="left:79%;top:77%;background:#3fd25c"></i></div>', ly)
    show(f"#{i}", t0, t1)
    enter(f"#{i}", t0, "tilt")
    tt, k = q(t0) + .3, 0
    while tt < press - .1:
        js(f'tl.set("#{i} .hit", {{opacity: {.5 if k % 2 == 0 else 0}, scale: {1.6 if k % 2 == 0 else 1}}}, {tt:.3f});')
        tt, k = tt + .2, k + 1
    js(f'tl.set("#{i} .hit", {{opacity: .95, scale: 1}}, {q(press):.3f});')
    js(f'tl.to("#{i} .hit", {{scale: 30, opacity: 1, duration: {4 * STEP:.3f}, ease: "steps(4)"}}, {q(press) + STEP:.3f});')


def g3(kind, t0, t1, z=3, **cues):
    """A 3D render (assets/js/g3d.js), pre-rendered by build/render3d.cjs to assets/video/g3d/<id>.mp4 on the scene's
    background colour and played here; cue times are relative to t0."""
    i = nid("g")
    t0, t1 = q(t0), q(t1)
    put(f'<div class="g3" style="z-index:{z}"><video id="v{i}" class="clip" src="assets/video/g3d/{i}.mp4" data-start="{t0:.3f}" '
        f'data-duration="{t1 - t0:.3f}" data-track-index="{3 + len(G3D)}" muted playsinline></video></div>', 1)
    G3D.append({"id": i, "kind": kind, "t0": t0, "t1": t1, "bg": CUR["bg"], "cues": cues})


# ------------------------------------------------------------------------------------------------ scenes
SCENES = []        # [t0, t1, id, bg, layers, camera]


def scene(t0, t1, bg=INK, cam=(0, 0, .06)):
    """cam: (dx, dy, dz) the camera travels over the scene; the background moves at .35, the subject layer at 1, the
    overlay type at 1.45 of it (the reference's parallax)."""
    i = f"sc{len(SCENES)}"
    CUR["ly"] = [[], [], []]
    CUR["bg"] = bg
    SCENES.append([q(t0), q(t1), i, bg, CUR["ly"], cam])


def build():
    E = [lt(k) for k in range(len(L))] + [DUR]

    # S0 the drop: Drake from behind on a rounded card that tilts in over starburst rays; DRAKE / 21 SAVAGE tags; title.
    scene(0, E[0], cam=(0, -18, .1))
    rays(0, E[0])
    photo("drake_back_jacket", 230, 150, 620, 780, 0, 0, E[0], kind="print", frame="round", how="tilt", push=.08,
          pos="object-position:50% 100%;transform:scale(1.9);transform-origin:50% 92%")
    cap("Drake", 170, 210, 96, .25, E[0], box=MAG, rot=-5, how="pop", ly=1)
    cap("21 Savage", 650, 800, 80, .6, E[0], box=MAG, rot=-4, how="pop", ly=1)
    cap("Spin", 540, 330, 230, 1.05, E[0], font="script", color=MAG, align="center", upper=False, how="pop", rot=-8)
    cap("Bout U", 540, 540, 190, 1.25, E[0], align="center", how="blocks")

    # S1 Jealous-**** ****, yeah: Drake laughing, JEALOUS behind him (moves with him), a censored tag, marker yeah.
    li = 0
    scene(E[0], E[1], bg=MAR, cam=(20, -12, .08))
    panel(560, 0, 520, S, MAG, E[0], E[1], how="right", clip="polygon(18% 0,100% 0,100% 100%,0 100%)")
    cap("JEALOUS", 50, 90, fit("JEALOUS", 940, 350), at(li, 0), E[1], how="blocks", ly=1, z=2)
    photo("drake_laugh_hands", 250, 260, 620, None, 0, at(li, 0), E[1], how="rise", push=0)
    cap(text(li, 1, 2) + ",", 560, 830, 120, at(li, 1), E[1], box=WHT, color=MAG, rot=-4, how="pop")
    cap("yeah", 110, 790, 160, at(li, 3), E[1], font="marker", upper=False, rot=-10, how="pop")
    scribble(jag(560, 540, 360, 420, 11, 18, .18), at(li, 3), E[1], dur=.35)

    # S2 ...'bout bein' in Vogue: the cat Vogue cover tilts in, the words stack, script VOGUE.
    li = 1
    scene(E[1], E[2], cam=(-15, 0, .07))
    photo("vogue_cat_cover", 330, 90, 640, 905, 4, lt(li), E[2], kind="print", how="tilt", z=2)
    cap(text(li, 0, 2), 50, 150, 96, at(li, 0), E[2], how="slide-l")
    cap(text(li, 3, 5), 50, 270, 96, at(li, 3), E[2], how="slide-l")
    cap(text(li, 6, 8), 50, 390, 96, at(li, 6), E[2], color=MAG, how="slide-l")
    cap("Vogue", 360, 760, 250, at(li, 9), E[2], font="script", color=MAG, upper=False, rot=-10, how="pop")
    scribble(jag(560, 860, 300, 110, 5, 18, .08, 1.08), at(li, 9) + .15, E[2], color=WHT, width=6)

    # S3 that R&B group from the '90s: En Vogue on a rounded card, R&B GROUP, a '90s burst.
    li = 2
    scene(E[2], E[3], bg=MAR, cam=(0, 18, .08))
    cap(text(li, 0, 3), 540, 96, 92, at(li, 0), E[3], align="center", how="flip")
    photo("envogue_funky_divas", 230, 200, 620, 620, -3, lt(li), E[3], kind="print", frame="round", how="zoom", z=3)
    cap("R&B group", 540, 760, fit("R&B GROUP", 1000, 250), at(li, 4), E[3], align="center", how="blocks", ly=1, z=4)
    burst(["'90s"], 900, 260, 150, at(li, 8), E[3], size=110)
    cap("from the", 120, 300, 70, at(li, 6), E[3], box=WHT, color=MAG, rot=-6, how="pop")

    # S4 Girl, one call, I'll get you in Vogue: the hand with the phone, the call screen (Vogue) answered on "Vogue".
    li = 3
    scene(E[3], E[4], cam=(-20, 0, .06))
    panel(0, 640, S, 440, MAG, E[3], E[4], how="up", clip="polygon(0 22%,100% 0,100% 100%,0 100%)")
    cap("Girl,", 60, 96, 150, at(li, 0), E[4], font="marker", upper=False, rot=-8, how="pop")
    cap("ONE CALL", 60, 260, fit("ONE CALL", 560, 250), at(li, 1), E[4], how="blocks")
    phone_card(640, 110, 360, "Vogue", lt(li), E[4], press=at(li, 7))
    photo("hand_phone_sticker", 40, 520, 520, None, -8, at(li, 1), E[4], how="rise", push=0, z=5)
    cap(text(li, 3, 6), 560, 880, 86, at(li, 3), E[4], align="center")
    cap("Vogue", 820, 640, 170, at(li, 7), E[4], font="script", upper=False, rot=-10, how="pop", z=8)

    # S5 One call, you in runway shows: the pearl cat on its white page, a magenta runway band.
    li = 4
    scene(E[4], E[5], bg=WHT, cam=(0, -24, .06))
    panel(-100, 380, 1300, 260, MAG, E[4], E[5], rot=-12, how="left", z=2)
    photo("rolex_cat_ad", 300, 40, 700, 956, 0, lt(li), E[5], kind="print", how="zoom", z=3, ly=1)
    cap(text(li, 0, 1), 60, 96, 110, at(li, 0), E[5], color=INK, how="slide-l")
    cap(text(li, 2, 3), 60, 226, 110, at(li, 2), E[5], color=INK, how="slide-l")
    cap("RUNWAY", 30, 600, fit("RUNWAY", 760, 290), at(li, 4), E[5], rot=-12, how="slide-l")
    cap("SHOWS", 520, 840, 200, at(li, 5), E[5], color=INK, how="blocks")

    # S6 One call, I'm sittin' front row: Drake in Chanel with a neon outline, FRONT ROW stacked behind (with him).
    li = 5
    scene(E[5], E[6], cam=(-25, 0, .07))
    for k in range(4):
        cap("FRONT ROW", 40, 100 + k * 230, 250, at(li, 4) + k * STEP, E[6], z=2, ly=1,
            stroke=f"3px {WHT}" if k else None, color=MAG if k == 0 else WHT, how="none")
    photo("drake_chanel_night", 380, 170, 700, None, 0, lt(li), E[6], how="right", glow=True, push=0)
    cap(text(li, 0, 1), 50, 96, 120, at(li, 0), E[6], box=MAG, how="pop")
    cap(text(li, 2, 3), 60, 900, 120, at(li, 2), E[6])

    # S7 One wrong call from your ex **** ...: a 3D phone, the ex declined and X-ed; then the dumb cat, SENT HOME.
    li = 6
    mid = at(li, 8)
    scene(E[6], E[7], bg=MAR, cam=(0, 0, .06))
    g3("phone", lt(li), mid, hit=round(at(li, 5) - lt(li), 3))
    cap(text(li, 0, 2), 50, 96, fit(text(li, 0, 2).upper(), 980, 150), at(li, 0), mid, how="blocks")
    cap(text(li, 3, 6), 50, 860, 110, at(li, 3), mid, box=MAG)
    photo("cat_white_dumb", 250, 230, 580, 540, 3, mid, E[7], kind="print", frame="round", how="zoom", push=.08, z=4)
    burst(["DUMB"], 870, 470, 140, mid, E[7], size=92)
    cap(text(li, 7, 7), 60, 96, 100, at(li, 7), E[7])
    cap(text(li, 9, 11), 400, 96, 100, at(li, 9), E[7], color=MAG, box=WHT)
    cap("SENT HOME", 540, 780, fit("SENT HOME", 1000, 250), at(li, 12), E[7], align="center", how="blocks")

    # S8 One call and my **** ten toes: Drake in Nocta on white, TEN TOES behind him.
    li = 7
    scene(E[7], E[8], bg=WHT, cam=(15, 0, .06))
    cap("TEN", 30, 140, 430, at(li, 5), E[8], color=MAG, z=2, ly=1, how="blocks")
    cap("TOES", 30, 570, 340, at(li, 6), E[8], color=INK, z=2, ly=1, how="blocks")
    photo("drake_nocta_red", 540, 120, 540, None, 0, lt(li), E[8], how="zoom", push=0)
    cap(text(li, 0, 2), 40, 96, 110, at(li, 0), E[8], color=WHT, box=INK, how="pop")
    cap(text(li, 3, 4), 640, 930, 100, at(li, 3), E[8], color=WHT, box=MAG, rot=-3, how="pop")

    # S9 Down to go wherever I say go: Drake points from the boat, a stroke to the GO burst.
    li = 8
    scene(E[8], E[9], cam=(30, 0, .06))
    panel(0, 0, S, 360, MAR, E[8], E[9], how="down")
    photo("drake_boat_sunset", 120, 270, 640, None, 0, lt(li), E[9], how="left", push=0)
    cap(text(li, 0, 2), 60, 96, 120, at(li, 0), E[9], how="flip")
    cap("WHEREVER", 50, 800, fit("WHEREVER", 940, 250), at(li, 3), E[9], how="slide-r")
    scribble([(700, 310), (800, 260), (880, 230), (960, 220)], at(li, 4), E[9], color=WHT, width=8, dur=.2)
    burst(["I SAY", "GO"], 900, 240, 170, at(li, 5), E[9], size=84)

    # S10 travel 'cross the globe: the 3D globe, orbit and planes.
    li = 9
    scene(E[9], E[10], cam=(0, 0, .05))
    g3("globe", lt(li), E[10])
    cap(text(li, 0, 3), 540, 96, 96, at(li, 0), E[10], align="center", how="flip")
    cap("TRAVEL", 540, 200, fit("TRAVEL", 900, 230), at(li, 4), E[10], align="center", color=MAG, how="blocks")
    cap("'cross the globe", 540, 900, 120, at(li, 5), E[10], align="center", box=MAG, how="pop")

    # S11 to the end of the road, for real: the 3D road at dusk, the sign passing.
    li = 10
    scene(E[10], E[11], bg=MAR, cam=(0, 0, .03))
    g3("road", lt(li), E[11])
    cap(text(li, 0, 3), 540, 96, 100, at(li, 0), E[11], align="center", box=INK)
    cap("TO THE END", 540, 230, 170, at(li, 4), E[11], align="center", how="blocks")
    cap("OF THE ROAD", 540, 420, 170, at(li, 7), E[11], align="center", color=MAG, how="blocks")
    cap("for real", 540, 760, 220, at(li, 10), E[11], font="marker", upper=False, align="center", rot=-8, how="pop")

    # S12 hook 1: The way you make me feel these days, as 3D words; the black cat for "these days".
    li = 11
    scene(E[11], E[12], cam=(0, -18, .06))
    tl0 = lt(li)
    ws = [("THE WAY", 1.7, -0.6, 3.0, at(li, 0)), ("YOU", 2.1, 0.9, 0.9, at(li, 2)), ("MAKE ME", 1.7, -0.4, -1.2, at(li, 3)),
          ("FEEL", 2.4, 0.5, -3.5, at(li, 5))]
    g3("words", tl0, E[12], words=[{"t": w, "s": s_, "x": x, "y": y, "at": round(a - tl0, 3)} for w, s_, x, y, a in ws])
    td = at(li, 6)
    panel(0, 380, S, 320, MAG, td, E[12], rot=-6, how="left", z=5, ly=2)
    photo("cat_black_collar", 640, 90, 400, None, 6, td, E[12], how="pop", glow=True, push=0, z=6, ly=2)
    cap("these days", 470, 400, 220, td, E[12], font="script", upper=False, align="center", rot=-6, how="pop", z=7)

    # S13 Somethin' gettin' dropped for you, baby girl: 3D diamonds rain and bounce, DROPPED falls in.
    li = 12
    scene(E[12], E[13], bg=MAR, cam=(0, 24, .06))
    g3("diamonds", lt(li), E[13], drop=round(at(li, 2) - lt(li), 3))
    cap(text(li, 0, 1), 60, 96, 110, at(li, 0), E[13], how="flip")
    cap("DROPPED", 40, 210, fit("DROPPED", 1000, 300), at(li, 2), E[13], how="drop", z=2, ly=1)
    cap(text(li, 3, 4), 60, 880, 110, at(li, 3), E[13], box=WHT, color=MAG, how="pop")
    burst(["BABY", "GIRL"], 860, 790, 170, at(li, 5), E[13], size=84)

    # S14 Smoke a **** top for you, baby girl: 3D SMOKE inside rising smoke.
    li = 13
    scene(E[13], E[14], cam=(0, -18, .05))
    g3("smoke", lt(li), E[14])
    cap(text(li, 1, 3), 60, 760, 130, at(li, 1), E[14], how="slide-l")
    cap(text(li, 4, 5), 640, 640, 110, at(li, 4), E[14], color=MAG, box=WHT, how="pop")
    cap("baby girl", 540, 900, 160, at(li, 6), E[14], font="script", upper=False, align="center", rot=-6, how="pop")

    # S15 Burn somebody block for you: the 3D city block burning, BURN flickering, BLOCK stamped.
    li = 14
    scene(E[14], E[15], cam=(0, 0, .04))
    g3("city", lt(li), E[15])
    b = cap("BURN", 40, 90, fit("BURN", 1000, 400), at(li, 0), E[15], how="none")
    tt, k = at(li, 0), 0
    while tt < E[15] - STEP:
        js(f'tl.set("#{b}", {{color: "{[MAG, WHT, "#ff7a1a"][k % 3]}"}}, {tt:.3f});')
        tt, k = tt + STEP, k + 1
    cap(text(li, 1, 1), 60, 560, 130, at(li, 1), E[15], how="slide-l")
    cap("BLOCK", 540, 660, 280, at(li, 2), E[15], align="center", box=MAG, how="pop")
    cap(text(li, 3, 4), 760, 960, 90, at(li, 3), E[15])

    # S16 hook 2: the chrome heart beating, the words around it.
    li = 15
    scene(E[15], E[16], bg=MAR, cam=(0, 18, .06))
    g3("heart", lt(li), E[16], beats=[round(x, 3) for x in BEATS[::2]])
    cap("THE WAY", 60, 96, 170, at(li, 0), E[16], how="blocks")
    cap("YOU", 780, 300, 170, at(li, 2), E[16], color=MAG, how="pop")
    cap("MAKE ME", 60, 700, 150, at(li, 3), E[16], how="slide-l")
    cap("FEEL", 700, 690, 200, at(li, 5), E[16], color=MAG, how="blocks")
    cap("these days", 540, 880, 170, at(li, 6), E[16], font="script", upper=False, align="center", rot=-6, how="pop")

    # S17 Comin' out my body for you, baby girl: BODY in 3D, the letters burst apart on "out".
    li = 16
    scene(E[16], E[17], bg=MAG, cam=(0, 0, .05))
    g3("body", lt(li), E[17], out=round(at(li, 1) - lt(li), 3))
    cap(text(li, 0, 1), 60, 96, 150, at(li, 0), E[17], how="blocks")
    cap("MY", 60, 300, 150, at(li, 2), E[17], color=INK, how="pop")
    cap(text(li, 4, 5), 60, 900, 110, at(li, 4), E[17], box=INK, how="pop")
    burst(["BABY", "GIRL"], 860, 820, 160, at(li, 6), E[17], color=INK, size=80)

    # S18 Wipe him like he snotty for you, baby girl: a magenta wipe, the 3D tissue box, snotty in marker.
    li = 17
    scene(E[17], E[18], cam=(0, -12, .05))
    w_ = panel(-60, 0, 1200, S, MAG, at(li, 0), E[18], how="", z=9, ly=2)
    js(f'tl.fromTo("#{w_}", {{x: -1300}}, {{x: 1300, duration: {6 * STEP:.3f}, ease: "steps(6)", immediateRender: false}}, {at(li, 0):.3f});')
    g3("tissue", lt(li), E[18], wipe=round(at(li, 0) - lt(li) + .1, 3))
    cap(text(li, 0, 1), 60, 96, 180, at(li, 0) + .15, E[18], how="blocks")
    cap(text(li, 2, 3), 60, 290, 110, at(li, 2), E[18], color=MAG, how="slide-l")
    cap("snotty", 540, 780, 210, at(li, 4), E[18], font="marker", upper=False, align="center", rot=-7, how="pop")
    cap(text(li, 5, 6), 700, 290, 100, at(li, 5), E[18], box=WHT, color=MAG, how="pop")
    burst(["BABY", "GIRL"], 900, 560, 140, at(li, 7), E[18], size=70)

    # S19 Comin' out my body for you: the 3D logo turning over rays, the line around it.
    li = 18
    scene(E[18], DUR, cam=(0, 0, .05))
    g3("logo", lt(li), DUR)
    cap(text(li, 0, 1), 50, 96, 100, at(li, 0), DUR, how="blocks")
    cap(text(li, 2, 3), 1030, 96, 100, at(li, 2), DUR, align="right", color=MAG, box=WHT, how="pop")
    cap(text(li, 4, 5), 540, 880, 110, at(li, 4), DUR, align="center", box=MAG, how="pop")


TRANS = ["streak", "zoomwhite", "circle", "tilt", "drop", "strips", "swoosh", "spincard", "streak", "zoomwhite", "circle",
         "invert", "drop", "strips", "spincard", "swoosh", "zoomwhite", "streak", "circle"]


def transitions():
    """The reference's cuts, one per scene change (2-5 frames each at 20 fps)."""
    for k in range(1, len(SCENES)):
        t = SCENES[k][0]
        prev, cur = SCENES[k - 1][2], SCENES[k][2]
        kind = TRANS[(k - 1) % len(TRANS)]
        p2 = t - 2 * STEP
        if kind == "streak":       # sideways whip-smear out, a maroon frame with a white light bar sweeping, then the scene
            js(f'tl.to("#{prev}", {{x: -520, filter: "url(#hblur)", duration: {2 * STEP:.3f}, ease: "steps(2)"}}, {p2:.3f});')
            js(f'tl.set("#streak", {{opacity: 1}}, {t:.3f});')
            js(f'tl.fromTo("#streak i", {{x: -200}}, {{x: 1200, duration: {3 * STEP:.3f}, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
            js(f'tl.set("#streak", {{opacity: 0}}, {t + 3 * STEP:.3f});')
            js(f'tl.fromTo("#{cur}", {{x: 420, filter: "url(#hblur)"}}, {{x: 0, filter: "none", duration: {3 * STEP:.3f}, ease: "steps(3)", '
               f'immediateRender: false}}, {t + 2 * STEP:.3f});')
        elif kind == "zoomwhite":  # zoom blur to a white frame, the next scene out of the blur
            js(f'tl.to("#{prev}", {{scale: 1.45, filter: "blur(18px)", duration: {2 * STEP:.3f}, ease: "steps(2)"}}, {p2:.3f});')
            js(f'tl.set("#flash", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {t + STEP:.3f});')
            js(f'tl.fromTo("#{cur}", {{scale: 1.3, filter: "blur(18px)"}}, {{scale: 1, filter: "blur(0px)", duration: {3 * STEP:.3f}, '
               f'ease: "steps(3)", immediateRender: false}}, {t + STEP:.3f});')
        elif kind == "circle":     # whip out, the next scene opens from a circle in the corner
            js(f'tl.to("#{prev}", {{x: -560, filter: "url(#hblur)", duration: {2 * STEP:.3f}, ease: "steps(2)"}}, {p2:.3f});')
            js(f'tl.fromTo("#{cur}", {{clipPath: "circle(0% at 86% 86%)"}}, {{clipPath: "circle(150% at 86% 86%)", duration: {4 * STEP:.3f}, '
               f'ease: "steps(4)", immediateRender: false}}, {t:.3f});')
        elif kind == "tilt":       # the next scene swings in in perspective
            js(f'tl.to("#{prev}", {{filter: "blur(14px)", duration: {2 * STEP:.3f}, ease: "steps(2)"}}, {p2:.3f});')
            js(f'tl.fromTo("#{cur}", {{rotationY: 70, scale: .7, transformPerspective: 1100}}, {{rotationY: 0, scale: 1, duration: {4 * STEP:.3f}, '
               f'ease: "steps(4)", immediateRender: false}}, {t:.3f});')
        elif kind == "drop":       # vertical blur drop
            js(f'tl.to("#{prev}", {{y: 560, filter: "url(#vblur)", duration: {2 * STEP:.3f}, ease: "steps(2)"}}, {p2:.3f});')
            js(f'tl.fromTo("#{cur}", {{y: -460, filter: "url(#vblur)"}}, {{y: 0, filter: "none", duration: {3 * STEP:.3f}, ease: "steps(3)", '
               f'immediateRender: false}}, {t:.3f});')
        elif kind == "strips":     # six strips slide across and back off
            for j in range(6):
                d = 1 if j % 2 == 0 else -1
                js(f'tl.set("#st{j}", {{opacity: 1}}, {p2 - STEP:.3f});')
                js(f'tl.fromTo("#st{j}", {{y: {1100 * d}}}, {{y: 0, duration: {3 * STEP:.3f}, ease: "steps(3)", immediateRender: false}}, {p2 - STEP:.3f});')
                js(f'tl.to("#st{j}", {{y: {-1100 * d}, duration: {3 * STEP:.3f}, ease: "steps(3)"}}, {t + STEP:.3f});')
                js(f'tl.set("#st{j}", {{opacity: 0}}, {t + 4 * STEP:.3f});')
        elif kind == "swoosh":     # a white swoosh line draws across, the scene slides in under it
            js(f'tl.set("#swoosh", {{opacity: 1}}, {p2:.3f});')
            js(f'tl.fromTo("#swoosh path", {{strokeDashoffset: 1000}}, {{strokeDashoffset: -1000, duration: {5 * STEP:.3f}, ease: "steps(5)", '
               f'immediateRender: false}}, {p2:.3f});')
            js(f'tl.set("#swoosh", {{opacity: 0}}, {t + 3 * STEP:.3f});')
            js(f'tl.fromTo("#{cur}", {{x: 540, filter: "url(#hblur)"}}, {{x: 0, filter: "none", duration: {3 * STEP:.3f}, ease: "steps(3)", '
               f'immediateRender: false}}, {t:.3f});')
        elif kind == "spincard":   # white frame, the next scene starts as a small turned card and zooms up
            js(f'tl.set("#wbg", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#wbg", {{opacity: 0}}, {t + 5 * STEP:.3f});')
            js(f'tl.fromTo("#{cur}", {{scale: .28, rotation: -28, filter: "blur(6px)", borderRadius: 60}}, {{scale: 1, rotation: 0, filter: "blur(0px)", '
               f'borderRadius: 0, duration: {5 * STEP:.3f}, ease: "steps(5)", immediateRender: false}}, {t:.3f});')
        elif kind == "invert":
            js(f'tl.set("#stage", {{filter: "invert(1)"}}, {t:.3f});')
            js(f'tl.set("#stage", {{filter: "none"}}, {t + 2 * STEP:.3f});')
    end = q(L[-1]["end"] + .3)
    js(f'tl.set("#flash", {{opacity: 1}}, {end:.3f});')
    js(f'tl.to("#flash", {{opacity: 0, duration: {4 * STEP:.3f}, ease: "steps(4)"}}, {end + STEP:.3f});')


def cameras():
    """Motion tracking: per scene, the three layers ride one camera path at different rates, stepped at 20 fps,
    plus a bump on every half-time beat across the frame."""
    for t0, t1, i, bg, lys, (dx, dy, dz) in SCENES:
        n = max(1, round((t1 - t0) * FPS)) + 3
        for k, f in enumerate((.35, 1.0, 1.45)):
            js(f'tl.fromTo("#{i} .ly{k}", {{x: 0, y: 0, scale: 1}}, {{x: {dx * f:.0f}, y: {dy * f:.0f}, scale: {1 + dz * f:.3f}, '
               f'duration: {n * STEP:.3f}, ease: "steps({n})", immediateRender: false}}, {t0:.3f});')
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
#wbg {{ position: absolute; inset: 0; background: {WHT}; opacity: 0; z-index: 0; }}
.sc {{ position: absolute; inset: 0; overflow: hidden; opacity: 0; }}
.ly0, .ly1, .ly2 {{ position: absolute; inset: 0; }}
.ly1 {{ z-index: 2; }} .ly2 {{ z-index: 3; }}
.pn {{ position: absolute; display: block; }}
.ph {{ position: absolute; }}
.ph .in {{ width: 100%; height: 100%; overflow: hidden; }}
.ph img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ph.round .in {{ border-radius: 40px; box-shadow: 0 20px 40px rgba(0,0,0,.45); }}
.ph.glow img {{ filter: drop-shadow(0 0 0 #fff) drop-shadow(0 0 3px #fff) drop-shadow(0 0 3px #fff) drop-shadow(0 0 14px rgba(255,255,255,.7)); }}
.tx {{ position: absolute; white-space: nowrap; line-height: .95; }}
.tx .c {{ display: inline-block; }}
.tx .cz {{ filter: blur(5px); }}
.bu {{ position: absolute; display: flex; align-items: center; justify-content: center; text-align: center; color: {WHT};
  font-family: "Anton"; line-height: .95; }}
.sb {{ position: absolute; inset: 0; width: {S}px; height: {S}px; overflow: visible; }}
.sb path {{ fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1000; }}
.rays {{ position: absolute; inset: 0; width: {S}px; height: {S}px; }}
.g3 {{ position: absolute; inset: -80px; }}
.g3 video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.g3::after {{ content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .18; mix-blend-mode: multiply;
  background: radial-gradient(circle, #000 0 30%, transparent 33%) 0 0 / 7px 7px; }}
.call {{ position: absolute; border-radius: 46px; overflow: hidden; border: 9px solid #2b2b2b; box-shadow: 0 20px 40px rgba(0,0,0,.5); }}
.call img {{ width: 100%; height: 100%; display: block; }}
.call b {{ position: absolute; left: 0; right: 0; top: 13%; text-align: center; font: 600 54px/1 "Inter Display"; color: #fff; }}
.call small {{ position: absolute; left: 0; right: 0; top: 21%; text-align: center; font: 600 22px/1 "Inter Display"; color: #bbb; }}
.call .hit {{ position: absolute; width: 22.5%; aspect-ratio: 1; border-radius: 50%; translate: -50% -50%; opacity: 0; }}
#streak {{ position: absolute; inset: 0; z-index: 41; background: {MAR}; opacity: 0; overflow: hidden; }}
#streak i {{ position: absolute; top: -40px; left: 0; width: 26px; height: 1160px; background: {WHT}; transform: rotate(4deg);
  box-shadow: 0 0 40px 18px rgba(255,255,255,.55); }}
.strip {{ position: absolute; top: 0; width: 182px; height: {S}px; z-index: 42; opacity: 0; }}
#swoosh {{ position: absolute; inset: 0; width: {S}px; height: {S}px; z-index: 43; opacity: 0; overflow: visible; }}
#swoosh path {{ fill: none; stroke: {WHT}; stroke-width: 10; stroke-linecap: round; stroke-dasharray: 1000; }}
#flash {{ position: absolute; inset: 0; z-index: 44; background: {WHT}; opacity: 0; }}
#grain {{ position: absolute; inset: -40px; z-index: 35; pointer-events: none; opacity: .07; mix-blend-mode: overlay;
  background: url(assets/img/grain.png); }}
"""


def main():
    build()
    transitions()
    cameras()
    g = random.Random(2)
    for f in range(int(DUR * FPS)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f * STEP:.3f});')
    scenes = ""
    for k, (t0, t1, i, bg, lys, cam) in enumerate(SCENES):
        layers = "".join(f'<div class="ly{j}">{"".join(lys[j])}</div>' for j in range(3))
        scenes += f'<div class="sc" id="{i}" style="z-index:{k + 1};background:{bg}">{layers}</div>'
        js(f'tl.set("#{i}", {{opacity: 1}}, {t0:.3f});')
        if t1 < DUR:
            js(f'tl.set("#{i}", {{opacity: 0}}, {t1:.3f});')
    strips = "".join(f'<i class="strip" id="st{j}" style="left:{j * 180}px;background:{[INK, MAG, WHT][j % 3]}"></i>' for j in range(6))
    HIDE.extend([f"#st{j}" for j in range(6)])
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
      <feGaussianBlur stdDeviation="30 0"/></filter><filter id="vblur" x="-5%" y="-20%" width="110%" height="140%">
      <feGaussianBlur stdDeviation="0 30"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{S}" data-height="{S}">
      <div id="stage"><div id="wbg"></div><div id="cam">
        <div id="scenes">{scenes}</div>
      </div></div>
      <div id="streak"><i></i></div>
      {strips}
      <svg id="swoosh" viewBox="0 0 1080 1080"><path pathLength="1000" d="M-60 820 C 240 380, 620 980, 1140 260"/></svg>
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
    json.dump(G3D, open(os.path.join(ROOT, "plan", "g3d.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SCENES)} scenes, {len(G3D)} 3D renders")


if __name__ == "__main__":
    main()
