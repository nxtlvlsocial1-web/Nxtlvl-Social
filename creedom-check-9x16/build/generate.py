"""Creators 100X x Creedom "CHECK" reel (9:16): writes index.html and plan/sfx_events.json from plan/words.json.

Look (owner: "premium glass fluid animations, nothing like paper or cardboard, premium transitions"; reference: the
yellow/black glass-pill reel): alternating LIGHT fluid scenes (white with drifting Creedom-pink, rose, lilac and peach
blobs) and DARK scenes (near-black with a magenta glow); every object is frosted glass (backdrop blur + saturate,
white highlight edge, inner glow); a liquid-glass lens orb stands for Creedom's AI; type blurs into focus word by word
(Inter, Instrument Serif Italic accents, JetBrains Mono labels); transitions are frosted-glass sweeps, zoom-throughs and
motion-blur text. The reel being checked is a neutral demo (Pexels 9384669, "3 AI tools I use daily"); its score is
labelled "Example reel". Creedom's own steps and its "timestamp + fix" format come from the owner's screen recording.
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


def head(hid, rows, top, line, size=88, dark=False, align="left", after=0.0):
    """premium headline: every word blurs into focus on its spoken time; ('word', cls) with cls '' or 'it' (serif)"""
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
    HTML.append(f'<div class="head {"dk" if dark else ""}" id="{hid}" style="top:{top}px;font-size:{size}px;text-align:{align}">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .06, .5, "{opacity: 0, filter: 'blur(14px)', y: 26}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    return out


def head_out(hid, t):
    to(f"#{hid}", t, .3, "{opacity: 0, filter: 'blur(16px)', y: -40}", "power2.in")


def sweep(t, dark_to=None):
    """frosted-glass panel sweeping across the frame (scene change)"""
    ft("#sweep", t - .22, .55, "{xPercent: -170}", "{xPercent: 170}", "power2.inOut")
    sfx("whoosh_big", t - .25)


def zoom_through(t):
    ft("#cam", t - .25, .3, "{scale: 1, filter: 'blur(0px)'}", "{scale: 1.9, filter: 'blur(18px)'}", "power2.in")
    ft("#cam", t + .05, .45, "{scale: .7, filter: 'blur(18px)'}", "{scale: 1, filter: 'blur(0px)'}", "expo.out")
    sfx("riser", t - .7)


def mode(t, dark):
    """crossfade between the light and the dark fluid worlds"""
    to("#dark", t - .1, .45, f"{{opacity: {1 if dark else 0}}}", "power2.inOut")


def scene(sid, t0, t1):
    st(f"#{sid}", t0, "{opacity: 1}")
    st(f"#{sid}", t1, "{opacity: 0}")


SA, SB, SC, SD, SE, SF, SG = 0.0, L0["c01"] - .14, L0["c02"] - .14, L0["c03"] - .1, L0["c04"] - .12, L0["c05"] - .12, L0["c06"] - .12

# ---- persistent objects: the phone (demo reel), the Share pill, the lens orb ------------------------------------------
VIDS = [(0, SB + .02, 0.0), (SC - .02, SD, 2.0), (SD, T("c03", "weak") - .05, 3.2), (T("c03", "weak") - .05, T("c03", "claim") - .05, 0.8),
        (T("c03", "claim") - .05, T("c03", "moment", 1) - .05, 6.8), (T("c03", "moment", 1) - .05, SE + .02, 8.6), (SF - .02, DUR, 4.0)]
vids = "".join(f'<video class="dv" id="dv{i}" src="assets/video/demo.mp4" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-media-start="{m:.3f}" '
               f'data-track-index="{1 + i % 2}" muted playsinline></video>' for i, (a, b, m) in enumerate(VIDS))
HTML.append('<div class="phone" id="phone"><div class="scr">' + vids +
            '<div class="ig"><div class="cap">3 AI tools I use daily</div><div class="side"><i></i><i></i><i></i></div>'
            '<div class="who"><b></b>creator.daily</div></div><div class="glint"></div></div>'
            '<div class="isl"></div></div>')
HTML.append('<div class="share glass" id="share"><svg class="lk" id="lk" viewBox="0 0 24 24"><path d="M7 11V8a5 5 0 0 1 10 0v3"/><rect x="5" y="11" width="14" height="10" rx="3"/></svg>'
            '<span id="shtx">Share</span></div>')

# ---- A hook (light) ---------------------------------------------------------------------------------------------------
HTML.append('<div class="scn" id="sa">')
head("ha", [[("An", ""), ("app", ""), ("that", ""), ("rates", "it")], [("your", ""), ("reel", ""), ("before", "it"), ("you", ""), ("post", "")]], 210, "c00", 86)
HTML.append('<div class="chip glass" id="fixchip">tells you exactly <i>what to fix</i></div></div>')
scene("sa", SA, SB)
ft("#phone", .05, .9, "{opacity: 0, y: 260, rotationX: 24, scale: .9}", "{opacity: 1, y: 0, rotationX: 0, scale: 1}", "expo.out")
ft("#share", .45, .6, "{opacity: 0, y: 60, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "expo.out")
t_r = T("c00", "rates")
sfx("whoosh", t_r - .1)
t_p = T("c00", "post")
to("#share", t_p, .12, "{scale: .94}")
to("#share", t_p + .12, .35, "{scale: 1}", "elastic.out(1,.4)")
ft("#lk", t_p, .4, "{rotation: -18}", "{rotation: 0}", "elastic.out(1.2,.3)")
sfx("click", t_p)
t_f = T("c00", "exactly")
ft("#fixchip", t_f - .1, .55, "{opacity: 0, filter: 'blur(12px)', y: 30, scale: .9}", "{opacity: 1, filter: 'blur(0px)', y: 0, scale: 1}", "expo.out")
sfx("pop", t_f)
head_out("ha", SB - .3)
to("#fixchip", SB - .3, .25, "{opacity: 0, filter: 'blur(12px)'}")

# ---- B contrast (dark) ------------------------------------------------------------------------------------------------
pts = " ".join(f"{i * 40},{120 - 60 * math.exp(-((i - 3) / 4) ** 2) - (i * 2)}" for i in range(11))
HTML.append('<div class="scn" id="sb">')
head("hb", [[("Not", ""), ("views", ""), ("after.", "it")], [("Reasons,", ""), ("before.", "it pk")]], 210, "c01", 92, dark=True)
HTML.append(f'<div class="card glass dkg" id="after"><div class="lab">AFTER YOU POST</div><div class="big">Views</div>'
            f'<svg viewBox="0 0 400 140" class="spark"><polyline points="{pts}"/></svg><div class="mut">numbers, no reasons</div></div>'
            '<div class="card glass dkg pkc" id="before"><div class="lab pk">BEFORE YOU POST</div><div class="big">Reasons</div>'
            '<div class="rows"><span>Hook</span><span>Proof</span><span>Trust</span></div><div class="mut">with the exact second</div></div></div>')
scene("sb", SB, SC)
sweep(SB)
mode(SB, True)
to("#phone", SB - .2, .3, "{opacity: 0, scale: .9, filter: 'blur(10px)'}", "power2.in")
to("#share", SB - .2, .3, "{opacity: 0}")
t_v = T("c01", "views")
ft("#after", t_v - .15, .7, "{opacity: 0, x: -200, rotationY: 30, filter: 'blur(14px)'}", "{opacity: 1, x: 0, rotationY: 12, filter: 'blur(0px)'}", "expo.out")
sfx("swish", t_v - .15)
t_re = T("c01", "reasons")
to("#after", t_re - .05, .5, "{opacity: .35, scale: .9, filter: 'grayscale(1) blur(3px)'}")
ft("#before", t_re - .1, .7, "{opacity: 0, x: 220, rotationY: -30, filter: 'blur(14px)', scale: .9}", "{opacity: 1, x: 0, rotationY: -8, filter: 'blur(0px)', scale: 1.04}", "expo.out")
sfx("whoosh", t_re - .1)
sfx("ding", T("c01", "before"))
head_out("hb", SC - .25)

# ---- C meet Creedom, it watches (light) --------------------------------------------------------------------------------
strip = "".join(f'<div class="fr glass" id="fr{i}"><img src="assets/img/demo_{t}.jpg"><span>0:0{t}</span></div>' for i, t in enumerate((1, 5, 8)))
steps = "".join(f'<div class="stp glass" id="sp{i}"><i>&#10003;</i>{s}</div>' for i, s in enumerate(["Watching the reel end to end", "Reading the scorecard"]))
HTML.append('<div class="scn" id="sc"><div class="brand glass" id="brand"><img src="assets/img/creedom_logo.png"></div>')
head("hcc", [[("It's", ""), ("called", "")], [("Creedom.", "it pk")]], 210, "c02", 96)
head("hc", [[("It", ""), ("watches", ""), ("your", ""), ("whole", ""), ("reel", "")], [("second", "it"), ("by", "it"), ("second.", "it")]], 210, "c02", 80,
     after=T("c02", "Creedom") + .2)
HTML.append(f'<div class="strip">{strip}</div><div class="steps">{steps}</div><div class="beam" id="beam"></div></div>')
scene("sc", SC, SD)
zoom_through(SC)
mode(SC, False)
t_cr = T("c02", "Creedom")
ft("#brand", SC + .05, .6, "{opacity: 0, scale: .6, filter: 'blur(16px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "expo.out")
sfx("impact", t_cr)
to("#brand", T("c02", "watches") - .2, .4, "{opacity: 0, scale: 1.4, filter: 'blur(14px)'}", "power2.in")
t_w = T("c02", "watches")
head_out("hcc", T("c02", "It", 1) - .3)
ft("#phone", t_w - .2, .7, "{opacity: 0, scale: .85, filter: 'blur(12px)', x: -150}", "{opacity: 1, scale: .86, filter: 'blur(0px)', x: -150}", "expo.out")
ft("#beam", t_w + .4, 2.6, "{opacity: .9, y: 0}", "{opacity: .9, y: 900}", "sine.inOut")
to("#beam", t_w + 2.9, .2, "{opacity: 0}")
for i in range(3):
    t = T("c02", "second") + .12 * i
    ft(f"#fr{i}", t, .6, "{opacity: 0, x: -320, scale: .6, filter: 'blur(10px)'}", f"{{opacity: 1, x: 0, scale: 1, filter: 'blur(0px)', rotation: {(-4, 2, 5)[i]}}}", "expo.out")
    sfx("shutter", t)
for i in range(2):
    t = T("c02", ("like", "viewer")[i]) - .05
    ft(f"#sp{i}", t, .5, "{opacity: 0, y: 40, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
    sfx("notify", t + .1)
head_out("hc", SD - .25)

# ---- D score + flags (dark) ---------------------------------------------------------------------------------------------
MARK = [("weak", "0:01", "Weak hook", "#F5B544", 1 / 15), ("claim", "0:07", "Claim, no proof", "#F5B544", 7 / 15), ("moment", "0:14", "Loses trust", MAG, 14 / 15)]
marks = "".join(f'<div class="mk" id="mk{i}" style="left:{p * 100:.1f}%;--c:{c}"><b></b><span class="glass dkg">{ts} · {lab}</span></div>'
                for i, (_, ts, lab, c, p) in enumerate(MARK))
HTML.append('<div class="scn" id="sd">')
head("hd", [[("Scores", ""), ("it", ""), ("out", ""), ("of", ""), ("five", "it pk")]], 200, "c03", 84, dark=True)
HTML.append('<div class="gauge glass dkg" id="gauge"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" class="gt"/>'
            '<circle cx="100" cy="100" r="84" class="gf" id="gf"/></svg><div class="gv"><b id="gnum">0.0</b><span>/5</span></div><div class="ex">EXAMPLE REEL</div></div>'
            f'<div class="rail glass dkg" id="rail"><div class="rl"><i id="ph"></i>{marks}</div><div class="tk"><span>0:00</span><span>0:05</span><span>0:10</span><span>0:15</span></div></div>'
            '<div class="flagh" id="flagh">Flags the exact moments</div></div>')
scene("sd", SD, SE)
sweep(SD)
mode(SD, True)
to("#phone", SD - .1, .55, "{opacity: 1, x: -250, y: -190, scale: .5, filter: 'blur(0px)'}", "expo.inOut")
for b in ("#fr0", "#fr1", "#fr2", "#sp0", "#sp1"):
    to(b, SD - .25, .2, "{opacity: 0}")
t_sc = T("c03", "scores")
ft("#gauge", t_sc - .1, .7, "{opacity: 0, scale: .7, filter: 'blur(14px)', rotation: -20}", "{opacity: 1, scale: 1, filter: 'blur(0px)', rotation: 0}", "expo.out")
ft("#gf", t_sc + .2, 1.1, "{strokeDashoffset: 528}", f"{{strokeDashoffset: {528 * (1 - 4.2 / 5):.0f}}}", "power2.out")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 4.2, duration: 1.1, ease: "power2.out", onUpdate: () => {{ document.getElementById("gnum").textContent = o.v.toFixed(1); }}}}, {t_sc + .2:.3f}); }})();')
sfx("riser_short", t_sc)
sfx("impact", t_sc + 1.2)
t_fl = T("c03", "flags")
head_out("hd", t_fl - .25)
ft("#flagh", t_fl - .1, .5, "{opacity: 0, filter: 'blur(14px)', y: 30}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
to("#gauge", t_fl - .1, .6, "{x: 140, y: -150, scale: .5}", "expo.inOut")
ft("#rail", t_fl, .7, "{opacity: 0, y: 120, filter: 'blur(14px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
sfx("swish", t_fl)
for i, (w, ts, lab, c, p) in enumerate(MARK):
    t = T("c03", w, 1 if w == "moment" else 0) - .05
    to("#ph", t, .35, f"{{left: '{p * 100:.1f}%'}}", "power3.inOut")
    ft(f"#mk{i} b", t + .1, .5, "{opacity: 0, y: -140, scale: .4}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.4)")
    ft(f"#mk{i} span", t + .25, .45, "{opacity: 0, y: 30, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
    ft(f"#mk{i} b", t + .55, .6, "{boxShadow: '0 0 0px 0px ' + 'rgba(255,255,255,0)'}", f"{{boxShadow: '0 0 40px 10px {c}'}}", "power2.out")
    sfx("pop", t + .15)

# ---- E the fix card (dark) --------------------------------------------------------------------------------------------
HTML.append('<div class="scn" id="se"><div class="fix glass dkg" id="fix"><div class="ft"><b>0:14</b><span>Loses trust</span></div>'
            '<div class="fl">The tool is never named, so viewers can\'t follow along.</div>'
            '<div class="fx"><i>Fix</i>Name the tool on screen at 0:14.</div></div>')
head("he", [[("With", ""), ("the", ""), ("timestamp,", "")], [("and", ""), ("the", ""), ("fix.", "it pk")]], 200, "c04", 92, dark=True)
HTML.append('</div>')
scene("se", SE, SF)
for b in ("#rail", "#gauge", "#flagh"):
    to(b, SE - .2, .3, "{opacity: 0, filter: 'blur(12px)'}")
to("#phone", SE - .2, .3, "{opacity: 0}")
ft("#fix", SE + .05, .8, "{opacity: 0, scale: .4, y: 420, rotationX: 40, filter: 'blur(18px)'}", "{opacity: 1, scale: 1, y: 0, rotationX: 0, filter: 'blur(0px)'}", "expo.out")
sfx("whoosh_big", SE)
ft("#fix .fx", T("c04", "fix") - .05, .5, "{opacity: 0, x: -60, filter: 'blur(10px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)'}", "expo.out")
sfx("ding", T("c04", "fix"))
head_out("he", SF - .25)
to("#fix", SF - .25, .3, "{opacity: 0, scale: 1.2, filter: 'blur(16px)'}", "power2.in")

# ---- F fix it before anyone sees it (light) -------------------------------------------------------------------------------
HTML.append('<div class="scn" id="sf">')
head("hf", [[("Fix", ""), ("it", "")], [("before", "it"), ("anyone", ""), ("sees", ""), ("it.", "")]], 210, "c05", 92)
HTML.append('<div class="ok glass" id="ok"><i>&#10003;</i>0:14 fixed</div></div>')
scene("sf", SF, SG)
zoom_through(SF)
mode(SF, False)
ft("#phone", SF + .05, .7, "{opacity: 0, x: 0, y: 0, scale: .9, filter: 'blur(14px)'}", "{opacity: 1, x: 0, y: 0, scale: 1, filter: 'blur(0px)'}", "expo.out")
ft("#share", SF + .1, .5, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "expo.out")
ft("#ok", T("c05", "fix") + .1, .55, "{opacity: 0, x: 120, filter: 'blur(12px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)'}", "expo.out")
sfx("notify", T("c05", "fix") + .1)
t_sees = T("c05", "sees")
to("#lk", t_sees - .1, .35, "{rotation: 24, y: -10, opacity: 0}", "back.in(2)")
to("#share", t_sees, .4, f"{{background: 'linear-gradient(135deg, {PINK}, {MAG})', color: '#fff', scale: 1.08, boxShadow: '0 20px 60px rgba(243,67,162,.55)'}}", "back.out(2)")
st("#shtx", t_sees, '{textContent: "Post it"}')
sfx("success", t_sees)
head_out("hf", SG - .25)
for b in ("#phone", "#share", "#ok"):
    to(b, SG - .25, .3, "{opacity: 0, filter: 'blur(12px)'}")

# ---- G CTA (dark) ---------------------------------------------------------------------------------------------------------------
fl = "".join(f'<div class="flt glass dkg" id="fl{i}" style="left:{x}px;top:{y}px">CHECK</div>' for i, (x, y) in enumerate([(90, 1330), (620, 1420), (260, 1530), (700, 1260), (120, 1180)]))
HTML.append('<div class="scn" id="sg"><div class="cm" id="cmh">Comment</div><div class="kw" id="kw">CHECK</div>'
            '<div class="cbox glass dkg" id="cbox"><i></i><span id="ctx">Add a comment…</span><b id="csend">&#10148;</b></div>'
            f'<div class="sub" id="sub">and I\'ll send you the <i>link.</i></div>{fl}</div>')
scene("sg", SG, DUR + 1)
sweep(SG)
mode(SG, True)
t_c = T("c06", "Comment")
ft("#cmh", t_c - .05, .5, "{opacity: 0, filter: 'blur(14px)', y: 30}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
t_k = T("c06", "Check")
ft("#kw", t_k - .1, .8, "{opacity: 0, scale: 1.6, scaleX: 1.9, filter: 'blur(24px)'}", "{opacity: 1, scale: 1, scaleX: 1, filter: 'blur(0px)'}", "expo.out")
sfx("impact", t_k)
ft("#cbox", t_k + .3, .5, "{opacity: 0, y: 60, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
t_ty = t_k + .55
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 5, duration: .45, ease: "steps(5)", onUpdate: () => {{ const e = document.getElementById("ctx"); '
   f'e.textContent = "CHECK".slice(0, Math.round(o.n)) || "Add a comment…"; e.style.color = o.n > 0 ? "#fff" : "rgba(255,255,255,.5)"; }}}}, {t_ty:.3f}); }})();')
for k in range(5):
    sfx("tick", t_ty + .09 * k)
to("#csend", t_ty + .5, .12, "{scale: 1.3}")
to("#csend", t_ty + .62, .15, "{scale: 1}")
sfx("click", t_ty + .5)
ft("#sub", T("c06", "send") - .05, .5, "{opacity: 0, filter: 'blur(12px)', y: 20}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
for i in range(5):
    t = t_ty + .7 + .15 * i
    ft(f"#fl{i}", t, 1.6, "{opacity: 0, y: 80, scale: .7}", "{opacity: 1, y: -160, scale: 1}", "power2.out")
    if i % 2 == 0:
        sfx("pop", t)

# ---- the Creedom mascot: he does the checking (owner: "use the creedom mascot that we made") ------------------------------
def star(sz, col=PINK):
    return (f'<svg viewBox="-50 -50 100 100" width="{sz}" height="{sz}"><path d="M0 -50 C6 -10 10 -6 50 0 C10 6 6 10 '
            f'0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z" fill="{col}"/></svg>')


HTML.append(f'<div id="birdlayer">{bird.rig(star)}</div>')
b = bird.Bird(js)
js('tl.set("#birdpos",{x:1250,y:1180,scale:.86},0);tl.set("#bflip",{scaleX:-1},0);')
js('tl.set("#sweat,#mag,.bub,.bsp,#cloud",{opacity:0,scale:.5},0);tl.set("#wingR,#footK",{opacity:0},0);')
for k in "LR":
    cx, cy, r = bird.EYES[k][:3]
    js(f'tl.set("#lu{k}",{{scaleY:0,svgOrigin:"{cx} {cy - r - 6}"}},0);tl.set("#ld{k}",{{scaleY:0,svgOrigin:"{cx} {cy + r + 6}"}},0);')
b.facing = -1
js(f'tl.to("#bidle",{{y:-7,duration:.42,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .42) - 1}}},0);')
js(f'tl.fromTo("#bidle",{{rotation:-2.5}},{{rotation:2.5,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.3) - 1}}},0);')
js(f'tl.to("#bbreath",{{scaleY:1.012,scaleX:.994,duration:.8,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .8) - 1}}},0);')
js(f'tl.fromTo("#wingLi",{{rotation:3}},{{rotation:-4,duration:.6,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .6) - 1}}},0);')
js(f'tl.fromTo("#wingDi",{{rotation:-3}},{{rotation:4,duration:.6,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .6) - 1}}},.3);')
js(f'tl.fromTo("#footLi",{{rotation:0,y:0}},{{rotation:-7,y:-4,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.3) - 1}}},0);')
js(f'tl.fromTo("#footRi",{{rotation:-7,y:-4}},{{rotation:0,y:0,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.3) - 1}}},0);')
# A: he walks in, lifts his glass magnifier to the reel, taps the locked Share, nods at "what to fix"
b.expr(0, "curious", .01)
b.at(.15, 730, 1200, 0.86, 1.0, "power2.out")
b.walk(.15, 1.0)
b.look(.3, -14, -6)
t_r = T("c00", "rates")
b.expr(t_r, "focused", .2)
b.show("#mag", t_r)
js(f'tl.to("#mag",{{rotation:-16,y:-24,duration:.45,ease:"sine.inOut",yoyo:true,repeat:3}},{t_r + .1:.3f});')
b.look(t_r, -18, -12)
t_p = T("c00", "post")
b.show("#mag", t_p - .1, False)
b.point(t_p, .9)
b.expr(t_p, "proud", .15)
b.nod(T("c00", "exactly"), 2)
b.expr(T("c00", "exactly"), "smile", .15)
# B (dark): skeptical at "views after", lights up at "reasons, before"
b.at(SB - .2, 370, 1340, 0.96, .5)
b.face(SB, 1)
b.expr(T("c01", "views"), "skeptical", .2)
b.shake(T("c01", "views") + .2, 3, 8)
t_re = T("c01", "Reasons")
b.expr(t_re, "excited", .12)
b.hop(t_re, 90)
b.flap(t_re, 4, 45)
b.expr(T("c01", "before") + .3, "joy", .15)
# C: pops up under the Creedom pill and waves, then scans the reel with the magnifier, second by second
b.at(SC - .1, 360, 1060, 0.86, .45)
t_cr = T("c02", "Creedom")
b.expr(t_cr - .1, "joy", .15)
b.wave(t_cr, 3)
b.show(".bsp", t_cr)
js(f'tl.to(".bsp",{{rotation:120,duration:1.0,ease:"none"}},{t_cr:.3f});')
b.show(".bsp", t_cr + 1.0, False)
t_wt = T("c02", "watches")
b.at(t_wt - .25, 610, 900, 0.79, .55)
b.face(t_wt - .25, -1)
b.expr(t_wt, "focused", .2)
b.show("#mag", t_wt)
js(f'tl.to("#birdpos",{{y:1340,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:1}},{t_wt + .4:.3f});')
js(f'tl.to("#mag",{{rotation:-12,duration:.35,ease:"sine.inOut",yoyo:true,repeat:7}},{t_wt + .3:.3f});')
b.look(t_wt + .3, -16, 6)
b.blink(T("c02", "viewer"))
b.show("#mag", SD - .2, False)
# D (dark): impressed by the score, then points at each flag; shocked at "loses trust"
b.at(SD - .1, 660, 1460, 0.79, .5)
b.face(SD, -1)
t_sc = T("c03", "scores")
b.expr(t_sc + 1.0, "excited", .12)
b.hop(t_sc + 1.1, 60)
for w, ex in (("weak", "skeptical"), ("claim", "focused")):
    t = T("c03", w)
    b.point(t, .7)
    b.expr(t, ex, .15)
t_tr = T("c03", "moment", 1)
b.expr(t_tr + .4, "shock", .1)
b.startle(t_tr + .4)
b.spread(t_tr + .4, 50, .12)
b.spread(t_tr + .9, 0, .2)
# E: beside the fix card, nods, proud
b.at(SE - .1, 670, 1330, 0.79, .5)
b.expr(SE + .2, "curious", .15)
b.nod(T("c04", "fix"), 2)
b.expr(T("c04", "fix"), "proud", .15)
# F: celebrates when Share unlocks
b.at(SF - .1, 740, 1240, 0.74, .5)
b.expr(T("c05", "fix"), "smile", .15)
t_se = T("c05", "sees")
b.expr(t_se, "joy", .12)
b.bounce(t_se, 3, 20)
b.flap(t_se, 4, 50)
b.show(".bsp", t_se)
js(f'tl.to(".bsp",{{rotation:-120,duration:1.0,ease:"none"}},{t_se:.3f});')
b.show(".bsp", t_se + 1.0, False)
# G: points up at CHECK, then waves goodbye
b.at(SG - .1, 360, 1420, 0.94, .5)
b.face(SG, 1)
b.point(T("c06", "Check"), .9)
b.expr(T("c06", "Check"), "excited", .12)
b.expr(T("c06", "send"), "love", .15)
b.wave(T("c06", "send") + .2, 3)

# ---- fluid blobs --------------------------------------------------------------------------------------------------------------
LB = [(-200, -150, 760, "rgba(238,104,139,.55)"), (520, 260, 820, "rgba(255,190,214,.75)"), (-260, 980, 900, "rgba(217,194,255,.6)"),
      (480, 1280, 820, "rgba(255,216,194,.6)"), (200, 620, 600, "rgba(243,67,162,.28)")]
DB = [(-220, -120, 800, "rgba(177,71,107,.55)"), (480, 900, 900, "rgba(243,67,162,.38)"), (-200, 1300, 760, "rgba(120,40,200,.35)"), (420, 120, 600, "rgba(238,104,139,.3)")]
blobs_l = "".join(f'<i class="bl" id="lb{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(LB))
blobs_d = "".join(f'<i class="bl" id="db{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(DB))
for i in range(len(LB)):
    js(f'tl.fromTo("#lb{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
       f'duration: {DUR / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, 0);')
for i in range(len(DB)):
    js(f'tl.fromTo("#db{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
       f'duration: {DUR / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, 0);')

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
#grain {{ position: absolute; inset: 0; opacity: .045; background: url(assets/img/grain.png); mix-blend-mode: overlay; pointer-events: none; }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 46%; perspective: 1600px; }}
.scn {{ position: absolute; inset: 0; opacity: 0; perspective: 1600px; }}
#sweep {{ position: absolute; top: -10%; bottom: -10%; left: 0; width: 70%; z-index: 50; pointer-events: none; transform: skewX(-12deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.28) 30%, rgba(255,255,255,.42) 50%, rgba(255,255,255,.28) 70%, rgba(255,255,255,0));
  backdrop-filter: blur(28px) saturate(1.6); -webkit-backdrop-filter: blur(28px) saturate(1.6); border-left: 2px solid rgba(255,255,255,.7); border-right: 2px solid rgba(255,255,255,.5); }}
/* glass */
.glass {{ background: linear-gradient(135deg, rgba(255,255,255,.62), rgba(255,255,255,.22)); backdrop-filter: blur(26px) saturate(1.7); -webkit-backdrop-filter: blur(26px) saturate(1.7);
  border: 1.5px solid rgba(255,255,255,.85); box-shadow: inset 0 1.5px 0 rgba(255,255,255,.95), inset 0 -18px 40px rgba(255,255,255,.18), 0 30px 80px rgba(120,20,60,.18); }}
.glass.dkg {{ background: linear-gradient(135deg, rgba(255,255,255,.16), rgba(255,255,255,.04)); border: 1.5px solid rgba(255,255,255,.26); color: #fff;
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,.35), inset 0 -18px 40px rgba(255,255,255,.04), 0 30px 90px rgba(0,0,0,.5); }}
.orb {{ position: absolute; border-radius: 50%; z-index: 2; pointer-events: none;
  background: radial-gradient(circle at 30% 26%, rgba(255,255,255,.8) 0, rgba(255,255,255,.18) 12%, rgba(255,255,255,0) 40%, rgba(255,255,255,.06) 70%, rgba(255,255,255,.45) 100%);
  border: 1px solid rgba(255,255,255,.55); opacity: .75;
  backdrop-filter: blur(3px) saturate(1.4) brightness(1.08); -webkit-backdrop-filter: blur(3px) saturate(1.4) brightness(1.08); box-shadow: inset -8px -12px 30px rgba(255,255,255,.18), 0 18px 40px rgba(0,0,0,.08); }}
.ringd {{ position: absolute; left: 520px; top: 1250px; width: 700px; height: 700px; border-radius: 50%; z-index: 1; pointer-events: none;
  border: 2px solid rgba(255,255,255,.25); box-shadow: 0 0 60px rgba(243,67,162,.25), inset 0 0 60px rgba(243,67,162,.15); }}
/* headlines */
.head {{ position: absolute; left: 80px; right: 80px; font-weight: 700; letter-spacing: -.035em; line-height: 1.04; z-index: 20; }}
.head.dk {{ color: #fff; }}
.hw {{ display: inline-block; opacity: 0; }}
.hw.it {{ font-family: Serif; font-style: italic; font-weight: 400; letter-spacing: -.01em; font-size: 1.12em; color: {ROSE}; }}
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
.ig .side {{ position: absolute; right: 22px; bottom: 170px; display: flex; flex-direction: column; gap: 26px; }}
.ig .side i {{ width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,.85); }}
.ig .who {{ position: absolute; left: 26px; bottom: 60px; display: flex; align-items: center; gap: 12px; color: #fff; font-weight: 700; font-size: 24px; }}
.ig .who b {{ width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, {MAG}); }}
.glint {{ position: absolute; inset: 0; background: linear-gradient(115deg, rgba(255,255,255,.22) 0%, rgba(255,255,255,0) 28%, rgba(255,255,255,0) 70%, rgba(255,255,255,.12) 100%); pointer-events: none; }}
.share {{ position: absolute; left: 50%; top: 1530px; width: 360px; height: 110px; margin-left: -180px; border-radius: 60px; display: flex; align-items: center; justify-content: center;
  gap: 18px; font-weight: 700; font-size: 44px; z-index: 11; opacity: 0; }}
.share svg {{ width: 44px; height: 44px; fill: none; stroke: currentColor; stroke-width: 2.4; }}
/* lens orb */
.lens {{ position: absolute; left: 640px; top: 760px; width: 320px; height: 320px; border-radius: 50%; z-index: 15; opacity: 0;
  background: radial-gradient(circle at 32% 28%, rgba(255,255,255,.95) 0, rgba(255,255,255,.35) 14%, rgba(255,255,255,.06) 42%, rgba(238,104,139,.22) 74%, rgba(255,255,255,.55) 100%);
  backdrop-filter: blur(4px) saturate(1.9) brightness(1.12); -webkit-backdrop-filter: blur(4px) saturate(1.9) brightness(1.12);
  box-shadow: inset -20px -30px 60px rgba(243,67,162,.35), inset 14px 18px 40px rgba(255,255,255,.6), 0 40px 90px rgba(243,67,162,.35); }}
.lring {{ position: absolute; inset: -26px; }}
.lring svg {{ width: 100%; height: 100%; transform: rotate(-90deg); overflow: visible; }}
.lring circle {{ fill: none; stroke: url(#none); stroke: {PINK}; stroke-width: 3; stroke-linecap: round; stroke-dasharray: 289; stroke-dashoffset: 289; filter: drop-shadow(0 0 8px {MAG}); }}
.lhi {{ position: absolute; left: 50px; top: 36px; width: 120px; height: 60px; border-radius: 50%; background: rgba(255,255,255,.75); filter: blur(10px); transform: rotate(-24deg); }}
.lcau {{ position: absolute; right: 40px; bottom: 34px; width: 90px; height: 90px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.7), transparent 70%); filter: blur(6px); }}
.chip {{ position: absolute; left: 80px; top: 430px; padding: 18px 30px; border-radius: 999px; font-weight: 600; font-size: 38px; z-index: 20; opacity: 0; }}
.chip i {{ font-family: Serif; font-weight: 400; font-size: 1.15em; color: {ROSE}; }}
/* B cards */
.card {{ position: absolute; top: 560px; width: 440px; height: 600px; border-radius: 44px; padding: 40px 36px; z-index: 12; opacity: 0; transform-style: preserve-3d; }}
#after {{ left: 70px; }} #before {{ right: 70px; }}
.card.pkc {{ border-color: rgba(243,67,162,.6); box-shadow: inset 0 1.5px 0 rgba(255,255,255,.35), 0 0 80px rgba(243,67,162,.35), 0 30px 90px rgba(0,0,0,.5); }}
.lab {{ font-family: Mono; font-size: 22px; letter-spacing: .14em; color: rgba(255,255,255,.6); }}
.lab.pk {{ color: #ff9cc0; }}
.big {{ font-weight: 700; font-size: 72px; letter-spacing: -.03em; margin: 18px 0 30px; }}
.spark {{ width: 100%; height: 160px; overflow: visible; }}
.spark polyline {{ fill: none; stroke: rgba(255,255,255,.55); stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; }}
.mut {{ position: absolute; left: 36px; bottom: 40px; font-family: Serif; font-style: italic; font-size: 38px; color: rgba(255,255,255,.6); }}
.rows {{ display: flex; flex-direction: column; gap: 18px; }}
.rows span {{ display: block; padding: 16px 22px; border-radius: 18px; background: rgba(243,67,162,.16); border: 1px solid rgba(243,67,162,.4); font-weight: 600; font-size: 32px; }}
/* C */
.brand {{ position: absolute; left: 50%; top: 820px; width: 620px; height: 200px; margin-left: -310px; border-radius: 100px; display: flex; align-items: center; justify-content: center;
  z-index: 25; opacity: 0; }}
.brand img {{ height: 92px; }}
.strip {{ position: absolute; left: 720px; top: 540px; display: flex; flex-direction: column; gap: 26px; z-index: 12; }}
.fr {{ width: 220px; padding: 10px; border-radius: 26px; opacity: 0; }}
.fr img {{ display: block; width: 100%; border-radius: 18px; }}
.fr span {{ display: block; text-align: center; font-family: Mono; font-size: 22px; margin-top: 8px; color: {ROSE}; }}
.steps {{ position: absolute; left: 80px; right: 80px; top: 1550px; display: flex; flex-direction: column; gap: 18px; z-index: 13; }}
.stp {{ display: flex; align-items: center; gap: 18px; padding: 20px 28px; border-radius: 26px; font-weight: 600; font-size: 34px; opacity: 0; }}
.stp i {{ width: 46px; height: 46px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, {MAG}); color: #fff; font-style: normal; font-size: 26px;
  display: flex; align-items: center; justify-content: center; }}
.beam {{ position: absolute; left: 136px; top: 540px; width: 540px; height: 8px; border-radius: 6px; z-index: 14; opacity: 0;
  background: linear-gradient(90deg, transparent, {MAG}, #fff, {MAG}, transparent); box-shadow: 0 0 40px 10px rgba(243,67,162,.5); }}
/* D */
.gauge {{ position: absolute; left: 560px; top: 450px; width: 440px; height: 440px; border-radius: 50%; z-index: 12; opacity: 0; display: flex; align-items: center; justify-content: center; }}
.gauge svg {{ position: absolute; inset: 20px; transform: rotate(-90deg); }}
.gt {{ fill: none; stroke: rgba(255,255,255,.12); stroke-width: 14; }}
.gf {{ fill: none; stroke: url(#none); stroke: {PINK}; stroke-width: 14; stroke-linecap: round; stroke-dasharray: 528; stroke-dashoffset: 528; filter: drop-shadow(0 0 12px {MAG}); }}
.gv {{ position: relative; text-align: center; }}
.gv b {{ font-weight: 700; font-size: 130px; letter-spacing: -.04em; }}
.gv span {{ font-family: Serif; font-style: italic; font-size: 70px; color: #ffb3cd; }}
.ex {{ position: absolute; bottom: 70px; font-family: Mono; font-size: 18px; letter-spacing: .2em; color: rgba(255,255,255,.55); }}
.rail {{ position: absolute; left: 60px; right: 60px; top: 1100px; height: 300px; border-radius: 40px; padding: 70px 50px 0; z-index: 12; opacity: 0; }}
.rl {{ position: relative; height: 12px; border-radius: 8px; background: linear-gradient(90deg, rgba(255,255,255,.3), rgba(255,255,255,.12)); }}
.rl #ph {{ position: absolute; left: 0; top: -22px; width: 4px; height: 56px; margin-left: -2px; background: #fff; border-radius: 2px; box-shadow: 0 0 20px #fff; }}
.mk {{ position: absolute; top: -12px; }}
.mk b {{ position: absolute; left: -18px; top: 0; width: 36px; height: 36px; border-radius: 50%; background: var(--c); border: 3px solid #fff; opacity: 0; }}
.mk span {{ position: absolute; top: 70px; left: -40px; white-space: nowrap; padding: 12px 20px; border-radius: 18px; font-weight: 600; font-size: 26px; opacity: 0; }}
#mk2 span {{ left: auto; right: -40px; }}
#mk1 span {{ left: -110px; top: 140px; }}
.tk {{ display: flex; justify-content: space-between; margin-top: 210px; font-family: Mono; font-size: 18px; color: rgba(255,255,255,.4); }}
.flagh {{ position: absolute; left: 80px; right: 80px; top: 200px; font-weight: 700; font-size: 84px; letter-spacing: -.035em; color: #fff; line-height: 1.04; opacity: 0; z-index: 20; }}
/* E */
.fix {{ position: absolute; left: 80px; right: 80px; top: 760px; border-radius: 48px; padding: 50px 50px 56px; z-index: 12; opacity: 0;
  border-color: rgba(243,67,162,.55); box-shadow: inset 0 1.5px 0 rgba(255,255,255,.35), 0 0 120px rgba(243,67,162,.35), 0 40px 100px rgba(0,0,0,.55); }}
.fix .ft {{ display: flex; align-items: baseline; gap: 22px; }}
.fix .ft b {{ font-weight: 700; font-size: 110px; letter-spacing: -.04em; }}
.fix .ft span {{ font-family: Serif; font-style: italic; font-size: 64px; color: #ff9cc0; }}
.fix .fl {{ font-weight: 500; font-size: 40px; line-height: 1.3; color: rgba(255,255,255,.75); margin: 26px 0 34px; }}
.fix .fx {{ display: flex; align-items: center; gap: 20px; padding: 24px 30px; border-radius: 28px; background: rgba(243,67,162,.18); border: 1.5px solid rgba(243,67,162,.55);
  font-weight: 700; font-size: 40px; opacity: 0; }}
.fix .fx i {{ font-style: normal; font-family: Mono; font-size: 24px; letter-spacing: .14em; padding: 8px 14px; border-radius: 12px; background: linear-gradient(135deg, {PINK}, {MAG}); }}
/* F */
.ok {{ position: absolute; right: 60px; top: 425px; display: flex; align-items: center; gap: 14px; padding: 16px 26px; border-radius: 999px; font-weight: 700; font-size: 34px; z-index: 20; opacity: 0; }}
.ok i {{ width: 42px; height: 42px; border-radius: 50%; background: #2fbf71; color: #fff; font-style: normal; font-size: 24px; display: flex; align-items: center; justify-content: center; }}
/* G */
.cm {{ position: absolute; left: 0; right: 0; top: 470px; text-align: center; font-family: Serif; font-style: italic; font-size: 110px; color: #ffb3cd; opacity: 0; z-index: 20; }}
.kw {{ position: absolute; left: 0; right: 0; top: 600px; text-align: center; font-weight: 800; font-size: 230px; letter-spacing: -.02em; opacity: 0; z-index: 20;
  background: linear-gradient(180deg, #fff 0%, #ffd6e6 45%, {PINK} 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 0 40px rgba(243,67,162,.6)); }}
.cbox {{ position: absolute; left: 90px; right: 90px; top: 960px; height: 130px; border-radius: 70px; display: flex; align-items: center; gap: 24px; padding: 0 22px 0 26px; z-index: 20; opacity: 0; }}
.cbox i {{ width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, {MAG}); }}
.cbox span {{ font-weight: 700; font-size: 52px; color: rgba(255,255,255,.5); }}
.cbox b {{ margin-left: auto; width: 92px; height: 92px; border-radius: 50%; background: #fff; color: {MAG}; font-size: 44px; display: flex; align-items: center; justify-content: center; }}
.sub {{ position: absolute; left: 0; right: 0; top: 1130px; text-align: center; font-weight: 600; font-size: 54px; color: #fff; opacity: 0; z-index: 20; }}
.sub i {{ font-family: Serif; font-weight: 400; font-size: 1.15em; color: #ffb3cd; }}
.flt {{ position: absolute; padding: 16px 30px; border-radius: 999px; font-weight: 800; font-size: 38px; letter-spacing: .04em; opacity: 0; z-index: 15; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: check before you post 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}{bird.CSS}#birdlayer {{ position: absolute; inset: 0; z-index: 30; pointer-events: none; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="world" id="light">{blobs_l}</div>
      <div class="world" id="dark">{blobs_d}</div>
      <div id="cam">
        {chr(10).join(HTML)}
      </div>
      <div id="sweep"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set("#sweep", {{xPercent: -170}}, 0);
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
