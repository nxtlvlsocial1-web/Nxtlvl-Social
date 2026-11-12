"""Copycat reel ("What if you could see every move your competitor makes?"): writes index.html. 1080x1920, 30 fps, under 60 s.
Account: @nxtlvlsocial.ai. Film noir in the house voxel style, black and white with selective colour. Midnight, rain: June,
a baker, walks into detective Kane's office; the bakery across the street copies every post she makes. Kane sets up five
open-source tools on public pages only (changedetection.io, RSSHub, Miniflux, Huginn, Ollama), pinned to his case board with
red string. At 2 AM the rival changes her prices and they know in under a minute; in the morning they find her "coming
Friday" lavender croissant, so June launches hers on Thursday, and on Friday the rival's customers cross the street.
Keyword CTA: comment SPY (we DM the free "Competitor Watch Kit" PDF).
The re-cut plays it as a noir parody with three spoken clues, each shown big on a laptop screen, and says the payoff out loud.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D (assets/js/copycat.js) plays the shot list; this file writes the HTML layer: the title, the time cards, a case card
for every tool, captions and the end card.
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

# the three clues: tool on the case card, what it stands in for, the card's tag
TOOLS = [
    ("changedetection.io", "Visualping", "WATCHES HER PRICES"),
    ("RSSHub + Miniflux", "Feedly Pro", "EVERY POST, ONE FEED"),
    ("Ollama", "ChatGPT Plus", "WRITES YOUR BRIEFING"),
]
M0 = r3(L[2] - 1.0)             # the clues begin
NT = [r3(L[2 + k] - .85) for k in range(3)]
D0 = r3(E[4] + .35)             # 7 AM
TH = r3(E[6] + .3)              # Thursday
FR = r3(TH + 2.3)               # Friday
SCREENS = [[r3(NT[k] + .95), r3(E[2 + k] + .15)] for k in range(3)]
T = {
    "who": WHO, "montage": M0, "tools": NT, "morning": D0, "thu": TH, "fri": FR, "endc": r3(L[9] - .3), "end": DUR, "screens": SCREENS,
    "bolts": [.3],
    "toolNames": [x[0] for x in TOOLS], "toolRep": [x[1] for x in TOOLS], "toolTag": [x[2] for x in TOOLS],
    # the office clock, minutes after midnight: 12:01 -> 12:40 through the clues | 7:00 in the morning
    "clock": [[0, 1], [D0 - .05, 40], [D0, 420], [DUR, 424]],
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


def interp(keys, t):
    for (a, x), (b, y) in zip(keys, keys[1:]):
        if a <= t < b:
            return x + (y - x) * (t - a) / max(1e-6, b - a)
    return keys[-1][1]


def clock_text(m):
    m = int(m) % 1440
    h, mi = divmod(m, 60)
    return f"{(h % 12) or 12}:{mi:02d}", ("AM" if h < 12 else "PM")


NAMES = {"june": "JUNE", "kane": "KANE"}


def screen(k, t0, t1):
    """A clue on the laptop, blown up big enough to read: a dark window with the tool's name and what it found."""
    nm, rep, tag = TOOLS[k]
    head = f'<div class="bar"><span class="cl">CLUE {k + 1}</span><span class="tn">{nm}</span></div><div class="sub">instead of {rep} · free · open source</div>'
    if k == 0:
        rows = [("Croissant", "<s>$3.50</s> <b>$4.25</b>", True), ("Pain au chocolat", "$4.00", False), ("Cinnamon roll", "$4.50", False), ("Sourdough loaf", "$8.00", False)]
        body = '<div class="url">crumbandco.com/menu</div>' + "".join(f'<div class="row{" hit" if h else ""}"><span>{a}</span><span>{b}</span></div>' for a, b, h in rows) + '<div class="ft">changed 1 minute ago · alert sent</div>'
        add(f'tl.fromTo("#scr0 .ring",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)",immediateRender:false}},{t0 + 1.2:.3f});')
        body += '<div class="ring"></div>'
    elif k == 1:
        items = [("Instagram", "new post: \"our NEW croissant\""), ("Blog", "behind the counter"), ("Newsletter", "this weekend's special"), ("Website", "\"coming soon\" page updated")]
        body = '<div class="url">Miniflux · Crumb &amp; Co. · 4 new</div>' + "".join(f'<div class="feed" id="fd{j}"><b>{a}</b><span>{b}</span></div>' for j, (a, b) in enumerate(items))
        for j in range(4):
            add(f'tl.fromTo("#fd{j}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.25,ease:"power2.out",immediateRender:false}},{t0 + .35 + j * .45:.3f});')
    else:
        lines = ["7 AM BRIEFING", "1. Croissant price up 75 cents.", "2. Coming soon page, Friday:", "<em>LAVENDER CROISSANT</em>"]
        body = '<div class="url">Ollama · runs on your laptop</div>' + "".join(f'<div class="ty" id="ty{j}">{x}</div>' for j, x in enumerate(lines))
        for j in range(4):
            add(f'tl.fromTo("#ty{j}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:.2,ease:"power1.out",immediateRender:false}},{t0 + .3 + j * .75:.3f});')
    show(f"#scr{k}", t0, .3, "opacity:0,y:40,scale:.96", "opacity:1,y:0,scale:1")
    hide(f"#scr{k}", t1, .25, "opacity:0,y:-20")
    return f'<div class="scr" id="scr{k}">{head}<div class="body">{body}</div></div>'


def story():
    html = []
    for c in ("t0", "t1", "t2", "t3"):
        show(f"#title .{c}", 0, .01, "opacity:1", "opacity:1")
    add('tl.fromTo("#title .t2",{scale:1.05},{scale:1,duration:1.4,ease:"power2.out",immediateRender:false},0);')
    hide("#title", 2.4, .35, "opacity:0,y:-30")
    for k, (txt, t0, d) in enumerate([("7:00 AM", D0 + .1, 1.3), ("THURSDAY", TH + .1, 1.6), ("FRIDAY", FR + .1, 1.3)]):
        html.append(f'<div class="when" id="when{k}">{txt}</div>')
        add(f'tl.fromTo("#when{k}",{{opacity:0,scale:1.12}},{{opacity:1,scale:1,duration:.45,ease:"power2.out",immediateRender:false}},{t0:.3f});')
        hide(f"#when{k}", t0 + d, .3)
    for k in range(3):
        html.append(screen(k, *SCREENS[k]))
    # "She launches Friday. You launch Thursday." as two calendar pages
    html.append('<div id="cal"><div class="pg" id="calT"><div class="hd">THU</div><div class="who">YOU<br>LAUNCH</div></div>'
                '<div class="pg" id="calF"><div class="hd">FRI</div><div class="who">SHE<br>LAUNCHES</div></div></div>')
    show("#cal", L[6] - .1, .01, "opacity:0", "opacity:1")
    show("#calF", L[6] - .05, .3, "opacity:0,y:30,rotation:4", "opacity:1,y:0,rotation:4")
    show("#calT", L[6] + 1.25, .35, "opacity:0,scale:1.3,rotation:-4", "opacity:1,scale:1,rotation:-4", "back.out(2)")
    hide("#cal", E[6] + .25, .3)
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
        if k == len(LINES) - 1:
            continue
        text = ln["text"]
        parts = [text] if len(text) < 52 else [p for p in re.split(r"(?:(?<=\.\.\.)|(?<=[,?]))\s+", text) if p]
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
@font-face { font-family: "Garamond"; font-style: italic; font-weight: 400 800; src: url("assets/fonts/EBGaramond-Italic.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #05060A; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #05060A; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.shadow { text-shadow: 0 3px 18px rgba(0,0,0,.7), 0 1px 3px rgba(0,0,0,.7); }
.cap, .scr, .when, #endc, #endc span { opacity: 0; }
#title { position: absolute; left: 60px; right: 60px; top: 400px; text-align: center; color: #F4F1EA; }
#title .t0 { display: inline-block; padding: 10px 26px; border: 3px solid #F4F1EA; color: #F4F1EA; font: 700 34px/1 "JBMono"; letter-spacing: 8px; margin-bottom: 30px; }
#title .t1, #title .t3 { display: block; font: 500 76px/1.1 "Garamond"; }
#title .t2 { display: block; font: italic 700 112px/1.05 "Garamond"; color: #FFFFFF; }
#title .t3 b { color: #FF3B30; font-weight: 700; }
.when { position: absolute; left: 0; right: 0; top: 300px; text-align: center; font: 700 46px/1 "JBMono"; color: #F4F1EA; letter-spacing: 10px; text-shadow: 0 3px 16px rgba(0,0,0,.8); }
.scr { position: absolute; left: 70px; right: 70px; top: 470px; background: #0E0F13; border: 2px solid #3A3D46; border-radius: 18px; overflow: hidden; color: #F4F1EA; box-shadow: 0 30px 60px rgba(0,0,0,.65); }
.scr .bar { display: flex; align-items: center; gap: 18px; padding: 20px 26px; background: #1C1E25; }
.scr .cl { padding: 6px 12px; border: 3px solid #FF3B30; color: #FF3B30; font: 700 26px/1 "JBMono"; letter-spacing: 3px; transform: rotate(-3deg); }
.scr .tn { font: 700 46px/1 "JBMono"; letter-spacing: -1px; }
.scr .sub { padding: 12px 26px 0; font: 700 24px/1.2 "JBMono"; color: #9AA0AA; letter-spacing: 1px; }
.scr .body { position: relative; padding: 18px 26px 28px; }
.scr .url { font: 700 26px/1.2 "JBMono"; color: #9AA0AA; margin-bottom: 14px; }
.scr .row { display: flex; justify-content: space-between; padding: 14px 6px; border-top: 1px solid #2A2D35; font: 700 40px/1.1 "Manrope"; }
.scr .row s { color: #8A8E96; } .scr .row b { color: #FF3B30; }
.scr .row.hit { color: #FFFFFF; }
.scr .ring { position: absolute; left: 6px; right: -6px; top: 70px; height: 82px; border: 6px solid #FF3B30; border-radius: 50%; transform: rotate(-2deg); }
.scr .ft { margin-top: 14px; font: 700 26px/1.2 "JBMono"; color: #FF8A80; }
.scr .feed { display: flex; gap: 16px; align-items: baseline; padding: 14px 6px; border-top: 1px solid #2A2D35; font: 600 34px/1.2 "Manrope"; }
.scr .feed b { flex: none; width: 210px; font: 700 26px/1 "JBMono"; color: #FF8A80; }
.scr .ty { font: 700 38px/1.5 "JBMono"; } .scr .ty em { font-style: normal; color: #C9A6FF; font-size: 46px; }
#cal { position: absolute; left: 0; right: 0; top: 470px; height: 520px; opacity: 0; }
#cal .pg { position: absolute; top: 0; width: 400px; height: 470px; background: #F4F1EA; border-radius: 16px; box-shadow: 0 24px 50px rgba(0,0,0,.6); text-align: center; color: #1E1B18; overflow: hidden; }
#cal .hd { padding: 26px 0 20px; font: 700 110px/1 "JBMono"; color: #FFFFFF; }
#cal .who { margin-top: 70px; font: 800 52px/1.15 "Manrope"; letter-spacing: 3px; }
#calT { left: 90px; } #calT .hd { background: #9B59F5; }
#calF { right: 90px; } #calF .hd { background: #4A4A50; } #calF .who { color: #6A6A70; }
.cap { position: absolute; left: 60px; right: 60px; top: 1300px; text-align: center; }
.cap .who { display: inline-block; margin-bottom: 10px; padding: 7px 16px; font: 700 26px/1 "JBMono"; letter-spacing: 5px; color: #0B0D12; background: #F4F1EA; }
.cap .tx { display: inline; padding: 8px 18px; border-radius: 12px; font: 800 48px/1.5 "Manrope"; color: #FFFFFF; background: rgba(8,8,10,.84); -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.cap .br { display: block; height: 0; }
.cap.sp-june .who { background: #C9A6FF; }
#endc { position: absolute; left: 70px; right: 70px; top: 330px; text-align: center; color: #F4F1EA; }
#endc span { display: block; }
#endc .e0 { font: italic 500 70px/1.1 "Garamond"; }
#endc .e1 { margin-top: 10px; font: 700 150px/1 "JBMono"; letter-spacing: 16px; color: #FF3B30; }
#endc .e2 { margin-top: 14px; font: italic 500 54px/1.15 "Garamond"; }
#endc .e3 { margin-top: 40px; font: 700 30px/1.4 "JBMono"; letter-spacing: 6px; }
#endc .e3 b { display: block; font: 800 42px/1.3 "Manrope"; letter-spacing: 2px; }
"""


def main():
    cards = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, "cuts": [M0, D0, TH, FR], **T}
    ui = ('<div id="title" class="shadow"><span class="t0">WHAT IF</span><span class="t1">you could see</span>'
          '<span class="t2">every move</span><span class="t3">your <b>competitor</b> makes?</span></div>'
          + cards +
          '<div id="endc" class="shadow"><span class="e0">Want the whole kit?</span><span class="e1">SPY</span>'
          '<span class="e2">Comment it and I\'ll DM you every tool</span>'
          '<span class="e3">FOLLOW<b>@nxtlvlsocial.ai</b></span></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Copycat 9x16</title>
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
    <script type="module" src="assets/js/copycat.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
