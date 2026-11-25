"""AI.NXTLVL "Your first 100 customers" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json.

The 3D stage (assets/js/scene.js) is a pure function of time; this file times it to the voice (plan/words.json, sentence
ids from build/relabel.py) through window.FC_T and lays the type over it on one paused GSAP timeline, on a fixed grid (all
centred): headline band (two lines, white + lavender serif accent), labels glued to the 3D props, the live caption (three
words at a time). Facts: plan/skills_readme.md and plan/skill_first-customers.md (github.com/slavingia/skills, 11k stars
on 2026-11-25). Script similarity to the reference: plan/similarity.json.
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
JS, SFX, HTML = [], [], []
VIOLET, LAV, NIGHT, GOLD = "#7a2ffb", "#b687f9", "#07050f", "#ffc23d"


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


def wt(words, n=0, after=0.0):
    """time of the n-th word (after `after`) starting with any of `words`, across the whole voiceover"""
    words = words if isinstance(words, (list, tuple)) else [words]
    hits = [w for w in W if w["t0"] >= after and any(key(w["w"]).startswith(x) for x in words)]
    if not hits:
        raise SystemExit(f"none of {words} after {after}")
    return hits[min(n, len(hits) - 1)]["t0"]


END = max(w["t1"] for w in W)
DUR = round(END + 1.4, 2)
T = {}
T["eleven"] = wt(["eleven", "11"]); T["stars0"] = T["eleven"] - .25; T["starred"] = wt("starred")
T["job"] = wt("job"); T["hundred"] = wt(["hundred", "100"], after=T["job"])
T["find"] = wt("describe"); T["maps"] = wt("maps"); T["places"] = wt("places")
T["hand"] = wt("hand", after=T["find"]) - .9; T["code"] = wt("code", after=T["find"])
T["friends"] = wt("sell", after=T["code"]); T["community"] = wt("community", after=T["friends"]); T["strangers"] = wt("strangers")
T["email"] = wt("email"); T["grew"] = wt("grew")
T["ten"] = wt(["ten", "10"], after=T["grew"]); T["twothousand"] = wt(["thousand", "2000", "2"], after=T["ten"] + 1.0)
T["launch"] = wt("launch", after=T["ten"]) - .4; T["paid"] = wt("paid")
T["send"] = wt("send", after=T["paid"]); T["cta"] = wt("comment"); T["callkw"] = wt("customers", after=T["cta"]); T["end"] = DUR

HEADS = [("Gumroad's founder", "made a Claude coach.", 0.0), ("11,000 stars.", "One job:", T["eleven"] - .1), ("Your first", "100 customers.", T["hundred"] - .5),
         ("Step 1:", "find your buyers.", T["find"]), ("Step 2:", "do it by hand.", T["hand"] + .5), ("Step 3:", "sell in circles.", T["friends"]),
         ("That's how", "Gumroad grew.", T["grew"] - .45), ("$10 a month", "× 200 = $2,000.", T["ten"] - .1), ("Don't launch", "until 100 pay.", T["launch"] + .2),
         ("Send this", "to a builder.", T["send"]), ("Comment", "CUSTOMERS.", T["cta"])]
for k, (a, b, t0) in enumerate(HEADS):
    t1 = HEADS[k + 1][2] if k + 1 < len(HEADS) else DUR + 1
    HTML.append(f'<div class="hd{" on" if k == 0 else ""}" id="hd{k}"><div class="h1">{a}</div><div class="h2">{b}</div></div>')
    if k:
        js(f'tl.set("#hd{k}", {{opacity: 1}}, {t0:.3f});')
        ft(f"#hd{k} .h1", t0, .35, "{opacity: 0, y: 26}", "{opacity: 1, y: 0}", "back.out(1.8)")
        ft(f"#hd{k} .h2", t0 + .12, .4, "{opacity: 0, y: 26}", "{opacity: 1, y: 0}", "back.out(1.8)")
    if t1 < DUR:
        to(f"#hd{k}", t1 - .14, .14, "{opacity: 0, y: -20, filter: 'blur(6px)'}", "power2.in")
    sfx("whoosh" if k % 2 else "swish", t0 - .12)

# live caption, three words at a time
k = 0
for i in range(0, len(W), 3):
    chunk = W[i:i + 3]
    nxt = W[i + 3]["t0"] if i + 3 < len(W) else chunk[-1]["t1"] + .25
    if nxt - chunk[-1]["t1"] > .6:
        nxt = chunk[-1]["t1"] + .35
    spans = " ".join(f'<span id="cw{k}_{j}">{w["w"]}</span>' for j, w in enumerate(chunk))
    HTML.append(f'<div class="cap" id="cp{k}">{spans}</div>')
    ft(f"#cp{k}", chunk[0]["t0"] - .06, .12, "{opacity: 0}", "{opacity: 1}", "none")
    for j, w in enumerate(chunk):
        ft(f"#cw{k}_{j}", w["t0"] - .04, .12, "{color: 'rgba(255,255,255,.42)'}", "{color: '#ffffff'}", "none")
    to(f"#cp{k}", nxt - .06, .06, "{opacity: 0}", "none")
    k += 1

tc = T["cta"]
ft("#cbox", tc - .05, .45, "{opacity: 0, y: 50, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for i, ch in enumerate("CUSTOMERS"):
    ft(f"#ck{i}", T["callkw"] - .2 + i * .045, .04, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["callkw"] - .2 + i * .045)
ft("#cpost", T["callkw"] + .3, .25, "{color: '#6b6585'}", "{color: '#7a2ffb'}", "power2.out")
for at, op in ((T["hundred"], .3), (T["grew"], .25), (T["paid"] + .4, .4), (T["callkw"] + .4, .3)):
    js(f'tl.set("#flash", {{opacity: {op}}}, {at - .02:.3f});')
    to("#flash", at, .45, "{opacity: 0}", "power2.out")

# sound
for i in range(14):
    sfx("g_pop", .1 + i * .07)
sfx("impact", 1.25)
sfx("sparkle", T["eleven"]); sfx("riser_short", T["hundred"] - .6); sfx("impact", T["hundred"])
sfx("whoosh_big", T["find"] - .2)
for i in range(3):
    sfx("g_pickup", T["places"] + i * .15)
sfx("g_swish", T["maps"]); sfx("buzzer", T["code"]); sfx("msg", T["hand"] + .3)
for x in ("friends", "community", "strangers"):
    sfx("g_tick", T[x])
for i in range(6):
    sfx("msg", T["email"] - .5 + i * .14)
sfx("g_levelup", T["grew"])
for i in range(5):
    sfx("cash", T["ten"] + .1 + i * .25)
sfx("lock", T["launch"] + .2)
for i in range(10):
    sfx("tick", T["launch"] + .3 + i * (T["paid"] - T["launch"]) / 10)
sfx("riser", T["paid"]); sfx("whoosh_big", T["paid"] + .5); sfx("g_complete", T["paid"] + .6)
sfx("whoosh", tc - .1); sfx("impact", T["callkw"] + .45)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: #fff;
  background: radial-gradient(80% 45% at 15% 8%, rgba(127,27,248,.36), rgba(0,0,0,0) 70%), radial-gradient(80% 45% at 85% 95%, rgba(96,8,242,.32), rgba(0,0,0,0) 70%), {NIGHT}; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(100% 62% at 50% 52%, rgba(0,0,0,0) 55%, rgba(3,2,8,.55) 100%); }}
#flash {{ position: absolute; inset: 0; background: {VIOLET}; mix-blend-mode: screen; opacity: 0; pointer-events: none; }}
#bar {{ position: absolute; left: 70px; right: 70px; top: 258px; display: flex; justify-content: space-between; align-items: center;
  font-family: Mono; font-size: 24px; letter-spacing: .16em; color: rgba(255,255,255,.62); }}
#bar img {{ height: 40px; }} #bar b {{ color: {LAV}; }}
.hd {{ position: absolute; left: 40px; right: 40px; top: 330px; text-align: center; opacity: 0; }}
.hd.on {{ opacity: 1; }}
.hd .h1, .hd .h2 {{ opacity: 0; }} .hd.on .h1, .hd.on .h2 {{ opacity: 1; }}
.h1 {{ font-size: 80px; line-height: 1.0; letter-spacing: -.035em; text-shadow: 0 6px 30px rgba(0,0,0,.7); white-space: nowrap; }}
.h2 {{ font-family: Serif; font-style: italic; font-weight: 400; font-size: 96px; line-height: 1.02; color: {LAV}; text-shadow: 0 0 40px rgba(122,47,251,.5); white-space: nowrap; }}
.cap {{ position: absolute; left: 60px; right: 60px; top: 1470px; text-align: center; font-family: Inter; font-weight: 700; font-size: 46px; opacity: 0;
  color: rgba(255,255,255,.42); text-shadow: 0 3px 12px rgba(0,0,0,.8); }}
.lbl {{ position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap; text-align: center; }}
.pill {{ font-family: Mono; font-size: 26px; letter-spacing: .06em; padding: 9px 18px; border-radius: 12px; background: rgba(20,12,40,.85); border: 2px solid rgba(182,135,249,.65); }}
#starBox b {{ font-size: 92px; letter-spacing: -.04em; color: {GOLD}; text-shadow: 0 0 30px rgba(255,194,61,.5); }}
#starBox span {{ display: block; font-family: Inter; font-weight: 700; font-size: 28px; color: rgba(255,255,255,.75); }}
#zero {{ font-family: Mono; font-size: 34px; color: #ff6b85; }}
#dm {{ font-family: Inter; font-weight: 700; font-size: 22px; line-height: 1.3; padding: 12px 14px; border-radius: 16px 16px 16px 4px; background: #4dabf7; width: 230px; white-space: normal; text-align: left; }}
#gumroadTag {{ font-family: Inter; font-weight: 700; font-size: 30px; padding: 10px 20px; border-radius: 999px; background: rgba(255,194,61,.16); border: 2px solid {GOLD}; color: {GOLD}; }}
#math {{ font-family: Mono; }}
#math .row {{ font-size: 40px; color: rgba(255,255,255,.85); }}
#math b {{ display: block; font-family: Mont; font-size: 120px; letter-spacing: -.05em; color: {GOLD}; text-shadow: 0 0 40px rgba(255,194,61,.5); line-height: 1; }}
#math span {{ font-family: Inter; font-weight: 700; font-size: 30px; color: rgba(255,255,255,.75); }}
#lock, #go {{ font-family: Mono; font-size: 30px; padding: 10px 20px; border-radius: 14px; }}
#lock {{ background: rgba(40,8,18,.85); border: 2px solid #ff6b85; color: #ff8aa0; }}
#go {{ background: rgba(8,40,20,.85); border: 2px solid #69db7c; color: #69db7c; }}
#paidBox b {{ font-size: 80px; letter-spacing: -.04em; color: {GOLD}; }}
#paidBox span {{ display: block; font-family: Inter; font-weight: 700; font-size: 26px; color: rgba(255,255,255,.75); }}
#cbox {{ position: absolute; left: 90px; right: 90px; top: 1300px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 38px 0 26px; background: rgba(248,246,255,.97); color: {NIGHT}; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(122,47,251,.7); }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: conic-gradient(#ff6b6b, #ffd43b, #69db7c, #4dabf7, #da77f2, #ff6b6b); flex: none; }}
#cbox .tx {{ flex: 1; font-size: 52px; letter-spacing: .03em; }} #cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #6b6585; }}
"""
labels = f"""
      <div class="lbl" id="starBox"><b id="starN">0</b><span>stars on GitHub</span></div>
      <div class="lbl pill" id="repo">slavingia / skills</div>
      <div class="lbl pill" id="isl0">forums</div><div class="lbl pill" id="isl1">Discord groups</div><div class="lbl pill" id="isl2">subreddits</div>
      <div class="lbl" id="zero">0 lines of code</div>
      <div class="lbl" id="dm">Hi! Want me to make your first one by hand?</div>
      <div class="lbl pill" id="rg0">friends &amp; family</div><div class="lbl pill" id="rg1">your community</div><div class="lbl pill" id="rg2">strangers</div>
      <div class="lbl" id="gumroadTag">one personal email at a time</div>
      <div class="lbl" id="math"><div class="row">$10/mo &#215; 200 customers</div><b id="mrr">$0</b><span>a month</span></div>
      <div class="lbl" id="lock">LAUNCH LOCKED</div><div class="lbl" id="go">LAUNCH</div>
      <div class="lbl" id="paidBox"><b id="paidN">0</b><span>/ 100 paid</span></div>
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI.NXTLVL First 100 customers 9x16</title>
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
      <div id="cbox"><div class="av"></div><div class="tx">{"".join(f'<span id="ck{i}">{c}</span>' for i, c in enumerate("CUSTOMERS"))}</div><b id="cpost">Post</b></div>
      <div id="flash"></div>
    </div>
    <script>window.FC_T = {json.dumps({k: round(v, 3) for k, v in T.items()})};</script>
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
