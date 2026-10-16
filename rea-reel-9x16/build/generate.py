"""Build the REA reel composition.

  python3 -I build/generate.py            -> index.html (avatar video + stage + graphics)
  python3 -I build/generate.py overlay    -> overlay/index.html (graphics only, transparent)

Timing comes from build/scribe_words.json (ElevenLabs Scribe on the avatar clip). The clip
is started 0.30 s in (leading silence only) so the last word ends at 29.94 s and the reel is
exactly 30.0 s, as the brief requires.
"""
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OVERLAY = len(sys.argv) > 1 and sys.argv[1] == "overlay"
DUR = 30.0
OFF = 0.30  # seconds trimmed from the head of the avatar clip

RAW = json.load(open(os.path.join(ROOT, "build", "scribe_words.json")))["words"]
W = [{"w": w["text"], "s": round(w["start"] - OFF, 3), "e": round(w["end"] - OFF, 3)} for w in RAW]


def at(word, after=0.0):
    key = re.sub(r"[^a-z0-9-]", "", word.lower())
    for w in W:
        if w["s"] >= after - 1e-6 and re.sub(r"[^a-z0-9-]", "", w["w"].lower()) == key:
            return w["s"]
    raise KeyError(word)


# ------------------------------------------------------------- scene times (re-synced)
S1, S2, S3, S4 = 0.0, at("its"), at("ask"), at("it", 13)
S5, S6, S7, S8 = at("and", 17), at("desktop"), at("and", 23.5), at("comment")
SC = [("s1", S1, S2), ("s2", S2, S3), ("s3", S3, S4), ("s4", S4, S5),
      ("s5", S5, S6), ("s6", S6, S7), ("s7", S7, S8), ("s8", S8, DUR)]
T = {k: (a, b) for k, a, b in SC}
t_free, t_rebuild = at("free"), at("rebuild")
t_two, t_stars = at("two"), at("stars")
t_why = at("why")
t_rule = at("rule")
t_drag0, t_slider = at("your", 17), at("slider")
t_and2, t_android, t_web = S6, at("android"), at("websites")
t_nothing = at("nothing")
t_repo, t_dm, t_link = at("repo", 27), at("dm"), at("link")

# ------------------------------------------------------------- pixel sprites (own drawing)
DINO_BODY = [
    "..........########..",
    ".........##.########",
    ".........###########",
    ".........###########",
    ".........#####......",
    ".........########...",
    "#.......#####.......",
    "#......#######......",
    "##....#########.....",
    "###..##########.....",
    "###############.....",
    ".#############......",
    "..###########.......",
    "...#########........",
    "....#######.........",
]
LEGS_A = [".....###.##.........", ".....##...#.........", ".....#.....##.......", ".....##.............."]
LEGS_B = [".....##.###.........", ".....#....##........", "....##.....#........", "...........##......."]
CACTUS = ["..##..", "..##.#", "#.##.#", "#.####", "####..", "..##..", "..##..", "..##..", "..##.."]


def sprite(rows, px, body="#8a8f98", rim="#FFD166"):
    out = []
    h = len(rows)
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != "#":
                continue
            right_open = x + 1 >= len(row) or row[x + 1] != "#"
            fill = rim if right_open else body
            out.append(f'<rect x="{x * px}" y="{y * px}" width="{px}" height="{px}" fill="{fill}"/>')
    w = max(len(r) for r in rows) * px
    return f'<svg width="{w}" height="{h * px}" viewBox="0 0 {w} {h * px}" shape-rendering="crispEdges">{"".join(out)}</svg>'


def dino(prefix, px):
    a = sprite(DINO_BODY + LEGS_A, px)
    b = sprite(DINO_BODY + LEGS_B, px)
    return (f'<div class="dino"><div id="{prefix}-fa" class="dframe">{a}</div>'
            f'<div id="{prefix}-fb" class="dframe">{b}</div></div>')


def runner(prefix, width, px, cacti_x, ground_len):
    cacti = "".join(f'<div class="cactus" style="left:{x}px">{sprite(CACTUS, px)}</div>' for x in cacti_x)
    dashes = "".join(f'<span class="gdash" style="left:{x}px;width:{18 + (x * 7) % 40}px;top:{8 + (x * 3) % 18}px"></span>'
                     for x in range(0, ground_len, 70))
    return (f'<div class="runner" style="width:{width}px" data-layout-allow-overflow>'
            f'<div id="{prefix}-world" class="world" style="width:{ground_len}px" data-layout-allow-overflow>{cacti}<div class="ground"></div>{dashes}</div>'
            f'{dino(prefix, px)}</div>')


ICON = {
    "desktop": '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "android": '<path d="M6 10a6 6 0 0 1 12 0v7H6z"/><path d="M8 4.5l1.5 2M16 4.5l-1.5 2"/><circle cx="9.5" cy="9.5" r=".6"/><circle cx="14.5" cy="9.5" r=".6"/><path d="M4 11v5M20 11v5M9 17v3M15 17v3"/>',
    "web": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/><circle cx="6" cy="6.5" r=".6"/><circle cx="8.5" cy="6.5" r=".6"/>',
    "laptop": '<rect x="5" y="5" width="14" height="10" rx="1.5"/><path d="M2 19h20l-2-4H4z"/>',
    "lock": '<rect x="6" y="11" width="12" height="9" rx="2"/><path d="M9 11V8a3 3 0 0 1 6 0v3"/>',
    "cloud": '<path d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9z"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24">{ICON[name]}</svg>'


def stamp(sid, text):
    return (f'<div class="stamp-wrap"><div id="{sid}" class="stamp">{icon("check", "stamp-ic")}'
            f'<span>{text}</span></div></div>')


def clip(sid, inner, track=2, cls=""):
    a, b = T[sid]
    return (f'<section id="{sid}" class="clip scene {cls}" data-start="{a:.3f}" data-duration="{b - a:.3f}" '
            f'data-track-index="{track}">{inner}</section>')


CODE = [
    ("k", "if"), ("p", " (this.currentSpeed < this.config.MAX_SPEED) {"),
]
SNIPPET = [
    'if (this.currentSpeed &lt; this.config.MAX_SPEED) {',
    '  this.currentSpeed += this.config.ACCELERATION;',
    '}',
    '',
    '<span class="cm">// config</span>',
    'SPEED: <span class="num">6</span>,',
    'ACCELERATION: <span class="num">0.001</span>,',
    'MAX_SPEED: <span class="num">13</span>',
]
parts = []

# S1 hook: a feature lifts out of an app and becomes code
s1 = (
    '<div class="hl-wrap top"><div id="s1-h1" class="hl">LOVE A <span class="acc">FEATURE?</span></div></div>'
    '<div class="hl-wrap top"><div id="s1-h2" class="hl">REBUILD <span class="acc">IT.</span></div></div>'
    '<div class="app-stage" data-layout-allow-overlap data-layout-allow-occlusion data-layout-allow-overflow><div id="app" class="app" data-layout-allow-overlap data-layout-allow-occlusion>'
    '<div class="app-top"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="app-name">Any app</span></div>'
    '<div class="flip-wrap" data-layout-allow-overlap data-layout-allow-occlusion data-layout-allow-overflow><div id="flip" class="flip" data-layout-allow-overlap data-layout-allow-overflow>'
    '<div id="sbar" class="face front"><span class="sb-ic">⌕</span><span class="sb-tx">Search notes…</span><span class="sb-k">⌘K</span></div>'
    '<div class="face back"><pre class="code sm"><span class="tag">&lt;SearchBar</span>\n  placeholder=<span class="str">"Search…"</span>\n  onChange={filter}\n  autoFocus <span class="tag">/&gt;</span></pre></div>'
    '</div></div>'
    '<div class="app-rows"><span></span><span></span><span></span><span class="short"></span></div>'
    '</div>'
    '<div class="free-wrap"><div id="s1-free" class="stamp free">FREE</div></div>'
    + stamp("s1-rebuilt", "REBUILT").replace('class="stamp-wrap"', 'class="stamp-wrap s1"') +
    '</div>'
)
parts.append(clip("s1", s1))

# S2 proof: repo card + star counter
burst = "".join(f'<div class="bs-wrap" style="transform:rotate({i * 30}deg)"><div id="bs{i}" class="bs">{icon("star", "bs-ic")}</div></div>'
                for i in range(12))
s2 = ('<div class="card-stage"><div id="repo" class="repo">'
      '<div class="repo-top"><span class="repo-glyph">▣</span><span class="repo-name">morluto/<b>rea</b></span><span class="pill">Public</span></div>'
      '<div class="repo-tag">Reverse engineer anything with agents</div>'
      '<div class="repo-row"><span class="star-box">' + icon("star", "star-ic") +
      '<span id="stars" class="stars">0</span><span class="stars-u">stars</span></span><span class="pill mit">MIT license</span></div>'
      f'<div class="burst">{burst}</div>'
      '</div></div>')
parts.append(clip("s2", s2))

# S3 open loop: dino runner speeding up
stars_bg = "".join(f'<span class="sky-dot" style="left:{(i * 137) % 900 + 40}px;top:{(i * 89) % 330 + 300}px"></span>' for i in range(26))
s3 = ('<div class="night"></div>' + stars_bg +
      '<div class="moon"></div>'
      '<div class="chip-wrap q"><div id="s3-chip" class="chip ghost">Ask your agent:</div></div>'
      '<div class="q-wrap"><div id="s3-q" class="question"></div></div>'
      '<div id="s3-lines" class="speedlines" data-layout-allow-overflow>' + "".join(f'<span class="sl" style="top:{740 + (i * 53) % 260}px;width:{120 + (i * 41) % 220}px"></span>' for i in range(9)) + '</div>'
      '<div class="run-stage">' + runner("d3", 900, 7, [700, 1400, 1950, 2700, 3300, 4100, 4700, 5500, 6200, 7000, 7700, 8500], 9000) + '</div>'
      '<div class="meter"><span class="m-lab">SPEED</span><div class="m-bar"><div id="s3-fill" class="m-fill"></div></div>'
      '<span id="s3-spd" class="m-num">6.0</span></div>')
parts.append(clip("s3", s3, cls="dark"))

# S4 evidence: the rule in the code
code_lines = "".join(f'<div class="ln"><span class="ln-n">{i + 1}</span><span class="ln-t">{l or "&nbsp;"}</span></div>'
                     for i, l in enumerate(SNIPPET))
s4 = ('<div class="thumb-wrap"><div id="s4-thumb" class="thumb">' + runner("d4", 300, 3, [180, 520, 900], 1200) + '</div></div>'
      '<div class="code-stage"><div id="code" class="codecard">'
      '<div class="cc-top"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="cc-file">runner.js</span></div>'
      '<div class="cc-body"><div id="hl-sweep" class="hl-sweep"></div>' + code_lines + '</div>'
      '<div class="ev-wrap"><div id="s4-ev" class="stamp ev">EVIDENCE</div></div>'
      '</div></div>'
      '<div class="chips">'
      '<div class="chip-wrap"><div id="c1" class="chip val">SPEED <b>6</b></div></div>'
      '<div class="chip-wrap"><div id="c2" class="chip val">ACCELERATION <b>0.001</b></div></div>'
      '<div class="chip-wrap"><div id="c3" class="chip val">MAX <b>13</b></div></div></div>'
      '<div class="foot">Use only on software you\'re authorized to analyze.</div>')
parts.append(clip("s4", s4))

# S5 rebuild: speed slider
s5 = ('<div class="mini-stage"><div id="mini" class="mini">' + runner("d5", 860, 6, [600, 1200, 1700, 2300, 2900, 3500, 4100, 4700, 5300, 5900], 6400) + '</div></div>'
      '<div class="slider-stage"><div id="slider" class="slider">'
      '<div class="sl-head"><span class="sl-lab">Speed</span><span id="s5-spd" class="sl-num">6.0</span></div>'
      '<div class="track"><div id="s5-fill" class="track-fill"></div><div id="knob" class="knob"><div id="cursor" class="cursor">➤</div></div></div>'
      '<div class="sl-ends"><span>6</span><span>13</span></div></div></div>'
      + stamp("s5-rebuilt", "REBUILT").replace('class="stamp-wrap"', 'class="stamp-wrap s5"'))
parts.append(clip("s5", s5))

# S6 targets
rows = [("desktop", "DESKTOP APPS", '<span class="tag-sm">+ Electron</span>'), ("android", "ANDROID APKs", ""), ("web", "WEBSITES", "")]
s6 = '<div class="rows">' + "".join(
    f'<div class="row-wrap"><div id="r{i}" class="trow"><span class="t-ic">{icon(k)}</span><span class="t-col"><span class="t-tx">{t}</span>{extra}</span></div></div>'
    for i, (k, t, extra) in enumerate(rows)) + '</div>'
parts.append(clip("s6", s6))

# S7 local
s7 = ('<div class="local-stage">'
      f'<div class="cloud-wrap"><div id="cloud" class="cloud">{icon("cloud", "big-ic")}</div></div>'
      '<svg class="arrow-svg" width="200" height="300" viewBox="0 0 200 300"><path id="arrow" class="arrow" d="M100 290 L100 40" pathLength="1"/>'
      '<path id="arrow-head" class="arrow-h" d="M70 75 L100 40 L130 75"/></svg>'
      '<div class="xmark-wrap"><div id="xmark" class="xmark">✕</div></div>'
      f'<div class="laptop-wrap"><div id="laptop" class="laptop">{icon("laptop", "big-ic")}<span id="lock" class="lock">{icon("lock", "lock-ic")}</span></div></div>'
      '<div class="local-tx"><div id="s7-t1" class="lt1">RUNS LOCALLY</div><div id="s7-t2" class="lt2">NOTHING UPLOADED</div></div>'
      '</div>')
parts.append(clip("s7", s7))

# S8 CTA: avatar full frame; graphics in the top band and below the captions
s8 = ('<div class="cta-top"><div id="bubble" class="bubble"><span class="b-user">You</span>'
      '<span id="b-text" class="b-text"></span><span id="caret" class="caret"></span></div>'
      '<div class="chip-wrap"><div id="repo-chip" class="chip key">REPO</div></div></div>'
      '<div class="cta-bottom"><div id="dm" class="dm"><span class="dm-av">R</span><span class="dm-col"><span class="dm-from">DM</span>'
      '<span class="dm-tx">REA repo link</span></span></div>'
      '<div id="url" class="url"><span class="rea-mark">R</span>github.com/morluto/rea</div></div>')
parts.append(clip("s8", s8, cls="cta"))

# ------------------------------------------------------------- captions (REA / DM / 286K)
REPL = {"rhea,": "REA,", "rhea": "REA", '"repo"': "REPO", '"why': "Why", 'faster?"': "faster?"}
cw = []
i = 0
while i < len(W):
    w = W[i]
    if w["w"].lower() == "two" and i + 4 < len(W) and W[i + 4]["w"].lower() == "thousand":
        cw.append({"w": "286K", "s": w["s"], "e": W[i + 4]["e"]}); i += 5; continue
    cw.append({"w": REPL.get(w["w"].lower(), w["w"]), "s": w["s"], "e": w["e"]}); i += 1
groups, cur = [], []
for w in cw:
    if cur and (len(cur) >= 4 or w["s"] - cur[-1]["e"] > 0.45 or len(" ".join(x["w"] for x in cur + [w])) > 22):
        groups.append(cur); cur = []
    cur.append(w)
    if re.search(r"[.?!]$", w["w"]):
        groups.append(cur); cur = []
if cur:
    groups.append(cur)
caps = []
js_caps = []
for gi, g in enumerate(groups):
    a = g[0]["s"]
    nxt = groups[gi + 1][0]["s"] if gi + 1 < len(groups) else DUR
    b = min(nxt, g[-1]["e"] + 0.4, DUR)
    spans = " ".join(f'<span id="w{gi}_{k}" class="cw">{html.escape(x["w"])}</span>' for k, x in enumerate(g))
    caps.append(f'<div id="cap{gi}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="5">'
                f'<div id="capi{gi}" class="cap-in">{spans}</div></div>')
    js_caps.append(f'tl.fromTo("#capi{gi}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{a:.3f});')
    for k, x in enumerate(g):
        js_caps.append(f'tl.set("#w{gi}_{k}",{{color:"#2EE6A6"}},{x["s"]:.3f});')
        js_caps.append(f'tl.set("#w{gi}_{k}",{{color:"#ffffff"}},{max(x["e"], x["s"] + 0.05):.3f});')

# ------------------------------------------------------------- timeline
J = []
A = J.append


def pop(sel, t, d=0.3, frm="scale:0.6,opacity:0", ease="back.out(2.2)"):
    A(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,duration:{d},ease:"{ease}"}},{t:.3f});')


def stamp_in(sel, t):
    A(f'tl.fromTo("{sel}",{{scale:1.4,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:-8,duration:0.2,ease:"back.out(3)"}},{t:.3f});')
    A(f'tl.fromTo("{sel}",{{x:0}},{{x:4,duration:0.04,repeat:3,yoyo:true,ease:"none"}},{t + 0.2:.3f});')


def run_cycle(prefix, a, b, step):
    t, k = a, 0
    while t < b:
        A(f'tl.set("#{prefix}-fa",{{opacity:{1 if k % 2 == 0 else 0}}},{t:.3f});')
        A(f'tl.set("#{prefix}-fb",{{opacity:{0 if k % 2 == 0 else 1}}},{t:.3f});')
        t += step(t); k += 1


# avatar: full frame (S1) -> circle (S2-S7) -> full frame (S8)
# The face sits near (540, 700) in the full frame. The circle state scales the frame by
# S_C around (0,0) and moves the face to the circle centre (200, 1370), clipped to radius 150.
FX, FY, R_FULL = 540, 700, 330
S_C = 150 / R_FULL
CX, CY = 200 - S_C * FX, 1370 - S_C * FY
CLIP_FULL = f"circle(2400px at {FX}px {FY}px)"
CLIP_CIRC = f"circle({R_FULL}px at {FX}px {FY}px)"
A(f'tl.fromTo("#avatar",{{scale:1,x:0,y:0,clipPath:"{CLIP_FULL}",transformOrigin:"0px 0px"}},'
  f'{{scale:{S_C:.4f},x:{CX:.1f},y:{CY:.1f},clipPath:"{CLIP_CIRC}",duration:0.35,ease:"power2.inOut"}},{S2:.3f});')
A(f'tl.to("#avatar",{{scale:1,x:0,y:0,clipPath:"{CLIP_FULL}",duration:0.4,ease:"power2.inOut"}},{S8:.3f});')
A(f'tl.fromTo("#avatar-in",{{scale:1}},{{scale:1.06,duration:{S2:.3f},ease:"none"}},0);')
A(f'tl.to("#avatar-in",{{scale:1,duration:0.35,ease:"power2.inOut"}},{S2:.3f});')
A(f'tl.fromTo("#ring",{{opacity:0}},{{opacity:1,duration:0.3}},{S2 + 0.1:.3f});')
A(f'tl.to("#ring",{{opacity:0,duration:0.2}},{S8:.3f});')
A(f'tl.fromTo("#stage",{{opacity:0}},{{opacity:1,duration:0.3}},{S2:.3f});')
A(f'tl.to("#stage",{{opacity:0,duration:0.35}},{S8:.3f});')

# S1
A('tl.fromTo("#s1-h1",{scale:1.15,opacity:0},{scale:1,opacity:1,duration:0.35,ease:"back.out(2)"},0.0);')
A('tl.fromTo("#app",{y:700,opacity:0},{y:0,opacity:1,duration:0.45,ease:"power3.out"},1.2);')
A('tl.fromTo("#sbar",{boxShadow:"0 0 0 0 rgba(46,230,166,0)"},{boxShadow:"0 0 0 8px rgba(46,230,166,0.55)",duration:0.25},1.45);')
A('tl.fromTo("#flip",{y:0,scale:1},{y:-150,scale:1.12,duration:0.3,ease:"power2.out"},1.6);')
A('tl.fromTo("#flip",{rotationY:0},{rotationY:180,duration:0.45,ease:"power2.inOut"},1.9);')
stamp_in("#s1-free", t_free - 0.05)
A('tl.to("#s1-h1",{opacity:0,y:-30,duration:0.2},3.2);')
A('tl.fromTo("#s1-h2",{scale:1.15,opacity:0},{scale:1,opacity:1,duration:0.3,ease:"back.out(2)"},3.25);')
stamp_in("#s1-rebuilt", t_rebuild)

# S2
pop("#repo", S2 + 0.15, 0.3, "scale:0.8,opacity:0")
A(f'(function(){{var o={{v:0}};tl.to(o,{{v:286,duration:1.6,ease:"expo.out",onUpdate:function(){{document.getElementById("stars").textContent=Math.round(o.v)+"K";}}}},{t_two:.3f});}})();')
for i in range(12):
    tb = t_two + 1.6
    A(f'tl.fromTo("#bs{i}",{{opacity:0}},{{opacity:1,duration:0.08}},{tb:.3f});')
    A(f'tl.fromTo("#bs{i}",{{y:0,scale:0.4}},{{y:-150,scale:1,duration:0.5,ease:"power2.out"}},{tb:.3f});')
    A(f'tl.to("#bs{i}",{{opacity:0,duration:0.2}},{tb + 0.3:.3f});')

# S3
a3, b3 = T["s3"]
pop("#s3-chip", a3 + 0.05, 0.3, "opacity:0,y:20")
Q = "WHY DOES IT GET FASTER?"
qt = t_why
for k in range(len(Q) + 1):
    A(f'tl.set("#s3-q",{{textContent:{json.dumps(Q[:k])}}},{qt + k / 25:.3f});')
A(f'tl.fromTo("#d3-world",{{x:0}},{{x:-7600,duration:{b3 - a3:.3f},ease:"power2.in"}},{a3:.3f});')
run_cycle("d3", a3, b3, lambda t: max(0.06, 0.14 - (t - a3) * 0.02))
A(f'tl.fromTo("#s3-lines",{{opacity:0}},{{opacity:1,duration:{b3 - a3:.3f},ease:"power1.in"}},{a3:.3f});')
A(f'tl.fromTo(".sl",{{x:900}},{{x:-500,duration:0.5,repeat:{int((b3 - a3) / 0.5) - 1},ease:"none",stagger:0.05}},{a3:.3f});')
A(f'tl.fromTo("#s3-fill",{{scaleX:0}},{{scaleX:1,duration:{b3 - a3 - 0.3:.3f},ease:"power1.in"}},{a3 + 0.2:.3f});')
A(f'(function(){{var o={{v:6}};tl.to(o,{{v:13,duration:{b3 - a3 - 0.3:.3f},ease:"power1.in",onUpdate:function(){{document.getElementById("s3-spd").textContent=o.v.toFixed(1);}}}},{a3 + 0.2:.3f});}})();')

# S4
a4, b4 = T["s4"]
pop("#s4-thumb", a4, 0.3, "scale:1.6,opacity:0")
A(f'tl.fromTo("#d4-world",{{x:0}},{{x:-900,duration:{b4 - a4:.3f},ease:"none"}},{a4:.3f});')
run_cycle("d4", a4, b4, lambda t: 0.1)
A(f'tl.fromTo("#code",{{y:500,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"power3.out"}},{a4 + 0.05:.3f});')
t_finds = at("finds")
A(f'tl.fromTo("#hl-sweep",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.inOut"}},{t_finds:.3f});')
for i, k in enumerate(("c1", "c2", "c3")):
    pop(f"#{k}", t_finds + 0.6 + i * 0.3, 0.3)
stamp_in("#s4-ev", t_rule + 0.05)

# S5
a5, b5 = T["s5"]
pop("#slider", a5, 0.3, "y:80,opacity:0")
pop("#mini", a5 + 0.05, 0.3, "scale:0.9,opacity:0")
d0, d1 = a5 + 0.4, t_slider - 0.05
A(f'tl.fromTo("#knob",{{x:0}},{{x:620,duration:{d1 - d0:.3f},ease:"power2.inOut"}},{d0:.3f});')
A(f'tl.fromTo("#s5-fill",{{scaleX:0}},{{scaleX:1,duration:{d1 - d0:.3f},ease:"power2.inOut"}},{d0:.3f});')
A(f'(function(){{var o={{v:6}};tl.to(o,{{v:13,duration:{d1 - d0:.3f},ease:"power2.inOut",onUpdate:function(){{document.getElementById("s5-spd").textContent=o.v.toFixed(1);}}}},{d0:.3f});}})();')
A(f'tl.fromTo("#d5-world",{{x:0}},{{x:-5400,duration:{b5 - a5:.3f},ease:"power2.in"}},{a5:.3f});')
run_cycle("d5", a5, b5, lambda t: 0.13 if t < d0 + 0.6 else (0.09 if t < d0 + 1.4 else 0.06))
stamp_in("#s5-rebuilt", d1 + 0.1)

# S6
for i, t in enumerate((t_and2 + 0.05, t_android - 0.05, t_web - 0.05)):
    pop(f"#r{i}", t, 0.25, "scale:0.6,opacity:0")

# S7
a7, b7 = T["s7"]
pop("#laptop", a7 + 0.05, 0.3)
pop("#lock", a7 + 0.25, 0.3)
pop("#cloud", a7 + 0.2, 0.3, "opacity:0,y:-30")
pop("#s7-t1", a7 + 0.3, 0.3, "opacity:0,y:30")
A(f'tl.fromTo("#arrow",{{strokeDashoffset:1}},{{strokeDashoffset:0.35,duration:{t_nothing - a7 - 0.7:.3f},ease:"power1.out"}},{a7 + 0.6:.3f});')
A(f'tl.fromTo("#arrow-head",{{opacity:0}},{{opacity:1,duration:0.2}},{a7 + 0.6:.3f});')
A(f'tl.fromTo("#arrow-head",{{y:250}},{{y:250 - 250 * 0.65,duration:{t_nothing - a7 - 0.7:.3f},ease:"power1.out"}},{a7 + 0.6:.3f});')
stamp_in("#xmark", t_nothing - 0.05)
pop("#s7-t2", t_nothing + 0.2, 0.3, "opacity:0,y:30")

# S8
a8 = T["s8"][0]
pop("#bubble", a8 + 0.3, 0.3, "opacity:0,y:-30")
for k, ch in enumerate("REPO"):
    A(f'tl.set("#b-text",{{textContent:"{"REPO"[:k + 1]}"}},{t_repo + k * 0.07:.3f});')
A(f'tl.fromTo("#caret",{{opacity:1}},{{opacity:0,duration:0.25,repeat:7,yoyo:true,ease:"steps(1)"}},{a8 + 0.3:.3f});')
pop("#repo-chip", t_repo + 0.35, 0.3)
A(f'tl.to("#repo-chip",{{scale:1.06,duration:0.6,repeat:{max(0, int((DUR - t_repo - 0.7) / 0.6) - 1)},yoyo:true,ease:"sine.inOut"}},{t_repo + 0.7:.3f});')
pop("#dm", t_dm - 0.1, 0.35, "opacity:0,x:-120")
pop("#url", t_link - 0.55, 0.35, "opacity:0,y:20")

J += js_caps

# ------------------------------------------------------------- document
css = open(os.path.join(ROOT, "build", "style.css")).read()
avatar = "" if OVERLAY else (
    '<div id="avatar" class="avatar"><div id="avatar-in" class="avatar-in">'
    f'<video id="avatar-video" src="assets/video/avatar.mp4" data-start="0" data-duration="{DUR}" '
    f'data-media-start="{OFF}" data-has-audio="true" data-track-index="0" playsinline></video></div></div>')
ring = '<div id="ring" class="ring"></div>'
if OVERLAY:  # keep the timeline targets the avatar tweens use, but draw nothing
    avatar = '<div id="avatar" class="avatar ghost"><div id="avatar-in" class="avatar-in"></div></div>'
stage = "" if OVERLAY else '<div id="stage" class="stage"></div>'
if OVERLAY:
    stage = '<div id="stage" class="stage ghost"></div>'
doc = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>REA reel 9x16{' overlay' if OVERLAY else ''}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{css}
{'#root, html, body { background: transparent !important; }' if OVERLAY else ''}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      {stage}
      {avatar}
      {ring}
      {"".join(parts)}
      {"".join(caps)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join("      " + l for l in J)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
if OVERLAY:
    out = os.path.join(ROOT, "overlay")
    os.makedirs(out, exist_ok=True)
    for sub in ("assets/fonts", "assets/vendor"):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(out, sub), dirs_exist_ok=True)
    for f in ("hyperframes.json", "meta.json", "package.json"):
        shutil.copy(os.path.join(ROOT, f), out)
    open(os.path.join(out, "index.html"), "w").write(doc)
else:
    open(os.path.join(ROOT, "index.html"), "w").write(doc)
json.dump({"offset": OFF, "scenes": SC, "captions": [[x["w"] for x in g] for g in groups]},
          open(os.path.join(ROOT, "build", "timing.json"), "w"), indent=1)
print("scenes", [(k, round(a, 2), round(b, 2)) for k, a, b in SC])
print("captions", len(groups), "tweens", len(J))
