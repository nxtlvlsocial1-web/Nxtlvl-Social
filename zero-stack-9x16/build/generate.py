"""Zero Stack reel ("What if every app you pay for vanished overnight?"): writes index.html. 1080x1920, 30 fps.
Account: @nxtlvlsocial.ai. A cinematic what-if told in dialogue: Maya, a solo founder, wakes up to every paid app
cancelled and locked for 30 days, a month before her launch. Noah, the developer next door, swaps each one for an
open-source tool, day by day: Adobe Creative Cloud, Canva, CapCut, Mailchimp, Hootsuite, Linktree, Notion and, on the
stormy night before launch with the internet down, ChatGPT (an AI running on her own laptop). Day 30: orders roll in and
the software bill is $0. Keyword CTA: comment STACK (we DM the free "Zero Stack" PDF).

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D (assets/js/stack.js) plays the shot list. This file writes the HTML layer: the title, the cancellation
notifications, the day and bill counters, a card for every swap, chapter cards, launch-day orders, the $0 reveal,
speaker-tagged serif captions and the end card. Prices are 2026 US list prices, monthly billing (see the description).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
DUR = round(LINES[-1]["end"] + 2.0, 2)

L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
WHO = [ln["speaker"] for ln in LINES]
r3 = lambda x: round(x, 3)  # noqa: E731

# the eight swaps: paid app -> open-source replacement, monthly price, tile colours (paid, open) and text colours
SWAPS = [
    ("Adobe\nCreative Cloud", "Adobe Creative Cloud", 69.99, "GIMP\nInkscape\nKdenlive", "GIMP · Inkscape · Kdenlive", "#E1251B", "#3D8B5A", "#FFFFFF", "#FFFFFF", 1),
    ("Canva Pro", "Canva Pro", 18.00, "Penpot", "Penpot", "#00B8C4", "#18181C", "#FFFFFF", "#31EFB8", 4),
    ("CapCut Pro", "CapCut Pro", 19.99, "Shotcut", "Shotcut", "#111111", "#2C7BD8", "#FFFFFF", "#FFFFFF", 8),
    ("Mailchimp", "Mailchimp", 108.88, "Listmonk", "Listmonk", "#F2C11B", "#0055D4", "#1E1B18", "#FFFFFF", 12),
    ("Hootsuite", "Hootsuite", 99.00, "Postiz", "Postiz", "#143059", "#612BD3", "#FFFFFF", "#FFFFFF", 16),
    ("Linktree Pro", "Linktree Pro", 15.00, "LinkStack", "LinkStack", "#43E55E", "#2B2B6E", "#1E1B18", "#FFFFFF", 20),
    ("Notion", "Notion", 24.00, "AppFlowy", "AppFlowy", "#F4F4F2", "#6E3FF3", "#1E1B18", "#FFFFFF", 25),
    ("ChatGPT Plus", "ChatGPT Plus", 20.00, "Ollama", "Ollama · local AI", "#10A37F", "#F4F4F2", "#FFFFFF", "#1E1B18", 29),
]
BILL0 = round(sum(s[2] for s in SWAPS), 2)          # 374.86
# the 60-second cut: lines 0 Adobe cancelled, 1 "What?", 2 locked, 3 "My launch", 4 Noah, 5 the night, 6 "run your own AI",
# 7 "still writing", 8 "Zero", 9 the CTA. The swaps between Noah's line and the night play as a fast montage.
CU0 = r3(E[4] + .3)
SW = [r3(CU0 + .85 + 1.6 * k) for k in range(7)] + [r3(L[6] + 1.1)]
CU = [CU0, r3(SW[2] + .8), r3(SW[6] + 1.2), r3(E[7] + .35)]
T = {
    "cuts": CU, "sw": SW, "who": WHO,
    "knock": r3(E[3] + .15), "cut": r3(L[5] + 3.05), "flash": [r3(CU[2] + .5), r3(L[5] + 2.9), r3(L[6] + 1.5)],
    "zero": r3(L[8] + .1), "endc": r3(L[9] - .3), "end": DUR,
    "tileNames": [[s[0], s[3]] for s in SWAPS], "tileCol": [[s[5], s[6]] for s in SWAPS], "tileFg": [[s[7], s[8]] for s in SWAPS],
    "lines": [{"s": ln["start"], "e": ln["end"]} for ln in LINES],
}
A = []


def add(js):
    A.append("      " + js)


def show(sel, t, d=.35, frm="opacity:0,y:14", to="opacity:1,y:0", ease="power2.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def hide(sel, t, d=.3, props="opacity:0"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


def setText(sel, txt, t):
    add(f'tl.set("{sel}",{{textContent:{json.dumps(txt)}}},{t:.3f});')


def money(x):
    return f"${x:,.2f}"


NAMES = {"maya": "MAYA", "noah": "NOAH", "system": "SYSTEM"}


def story():
    html = []
    # the title: on screen from the first frame, then it lifts
    show(".t1", 0.0, .01, "opacity:1", "opacity:1"); show(".t2", 0.0, .01, "opacity:1", "opacity:1"); show(".t3", 0.0, .01, "opacity:1", "opacity:1")
    add('tl.fromTo("#title .t2",{scale:1.04},{scale:1,duration:1.2,ease:"power2.out",immediateRender:false},0);')
    hide("#title", 2.45, .4, "opacity:0,y:-30")
    # the notifications: Adobe on line 0, the other seven pile in during "What? I didn't cancel anything."
    times = [L[0] + .05] + [L[1] + .1 + .36 * k for k in range(7)]
    for k, t0 in enumerate(times):
        nid = f"#n{k}"
        add(f'tl.fromTo("{nid}",{{opacity:0,y:-40,scale:.96}},{{opacity:1,y:0,scale:1,duration:.24,ease:"back.out(1.6)",immediateRender:false}},{t0:.3f});')
        for j in range(k + 1, len(times)):
            add(f'tl.to("{nid}",{{y:{(j - k) * 108},duration:.2,ease:"power2.out"}},{times[j]:.3f});')
    for k in range(8):
        hide(f"#n{k}", L[2] + .6 + (7 - k) * .03, .35, f"opacity:0,y:{(7 - k) * 108 - 60}")
    # the HUD: day and bill
    show("#hud", L[3] - .2, .45, "opacity:0,y:-14")
    days = [(L[3] - .2, 1)] + [(SW[k] - .6, SWAPS[k][9]) for k in range(1, 7)] + [(CU[2], 29), (CU[3], 30)]
    for t0, d in days:
        setText("#hud .d-n", str(d), t0)
        add(f'tl.fromTo("#hud .d-n",{{scale:1.35,color:"#F2C94C"}},{{scale:1,color:"#FFFDF6",duration:.45,ease:"power2.out",immediateRender:false}},{t0:.3f});')
    bill = BILL0
    for k, s in enumerate(SWAPS):
        new = round(bill - s[2], 2); t0 = SW[k] + .4
        for j in range(1, 9):
            setText("#hud .b-n", money(bill + (new - bill) * j / 8), t0 + j * .05)
        add(f'tl.fromTo("#hud .b-n",{{scale:1.2}},{{scale:1,duration:.4,ease:"power2.out",immediateRender:false}},{t0 + .4:.3f});')
        bill = new
    add(f'tl.to("#hud .b-n",{{color:"#5BE38A",duration:.3}},{SW[7] + .9:.3f});')
    hide("#hud", T["endc"] - .1, .4, "opacity:0,y:-14")
    # a card for every swap: the paid app and its price, struck out, and the open-source tool, free
    for k, s in enumerate(SWAPS):
        b = SW[k]
        z = b + .88 if k < 6 else (CU[2] - .15 if k == 6 else b + 2.2)
        cid = f"#sw{k}"
        show(cid, b - .55 if k else b - .6, .2, "opacity:0,y:-16,scale:.97", "opacity:1,y:0,scale:1")
        add(f'tl.fromTo("{cid} .strike",{{scaleX:0}},{{scaleX:1,duration:.22,ease:"power2.out",immediateRender:false}},{b:.3f});')
        add(f'tl.to("{cid} .old",{{opacity:.5,duration:.2}},{b + .1:.3f});')
        show(f"{cid} .new", b + .15, .25, "opacity:0,y:12")
        hide(cid, z, .14, "opacity:0,y:-12")
        html.append(f'<div class="swap" id="sw{k}"><div class="day">DAY {s[9]}</div>'
                    f'<div class="old"><span class="nm">{s[1]}</span><span class="pr">{money(s[2])}/mo</span><i class="strike"></i></div>'
                    f'<div class="new"><span class="ar">&#8594;</span><span class="nm">{s[4]}</span><span class="pr">FREE · OPEN SOURCE</span></div></div>')
    # the night
    show("#ch1", CU[2] + .1, .4, "opacity:0,scale:1.08", "opacity:1,scale:1"); hide("#ch1", CU[2] + 1.5, .3, "opacity:0,y:-16")
    show("#offline", T["cut"] + .25, .3, "opacity:0,scale:.9", "opacity:1,scale:1"); hide("#offline", SW[7] - .75, .25)
    # launch day: the orders roll in
    for k in range(3):
        t0 = CU[3] + .15 + k * .22
        oid = f"#o{k}"
        add(f'tl.fromTo("{oid}",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.22,ease:"back.out(1.6)",immediateRender:false}},{t0:.3f});')
        for j in range(k + 1, 3):
            add(f'tl.to("{oid}",{{y:{(j - k) * 108},duration:.18,ease:"power2.out"}},{CU[3] + .15 + j * .22:.3f});')
    for k in range(3):
        hide(f"#o{k}", T["zero"] - .2 + (2 - k) * .03, .25, f"opacity:0,y:{(2 - k) * 108 - 60}")
    # the $0 reveal
    show("#zero", T["zero"], .4, "opacity:0,scale:1.12", "opacity:1,scale:1")
    hide("#zero", E[8] + .25, .3)
    # the end card
    show("#endc", T["endc"], .5, "opacity:0", "opacity:1")
    show("#endc .e0", T["endc"] + .05, .4, "opacity:0,y:14")
    show("#endc .e1", T["endc"] + .3, .5, "opacity:0,scale:1.15", "opacity:1,scale:1")
    show("#endc .e2", T["endc"] + .7, .4, "opacity:0,y:14")
    show("#endc .e3", T["endc"] + 1.0, .4, "opacity:0,y:14")
    return "".join(html)


def captions():
    html = []
    for k, ln in enumerate(LINES):
        if k == len(LINES) - 1:              # the CTA is on the end card
            continue
        text = ln["text"]
        parts = [text] if len(text) < 44 else [p for p in re.split(r"(?<=[.?!,])\s+(?=[A-Z0-9])", text) if p]
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        wi = 0
        nxt = LINES[k + 1]["start"] if k + 1 < len(LINES) else DUR
        for j, p in enumerate(parts):
            n = len(p.split())
            a0 = ws[min(wi, len(ws) - 1)]["s"] - .1
            z = ws[wi + n]["s"] - .32 if wi + n < len(ws) else min(ln["end"] + .3, nxt - .2)
            wi += n
            pid = f"c{k}_{j}"
            who = ln["speaker"]
            html.append(f'<div class="cap sp-{who}" id="{pid}"><span class="who">{NAMES[who]}</span><span class="br"></span><span class="tx">{p}</span></div>')
            add(f'tl.fromTo("#{pid}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.22,ease:"power2.out",immediateRender:false}},{a0:.3f});')
            add(f'tl.to("#{pid}",{{opacity:0,duration:.18,ease:"power1.in"}},{z:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Garamond"; font-weight: 400 800; src: url("assets/fonts/EBGaramond.ttf"); }
@font-face { font-family: "Garamond"; font-style: italic; font-weight: 400 800; src: url("assets/fonts/EBGaramond-Italic.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0B0A12; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0B0A12; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.shadow { text-shadow: 0 3px 18px rgba(0,0,0,.55), 0 1px 3px rgba(0,0,0,.6); }
#hud, .cap, .stamp, .chap, .note, .swap, .swap .new, #offline, .order, #zero, #endc, #endc span { opacity: 0; }
#title { position: absolute; left: 70px; right: 70px; top: 470px; text-align: center; color: #FFFDF6; }
#title .t0 { display: inline-block; padding: 10px 26px; border-radius: 40px; background: #F2C94C; color: #1E1B18; font: 800 34px/1 "Manrope"; letter-spacing: 6px; margin-bottom: 34px; }
#title .t1, #title .t3 { display: block; font: 500 80px/1.1 "Garamond"; letter-spacing: -.5px; }
#title .t2 { display: block; font: 700 112px/1.08 "Garamond"; color: #F2C94C; }
.stamp { position: absolute; left: 0; right: 0; top: 330px; text-align: center; color: #FFFDF6; font: italic 500 64px/1.1 "Garamond"; }
.stamp b { display: block; margin-top: 10px; font: 800 30px/1 "Manrope"; letter-spacing: 6px; font-style: normal; color: #F2C94C; }
.note { position: absolute; left: 70px; right: 70px; top: 300px; height: 96px; border-radius: 26px; background: rgba(250,250,252,.94);
  box-shadow: 0 10px 30px rgba(0,0,0,.35); display: flex; align-items: center; padding: 0 24px; gap: 20px; }
.note .ic { width: 58px; height: 58px; border-radius: 14px; flex: none; display: flex; align-items: center; justify-content: center; font: 800 30px/1 "Manrope"; color: #fff; }
.note .tx { flex: 1; min-width: 0; }
.note .tt { display: block; font: 800 28px/1.15 "Manrope"; color: #14161C; }
.note .bd { display: block; font: 600 26px/1.2 "Manrope"; color: #C0392B; margin-top: 4px; }
.note .tm { font: 600 22px/1 "Manrope"; color: #8A8F9C; align-self: flex-start; margin-top: 18px; }
#hud { position: absolute; left: 64px; right: 64px; top: 268px; display: flex; justify-content: space-between; color: #FFFDF6; }
#hud .lab { display: block; font: 800 28px/1 "Manrope"; letter-spacing: 4px; color: rgba(255,253,246,.85); }
#hud .row { display: block; margin-top: 8px; font: 700 66px/1 "Garamond"; }
#hud .row small { font: 600 30px/1 "Garamond"; color: rgba(255,253,246,.75); }
#hud .bill { text-align: right; }
#hud .d-n, #hud .b-n { display: inline-block; transform-origin: 50% 70%; }
.swap { position: absolute; left: 80px; right: 80px; top: 400px; padding: 18px 26px 20px; border-radius: 28px; background: rgba(12,14,22,.94);
  box-shadow: 0 14px 40px rgba(0,0,0,.45); color: #FFFDF6; text-align: center; }
.swap .day { font: 800 28px/1 "Manrope"; letter-spacing: 6px; color: #F2C94C; }
.swap .old { position: relative; display: inline-block; margin-top: 12px; padding: 0 8px; white-space: nowrap; }
.swap .old .nm { font: 800 38px/1.1 "Manrope"; }
.swap .old .pr { margin-left: 14px; font: 700 30px/1.1 "Manrope"; color: #FF8A80; }
.swap .strike { position: absolute; left: -6px; right: -6px; top: 50%; height: 6px; margin-top: -3px; background: #FF5A4E; border-radius: 4px; transform-origin: 0 50%; transform: scaleX(0); }
.swap .new { margin-top: 8px; white-space: nowrap; }
.swap .new .ar { font: 800 34px/1 "Manrope"; color: rgba(255,253,246,.7); margin-right: 12px; }
.swap .new .nm { font: 800 44px/1.1 "Manrope"; color: #5BE38A; }
.swap .new .pr { display: block; margin-top: 6px; font: 800 28px/1 "Manrope"; letter-spacing: 5px; color: #FFFDF6; }
.chap { position: absolute; left: 0; right: 0; top: 560px; text-align: center; color: #FFFDF6; }
.chap .cd { display: block; font: 600 132px/1 "Garamond"; letter-spacing: -1px; }
.chap .cp { display: block; margin-top: 16px; font: 800 36px/1 "Manrope"; letter-spacing: 10px; color: #F2C94C; }
#offline { position: absolute; left: 50%; top: 430px; margin-left: -190px; width: 380px; padding: 18px 0; border-radius: 40px; background: #E5484D; color: #fff; text-align: center; font: 800 32px/1 "Manrope"; letter-spacing: 5px; }
.order { position: absolute; left: 110px; right: 110px; top: 430px; height: 92px; border-radius: 24px; background: rgba(250,250,252,.95); box-shadow: 0 10px 30px rgba(0,0,0,.3);
  display: flex; align-items: center; padding: 0 22px; gap: 18px; }
.order .ic { width: 54px; height: 54px; border-radius: 14px; background: #3FA372; color: #fff; display: flex; align-items: center; justify-content: center; font: 800 30px/1 "Manrope"; flex: none; }
.order .tt { flex: 1; font: 800 30px/1 "Manrope"; color: #14161C; }
.order .pr { font: 800 30px/1 "Manrope"; color: #3FA372; }
#zero { position: absolute; left: 90px; right: 90px; top: 390px; text-align: center; color: #FFFDF6; }
#zero .z0 { display: block; font: 800 30px/1 "Manrope"; letter-spacing: 6px; }
#zero .z1 { display: block; margin-top: 8px; font: 700 190px/1 "Garamond"; color: #5BE38A; }
#zero .z2 { display: block; margin-top: 6px; font: italic 500 52px/1.1 "Garamond"; }
#zero .z2 s { color: #FF8A80; }
#zero .z3 { display: block; margin-top: 12px; font: 700 28px/1.2 "Manrope"; letter-spacing: 2px; color: rgba(255,253,246,.8); }
.cap { position: absolute; left: 60px; right: 60px; top: 1300px; text-align: center; }
.cap .who { display: inline-block; margin-bottom: 10px; padding: 7px 16px; border-radius: 20px; font: 800 26px/1 "Manrope"; letter-spacing: 4px; color: #0B0D12; background: #F2C94C; }
.cap .tx { display: inline; padding: 8px 18px; border-radius: 16px; line-height: 1.55; font: 800 48px/1.5 "Manrope"; color: #FFFFFF;
  background: rgba(8,10,16,.82); -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.cap .br { display: block; height: 0; }
.cap.sp-noah .who { background: #5BE38A; } .cap.sp-system .who { background: #FF8A80; } .cap.sp-system .tx { color: #FFD3CF; }
#endc { position: absolute; left: 70px; right: 70px; top: 330px; text-align: center; color: #FFFDF6; }
#endc span { display: block; }
#endc .e0 { font: italic 500 70px/1.1 "Garamond"; }
#endc .e1 { margin-top: 6px; font: 800 170px/1 "Manrope"; letter-spacing: 6px; color: #F2C94C; }
#endc .e2 { margin-top: 14px; font: italic 500 54px/1.15 "Garamond"; }
#endc .e3 { margin-top: 40px; font: 800 30px/1.4 "Manrope"; letter-spacing: 5px; }
#endc .e3 b { display: block; font: 800 42px/1.3 "Manrope"; letter-spacing: 2px; }
"""

NOTES = [("Adobe Creative Cloud", "#E1251B", "A")] + [(s[1], s[5], s[1][0]) for s in SWAPS[1:]]


def main():
    sw_html = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, **T}
    notes = "".join(f'<div class="note" id="n{k}"><span class="ic" style="background:{c};{"color:#1E1B18;" if c in ("#F2C11B", "#43E55E", "#F4F4F2") else ""}">{i}</span>'
                    f'<span class="tx"><span class="tt">{n}</span><span class="bd">Your subscription has been cancelled.</span></span><span class="tm">now</span></div>'
                    for k, (n, c, i) in enumerate(NOTES))
    orders = "".join(f'<div class="order" id="o{k}"><span class="ic">$</span><span class="tt">New order</span><span class="pr">{p}</span></div>'
                     for k, p in enumerate(["$39.00", "$78.00", "$117.00"]))
    ui = ('<div id="title" class="shadow"><span class="t0">WHAT IF</span><span class="t1">every app you pay for</span>'
          '<span class="t2">vanished</span><span class="t3">overnight?</span></div>'
          + notes +
          '<div id="hud" class="shadow"><div><span class="lab">DAY</span><span class="row"><span class="d-n">1</span> <small>/ 30</small></span></div>'
          f'<div class="bill"><span class="lab">SOFTWARE BILL</span><span class="row"><span class="b-n">{money(BILL0)}</span><small>/mo</small></span></div></div>'
          + sw_html +
          '<div id="ch1" class="chap shadow"><span class="cd">Day 29</span><span class="cp">11:48 PM · A STORM</span></div>'
          '<div id="offline">NO INTERNET</div>'
          + orders +
          f'<div id="zero" class="shadow"><span class="z0">SOFTWARE BILL</span><span class="z1">$0</span><span class="z2">was <s>{money(BILL0)}/mo</s></span>'
          '<span class="z3">$4,498 A YEAR, BACK IN HER POCKET</span></div>'
          '<div id="endc" class="shadow"><span class="e0">Want the whole stack?</span><span class="e1">STACK</span>'
          '<span class="e2">Comment it and I\'ll DM you every tool</span>'
          '<span class="e3">FOLLOW<b>@nxtlvlsocial.ai</b></span></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Zero Stack 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-hold data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>{ui}</div>
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
    <script type="module" src="assets/js/stack.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}, bill {BILL0}")


if __name__ == "__main__":
    main()
