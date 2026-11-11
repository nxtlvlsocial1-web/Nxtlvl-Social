"""Autopilot reel ("What if your marketing ran itself while you slept?"): writes index.html. 1080x1920, 30 fps, under 60 s.
Account: @nxtlvlsocial.ai. Rosa runs a small café and is drowning in messages at 11 PM. Her friend Theo sets up six
open-source automations and tells her to go to sleep. Through the night six neon signs light up on the café wall, one per
tool (Activepieces, Chatwoot, Cal.com, Mautic, Formbricks, Flowise), streams of light fly from her phone to each, and the
clock races. At 4:12 AM a post goes viral and the system handles it. At dawn she wakes to 1,147 messages handled and 63
bookings, for $0 in software. Keyword CTA: comment AUTOPILOT (we DM the free "Autopilot Stack" PDF).

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D (assets/js/autopilot.js) plays the shot list; this file writes the HTML layer: the title, the clock and the two
counters, a card for every tool, the viral banner, the morning stats, captions and the end card.
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

# the six neon signs: tool, label under it, colour, the paid tool it replaces, what it does for the café
TOOLS = [
    ("ACTIVEPIECES", "AUTOMATIONS", "#FF4FD8", "Zapier", "Every new lead goes straight into her CRM"),
    ("CHATWOOT", "ONE INBOX", "#4FC3FF", "Intercom", "Instagram, WhatsApp and web chat, answered in one inbox"),
    ("CAL.COM", "BOOKINGS", "#FFE14F", "Calendly", "Tables and events booked automatically"),
    ("MAUTIC", "EMAIL", "#FFA14F", "HubSpot email", "Welcome emails and follow-ups, sent on time"),
    ("FORMBRICKS", "FORMS", "#5BE38A", "Typeform", "Pre-orders and feedback, collected for her"),
    ("FLOWISE", "AI AGENT", "#B987FF", "paid AI chatbots", "An AI that answers questions at 3 AM"),
]
M0 = r3(E[1] + .5)
NT = [r3(M0 + .9 + 4.5 * k) for k in range(6)]
V0 = r3(M0 + 27.2)
D0 = r3(V0 + 6.5)   # dawn; Rosa speaks 2.2 s later
HANDLED = [18, 218, 226, 236, 241, 247]
BOOKED = [0, 0, 27, 33, 38, 41]
T = {
    "who": WHO, "montage": M0, "neon": NT, "viral": V0, "dawn": D0, "endc": r3(L[4] - .3), "end": DUR,
    "neonNames": [x[0] for x in TOOLS], "neonSub": [x[1] for x in TOOLS], "neonCol": [x[2] for x in TOOLS],
    # story clock, minutes after midnight (past 1440 wraps): 11:04 PM -> 11:30 -> 4:00 AM -> 4:12 -> 4:40 | 6:58 -> 7:03
    "clock": [[0, 1384], [E[1], 1386], [M0, 1410], [V0, 1680], [V0 + 1.0, 1692], [D0 - .05, 1720], [D0, 1858], [DUR, 1863]],
    "handled": [[0, 0], [M0, 0]] + [[NT[k] + .6, HANDLED[k]] for k in range(6)] + [[V0, 247], [V0 + 1.0, 262], [V0 + 4.2, 1147], [DUR, 1147]],
    "booked": [[0, 0], [M0, 0]] + [[NT[k] + .6, BOOKED[k]] for k in range(6)] + [[V0, 41], [V0 + 1.0, 41], [V0 + 4.2, 63], [DUR, 63]],
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


NAMES = {"rosa": "ROSA", "theo": "THEO"}


def story():
    html = []
    show(".t0", 0, .01, "opacity:1", "opacity:1"); show(".t1", 0, .01, "opacity:1", "opacity:1"); show(".t2", 0, .01, "opacity:1", "opacity:1"); show(".t3", 0, .01, "opacity:1", "opacity:1")
    add('tl.fromTo("#title .t2",{scale:1.05},{scale:1,duration:1.4,ease:"power2.out",immediateRender:false},0);')
    hide("#title", 2.6, .4, "opacity:0,y:-30")
    # the HUD: the clock (left) and the night's tally (right)
    show("#hud", 2.9, .4, "opacity:0,y:-14")
    last = (None, None, None)
    t = 0.0
    while t < DUR:
        hm, ap = clock_text(interp(T["clock"], t))
        n, b = round(interp(T["handled"], t)), round(interp(T["booked"], t))
        if hm != last[0]:
            setText("#hud .c-hm", hm, t); setText("#hud .c-ap", ap, t)
        if n != last[1]:
            setText("#hud .n-h", f"{n:,}", t)
        if b != last[2]:
            setText("#hud .n-b", f"{b:,}", t)
        last = (hm, n, b)
        t = round(t + (.1 if M0 <= t < D0 else .25), 3)
    add(f'tl.to("#hud .n-h",{{color:"#5BE38A",duration:.3}},{V0 + 1.2:.3f});')
    hide("#hud", L[3] + .05, .3, "opacity:0,y:-14")
    # a card for each tool as its sign lights
    for k, (nm, sub, col, rep, does) in enumerate(TOOLS):
        n = NT[k]
        cid = f"#tool{k}"
        show(cid, n - .15, .3, "opacity:0,y:-16,scale:.97", "opacity:1,y:0,scale:1")
        hide(cid, n + 3.75, .25, "opacity:0,y:-12")
        html.append(f'<div class="tool" id="tool{k}" style="--c:{col}"><div class="nm">{nm.title() if nm != "CAL.COM" else "Cal.com"}</div>'
                    f'<div class="rp">replaces {rep}</div><div class="ds">{does}</div><div class="fr">FREE · OPEN SOURCE</div></div>')
    # 4:12 AM: viral
    show("#viral", V0 + .25, .3, "opacity:0,scale:1.12", "opacity:1,scale:1")
    add(f'tl.fromTo("#viral .vn",{{scale:1.3}},{{scale:1,duration:.5,ease:"back.out(2)",immediateRender:false}},{V0 + 1.0:.3f});')
    hide("#viral", V0 + 4.4, .3)
    # the morning stats, on Theo's "For zero dollars"
    show("#stats", L[3] + .2, .4, "opacity:0,scale:1.1", "opacity:1,scale:1")
    hide("#stats", E[3] + .5, .3)
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
        parts = [text] if len(text) < 56 else [p for p in re.split(r"(?<=[.?!,])\s+(?=[A-Z0-9])", text) if p]
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
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #070A16; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #070A16; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.shadow { text-shadow: 0 3px 18px rgba(0,0,0,.6), 0 1px 3px rgba(0,0,0,.6); }
#hud, .cap, .tool, #viral, #stats, #endc, #endc span { opacity: 0; }
#title { position: absolute; left: 70px; right: 70px; top: 430px; text-align: center; color: #FFFDF6; }
#title .t0 { display: inline-block; padding: 10px 26px; border-radius: 40px; background: #F2C94C; color: #1E1B18; font: 800 34px/1 "Manrope"; letter-spacing: 6px; margin-bottom: 30px; }
#title .t1, #title .t3 { display: block; font: 500 78px/1.1 "Garamond"; }
#title .t2 { display: block; font: 700 116px/1.05 "Garamond"; color: #F2C94C; }
#hud { position: absolute; left: 64px; right: 64px; top: 268px; display: flex; justify-content: space-between; color: #FFFDF6; }
#hud .lab { display: block; font: 800 26px/1 "Manrope"; letter-spacing: 4px; color: rgba(255,253,246,.85); }
#hud .clk { display: block; margin-top: 8px; font: 700 80px/1 "Garamond"; }
#hud .clk small { font: 800 30px/1 "Manrope"; margin-left: 8px; letter-spacing: 2px; }
#hud .tally { text-align: right; }
#hud .row { display: block; margin-top: 8px; font: 700 52px/1.05 "Garamond"; }
#hud .row small { font: 800 28px/1 "Manrope"; letter-spacing: 2px; color: rgba(255,253,246,.8); margin-left: 6px; }
.tool { position: absolute; left: 90px; right: 90px; top: 440px; padding: 22px 28px 24px; border-radius: 28px; background: rgba(10,10,20,.9); border: 2px solid var(--c);
  box-shadow: 0 0 40px color-mix(in srgb, var(--c) 45%, transparent); text-align: center; color: #FFFDF6; }
.tool .nm { font: 800 58px/1.05 "Manrope"; color: var(--c); letter-spacing: 1px; }
.tool .rp { margin-top: 8px; font: 700 32px/1.2 "Manrope"; color: #FF9A8F; }
.tool .ds { margin-top: 10px; font: 600 32px/1.3 "Manrope"; }
.tool .fr { margin-top: 12px; font: 800 28px/1 "Manrope"; letter-spacing: 5px; color: #5BE38A; }
#viral { position: absolute; left: 90px; right: 90px; top: 460px; padding: 26px 30px; border-radius: 30px; background: rgba(10,10,20,.92); border: 2px solid #E1306C; text-align: center; color: #FFFDF6; }
#viral .vt { font: 800 30px/1.2 "Manrope"; letter-spacing: 3px; color: #FF8AB3; }
#viral .vn { display: inline-block; margin-top: 8px; font: 800 120px/1 "Manrope"; color: #FFD34A; }
#viral .vs { margin-top: 8px; font: 700 34px/1.2 "Manrope"; }
#stats { position: absolute; left: 70px; right: 70px; top: 360px; text-align: center; color: #FFFDF6; }
#stats .s1 { display: block; font: 800 30px/1 "Manrope"; letter-spacing: 6px; }
#stats .s2 { display: block; margin-top: 12px; font: 700 96px/1.02 "Garamond"; }
#stats .s2 b { color: #5BE38A; }
#stats .s3 { display: block; margin-top: 8px; font: 700 124px/1 "Garamond"; color: #F2C94C; }
#stats .s4 { display: block; margin-top: 4px; font: 800 28px/1 "Manrope"; letter-spacing: 4px; }
.cap { position: absolute; left: 60px; right: 60px; top: 1300px; text-align: center; }
.cap .who { display: inline-block; margin-bottom: 10px; padding: 7px 16px; border-radius: 20px; font: 800 26px/1 "Manrope"; letter-spacing: 4px; color: #0B0D12; background: #F2C94C; }
.cap .tx { display: inline; padding: 8px 18px; border-radius: 16px; font: 800 48px/1.5 "Manrope"; color: #FFFFFF; background: rgba(8,10,16,.82); -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.cap .br { display: block; height: 0; }
.cap.sp-theo .who { background: #5BE38A; }
#endc { position: absolute; left: 70px; right: 70px; top: 330px; text-align: center; color: #FFFDF6; }
#endc span { display: block; }
#endc .e0 { font: italic 500 70px/1.1 "Garamond"; }
#endc .e1 { margin-top: 6px; font: 800 132px/1 "Manrope"; letter-spacing: 4px; color: #F2C94C; }
#endc .e2 { margin-top: 14px; font: italic 500 54px/1.15 "Garamond"; }
#endc .e3 { margin-top: 40px; font: 800 30px/1.4 "Manrope"; letter-spacing: 5px; }
#endc .e3 b { display: block; font: 800 42px/1.3 "Manrope"; letter-spacing: 2px; }
"""


def main():
    tools = story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, "cuts": [M0, V0, D0], **T}
    hm, ap = clock_text(T["clock"][0][1])
    ui = ('<div id="title" class="shadow"><span class="t0">WHAT IF</span><span class="t1">your marketing ran itself</span>'
          '<span class="t2">while you slept?</span><span class="t3"></span></div>'
          f'<div id="hud" class="shadow"><div><span class="lab">ROSA\'S CAFÉ</span><span class="clk"><span class="c-hm">{hm}</span><small class="c-ap">{ap}</small></span></div>'
          '<div class="tally"><span class="row"><span class="n-h">0</span><small>HANDLED</small></span><span class="row"><span class="n-b">0</span><small>BOOKINGS</small></span></div></div>'
          + tools +
          '<div id="viral"><div class="vt">4:12 AM · HER REEL IS GOING VIRAL</div><div class="vn">+900</div><div class="vs">new followers, every one answered</div></div>'
          '<div id="stats" class="shadow"><span class="s1">WHILE SHE SLEPT</span><span class="s2"><b>1,147</b> handled<br><b>63</b> bookings</span>'
          '<span class="s3">$0</span><span class="s4">IN SOFTWARE</span></div>'
          '<div id="endc" class="shadow"><span class="e0">Want the whole setup?</span><span class="e1">AUTOPILOT</span>'
          '<span class="e2">Comment it and I\'ll DM you every tool</span>'
          '<span class="e3">FOLLOW<b>@nxtlvlsocial.ai</b></span></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Autopilot 9x16</title>
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
    <script type="module" src="assets/js/autopilot.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
