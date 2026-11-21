"""Creators 100X x Creedom "Thermal vision" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json from plan/words.json.

Script approved by the owner on 2026-11-21, voiced with ElevenLabs Jessica (Eleven v3; build/vo_el.py take 1, pauses trimmed by
build/vo_tight.py, word times by build/vo_words.py). One strict layout like the NICHE v3 reel: headline band 190..470, status pill
480..540, a phone with her profile grid in the centre, Cree bottom-left.
  t0 hook: the phone springs in, nine reels pop onto the grid;
  t1: question marks over the tiles: which one worked?
  t2: the tiles look the same... Cree pops in, slides on thermal goggles; on "heat" (the music's drop) a scan line sweeps the
      phone and the grid snaps into heat vision; the backdrop goes deep purple; a temperature scale slides in;
  t3: target brackets jump tile to tile, COLD, COLD, COLD; then lock on two burning tiles, MOST SAVED (example); save icons
      float up again and again;
  t4: the goggles flip up; heat streams pour out of the two hot tiles into a new reel: POST THIS NEXT;
  t5 CTA: a HUD readout locks on: COMMENT GROW.
Claims stay within what Creedom does: it reads the account and tells you what to post next, based on what your audience saved.
python3 build/generate.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT  # noqa: E402
from fx import cree_html, cree_to, pose, cree_hop, sparkle, P  # noqa: E402

random.seed(21)
DUR = round(L1["t5"] + 1.7, 2)
T0 = {k: (L0[k], L1[k]) for k in LINES}

HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, line, size=84, after=0.0, light=False):
    spoken, k, out_, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?…\""), None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?\"")
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="hw {cls}" id="{wid}">{word}</span>')
            out_.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTMLS.append(f'<div class="head{" lt" if light else ""}" id="{hid}" style="font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out_:
        ft(f"#{wid}", t - .05, .3, "{opacity: 0, filter: 'blur(10px)', y: 24}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out_)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .25, .18, "{opacity: 0, filter: 'blur(12px)', y: -30}", "power2.in")
    OPEN[0] = hid


STAT = []


def stat(t, text, hot=False):
    i = len(STAT)
    STAT.append(f'<div class="stat{" hot" if hot else ""}" id="st{i}"><span>{text}</span></div>')
    if i:
        to(f"#st{i - 1}", t - .05, .15, "{opacity: 0, y: -14}", "power2.in")
    ft(f"#st{i}", t, .3, "{opacity: 0, y: 14, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")


def flash(t, o=.7, d=.35):
    st("#flash", t, f"{{opacity: {o}}}")
    to("#flash", t + .02, d, "{opacity: 0}", "power2.out")


def stage(t, props, d=.6, ease="power3.inOut"):
    js(f'tl.to("#stage", {{{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


# =======================================================================================================================
# THE GRID: 3 x 3 tiles in the phone screen (screen offset 216, 576; grid top 250)
TILES = [("Morning routine", "#ffb3c7,#ff6f91"), ("Q&amp;A", "#b3d4ff,#5b8def"), ("Budget meal #3", "#ffd27a,#ff8a3d"),
         ("Day in my life", "#c9b3ff,#7a5cf0"), ("Room tour", "#a8f0d1,#2fb37f"), ("GRWM", "#ffc2e2,#e055a8"),
         ("Hostel hack #1", "#ffe08a,#f5a524"), ("Study vlog", "#b3e5ff,#3aa0d8"), ("Gym day", "#ffb59e,#ef5d4a")]
HOT = (2, 6)
TEMPS = [14, 11, 97, 16, 12, 18, 94, 13, 15]
TX = [0, 218, 436]
TY = [0, 296, 592]
SCR_X, SCR_Y, GRID_Y = 216, 576, 250


def tile_xy(i):
    """centre of tile i in frame coordinates"""
    return SCR_X + TX[i % 3] + 106, SCR_Y + GRID_Y + TY[i // 3] + 145


GRID = ""
for i, (t, g) in enumerate(TILES):
    hot = i in HOT
    GRID += (f'<div class="tile" id="tl{i}" style="left:{TX[i % 3]}px;top:{TY[i // 3]}px"><div class="tb" style="background:linear-gradient(160deg,{g})"></div>'
             f'<i class="fc"></i><i class="pl"></i><div class="tt">{t}</div>'
             f'<div class="th {"hot" if hot else "cold"}" id="th{i}"><span class="tp">{TEMPS[i]}°</span><div class="tt2">{t}</div></div></div>')
QMS = "".join(f'<i class="qm" id="qm{k}" style="left:{TX[i % 3] + 106}px;top:{TY[i // 3] + 145}px">?</i>' for k, i in enumerate((1, 3, 5, 7)))
PHONE = (f'<div id="ph"><div id="scr"><i class="isl"></i><div class="prof"><div class="av"><i></i></div><div class="pname">your.page</div>'
         f'<div class="pst"><span><b>9</b>posts</span><span><b>1.2K</b>followers</span><span><b>210</b>following</span></div></div>'
         f'<div id="thhead"><i></i></div><div class="grid">{GRID}{QMS}</div><i id="scan"></i></div></div>')
SCALE = '<div id="scale"><small style="top:-40px">HOT</small><small style="bottom:-40px">COLD</small><i id="needle"></i></div>'
BRK = lambda bid, cls, lab: f'<div class="brk {cls}" id="{bid}"><i></i><i></i><i></i><i></i><b>{lab}</b></div>'
BRACKETS = BRK("bc", "c", "COLD") + BRK("bh0", "h", "MOST SAVED") + BRK("bh1", "h", "MOST SAVED")
HAZE = "".join(f'<i class="haze" id="hz{k}" style="left:{tile_xy(i)[0]}px;top:{tile_xy(i)[1]}px"></i>' for k, i in enumerate(HOT))
BOOK = '<svg viewBox="0 0 44 56"><path d="M4 4 H40 V52 L22 40 L4 52 Z" fill="#fff4a0" stroke="#ffb020" stroke-width="3"/></svg>'
SAVES = "".join(f'<i class="sv" id="sv{k}">{BOOK}</i>' for k in range(10))
STAGE = f'<div id="stage">{PHONE}{SCALE}{BRACKETS}{HAZE}{SAVES}</div>'
NX, NY = 540, 980          # centre of the new reel
STREAMS = ('<svg class="streams" viewBox="0 0 1080 1920"><defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/>'
           '<stop offset=".5" stop-color="#ffb020"/><stop offset="1" stop-color="#ff3d6e"/></linearGradient></defs>'
           + "".join(f'<path id="str{k}" d="M{tile_xy(i)[0]} {tile_xy(i)[1]} Q {(tile_xy(i)[0] + NX) / 2 + (120 if k else -120)} {min(tile_xy(i)[1], NY) - 160} {NX} {NY}" '
                     f'fill="none" stroke="url(#sg)" stroke-width="26" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" '
                     f'style="filter:drop-shadow(0 0 14px rgba(255,160,60,.9))"/>' for k, i in enumerate(HOT)) + '</svg>')
NEXT = ('<div id="next"><div class="nb"></div><i class="fc"></i><div class="nh" id="nexth"></div><div class="tt">Hostel meals under 100</div></div>'
        '<div class="ptn" id="ptn"><span>POST THIS NEXT</span></div><div class="exm" id="exm">EXAMPLE</div>')
HUD = ('<div id="hud"><div class="brk"><i></i><i></i><i></i><i></i></div><div class="ln" id="hl1" style="top:70px">TARGET LOCKED: YOUR NEXT REEL</div>'
       '<div class="big" id="hbig">COMMENT<br>GROW</div></div>')
GOG = ('<svg id="gog" viewBox="0 0 360 150"><rect x="0" y="52" width="360" height="30" rx="15" fill="#2a1430"/>'
       '<defs><radialGradient id="gl" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#ffd27a"/><stop offset=".35" stop-color="#ff3d6e"/>'
       '<stop offset="1" stop-color="#3a0a5a"/></radialGradient></defs>'
       '<circle cx="92" cy="72" r="66" fill="#1a0a20"/><circle cx="268" cy="72" r="66" fill="#1a0a20"/>'
       '<circle cx="92" cy="72" r="54" fill="url(#gl)"/><circle cx="268" cy="72" r="54" fill="url(#gl)"/>'
       '<ellipse cx="74" cy="52" rx="16" ry="10" fill="#fff" opacity=".6"/><ellipse cx="250" cy="52" rx="16" ry="10" fill="#fff" opacity=".6"/>'
       '<rect x="150" y="62" width="60" height="18" rx="8" fill="#1a0a20"/></svg>')
CREE = cree_html().replace('</div></div><svg viewBox="0 0 820 820" class="csw">', GOG + '</div></div><svg viewBox="0 0 820 820" class="csw">', 1)

# =======================================================================================================================
# TIMELINE
CF = (955, 1850, .34)
js(f'tl.fromTo("#ph", {{y: 0, rotation: -.5}}, {{y: -8, rotation: .5, duration: 2.3, yoyo: true, repeat: {int(DUR / 2.3)}, ease: "sine.inOut", immediateRender: false}}, 0);')

# ---- t0 hook ---------------------------------------------------------------------------------------------------------------------------
ft("#ph", 0, .6, "{y: 420, rotationX: 26, scale: .92, transformPerspective: 1600}", "{y: 0, rotationX: 0, scale: 1}", "back.out(1.3)")
sfx("whoosh_big", 0)
for i in range(9):
    ft(f"#tl{i}", .25 + i * .07, .35, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2)")
    if i % 3 == 0:
        sfx("pop", .25 + i * .07)
head("h0", [[("Your", ""), ("audience", ""), ("already", "")], [("told", ""), ("you", ""), ("what", ""), ("to", "")], [("post", "pk"), ("next.", "")]], "t0", size=82)
stage(.4, "scale: 1.05", 2.6, "sine.inOut")

# ---- t1: which one? --------------------------------------------------------------------------------------------------------------------
t1 = T0["t1"][0]
head("h1", [[("You", ""), ("just", ""), ("can't", "")], [("see", "pk"), ("it.", "")]], "t1", size=110)
stat(t1 - .1, "WHICH ONE WORKED?")
for k in range(4):
    ft(f"#qm{k}", t1 + k * .12, .3, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}", "back.out(3)")
    sfx("tick", t1 + k * .12)
stage(t1, "scale: 1", .6)

# ---- t2: the same... until the heat ---------------------------------------------------------------------------------------------------
t2 = T0["t2"][0]
head("h2", [[("Every", ""), ("reel", ""), ("looks", ""), ("the", ""), ("same…", "")], [("until", ""), ("Creedom", "pk")], [("turns", ""), ("on", ""), ("the", ""), ("heat.", "ht")]],
     "t2", size=80)
for k in range(4):
    to(f"#qm{k}", t2 - .1, .2, "{opacity: 0, scale: .5}", "power2.in")
t_sm = T("t2", "same")
js(f'tl.fromTo(".tile", {{scale: 1}}, {{scale: .94, duration: .15, yoyo: true, repeat: 1, stagger: .02, immediateRender: false}}, {t_sm:.3f});')
t_cr = T("t2", "Creedom")
cree_to(t_cr - .1, *P(CF[0], CF[1] + 260, CF[2]), d=.01)
st("#cree", t_cr - .1, "{opacity: 1}")
pose(t_cr - .1, "stand", flip=False, squash=False)
cree_to(t_cr - .05, *P(*CF), d=.45, ease="back.out(1.8)")
sfx("pop", t_cr)
sparkle(t_cr + .1, .6)
t_gg = T("t2", "turns") + .05
ft("#gog", t_gg, .3, "{opacity: 0, y: -160, rotation: -20}", "{opacity: 1, y: 0, rotation: 0}", "back.out(2)")
sfx("click", t_gg + .25)
stat(t_gg, "THERMAL VIEW: ON", hot=True)
t_ht = T("t2", "heat") - .1                       # the music's drop
st("#scan", t_ht - .35, "{opacity: 1}")
ft("#scan", t_ht - .35, .45, "{y: 0}", "{y: 1140}", "power1.inOut")
st("#scan", t_ht + .12, "{opacity: 0}")
st("#thhead", t_ht - .3, "{opacity: 1}")
for r in range(3):
    for c in range(3):
        st(f"#th{r * 3 + c}", t_ht - .2 + r * .1, "{opacity: 1}")
to("#bgt", t_ht, .25, "{opacity: 1}", "power2.out")
st(".scanlines", t_ht, "{opacity: 1}")
flash(t_ht + .02, .8, .35)
js(f'tl.fromTo("#stage", {{scale: 1}}, {{keyframes: [{{scale: 1.07, duration: .08}}, {{scale: 1, duration: .45, ease: "power3.out"}}], immediateRender: false}}, {t_ht:.3f});')
sfx("whoosh_big", t_ht - .35)
sfx("impact", t_ht)
ft("#scale", t_ht + .15, .4, "{opacity: 0, x: 60}", "{opacity: 1, x: 0}", "power3.out")
to("#h2", t_ht + .35, .2, "{opacity: 0, y: -30}", "power2.in")
for k in range(2):
    js(f'tl.fromTo("#hz{k}", {{opacity: 0, scale: .9}}, {{opacity: .85, scale: 1.08, duration: .5, yoyo: true, repeat: {int((T0["t4"][0] - t_ht) / .5)}, ease: "sine.inOut", '
       f'immediateRender: false}}, {t_ht + .3:.3f});')

# ---- t3: cold, cold, cold; these two -----------------------------------------------------------------------------------------------
t3 = T0["t3"][0]
OPEN[0] = None
head("h3a", [[("Cold.", "cd"), ("Cold.", "cd"), ("Cold.", "cd")]], "t3", size=110, light=True)
COLD_T = [T("t3", "Cold", 0), T("t3", "Cold", 1), T("t3", "Cold", 2)]
for k, (tc, i) in enumerate(zip(COLD_T, (0, 4, 8))):
    x, y = tile_xy(i)
    if k == 0:
        ft("#bc", tc - .1, .2, f"{{opacity: 0, left: {x}, top: {y}, scale: 1.4}}", f"{{opacity: 1, left: {x}, top: {y}, scale: 1}}", "back.out(2)")
    else:
        to("#bc", tc - .12, .18, f"{{left: {x}, top: {y}}}", "power3.out")
    js(f'tl.fromTo("#bc", {{scale: 1.2}}, {{scale: 1, duration: .15, immediateRender: false}}, {tc - .02:.3f});')
    sfx("glitch", tc)
    js(f'tl.to("#needle", {{top: {640 - k * 12}, duration: .15}}, {tc:.3f});')
t_tw = T("t3", "these")
to("#bc", t_tw - .15, .15, "{opacity: 0}")
head("h3b", [[("And", ""), ("these", ""), ("two?", "ht")], [("Your", ""), ("viewers", ""), ("saved", "ht"), ("them.", "")], [("Again", ""), ("and", ""), ("again.", "")]],
     "t3", size=80, after=t_tw - .3, light=True)
for k, i in enumerate(HOT):
    x, y = tile_xy(i)
    ft(f"#bh{k}", t_tw + k * .15, .25, f"{{opacity: 0, left: {x}, top: {y}, scale: 1.5}}", f"{{opacity: 1, left: {x}, top: {y}, scale: 1}}", "back.out(2.4)")
    sfx("stamp2", t_tw + k * .15 + .1)
js(f'tl.to("#needle", {{top: 30, duration: .5, ease: "back.out(1.6)"}}, {t_tw:.3f});')
stat(t_tw, "2 HOT REELS · EXAMPLE", hot=True)
sfx("riser_short", t_tw)
hx = (tile_xy(HOT[0])[0] + tile_xy(HOT[1])[0]) / 2
stage(t_tw + .2, f"scale: 1.12, x: {(540 - hx) * 1.12:.0f}", .8)
t_ag = T("t3", "Again")
for k in range(10):
    i = HOT[k % 2]
    x, y = tile_xy(i)
    tk = t_ag - .1 + k * .1
    js(f'tl.fromTo("#sv{k}", {{opacity: 0, left: {x + random.randint(-50, 50)}, top: {y}, scale: .4}}, {{keyframes: [{{opacity: 1, scale: 1, top: {y - 90}, duration: .25}}, '
       f'{{opacity: 0, top: {y - 220}, duration: .4}}], immediateRender: false}}, {tk:.3f});')
    if k % 2 == 0:
        sfx("tick", tk)

# ---- t4: pour the heat into the next reel ---------------------------------------------------------------------------------------------
t4 = T0["t4"][0]
head("h4", [[("That's", ""), ("your", ""), ("next", ""), ("reel,", "ht")], [("hiding", ""), ("in", ""), ("plain", ""), ("sight.", "")]], "t4", size=84, light=True)
stage(t4 - .25, "scale: 1, x: 0", .5)
js(f'tl.to("#gog", {{y: -120, rotation: -25, opacity: 0, duration: .35, ease: "power2.in"}}, {t4 - .2:.3f});')
pose(t4 - .05, "present", flip=True)
for s in ("#bh0", "#bh1"):
    to(s, t4 - .2, .2, "{opacity: 0}")
for k in range(2):
    ft(f"#str{k}", t4 + .05 + k * .1, .55, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "power2.inOut")
    to(f"#str{k}", t4 + 1.0, .3, "{opacity: 0}")
sfx("whoosh", t4)
ft("#dim", t4 + .3, .3, "{opacity: 0}", "{opacity: .6}", "power2.out")
t_nr = T("t4", "next")
ft("#next", t_nr - .05, .5, "{opacity: 0, scale: .3, rotationY: -40, transformPerspective: 1400}", "{opacity: 1, scale: 1, rotationY: 0}", "back.out(1.6)")
js(f'tl.fromTo("#nexth", {{opacity: 0}}, {{keyframes: [{{opacity: 1, duration: .2}}, {{opacity: 0, duration: .6}}], immediateRender: false}}, {t_nr + .15:.3f});')
flash(t_nr + .1, .45, .3)
sfx("sparkle", t_nr)
t_pl = T("t4", "plain") - .2
ft("#ptn", t_pl, .3, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "back.out(2.2)")
ft("#exm", t_pl + .3, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
sfx("ding", t_pl + .05)
stat(t_nr, "POST THIS NEXT", hot=True)
js(f'tl.fromTo("#next", {{rotation: -1.5}}, {{rotation: 1.5, duration: 1, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {t_nr + .5:.3f});')

# ---- t5 CTA: the HUD locks on ------------------------------------------------------------------------------------------------------------
t5 = T0["t5"][0]
head("h5", [[("and", ""), ("I'll", ""), ("send", ""), ("you", "")], [("the", ""), ("secret.", "ht")]], "t5", size=92, after=T("t5", "and"), light=True)
to(f"#st{len(STAT) - 1}", t5 - .2, .2, "{opacity: 0}")
for s in ("#next", "#ptn", "#exm"):
    to(s, t5 - .25, .25, "{opacity: 0, scale: .9}", "power2.in")
js(f'tl.to("#stage", {{opacity: .12, scale: .92, duration: .4, ease: "power2.inOut"}}, {t5 - .25:.3f});')
to("#dim", t5 - .2, .3, "{opacity: .3}")
ft("#hud", t5 - .05, .35, "{opacity: 0, scale: 1.3}", "{opacity: 1, scale: 1}", "power3.out")
ft("#hl1", t5 + .1, .3, "{opacity: 0, x: -30}", "{opacity: 1, x: 0}", "power2.out")
ft("#hbig", T("t5", "GROW") - .1, .35, "{opacity: 0, scale: 1.6, filter: 'blur(12px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "back.out(2)")
js(f'tl.fromTo("#hbig", {{scale: 1}}, {{scale: 1.05, duration: .35, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {T("t5", "GROW") + .4:.3f});')
js(f'tl.fromTo("#hud .brk", {{scale: 1.08}}, {{scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false}}, {t5:.3f});')
sfx("click", t5)
sfx("ding", T("t5", "GROW"))
pose(t5, "wave", flip=False)
cree_hop(T("t5", "GROW"), 40, 2)

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: Thermal vision 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="bg" id="bgn"></div><div class="bg" id="bgt"></div>
      {STAGE}
      <div id="dim"></div>{STREAMS}{NEXT}{HUD}
      <div class="scanlines"></div>
      <div style="position:absolute;inset:0;z-index:28;pointer-events:none">{CREE}</div>
      {"".join(STAT)}
      {chr(10).join(HTMLS)}
      <div id="flash"></div><div id="grain"></div>
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
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
