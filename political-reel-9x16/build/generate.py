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
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hinglish import roman  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
W = json.load(open(os.path.join(ROOT, "plan", "words_tight.json")))
VDUR = round(float(__import__("subprocess").run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
    os.path.join(ROOT, "assets", "video", "face_split.mp4")], capture_output=True, text=True).stdout), 3)     # v2: the take at 1.1x
BY, BH = 240, 380                   # v3: the board strip (inside the Reels safe area: 250 to 1520)
CARD = (90, 650, 900, 860)          # v3: her video as a taped print, x y w h, ends at 1510 above the caption UI
DUR = round(VDUR + 1.0, 3)          # the last board holds a second on her last frame
A, HIDE, TOP, POST = [], [], [], []
NID = [0]
RND = random.Random(5)


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
    return draw(["M 150 14 C 250 10 300 62 296 116 C 292 180 222 222 146 220 C 62 218 6 172 8 112 C 10 50 70 12 160 14 C 222 16 266 36 286 64"],
                x, y, w, h, "0 0 300 230", t, d=.45, z=z, sw=8)


STAR = "M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z"


def twinkle(n, t0, t1, area=(40, 40, 1000, 880), colors=("#d9a520", "#e3202f", "#111"), z=8):
    """Little four-point sparkles that twinkle (stepped) for the whole board."""
    ax, ay, aw, ah = area
    for k in range(n):
        i = nid("tw")
        sz = RND.uniform(30, 66)
        TOP.append(f'<svg class="tw" id="{i}" viewBox="-50 -50 100 100" style="left:{ax + RND.uniform(0, aw):.0f}px;top:{ay + RND.uniform(0, ah):.0f}px;'
                   f'width:{sz:.0f}px;height:{sz:.0f}px;z-index:{z}"><path d="{STAR}" fill="{colors[k % len(colors)]}"/></svg>')
        st, per = t0 + RND.uniform(.1, .9), RND.uniform(.45, .8)
        reps = max(1, int((t1 - st) / per) - 1)
        js(f'tl.fromTo("#{i}", {{opacity: 0, scale: 0, rotation: -40}}, {{opacity: 1, scale: 1, rotation: 25, duration: {per:.2f}, ease: {ST(per, "sine.inOut")}, '
           f'yoyo: true, repeat: {reps}, immediateRender: false}}, {st:.3f});')
        js(f'tl.set("#{i}", {{opacity: 0}}, {t1:.3f});')


def diya(x, y, w, t, t1, z=7):
    """A clay diya whose flame flickers."""
    i = nid("dy")
    TOP.append(f'<svg class="diya" id="{i}" viewBox="0 0 160 130" style="left:{x}px;top:{y}px;width:{w}px;height:{w * 130 / 160:.0f}px;z-index:{z}">'
               f'<ellipse class="gl" cx="80" cy="52" rx="44" ry="44"/>'
               f'<path class="body" d="M 8 78 C 24 124 136 124 152 78 C 120 92 40 92 8 78 Z"/><path class="rim" d="M 8 78 C 40 92 120 92 152 78"/>'
               f'<g class="fl"><path class="f1" d="M 80 80 C 58 62 68 34 80 12 C 92 34 102 62 80 80 Z"/><path class="f2" d="M 80 78 C 70 66 74 50 80 38 C 86 50 90 66 80 78 Z"/></g></svg>')
    slap(i, t, 0, d=.3, frm=1.6)
    n = max(2, int((t1 - t) / .13))
    js(f'tl.fromTo("#{i} .fl", {{scaleY: 1, scaleX: 1}}, {{scaleY: 1.22, scaleX: .86, duration: .13, ease: "sine.inOut", yoyo: true, repeat: {n}, immediateRender: false}}, {t + .1:.3f});')
    js(f'tl.fromTo("#{i} .gl", {{opacity: .35}}, {{opacity: .7, duration: .26, ease: "sine.inOut", yoyo: true, repeat: {n // 2}, immediateRender: false}}, {t + .1:.3f});')
    return i


def firework(cx, cy, r, t0, t1, color="#e3202f", period=1.1, z=4):
    """A burst of lines that bursts out from its centre and fades, again and again."""
    i = nid("fw")
    import math
    lines = "".join(f'<path d="M {math.cos(k / 12 * 6.283) * 30:.0f} {math.sin(k / 12 * 6.283) * 30:.0f} L {math.cos(k / 12 * 6.283) * 96:.0f} '
                    f'{math.sin(k / 12 * 6.283) * 96:.0f}"/>' for k in range(12))
    dots = "".join(f'<circle cx="{math.cos((k + .5) / 12 * 6.283) * 80:.0f}" cy="{math.sin((k + .5) / 12 * 6.283) * 80:.0f}" r="5"/>' for k in range(12))
    TOP.append(f'<svg class="fw" id="{i}" viewBox="-100 -100 200 200" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;z-index:{z};'
               f'stroke:{color};fill:{color}">{lines}{dots}</svg>')
    reps = max(0, int((t1 - t0) / period) - 1)
    js(f'tl.fromTo("#{i}", {{opacity: 1, scale: .12, rotation: 0}}, {{opacity: 0, scale: 1, rotation: 12, duration: .85, ease: {ST(.85, "expo.out")}, '
       f'repeat: {reps}, repeatDelay: {period - .85:.2f}, immediateRender: false}}, {t0:.3f});')
    HIDE.append(f"#{i}")


def lantern(x, y, w, t, t1, color="#e3202f", z=6, string=140):
    """A paper kandil on a string that swings."""
    i = nid("kd")
    h = w * 1.9
    TOP.append(f'<svg class="kand" id="{i}" viewBox="0 0 100 {190 + string * 100 / w:.0f}" style="left:{x}px;top:{y - string}px;width:{w}px;'
               f'height:{h + string:.0f}px;z-index:{z}"><g transform="translate(0 {string * 100 / w:.0f})">'
               f'<path class="str" d="M 50 {-string * 100 / w:.0f} L 50 8"/>'
               f'<path class="lt" style="fill:{color}" d="M 50 8 L 92 46 L 92 106 L 50 146 L 8 106 L 8 46 Z"/>'
               f'<path class="ln" d="M 8 46 L 92 46 M 8 106 L 92 106 M 50 8 L 50 146 M 29 27 L 29 126 M 71 27 L 71 126"/>'
               f'<path class="ts" d="M 50 146 L 50 186 M 40 150 L 36 184 M 60 150 L 64 184"/></g></svg>')
    slap(i, t, 0, d=.3, frm=1.4, dy=-120)
    n = max(1, int((t1 - t) / 1.0))
    js(f'tl.fromTo("#{i}", {{rotation: -8}}, {{rotation: 8, duration: 1.0, ease: "sine.inOut", yoyo: true, repeat: {n}, immediateRender: false}}, {t + .3:.3f});')
    return i


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
    twinkle(6, ta, tb)
    diya(860, 700, 130, title_at + .2, tb)
    end_group()


# ------------------------------------------------------------------------------------------------ the boards
# v3 (owner: "fit the reels grid perfectly without anything overlapping"): everything that matters sits between the
# Reels top bar (0-250) and the caption / username area (from 1520): a board strip 1080x380 at y 240 and her video as
# a taped print below it (90,650 900x860). Board coordinates below are in that 1080x380 strip.
def boards():
    S = {s[5]: s for s in SECS if s[5]}

    # 1. The hook: her quote, typed on as she says it, key words marked; diyas either side
    _, ta, tb, a, b, _ = S["quote"]
    group("quote", ta, tb)
    scrap("red", 0, 20, 10, 420, -6, ta + .05, z=1)
    words = [j for j in range(1, 24)]
    body = " ".join(f'<span class="qw{" mk" if j in (15, 19, 20, 21) else ""}" id="qw{j}">{word(j)}</span>' for j in words)
    card(f'<div class="qmark">&ldquo;</div><div class="qtxt">{body}</div><div class="qby">&mdash; a Maharashtra cabinet minister</div>',
         150, 0, 780, ta + .08, rot=-1.5, z=3, cls="note quote")
    words_on("qw", words)
    marker("#qw15", T(15) + .05)
    for j in (19, 20, 21):
        marker(f"#qw{j}", T(j) + .02, .18)
    diya(20, 270, 120, ta + .4, tb)
    diya(940, 270, 120, ta + .55, tb)
    twinkle(5, ta, tb, area=(180, 300, 720, 40))
    end_group()
    js('tl.set(".qby", {opacity: 0}, 0);')
    js(f'tl.to(".qby", {{opacity: 1, duration: .2}}, {T(23) + .2:.3f});')

    # 2. Who said it: his photo as a black-and-white print, circled, his name types on
    _, ta, tb, a, b, _ = S["rane"]
    group("rane", ta, tb)
    scrap("red", 1, 40, 20, 380, -10, ta + .03, z=1)
    prt("assets/img/ref/speaker_face.jpg", 100, 20, 280, 300, -4, ta + .06, z=3)
    label("SITTING CABINET MINISTER", 470, 40, T(37) - .05, kind="white", size=34, rot=2, z=9)
    label("MAHARASHTRA", 480, 100, T(35), kind="red", size=52, rot=2, z=9)
    label("NITESH RANE", 450, 180, T(40) - .04, kind="black", size=96, rot=-3, z=9)
    circle(40, -20, 410, 410, T(40) + .05)
    draw(["M 40 90 C 120 30 200 14 300 22", "M 300 22 L 262 2 M 300 22 L 268 48"], 520, 290, 300, 100, "0 0 320 110", T(41) + .1, d=.35)
    end_group()

    def chapter2(board, num, title, lead, title_at):
        _, ta, tb, a, b, _ = S[board]
        group(board, ta, tb)
        scrap("black", 1, 500, 110, 520, -5, ta + .05, z=1)
        i = nid("num")
        TOP.append(f'<div class="num" id="{i}">{num}</div>')
        slap(i, ta + .02, -4, d=.4, frm=1.6)
        label(lead, 420, 50, ta + .1, kind="white", size=40, rot=-2)
        label(title, 400, 150, title_at, kind="black", size=68, rot=-3)
        draw(["M 30 40 C 200 10 420 60 600 30"], 420, 270, 560, 60, "0 0 640 70", title_at + .3, d=.35)
        diya(880, 280, 110, title_at + .2, tb)
        twinkle(5, ta, tb)
        end_group()

    # 3. Chapter one
    chapter2("ch1", "01", "MUSLIM COMMUNITY", "LET'S START WITH", T(61) - .04)

    # 4. Pataake: bursts that keep going off, Mumbai, the biggest market
    _, ta, tb, a, b, _ = S["crackers"]
    group("crackers", ta, tb)
    scrap("white", 0, 60, -10, 960, -2, ta + .03, z=1)
    firework(190, 120, 120, T(70) - .05, tb, "#e3202f", 1.0)
    firework(540, 80, 90, T(70) + .3, tb, "#111", 1.2)
    firework(900, 130, 130, T(71), tb, "#d9a520", 0.9)
    draw(["M 190 120 C 196 200 200 300 204 380", "M 900 130 C 890 220 884 300 880 380"], 0, 0, 1080, 380, "0 0 1080 380", T(70) - .3, d=.3, z=3,
         stroke="#111", sw=6)
    label("PATAAKE", 360, 140, T(70), kind="black", size=96, rot=-3)
    label("MUMBAI", 110, 290, T(76), kind="white", size=52, rot=2)
    stamp("SABSE BADA MARKET", 420, 270, T(85) - .03, rot=-4, size=64)
    twinkle(6, ta, tb)
    end_group()

    # 5. Mohammad Ali Road: the owner's photo (Minara Masjid over the market), the pin drops on the minaret
    _, ta, tb, a, b, _ = S["mar"]
    group("mar", ta, tb)
    scrap("black", 0, 50, 0, 300, -9, ta + .03, z=1)
    prt("assets/img/ref/mohammad_ali_road.jpg", 80, -10, 270, 360, -3, ta + .05, z=3, bw=True, color_at=T(89) + .1)
    i = nid("pin")
    TOP.append(f'<div class="pin" id="{i}" style="left:270px;top:20px"><svg viewBox="0 0 60 80"><path d="M30 78 C 30 78 4 46 4 28 A 26 26 0 1 1 56 28 '
               f'C 56 46 30 78 30 78 Z"/><circle cx="30" cy="28" r="10"/></svg></div>')
    js(f'tl.fromTo("#{i}", {{opacity: 0, y: -200}}, {{opacity: 1, y: 0, duration: .4, ease: {ST(.4, "bounce.out")}, immediateRender: false}}, {T(89) - .05:.3f});')
    label("MOHAMMAD", 420, 20, T(89) - .02, kind="black", size=92, rot=-3)
    label("ALI ROAD", 450, 130, T(90) - .02, kind="black", size=92, rot=-3)
    label("MUMBAI", 820, 150, T(91) + .1, kind="white", size=46, rot=4)
    stamp("MUSLIM-OWNED", 480, 260, T(99) - .03, rot=-5, size=68)
    twinkle(6, ta, tb, area=(90, 0, 260, 300), colors=("#ffd34d", "#fff"))
    end_group()

    # 6. Kandil: the stall print turns to colour on "kandil"; kandils swing
    _, ta, tb, a, b, _ = S["kandil"]
    group("kandil", ta, tb)
    scrap("black", 2, 380, 20, 380, 8, ta + .03, z=1)
    prt("assets/img/ref/attar_kandil_lanterns_pune.jpg", 90, 10, 470, 310, -3, ta + .05, z=3, color_at=T(116) - .05)
    label("KANDIL", 620, 110, T(116) - .03, kind="red", size=110, rot=3)
    label("LANTERNS", 650, 250, T(119), kind="white", size=50, rot=-2)
    lantern(940, 20, 80, ta + .2, tb, "#d9a520")
    lantern(30, 30, 70, ta + .35, tb, "#e3202f")
    lantern(840, 10, 60, T(116), tb, "#111")
    twinkle(5, ta, tb)
    end_group()

    # 7. Attar community, Pune: generations of makers
    _, ta, tb, a, b, _ = S["attar"]
    group("attar", ta, tb)
    scrap("red", 2, 40, 190, 700, -3, ta + .03, z=1)
    prt("assets/img/ref/attar_kandil_lanterns_pune.jpg?v=2", 790, 0, 230, 160, 6, ta + .02, z=2, bw=False)
    label("PUNE", 80, 10, T(124) - .04, kind="white", size=60, rot=-3)
    label("ATTAR COMMUNITY", 80, 90, T(126) - .04, kind="black", size=84, rot=-2)
    person = "M 50 30 A 18 18 0 1 1 50.1 30 M 50 52 L 50 110 M 50 70 L 22 92 M 50 70 L 78 92 M 50 110 L 30 150 M 50 110 L 70 150"
    for k, (x, sz, tk) in enumerate([(110, 150, T(130)), (300, 130, T(131) + .1), (480, 110, T(133))]):
        draw([person], x, 210 + (150 - sz), sz * .66, sz, "0 0 100 160", tk, d=.4, z=4, stroke="#fff", sw=7)
    draw(["M 90 370 L 700 370", "M 700 370 L 668 350 M 700 370 L 668 390"], 0, 0, 1080, 400, "0 0 1080 400", T(130), d=.5, z=4, stroke="#fff", sw=7)
    label("PEEDHIYON SE", 740, 260, T(133) - .03, kind="white", size=56, rot=-2)
    lantern(960, 230, 60, T(136) - .1, tb, "#d9a520", z=7, string=60)
    end_group()

    # 8. Crawford Market: the print, half of Mumbai, Bohri Muslims
    _, ta, tb, a, b, _ = S["crawford"]
    group("crawford", ta, tb)
    scrap("grey", 1, 40, 0, 420, -6, ta + .03, z=1)
    prt("assets/img/ref/crawford_market.jpg", 70, 10, 540, 320, 2, ta + .05, z=3)
    label("CRAWFORD", 650, 20, ta + .2, kind="black", size=80, rot=-2)
    label("MARKET", 680, 120, ta + .35, kind="black", size=80, rot=-2)
    i = nid("pie")
    TOP.append(f'<div class="pie" id="{i}"><svg viewBox="0 0 200 200"><circle class="pbg" cx="100" cy="100" r="78"/>'
               f'<circle class="pfg" cx="100" cy="100" r="78" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg>'
               f'<div class="pt">&frac12;+</div><div class="pl">MUMBAI</div></div>')
    slap(i, T(162) - .05, -4, d=.3, frm=1.5)
    js(f'tl.fromTo("#{i} .pfg", {{strokeDashoffset: 1}}, {{strokeDashoffset: .4, duration: .6, ease: {ST(.6, "power2.out")}, immediateRender: false}}, {T(162):.3f});')
    label("SHOPPING YAHIN SE", 640, 250, T(169) - .05, kind="white", size=40, rot=2)
    js(f'tl.to("#{i}", {{opacity: 0, scale: .6, duration: .2, ease: {ST(.2, "power2.in")}}}, {T(188) - .25:.3f});')
    stamp("BOHRI MUSLIMS", 120, 130, T(192) - .03, rot=-7, size=78)
    twinkle(5, ta, tb, area=(80, 20, 520, 280), colors=("#ffd34d", "#e3202f"))
    end_group()

    # 9. Chapter two
    chapter2("ch2", "02", "PARSI COMMUNITY", "NOW LET'S TALK ABOUT", T(202) - .04)

    # 10. Dhanteras gold, the biggest jewellery brand: Tanishq
    _, ta, tb, a, b, _ = S["tanishq"]
    group("tanishq", ta, tb)
    scrap("black", 3, 40, 0, 400, -7, ta + .03, z=1)
    label("DHANTERAS", 70, 30, T(207) - .04, kind="red", size=80, rot=-4)
    draw(["M 110 230 A 52 52 0 1 1 110.1 230", "M 110 186 L 124 164 L 96 164 Z", "M 230 260 A 36 36 0 1 1 230.1 260",
          "M 310 270 A 36 36 0 1 1 310.1 270"], 30, 0, 400, 330, "0 0 400 330", T(212) - .05, d=.5, z=4, stroke="#d9a520", sw=8)
    label("JEWELLERY", 70, 300, T(212) - .03, kind="white", size=44, rot=2)
    label("GOLD", 300, 300, T(215) - .03, kind="white", size=44, rot=-2)
    card('<div class="qq">India ka sabse bada<br>jewellery brand?</div>', 440, 20, 330, T(219) - .05, rot=3, z=3)
    logo("tanishq", 800, 60, 240, 240, T(229) - .04, rot=-3, z=6)
    circle(760, 30, 320, 300, T(229) + .2)
    twinkle(7, ta, tb, colors=("#d9a520", "#ffd34d", "#e3202f"))
    end_group()

    # 11. Electronics: Croma
    _, ta, tb, a, b, _ = S["croma"]
    group("croma", ta, tb)
    scrap("red", 3, 600, 20, 420, 6, ta + .03, z=1)
    label("ELECTRONICS", 70, 40, T(233) - .04, kind="black", size=88, rot=-3)
    card('<div class="qq">Kahaan se?<br><span>mostly&hellip;</span></div>', 100, 200, 320, T(239) - .05, rot=-2, z=3)
    logo("croma", 660, 40, 290, 290, T(245) - .04, rot=3, z=6)
    circle(620, 10, 370, 350, T(245) + .2)
    twinkle(4, ta, tb)
    end_group()

    # 12. New clothes: Westside and Zudio
    _, ta, tb, a, b, _ = S["wz"]
    group("wz", ta, tb)
    scrap("grey", 3, 400, 120, 460, -5, ta + .03, z=1)
    label("NAYE KAPDE", 70, 30, T(251) - .04, kind="black", size=84, rot=-3)
    hng = draw(["M 300 360 C 300 330 340 320 350 345 C 358 368 330 380 320 392 L 320 410", "M 320 410 L 160 500 L 480 500 Z"],
               40, 130, 300, 245, "0 0 640 520", T(252), d=.5, z=3, stroke="#111", sw=10)
    js(f'tl.fromTo("#{hng}", {{rotation: -6, transformOrigin: "50% 10%"}}, {{rotation: 6, duration: .9, ease: "sine.inOut", yoyo: true, repeat: 7, immediateRender: false}}, {T(252) + .5:.3f});')
    logo("westside", 450, 40, 260, 260, T(265) - .04, rot=-4, z=6)
    logo("zudio", 760, 200, 270, 72, T(267) - .04, rot=3, z=7)
    twinkle(4, ta, tb)
    end_group()

    # 13. All of them: Tata, a Parsi family
    _, ta, tb, a, b, _ = S["tata"]
    group("tata", ta, tb)
    for k, (n, x, y, w, h, r) in enumerate([("tanishq", 60, 10, 170, 170, -4), ("croma", 850, 10, 170, 170, 4),
                                            ("westside", 80, 200, 160, 160, 3), ("zudio", 820, 270, 210, 56, -3)]):
        logo(n, x, y, w, h, ta + .05 + k * .1, rot=r, z=4)
    draw(["M 230 100 L 390 150", "M 850 100 L 690 150", "M 240 280 L 390 220", "M 820 290 L 690 220"], 0, 0, 1080, 380, "0 0 1080 380",
         T(283) - .05, d=.3, z=3, stroke="#111", sw=6)
    i = nid("tata")
    TOP.append(f'<div class="tatabox" id="{i}">TATA</div>')
    slap(i, T(285) - .05, -3, d=.36, frm=2)
    stamp("PARSI FAMILY", 380, 270, T(293) - .03, rot=-5, size=60)
    twinkle(5, ta, tb)
    end_group()

    # 14. Secular: the Preamble, SECULAR marked
    _, ta, tb, a, b, _ = S["secular"]
    group("secular", ta, tb)
    scrap("red", 0, 780, 0, 280, 8, ta + .03, z=1)
    card('<div class="pre-h">THE CONSTITUTION OF INDIA &middot; PREAMBLE</div><div class="pre">WE, THE PEOPLE OF INDIA, having solemnly resolved to '
         'constitute India into a SOVEREIGN SOCIALIST <b id="sec">SECULAR</b> DEMOCRATIC REPUBLIC and to secure to all its citizens: JUSTICE, '
         'social, economic and political; LIBERTY of thought, expression, belief, faith and worship&hellip;</div>',
         80, 0, 920, ta + .05, rot=-1.5, z=3, cls="note doc")
    marker("#sec", T(337) - .05, .35)
    stamp("KHILAAF", 770, 270, T(342) - .03, rot=-8, size=70)
    end_group()

    # 15. The close: every community, Happy Diwali, diyas, fireworks
    _, ta, tb, a, b, _ = S["names"]
    group("names", ta, tb)
    scrap("white", 2, 30, -10, 1020, -2, ta + .03, z=1)
    spots = [(355, "HINDU", 80, 0, "black", -4), (356, "MUSLIM", 320, 10, "red", 3), (357, "SIKH", 630, 0, "white", 2),
             (358, "ISAAI", 820, 20, "black", -3), (359, "PARSI", 180, 110, "red", -2), (360, "JAIN", 560, 110, "white", 4)]
    for j, txt, x, y, kind, r in spots:
        label(txt, x, y, T(j) - .04, kind=kind, size=74, rot=r, type_on=False)
    i = nid("hd")
    TOP.append(f'<div class="hd" id="{i}"><span>HAPPY</span> <span class="r">DIWALI</span></div>')
    slap(i, T(365) - .05, -3, d=.4, frm=1.8)
    diya(20, 250, 120, T(365) + .1, DUR)
    diya(940, 250, 120, T(365) + .2, DUR)
    firework(150, 90, 110, T(365) - .1, DUR, "#e3202f", .9, z=2)
    firework(930, 100, 120, T(365) + .2, DUR, "#d9a520", 1.0, z=2)
    twinkle(8, ta, DUR)
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


def big_tear(t, n):
    """Full frame to split and back: a big torn sheet sweeps across the whole screen; the cut happens under it."""
    js(f'tl.set("#tearbig", {{attr: {{src: "assets/img/paper/scrap/{["white-0", "white-2", "grey-1", "white-3"][n % 4]}.png"}}}}, {t - .3:.3f});')
    js(f'tl.fromTo("#tearbig", {{opacity: 1, x: -2300, y: 300, rotation: {-14 if n % 2 else 12}}}, {{opacity: 1, x: 2300, y: -300, duration: .6, '
       f'ease: {ST(.6, "power2.inOut")}, immediateRender: false}}, {t - .3:.3f});')
    js(f'tl.set("#tearbig", {{opacity: 0}}, {t + .31:.3f});')


def layout():
    nt = nb = 0
    for k, (kind, ta, tb, a, b, board) in enumerate(SECS):
        prev = SECS[k - 1][0] if k else None
        nxt = SECS[k + 1][0] if k + 1 < len(SECS) else None
        if kind == "split":
            js(f'tl.set("#split", {{opacity: 1, scale: 1, filter: "blur(0px)"}}, {ta:.3f});')
            js(f'tl.fromTo("#stagew", {{scale: 1}}, {{scale: 1.05, duration: {tb - ta - .02:.2f}, ease: "none", immediateRender: false}}, {ta:.3f});')
            if tb < DUR:
                js(f'tl.set("#split", {{opacity: 0}}, {tb:.3f});')
            if prev is None:
                js(f'tl.fromTo("#botin", {{scale: 1.5, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                js(f'tl.fromTo("#topin", {{scale: 1.12, filter: "blur(12px)"}}, {{scale: 1, filter: "blur(0px)", duration: .42, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
            elif prev == "full":
                big_tear(ta, nb)
                nb += 1
                js(f'tl.fromTo("#botin", {{scale: 1.3}}, {{scale: 1, duration: .45, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                js(f'tl.fromTo("#topin", {{scale: 1.15, rotation: -2}}, {{scale: 1, rotation: 0, duration: .5, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
            else:
                kind2 = ["tear", "whip", "zoom"][nt % 3]
                nt += 1
                if kind2 == "tear":                 # a torn sheet tears across the board (stepped)
                    tear = TEAR[nt % len(TEAR)]
                    js(f'tl.set("#tear", {{attr: {{src: "assets/img/paper/scrap/{tear}.png"}}}}, {ta - .25:.3f});')
                    js(f'tl.fromTo("#tear", {{opacity: 1, x: -1500, rotation: {-8 if nt % 2 else 6}}}, {{opacity: 1, x: 1500, duration: .5, ease: {ST(.5, "power2.inOut")}, '
                       f'immediateRender: false}}, {ta - .25:.3f});')
                    js(f'tl.set("#tear", {{opacity: 0}}, {ta + .26:.3f});')
                elif kind2 == "whip":               # the camera whips across the paper with motion blur
                    js(f'tl.set("#topin", {{filter: "url(#mbx)"}}, {ta - .16:.3f});')
                    js(f'tl.fromTo("#mbx feGaussianBlur", {{attr: {{stdDeviation: "0 0"}}}}, {{attr: {{stdDeviation: "80 0"}}, duration: .16, ease: "power2.in", immediateRender: false}}, {ta - .16:.3f});')
                    js(f'tl.to("#mbx feGaussianBlur", {{attr: {{stdDeviation: "0 0"}}, duration: .24, ease: "power2.out"}}, {ta:.3f});')
                    js(f'tl.fromTo("#topin", {{x: 0}}, {{x: -320, duration: .16, ease: "power3.in", immediateRender: false}}, {ta - .16:.3f});')
                    js(f'tl.fromTo("#topin", {{x: 320}}, {{x: 0, duration: .26, ease: "power3.out", immediateRender: false}}, {ta:.3f});')
                    js(f'tl.set("#topin", {{filter: "none"}}, {ta + .27:.3f});')
                else:                               # zoom through the board, a paper flash, the next one lands
                    js(f'tl.to("#topin", {{scale: 1.35, filter: "blur(14px)", duration: .16, ease: "power2.in"}}, {ta - .16:.3f});')
                    js(f'tl.fromTo("#tflash", {{opacity: 0}}, {{opacity: .9, duration: .05, immediateRender: false}}, {ta - .04:.3f});')
                    js(f'tl.to("#tflash", {{opacity: 0, duration: .22, ease: "power2.out"}}, {ta + .02:.3f});')
                    js(f'tl.fromTo("#topin", {{scale: .82, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .3, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                js(f'tl.fromTo("#botin", {{scale: 1.14}}, {{scale: 1, duration: .3, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
            seam_caps(a, b, tb)
            continue
        js(f'tl.set("#full", {{opacity: 1}}, {ta:.3f});')
        js(f'tl.set("#full", {{opacity: 0}}, {tb:.3f});')
        big_tear(ta, nb)
        nb += 1
        js(f'tl.fromTo("#fullin", {{scale: 1.2, rotation: 1.5}}, {{scale: 1, rotation: 0, duration: .45, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
        starts = [i for i in range(a + 1, b) if W[i - 1]["text"][-1] in ".?।" and not W[i].get("cut")]
        for n, i in enumerate(starts):
            js(f'tl.set("#fullz", {{scale: {1.14 if n % 2 == 0 else 1}}}, {T(i) - .04:.3f});')
        if starts:
            js(f'tl.set("#fullz", {{scale: 1}}, {tb:.3f});')
        full_caps(a, b, tb)
    HIDE.extend(["#split", "#full", "#flash", "#tflash", "#tear", "#tearbig", "#hold"])
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
#top {{ position: absolute; left: 0; top: {BY - 60}px; width: {FW}px; height: {BH + 90}px; overflow: hidden; }}
#topin {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
#paper {{ position: absolute; left: -300px; top: -300px; width: 1700px; height: 2550px; background: url(assets/img/paper/paper.png) 0 0 / 1700px auto;
  filter: sepia(.06) saturate(.8) brightness(1.06); }}
#grid {{ position: absolute; inset: -40px; opacity: .55;
  background-image: linear-gradient(rgba(70,90,130,.22) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(70,90,130,.22) 1.5px, transparent 1.5px);
  background-size: 72px 72px; }}
#stagefit {{ position: absolute; left: 0; top: 60px; width: 1080px; height: {BH}px; }}
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
.note {{ position: absolute; opacity: 0; background: #fbf9f4; padding: 24px 32px 26px; box-shadow: 0 18px 34px rgba(0,0,0,.3); }}
.quote .qmark {{ font: italic 700 130px/0.6 "Play"; color: #e3202f; height: 44px; }}
.quote .qtxt {{ font: 700 37px/1.28 "Inter"; letter-spacing: -.01em; color: #111; }}
.quote .qw {{ display: inline-block; opacity: 0; padding: 0 .06em; }}
.quote .qw.mk {{ background: linear-gradient(transparent 52%, rgba(255,214,0,.85) 52%) 0 0 / 0% 100% no-repeat; }}
.quote .qby {{ font: 500 24px/1.2 "Inter"; color: #666; margin-top: 10px; }}
.mapc {{ height: 460px; padding: 20px; }}
.mapc .map {{ position: absolute; left: 20px; top: 20px; width: 740px; height: 420px; opacity: 1; stroke: #b9b2a5; stroke-width: 14; }}
.mapc .map .main {{ stroke: #111; stroke-width: 22; }}
.pin {{ position: absolute; width: 90px; height: 120px; opacity: 0; z-index: 5; filter: drop-shadow(0 8px 8px rgba(0,0,0,.3)); }}
.pin svg {{ width: 100%; height: 100%; }}
.pin path {{ fill: #e3202f; }}
.pin circle {{ fill: #fff; }}
.num {{ position: absolute; left: 90px; top: 0px; opacity: 0; font: 400 330px/1 "Anton"; color: transparent; -webkit-text-stroke: 10px #111; z-index: 2; }}
.qq {{ font: 800 36px/1.15 "Inter"; letter-spacing: -.02em; }}
.qq span {{ font: 700 italic 32px/1.2 "Play"; color: #e3202f; }}
.logo {{ position: absolute; opacity: 0; background: #fff; padding: 18px; box-shadow: 0 14px 28px rgba(0,0,0,.3); display: grid; place-items: center; }}
.logo img {{ max-width: 100%; max-height: 100%; display: block; }}
.pie {{ position: absolute; left: 470px; top: 160px; width: 210px; height: 210px; opacity: 0; z-index: 6; background: #fbf9f4; border-radius: 50%;
  box-shadow: 0 14px 28px rgba(0,0,0,.3); }}
.pie svg {{ position: absolute; inset: 0; }}
.pie .pbg {{ fill: none; stroke: #e6e0d4; stroke-width: 20; }}
.pie .pfg {{ fill: none; stroke: #e3202f; stroke-width: 20; }}
.pie .pt {{ position: absolute; left: 0; right: 0; top: 60px; text-align: center; font: 400 64px/1 "Anton"; color: #111; }}
.pie .pl {{ position: absolute; left: 0; right: 0; top: 132px; text-align: center; font: 800 22px/1 "Inter"; letter-spacing: .04em; color: #e3202f; }}
.tatabox {{ position: absolute; left: 390px; top: 70px; width: 300px; padding: 24px 0 18px; opacity: 0; z-index: 6; background: #111; color: #fff; text-align: center;
  font: 400 130px/1 "Anton"; letter-spacing: .04em; box-shadow: 0 16px 30px rgba(0,0,0,.35); }}
.doc {{ padding: 24px 34px; }}
.pre-h {{ font: 800 22px/1.2 "Inter"; letter-spacing: .14em; color: #e3202f; margin-bottom: 12px; }}
.pre {{ font: 500 31px/1.36 "Play"; font-style: italic; color: #222; }}
.pre b {{ font-style: normal; font-family: "Anton"; font-weight: 400; letter-spacing: .02em; padding: 0 .1em;
  background: linear-gradient(transparent 50%, rgba(255,214,0,.9) 50%) 0 0 / 0% 100% no-repeat; }}
.hd {{ position: absolute; left: 0; width: {FW}px; top: 215px; text-align: center; opacity: 0; z-index: 8; font: 400 130px/1 "Anton"; color: #111; }}
.hd .r {{ color: #e3202f; }}
#bot {{ position: absolute; left: {CARD[0]}px; top: {CARD[1]}px; width: {CARD[2]}px; height: {CARD[3]}px; background: #fbf9f4; padding: 14px;
  box-shadow: 0 22px 44px rgba(0,0,0,.32); transform: rotate(-.6deg); }}
#bot .tape {{ z-index: 3; top: -24px; width: 220px; margin-left: -110px; }}
#botclip {{ position: absolute; inset: 14px; overflow: hidden; background: #222; }}
#botin {{ position: absolute; inset: 0; transform-origin: 50% 35%; }}
#botin video, #hold {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#hold {{ position: absolute; inset: 0; opacity: 0; }}
#seamline {{ display: none; position: absolute; left: -20px; top: 0; width: {FW + 40}px; height: 34px; z-index: 6; background: #fbf9f4;
  clip-path: polygon(0 30%, 4% 10%, 9% 40%, 14% 15%, 20% 35%, 26% 8%, 31% 30%, 37% 12%, 43% 38%, 49% 10%, 55% 32%, 61% 14%, 67% 36%, 73% 9%, 79% 30%,
  85% 12%, 91% 38%, 96% 14%, 100% 30%, 100% 74%, 95% 92%, 89% 70%, 83% 95%, 77% 72%, 71% 90%, 65% 68%, 59% 94%, 53% 70%, 47% 92%, 41% 66%, 35% 90%,
  29% 70%, 23% 95%, 17% 72%, 11% 92%, 5% 70%, 0 88%); }}
#tear {{ position: absolute; left: -200px; top: -40px; width: 1480px; height: 560px; object-fit: fill; opacity: 0; z-index: 7; filter: drop-shadow(0 10px 20px rgba(0,0,0,.3)); }}
#full {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; background: #222; }}
#fullin, #fullz {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#fullz video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.seam {{ position: absolute; left: 0; width: {FW}px; top: {CARD[1] - 46}px; text-align: center; opacity: 0; z-index: 9; }}
.seam span {{ display: inline-block; background: #000; color: #fff; font: 800 52px/1 "Inter"; padding: 13px 26px 15px; border-radius: 8px; letter-spacing: -.01em; }}
.fcap {{ position: absolute; left: 100px; right: 80px; top: 1290px; opacity: 0; z-index: 9; }}
.fcap .scr {{ font: 400 74px/1.1 "Kaushan"; color: #fff; text-shadow: 0 4px 14px rgba(0,0,0,.6); margin-left: 6px; }}
.fcap .bigw {{ font: 400 150px/1 "Anton"; color: #fff; letter-spacing: .01em; text-shadow: 0 8px 26px rgba(0,0,0,.5); transform-origin: 0 60%; }}
.fcap .bigw.red {{ color: #ff2d3d; text-shadow: 0 4px 0 #fff, 0 10px 30px rgba(0,0,0,.5); }}
#tflash {{ position: absolute; inset: 0; z-index: 8; opacity: 0; background: #fbf9f4; }}
#tearbig {{ position: absolute; left: -500px; top: -500px; width: 2100px; height: 2900px; object-fit: fill; opacity: 0; z-index: 21;
  filter: drop-shadow(0 20px 40px rgba(0,0,0,.35)); }}
.tw {{ position: absolute; opacity: 0; }}
.diya {{ position: absolute; opacity: 0; overflow: visible; }}
.diya .body {{ fill: #b8521f; }}
.diya .rim {{ fill: none; stroke: #e2a33a; stroke-width: 6; }}
.diya .fl {{ transform-origin: 80px 80px; transform-box: view-box; }}
.diya .f1 {{ fill: #ff9a1a; }}
.diya .f2 {{ fill: #fff1a8; }}
.diya .gl {{ fill: rgba(255,190,80,.5); }}
.fw {{ position: absolute; opacity: 0; overflow: visible; stroke-width: 7; stroke-linecap: round; }}
.kand {{ position: absolute; opacity: 0; overflow: visible; transform-origin: 50% 0; }}
.kand .str {{ stroke: #111; stroke-width: 3; fill: none; }}
.kand .lt {{ stroke: #111; stroke-width: 3; }}
.kand .ln {{ stroke: rgba(255,255,255,.8); stroke-width: 3; fill: none; }}
.kand .ts {{ stroke: #d9a520; stroke-width: 4; fill: none; stroke-linecap: round; }}
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
    <svg width="0" height="0" style="position:absolute"><filter id="mbx" x="-30%" y="0" width="160%" height="100%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0 0"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="split">
        <div id="paper"></div><div id="grid"></div>
        <div id="top"><div id="topin"><div id="stagefit"><div id="stagew">{"".join(TOP)}</div></div>
          <img id="tear" src="assets/img/paper/scrap/white-1.png" alt=""><div id="tflash"></div></div></div>
        <div id="bot"><i class="tape"></i><div id="botclip"><div id="botin"><video id="vsplit" class="clip" src="assets/video/face_split.mp4" data-start="0" data-duration="{VDUR}" data-track-index="2" muted playsinline></video>
          <img id="hold" src="assets/img/hold/last_split.png" alt=""></div></div></div>
        <div id="seamline"></div>
      </div>
      <div id="full"><div id="fullin"><div id="fullz"><video id="vfull" class="clip" src="assets/video/face_full.mp4" data-start="0" data-duration="{VDUR}" data-track-index="1" muted playsinline></video></div></div></div>
      {"".join(POST)}
      <img id="tearbig" src="assets/img/paper/scrap/white-0.png" alt=""><div id="flash"></div><div id="grain"></div>
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
