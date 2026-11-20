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
Cinema pass (owner's v1 notes, 2026-11-19): the sad half is letterboxed and cold; at "Creedom" the bars open, the grade warms,
focus pulls from her to Cree's glow with an anamorphic flare, and the music hands over to an uplifting track; "they stayed" gets
confetti, a second flare and sweeping spots; the followspot sways and the whole world drifts like a handheld camera.
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
CONF = 70

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

# the audience: chibi mascots, each one assembled from parts (hairstyle, head shape, face, colours): see build/chibi.py
from chibi import DEFS as CHIBI_DEFS, seated, walker  # noqa: E402

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
    row, chibis, seats = [], "", ""
    for s in range(n):
        x = x0 + s * (w + gap)
        has_ph = random.random() < .45
        turn = r >= 2 and random.random() < .6
        cw = w * 1.1
        chibis += seated(f"pp{pid}", x + w / 2 - cw / 2, -.72 * w, cw, turn=turn, phone=has_ph, style=f"--ph:{1 if has_ph else 0}")
        seats += f'<i class="seat" style="left:{x:.0f}px;width:{w:.0f}px;height:{h:.0f}px"></i>'
        row.append((pid, x + w / 2, yb, w, has_ph))
        pid += 1
    ROWS.append(row)
    seats_html += f'<div class="row" id="row{r}" style="top:{yb - h:.0f}px;height:{h:.0f}px">{chibis}{seats}<!--W{r}--></div>'

# the few who came: four chibis in rows 2-4, each with a standing walker in front of their row's seats
WALK = [(4, 4, -60), (5, len(ROWS[5]) - 4, 1130), (6, 6, -70), (4, len(ROWS[4]) - 3, 1120)]
WPID = set()
for i, (r, k, ex) in enumerate(WALK):
    pid_, cx, yb, w, _ = ROWS[r][k]
    WPID.add(pid_)
    ww = w * 1.25
    hh = ww * 1.7
    h = w * 1.05
    wk = walker(f"wk{i}", cx - ww / 2, h + .15 * w - hh, ww, hh)
    seats_html = seats_html.replace(f"<!--W{r}-->", wk + f"<!--W{r}-->")
WALK = [(ROWS[r][k], ex) for r, k, ex in WALK]
walkers = ""
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
FGS = [(-120, 300, 360), (200, 300, 330), (520, 300, 340), (840, 300, 360)]
fgseats = ("".join(seated(f"fp{i}", x + w / 2 - 138, 2040 - h - 1920 - 150, 276) for i, (x, w, h) in enumerate(FGS))
           + "".join(f'<i class="fgseat" style="left:{x}px;width:{w}px;height:{h}px"></i>' for x, w, h in FGS))
FG = f'<div id="fgl" style="position:absolute;left:0;right:0;top:1920px">{fgseats}</div>'
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
for i, ((pid_, cx, yb, w, _), _) in enumerate(WALK):
    ft(f"#pp{pid_}", t_fw + .1 * i, .4, f"{{opacity: 0, y: {w * .4:.0f}, scaleY: .7}}", "{opacity: 1, y: 0, scaleY: 1}", "back.out(2.2)")
    sfx("pop", t_fw + .1 * i)
t_lf = T("g2", "left")
head("h2b", [[("left", "rd"), ("in", ""), ("the", ""), ("first", "")], [("three", ""), ("seconds.", "")]], 250, "g2", size=104, after=t_lf)
for i, ((pid_, cx, yb, w, _), ex) in enumerate(WALK):
    tk = t_lf + .1 * i
    st(f"#pp{pid_}", tk, "{opacity: 0}")
    ft(f"#wk{i}", tk, .25, "{opacity: 1, scaleY: .7, y: 20}", "{opacity: 1, scaleY: 1, y: 0}", "back.out(2)")
    dirn = -1 if ex < cx else 1
    js(f'tl.to("#wk{i}", {{x: {ex - cx:.0f}, duration: 1.5, ease: "power1.in"}}, {tk + .25:.3f});')
    js(f'tl.fromTo("#wk{i}", {{rotation: {-4 + 3 * dirn}, y: 0}}, {{keyframes: [' + ", ".join(
        f'{{rotation: {(4 if k % 2 == 0 else -4) + 3 * dirn}, y: {-6 if k % 2 == 0 else 0}, duration: .18}}' for k in range(8))
       + f'], immediateRender: false}}, {tk + .25:.3f});')
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

# ---- 5 her next reel, checked: Cree projects the reel check (owner's note on the final, 2026-11-20) ----------------------------
# the voice holds a 1.8 s breath after "posted." (build/vo_insert.py) so the check can play out: scan, score counts up to
# 4.7 / 5, the six category chips tick, "Very good", then the panel folds into the stage screen and READY TO POST lights.
# The score is an example (marked on the panel), never a promise.
t_ck = T("g5", "checked")
t_po = T("g5", "posted")
t_nx = T0["g6"][0]                                            # "And this time"
head("h5", [[("It", ""), ("checked", "it"), ("her", ""), ("next", ""), ("reel", "")], [("before", ""), ("she", ""), ("posted.", "")]], 250, "g5", size=92)
to("#tc", T0["g5"][0] - .2, .2, "{opacity: 0}")
cam(T0["g5"][0] - .2, 540, 470, 1.35, .9)
to("#tbe", T0["g5"][0] - .2, .2, "{opacity: 0}")
ft("#rnew", t_ck, .5, "{opacity: 0, scale: 1.1}", "{opacity: 1, scale: 1}", "power3.out")
js(f'tl.fromTo("#tbb", {{width: "0%"}}, {{width: "100%", duration: {t_nx - t_ck:.2f}, ease: "none", immediateRender: false}}, {t_ck:.3f});')
js(f'tl.to("#sarm", {{rotation: 0, svgOrigin: "136 176", duration: .6, ease: "back.out(1.6)"}}, {t_ck:.3f});')
js(f'tl.to("#sscr", {{fill: "#ffd0e6", duration: .3}}, {t_ck:.3f});')
pose(t_ck - .15, "mag", flip=True)
# the panel beams up out of Cree's magnifier
ft("#abeam", t_ck, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
ft("#ana", t_ck + .05, .5, "{opacity: 0, scale: .25, y: 260}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.5)")
sfx("whoosh", t_ck)
sfx("riser_short", t_ck)
# scan the reel twice
for k in range(2):
    ft("#scan", t_ck + .4 + .6 * k, .6, "{y: 0, opacity: 1}", "{y: 400, opacity: 1}", "sine.inOut")
    sfx("glitch", t_ck + .45 + .6 * k)
st("#scan", t_ck + 1.6, "{opacity: 0}")
js(f'tl.fromTo("#adots", {{opacity: 1}}, {{opacity: .2, duration: .25, yoyo: true, repeat: 5, ease: "none", immediateRender: false}}, {t_ck + .2:.3f});')
# the score counts up while the chips tick in
T_SC = t_ck + 1.05
js(f'(() => {{ const sc = {{v: 0}}; tl.to(sc, {{v: 4.7, duration: 1.3, ease: "power2.out", onUpdate: () => {{ document.getElementById("scn").textContent = sc.v.toFixed(1); }}}}, {T_SC:.3f}); }})();')
for i in range(6):
    tk = T_SC + .15 + .19 * i
    ft(f"#ch{i}", tk, .3, "{opacity: 0, scale: .6, y: 16}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.6)")
    sfx("tick", tk)
t_vg = T_SC + 1.35
ft("#avg", t_vg, .3, "{opacity: 0, x: -20}", "{opacity: 1, x: 0}", "power3.out")
js(f'tl.fromTo("#abar", {{width: "0%"}}, {{width: "94%", duration: .55, ease: "power3.out", immediateRender: false}}, {t_vg:.3f});')
to("#ahd1", t_vg, .2, "{opacity: 0}")
ft("#ahd2", t_vg + .05, .25, "{opacity: 0}", "{opacity: 1}", "power2.out")
ft("#atk", t_vg + .05, .3, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1}", "back.out(3)")
js(f'tl.fromTo("#ascore", {{scale: 1}}, {{scale: 1.12, duration: .16, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_vg:.3f});')
sfx("ding2", t_vg)
sparkle(t_vg + .05, .7)
pose(t_vg, "cheer")
# fold the panel into the stage screen: READY TO POST
t_fd = t_nx - .75
to("#ana", t_fd, .4, "{opacity: 0, scale: .3, y: 300}", "power3.in")
to("#abeam", t_fd, .3, "{opacity: 0}")
sfx("whoosh", t_fd)
ft("#rdy", t_fd + .35, .35, "{opacity: 0, y: 30, scale: .6}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.4)")
sfx("ding", t_fd + .38)
pose(t_fd + .35, "proud")

# ---- 6 and this time they stayed: house lights, the seats fill, applause --------------------------------------------------------
t_and = T0["g6"][0]
t_st = T("g6", "stayed")
head("h6a", [[("And", ""), ("this", ""), ("time…", "")]], 260, "g6", size=124)
head("h6b", [[("they", ""), ("stayed.", "au")]], 250, "g6", size=170, after=T("g6", "they"))
cam(t_and - .1, 540, 1260, .78, 1.6, "power2.inOut")
sfx("whoosh_big", t_and - .1)
# the four who left come back in through the doors, smiling
for d in (0, 1):
    js(f'tl.fromTo("#dl{d}", {{opacity: 0}}, {{opacity: .9, duration: .25, yoyo: true, repeat: 1, repeatDelay: .6, immediateRender: false}}, {t_and - .3 + .1 * d:.3f});')
sfx("door", t_and - .25)
sfx("steps", t_and)
for i, ((pid_, cx, yb, w, _), ex) in enumerate(WALK):
    tk = t_and - .15 + .08 * i
    dirn = 1 if ex < cx else -1                               # walking back towards the seat
    st(f"#wk{i}", tk, f'{{"--happy": 1, x: {ex - cx:.0f}, rotation: 0}}')
    ft(f"#wk{i}", tk, .2, "{opacity: 0}", "{opacity: 1}", "power1.out")
    js(f'tl.to("#wk{i}", {{x: 0, duration: 1.0, ease: "power1.out"}}, {tk:.3f});')
    js(f'tl.fromTo("#wk{i}", {{rotation: {3 * dirn}, y: 0}}, {{keyframes: [' + ", ".join(
        f'{{rotation: {(5 if k % 2 == 0 else -5) + 3 * dirn}, y: {-9 if k % 2 == 0 else 0}, duration: .15}}' for k in range(6))
       + f', {{rotation: 0, y: 0, duration: .1}}], immediateRender: false}}, {tk:.3f});')
    st(f"#wk{i}", tk + 1.0, "{opacity: 0}")
    ft(f"#pp{pid_}", tk + 1.0, .3, f"{{opacity: 1, y: {-w * .2:.0f}}}", "{opacity: 1, y: 0}", "bounce.out")
    sfx("pop", tk + 1.0)
# then the whole house fills, row by row towards the camera
FILL0 = T("g6", "they") - .25
for r, row in enumerate(ROWS):
    for pid_, cx, yb, w, has_ph in row:
        if pid_ in WPID:
            continue
        tk = FILL0 + .14 * r + random.uniform(0, .18)
        ft(f"#pp{pid_}", tk, .4, f"{{opacity: 0, y: {w * .45:.0f}, scaleY: .65}}", "{opacity: 1, y: 0, scaleY: 1}", "back.out(2.2)")
    sfx("seat", FILL0 + .14 * r)
for i in range(4):
    ft(f"#fp{i}", FILL0 + 1.3 + .08 * i, .45, "{opacity: 0, y: 120}", "{opacity: 1, y: 0}", "back.out(1.8)")
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
# everyone cheers: arms (and phones) up, bouncing; some of the nearer ones turn round to the camera
cam(t_st + .1, 540, 1330, .92, 1.1, "power1.inOut")
js(f'tl.to(".cbs", {{"--arms": 1, duration: .18, stagger: {{each: .004, from: "random"}}}}, {t_st - .1:.3f});')
js(f'tl.fromTo("#rw .cbs", {{y: 0}}, {{y: -9, duration: .22, yoyo: true, repeat: 11, ease: "sine.inOut", stagger: {{each: .005, from: "random"}}, immediateRender: false}}, {t_st:.3f});')
js(f'tl.fromTo("#fgl .cbs", {{y: 0}}, {{y: -26, duration: .24, yoyo: true, repeat: 9, ease: "sine.inOut", stagger: .06, immediateRender: false}}, {t_st + .2:.3f});')
js(f'tl.to(".cbs.tn", {{"--turn": 1, duration: .14, stagger: {{each: .012, from: "random"}}}}, {t_st + .35:.3f});')
js(f'tl.fromTo(".cbs.tn", {{scaleX: 1}}, {{keyframes: [{{scaleX: .6, duration: .07}}, {{scaleX: 1, duration: .12, ease: "back.out(3)"}}], stagger: {{each: .012, from: "random"}}, immediateRender: false}}, {t_st + .3:.3f});')
js(f'tl.to(".cbs.hp", {{"--ph": .55, duration: .25, yoyo: true, repeat: 5, stagger: {{each: .01, from: "random"}}, ease: "sine.inOut"}}, {t_st + 1.0:.3f});')

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

# ---- cinema pass: letterbox, grade, rack focus, followspot sway, flares, sweeping spots, confetti, handheld drift -----------------
# the sad half plays in a cold, letterboxed frame; at "Creedom" the bars open, the grade warms and the music lifts
st("#lbT", 0, "{scaleY: 1}")
st("#lbB", 0, "{scaleY: 1}")
to("#lbT", t_cr - .1, .9, "{scaleY: 0}", "power3.inOut")
to("#lbB", t_cr - .1, .9, "{scaleY: 0}", "power3.inOut")
to("#cold", t_cr, 1.2, "{opacity: .35}", "power1.inOut")
to("#warmg", t_cr, 1.2, "{opacity: .45}", "power1.inOut")
punch(t_cr, 1.03)
# rack focus: the hall is soft in the close shots, sharp in the wide ones; at "Creedom" focus pulls from her to the front row
ft("#rbg", 0, 1.6, "{filter: 'blur(6px)'}", "{filter: 'blur(0px)'}", "power2.inOut")
to("#rbg", T0["g3"][0] - .3, .8, "{filter: 'blur(6px)'}", "power2.inOut")
to("#rbg", T0["g4"][0] - .2, .8, "{filter: 'blur(0px)'}", "power2.inOut")
ft("#star", t_cr - .15, .35, "{filter: 'blur(0px)'}", "{filter: 'blur(4px)'}", "power2.out")
to("#star", t_rd + .1, .5, "{filter: 'blur(0px)'}", "power2.inOut")
# the followspot breathes like a real operator is holding it
js(f'tl.fromTo("#beam", {{rotation: -1.4}}, {{rotation: 1.4, duration: 2.6, yoyo: true, repeat: {int(t_cr // 2.6)}, ease: "sine.inOut", immediateRender: false}}, 0);')
# anamorphic flares: Cree's glow, then the house lights
ft("#flare1", t_cr - .05, .35, "{opacity: 0, scaleX: .1}", "{opacity: 1, scaleX: 1}", "power3.out")
to("#flare1", t_cr + .5, 1.0, "{opacity: 0, scaleX: 1.4}", "power2.in")
ft("#flare2", t_st - .05, .4, "{opacity: 0, scaleX: .1}", "{opacity: .9, scaleX: 1}", "power3.out")
to("#flare2", t_st + .6, 1.2, "{opacity: 0, scaleX: 1.5}", "power2.in")
# sweeping spots over the full house and across the falling curtain
for i, (a0, a1) in enumerate(((-28, 18), (28, -18))):
    ft(f"#sw{i}", t_and + .3, .6, "{opacity: 0}", "{opacity: .8}", "power1.out")
    js(f'tl.fromTo("#sw{i}", {{rotation: {a0}}}, {{rotation: {a1}, duration: 1.6, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_and + .3:.3f});')
# confetti falls on "stayed"
for i in range(CONF):
    x0, dx = random.uniform(0, 1080), random.uniform(-160, 160)
    t0 = t_st - .1 + random.uniform(0, 1.6)
    d = random.uniform(2.6, 4.2)
    js(f'tl.fromTo("#cf{i}", {{x: {x0:.0f}, y: -60, rotation: {random.randint(0, 180)}, rotationX: 0, opacity: 1}}, '
       f'{{x: {x0 + dx:.0f}, y: 2000, rotation: {random.randint(360, 900)}, rotationX: {random.choice((540, 720, 900))}, opacity: 1, duration: {d:.2f}, ease: "none", immediateRender: false}}, {t0:.3f});')
sfx("whoosh", t_st - .1)
# handheld drift on everything in the world
js(f'tl.fromTo("#hand", {{x: -6, y: 4}}, {{x: 6, y: -4, duration: 3.7, yoyo: true, repeat: {int(DUR / 3.7)}, ease: "sine.inOut", immediateRender: false}}, 0);')

# ---- ambience: dust in the beam, sconce shimmer, Cree breathing ------------------------------------------------------------------
for i in range(22):
    js(f'tl.fromTo("#mo{i}", {{x: 0, y: 0}}, {{x: {random.randint(-30, 30)}, y: {random.randint(-120, -40)}, duration: {random.uniform(3, 6):.2f}, yoyo: true, repeat: 5, '
       f'ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -8, duration: .7, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .7)}, immediateRender: false}}, 0);')
js(f'tl.fromTo("#punch", {{rotation: -.25}}, {{rotation: .25, duration: 3, yoyo: true, repeat: {int(DUR / 3)}, ease: "sine.inOut", immediateRender: false}}, 0);')

CHIPS = [("Hook", 5), ("Pacing", 4), ("Ending", 5), ("Visuals", 5), ("Audio", 4), ("CTA", 5)]
ANAH = ('<div class="ahd"><img src="assets/img/poses/mag.png" alt=""><span id="ahd1">CREE · CHECKING YOUR REEL<b id="adots">…</b></span>'
        f'<span id="ahd2">CREE · REEL CHECKED</span><i class="atick" id="atk">{TICK}</i></div>'
        '<div class="athumb"><i class="asil"></i><b data-layout-ignore>Your best<br>moment,<br>first.</b><i id="scan"></i>'
        '<i class="abr tl"></i><i class="abr tr"></i><i class="abr bl"></i><i class="abr br"></i></div>'
        '<div class="aright"><div class="alab">REEL SCORE</div><div id="ascore"><span id="scn">0.0</span><small>/ 5</small></div>'
        '<div id="avg">Very good</div><div class="atrack"><i id="abar"></i></div><div class="achips">'
        + "".join(f'<span class="chip" id="ch{i}">{n} <b>{v}</b></span>' for i, (n, v) in enumerate(CHIPS))
        + '</div><div class="aex">Example score</div></div>')
COLS = ("#ffd27a", "#f5c062", "#F343A2", "#ff9fd0", "#ffffff", "#ff7a59")
CONFH = "".join(f'<i class="cf" id="cf{i}" style="background:{random.choice(COLS)};width:{random.randint(12, 20)}px;height:{random.randint(22, 34)}px"></i>' for i in range(CONF))
WORLD = WORLD.replace('<i id="crglow"', '<i class="flare" id="flare1" style="top:1080px"></i><i class="flare" id="flare2" style="top:320px"></i>'
                      '<i class="sweep" id="sw0" style="left:60px"></i><i class="sweep" id="sw1" style="left:900px"></i><i id="crglow"')
WORLD = CHIBI_DEFS + WORLD
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
      <div id="punch"><div id="hand">
        <div class="rig" id="rbg" data-layout-allow-overflow>{BG}{HOUSE}</div>
        <div class="rig" id="rw" data-layout-allow-overflow data-layout-allow-overlap>{WORLD}</div>
        <div class="rig" id="rfg" data-layout-allow-overflow>{FG}</div>
      </div></div>
      <div id="abeam"></div><div id="ana" data-layout-allow-overlap>{ANAH}</div>
      <div id="conf">{CONFH}</div><div id="lbT"></div><div id="lbB"></div>
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
json.dump({"dur": DUR, "music_switch": round(t_cr, 3), "lines": T0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {pid} seats")
