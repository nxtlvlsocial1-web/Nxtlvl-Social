"""Unrest promo (9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

Recreates the owner's reference (a Duolingo-style product promo: a 3D phone walkthrough, tap ripples, UI that breaks out
of the phone, a brand-colour shape sweep, rings, a blob wipe into the tagline, the logo) for Unrest, the verified network
for Delhi University students (brands/unrest/brand.md). Fixes the reference's reach gaps: a hook line on frame 1, sound on
every tap and pop, a CTA (Comment UNREST). Every cut lands on a downbeat of the track (plan/beats.json, about 129 BPM).
The app screens are designed mockups from the owner's feature list (no real screenshots yet).
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = json.load(open(os.path.join(ROOT, "plan", "beats.json")))["beats"]
BAR = [B[i] for i in range(0, len(B), 4)]                  # downbeats
DUR = round(BAR[8] + 2.8, 2)
BK, CARD, WHITE, MUTE, LIME = "#0a0a0b", "#141416", "#ffffff", "#a9a9b0", "#ccff4d"
JS, SFX, HTML, TOP, HIDDEN = [], [], [], [], []


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def _join(obj, extra):
    body = obj.strip()[1:-1].strip()
    return "{" + (body + ", " if body else "") + extra + "}"


def ft(sel, t, d, frm, to_, ease="expo.out"):
    if re.search(r"opacity:\s*1\b", frm) and "opacity" not in to_:
        to_ = _join(to_, "opacity: 1")
    js(f'tl.fromTo("{sel}", {frm}, {_join(to_, f"duration: {d}, ease: \"{ease}\", immediateRender: false")}, {t:.3f});')


def to(sel, t, d, props, ease="expo.inOut"):
    js(f'tl.to("{sel}", {_join(props, f"duration: {d}, ease: \"{ease}\"")}, {t:.3f});')


def st(sel, t, props):
    if t <= .0001 and props.replace(" ", "") == "{opacity:0}":
        HIDDEN.append(sel)
    js(f'tl.set("{sel}", {props}, {t:.3f});')


def hide(sel):
    HIDDEN.append(sel)


def pop_in(sel, t, d=.55, frm="{opacity: 1, scale: .4, y: 40}", to_="{scale: 1, y: 0}", ease="back.out(2.2)"):
    hide(sel)
    ft(sel, t, d, frm, to_, ease)


def out(sel, t, d=.3, props='{opacity: 0, scale: .9, filter: "blur(10px)"}'):
    to(sel, t, d, props, "power2.in")


def b(bar, beat=0):
    """time of beat `beat` in bar `bar`"""
    return B[bar * 4 + beat]


def head(i, html, bar, top=300, size=96, beat=0):
    """a headline that slides up out of its mask on a downbeat and leaves before the next one"""
    lines = "".join(f'<span class="ln"><span>{ln}</span></span>' for ln in html)
    HTML.append(f'<div class="hd" id="h{i}" style="top:{top}px;font-size:{size}px">{lines}</div>')
    hide(f"#h{i}")
    t = b(bar, beat)
    st(f"#h{i}", t - .02, "{opacity: 1}")
    js(f'tl.fromTo("#h{i} .ln > span", {{yPercent: 110}}, {{yPercent: 0, duration: .55, ease: "expo.out", stagger: .07, immediateRender: false}}, {t - .02:.3f});')


def tap(sid, x, y, t):
    """a tap on the phone screen: a dot lands, a ring ripples out (inside the screen, so it moves with the phone)"""
    HTML_SCREENS[sid].append(f'<i class="tap" id="tp{len(SFX)}_{sid}" style="left:{x - 40}px;top:{y - 40}px"></i>')
    i = f"#tp{len(SFX)}_{sid}"
    hide(i)
    ft(i, t - .12, .14, "{opacity: 1, scale: .4}", "{scale: 1}", "power2.out")
    to(i, t + .02, .08, "{scale: .8}", "power2.in")
    to(i, t + .1, .35, "{scale: 1.8, opacity: 0}", "power2.out")
    sfx("click", t)


# ---------------------------------------------------------------- the phone and its screens (designed mockups)
HTML_SCREENS = {k: [] for k in "ABCDEF"}
HDR = '<div class="ah"><img src="assets/img/unrest_wordmark.png" alt=""><i class="vd">DU verified</i></div>'
SCREENS = {
    "A": '<div class="sA"><img class="wm" src="assets/img/unrest_wordmark.png" alt=""><p>Only for Delhi University students</p>'
         '<div class="avs"><i>A</i><i>R</i><i>K</i><i>S</i><i>+</i></div><b class="btn">Continue with DU email</b></div>',
    "B": HDR + '<div class="sB"><h3>Verify you\'re at DU</h3><div class="fld">your.name@college email</div>'
         '<div class="chk"><i></i>College email</div><div class="chk"><i></i>Student ID</div><b class="btn" id="vbtn">Verify</b></div>',
    "C": HDR + '<div class="sC"><div class="live"><i></i>Corridor <span>LIVE</span></div>'
         '<div class="pc"><div class="pav">A</div><b>Aanya</b><span>2nd year &middot; B.Com &middot; North Campus</span>'
         '<div class="tags"><i>open mics</i><i>football</i><i>startups</i></div></div>'
         '<div class="two"><b class="ghost">Skip</b><b class="btn">Say hi</b></div></div>',
    "D": HDR + '<div class="sD"><h3>Events near you</h3>'
         '<div class="ev"><b>Open mic night</b><span>North Campus &middot; Fri 6 PM</span></div>'
         '<div class="ev"><b>Freshers meetup</b><span>South Campus &middot; Sat 4 PM</span></div>'
         '<div class="ev"><b>Startup talk</b><span>Arts Faculty &middot; Mon 2 PM</span></div><b class="btn">I\'m going</b></div>',
    "E": HDR + '<div class="sE"><h3>Everything DU</h3><div class="grid">'
         '<i>Flatmates</i><i>Part-time</i><i>Internships</i><i>Events</i><i class="nw">Course feed</i><i class="nw">Library rooms</i></div></div>',
    "F": HDR + '<div class="sF"><h3>Course feed <em>NEW</em></h3>'
         '<div class="post"><b>Eco (H), 2nd year</b><span>Anyone has notes for Unit 3?</span><i>12 replies</i></div>'
         '<div class="post"><b>Library rooms <em>NEW</em></b><span>Room 4 &middot; 3 seats free &middot; till 6 PM</span><i class="lk">Join room</i></div></div>',
}
ORDER = "ABCDEF"

# bar 0: frame 1 shows the hook line, the giant wordmark and the phone (visible in CSS from frame 0)
HTML.append('<img id="bgwm" src="assets/img/unrest_wordmark.png" alt="">')
HTML.append('<div class="hd" id="h0" style="top:300px;font-size:100px"><span class="ln"><span>Everyone here is</span></span>'
            f'<span class="ln"><span>a <em>DU student.</em></span></span></div>')
js(f'tl.fromTo("#bgwm", {{x: 120, y: 0, scale: 2.6}}, {{x: -260, y: 0, scale: 2.9, duration: {DUR:.2f}, ease: "none", immediateRender: true}}, 0);')
js('tl.fromTo("#h0 .ln > span", {y: 10}, {y: 0, duration: .4, ease: "expo.out", stagger: .06, immediateRender: true}, 0);')
sfx("thump", .02)

# phone poses: one per bar (3D swing on every downbeat)
POSES = [(-14, 8, -3, 0), (16, 6, 3, -10), (-18, 10, -4, 0), (14, 6, 2, -10), (0, 4, 0, 0), (-12, 8, -2, -10)]
ft("#phone", 0, .9, "{rotationY: -24, rotationX: 16, rotation: -6, y: 80}", f"{{rotationY: {POSES[0][0]}, rotationX: {POSES[0][1]}, rotation: {POSES[0][2]}, y: {POSES[0][3]}}}")
for k in range(1, 6):
    ry, rx, rz, yy = POSES[k]
    to("#phone", b(k) - .25, .55, f"{{rotationY: {ry}, rotationX: {rx}, rotation: {rz}, y: {yy}}}", "expo.inOut")
    # the screen slides to the next one
    to(f"#scr{ORDER[k - 1]}", b(k) - .22, .45, "{xPercent: -100}", "expo.inOut")
    st(f"#scr{ORDER[k - 1]}", b(k) + .24, "{opacity: 0}")           # parked screens are hidden, not just off to the side
    ft(f"#scr{ORDER[k]}", b(k) - .22, .45, "{opacity: 1, xPercent: 100}", "{xPercent: 0}", "expo.inOut")
    sfx("whoosh", b(k) - .22)
for k in range(1, 6):
    st(f"#scr{ORDER[k]}", 0, "{xPercent: 100}")
    hide(f"#scr{ORDER[k]}")

# bar 0: tap "Continue with DU email"
tap("A", 200, 760, b(0, 2))
out("#h0", b(1) - .25)

# bar 1: verify -> the badge breaks out of the phone
head(1, ["Verified.", "<em>Every single person.</em>"], 1)
tap("B", 200, 720, b(1, 1))
st(".chk", b(1, 1) + .1, "{className: 'chk on'}")
sfx("g_tick", b(1, 1) + .1)
TOP_POP = []
HTML.append(f'<div data-layout-allow-overlap class="pop badge" id="pbadge"><i>&#10003;</i>Verified DU student</div>')
pop_in("#pbadge", b(1, 2), .6, "{opacity: 1, scale: .3, y: 160, rotation: -8}", "{scale: 1, y: 0, rotation: -4}")
sfx("pop", b(1, 2)); sfx("sparkle", b(1, 2) + .05)
out("#pbadge", b(2) - .3)
out("#h1", b(2) - .25)

# bar 2: Corridor live -> the match card breaks out
head(2, ["Meet people", "<em>live, on Corridor.</em>"], 2)
tap("C", 280, 780, b(2, 2))
HTML.append('<div data-layout-allow-overlap class="pop match" id="pmatch"><div class="pav">A</div><div><b>You and Aanya</b><span>both into open mics &middot; say hi</span></div></div>')
pop_in("#pmatch", b(2, 2) + .08, .6, "{opacity: 1, scale: .3, y: 120, rotation: 8}", "{scale: 1, y: 0, rotation: 3}")
sfx("pop", b(2, 2) + .08); sfx("msg", b(2, 3))
out("#pmatch", b(3) - .3)
out("#h2", b(3) - .25)

# bar 3: events, a lime curve sweeps behind the phone, the ticket breaks out
head(3, ["On-ground", "<em>events.</em>"], 3)
HTML.append('<svg id="arc" viewBox="0 0 1000 1000"><path d="M -100 900 C 200 300 800 300 1100 900" fill="none" stroke="#ccff4d" stroke-width="150" stroke-linecap="round" pathLength="1"/></svg>')
hide("#arc")
st("#arc", b(3) - .3, "{opacity: 1}")
ft("#arc path", b(3) - .3, .7, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "expo.inOut")
to("#arc", b(4) - .35, .4, "{opacity: 0}", "power2.in")
sfx("whoosh_big", b(3) - .3)
tap("D", 200, 760, b(3, 2))
HTML.append('<div data-layout-allow-overlap class="pop ticket" id="pticket"><b>Open mic night</b><span>North Campus &middot; Fri 6 PM</span><i>&#10003; Going</i></div>')
pop_in("#pticket", b(3, 2) + .08, .6, "{opacity: 1, scale: .3, y: 140, rotation: -10}", "{scale: 1, y: 0, rotation: -5}")
sfx("pop", b(3, 2) + .08); sfx("cash", b(3, 3))
out("#pticket", b(4) - .3)
out("#h3", b(4) - .25)

# bar 4: everything DU: rings pulse, the five things burst out of the phone, one per beat
head(4, ["Flatmates. Work.", "<em>Internships.</em>"], 4)
for r in range(3):
    HTML.append(f'<i class="ring" id="rg{r}"></i>')
    hide(f"#rg{r}")
    ft(f"#rg{r}", b(4) + r * .15, 1.1, "{opacity: .6, scale: .3}", "{opacity: 0, scale: 1.6}", "power2.out")
TILES = [("Flatmates", -330, -330, -8), ("Part-time work", 330, -250, 6), ("Internships", -340, 170, 5), ("Course feed", 340, 250, -6), ("Library rooms", 0, 470, 2)]
for k, (lab, x, y, r) in enumerate(TILES):
    HTML.append(f'<div data-layout-allow-overlap class="pop tile" id="tl{k}">{lab}</div>')
    t = b(4) + .05 + k * (b(4, 2) - b(4)) / 4               # the last one lands before the bar's exits start
    pop_in(f"#tl{k}", t, .5, f"{{opacity: 1, x: 0, y: 0, scale: .2, rotation: 0}}", f"{{x: {x}, y: {y}, scale: 1, rotation: {r}}}", "back.out(1.8)")
    sfx("g_pickup" if k % 2 == 0 else "pop", t)
for k in range(5):
    out(f"#tl{k}", b(5) - .3)
out("#h4", b(5) - .25)

# bar 5: new: course feed + library rooms
head(5, ["New: course feed", "<em>+ library rooms.</em>"], 5)
tap("F", 290, 760, b(5, 2))
HTML.append('<div data-layout-allow-overlap class="pop newp" id="pnew"><em>NEW</em>Library rooms &middot; 3 seats free</div>')
pop_in("#pnew", b(5, 2) + .08, .55, "{opacity: 1, scale: .3, y: 120}", "{scale: 1, y: 0}")
sfx("pop", b(5, 2) + .08); sfx("ding", b(5, 3))
out("#pnew", b(6) - .3)
out("#h5", b(6) - .25)

# bar 6: a lime blob wipes the frame: "You're not doing DU alone."
out("#phone", b(6) - .3, .35, '{opacity: 0, scale: .8, y: 200, filter: "blur(12px)"}')
HTML.append('<i id="blob"></i>')
hide("#blob")
ft("#blob", b(6) - .25, .6, "{opacity: 1, scale: 0}", "{scale: 1}", "expo.inOut")
sfx("whoosh_big", b(6) - .3)
HTML.append('<div class="big" data-layout-allow-overlap id="alone"><span class="ln"><span>You\'re not</span></span><span class="ln"><span>doing DU</span></span><span class="ln"><span><em>alone.</em></span></span></div>')
hide("#alone")
st("#alone", b(6) + .1, "{opacity: 1}")
js(f'tl.fromTo("#alone .ln > span", {{yPercent: 110}}, {{yPercent: 0, duration: .6, ease: "expo.out", stagger: .09, immediateRender: false}}, {b(6) + .1:.3f});')
sfx("thump", b(6, 1))

# bar 7: the blob shrinks away; the tagline in white on black
to("#blob", b(7) - .25, .55, "{scale: 0}", "expo.inOut")
out("#alone", b(7) - .3, .3)
sfx("whoosh", b(7) - .25)
HTML.append('<div class="big w" id="tag"><span class="ln"><span>Your Campus.</span></span><span class="ln"><span><em>Your Network.</em></span></span></div>')
hide("#tag")
st("#tag", b(7) + .05, "{opacity: 1}")
js(f'tl.fromTo("#tag .ln > span", {{yPercent: 110}}, {{yPercent: 0, duration: .6, ease: "expo.out", stagger: .25, immediateRender: false}}, {b(7) + .05:.3f});')
sfx("thump", b(7)); sfx("thump", b(7, 1) + .1)
out("#tag", b(8) - .3, .3)

# bar 8: the owner's logo animation + the CTA
HTML.append(f'<video id="logo" src="assets/video/unrest_logo.mp4" data-start="{b(8) - .1:.3f}" data-duration="{DUR - b(8) + .1:.2f}" data-track-index="1" muted playsinline></video>')
hide("#logo")
st("#logo", b(8) - .1, "{opacity: 1}")
sfx("riser_short", b(8) - .6); sfx("sparkle", b(8) + .6)
HTML.append('<div class="cbox" id="cbox"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>'
            '<div class="ctal" id="ctal">Comment <b>UNREST</b> and get the link in DM</div>')
pop_in("#cbox", b(8, 2), .5, "{opacity: 1, y: 40}", "{y: 0}", "expo.out")
pop_in("#ctal", b(8, 2) + .15, .5, "{opacity: 1, y: 20}", "{y: 0}", "expo.out")
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 6, duration: .5, ease: "steps(6)", onUpdate: () => {{ document.getElementById("cty").textContent = "UNREST".slice(0, Math.round(o.n)); }}}}, {b(8, 3):.3f}); }})();')
st("#cph", b(8, 3), "{opacity: 0}")
sfx("typing", b(8, 3)); sfx("notify", b(8, 3) + .7)

# ---------------------------------------------------------------- page
screens = "".join(f'<div class="scr" id="scr{k}">{SCREENS[k]}{"".join(HTML_SCREENS[k])}</div>' for k in ORDER)
PHONE = f'<div id="stage"><div id="phone" data-layout-allow-overlap><div class="notch"></div><div class="glass">{screens}</div></div></div>'
CSS = f"""
@font-face {{ font-family: Ser; src: url("assets/fonts/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family: Ser; font-style: italic; src: url("assets/fonts/instrument-serif-latin-400-italic.woff2"); }}
@font-face {{ font-family: Sat; font-weight: 500; src: url("assets/fonts/fontshare/Satoshi-Medium.woff2"); }}
@font-face {{ font-family: Sat; font-weight: 700; src: url("assets/fonts/fontshare/Satoshi-Bold.woff2"); }}
@font-face {{ font-family: Sat; font-weight: 900; src: url("assets/fonts/fontshare/Satoshi-Black.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {BK}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Sat; color: {WHITE};
  background: radial-gradient(60% 40% at 50% 62%, rgba(204,255,77,.10), rgba(0,0,0,0) 70%), {BK}; }}
#grain {{ position: absolute; inset: 0; background: url(assets/img/noise.png); opacity: .07; mix-blend-mode: overlay; pointer-events: none; z-index: 90; }}
#bgwm {{ position: absolute; left: 220px; top: 860px; width: 640px; opacity: .07; z-index: 1; }}
.hd {{ position: absolute; left: 80px; right: 70px; font-family: Ser; line-height: .98; letter-spacing: -.01em; z-index: 30; }}
.hd em, .big em {{ font-style: italic; color: {LIME}; }}
.ln {{ display: block; overflow: hidden; padding-bottom: .08em; }}
.ln > span {{ display: inline-block; }}
#stage {{ position: absolute; left: 0; right: 0; top: 600px; height: 900px; perspective: 1800px; z-index: 10; }}
#phone {{ position: relative; margin: 0 auto; width: 430px; height: 880px; border-radius: 66px; background: #1b1b1f; padding: 14px;
  box-shadow: 0 0 0 2px #2a2a30, 0 60px 120px rgba(0,0,0,.7), 0 0 120px rgba(204,255,77,.10); transform-style: preserve-3d; }}
.notch {{ position: absolute; left: 50%; top: 26px; width: 120px; height: 34px; margin-left: -60px; border-radius: 20px; background: #000; z-index: 5; }}
.glass {{ position: relative; width: 100%; height: 100%; border-radius: 54px; overflow: hidden; background: #0e0e10; }}
.scr {{ position: absolute; inset: 0; padding: 80px 26px 30px; }}
.ah {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 26px; }}
.ah img {{ height: 34px; }}
.vd {{ font-style: normal; font-size: 18px; font-weight: 700; color: {BK}; background: {LIME}; padding: 6px 12px; border-radius: 999px; }}
.btn {{ display: block; background: {LIME}; color: {BK}; text-align: center; font-weight: 900; font-size: 26px; padding: 22px; border-radius: 22px; }}
.ghost {{ display: block; background: #222227; color: {WHITE}; text-align: center; font-weight: 700; font-size: 26px; padding: 22px; border-radius: 22px; }}
h3 {{ font-family: Ser; font-weight: 400; font-size: 52px; line-height: 1; margin-bottom: 22px; }}
h3 em, .post em {{ font-style: normal; font-family: Sat; font-weight: 900; font-size: 16px; color: {BK}; background: {LIME}; padding: 4px 10px; border-radius: 999px; vertical-align: middle; }}
.sA {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px; text-align: center; }}
.sA .wm {{ width: 300px; }}
.sA p {{ margin: 18px 0 40px; font-size: 24px; color: {MUTE}; font-weight: 500; }}
.avs {{ display: flex; margin-bottom: 70px; }}
.avs i {{ width: 62px; height: 62px; border-radius: 50%; margin-left: -14px; border: 3px solid #0e0e10; display: grid; place-items: center; font-style: normal; font-weight: 900;
  font-size: 24px; color: {BK}; background: linear-gradient(135deg, #e6e6ea, {LIME}); }}
.sA .btn {{ position: absolute; left: 26px; right: 26px; bottom: 60px; }}
.fld {{ background: {CARD}; border: 2px solid #2a2a30; border-radius: 18px; padding: 22px; font-size: 22px; color: {MUTE}; margin-bottom: 24px; }}
.chk {{ display: flex; align-items: center; gap: 14px; font-size: 24px; font-weight: 700; margin-bottom: 18px; color: {MUTE}; }}
.chk i {{ width: 30px; height: 30px; border-radius: 8px; border: 2px solid #3a3a40; }}
.chk.on {{ color: {WHITE}; }} .chk.on i {{ background: {LIME}; border-color: {LIME}; }}
.sB .btn {{ margin-top: 260px; }}
.live {{ display: flex; align-items: center; gap: 12px; font-family: Ser; font-size: 46px; margin-bottom: 20px; }}
.live i {{ width: 16px; height: 16px; border-radius: 50%; background: {LIME}; box-shadow: 0 0 0 8px rgba(204,255,77,.2); }}
.live span {{ font-family: Sat; font-weight: 900; font-size: 16px; letter-spacing: .1em; color: {BK}; background: {LIME}; padding: 4px 10px; border-radius: 6px; }}
.pc {{ background: {CARD}; border-radius: 30px; padding: 30px 24px; text-align: center; margin-bottom: 26px; }}
.pav {{ width: 140px; height: 140px; border-radius: 50%; margin: 0 auto 16px; display: grid; place-items: center; font-family: Ser; font-size: 80px; color: {BK};
  background: linear-gradient(135deg, #f0f0f3, {LIME}); }}
.pc b {{ display: block; font-size: 34px; }}
.pc span {{ display: block; font-size: 20px; color: {MUTE}; margin-top: 6px; }}
.tags {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 16px; }}
.tags i {{ font-style: normal; font-size: 18px; font-weight: 700; padding: 6px 12px; border-radius: 999px; background: #222227; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
.ev {{ background: {CARD}; border-radius: 22px; padding: 20px 22px; margin-bottom: 14px; border-left: 6px solid {LIME}; }}
.ev b {{ display: block; font-size: 28px; }}
.ev span {{ font-size: 20px; color: {MUTE}; }}
.sD .btn {{ margin-top: 40px; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
.grid i {{ font-style: normal; height: 150px; border-radius: 24px; background: {CARD}; display: flex; align-items: flex-end; padding: 18px; font-weight: 900; font-size: 24px; }}
.grid i.nw {{ background: {LIME}; color: {BK}; }}
.post {{ background: {CARD}; border-radius: 22px; padding: 22px; margin-bottom: 16px; }}
.post b {{ display: block; font-size: 26px; }}
.post span {{ display: block; font-size: 22px; color: #c9c9cf; margin: 8px 0 12px; }}
.post i {{ font-style: normal; font-size: 18px; color: {MUTE}; }}
.post i.lk {{ display: inline-block; color: {BK}; background: {LIME}; font-weight: 900; padding: 8px 16px; border-radius: 999px; }}
.tap {{ position: absolute; width: 80px; height: 80px; border-radius: 50%; background: rgba(255,255,255,.35); border: 4px solid #fff; z-index: 9; }}
.pop {{ position: absolute; z-index: 40; box-shadow: 0 40px 80px rgba(0,0,0,.55); }}
.badge {{ left: 230px; top: 1000px; display: flex; align-items: center; gap: 18px; background: {LIME}; color: {BK}; font-weight: 900; font-size: 46px; padding: 26px 40px; border-radius: 999px; }}
.badge i {{ width: 60px; height: 60px; border-radius: 50%; background: {BK}; color: {LIME}; display: grid; place-items: center; font-style: normal; font-size: 34px; }}
.match {{ left: 150px; top: 1080px; width: 780px; display: flex; align-items: center; gap: 24px; background: {WHITE}; color: {BK}; padding: 26px 32px; border-radius: 40px; }}
.match .pav {{ width: 110px; height: 110px; font-size: 64px; margin: 0; flex: none; }}
.match b {{ display: block; font-size: 44px; }} .match span {{ font-size: 28px; color: #55555c; }}
.ticket {{ left: 190px; top: 1050px; width: 700px; background: {WHITE}; color: {BK}; padding: 30px 36px; border-radius: 34px; border-left: 16px solid {LIME}; }}
.ticket b {{ display: block; font-family: Ser; font-weight: 400; font-size: 64px; line-height: 1; }}
.ticket span {{ display: block; font-size: 28px; color: #55555c; margin: 8px 0 16px; }}
.ticket i {{ font-style: normal; font-weight: 900; font-size: 30px; background: {LIME}; padding: 10px 20px; border-radius: 999px; }}
.tile {{ left: 400px; top: 960px; width: 280px; height: 110px; display: grid; place-items: center; background: {WHITE}; color: {BK}; font-weight: 900; font-size: 32px; border-radius: 28px; }}
.newp {{ left: 160px; top: 1090px; width: 760px; display: flex; align-items: center; gap: 18px; background: {WHITE}; color: {BK}; font-weight: 900; font-size: 38px; padding: 28px 34px; border-radius: 34px; }}
.newp em {{ font-style: normal; font-size: 22px; background: {LIME}; padding: 8px 14px; border-radius: 999px; }}
.ring {{ position: absolute; left: 140px; top: 640px; width: 800px; height: 800px; border-radius: 50%; border: 4px solid {LIME}; z-index: 5; }}
#arc {{ position: absolute; left: 0; top: 720px; width: 1080px; height: 1080px; z-index: 4; }}
#arc path {{ stroke-dasharray: 1; stroke-dashoffset: 1; }}
#blob {{ position: absolute; left: -600px; top: -100px; width: 2300px; height: 2300px; border-radius: 50%; background: {LIME}; z-index: 50; transform-origin: 50% 100%; }}
.big {{ position: absolute; left: 80px; right: 70px; top: 640px; font-family: Ser; font-size: 170px; line-height: .92; color: {BK}; z-index: 55; }}
.big em {{ color: {BK}; }}
.big.w {{ color: {WHITE}; top: 720px; font-size: 150px; }}
.big.w em {{ color: {LIME}; }}
#logo {{ position: absolute; left: 0; top: 420px; width: 1080px; height: 1080px; object-fit: cover; z-index: 45; mix-blend-mode: screen; }}
.cbox {{ position: absolute; left: 110px; width: 860px; top: 1300px; height: 130px; border-radius: 65px; background: {CARD}; border: 2px solid #2a2a30; display: flex; align-items: center;
  gap: 22px; padding: 0 30px; font-weight: 900; font-size: 56px; letter-spacing: .04em; z-index: 60; }}
.cbox .av {{ width: 76px; height: 76px; border-radius: 50%; background: linear-gradient(135deg, #f0f0f3, {LIME}); flex: none; }}
#cph {{ position: absolute; left: 130px; color: {MUTE}; font-weight: 500; font-size: 44px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: {LIME}; }}
.ctal {{ position: absolute; left: 0; right: 0; top: 1460px; text-align: center; font-size: 40px; font-weight: 700; color: #d8d8dc; z-index: 60; }}
.ctal b {{ color: {LIME}; font-weight: 900; }}
"""
hidden_css = "".join(f"{s} {{ opacity: 0; }}" for s in dict.fromkeys(HIDDEN))
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Unrest promo 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}{hidden_css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      {PHONE}
      {chr(10).join(HTML)}
      {chr(10).join(TOP)}
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, bars {[round(x, 2) for x in BAR[:9]]}")
