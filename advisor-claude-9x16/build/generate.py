"""AI.NXTLVL "The advisor strategy" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json.

Rebuilt from a reference reel (a talking head on Claude Code's advisor setup, "comment Claude") with a new script, our
own 3D cast (assets/js/scene.js: Nyx the small model, the Advisor star for Opus) and word-by-word captions. The 3D stage
is a pure function of time; this file times it to the voice (plan/words.json, sentence ids from build/relabel.py) through
window.AD_T and lays the type over it on one paused GSAP timeline, on a fixed grid (all centred): headline band, labels
glued to the 3D props, the live caption (each word pops in as it is spoken, the spoken word on a violet chip).
Facts: claude.com/blog/the-advisor-strategy (2026-04-09) and code.claude.com/docs/en/advisor, read 2026-11-26.
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
VIOLET, LAV, NIGHT, GOLD, GREEN = "#7a2ffb", "#b687f9", "#07050f", "#ffc23d", "#3ddc84"


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
DUR = round(END + 1.8, 2)
T = {}
T["scored"] = wt("scored"); T["give"] = wt("give"); T["jumps"] = wt("jumps"); T["same"] = wt("same"); T["ask"] = wt("ask")
T["trick"] = wt("heres"); T["writes"] = wt("writes"); T["runs"] = wt("runs"); T["reads"] = wt("reads")
T["big"] = wt("big", after=T["reads"]); T["keyboard"] = wt("keyboard"); T["plan"] = wt("before", after=T["keyboard"])
T["error"] = wt("error"); T["done"] = wt("done", after=T["error"]); T["strategy"] = wt("anthropic") - .35
T["claude"] = wt("claude"); T["command"] = wt("command"); T["slash"] = wt(["advisor", "slash"], after=T["command"])
T["opus"] = wt("opus", after=T["slash"]); T["tests"] = wt("tests") - .55; T["higher"] = wt("higher"); T["cost"] = wt("cost", after=T["higher"])
T["less"] = wt("less"); T["send"] = wt("send"); T["everything"] = wt("everything"); T["cta"] = wt("comment")
T["kw"] = wt("advisor", after=T["cta"]); T["setup"] = wt("setup"); T["end"] = DUR

# ------------------------------------------------------------------ headline band (two lines: white + lavender serif accent)
HEADS = [("The cheapest model", "scored 19.7%.", 0.0), ("Give it", "an advisor.", T["give"] - .1), ("Same cheap model.", "It asks for help.", T["same"] - .1),
         ("The small model", "does the work.", T["trick"] - .1), ("The big model", "never types.", T["big"] - .1), ("It only steps in", "at the hard parts.", T["plan"] - .35),
         ("Anthropic's", "advisor strategy.", T["strategy"]), ("One command.", "/advisor opus", T["command"] - .1), ("Anthropic's tests:", "better and cheaper.", T["tests"]),
         ("Send this", "to that friend.", T["send"] - .1), ("Comment", "ADVISOR.", T["cta"] - .1)]
for k, (a, b, t0) in enumerate(HEADS):
    t1 = HEADS[k + 1][2] if k + 1 < len(HEADS) else DUR + 1
    mono = ' style="font-family: Mono; font-style: normal; font-size: 74px; color: #b687f9"' if b.startswith("/") else ""
    HTML.append(f'<div class="hd{" on" if k == 0 else ""}" id="hd{k}"><div class="h1">{a}</div><div class="h2"{mono}>{b}</div></div>')
    if k:
        js(f'tl.set("#hd{k}", {{opacity: 1}}, {t0:.3f});')
        ft(f"#hd{k} .h1", t0, .35, "{opacity: 0, y: 30, rotationX: -50}", "{opacity: 1, y: 0, rotationX: 0}", "back.out(1.7)")
        ft(f"#hd{k} .h2", t0 + .1, .4, "{opacity: 0, y: 30, rotationX: -50}", "{opacity: 1, y: 0, rotationX: 0}", "back.out(1.7)")
        sfx("swish", t0 - .3)          # before the line starts, never on its first word
    if t1 < DUR:
        to(f"#hd{k}", t1 - .14, .14, "{opacity: 0, y: -24}", "power2.in")

# ------------------------------------------------------------------ live caption: up to three words, each pops in as spoken
EMPH = {"19.7%": GOLD, "41.2%": GOLD, "11.9%": GOLD, "advisor": LAV, "advisor,": LAV, "advisor.": LAV, "opus.": LAV, "opus": LAV, "opus,": LAV,
        "help.": LAV, "keyboard.": LAV, "hard": LAV, "parts:": LAV, "higher,": GREEN, "less": GREEN, "advisor": LAV, "ADVISOR,": GOLD}
groups, cur = [], []
for w in W:
    if cur and (len(cur) == 3 or cur[-1]["line"] != w["line"] or cur[-1]["w"][-1:] in ".:?," or w["t0"] - cur[-1]["t1"] > .35):
        groups.append(cur); cur = []
    cur.append(w)
groups.append(cur)
for k, g in enumerate(groups):
    nxt = groups[k + 1][0]["t0"] if k + 1 < len(groups) else g[-1]["t1"] + .4
    nxt = min(nxt, g[-1]["t1"] + .5)
    spans = "".join(f'<span class="cw" id="cw{k}_{j}"{" style=" + chr(34) + "color:" + EMPH[w["w"]] + chr(34) if w["w"] in EMPH else ""}>{w["w"]}</span>' for j, w in enumerate(g))
    HTML.append(f'<div class="cap" id="cp{k}">{spans}</div>')
    js(f'tl.set("#cp{k}", {{opacity: 1}}, {g[0]["t0"] - .08:.3f});')
    for j, w in enumerate(g):
        ft(f"#cw{k}_{j}", w["t0"] - .07, .24, "{opacity: 0, scale: .55, y: 22}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.6)")
        col = EMPH.get(w["w"], "#ffffff")                    # the spoken word sits on a white chip in dark type
        js(f'tl.set("#cw{k}_{j}", {{backgroundColor: "#ffffff", color: "#140a2e", textShadow: "none"}}, {w["t0"] - .02:.3f});')
        end = g[j + 1]["t0"] - .02 if j + 1 < len(g) else nxt - .08
        js(f'tl.set("#cw{k}_{j}", {{backgroundColor: "rgba(255,255,255,0)", color: "{col}", textShadow: "0 3px 14px rgba(0,0,0,.85)"}}, {end:.3f});')
    to(f"#cp{k}", nxt - .08, .08, "{opacity: 0}", "none")

# ------------------------------------------------------------------ terminal typing, CTA box, flashes
for i, ch in enumerate("/advisor opus"):
    ft(f"#tk{i}", T["slash"] - .15 + i * .05, .03, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["slash"] - .15 + i * .05)
ft("#tline3", T["opus"] + .45, .25, "{opacity: 0, x: -14}", "{opacity: 1, x: 0}")
tc = T["cta"]
ft("#cbox", tc - .05, .45, "{opacity: 0, y: 50, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for i, ch in enumerate("ADVISOR"):
    ft(f"#ck{i}", T["kw"] - .15 + i * .05, .04, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["kw"] - .15 + i * .05)
ft("#cpost", T["kw"] + .3, .25, "{color: '#6b6585'}", "{color: '#7a2ffb'}", "power2.out")
for at, op in ((T["jumps"], .28), (T["higher"], .18), (T["kw"] + .4, .22)):
    js(f'tl.set("#flash", {{opacity: {op}}}, {at - .02:.3f});')
    to("#flash", at, .45, "{opacity: 0}", "power2.out")

# ------------------------------------------------------------------ sound (build/sfx_mix.py turns these into the mix)
sfx("whoosh_big", 0.0); sfx("pop", T["scored"]); sfx("riser", T["give"] - .7); sfx("whoosh_big", T["give"]); sfx("wake", T["give"] + .3)
sfx("impact", T["jumps"]); sfx("upgrade", T["jumps"] + .1)
sfx("beep", T["ask"] - .1); sfx("chime_short", T["ask"] + .2)   # done before "Here's the trick"
sfx("typing", T["writes"] - .1); sfx("pop", T["runs"]); sfx("notify", T["runs"] + .55); sfx("pop", T["reads"]); sfx("swish", T["reads"] + .1)
sfx("typing_soft", T["big"]); sfx("thump", T["keyboard"])
for x in ("plan", "error", "done"):
    sfx("chime", T[x] + .2); sfx("beep_soft", T[x] - .05)
sfx("whoosh_big", T["strategy"]); sfx("notify", T["opus"] + .45)
sfx("pop", T["tests"] + .1); sfx("upgrade", T["higher"]); sfx("coin", T["cost"]); sfx("coin", T["less"])
sfx("swish", T["send"] + .2); sfx("whoosh", T["send"] + .35)
sfx("whoosh", tc - .1); sfx("impact_soft", T["kw"] + .45)

# ------------------------------------------------------------------ page
CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: #fff;
  background: radial-gradient(80% 45% at 15% 8%, rgba(127,27,248,.34), rgba(0,0,0,0) 70%), radial-gradient(80% 45% at 85% 95%, rgba(96,8,242,.3), rgba(0,0,0,0) 70%), {NIGHT}; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(100% 62% at 50% 52%, rgba(0,0,0,0) 55%, rgba(3,2,8,.55) 100%); }}
#flash {{ position: absolute; inset: 0; background: {VIOLET}; mix-blend-mode: screen; opacity: 0; pointer-events: none; }}
#bar {{ position: absolute; left: 70px; right: 70px; top: 258px; display: flex; justify-content: space-between; align-items: center;
  font-family: Mono; font-size: 24px; letter-spacing: .16em; color: rgba(255,255,255,.62); }}
#bar img {{ height: 40px; }} #bar b {{ color: {LAV}; }}
.hd {{ position: absolute; left: 40px; right: 40px; top: 330px; text-align: center; opacity: 0; perspective: 800px; }}
.hd.on {{ opacity: 1; }}
.hd .h1, .hd .h2 {{ opacity: 0; transform-origin: 50% 100%; }} .hd.on .h1, .hd.on .h2 {{ opacity: 1; }}
.h1 {{ font-size: 78px; line-height: 1.02; letter-spacing: -.035em; text-shadow: 0 6px 30px rgba(0,0,0,.7); white-space: nowrap; }}
.h2 {{ font-family: Serif; font-style: italic; font-weight: 400; font-size: 96px; line-height: 1.04; color: {LAV}; text-shadow: 0 4px 24px rgba(0,0,0,.6); white-space: nowrap; }}
.cap {{ position: absolute; left: 60px; right: 60px; top: 1440px; text-align: center; font-family: Inter; font-weight: 700; font-size: 58px; opacity: 0;
  letter-spacing: -.01em; line-height: 1.2; text-shadow: 0 3px 14px rgba(0,0,0,.85); }}
.cw {{ display: inline-block; padding: 2px 12px; margin: 0 2px; border-radius: 14px; opacity: 0; transform-origin: 50% 80%; }}
.lbl {{ position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap; text-align: center; }}
.pill {{ font-family: Mono; font-size: 28px; letter-spacing: .06em; padding: 9px 18px; border-radius: 12px; background: rgba(20,12,40,.88); border: 2px solid rgba(182,135,249,.65); }}
.pct b {{ display: block; font-size: 86px; letter-spacing: -.04em; line-height: 1; }}
.pct span {{ display: block; font-family: Inter; font-weight: 700; font-size: 30px; color: rgba(255,255,255,.8); margin-top: 6px; }}
#lblA b {{ color: rgba(255,255,255,.8); }} #lblB b {{ color: {GOLD}; }}
#bar .rt {{ position: relative; display: block; width: 520px; height: 34px; text-align: right; }}
#bar .rt > span {{ position: absolute; right: 0; top: 0; white-space: nowrap; }}
.src {{ font-family: Mono; font-size: 22px; letter-spacing: .1em; color: rgba(255,255,255,.62); opacity: 0; }}
#advTag {{ border-color: {GOLD}; color: {GOLD}; }}
#qmark {{ width: 96px; height: 96px; border-radius: 30px 30px 30px 6px; background: #fff; color: {VIOLET}; font-size: 66px; line-height: 96px; }}
#noKeys {{ font-family: Mono; font-size: 26px; padding: 9px 18px; border-radius: 12px; background: rgba(40,8,18,.88); border: 2px solid #ff6b85; color: #ff9aae; }}
.gate {{ font-family: Inter; font-weight: 700; font-size: 30px; padding: 8px 16px; border-radius: 999px; background: rgba(20,12,40,.9); border: 2px solid {LAV}; }}
#termTx {{ width: 700px; text-align: left; font-family: Mono; font-size: 38px; line-height: 1.65; }}
#termTx .dim {{ color: rgba(255,255,255,.5); font-size: 30px; }}
#termTx .tk {{ opacity: 0; color: #fff; }} #termTx .pr {{ color: {LAV}; }}
#tline3 {{ opacity: 0; color: {GREEN}; font-size: 28px; }}
.tst b {{ display: block; font-size: 64px; letter-spacing: -.03em; line-height: 1; }}
.tst span {{ display: block; font-family: Inter; font-weight: 700; font-size: 30px; color: rgba(255,255,255,.82); margin-top: 6px; }}
#tB b {{ color: {GREEN}; }} #tB i {{ display: block; font-style: normal; font-family: Mono; font-size: 30px; color: {GOLD}; margin-top: 8px; }}
#cbox {{ position: absolute; left: 90px; right: 90px; top: 600px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 38px 0 26px; background: rgba(248,246,255,.97); color: {NIGHT}; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(122,47,251,.7); }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: conic-gradient(#ff6b6b, #ffd43b, #69db7c, #4dabf7, #da77f2, #ff6b6b); flex: none; }}
#cbox .tx {{ flex: 1; font-size: 54px; letter-spacing: .03em; }} #cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #6b6585; }}
"""
term = ('<div class="dim">Claude Code</div><div><span class="pr">&gt; </span>' + "".join(f'<span class="tk" id="tk{i}">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate("/advisor opus"))
        + '</div><div id="tline3">saved to settings: "advisorModel": "opus"</div>')
labels = f"""
      <div class="lbl pill" id="nyxTag">HAIKU</div>
      <div class="lbl pill" id="advTag">OPUS · ADVISOR</div>
      <div class="lbl" id="qmark">?</div>
      <div class="lbl pct" id="lblA"><b id="pA">0%</b><span>Haiku alone</span></div>
      <div class="lbl pct" id="lblB"><b id="pB">0%</b><span>+ Opus advisor</span></div>
      <div class="lbl pill" id="p0">writes the code</div><div class="lbl pill" id="p1">runs it</div><div class="lbl pill" id="p2">reads the files</div>
      <div class="lbl gate" id="g0">before the plan</div><div class="lbl gate" id="g1">same error again</div><div class="lbl gate" id="g2">before it's done</div>
      <div class="lbl" id="termTx">{term}</div>
      <div class="lbl tst" id="tA"><b>Sonnet</b><span>alone</span></div>
      <div class="lbl tst" id="tB"><b>+2.7 pts</b><span>with an Opus advisor</span><i><span id="costB">-0%</span> cost per task</i></div>
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI.NXTLVL Advisor strategy 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920" data-layout-allow-overflow></canvas>
      <div id="vig"></div>
      {labels}
      <div id="bar"><img src="assets/img/logo-wordmark.png" alt=""><span class="rt"><span id="barTag"><b>AI</b> TOOLS</span><span class="src" id="srcA">SOURCE: ANTHROPIC, BROWSECOMP</span><span class="src" id="srcB">SOURCE: ANTHROPIC, SWE-BENCH</span></span></div>
      {chr(10).join(HTML)}
      <div id="cbox"><div class="av"></div><div class="tx">{"".join(f'<span id="ck{i}">{c}</span>' for i, c in enumerate("ADVISOR"))}</div><b id="cpost">Post</b></div>
      <div id="flash"></div>
    </div>
    <script>window.AD_T = {json.dumps({k: round(v, 3) for k, v in T.items()})};</script>
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
json.dump({"dur": DUR}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {len(groups)} caption groups")
print({k: round(v, 2) for k, v in T.items()})
