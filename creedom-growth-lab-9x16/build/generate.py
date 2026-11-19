"""Creators 100X x Creedom "The Growth Lab" (9:16, 2.5D designer-toy diorama): writes index.html, plan/sfx_events.json and
plan/edit.json from plan/words.json.

Script approved by the owner on 2026-11-19, voiced with ElevenLabs (Jessica, Eleven v3; build/vo_el.py take 2, pauses
trimmed by build/vo_tight.py, word times by build/vo_words.py).

One continuous miniature world on a desk, shot through a camera that moves in depth (three parallax rigs: wall and
shelf, the desk world, soft-focus foreground props) with tilt-shift blur at the top and bottom of the frame:
  0 hook: golden hour; a creator (clay figure) at her desk; her account is a plant in a glass cloche, its leaves are reel
    thumbnails, wilting and grey; a hanging tag counts her views down;
  1 "it wasn't the algorithm": a grey ALGORITHM? cloud puffs away; the camera pushes in on one dry leaf, tagged 0:03;
  2 "Creedom read her whole account": Cree pops into the cloche, the Creedom plaque lights on the base, the roots light
    up like data veins, then one goes red and a red pulse runs up the stem to the dry leaf (KILLING VIEWS);
  3 "checked the hook, and fixed it": magnifier, snips; the dry leaf falls, a fresh glowing leaf unfurls; tag READY TO POST;
  4 "planted what to post next": three glowing seeds with bookmark flags drop into the soil and sprout;
  5 "the best part": time-lapse: the window light sweeps, the plant colours up and grows, flowers open as hearts, a
    chart stake rises; the creator smiles and hearts float from her phone;
  6 CTA: a "Comment GROW" tag swings onto the cloche, the DM "Here's the secret" drops in.
Cree keeps his rules: his own 3D poses, no clothes (the magnifier is his), he never flaps or flies.
python3 build/generate.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, HTML, ROOT, punch  # noqa: E402
from fx import cree_html, cree_to, pose, cree_hop, cree_wiggle, blink, sweat, say, sparkle, P  # noqa: E402

random.seed(19)
DUR = round(L1["g6"] + .7, 2)
K = ["g0", "g1", "g2", "g3", "g4", "g5", "g6"]
JX, JY = 250, 520                                   # the cloche's top-left corner in world px


def J(x, y):
    """cloche-local point -> world point"""
    return JX + x, JY + y


# ---- headlines (screen space): one at a time, the previous leaves before the next one's first word ----------------------
HTMLS = []                                          # screen-space layers (headlines, DM)
OPEN = [None]
WID = [0]


def head(hid, rows, top, line, size=110, after=0.0):
    spoken, k, out, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
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
    HTMLS.append(f'<div class="head" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .05, .32, "{opacity: 0, filter: 'blur(12px)', y: 22}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .3, .2, "{opacity: 0, filter: 'blur(14px)', y: -36}", "power2.in")
    OPEN[0] = hid
    return out


# ---- camera: three parallax rigs ---------------------------------------------------------------------------------------
RIGS = (("#rbg", .4), ("#rw", 1.0), ("#rfg", 1.7))
OFS = 170                                           # the world sits 170 px lower than its logical coordinates (#wofs)


def cam(t, cx, cy, z, d=1.0, ease="power2.inOut"):
    """frame the world point (cx, cy) at screen centre with zoom z; the background and foreground move less / more"""
    for sel, f in RIGS:
        zf = 1 + (z - 1) * f
        cxf, cyf = 540 + (cx - 540) * f, 960 + (cy + OFS - 960) * f
        js(f'tl.to("{sel}", {{x: {540 - cxf * zf:.1f}, y: {1080 - cyf * zf:.1f}, scale: {zf:.4f}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def cam_set(cx, cy, z):
    for sel, f in RIGS:
        zf = 1 + (z - 1) * f
        cxf, cyf = 540 + (cx - 540) * f, 960 + (cy + OFS - 960) * f
        js(f'tl.set("{sel}", {{x: {540 - cxf * zf:.1f}, y: {1080 - cyf * zf:.1f}, scale: {zf:.4f}}}, 0);')


# ---- icons ---------------------------------------------------------------------------------------------------------------
HEART = ('<svg viewBox="0 0 24 24"><path d="M12 21 C5 15.5 2 12.4 2 8.6 C2 5.5 4.4 3.2 7.3 3.2 C9.2 3.2 10.9 4.2 12 5.8 C13.1 4.2 14.8 3.2 16.7 3.2 '
         'C19.6 3.2 22 5.5 22 8.6 C22 12.4 19 15.5 12 21 Z" fill="url(#hg)"/><defs><linearGradient id="hg" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#ff8cc6"/><stop offset="1" stop-color="#E0187E"/></linearGradient></defs></svg>')
DOWN = '<svg viewBox="0 0 24 24"><path d="M12 4v15M5 13l7 7 7-7" fill="none" stroke="#e11d48" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
KEY = ('<svg viewBox="0 0 48 48"><circle cx="15" cy="24" r="9" fill="none" stroke="#F343A2" stroke-width="5"/><path d="M24 24 H44 M36 24 V31 M42 24 V30" '
       'fill="none" stroke="#F343A2" stroke-width="5" stroke-linecap="round"/></svg>')
SNIPS = ('<svg viewBox="-60 -60 120 120"><g class="sa"><path d="M0 0 L58 -10 L58 -2 Z" fill="#cfd6dc" stroke="#7d8a94" stroke-width="2"/><circle cx="-30" cy="18" r="15" '
         'fill="none" stroke="#F343A2" stroke-width="9"/><path d="M0 0 L-18 10" stroke="#F343A2" stroke-width="9"/></g><g class="sb"><path d="M0 0 L58 10 L58 2 Z" '
         'fill="#e6ebef" stroke="#7d8a94" stroke-width="2"/><circle cx="-30" cy="-18" r="15" fill="none" stroke="#F343A2" stroke-width="9"/><path d="M0 0 L-18 -10" '
         'stroke="#F343A2" stroke-width="9"/></g><circle r="6" fill="#ffc21a"/></svg>')
SPROUT = ('<svg viewBox="0 0 70 70"><path d="M35 70 C35 55 35 45 35 38" stroke="#4f9a62" stroke-width="6" stroke-linecap="round" fill="none"/>'
          '<path d="M35 42 C20 40 10 30 8 16 C24 16 34 26 35 42 Z" fill="#7ccf86"/><path d="M35 40 C48 38 60 28 62 14 C46 14 36 24 35 40 Z" fill="#5fbb72"/></svg>')

# =======================================================================================================================
# THE WORLD
# background rig: wall, window light, shelf, fairy lights
books = "".join(f'<i class="book" style="left:{x}px;width:{w}px;height:{h}px;background:{c}"></i>'
                for x, w, h, c in [(40, 46, 150, "#c9a0ff"), (90, 38, 126, "#ffb38a"), (132, 54, 168, "#F343A2"), (190, 40, 120, "#ffd27a"), (234, 48, 140, "#9ad7c2")])
fl_pts = [(-60 + 105 * i, 150 + 38 * math.sin(i * .9)) for i in range(13)]
flwire = "M" + " ".join(f"{x + 100:.0f} {y - 120 + 50:.0f}" for x, y in fl_pts)
fls = "".join(f'<i class="fl" id="fl{i}" style="left:{x:.0f}px;top:{y + 40:.0f}px"></i>' for i, (x, y) in enumerate(fl_pts))
BG = (f'<div class="wall"></div><div class="winlight" id="win"><i style="left:180px"></i><i style="left:400px"></i></div>'
      f'<div id="bgblur"><div class="shelf">{books}<i class="ppot" style="left:330px"></i></div></div>'
      f'<svg class="flw" viewBox="0 0 1300 200"><path d="{flwire}"/></svg>{fls}')

# the cloche: plant (stem + reel-thumbnail leaves), soil with roots, glass
LEAVES = [  # (x, y, angle, left?)  cloche-local attachment points on the stem
    (297, 468, -34, False), (284, 428, 36, True), (299, 360, -40, False), (282, 310, 40, True),
    (300, 254, -36, False), (283, 204, 34, True), (295, 156, -26, False)]
# v1.1 (owner: "everything is cluttered and hiding behind the mascot, spacing not done"): leaves lifted so the lowest
# ones clear Cree, Cree moved to his own spot by the glass and made smaller, camera frames everything lower so the
# headline band stays clean (soft scrim behind it), the extra COMMENT GROW tag dropped, the cloud moved off the shelf
DRY = 2                                               # the right leaf at (299, 400)
NEW_LEAVES = [(286, 128, 22, True), (293, 108, -16, False)]
LCOL = ["linear-gradient(160deg,#ffd0e6,#F343A2)", "linear-gradient(160deg,#ffe3c8,#F5876C)", "linear-gradient(160deg,#ead9ff,#b14dff)",
        "linear-gradient(160deg,#ffe0ef,#ee688b)", "linear-gradient(160deg,#fff0c4,#f2b134)", "linear-gradient(160deg,#ffd6e8,#d81f86)",
        "linear-gradient(160deg,#f9d9c8,#e68b70)", "linear-gradient(160deg,#ffd0e6,#ff8cc6)", "linear-gradient(160deg,#ead9ff,#c58bff)"]


def leaf_html(lid, x, y, ang, left, col, cls=""):
    pos = f"left:{x - 74}px" if left else f"left:{x}px"
    return (f'<div class="leaf {"flip" if left else ""} {cls}" id="{lid}" style="{pos};top:{y}px;transform:rotate({ang}deg)">'
            f'<div class="lf" style="background:{col}"><i></i><b></b></div></div>')


leaves = "".join(leaf_html(f"lv{i}", x, y, a, l, LCOL[i], "dry" if i == DRY else "") for i, (x, y, a, l) in enumerate(LEAVES))
leaves += leaf_html("lvfresh", *LEAVES[DRY][:3], False, LCOL[0], "fresh")
leaves += "".join(leaf_html(f"lvn{i}", x, y, a, l, LCOL[7 + i]) for i, (x, y, a, l) in enumerate(NEW_LEAVES))
STEM = "M290 600 C 280 490 306 420 294 300 C 286 230 298 170 290 110"
FLOWERS = [(290, 86), (210, 150), (372, 196)]
hearts = "".join(f'<i class="heart" id="hf{i}" style="left:{x}px;top:{y}px;transform:scale(0)">{HEART}</i>' for i, (x, y) in enumerate(FLOWERS))
ROOTS = ["M290 0 C 280 40 230 60 180 90 C 150 110 120 120 90 140", "M290 0 C 300 50 360 70 410 100 C 440 120 470 130 500 146",
         "M290 0 C 288 60 270 110 250 150", "M290 0 C 296 60 320 110 340 150", "M290 0 C 270 26 230 36 190 40"]
RNODES = [(90, 140), (500, 146), (250, 150), (340, 150), (190, 40)]
roots = "".join(f'<path d="{d}"/>' for d in ROOTS)
roots += "".join(f'<path class="rg" id="rg{i}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="{d}"/>' for i, d in enumerate(ROOTS))
nodes = "".join(f'<i class="node" id="nd{i}" style="left:{x - 15}px;top:{590 + y - 20}px;background:{LCOL[i]}"></i>' for i, (x, y) in enumerate(RNODES))
pebbles = "".join(f'<i class="pebble" style="left:{x}px;top:{y}px;width:{w}px;height:{w * .7:.0f}px"></i>'
                  for x, y, w in [(40, 600, 46), (130, 612, 30), (420, 604, 40), (500, 616, 34), (220, 640, 26), (360, 650, 28)])
SEEDS = [(150, 600), (420, 604), (500, 610)]
seeds = "".join(f'<i class="seed" id="sd{i}" style="left:{x}px;top:{y - 420}px"><i class="flag"></i></i>' for i, (x, y) in enumerate(SEEDS))
sprouts = "".join(f'<i class="sprout" id="spr{i}" style="left:{x}px;top:{y + 4}px">{SPROUT}</i>' for i, (x, y) in enumerate(SEEDS))
stake = '<div class="stake" id="stake" style="left:30px;top:410px"><i class="post"></i><div class="sign"><i id="sb0" style="height:30%"></i><i id="sb1" style="height:45%"></i><i class="g" id="sb2" style="height:70%"></i><i class="g" id="sb3" style="height:100%"></i></div></div>'
glass = ('<div class="jglass"><i style="left:70px;top:120px;width:30px;height:420px;transform:rotate(8deg)"></i>'
         '<i style="left:120px;top:90px;width:12px;height:300px;transform:rotate(10deg);opacity:.7"></i><i style="right:70px;top:200px;width:16px;height:300px;'
         'transform:rotate(-6deg);opacity:.5"></i></div>')
JAR = (f'<div id="jar"><div class="jbase"></div><div class="jinner"><div class="jback"></div><div class="soil"></div>{pebbles}'
       f'<svg class="roots" viewBox="0 0 580 170">{roots}</svg>{nodes}{stake}{sprouts}'
       f'<div id="plant"><svg class="stem" viewBox="0 0 580 760"><path d="{STEM}"/><path class="s2" d="{STEM}"/>'
       f'<path id="pulse" pathLength="1" stroke-dasharray=".18 1.2" stroke-dashoffset=".18" d="M290 600 C 280 490 306 420 297 402" '
       f'style="stroke:#ff3d5c;stroke-width:12;opacity:0;filter:drop-shadow(0 0 10px rgba(255,40,80,.9))"/></svg>{leaves}{hearts}</div>{seeds}</div>'
       f'{glass}<i class="knob"></i><div class="plaque" id="plaque"><img src="assets/img/creedom_logo.png" alt="Creedom"></div></div>')

# the creator, a clay figure: body, head with a bun, arm holding a phone, three mouths
GIRL = ('<div id="girl"><svg viewBox="0 0 300 480"><defs>'
        '<radialGradient id="gsk" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffe0cc"/><stop offset="1" stop-color="#e8a98c"/></radialGradient>'
        '<radialGradient id="gsw" cx=".3" cy=".25" r=".9"><stop offset="0" stop-color="#ffd3a8"/><stop offset=".6" stop-color="#f5a06e"/><stop offset="1" stop-color="#d97d55"/></radialGradient>'
        '<radialGradient id="ghr" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6b3b3f"/><stop offset="1" stop-color="#2e1517"/></radialGradient></defs>'
        '<ellipse cx="160" cy="470" rx="130" ry="14" fill="rgba(110,40,60,.25)"/>'
        '<g id="gbody"><path d="M60 480 C60 330 100 268 160 268 C220 268 258 330 258 480 Z" fill="url(#gsw)"/>'
        '<path d="M126 268 Q160 300 194 268" fill="none" stroke="#e5895d" stroke-width="8" stroke-linecap="round"/>'
        '<g id="ghead"><circle cx="160" cy="170" r="92" fill="url(#ghr)"/><circle cx="160" cy="70" r="44" fill="url(#ghr)"/>'
        '<ellipse cx="166" cy="186" rx="76" ry="82" fill="url(#gsk)"/>'
        '<path d="M88 170 C92 110 140 88 180 92 C222 96 248 126 246 168 C214 140 176 132 140 142 C118 148 100 156 88 170 Z" fill="url(#ghr)"/>'
        '<circle cx="128" cy="214" r="14" fill="#f59bb1" opacity=".6"/><circle cx="218" cy="210" r="14" fill="#f59bb1" opacity=".6"/>'
        '<g id="geyes"><ellipse cx="150" cy="190" rx="8" ry="11" fill="#2a1220"/><ellipse cx="200" cy="188" rx="8" ry="11" fill="#2a1220"/>'
        '<circle cx="153" cy="186" r="3" fill="#fff"/><circle cx="203" cy="184" r="3" fill="#fff"/></g>'
        '<path id="gm_sad" d="M160 232 Q176 222 192 232" fill="none" stroke="#9a3b4e" stroke-width="5" stroke-linecap="round"/>'
        '<path id="gm_smile" d="M156 224 Q176 252 196 224 Z" fill="#9a3b4e" opacity="0"/></g>'
        '<g id="garm"><path d="M210 320 C250 330 270 300 262 262" fill="none" stroke="url(#gsw)" stroke-width="40" stroke-linecap="round"/>'
        '<circle cx="262" cy="258" r="20" fill="url(#gsk)"/><rect x="236" y="196" width="50" height="86" rx="10" fill="#2a1220"/>'
        '<rect id="gscr" x="241" y="202" width="40" height="72" rx="7" fill="#8a7a84"/></g></g></svg></div>')

vtag = (f'<div class="vtag" id="vtag" style="left:690px;top:640px"><i class="str" style="left:60px;top:-120px;height:124px"></i><div class="card"><small>VIEWS THIS WEEK</small>'
        f'<b><span id="vnum">1,240</span>{DOWN}</b></div></div>')
cloud = ('<div class="cloud" id="cloud"><svg viewBox="0 0 300 150"><path d="M60 130 C20 130 10 90 40 76 C34 40 80 24 104 46 C116 14 176 10 192 46 C220 30 262 46 '
         '256 80 C292 88 290 130 250 130 Z" fill="#9b8f98"/></svg><span>ALGORITHM?</span></div>')
ctag = ('<div class="ctag" id="ctag" style="left:330px;top:1010px"><i class="str"></i><div class="card"><small>COMMENT</small><b>GROW</b></div></div>')
drops = '<div class="drops">' + "".join(f'<i id="dr{i}" style="left:{JX + 160 + 50 * i}px;top:{JY + 40}px"></i>' for i in range(6)) + "</div>"
dry_tag = f'<div class="tag red" id="tagdry" style="left:{JX + 110}px;top:{JY + 480}px">0:03 · WEAK HOOK</div>'
kill_tag = f'<div class="tag red" id="tagkill" style="left:{JX + 90}px;top:{JY + 480}px">KILLING VIEWS</div>'
ready_tag = f'<div class="tag grn" id="tagready" style="left:{JX + 100}px;top:{JY + 480}px">READY TO POST ✓</div>'
snips = f'<div class="snips" id="snips" style="left:{JX + 330}px;top:{JY + 330}px">{SNIPS}</div>'
ghearts = "".join(f'<i class="hrt" id="gh{i}" style="left:{200 + 30 * i}px;top:1000px">{HEART}</i>' for i in range(4))
WORLD = (f'<div class="desk"></div><div class="deskgrain"></div><i class="shadow" style="left:200px;top:1300px;width:700px;height:80px"></i>'
         f'<i class="shadow" style="left:-40px;top:1290px;width:360px;height:50px"></i>{GIRL}{ghearts}{JAR}{cloud}{vtag}{dry_tag}{kill_tag}{ready_tag}{snips}{drops}')
bokeh = "".join(f'<i class="bokeh" id="bk{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:{o}"></i>'
                for i, (x, y, s, o) in enumerate([(-60, 120, 220, .5), (880, 260, 180, .45), (60, 1680, 260, .4), (900, 1720, 200, .35)]))
FG = f'<div class="fgmug"></div><div class="fgpen"></div>{bokeh}'

# =======================================================================================================================
# TIMELINE
L = {k: (L0[k], L1[k]) for k in K}
cam_set(540, 990, 1.0)
for i, (x, y, a, l) in enumerate(LEAVES):        # wilting: every leaf hangs lower, the plant is grey
    droop = 26 if not l else -26
    js(f'tl.set("#lv{i}", {{rotation: {a + droop}}}, 0);')
st("#plant", 0, "{filter: 'saturate(.45) brightness(.96)'}")
st("#lvfresh", 0, "{scale: 0, opacity: 0}")
for i in range(len(NEW_LEAVES)):
    st(f"#lvn{i}", 0, "{scale: 0}")
js('tl.set("#plant", {rotation: 4}, 0);')

# ---- 0 hook: "Her account was wilting. Same posts, fewer views, every single week."
head("h0a", [[("Her", ""), ("account", "")], [("was", ""), ("wilting.", "br")]], 250, "g0", size=128)
t_few = T("g0", "fewer")
head("h0b", [[("fewer", "rd"), ("views,", "")], [("every", ""), ("single", ""), ("week.", "")]], 250, "g0", size=112, after=t_few)
cam(0, 520, 960, 1.1, L["g0"][1] + .3, "sine.inOut")
js(f'tl.fromTo("#plant", {{rotation: 4}}, {{rotation: 7, duration: 2.2, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, 0);')
t_wil = T("g0", "wilting")
for i, (x, y, a, l) in enumerate(LEAVES):
    droop = 38 if not l else -38
    to(f"#lv{i}", t_wil - .1 + .04 * i, .8, f"{{rotation: {a + droop}}}", "power2.inOut")
sfx("whoosh", .05)
vals = [1240, 1060, 870, 690, 520, 380]
t_v0 = T("g0", "Same")
for k, v in enumerate(vals):
    st("#vnum", t_v0 + .45 * k, f'{{textContent: "{v:,}"}}')
    if k:
        sfx("tick", t_v0 + .45 * k)
js(f'tl.fromTo("#vtag", {{rotation: -6}}, {{rotation: 6, duration: 1.1, yoyo: true, repeat: 4, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.to("#gbody", {{y: 8, duration: .5, yoyo: true, repeat: 1, ease: "sine.inOut"}}, {T("g0", "week") - .2:.3f});')
js(f'tl.to("#ghead", {{rotation: -6, svgOrigin: "160 260", duration: .6, ease: "sine.inOut"}}, {t_few:.3f});')
st("#cloud", 0, "{opacity: .9}")
js(f'tl.fromTo("#cloud", {{x: 0}}, {{x: 30, duration: 3, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, 0);')

# ---- 1 "Turns out, it wasn't the algorithm. It was one dry leaf."
t_alg = T("g1", "algorithm")
head("h1a", [[("It", ""), ("wasn't", ""), ("the", "")], [("algorithm.", "sm")]], 250, "g1", size=120, after=T("g1", "it"))
to("#vtag", T("g1", "Turns") - .1, .3, "{opacity: 0, y: -40}", "power2.in")
to("#cloud", t_alg + .15, .3, "{scale: 1.3, opacity: 0, filter: 'blur(10px)'}", "power2.out")
sfx("pop", t_alg + .15)
sfx("swish", t_alg + .2)
t_it2 = T("g1", "It", 1) if len([w for w in LINES["g1"] if w["w"].lower().startswith("it")]) > 1 else T("g1", "was")
head("h1b", [[("It", ""), ("was", ""), ("one", "")], [("dry", "br"), ("leaf.", "br")]], 250, "g1", size=124, after=t_it2)
dx, dy = J(LEAVES[DRY][0] + 37, LEAVES[DRY][1])
cam(t_alg - .2, dx, dy + 30, 1.8, 1.1)
sfx("whoosh_big", t_alg - .25)
t_dry = T("g1", "dry")
ft("#tagdry", t_dry, .3, "{opacity: 0, scale: .4, y: 20}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.4)")
js(f'tl.fromTo("#lv{DRY}", {{x: 0}}, {{keyframes: [{{x: -4, duration: .05}}, {{x: 4, duration: .05}}, {{x: -3, duration: .05}}, {{x: 0, duration: .05}}], immediateRender: false}}, {t_dry:.3f});')
punch(t_dry + .05, 1.05)
sfx("error", t_dry)

# ---- 2 "Creedom read her whole account, and found the reel killing her views."
t_cr = T("g2", "Creedom")
to("#tagdry", t_cr - .3, .2, "{opacity: 0, y: -20}")
head("h2a", [[("Creedom", "it"), ("read", ""), ("her", "")], [("whole", ""), ("account,", "")]], 250, "g2", size=118)
cam(t_cr - .35, 540, 1030, 1.38, .8)
CR = (JX + 505, JY + 594, .26)                           # Cree on the soil, right of the stem (world px; feet y)
cree_to(t_cr - .05, *P(*CR), d=.01)
pose(t_cr, "wave", flip=False, squash=False)
st("#cree", t_cr, "{opacity: 1}")
ft("#creeb", t_cr, .45, "{y: -360}", "{y: 0}", "bounce.out")
sfx("pop", t_cr + .3)
sparkle(t_cr + .35, .8)
ft("#plaque", t_cr, .4, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "power3.out")
js(f'tl.fromTo("#plaque", {{boxShadow: "0 0 0 0 rgba(243,67,162,0)"}}, {{boxShadow: "0 0 40px 10px rgba(243,67,162,.6)", duration: .3, yoyo: true, repeat: 1, immediateRender: false}}, {t_cr + .1:.3f});')
sfx("ding", t_cr + .05)
t_rd = T("g2", "read")
pose(t_rd, "mag", flip=False)
cam(t_rd + .1, 540, 1180, 1.6, .7)
for i in range(len(ROOTS)):
    ft(f"#rg{i}", t_rd + .2 + .12 * i, .5, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "power2.out")
    ft(f"#nd{i}", t_rd + .55 + .12 * i, .25, "{scale: 1}", "{scale: 1.35}", "back.out(3)")
    to(f"#nd{i}", t_rd + .8 + .12 * i, .2, "{scale: 1}")
    sfx("ding2", t_rd + .6 + .12 * i)
sfx("riser_short", t_rd)
t_kl = T("g2", "killing")
head("h2b", [[("found", ""), ("the", ""), ("reel", "")], [("killing", "rd"), ("her", ""), ("views.", "")]], 250, "g2", size=112, after=T("g2", "found"))
cam(T("g2", "found") - .1, dx - 30, dy + 160, 1.5, .8)
st("#pulse", T("g2", "found"), "{opacity: 1}")
ft("#pulse", T("g2", "found"), .9, "{strokeDashoffset: .18}", "{strokeDashoffset: -1}", "power1.in")
st("#pulse", T("g2", "found") + .95, "{opacity: 0}")
sfx("riser_short", T("g2", "found") - .3)
ft("#tagkill", t_kl, .25, "{opacity: 0, scale: 2}", "{opacity: 1, scale: 1}", "power4.in")
js(f'tl.to("#lv{DRY} .lf", {{boxShadow: "inset 0 0 0 5px #ff3d5c, 0 0 40px rgba(255,40,80,.9)", duration: .2}}, {t_kl:.3f});')
sfx("error", t_kl)
sfx("stamp2", t_kl + .15)
pose(t_kl - .05, "shock")
sweat(t_kl + .1, .8)
say(t_kl + .05, "!", .7, left=True)
punch(t_kl + .05, 1.04)

# ---- 3 "Before her next post, it checked the hook, and fixed it."
t_bf = T("g3", "Before")
to("#tagkill", t_bf - .2, .2, "{opacity: 0, y: -20}")
head("h3a", [[("Before", ""), ("her", "")], [("next", ""), ("post,", "pk")]], 250, "g3", size=120)
cam(t_bf - .15, dx, dy + 110, 1.75, .7)
pose(t_bf, "point", flip=True)
t_ck = T("g3", "checked")
head("h3b", [[("it", ""), ("checked", "it"), ("the", ""), ("hook,", "")], [("and", ""), ("fixed", "pk"), ("it.", "")]], 250, "g3", size=104, after=T("g3", "it"))
pose(t_ck, "mag", flip=False)
js(f'tl.to("#lv{DRY} .lf", {{boxShadow: "inset 0 0 0 5px #ffc21a, 0 0 30px rgba(255,194,26,.9)", duration: .2}}, {t_ck:.3f});')
sfx("click", t_ck)
t_fx = T("g3", "fixed")
ft("#snips", t_fx - .35, .25, "{opacity: 0, x: 80, rotation: -30}", "{opacity: 1, x: 0, rotation: 0}", "back.out(2)")
js(f'tl.fromTo("#snips .sa", {{rotation: -16}}, {{rotation: 8, duration: .07, yoyo: true, repeat: 3, ease: "none", svgOrigin: "0 0", immediateRender: false}}, {t_fx - .1:.3f});')
js(f'tl.fromTo("#snips .sb", {{rotation: 16}}, {{rotation: -8, duration: .07, yoyo: true, repeat: 3, ease: "none", svgOrigin: "0 0", immediateRender: false}}, {t_fx - .1:.3f});')
sfx("scratch", t_fx - .08)
sfx("click", t_fx)
to("#snips", t_fx + .25, .2, "{opacity: 0, x: 60}")
to(f"#lv{DRY}", t_fx, .7, "{y: 420, rotation: 140, opacity: 0}", "power2.in")
ft("#lvfresh", t_fx + .15, .55, "{scale: 0, opacity: 1, rotation: 40}", f"{{scale: 1, opacity: 1, rotation: {LEAVES[DRY][2]}}}", "back.out(1.8)")
ft("#tagready", t_fx + .3, .3, "{opacity: 0, scale: .4, y: 20}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.4)")
sfx("ding", t_fx + .3)
sparkle(t_fx + .2, .8)
pose(t_fx + .25, "cheer")
cree_hop(t_fx + .3, 70, 2)

# ---- 4 "Then it planted what to post next, from what her audience saved."
t_pl = T("g4", "planted")
to("#tagready", t_pl - .3, .2, "{opacity: 0, y: -20}")
head("h4a", [[("planted", "gn"), ("what", "")], [("to", ""), ("post", ""), ("next,", "it")]], 250, "g4", size=120, after=t_pl)
cam(L["g4"][0] - .1, 540, 1060, 1.45, .8)
pose(L["g4"][0], "present", flip=False)
for i in range(len(SEEDS)):
    tk = t_pl + .12 * i
    st(f"#sd{i}", tk, "{opacity: 1}")
    ft(f"#sd{i}", tk, .5, "{y: 0}", "{y: 420}", "bounce.out")
    ft(f"#spr{i}", tk + .55, .45, "{scale: 0}", "{scale: 1}", "back.out(2.2)")
    sfx("pop", tk + .35)
    to(f"#sd{i}", tk + .6, .3, "{opacity: 0, scale: .5}")
t_sv = T("g4", "saved")
head("h4b", [[("from", ""), ("what", ""), ("her", "")], [("audience", ""), ("saved.", "pk")]], 250, "g4", size=110, after=T("g4", "from"))
for i in range(len(SEEDS)):
    js(f'tl.to("#spr{i}", {{scale: 1.35, duration: .25, yoyo: true, repeat: 1, ease: "power2.out"}}, {t_sv - .1 + .08 * i:.3f});')
    sfx("ding2", t_sv - .1 + .08 * i)
pose(t_sv - .1, "cheer")
cree_hop(t_sv, 60)

# ---- 5 "And the best part? It showed her exactly what worked."  (time-lapse)
t_bp = T("g5", "And")
head("h5a", [[("And", ""), ("the", "")], [("best", "it"), ("part?", "")]], 250, "g5", size=140)
cam(t_bp - .1, 540, 900, .95, 1.1)
sfx("whoosh_big", t_bp - .15)
t_sh = T("g5", "showed")
TL0, TL1 = t_bp + .25, T("g5", "worked") + .1
js(f'tl.fromTo("#win", {{x: -500, opacity: .3}}, {{x: 420, opacity: .7, duration: {TL1 - TL0:.2f}, ease: "none", immediateRender: false}}, {TL0:.3f});')
sfx("riser", TL0)
to("#plant", TL0, TL1 - TL0, "{filter: 'saturate(1.1) brightness(1.03)', rotation: 0, scale: 1.16}", "power1.inOut")
for i, (x, y, a, l) in enumerate(LEAVES):
    if i != DRY:
        to(f"#lv{i}", TL0 + .1 * i, .6, f"{{rotation: {a}}}", "back.out(1.6)")
for i in range(len(NEW_LEAVES)):
    ft(f"#lvn{i}", TL0 + .7 + .2 * i, .45, "{scale: 0}", "{scale: 1}", "back.out(2)")
    sfx("pop", TL0 + .7 + .2 * i)
js(f'tl.to("#stake", {{scaleY: 1, duration: .5, ease: "back.out(1.6)"}}, {t_sh:.3f});')
js(f'tl.fromTo("#stake .sign i", {{scaleY: 0}}, {{scaleY: 1, duration: .3, stagger: .1, ease: "back.out(2)", immediateRender: false}}, {t_sh + .3:.3f});')
sfx("paper", t_sh)
head("h5b", [[("exactly", "")], [("what", ""), ("worked.", "gn")]], 250, "g5", size=140, after=T("g5", "exactly"))
t_wo = T("g5", "worked")
for i in range(len(FLOWERS)):
    ft(f"#hf{i}", t_wo - .1 + .12 * i, .4, "{scale: 0, rotation: -40}", "{scale: 1, rotation: 0}", "back.out(2.6)")
sfx("bell", t_wo)
sfx("ding", t_wo + .05)
punch(t_wo + .05, 1.04)
st("#gm_sad", t_wo, "{opacity: 0}")
st("#gm_smile", t_wo, "{opacity: 1}")
js(f'tl.to("#ghead", {{rotation: 4, svgOrigin: "160 260", duration: .4, ease: "back.out(2)"}}, {t_wo:.3f});')
js(f'tl.to("#gscr", {{fill: "#ffd0e6", duration: .2}}, {t_wo:.3f});')
for i in range(4):
    ft(f"#gh{i}", t_wo + .15 * i, .9, "{opacity: 0, y: 0, scale: .4}", f"{{opacity: 1, y: {-160 - 40 * i}, x: {random.randint(-40, 40)}, scale: 1}}", "power2.out")
    to(f"#gh{i}", t_wo + .15 * i + .9, .3, "{opacity: 0}")
pose(t_bp, "proud")
pose(t_wo, "cheer")
cree_hop(t_wo + .05, 70, 2)

# ---- 6 CTA "Comment GROW, and I'll send you the secret."
t_cm = T("g6", "Comment")
head("h6", [[("Comment", "")], [("GROW", "it")]], 250, "g6", size=150)
cam(t_cm - .2, 540, 1010, 1.1, .7)
js(f'tl.fromTo("#plaque", {{boxShadow: "0 0 0 0 rgba(243,67,162,0)"}}, {{boxShadow: "0 0 40px 12px rgba(243,67,162,.6)", duration: .4, yoyo: true, repeat: 3, immediateRender: false}}, {t_cm:.3f});')
sfx("whoosh", t_cm)
t_sd = T("g6", "send")
HTMLS.append(f'<div class="dm" id="dm" style="top:660px"><img src="assets/img/c100x_mark.png" alt=""><div><b>creators.100x</b><span>{KEY}Here\'s the secret</span></div><em>now</em></div>')
ft("#dm", t_sd - .15, .45, "{opacity: 0, y: -120}", "{opacity: 1, y: 0}", "back.out(1.6)")
sfx("ding", t_sd - .05)
pose(t_cm, "point", flip=True)
pose(T("g6", "secret"), "wave", flip=False)
cree_wiggle(T("g6", "secret") + .1, 2, 5)

# ---- ambience: fairy lights twinkle, Cree breathes, blinks
for i in range(len(fl_pts)):
    js(f'tl.fromTo("#fl{i}", {{opacity: .5, scale: .8}}, {{opacity: 1, scale: 1.2, duration: {random.uniform(.6, 1.2):.2f}, yoyo: true, repeat: {int(DUR)}, '
       f'ease: "sine.inOut", immediateRender: false}}, {random.uniform(0, 1):.2f});')
for i in range(4):
    js(f'tl.fromTo("#bk{i}", {{x: 0, y: 0}}, {{x: {random.randint(-40, 40)}, y: {random.randint(-40, 40)}, duration: {random.uniform(3, 5):.2f}, yoyo: true, repeat: 6, '
       f'ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -8, duration: .7, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .7)}, immediateRender: false}}, 0);')
for tb in (13.0, 19.8, 23.6):
    blink(tb)
js(f'tl.fromTo("#geyes", {{scaleY: 1}}, {{scaleY: .1, duration: .06, yoyo: true, repeat: 1, svgOrigin: "175 189", immediateRender: false}}, 2.2);')
js(f'tl.fromTo("#geyes", {{scaleY: 1}}, {{scaleY: .1, duration: .06, yoyo: true, repeat: 1, svgOrigin: "175 189", immediateRender: false}}, 9.4);')

WORLD += cree_html()
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: The Growth Lab (2.5D diorama) 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="punch">
        <div class="rig" id="rbg" data-layout-allow-overflow>{BG}</div>
        <div class="rig" id="rw" data-layout-allow-overflow data-layout-allow-overlap><div id="wofs" style="position:absolute;inset:0;transform:translateY({OFS}px)">{WORLD}</div></div>
        <div class="rig" id="rfg" data-layout-allow-overflow>{FG}</div>
      </div>
      <div class="tilt" id="tiltT"></div><div class="tilt" id="tiltB"></div>
      <div id="grade"></div><div id="vig"></div>
      <div id="scrim"></div>
      {chr(10).join(HTMLS)}
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
json.dump({"dur": DUR, "lines": L}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
