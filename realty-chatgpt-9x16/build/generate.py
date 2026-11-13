"""Real estate what-if ("What if ChatGPT sent all your clients to your competitor?"): writes index.html. 1080x1920, 30 fps,
under 60 s. Account: @nxtlvlsocial.ai. Voxel what-if in full colour: Keystone Realty is empty while every house hunter asks
ChatGPT for an agent and a floating answer card says Prime Nest Realty. Junior agent Lena claims the agency in Business Hub
(Businesses in ChatGPT, beta, launched 10 Nov 2026), a blue check snaps onto the sign and the crowd crosses back.
Keyword CTA: comment CHATGPT (we DM the free "Get Your Business into ChatGPT" checklist PDF). The story's effect is
illustrative: the end card and description say claiming doesn't guarantee a higher ranking, and that local businesses may
need an existing US listing for now.

python3 build/generate.py      (from the project root, after build/voice.py)
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
WHO = [ln["speaker"] for ln in LINES]
r3 = lambda x: round(x, 3)  # noqa: E731

A = []


def add(js):
    A.append("      " + js)


def show(sel, t, d=.35, frm="opacity:0,y:14", to="opacity:1,y:0", ease="power2.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def hide(sel, t, d=.3, props="opacity:0"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


def setText(sel, txt, t):
    add(f'tl.set("{sel}",{{textContent:{json.dumps(txt)}}},{t:.3f});')


def interp(keys, t):
    for (a, x), (b, y) in zip(keys, keys[1:]):
        if a <= t < b:
            return x + (y - x) * (t - a) / max(1e-6, b - a)
    return keys[-1][1]


def clock_text(m):
    m = int(m) % 1440
    h, mi = divmod(m, 60)
    return f"{(h % 12) or 12}:{mi:02d}", ("AM" if h < 12 else "PM")


NAMES = {"marcus": "MARCUS", "lena": "LENA"}
IN0 = r3(L[3] - .35)            # inside the office
CK = r3(L[5] - 1.45)            # the blue check snaps on (a full beat before Marcus sees it)
FL = r3(E[5] + .2)              # the cards flip, the crowd crosses back
NX = r3(L[7] - .35)             # a full office
w5 = [w for w in WORDS if w["line"] == 5]
def wt(word):
    return next(w["s"] for w in w5 if w["w"].strip(".,").lower() == word.lower())
STEPS = [r3(wt("Business")), r3(wt("Search")), r3(wt("Verify")), r3(wt("Quick"))]
CARDS = [[r3(STEPS[0] - .2), r3(CK + .1)], [r3(L[6] - .1), r3(E[6] + .3)]]
T = {"who": WHO, "inside": IN0, "check": CK, "flip": FL, "next": NX, "steps": STEPS, "cards": CARDS, "endc": r3(L[8] - .3), "end": DUR,
     "lines": [{"s": ln["start"], "e": ln["end"]} for ln in LINES]}


def story():
    html = []
    for c in ("t0", "t1", "t2", "t3"):
        show(f"#title .{c}", 0, .01, "opacity:1", "opacity:1")
    add('tl.fromTo("#title .t2",{scale:1.05},{scale:1,duration:1.4,ease:"power2.out",immediateRender:false},0);')
    hide("#title", 2.5, .35, "opacity:0,y:-30")
    # the four steps, ticked off as Zara says them
    html.append('<div id="steps"><div class="sh">CLAIM YOUR BUSINESS IN CHATGPT</div>' + "".join(
        f'<div class="st" id="st{k}"><span class="n">{k + 1}</span><span class="tx">{s}</span><span class="ok"></span></div>' for k, s in enumerate(
            ["Open chatgpt.com/business-hub", "Search your business, tap Get Started", "Verify: phone, email, website or Shopify", "Quick ID check: blue check"])) + "</div>")
    show("#steps", CARDS[0][0], .3, "opacity:0,y:-20", "opacity:1,y:0")
    for k, t0 in enumerate(STEPS):
        show(f"#st{k}", t0 - .05, .25, "opacity:.35", "opacity:1")
        show(f"#st{k} .ok", t0 + .35, .25, "opacity:0,scale:0", "opacity:1,scale:1", "back.out(3)")
    hide("#steps", CARDS[0][1], .3)
    html.append('<div id="news"><span class="k">REAL, NOT A WHAT-IF</span><span class="t">Launched Nov 10</span><span class="f">FREE · BETA</span></div>')
    show("#news", CARDS[1][0], .35, "opacity:0,scale:1.1", "opacity:1,scale:1")
    hide("#news", CARDS[1][1], .3)
    show("#endc", T["endc"], .5, "opacity:0", "opacity:1")
    show("#endc .e0", T["endc"] + .05, .4, "opacity:0,y:14")
    show("#endc .e1", T["endc"] + .3, .5, "opacity:0,scale:1.15", "opacity:1,scale:1")
    show("#endc .e2", T["endc"] + .7, .4, "opacity:0,y:14")
    show("#endc .e3", T["endc"] + 1.0, .4, "opacity:0,y:14")
    show("#endc .e4", T["endc"] + 1.3, .4, "opacity:0", "opacity:1")
    return "".join(html)


def captions():
    html = []
    for k, ln in enumerate(LINES):
        if k == len(LINES) - 1:
            continue
        text = ln["text"]
        parts = [text] if len(text) < 48 else [p for p in re.split(r"(?:(?<=\.\.\.)|(?<=[,?]))\s+", text) if p]
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        wi = 0
        nxt = LINES[k + 1]["start"] if k + 1 < len(LINES) else DUR
        for j, p in enumerate(parts):
            n = len(p.split())
            a0 = ws[min(wi, len(ws) - 1)]["s"] - .1
            z = ws[wi + n]["s"] - .3 if wi + n < len(ws) else min(ln["end"] + .3, nxt - .2)
            wi += n
            pid = f"c{k}_{j}"
            who = ln["speaker"]
            html.append(f'<div class="cap sp-{who}" id="{pid}"><span class="who">{NAMES[who]}</span><span class="br"></span><span class="tx">{p}</span></div>')
            add(f'tl.fromTo("#{pid}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.22,ease:"power2.out",immediateRender:false}},{a0:.3f});')
            add(f'tl.to("#{pid}",{{opacity:0,duration:.18,ease:"power1.in"}},{z:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Garamond"; font-weight: 400 800; src: url("assets/fonts/EBGaramond.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #BFD9F2; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #BFD9F2; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.shadow { text-shadow: 0 3px 18px rgba(0,0,0,.55), 0 1px 3px rgba(0,0,0,.6); }
.cap, #steps, #news, #endc, #endc span { opacity: 0; }
#title { position: absolute; left: 60px; right: 60px; top: 330px; text-align: center; color: #FFFDF6; }
#title .t0 { display: inline-block; padding: 10px 26px; border-radius: 40px; background: #F2C94C; color: #1E1B18; font: 800 34px/1 "Manrope"; letter-spacing: 6px; margin-bottom: 26px; text-shadow: none; }
#title .t1, #title .t3 { display: block; font: 500 74px/1.08 "Garamond"; }
#title .t2 { display: block; font: 700 112px/1.02 "Garamond"; color: #F2C94C; }
#steps { position: absolute; left: 60px; right: 60px; top: 290px; padding: 24px 26px 18px; border-radius: 26px; background: rgba(12,14,22,.9); color: #fff; }
#steps .sh { font: 800 26px/1 "Manrope"; letter-spacing: 4px; color: #F2C94C; margin-bottom: 14px; }
#steps .st { display: flex; align-items: center; gap: 18px; padding: 12px 0; border-top: 1px solid rgba(255,255,255,.12); opacity: .35; }
#steps .n { flex: none; width: 54px; height: 54px; border-radius: 50%; background: #F2C94C; color: #1E1B18; font: 800 32px/54px "Manrope"; text-align: center; }
#steps .tx { flex: 1; font: 700 36px/1.2 "Manrope"; }
#steps .ok { flex: none; width: 46px; height: 46px; border-radius: 50%; background: #2F7BF6; opacity: 0; position: relative; }
#steps .ok::after { content: ""; position: absolute; left: 15px; top: 9px; width: 11px; height: 20px; border: solid #fff; border-width: 0 5px 5px 0; transform: rotate(45deg); }
#news { position: absolute; left: 140px; right: 140px; top: 270px; padding: 26px; border-radius: 30px; background: rgba(12,14,22,.9); text-align: center; color: #fff; }
#news .k { display: block; font: 800 26px/1 "Manrope"; letter-spacing: 4px; color: #5BE38A; }
#news .t { display: block; margin-top: 14px; font: 800 72px/1 "Manrope"; }
#news .f { display: block; margin-top: 12px; font: 800 34px/1 "Manrope"; letter-spacing: 6px; color: #F2C94C; }
.cap { position: absolute; left: 60px; right: 60px; top: 1300px; text-align: center; }
.cap .who { display: inline-block; margin-bottom: 10px; padding: 7px 16px; border-radius: 20px; font: 800 26px/1 "Manrope"; letter-spacing: 4px; color: #0B0D12; background: #F2C94C; }
.cap .tx { display: inline; padding: 8px 18px; border-radius: 16px; font: 800 48px/1.5 "Manrope"; color: #FFFFFF; background: rgba(8,10,16,.82); -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.cap .br { display: block; height: 0; }
.cap.sp-lena .who { background: #2F6F5E; color: #fff; }
#endc { position: absolute; left: 60px; right: 60px; top: 300px; text-align: center; color: #FFFDF6; }
#endc span { display: block; }
#endc .e0 { font: italic 500 68px/1.1 "Garamond"; }
#endc .e1 { margin-top: 6px; font: 800 140px/1 "Manrope"; letter-spacing: 2px; color: #F2C94C; }
#endc .e2 { margin-top: 12px; font: italic 500 52px/1.15 "Garamond"; }
#endc .e3 { margin-top: 34px; font: 800 30px/1.4 "Manrope"; letter-spacing: 5px; }
#endc .e3 b { display: block; font: 800 42px/1.3 "Manrope"; letter-spacing: 2px; }
#endc .e4 { margin-top: 24px; font: 700 24px/1.4 "Manrope"; color: rgba(255,253,246,.85); }
"""


def main():
    cards = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, "cuts": [IN0, CK, FL, NX], **T}
    ui = ('<div id="title" class="shadow"><span class="t0">WHAT IF</span><span class="t1">ChatGPT sent all</span>'
          '<span class="t2">your clients</span><span class="t3">to your competitor?</span></div>' + cards +
          '<div id="endc" class="shadow"><span class="e0">Want the checklist?</span><span class="e1">CHATGPT</span>'
          '<span class="e2">Comment it and I\'ll DM you the setup checklist</span>'
          '<span class="e3">FOLLOW<b>@nxtlvlsocial.ai</b></span>'
          '<span class="e4">Claiming doesn\'t guarantee a higher ranking. Local businesses may need an existing US listing for now.</span></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Realty ChatGPT 9x16</title>
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
    <script type="module" src="assets/js/realty.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
