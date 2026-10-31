"""Spin Bout U (Drake & 21 Savage) lyric edit, 1:1, 60 s from the 2:13 bass drop, v9: writes index.html.

python3 build/collage.py      (from the project root; after build/assets.py, anime.py, clips90.py, collage_tex.py and
node build/render3d.cjs for the 3D elements)

The owner asked for the Ashke edit's structure (../ashke-lyric-9x16, square cut in ../ashke-lyric-1x1) in this edit's
colours. So this is the Ashke engine, ported: one big crumpled paper sheet that a virtual camera travels over (here
maroon, under soft blind shadows and faint grid lines); each lyric line is built up on it with one of the nine scene
recipes (torn paper scraps, a cut-out sticker with a paper border, photo prints with a border, labels that type on
letter by letter behind a cursor block or slam in big, stamped words, 3D words, a keyword filled with a picture that
the camera zooms into, marker circles, stars, a doodle sticker for the line); the camera never stops, glides through
each scene's labels on a time-aware spline, whips into the next scene at peak speed with directional motion blur and
punches in on every beat, stepped at 15 fps; three single-frame stills before most cuts; one-step invert, white and
split flashes. Colours: black, maroon, magenta, off-white; type Anton. Pictures: the owner's photos in the opening,
the anime art (stills and the owner's animated clips), the 3D elements. Captions are the owner's lyrics on their sung
words; every cuss word shows only as a blurred ****.
"""
import json
import math
import os
import random
import re
import sys

from PIL import Image, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doodles import ICON, WORD, svg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR, FPS = 60.0, 30
STEP = 1 / 15
FW = FH = 1080
CY, ZOOM, VTRACK = 540, .64, .55          # the board is 1080x1920 (the Ashke layouts); the square camera pulls back
L = json.load(open(os.path.join(ROOT, "plan", "lines.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats.json")))
PERIOD = 60 / BEATS["bpm"]
G3T = {e["kind"]: e["t0"] for e in json.load(open(os.path.join(ROOT, "plan", "g3d.json")))}   # the 3D clips' start times
INK, MAR, MAG, WHT = "#151314", "#5f1b30", "#b0194f", "#f2f1ec"
ANTON = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Anton.ttf"), 100)
CURSE = {"ass", "hoes", "nigga", "niggas", "shitll", "shit"}
KEY = {0: {"jealous"}, 1: {"vogue"}, 2: {"90s"}, 3: {"vogue"}, 4: {"runway"}, 5: {"row"}, 6: {"home"}, 7: {"toes"}, 8: {"go"},
       9: {"globe"}, 10: {"road"}, 11: {"feel"}, 12: {"dropped"}, 13: {"smoke"}, 14: {"block"}, 15: {"feel"}, 16: {"body"},
       17: {"snotty"}, 18: {"body"}}
PHRASES = {("for", "you"), ("baby", "girl"), ("front", "row"), ("sent", "home"), ("ten", "toes"), ("these", "days"), ("the", "way"),
           ("make", "me")}
RECIPE = {-1: "R1", 0: "R2", 1: "R3", 2: "R5", 3: "R4", 4: "R6", 5: "R8", 6: "R2", 7: "R1", 8: "R7", 9: "R3", 10: "R9", 11: "R2",
          12: "R5", 13: "R6", 14: "R4", 15: "R8", 16: "R3", 17: "R1", 18: "R9"}
CUTOUT = {-1: "drake_back_jacket", 1: "cat_black_collar", 3: "hand_phone_sticker", 5: "drake_chanel_night", 6: "cat_white_dumb",
          17: "snotty", 18: "finale"}
AF, PR, AV = "assets/img/anime/full/", "assets/img/print/", "assets/video/anime/"
CARD1 = {0: AV + "jealous.mp4", 2: PR + "envogue_funky_divas.jpg", 4: PR + "rolex_cat_ad.jpg",
         11: AV + "her_blush.mp4"}
CARD2 = {1: PR + "vogue_cat_cover.jpg", 3: "assets/img/collage/call_vogue.jpg", 9: AF + "jet.jpg", 10: AV + "road.mp4"}
CUTPRINT = {14: None, 9: None, 16: None, 7: None}     # recipes with a cut-out slot that use a picture instead
FILL = {0: AF + "jealous.jpg", 6: PR + "cat_white_dumb.jpg", 11: AF + "her_blush.jpg"}
G3D_AT = {9: ("globe", 120, 620, 860), 12: ("diamonds", 0, 360, 1080), 15: ("heart", 140, 470, 800),
          16: ("body", 0, 700, 1080), 17: ("tissue", 40, 1350, 460)}
STILLS = [AF + n + ".jpg" for n in ("jealous", "her_blush", "jet", "road", "finale", "snotty")] + [PR + "vogue_cat_cover.jpg", PR + "rolex_cat_ad.jpg", PR + "envogue_funky_divas.jpg"]
A, HIDE, PAN, SCREEN = [], [], [], []
CAMKEYS, FLASH = {}, []
LOCKS, CAMSTATE = [], {}     # screen-pinned layers inside the board; the camera per 15 fps frame (fx, fy, scale, rot)
NID, VTR = [0], [1]
R = random.Random(23)


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def lt(li):
    return L[li]["start"]


def scenes():
    out = [(0.0, lt(0) - .06, -1)]
    for li in range(len(L)):
        a = lt(li) - .06
        b = (lt(li + 1) - .06) if li + 1 < len(L) else DUR
        out.append((a, b, li))
    return out


def groups_of(li):
    """Labels of one or two words (keywords on their own, cuss words as ****); one- and two-letter words ride along."""
    ws = []
    for w, s, e in L[li]["words"]:
        core = re.sub(r"[^a-z0-9]", "", w.lower())
        txt = "****" if core in CURSE else w.rstrip(",.")
        ws.append((txt.upper(), core in KEY.get(li, ()), s))
    j = 0                                   # natural phrases stay together on one label
    while j < len(ws) - 1:
        pair = (ws[j][0].lower().strip("'"), ws[j + 1][0].lower().strip("'"))
        if pair in PHRASES:
            ws[j:j + 2] = [(ws[j][0] + " " + ws[j + 1][0], ws[j][1] or ws[j + 1][1], ws[j][2])]
        j += 1
    groups, cur = [], []
    for w in ws:
        if w[1]:
            if cur:
                groups.append(cur)
                cur = []
            groups.append([w])
        else:
            cur.append(w)
            if len(cur) == 2 or sum(len(x[0]) for x in cur) > 10 or " " in w[0]:
                groups.append(cur)
                cur = []
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        txt = " ".join(x[0] for x in g)
        if out and len(txt) <= 2 and not g[0][1]:
            out[-1] = (out[-1][0] + " " + txt, out[-1][1], out[-1][2])
            continue
        out.append((txt, g[0][1], g[0][2]))
    return out


def tw(text, size):
    return ANTON.getlength(text) * size / 100


def fit(text, maxw, size):
    return min(size, maxw / (tw(text, 100) / 100 + .56))


def star_path(n=7, r1=48, r2=22, seed=0):
    g = random.Random(seed)
    pts = []
    for k in range(n * 2):
        r = r1 * g.uniform(.9, 1) if k % 2 == 0 else r2
        a = k / (n * 2) * math.pi * 2 - math.pi / 2
        pts.append(f"{math.cos(a) * r:.1f} {math.sin(a) * r:.1f}")
    return "M" + " L".join(pts) + " Z"


CIRC = ('<svg class="circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path pathLength="400" '
        'd="M50 7 C93 3 106 88 50 94 S-8 14 62 8"/></svg>')


# ------------------------------------------------------------------------------------------------ elements
def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {t0:.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')


def scrap(kind, k, x, y, w, rot, t0, t1, z=1):
    kind = {"red": "mag", "grey": "maroon"}.get(kind, kind)
    i = nid("sc")
    PAN.append(f'<img class="el" id="{i}" src="assets/img/collage/scrap/{kind}-{k}.png" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;'
               f'transform:rotate({rot:.1f}deg);z-index:{z}" alt="">')
    show(f"#{i}", t0, t1)
    return i


def printel(src, x, y, w, h, rot, t0, t1, red=False, z=2):
    """A photo print with an off-white border; a video when src is an animated clip (it plays from t0)."""
    if not src or t1 - t0 < .15:
        return
    i = nid("pr")
    if src.endswith(".mp4"):
        n = float(os.popen(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{os.path.join(ROOT, src)}"').read() or 0)
        VTR[0] += 1
        media = (f'<video id="v{i}" class="clip" src="{src}" data-start="{t0:.3f}" data-duration="{min(n, t1 - t0):.3f}" '
                 f'data-track-index="{VTR[0]}" muted playsinline></video>')
    else:
        media = f'<img src="{src}" alt="">'
    PAN.append(f'<div class="print el" id="{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;'
               f'transform:rotate({rot:.1f}deg);z-index:{z}">{media}<i style="opacity:{.85 if red else 0}"></i></div>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i}", {{x: {R.choice([-120, 120])}}}, {{x: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')


def cutout(li, x, y, w, rot, t0, t1, rise=0, z=3):
    """The line's cut-out sticker in a slot w wide (at most 1.15 w tall); a picture print where the line has none."""
    if li in CUTPRINT:
        src = CUTPRINT[li]
        if src:
            printel(src, x + w * .08, y, w * .84, w * .84, rot, t0, t1, z=z)
        return
    name = CUTOUT.get(li)
    if not name:
        return
    p = os.path.join(ROOT, "assets", "img", "collage", "sticker", f"{name}.png")
    iw, ih = Image.open(p).size
    fw = min(w, w * 1.15 * iw / ih)
    x, w = x + (w - fw) / 2, fw
    i = nid("ct")
    PAN.append(f'<img class="el" id="{i}" src="assets/img/collage/sticker/{name}.png" style="left:{x:.0f}px;top:{y:.0f}px;'
               f'width:{w:.0f}px;transform:rotate({rot:.1f}deg);z-index:{z}" alt="">')
    show(f"#{i}", t0, t1)
    if rise:
        js(f'tl.fromTo("#{i}", {{y: {rise}}}, {{y: 0, duration: .4, ease: "steps(6)", immediateRender: false}}, {t0:.3f});')


def g3el(li, t0, t1):
    """The line's 3D element (transparent WebM), on the board with the rest."""
    if li not in G3D_AT:
        return
    kind, x, y, w = G3D_AT[li]
    i = nid("g3")
    ts = G3T[kind]
    VTR[0] += 1
    PAN.append(f'<div class="el g3b" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px;z-index:4">'
               f'<video id="v{i}" class="clip" src="assets/video/g3d/g3{kind}.webm" data-start="{ts:.3f}" data-duration="{max(.2, t1 - ts):.3f}" '
               f'data-track-index="{VTR[0]}" muted playsinline></video></div>')
    show(f"#{i}", max(t0, ts), t1)


def star(x, y, size, t0, t1, color=WHT, n=7, seed=0):
    i = nid("st")
    PAN.append(f'<svg class="el" id="{i}" viewBox="-50 -50 100 100" style="left:{x:.0f}px;top:{y:.0f}px;width:{size}px;height:{size}px;z-index:4">'
               f'<path d="{star_path(n, seed=seed)}" fill="{color}"/></svg>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i}", {{scale: 0, rotation: -40}}, {{scale: 1, rotation: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')


def label(text, style, x, y, size, rot, t, t1, mode="type", circle=False, anchor="center", z=5):
    """A label. mode: type (letter by letter behind a cursor block), slam (big, settles), pop."""
    i = nid("lb")
    size = min(size * 1.12, fit(text, 980, 999))
    w = tw(text, size) + size * .56
    left = x - w / 2 if anchor == "center" else x
    letters = "".join(f'<span class="ch{" cz" if c == "*" else ""}">{c if c != " " else "&nbsp;"}</span>' for c in text)
    cur = '<span class="cur"></span>' if mode == "type" else ""
    PAN.append(f'<div class="lw" data-layout-allow-overlap style="left:{left:.0f}px;top:{y:.0f}px;transform:rotate({rot:.1f}deg);z-index:{z}">'
               f'<div class="lb {style}" id="{i}" style="font-size:{size:.0f}px">{letters}{cur}{CIRC if circle else ""}</div></div>')
    show(f"#{i}", t, t1)
    if mode == "type":
        n = len(text)
        per = 3 if n > 8 else 2
        js(f'tl.set("#{i} .ch", {{display: "none"}}, {t - .001:.3f});')
        k = 0
        while k < n:
            js(f'tl.set("#{i} .ch:nth-child(-n+{min(n, k + per)})", {{display: "inline"}}, {t + (k // per) * STEP:.3f});')
            k += per
        done = t + (n // per + 1) * STEP
        js(f'tl.set("#{i} .cur", {{display: "none"}}, {done:.3f});')
    elif mode == "slam":
        js(f'tl.fromTo("#{i}", {{scale: 1.65}}, {{scale: 1, duration: .2, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
        done = t + .2
    else:
        js(f'tl.fromTo("#{i}", {{scale: 1.4}}, {{scale: 1, duration: .134, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
        done = t + .134
    if circle:
        js(f'tl.fromTo("#{i} .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .33, ease: "steps(5)", immediateRender: false}}, {done + .05:.3f});')
    return i, w


def ghost(text, x, y, size, t0, t1):
    i = nid("gh")
    PAN.append(f'<div class="lw" data-layout-allow-overlap style="left:{x - 700:.0f}px;top:{y:.0f}px;width:1400px;z-index:1;text-align:center"><div class="ghost" id="{i}" '
               f'style="font-size:{size}px">{text}&nbsp;{text}</div></div>')
    show(f"#{i}", t0, t1)


def para(lines, x, y, t0, t1):
    i = nid("pa")
    PAN.append(f'<div class="para el" id="{i}" style="left:{x}px;top:{y:.0f}px">{"<br>".join(lines)}</div>')
    show(f"#{i}", t0, t1)


def rect_outline(x, y, w, h, t0, t1):
    i = nid("ro")
    PAN.append(f'<i class="el rline" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>')
    show(f"#{i}", t0, t1)


def arc(x, y, size, t0, t1):
    i = nid("ar")
    PAN.append(f'<svg class="el" id="{i}" viewBox="0 0 100 100" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:4;overflow:visible">'
               f'<path pathLength="400" d="M8 70 C4 20 60 -6 96 30" fill="none" stroke="{WHT}" stroke-width="3.2" stroke-linecap="round" '
               f'stroke-dasharray="400"/></svg>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i} path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .27, ease: "steps(4)", immediateRender: false}}, {t0:.3f});')


def block(x, y, w, h, t0, t1, cls="magblk"):
    i = nid("bk")
    PAN.append(f'<i class="el {cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>')
    show(f"#{i}", t0, t1)


def flame(x, y, t0, t1):
    i = nid("fl")
    PAN.append(f'<svg class="el" id="{i}" viewBox="0 0 100 120" style="left:{x}px;top:{y}px;width:150px;height:180px;z-index:4">'
               '<path d="M50 4 C62 30 88 42 80 78 C76 100 60 114 46 114 C26 112 12 96 16 74 C20 56 34 52 34 36 C44 46 46 56 46 64 '
               f'C56 52 58 30 50 4 Z M40 112 C30 96 38 84 48 72 C50 86 62 92 56 112" fill="{MAG}" stroke="{WHT}" stroke-width="5" '
               'stroke-linejoin="round"/></svg>')
    show(f"#{i}", t0, t1)


def cam(si, t, fx, fy, s=1.0, rot=0.0, dur=.35):
    CAMKEYS.setdefault(si, []).append((t, fx, fy, s, rot, dur * .6))


# ------------------------------------------------------------------------------------------------ recipes (Ashke)
def r1(si, a, b, li, gs):
    scrap("red", 0, 30, 230, 1020, -7, a, b)
    scrap("black", 3, 600, 40, 560, 14, a, b)
    cutout(li, 120, 150, 840, -2, a, b, rise=320)
    g3el(li, a, b)
    cam(si, a, 540, 700, 1.08, -2, .01)
    y = 1000
    for k, (txt, key, t) in enumerate(gs):
        if k == 0:
            size = fit(txt, 900, 160)
            label(txt, "blk", 540, y, size, -2, t, b, mode="slam")
            y += size * 1.12 + 26
            cam(si, t, 540, 900, 1.0, -1, .3)
        else:
            size = fit(txt, 760, 118)
            label(txt, "magw", 560, y, size, -1.5, t, b, mode="type", circle=key)
            y += size * 1.12 + 22
            cam(si, t, 540, 960 + (y - 1200) * .3, 1.02, 0, .4)
    if li < 0:
        para(["SPIN BOUT U · DRAKE & 21 SAVAGE"], 110, y + 30, gs[min(1, len(gs) - 1)][2], b)
    printel(CARD2.get(li), 620, 1380, 380, 450, 7, a + PERIOD * .5, b)
    star(60, max(1530, y + 190), 230, a + PERIOD, b, seed=si)
    star(290, max(1700, y + 330), 110, a + PERIOD * 1.5, b, color=MAG, seed=si + 1)
    if b - a > 1.4:
        FLASH.append((a + PERIOD * 2, "invert"))


def r2(si, a, b, li, gs):
    kw = next((g for g in reversed(gs) if g[1]), gs[-1])
    ki = gs.index(kw)
    if kw[2] - .067 > a + .1:
        printel(CARD1.get(li), 60, 580, 960, 1060, 2, a, kw[2] - .067)
    scrap("black", 1, -80, 1500, 900, -4, a, b)
    cam(si, a, 540, 860, 1.12, 1.5, .01)
    y = 520
    for k, (txt, key, t) in enumerate(gs[:ki]):
        size = fit(txt, 820, 120)
        label(txt, "blk", 540 - 60 * k, y, size, -2, t, b)
        y += size * 1.15 + 18
        cam(si, t, 540, 760 + 60 * k, 1.1, 1, .3)
    FLASH.append((kw[2] - .067, "white"))
    scrap("black", 3, -60, 760, 1200, -5, kw[2], b)
    size = fit(kw[0], 1060, 330)
    after_n = len(gs) - ki - 1
    if li == 6:
        td = next(g[2] for g in gs if g[0].startswith("DUMB"))
        cutout(li, 600, 1080, 460, 6, td, b, z=8)
        cam(si, td, 640, 1120, 1.05, 2, .25)
    else:
        cutout(li, 540 - 220, 860 + size * 1.25 + 150 * after_n, 440, 2, kw[2], b, z=2)
    _, fw = label(kw[0], f"fill f{li}", 540, 860, size, -3, kw[2], b, mode="pop", z=6)
    cam(si, kw[2], 540, 960, 1.0, 0, .2)
    zt = kw[2] + .4
    after = gs[ki + 1:]
    back = min(b - .1, (after[0][2] - .05) if after else kw[2] + 1.0, zt + .55)
    if back - zt > .2:
        cam(si, zt, 540 + fw * .22, 860 + size * .5, 2.6, -2, .27)
        cam(si, back, 540, 1000, 1.0, 0, .27)
    y = 860 + size + 20
    for txt, key, t in after:
        sz = fit(txt, 820, 120)
        label(txt, "wht", 560, y, sz, 2, t, b)
        y += sz * 1.15 + 18
        cam(si, max(t, back + .05), 540, 1080, 1.0, 0, .35)


def r3(si, a, b, li, gs):
    kw = next((g for g in gs if g[1]), gs[-1])
    scrap("grey", 0, -80, 880, 1240, 3, a, b)
    scrap("black", 2, 720, 120, 420, -10, a, b)
    g0 = gs[0]
    size = fit(g0[0], 860, 140)
    label(g0[0], "mb", 520, 520, size, -2, g0[2], b)
    cam(si, a, 540, 560, 1.45, -2, .01)
    rest = [g for g in gs[1:] if g is not kw]
    t_pull = rest[0][2] if rest else (kw[2] if kw is not g0 else a + .6)
    block(170, 960, 740, 560, t_pull, b)
    printel(CARD2.get(li), 700, 70, 340, 400, 8, t_pull, b)
    cutout(li, 150, 640, 780, 1, t_pull, b)
    g3el(li, t_pull, b)
    cam(si, t_pull, 540, 1000, 1.0, 0, .4)
    for k, (txt, key, t) in enumerate(rest):
        label(txt, "blk", 300 + 60 * k, 700 + 130 * k, fit(txt, 600, 100), -4, t, b)
    if kw is not g0:
        scrap("white", 1, 140, 1320, 800, -3, kw[2], b, z=4)
        label(kw[0], "m3d", 540, 1390, fit(kw[0], 760, 200), -3, kw[2], b, z=6)
        ghost(kw[0], 540, 1640, 250, kw[2], b)
        cam(si, kw[2], 540, 1090, 1.03, 0, .35)


def r4(si, a, b, li, gs):
    kw = next((g for g in gs if g[1]), gs[-1])
    g0 = gs[0]
    FLASH.append((a, "invert"))
    label(g0[0], "stamp", 540, 260, fit(g0[0], 1000, 300), 0, g0[2], b, z=4)
    if li != 14:
        rect_outline(200, 560, 680, 560, a + .134, b)
    scrap("red", 1, 560, 760, 520, 6, a + .134, b)
    cam(si, a, 540, 430, 1.3, 0, .01)
    mids = [g for g in gs[1:] if g is not kw]
    t_cut = min(mids[0][2] if mids else (kw[2] if kw is not g0 else a + .5), a + .45)
    cutout(li, 150, 480, 780, -1, t_cut, b)
    g3el(li, a + .134, b)
    if li == 3:
        printel(CARD2[li], 20, 420, 300, 650, -8, t_cut + PERIOD / 2, b, z=4)
    else:
        printel(CARD2.get(li), 30, 560, 300, 360, -8, t_cut + PERIOD / 2, b)
    cam(si, t_cut, 540, 820, 1.18, 0, .35)
    for k, (txt, key, t) in enumerate(mids):
        label(txt, "blk", 780, 1180 + 120 * k, fit(txt, 520, 96), 4, t, b, z=6)
    if kw is not g0:
        scrap("black", 0, -90, 1300, 1260, -3, kw[2] - .067, b, z=4)
        label(kw[0], "w3d", 540, 1420, fit(kw[0], 820, 220), -2, kw[2], b, z=6)
        cam(si, kw[2], 540, 1250, 1.15, 0, .3)
        if b - kw[2] > .7:
            cam(si, kw[2] + .45, 540, 960, .92, 0, .4)


def r5(si, a, b, li, gs):
    g0 = gs[0]
    scrap("red", 2, 20, 600, 700, -9, a, b)
    printel(CARD1.get(li), 120, 520, 640, 760, -5, a, b)
    g3el(li, a, b)
    cam(si, a, 520, 860, 1.05, -1, .01)
    label(g0[0], "stamp", 540, 260, fit(g0[0], 1000, 270), -1, g0[2], b, z=4)
    cam(si, g0[2], 540, 620, 1.0, 0, .3)
    rest = gs[1:]
    y = 1320
    for k, (txt, key, t) in enumerate(rest):
        if k == 0:
            FLASH.append((t, "invert"))
        sz = fit(txt, 760, 118)
        label(txt, "blk" if (key or k % 2 == 0) else "wht", 430 + (k % 2) * 120, y, sz, -3 + 5 * (k % 2), t, b, circle=key, z=6)
        y += sz * 1.15 + 22
        cam(si, t, 520, min(1250, 1000 + 70 * k), 1.0, 0, .35)
    tc = rest[len(rest) // 2][2] if rest else a + .8
    if li in CARD2 and li not in (12,):
        printel(CARD2[li], 500, 700, 560, 700, 6, tc, b, red=True)
        cam(si, tc + .1, 640, 1100, 1.0, 1, .4)


def r6(si, a, b, li, gs):
    kw = gs[-1]
    printel(CARD1.get(li), 400, 170, 660, 760, 9, a, b)
    scrap("black", 1, -120, 820, 700, -6, a, b)
    arc(60, 160, 360, a + .2, b)
    cam(si, a, 640, 860, 1.0, 1, .01)
    rest = [g for g in gs if g is not kw]
    y = 1040
    for k, (txt, key, t) in enumerate(rest):
        sz = fit(txt, 760, 150)
        label(txt, "wht" if k == 0 else "blk", 400 + 120 * (k % 2), y, sz, -3 + 4 * k, t, b, circle=key, z=6)
        y += sz * 1.15 + 20
        cam(si, t, 480, 1000 + 40 * k, 1.0, 0, .35)
    label(kw[0], "mlet", 560, y + 20, fit(kw[0], 900, 240), -6, kw[2], b, circle=kw[1], z=6)
    star(720, y + 240, 90, kw[2] + .2, b, color=MAG, n=6, seed=si)
    star(830, y + 300, 60, kw[2] + .27, b, color=WHT, n=6, seed=si + 5)
    cam(si, kw[2], 540, min(1250, y + 60), 1.08, -1, .35)


def r7(si, a, b, li, gs):
    kw = gs[-1]
    rest = gs[:-1]
    scrap("black", 2, 260, 110, 480, 8, a, b)
    cam(si, a, 540, 760, 1.0, 0, .01)
    y = 330
    for k, (txt, key, t) in enumerate(rest):
        sz = fit(txt, 760, 112 if k == 0 else 108)
        label(txt, "mtyp" if k == 0 else "blk", 560 + (40, -40)[k % 2], y, sz, (-6, 3)[k % 2], t, b, z=6)
        cam(si, t, 560, y + 260, 1.1, -1, .3)
        y += sz * 1.3 + 24
    ksz = fit(kw[0], 900, 180)
    label(kw[0], "wht", 540, y + 10, ksz, -2, kw[2], b, circle=kw[1], z=6)
    cam(si, kw[2], 540, y + 300, 1.04, 0, .35)
    printel(CARD1.get(li), 140, y + ksz * 1.35 + 40, 760, 660, -3, a, b)


def r8(si, a, b, li, gs):
    kw = next((g for g in reversed(gs) if g[1]), gs[-1])
    g0 = gs[0]
    FLASH.append((a, "invert"))
    t2 = gs[1][2] if len(gs) > 1 else a + .9
    scrap("red", 0, -60, 1080, 960, -8, a, t2)
    scrap("black", 2, -160, 720, 420, 4, a, t2)
    cutout(li, 90, 260, 900, 0, a, t2)
    flame(800, 1260, a + .2, t2)
    label(g0[0], "magw", 540, 1270, fit(g0[0], 900, 150), -2, g0[2], t2, z=6)
    cam(si, a, 540, 960, 1.0, 0, .01)
    cam(si, g0[2], 540, 1060, 1.05, 0, .3)
    scrap("red", 3, -40, 1180, 1000, -6, t2, b)
    cutout(li, 280, 640, 540, 0, t2, b)
    g3el(li, t2, b)
    printel(CARD2.get(li), 660, 1060, 360, 430, 8, t2 + .1, b)
    flame(760, 1380, t2, b)
    label(g0[0], "magw", 540, 220, fit(g0[0], 800, 120), -4, t2, b, mode="pop", z=6)
    for k, (txt, key, t) in enumerate(g for g in gs[1:] if g is not kw):
        label(txt, "blkm", 540, 420 + 150 * k, fit(txt, 900, 130), -2, t, b, z=6)
    if kw is not g0:
        label(kw[0], "stamp", 540, 1420, fit(kw[0], 1000, 250), -3, kw[2], b, z=5)
    cam(si, t2, 540, 880, 1.0, 0, .01)
    cam(si, t2 + .3, 540, 920, 1.04, 0, .5)


def r9(si, a, b, li, gs):
    FLASH.append((a, "split"))
    printel(CARD2.get(li), 600, 60, 440, 550, 7, a + .067, b)
    scrap("grey", 3, -160, -90, 1000, 5, a, b)
    scrap("grey", 1, 420, 1560, 860, -7, a, b)
    scrap("black", 2, -120, 880, 760, 3, a, b)            # dark under the stamp: the stamp is off-white here
    kw = next((g for g in reversed(gs) if g[1]), gs[-1]) if gs else None
    rest = [g for g in gs if g is not kw]
    styles = ["magw", "mag", "w3d", "blk"]
    y = 560 if len(rest) > 2 else 700
    cam(si, a, 470, y + 120, 1.15, -1, .01)
    for k, (txt, key, t) in enumerate(rest):
        x = 540 + (-80, 80)[k % 2]
        sz = fit(txt, 820, (170, 140, 190, 130)[k % 4])
        label(txt, styles[k % 4], x, y, sz, (-2, 3, -2, -3)[k % 4], t, b, z=6)
        cam(si, t, (x + 540) / 2, y + sz * .6, 1.12, (-2, 3, -2, -3)[k % 4] * .3, .3)
        y += sz * 1.3 + 34
    if kw:
        sz = fit(kw[0], 1000, 290)
        label(kw[0], "stamp", 540, y + 10, sz, -2, kw[2], b, circle=kw[1], z=5)
        cam(si, kw[2], 540, y + sz * .6, 1.0, 0, .4)
    if li in CUTOUT:
        cutout(li, 600, 40, 440, 6, a + .067, b, z=4)


ICON_AT = {"R1": (800, 1500, 8), "R2": (60, 300, -8), "R3": (790, 330, 10), "R4": (90, 1100, -10), "R5": (810, 1520, 8),
           "R6": (60, 1540, -6), "R7": (60, 300, -8), "R8": (90, 960, -10), "R9": (780, 1460, 10)}


def lyric_icons():
    for si, (a, b, li) in enumerate(scenes()):
        gs = groups_of(li) if li >= 0 else [("", True, a + 1.2)]
        kws = [g for g in gs if g[1]]
        t = (kws[-1] if kws else gs[len(gs) // 2])[2]
        rec = RECIPE[li]
        if rec == "R8" and len(gs) > 1:
            t = max(t, gs[1][2])
        if t >= b - .15:
            t = max(a + .2, b - .5)
        x, y, rot = ICON_AT[rec]
        i = nid("ic")
        PAN.append(f'<div class="el" id="{i}" style="left:{x}px;top:{y}px;width:230px;height:230px;z-index:7;transform:rotate({rot}deg)">'
                   f'{svg(ICON[li])}<b class="itag">{WORD[li]}</b></div>')
        show(f"#{i}", t, b)
        js(f'tl.fromTo("#{i}", {{scale: 1.6, rotation: {rot - 20}}}, {{scale: 1, rotation: {rot}, duration: .2, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
        k, tt = 0, t + .27
        while tt < b - .07:
            js(f'tl.set("#{i}", {{rotation: {rot + (2.5 if k % 2 else -2.5)}}}, {tt:.3f});')
            tt, k = tt + PERIOD / 2, k + 1


def transition_frames():
    """Three single-frame stills (one 30 fps frame each) right before most cuts: the Ashke transitions' frame pacing."""
    k = 0
    for si, (a, b, li) in enumerate(scenes()):
        if si == 0 or RECIPE[li] in ("R4", "R8", "R9"):
            continue
        for j in range(3):
            src = STILLS[k % len(STILLS)]
            k += 1
            i = nid("tf")
            rot = (-4, 5, -2)[j]
            w = (820, 700, 900)[j] * .82
            SCREEN.append(f'<div class="tframe" id="{i}" style="left:{540 - w / 2:.0f}px;top:{CY - w * 1.25 / 2:.0f}px;width:{w:.0f}px;height:{w * 1.25:.0f}px;'
                          f'transform:rotate({rot}deg)"><img src="{src}" alt=""></div>')
            t0 = a - (3 - j) / 30
            show(f"#{i}", t0, t0 + 1 / 30)


# ------------------------------------------------------------------------------------------------ camera (Ashke)
DIRS = [(0, 1), (0, 1), (1, .3), (0, 1), (-.8, .6), (0, -1), (.7, .7), (0, 1), (-1, 0), (0, 1), (.6, .8), (1, 0)]


def camera():
    plans = []
    for si, (a, b, li) in enumerate(scenes()):
        keys = sorted(CAMKEYS.get(si, [(a, 540, 960, 1.0, 0, .01)]))
        d = DIRS[si % len(DIRS)]
        n = math.hypot(*d)
        d = (d[0] / n, d[1] / n)
        pts = [(a, keys[0][1], keys[0][2], keys[0][3], keys[0][4])]
        for (tk, kx, ky, ks, kr, kd) in keys[1:]:
            tt = min(max(tk + .12, pts[-1][0] + .1), b - .05)
            if tt > pts[-1][0] + .05:
                pts.append((tt, kx, ky, ks, kr))
        lx, ly, ls, lr = pts[-1][1:]
        run = min(440, 520 * (b - pts[-1][0]))
        pts.append((b + .001, lx + d[0] * run, ly + d[1] * run, ls, lr))
        plans.append(dict(a=a, b=b, li=li, d=d, pts=pts))
    tend = DUR - .5
    E, X, TAU = 560, 480, .075

    def herm(pts, t, idx):
        T = [p[0] for p in pts]
        k = max(0, min(len(pts) - 2, max(i for i in range(len(pts)) if T[i] <= t + 1e-9)))
        t0, t1 = T[k], T[k + 1]
        u = max(0, min(1, (t - t0) / max(1e-6, t1 - t0)))

        def tan(m):
            lo, hi = max(0, m - 1), min(len(pts) - 1, m + 1)
            return (pts[hi][idx] - pts[lo][idx]) / max(1e-6, T[hi] - T[lo])
        p0, p1 = pts[k][idx], pts[k + 1][idx]
        m0, m1 = tan(k) * (t1 - t0), tan(k + 1) * (t1 - t0)
        h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
        return h00 * p0 + h10 * m0 + h01 * p1 + h11 * m1

    def focus(si, t):
        p = plans[si]
        fx, fy, s, rot = (herm(p["pts"], t, i) for i in (1, 2, 3, 4))
        u = max(0, t - p["a"])
        e = math.exp(-u / TAU)
        fx -= p["d"][0] * E * e
        fy -= p["d"][1] * E * e
        rot += 3 * e * (1 if si % 2 else -1)
        if si + 1 < len(plans):
            nd = plans[si + 1]["d"]
            x = math.exp(-max(0, p["b"] - t) / TAU)
            fx += nd[0] * X * x
            fy += nd[1] * X * x
            rot += 2 * x * (1 if si % 2 else -1)
        return fx, fy, s, rot

    td = next(s_ for w, s_ in words_of(12) if w == "dropped")       # dropped: the frame falls out and slams back in
    DROP = {round(td * 15) + k: y for k, y in enumerate([420, 1000, -760, -200, 50, -28, 12])}
    blurred = False
    for f in range(int(DUR * 15)):
        t = f / 15
        si = max(i for i, p in enumerate(plans) if p["a"] <= t + 1e-6)
        fx, fy, s, rot = focus(si, t)
        px, py, _, _ = focus(si, max(plans[si]["a"], t - STEP)) if t - STEP >= plans[si]["a"] else focus(si, t + STEP)
        vx, vy = (fx - px) * s, (fy - py) * s
        if t - STEP < plans[si]["a"]:
            vx, vy = -vx, -vy
        lb = max([bt for bt in BEATS["beats"] if bt <= t + 1e-6] or [-9])
        s *= 1 + .05 * math.exp(-(t - lb) / .09)
        s *= 1 + .22 * math.exp(-(t - plans[si]["a"]) / .07)          # zoom snap into every scene
        fy = 960 + (fy - 960) * VTRACK
        dy = DROP.get(f, 0)
        if dy:
            fy -= dy / (s * 1.06 * ZOOM)
        CAMSTATE[f] = (fx, fy, s * 1.06 * ZOOM, rot)
        js(f'tl.set("#pan", {{x: {540 - fx:.1f}, y: {CY - fy:.1f}}}, {t:.3f});')
        js(f'tl.set("#cam", {{scale: {s * 1.06 * ZOOM:.4f}, rotation: {rot:.2f}}}, {t:.3f});')
        sp = math.hypot(vx, vy)
        if sp > 90:
            k = min(13, sp * .045)
            js(f'tl.set("#mbg", {{attr: {{stdDeviation: "{abs(vx) / sp * k:.1f} {abs(vy) / sp * k:.1f}"}}}}, {t:.3f});')
            if not blurred:
                js(f'tl.set("#cam", {{filter: "url(#mb)"}}, {t:.3f});')
                blurred = True
        elif blurred:
            js(f'tl.set("#cam", {{filter: "none"}}, {t:.3f});')
            blurred = False


# ------------------------------------------------------------------------------------------------ lyric concepts
def conc(html, t0, t1, z=5):
    i = nid("cc")
    PAN.append(html.replace("ID", i).replace("ZZ", str(z)))
    show(f"#{i}", t0, t1)
    return i


def words_of(li):
    return [(w.lower().strip(",.'"), s) for w, s, e in L[li]["words"]]


def concepts():
    """Motion-graphics concepts drawn from what each line says, where the removed anime pictures were."""
    sc = {li: (a, b) for a, b, li in scenes()}
    # ten toes: footsteps march up the page one per beat, a 10 counter ticks with them and slams
    a, b = sc[7]
    steps = [t for t in BEATS["beats"] if a + .05 < t < b - .1][:10]
    for k, t in enumerate(steps):
        x, y = (330 if k % 2 == 0 else 520), 820 - k * 62
        i = conc(f'<svg class="el" id="ID" viewBox="0 0 120 120" style="left:{x}px;top:{y}px;width:170px;height:170px;z-index:ZZ;'
                 f'transform:rotate({-12 if k % 2 == 0 else 12}deg)">' + svg_foot(k % 2) + '</svg>', t, b)
        js(f'tl.fromTo("#{i}", {{scale: 1.8}}, {{scale: 1, duration: .134, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
    cnt = conc(f'<div class="el counter" id="ID" style="left:700px;top:260px;z-index:ZZ">1</div>', steps[0] if steps else a, b, z=6)
    for k, t in enumerate(steps):
        js(f'tl.set("#{cnt}", {{textContent: "{k + 1}"}}, {t:.3f});')
        js(f'tl.fromTo("#{cnt}", {{scale: 1.5}}, {{scale: 1, duration: .134, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
    # wherever I say go: a GPS route draws across, pins drop on each "go", a compass needle snaps round
    a, b = sc[8]
    gos = [s_ for w, s_ in words_of(8) if w == "go"]
    route = "M120 1500 C 160 1420, 190 1360, 250 1330 S 600 1250, 700 1170 S 860 1080, 900 1060"
    rt = conc(f'<svg class="el" id="ID" viewBox="0 0 1080 1920" style="left:0;top:0;width:1080px;height:1920px;z-index:ZZ;overflow:visible">'
              f'<path d="{route}" pathLength="1000" fill="none" stroke="{WHT}" stroke-width="16" stroke-dasharray="1000" stroke-linecap="round"/>'
              f'<path d="{route}" pathLength="1000" fill="none" stroke="{MAG}" stroke-width="8" stroke-dasharray="14 18" stroke-linecap="round"/></svg>', a, b, z=4)
    js(f'tl.fromTo("#{rt} path", {{strokeDashoffset: 1000}}, {{strokeDashoffset: 0, duration: {max(.4, gos[-1] - a):.2f}, ease: "steps({max(4, round((gos[-1] - a) * 15))})", immediateRender: false}}, {a:.3f});')
    for k, (t, (px, py)) in enumerate(zip([a + .2] + gos, [(120, 1500), (250, 1330), (900, 1060)])):
        i = conc(f'<svg class="el" id="ID" viewBox="0 0 100 130" style="left:{px - 60}px;top:{py - 150}px;width:120px;height:156px;z-index:ZZ">'
                 f'<path d="M50 125 C20 80 6 62 6 44 A44 44 0 1 1 94 44 C94 62 80 80 50 125 Z" fill="{MAG}" stroke="{WHT}" stroke-width="8"/>'
                 f'<circle cx="50" cy="44" r="16" fill="{WHT}"/></svg>', t, b, z=6)
        js(f'tl.fromTo("#{i}", {{y: -260, scale: 1.3}}, {{y: 0, scale: 1, duration: .2, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
    cp = conc(f'<svg class="el" id="ID" viewBox="-110 -110 220 220" style="left:600px;top:1180px;width:400px;height:400px;z-index:ZZ">'
              f'<circle r="100" fill="{INK}" stroke="{WHT}" stroke-width="8"/>'
              + "".join(f'<text x="{78 * math.sin(k * math.pi / 2):.0f}" y="{-78 * math.cos(k * math.pi / 2) + 9:.0f}" fill="{WHT}" font-family="Anton" font-size="28" text-anchor="middle">{d}</text>'
                        for k, d in enumerate("NESW")) +
              f'<g class="ndl"><path d="M0 -70 L14 0 L0 12 L-14 0 Z" fill="{MAG}"/><path d="M0 70 L14 0 L0 -12 L-14 0 Z" fill="{WHT}"/></g></svg>', a, b, z=5)
    ang = 0
    for k, t in enumerate([a] + gos + [b - .3]):
        ang += 160 + 70 * k
        js(f'tl.to("#{cp} .ndl", {{rotation: {ang}, svgOrigin: "0 0", duration: .2, ease: "back.out(3)"}}, {t:.3f});')
    # dropped: impact shockwaves under the 3D diamonds
    a, b = sc[12]
    td = next(s_ for w, s_ in words_of(12) if w == "dropped")
    for k in range(3):
        i = conc(f'<i class="el shock" id="ID" style="left:240px;top:1080px;width:600px;height:200px;z-index:ZZ"></i>', td + k * .12, td + .9 + k * .12, z=3)
        js(f'tl.fromTo("#{i}", {{scale: .2, opacity: 1}}, {{scale: 2.2, opacity: 0, duration: .8, ease: "steps(12)", immediateRender: false}}, {td + k * .12:.3f});')
    # hook 2: rings pulse out of the chrome heart on every other beat
    a, b = sc[15]
    for k, t in enumerate([t for t in BEATS["beats"][::2] if a < t < b - .2]):
        i = conc(f'<i class="el ring" id="ID" style="left:340px;top:670px;width:400px;height:400px;z-index:ZZ"></i>', t, t + .6, z=3)
        js(f'tl.fromTo("#{i}", {{scale: .5, opacity: 1}}, {{scale: 2.4, opacity: 0, duration: .6, ease: "steps(9)", immediateRender: false}}, {t:.3f});')
    # comin' out my body: glowing wisps rising out of the 3D BODY
    a, b = sc[16]
    g = random.Random(16)
    for k in range(14):
        x = g.uniform(160, 920)
        i = conc(f'<i class="el wisp" id="ID" style="left:{x:.0f}px;top:1300px;width:{g.uniform(30, 70):.0f}px;height:{g.uniform(120, 260):.0f}px;z-index:ZZ"></i>', a, b, z=5)
        per = g.uniform(1.2, 2.0)
        st = a - g.uniform(0, per)
        while st < b:
            nn = max(2, round(per * 15))
            js(f'tl.fromTo("#{i}", {{y: 0, opacity: .9, scaleY: .6}}, {{y: -900, opacity: 0, scaleY: 1.4, duration: {per:.2f}, ease: "steps({nn})", immediateRender: false}}, {max(a, st):.3f});')
            st += per


def svg_foot(right):
    s_ = -1 if right else 1
    return (f'<g transform="translate(60 60) scale({s_} 1) translate(-60 -60)">'
            f'<path d="M48 42 C30 50 32 96 50 106 C68 114 80 96 76 72 C74 56 64 38 48 42 Z" fill="{WHT}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="62" cy="14" r="9" fill="{MAG}" stroke="{INK}" stroke-width="4"/><circle cx="78" cy="22" r="7" fill="{MAG}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="88" cy="35" r="6" fill="{MAG}" stroke="{INK}" stroke-width="4"/><circle cx="44" cy="20" r="8" fill="{MAG}" stroke="{INK}" stroke-width="4"/></g>')


def finishing():
    """The After Effects pass on the cuts: a bloom burst on some cuts (random), a light leak sweep on others, a colour
    split on every whip."""
    g = random.Random(31)
    for si, (a, b, li) in enumerate(scenes()):
        if si == 0:
            continue
        r = g.random()
        fil = []
        for k in range(4):
            parts = []
            if r < .6:
                parts.append("url(#bloom)")
            if k < 2:
                parts.append("url(#rgbsplit)")
            fil.append(" ".join(parts) or "none")
        for k in range(4):
            t = a - STEP + k * STEP
            js(f'tl.set("#glow", {{filter: "{fil[k]}"}}, {t:.3f});')
            js(f'tl.set("#blg", {{attr: {{stdDeviation: {[26, 20, 13, 7][k]}}}}}, {t:.3f});')
            js(f'tl.set("#rgbR", {{attr: {{dx: {[30, 16, 0, 0][k]}}}}}, {t:.3f});')
            js(f'tl.set("#rgbB", {{attr: {{dx: {[-30, -16, 0, 0][k]}}}}}, {t:.3f});')
        js(f'tl.set("#glow", {{filter: "none"}}, {a + 3 * STEP:.3f});')
        if r >= .45:
            js(f'tl.set("#leak", {{opacity: 1}}, {a - STEP:.3f});')
            js(f'tl.fromTo("#leak", {{x: {-900 if si % 2 else 900}, opacity: 1}}, {{x: {900 if si % 2 else -900}, opacity: 0, duration: .5, ease: "steps(8)", immediateRender: false}}, {a - STEP:.3f});')
        if b - a > 2.6:                       # a smaller bloom pulse mid-scene on a strong beat
            mb = [t for t in BEATS["beats"][::4] if a + 1 < t < b - .6]
            if mb:
                t = mb[0]
                js(f'tl.set("#glow", {{filter: "url(#bloom)"}}, {t:.3f});')
                js(f'tl.set("#blg", {{attr: {{stdDeviation: 16}}}}, {t:.3f});')
                js(f'tl.set("#glow", {{filter: "none"}}, {t + 2 * STEP:.3f});')


# ------------------------------------------------------------------------------------------------ full-screen lyric effects
def locked(inner, t0, t1, z=5):
    """A full-screen layer pinned to the screen but living in the board under the lyric labels, so the words stay
    readable while the whole picture burns / fills with smoke. pin_locks() counter-moves it against the camera."""
    i = nid("lk")
    PAN.insert(0, f'<div class="el lock" id="{i}" style="z-index:{z}">{inner}</div>')
    show(f"#{i}", t0, t1)
    LOCKS.append((i, t0, t1))
    return i


def pin_locks():
    for i, t0, t1 in LOCKS:
        for f in range(int(t0 * 15) - 1, int(t1 * 15) + 2):
            if f in CAMSTATE:
                fx, fy, S, rot = CAMSTATE[f]
                js(f'tl.set("#{i}", {{x: {fx - 540:.1f}, y: {fy - CY:.1f}, scale: {1 / S:.4f}, rotation: {-rot:.2f}}}, {f / 15:.3f});')


def front_layer(gid, fil, t0, t1, y_from, y_to, t_full, L, drift, z=5, extra=""):
    """A procedural noise front sweeping up the screen (filter fil maps the swept value to colour)."""
    svg = (f'<svg viewBox="-80 -80 1240 1240" style="position:absolute;left:-80px;top:-80px;width:1240px;height:1240px;overflow:visible">'
           f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{y_from - L / 2:.0f}" x2="0" y2="{y_from + L / 2:.0f}">'
           f'<stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient></defs>'
           f'<rect x="-80" y="-80" width="1240" height="1240" fill="url(#{gid})" filter="url(#{fil})"/></svg>{extra}')
    i = locked(svg, t0, t1, z)
    n = max(1, round((t_full - t0) * 15))
    for k in range(n + 1):
        u = k / n
        yf = y_from + (y_to - y_from) * (1 - (1 - u) ** 1.35)
        js(f'tl.set("#{gid}", {{attr: {{y1: {yf - L / 2:.0f}, y2: {yf + L / 2:.0f}}}}}, {t0 + k * STEP:.3f});')
    off = {"firef": "fireo", "smk2": "smko"}[fil]
    m = max(1, round((t1 - t0) * 15))
    for k in range(m + 1):
        js(f'tl.set("#{off}", {{attr: {{dx: {drift[0] * k / m:.0f}, dy: {drift[1] * k / m:.0f}}}}}, {t0 + k * STEP:.3f});')
    return i


def context_fx():
    """The lyric lines that say something physical happen to the whole screen: smoke fills it, burn sets it on fire,
    dropped drops the frame, comin' out my body lifts a ghost of the whole picture out of itself."""
    sc = {li: (a, b) for a, b, li in scenes()}
    # smoke a top: smoke billows up from the bottom and swallows the whole frame, swirling until the cut
    a, b = sc[13]
    front_layer("smg", "smk2", a, b, 1400, -700, a + 1.3, 1100, (140, -520), z=4)
    # burn somebody block: a fire front sweeps up the whole screen and leaves it charred, embers flying
    a, b = sc[14]
    g = random.Random(14)
    em = "".join(f'<i class="ember" style="position:absolute;left:{g.uniform(0, 1080):.0f}px;top:{g.uniform(700, 1250):.0f}px;'
                 f'width:{g.uniform(7, 16):.0f}px;height:{g.uniform(7, 16):.0f}px"></i>' for _ in range(36))
    bi = front_layer("fig", "firef", a, b, 1350, -520, b - .2, 900, (0, -620), z=4, extra=f'<div class="embers">{em}</div>')
    n = max(2, round((b - a) * 15))
    js(f'tl.fromTo("#{bi} .ember", {{y: 0, x: 0}}, {{y: (k) => -700 - (k * 137) % 600, x: (k) => (k * 53) % 160 - 80, duration: {b - a:.2f}, ease: "steps({n})", '
       f'stagger: .012, immediateRender: false}}, {a:.3f});')
    SCREEN.append('<div id="heat"></div>')
    HIDE.append("#heat")
    js(f'tl.set("#heat", {{opacity: .55, background: "#ff9a50"}}, {a:.3f});')                  # the ignition flash
    js(f'tl.set("#heat", {{background: "radial-gradient(ellipse 90% 70% at 50% 100%, rgba(255,120,40,.7), rgba(255,70,40,.18) 50%, rgba(0,0,0,0) 85%)"}}, {a + STEP:.3f});')
    for k in range(1, n):
        t = a + k * STEP
        js(f'tl.set("#heat", {{opacity: {.18 + .22 * abs(math.sin(k * 2.3)) * abs(math.sin(k * .7 + 1)):.2f}}}, {t:.3f});')
    for tw in [s_ for w, s_ in words_of(14) if w in ("burn", "block")]:   # bloom hits, not a constant wash
        for k, sd in enumerate([18, 11]):
            js(f'tl.set("#glow", {{filter: "url(#bloom)"}}, {tw + k * STEP + .002:.3f});')
            js(f'tl.set("#blg", {{attr: {{stdDeviation: {sd}}}}}, {tw + k * STEP + .002:.3f});')
        js(f'tl.set("#glow", {{filter: "none"}}, {tw + 2 * STEP + .002:.3f});')
    js(f'tl.set("#heat", {{opacity: 0}}, {b:.3f});')
    # somethin' gettin' dropped: the whole frame falls out the bottom, slams back in from the top and judders
    a, b = sc[12]
    td = next(s_ for w, s_ in words_of(12) if w == "dropped")
    for k, dx in enumerate([22, 26, 16, 8]):
        js(f'tl.set("#glow", {{filter: "url(#rgbsplit)"}}, {td + k * STEP:.3f});')
        js(f'tl.set("#rgbR", {{attr: {{dx: 0, dy: {dx}}}}}, {td + k * STEP:.3f});')
        js(f'tl.set("#rgbB", {{attr: {{dx: 0, dy: {-dx}}}}}, {td + k * STEP:.3f});')
    js(f'tl.set("#glow", {{filter: "none"}}, {td + 4 * STEP:.3f});')
    js(f'tl.set("#rgbR", {{attr: {{dy: 0}}}}, {td + 4 * STEP:.3f});')
    js(f'tl.set("#rgbB", {{attr: {{dy: 0}}}}, {td + 4 * STEP:.3f});')
    FLASH.append((td + 3 * STEP, "white"))
    # comin' out my body: a ghost of the whole picture lifts up out of it on "out", again on "body"
    a, b = sc[16]
    for tw in [s_ for w, s_ in words_of(16) if w in ("out", "body")]:
        m = 12
        for k in range(m + 1):
            u = k / m
            t = tw + k * STEP
            d = 260 * u ** .7
            al = .6 * (1 - u)
            js(f'tl.set("#fx", {{filter: "url(#ghostf)"}}, {t:.3f});')
            js(f'tl.set("#gho1", {{attr: {{dy: {-d:.0f}, dx: {8 * math.sin(k):.0f}}}}}, {t:.3f});')
            js(f'tl.set("#gho2", {{attr: {{dy: {-d * 1.9:.0f}, dx: {-10 * math.sin(k):.0f}}}}}, {t:.3f});')
            js(f'tl.set("#ghc1", {{attr: {{values: "0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 {al:.2f} 0"}}}}, {t:.3f});')
            js(f'tl.set("#ghc2", {{attr: {{values: "0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 {al * .55:.2f} 0"}}}}, {t:.3f});')
        js(f'tl.set("#fx", {{filter: "none"}}, {tw + (m + 1) * STEP:.3f});')


def tables(rows):
    return "".join(f'<feFunc{c} type="table" tableValues="{" ".join(f"{v:g}" for v in vals)}"/>' for c, vals in zip("RGBA", rows))


FIRE_T = tables([[.69] * 9 + [.69, 1, 1, .95, .55, .22, .12, .08, .07, .06, .06, .06],
                 [.10] * 9 + [.10, .9, .62, .3, .1, .05, .035, .03, .025, .02, .02, .02],
                 [.31] * 9 + [.31, .55, .15, .06, .06, .05, .04, .035, .03, .03, .03, .03],
                 [0] * 8 + [0, .55, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
SMOKE_T = tables([[.96] * 9 + [.96, .94, .9, .78, .66, .74, .88, .96, .86, .72, .8, .92],
                  [.86] * 9 + [.86, .84, .79, .64, .52, .6, .76, .86, .74, .58, .66, .82],
                  [.9] * 9 + [.9, .88, .84, .7, .58, .66, .8, .9, .79, .64, .72, .86],
                  [0] * 8 + [.08, .25, .45, .62, .55, .5, .66, .82, .9, .84, .72, .8, .9]])
FX_DEFS = f"""
      <filter id="firef" filterUnits="objectBoundingBox" x="0" y="0" width="1" height="1.6" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.010 0.004" numOctaves="4" seed="11" result="n0"/>
      <feOffset id="fireo" in="n0" dx="0" dy="0" result="n1"/>
      <feColorMatrix in="n1" type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" result="n"/>
      <feComposite in="SourceGraphic" in2="n" operator="arithmetic" k1="0" k2="0.6" k3="0.4" k4="0" result="v"/>
      <feComponentTransfer in="v" result="c">{FIRE_T}</feComponentTransfer>
      <feComposite in="c" in2="SourceAlpha" operator="in"/></filter>
      <filter id="smk2" filterUnits="objectBoundingBox" x="-0.2" y="0" width="1.4" height="1.6" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.005 0.006" numOctaves="5" seed="3" result="n0"/>
      <feOffset id="smko" in="n0" dx="0" dy="0" result="n1"/>
      <feColorMatrix in="n1" type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" result="n"/>
      <feComposite in="SourceGraphic" in2="n" operator="arithmetic" k1="0" k2="0.6" k3="0.4" k4="0" result="v"/>
      <feComponentTransfer in="v" result="c">{SMOKE_T}</feComponentTransfer>
      <feGaussianBlur in="c" stdDeviation="2" result="cb"/>
      <feComposite in="cb" in2="SourceAlpha" operator="in"/></filter>
      <filter id="ghostf" x="-5%" y="-60%" width="110%" height="170%" color-interpolation-filters="sRGB">
      <feOffset id="gho1" in="SourceGraphic" dx="0" dy="0" result="o1"/>
      <feColorMatrix id="ghc1" in="o1" type="matrix" values="0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 0 0" result="c1"/>
      <feGaussianBlur in="c1" stdDeviation="3" result="g1"/>
      <feOffset id="gho2" in="SourceGraphic" dx="0" dy="0" result="o2"/>
      <feColorMatrix id="ghc2" in="o2" type="matrix" values="0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 0 0" result="c2"/>
      <feGaussianBlur in="c2" stdDeviation="9" result="g2"/>
      <feBlend in="g2" in2="SourceGraphic" mode="screen" result="s1"/><feBlend in="g1" in2="s1" mode="screen"/></filter>"""


# The lively gradient behind the collage (screen space, under the moving paper): big soft colour blobs drifting on
# slow loops, a little brighter on every beat. (x, y, radius, colour, drift x, drift y, period s, phase)
BLOBS = [(300, 300, 480, "#b0194f", 260, 180, 9.0, 0.0), (1100, 380, 400, "#e0336f", -240, 220, 11.0, 1.7),
         (700, 1150, 620, "#2e0818", 200, -260, 13.0, 3.1), (200, 1100, 440, "#5a1660", 220, -160, 10.0, 4.4),
         (1150, 1200, 460, "#8c1442", -260, -200, 12.0, 2.2), (740, 640, 300, "#ff5c8a", 180, 160, 7.5, 5.0)]


def background():
    for f in range(int(DUR * 15)):           # stepped on the edit's 15 fps grid, smooth curves (no shake)
        t = f / 15
        for k, (x, y, r, c, dx, dy, per, ph) in enumerate(BLOBS):
            u = t / per * math.tau + ph
            js(f'tl.set("#bl{k}", {{x: {dx * math.sin(u):.0f}, y: {dy * math.cos(u * .8):.0f}, scale: {1 + .18 * math.sin(u * 1.3):.3f}}}, {t:.3f});')
        lb = max([bt for bt in BEATS["beats"] if bt <= t + 1e-6] or [-9])
        js(f'tl.set("#bg", {{filter: "brightness({1 + .22 * math.exp(-(t - lb) / .12):.3f}) saturate(1.1)"}}, {t:.3f});')


def flashes():
    SCREEN.append('<div id="flash"></div><div id="split"><i></i></div>')
    HIDE.extend(["#flash", "#split"])
    for t, kind in FLASH:
        if kind == "invert":
            js(f'tl.set("#fx", {{filter: "invert(1)"}}, {t:.3f});')
            js(f'tl.set("#fx", {{filter: "none"}}, {t + STEP:.3f});')
        elif kind == "white":
            js(f'tl.set("#flash", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {t + STEP:.3f});')
        elif kind == "split":
            js(f'tl.set("#split", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#split", {{opacity: 0}}, {t + STEP:.3f});')


SP = "url(assets/img/collage/tex/speckle.png) 0 0 / 300px auto"
GR = "url(assets/img/collage/tex/grunge.png)"
CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Archivo Black"; src: url("assets/fonts/ArchivoBlack.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: {INK}; }}
#fx {{ position: absolute; inset: 0; }}
#cam {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; transform-origin: 540px {CY}px; }}
#pan {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; }}
#bg {{ position: absolute; inset: -200px; overflow: hidden; background: radial-gradient(ellipse at 50% 50%, #2a0818, #0c0408 75%); }}
.blob {{ position: absolute; display: block; border-radius: 50%; mix-blend-mode: screen; filter: blur(60px); opacity: .62; }}
{"".join(f'#bl{k} {{ left: {x}px; top: {y}px; width: {r * 2}px; height: {r * 2}px; margin: -{r}px 0 0 -{r}px; background: radial-gradient(circle, {c} 0%, {c}aa 35%, rgba(0,0,0,0) 70%); }}' for k, (x, y, r, c, *_) in enumerate(BLOBS))}
#paper {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; background: url(assets/img/collage/shade.png); opacity: .85; }}
#grid {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; pointer-events: none; opacity: .3; }}
#grid line {{ stroke: {WHT}; stroke-width: 1.6; }}
#board {{ position: absolute; inset: 0; }}
#blinds {{ position: absolute; left: -1100px; top: -1300px; width: 3300px; height: 4500px; z-index: 9; pointer-events: none; mix-blend-mode: multiply;
  background: repeating-linear-gradient(-32deg, rgba(20,6,12,0) 0px, rgba(20,6,12,0) 70px, rgba(20,6,12,.38) 150px, rgba(20,6,12,.42) 210px,
  rgba(20,6,12,0) 290px, rgba(20,6,12,0) 330px); }}
.el {{ position: absolute; opacity: 0; }}
img.el {{ display: block; height: auto; }}
.g3b video {{ width: 100%; height: 100%; display: block; }}
.print {{ position: absolute; background: {WHT}; padding: 16px; box-shadow: 0 14px 26px rgba(0,0,0,.5); z-index: 2; }}
.print img, .print video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.print i {{ position: absolute; inset: 16px; background: {MAG}; mix-blend-mode: multiply; }}
.lw {{ position: absolute; transform-origin: 50% 50%; }}
.lb {{ position: relative; display: inline-block; font: 400 120px/1.12 "Anton"; white-space: nowrap; opacity: 0; padding: .04em .28em 0;
  letter-spacing: .01em; }}
.lb .ch {{ display: inline; }}
.lb .cz {{ filter: blur(.08em); }}
.lb .cur {{ display: inline-block; width: .42em; height: .78em; margin-left: .06em; vertical-align: -.02em; background: rgba(160,150,150,.9); }}
.blk {{ background: {SP}, {INK}; color: {WHT}; box-shadow: 0 12px 22px rgba(0,0,0,.4); }}
.wht {{ background: {SP}, {WHT}; color: {INK}; box-shadow: 0 12px 22px rgba(0,0,0,.35); }}
.magw {{ background: {SP}, {WHT}; color: {MAG}; box-shadow: 0 12px 22px rgba(0,0,0,.35); }}
.magw .cur {{ background: {MAG}; }}
.mag {{ background: {SP}, {MAG}; color: #fff; box-shadow: 0 12px 22px rgba(0,0,0,.35); }}
.mb {{ background: {MAG}; color: #fff; text-shadow: 4px 4px 0 {INK}; box-shadow: 18px 16px 0 {INK}; }}
.blkm {{ background: {INK}; color: #fff; box-shadow: 16px 18px 0 {MAG}; }}
.mtyp {{ background: none; color: {MAG}; padding: 0; -webkit-mask-image: {GR}; mask-image: {GR}; }}
.stamp {{ background: none; color: {WHT}; padding: 0; line-height: 1.08;
  -webkit-mask-image: {GR}; mask-image: {GR}; -webkit-mask-size: 520px auto; mask-size: 520px auto; }}
.stamp .cur {{ background: rgba(240,236,236,.55); }}
.w3d {{ background: none; color: {WHT}; padding: 0; -webkit-text-stroke: 2px #2a2a2a;
  text-shadow: 1px 1px 0 #cfcac2, 2px 2px 0 #bdb7ae, 3px 3px 0 #a7a097, 4px 4px 0 #8f887f, 5px 5px 0 #77706a, 6px 6px 0 #5e5852, 7px 7px 0 #48433e, 10px 12px 10px rgba(0,0,0,.5); }}
.m3d {{ background: none; color: {MAG}; padding: 0; -webkit-text-stroke: 2px #5c0a28;
  text-shadow: 1px 1px 0 #9a1645, 2px 2px 0 #84123b, 3px 3px 0 #6e0f31, 4px 4px 0 #580c27, 5px 5px 0 #42091d, 6px 6px 0 #2c0613, 9px 11px 10px rgba(0,0,0,.45); }}
.mlet {{ background: none; color: {MAG}; padding: 0; text-shadow: 5px 5px 0 rgba(10,10,10,.85);
  -webkit-mask-image: {GR}; mask-image: {GR}; -webkit-mask-size: 700px auto; mask-size: 700px auto; }}
.fill {{ color: transparent; padding: 0; line-height: 1.1; background-size: cover; background-position: 50% 40%;
  -webkit-background-clip: text; background-clip: text; -webkit-text-stroke: 5px {WHT}; filter: drop-shadow(8px 10px 0 rgba(10,10,10,.85)); }}
{"".join(f'.f{li} {{ background-image: url({src}); }}' for li, src in FILL.items())}
.ghost {{ font: 400 250px/1.15 "Anton"; color: rgba(242,241,236,.12); white-space: nowrap; opacity: 0; }}
.para {{ font: 400 38px/1.3 "Archivo Black"; color: {WHT}; z-index: 5; }}
.itag {{ position: absolute; left: 50%; top: 212px; transform: translateX(-50%) rotate(-3deg); font: 400 50px/1.2 "Anton"; white-space: nowrap;
  background: {MAG}; color: #fff; padding: 0 .3em; box-shadow: 0 8px 14px rgba(0,0,0,.35); }}
.rline {{ border: 9px solid {WHT}; z-index: 2; }}
.magblk {{ z-index: 2; background: repeating-linear-gradient(90deg, rgba(0,0,0,.25) 0 3px, rgba(0,0,0,0) 3px 9px),
  radial-gradient(ellipse at 40% 40%, #c21d57, #3d0a1b); }}
.circ {{ position: absolute; left: -10%; top: -22%; width: 120%; height: 144%; overflow: visible; pointer-events: none; }}
.circ path {{ fill: none; stroke: {WHT}; stroke-width: 5.5; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
.tframe {{ position: absolute; z-index: 15; opacity: 0; background: {WHT}; padding: 18px; box-shadow: 0 18px 40px rgba(0,0,0,.55); }}
.tframe img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#flash {{ position: absolute; inset: 0; z-index: 20; background: {WHT}; opacity: 0; }}
#split {{ position: absolute; inset: 0; z-index: 20; background: {MAG}; opacity: 0; }}
#split i {{ position: absolute; left: 50%; top: 0; width: 50%; height: 100%; background: {INK}; }}
#glow {{ position: absolute; inset: 0; }}
#leak {{ position: absolute; inset: -200px; z-index: 17; opacity: 0; pointer-events: none; mix-blend-mode: screen;
  background: radial-gradient(ellipse 35% 60% at 50% 50%, rgba(255,170,120,.85), rgba(255,60,140,.5) 45%, rgba(0,0,0,0) 75%); }}
.counter {{ font: 400 300px/1 "Anton"; color: {WHT}; -webkit-text-stroke: 6px {INK}; paint-order: stroke fill; text-shadow: 14px 14px 0 {MAG}; }}
.shock {{ border-radius: 50%; border: 10px solid {WHT}; box-shadow: 0 0 30px 6px rgba(255,140,190,.8); }}
.ring {{ border-radius: 50%; border: 12px solid {MAG}; box-shadow: 0 0 34px 8px rgba(255,90,150,.7); }}
.ember {{ border-radius: 50%; background: #ffb36b; box-shadow: 0 0 12px 5px #ff4f7a; }}
.wisp {{ border-radius: 50%; background: radial-gradient(ellipse, rgba(255,230,240,.9), rgba(255,120,170,.4) 50%, rgba(0,0,0,0) 72%); filter: blur(6px); }}
.lock {{ left: 0; top: 0; width: {FW}px; height: {FH}px; transform-origin: 540px 540px; pointer-events: none; }}
.embers {{ position: absolute; inset: 0; }}
#heat {{ position: absolute; inset: 0; z-index: 16; opacity: 0; pointer-events: none; mix-blend-mode: screen; }}
#vig {{ position: absolute; inset: 0; z-index: 18; pointer-events: none; background: radial-gradient(ellipse 80% 75% at 50% 48%, rgba(0,0,0,0) 55%, rgba(0,0,0,.4) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1120px; height: 1120px; z-index: 18; pointer-events: none; opacity: .08; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
"""


def main():
    builders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6, "R7": r7, "R8": r8, "R9": r9}
    for si, (a, b, li) in enumerate(scenes()):
        gs = [("SPIN BOUT U", False, .3), ("DRAKE", True, 1.1), ("21 SAVAGE", False, 1.6)] if li < 0 else groups_of(li)
        builders[RECIPE[li]](si, a, b, li, gs)
    lyric_icons()
    transition_frames()
    concepts()
    camera()
    background()
    finishing()
    context_fx()
    pin_locks()
    flashes()
    g = random.Random(3)
    for f in range(int(DUR * 15)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 15:.3f});')
    gl = random.Random(4)
    grid = "".join(f'<line x1="{x + gl.uniform(-8, 8):.0f}" y1="-20" x2="{x + gl.uniform(-40, 40):.0f}" y2="3920"/>' for x in range(260, 2600, 390)) + \
           "".join(f'<line x1="-20" y1="{y + gl.uniform(-8, 8):.0f}" x2="2620" y2="{y + gl.uniform(-40, 40):.0f}"/>' for y in range(200, 3900, 420))
    html = f"""<!doctype html>
<html lang="en" data-resolution="square">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Spin Bout U collage lyric edit 1x1</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><filter id="mb" x="-5%" y="-5%" width="110%" height="110%">
      <feGaussianBlur id="mbg" stdDeviation="0 0"/></filter>
      <filter id="bloom" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feGaussianBlur id="blg" in="SourceGraphic" stdDeviation="20" result="b"/>
      <feColorMatrix in="b" type="matrix" values="1.7 0 0 0 0  0 1.3 0 0 0  0 0 1.6 0 0  0 0 0 1 0" result="bb"/>
      <feBlend in="SourceGraphic" in2="bb" mode="screen"/></filter>
      <filter id="rgbsplit" color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r"/>
      <feOffset id="rgbR" in="r" dx="0" dy="0" result="r2"/>
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g"/>
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b2"/>
      <feOffset id="rgbB" in="b2" dx="0" dy="0" result="b3"/>
      <feBlend in="r2" in2="g" mode="screen" result="rg"/><feBlend in="rg" in2="b3" mode="screen"/></filter>
      <filter id="smokef" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="4" seed="6"/>
      <feOffset id="smo" dx="0" dy="0" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="140" xChannelSelector="R" yChannelSelector="G"/>
      <feGaussianBlur stdDeviation="3"/></filter>{FX_DEFS}</svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="glow"><div id="fx">
        <div id="bg">{"".join(f'<i class="blob" id="bl{k}"></i>' for k in range(len(BLOBS)))}</div>
        <div id="cam"><div id="pan">
          <div id="paper"></div>
          <div id="board">
            {"".join(PAN)}
          </div>
        </div></div>
        <div id="blinds"></div>
        {"".join(SCREEN)}
      </div></div>
      <div id="leak"></div>
      <div id="vig"></div>
      <div id="grain"></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="0" data-volume="1"></audio>
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
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(scenes())} scenes")


if __name__ == "__main__":
    main()
