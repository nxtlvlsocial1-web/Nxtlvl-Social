"""Political opinion reel (Diwali, "buy only from tilak-wearing sellers" rebuttal), 9:16, 1080x1920. Writes index.html.

Owner's brief and notes so far:
- Talking head, gaps trimmed and the take at 1.1x (build/tight.py), the voice cleaned.
- Top half: the boards (Ashke paper format: grid paper, torn scraps, photo prints, stepped motion), shown inside the
  Reels safe area (the 1080x960 board is drawn at 0.75 from y 230, so nothing sits under the Reels top bar or the
  right-hand buttons). Bottom half: her video, full width, hands in frame.
- v4 (owner): no words on the boards that she also says (the captions carry the words): every board tells its line
  with pictures instead; no captions while the quote card is up; captions everywhere else, white bold type with a
  black outline (the owner's reference); real sound effects (CC0, OpenGameArt: Openverse's Freesound files refuse
  downloads from the cloud) via build/sfx_sheet.py and the real-sfx mixer.
Images: the owner's (assets/img/ref, assets/img/logos; not in git).

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
SX, SY, SS = 135, 230, .75         # v4: the 1080x960 board drawn at 0.75 from (135, 230): inside the Reels safe area
DUR = round(VDUR + 1.0, 3)          # the last board holds a second on her last frame
A, HIDE, TOP, POST, CUES = [], [], [], [], []
NID = [0]
RND = random.Random(5)


def T(i):
    return W[i]["s"]


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def cue(t, kind):
    CUES.append((round(t, 3), kind))


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
    cue(t, "paper")
    js(f'tl.to("#{i}", {{rotation: {rot - 1.2}, y: -8, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: 3}}, {t + .45:.3f});')
    if color_at is not None:
        js(f'tl.to("#{i} img", {{filter: "grayscale(0) contrast(1.05)", duration: .4, ease: {ST(.4, "power2.out")}}}, {color_at:.3f});')
        cue(color_at, "shimmer")
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
    cue(t, "marker")
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


def diya(x, y, w, t, t1, z=7, lit_at=None):
    """A clay diya whose flame flickers (lit_at: it sits unlit until then and lights with a soft chime)."""
    i = nid("dy")
    TOP.append(f'<svg class="diya" id="{i}" viewBox="0 0 160 130" style="left:{x}px;top:{y}px;width:{w}px;height:{w * 130 / 160:.0f}px;z-index:{z}">'
               f'<ellipse class="gl" cx="80" cy="52" rx="44" ry="44"/>'
               f'<path class="body" d="M 8 78 C 24 124 136 124 152 78 C 120 92 40 92 8 78 Z"/><path class="rim" d="M 8 78 C 40 92 120 92 152 78"/>'
               f'<g class="fl"><path class="f1" d="M 80 80 C 58 62 68 34 80 12 C 92 34 102 62 80 80 Z"/><path class="f2" d="M 80 78 C 70 66 74 50 80 38 C 86 50 90 66 80 78 Z"/></g></svg>')
    slap(i, t, 0, d=.3, frm=1.6)
    if lit_at is not None:
        js(f'tl.set("#{i} .fl, #{i} .gl", {{opacity: 0}}, {t:.3f});')
        js(f'tl.fromTo("#{i} .fl, #{i} .gl", {{opacity: 0, scale: 0}}, {{opacity: 1, scale: 1, duration: .25, ease: {ST(.25, "back.out(2)")}, immediateRender: false}}, {lit_at:.3f});')
        cue(lit_at, "chime")
        t = lit_at
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
    for k in range(min(2, reps + 1)):
        cue(t0 + k * period, "firework")
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
    cue(t, "pop")
    return i


def coin(x, y, sz, t, t1, z=6):
    """A gold coin that drops in, bounces and keeps spinning."""
    i = nid("cn")
    TOP.append(f'<div class="coin" id="{i}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;font-size:{sz * .55:.0f}px;z-index:{z}">&#8377;</div>')
    js(f'tl.fromTo("#{i}", {{opacity: 1, y: -700}}, {{opacity: 1, y: 0, duration: .55, ease: {ST(.55, "bounce.out")}, immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#{i}", {{scaleX: 1}}, {{scaleX: .1, duration: .3, ease: "sine.inOut", yoyo: true, repeat: {max(1, int((t1 - t - .6) / .3))}, immediateRender: false}}, {t + .6:.3f});')
    HIDE.append(f"#{i}")
    cue(t + .3, "coin")
    return i


def icon(paths, x, y, w, h, vb, t, stroke="#111", sw=8, z=5, d=.45, bob=True, t1=None, snd="pop"):
    """A hand-drawn icon that draws itself on, pops, then floats."""
    i = draw(paths, x, y, w, h, vb, t, d=d, z=z, stroke=stroke, sw=sw)
    js(f'tl.fromTo("#{i}", {{scale: 1.25, rotation: 6}}, {{scale: 1, rotation: 0, duration: .3, ease: {ST(.3)}, immediateRender: false}}, {t:.3f});')
    if bob:
        js(f'tl.to("#{i}", {{y: -10, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: 5}}, {t + .5:.3f});')
    if snd:
        cue(t, snd)
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
# v4: 1080x960 boards (drawn at 0.75 inside the safe area). No word she says is written on a board: the captions
# carry the words, the boards tell the line in pictures.
PERSON = "M 50 30 A 18 18 0 1 1 50.1 30 M 50 52 L 50 110 M 50 70 L 22 92 M 50 70 L 78 92 M 50 110 L 30 150 M 50 110 L 70 150"
ELDER = PERSON + " M 78 92 L 86 152"
LAMP = "M 78 92 L 90 106 L 78 120 L 66 106 Z"
BUBBLE = "M 40 20 H 400 Q 430 20 430 50 V 230 Q 430 260 400 260 H 160 L 90 320 L 110 260 H 40 Q 10 260 10 230 V 50 Q 10 20 40 20 Z"
TILAK = ["M 120 70 C 120 160 160 185 175 185 C 190 185 230 160 230 70", "M 175 210 A 10 10 0 1 1 175.1 210"]
BAG = ["M 280 110 H 380 L 372 230 H 288 Z", "M 305 110 C 305 76 355 76 355 110"]
CHECK = ["M 300 170 L 325 196 L 365 140"]
HOUSE = ["M 40 200 L 40 400 L 360 400 L 360 200", "M 16 214 L 200 60 L 384 214", "M 160 400 L 160 300 L 240 300 L 240 400",
         "M 70 250 L 130 250 L 130 300 L 70 300 Z", "M 270 250 L 330 250 L 330 300 L 270 300 Z"]
SKYLINE = ["M 0 300 V 170 H 70 V 300", "M 70 300 V 100 H 150 V 300", "M 150 300 V 200 H 220 V 300", "M 220 300 V 50 H 280 V 300",
           "M 280 300 V 150 H 370 V 300", "M 370 300 V 220 H 440 V 300", "M 440 300 V 120 H 520 V 300", "M 520 300 V 190 H 600 V 300",
           "M 600 300 V 80 H 660 V 300", "M 660 300 V 170 H 760 V 300", "M 760 300 V 230 H 840 V 300", "M 840 300 V 140 H 920 V 300",
           "M 0 300 H 920"]
AWNING = ["M 0 40 L 200 40 L 180 0 L 20 0 Z", "M 0 40 Q 25 72 50 40 Q 75 72 100 40 Q 125 72 150 40 Q 175 72 200 40",
          "M 20 46 L 20 200 M 180 46 L 180 200", "M 0 200 L 200 200"]
TV = ["M 10 10 H 190 V 130 H 10 Z", "M 70 170 H 130 M 100 130 V 170"]
PHONE = ["M 30 2 H 90 Q 100 2 100 12 V 168 Q 100 178 90 178 H 30 Q 20 178 20 168 V 12 Q 20 2 30 2 Z", "M 50 160 H 70"]
LAPTOP = ["M 30 10 H 170 V 110 H 30 Z", "M 0 130 H 200 L 185 145 H 15 Z"]
KURTA = ["M 220 40 C 220 20 245 15 250 32 C 255 48 235 55 225 62 L 220 80", "M 220 80 L 130 150 L 310 150",
         "M 200 150 L 140 180 L 110 260 L 150 270 L 160 230 L 160 420 L 280 420 L 280 230 L 290 270 L 330 260 L 300 180 L 240 150 Q 220 175 200 150 Z"]
NECK = ["M 30 30 C 60 170 240 170 270 30", "M 150 150 L 150 165", "M 150 185 A 18 18 0 1 1 150.1 185"]
MEDAL = ["M 100 70 A 60 60 0 1 1 100.1 70", "M 88 52 L 104 40 L 104 102 M 90 102 L 118 102", "M 70 120 L 50 205 L 78 190 L 92 214 L 98 130", "M 130 120 L 150 205 L 122 190 L 108 214 L 102 130"]
CROSS = ["M 20 20 L 380 230", "M 380 20 L 20 230"]
ROCKET = "M 0 0 L 14 -40 L 28 0 Z M 14 0 L 14 30"


def people_row(x0, y0, h, t, gap=150, n=3, stroke="#111"):
    for k in range(n):
        icon([PERSON], x0 + k * gap, y0, h * .66, h, "0 0 100 160", t + k * .12, stroke=stroke, sw=7, snd="pop" if k == 0 else None)


def boards():
    S = {s[5]: s for s in SECS if s[5]}

    # 1. The hook (no captions while it is up): her quote typed on as she says it, the key words marked, diyas
    _, ta, tb, a, b, _ = S["quote"]
    group("quote", ta, tb)
    scrap("red", 0, 40, 120, 600, -8, ta + .05, z=1)
    scrap("grey", 2, 600, 480, 420, 7, ta + .12, z=1)
    words = [j for j in range(1, 24)]
    body = " ".join(f'<span class="qw{" mk" if j in (15, 19, 20, 21) else ""}" id="qw{j}">{word(j)}</span>' for j in words)
    card(f'<div class="qmark">&ldquo;</div><div class="qtxt">{body}</div>', 110, 150, 860, ta + .08, rot=-2, z=3, cls="note quote")
    cue(ta + .08, "paper")
    words_on("qw", words)
    marker("#qw15", T(15) + .05)
    for j in (19, 20, 21):
        marker(f"#qw{j}", T(j) + .02, .18)
    cue(T(15) + .05, "marker")
    diya(60, 700, 170, ta + .4, tb)
    diya(850, 710, 160, ta + .55, tb)
    twinkle(6, ta, tb, area=(60, 40, 960, 90))
    end_group()

    # 2. Who said it: his photo, circled; a speech bubble says it in pictures (a tilak, a shopping bag ticked)
    _, ta, tb, a, b, _ = S["rane"]
    group("rane", ta, tb)
    scrap("red", 1, 30, 120, 600, -10, ta + .03, z=1)
    prt("assets/img/ref/speaker_face.jpg", 90, 150, 440, 520, -4, ta + .06, z=3)
    circle(20, 90, 600, 640, T(40) + .05)
    icon([BUBBLE], 560, 160, 460, 345, "0 0 440 330", T(37) - .1, stroke="#111", sw=7, bob=False)
    icon(TILAK, 560, 160, 460, 345, "0 0 440 330", T(38), stroke="#e3202f", sw=14, bob=False, snd=None)
    icon(BAG, 560, 160, 460, 345, "0 0 440 330", T(39), stroke="#111", sw=8, bob=False, snd=None)
    icon(CHECK, 560, 160, 460, 345, "0 0 440 330", T(40), stroke="#18a058", sw=12, bob=False, snd="tick")
    end_group()

    def chapter2(board, num, at):
        _, ta, tb, a, b, _ = S[board]
        group(board, ta, tb)
        scrap("black", 1, 500, 280, 520, -6, ta + .05, z=1)
        i = nid("num")
        TOP.append(f'<div class="num" id="{i}">{num}</div>')
        slap(i, ta + .02, -4, d=.4, frm=1.6)
        cue(ta + .02, "hit")
        people_row(540, 330, 260, at, gap=160, stroke="#fff")
        draw(["M 30 40 C 200 10 420 60 600 30"], 470, 660, 560, 70, "0 0 640 70", at + .4, d=.35)
        diya(120, 690, 140, at + .2, tb)
        twinkle(6, ta, tb)
        end_group()

    # 3. Chapter one: the number and the community, as people
    chapter2("ch1", "01", T(61) - .04)

    # 4. Pataake: rockets go up over a Mumbai skyline and burst; the biggest market gets a #1 medal
    _, ta, tb, a, b, _ = S["crackers"]
    group("crackers", ta, tb)
    scrap("white", 0, 50, 90, 980, -2, ta + .03, z=1)
    icon(SKYLINE, 80, 520, 920, 300, "0 0 920 300", T(76) - .1, stroke="#111", sw=6, bob=False, snd="whoosh")
    for k, (x, tk) in enumerate([(240, T(70) - .2), (560, T(70) + .1), (840, T(71) - .1)]):
        i = nid("rk")
        TOP.append(f'<svg class="rk" id="{i}" viewBox="-5 -45 40 80" style="left:{x}px;top:640px;width:46px;height:90px;z-index:5">'
                   f'<path d="{ROCKET}"/></svg>')
        js(f'tl.fromTo("#{i}", {{opacity: 1, y: 0}}, {{opacity: 0, y: -440, duration: .5, ease: "power2.in", immediateRender: false}}, {tk:.3f});')
        HIDE.append(f"#{i}")
        cue(tk, "rocket")
    firework(262, 230, 150, T(70) + .3, tb, "#e3202f", 1.0)
    firework(582, 180, 120, T(70) + .6, tb, "#d9a520", 1.2)
    firework(862, 240, 160, T(71) + .4, tb, "#111", 0.9)
    icon(MEDAL, 800, 470, 200, 220, "0 0 200 220", T(85) - .05, stroke="#d9a520", sw=10, bob=True, snd="stamp")
    twinkle(6, ta, tb)
    end_group()

    # 5. Mohammad Ali Road: the owner's photo (Minara Masjid over the market), the pin drops, shopfronts draw on
    _, ta, tb, a, b, _ = S["mar"]
    group("mar", ta, tb)
    scrap("black", 0, 40, 60, 560, -9, ta + .03, z=1)
    prt("assets/img/ref/mohammad_ali_road.jpg", 90, 70, 520, 690, -3, ta + .05, z=3, bw=True, color_at=T(89) + .1)
    i = nid("pin")
    TOP.append(f'<div class="pin" id="{i}" style="left:470px;top:150px"><svg viewBox="0 0 60 80"><path d="M30 78 C 30 78 4 46 4 28 A 26 26 0 1 1 56 28 '
               f'C 56 46 30 78 30 78 Z"/><circle cx="30" cy="28" r="10"/></svg></div>')
    js(f'tl.fromTo("#{i}", {{opacity: 0, y: -260}}, {{opacity: 1, y: 0, duration: .4, ease: {ST(.4, "bounce.out")}, immediateRender: false}}, {T(89) - .05:.3f});')
    cue(T(89) + .2, "pop")
    for k, (x, y) in enumerate([(680, 150), (800, 360), (680, 570)]):
        icon(AWNING, x, y, 240, 250, "0 0 200 210", T(97) + k * .25, stroke="#e3202f" if k % 2 == 0 else "#111", sw=7, snd="pop" if k == 0 else None)
    twinkle(7, ta, tb, area=(90, 70, 520, 600), colors=("#ffd34d", "#fff"))
    end_group()

    # 6. Kandil: a house draws on, a kandil hangs outside it, the stall print turns to colour
    _, ta, tb, a, b, _ = S["kandil"]
    group("kandil", ta, tb)
    scrap("black", 2, 40, 420, 520, 6, ta + .03, z=1)
    prt("assets/img/ref/attar_kandil_lanterns_pune.jpg", 80, 110, 520, 360, -3, ta + .05, z=3, color_at=T(116) - .05)
    icon(HOUSE, 600, 300, 420, 440, "0 0 400 420", T(113) - .1, stroke="#111", sw=8, bob=False, snd="whoosh")
    lantern(740, 360, 80, T(115), tb, "#e3202f", z=6, string=60)
    lantern(880, 360, 80, T(116), tb, "#d9a520", z=6, string=60)
    lantern(60, 40, 90, ta + .3, tb, "#d9a520")
    lantern(940, 40, 80, T(119), tb, "#111")
    twinkle(6, ta, tb)
    end_group()

    # 7. Attar community, Pune: three generations, each holding a kandil, along a time arrow
    _, ta, tb, a, b, _ = S["attar"]
    group("attar", ta, tb)
    scrap("red", 2, 50, 260, 980, -3, ta + .03, z=1)
    prt("assets/img/ref/attar_kandil_lanterns_pune.jpg?v=2", 700, 40, 320, 220, 6, ta + .02, z=2, bw=False)
    for k, (path, x, sz, tk) in enumerate([(ELDER, 130, 330, T(130)), (PERSON, 430, 300, T(131) + .1), (PERSON, 720, 220, T(133))]):
        icon([path, LAMP], x, 300 + (330 - sz), sz * .66, sz, "0 0 100 160", tk, stroke="#fff", sw=6, snd="pop")
    draw(["M 120 720 L 960 720", "M 960 720 L 925 698 M 960 720 L 925 742"], 0, 0, 1080, 960, "0 0 1080 960", T(130), d=.6, z=4, stroke="#fff", sw=8)
    lantern(80, 60, 90, ta + .2, tb, "#e3202f")
    end_group()

    # 8. Crawford Market: the print; half of Mumbai on the dial; shopping bags drop in; the shops circled
    _, ta, tb, a, b, _ = S["crawford"]
    group("crawford", ta, tb)
    scrap("grey", 1, 30, 80, 700, -6, ta + .03, z=1)
    prt("assets/img/ref/crawford_market.jpg", 90, 100, 900, 560, 2, ta + .05, z=3)
    i = nid("pie")
    TOP.append(f'<div class="pie" id="{i}"><svg viewBox="0 0 200 200"><circle class="pbg" cx="100" cy="100" r="78"/>'
               f'<circle class="pfg" cx="100" cy="100" r="78" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg>'
               f'<div class="pt">&frac12;+</div></div>')
    slap(i, T(162) - .05, -4, d=.3, frm=1.5)
    js(f'tl.fromTo("#{i} .pfg", {{strokeDashoffset: 1}}, {{strokeDashoffset: .4, duration: .6, ease: {ST(.6, "power2.out")}, immediateRender: false}}, {T(162):.3f});')
    cue(T(162), "tick")
    for k, x in enumerate([130, 330, 530]):
        i = icon(BAG, x, 560, 200, 240, "270 60 120 190", T(169) + k * .15, stroke="#e3202f" if k % 2 else "#111", sw=7, bob=False, snd="thud" if k == 0 else None)
        js(f'tl.fromTo("#{i}", {{y: -400}}, {{y: 0, duration: .45, ease: {ST(.45, "bounce.out")}, immediateRender: false}}, {T(169) + k * .15:.3f});')
    js(f'tl.to("#{i}", {{opacity: 0, duration: .2}}, {T(188) - .3:.3f});')
    circle(60, 60, 960, 640, T(192) - .03)
    twinkle(6, ta, tb, area=(100, 120, 880, 500), colors=("#ffd34d", "#e3202f"))
    end_group()

    # 9. Chapter two
    chapter2("ch2", "02", T(202) - .04)

    # 10. Dhanteras: gold coins drop and spin, a necklace draws on, then Tanishq
    _, ta, tb, a, b, _ = S["tanishq"]
    group("tanishq", ta, tb)
    scrap("black", 3, 40, 100, 520, -7, ta + .03, z=1)
    icon(NECK, 80, 160, 420, 280, "0 0 300 200", T(212) - .1, stroke="#d9a520", sw=9, snd="shimmer")
    for k, (x, y, sz, tk) in enumerate([(110, 520, 150, T(215)), (290, 560, 130, T(215) + .2), (440, 500, 160, T(216))]):
        coin(x, y, sz, tk, tb)
    logo("tanishq", 590, 230, 400, 400, T(229) - .04, rot=-3, z=6)
    circle(540, 190, 500, 480, T(229) + .2)
    twinkle(8, ta, tb, colors=("#d9a520", "#ffd34d", "#e3202f"))
    end_group()

    # 11. Electronics: a TV, a phone and a laptop pop up, then Croma
    _, ta, tb, a, b, _ = S["croma"]
    group("croma", ta, tb)
    scrap("red", 3, 520, 140, 520, 6, ta + .03, z=1)
    icon(TV, 70, 130, 340, 306, "0 0 200 180", T(233) - .05, sw=8)
    icon(PHONE, 330, 420, 170, 255, "0 0 120 180", T(233) + .15, sw=8, snd=None)
    icon(LAPTOP, 60, 500, 300, 225, "0 0 200 150", T(233) + .3, sw=8, snd=None)
    logo("croma", 560, 260, 420, 420, T(245) - .04, rot=3, z=6)
    circle(510, 230, 520, 480, T(245) + .2)
    twinkle(5, ta, tb)
    end_group()

    # 12. New clothes: a kurta on a hanger swings, then Westside and Zudio
    _, ta, tb, a, b, _ = S["wz"]
    group("wz", ta, tb)
    scrap("grey", 3, 40, 420, 620, -5, ta + .03, z=1)
    k_ = icon(KURTA, 60, 80, 420, 420, "0 0 440 440", T(251) - .05, stroke="#e3202f", sw=9, bob=False, snd="swish")
    js(f'tl.fromTo("#{k_}", {{rotation: -7, transformOrigin: "50% 8%"}}, {{rotation: 7, duration: .9, ease: "sine.inOut", yoyo: true, repeat: 7, immediateRender: false}}, {T(251) + .5:.3f});')
    logo("westside", 560, 120, 400, 400, T(265) - .04, rot=-4, z=6)
    logo("zudio", 130, 590, 460, 120, T(267) - .04, rot=3, z=7)
    twinkle(5, ta, tb)
    end_group()

    # 13. All of them: the four logos, lines meet in one family (three people in a box)
    _, ta, tb, a, b, _ = S["tata"]
    group("tata", ta, tb)
    for k, (n, x, y, w, h, r) in enumerate([("tanishq", 60, 90, 250, 250, -4), ("croma", 770, 90, 250, 250, 4),
                                            ("westside", 60, 560, 250, 250, 3), ("zudio", 730, 680, 300, 80, -3)]):
        logo(n, x, y, w, h, ta + .05 + k * .1, rot=r, z=4)
    draw(["M 310 220 L 430 380", "M 770 220 L 650 380", "M 310 680 L 430 560", "M 760 690 L 650 560"], 0, 0, 1080, 960, "0 0 1080 960",
         T(283) - .05, d=.3, z=3, stroke="#111", sw=7)
    cue(T(283) - .05, "marker")
    i = nid("fam")
    TOP.append(f'<div class="fambox" id="{i}"><svg viewBox="0 0 300 170">'
               + "".join(f'<path transform="translate({20 + k * 90} 5) scale(.9)" d="{PERSON}"/>' for k in range(3)) + '</svg></div>')
    slap(i, T(285) - .05, -3, d=.36, frm=2)
    cue(T(285) - .05, "stamp")
    twinkle(6, ta, tb)
    end_group()

    # 14. Secular: the Preamble, SECULAR marked; then a little copy of the quote, crossed out
    _, ta, tb, a, b, _ = S["secular"]
    group("secular", ta, tb)
    scrap("red", 0, 600, 80, 460, 8, ta + .03, z=1)
    card('<div class="pre-h">THE CONSTITUTION OF INDIA &middot; PREAMBLE</div><div class="pre">WE, THE PEOPLE OF INDIA, having solemnly resolved to '
         'constitute India into a SOVEREIGN SOCIALIST <b id="sec">SECULAR</b> DEMOCRATIC REPUBLIC and to secure to all its citizens: JUSTICE, '
         'social, economic and political; LIBERTY of thought, expression, belief, faith and worship&hellip;</div>',
         110, 90, 860, ta + .05, rot=-2, z=3, cls="note doc")
    cue(ta + .05, "paper")
    marker("#sec", T(337) - .05, .35)
    cue(T(337) - .05, "marker")
    mini = " ".join(word(j) for j in range(1, 11))
    card(f'<div class="mini">&ldquo;{mini}&hellip;&rdquo;</div>', 540, 560, 440, T(340) - .05, rot=4, z=5)
    cue(T(340) - .05, "paper")
    icon(CROSS, 520, 540, 480, 300, "0 0 400 250", T(342) - .05, stroke="#e3202f", sw=16, z=7, bob=False, snd="hit")
    end_group()

    # 15. The close: six diyas, one lights for each community she names; a rangoli draws on; fireworks
    _, ta, tb, a, b, _ = S["names"]
    group("names", ta, tb)
    scrap("white", 2, 30, 90, 1020, -2, ta + .03, z=1)
    for k, j in enumerate(range(355, 361)):
        diya(70 + k * 160, 280 + (40 if k % 2 else 0), 140, ta + .1 + k * .06, DUR, lit_at=T(j) - .02)
    rang = []
    import math
    for k in range(8):
        a_ = k / 8 * 6.283
        cx, cy = 540 + math.cos(a_) * 120, 700 + math.sin(a_) * 120
        rang.append(f"M 540 700 Q {540 + math.cos(a_ - .4) * 150:.0f} {700 + math.sin(a_ - .4) * 150:.0f} {cx + math.cos(a_) * 60:.0f} {cy + math.sin(a_) * 60:.0f} "
                    f"Q {540 + math.cos(a_ + .4) * 150:.0f} {700 + math.sin(a_ + .4) * 150:.0f} 540 700")
    icon(rang, 290, 450, 500, 500, "290 450 500 500", T(365) - .05, stroke="#e3202f", sw=8, bob=False, snd="chime", d=.6)
    icon(["M 540 640 A 60 60 0 1 1 540.1 640", "M 540 610 A 90 90 0 1 1 540.1 610"], 290, 450, 500, 500, "290 450 500 500", T(365) + .2,
         stroke="#d9a520", sw=8, bob=False, snd=None, d=.5)
    firework(150, 140, 130, T(365) - .1, DUR, "#e3202f", .9, z=2)
    firework(930, 160, 150, T(365) + .2, DUR, "#d9a520", 1.0, z=2)
    firework(880, 700, 110, T(366), DUR, "#111", 1.1, z=2)
    twinkle(10, ta, DUR)
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


def caps(a, b, tend, where):
    """v4 (owner's reference): white bold words with a black outline, one line of up to five words. On split screens
    they sit on the seam (above her head), on full-frame shots over her chest; both inside the safe area."""
    ch = chunks(a, b, maxw=4, maxc=24)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        i = nid("cp")
        txt = " ".join(word(j) for j in c)
        POST.append(f'<div class="cap {where}" id="{i}"><span>{txt}</span></div>')
        show(f"#{i}", t0, t1)
        js(f'tl.fromTo("#{i} span", {{scale: .9, y: 8}}, {{scale: 1, y: 0, duration: .14, ease: "power3.out", immediateRender: false}}, {t0:.3f});')


# ------------------------------------------------------------------------------------------------ layout + transitions
TEAR = ["white-1", "grey-0", "red-2", "black-0", "white-3", "grey-2"]


def big_tear(t, n):
    """Full frame to split and back: a big torn sheet sweeps across the whole screen; the cut happens under it."""
    cue(t - .3, "tear_big")
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
                cue(ta - .2, {"tear": "tear", "whip": "whoosh", "zoom": "zoom"}[kind2])
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
            if board != "quote":            # v4 (owner): no captions while the quote card is up
                caps(a, b, tb, "seam")
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
        caps(a, b, tb, "low")
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
#top {{ position: absolute; left: 0; top: 0; width: {FW}px; height: 960px; overflow: hidden; }}
#topin {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
#paper {{ position: absolute; left: -300px; top: -300px; width: 1700px; height: 2550px; background: url(assets/img/paper/paper.png) 0 0 / 1700px auto;
  filter: sepia(.06) saturate(.8) brightness(1.06); }}
#grid {{ position: absolute; inset: -40px; opacity: .55;
  background-image: linear-gradient(rgba(70,90,130,.22) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(70,90,130,.22) 1.5px, transparent 1.5px);
  background-size: 72px 72px; }}
#stagefit {{ position: absolute; left: {SX}px; top: {SY}px; width: 1080px; height: 960px; transform: scale({SS}); transform-origin: 0 0; }}
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
.quote .qtxt {{ font: 700 56px/1.3 "Inter"; letter-spacing: -.01em; color: #111; }}
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
.num {{ position: absolute; left: 80px; top: 230px; opacity: 0; font: 400 420px/1 "Anton"; color: transparent; -webkit-text-stroke: 10px #111; z-index: 2; }}
.qq {{ font: 800 36px/1.15 "Inter"; letter-spacing: -.02em; }}
.qq span {{ font: 700 italic 32px/1.2 "Play"; color: #e3202f; }}
.logo {{ position: absolute; opacity: 0; background: #fff; padding: 18px; box-shadow: 0 14px 28px rgba(0,0,0,.3); display: grid; place-items: center; }}
.logo img {{ max-width: 100%; max-height: 100%; display: block; }}
.pie {{ position: absolute; left: 720px; top: 500px; width: 290px; height: 290px; opacity: 0; z-index: 6; background: #fbf9f4; border-radius: 50%;
  box-shadow: 0 14px 28px rgba(0,0,0,.3); }}
.pie svg {{ position: absolute; inset: 0; }}
.pie .pbg {{ fill: none; stroke: #e6e0d4; stroke-width: 20; }}
.pie .pfg {{ fill: none; stroke: #e3202f; stroke-width: 20; }}
.pie .pt {{ position: absolute; left: 0; right: 0; top: 92px; text-align: center; font: 400 104px/1 "Anton"; color: #111; }}
.pie .pl {{ position: absolute; left: 0; right: 0; top: 132px; text-align: center; font: 800 22px/1 "Inter"; letter-spacing: .04em; color: #e3202f; }}
.tatabox {{ position: absolute; left: 390px; top: 70px; width: 300px; padding: 24px 0 18px; opacity: 0; z-index: 6; background: #111; color: #fff; text-align: center;
  font: 400 130px/1 "Anton"; letter-spacing: .04em; box-shadow: 0 16px 30px rgba(0,0,0,.35); }}
.doc {{ padding: 40px 46px; }}
.pre-h {{ font: 800 28px/1.2 "Inter"; letter-spacing: .14em; color: #e3202f; margin-bottom: 22px; }}
.pre {{ font: 500 44px/1.38 "Play"; font-style: italic; color: #222; }}
.pre b {{ font-style: normal; font-family: "Anton"; font-weight: 400; letter-spacing: .02em; padding: 0 .1em;
  background: linear-gradient(transparent 50%, rgba(255,214,0,.9) 50%) 0 0 / 0% 100% no-repeat; }}
.hd {{ position: absolute; left: 0; width: {FW}px; top: 215px; text-align: center; opacity: 0; z-index: 8; font: 400 130px/1 "Anton"; color: #111; }}
.hd .r {{ color: #e3202f; }}
#bot {{ position: absolute; left: 0; top: 960px; width: {FW}px; height: 960px; overflow: hidden; background: #222; }}
#botclip {{ position: absolute; inset: 0; }}
#botin {{ position: absolute; inset: 0; transform-origin: 50% 35%; }}
#botin video, #hold {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#hold {{ position: absolute; inset: 0; opacity: 0; }}
#seamline {{ position: absolute; left: -20px; top: 944px; width: {FW + 40}px; height: 34px; z-index: 6; background: #fbf9f4;
  clip-path: polygon(0 30%, 4% 10%, 9% 40%, 14% 15%, 20% 35%, 26% 8%, 31% 30%, 37% 12%, 43% 38%, 49% 10%, 55% 32%, 61% 14%, 67% 36%, 73% 9%, 79% 30%,
  85% 12%, 91% 38%, 96% 14%, 100% 30%, 100% 74%, 95% 92%, 89% 70%, 83% 95%, 77% 72%, 71% 90%, 65% 68%, 59% 94%, 53% 70%, 47% 92%, 41% 66%, 35% 90%,
  29% 70%, 23% 95%, 17% 72%, 11% 92%, 5% 70%, 0 88%); }}
#tear {{ position: absolute; left: -200px; top: 120px; width: 1480px; height: 860px; object-fit: fill; opacity: 0; z-index: 7; filter: drop-shadow(0 10px 20px rgba(0,0,0,.3)); }}
#full {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; background: #222; }}
#fullin, #fullz {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#fullz video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
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
.cap {{ position: absolute; left: 60px; right: 140px; text-align: center; opacity: 0; z-index: 12; }}
.cap.seam {{ top: 905px; }}
.cap.low {{ top: 1330px; }}
.cap span {{ display: inline-block; font: 800 60px/1.12 "Inter"; color: #fff; letter-spacing: -.01em;
  text-shadow: 4px 0 0 #000, -4px 0 0 #000, 0 4px 0 #000, 0 -4px 0 #000, 3px 3px 0 #000, -3px 3px 0 #000, 3px -3px 0 #000, -3px -3px 0 #000,
  2px 4px 0 #000, -2px 4px 0 #000, 4px 2px 0 #000, -4px 2px 0 #000, 0 7px 14px rgba(0,0,0,.6); }}
.coin {{ position: absolute; opacity: 0; border-radius: 50%; background: #e7b320; border: 6px solid #b8860b; color: #8a5a00; display: grid; place-items: center;
  font-family: "Inter"; font-weight: 800; box-shadow: inset 0 -8px 0 rgba(0,0,0,.12), 0 10px 18px rgba(0,0,0,.25); }}
.rk {{ position: absolute; opacity: 0; fill: #e3202f; stroke: #111; stroke-width: 3; overflow: visible; }}
.m1 {{ position: absolute; left: 860px; top: 506px; width: 80px; text-align: center; opacity: 0; z-index: 7; font: 400 92px/1 "Anton"; color: #b8860b; }}
.fambox {{ position: absolute; left: 380px; top: 360px; width: 320px; height: 210px; padding: 20px 10px; opacity: 0; z-index: 6; background: #111;
  box-shadow: 0 16px 30px rgba(0,0,0,.35); }}
.fambox svg {{ width: 100%; height: 100%; fill: none; stroke: #fff; stroke-width: 7; stroke-linecap: round; }}
.mini {{ font: 700 30px/1.3 "Inter"; color: #333; }}
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
        <div id="bot"><div id="botclip"><div id="botin"><video id="vsplit" class="clip" src="assets/video/face_split.mp4" data-start="0" data-duration="{VDUR}" data-track-index="2" muted playsinline></video>
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
    ev = sorted(({"t": t, "type": k} for t, k in CUES if 0 <= t < DUR), key=lambda e: e["t"])
    json.dump(ev, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SECS)} sections, {DUR} s, {len(ev)} sound moments")


if __name__ == "__main__":
    main()
