"""Builds index.html for the engagement invite (two couples), 1080x1920, 50 s. Version 4: royal maroon & gold.

python3 -I build/generate.py      (run from the project root)

Look: the client's maroon leather card with gold filigree. Motion: kinetic type that slams in out
of a blur, gold-foil shimmer, film grain and light leaks, and a different transition at every cut
(light flare, zoom through the ring, whip pan, diamond shatter, petal burst, iris). Both couples
hold hands and walk through palace spaces. Cuts sit on strong beats of the song.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art  # noqa: E402
import elements as el  # noqa: E402
import figures as fg  # noqa: E402
import romance as ro  # noqa: E402
import royal as ry  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 46.0
CUTS = [7.13, 12.79, 18.44, 23.27, 27.86, 33.45, 39.5]
S = {
    "ganesh": (0.0, CUTS[0]),
    "invite": (CUTS[0], CUTS[1]),
    "c1": (CUTS[1], CUTS[2]),
    "c2": (CUTS[2], CUTS[3]),
    "walk": (CUTS[3], CUTS[4]),
    "both": (CUTS[4], CUTS[5]),
    "date": (CUTS[5], CUTS[6]),
    "close": (CUTS[6], DUR),
}
KIND = {"ganesh": "card", "invite": "card", "c1": "night", "c2": "night", "walk": "night", "both": "walk", "date": "card",
        "close": "card"}
# how far each clip reaches past its cut so the transitions can overlap
PAD_IN = {"invite": 0.0, "c1": 0.6, "c2": 0.0, "walk": 0.7, "both": 0.7, "date": 0.0, "close": 0.0}
PAD_OUT = {"ganesh": 0.0, "invite": 0.15, "c1": 0.0, "c2": 0.0, "both": 0.0, "date": 0.0}
RING = (540, 600)          # centre of the hands medallion: the zoom-through target
PIN = (540, 830)           # the location pin: the iris target


# ------------------------------------------------------------------ markup helpers
def scene(sid, inner):
    a, b = S[sid]
    a0, b0 = max(0.0, a - PAD_IN.get(sid, 0)), min(DUR, b + PAD_OUT.get(sid, 0))
    if KIND[sid] == "card":
        world = ry.card_bg() + ry.card_frame(sid)
    else:
        space = {"c1": ro.rooftop, "c2": ro.pond, "walk": ro.walkway, "both": ry.hall}[sid](sid)
        world = ry.card_bg() + space + ry.card_frame(sid)
    return (f'<div id="sc-{sid}" class="clip scene {KIND[sid]}" data-start="{a0}" data-duration="{round(b0 - a0, 2)}" '
            f'data-track-index="{2 + list(S).index(sid) % 2}" style="z-index:{5 + list(S).index(sid)}">'
            f'<div class="pan">{world}{inner}</div></div>')


def at(y, inner, cls=""):
    return f'<div class="row {cls}" style="top:{y}px"><span class="t">{inner}</span></div>'


def letters(text):
    return "".join(f'<span class="lt">{"&nbsp;" if c == " " else c}</span>' for c in text)


def words(text):
    return " ".join(f'<span class="wd">{w}</span>' for w in text.split())


def box(cls, x, y, w, h, inner):
    return f'<div class="box {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def stage(cls, inner):
    return f'<svg class="stage {cls}" viewBox="0 0 1080 1920" width="1080" height="1920">{inner}</svg>'


def divider(w=420):
    return art.divider(w, col="#e9c46a")


def mandala_ring():
    dots = "".join(f'<circle cx="{270 + 250 * __import__("math").cos(i / 48 * 6.283):.1f}" '
                   f'cy="{270 + 250 * __import__("math").sin(i / 48 * 6.283):.1f}" r="{5 if i % 2 else 3}" fill="#e9c46a"/>'
                   for i in range(48))
    petals = "".join(f'<path d="M270 30 C290 60 290 90 270 110 C250 90 250 60 270 30 Z" fill="none" stroke="#e9c46a" '
                     f'stroke-width="2" transform="rotate({i * 22.5} 270 270)"/>' for i in range(16))
    return (f'<svg viewBox="0 0 540 540" width="540" height="540"><circle cx="270" cy="270" r="262" fill="none" '
            f'stroke="#e9c46a" stroke-width="3"/><circle cx="270" cy="270" r="238" fill="none" stroke="#e9c46a" '
            f'stroke-width="1.5" opacity=".7"/>{dots}{petals}</svg>')


def build_scenes():
    out = []
    out.append(scene("ganesh", (
        box("gring", 270, 330, 540, 540, mandala_ring()) +
        box("gglow", 270, 330, 540, 540, "") +
        box("gwrap", 320, 380, 440, 446, '<img src="assets/img/ganesh.png" width="440" height="446" alt="">') +
        at(915, '<span class="foil-txt">॥ श्री गणेशाय नमः ॥</span>', "deva g-deva") +
        at(1000, '<span class="wipe g-en">Shree Ganeshaya Namah</span>', "script g-en-row") +
        at(1112, divider(), "g-div") +
        at(1160, words("वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ।"), "shloka g-sh1") +
        at(1214, words("निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥"), "shloka g-sh2")
    )))
    out.append(scene("invite", (
        at(318, letters("YOU ARE CORDIALLY INVITED"), "caps i-1") +
        at(368, letters("TO THE ENGAGEMENT OF"), "caps i-2") +
        box("medal i-hands", 390, 450, 300, 300, ry.hands_royal(300)) +
        "".join(f'<div class="spark i-sp" style="transform:translate({x}px,{y}px)">{art.sparkle("#fff1b8")}</div>'
                for x, y in [(540, 560), (590, 590), (495, 605)]) +
        at(782, '<span class="wipe foil-txt i-eng">Two Beautiful Couples</span>', "script i-4") +
        at(930, letters("ENGAGEMENT CEREMONY"), "caps2 i-5") +
        at(1000, divider(), "i-div") +
        at(1046, words("with the divine blessings of"), "ital i-6") +
        at(1100, words("Lord Ganesha & our beloved elders"), "ital i-7")
    )))
    for n, him, her, pose in (
            (1, "Jyoti", "Manish Tamoli",
             f'<g class="pose1"><g transform="translate(540 1450) scale(1.25)">{ro.back_seated(ry.C1)}</g></g>'),
            (2, "Shalu", "Harsh Aswal",
             f'<g class="pose2"><g transform="translate(760 1520) scale(1.05)">{ro.side_seated(ry.C2)}</g></g>')):
        out.append(scene(f"c{n}", (
            stage(f"c{n}-stage", pose) +
            at(286, letters("THE ENGAGEMENT OF"), f"caps c{n}-cap") +
            at(330, f'<span class="wipe c{n}-him">{him}</span>', "name") +
            at(452, "&amp;", f"amp c{n}-amp") +
            at(488, f'<span class="wipe c{n}-her">{her}</span>', "name") +
            at(616, divider(360), f"c{n}-div") +
            "".join(f'<div class="spark c{n}-sp" style="transform:translate({x}px,{y}px)">{art.sparkle("#fff1b8")}</div>'
                    for x, y in [(250, 380), (830, 370), (330, 560), (750, 570), (540, 300)])
        )))
    out.append(scene("walk", (
        stage("wk-stage",
              f'<g class="wk1"><g class="wkm1" transform="translate(478 1292) scale(0.4)">{fg.couple(ry.C1, "k1")}</g></g>'
              f'<g class="wk2"><g class="wkm2" transform="translate(602 1292) scale(0.4)">{fg.couple(ry.C2, "k2")}</g></g>') +
        at(300, letters("HAND IN HAND"), "caps k-cap") +
        at(344, '<span class="wipe foil-txt k-s1">into forever</span>', "script2")
    )))
    out.append(scene("both", (
        stage("b-stage", f'<g class="hug1"><g transform="translate(300 1660) scale(.86)">{ro.embrace(ry.C1)}</g></g>'
              f'<g class="hug2"><g transform="translate(790 1660) scale(.86)">{ro.embrace(ry.C2)}</g></g>'
              + "".join(f'<g class="bh" transform="translate({x} {y})"><path d="M0 18 C-6 13 -10 9 -10 5 C-10 2 -8 0 -5 0 '
                        f'C-3 0 -1 1 0 3 C1 1 3 0 5 0 C8 0 10 2 10 5 C10 9 6 13 0 18 Z" fill="#f43f5e"/></g>'
                        for x, y in [(290, 1240), (310, 1200), (780, 1240), (800, 1200), (300, 1180), (790, 1170)])) +
        at(286, letters("TWICE THE JOY"), "caps b-cap") +
        at(328, '<span class="wipe b-s1">Two love stories,</span>', "script2") +
        at(420, '<span class="wipe foil-txt b-s2">one joyous celebration</span>', "script2") +
        at(552, words("Please join us as they exchange rings"), "ital sm b-t1") +
        at(600, words("and begin a bright new chapter together"), "ital sm b-t2")
    )))
    out.append(scene("date", (
        at(350, letters("SAVE THE DATE"), "caps3 d-cap") +
        at(436, divider(), "d-div") +
        at(492, letters("FRIDAY"), "caps gold d-day") +
        f'<div class="daterow" style="top:540px"><div class="side d-mon">OCT</div><div class="bar d-b1"></div>'
        f'<div class="num d-num">30</div><div class="bar d-b2"></div><div class="side d-yr">2026</div></div>' +
        at(764, letters("SH. RAJENDER KUMAR"), "host d-host") +
        at(818, letters("9312634827  ·  9654569022"), "caps gold d-ph") +
        at(880, art.pin(48).replace(art.ROSE_D, "#ffffff").replace('fill="#fff"', 'fill="#7a1022"'), "d-pin") +
        at(952, letters("VENUE"), "caps gold d-ven") +
        at(1000, letters("DDA MARKET,"), "addr d-a1") +
        at(1048, letters("NEAR 2 PETROL PUMP,"), "addr d-a2") +
        at(1096, letters("INDUSTRIAL AREA PHASE 1,"), "addr d-a3") +
        at(1144, letters("MANGOLPURI, NEW DELHI"), "addr d-a4") +
        at(1192, letters("110083"), "addr d-a5") +
        at(1270, divider(), "d-div2")
    )))
    out.append(scene("close", (
        at(318, letters("AWAITING YOUR"), "caps x-1") +
        at(360, '<span class="wipe foil-txt x-2">gracious presence</span>', "script") +
        box("pav x-pav", 364, 520, 352, 448, el.pavilion().replace("#c9973f", "#e9c46a")) +
        at(790, '<span class="foil-txt">शुभ सगाई</span>', "deva2 x-ss") +
        box("ele x-el1", 140, 800, 250, 161, f'<svg viewBox="-150 -255 420 270" width="250" height="161">'
            f'{ry.elephant_royal()}</svg>') +
        box("ele x-el2", 690, 800, 250, 161, f'<svg viewBox="-270 -255 420 270" width="250" height="161">'
            f'{ry.elephant_royal(True)}</svg>') +
        box("bq x-bq", 340, 860, 400, 175, f'<svg viewBox="-200 -150 400 175" width="400" height="175">'
            f'{ry.bouquet_royal()}</svg>') +
        at(1060, '<span class="wipe x-3">Happily ever after begins</span>', "script3") +
        at(1166, letters("30 · 10 · 2026"), "caps gold x-date") +
        at(1214, words("With love & warm wishes"), "ital x-5")
    )))
    return "".join(out)


# ------------------------------------------------------------------ timeline
T = []


def add(s):
    T.append(s)


def slam(sel, t, per=.03):
    """Letters punch in from big and blurred (the reference's kinetic type)."""
    add(f'tl.fromTo("{sel} .lt",{{opacity:0,scale:2.4,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",'
        f'duration:.42,stagger:{per},ease:"expo.out"}},{t:.2f});')


def wordsin(sel, t, per=.08):
    add(f'tl.fromTo("{sel} .wd",{{opacity:0,y:26,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",'
        f'duration:.5,stagger:{per},ease:"power3.out"}},{t:.2f});')


def wipe(sel, t, d):
    add(f'tl.fromTo("{sel}",{{clipPath:"inset(-30% 100% -40% 0%)"}},{{clipPath:"inset(-30% 0% -40% 0%)",'
        f'duration:{d},ease:"power1.inOut"}},{t:.2f});')


def glint(sel, t, d=1.1):
    add(f'tl.fromTo("{sel}",{{backgroundPosition:"120% 0"}},{{backgroundPosition:"-20% 0",duration:{d},'
        f'ease:"power1.inOut"}},{t:.2f});')


def draw_div(sel, t):
    add(f'tl.fromTo("{sel} .dv",{{strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.6,'
        f'ease:"power2.out"}},{t:.2f});')
    add(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:.25}},{t:.2f});')


def pop(sel, t, d=.55, frm="scale:0,opacity:0", ease="back.out(2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,duration:{d},ease:"{ease}"}},{t:.2f});')


def sparks(sel, t):
    add(f'tl.fromTo("{sel}",{{scale:0,opacity:0,rotation:0}},{{scale:1.1,opacity:1,rotation:90,duration:.35,'
        f'stagger:.08,ease:"back.out(3)"}},{t:.2f});')
    add(f'tl.to("{sel}",{{scale:0,opacity:0,rotation:180,duration:.45,stagger:.08,ease:"power2.in"}},{t + .6:.2f});')


def frame_in(sid, t):
    """Gold filigree draws in from the corners."""
    add(f'tl.fromTo("#sc-{sid} .frame g[class^=fr-]",{{opacity:0,scale:.7,transformOrigin:"50% 50%"}},'
        f'{{opacity:1,scale:1,duration:.7,stagger:.06,ease:"power3.out"}},{t:.2f});')


def walk_cycle(cls, t0, t1, step=.5):
    n = int((t1 - t0) / step)
    add(f'tl.fromTo(".{cls} .lg1",{{rotation:-14}},{{rotation:14,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 0%"}},{t0:.2f});')
    add(f'tl.fromTo(".{cls} .lg2",{{rotation:14}},{{rotation:-14,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 0%"}},{t0:.2f});')
    add(f'tl.fromTo(".{cls} .skirt",{{skewX:-4}},{{skewX:4,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 0%"}},{t0:.2f});')
    add(f'tl.fromTo(".{cls}",{{y:0}},{{y:-9,duration:{step / 2},ease:"sine.inOut",yoyo:true,repeat:{2 * n + 1}}},'
        f'{t0:.2f});')


def timeline():
    # ---- doors: burst open fast with a gold flash
    add('tl.fromTo(".door-medal",{scale:1,opacity:1},{scale:.5,opacity:0,duration:.22,ease:"power2.in"},.08);')
    add('tl.fromTo("#door-l",{rotationY:0},{rotationY:-110,duration:.6,ease:"power3.in"},.1);')
    add('tl.fromTo("#door-r",{rotationY:0},{rotationY:110,duration:.6,ease:"power3.in"},.1);')
    add('tl.fromTo("#doorframe",{scale:1,opacity:1},{scale:1.7,opacity:0,duration:.5,ease:"power3.in"},.3);')
    add('tl.fromTo("#flare",{opacity:0,scale:.3},{opacity:.8,scale:2.2,duration:.3,ease:"power2.out"},.42);')
    add('tl.to("#flare",{opacity:0,scale:3,duration:.45,ease:"power2.in"},.72);')

    # ---- Ganesh ji
    frame_in("ganesh", .6)
    add('tl.fromTo(".gring",{scale:.4,opacity:0,rotation:-90},{scale:1,opacity:1,rotation:0,duration:1.1,'
        'ease:"expo.out"},.65);')
    add(f'tl.fromTo(".gring",{{rotation:0}},{{rotation:35,duration:{CUTS[0] - 1.8:.2f},ease:"none"}},1.8);')
    add('tl.fromTo(".gwrap",{opacity:0,scale:.5,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",'
        'duration:1.0,ease:"expo.out"},.8);')
    add('tl.fromTo(".gglow",{opacity:0,scale:.6},{opacity:1,scale:1.1,duration:1.4,ease:"sine.out"},1.0);')
    add('tl.to(".gwrap",{scale:1.04,duration:2,ease:"sine.inOut",yoyo:true,repeat:1},2.6);')
    add('tl.fromTo(".g-deva",{opacity:0,scale:2,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",'
        'duration:.5,ease:"expo.out"},1.8);')
    glint(".g-deva .foil-txt", 2.4)
    wipe(".g-en", 2.5, 1.0)
    draw_div(".g-div", 3.4)
    wordsin(".g-sh1", 4.0, .1)
    wordsin(".g-sh2", 4.7, .1)
    glint(".g-deva .foil-txt", 5.8)

    # ---- T0 flare + zoom-blur into the invitation
    c = CUTS[0]
    add(f'tl.to("#sc-ganesh .pan",{{scale:1.25,filter:"blur(10px)",duration:.4,ease:"power2.in"}},{c - .4:.2f});')
    add(f'tl.fromTo("#flare",{{opacity:0,scale:.2}},{{opacity:1,scale:3,duration:.35,ease:"power2.in"}},{c - .35:.2f});')
    add(f'tl.to("#flare",{{opacity:0,scale:4,duration:.5,ease:"power2.out"}},{c:.2f});')
    add(f'tl.fromTo("#sc-invite .pan",{{scale:1.2,filter:"blur(10px)"}},{{scale:1,filter:"blur(0px)",duration:.6,'
        f'ease:"power3.out"}},{c:.2f});')

    # ---- invitation
    a = S["invite"][0]
    frame_in("invite", a + .05)
    slam(".i-1", a + .2, .022)
    slam(".i-2", a + .6, .028)
    pop(".i-hands", a + 1.0, .6, "scale:.3,opacity:0,rotation:-30", "back.out(1.6)")
    add(f'tl.fromTo(".i-hands .hm-his",{{x:-90,opacity:0}},{{x:0,opacity:1,duration:.7,ease:"power2.out"}},{a + 1.2:.2f});')
    add(f'tl.fromTo(".i-hands .hm-her",{{x:110,opacity:0}},{{x:0,opacity:1,duration:.7,ease:"power2.out"}},{a + 1.4:.2f});')
    pop(".i-hands .hm-ring", a + 2.0, .4, 'scale:0,opacity:0,transformOrigin:"50% 50%"', "back.out(3)")
    sparks(".i-sp", a + 2.1)
    wipe(".i-eng", a + 2.2, 1.0)
    glint(".i-eng", a + 3.2)
    slam(".i-5", a + 3.0, .025)
    draw_div(".i-div", a + 3.5)
    wordsin(".i-6", a + 3.6, .07)
    wordsin(".i-7", a + 4.0, .07)

    # ---- T1 spin-zoom through the ring onto the starlit rooftop
    c = CUTS[1]
    add(f'tl.to("#sc-invite .pan",{{scale:9,rotation:25,duration:.75,ease:"power3.in",'
        f'transformOrigin:"{RING[0]}px {RING[1]}px"}},{c - .6:.2f});')
    add(f'tl.fromTo("#sc-c1",{{clipPath:"circle(0px at {RING[0]}px {RING[1]}px)"}},'
        f'{{clipPath:"circle(1500px at {RING[0]}px {RING[1]}px)",duration:.85,ease:"power2.in"}},{c - .55:.2f});')
    add(f'tl.fromTo("#sc-c1 .pan",{{scale:1.3,rotation:-8}},{{scale:1,rotation:0,duration:1.2,ease:"power3.out",'
        f'transformOrigin:"{RING[0]}px {RING[1]}px"}},{c - .55:.2f});')

    # ---- the two couples, at night
    for n in (1, 2):
        a, b = S[f"c{n}"]
        slam(f".c{n}-cap", a + .3, .028)
        wipe(f".c{n}-him", a + .65, .8)
        glint(f".c{n}-him", a + 1.6)
        pop(f".c{n}-amp", a + 1.35, .3, "scale:.3,opacity:0", "back.out(3)")
        wipe(f".c{n}-her", a + 1.5, .9)
        draw_div(f".c{n}-div", a + 2.1)
        sparks(f".c{n}-sp", a + 2.2)
        # golden afternoon -> sunset -> night
        a0 = a - PAD_IN.get(f"c{n}", 0)
        add(f'tl.fromTo("#sc-c{n} .sun",{{y:0,opacity:1}},{{y:640,opacity:.2,duration:{a + 2.9 - a0:.2f},ease:"sine.in"}},{a0:.2f});')
        add(f'tl.fromTo("#sc-c{n} .day",{{opacity:1}},{{opacity:0,duration:1.4,ease:"sine.inOut"}},{a + .9:.2f});')
        add(f'tl.fromTo("#sc-c{n} .dusk",{{opacity:1}},{{opacity:0,duration:1.3,ease:"sine.inOut"}},{a + 2.3:.2f});')
        add(f'tl.fromTo("#sc-c{n} .moon",{{opacity:0,y:90}},{{opacity:1,y:0,duration:1.3,ease:"power2.out"}},{a + 2.5:.2f});')
        add(f'tl.fromTo("#sc-c{n} .star",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5,ease:"power2.out",'
            f'stagger:{{each:.02,from:"random"}}}},{a + 2.8:.2f});')
        add(f'tl.to("#sc-c{n} .star",{{opacity:.45,duration:.5,ease:"sine.inOut",yoyo:true,repeat:3,'
            f'stagger:{{each:.04,from:"random"}}}},{a + 4.0:.2f});')
        add(f'tl.fromTo("#sc-c{n} .lglow",{{opacity:.03}},{{opacity:.4,duration:.8,ease:"power2.out"}},{a + 3.0:.2f});')
        add(f'tl.fromTo("#sc-c{n} .world",{{scale:1.08}},{{scale:1,duration:{b - a + .6:.2f},ease:"none"}},{a - .6:.2f});')
    a, b = S["c1"]
    # rooftop: she nestles in, a shooting star crosses
    add(f'tl.fromTo(".pose1",{{y:240,opacity:0}},{{y:0,opacity:1,duration:1.1,ease:"power3.out"}},{a - .2:.2f});')
    add(f'tl.fromTo(".pose1",{{rotation:-.6}},{{rotation:.6,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:3,'
        f'transformOrigin:"50% 100%"}},{a + .9:.2f});')
    add(f'tl.fromTo("#sc-c1 .shoot",{{x:200,y:-80,opacity:0}},{{x:-420,y:200,opacity:1,duration:.8,ease:"power2.in",'
        f'keyframes:{{opacity:[0,1,1,0]}}}},{a + 4.2:.2f});')
    a, b = S["c2"]
    add(f'tl.fromTo(".pose2",{{x:160,opacity:0}},{{x:0,opacity:1,duration:1.0,ease:"power3.out"}},{a:.2f});')
    add(f'tl.fromTo("#sc-c2 .fly",{{x:0,y:0,opacity:0}},{{x:40,y:-60,opacity:1,duration:1.0,ease:"sine.inOut",yoyo:true,'
        f'repeat:1,stagger:{{each:.04,from:"random"}}}},{a + 2.9:.2f});')
    add(f'tl.fromTo("#sc-c2 .ripple",{{x:-20,opacity:.2}},{{x:20,opacity:.6,duration:1.2,ease:"sine.inOut",yoyo:true,'
        f'repeat:3,stagger:.15}},{a:.2f});')
    add(f'tl.fromTo("#sc-c2 .reflect",{{scaleX:.9,opacity:.35}},{{scaleX:1.1,opacity:.6,duration:.9,ease:"sine.inOut",'
        f'yoyo:true,repeat:5,transformOrigin:"50% 50%"}},{a:.2f});')
    add(f'tl.fromTo("#sc-c2 .fdiya",{{y:0}},{{y:-8,duration:.8,ease:"sine.inOut",yoyo:true,repeat:5,stagger:.2}},{a:.2f});')

    # ---- T2 comet sweep: a shooting star streaks across, its bloom covers the cut
    c = CUTS[2]
    add(f'tl.fromTo("#comet",{{x:1200,y:-200,rotation:-30,opacity:0}},{{x:-1700,y:1500,rotation:-30,opacity:1,duration:.75,'
        f'ease:"power2.inOut",keyframes:{{opacity:[0,1,1,0]}}}},{c - .4:.2f});')
    add(f'tl.fromTo("#flare",{{opacity:0,scale:.4}},{{opacity:.85,scale:3.2,duration:.32,ease:"power2.in"}},{c - .3:.2f});')
    add(f'tl.to("#flare",{{opacity:0,scale:4,duration:.45,ease:"power2.out"}},{c + .02:.2f});')
    add(f'tl.to("#sc-c1 .pan",{{x:-140,duration:.4,ease:"power2.in"}},{c - .4:.2f});')
    add(f'tl.fromTo("#sc-c2 .pan",{{x:160}},{{x:0,duration:.6,ease:"power3.out"}},{c:.2f});')

    # ---- T3 dolly dissolve from the pond onto the palace path
    c = CUTS[3]
    add(f'tl.to("#sc-c2 .pan",{{scale:1.12,duration:.8,ease:"power2.in"}},{c - .7:.2f});')
    add(f'tl.fromTo("#sc-walk",{{opacity:0}},{{opacity:1,duration:.8,ease:"sine.inOut"}},{c - .7:.2f});')
    add(f'tl.fromTo("#sc-walk .pan",{{scale:1.12}},{{scale:1,duration:1.2,ease:"power2.out"}},{c - .7:.2f});')

    # ---- both couples walk hand in hand towards the screen, unhurried
    a, b = S["walk"]
    a0 = a - PAD_IN["walk"]
    walk_t = b - a0
    for cls, (x0, x1) in (("wkm1", (478, 318)), ("wkm2", (602, 772))):
        add(f'tl.fromTo(".{cls}",{{attr:{{transform:"translate({x0} 1292) scale(0.4)"}}}},'
            f'{{attr:{{transform:"translate({x1} 1800) scale(0.9)"}},duration:{walk_t:.2f},ease:"sine.inOut"}},{a0:.2f});')
    step = .58
    n = int(walk_t / step)
    add(f'tl.fromTo(".wk1 .lg1, .wk2 .lg2",{{y:0,scaleY:1}},{{y:-12,scaleY:.93,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 0%"}},{a0:.2f});')
    add(f'tl.fromTo(".wk1 .lg2, .wk2 .lg1",{{y:-12,scaleY:.93}},{{y:0,scaleY:1,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 0%"}},{a0:.2f});')
    add(f'tl.fromTo(".k1-g, .k2-g",{{rotation:-1.4}},{{rotation:1.4,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 100%"}},{a0:.2f});')
    add(f'tl.fromTo(".k1-b, .k2-b",{{rotation:1.4}},{{rotation:-1.4,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 100%"}},{a0:.2f});')
    add(f'tl.fromTo(".wk1 .skirt, .wk2 .skirt",{{skewX:-2.5}},{{skewX:2.5,duration:{step},ease:"sine.inOut",yoyo:true,'
        f'repeat:{n},transformOrigin:"50% 0%"}},{a0:.2f});')
    add(f'tl.fromTo("#sc-walk .lglow",{{opacity:.15}},{{opacity:.4,duration:.9,ease:"sine.inOut",yoyo:true,repeat:5,'
        f'stagger:.1}},{a0:.2f});')
    slam(".k-cap", a + .2, .05)
    wipe(".k-s1", a + .6, 1.0)
    glint(".k-s1", a + 1.7)

    # ---- T4 heart reveal into the embrace
    c = CUTS[4]
    add(f'tl.fromTo("#sc-both",{{webkitMaskSize:"0px 0px",maskSize:"0px 0px"}},{{webkitMaskSize:"4400px 3960px",'
        f'maskSize:"4400px 3960px",duration:1.0,ease:"power2.in"}},{c - .7:.2f});')
    add(f'tl.set("#sc-both",{{webkitMaskImage:"none",maskImage:"none"}},{c + .32:.2f});')
    add(f'tl.to("#sc-walk .pan",{{scale:1.1,duration:.7,ease:"power2.in"}},{c - .7:.2f});')

    # ---- both couples embrace in the durbar hall
    a, b = S["both"]
    add(f'tl.fromTo("#sc-both .mid",{{x:0}},{{x:-260,duration:{b - a + .7:.2f},ease:"none"}},{a - .7:.2f});')
    add(f'tl.fromTo(".hug1, .hug2",{{rotation:-1.2}},{{rotation:1.2,duration:1.1,ease:"sine.inOut",yoyo:true,repeat:4,'
        f'transformOrigin:"50% 100%"}},{a - .7:.2f});')
    add(f'tl.fromTo(".bh",{{y:0,opacity:0,scale:.5}},{{y:-260,opacity:0,scale:1.4,duration:2,stagger:.35,ease:"sine.out",'
        f'keyframes:{{opacity:[0,1,1,0]}}}},{a + .6:.2f});')
    add(f'tl.fromTo(".chand",{{rotation:-2}},{{rotation:2,duration:1.5,ease:"sine.inOut",yoyo:true,repeat:3}},{a - .7:.2f});')
    slam(".b-cap", a + .25, .04)
    wipe(".b-s1", a + .55, .8)
    wipe(".b-s2", a + 1.25, .9)
    glint(".b-s2", a + 2.2)
    wordsin(".b-t1", a + 2.1, .06)
    wordsin(".b-t2", a + 2.5, .06)

    # ---- T5 diamond shatter into the save-the-date
    c = CUTS[5]
    add(f'tl.fromTo("#diamond",{{scale:0,opacity:0,rotation:-40}},{{scale:1,opacity:1,rotation:0,duration:.4,'
        f'ease:"back.out(2)"}},{c - .6:.2f});')
    add(f'tl.to("#diamond",{{scale:1.15,duration:.18,ease:"power2.in"}},{c - .2:.2f});')
    add(f'tl.set("#diamond",{{opacity:0}},{c:.2f});')
    add(f'tl.fromTo("#shardset",{{opacity:0}},{{opacity:1,duration:.01}},{c:.2f});')
    add(f'document.querySelectorAll(".shard").forEach(e => tl.fromTo(e,{{x:0,y:0,rotation:0,opacity:1}},'
        f'{{x:+e.dataset.tx,y:+e.dataset.ty,rotation:+e.dataset.r,opacity:0,duration:.9,ease:"power3.out"}},{c:.2f}));')
    add(f'tl.set("#flash",{{opacity:.9}},{c:.2f});')
    add(f'tl.to("#flash",{{opacity:0,duration:.45,ease:"power2.out"}},{c + .01:.2f});')

    # ---- save the date
    a = S["date"][0]
    frame_in("date", a + .05)
    slam(".d-cap", a + .25, .04)
    draw_div(".d-div", a + .65)
    slam(".d-day", a + .7, .05)
    add(f'tl.fromTo(".d-b1, .d-b2",{{scaleY:0}},{{scaleY:1,duration:.4,ease:"power3.out"}},{a + .8:.2f});')
    pop(".d-num", a + .9, .5, "scale:3,opacity:0", "expo.out")
    add(f'tl.fromTo(".d-mon",{{x:-90,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"power3.out"}},{a + 1.05:.2f});')
    add(f'tl.fromTo(".d-yr",{{x:90,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"power3.out"}},{a + 1.05:.2f});')
    slam(".d-host", a + 1.4, .03)
    slam(".d-ph", a + 1.8, .02)
    add(f'tl.fromTo(".d-pin",{{y:-200,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"bounce.out"}},{a + 2.2:.2f});')
    slam(".d-ven", a + 2.5, .05)
    slam(".d-a1", a + 2.7, .025)
    slam(".d-a2", a + 2.9, .018)
    slam(".d-a3", a + 3.15, .018)
    slam(".d-a4", a + 3.4, .018)
    slam(".d-a5", a + 3.65, .04)
    draw_div(".d-div2", a + 3.9)

    # ---- T6 rose-petal burst into the closing card
    c = CUTS[6]
    add(f'document.querySelectorAll(".bp").forEach(e => tl.fromTo(e,{{x:-200,y:+e.dataset.y + 300,rotation:0}},'
        f'{{x:1300,y:+e.dataset.y - 300,rotation:+e.dataset.rot,duration:1.0,ease:"power1.inOut"}},'
        f'{c - .5:.2f} + +e.dataset.d));')
    add(f'tl.fromTo("#sc-close .pan",{{scale:1.15,filter:"blur(8px)"}},{{scale:1,filter:"blur(0px)",duration:.7,'
        f'ease:"power3.out"}},{c:.2f});')

    # ---- closing
    a = S["close"][0]
    frame_in("close", a + .2)
    slam(".x-1", a + .4, .04)
    wipe(".x-2", a + .7, .9)
    glint(".x-2", a + 1.7)
    add(f'tl.fromTo(".x-pav",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:1.0,'
        f'ease:"power2.out"}},{a + .9:.2f});')
    add(f'tl.fromTo(".x-el1",{{x:-280,opacity:0}},{{x:0,opacity:1,duration:1.0,ease:"power2.out"}},{a + 1.1:.2f});')
    add(f'tl.fromTo(".x-el2",{{x:280,opacity:0}},{{x:0,opacity:1,duration:1.0,ease:"power2.out"}},{a + 1.1:.2f});')
    pop(".x-bq", a + 1.7, .55, 'scale:0,opacity:0,transformOrigin:"50% 100%"', "back.out(1.8)")
    add(f'tl.fromTo(".x-ss",{{opacity:0,scale:2,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",'
        f'duration:.5,ease:"expo.out"}},{a + 1.9:.2f});')
    glint(".x-ss .foil-txt", a + 2.5)
    wipe(".x-3", a + 2.3, 1.0)
    slam(".x-date", a + 3.1, .04)
    wordsin(".x-5", a + 3.5)
    glint(".x-2", a + 4.8)

    # ---- always on: grain, light leaks, gold dust, slow push on card scenes
    add(f'tl.fromTo("#grain",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"-2560px 1280px",duration:{DUR},'
        f'ease:"steps(600)"}},0);')
    add(f'tl.fromTo("#leak1",{{x:-300,y:-200,opacity:.35}},{{x:300,y:300,opacity:.6,duration:{DUR / 2},ease:"sine.inOut",'
        f'yoyo:true,repeat:1}},0);')
    add(f'tl.fromTo("#leak2",{{x:250,y:400,opacity:.25}},{{x:-250,y:-100,opacity:.5,duration:{DUR / 3},'
        f'ease:"sine.inOut",yoyo:true,repeat:2}},0);')
    for sid, (a, b) in S.items():
        if KIND[sid] == "card":
            add(f'tl.fromTo("#sc-{sid} .leather",{{scale:1}},{{scale:1.06,duration:{b - a + .5:.2f},ease:"none"}},{a:.2f});')
    return "\n".join(T)


def dust_timeline(specs):
    out = []
    for i, delay, dur, dy, dx in specs:
        t = delay
        while t < DUR:
            out.append(f'tl.fromTo("#gd{i}",{{y:0,x:0,opacity:0}},{{y:{dy:.0f},x:{dx:.0f},opacity:0,duration:{dur:.2f},'
                       f'ease:"sine.inOut",keyframes:{{opacity:[0,1,.8,0]}}}},{t:.2f});')
            t += dur + 1.0
    return "\n".join(out)


CSS = """
@font-face { font-family: "Pinyon"; src: url("assets/fonts/pinyon.ttf"); }
@font-face { font-family: "Cinzel"; font-weight: 400 900; src: url("assets/fonts/cinzel.ttf"); }
@font-face { font-family: "Playfair"; font-style: italic; font-weight: 400 900; src: url("assets/fonts/playfair-italic.ttf"); }
@font-face { font-family: "Yatra"; src: url("assets/fonts/yatra.ttf"); }
@font-face { font-family: "NotoDeva"; font-weight: 100 900; src: url("assets/fonts/notoserifdeva.ttf"); }
:root { --gold: #e9c46a; --cream: #fff4e0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #3f0712; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #3f0712; }
.clip { position: absolute; inset: 0; }
.scene { overflow: hidden; }
.pan { position: absolute; inset: 0; }
.leather { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 50% 50%; }
.world, .frame, .stage { position: absolute; left: 0; top: 0; }
.walk .frame .fr-c3, .walk .frame .fr-c4, .walk .frame .fr-s1, .walk .frame .fr-s2, .walk .frame .band-b,
.night .frame .fr-c3, .night .frame .fr-c4, .night .frame .fr-s1, .night .frame .fr-s2, .night .frame .band-b,
.night .frame .band-t, .night .leather { display: none; }
#sc-both { -webkit-mask-image: url("MASK"); mask-image: url("MASK"); -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
  -webkit-mask-position: 50% 52%; mask-position: 50% 52%; -webkit-mask-size: 0px 0px; mask-size: 0px 0px; }
#comet { position: absolute; left: 0; top: 0; width: 1600px; height: 140px; z-index: 46; opacity: 0;
  transform-origin: 100% 50%; }
.row { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }
.row svg { display: inline-block; vertical-align: top; }
.t, .lt, .wd { display: inline-block; }
.box { position: absolute; }
.box > svg, .box > img { display: block; }
.caps { font: 600 32px "Cinzel"; letter-spacing: 5px; color: #ffffff; }
.caps.gold { color: var(--gold); }
.caps2 { font: 700 34px "Cinzel"; letter-spacing: 7px; color: #ffffff; }
.caps3 { font: 700 56px "Cinzel"; letter-spacing: 8px; color: #ffffff; }
.host { font: 700 40px "Cinzel"; letter-spacing: 4px; color: #ffffff; }
.addr { font: 600 34px "Cinzel"; letter-spacing: 3px; color: #ffffff; }
.ital { font: italic 400 38px "Playfair"; color: var(--cream); }
.ital.sm { font-size: 34px; }
.deva { font: 64px "Yatra"; }
.deva2 { font: 40px "Yatra"; }
.shloka { font: 500 32px "NotoDeva"; color: var(--cream); }
.script { font: 70px "Pinyon"; color: #ffffff; line-height: 1.3; }
.script2 { font: 76px "Pinyon"; color: #ffffff; line-height: 1.3; }
.g-en-row { font-size: 64px; }
.script3 { font: 64px "Pinyon"; color: #ffffff; line-height: 1.3; }
.name { font: italic 600 74px "Playfair"; letter-spacing: .5px; color: #ffffff; line-height: 1.3; text-shadow: 0 4px 18px rgba(0,0,0,.35); }
.amp { font: italic 400 46px "Playfair"; color: var(--gold); }
.foil-txt {
  background: linear-gradient(100deg, #b8862b 0%, #e9c46a 35%, #fff6d5 48%, #fff 50%, #fff6d5 52%, #e9c46a 65%, #b8862b 100%);
  background-size: 300% 100%; background-position: 120% 0; -webkit-background-clip: text; background-clip: text;
  color: transparent; }
.name .wipe { background: linear-gradient(100deg, #fff 40%, #fff6d5 48%, #e9c46a 50%, #fff6d5 52%, #fff 60%);
  background-size: 300% 100%; background-position: 120% 0; -webkit-background-clip: text; background-clip: text; color: transparent; }
.wipe { display: inline-block; padding: 0 24px; }
.gwrap, .gring, .gglow { transform-origin: 50% 50%; }
.gglow { border-radius: 50%; background: radial-gradient(circle, rgba(255,214,120,.55) 0%, rgba(255,214,120,0) 65%); }
.gwrap img { width: 440px; height: 446px; }
.spark { position: absolute; left: -20px; top: -20px; }
.pav svg { width: 100%; height: 100%; }
.daterow { position: absolute; left: 0; width: 1080px; display: flex; align-items: center; justify-content: center; gap: 26px; }
.side { font: 700 46px "Cinzel"; letter-spacing: 3px; color: #ffffff; width: 160px; text-align: center; }
.bar { width: 4px; height: 150px; background: linear-gradient(#b8862b, #fff1b8, #b8862b); transform-origin: 50% 50%; }
.num { font: 700 180px "Cinzel"; color: #ffffff; line-height: 1; width: 240px; text-align: center; }
#flare { position: absolute; left: 140px; top: 560px; width: 800px; height: 800px; border-radius: 50%; z-index: 45;
  background: radial-gradient(circle, #ffffff 0%, #fff1b8 25%, rgba(233,196,106,.6) 50%, rgba(233,196,106,0) 70%); opacity: 0; }
#flash { position: absolute; inset: 0; background: #fff6e0; opacity: 0; z-index: 44; }
#streaks { position: absolute; inset: 0; z-index: 43; opacity: 0; }
#diamond { position: absolute; left: 340px; top: 760px; width: 400px; height: 400px; z-index: 42; opacity: 0; }
#shardset { position: absolute; left: 340px; top: 760px; width: 400px; height: 400px; z-index: 42; opacity: 0; }
.bp { position: absolute; left: 0; top: 0; z-index: 41; }
.gd { position: absolute; border-radius: 50%; background: radial-gradient(circle, #fff6d5, #e9c46a 60%, rgba(233,196,106,0)); z-index: 30; }
#grain { position: absolute; inset: 0; z-index: 50; background-image: url("assets/img/grain.png"); opacity: .09;
  mix-blend-mode: overlay; pointer-events: none; }
.leak { position: absolute; width: 900px; height: 900px; border-radius: 50%; mix-blend-mode: screen; z-index: 31; }
#leak1 { left: -200px; top: 100px; background: radial-gradient(circle, rgba(255,170,80,.35), rgba(255,170,80,0) 65%); }
#leak2 { left: 400px; top: 1000px; background: radial-gradient(circle, rgba(255,90,90,.28), rgba(255,90,90,0) 65%); }
#doors { z-index: 60; perspective: 1600px; }
#door-l, #door-r { position: absolute; top: 0; width: 540px; height: 1920px; }
#door-l { left: 0; transform-origin: 0% 50%; } #door-r { left: 540px; transform-origin: 100% 50%; }
#doorframe { position: absolute; inset: 0; transform-origin: 50% 45%; }
.door-medal { position: absolute; left: 430px; top: 320px; width: 220px; height: 220px; border-radius: 50%;
  background: #4a0912; border: 6px solid #e9c46a; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 10px rgba(233,196,106,.25); }
.door-medal img { display: block; width: 190px; height: 193px; }
"""


def main():
    import random
    rr = random.Random(4)
    streaks = "".join(f'<rect x="{rr.uniform(-200, 900):.0f}" y="{rr.uniform(0, 1920):.0f}" width="{rr.uniform(300, 900):.0f}" '
                      f'height="{rr.uniform(2, 8):.0f}" fill="#fff6d5" opacity="{rr.uniform(.2, .7):.2f}"/>' for _ in range(40))
    dust_html, dust_specs = ry.gold_dust()
    dl, dr, dframe = ry.doors_royal()
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Engagement invite 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS.replace("MASK", ro.heart_mask_svg())}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <svg width="0" height="0" style="position:absolute"><defs>
        <filter id="whip" x="-20%" y="0" width="140%" height="100%"><feGaussianBlur stdDeviation="70 0"/></filter>
        <linearGradient id="dia" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/>
          <stop offset=".4" stop-color="#e6f4ff"/><stop offset=".6" stop-color="#b9dcf2"/><stop offset="1" stop-color="#ffffff"/></linearGradient>
      </defs></svg>
      {build_scenes()}
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8" data-layout-allow-overflow>
        <div id="leak1" class="leak"></div><div id="leak2" class="leak"></div>
        {dust_html}
        <div id="flare"></div><div id="flash"></div>
        <svg id="comet" viewBox="0 0 1600 140" width="1600" height="140"><defs><linearGradient id="cometg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".85" stop-color="#fff1b8" stop-opacity=".7"/><stop offset="1" stop-color="#fff"/></linearGradient><filter id="cblur"><feGaussianBlur stdDeviation="6"/></filter></defs><path d="M0 70 L1540 40 L1540 100 Z" fill="url(#cometg)" filter="url(#cblur)"/><circle cx="1540" cy="70" r="34" fill="#fff" filter="url(#cblur)"/><circle cx="1540" cy="70" r="16" fill="#fff"/></svg>
        <svg id="streaks" viewBox="0 0 1080 1920" width="1080" height="1920">{streaks}</svg>
        <svg id="diamond" viewBox="-200 -200 400 400" width="400" height="400">{ry.diamond_heart()}</svg>
        <svg id="shardset" viewBox="-200 -200 400 400" width="400" height="400" style="overflow:visible">{"".join(ry.shards())}</svg>
        {ry.burst_petals()}
        <div id="grain"></div>
      </div>
      <div id="doors" class="clip" data-start="0" data-duration="1.3" data-track-index="9">
        <div id="door-l">{dl}</div><div id="door-r">{dr}</div>
        <div id="doorframe">{dframe}</div>
        <div class="door-medal"><img src="assets/img/ganesh.png" width="190" height="193" alt=""></div>
      </div>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set(".rg, .dv", {{ strokeDasharray: 1, strokeDashoffset: 1, opacity: 0 }});
      gsap.set(".bp", {{ x: -300, y: -300 }});
      document.querySelectorAll(".lantern, .chand").forEach(e => gsap.set(e, {{ svgOrigin: e.dataset.o }}));
{timeline()}
{dust_timeline(dust_specs)}
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
