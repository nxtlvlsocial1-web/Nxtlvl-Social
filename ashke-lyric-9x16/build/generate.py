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
Also, at the owner's request: every print opens on its sharpest frame and then runs into the footage (build/cards.py),
scene changes get two single-frame stills (a print-sized freeze frame per step) ahead of the cut, and each lyric line
gets one element drawn from what it says (build/icons.py).
"""
import json
import math
import os
import random
import sys

from PIL import ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import ICON, WORD, svg  # noqa: E402
from plan import CARD2, CUTOUT, FILL, OFFSET, PRINT, RECIPE, TRANS_POOL, W, line_times, scenes  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR, SONG, FW, FH = 60.0, 60.0, 1080, 1920     # 60 s from 2:14 (build/plan.py)
EV = []               # sound events for build/sound.py: (time, kind)
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
PERIOD = 60 / BEATS["bpm"]
STEP = 1 / 15
R = random.Random(23)
A, HIDE, PAN, SCREEN = [], [], [], []
RED, INK, BLUE = "#d8232a", "#161616", "#2aa7d8"
GUR = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "AnekGurmukhi", "AnekGurmukhi-Condensed-800.ttf"), 100,
                         layout_engine=ImageFont.Layout.RAQM)
CAMKEYS = {}          # scene index -> list of (t, fx, fy, scale, rot, dur)
FLASH = []            # (t, kind)
NID = [0]

LYRICS = [   # the owner's lyrics (2026-10-31), on the sung lines; (first word, last word) index the Scribe timings
    (3, 6, "Main *sidha turiya jaavaan"), (7, 10, "Tu takkdi tedhi *tedhi"), (11, 15, "Tu body karli *slim"),
    (16, 21, "Teri te main karda kamm *shady"), (22, 27, "Saada taan tora phera ae na"), (28, 31, "Main ni laaunda *gedhi"),
    (32, 35, "*Car'an jutti te *asla"), (36, 40, "Ni eh tinne *Italy made hi"), (41, 43, "Ni leerha *latta"),
    (44, 50, "Top da rakhaa main jaane *chaadh ke"), (51, 54, "Kacchi o *chabb ja"), (55, 61, "Peene aa *chaahaan nu ohda kaadh ke"),
    (62, 64, "*Jatt khulla *ghummda"), (65, 71, "*Vairi nu rakhhaan main ohda taadh ke"), (72, 75, "Ni tu *phull vargi"),
    (76, 80, "*Pathraan nu aaya munda paarh ke"), (81, 83, "Kardi meriyan *deeda"), (84, 88, "Ni saada khull gaya *jhaaka"),
    (89, 94, "Tu dil kardi ae *chori ni"), (95, 100, "Te main maarida *daaka"), (101, 104, "*Bebe kehndi tainu viaahuna"),
    (105, 109, "Te mera *shastar de naal thaaka"), (110, 114, "Dass ki kar laina *kaavaan"), (115, 119, "Ni mera *baajaan aala raakha"),
    (120, 122, "Raahan vich *rodhe"), (123, 128, "Behna je *yaaran naa paina kasske"), (129, 131, "*Jatt mudh ton *zehri"),
    (132, 137, "*Naag ni riha koi saanu dass ke"), (138, 141, "*Baabe di saanu bakhshe"), (142, 145, "Kann nattian *gaani lashke"),
    (146, 148, "Ni *modhe paundi"), (149, 153, "Jhummar doonaali keh ke *Ashke"), (154, 156, "Ni modhe paundi"),
]


GURMUKHI = [   # the owner's Gurmukhi (2026-10-31), word for word with LYRICS; English words stay in Latin as written
    "ਮੈਂ *ਸਿੱਧਾ ਤੁਰਿਆ ਜਾਵਾਂ", "ਤੂੰ ਤੱਕਦੀ ਟੇਢੀ *ਟੇਢੀ", "ਤੂੰ body ਕਰਲੀ *slim", "ਤੇਰੀ ਤੇ ਮੈਂ ਕਰਦਾ ਕੰਮ *shady",
    "ਸਾਡਾ ਤਾਂ ਤੋਰਾ ਫੇਰਾ ਏ ਨਾ", "ਮੈਂ ਨੀ ਲਾਉਂਦਾ *ਗੇੜੀ", "*Car'an ਜੁੱਤੀ ਤੇ *ਅਸਲਾ", "ਨੀ ਏਹ ਤਿੰਨੇ *Italy made ਹੀ",
    "ਨੀ ਲੀੜਾ *ਲੱਤਾ", "top ਦਾ ਰੱਖਾ ਮੈਂ ਜਾਣੇ *ਚਾੜ੍ਹ ਕੇ", "ਕੱਚੀ ਓ *ਚੱਬ ਜਾ", "ਪੀਣੇ ਆ *ਚਾਹਾਂ ਨੂੰ ਓਹਦਾ ਕਾੜ੍ਹ ਕੇ",
    "*ਜੱਟ ਖੁੱਲ੍ਹਾ *ਘੁੰਮਦਾ", "*ਵੈਰੀ ਨੂੰ ਰੱਖਾਂ ਮੈਂ ਓਹਦਾ ਤਾੜ ਕੇ", "ਨੀ ਤੂੰ *ਫੁੱਲ ਵਰਗੀ", "*ਪੱਥਰਾਂ ਨੂੰ ਆਇਆ ਮੁੰਡਾ ਪਾੜ ਕੇ",
    "ਕਰਦੀ ਮੇਰੀਆਂ *ਦੀਦਾ", "ਨੀ ਸਾਡਾ ਖੁੱਲ ਗਿਆ *ਝਾਕਾ", "ਤੂੰ ਦਿਲ ਕਰਦੀ ਏ *ਚੋਰੀ ਨੀ", "ਤੇ ਮੈਂ ਮਾਰੀਦਾ *ਡਾਕਾ",
    "*ਬੇਬੇ ਕਹਿੰਦੀ ਤੈਨੂੰ ਵਿਆਹੁਣਾ", "ਤੇ ਮੇਰਾ *ਸ਼ਸਤਰ ਦੇ ਨਾਲ ਠਾਕਾ", "ਦੱਸ ਕੀ ਕਰ ਲੈਣਾ *ਕਾਵਾਂ", "ਨੀ ਮੇਰਾ *ਬਾਜਾਂ ਆਲਾ ਰਾਖਾ",
    "ਰਾਹਾਂ ਵਿੱਚ *ਰੋੜੇ", "ਬਹਿਣਾ ਜੇ *ਯਾਰਾਂ ਨਾ ਪੈਣਾ ਕੱਸਕੇ", "*ਜੱਟ ਮੁੱਢ ਤੋਂ *ਜ਼ਹਿਰੀ", "*ਨਾਗ ਨੀ ਰਿਹਾ ਕੋਈ ਸਾਨੂੰ ਡੱਸ ਕੇ",
    "*ਬਾਬੇ ਦੀ ਸਾਨੂੰ ਬਖ਼ਸ਼ੇ", "ਕੰਨ ਨੱਤੀਆਂ *ਗਾਨੀ ਲਸ਼ਕੇ", "ਨੀ *ਮੋਢੇ ਪਾਉਂਦੀ", "ਝੁੰਮਰ ਦੂਨਾਲੀ ਕਹਿ ਕੇ *ਅਸ਼ਕੇ",
    "ਨੀ ਮੋਢੇ ਪਾਉਂਦੀ",
]


def clusters(text):
    """Gurmukhi letters with their vowel signs and marks (and a subjoined letter after a virama) kept together, so
    typing on letter by letter never shows a loose mark."""
    import unicodedata
    out = []
    for c in text:
        if out and (unicodedata.category(c) in ("Mn", "Mc") or out[-1].endswith("\u0a4d")):
            out[-1] += c
        else:
            out.append(c)
    return out


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def word_slots(li):
    i0, i1, text = LYRICS[li]
    toks = text.split()
    gur = [g.lstrip("*") for g in GURMUKHI[li].split()]
    assert len(gur) == len(toks), (li, toks, gur)
    n = i1 - i0 + 1
    slots = [i0 + round(k * (n - 1) / max(1, len(toks) - 1)) for k in range(len(toks))] if len(toks) > 1 else [i0]
    return [(tok.lstrip("*"), tok.startswith("*"), W[s]["s"], g) for tok, s, g in zip(toks, slots, gur)]


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
        rom = " ".join(x[0] for x in g)
        txt = " ".join(x[3] for x in g).rstrip(",")
        if out and len(rom) <= 2:
            out[-1] = (out[-1][0] + " " + txt, out[-1][1], out[-1][2])
            continue
        out.append((txt, g[0][1], g[0][2]))
    return out


def tw(text, size):
    return GUR.getlength(text) * size / 100


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
    """A cut-out sticker in a slot w wide (and at most 1.15 w tall), centred in the slot."""
    from PIL import Image
    iw, ih = Image.open(os.path.join(ROOT, "assets", "img", "cut", f"{name}.png")).size
    fw = min(w, w * 1.15 * iw / ih)
    x, w = x + (w - fw) / 2, fw
    i = nid("ct")
    EV.append((t0, "paper"))
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
    EV.append((t0, "shutter"))
    js(f'tl.fromTo("#pr{n}", {{x: {R.choice([-120, 120])}}}, {{x: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')
    if t1 < DUR:
        js(f'tl.set("#pr{n}", {{opacity: 0}}, {t1:.3f});')


def star(x, y, size, t0, t1, color=INK, n=7, seed=0):
    i = nid("st")
    PAN.append(f'<svg class="el" id="{i}" viewBox="-50 -50 100 100" style="left:{x:.0f}px;top:{y:.0f}px;width:{size}px;height:{size}px;z-index:4">'
               f'<path d="{star_path(n, seed=seed)}" fill="{color}"/></svg>')
    show(f"#{i}", t0, t1)
    EV.append((t0, "tick"))
    js(f'tl.fromTo("#{i}", {{scale: 0, rotation: -40}}, {{scale: 1, rotation: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')


def label(text, style, x, y, size, rot, t, t1, mode="type", circle=False, anchor="center", z=5):
    """A label. mode: type (letter by letter behind a cursor block), slam (big, settles), pop."""
    i = nid("lb")
    size = min(size * 1.12, fit(text, 980, 999))          # the reference's labels run big, close to the frame edges
    w = tw(text, size) + size * .56
    left = x - w / 2 if anchor == "center" else x
    cl = clusters(text)
    letters = "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in cl)
    cur = '<span class="cur"></span>' if mode == "type" else ""
    PAN.append(f'<div class="lw" data-layout-allow-overlap style="left:{left:.0f}px;top:{y:.0f}px;transform:rotate({rot:.1f}deg);z-index:{z}">'
               f'<div class="lb {style}" id="{i}" style="font-size:{size:.0f}px">{letters}{cur}{CIRC if circle else ""}</div></div>')
    show(f"#{i}", t, t1)
    if "stamp" in style:
        EV.append((t, "stamp"))
    if mode == "type":
        n = len(cl)
        per = 3 if n > 8 else 2
        js(f'tl.set("#{i} .ch", {{display: "none"}}, {t - .001:.3f});')
        k = 0
        while k < n:
            js(f'tl.set("#{i} .ch:nth-child(-n+{min(n, k + per)})", {{display: "inline"}}, {t + (k // per) * STEP:.3f});')
            k += per
        done = t + (n // per + 1) * STEP
        js(f'tl.set("#{i} .cur", {{display: "none"}}, {done:.3f});')
    elif mode == "slam":
        EV.append((t, "slam"))
        js(f'tl.fromTo("#{i}", {{scale: 1.65}}, {{scale: 1, duration: .2, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
        done = t + .2
    else:
        EV.append((t, "pop"))
        js(f'tl.fromTo("#{i}", {{scale: 1.4}}, {{scale: 1, duration: .134, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
        done = t + .134
    if circle:
        EV.append((done + .05, "marker"))
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
    CAMKEYS.setdefault(si, []).append((t, fx, fy, s, rot, dur * .6))      # v5: quicker moves


def fit(text, maxw, size):
    return min(size, maxw / (tw(text, 100) / 100 + .56))


def extra_print(li, x, y, w, h, rot, t0, t1):
    """A second, smaller footage print (card2) in scenes that otherwise only have a cut-out: more of the clips."""
    if li in CARD2 and RECIPE[li] != "R5" and t0 < t1 - .2:
        card(2, x, y, w, h, rot, t0, t1)


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
    para(["ਅਸ਼ਕੇ · ਕਰਨ ਔਜਲਾ, ਮਰਸੀ", "ਲਿਰਿਕ ਐਡਿਟ:", "ਨੈਕਸਟ ਲੈਵਲ ਸੋਸ਼ਲ"], 110, y + 30, gs[min(1, len(gs) - 1)][2], b)
    extra_print(li, 620, 1380, 380, 450, 7, a + PERIOD * .5, b)
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
    scrap("black", 3, -60, 760, 1200, -5, kw[2], b)
    size = fit(kw[0], 1060, 330)
    after_n = len(gs) - ki - 1
    cutout(CUTOUT[li], 220, 860 + size * 1.25 + 150 * after_n, 640, 2, kw[2], b, z=2)   # under the word and its labels
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
    label(g0[0], "rb", 520, 520, size, -2, g0[2], b)
    cam(si, a, 540, 560, 1.45, -2, .01)
    rest = [g for g in gs[1:] if g is not kw]
    t_pull = rest[0][2] if rest else (kw[2] if kw is not g0 else a + .6)
    block(170, 960, 740, 560, t_pull, b)
    extra_print(li, 700, 70, 340, 400, 8, t_pull, b)
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
    extra_print(li, 30, 560, 300, 360, -8, t_cut + PERIOD / 2, b)
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
    kw = gs[-1]                         # the line's last word is the big one: the stack reads in sung order
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
    kw = gs[-1]                         # read top-down in sung order, the last word big
    rest = gs[:-1]
    scrap("black", 2, 260, 110, 480, 8, a, b)
    cam(si, a, 540, 760, 1.0, 0, .01)
    y = 330
    for k, (txt, key, t) in enumerate(rest):
        sz = fit(txt, 760, 112 if k == 0 else 108)
        label(txt, "rtyp" if k == 0 else "blk", 560 + (40, -40)[k % 2], y, sz, (-6, 3)[k % 2], t, b, z=6)
        cam(si, t, 560, y + 260, 1.1, -1, .3)
        y += sz * 1.3 + 24
    ksz = fit(kw[0], 900, 180)
    label(kw[0], "wht", 540, y + 10, ksz, -2, kw[2], b, circle=kw[1], z=6)
    cam(si, kw[2], 540, y + 300, 1.04, 0, .35)
    card(1, 140, y + ksz * 1.35 + 40, 760, 660, -3, a, b)


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
    extra_print(li, 660, 1060, 360, 430, 8, t2 + .1, b)
    flame(760, 1380, t2, b)
    label(g0[0], "redw", 540, 220, fit(g0[0], 800, 120), -4, t2, b, mode="pop", z=6)     # sung order, top-down
    for k, (txt, key, t) in enumerate(g for g in gs[1:] if g is not kw):
        label(txt, "blkr", 540, 420 + 150 * k, fit(txt, 900, 130), -2, t, b, z=6)
    if kw is not g0:
        label(kw[0], "stamp", 540, 1420, fit(kw[0], 1000, 250), -3, kw[2], b, z=5)
    cam(si, t2, 540, 880, 1.0, 0, .01)
    cam(si, t2 + .3, 540, 920, 1.04, 0, .5)


def still(name, x, y, w, h, rot, t0, t1):
    i = nid("sp")
    PAN.append(f'<div class="print el" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:2">'
               f'<img src="assets/img/photo/{name}.jpg" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
    show(f"#{i}", t0, t1)
    EV.append((t0, "shutter"))
    js(f'tl.fromTo("#{i}", {{x: 160}}, {{x: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')


def r9(si, a, b, li, gs):
    FLASH.append((a, "split"))
    if li in PRINT:
        still(PRINT[li], 600, 60, 440, 550, 7, a + .067, b)
    scrap("grey", 3, -160, -90, 1000, 5, a, b)
    scrap("grey", 1, 420, 1560, 860, -7, a, b)
    scrap("white", 2, -120, 880, 760, 3, a, b)
    kw = gs[-1] if gs else None         # sung order top-down, the last word stamped big at the bottom
    rest = gs[:-1]
    styles = ["redw", "red", "w3d", "blk"]
    y = 560 if len(rest) > 2 else 700
    cam(si, a, 470, y + 120, 1.15, -1, .01)
    for k, (txt, key, t) in enumerate(rest):                      # stacked down the page, each on its own line
        x = 540 + (-80, 80)[k % 2]
        sz = fit(txt, 820, (170, 140, 190, 130)[k % 4])
        label(txt, styles[k % 4], x, y, sz, (-2, 3, -2, -3)[k % 4], t, b, z=6)
        cam(si, t, (x + 540) / 2, y + sz * .6, 1.12, (-2, 3, -2, -3)[k % 4] * .3, .3)
        y += sz * 1.3 + 34
    if kw:
        sz = fit(kw[0], 1000, 290)
        label(kw[0], "stamp", 540, y + 10, sz, -2, kw[2], b, circle=kw[1], z=5)
        cam(si, kw[2], 540, y + sz * .6, 1.0, 0, .4)


def ending(si, a, b, li, gs):
    """Line 31 runs as type only up to "Ashke", then the end title takes over (end_card)."""
    t = W[153]["s"]
    r9(si, a, t, li, gs)
    FLASH.append((t - .067, "white"))


LOGO = ('<svg viewBox="0 0 1080 1080" width="1080" height="1080"><defs>'
        '<linearGradient id="ng" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#c4a6ff"/><stop offset=".45" stop-color="#ffffff"/>'
        '<stop offset="1" stop-color="#d9c8ff"/></linearGradient>'
        '<linearGradient id="sp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f1eaff"/><stop offset="1" stop-color="#b48cff"/></linearGradient>'
        '<radialGradient id="gl"><stop offset="0" stop-color="#b48cff" stop-opacity=".55"/><stop offset="1" stop-color="#b48cff" stop-opacity="0"/></radialGradient></defs>'
        '<circle id="lglow" cx="540" cy="560" r="420" fill="url(#gl)" opacity="0"/>'
        '<path id="ln" pathLength="1000" d="M357 825 L357 495 A65 65 0 0 1 484 472 L597 772 A66 66 0 0 0 722 756 L722 470" fill="none" '
        'stroke="url(#ng)" stroke-width="26" stroke-dasharray="1000" stroke-dashoffset="1000"/>'
        '<path id="lsp" d="M709 470 L722 345 L735 470 Z" fill="url(#sp)" opacity="0"/>'
        '<path id="lst" d="M722 258 Q727 295 764 300 Q727 305 722 342 Q717 305 681 300 Q717 295 722 258 Z" fill="#fff" '
        'opacity="0"/></svg>')


def logo_outro():
    """The owner's N logo, blended in with the collage: a black torn sheet tears across the paper, the logo's night
    violet underneath, the N draws on like the marker circles, the star pops, torn black paper frames it."""
    t = SONG
    SCREEN.append('<div id="endcard"><div id="ecglow"></div>' + f'<div id="ecl">{LOGO}</div>' +
                  '<img class="ecs" src="assets/img/scrap/black-3.png" style="left:-260px;top:-150px;width:900px;transform:rotate(8deg)" alt="">'
                  '<img class="ecs" src="assets/img/scrap/black-1.png" style="left:420px;top:1580px;width:900px;transform:rotate(-6deg)" alt="">'
                  '</div><img id="ectear" src="assets/img/scrap/black-0.png" alt="">')
    HIDE.extend(["#endcard", "#ectear"])
    js(f'tl.set("#ectear", {{opacity: 1}}, {t - .2:.3f});')
    js(f'tl.fromTo("#ectear", {{y: 2400, rotation: -8}}, {{y: -2600, rotation: 6, duration: .67, ease: "steps(10)", immediateRender: false}}, {t - .2:.3f});')
    js(f'tl.set("#endcard", {{opacity: 1}}, {t + .07:.3f});')
    js(f'tl.set("#ectear", {{opacity: 0}}, {t + .47:.3f});')
    EV.extend([(t - .2, "tear"), (t + .3, "logo")])
    js(f'tl.to("#ln", {{strokeDashoffset: 0, duration: .9, ease: "steps(14)"}}, {t + .3:.3f});')
    js(f'tl.set("#lsp", {{opacity: 1}}, {t + 1.2:.3f});')
    js(f'tl.fromTo("#lsp", {{scaleY: 0, svgOrigin: "722 470"}}, {{scaleY: 1, duration: .2, ease: "steps(3)", immediateRender: false}}, {t + 1.2:.3f});')
    js(f'tl.set("#lst", {{opacity: 1}}, {t + 1.36:.3f});')
    js(f'tl.fromTo("#lst", {{scale: 0, rotation: -90, svgOrigin: "722 300"}}, {{scale: 1, rotation: 0, duration: .27, ease: "steps(4)", immediateRender: false}}, {t + 1.36:.3f});')
    js(f'tl.to("#lglow", {{opacity: 1, duration: .4, ease: "steps(6)"}}, {t + 1.36:.3f});')
    EV.append((t + 1.36, "sparkle"))
    for k in range(6):                                         # the star twinkles
        js(f'tl.set("#lst", {{scale: {1.12 if k % 2 == 0 else 1}, svgOrigin: "722 300"}}, {t + 1.8 + k * .2:.3f});')
    js(f'tl.to("#endcard", {{opacity: 0, duration: .4, ease: "steps(6)"}}, {DUR - .45:.3f});')


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
               + "".join(f'<span class="ch">{c}</span>' for c in clusters("ਅਸ਼ਕੇ")) + f'<span class="cur"></span>{CIRC}</div></div>')
    show("#logo", t + .067, DUR)
    js(f'tl.set("#logo .ch", {{display: "none"}}, {t + .066:.3f});')
    for k in range(len(clusters("ਅਸ਼ਕੇ"))):
        js(f'tl.set("#logo .ch:nth-child(-n+{k + 1})", {{display: "inline"}}, {t + .067 + k * STEP:.3f});')
        EV.append((t + .067 + k * STEP, "type"))
    EV.append((t + .55, "marker"))
    js(f'tl.set("#logo .cur", {{display: "none"}}, {t + .067 + 6 * STEP:.3f});')
    js(f'tl.fromTo("#logo .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .5, ease: "steps(8)", immediateRender: false}}, {t + .55:.3f});')
    label("ਕਰਨ ਔਜਲਾ · ਮਰਸੀ", "blk", 540, 1180, 70, 1.5, line_times(32)[0], DUR, z=6)


# one free spot per recipe for the line's element (board coordinates, top-left of a 230 px sticker)
ICON_AT = {"R1": (800, 1500, 8), "R2": (60, 300, -8), "R3": (790, 330, 10), "R4": (90, 1100, -10), "R5": (810, 1520, 8),
           "R6": (60, 1540, -6), "R7": (60, 300, -8), "R8": (90, 960, -10), "R9": (780, 1460, 10), "END": (780, 1460, 10)}


def lyric_icons():
    """One element per line, popping in on the line's keyword (or its middle word) and staying to the cut."""
    for si, (a, b, li) in enumerate(scenes()):
        if li not in ICON:
            continue
        gs = groups_of(li)
        if not gs:
            continue
        kws = [g for g in gs if g[1]]
        t = (kws[-1] if kws else gs[len(gs) // 2])[2]
        rec = RECIPE[li]
        if rec == "R8" and len(gs) > 1:
            t = max(t, gs[1][2])
        if li == 31:
            b = W[153]["s"] - .067
        if t >= b - .15:
            t = max(a + .2, b - .5)
        x, y, rot = ICON_AT[rec]
        i = nid("ic")
        PAN.append(f'<div class="el" id="{i}" style="left:{x}px;top:{y}px;width:230px;height:230px;z-index:7;transform:rotate({rot}deg)">'
                   f'{svg(ICON[li])}<b class="itag">{WORD[li]}</b></div>')
        show(f"#{i}", t, b)
        EV.append((t, "pop"))
        js(f'tl.fromTo("#{i}", {{scale: 1.6, rotation: {rot - 20}}}, {{scale: 1, rotation: {rot}, duration: .2, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
        # a little stop-motion wobble while it sits there
        k, tt = 0, t + .27
        while tt < b - .07:
            js(f'tl.set("#{i}", {{rotation: {rot + (2.5 if k % 2 else -2.5)}}}, {tt:.3f});')
            tt, k = tt + PERIOD / 2, k + 1


def transition_frames():
    """Two single-frame stills (one 15 fps step each) right before the cut: the frame pacing of the transitions."""
    k = 0
    for si, (a, b, li) in enumerate(scenes()):
        if si == 0 or li == 32 or RECIPE[li] in ("R4", "R8", "R9"):
            continue
        for j in range(3):
            shot = TRANS_POOL[k % len(TRANS_POOL)]
            k += 1
            i = nid("tf")
            rot = (-4, 5, -2)[j]
            w = (820, 700, 900)[j]
            SCREEN.append(f'<div class="tframe" id="{i}" style="left:{540 - w / 2:.0f}px;top:{960 - w * 1.25 / 2:.0f}px;width:{w}px;height:{w * 1.25:.0f}px;'
                          f'transform:rotate({rot}deg)"><img src="assets/img/photo/frame_{shot}.jpg" alt=""></div>')
            t0 = a - (3 - j) / 30
            show(f"#{i}", t0, t0 + 1 / 30)


# ------------------------------------------------------------------------------------------------ camera
def ease_out(u, p=3):
    return 1 - (1 - max(0, min(1, u))) ** p


DIRS = [(0, 1), (0, 1), (1, .3), (0, 1), (-.8, .6), (0, -1), (.7, .7), (0, 1), (-1, 0), (0, 1), (.6, .8), (1, 0)]


def camera():
    """Sampled at 15 fps, modelled on the reference's measured camera (phase correlation, frame by frame): it never
    stops. Inside a scene the focus glides through the scene's keys on a time-aware Hermite spline, arriving at each
    label just after it lands, and keeps drifting past the last one along the scene's direction (the reference holds
    at 300-450 px/s). Every cut sits at peak speed: the camera accelerates into it along the next scene's direction
    and comes out of the next one decelerating (expo, tau 0.1 s), so a cut reads as one whip. Fast steps get a
    directional motion blur like the reference. A small punch-in on each beat. From the end title on, it rests."""
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
        run = min(320, 380 * (b - pts[-1][0]))                    # keep drifting to the cut
        pts.append((b + .001, lx + d[0] * run, ly + d[1] * run, ls, lr))
        plans.append(dict(a=a, b=b, li=li, d=d, pts=pts))
    tend = W[153]["s"] - .067
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
        e = math.exp(-u / TAU)                                    # whip in, decelerating
        fx -= p["d"][0] * E * e
        fy -= p["d"][1] * E * e
        rot += 3 * e * (1 if si % 2 else -1)
        if si + 1 < len(plans) and p["b"] < tend:                 # whip out, accelerating into the cut
            nd = plans[si + 1]["d"]
            x = math.exp(-max(0, p["b"] - t) / TAU)
            fx += nd[0] * X * x
            fy += nd[1] * X * x
            rot += 2 * x * (1 if si % 2 else -1)
        return fx, fy, s, rot

    g = random.Random(9)
    blurred = False
    for f in range(int(DUR * 15)):
        t = f / 15
        if t >= tend:
            u = t - tend
            js(f'tl.set("#pan", {{x: {g.uniform(-1, 1):.1f}, y: {g.uniform(-1, 1):.1f}}}, {t:.3f});')
            js(f'tl.set("#cam", {{scale: {1 + .03 * u:.4f}, rotation: 0}}, {t:.3f});')
            if blurred:
                js(f'tl.set("#cam", {{filter: "none"}}, {t:.3f});')
                blurred = False
            continue
        si = max(i for i, p in enumerate(plans) if p["a"] <= t + 1e-6)
        fx, fy, s, rot = focus(si, t)
        px, py, _, _ = focus(si, max(plans[si]["a"], t - STEP)) if t - STEP >= plans[si]["a"] else focus(si, t + STEP)
        vx, vy = (fx - px) * s, (fy - py) * s
        if t - STEP < plans[si]["a"]:
            vx, vy = -vx, -vy
        lb = max([bt for bt in BEATS["beats"] if bt - OFFSET <= t + 1e-6] or [-9]) - OFFSET
        s *= 1 + .025 * math.exp(-(t - lb) / .09)                  # a punch-in on every beat
        fx += g.uniform(-1, 1)
        fy += g.uniform(-1, 1)
        js(f'tl.set("#pan", {{x: {540 - fx:.1f}, y: {960 - fy:.1f}}}, {t:.3f});')
        js(f'tl.set("#cam", {{scale: {s * 1.06:.4f}, rotation: {rot:.2f}}}, {t:.3f});')
        sp = math.hypot(vx, vy)
        if sp > 90:                                               # directional motion blur on fast steps
            k = min(13, sp * .045)
            js(f'tl.set("#mbg", {{attr: {{stdDeviation: "{abs(vx) / sp * k:.1f} {abs(vy) / sp * k:.1f}"}}}}, {t:.3f});')
            if not blurred:
                js(f'tl.set("#cam", {{filter: "url(#mb)"}}, {t:.3f});')
                blurred = True
        elif blurred:
            js(f'tl.set("#cam", {{filter: "none"}}, {t:.3f});')
            blurred = False


def flashes():
    """One-step accents, as in the reference: colour invert, white, black/white split."""
    SCREEN.append('<div id="flash"></div><div id="split"><i></i></div>')
    HIDE.extend(["#flash", "#split"])
    for t, kind in FLASH:
        EV.append((t, {"invert": "glitch", "white": "flash", "split": "click"}[kind]))
        if kind == "invert":
            js(f'tl.set("#fx", {{filter: "invert(1)"}}, {t:.3f});')            # red goes teal, like the reference
            js(f'tl.set("#fx", {{filter: "none"}}, {t + STEP:.3f});')
        elif kind == "white":
            js(f'tl.set("#flash", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {t + STEP:.3f});')
        elif kind == "split":
            js(f'tl.set("#split", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#split", {{opacity: 0}}, {t + STEP:.3f});')


CSS = f"""
@font-face {{ font-family: "Anek C"; font-weight: 800; src: url("assets/fonts/AnekGurmukhi/AnekGurmukhi-Condensed-800.ttf"); }}
@font-face {{ font-family: "Anek"; font-weight: 600; src: url("assets/fonts/AnekGurmukhi/AnekGurmukhi-600.ttf"); }}
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
.lb {{ position: relative; display: inline-block; font: 800 120px/1.18 "Anek C"; white-space: nowrap; opacity: 0;
  padding: .06em .28em .02em; }}
.lb .ch {{ display: inline; }}
.lb .cur {{ display: inline-block; width: .45em; height: .8em; margin-left: .06em; vertical-align: -.02em; background: rgba(95,92,88,.9); }}
.blk {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, {INK}; color: #f1eee8; box-shadow: 0 12px 22px rgba(0,0,0,.28); }}
.wht {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, #f3f1ec; color: {INK}; box-shadow: 0 12px 22px rgba(0,0,0,.25); }}
.redw {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, #f3f1ec; color: {RED}; box-shadow: 0 12px 22px rgba(0,0,0,.25); }}
.redw .cur {{ background: {RED}; }}
.red {{ background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, {RED}; color: #fff; box-shadow: 0 12px 22px rgba(0,0,0,.25); }}
.rb {{ background: {RED}; color: #fff; text-shadow: 4px 4px 0 {INK}; box-shadow: 18px 16px 0 {INK}; }}
.blkr {{ background: {INK}; color: #fff; box-shadow: 16px 18px 0 {RED}; }}
.rtyp {{ background: none; color: {RED}; padding: 0; -webkit-mask-image: url(assets/img/tex/grunge.png); mask-image: url(assets/img/tex/grunge.png); }}
.stamp {{ background: none; color: #1c1b1a; padding: 0; line-height: 1.12;
  -webkit-mask-image: url(assets/img/tex/grunge.png); mask-image: url(assets/img/tex/grunge.png); -webkit-mask-size: 520px auto; mask-size: 520px auto; }}
.stamp .cur {{ background: rgba(60,58,55,.55); }}
.w3d {{ background: none; color: #f6f4ef; padding: 0; -webkit-text-stroke: 2px #2a2a2a;
  text-shadow: 1px 1px 0 #cfcac2, 2px 2px 0 #bdb7ae, 3px 3px 0 #a7a097, 4px 4px 0 #8f887f, 5px 5px 0 #77706a, 6px 6px 0 #5e5852, 7px 7px 0 #48433e, 10px 12px 10px rgba(0,0,0,.5); }}
.r3d {{ background: none; color: {RED}; padding: 0; -webkit-text-stroke: 2px #6e0b0f;
  text-shadow: 1px 1px 0 #a5121a, 2px 2px 0 #8c0f16, 3px 3px 0 #730c12, 4px 4px 0 #5a090e, 5px 5px 0 #40070a, 6px 6px 0 #2a0507, 9px 11px 10px rgba(0,0,0,.45); }}
.rlet {{ background: none; color: {RED}; padding: 0; text-shadow: 5px 5px 0 rgba(22,22,22,.85);
  -webkit-mask-image: url(assets/img/tex/grunge.png); mask-image: url(assets/img/tex/grunge.png); -webkit-mask-size: 700px auto; mask-size: 700px auto; }}
.fill {{ color: transparent; padding: 0; line-height: 1.12; background-size: cover; background-position: 50% 40%;
  -webkit-background-clip: text; background-clip: text; -webkit-text-stroke: 5px {INK}; filter: drop-shadow(8px 10px 0 rgba(22,22,22,.85)); }}
{"".join(f'.f{li} {{ background-image: url(assets/img/photo/fill_{li}.jpg); }}' for li in FILL)}
.ghost {{ font: 800 250px/1.15 "Anek C"; color: rgba(40,36,32,.16); white-space: nowrap; opacity: 0; }}
.para {{ font: 600 36px/1.3 "Anek"; color: #2a2724; z-index: 5; }}
.itag {{ position: absolute; left: 50%; top: 212px; transform: translateX(-50%) rotate(-3deg); font: 800 52px/1.2 "Anek C"; white-space: nowrap;
  background: {RED}; color: #fff; padding: 0 .3em; box-shadow: 0 8px 14px rgba(0,0,0,.25); }}
.rline {{ border: 9px solid {RED}; z-index: 2; }}
.redblk {{ z-index: 2; background: repeating-linear-gradient(90deg, rgba(0,0,0,.25) 0 3px, rgba(0,0,0,0) 3px 9px),
  radial-gradient(ellipse at 40% 40%, #a3121a, #4a0609); }}
.logo {{ font: 800 170px/1.15 "Anek C"; color: {RED}; padding: .04em .34em .02em;
  background: url(assets/img/tex/speckle.png) 0 0 / 300px auto, #f5f3ee; box-shadow: 0 16px 26px rgba(0,0,0,.28); }}
.logo .cur {{ background: rgba(90,88,85,.8); }}
.circ {{ position: absolute; left: -10%; top: -22%; width: 120%; height: 144%; overflow: visible; pointer-events: none; }}
.circ path {{ fill: none; stroke: {BLUE}; stroke-width: 5.5; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
.tframe {{ position: absolute; z-index: 15; opacity: 0; background: #f3f1ec; padding: 18px; box-shadow: 0 18px 40px rgba(0,0,0,.45); }}
.tframe img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#endcard {{ position: absolute; inset: 0; z-index: 17; opacity: 0; overflow: hidden;
  background: radial-gradient(ellipse 70% 45% at 30% 30%, rgba(101,22,199,.35), rgba(0,0,0,0) 70%),
  radial-gradient(ellipse 70% 45% at 75% 75%, rgba(75,6,193,.3), rgba(0,0,0,0) 70%), #08060f; }}
#ecl {{ position: absolute; left: 0; top: 420px; width: 1080px; height: 1080px; }}
.ecs {{ position: absolute; height: auto; filter: brightness(.55); }}
#ectear {{ position: absolute; left: -760px; top: -200px; width: 2600px; height: auto; z-index: 18; opacity: 0; }}
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
        gs = [("ਅਸ਼ਕੇ", False, .56), ("ਕਰਨ ਔਜਲਾ", True, .8)] if li < 0 else groups_of(li)   # ASHKE lands on the drop
        builders[RECIPE[li]](si, a, b, li, gs)
    end_card()
    lyric_icons()
    transition_frames()
    camera()
    flashes()
    for si, (a, b, li) in enumerate(scenes()):                  # a whoosh on every camera whip into the next scene
        if 0 < si and li != 32 and a < SONG:
            EV.append((a - .2, "whoosh"))
    json.dump(sorted(EV), open(os.path.join(ROOT, "plan", "events.json"), "w"))
    g = random.Random(3)
    for f in range(int(DUR * 15)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 15:.3f});')
    gl = random.Random(4)
    grid = "".join(f'<line x1="{x + gl.uniform(-8, 8):.0f}" y1="-20" x2="{x + gl.uniform(-40, 40):.0f}" y2="3920"/>' for x in range(260, 2600, 390)) + \
           "".join(f'<line x1="-20" y1="{y + gl.uniform(-8, 8):.0f}" x2="2620" y2="{y + gl.uniform(-40, 40):.0f}"/>' for y in range(200, 3900, 420))
    prints = "".join(f'<div class="print" id="pr{n}"><video id="cv{n}" class="clip" src="assets/video/card{n}.mp4" data-start="0" '
                     f'data-duration="{SONG}" data-track-index="{n}" muted playsinline></video><i></i></div>' for n in (1, 2))
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
    <svg width="0" height="0" style="position:absolute"><filter id="mb" x="-5%" y="-5%" width="110%" height="110%">
      <feGaussianBlur id="mbg" stdDeviation="0 0"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{FW}" data-height="{FH}">
      <div id="fx">
        <div id="cam"><div id="pan">
          <div id="paper"></div>
          <svg id="grid" viewBox="0 0 2600 3900">{grid}</svg>
          <div id="board">
            {prints}
            {"".join(PAN)}
          </div>
        </div></div>
        <div id="blinds"></div>
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
