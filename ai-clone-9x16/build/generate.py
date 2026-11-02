"""AI Clone reel ("What if an AI clone of you answered every message?"): writes index.html. 1080x1920, 30 fps,
about 65 s. Account: @nxtlvlsocial.ai. This what-if reel carries a keyword CTA (comment CLONE) because there is a real
resource to send: the auto-DM tool link.

python3 build/generate.py      (from the project root, after build/voice.py)

The world is a voxel diorama in the style of the owner's reference (assets/js/clone.js): a creator street with your
studio, a fan's house, a brand's office, blocky characters with pixel-art faces, and your AI clone as a hologram of you.
This file writes the HTML layer in the cream house style: top bar with the day, captions, one card at a time in the
card band (y 430-820), the HUD (auto-replies and followers), name tags under close-ups and the CTA end card.

The month is a hypothetical (the top bar says WHAT IF); its numbers are illustrative. The one real-world claim is the
Instagram card: Meta's Instagram Platform lets professional accounts send a private reply (DM) to people who comment,
with a limit of 750 per hour per account for comments on posts and reels (Meta for Developers, Instagram Platform
overview).
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
    "youre": word(1, "you"), "asleep": word(1, "asleep"), "clone": word(1, "clone"), "answered": word(1, "answered"), "three": word(1, "three", 2), "messages": word(1, "messages"), "voice1": word(1, "voice"),
    "fan": word(2, "fan"), "advice": word(2, "advice"), "replies": word(2, "replies"), "jokes": word(2, "jokes"), "slang": word(2, "slang"), "idea": word(2, "idea"),
    "brand": word(3, "brand"), "dms": word(3, "dms"), "midnight": word(3, "midnight"), "negotiates": word(3, "negotiates"), "closes": word(3, "closes"), "double": word(3, "double"),
    "remembers": word(4, "remembers"), "name": word(4, "name"), "birthday": word(4, "birthday"), "people": word(4, "people"), "nicest": word(4, "nicest"),
    "stranger": word(5, "stranger"), "voice": word(5, "voice"), "thanks": word(5, "thanks"), "lastnight": word(5, "night"), "never": word(5, "never"), "spoken": word(5, "spoken"),
    "followers": word(6, "followers"), "doubled": word(6, "doubled"), "comment": word(6, "comment"), "honestly": word(6, "honestly"), "nicer": word(6, "nicer"), "you6": word(6, "you", 2),
    "farfetched": word(7, "farfetched"), "instagram": word(7, "instagram"), "automatic": word(7, "automatic"), "everyone": word(7, "everyone"), "seven": word(7, "seven"), "hour": word(7, "hour"),
    "setup": word(8, "setup"), "follow": word(8, "follow"), "commentk": word(8, "comment"), "clonek": word(8, "clone"), "tool": word(8, "tool"), "end": DUR,
}
T["cuts"] = [round(L[k] - .12, 3) for k in range(1, 8)]
# close-ups and the name tag under each
T["focus"] = [
    {"who": "clone", "a": round(T["clone"] - .1, 3), "b": round(T["three"] - .25, 3)},
    {"who": "you", "a": round(T["messages"] + .1, 3), "b": round(E[0] + .15, 3)},
    {"who": "fan", "a": round(T["slang"] + .25, 3), "b": round(E[1] + .2, 3)},
    {"who": "boss", "a": round(T["negotiates"] - .15, 3), "b": round(T["double"] - .15, 3)},
    {"who": "you", "a": round(T["never"] - .5, 3), "b": round(E[4] + .25, 3)},
    {"who": "you", "a": round(T["honestly"] - .1, 3), "b": round(T["nicer"] - .2, 3)},
    {"who": "clone", "a": round(T["nicer"] - .15, 3), "b": round(E[5] + .3, 3)},
]
F = T["focus"]
TAGS = [("tg-clone", F[0]["a"] + .25, F[0]["b"] - .15, "YOUR AI CLONE", "never sleeps"),
        ("tg-you1", F[1]["a"] + .25, F[1]["b"] - .2, "YOU", "fast asleep"),
        ("tg-fan", F[2]["a"] + .2, F[2]["b"] - .2, "THE FAN", "thinks it was you"),
        ("tg-boss", F[3]["a"] + .25, F[3]["b"] - .2, "THE BRAND", "just got out-negotiated"),
        ("tg-you2", F[4]["a"] + .25, F[4]["b"] - .25, "YOU", "never met them")]
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
    '<div class="card c-inbox"><span class="mono lab">INBOX &middot; WHILE YOU SLEPT</span><b class="big2"><i class="ib">0</i></b><span class="sub">replies sent, in your voice</span></div>'
    '<div class="card c-chat"><span class="mono lab">DM &middot; 2:41 PM</span>'
    '<div class="msg in m1">what&rsquo;s your best tip??</div><div class="msg out m2">post daily, answer every comment, and touch grass lol</div>'
    '<span class="sub mono sent">SENT BY YOUR CLONE</span></div>'
    '<div class="card c-deal"><span class="mono lab">BRAND DEAL &middot; 12:04 AM</span><b class="big2"><i class="dl">$1,500</i></b>'
    '<span class="stamp2 stx2">DEAL CLOSED &times;2</span></div>'
    '<div class="card c-names"><span class="mono lab">IT REMEMBERED</span>'
    + "".join(f'<div class="nrow n{k}"><b class="ck">&#10003;</b><span class="nn">{n}</span><span class="nd">{d}</span></div>'
              for k, (n, d) in enumerate([("Maya", "birthday today"), ("Jordan", "asked about editing"), ("Priya", "3rd comment this week")]))
    + '<div class="chip">&ldquo;nicest creator online fr&rdquo;</div></div>'
    '<div class="card c-voice"><span class="mono lab">VOICE NOTE &middot; @unknown_user</span>'
    '<div class="vn"><i class="play"></i><em class="wave">' + "".join(f'<i class="wv wv{k}"></i>' for k in range(26)) + '</em><span class="mono vt">0:04</span></div>'
    '<b class="ser q">&ldquo;Thanks for talking me through last night.&rdquo;</b></div>'
    '<div class="card c-follow"><span class="mono lab">FOLLOWERS &middot; DAY 30</span><b class="big2"><i class="fl">12,400</i></b><span class="stamp2 sx2">&times;2</span></div>'
    '<div class="card alert c-cmt"><div class="cm"><i class="av"></i><span class="mono who">@real_one_22</span></div><b>Honestly? Your clone is nicer than you.</b></div>'
    '<div class="card c-real"><span class="mono lab real">REAL WORLD &middot; INSTAGRAM</span><b>You can already auto-DM everyone who comments</b>'
    '<b class="bign"><i class="nb">0</i> / hour</b><span class="sub">private replies per account, per Meta&rsquo;s developer docs</span></div>'
)
CARDS += "".join(f'<div class="ptag {c}"><span class="mono">{a}</span><b>{b}</b></div>' for c, _, _, a, b in TAGS)
CTX = ["3:00 AM", "DAY 2", "DAY 5 &middot; 12:04 AM", "DAY 9", "DAY 14", "DAY 30", "REAL WORLD", "GET THE TOOL"]
REPLIES = [(T["three"], 0, 300, .8), (T["replies"], 300, 1240, 2.0), (T["negotiates"], 1240, 2900, 2.4), (T["remembers"], 2900, 6100, 3.0), (T["followers"], 6100, 14800, 3.0)]


def story():
    cu = T["cuts"]
    # 3 AM: the inbox counter
    pop(".c-inbox", T["answered"] - .2, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".ib", T["three"], 0, 300, .9, "Math.round(o.v)", "power2.out")
    add(f'tl.fromTo(".c-inbox .big2",{{scale:1.15}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["three"] + .9:.3f});')
    out(".c-inbox", E[0] - .3)
    # day 2: the fan's question and your clone's reply
    pop(".c-chat", T["fan"] - .2, "x:-110,opacity:0", .3, "back.out(1.8)")
    pop(".m1", T["advice"] - .3, "scale:.6,opacity:0", .25, "back.out(2.4)")
    pop(".m2", T["replies"] + .1, "scale:.6,opacity:0", .25, "back.out(2.4)")
    pop(".sent", T["jokes"], "y:10,opacity:0", .25)
    out(".c-chat", F[2]["a"] - .1)
    # day 5: the deal doubles
    pop(".c-deal", T["midnight"] - .2, "x:110,opacity:0", .3, "back.out(1.8)")
    count(".dl", T["double"] - .1, 1500, 3000, .7, "'$'+Math.round(o.v).toLocaleString('en-US')", "power3.out")
    pop(".stx2", T["double"] + .35, "scale:2.4,opacity:0,rotation:-20", .25, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    out(".c-deal", E[2] + .15)
    # day 9: names, birthdays, the comment
    pop(".c-names", T["remembers"] - .2, "y:40,opacity:0", .35, "back.out(1.8)")
    for k, t0 in enumerate([T["name"] - .2, T["birthday"] - .2, T["people"]]):
        pop(f".n{k}", t0, "x:-30,opacity:0", .25, "back.out(2)")
        pop(f".n{k} .ck", t0 + .15, "scale:0", .2, "back.out(3)")
    pop(".chip", T["nicest"] - .1, "scale:.6,opacity:0,rotation:-6", .3, "back.out(2.4)", "scale:1,opacity:1,rotation:-3")
    out(".c-names", E[3] + .15)
    # day 14: the voice note
    pop(".c-voice", T["voice"] - .25, "y:40,opacity:0", .3, "back.out(1.8)")
    for k in range(26):
        add(f'tl.fromTo(".wv{k}",{{scaleY:.2}},{{scaleY:{.3 + .7 * abs(((k * 7) % 11) / 10 - .4):.2f},duration:.1,yoyo:true,repeat:{int((T["never"] - T["thanks"]) / .1)},ease:"sine.inOut",immediateRender:false}},{T["thanks"] + k * .01:.3f});')
    pop(".q", T["thanks"], "y:14,opacity:0", .3)
    out(".c-voice", F[4]["a"] + .2)
    # day 30: followers double, then the comment
    pop(".c-follow", T["followers"] - .2, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".fl", T["followers"] + .1, 12400, 24800, 1.2, "Math.round(o.v).toLocaleString('en-US')", "power2.in")
    pop(".sx2", T["doubled"] + .1, "scale:2.4,opacity:0,rotation:-20", .25, "back.out(2)", "scale:1,opacity:1,rotation:-8")
    out(".c-follow", T["comment"] - .3)
    pop(".c-cmt", T["comment"] - .1, "scale:.7,opacity:0", .3, "back.out(2)")
    add(f'tl.fromTo(".c-cmt",{{x:0}},{{x:7,duration:.05,yoyo:true,repeat:5,ease:"none",immediateRender:false}},{T["nicer"]:.3f});')
    out(".c-cmt", E[5] + .2)
    # real world
    pop(".c-real", T["instagram"] - .2, "y:40,opacity:0", .35, "back.out(1.8)")
    count(".nb", T["seven"] - .1, 0, 750, 1.2, "Math.round(o.v)", "power3.out")
    add(f'tl.fromTo(".bign",{{scale:1.12}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["hour"]:.3f});')
    out(".c-real", E[6] + .15)
    # the CTA end card: follow + comment CLONE
    pop("#endc", T["setup"] - .2, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-h", T["follow"], "scale:.6,opacity:0", .3, "back.out(2.4)")
    pop(".ec-kw", T["commentk"] - .05, "scale:.5,opacity:0,rotation:-8", .35, "back.out(2.6)", "scale:1,opacity:1,rotation:-2")
    add(f'tl.fromTo(".ec-kw",{{scale:1}},{{scale:1.08,duration:.18,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{T["clonek"] + .1:.3f});')
    pop(".ec-2", T["tool"] - .5, "y:20,opacity:0", .3)
    for c, a, b, _, _ in TAGS:
        pop(f".{c}", a, "y:24,opacity:0", .25, "back.out(2)")
        out(f".{c}", b, .18)
    # HUD: auto-replies, followers
    pop(".hud", .3, "y:40,opacity:0", .3, "back.out(2)")
    for t0, a, b, d in REPLIES:
        count(".hr", t0, a, b, d, "Math.round(o.v).toLocaleString('en-US')", "power1.inOut")
    count(".hf", T["followers"] + .1, 12400, 24800, 1.2, "Math.round(o.v).toLocaleString('en-US')", "power2.in")
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
.c-cmt b { font-size: 60px; max-width: 800px; }
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
           '<span class="row1 mono">AUTO-REPLIES <b class="hr">0</b></span>'
           '<span class="row2 mono">FOLLOWERS <b class="hf">12,400</b></span></span></div>')
    endc = ('<div id="endc"><div class="ec-1">Want the setup?</div><div class="ec-h mono">Follow @nxtlvlsocial.ai</div>'
            '<div class="ec-c">and comment</div><div class="ec-kw">CLONE</div>'
            '<div class="ec-2">I&rsquo;ll DM you the tool</div></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Clone 9x16</title>
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
    <script type="module" src="assets/js/clone.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
