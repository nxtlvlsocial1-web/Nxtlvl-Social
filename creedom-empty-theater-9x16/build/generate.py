"""Creators 100X x Creedom "The Empty Theater" (9:16, 2.5D): writes index.html, plan/sfx_events.json and plan/edit.json
from plan/words.json.

Script approved by the owner on 2026-11-19, voiced with ElevenLabs (Jessica, Eleven v3; build/vo_el.py take 3, pauses
trimmed by build/vo_tight.py, word times by build/vo_words.py).

One theater, shot through three parallax camera rigs (hall walls, the stage-and-seats world, soft-focus nearest seat backs):
  0 hook: dark; a spotlight clunks on a creator on stage, phone raised like a microphone; the camera dollies back;
  1 the reveal: a red-velvet theater, every seat empty, her reel on the giant screen reads "47 views";
  2 the few who came stand up and walk out through the glowing EXIT doors as 0:03 flashes on the screen; the spot flickers;
  3 close on her, alone in the light; the phone lowers;
  4 the turn: a pink glow rises in the front row: Cree with his magnifier; he hops onto the stage, the screen rewinds and
    0:01-0:03 lights red ("exactly where they left");
  5 her next reel plays bright on the screen, READY TO POST;
  6 "and this time... they stayed": the house lights come up gold, the seats fill row by row towards the camera, phone
    lights glow like stars, applause swells;
  7 CTA: the curtain falls and the marquee lights COMMENT GROW.
Claims stay within what Creedom does (reads the account, shows where viewers left, checks a reel before posting).
python3 build/generate.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT, punch  # noqa: E402
from fx import cree_html, cree_to, pose, cree_hop, cree_wiggle, blink, sparkle, P  # noqa: E402

random.seed(7)
DUR = round(L1["g7"] + 1.7, 2)

# ---- headlines (screen space) --------------------------------------------------------------------------------------------
HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, top, line, size=100, after=0.0):
    spoken, k, out, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?…"), None
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
    HTMLS.append(f'<div class="head" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .05, .34, "{opacity: 0, filter: 'blur(12px)', y: 22}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .3, .2, "{opacity: 0, filter: 'blur(14px)', y: -36}", "power2.in")
    OPEN[0] = hid


# ---- camera ----------------------------------------------------------------------------------------------------------------
RIGS = (("#rbg", .55), ("#rw", 1.0), ("#rfg", 1.6))


def cam(t, cx, cy, z, d=1.0, ease="power2.inOut", setonly=False):
    for sel, f in RIGS:
        zf = 1 + (z - 1) * f
        cxf, cyf = 540 + (cx - 540) * f, 960 + (cy - 960) * f
        props = f"x: {540 - cxf * zf:.1f}, y: {960 - cyf * zf:.1f}, scale: {zf:.4f}"
        js(f'gsap.set("{sel}", {{{props}}});' if setonly else f'tl.to("{sel}", {{{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def shake(t, amp=8, n=5, per=.04):
    ks = ", ".join(f'{{x: {random.choice((-1, 1)) * amp * (1 - k / n):.1f}, y: {random.choice((-1, 1)) * amp * .6 * (1 - k / n):.1f}, duration: {per}}}' for k in range(n))
    js(f'tl.fromTo("#punch", {{x: 0, y: 0}}, {{keyframes: [{ks}, {{x: 0, y: 0, duration: {per}}}], immediateRender: false}}, {t:.3f});')


TICK = ('<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="#2fbf71"/><path d="M13 25 L21 33 L36 16" fill="none" stroke="#fff" stroke-width="5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

# =======================================================================================================================
# THE WORLD
# background rig: hall, side walls, sconces, balconies, exits
sconces = ""
for i, (x, y) in enumerate([(-80, 700), (-120, 1150), (1150, 700), (1190, 1150)]):
    sconces += f'<i class="sglow" id="sg{i}" style="left:{x}px;top:{y}px"></i><i class="sconce" style="left:{x - 15}px;top:{y - 30}px"></i>'
BG = (f'<div class="hall"></div><div class="wallL"></div><div class="wallR"></div>{sconces}'
      '<div class="balc" style="left:-260px;top:520px;width:420px"></div><div class="balc" style="left:920px;top:520px;width:420px"></div>')

# world rig: proscenium, stage, screen, star, seats
FL = "".join(f'<i class="fl" style="left:{150 + 62 * i}px"></i>' for i in range(13))
motes = "".join(f'<i class="mote" id="mo{i}" style="left:{random.randint(430, 650)}px;top:{random.randint(200, 940)}px;opacity:{random.uniform(.2, .8):.2f}"></i>' for i in range(22))
bulbs = "".join(f'<i class="bulb" id="bl{i}" style="left:{230 + 8 + 30.5 * (i % 20)}px;top:{150 - 20 if i < 20 else 150 + 108}px"></i>' for i in range(40))
STAR = ('<div id="star"><svg viewBox="0 0 190 340"><defs>'
        '<radialGradient id="ssk" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffe0cc"/><stop offset="1" stop-color="#e8a98c"/></radialGradient>'
        '<radialGradient id="sdr" cx=".3" cy=".2" r=".9"><stop offset="0" stop-color="#ffb0d4"/><stop offset=".6" stop-color="#e2559c"/><stop offset="1" stop-color="#a8306c"/></radialGradient>'
        '<radialGradient id="shr" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6b3b3f"/><stop offset="1" stop-color="#2e1517"/></radialGradient></defs>'
        '<rect x="70" y="250" width="20" height="86" rx="10" fill="#3a2430"/><rect x="100" y="250" width="20" height="86" rx="10" fill="#3a2430"/>'
        '<path d="M42 268 C42 180 64 140 95 140 C126 140 148 180 148 268 Z" fill="url(#sdr)"/>'
        '<g id="shead"><circle cx="95" cy="88" r="52" fill="url(#shr)"/><circle cx="95" cy="32" r="24" fill="url(#shr)"/>'
        '<ellipse cx="99" cy="98" rx="42" ry="46" fill="url(#ssk)"/>'
        '<path d="M56 90 C58 56 86 42 108 44 C132 46 146 64 145 88 C126 72 104 68 84 74 C72 78 62 84 56 90 Z" fill="url(#shr)"/>'
        '<circle cx="78" cy="118" r="8" fill="#f59bb1" opacity=".6"/><circle cx="124" cy="116" r="8" fill="#f59bb1" opacity=".6"/>'
        '<ellipse cx="88" cy="102" rx="4.5" ry="6" fill="#2a1220"/><ellipse cx="114" cy="101" rx="4.5" ry="6" fill="#2a1220"/>'
        '<path id="sm_open" d="M92 124 Q101 134 110 124 Z" fill="#9a3b4e"/>'
        '<path id="sm_sad" d="M92 130 Q101 122 110 130" fill="none" stroke="#9a3b4e" stroke-width="3.5" stroke-linecap="round" opacity="0"/>'
        '<path id="sm_smile" d="M88 122 Q101 140 114 122 Z" fill="#9a3b4e" opacity="0"/></g>'
        '<g id="sarm"><path d="M136 176 C160 168 164 140 146 118" fill="none" stroke="url(#sdr)" stroke-width="24" stroke-linecap="round"/>'
        '<circle cx="144" cy="114" r="11" fill="url(#ssk)"/><rect x="128" y="76" width="26" height="44" rx="6" fill="#1a1016"/>'
        '<rect id="sscr" x="131" y="79" width="20" height="38" rx="4" fill="#ffd9ea"/></g>'
        '<path d="M50 180 C34 210 40 240 52 250" fill="none" stroke="url(#sdr)" stroke-width="22" stroke-linecap="round"/></svg></div>')

# seats: 9 rows from the stage towards the camera, bigger and lower as they come closer
ROWS = []
seats_html = ""
pid = 0
for r in range(9):
    yb = 1112 + 70 * r + 9 * r * r
    w = 50 + 9 * r
    h = w * 1.05
    gap = w * .2
    span = 760 + 130 * r
    n = int(span // (w + gap))
    x0 = 540 - (n * (w + gap) - gap) / 2
    row = []
    seats_html += f'<div class="row" style="top:{yb - h:.0f}px;height:{h:.0f}px">'
    for s in range(n):
        x = x0 + s * (w + gap)
        hd, shw = w * .44, w * .86
        ph = (f'<i class="ph" id="ph{pid}" style="left:{-w * .07:.0f}px;top:{-w * .16:.0f}px;width:{w * .14:.0f}px;height:{w * .22:.0f}px"></i>' if random.random() < .45 else "")
        seats_html += (f'<i class="seat" style="left:{x:.0f}px;width:{w:.0f}px;height:{h:.0f}px"><i class="ppl" id="pp{pid}" style="width:0;height:0">'
                       f'<i class="sh" style="left:{-shw / 2:.0f}px;top:{-w * .3:.0f}px;width:{shw:.0f}px;height:{w * .55:.0f}px"></i>'
                       f'<i class="hd" style="left:{-hd / 2:.0f}px;top:{-w * .3 - hd * .9:.0f}px;width:{hd:.0f}px;height:{hd:.0f}px"></i>{ph}</i></i>')
        row.append((pid, x + w / 2, yb, w, bool(ph)))
        pid += 1
    seats_html += "</div>"
    ROWS.append(row)

# the few who came: four walkers in rows 2-4
WALK = [(ROWS[2][3], -40), (ROWS[3][len(ROWS[3]) - 4], 1120), (ROWS[4][5], -60), (ROWS[2][len(ROWS[2]) - 3], 1110)]
walkers = ""
for i, ((_, cx, yb, w, _), _) in enumerate(WALK):
    s = w * 1.1
    walkers += (f'<div class="walker" id="wk{i}" style="left:{cx - s / 2:.0f}px;top:{yb - s * 2.1:.0f}px;width:{s:.0f}px;height:{s * 2:.0f}px">'
                f'<i class="hd" style="left:{s * .3:.0f}px;top:0;width:{s * .4:.0f}px;height:{s * .4:.0f}px"></i>'
                f'<i class="sh" style="left:{s * .1:.0f}px;top:{s * .42:.0f}px;width:{s * .8:.0f}px;height:{s * 1.5:.0f}px"></i></div>')
WORLD = (f'<div class="backwall"></div><div class="screen" id="screen"><div class="reelbg"><i></i></div>'
         f'<div class="reelnew" id="rnew"><i></i><b data-layout-ignore>Your best<br>moment,<br>first.</b></div><div class="rew" id="rew"></div>'
         f'<div class="tc" id="tc">0:03</div><div class="sign47" id="s47" style="left:0;top:190px;width:340px;font-size:84px;opacity:0">47<small>VIEWS</small></div>'
         f'<div class="rdy" id="rdy">{TICK}READY TO POST</div><div class="tbar"><b id="tbb"></b><em id="tbe"></em></div></div>'
         f'<div class="stagefloor"></div><div class="stagelip"></div>{FL}'
         f'<div class="frame"></div><div class="curtain" id="curL"></div><div class="curtain" id="curR"></div>'
         f'<div class="cfull" id="cfL"></div><div class="cfull" id="cfR"></div>'
         f'<div class="valance"></div><div class="marq" id="marq" data-layout-ignore><b id="mq">COMMENT GROW</b></div>{bulbs}'
         f'<div class="beam" id="beam"></div><div class="pool" id="pool"></div>{motes}{STAR}'
         f'<div class="door" style="left:-90px;top:1180px"><i class="doorlight" id="dl0"></i></div><div class="exit" style="left:-70px;top:1120px">EXIT</div>'
         f'<div class="door" style="left:1040px;top:1180px"><i class="doorlight" id="dl1"></i></div><div class="exit" style="left:1050px;top:1120px">EXIT</div>'
         f'{seats_html}{walkers}<i id="crglow" style="left:540px;top:1080px"></i>')
fgseats = "".join(f'<i class="fgseat" style="left:{x}px;width:{w}px;height:{h}px"><i class="ppl" id="fp{i}" style="width:0;height:0;bottom:62%">'
                  f'<i class="sh" style="left:-130px;top:-90px;width:260px;height:170px"></i><i class="hd" style="left:-66px;top:-210px;width:132px;height:132px"></i></i></i>'
                  for i, (x, w, h) in enumerate([(-120, 300, 360), (200, 300, 330), (520, 300, 340), (840, 300, 360)]))
FG = f'<div style="position:absolute;left:0;right:0;top:1920px">{fgseats}</div>'
HOUSE = '<div class="houselight" id="house"></div>'

# =======================================================================================================================
# TIMELINE
T0 = {k: (L0[k], L1[k]) for k in LINES}
cam(0, 540, 820, 2.5, setonly=True)
st("#beam", 0, "{opacity: .35}")
st("#pool", 0, "{opacity: .35}")

# ---- 0 hook: the spotlight clunks on, dolly back ------------------------------------------------------------------------------
head("h0", [[("She", ""), ("gave", ""), ("every", ""), ("reel", "")], [("everything", "au"), ("she", ""), ("had.", "")]], 250, "g0", size=96)
ft("#beam", .08, .12, "{opacity: .35}", "{opacity: 1}", "power4.in")
ft("#pool", .08, .12, "{opacity: .35}", "{opacity: 1}", "power4.in")
sfx("clunk", .06)
js('tl.fromTo("#star", {scaleY: .97}, {scaleY: 1, duration: 1.2, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}, 0);')
t_ev = T("g0", "everything")
js(f'tl.to("#sarm", {{rotation: -6, svgOrigin: "136 176", duration: .6, yoyo: true, repeat: 1, ease: "sine.inOut"}}, {t_ev:.3f});')
cam(.25, 540, 1050, .8, 4.6, "power2.inOut")
sfx("whoosh_big", .3)

# ---- 1 the reveal: every seat empty, 47 views ----------------------------------------------------------------------------------
t_em = T("g1", "empty")
head("h1", [[("the", ""), ("same", "")], [("empty", "dim"), ("room.", "")]], 250, "g1", size=120, after=T("g1", "the"))
ft("#s47", T("g1", "night"), .5, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2)")
sfx("ding2", T("g1", "night"))
js(f'tl.to("#s47", {{opacity: .55, duration: .08, yoyo: true, repeat: 3}}, {t_em:.3f});')
for i in range(4):
    js(f'tl.fromTo("#sg{i}", {{opacity: .12}}, {{opacity: .05, duration: .3, yoyo: true, repeat: 1, immediateRender: false}}, {t_em + .1 * i:.3f});')

# ---- 2 the few who came, leave at 0:03 -----------------------------------------------------------------------------------------
t_fw = T("g2", "few")
head("h2a", [[("The", ""), ("few", ""), ("who", ""), ("came…", "")]], 250, "g2", size=110)
cam(T0["g2"][0] - .2, 540, 1050, .86, 1.2)
for i in range(4):
    ft(f"#wk{i}", t_fw + .08 * i, .4, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "power2.out")
t_lf = T("g2", "left")
head("h2b", [[("left", "rd"), ("in", ""), ("the", ""), ("first", "")], [("three", ""), ("seconds.", "")]], 250, "g2", size=104, after=t_lf)
for i, (_, ex) in enumerate(WALK):
    tk = t_lf + .1 * i
    js(f'tl.to("#wk{i}", {{scaleY: 1.12, duration: .25, ease: "power2.out"}}, {tk:.3f});')
    cx = WALK[i][0][1]
    js(f'tl.to("#wk{i}", {{x: {ex - cx:.0f}, duration: 1.5, ease: "power1.in"}}, {tk + .25:.3f});')
    js(f'tl.fromTo("#wk{i}", {{rotation: -3}}, {{rotation: 3, duration: .18, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}}, {tk + .25:.3f});')
    to(f"#wk{i}", tk + 1.55, .2, "{opacity: 0}")
    sfx("seat", tk)
sfx("steps", t_lf + .3)
for d in (0, 1):
    js(f'tl.fromTo("#dl{d}", {{opacity: 0}}, {{opacity: .9, duration: .2, yoyo: true, repeat: 1, repeatDelay: .5, immediateRender: false}}, {t_lf + 1.2 + .15 * d:.3f});')
sfx("door", t_lf + 1.9)
t_th = T("g2", "three")
ft("#tc", t_th - .05, .25, "{opacity: 0, scale: 2}", "{opacity: 1, scale: 1}", "power4.in")
to("#tc", T0["g2"][1] + .3, .3, "{opacity: 0}")
to("#s47", t_th - .1, .2, "{opacity: 0}")
sfx("error", t_th)
for k, dt in enumerate((.0, .12, .2, .34)):
    st("#beam", t_th + .2 + dt, f"{{opacity: {(.45, 1, .55, 1)[k]}}}")
    st("#pool", t_th + .2 + dt, f"{{opacity: {(.45, 1, .55, 1)[k]}}}")
sfx("clunk", t_th + .2)

# ---- 3 alone in the light ----------------------------------------------------------------------------------------------------
head("h3a", [[("She", ""), ("didn't", ""), ("need", "")], [("more", ""), ("effort.", "dim")]], 250, "g3", size=112)
cam(T0["g3"][0] - .3, 540, 820, 2.2, 1.2)
cam(T0["g3"][0] + 1.0, 540, 820, 2.4, T0["g4"][0] - .25 - (T0["g3"][0] + 1.0), "none")
st("#sm_open", T0["g3"][0], "{opacity: 0}")
st("#sm_sad", T0["g3"][0], "{opacity: 1}")
js(f'tl.to("#shead", {{rotation: -7, svgOrigin: "95 140", duration: .7, ease: "sine.inOut"}}, {T0["g3"][0]:.3f});')
t_ne = T("g3", "needed")
head("h3b", [[("She", ""), ("needed", ""), ("to", "")], [("know", ""), ("why.", "it")]], 250, "g3", size=124, after=t_ne - .2)
js(f'tl.to("#sarm", {{rotation: 58, svgOrigin: "136 176", duration: .8, ease: "power2.inOut"}}, {T("g3", "why") - .3:.3f});')
js(f'tl.to("#sscr", {{fill: "#6a5a64", duration: .4}}, {T("g3", "why"):.3f});')

# ---- 4 the turn: Cree's glow in the front row, onto the stage, the screen rewinds ---------------------------------------------------
t_cr = T("g4", "Creedom")
head("h4a", [[("Creedom", "it"), ("read", ""), ("her", "")], [("whole", ""), ("account,", "")]], 250, "g4", size=110)
cam(T0["g4"][0] - .2, 540, 1020, 1.25, 1.0)
ft("#crglow", T0["g4"][0], .8, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}", "power2.out")
sfx("riser", T0["g4"][0] - .2)
CF = (540, 1104, .2)                                          # Cree on the front-row seat (feet y)
cree_to(T0["g4"][0] - .05, *P(*CF), d=.01)
st("#cree", t_cr - .1, "{opacity: 1}")
pose(t_cr - .1, "mag", flip=False, squash=False)
ft("#creeb", t_cr - .1, .4, "{y: 120}", "{y: 0}", "back.out(1.6)")
sparkle(t_cr, .8)
sfx("ding", t_cr)
t_rd = T("g4", "read")
CS = (690, 1000, .22)                                         # Cree on the stage, right of her
js(f'tl.to("#cree", {{x: {P(*CS)[0] - 410:.0f}, y: {P(*CS)[1] - 500:.0f}, scale: {CS[2]}, duration: .7, ease: "power2.inOut"}}, {t_rd + .1:.3f});')
js(f'tl.fromTo("#creeb", {{y: 0}}, {{keyframes: [{{y: -140, duration: .35, ease: "power2.out"}}, {{y: 0, duration: .35, ease: "power2.in"}}], immediateRender: false}}, {t_rd + .1:.3f});')
to("#crglow", t_rd + .1, .7, f"{{x: {CS[0] - 540}, y: {CS[1] - 1080}, opacity: .7}}", "power2.inOut")
pose(t_rd + .1, "cheer")
pose(t_rd + .85, "point", flip=True)
sfx("pop", t_rd + .8)
cam(t_rd + .2, 560, 620, 1.45, 1.1)
t_sh = T("g4", "showed")
head("h4b", [[("showed", ""), ("her", ""), ("exactly", "")], [("where", ""), ("they", ""), ("left.", "rd")]], 250, "g4", size=104, after=t_sh)
st("#rew", t_sh - .3, "{opacity: 1}")
js(f'tl.fromTo("#rew", {{backgroundPositionY: "0px"}}, {{backgroundPositionY: "-200px", duration: .5, ease: "none", immediateRender: false}}, {t_sh - .3:.3f});')
st("#rew", t_sh + .2, "{opacity: 0}")
sfx("whoosh", t_sh - .3)
js(f'tl.fromTo("#tbb", {{width: "60%"}}, {{width: "9%", duration: .5, ease: "power3.inOut", immediateRender: false}}, {t_sh - .3:.3f});')
t_wh = T("g4", "where")
ft("#tbe", t_wh, .25, "{opacity: 0, scaleY: .3}", "{opacity: 1, scaleY: 1}", "back.out(3)")
ft("#tc", t_wh, .25, "{opacity: 0, scale: 1.6}", "{opacity: 1, scale: 1}", "power4.in")
sfx("error", t_wh)
punch(t_wh + .05, 1.04)
st("#sm_sad", T("g4", "left"), "{opacity: 0}")
st("#sm_open", T("g4", "left"), "{opacity: 1}")
js(f'tl.to("#shead", {{rotation: 0, svgOrigin: "95 140", duration: .5, ease: "sine.inOut"}}, {T("g4", "left"):.3f});')

# ---- 5 her next reel, checked ------------------------------------------------------------------------------------------------
t_ck = T("g5", "checked")
head("h5", [[("It", ""), ("checked", "it"), ("her", ""), ("next", ""), ("reel", "")], [("before", ""), ("she", ""), ("posted.", "")]], 250, "g5", size=92)
to("#tc", T0["g5"][0] - .2, .2, "{opacity: 0}")
cam(T0["g5"][0] - .2, 540, 600, 1.35, .9)
to("#tbe", T0["g5"][0] - .2, .2, "{opacity: 0}")
ft("#rnew", t_ck, .5, "{opacity: 0, scale: 1.1}", "{opacity: 1, scale: 1}", "power3.out")
js(f'tl.fromTo("#tbb", {{width: "0%"}}, {{width: "100%", duration: {T0["g5"][1] - t_ck + .3:.2f}, ease: "none", immediateRender: false}}, {t_ck:.3f});')
sfx("ding2", t_ck)
ft("#rdy", T("g5", "posted") - .1, .35, "{opacity: 0, y: 30, scale: .6}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.4)")
sfx("ding", T("g5", "posted"))
js(f'tl.to("#sarm", {{rotation: 0, svgOrigin: "136 176", duration: .6, ease: "back.out(1.6)"}}, {t_ck:.3f});')
js(f'tl.to("#sscr", {{fill: "#ffd0e6", duration: .3}}, {t_ck:.3f});')
pose(T("g5", "posted"), "proud")

# ---- 6 and this time they stayed: house lights, the seats fill, applause --------------------------------------------------------
t_and = T0["g6"][0]
t_st = T("g6", "stayed")
head("h6a", [[("And", ""), ("this", ""), ("time…", "")]], 260, "g6", size=124)
head("h6b", [[("they", ""), ("stayed.", "au")]], 250, "g6", size=170, after=T("g6", "they"))
cam(t_and - .1, 540, 1260, .78, 1.6, "power2.inOut")
sfx("whoosh_big", t_and - .1)
FILL0 = T("g6", "they") - .25
for r, row in enumerate(ROWS):
    for pid_, cx, yb, w, has_ph in row:
        tk = FILL0 + .14 * r + random.uniform(0, .18)
        ft(f"#pp{pid_}", tk, .35, "{opacity: 0, y: 14}", "{opacity: 1, y: 0}", "power2.out")
        if has_ph:
            ft(f"#ph{pid_}", tk + .5 + random.uniform(0, .6), .25, "{opacity: 0}", "{opacity: 1}", "power2.out")
    sfx("seat", FILL0 + .14 * r)
for i in range(4):
    ft(f"#fp{i}", FILL0 + 1.3 + .08 * i, .4, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "power2.out")
ft("#house", t_and + .2, 2.0, "{opacity: 0}", "{opacity: 1}", "power1.inOut")
for i in range(4):
    to(f"#sg{i}", t_and + .2, 1.6, "{opacity: .9}", "power1.inOut")
to("#cold", t_and, 1.8, "{opacity: 0}", "power1.inOut")
to("#warmg", t_and, 1.8, "{opacity: 1}", "power1.inOut")
to("#beam", t_and + .4, 1.4, "{opacity: .45}")
sfx("applause", t_st - .1)
sfx("bell", t_st)
st("#sm_open", t_st, "{opacity: 0}")
st("#sm_smile", t_st, "{opacity: 1}")
js(f'tl.to("#shead", {{rotation: 5, svgOrigin: "95 140", duration: .4, ease: "back.out(2)"}}, {t_st:.3f});')
pose(t_st, "cheer")
cree_hop(t_st + .05, 70, 2)
js(f'tl.to(".ph", {{opacity: .5, duration: .25, yoyo: true, repeat: 5, stagger: {{each: .01, from: "random"}}, ease: "sine.inOut"}}, {t_st + .9:.3f});')

# ---- 7 CTA: COMMENT GROW lights over the full house, then the curtain falls ---------------------------------------------------
t_cm = T("g7", "Comment")
t_gw = T("g7", "GROW")
t_an = T("g7", "and")
ft("#cta1", t_cm - .05, .3, "{opacity: 0, y: 30, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "power3.out")
ft("#cta2", t_gw - .05, .4, "{opacity: 0, scale: 1.5, filter: 'blur(14px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "power4.out")
punch(t_gw, 1.05)
sfx("click", t_cm)
sfx("ding", t_gw)
js(f'tl.to(".bulb", {{backgroundColor: "#ffe7a8", boxShadow: "0 0 12px 4px rgba(255,210,120,.9)", duration: .05, stagger: .02}}, {t_cm:.3f});')
js(f'tl.to("#marq", {{color: "#ffd27a", textShadow: "0 0 12px rgba(255,200,100,.9), 0 0 40px rgba(255,170,60,.7)", duration: .3}}, {t_gw - .1:.3f});')
js(f'tl.to(".bulb", {{opacity: .4, duration: .2, yoyo: true, repeat: 7, stagger: {{each: .03, from: "edges"}}}}, {t_gw + .4:.3f});')
js(f'tl.fromTo("#cta2", {{scale: 1}}, {{scale: 1.04, duration: .5, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_gw + .5:.3f});')
head("h7", [[("and", ""), ("I'll", ""), ("send", ""), ("you", "")], [("the", ""), ("secret.", "it")]], 250, "g7", size=96, after=t_an)
cam(t_an - .3, 540, 560, 1.0, 1.0)
to("#cfL", t_an - .25, .8, "{x: 0}", "power3.inOut")
to("#cfR", t_an - .25, .8, "{x: 0}", "power3.inOut")
sfx("whoosh_big", t_an - .3)

# ---- ambience: dust in the beam, sconce shimmer, Cree breathing ------------------------------------------------------------------
for i in range(22):
    js(f'tl.fromTo("#mo{i}", {{x: 0, y: 0}}, {{x: {random.randint(-30, 30)}, y: {random.randint(-120, -40)}, duration: {random.uniform(3, 6):.2f}, yoyo: true, repeat: 5, '
       f'ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -8, duration: .7, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .7)}, immediateRender: false}}, 0);')
js(f'tl.fromTo("#punch", {{rotation: -.25}}, {{rotation: .25, duration: 3, yoyo: true, repeat: {int(DUR / 3)}, ease: "sine.inOut", immediateRender: false}}, 0);')

WORLD += cree_html()
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: The Empty Theater 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="punch">
        <div class="rig" id="rbg" data-layout-allow-overflow>{BG}{HOUSE}</div>
        <div class="rig" id="rw" data-layout-allow-overflow data-layout-allow-overlap>{WORLD}</div>
        <div class="rig" id="rfg" data-layout-allow-overflow>{FG}</div>
      </div>
      <div id="cold"></div><div id="warmg"></div><div id="vig"></div><div id="black"></div>
      <div id="scrim"></div>
      {chr(10).join(HTMLS)}
      <div id="cta"><b id="cta1">Comment</b><b id="cta2">GROW</b></div>
      <div id="grain"></div><div id="flash"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      tl.progress(1, true).progress(0, true);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "lines": T0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {pid} seats")
