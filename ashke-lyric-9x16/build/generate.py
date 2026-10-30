"""Ashke (Karan Aujla, Mxrci) lyric edit, 9:16, 60 s from 2:14 of the song, v3: writes index.html.

python3 build/generate.py      (from the project root; after build/paper.py, scraps.py, cutouts.py, cards.py and
audio.py)

Built as closely as we can to the owner's YouMotion reference ("COUNTRY STREETS ... RIDE YOUR OWN ROAD"): warm crumpled
paper under soft window-blind shadows, hand-drawn grid lines, torn red / black / grey / white paper, photocopied
cut-out stickers of Karan with a white paper border, black-and-white photo prints, condensed bold labels that type on
letter by letter behind a cursor block (black, white, red-on-white, red, red-and-black), a label that slams in big and
settles, huge stamped words, white and red 3D words, a keyword filled with a photo, ghosted repeats, blue marker
circles, black stars, a small print paragraph; one-frame colour-invert flashes, white flash frames, a black/white split
frame; the camera whips into every scene, tracks each label as it lands, pushes, pulls out and zooms in, all stepped
at 15 fps like the reference. The scene recipes and their order are in build/plan.py. Footage: the owner's estate and
Manchester tour clips (cut-outs, prints); no 9:16 blow-ups. Lyric timings: ElevenLabs Scribe; the romanized Punjabi is
ours (confirmed by the owner).
"""
import json
import math
import os
import random
import sys

from PIL import ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan import CARD2, CUTOUT, FILL, RECIPE, W, line_times, scenes  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR, FW, FH = 60.0, 1080, 1920
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
PERIOD = 60 / BEATS["bpm"]
STEP = 1 / 15
R = random.Random(23)
A, HIDE, PAN, SCREEN = [], [], [], []
RED, INK, BLUE = "#d8232a", "#161616", "#2aa7d8"
OSW = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Oswald", "Oswald-700.ttf"), 100)
CAMKEYS = {}          # scene index -> list of (t, fx, fy, scale, rot, dur)
FLASH = []            # (t, kind)
NID = [0]

LYRICS = [
    (3, 6, "Main *seedha turiya jaavan"), (7, 10, "Tu takdi tedi *tedi"), (11, 15, "Tu body kar layi *slim"),
    (16, 21, "Tere te main karda kamm *shady"), (22, 27, "Saada taan tora fera hai na"), (28, 31, "Main nahi launda *gedi"),
    (32, 35, "*Kaaran, jutti te *asla"), (36, 40, "Nahi ae tinn ikki *dukki"), (41, 43, "Nahi leeda *latta"),
    (44, 50, "Top da rakhaan main jaana *chadh ke"), (51, 54, "Kacchi oh *chabb jaa"), (55, 61, "Peene haan *chaa nahi, udda kaadh ke"),
    (62, 64, "*Jatt khulla *ghummda"), (65, 71, "*Vairi nu rakhaan main udda taad ke"), (72, 75, "Nahi taan full *baggy"),
    (76, 80, "*Patthraan 'ch aaya munda paadh ke"), (81, 83, "Kardi meri *adeeta"), (84, 88, "Nahi saada khul gaya *chaaka"),
    (89, 94, "Tu dil kardi ae *chori"), (95, 100, "Nahi taan main maari da *daaka"), (101, 104, "*Bebe kehndi tainu vyahna"),
    (105, 109, "Te mera *shastar dena thaaka"), (110, 114, "Dass ki kar lena *kaama"), (115, 119, "Nahi mera *baaja yaala raakha"),
    (120, 122, "Raahan vich *rode"), (123, 128, "Behna ji *yaarana bhena kass ke"), (129, 131, "*Jatt mudhto *zehri"),
    (132, 137, "*Naagni reha koi saanu dass ke"), (138, 141, "*Baape di saanu bakhshe"), (142, 145, "Chanattiyan *gaani lass ke"),
    (146, 148, "Nahi *mod te paundi"), (149, 153, "Chhumbar de naale kehki *Ashke"), (154, 156, "Nahi mod te paundi"),
]


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def word_slots(li):
    i0, i1, text = LYRICS[li]
    toks = text.split()
    n = i1 - i0 + 1
    slots = [i0 + round(k * (n - 1) / max(1, len(toks) - 1)) for k in range(len(toks))] if len(toks) > 1 else [i0]
    return [(tok.lstrip("*"), tok.startswith("*"), W[s]["s"]) for tok, s in zip(toks, slots)]


def groups_of(li):
    """Labels of one or two words, keywords on their own; one- and two-letter words ride with the label before."""
    ws = word_slots(li)
    if li == 31:
        ws = [w for w in ws if w[0] != "Ashke"]           # "Ashke" is the end title itself
    groups, cur = [], []
    for w in ws:
        if w[1]:
            if cur:
                groups.append(cur)
                cur = []
            groups.append([w])
        else:
            cur.append(w)
            if len(cur) == 2 or sum(len(x[0]) for x in cur) > 10:
                groups.append(cur)
                cur = []
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        txt = " ".join(x[0] for x in g).rstrip(",").upper()
        if out and len(txt) <= 2:
            out[-1] = (out[-1][0] + " " + txt, out[-1][1], out[-1][2])
            continue
        out.append((txt, g[0][1], g[0][2]))
    return out


def tw(text, size):
    return OSW.getlength(text) * size / 100


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


# ------------------------------------------------------------------------------------------------ element helpers
def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {t0:.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')


def scrap(kind, k, x, y, w, rot, t0, t1, z=1):
    i = nid("sc")
    PAN.append(f'<img class="el" id="{i}" src="assets/img/scrap/{kind}-{k}.png" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;'
               f'transform:rotate({rot:.1f}deg);z-index:{z}" alt="">')
    show(f"#{i}", t0, t1)
    return i


def cutout(name, x, y, w, rot, t0, t1, rise=0, red=False, z=3):
    i = nid("ct")
    PAN.append(f'<img class="el" id="{i}" src="assets/img/cut/{name}{"-red" if red else ""}.png" style="left:{x:.0f}px;top:{y:.0f}px;'
               f'width:{w:.0f}px;transform:rotate({rot:.1f}deg);z-index:{z}" alt="">')
    show(f"#{i}", t0, t1)
    if rise:
        js(f'tl.fromTo("#{i}", {{y: {rise}}}, {{y: 0, duration: .4, ease: "steps(6)", immediateRender: false}}, {t0:.3f});')
    return i


def card(n, x, y, w, h, rot, t0, t1, red=False):
    """Move a footage print (card1 / card2 track) into place for [t0, t1)."""
    js(f'tl.set("#pr{n}", {{opacity: 1, left: {x:.0f}, top: {y:.0f}, width: {w:.0f}, height: {h:.0f}, rotation: {rot:.1f}}}, {t0:.3f});')
    js(f'tl.set("#pr{n} i", {{opacity: {.9 if red else 0}}}, {t0:.3f});')
    js(f'tl.fromTo("#pr{n}", {{x: {R.choice([-120, 120])}}}, {{x: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')
    if t1 < DUR:
        js(f'tl.set("#pr{n}", {{opacity: 0}}, {t1:.3f});')


def star(x, y, size, t0, t1, color=INK, n=7, seed=0):
    i = nid("st")
    PAN.append(f'<svg class="el" id="{i}" viewBox="-50 -50 100 100" style="left:{x:.0f}px;top:{y:.0f}px;width:{size}px;height:{size}px;z-index:4">'
               f'<path d="{star_path(n, seed=seed)}" fill="{color}"/></svg>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i}", {{scale: 0, rotation: -40}}, {{scale: 1, rotation: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')


def label(text, style, x, y, size, rot, t, t1, mode="type", circle=False, anchor="center", z=5):
    """A label. mode: type (letter by letter behind a cursor block), slam (big, settles), pop."""
    i = nid("lb")
    size = min(size * 1.12, fit(text, 980, 999))          # the reference's labels run big, close to the frame edges
    w = tw(text, size) + size * .56
    left = x - w / 2 if anchor == "center" else x
    letters = "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in text)
    cur = '<span class="cur"></span>' if mode == "type" else ""
    PAN.append(f'<div class="lw" data-layout-allow-overlap style="left:{left:.0f}px;top:{y:.0f}px;transform:rotate({rot:.1f}deg);z-index:{z}">'
               f'<div class="lb {style}" id="{i}" style="font-size:{size:.0f}px">{letters}{cur}{CIRC if circle else ""}</div></div>')
    show(f"#{i}", t, t1)
    if mode == "type":
        per = 2 if len(text) > 9 else 1
        js(f'tl.set("#{i} .ch", {{display: "none"}}, {t - .001:.3f});')
        k = 0
        while k < len(text):
            js(f'tl.set("#{i} .ch:nth-child(-n+{min(len(text), k + per)})", {{display: "inline"}}, {t + (k // per) * STEP:.3f});')
            k += per
        done = t + (len(text) // per + 1) * STEP
        js(f'tl.set("#{i} .cur", {{display: "none"}}, {done:.3f});')
    elif mode == "slam":
        js(f'tl.fromTo("#{i}", {{scale: 1.65}}, {{scale: 1, duration: .27, ease: "steps(4)", immediateRender: false}}, {t:.3f});')
        done = t + .27
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
               f'<path pathLength="400" d="M8 70 C4 20 60 -6 96 30" fill="none" stroke="{BLUE}" stroke-width="3.2" stroke-linecap="round" '
               f'stroke-dasharray="400"/></svg>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i} path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .27, ease: "steps(4)", immediateRender: false}}, {t0:.3f});')


def block(x, y, w, h, t0, t1, cls="redblk"):
    i = nid("bk")
    PAN.append(f'<i class="el {cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>')
    show(f"#{i}", t0, t1)


def flame(x, y, t0, t1):
    i = nid("fl")
    PAN.append(f'<svg class="el" id="{i}" viewBox="0 0 100 120" style="left:{x}px;top:{y}px;width:150px;height:180px;z-index:4">'
               '<path d="M50 4 C62 30 88 42 80 78 C76 100 60 114 46 114 C26 112 12 96 16 74 C20 56 34 52 34 36 C44 46 46 56 46 64 '
               'C56 52 58 30 50 4 Z M40 112 C30 96 38 84 48 72 C50 86 62 92 56 112" fill="#f4f2ec" stroke="#161616" stroke-width="5" '
               'stroke-linejoin="round"/></svg>')
    show(f"#{i}", t0, t1)


def cam(si, t, fx, fy, s=1.0, rot=0.0, dur=.35):
    CAMKEYS.setdefault(si, []).append((t, fx, fy, s, rot, dur))


def fit(text, maxw, size):
    return min(size, maxw / (tw(text, 100) / 100 + .56))


# ------------------------------------------------------------------------------------------------ recipes
def r1(si, a, b, li, gs):
    scrap("red", 0, 30, 230, 1020, -7, a, b)
    scrap("black", 3, 600, 40, 560, 14, a, b)
    cutout(CUTOUT[li], 120, 150, 840, -2, a, b, rise=320)
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
            label(txt, "redw", 560, y, size, -1.5, t, b, mode="type", circle=key)
            y += size * 1.12 + 22
            cam(si, t, 540, 960 + (y - 1200) * .3, 1.02, 0, .4)
    para(["ASHKE. KARAN AUJLA, MXRCI.", "A LYRIC EDIT BY", "NXTLVL SOCIAL."], 110, y + 30, gs[min(1, len(gs) - 1)][2], b)
    star(60, max(1530, y + 190), 230, a + PERIOD, b, seed=si)
    star(290, max(1700, y + 330), 110, a + PERIOD * 1.5, b, seed=si + 1)
    if b - a > 1.4:
        FLASH.append((a + PERIOD * 2, "invert"))


def r2(si, a, b, li, gs):
    kw = next((g for g in reversed(gs) if g[1]), gs[-1])      # the last keyword is the photo-filled one
    ki = gs.index(kw)
    if kw[2] - .067 > a + .1:
        card(1, 60, 580, 960, 1060, 2, a, kw[2] - .067)
    scrap("black", 1, -80, 1500, 900, -4, a, b)
    cam(si, a, 540, 860, 1.12, 1.5, .01)
    y = 520
    for k, (txt, key, t) in enumerate(gs[:ki]):
        size = fit(txt, 820, 120)
        label(txt, "blk", 540 - 60 * k, y, size, -2, t, b)
        y += size * 1.15 + 18
        cam(si, t, 540, 760 + 60 * k, 1.1, 1, .3)
    FLASH.append((kw[2] - .067, "white"))
    scrap("red", 3, -60, 760, 1200, -5, kw[2], b)
    cutout(CUTOUT.get(li, "suit_b"), 180, 620, 720, 2, kw[2], b, z=2)
    size = fit(kw[0], 1060, 330)
    _, fw = label(kw[0], f"fill f{li}", 540, 860, size, -3, kw[2], b, mode="pop", z=6)
    cam(si, kw[2], 540, 960, 1.0, 0, .2)
    zt = kw[2] + .4
    after = gs[ki + 1:]
    back = min(b - .1, (after[0][2] - .05) if after else kw[2] + 1.0, zt + .55)
    if back - zt > .2:
        cam(si, zt, 540 + fw * .22, 860 + size * .5, 1.85, -2, .27)
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
    label(g0[0], "rb", 520, 520, size, -2, g0[2], b)
    cam(si, a, 540, 560, 1.45, -2, .01)
    rest = [g for g in gs[1:] if g is not kw]
    t_pull = rest[0][2] if rest else (kw[2] if kw is not g0 else a + .6)
    block(170, 960, 740, 560, t_pull, b)
    cutout(CUTOUT[li], 150, 640, 780, 1, t_pull, b)
    cam(si, t_pull, 540, 1000, 1.0, 0, .4)
    for k, (txt, key, t) in enumerate(rest):
        label(txt, "blk", 300 + 60 * k, 700 + 130 * k, fit(txt, 600, 100), -4, t, b)
    if kw is not g0:
        scrap("white", 1, 140, 1320, 800, -3, kw[2], b, z=4)
        label(kw[0], "r3d", 540, 1390, fit(kw[0], 760, 200), -3, kw[2], b, z=6)
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
    cutout(CUTOUT[li], 150, 480, 780, -1, t_cut, b)
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
    card(1, 120, 520, 640, 760, -5, a, b)
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
    if li in CARD2:
        card(2, 500, 700, 560, 700, 6, tc, b, red=True)
        cam(si, tc + .1, 640, 1100, 1.0, 1, .4)


def r6(si, a, b, li, gs):
    kw = next((g for g in gs if g[1]), gs[-1])
    card(1, 400, 170, 660, 760, 9, a, b)
    scrap("black", 1, -120, 820, 700, -6, a, b)
    arc(60, 160, 360, a + .2, b)
    cam(si, a, 640, 860, 1.0, 1, .01)
    rest = [g for g in gs if g is not kw]
    y = 1040
    for k, (txt, key, t) in enumerate(rest):
        sz = fit(txt, 760, 150)
        label(txt, "wht" if k == 0 else "blk", 400 + 120 * (k % 2), y, sz, -3 + 4 * k, t, b, z=6)
        y += sz * 1.15 + 20
        cam(si, t, 480, 1000 + 40 * k, 1.0, 0, .35)
    label(kw[0], "rlet", 560, y + 20, fit(kw[0], 900, 240), -6, kw[2], b, circle=kw[1], z=6)
    star(720, y + 240, 90, kw[2] + .2, b, color=RED, n=6, seed=si)
    star(830, y + 300, 60, kw[2] + .27, b, color=RED, n=6, seed=si + 5)
    cam(si, kw[2], 540, min(1250, y + 60), 1.08, -1, .35)


def r7(si, a, b, li, gs):
    kw = next((g for g in gs if g[1]), gs[-1])
    scrap("black", 2, 260, 110, 480, 8, a, b)
    card(1, 140, 880, 760, 700, -3, a, b)
    cam(si, a, 540, 1000, 1.0, 0, .01)
    rest = [g for g in gs if g is not kw]
    if rest:
        g0 = rest[0]
        label(g0[0], "rtyp", 620, 430, fit(g0[0], 700, 112), -6, g0[2], b, z=6)
        cam(si, g0[2], 600, 620, 1.12, -1, .3)
    label(kw[0], "wht", 540, 560, fit(kw[0], 900, 180), -2, kw[2], b, z=6)
    cam(si, kw[2], 540, 800, 1.04, 0, .35)
    for k, (txt, key, t) in enumerate(rest[1:]):
        label(txt, "blk", 540, 1600 + 130 * k, fit(txt, 700, 110), 3, t, b, z=6)
        cam(si, t, 540, 1200, 1.0, 0, .35)


def r8(si, a, b, li, gs):
    kw = next((g for g in reversed(gs) if g[1]), gs[-1])
    g0 = gs[0]
    FLASH.append((a, "invert"))
    t2 = gs[1][2] if len(gs) > 1 else a + .9
    # phase A: the cut-out over red torn paper, the first label red on white
    scrap("red", 0, -60, 1080, 960, -8, a, t2)
    scrap("black", 2, -160, 720, 420, 4, a, t2)
    cutout(CUTOUT[li], 90, 260, 900, 0, a, t2)
    flame(800, 1260, a + .2, t2)
    label(g0[0], "redw", 540, 1270, fit(g0[0], 900, 150), -2, g0[2], t2, z=6)
    cam(si, a, 540, 960, 1.0, 0, .01)
    cam(si, g0[2], 540, 1060, 1.05, 0, .3)
    # phase B: relayout, the cut-out smaller, a big stamped word over a black label with a red block, first label below
    scrap("red", 3, -40, 1180, 1000, -6, t2, b)
    cutout(CUTOUT[li], 280, 640, 540, 0, t2, b)
    flame(760, 1380, t2, b)
    label(g0[0], "redw", 540, 1460, fit(g0[0], 800, 120), -4, t2, b, mode="pop", z=6)
    for k, (txt, key, t) in enumerate(g for g in gs[1:] if g is not kw):
        label(txt, "blkr", 540, 470 + 10 * k, fit(txt, 900, 130), -2, t, b, z=6)
    if kw is not g0:
        label(kw[0], "stamp", 540, 220, fit(kw[0], 1000, 250), -3, kw[2], b, z=5)
    cam(si, t2, 540, 880, 1.0, 0, .01)
    cam(si, t2 + .3, 540, 920, 1.04, 0, .5)


def r9(si, a, b, li, gs):
    FLASH.append((a, "split"))
    scrap("grey", 3, -160, -90, 1000, 5, a, b)
    scrap("grey", 1, 420, 1560, 860, -7, a, b)
    scrap("white", 2, -120, 880, 760, 3, a, b)
    kw = next((g for g in gs if g[1]), None)
    rest = [g for g in gs if g is not kw]
    pos = [(420, 740, "redw", 175, -2), (680, 960, "red", 140, 3), (520, 1170, "w3d", 210, -2), (440, 1380, "blk", 130, -3)]
    cam(si, a, 420, 820, 1.25, -1, .01)
    for k, (txt, key, t) in enumerate(rest):
        x, y, st, size, rot = pos[k % 4]
        label(txt, st, x, y, fit(txt, 900, size), rot, t, b, z=6)
        cam(si, t, (x + 540) / 2, y + 60, 1.22, rot * .3, .3)
    if kw:
        label(kw[0], "stamp", 540, 1000, fit(kw[0], 1040, 300), -2, kw[2], b, circle=True, z=5)
        cam(si, kw[2], 540, 1060, 1.0, 0, .4)


def ending(si, a, b, li, gs):
    """Line 31 runs as type only up to "Ashke", then the end title takes over (end_card)."""
    t = W[153]["s"]
    r9(si, a, t, li, gs)
    FLASH.append((t - .067, "white"))


def end_card():
    """The reference's logo moment: white flash, ASHKE on white tape between grid lines, the blue circle draws round."""
    t = W[153]["s"]
    PAN.append('<svg class="el" id="eg" viewBox="0 0 700 300" style="left:190px;top:800px;width:700px;height:300px;z-index:5">' +
               "".join(f'<line x1="{x}" y1="10" x2="{x + 4}" y2="290" stroke="#2b2724" stroke-width="2.4"/>' for x in range(80, 640, 72)) +
               '<line x1="10" y1="60" x2="690" y2="56" stroke="#2b2724" stroke-width="2.4"/>'
               '<line x1="10" y1="246" x2="690" y2="250" stroke="#2b2724" stroke-width="2.4"/></svg>')
    show("#eg", t, DUR)
    scrap("black", 0, 160, -160, 760, 4, t, DUR)
    scrap("white", 3, 280, 1480, 640, -4, t, DUR)
    PAN.append('<div class="lw" data-layout-allow-overlap style="left:236px;top:870px;z-index:6;transform:rotate(-1.5deg)"><div class="lb logo" id="logo">'
               + "".join(f'<span class="ch">{c}</span>' for c in "Ashke") + f'<span class="cur"></span>{CIRC}</div></div>')
    show("#logo", t + .067, DUR)
    js(f'tl.set("#logo .ch", {{display: "none"}}, {t + .066:.3f});')
    for k in range(5):
        js(f'tl.set("#logo .ch:nth-child(-n+{k + 1})", {{display: "inline"}}, {t + .067 + k * STEP:.3f});')
    js(f'tl.set("#logo .cur", {{display: "none"}}, {t + .067 + 6 * STEP:.3f});')
    js(f'tl.fromTo("#logo .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .5, ease: "steps(8)", immediateRender: false}}, {t + .55:.3f});')
    label("KARAN AUJLA · MXRCI", "blk", 540, 1180, 64, 1.5, line_times(32)[0], DUR, z=6)
    js(f'tl.to("#dim", {{opacity: .55, duration: .3, ease: "steps(3)"}}, {DUR - .3:.3f});')


# ------------------------------------------------------------------------------------------------ camera
def ease_out(u, p=3):
    return 1 - (1 - max(0, min(1, u))) ** p


DIRS = [(0, 1), (0, 1), (1, .3), (0, 1), (-.8, .6), (0, -1), (.7, .7), (0, 1), (-1, 0), (0, 1), (.6, .8), (1, 0)]


def camera():
    """Sampled at 15 fps: each scene's keys (eased, power3 out), a whip in (expo out), a slow drift along the scene's
    direction, a whip out along the next scene's direction, a little hand jitter. From the end title on, it rests."""
    plans = []
    for si, (a, b, li) in enumerate(scenes()):
        keys = sorted(CAMKEYS.get(si, [(a, 540, 960, 1.0, 0, .01)]))
        d = DIRS[si % len(DIRS)]
        n = math.hypot(*d)
        plans.append(dict(a=a, b=b, li=li, keys=keys, d=(d[0] / n, d[1] / n)))
    E, X = 430, 340
    tend = W[153]["s"] - .067
    g = random.Random(9)
    for f in range(int(DUR * 15)):
        t = f / 15
        if t >= tend:
            u = t - tend
            js(f'tl.set("#pan", {{x: {g.uniform(-1, 1):.1f}, y: {g.uniform(-1, 1):.1f}}}, {t:.3f});')
            js(f'tl.set("#cam", {{scale: {1 + .03 * u:.4f}, rotation: 0}}, {t:.3f});')
            continue
        si = max(i for i, p in enumerate(plans) if p["a"] <= t + 1e-6)
        p = plans[si]
        k0 = p["keys"][0]
        fx, fy, s, rot = k0[1], k0[2], k0[3], k0[4]
        for (tk, kx, ky, ks, kr, kd) in p["keys"][1:]:
            if t >= tk:
                v = ease_out((t - tk) / kd)
                fx, fy, s, rot = fx + (kx - fx) * v, fy + (ky - fy) * v, s + (ks - s) * v, rot + (kr - rot) * v
        u = t - p["a"]
        d = p["d"]
        e = 1 - ease_out(u / .4, 4)
        fx -= d[0] * E * e
        fy -= d[1] * E * e
        rot += 3.5 * e * (1 if si % 2 else -1)
        fx += d[0] * 22 * u
        fy += d[1] * 22 * u
        if si + 1 < len(plans) and p["b"] < tend:
            w = p["b"] - t
            if w < .2:
                v = ((.2 - w) / .2) ** 2
                nd = plans[si + 1]["d"]
                fx += nd[0] * X * v
                fy += nd[1] * X * v
                rot += 2.5 * v * (1 if si % 2 else -1)
        fx += g.uniform(-1.5, 1.5)
        fy += g.uniform(-1.5, 1.5)
        js(f'tl.set("#pan", {{x: {540 - fx:.1f}, y: {960 - fy:.1f}}}, {t:.3f});')
        js(f'tl.set("#cam", {{scale: {s * 1.06:.4f}, rotation: {rot:.2f}}}, {t:.3f});')


def flashes():
    """One-step accents, as in the reference: colour invert, white, black/white split."""
    SCREEN.append('<div id="flash"></div><div id="split"><i></i></div>')
    HIDE.extend(["#flash", "#split"])
    for t, kind in FLASH:
        if kind == "invert":
            js(f'tl.set("#fx", {{filter: "invert(1) hue-rotate(180deg) saturate(1.4)"}}, {t:.3f});')
            js(f'tl.set("#fx", {{filter: "none"}}, {t + STEP:.3f});')
        elif kind == "white":
            js(f'tl.set("#flash", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {t + STEP:.3f});')
        elif kind == "split":
            js(f'tl.set("#split", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#split", {{opacity: 0}}, {t + STEP:.3f});')


CSS = f"""
@font-face {{ font-family: "Oswald"; font-weight: 700; src: url("assets/fonts/Oswald/Oswald-700.ttf"); }}
@font-face {{ font-family: "Oswald"; font-weight: 500; src: url("assets/fonts/Oswald/Oswald-500.ttf"); }}
@font-face {{ font-family: "Outfit"; font-weight: 800; src: url("assets/fonts/Outfit/Outfit-800.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #e9e4dc; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #e9e4dc; }}
#fx {{ position: absolute; inset: 0; }}
#cam {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; transform-origin: 540px 960px; }}
#pan {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; }}
#paper {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; background: url(assets/img/paper.png);
  filter: sepia(.18) brightness(.98); }}
#grid {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; pointer-events: none; opacity: .55; }}
#grid line {{ stroke: #2f2b28; stroke-width: 1.6; }}
#board {{ position: absolute; inset: 0; }}
#blinds {{ position: absolute; left: -1100px; top: -1300px; width: 3300px; height: 4500px; z-index: 9; pointer-events: none; mix-blend-mode: multiply;
  background: repeating-linear-gradient(-32deg, rgba(70,55,40,0) 0px, rgba(70,55,40,0) 70px, rgba(70,55,40,.30) 150px, rgba(70,55,40,.34) 210px,
  rgba(70,55,40,0) 290px, rgba(70,55,40,0) 330px); }}
.el {{ position: absolute; opacity: 0; }}
img.el {{ display: block; height: auto; }}
.print {{ position: absolute; left: 0; top: 0; width: 600px; height: 700px; opacity: 0; z-index: 2; background: #f3f1ec; padding: 16px;
  box-shadow: 0 14px 26px rgba(0,0,0,.32); }}
.print video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.print i {{ position: absolute; inset: 16px; background: {RED}; mix-blend-mode: multiply; opacity: 0; }}
.lw {{ position: absolute; transform-origin: 50% 50%; }}
.lb {{ position: relative; display: inline-block; font: 700 120px/1 "Oswald"; text-transform: uppercase; white-space: nowrap; opacity: 0;
  padding: .1em .28em .06em; letter-spacing: .5px; }}
.lb .ch {{ display: inline; }}
.lb .cur {{ display: inline-block; width: .5em; height: .86em; margin-left: .06em; vertical-align: -.04em; background: rgba(95,92,88,.9); }}
.blk {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, {INK}; color: #f1eee8; box-shadow: 0 12px 22px rgba(0,0,0,.28); }}
.wht {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, #f3f1ec; color: {INK}; box-shadow: 0 12px 22px rgba(0,0,0,.25); }}
.redw {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, #f3f1ec; color: {RED}; box-shadow: 0 12px 22px rgba(0,0,0,.25); }}
.redw .cur {{ background: {RED}; }}
.red {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, {RED}; color: #fff; box-shadow: 0 12px 22px rgba(0,0,0,.25); }}
.rb {{ background: {RED}; color: #fff; text-shadow: 4px 4px 0 {INK}; box-shadow: 18px 16px 0 {INK}; }}
.blkr {{ background: {INK}; color: #fff; box-shadow: 16px 18px 0 {RED}; }}
.rtyp {{ background: none; color: {RED}; padding: 0; -webkit-mask-image: url(assets/img/tex/grunge.png); mask-image: url(assets/img/tex/grunge.png); }}
.stamp {{ background: none; color: #1c1b1a; padding: 0; letter-spacing: -2px; line-height: .92;
  -webkit-mask-image: url(assets/img/tex/grunge.png); mask-image: url(assets/img/tex/grunge.png); -webkit-mask-size: 520px auto; mask-size: 520px auto; }}
.stamp .cur {{ background: rgba(60,58,55,.55); }}
.w3d {{ background: none; color: #f6f4ef; padding: 0; -webkit-text-stroke: 2px #2a2a2a;
  text-shadow: 1px 1px 0 #cfcac2, 2px 2px 0 #bdb7ae, 3px 3px 0 #a7a097, 4px 4px 0 #8f887f, 5px 5px 0 #77706a, 6px 6px 0 #5e5852, 7px 7px 0 #48433e, 10px 12px 10px rgba(0,0,0,.5); }}
.r3d {{ background: none; color: {RED}; padding: 0; -webkit-text-stroke: 2px #6e0b0f;
  text-shadow: 1px 1px 0 #a5121a, 2px 2px 0 #8c0f16, 3px 3px 0 #730c12, 4px 4px 0 #5a090e, 5px 5px 0 #40070a, 6px 6px 0 #2a0507, 9px 11px 10px rgba(0,0,0,.45); }}
.rlet {{ background: none; color: {RED}; padding: 0; text-shadow: 5px 5px 0 rgba(22,22,22,.85);
  -webkit-mask-image: url(assets/img/tex/grunge.png); mask-image: url(assets/img/tex/grunge.png); -webkit-mask-size: 700px auto; mask-size: 700px auto; }}
.fill {{ color: transparent; padding: 0; letter-spacing: -2px; line-height: .95; background-size: cover; background-position: 50% 40%;
  -webkit-background-clip: text; background-clip: text; -webkit-text-stroke: 3px {INK}; filter: drop-shadow(8px 10px 0 rgba(22,22,22,.85)); }}
{"".join(f'.f{li} {{ background-image: url(assets/img/photo/fill_{li}.jpg); }}' for li in FILL)}
.ghost {{ font: 700 250px/1 "Oswald"; text-transform: uppercase; color: rgba(40,36,32,.16); white-space: nowrap; opacity: 0; letter-spacing: -2px; }}
.para {{ font: 500 34px/1.22 "Oswald"; color: #2a2724; letter-spacing: .3px; z-index: 5; }}
.rline {{ border: 9px solid {RED}; z-index: 2; }}
.redblk {{ z-index: 2; background: repeating-linear-gradient(90deg, rgba(0,0,0,.25) 0 3px, rgba(0,0,0,0) 3px 9px),
  radial-gradient(ellipse at 40% 40%, #a3121a, #4a0609); }}
.logo {{ font: 800 150px/1 "Outfit"; text-transform: none; color: {RED}; letter-spacing: -2px; padding: .12em .34em .16em;
  background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, #f5f3ee; box-shadow: 0 16px 26px rgba(0,0,0,.28); }}
.logo .cur {{ background: rgba(90,88,85,.8); }}
.circ {{ position: absolute; left: -10%; top: -22%; width: 120%; height: 144%; overflow: visible; pointer-events: none; }}
.circ path {{ fill: none; stroke: {BLUE}; stroke-width: 5.5; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
#flash {{ position: absolute; inset: 0; z-index: 20; background: #f7f6f2; opacity: 0; }}
#split {{ position: absolute; inset: 0; z-index: 20; background: #f4f3ef; opacity: 0; }}
#split i {{ position: absolute; left: 50%; top: 0; width: 50%; height: 100%; background: #111; }}
#dim {{ position: absolute; inset: 0; z-index: 19; background: #000; opacity: 0; pointer-events: none; }}
#vig {{ position: absolute; inset: 0; z-index: 18; pointer-events: none; background: radial-gradient(ellipse 80% 75% at 50% 48%, rgba(0,0,0,0) 58%, rgba(30,20,10,.28) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1120px; height: 1960px; z-index: 18; pointer-events: none; opacity: .07; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
"""


def main():
    builders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6, "R7": r7, "R8": r8, "R9": r9, "END": ending}
    for si, (a, b, li) in enumerate(scenes()):
        if li == 32:
            continue
        gs = [("ASHKE", False, .75), ("KARAN AUJLA", True, 1.25)] if li < 0 else groups_of(li)
        builders[RECIPE[li]](si, a, b, li, gs)
    end_card()
    camera()
    flashes()
    g = random.Random(3)
    for f in range(int(DUR * 15)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 15:.3f});')
    gl = random.Random(4)
    grid = "".join(f'<line x1="{x + gl.uniform(-8, 8):.0f}" y1="-20" x2="{x + gl.uniform(-40, 40):.0f}" y2="3920"/>' for x in range(260, 2600, 390)) + \
           "".join(f'<line x1="-20" y1="{y + gl.uniform(-8, 8):.0f}" x2="2620" y2="{y + gl.uniform(-40, 40):.0f}"/>' for y in range(200, 3900, 420))
    prints = "".join(f'<div class="print" id="pr{n}"><video id="cv{n}" class="clip" src="assets/video/card{n}.mp4" data-start="0" '
                     f'data-duration="{DUR}" data-track-index="{n}" muted playsinline></video><i></i></div>' for n in (1, 2))
    HIDE.extend(["#pr1", "#pr2"])
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Ashke collage lyric edit 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{FW}" data-height="{FH}">
      <div id="fx">
        <div id="cam"><div id="pan">
          <div id="paper"></div>
          <svg id="grid" viewBox="0 0 2600 3900">{grid}</svg>
          <div id="board">
            {prints}
            {"".join(PAN)}
          </div>
          <div id="blinds"></div>
        </div></div>
        {"".join(SCREEN)}
      </div>
      <div id="dim"></div>
      <div id="vig"></div>
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
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(scenes())} scenes")


if __name__ == "__main__":
    main()
