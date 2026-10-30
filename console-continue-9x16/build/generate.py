"""Writes index.html: the "Continue?" Reel for AI.NXTLVL (console-skill) as one HyperFrames composition.

python3 build/generate.py      (from the project root, after build/voice.py)

The whole Reel plays like an original early-2000s game on a bright lavender-white stage: GAME OVER and a chrome
countdown, Player 2 (Claude) joins, the title screen, a loading screen, the inventory, a boss fight, the New Game+ world
map, an early-access stamp and the countdown again for the CTA. 3D props live in assets/js/world.js (canvas #gl); this
file writes the 2D layer (headers, HUD, cards, the dialogue-box captions) and one GSAP timeline. Layout keeps fixed
zones so nothing crowds: headers 290-500 px, the visual 520-1250 px, captions 1290-1460 px.
Writes build/cues.json (scene cuts and sound events) for build/audio.py.
"""
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
W = json.load(open(os.path.join(B, "words.json")))
w = [x["s"] for x in W]
DUR = 39.4
R = random.Random(5)
INK, VIO, PAPER, RED = "#1d1a26", "#7a2ffb", "#ffffff", "#e0335a"

A, HIDE, EV = [], [], []


def js(s):
    A.append("      " + s)


def ev(t, kind):
    EV.append((round(t, 3), kind))


S = {}
order = [("A", 0), ("B", w[10] - .02), ("C1", w[17] - .04), ("C2", w[25] - .04), ("D", w[37] - .04), ("E", w[53] - .04),
         ("F", w[63] - .04), ("G", w[77] - .04), ("H", w[87] - .04)]
for i, (k, a) in enumerate(order):
    S[k] = [round(a, 3), round(order[i + 1][1] if i + 1 < len(order) else DUR, 3)]

count = [["9", 0.0], ["8", .8], ["7", 1.55], ["6", 2.3], ["5", w[9]], ["4", w[9] + .16], ["3", w[9] + .32], ["2", w[9] + .48], ["1", w[9] + .64]]
count2 = [["3", S["H"][0]], ["2", w[88] - .2]]
hits = [w[58], w[60], w[61], w[62]]
ko = round(w[62] + .32, 3)
unlock = [w[70], w[71], w[72], w[76]]
CT = {"S": S, "w": w, "count": count, "count2": count2, "burst": w[88], "press": w[90], "hits": hits, "ko": ko, "unlock": unlock}

SCENES = {k: [] for k in S}   # html per scene


def add(k, html):
    SCENES[k].append(html)


# ------------------------------------------------------------------ animation helpers

def show(sel, t, kind="up", d=.4):
    HIDE.append(sel)
    if kind == "up":
        js(f'tl.fromTo("{sel}", {{opacity: 0, y: 46}}, {{opacity: 1, y: 0, duration: {d}, ease: "back.out(2.2)"}}, {t:.3f});')
    elif kind == "pop":
        js(f'tl.fromTo("{sel}", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.6)"}}, {t:.3f});')
    elif kind == "slam":
        js(f'tl.fromTo("{sel}", {{opacity: 0, scale: 1.7}}, {{opacity: 1, scale: 1, duration: .28, ease: "power4.out"}}, {t:.3f});')
        ev(t + .05, "slam")
    elif kind == "left":
        js(f'tl.fromTo("{sel}", {{opacity: 0, x: -120}}, {{opacity: 1, x: 0, duration: {d}, ease: "power3.out"}}, {t:.3f});')
    elif kind == "fade":
        js(f'tl.fromTo("{sel}", {{opacity: 0}}, {{opacity: 1, duration: {d}, ease: "power1.out"}}, {t:.3f});')


def hide(sel, t, d=.22):
    js(f'tl.to("{sel}", {{opacity: 0, scale: .85, duration: {d}, ease: "power2.in"}}, {t:.3f});')


def shake(sel, t, n=8, amp=16):
    for k in range(n):
        a = amp * (1 - k / n)
        js(f'tl.set("{sel}", {{x: {R.uniform(-a, a):.1f}, y: {R.uniform(-a, a):.1f}}}, {t + k / 30:.3f});')
    js(f'tl.set("{sel}", {{x: 0, y: 0}}, {t + n / 30:.3f});')


def blink(sel, t0, t1, per=.5):
    t, k = t0, 0
    while t < t1:
        js(f'tl.set("{sel}", {{opacity: {1 if k % 2 == 0 else .15}}}, {t:.3f});')
        t += per / 2
        k += 1


def head(k, chip=None, title=None, t=None, chip_cls="", title_cls="", tsize=None):
    if chip:
        add(k, f'<div class="chipwrap"><span class="chip {chip_cls}" id="{k}-chip">{chip}</span></div>')
        show(f"#{k}-chip", t, "pop")
    if title:
        st = f' style="font-size:{tsize}px"' if tsize else ""
        add(k, f'<div class="hdr {title_cls}" id="{k}-hdr"{st}>{title}</div>')
        show(f"#{k}-hdr", t + .08, "slam")


def ring(k, cx, cy, r, n=28):
    ticks = "".join(f'<i id="{k}-tk{i}" style="transform:rotate({i * 360 / n:.2f}deg) translateY(-{r}px)"></i>' for i in range(n))
    add(k, f'<div class="ring" id="{k}-ring" style="left:{cx}px;top:{cy}px">{ticks}</div>')
    js(f'tl.fromTo("#{k}-ring", {{rotation: 0}}, {{rotation: 40, duration: {S[k][1] - S[k][0]:.3f}, ease: "none"}}, {S[k][0]:.3f});')
    return n


# ------------------------------------------------------------------ scenes

def scene_A():
    k = "A"
    head(k, "GAME OVER", "CONTINUE?", 0.0, tsize=124)
    n = ring(k, 540, 820, 285)
    offs = [.25 + i * (w[9] - .4) / 16 for i in range(16)] + [w[9] + .06 + i * .06 for i in range(12)]
    for i, t in enumerate(offs[:n]):
        js(f'tl.set("#A-tk{i}", {{opacity: .14}}, {t:.3f});')
    for d, t in count:
        ev(t, "tick")
    add(k, '<div class="save" id="A-save"><img class="cv" src="assets/img/cover-god-of-war-2.png" alt="">'
           '<div class="st"><b>SAVE DATA</b><span>SLOT 1</span></div><img class="ps" src="assets/img/ps2-logo.png" alt="">'
           '<span class="warn" id="A-warn">EXPIRING</span></div>')
    show("#A-save", .25, "up")
    show("#A-warn", w[9], "pop", .3)
    shake("#A-save", w[9], 10, 10)
    js(f'tl.to("#A-save .cv", {{opacity: .35, duration: .6}}, {w[9]:.3f});')


def scene_B():
    k = "B"
    add(k, '<div class="chipwrap"><span class="chip" id="B-pause">PAUSED</span></div>')
    show("#B-pause", S[k][0] + .02, "pop", .25)
    add(k, f'<div class="hdr vio big" id="B-h1">PLAYER 2</div><div class="hdr sub" id="B-h2">HAS JOINED</div>')
    hide("#B-pause", w[14] - .15, .15)
    show("#B-h1", w[14], "slam")
    show("#B-h2", w[14] + .12, "up", .35)
    add(k, '<span class="tag" id="B-p1" style="left:300px">P1 · YOU</span>')
    show("#B-p1", S[k][0] + .3, "up", .35)
    add(k, '<span class="tag vio" id="B-p2" style="left:780px">P2</span>')
    show("#B-p2", w[14] + .1, "pop")
    add(k, '<span class="name" id="B-name" style="left:780px">CLAUDE</span>')
    hide("#B-p2", w[16] - .1, .1)
    show("#B-name", w[16], "slam")
    add(k, '<div class="burst" id="B-burst" style="left:780px;top:880px"></div>')
    HIDE.append("#B-burst")
    js(f'tl.set("#B-burst", {{opacity: .9, scale: .2}}, {w[14]:.3f});')
    js(f'tl.to("#B-burst", {{opacity: 0, scale: 2.4, duration: .7, ease: "power2.out"}}, {w[14] + .01:.3f});')
    ev(w[11], "whoosh")
    ev(w[14], "land")
    ev(w[16], "chime")


def scene_C1():
    k = "C1"
    head(k, "FOR CLAUDE CODE", None, S[k][0] + .05)
    ev(w[19], "whoosh")
    ev(w[20], "whoosh")
    ev(w[20] + .1, "slam")
    add(k, '<div class="chips" id="C1-chips"><span class="pill" id="C1-c0">11 SKILLS</span><span class="pill vio" id="C1-c1">FREE</span><span class="pill" id="C1-c2">OPEN SOURCE</span></div>')
    show("#C1-c0", w[21], "pop"); ev(w[21], "blip")
    show("#C1-c1", w[22], "pop"); ev(w[22], "blip")
    show("#C1-c2", w[23], "pop"); ev(w[23], "blip")
    add(k, '<div class="press" id="C1-press">PRESS START</div>')
    show("#C1-press", w[20] + .3, "fade", .2)
    blink("#C1-press", w[20] + .6, S[k][1], .6)


def scene_C2():
    k = "C2"
    add(k, '<div class="hdr" id="C2-hdr" style="font-size:96px">NOW LOADING</div>')
    show("#C2-hdr", S[k][0] + .05, "slam")
    add(k, '<div class="bar" id="C2-bar"><i id="C2-fill"></i></div>')
    show("#C2-bar", S[k][0] + .15, "up", .3)
    js(f'tl.fromTo("#C2-fill", {{scaleX: 0}}, {{scaleX: 1, duration: {w[33] - w[25]:.3f}, ease: "power1.inOut"}}, {w[25]:.3f});')
    add(k, '<div class="tip" id="C2-tip"><span class="pill vio sm">TIP</span><div class="tt"><b>NOT</b> AN EMULATOR</div>'
           '<div class="td">Claude rebuilds the game\'s code so it runs natively on PC.</div></div>')
    show("#C2-tip", w[34], "up")
    ev(w[34], "slam")
    for t in [w[25] + i * .35 for i in range(9)]:
        ev(t, "data")
    ev(w[32], "chime")


def scene_D():
    k = "D"
    head(k, "POWER-UPS", "INVENTORY", S[k][0] + .02)
    labels = ["GRAPHICS", "LEVELS", "CONTROLLER"]
    slots = "".join(f'<div class="slot" id="D-s{i}" style="left:{x - 105}px"><span>{lb}</span><b class="plus" id="D-p{i}">+1</b></div>'
                    for i, (x, lb) in enumerate(zip([250, 540, 830], labels)))
    add(k, slots)
    for i in range(3):
        show(f"#D-s{i}", S[k][0] + .2 + i * .08, "up", .35)
    add(k, '<div class="chat" id="D-chat"><div class="bub me" id="D-b0">make the graphics sharper</div><div class="bub ai" id="D-b1">on it!</div></div>')
    show("#D-b0", w[41], "pop", .35); ev(w[41], "msg")
    show("#D-b1", w[45], "pop", .35); ev(w[45], "msg")
    hide("#D-chat", w[46] - .12, .12)
    for i, a in enumerate([w[46], w[48], w[50]]):
        ev(a, "item")
        land = [w[48] - .05 + .3, w[50] - .05 + .3, S[k][1] - .55 + .3][i]
        js(f'tl.set("#D-s{i}", {{borderColor: "{VIO}"}}, {land:.3f});')
        show(f"#D-p{i}", land, "pop", .3)
        ev(land, "blip")
    add(k, '<div class="burst" id="D-burst" style="left:540px;top:760px"></div>')
    HIDE.append("#D-burst")
    for a in [w[37], w[46], w[48], w[50]]:
        js(f'tl.set("#D-burst", {{opacity: .85, scale: .3}}, {a:.3f});')
        js(f'tl.to("#D-burst", {{opacity: 0, scale: 2.2, duration: .6, ease: "power2.out"}}, {a + .01:.3f});')


def scene_E():
    k = "E"
    errs = "".join(f'<div class="err" id="E-e{i}" style="left:{x}px;top:{y}px"><div class="et">ERROR<i></i></div><div class="eb"><b>×</b>GAME CRASHED</div></div>'
                   for i, (x, y) in enumerate([(120, 600), (330, 760), (210, 920)]))
    add(k, f'<div id="E-errs">{errs}</div>')
    for i in range(3):
        show(f"#E-e{i}", w[54] + i * .1, "pop", .25)
        ev(w[54] + i * .1, "err")
    shake("#E-errs", w[54] + .3, 10, 18)
    js(f'tl.to("#E-errs", {{opacity: 0, scale: .6, duration: .2, ease: "power2.in"}}, {w[55] - .12:.3f});')
    add(k, '<div class="hdr" id="E-hdr" style="font-size:112px">BOSS FIGHT</div>')
    show("#E-hdr", w[55], "slam")
    ev(w[55], "roar")
    add(k, '<div class="hp" id="E-hp"><span>CRASH.EXE</span><div class="hb"><i id="E-hpf"></i></div></div>')
    show("#E-hp", w[55] + .15, "up", .3)
    lv = [.68, .42, .18, 0]
    for h, v in zip(hits, lv):
        js(f'tl.to("#E-hpf", {{scaleX: {v}, duration: .13, ease: "power2.out"}}, {h + .2:.3f});')
        ev(h, "shot")
        ev(h + .2, "hit")
    add(k, '<span class="move" id="E-move">P2 USES <b>TESTER SKILL</b></span>')
    show("#E-move", w[57], "left", .3)
    add(k, '<div class="ko" id="E-ko">K.O.!</div>')
    show("#E-ko", ko, "slam")
    ev(ko, "boom")
    shake("#E-ko", ko + .28, 6, 10)


def scene_F():
    k = "F"
    head(k, "WORLD 2", "NEW GAME +", w[63] + .05)
    ev(w[64], "chime")
    for t in unlock:
        ev(t, "unlock")


def scene_G():
    k = "G"
    head(k, "HEADS UP", None, S[k][0] + .05)
    ev(w[79], "stamp")


def scene_H():
    k = "H"
    add(k, '<div class="hdr" id="H-hdr" style="font-size:124px">CONTINUE?</div>')
    show("#H-hdr", S[k][0] + .02, "slam")
    n = ring(k, 540, 735, 240)
    for i in range(n):
        js(f'tl.set("#H-tk{i}", {{opacity: .14}}, {S[k][0]:.3f});')
        js(f'tl.set("#H-tk{i}", {{opacity: 1}}, {w[88] + i * .025:.3f});')
    for d, t in count2:
        ev(t, "tick")
    ev(w[88], "burst")
    add(k, '<div class="cta" id="H-cta"><div class="c1" id="H-c1">COMMENT</div><div class="c2" id="H-c2">“CONSOLE”</div></div>')
    show("#H-c1", w[87], "up", .35)
    show("#H-c2", w[88], "slam")
    js(f'tl.fromTo("#H-c2", {{scale: 1}}, {{scale: 1.08, duration: .16, yoyo: true, repeat: 1, ease: "power2.out"}}, {w[90]:.3f});')
    ev(w[90], "press")
    t, kk = w[90] + .6, 0
    while t < DUR - .2:
        js(f'tl.to("#H-c2", {{scale: {1.04 if kk % 2 == 0 else 1}, duration: .5, ease: "sine.inOut"}}, {t:.3f});')
        t += .5
        kk += 1


# ------------------------------------------------------------------ captions: a game dialogue box

CHUNKS = [(0, 4), (5, 9), (10, 14), (15, 16), (17, 20), (21, 23), (24, 29), (30, 33), (34, 36), (37, 40), (41, 45), (46, 47),
          (48, 49), (50, 52), (53, 54), (55, 56), (57, 62), (63, 66), (67, 72), (73, 76), (77, 80), (81, 86), (87, 90), (91, 96)]
HL = {2, 16, 19, 20, 21, 22, 26, 31, 32, 33, 34, 35, 36, 39, 40, 41, 46, 47, 48, 49, 51, 52, 55, 56, 58, 59, 64, 65, 66, 70, 71, 72, 75, 76, 79, 80, 88, 90}
SHOW = {"favorite": "favourite", '"console"': "“CONSOLE”"}


def captions():
    rows = []
    for ci, (a, b) in enumerate(CHUNKS):
        spans = []
        for i in range(a, b + 1):
            txt = SHOW.get(W[i]["w"], W[i]["w"])
            cls = ' class="hl"' if i in HL else ""
            spans.append(f'<span id="cw{i}"{cls}>{txt}</span>')
            HIDE.append(f"#cw{i}")
            js(f'tl.fromTo("#cw{i}", {{opacity: 0, y: 18}}, {{opacity: 1, y: 0, duration: .16, ease: "back.out(3)"}}, {w[i]:.3f});')
        rows.append(f'<div class="cl" id="cc{ci}">{" ".join(spans)}</div>')
        t0 = w[a] - .02
        t1 = w[CHUNKS[ci + 1][0]] - .03 if ci + 1 < len(CHUNKS) else DUR
        HIDE.append(f"#cc{ci}")
        js(f'tl.set("#cc{ci}", {{opacity: 1}}, {t0:.3f});')
        js(f'tl.set("#cc{ci}", {{opacity: 0}}, {t1:.3f});')
    # the dialogue box bobs its little arrow the whole time
    t, k = 0.0, 0
    while t < DUR:
        js(f'tl.to("#cap .nx", {{y: {8 if k % 2 == 0 else 0}, duration: .35, ease: "sine.inOut"}}, {t:.3f});')
        t += .35
        k += 1
    show("#cap .box", 0.0, "up", .35)
    return "".join(rows)


def transitions():
    for k, (a, b) in S.items():
        if a == 0:
            continue
        js(f'tl.fromTo("#wipe", {{x: -1900}}, {{x: 1900, duration: .42, ease: "power2.inOut"}}, {a - .21:.3f});')
        ev(a - .15, "swish")
    # freeze glitch on "Wait" and on the crash
    for t in [w[10], w[54]]:
        for f in range(3):
            js(f'tl.set("#glitch", {{opacity: 1, y: {R.randint(-30, 30)}}}, {t + f / 30:.3f});')
            for i in range(5):
                js(f'tl.set("#gb{i}", {{y: {R.randint(0, 1880)}, height: {R.choice([10, 22, 40, 70])}, x: {R.randint(-60, 60)}, '
                   f'backgroundColor: "{R.choice([VIO, INK, "#ff9ccf", "#8fb8ff"])}"}}, {t + f / 30:.3f});')
        js(f'tl.set("#glitch", {{opacity: 0}}, {t + .1:.3f});')
        ev(t, "glitch")
    for t, o, d in [(w[10], .85, .35), (ko, .9, .45), (w[88], .7, .4)]:
        js(f'tl.set("#flash", {{opacity: {o}}}, {t:.3f});')
        js(f'tl.to("#flash", {{opacity: 0, duration: {d}, ease: "power2.out"}}, {t + .01:.3f});')
    # scanlines drift all the time
    js(f'tl.fromTo("#scan", {{y: 0}}, {{y: 64, duration: {DUR}, ease: "none"}}, 0);')


CSS = f"""
@font-face {{ font-family: "Russo One"; src: url("assets/fonts/RussoOne.ttf"); }}
@font-face {{ font-family: "Chakra Petch"; font-weight: 600; src: url("assets/fonts/ChakraPetch-SemiBold.ttf"); }}
@font-face {{ font-family: "Chakra Petch"; font-weight: 700; src: url("assets/fonts/ChakraPetch-Bold.ttf"); }}
@font-face {{ font-family: "Rubik"; font-weight: 700; src: url("assets/fonts/Rubik-Bold.ttf"); }}
@font-face {{ font-family: "Rubik"; font-weight: 800; src: url("assets/fonts/Rubik-ExtraBold.ttf"); }}
@font-face {{ font-family: "Orbitron"; font-weight: 900; src: url("assets/fonts/Orbitron-Black.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #F1EEF4; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #F1EEF4; color: {INK}; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; display: block; }}
.scene {{ position: absolute; inset: 0; }}
.chipwrap {{ position: absolute; left: 0; right: 0; top: 296px; text-align: center; }}
.chip {{ display: inline-block; font: 700 30px/1 "Chakra Petch"; color: #fff; background: {INK}; padding: 12px 26px; border-radius: 999px; letter-spacing: 3px; }}
.hdr {{ position: absolute; left: 60px; right: 60px; top: 362px; text-align: center; font: 400 116px/1 "Russo One"; color: {INK};
  text-shadow: 0 7px 0 rgba(122,47,251,.16); white-space: nowrap; }}
.hdr.vio {{ color: {VIO}; text-shadow: 0 8px 0 rgba(29,26,38,.12); }}
.hdr.big {{ top: 330px; font-size: 150px; }}
.hdr.sub {{ top: 486px; font-size: 64px; letter-spacing: 6px; }}
.ring {{ position: absolute; width: 0; height: 0; }}
.ring i {{ position: absolute; left: -7px; top: -22px; width: 14px; height: 44px; border-radius: 8px; background: {VIO}; transform-origin: 7px 22px;
  box-shadow: 0 0 14px rgba(122,47,251,.45); }}
.save {{ position: absolute; left: 160px; width: 760px; top: 1148px; height: 104px; background: {PAPER}; border: 4px solid {INK}; border-radius: 26px;
  display: flex; align-items: center; gap: 22px; padding: 0 24px; box-shadow: 0 10px 0 rgba(29,26,38,.1); }}
.save .cv {{ width: 56px; height: 76px; object-fit: cover; border-radius: 6px; }}
.save .st {{ display: flex; flex-direction: column; gap: 4px; }}
.save .st b {{ font: 400 34px/1 "Russo One"; }}
.save .st span {{ font: 700 24px/1 "Chakra Petch"; color: #6a6480; letter-spacing: 2px; }}
.save .ps {{ height: 64px; margin-left: auto; }}
.save .warn {{ position: absolute; right: -18px; top: -24px; font: 700 24px/1 "Chakra Petch"; letter-spacing: 2px; color: #fff; background: {RED}; padding: 10px 16px; border-radius: 999px; }}
.tag {{ position: absolute; top: 1112px; transform: translateX(-50%); font: 700 32px/1 "Chakra Petch"; letter-spacing: 3px; padding: 14px 26px; border-radius: 999px;
  background: {PAPER}; border: 4px solid {INK}; white-space: nowrap; }}
.tag.vio {{ background: {VIO}; color: #fff; border-color: {VIO}; }}
.name {{ position: absolute; top: 1096px; transform: translateX(-50%); font: 400 60px/1 "Russo One"; color: #fff; background: {VIO}; padding: 18px 36px; border-radius: 999px;
  box-shadow: 0 10px 0 rgba(29,26,38,.15), 0 0 40px rgba(122,47,251,.5); }}
.burst {{ position: absolute; width: 420px; height: 420px; margin: -210px 0 0 -210px; border-radius: 50%; border: 10px solid {VIO}; }}
.chips {{ position: absolute; left: 0; right: 0; top: 1040px; display: flex; justify-content: center; gap: 18px; }}
.pill {{ font: 700 34px/1 "Chakra Petch"; letter-spacing: 3px; padding: 14px 26px; border-radius: 999px; background: {PAPER}; border: 4px solid {INK}; }}
.pill.vio {{ background: {VIO}; border-color: {VIO}; color: #fff; }}
.pill.sm {{ font-size: 26px; padding: 10px 18px; }}
.press {{ position: absolute; left: 0; right: 0; top: 1150px; text-align: center; font: 700 36px/1 "Chakra Petch"; letter-spacing: 10px; color: {VIO}; }}
.bar {{ position: absolute; left: 180px; width: 720px; top: 486px; height: 30px; border: 4px solid {INK}; border-radius: 999px; background: {PAPER}; overflow: hidden; }}
.bar i {{ position: absolute; inset: 3px; border-radius: 999px; background: linear-gradient(90deg, #8fb8ff, {VIO}); transform-origin: 0 50%; }}
.tip {{ position: absolute; left: 110px; right: 110px; top: 1060px; padding: 24px 34px; background: {PAPER}; border: 4px solid {INK}; border-radius: 28px;
  box-shadow: 0 10px 0 rgba(29,26,38,.1); text-align: center; }}
.tip .tt {{ margin-top: 12px; font: 400 52px/1 "Russo One"; }}
.tip .tt b {{ font-weight: 400; color: {VIO}; }}
.tip .td {{ margin-top: 10px; font: 700 30px/1.25 "Rubik"; color: #5d5770; }}
.slot {{ position: absolute; top: 990px; width: 210px; height: 180px; border-radius: 26px; background: transparent; border: 4px dashed #bdb5d6; }}
.slot span {{ position: absolute; left: 0; right: 0; bottom: 14px; text-align: center; font: 700 24px/1 "Chakra Petch"; letter-spacing: 2px; color: #4a4560; }}
.slot .plus {{ position: absolute; right: -14px; top: -22px; font: 400 30px/1 "Russo One"; color: #fff; background: {VIO}; padding: 8px 12px; border-radius: 999px; }}
.chat {{ position: absolute; left: 150px; right: 150px; top: 640px; display: flex; flex-direction: column; gap: 22px; }}
.bub {{ font: 800 42px/1.15 "Rubik"; padding: 22px 30px; border-radius: 30px; max-width: 86%; box-shadow: 0 8px 0 rgba(29,26,38,.1); }}
.bub.me {{ align-self: flex-end; background: {VIO}; color: #fff; border-bottom-right-radius: 8px; }}
.bub.ai {{ align-self: flex-start; background: {PAPER}; border: 4px solid {INK}; border-bottom-left-radius: 8px; }}
.err {{ position: absolute; width: 520px; background: {PAPER}; border: 4px solid {INK}; border-radius: 18px; overflow: hidden; box-shadow: 0 12px 0 rgba(29,26,38,.12); }}
.err .et {{ height: 54px; background: {VIO}; color: #fff; font: 700 28px/54px "Chakra Petch"; letter-spacing: 3px; padding-left: 20px; position: relative; }}
.err .et i {{ position: absolute; right: 14px; top: 13px; width: 28px; height: 28px; border-radius: 8px; background: #fff; }}
.err .eb {{ padding: 26px 22px; font: 400 40px/1 "Russo One"; display: flex; align-items: center; gap: 18px; }}
.err .eb b {{ width: 52px; height: 52px; border-radius: 50%; background: {RED}; color: #fff; font: 700 40px/50px "Rubik"; text-align: center; }}
.hp {{ position: absolute; left: 160px; width: 760px; top: 494px; }}
.hp span {{ font: 700 28px/1 "Chakra Petch"; letter-spacing: 3px; color: {RED}; }}
.hp .hb {{ margin-top: 10px; height: 34px; border: 4px solid {INK}; border-radius: 999px; background: {PAPER}; overflow: hidden; position: relative; }}
.hp .hb i {{ position: absolute; inset: 3px; border-radius: 999px; background: linear-gradient(90deg, {RED}, #ff7a92); transform-origin: 0 50%; }}
.move {{ position: absolute; left: 70px; top: 1150px; font: 700 32px/1 "Chakra Petch"; letter-spacing: 2px; padding: 16px 26px; border-radius: 999px; background: {PAPER}; border: 4px solid {VIO}; color: {VIO}; }}
.move b {{ color: {INK}; }}
.ko {{ position: absolute; left: 0; right: 0; top: 650px; text-align: center; font: 400 230px/1 "Russo One"; color: {VIO};
  text-shadow: 0 0 0 #fff, 8px 8px 0 {INK}; -webkit-text-stroke: 8px #fff; paint-order: stroke fill; }}
.unl {{ position: absolute; left: 0; right: 0; top: 1170px; text-align: center; font: 700 34px/1 "Chakra Petch"; letter-spacing: 4px; }}
.unl .nums {{ position: relative; display: inline-block; width: 30px; height: 34px; color: {VIO}; }}
.unl .nums b {{ position: absolute; left: 0; top: 0; }}
.cta {{ position: absolute; left: 0; right: 0; top: 1020px; text-align: center; }}
.cta .c1 {{ font: 400 64px/1 "Russo One"; letter-spacing: 4px; }}
.cta .c2 {{ display: inline-block; margin-top: 16px; font: 400 104px/1 "Russo One"; color: #fff; background: {VIO}; padding: 18px 44px 22px; border-radius: 36px;
  box-shadow: 0 12px 0 {INK}, 0 0 50px rgba(122,47,251,.45); }}
#cap {{ position: absolute; left: 0; right: 0; top: 0; height: 1920px; pointer-events: none; }}
#cap .box {{ position: absolute; left: 70px; right: 70px; top: 1290px; height: 170px; background: rgba(255,255,255,.94); border: 4px solid {INK};
  border-radius: 30px; box-shadow: 0 10px 0 rgba(29,26,38,.12); }}
#cap .cl {{ position: absolute; left: 36px; right: 36px; top: 0; height: 162px; display: flex; flex-wrap: wrap; align-content: center; justify-content: center;
  column-gap: 14px; row-gap: 4px; font: 800 50px/1.15 "Rubik"; text-align: center; }}
#cap .cl span {{ display: inline-block; }}
#cap .hl {{ color: {VIO}; }}
#cap .nx {{ position: absolute; right: 30px; bottom: 14px; width: 0; height: 0; border-left: 14px solid transparent; border-right: 14px solid transparent; border-top: 18px solid {VIO}; }}
#wipe {{ position: absolute; top: -200px; left: -400px; width: 1300px; height: 2400px; transform: skewX(-16deg); background: {VIO}; z-index: 40;
  box-shadow: -60px 0 0 #b9a2ff, 60px 0 0 {INK}; }}
#flash {{ position: absolute; inset: 0; background: #fff; z-index: 41; opacity: 0; }}
#glitch {{ position: absolute; inset: 0; z-index: 42; opacity: 0; }}
#glitch b {{ position: absolute; left: 0; width: 1080px; display: block; }}
#scan {{ position: absolute; left: 0; right: 0; top: -64px; height: 2048px; z-index: 30; opacity: .05;
  background: repeating-linear-gradient(180deg, {INK} 0 2px, transparent 2px 8px); }}
"""


def no_immediate():
    """A target tweened by several fromTo calls keeps the earliest one's from-values at rest: the later ones get
    immediateRender: false."""
    import re
    seen = {}
    for i, ln in enumerate(A):
        m = re.match(r'\s*tl\.fromTo\("([^"]+)".*, ([\d.]+)\);$', ln)
        if m:
            seen.setdefault(m.group(1), []).append((float(m.group(2)), i))
    for sel, lst in seen.items():
        if len(lst) > 1:
            for _, i in sorted(lst)[1:]:
                A[i] = A[i].replace("duration:", "immediateRender: false, duration:", 1)


def main():
    for f in [scene_A, scene_B, scene_C1, scene_C2, scene_D, scene_E, scene_F, scene_G, scene_H]:
        f()
    caps = captions()
    transitions()
    no_immediate()
    A.insert(0, "      gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ", {opacity: 0});")
    A.insert(1, '      gsap.set("#wipe", {x: -1900});')
    scenes = "\n      ".join(
        f'<div id="sc-{k}" class="clip scene" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{2 + i % 2}">{"".join(SCENES[k])}</div>'
        for i, (k, (a, b)) in enumerate(S.items()))
    has_mix = os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav"))
    src = "mix" if has_mix else "voice"
    gb = "".join(f"<b id=\"gb{i}\"></b>" for i in range(5))
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Console skill: Continue? 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      {scenes}
      <div id="cap" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6"><div class="box">{caps}<i class="nx"></i></div></div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8" data-layout-ignore><div id="scan"></div><div id="wipe"></div><div id="flash"></div><div id="glitch">{gb}</div></div>
      <audio id="mix" src="assets/audio/{src}.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.CS_T = {json.dumps(CT)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/world.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"dur": DUR, "S": S, "ev": sorted(EV)}, open(os.path.join(B, "cues.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(EV)} sound events, audio: {src}")
    print({k: v for k, v in S.items()})


if __name__ == "__main__":
    main()
