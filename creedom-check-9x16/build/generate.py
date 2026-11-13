"""Creators 100X x Creedom "CHECK" reel (9:16): writes index.html and plan/sfx_events.json from plan/words.json.

Look (owner: "premium glass fluid animations, nothing like paper or cardboard, premium transitions"): alternating LIGHT
fluid scenes (white with drifting Creedom-pink, rose, lilac and peach blobs) and DARK scenes (near-black with a magenta
glow), with big frosted-glass panes drifting at the edges. Every object is frosted glass (backdrop blur + saturate,
white highlight edge, inner glow) that tilts slowly in 3D and catches a moving specular shine. Type blurs into focus
word by word (Inter, Instrument Serif Italic accents, JetBrains Mono labels). Transitions: liquid-glass morphs (an
organic glass drop grows over the frame and melts away), frosted-glass sweeps and zoom-throughs.
The reel being checked is a neutral demo (Pexels clips, "3 AI tools I use daily"); its score is labelled "Example reel".
Creedom's own steps and its "timestamp + fix" format come from the owner's screen recording.

v4 (owner: "look at all these alignment issues", "the mascot still looks bad, not the same quality as the previous
Creedom reel", "still very less glass animations"):
- one layout grid: headline block 190-470, hero band below it, everything centred on x=540 or on clean columns,
  nothing in the bottom caption zone (y > 1610) and no element covering another;
- the mascot performs like he did in the Creedom reel-analyser reel (walks in, hops, kicks, spins, shrugs, scratches
  his head, glass "?" and "!" bubbles, sweat, sparkles, heart and star eyes) with his arms used as arms, never flapped;
- liquid-glass transitions, glass panes in the background, shine sweeps and slow 3D tilt on every glass object.
python3 build/generate.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bird  # noqa: E402  (the Creedom mascot rig, from creedom-reel-analyser-9x16)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
PINK, MAG, ROSE, INK = "#EE688B", "#F343A2", "#B1476B", "#0B0B0B"
random.seed(11)
LINES = {}
for w in W:
    LINES.setdefault(w["line"], []).append(w)
L0 = {k: v[0]["t0"] for k, v in LINES.items()}
L1 = {k: v[-1]["t1"] for k, v in LINES.items()}
DUR = round(L1["c06"] + .8, 2)
JS, SFX, HTML = [], [], []


def T(line, word, n=0):
    k = word.lower()
    hits = [w for w in LINES[line] if w["w"].lower().strip(".,:!?").startswith(k)]
    return hits[min(n, len(hits) - 1)]["t0"]


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def ft(sel, t, d, frm, to, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


WID = [0]


def head(hid, rows, top, line, size=88, dark=False, after=0.0):
    """premium headline, centred: every word blurs into focus on its spoken time; ('word', cls) with cls '' or 'it'"""
    spoken, k, out, rws = [w for w in LINES[line] if w["t0"] >= after], 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?"), None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?")
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="hw {cls}" id="{wid}">{word}</span>')
            out.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTML.append(f'<div class="head {"dk" if dark else ""}" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .06, .5, "{opacity: 0, filter: 'blur(14px)', y: 26}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    return out


def head_out(hid, t):
    to(f"#{hid}", t, .3, "{opacity: 0, filter: 'blur(16px)', y: -40}", "power2.in")


SH = '<i class="sh"></i>'                       # specular shine bar inside a glass object


def shine(sel, t, d=.9):
    ft(f"{sel} > .sh", t, d, "{xPercent: -160, opacity: 1}", "{xPercent: 420, opacity: 1}", "power2.inOut")


def tilt(sel, t0, t1, a=4, per=1.7):
    """slow 3D drift so the glass catches the light (rotation only, so it never fights the position tweens)"""
    n = max(1, int((t1 - t0) / per))
    js(f'tl.fromTo("{sel}", {{rotationX: 0, rotationY: 0, transformPerspective: 1400}}, {{rotationX: {a * .6:.1f}, rotationY: {-a}, transformPerspective: 1400, duration: {per:.2f}, ease: "sine.inOut", '
       f'yoyo: true, repeat: {n - 1}, immediateRender: false}}, {t0:.3f});')


def sweep(t):
    """frosted-glass panel sweeping across the frame (scene change)"""
    ft("#sweep", t - .22, .55, "{xPercent: -170}", "{xPercent: 170}", "power2.inOut")
    sfx("whoosh_big", t - .25)


LIQ = [0]


def liquid(t):
    """liquid-glass morph: an organic glass drop grows over the frame, the scene changes under it, and it melts away"""
    LIQ[0] += 1
    r0, r1 = "50% 50% 50% 50% / 50% 50% 50% 50%", ("42% 58% 63% 37% / 41% 44% 56% 59%", "58% 42% 38% 62% / 55% 61% 39% 45%")[LIQ[0] % 2]
    ft("#liq", t - .5, .55, f"{{scale: .04, rotation: 0, borderRadius: '{r0}'}}", f"{{scale: 4.4, opacity: 1, rotation: {(90, -90)[LIQ[0] % 2]}, borderRadius: '{r1}'}}", "power2.in")
    to("#liq", t + .05, .45, "{opacity: 0, filter: 'blur(30px)'}", "power2.out")
    st("#liq", t - .5, "{filter: 'blur(0px)', opacity: 1}")
    st("#liq", t + .52, "{scale: .04, filter: 'blur(0px)'}")
    sfx("whoosh", t - .45)
    sfx("swish", t - .05)


def zoom_through(t):
    ft("#cam", t - .25, .3, "{scale: 1, filter: 'blur(0px)'}", "{scale: 1.6, filter: 'blur(14px)'}", "power2.in")
    ft("#cam", t + .05, .5, "{scale: .8, filter: 'blur(14px)'}", "{scale: 1, filter: 'blur(0px)'}", "expo.out")
    sfx("riser", t - .7)


def mode(t, dark):
    """crossfade between the light and the dark fluid worlds"""
    to("#dark", t - .1, .45, f"{{opacity: {1 if dark else 0}}}", "power2.inOut")


def scene(sid, t0, t1):
    st(f"#{sid}", t0, "{opacity: 1}")
    st(f"#{sid}", t1, "{opacity: 0}")
    ft("#drift", t0, t1 - t0, "{scale: 1}", "{scale: 1.035}", "none")      # slow push-in on every scene


SA, SB, SC, SD, SE, SF, SG = 0.0, L0["c01"] - .14, L0["c02"] - .14, L0["c03"] - .1, L0["c04"] - .12, L0["c05"] - .12, L0["c06"] - .12
# ---- layout grid (v4) -----------------------------------------------------------------------------------------------------
# headline block from y 190; phone (base box 540x960 at 270,520, centre 540,1000) at scale .78 -> 329..751 x 615..1365;
# chip slot 1392..1474 and Share pill 1500..1600 under it; the mascot stands right of the phone, feet on y 1365.
PH = "{x: 0, y: -10, scale: .78}"
MASCOT_R = (755, 1049, .9)                      # right of the phone, feet level with its bottom (box 300x318, feet ~y+316)

# ---- persistent objects: the phone (demo reel) and the Share pill ----------------------------------------------------------
# a 30 s demo reel (three Pexels clips) that plays straight through on the scene clock
VIDS = [(0, SB + .02, 0.0), (SC - .02, SD + .02, 5.0), (SF - .02, DUR, 14.0)]
vids = "".join(f'<video class="dv" id="dv{i}" src="assets/video/demo_long.mp4" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-media-start="{m:.3f}" '
               f'data-track-index="{1 + i % 2}" muted playsinline></video>' for i, (a, b, m) in enumerate(VIDS))
ICONS = ('<svg viewBox="0 0 24 24"><path d="M12 20.5s-7.5-4.6-9.3-9.2C1.4 7.9 3.6 4.5 7 4.5c2 0 3.6 1.1 5 3 1.4-1.9 3-3 5-3 3.4 0 5.6 3.4 4.3 6.8-1.8 4.6-9.3 9.2-9.3 9.2z"/></svg>'
         '<svg viewBox="0 0 24 24"><path d="M20.5 11.5a8.5 8.5 0 0 1-12.6 7.4L3.5 20l1.2-4.1A8.5 8.5 0 1 1 20.5 11.5z"/></svg>'
         '<svg viewBox="0 0 24 24"><path d="M21.5 3 10 14.5M21.5 3 15 21l-5-6.5L3 9.5 21.5 3z"/></svg>')
HTML.append('<div class="phone" id="phone"><div class="scr">' + vids +
            f'<div class="ig"><div class="cap">3 AI tools I use daily</div><div class="tool glass" id="tool">Tool 3: <b>Creedom</b></div>'
            f'<div class="side">{ICONS}</div><div class="who"><b></b>creator.daily</div></div><div class="glint"></div><i class="pshine" id="pshine"></i></div>'
            '<div class="isl"></div></div>')
HTML.append(f'<div class="share glass" id="share">{SH}<svg class="lk" id="lk" viewBox="0 0 24 24"><path d="M7 11V8a5 5 0 0 1 10 0v3"/><rect x="5" y="11" width="14" height="10" rx="3"/></svg>'
            '<span id="shtx">Share</span></div>')


def phone_shine(t):
    ft("#pshine", t, 1.0, "{xPercent: -150, opacity: 1}", "{xPercent: 330, opacity: 1}", "power2.inOut")


# ---- A hook (light) -----------------------------------------------------------------------------------------------------------
HTML.append('<div class="scn" id="sa">')
head("ha", [[("An", ""), ("app", ""), ("that", ""), ("rates", "it")], [("your", ""), ("reel", ""), ("before", "it")], [("you", ""), ("post.", "")]], 190, "c00", 84)
HTML.append(f'<div class="chip glass" id="fixchip">{SH}tells you exactly <i>what to fix</i></div></div>')
scene("sa", SA, SB)
ft("#phone", .05, .9, "{opacity: 0, x: 0, y: 300, rotationX: 24, scale: .7}", "{opacity: 1, x: 0, y: -10, rotationX: 0, scale: .78}", "expo.out")
ft("#share", .45, .6, "{opacity: 0, y: 60, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "expo.out")
phone_shine(.6)
shine("#share", .9)
t_r = T("c00", "rates")
sfx("whoosh", t_r - .1)
t_p = T("c00", "post")
to("#share", t_p, .12, "{scale: .94}")
to("#share", t_p + .12, .35, "{scale: 1}", "elastic.out(1,.4)")
ft("#lk", t_p, .4, "{rotation: -18}", "{rotation: 0}", "elastic.out(1.2,.3)")
sfx("click", t_p)
t_f = T("c00", "exactly")
ft("#fixchip", t_f - .1, .55, "{opacity: 0, filter: 'blur(12px)', y: 30, scale: .9}", "{opacity: 1, filter: 'blur(0px)', y: 0, scale: 1}", "expo.out")
shine("#fixchip", t_f + .25)
sfx("pop", t_f)
tilt("#phone .scr", .9, SB)
head_out("ha", SB - .3)
to("#fixchip", SB - .3, .25, "{opacity: 0, filter: 'blur(12px)'}")

# ---- B contrast (dark): two equal glass cards, flat (no residual 3D tilt), text inside the cards -------------------------------
pts = " ".join(f"{i * 37},{120 - 60 * math.exp(-((i - 3) / 4) ** 2) - (i * 2)}" for i in range(11))
HTML.append('<div class="scn" id="sb">')
head("hb", [[("Not", ""), ("views", ""), ("after.", "it")], [("Reasons,", ""), ("before.", "it pk")]], 190, "c01", 92, dark=True)
HTML.append(f'<div class="card glass dkg" id="after">{SH}<div class="lab">AFTER YOU POST</div><div class="big">Views</div>'
            f'<svg viewBox="0 0 370 140" class="spark"><polyline points="{pts}"/></svg><div class="mut">numbers, no reasons</div></div>'
            f'<div class="card glass dkg pkc" id="before">{SH}<div class="lab pk">BEFORE YOU POST</div><div class="big">Reasons</div>'
            '<div class="rows"><span>Hook</span><span>Proof</span><span>Trust</span></div><div class="mut">with the exact second</div></div></div>')
scene("sb", SB, SC)
sweep(SB)
mode(SB, True)
to("#phone", SB - .2, .3, "{opacity: 0, scale: .7, filter: 'blur(10px)'}", "power2.in")
to("#share", SB - .2, .3, "{opacity: 0}")
t_v = T("c01", "views")
ft("#after", t_v - .15, .7, "{opacity: 0, x: -200, rotationY: 35, filter: 'blur(14px)'}", "{opacity: 1, x: 0, rotationY: 0, filter: 'blur(0px)'}", "expo.out")
shine("#after", t_v + .3)
tilt("#after", t_v + .6, T("c01", "reasons") - .1, 5, .8)
sfx("swish", t_v - .15)
t_re = T("c01", "reasons")
to("#after", t_re - .05, .5, "{opacity: .4, scale: .94, filter: 'grayscale(1) blur(2px)'}")
ft("#before", t_re - .1, .7, "{opacity: 0, x: 200, rotationY: -35, filter: 'blur(14px)', scale: .9}", "{opacity: 1, x: 0, rotationY: 0, filter: 'blur(0px)', scale: 1.03}", "expo.out")
shine("#before", t_re + .35)
tilt("#before", t_re + .65, SC, 5, .9)
ft("#before .rows span", t_re + .2, .45, "{opacity: 0, x: 40, filter: 'blur(8px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)', stagger: .09}", "expo.out")
sfx("whoosh", t_re - .1)
sfx("ding", T("c01", "before"))
head_out("hb", SC - .25)

# ---- C meet Creedom, it watches (light) ---------------------------------------------------------------------------------------
FS = (1, 4, 7, 10, 14)
strip = "".join(f'<div class="fr glass" id="fr{i}">{SH}<img src="assets/img/demo_f{t:02d}.jpg"><span>0:{t:02d}</span></div>' for i, t in enumerate(FS))
HTML.append(f'<div class="scn" id="sc"><div class="brand glass" id="brand">{SH}<img src="assets/img/creedom_logo.png"></div>')
head("hcc", [[("It's", ""), ("called", "")], [("Creedom.", "it pk")]], 210, "c02", 96)
head("hc", [[("It", ""), ("watches", ""), ("your", "")], [("whole", ""), ("reel,", "")], [("second", "it"), ("by", "it"), ("second.", "it")]], 190, "c02", 80,
     after=T("c02", "Creedom") + .2)
HTML.append(f'<div class="stat glass" id="stat">{SH}<i></i>WATCHING<b id="stt">0:00</b></div>'
            f'<div class="strip">{strip}</div><div class="beam" id="beam"></div></div>')
scene("sc", SC, SD)
liquid(SC)
zoom_through(SC)
mode(SC, False)
t_cr = T("c02", "Creedom")
ft("#brand", SC + .05, .6, "{opacity: 0, scale: .6, filter: 'blur(16px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "expo.out")
shine("#brand", t_cr + .05)
tilt("#brand", SC + .7, T("c02", "watches") - .2, 6, .8)
sfx("impact", t_cr)
t_w = T("c02", "watches")
to("#brand", t_w - .2, .4, "{opacity: 0, scale: 1.4, filter: 'blur(14px)'}", "power2.in")
head_out("hcc", T("c02", "It", 1) - .3)
# phone at x 390 (scale .7: 201..579 x 604..1276), status pill over it, the mascot holds his magnifier up to it on the right
ft("#phone", t_w - .2, .7, "{opacity: 0, x: -150, y: -60, scale: .6, filter: 'blur(12px)'}", "{opacity: 1, x: -150, y: -60, scale: .7, filter: 'blur(0px)'}", "expo.out")
phone_shine(t_w + .5)
ft("#stat", t_w, .55, "{opacity: 0, y: 30, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
shine("#stat", t_w + .4)
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 15, duration: {SD - .3 - (t_w + .3):.2f}, ease: "none", onUpdate: () => {{ '
   f'document.getElementById("stt").textContent = "0:" + String(Math.floor(o.v)).padStart(2, "0"); }}}}, {t_w + .3:.3f}); }})();')
ft("#beam", t_w + .3, 1.2, "{opacity: .95, y: 0}", "{opacity: .95, y: 630}", "sine.inOut")
to("#beam", t_w + 1.5, 1.2, "{y: 0}", "sine.inOut")
to("#beam", t_w + 2.7, .2, "{opacity: 0}")
t_s = T("c02", "second")
for i in range(len(FS)):
    t = t_s - .05 + .14 * i
    ft(f"#fr{i}", t, .6, "{opacity: 0, y: 80, scale: .7, filter: 'blur(10px)', rotationX: 50}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)', rotationX: 0}", "expo.out")
    shine(f"#fr{i}", t + .3, .6)
    sfx("shutter" if i % 2 == 0 else "tick", t)
ft("#fr4", T("c02", "viewer"), .4, "{boxShadow: '0 0 0px 0px rgba(243,67,162,0)'}", "{boxShadow: '0 0 50px 8px rgba(243,67,162,.6)'}", "power2.out")
head_out("hc", SD - .25)

# ---- D score + flags (dark): mascot left + gauge right in one band, the flag rail below ---------------------------------------
MARK = [("weak", "0:01", "Weak hook", "HOOK", "#F5B544", 1 / 15), ("claim", "0:07", "Claim, no proof", "PROOF", "#F5B544", 7 / 15),
        ("moment", "0:14", "Loses trust", "TRUST", MAG, 14 / 15)]
marks = "".join(f'<b class="mk" id="mk{i}" style="left:{p * 100:.3f}%;--c:{c}"></b>' for i, (_, ts, lab, tag, c, p) in enumerate(MARK))
ticks = "".join(f'<span style="left:{p * 100:.3f}%">0:{s:02d}</span>' for p, s in ((0, 0), (1 / 3, 5), (2 / 3, 10), (1, 15)))
rows = "".join(f'<div class="fl glass dkg" id="fl{i}" style="--c:{c}"><i></i><em>{ts}</em><span>{lab}</span><u>{tag}</u></div>'
               for i, (_, ts, lab, tag, c, p) in enumerate(MARK))
HTML.append('<div class="scn" id="sd">')
head("hd", [[("Scores", ""), ("it", "")], [("out", ""), ("of", ""), ("five.", "it pk")]], 190, "c03", 84, dark=True)
head("hd2", [[("Flags", ""), ("the", ""), ("exact", "")], [("moments.", "it pk")]], 190, "c03", 84, dark=True, after=T("c03", "flags") - .05)
HTML.append(f'<div class="gauge glass dkg" id="gauge"><i class="gsh"></i><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" class="gt"/>'
            '<circle cx="100" cy="100" r="84" class="gf" id="gf"/></svg><div class="gin"><div class="gv"><b id="gnum">0.0</b><span>/5</span></div>'
            '<div class="ex">EXAMPLE REEL</div></div></div>'
            f'<div class="rail glass dkg" id="rail">{SH}<div class="rl"><i id="ph"></i>{marks}</div><div class="tk">{ticks}</div>'
            f'<div class="rws">{rows}</div></div></div>')
scene("sd", SD, SE)
sweep(SD)
mode(SD, True)
for b in ["#phone", "#stat", "#beam"] + [f"#fr{i}" for i in range(len(FS))]:
    to(b, SD - .25, .2, "{opacity: 0}")
t_sc = T("c03", "scores")
ft("#gauge", t_sc - .1, .7, "{opacity: 0, scale: .7, filter: 'blur(14px)', rotation: -20}", "{opacity: 1, scale: 1, filter: 'blur(0px)', rotation: 0}", "expo.out")
ft("#gf", t_sc + .2, 1.1, "{strokeDashoffset: 528}", f"{{strokeDashoffset: {528 * (1 - 4.2 / 5):.0f}}}", "power2.out")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 4.2, duration: 1.1, ease: "power2.out", onUpdate: () => {{ document.getElementById("gnum").textContent = o.v.toFixed(1); }}}}, {t_sc + .2:.3f}); }})();')
js(f'tl.fromTo(".gsh", {{rotation: 0}}, {{rotation: 360, duration: 3.2, ease: "none", repeat: 1, immediateRender: false}}, {t_sc:.3f});')
tilt("#gauge", t_sc + .7, SE, 7, 1.1)
sfx("riser_short", t_sc)
sfx("impact", t_sc + 1.3)
t_fl = T("c03", "flags")
head_out("hd", t_fl - .25)
ft("#rail", t_fl, .7, "{opacity: 0, y: 120, filter: 'blur(14px)', rotationX: 30}", "{opacity: 1, y: 0, filter: 'blur(0px)', rotationX: 0}", "expo.out")
shine("#rail", t_fl + .4, 1.1)
sfx("swish", t_fl)
for i, (w, ts, lab, tag, c, p) in enumerate(MARK):
    t = T("c03", w, 1 if w == "moment" else 0) - .05
    to("#ph", t, .35, f"{{left: '{p * 100:.3f}%'}}", "power3.inOut")
    ft(f"#mk{i}", t + .1, .5, "{opacity: 0, y: -120, scale: .4}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.4)")
    ft(f"#mk{i}", t + .5, .6, "{boxShadow: '0 0 0px 0px rgba(255,255,255,0)'}", f"{{boxShadow: '0 0 34px 8px {c}'}}", "power2.out")
    ft(f"#fl{i}", t + .2, .55, "{opacity: 0, x: -60, filter: 'blur(10px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)'}", "expo.out")
    sfx("pop", t + .15)

# ---- E the fix card (dark) --------------------------------------------------------------------------------------------------
HTML.append(f'<div class="scn" id="se"><div class="fix glass dkg" id="fix">{SH}<div class="ft"><b>0:14</b><span>Loses trust</span></div>'
            '<div class="fl2">The tool is never named, so viewers can\'t follow along.</div>'
            '<div class="fx"><i>FIX</i>Name the tool on screen at 0:14.</div></div>')
head("he", [[("With", ""), ("the", ""), ("timestamp,", "")], [("and", ""), ("the", ""), ("fix.", "it pk")]], 190, "c04", 88, dark=True)
HTML.append('</div>')
scene("se", SE, SF)
liquid(SE)
for b in ("#rail", "#gauge"):
    to(b, SE - .2, .3, "{opacity: 0, filter: 'blur(12px)'}")
ft("#fix", SE + .05, .8, "{opacity: 0, scale: .5, y: 300, rotationX: 40, filter: 'blur(18px)'}", "{opacity: 1, scale: 1, y: 0, rotationX: 0, filter: 'blur(0px)'}", "expo.out")
shine("#fix", SE + .55, 1.0)
tilt("#fix", SE + .85, SF, 5, .9)
sfx("whoosh_big", SE)
ft("#fix .fx", T("c04", "fix") - .05, .5, "{opacity: 0, x: -60, filter: 'blur(10px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)'}", "expo.out")
sfx("ding", T("c04", "fix"))
head_out("he", SF - .25)
to("#fix", SF - .25, .3, "{opacity: 0, scale: 1.2, filter: 'blur(16px)'}", "power2.in")

# ---- F fix it before anyone sees it (light): the hook layout again, now fixed --------------------------------------------------
HTML.append('<div class="scn" id="sf">')
head("hf", [[("Fix", ""), ("it", ""), ("before", "it")], [("anyone", ""), ("sees", ""), ("it.", "")]], 190, "c05", 88)
HTML.append(f'<div class="ok glass" id="ok">{SH}<i>&#10003;</i>0:14 fixed</div></div>')
scene("sf", SF, SG)
liquid(SF)
mode(SF, False)
ft("#phone", SF + .05, .7, "{opacity: 0, x: 0, y: -10, scale: .7, filter: 'blur(14px)'}", "{opacity: 1, x: 0, y: -10, scale: .78, filter: 'blur(0px)'}", "expo.out")
ft("#share", SF + .1, .5, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "expo.out")
t_fx2 = T("c05", "fix")
ft("#tool", t_fx2, .55, "{opacity: 0, scale: .6, filter: 'blur(10px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "back.out(2)")
shine("#tool", t_fx2 + .3, .7)
ft("#ok", t_fx2 + .15, .55, "{opacity: 0, y: 30, filter: 'blur(12px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
shine("#ok", t_fx2 + .5)
sfx("notify", t_fx2 + .1)
phone_shine(t_fx2 + .2)
t_sees = T("c05", "sees")
to("#lk", t_sees - .1, .35, "{rotation: 24, y: -10, opacity: 0}", "back.in(2)")
to("#share", t_sees, .4, f"{{background: 'linear-gradient(135deg, {PINK}, {MAG})', color: '#fff', scale: 1.08, boxShadow: '0 20px 60px rgba(243,67,162,.55)'}}", "back.out(2)")
st("#shtx", t_sees, '{textContent: "Post it"}')
shine("#share", t_sees + .2)
sfx("success", t_sees)
tilt("#phone .scr", SF + .7, SG, 4, 1.2)
head_out("hf", SG - .25)
for b in ("#phone", "#share", "#ok"):
    to(b, SG - .25, .3, "{opacity: 0, filter: 'blur(12px)'}")

# ---- G CTA (dark) ---------------------------------------------------------------------------------------------------------------
HTML.append(f'<div class="scn" id="sg"><div class="dm glass dkg" id="dm">{SH}<img src="assets/img/creedom_logo.png"><div><b>Creedom</b><span>sent you the link</span></div><em>now</em></div>'
            '<div class="cm" id="cmh">Comment</div><div class="kw" id="kw">CHECK</div>'
            f'<div class="cbox glass dkg" id="cbox">{SH}<i></i><span id="ctx">Add a comment…</span><b id="csend">&#10148;</b></div>'
            '<div class="sub" id="sub">and I\'ll send you the <i>link.</i></div></div>')
scene("sg", SG, DUR + 1)
sweep(SG)
mode(SG, True)
t_c = T("c06", "Comment")
ft("#cmh", t_c - .05, .5, "{opacity: 0, filter: 'blur(14px)', y: 30}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
t_k = T("c06", "Check")
ft("#kw", t_k - .1, .8, "{opacity: 0, scale: 1.6, scaleX: 1.9, filter: 'blur(24px)'}", "{opacity: 1, scale: 1, scaleX: 1, filter: 'blur(0px)'}", "expo.out")
sfx("impact", t_k)
ft("#cbox", t_k + .3, .5, "{opacity: 0, y: 60, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
shine("#cbox", t_k + .55)
t_ty = t_k + .55
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 5, duration: .45, ease: "steps(5)", onUpdate: () => {{ const e = document.getElementById("ctx"); '
   f'e.textContent = "CHECK".slice(0, Math.round(o.n)) || "Add a comment…"; e.style.color = o.n > 0 ? "#fff" : "rgba(255,255,255,.5)"; }}}}, {t_ty:.3f}); }})();')
for k in range(5):
    sfx("tick", t_ty + .09 * k)
to("#csend", t_ty + .5, .12, "{scale: 1.3}")
to("#csend", t_ty + .62, .15, "{scale: 1}")
sfx("click", t_ty + .5)
ft("#sub", T("c06", "send") - .05, .5, "{opacity: 0, filter: 'blur(12px)', y: 20}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
t_dm = T("c06", "link")
ft("#dm", t_dm - .1, .7, "{opacity: 0, y: -160, scale: .9, filter: 'blur(12px)'}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)'}", "expo.out")
shine("#dm", t_dm + .35)
sfx("notify", t_dm)
tilt("#cbox", t_ty + .8, DUR, 4, 1.0)


# ---- the Creedom mascot (not a bird): he performs every line, like in the Creedom reel-analyser reel -------------------------------
def star(sz, col=PINK):
    return (f'<svg viewBox="-50 -50 100 100" width="{sz}" height="{sz}"><path d="M0 -50 C6 -10 10 -6 50 0 C10 6 6 10 '
            f'0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z" fill="{col}"/></svg>')


HTML.append(f'<div id="birdlayer">{bird.rig(star)}</div>')
b = bird.Bird(js)
js(f'tl.set("#birdpos",{{x:1250,y:{MASCOT_R[1]},scale:{MASCOT_R[2]}}},0);tl.set("#bflip",{{scaleX:-1}},0);')
js('tl.set("#sweat,#mag,.bub,.bsp,#cloud",{opacity:0,scale:.5},0);tl.set("#wingR,#footK",{opacity:0},0);')
for k in "LR":
    cx, cy, r = bird.EYES[k][:3]
    js(f'tl.set("#lu{k}",{{scaleY:0,svgOrigin:"{cx} {cy - r - 6}"}},0);tl.set("#ld{k}",{{scaleY:0,svgOrigin:"{cx} {cy + r + 6}"}},0);')
b.facing = -1
# always alive under every gesture (the reel-analyser loops: bob, sway, breath, arms swinging a little, weight shifts)
js(f'tl.to("#bidle",{{y:-7,duration:.42,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .42) - 1}}},0);')
js(f'tl.fromTo("#bidle",{{rotation:-2.5}},{{rotation:2.5,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.3) - 1}}},0);')
js(f'tl.to("#bbreath",{{scaleY:1.012,scaleX:.994,duration:.8,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .8) - 1}}},0);')
js(f'tl.fromTo("#wingLi",{{rotation:3}},{{rotation:-4,duration:.6,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .6) - 1}}},0);')
js(f'tl.fromTo("#wingDi",{{rotation:-3}},{{rotation:4,duration:.6,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .6) - 1}}},.3);')
js(f'tl.fromTo("#footLi",{{rotation:0,y:0}},{{rotation:-7,y:-4,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.3) - 1}}},0);')
js(f'tl.fromTo("#footRi",{{rotation:-7,y:-4}},{{rotation:0,y:0,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.3) - 1}}},0);')
js(f'tl.fromTo("#wingRi",{{rotation:-4}},{{rotation:8,duration:.45,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .45) - 1}}},0);')
js('tl.set("#bshadow",{opacity:0},0);tl.to("#bshadow",{opacity:1,duration:.3},.6);')


def sparkle(t, d=1.0, rot=120):
    b.show(".bsp", t)
    js(f'tl.to(".bsp",{{rotation:"+={rot}",duration:{d},ease:"none"}},{t:.3f});')
    b.show(".bsp", t + d, False)
    sfx("pop", t)


def bubble(sel, t, d=.8):
    b.show(sel, t)
    b.show(sel, t + d, False)
    sfx("pop", t)


# A: walks in from the right, studies the phone through his glass magnifier, jumps at "post", points, nods, winks
b.expr(0, "curious", .01)
b.at(.1, MASCOT_R[0], MASCOT_R[1], MASCOT_R[2], .9, "power1.out")
b.walk(.1, .9)
b.look(.2, 14, -4)
b.blink(.75)
t_r = T("c00", "rates")
b.expr(t_r, "focused", .2)
b.pose(t_r, "leanin", .3)
b.show("#mag", t_r)
js(f'tl.fromTo("#mag",{{rotation:0,y:0}},{{rotation:-14,y:-40,duration:.45,ease:"sine.inOut",yoyo:true,repeat:1}},{t_r + .05:.3f});')
b.look(t_r, 16, -10)
t_p = T("c00", "post")
b.show("#mag", t_p - .12, False)
b.pose(t_p - .1, "tall", .15)
b.expr(t_p, "excited", .12)
b.hop(t_p + .05, 80)
b.kick(t_p + .05, .55)
b.pulse_overlay(t_p + .15, "str", 3)
bubble(".bx", t_p + .05, .7)
b.pose(T("c00", "and") + .1, "neutral", .2)
t_tl = T("c00", "tells")
b.expr(t_tl, "curious", .15)
b.look(t_tl, 16, 16)
b.point(t_tl, 1.0)
t_x = T("c00", "exactly")
b.expr(t_x + .25, "smile", .15)
b.nod(t_x + .3, 2)
t_fix = T("c00", "fix")
b.expr(t_fix, "wink", .12)
sparkle(t_fix, .9)

# B (dark): unimpressed by views after you post (shrug, head shake, "?"), thrilled by reasons before (jump, star eyes)
b.at(SB - .2, 390, 1230, .9, .55, "power2.inOut")
b.walk(SB - .2, .55)
b.face(SB + .4, 1)
t_vw = T("c01", "views")
b.expr(t_vw, "skeptical", .2)
b.look(t_vw, -14, -18)
b.pose(t_vw, "leanback", .3)
b.spread(T("c01", "after") + .05, 55, .18)
b.shake(T("c01", "after") + .15, 3, 9)
bubble(".bq", T("c01", "after"), .9)
b.spread(T("c01", "post") + .3, 0, .2)
t_re2 = T("c01", "Reasons")
b.pose(t_re2 - .05, "neutral", .15)
b.expr(t_re2 - .05, "shock", .1)
b.startle(t_re2 - .05)
b.look(t_re2, 14, -18)
b.expr(t_re2 + .25, "excited", .12)
b.hop(t_re2 + .3, 90)
b.kick(t_re2 + .3, .6)
b.pulse_overlay(t_re2 + .4, "str", 3)
sparkle(t_re2 + .35, 1.0, 140)
b.expr(T("c01", "before") + .5, "joy", .15)
b.blink(5.9)

# C: introduces Creedom with a jump and a spin under the logo, waves; then scans the reel with his magnifier
b.at(SC - .2, 390, 1100, 1.0, .5, "power2.inOut")
b.look(SC + .2, 0, -18)
b.expr(T("c02", "called"), "curious", .15)
t_cr2 = T("c02", "Creedom")
b.expr(t_cr2, "joy", .12)
b.pose(t_cr2, "tall", .15)
b.hop(t_cr2 + .05, 120)
b.spin(t_cr2 + .05)
sparkle(t_cr2 + .1, 1.1, 160)
b.wave(t_cr2 + .55, 2)
b.pose(t_cr2 + .6, "neutral", .2)
t_wt = T("c02", "watches")
b.face(t_wt - .3, 1)
b.at(t_wt - .25, 650, 960, .9, .5, "power2.inOut")
b.walk(t_wt - .25, .5)
b.face(t_wt + .28, -1)
b.expr(t_wt + .1, "focused", .2)
b.pose(t_wt + .2, "leanin", .3)
b.show("#mag", t_wt + .15)
js(f'tl.fromTo("#mag",{{y:-150,rotation:-10}},{{y:40,rotation:-18,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1,immediateRender:false}},{t_wt + .3:.3f});')
b.look(t_wt + .3, 18, -16)
b.look(t_wt + .9, 18, 2)
b.look(t_wt + 1.5, 18, 14)
b.look(t_wt + 2.1, 18, -8)
b.show("#mag", T("c02", "second") - .1, False)
b.pose(T("c02", "second") - .1, "neutral", .2)
t_s2 = T("c02", "second")
b.expr(t_s2, "curious", .15)
for i in range(5):
    b.look(t_s2 + .14 * i, 20 - 9 * i, 18)      # follows the frames as they land, left to right (he faces left)
b.tap(t_s2 + .1, 4)
t_vr = T("c02", "real")
b.expr(t_vr, "smile", .15)
b.nod(t_vr + .05, 2)
b.blink(SD - .4)

# D (dark): counts along with the score, jumps with heart eyes; then reads the flags: scratches his head, wags a
# finger, and gets a fright (sweat, "!") at "loses trust"
b.at(SD - .25, 150, 574, .9, .55, "power2.inOut")
b.walk(SD - .25, .55)
b.face(SD + .35, 1)
b.expr(t_sc, "curious", .15)
b.pose(t_sc, "leanin", .3)
b.look(t_sc, 16, -4)
b.tap(t_sc + .15, 5)
t_land = t_sc + 1.3
b.expr(t_land, "love", .12)
b.pose(t_land, "tall", .15)
b.hop(t_land, 110)
b.kick(t_land, .6)
b.pulse_overlay(t_land + .1, "hrt", 3)
sparkle(t_land + .05, 1.0)
b.expr(t_fl + .5, "joy", .15)
b.pose(t_fl + .5, "neutral", .2)
b.look(t_fl + .6, 12, 18)
b.expr(t_fl + 1.0, "focused", .2)
b.blink(15.6)
t_wk = T("c03", "weak")
b.expr(t_wk, "skeptical", .15)
b.scratch(t_wk + .05, .9)
bubble(".bq", t_wk + .1, .8)
t_cl = T("c03", "claim")
b.expr(t_cl, "annoyed", .15)
b.shake(t_cl + .05, 2, 8)
b.look(t_cl, 14, 18)
b.point(t_cl + .5, .7)
t_tr = T("c03", "loses")
b.expr(t_tr, "shock", .1)
b.startle(t_tr)
b.spread(t_tr, 50, .12)
b.spread(t_tr + .45, 0, .2)
bubble(".bx", t_tr + .05, .7)
b.show("#sweat", t_tr + .05)
js(f'tl.to("#sweat",{{y:40,duration:.8,ease:"power1.in"}},{t_tr + .15:.3f});')
b.show("#sweat", t_tr + .75, False)
b.expr(t_tr + .4, "sad", .2)

# E: reads the fix card with his magnifier, then a proud nod at "the fix" and a little hop
b.at(SE - .2, 390, 1090, .9, .45, "power2.inOut")
b.expr(SE + .1, "curious", .15)
b.look(SE + .1, 0, -18)
b.show("#mag", SE + .2)
js(f'tl.fromTo("#mag",{{y:-60,rotation:-8}},{{y:-130,rotation:-16,duration:.5,ease:"sine.inOut",yoyo:true,repeat:1,immediateRender:false}},{SE + .25:.3f});')
b.expr(SE + .3, "focused", .2)
t_fx = T("c04", "fix")
b.show("#mag", t_fx - .15, False)
b.expr(t_fx, "proud", .15)
b.pose(t_fx, "tall", .2)
b.nod(t_fx + .05, 1)
b.hop(t_fx + .35, 50)

# F: back beside the phone; points at the fixed reel, watches Share unlock, then celebrates with a jump and a kick
b.at(SF - .2, *MASCOT_R, .45, "power2.inOut")
b.walk(SF - .2, .45)
b.face(SF + .27, -1)
b.pose(SF, "neutral", .2)
b.expr(SF + .2, "curious", .15)
b.look(SF + .2, 16, -6)
b.expr(t_fx2, "excited", .12)
b.point(t_fx2 + .05, .9)
b.look(T("c05", "anyone"), 16, 16)
b.expr(T("c05", "anyone"), "hopeful", .15)
b.expr(t_sees, "joy", .12)
b.hop(t_sees + .05, 100)
b.kick(t_sees + .05, .6)
sparkle(t_sees + .1, 1.0, -140)
b.blink(SG - .5)

# G: walks to centre stage, cheers at CHECK, chatters while the comment types, heart eyes, waves goodbye, winks
b.at(SG - .2, 390, 1200, .95, .55, "power2.inOut")
b.walk(SG - .2, .55)
b.face(SG + .4, 1)
b.look(SG + .45, 0, -18)
b.expr(t_k, "excited", .12)
b.hop(t_k + .05, 80)
b.spread(t_k + .05, 55, .15)
b.spread(t_k + .5, 0, .2)
b.talk(t_ty, .6)
b.look(t_ty, 0, -10)
b.expr(T("c06", "send"), "love", .15)
b.pulse_overlay(T("c06", "send") + .1, "hrt", 3)
b.wave(t_dm + .05, 2)
b.expr(DUR - .5, "wink", .12)
b.hist.sort(key=lambda h: h[0])
for t in (3.6, 9.6, 14.9, 17.9, 22.4, 24.9):
    b.blink(t)

# ---- fluid blobs and drifting glass panes --------------------------------------------------------------------------------------
LB = [(-200, -150, 760, "rgba(238,104,139,.55)"), (520, 260, 820, "rgba(255,190,214,.75)"), (-260, 980, 900, "rgba(217,194,255,.6)"),
      (480, 1280, 820, "rgba(255,216,194,.6)")]
DB = [(-220, -120, 800, "rgba(177,71,107,.55)"), (480, 900, 900, "rgba(243,67,162,.38)"), (-200, 1300, 760, "rgba(120,40,200,.35)")]
blobs_l = "".join(f'<i class="bl" id="lb{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(LB))
blobs_d = "".join(f'<i class="bl" id="db{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(DB))
for i in range(len(LB)):
    js(f'tl.fromTo("#lb{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
       f'duration: {DUR / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, 0);')
for i in range(len(DB)):
    js(f'tl.fromTo("#db{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
       f'duration: {DUR / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, 0);')
# big frosted panes, mostly off-frame at the edges, drifting and turning slowly (glass, not bubbles)
PANES = [(-300, 330, 560, 340, -18), (830, 1500, 600, 360, 16), (690, -170, 520, 300, 24), (-330, 1560, 600, 320, -10)]
panes = "".join(f'<i class="pane" id="pn{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>' for i, (x, y, w, h, r) in enumerate(PANES))
for i, (x, y, w, h, r) in enumerate(PANES):
    js(f'tl.fromTo("#pn{i}", {{rotation: {r}, x: 0, y: 0}}, {{rotation: {r + random.choice((-1, 1)) * random.randint(8, 14)}, x: {random.randint(-80, 80)}, '
       f'y: {random.randint(-120, 120)}, duration: {DUR / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, 0);')

CSS = f"""
@font-face {{ font-family: Inter; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #fbf7f9; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: {INK}; background: #fbf7f9; }}
.world {{ position: absolute; inset: 0; overflow: hidden; }}
#light {{ background: radial-gradient(120% 90% at 50% 30%, #ffffff 0%, #fbf3f6 55%, #f6e9ef 100%); }}
#dark {{ background: radial-gradient(110% 80% at 50% 70%, #1a0912 0%, #0a0609 55%, #050405 100%); opacity: 0; }}
.bl {{ position: absolute; border-radius: 50%; filter: blur(90px); }}
#panes {{ position: absolute; inset: 0; pointer-events: none; }}
.pane {{ position: absolute; border-radius: 70px; background: linear-gradient(135deg, rgba(255,255,255,.34), rgba(255,255,255,.06) 60%, rgba(255,255,255,.14));
  backdrop-filter: blur(24px) saturate(1.5); -webkit-backdrop-filter: blur(24px) saturate(1.5); border: 1.5px solid rgba(255,255,255,.45);
  box-shadow: inset 0 2px 0 rgba(255,255,255,.6), 0 30px 80px rgba(120,20,60,.10); }}
#grain {{ position: absolute; inset: 0; opacity: .045; background: url(assets/img/grain.png); mix-blend-mode: overlay; pointer-events: none; }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 46%; }}
#drift {{ position: absolute; inset: 0; transform-origin: 50% 50%; perspective: 1600px; }}
.scn {{ position: absolute; inset: 0; opacity: 0; perspective: 1600px; }}
#sweep {{ position: absolute; top: -10%; bottom: -10%; left: 0; width: 70%; z-index: 50; pointer-events: none;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.28) 30%, rgba(255,255,255,.42) 50%, rgba(255,255,255,.28) 70%, rgba(255,255,255,0));
  backdrop-filter: blur(28px) saturate(1.6); -webkit-backdrop-filter: blur(28px) saturate(1.6); border-left: 2px solid rgba(255,255,255,.7); border-right: 2px solid rgba(255,255,255,.5); }}
#liq {{ position: absolute; left: 50%; top: 50%; width: 520px; height: 520px; margin: -260px 0 0 -260px; z-index: 49; pointer-events: none; opacity: 0; border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, rgba(255,255,255,.75) 0, rgba(255,255,255,.28) 22%, rgba(255,214,230,.22) 60%, rgba(243,67,162,.22) 100%);
  backdrop-filter: blur(26px) saturate(1.9) brightness(1.06); -webkit-backdrop-filter: blur(26px) saturate(1.9) brightness(1.06);
  border: 2px solid rgba(255,255,255,.8); box-shadow: inset -30px -40px 80px rgba(243,67,162,.28), inset 20px 26px 60px rgba(255,255,255,.55); }}
/* glass */
.glass {{ background: linear-gradient(135deg, rgba(255,255,255,.62), rgba(255,255,255,.22)); backdrop-filter: blur(26px) saturate(1.7); -webkit-backdrop-filter: blur(26px) saturate(1.7);
  border: 1.5px solid rgba(255,255,255,.85); box-shadow: inset 0 1.5px 0 rgba(255,255,255,.95), inset 0 -18px 40px rgba(255,255,255,.18), 0 30px 80px rgba(120,20,60,.18);
  overflow: hidden; }}
.glass.dkg {{ background: linear-gradient(135deg, rgba(255,255,255,.16), rgba(255,255,255,.04)); border: 1.5px solid rgba(255,255,255,.26); color: #fff;
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,.35), inset 0 -18px 40px rgba(255,255,255,.04), 0 30px 90px rgba(0,0,0,.5); }}
.sh {{ position: absolute; top: -30%; bottom: -30%; left: 0; width: 30%; pointer-events: none; opacity: 0; z-index: 5;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55) 50%, rgba(255,255,255,0)); mix-blend-mode: soft-light; }}
.dkg > .sh {{ background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.22) 50%, rgba(255,255,255,0)); mix-blend-mode: normal; }}
/* headlines: centred */
.head {{ position: absolute; left: 60px; right: 60px; font-weight: 700; letter-spacing: -.035em; line-height: 1.04; z-index: 20; text-align: center; }}
.hl {{ white-space: nowrap; }}
.head.dk {{ color: #fff; }}
.hw {{ display: inline-block; opacity: 0; }}
.hw.it {{ font-family: Serif; font-style: italic; font-weight: 400; letter-spacing: -.01em; font-size: 1.12em; color: {ROSE}; padding-right: .04em; }}
.head.dk .hw.it {{ color: #ffb3cd; }}
.hw.pk {{ background: linear-gradient(90deg, {PINK}, {MAG}); -webkit-background-clip: text; background-clip: text; color: transparent !important; }}
/* phone */
.phone {{ position: absolute; left: 270px; top: 520px; width: 540px; height: 960px; border-radius: 74px; padding: 14px; z-index: 10; opacity: 0;
  background: linear-gradient(150deg, rgba(255,255,255,.9), rgba(230,210,220,.5) 40%, rgba(255,255,255,.75)); box-shadow: 0 50px 120px rgba(120,20,60,.3), inset 0 2px 0 #fff;
  transform-origin: 50% 50%; }}
.scr {{ position: relative; width: 100%; height: 100%; border-radius: 62px; overflow: hidden; background: #111; }}
.dv {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.isl {{ position: absolute; left: 50%; top: 32px; width: 150px; height: 42px; margin-left: -75px; border-radius: 30px; background: #000; }}
.ig {{ position: absolute; inset: 0; }}
.ig .cap {{ position: absolute; left: 30px; right: 30px; top: 300px; text-align: center; font-weight: 800; font-size: 44px; color: #fff; line-height: 1.1;
  text-shadow: 0 4px 20px rgba(0,0,0,.5); }}
.ig .tool {{ position: absolute; left: 50%; top: 380px; width: 380px; margin-left: -190px; padding: 16px 0; border-radius: 999px; text-align: center; font-weight: 700; font-size: 36px;
  color: {INK}; opacity: 0; }}
.ig .tool b {{ color: {MAG}; }}
.ig .side {{ position: absolute; right: 24px; bottom: 190px; display: flex; flex-direction: column; gap: 30px; }}
.ig .side svg {{ display: block; width: 46px; height: 46px; fill: none; stroke: #fff; stroke-width: 2; stroke-linejoin: round; filter: drop-shadow(0 2px 6px rgba(0,0,0,.5)); }}
.ig .who {{ position: absolute; left: 26px; bottom: 60px; display: flex; align-items: center; gap: 12px; color: #fff; font-weight: 700; font-size: 26px; text-shadow: 0 2px 8px rgba(0,0,0,.5); }}
.ig .who b {{ width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, {MAG}); border: 2px solid #fff; }}
.glint {{ position: absolute; inset: 0; background: linear-gradient(115deg, rgba(255,255,255,.22) 0%, rgba(255,255,255,0) 28%, rgba(255,255,255,0) 70%, rgba(255,255,255,.12) 100%); pointer-events: none; }}
.pshine {{ position: absolute; top: -20%; bottom: -20%; left: 0; width: 34%; opacity: 0; pointer-events: none;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.35) 50%, rgba(255,255,255,0)); }}
.share {{ position: absolute; left: 50%; top: 1500px; width: 340px; height: 100px; margin-left: -170px; border-radius: 60px; display: flex; align-items: center; justify-content: center;
  gap: 18px; font-weight: 700; font-size: 42px; z-index: 11; opacity: 0; }}
.share svg {{ width: 42px; height: 42px; fill: none; stroke: currentColor; stroke-width: 2.4; }}
.chip {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: 640px; top: 1392px; height: 84px; border-radius: 999px; display: flex; align-items: center;
  justify-content: center; gap: 12px; font-weight: 600; font-size: 36px; z-index: 20; opacity: 0; }}
.chip i {{ font-family: Serif; font-weight: 400; font-size: 1.18em; color: {ROSE}; }}
/* B cards: equal, side by side, centred (70..520 and 560..1010) */
.card {{ position: absolute; top: 520px; width: 450px; height: 570px; border-radius: 44px; padding: 40px 38px; z-index: 12; opacity: 0; }}
#after {{ left: 70px; }} #before {{ left: 560px; }}
.card.pkc {{ border-color: rgba(243,67,162,.6); box-shadow: inset 0 1.5px 0 rgba(255,255,255,.35), 0 0 80px rgba(243,67,162,.35), 0 30px 90px rgba(0,0,0,.5); }}
.lab {{ font-family: Mono; font-size: 22px; letter-spacing: .14em; color: rgba(255,255,255,.6); }}
.lab.pk {{ color: #ff9cc0; }}
.big {{ font-weight: 700; font-size: 72px; letter-spacing: -.03em; margin: 16px 0 28px; }}
.spark {{ width: 100%; height: 150px; overflow: visible; }}
.spark polyline {{ fill: none; stroke: rgba(255,255,255,.55); stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; }}
.mut {{ position: absolute; left: 38px; right: 38px; bottom: 38px; font-family: Serif; font-style: italic; font-size: 36px; color: rgba(255,255,255,.62); white-space: nowrap; }}
.rows {{ display: flex; flex-direction: column; gap: 16px; }}
.rows span {{ display: block; padding: 15px 22px; border-radius: 18px; background: rgba(243,67,162,.16); border: 1px solid rgba(243,67,162,.4); font-weight: 600; font-size: 32px; }}
/* C */
.brand {{ position: absolute; left: 50%; top: 600px; width: 620px; height: 200px; margin-left: -310px; border-radius: 100px; display: flex; align-items: center; justify-content: center;
  z-index: 25; opacity: 0; }}
.brand img {{ height: 92px; }}
.stat {{ position: absolute; left: 215px; top: 514px; width: 350px; height: 64px; border-radius: 999px; display: flex; align-items: center; gap: 14px; padding: 0 26px;
  font-family: Mono; font-size: 22px; letter-spacing: .14em; color: {ROSE}; z-index: 14; opacity: 0; }}
.stat > i {{ width: 14px; height: 14px; border-radius: 50%; background: {MAG}; box-shadow: 0 0 12px {MAG}; }}
.stat b {{ margin-left: auto; color: {INK}; letter-spacing: .04em; font-size: 26px; }}
.strip {{ position: absolute; left: 118px; top: 1310px; display: flex; gap: 16px; z-index: 12; perspective: 1200px; }}
.fr {{ width: 156px; padding: 8px; border-radius: 22px; opacity: 0; }}
.fr img {{ display: block; width: 140px; height: 190px; object-fit: cover; border-radius: 15px; }}
.fr span {{ display: block; text-align: center; font-family: Mono; font-size: 22px; margin: 8px 0 2px; color: {ROSE}; }}
.beam {{ position: absolute; left: 215px; top: 622px; width: 350px; height: 8px; border-radius: 6px; z-index: 14; opacity: 0;
  background: linear-gradient(90deg, transparent, {MAG}, #fff, {MAG}, transparent); box-shadow: 0 0 40px 10px rgba(243,67,162,.5); }}
/* D: mascot left (150..450), gauge right (600..1000) in the band 490..890; rail 60..1020 x 960..1422 */
.gauge {{ position: absolute; left: 600px; top: 490px; width: 400px; height: 400px; border-radius: 50%; z-index: 12; opacity: 0; }}
.gsh {{ position: absolute; inset: 0; border-radius: 50%; background: conic-gradient(from 0deg, rgba(255,255,255,0) 0 62%, rgba(255,255,255,.22) 72%, rgba(255,255,255,0) 82%); }}
.gauge svg {{ position: absolute; inset: 18px; width: 364px; height: 364px; transform: rotate(-90deg); }}
.gt {{ fill: none; stroke: rgba(255,255,255,.12); stroke-width: 12; }}
.gf {{ fill: none; stroke: {PINK}; stroke-width: 12; stroke-linecap: round; stroke-dasharray: 528; stroke-dashoffset: 528; filter: drop-shadow(0 0 10px {MAG}); }}
.gin {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.gv {{ display: flex; align-items: baseline; justify-content: center; line-height: 1; padding-top: 10px; }}
.gv b {{ font-weight: 700; font-size: 118px; letter-spacing: -.04em; font-variant-numeric: tabular-nums; }}
.gv span {{ font-family: Serif; font-style: italic; font-size: 64px; color: #ffb3cd; margin-left: 6px; }}
.ex {{ margin-top: 14px; font-family: Mono; font-size: 17px; letter-spacing: .22em; color: rgba(255,255,255,.55); }}
.rail {{ position: absolute; left: 60px; right: 60px; top: 960px; height: 462px; border-radius: 40px; z-index: 12; opacity: 0; }}
.rl {{ position: absolute; left: 56px; right: 56px; top: 64px; height: 10px; border-radius: 8px; background: linear-gradient(90deg, rgba(255,255,255,.32), rgba(255,255,255,.12)); }}
.rl #ph {{ position: absolute; left: 0; top: -21px; width: 4px; height: 52px; margin-left: -2px; background: #fff; border-radius: 2px; box-shadow: 0 0 20px #fff; }}
.mk {{ position: absolute; top: -12px; width: 34px; height: 34px; margin-left: -17px; border-radius: 50%; background: var(--c); border: 3px solid #fff; opacity: 0; }}
.tk {{ position: absolute; left: 56px; right: 56px; top: 104px; height: 22px; font-family: Mono; font-size: 19px; color: rgba(255,255,255,.45); }}
.tk span {{ position: absolute; top: 0; transform: translateX(-50%); }}
.rws {{ position: absolute; left: 40px; right: 40px; top: 156px; display: flex; flex-direction: column; gap: 14px; }}
.fl {{ height: 84px; border-radius: 24px; display: flex; align-items: center; gap: 22px; padding: 0 28px; opacity: 0; }}
.fl > i {{ width: 22px; height: 22px; border-radius: 50%; background: var(--c); box-shadow: 0 0 14px var(--c); flex: none; }}
.fl em {{ font-style: normal; font-family: Mono; font-size: 28px; color: rgba(255,255,255,.75); width: 74px; flex: none; }}
.fl span {{ font-weight: 600; font-size: 36px; }}
.fl u {{ text-decoration: none; margin-left: auto; font-family: Mono; font-size: 18px; letter-spacing: .16em; color: var(--c); padding: 8px 14px; border-radius: 12px;
  border: 1px solid var(--c); }}
/* E */
.fix {{ position: absolute; left: 80px; right: 80px; top: 470px; border-radius: 48px; padding: 46px 50px 50px; z-index: 12; opacity: 0;
  border-color: rgba(243,67,162,.55); box-shadow: inset 0 1.5px 0 rgba(255,255,255,.35), 0 0 120px rgba(243,67,162,.35), 0 40px 100px rgba(0,0,0,.55); }}
.fix .ft {{ display: flex; align-items: baseline; gap: 22px; }}
.fix .ft b {{ font-weight: 700; font-size: 110px; letter-spacing: -.04em; line-height: 1; }}
.fix .ft span {{ font-family: Serif; font-style: italic; font-size: 64px; color: #ff9cc0; }}
.fix .fl2 {{ font-weight: 500; font-size: 40px; line-height: 1.3; color: rgba(255,255,255,.75); margin: 24px 0 30px; }}
.fix .fx {{ display: flex; align-items: center; gap: 20px; padding: 24px 28px; border-radius: 28px; background: rgba(243,67,162,.18); border: 1.5px solid rgba(243,67,162,.55);
  font-weight: 700; font-size: 38px; opacity: 0; }}
.fix .fx i {{ font-style: normal; font-family: Mono; font-size: 24px; letter-spacing: .14em; padding: 8px 14px; border-radius: 12px; background: linear-gradient(135deg, {PINK}, {MAG}); flex: none; }}
/* F */
.ok {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: 330px; top: 1392px; height: 84px; display: flex; align-items: center; justify-content: center; gap: 14px;
  border-radius: 999px; font-weight: 700; font-size: 36px; z-index: 20; opacity: 0; }}
.ok i {{ width: 44px; height: 44px; border-radius: 50%; background: #2fbf71; color: #fff; font-style: normal; font-size: 26px; display: flex; align-items: center; justify-content: center; }}
/* G */
.dm {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: 760px; top: 230px; height: 124px; border-radius: 36px; display: flex; align-items: center; gap: 22px;
  padding: 0 30px; z-index: 20; opacity: 0; }}
.dm img {{ width: 72px; height: 72px; object-fit: contain; padding: 10px; border-radius: 20px; background: #fff; }}
.dm b {{ display: block; font-weight: 700; font-size: 32px; }}
.dm span {{ display: block; font-weight: 500; font-size: 28px; color: rgba(255,255,255,.7); }}
.dm em {{ margin-left: auto; font-style: normal; font-family: Mono; font-size: 20px; color: rgba(255,255,255,.5); }}
.cm {{ position: absolute; left: 0; right: 0; top: 430px; text-align: center; font-family: Serif; font-style: italic; font-size: 110px; line-height: 1.1; color: #ffb3cd; opacity: 0; z-index: 20; }}
.kw {{ position: absolute; left: 0; right: 0; top: 560px; text-align: center; font-weight: 800; font-size: 230px; line-height: 1.1; letter-spacing: -.02em; opacity: 0; z-index: 20;
  background: linear-gradient(180deg, #fff 0%, #ffd6e6 45%, {PINK} 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 0 40px rgba(243,67,162,.6)); }}
.cbox {{ position: absolute; left: 90px; right: 90px; top: 900px; height: 130px; border-radius: 70px; display: flex; align-items: center; gap: 24px; padding: 0 20px 0 24px; z-index: 20; opacity: 0; }}
.cbox > i {{ width: 82px; height: 82px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, {MAG}); flex: none; }}
.cbox span {{ font-weight: 700; font-size: 52px; color: rgba(255,255,255,.5); }}
.cbox b {{ margin-left: auto; width: 92px; height: 92px; border-radius: 50%; background: #fff; color: {MAG}; font-size: 44px; display: flex; align-items: center; justify-content: center; flex: none; }}
.sub {{ position: absolute; left: 0; right: 0; top: 1066px; text-align: center; font-weight: 600; font-size: 54px; color: #fff; opacity: 0; z-index: 20; }}
.sub i {{ font-family: Serif; font-weight: 400; font-size: 1.15em; color: #ffb3cd; }}
/* mascot bubbles: inside the frame when he stands on the right */
.bub {{ left: 120px; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: check before you post 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{bird.CSS}{CSS}#birdlayer {{ position: absolute; inset: 0; z-index: 30; pointer-events: none; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="world" id="light">{blobs_l}</div>
      <div class="world" id="dark">{blobs_d}</div>
      <div id="panes">{panes}</div>
      <div id="cam"><div id="drift">
        {chr(10).join(HTML)}
      </div></div>
      <div id="liq"></div><div id="sweep"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set("#sweep", {{xPercent: -170}}, 0);
      tl.set("#liq", {{scale: .04}}, 0);
      tl.set(".sh, .pshine", {{skewX: -18, xPercent: -160}}, 0);
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
json.dump({"dur": DUR, "scenes": {"hook": [SA, SB], "contrast": [SB, SC], "creedom": [SC, SD], "score": [SD, SE], "fix": [SE, SF], "post": [SF, SG], "cta": [SG, DUR]}},
          open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
