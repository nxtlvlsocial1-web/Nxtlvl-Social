"""ChatGPT business skit (the tutorial skit format, nxtlvl-social-video section 8): writes index.html. 1080x1920, 30 fps,
under 60 s. Account: @nxtlvlsocial.ai.

Top half: one big app screen panel (STEP n/4, a progress bar, the step title and an illustrated Business Hub window acted
out step by step). Bottom half: one cozy 3D office (assets/js/skit.js) where Marcus, a real estate agent, talks with Byte,
his AI sidekick. Hook: comment questions. Steps per VentureBeat's walkthrough of Businesses in ChatGPT (beta, launched
10 Nov 2026). Honest beat: claiming doesn't buy a ranking. End card: share prompt, CHATGPT keyword, follow. Screens are
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
END_IN = round(E[-1] + .45, 3)            # the end card
DUR = round(END_IN + 2.6, 2)
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
STEP_LINES = [4, 7, 10, 13]
PANEL_IN = r3(L[4] - .45)
SCR = [(r3(L[s] - .35), r3(L[s + 3] - .35) if k < 3 else r3(L[16] - .35)) for k, s in enumerate(STEP_LINES)]
PAY = (r3(L[16] - .35), END_IN)
TITLES = ["Open Business Hub", "Find your business", "Prove it&rsquo;s yours", "ID check, blue check"]


def screen(k, t0, t1, body):
    show(f"#s{k}", t0, .3, "opacity:0,x:50", "opacity:1,x:0")
    hide(f"#s{k}", t1 - .12, .18, "opacity:0,x:-50")
    return f'<div class="scr" id="s{k}">{body}</div>'


def story():
    H = []
    # the hook: comment questions float in over the office
    cm = [("k.tanaka", "why does ChatGPT keep recommending my competitor??"), ("devon.realty", "how do I get my business on ChatGPT"), ("mira.homes", "is it free??")]
    H.append('<div id="cms">' + "".join(f'<div class="cm" id="cm{j}"><i>{u[0].upper()}</i><div><b>@{u}</b><span>{q}</span></div></div>' for j, (u, q) in enumerate(cm)) + "</div>")
    for j in range(3):
        show(f"#cm{j}", .05 + j * .45, .3, "opacity:0,y:20,scale:.9", "opacity:1,y:0,scale:1", "back.out(1.8)")
    hide("#cms", PANEL_IN - .1, .25, "opacity:0,y:-20")
    # the panel: header (STEP n/4, progress, title) and the app window
    head = "".join(f'<div class="hd" id="hd{k}"><span class="pill">STEP {k + 1}/4</span><span class="prog">' + "".join(f'<i class="{"on" if j <= k else ""}"></i>' for j in range(4)) + f'</span><b>{TITLES[k]}</b></div>' for k in range(4))
    head += '<div class="hd" id="hd4"><span class="pill done">DONE</span><span class="prog">' + "".join('<i class="on"></i>' for _ in range(4)) + '</span><b>Now ask ChatGPT</b></div>'
    S = []
    S.append(screen(0, *SCR[0], f'''<div class="url"><span class="lk"></span><span id="u0">chatgpt.com/business-hub</span></div>
      <div class="hub"><b>Business Hub</b><p>Claim your business on ChatGPT</p><div class="box">Search your business name</div>
      <div class="note" id="n0"><span>No paid plan</span><span>No ads account</span></div></div>'''))
    add(f'tl.fromTo("#u0",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:1.1,ease:"steps(25)",immediateRender:false}},{SCR[0][0] + .5:.3f});')
    show("#n0", L[6] - .05, .3, "opacity:0,scale:.8", "opacity:1,scale:1", "back.out(2)")
    S.append(screen(1, *SCR[1], '''<div class="url"><span class="lk"></span><span>chatgpt.com/business-hub</span></div>
      <div class="hub"><div class="box on"><span id="ty1">Keystone Realty</span><i class="cur"></i></div>
      <div class="drop" id="dd1"><b>Keystone Realty</b><span>Real estate agency · 48 Oak Street</span></div>
      <div class="drop add" id="ad1">+ Not listed? Add it yourself</div>
      <div class="btn" id="go1">Get Started</div><div class="tap" id="tap1"></div></div>'''))
    add(f'tl.fromTo("#ty1",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.8,ease:"steps(15)",immediateRender:false}},{SCR[1][0] + .4:.3f});')
    show("#dd1", SCR[1][0] + 1.25, .22, "opacity:0,y:-10", "opacity:1,y:0")
    show("#go1", SCR[1][0] + 1.6, .22, "opacity:0,y:10", "opacity:1,y:0")
    add(f'tl.fromTo("#tap1",{{opacity:.7,scale:.2}},{{opacity:0,scale:1.6,duration:.45,ease:"power2.out",immediateRender:false}},{E[7] - .5:.3f});')
    add(f'tl.fromTo("#go1",{{scale:1}},{{scale:.94,duration:.1,yoyo:true,repeat:1,immediateRender:false}},{E[7] - .5:.3f});')
    show("#ad1", L[9] + .1, .25, "opacity:0,x:-20", "opacity:1,x:0")
    opts = ["Business phone", "Business email", "Website domain", "Shopify store"]
    S.append(screen(2, *SCR[2], '<div class="hub"><b>Verify your business</b><p>Just one of these</p>' + "".join(
        f'<div class="opt" id="o{j}"><span>{o}</span>{TICK}</div>' for j, o in enumerate(opts)) + '<div class="note" id="n2"><span>Use the email on your website</span></div></div>'))
    w11 = [w for w in WORDS if w["line"] == 11]
    for j, o in enumerate(["phone,", "email,", "website,", "Shopify."]):
        tw = next((w["s"] for w in w11 if w["w"].lower().startswith(o[:5].lower())), L[10] + 1.5 + j * .5)
        add(f'tl.to("#o{j}",{{borderColor:"#a75bfc",background:"#24174a",duration:.12,yoyo:true,repeat:1,repeatDelay:.22,immediateRender:false}},{tw:.3f});')
    add(f'tl.to("#o1",{{borderColor:"#22C55E",duration:.2,immediateRender:false}},{L[12]:.3f});')
    show("#o1 .tk", L[12], .3, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    show("#n2", L[12] + .1, .3, "opacity:0,scale:.8", "opacity:1,scale:1", "back.out(2)")
    S.append(screen(3, *SCR[3], f'''<div class="idc"><div class="idpic"></div><div class="idl"><i></i><i></i><i class="s"></i></div><div class="scan" id="sc3"></div></div>
      <div class="scrawl" id="sw3">not a headshot</div>
      <div class="prof" id="pf3"><div class="ph p4"></div><div><b>Keystone Realty <span id="vb3">{CHECK}</span></b><span>Verified business</span></div></div>'''))
    add(f'tl.fromTo("#sc3",{{y:0}},{{y:200,duration:.55,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{SCR[3][0] + .4:.3f});')
    show("#pf3", E[13] - .9, .3, "opacity:0,y:20", "opacity:1,y:0")
    show("#vb3", E[13] - .45, .35, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    show("#sw3", L[15], .3, "opacity:0,rotation:-10,scale:1.3", "opacity:1,rotation:-6,scale:1", "back.out(2)")
    S.append(screen(4, *PAY, f'''<div class="bar2"><b>ChatGPT</b></div>
      <div class="msg me">Best real estate agent near me?</div>
      <div class="biz top" id="bz0"><div class="ph p4"></div><div><b>Keystone Realty {CHECK}</b><span>open now · showings today</span></div></div>
      <div class="biz"><div class="ph p1"></div><div><b>Prime Nest Realty {CHECK}</b><span>open now · 4.6</span></div></div>
      <div class="stamp" id="st4"><b>DOESN&rsquo;T BUY RANKING</b><span>it gives ChatGPT your real details</span></div>'''))
    show("#bz0", PAY[0] + .4, .35, "opacity:0,x:-30", "opacity:1,x:0")
    show("#st4", L[17] + .2, .35, "opacity:0,scale:1.5,rotation:-10", "opacity:1,scale:1,rotation:-5", "back.out(2)")
    # headers follow the screens
    for k in range(4):
        show(f"#hd{k}", SCR[k][0], .25, "opacity:0", "opacity:1")
        hide(f"#hd{k}", SCR[k][1] - .1, .15)
    show("#hd4", PAY[0], .25, "opacity:0", "opacity:1")
    show("#panel", PANEL_IN, .4, "opacity:0,y:-40,scale:.96", "opacity:1,y:0,scale:1")
    hide("#panel", END_IN - .05, .3, "opacity:0,y:-30")
    # the end card
    show("#endc", END_IN, .45, "opacity:0", "opacity:1")
    for j, c in enumerate(["e0", "e1", "e2", "e3"]):
        show(f"#endc .{c}", END_IN + .1 + j * .25, .35, "opacity:0,y:14")
    return "".join(H) + f'<div id="panel">{head}<div class="win"><div class="chrome"><i></i><i></i><i></i></div><div class="wbody">{"".join(S)}</div></div></div>'


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
            html.append(f'<div class="cap sp-{ln["speaker"]}" id="{pid}">{p}</div>')
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
.cm, .scr, .hd, .note, .drop, .btn, .opt .tk, .prof, #vb3, .stamp, .scrawl, .cap, #panel, #endc, #endc > * { opacity: 0; }
#cms { position: absolute; left: 70px; top: 290px; width: 760px; }
.cm { display: flex; gap: 16px; align-items: center; margin-bottom: 16px; padding: 14px 22px 14px 14px; border-radius: 22px; background: rgba(255,250,240,.96); box-shadow: 0 14px 30px rgba(0,0,0,.35); width: fit-content; max-width: 760px; }
.cm i { flex: none; width: 56px; height: 56px; border-radius: 50%; background: #8B5CF6; color: #fff; font: 800 28px/56px "Manrope"; text-align: center; font-style: normal; }
.cm b { display: block; font: 800 24px/1.2 "Manrope"; color: #6A6878; } .cm span { display: block; font: 700 32px/1.25 "Manrope"; color: #14161C; }
#panel { position: absolute; left: 50px; right: 50px; top: 262px; height: 730px; border-radius: 30px; background: #1A1410; border: 2px solid #3A2C22; box-shadow: 0 30px 70px rgba(0,0,0,.55); overflow: hidden; }
.hd { position: absolute; left: 30px; right: 30px; top: 24px; }
.hd .pill { display: inline-block; padding: 7px 14px; border-radius: 10px; background: #E8735A; color: #fff; font: 800 22px/1 "Manrope"; letter-spacing: 2px; vertical-align: middle; } .hd .pill.done { background: #22C55E; }
.hd .prog { display: inline-flex; gap: 10px; margin-left: 18px; vertical-align: middle; } .hd .prog i { width: 150px; height: 8px; border-radius: 4px; background: #4A3A2E; } .hd .prog i.on { background: #E8735A; }
.hd b { display: block; margin-top: 16px; font: 700 54px/1 "Garamond"; color: #FFF3DC; }
.win { position: absolute; left: 30px; right: 30px; top: 150px; bottom: 30px; border-radius: 18px; background: #F7F4EE; overflow: hidden; }
.chrome { height: 34px; background: #E6DFD3; display: flex; gap: 9px; align-items: center; padding-left: 16px; } .chrome i { width: 13px; height: 13px; border-radius: 50%; background: #C9BFB0; }
.wbody { position: absolute; left: 0; right: 0; top: 34px; bottom: 0; }
.scr { position: absolute; inset: 0; padding: 26px 30px; color: #14161C; }
.url { display: flex; align-items: center; gap: 12px; padding: 16px 20px; border-radius: 14px; background: #fff; border: 2px solid #E2DACD; font: 700 32px/1 "Mono"; }
.url .lk { width: 18px; height: 22px; border-radius: 4px; border: 4px solid #22C55E; }
.hub { margin-top: 24px; } .hub > b { display: block; font: 800 42px/1.1 "Manrope"; } .hub > p { margin-top: 8px; font: 600 28px/1.3 "Manrope"; color: #6A6878; }
.box { margin-top: 20px; padding: 20px 22px; border-radius: 14px; border: 2px solid #D9D1C4; background: #fff; font: 600 32px/1 "Manrope"; color: #9A93A6; display: flex; align-items: center; }
.box.on { color: #14161C; border-color: #8B5CF6; } .cur { display: inline-block; width: 3px; height: 34px; background: #8B5CF6; margin-left: 6px; }
.drop { margin-top: 10px; padding: 16px 22px; border-radius: 14px; background: #fff; border: 2px solid #E2DACD; } .drop b { display: block; font: 800 32px/1.2 "Manrope"; } .drop span { font: 600 24px/1.4 "Manrope"; color: #6A6878; }
.drop.add { font: 800 28px/1 "Manrope"; color: #8B5CF6; border-style: dashed; border-color: #8B5CF6; }
.btn { position: relative; margin-top: 22px; padding: 22px; border-radius: 999px; background: #14161C; color: #fff; text-align: center; font: 800 34px/1 "Manrope"; }
.tap { position: absolute; left: 50%; top: 395px; width: 130px; height: 130px; margin-left: -65px; border-radius: 50%; background: rgba(139,92,246,.55); opacity: 0; }
.opt { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding: 18px 22px; border-radius: 16px; background: #fff; border: 2px solid #E2DACD; font: 700 34px/1 "Manrope"; }
.tk { width: 42px; height: 42px; } .vb { width: 34px; height: 34px; flex: none; }
.note { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 18px; } .note span { padding: 10px 18px; border-radius: 999px; background: #E7F7EC; color: #15803D; font: 800 26px/1 "Manrope"; }
.idc { position: relative; margin: 20px auto 0; width: 600px; height: 250px; border-radius: 24px; background: #fff; border: 2px solid #E2DACD; overflow: hidden; }
.idpic { position: absolute; left: 30px; top: 36px; width: 140px; height: 175px; border-radius: 14px; background: linear-gradient(180deg, #D9D1C4, #BFB4A4); }
.idl { position: absolute; left: 200px; top: 56px; right: 30px; } .idl i { display: block; height: 20px; margin-bottom: 24px; border-radius: 10px; background: #E6DFD3; } .idl i.s { width: 60%; }
.scan { position: absolute; left: 0; right: 0; top: 24px; height: 6px; background: #8B5CF6; box-shadow: 0 0 24px #8B5CF6; }
.scrawl { position: absolute; left: 70px; top: 270px; font: italic 600 40px/1 "Garamond"; color: #E8735A; transform: rotate(-6deg); }
.prof { display: flex; align-items: center; gap: 18px; margin-top: 70px; padding: 20px; border-radius: 20px; background: #fff; border: 2px solid #E2DACD; }
.prof b { display: flex; align-items: center; gap: 12px; font: 800 40px/1.1 "Manrope"; } .prof span { font: 600 26px/1.4 "Manrope"; color: #6A6878; }
.ph { flex: none; width: 70px; height: 70px; border-radius: 16px; } .p1 { background: linear-gradient(135deg, #7DBA6A, #1F7A4D); } .p4 { background: linear-gradient(135deg, #F2C94C, #1C2A4A); }
.bar2 { font: 800 30px/1 "Manrope"; color: #6A6878; padding-bottom: 16px; border-bottom: 1px solid #E2DACD; margin-bottom: 18px; }
.msg.me { margin-left: 190px; padding: 16px 22px; border-radius: 22px; background: #ECE6DB; font: 700 30px/1.3 "Manrope"; margin-bottom: 16px; }
.biz { display: flex; gap: 16px; align-items: center; padding: 14px 16px; border-radius: 18px; background: #fff; border: 2px solid #E2DACD; margin-bottom: 12px; }
.biz b { display: flex; align-items: center; gap: 10px; font: 800 32px/1.1 "Manrope"; } .biz span { font: 600 24px/1.4 "Manrope"; color: #6A6878; }
.biz.top { border-color: #2F7BF6; box-shadow: 0 0 0 4px rgba(47,123,246,.15); } .biz.top { opacity: 0; }
.stamp { position: absolute; left: 60px; right: 60px; bottom: 30px; padding: 16px; border: 5px solid #E8735A; border-radius: 16px; text-align: center; color: #E8735A; background: rgba(255,250,240,.92); transform: rotate(-5deg); }
.stamp b { display: block; font: 900 40px/1 "Manrope"; letter-spacing: 2px; } .stamp span { display: block; margin-top: 8px; font: italic 600 30px/1 "Garamond"; color: #6A4A3A; }
.cap { position: absolute; left: 50px; right: 50px; top: 1040px; text-align: center; font: 600 54px/1.15 "Garamond"; color: #FFF1D6; text-shadow: 0 3px 14px rgba(0,0,0,.85), 0 1px 3px rgba(0,0,0,.9); }
.cap.sp-byte { color: #C9F7E4; }
#endc { position: absolute; inset: 0; background: radial-gradient(700px 700px at 50% 32%, #4A3426, #1E1510 70%); text-align: center; color: #FFF1D6; }
#endc .e0 { position: absolute; left: 50%; top: 380px; width: 230px; height: 230px; margin-left: -115px; border-radius: 50%; background: rgba(255,214,140,.12); display: flex; align-items: center; justify-content: center; }
#endc .e0 svg { width: 120px; height: 120px; }
#endc .e1 { position: absolute; left: 80px; right: 80px; top: 680px; font: 700 64px/1.15 "Garamond"; }
#endc .e2 { position: absolute; left: 60px; right: 60px; top: 900px; font: 800 40px/1.4 "Manrope"; } #endc .e2 b { padding: 4px 14px; border-radius: 10px; background: #E8735A; color: #fff; }
#endc .e3 { position: absolute; left: 60px; right: 60px; top: 990px; font: 700 32px/1.4 "Manrope"; color: #D9C9B0; }
"""


def main():
    ui = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, "who": WHO, "end": DUR, "cuts": [], "stepLines": STEP_LINES, "panelIn": PANEL_IN, "endIn": END_IN, "scr": SCR, "pay": PAY}
    house = '<svg viewBox="0 0 64 64"><path d="M8 30 L32 10 L56 30" stroke="#F2C94C" stroke-width="5" fill="none" stroke-linejoin="round"/><rect x="16" y="28" width="32" height="26" rx="3" fill="#F2C94C"/><circle cx="46" cy="44" r="12" fill="#2F7BF6"/><path d="M40 44.5l4 4 8-8" stroke="#fff" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    endc = (f'<div id="endc"><div class="e0">{house}</div><div class="e1">Send this to an agent who&rsquo;s invisible on ChatGPT</div>'
            '<div class="e2">Comment <b>CHATGPT</b> for the full checklist</div><div class="e3">Follow @nxtlvlsocial.ai for the next one</div></div>')
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
