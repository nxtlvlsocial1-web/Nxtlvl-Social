"""AI Football Club reel ("What if an AI managed a football club for a season?"): writes index.html. 1080x1920,
30 fps, about 67 s. Account: @nxtlvlsocial.ai. A "what if" reel: no keyword CTA (house rule), it ends on a question
and the follow prompt.

python3 build/generate.py      (from the project root, after build/voice.py and build/timing.py)

The stadium is a Three.js diorama (assets/js/stadium.js) drawn on hf-seek; this file writes the HTML layer on top in
the cream house style: a top bar with the match context, word-by-word caption cards, one card at a time in the card
band (y 430-820) and the end card. Cue times come from build/words.json and go to stadium.js as window.CT.

The season is a hypothetical (the top bar says WHAT IF); its numbers are illustrative. The one real-world claim is
the TacticAI card: Google DeepMind and Liverpool FC built TacticAI, an AI assistant for corner-kick tactics, and in a
blind test Liverpool's experts preferred its suggestions 90% of the time (Nature Communications, March 2024).
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
    "benched": word(1, "benched"), "thirty": word(1, "thirty"), "booing": word(1, "booing"),
    "later": word(2, "later"), "fournil": word(2, "fournil"), "tracking": word(2, "tracking"), "pace": word(2, "pace"),
    "signs": word(3, "signs"), "seventeen": word(3, "seventeen"), "month": word(3, "month"), "scores": word(3, "scores"), "debut": word(3, "debut"),
    "managing": word(4, "managing"), "twonil": word(4, "twonil"), "rewires": word(4, "rewires"), "heart": word(4, "heartrate"),
    "three": word(4, "three"), "goals": word(4, "goals"), "twenty": word(4, "twenty"),
    "christmas": word(5, "christmas"), "top": word(5, "top"), "booed": word(5, "booed"), "chanting": word(5, "chanting"),
    "january": word(6, "january"), "sells": word(6, "sells"), "warning": word(6, "warning"), "explanation": word(6, "explanation"),
    "cup": word(6, "cup"), "winner": word(6, "winner"), "against": word(6, "against"),
    "liverpool": word(7, "liverpool"), "designs": word(7, "designs"), "tactics": word(7, "tactics"), "blind": word(7, "blind"),
    "nine": word(7, "nine"),
    "trust": word(8, "trust"), "follow": word(8, "follow"), "end": DUR,
}
# goal shot times, the same list stadium.js scripts (the score and the SFX hit on them)
T["goals_t"] = [7.32, 7.74, 8.16, 8.6, T["scores"] + .05, T["twonil"] - .7, T["twonil"] - .25,
                T["three"], T["goals"] + .3, T["twenty"] + .3, T["winner"] - .35]
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


# ---------------------------------------------------------------- the story cards (one at a time in the card band)
# ---------------------------------------------------------------- the story cards (one at a time in the card band)
CARDS = (
    '<div class="stamp st-bench">BENCHED</div>'
    '<div class="card alert c-boo"><span class="dot r"></span><div><span class="mono lab">30,000 FANS</span><b>BOOING</b>'
    '<em class="bars">' + "".join(f'<i class="bb bb{k}"></i>' for k in range(7)) + '</em></div></div>'
    '<div class="card score c-ft"><span class="mono lab">FULL TIME &middot; MATCHDAY 1</span><b><i class="hs1">0</i> &ndash; 0</b></div>'
    '<div class="card c-track"><span class="mono lab">TRACKING DATA &middot; STAR PLAYER</span><b>top speed &darr;</b>'
    '<svg class="spark" viewBox="0 0 300 70"><polyline class="spk" points="0,14 50,12 100,18 150,22 200,34 250,46 300,58" fill="none" stroke="#D9483B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    '<span class="sub">half a yard slower. No coach saw it.</span></div>'
    '<div class="card c-sign"><span class="mono lab">NEW SIGNING</span><b>AGE <i class="n17">0</i></b><span class="sub">fee: less than one month of the star&rsquo;s wages</span></div>'
    '<div class="stamp st-debut">GOAL ON DEBUT</div>'
    '<div class="card score alert c-ht"><span class="mono lab">HALF-TIME</span><b>0 &ndash; 2</b></div>'
    '<div class="card c-form"><span class="mono lab">FORMATION &middot; FROM HEART-RATE DATA</span><b><i class="fa">4-4-2</i> &rarr; <i class="fb">3-4-3</i></b>'
    '<svg class="ecg" viewBox="0 0 320 60"><polyline class="ecgl" points="0,30 60,30 75,30 85,8 95,52 105,30 170,30 185,30 195,8 205,52 215,30 320,30" fill="none" stroke="#D9483B" stroke-width="5" stroke-linejoin="round"/></svg></div>'
    '<div class="card score c-come"><span class="mono lab">FULL TIME</span><b><i class="hs3">0</i> &ndash; 2</b></div>'
    '<div class="card c-table"><span class="mono lab">LEAGUE TABLE &middot; CHRISTMAS</span>'
    '<div class="tbl">' + "".join(f'<div class="row r{k}"><span class="pos mono">{k + 1}</span><span class="tn">{n}</span><span class="pts mono">{p}</span></div>'
                                   for k, (n, p) in enumerate([("Rivals United", 40), ("City Athletic", 38), ("Northside", 37), ("Harbour FC", 35)]))
    + '<div class="row you"><span class="pos mono"><i class="npos">7</i></span><span class="tn">YOUR CLUB</span><span class="pts mono">41</span></div></div></div>'
    '<div class="chant mono">A &middot; I &middot; A &middot; I</div>'
    '<div class="stamp st-sold">CAPTAIN SOLD</div>'
    '<div class="card c-why"><span class="mono lab">REASON GIVEN</span><b class="ser big">none.</b></div>'
    '<div class="card score alert c-final"><span class="mono lab">CUP FINAL &middot; 89&rsquo;</span><b>0 &ndash; 1</b><span class="sub">scored by your old captain</span></div>'
    '<div class="card c-real"><span class="mono lab real">REAL WORLD, 2024</span><b>Liverpool &times; Google DeepMind</b>'
    '<span class="sub">TacticAI suggests corner-kick tactics. In a blind test, the club&rsquo;s experts preferred it</span>'
    '<b class="big9"><i class="n9">0</i> / 10</b></div>'
    '<div class="card c-q"><b class="ser big">Would you trust an AI</b><b class="ser big coral">with your club?</b></div>'
)
CTX = ["MATCHDAY 1", "FULL TIME", "WEEK 3", "HALF-TIME", "CHRISTMAS", "JANUARY", "CUP FINAL", "REAL WORLD", "YOUR CALL"]


def story():
    # hook: benched, booing
    pop(".st-bench", T["benched"] - .05, "scale:2.4,opacity:0,rotation:-18", .25, "back.out(2)", "scale:1,opacity:1,rotation:-6")
    out(".st-bench", T["thirty"] - .25, .18)
    pop(".c-boo", T["thirty"] - .1, "x:-120,opacity:0", .3, "back.out(1.8)")
    for k in range(7):
        add(f'tl.fromTo(".bb{k}",{{scaleY:.25}},{{scaleY:{[.9, .55, 1, .7, .85, .5, .95][k]},duration:.2,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{T["thirty"] + k * .04:.3f});')
    out(".c-boo", L[1] - .1)
    # 4-0, then the tracking data
    pop(".c-ft", T["later"] - .1, "scale:.7,opacity:0", .3, "back.out(2)")
    for k, gt in enumerate([7.32, 7.74, 8.16, 8.6]):
        count(".hs1", gt + .3, k, k + 1, .08, "Math.round(o.v)", "none")
    add(f'tl.fromTo(".c-ft b",{{scale:1}},{{scale:1.15,duration:.15,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false}},{T["fournil"]:.3f});')
    out(".c-ft", T["tracking"] - .25)
    pop(".c-track", T["tracking"] - .1, "x:120,opacity:0", .3, "back.out(1.8)")
    add(f'tl.fromTo(".spk",{{strokeDashoffset:420}},{{strokeDashoffset:0,duration:1.2,ease:"power1.inOut",immediateRender:false}},{T["tracking"] + .2:.3f});')
    out(".c-track", E[1] + .15)
    # week 3: the signing, the debut goal
    pop(".c-sign", T["signs"] - .1, "x:-120,opacity:0", .3, "back.out(1.8)")
    count(".n17", T["seventeen"], 30, 17, .6, "Math.round(o.v)")
    out(".c-sign", T["scores"] - .2)
    pop(".st-debut", T["debut"] - .05, "scale:2.4,opacity:0,rotation:16", .25, "back.out(2)", "scale:1,opacity:1,rotation:5")
    out(".st-debut", E[2] + .15)
    # half-time: 0-2, the rewire, three goals
    pop(".c-ht", T["twonil"] - .1, "scale:1.5,opacity:0", .25, "back.out(2)")
    out(".c-ht", T["rewires"] - .25)
    pop(".c-form", T["rewires"] - .1, "x:120,opacity:0", .3, "back.out(1.8)")
    add(f'tl.fromTo(".fb",{{opacity:.15}},{{opacity:1,duration:.3,immediateRender:false}},{T["rewires"] + .6:.3f});')
    add(f'tl.fromTo(".ecgl",{{strokeDashoffset:600}},{{strokeDashoffset:0,duration:1.0,ease:"none",immediateRender:false}},{T["heart"] - .2:.3f});')
    out(".c-form", T["three"] - .25)
    pop(".c-come", T["three"] - .1, "scale:.7,opacity:0", .3, "back.out(2)")
    for k, gt in enumerate([T["three"], T["goals"] + .3, T["twenty"] + .3]):
        count(".hs3", gt + .38, k, k + 1, .08, "Math.round(o.v)", "none")
    out(".c-come", E[3] + .15)
    # Christmas: the table climbs, the chant
    pop(".c-table", T["christmas"] - .1, "y:40,opacity:0", .35, "back.out(1.8)")
    count(".npos", T["top"] - .3, 7, 1, .7, "Math.round(o.v)", "power2.in")
    add(f'tl.fromTo(".you",{{y:0}},{{y:-290,duration:.7,ease:"power2.in",immediateRender:false}},{T["top"] - .3:.3f});')
    for k in range(4):
        add(f'tl.fromTo(".r{k}",{{y:0}},{{y:58,duration:.7,ease:"power2.in",immediateRender:false}},{T["top"] - .3:.3f});')
    out(".c-table", T["booed"] + .3)
    pop(".chant", T["chanting"] - .15, "scale:.6,opacity:0", .3, "back.out(2.4)")
    add(f'tl.fromTo(".chant",{{y:0}},{{y:-10,duration:.16,yoyo:true,repeat:7,ease:"sine.inOut",immediateRender:false}},{T["chanting"] + .2:.3f});')
    out(".chant", E[4] + .2)
    # January: sold, no reason, the cup final
    pop(".st-sold", T["sells"] - .05, "scale:2.4,opacity:0,rotation:-18", .25, "back.out(2)", "scale:1,opacity:1,rotation:-6")
    out(".st-sold", T["warning"] - .2)
    pop(".c-why", T["warning"] - .05, "scale:.8,opacity:0", .3, "back.out(2)")
    out(".c-why", T["cup"] - .25)
    pop(".c-final", T["winner"] + .5, "scale:1.6,opacity:0", .25, "back.out(2)")
    out(".c-final", E[5] + .2)
    # real world: TacticAI, 9 out of 10
    pop(".c-real", T["liverpool"] - .15, "y:40,opacity:0", .35, "back.out(1.8)")
    pop(".big9", T["nine"] - .3, "scale:.6,opacity:0", .3, "back.out(2.4)")
    count(".n9", T["nine"] - .2, 0, 9, .5, "Math.round(o.v)")
    out(".c-real", E[6] + .15)
    # the question, then the follow card (no keyword: house rule for what-if reels)
    pop(".c-q", T["trust"] - .3, "scale:.8,opacity:0", .4, "back.out(1.8)")
    out(".c-q", T["follow"] - .25)
    pop("#endc", T["follow"] - .15, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-kw", T["follow"] + .05, "scale:.6,opacity:0", .3, "back.out(2.2)")
    pop(".ec-2", T["follow"] + .25, "y:20,opacity:0", .3)
    pop(".ec-h", T["follow"] + .5, "y:20,opacity:0", .3)
    # top bar: progress, the WHAT IF light, the match context
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')
    add(f'tl.fromTo(".live b",{{opacity:1}},{{opacity:.15,duration:.45,yoyo:true,repeat:{int(DUR / .45)},ease:"sine.inOut",immediateRender:false}},0);')
    starts = [0, T["later"] - .1, L[2] - .1, T["twonil"] - .15, L[4] - .1, L[5] - .1, T["cup"] - .2, L[6] - .1, L[7] - .1, DUR + 1]
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
.card, .stamp, #endc, .ec-kw, .ec-2, .ec-h, .chant, .big9 { opacity: 0; }
.card.score { flex-direction: column; gap: 2px; text-align: center; padding: 22px 60px; }
.card.score b { font-size: 120px; letter-spacing: -3px; line-height: 1; }
.bars { display: flex; gap: 8px; align-items: flex-end; height: 56px; margin-top: 6px; }
.bb { display: block; width: 26px; height: 56px; border-radius: 6px; background: #D9483B; transform-origin: 50% 100%; }
.c-track, .c-sign, .c-real, .c-form, .c-table { flex-direction: column; align-items: flex-start; gap: 4px; }
.spark { width: 300px; height: 70px; margin-top: 6px; } .spk { stroke-dasharray: 420; }
.ecg { width: 320px; height: 60px; margin-top: 6px; } .ecgl { stroke-dasharray: 600; }
.c-form b i { font-style: normal; } .c-form .fb { color: #D45C40; }
.tbl { position: relative; width: 640px; height: 300px; margin-top: 8px; overflow: hidden; }
.row { position: absolute; left: 0; right: 0; height: 52px; display: flex; align-items: center; gap: 18px; padding: 0 16px; border-radius: 14px;
  font: 700 30px "Manrope"; }
.r0 { top: 0; } .r1 { top: 58px; } .r2 { top: 116px; } .r3 { top: 174px; }
.row .pos { width: 40px; color: #7a7268; } .row .tn { flex: 1; } .row .pts { color: #5b5650; }
.row.you { top: 232px; background: #D45C40; color: #fff; } .row.you .pos, .row.you .pts { color: #fff; } .row.you i { font-style: normal; }
.chant { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 470px; padding: 16px 40px; border-radius: 40px;
  background: #D45C40; color: #fff; font-size: 64px; letter-spacing: 6px; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; }
.big9 { font-size: 110px !important; letter-spacing: -3px !important; color: #3FA372; line-height: 1 !important; margin-top: 4px; }
.st-bench { left: 0; right: 0; margin: 0 auto; width: max-content; top: 480px; font-size: 88px; }
.st-debut { left: 0; right: 0; margin: 0 auto; width: max-content; top: 480px; font-size: 70px; border-color: #3FA372; color: #3FA372; }
.st-sold { left: 0; right: 0; margin: 0 auto; width: max-content; top: 480px; font-size: 76px; }
.card { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; max-width: 960px; top: 440px; padding: 22px 34px;
  border-radius: 30px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; display: flex; align-items: center; gap: 22px; }
.card .lab { display: block; font-size: 22px; letter-spacing: 4px; color: #D45C40; }
.card b { display: block; font: 800 56px/1.08 "Manrope"; letter-spacing: -1.5px; }
.card b i { font-style: normal; }
.card .sub { display: block; font: 600 28px/1.3 "Manrope"; color: #5b5650; margin-top: 6px; max-width: 760px; }
.card .sub.mono { font: 700 22px "JBMono"; letter-spacing: 3px; color: #D45C40; }
.ser { font-family: "Serif" !important; font-style: italic; font-weight: 400 !important; letter-spacing: 0 !important; }
.card .ser.big { font-size: 84px; line-height: 1; }
.card .coral { color: #D45C40; }
.dot { flex: none; width: 34px; height: 34px; border-radius: 50%; border: 3px solid #1E1B18; }
.dot.g { background: #3FA372; } .dot.c { background: #E8735A; } .dot.y { background: #F2B33D; } .dot.r { background: #D9483B; }
.card.alert { border-color: #D9483B; box-shadow: 8px 9px 0 #D9483B; }
.card.alert .lab { color: #D9483B; }
.card.alert b { color: #D9483B; }
.bigclock { flex-direction: column; gap: 4px; text-align: center; padding: 26px 56px; }
.bigclock b { font-size: 110px; letter-spacing: -4px; line-height: 1; }
.bigclock .ser { font-size: 46px; color: #D45C40; }
.c-rush, .c-grid, .c-reroute, .c-real, .c-q, .c-why, .c-cut { flex-direction: column; align-items: flex-start; gap: 4px; }
.c-q, .c-why { align-items: center; text-align: center; }
.strike { position: relative; --s: 0; }
.strike::after { content: ""; position: absolute; left: -8px; right: -8px; top: 52%; height: 8px; border-radius: 4px; background: #D9483B;
  transform: scaleX(var(--s)); transform-origin: 0 50%; }
.bars { display: flex; gap: 10px; align-items: flex-end; height: 60px; margin-top: 8px; }
.gb { display: block; width: 40px; height: 60px; border-radius: 8px; background: #F2B33D; border: 3px solid #1E1B18; transform-origin: 50% 100%; }
.arrow { display: block; font: 800 44px "Manrope"; color: #D45C40; }
.c-real { max-width: 900px; top: 490px; }
.c-real .lab.real { color: #3FA372; }
.c-real b { font-size: 50px; }
.stamp { position: absolute; top: 470px; padding: 14px 26px; border: 8px solid #D9483B; border-radius: 20px; color: #D9483B;
  font: 800 56px/1 "Manrope"; letter-spacing: 1px; background: rgba(255,253,248,.92); white-space: nowrap; }
.st-mayor { left: 70px; }
.st-cops { right: 70px; top: 600px; }
.st-frozen { left: 0; right: 0; margin: 0 auto; width: max-content; top: 520px; font-size: 92px; border-color: #3a6fb0; color: #3a6fb0; }
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
.ty { display: inline-block; }
.cur { display: inline-block; width: 10px; height: 118px; margin-left: 10px; vertical-align: -10px; border-radius: 5px; background: #fff; }
.ec-2 { font: italic 50px "Serif"; color: #D45C40; }
.ec-h { margin-top: 18px; font-size: 32px; letter-spacing: 4px; color: #1E1B18; }
"""


def main():
    story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, **T}
    ctx = "".join(f'<i class="cx cx{k}">{c}</i>' for k, c in enumerate(CTX))
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Football 9x16</title>
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
        {CARDS}{endcard()}
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
    <script type="module" src="assets/js/stadium.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
