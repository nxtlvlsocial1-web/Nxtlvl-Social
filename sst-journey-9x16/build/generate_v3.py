"""SST "The Journey Continues" (9:16, ~59 s): writes index.html, plan/sfx_events.json and plan/edit.json.

The client's editor brief (SST_The_Journey_Continues_Editor_Production_Brief.pdf), scene by scene: the master VO verbatim
(plan/words.json from build/vo_pick.py, lines placed on the brief's time codes), the brief's on-screen text per scene,
English subtitles (the script's own wording, max two lines), Pexels footage cut and graded by build/prep_shots.py
(plan/edl.json) in a cinematic band with slow push-ins and soft dissolves, a restrained glitch only in the challenge
section (never readable, no fake evidence), the light warming from the pause on, and a deep-navy end card with the exact
official SST logo (unaltered, on a white card) and the closing line. Palette: deep navy, matte black, white, royal blue.
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
EDL = json.load(open(os.path.join(ROOT, "plan", "edl.json")))
SCRIPT = json.load(open(os.path.join(ROOT, "plan", "sentences.json")))    # sentence id -> the script's text (build/relabel.py)
LW = {}
for w in W:
    LW.setdefault(w["line"], []).append(w)
JS, SFX, HTML = [], [], []
NAVY, INK, BLUE, BLUE2 = "#0b1526", "#05080f", "#2f6bdc", "#6f9bff"
BX, BY, BWID, BHGT = 0, 380, 1080, 1160          # the footage band


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power2.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {max(0, t):.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {max(0, t):.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


start = {k: v[0]["t0"] for k, v in LW.items()}
endl = {k: v[-1]["t1"] for k, v in LW.items()}
DUR = 59.3

# ---- footage: one video per shot, alternating tracks so dissolves can overlap
clips = []
for k, s in enumerate(EDL["shots"]):
    t, d = s["t"], s["d"]
    nxt_cut = k + 1 < len(EDL["shots"]) and EDL["shots"][k + 1].get("cut")
    vis = d + (.08 if nxt_cut else EDL["handle"] if k < len(EDL["shots"]) - 1 else .0)
    clips.append(f'<div class="shot" id="w{s["id"]}"><video id="{s["id"]}" class="clip" src="assets/video/{s["id"]}.mp4" muted playsinline '
                 f'data-start="{t:.3f}" data-duration="{vis:.3f}" data-track-index="{1 + k % 2}"></video></div>')
    fade = 1.2 if k == 0 else (.05 if s.get("cut") else .5)          # the allegation montage cuts hard
    ft(f"#w{s['id']}", t, fade, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
    ft(f"#w{s['id']}", t, vis, "{scale: 1.0}", "{scale: 1.055}", "none")       # slow push-in
    to(f"#w{s['id']}", t + vis - .02, .01, "{opacity: 0}")
for o in EDL.get("overlays", []):
    clips.append(f'<div class="shot ovl" id="w{o["id"]}"><video id="{o["id"]}" class="clip" src="assets/video/{o["id"]}.mp4" muted playsinline '
                 f'data-start="{o["t"]:.3f}" data-duration="{o["d"]:.3f}" data-track-index="3"></video></div>')
    st(f"#w{o['id']}", o["t"], "{opacity: .85}")
    to(f"#w{o['id']}", o["t"] + o["d"] - .02, .01, "{opacity: 0}")
# the band hands over to the end card under the closing lines
to("#band", start["j15"] - .5, .9, "{opacity: 0}", "sine.inOut")

# ---- the brief's on-screen text, per scene (white with royal-blue emphasis)
SCENES = [("EVERY VISION HAS A JOURNEY.", "", "", 0.0, start["j02"] - .3),
          ("YEARS OF WORK.", "A VISION WITH PURPOSE.", "", start["j02"], start["j05"] - .3),
          ("CHALLENGES BEHIND THE SCENES.", "", "", start["j05"], start["j06"] + 1.6),
          ("THE JOURNEY IS TESTED.", "THE VISION REMAINS.", "", start["j07"], start["j11"] - .3),
          ("THE WORK CONTINUES.", "THE VISION MOVES FORWARD.", "", start["j11"], start["j13"] - .3)]
for k, (a, b, note, t0, t1) in enumerate(SCENES):
    inner = f'<div class="h1" id="hd{k}a">{a}</div>' + (f'<div class="h2" id="hd{k}b">{b}</div>' if b else "") + \
            (f'<div class="note" id="hd{k}n">{note}</div>' if note else "")
    HTML.append(f'<div class="head" id="hd{k}">{inner}</div>')
    if k == 0:
        pass                                         # on screen from frame 1 (the hook inside 2 s); CSS opacity 1
    else:
        ft(f"#hd{k}", t0, .6, "{opacity: 0, y: 14}", "{opacity: 1, y: 0}", "power2.out")
    if b:
        tb = {1: start["j03"], 3: start["j09"] - .2, 4: start["j12"]}.get(k, t0 + .8)
        ft(f"#hd{k}b", tb, .6, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "power2.out")
    if note:
        ft(f"#hd{k}n", start["j06"] - .2, .6, "{opacity: 0}", "{opacity: 1}", "power1.out")
    to(f"#hd{k}", t1, .4, "{opacity: 0}", "power1.in")

# ---- the allegations, as the account describes them: a 2x2 list that lights word by word, the attribution always under it
J6 = {w["w"].lower().strip(",."): w["t0"] for w in LW["j06"]}
ALG = [("HACKING.", J6["hacking"]), ("TRACKING.", J6["tracking"]), ("STALKING.", J6["stalking"]), ("ENGINEERED ACCIDENTS.", J6["accidents"])]
items = "".join(f'<span class="al" id="al{k}">{w}</span>' for k, (w, _) in enumerate(ALG))
HTML.append(f'<div class="head" id="alg"><div class="algrid">{items}</div><div class="note" id="algn">ALLEGATIONS DESCRIBED IN A PUBLISHED ACCOUNT</div></div>')
ft("#alg", start["j06"] + 1.6, .4, "{opacity: 0}", "{opacity: 1}", "power1.out")
st("#algn", start["j06"] + 1.6, "{opacity: 1}")
for k, (w, at) in enumerate(ALG):
    ft(f"#al{k}", at - .06, .25, "{opacity: .22, y: 8}", "{opacity: 1, y: 0}", "power2.out")
    ft(f"#al{k}", at - .06, .5, "{'--u': 0}", "{'--u': 1}", "power2.out")
to("#alg", start["j07"] - .3, .4, "{opacity: 0}", "power1.in")

# ---- subtitles: the script's words, max two lines; long lines split at a natural pause
SPLIT = {"j06": [9, 16]}          # "...tracking and stalking," / "and accidents it says were deliberately engineered," / "all aimed at..."
subs = []
for lid in sorted(LW):
    if lid in ("j15", "j16"):                     # the end card carries these (logo = SST, the closing line)
        continue
    ws = LW[lid]
    words = SCRIPT[lid].split()
    if len(words) != len(ws):
        words = [w["w"] for w in ws]
    cuts = [0] + SPLIT.get(lid, []) + [len(words)]
    parts = [(words[a:b], ws[a:b]) for a, b in zip(cuts, cuts[1:])]
    for txt, tw in parts:
        subs.append((" ".join(txt), tw[0]["t0"], tw[-1]["t1"]))
for k, (txt, t0, t1) in enumerate(subs):
    nxt = subs[k + 1][1] if k + 1 < len(subs) else DUR
    off = min(t1 + .5, nxt - .06)
    HTML.append(f'<div class="sub" id="sb{k}">{txt}</div>')
    ft(f"#sb{k}", t0 - .08, .22, "{opacity: 0}", "{opacity: 1}", "power1.out")
    to(f"#sb{k}", off, .18, "{opacity: 0}", "power1.in")

# ---- the challenge section: restrained glitch on the band, blurred notification glows, faint network lines
gl0, gl1 = start["j05"], start["j07"] - .2
ft("#scan", gl0, 1.0, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
to("#scan", gl1, 1.0, "{opacity: 0}", "sine.inOut")
ft("#cool", gl0 - .5, 1.5, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
to("#cool", start["j10"], 2.0, "{opacity: 0}", "sine.inOut")
HITS = [gl0 + .05] + [s["t"] for s in EDL["shots"] if s.get("cut")] + [s["t"] for s in EDL["shots"] if s["id"] in ("sh20", "sh09")]
for k, at in enumerate(HITS):
    js(f'tl.set("#band", {{filter: "drop-shadow(5px 0 0 rgba(255,40,70,.55)) drop-shadow(-5px 0 0 rgba(60,170,255,.55))", x: {6 if k % 2 else -6}}}, {at:.3f});')
    js(f'tl.set("#slice", {{opacity: .9, y: {[120, 460, 820, 300, 640, 980, 220, 760][k % 8]}}}, {at:.3f});')
    js(f'tl.set("#band", {{filter: "none", x: 0}}, {at + .09:.3f});')
    js(f'tl.set("#slice", {{opacity: 0}}, {at + .09:.3f});')
    sfx("glitch", at)
sh07 = next(s for s in EDL["shots"] if s["id"] == "sh07")
for k in range(3):
    ft(f"#nt{k}", sh07["t"] + .02 + k * .1, .2, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "power2.out")
    to(f"#nt{k}", sh07["t"] + sh07["d"] - .05, .1, "{opacity: 0}")
sfx("notify_soft", sh07["t"] + .02)
# TRACKING: location rings pulse over the phone (symbolic, no map, no data)
ft("#track", sh07["t"], .12, "{opacity: 0}", "{opacity: 1}", "none")
js(f'tl.fromTo("#track circle", {{attr: {{r: 10}}, opacity: .9}}, {{attr: {{r: 260}}, opacity: 0, duration: .9, stagger: .18, ease: "power1.out", immediateRender: false}}, {sh07["t"]:.3f});')
to("#track", sh07["t"] + sh07["d"] - .02, .05, "{opacity: 0}")
sfx("thump", J6["accidents"] - .04)
js(f'tl.fromTo("#net path", {{strokeDashoffset: 900}}, {{strokeDashoffset: 0, duration: 4.5, ease: "power1.inOut", stagger: .4, immediateRender: false}}, {gl0 + .5:.3f});')
ft("#net", gl0 + .5, 1.0, "{opacity: 0}", "{opacity: 1}")
to("#net", gl1 - 1.0, 1.0, "{opacity: 0}")

# ---- the light warms from the pause on (the return to work), dawn by the end
ft("#warm", start["j10"] + .4, 6.0, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
to("#warm", start["j15"] - .5, .9, "{opacity: 0}")

# ---- end card: deep navy, one blue light sweep, the exact SST logo, the closing line
te = start["j15"]
ft("#endbg", te - .5, .9, "{opacity: 0}", "{opacity: 1}", "sine.inOut")
ft("#sweep", te - .3, 1.6, "{x: -1400, opacity: 0}", "{x: 1400, opacity: 1}", "power2.inOut")
ft("#logo", te - .05, .9, "{opacity: 0, scale: .96}", "{opacity: 1, scale: 1}", "power2.out")
ft("#tag1", start["j16"] - .05, .8, "{opacity: 0, y: 12}", "{opacity: 1, y: 0}", "power2.out")
ft("#tagrule", start["j16"] + .2, .9, "{scaleX: 0}", "{scaleX: 1}", "power2.inOut")

# ---- sound
sfx("whoosh_soft", start["j02"] - .35)
sfx("whoosh_soft", start["j07"] - .4)
sfx("whoosh_soft", start["j11"] - .4)
sfx("riser_low", te - 1.1)
sfx("impact", te - .02)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: linear-gradient(180deg, {NAVY} 0%, #08101d 45%, {INK} 100%); font-family: Mont; color: #fff; }}
#band {{ position: absolute; left: {BX}px; top: {BY}px; width: {BWID}px; height: {BHGT}px; overflow: hidden;
  -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 110px, #000 calc(100% - 140px), transparent 100%);
  mask-image: linear-gradient(180deg, transparent 0, #000 110px, #000 calc(100% - 140px), transparent 100%); }}
.shot {{ position: absolute; inset: 0; opacity: 0; transform-origin: 50% 45%; }}
.clip {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#cool {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(90% 70% at 50% 50%, rgba(10,25,60,0) 30%, rgba(4,10,28,.55) 100%); mix-blend-mode: multiply; }}
#warm {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(80% 60% at 70% 20%, rgba(255,196,140,.22), rgba(255,196,140,0) 70%); mix-blend-mode: soft-light; }}
#scan {{ position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(120,160,255,.05) 0 2px, rgba(0,0,0,0) 2px 5px); mix-blend-mode: screen; }}
.algrid {{ display: grid; grid-template-columns: auto auto; gap: 8px 34px; justify-content: center; }}
.al {{ --u: 0; position: relative; font-weight: 800; font-size: 40px; letter-spacing: .05em; white-space: nowrap; opacity: .22; }}
.al::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: -6px; height: 4px; background: {BLUE}; transform: scaleX(var(--u)); transform-origin: 0 50%; }}
#algn {{ margin-top: 20px; }}
#track {{ position: absolute; inset: 0; opacity: 0; }}
#track circle {{ fill: none; stroke: rgba(130,180,255,.8); stroke-width: 3; }}
.ovl {{ mix-blend-mode: screen; }}
#slice {{ position: absolute; left: 0; right: 0; height: 26px; opacity: 0; background: linear-gradient(90deg, rgba(60,150,255,0), rgba(120,190,255,.35), rgba(255,60,90,.25), rgba(60,150,255,0)); mix-blend-mode: screen; }}
.nt {{ position: absolute; left: 330px; width: 420px; height: 96px; border-radius: 26px; opacity: 0; background: rgba(150,185,255,.28); filter: blur(14px); }}
#net {{ position: absolute; inset: 0; opacity: 0; mix-blend-mode: screen; }}
#net path {{ fill: none; stroke: rgba(110,160,255,.2); stroke-width: 2; stroke-dasharray: 900; }}
#net circle {{ fill: rgba(140,185,255,.35); }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(110% 70% at 50% 52%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); }}
#grain {{ position: absolute; inset: -50%; pointer-events: none; opacity: .06; background-image: repeating-radial-gradient(circle at 23% 41%, rgba(255,255,255,.55) 0 1px, transparent 1px 3px); mix-blend-mode: overlay; }}
.head {{ position: absolute; left: 40px; right: 40px; top: 222px; text-align: center; opacity: 0; }}
#hd0 {{ opacity: 1; }}
.h1 {{ font-weight: 800; font-size: 43px; letter-spacing: .05em; white-space: nowrap; line-height: 1.15; }}
.h2 {{ font-weight: 800; font-size: 43px; letter-spacing: .05em; white-space: nowrap; line-height: 1.15; color: {BLUE2}; opacity: 0; }}
.note {{ margin-top: 12px; font-family: Inter; font-weight: 600; font-size: 24px; letter-spacing: .14em; color: rgba(255,255,255,.78); opacity: 0; }}
.sub {{ position: absolute; left: 90px; right: 90px; top: 1418px; text-align: center; font-family: Inter; font-weight: 600; font-size: 40px; line-height: 1.28;
  color: #fff; opacity: 0; text-shadow: 0 2px 4px rgba(0,0,0,.9), 0 0 24px rgba(0,0,0,.8); }}
#endbg {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(70% 45% at 50% 46%, #13254a 0%, {NAVY} 55%, {INK} 100%); }}
#sweep {{ position: absolute; top: 0; bottom: 0; left: 0; width: 900px; opacity: 0; transform: skewX(-18deg);
  background: linear-gradient(90deg, rgba(47,107,220,0), rgba(80,140,255,.28), rgba(47,107,220,0)); filter: blur(20px); }}
#logo {{ position: absolute; left: 190px; width: 700px; top: 700px; padding: 34px 40px; border-radius: 28px; background: #fff; opacity: 0;
  box-shadow: 0 40px 100px rgba(0,0,0,.55), 0 0 60px rgba(47,107,220,.25); }}
#logo img {{ display: block; width: 100%; }}
#tag {{ position: absolute; left: 60px; right: 60px; top: 1150px; text-align: center; }}
#tag1 {{ font-weight: 800; font-size: 44px; letter-spacing: .08em; color: #fff; opacity: 0; }}
#tagrule {{ width: 220px; height: 4px; margin: 26px auto 0; background: {BLUE}; transform: scaleX(0); }}
"""
net = '<svg id="net" viewBox="0 0 1080 1160"><path d="M60 900 L300 640 L520 760 L760 420 L1020 560"/><path d="M120 200 L360 360 L600 240 L860 330"/>' \
      '<path d="M300 640 L360 360 M760 420 L600 240 M520 760 L700 980"/>' + \
      "".join(f'<circle cx="{x}" cy="{y}" r="5"/>' for x, y in [(60, 900), (300, 640), (520, 760), (760, 420), (1020, 560), (120, 200), (360, 360), (600, 240), (860, 330), (700, 980)]) + "</svg>"
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>SST The Journey Continues 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="band" data-layout-allow-overlap>
        {chr(10).join("        " + c for c in clips).strip()}
        <div id="cool"></div>
        <div id="warm"></div>
        {net}
        <div class="nt" id="nt0" style="top:330px"></div><div class="nt" id="nt1" style="top:450px"></div><div class="nt" id="nt2" style="top:570px"></div>
        <svg id="track" viewBox="0 0 1080 1160"><circle cx="540" cy="560" r="10"/><circle cx="540" cy="560" r="10"/><circle cx="540" cy="560" r="10"/>
          <path d="M540 470 V650 M450 560 H630" stroke="rgba(130,180,255,.7)" stroke-width="2"/></svg>
        <div id="scan"></div>
        <div id="slice"></div>
      </div>
      <div id="endbg"><div id="sweep"></div></div>
      <div id="logo"><img src="assets/img/sst_logo.jpg" alt="SST"></div>
      <div id="tag"><div id="tag1">THE JOURNEY IS FAR FROM OVER.</div><div id="tagrule"></div></div>
      {chr(10).join(HTML)}
      <div id="vig"></div>
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
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {len(subs)} subtitles")
