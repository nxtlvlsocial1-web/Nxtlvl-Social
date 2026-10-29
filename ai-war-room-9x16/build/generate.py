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
    "society": word(1, "society"), "tried": word(2, "tried"), "town2": word(2, "town"), "shortcuts": word(3, "shortcuts"),
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
    ("chatgpt", "ChatGPT", "#0f9e7a", "#10a37f", (262, 268), 2),
    ("gemini", "Gemini", "#3b78e7", "#1E1B18", (740, 262), 60),
    ("claude", "Claude", "#D45C40", "#D97757", (258, 742), 0),
    ("grok", "Grok", "#4a4540", "#1E1B18", (742, 744), 42),
]
KI = {k[0]: i for i, k in enumerate(K)}
LABEL = {"chatgpt": "#086b52", "gemini": "#2a5bb8", "claude": "#A8452F", "grok": "#3a3530"}   # 4.5:1+ on cream


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
    svg = (f'<svg class="land" viewBox="0 0 1000 1000" width="1000" height="1000"><path d="{p}" fill="{col}" fill-opacity=".16" stroke="#1E1B18" '
           f'stroke-opacity=".9" stroke-width="5" transform="translate(7 9)" opacity=".18"/><path d="{p}" fill="#FFFDF8" stroke="none"/>'
           f'<path class="coast" d="{p}" fill="{col}" fill-opacity=".2" stroke="{col}" stroke-width="5"/>'
           f'<path d="{blob(cx, cy, 150, i * 1.7 + 2)}" fill="none" stroke="{col}" stroke-opacity=".45" stroke-width="2.5" stroke-dasharray="8 10"/></svg>')
    ags = "".join(f'<i class="ag ag{i}_{a}" style="left:{cx + math.cos(a / 10 * math.tau + i) * 128 - 13:.0f}px;top:{cy + math.sin(a / 10 * math.tau + i) * 122 - 13:.0f}px;'
                  f'background:{col}"></i>' for a in range(10))
    pins = "".join(f'<b class="pin pn{i}_{j}" style="left:{cx + (h(j * 3 + i * 91) - .5) * 300 - 10:.0f}px;top:{cy + (h(j * 7 + i * 13) - .5) * 290 - 26:.0f}px"></b>'
                   for j in range(npin))
    hs = "".join(f'<b class="hs hs{i}_{j}" style="left:{cx + math.cos(math.radians(d)) * 94 - 15:.0f}px;top:{cy + math.sin(math.radians(d)) * 90 - 10:.0f}px"></b>'
                 for j, d in enumerate((160, 200, 240, 280, 320, 0)))   # houses ring the emblem but leave the town label below it clear
    ring = f'<i class="ring rg{i}" style="left:{cx - 70}px;top:{cy - 70}px;border-color:{col}"></i>'
    return (f'<div class="kd kd{i}" style="--c:{col}">{svg}{hs}{ags}{pins}{ring}'
            f'<div class="emb" style="left:{cx - 66}px;top:{cy - 66}px;background:{disc};border-color:{col}"><img src="assets/logos/{key}.png" alt=""/></div>'
            f'<div class="kname mono" style="left:{cx - 150}px;top:{cy + 74}px;color:{LABEL[key]}">{name.upper()} TOWN</div></div>')


ROUTES = [(0, 1), (1, 3), (3, 2), (2, 0), (0, 3), (1, 2), (1, 0), (2, 3)]   # town pairs the hook's messengers shuttle between


def route(j):
    a, b = (K[n][4] for n in ROUTES[j])
    dx, dy = b[0] - a[0], b[1] - a[1]
    u = math.hypot(dx, dy)
    return (a[0] + dx / u * 92, a[1] + dy / u * 92), (b[0] - dx / u * 92, b[1] - dy / u * 92)


def messengers():
    return "".join(f'<i class="msg ms{j}" style="background:{K[ROUTES[j][0]][2]}"></i>' for j in range(len(ROUTES)))


FIRES = {"grok": [(680, 690), (800, 700), (720, 820), (790, 800), (660, 780), (760, 640)], "gemini": [(690, 220), (800, 300)]}


def fires():
    out = [BURST.format(c=f"bst bs{j}").replace('width="104" height="104"', 'width="86" height="86"').replace('<svg ', f'<svg style="left:{742 + (h(j * 13 + 4) - .5) * 260 - 43:.0f}px;top:{744 + (h(j * 17 + 9) - .5) * 240 - 43:.0f}px" ')
           for j in range(8)]
    for key, pts in FIRES.items():
        for j, (x, y) in enumerate(pts):
            out.append(f'<b class="fire f{key}{j}" style="left:{x - 22}px;top:{y - 30}px"></b>')
    return "".join(out)


CAM = {"all": (500, 500, 1.0)}
for k in K:
    CAM[k[0]] = (k[4][0], k[4][1], 1.6)


def cam(t, key, d=.65, s=None, ease="power3.inOut", dy=-55):
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


BURST = ('<svg class="{c}" viewBox="0 0 100 100" width="104" height="104"><polygon points="'
         + " ".join(f"{50 + math.cos(j / 24 * math.tau) * (48 if j % 2 == 0 else 26):.1f},{50 + math.sin(j / 24 * math.tau) * (48 if j % 2 == 0 else 26):.1f}" for j in range(24))
         + '" fill="#F2B33D" stroke="#1E1B18" stroke-width="4"/><text x="50" y="58" text-anchor="middle" font-family="Manrope" font-weight="800" font-size="22" fill="#1E1B18">POW</text></svg>')

OVER = (
    '<div id="radar"></div>'
    '<div class="chip c15 mono"><span class="n15">1</span> DAYS</div>'
    '<div class="stamp nohum"><svg viewBox="0 0 100 100" width="92" height="92"><circle cx="50" cy="30" r="14" fill="#fff"/>'
    '<path d="M24 86 Q24 52 50 52 Q76 52 76 86 Z" fill="#fff"/><circle cx="50" cy="50" r="44" fill="none" stroke="#ff3b46" stroke-width="9"/>'
    '<path d="M19 81 L81 19" stroke="#ff3b46" stroke-width="9"/></svg><span>NO HUMANS</span></div>'
    '<div class="dossier"><div class="mono dl">CASE FILE</div><b>' + "".join(f'<em class="tl tl{k}">{c}</em>' if c != " " else " " for k, c in enumerate("Emergence World")) + '</b>'
    '<span>a study by Emergence AI</span>'
    '<div class="drow mono"><i>4 AI societies</i><i>10 agents each</i><i>15 days</i></div><i class="scan"></i></div>'
    '<div class="rs">REAL STUDY</div>'
    '<div class="needs"><span class="coin">C</span><div><b>credits = survival</b><span>no credits, no energy, no agent</span></div><em class="nbar"><i></i></em></div>'
    + "".join(f'<b class="fc fc{j}">C</b>' for j in range(8)) +
    '<div class="acts"><div class="act a0"><b class="aic">&#9994;</b>PUNCH</div><div class="act a1"><b class="aic">$</b>STEAL</div>'
    '<div class="act a2"><b class="aic flame"></b>ARSON</div>'
    '<div class="vg vg0"><i class="vbot vp-a"></i><b class="vp-f">&#9994;</b>' + BURST.format(c="vp-b") + '</div>'
    '<div class="vg vg1"><i class="vbot vs-a"></i><b class="vs-q">?</b><i class="vbot vs-t"></i><b class="vs-c">C</b></div>'
    '<div class="vg vg2"><b class="va-h"></b>' + "".join(f'<b class="vfl vf{j}"></b>' for j in range(3))
    + "".join(f'<i class="smk sk{j}"></i>' for j in range(4)) + '</div>'
    '<div class="stamp banned">BANNED</div></div>'
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
    to(".dossier", T["credits"] - .4, "opacity:0,y:-30", .22, "power2.in")
    pop(".needs", T["credits"] - .15, "y:40,opacity:0", .35, "back.out(1.8)")
    to(".needs", L[2] + .1, "opacity:0,y:-20", .25)
    # SHORTCUTS: three banned buttons, then the question
    for j, k in enumerate(("punch", "steal", "fire")):
        pop(f".a{j}", T[k] - (.5 if k == "fire" else .08), "x:-220,opacity:0", .3, "back.out(1.8)")
    pop(".acts", T["punch"] - .12, "opacity:0", .15, "none")
    pop(".banned", T["banned"] - .05, "scale:2.6,opacity:0,rotation:-20", .25, "back.out(2)", "scale:1,opacity:1,rotation:-10")
    to(".act, .vg", T["banned"] + .05, "filter:'grayscale(1)',opacity:.55", .2)
    to(".acts", T["who"] - .2, "opacity:0,scale:.9", .25)
    pop(".q", T["who"], "scale:0,opacity:0", .35, "back.out(2.6)")
    for i in range(4):
        add(f'tl.to(".kd{i} .emb",{{scale:1.15,duration:.16,yoyo:true,repeat:3,ease:"sine.inOut"}},{T["who"] + .1 + i * .08:.3f});')
    to(".q", L[3] - .1, "opacity:0,scale:1.4", .2)
    # GROK: zoom in, the crimes rain down, the fires, then nobody is left
    g = KI["grok"]
    cam(L[3] - .15, "grok")
    to(f".kd{KI['chatgpt']}, .kd{KI['gemini']}, .kd{KI['claude']}", L[3] - .15, "opacity:0", .5)
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
    to(f".kd{g}", L[4] - .15, "opacity:0", .4)
    to(".fgrok0, .fgrok1, .fgrok2, .fgrok3, .fgrok4, .fgrok5", L[4] - .15, "opacity:0", .3)
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
    to(f".kd{m}", L[5] - .15, "opacity:0", .4)
    to(".fgemini0, .fgemini1", L[5] - .15, "opacity:0", .3)
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
    to(f".kd{c}", L[6] - .15, "opacity:0", .4)
    pop(f".hd{q}", L[6], "y:80,opacity:0", .35, "back.out(1.6)")
    count(f".dd{q}", L[6], 1, 15, T["allten"] - L[6])
    pop(".shield", T["zero"] - .2, "scale:.4,opacity:0", .5, "back.out(1.6)")
    pop(".t0", T["zero"] - .05, "scale:2.2,opacity:0", .28, "back.out(2)")
    pop(".talive", T["allten"] - .05, "y:30,opacity:0", .3, "back.out(2)")
    for a in range(10):
        add(f'tl.fromTo(".ag{q}_{a}",{{scale:1}},{{scale:1.45,duration:.16,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{T["allten"] + a * .05:.3f});')
    to(".t0, .talive, .shield", L[7] - .2, "opacity:0", .25)
    to(f".hd{q}", L[7] - .2, "opacity:0,y:40", .2)
    # MIXED WORLD: the kingdoms slide into one, Claude's agents turn, normative drift
    add(f'tl.to("#cam",{{x:0,y:-10,scale:1.05,duration:.8,ease:"power3.inOut"}},{L[7] - .15:.3f});')
    for i, (key, _, _, _, (cx, cy), _) in enumerate(K):
        add(f'tl.to(".kd{i}",{{opacity:1,x:{(500 - cx) * .62:.1f},y:{(500 - cy) * .62:.1f},duration:1.1,ease:"power3.inOut"}},{T["oneworld"] - 1.0:.3f});')
        add(f'tl.to(".kd{i} .land, .kd{i} .emb",{{filter:"grayscale(0) brightness(1)",duration:.4}},{L[7]:.3f});')
        add(f'tl.to(".kd{i} .pin, .kd{i} .fire",{{opacity:0,duration:.3}},{L[7]:.3f});')
        add(f'tl.to(".kd{i} .ag",{{scale:1,opacity:1,duration:.3}},{T["oneworld"] + .1:.3f});')
    add('tl.set(".fire",{opacity:0},%.3f);' % (L[7] + .3))
    pop(".mixed", T["oneworld"] - .3, "y:-40,opacity:0", .35, "back.out(1.8)")
    to(".kname", T["oneworld"] - .4, "opacity:0", .25)
    add(f'tl.set(".kd{q}",{{zIndex:5}},{L[7]:.3f});')
    add(f'tl.to(".kd{q} .ag",{{scale:1.5,duration:.3,ease:"back.out(3)"}},{T["cagents"]:.3f});')
    add(f'tl.to(".kd{q} .ag",{{backgroundColor:"#D9483B",borderColor:"#1E1B18",duration:.3}},{T["stealing"] - .05:.3f});')
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
    hook_fx()
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')


# ---------------------------------------------------------------- the opening 22 s: something moves on every frame
def camk(t, x, y, sc, d, ease="power2.inOut"):
    add(f'tl.to("#cam",{{x:{x:.1f},y:{y:.1f},scale:{sc},duration:{d},ease:"{ease}"}},{t:.3f});')


def nudge(key, sc, y0, f=.2):
    cx, cy = K[KI[key]][4]
    return (500 - cx) * sc * f, (500 - cy) * sc * f + y0


def yoyo(sel, t0, t1, props, d, ease="sine.inOut"):
    """A there-and-back loop from t0 that always lands back on its start values before t1."""
    rep = max(1, int((t1 - t0) / d))
    rep -= 1 - rep % 2
    add(f'tl.fromTo("{sel}",{{x:0,y:0}},{{{props},duration:{d:.2f},yoyo:true,repeat:{rep},ease:"{ease}",immediateRender:false}},{t0:.3f});')


def hook_fx():
    end = L[3] - .3                       # Grok's chapter takes the camera over here
    # the camera never stops: a push in, a glance at each town as it is named, a pull back, a shake on "no humans"
    # the map lives in the lower part of the screen (y 900+) so the cards above never cover a town; the camera never stops
    add('tl.fromTo("#cam",{scale:1.15,x:0,y:80,opacity:.6},{scale:1.02,y:110,opacity:1,duration:1.65,ease:"power2.out",immediateRender:false},0);')
    for k, d in (("chatgpt", .24), ("claude", .24), ("gemini", .8), ("grok", .3)):
        camk(T[k] - .08, *nudge(k, 1.02, 110), 1.02, d, "power3.out")
    camk(T["society"] - .9, 0, 127, .95, 1.6)
    camk(T["fifteen"] - .1, 0, 130, .98, 1.3, "power1.inOut")
    for j, (dx, dy) in enumerate(((16, -10), (-18, 12), (12, 14), (-10, -14), (8, 6), (0, 0))):
        camk(T["humans"] - .02 + j * .045, dx, 130 + dy, .98, .045, "none")
    camk(T["humans"] + .3, 0, 127, .92, .5, "power2.out")
    camk(L[1] + .1, 0, 140, .94, 2.0)
    camk(T["town2"] - .95, 0, 127, .92, .5)
    camk(T["ten"] - .15, 0, 135, .96, .8, "power2.out")
    camk(T["credits"] - .95, 0, 127, .92, .55)
    camk(T["shortcuts"] - 1.1, 0, 140, .94, end - (T["shortcuts"] - 1.1) - .05, "sine.inOut")
    # ambient: the grid drifts, the SIMULATION light blinks, the emblems float
    add(f'tl.fromTo("#grid",{{backgroundPosition:"30px 0px"}},{{backgroundPosition:"30px 600px",duration:{DUR},ease:"none",immediateRender:false}},0);')
    add(f'tl.fromTo(".live b",{{opacity:1}},{{opacity:.15,duration:.45,yoyo:true,repeat:{int(DUR / .45)},ease:"sine.inOut",immediateRender:false}},0);')
    for k in ("chatgpt", "claude", "gemini", "grok"):
        i = KI[k]
        yoyo(f".kd{i} .emb", T[k] + .4, DUR - .1, "y:-7", .85 + i * .11)
    # each town rings out as it is named, and again on "each AI got its own town"
    for k in ("chatgpt", "claude", "gemini", "grok"):
        i = KI[k]
        add(f'tl.fromTo(".rg{i}",{{scale:.6,opacity:.9}},{{scale:2.2,opacity:0,duration:.7,ease:"power2.out",immediateRender:false}},{T[k] - .05:.3f});')
    for i in range(4):
        add(f'tl.fromTo(".rg{i}",{{scale:.6,opacity:.9}},{{scale:2.2,opacity:0,duration:.7,ease:"power2.out",immediateRender:false}},{L[1] + 2.2 + i * .2:.3f});')
        add(f'tl.fromTo(".kd{i} .emb",{{scale:1}},{{scale:1.12,duration:.12,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{L[1] + 2.2 + i * .2:.3f});')
    # "run their own society": houses go up in every town, messengers start running between them
    for i in range(4):
        for j in range(6):
            pop(f".hs{i}_{j}", T["society"] - .25 + i * .09 + j * .05, "y:-26,scale:0,opacity:0", .28, "back.out(2.6)")
    for j in range(len(ROUTES)):
        (ax, ay), (bx, by) = route(j)
        t0 = T["society"] + .3 + j * .12
        add(f'tl.fromTo(".ms{j}",{{opacity:0}},{{opacity:1,duration:.2,immediateRender:false}},{t0:.3f});')
        d = 1.1 + h(j * 5 + 2) * .6
        rep = max(1, int((end - .3 - t0) / d))
        rep -= 1 - rep % 2
        add(f'tl.fromTo(".ms{j}",{{x:{ax - 10:.0f},y:{ay - 10:.0f}}},{{x:{bx - 10:.0f},y:{by - 10:.0f},duration:{d:.2f},yoyo:true,repeat:{rep},ease:"sine.inOut",immediateRender:false}},{t0:.3f});')
        to(f".ms{j}", end - .3, "opacity:0", .2)
    # "fifteen days" counts up
    count(".n15", T["fifteen"] - .05, 1, 15, .55, "power2.out")
    # the case file types its title, a scan line reads it, a REAL STUDY stamp lands on "actually tried it"
    for k, c in enumerate("Emergence World"):
        if c != " ":
            pop(f".tl{k}", T["emergence"] + .05 + k * .035, "opacity:0,y:12", .12, "power2.out", "opacity:1,y:0")
    add(f'tl.fromTo(".scan",{{opacity:.8,y:0}},{{opacity:.8,y:250,duration:.7,repeat:1,ease:"none",immediateRender:false}},{T["emergence"] + .1:.3f});')
    to(".scan", T["emergence"] + 1.5, "opacity:0", .1)
    pop(".rs", T["tried"] - .05, "scale:2.4,opacity:0,rotation:-24", .26, "back.out(2)", "scale:1,opacity:1,rotation:-10")
    to(".rs", T["credits"] - .4, "opacity:0", .2)
    # ten agents each, and they start milling around their towns
    for i in range(4):
        for a in range(10):
            n = i * 10 + a
            yoyo(f".ag{i}_{a}", T["ten"] + .65 + h(n) * .3, DUR - .1, f"x:{(h(n * 3 + 1) - .5) * 22:.1f},y:{(h(n * 7 + 5) - .5) * 20:.1f}", .7 + h(n * 11) * .5)
    # "credits to stay alive": the energy bar drains, coins fly to each town, the bar refills
    add(f'tl.fromTo(".nbar i",{{scaleX:1}},{{scaleX:.18,duration:.55,ease:"power2.in",immediateRender:false}},{T["credits"] - .05:.3f});')
    tgt = [(328, 1076), (752, 1076), (314, 1468), (768, 1468)]   # the emblems at the resting camera (scale .92, y 127)
    for j in range(8):
        tx, ty = tgt[j % 4]
        dx, dy = tx - 137, ty - 505
        t0 = T["credits"] + .25 + j * .07
        add(f'tl.fromTo(".fc{j}",{{x:0,y:0,opacity:0,scale:.6}},{{keyframes:[{{x:{dx * .5:.0f},y:{min(dy * .5, 0) - 160:.0f},opacity:1,scale:1.1,duration:.28,ease:"power1.out"}},'
            f'{{x:{dx},y:{dy},scale:.5,duration:.28,ease:"power1.in"}},{{opacity:0,duration:.06}}],immediateRender:false}},{t0:.3f});')
    for i in range(4):
        add(f'tl.fromTo(".kd{i} .emb",{{scale:1}},{{scale:1.14,duration:.1,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{T["credits"] + .78 + i * .07:.3f});')
    add(f'tl.to(".nbar i",{{scaleX:1,duration:.4,ease:"back.out(2)"}},{T["credits"] + .85:.3f});')
    # the three shortcuts act themselves out: a punch lands, a coin gets lifted, a house burns
    p0 = T["punch"]
    pop(".vg0", p0 - .1, "x:120,opacity:0", .28, "back.out(1.8)")
    pop(".vp-a", p0 - .05, "scale:0,opacity:0", .2, "back.out(3)")
    add(f'tl.fromTo(".vp-f",{{x:0,opacity:0}},{{keyframes:[{{opacity:1,duration:.05}},{{x:196,duration:.17,ease:"power3.in"}},{{x:150,duration:.3,ease:"power2.out"}}],immediateRender:false}},{p0 + .1:.3f});')
    pop(".vp-b", p0 + .31, "scale:0,opacity:0,rotation:-30", .16, "back.out(3)", "scale:1,opacity:1,rotation:0")
    to(".vp-b", p0 + .6, "scale:.6,opacity:0", .2)
    add(f'tl.fromTo(".vp-a",{{x:0,rotation:0}},{{x:84,rotation:40,duration:.35,ease:"power2.out",immediateRender:false}},{p0 + .32:.3f});')
    add(f'tl.fromTo(".vg0",{{y:0}},{{y:6,duration:.04,yoyo:true,repeat:5,ease:"none",immediateRender:false}},{p0 + .32:.3f});')
    s0 = T["steal"]
    pop(".vg1", s0 - .1, "x:120,opacity:0", .28, "back.out(1.8)")
    pop(".vs-a, .vs-c", s0 - .05, "scale:0,opacity:0", .2, "back.out(3)")
    add(f'tl.fromTo(".vs-t",{{x:0,opacity:0}},{{keyframes:[{{opacity:1,duration:.05}},{{x:-210,duration:.22,ease:"power3.out"}}],immediateRender:false}},{s0 + .05:.3f});')
    add(f'tl.fromTo(".vs-c",{{x:0,y:0}},{{keyframes:[{{x:65,y:-30,duration:.12,ease:"power1.out"}},{{x:130,y:0,duration:.12,ease:"power1.in"}},{{x:380,duration:.3,ease:"power2.in"}}],immediateRender:false}},{s0 + .3:.3f});')
    add(f'tl.to(".vs-t",{{x:40,duration:.3,ease:"power2.in"}},{s0 + .54:.3f});')
    pop(".vs-q", s0 + .7, "scale:0,opacity:0,y:10", .22, "back.out(3)", "scale:1,opacity:1,y:0")
    add(f'tl.fromTo(".vs-a",{{x:0}},{{x:-5,duration:.05,yoyo:true,repeat:5,ease:"none",immediateRender:false}},{s0 + .7:.3f});')
    f0 = T["fire"]
    pop(".vg2", f0 - .5, "x:120,opacity:0", .28, "back.out(1.8)")
    pop(".va-h", f0 - .45, "scale:0,opacity:0,y:-20", .25, "back.out(2.4)")
    for j in range(3):
        pop(f".vf{j}", f0 - .05 + j * .12, "scale:0,opacity:0", .25, "back.out(2.4)")
    add(f'tl.fromTo(".vfl",{{scaleY:1}},{{scaleY:1.22,duration:.11,yoyo:true,repeat:{int((T["who"] - f0) / .22)},ease:"sine.inOut",immediateRender:false}},{f0 + .3:.3f});')
    add(f'tl.to(".va-h",{{backgroundColor:"#3a3530",duration:.5}},{f0 + .2:.3f});')
    for j in range(4):
        add(f'tl.fromTo(".sk{j}",{{y:0,scale:.5,opacity:0}},{{keyframes:[{{opacity:.7,duration:.15}},{{y:-70,scale:1.6,opacity:0,duration:.75,ease:"power1.out"}}],repeat:2,immediateRender:false}},{f0 + .15 + j * .22:.3f});')
    # Grok's assaults land as POW bursts across the town
    for j in range(8):
        t0 = T["assaults"] - .15 + j * (T["e183"] - T["assaults"] + .2) / 8
        pop(f".bs{j}", t0, "scale:0,opacity:0,rotation:-40", .16, "back.out(3)", "scale:1,opacity:1,rotation:0")
        to(f".bs{j}", t0 + .4, "scale:.5,opacity:0", .2)
    # Claude's shield rings out on "zero" and "all ten"
    for t in (T["zero"] - .05, T["allten"] - .05):
        add(f'tl.fromTo(".rg{KI["claude"]}",{{scale:.6,opacity:.9}},{{scale:2.2,opacity:0,duration:.7,ease:"power2.out",immediateRender:false}},{t:.3f});')
    # "but there were shortcuts": the red alert frame pulses
    add(f'tl.fromTo("#alert",{{opacity:0}},{{opacity:.85,duration:.16,yoyo:true,repeat:3,ease:"sine.inOut",immediateRender:false}},{T["shortcuts"] - .1:.3f});')
    # the houses burn out or grey with their towns, and come back for the mixed world
    add(f'tl.to(".kd{KI["grok"]} .hs",{{filter:"grayscale(1) brightness(.45)",duration:.4}},{T["alive4"] - .1:.3f});')
    add(f'tl.to(".kd{KI["chatgpt"]} .hs",{{filter:"grayscale(1) brightness(.5)",duration:.4}},{T["seven"]:.3f});')
    add(f'tl.to(".hs",{{filter:"grayscale(0) brightness(1)",duration:.4}},{L[7]:.3f});')


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
                if ln["line"] <= 3:   # the opening words punch in as they are spoken
                    add(f'tl.fromTo("#{cid}_{k}",{{scale:1.22}},{{scale:1,duration:.2,ease:"back.out(3)",immediateRender:false}},{w["s"]:.3f});')
                add(f'tl.set("#{cid}_{k}",{{attr:{{class:"w"}}}},{w["e"] + .02:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "Serif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #F1E9DC; }
body { font-family: "Manrope", sans-serif; color: #1E1B18; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #F1E9DC; }
.clip { position: absolute; inset: 0; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
#grid { background-image: linear-gradient(#E4D9C7 2px, transparent 2px), linear-gradient(90deg, #E4D9C7 2px, transparent 2px);
  background-size: 60px 60px; background-position: 30px 0; }
#cam { position: absolute; left: 40px; top: 640px; width: 1000px; height: 1000px; transform-origin: 50% 50%; opacity: 0; perspective: 1700px; }
#tilt { position: absolute; inset: 0; transform: rotateX(22deg); transform-origin: 50% 60%; }
.kd { position: absolute; inset: 0; opacity: .3; }
.land { position: absolute; left: 0; top: 0; }
.ag { position: absolute; width: 26px; height: 26px; border-radius: 50%; border: 3px solid #1E1B18; opacity: 0; }
.pin { position: absolute; width: 24px; height: 24px; border-radius: 50% 50% 50% 0; background: #D9483B; border: 3px solid #1E1B18; opacity: 0; }
.pin::after { content: ""; position: absolute; left: 6px; top: 6px; width: 7px; height: 7px; border-radius: 50%; background: #fff; }
.emb { position: absolute; width: 132px; height: 132px; border-radius: 50%; border: 5px solid #1E1B18 !important; display: flex; align-items: center;
  justify-content: center; box-shadow: 7px 8px 0 #1E1B18; }
.emb img { width: 76px; height: 76px; }
.kname { position: absolute; width: 300px; text-align: center; font-size: 26px; letter-spacing: 4px; color: var(--c); }
.fire { position: absolute; width: 44px; height: 60px; border-radius: 50% 50% 45% 45%; transform-origin: 50% 100%; opacity: 0;
  background: radial-gradient(ellipse 50% 60% at 50% 70%, #fff3b0 0%, #ffb830 35%, #E8735A 65%, rgba(232,115,90,0) 100%); }
#radar { position: absolute; left: 140px; top: 880px; width: 800px; height: 800px; border-radius: 50%; opacity: .5;
  background: conic-gradient(from 0deg, rgba(232,115,90,0) 0deg, rgba(232,115,90,0) 300deg, rgba(232,115,90,.3) 360deg); }
#ui { z-index: 5; }
.top { position: absolute; left: 70px; right: 70px; top: 170px; display: flex; justify-content: space-between; align-items: center; }
.brand { font-size: 30px; letter-spacing: 4px; color: #1E1B18; display: flex; align-items: center; gap: 14px; }
.brand b { width: 18px; height: 18px; border-radius: 50%; background: #E8735A; font-size: 0; }
.prog { width: 220px; height: 26px; border-radius: 13px; border: 3px solid #1E1B18; overflow: hidden; }
.prog i { display: block; height: 100%; background: #E8735A; transform-origin: 0 50%; transform: scaleX(0); }
/* everything that pops in later starts hidden here, never through a set at t=0 */
.chip, .stamp, .dossier, .needs, .acts, .act, .q, .tag, .mira, .shield, .drift, .hud, #endc, .ec-1, .ec-kw, .ec-2, .ec-h, .ty { opacity: 0; }
.card { background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; }
.chip { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; padding: 10px 30px; border-radius: 30px; font-size: 34px;
  letter-spacing: 4px; background: #1E1B18; color: #F1E9DC; }
.c15 { top: 430px; }
.mixed { top: 430px; white-space: nowrap; }
.stamp { position: absolute; left: 50%; top: 1100px; margin-left: -330px; width: 660px; padding: 16px 0; text-align: center; border: 8px solid #D9483B;
  border-radius: 20px; color: #D9483B; font: 800 76px/1 "Manrope"; letter-spacing: 2px; background: rgba(255,253,248,.85); }
.nohum { top: 525px; display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 70px; }
.nohum svg circle:first-child, .nohum svg path:first-of-type { fill: #1E1B18; }
.ext, .gone { top: 1030px; font-size: 62px; }
.dossier { position: absolute; left: 70px; top: 430px; width: 620px; padding: 22px 28px; border-radius: 22px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; }
.dossier .dl { font-size: 22px; letter-spacing: 5px; color: #D45C40; }
.dossier b { display: block; font: 800 54px/1.1 "Manrope"; letter-spacing: -1.5px; margin-top: 4px; }
.dossier span { display: block; font: italic 34px "Serif"; color: #D45C40; }
.drow { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.drow i { font-style: normal; font-size: 22px; padding: 6px 14px; border-radius: 14px; background: #F1E9DC; border: 2px solid #1E1B18; }
.needs { position: absolute; left: 70px; right: 70px; top: 440px; display: flex; align-items: center; gap: 22px; padding: 18px 26px; border-radius: 26px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; }
.coin { flex: none; width: 76px; height: 76px; border-radius: 50%; background: #F2B33D; border: 3px solid #1E1B18;
  display: flex; align-items: center; justify-content: center; font: 800 44px "Manrope"; color: #1E1B18; }
.needs b { display: block; font: 800 40px "Manrope"; letter-spacing: -1px; }
.needs span { display: block; font: 600 28px "Manrope"; color: #5b5650; }
.acts { position: absolute; left: 60px; right: 60px; top: 430px; height: 380px; }
.act { position: absolute; left: 0; width: 420px; height: 110px; border-radius: 28px; display: flex; align-items: center; gap: 22px; padding: 0 22px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; font: 800 50px "Manrope"; letter-spacing: 1px; color: #1E1B18; }
.a0, .vg0 { top: 0; } .a1, .vg1 { top: 130px; } .a2, .vg2 { top: 260px; }
.aic { width: 70px; height: 70px; border-radius: 20px; background: #D9483B; border: 3px solid #1E1B18; display: flex; align-items: center;
  justify-content: center; font: 800 52px "Manrope"; color: #fff; }
.aic.flame { background: radial-gradient(ellipse 45% 55% at 50% 65%, #fff3b0 0%, #ffb830 40%, #D9483B 80%); }
.banned { top: 130px; left: 50%; }
.q { position: absolute; left: 0; right: 0; top: 420px; text-align: center; font: italic 340px/1 "Serif"; color: #D45C40; }
.tag { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; white-space: nowrap; padding: 12px 30px; border-radius: 24px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 7px 8px 0 #1E1B18; color: #1E1B18; font: 800 40px "Manrope"; }
.tag b { font: 800 84px/1 "Manrope"; letter-spacing: -3px; color: #D9483B; margin-right: 10px; vertical-align: -6px; }
.tag.mono { font-size: 30px; letter-spacing: 3px; }
.t183, .t683, .t2, .t0 { top: 430px; }
.tas, .tclimb, .tsurv, .talive { top: 558px; }
.tfi { top: 642px; }
.t0 b { color: #3FA372; }
.talive { background: #3FA372; color: #fff; }
.tclimb { background: #D9483B; color: #fff; }
.tsurv { background: #10a37f; color: #fff; }
.tsteal { top: 540px; background: #D9483B; color: #fff; }
.mira { position: absolute; left: 120px; right: 120px; top: 650px; display: flex; align-items: center; gap: 20px; padding: 16px 24px; border-radius: 24px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 7px 8px 0 #1E1B18; }
.mira i { flex: none; width: 46px; height: 46px; border-radius: 50%; background: #3b78e7; border: 3px solid #1E1B18; }
.mira span { font: 600 34px "Manrope"; } .mira b { font-weight: 800; }
.shield { position: absolute; left: 270px; top: 815px; width: 540px; height: 540px; border-radius: 50%; border: 7px solid #3FA372;
  background: rgba(63,163,114,.1); }
.drift { position: absolute; left: 60px; right: 60px; top: 440px; padding: 30px 30px 34px; border-radius: 32px; text-align: center;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 10px 11px 0 #1E1B18; }
.drift span { display: block; font-size: 26px; letter-spacing: 5px; color: #D45C40; }
.drift b { display: block; font: italic 120px/1.05 "Serif"; margin: 6px 0; color: #D45C40; }
.drift i { font: 700 36px "Manrope"; font-style: normal; color: #1E1B18; }
.hud { position: absolute; left: 50px; right: 50px; top: 1395px; height: 124px; display: flex; align-items: center; gap: 22px; padding: 0 26px;
  border-radius: 28px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; }
.hemb { flex: none; width: 82px; height: 82px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 3px solid #1E1B18; }
.hemb img { width: 48px; height: 48px; }
.hcol { display: flex; flex-direction: column; min-width: 0; }
.hcol:nth-child(2) { flex: 1; }
.hl { font-size: 18px; letter-spacing: 3px; color: #7a7268; }
.hcol b { font: 800 40px/1.1 "Manrope"; letter-spacing: -1px; color: #1E1B18; white-space: nowrap; }
.hcol b i { font-style: normal; }
.hcol b.red { color: #D9483B; }
#caps { z-index: 6; }
.cap { position: absolute; left: 50px; right: 50px; top: 245px; text-align: center; font: 800 62px/1.22 "Manrope"; letter-spacing: -1.5px;
  color: #1E1B18; opacity: 0; }
.cap .w { display: inline-block; padding: 0 12px 6px; border-radius: 14px; }
.cap .w.on { background: #D45C40; color: #fff; }
#endc { position: absolute; left: 60px; right: 60px; top: 480px; padding: 46px 40px 42px; border-radius: 40px; text-align: center;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 12px 13px 0 #1E1B18; }
.ec-1 { font: 800 56px "Manrope"; letter-spacing: -1.5px; }
.ec-kw { display: inline-block; margin: 14px 0 10px; padding: 6px 54px; border-radius: 40px; background: #D45C40; border: 3px solid #1E1B18;
  font: 800 150px/1.1 "Manrope"; letter-spacing: 4px; color: #fff; }
.ty { display: inline-block; }
.cur { display: inline-block; width: 10px; height: 118px; margin-left: 10px; vertical-align: -10px; border-radius: 5px; background: #fff; }
.ec-2 { font: italic 54px "Serif"; color: #D45C40; }
.ec-h { margin-top: 18px; font-size: 32px; letter-spacing: 4px; color: #1E1B18; }
.ring { position: absolute; width: 140px; height: 140px; border-radius: 50%; border: 6px solid; opacity: 0; }
.hs { position: absolute; width: 30px; height: 22px; border-radius: 3px; background: #FFFDF8; border: 3px solid #1E1B18; opacity: 0; }
.hs::before { content: ""; position: absolute; left: -6px; top: -17px; border-left: 18px solid transparent; border-right: 18px solid transparent;
  border-bottom: 14px solid var(--c); }
.msg { position: absolute; left: 0; top: 0; width: 20px; height: 20px; border-radius: 50%; border: 3px solid #1E1B18; opacity: 0; }
.live { display: flex; align-items: center; gap: 10px; font-size: 22px; letter-spacing: 3px; color: #D9483B; }
.live b { width: 14px; height: 14px; border-radius: 50%; background: #D9483B; }
.dossier { overflow: hidden; }
.dossier b em { font-style: normal; display: inline-block; opacity: 0; }
.scan { position: absolute; left: 0; right: 0; top: 0; height: 4px; background: #E8735A; opacity: 0; }
.rs { position: absolute; left: 730px; top: 535px; padding: 8px 18px; border: 6px solid #D9483B; border-radius: 14px; color: #D9483B;
  font: 800 38px/1 "Manrope"; letter-spacing: 1px; background: rgba(255,253,248,.9); opacity: 0; }
.nbar { flex: none; margin-left: auto; width: 110px; height: 22px; border-radius: 11px; border: 3px solid #1E1B18; overflow: hidden; }
.nbar i { display: block; height: 100%; background: #3FA372; transform-origin: 0 50%; }
.fc { position: absolute; left: 120px; top: 488px; width: 34px; height: 34px; border-radius: 50%; background: #F2B33D; border: 3px solid #1E1B18;
  display: flex; align-items: center; justify-content: center; font: 800 18px "Manrope"; color: #1E1B18; opacity: 0; }
#alert { position: absolute; inset: 0; border: 16px solid #D9483B; opacity: 0; }
.vg { position: absolute; left: 470px; right: 0; height: 110px; border-radius: 28px; overflow: hidden; background: #FFFDF8;
  border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; opacity: 0; }
.vbot { position: absolute; width: 46px; height: 46px; border-radius: 50%; border: 3px solid #1E1B18; background: #9a9187; }
.vp-a { left: 300px; top: 30px; opacity: 0; }
.vp-f { position: absolute; left: 40px; top: 24px; width: 62px; height: 62px; border-radius: 18px; background: #D9483B; border: 3px solid #1E1B18;
  display: flex; align-items: center; justify-content: center; font-size: 34px; color: #fff; opacity: 0; }
.vp-b { position: absolute; left: 240px; top: 2px; opacity: 0; }
.vs-a { left: 60px; top: 50px; opacity: 0; }
.vs-t { left: 400px; top: 50px; background: #1E1B18; opacity: 0; }
.vs-c { position: absolute; left: 66px; top: 10px; width: 34px; height: 34px; border-radius: 50%; background: #F2B33D; border: 3px solid #1E1B18;
  display: flex; align-items: center; justify-content: center; font: 800 18px "Manrope"; color: #1E1B18; opacity: 0; }
.vs-q { position: absolute; left: 118px; top: 12px; font: italic 54px/1 "Serif"; color: #D45C40; opacity: 0; }
.va-h { position: absolute; left: 196px; top: 50px; width: 90px; height: 52px; border-radius: 4px; background: #FFFDF8; border: 3px solid #1E1B18; opacity: 0; }
.va-h::before { content: ""; position: absolute; left: -14px; top: -34px; border-left: 56px solid transparent; border-right: 56px solid transparent;
  border-bottom: 32px solid #7a7268; }
.vfl { position: absolute; top: 24px; width: 40px; height: 56px; border-radius: 50% 50% 45% 45%; transform-origin: 50% 100%; opacity: 0;
  background: radial-gradient(ellipse 50% 60% at 50% 70%, #fff3b0 0%, #ffb830 35%, #E8735A 65%, rgba(232,115,90,0) 100%); }
.vf0 { left: 196px; } .vf1 { left: 222px; top: 8px; } .vf2 { left: 250px; }
.smk { position: absolute; top: 18px; width: 30px; height: 30px; border-radius: 50%; background: #7a7268; opacity: 0; }
.sk0 { left: 214px; } .sk1 { left: 246px; } .sk2 { left: 228px; } .sk3 { left: 258px; }
.bst { position: absolute; opacity: 0; }
#fx { z-index: 7; }
#flash { position: absolute; inset: 0; background: #FFFDF8; opacity: 0; }
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
        <div id="cam"><div id="tilt">{kds}{fires()}{messengers()}</div></div>
      </div>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b>&#9679;</b> AI.NXTLVL</span><span class="live mono"><b></b>SIMULATION</span><span class="prog"><i></i></span></div>
        {OVER}{hud()}{endc}
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4">{caps}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5" data-layout-ignore><div id="flash"></div><div id="alert"></div></div>
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
