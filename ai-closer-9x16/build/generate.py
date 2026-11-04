"""AI Closer reel ("What if every DM turned into a sale on autopilot?"): writes index.html. 1080x1920, 30 fps, about
65 s. Account: @nxtlvlsocial.ai. This what-if reel carries a keyword CTA (comment CLOSE) because there is a real resource
to send: the DM sales template for HeyDM.

python3 build/generate.py      (from the project root, after build/voice.py)

The world is the voxel creator street of the AI clone reel (assets/js/closer.js): your studio, the fan's bench, a cafe,
the plaza, and THE CLOSER, a small floating voxel robot with a pixel screen face that sells while you sleep. This file
writes the HTML layer in the cream house style: top bar with the day, captions, one card at a time in the card band
(y 430-820), the HUD (sales, calls), name tags under close-ups and the CTA end card.

The month is a hypothetical (the top bar says WHAT IF); its numbers are illustrative. The one real-world claim is the
Meta card: Meta has said that about a billion people message a business every week across its messaging apps
(WhatsApp, Messenger and Instagram), e.g. Meta newsroom, "Conversations 2023".
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
    "am": word(1, "am"), "phone": word(1, "phone"), "buzzing": word(1, "buzzing"), "seven": word(1, "seven"), "sales1": word(1, "sales"), "havent": word(1, "havent"), "buyer1": word(1, "buyer"),
    "comments": word(2, "comments"), "price": word(2, "price"), "scroll": word(2, "scroll"), "closer": word(2, "closer"), "already": word(2, "already"), "dms": word(2, "dms"),
    "buyer": word(3, "buyer"), "expensive": word(3, "expensive"), "argue": word(3, "argue"), "story": word(3, "story"), "student": word(3, "student"), "buys": word(3, "buys"), "nine": word(3, "nine"),
    "clicked": word(4, "clicked"), "buy4": word(4, "buy"), "later": word(4, "later"), "follows": word(4, "follows"), "half": word(4, "half"), "back4": word(4, "back"),
    "midnight": word(5, "midnight"), "stranger": word(5, "stranger"), "pay": word(5, "pay"), "says": word(5, "says"), "no": word(5, "no"), "fit": word(5, "fit"),
    "two": word(6, "two"), "zero": word(6, "zero"), "calls": word(6, "calls"), "woman": word(6, "woman"), "turned": word(6, "turned"), "she": word(6, "she"), "friends": word(6, "friends"),
    "farfetched": word(7, "farfetched"), "billion": word(7, "billion"), "business": word(7, "business"), "every": word(7, "every"), "week": word(7, "week"),
    "setup": word(8, "setup"), "follow": word(8, "follow"), "commentk": word(8, "comment"), "closek": word(8, "close"), "template": word(8, "template"), "end": DUR,
}
T["cuts"] = [round(L[k] - .12, 3) for k in range(1, 8)]
# close-ups and the name tag under each
T["focus"] = [
    {"who": "you", "a": round(T["havent"] - .3, 3), "b": round(E[0] + .15, 3)},
    {"who": "robot", "a": round(T["closer"] - .55, 3), "b": round(E[1] + .15, 3)},
    {"who": "maya", "a": round(T["buys"] - .45, 3), "b": round(E[2] + .2, 3)},
    {"who": "robot", "a": round(T["says"] - .9, 3), "b": round(T["no"] + .55, 3)},
    {"who": "priya", "a": round(T["no"] + .6, 3), "b": round(E[4] + .2, 3)},
    {"who": "priya", "a": round(T["she"] - .35, 3), "b": round(E[5] + .25, 3)},
]
F = T["focus"]
TAGS = [("tg-you", F[0]["a"] + .25, F[0]["b"] - .2, "YOU", "fast asleep"),
        ("tg-bot", F[1]["a"] + .25, F[1]["b"] - .2, "YOUR AI CLOSER", "replies in 2 seconds"),
        ("tg-maya", F[2]["a"] + .25, F[2]["b"] - .2, "THE BUYER", "paid in 9 minutes"),
        ("tg-bot2", F[3]["a"] + .25, F[3]["b"] - .15, "YOUR AI CLOSER", "just said no to $497"),
        ("tg-pri", F[4]["a"] + .2, F[4]["b"] - .2, "THE STRANGER", "ready to pay"),
        ("tg-pri2", F[5]["a"] + .25, F[5]["b"] - .25, "THE ONE IT TURNED AWAY", "came back with 4 friends")]
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


CARDS = (
    '<div class="card c-sales"><span class="mono lab">STORE &middot; WHILE YOU SLEPT</span><b class="big2"><i class="sn">0</i> <em class="u">sales</em></b><span class="sub">+<i class="rv">$0</i> &middot; 0 messages from you</span></div>'
    '<div class="card c-price"><span class="mono lab">REEL &middot; NEW COMMENT</span>'
    '<div class="cm"><i class="av av2"></i><span class="mono who">@maya.makes</span></div><b class="kw">PRICE</b>'
    '<div class="msg out m2">Hey Maya! It&rsquo;s $97, here&rsquo;s the link &rarr;</div><span class="sub mono sent">REPLIED IN 2 SEC</span></div>'
    '<div class="card c-obj"><span class="mono lab">DM &middot; DAY 4</span>'
    '<div class="msg in o1">honestly it&rsquo;s too expensive</div>'
    '<div class="msg out o2">Jordan felt the same. Here&rsquo;s his story &darr;</div>'
    '<span class="stamp2 paid">PAID &middot; 9 MIN</span></div>'
    '<div class="card c-fol"><span class="mono lab">CLICKED, DIDN&rsquo;T BUY</span>'
    '<div class="srow r1"><span>Followed up</span><b><i class="f1">0</i></b></div>'
    '<div class="srow r2"><span>Came back</span><b class="green"><i class="f2">0</i></b></div><span class="chip ch50">50% came back</span></div>'
    '<div class="card c-no"><span class="mono lab">DM &middot; 12:07 AM &middot; @new_here</span>'
    '<div class="msg in n1">ok I&rsquo;m ready, how do I pay the $497?</div>'
    '<div class="msg out n2">Honestly? This isn&rsquo;t the right fit for you yet.</div><span class="stamp2 red nos">NO SALE</span></div>'
    '<div class="card c-d30"><span class="mono lab">DAY 30</span>'
    '<div class="srow"><span>Sales</span><b><i class="d1">0</i></b></div><div class="srow"><span>Sales calls</span><b class="coral">0</b></div></div>'
    '<div class="card c-ret"><span class="mono lab">NEW BUYERS &middot; REFERRED BY @new_here</span><b class="big2 green">+4</b><span class="sub">she came back, and brought her friends</span></div>'
    '<div class="card c-real"><span class="mono lab real">REAL WORLD &middot; META</span><b>About a billion people message a business</b>'
    '<b class="bign">every week</b><span class="sub">on WhatsApp, Messenger and Instagram, per Meta</span></div>'
)
CARDS += "".join(f'<div class="ptag {c}"><span class="mono">{a}</span><b>{b}</b></div>' for c, _, _, a, b in TAGS)
CTX = ["3:00 AM", "DAY 1", "DAY 4", "DAY 10", "DAY 18 &middot; 12:07 AM", "DAY 30", "REAL WORLD", "GET THE TEMPLATE"]
SALES = [(T["seven"] - .1, 0, 7, .5), (T["buys"], 7, 31, .8), (T["half"], 31, 96, 1.2), (T["two"], 96, 212, 1.2)]


def story():
    cu = T["cuts"]
    # 3 AM: the sales come in while you sleep
    pop(".c-sales", T["phone"] - .2, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".sn", T["seven"] - .1, 0, 7, .6, "Math.round(o.v)", "power2.out")
    count(".rv", T["seven"] - .1, 0, 679, .9, "'$'+Math.round(o.v)", "power2.out")
    add(f'tl.fromTo(".c-sales .big2",{{scale:1.15}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["sales1"] + .1:.3f});')
    out(".c-sales", F[0]["a"] + .1)
    # day 1: the comment, the instant DM
    pop(".c-price", T["comments"] - .2, "x:-110,opacity:0", .3, "back.out(1.8)")
    pop(".kw", T["price"] - .05, "scale:2,opacity:0,rotation:-8", .3, "back.out(2.4)", "scale:1,opacity:1,rotation:-3")
    pop(".m2", T["already"] - .1, "scale:.6,opacity:0", .25, "back.out(2.4)")
    pop(".sent", T["dms"] - .05, "y:10,opacity:0", .25)
    out(".c-price", E[1] + .15)
    # day 4: the objection, the story, paid
    pop(".c-obj", T["buyer"] - .2, "x:110,opacity:0", .3, "back.out(1.8)")
    pop(".o1", T["expensive"] - .4, "scale:.6,opacity:0", .25, "back.out(2.4)")
    pop(".o2", T["story"] - .1, "scale:.6,opacity:0", .3, "back.out(2.2)")
    pop(".paid", T["buys"], "scale:2.4,opacity:0,rotation:-20", .25, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    out(".c-obj", F[2]["a"] + .35)
    # day 10: follow-ups, half come back
    pop(".c-fol", T["clicked"] - .2, "y:40,opacity:0", .3, "back.out(1.8)")
    pop(".r1", T["follows"] - .2, "x:-30,opacity:0", .25, "back.out(2)")
    count(".f1", T["follows"], 0, 48, .7, "Math.round(o.v)", "power2.out")
    pop(".r2", T["half"] - .15, "x:-30,opacity:0", .25, "back.out(2)")
    count(".f2", T["half"], 0, 24, .7, "Math.round(o.v)", "power2.out")
    pop(".ch50", T["back4"] - .1, "scale:.6,opacity:0,rotation:-6", .3, "back.out(2.4)", "scale:1,opacity:1,rotation:-3")
    out(".c-fol", E[3] + .15)
    # day 18: ready to pay, and the AI says no
    pop(".c-no", T["stranger"] - .2, "y:40,opacity:0", .3, "back.out(1.8)")
    pop(".n1", T["pay"] - .5, "scale:.6,opacity:0", .25, "back.out(2.4)")
    pop(".n2", T["no"] + .55, "scale:.6,opacity:0", .3, "back.out(2.2)")
    pop(".nos", T["no"] + .8, "scale:2.4,opacity:0,rotation:-20", .25, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    out(".c-no", F[4]["a"] + .15)
    # day 30: 212 sales, zero calls; she came back with four friends
    pop(".c-d30", T["two"] - .2, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".d1", T["two"], 0, 212, 1.0, "Math.round(o.v)", "power2.out")
    add(f'tl.fromTo(".c-d30 .srow:nth-of-type(2) b",{{scale:1.3}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["zero"]:.3f});')
    out(".c-d30", T["woman"] - .3)
    pop(".c-ret", F[5]["a"] + .3, "scale:.7,opacity:0", .3, "back.out(2)")
    out(".c-ret", E[5] + .2)
    # real world
    pop(".c-real", T["billion"] - .3, "y:40,opacity:0", .35, "back.out(1.8)")
    add(f'tl.fromTo(".bign",{{scale:1.12}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["every"]:.3f});')
    out(".c-real", E[6] + .15)
    # the CTA end card: follow + comment CLOSE
    pop("#endc", T["setup"] - .4, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-h", T["follow"], "scale:.6,opacity:0", .3, "back.out(2.4)")
    pop(".ec-kw", T["commentk"] - .05, "scale:.5,opacity:0,rotation:-8", .35, "back.out(2.6)", "scale:1,opacity:1,rotation:-2")
    add(f'tl.fromTo(".ec-kw",{{scale:1}},{{scale:1.08,duration:.18,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{T["closek"] + .1:.3f});')
    pop(".ec-2", T["template"] - .5, "y:20,opacity:0", .3)
    for c, a, b, _, _ in TAGS:
        pop(f".{c}", a, "y:24,opacity:0", .25, "back.out(2)")
        out(f".{c}", b, .18)
    # HUD: sales, calls
    pop(".hud", .3, "y:40,opacity:0", .3, "back.out(2)")
    for t0, a, b, d in SALES:
        count(".hr", t0, a, b, d, "Math.round(o.v).toLocaleString('en-US')", "power1.inOut")
    out(".hud", E[6] + .2, .2, "opacity:0,y:30")
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')
    add(f'tl.fromTo(".live b",{{opacity:1}},{{opacity:.15,duration:.45,yoyo:true,repeat:{int(DUR / .45)},ease:"sine.inOut",immediateRender:false}},0);')
    starts = [0] + cu + [DUR + 1]
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
            if len(cur) == 4 or re.search(r"[.,?!]$", w["w"]):
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
.ctx { position: relative; width: 270px; height: 30px; }
.cx { position: absolute; left: 0; right: 0; top: 0; text-align: center; font-style: normal; font-size: 22px; letter-spacing: 2px; opacity: 0; white-space: nowrap; }
.prog { width: 110px; height: 20px; border-radius: 10px; border: 3px solid #1E1B18; overflow: hidden; }
.prog i { display: block; height: 100%; background: #E8735A; transform-origin: 0 50%; transform: scaleX(0); }
.card, .stamp, #endc, .ec-kw, .ec-2, .ec-h, .ptag, .hud, .stamp2 { opacity: 0; }
.card { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; max-width: 960px; top: 440px; padding: 22px 34px;
  border-radius: 30px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; display: flex; flex-direction: column;
  align-items: flex-start; gap: 4px; }
.card .lab { display: block; font-size: 22px; letter-spacing: 4px; color: #D45C40; }
.card b { display: block; font: 800 56px/1.08 "Manrope"; letter-spacing: -1.5px; }
.card b i, .card .sub i { font-style: normal; }
.card .sub { display: block; font: 600 28px/1.3 "Manrope"; color: #5b5650; margin-top: 6px; max-width: 760px; }
.card .sub.mono { font: 700 24px "JBMono"; letter-spacing: 2px; color: #5b5650; }
.card.alert { border-color: #D9483B; box-shadow: 8px 9px 0 #D9483B; }
.card.alert .lab, .card.alert b { color: #D9483B; }
.card .coral, .coral { color: #D45C40; } .inl { display: inline !important; font: inherit !important; }
.big2 { font-size: 110px !important; letter-spacing: -4px !important; line-height: 1 !important; }
.big2.green { color: #3FA372; }
.srow { position: relative; display: flex; gap: 26px; align-items: baseline; width: 600px; justify-content: space-between; padding: 6px 0; font: 800 40px "Manrope"; }
.srow .sp { font-size: 26px; color: #5b5650; }
.sx { position: absolute; left: -6px; right: -6px; top: 52%; height: 7px; border-radius: 4px; background: #D9483B; transform-origin: 0 50%; transform: scaleX(0); }
.stamp2 { position: absolute; right: -40px; top: -34px; padding: 6px 18px; border: 6px solid #3FA372; border-radius: 16px; color: #3FA372;
  font: 800 54px "Manrope"; background: rgba(255,253,248,.95); }
.spark { width: 340px; height: 80px; margin-top: 6px; } .spk { stroke-dasharray: 420; }
.c-q, .c-why { align-items: center; text-align: center; }
.ser { font-family: "Serif" !important; font-style: italic; font-weight: 400 !important; letter-spacing: 0 !important; }
.card .ser.big { font-size: 80px; line-height: 1.02; }
.c-real { max-width: 900px; top: 470px; } .c-real .lab.real { color: #3FA372; } .c-real b { font-size: 48px; }
.bign { font-size: 84px !important; letter-spacing: -3px !important; color: #3FA372; line-height: 1 !important; margin-top: 6px; }
.stamp { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 480px; padding: 14px 26px; border: 8px solid #D9483B; border-radius: 20px;
  color: #D9483B; font: 800 88px/1 "Manrope"; letter-spacing: 1px; background: rgba(255,253,248,.92); white-space: nowrap; }
.st-frozen { border-color: #3A7BD5; color: #3A7BD5; }
.ptag { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1190px; padding: 14px 30px 16px; border-radius: 26px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 7px 8px 0 #1E1B18; text-align: center; }
.ptag::before { content: ""; position: absolute; left: 50%; top: -17px; margin-left: -14px; border-left: 14px solid transparent;
  border-right: 14px solid transparent; border-bottom: 16px solid #1E1B18; }
.ptag span { display: block; font-size: 24px; letter-spacing: 5px; color: #D45C40; }
.ptag b { display: block; font: 800 40px/1.15 "Manrope"; letter-spacing: -1px; }
.hud { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1350px; display: flex; align-items: center; gap: 22px;
  padding: 14px 30px 14px 16px; border-radius: 34px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 7px 8px 0 #1E1B18; }
.hud .ico { width: 64px; height: 64px; border-radius: 18px; background: #1E1B18; display: flex; align-items: center; justify-content: center; }
.hud .ico i { width: 26px; height: 26px; border-radius: 50%; background: #E8735A; box-shadow: 0 0 0 6px rgba(232,115,90,.3); }
.hud .rows { display: flex; flex-direction: column; gap: 2px; }
.hud .row1, .hud .row2 { display: flex; gap: 16px; align-items: baseline; font-size: 24px; letter-spacing: 3px; transform-origin: 0 50%; }
.hud .row1 b { font: 800 40px "Manrope"; letter-spacing: -1px; }
.hud .row2 b.zero { color: #D45C40; }
.hud .row1.red b { color: #D9483B; }
.hud .row2 { color: #3FA372; } .hud .row2 b { font: 800 32px "Manrope"; letter-spacing: -.5px; }
.msg { max-width: 640px; padding: 14px 22px; border-radius: 24px; font: 700 34px/1.25 "Manrope"; margin-top: 10px; opacity: 0; }
.msg.in { background: #EFE6D6; border-bottom-left-radius: 6px; }
.msg.out { background: #E8735A; color: #fff; align-self: flex-end; border-bottom-right-radius: 6px; }
.c-chat { width: 760px; } .sent { align-self: flex-end; color: #A8452F !important; opacity: 0; }
.nrow { display: flex; align-items: center; gap: 16px; width: 640px; padding: 6px 0; font: 800 38px "Manrope"; opacity: 0; }
.nrow .ck { display: inline-flex !important; width: 40px; height: 40px; border-radius: 50%; background: #3FA372; color: #fff; font: 800 26px "Manrope" !important;
  align-items: center; justify-content: center; letter-spacing: 0 !important; }
.nrow .nd { font: 600 26px "Manrope"; color: #5b5650; }
.chip { margin-top: 12px; padding: 10px 22px; border-radius: 22px; background: #1E1B18; color: #F2B33D; font: 800 32px "Manrope"; opacity: 0; }
.vn { display: flex; align-items: center; gap: 16px; margin: 10px 0 6px; padding: 12px 20px; border-radius: 30px; background: #EFE6D6; }
.play { width: 0; height: 0; border-left: 26px solid #1E1B18; border-top: 16px solid transparent; border-bottom: 16px solid transparent; }
.wave { display: flex; gap: 5px; align-items: center; height: 60px; }
.wv { display: block; width: 9px; height: 60px; border-radius: 5px; background: #E8735A; transform: scaleY(.2); }
.vt { font-size: 24px; color: #5b5650; }
.q { font-size: 54px !important; line-height: 1.1 !important; max-width: 760px; opacity: 0; }
.cm { display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }
.av { width: 54px; height: 54px; border-radius: 50%; background: linear-gradient(135deg, #7E5BB0, #E36FA6); border: 3px solid #1E1B18; }
.who { font-size: 26px; letter-spacing: 1px; color: #5b5650; }
.c-price { width: 780px; } .c-price .kw { font: 800 92px/1 "Manrope" !important; color: #D45C40; letter-spacing: 2px !important; margin: 4px 0 2px; }
.av2 { background: linear-gradient(135deg, #F2B33D, #E8735A); }
.c-obj, .c-no { width: 800px; } .c-obj .msg.out, .c-no .msg.out { max-width: 680px; }
.stamp2.red { border-color: #D9483B; color: #D9483B; }
.c-fol .srow, .c-d30 .srow { width: 640px; } .c-fol .srow b, .c-d30 .srow b { font-size: 64px; letter-spacing: -2px; }
.srow b.green, .big2.green { color: #3FA372; } .srow b.coral { color: #D45C40; }
.big2 .u { font: 800 48px "Manrope"; font-style: normal; letter-spacing: -1px; color: #5b5650; }
.c-sales .sub i { font-style: normal; }
.srow { opacity: 1; } .c-fol .srow { opacity: 0; }
#caps { z-index: 6; }
.cap { position: absolute; left: 0; right: 0; top: 262px; text-align: center; opacity: 0; }
.capin { display: inline-block; max-width: 960px; padding: 10px 22px 14px; border-radius: 26px; background: rgba(255,253,248,.94);
  font: 800 58px/1.2 "Manrope"; letter-spacing: -1.5px; color: #1E1B18; }
.cap .w { display: inline-block; padding: 0 10px 4px; border-radius: 14px; }
.cap .w.on { background: #D45C40; color: #fff; }
#endc { position: absolute; left: 60px; right: 60px; top: 520px; padding: 46px 40px 42px; border-radius: 40px; text-align: center;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 12px 13px 0 #1E1B18; }
.ec-1 { font: 800 50px "Manrope"; letter-spacing: -1.5px; }
.ec-h { font-size: 40px !important; }
.ec-c { font: 800 44px "Manrope"; margin-top: 22px; }
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
    hud = ('<div class="hud"><span class="ico"><i></i></span><span class="rows">'
           '<span class="row1 mono">SALES <b class="hr">0</b></span>'
           '<span class="row2 mono">SALES CALLS <b class="zero">0</b></span></span></div>')
    endc = ('<div id="endc"><div class="ec-1">Want my DM sales setup?</div><div class="ec-h mono">Follow @nxtlvlsocial.ai</div>'
            '<div class="ec-c">and comment</div><div class="ec-kw">CLOSE</div>'
            '<div class="ec-2">I&rsquo;ll DM you the template</div></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Closer 9x16</title>
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
        {hud}{CARDS}{endc}
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
    <script type="module" src="assets/js/closer.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
