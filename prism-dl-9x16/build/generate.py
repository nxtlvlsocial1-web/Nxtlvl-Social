"""AI.NXTLVL "Prism: a free download manager" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json.

The 3D stage (assets/js/scene.js) is a pure function of time; this file times it to the voice (plan/words.json from
build/vo_pick.py) through window.PR_T and lays the type over it on one paused GSAP timeline, on a fixed grid (all centred):
headline band (two lines: white + lavender serif accent, y 300-560), labels glued to the 3D objects, the live caption
(three words at a time, y 1480). Facts: plan/prism_readme.md (the project's README, MIT, 1.6k stars on 2026-11-25).
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = []
for w in json.load(open(os.path.join(ROOT, "plan", "words.json"))):
    if W and w["w"][:1] in ".,-" and W[-1]["line"] == w["line"]:
        W[-1]["w"] += w["w"]; W[-1]["t1"] = w["t1"]
    else:
        W.append(dict(w))
LW = {}
for w in W:
    LW.setdefault(w["line"], []).append(w)
JS, SFX, HTML = [], [], []
VIOLET, LAV, NIGHT = "#7a2ffb", "#b687f9", "#07050f"


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {max(0, t):.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {max(0, t):.3f});')


def key(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def wt(line, words, n=0, end=False):
    words = words if isinstance(words, (list, tuple)) else [words]
    hits = [w for w in LW[line] if any(key(w["w"]).startswith(x) for x in words)]
    if not hits:
        raise SystemExit(f"{line}: none of {words} in {[w['w'] for w in LW[line]]}")
    h = hits[min(n, len(hits) - 1)]
    return h["t1"] if end else h["t0"]


start = {k: v[0]["t0"] for k, v in LW.items()}
END = max(w["t1"] for w in W)
DUR = round(END + 1.4, 2)
T = {**{k: start[k] for k in start},
     "seventeen": wt("p00", ["seventeen", "17"]), "four": wt("p00", ["four", "4"]), "minutes": wt("p00", "minutes"),
     "alternative": wt("p01", "alternative"), "cap": wt("p02", "cap"), "split": wt("p03", "split"),
     "thirtytwo": wt("p03", ["thirty", "32"]), "once": wt("p03", "once"), "half": wt("p04", "half"), "idle": wt("p04", "idle"),
     "eighteen": wt("p05", ["eighteen", "1800", "18"]), "k8": wt("p05", ["8k", "eight", "8"]), "mp3": wt("p05", "mp3"),
     "dies": wt("p06", "dies"), "picks": wt("p06", "picks"), "stopped": wt("p06", "stopped"), "hugging": wt("p07", "hugging"),
     "internet": wt("p08", "internet"), "slow": wt("p08", "slow"), "callkw": wt("p10", "prism"), "end": DUR}

# ---- headline band: one two-line headline per beat (white line + lavender accent)
HEADS = [("1 GB file.", "17 seconds.", 0.0), ("It's called", "Prism.", T["p01"]), ("The free alternative", "to IDM.", T["alternative"] - .1),
         ("1 file.", "1 connection.", T["p02"]), ("Servers cap", "each one.", T["cap"] - .1), ("Up to 32 parts.", "All at once.", T["p03"]),
         ("Done early?", "Take half.", T["p04"]), ("Nothing", "sits idle.", T["idle"] - .1), ("Videos too.", "1,800+ sites.", T["p05"]),
         ("Or just", "the MP3.", T["mp3"] - .1), ("Laptop dies?", "It picks up.", T["p06"]), ("Torrents.", "AI models.", T["p07"]),
         ("One honest catch.", "", T["p08"]), ("Your internet", "is the ceiling.", T["internet"] - .1), ("Send this", "to a friend.", T["p09"]),
         ("Comment", "PRISM.", T["p10"])]
for k, (a, b, t0) in enumerate(HEADS):
    t1 = HEADS[k + 1][2] if k + 1 < len(HEADS) else DUR + 1
    HTML.append(f'<div class="hd{" on" if k == 0 else ""}" id="hd{k}"><div class="h1">{a}</div>' + (f'<div class="h2">{b}</div>' if b else "") + "</div>")
    if k:
        ft(f"#hd{k} .h1", t0, .35, "{opacity: 0, y: 26}", "{opacity: 1, y: 0}", "back.out(1.8)")
        if b:
            ft(f"#hd{k} .h2", t0 + .12, .4, "{opacity: 0, y: 26}", "{opacity: 1, y: 0}", "back.out(1.8)")
        js(f'tl.set("#hd{k}", {{opacity: 1}}, {t0:.3f});')
    if t1 < DUR:
        to(f"#hd{k}", t1 - .14, .14, "{opacity: 0, y: -20, filter: 'blur(6px)'}", "power2.in")
    sfx("whoosh" if k % 2 else "swish", t0 - .12)

# ---- live caption: three words at a time, the spoken one bright
k = 0
for lid in sorted(LW):
    ws = LW[lid]
    for i in range(0, len(ws), 3):
        chunk = ws[i:i + 3]
        nxt = ws[i + 3]["t0"] if i + 3 < len(ws) else chunk[-1]["t1"] + .25
        spans = " ".join(f'<span id="cw{k}_{j}">{w["w"]}</span>' for j, w in enumerate(chunk))
        HTML.append(f'<div class="cap" id="cp{k}">{spans}</div>')
        ft(f"#cp{k}", chunk[0]["t0"] - .06, .12, "{opacity: 0}", "{opacity: 1}", "none")
        for j, w in enumerate(chunk):
            ft(f"#cw{k}_{j}", w["t0"] - .04, .12, "{color: 'rgba(255,255,255,.42)'}", "{color: '#ffffff'}", "none")
        to(f"#cp{k}", nxt - .06, .06, "{opacity: 0}", "none")
        k += 1

# ---- comment box (CTA) + flashes
tc = T["p10"]
ft("#cbox", tc - .05, .45, "{opacity: 0, y: 50, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for i, ch in enumerate("PRISM"):
    ft(f"#ck{i}", T["callkw"] - .2 + i * .06, .05, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["callkw"] - .2 + i * .06)
ft("#cpost", T["callkw"] + .2, .25, "{color: '#6b6585'}", "{color: '#7a2ffb'}", "power2.out")
for at, op in ((T["p01"], .35), (T["thirtytwo"], .3), (T["callkw"] + .3, .3)):
    js(f'tl.set("#flash", {{opacity: {op}}}, {at - .02:.3f});')
    to("#flash", at, .45, "{opacity: 0}", "power2.out")

# ---- sound design on the beats
sfx("riser_short", T["seventeen"] - .6); sfx("ding", T["seventeen"] + .5)
for i in range(8):
    sfx("tick", T["four"] - .5 + i * .14)
sfx("impact", T["p01"]); sfx("sparkle", T["p01"] + .15)
sfx("pop", T["alternative"])
sfx("thump", T["cap"] + .05)
sfx("riser_short", T["split"] - .6); sfx("impact", T["thirtytwo"]); sfx("sparkle", T["thirtytwo"] + .1)
for i in range(6):
    sfx("g_tick", T["split"] + i * .12)
sfx("g_correct", T["half"] - .55); sfx("g_swish", T["half"]); sfx("g_complete", T["idle"] + .2)
sfx("pop", T["eighteen"]); sfx("stamp", T["k8"]); sfx("g_pop", T["mp3"])
sfx("buzzer", T["dies"]); sfx("thump", T["dies"] + .35); sfx("g_levelup", T["picks"] + .2)
sfx("lock", T["p07"]); sfx("g_pickup", T["hugging"])
sfx("thump", T["internet"])
sfx("whoosh", tc - .1); sfx("impact", T["callkw"] + .3); sfx("g_complete", T["callkw"] + .4)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: #fff;
  background: radial-gradient(80% 45% at 15% 8%, rgba(127,27,248,.32), rgba(0,0,0,0) 70%), radial-gradient(80% 45% at 85% 95%, rgba(96,8,242,.3), rgba(0,0,0,0) 70%), {NIGHT}; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(100% 62% at 50% 52%, rgba(0,0,0,0) 55%, rgba(3,2,8,.6) 100%); }}
#flash {{ position: absolute; inset: 0; background: {VIOLET}; mix-blend-mode: screen; opacity: 0; pointer-events: none; }}
#bar {{ position: absolute; left: 70px; right: 70px; top: 258px; display: flex; justify-content: space-between; align-items: center;
  font-family: Mono; font-size: 24px; letter-spacing: .16em; color: rgba(255,255,255,.62); }}
#bar img {{ height: 40px; }}
#bar b {{ color: {LAV}; }}
.hd {{ position: absolute; left: 50px; right: 50px; top: 330px; text-align: center; opacity: 0; }}
.hd.on {{ opacity: 1; }}
.hd .h1, .hd .h2 {{ opacity: 0; }}
.hd.on .h1, .hd.on .h2 {{ opacity: 1; }}
.h1 {{ font-size: 84px; line-height: 1.0; letter-spacing: -.035em; text-shadow: 0 6px 30px rgba(0,0,0,.7); }}
.h2 {{ font-family: Serif; font-style: italic; font-weight: 400; font-size: 100px; line-height: 1.02; color: {LAV}; text-shadow: 0 0 40px rgba(122,47,251,.5); }}
.cap {{ position: absolute; left: 60px; right: 60px; top: 1470px; text-align: center; font-family: Inter; font-weight: 700; font-size: 46px; opacity: 0;
  color: rgba(255,255,255,.42); text-shadow: 0 3px 12px rgba(0,0,0,.8); }}
.lbl {{ position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap; }}
.tm {{ font-family: Mono; font-size: 96px; letter-spacing: -.02em; }}
#tmB {{ text-shadow: 0 0 30px rgba(182,135,249,.8); }}
#tmA {{ color: #c9c5da; }}
.sub {{ font-family: Inter; font-weight: 700; font-size: 32px; color: rgba(255,255,255,.75); }}
.chip {{ display: inline-block; font-family: Mono; font-size: 26px; letter-spacing: .1em; padding: 12px 22px; border-radius: 999px; margin: 0 6px;
  background: rgba(20,12,40,.75); border: 2px solid rgba(182,135,249,.6); }}
#capTag {{ font-family: Mono; font-size: 30px; color: #ff6b85; padding: 8px 18px; border-radius: 14px; background: rgba(40,8,18,.8); border: 2px solid #ff4d6d; }}
#nBig {{ text-align: center; }}
#nBig b {{ display: block; font-size: 110px; line-height: .9; letter-spacing: -.05em; }}
#nBig span.s {{ display: block; font-family: Inter; font-weight: 700; font-size: 26px; color: rgba(255,255,255,.75); }}
#fname {{ font-family: Mono; font-size: 30px; color: #e9e4ff; }}
#doneTag, #halfTag {{ font-family: Inter; font-weight: 700; font-size: 30px; padding: 8px 18px; border-radius: 12px; }}
#doneTag {{ background: #18a05a; }}
#halfTag {{ background: #ff4d6d; }}
#k8 {{ font-size: 64px; padding: 6px 22px; border-radius: 16px; background: {VIOLET}; box-shadow: 0 0 40px rgba(122,47,251,.7); }}
#sitesBox {{ text-align: center; }}
#sitesBox b {{ font-size: 96px; letter-spacing: -.04em; }}
#sitesBox span {{ display: block; font-family: Inter; font-weight: 700; font-size: 30px; color: rgba(255,255,255,.75); margin-top: -6px; }}
#pct {{ font-family: Mono; font-size: 70px; }}
#batt, #resumed {{ font-family: Inter; font-weight: 700; font-size: 34px; display: flex; align-items: center; gap: 14px; }}
#batt i {{ display: inline-block; width: 92px; height: 40px; border: 4px solid #ff4d6d; border-radius: 8px; padding: 3px; position: relative; }}
#batt i::after {{ content: ""; position: absolute; right: -12px; top: 10px; width: 6px; height: 14px; background: #ff4d6d; border-radius: 2px; }}
#battFill {{ display: block; height: 100%; background: #ff4d6d; border-radius: 3px; width: 70%; }}
#resumed {{ color: #7ee081; }}
#model {{ width: 560px; font-family: Inter; font-weight: 700; }}
#model .nm {{ font-family: Mono; font-size: 34px; color: #fff; }}
#model .rw {{ display: flex; gap: 12px; margin-top: 18px; }}
#model .rw span {{ font-family: Mono; font-size: 24px; padding: 6px 14px; border-radius: 10px; background: rgba(122,47,251,.35); }}
#model .ok {{ margin-top: 16px; font-size: 28px; color: #7ee081; }}
#pipeTag {{ font-family: Mono; font-size: 26px; letter-spacing: .1em; padding: 8px 16px; border-radius: 10px; background: rgba(20,12,40,.85); border: 2px solid {LAV}; }}
#bench {{ width: 760px; font-family: Inter; font-weight: 700; font-size: 28px; }}
#bench .r {{ display: flex; align-items: center; gap: 14px; margin-top: 12px; }}
#bench .r span {{ width: 220px; text-align: right; color: rgba(255,255,255,.8); }}
#bench .r i {{ height: 34px; border-radius: 8px; background: {VIOLET}; display: block; }}
#bench .r em {{ font-style: normal; font-family: Mono; font-size: 26px; }}
#bench .note {{ margin-top: 12px; text-align: center; font-size: 24px; color: rgba(255,255,255,.6); }}
#cbox {{ position: absolute; left: 90px; right: 90px; top: 1300px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 38px 0 26px; background: rgba(248,246,255,.97); color: {NIGHT}; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(122,47,251,.7); }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: conic-gradient(#ff4d6d, #ffd23f, #7ee081, #4d9bff, #d35cff, #ff4d6d); flex: none; }}
#cbox .tx {{ flex: 1; font-size: 56px; letter-spacing: .04em; }}
#cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #6b6585; }}
"""
labels = """
      <div class="lbl tm" id="tmA">4:16</div><div class="lbl tm" id="tmB">0:17</div>
      <div class="lbl sub" id="lbA">1 connection</div><div class="lbl sub" id="lbB">Prism</div>
      <div class="lbl" id="chips"><span class="chip">FREE</span><span class="chip">OPEN SOURCE</span><span class="chip">WIN · MAC · LINUX</span></div>
      <div class="lbl" id="capTag">4 MiB/s cap</div>
      <div class="lbl" id="nBig"><b id="nRays">1</b><span class="s">connections</span></div>
      <div class="lbl" id="fname">big-file.iso · 1 GB</div>
      <div class="lbl" id="doneTag">&#10003; done</div><div class="lbl" id="halfTag">takes half</div>
      <div class="lbl" id="k8">8K</div>
      <div class="lbl" id="sitesBox"><b id="sites">0+</b><span>sites, YouTube included</span></div>
      <div class="lbl" id="pct">63%</div>
      <div class="lbl" id="batt"><i><b id="battFill"></b></i>Battery dead</div>
      <div class="lbl" id="resumed">&#10003; Resumed at 63%</div>
      <div class="lbl" id="model"><div class="nm">Qwen/Qwen3-8B</div><div class="rw"><span>Hugging Face</span><span>GGUF</span></div><div class="ok">&#10003; SHA-256 verified</div></div>
      <div class="lbl" id="pipeTag">YOUR INTERNET</div>
      <div class="lbl" id="bench"><div class="r"><span>Prism</span><i style="width:300px"></i><em>25.1 MiB/s</em></div>
        <div class="r"><span>1 connection</span><i style="width:309px;background:#6b6585"></i><em>25.9 MiB/s</em></div>
        <div class="note">their test on a real 200 Mbit/s line: same speed</div></div>
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI.NXTLVL Prism download manager 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920" data-layout-allow-overflow></canvas>
      <div id="vig"></div>
      {labels}
      <div id="bar"><img src="assets/img/logo-wordmark.png" alt=""><span><b>AI</b> TOOLS</span></div>
      {chr(10).join(HTML)}
      <div id="cbox"><div class="av"></div><div class="tx">{"".join(f'<span id="ck{i}">{c}</span>' for i, c in enumerate("PRISM"))}</div><b id="cpost">Post</b></div>
      <div id="flash"></div>
    </div>
    <script>window.PR_T = {json.dumps({k: round(v, 3) for k, v in T.items()})};</script>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/scene.js"></script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
print({k: round(v, 2) for k, v in T.items()})
