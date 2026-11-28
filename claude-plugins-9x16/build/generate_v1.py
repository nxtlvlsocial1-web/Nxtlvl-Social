"""NXTLVLSOCIAL.AI "5 free Claude Code plugins" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json.

Recreated from a reference reel (refs/ref_34964.mp4: a creator's talking head over GitHub screenshots, "comment Claude") in
its look, rebuilt from our own material: a light grid-paper page, browser-window cards holding our fresh captures of each
plugin's public page (build/capture.cjs, build/capture_targets.cjs), a zoom onto the sentence that proves the line with a
violet selection frame and handles, fact chips under the card, word-by-word captions. No face, footage or audio from the
reference. Every claim is checked against the plugin's own README / site (caption.md, "Facts used").
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
T["b1"] = wt("number"); T["b2"] = wt(["two", "2"], after=T["b1"] + 1); T["b3"] = wt(["three", "3"], after=T["b2"] + 1)
T["b4"] = wt(["four", "4"], after=T["b3"] + 1); T["b5"] = wt("and", after=wt(["five", "5"], after=T["b4"]) - 1.0); T["b6"] = wt("send"); T["b7"] = wt("comment")
T["stars"] = wt(["200", "two"]); T["tests"] = wt("tests"); T["half"] = wt("half"); T["quarter"] = wt("quarter"); T["same"] = wt("same", after=T["quarter"])
T["purple"] = wt("purple"); T["designed"] = wt("designed"); T["fresh"] = wt("fresh"); T["google2"] = wt("google", after=T["fresh"])
T["thousands"] = wt("thousands"); T["read"] = wt("read", after=T["b4"]); T["never"] = wt("never"); T["scans"] = wt("scans")
T["hooks"] = wt("hooks"); T["zero"] = wt("zero"); T["kw"] = wt("plugins", after=T["b7"])

# ------------------------------------------------------------------ the browser card: images, camera moves, frames
CW, CH, BAR = 960, 760, 54          # card size; the screenshot viewport is CW x (CH - BAR)
VW, VH = CW, CH - BAR
SHOTS = {  # name -> (file, natural w, h, url shown in the bar)
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
# the card's sequence: (shot, from time, target box or None). A box zooms the camera onto it and draws the frame.
SEQ = [("pony_stars", 0.0, "t_pony_stars"), ("pony_top", T["b1"], None), ("pony_bench", T["tests"] - .2, "t_pony_bench"),
       ("unslop_top", T["b2"], None), ("unslop_slop", T["purple"] - .3, "t_unslop_slop"),
       ("egm_hero", T["b3"], "t_egm_hero"), ("google", T["google2"] - .25, "t_google"),
       ("reach_top", T["b4"], None), ("reach_about", T["read"] - .3, "t_reach_about"), ("reach_ro", T["never"] - .35, "t_reach_ro"),
       ("setup_top", T["b5"], None), ("setup", T["scans"] - .3, "t_setup")]
CARD_END = T["b6"]


def cam(shot, box):
    """start and end transform (x, y, scale) for a shot: tops pan down gently at full width; targets zoom onto the box"""
    _, w, h, _ = SHOTS[shot]
    s0 = VW / w
    if not box:
        return (0, 0, s0 * 1.0), (0, -(h * s0 - VH) * .35, s0 * 1.0)
    b = TG[box]
    s1 = min(s0 * 2.1, .86 * VW / b["w"])
    s1 = max(s1, s0 * 1.05)
    cx, cy = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    x1 = min(0, max(VW - w * s1, VW / 2 - cx * s1)); y1 = min(0, max(VH - h * s1, VH * .5 - cy * s1))
    sA = s0 * 1.02
    xA = min(0, max(VW - w * sA, VW / 2 - cx * sA)); yA = min(0, max(VH - h * sA, VH * .5 - cy * sA))
    return (xA, yA, sA), (x1, y1, s1)


imgs, frames = [], []
for k, (shot, t0, box) in enumerate(SEQ):
    f, w, h, url = SHOTS[shot]
    t1 = SEQ[k + 1][1] if k + 1 < len(SEQ) else CARD_END
    (xa, ya, sa), (xb, yb, sb) = cam(shot, box)
    imgs.append(f'<img class="shot" id="im{k}" src="assets/img/shots/{f}.png" style="width:{w}px;height:{h}px" alt="">')
    first = k == 0
    if first:
        js(f'tl.set("#im{k}", {{x: {xb:.1f}, y: {yb:.1f}, scale: {sb:.4f}, opacity: 1}}, 0);')   # frame 1 already shows the proof
    else:   # the next page slides up into the window, like scrolling to it
        ft(f"#im{k}", t0, .45, f"{{x: {xa:.1f}, y: {ya + 260:.1f}, scale: {sa:.4f}, opacity: 0}}", f"{{x: {xa:.1f}, y: {ya:.1f}, scale: {sa:.4f}, opacity: 1}}", "power3.out")
        to(f"#im{k - 1}", t0, .4, "{opacity: 0, y: '-=200'}", "power2.in")
        sfx("swish", t0 - .05)
    st("#url", t0 + .05, f'{{textContent: "{url}"}}')
    zoom_at = t0 + .45 if not first else -.75
    if box and first:
        b = TG[box]
        fx, fy, fw, fh = b["x"] * sb + xb - 10, b["y"] * sb + yb - 8, b["w"] * sb + 20, b["h"] * sb + 16
        frames.append(f'<div class="sel" id="fr{k}" style="left:{fx:.0f}px;top:{fy:.0f}px;width:{fw:.0f}px;height:{fh:.0f}px"><i></i><i></i><i></i><i></i></div>')
        ft(f"#fr{k}", .25, .3, "{opacity: 0, scale: 1.12}", "{opacity: 1, scale: 1}", "back.out(2)")
        sfx("click", .27)
        to(f"#fr{k}", t1 - .25, .2, "{opacity: 0}")
    elif box:
        ft(f"#im{k}", zoom_at, .75, f"{{x: {xa:.1f}, y: {ya:.1f}, scale: {sa:.4f}}}", f"{{x: {xb:.1f}, y: {yb:.1f}, scale: {sb:.4f}}}", "power3.inOut")
        b = TG[box]
        fx, fy, fw, fh = b["x"] * sb + xb - 10, b["y"] * sb + yb - 8, b["w"] * sb + 20, b["h"] * sb + 16
        fx, fy = max(4, fx), max(4, fy); fw, fh = min(VW - 8 - fx, fw), min(VH - 8 - fy, fh)
        frames.append(f'<div class="sel" id="fr{k}" style="left:{fx:.0f}px;top:{fy:.0f}px;width:{fw:.0f}px;height:{fh:.0f}px"><i></i><i></i><i></i><i></i></div>')
        ft(f"#fr{k}", zoom_at + .7, .3, "{opacity: 0, scale: 1.12}", "{opacity: 1, scale: 1}", "back.out(2)")
        sfx("click", zoom_at + .72)
        to(f"#fr{k}", t1 - .25, .2, "{opacity: 0}")
    else:
        ft(f"#im{k}", zoom_at, max(.5, t1 - zoom_at - .1), f"{{x: {xa:.1f}, y: {ya:.1f}}}", f"{{x: {xb:.1f}, y: {yb:.1f}}}", "sine.inOut")
to("#card", CARD_END - .3, .35, "{opacity: 0, y: -40, scale: .96}", "power2.in")
ft("#card", 0, .5, "{opacity: 1, y: 30, scale: .97}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.4)")   # visible on frame 1
# ------------------------------------------------------------------ headline band (line + violet chip), and the counter
HEADS = [("5 Claude Code plugins", "all free", 0.0, "00"), ("01  Ponytail", "half the code", T["b1"], "01"), ("02  Unslop", "no more AI slop", T["b2"], "02"),
         ("03  Elephant-Goldfish", "open-sourced by Google", T["b3"], "03"), ("04  Agent Reach", "read-only web access", T["b4"], "04"),
         ("05  Claude Code Setup", "official, from Anthropic", T["b5"], "05"), ("Send this", "to that friend", T["b6"], "05"),
         ("Comment", "PLUGINS", T["b7"], "05")]
for k, (a, b, t0, n) in enumerate(HEADS):
    t1 = HEADS[k + 1][2] if k + 1 < len(HEADS) else DUR + 1
    HTML.append(f'<div class="hd{" on" if k == 0 else ""}" id="hd{k}"><div class="h1">{a}</div><div class="h2"><span>{b}</span></div></div>')
    if k:
        js(f'tl.set("#hd{k}", {{opacity: 1}}, {t0 - .05:.3f});')
        ft(f"#hd{k} .h1", t0 - .05, .35, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "back.out(1.8)")
        ft(f"#hd{k} .h2 span", t0 + .12, .35, "{opacity: 0, scale: .7}", "{opacity: 1, scale: 1}", "back.out(2.2)")
        js(f'tl.call(() => {{ document.querySelector("#cnt b").textContent = "{n}"; }}, null, {t0:.3f});')
        sfx("whoosh", t0 - .15)
    if t1 < DUR:
        to(f"#hd{k}", t1 - .14, .14, "{opacity: 0, y: -18}", "power2.in")

# ------------------------------------------------------------------ fact chips under the card
CHIPS = [  # (text, at, gold?)  each beat's chips leave when the next beat starts
    [("200,000 stars", T["stars"], True)],
    [("-53% code", T["half"], True), ("-26% cost", T["quarter"], True), ("same accuracy", T["same"], False)],
    [("22.8k stars", T["b2"] + .4, True), ("finds the slop first", T["purple"], False)],
    [("Apache 2.0, open source", T["b3"] + .5, False), ("used daily at Google", T["thousands"], True)],
    [("115k stars", T["b4"] + .4, True), ("reads only, never posts", T["never"], False)],
    [("official Anthropic plugin", T["b5"] + .4, True), ("analyzes, never edits", T["hooks"], False)],
]
SRC = ["SOURCE: GITHUB", "SOURCE: PONYTAIL'S OWN BENCHMARK, 585 RUNS", "SOURCE: GITHUB.COM/HEYDAMIR/UNSLOP", "SOURCE: GOOGLE OPEN SOURCE BLOG, OCT 2026",
       "SOURCE: AGENT REACH README", "SOURCE: ANTHROPIC'S PLUGIN README"]
BEAT_T = [0.0, T["b1"], T["b2"], T["b3"], T["b4"], T["b5"], T["b6"]]
for k, row in enumerate(CHIPS):
    t_end = BEAT_T[k + 1]
    cells = "".join(f'<span class="chip{" gold" if g else ""}" id="ch{k}_{j}">{"<b id=" + chr(34) + "starN" + chr(34) + ">0</b> stars" if k == 0 else tx}</span>' for j, (tx, _, g) in enumerate(row))
    HTML.append(f'<div class="chips" id="chips{k}">{cells}</div><div class="src" id="src{k}">{SRC[k]}</div>')
    st(f"#chips{k}", BEAT_T[k], "{opacity: 1}")
    for j, (tx, at, g) in enumerate(row):
        ft(f"#ch{k}_{j}", at - .05, .35, "{opacity: 0, y: 26, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.2)")
        sfx("pop", at)
    ft(f"#src{k}", row[0][1] + .2, .4, "{opacity: 0}", "{opacity: 1}", "none")
    to(f"#chips{k}", t_end - .2, .2, "{opacity: 0, y: 14}", "power2.in")
    to(f"#src{k}", t_end - .2, .2, "{opacity: 0}", "none")
js(f'const SN = {{v: 0}}; tl.to(SN, {{v: 200000, duration: .9, ease: "power2.out", onUpdate: () => {{ document.getElementById("starN").textContent = Math.round(SN.v).toLocaleString("en-US"); }}}}, {T["stars"]:.3f});')
sfx("upgrade", T["stars"] + .6)

# ------------------------------------------------------------------ share beat: the five pages in a grid, each ticked
grid = "".join(f'<div class="gt" id="gt{i}"><img src="assets/img/shots/{SHOTS[s][0]}.png" alt=""><b>{n}</b></div>'
               for i, (s, n) in enumerate((("pony_top", "Ponytail"), ("unslop_top", "Unslop"), ("egm_hero", "Elephant-Goldfish"), ("reach_top", "Agent Reach"), ("setup_top", "Claude Code Setup"))))
HTML.append(f'<div id="grid">{grid}</div>')
for i in range(5):
    ft(f"#gt{i}", T["b6"] + .05 + i * .09, .4, "{opacity: 0, y: 40, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.7)")
    sfx("pop", T["b6"] + .1 + i * .09)
to("#grid", T["b7"] - .25, .25, "{opacity: 0, scale: .96}", "power2.in")

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
sfx("impact_soft", T["kw"] + .45)

CSS = f"""
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {PAPER}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; font-weight: 800; color: {INK};
  background-color: {PAPER};
  background-image: linear-gradient(rgba(101,22,199,.075) 2px, transparent 2px), linear-gradient(90deg, rgba(101,22,199,.075) 2px, transparent 2px),
    linear-gradient(rgba(101,22,199,.04) 1px, transparent 1px), linear-gradient(90deg, rgba(101,22,199,.04) 1px, transparent 1px);
  background-size: 216px 216px, 216px 216px, 54px 54px, 54px 54px; background-position: -2px -2px; }}
#glow {{ position: absolute; inset: 0; background: radial-gradient(60% 30% at 50% 50%, rgba(255,255,255,.85), rgba(255,255,255,0) 70%); }}
#bar {{ position: absolute; left: 64px; right: 64px; top: 252px; display: flex; justify-content: space-between; align-items: center; }}
#brand {{ display: flex; align-items: center; gap: 14px; font-family: Mono; font-size: 24px; letter-spacing: .14em; color: {INK}; }}
#brand i {{ width: 46px; height: 46px; border-radius: 13px; background: {INK}; display: grid; place-items: center; }}
#brand i img {{ width: 34px; height: 34px; }}
#cnt {{ font-family: Mono; font-size: 24px; letter-spacing: .14em; color: rgba(20,10,46,.55); }} #cnt b {{ color: {VIOLET}; }}
.hd {{ position: absolute; left: 40px; right: 40px; top: 322px; text-align: center; opacity: 0; }}
.hd.on {{ opacity: 1; }} .hd .h1, .hd .h2 span {{ opacity: 0; }} .hd.on .h1, .hd.on .h2 span {{ opacity: 1; }}
.h1 {{ font-size: 62px; line-height: 1.08; letter-spacing: -.035em; white-space: nowrap; }}
.h2 {{ margin-top: 10px; }}
.h2 span {{ display: inline-block; font-size: 52px; letter-spacing: -.02em; line-height: 1.15; padding: 4px 22px 8px; border-radius: 14px; background: {VIOLET}; color: #fff; white-space: nowrap; }}
#card {{ position: absolute; left: {(1080 - CW) // 2}px; top: 520px; width: {CW}px; height: {CH}px; border-radius: 26px; overflow: hidden; background: #fff;
  box-shadow: 0 30px 80px rgba(40,20,90,.22), 0 0 0 2px rgba(20,10,46,.08); }}
#cbar {{ height: {BAR}px; display: flex; align-items: center; gap: 10px; padding: 0 20px; background: #f1eff6; border-bottom: 2px solid #e4e0ee; }}
#cbar i {{ width: 15px; height: 15px; border-radius: 50%; }} #cbar i:nth-child(1) {{ background: #ff5f57; }} #cbar i:nth-child(2) {{ background: #febc2e; }} #cbar i:nth-child(3) {{ background: #28c840; }}
#url {{ margin-left: 18px; flex: 1; font-family: Inter; font-weight: 600; font-size: 22px; color: #5b5470; background: #fff; border-radius: 10px; padding: 6px 16px; white-space: nowrap; overflow: hidden; }}
#vp {{ position: relative; width: {VW}px; height: {VH}px; overflow: hidden; background: #fff; }}
.shot {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; opacity: 0; }}
.sel {{ position: absolute; border: 4px solid {VIOLET}; border-radius: 6px; opacity: 0; box-shadow: 0 0 0 9999px rgba(20,10,46,.10); }}
.sel i {{ position: absolute; width: 16px; height: 16px; background: #fff; border: 4px solid {VIOLET}; border-radius: 3px; }}
.sel i:nth-child(1) {{ left: -10px; top: -10px; }} .sel i:nth-child(2) {{ right: -10px; top: -10px; }} .sel i:nth-child(3) {{ left: -10px; bottom: -10px; }} .sel i:nth-child(4) {{ right: -10px; bottom: -10px; }}
.fan {{ position: absolute; left: 290px; top: 600px; width: 500px; height: 560px; border-radius: 20px; overflow: hidden; background: #fff; opacity: 0;
  box-shadow: 0 20px 50px rgba(40,20,90,.18), 0 0 0 2px rgba(20,10,46,.08); }}
.fan img {{ width: 100%; }}
.chips {{ position: absolute; left: 40px; right: 40px; top: 1305px; display: flex; justify-content: center; flex-wrap: wrap; gap: 16px; opacity: 0; }}
.chip {{ font-family: Inter; font-weight: 700; font-size: 36px; padding: 12px 24px; border-radius: 16px; background: #fff; color: {INK}; opacity: 0;
  box-shadow: 0 8px 22px rgba(40,20,90,.12), 0 0 0 2px rgba(101,22,199,.18); white-space: nowrap; }}
.chip.gold {{ background: {INK}; color: #fff; box-shadow: 0 8px 22px rgba(40,20,90,.2); }}
.chip b {{ font-variant-numeric: tabular-nums; }}
.src {{ position: absolute; left: 0; right: 0; top: 1392px; text-align: center; font-family: Mono; font-size: 19px; letter-spacing: .12em; color: rgba(20,10,46,.66); opacity: 0;
  }}
.cap {{ position: absolute; left: 50px; right: 50px; top: 1440px; text-align: center; font-family: Inter; font-weight: 700; font-size: 56px; opacity: 0; letter-spacing: -.01em; line-height: 1.2; color: {INK}; }}
.cw {{ display: inline-block; padding: 2px 12px; margin: 0 2px; border-radius: 14px; opacity: 0; transform-origin: 50% 80%; }}
#grid {{ position: absolute; left: 60px; right: 60px; top: 560px; display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }}
.gt {{ position: relative; height: 230px; border-radius: 20px; overflow: hidden; background: #fff; opacity: 0; box-shadow: 0 14px 34px rgba(40,20,90,.16), 0 0 0 2px rgba(20,10,46,.08); }}
.gt:nth-child(5) {{ grid-column: 1 / span 2; width: 470px; justify-self: center; }}
.gt img {{ width: 100%; }}
.gt b {{ position: absolute; left: 14px; bottom: 14px; font-family: Inter; font-weight: 700; font-size: 28px; padding: 6px 14px; border-radius: 10px; background: {VIOLET}; color: #fff; }}
#cbox {{ position: absolute; left: 90px; right: 90px; top: 760px; height: 132px; border-radius: 66px; opacity: 0; display: flex; align-items: center; gap: 24px;
  padding: 0 38px 0 26px; background: #fff; color: {INK}; box-shadow: 0 30px 80px rgba(40,20,90,.22), 0 0 0 3px {VIOLET}; }}
#cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: {INK}; display: grid; place-items: center; flex: none; }} #cbox .av img {{ width: 54px; }}
#cbox .tx {{ flex: 1; font-size: 54px; letter-spacing: .03em; }} #cbox .tx span {{ opacity: 0; }}
#cpost {{ font-size: 36px; color: #8a8299; }}
#endmark {{ position: absolute; left: 0; right: 0; top: 960px; text-align: center; font-family: Mono; font-size: 30px; letter-spacing: .18em; color: rgba(20,10,46,.7); opacity: 0; }}
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>NXTLVL 5 Claude Code plugins 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="glow"></div>
      <div id="bar"><div id="brand"><i><img src="assets/img/logo-mark.svg" alt=""></i>NXTLVLSOCIAL.AI</div><div id="cnt"><b>00</b> / 05</div></div>
      <div id="card"><div id="cbar"><i></i><i></i><i></i><div id="url">github.com</div></div><div id="vp">{''.join(imgs)}{''.join(frames)}</div></div>
      {chr(10).join(HTML)}
      <div id="cbox"><div class="av"><img src="assets/img/logo-mark.svg" alt=""></div><div class="tx">{"".join(f'<span id="ck{i}">{c}</span>' for i, c in enumerate("PLUGINS"))}</div><b id="cpost">Post</b></div>
      <div id="endmark">ALL FIVE LINKS IN YOUR DMS</div>
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
json.dump({"dur": DUR}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {len(groups)} caption groups")
print({k: round(v, 2) for k, v in T.items()})
