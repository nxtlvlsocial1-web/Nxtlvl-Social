"""For Certain (PARTYNEXTDOOR) v2: storybook-collage lyric edit, 3:4 (1080x1440). Writes index.html.

v2 (owner: "the song timestamp didn't match the lyrics ... everything is so static"):
- Starts where the singing starts. The vocals begin at 20.18 s of the song file (centre-minus-side vocal analysis),
  so the edit plays the song from OFF = 19.70 s. Every word below is timed in SONG seconds from the detected
  syllable onsets; T() turns them into edit time.
- "And I want you" x5 are the five repeats at 60.2, 65.4, 70.5, 75.7 and 80.9 s (the same phrase, spectral match
  0.93-0.95), sung over the breakdown. The edit ends on the fifth, then the logo.
- The reference's grammar (reference/ref_edit.mp4, studied frame by frame):
  * words land one by one exactly when sung: small white caps stack, one big red keyword; letters fly in from
    blur, the keyword's tracking collapses as it lands, and the old line goes soft when the next arrives
  * the camera never stops: every shot pushes, drifts and turns; text drifts faster than the world (parallax)
  * every line is a new shot: portal dives through round things, torn-paper holes, motion-blur whips, light-leak
    burns, zoom-throughs
  * objects act the line out and keep moving: a spinning record, a ringing phone, a beating heart, bags that
    drop and bounce, a stamp, a lens that magnifies
  * particles (petals, embers, dust, sparkles), grain, vignette and warm light leaks over everything
- The five "And I want you" shots become polaroid memories that drop onto a pile; the camera pulls back over the
  pile and the logo burns in while the song fades.

python3 build/generate.py
"""
import json
import math
import os
import random

from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1440, 30
OFF = 19.70                     # song time of edit 0
LOGO = 83.75                    # song time the logo burns in
SONG_OUT = 85.70                # song time the edit ends (song fades 83.0 -> 85.7)
DUR = round(SONG_OUT - OFF, 2)
BOX = json.load(open(os.path.join(ROOT, "plan", "bboxes.json")))
G = "assets/img/gen/"
A, HIDE, CUES, LEAKS, GPARTS = [], [], [], [], []
NID = [0]
R = random.Random(11)
BG_S = 1080 / 1024
F_ANTON = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/Anton.ttf"), 100)
F_INTER = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/inter-latin-800-normal.woff2"), 100)
F_PLAY = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/PlayfairDisplay-700Italic.ttf"), 100)


def isw(n):
    return n[0] == "w" and n[1:].isdigit()


def T(x):
    return round(x - OFF, 3)


def js(s):
    import re
    m = re.search(r"\}, (-[\d.]+)\);$", s)
    if m and float(m.group(1)) < 0:
        raise SystemExit(f"negative timeline position: {s[:120]}")
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def bgpt(x, y):
    return x * BG_S, y * BG_S - 90


def cue(t, kind):
    CUES.append((T(t), kind))


# ------------------------------------------------------------------------------------------------ scenes (song time)
# (name, start, end, background, transition into the next, point for portal / tear / zoom)
SC = [
    ("party", OFF, 23.30, "b1_party", "tear", (560, 560)),
    ("moon", 23.30, 25.62, "b2_moon", "portal", bgpt(571, 657)),
    ("vinyl", 25.62, 28.72, "b5_dancefloor", "whipl", None),
    ("phone", 28.72, 30.72, "b6_rain", "portal", (540, 700)),
    ("eye", 30.72, 32.78, "f1_eye", "portal", bgpt(524, 746)),
    ("desire", 32.78, 34.74, "b3_swirl", "flash", None),
    ("heart", 34.74, 37.08, "b9_wall", "whipup", None),
    ("body", 37.08, 41.15, "b7_stage", "drop", None),
    ("ring", 41.15, 44.72, "b8_bar", "tear", (540, 640)),
    ("globe", 44.72, 47.48, "b4_sunset", "portal", bgpt(505, 723)),
    ("badman", 47.48, 50.08, "b9_wall", "whipr", None),
    ("birkin", 50.08, 51.86, "b5_dancefloor", "zoom", (540, 760)),
    ("certain", 51.86, 55.22, "b2_moon", "whipl", None),
    ("search", 55.22, 58.88, "b1_party", "portal", None),       # the lens point is set by the search scene
    ("woah", 58.88, 60.06, "b3_swirl", "flash", None),
    ("w1", 60.06, 65.25, "c5_couple_slowdance", "slap", None),
    ("w2", 65.25, 70.40, "c6_couple_laugh", "slap", None),
    ("w3", 70.40, 75.55, "c7_couple_walk", "slap", None),
    ("w4", 75.55, 80.70, "b8_bar", "slap", None),
    ("w5", 80.70, LOGO, "b4_sunset", "logo", None),
]
SC = [list(s) for s in SC]
IDX = {s[0]: k for k, s in enumerate(SC)}
EL = {s[0]: [] for s in SC}
ELT = {s[0]: [] for s in SC}          # text: inside the camera but outside the push, so it drifts on its own
WS = [s[0] for s in SC if isw(s[0])]
# camera drift per scene: (push, dx, dy, rot0, rot1)
CAM = {"party": (.16, -40, -20, -1, .8), "moon": (.18, 30, 30, 1, -1), "vinyl": (.14, -30, 0, 0, 1.5),
       "phone": (.16, 20, -30, -1.5, 1), "eye": (.10, 0, 0, 0, 2), "desire": (.2, 0, 0, -2, 2),
       "heart": (.16, 0, -30, 1, -1), "body": (.2, 40, -20, -1, 1.5), "ring": (.16, -20, -40, 1, -1),
       "globe": (.18, 0, 30, -1, 1), "badman": (.16, -40, 0, -1, 1), "birkin": (.14, 30, 0, 1, -1),
       "certain": (.18, 0, -30, -1.5, 1.5), "search": (.12, -30, 0, 0, 0), "woah": (.25, 0, 0, -4, 4)}


def put(scene, html):
    EL[scene].append(html)


def k_of(scene):
    return IDX[scene]


# ------------------------------------------------------------------------------------------------ building blocks
def obj(scene, name, cx, cy, h, t0, z=4, rot=0, enter="rise", d=.6, extra="", idle=(16, 2.5, 1.4), cls="obj"):
    """A cut-out centred (visible box) on (cx, cy), h px tall. t0 in song time. Returns (id, left, top, scale)."""
    x0, y0, x1, y1 = BOX[name]
    s = h / (y1 - y0)
    w = 1024 * s
    left = cx - ((x0 + x1) / 2) * s
    top = cy - ((y0 + y1) / 2) * s
    i = nid("o")
    put(scene, f'<div class="{cls}" id="{i}" style="left:{left:.0f}px;top:{top:.0f}px;width:{w:.0f}px;height:{1536 * s:.0f}px;'
               f'z-index:{z}"><div class="ob"><img src="{G}{name}.png?u={i}" alt="">{extra}</div></div>')
    HIDE.append(f"#{i}")
    t = T(t0)
    if enter == "rise":
        js(f'tl.fromTo("#{i}", {{opacity: 0, y: 220, scale: .8, rotation: {rot - 8}, filter: "blur(20px)"}}, {{opacity: 1, y: 0, scale: 1, rotation: {rot}, '
           f'filter: "blur(0px)", duration: {d}, ease: "expo.out", immediateRender: false}}, {t});')
    elif enter == "pop":
        js(f'tl.fromTo("#{i}", {{opacity: 0, scale: .15, rotation: {rot - 30}}}, {{opacity: 1, scale: 1, rotation: {rot}, '
           f'duration: {d}, ease: "back.out(1.8)", immediateRender: false}}, {t});')
    elif enter == "drop":
        js(f'tl.fromTo("#{i}", {{opacity: 1, y: -1500, rotation: {rot - 25}}}, {{opacity: 1, y: 0, rotation: {rot}, duration: {d}, ease: "bounce.out", '
           f'immediateRender: false}}, {t});')
    elif enter in ("left", "right"):
        sx = -900 if enter == "left" else 900
        js(f'tl.fromTo("#{i}", {{opacity: 0, x: {sx}, filter: "blur(24px)"}}, {{opacity: 1, x: 0, filter: "blur(0px)", duration: {d}, '
           f'ease: "expo.out", immediateRender: false}}, {t});')
    elif enter == "none":
        js(f'tl.set("#{i}", {{opacity: 1}}, {t});')
    if idle:
        amp, r, per = idle
        reps = int((SC[k_of(scene)][2] - t0 + 1) / per) + 1
        js(f'tl.fromTo("#{i} > .ob", {{y: {amp / 2}, rotation: {-r / 2}}}, {{y: {-amp / 2}, rotation: {r / 2}, duration: {per}, ease: "sine.inOut", '
           f'yoyo: true, repeat: {reps}, immediateRender: false}}, {t});')
    return i, left, top, s


def measure(word, kind):
    f = {"big": F_ANTON, "bigw": F_ANTON, "sm": F_INTER, "scr": F_PLAY, "scrw": F_PLAY}[kind]
    w = f.getlength(word) / 100
    if kind == "sm":
        w += .06 * len(word)
    return w


def lyr(scene, rows, x=70, y=150, width=940, align="left", dim=None, out=None, z=9, drift=(-40, 1.07), maxbig=240, maxsm=64):
    """Word-synced lyric block. rows: [(kind, [(word, song_t), ...]), ...], kinds: sm (white caps), big (red keyword),
    bigw (white keyword), scr (red script), scrw (white script). dim / out in song time."""
    x = max(x, 80)
    width = min(width, FW - 80 - x)
    y = max(y, 120)
    i = nid("t")
    html = []
    first = min(t for _, ws in rows for _, t in ws)
    last = max(t for _, ws in rows for _, t in ws)
    for kind, ws in rows:
        line = " ".join(w for w, _ in ws)
        em = measure(line, kind) + .05
        size = min(maxsm if kind == "sm" else maxbig, width * .93 / em)        # room for the drift's scale
        spans = []
        for wi, (w, t) in enumerate(ws):
            wid = f"{i}w{len(html)}_{wi}"
            letters = "".join(f'<span class="l">{c}</span>' for c in w)
            spans.append(f'<span class="w" id="{wid}">{letters}</span>')
            nl = len(w)
            dl = [round(R.uniform(0, .09 if kind in ("big", "bigw") else .07), 3) for _ in range(nl)]
            tt = T(t)
            if kind in ("big", "bigw"):
                ys = [R.choice([-1, 1]) * R.randint(30, 80) for _ in range(nl)]
                xs_ = [round((c - (nl - 1) / 2) * 40) for c in range(nl)]
                js(f'tl.fromTo("#{wid}", {{opacity: 0, scale: 1.7, filter: "blur(16px)"}}, {{opacity: 1, scale: 1, '
                   f'filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {tt - .04:.3f});')
                js(f'tl.fromTo("#{wid} .l", {{x: (k) => {xs_}[k], y: (k) => {ys}[k], opacity: 0}}, {{x: 0, y: 0, opacity: 1, duration: .34, ease: "expo.out", '
                   f'stagger: (k) => {dl}[k], immediateRender: false}}, {tt - .04:.3f});')
            elif kind in ("scr", "scrw"):
                js(f'tl.fromTo("#{wid}", {{opacity: 0, scale: .55, rotation: -8, filter: "blur(12px)"}}, {{opacity: 1, scale: 1, rotation: 0, '
                   f'filter: "blur(0px)", duration: .4, ease: "back.out(1.6)", immediateRender: false}}, {tt - .03:.3f});')
            else:
                js(f'tl.fromTo("#{wid} .l", {{opacity: 0, y: 20, scale: 1.5, filter: "blur(8px)"}}, {{opacity: 1, y: 0, scale: 1, filter: "blur(0px)", '
                   f'duration: .24, ease: "power3.out", stagger: (k) => {dl}[k], immediateRender: false}}, {tt - .03:.3f});')
        html.append(f'<div class="{kind}" style="font-size:{size:.0f}px">{" ".join(spans)}</div>')
    xs = f"left:{x}px;width:{width}px;"
    ELT[scene].append( f'<div class="lyr" id="{i}" style="top:{y}px;{xs}text-align:{align};z-index:{z}"><div class="ld">{"".join(html)}</div></div>')
    HIDE.append(f"#{i}")
    js(f'tl.set("#{i}", {{opacity: 1}}, {T(first) - .06:.3f});')
    end = out if out else SC[k_of(scene)][2] + .5
    js(f'tl.fromTo("#{i} > .ld", {{y: 0, scale: 1}}, {{y: {drift[0]}, scale: {drift[1]}, duration: {end - first + .3:.2f}, ease: "none", '
       f'immediateRender: false}}, {T(first):.3f});')
    if dim:
        js(f'tl.to("#{i}", {{opacity: .5, scale: .92, filter: "blur(5px)", duration: .2, ease: "power2.out"}}, {T(dim):.3f});')
    if out:
        js(f'tl.to("#{i}", {{opacity: 0, scale: 1.45, filter: "blur(16px)", duration: .3, ease: "power2.in"}}, {T(out) - .3:.3f});')
    return i


def glow_sprite(color):
    """A radial glow baked to a PNG (assets/img/fx), so the page carries no CSS gradients."""
    import re
    from PIL import Image
    r_, g_, b_, a_ = [float(v) for v in re.findall(r"[\d.]+", color)]
    name = f"assets/img/fx/glow_{int(r_)}_{int(g_)}_{int(b_)}_{int(a_ * 100)}.png"
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        n = 128
        im = Image.new("RGBA", (n, n))
        px = im.load()
        for yy in range(n):
            for xx in range(n):
                d = math.hypot(xx + .5 - n / 2, yy + .5 - n / 2) / (n / 2) / .68
                px[xx, yy] = (int(r_), int(g_), int(b_), int(255 * a_ * max(0, 1 - d) ** 1.3))
        im.save(path)
    return name


LEAK_SPRITE = {"255,120,40": "leak_amber", "255,190,120": "leak_gold", "255,90,140": "leak_pink", "255,100,40": "leak_red",
               "255,150,80": "leak_peach", "255,80,20": "leak_red", "255,140,60": "leak_amber", "255,170,90": "leak_gold",
               "255,140,70": "leak_peach"}


def punch(scene, t, amt=.05):
    k = k_of(scene)
    js(f'tl.fromTo("#m{k}", {{scale: 1}}, {{keyframes: [{{scale: {1 + amt}, duration: .06, ease: "power2.out"}}, {{scale: 1, duration: .4, '
       f'ease: "power2.out"}}], immediateRender: false}}, {T(t):.3f});')


def glow(scene, x, y, r, color, t0, t1=None, op=.8, z=3, pulse=None):
    i = nid("gl")
    put(scene, f'<i class="glow" id="{i}" style="left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r}px;height:{2 * r}px;z-index:{z};'
               f'background-image:url({glow_sprite(color)})"></i>')
    HIDE.append(f"#{i}")
    js(f'tl.fromTo("#{i}", {{opacity: 0, scale: .4}}, {{opacity: {op}, scale: 1, duration: .45, ease: "power2.out", immediateRender: false}}, {T(t0):.3f});')
    if pulse:
        js(f'tl.to("#{i}", {{scale: 1.18, opacity: {op * .7:.2f}, duration: {pulse}, ease: "sine.inOut", yoyo: true, repeat: 5}}, {T(t0) + .45:.3f});')
    return i


def parts(scene, kind, n, z=7, t0=None, t1=None, area=(0, 0, FW, FH)):
    """Particles that drift through the whole shot: petal / ember / dust / spark / shard."""
    if scene is not None:
        k = k_of(scene)
        a, b = SC[k][1], SC[k][2]
    t0 = max(OFF, t0 if t0 is not None else a - .7)          # never before 0: a negative position shifts the whole timeline
    t1 = t1 if t1 is not None else b + .6
    dur = t1 - t0
    ax, ay, aw, ah = area
    html = []
    for j in range(n):
        pid = nid("pt")
        x0, y0 = ax + R.uniform(0, aw), ay + R.uniform(0, ah)
        if kind == "petal":
            sz = R.uniform(22, 46)
            sty = f"width:{sz:.0f}px;height:{sz * .7:.0f}px"
            dx, dy, rot = R.uniform(-160, 160), R.uniform(260, 520) * dur / 2.5, R.uniform(-540, 540)
            y0 -= dy * .5
        elif kind == "ember":
            sz = R.uniform(18, 40)
            sty = f"width:{sz:.0f}px;height:{sz:.0f}px"
            dx, dy, rot = R.uniform(-90, 90), -R.uniform(300, 700) * dur / 2.5, 0
            y0 += -dy * .5
        elif kind == "shard":
            sz = R.uniform(26, 70)
            sty = f"width:{sz:.0f}px;height:{sz * R.uniform(.6, 1.3):.0f}px"
            dx, dy, rot = R.uniform(-260, 260), R.uniform(-200, 300), R.uniform(-400, 400)
        elif kind == "spark":
            sz = R.uniform(20, 46)
            sty = f"width:{sz:.0f}px;height:{sz:.0f}px"
            dx, dy, rot = R.uniform(-40, 40), R.uniform(-60, 20), R.uniform(-90, 90)
        else:                                  # dust / bokeh
            sz = R.uniform(10, 46)
            sty = f"width:{sz:.0f}px;height:{sz:.0f}px;opacity:{R.uniform(.25, .7):.2f}"
            dx, dy, rot = R.uniform(-120, 120), R.uniform(-120, 60), 0
        html.append(f'<i class="pt {kind}" id="{pid}" style="left:{x0:.0f}px;top:{y0:.0f}px;{sty}"></i>')
        js(f'tl.fromTo("#{pid}", {{x: 0, y: 0, rotation: 0}}, {{x: {dx:.0f}, y: {dy:.0f}, rotation: {rot:.0f}, duration: {dur:.2f}, ease: "none", '
           f'immediateRender: false}}, {T(t0):.3f});')
        if kind == "spark":
            js(f'tl.fromTo("#{pid}", {{scale: 0}}, {{scale: 1, duration: .35, ease: "sine.inOut", yoyo: true, repeat: {int(dur / .7)}, '
               f'immediateRender: false}}, {T(t0) + R.uniform(0, .7):.3f});')
    gid = nid("pg")
    if scene is None:
        GPARTS.append(f'<div class="ptg" id="{gid}" style="z-index:{z}">{"".join(html)}</div>')
    else:
        put(scene, f'<div class="ptg" id="{gid}" style="z-index:{z}">{"".join(html)}</div>')
    return gid


def leak(t, x=0, color="rgba(255,120,40,.9)", op=.8, d=.7):
    """A warm light leak that sweeps across the frame (screen blend), song time."""
    LEAKS.append((T(t), x, color, op, d))


def flick(t, op=.85, d=.32):
    js(f'tl.fromTo("#flash", {{opacity: 0}}, {{opacity: {op}, duration: .05, immediateRender: false}}, {T(t) - .05:.3f});')
    js(f'tl.to("#flash", {{opacity: 0, duration: {d}, ease: "power2.out"}}, {T(t):.3f});')


# ------------------------------------------------------------------------------------------------ the shots
def shots():
    # 1. We didn't vibe on the first night: the party, she turns away; he arrives on the drop
    js('tl.fromTo("#c0", {scale: 1.35, filter: "blur(22px) brightness(.2)"}, {scale: 1, filter: "blur(0px) brightness(1)", duration: .9, '
       'ease: "expo.out", immediateRender: false}, 0);')
    leak(OFF + .05, -200, op=.9, d=1.0)
    obj("party", "c3_her_turn", 790, 1010, 860, 19.95, z=5, enter="right", d=.8, idle=(10, 1.5, 1.6))
    obj("party", "c1_him_profile", 250, 1080, 760, 20.66, z=6, enter="left", d=.7, idle=(8, 1, 1.8))
    punch("party", 20.66, .06)
    flick(20.66, .5, .35)
    cue(20.66, "hit")
    parts("party", "dust", 22, z=8)
    lyr("party", [("sm", [("WE", 20.18), ("DIDN'T", 20.39), ("VIBE", 20.70), ("ON", 21.08), ("THE", 21.20)]),
                  ("big", [("FIRST", 21.44), ("NIGHT", 21.77)])], x=70, y=120, width=760)
    punch("party", 21.77, .04)

    # 2. But you're so enticin': the perfume turns in the moonlight and sprays on ENTICIN'
    i, l, t, s = obj("moon", "o1_perfume", 560, 1030, 600, 23.32, z=5, enter="pop", d=.55, idle=(20, 4, 1.2))
    js(f'tl.fromTo("#{i} > .ob img", {{rotationY: -35, transformPerspective: 900}}, {{rotationY: 35, duration: 1.1, ease: "sine.inOut", '
       f'yoyo: true, repeat: 2, immediateRender: false}}, {T(23.32)});')
    mist = "".join(f'<i class="mist" style="left:{470 + R.uniform(-30, 30):.0f}px;top:{740 + R.uniform(-20, 20):.0f}px"></i>' for _ in range(18))
    put("moon", f'<div class="mistw" id="mist">{mist}</div>')
    HIDE.append("#mist")
    js(f'tl.set("#mist", {{opacity: 1}}, {T(24.45)});')
    js(f'tl.fromTo("#mist .mist", {{opacity: .95, x: 0, y: 0, scale: .3}}, {{opacity: 0, x: (k) => -300 + (k % 7) * 95, y: (k) => -360 + (k % 5) * 60, '
       f'scale: 3, duration: 1.2, ease: "power2.out", stagger: .02, immediateRender: false}}, {T(24.45)});')
    cue(24.45, "spray")
    parts("moon", "spark", 10, z=6, area=(200, 300, 700, 800))
    lyr("moon", [("sm", [("BUT", 23.52), ("YOU'RE", 23.77), ("SO", 24.13)]), ("big", [("ENTICIN'", 24.45)])], x=90, y=130, width=900)
    punch("moon", 24.45)

    # 3. We didn't vibe then: a record spins on the floor (3D), scratches dead on THEN, then rewinds
    i, *_ = obj("vinyl", "o2_vinyl", 540, 980, 820, 25.64, z=5, enter="rise", d=.5, idle=None)
    js(f'tl.set("#{i} > .ob", {{rotationX: 58, transformPerspective: 1100}}, 0);')
    js(f'tl.fromTo("#{i} > .ob img", {{rotation: 0}}, {{rotation: 520, duration: 1.2, ease: "none", immediateRender: false}}, {T(25.64)});')
    js(f'tl.to("#{i} > .ob img", {{rotation: 470, duration: .16, ease: "power2.out"}}, {T(26.84)});')
    js(f'tl.to("#{i} > .ob img", {{rotation: 478, duration: .5, ease: "power3.out"}}, {T(27.0)});')
    js(f'tl.to("#{i} > .ob img", {{rotation: -260, duration: 1.2, ease: "power2.in"}}, {T(27.5)});')       # the rewind into the whip
    cue(26.84, "scratch")
    obj("vinyl", "c4_her_dance", 830, 560, 560, 25.9, z=4, enter="right", d=.7, idle=(14, 4, .65))
    parts("vinyl", "dust", 14, z=6)
    t3 = lyr("vinyl", [("sm", [("WE", 25.74), ("DIDN'T", 25.86), ("VIBE", 26.35)]), ("big", [("THEN", 26.84)])], x=70, y=140, width=600, maxbig=300)
    for j, dt in enumerate([0, .05, .1, .15, .2]):                                        # glitch on THEN
        js(f'tl.set("#{t3}", {{x: {R.choice([-18, 14, -8, 20, 0]) if j < 4 else 0}, filter: "{"drop-shadow(6px 0 #0ff) drop-shadow(-6px 0 #f0f)" if j < 4 else "none"}"}}, {T(26.84) + dt:.3f});')
    punch("vinyl", 26.84, .07)

    # 4. But now I want you: the phone slams in and rings, her name on the screen
    i, l, t, s = obj("phone", "o3_phone", 540, 760, 1100, 28.74, z=5, enter="drop", d=.6, idle=None)
    scr = (f'<div class="pscr" style="left:{172 * s:.0f}px;top:{86 * s:.0f}px;width:{(852 - 172) * s:.0f}px;height:{(1456 - 86) * s:.0f}px">'
           '<div class="ring1"></div><div class="ring2"></div><div class="who">her</div><div class="call">calling...</div></div>')
    put("phone", f'<div id="pwrap" style="position:absolute;left:{l:.0f}px;top:{t:.0f}px;width:{1024 * s:.0f}px;height:{1536 * s:.0f}px;z-index:5">{scr}</div>')
    HIDE.append("#pwrap")
    js(f'tl.fromTo("#pwrap", {{opacity: 0}}, {{opacity: 1, duration: .2, immediateRender: false}}, {T(29.0)});')
    js(f'tl.fromTo("#pwrap", {{y: -1500}}, {{y: 0, duration: .6, ease: "bounce.out", immediateRender: false}}, {T(28.74)});')
    js(f'tl.fromTo("#pwrap .ring1, #pwrap .ring2", {{scale: .4, opacity: .9}}, {{scale: 2.4, opacity: 0, duration: .9, ease: "power2.out", '
       f'stagger: .3, repeat: 2, immediateRender: false}}, {T(29.05)});')
    for tb in (29.2, 29.75):                                                             # the buzz
        js(f'tl.fromTo("#{i}, #pwrap", {{rotation: 0}}, {{keyframes: [{{rotation: -2.5, duration: .04}}, {{rotation: 2.5, duration: .04}}, '
           f'{{rotation: -2, duration: .04}}, {{rotation: 2, duration: .04}}, {{rotation: -1, duration: .04}}, {{rotation: 0, duration: .04}}], '
           f'immediateRender: false}}, {T(tb):.3f});')
        cue(tb, "buzz")
    parts("phone", "dust", 12, z=7)
    lyr("phone", [("sm", [("BUT", 28.98), ("NOW", 29.19)]), ("big", [("I", 29.41), ("WANT", 29.60), ("YOU", 29.74)])], x=80, y=130, width=920, z=9)
    punch("phone", 29.74)

    # 5. So, I-I-I: the eye; each I stamps and the camera steps into the pupil
    px, py = bgpt(524, 746)
    glow("eye", px, py, 300, "rgba(255,90,30,.8)", 31.27, op=.85, z=2, pulse=.25)
    lyr("eye", [("sm", [("SO,", 30.89)]), ("big", [("I-", 31.27), ("I-", 31.51), ("I,", 31.99)])], x=80, y=150, width=920, maxbig=250, align="center")
    k = k_of("eye")
    for j, tk in enumerate([31.27, 31.51, 31.99]):
        js(f'tl.to("#m{k}", {{scale: {1.07 + .08 * j:.2f}, duration: .12, ease: "power4.out", transformOrigin: "{px:.0f}px {py:.0f}px"}}, {T(tk):.3f});')
        cue(tk, "hit")
    parts("eye", "ember", 16, z=6, area=(250, 450, 600, 700))

    # 6. Pure desire: the swirl turns, embers rise, she rises out of the fire
    k = k_of("desire")
    js(f'tl.fromTo("#bg{k}", {{rotation: 0, scale: 1.3}}, {{rotation: 55, scale: 1.45, duration: 2.6, ease: "none", immediateRender: false}}, {T(32.2)});')
    glow("desire", 540, 1150, 520, "rgba(255,110,30,.85)", 33.28, op=.9, z=3, pulse=.3)
    obj("desire", "c4_her_dance", 560, 980, 900, 32.9, z=5, enter="rise", d=.8, idle=(16, 5, .7))
    parts("desire", "ember", 34, z=7)
    lyr("desire", [("sm", [("PURE", 33.00)]), ("big", [("DESIRE", 33.28)])], x=70, y=110, width=940, maxbig=260)
    punch("desire", 33.28)
    leak(33.3, 100, "rgba(255,80,20,.9)", .6, .9)

    # 7. So heart racin': the heart beats on every syllable, faster; the ECG races
    i, *_ = obj("heart", "o4_heart", 540, 820, 760, 34.76, z=5, enter="pop", d=.5, idle=None)
    t, beat = 35.21, .38
    while t < 37.0:
        js(f'tl.fromTo("#{i} > .ob", {{scale: 1}}, {{keyframes: [{{scale: 1.12, duration: .05}}, {{scale: 1, duration: .15}}], ease: "power2.out", '
           f'immediateRender: false}}, {T(t):.3f});')
        beat = max(.17, beat * .9)
        t += beat
    glow("heart", 540, 820, 420, "rgba(255,40,60,.7)", 35.21, op=.7, z=3, pulse=.19)
    put("heart", '<svg id="ecg" class="ecg" viewBox="0 0 1080 200" width="1080" height="200"><path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" '
                 'd="M0 120 H200 L230 120 L250 60 L270 180 L290 20 L312 150 L332 120 H470 L500 120 L520 60 L540 180 L560 20 L582 150 L602 120 H740 L770 120 '
                 'L790 60 L810 180 L830 20 L852 150 L872 120 H1080"/></svg>')
    HIDE.append("#ecg")
    js(f'tl.set("#ecg", {{opacity: 1}}, {T(35.2)});')
    js(f'tl.fromTo("#ecg path", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .8, ease: "none", repeat: 2, immediateRender: false}}, {T(35.2)});')
    parts("heart", "dust", 14, z=7)
    lyr("heart", [("sm", [("SO", 35.21), ("HEART", 35.54)]), ("big", [("RACIN'", 35.86)])], x=70, y=110, width=940)
    punch("heart", 35.86)
    cue(35.86, "heartbeat")

    # 8. Entire body sayin' ah-ooh-ah: she dances under moving spotlights; each ah-ooh-ah lands somewhere new
    k = k_of("body")
    put("body", '<div class="beams" id="beams"><i></i><i></i><i></i></div>')
    HIDE.append("#beams")
    js(f'tl.set("#beams", {{opacity: 1}}, {T(37.0)});')
    js(f'tl.fromTo("#beams i", {{rotation: (k) => [-28, 0, 28][k]}}, {{rotation: (k) => [22, -26, -18][k], duration: 1.3, ease: "sine.inOut", yoyo: true, '
       f'repeat: 3, immediateRender: false}}, {T(37.0)});')
    i, *_ = obj("body", "c4_her_dance", 560, 930, 1080, 37.1, z=5, enter="rise", d=.7, idle=(20, 6, .64))
    parts("body", "spark", 14, z=6)
    parts("body", "dust", 16, z=7)
    lyr("body", [("sm", [("ENTIRE", 37.15), ("BODY", 37.96)]), ("bigw", [("SAYIN'", 38.43)])], x=70, y=110, width=760, dim=39.05, out=39.6)
    lyr("body", [("scr", [("ah-", 39.11)])], x=60, y=430, width=520, maxbig=200, z=10)
    lyr("body", [("scr", [("ooh-", 39.73)])], x=480, y=650, width=540, z=10)
    lyr("body", [("scr", [("ah", 40.37)])], x=200, y=980, width=680, z=10)
    for tk, dx in ((39.11, -50), (39.73, 60), (40.37, 0)):
        punch("body", tk, .05)
        js(f'tl.to("#c{k}", {{x: {dx}, duration: .5, ease: "power3.out"}}, {T(tk):.3f});')
    js(f'tl.to("#c{k}", {{scale: 1.5, duration: .8, ease: "power2.in", transformOrigin: "540px 760px"}}, {T(40.4):.3f});')
    leak(39.1, -100, "rgba(255,90,140,.85)", .55, .6)
    leak(40.4, 200, "rgba(255,140,60,.85)", .6, .7)

    # 9. I want you to make you my girlfriend: the ring box on the bar, the diamond flares on GIRLFRIEND
    i, l, t, s = obj("ring", "o5_ringbox", 540, 1030, 760, 41.2, z=5, enter="pop", d=.55, idle=(12, 2, 1.3))
    x0, y0, x1, y1 = BOX["o5_ringbox"]
    dx_, dy_ = 540 + (522 - (x0 + x1) / 2) * s, 1030 + (560 - (y0 + y1) / 2) * s
    put("ring", f'<svg id="spk" class="spark2" viewBox="-50 -50 100 100" style="left:{dx_ - 110:.0f}px;top:{dy_ - 110:.0f}px;width:220px;height:220px">'
                '<path d="M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z" fill="#fff"/></svg>')
    HIDE.append("#spk")
    js(f'tl.fromTo("#spk", {{opacity: 0, scale: 0, rotation: -60}}, {{opacity: 1, scale: 1.3, rotation: 0, duration: .35, ease: "back.out(2.4)", '
       f'immediateRender: false}}, {T(43.30)});')
    js(f'tl.to("#spk", {{rotation: 90, scale: .6, opacity: .0, duration: 1.0, ease: "power2.in"}}, {T(43.7)});')
    glow("ring", dx_, dy_, 300, "rgba(255,240,220,.9)", 43.30, op=.9, z=6, pulse=.3)
    cue(43.30, "sparkle")
    parts("ring", "spark", 12, z=7, area=(150, 450, 780, 800))
    lyr("ring", [("sm", [("I", 41.21), ("WANT", 41.33), ("YOU", 41.82), ("TO", 42.30), ("MAKE", 42.49), ("YOU", 42.63), ("MY", 43.11)]),
                 ("big", [("GIRLFRIEND", 43.30)])], x=80, y=130, width=920, maxsm=52)
    lyr("ring", [("scrw", [("yeah", 44.22)])], x=700, y=520, width=300, maxbig=130)
    punch("ring", 43.30, .06)
    leak(41.2, 0, "rgba(255,170,90,.9)", .5, .6)

    # 10. Wait 'til the world ends: the globe turns over the sunset; it cracks and the sun flares on WORLD ENDS
    i, *_ = obj("globe", "o6_globe", 540, 560, 560, 44.76, z=5, enter="rise", d=.6, idle=(14, 0, 1.3))
    js(f'tl.fromTo("#{i} > .ob img", {{rotation: -10}}, {{rotation: 40, duration: 3.2, ease: "none", immediateRender: false}}, {T(44.76)});')
    js(f'tl.fromTo("#{i}", {{x: 0}}, {{keyframes: [{{x: -16, duration: .05}}, {{x: 14, duration: .05}}, {{x: -10, duration: .05}}, {{x: 8, duration: .05}}, '
       f'{{x: 0, duration: .06}}], immediateRender: false}}, {T(46.17):.3f});')
    put("globe", f'<svg id="crack" class="crack" viewBox="0 0 400 400" style="left:340px;top:360px;width:400px;height:400px">'
                 '<path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M200 20 L185 120 L230 170 L170 240 L215 300 L190 390 M230 170 L320 150 '
                 'L380 190 M170 240 L80 260 L30 230"/></svg>')
    HIDE.append("#crack")
    js(f'tl.set("#crack", {{opacity: 1}}, {T(46.17)});')
    js(f'tl.fromTo("#crack path", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .25, ease: "power2.out", immediateRender: false}}, {T(46.17)});')
    sx, sy = bgpt(505, 723)
    glow("globe", sx, sy, 380, "rgba(255,200,110,.95)", 46.48, op=.95, z=4, pulse=.25)
    cue(46.17, "shatter")
    parts("globe", "dust", 16, z=7)
    lyr("globe", [("sm", [("WAIT", 44.88), ("'TIL", 45.21), ("THE", 45.69)]), ("big", [("WORLD", 46.17), ("ENDS", 46.48)])], x=80, y=960, width=920)
    punch("globe", 46.17, .06)

    # 11. Badman deserves ya: he walks in, a gold crown draws itself on his head
    i = obj("badman", "c1_him_profile", 560, 860, 1150, 47.5, z=5, enter="left", d=.7, idle=(8, 1, 1.6))[0]
    x0, y0, x1, y1 = BOX["c1_him_profile"]
    s = 1150 / (y1 - y0)
    hx = 560 + (480 - (x0 + x1) / 2) * s
    hy = 860 - 575 + (75 - y0) * s
    put("badman", f'<svg id="crown" class="crown" viewBox="0 0 200 120" style="left:{hx - 115:.0f}px;top:{hy - 125:.0f}px">'
                  '<path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M15 105 L28 30 L68 70 L100 12 L132 70 L172 30 L185 105 Z"/></svg>')
    HIDE.append("#crown")
    js(f'tl.set("#crown", {{opacity: 1}}, {T(47.65)});')
    js(f'tl.fromTo("#crown path", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .55, ease: "power2.inOut", immediateRender: false}}, {T(47.65)});')
    js(f'tl.fromTo("#crown", {{scale: 1.5, rotation: -14, y: -60}}, {{scale: 1, rotation: -6, y: 0, duration: .5, ease: "back.out(2)", immediateRender: false}}, {T(47.65)});')
    js(f'tl.to("#crown", {{y: -10, duration: .8, ease: "sine.inOut", yoyo: true, repeat: 2}}, {T(48.2)});')
    cue(47.65, "sparkle")
    parts("badman", "spark", 10, z=7, area=(250, 100, 600, 500))
    parts("badman", "dust", 12, z=7)
    lyr("badman", [("big", [("BADMAN", 47.65)]), ("sm", [("DESERVES", 48.18), ("YA", 48.75)])], x=80, y=960, width=920, maxbig=250)
    lyr("badman", [("scrw", [("yeah", 49.56)])], x=640, y=640, width=360, maxbig=150)
    punch("badman", 47.65, .06)

    # 12. Badman buy Birkins: bags drop on every syllable and bounce
    for j, (cx, cy, h, td, rot) in enumerate([(270, 900, 380, 50.23, -10), (810, 860, 400, 50.70, 9), (330, 1200, 360, 51.01, 6),
                                             (760, 1180, 420, 51.33, -6), (545, 1010, 520, 51.52, 0)]):
        obj("birkin", "o7_handbag", cx, cy, h, td, z=5 + j, rot=rot, enter="drop", d=.55, idle=None)
        cue(td + .22, "thud")
    parts("birkin", "spark", 10, z=11)
    lyr("birkin", [("sm", [("BADMAN", 50.23), ("BUY", 50.70)]), ("big", [("BIRKINS", 51.01)])], x=60, y=110, width=960, z=12)
    punch("birkin", 51.01, .06)

    # 13. For you, for certain: the record cover falls in turning, CERTAIN stamps across it
    i = nid("o")
    put("certain", f'<div class="print" id="{i}" style="left:230px;top:420px;width:620px;height:620px"><img src="assets/img/cover.jpg" alt=""></div>')
    HIDE.append(f"#{i}")
    js(f'tl.fromTo("#{i}", {{opacity: 0, y: -900, rotation: 30, rotationY: 70, transformPerspective: 1200, filter: "blur(16px)"}}, {{opacity: 1, y: 0, '
       f'rotation: -4, rotationY: 0, filter: "blur(0px)", duration: .8, ease: "expo.out", immediateRender: false}}, {T(51.9)});')
    js(f'tl.to("#{i}", {{rotation: 2, y: -16, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 1}}, {T(52.7)});')
    j = nid("t")
    put("certain", f'<div class="stamp" id="{j}">CERTAIN</div>')
    HIDE.append(f"#{j}")
    js(f'tl.fromTo("#{j}", {{opacity: 0, scale: 2.6, rotation: -2}}, {{opacity: 1, scale: 1, rotation: -8, duration: .26, ease: "back.out(2)", '
       f'immediateRender: false}}, {T(53.42)});')
    cue(53.42, "stamp")
    flick(53.42, .35, .25)
    parts("certain", "spark", 12, z=7)
    lyr("certain", [("sm", [("FOR", 52.14), ("YOU,", 52.62), ("FOR", 52.94)])], x=60, y=200, width=960, maxsm=80, align="center")
    punch("certain", 53.42, .07)

    # 14. Search, I been searchin': the lens sweeps the party, magnifying it, and finds her
    k = k_of("search")
    obj("search", "c3_her_turn", 860, 1080, 640, 55.0, z=4, enter="none", idle=(6, 1, 1.5))
    lx0, ly0, lh = 300, 760, 980                                   # the magnifier: visible box centre and height
    x0, y0, x1, y1 = BOX["o8_magnifier"]
    s = lh / (y1 - y0)
    ml, mt = lx0 - ((x0 + x1) / 2) * s, ly0 - ((y0 + y1) / 2) * s
    gx, gy, gr = ml + 405 * s, mt + 516 * s, 262 * s                # glass centre and radius in frame px
    m = 1.8
    path = [(55.25, -650, 260), (55.75, 0, 0), (56.5, 320, -150), (57.3, 120, 120), (58.1, 470, 180)]   # (t, dx, dy): ends on her
    put("search", f'<div id="lens" style="position:absolute;left:0;top:0;width:{FW}px;height:{FH}px;z-index:6">'
                  f'<img src="{G}o8_magnifier.png?m=1" style="position:absolute;left:{ml:.0f}px;top:{mt:.0f}px;width:{1024 * s:.0f}px;height:{1536 * s:.0f}px">'
                  f'<div class="mag" style="left:{gx - gr:.0f}px;top:{gy - gr:.0f}px;width:{2 * gr:.0f}px;height:{2 * gr:.0f}px">'
                  f'<div id="magin" style="position:absolute;left:{gr - gx * m:.0f}px;top:{gr - gy * m:.0f}px;width:{FW * m:.0f}px;height:{FH * m:.0f}px">'
                  f'<img src="{G}b1_party.png?m=1" style="position:absolute;left:0;top:{-90 * m:.0f}px;width:{FW * m:.0f}px;height:{1620 * m:.0f}px">'
                  f'<img src="{G}c3_her_turn.png?m=1" id="magher" style="position:absolute"></div><i class="glass"></i></div></div>')
    HIDE.append("#lens")
    # her inside the lens: same place as the cut-out above, magnified
    hx0, hy0, hx1, hy1 = BOX["c3_her_turn"]
    hs = 640 / (hy1 - hy0)
    hl, ht = 860 - ((hx0 + hx1) / 2) * hs, 1080 - ((hy0 + hy1) / 2) * hs
    js(f'tl.set("#magher", {{left: {hl * m:.0f}, top: {ht * m:.0f}, width: {1024 * hs * m:.0f}, height: {1536 * hs * m:.0f}}}, 0);')
    js(f'tl.fromTo("#lens", {{opacity: 0, rotation: -20}}, {{opacity: 1, rotation: 0, duration: .5, ease: "expo.out", '
       f'immediateRender: false}}, {T(55.25)});')
    for (ta, ax, ay), (tb, bx, by) in zip(path, path[1:]):
        js(f'tl.fromTo("#lens", {{x: {ax}, y: {ay}}}, {{x: {bx}, y: {by}, duration: {tb - ta:.2f}, ease: "power2.inOut", immediateRender: false}}, {T(ta):.3f});')
        js(f'tl.fromTo("#magin", {{x: {-ax * m:.0f}, y: {-ay * m:.0f}}}, {{x: {-bx * m:.0f}, y: {-by * m:.0f}, duration: {tb - ta:.2f}, ease: "power2.inOut", '
           f'immediateRender: false}}, {T(ta):.3f});')
    SC[k][5] = (gx + path[-1][1], gy + path[-1][2])
    parts("search", "dust", 16, z=8)
    lyr("search", [("big", [("SEARCH,", 55.38)]), ("sm", [("I", 56.48), ("BEEN", 56.67), ("SEARCHIN'", 56.80)])], x=60, y=100, width=960, maxbig=230)
    punch("search", 55.38, .05)
    cue(55.3, "air")

    # 15. Woah, woah, ah: the swirl spins; three stutter pushes
    k = k_of("woah")
    js(f'tl.fromTo("#bg{k}", {{rotation: 0, scale: 1.35}}, {{rotation: -90, scale: 1.35, duration: 1.9, ease: "power1.in", immediateRender: false}}, {T(58.4)});')
    for j, tk in enumerate([59.06, 59.38, 59.77]):
        js(f'tl.to("#m{k}", {{scale: {1.12 + .14 * j:.2f}, duration: .1, ease: "power4.out", transformOrigin: "540px 720px"}}, {T(tk):.3f});')
        cue(tk, "hit")
    parts("woah", "ember", 24, z=6)
    lyr("woah", [("bigw", [("WOAH,", 59.06)]), ("bigw", [("WOAH,", 59.38)]), ("big", [("AH", 59.77)])], x=80, y=280, width=920, align="center", maxbig=200)

    # 16-20. And I want you x5: memories, each slaps in full frame, then becomes a polaroid on the pile
    W = [("w1", [60.17, 60.35, 60.54, 61.02], 61.66, "the slow one", (-190, -250, -7)),
         ("w2", [65.37, 65.51, 65.84, 66.19], 66.82, "you, laughing", (200, -190, 6)),
         ("w3", [70.52, 70.67, 70.99, 71.34], 71.96, "walk me home", (-170, 190, 4)),
         ("w4", [75.67, 75.82, 76.15, 76.50], 77.10, "'42, for two", (190, 240, -5)),
         ("w5", [80.83, 80.98, 81.30, 81.66], 82.28, "for certain", (0, -10, -2))]
    layouts = [dict(rows=lambda w: [("sm", [("AND", w[0]), ("I", w[1])]), ("big", [("WANT", w[2]), ("YOU", w[3])])], x=60, y=110, width=960),
               dict(rows=lambda w: [("bigw", [("AND", w[0]), ("I", w[1])]), ("big", [("WANT", w[2]), ("YOU", w[3])])], x=60, y=760, width=960, align="center"),
               dict(rows=lambda w: [("bigw", [("AND", w[0])]), ("bigw", [("I", w[1])]), ("big", [("WANT", w[2])]), ("big", [("YOU", w[3])])],
                    x=60, y=100, width=420, maxbig=230),
               dict(rows=lambda w: [("sm", [("AND", w[0]), ("I", w[1])]), ("big", [("WANT", w[2]), ("YOU", w[3])])], x=80, y=130, width=920, align="center"),
               dict(rows=lambda w: [("sm", [("AND", w[0])]), ("big", [("I", w[1]), ("WANT", w[2]), ("YOU", w[3])])], x=80, y=150, width=920,
                    align="center", maxbig=250)]
    for n, (name, ws, end, cap, (px_, py_, pr)) in enumerate(W):
        k = k_of(name)
        lay = dict(layouts[n])
        rows = lay.pop("rows")(ws)
        shrink = end + (.3 if name == "w5" else .55)
        lyr(name, rows, out=shrink, **lay)
        punch(name, ws[2], .05)
        punch(name, ws[3], .04)
        SC[k].append(cap)
        if name == "w4":                                                  # the '42 pours into a glass
            i, *_ = obj(name, "o11_bottle", 330, 900, 820, 75.6, z=5, enter="rise", d=.6, idle=None, extra='<div class="lbl42">\'42</div>')
            js(f'tl.to("#{i}", {{rotation: -48, x: 210, y: -150, duration: .8, ease: "power2.inOut"}}, {T(76.2)});')
            obj(name, "o12_glass_top", 700, 1180, 440, 75.9, z=4, enter="pop", d=.5, idle=None)
            cue(76.6, "pour")
        if name == "w5":                                                  # him reaching out to her at sunset
            obj(name, "c2_him_reach", 330, 900, 980, 80.75, z=5, enter="left", d=.7, idle=(6, 1, 1.6))
            obj(name, "c3_her_turn", 790, 920, 940, 80.9, z=4, enter="right", d=.7, idle=(6, 1, 1.6))
        if name in ("w1", "w2", "w3"):
            glow(name, 540, 700, 520, "rgba(255,170,90,.45)", ws[2], op=.6, z=3, pulse=.6)
        parts(name, "dust", 14, z=7)
        leak(ws[2], R.choice([-200, 0, 200]), "rgba(255,140,70,.9)", .5, .8)
        # the polaroid: shutter flash, shrink, frame, land on the pile
        if True:
            js(f'tl.fromTo("#pl{k}", {{scale: 1, x: 0, y: 0, rotation: 0}}, {{scale: .52, x: {px_}, y: {py_}, rotation: {pr}, duration: .7, ease: "expo.inOut", '
               f'immediateRender: false}}, {T(shrink):.3f});')
            js(f'tl.fromTo("#pl{k} .pframe", {{opacity: 0}}, {{opacity: 1, duration: .25, immediateRender: false}}, {T(shrink) + .1:.3f});')
            js(f'tl.fromTo("#pl{k} .cap", {{opacity: 0, x: -20}}, {{opacity: 1, x: 0, duration: .5, ease: "power2.out", immediateRender: false}}, {T(shrink) + .7:.3f});')
            flick(shrink, .9, .4)
            cue(shrink - .03, "shutter")
    # the pile: drifts the whole time; pulls back at the end
    js(f'tl.fromTo("#pile", {{scale: 1, rotation: 0}}, {{scale: 1.05, rotation: 1, duration: {82.6 - 60.06:.2f}, ease: "none", immediateRender: false}}, {T(60.06)});')
    js(f'tl.to("#pile", {{scale: .82, rotation: -2, duration: 1.4, ease: "power2.inOut"}}, {T(82.6)});')
    parts(None, "petal", 26, t0=60.0, t1=LOGO + .5)


# ------------------------------------------------------------------------------------------------ transitions
def jag(x, y, r, n=44, seed=5):
    g = random.Random(seed)
    pts = []
    for j in range(n):
        a = 6.2832 * j / n
        rr = r * (1 + g.uniform(-.13, .13) + (.09 if j % 2 else -.05))
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return pts


def transitions():
    n_sc = len(SC)
    for k, sc in enumerate(SC):
        name, a, b, bg, kind, pt = sc[:6]
        prev = SC[k - 1][4] if k else None
        is_w = isw(name)
        if k == 0:
            js('tl.set("#s0", {opacity: 1}, 0);')
        elif prev in ("whipl", "whipr", "whipup", "whipdown"):
            js(f'tl.set("#s{k}", {{opacity: 1}}, {T(a) - .05:.3f});')
        elif prev == "portal":
            js(f'tl.set("#s{k}", {{opacity: 1}}, {T(a) - .56:.3f});')
        elif prev == "tear":
            js(f'tl.set("#s{k}", {{opacity: 1}}, {T(a) - .42:.3f});')
        elif prev == "zoom":
            pass
        else:
            js(f'tl.set("#s{k}", {{opacity: 1}}, {T(a) - .05:.3f});')
        if not is_w:
            push, dx, dy, r0, r1 = CAM[name]
            js(f'tl.fromTo("#p{k}", {{scale: 1, x: 0, y: 0, rotation: {r0}}}, {{scale: {1 + push}, x: {dx}, y: {dy}, rotation: {r1}, duration: {b - a + 1.2:.2f}, '
               f'ease: "none", immediateRender: false}}, {max(0, T(a) - .6):.3f});')
        else:
            js(f'tl.fromTo("#p{k}", {{scale: 1.02, x: 0, y: 0}}, {{scale: 1.16, x: {R.choice([-30, 30])}, y: -20, duration: 3.2, ease: "power1.out", '
               f'immediateRender: false}}, {T(a):.3f});')
        if k + 1 >= n_sc:
            continue
        nx = k + 1
        if kind == "portal":
            D = .55
            x, y = pt
            js(f'tl.to("#c{k}", {{scale: 9, filter: "blur(10px)", duration: {D}, ease: "power3.in", '
               f'transformOrigin: "{x:.0f}px {y:.0f}px"}}, {T(b) - D:.3f});')
            js(f'tl.fromTo("#s{nx}", {{clipPath: "circle(20px at {x:.0f}px {y:.0f}px)"}}, {{clipPath: "circle(1900px at {x:.0f}px {y:.0f}px)", '
               f'duration: {D + .15}, ease: "power3.in", immediateRender: false}}, {T(b) - D:.3f});')
            js(f'tl.fromTo("#c{nx}", {{scale: .3, filter: "blur(8px)"}}, {{scale: 1, filter: "blur(0px)", duration: {D + .35}, ease: "power3.out", '
               f'immediateRender: false, transformOrigin: "{x:.0f}px {y:.0f}px"}}, {T(b) - D:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {T(b) + .2:.3f});')
            js(f'tl.set("#s{nx}", {{clipPath: "none"}}, {T(b) + .2:.3f});')
            cue(b - .55, "portal")
            leak(b - .1, 0, "rgba(255,190,120,.9)", .55, .5)
        elif kind == "tear":
            x, y = pt
            small = "polygon(" + ", ".join(f"{px:.0f}px {py:.0f}px" for px, py in jag(x, y, 24, seed=k)) + ")"
            big = "polygon(" + ", ".join(f"{px:.0f}px {py:.0f}px" for px, py in jag(x, y, 1500, seed=k)) + ")"
            js(f'tl.fromTo("#s{nx}", {{clipPath: "{small}"}}, {{clipPath: "{big}", duration: .55, ease: "power3.in", immediateRender: false}}, {T(b) - .42:.3f});')
            js(f'tl.fromTo("#c{nx}", {{scale: 1.25}}, {{scale: 1, duration: .8, ease: "power3.out", immediateRender: false}}, {T(b) - .42:.3f});')
            js(f'tl.to("#c{k}", {{scale: 1.18, duration: .55, ease: "power3.in", transformOrigin: "{x:.0f}px {y:.0f}px"}}, {T(b) - .42:.3f});')
            tid = f"tear{k}"
            def ring(r):
                o = jag(x, y, r * 1.1 + 10, seed=k + 50)
                i_ = jag(x, y, r, seed=k)
                return "polygon(evenodd, " + ", ".join(f"{px:.0f}px {py:.0f}px" for px, py in o + [o[0]] + i_ + [i_[0]]) + ")"
            TEARS.append(f'<div class="tearfx" id="{tid}"></div>')
            js(f'tl.set("#{tid}", {{opacity: 1}}, {T(b) - .42:.3f});')
            js(f'tl.fromTo("#{tid}", {{clipPath: "{ring(24)}"}}, {{clipPath: "{ring(1500)}", duration: .55, ease: "power3.in", immediateRender: false}}, {T(b) - .42:.3f});')
            js(f'tl.set("#{tid}", {{opacity: 0}}, {T(b) + .14:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {T(b) + .14:.3f});')
            js(f'tl.set("#s{nx}", {{clipPath: "none"}}, {T(b) + .14:.3f});')
            cue(b - .42, "tear")
        elif kind in ("whipup", "whipdown", "whipl", "whipr"):
            dx, dy = {"whipup": (0, 1), "whipdown": (0, -1), "whipl": (-1, 0), "whipr": (1, 0)}[kind]
            fid = "mbx" if dx else "mby"
            js(f'tl.set("#m{k}, #m{nx}", {{filter: "url(#{fid})"}}, {T(b) - .3:.3f});')
            js(f'tl.fromTo("#{fid} feGaussianBlur", {{attr: {{stdDeviation: "0 0"}}}}, {{attr: {{stdDeviation: "{"90 0" if dx else "0 90"}"}}, duration: .3, '
               f'ease: "power2.in", immediateRender: false}}, {T(b) - .3:.3f});')
            js(f'tl.to("#{fid} feGaussianBlur", {{attr: {{stdDeviation: "0 0"}}, duration: .38, ease: "power2.out"}}, {T(b):.3f});')
            js(f'tl.fromTo("#c{k}", {{x: 0, y: 0}}, {{x: {-dx * 1250}, y: {dy * 1650}, duration: .3, ease: "power3.in", immediateRender: false}}, {T(b) - .3:.3f});')
            js(f'tl.fromTo("#c{nx}", {{x: {dx * 1250}, y: {-dy * 1650}}}, {{x: 0, y: 0, duration: .4, ease: "power3.out", immediateRender: false}}, {T(b) - .04:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {T(b) + .02:.3f});')
            js(f'tl.set("#m{k}, #m{nx}", {{filter: "none"}}, {T(b) + .4:.3f});')
            cue(b - .3, "whip")
        elif kind == "zoom":
            x, y = pt
            js(f'tl.to("#c{k}", {{scale: 1.7, filter: "blur(18px)", duration: .35, ease: "power3.in", transformOrigin: "{x:.0f}px {y:.0f}px"}}, {T(b) - .3:.3f});')
            js(f'tl.fromTo("#s{nx}", {{opacity: 0}}, {{opacity: 1, duration: .25, immediateRender: false}}, {T(b) - .15:.3f});')
            js(f'tl.fromTo("#c{nx}", {{scale: .6, filter: "blur(16px)"}}, {{scale: 1, filter: "blur(0px)", duration: .5, ease: "expo.out", immediateRender: false}}, {T(b) - .15:.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {T(b) + .15:.3f});')
            cue(b - .3, "air")
        elif kind in ("flash", "drop"):
            big = kind == "drop"
            flick(b, .95 if big else .8, .5 if big else .32)
            js(f'tl.fromTo("#c{nx}", {{scale: {1.4 if big else 1.2}, filter: "blur(12px)"}}, {{scale: 1, filter: "blur(0px)", duration: .55, ease: "expo.out", '
               f'immediateRender: false}}, {T(b):.3f});')
            js(f'tl.set("#s{k}", {{opacity: 0}}, {T(b):.3f});')
            leak(b - .05, R.choice([-150, 150]), "rgba(255,100,40,.95)", .85, .7)
            cue(b - .05, "drop" if big else "hit")
        elif kind == "slap":
            js(f'tl.fromTo("#pl{nx}", {{y: -1600, rotation: -10}}, {{y: 0, rotation: 0, duration: .5, ease: "expo.out", immediateRender: false}}, {T(b) - .05:.3f});')
            js(f'tl.set("#m{nx}", {{filter: "url(#mby)"}}, {T(b) - .05:.3f});')
            js(f'tl.fromTo("#mby feGaussianBlur", {{attr: {{stdDeviation: "0 70"}}}}, {{attr: {{stdDeviation: "0 0"}}, duration: .4, ease: "power2.out", '
               f'immediateRender: false}}, {T(b) - .05:.3f});')
            js(f'tl.set("#m{nx}", {{filter: "none"}}, {T(b) + .4:.3f});')
            cue(b - .1, "whip")
            cue(b + .25, "slap")
    # into the first memory from the woah flash: the first polaroid's table appears with it
    # the logo
    js(f'tl.fromTo("#logo", {{opacity: 0}}, {{opacity: 1, duration: .6, ease: "sine.inOut", immediateRender: false}}, {T(LOGO) - .1:.3f});')
    js(f'tl.fromTo("#logo img", {{opacity: 0, scale: 1.12, filter: "blur(18px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .7, ease: "power3.out", '
       f'immediateRender: false}}, {T(LOGO) + .1:.3f});')
    js(f'tl.fromTo("#logo .lsweep i", {{x: -700}}, {{x: 700, duration: .75, ease: "power2.inOut", immediateRender: false}}, {T(LOGO) + .6:.3f});')
    js(f'tl.fromTo("#logo .lstar", {{scale: 0, rotation: -45, opacity: 0}}, {{scale: 1, rotation: 0, opacity: 1, duration: .35, ease: "back.out(2.2)", '
       f'immediateRender: false}}, {T(LOGO) + 1.05:.3f});')
    js(f'tl.to("#logo .lstar", {{scale: .55, opacity: 0, duration: .4, ease: "power2.in"}}, {T(LOGO) + 1.4:.3f});')
    js(f'tl.to("#logo img", {{scale: .96, duration: 1.8, ease: "none"}}, {T(LOGO) + .8:.3f});')
    leak(LOGO - .1, 0, "rgba(255,150,80,.9)", .7, 1.0)
    cue(LOGO - .45, "logo")
    HIDE.append("#logo")


TEARS = []

CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Play"; font-style: italic; font-weight: 700; src: url("assets/fonts/PlayfairDisplay-700Italic.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #07070f; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #07070f; }}
.scene {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; }}
.push, .cam, .mb {{ position: absolute; inset: 0; }}
.bgi {{ position: absolute; left: 0; top: -90px; width: 1080px; height: 1620px; object-fit: cover; }}
.obj {{ position: absolute; opacity: 0; }}
.ob, .ob > img {{ position: absolute; inset: 0; }}
.ob > img {{ width: 100%; height: 100%; display: block; }}
.glow {{ position: absolute; opacity: 0; mix-blend-mode: screen; background-position: center; background-size: 100% 100%; }}
.lyr {{ position: absolute; opacity: 0; pointer-events: none; transform-origin: 50% 40%; }}
.ld {{ transform-origin: 30% 40%; }}
.lyr .w {{ display: inline-block; opacity: 1; white-space: nowrap; }}
.lyr .l {{ display: inline-block; }}
.sm {{ font-family: "Inter"; font-weight: 800; line-height: 1.15; color: #fff; letter-spacing: .06em; text-shadow: 0 3px 16px rgba(0,0,0,.75); white-space: nowrap; }}
.big, .bigw {{ font-family: "Anton"; line-height: .98; letter-spacing: .01em; white-space: nowrap; text-shadow: 0 8px 30px rgba(0,0,0,.6); }}
.big {{ color: #ff3048; text-shadow: 0 0 28px rgba(255,48,72,.5), 0 8px 30px rgba(0,0,0,.6); }}
.bigw {{ color: #fff; }}
.scr, .scrw {{ font-family: "Play"; font-style: italic; font-weight: 700; line-height: 1.05; white-space: nowrap; }}
.scr {{ color: #ff3048; text-shadow: 0 0 28px rgba(255,48,72,.55), 0 8px 26px rgba(0,0,0,.6); }}
.scrw {{ color: #fff; text-shadow: 0 6px 22px rgba(0,0,0,.7); }}
.lyr .big .w, .lyr .bigw .w {{ transform-origin: 50% 60%; }}
.ptg {{ position: absolute; inset: 0; pointer-events: none; }}
.pt {{ position: absolute; display: block; }}
.pt {{ background-position: center; background-size: 100% 100%; background-repeat: no-repeat; }}
.pt.dust {{ background-image: url(assets/img/fx/dust.png); }}
.pt.ember {{ background-image: url(assets/img/fx/ember.png); transform-origin: 50% 50%; }}
.pt.petal {{ background-image: url(assets/img/fx/petal.png); }}
.pt.spark {{ background-image: url(assets/img/fx/spark.png); }}
.spark2 {{ position: absolute; opacity: 0; z-index: 8; filter: drop-shadow(0 0 16px #fff) drop-shadow(0 0 40px #ffd9a0); }}
.mistw {{ position: absolute; inset: 0; opacity: 0; z-index: 6; }}
.mist {{ position: absolute; width: 150px; height: 150px; background: url(assets/img/fx/mist.png) center/100% 100% no-repeat; }}
.pscr {{ position: absolute; border-radius: 60px; overflow: hidden; background: radial-gradient(ellipse at 50% 35%, rgba(255,120,90,.55), rgba(40,10,40,.2) 70%); }}
.pscr .who {{ position: absolute; left: 0; right: 0; top: 30%; text-align: center; font: italic 700 130px/1 "Play"; color: #fff; text-shadow: 0 0 30px rgba(255,140,120,.9); }}
.pscr .call {{ position: absolute; left: 0; right: 0; top: 47%; text-align: center; font: 500 42px/1 "Inter"; color: rgba(255,255,255,.85); letter-spacing: .08em; }}
.ring1, .ring2 {{ position: absolute; left: 50%; top: 34%; width: 260px; height: 260px; margin: -130px; border-radius: 50%; border: 4px solid rgba(255,190,170,.85); }}
.ecg {{ position: absolute; left: 0; top: 1230px; opacity: 0; z-index: 7; }}
.ecg path {{ fill: none; stroke: #ff3048; stroke-width: 7; stroke-linejoin: round; filter: drop-shadow(0 0 10px #ff3048); }}
.beams {{ position: absolute; inset: 0; opacity: 0; z-index: 3; mix-blend-mode: screen; }}
.beams i {{ position: absolute; left: 50%; top: -120px; width: 260px; height: 1800px; margin-left: -130px; transform-origin: 50% 0;
  background: linear-gradient(rgba(255,220,170,.55), rgba(255,170,90,0) 85%); clip-path: polygon(42% 0, 58% 0, 100% 100%, 0 100%); filter: blur(6px); }}
.crack {{ position: absolute; opacity: 0; z-index: 6; overflow: visible; }}
.crack path {{ fill: none; stroke: #fff6e0; stroke-width: 5; filter: drop-shadow(0 0 8px #ffc070); }}
.crown {{ position: absolute; width: 230px; height: 138px; opacity: 0; z-index: 7; transform-origin: 50% 100%; overflow: visible; }}
.crown path {{ fill: rgba(255,200,90,.18); stroke: #ffc65a; stroke-width: 7; stroke-linejoin: round; filter: drop-shadow(0 0 12px #ffb040); }}
.print {{ position: absolute; opacity: 0; background: #f4ecdf; padding: 18px; box-shadow: 0 30px 60px rgba(0,0,0,.6); z-index: 5; }}
.print img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.stamp {{ position: absolute; left: 120px; top: 930px; width: 840px; text-align: center; opacity: 0; z-index: 8; font: 400 190px/1.3 "Anton"; color: #ff3048; padding-top: 6px;
  border: 12px solid #ff3048; border-radius: 18px; transform: rotate(-8deg); text-shadow: 0 0 20px rgba(255,48,72,.5); box-shadow: 0 0 30px rgba(255,48,72,.35); }}
.mag {{ position: absolute; border-radius: 50%; overflow: hidden; }}
.mag .glass {{ position: absolute; inset: 0; border-radius: 50%; box-shadow: inset 0 0 50px rgba(255,220,180,.55), inset 0 0 6px rgba(255,230,190,.9);
  background: linear-gradient(140deg, rgba(255,255,255,.28), rgba(255,255,255,0) 40%); }}
.lbl42 {{ position: absolute; left: 0; right: 0; top: 54%; text-align: center; font: italic 700 130px/1 "Play"; color: #6a2a12; opacity: .85; }}
.pol {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
.pclip {{ position: absolute; inset: 0; overflow: hidden; }}
.pframe {{ position: absolute; left: -40px; top: -40px; right: -40px; bottom: -230px; background: #f3ece0; opacity: 0;
  box-shadow: 0 40px 90px rgba(0,0,0,.65); }}
.pframe .cap {{ position: absolute; left: 70px; bottom: 50px; font: italic 700 110px/1 "Play"; color: #2b1b14; opacity: 0; }}
.table {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 40%, #3a2216, #120a08 75%); }}
.table img {{ position: absolute; left: 0; top: -90px; width: 1080px; height: 1620px; object-fit: cover; opacity: .35; filter: blur(8px); }}
#pile {{ position: absolute; inset: 0; z-index: 30; }}
#gparts {{ position: absolute; inset: 0; z-index: 33; pointer-events: none; }}
.tearfx {{ position: absolute; inset: 0; opacity: 0; z-index: 35; pointer-events: none; background: #efe6d6 url(assets/img/grain.png); }}
.leak {{ position: absolute; top: -300px; width: 1400px; height: 2000px; opacity: 0; z-index: 39; mix-blend-mode: screen; pointer-events: none;
  background-position: center; background-size: 100% 100%; background-repeat: no-repeat; }}
#flash {{ position: absolute; inset: 0; z-index: 40; background: #fff4e6; opacity: 0; }}
#vig {{ position: absolute; inset: 0; z-index: 41; pointer-events: none; background: radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,.5) 100%); }}
#grain {{ position: absolute; left: -40px; top: -40px; width: 1160px; height: 1520px; z-index: 42; pointer-events: none; opacity: .1; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
#logo {{ position: absolute; inset: 0; z-index: 50; background: #05030d; opacity: 0; overflow: hidden; }}
.lin {{ position: absolute; left: 0; top: {FH / 2 - 540:.0f}px; width: 1080px; height: 1080px; transform: scale(.6); }}
#logo img {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block;
  -webkit-mask-image: radial-gradient(circle closest-side, #000 74%, transparent 100%); mask-image: radial-gradient(circle closest-side, #000 74%, transparent 100%); }}
.lsweep {{ position: absolute; left: 228px; top: 228px; width: 624px; height: 624px; border-radius: 50%; overflow: hidden; mix-blend-mode: screen;
  -webkit-mask-image: radial-gradient(circle, #000 70%, transparent 71%); mask-image: radial-gradient(circle, #000 70%, transparent 71%); }}
.lsweep i {{ position: absolute; left: -50%; top: 0; width: 200%; height: 100%;
  background: linear-gradient(115deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.7) 50%, rgba(255,255,255,0) 60%); }}
.lstar {{ position: absolute; left: 651px; top: 285px; width: 80px; height: 80px; opacity: 0; filter: drop-shadow(0 0 14px #fff) drop-shadow(0 0 30px #c9a8ff); }}
"""


def main():
    shots()
    transitions()
    # light leaks: a pool of four, used round-robin
    for j, (t, x, color, op, d) in enumerate(sorted(LEAKS)):
        lid = f"#lk{j % 4}"
        key = ",".join(color[5:].split(",")[:3])
        js(f'tl.set("{lid}", {{backgroundImage: "url(assets/img/fx/{LEAK_SPRITE[key]}.png)"}}, {max(0, t - .01):.3f});')
        js(f'tl.fromTo("{lid}", {{opacity: 0, x: {x - 500}, scale: .8}}, {{keyframes: [{{opacity: {op}, x: {x - 150}, scale: 1, duration: {d * .35:.2f}, '
           f'ease: "power2.out"}}, {{opacity: 0, x: {x + 300}, scale: 1.15, duration: {d * .65:.2f}, ease: "power1.in"}}], immediateRender: false}}, {t:.3f});')
    g = random.Random(3)
    for f in range(int(DUR * 12)):
        js(f'tl.set("#grain", {{x: {g.randint(0, 40)}, y: {g.randint(0, 40)}}}, {f / 12:.3f});')
    html_sc, html_w = [], []
    for k, sc in enumerate(SC):
        name, a, b, bg = sc[:4]
        inner = (f'<div class="mb" id="m{k}"><div class="cam" id="c{k}"><div class="push" id="p{k}">'
                 f'<img class="bgi" id="bg{k}" src="{G}{bg}.png?s={k}" alt="">{"".join(EL[name])}</div>{"".join(ELT[name])}</div></div>')
        HIDE.append(f"#s{k}")
        if isw(name):
            cap = sc[6]
            table = f'<div class="table"><img src="{G}b9_wall.png?t=1" alt=""></div>' if name == "w1" else ""
            html_w.append(f'<div class="scene" id="s{k}" style="z-index:{k + 1};overflow:visible">{table}<div class="pol" id="pl{k}">'
                          f'<div class="pframe"><span class="cap">{cap}</span></div><div class="pclip">{inner}</div></div></div>')
        else:
            html_sc.append(f'<div class="scene" id="s{k}" style="z-index:{k + 1}">{inner}</div>')
    leaks = "".join(f'<div class="leak" id="lk{j}" style="left:-160px"></div>' for j in range(4))
    svgf = ('<svg width="0" height="0" style="position:absolute"><filter id="mbx" x="-30%" y="0" width="160%" height="100%" color-interpolation-filters="sRGB">'
            '<feGaussianBlur stdDeviation="0 0"/></filter><filter id="mby" x="0" y="-30%" width="100%" height="160%" color-interpolation-filters="sRGB">'
            '<feGaussianBlur stdDeviation="0 0"/></filter></svg>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>For Certain lyric edit 3x4</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    {svgf}
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      {"".join(html_sc)}
      <div id="pile">{"".join(html_w)}</div>
      <div id="gparts">{"".join(GPARTS)}</div>
      {"".join(TEARS)}
      {leaks}<div id="flash"></div><div id="vig"></div><div id="grain"></div>
      <div id="logo"><div class="lin"><img src="assets/img/brand/nxtlvl_logo.png" alt="Nxtlvl"><div class="lsweep"><i></i></div>
        <svg class="lstar" viewBox="-50 -50 100 100"><path d="M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z" fill="#fff"/></svg></div></div>
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
    json.dump([{"t": round(t, 3), "type": k} for t, k in sorted(CUES) if t >= 0], open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SC)} shots, {DUR} s (song {OFF}-{SONG_OUT})")


if __name__ == "__main__":
    main()
