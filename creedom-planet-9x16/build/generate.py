"""Creators 100X x Creedom "Planet You" (9:16, 2.5D): writes index.html, plan/sfx_events.json and plan/edit.json from plan/words.json.

Script approved by the owner on 2026-11-22, voiced with Kokoro af_heart (build/vo_kokoro.py; ElevenLabs was out of credits), word
times by build/vo_words.py. Her account is a tiny planet; every reel she has posted is a building standing on its curved surface.
  p0: deep space, the camera dollies in on the planet;
  p1: it turns: dark windows, flickering signs, one lonely streetlamp: a ghost town;
  p2: Cree flies in and hovers over the planet with a pink scanner beam; the world turns under it;
  p3: "Dark. Dark. Dark.": three buildings pass under the beam (EMPTY); "these two": two buildings light up with tiny crowds (MOST SAVED);
  p4: Cree drops a seed between them and a pink skyscraper grows: YOUR NEXT REEL; the crowds walk over;
  p5: on the music's lift, lights ripple out across the whole planet, fireworks;
  p6 CTA: a satellite beams down COMMENT GROW.
Claims stay within what Creedom does: it reads the whole account and tells you what to post next, based on what your audience saved.
python3 build/generate.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT  # noqa: E402
from fx import cree_html, cree_to, pose, cree_hop, sparkle, P  # noqa: E402
from chibi import DEFS as CHIBI_DEFS, seated  # noqa: E402

random.seed(11)
DUR = round(L1["p6"] + 1.7, 2)
T0 = {k: (L0[k], L1[k]) for k in LINES}
R, CX, CY = 360, 540, 1300
N = 11
TH = 360 / N
HOT = (4, 5)

HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, line, size=84, after=0.0):
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
    HTMLS.append(f'<div class="head" id="{hid}" style="font-size:{size}px">{"".join(rws)}</div>')
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


TAGS = []


def tag(t, text, cls, d=.9):
    i = len(TAGS)
    TAGS.append(f'<div class="tag {cls}" id="tg{i}" style="top:780px;left:630px;right:auto;text-align:left;white-space:nowrap"><span>{text}</span></div>')
    ft(f"#tg{i}", t, .2, "{opacity: 0, x: -20, scale: .8}", "{opacity: 1, x: 0, scale: 1}", "back.out(2.4)")
    if d:
        to(f"#tg{i}", t + d, .15, "{opacity: 0}")
    return f"#tg{i}"


def flash(t, o=.6, d=.35):
    st("#flash", t, f"{{opacity: {o}}}")
    to("#flash", t + .02, d, "{opacity: 0}", "power2.out")


def world(t, w, d=.4, ease="power3.inOut"):
    js(f'tl.to(["#world", "#surf"], {{rotation: {w:.2f}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


# =======================================================================================================================
# THE PLANET
def stars(n, size):
    return "".join(f'<i class="st" style="left:{random.uniform(-600, 1680):.0f}px;top:{random.uniform(-600, 2500):.0f}px;width:{s:.1f}px;height:{s:.1f}px;'
                   f'opacity:{random.uniform(.3, 1):.2f};box-shadow:0 0 {s * 3:.0f}px #fff"></i>' for s in (random.uniform(*size) for _ in range(n)))


SPACE = (f'<div class="space"></div>{stars(130, (1, 2.6))}'
         '<i class="neb" style="left:-420px;top:300px;width:1100px;height:1100px;background:radial-gradient(closest-side,rgba(243,67,162,.28),rgba(243,67,162,0))"></i>'
         '<i class="neb" style="left:460px;top:-200px;width:1100px;height:1100px;background:radial-gradient(closest-side,rgba(110,80,255,.32),rgba(110,80,255,0))"></i>'
         + "".join(f'<i class="comet" id="cm{i}" style="left:{x}px;top:{y}px"></i>' for i, (x, y) in enumerate(((900, 300), (1000, 1500), (850, 900)))))
CONTS = "".join(f'<i class="cont" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg)"></i>'
                for x, y, w, h, r in ((80, 160, 260, 170, 20), (420, 90, 200, 140, -15), (360, 420, 280, 200, 35), (60, 470, 180, 130, -25)))
CRATS = "".join(f'<i class="crat" style="left:{random.randint(60, 600)}px;top:{random.randint(60, 600)}px;width:{s}px;height:{s}px"></i>'
                for s in (random.randint(26, 60) for _ in range(9)))
DISC = f'<div id="atmo"></div><div id="disc"><div id="surf">{CONTS}{CRATS}</div><div id="shade"></div><div id="warm"></div></div>'
BCOL = ("#e9d8ff", "#d6e4ff", "#ffe0ec", "#dff7ea", "#fff1d6", "#e6defc")
SIGNC = ("#ff9ec7,#f343a2", "#9ad0ff,#4a7de8", "#ffe08a,#f59e3d", "#a8f0c6,#3fb37f", "#d6b8ff,#8a5cf0")
BLD = ""
WINS = {}
LIT = {}
DARKB = ("#3a3470", "#332e66", "#3d356f", "#2f2a5e")
for i in range(N):
    w, h = random.randint(78, 108), random.randint(130, 215)
    if i in HOT:
        w, h = 104, 200
    body = random.choice(BCOL)
    LIT[i] = body
    wins = ""
    cols, rows = max(2, (w - 20) // 24), max(3, (h - 50) // 28)
    n = 0
    for r in range(rows):
        for c in range(cols):
            wx = 12 + c * ((w - 24 - 14) / max(cols - 1, 1))
            wins += f'<i class="win" style="left:{wx:.0f}px;top:{36 + r * 28}px"></i>'
            n += 1
    WINS[i] = n
    roof = random.choice(("flat", "peak", "dome"))
    roof_h = ""
    if roof == "peak":
        roof_h = f'<i class="roof" style="left:{-6}px;top:-34px;width:0;height:0;border-left:{w // 2 + 6}px solid transparent;border-right:{w // 2 + 6}px solid transparent;border-bottom:36px solid #8a7bd6"></i>'
    elif roof == "dome":
        roof_h = f'<i class="roof" style="left:{w * .15:.0f}px;top:-30px;width:{w * .7:.0f}px;height:60px;border-radius:50% 50% 0 0;background:#8a7bd6"></i>'
    sign = ""
    if random.random() < .7 or i in HOT:
        sg = SIGNC[i % len(SIGNC)]
        sign = f'<div class="sign" style="left:{w * .2:.0f}px;top:8px;width:{w * .6:.0f}px;height:22px;background:linear-gradient(90deg,{sg})"><i id="sg{i}" style="background:#000"></i></div>'
    crowd = ""
    if i in HOT:
        crowd = '<div class="crowd" id="cr' + str(i) + '">' + "".join(seated(f"c{i}_{k}", x - 22, -R - 46, 44, turn=True, style="--turn:1")
                                                                        for k, x in enumerate((-80, -42, -4, 34, 72))) + '</div>'
    glow = f'<i class="bglow" id="bg{i}" style="left:{-w}px;top:{-R - h - 40}px;width:{2 * w}px;height:{h + 120}px"></i>' if i in HOT else ""
    lamp = f'<i class="lamp" style="left:{w // 2 + 14}px;top:{-R - 56}px"><b id="lb{i}"></b></i>' if i == 2 else ""
    BLD += (f'<div class="bld" id="bw{i}" style="transform:rotate({i * TH:.2f}deg)">{glow}'
            f'<div class="bb" id="b{i}" style="left:{-w // 2}px;top:{-R - h + 4}px;width:{w}px;height:{h}px;background:{random.choice(DARKB)}">{roof_h}{wins}{sign}</div>'
            f'{lamp}{crowd}</div>')
TOWER = ('<div class="bld" style="transform:rotate(' + f"{4.5 * TH:.2f}" + 'deg)"><div class="tower" id="tower" style="top:' + str(-R - 330 + 4) + 'px">'
         '<i class="spire"><b></b></i>' + "".join(f'<i class="tw" style="left:{14 + c * 36}px;top:{30 + r * 30}px"></i>' for r in range(9) for c in range(2)) + '</div></div>')
WORLDH = f'<div id="world">{BLD}{TOWER}</div>'
FW = ""
FWP = [(300, 760), (790, 720), (200, 1040), (880, 1010)]
for f, (x, y) in enumerate(FWP):
    col = ("#ffd27a", "#ff7ab0", "#9ad0ff", "#ffffff")[f]
    FW += f'<div class="fw" id="fw{f}" style="left:{x}px;top:{y}px">' + "".join(f'<i id="fw{f}_{k}" style="background:{col};box-shadow:0 0 10px {col}"></i>' for k in range(12)) + '</div>'
SAT = ('<svg id="sat" viewBox="0 0 180 120"><rect x="60" y="40" width="60" height="40" rx="8" fill="#e8e4ff"/><rect x="0" y="48" width="54" height="24" fill="#6a8cff"/>'
       '<rect x="126" y="48" width="54" height="24" fill="#6a8cff"/><circle cx="90" cy="92" r="10" fill="#F343A2"/><path d="M90 40 V20" stroke="#e8e4ff" stroke-width="4"/>'
       '<circle cx="90" cy="16" r="6" fill="#ffd27a"/></svg><div id="satbeam"></div>')
CTA = '<div class="cta" id="cta"><small>YOUR NEXT REEL IS WAITING</small><b>COMMENT<br>GROW</b></div>'
PLANET = f'{DISC}{WORLDH}<div id="beam"></div><i id="seed"></i>{FW}'

# =======================================================================================================================
# TIMELINE
for i in range(3):
    js(f'tl.fromTo("#cm{i}", {{opacity: 0, x: 0, y: 0}}, {{keyframes: [{{opacity: 1, x: -260, y: 140, duration: .5}}, {{opacity: 0, x: -520, y: 280, duration: .5}}], '
       f'immediateRender: false}}, {2 + i * 6.5:.2f});')
js(f'tl.fromTo("#atmo", {{scale: 1}}, {{scale: 1.04, duration: 1.6, yoyo: true, repeat: {int(DUR / 1.6)}, ease: "sine.inOut", immediateRender: false}}, 0);')
# ---- p0: dolly in --------------------------------------------------------------------------------------------------------------
ft("#rp", 0, 1.9, "{scale: .32, y: -260}", "{scale: 1, y: 0}", "power2.out")
ft("#rs", 0, 2.4, "{scale: .8}", "{scale: 1}", "power2.out")
sfx("whoosh_big", .05)
head("h0", [[("This", ""), ("is", ""), ("your", "")], [("account.", "pk")]], "p0", size=110)
world(0, 60, .01)
t_th = T("p2", "Then")
world(.02, 18, t_th - .05, "none")
stat(.9, "YOUR ACCOUNT")

# ---- p1: a ghost town --------------------------------------------------------------------------------------------------------
t1 = T0["p1"][0]
head("h1", [[("Every", ""), ("reel", ""), ("you've", "")], [("ever", ""), ("posted…", "")], [("mostly", ""), ("a", ""), ("ghost", "cd"), ("town.", "cd")]], "p1", size=80)
for i in range(N):
    if f'id="sg{i}"' in BLD:
        js(f'tl.fromTo("#sg{i}", {{opacity: .25}}, {{keyframes: [{{opacity: .75, duration: .06}}, {{opacity: .2, duration: .1}}, {{opacity: .7, duration: .05}}, {{opacity: .25, duration: .2}}], '
           f'repeat: 3, repeatDelay: {random.uniform(.6, 1.4):.2f}, immediateRender: false}}, {t1 + random.uniform(0, 1.5):.2f});')
js(f'tl.fromTo("#lb2", {{opacity: 1}}, {{keyframes: [{{opacity: .2, duration: .08}}, {{opacity: 1, duration: .08}}, {{opacity: .1, duration: .12}}, {{opacity: 1, duration: .3}}], '
   f'repeat: 4, repeatDelay: .5, immediateRender: false}}, {t1:.2f});')
stat(T("p1", "ghost") - .1, "MOSTLY DARK")
sfx("riser_short", T("p1", "ghost") - .4)

# ---- p2: Cree scans ----------------------------------------------------------------------------------------------------------------
t2 = T0["p2"][0]
head("h2", [[("Then", ""), ("Creedom", "pk"), ("scans", "")], [("the", ""), ("whole", ""), ("planet.", "")]], "p2", size=88)
CF = (540, 700, .2)
cree_to(t2 - .2, *P(1260, 620, .2), d=.01)
st("#cree", t2 - .2, "{opacity: 1}")
pose(t2 - .2, "stand", flip=False, squash=False)
cree_to(t2 - .15, *P(*CF), d=.7, ease="power3.out")
sfx("whoosh", t2 - .15)
js(f'tl.fromTo("#creeb", {{y: 0}}, {{y: -10, duration: .8, yoyo: true, repeat: {int((DUR - t2) / .8)}, ease: "sine.inOut", immediateRender: false}}, {t2 + .6:.3f});')
t_sc = T("p2", "scans")
ft("#beam", t_sc, .35, "{opacity: 0, scaleY: .2}", "{opacity: 1, scaleY: 1}", "power3.out")
js(f'tl.fromTo("#beam", {{opacity: 1}}, {{opacity: .65, duration: .25, yoyo: true, repeat: 15, ease: "sine.inOut", immediateRender: false}}, {t_sc + .4:.3f});')
sfx("riser", t_sc)
stat(t_sc, "SCANNING YOUR ACCOUNT")
world(T("p2", "planet") - .1, 0, .6)

# ---- p3: dark, dark, dark; these two -----------------------------------------------------------------------------------------------
t3 = T0["p3"][0]
head("h3a", [[("Dark.", "cd"), ("Dark.", "cd"), ("Dark.", "cd")]], "p3", size=110)
for k in range(3):
    td = T("p3", "Dark", k)
    world(td - .18, -(k + 1) * TH, .3)
    tag(td + .05, "EMPTY", "c", .32)
    sfx("glitch", td)
t_tw = T("p3", "these")
head("h3b", [[("But", ""), ("these", ""), ("two?", "gd")], [("Your", ""), ("people", "gd")], [("showed", ""), ("up", ""), ("here.", "")]], "p3", size=82, after=T("p3", "But") - .05)
world(t_tw - .25, -4.5 * TH, .5)
for k, i in enumerate(HOT):
    tl_ = t_tw + .15 + k * .2
    js(f'tl.to("#b{i} .win", {{backgroundColor: "#ffd27a", boxShadow: "0 0 10px rgba(255,210,120,.9)", duration: .12, stagger: {{each: .012, from: "random"}}}}, {tl_:.3f});')
    js(f'tl.to("#b{i}", {{backgroundColor: "{LIT[i]}", duration: .3}}, {tl_:.3f});')
    ft(f"#bg{i}", tl_, .4, "{opacity: 0}", "{opacity: 1}", "power2.out")
    js(f'tl.to("#cr{i} .cb", {{opacity: 1, duration: .2, stagger: .06}}, {tl_ + .2:.3f});')
    js(f'tl.fromTo("#cr{i} .cb", {{y: 20}}, {{y: 0, duration: .3, stagger: .06, ease: "back.out(3)", immediateRender: false}}, {tl_ + .2:.3f});')
    sfx("chime", tl_)
tag(t_tw + .5, "MOST SAVED · EXAMPLE", "h", 2.2)
stat(t_tw + .3, "2 BUILDINGS FULL", hot=True)
pose(t_tw + .2, "cheer")
sparkle(t_tw + .3, .6)
js(f'tl.fromTo("#rp", {{scale: 1}}, {{scale: 1.12, duration: 1.4, ease: "power2.inOut", immediateRender: false}}, {t_tw:.3f});')

# ---- p4: the next reel grows -------------------------------------------------------------------------------------------------------
t4 = T0["p4"][0]
head("h4", [[("So", ""), ("your", ""), ("next", ""), ("reel", "pk")], [("goes", ""), ("right", ""), ("where", "")], [("they", ""), ("are.", "")]], "p4", size=84)
js(f'tl.to("#rp", {{scale: 1, duration: .5, ease: "power2.inOut"}}, {t4 - .2:.3f});')
pose(t4 - .1, "stand")
ft("#seed", t4, .45, "{opacity: 1, y: 0, scale: .6}", "{opacity: 1, y: 235, scale: 1}", "power2.in")
st("#seed", t4 + .47, "{opacity: 0}")
flash(t4 + .45, .45, .3)
sfx("pop", t4 + .45)
t_nx = T("p4", "next")
ft("#tower", t_nx - .05, .7, "{scaleY: 0}", "{scaleY: 1}", "back.out(1.4)")
sfx("whoosh", t_nx - .05)
sfx("sparkle", t_nx + .3)
tag(t_nx + .5, "NEXT REEL · EXAMPLE", "p", 0)
stat(t_nx, "YOUR NEXT REEL", hot=True)
t_go = T("p4", "goes")
for k, i in enumerate(HOT):
    js(f'tl.to("#cr{i} .cb", {{x: {58 if k == 0 else -58}, duration: .9, stagger: .05, ease: "power1.inOut"}}, {t_go:.3f});')
    js(f'tl.fromTo("#cr{i} .cbs", {{y: 0}}, {{y: -5, duration: .12, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}}, {t_go:.3f});')

# ---- p5: the whole planet lights up (the music lifts on "lights") -----------------------------------------------------------------
t5 = T0["p5"][0]
t_li = T("p5", "lights")
head("h5", [[("And", ""), ("the", ""), ("whole", "")], [("planet", ""), ("lights", "gd"), ("up.", "gd")]], "p5", size=96)
to(TAGS and f"#tg{len(TAGS) - 1}" or "#flash", t_li - .2, .2, "{opacity: 0}")
for i in range(N):
    d = min(abs(i - 4.5), N - abs(i - 4.5))
    tk = t_li + d * .13
    if i not in HOT:
        js(f'tl.to("#b{i}", {{backgroundColor: "{LIT[i]}", duration: .25}}, {tk:.3f});')
        js(f'tl.to("#b{i} .win", {{backgroundColor: "#ffd27a", boxShadow: "0 0 10px rgba(255,210,120,.9)", duration: .1, stagger: {{each: .008, from: "random"}}}}, {tk:.3f});')
    if i % 2 == 0:
        sfx("ping", tk)
to("#shade", t_li, 1.0, "{opacity: .15}", "power1.inOut")
to("#warm", t_li, 1.0, "{opacity: 1}", "power1.inOut")
flash(t_li, .55, .4)
sfx("impact", t_li)
js(f'tl.fromTo("#rp", {{scale: 1}}, {{keyframes: [{{scale: 1.05, duration: .1}}, {{scale: 1, duration: .5, ease: "power3.out"}}], immediateRender: false}}, {t_li:.3f});')
for f in range(4):
    tf = t_li + .15 + f * .22
    for k in range(12):
        a = k * math.pi * 2 / 12
        js(f'tl.fromTo("#fw{f}_{k}", {{x: 0, y: 0, opacity: 1, scale: 1}}, {{x: {math.cos(a) * 170:.0f}, y: {math.sin(a) * 170 + 40:.0f}, opacity: 0, scale: .4, duration: .9, '
           f'ease: "power2.out", immediateRender: false}}, {tf:.3f});')
    sfx("pop", tf)
for i in HOT:
    js(f'tl.to("#cr{i} .cbs", {{"--arms": 1, duration: .15}}, {t_li:.3f});')
pose(t_li, "cheer")
cree_hop(t_li + .05, 40, 2)
stat(t_li, "LIGHTS ON", hot=True)
world(t_li + .3, -4.5 * TH - 10, T0["p6"][0] - t_li - .5, "sine.inOut")

# ---- p6 CTA: the satellite beam ---------------------------------------------------------------------------------------------------
t6 = T0["p6"][0]
head("h6", [[("and", ""), ("I'll", ""), ("send", ""), ("you", "")], [("the", ""), ("secret.", "pk")]], "p6", size=96, after=T("p6", "and"))
to(f"#st{len(STAT) - 1}", t6 - .2, .2, "{opacity: 0}")
world(t6 - .3, -4.5 * TH + 60, .8, "power2.inOut")
cree_to(t6 - .3, *P(150, 1560, .22), d=.6)
to("#beam", t6 - .3, .2, "{opacity: 0}")
ft("#sat", t6 - .2, .5, "{opacity: 0, x: 200, y: -120}", "{opacity: 1, x: 0, y: 0}", "power3.out")
ft("#satbeam", t6 + .1, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
ft("#cta", t6 + .15, .4, "{opacity: 0, scale: 1.3, filter: 'blur(12px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "back.out(1.8)")
js(f'tl.fromTo("#cta b", {{scale: 1}}, {{scale: 1.05, duration: .35, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {T("p6", "GROW") + .3:.3f});')
sfx("whoosh", t6 - .2)
sfx("ding", T("p6", "GROW"))
pose(t6, "wave", flip=False)

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: Planet You 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      {CHIBI_DEFS}
      <div class="rig" id="rs">{SPACE}</div>
      <div class="rig" id="rp">{PLANET}<div style="position:absolute;inset:0;z-index:16">{cree_html()}</div></div>
      <div id="vig"></div>
      {"".join(TAGS)}{SAT}{CTA}
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
