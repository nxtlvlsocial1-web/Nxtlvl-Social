"""Builds index.html for the engagement invite (two couples), 1080x1920, 50 s. Version 3.

python3 -I build/generate.py      (run from the project root)

Each scene is its own illustrated world (palace arch over a lotus lake in a scene palette, or an
ivory watercolour garden page). Scenes are joined by a camera pan with a marble pillar sweeping
past in the foreground. Scene changes sit on the song's phrase grid (vocals at 7.13 s, ~3.76 s
phrases).
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art  # noqa: E402
import elements as el  # noqa: E402
import figures as fg  # noqa: E402
import worlds as wd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 50.0
X = 0.55                     # half of a pillar transition
CUTS = [10.89, 18.41, 25.93, 33.45, 40.97, 44.9]

S = {                        # nominal scene windows (start, end)
    "ganesh": (0.0, CUTS[0]),
    "invite": (CUTS[0], CUTS[1]),
    "c1": (CUTS[1], CUTS[2]),
    "c2": (CUTS[2], CUTS[3]),
    "both": (CUTS[3], CUTS[4]),
    "date": (CUTS[4], CUTS[5]),
    "close": (CUTS[5], DUR),
}
KIND = {"ganesh": ("palace", "mint"), "invite": ("garden", "gazebo"), "c1": ("palace", "haldi"),
        "c2": ("palace", "sangeet"), "both": ("palace", "wedding"), "date": ("garden", "fountain"),
        "close": ("palace", "mint")}

HALDI_G = ("#f5c542", "#b45309", "#fde68a", "#fff7e0", "#a16207")
HALDI_B = ("#facc15", "#db2777", "#f472b6", "#86efac", "#d4a24c")
SANGEET_G = ("#cfe3d2", "#c9973f", "#f6ead2", "#efe9dc", "#7a5a2a")
SANGEET_B = ("#15803d", "#facc15", "#be185d", "#fbcfe8", "#d4a24c")


# ------------------------------------------------------------------ markup helpers
def scene(sid, inner):
    a, b = S[sid]
    a0, b0 = max(0.0, a - X), min(DUR, b + X)
    kind, sub = KIND[sid]
    world = wd.palace(sub, sid, fl_seed=len(sid) * 3) if kind == "palace" else wd.garden_vignette(sub, sid)
    tone = "light" if sub == "sangeet" else "dark"
    return (f'<div id="sc-{sid}" class="clip scene {tone}" data-start="{a0}" data-duration="{round(b0 - a0, 2)}" '
            f'data-track-index="{2 + list(S).index(sid) % 2}"><div class="pan">{world}{inner}</div></div>')


def at(y, inner, cls=""):
    return f'<div class="row {cls}" style="top:{y}px"><span class="t">{inner}</span></div>'


def letters(text):
    return "".join(f'<span class="lt">{"&nbsp;" if c == " " else c}</span>' for c in text)


def box(cls, x, y, w, h, inner):
    return f'<div class="box {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def stage(cls, inner):
    """A full-frame SVG layer for figures (frame coordinates)."""
    return f'<svg class="stage {cls}" viewBox="0 0 1080 1920" width="1080" height="1920">{inner}</svg>'


def build_scenes():
    out = []
    out.append(scene("ganesh", (
        box("gwrap", 290, 360, 500, 507, '<img src="assets/img/ganesh.png" width="500" height="507" alt="">') +
        at(900, "॥ श्री गणेशाय नमः ॥", "deva g-deva") +
        at(982, "Shree Ganeshaya Namah", "script g-en") +
        at(1092, art.divider(440), "g-div") +
        at(1140, "वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ।", "shloka g-sh1") +
        at(1194, "निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥", "shloka g-sh2")
    )))
    out.append(scene("invite", (
        at(296, letters("With the divine blessings of"), "ital lts i-1") +
        at(352, letters("LORD GANESHA & OUR ELDERS"), "cap2 lts i-2") +
        box("medal i-hands", 395, 418, 290, 290, el.hands_medallion(290)) +
        "".join(f'<div class="spark i-sp" style="transform:translate({x}px,{y}px)">{art.sparkle()}</div>'
                for x, y in [(540, 530), (585, 555), (500, 570)]) +
        at(734, letters("we joyfully invite you to celebrate the"), "body lts i-3") +
        at(782, '<span class="wipe i-eng">Engagement</span>', "big i-4") +
        at(952, letters("CEREMONY"), "cap3 lts i-5") +
        at(1030, art.divider(440), "i-div") +
        at(1076, letters("of our two beautiful couples"), "ital lts i-6") +
        at(1136, letters("two families · two love stories · one celebration"), "small lts i-7")
    )))
    for n, him, her, figure in (
            (1, "Manish Tamboli", "Jyoti",
             f'<g class="swing">{"<g transform=" + chr(34) + "translate(540 1395) scale(1.12)" + chr(34) + ">"}'
             f'{wd.swing_couple(HALDI_G, HALDI_B)}</g></g>'),
            (2, "Harsh Aswal", "Shalu",
             f'<g transform="translate(540 1530) scale(1.0)">{wd.sangeet_couple(SANGEET_G, SANGEET_B)}</g>')):
        out.append(scene(f"c{n}", (
            stage(f"c{n}-stage", figure) +
            at(500, letters("THE ENGAGEMENT OF"), f"cap lts c{n}-cap") +
            at(546, f'<span class="wipe c{n}-him">{him}</span>', "name") +
            at(656, "&amp;", f"amp c{n}-amp") +
            at(694, f'<span class="wipe c{n}-her">{her}</span>', "name") +
            at(812, art.divider(380), f"c{n}-div") +
            "".join(f'<div class="spark c{n}-sp" style="transform:translate({x}px,{y}px)">{art.sparkle()}</div>'
                    for x, y in [(270, 580), (810, 570), (340, 740), (740, 750), (540, 520)])
        )))
    out.append(scene("both", (
        stage("b-stage",
              f'<g class="bp1"><g transform="translate(310 1535) scale(.76)">{fg.couple(fg.COUPLE1, "bq1")}</g></g>'
              f'<g class="bp2"><g transform="translate(770 1535) scale(.76)">{fg.couple(fg.COUPLE2, "bq2")}</g></g>') +
        at(500, letters("TWICE THE JOY"), "cap lts b-cap") +
        at(546, '<span class="wipe b-s1">Two love stories,</span>', "script2") +
        at(636, '<span class="wipe b-s2">one joyous celebration</span>', "script2") +
        at(768, letters("Please join us as they exchange rings"), "ital sm lts b-t1") +
        at(816, letters("and begin a bright new chapter together"), "ital sm lts b-t2") +
        box("heart b-heart", 505, 1240, 70, 63, heart(70))
    )))
    out.append(scene("date", (
        at(320, letters("SAVE THE DATE"), "cap4 lts d-cap") +
        at(400, art.divider(440), "d-div") +
        at(462, "OCTOBER", "cap2 d-mon") +
        f'<div class="daterow" style="top:515px"><div class="side d-day">FRIDAY</div>'
        f'<div class="num d-num">30</div><div class="side d-yr">2026</div></div>' +
        at(780, art.pin(60), "d-pin") +
        at(872, "VENUE", "cap2 d-ven") +
        at(930, letters("Near 2 Petrol Pump,"), "addr lts d-a1") +
        at(994, letters("Industrial Area Phase 1,"), "addr lts d-a2") +
        at(1058, letters("Mangolpuri, New Delhi – 110083"), "addr lts d-a3") +
        at(1160, art.divider(440), "d-div2")
    )))
    out.append(scene("close", (
        at(470, letters("Awaiting your"), "ital lts x-1") +
        at(518, '<span class="wipe x-2">gracious presence</span>', "script2") +
        box("pav x-pav", 364, 640, 352, 448, el.pavilion()) +
        box("pea x-pea", 352, 742, 170, 200,
            f'<svg viewBox="-85 -60 170 200" width="170" height="200">{art.peacock(10, 20, .34)}</svg>') +
        at(908, "शुभ सगाई", "deva2 x-ss") +
        box("ele x-el1", 140, 920, 250, 161, f'<svg viewBox="-150 -255 420 270" width="250" height="161">'
            f'{el.elephant()}</svg>') +
        box("ele x-el2", 690, 920, 250, 161, f'<svg viewBox="-270 -255 420 270" width="250" height="161">'
            f'{el.elephant(True)}</svg>') +
        box("bq x-bq", 340, 975, 400, 175, f'<svg viewBox="-200 -150 400 175" width="400" height="175">'
            f'{el.bouquet()}</svg>') +
        at(1162, '<span class="wipe x-3">Happily ever after begins</span>', "script3") +
        at(1252, "30 · 10 · 2026", "cap2 x-date") +
        at(1300, letters("With love & warm wishes"), "ital lts x-5")
    )))
    return "".join(out)


def heart(size=90, col=art.ROSE):
    return (f'<svg viewBox="0 0 100 90" width="{size}" height="{size * .9:.0f}"><path d="M50 88 C20 64 0 46 0 26 '
            f'C0 10 12 0 27 0 C38 0 46 6 50 14 C54 6 62 0 73 0 C88 0 100 10 100 26 C100 46 80 64 50 88 Z" '
            f'fill="{col}"/></svg>')


# ------------------------------------------------------------------ petals (deterministic)
def petals():
    rnd = random.Random(7)
    shapes = art.petal_shapes()
    els, tw = [], []
    for i in range(30):
        els.append(f'<div class="petal" id="pt{i}">{shapes[i % len(shapes)]}</div>')
        t = 2.0 + rnd.uniform(0, 7)
        while t < DUR:
            d = rnd.uniform(7.5, 11)
            x0 = rnd.uniform(-20, 1080)
            dx = rnd.uniform(-160, 160)
            s = rnd.uniform(0.6, 1.25)
            r0, r1 = rnd.uniform(0, 360), rnd.uniform(200, 700) * rnd.choice((1, -1))
            tw.append(f'tl.fromTo("#pt{i}",{{x:{x0:.0f},y:-60,rotation:{r0:.0f},scale:{s:.2f},opacity:.95}},'
                      f'{{x:{x0 + dx:.0f},y:1980,rotation:{r0 + r1:.0f},duration:{d:.2f},ease:"none"}},{t:.2f});')
            t += d + rnd.uniform(0, 1.5)
    return "".join(els), "\n".join(tw)


# ------------------------------------------------------------------ timeline
T = []


def add(s):
    T.append(s)


def rise(sel, t, d=.6):
    add(f'tl.fromTo("{sel}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{t:.2f});')


def write(sel, t, per=.035):
    """WedMeGood-style reveal: letters fade up out of a soft blur, one after another."""
    add(f'tl.fromTo("{sel} .lt",{{opacity:0,y:10,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",'
        f'duration:.45,stagger:{per},ease:"power2.out"}},{t:.2f});')


def wipe(sel, t, d):
    add(f'tl.fromTo("{sel}",{{clipPath:"inset(-30% 100% -40% 0%)"}},{{clipPath:"inset(-30% 0% -40% 0%)",'
        f'duration:{d},ease:"power1.inOut"}},{t:.2f});')


def draw_div(sel, t):
    add(f'tl.fromTo("{sel} .dv",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.7,'
        f'ease:"power2.out"}},{t:.2f});')
    add(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:.3}},{t:.2f});')


def pop(sel, t, d=.55, frm="scale:0,opacity:0", ease="back.out(2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,duration:{d},ease:"{ease}"}},{t:.2f});')


def sparks(sel, t):
    add(f'tl.fromTo("{sel}",{{scale:0,opacity:0,rotation:0}},{{scale:1.1,opacity:1,rotation:90,duration:.4,'
        f'stagger:.1,ease:"back.out(3)"}},{t:.2f});')
    add(f'tl.to("{sel}",{{scale:0,opacity:0,rotation:180,duration:.5,stagger:.1,ease:"power2.in"}},{t + .7:.2f});')


def timeline():
    # camera pans between scenes, with the marble pillar sweeping past in the foreground
    ids = list(S)
    for k, c in enumerate(CUTS):
        out_id, in_id = ids[k], ids[k + 1]
        add(f'tl.fromTo("#sc-{out_id} .pan",{{x:0}},{{x:-1080,duration:{2 * X},ease:"power2.inOut"}},{c - X:.2f});')
        add(f'tl.fromTo("#sc-{in_id} .pan",{{x:1080}},{{x:0,duration:{2 * X},ease:"power2.inOut"}},{c - X:.2f});')
        add(f'tl.fromTo("#pillar",{{x:1240}},{{x:-480,duration:{2 * X + .1:.2f},ease:"power2.inOut"}},{c - X - .05:.2f});')
    # slow camera push and living details in every world
    for sid, (a, b) in S.items():
        a0, b0 = max(0, a - X), min(DUR, b + X)
        add(f'tl.fromTo("#sc-{sid} .world",{{scale:1}},{{scale:1.035,duration:{b0 - a0:.2f},ease:"none"}},{a0:.2f});')
        if KIND[sid][0] == "palace":
            n = max(1, int((b0 - a0) / 2.2))
            add(f'tl.fromTo("#sc-{sid} .hang",{{rotation:-2.5}},{{rotation:2.5,duration:2.2,ease:"sine.inOut",'
                f'yoyo:true,repeat:{n},stagger:.06}},{a0:.2f});')
            add(f'tl.fromTo("#sc-{sid} .w-pea",{{rotation:-1.5}},{{rotation:1.5,duration:1.9,ease:"sine.inOut",'
                f'yoyo:true,repeat:{n}}},{a0:.2f});')
        else:
            add(f'tl.fromTo("#sc-{sid} .wisteria",{{y:-30}},{{y:0,duration:2.2,ease:"power2.out"}},{a0:.2f});')
            add(f'tl.fromTo("#sc-{sid} .gv-centre",{{y:220,opacity:0}},{{y:0,opacity:1,duration:2.0,'
                f'ease:"power3.out"}},{a + .1:.2f});')
            add(f'tl.fromTo("#sc-{sid} .gv-back",{{y:120}},{{y:0,duration:2.4,ease:"power3.out"}},{a:.2f});')
            add(f'tl.fromTo("#sc-{sid} .swan",{{x:-20}},{{x:30,duration:{b0 - a0:.2f},ease:"sine.inOut"}},{a0:.2f});')

    # doors open onto the mint palace
    add('tl.fromTo(".door-medal",{scale:.92,opacity:.9},{scale:1.04,opacity:1,duration:.5,ease:"sine.inOut"},0);')
    add('tl.to(".door-medal",{scale:.6,opacity:0,duration:.45,ease:"power2.in"},.55);')
    add('tl.fromTo("#door-l",{rotationY:0},{rotationY:-104,duration:1.6,ease:"power2.inOut"},.6);')
    add('tl.fromTo("#door-r",{rotationY:0},{rotationY:104,duration:1.6,ease:"power2.inOut"},.6);')
    add('tl.fromTo("#doorframe",{scale:1,opacity:1},{scale:1.5,opacity:0,duration:1.2,ease:"power2.in"},1.7);')

    # Ganesh ji
    add('tl.fromTo(".gwrap",{opacity:0,scale:.9,filter:"blur(10px)"},{opacity:1,scale:1,filter:"blur(0px)",'
        'duration:1.7,ease:"power2.out"},2.4);')
    add('tl.fromTo(".gwrap img",{scale:1},{scale:1.03,duration:2.6,ease:"sine.inOut",yoyo:true,repeat:1},4.2);')
    rise(".g-deva", 3.9)
    wipe(".g-en", 4.5, 1.2)
    draw_div(".g-div", 5.6)
    rise(".g-sh1", 7.13)
    rise(".g-sh2", 7.6)

    # invitation (ivory garden page)
    a = S["invite"][0]
    write(".i-1", a + .3)
    write(".i-2", a + .9, .03)
    pop(".i-hands", a + 1.4, .7, "scale:.6,opacity:0", "back.out(1.6)")
    add(f'tl.fromTo(".i-hands .hm-his",{{x:-90,opacity:0}},{{x:0,opacity:1,duration:.9,ease:"power2.out"}},{a + 1.6:.2f});')
    add(f'tl.fromTo(".i-hands .hm-her",{{x:110,opacity:0}},{{x:0,opacity:1,duration:.9,ease:"power2.out"}},{a + 1.9:.2f});')
    pop(".i-hands .hm-ring", a + 2.7, .45, 'scale:0,opacity:0,transformOrigin:"50% 50%"', "back.out(3)")
    sparks(".i-sp", a + 2.85)
    write(".i-3", a + 3.0, .025)
    wipe(".i-eng", a + 3.9, 1.2)
    write(".i-5", a + 4.8, .07)
    draw_div(".i-div", a + 5.3)
    write(".i-6", a + 5.5, .03)
    write(".i-7", a + 6.1, .02)

    # couples
    for n in (1, 2):
        a = S[f"c{n}"][0]
        write(f".c{n}-cap", a + .4, .04)
        wipe(f".c{n}-him", a + 1.0, 1.0)
        pop(f".c{n}-amp", a + 1.9, .4, "scale:.4,opacity:0", "back.out(3)")
        wipe(f".c{n}-her", a + 2.1, .8)
        draw_div(f".c{n}-div", a + 2.8)
        sparks(f".c{n}-sp", a + 3.0)
    a, b = S["c1"]
    add(f'tl.fromTo(".c1-stage",{{y:260,opacity:0}},{{y:0,opacity:1,duration:1.4,ease:"power3.out"}},{a + .3:.2f});')
    add(f'tl.fromTo(".swing",{{rotation:-3}},{{rotation:3,duration:1.6,ease:"sine.inOut",yoyo:true,repeat:5}},{a + .3:.2f});')
    a, b = S["c2"]
    add(f'tl.fromTo(".c2-stage",{{opacity:0,y:120}},{{opacity:1,y:0,duration:1.2,ease:"power3.out"}},{a + .3:.2f});')
    # sangeet: they sway together to the beat while music notes drift up
    add(f'tl.fromTo(".dsway",{{rotation:-2}},{{rotation:2,duration:.8,ease:"sine.inOut",yoyo:true,repeat:9}},{a + .5:.2f});')
    add(f'tl.fromTo(".cs-g",{{y:0}},{{y:-10,duration:.4,ease:"sine.inOut",yoyo:true,repeat:17}},{a + .5:.2f});')
    add(f'tl.fromTo(".cs-b",{{y:-10}},{{y:0,duration:.4,ease:"sine.inOut",yoyo:true,repeat:17}},{a + .5:.2f});')
    add(f'tl.fromTo(".note",{{y:40,opacity:0}},{{y:-60,opacity:1,duration:2.4,stagger:.5,ease:"sine.out"}},{a + 1.0:.2f});')

    # both couples
    a = S["both"][0]
    write(".b-cap", a + .4, .05)
    wipe(".b-s1", a + .9, 1.0)
    wipe(".b-s2", a + 1.8, 1.2)
    add(f'tl.fromTo(".bp1",{{x:-320,opacity:0}},{{x:0,opacity:1,duration:1.5,ease:"power2.out"}},{a + .6:.2f});')
    add(f'tl.fromTo(".bp2",{{x:320,opacity:0}},{{x:0,opacity:1,duration:1.5,ease:"power2.out"}},{a + .6:.2f});')
    write(".b-t1", a + 3.1, .025)
    write(".b-t2", a + 4.0, .025)
    pop(".b-heart", a + 2.4, .5, "scale:0,opacity:0", "back.out(3)")
    add(f'tl.to(".b-heart",{{scale:1.15,duration:.36,ease:"sine.inOut",yoyo:true,repeat:9}},{a + 2.9:.2f});')

    # date and venue
    a = S["date"][0]
    write(".d-cap", a + .3, .04)
    draw_div(".d-div", a + .7)
    rise(".d-mon", a + .8)
    pop(".d-num", a + .9, .6, "scale:2.2,opacity:0", "back.out(1.6)")
    add(f'tl.fromTo(".d-day",{{x:-110,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},{a + 1.1:.2f});')
    add(f'tl.fromTo(".d-yr",{{x:110,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},{a + 1.1:.2f});')
    add(f'tl.fromTo(".d-pin",{{y:-240,opacity:0}},{{y:0,opacity:1,duration:.7,ease:"bounce.out"}},{a + 1.4:.2f});')
    rise(".d-ven", a + 1.8)
    write(".d-a1", a + 1.95, .02)
    write(".d-a2", a + 2.25, .02)
    write(".d-a3", a + 2.55, .02)
    draw_div(".d-div2", a + 3.0)

    # closing: pavilion, elephants, bouquet
    a = S["close"][0]
    write(".x-1", a + .3, .04)
    wipe(".x-2", a + .7, 1.0)
    add(f'tl.fromTo(".x-pav",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:1.2,'
        f'ease:"power2.out"}},{a + .8:.2f});')
    add(f'tl.fromTo(".x-el1",{{x:-260,opacity:0}},{{x:0,opacity:1,duration:1.2,ease:"power2.out"}},{a + 1.0:.2f});')
    add(f'tl.fromTo(".x-el2",{{x:260,opacity:0}},{{x:0,opacity:1,duration:1.2,ease:"power2.out"}},{a + 1.0:.2f});')
    pop(".x-bq", a + 1.8, .6, 'scale:0,opacity:0,transformOrigin:"50% 100%"', "back.out(1.8)")
    pop(".x-ss", a + 1.9, .5, "scale:.6,opacity:0", "back.out(2)")
    add(f'tl.fromTo(".x-pea",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.6,ease:"power2.out"}},{a + 2.0:.2f});')
    wipe(".x-3", a + 2.3, 1.1)
    rise(".x-date", a + 3.0)
    write(".x-5", a + 3.2, .03)
    return "\n".join(T)


CSS = """
@font-face { font-family: "Pinyon"; src: url("assets/fonts/pinyon.ttf"); }
@font-face { font-family: "Marcellus"; src: url("assets/fonts/marcellus.ttf"); }
@font-face { font-family: "Playfair"; font-weight: 400 900; src: url("assets/fonts/playfair.ttf"); }
@font-face { font-family: "Playfair"; font-style: italic; font-weight: 400 900; src: url("assets/fonts/playfair-italic.ttf"); }
@font-face { font-family: "Yatra"; src: url("assets/fonts/yatra.ttf"); }
@font-face { font-family: "NotoDeva"; font-weight: 100 900; src: url("assets/fonts/notoserifdeva.ttf"); }
:root { --maroon: #7d1d3f; --rose: #b0365f; --gold: #8a5f1c; --ink: #3f2533; --teal: #1d5566; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #bfe3d9; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #bfe3d9; }
.clip { position: absolute; inset: 0; }
.scene { overflow: hidden; }
.pan { position: absolute; inset: 0; }
.world { position: absolute; left: 0; top: 0; transform-origin: 50% 60%; }
.stage { position: absolute; left: 0; top: 0; }
.row { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }
.row svg { display: inline-block; vertical-align: top; }
.t { display: inline-block; }
.lt { display: inline-block; }
.box { position: absolute; }
.box > svg, .box > img { display: block; }
.cap { font: 30px "Marcellus"; letter-spacing: 6px; color: var(--gold); }
.cap2 { font: 34px "Marcellus"; letter-spacing: 4px; color: var(--teal); }
.cap3 { font: 54px "Marcellus"; letter-spacing: 14px; color: var(--maroon); }
.cap4 { font: 56px "Marcellus"; letter-spacing: 6px; color: var(--maroon); }
.ital { font: italic 400 40px "Playfair"; color: var(--ink); }
.ital.sm { font-size: 34px; }
.body { font: 400 38px "Playfair"; color: var(--ink); }
.small { font: italic 400 30px "Playfair"; color: var(--gold); }
.addr { font: 500 42px "Playfair"; color: var(--ink); }
.deva { font: 62px "Yatra"; color: #c2410c; }
.deva2 { font: 38px "Yatra"; color: #a3123f; }
.shloka { font: 500 34px "NotoDeva"; color: var(--teal); }
.script { font: 72px "Pinyon"; color: var(--rose); line-height: 1.25; }
.script2 { font: 74px "Pinyon"; color: var(--rose); line-height: 1.25; }
.script3 { font: 56px "Pinyon"; color: var(--maroon); line-height: 1.25; }
.big { font: 132px "Pinyon"; color: var(--rose); line-height: 1.25; }
.name { font: 90px "Pinyon"; color: var(--maroon); line-height: 1.25; }
.amp { font: italic 400 46px "Playfair"; color: var(--gold); }
.light .cap { color: #f5d58a; } .light .name { color: #fff4e6; } .light .amp { color: #f5d58a; }
.light .name, .light .cap { text-shadow: 0 2px 14px rgba(40, 10, 60, .45); }
.wipe { display: inline-block; padding: 0 24px; }
.gwrap { transform-origin: 50% 50%; }
.gwrap img { width: 500px; height: 507px; }
.spark { position: absolute; left: -20px; top: -20px; }
.heart { transform-origin: 50% 50%; }
.pav svg { width: 100%; height: 100%; }
.daterow { position: absolute; left: 0; width: 1080px; display: flex; align-items: center; justify-content: center; gap: 22px; }
.side { font: 34px "Marcellus"; letter-spacing: 4px; color: var(--teal); border-top: 2px solid #c9973f;
  border-bottom: 2px solid #c9973f; padding: 12px 4px; width: 190px; text-align: center; }
.num { font: 700 200px "Playfair"; color: var(--rose); line-height: 1.05; width: 250px; text-align: center; }
.petal { position: absolute; left: 0; top: 0; z-index: 25; }
#pillar { position: absolute; left: 0; top: 0; width: 260px; height: 1920px; filter: blur(3px); z-index: 30; }
#doors { z-index: 40; perspective: 2200px; }
#door-l, #door-r { position: absolute; top: 0; width: 540px; height: 1920px; }
#door-l { left: 0; transform-origin: 0% 50%; } #door-r { left: 540px; transform-origin: 100% 50%; }
#doorframe { position: absolute; inset: 0; transform-origin: 50% 45%; }
.door-medal { position: absolute; left: 430px; top: 320px; width: 220px; height: 220px; border-radius: 50%;
  background: #fbf0dc; border: 6px solid #c9973f; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 10px rgba(201,151,63,.25); }
.door-medal img { display: block; width: 190px; height: 193px; }
"""


def main():
    petal_html, petal_tl = petals()
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Engagement invite 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      {build_scenes()}
      <div id="petals" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-allow-overflow>{petal_html}</div>
      <div id="pillarclip" class="clip" data-start="{CUTS[0] - X - .1:.2f}" data-duration="{CUTS[-1] - CUTS[0] + 2 * X + .3:.2f}" data-track-index="5" data-layout-allow-overflow>
        <div id="pillar">{wd.pillar()}</div>
      </div>
      <div id="doors" class="clip" data-start="0" data-duration="3.4" data-track-index="6">
        <div id="door-l">{art.door_panel("l")}</div><div id="door-r">{art.door_panel("r")}</div>
        <div id="doorframe">{art.door_frame()}</div>
        <div class="door-medal"><img src="assets/img/ganesh.png" width="190" height="193" alt=""></div>
      </div>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="7" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set(".rg, .dv", {{ strokeDasharray: 1, strokeDashoffset: 1, opacity: 0 }});
      gsap.set(".petal", {{ x: -100, y: -80, opacity: 0 }});
      gsap.set("#pillar", {{ x: 1300 }});
      document.querySelectorAll(".hang").forEach(e => gsap.set(e, {{ svgOrigin: e.dataset.o }}));
      gsap.set(".w-pea", {{ svgOrigin: "215 1560" }});
      gsap.set(".swing", {{ svgOrigin: "540 0" }});
      gsap.set(".dsway", {{ svgOrigin: "540 1530" }});
{timeline()}
{petal_tl}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    print("wrote index.html", len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
