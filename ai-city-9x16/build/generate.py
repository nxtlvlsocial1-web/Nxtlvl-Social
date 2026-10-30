"""AI City reel ("What if one AI ran a city for 24 hours?"): writes index.html. 1080x1920, 30 fps, about 68 s.
Account: @ai.nxtlvl.

python3 build/generate.py      (from the project root, after build/voice.py and build/timing.py)

The city is a Three.js diorama (assets/js/city.js) drawn on hf-seek; this file writes the HTML layer on top in the
cream ai.nxtlvl house style: a top bar with the city clock, word-by-word caption cards, one story card at a time in
the card band (y 430-820) and the CTA card. Cue times come from build/words.json and are handed to city.js as
window.CT.

The scenario is a hypothetical (the top bar says WHAT IF · SIMULATION) and its numbers are illustrative. The one
real-world claim is the takeaway card: Google's Project Green Light uses AI to recommend traffic-light timing to
cities, including Seattle and Rio de Janeiro.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
DUR = round(LINES[-1]["end"] + 1.6, 2)


def word(line, text, nth=1):
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1]["s"]


L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
T = {
    "entire": word(1, "entire"), "mayor": word(1, "mayor"), "cops": word(1, "cops"), "clock": word(1, "clock"),
    "syncs": word(2, "syncs"), "buses": word(2, "buses"), "waiting": word(2, "waiting"), "rush": word(2, "rush"), "disappears": word(2, "disappears"),
    "drones": word(3, "drones"), "minutes": word(3, "minutes"), "grid": word(3, "grid"), "energy": word(3, "energy"), "hospitals": word(3, "hospitals"),
    "ambulance": word(3, "ambulance"),
    "sensor": word(4, "sensor"), "flooded": word(4, "flooded"), "reroutes": word(4, "reroutes"), "ten": word(4, "ten"), "bridge": word(4, "bridge"),
    "locks": word(5, "locks"), "deliveries": word(5, "deliveries"), "grid2": word(5, "grid"), "cuts": word(5, "cuts"), "tiny": word(5, "tiny"),
    "freezes": word(5, "freezes"),
    "fixes": word(6, "fixes"), "seconds": word(6, "seconds"), "nobody": word(6, "nobody"), "why": word(6, "why"),
    "science": word(7, "science"), "google": word(7, "google"), "seattle": word(7, "seattle"), "real": word(7, "real"), "charge": word(7, "charge"),
    "wrong": word(7, "wrong"),
    "comment": word(8, "comment"), "citykw": word(8, "city"), "end": DUR,
}
HOURS = [[5.0, 5.8], [6.0, 7.4], [12.0, 12.9], [16.0, 16.3], [16.3, 17.0], [24.0, 24.15], [30.0, 30.5], [30.5, 30.7]]
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
CARDS = (
    '<div class="stamp st-mayor">NO MAYOR</div><div class="stamp st-cops">NO TRAFFIC COPS</div>'
    '<div class="card bigclock"><span class="mono lab">THE AI GETS</span><b><i class="n24">0</i> HOURS</b><span class="ser">to run the whole city</span></div>'
    '<div class="card c-sync"><span class="dot g"></span><div><span class="mono lab">ALL TRAFFIC LIGHTS</span><b>SYNCED <i class="nsync">0</i>/22</b></div></div>'
    '<div class="card c-bus"><span class="dot c"></span><div><span class="mono lab">BUSES</span><b>stop only where people wait</b></div></div>'
    '<div class="card c-rush"><span class="mono lab">8 AM</span><b class="strike">RUSH HOUR</b></div>'
    '<div class="card c-drone"><span class="dot y"></span><div><span class="mono lab">DRONE DELIVERY</span><b><i class="ndel">0</i> MIN</b></div></div>'
    '<div class="card c-grid"><span class="mono lab">POWER GRID</span><b>shifting energy</b><em class="bars">'
    + "".join(f'<i class="gb gb{k}"></i>' for k in range(6)) + '</em></div>'
    '<div class="card c-hosp"><span class="dot g"></span><div><span class="mono lab">HOSPITAL</span><b>READY</b><span class="sub">ambulance still 3 min out</span></div></div>'
    '<div class="card alert c-sensor"><span class="dot r"></span><div><span class="mono lab">SENSOR 14</span><b>FLOOD DETECTED?</b></div></div>'
    '<div class="card c-reroute"><span class="mono lab">REROUTING</span><b><i class="ncar">0</i> CARS</b><span class="arrow">&rarr; 1 BRIDGE</span></div>'
    '<div class="card alert c-lock"><span class="dot r"></span><div><span class="mono lab">BRIDGE</span><b>GRIDLOCK</b></div></div>'
    '<div class="card alert c-stall"><span class="dot r"></span><div><span class="mono lab">DELIVERIES</span><b>STALLED</b></div></div>'
    '<div class="card alert c-cut"><span class="mono lab">POWER CUT</span><b><i class="ndis">0</i> DISTRICTS DARK</b></div>'
    '<div class="stamp st-frozen">CITY FROZEN</div>'
    '<div class="card c-fix"><span class="dot g"></span><div><span class="mono lab">FIXED IN</span><b><i class="nfix">0.0</i> SECONDS</b></div></div>'
    '<div class="card c-why"><span class="mono lab">ROOT CAUSE</span><b class="ser big">Why did it happen?</b><span class="sub mono">NO ONE CAN EXPLAIN IT</span></div>'
    '<div class="card c-real"><span class="mono lab real">REAL WORLD, TODAY</span><b>Google&rsquo;s Project Green Light</b>'
    '<span class="sub">uses AI to suggest traffic-light timing to cities like Seattle and Rio</span></div>'
    '<div class="card c-q"><b class="ser big">Who&rsquo;s in charge</b><b class="ser big coral">when it gets it wrong?</b></div>'
)


def story():
    # hook: the stamps, then the 24-hour card
    pop(".st-mayor", T["mayor"] - .05, "scale:2.2,opacity:0,rotation:-16", .25, "back.out(2)", "scale:1,opacity:1,rotation:-6")
    pop(".st-cops", T["cops"] - .05, "scale:2.2,opacity:0,rotation:14", .25, "back.out(2)", "scale:1,opacity:1,rotation:5")
    out(".st-mayor, .st-cops", T["clock"] - .45)
    pop(".bigclock", T["clock"] - .35, "scale:.7,opacity:0,y:30", .35, "back.out(1.8)")
    count(".n24", T["clock"] - .3, 0, 24, .7)
    out(".bigclock", L[1] - .15)
    # 6 AM
    pop(".c-sync", T["syncs"] - .1, "x:-120,opacity:0", .3, "back.out(1.8)")
    count(".nsync", T["syncs"], 0, 22, .9)
    out(".c-sync", T["buses"] - .25)
    pop(".c-bus", T["buses"] - .1, "x:120,opacity:0", .3, "back.out(1.8)")
    out(".c-bus", T["rush"] - .25)
    pop(".c-rush", T["rush"] - .1, "scale:.7,opacity:0", .3, "back.out(2)")
    add(f'tl.fromTo(".strike",{{"--s":0}},{{"--s":1,duration:.45,ease:"power2.inOut",immediateRender:false}},{T["disappears"]:.3f});')
    out(".c-rush", E[1] + .15)
    # noon
    pop(".c-drone", T["drones"] - .1, "x:-120,opacity:0", .3, "back.out(1.8)")
    count(".ndel", T["drones"] + .1, 30, 4, T["minutes"] + .3 - T["drones"])
    out(".c-drone", T["grid"] - .25)
    pop(".c-grid", T["grid"] - .1, "x:120,opacity:0", .3, "back.out(1.8)")
    for k in range(6):
        add(f'tl.fromTo(".gb{k}",{{scaleY:.3}},{{scaleY:{[.9, .5, .7, .35, 1, .6][k]},duration:.35,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{T["grid"] + k * .06:.3f});')
    out(".c-grid", T["hospitals"] - .25)
    pop(".c-hosp", T["hospitals"] - .1, "scale:.7,opacity:0", .3, "back.out(2)")
    out(".c-hosp", E[2] + .2)
    # 4 PM
    pop(".c-sensor", T["sensor"] - .05, "x:-120,opacity:0", .3, "back.out(1.8)")
    add(f'tl.fromTo(".c-sensor",{{x:0}},{{x:8,duration:.05,yoyo:true,repeat:7,ease:"none",immediateRender:false}},{T["flooded"] + .1:.3f});')
    out(".c-sensor", T["reroutes"] - .25)
    pop(".c-reroute", T["reroutes"] - .1, "scale:.7,opacity:0", .3, "back.out(2)")
    count(".ncar", T["ten"], 0, 10000, T["bridge"] - T["ten"])
    pop(".arrow", T["bridge"] - .05, "x:-60,opacity:0", .25, "back.out(2)")
    out(".c-reroute", E[3] + .1)
    # chaos
    pop(".c-lock", T["locks"] - .1, "scale:1.6,opacity:0", .22, "back.out(2)")
    out(".c-lock", T["deliveries"] - .2, .15)
    pop(".c-stall", T["deliveries"] - .1, "scale:1.6,opacity:0", .22, "back.out(2)")
    out(".c-stall", T["grid2"] - .2, .15)
    pop(".c-cut", T["grid2"] - .1, "scale:1.6,opacity:0", .22, "back.out(2)")
    count(".ndis", T["cuts"], 0, 9, .9)
    out(".c-cut", T["freezes"] - .15, .12)
    pop(".st-frozen", T["freezes"] - .03, "scale:2.4,opacity:0,rotation:-18", .22, "back.out(2)", "scale:1,opacity:1,rotation:-7")
    out(".st-frozen", L[5] - .15)
    # midnight
    pop(".c-fix", T["fixes"] + .1, "scale:.7,opacity:0", .3, "back.out(2)")
    count(".nfix", T["fixes"] + .2, 0, 2.4, 1.8, "o.v.toFixed(1)", "power1.out")
    out(".c-fix", T["nobody"] - .25)
    pop(".c-why", T["nobody"] - .1, "scale:.8,opacity:0", .35, "back.out(1.8)")
    add(f'tl.fromTo(".c-why .big",{{x:0}},{{x:5,duration:.05,yoyo:true,repeat:9,ease:"none",immediateRender:false}},{T["why"]:.3f});')
    out(".c-why", E[5] + .2)
    # morning: the real world, then the question
    pop(".c-real", T["google"] - .15, "y:40,opacity:0", .35, "back.out(1.8)")
    out(".c-real", T["real"] - .3)
    pop(".c-q", T["real"] - .1, "scale:.8,opacity:0", .4, "back.out(1.8)")
    out(".c-q", E[6] + .2)
    # CTA
    pop("#endc", L[7] - .1, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    a = T["citykw"] - .1
    pop(".ec-kw", L[7] + .15, "scale:.6,opacity:0", .3, "back.out(2.2)")
    for i in range(4):
        pop(f".ty{i}", a + .05 + i * .08, "opacity:0,y:-30,scale:1.4", .14, "back.out(3)")
    add(f'tl.fromTo(".cur",{{opacity:1}},{{opacity:0,duration:.22,yoyo:true,repeat:{int((DUR - a) / .44)},ease:"steps(1)",immediateRender:false}},{a:.3f});')
    pop(".ec-2", L[7] + .35, "y:20,opacity:0", .3)
    pop(".ec-h", L[7] + .55, "y:20,opacity:0", .3)
    # the top bar: progress, the WHAT IF light, the city clock (written per frame from the same hour curve as city.js)
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')
    add(f'tl.fromTo(".live b",{{opacity:1}},{{opacity:.15,duration:.45,yoyo:true,repeat:{int(DUR / .45)},ease:"sine.inOut",immediateRender:false}},0);')
    add('(()=>{const o={v:0};tl.to(o,{v:%s,duration:%s,ease:"none",onUpdate:()=>{const h=cityHour(o.v);const d=h>=24?2:1;const x=((h%%24)+24)%%24;'
        'const hh=Math.floor(x),mm=Math.floor((x-hh)*60);document.querySelector(".clk b").textContent=String(hh).padStart(2,"0")+":"+String(mm).padStart(2,"0");'
        'document.querySelector(".clk span").textContent="DAY "+d;}},0);})();' % (DUR, DUR))
    pop(".clk", .3, "opacity:0,y:-10", .3, "power2.out")


# ---------------------------------------------------------------- captions: cards of up to 4 words, the spoken word boxed
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
    ty = "".join(f'<span class="ty ty{i}">{c}</span>' for i, c in enumerate("CITY"))
    return ('<div id="endc"><div class="ec-1">Follow + comment</div><div class="ec-kw">' + ty + '<i class="cur"></i></div>'
            '<div class="ec-2">and I\'ll send you the cities already testing this</div><div class="ec-h mono">@ai.nxtlvl</div></div>')


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
.brand { font-size: 26px; letter-spacing: 4px; display: flex; align-items: center; gap: 12px; }
.brand b { width: 16px; height: 16px; border-radius: 50%; background: #E8735A; }
.live { display: flex; align-items: center; gap: 8px; font-size: 20px; letter-spacing: 2px; color: #A8452F; }
.live b { width: 12px; height: 12px; border-radius: 50%; background: #D9483B; }
.clk { display: flex; align-items: baseline; gap: 10px; opacity: 0; }
.clk span { font-size: 20px; letter-spacing: 2px; color: #5b5650; }
.clk b { font-size: 36px; letter-spacing: 1px; }
.prog { width: 120px; height: 20px; border-radius: 10px; border: 3px solid #1E1B18; overflow: hidden; }
.prog i { display: block; height: 100%; background: #E8735A; transform-origin: 0 50%; transform: scaleX(0); }
.card, .stamp, #endc, .ec-kw, .ec-2, .ec-h, .ty, .arrow { opacity: 0; }
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
.c-real { max-width: 900px; }
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
.ec-kw { display: inline-block; min-width: 520px; min-height: 175px; margin: 14px 0 10px; padding: 6px 54px; border-radius: 40px; background: #D45C40; border: 3px solid #1E1B18;
  font: 800 150px/1.1 "Manrope"; letter-spacing: 4px; color: #fff; }
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
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI City 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b></b>AI.NXTLVL</span><span class="clk mono"><span>DAY 1</span><b>05:00</b></span>
          <span class="live mono"><b></b>WHAT IF</span><span class="prog"><i></i></span></div>
        {CARDS}{endcard()}
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4">{caps}</div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.CT = {json.dumps(ct)};
      const HOURS = {json.dumps(HOURS)};
      const L = window.CT.l, E = window.CT.e;
      const clamp = (x, a, b) => Math.min(b, Math.max(a, x)), ramp = (t, a, b) => clamp((t - a) / (b - a), 0, 1);
      const sm = (x) => x * x * (3 - 2 * x);
      function cityHour(t) {{
        let h = HOURS[0][0];
        for (let k = 0; k < L.length; k++) {{
          const h0 = HOURS[k][0], h1 = HOURS[k][1];
          if (t < L[k] - .35) break;
          const prev = k ? HOURS[k - 1][1] : h0;
          h = prev + (h0 - prev) * sm(ramp(t, L[k] - .35, L[k] + .55)) + (h1 - h0) * ramp(t, L[k] + .55, E[k] + .2);
        }}
        return h;
      }}
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/city.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
