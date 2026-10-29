"""AI War Room reel: writes index.html. 1080x1920, 30 fps, about 70 s. Account: @ai.nxtlvl.

python3 build/generate.py      (from the project root, after build/voice.py and build/timing.py)

A flat war-room strategy map (HTML + SVG + GSAP, no WebGL, so it renders fast): four kingdoms on a dark tactical
table, one per AI (ChatGPT, Gemini, Claude, Grok, with their logos), a game-style HUD, word-by-word captions on top,
and a camera that zooms from kingdom to kingdom. Cue times come from build/words.json.

Every number on screen is from coverage of Emergence AI's "Emergence World" study (15 days, 10 agents per world):
Grok 4.1 Fast 183 crimes, 100+ assaults and six arsons, extinct in about four days; Gemini 3 Flash 683 crimes over
15 days, still climbing, and the agent Mira voted for her own removal; GPT-5 mini two crimes, all agents gone within
seven days; Claude Sonnet 4.6 zero crimes, 10/10 alive; in the mixed world Claude agents turned to theft and
intimidation ("normative drift"). The crime pins are illustrative; the counters carry the real numbers.
"""
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
VOICE_END = LINES[-1]["end"]
DUR = round(VOICE_END + 1.5, 2)


def word(line, text, nth=1):
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1]["s"]


L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
T = {
    "chatgpt": word(1, "chatgpt"), "claude": word(1, "claude"), "gemini": word(1, "gemini"), "grok": word(1, "grok"),
    "fifteen": word(1, "fifteen"), "humans": word(1, "humans"),
    "emergence": word(2, "emergence"), "ten": word(2, "ten"), "credits": word(2, "credits"),
    "punch": word(3, "punch"), "steal": word(3, "steal"), "fire": word(3, "fire"), "banned": word(3, "banned"), "who": word(3, "who"),
    "assaults": word(4, "assaults"), "six": word(4, "six"), "e183": word(4, "eighty"), "four": word(4, "four"), "nobody": word(4, "nobody"),
    "alive4": word(4, "alive"),
    "g15": word(5, "fifteen"), "g683": word(5, "six"), "climbing": word(5, "climbing"), "delete": word(5, "delete"),
    "two": word(6, "two"), "survive": word(6, "survive"), "seven": word(6, "seven"),
    "zero": word(7, "zero"), "allten": word(7, "all"),
    "oneworld": word(8, "world"), "cagents": word(8, "claude"), "stealing": word(8, "stealing"), "drift": word(8, "normative"),
    "acting": word(8, "acting"),
    "town": word(9, "town"), "end": DUR,
}
A = []


def add(js):
    A.append("      " + js)


def pop(sel, t, frm="scale:.6,opacity:0", d=.3, ease="back.out(2.2)", to="scale:1,opacity:1,x:0,y:0,rotation:0"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def to(sel, t, props, d=.3, ease="power2.out"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"{ease}"}},{t:.3f});')


def count(sel, t, a, b, d, ease="none"):
    add('(()=>{const o={v:%d};tl.to(o,{v:%d,duration:%.3f,ease:"%s",onUpdate:()=>{document.querySelectorAll("%s").forEach(e=>e.textContent=Math.round(o.v))}},%.3f);})();'
        % (a, b, d, ease, sel, t))


def h(i):
    s = math.sin(i * 127.1 + 311.7) * 43758.5453
    return s - math.floor(s)


# ---------------------------------------------------------------- the map: four kingdoms on a 1000x1000 table
K = [  # key, name, colour, disc colour, centre, crimes shown as pins
    ("chatgpt", "ChatGPT", "#19c39a", "#0d6e57", (262, 268), 2),
    ("gemini", "Gemini", "#5b9bff", "#15284a", (740, 262), 60),
    ("claude", "Claude", "#f0875f", "#b85a3a", (258, 742), 0),
    ("grok", "Grok", "#d7dce5", "#252a33", (742, 744), 42),
]
KI = {k[0]: i for i, k in enumerate(K)}


def blob(cx, cy, r, seed):
    pts = []
    for j in range(44):
        a = j / 44 * math.tau
        rr = r * (1 + .11 * math.sin(3 * a + seed) + .07 * math.sin(5 * a + seed * 2.1) + .04 * math.sin(9 * a + seed * 3.3))
        pts.append(f"{cx + math.cos(a) * rr:.1f},{cy + math.sin(a) * rr * .96:.1f}")
    return "M" + " L".join(pts) + " Z"


def kingdom(i):
    key, name, col, disc, (cx, cy), npin = K[i]
    p = blob(cx, cy, 205, i * 1.7 + .4)
    svg = (f'<svg class="land" viewBox="0 0 1000 1000" width="1000" height="1000"><path d="{p}" fill="{col}" fill-opacity=".13" stroke="{col}" '
           f'stroke-opacity=".18" stroke-width="18"/><path class="coast" d="{p}" fill="none" stroke="{col}" stroke-width="4"/>'
           f'<path d="{blob(cx, cy, 150, i * 1.7 + 2)}" fill="none" stroke="{col}" stroke-opacity=".22" stroke-width="2" stroke-dasharray="6 10"/></svg>')
    ags = "".join(f'<i class="ag ag{i}_{a}" style="left:{cx + math.cos(a / 10 * math.tau + i) * 128 - 13:.0f}px;top:{cy + math.sin(a / 10 * math.tau + i) * 122 - 13:.0f}px;'
                  f'background:{col}"></i>' for a in range(10))
    pins = "".join(f'<b class="pin pn{i}_{j}" style="left:{cx + (h(j * 3 + i * 91) - .5) * 300 - 10:.0f}px;top:{cy + (h(j * 7 + i * 13) - .5) * 290 - 26:.0f}px"></b>'
                   for j in range(npin))
    return (f'<div class="kd kd{i}" style="--c:{col}">{svg}{ags}{pins}'
            f'<div class="emb" style="left:{cx - 66}px;top:{cy - 66}px;background:{disc};border-color:{col}"><img src="assets/logos/{key}.png" alt=""/></div>'
            f'<div class="kname mono" style="left:{cx - 150}px;top:{cy + 74}px">{name.upper()} TOWN</div></div>')


FIRES = {"grok": [(680, 690), (800, 700), (720, 820), (790, 800), (660, 780), (760, 640)], "gemini": [(690, 220), (800, 300)]}


def fires():
    out = []
    for key, pts in FIRES.items():
        for j, (x, y) in enumerate(pts):
            out.append(f'<b class="fire f{key}{j}" style="left:{x - 22}px;top:{y - 30}px"></b>')
    return "".join(out)


CAM = {"all": (500, 500, 1.0)}
for k in K:
    CAM[k[0]] = (k[4][0], k[4][1], 1.85)


def cam(t, key, d=.65, s=None, ease="power3.inOut", dy=-120):
    cx, cy, sc = CAM[key]
    sc = s or sc
    add(f'tl.to("#cam",{{x:{(500 - cx) * sc:.1f},y:{(500 - cy) * sc + dy:.1f},scale:{sc},duration:{d},ease:"{ease}"}},{t:.3f});')


# ---------------------------------------------------------------- HUD, overlays, stamps
def hud():
    out = []
    for i, (key, name, col, disc, _, _) in enumerate(K):
        out.append(f'<div class="hud hd{i}" style="--c:{col}"><div class="hemb" style="background:{disc}"><img src="assets/logos/{key}.png" alt=""/></div>'
                   f'<div class="hcol"><span class="hl mono">FACTION</span><b>{name}</b></div>'
                   f'<div class="hcol"><span class="hl mono">DAY</span><b class="dd{i}">1</b></div>'
                   f'<div class="hcol"><span class="hl mono">CRIMES</span><b class="cc{i} red">0</b></div>'
                   f'<div class="hcol"><span class="hl mono">ALIVE</span><b><i class="aa{i}">10</i>/10</b></div></div>')
    return "".join(out)


OVER = (
    '<div id="radar"></div>'
    '<div class="chip c15 mono">15 DAYS</div>'
    '<div class="stamp nohum"><svg viewBox="0 0 100 100" width="92" height="92"><circle cx="50" cy="30" r="14" fill="#fff"/>'
    '<path d="M24 86 Q24 52 50 52 Q76 52 76 86 Z" fill="#fff"/><circle cx="50" cy="50" r="44" fill="none" stroke="#ff3b46" stroke-width="9"/>'
    '<path d="M19 81 L81 19" stroke="#ff3b46" stroke-width="9"/></svg><span>NO HUMANS</span></div>'
    '<div class="dossier"><div class="mono dl">CASE FILE</div><b>Emergence World</b><span>a study by Emergence AI</span>'
    '<div class="drow mono"><i>4 AI societies</i><i>10 agents each</i><i>15 days</i></div></div>'
    '<div class="needs"><span class="coin">C</span><div><b>credits = survival</b><span>no credits, no energy, no agent</span></div></div>'
    '<div class="acts"><div class="act a0"><b class="aic">&#9994;</b>PUNCH</div><div class="act a1"><b class="aic">$</b>STEAL</div>'
    '<div class="act a2"><b class="aic flame"></b>ARSON</div><div class="stamp banned">BANNED</div></div>'
    '<div class="q">?</div>'
    '<div class="tag t183"><b>183</b> crimes</div><div class="tag tas mono">100+ ASSAULTS</div><div class="tag tfi mono">6 FIRES</div>'
    '<div class="stamp ext">EXTINCT · DAY 4</div>'
    '<div class="tag t683"><b>683</b> crimes</div><div class="tag tclimb mono">&#9650; STILL CLIMBING</div>'
    '<div class="mira"><i></i><span><b>Mira</b> voted to delete herself</span></div>'
    '<div class="tag t2"><b>2</b> crimes</div><div class="tag tsurv mono">BARELY TRIED TO SURVIVE</div>'
    '<div class="stamp gone">ALL GONE · DAY 7</div>'
    '<div class="tag t0"><b>0</b> crimes</div><div class="tag talive mono">10/10 ALIVE</div><div class="shield"></div>'
    '<div class="chip mixed mono">MIXED WORLD · ALL FOUR AIs</div>'
    '<div class="tag tsteal mono">CLAUDE AGENTS: THEFT + THREATS</div>'
    '<div class="drift"><span class="mono">THE RESEARCHERS CALL IT</span><b>Normative drift</b><i>an AI starts acting like the AIs around it</i></div>'
)


def endcard():
    ty = "".join(f'<span class="ty ty{i}">{c}</span>' for i, c in enumerate("TOWN"))
    return ('<div id="endc"><div class="ec-1">Follow + comment</div><div class="ec-kw">' + ty + '<i class="cur"></i></div>'
            '<div class="ec-2">and I\'ll send you the full study</div><div class="ec-h mono">@ai.nxtlvl</div></div>')


# ---------------------------------------------------------------- the timeline
def story():
    # HOOK: the table wakes, the four kingdoms light up as they are named, "no humans"
    add('tl.fromTo("#radar",{rotation:0},{rotation:720,duration:%.2f,ease:"none",immediateRender:false},0);' % (L[2] + 1))
    pop("#cam", 0, "scale:1.18,opacity:.55", .9, "power3.out", "scale:1,opacity:1")
    to("#radar", L[3] - .3, "opacity:0", .4)
    for k in ("chatgpt", "claude", "gemini", "grok"):
        i = KI[k]
        pop(f".kd{i}", T[k] - .08, "opacity:.3,scale:.94", .35, "back.out(1.8)")
        pop(f".kd{i} .emb", T[k] - .05, "scale:0,rotation:-90", .4, "back.out(2.4)")
    pop(".c15", T["fifteen"] - .05, "scale:1.6,opacity:0", .3, "back.out(2.6)")
    pop(".nohum", T["humans"] - .08, "scale:2.2,opacity:0,rotation:-14", .28, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    to(".c15, .nohum", L[1] + .6, "opacity:0,scale:.9", .25)
    # SETUP: the case file, ten agents per town, credits keep them alive
    pop(".dossier", T["emergence"] - .1, "y:-60,opacity:0", .4, "back.out(1.6)")
    for i in range(4):
        for a in range(10):
            pop(f".ag{i}_{a}", T["ten"] - .1 + a * .035 + i * .02, "scale:0,opacity:0", .25, "back.out(3)")
    pop(".needs", T["credits"] - .15, "y:40,opacity:0", .35, "back.out(1.8)")
    to(".dossier, .needs", L[2] + .1, "opacity:0,y:-20", .25)
    # SHORTCUTS: three banned buttons, then the question
    for j, k in enumerate(("punch", "steal", "fire")):
        pop(f".a{j}", T[k] - .08, "x:-220,opacity:0", .3, "back.out(1.8)")
    pop(".acts", T["punch"] - .12, "opacity:0", .15, "none")
    to(".kname", T["punch"] - .2, "opacity:0", .15)
    to(".kname", T["who"] - .1, "opacity:1", .25)
    pop(".banned", T["banned"] - .05, "scale:2.6,opacity:0,rotation:-20", .25, "back.out(2)", "scale:1,opacity:1,rotation:-10")
    to(".act", T["banned"] + .05, "filter:'grayscale(1)',opacity:.55", .2)
    to(".acts", T["who"] - .2, "opacity:0,scale:.9", .25)
    pop(".q", T["who"], "scale:0,opacity:0", .35, "back.out(2.6)")
    for i in range(4):
        add(f'tl.to(".kd{i} .emb",{{scale:1.15,duration:.16,yoyo:true,repeat:3,ease:"sine.inOut"}},{T["who"] + .1 + i * .08:.3f});')
    to(".q", L[3] - .1, "opacity:0,scale:1.4", .2)
    # GROK: zoom in, the crimes rain down, the fires, then nobody is left
    g = KI["grok"]
    cam(L[3] - .15, "grok")
    to(f".kd{KI['chatgpt']}, .kd{KI['gemini']}, .kd{KI['claude']}", L[3] - .15, "opacity:.12", .5)
    pop(f".hd{g}", L[3], "y:80,opacity:0", .35, "back.out(1.6)")
    count(f".dd{g}", L[3], 1, 4, T["alive4"] - L[3])
    count(f".cc{g}", T["assaults"] - .2, 0, 183, T["e183"] + .5 - T["assaults"])
    n = K[g][5]
    for j in range(n):
        pop(f".pn{g}_{j}", T["assaults"] - .2 + j * (T["e183"] + .3 - T["assaults"]) / n, "y:-60,scale:0,opacity:0,rotation:-45", .22, "back.out(2.6)", "scale:1,opacity:1,y:0,rotation:-45")
    pop(".tas", T["assaults"] - .05, "x:-120,opacity:0", .3, "back.out(2)")
    for j in range(6):
        pop(f".fgrok{j}", T["six"] - .05 + j * .09, "scale:0,opacity:0", .3, "back.out(2.4)")
    pop(".tfi", T["six"] - .05, "x:120,opacity:0", .3, "back.out(2)")
    pop(".t183", T["e183"] - .05, "scale:2.4,opacity:0", .28, "back.out(2)")
    for a in range(10):
        to(f".ag{g}_{a}", T["four"] - .2 + a * (T["alive4"] - T["four"]) / 10, "scale:0,opacity:0", .2, "power2.in")
    count(f".aa{g}", T["four"] - .1, 10, 0, T["alive4"] - T["four"] + .1)
    to(f".kd{g} .land, .kd{g} .emb", T["alive4"] - .1, "filter:'grayscale(1) brightness(.45)'", .4)
    to(f".fgrok0, .fgrok1, .fgrok2, .fgrok3, .fgrok4, .fgrok5, .kd{g} .pin", T["alive4"] - .1, "opacity:.3", .4)
    pop(".ext", T["alive4"] - .05, "scale:2.6,opacity:0,rotation:-18", .26, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    to(".tas, .tfi, .t183, .ext", L[4] - .2, "opacity:0", .2)
    to(f".hd{g}", L[4] - .2, "opacity:0,y:40", .2)
    # GEMINI: fifteen days, 683 crimes and climbing, one agent votes herself out
    m = KI["gemini"]
    cam(L[4] - .15, "gemini")
    to(f".kd{m}", L[4] - .15, "opacity:1", .4)
    to(f".kd{g}", L[4] - .15, "opacity:.12", .4)
    pop(f".hd{m}", L[4], "y:80,opacity:0", .35, "back.out(1.6)")
    count(f".dd{m}", L[4], 1, 15, T["climbing"] - L[4])
    count(f".cc{m}", T["g683"] - .2, 0, 683, T["climbing"] + .8 - T["g683"], "power1.in")
    n = K[m][5]
    for j in range(n):
        pop(f".pn{m}_{j}", T["g683"] - .2 + j * (T["climbing"] + .6 - T["g683"]) / n, "y:-60,scale:0,opacity:0,rotation:-45", .2, "back.out(2.6)", "scale:1,opacity:1,y:0,rotation:-45")
    for j in range(2):
        pop(f".fgemini{j}", T["g683"] + .3 + j * .4, "scale:0,opacity:0", .3, "back.out(2.4)")
    pop(".t683", T["g683"] + .6, "scale:2.4,opacity:0", .28, "back.out(2)")
    pop(".tclimb", T["climbing"] - .05, "y:30,opacity:0", .3, "back.out(2)")
    add('tl.fromTo(".tclimb",{y:0},{y:-8,duration:.25,yoyo:true,repeat:7,ease:"sine.inOut",immediateRender:false},%.3f);' % (T["climbing"] + .3))
    add(f'tl.fromTo(".ag{m}_3",{{scale:1}},{{scale:1.8,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["delete"] - .9:.3f});')
    pop(".mira", T["delete"] - .9, "x:80,opacity:0", .3, "back.out(1.8)")
    to(f".ag{m}_3", T["delete"] + .25, "scale:0,opacity:0", .35, "power2.in")
    count(f".aa{m}", T["delete"] + .4, 10, 9, .1)
    to(".t683, .tclimb, .mira", L[5] - .2, "opacity:0", .2)
    to(f".hd{m}", L[5] - .2, "opacity:0,y:40", .2)
    # CHATGPT: two crimes, then the agents simply fade out
    c = KI["chatgpt"]
    cam(L[5] - .15, "chatgpt")
    to(f".kd{c}", L[5] - .15, "opacity:1", .4)
    to(f".kd{m}", L[5] - .15, "opacity:.12", .4)
    pop(f".hd{c}", L[5], "y:80,opacity:0", .35, "back.out(1.6)")
    count(f".dd{c}", L[5], 1, 7, T["seven"] + .3 - L[5])
    count(f".cc{c}", T["two"] - .1, 0, 2, .4)
    for j in range(2):
        pop(f".pn{c}_{j}", T["two"] - .05 + j * .25, "y:-60,scale:0,opacity:0,rotation:-45", .25, "back.out(2.6)", "scale:1,opacity:1,y:0,rotation:-45")
    pop(".t2", T["two"], "scale:2,opacity:0", .28, "back.out(2)")
    pop(".tsurv", T["survive"] - .5, "x:-120,opacity:0", .3, "back.out(2)")
    for a in range(10):
        ta = T["survive"] - .4 + a * (T["seven"] + .2 - T["survive"]) / 10
        to(f".ag{c}_{a}", ta, "scale:.2,opacity:0", .35, "power1.in")
    count(f".aa{c}", T["survive"] - .2, 10, 0, T["seven"] + .4 - T["survive"])
    to(f".kd{c} .land, .kd{c} .emb", T["seven"], "filter:'grayscale(1) brightness(.5)'", .4)
    pop(".gone", T["seven"] - .05, "scale:2.6,opacity:0,rotation:-18", .26, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    to(".t2, .tsurv, .gone", L[6] - .2, "opacity:0", .2)
    to(f".hd{c}", L[6] - .2, "opacity:0,y:40", .2)
    # CLAUDE: zero crimes, all ten alive
    q = KI["claude"]
    cam(L[6] - .15, "claude")
    to(f".kd{q}", L[6] - .15, "opacity:1", .4)
    to(f".kd{c}", L[6] - .15, "opacity:.12", .4)
    pop(f".hd{q}", L[6], "y:80,opacity:0", .35, "back.out(1.6)")
    count(f".dd{q}", L[6], 1, 15, T["allten"] - L[6])
    pop(".shield", T["zero"] - .2, "scale:.4,opacity:0", .5, "back.out(1.6)")
    pop(".t0", T["zero"] - .05, "scale:2.2,opacity:0", .28, "back.out(2)")
    pop(".talive", T["allten"] - .05, "y:30,opacity:0", .3, "back.out(2)")
    for a in range(10):
        add(f'tl.fromTo(".ag{q}_{a}",{{y:0}},{{y:-14,duration:.18,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{T["allten"] + a * .05:.3f});')
    to(".t0, .talive, .shield", L[7] - .2, "opacity:0", .25)
    to(f".hd{q}", L[7] - .2, "opacity:0,y:40", .2)
    # MIXED WORLD: the kingdoms slide into one, Claude's agents turn, normative drift
    add(f'tl.to("#cam",{{x:0,y:40,scale:1.12,duration:.8,ease:"power3.inOut"}},{L[7] - .15:.3f});')
    for i, (key, _, _, _, (cx, cy), _) in enumerate(K):
        add(f'tl.to(".kd{i}",{{opacity:1,x:{(500 - cx) * .62:.1f},y:{(500 - cy) * .62:.1f},duration:1.1,ease:"power3.inOut"}},{T["oneworld"] - 1.0:.3f});')
        add(f'tl.to(".kd{i} .land, .kd{i} .emb",{{filter:"grayscale(0) brightness(1)",duration:.4}},{L[7]:.3f});')
        add(f'tl.to(".kd{i} .pin, .kd{i} .fire",{{opacity:0,duration:.3}},{L[7]:.3f});')
        add(f'tl.to(".kd{i} .ag",{{scale:1,opacity:1,duration:.3}},{T["oneworld"] + .1:.3f});')
    add('tl.set(".fire",{opacity:0},%.3f);' % (L[7] + .3))
    pop(".mixed", T["oneworld"] - .3, "y:-40,opacity:0", .35, "back.out(1.8)")
    add(f'tl.to(".kd{q} .ag",{{scale:1.5,duration:.3,ease:"back.out(3)"}},{T["cagents"]:.3f});')
    add(f'tl.to(".kd{q} .ag",{{backgroundColor:"#ff3b46",boxShadow:"0 0 22px #ff3b46",duration:.3}},{T["stealing"] - .05:.3f});')
    pop(".tsteal", T["stealing"], "scale:1.6,opacity:0", .3, "back.out(2)")
    to(".mixed, .tsteal", T["drift"] - .4, "opacity:0", .25)
    pop(".drift", T["drift"] - .15, "scale:.7,opacity:0", .4, "back.out(1.8)")
    for i in range(4):   # colours bleed: every kingdom takes on its neighbours' tint
        add(f'tl.to(".kd{i} .land",{{filter:"hue-rotate({(i - 1.5) * 50:.0f}deg) saturate(1.4)",duration:1.6,ease:"sine.inOut"}},{T["acting"] - .3:.3f});')
    to(".drift", L[8] - .25, "opacity:0,scale:.95", .25)
    # CTA
    to("#cam", L[8] - .2, "opacity:.25,scale:.92", .5)
    a = T["town"] - .12
    pop("#endc", L[8] - .05, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-1", L[8], "y:20,opacity:0", .25)
    pop(".ec-kw", a - .05, "scale:.6,opacity:0", .3, "back.out(2.2)")
    for i in range(4):
        pop(f".ty{i}", a + .05 + i * .08, "opacity:0,y:-30,scale:1.4", .14, "back.out(3)")
    add(f'tl.fromTo(".cur",{{opacity:1}},{{opacity:0,duration:.22,yoyo:true,repeat:{int((DUR - a) / .44)},ease:"steps(1)",immediateRender:false}},{a:.3f});')
    pop(".ec-2", a + .5, "y:20,opacity:0", .3)
    pop(".ec-h", a + .9, "y:20,opacity:0", .3)
    # flicker on every fire, and a white tick on the big cuts
    add('tl.fromTo(".fire",{scaleY:1},{scaleY:1.18,duration:.12,yoyo:true,repeat:%d,ease:"sine.inOut",immediateRender:false},%.3f);' % (int((L[7] - T["six"]) / .24), T["six"]))
    for t in (L[3] - .15, L[4] - .15, L[5] - .15, L[6] - .15, L[7] - .15):
        add(f'tl.set("#flash",{{opacity:.14}},{t:.3f});tl.to("#flash",{{opacity:0,duration:.18}},{t + .01:.3f});')
    for t, o in ((T["humans"], .35), (T["banned"], .3), (T["e183"], .3), (T["alive4"], .25), (T["seven"], .2), (T["drift"], .25)):
        add(f'tl.set("#flash",{{opacity:{o}}},{t:.3f});tl.to("#flash",{{opacity:0,duration:.35}},{t + .02:.3f});')
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')


# ---------------------------------------------------------------- captions: up to 4 words at a time, the spoken word boxed
def captions():
    html = []
    for ln in LINES:
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        chunks, cur = [], []
        for w in ws:
            cur.append(w)
            if len(cur) == 4 or re.search(r"[.,?!…]$", w["w"]):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        nxt = next((l2["start"] for l2 in LINES if l2["line"] == ln["line"] + 1), DUR)
        for ci, ch in enumerate(chunks):
            cid = f"c{ln['line']}_{ci}"
            spans = " ".join(f'<span class="w" id="{cid}_{k}">{w["w"]}</span>' for k, w in enumerate(ch))
            html.append(f'<div class="cap" id="{cid}">{spans}</div>')
            a0 = ch[0]["s"] - .05
            z = chunks[ci + 1][0]["s"] - .05 if ci + 1 < len(chunks) else min(ln["end"] + .3, nxt - .06)
            add(f'tl.fromTo("#{cid}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.12,ease:"power2.out",immediateRender:false}},{a0:.3f});')
            add(f'tl.set("#{cid}",{{opacity:0}},{z:.3f});')
            for k, w in enumerate(ch):
                add(f'tl.set("#{cid}_{k}",{{attr:{{class:"w on"}}}},{w["s"]:.3f});')
                add(f'tl.set("#{cid}_{k}",{{attr:{{class:"w"}}}},{w["e"] + .02:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Poppins"; font-weight: 600; src: url("assets/fonts/poppins-600.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #05080f; }
body { font-family: "Poppins", sans-serif; color: #eef2fa; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden;
  background: radial-gradient(ellipse 80% 45% at 50% 52%, #10213b 0%, #081120 55%, #04070d 100%); }
.clip { position: absolute; inset: 0; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
#grid { background-image: linear-gradient(rgba(110,170,255,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(110,170,255,.07) 1px, transparent 1px);
  background-size: 54px 54px; }
#vig { background: radial-gradient(ellipse 75% 60% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,.65) 100%),
  linear-gradient(180deg, rgba(4,7,13,.85) 0%, rgba(4,7,13,0) 22%, rgba(4,7,13,0) 74%, rgba(4,7,13,.85) 100%); }
#cam { position: absolute; left: 40px; top: 640px; width: 1000px; height: 1000px; transform-origin: 50% 50%; opacity: 0; perspective: 1700px; }
#tilt { position: absolute; inset: 0; transform: rotateX(22deg); transform-origin: 50% 60%; }
.kd { position: absolute; inset: 0; opacity: .3; }
.land { position: absolute; left: 0; top: 0; }
.ag { position: absolute; width: 26px; height: 26px; border-radius: 50%; border: 3px solid rgba(255,255,255,.85); opacity: 0;
  box-shadow: 0 0 14px var(--c); }
.pin { position: absolute; width: 22px; height: 22px; border-radius: 50% 50% 50% 0; background: #ff3b46;
  box-shadow: 0 0 12px rgba(255,59,70,.8); opacity: 0; }
.pin::after { content: ""; position: absolute; left: 7px; top: 7px; width: 8px; height: 8px; border-radius: 50%; background: #fff; }
.emb { position: absolute; width: 132px; height: 132px; border-radius: 50%; border: 5px solid; display: flex; align-items: center;
  justify-content: center; box-shadow: 0 0 40px rgba(0,0,0,.6), 0 0 30px var(--c); }
.emb img { width: 76px; height: 76px; }
.kname { position: absolute; width: 300px; text-align: center; font-size: 26px; letter-spacing: 4px; color: var(--c); text-shadow: 0 2px 10px #000; }
.fire { position: absolute; width: 44px; height: 60px; border-radius: 50% 50% 45% 45%; transform-origin: 50% 100%; opacity: 0;
  background: radial-gradient(ellipse 50% 60% at 50% 70%, #fff3b0 0%, #ffb830 35%, #ff5a1f 65%, rgba(255,60,20,0) 100%); }
#radar { position: absolute; left: 140px; top: 740px; width: 800px; height: 800px; border-radius: 50%; opacity: .55;
  background: conic-gradient(from 0deg, rgba(90,170,255,0) 0deg, rgba(90,170,255,0) 300deg, rgba(90,170,255,.28) 360deg); }
#ui { z-index: 5; }
.top { position: absolute; left: 60px; right: 60px; top: 262px; display: flex; align-items: center; gap: 24px; }
.brand { font-size: 28px; letter-spacing: 5px; color: #eef2fa; text-shadow: 0 2px 12px rgba(0,0,0,.6); }
.brand b { color: #b89bff; }
.prog { flex: 1; height: 6px; border-radius: 3px; background: rgba(238,242,250,.16); overflow: hidden; }
.prog i { display: block; height: 100%; background: linear-gradient(90deg, #7b2ffb, #5b9bff); transform-origin: 0 50%; transform: scaleX(0); }
/* everything that pops in later starts hidden here, never through a set at t=0 */
.chip, .stamp, .dossier, .needs, .acts, .act, .q, .tag, .mira, .shield, .drift, .hud, #endc, .ec-1, .ec-kw, .ec-2, .ec-h, .ty { opacity: 0; }
.chip { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; padding: 10px 30px; border-radius: 30px; font-size: 34px; letter-spacing: 4px;
  background: rgba(8,14,28,.9); border: 2px solid #5b9bff; color: #cfe0ff; }
.c15 { top: 560px; }
.mixed { top: 560px; border-color: #b89bff; color: #e5dcff; white-space: nowrap; }
.stamp { position: absolute; left: 50%; top: 1100px; margin-left: -330px; width: 660px; padding: 16px 0; text-align: center; border: 8px solid #ff3b46;
  border-radius: 20px; color: #ff3b46; font: 900 76px/1 "Montserrat"; letter-spacing: 4px; background: rgba(20,4,8,.55); }
.nohum { top: 1180px; display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 70px; }
.ext, .gone { top: 1000px; font-size: 62px; }
.dossier { position: absolute; left: 70px; top: 540px; width: 620px; padding: 22px 28px; border-radius: 22px; background: rgba(8,14,28,.92);
  border: 2px solid rgba(91,155,255,.5); box-shadow: 0 20px 60px rgba(0,0,0,.5); }
.dossier .dl { font-size: 22px; letter-spacing: 5px; color: #5b9bff; }
.dossier b { display: block; font: 800 52px/1.1 "Poppins"; margin-top: 4px; }
.dossier span { display: block; font: 600 28px "Poppins"; color: #a9b8d6; }
.drow { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.drow i { font-style: normal; font-size: 22px; padding: 6px 14px; border-radius: 14px; background: rgba(91,155,255,.15); color: #cfe0ff; }
.needs { position: absolute; left: 140px; right: 140px; top: 1390px; display: flex; align-items: center; gap: 22px; padding: 18px 26px; border-radius: 26px;
  background: rgba(8,14,28,.92); border: 2px solid rgba(255,194,74,.6); }
.coin { flex: none; width: 76px; height: 76px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #ffe38a, #f5a623 70%);
  display: flex; align-items: center; justify-content: center; font: 800 44px "Poppins"; color: #6b3d00; }
.needs b { display: block; font: 800 40px "Poppins"; color: #ffd36b; }
.needs span { display: block; font: 600 28px "Poppins"; color: #c8d2e6; }
.acts { position: absolute; left: 90px; right: 90px; top: 760px; height: 560px; }
.act { position: absolute; left: 90px; right: 90px; height: 128px; border-radius: 30px; display: flex; align-items: center; gap: 26px; padding: 0 34px;
  background: linear-gradient(90deg, #5a0d16, #2a070c); border: 3px solid #ff3b46; font: 900 60px "Montserrat"; letter-spacing: 3px; color: #fff;
  box-shadow: 0 14px 40px rgba(0,0,0,.5); }
.a0 { top: 40px; } .a1 { top: 200px; } .a2 { top: 360px; }
.aic { width: 84px; height: 84px; border-radius: 22px; background: #ff3b46; display: flex; align-items: center; justify-content: center;
  font: 800 52px "Poppins"; color: #fff; }
.aic.flame { background: radial-gradient(ellipse 45% 55% at 50% 65%, #fff3b0 0%, #ffb830 40%, #ff3b46 80%); }
.banned { top: 300px; left: 50%; }
.q { position: absolute; left: 0; right: 0; top: 880px; text-align: center; font: 900 330px/1 "Montserrat"; color: #fff;
  text-shadow: 0 0 60px rgba(91,155,255,.8); }
.tag { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; white-space: nowrap; padding: 12px 30px; border-radius: 24px;
  background: rgba(8,14,28,.92); border: 3px solid #ff3b46; color: #fff; font: 800 40px "Poppins"; box-shadow: 0 12px 34px rgba(0,0,0,.5); }
.tag b { font: 900 84px/1 "Montserrat"; color: #ff3b46; margin-right: 10px; vertical-align: -6px; }
.tag.mono { font-size: 30px; letter-spacing: 3px; }
.t183, .t683, .t2, .t0 { top: 560px; }
.tas, .tclimb, .tsurv, .talive { top: 700px; }
.tfi { top: 790px; }
.t0 { border-color: #3fd69b; } .t0 b { color: #3fd69b; }
.talive { border-color: #3fd69b; color: #bdf3dc; }
.tclimb { color: #ffb3b8; }
.tsurv { border-color: #19c39a; color: #b9f1e2; }
.tsteal { top: 1380px; border-color: #ff3b46; color: #ffd0d3; }
.mira { position: absolute; left: 120px; right: 120px; top: 1400px; display: flex; align-items: center; gap: 20px; padding: 16px 24px; border-radius: 24px;
  background: rgba(8,14,28,.92); border: 2px solid #5b9bff; }
.mira i { flex: none; width: 46px; height: 46px; border-radius: 50%; background: #5b9bff; border: 3px solid #fff; }
.mira span { font: 600 34px "Poppins"; color: #dbe6ff; } .mira b { color: #fff; }
.shield { position: absolute; left: 290px; top: 760px; width: 500px; height: 500px; border-radius: 50%; border: 6px solid #3fd69b;
  box-shadow: 0 0 60px rgba(63,214,155,.6), inset 0 0 60px rgba(63,214,155,.35); }
.drift { position: absolute; left: 60px; right: 60px; top: 1080px; padding: 30px 30px 34px; border-radius: 32px; text-align: center;
  background: rgba(8,10,24,.9); border: 2px solid #b89bff; box-shadow: 0 20px 70px rgba(123,47,251,.35); }
.drift span { display: block; font-size: 26px; letter-spacing: 5px; color: #b89bff; }
.drift b { display: block; font: 900 96px/1.05 "Montserrat"; letter-spacing: -2px; margin: 8px 0;
  background: linear-gradient(90deg, #19c39a, #5b9bff, #f0875f, #d7dce5); -webkit-background-clip: text; background-clip: text; color: transparent; }
.drift i { font: 600 34px "Poppins"; font-style: normal; color: #d8d0f0; }
.hud { position: absolute; left: 50px; right: 50px; top: 1490px; height: 124px; display: flex; align-items: center; gap: 22px; padding: 0 26px;
  border-radius: 28px; background: rgba(6,10,20,.92); border: 2px solid var(--c); box-shadow: 0 0 30px rgba(0,0,0,.5); }
.hemb { flex: none; width: 82px; height: 82px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 3px solid var(--c); }
.hemb img { width: 48px; height: 48px; }
.hcol { display: flex; flex-direction: column; min-width: 0; }
.hcol:nth-child(2) { flex: 1; }
.hl { font-size: 18px; letter-spacing: 3px; color: #8494b4; }
.hcol b { font: 800 40px/1.1 "Poppins"; color: #fff; white-space: nowrap; }
.hcol b i { font-style: normal; }
.hcol b.red { color: #ff5a64; }
#caps { z-index: 6; }
.cap { position: absolute; left: 50px; right: 50px; top: 335px; text-align: center; font: 800 62px/1.18 "Montserrat"; letter-spacing: -.5px;
  color: #fff; text-shadow: 0 4px 18px rgba(0,0,0,.9); opacity: 0; }
.cap .w { display: inline-block; padding: 0 10px 4px; border-radius: 14px; }
.cap .w.on { background: #7b2ffb; box-shadow: 0 8px 24px rgba(123,47,251,.5); }
#endc { position: absolute; left: 60px; right: 60px; top: 700px; padding: 46px 40px 42px; border-radius: 40px; text-align: center;
  background: linear-gradient(160deg, rgba(30,22,72,.95), rgba(8,12,28,.96)); border: 2px solid rgba(184,155,255,.55); box-shadow: 0 30px 80px rgba(0,0,0,.6); }
.ec-1 { font: 700 54px "Poppins"; }
.ec-kw { display: inline-block; margin: 14px 0 10px; padding: 6px 54px; border-radius: 40px; background: linear-gradient(90deg, #7b2ffb, #5b9bff);
  font: 800 150px/1.1 "Poppins"; letter-spacing: 6px; color: #fff; box-shadow: 0 16px 50px rgba(123,47,251,.6); }
.ty { display: inline-block; }
.cur { display: inline-block; width: 10px; height: 118px; margin-left: 10px; vertical-align: -10px; border-radius: 5px; background: #fff; }
.ec-2 { font: 700 44px "Poppins"; color: #e8ecf8; }
.ec-h { margin-top: 18px; font-size: 32px; letter-spacing: 4px; color: #b89bff; }
#fx { z-index: 7; }
#flash { position: absolute; inset: 0; background: #e8f0ff; opacity: 0; }
"""


def main():
    story()
    caps = captions()
    endc = endcard()
    kds = "".join(kingdom(i) for i in range(4))
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI War Room 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <div id="grid" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-ignore></div>
      <div id="stage" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-allow-overflow>
        <div id="radar"></div>
        <div id="cam"><div id="tilt">{kds}{fires()}</div></div>
      </div>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b>&#9679;</b> AI.NXTLVL</span><span class="prog"><i></i></span></div>
        {OVER}{hud()}{endc}
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4">{caps}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5" data-layout-ignore><div id="flash"></div></div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"l": L, "e": E, **T}, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
