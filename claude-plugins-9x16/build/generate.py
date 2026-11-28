"""NXTLVLSOCIAL.AI "5 free Claude Code plugins" v2 (9:16): writes index.html, plan/sfx_events.json and plan/edit.json.

v2 (owner: "make it 3D, add more motion graphics, better SFX and voiceover for better understanding"): the browser window
is a 3D slab on a receding grid floor (assets/js/scene.js) holding our own captures of each plugin's page; it flips
between plugins and pushes in onto the proof line, where a violet selection frame lands. Desk props animate each claim
(code bar and coins shrink, slop blobs snap into tiles, reviewer orbs scan a plan, a globe with platform tiles, a codebase
scan). Voice: Kokoro af_heart (clear, natural; build/vo_kok.py), a plainer script. v1 kept as build/generate_v1.py.
Reference: refs/ref_34964.mp4 (its look only, rebuilt from our material; facts in caption.md).
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
TG = json.load(open(os.path.join(ROOT, "plan", "targets.json")))
JS, SFX, HTML = [], [], []
INK, VIOLET, ORCHID, PAPER = "#140a2e", "#6516c7", "#a75bfc", "#f4f2f8"


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {max(0, t):.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {max(0, t):.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {max(0, t):.3f});')


def key(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def wt(words, n=0, after=0.0):
    words = words if isinstance(words, (list, tuple)) else [words]
    hits = [w for w in W if w["t0"] >= after and any(key(w["w"]).startswith(x) for x in words)]
    if not hits:
        raise SystemExit(f"none of {words} after {after}")
    return hits[min(n, len(hits) - 1)]["t0"]


END = max(w["t1"] for w in W)
DUR = round(END + 1.6, 2)
T = {}
T["b1"] = wt("number"); T["b2"] = wt("number", after=T["b1"] + 1); T["b3"] = wt("number", after=T["b2"] + 1)
T["b4"] = wt("number", after=T["b3"] + 1); T["b5"] = wt("number", after=T["b4"] + 1); T["b6"] = wt("send"); T["b7"] = wt("comment")
T["stars"] = wt(["200", "two"]); T["tests"] = wt("tests"); T["half"] = wt("half"); T["quarter"] = wt("quarter"); T["same"] = wt("same", after=T["quarter"])
T["purple"] = wt("purple"); T["designed"] = wt("designed"); T["fresh"] = wt("fresh"); T["google2"] = wt("google", after=T["fresh"])
T["thousands"] = wt("thousands"); T["read"] = wt("read", after=T["b4"]); T["never"] = wt("never"); T["scans"] = wt("scans")
T["hooks"] = wt("hooks"); T["zero"] = wt("zero"); T["kw"] = wt("plugins", after=T["b7"])

# ------------------------------------------------------------------ the 3D window's page sequence (scene.js)
SHOTS = {
    "pony_top": ("ponytail_top", 2200, 2000, "github.com/DietrichGebert/ponytail"),
    "pony_stars": ("t_pony_stars", 2200, 2600, "github.com/DietrichGebert/ponytail"),
    "pony_bench": ("t_pony_bench", 2200, 2600, "github.com/DietrichGebert/ponytail"),
    "unslop_top": ("unslop_top", 2200, 2000, "github.com/heydamir/unslop"),
    "unslop_slop": ("t_unslop_slop", 2200, 2600, "github.com/heydamir/unslop"),
    "egm_hero": ("t_egm_hero", 2200, 2600, "egm.dev"),
    "google": ("t_google", 2200, 2600, "opensource.googleblog.com"),
    "reach_top": ("agentreach_top", 2200, 2000, "github.com/Panniantong/Agent-Reach"),
    "reach_about": ("t_reach_about", 2200, 2600, "github.com/Panniantong/Agent-Reach"),
    "reach_ro": ("t_reach_ro", 2200, 2600, "github.com/Panniantong/Agent-Reach"),
    "setup_top": ("setup_top", 2200, 2000, "github.com/anthropics/claude-plugins-official"),
    "setup": ("t_setup", 2200, 2600, "github.com/anthropics/claude-plugins-official"),
}
SEQ = [("pony_stars", 0.0, "t_pony_stars"), ("pony_top", T["b1"], None), ("pony_bench", T["tests"] - .2, "t_pony_bench"),
       ("unslop_top", T["b2"], None), ("unslop_slop", T["purple"] - .3, "t_unslop_slop"),
       ("egm_hero", T["b3"], "t_egm_hero"), ("google", T["google2"] - .25, "t_google"),
       ("reach_top", T["b4"], None), ("reach_about", T["read"] - .3, "t_reach_about"), ("reach_ro", T["never"] - .35, "t_reach_ro"),
       ("setup_top", T["b5"], None), ("setup", T["scans"] - .3, "t_setup")]
BEATS = {round(T[b], 3) for b in ("b1", "b2", "b3", "b4", "b5")}
seq = []
for shot, t0, box in SEQ:
    f, w, h, url = SHOTS[shot]
    d = {"src": f"assets/img/shots/{f}.png", "w": w, "h": h, "url": url, "t0": round(t0, 3), "flip": round(t0, 3) in BEATS}
    if box:
        b = TG[box]; d["box"] = {k: round(b[k], 1) for k in ("x", "y", "w", "h")}
    seq.append(d)
CARO = [1, 3, 5, 7, 10]       # the five plugins' pages for the share carousel
for d in seq:
    if d["flip"] or d is seq[0]:
        sfx("flip", d["t0"] - .2) if d["flip"] else None
    else:
        sfx("swish", d["t0"])
    if "box" in d:
        on = .25 if d is seq[0] else d["t0"] + 1.1
        sfx("scan" if d is not seq[0] else "click", on - .05); sfx("click", on + .05)

# ------------------------------------------------------------------ headline band (line + violet chip), counter, source
HEADS = [("5 Claude Code plugins", "all free", 0.0, "00", "SOURCE: GITHUB, 28 NOV 2026"),
         ("01  Ponytail", "half the code", T["b1"], "01", "SOURCE: PONYTAIL'S OWN BENCHMARK (585 RUNS)"),
         ("02  Unslop", "no more AI slop", T["b2"], "02", "SOURCE: GITHUB.COM/HEYDAMIR/UNSLOP"),
         ("03  Elephant-Goldfish", "open-sourced by Google", T["b3"], "03", "SOURCE: EGM.DEV, GOOGLE OPEN SOURCE BLOG"),
         ("04  Agent Reach", "read-only web access", T["b4"], "04", "SOURCE: AGENT REACH README"),
         ("05  Claude Code Setup", "official, from Anthropic", T["b5"], "05", "SOURCE: ANTHROPIC'S PLUGIN README"),
         ("Send this", "to that friend", T["b6"], "05", ""), ("Comment", "PLUGINS", T["b7"], "05", "")]
for k, (a, b, t0, n, src) in enumerate(HEADS):
    t1 = HEADS[k + 1][2] if k + 1 < len(HEADS) else DUR + 1
    HTML.append(f'<div class="hd{" on" if k == 0 else ""}" id="hd{k}"><div class="h1">{a}</div><div class="h2"><span>{b}</span></div></div>')
    if src:
        HTML.append(f'<div class="src" id="src{k}">{src}</div>')
        ft(f"#src{k}", t0 + .5, .4, "{opacity: 0}", "{opacity: 1}", "none")
        to(f"#src{k}", t1 - .2, .2, "{opacity: 0}", "none")
    if k:
        js(f'tl.set("#hd{k}", {{opacity: 1}}, {t0 - .05:.3f});')
        ft(f"#hd{k} .h1", t0 - .05, .4, "{opacity: 0, y: 30, rotationX: -60}", "{opacity: 1, y: 0, rotationX: 0}", "back.out(1.7)")
        ft(f"#hd{k} .h2 span", t0 + .12, .38, "{opacity: 0, scale: .6, rotation: -4}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(2.2)")
        js(f'tl.call(() => {{ document.querySelector("#cnt b").textContent = "{n}"; }}, null, {t0:.3f});')
    if t1 < DUR:
        to(f"#hd{k}", t1 - .14, .14, "{opacity: 0, y: -18}", "power2.in")
for b in ("b1", "b2", "b3", "b4", "b5"):     # each new plugin: a reverse swell into a low hit on the number
    sfx("revbass", T[b] - 1.25); sfx("bass", T[b])
sfx("whoosh", T["b6"] - .1); sfx("whoosh", T["b7"] - .1)

# ------------------------------------------------------------------ labels riding on the 3D props (scene.js positions them)
LBL = [("lbl0", '<b id="starN">0</b> stars', True), ("lbl1a", "-53% code", True), ("lbl1b", "-26% cost", True), ("lbl1c", "same accuracy", False),
       ("lbl2a", "purple gradients, emoji labels", False), ("lbl2b", "designed", True), ("lbl3a", "fresh reviewers", False),
       ("lbl3b", "used daily at Google", True), ("lbl4", "reads only, never posts", True), ("lbl5", "official Anthropic plugin", True)]
for i, (lid, txt, dark) in enumerate(LBL):
    HTML.append(f'<div class="lbl{" dark" if dark else ""}" id="{lid}">{txt}</div>')
for i, n in enumerate(("Ponytail", "Unslop", "Elephant-Goldfish", "Agent Reach", "Claude Code Setup")):
    HTML.append(f'<div class="lbl cn" id="cn{i}">{n}</div>')
js(f'const SN = {{v: 0}}; tl.to(SN, {{v: 200000, duration: .9, ease: "power2.out", onUpdate: () => {{ document.getElementById("starN").textContent = Math.round(SN.v).toLocaleString("en-US"); }}}}, {T["stars"]:.3f});')
sfx("shimmer", T["stars"] - .05); sfx("upgrade", T["stars"] + .7)
sfx("pop", T["half"]); sfx("thump", T["half"] + .3)
for i in range(3):
    sfx("coin", T["quarter"] + i * .12)
sfx("chime", T["same"])
for i in range(4):
    sfx("pop", T["b2"] + .3 + i * .08)
sfx("whoosh_soft", T["designed"] - .9); sfx("shimmer_soft", T["designed"] - .5); sfx("chime", T["designed"] - .2)
for i in range(3):
    sfx("beep_soft", T["fresh"] + i * .12); sfx("click", T["fresh"] + .75 + i * .2)
sfx("upgrade", T["thousands"])
for i in range(3):
    sfx("pop", T["read"] + i * .25)
sfx("notify", T["never"])
sfx("scan", T["scans"] - .05); sfx("scan", T["scans"] + .6)
for i in range(3):
    sfx("pop", T["hooks"] - .05 + i * .3)
for i in range(5):
    sfx("pop", T["b6"] + .2 + i * .08)

# ------------------------------------------------------------------ live caption: up to three words, each pops in as spoken
EMPH = {"200,000": VIOLET, "Ponytail.": VIOLET, "Unslop.": VIOLET, "Elephant-Goldfish,": VIOLET, "Reach.": VIOLET, "Setup,": VIOLET, "PLUGINS,": VIOLET,
        "half": VIOLET, "quarter": VIOLET, "Google.": VIOLET, "never": VIOLET, "posts.": VIOLET, "thousands": VIOLET}
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
    st(f"#cp{k}", g[0]["t0"] - .08, "{opacity: 1}")
    for j, w in enumerate(g):
        ft(f"#cw{k}_{j}", w["t0"] - .07, .22, "{opacity: 0, scale: .6, y: 18}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.5)")
        col = EMPH.get(w["w"], INK)
        st(f"#cw{k}_{j}", w["t0"] - .02, f'{{backgroundColor: "{VIOLET}", color: "#ffffff"}}')
        end = g[j + 1]["t0"] - .02 if j + 1 < len(g) else nxt - .08
        st(f"#cw{k}_{j}", end, f'{{backgroundColor: "rgba(101,22,199,0)", color: "{col}"}}')
    to(f"#cp{k}", nxt - .08, .08, "{opacity: 0}", "none")

# ------------------------------------------------------------------ CTA: the comment box
tc = T["b7"]
ft("#cbox", tc - .05, .45, "{opacity: 0, y: 50, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
for i, ch in enumerate("PLUGINS"):
    ft(f"#ck{i}", T["kw"] - .15 + i * .05, .04, "{opacity: 0}", "{opacity: 1}", "none")
    sfx("click", T["kw"] - .15 + i * .05)
ft("#cpost", T["kw"] + .3, .25, "{color: '#8a8299'}", f"{{color: '{VIOLET}'}}", "power2.out")
ft("#endmark", T["kw"] + .3, .5, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "back.out(1.6)")
sfx("impact_soft", T["kw"] + .45); sfx("shimmer_soft", T["kw"] + .5)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {PAPER}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: {INK}; background: {PAPER}; }}
#gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
#topfade {{ position: absolute; left: 0; right: 0; top: 0; height: 520px; background: linear-gradient({PAPER} 70%, rgba(244,242,248,0)); }}
#bar {{ position: absolute; left: 64px; right: 64px; top: 252px; display: flex; justify-content: space-between; align-items: center; }}
#brand {{ display: flex; align-items: center; gap: 14px; font-family: Mono; font-size: 24px; letter-spacing: .14em; color: {INK}; }}
#brand i {{ width: 46px; height: 46px; border-radius: 13px; background: {INK}; display: grid; place-items: center; }}
#brand i img {{ width: 34px; height: 34px; }}
#cnt {{ font-family: Mono; font-size: 24px; letter-spacing: .14em; color: rgba(20,10,46,.55); }} #cnt b {{ color: {VIOLET}; }}
.hd {{ position: absolute; left: 40px; right: 40px; top: 318px; text-align: center; opacity: 0; perspective: 900px; }}
.hd.on {{ opacity: 1; }} .hd .h1, .hd .h2 span {{ opacity: 0; }} .hd.on .h1, .hd.on .h2 span {{ opacity: 1; }}
.h1 {{ font-size: 62px; line-height: 1.08; letter-spacing: -.035em; white-space: nowrap; transform-origin: 50% 100%; }}
.h2 {{ margin-top: 8px; }}
.h2 span {{ display: inline-block; font-size: 50px; letter-spacing: -.02em; line-height: 1.15; padding: 4px 22px 8px; border-radius: 14px; background: {VIOLET}; color: #fff; white-space: nowrap; }}
.src {{ position: absolute; left: 0; right: 0; top: 500px; text-align: center; font-family: Mono; font-size: 19px; letter-spacing: .12em; color: rgba(20,10,46,.66); opacity: 0; }}
.lbl {{ position: absolute; left: 0; top: 0; opacity: 0; white-space: nowrap; font-family: Inter; font-weight: 700; font-size: 34px; padding: 10px 22px; border-radius: 16px;
  background: #fff; color: {INK}; box-shadow: 0 10px 26px rgba(40,20,90,.16), 0 0 0 2px rgba(101,22,199,.2); }}
.lbl.dark {{ background: {INK}; color: #fff; box-shadow: 0 10px 26px rgba(40,20,90,.25); }}
.lbl b {{ font-variant-numeric: tabular-nums; }}
.lbl.cn {{ font-size: 26px; padding: 6px 14px; background: {VIOLET}; color: #fff; }}
.cap {{ position: absolute; left: 50px; right: 50px; top: 1440px; text-align: center; font-family: Inter; font-weight: 700; font-size: 56px; opacity: 0; letter-spacing: -.01em; line-height: 1.2; color: {INK}; }}
.cw {{ display: inline-block; padding: 2px 12px; margin: 0 2px; border-radius: 14px; opacity: 0; transform-origin: 50% 80%; }}
#cbox {{ position: absolute; left: 90px; right: 90px; top: 640px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 38px 0 26px; background: #fff; color: {INK}; box-shadow: 0 30px 80px rgba(40,20,90,.22), 0 0 0 3px {VIOLET}; }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: {INK}; display: grid; place-items: center; flex: none; }} #cbox .av img {{ width: 54px; }}
#cbox .tx {{ flex: 1; font-size: 54px; letter-spacing: .03em; }} #cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #8a8299; }}
#endmark {{ position: absolute; left: 0; right: 0; top: 820px; text-align: center; font-family: Mono; font-size: 30px; letter-spacing: .18em; color: rgba(20,10,46,.7); opacity: 0; }}
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>NXTLVL 5 Claude Code plugins 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920" data-layout-allow-overflow></canvas>
      <div id="topfade"></div>
      <div id="bar"><div id="brand"><i><img src="assets/img/logo-mark.svg" alt=""></i>NXTLVLSOCIAL.AI</div><div id="cnt"><b>00</b> / 05</div></div>
      {chr(10).join(HTML)}
      <div id="cbox"><div class="av"><img src="assets/img/logo-mark.svg" alt=""></div><div class="tx">{"".join(f'<span id="ck{i}">{c}</span>' for i, c in enumerate("PLUGINS"))}</div><b id="cpost">Post</b></div>
      <div id="endmark">ALL FIVE LINKS IN YOUR DMS</div>
    </div>
    <script>window.PL = {json.dumps({"T": {k: round(v, 3) for k, v in T.items()}, "seq": seq, "caro": CARO})};</script>
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
