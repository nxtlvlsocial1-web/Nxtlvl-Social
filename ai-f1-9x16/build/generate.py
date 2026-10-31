"""AI F1 reel ("What if an AI ran a Formula 1 team for a race?"): writes index.html. 1080x1920, 30 fps, about 64 s.
Account: @nxtlvlsocial.ai. A "what if" reel: no keyword CTA (house rule), it ends on a question and the follow prompt.

python3 build/generate.py      (from the project root, after build/voice.py)

The circuit is a Three.js diorama (assets/js/track.js) drawn on hf-seek; this file writes the HTML layer on top in the
cream house style: a top bar with the lap, word-by-word caption cards, one card at a time in the card band
(y 430-820), the race HUD (#7's position and tyres, written by track.js), name tags under the close-ups and the end
card. Cue times come from build/words.json and go to track.js as window.CT.

The race is a hypothetical (the top bar says WHAT IF); its numbers are illustrative. The one real-world claim is the
simulation card: Oracle Red Bull Racing runs billions of race simulations (8 billion before a race weekend, The
National / AFP, October 2026) to plan strategy such as pit stops.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
DUR = round(LINES[-1]["end"] + 1.8, 2)


def word(line, text, nth=1):
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1]["s"]


L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
T = {
    "ai": word(1, "ai"), "called": word(1, "called"), "just": word(1, "just"), "pits": word(1, "pits"), "onlap": word(1, "on", 2),
    "drops": word(1, "drops"), "last": word(1, "last"),
    "later": word(2, "later"), "rain": word(2, "rain"), "every": word(2, "every"), "slick": word(2, "slick"), "only": word(2, "only"),
    "wets": word(2, "wets"), "six": word(2, "six"), "passed": word(2, "passed"), "lap": word(2, "lap", 2),
    "listening": word(3, "listening"), "tyre": word(3, "tyre"), "sound": word(3, "sound"), "engine": word(3, "engine"),
    "exactly": word(3, "exactly"), "corner": word(3, "corner"), "attack": word(3, "attack"),
    "forty": word(4, "forty"), "crash": word(4, "crash"), "happens": word(4, "happens"), "slows": word(4, "slows"), "second": word(4, "second"),
    "early": word(4, "early"), "two": word(4, "two"), "spin": word(4, "spin"), "drives": word(4, "drives"), "through": word(4, "through"),
    "final": word(5, "final"), "leading": word(5, "leading"), "teammate": word(5, "teammate"), "behind": word(5, "behind"),
    "says": word(5, "says"), "let": word(5, "let"), "through2": word(5, "through"),
    "understand": word(6, "understand"), "obeys": word(6, "obeys"), "wins": word(6, "wins"), "championship": word(6, "championship"),
    "one": word(6, "one"), "point": word(6, "point"),
    "farfetched": word(7, "farfetched"), "formula": word(7, "formula"), "billions": word(7, "billions"), "simulations": word(7, "simulations"),
    "pit": word(7, "pit"),
    "would": word(8, "would"), "orders": word(8, "orders"), "follow": word(8, "follow", 2), "end": DUR,
}
# race script shared with track.js
T["cuts"] = [7.5, 15.85, 23.3, 32.5, 48.6]
T["pb"] = [13.55, 13.9, 14.25, 14.6, 14.95, 15.3]          # #7 passes the last six cars
T["att"] = round(T["attack"] + .1, 3)                     # the hairpin pass
T["tc"] = round(T["two"] + .12, 3)                        # the two leaders touch
T["slowmo"] = [30.0, 31.9]
T["finish"] = 40.75                                       # #11 takes the flag
T["radio"] = [[T["just"] - .15, T["pits"] + .4], [T["exactly"] - .2, T["att"] + .2], [T["slows"] - .2, T["early"] + .4], [T["let"] - .2, T["through2"] + .6]]
# close-ups (camera in front of the driver's face) and the name tag under each
T["focus"] = [
    {"id": 0, "a": 4.25, "b": 5.95},                                   # 0 #7 in the pit box
    {"id": 0, "a": round(T["leading"] - .45, 3), "b": round(T["teammate"] - .25, 3)},    # 1 #7 leading
    {"id": 1, "a": round(T["teammate"] - .2, 3), "b": 37.0},            # 2 #11 right behind
    {"id": 0, "a": round(T["let"] - .1, 3), "b": 40.35},                # 3 #7 hears "let him through"
    {"id": 0, "a": round(E[4] + .25, 3), "b": round(T["wins"] - .9, 3)},  # 4 #7 doesn't understand, obeys
    {"id": 1, "a": round(T["one"] - .7, 3), "b": 48.55},                # 5 #11, champion
]
F = T["focus"]
TAGS = [("tg-ai", T["ai"] - .1, T["called"] + .2, "THE AI RACE ENGINEER", "makes every call"),
        ("tg-d1", F[0]["a"] + .3, F[0]["b"] - .25, "#7 &middot; THE DRIVER", "called in on lap one"),
        ("tg-d2", F[1]["a"] + .3, F[1]["b"] - .2, "#7 &middot; THE DRIVER", "leading the final lap"),
        ("tg-m1", F[2]["a"] + .3, F[2]["b"] - .25, "#11 &middot; HIS TEAMMATE", "fighting for the title"),
        ("tg-d3", F[4]["a"] + .3, F[4]["b"] - .25, "#7 &middot; THE DRIVER", "gave up the win"),
        ("tg-m2", F[5]["a"] + .3, F[5]["b"] - .2, "#11 &middot; HIS TEAMMATE", "world champion by 1 point")]
A = []


def add(js):
    A.append("      " + js)


def pop(sel, t, frm="scale:.6,opacity:0", d=.3, ease="back.out(2.2)", to="scale:1,opacity:1,x:0,y:0,rotation:0"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def out(sel, t, d=.22, props="opacity:0,y:-24"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


def count(sel, t, a, b, d, fmt="Math.round(o.v).toLocaleString('en-US')", ease="power2.out"):
    add('(()=>{const o={v:%s};tl.to(o,{v:%s,duration:%.3f,ease:"%s",onUpdate:()=>{document.querySelectorAll("%s").forEach(e=>e.textContent=%s)}},%.3f);})();'
        % (a, b, d, ease, sel, fmt, t))


def radio(cls, msg, extra=""):
    bars = "".join(f'<i class="rb rb{k}"></i>' for k in range(9))
    return (f'<div class="card radio {cls}"><div class="rtop"><span class="mono lab">AI RACE ENGINEER &middot; RADIO</span><em class="rbars">{bars}</em></div>'
            f'<b class="mono msg">{msg}</b>{extra}</div>')


TYRES = "".join(f'<i class="td {"wet" if k == 19 else "soft" if k % 3 else "med"} td{k}"></i>' for k in range(20))
CARDS = (
    '<div class="slam lap1">LAP 1</div>'
    + radio("c-box", "BOX, BOX. NOW.", '<span class="sub">lap 1 of 52</span>')
    + '<div class="stamp st-last">P20 &middot; LAST</div>'
    '<div class="card c-rain"><span class="mono lab">WEATHER</span><b>RAIN <i class="rpct">0</i>%</b>'
    '<em class="drops">' + "".join(f'<i class="dr dr{k}"></i>' for k in range(12)) + '</em></div>'
    f'<div class="card c-tyres"><span class="mono lab">TYRES ON THE GRID</span><div class="tgrid">{TYRES}</div>'
    '<span class="sub"><b class="k soft"></b> slicks: 19 cars &nbsp; <b class="k wet"></b> wets: <i class="hl">#7 only</i></span></div>'
    '<div class="card c-ot"><span class="mono lab">OVERTAKES THIS LAP</span><b class="big">+<i class="otn">0</i></b></div>'
    '<div class="card c-listen"><span class="mono lab">AI &middot; LISTENING TO THE ENGINE</span>'
    '<em class="wave">' + "".join(f'<i class="wv wv{k}"></i>' for k in range(24)) + '</em></div>'
    '<div class="card c-wear"><span class="mono lab">TYRE WEAR &middot; FROM ENGINE SOUND</span><b>FRONT LEFT <i class="wn">0</i>%</b>'
    '<span class="bar"><i class="barf"></i></span></div>'
    + radio("c-att", "ATTACK. TURN 9.")
    + '<div class="card alert c-pred"><span class="mono lab">PREDICTION &middot; TURN 1</span><b>CRASH AHEAD</b>'
    '<span class="sub">probability <i class="pp">0</i>%</span></div>'
    + radio("c-lift", "LIFT. NOW.", '<b class="minus">&minus;<i class="mn">0.0</i> s</b>')
    + '<div class="stamp st-crash">CRASH</div>'
    '<div class="stamp st-final">FINAL LAP</div>'
    + radio("c-let", "LET HIM THROUGH.")
    + '<div class="card c-champ"><span class="mono lab">DRIVERS&rsquo; CHAMPIONSHIP &middot; FINAL</span>'
    '<div class="tbl"><div class="row r-mate"><span class="pos mono"><i class="mp">2</i></span><span class="tn">#11 HIS TEAMMATE</span><span class="pts mono"><i class="mpts">400</i></span></div>'
    '<div class="row r-riv"><span class="pos mono"><i class="rp">1</i></span><span class="tn">#4 RIVAL</span><span class="pts mono">411</span></div></div>'
    '<span class="sub onept">won by <b class="coral">1 point</b></span></div>'
    '<div class="card c-real"><span class="mono lab real">REAL WORLD, 2026</span><b>Oracle Red Bull Racing</b>'
    '<span class="sub">runs this many race simulations before a race weekend, to plan its pit stops</span>'
    '<b class="bign"><i class="nb">0</i></b></div>'
    '<div class="card c-q"><b class="ser big">Would you follow</b><b class="ser big coral">its orders?</b></div>'
)
SLAMS = [("sl-p1", T["through"] + .2, "P1!", "home"), ("sl-ot", T["att"] + .15, "OVERTAKE!", "home"), ("sl-p2", T["finish"] + .15, "P2", "away")]
CARDS += "".join(f'<div class="ptag {c}"><span class="mono">{a}</span><b>{b}</b></div>' for c, _, _, a, b in TAGS)
CARDS += "".join(f'<div class="goal {c} {k}">{txt}</div>' for c, _, txt, k in SLAMS)
CTX = ["LAP 1 / 52", "LAP 3 / 52", "LAP 12 / 52", "LAP 40 / 52", "FINAL LAP", "TITLE DECIDED", "REAL WORLD", "YOUR CALL"]


def radio_anim(cls, t0, t1):
    pop(f".{cls}", t0, "x:-110,opacity:0", .3, "back.out(1.8)")
    for k in range(9):
        add(f'tl.fromTo(".{cls} .rb{k}",{{scaleY:.2}},{{scaleY:{[.5, .9, .6, 1, .7, .95, .45, .8, .55][k]},duration:.12,yoyo:true,repeat:{int((t1 - t0) / .12)},ease:"sine.inOut",immediateRender:false}},{t0 + k * .02:.3f});')
    add(f'tl.fromTo(".{cls} .msg",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.45,ease:"steps(14)",immediateRender:false}},{t0 + .12:.3f});')
    out(f".{cls}", t1)


def story():
    # hook: lap 1, the radio call, the drop to last
    pop(".lap1", .05, "scale:2.6,opacity:0,rotation:-12", .22, "back.out(2)", "scale:1,opacity:1,rotation:-5")
    out(".lap1", .95, .18)
    radio_anim("c-box", T["just"] - .15, T["onlap"] - .2)
    pop(".st-last", T["drops"] - .05, "scale:2.4,opacity:0,rotation:-18", .25, "back.out(2)", "scale:1,opacity:1,rotation:-6")
    out(".st-last", E[0] + .1, .18)
    # rain, the tyres, six overtakes
    pop(".c-rain", T["rain"] - .1, "y:-40,opacity:0", .3, "back.out(1.8)")
    count(".rpct", T["rain"], 0, 100, .6, "Math.round(o.v)")
    for k in range(12):
        add(f'tl.fromTo(".dr{k}",{{y:-30,opacity:0}},{{y:40,opacity:1,duration:.45,repeat:4,ease:"none",immediateRender:false}},{T["rain"] + k * .06:.3f});')
    out(".c-rain", T["slick"] - .35)
    pop(".c-tyres", T["slick"] - .2, "x:120,opacity:0", .3, "back.out(1.8)")
    for k in range(19):
        pop(f".td{k}", T["slick"] + k * .03, "scale:0,opacity:0", .18, "back.out(3)")
    pop(".td19", T["wets"] - .05, "scale:0,opacity:0", .3, "back.out(4)", "scale:1.35,opacity:1")
    pop(".c-tyres .hl", T["wets"], "scale:1,opacity:1", .25, "back.out(3)", "scale:1.12,opacity:1")
    out(".c-tyres", T["six"] - .3)
    pop(".c-ot", T["six"] - .15, "scale:.7,opacity:0", .3, "back.out(2)")
    for k, tp in enumerate(T["pb"]):
        count(".otn", tp, k, k + 1, .06, "Math.round(o.v)", "none")
        add(f'tl.fromTo(".c-ot .big",{{scale:1.18}},{{scale:1,duration:.22,ease:"back.out(3)",immediateRender:false}},{tp:.3f});')
    out(".c-ot", E[1] + .2)
    # listening: the engine wave, the tyre wear, the attack call
    pop(".c-listen", T["listening"] - .25, "y:40,opacity:0", .3, "back.out(1.8)")
    for k in range(24):
        add(f'tl.fromTo(".wv{k}",{{scaleY:.15}},{{scaleY:{.3 + .7 * abs(((k * 7) % 11) / 10 - .3):.2f},duration:.09,yoyo:true,repeat:16,ease:"sine.inOut",immediateRender:false}},{T["listening"] + k * .015:.3f});')
    out(".c-listen", T["tyre"] - .3)
    pop(".c-wear", T["tyre"] - .15, "x:120,opacity:0", .3, "back.out(1.8)")
    count(".wn", T["tyre"] + .1, 0, 62, 1.2, "Math.round(o.v)")
    add(f'tl.fromTo(".barf",{{scaleX:0}},{{scaleX:.62,duration:1.2,ease:"power2.out",immediateRender:false}},{T["tyre"] + .1:.3f});')
    out(".c-wear", T["exactly"] - .35)
    radio_anim("c-att", T["exactly"] - .2, T["att"] + .1)
    # lap 40: the prediction, lift, the crash, P1
    pop(".c-pred", T["crash"] - .15, "scale:1.4,opacity:0", .25, "back.out(2)")
    count(".pp", T["crash"], 0, 94, .9, "Math.round(o.v)")
    out(".c-pred", T["slows"] - .3)
    radio_anim("c-lift", T["slows"] - .2, T["two"] - .3)
    count(".mn", T["second"] - .1, 0, 1, .5, "o.v.toFixed(1)")
    pop(".st-crash", T["tc"] + .05, "scale:2.6,opacity:0,rotation:16", .22, "back.out(2)", "scale:1,opacity:1,rotation:5")
    add(f'tl.fromTo(".st-crash",{{x:0}},{{x:9,duration:.04,yoyo:true,repeat:7,ease:"none",immediateRender:false}},{T["tc"] + .25:.3f});')
    out(".st-crash", T["drives"] - .35, .18)
    # final lap
    pop(".st-final", T["final"] - .1, "scale:2.4,opacity:0,rotation:-14", .25, "back.out(2)", "scale:1,opacity:1,rotation:-5")
    out(".st-final", F[1]["a"] + .1, .18)
    radio_anim("c-let", T["let"] - .15, T["finish"] + .05)
    # the title by one point
    pop(".c-champ", T["wins"] - .15, "y:40,opacity:0", .35, "back.out(1.8)")
    count(".mpts", T["wins"], 400, 412, .9, "Math.round(o.v)", "power1.inOut")
    add(f'tl.fromTo(".r-mate",{{y:0}},{{y:-64,duration:.5,ease:"power2.inOut",immediateRender:false}},{T["championship"]:.3f});')
    add(f'tl.fromTo(".r-riv",{{y:0}},{{y:64,duration:.5,ease:"power2.inOut",immediateRender:false}},{T["championship"]:.3f});')
    add(f'tl.set(".mp",{{textContent:"1"}},{T["championship"] + .25:.3f}); tl.set(".rp",{{textContent:"2"}},{T["championship"] + .25:.3f});')
    pop(".onept", T["one"] - .1, "scale:.6,opacity:0", .3, "back.out(2.4)")
    out(".c-champ", F[5]["a"] + .05)
    # real world
    pop(".c-real", T["formula"] - .2, "y:40,opacity:0", .35, "back.out(1.8)")
    count(".nb", T["billions"] - .1, 0, 8e9, 1.6, "Math.round(o.v).toLocaleString('en-US')", "power3.out")
    add(f'tl.fromTo(".bign",{{scale:1.12}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["billions"] + 1.5:.3f});')
    out(".c-real", E[6] + .15)
    # the question, then the follow card (no keyword: house rule for what-if reels)
    pop(".c-q", T["would"] - .3, "scale:.8,opacity:0", .4, "back.out(1.8)")
    out(".c-q", T["follow"] - .25)
    pop("#endc", T["follow"] - .15, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-kw", T["follow"] + .05, "scale:.6,opacity:0", .3, "back.out(2.2)")
    pop(".ec-2", T["follow"] + .25, "y:20,opacity:0", .3)
    pop(".ec-h", T["follow"] + .5, "y:20,opacity:0", .3)
    # name tags, slams, the HUD
    for c, a, b, _, _ in TAGS:
        pop(f".{c}", a, "y:24,opacity:0", .25, "back.out(2)")
        out(f".{c}", b, .18)
    for c, t0, _, _ in SLAMS:
        pop(f".{c}", t0 - .02, "scale:2.6,opacity:0,rotation:-14", .22, "back.out(2.2)", "scale:1,opacity:1,rotation:-6")
        add(f'tl.fromTo(".{c}",{{x:0}},{{x:7,duration:.04,yoyo:true,repeat:5,ease:"none",immediateRender:false}},{t0 + .2:.3f});')
        out(f".{c}", t0 + .7, .15, "opacity:0,scale:1.3")
    pop(".hud", .3, "y:40,opacity:0", .3, "back.out(2)")
    for a in [T["cuts"][0], T["cuts"][1], T["cuts"][2], T["cuts"][3]]:
        add(f'tl.fromTo(".hud",{{scale:1.12}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{a + .05:.3f});')
    out(".hud", E[4] + .2, .2, "opacity:0,y:30")
    # top bar: progress, the WHAT IF light, the lap
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')
    add(f'tl.fromTo(".live b",{{opacity:1}},{{opacity:.15,duration:.45,yoyo:true,repeat:{int(DUR / .45)},ease:"sine.inOut",immediateRender:false}},0);')
    starts = [0] + T["cuts"][:4] + [T["finish"] + .1, T["cuts"][4], L[7] - .1, DUR + 1]
    for k in range(len(CTX)):
        add(f'tl.fromTo(".cx{k}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:.18,immediateRender:false}},{max(0, starts[k]):.3f});' if k else 'tl.set(".cx0",{opacity:1},0);')
        add(f'tl.to(".cx{k}",{{opacity:0,y:-8,duration:.15}},{starts[k + 1] - .15:.3f});')


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
            html.append(f'<div class="cap" id="{cid}"><div class="capin">{spans}</div></div>')
            a0 = ch[0]["s"] - .05
            z = chunks[ci + 1][0]["s"] - .05 if ci + 1 < len(chunks) else min(ln["end"] + .3, nxt - .06)
            add(f'tl.fromTo("#{cid}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.12,ease:"power2.out",immediateRender:false}},{a0:.3f});')
            add(f'tl.set("#{cid}",{{opacity:0}},{z:.3f});')
            for k, w in enumerate(ch):
                add(f'tl.set("#{cid}_{k}",{{attr:{{class:"w on"}}}},{w["s"]:.3f});')
                add(f'tl.fromTo("#{cid}_{k}",{{scale:1.18}},{{scale:1,duration:.2,ease:"back.out(3)",immediateRender:false}},{w["s"]:.3f});')
                add(f'tl.set("#{cid}_{k}",{{attr:{{class:"w"}}}},{w["e"] + .02:.3f});')
    return "".join(html)


def endcard():
    return ('<div id="endc"><div class="ec-1">Follow for more</div><div class="ec-kw">what ifs</div>'
            '<div class="ec-2">new scenario every week</div><div class="ec-h mono">@nxtlvlsocial.ai</div></div>')


CSS = """
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "Serif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #F1E9DC; }
body { font-family: "Manrope", sans-serif; color: #1E1B18; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #F1E9DC; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
#ui { z-index: 5; }
.top { position: absolute; left: 50px; right: 50px; top: 150px; height: 76px; display: flex; justify-content: space-between; align-items: center;
  padding: 0 26px; border-radius: 38px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 6px 7px 0 #1E1B18; }
.brand { font-size: 24px; letter-spacing: 3px; display: flex; align-items: center; gap: 12px; }
.brand b { width: 16px; height: 16px; border-radius: 50%; background: #E8735A; }
.live { display: flex; align-items: center; gap: 8px; font-size: 20px; letter-spacing: 2px; color: #A8452F; }
.live b { width: 12px; height: 12px; border-radius: 50%; background: #D9483B; }
.ctx { position: relative; width: 250px; height: 30px; }
.cx { position: absolute; left: 0; right: 0; top: 0; text-align: center; font-style: normal; font-size: 24px; letter-spacing: 2px; opacity: 0; white-space: nowrap; }
.prog { width: 120px; height: 20px; border-radius: 10px; border: 3px solid #1E1B18; overflow: hidden; }
.prog i { display: block; height: 100%; background: #E8735A; transform-origin: 0 50%; transform: scaleX(0); }
.card, .stamp, #endc, .ec-kw, .ec-2, .ec-h, .ptag, .goal, .slam, .hud, .onept { opacity: 0; }
.card { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; max-width: 960px; top: 440px; padding: 22px 34px;
  border-radius: 30px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; display: flex; flex-direction: column;
  align-items: flex-start; gap: 4px; }
.card .lab { display: block; font-size: 22px; letter-spacing: 4px; color: #D45C40; }
.card b { display: block; font: 800 56px/1.08 "Manrope"; letter-spacing: -1.5px; }
.card b i, .card .sub i { font-style: normal; }
.card .sub { display: block; font: 600 28px/1.3 "Manrope"; color: #5b5650; margin-top: 6px; max-width: 760px; }
.card .big { font-size: 130px; line-height: 1; letter-spacing: -4px; color: #D45C40; }
.card.alert { border-color: #D9483B; box-shadow: 8px 9px 0 #D9483B; }
.card.alert .lab, .card.alert b { color: #D9483B; }
.card.radio { background: #1E1B18; color: #F1E9DC; border-color: #1E1B18; box-shadow: 8px 9px 0 #E8735A; padding: 22px 34px 26px; min-width: 640px; }
.radio .rtop { display: flex; align-items: center; gap: 22px; width: 100%; justify-content: space-between; }
.radio .lab { color: #E8735A; }
.rbars { display: flex; gap: 6px; align-items: center; height: 44px; }
.rb { display: block; width: 8px; height: 44px; border-radius: 4px; background: #E8735A; transform: scaleY(.2); }
.radio .msg { font: 700 70px/1.1 "JBMono"; letter-spacing: 1px; color: #FFFDF8; margin-top: 8px; }
.radio .sub { color: #b9b0a4; }
.radio .minus { font: 800 64px "Manrope"; color: #F2B33D; margin-top: 4px; }
.c-let .msg { color: #F2B33D; font-size: 76px; }
.drops { position: relative; display: block; width: 420px; height: 70px; overflow: hidden; margin-top: 4px; }
.dr { position: absolute; top: 0; width: 6px; height: 24px; border-radius: 3px; background: #3A7BD5; opacity: 0; }
""" + "".join(f".dr{k} {{ left: {18 + k * 34}px; }}" for k in range(12)) + """
.tgrid { display: grid; grid-template-columns: repeat(10, 52px); gap: 12px; margin: 10px 0 4px; }
.td { display: block; width: 52px; height: 52px; border-radius: 50%; border: 9px solid #D9483B; background: #2A2623; opacity: 0; }
.td.med { border-color: #F2B33D; } .td.wet { border-color: #3A7BD5; box-shadow: 0 0 0 4px #FFFDF8, 0 0 0 7px #3A7BD5; }
.k { display: inline-block !important; width: 22px; height: 22px; border-radius: 50%; border: 6px solid #D9483B; vertical-align: -3px; }
.k.wet { border-color: #3A7BD5; } .hl { color: #3A7BD5; font-weight: 800; display: inline-block; }
.wave { display: flex; gap: 7px; align-items: center; height: 110px; margin-top: 6px; }
.wv { display: block; width: 14px; height: 110px; border-radius: 7px; background: #E8735A; transform: scaleY(.15); }
.bar { display: block; width: 560px; height: 26px; border-radius: 13px; border: 3px solid #1E1B18; margin-top: 10px; overflow: hidden; }
.barf { display: block; height: 100%; width: 100%; background: linear-gradient(90deg, #3FA372, #F2B33D 60%, #D9483B); transform-origin: 0 50%; transform: scaleX(0); }
.tbl { position: relative; width: 640px; height: 124px; margin-top: 8px; overflow: hidden; }
.row { position: absolute; left: 0; right: 0; height: 56px; display: flex; align-items: center; gap: 18px; padding: 0 16px; border-radius: 14px; font: 700 32px "Manrope"; }
.row .pos { width: 40px; } .row .tn { flex: 1; } .row i { font-style: normal; }
.r-riv { top: 0; background: #EFE6D6; } .r-mate { top: 64px; background: #D45C40; color: #fff; }
.card .coral { color: #D45C40; display: inline; font: inherit; }
.onept { font-size: 34px !important; }
.c-real { max-width: 900px; top: 470px; } .c-real .lab.real { color: #3FA372; } .c-real b { font-size: 50px; }
.bign { font-size: 92px !important; letter-spacing: -3px !important; color: #3FA372; line-height: 1 !important; margin-top: 6px; }
.c-q { align-items: center; text-align: center; }
.ser { font-family: "Serif" !important; font-style: italic; font-weight: 400 !important; letter-spacing: 0 !important; }
.card .ser.big { font-size: 84px; line-height: 1; }
.stamp { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 480px; padding: 14px 26px; border: 8px solid #D9483B; border-radius: 20px;
  color: #D9483B; font: 800 84px/1 "Manrope"; letter-spacing: 1px; background: rgba(255,253,248,.92); white-space: nowrap; }
.st-final { border-color: #1E1B18; color: #1E1B18; }
.slam { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 470px; padding: 6px 40px 14px; border-radius: 34px;
  font: 800 150px/1 "Manrope"; letter-spacing: -5px; color: #fff; background: #1E1B18; border: 4px solid #1E1B18; box-shadow: 10px 11px 0 #E8735A; }
.ptag { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1190px; padding: 14px 30px 16px; border-radius: 26px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 7px 8px 0 #1E1B18; text-align: center; }
.ptag::before { content: ""; position: absolute; left: 50%; top: -17px; margin-left: -14px; border-left: 14px solid transparent;
  border-right: 14px solid transparent; border-bottom: 16px solid #1E1B18; }
.ptag span { display: block; font-size: 24px; letter-spacing: 5px; color: #D45C40; }
.ptag b { display: block; font: 800 40px/1.15 "Manrope"; letter-spacing: -1px; }
.goal { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1120px; padding: 6px 40px 14px; border-radius: 34px;
  font: 800 150px/1 "Manrope"; letter-spacing: -5px; color: #fff; border: 4px solid #1E1B18; box-shadow: 10px 11px 0 #1E1B18; }
.goal.home { background: #D45C40; } .goal.away { background: #34508F; }
.hud { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1356px; display: flex; align-items: center; gap: 26px;
  padding: 12px 30px 12px 16px; border-radius: 40px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 7px 8px 0 #1E1B18; }
.hud .pbox { display: flex; align-items: baseline; gap: 2px; padding: 4px 22px 8px; border-radius: 28px; background: #1E1B18; color: #FFFDF8; }
.hud .pbox span { font: 800 34px "Manrope"; color: #E8735A; } .hud .pbox b { font: 800 60px/1 "Manrope"; letter-spacing: -2px; }
.hud .car { font-size: 30px; letter-spacing: 3px; display: flex; align-items: center; gap: 12px; }
.hud .car i { width: 26px; height: 26px; border-radius: 6px; background: #E8735A; border: 3px solid #1E1B18; }
.hud .ty { display: flex; align-items: center; gap: 12px; font-size: 28px; letter-spacing: 3px; }
.hud .ty i { display: block; width: 34px; height: 34px; border-radius: 50%; border: 8px solid #D9483B; background: #2A2623; }
#caps { z-index: 6; }
.cap { position: absolute; left: 0; right: 0; top: 262px; text-align: center; opacity: 0; }
.capin { display: inline-block; max-width: 960px; padding: 10px 22px 14px; border-radius: 26px; background: rgba(255,253,248,.94);
  font: 800 58px/1.2 "Manrope"; letter-spacing: -1.5px; color: #1E1B18; }
.cap .w { display: inline-block; padding: 0 10px 4px; border-radius: 14px; }
.cap .w.on { background: #D45C40; color: #fff; }
#endc { position: absolute; left: 60px; right: 60px; top: 520px; padding: 46px 40px 42px; border-radius: 40px; text-align: center;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 12px 13px 0 #1E1B18; }
.ec-1 { font: 800 56px "Manrope"; letter-spacing: -1.5px; }
.ec-kw { display: inline-block; margin: 12px 0 10px; padding: 4px 54px 14px; border-radius: 40px; background: #D45C40; border: 3px solid #1E1B18;
  font: italic 130px/1.05 "Serif"; color: #fff; }
.ec-2 { font: italic 50px "Serif"; color: #D45C40; }
.ec-h { margin-top: 18px; font-size: 32px; letter-spacing: 4px; color: #1E1B18; }
"""


def main():
    story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, **T}
    ctx = "".join(f'<i class="cx cx{k}">{c}</i>' for k, c in enumerate(CTX))
    hud = ('<div class="hud"><span class="pbox"><span>P</span><b id="pos">5</b></span><span class="car mono"><i></i>#7</span>'
           '<span class="ty mono"><i id="tdot"></i><span id="tyre">SOFT</span></span></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI F1 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b></b>NXTLVLSOCIAL.AI</span><span class="ctx mono">{ctx}</span>
          <span class="live mono"><b></b>WHAT IF</span><span class="prog"><i></i></span></div>
        {hud}{CARDS}{endcard()}
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4">{caps}</div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.CT = {json.dumps(ct)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/track.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
