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
          7: "crew", 15: "spin", 16: "spirit", 17: "snotty", 18: "finale"}
AF, PR, AV = "assets/img/anime/full/", "assets/img/print/", "assets/video/anime/"
CARD1 = {0: AV + "jealous.mp4", 2: PR + "envogue_funky_divas.jpg", 4: PR + "rolex_cat_ad.jpg",
         8: AF + "point.jpg", 11: AV + "her_blush.mp4", 12: AF + "diamonds.jpg", 13: AF + "smoke.jpg"}
CARD2 = {1: PR + "vogue_cat_cover.jpg", 3: "assets/img/src/incoming_call.jpg", 9: AF + "jet.jpg", 10: AV + "road.mp4",
         12: AF + "diamonds.jpg", 15: AV + "spin.mp4", 16: AV + "him_smitten.mp4"}
CUTPRINT = {13: AF + "smoke.jpg", 14: AF + "fire.jpg", 9: None}     # recipes with a cut-out slot that use a picture instead
FILL = {0: AF + "jealous.jpg", 6: PR + "cat_white_dumb.jpg", 11: AF + "him_smitten.jpg"}
G3D_AT = {9: ("globe", 120, 620, 860), 12: ("diamonds", 440, 160, 700), 15: ("heart", 560, 1180, 520), 17: ("tissue", 40, 1350, 460)}
STILLS = [AF + n + ".jpg" for n in ("jealous", "point", "her_blush", "jet", "road", "him_smitten", "diamonds", "smoke", "fire",
                                    "spin", "crew", "finale")] + [PR + "vogue_cat_cover.jpg", PR + "rolex_cat_ad.jpg", PR + "envogue_funky_divas.jpg"]
A, HIDE, PAN, SCREEN = [], [], [], []
CAMKEYS, FLASH = {}, []
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
    rect_outline(200, 560, 680, 560, a + .134, b)
    scrap("red", 1, 560, 760, 520, 6, a + .134, b)
    cam(si, a, 540, 430, 1.3, 0, .01)
    mids = [g for g in gs[1:] if g is not kw]
    t_cut = min(mids[0][2] if mids else (kw[2] if kw is not g0 else a + .5), a + .45)
    cutout(li, 150, 480, 780, -1, t_cut, b)
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
        run = min(320, 380 * (b - pts[-1][0]))
        pts.append((b + .001, lx + d[0] * run, ly + d[1] * run, ls, lr))
        plans.append(dict(a=a, b=b, li=li, d=d, pts=pts))
    tend = DUR - .5
    E, X, TAU = 380, 330, .1

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
        s *= 1 + .025 * math.exp(-(t - lb) / .09)
        fy = 960 + (fy - 960) * VTRACK
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
#paper {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; background: url(assets/img/collage/paper.png); }}
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
    camera()
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
      <feGaussianBlur id="mbg" stdDeviation="0 0"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="fx">
        <div id="cam"><div id="pan">
          <div id="paper"></div>
          <svg id="grid" viewBox="0 0 2600 3900">{grid}</svg>
          <div id="board">
            {"".join(PAN)}
          </div>
        </div></div>
        <div id="blinds"></div>
        {"".join(SCREEN)}
      </div>
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
