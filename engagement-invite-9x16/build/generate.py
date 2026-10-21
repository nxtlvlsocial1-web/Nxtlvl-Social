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
import royal as ry  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 50.0
CUTS = [9.01, 15.74, 22.2, 27.86, 34.6, 41.03]
S = {
    "ganesh": (0.0, CUTS[0]),
    "invite": (CUTS[0], CUTS[1]),
    "c1": (CUTS[1], CUTS[2]),
    "c2": (CUTS[2], CUTS[3]),
    "both": (CUTS[3], CUTS[4]),
    "date": (CUTS[4], CUTS[5]),
    "close": (CUTS[5], DUR),
}
KIND = {"ganesh": "card", "invite": "card", "c1": "walk", "c2": "walk", "both": "walk", "date": "card",
        "close": "card"}
# how far each clip reaches past its cut so the transitions can overlap
PAD_IN = {"invite": 0.0, "c1": 0.6, "c2": 0.25, "both": 0.0, "date": 0.0, "close": 0.3}
PAD_OUT = {"ganesh": 0.0, "invite": 0.0, "c1": 0.15, "c2": 0.0, "both": 0.0, "date": 0.5}
RING = (540, 600)          # centre of the hands medallion: the zoom-through target
PIN = (540, 830)           # the location pin: the iris target


# ------------------------------------------------------------------ markup helpers
def scene(sid, inner):
    a, b = S[sid]
    a0, b0 = max(0.0, a - PAD_IN.get(sid, 0)), min(DUR, b + PAD_OUT.get(sid, 0))
    if KIND[sid] == "card":
        world = ry.card_bg() + ry.card_frame(sid)
    else:
        space = {"c1": ry.corridor, "c2": ry.courtyard, "both": ry.hall}[sid](sid)
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
    for n, him, her, pal in ((1, "Manish Tamboli", "Jyoti", ry.C1), (2, "Harsh Aswal", "Shalu", ry.C2)):
        out.append(scene(f"c{n}", (
            stage(f"c{n}-stage", ry.walkers(pal, f"w{n}", 540, 1655, 1.05)) +
            at(286, letters("THE ENGAGEMENT OF"), f"caps c{n}-cap") +
            at(330, f'<span class="wipe c{n}-him">{him}</span>', "name") +
            at(452, "&amp;", f"amp c{n}-amp") +
            at(488, f'<span class="wipe c{n}-her">{her}</span>', "name") +
            at(616, divider(360), f"c{n}-div") +
            "".join(f'<div class="spark c{n}-sp" style="transform:translate({x}px,{y}px)">{art.sparkle("#fff1b8")}</div>'
                    for x, y in [(250, 380), (830, 370), (330, 560), (750, 570), (540, 300)])
        )))
    out.append(scene("both", (
        stage("b-stage", ry.walkers(ry.C1, "w3", 300, 1655, .82) + ry.walkers(ry.C2, "w4", 780, 1655, .82)) +
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
        at(800, art.pin(56).replace(art.ROSE_D, "#ffffff").replace('fill="#fff"', 'fill="#7a1022"'), "d-pin") +
        at(888, letters("VENUE"), "caps gold d-ven") +
        at(938, letters("NEAR 2 PETROL PUMP,"), "addr d-a1") +
        at(988, letters("INDUSTRIAL AREA PHASE 1,"), "addr d-a2") +
        at(1038, letters("MANGOLPURI, NEW DELHI"), "addr d-a3") +
        at(1088, letters("110083"), "addr d-a4") +
        at(1170, divider(), "d-div2")
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
    add('tl.fromTo(".door-medal",{scale:1,opacity:1},{scale:.5,opacity:0,duration:.25,ease:"power2.in"},.1);')
    add('tl.fromTo("#door-l",{rotationY:0},{rotationY:-110,duration:.7,ease:"power3.in"},.12);')
    add('tl.fromTo("#door-r",{rotationY:0},{rotationY:110,duration:.7,ease:"power3.in"},.12);')
    add('tl.fromTo("#doorframe",{scale:1,opacity:1},{scale:1.7,opacity:0,duration:.6,ease:"power3.in"},.35);')
    add('tl.fromTo("#flare",{opacity:0,scale:.3},{opacity:.9,scale:2.2,duration:.35,ease:"power2.out"},.5);')
    add('tl.to("#flare",{opacity:0,scale:3,duration:.5,ease:"power2.in"},.85);')

    # ---- Ganesh ji
    frame_in("ganesh", .7)
    add('tl.fromTo(".gring",{scale:.4,opacity:0,rotation:-90},{scale:1,opacity:1,rotation:0,duration:1.2,'
        'ease:"expo.out"},.8);')
    add(f'tl.fromTo(".gring",{{rotation:0}},{{rotation:40,duration:{CUTS[0] - 2:.2f},ease:"none"}},2.0);')
    add('tl.fromTo(".gwrap",{opacity:0,scale:.5,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",'
        'duration:1.1,ease:"expo.out"},.95);')
    add('tl.fromTo(".gglow",{opacity:0,scale:.6},{opacity:1,scale:1.1,duration:1.6,ease:"sine.out"},1.2);')
    add('tl.to(".gwrap",{scale:1.04,duration:2.4,ease:"sine.inOut",yoyo:true,repeat:1},3.0);')
    add('tl.fromTo(".g-deva",{opacity:0,scale:2,filter:"blur(12px)"},{opacity:1,scale:1,filter:"blur(0px)",'
        'duration:.5,ease:"expo.out"},2.2);')
    glint(".g-deva .foil-txt", 2.9)
    wipe(".g-en", 3.1, 1.2)
    draw_div(".g-div", 4.2)
    wordsin(".g-sh1", 5.2, .12)
    wordsin(".g-sh2", 6.2, .12)
    glint(".g-deva .foil-txt", 7.4)

    # ---- T0 light flare into the invitation
    add(f'tl.fromTo("#flare",{{opacity:0,scale:.2}},{{opacity:1,scale:3,duration:.3,ease:"power2.in"}},{CUTS[0] - .3:.2f});')
    add(f'tl.to("#flare",{{opacity:0,scale:4,duration:.55,ease:"power2.out"}},{CUTS[0]:.2f});')

    # ---- invitation
    a = S["invite"][0]
    frame_in("invite", a + .05)
    slam(".i-1", a + .25, .025)
    slam(".i-2", a + .8, .03)
    pop(".i-hands", a + 1.3, .7, "scale:.3,opacity:0,rotation:-30", "back.out(1.6)")
    add(f'tl.fromTo(".i-hands .hm-his",{{x:-90,opacity:0}},{{x:0,opacity:1,duration:.8,ease:"power2.out"}},{a + 1.6:.2f});')
    add(f'tl.fromTo(".i-hands .hm-her",{{x:110,opacity:0}},{{x:0,opacity:1,duration:.8,ease:"power2.out"}},{a + 1.85:.2f});')
    pop(".i-hands .hm-ring", a + 2.55, .4, 'scale:0,opacity:0,transformOrigin:"50% 50%"', "back.out(3)")
    sparks(".i-sp", a + 2.7)
    wipe(".i-eng", a + 2.9, 1.2)
    glint(".i-eng", a + 4.0)
    slam(".i-5", a + 3.9, .03)
    draw_div(".i-div", a + 4.5)
    wordsin(".i-6", a + 4.7)
    wordsin(".i-7", a + 5.2)

    # ---- T1 zoom through the ring into the corridor
    c = CUTS[1]
    add(f'tl.to("#sc-invite .pan",{{scale:9,duration:.75,ease:"power3.in",transformOrigin:"{RING[0]}px {RING[1]}px"}},'
        f'{c - .6:.2f});')
    add(f'tl.fromTo("#sc-c1",{{clipPath:"circle(0px at {RING[0]}px {RING[1]}px)"}},'
        f'{{clipPath:"circle(1500px at {RING[0]}px {RING[1]}px)",duration:.85,ease:"power2.in"}},{c - .55:.2f});')

    # ---- couples walking through the palace
    for n, sid in ((1, "c1"), (2, "c2")):
        a, b = S[sid]
        a0, b0 = a - PAD_IN[sid], b + PAD_OUT.get(sid, 0)
        add(f'tl.fromTo("#sc-{sid} .mid",{{x:0}},{{x:-1100,duration:{b0 - a0:.2f},ease:"none"}},{a0:.2f});')
        if sid == "c1":
            add(f'tl.fromTo("#sc-{sid} .fore",{{x:200}},{{x:-2400,duration:{b0 - a0:.2f},ease:"none"}},{a0:.2f});')
        walk_cycle(f"w{n}", a0, b0)
        slam(f".c{n}-cap", a + .35, .03)
        wipe(f".c{n}-him", a + .8, .9)
        glint(f".c{n}-him", a + 1.8)
        pop(f".c{n}-amp", a + 1.6, .35, "scale:.3,opacity:0", "back.out(3)")
        wipe(f".c{n}-her", a + 1.8, .7)
        draw_div(f".c{n}-div", a + 2.5)
        sparks(f".c{n}-sp", a + 2.6)

    # ---- T2 whip pan c1 -> c2
    c = CUTS[2]
    add(f'tl.fromTo("#sc-c1 .pan",{{x:0}},{{x:-1080,duration:.4,ease:"power3.in"}},{c - .25:.2f});')
    add(f'tl.fromTo("#sc-c2 .pan",{{x:1080}},{{x:0,duration:.45,ease:"power3.out"}},{c - .1:.2f});')
    add(f'tl.set("#sc-c1 .pan, #sc-c2 .pan",{{filter:"url(#whip)"}},{c - .2:.2f});')
    add(f'tl.set("#sc-c1 .pan, #sc-c2 .pan",{{filter:"none"}},{c + .35:.2f});')
    add(f'tl.fromTo("#streaks",{{opacity:0,x:600}},{{opacity:.8,x:-600,duration:.45,ease:"none"}},{c - .2:.2f});')
    add(f'tl.set("#streaks",{{opacity:0}},{c + .3:.2f});')
    add(f'tl.fromTo("#sc-c2 .sundisc",{{scale:.8,opacity:.6}},{{scale:1.15,opacity:1,duration:4,ease:"sine.inOut",'
        f'transformOrigin:"50% 50%"}},{c:.2f});')

    # ---- T3 diamond shatter c2 -> both
    c = CUTS[3]
    add(f'tl.fromTo("#diamond",{{scale:0,opacity:0,rotation:-40}},{{scale:1,opacity:1,rotation:0,duration:.45,'
        f'ease:"back.out(2)"}},{c - .7:.2f});')
    add(f'tl.to("#diamond",{{scale:1.15,duration:.2,ease:"power2.in"}},{c - .22:.2f});')
    add(f'tl.set("#diamond",{{opacity:0}},{c:.2f});')
    add(f'tl.fromTo("#shardset",{{opacity:0}},{{opacity:1,duration:.01}},{c:.2f});')
    add(f'document.querySelectorAll(".shard").forEach(e => tl.fromTo(e,{{x:0,y:0,rotation:0,opacity:1}},'
        f'{{x:+e.dataset.tx,y:+e.dataset.ty,rotation:+e.dataset.r,opacity:0,duration:.9,ease:"power3.out"}},{c:.2f}));')
    add(f'tl.set("#flash",{{opacity:.9}},{c:.2f});')
    add(f'tl.to("#flash",{{opacity:0,duration:.45,ease:"power2.out"}},{c + .01:.2f});')

    # ---- both couples walk into the durbar hall
    a, b = S["both"]
    add(f'tl.fromTo("#sc-both .mid",{{x:0}},{{x:-700,duration:{b - a:.2f},ease:"none"}},{a:.2f});')
    walk_cycle("w3", a, b)
    walk_cycle("w4", a + .1, b)
    add(f'tl.fromTo(".chand",{{rotation:-2}},{{rotation:2,duration:1.8,ease:"sine.inOut",yoyo:true,repeat:3}},{a:.2f});')
    slam(".b-cap", a + .4, .04)
    wipe(".b-s1", a + .8, .9)
    wipe(".b-s2", a + 1.6, 1.1)
    glint(".b-s2", a + 2.7)
    wordsin(".b-t1", a + 2.8)
    wordsin(".b-t2", a + 3.3)

    # ---- T4 rose-petal burst both -> date
    c = CUTS[4]
    add(f'document.querySelectorAll(".bp").forEach(e => tl.fromTo(e,{{x:-200,y:+e.dataset.y + 300,rotation:0}},'
        f'{{x:1300,y:+e.dataset.y - 300,rotation:+e.dataset.rot,duration:1.1,ease:"power1.inOut"}},'
        f'{c - .55:.2f} + +e.dataset.d));')

    # ---- save the date
    a = S["date"][0]
    frame_in("date", a + .05)
    slam(".d-cap", a + .3, .045)
    draw_div(".d-div", a + .8)
    slam(".d-day", a + .9, .05)
    add(f'tl.fromTo(".d-b1, .d-b2",{{scaleY:0}},{{scaleY:1,duration:.4,ease:"power3.out"}},{a + 1.0:.2f});')
    pop(".d-num", a + 1.1, .55, "scale:3,opacity:0", "expo.out")
    add(f'tl.fromTo(".d-mon",{{x:-90,opacity:0}},{{x:0,opacity:1,duration:.45,ease:"power3.out"}},{a + 1.3:.2f});')
    add(f'tl.fromTo(".d-yr",{{x:90,opacity:0}},{{x:0,opacity:1,duration:.45,ease:"power3.out"}},{a + 1.3:.2f});')
    add(f'tl.fromTo(".d-pin",{{y:-260,opacity:0}},{{y:0,opacity:1,duration:.7,ease:"bounce.out"}},{a + 1.7:.2f});')
    slam(".d-ven", a + 2.2, .05)
    slam(".d-a1", a + 2.45, .02)
    slam(".d-a2", a + 2.8, .02)
    slam(".d-a3", a + 3.15, .02)
    slam(".d-a4", a + 3.5, .04)
    draw_div(".d-div2", a + 3.8)

    # ---- T5 iris from the pin into the closing card
    c = CUTS[5]
    add(f'tl.fromTo("#sc-close",{{clipPath:"circle(0px at {PIN[0]}px {PIN[1]}px)"}},'
        f'{{clipPath:"circle(1500px at {PIN[0]}px {PIN[1]}px)",duration:.8,ease:"power2.in"}},{c - .3:.2f});')

    # ---- closing
    a = S["close"][0]
    frame_in("close", a + .3)
    slam(".x-1", a + .5, .04)
    wipe(".x-2", a + .9, 1.0)
    glint(".x-2", a + 2.0)
    add(f'tl.fromTo(".x-pav",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:1.1,'
        f'ease:"power2.out"}},{a + 1.1:.2f});')
    add(f'tl.fromTo(".x-el1",{{x:-280,opacity:0}},{{x:0,opacity:1,duration:1.1,ease:"power2.out"}},{a + 1.3:.2f});')
    add(f'tl.fromTo(".x-el2",{{x:280,opacity:0}},{{x:0,opacity:1,duration:1.1,ease:"power2.out"}},{a + 1.3:.2f});')
    pop(".x-bq", a + 2.0, .6, 'scale:0,opacity:0,transformOrigin:"50% 100%"', "back.out(1.8)")
    add(f'tl.fromTo(".x-ss",{{opacity:0,scale:2,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",'
        f'duration:.5,ease:"expo.out"}},{a + 2.2:.2f});')
    glint(".x-ss .foil-txt", a + 2.8)
    wipe(".x-3", a + 2.6, 1.1)
    slam(".x-date", a + 3.5, .04)
    wordsin(".x-5", a + 3.9)
    glint(".x-2", a + 5.5)

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
.walk .frame .fr-c3, .walk .frame .fr-c4, .walk .frame .fr-s1, .walk .frame .fr-s2, .walk .frame .band-b { display: none; }
.row { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }
.row svg { display: inline-block; vertical-align: top; }
.t, .lt, .wd { display: inline-block; }
.box { position: absolute; }
.box > svg, .box > img { display: block; }
.caps { font: 600 32px "Cinzel"; letter-spacing: 5px; color: #ffffff; }
.caps.gold { color: var(--gold); }
.caps2 { font: 700 34px "Cinzel"; letter-spacing: 7px; color: #ffffff; }
.caps3 { font: 700 56px "Cinzel"; letter-spacing: 8px; color: #ffffff; }
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
.name { font: 96px "Pinyon"; color: #ffffff; line-height: 1.3; text-shadow: 0 4px 18px rgba(0,0,0,.35); }
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
    <style>{CSS}</style>
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
