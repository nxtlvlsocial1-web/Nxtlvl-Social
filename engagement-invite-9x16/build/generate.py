"""Builds index.html for the engagement invite (two couples), 1080x1920, 43 s.

python3 -I build/generate.py      (run from the project root)

Scenes follow the music: 84 bpm, one bar = 2.857 s.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAR = 60 / 84 * 4
DUR = 43.0

# scene windows (start, end), on bar lines
S = {
    "doors": (0.0, 3.0),
    "ganesh": (1.9, 3 * BAR),          # -> 8.57
    "invite": (3 * BAR, 5 * BAR),      # -> 14.29
    "c1": (5 * BAR, 7 * BAR),          # -> 20.0
    "c2": (7 * BAR, 9 * BAR),          # -> 25.71
    "both": (9 * BAR, 11 * BAR),       # -> 31.43
    "date": (11 * BAR, 13 * BAR),      # -> 37.14
    "close": (13 * BAR, DUR),
}


def r2(x):
    return round(x, 3)


# ------------------------------------------------------------------ scene markup
def scene(sid, inner):
    a, b = S[sid]
    return (f'<div id="sc-{sid}" class="clip scene" data-start="{r2(a)}" data-duration="{r2(b - a)}" '
            f'data-track-index="3">{inner}</div>')


def at(y, inner, cls="", extra=""):
    """A centred row whose top edge sits at y px."""
    return f'<div class="row {cls}" style="top:{y}px;{extra}">{inner}</div>'


def chars(text, cls="ch"):
    return "".join(f'<span class="{cls}">{"&nbsp;" if c == " " else c}</span>' for c in text)


def couple(n, mono, him, her):
    return scene(f"c{n}", (
        at(410, "THE ENGAGEMENT OF", f"cap c{n}-cap") +
        f'<div class="wreath c{n}-wreath">{art.wreath(10 + n)}</div>' +
        at(595, mono, f"mono c{n}-mono") +
        at(985, f'<span class="wipe c{n}-him">{him}</span>', "name") +
        at(1112, "&amp;", f"amp c{n}-amp") +
        at(1180, f'<span class="wipe c{n}-her">{her}</span>', "name") +
        at(1340, art.divider(), f"c{n}-div") +
        "".join(f'<div class="spark c{n}-sp" style="transform:translate({x}px,{y}px)">{art.sparkle()}</div>'
                for x, y in [(250, 1010), (800, 1000), (330, 1230), (720, 1240), (540, 940), (180, 760), (880, 700)])
    ))


def build_scenes():
    out = []
    # 1. Ganesh ji
    out.append(scene("ganesh", (
        f'<div class="rays">{rays()}</div>'
        f'<div class="gwrap">{art.ganesh()}</div>' +
        at(1000, "॥ श्री गणेशाय नमः ॥", "deva g-deva") +
        at(1090, "Shree Ganeshaya Namah", "script g-en") +
        at(1215, art.divider(), "g-div") +
        at(1265, "वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ।", "shloka g-sh1") +
        at(1325, "निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥", "shloka g-sh2")
    )))
    # 2. the invitation
    out.append(scene("invite", (
        at(400, "With the divine blessings of", "ital i-1") +
        at(462, "LORD GANESHA &amp; OUR ELDERS", "cap2 i-2") +
        at(560, art.rings(190), "i-rings") +
        at(780, "we joyfully invite you to celebrate the", "body i-3") +
        at(870, f'<span class="wipe i-eng">Engagement</span>', "big i-4") +
        at(1070, chars("CEREMONY", "ic"), "cap3 i-5") +
        at(1170, art.divider(), "i-div") +
        at(1230, "of our two beautiful couples", "ital i-6")
    )))
    out.append(couple(1, "M <i>&amp;</i> J", "Manish Tamboli", "Jyoti"))
    out.append(couple(2, "H <i>&amp;</i> S", "Harsh Aswal", "Shalu"))
    # 5. both couples together
    out.append(scene("both", (
        at(415, "TWICE THE JOY", "cap b-cap") +
        f'<div class="mini b-m1">{art.wreath(21, 330)}<div class="mini-t">M <i>&amp;</i> J</div></div>'
        f'<div class="mini b-m2">{art.wreath(22, 330)}<div class="mini-t">H <i>&amp;</i> S</div></div>'
        f'<div class="heart b-heart">{heart()}</div>' +
        at(890, '<span class="wipe b-s1">Two love stories,</span>', "script2") +
        at(1005, '<span class="wipe b-s2">one joyous celebration</span>', "script2") +
        at(1165, "Please join us as they exchange rings", "ital b-t1") +
        at(1225, "and begin a bright new chapter together", "ital b-t2") +
        at(1320, art.divider(), "b-div")
    )))
    # 6. date and venue
    out.append(scene("date", (
        at(380, chars("SAVE THE DATE", "dc"), "cap4 d-cap") +
        at(462, art.divider(), "d-div") +
        at(525, "OCTOBER", "cap2 d-mon") +
        f'<div class="daterow" style="top:585px">'
        f'<div class="side d-day">FRIDAY</div><div class="num d-num">30</div><div class="side d-yr">2026</div></div>' +
        at(875, art.pin(64), "d-pin") +
        at(975, "VENUE", "cap2 d-ven") +
        at(1035, "Near 2 Petrol Pump,", "addr d-a1") +
        at(1103, "Industrial Area Phase 1,", "addr d-a2") +
        at(1171, "Mangolpuri, New Delhi – 110083", "addr d-a3") +
        at(1290, art.divider(), "d-div2")
    )))
    # 7. closing
    out.append(scene("close", (
        f'<div class="diya dy-l">{art.diya()}</div><div class="diya dy-r">{art.diya()}</div>' +
        at(400, "Awaiting your", "ital x-1") +
        at(455, '<span class="wipe x-2">gracious presence</span>', "script2") +
        at(640, "Come, bless the couples as they begin", "body x-3") +
        at(705, "their beautiful journey together", "body x-4") +
        at(800, art.divider(), "x-div") +
        f'<div class="mini x-m1">{art.wreath(31, 280)}<div class="mini-t sm">M <i>&amp;</i> J</div></div>'
        f'<div class="mini x-m2">{art.wreath(32, 280)}<div class="mini-t sm">H <i>&amp;</i> S</div></div>'
        f'<div class="heart x-heart">{heart(70)}</div>' +
        at(1215, "30 · 10 · 2026", "cap2 x-date") +
        at(1275, "With love &amp; warm wishes", "ital x-5")
    )))
    return "".join(out)


def rays():
    n = 24
    import math
    paths = "".join(
        f'<path d="M0 0 L{math.cos(i / n * math.tau - .05) * 520:.0f} {math.sin(i / n * math.tau - .05) * 520:.0f} '
        f'L{math.cos(i / n * math.tau + .05) * 520:.0f} {math.sin(i / n * math.tau + .05) * 520:.0f} Z"/>'
        for i in range(n))
    return (f'<svg viewBox="-520 -520 1040 1040" width="1040" height="1040"><defs><radialGradient id="rayf">'
            f'<stop offset="0" stop-color="#ffd98a" stop-opacity=".75"/><stop offset="1" stop-color="#ffd98a" '
            f'stop-opacity="0"/></radialGradient></defs><g fill="url(#rayf)">{paths}</g></svg>')


def heart(size=90):
    return (f'<svg viewBox="0 0 100 90" width="{size}" height="{size * .9:.0f}"><path d="M50 88 C20 64 0 46 0 26 '
            f'C0 10 12 0 27 0 C38 0 46 6 50 14 C54 6 62 0 73 0 C88 0 100 10 100 26 C100 46 80 64 50 88 Z" '
            f'fill="{art.ROSE}"/></svg>')


# ------------------------------------------------------------------ petals (deterministic)
def petals():
    rnd = random.Random(7)
    shapes = art.petal_shapes()
    els, tweens = [], []
    for i in range(34):
        els.append(f'<div class="petal" id="pt{i}">{shapes[i % len(shapes)]}</div>')
        t = 2.0 + rnd.uniform(0, 7)
        while t < DUR:
            d = rnd.uniform(7.5, 11)
            x0 = rnd.uniform(-20, 1080)
            dx = rnd.uniform(-160, 160)
            s = rnd.uniform(0.6, 1.25)
            rot0, rot1 = rnd.uniform(0, 360), rnd.uniform(200, 700) * rnd.choice((1, -1))
            tweens.append(f'tl.fromTo("#pt{i}",{{x:{x0:.0f},y:-60,rotation:{rot0:.0f},scale:{s:.2f},opacity:.95}},'
                          f'{{x:{x0 + dx:.0f},y:1980,rotation:{rot0 + rot1:.0f},duration:{d:.2f},ease:"none"}},{t:.2f});')
            t += d + rnd.uniform(0, 1.5)
    return "".join(els), "\n".join(tweens)


# ------------------------------------------------------------------ timeline
def timeline():
    T = []
    add = T.append

    # background life (whole video)
    add('tl.fromTo("#bg",{scale:1.0},{scale:1.06,duration:%s,ease:"none"},0);' % DUR)
    add('tl.fromTo("#clouds",{x:-40},{x:60,duration:%s,ease:"none"},0);' % DUR)
    add('tl.fromTo("#sunglow",{opacity:.6},{opacity:1,duration:4,ease:"sine.inOut",yoyo:true,repeat:9},0);')
    for sel, amp, per in [("#trees-l", 1.2, 3.1), ("#trees-r", -1.2, 3.4), ("#bananas", 1.6, 2.6),
                          ("#pea-l", 1.5, 1.9), ("#pea-r", -1.5, 2.1), ("#toran", 0.6, 2.9)]:
        n = int(DUR / per)
        add(f'tl.fromTo("{sel}",{{rotation:{-amp}}},{{rotation:{amp},duration:{per},ease:"sine.inOut",'
            f'yoyo:true,repeat:{n - 1}}},0);')
    # birds: two flocks
    for k, (t0, y0) in enumerate([(4.5, 520), (22.0, 380), (33.5, 600)]):
        add(f'tl.fromTo(".flock{k}",{{x:-160,y:{y0}}},{{x:1240,y:{y0 - 160},duration:7,ease:"none"}},{t0});')

    # --- doors: hold, open, push through
    add('tl.fromTo(".door-medal",{scale:.9,opacity:.85},{scale:1.04,opacity:1,duration:.6,ease:"sine.inOut"},0);')
    add('tl.to(".door-medal",{scale:.6,opacity:0,duration:.45,ease:"power2.in"},.6);')
    add('tl.fromTo("#door-l",{rotationY:0},{rotationY:-104,duration:1.5,ease:"power2.inOut"},.55);')
    add('tl.fromTo("#door-r",{rotationY:0},{rotationY:104,duration:1.5,ease:"power2.inOut"},.55);')
    add('tl.fromTo("#doorframe",{scale:1,opacity:1},{scale:1.5,opacity:0,duration:1.1,ease:"power2.in"},1.55);')
    add('tl.fromTo("#arch",{opacity:0,scale:.92},{opacity:1,scale:1,duration:.9,ease:"power2.out"},1.8);')

    # --- Ganesh ji
    g0 = 1.95
    add(f'tl.fromTo("#sc-ganesh .rays",{{rotation:0}},{{rotation:40,duration:{S["ganesh"][1] - g0:.2f},'
        f'ease:"none"}},{g0});')
    add(f'tl.fromTo("#sc-ganesh .rays",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:1.2,ease:"power2.out"}},'
        f'{g0});')
    add(f'tl.fromTo("#sc-ganesh .gl",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:1.3,stagger:.04,'
        f'ease:"power2.out"}},{g0});')
    add(f'tl.fromTo("#sc-ganesh .gl-dot",{{opacity:0}},{{opacity:1,duration:.3,stagger:.05,'
        f'ease:"power1.out"}},{g0 + 1.6});')
    add(f'tl.fromTo("#sc-ganesh .gwrap",{{scale:.94,filter:"drop-shadow(0 0 0px rgba(255,190,90,0))"}},'
        f'{{scale:1,filter:"drop-shadow(0 0 22px rgba(255,190,90,.9))",duration:1.2,ease:"sine.out"}},{g0 + 2.6});')
    rise(T, ".g-deva", g0 + 2.5)
    rise(T, ".g-en", g0 + 2.9)
    draw_div(T, ".g-div", g0 + 3.3)
    rise(T, ".g-sh1", g0 + 3.6, d=.6)
    rise(T, ".g-sh2", g0 + 4.0, d=.6)
    fade_out(T, "#sc-ganesh .gwrap, #sc-ganesh .row", S["ganesh"][1] - .45)
    add(f'tl.to("#sc-ganesh .rays",{{opacity:0,duration:.4}},{S["ganesh"][1] - .45:.2f});')

    # --- invite
    a = S["invite"][0]
    rise(T, ".i-1", a + .1)
    rise(T, ".i-2", a + .4)
    add(f'tl.fromTo(".i-rings .rg",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.9,stagger:.25,'
        f'ease:"power2.inOut"}},{a + .6:.2f});')
    add(f'tl.fromTo(".i-rings .rg-gem",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.35,'
        f'ease:"back.out(3)"}},{a + 1.5:.2f});')
    rise(T, ".i-3", a + 1.3)
    wipe(T, ".i-eng", a + 1.8, 1.1)
    add(f'tl.fromTo(".i-5 .ic",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.35,stagger:.06,ease:"power2.out"}},'
        f'{a + 2.7:.2f});')
    draw_div(T, ".i-div", a + 3.2)
    rise(T, ".i-6", a + 3.5)
    fade_out(T, "#sc-invite .row", S["invite"][1] - .45)

    # --- the two couples
    for n in (1, 2):
        a = S[f"c{n}"][0]
        rise(T, f".c{n}-cap", a + .1)
        add(f'tl.fromTo(".c{n}-wreath .wr",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:1.2,'
            f'ease:"power2.inOut"}},{a + .2:.2f});')
        add(f'tl.fromTo(".c{n}-wreath .wr-leaf",{{scale:0,opacity:0,transformOrigin:"50% 100%"}},{{scale:1,'
            f'opacity:1,duration:.35,stagger:.03,ease:"back.out(2)"}},{a + .5:.2f});')
        add(f'tl.fromTo(".c{n}-wreath .wr-rose",{{scale:0,transformOrigin:"50% 50%",rotation:-90}},{{scale:1,'
            f'rotation:0,duration:.5,stagger:.08,ease:"back.out(2.2)"}},{a + .9:.2f});')
        add(f'tl.fromTo(".c{n}-mono",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.7,ease:"back.out(1.8)"}},'
            f'{a + 1.1:.2f});')
        wipe(T, f".c{n}-him", a + 1.7, 1.0)
        add(f'tl.fromTo(".c{n}-amp",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.4,ease:"back.out(3)"}},'
            f'{a + 2.6:.2f});')
        wipe(T, f".c{n}-her", a + 2.85, .8)
        draw_div(T, f".c{n}-div", a + 3.5)
        add(f'tl.fromTo(".c{n}-sp",{{scale:0,opacity:0,rotation:0}},{{scale:1.2,opacity:1,rotation:90,duration:.4,'
            f'stagger:.09,ease:"back.out(3)"}},{a + 3.0:.2f});')
        add(f'tl.to(".c{n}-sp",{{scale:0,opacity:0,rotation:180,duration:.5,stagger:.09,ease:"power2.in"}},'
            f'{a + 3.7:.2f});')
        add(f'tl.fromTo(".c{n}-wreath",{{rotation:-4}},{{rotation:4,duration:{S[f"c{n}"][1] - a:.2f},ease:"none"}},'
            f'{a:.2f});')
        fade_out(T, f"#sc-c{n} .row, #sc-c{n} .wreath", S[f"c{n}"][1] - .45)

    # --- both
    a = S["both"][0]
    rise(T, ".b-cap", a + .1)
    add(f'tl.fromTo(".b-m1",{{x:-420,opacity:0}},{{x:0,opacity:1,duration:.9,ease:"power3.out"}},{a + .3:.2f});')
    add(f'tl.fromTo(".b-m2",{{x:420,opacity:0}},{{x:0,opacity:1,duration:.9,ease:"power3.out"}},{a + .3:.2f});')
    add(f'tl.fromTo(".b-heart",{{scale:0}},{{scale:1,duration:.5,ease:"back.out(3)"}},{a + 1.1:.2f});')
    add(f'tl.to(".b-heart",{{scale:1.15,duration:.36,ease:"sine.inOut",yoyo:true,repeat:7}},{a + 1.7:.2f});')
    wipe(T, ".b-s1", a + 1.4, .9)
    wipe(T, ".b-s2", a + 2.2, 1.1)
    rise(T, ".b-t1", a + 3.3)
    rise(T, ".b-t2", a + 3.6)
    draw_div(T, ".b-div", a + 3.9)
    fade_out(T, "#sc-both .row, #sc-both .mini, #sc-both .heart", S["both"][1] - .45)

    # --- date
    a = S["date"][0]
    add(f'tl.fromTo(".d-cap .dc",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,stagger:.04,ease:"back.out(2)"}},'
        f'{a + .1:.2f});')
    draw_div(T, ".d-div", a + .6)
    rise(T, ".d-mon", a + .8)
    add(f'tl.fromTo(".d-num",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:"back.out(1.6)"}},'
        f'{a + 1.0:.2f});')
    add(f'tl.fromTo(".d-day",{{x:-120,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},{a + 1.3:.2f});')
    add(f'tl.fromTo(".d-yr",{{x:120,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},{a + 1.3:.2f});')
    add(f'tl.fromTo(".d-pin",{{y:-260,opacity:0}},{{y:0,opacity:1,duration:.7,ease:"bounce.out"}},{a + 2.0:.2f});')
    rise(T, ".d-ven", a + 2.5)
    rise(T, ".d-a1", a + 2.75)
    rise(T, ".d-a2", a + 2.95)
    rise(T, ".d-a3", a + 3.15)
    draw_div(T, ".d-div2", a + 3.5)
    fade_out(T, "#sc-date .row, #sc-date .daterow", S["date"][1] - .45)

    # --- close
    a = S["close"][0]
    add(f'tl.fromTo(".diya",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:"back.out(2)"}},{a + .1:.2f});')
    add(f'tl.fromTo(".diya .flame",{{scaleY:.9,transformOrigin:"50% 100%"}},{{scaleY:1.12,duration:.25,'
        f'ease:"sine.inOut",yoyo:true,repeat:21}},{a + .2:.2f});')
    rise(T, ".x-1", a + .3)
    wipe(T, ".x-2", a + .6, 1.1)
    rise(T, ".x-3", a + 1.6)
    rise(T, ".x-4", a + 1.85)
    draw_div(T, ".x-div", a + 2.1)
    add(f'tl.fromTo(".x-m1",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:"back.out(1.8)"}},{a + 2.3:.2f});')
    add(f'tl.fromTo(".x-m2",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:"back.out(1.8)"}},{a + 2.5:.2f});')
    add(f'tl.fromTo(".x-heart",{{scale:0}},{{scale:1,duration:.5,ease:"back.out(3)"}},{a + 2.8:.2f});')
    add(f'tl.to(".x-heart",{{scale:1.15,duration:.36,ease:"sine.inOut",yoyo:true,repeat:5}},{a + 3.3:.2f});')
    rise(T, ".x-date", a + 3.1)
    rise(T, ".x-5", a + 3.4)
    return "\n".join(T)


def rise(T, sel, t, d=.55):
    T.append(f'tl.fromTo("{sel}",{{opacity:0,y:34}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{t:.2f});')


def wipe(T, sel, t, d):
    T.append(f'tl.fromTo("{sel}",{{clipPath:"inset(-20% 100% -30% 0%)"}},{{clipPath:"inset(-20% 0% -30% 0%)",'
             f'duration:{d},ease:"power1.inOut"}},{t:.2f});')


def draw_div(T, sel, t):
    T.append(f'tl.fromTo("{sel} .dv",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.7,ease:"power2.out"}},'
             f'{t:.2f});')
    T.append(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:.3}},{t:.2f});')


def fade_out(T, sel, t):
    T.append(f'tl.to("{sel}",{{opacity:0,y:-26,duration:.4,ease:"power2.in"}},{t:.2f});')


CSS = """
@font-face { font-family: "Great Vibes"; src: url("assets/fonts/greatvibes.ttf"); }
@font-face { font-family: "Cinzel"; font-weight: 400 900; src: url("assets/fonts/cinzel.ttf"); }
@font-face { font-family: "Cormorant"; font-weight: 300 700; src: url("assets/fonts/cormorant.ttf"); }
@font-face { font-family: "Cormorant"; font-style: italic; font-weight: 300 700; src: url("assets/fonts/cormorant-italic.ttf"); }
@font-face { font-family: "Tiro Deva"; src: url("assets/fonts/tiro.ttf"); }
:root { --maroon: #7d1d3f; --rose: #b83a64; --gold: #a8782c; --ink: #4a2a3a; --teal: #1f5a6a; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #cfe9f1; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #cfe9f1; }
.clip { position: absolute; inset: 0; }
#bg { position: absolute; inset: 0; transform-origin: 50% 70%; }
#bg svg, #fg svg { display: block; }
#fg { position: absolute; inset: 0; }
#trees-l, #trees-l2 { transform-origin: 110px 1740px; transform-box: view-box; }
#trees-r { transform-origin: 970px 1740px; transform-box: view-box; }
#bananas { transform-origin: 540px 1600px; transform-box: view-box; }
#pea-l { transform-origin: 215px 1635px; transform-box: view-box; }
#pea-r { transform-origin: 870px 1640px; transform-box: view-box; }
#toran { transform-origin: 540px 0px; transform-box: view-box; }
.flock { position: absolute; left: 0; top: 0; }
.flock g { display: inline-block; }
#arch { position: absolute; left: 110px; top: 250px; width: 860px; height: 1260px; transform-origin: 50% 60%; }
.scene { z-index: 5; }
.row { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }
.row svg { display: inline-block; }
.cap { font: 600 30px "Cinzel"; letter-spacing: 5px; color: var(--gold); }
.cap2 { font: 600 40px "Cinzel"; letter-spacing: 6px; color: var(--teal); }
.cap3 { font: 700 60px "Cinzel"; letter-spacing: 16px; color: var(--maroon); }
.cap4 { font: 700 62px "Cinzel"; letter-spacing: 8px; color: var(--maroon); }
.ital { font: italic 500 48px "Cormorant"; color: var(--ink); }
.body { font: 500 50px "Cormorant"; color: var(--ink); }
.addr { font: 600 52px "Cormorant"; color: var(--ink); }
.deva { font: 64px "Tiro Deva"; color: var(--maroon); }
.shloka { font: 38px "Tiro Deva"; color: var(--teal); }
.script { font: 76px "Great Vibes"; color: var(--rose); }
.script2 { font: 92px "Great Vibes"; color: var(--rose); line-height: 1.2; }
.big { font: 170px "Great Vibes"; color: var(--rose); line-height: 1.1; }
.name { font: 118px "Great Vibes"; color: var(--maroon); line-height: 1.15; }
.amp { font: 600 64px "Cormorant"; font-style: italic; color: var(--gold); }
.mono { font: 168px "Great Vibes"; color: var(--rose); line-height: 1.2; }
.mono i, .mini-t i { font-style: normal; color: var(--gold); font-size: .6em; }
.wipe { display: inline-block; padding: 0 30px; }
.ch, .ic, .dc { display: inline-block; }
.gwrap { position: absolute; left: 270px; top: 395px; width: 540px; height: 594px; transform-origin: 50% 50%; }
.gwrap svg { width: 540px; height: 594px; }
.rays { position: absolute; left: 20px; top: 170px; width: 1040px; height: 1040px; transform-origin: 50% 50%; }
.wreath { position: absolute; left: 290px; top: 440px; width: 520px; height: 520px; transform-origin: 50% 50%; }
.spark { position: absolute; left: -20px; top: -20px; }
.mini { position: absolute; width: 300px; height: 300px; top: 490px; }
.mini svg { width: 300px; height: 300px; }
.b-m1 { left: 165px; } .b-m2 { left: 615px; }
.mini-t { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  font: 110px "Great Vibes"; color: var(--rose); }
.mini-t.sm { font-size: 92px; }
.x-m1, .x-m2 { width: 280px; height: 280px; top: 880px; }
.x-m1 svg, .x-m2 svg { width: 280px; height: 280px; }
.x-m1 { left: 170px; } .x-m2 { left: 630px; }
.heart { position: absolute; left: 495px; top: 600px; width: 90px; height: 81px; transform-origin: 50% 50%; }
.x-heart { left: 505px; top: 985px; width: 70px; height: 63px; }
.daterow { position: absolute; left: 0; width: 1080px; display: flex; align-items: center; justify-content: center; gap: 24px; }
.side { font: 700 40px "Cinzel"; letter-spacing: 3px; color: var(--teal); border-top: 3px solid var(--gold);
  border-bottom: 3px solid var(--gold); padding: 12px 6px; width: 210px; text-align: center; }
.num { font: 700 230px "Cinzel"; color: var(--rose); line-height: 1; width: 280px; text-align: center; }
.diya { position: absolute; top: 440px; }
.dy-l { left: 150px; } .dy-r { left: 820px; }
.petal { position: absolute; left: 0; top: 0; z-index: 8; }
#doors { z-index: 20; perspective: 2200px; }
#door-l, #door-r { position: absolute; top: 0; width: 540px; height: 1920px; }
#door-l { left: 0; transform-origin: 0% 50%; } #door-r { left: 540px; transform-origin: 100% 50%; }
#doorframe { position: absolute; inset: 0; transform-origin: 50% 45%; }
.door-medal { position: absolute; left: 430px; top: 330px; width: 220px; height: 220px; border-radius: 50%;
  background: #fbf0dc; border: 6px solid #c9973f; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 10px rgba(201,151,63,.25); }
.door-medal svg { width: 170px; height: 187px; }
.door-title { position: absolute; left: 0; width: 1080px; top: 600px; text-align: center; font: 66px "Tiro Deva"; color: #7d1d3f; }
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
        f'<div class="flock flock{k}" data-layout-allow-overflow>'
        f'<svg width="200" height="90" viewBox="0 0 200 90">'
        f'<g transform="translate(0 30)">{art.bird("b", 1.0)}</g><g transform="translate(70 0)">{art.bird("b", .8)}</g>'
        f'<g transform="translate(120 50)">{art.bird("b", .7)}</g></svg></div>' for k in range(3))
    medal = art.ganesh(stroke="#c0661c", width=6, cls="gm")
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
      <div id="doors" class="clip" data-start="0" data-duration="3.0" data-track-index="5">
        <div id="door-l">{art.door_panel("l")}</div><div id="door-r">{art.door_panel("r")}</div>
        <div id="doorframe">{art.door_frame()}</div>
        <div class="door-medal">{medal}</div>
      </div>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="7" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set(".gl, .wr, .rg, .dv", {{ strokeDasharray: 1, strokeDashoffset: 1, opacity: 0 }});
      gsap.set(".petal", {{ x: -100, y: -80, opacity: 0 }});
      gsap.set(".gl-dot", {{ opacity: 0 }});
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
