"""ChatGPT business skit (the tutorial skit format, nxtlvl-social-video section 8): writes index.html. 1080x1920, 30 fps,
under 60 s. Account: @nxtlvlsocial.ai.

Upper half: a phone (right) that carries every screen, acted out step by step, and a legal-pad list of the four steps
(left) that highlights the current one and ticks off the finished ones. Lower half: one cozy 3D office (assets/js/skit.js)
where Marcus, a real estate agent, talks with Byte, his AI sidekick. Hook: the ChatGPT answer that recommends Prime Nest;
the payoff shows the same question with Keystone on top. Steps per VentureBeat's walkthrough of Businesses in ChatGPT (beta, launched
10 Nov 2026). Honest beat: claiming doesn't buy a ranking. End card: a sticky note over the dimmed office (share prompt, CHATGPT
keyword, follow). Screens are
illustrations without OpenAI's logo.

python3 build/generate.py      (from the project root, after build/voice.py; build/audio.py writes the mix)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
WHO = [ln["speaker"] for ln in LINES]
TK = {ln["take"]: k for k, ln in enumerate(LINES)}       # line index by take id, so cuts never shift the cues
END_IN = round(E[-1] + .45, 3)            # the end card
DUR = round(END_IN + 2.3, 2)
r3 = lambda x: round(x, 3)  # noqa: E731
A = []


def add(js):
    A.append("      " + js)


def show(sel, t, d=.3, frm="opacity:0,y:16", to="opacity:1,y:0", ease="power3.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def hide(sel, t, d=.22, props="opacity:0"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


CHECK = '<svg class="vb" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#2F7BF6"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
TICK = '<svg class="tk" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#22C55E"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STEP_LINES = [TK["05"], TK["08"], TK["11"], TK["14"]]
PANEL_IN = .25
HOOK = (.35, r3(L[TK["05"]] - .35))
SCR = [(r3(L[s] - .35), r3(L[STEP_LINES[k + 1]] - .35) if k < 3 else r3(L[TK["17"]] - .35)) for k, s in enumerate(STEP_LINES)]
PAY = (r3(L[TK["17"]] - .35), END_IN)
PAD = ["Open the hub", "Find your agency", "Prove it&rsquo;s yours", "Quick ID check"]


def screen(k, t0, t1, body):
    show(f"#s{k}", t0, .3, "opacity:0,y:40", "opacity:1,y:0")
    hide(f"#s{k}", t1 - .12, .18, "opacity:0,y:-40")
    return f'<div class="scr" id="s{k}">{body}</div>'


def story():
    # one phone (right) that carries every screen, and a notepad of the four steps (left) that ticks them off
    S = []
    # the hook: the ChatGPT answer that started it all, Prime Nest on top; the blue check shows why
    S.append(screen(5, HOOK[0], HOOK[1], f'''<div class="bar2"><b>ChatGPT</b></div>
      <div class="msg me">Best real estate agent near me?</div>
      <div class="biz top" id="bh0"><div class="ph p1"></div><div><b>Prime Nest Realty <span id="vbh">{CHECK}</span></b><span>open now · 4.6</span></div></div>
      <div class="biz dim" id="bh1"><div class="ph p4"></div><div><b>Keystone Realty</b><span>not claimed</span></div></div>
      <div class="note" id="nh"><span>Free · since Nov 10</span></div>'''))
    show("#bh0", HOOK[0] + .5, .35, "opacity:0,x:-30", "opacity:1,x:0")
    show("#bh1", HOOK[0] + .8, .35, "opacity:0,x:-30", "opacity:1,x:0")
    show("#vbh", L[TK["02"]] + .3, .35, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    show("#nh", L[TK["04"]] + .05, .3, "opacity:0,scale:.8", "opacity:1,scale:1", "back.out(2)")
    S.append(screen(0, *SCR[0], f'''<div class="url"><span class="lk"></span><span id="u0">chatgpt.com/business-hub</span></div>
      <div class="hub"><b>Business Hub</b><p>Claim your business on ChatGPT</p><div class="box">Search your business name</div>
      <div class="note" id="n0"><span>No paid plan</span><span>No ads account</span></div></div>'''))
    add(f'tl.fromTo("#u0",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:1.1,ease:"steps(25)",immediateRender:false}},{SCR[0][0] + .5:.3f});')
    show("#n0", L[TK["07"]] - .05, .3, "opacity:0,scale:.8", "opacity:1,scale:1", "back.out(2)")
    S.append(screen(1, *SCR[1], '''<div class="url"><span class="lk"></span><span>chatgpt.com/business-hub</span></div>
      <div class="hub"><div class="box on"><span id="ty1">Keystone Realty</span><i class="cur"></i></div>
      <div class="drop" id="dd1"><b>Keystone Realty</b><span>Real estate · 48 Oak Street</span></div>
      <div class="drop add" id="ad1">+ Not listed? Add it yourself</div>
      <div class="btn" id="go1">Get Started</div><div class="tap" id="tap1"></div></div>'''))
    add(f'tl.fromTo("#ty1",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.8,ease:"steps(15)",immediateRender:false}},{SCR[1][0] + .4:.3f});')
    show("#dd1", SCR[1][0] + 1.25, .22, "opacity:0,y:-10", "opacity:1,y:0")
    show("#go1", SCR[1][0] + 1.6, .22, "opacity:0,y:10", "opacity:1,y:0")
    add(f'tl.fromTo("#tap1",{{opacity:.7,scale:.2}},{{opacity:0,scale:1.6,duration:.45,ease:"power2.out",immediateRender:false}},{E[TK["08"]] - .5:.3f});')
    add(f'tl.fromTo("#go1",{{scale:1}},{{scale:.94,duration:.1,yoyo:true,repeat:1,immediateRender:false}},{E[TK["08"]] - .5:.3f});')
    show("#ad1", L[TK["10"]] + .1, .25, "opacity:0,x:-20", "opacity:1,x:0")
    opts = ["Business phone", "Business email", "Website domain", "Shopify store"]
    S.append(screen(2, *SCR[2], '<div class="hub"><b>Verify your business</b><p>Just one of these</p>' + "".join(
        f'<div class="opt" id="o{j}"><span>{o}</span>{TICK}</div>' for j, o in enumerate(opts)) + '<div class="note" id="n2"><span>Use the email on your website</span></div></div>'))
    w11 = [w for w in WORDS if w["line"] == LINES[TK["11"]]["line"]]
    for j, o in enumerate(["phone,", "email,", "website,", "Shopify."]):
        tw = next((w["s"] for w in w11 if w["w"].lower().startswith(o[:5].lower())), L[TK["11"]] + 1.5 + j * .5)
        add(f'tl.to("#o{j}",{{borderColor:"#8B5CF6",background:"#EFE7FF",duration:.12,yoyo:true,repeat:1,repeatDelay:.22,immediateRender:false}},{tw:.3f});')
    add(f'tl.to("#o1",{{borderColor:"#22C55E",duration:.2,immediateRender:false}},{L[TK["13"]]:.3f});')
    show("#o1 .tk", L[TK["13"]], .3, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    show("#n2", L[TK["13"]] + .1, .3, "opacity:0,scale:.8", "opacity:1,scale:1", "back.out(2)")
    S.append(screen(3, *SCR[3], f'''<div class="idc"><div class="idpic"></div><div class="idl"><i></i><i></i><i class="s"></i></div><div class="scan" id="sc3"></div></div>
      <div class="scrawl" id="sw3">not a headshot</div>
      <div class="prof" id="pf3"><div class="ph p4"></div><div><b>Keystone Realty <span id="vb3">{CHECK}</span></b><span>Verified business</span></div></div>'''))
    add(f'tl.fromTo("#sc3",{{y:0}},{{y:190,duration:.55,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{SCR[3][0] + .4:.3f});')
    show("#pf3", E[TK["14"]] - .9, .3, "opacity:0,y:20", "opacity:1,y:0")
    show("#vb3", E[TK["14"]] - .45, .35, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    show("#sw3", L[TK["16"]], .3, "opacity:0,rotation:-10,scale:1.3", "opacity:1,rotation:-6,scale:1", "back.out(2)")
    # the payoff: the same question as the hook, and now Keystone is on top
    S.append(screen(4, *PAY, f'''<div class="bar2"><b>ChatGPT</b></div>
      <div class="msg me">Best real estate agent near me?</div>
      <div class="biz top" id="bz0"><div class="ph p4"></div><div><b>Keystone Realty {CHECK}</b><span>open now · showings today</span></div></div>
      <div class="biz"><div class="ph p1"></div><div><b>Prime Nest Realty {CHECK}</b><span>open now · 4.6</span></div></div>
      <div class="stamp" id="st4"><b>DOESN&rsquo;T BUY RANKING</b><span>it gives ChatGPT your real details</span></div>'''))
    show("#bz0", PAY[0] + .4, .35, "opacity:0,x:-30", "opacity:1,x:0")
    show("#st4", L[TK["18"]] + .2, .35, "opacity:0,scale:1.5,rotation:-10", "opacity:1,scale:1,rotation:-5", "back.out(2)")
    # the notepad: four steps; the current one gets the marker, finished ones a tick
    items = "".join(f'<div class="it" id="it{k}"><span class="num">{k + 1}</span>{TICK}<b>{PAD[k]}</b><i class="hl" id="hl{k}"></i></div>' for k in range(4))
    pad = f'<div id="pad"><div class="pt"><span class="pa">4 steps</span><span class="pb">all done!</span></div>{items}</div>'
    show("#pad", SCR[0][0] - .1, .45, "opacity:0,x:-60,rotation:-8", "opacity:1,x:0,rotation:-3", "back.out(1.6)")
    for k in range(4):
        add(f'tl.fromTo("#hl{k}",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power2.out",immediateRender:false}},{SCR[k][0] + .1:.3f});')
        add(f'tl.to("#it{k}",{{opacity:1,duration:.2,immediateRender:false}},{SCR[k][0]:.3f});')
        t_done = SCR[k][1] - .3
        add(f'tl.to("#hl{k}",{{opacity:0,duration:.2,immediateRender:false}},{t_done:.3f});')
        add(f'tl.to("#it{k} .num",{{opacity:0,duration:.12,immediateRender:false}},{t_done:.3f});')
        show(f"#it{k} .tk", t_done, .3, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    hide("#pad .pa", PAY[0], .15)
    show("#pad .pb", PAY[0] + .1, .3, "opacity:0,scale:.7", "opacity:1,scale:1", "back.out(2)")
    show("#phone", HOOK[0] - .2, .5, "opacity:0,y:60,rotation:6", "opacity:1,y:0,rotation:2", "back.out(1.4)")
    add('tl.set("#phone",{x:-162},0);')                     # centred for the hook, then it makes room for the notepad
    add(f'tl.to("#phone",{{x:0,duration:.55,ease:"power3.inOut"}},{SCR[0][0] - .45:.3f});')
    hide("#phone", END_IN - .05, .3, "opacity:0,y:-30")
    hide("#pad", END_IN - .05, .3, "opacity:0,x:-40")
    # the end card: a sticky note over the dimmed office
    show("#endc", END_IN, .4, "opacity:0", "opacity:1")
    show("#endc .note2", END_IN + .05, .5, "opacity:0,y:60,rotation:-9,scale:.9", "opacity:1,y:0,rotation:-2,scale:1", "back.out(1.5)")
    return pad + f'<div id="phone"><div class="isl"></div><div class="sbar"><b>9:41</b></div><div class="wbody">{"".join(S)}</div></div>'


def captions():
    html = []
    for k, ln in enumerate(LINES):
        text = ln["text"]
        parts = [p for p in re.split(r"(?<=[.?!,])\s+(?=[A-Za-z0-9])", text) if p]
        merged = []
        for p in parts:
            if merged and len(merged[-1]) + len(p) < 30:
                merged[-1] += " " + p
            else:
                merged.append(p)
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        wi = 0
        nxt = LINES[k + 1]["start"] if k + 1 < len(LINES) else END_IN
        for j, p in enumerate(merged):
            n = len(p.split())
            a0 = ws[min(wi, len(ws) - 1)]["s"] - .06
            z = ws[wi + n]["s"] - .04 if wi + n < len(ws) else min(ln["end"] + .15, nxt - .08)
            wi += n
            pid = f"c{k}_{j}"
            html.append(f'<div class="cap sp-{ln["speaker"]}" id="{pid}"><span>{p}</span></div>')
            add(f'tl.fromTo("#{pid}",{{opacity:0,y:6}},{{opacity:1,y:0,duration:.12,ease:"power2.out",immediateRender:false}},{a0:.3f});')
            add(f'tl.to("#{pid}",{{opacity:0,duration:.08}},{z:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Garamond"; font-weight: 400 800; src: url("assets/fonts/EBGaramond.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "Mono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #2A1E16; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #2A1E16; font-family: "Manrope"; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.scr, .note, .drop, .btn, .opt .tk, .prof, #vb3, #vbh, .stamp, .scrawl, .cap, #phone, #pad, .it .tk, #endc, #endc .note2 { opacity: 0; }
#phone { position: absolute; left: 372px; top: 262px; width: 660px; height: 740px; border-radius: 64px; background: #101114; padding: 16px; box-shadow: 0 30px 70px rgba(0,0,0,.55), inset 0 0 0 3px #2A2C33; transform: rotate(2deg); }
#phone .isl { position: absolute; left: 50%; top: 30px; width: 150px; height: 34px; margin-left: -75px; border-radius: 20px; background: #000; z-index: 2; }
#phone .sbar { position: absolute; left: 16px; right: 16px; top: 16px; height: 70px; border-radius: 48px 48px 0 0; background: #F7F4EE; padding: 26px 0 0 50px; } #phone .sbar b { font: 800 24px/1 "Manrope"; color: #14161C; }
#phone .wbody { position: absolute; left: 16px; right: 16px; top: 86px; bottom: 16px; border-radius: 0 0 48px 48px; background: #F7F4EE; overflow: hidden; }
.scr { position: absolute; inset: 0; padding: 8px 24px; color: #14161C; }
.url { display: flex; align-items: center; gap: 10px; padding: 14px 16px; border-radius: 14px; background: #fff; border: 2px solid #E2DACD; font: 700 27px/1 "Mono"; }
.url .lk { flex: none; width: 16px; height: 20px; border-radius: 4px; border: 4px solid #22C55E; }
.hub { margin-top: 16px; } .hub > b { display: block; font: 800 38px/1.1 "Manrope"; } .hub > p { margin-top: 6px; font: 600 25px/1.3 "Manrope"; color: #6A6878; }
.box { margin-top: 14px; padding: 15px 18px; border-radius: 14px; border: 2px solid #D9D1C4; background: #fff; font: 600 29px/1 "Manrope"; color: #9A93A6; display: flex; align-items: center; }
.box.on { color: #14161C; border-color: #8B5CF6; } .cur { display: inline-block; width: 3px; height: 32px; background: #8B5CF6; margin-left: 6px; }
.drop { margin-top: 8px; padding: 12px 18px; border-radius: 14px; background: #fff; border: 2px solid #E2DACD; } .drop b { display: block; font: 800 29px/1.2 "Manrope"; } .drop span { font: 600 23px/1.4 "Manrope"; color: #6A6878; }
.drop.add { font: 800 26px/1 "Manrope"; color: #8B5CF6; border-style: dashed; border-color: #8B5CF6; }
.btn { position: relative; margin-top: 14px; padding: 18px; border-radius: 999px; background: #14161C; color: #fff; text-align: center; font: 800 31px/1 "Manrope"; }
.tap { position: absolute; left: 50%; top: 330px; width: 120px; height: 120px; margin-left: -60px; border-radius: 50%; background: rgba(139,92,246,.55); opacity: 0; }
.opt { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding: 14px 18px; border-radius: 14px; background: #fff; border: 2px solid #E2DACD; font: 700 30px/1 "Manrope"; }
.tk { width: 38px; height: 38px; } .vb { width: 32px; height: 32px; flex: none; }
.note { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; } .note span { padding: 10px 16px; border-radius: 999px; background: #E7F7EC; color: #15803D; font: 800 25px/1 "Manrope"; }
.idc { position: relative; margin: 20px auto 0; width: 560px; height: 236px; border-radius: 24px; background: #fff; border: 2px solid #E2DACD; overflow: hidden; }
.idpic { position: absolute; left: 26px; top: 32px; width: 130px; height: 170px; border-radius: 14px; background: linear-gradient(180deg, #D9D1C4, #BFB4A4); }
.idl { position: absolute; left: 186px; top: 52px; right: 26px; } .idl i { display: block; height: 20px; margin-bottom: 24px; border-radius: 10px; background: #E6DFD3; } .idl i.s { width: 60%; }
.scan { position: absolute; left: 0; right: 0; top: 20px; height: 6px; background: #8B5CF6; box-shadow: 0 0 24px #8B5CF6; }
.scrawl { position: absolute; left: 60px; top: 272px; font: italic 600 40px/1 "Garamond"; color: #E8735A; transform: rotate(-6deg); }
.prof { display: flex; align-items: center; gap: 16px; margin-top: 76px; padding: 18px; border-radius: 20px; background: #fff; border: 2px solid #E2DACD; }
.prof b { display: flex; align-items: center; gap: 10px; font: 800 34px/1.1 "Manrope"; } .prof span { font: 600 24px/1.4 "Manrope"; color: #6A6878; }
.ph { flex: none; width: 62px; height: 62px; border-radius: 14px; } .p1 { background: linear-gradient(135deg, #7DBA6A, #1F7A4D); } .p4 { background: linear-gradient(135deg, #F2C94C, #1C2A4A); }
.bar2 { font: 800 28px/1 "Manrope"; color: #6A6878; padding: 6px 0 14px; border-bottom: 1px solid #E2DACD; margin-bottom: 16px; }
.msg.me { margin-left: 80px; padding: 14px 20px; border-radius: 22px; background: #ECE6DB; font: 700 28px/1.3 "Manrope"; margin-bottom: 16px; }
.biz { display: flex; gap: 14px; align-items: center; padding: 14px; border-radius: 18px; background: #fff; border: 2px solid #E2DACD; margin-bottom: 12px; }
.biz b { display: flex; align-items: center; gap: 8px; font: 800 29px/1.1 "Manrope"; } .biz span { font: 600 23px/1.4 "Manrope"; color: #6A6878; }
.biz.top { border-color: #2F7BF6; box-shadow: 0 0 0 4px rgba(47,123,246,.15); opacity: 0; } .biz.dim { opacity: 0; } .biz.dim > * { filter: grayscale(1); } .biz.dim b { color: #8A8496; }
.stamp { position: absolute; left: 30px; right: 30px; bottom: 26px; padding: 14px; border: 5px solid #E8735A; border-radius: 16px; text-align: center; color: #E8735A; background: rgba(255,250,240,.94); transform: rotate(-5deg); }
.stamp b { display: block; font: 900 36px/1 "Manrope"; letter-spacing: 2px; } .stamp span { display: block; margin-top: 8px; font: italic 600 28px/1 "Garamond"; color: #6A4A3A; }
#pad { position: absolute; left: 44px; top: 300px; width: 316px; padding: 26px 22px 18px; border-radius: 10px; background: #FFF6C9; box-shadow: 0 22px 44px rgba(0,0,0,.45); transform: rotate(-3deg);
  background-image: repeating-linear-gradient(180deg, transparent 0 63px, rgba(90,120,200,.22) 63px 65px); }
#pad::before { content: ""; position: absolute; left: 0; right: 0; top: -14px; height: 28px; background: #C9473A; border-radius: 8px 8px 4px 4px; }
#pad .pt { position: relative; height: 44px; font: italic 700 44px/1 "Garamond"; color: #2A2440; margin-bottom: 14px; } #pad .pt span { position: absolute; left: 0; top: 0; } #pad .pb { color: #15803D; opacity: 0; }
.it { position: relative; display: flex; align-items: center; gap: 14px; min-height: 104px; opacity: .45; }
.it .num { flex: none; width: 48px; height: 48px; border-radius: 50%; border: 3px solid #2A2440; font: 800 28px/42px "Manrope"; text-align: center; color: #2A2440; }
.it .tk { position: absolute; left: 4px; width: 44px; height: 44px; }
.it b { position: relative; z-index: 1; font: 800 33px/1.12 "Manrope"; color: #2A2440; }
.it .hl { position: absolute; left: 58px; right: -6px; top: 50%; height: 64px; margin-top: -32px; background: rgba(255,140,90,.45); border-radius: 6px; transform-origin: left center; transform: scaleX(0); z-index: 0; }
.cap { position: absolute; left: 40px; right: 40px; top: 1036px; text-align: center; }
.cap span { display: inline; padding: 6px 18px; border-radius: 14px; background: rgba(20,14,10,.78); font: 800 44px/1.5 "Manrope"; color: #FFFFFF; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.cap.sp-byte span { color: #9EF5D2; }
#endc { position: absolute; inset: 0; background: rgba(22,15,10,.66); }
#endc .note2 { position: absolute; left: 110px; right: 110px; top: 470px; padding: 70px 54px 56px; border-radius: 12px; background: #FFF6C9; box-shadow: 0 30px 70px rgba(0,0,0,.5); text-align: center; color: #2A2440; }
#endc .note2::before { content: ""; position: absolute; left: 50%; top: -22px; width: 150px; height: 44px; margin-left: -75px; background: rgba(255,255,255,.55); transform: rotate(-3deg); }
#endc .e0 svg { width: 110px; height: 110px; }
#endc .e1 { margin-top: 18px; font: 700 62px/1.12 "Garamond"; }
#endc .e2 { margin-top: 34px; font: 800 40px/1.45 "Manrope"; } #endc .e2 b { padding: 4px 14px; border-radius: 10px; background: #E8735A; color: #fff; }
#endc .e3 { margin-top: 22px; font: 700 31px/1.4 "Manrope"; color: #6A5A48; }
"""


def main():
    ui = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, "who": WHO, "end": DUR, "cuts": [], "stepLines": STEP_LINES, "tk": TK, "panelIn": PANEL_IN, "hook": HOOK, "endIn": END_IN, "scr": SCR, "pay": PAY}
    house = '<svg viewBox="0 0 64 64"><path d="M8 30 L32 10 L56 30" stroke="#F2C94C" stroke-width="5" fill="none" stroke-linejoin="round"/><rect x="16" y="28" width="32" height="26" rx="3" fill="#F2C94C"/><circle cx="46" cy="44" r="12" fill="#2F7BF6"/><path d="M40 44.5l4 4 8-8" stroke="#fff" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    endc = (f'<div id="endc"><div class="note2"><div class="e0">{house}</div><div class="e1">Send this to an agent who&rsquo;s invisible on ChatGPT</div>'
            '<div class="e2">Comment <b>CHATGPT</b> for the full checklist</div><div class="e3">Follow @nxtlvlsocial.ai for the next one</div></div></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>ChatGPT Skit 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-hold data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>{ui}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4">{caps}</div>
      <div id="end" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5">{endc}</div>
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
    <script type="module" src="assets/js/skit.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
