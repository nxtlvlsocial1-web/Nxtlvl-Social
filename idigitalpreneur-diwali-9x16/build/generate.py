"""Idigitalpreneur x Impact Icon: Diwali leads price-drop ad. 1080x1920, 30 s, 128 bpm.

python3 -I build/generate.py      (run from the project root)

Style after the client's reference: glowing sparkle intro, single punchy words on the beat, RGB-glitch
logo, star wipe, pill highlights, rolling price counter, tilted card grid, sparkle end card.
Recoloured to the brands' blues. Every cut sits on a beat (one beat = 0.469 s, one bar = 1.875 s).
"""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 128
BEAT = 60 / BPM
BAR = BEAT * 4
DUR = 30.0


def b(n):
    """Time of beat n."""
    return round(n * BEAT, 3)


# scene windows, in beats
SC = [
    ("intro", 0, 4), ("words", 4, 8), ("logo", 8, 12), ("offer", 12, 16), ("drop", 16, 22),
    ("mix", 22, 28), ("fem", 28, 34), ("board", 34, 40), ("grid", 40, 46), ("dates", 46, 52),
    ("miss", 52, 58), ("end", 58, 64),
]
S = {k: (b(a), b(z) if z < 64 else DUR) for k, a, z in SC}


def clip(sid, inner, track=2):
    a, z = S[sid]
    return (f'<div id="sc-{sid}" class="clip scene" data-start="{a}" data-duration="{round(z - a, 3)}" '
            f'data-track-index="{track + list(S).index(sid) % 2}">{inner}</div>')


def row(y, inner, cls=""):
    return f'<div class="row {cls}" style="top:{y}px"><span class="t">{inner}</span></div>'


def letters(text):
    return "".join(f'<span class="lt">{"&nbsp;" if c == " " else c}</span>' for c in text)


def sparkle_svg(size, col="#7cc8ff"):
    return (f'<svg viewBox="-50 -50 100 100" width="{size}" height="{size}"><path d="M0 -50 C6 -10 10 -6 50 0 '
            f'C10 6 6 10 0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z" fill="{col}"/></svg>')


def rays(n=36):
    r = random.Random(3)
    return "".join(
        f'<line x1="{math.cos(a) * 140:.0f}" y1="{math.sin(a) * 140:.0f}" x2="{math.cos(a) * L:.0f}" '
        f'y2="{math.sin(a) * L:.0f}" stroke="#9fd8ff" stroke-width="{r.uniform(1, 2.5):.1f}" opacity="{r.uniform(.2, .6):.2f}"/>'
        for a, L in ((i / n * math.tau, r.uniform(600, 1100)) for i in range(n)))


def chevrons():
    return ('<svg viewBox="0 0 80 60" width="80" height="60"><path class="chev c1" d="M8 6 L32 30 L8 54" stroke="#38bdf8" '
            'stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path class="chev c2" '
            'd="M40 6 L64 30 L40 54" stroke="#38bdf8" stroke-width="10" fill="none" stroke-linecap="round" '
            'stroke-linejoin="round"/></svg>')


def price_scene(sid, label, old, new):
    return clip(sid, (
        row(330, letters(label.upper()), f"kicker {sid}-k") +
        f'<div class="card old {sid}-old"><div class="ptag">OLD PRICE</div><div class="pnum">₹{old}</div>'
        f'<svg class="xmark" viewBox="0 0 300 160" width="300" height="160"><path class="x1" d="M20 20 L280 140" '
        f'pathLength="1"/><path class="x2" d="M280 20 L20 140" pathLength="1"/></svg></div>'
        f'<div class="chevwrap {sid}-chev">{chevrons()}</div>'
        f'<div class="card new {sid}-new"><div class="ptag">DIWALI PRICE</div>'
        f'<div class="pnum"><span class="rs">₹</span><span class="count {sid}-count">{old}</span></div>'
        f'<div class="plabel">{label}</div></div>'
        f'<div class="save {sid}-save">SAVE ₹{old - new} PER LEAD</div>'
    ))


def grid_cards():
    r = random.Random(5)
    labels = ["Mix Lead's", "Female Lead's", "₹15", "₹18", "Price Drop", "Diwali Offer", "20–25 Oct", "Leads"]
    out = []
    for i in range(48):
        lab = labels[i % len(labels)]
        hot = i % 5 == 0
        out.append(f'<div class="gc{" hot" if hot else ""}"><div class="gi">{sparkle_svg(26, "#ffffff" if hot else "#38bdf8")}</div>'
                   f'<div class="gl">{lab}</div><div class="gbar" style="width:{r.randint(40, 90)}%"></div></div>')
    return "".join(out)


def build():
    words = ["DIWALI.", "SPECIAL.", "OFFER.", "IS LIVE."]
    scenes = [
        clip("intro", (
            f'<svg class="rays" viewBox="-1100 -1100 2200 2200" width="2200" height="2200">{rays()}</svg>'
            f'<div class="ring"></div><div class="spark">{sparkle_svg(220)}</div>'
        )),
        clip("words", f'<div class="wordstage">{"".join(f"<div class=\'word w{i}\'>{w}</div>" for i, w in enumerate(words))}</div>'),
        clip("logo", (
            '<div class="glitch g-main"><img src="assets/img/logo-idp.png" alt=""></div>'
            '<div class="glitch g-r"><img src="assets/img/logo-idp.png" alt=""></div>'
            '<div class="glitch g-c"><img src="assets/img/logo-idp.png" alt=""></div>'
            '<div class="slice s1"></div><div class="slice s2"></div><div class="slice s3"></div>'
            + row(1040, letters("THE DIGITAL UNIVERSITY"), "tag l-tag") +
            row(1120, "×", "times l-x") +
            '<div class="impact l-imp"><img src="assets/img/logo-impact.png" alt=""></div>'
            f'<div class="lspark">{sparkle_svg(90)}</div>'
        )),
        clip("offer", (
            row(560, "Diwali", "hero o-hero") +
            '<div class="pill o-pill"><span>Special Offer</span></div>' +
            "".join(f'<div class="ospark os{i}">{sparkle_svg(s, c)}</div>' for i, (s, c) in
                    enumerate([(70, "#ffd166"), (46, "#7cc8ff"), (56, "#ffd166"), (40, "#ffffff")]))
        )),
        clip("drop", (
            row(520, '<span class="wht">Lead\'s</span>', "big d-1") +
            row(680, '<span class="cyan">Price Drop</span>', "big d-2") +
            '<svg class="arrow" viewBox="0 0 400 520" width="400" height="520"><path class="ar" pathLength="1" '
            'd="M60 40 C260 40 340 160 320 420" fill="none" stroke="url(#ag)" stroke-width="34" stroke-linecap="round"/>'
            '<path class="ah" d="M250 380 L320 480 L390 380 Z" fill="#38bdf8"/><defs><linearGradient id="ag" x1="0" y1="0" '
            'x2="0" y2="1"><stop offset="0" stop-color="#1d4ed8"/><stop offset="1" stop-color="#38bdf8"/></linearGradient>'
            '</defs></svg>'
            '<svg class="chart" viewBox="0 0 800 300" width="800" height="300"><path class="cl" pathLength="1" '
            'd="M0 40 L140 70 L240 50 L360 130 L470 110 L590 210 L800 270" fill="none" stroke="#38bdf8" stroke-width="10" '
            'stroke-linejoin="round"/></svg>'
        )),
        price_scene("mix", "Mix Lead's", 18, 15),
        price_scene("fem", "Female Lead's", 22, 18),
        clip("board", (
            row(300, letters("NEW DIWALI PRICES"), "kicker bd-k") +
            '<div class="board bd-b"><div class="brow r1"><span class="bo">₹18</span><span class="bn">₹15</span>'
            '<span class="bl">Mix Lead\'s</span></div><div class="brow r2"><span class="bo">₹22</span><span class="bn">₹18</span>'
            '<span class="bl">Female Lead\'s</span></div></div>'
        )),
        clip("grid", (
            f'<div class="plane"><div class="gridin" data-layout-allow-overlap>{grid_cards()}</div></div>'
            '<div class="fade"></div>'
            + row(760, "More leads.", "mid g-1") + row(880, '<span class="cyan">Lower prices.</span>', "mid g-2")
        )),
        clip("dates", (
            row(400, letters("OFFER STARTS"), "kicker dt-k") +
            '<div class="date dt-a"><div class="dm">OCT</div><div class="dd">20</div><div class="dy">2026</div></div>'
            '<div class="dash dt-dash"></div>'
            '<div class="date dt-b"><div class="dm">OCT</div><div class="dd">25</div><div class="dy">2026</div></div>'
            + row(1170, 'Start from <span class="cyan">20 Oct</span> to <span class="cyan">25 Oct 2026</span>', "small dt-s")
        )),
        clip("miss", (
            row(560, "Don't miss", "big2 m-1") +
            '<div class="glx m-2"><span class="gx gx-m">this exclusive</span><span class="gx gx-r">this exclusive</span>'
            '<span class="gx gx-c">this exclusive</span></div>' +
            row(940, '<span class="cyan">offer.</span>', "big2 m-3")
        )),
        clip("end", (
            f'<div class="espark">{sparkle_svg(120)}</div>'
            '<div class="elogo e-l"><img src="assets/img/logo-idp.png" alt=""></div>'
            + row(840, letters("THE DIGITAL UNIVERSITY"), "tag e-tag") +
            row(910, "×", "times e-x") +
            '<div class="impact e-imp"><img src="assets/img/logo-impact.png" alt=""></div>'
            '<div class="cta e-cta">Grab the Diwali offer →</div>'
            + row(1360, "Valid 20 – 25 Oct 2026", "small e-valid")
        )),
    ]
    return "".join(scenes)


# ------------------------------------------------------------------ timeline
T = []


def add(s):
    T.append(s)


def slam(sel, t, per=.025):
    add(f'tl.fromTo("{sel} .lt",{{opacity:0,y:30,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.35,'
        f'stagger:{per},ease:"expo.out"}},{t:.3f});')


def punch(sel, t, frm="scale:1.6,opacity:0,filter:\"blur(14px)\"", d=.32):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{x:0,y:0,scale:1,opacity:1,filter:"blur(0px)",duration:{d},ease:"expo.out"}},{t:.3f});')


def flash(t, o=.85):
    add(f'tl.set("#flash",{{opacity:{o}}},{t:.3f});')
    add(f'tl.to("#flash",{{opacity:0,duration:.22,ease:"power2.out"}},{t + .01:.3f});')


def timeline():
    # intro: sparkle grows out of black, ring pulses, rays spin
    add(f'tl.fromTo(".spark",{{scale:0,rotation:-90,opacity:0}},{{scale:1,rotation:0,opacity:1,duration:1.1,ease:"expo.out"}},.1);')
    add(f'tl.fromTo(".ring",{{scale:.3,opacity:0}},{{scale:1.3,opacity:.9,duration:1.2,ease:"power2.out"}},.2);')
    add(f'tl.fromTo(".rays",{{scale:.4,opacity:0,rotation:0}},{{scale:1,opacity:1,rotation:30,duration:1.8,ease:"power2.out"}},.1);')
    add(f'tl.to(".spark",{{scale:6,opacity:0,duration:.35,ease:"power3.in"}},{b(4) - .35:.3f});')
    flash(b(4))

    # words on the beat
    for i in range(4):
        t = b(4 + i)
        add(f'tl.set("#sc-words .word",{{opacity:0}},{t:.3f});')
        punch(f"#sc-words .w{i}", t, "scale:1.8,opacity:0,filter:\"blur(16px)\"", .28)
        add(f'tl.to("#sc-words .w{i}",{{scale:.94,duration:{BEAT - .28:.3f},ease:"none"}},{t + .28:.3f});')
    add(f'tl.set("#bgwhite",{{opacity:1}},{b(6):.3f});')
    add(f'tl.set("#bgwhite",{{opacity:0}},{b(7):.3f});')

    # logo glitch reveal
    a = S["logo"][0]
    add(f'tl.fromTo(".g-main",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:.3,ease:"expo.out"}},{a:.3f});')
    for k, (sel, dx) in enumerate(((".g-r", -18), (".g-c", 18))):
        add(f'tl.fromTo("{sel}",{{x:{dx * 2},opacity:.9}},{{x:0,opacity:0,duration:.6,ease:"steps(6)"}},{a:.3f});')
        add(f'tl.fromTo("{sel}",{{x:{dx}}},{{x:0,opacity:0,duration:.25,ease:"steps(3)",immediateRender:false,'
            f'keyframes:{{opacity:[.9,0,.8,0]}}}},{a + 1.3:.3f});')
    add(f'tl.fromTo(".slice",{{x:-200,opacity:0}},{{x:200,opacity:.9,duration:.4,stagger:.06,ease:"steps(4)",'
        f'keyframes:{{opacity:[0,.9,.9,0]}}}},{a:.3f});')
    slam(".l-tag", a + .5)
    punch(".l-x", a + .9, "scale:0,opacity:0,rotation:-90")
    add(f'tl.fromTo(".l-imp",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"expo.out"}},{a + 1.05:.3f});')
    add(f'tl.fromTo(".lspark",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:.5,ease:"back.out(3)"}},{a + .3:.3f});')
    add(f'tl.to(".lspark",{{rotation:90,duration:1.2,ease:"none"}},{a + .8:.3f});')

    # star wipe into "Diwali Special Offer"
    a = S["offer"][0]
    add(f'tl.fromTo("#starfill",{{scale:0,rotation:-45}},{{scale:9,rotation:0,duration:.35,ease:"power3.in",'
        f'svgOrigin:"540 960"}},{a - .35:.3f});')
    add(f'tl.set("#starwipe",{{opacity:1}},{a - .35:.3f});')
    add(f'tl.set("#starfill",{{opacity:0}},{a:.3f});')
    add(f'tl.fromTo("#starhole",{{scale:0,rotation:0}},{{scale:14,rotation:45,duration:.55,ease:"power3.in",'
        f'svgOrigin:"540 960"}},{a:.3f});')
    add(f'tl.set("#starwipe",{{opacity:0}},{a + .56:.3f});')
    punch(".o-hero", a + .25, "scale:2.2,opacity:0,filter:\"blur(18px)\"", .4)
    add(f'tl.fromTo(".o-pill",{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:.45,ease:"expo.out"}},{a + .7:.3f});')
    add(f'tl.fromTo(".o-pill span",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"power2.out"}},{a + .95:.3f});')
    add(f'tl.fromTo(".ospark",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:.45,stagger:.12,ease:"back.out(3)"}},{a + .9:.3f});')
    add(f'tl.to(".ospark",{{rotation:90,duration:1.2,stagger:.12,ease:"none"}},{a + 1.4:.3f});')
    add(f'tl.to(".o-hero, .o-pill",{{scale:1.06,duration:{BAR - 1.1:.3f},ease:"none"}},{a + 1.1:.3f});')

    # lead's price drop
    a = S["drop"][0]
    flash(a, .6)
    punch(".d-1", a + .05, "x:-300,opacity:0,filter:\"blur(14px)\"", .4)
    punch(".d-2", a + .35, "x:300,opacity:0,filter:\"blur(14px)\"", .4)
    add(f'tl.fromTo(".ar",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.6,ease:"power2.in"}},{a + .7:.3f});')
    add(f'tl.fromTo(".ah",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.25,ease:"back.out(3)"}},{a + 1.25:.3f});')
    add(f'tl.fromTo(".arrow",{{y:0}},{{y:24,duration:{BEAT:.3f},ease:"sine.inOut",yoyo:true,repeat:3}},{a + 1.5:.3f});')
    add(f'tl.fromTo(".cl",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.0,ease:"power2.inOut"}},{a + 1.0:.3f});')

    # the two price cards
    for sid, old, new in (("mix", 18, 15), ("fem", 22, 18)):
        a = S[sid][0]
        flash(a, .5)
        slam(f".{sid}-k", a + .05)
        punch(f".{sid}-old", a + .2, "y:80,opacity:0,filter:\"blur(10px)\"", .4)
        add(f'tl.fromTo(".{sid}-old .x1",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.22,ease:"power2.in"}},{a + .75:.3f});')
        add(f'tl.fromTo(".{sid}-old .x2",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.22,ease:"power2.in"}},{a + .95:.3f});')
        add(f'tl.to(".{sid}-old",{{opacity:.55,scale:.92,duration:.3}},{a + 1.2:.3f});')
        add(f'tl.fromTo(".{sid}-chev .chev",{{opacity:.2,x:-20}},{{opacity:1,x:0,duration:.25,stagger:.1,yoyo:true,repeat:3,'
            f'ease:"power2.out"}},{a + 1.2:.3f});')
        punch(f".{sid}-new", a + 1.4, "scale:.4,opacity:0,filter:\"blur(14px)\"", .4)
        add(f'(()=>{{const o={{v:{old}}};tl.to(o,{{v:{new},duration:.7,ease:"power2.out",onUpdate:()=>{{'
            f'document.querySelector(".{sid}-count").textContent=Math.round(o.v);}}}},{a + 1.55:.3f});}})();')
        add(f'tl.fromTo(".{sid}-count",{{filter:"blur(6px)"}},{{filter:"blur(0px)",duration:.7,ease:"power2.out"}},{a + 1.55:.3f});')
        add(f'tl.fromTo(".{sid}-new",{{boxShadow:"0 0 0px rgba(56,189,248,0)"}},{{boxShadow:"0 0 80px rgba(56,189,248,.8)",'
            f'duration:.4,yoyo:true,repeat:1}},{a + 2.25:.3f});')
        punch(f".{sid}-save", a + 2.3, "scale:.5,opacity:0", .35)

    # board: both new prices together, tilted like a UI card
    a = S["board"][0]
    flash(a, .5)
    slam(".bd-k", a + .05)
    add(f'tl.fromTo(".bd-b",{{rotationX:40,rotationY:-25,y:200,opacity:0}},{{rotationX:12,rotationY:-10,y:0,opacity:1,duration:.7,'
        f'ease:"expo.out"}},{a + .15:.3f});')
    add(f'tl.to(".bd-b",{{rotationX:0,rotationY:0,duration:{BAR * 1.5 - .9:.3f},ease:"sine.inOut"}},{a + .85:.3f});')
    for i, r in enumerate((".r1", ".r2")):
        add(f'tl.fromTo("{r}",{{x:-120,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"expo.out"}},{a + .5 + i * .25:.3f});')
        add(f'tl.fromTo("{r} .bn",{{scale:1.8,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:"expo.out"}},{a + 1.1 + i * .25:.3f});')

    # tilted grid of cards scrolling past
    a = S["grid"][0]
    add(f'tl.fromTo(".gridin",{{y:0}},{{y:-900,duration:{BAR * 1.5:.3f},ease:"none"}},{a:.3f});')
    add(f'tl.fromTo(".plane",{{rotationZ:-24,scale:1.25}},{{rotationZ:-18,scale:1.1,duration:{BAR * 1.5:.3f},ease:"none"}},{a:.3f});')
    punch(".g-1", a + .3, "y:60,opacity:0,filter:\"blur(10px)\"", .4)
    punch(".g-2", a + .75, "y:60,opacity:0,filter:\"blur(10px)\"", .4)

    # dates
    a = S["dates"][0]
    flash(a, .5)
    slam(".dt-k", a + .05)
    add(f'tl.fromTo(".dt-a",{{rotationX:-90,opacity:0}},{{rotationX:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},{a + .3:.3f});')
    add(f'tl.fromTo(".dt-dash",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power2.out"}},{a + .75:.3f});')
    add(f'tl.fromTo(".dt-b",{{rotationX:-90,opacity:0}},{{rotationX:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},{a + 1.05:.3f});')
    punch(".dt-s", a + 1.6, "y:40,opacity:0", .4)

    # don't miss this exclusive offer
    a = S["miss"][0]
    flash(a, .6)
    punch(".m-1", a + .05, "scale:1.8,opacity:0,filter:\"blur(14px)\"", .3)
    punch(".gx-m", a + .5, "scale:1.8,opacity:0,filter:\"blur(14px)\"", .3)
    for sel, dx in ((".gx-r", -14), (".gx-c", 14)):
        add(f'tl.fromTo("{sel}",{{x:{dx},opacity:0}},{{x:0,opacity:0,duration:.6,ease:"steps(6)",'
            f'keyframes:{{opacity:[0,.85,0,.85,0]}}}},{a + .5:.3f});')
        add(f'tl.fromTo("{sel}",{{x:{dx}}},{{x:0,opacity:0,duration:.3,ease:"steps(3)",immediateRender:false,'
            f'keyframes:{{opacity:[.85,0,.85,0]}}}},{a + 1.9:.3f});')
    punch(".m-3", a + .95, "scale:1.8,opacity:0,filter:\"blur(14px)\"", .3)
    add(f'tl.to(".m-1, .m-2, .m-3",{{scale:1.05,duration:{BAR * 1.5 - 1.3:.3f},ease:"none"}},{a + 1.3:.3f});')

    # end card
    a = S["end"][0]
    flash(a, .8)
    add(f'tl.fromTo(".espark",{{scale:0,rotation:-180}},{{scale:1,rotation:0,duration:.6,ease:"back.out(2)"}},{a + .05:.3f});')
    add(f'tl.to(".espark",{{rotation:120,duration:2.4,ease:"none"}},{a + .65:.3f});')
    add(f'tl.fromTo(".e-l",{{opacity:0,scale:1.3,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.5,'
        f'ease:"expo.out"}},{a + .2:.3f});')
    slam(".e-tag", a + .6)
    punch(".e-x", a + .9, "scale:0,opacity:0,rotation:-90")
    add(f'tl.fromTo(".e-imp",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"expo.out"}},{a + 1.0:.3f});')
    add(f'tl.fromTo(".e-cta",{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:.5,ease:"expo.out"}},{a + 1.4:.3f});')
    add(f'tl.fromTo(".e-cta",{{boxShadow:"0 0 0 rgba(56,189,248,0)"}},{{boxShadow:"0 0 60px rgba(56,189,248,.9)",duration:{BEAT:.3f},'
        f'yoyo:true,repeat:3}},{a + 1.9:.3f});')
    punch(".e-valid", a + 1.7, "y:30,opacity:0", .35)

    # always on: speed streaks, drifting glow, grain
    add(f'tl.fromTo("#glow1",{{x:-200,y:-100}},{{x:200,y:150,duration:{DUR / 2},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
    add(f'tl.fromTo("#glow2",{{x:150,y:200}},{{x:-150,y:-200,duration:{DUR / 3},ease:"sine.inOut",yoyo:true,repeat:2}},0);')
    for i in range(36):
        d0 = (i * .11) % 1.4
        add(f'tl.fromTo(".streak.s{i}",{{x:160,scaleX:.2,opacity:0}},{{x:620,scaleX:1.6,opacity:.8,duration:1.4,'
            f'ease:"power1.in",repeat:{int((DUR - d0) / 1.4) - 1}}},{d0:.2f});')
    add(f'tl.fromTo("#grain",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"-2560px 1280px",duration:{DUR},'
        f'ease:"steps(360)"}},0);')
    return "\n".join(T)


def streaks():
    r = random.Random(9)
    out = []
    for i in range(36):
        a = r.uniform(0, 360)
        out.append(f'<div class="streakw" style="transform:rotate({a:.0f}deg)"><div class="streak s{i}"></div></div>')
    return "".join(out)


CSS = """
@font-face { font-family: "Poppins"; font-weight: 600; src: url("assets/fonts/poppins-600.woff2") format("woff2"); }
@font-face { font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/poppins-700.woff2") format("woff2"); }
@font-face { font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-800.woff2") format("woff2"); }
:root { --b1: #1d4ed8; --b2: #2563eb; --cy: #38bdf8; --ink: #04060f; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--ink); }
body { font-family: "Poppins", sans-serif; color: #fff; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden;
  background: radial-gradient(120% 70% at 50% 45%, #0b1a4a 0%, #050a1f 55%, #02030a 100%); }
.clip { position: absolute; inset: 0; }
.scene { z-index: 5; }
.row { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; }
.t, .lt { display: inline-block; }
.cyan { background: linear-gradient(90deg, #60a5fa, #38bdf8, #a5f3fc); -webkit-background-clip: text; background-clip: text; color: transparent; }
.wht { color: #fff; }
#glow1, #glow2 { position: absolute; width: 1100px; height: 1100px; border-radius: 50%; filter: blur(20px); z-index: 1; }
#glow1 { left: -300px; top: 200px; background: radial-gradient(circle, rgba(37,99,235,.55), rgba(37,99,235,0) 65%); }
#glow2 { left: 300px; top: 900px; background: radial-gradient(circle, rgba(56,189,248,.35), rgba(56,189,248,0) 65%); }
#streaks { position: absolute; left: 540px; top: 960px; width: 0; height: 0; z-index: 2; }
.streakw { position: absolute; left: 0; top: 0; width: 0; height: 0; }
.streak { position: absolute; left: 0; top: 0; width: 160px; height: 3px; transform-origin: 0 50%;
  background: linear-gradient(90deg, rgba(160,216,255,0), rgba(160,216,255,.9)); }
#grain { position: absolute; inset: 0; z-index: 40; background-image: url("assets/img/grain.png"); opacity: .07; mix-blend-mode: overlay; }
#flash { position: absolute; inset: 0; z-index: 39; background: #dbeafe; opacity: 0; }
#bgwhite { position: absolute; inset: 0; z-index: 4; opacity: 0;
  background: radial-gradient(70% 45% at 50% 50%, #ffffff 0%, #e0ecff 60%, #b9cdf5 100%); }
/* intro */
.rays { position: absolute; left: -560px; top: -140px; transform-origin: 50% 50%; }
.ring { position: absolute; left: 340px; top: 760px; width: 400px; height: 400px; border-radius: 50%;
  border: 3px solid rgba(160,216,255,.7); box-shadow: 0 0 60px rgba(56,189,248,.5); }
.spark { position: absolute; left: 430px; top: 850px; filter: drop-shadow(0 0 30px #38bdf8) drop-shadow(0 0 80px #2563eb); }
/* words */
.wordstage { position: absolute; inset: 0; }
.word { position: absolute; left: 0; width: 1080px; top: 870px; text-align: center; font: 800 150px "Poppins";
  letter-spacing: -4px; opacity: 0; }
.w1 { color: transparent; -webkit-text-stroke: 4px #9fd8ff; }
.w2 { color: #0a1a4a; }
.w3 { background: linear-gradient(90deg, #60a5fa, #38bdf8); -webkit-background-clip: text; background-clip: text; color: transparent; }
/* logo */
.glitch { position: absolute; left: 90px; top: 820px; width: 900px; }
.glitch img, .elogo img { width: 100%; display: block; }
.g-r img { filter: sepia(1) saturate(8) hue-rotate(-40deg); } .g-c img { filter: sepia(1) saturate(8) hue-rotate(140deg); }
.g-r, .g-c { mix-blend-mode: screen; opacity: 0; }
.slice { position: absolute; left: 0; width: 1080px; height: 14px; opacity: 0; background: linear-gradient(90deg, transparent, #38bdf8, transparent); }
.s1 { top: 850px; } .s2 { top: 905px; height: 8px; } .s3 { top: 960px; }
.tag { font: 600 34px "Poppins"; letter-spacing: 12px; color: #bcd7ff; }
.times { font: 300 70px "Poppins"; color: #7cc8ff; }
.impact { position: absolute; left: 330px; top: 1220px; width: 420px; }
.impact img { width: 100%; display: block; }
.lspark { position: absolute; left: 930px; top: 760px; filter: drop-shadow(0 0 20px #38bdf8); }
/* offer */
.hero { font: 800 230px "Poppins"; letter-spacing: -6px; line-height: 1; text-shadow: 0 10px 60px rgba(37,99,235,.6); }
.pill { position: absolute; left: 110px; top: 830px; width: 860px; height: 190px; border-radius: 40px;
  background: linear-gradient(180deg, #2f6bff, #1d4ed8); border: 4px solid #60a5fa;
  box-shadow: 0 0 60px rgba(37,99,235,.7), inset 0 2px 0 rgba(255,255,255,.35);
  display: flex; align-items: center; justify-content: center; transform-origin: 50% 50%; }
.pill span { font: 800 112px "Poppins"; letter-spacing: -3px; }
.ospark { position: absolute; filter: drop-shadow(0 0 16px #ffd166); }
.os0 { left: 120px; top: 470px; } .os1 { left: 900px; top: 520px; } .os2 { left: 880px; top: 1080px; } .os3 { left: 150px; top: 1090px; }
/* drop */
.big { font: 800 170px "Poppins"; letter-spacing: -5px; line-height: 1; }
.arrow { position: absolute; left: 600px; top: 860px; filter: drop-shadow(0 0 30px rgba(56,189,248,.7)); }
.chart { position: absolute; left: 140px; top: 1180px; opacity: .8; filter: drop-shadow(0 0 16px #38bdf8); }
/* price cards */
.kicker { font: 700 46px "Poppins"; letter-spacing: 10px; color: #9fd8ff; }
.card { position: absolute; left: 140px; width: 800px; border-radius: 36px; text-align: center; }
.card.old { top: 460px; height: 300px; background: rgba(10,20,60,.7); border: 3px solid rgba(96,165,250,.4); }
.card.new { top: 960px; height: 400px; background: linear-gradient(180deg, #2f6bff, #1d4ed8); border: 4px solid #7cc8ff; }
.ptag { margin-top: 26px; font: 700 30px "Poppins"; letter-spacing: 8px; color: #bcd7ff; }
.pnum { font: 800 190px "Poppins"; line-height: 1.05; letter-spacing: -4px; }
.card.new .pnum { font-size: 220px; }
.rs { font-size: .6em; vertical-align: .32em; margin-right: 6px; }
.plabel { font: 700 54px "Poppins"; margin-top: -6px; }
.xmark { position: absolute; left: 250px; top: 90px; }
.xmark path { stroke: #ff3b5c; stroke-width: 16; stroke-linecap: round; fill: none; stroke-dasharray: 1; stroke-dashoffset: 1; }
.chevwrap { position: absolute; left: 0; width: 1080px; top: 820px; text-align: center; transform: rotate(90deg); }
.save { position: absolute; left: 0; width: 1080px; top: 1420px; text-align: center; font: 800 50px "Poppins"; color: #a5f3fc; letter-spacing: 3px; }
/* board */
#sc-board { perspective: 1400px; }
.board { position: absolute; left: 90px; top: 520px; width: 900px; padding: 30px; border-radius: 40px;
  background: rgba(8,16,48,.85); border: 3px solid rgba(96,165,250,.6); box-shadow: 0 30px 120px rgba(37,99,235,.45); }
.brow { display: flex; align-items: center; gap: 30px; padding: 34px 30px; border-radius: 28px; margin: 18px 0;
  background: rgba(37,99,235,.18); border: 2px solid rgba(96,165,250,.35); }
.bo { font: 800 80px "Poppins"; color: rgba(255,255,255,.45); text-decoration: line-through; text-decoration-color: #ff3b5c;
  text-decoration-thickness: 8px; }
.bn { font: 800 120px "Poppins"; display: inline-block; }
.bl { font: 700 46px "Poppins"; color: #bcd7ff; }
/* grid */
#sc-grid { perspective: 1600px; overflow: hidden; }
.plane { position: absolute; left: -300px; top: -200px; width: 1700px; height: 2400px; transform: rotateX(42deg) rotateZ(-20deg); }
.gridin { display: grid; grid-template-columns: repeat(6, 260px); gap: 28px; padding: 40px; }
.gc { height: 300px; border-radius: 26px; background: linear-gradient(160deg, rgba(37,99,235,.35), rgba(8,16,48,.9));
  border: 2px solid rgba(96,165,250,.45); padding: 24px; }
.gc.hot { background: linear-gradient(160deg, #2f6bff, #1d4ed8); }
.gl { font: 700 34px "Poppins"; margin-top: 30px; }
.gbar { height: 14px; border-radius: 8px; margin-top: 30px; background: rgba(160,216,255,.6); }
.fade { position: absolute; inset: 0; background: radial-gradient(60% 30% at 50% 47%, rgba(2,3,10,.92), rgba(2,3,10,.2) 70%, rgba(2,3,10,0)); }
.mid { font: 800 130px "Poppins"; letter-spacing: -4px; line-height: 1; }
/* dates */
#sc-dates { perspective: 1200px; }
.date { position: absolute; top: 560px; width: 360px; height: 460px; border-radius: 36px; text-align: center;
  background: linear-gradient(180deg, #2f6bff, #1d4ed8); border: 4px solid #7cc8ff; box-shadow: 0 0 70px rgba(37,99,235,.6); transform-origin: 50% 0; }
.dt-a { left: 80px; } .dt-b { left: 640px; }
.dm { margin-top: 30px; font: 800 64px "Poppins"; letter-spacing: 8px; color: #dbeafe; }
.dd { font: 800 210px "Poppins"; line-height: 1; letter-spacing: -6px; }
.dy { font: 700 50px "Poppins"; color: #bcd7ff; }
.dash { position: absolute; left: 470px; top: 780px; width: 140px; height: 14px; border-radius: 7px; background: #38bdf8; }
.small { font: 700 52px "Poppins"; }
/* miss */
.big2 { font: 800 150px "Poppins"; letter-spacing: -4px; line-height: 1; }
.glx { position: absolute; left: 0; width: 1080px; top: 740px; height: 150px; text-align: center; }
.gx { position: absolute; left: 0; width: 1080px; font: 800 120px "Poppins"; letter-spacing: -3px; }
.gx-m { color: #fff; } .gx-r { color: #ff2e63; mix-blend-mode: screen; opacity: 0; } .gx-c { color: #22d3ee; mix-blend-mode: screen; opacity: 0; }
/* end */
.espark { position: absolute; left: 900px; top: 540px; filter: drop-shadow(0 0 30px #38bdf8); }
.elogo { position: absolute; left: 90px; top: 650px; width: 900px; }
.e-imp { top: 1010px; }
.cta { position: absolute; left: 160px; top: 1220px; width: 760px; height: 120px; border-radius: 60px; background: linear-gradient(90deg, #2563eb, #38bdf8);
  font: 800 54px "Poppins"; display: flex; align-items: center; justify-content: center; transform-origin: 50% 50%; }
#starwipe { position: absolute; inset: 0; z-index: 38; opacity: 0; }
"""


def main():
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Idigitalpreneur Diwali ad 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-allow-overflow>
        <div id="glow1"></div><div id="glow2"></div><div id="streaks">{streaks()}</div><div id="bgwhite"></div>
      </div>
      {build()}
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="9" data-layout-allow-overflow>
        <svg id="starwipe" viewBox="0 0 1080 1920" width="1080" height="1920"><defs><mask id="sm">
          <rect width="1080" height="1920" fill="#fff"/><g id="starhole"><path transform="translate(540 960)"
          d="M0 -120 C14 -24 24 -14 120 0 C24 14 14 24 0 120 C-14 24 -24 14 -120 0 C-24 -14 -14 -24 0 -120 Z" fill="#000"/></g>
          </mask></defs><rect width="1080" height="1920" fill="#2563eb" mask="url(#sm)"/>
          <g id="starfill"><path transform="translate(540 960)" d="M0 -120 C14 -24 24 -14 120 0 C24 14 14 24 0 120 C-14 24 -24 14 -120 0 C-24 -14 -14 -24 0 -120 Z" fill="#2563eb"/></g></svg>
        <div id="flash"></div><div id="grain"></div>
      </div>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{timeline()}
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
