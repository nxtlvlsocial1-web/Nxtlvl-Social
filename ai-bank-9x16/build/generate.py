"""AI Bank reel ("What if an AI ran your bank account for a month?"): writes index.html. 1080x1920, 30 fps, about 54 s.
Account: @nxtlvlsocial.ai. A "what if" reel: no keyword CTA (house rule), it ends on a question and the follow prompt.

python3 build/generate.py      (from the project root, after build/voice.py)

The world is a Three.js diorama (assets/js/bank.js) drawn on hf-seek: a cutaway home with a vault below it, the
phone company's tower, a money tree in the garden and, far away, a street in another country. This file writes the HTML
layer in the cream house style: the top bar with the day, word-by-word captions, one card at a time in the card band
(y 430-820), the bank-app HUD (savings and what the AI saved), name tags under the close-ups and the end card. Cue
times come from build/words.json and go to bank.js as window.CT.

The month is a hypothetical (the top bar says WHAT IF); its money figures are illustrative. The one real-world claim
is the Visa card: Visa says its AI scores every transaction in real time and helped prevent about $40 billion of fraud
in fiscal 2023 (CNBC, July 2024).
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
    "ai": word(1, "ai"), "bank": word(1, "bank"), "hour": word(1, "hour"), "cancels": word(1, "cancels"), "four": word(1, "four"),
    "subs": word(1, "subscriptions"), "forgot": word(1, "forgot"),
    "calls": word(2, "calls"), "phone": word(2, "phone"), "argues": word(2, "argues"), "their": word(2, "their"), "bill": word(2, "bill"),
    "drops": word(2, "drops"), "forty": word(2, "forty"),
    "two": word(3, "two"), "shoes": word(3, "shoes"), "need": word(3, "need"), "freezes": word(3, "freezes"), "card": word(3, "card"),
    "investing": word(4, "investing"), "coffee": word(4, "coffee"), "three": word(4, "three"), "up": word(4, "up"), "hundred": word(4, "hundred"),
    "someone": word(5, "someone"), "country": word(5, "country"), "tries": word(5, "tries"), "blocked": word(5, "blocked"),
    "eleven": word(5, "eleven"), "tried": word(5, "tried"),
    "thirty": word(6, "thirty"), "moves": word(6, "moves"), "savings": word(6, "savings"), "every": word(6, "every"), "cent": word(6, "cent"),
    "go": word(6, "go"), "wont": word(6, "wont"), "where": word(6, "where"),
    "farfetched": word(7, "farfetched"), "visa": word(7, "visas"), "checks": word(7, "checks"), "payment": word(7, "payment"),
    "stopped": word(7, "stopped"), "forty2": word(7, "forty"), "billion": word(7, "billion"), "fraud": word(7, "fraud"), "year": word(7, "year"),
    "trust": word(8, "trust"), "follow": word(8, "follow"), "end": DUR,
}
T["cuts"] = [round(L[k] - .12, 3) for k in range(1, 8)]
# face close-ups (the camera on a face) and the name tag under each
T["focus"] = [
    {"who": "orb", "a": round(T["ai"] - .15, 3), "b": round(T["hour"] - .3, 3)},
    {"who": "you", "a": round(T["forgot"] - .15, 3), "b": round(E[0] + .12, 3)},
    {"who": "robot", "a": round(T["argues"] - .1, 3), "b": round(T["bill"] - .3, 3)},
    {"who": "you", "a": round(T["shoes"] - .9, 3), "b": round(T["freezes"] - .25, 3)},
    {"who": "thief", "a": round(T["someone"] - .05, 3), "b": round(T["blocked"] - .55, 3)},
    {"who": "you", "a": round(T["tried"] - 1.1, 3), "b": round(E[4] + .2, 3)},
    {"who": "you", "a": round(T["go"] + .05, 3), "b": round(E[5] + .25, 3)},
]
F = T["focus"]
TAGS = [("tg-ai", F[0]["a"] + .25, F[0]["b"] - .15, "YOUR BANK&rsquo;S AI", "in charge of your money"),
        ("tg-you1", F[1]["a"] + .25, F[1]["b"] - .2, "YOU", "four subscriptions lighter"),
        ("tg-bot", F[2]["a"] + .25, F[2]["b"] - .2, "YOUR PHONE COMPANY&rsquo;S AI", "losing the argument"),
        ("tg-you2", F[3]["a"] + .25, F[3]["b"] - .2, "YOU &middot; 2:04 AM", "cart full"),
        ("tg-thief", F[4]["a"] + .25, F[4]["b"] - .2, "SOMEONE IN ANOTHER COUNTRY", "with your card number"),
        ("tg-you3", F[5]["a"] + .25, F[5]["b"] - .25, "YOU", "fast asleep")]
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


MONEY = "'$'+o.v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})"
SUBS = [("STREAMFLIX", "15.99"), ("GYMPASS", "39.00"), ("TUNES+", "10.99"), ("CLOUDBOX", "3.98")]
CARDS = (
    '<div class="card c-subs"><span class="mono lab">SUBSCRIPTIONS YOU FORGOT</span>'
    + "".join(f'<div class="srow s{k}"><span class="sn">{n}</span><span class="sp mono">${p}/mo</span><i class="sx"></i></div>' for k, (n, p) in enumerate(SUBS))
    + '<span class="sub">saved <b class="coral inl">$69.96</b> a month</span></div>'
    '<div class="card c-bill"><span class="mono lab">PHONE BILL &middot; NEGOTIATED BY AI</span><b class="big2"><i class="bn">$89.00</i></b>'
    '<span class="stamp2 st40">&minus;40%</span></div>'
    '<div class="stamp st-frozen">CARD FROZEN</div>'
    '<div class="card c-why"><span class="mono lab">REASON</span><b class="ser big">your 6th pair this year.</b></div>'
    '<div class="card c-inv"><span class="mono lab">INVESTED &middot; COFFEE MONEY</span>'
    '<svg class="spark" viewBox="0 0 340 80"><polyline class="spk" points="0,70 40,66 80,64 120,58 160,55 200,44 240,40 280,26 340,10" fill="none" stroke="#3FA372" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    '<b class="big2 green">+$<i class="iv">0</i></b></div>'
    '<div class="card alert c-fraud"><span class="mono lab">PAYMENT ATTEMPT &middot; 03:12 AM</span><b>6,420 km from you</b>'
    '<span class="sub mono">CARD &bull;&bull;&bull;&bull; 4821 &middot; $2,400.00</span></div>'
    '<div class="stamp st-blocked">BLOCKED</div>'
    '<div class="card c-rewind"><span class="mono lab">BLOCKED</span><b class="big2"><i class="rw">0</i> s</b><span class="sub">before they even tried</span></div>'
    '<div class="card alert c-xfer"><span class="mono lab">TRANSFER COMPLETE</span><b>ALL SAVINGS</b>'
    '<span class="sub mono">TO: &bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull; &middot; REASON: &mdash;</span></div>'
    '<div class="card c-real"><span class="mono lab real">REAL WORLD &middot; VISA</span><b>AI already checks every card payment in real time</b>'
    '<span class="sub">fraud it helped stop in a single year</span><b class="bign">$<i class="nb">0</i></b></div>'
    '<div class="card c-q"><b class="ser big">How much would you</b><b class="ser big coral">trust it with?</b></div>'
)
CARDS += "".join(f'<div class="ptag {c}"><span class="mono">{a}</span><b>{b}</b></div>' for c, _, _, a, b in TAGS)
CTX = ["DAY 1", "DAY 3", "DAY 9 &middot; 2:04 AM", "WEEK 2", "DAY 21 &middot; 3:12 AM", "DAY 30", "REAL WORLD", "YOUR CALL"]
SAVED = [(T["cancels"] + 1.3, 0, 69.96), (T["forty"] + .3, 69.96, 105.56), (T["freezes"] + .2, 105.56, 294.56), (T["hundred"] - .2, 294.56, 594.56)]


def story():
    cu = T["cuts"]
    # day 1: the subscriptions, crossed out one by one
    pop(".c-subs", T["ai"] - .2, "y:40,opacity:0", .35, "back.out(1.8)")
    for k in range(4):
        tk = T["cancels"] + k * .32
        add(f'tl.fromTo(".s{k} .sx",{{scaleX:0}},{{scaleX:1,duration:.18,ease:"power2.out",immediateRender:false}},{tk:.3f});')
        add(f'tl.to(".s{k}",{{opacity:.45,duration:.15}},{tk + .1:.3f});')
    pop(".c-subs .sub", T["cancels"] + 1.3, "y:14,opacity:0", .25)
    out(".c-subs", T["forgot"] - .2)
    # day 3: the bill comes down
    pop(".c-bill", T["bill"] - .2, "x:-120,opacity:0", .3, "back.out(1.8)")
    count(".bn", T["drops"], 89, 53.4, .8, MONEY, "power3.out")
    pop(".st40", T["forty"] - .05, "scale:2.4,opacity:0,rotation:-20", .25, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    out(".c-bill", E[1] + .15)
    # day 9: frozen, and why
    pop(".st-frozen", T["freezes"] - .05, "scale:2.4,opacity:0,rotation:16", .25, "back.out(2)", "scale:1,opacity:1,rotation:5")
    add(f'tl.fromTo(".st-frozen",{{x:0}},{{x:8,duration:.04,yoyo:true,repeat:5,ease:"none",immediateRender:false}},{T["freezes"] + .2:.3f});')
    out(".st-frozen", T["card"] + .5, .18)
    pop(".c-why", T["card"] + .45, "y:30,opacity:0", .3, "back.out(1.8)")
    out(".c-why", E[2] + .15)
    # week 2: the coffee money grows
    pop(".c-inv", T["coffee"] - .2, "x:120,opacity:0", .3, "back.out(1.8)")
    add(f'tl.fromTo(".spk",{{strokeDashoffset:420}},{{strokeDashoffset:0,duration:2.2,ease:"power1.inOut",immediateRender:false}},{T["coffee"] + .1:.3f});')
    count(".iv", T["three"], 0, 300, T["hundred"] - T["three"] + .3, "Math.round(o.v)", "power2.in")
    add(f'tl.fromTo(".c-inv .big2",{{scale:1.2}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["hundred"] + .1:.3f});')
    out(".c-inv", E[3] + .15)
    # day 21: the attempt, blocked, eleven seconds early
    pop(".c-fraud", T["someone"] + .2, "scale:1.4,opacity:0", .25, "back.out(2)")
    out(".c-fraud", T["blocked"] - .3)
    pop(".st-blocked", T["blocked"] - .1, "scale:2.6,opacity:0,rotation:-16", .22, "back.out(2)", "scale:1,opacity:1,rotation:-6")
    add(f'tl.fromTo(".st-blocked",{{x:0}},{{x:9,duration:.04,yoyo:true,repeat:7,ease:"none",immediateRender:false}},{T["blocked"] + .15:.3f});')
    out(".st-blocked", T["eleven"] - .1, .15)
    pop(".c-rewind", T["eleven"], "y:30,opacity:0", .25, "back.out(2)")
    count(".rw", T["eleven"] + .05, 0, 11, .6, "Math.round(o.v)", "power2.out")
    out(".c-rewind", E[4] + .1)
    # day 30: everything moves
    pop(".c-xfer", T["savings"] - .1, "scale:1.5,opacity:0", .25, "back.out(2)")
    add(f'tl.fromTo(".c-xfer",{{x:0}},{{x:6,duration:.05,yoyo:true,repeat:5,ease:"none",immediateRender:false}},{T["cent"]:.3f});')
    out(".c-xfer", T["wont"] - .3)
    # real world
    pop(".c-real", T["visa"] - .2, "y:40,opacity:0", .35, "back.out(1.8)")
    count(".nb", T["forty2"] - .1, 0, 4e10, 1.6, "Math.round(o.v).toLocaleString('en-US')", "power3.out")
    add(f'tl.fromTo(".bign",{{scale:1.12}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["forty2"] + 1.5:.3f});')
    out(".c-real", E[6] + .15)
    # the question, then the follow card (no keyword: house rule for what-if reels)
    pop(".c-q", T["trust"] - .45, "scale:.8,opacity:0", .4, "back.out(1.8)")
    out(".c-q", T["follow"] - .25)
    pop("#endc", T["follow"] - .15, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-kw", T["follow"] + .05, "scale:.6,opacity:0", .3, "back.out(2.2)")
    pop(".ec-2", T["follow"] + .25, "y:20,opacity:0", .3)
    pop(".ec-h", T["follow"] + .5, "y:20,opacity:0", .3)
    for c, a, b, _, _ in TAGS:
        pop(f".{c}", a, "y:24,opacity:0", .25, "back.out(2)")
        out(f".{c}", b, .18)
    # the bank-app HUD: savings, and what the AI has saved you
    pop(".hud", .25, "y:40,opacity:0", .3, "back.out(2)")
    for t0, a, b in SAVED:
        count(".hsv", t0, a, b, .6, "'+'+" + MONEY.replace("'$'+", "'$'+"), "power2.out")
        add(f'tl.fromTo(".hud .row2",{{scale:1.15}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{t0:.3f});')
    count(".hsa", T["moves"] + .3, 48210, 0, T["go"] - T["moves"] + .2, MONEY, "power2.in")
    add(f'tl.set(".hud .row1",{{attr:{{class:"row1 red"}}}},{T["moves"] + .3:.3f});')
    add(f'tl.fromTo(".hud",{{x:0}},{{x:7,duration:.05,yoyo:true,repeat:9,ease:"none",immediateRender:false}},{T["go"] + .1:.3f});')
    out(".hud", E[5] + .4, .2, "opacity:0,y:30")
    # top bar: progress, the WHAT IF light, the day
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
.card, .stamp, #endc, .ec-kw, .ec-2, .ec-h, .ptag, .hud, .stamp2, .c-subs .sub { opacity: 0; }
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
.hud .row1.red b { color: #D9483B; }
.hud .row2 { color: #3FA372; } .hud .row2 b { font: 800 32px "Manrope"; letter-spacing: -.5px; }
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
    hud = ('<div class="hud"><span class="ico"><i></i></span><span class="rows">'
           '<span class="row1 mono">SAVINGS <b class="hsa">$48,210.00</b></span>'
           '<span class="row2 mono">AI SAVED <b class="hsv">+$0.00</b></span></span></div>')
    endc = ('<div id="endc"><div class="ec-1">Follow for more</div><div class="ec-kw">what ifs</div>'
            '<div class="ec-2">new scenario every week</div><div class="ec-h mono">@nxtlvlsocial.ai</div></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Bank 9x16</title>
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
    <script type="module" src="assets/js/bank.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
