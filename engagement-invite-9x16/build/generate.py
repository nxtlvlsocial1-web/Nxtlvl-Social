"""Builds index.html for the engagement invite (two couples), 1080x1920, 50 s.

python3 -I build/generate.py      (run from the project root)

Scenes follow the client's track: vocals enter at 7.13 s and phrases turn over every ~3.76 s, so
scene changes sit on that grid (10.89, 18.41, 25.93, 33.45, 40.97 ...).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art  # noqa: E402
import figures as fg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 50.0
PH = 3.76


def g(k):
    return round(7.13 + PH * k, 2)


S = {
    "doors": (0.0, 3.4),
    "ganesh": (1.9, g(1)),      # -> 10.89
    "invite": (g(1), g(3)),     # -> 18.41
    "c1": (g(3), g(5)),         # -> 25.93
    "c2": (g(5), g(7)),         # -> 33.45
    "both": (g(7), g(9)),       # -> 40.97
    "date": (g(9), 45.6),
    "close": (45.6, DUR),
}


# ------------------------------------------------------------------ markup helpers
def scene(sid, inner):
    a, b = S[sid]
    return (f'<div id="sc-{sid}" class="clip scene" data-start="{a}" data-duration="{round(b - a, 2)}" '
            f'data-track-index="3">{inner}</div>')


def at(y, inner, cls=""):
    return f'<div class="row {cls}" style="top:{y}px"><span class="t">{inner}</span></div>'


def chars(text, cls):
    return "".join(f'<span class="{cls}">{"&nbsp;" if c == " " else c}</span>' for c in text)


def box(cls, x, y, w, h, inner):
    return f'<div class="box {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def heart(size=90, col=art.ROSE):
    return (f'<svg viewBox="0 0 100 90" width="{size}" height="{size * .9:.0f}"><path d="M50 88 C20 64 0 46 0 26 '
            f'C0 10 12 0 27 0 C38 0 46 6 50 14 C54 6 62 0 73 0 C88 0 100 10 100 26 C100 46 80 64 50 88 Z" '
            f'fill="{col}"/></svg>')


def rays():
    n = 28
    paths = "".join(
        f'<path d="M0 0 L{math.cos(i / n * math.tau - .045) * 520:.0f} {math.sin(i / n * math.tau - .045) * 520:.0f} '
        f'L{math.cos(i / n * math.tau + .045) * 520:.0f} {math.sin(i / n * math.tau + .045) * 520:.0f} Z"/>'
        for i in range(n))
    return (f'<svg viewBox="-520 -520 1040 1040" width="1040" height="1040"><defs><radialGradient id="rayf">'
            f'<stop offset="0" stop-color="#ffd98a" stop-opacity=".7"/><stop offset="1" stop-color="#ffd98a" '
            f'stop-opacity="0"/></radialGradient></defs><g fill="url(#rayf)">{paths}</g></svg>')


def couple_window(n, pal):
    """Arch window with palace and hills; the couple stands on the terrace holding hands."""
    w, h = 600, 660
    feet = h * .78 + 34
    hearts = "".join(f'<g class="hf c{n}-hf" transform="translate({x} {feet - 330})"><path d="M0 18 C-6 13 -10 9 -10 5 '
                     f'C-10 2 -8 0 -5 0 C-3 0 -1 1 0 3 C1 1 3 0 5 0 C8 0 10 2 10 5 C10 9 6 13 0 18 Z" '
                     f'fill="{art.ROSE}"/></g>' for x in (270, 290, 305, 282))
    inner = (f'<g transform="translate(285 {feet:.0f}) scale(.76)">{fg.couple(pal, f"cp{n}")}</g>{hearts}'
             f'<g class="vbird c{n}-vb" transform="translate(-60 120)">{art.bird("b", .8)}'
             f'<g transform="translate(40 -18)">{art.bird("b", .6)}</g></g>')
    return box(f"win c{n}-win", 240, 785, w, h, art.vignette(f"c{n}", w, h, inner))


def both_window():
    w, h = 700, 580
    feet = h * .78 + 30
    inner = (f'<g transform="translate(200 {feet:.0f}) scale(.56)">{fg.couple(fg.COUPLE1, "bp1")}</g>'
             f'<g transform="translate(500 {feet:.0f}) scale(.56)">{fg.couple(fg.COUPLE2, "bp2")}</g>'
             f'<g class="vbird b-vb" transform="translate(-60 110)">{art.bird("b", .8)}'
             f'<g transform="translate(40 -18)">{art.bird("b", .6)}</g></g>')
    return box("win b-win", 190, 668, w, h, art.vignette("both", w, h, inner))


def build_scenes():
    out = []
    # Ganesh ji, presented like the reference: soft fade-in of the line art, title below
    out.append(scene("ganesh", (
        f'<div class="rayclip"><div class="rays">{rays()}</div></div>' +
        box("gwrap", 330, 400, 420, 525, fg.ganesh_brush()) +
        at(975, "॥ श्री गणेशाय नमः ॥", "deva g-deva") +
        at(1060, "Shree Ganeshaya Namah", "script g-en") +
        at(1180, art.divider(440), "g-div") +
        at(1235, "वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ।", "shloka g-sh1") +
        at(1292, "निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥", "shloka g-sh2")
    )))
    out.append(scene("invite", (
        at(470, "With the divine blessings of", "ital i-1") +
        at(532, "LORD GANESHA &amp; OUR ELDERS", "cap2 i-2") +
        at(615, art.rings(170), "i-rings") +
        at(790, "we joyfully invite you to celebrate the", "body i-3") +
        at(860, '<span class="wipe i-eng">Engagement</span>', "big i-4") +
        at(1045, chars("CEREMONY", "ic"), "cap3 i-5") +
        at(1135, art.divider(440), "i-div") +
        at(1185, "of our two beautiful couples", "ital i-6") +
        at(1265, "two families · two love stories · one celebration", "small i-7")
    )))
    for n, him, her, pal in ((1, "Manish Tamboli", "Jyoti", fg.COUPLE1), (2, "Harsh Aswal", "Shalu", fg.COUPLE2)):
        out.append(scene(f"c{n}", (
            at(440, "THE ENGAGEMENT OF", f"cap c{n}-cap") +
            at(488, f'<span class="wipe c{n}-him">{him}</span>', "name") +
            at(598, "&amp;", f"amp c{n}-amp") +
            at(640, f'<span class="wipe c{n}-her">{her}</span>', "name") +
            at(752, art.divider(380), f"c{n}-div") +
            couple_window(n, pal) +
            "".join(f'<div class="spark c{n}-sp" style="transform:translate({x}px,{y}px)">{art.sparkle()}</div>'
                    for x, y in [(290, 520), (790, 510), (360, 690), (720, 700), (540, 470)])
        )))
    out.append(scene("both", (
        at(440, "TWICE THE JOY", "cap b-cap") +
        at(490, '<span class="wipe b-s1">Two love stories,</span>', "script2") +
        at(580, '<span class="wipe b-s2">one joyous celebration</span>', "script2") +
        both_window() +
        at(1268, "Please join us as they exchange rings", "ital sm b-t1") +
        at(1316, "and begin a bright new chapter together", "ital sm b-t2")
    )))
    out.append(scene("date", (
        at(470, chars("SAVE THE DATE", "dc"), "cap4 d-cap") +
        at(548, art.divider(440), "d-div") +
        at(610, "OCTOBER", "cap2 d-mon") +
        f'<div class="daterow" style="top:665px"><div class="side d-day">FRIDAY</div>'
        f'<div class="num d-num">30</div><div class="side d-yr">2026</div></div>' +
        at(930, art.pin(60), "d-pin") +
        at(1025, "VENUE", "cap2 d-ven") +
        at(1085, "Near 2 Petrol Pump,", "addr d-a1") +
        at(1150, "Industrial Area Phase 1,", "addr d-a2") +
        at(1215, "Mangolpuri, New Delhi – 110083", "addr d-a3") +
        at(1320, art.divider(440), "d-div2")
    )))
    out.append(scene("close", (
        box("diya dy-l", 175, 470, 110, 101, art.diya()) + box("diya dy-r", 795, 470, 110, 101, art.diya()) +
        at(470, "Awaiting your", "ital x-1") +
        at(522, '<span class="wipe x-2">gracious presence</span>', "script2") +
        at(660, "Come, bless the couples as they begin", "body x-3") +
        at(716, "their beautiful journey together", "body x-4") +
        at(800, art.divider(380), "x-div") +
        box("mini x-m1", 200, 860, 290, 290, art.wreath(31, 290) + '<div class="mini-t">M<i>&amp;</i>J</div>') +
        box("mini x-m2", 590, 860, 290, 290, art.wreath(32, 290) + '<div class="mini-t">H<i>&amp;</i>S</div>') +
        box("heart x-heart", 505, 975, 70, 63, heart(70)) +
        at(1190, "30 · 10 · 2026", "cap2 x-date") +
        at(1250, "With love &amp; warm wishes", "ital x-5")
    )))
    return "".join(out)


# ------------------------------------------------------------------ petals (deterministic)
def petals():
    rnd = random.Random(7)
    shapes = art.petal_shapes()
    els, tw = [], []
    for i in range(34):
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


def wipe(sel, t, d):
    add(f'tl.fromTo("{sel}",{{clipPath:"inset(-30% 100% -40% 0%)"}},{{clipPath:"inset(-30% 0% -40% 0%)",'
        f'duration:{d},ease:"power1.inOut"}},{t:.2f});')


def draw_div(sel, t):
    add(f'tl.fromTo("{sel} .dv",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.7,'
        f'ease:"power2.out"}},{t:.2f});')
    add(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:.3}},{t:.2f});')


def pop(sel, t, d=.55, frm="scale:0,opacity:0", ease="back.out(2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,duration:{d},ease:"{ease}"}},{t:.2f});')


def fade_out(sel, t):
    add(f'tl.to("{sel}",{{opacity:0,y:-24,duration:.4,ease:"power2.in"}},{t:.2f});')


def timeline():
    # background life
    add(f'tl.fromTo("#bg",{{scale:1.0}},{{scale:1.06,duration:{DUR},ease:"none"}},0);')
    add(f'tl.fromTo("#clouds",{{x:-40}},{{x:70,duration:{DUR},ease:"none"}},0);')
    add('tl.fromTo("#sunglow",{opacity:.6},{opacity:1,duration:4,ease:"sine.inOut",yoyo:true,repeat:11},0);')
    for sel, amp, per in [("#trees-l", 1.2, 3.1), ("#trees-r", -1.2, 3.4), ("#bananas", 1.6, 2.6),
                          ("#pea-l", 1.5, 1.9), ("#pea-r", -1.5, 2.1), ("#toran", 0.6, 2.9)]:
        n = int(DUR / per)
        add(f'tl.fromTo("{sel}",{{rotation:{-amp}}},{{rotation:{amp},duration:{per},ease:"sine.inOut",'
            f'yoyo:true,repeat:{n - 1}}},0);')
    for k, (t0, y0) in enumerate([(5.0, 520), (19.0, 380), (42.0, 600)]):
        add(f'tl.fromTo(".flock{k}",{{x:-200,y:{y0}}},{{x:1240,y:{y0 - 160},duration:7,ease:"none"}},{t0});')

    # doors
    add('tl.fromTo(".door-medal",{scale:.92,opacity:.9},{scale:1.04,opacity:1,duration:.5,ease:"sine.inOut"},0);')
    add('tl.to(".door-medal",{scale:.6,opacity:0,duration:.45,ease:"power2.in"},.55);')
    add('tl.fromTo("#door-l",{rotationY:0},{rotationY:-104,duration:1.6,ease:"power2.inOut"},.6);')
    add('tl.fromTo("#door-r",{rotationY:0},{rotationY:104,duration:1.6,ease:"power2.inOut"},.6);')
    add('tl.fromTo("#doorframe",{scale:1,opacity:1},{scale:1.5,opacity:0,duration:1.2,ease:"power2.in"},1.7);')
    add('tl.fromTo("#arch",{opacity:0,scale:.92},{opacity:1,scale:1,duration:.9,ease:"power2.out"},2.0);')

    # Ganesh ji: soft fade-in with a little focus pull, then a warm glow (as in the reference)
    a, b = S["ganesh"]
    add(f'tl.fromTo("#sc-ganesh .rays",{{rotation:0}},{{rotation:30,duration:{b - 2.3:.2f},ease:"none"}},2.3);')
    add('tl.fromTo("#sc-ganesh .rays",{opacity:0,scale:.6},{opacity:1,scale:1,duration:1.6,ease:"power2.out"},2.6);')
    add('tl.fromTo(".gwrap",{opacity:0,scale:.94,filter:"blur(10px)"},{opacity:1,scale:1,filter:"blur(0px)",'
        'duration:1.7,ease:"power2.out"},3.0);')
    add('tl.fromTo(".gwrap svg",{filter:"drop-shadow(0 0 0px rgba(255,170,70,0))"},{filter:'
        '"drop-shadow(0 0 18px rgba(255,170,70,.85))",duration:1.4,ease:"sine.inOut",yoyo:true,repeat:1},4.7);')
    rise(".g-deva", 4.3)
    rise(".g-en", 4.9)
    draw_div(".g-div", 5.6)
    rise(".g-sh1", 7.13)
    rise(".g-sh2", 7.6)
    fade_out("#sc-ganesh .gwrap, #sc-ganesh .row", b - .45)
    add(f'tl.to("#sc-ganesh .rays",{{opacity:0,duration:.45}},{b - .45:.2f});')

    # invite
    a, b = S["invite"]
    rise(".i-1", a + .15)
    rise(".i-2", a + .5)
    add(f'tl.fromTo(".i-rings .rg",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.9,'
        f'stagger:.25,ease:"power2.inOut"}},{a + .8:.2f});')
    pop(".i-rings .rg-gem", a + 1.8, .4, 'scale:0,opacity:0,transformOrigin:"50% 50%"', "back.out(3)")
    rise(".i-3", a + 1.9)
    wipe(".i-eng", a + 2.5, 1.2)
    add(f'tl.fromTo(".i-5 .ic",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.35,stagger:.06,ease:"power2.out"}},'
        f'{a + 3.5:.2f});')
    draw_div(".i-div", a + 4.1)
    rise(".i-6", a + 4.4)
    rise(".i-7", a + 5.0)
    fade_out("#sc-invite .row", b - .45)

    # each couple: names, then the palace window with the couple walking in and joining hands
    for n in (1, 2):
        a, b = S[f"c{n}"]
        rise(f".c{n}-cap", a + .15)
        wipe(f".c{n}-him", a + .45, 1.0)
        pop(f".c{n}-amp", a + 1.35, .4, "scale:.4,opacity:0", "back.out(3)")
        wipe(f".c{n}-her", a + 1.55, .8)
        draw_div(f".c{n}-div", a + 2.2)
        add(f'tl.fromTo(".c{n}-win",{{opacity:0,scale:.86,y:40}},{{opacity:1,scale:1,y:0,duration:.9,'
            f'ease:"power3.out"}},{a + 1.2:.2f});')
        add(f'tl.fromTo(".cp{n}-g",{{x:-170,opacity:0}},{{x:0,opacity:1,duration:1.3,ease:"power2.out"}},{a + 1.8:.2f});')
        add(f'tl.fromTo(".cp{n}-b",{{x:170,opacity:0}},{{x:0,opacity:1,duration:1.3,ease:"power2.out"}},{a + 1.8:.2f});')
        pop(f".cp{n}-h", a + 3.05, .35, 'scale:0,opacity:0,transformOrigin:"50% 50%"', "back.out(3)")
        add(f'tl.fromTo(".cp{n}-g",{{rotation:-1.2,transformOrigin:"50% 100%"}},{{rotation:1.2,duration:1.6,'
            f'ease:"sine.inOut",yoyo:true,repeat:1}},{a + 3.2:.2f});')
        add(f'tl.fromTo(".cp{n}-b",{{rotation:1.2,transformOrigin:"50% 100%"}},{{rotation:-1.2,duration:1.6,'
            f'ease:"sine.inOut",yoyo:true,repeat:1}},{a + 3.2:.2f});')
        add(f'tl.to(".c{n}-hf",{{keyframes:[{{opacity:1,y:-40,scale:.9,duration:.5,ease:"sine.out"}},'
            f'{{opacity:0,y:-160,scale:1.3,duration:1.6,ease:"sine.in"}}],stagger:.45}},{a + 3.3:.2f});')
        add(f'tl.fromTo(".c{n}-vb",{{x:-60}},{{x:680,duration:5,ease:"none"}},{a + 1.6:.2f});')
        add(f'tl.fromTo(".c{n}-sp",{{scale:0,opacity:0,rotation:0}},{{scale:1.1,opacity:1,rotation:90,duration:.4,'
            f'stagger:.1,ease:"back.out(3)"}},{a + 2.4:.2f});')
        add(f'tl.to(".c{n}-sp",{{scale:0,opacity:0,rotation:180,duration:.5,stagger:.1,ease:"power2.in"}},'
            f'{a + 3.1:.2f});')
        fade_out(f"#sc-c{n} .row, #sc-c{n} .win", b - .45)

    # both couples together
    a, b = S["both"]
    rise(".b-cap", a + .15)
    wipe(".b-s1", a + .45, 1.0)
    wipe(".b-s2", a + 1.35, 1.2)
    add(f'tl.fromTo(".b-win",{{opacity:0,scale:.86,y:40}},{{opacity:1,scale:1,y:0,duration:.9,ease:"power3.out"}},'
        f'{a + 1.6:.2f});')
    for k, dx in ((1, -200), (2, 200)):
        add(f'tl.fromTo(".bp{k}",{{x:{dx},opacity:0}},{{x:0,opacity:1,duration:1.3,ease:"power2.out"}},{a + 2.1:.2f});')
    add(f'tl.fromTo(".b-vb",{{x:-60}},{{x:780,duration:5.5,ease:"none"}},{a + 1.8:.2f});')
    rise(".b-t1", a + 3.4)
    rise(".b-t2", a + 3.7)
    fade_out("#sc-both .row, #sc-both .win", b - .45)

    # date and venue
    a, b = S["date"]
    add(f'tl.fromTo(".d-cap .dc",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,stagger:.04,ease:"back.out(2)"}},'
        f'{a + .1:.2f});')
    draw_div(".d-div", a + .55)
    rise(".d-mon", a + .7)
    pop(".d-num", a + .85, .6, "scale:2.2,opacity:0", "back.out(1.6)")
    add(f'tl.fromTo(".d-day",{{x:-110,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},{a + 1.1:.2f});')
    add(f'tl.fromTo(".d-yr",{{x:110,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},{a + 1.1:.2f});')
    add(f'tl.fromTo(".d-pin",{{y:-240,opacity:0}},{{y:0,opacity:1,duration:.7,ease:"bounce.out"}},{a + 1.6:.2f});')
    rise(".d-ven", a + 2.0)
    rise(".d-a1", a + 2.2)
    rise(".d-a2", a + 2.4)
    rise(".d-a3", a + 2.6)
    draw_div(".d-div2", a + 2.9)
    fade_out("#sc-date .row, #sc-date .daterow", b - .4)

    # closing card
    a, b = S["close"]
    pop(".diya", a + .1, .6)
    add(f'tl.fromTo(".diya .flame",{{scaleY:.9,transformOrigin:"50% 100%"}},{{scaleY:1.12,duration:.25,'
        f'ease:"sine.inOut",yoyo:true,repeat:15}},{a + .2:.2f});')
    rise(".x-1", a + .2)
    wipe(".x-2", a + .45, 1.0)
    rise(".x-3", a + 1.2)
    rise(".x-4", a + 1.4)
    draw_div(".x-div", a + 1.6)
    pop(".x-m1", a + 1.7, .6, "scale:0,opacity:0", "back.out(1.8)")
    pop(".x-m2", a + 1.85, .6, "scale:0,opacity:0", "back.out(1.8)")
    add(f'tl.fromTo(".mini .wr",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.9,'
        f'ease:"power2.inOut"}},{a + 1.8:.2f});')
    pop(".x-heart", a + 2.1, .5, "scale:0,opacity:0", "back.out(3)")
    add(f'tl.to(".x-heart",{{scale:1.15,duration:.36,ease:"sine.inOut",yoyo:true,repeat:3}},{a + 2.6:.2f});')
    rise(".x-date", a + 2.3)
    rise(".x-5", a + 2.5)
    return "\n".join(T)


CSS = """
@font-face { font-family: "Pinyon"; src: url("assets/fonts/pinyon.ttf"); }
@font-face { font-family: "Marcellus"; src: url("assets/fonts/marcellus.ttf"); }
@font-face { font-family: "Playfair"; font-weight: 400 900; src: url("assets/fonts/playfair.ttf"); }
@font-face { font-family: "Playfair"; font-style: italic; font-weight: 400 900; src: url("assets/fonts/playfair-italic.ttf"); }
@font-face { font-family: "Yatra"; src: url("assets/fonts/yatra.ttf"); }
@font-face { font-family: "NotoDeva"; font-weight: 100 900; src: url("assets/fonts/notoserifdeva.ttf"); }
:root { --maroon: #7d1d3f; --rose: #b0365f; --gold: #9c6f24; --ink: #4a2a3a; --teal: #1d5566; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #cfe9f1; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #cfe9f1; }
.clip { position: absolute; inset: 0; }
#bg, #fg { position: absolute; inset: 0; }
#bg { transform-origin: 50% 70%; }
#bg svg, #fg svg { display: block; }
#trees-l, #trees-l2 { transform-origin: 110px 1740px; transform-box: view-box; }
#trees-r { transform-origin: 970px 1740px; transform-box: view-box; }
#bananas { transform-origin: 540px 1600px; transform-box: view-box; }
#pea-l { transform-origin: 215px 1635px; transform-box: view-box; }
#pea-r { transform-origin: 870px 1640px; transform-box: view-box; }
#toran { transform-origin: 540px 0px; transform-box: view-box; }
.flock { position: absolute; left: 0; top: 0; }
#arch { position: absolute; left: 110px; top: 250px; width: 860px; height: 1260px; transform-origin: 50% 60%; }
.scene { z-index: 5; }
.row { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }
.row svg { display: inline-block; vertical-align: top; }
.t { display: inline-block; }
.box { position: absolute; }
.box > svg { display: block; }
.cap { font: 28px "Marcellus"; letter-spacing: 5px; color: var(--gold); }
.cap2 { font: 34px "Marcellus"; letter-spacing: 4px; color: var(--teal); }
.cap3 { font: 54px "Marcellus"; letter-spacing: 14px; color: var(--maroon); }
.cap4 { font: 54px "Marcellus"; letter-spacing: 6px; color: var(--maroon); }
.ital { font: italic 400 40px "Playfair"; color: var(--ink); }
.ital.sm { font-size: 34px; }
.body { font: 400 38px "Playfair"; color: var(--ink); }
.small { font: italic 400 30px "Playfair"; color: var(--gold); }
.addr { font: 500 42px "Playfair"; color: var(--ink); }
.deva { font: 62px "Yatra"; color: #c2410c; }
.shloka { font: 500 34px "NotoDeva"; color: var(--teal); }
.script { font: 72px "Pinyon"; color: var(--rose); line-height: 1.25; }
.script2 { font: 74px "Pinyon"; color: var(--rose); line-height: 1.25; }
.big { font: 132px "Pinyon"; color: var(--rose); line-height: 1.25; }
.name { font: 88px "Pinyon"; color: var(--maroon); line-height: 1.25; }
.amp { font: italic 400 46px "Playfair"; color: var(--gold); }
.wipe { display: inline-block; padding: 0 24px; }
.ch, .ic, .dc { display: inline-block; }
.gwrap { transform-origin: 50% 50%; }
.gwrap svg { width: 420px; height: 525px; }
.rayclip { position: absolute; inset: 0; clip-path: path('M134 1488 L134 588 C134 456 384 382 540 276 C696 382 946 456 946 588 L946 1488 Z'); }
.rays { position: absolute; left: 20px; top: 140px; width: 1040px; height: 1040px; transform-origin: 50% 50%; }
.win { transform-origin: 50% 60%; }
.spark { position: absolute; left: -20px; top: -20px; }
.mini svg { width: 290px; height: 290px; }
.mini-t { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  font: 84px "Pinyon"; color: var(--rose); padding-top: 6px; }
.mini-t i { font: italic 400 40px "Playfair"; color: var(--gold); margin: 0 4px; }
.heart { transform-origin: 50% 50%; }
.daterow { position: absolute; left: 0; width: 1080px; display: flex; align-items: center; justify-content: center; gap: 22px; }
.side { font: 34px "Marcellus"; letter-spacing: 4px; color: var(--teal); border-top: 2px solid #c9973f;
  border-bottom: 2px solid #c9973f; padding: 12px 4px; width: 190px; text-align: center; }
.num { font: 700 200px "Playfair"; color: var(--rose); line-height: 1.05; width: 250px; text-align: center; }
.petal { position: absolute; left: 0; top: 0; z-index: 8; }
#doors { z-index: 20; perspective: 2200px; }
#door-l, #door-r { position: absolute; top: 0; width: 540px; height: 1920px; }
#door-l { left: 0; transform-origin: 0% 50%; } #door-r { left: 540px; transform-origin: 100% 50%; }
#doorframe { position: absolute; inset: 0; transform-origin: 50% 45%; }
.door-medal { position: absolute; left: 430px; top: 320px; width: 220px; height: 220px; border-radius: 50%;
  background: #fbf0dc; border: 6px solid #c9973f; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 10px rgba(201,151,63,.25); }
.door-medal svg { width: 150px; height: 188px; }
"""


def arch_svg():
    return ('<svg viewBox="0 0 860 1260" width="860" height="1260">'
            '<path d="M0 1260 L0 330 C0 190 260 110 430 0 C600 110 860 190 860 330 L860 1260 Z" '
            'fill="#fffaf1" fill-opacity=".95" stroke="#c9973f" stroke-width="5"/>'
            '<path d="M22 1238 L22 338 C22 206 274 132 430 26 C586 132 838 206 838 338 L838 1238 Z" '
            'fill="none" stroke="#c9973f" stroke-width="1.6" opacity=".7"/></svg>')


def main():
    petal_html, petal_tl = petals()
    flocks = "".join(
        f'<div class="flock flock{k}" data-layout-allow-overflow><svg width="200" height="90" viewBox="0 0 200 90">'
        f'<g transform="translate(0 30)">{art.bird("b", 1.0)}</g><g transform="translate(70 0)">{art.bird("b", .8)}</g>'
        f'<g transform="translate(120 50)">{art.bird("b", .7)}</g></svg></div>' for k in range(3))
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
      <div id="bgclip" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0">
        <div id="bg">{art.background()}</div>{flocks}
        <div id="arch">{arch_svg()}</div>
        <div id="fg">{art.foreground()}</div>
      </div>
      {build_scenes()}
      <div id="petals" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-allow-overflow>{petal_html}</div>
      <div id="doors" class="clip" data-start="0" data-duration="{S["doors"][1]}" data-track-index="5">
        <div id="door-l">{art.door_panel("l")}</div><div id="door-r">{art.door_panel("r")}</div>
        <div id="doorframe">{art.door_frame()}</div>
        <div class="door-medal">{fg.ganesh_brush(cls="gm")}</div>
      </div>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="7" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set(".wr, .rg, .dv", {{ strokeDasharray: 1, strokeDashoffset: 1, opacity: 0 }});
      gsap.set(".petal", {{ x: -100, y: -80, opacity: 0 }});
      gsap.set(".hf", {{ opacity: 0, scale: .4, transformOrigin: "50% 50%" }});
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
