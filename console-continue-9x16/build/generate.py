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
DUR = 42.4
R = random.Random(5)
INK, VIO, PAPER, RED = "#1d1a26", "#7a2ffb", "#ffffff", "#e0335a"
CL = "#D97757"   # Claude's orange: everything that is Player 2 (Claude) wears it


def claude_mark(size, color="#fff"):
    """Claude's spark mark: rounded rays of uneven length around a centre."""
    rays = [1, .78, .95, .72, 1, .82, .9, .7, .98, .8, .88, .74]
    g = "".join(f'<rect x="-5.5" y="{-46 * r:.1f}" width="11" height="{46 * r - 8:.1f}" rx="5.5" transform="rotate({i * 30 + (7 if i % 2 else 0)})"/>'
                for i, r in enumerate(rays))
    return f'<svg class="cm" viewBox="-50 -50 100 100" width="{size}" height="{size}"><g fill="{color}">{g}<circle r="9"/></g></svg>'

A, HIDE, EV = [], [], []


PROPS = ["mag", "gear", "brush", "pad", "hat", "flag", "phones", "ball", "card", "globe", "bug"]   # one per skill, in README order


def crab(size, prop=None, cid=None):
    """Player 2's mascot: a little pixel crab in Claude's orange (as in the reference Reel), with an optional prop for
    its skill. Drawn on a 16-unit grid; the prop sits above or beside it."""
    o, d = CL, "#2a1d18"
    r = lambda x, y, w_, h, c: f'<rect x="{x}" y="{y}" width="{w_}" height="{h}" fill="{c}"/>'
    body = (r(2, 6, 12, 7, o) + r(0, 8, 2, 2, o) + r(14, 8, 2, 2, o) + r(5, 8, 1, 2, d) + r(10, 8, 1, 2, d)
            + "".join(r(x, 13, 1, 2, o) for x in (3, 5, 10, 12)))
    pr = {
        "mag": '<circle cx="15" cy="3" r="2.6" fill="#dff1ff" stroke="#2a1d18" stroke-width="1"/>' + r(12, 5, 1, 2, d),
        "gear": '<circle cx="8" cy="2.5" r="2.6" fill="#8fb8ff" stroke="#2a1d18" stroke-width=".8"/><circle cx="8" cy="2.5" r=".9" fill="#2a1d18"/>',
        "brush": r(7, 0, 2, 4, "#8b5a2b") + r(6, 3, 4, 2, "#ff6fae"),
        "pad": r(4, 9, 8, 3, "#2a1d18") + r(5, 10, 1, 1, "#8fb8ff") + r(10, 10, 1, 1, "#ff9ccf"),
        "hat": '<path d="M8 -4 L12 5 H4 Z" fill="#7a2ffb"/>' + r(3, 5, 10, 1, "#5a1fc4") + r(8, 0, 1, 1, "#ffd36e"),
        "flag": r(13, -1, 1, 7, d) + r(14, -1, 3, 2, "#ffd36e"),
        "phones": '<path d="M3 7 Q8 -1 13 7" fill="none" stroke="#2a1d18" stroke-width="1.4"/>' + r(1, 6, 3, 3, "#7a2ffb") + r(12, 6, 3, 3, "#7a2ffb"),
        "ball": '<circle cx="8" cy="2.5" r="2.4" fill="#ff6b6b"/>' + r(8, -1, 1, 1, "#3c9a4a"),
        "card": r(6, 0, 4, 5, "#26222f") + r(7, 1, 2, 1, "#ffd36e"),
        "globe": '<circle cx="8" cy="2.5" r="2.6" fill="#7fd1a0" stroke="#2a1d18" stroke-width=".8"/>' + r(6, 1, 2, 2, "#3c78d8"),
        "bug": r(13, 1, 3, 3, "#e0335a") + r(12, 2, 1, 1, d) + r(16, 2, 1, 1, d),
    }.get(prop, "")
    ids = f' id="{cid}"' if cid else ""
    return (f'<svg class="crab"{ids} viewBox="-1 -5 19 21" width="{size}" height="{size * 21 / 19:.0f}" shape-rendering="crispEdges">'
            f'{body}{pr}</svg>')


def js(s):
    A.append("      " + s)


def ev(t, kind):
    EV.append((round(t, 3), kind))


S = {}
order = [("A", 0), ("B", w[10] - .02), ("C1", w[17] - .04), ("C2", w[25] - .04), ("D", w[37] - .04), ("E", w[52] - .04),
         ("F", w[62] - .04), ("G", w[76] - .04), ("H", w[86] - .04)]
for i, (k, a) in enumerate(order):
    S[k] = [round(a, 3), round(order[i + 1][1] if i + 1 < len(order) else DUR, 3)]

A_IN = w[4] - .05   # "is about to time out": the gameplay shrinks into the paused screen and the countdown starts
count = [["9", A_IN], ["8", A_IN + .6], ["7", A_IN + 1.2], ["6", A_IN + 1.75], ["5", w[9]], ["4", w[9] + .16], ["3", w[9] + .32], ["2", w[9] + .48], ["1", w[9] + .64]]
count2 = [["3", S["H"][0]], ["2", w[87] - .2]]
hits = [w[57], w[59], w[60], w[61]]
ko = round(w[61] + .32, 3)
unlock = [w[69], w[70], w[71], w[75]]
CT = {"S": S, "w": w, "CL": "#D97757", "count": count, "count2": count2, "burst": w[87], "press": w[89], "hits": hits, "ko": ko, "unlock": unlock}

SCENES = {k: [] for k in S}   # html per scene
APANEL, WINDOW = [], []        # root-level gameplay panels (their videos may not sit inside a timed scene)


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


def hop(sel, t0, t1, h=16):
    """A little crab hop on every half second until t1."""
    t = t0
    while t < t1 - .3:
        js(f'tl.to("{sel}", {{y: -{h}, duration: .14, ease: "power2.out", immediateRender: false}}, {t:.3f});')
        js(f'tl.to("{sel}", {{y: 0, duration: .16, ease: "power2.in", immediateRender: false}}, {t + .14:.3f});')
        t += .5


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
    # 0 to A_IN: the real game, full screen. Then it shrinks into a paused screen under the countdown, and greys out
    # (a still frame) on "forever".
    APANEL.append(f'<div id="apanel"><video id="a-v" class="clip" src="assets/video/gow-game.mp4" data-start="0" '
                  f'data-duration="{S[k][1]:.3f}" data-media-start="0.3" data-track-index="4" muted playsinline></video>'
                  '<img id="a-freeze" src="assets/img/gow-freeze.jpg" alt=""><div id="a-dim"></div></div>')
    js('tl.set("#apanel", {opacity: 1, scale: 1.3, y: 60}, 0);')
    js(f'tl.to("#apanel", {{scale: 1.42, duration: {A_IN - .1:.3f}, ease: "sine.inOut"}}, 0);')
    js(f'tl.to("#apanel", {{scale: 1, y: 0, duration: .55, ease: "power3.inOut"}}, {A_IN - .1:.3f});')
    js(f'tl.fromTo("#a-dim", {{opacity: 0}}, {{opacity: .3, duration: .4}}, {A_IN:.3f});')
    HIDE.append("#a-freeze")
    js(f'tl.to("#a-freeze", {{opacity: 1, duration: .25}}, {w[9]:.3f});')
    js(f'tl.set("#apanel", {{opacity: 0}}, {S[k][1]:.3f});')
    ev(A_IN, "swish")
    head(k, "GAME OVER", "CONTINUE?", A_IN + .1, tsize=124)
    n = ring(k, 540, 820, 285)
    for i in range(n):
        HIDE.append(f"#A-tk{i}")
        js(f'tl.set("#A-tk{i}", {{opacity: 1}}, {A_IN + .1 + i * .012:.3f});')
    offs = [A_IN + .3 + i * (w[9] - A_IN - .4) / 16 for i in range(16)] + [w[9] + .06 + i * .05 for i in range(12)]
    for i, t in enumerate(offs[:n]):
        js(f'tl.set("#A-tk{i}", {{opacity: .14}}, {t:.3f});')
    for d, t in count:
        ev(t, "tick")
    add(k, '<div class="save" id="A-save"><img class="cv" src="assets/img/cover-god-of-war-2.png" alt="">'
           '<div class="st"><b>SAVE DATA</b><span>SLOT 1</span></div><img class="ps" src="assets/img/ps2-logo.png" alt="">'
           '<span class="warn" id="A-warn">EXPIRING</span></div>')
    show("#A-save", A_IN + .25, "up")
    show("#A-warn", w[9], "pop", .3)
    shake("#A-save", w[9], 10, 10)
    js(f'tl.to("#A-save .cv", {{opacity: .35, duration: .6}}, {w[9]:.3f});')


def scene_B():
    k = "B"
    add(k, '<div class="chipwrap"><span class="chip" id="B-pause">PAUSED</span></div>')
    show("#B-pause", S[k][0] + .02, "pop", .25)
    add(k, f'<div class="hdr cl big" id="B-h1">PLAYER 2</div><div class="hdr sub" id="B-h2">HAS JOINED</div>')
    hide("#B-pause", w[14] - .15, .15)
    show("#B-h1", w[14], "slam")
    show("#B-h2", w[14] + .12, "up", .35)
    add(k, '<span class="tag" id="B-p1" style="left:300px">P1 · YOU</span>')
    show("#B-p1", S[k][0] + .3, "up", .35)
    add(k, '<span class="tag cl" id="B-p2" style="left:780px">P2</span>')
    show("#B-p2", w[14] + .1, "pop")
    add(k, f'<span class="name" id="B-name" style="left:780px">{claude_mark(54)}CLAUDE</span>')
    hide("#B-p2", w[16] - .1, .1)
    show("#B-name", w[16], "slam")
    add(k, '<div class="burst cl" id="B-burst" style="left:780px;top:880px"></div>')
    HIDE.append("#B-burst")
    js(f'tl.set("#B-burst", {{opacity: .9, scale: .2}}, {w[14]:.3f});')
    js(f'tl.to("#B-burst", {{opacity: 0, scale: 2.4, duration: .7, ease: "power2.out"}}, {w[14] + .01:.3f});')
    add(k, f'<div class="crabw" id="B-crab" style="left:440px;top:930px">{crab(200, "pad")}</div>')
    HIDE.append("#B-crab")
    js(f'tl.set("#B-crab", {{opacity: 1, y: 260, scale: .4}}, {w[15]:.3f});')
    js(f'tl.to("#B-crab", {{y: 0, scale: 1, duration: .45, ease: "back.out(2.4)"}}, {w[15] + .01:.3f});')
    hop("#B-crab", w[15] + .5, S[k][1])
    ev(w[11], "whoosh")
    ev(w[14], "land")
    ev(w[15], "boing")
    ev(w[16], "chime")


def scene_C1():
    k = "C1"
    head(k, "FOR CLAUDE CODE", None, S[k][0] + .05)
    ev(w[19], "whoosh")
    ev(w[20], "whoosh")
    ev(w[20] + .1, "slam")
    add(k, '<div class="press" id="C1-press">PRESS START</div>')
    show("#C1-press", w[20] + .3, "fade", .2)
    blink("#C1-press", w[20] + .6, w[21] - .05, .6)
    js(f'tl.to("#C1-press", {{opacity: 0, duration: .1}}, {w[21] - .05:.3f});')
    # "Eleven free skills": eleven crabs pop into a grid, one per skill
    rows = [(6, 1030), (5, 1170)]
    i = 0
    cells = []
    for n, y in rows:
        for j in range(n):
            x = 540 + (j - (n - 1) / 2) * 162
            cells.append(f'<div class="crabw" id="C1-k{i}" style="left:{x - 80:.0f}px;top:{y - 90}px">{crab(160, PROPS[i])}</div>')
            t = w[21] + i * .055
            HIDE.append(f"#C1-k{i}")
            js(f'tl.fromTo("#C1-k{i}", {{opacity: 0, y: 40, scale: .3}}, {{opacity: 1, y: 0, scale: 1, duration: .3, ease: "back.out(3)"}}, {t:.3f});')
            hop(f"#C1-k{i}", t + .4 + (i % 3) * .1, S[k][1], 10)
            if i % 2 == 0:
                ev(t, "blip")
            i += 1
    add(k, "".join(cells))
    add(k, '<div class="stamp2" id="C1-free"><span>FREE</span></div>')
    show("#C1-free", w[22], "slam")


def scene_C2():
    k = "C2"
    add(k, '<div class="hdr" id="C2-hdr" style="font-size:96px">NOW LOADING</div>')
    show("#C2-hdr", S[k][0] + .05, "slam")
    add(k, '<div class="bar" id="C2-bar"><i id="C2-fill"></i></div>')
    show("#C2-bar", S[k][0] + .15, "up", .3)
    js(f'tl.fromTo("#C2-fill", {{scaleX: 0}}, {{scaleX: 1, duration: {w[33] - w[25]:.3f}, ease: "power1.inOut"}}, {w[25]:.3f});')
    # the GAME.EXE window: compiling first, then real RE4 gameplay running in it
    t0 = w[25] - .1
    WINDOW.append(f'<div id="win"><div class="wt">GAME.EXE<span>NATIVE PC BUILD</span><i></i></div><div class="wb">'
                  f'<video id="win-v" class="clip" src="assets/video/re4-game.mp4" data-start="{t0:.3f}" data-duration="{S[k][1] - t0:.3f}" '
                  f'data-media-start="0.6" data-track-index="5" muted playsinline></video>'
                  '<div id="win-comp"><b>REBUILDING</b><span>PS2 code &gt; PC code</span><div class="dots"><i></i><i></i><i></i></div></div></div></div>')
    HIDE.append("#win")
    js(f'tl.fromTo("#win", {{opacity: 0, scale: .6, y: 60}}, {{opacity: 1, scale: 1, y: 0, duration: .45, ease: "back.out(1.8)"}}, {t0:.3f});')
    js(f'tl.to("#win-comp", {{opacity: 0, duration: .3}}, {w[32]:.3f});')
    js(f'tl.set("#win", {{opacity: 0}}, {S[k][1]:.3f});')
    for i in range(3):
        js(f'tl.fromTo("#win-comp .dots i:nth-child({i + 1})", {{y: 0}}, {{y: -16, duration: .25, yoyo: true, repeat: {int((w[32] - t0) / .5)}, ease: "sine.inOut"}}, {t0 + i * .12:.3f});')
    add(k, '<div class="sticker" id="C2-st"><div class="sk"><b>NOT</b> AN EMULATOR</div></div>')
    show("#C2-st", w[34], "slam")
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
    show("#D-b0", w[40], "pop", .35); ev(w[40], "msg")
    show("#D-b1", w[44], "pop", .35); ev(w[44], "msg")
    hide("#D-chat", w[45] - .12, .12)
    for i, a in enumerate([w[45], w[47], w[49]]):
        ev(a, "item")
        land = [w[47] - .05 + .3, w[49] - .05 + .3, S[k][1] - .55 + .3][i]
        js(f'tl.set("#D-s{i}", {{borderColor: "{VIO}"}}, {land:.3f});')
        show(f"#D-p{i}", land, "pop", .3)
        ev(land, "blip")
    # show, don't tell: a card per power-up
    pad_svg = ('<svg viewBox="0 0 120 70" width="190" height="111"><path d="M30 8h60c16 0 26 12 28 30l2 14c1 10-9 16-17 9l-11-10H28L17 61c-8 7-18 1-17-9l2-14C4 20 14 8 30 8z" '
               'fill="{c}" stroke="#1d1a26" stroke-width="4"/><circle cx="38" cy="30" r="7" fill="#1d1a26"/><circle cx="84" cy="26" r="4" fill="#1d1a26"/>'
               '<circle cx="92" cy="34" r="4" fill="#1d1a26"/></svg>')
    pads = "".join(f'<div class="pd" id="D-pd{i}">{pad_svg.format(c=c)}<b class="ok" id="D-ok{i}">&#10003;</b></div>'
                   for i, c in enumerate(["#ffffff", "#2d2a36", CL]))
    add(k, '<div class="demo" id="D-c0"><img src="assets/img/gow-16.0.jpg" alt=""><img class="blur" id="D-blur" src="assets/img/gow-16.0.jpg" alt="">'
           '<i class="sweep" id="D-sweep"></i><span class="dtag" id="D-t0">BEFORE</span><span class="dtag on" id="D-t1">AFTER</span></div>'
           '<div class="demo lv" id="D-c1"><div class="dh">SELECT LEVEL</div><div class="tiles">'
           + "".join(f'<div class="tile" id="D-tl{i}"><img src="assets/img/gow-{t}.jpg" alt=""><span>{lb}</span></div>'
                     for i, (t, lb) in enumerate([("2.0", "LEVEL 1"), ("13.2", "LEVEL 2"), ("19.4", "NEW")]))
           + '</div><i class="sel" id="D-sel"></i></div>'
           f'<div class="demo pads" id="D-c2"><div class="dh">ANY CONTROLLER</div><div class="pdrow">{pads}</div></div>')
    a0, a1, a2 = w[45], w[47], w[49]
    for i, (a, b) in enumerate([(a0, a1), (a1, a2), (a2, S[k][1] + .1)]):
        HIDE.append(f"#D-c{i}")
        js(f'tl.fromTo("#D-c{i}", {{opacity: 0, scale: .7, rotation: {(-4, 3, -2)[i]}}}, {{opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(2)"}}, {a - .02:.3f});')
        if b < S[k][1]:
            js(f'tl.to("#D-c{i}", {{opacity: 0, x: -160, duration: .14, ease: "power2.in"}}, {b - .12:.3f});')
    HIDE.extend(["#D-t1"])
    js(f'tl.fromTo("#D-sweep", {{x: -60}}, {{x: 880, duration: .45, ease: "power2.inOut"}}, {w[46] + .05:.3f});')
    js(f'tl.to("#D-blur", {{opacity: 0, duration: .4, ease: "power2.inOut"}}, {w[46] + .05:.3f});')
    js(f'tl.to("#D-t0", {{opacity: 0, duration: .1}}, {w[46] + .3:.3f});')
    js(f'tl.fromTo("#D-t1", {{opacity: 0, scale: 1.6}}, {{opacity: 1, scale: 1, duration: .25, ease: "back.out(3)"}}, {w[46] + .3:.3f});')
    for i, t in enumerate([a1 + .05, a1 + .3, a1 + .55]):
        js(f'tl.to("#D-sel", {{x: {i * 252}, duration: .14, ease: "power2.out", immediateRender: false}}, {t:.3f});')
        ev(t, "blip")
    js(f'tl.fromTo("#D-tl2", {{scale: 1}}, {{scale: 1.08, duration: .15, yoyo: true, repeat: 1}}, {a1 + .55:.3f});')
    for i in range(3):
        show(f"#D-ok{i}", a2 + .25 + i * .15, "pop", .25)
        ev(a2 + .25 + i * .15, "blip")
        js(f'tl.fromTo("#D-pd{i}", {{rotation: 0}}, {{rotation: {(-6, 6, -6)[i]}, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut"}}, {a2 + .2 + i * .1:.3f});')
    add(k, '<div class="burst" id="D-burst" style="left:540px;top:760px"></div>')
    HIDE.append("#D-burst")
    for a in [w[37], w[45], w[47], w[49]]:
        js(f'tl.set("#D-burst", {{opacity: .85, scale: .3}}, {a:.3f});')
        js(f'tl.to("#D-burst", {{opacity: 0, scale: 2.2, duration: .6, ease: "power2.out"}}, {a + .01:.3f});')


def scene_E():
    k = "E"
    errs = "".join(f'<div class="err" id="E-e{i}" style="left:{x}px;top:{y}px"><div class="et">ERROR<i></i></div><div class="eb"><b>×</b>GAME CRASHED</div></div>'
                   for i, (x, y) in enumerate([(120, 600), (330, 760), (210, 920)]))
    add(k, f'<div id="E-errs">{errs}</div>')
    for i in range(3):
        show(f"#E-e{i}", w[53] + i * .1, "pop", .25)
        ev(w[53] + i * .1, "err")
    shake("#E-errs", w[53] + .3, 10, 18)
    js(f'tl.to("#E-errs", {{opacity: 0, scale: .6, duration: .2, ease: "power2.in"}}, {w[54] - .12:.3f});')
    add(k, '<div class="hdr" id="E-hdr" style="font-size:112px">BOSS FIGHT</div>')
    show("#E-hdr", w[54], "slam")
    ev(w[54], "roar")
    add(k, '<div class="hp" id="E-hp"><span>CRASH.EXE</span><div class="hb"><i id="E-hpf"></i></div></div>')
    show("#E-hp", w[54] + .15, "up", .3)
    lv = [.68, .42, .18, 0]
    for h, v in zip(hits, lv):
        js(f'tl.to("#E-hpf", {{scaleX: {v}, duration: .13, ease: "power2.out"}}, {h + .2:.3f});')
        ev(h, "shot")
        ev(h + .2, "hit")
    add(k, f'<span class="move" id="E-move">{claude_mark(34, CL)}CLAUDE USES <b>TESTER SKILL</b></span>')
    show("#E-move", w[56], "left", .3)
    add(k, f'<div class="crabw" id="E-crab" style="left:760px;top:930px">{crab(230, "mag")}</div>')
    show("#E-crab", w[56], "pop", .35)
    hop("#E-crab", w[56] + .4, S[k][1], 14)
    add(k, '<div class="ko" id="E-ko">K.O.!</div>')
    show("#E-ko", ko, "slam")
    ev(ko, "boom")
    shake("#E-ko", ko + .28, 6, 10)


def scene_F():
    k = "F"
    head(k, "WORLD 2", "NEW GAME +", w[62] + .05)
    ev(w[63], "chime")
    for t in unlock:
        ev(t, "unlock")


def scene_G():
    k = "G"
    head(k, "HEADS UP", None, S[k][0] + .05)
    ev(w[78], "stamp")


def scene_H():
    k = "H"
    add(k, '<div class="hdr" id="H-hdr" style="font-size:124px">CONTINUE?</div>')
    show("#H-hdr", S[k][0] + .02, "slam")
    n = ring(k, 540, 735, 240)
    for i in range(n):
        js(f'tl.set("#H-tk{i}", {{opacity: .14}}, {S[k][0]:.3f});')
        js(f'tl.set("#H-tk{i}", {{opacity: 1}}, {w[87] + i * .025:.3f});')
    for d, t in count2:
        ev(t, "tick")
    ev(w[87], "burst")
    letters = "".join(f'<b id="H-L{i}">{c}</b>' for i, c in enumerate("CONSOLE"))
    add(k, '<div class="cbox" id="H-cbox"><div class="cav">' + claude_mark(40) + '</div><div class="cin"><span class="cl1">Comment</span>'
           f'<span class="ctx">{letters}<i class="caret" id="H-caret"></i></span></div><div class="csend" id="H-send">&#10148;</div></div>')
    show("#H-cbox", w[86], "up", .35)
    for i in range(7):
        HIDE.append(f"#H-L{i}")
        js(f'tl.fromTo("#H-L{i}", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: .1}}, {w[87] + i * .07:.3f});')
        ev(w[87] + i * .07, "key")
    blink("#H-caret", w[86], DUR, .5)
    js(f'tl.fromTo("#H-send", {{scale: 1}}, {{scale: 1.3, duration: .14, yoyo: true, repeat: 1, ease: "power2.out"}}, {w[89]:.3f});')
    ev(w[89], "press")
    add(k, f'<div class="crabw" id="H-crab" style="left:810px;top:850px">{crab(190, "pad")}</div>')
    show("#H-crab", w[87] + .2, "pop", .35)
    hop("#H-crab", w[87] + .6, DUR, 22)


# ------------------------------------------------------------------ captions: a game dialogue box

CHUNKS = [(0, 3), (4, 6), (7, 9), (10, 10), (11, 14), (15, 16), (17, 18), (19, 20), (21, 23), (24, 27), (28, 30), (31, 33), (34, 36),
          (37, 39), (40, 41), (42, 44), (45, 46), (47, 48), (49, 51), (52, 53), (54, 55), (56, 58), (59, 61), (62, 65), (66, 69), (70, 71),
          (72, 75), (76, 79), (80, 82), (83, 85), (86, 89), (90, 95)]
HL = {2, 16, 19, 20, 21, 22, 26, 31, 32, 33, 34, 35, 36, 39, 40, 45, 46, 47, 48, 50, 51, 54, 55, 57, 58, 63, 64, 65, 69, 70, 71, 74, 75, 78, 79, 87, 89}
SHOW = {"favorite": "favourite", "console": "“CONSOLE”", "powerups.": "power-ups!", "11": "Eleven", "link": "link!"}


def captions():
    """Short caption labels like the reference: 1-4 words on a dark pill, a new one about every second, keywords in
    Claude orange, each popping in on its first word."""
    rows = []
    for ci, (a, b) in enumerate(CHUNKS):
        spans = " ".join(f'<span{" class=" + chr(34) + "hl" + chr(34) if i in HL else ""}>{SHOW.get(W[i]["w"], W[i]["w"])}</span>' for i in range(a, b + 1))
        rows.append(f'<div class="cl" id="cc{ci}"><div class="pill2">{spans}</div></div>')
        t0 = w[a] - .03
        t1 = w[CHUNKS[ci + 1][0]] - .04 if ci + 1 < len(CHUNKS) else DUR
        HIDE.append(f"#cc{ci}")
        js(f'tl.set("#cc{ci}", {{opacity: 1, scale: .55, y: 26}}, {t0:.3f});')
        js(f'tl.to("#cc{ci}", {{scale: 1, y: 0, duration: .2, ease: "back.out(3.2)"}}, {t0 + .01:.3f});')
        js(f'tl.set("#cc{ci}", {{opacity: 0}}, {t1:.3f});')
    return "".join(rows)


def transitions():
    for k, (a, b) in S.items():
        if a == 0:
            continue
        js(f'tl.fromTo("#wipe", {{x: -1900}}, {{x: 1900, duration: .32, ease: "power2.inOut"}}, {a - .16:.3f});')
        ev(a - .15, "swish")
    # freeze glitch on "Wait" and on the crash
    for t in [w[10], w[53]]:
        for f in range(3):
            js(f'tl.set("#glitch", {{opacity: 1, y: {R.randint(-30, 30)}}}, {t + f / 30:.3f});')
            for i in range(5):
                js(f'tl.set("#gb{i}", {{y: {R.randint(0, 1880)}, height: {R.choice([10, 22, 40, 70])}, x: {R.randint(-60, 60)}, '
                   f'backgroundColor: "{R.choice([VIO, INK, "#ff9ccf", "#8fb8ff"])}"}}, {t + f / 30:.3f});')
        js(f'tl.set("#glitch", {{opacity: 0}}, {t + .1:.3f});')
        ev(t, "glitch")
    for t, o, d in [(w[10], .85, .35), (ko, .55, .3), (w[87], .6, .35)]:
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
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; display: block; z-index: 4; }}
.scene {{ position: absolute; inset: 0; z-index: 5; }}
.sw, .pw {{ position: absolute; inset: 0; transform-origin: 540px 880px; }}
#deco {{ position: absolute; inset: 0; z-index: 5; pointer-events: none; }}
#deco .d {{ position: absolute; display: block; }}
#rays {{ position: absolute; left: 0; top: 0; width: 1400px; height: 1400px; margin: -700px 0 0 -700px; z-index: 2; opacity: 0; pointer-events: none; }}
#bg {{ position: absolute; inset: 0; z-index: 0; overflow: hidden; }}
#bg video {{ position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; object-fit: cover; filter: blur(8px) saturate(1.25); }}
#wash {{ position: absolute; inset: 0; z-index: 1; background: linear-gradient(180deg, #F7F6F3 0%, #F1EEF4 55%, #E8E4F1 100%); overflow: hidden; }}
#wash .blob {{ position: absolute; width: 900px; height: 900px; border-radius: 50%; display: block; }}
#blob0 {{ left: -260px; top: 80px; background: radial-gradient(circle, rgba(170,140,255,.42) 0, rgba(170,140,255,0) 65%); }}
#blob1 {{ left: 420px; top: 560px; background: radial-gradient(circle, rgba(120,190,255,.34) 0, rgba(120,190,255,0) 65%); }}
#blob2 {{ left: 60px; top: 1180px; background: radial-gradient(circle, rgba(255,170,215,.32) 0, rgba(255,170,215,0) 65%); }}
#resume {{ position: absolute; inset: 0; z-index: 2; overflow: hidden; }}
#resume video {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
#apanel {{ position: absolute; left: 120px; top: 505px; width: 840px; height: 630px; z-index: 3; border: 8px solid #fff; border-radius: 32px; overflow: hidden;
  box-shadow: 0 24px 60px rgba(29,26,38,.25); background: #000; }}
#apanel video, #a-freeze {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#a-dim {{ position: absolute; inset: 0; background: {INK}; opacity: 0; }}
#win {{ position: absolute; left: 160px; top: 770px; width: 760px; z-index: 3; background: #fff; border: 5px solid {INK}; border-radius: 26px; overflow: hidden;
  box-shadow: 0 16px 0 rgba(29,26,38,.12), 0 30px 60px rgba(29,26,38,.2); }}
#win .wt {{ height: 50px; background: {VIO}; color: #fff; font: 700 28px/50px "Chakra Petch"; letter-spacing: 3px; padding-left: 20px; position: relative; }}
#win .wt span {{ margin-left: 16px; font-size: 20px; opacity: .8; }}
#win .wt i {{ position: absolute; right: 14px; top: 13px; width: 24px; height: 24px; border-radius: 7px; background: #fff; }}
#win .wb {{ position: relative; height: 428px; background: #0d0b14; }}
#win video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#win-comp {{ position: absolute; inset: 0; background: #16131f; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; color: #fff; }}
#win-comp b {{ font: 400 56px/1 "Russo One"; }}
#win-comp span {{ font: 700 28px/1 "Chakra Petch"; letter-spacing: 3px; color: #b9a2ff; }}
#win-comp .dots {{ display: flex; gap: 14px; margin-top: 10px; }}
#win-comp .dots i {{ width: 18px; height: 18px; border-radius: 50%; background: {VIO}; display: block; }}
.sticker {{ position: absolute; right: 70px; top: 712px; }}
.sticker {{ font: 400 40px/1 "Russo One"; }}
.sticker .sk {{ transform: rotate(-6deg); background: #ffd36e; border: 4px solid {INK}; border-radius: 16px; padding: 14px 24px; box-shadow: 0 8px 0 rgba(29,26,38,.15); }}
.sticker b {{ font-weight: 400; color: {VIO}; }}
.chipwrap {{ position: absolute; left: 0; right: 0; top: 296px; text-align: center; }}
.chip {{ display: inline-block; font: 700 30px/1 "Chakra Petch"; color: #fff; background: {INK}; padding: 12px 26px; border-radius: 999px; letter-spacing: 3px; }}
.hdr {{ position: absolute; left: 60px; right: 60px; top: 362px; text-align: center; font: 400 116px/1 "Russo One"; color: {INK};
  text-shadow: 0 7px 0 rgba(122,47,251,.16), 0 0 30px rgba(255,255,255,.85); white-space: nowrap; }}
.hdr.vio {{ color: {VIO}; text-shadow: 0 8px 0 rgba(29,26,38,.12); }}
.hdr.cl {{ color: {CL}; text-shadow: 0 8px 0 rgba(29,26,38,.14), 0 0 34px rgba(255,255,255,.9); }}
.tag.cl {{ background: {CL}; color: #fff; border-color: {CL}; }}
.burst.cl {{ border-color: {CL}; }}
.cm {{ display: inline-block; vertical-align: middle; }}
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
.name {{ position: absolute; top: 1090px; transform: translateX(-50%); font: 400 60px/1 "Russo One"; color: #fff; background: {CL}; padding: 14px 34px 14px 22px; border-radius: 999px;
  box-shadow: 0 10px 0 rgba(29,26,38,.15), 0 0 40px rgba(217,119,87,.55); display: flex; align-items: center; gap: 14px; white-space: nowrap; }}
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
.move {{ position: absolute; left: 70px; top: 1150px; font: 700 32px/1 "Chakra Petch"; letter-spacing: 2px; padding: 12px 26px 12px 16px; border-radius: 999px; background: {PAPER}; border: 4px solid {CL}; color: {CL};
  display: flex; align-items: center; gap: 12px; }}
.move b {{ color: {INK}; }}
.ko {{ position: absolute; left: 0; right: 0; top: 650px; text-align: center; font: 400 230px/1 "Russo One"; color: {VIO};
  text-shadow: 0 0 0 #fff, 8px 8px 0 {INK}; -webkit-text-stroke: 8px #fff; paint-order: stroke fill; }}
.unl {{ position: absolute; left: 0; right: 0; top: 1170px; text-align: center; font: 700 34px/1 "Chakra Petch"; letter-spacing: 4px; }}
.unl .nums {{ position: relative; display: inline-block; width: 30px; height: 34px; color: {VIO}; }}
.unl .nums b {{ position: absolute; left: 0; top: 0; }}
.cta {{ position: absolute; left: 0; right: 0; top: 1010px; display: flex; flex-direction: column; align-items: center; gap: 14px; }}
.cta .c1 {{ display: inline-block; font: 400 60px/1 "Russo One"; letter-spacing: 4px; background: #fff; padding: 12px 30px; border-radius: 999px; border: 4px solid {INK}; }}
.cta .c2 {{ display: inline-block; font: 400 104px/1 "Russo One"; color: #fff; background: {VIO}; padding: 18px 44px 22px; border-radius: 36px;
  box-shadow: 0 12px 0 {INK}, 0 0 50px rgba(122,47,251,.45); }}
#cap {{ position: absolute; left: 0; right: 0; top: 0; height: 1920px; pointer-events: none; z-index: 6; }}
#cap .cl {{ position: absolute; left: 60px; right: 60px; top: 1300px; display: flex; justify-content: center; transform-origin: 50% 50%; }}
#cap .pill2 {{ display: inline-block; max-width: 960px; text-align: center; font: 700 54px/1.15 "Chakra Petch"; text-transform: uppercase; letter-spacing: 1px;
  color: #fff; background: {INK}; padding: 18px 34px 20px; border-radius: 22px; box-shadow: 0 10px 0 rgba(29,26,38,.18), 0 18px 40px rgba(29,26,38,.25); }}
#cap .hl {{ color: #ffa27f; }}
.crabw {{ position: absolute; z-index: 6; }}
.crab {{ display: block; filter: drop-shadow(0 8px 0 rgba(29,26,38,.18)); }}
.stamp2 {{ position: absolute; left: 720px; top: 540px; z-index: 7; }}
.stamp2 span {{ display: inline-block; transform: rotate(-10deg); font: 400 76px/1 "Russo One"; color: #fff; background: {CL}; padding: 12px 30px 16px; border-radius: 18px;
  border: 5px solid #fff; box-shadow: 0 10px 0 rgba(29,26,38,.2); }}
.demo {{ position: absolute; left: 130px; width: 820px; top: 540px; height: 420px; background: #fff; border: 5px solid {INK}; border-radius: 28px; overflow: hidden;
  box-shadow: 0 14px 0 rgba(29,26,38,.12), 0 30px 60px rgba(29,26,38,.2); }}
.demo > img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.demo .blur {{ filter: blur(9px) saturate(.6) brightness(.9); }}
.demo .sweep {{ position: absolute; left: 0; top: 0; width: 10px; height: 100%; background: #fff; box-shadow: 0 0 30px 10px rgba(255,255,255,.8); display: block; }}
.demo .dtag {{ position: absolute; left: 22px; top: 22px; font: 700 30px/1 "Chakra Petch"; letter-spacing: 3px; color: #fff; background: {INK}; padding: 10px 18px; border-radius: 999px; }}
.demo .dtag.on {{ background: {CL}; }}
.demo .dh {{ height: 70px; background: {INK}; color: #fff; font: 400 40px/70px "Russo One"; text-align: center; letter-spacing: 2px; }}
.demo .tiles {{ position: absolute; left: 30px; top: 100px; display: flex; gap: 22px; }}
.demo .tile {{ width: 230px; height: 290px; border-radius: 18px; overflow: hidden; position: relative; border: 4px solid {INK}; }}
.demo .tile img {{ width: 100%; height: 100%; object-fit: cover; }}
.demo .tile span {{ position: absolute; left: 10px; bottom: 10px; font: 700 26px/1 "Chakra Petch"; color: #fff; background: rgba(29,26,38,.85); padding: 8px 12px; border-radius: 10px; }}
.demo .tile:last-child span {{ background: {CL}; }}
.demo .sel {{ position: absolute; left: 22px; top: 92px; width: 246px; height: 306px; border: 8px solid {CL}; border-radius: 22px; display: block; box-shadow: 0 0 30px rgba(217,119,87,.6); }}
.demo .pdrow {{ position: absolute; left: 0; right: 0; top: 130px; display: flex; justify-content: center; gap: 40px; }}
.demo .pd {{ position: relative; }}
.demo .ok {{ position: absolute; right: -6px; top: -26px; width: 56px; height: 56px; border-radius: 50%; background: {CL}; color: #fff; font: 700 34px/56px "Rubik"; text-align: center; }}
.cbox {{ position: absolute; left: 110px; width: 860px; top: 1030px; height: 150px; background: #fff; border: 5px solid {INK}; border-radius: 30px; display: flex; align-items: center; gap: 22px;
  padding: 0 24px; box-shadow: 0 14px 0 rgba(29,26,38,.14), 0 30px 60px rgba(29,26,38,.22); }}
.cbox .cav {{ width: 92px; height: 92px; border-radius: 50%; background: {CL}; display: flex; align-items: center; justify-content: center; flex: none; }}
.cbox .cin {{ flex: 1; display: flex; flex-direction: column; gap: 6px; }}
.cbox .cl1 {{ font: 700 26px/1 "Chakra Petch"; letter-spacing: 2px; color: #6a6480; text-transform: uppercase; }}
.cbox .ctx {{ display: flex; align-items: center; height: 70px; font: 400 64px/1 "Russo One"; color: {INK}; border: 4px solid {CL}; border-radius: 16px; padding: 0 16px; }}
.cbox .ctx b {{ font-weight: 400; display: inline-block; }}
.cbox .caret {{ width: 6px; height: 50px; background: {CL}; margin-left: 6px; display: block; }}
.cbox .csend {{ width: 92px; height: 92px; border-radius: 50%; background: {CL}; color: #fff; font: 700 48px/92px "Rubik"; text-align: center; flex: none; }}
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


def beats():
    """The music's kick grid in video time (120 BPM, kicks on every half second), skipped while the music is muffled
    (before Player 2 joins) and through its breakdown (after "Steam Deck" until "console")."""
    music_in = 96.35 - w[87]
    t0 = 88.35 - music_in
    out, k = [], -200
    while True:
        t = t0 + k * .5
        k += 1
        if t < 0:
            continue
        if t >= DUR - .3:
            break
        if t < w[11] or (92.2 - music_in <= t < w[87] - .05):
            continue
        out.append((round(t, 3), abs(((t - t0) / 2) - round((t - t0) / 2)) < .01))
    return out


def motion():
    """Movement on top of every scene: each scene zooms in as it arrives and pulses on the music's beat (harder on the
    bar), big moments shake, ray bursts flare behind the peaks, headers float, and shapes drift in the margins."""
    for k, (a, b) in S.items():
        if a > 0:
            js(f'tl.fromTo("#sw-{k}", {{scale: 1.12}}, {{scale: 1, duration: .45, ease: "power3.out"}}, {a:.3f});')
    for t, bar in beats():
        k = next(k for k, (a, b) in S.items() if a <= t < b)
        js(f'tl.to("#pw-{k}", {{scale: {1.032 if bar else 1.014}, duration: .05, ease: "power2.out"}}, {t:.3f});')
        js(f'tl.to("#pw-{k}", {{scale: 1, duration: .3, ease: "power2.out"}}, {t + .05:.3f});')
    for k, t, amp in [("B", w[14], 18), ("C1", w[20], 12), ("E", w[54], 20), ("E", ko, 28), ("F", w[75], 16), ("H", w[87], 18)]:
        shake(f"#pw-{k}", t, 9, amp)
    for hid, k in [("A-hdr", "A"), ("B-h1", "B"), ("C2-hdr", "C2"), ("D-hdr", "D"), ("E-hdr", "E"), ("F-hdr", "F"), ("H-hdr", "H")]:
        a, b = S[k]
        n = max(1, int((b - a - .6) / 1.1))
        js(f'tl.to("#{hid}", {{y: -10, rotation: -1.2, duration: 1.1, yoyo: true, repeat: {n}, ease: "sine.inOut", immediateRender: false}}, {a + .6:.3f});')
    LV, LC = "#b9a2ff", "#f0a07e"
    rays_at = [(w[14], 780, 880, LC), (w[20], 540, 840, LV), (w[45], 540, 760, LV), (w[47], 540, 760, LC),
               (w[49], 540, 760, LV), (ko, 540, 820, LC), (w[75], 700, 760, LV), (w[87], 540, 735, LC)]
    for t, x, y, c in rays_at:
        js(f'tl.set("#rays", {{left: {x}, top: {y}, opacity: .3, scale: .25, rotation: 0}}, {t:.3f});')
        js(f'tl.set("#rays path", {{fill: "{c}"}}, {t:.3f});')
        js(f'tl.to("#rays", {{scale: 1.5, rotation: 35, opacity: 0, duration: .55, ease: "power2.out"}}, {t + .01:.3f});')
    wedges = "".join(f'<path d="M0 0 L{700 * __import__("math").cos(a):.1f} {700 * __import__("math").sin(a):.1f} '
                     f'L{700 * __import__("math").cos(a + .09):.1f} {700 * __import__("math").sin(a + .09):.1f} Z"/>'
                     for a in [i * 2 * 3.14159 / 24 for i in range(24)])
    shapes = [("ring", 64, 1180, 54, VIO), ("plus", 1004, 610, 44, CL), ("tri", 48, 650, 46, "#8fb8ff"), ("sq", 1010, 1200, 36, "#ff9ccf"),
              ("ring", 1000, 300, 40, "#8fb8ff"), ("plus", 70, 300, 36, VIO), ("tri", 990, 940, 40, VIO), ("sq", 60, 930, 30, CL)]
    svg = {"ring": '<circle cx="50" cy="50" r="36" fill="none" stroke="{c}" stroke-width="12"/>',
           "plus": '<path d="M38 8h24v30h30v24H62v30H38V62H8V38h30z" fill="{c}"/>',
           "tri": '<path d="M50 8 L92 86 H8 Z" fill="none" stroke="{c}" stroke-width="11" stroke-linejoin="round"/>',
           "sq": '<rect x="14" y="14" width="72" height="72" rx="14" fill="{c}"/>'}
    out = []
    for i, (kind, x, y, sz, c) in enumerate(shapes):
        out.append(f'<svg class="d" id="dc{i}" viewBox="0 0 100 100" width="{sz}" height="{sz}" style="left:{x - sz // 2}px;top:{y - sz // 2}px">{svg[kind].format(c=c)}</svg>')
        js(f'tl.fromTo("#dc{i}", {{rotation: 0}}, {{rotation: {360 * (2 if i % 2 else -2)}, duration: {DUR}, ease: "none"}}, 0);')
        js(f'tl.fromTo("#dc{i}", {{y: 0}}, {{y: {-26 if i % 2 else 26}, duration: {1.4 + .2 * i:.2f}, yoyo: true, repeat: {int(DUR / (1.4 + .2 * i))}, ease: "sine.inOut"}}, 0);')
    return (f'<div id="deco">{"".join(out)}</div>'
            f'<svg id="rays" viewBox="-700 -700 1400 1400"><g>{wedges}</g></svg>')


def background():
    """The real PS2 gameplay, full-bleed and softly blurred, under a lavender-white wash: the game keeps moving behind
    every scene. The wash thins on the world map and pulls back on "console", when the game resumes behind the CTA."""
    # God of War (its tutorial banner sits in 6.3-11.7 s of the clip, so those seconds are never used) and Resident Evil 4
    segs = [("gow-game.mp4", 0, S["B"][0], .3), ("gow-game.mp4", S["B"][0], S["C2"][0], 11.9), ("gow-game.mp4", S["C2"][0], S["D"][0], 16.4),
            ("re4-game.mp4", S["D"][0], S["E"][0], 11.0), ("re4-game.mp4", S["E"][0], S["F"][0], 1.0), ("gow-game.mp4", S["F"][0], S["G"][0], .5),
            ("re4-game.mp4", S["G"][0], S["H"][0], 5.5), ("gow-game.mp4", S["H"][0], DUR, 12.4)]
    vids = "".join(f'<video id="bg{i}" class="clip" src="assets/video/{src}" data-start="{a:.3f}" data-duration="{b - a:.3f}" '
                   f'data-media-start="{m}" data-track-index="0" muted playsinline></video>' for i, (src, a, b, m) in enumerate(segs))
    js(f'tl.fromTo("#bg", {{scale: 1.04, x: -30}}, {{scale: 1.16, x: 30, duration: 4, yoyo: true, repeat: {int(DUR / 4)}, ease: "sine.inOut"}}, 0);')
    for i, (x, y) in enumerate([(160, 60), (-140, 90), (120, -80)]):
        js(f'tl.fromTo("#blob{i}", {{x: 0, y: 0}}, {{x: {x}, y: {y}, duration: {DUR / 3:.2f}, yoyo: true, repeat: 2, ease: "sine.inOut"}}, 0);')
    js('tl.set("#wash", {opacity: 0}, 0);')
    js(f'tl.to("#wash", {{opacity: .8, duration: .5}}, {A_IN - .1:.3f});')
    js(f'tl.to("#wash", {{opacity: .62, duration: .5}}, {S["F"][0]:.3f});')
    js(f'tl.to("#wash", {{opacity: .8, duration: .4}}, {S["G"][0]:.3f});')
    js(f'tl.to("#wash", {{opacity: .4, duration: .6}}, {w[87]:.3f});')
    a = S["H"][0]
    resume = (f'<div id="resume"><video id="res-v" class="clip" src="assets/video/gow-game.mp4" data-start="{a:.3f}" data-duration="{DUR - a:.3f}" '
              f'data-media-start="12.4" data-track-index="3" muted playsinline></video></div>')
    HIDE.append("#resume")
    js(f'tl.to("#resume", {{opacity: .55, duration: .6}}, {w[87]:.3f});')
    blobs = "".join(f'<i class="blob" id="blob{i}"></i>' for i in range(3))
    return f'<div id="bg">{vids}</div><div id="wash">{blobs}</div>{resume}'


def main():
    for f in [scene_A, scene_B, scene_C1, scene_C2, scene_D, scene_E, scene_F, scene_G, scene_H]:
        f()
    caps = captions()
    bg = background()
    transitions()
    deco = motion()
    no_immediate()
    A.insert(0, "      gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ", {opacity: 0});")
    A.insert(1, '      gsap.set("#wipe", {x: -1900});')
    scenes = "\n      ".join(
        f'<div id="sc-{k}" class="clip scene" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{2 + i % 2}">'
        f'<div class="sw" id="sw-{k}"><div class="pw" id="pw-{k}">{"".join(SCENES[k])}</div></div></div>'
        for i, (k, (a, b)) in enumerate(S.items()))
    CT["beats"] = [t for t, _ in beats()]
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
      {bg}
      {"".join(APANEL)}{"".join(WINDOW)}
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1"></canvas>
      {scenes}
      <div id="cap" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6">{caps}</div>
      {deco}
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
