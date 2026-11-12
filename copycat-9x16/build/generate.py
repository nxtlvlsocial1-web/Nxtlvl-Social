"""Copycat reel ("What if you could see every move your competitor makes?"): writes index.html. 1080x1920, 30 fps, under 60 s.
Account: @nxtlvlsocial.ai. Film noir in the house voxel style, black and white with selective colour. Midnight, rain: June,
a baker, walks into detective Kane's office; the bakery across the street copies every post she makes. Kane sets up five
open-source tools on public pages only (changedetection.io, RSSHub, Miniflux, Huginn, Ollama), pinned to his case board with
red string. At 2 AM the rival changes her prices and they know in under a minute; in the morning they find her "coming
Friday" lavender croissant, so June launches hers on Thursday, and on Friday the rival's customers cross the street.
Keyword CTA: comment SPY (we DM the free "Competitor Watch Kit" PDF).

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

# the five case cards: tool, the paid tool it stands in for, the card's one-line tag, what it does (the HTML card)
TOOLS = [
    ("changedetection.io", "Visualping", "WATCHES HER PAGES", "Watches her menu, prices and \"coming soon\" page. Flags every change."),
    ("RSSHub", "paid scrapers", "TURNS PAGES INTO FEEDS", "Turns her website, blog and public posts into feeds."),
    ("Miniflux", "Feedly Pro", "ONE QUIET INBOX", "Every update from every feed, in one reader."),
    ("Huginn", "IFTTT Pro", "PINGS YOUR PHONE", "Agents that ping your phone the minute she posts."),
    ("Ollama", "ChatGPT Plus", "WRITES THE BRIEFING", "A local AI that reads it all and writes your 7 AM briefing."),
]
OPEN = 2.6                      # the cut from the street to the office
M0 = r3(E[2] + .3)              # the case board
NT = [r3(M0 + .2 + 3.0 * k) for k in range(5)]
A0 = r3(L[3] - .3)              # 2 AM: the alert
D0 = r3(E[3] + .9)              # morning
TH = r3(E[5] + .3)              # Thursday
FR = r3(TH + 2.6)               # Friday
T = {
    "who": WHO, "open": OPEN, "montage": M0, "tools": NT, "alert": A0, "morning": D0, "thu": TH, "fri": FR, "endc": r3(L[7] - .3), "end": DUR,
    "bolts": [.85, r3(OPEN + .4), r3(NT[1] + 2.2), r3(A0 - .05)],      # lightning (and thunder in build/audio.py)
    "toolNames": [x[0] for x in TOOLS], "toolRep": [x[1] for x in TOOLS], "toolTag": [x[2] for x in TOOLS],
    # the office clock, minutes after midnight: 12:00 -> 1:59 at the alert -> 2:00 | 8:15 in the morning
    "clock": [[0, 0], [M0, 12], [A0 - .05, 119], [A0 + .1, 120], [D0 - .05, 124], [D0, 495], [DUR, 500]],
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


def story():
    html = []
    for c in ("t0", "t1", "t2", "t3"):
        show(f"#title .{c}", 0, .01, "opacity:1", "opacity:1")
    add('tl.fromTo("#title .t2",{scale:1.05},{scale:1,duration:1.4,ease:"power2.out",immediateRender:false},0);')
    hide("#title", OPEN - .25, .35, "opacity:0,y:-30")
    # time cards, typed
    for k, (txt, t0, d) in enumerate([("MIDNIGHT", OPEN + .15, 1.7), ("2:00 AM", A0 + .15, 1.6), ("8:15 AM", D0 + .1, 1.4), ("THURSDAY", TH + .1, 1.6), ("FRIDAY", FR + .1, 1.2)]):
        html.append(f'<div class="when" id="when{k}">{txt}</div>')
        add(f'tl.fromTo("#when{k}",{{opacity:0,scale:1.12}},{{opacity:1,scale:1,duration:.45,ease:"power2.out",immediateRender:false}},{t0:.3f});')
        hide(f"#when{k}", t0 + d, .3)
    # a case card for each tool
    for k, (nm, rep, tag, does) in enumerate(TOOLS):
        n = NT[k]
        cid = f"#tool{k}"
        show(cid, n - .1, .3, "opacity:0,y:-16,rotation:-2", "opacity:1,y:0,rotation:0")
        hide(cid, n + 2.75, .22, "opacity:0,y:-12")
        html.append(f'<div class="tool" id="tool{k}"><div class="ex">EXHIBIT {"ABCDE"[k]}</div><div class="nm">{nm}</div>'
                    f'<div class="rp">instead of {rep}</div><div class="ds">{does}</div><div class="fr">FREE · OPEN SOURCE</div></div>')
    # what the tools found in the morning
    show("#found", L[4] + .2, .35, "opacity:0,scale:1.08", "opacity:1,scale:1")
    hide("#found", E[5] - .1, .3)
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
.cap, .tool, .when, #found, #endc, #endc span { opacity: 0; }
#title { position: absolute; left: 60px; right: 60px; top: 400px; text-align: center; color: #F4F1EA; }
#title .t0 { display: inline-block; padding: 10px 26px; border: 3px solid #F4F1EA; color: #F4F1EA; font: 700 34px/1 "JBMono"; letter-spacing: 8px; margin-bottom: 30px; }
#title .t1, #title .t3 { display: block; font: 500 76px/1.1 "Garamond"; }
#title .t2 { display: block; font: italic 700 112px/1.05 "Garamond"; color: #FFFFFF; }
#title .t3 b { color: #FF3B30; font-weight: 700; }
.when { position: absolute; left: 0; right: 0; top: 300px; text-align: center; font: 700 46px/1 "JBMono"; color: #F4F1EA; letter-spacing: 10px; text-shadow: 0 3px 16px rgba(0,0,0,.8); }
.tool { position: absolute; left: 100px; right: 100px; top: 400px; padding: 24px 30px 26px; background: #E4D7B4; color: #1E1B18; text-align: left;
  box-shadow: 0 18px 40px rgba(0,0,0,.6); border-top: 10px solid #1E1B18; }
.tool .ex { display: inline-block; padding: 6px 14px; border: 3px solid #D7261C; color: #D7261C; font: 700 26px/1 "JBMono"; letter-spacing: 4px; transform: rotate(-3deg); }
.tool .nm { margin-top: 14px; font: 700 56px/1.05 "JBMono"; letter-spacing: -1px; }
.tool .rp { margin-top: 8px; font: 700 30px/1.2 "JBMono"; color: #6A5A3A; }
.tool .ds { margin-top: 12px; font: 600 32px/1.3 "Manrope"; }
.tool .fr { margin-top: 14px; font: 700 26px/1 "JBMono"; letter-spacing: 4px; color: #1E1B18; }
#found { position: absolute; left: 110px; right: 110px; top: 380px; padding: 22px 28px; background: rgba(12,10,18,.92); border: 3px solid #B26BFF; color: #F4F1EA; text-align: center; }
#found .f0 { font: 700 26px/1.2 "JBMono"; letter-spacing: 3px; color: #D9B8FF; }
#found .f1 { margin-top: 10px; font: italic 700 64px/1.05 "Garamond"; color: #FFFFFF; }
#found .f2 { margin-top: 8px; font: 700 30px/1 "JBMono"; letter-spacing: 6px; color: #B26BFF; }
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
    ct = {"l": L, "e": E, "cuts": [OPEN, M0, A0, D0, TH, FR], **T}
    ui = ('<div id="title" class="shadow"><span class="t0">WHAT IF</span><span class="t1">you could see</span>'
          '<span class="t2">every move</span><span class="t3">your <b>competitor</b> makes?</span></div>'
          + cards +
          '<div id="found"><div class="f0">CRUMB &amp; CO. · "COMING SOON" PAGE</div><div class="f1">Lavender croissant</div><div class="f2">FRIDAY</div></div>'
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
