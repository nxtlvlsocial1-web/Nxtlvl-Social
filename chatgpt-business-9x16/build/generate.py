"""ChatGPT business-profile reel: writes index.html. 1080x1920, 30 fps, under 60 s. Account: @nxtlvlsocial.ai.

News + tutorial: on 10 November 2026 OpenAI launched "Businesses in ChatGPT" (beta). A business can claim and verify a
free profile in Business Hub (chatgpt.com/business-hub). The reel opens on the payoff (ChatGPT recommending businesses,
"YOUR BUSINESS?" missing), then four on-screen steps, what you get, who can claim today, and the CHATGPT keyword CTA.
Facts from VentureBeat and The Next Web (10 Nov 2026); the steps follow VentureBeat's walkthrough. On-screen app screens
are illustrations, not screenshots, and carry no OpenAI logo.

python3 build/generate.py      (from the project root, after build/voice.py; build/audio.py writes the mix)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
DUR = round(LINES[-1]["end"] + 1.8, 2)
L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
r3 = lambda x: round(x, 3)  # noqa: E731
A = []


def add(js):
    A.append("      " + js)


def show(sel, t, d=.35, frm="opacity:0,y:20", to="opacity:1,y:0", ease="power3.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def hide(sel, t, d=.25, props="opacity:0"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


CHECK = '<svg class="vb" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#2F7BF6"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
TICK = '<svg class="tk" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#22C55E"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# scene k runs from the start of line k (a little before) to the start of line k + 1
SC = [max(0, r3(L[k] - (0 if k == 0 else .25))) for k in range(len(LINES))]
SE = SC[1:] + [DUR]


def head(k, html, t0, t1):
    """The headline block in the top band (below the 250 px safe line)."""
    show(f"#h{k}", t0, .01 if t0 == 0 else .4, "opacity:1" if t0 == 0 else "opacity:0,y:-24", "opacity:1,y:0")
    if t1 < DUR:
        hide(f"#h{k}", t1 - .2, .2, "opacity:0,y:-16")
    return f'<div class="head" id="h{k}">{html}</div>'


def screen(k, html, t0, t1):
    """One app screen inside the phone."""
    show(f"#s{k}", t0, .01 if t0 == 0 else .35, "opacity:1" if t0 == 0 else "opacity:0,x:60", "opacity:1,x:0")
    if t1 < DUR:
        hide(f"#s{k}", t1 - .15, .2, "opacity:0,x:-60")
    return f'<div class="scr" id="s{k}">{html}</div>'


def story():
    H, S = [], []
    # 1 the hook: ChatGPT recommends two businesses; yours is missing
    H.append(head(0, '<span class="k">NEW IN CHATGPT</span><span class="t">ChatGPT now recommends <em>businesses.</em></span>', 0, SE[0]))
    S.append(screen(0, f'''<div class="bar"><b>ChatGPT</b></div>
      <div class="msg me" id="q0">Best bakery near me, open now?</div>
      <div class="msg ai" id="a0"><p>Here are two great picks nearby:</p>
        <div class="biz" id="b0"><div class="ph p1"></div><div><b>Crumb &amp; Co. {CHECK}</b><span>4.8 · open until 7 PM</span></div></div>
        <div class="biz" id="b1"><div class="ph p2"></div><div><b>Sunrise Bakes {CHECK}</b><span>4.7 · open until 6 PM</span></div></div>
        <div class="biz miss" id="b2"><div class="ph p3">?</div><div><b>YOUR BUSINESS?</b><span>not claimed</span></div></div>
      </div>''', 0, SE[0]))
    show("#q0", 0, .01, "opacity:1", "opacity:1")                      # the first frame already shows the question
    show("#a0", .12, .2, "opacity:0,y:12", "opacity:1,y:0")
    for j in range(3):
        show(f"#b{j}", .2 + j * .14, .22, "opacity:0,x:-24", "opacity:1,x:0")
    add(f'tl.fromTo("#b2",{{scale:1}},{{scale:1.05,duration:.35,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{1.5:.3f});')
    # 2 new + free
    H.append(head(1, '<span class="k">LAUNCHED NOV 10 · BETA</span><span class="t">Claim your business profile. <em>Free.</em></span>', SC[1], SE[1]))
    S.append(screen(1, '''<div class="stamp" id="st1"><span>NEW</span><b>Businesses in ChatGPT</b><i>free at launch</i></div>''', SC[1], SE[1]))
    show("#st1", SC[1] + .2, .45, "opacity:0,scale:1.6,rotation:-8", "opacity:1,scale:1,rotation:-4", "back.out(2)")
    # 3 step one: Business Hub
    H.append(head(2, '<span class="k">STEP 1 OF 4</span><span class="t">Open <em>Business Hub</em></span>', SC[2], SE[2]))
    S.append(screen(2, '''<div class="url"><span class="lk"></span><span id="u2">chatgpt.com/business-hub</span></div>
      <div class="hub"><b>Business Hub</b><p>Claim your business on ChatGPT</p><div class="box">Search your business name</div></div>''', SC[2], SE[2]))
    add(f'tl.fromTo("#u2",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:1.2,ease:"steps(25)",immediateRender:false}},{SC[2] + .4:.3f});')
    # 4 step two: search, Get Started
    H.append(head(3, '<span class="k">STEP 2 OF 4</span><span class="t">Search it. Tap <em>Get Started.</em></span>', SC[3], SE[3]))
    S.append(screen(3, '''<div class="hub"><b>Business Hub</b><div class="box on"><span id="ty3">June&rsquo;s Bakery</span><i class="cur"></i></div>
      <div class="drop" id="dd3"><b>June&rsquo;s Bakery</b><span>12 Main St · Bakery</span></div>
      <div class="btn" id="go3">Get Started</div><div class="tap" id="tap3"></div></div>''', SC[3], SE[3]))
    add(f'tl.fromTo("#ty3",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.8,ease:"steps(13)",immediateRender:false}},{SC[3] + .35:.3f});')
    show("#dd3", SC[3] + 1.2, .25, "opacity:0,y:-10", "opacity:1,y:0")
    show("#go3", SC[3] + 1.6, .25, "opacity:0,y:10", "opacity:1,y:0")
    add(f'tl.fromTo("#tap3",{{opacity:.7,scale:.2}},{{opacity:0,scale:1.6,duration:.5,ease:"power2.out",immediateRender:false}},{L[3] + 2.2:.3f});')
    add(f'tl.fromTo("#go3",{{scale:1}},{{scale:.94,duration:.1,yoyo:true,repeat:1,immediateRender:false}},{L[3] + 2.2:.3f});')
    # 5 step three: verify
    H.append(head(4, '<span class="k">STEP 3 OF 4</span><span class="t">Prove it&rsquo;s <em>yours</em></span>', SC[4], SE[4]))
    opts = ["Business phone", "Business email", "Website domain", "Shopify store"]
    S.append(screen(4, '<div class="hub"><b>Verify your business</b><p>Just one of these, depending on your business</p>' + "".join(
        f'<div class="opt" id="o{j}"><span>{o}</span>{TICK}</div>' for j, o in enumerate(opts)) + "</div>", SC[4], SE[4]))
    for j in range(4):
        show(f"#o{j}", SC[4] + .3 + j * .25, .25, "opacity:0,x:30", "opacity:1,x:0")
        add(f'tl.to("#o{j}",{{borderColor:"#a75bfc",background:"#24174a",duration:.15,yoyo:true,repeat:1,repeatDelay:.25,immediateRender:false}},{L[4] + 1.0 + j * .45:.3f});')   # each option lights up as it's named
    add(f'tl.to("#o2",{{borderColor:"#22C55E",duration:.2,immediateRender:false}},{L[4] + 3.1:.3f});')
    show("#o2 .tk", L[4] + 3.1, .3, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")      # one of them is enough
    # 6 step four: ID check, blue check
    H.append(head(5, '<span class="k">STEP 4 OF 4</span><span class="t">ID check. Get the <em>blue check.</em></span>', SC[5], SE[5]))
    S.append(screen(5, f'''<div class="idc" id="id5"><div class="idpic"></div><div class="idl"><i></i><i></i><i class="s"></i></div><div class="scan" id="sc5"></div></div>
      <div class="prof" id="pf5"><div class="ph p4"></div><div><b>June's Bakery <span id="vb5">{CHECK}</span></b><span>Verified business</span></div></div>''', SC[5], SE[5]))
    add(f'tl.fromTo("#sc5",{{y:0}},{{y:230,duration:.6,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{SC[5] + .3:.3f});')
    show("#pf5", L[5] + 1.5, .3, "opacity:0,y:20", "opacity:1,y:0")
    show("#vb5", L[5] + 2.1, .35, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    # 7 what you get
    H.append(head(6, '<span class="k">THEN</span><span class="t">Prices, stock and <em>mentions</em></span>', SC[6], SE[6]))
    S.append(screen(6, f'''<div class="prof sm"><div class="ph p4"></div><div><b>June's Bakery {CHECK}</b><span>Business Hub</span></div></div>
      <div class="row" id="r60"><span>Croissant</span><b>$3.50 · in stock</b></div>
      <div class="row" id="r61"><span>Sourdough loaf</span><b>$8.00 · in stock</b></div>
      <div class="row sh" id="r62"><span>Connect Shopify</span><i class="tg"></i></div>
      <div class="stats" id="st6"><div><b>128</b><span>mentions</span></div><div><b>34</b><span>website clicks</span></div></div>
      <div class="note">last 28 days · illustration</div>''', SC[6], SE[6]))
    for j in range(3):
        show(f"#r6{j}", SC[6] + .3 + j * .3, .25, "opacity:0,x:30", "opacity:1,x:0")
    show("#st6", L[6] + 2.0, .35, "opacity:0,y:20", "opacity:1,y:0")
    # 8 who can claim today
    H.append(head(7, '<span class="k">WHO CAN CLAIM</span><span class="t">Today, in the <em>beta</em></span>', SC[7], SE[7]))
    S.append(screen(7, '''<div class="elig" id="e70"><b>Online business</b><span>anywhere ChatGPT works</span></div>
      <div class="elig loc" id="e71"><b>Local shop</b><span>existing US listings, for now</span></div>
      <div class="note">claiming doesn't buy a higher ranking</div>''', SC[7], SE[7]))
    show("#e70", SC[7] + .3, .3, "opacity:0,y:20", "opacity:1,y:0")
    show("#e71", L[7] + 2.1, .3, "opacity:0,y:20", "opacity:1,y:0")
    # 9 the CTA
    add(f'tl.to("#phone",{{opacity:0,scale:.9,duration:.3,ease:"power2.in"}},{SC[8]:.3f});')
    H.append(head(8, '<span class="k">FREE CHECKLIST</span><span class="t">Comment</span><span class="kw">CHATGPT</span><span class="sub">and I\'ll DM you the full setup checklist</span><span class="fol">FOLLOW <b>@nxtlvlsocial.ai</b></span>', SC[8], DUR))
    add(f'tl.fromTo("#h8 .kw",{{scale:1.25}},{{scale:1,duration:.5,ease:"back.out(2)",immediateRender:false}},{SC[8] + .15:.3f});')
    return "".join(H), "".join(S)


def captions():
    html = []
    for k, ln in enumerate(LINES):
        if k == len(LINES) - 1:
            continue
        text = ln["text"]
        parts = [text] if len(text) < 44 else [p for p in re.split(r"(?<=[.?!:,])\s+(?=[A-Za-z0-9])", text) if p]
        merged = []
        for p in parts:
            if merged and len(merged[-1]) + len(p) < 40:
                merged[-1] += " " + p
            else:
                merged.append(p)
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        wi = 0
        nxt = LINES[k + 1]["start"]
        for j, p in enumerate(merged):
            n = len(p.split())
            a0 = ws[min(wi, len(ws) - 1)]["s"] - .08
            z = ws[wi + n]["s"] - .05 if wi + n < len(ws) else min(ln["end"] + .2, nxt - .15)
            wi += n
            pid = f"c{k}_{j}"
            html.append(f'<div class="cap" id="{pid}"><span>{p}</span></div>')
            add(f'tl.fromTo("#{pid}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:.15,ease:"power2.out",immediateRender:false}},{a0:.3f});')
            add(f'tl.to("#{pid}",{{opacity:0,duration:.1}},{z:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "Serif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: "Mono"; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #07050f; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #07050f; font-family: "Montserrat"; color: #fff; }
.clip { position: absolute; inset: 0; }
#bg { background: radial-gradient(900px 900px at 0% 0%, rgba(101,22,199,.55), transparent 65%), radial-gradient(900px 900px at 100% 100%, rgba(75,6,193,.5), transparent 65%), #07050f; }
#glow { position: absolute; width: 700px; height: 700px; left: 190px; top: 700px; border-radius: 50%; background: radial-gradient(circle, rgba(167,91,252,.28), transparent 70%); }
.head, .scr, .cap, .msg, .biz, .drop, .btn, .opt, .opt .tk, .prof, .stats, .elig, .row, .stamp, #vb5 { opacity: 0; }
#h0, #s0, #q0 { opacity: 1; }                 /* the very first frame shows the headline and the question */
.head { position: absolute; left: 70px; right: 70px; top: 290px; text-align: center; }
.head .k { display: inline-block; padding: 9px 18px; border: 2px solid #a75bfc; border-radius: 999px; font: 700 28px/1 "Mono"; letter-spacing: 4px; color: #b687f9; }
.head .t { display: block; margin-top: 22px; font: 800 70px/1.08 "Montserrat"; letter-spacing: -1.5px; }
.head em { font: italic 400 86px/1 "Serif"; color: #b687f9; letter-spacing: 0; }
#h8 { top: 520px; }
#h8 .t { font-size: 64px; } #h8 .kw { display: block; margin-top: 10px; font: 900 150px/1 "Montserrat"; letter-spacing: -3px; color: #fff; text-shadow: 0 0 60px rgba(167,91,252,.8); }
#h8 .sub { display: block; margin-top: 26px; font: 600 44px/1.25 "Montserrat"; color: #cfc8dd; }
#h8 .fol { display: block; margin-top: 70px; font: 700 30px/1.5 "Mono"; letter-spacing: 6px; color: #b687f9; } #h8 .fol b { display: block; font: 800 50px/1.2 "Montserrat"; letter-spacing: 0; color: #fff; }
#phone { position: absolute; left: 175px; top: 600px; width: 730px; height: 760px; border-radius: 56px; background: #0f0b1d; border: 3px solid #2c2150; box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 0 10px rgba(167,91,252,.07); overflow: hidden; }
.scr { position: absolute; inset: 0; padding: 36px 34px; }
.bar { font: 800 32px/1 "Montserrat"; padding-bottom: 22px; border-bottom: 1px solid #2c2150; margin-bottom: 26px; color: #cfc8dd; }
.msg { border-radius: 26px; padding: 18px 24px; font: 600 32px/1.3 "Montserrat"; margin-bottom: 18px; }
.msg.me { margin-left: 140px; background: #2c2150; }
.msg.ai p { color: #cfc8dd; margin-bottom: 14px; }
.biz { display: flex; gap: 18px; align-items: center; padding: 14px 16px; border-radius: 20px; background: #160f2c; margin-bottom: 12px; }
.biz b { display: flex; align-items: center; gap: 10px; font: 800 32px/1.1 "Montserrat"; } .biz span { font: 600 24px/1.4 "Montserrat"; color: #9d95b4; }
.biz.miss { border: 3px dashed #a75bfc; background: transparent; } .biz.miss b { color: #b687f9; }
.ph { flex: none; width: 74px; height: 74px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font: 800 40px/1 "Montserrat"; color: #b687f9; }
.p1 { background: linear-gradient(135deg, #d9a066, #8a5a2b); } .p2 { background: linear-gradient(135deg, #f2c94c, #c27c2c); } .p3 { background: #1d1438; } .p4 { background: linear-gradient(135deg, #f4b6c2, #a75bfc); }
.vb { width: 34px; height: 34px; flex: none; }
.stamp { position: absolute; left: 70px; right: 70px; top: 200px; padding: 40px 30px; border: 6px solid #a75bfc; border-radius: 30px; text-align: center; transform: rotate(-4deg); }
.stamp span { display: block; font: 900 92px/1 "Montserrat"; color: #a75bfc; letter-spacing: 6px; } .stamp b { display: block; margin-top: 18px; font: 800 44px/1.1 "Montserrat"; } .stamp i { display: block; margin-top: 12px; font: italic 400 50px/1 "Serif"; color: #b687f9; }
.url { display: flex; align-items: center; gap: 14px; padding: 20px 24px; border-radius: 20px; background: #1d1438; font: 700 36px/1 "Mono"; color: #fff; }
.url .lk { width: 22px; height: 26px; border-radius: 5px; border: 4px solid #22C55E; }
.hub { margin-top: 30px; } .hub > b { display: block; font: 800 46px/1.1 "Montserrat"; } .hub > p { margin-top: 10px; font: 600 28px/1.3 "Montserrat"; color: #9d95b4; }
.box { margin-top: 26px; padding: 22px 24px; border-radius: 18px; border: 2px solid #3a2d66; font: 600 32px/1 "Montserrat"; color: #6f6690; display: flex; align-items: center; }
.box.on { color: #fff; border-color: #a75bfc; } .cur { display: inline-block; width: 3px; height: 34px; background: #a75bfc; margin-left: 6px; }
.drop { margin-top: 10px; padding: 20px 24px; border-radius: 18px; background: #1d1438; } .drop b { display: block; font: 800 34px/1.2 "Montserrat"; } .drop span { font: 600 26px/1.4 "Montserrat"; color: #9d95b4; }
.btn { position: relative; margin-top: 30px; padding: 26px; border-radius: 999px; background: #fff; color: #07050f; text-align: center; font: 800 38px/1 "Montserrat"; }
.tap { position: absolute; left: 50%; top: 455px; width: 140px; height: 140px; margin-left: -70px; border-radius: 50%; background: rgba(167,91,252,.6); opacity: 0; }
.opt { display: flex; justify-content: space-between; align-items: center; margin-top: 18px; padding: 22px 24px; border-radius: 20px; background: #160f2c; border: 2px solid transparent; font: 700 36px/1 "Montserrat"; }
.tk { width: 46px; height: 46px; }
.idc { position: relative; margin: 30px auto 0; width: 560px; height: 300px; border-radius: 30px; background: #1d1438; border: 2px solid #3a2d66; overflow: hidden; }
.idpic { position: absolute; left: 36px; top: 50px; width: 160px; height: 200px; border-radius: 18px; background: linear-gradient(180deg, #3a2d66, #2c2150); }
.idl { position: absolute; left: 230px; top: 70px; right: 36px; } .idl i { display: block; height: 22px; margin-bottom: 26px; border-radius: 11px; background: #3a2d66; } .idl i.s { width: 60%; }
.scan { position: absolute; left: 0; right: 0; top: 30px; height: 6px; background: #a75bfc; box-shadow: 0 0 30px #a75bfc; }
.prof { display: flex; align-items: center; gap: 20px; margin-top: 40px; padding: 24px; border-radius: 26px; background: #160f2c; }
.prof b { display: flex; align-items: center; gap: 12px; font: 800 44px/1.1 "Montserrat"; } .prof span { font: 600 28px/1.4 "Montserrat"; color: #9d95b4; }
.prof.sm { margin-top: 0; opacity: 1; } .prof.sm b { font-size: 36px; }
.row { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; padding: 22px 24px; border-radius: 18px; background: #160f2c; font: 700 30px/1 "Montserrat"; } .row b { font-weight: 700; color: #b687f9; }
.tg { width: 76px; height: 42px; border-radius: 21px; background: #22C55E; position: relative; } .tg::after { content: ""; position: absolute; right: 5px; top: 5px; width: 32px; height: 32px; border-radius: 50%; background: #fff; }
.stats { display: flex; gap: 16px; margin-top: 20px; } .stats div { flex: 1; padding: 20px; border-radius: 20px; background: linear-gradient(135deg, #4b06c1, #6516c7); text-align: center; }
.stats b { display: block; font: 900 64px/1 "Montserrat"; } .stats span { font: 600 26px/1.4 "Montserrat"; color: #e7defa; }
.note { position: absolute; left: 0; right: 0; bottom: 26px; text-align: center; font: 700 22px/1 "Mono"; letter-spacing: 2px; color: #6f6690; }
.elig { margin-top: 40px; padding: 40px 34px; border-radius: 30px; background: #160f2c; border: 3px solid #22C55E; } .elig.loc { border-color: #f2c94c; }
.elig b { display: block; font: 800 52px/1.1 "Montserrat"; } .elig span { display: block; margin-top: 12px; font: 600 36px/1.3 "Montserrat"; color: #cfc8dd; }
.cap { position: absolute; left: 60px; right: 60px; top: 1400px; text-align: center; }
.cap span { display: inline; padding: 8px 18px; border-radius: 14px; font: 800 50px/1.45 "Montserrat"; color: #fff; background: rgba(7,5,15,.85); -webkit-box-decoration-break: clone; box-decoration-break: clone; }
"""


def main():
    heads, screens = story()
    caps = captions()
    add(f'tl.fromTo("#glow",{{x:-60,y:-30}},{{x:60,y:40,duration:{DUR},ease:"none",immediateRender:false}},0);')
    add('tl.set("#phone",{opacity:1},0);')
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, "sc": SC, "end": DUR}
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>ChatGPT Business 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"><div id="glow"></div></div>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2" data-layout-allow-overflow>{heads}<div id="phone">{screens}</div></div>
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
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
