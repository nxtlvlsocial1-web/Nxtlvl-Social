"""Political opinion reel (Diwali, "buy only from tilak-wearing sellers" rebuttal), 9:16, 1080x1920. Writes index.html.

Owner's brief:
- Talking head, gaps trimmed (build/tight.py), the voice cleaned to a studio sound, no music, no sound effects.
- The Surrender ad's layout and captions: split screens (graphics on top, her face below, a black box with white
  Hinglish words on the seam) and full-frame face moments (a script line over a big condensed word, red on key words).
- The Ashke edit's paper format for the graphics: whitish crumpled paper with grid lines, torn red / black / white
  paper, black-and-white photo prints with tape, condensed labels that type on, red marker circles, motion that steps
  on twos (15 fps), torn-sheet wipes between the boards.
- The political-explainer reference (reference/ref_political.mp4): each claim gets its picture or document on the top
  half while she talks underneath.
Images: the owner's (assets/img/ref, assets/img/logos; not in git). The photo the owner labelled Mohammad Ali Road
is Metro House / Cafe Mondegar on Colaba Causeway, so that board is drawn as a map until a right photo comes in.

python3 build/generate.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hinglish import roman  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
W = json.load(open(os.path.join(ROOT, "plan", "words_tight.json")))
VDUR = 135.767
DUR = round(VDUR + 1.0, 3)          # the last board holds a second on her last frame
A, HIDE, TOP, POST = [], [], [], []
NID = [0]


def T(i):
    return W[i]["s"]


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def word(i):
    return roman(W[i]["text"])


def show(sel, t0, t1):
    js(f'tl.set("{sel}", {{opacity: 1}}, {max(0, t0):.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')
    HIDE.append(sel)


def ST(d, ease="expo.out"):
    """An ease that keeps its curve but steps on twos (15 fps), like the Ashke edit."""
    return f'ST({max(2, round(d * 15))}, "{ease}")'


# ------------------------------------------------------------------------------------------------ sections
# (kind, first word, board): split = board on top + face below; full = the face fills the frame
SECS_DEF = [("split", 1, "quote"), ("full", 24, None), ("split", 32, "rane"), ("full", 43, None),
            ("split", 57, "ch1"), ("split", 64, "crackers"), ("split", 89, "mar"), ("split", 105, "kandil"),
            ("split", 123, "attar"), ("full", 139, None), ("split", 159, "crawford"), ("split", 197, "ch2"),
            ("split", 204, "tanishq"), ("split", 230, "croma"), ("split", 247, "wz"), ("split", 268, "tata"),
            ("full", 295, None), ("split", 329, "secular"), ("split", 345, "names")]


def sec_times():
    out = []
    for k, (kind, a, board) in enumerate(SECS_DEF):
        ta = 0.0 if k == 0 else round(T(a) - .06, 3)
        b = SECS_DEF[k + 1][1] if k + 1 < len(SECS_DEF) else len(W)
        tb = round(T(SECS_DEF[k + 1][1]) - .06, 3) if k + 1 < len(SECS_DEF) else DUR
        out.append((kind, ta, tb, a, b, board))
    return out


SECS = sec_times()
RED = {15, 19, 20, 21, 50, 56, 61, 70, 89, 90, 91, 100, 116, 126, 153, 154, 192, 193, 194, 202, 229, 245, 265, 267, 285,
       289, 293, 313, 318, 319, 337, 365, 366}

# ------------------------------------------------------------------------------------------------ board pieces
SCRAP = {"red": 4, "black": 4, "grey": 4, "white": 4}


def group(board, t0, t1):
    g = f"g_{board}"
    TOP.append(f'<div class="grp" id="{g}">')
    show(f"#{g}", t0, t1)
    return g


def end_group():
    TOP.append("</div>")


def slap(i, t, rot=0, d=.36, frm=1.35, dx=0, dy=0):
    js(f'tl.fromTo("#{i}", {{opacity: 0, scale: {frm}, rotation: {rot + 9}, x: {dx}, y: {dy}}}, {{opacity: 1, scale: 1, rotation: {rot}, x: 0, y: 0, '
       f'duration: {d}, ease: {ST(d)}, immediateRender: false}}, {t:.3f});')


def scrap(color, n, x, y, w, rot, t, z=1, flip=False):
    i = nid("s")
    TOP.append(f'<img class="scrap" id="{i}" src="assets/img/paper/scrap/{color}-{n % SCRAP[color]}.png" '
               f'style="left:{x}px;top:{y}px;width:{w}px;z-index:{z};transform:rotate({rot}deg){" scaleX(-1)" if flip else ""}" alt="">')
    slap(i, t, rot, d=.3, frm=1.2)
    return i


def prt(src, x, y, w, h, rot, t, z=3, bw=True, tape=True, pos="50% 50%", color_at=None):
    """A photo print: white border, tape, black-and-white photocopy."""
    i = nid("p")
    TOP.append(f'<div class="print{" bw" if bw else ""}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">'
               f'<img src="{src}" style="object-position:{pos}" alt="">{"<i class=tape></i>" if tape else ""}</div>')
    slap(i, t, rot, d=.4, frm=1.3)
    js(f'tl.to("#{i}", {{rotation: {rot - 1.2}, y: -8, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: 3}}, {t + .45:.3f});')
    if color_at is not None:
        js(f'tl.to("#{i} img", {{filter: "grayscale(0) contrast(1.05)", duration: .4, ease: {ST(.4, "power2.out")}}}, {color_at:.3f});')
    return i


def label(text, x, y, t, kind="black", size=70, rot=0, z=6, type_on=True):
    """A condensed label on tape that types on letter by letter."""
    i = nid("l")
    chars = "".join(f'<span class="c">{c if c != " " else "&nbsp;"}</span>' for c in text)
    TOP.append(f'<div class="lab {kind}" id="{i}" style="left:{x}px;top:{y}px;font-size:{size}px;z-index:{z};transform:rotate({rot}deg)">{chars}</div>')
    js(f'tl.fromTo("#{i}", {{opacity: 0, scaleX: .2}}, {{opacity: 1, scaleX: 1, duration: .2, ease: {ST(.2, "power3.out")}, immediateRender: false}}, {t:.3f});')
    if type_on:
        js(f'tl.fromTo("#{i} .c", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: {min(.045, .5 / max(1, len(text))):.3f}, immediateRender: false}}, {t + .05:.3f});')
    return i


def stamp(text, x, y, t, rot=-8, size=110, z=8):
    i = nid("st")
    TOP.append(f'<div class="stamp" id="{i}" style="left:{x}px;top:{y}px;font-size:{size}px;z-index:{z}">{text}</div>')
    js(f'tl.fromTo("#{i}", {{opacity: 0, scale: 2.4, rotation: {rot - 6}}}, {{opacity: 1, scale: 1, rotation: {rot}, duration: .26, ease: {ST(.26, "back.out(2)")}, '
       f'immediateRender: false}}, {t:.3f});')
    return i


def draw(svg_paths, x, y, w, h, vb, t, d=.6, z=5, stroke="#e3202f", sw=9, cls="doo"):
    """Hand-drawn strokes that draw themselves on (stepped)."""
    i = nid("d")
    paths = "".join(f'<path d="{p}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>' for p in svg_paths)
    TOP.append(f'<svg class="{cls}" id="{i}" viewBox="{vb}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};'
               f'stroke:{stroke};stroke-width:{sw}">{paths}</svg>')
    js(f'tl.set("#{i}", {{opacity: 1}}, {t:.3f});')
    js(f'tl.fromTo("#{i} path", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: {d}, ease: {ST(d, "power2.inOut")}, stagger: {d * .6:.2f}, '
       f'immediateRender: false}}, {t:.3f});')
    HIDE.append(f"#{i}")
    return i


def circle(x, y, w, h, t, z=7):
    """A red marker circle drawn round something."""
    return draw(["M 60 18 C 150 -6 262 20 288 92 C 312 160 236 214 140 210 C 52 206 4 160 14 100 C 22 52 70 26 120 22"],
                x, y, w, h, "0 0 300 230", t, d=.45, z=z, sw=8)


def logo(name, x, y, w, h, t, rot=0, z=5):
    i = nid("lg")
    TOP.append(f'<div class="logo" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">'
               f'<img src="assets/img/logos/{name}_rgba.png" alt="{name}"><i class="tape"></i></div>')
    slap(i, t, rot, d=.34, frm=1.5)
    return i


def card(html, x, y, w, t, rot=0, z=4, cls="note"):
    i = nid("n")
    TOP.append(f'<div class="{cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z}">{html}</div>')
    slap(i, t, rot, d=.38, frm=1.25)
    return i


def words_on(sel_prefix, idx):
    """Words of a card that appear as she says them."""
    for j in idx:
        js(f'tl.fromTo("#{sel_prefix}{j}", {{opacity: 0, y: 10}}, {{opacity: 1, y: 0, duration: .12, ease: {ST(.12, "power2.out")}, immediateRender: false}}, {T(j) - .03:.3f});')


def marker(sel, t, d=.3):
    js(f'tl.fromTo("{sel}", {{backgroundSize: "0% 100%"}}, {{backgroundSize: "100% 100%", duration: {d}, ease: {ST(d, "power2.out")}, immediateRender: false}}, {t:.3f});')


def chapter(board, num, title, lead, ta, tb, a, title_at):
    g = group(board, ta, tb)
    scrap("black", 1, 520, 300, 560, -6, ta + .05, z=1)
    i = nid("num")
    TOP.append(f'<div class="num" id="{i}">{num}</div>')
    slap(i, ta + .02, -4, d=.4, frm=1.6)
    label(lead, 90, 250, ta + .1, kind="white", size=46, rot=-2)
    label(title, 400, 470, title_at, kind="black", size=78, rot=-3)
    draw(["M 30 40 C 200 10 420 60 600 30"], 400, 590, 560, 70, "0 0 640 70", title_at + .3, d=.35)
    end_group()


# ------------------------------------------------------------------------------------------------ the boards
def boards():
    S = {s[5]: s for s in SECS if s[5]}

    # 1. The hook: her quote of the minister, typed on as she says it, the key words marked
    _, ta, tb, a, b, _ = S["quote"]
    group("quote", ta, tb)
    scrap("red", 0, 40, 90, 640, -8, ta + .05, z=1)
    scrap("grey", 2, 560, 520, 520, 7, ta + .12, z=1)
    words = [j for j in range(1, 24)]
    body = " ".join(f'<span class="qw{" mk" if j in (15, 19, 20, 21) else ""}" id="qw{j}">{word(j)}</span>' for j in words)
    card(f'<div class="qmark">&ldquo;</div><div class="qtxt">{body}</div><div class="qby">&mdash; a Maharashtra cabinet minister</div>',
         120, 150, 840, ta + .08, rot=-2, z=3, cls="note quote")
    words_on("qw", words)
    marker("#qw15", T(15) + .05)
    for j in (19, 20, 21):
        marker(f"#qw{j}", T(j) + .02, .18)
    end_group()
    js('tl.set(".qby", {opacity: 0}, 0);')
    js(f'tl.to(".qby", {{opacity: 1, duration: .2}}, {T(23) + .2:.3f});')

    # 2. Who said it: the minister's photo as a black-and-white print, his name types on, circled
    _, ta, tb, a, b, _ = S["rane"]
    group("rane", ta, tb)
    scrap("red", 1, 30, 120, 600, -10, ta + .03, z=1)
    prt("assets/img/ref/speaker_face.jpg", 90, 140, 480, 560, -4, ta + .06, z=3)
    label("SITTING CABINET MINISTER", 610, 240, T(37) - .05, kind="white", size=36, rot=3, z=9)
    label("MAHARASHTRA", 630, 310, T(35), kind="red", size=58, rot=3, z=9)
    label("NITESH RANE", 540, 420, T(40) - .04, kind="black", size=92, rot=-3, z=9)
    circle(60, 110, 560, 460, T(40) + .05)
    draw(["M 40 120 C 120 40 200 20 300 30", "M 300 30 L 262 8 M 300 30 L 268 58"], 560, 600, 330, 140, "0 0 320 140", T(41) + .1, d=.35)
    end_group()

    # 3. Chapter one
    _, ta, tb, a, b, _ = S["ch1"]
    chapter("ch1", "01", "MUSLIM COMMUNITY", "LET'S START WITH", ta, tb, a, T(61) - .04)

    # 4. Firecrackers: drawn rockets and sparkle bursts, Mumbai, the biggest market
    _, ta, tb, a, b, _ = S["crackers"]
    group("crackers", ta, tb)
    scrap("white", 0, 60, 120, 960, -3, ta + .03, z=1)
    burst = []
    import math
    for cx, cy, r in [(230, 300, 120), (560, 220, 90), (820, 330, 130)]:
        for k in range(10):
            ang = k / 10 * 6.283
            burst.append(f"M {cx + math.cos(ang) * r * .35:.0f} {cy + math.sin(ang) * r * .35:.0f} L {cx + math.cos(ang) * r:.0f} {cy + math.sin(ang) * r:.0f}")
    draw(burst[:10], 0, 0, 1080, 960, "0 0 1080 960", T(70) - .05, d=.35, z=4)
    draw(burst[10:20], 0, 0, 1080, 960, "0 0 1080 960", T(70) + .2, d=.35, z=4, stroke="#111")
    draw(burst[20:], 0, 0, 1080, 960, "0 0 1080 960", T(71), d=.35, z=4)
    draw(["M 230 300 C 240 420 250 560 260 700", "M 820 330 C 800 450 790 560 780 700"], 0, 0, 1080, 960, "0 0 1080 960", T(70) - .3, d=.3, z=3,
         stroke="#111", sw=6)
    label("PATAAKHE", 330, 470, T(70), kind="black", size=100, rot=-3)
    label("MUMBAI", 140, 640, T(76), kind="white", size=70, rot=2)
    stamp("SABSE BADA MARKET", 250, 690, T(85) - .03, rot=-5, size=78)
    end_group()

    # 5. Mohammad Ali Road (drawn as a map: the owner's photo is of Colaba, not this road)
    _, ta, tb, a, b, _ = S["mar"]
    group("mar", ta, tb)
    card('<svg class="map" viewBox="0 0 700 520"><path d="M 30 420 C 200 380 380 330 680 120"/><path d="M 120 40 L 260 500"/>'
         '<path d="M 420 30 L 520 500"/><path d="M 20 210 C 260 240 460 230 690 300"/><path class="main" d="M 60 470 C 250 360 420 280 650 90"/></svg>',
         150, 130, 780, ta + .04, rot=2, z=2, cls="note mapc")
    i = nid("pin")
    TOP.append(f'<div class="pin" id="{i}" style="left:500px;top:250px"><svg viewBox="0 0 60 80"><path d="M30 78 C 30 78 4 46 4 28 A 26 26 0 1 1 56 28 '
               f'C 56 46 30 78 30 78 Z"/><circle cx="30" cy="28" r="10"/></svg></div>')
    js(f'tl.fromTo("#{i}", {{opacity: 0, y: -260}}, {{opacity: 1, y: 0, duration: .4, ease: {ST(.4, "bounce.out")}, immediateRender: false}}, {T(89) - .05:.3f});')
    label("MOHAMMAD ALI ROAD", 130, 560, T(89) - .02, kind="black", size=88, rot=-2)
    label("MUMBAI", 820, 470, T(91) + .1, kind="white", size=46, rot=4)
    stamp("ZYAADATAR MUSLIM-OWNED", 250, 680, T(99) - .03, rot=-5, size=58)
    end_group()

    # 6. Kandeel: the lantern stall as a print that turns to colour on "kandeel"
    _, ta, tb, a, b, _ = S["kandil"]
    group("kandil", ta, tb)
    scrap("black", 2, 520, 140, 520, 8, ta + .03, z=1)
    prt("assets/img/ref/attar_kandil_lanterns_pune.jpg", 110, 140, 760, 520, -3, ta + .05, z=3, color_at=T(116) - .05)
    label("KANDEEL", 560, 640, T(116) - .03, kind="red", size=100, rot=3)
    label("LANTERNS", 600, 770, T(119), kind="white", size=56, rot=-2)
    end_group()

    # 7. The Attar community of Pune, generations of makers
    _, ta, tb, a, b, _ = S["attar"]
    group("attar", ta, tb)
    scrap("red", 2, 60, 360, 960, -3, ta + .03, z=1)
    prt("assets/img/ref/attar_kandil_lanterns_pune.jpg?v=2", 640, 90, 360, 250, 6, ta + .02, z=2, bw=False)
    label("PUNE", 110, 150, T(124) - .04, kind="white", size=80, rot=-3)
    label("ATTAR COMMUNITY", 110, 270, T(126) - .04, kind="black", size=96, rot=-2)
    person = "M 50 30 A 18 18 0 1 1 50.1 30 M 50 52 L 50 110 M 50 70 L 22 92 M 50 70 L 78 92 M 50 110 L 30 150 M 50 110 L 70 150"
    for k, (x, sz, tk) in enumerate([(160, 230, T(130)), (440, 200, T(131) + .1), (700, 170, T(133))]):
        draw([person], x, 420 + (230 - sz), sz * .66, sz, "0 0 100 160", tk, d=.4, z=4, stroke="#fff", sw=7)
    draw(["M 120 680 L 960 680", "M 960 680 L 925 658 M 960 680 L 925 702"], 0, 0, 1080, 960, "0 0 1080 960", T(130), d=.5, z=4, stroke="#fff", sw=7)
    label("PEEDHIYON SE", 380, 720, T(133) - .03, kind="white", size=60, rot=-1)
    end_group()

    # 8. Crawford Market: the print, half of Mumbai, Bohri Muslims
    _, ta, tb, a, b, _ = S["crawford"]
    group("crawford", ta, tb)
    scrap("grey", 1, 30, 80, 700, -6, ta + .03, z=1)
    prt("assets/img/ref/crawford_market.jpg", 90, 110, 900, 560, 2, ta + .05, z=3)
    label("CRAWFORD MARKET", 120, 680, ta + .2, kind="black", size=96, rot=-2)
    i = nid("pie")
    TOP.append(f'<div class="pie" id="{i}"><svg viewBox="0 0 200 200"><circle class="pbg" cx="100" cy="100" r="70"/>'
               f'<circle class="pfg" cx="100" cy="100" r="70" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg>'
               f'<div class="pt">&frac12;+</div><div class="pl">MUMBAI</div></div>')
    slap(i, T(162) - .05, -4, d=.3, frm=1.5)
    js(f'tl.fromTo("#{i} .pfg", {{strokeDashoffset: 1}}, {{strokeDashoffset: .4, duration: .6, ease: {ST(.6, "power2.out")}, immediateRender: false}}, {T(162):.3f});')
    label("SHOPPING YAHIN SE", 600, 770, T(169) - .05, kind="white", size=48, rot=2)
    js(f'tl.to("#{i}", {{opacity: 0, scale: .6, duration: .2, ease: {ST(.2, "power2.in")}}}, {T(188) - .25:.3f});')
    stamp("BOHRI MUSLIMS", 300, 300, T(192) - .03, rot=-7, size=100)
    end_group()

    # 9. Chapter two
    _, ta, tb, a, b, _ = S["ch2"]
    chapter("ch2", "02", "PARSI COMMUNITY", "NOW LET'S TALK ABOUT", ta, tb, a, T(202) - .04)

    # 10. Dhanteras gold, the biggest jewellery brand: Tanishq
    _, ta, tb, a, b, _ = S["tanishq"]
    group("tanishq", ta, tb)
    scrap("black", 3, 40, 100, 520, -7, ta + .03, z=1)
    label("DHANTERAS", 100, 150, T(207) - .04, kind="red", size=100, rot=-4)
    draw(["M 150 360 A 70 70 0 1 1 150.1 360", "M 150 300 L 168 270 L 132 270 Z", "M 300 400 A 46 46 0 1 1 300.1 400",
          "M 400 420 A 46 46 0 1 1 400.1 420"], 60, 260, 520, 330, "0 0 520 330", T(212) - .05, d=.5, z=4, stroke="#d9a520", sw=8)
    label("JEWELLERY", 120, 590, T(212) - .03, kind="white", size=60, rot=2)
    label("GOLD", 420, 590, T(215) - .03, kind="white", size=60, rot=-2)
    card('<div class="qq">India ka sabse bada<br>jewellery brand?</div>', 560, 160, 470, T(219) - .05, rot=3, z=3)
    logo("tanishq", 590, 430, 380, 380, T(229) - .04, rot=-3, z=6)
    circle(540, 400, 480, 440, T(229) + .2)
    end_group()

    # 11. Electronics: Croma
    _, ta, tb, a, b, _ = S["croma"]
    group("croma", ta, tb)
    scrap("red", 3, 520, 140, 520, 6, ta + .03, z=1)
    label("ELECTRONICS", 90, 170, T(233) - .04, kind="black", size=96, rot=-3)
    card('<div class="qq">Kahaan se?<br><span>mostly&hellip;</span></div>', 110, 360, 400, T(239) - .05, rot=-2, z=3)
    logo("croma", 560, 300, 420, 420, T(245) - .04, rot=3, z=6)
    circle(510, 270, 520, 480, T(245) + .2)
    end_group()

    # 12. New clothes: Westside and Zudio
    _, ta, tb, a, b, _ = S["wz"]
    group("wz", ta, tb)
    scrap("grey", 3, 40, 420, 620, -5, ta + .03, z=1)
    label("NAYE KAPDE", 90, 150, T(251) - .04, kind="black", size=100, rot=-3)
    draw(["M 300 360 C 300 330 340 320 350 345 C 358 368 330 380 320 392 L 320 410", "M 320 410 L 160 500 L 480 500 Z"],
         520, 140, 520, 420, "0 0 640 520", T(252), d=.5, z=3, stroke="#111", sw=8)
    logo("westside", 90, 420, 400, 400, T(265) - .04, rot=-4, z=6)
    i = logo("zudio", 560, 560, 460, 120, T(267) - .04, rot=3, z=7)
    end_group()

    # 13. All of them: Tata, a Parsi family
    _, ta, tb, a, b, _ = S["tata"]
    group("tata", ta, tb)
    for k, (n, x, y, w, h, r) in enumerate([("tanishq", 60, 90, 250, 250, -4), ("croma", 770, 90, 250, 250, 4),
                                            ("westside", 60, 600, 250, 250, 3), ("zudio", 730, 720, 300, 80, -3)]):
        logo(n, x, y, w, h, ta + .05 + k * .1, rot=r, z=4)
    draw(["M 310 220 L 430 400", "M 770 220 L 650 400", "M 310 720 L 430 560", "M 760 730 L 650 560"], 0, 0, 1080, 960, "0 0 1080 960",
         T(283) - .05, d=.3, z=3, stroke="#111", sw=7)
    i = nid("tata")
    TOP.append(f'<div class="tatabox" id="{i}">TATA</div>')
    slap(i, T(285) - .05, -3, d=.36, frm=2)
    stamp("PARSI FAMILY", 330, 580, T(293) - .03, rot=-6, size=76)
    end_group()

    # 14. Secular: the Preamble, SECULAR marked
    _, ta, tb, a, b, _ = S["secular"]
    group("secular", ta, tb)
    scrap("red", 0, 600, 80, 460, 8, ta + .03, z=1)
    card('<div class="pre-h">THE CONSTITUTION OF INDIA &middot; PREAMBLE</div><div class="pre">WE, THE PEOPLE OF INDIA, having solemnly resolved to '
         'constitute India into a SOVEREIGN SOCIALIST <b id="sec">SECULAR</b> DEMOCRATIC REPUBLIC and to secure to all its citizens: JUSTICE, '
         'social, economic and political; LIBERTY of thought, expression, belief, faith and worship; EQUALITY of status and of opportunity&hellip;</div>',
         110, 120, 860, ta + .05, rot=-2, z=3, cls="note doc")
    marker("#sec", T(337) - .05, .35)
    circle(100, 350, 270, 150, T(337) + .25, z=6)
    stamp("KHILAAF", 640, 730, T(342) - .03, rot=-8, size=90)
    end_group()

    # 15. The close: every community, Happy Diwali
    _, ta, tb, a, b, _ = S["names"]
    group("names", ta, tb)
    scrap("white", 2, 30, 90, 1020, -2, ta + .03, z=1)
    spots = [(355, "HINDU", 90, 130, "black", -4), (356, "MUSLIM", 520, 160, "red", 3), (357, "SIKH", 140, 300, "white", 2),
             (358, "ISAAI", 470, 330, "black", -3), (359, "PARSI", 150, 470, "red", -2), (360, "JAIN", 560, 500, "white", 4)]
    for j, txt, x, y, kind, r in spots:
        label(txt, x, y, T(j) - .04, kind=kind, size=100, rot=r, type_on=False)
    i = nid("hd")
    TOP.append(f'<div class="hd" id="{i}"><span>HAPPY</span> <span class="r">DIWALI</span></div>')
    slap(i, T(365) - .05, -3, d=.4, frm=1.8)
    diya = "M 20 60 C 40 90 120 90 140 60 Z M 80 52 C 66 36 74 18 80 6 C 86 18 94 36 80 52 Z"
    for k, x in enumerate([120, 470, 820]):
        draw([diya], x, 790, 160, 110, "0 0 160 110", T(365) + .1 + k * .08, d=.35, z=5, stroke="#d9a520", sw=6)
    end_group()


# ------------------------------------------------------------------------------------------------ captions (the Surrender ad's)
FUNC = {"ki", "ke", "ka", "ko", "se", "pe", "hai", "hain", "toh", "aur", "ek", "ye", "woh", "mein", "the", "of", "to", "a", "and", "is", "an",
        "you", "i", "am", "or", "bhi", "main", "thi", "hoon", "sab", "har", "hi", "hum", "aap", "jo", "un", "in", "by", "as", "with", "me",
        "let", "are", "that", "such", "from", "par", "bas", "ab", "sa", "liye", "karte", "karta", "karna", "agar", "uske"}


def chunks(a, b, maxw=3, maxc=16):
    out, cur = [], []
    for i in range(a, b):
        if W[i].get("cut"):
            continue
        cur.append(i)
        txt = " ".join(word(j) for j in cur)
        end = W[i]["text"][-1] in ",.।?"
        if (len(cur) >= maxw or len(txt) >= maxc or end) and (end or word(i).lower().strip(",.?") not in FUNC or len(cur) >= maxw + 2):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    merged = []
    for c in out:
        if merged and all(word(j).lower().strip(",.?") in FUNC for j in c):
            merged[-1] = merged[-1] + c
        else:
            merged.append(c)
    return merged


def seam_caps(a, b, tend):
    """Split sections: one to three words in a black box with white type on the seam."""
    ch = chunks(a, b)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        i = nid("sc")
        POST.append(f'<div class="seam" id="{i}"><span>{" ".join(word(j) for j in c)}</span></div>')
        show(f"#{i}", t0, t1)
        js(f'tl.fromTo("#{i} span", {{scale: 1.12}}, {{scale: 1, duration: .16, ease: "power3.out", immediateRender: false}}, {t0:.3f});')


def full_caps(a, b, tend):
    """Full sections: a small script line over a big condensed word, red on key words."""
    ch = chunks(a, b, maxw=4, maxc=22)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        key = [j for j in c if j in RED]
        tail = [j for j in c if word(j).lower().strip(",.?") not in FUNC]
        big = key if key else (c[c.index(tail[-1]):] if tail else c[-1:])
        small = [j for j in c if j not in big]
        i = nid("fc")
        sm = " ".join(word(j) for j in small).lower()
        bg = " ".join(word(j) for j in big).upper().rstrip(",.")
        POST.append(f'<div class="fcap" id="{i}">' + (f'<div class="scr">{sm}</div>' if sm else "") +
                    f'<div class="bigw{" red" if key else ""}" style="font-size:{min(150, int(1780 / max(1, len(bg))))}px">{bg}</div></div>')
        show(f"#{i}", t0, t1)
        if sm:
            js(f'tl.fromTo("#{i} .scr", {{opacity: 0, x: -20, filter: "blur(6px)"}}, {{opacity: 1, x: 0, filter: "blur(0px)", duration: .18, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
        tb = T(big[0]) - .02
        js(f'tl.set("#{i} .bigw", {{opacity: 0}}, {t0 - .001:.3f});')
        js(f'tl.fromTo("#{i} .bigw", {{opacity: 0, scale: 1.3, filter: "blur(10px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "expo.out", immediateRender: false}}, {max(t0, tb):.3f});')


# ------------------------------------------------------------------------------------------------ layout + transitions
TEAR = ["white-1", "grey-0", "red-2", "black-0", "white-3", "grey-2"]


def layout():
    nt = 0
    for k, (kind, ta, tb, a, b, board) in enumerate(SECS):
        prev = SECS[k - 1][0] if k else None
        nxt = SECS[k + 1][0] if k + 1 < len(SECS) else None
        if kind == "split":
            js(f'tl.set("#split", {{opacity: 1, scale: 1, filter: "blur(0px)"}}, {ta:.3f});')
            js(f'tl.fromTo("#stagew", {{scale: 1}}, {{scale: 1.05, duration: {tb - ta - .02:.2f}, ease: "none", immediateRender: false}}, {ta:.3f});')
            if tb < DUR:
                js(f'tl.set("#split", {{opacity: 0}}, {tb:.3f});')
            if prev == "full" or prev is None:
                js(f'tl.fromTo("#botin", {{scale: 1.5, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                js(f'tl.fromTo("#topin", {{scale: 1.12, filter: "blur(12px)"}}, {{scale: 1, filter: "blur(0px)", duration: .42, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
            else:
                # board to board: a torn sheet tears across the top (stepped), the face pushes in
                tear = TEAR[nt % len(TEAR)]
                nt += 1
                js(f'tl.set("#tear", {{attr: {{src: "assets/img/paper/scrap/{tear}.png"}}}}, {ta - .25:.3f});')
                js(f'tl.fromTo("#tear", {{opacity: 1, x: -1500, rotation: {-8 if nt % 2 else 6}}}, {{opacity: 1, x: 1500, duration: .5, ease: {ST(.5, "power2.inOut")}, '
                   f'immediateRender: false}}, {ta - .25:.3f});')
                js(f'tl.set("#tear", {{opacity: 0}}, {ta + .26:.3f});')
                js(f'tl.fromTo("#botin", {{scale: 1.18}}, {{scale: 1, duration: .3, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
            if nxt == "full":
                js(f'tl.to("#split", {{scale: 1.2, filter: "blur(14px)", duration: .2, ease: "power2.in"}}, {tb - .2:.3f});')
            seam_caps(a, b, tb)
            continue
        js(f'tl.set("#full", {{opacity: 1}}, {ta:.3f});')
        js(f'tl.set("#full", {{opacity: 0}}, {tb:.3f});')
        js(f'tl.fromTo("#fullin", {{scale: 1.18, filter: "blur(12px)"}}, {{scale: 1, filter: "blur(0px)", duration: .3, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
        # punch-ins on sentence starts inside a long full section (a jump-cut feel, no pulsing)
        starts = [i for i in range(a + 1, b) if W[i - 1]["text"][-1] in ".?।" and not W[i].get("cut")]
        for n, i in enumerate(starts):
            js(f'tl.set("#fullz", {{scale: {1.14 if n % 2 == 0 else 1}}}, {T(i) - .04:.3f});')
        if starts:
            js(f'tl.set("#fullz", {{scale: 1}}, {tb:.3f});')
        full_caps(a, b, tb)
        if nxt == "split":
            js(f'tl.fromTo("#flash", {{opacity: 0}}, {{opacity: .8, duration: .06, immediateRender: false}}, {tb - .05:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: .25, ease: "power2.out"}}, {tb + .02:.3f});')
    HIDE.extend(["#split", "#full", "#flash", "#tear", "#hold"])
    js(f'tl.set("#hold", {{opacity: 1}}, {VDUR - .04:.3f});')


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/Inter-700.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Kaushan"; src: url("assets/fonts/KaushanScript.ttf"); }}
@font-face {{ font-family: "Play"; font-style: italic; font-weight: 700; src: url("assets/fonts/PlayfairDisplay-700Italic.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #efebe4; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter"; color: #111; background: #efebe4; }}
#split {{ position: absolute; inset: 0; opacity: 0; transform-origin: 50% 50%; }}
#top {{ position: absolute; left: 0; top: 0; width: {FW}px; height: 960px; overflow: hidden; background: #efebe4; }}
#topin {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
#paper {{ position: absolute; left: -300px; top: -400px; width: 1700px; height: 2550px; background: url(assets/img/paper/paper.png) 0 0 / 1700px auto;
  filter: sepia(.06) saturate(.8) brightness(1.06); }}
#grid {{ position: absolute; inset: -40px; opacity: .55;
  background-image: linear-gradient(rgba(70,90,130,.22) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(70,90,130,.22) 1.5px, transparent 1.5px);
  background-size: 72px 72px; }}
#stagew {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.grp {{ position: absolute; inset: 0; opacity: 0; }}
.scrap {{ position: absolute; opacity: 0; filter: drop-shadow(0 10px 14px rgba(0,0,0,.28)); }}
.print {{ position: absolute; opacity: 0; background: #f6f3ec; padding: 16px 16px 50px; box-shadow: 0 18px 34px rgba(0,0,0,.35); }}
.print img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.print.bw img {{ filter: grayscale(1) contrast(1.25) brightness(1.05); }}
.tape {{ position: absolute; left: 50%; top: -22px; width: 170px; height: 46px; margin-left: -85px; background: rgba(238,228,196,.78);
  transform: rotate(-3deg); box-shadow: 0 2px 4px rgba(0,0,0,.12); }}
.lab {{ position: absolute; opacity: 0; font-family: "Anton"; line-height: 1; padding: .1em .22em .12em; white-space: nowrap; transform-origin: 0 50%;
  box-shadow: 0 8px 16px rgba(0,0,0,.25); letter-spacing: .01em; }}
.lab.black {{ background: #111; color: #fff; }}
.lab.white {{ background: #fbf9f4; color: #111; }}
.lab.red {{ background: #e3202f; color: #fff; }}
.lab .c {{ display: inline-block; }}
.stamp {{ position: absolute; opacity: 0; font-family: "Anton"; line-height: 1.15; color: #e3202f; border: 9px solid #e3202f; border-radius: 12px; padding: .04em .26em 0;
  white-space: nowrap; background: rgba(251,249,244,.55); mix-blend-mode: multiply; }}
.doo, .map {{ position: absolute; opacity: 0; fill: none; stroke-linecap: round; stroke-linejoin: round; overflow: visible; }}
.note {{ position: absolute; opacity: 0; background: #fbf9f4; padding: 34px 40px 38px; box-shadow: 0 18px 34px rgba(0,0,0,.3); }}
.quote .qmark {{ font: italic 700 190px/0.6 "Play"; color: #e3202f; height: 80px; }}
.quote .qtxt {{ font: 700 52px/1.3 "Inter"; letter-spacing: -.01em; color: #111; }}
.quote .qw {{ display: inline-block; opacity: 0; padding: 0 .06em; }}
.quote .qw.mk {{ background: linear-gradient(transparent 52%, rgba(255,214,0,.85) 52%) 0 0 / 0% 100% no-repeat; }}
.quote .qby {{ font: 500 30px/1.2 "Inter"; color: #666; margin-top: 20px; }}
.mapc {{ height: 460px; padding: 20px; }}
.mapc .map {{ position: absolute; left: 20px; top: 20px; width: 740px; height: 420px; opacity: 1; stroke: #b9b2a5; stroke-width: 14; }}
.mapc .map .main {{ stroke: #111; stroke-width: 22; }}
.pin {{ position: absolute; width: 90px; height: 120px; opacity: 0; z-index: 5; filter: drop-shadow(0 8px 8px rgba(0,0,0,.3)); }}
.pin svg {{ width: 100%; height: 100%; }}
.pin path {{ fill: #e3202f; }}
.pin circle {{ fill: #fff; }}
.num {{ position: absolute; left: 70px; top: 330px; opacity: 0; font: 400 400px/1 "Anton"; color: transparent; -webkit-text-stroke: 10px #111; z-index: 2; }}
.qq {{ font: 800 50px/1.15 "Inter"; letter-spacing: -.02em; }}
.qq span {{ font: 700 italic 40px/1.2 "Play"; color: #e3202f; }}
.logo {{ position: absolute; opacity: 0; background: #fff; padding: 18px; box-shadow: 0 14px 28px rgba(0,0,0,.3); display: grid; place-items: center; }}
.logo img {{ max-width: 100%; max-height: 100%; display: block; }}
.pie {{ position: absolute; left: 740px; top: 60px; width: 300px; height: 300px; opacity: 0; z-index: 6; background: #fbf9f4; border-radius: 50%;
  box-shadow: 0 14px 28px rgba(0,0,0,.3); }}
.pie svg {{ position: absolute; inset: 0; }}
.pie .pbg {{ fill: none; stroke: #e6e0d4; stroke-width: 34; }}
.pie .pfg {{ fill: none; stroke: #e3202f; stroke-width: 34; }}
.pie .pt {{ position: absolute; left: 0; right: 0; top: 92px; text-align: center; font: 400 92px/1 "Anton"; color: #111; }}
.pie .pl {{ position: absolute; left: 0; right: 0; top: 190px; text-align: center; font: 800 26px/1 "Inter"; letter-spacing: .1em; color: #e3202f; }}
.tatabox {{ position: absolute; left: 380px; top: 380px; width: 320px; padding: 30px 0 22px; opacity: 0; z-index: 6; background: #111; color: #fff; text-align: center;
  font: 400 150px/1 "Anton"; letter-spacing: .04em; box-shadow: 0 16px 30px rgba(0,0,0,.35); }}
.doc {{ padding: 40px 46px; }}
.pre-h {{ font: 800 28px/1.2 "Inter"; letter-spacing: .14em; color: #e3202f; margin-bottom: 22px; }}
.pre {{ font: 500 44px/1.38 "Play"; font-style: italic; color: #222; }}
.pre b {{ font-style: normal; font-family: "Anton"; font-weight: 400; letter-spacing: .02em; padding: 0 .1em;
  background: linear-gradient(transparent 50%, rgba(255,214,0,.9) 50%) 0 0 / 0% 100% no-repeat; }}
.hd {{ position: absolute; left: 0; width: {FW}px; top: 640px; text-align: center; opacity: 0; z-index: 8; font: 400 150px/1 "Anton"; color: #111; }}
.hd .r {{ color: #e3202f; }}
#bot {{ position: absolute; left: 0; top: 960px; width: {FW}px; height: 960px; overflow: hidden; background: #222; }}
#botin {{ position: absolute; inset: 0; transform-origin: 50% 35%; }}
#botin video, #hold {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#hold {{ position: absolute; inset: 0; opacity: 0; }}
#seamline {{ position: absolute; left: -20px; top: 944px; width: {FW + 40}px; height: 34px; z-index: 6; background: #fbf9f4;
  clip-path: polygon(0 30%, 4% 10%, 9% 40%, 14% 15%, 20% 35%, 26% 8%, 31% 30%, 37% 12%, 43% 38%, 49% 10%, 55% 32%, 61% 14%, 67% 36%, 73% 9%, 79% 30%,
  85% 12%, 91% 38%, 96% 14%, 100% 30%, 100% 74%, 95% 92%, 89% 70%, 83% 95%, 77% 72%, 71% 90%, 65% 68%, 59% 94%, 53% 70%, 47% 92%, 41% 66%, 35% 90%,
  29% 70%, 23% 95%, 17% 72%, 11% 92%, 5% 70%, 0 88%); }}
#tear {{ position: absolute; left: -200px; top: -60px; width: 1480px; height: 1080px; object-fit: fill; opacity: 0; z-index: 7; filter: drop-shadow(0 10px 20px rgba(0,0,0,.3)); }}
#full {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; background: #222; }}
#fullin, #fullz {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#fullz video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.seam {{ position: absolute; left: 0; width: {FW}px; top: 872px; text-align: center; opacity: 0; z-index: 9; }}
.seam span {{ display: inline-block; background: #000; color: #fff; font: 800 52px/1 "Inter"; padding: 13px 26px 15px; border-radius: 8px; letter-spacing: -.01em; }}
.fcap {{ position: absolute; left: 100px; right: 80px; top: 1290px; opacity: 0; z-index: 9; }}
.fcap .scr {{ font: 400 74px/1.1 "Kaushan"; color: #fff; text-shadow: 0 4px 14px rgba(0,0,0,.6); margin-left: 6px; }}
.fcap .bigw {{ font: 400 150px/1 "Anton"; color: #fff; letter-spacing: .01em; text-shadow: 0 8px 26px rgba(0,0,0,.5); transform-origin: 0 60%; }}
.fcap .bigw.red {{ color: #ff2d3d; text-shadow: 0 4px 0 #fff, 0 10px 30px rgba(0,0,0,.5); }}
#flash {{ position: absolute; inset: 0; z-index: 22; opacity: 0; background: #fbf9f4; }}
#grain {{ position: absolute; inset: 0; z-index: 23; pointer-events: none; opacity: .06; background: url(assets/img/paper/grain.png); mix-blend-mode: multiply; }}
"""


def main():
    boards()
    layout()
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Diwali opinion reel 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="split">
        <div id="top"><div id="topin"><div id="paper"></div><div id="grid"></div><div id="stagew">{"".join(TOP)}</div>
          <img id="tear" src="assets/img/paper/scrap/white-1.png" alt=""></div></div>
        <div id="bot"><div id="botin"><video id="vsplit" class="clip" src="assets/video/face_split.mp4" data-start="0" data-duration="{VDUR}" data-track-index="2" muted playsinline></video>
          <img id="hold" src="assets/img/hold/last_split.png" alt=""></div></div>
        <div id="seamline"></div>
      </div>
      <div id="full"><div id="fullin"><div id="fullz"><video id="vfull" class="clip" src="assets/video/face_full.mp4" data-start="0" data-duration="{VDUR}" data-track-index="1" muted playsinline></video></div></div></div>
      {"".join(POST)}
      <div id="flash"></div><div id="grain"></div>
      <audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{VDUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const ST = (n, e) => {{ const f = gsap.parseEase(e); return (p) => f(Math.round(p * n) / n); }};
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
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SECS)} sections, {DUR} s")


if __name__ == "__main__":
    main()
