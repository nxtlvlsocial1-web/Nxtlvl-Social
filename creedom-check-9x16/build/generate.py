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


# v6 (owner: "it still feels very slow"): voice ~1.12x faster, a punchy CC BY track ("Corporate Music" by Ruslan Latypov,
# 99.4 bpm, strong kick) with every scene cut on its half-beat grid, 0.3 s whips and zooms instead of 0.5 s glides,
# a punch-in + glass flash on every key word, the score scene split in two shots, light streaks on cuts, overshoot
# entrances, faster panes, more mascot poses, a riser into every cut and deep hits on the hook and CHECK.
BEAT = 60 / 99.384
HB = BEAT / 2


def snap(t):
    """nearest half-beat of the song (it starts on a beat at reel t = 0)"""
    return round(t / HB) * HB


def sweep(t):
    """frosted-glass panel sweeping across the frame (scene change)"""
    ft("#sweep", t - .16, .36, "{xPercent: -170}", "{xPercent: 170}", "power2.inOut")
    sfx("whoosh_big", t - .2)


def streak(t):
    """three glass light streaks flying through the cut"""
    for i in range(3):
        ft(f"#stk{i}", t - .14 + .05 * i, .38, "{xPercent: -260, opacity: 1}", "{xPercent: 260, opacity: 1}", "power2.inOut")


def whip(t, d=1):
    """fast whip pan with motion blur: out to one side, in from the other (0.38 s in all)"""
    ft("#cam", t - .16, .16, "{x: 0, filter: 'blur(0px)'}", f"{{x: {-460 * d}, filter: 'blur(24px)'}}", "power2.in")
    ft("#cam", t, .24, f"{{x: {460 * d}, filter: 'blur(24px)'}}", "{x: 0, filter: 'blur(0px)'}", "power3.out")
    streak(t)
    sfx("riser_short", t - .9)
    sfx("whoosh", t - .18)


def punch(t, k=1.055):
    """punch-in with a soft glass flash on a key word"""
    ft("#punch", t - .03, .08, "{scale: 1}", f"{{scale: {k}}}", "power2.out")
    to("#punch", t + .05, .42, "{scale: 1}", "power3.out")
    st("#flash", t - .03, "{opacity: .38}")
    to("#flash", t - .02, .32, "{opacity: 0}", "power2.out")
    sfx("thump", t - .02)


LIQ = [0]


def liquid(t):
    """liquid-glass morph: an organic glass drop grows over the frame, the scene changes under it, and it melts away"""
    LIQ[0] += 1
    r0, r1 = "50% 50% 50% 50% / 50% 50% 50% 50%", ("42% 58% 63% 37% / 41% 44% 56% 59%", "58% 42% 38% 62% / 55% 61% 39% 45%")[LIQ[0] % 2]
    ft("#liq", t - .42, .45, f"{{scale: .04, rotation: 0, borderRadius: '{r0}'}}", f"{{scale: 4.4, opacity: 1, rotation: {(90, -90)[LIQ[0] % 2]}, borderRadius: '{r1}'}}", "power2.in")
    to("#liq", t + .03, .35, "{opacity: 0, filter: 'blur(30px)'}", "power2.out")
    st("#liq", t - .42, "{filter: 'blur(0px)', opacity: 1}")
    st("#liq", t + .4, "{scale: .04, filter: 'blur(0px)'}")
    streak(t)
    sfx("riser_short", t - .9)
    sfx("whoosh", t - .4)
    sfx("swish", t - .05)


def zoom_through(t):
    ft("#cam", t - .18, .2, "{scale: 1, filter: 'blur(0px)'}", "{scale: 1.6, filter: 'blur(14px)'}", "power2.in")
    ft("#cam", t + .02, .34, "{scale: .82, filter: 'blur(14px)'}", "{scale: 1, filter: 'blur(0px)'}", "expo.out")
    streak(t)
    sfx("riser", t - .8)
    sfx("whoosh", t - .15)


def mode(t, dark):
    """crossfade between the light and the dark fluid worlds"""
    to("#dark", t - .08, .3, f"{{opacity: {1 if dark else 0}}}", "power2.inOut")


def scene(sid, t0, t1):
    st(f"#{sid}", t0, "{opacity: 1}")
    st(f"#{sid}", t1, "{opacity: 0}")
    ft("#drift", t0, t1 - t0, "{scale: 1}", "{scale: 1.035}", "none")      # slow push-in on every scene


SA = 0.0
SB, SC, SD, SE, SF, SG = (snap(x) for x in (L0["c01"] - .12, L0["c02"] - .12, L0["c03"] - .08, L0["c04"] - .1, L0["c05"] - .1, L0["c06"] - .1))
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
ft("#phone", 0, .6, "{opacity: 1, x: 0, y: 170, rotationX: 16, scale: .74}", "{opacity: 1, x: 0, y: -10, rotationX: 0, scale: .78}", "back.out(1.4)")
ft("#share", .2, .45, "{opacity: 0, y: 60, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.6)")
sfx("impact", 0)
streak(.12)
phone_shine(.6)
shine("#share", .9)
t_r = T("c00", "rates")
sfx("whoosh", t_r - .1)
punch(t_r)
punch(T("c00", "before"), 1.04)
t_p = T("c00", "post")
to("#share", t_p, .12, "{scale: .94}")
to("#share", t_p + .12, .35, "{scale: 1}", "elastic.out(1,.4)")
ft("#lk", t_p, .4, "{rotation: -18}", "{rotation: 0}", "elastic.out(1.2,.3)")
sfx("click", t_p)
t_f = T("c00", "exactly")
ft("#fixchip", t_f - .1, .55, "{opacity: 0, filter: 'blur(12px)', y: 30, scale: .9}", "{opacity: 1, filter: 'blur(0px)', y: 0, scale: 1}", "back.out(1.4)")
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
whip(SB)
mode(SB, True)
st("#phone", SB, "{opacity: 0}")
st("#share", SB, "{opacity: 0}")
t_v = T("c01", "views")
ft("#after", t_v - .15, .7, "{opacity: 0, x: -200, rotationY: 35, filter: 'blur(14px)'}", "{opacity: 1, x: 0, rotationY: 0, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#after", t_v + .3)
tilt("#after", t_v + .6, T("c01", "reasons") - .1, 5, .8)
sfx("swish", t_v - .15)
t_re = T("c01", "reasons")
punch(t_re)
to("#after", t_re - .05, .5, "{opacity: .4, scale: .94, filter: 'grayscale(1) blur(2px)'}")
ft("#before", t_re - .1, .7, "{opacity: 0, x: 200, rotationY: -35, filter: 'blur(14px)', scale: .9}", "{opacity: 1, x: 0, rotationY: 0, filter: 'blur(0px)', scale: 1.03}", "back.out(1.4)")
shine("#before", t_re + .35)
tilt("#before", t_re + .65, SC, 5, .9)
ft("#before .rows span", t_re + .2, .45, "{opacity: 0, x: 40, filter: 'blur(8px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)', stagger: .09}", "back.out(1.4)")
sfx("whoosh", t_re - .1)
sfx("ding", T("c01", "before"))
head_out("hb", SC - .25)

# ---- C meet Creedom, it watches (light) ---------------------------------------------------------------------------------------
FS = (1, 4, 7, 10, 14)
strip = "".join(f'<div class="fr glass" id="fr{i}">{SH}<img src="assets/img/demo_f{t:02d}.jpg"><span>0:{t:02d}</span></div>' for i, t in enumerate(FS))
HTML.append(f'<div class="scn" id="sc"><div class="brand glass" id="brand">{SH}<img src="assets/img/creedom_logo.png"></div>')
head("hcc", [[("It's", ""), ("called", "")]], 330, "c02", 96)
head("hc", [[("It", ""), ("watches", ""), ("your", "")], [("whole", ""), ("reel,", "")], [("second", "it"), ("by", "it"), ("second.", "it")]], 190, "c02", 80,
     after=T("c02", "Creedom") + .2)
HTML.append(f'<div class="stat glass" id="stat">{SH}<i></i>WATCHING<b id="stt">0:00</b></div>'
            f'<div class="strip">{strip}</div><div class="beam" id="beam"></div></div>')
scene("sc", SC, SD)
liquid(SC)
zoom_through(SC)
mode(SC, False)
t_cr = T("c02", "Creedom")
ft("#brand", SC + .05, .6, "{opacity: 0, scale: .6, filter: 'blur(16px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#brand", t_cr + .05)
tilt("#brand", SC + .7, T("c02", "watches") - .2, 6, .8)
sfx("impact", t_cr)
punch(t_cr, 1.07)
t_w = T("c02", "watches")
to("#brand", t_w - .2, .4, "{opacity: 0, scale: 1.4, filter: 'blur(14px)'}", "power2.in")
head_out("hcc", T("c02", "It", 1) - .3)
# phone at x 390 (scale .7: 201..579 x 604..1276), status pill over it, the mascot holds his magnifier up to it on the right
ft("#phone", t_w - .2, .7, "{opacity: 0, x: -150, y: -60, scale: .6, filter: 'blur(12px)'}", "{opacity: 1, x: -150, y: -60, scale: .7, filter: 'blur(0px)'}", "back.out(1.4)")
phone_shine(t_w + .5)
ft("#stat", t_w, .55, "{opacity: 0, y: 30, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#stat", t_w + .4)
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 15, duration: {SD - .3 - (t_w + .3):.2f}, ease: "none", onUpdate: () => {{ '
   f'document.getElementById("stt").textContent = "0:" + String(Math.floor(o.v)).padStart(2, "0"); }}}}, {t_w + .3:.3f}); }})();')
ft("#beam", t_w + .3, 1.2, "{opacity: .95, y: 0}", "{opacity: .95, y: 630}", "sine.inOut")
to("#beam", t_w + 1.5, 1.2, "{y: 0}", "sine.inOut")
to("#beam", t_w + 2.7, .2, "{opacity: 0}")
t_s = T("c02", "second")
for i in range(len(FS)):
    t = t_s - .05 + .14 * i
    ft(f"#fr{i}", t, .6, "{opacity: 0, y: 80, scale: .7, filter: 'blur(10px)', rotationX: 50}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)', rotationX: 0}", "back.out(1.4)")
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
CHIPS = [("Hook", "#F5B544", 40, 600), ("Proof", "#F5B544", 836, 700), ("Trust", MAG, 40, 840)]
HTML.append('<div id="gcs">' + "".join(f'<div class="gc glass dkg" id="gc{i}" style="left:{x}px;top:{y}px;--c:{c}">{SH}<i></i>{n}</div>' for i, (n, c, x, y) in enumerate(CHIPS)) + '</div>')
HTML.append(f'<div class="gauge glass dkg" id="gauge"><i class="gsh"></i><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" class="gt"/>'
            '<circle cx="100" cy="100" r="84" class="gf" id="gf"/></svg><div class="gin"><div class="gv"><b id="gnum">0.0</b><span>/5</span></div>'
            '<div class="ex">EXAMPLE REEL</div></div></div>'
            f'<div class="rail glass dkg" id="rail">{SH}<div class="rl"><i id="ph"></i>{marks}</div><div class="tk">{ticks}</div>'
            f'<div class="rws">{rows}</div></div></div>')
scene("sd", SD, SE)
whip(SD, -1)
mode(SD, True)
for b in ["#phone", "#stat", "#beam"] + [f"#fr{i}" for i in range(len(FS))]:
    st(b, SD, "{opacity: 0}")
t_sc = T("c03", "scores")
ft("#gauge", SD + .02, .55, "{opacity: 0, scale: .6, filter: 'blur(14px)', rotation: -30}", "{opacity: 1, scale: 1, filter: 'blur(0px)', rotation: 0}", "back.out(1.5)")
punch(T("c03", "five"))
t_land = T("c03", "five")                            # v6: the faster voice leaves 0.6 s to count up, landing on "five"
ft("#gf", t_sc, t_land - t_sc, "{strokeDashoffset: 528}", f"{{strokeDashoffset: {528 * (1 - 4.2 / 5):.0f}}}", "power2.out")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 4.2, duration: {t_land - t_sc:.2f}, ease: "power2.out", onUpdate: () => {{ document.getElementById("gnum").textContent = o.v.toFixed(1); }}}}, {t_sc:.3f}); }})();')
js(f'tl.fromTo(".gsh", {{rotation: 0}}, {{rotation: 360, duration: 3.2, ease: "none", repeat: 1, immediateRender: false}}, {t_sc:.3f});')
t_fl = snap(T("c03", "flags") - .05)
tilt("#gauge", SD + .6, t_fl - .1, 7, .8)
sfx("impact", t_land)
for i in range(3):                                   # glass chips pop out of the ring when the score lands
    tc = t_land + .02 + .05 * i
    ft(f"#gc{i}", tc, .3, f"{{opacity: 0, x: {(260, -260, 260)[i]}, scale: .3}}", "{opacity: 1, x: 0, scale: 1}", "back.out(1.8)")
    shine(f"#gc{i}", tc + .15, .35)
    sfx("pop", tc)
# D2: zoom through into the flags shot; the ring and chips leave under the zoom, the rail fills the frame
zoom_through(t_fl)
# v6.1 (owner: "fix this flickering from 0:13"): the Trust chip's entrance still ran when the flags shot began, so it
# fought the hide; the chips now finish 0.2 s before the cut and leave as one group (#gcs) no chip tween touches
for b in ["#gauge", "#hd", "#gcs"]:
    st(b, t_fl, "{opacity: 0}")
ft("#rail", t_fl + .02, .5, "{opacity: 0, y: 140, rotationX: 30}", "{opacity: 1, y: 0, rotationX: 0}", "back.out(1.4)")
shine("#rail", t_fl + .35, 1.0)
for i, (w, ts, lab, tag, c, p) in enumerate(MARK):
    t = T("c03", w, 1 if w == "moment" else 0) - .05
    to("#ph", t, .35, f"{{left: '{p * 100:.3f}%'}}", "power3.inOut")
    ft(f"#mk{i}", t + .1, .5, "{opacity: 0, y: -120, scale: .4}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.4)")
    ft(f"#mk{i}", t + .5, .6, "{boxShadow: '0 0 0px 0px rgba(255,255,255,0)'}", f"{{boxShadow: '0 0 34px 8px {c}'}}", "power2.out")
    ft(f"#fl{i}", t + .15, .45, "{opacity: 0, x: -90, filter: 'blur(10px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)'}", "back.out(1.7)")
    shine(f"#fl{i}", t + .45, .6)
    punch(t + .12, 1.035)
    sfx("pop", t + .15)

# ---- E the fix card (dark) --------------------------------------------------------------------------------------------------
HTML.append(f'<div class="scn" id="se"><div class="fix glass dkg" id="fix">{SH}<div class="ft"><b>0:14</b><span>Loses trust</span></div>'
            '<div class="fl2">The tool is never named, so viewers can\'t follow along.</div>'
            '<div class="fx"><i>FIX</i>Name the tool on screen at 0:14.</div></div>')
head("he", [[("With", ""), ("the", ""), ("timestamp,", "")], [("and", ""), ("the", ""), ("fix.", "it pk")]], 190, "c04", 88, dark=True)
HTML.append('</div>')
scene("se", SE, SF)
whip(SE)
for b in ("#rail", "#gauge"):
    st(b, SE, "{opacity: 0}")
ft("#fix", SE + .02, .6, "{opacity: 0, scale: .5, y: 300, rotationX: 40, filter: 'blur(18px)'}", "{opacity: 1, scale: 1, y: 0, rotationX: 0, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#fix", SE + .55, 1.0)
tilt("#fix", SE + .85, SF, 5, .9)
sfx("whoosh_big", SE)
ft("#fix .fx", T("c04", "fix") - .05, .5, "{opacity: 0, x: -60, filter: 'blur(10px)'}", "{opacity: 1, x: 0, filter: 'blur(0px)'}", "back.out(1.4)")
sfx("ding", T("c04", "fix"))
punch(T("c04", "fix"))
head_out("he", SF - .25)
to("#fix", SF - .2, .2, "{opacity: 0, scale: 1.2, filter: 'blur(16px)'}", "power2.in")

# ---- F fix it before anyone sees it (light): the hook layout again, now fixed --------------------------------------------------
HTML.append('<div class="scn" id="sf">')
head("hf", [[("Fix", ""), ("it", ""), ("before", "it")], [("anyone", ""), ("sees", ""), ("it.", "")]], 190, "c05", 88)
HTML.append(f'<div class="ok glass" id="ok">{SH}<i>&#10003;</i>0:14 fixed</div></div>')
scene("sf", SF, SG)
zoom_through(SF)
mode(SF, False)
ft("#phone", SF + .05, .7, "{opacity: 0, x: 0, y: -10, scale: .7, filter: 'blur(14px)'}", "{opacity: 1, x: 0, y: -10, scale: .78, filter: 'blur(0px)'}", "back.out(1.4)")
ft("#share", SF + .1, .5, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(1.4)")
t_fx2 = T("c05", "fix")
ft("#tool", t_fx2, .55, "{opacity: 0, scale: .6, filter: 'blur(10px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "back.out(2)")
shine("#tool", t_fx2 + .3, .7)
ft("#ok", t_fx2 + .15, .55, "{opacity: 0, y: 30, filter: 'blur(12px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#ok", t_fx2 + .5)
sfx("notify", t_fx2 + .1)
phone_shine(t_fx2 + .2)
t_sees = T("c05", "sees")
to("#lk", t_sees - .1, .35, "{rotation: 24, y: -10, opacity: 0}", "back.in(2)")
to("#share", t_sees, .4, f"{{background: 'linear-gradient(135deg, {PINK}, {MAG})', color: '#fff', scale: 1.08, boxShadow: '0 20px 60px rgba(243,67,162,.55)'}}", "back.out(2)")
st("#shtx", t_sees, '{textContent: "Post it"}')
shine("#share", t_sees + .2)
sfx("success", t_sees)
punch(t_sees)
tilt("#phone .scr", SF + .7, SG, 4, 1.2)
head_out("hf", SG - .25)
for b in ("#phone", "#share", "#ok"):
    st(b, SG, "{opacity: 0}")

# ---- G CTA (dark) ---------------------------------------------------------------------------------------------------------------
HTML.append(f'<div class="scn" id="sg"><div class="dm glass dkg" id="dm">{SH}<img src="assets/img/creedom_logo.png"><div><b>Creedom</b><span>sent you the link</span></div><em>now</em></div>'
            '<div class="cm" id="cmh">Comment</div><div class="kw" id="kw">CHECK</div>'
            f'<div class="cbox glass dkg" id="cbox">{SH}<i></i><span id="ctx">Add a comment…</span><b id="csend">&#10148;</b></div>'
            '<div class="sub" id="sub">and I\'ll send you the <i>link.</i></div></div>')
scene("sg", SG, DUR + 1)
liquid(SG)
mode(SG, True)
t_c = T("c06", "Comment")
ft("#cmh", t_c - .05, .5, "{opacity: 0, filter: 'blur(14px)', y: 30}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
t_k = T("c06", "Check")
ft("#kw", t_k - .1, .8, "{opacity: 0, scale: 1.6, scaleX: 1.9, filter: 'blur(24px)'}", "{opacity: 1, scale: 1, scaleX: 1, filter: 'blur(0px)'}", "back.out(1.4)")
sfx("impact", t_k)
sfx("thump", t_k)
punch(t_k, 1.08)
ft("#cbox", t_k + .3, .5, "{opacity: 0, y: 60, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "back.out(1.4)")
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
ft("#dm", t_dm - .1, .7, "{opacity: 0, y: -160, scale: .9, filter: 'blur(12px)'}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#dm", t_dm + .35)
sfx("notify", t_dm)
tilt("#cbox", t_ty + .8, DUR, 4, 1.0)


# ---- the Creedom mascot, Cree (not a bird): the full 3D mascot from the creedom-explainer reel ------------------------------
# v5 (owner: "when i say the mascot looks bad then it is bad, look how full he looks in the previous video, make him
# like that"): the cut-out rig is gone; Cree is the mascot's own 3D render in thirteen poses (creedom-explainer-9x16,
# assets/img/poses, plan/poses.json): stand, walk + pass (walk cycle), wave, point (to his left = frame right), present,
# cheer, shock, sad, mag (magnifying glass), phone (typing), think, proud. Every pose sits on one 820 x 820 canvas with
# the feet on y 800, so a pose swap never moves him; the body centre is (410, 500). He swaps poses on the script beats,
# walks between scenes, hops with squash and stretch, blinks, sweats, and gets glass "?" and "!" bubbles.
POSES = json.load(open(os.path.join(ROOT, "plan", "poses.json")))
PCX, PCY = 410, 500
CS = .52                                         # his scale: 600 px pose height -> ~312 px on screen


def cree_html():
    parts = []
    for name, m in POSES.items():
        defs, lids = "", ""
        for k, (cx, cy, rx, ry, top, bot) in enumerate(m["eyes"]):
            defs += (f'<linearGradient id="lg{name}{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
                     f'<stop offset="1" stop-color="{bot}"/></linearGradient>')
            lids += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 8}" ry="{ry + 8}" fill="url(#lg{name}{k})"/>'
                     f'<path d="M {cx - rx * .8:.0f} {cy + ry * .05:.0f} Q {cx} {cy + ry * .55:.0f} {cx + rx * .8:.0f} {cy + ry * .05:.0f}" fill="none" '
                     f'stroke="#2a0c22" stroke-width="9" stroke-linecap="round"/>')
        svg = f'<svg viewBox="0 0 820 820" class="clids"><defs>{defs}</defs><g class="lidg">{lids}</g></svg>' if lids else ""
        parts.append(f'<div class="cpose" id="cp-{name}"><img src="assets/img/poses/{name}.png" alt="">{svg}</div>')
    sweat = ('<svg viewBox="0 0 820 820" class="csw"><path class="sweat" d="M 690 190 C 675 220 665 240 665 255 A 25 25 0 0 0 715 255 C 715 240 705 220 690 190 Z" '
             'fill="#7fd3ff" stroke="#3aa6e6" stroke-width="5"/></svg>')
    sp = "".join(f'<div class="csp" style="left:{x}px;top:{y}px">{star(z, c)}</div>'
                 for x, y, z, c in [(40, 170, 110, PINK), (680, 110, 90, "#f2b134"), (720, 440, 70, PINK), (60, 470, 64, "#f2b134")])
    return (f'<div id="cree"><i id="cshadow"></i><div id="creeb"><div id="creef"><div id="creep">{"".join(parts)}</div></div>{sweat}</div>'
            f'{sp}<div id="bub"><span id="bubt">!</span></div></div>')


def cree_to(t, x, y, s=CS, d=.6, ease="power3.inOut"):
    """Move Cree (body centre at x, y in frame px; s = scale of the 820 px pose canvas)."""
    js(f'tl.to("#cree", {{x: {x - PCX:.0f}, y: {y - PCY:.0f}, scale: {s}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def pose(t, name, flip=None, squash=True):
    """Swap to a pose (flip: True faces him the other way, None keeps the current facing), with a little squash."""
    js(f'tl.set("#cree .cpose", {{opacity: 0}}, {t:.3f});')
    js(f'tl.set("#cp-{name}", {{opacity: 1}}, {t:.3f});')
    if flip is not None:
        js(f'tl.set("#creef", {{scaleX: {-1 if flip else 1}}}, {t:.3f});')
    if squash:
        js(f'tl.fromTo("#creep", {{scaleX: 1.07, scaleY: .9}}, {{scaleX: 1, scaleY: 1, duration: .28, ease: "back.out(3)", immediateRender: false}}, {t:.3f});')


def cree_walk(t0, t1, frm, to, end="stand", step=.15, end_flip=False):
    """Walk from frm (x, y, s) to to (x, y, s): stride and pass frames alternate with a bob, facing the way he goes."""
    n = max(2, round((t1 - t0) / step))
    n += n % 2
    stp = (t1 - t0) / n
    flip = to[0] < frm[0]
    js(f'tl.fromTo("#cree", {{x: {frm[0] - PCX:.0f}, y: {frm[1] - PCY:.0f}, scale: {frm[2]}}}, {{x: {to[0] - PCX:.0f}, y: {to[1] - PCY:.0f}, scale: {to[2]}, '
       f'duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    for k in range(n):
        pose(t0 + k * stp, "walk" if k % 2 == 0 else "pass", flip=flip if k == 0 else None, squash=False)
    js(f'tl.fromTo("#creef", {{y: 0}}, {{y: -22, duration: {stp / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: {2 * n - 1}, immediateRender: false}}, {t0:.3f});')
    js(f'tl.fromTo("#creef", {{rotation: -4}}, {{rotation: 4, duration: {stp:.3f}, ease: "sine.inOut", yoyo: true, repeat: {n - 1}, immediateRender: false}}, {t0:.3f});')
    js(f'tl.to("#creef", {{rotation: 0, y: 0, duration: .12}}, {t1:.3f});')
    pose(t1, end, flip=end_flip)
    sfx("swish", t0)


def cree_hop(t, h=70, n=1, period=.36):
    for k in range(n):
        tk = t + k * period
        js(f'tl.fromTo("#creeb", {{y: 0, scaleY: 1, scaleX: 1}}, {{keyframes: [{{scaleY: .86, scaleX: 1.1, y: 10, duration: .07}}, '
           f'{{scaleY: 1.08, scaleX: .94, y: {-h}, duration: .14, ease: "power2.out"}}, {{scaleY: 1, scaleX: 1, y: 0, duration: .13, ease: "power2.in"}}, '
           f'{{scaleY: .92, scaleX: 1.06, y: 0, duration: .04}}, {{scaleY: 1, scaleX: 1, duration: .06}}], immediateRender: false}}, {tk:.3f});')
        js(f'tl.fromTo("#cshadow", {{scale: 1, opacity: 1}}, {{scale: .7, opacity: .5, duration: .21, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false}}, {tk + .07:.3f});')
    sfx("pop", t)


def cree_wiggle(t, n=3, amp=8, period=.22):
    js(f'tl.fromTo("#creeb", {{rotation: 0}}, {{keyframes: [' + ", ".join(f'{{rotation: {amp if k % 2 == 0 else -amp}, duration: {period / 2:.2f}}}' for k in range(n * 2))
       + f', {{rotation: 0, duration: .1}}], immediateRender: false}}, {t:.3f});')


def cree_tilt(t, a, d=.35):
    js(f'tl.to("#creef", {{rotation: {a}, duration: {d}, ease: "back.out(2)"}}, {t:.3f});')


def blink(t):
    js(f'tl.set("#cree .lidg", {{opacity: 1}}, {t:.3f});')
    js(f'tl.set("#cree .lidg", {{opacity: 0}}, {t + .11:.3f});')


def sweat(t, d=1.0):
    js(f'tl.fromTo("#cree .sweat", {{opacity: 0, y: -20, scale: .4}}, {{opacity: 1, y: 0, scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#cree .sweat", {{y: 40, duration: {d - .2:.2f}, ease: "power1.in"}}, {t + .25:.3f});')
    js(f'tl.to("#cree .sweat", {{opacity: 0, duration: .1}}, {t + d:.3f});')


def say(t, text, d=.9, left=False):
    """A glass thought bubble by his head (left=True puts it on his other side, for when he stands at the right edge)."""
    js(f'tl.set("#bubt", {{textContent: "{text}"}}, {t - .01:.3f});')
    js(f'tl.set("#bub", {{x: {-560 if left else 0}}}, {t - .01:.3f});')
    js(f'tl.fromTo("#bub", {{opacity: 0, scale: .2, rotation: -30}}, {{opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(2.4)", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#bub", {{opacity: 0, scale: .6, duration: .2, ease: "power2.in"}}, {t + d:.3f});')
    sfx("pop", t)


def sparkle(t, d=1.0, rot=120):
    js(f'tl.fromTo("#cree .csp", {{opacity: 0, scale: .3}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(3)", stagger: .05, immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#cree .csp", {{rotation: "+={rot}", duration: {d}, ease: "none"}}, {t:.3f});')
    js(f'tl.to("#cree .csp", {{opacity: 0, scale: .5, duration: .2, ease: "power2.in"}}, {t + d:.3f});')


def star(sz, col=PINK):
    return (f'<svg viewBox="-50 -50 100 100" width="{sz}" height="{sz}"><path d="M0 -50 C6 -10 10 -6 50 0 C10 6 6 10 '
            f'0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z" fill="{col}"/></svg>')


HTML.append(cree_html())


def P(cx, feet, s=CS):
    """frame position of his body centre from where his feet stand"""
    return (cx, feet - (800 - PCY) * s, s)


RIGHT = P(885, 1362, .48)                           # right of the phone, feet level with its bottom
js(f'tl.set("#cree", {{x: {1010 - PCX}, y: {RIGHT[1] - PCY:.0f}, scale: {RIGHT[2]}, opacity: 1}}, 0);')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -9, duration: .8, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .8)}, immediateRender: false}}, 0);')
js(f'tl.fromTo("#creeb", {{scaleY: 1}}, {{scaleY: 1.015, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / 1.1)}, immediateRender: false}}, 0);')

# A: walks in, studies the phone through his magnifier, cheers at "post", points at the phone, proud at "exactly"
cree_walk(0, .5, (1010, RIGHT[1], RIGHT[2]), RIGHT, end="stand")
t_r = T("c00", "rates")
pose(t_r - .05, "mag")
js(f'tl.fromTo("#creef", {{rotation: 0}}, {{rotation: -7, duration: .4, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, {t_r + .1:.3f});')
t_p = T("c00", "post")
pose(t_p - .05, "cheer")
cree_hop(t_p, 90)
say(t_p + .05, "!", .8, left=True)
t_tl = T("c00", "tells")
pose(t_tl - .05, "point", flip=True)
t_x = T("c00", "exactly")
pose(t_x + .2, "proud")
cree_wiggle(t_x + .3, 2, 5)
blink(T("c00", "fix"))
sparkle(T("c00", "fix"), .9)

# B (dark): "views after"? he thinks, then droops; "reasons, before" makes him cheer and jump twice
B_POS = P(540, 1545)
cree_walk(SB - .25, SB + .35, RIGHT, B_POS, end="stand")
t_vw = T("c01", "views")
pose(t_vw - .05, "think")
cree_tilt(t_vw, -8)
say(t_vw + .1, "?", .9)
pose(T("c01", "post") - .05, "sad")
cree_tilt(T("c01", "post"), 0)
t_re2 = T("c01", "Reasons")
pose(t_re2 - .05, "cheer")
cree_hop(t_re2, 100, 2)
sparkle(t_re2 + .1, 1.0, 140)

# C: one "Creedom" only (the logo pill), he waves under it and jumps; then scans the reel with his magnifier
C_POS = P(540, 1330, .66)
cree_to(SC - .2, *C_POS, d=.5)
pose(SC + .1, "stand")
blink(SC + .5)
t_cr2 = T("c02", "Creedom")
pose(t_cr2 - .05, "wave")
cree_hop(t_cr2 + .05, 110)
sparkle(t_cr2 + .1, 1.1, 160)
pose(t_cr2 + .55, "present", flip=True)
t_wt = T("c02", "watches")
W_POS = P(800, 1276, .5)
cree_walk(t_wt - .35, t_wt + .1, C_POS, W_POS, end="mag")
js(f'tl.fromTo("#creef", {{rotation: 0, y: 0}}, {{rotation: -8, y: -30, duration: .45, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, {t_wt + .2:.3f});')
t_s2 = T("c02", "second")
pose(t_s2 + .05, "point", flip=True)
js(f'tl.to("#creef", {{rotation: 10, duration: .3, ease: "back.out(2)"}}, {t_s2 + .1:.3f});')
js(f'tl.to("#creef", {{rotation: 0, duration: .25}}, {T("c02", "real") - .1:.3f});')
pose(T("c02", "real") - .05, "proud")
blink(SD - .45)

# D (dark): thinks while the score counts, cheers when it lands, points at the flags, thinks at "weak hook", points
# at "claim", gets a fright (shock, sweat, "!") at "loses trust" and droops
D_POS = P(540, 1470)                             # under the ring (D1) and the rail (D2)
cree_walk(SD - .3, SD + .3, W_POS, D_POS, end="stand")
pose(t_sc - .05, "think")
cree_tilt(t_sc, -6)

cree_tilt(t_land - .1, 0, .15)
pose(t_land - .05, "cheer")
cree_hop(t_land, 110)
sparkle(t_land + .05, 1.0)
pose(t_fl + .3, "present")
cree_hop(t_fl + .3, 40)
blink(t_fl + 1.4)
t_wk = T("c03", "weak")
pose(t_wk - .05, "think")
say(t_wk + .05, "?", .8)
t_cl = T("c03", "claim")
pose(t_cl - .05, "point")
cree_wiggle(t_cl + .1, 2, 6)
t_tr = T("c03", "loses")
pose(t_tr - .05, "shock")
cree_hop(t_tr, 50)
say(t_tr + .05, "!", .7)
sweat(t_tr + .1, .9)
pose(t_tr + .6, "sad")

# E: reads the fix card through his magnifier, proud at "the fix"
E_POS = P(540, 1405)
cree_to(SE - .2, *E_POS, d=.45)
pose(SE + .05, "mag", flip=True)
js(f'tl.fromTo("#creef", {{y: 0}}, {{y: -24, duration: .4, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, {SE + .2:.3f});')
t_fx = T("c04", "fix")
pose(t_fx - .05, "proud", flip=False)
cree_hop(t_fx + .1, 60)

# F: back beside the phone; points at the fixed reel, watches Share unlock, cheers
cree_walk(SF - .25, SF + .3, E_POS, RIGHT, end="stand")
pose(t_fx2 - .05, "point", flip=True)
pose(T("c05", "anyone") + .05, "think", flip=False)
pose(t_sees - .05, "cheer")
cree_hop(t_sees, 100, 2)
sparkle(t_sees + .1, 1.0, -140)

# G: walks to centre stage, cheers at CHECK, types the comment on his phone, waves goodbye
G_POS = P(540, 1520, .55)
cree_walk(SG - .25, SG + .35, RIGHT, G_POS, end="stand")
pose(t_k - .05, "cheer")
cree_hop(t_k, 90)
pose(t_ty - .1, "phone")
pose(t_dm - .05, "wave")
cree_wiggle(t_dm + .1, 3, 6)
pose(DUR - .7, "proud")
for t in (3.1, 8.8, 13.5, 15.8, 20.1, 22.2):
    blink(t)

# ---- fluid blobs and drifting glass panes --------------------------------------------------------------------------------------
LB = [(-200, -150, 760, "rgba(238,104,139,.55)"), (520, 260, 820, "rgba(255,190,214,.75)"), (-260, 980, 900, "rgba(217,194,255,.6)"),
      (480, 1280, 820, "rgba(255,216,194,.6)")]
DB = [(-220, -120, 800, "rgba(177,71,107,.55)"), (480, 900, 900, "rgba(243,67,162,.38)"), (-200, 1300, 760, "rgba(120,40,200,.35)")]
blobs_l = "".join(f'<i class="bl" id="lb{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(LB))
blobs_d = "".join(f'<i class="bl" id="db{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(DB))
for i in range(len(LB)):
    js(f'tl.fromTo("#lb{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
       f'duration: {DUR / 3:.2f}, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false}}, 0);')
for i in range(len(DB)):
    js(f'tl.fromTo("#db{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
       f'duration: {DUR / 3:.2f}, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false}}, 0);')
# big frosted panes, mostly off-frame at the edges, drifting and turning slowly (glass, not bubbles)
PANES = [(-300, 330, 560, 340, -18), (830, 1500, 600, 360, 16), (690, -170, 520, 300, 24), (-330, 1560, 600, 320, -10)]
panes = "".join(f'<i class="pane" id="pn{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>' for i, (x, y, w, h, r) in enumerate(PANES))
for i, (x, y, w, h, r) in enumerate(PANES):
    js(f'tl.fromTo("#pn{i}", {{rotation: {r}, x: 0, y: 0}}, {{rotation: {r + random.choice((-1, 1)) * random.randint(8, 14)}, x: {random.randint(-80, 80)}, '
       f'y: {random.randint(-160, 160)}, duration: {DUR / 4:.2f}, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, 0);')

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
#punch {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#flash {{ position: absolute; inset: 0; z-index: 48; pointer-events: none; opacity: 0; mix-blend-mode: soft-light;
  background: rgba(255,236,246,.9); }}
.stk {{ position: absolute; left: 0; width: 60%; height: 10px; z-index: 51; pointer-events: none; opacity: 0; border-radius: 10px;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.95) 50%, rgba(255,255,255,0)); box-shadow: 0 0 30px 6px rgba(255,170,210,.55); }}
#stk0 {{ top: 560px; }} #stk1 {{ top: 980px; height: 18px; }} #stk2 {{ top: 1380px; height: 6px; }}
.gc {{ position: absolute; width: 204px; height: 76px; border-radius: 999px; display: flex; align-items: center; justify-content: center; gap: 14px;
  font-weight: 700; font-size: 32px; z-index: 13; opacity: 0; }}
.gc > i {{ width: 18px; height: 18px; border-radius: 50%; background: var(--c); box-shadow: 0 0 12px var(--c); }}
#drift {{ position: absolute; inset: 0; transform-origin: 50% 50%; perspective: 1600px; }}
.scn {{ position: absolute; inset: 0; opacity: 0; perspective: 1600px; }}
#sweep {{ position: absolute; top: -10%; bottom: -10%; left: 0; width: 70%; z-index: 50; pointer-events: none;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.28) 30%, rgba(255,255,255,.42) 50%, rgba(255,255,255,.28) 70%, rgba(255,255,255,0));
  backdrop-filter: blur(28px) saturate(1.6); -webkit-backdrop-filter: blur(28px) saturate(1.6); border-left: 2px solid rgba(255,255,255,.7); border-right: 2px solid rgba(255,255,255,.5); }}
#liq {{ position: absolute; left: 50%; top: 50%; width: 520px; height: 520px; margin: -260px 0 0 -260px; z-index: 49; pointer-events: none; opacity: 0; border-radius: 50%;
  background: linear-gradient(135deg, rgba(255,255,255,.7) 0, rgba(255,255,255,.26) 30%, rgba(255,214,230,.22) 65%, rgba(243,67,162,.24) 100%);
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
.brand {{ position: absolute; left: 50%; top: 500px; width: 620px; height: 200px; margin-left: -310px; border-radius: 100px; display: flex; align-items: center; justify-content: center;
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
.gauge {{ position: absolute; left: 280px; top: 450px; width: 520px; height: 520px; border-radius: 50%; z-index: 12; opacity: 0; }}
.gsh {{ position: absolute; inset: 0; border-radius: 50%; background: conic-gradient(from 0deg, rgba(255,255,255,0) 0 62%, rgba(255,255,255,.22) 72%, rgba(255,255,255,0) 82%); }}
.gauge svg {{ position: absolute; inset: 22px; width: 476px; height: 476px; transform: rotate(-90deg); }}
.gt {{ fill: none; stroke: rgba(255,255,255,.12); stroke-width: 12; }}
.gf {{ fill: none; stroke: {PINK}; stroke-width: 12; stroke-linecap: round; stroke-dasharray: 528; stroke-dashoffset: 528; filter: drop-shadow(0 0 10px {MAG}); }}
.gin {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.gv {{ display: flex; align-items: baseline; justify-content: center; line-height: 1; padding-top: 10px; }}
.gv b {{ font-weight: 700; font-size: 150px; letter-spacing: -.04em; font-variant-numeric: tabular-nums; }}
.gv span {{ font-family: Serif; font-style: italic; font-size: 82px; color: #ffb3cd; margin-left: 6px; }}
.ex {{ margin-top: 16px; font-family: Mono; font-size: 21px; letter-spacing: .22em; color: rgba(255,255,255,.55); }}
.rail {{ position: absolute; left: 60px; right: 60px; top: 560px; height: 462px; border-radius: 40px; z-index: 12; opacity: 0; }}
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
/* Cree */
#cree {{ position: absolute; left: 0; top: 0; width: 820px; height: 820px; z-index: 30; opacity: 0; transform-origin: 410px 500px; pointer-events: none;
  filter: drop-shadow(0 24px 30px rgba(200,40,120,.22)); }}
#cshadow {{ position: absolute; left: 210px; top: 770px; width: 400px; height: 60px; border-radius: 50%; background: radial-gradient(closest-side, rgba(226,53,160,.35), rgba(226,53,160,0)); }}
#creeb {{ position: absolute; inset: 0; transform-origin: 50% 97.5%; }}
#creef {{ position: absolute; inset: 0; transform-origin: 50% 60%; }}
#creep {{ position: absolute; inset: 0; transform-origin: 50% 97.5%; }}
.cpose {{ position: absolute; inset: 0; opacity: 0; }}
.cpose img, .clids, .csw {{ position: absolute; inset: 0; width: 820px; height: 820px; }}
.csw {{ overflow: visible; }}
.lidg {{ opacity: 0; }}
.sweat {{ opacity: 0; transform-box: fill-box; transform-origin: 50% 0; }}
.csp {{ position: absolute; opacity: 0; }}
#bub {{ position: absolute; left: 600px; top: 0; width: 210px; height: 190px; opacity: 0; border-radius: 50% 50% 50% 14px; display: grid; place-items: center;
  transform-origin: 0 100%; background: linear-gradient(135deg, rgba(255,255,255,.8), rgba(255,255,255,.38)); backdrop-filter: blur(18px) saturate(1.7);
  -webkit-backdrop-filter: blur(18px) saturate(1.7); border: 2px solid rgba(255,255,255,.95); box-shadow: inset 0 2px 0 #fff, 0 20px 40px rgba(160,20,90,.28); }}
#bubt {{ font: 800 120px/1 Inter; background: linear-gradient(180deg, {MAG}, {PINK}); -webkit-background-clip: text; background-clip: text; color: transparent; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: check before you post 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="world" id="light">{blobs_l}</div>
      <div class="world" id="dark">{blobs_d}</div>
      <div id="panes">{panes}</div>
      <div id="cam"><div id="punch"><div id="drift">
        {chr(10).join(HTML)}
      </div></div></div>
      <div id="flash"></div><div id="stk0" class="stk"></div><div id="stk1" class="stk"></div><div id="stk2" class="stk"></div>
      <div id="liq"></div><div id="sweep"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set("#sweep", {{xPercent: -170}}, 0);
      tl.set("#liq", {{scale: .04}}, 0);
      tl.set(".stk", {{rotation: -24, xPercent: -260}}, 0);
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
