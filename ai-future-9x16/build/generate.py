"""AI Future reel ("What if your phone could see 24 hours into the future?"): writes index.html. 1080x1920, 30 fps.
Account: @nxtlvlsocial.ai. A cinematic what-if told in dialogue, no narrator: Alex's phone starts showing him tomorrow.
New York (the coffee at 9:14), Las Vegas with his friend Jay (black 17), Miami in a storm (the bridge), home on day 21
(a text from his own number: don't open the door; a knock; "that's not Jay"), day 30 (there is no tomorrow). The phone
speaks in its own AI voice and closes the reel with the question and the follow prompt. Pure what-if: no keyword CTA.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D (assets/js/future.js) plays a shot list per scene: wides, close-ups, over-the-shoulders, slow motion and POV
shots of the phone in Alex's hand. This file writes the HTML layer: the title card, the place/day tracker, the "next
day" stamp, speaker-tagged serif captions and the end card.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
DUR = round(LINES[-1]["end"] + 3.2, 2)


def word(line, text, nth=1, end=False):
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9$]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1]["e" if end else "s"]


L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
WHO = [ln["speaker"] for ln in LINES]
T = {
    "tom1": word(1, "tomorrow"), "coffee1": word(1, "coffee"),
    "black5": word(5, "black"), "trust": word(5, "trust"),
    "bridge9": word(9, "bridge"), "cars9": word(9, "14"),
    "follow": word(17, "follow"), "look": word(17, "look"),
    "end": DUR,
}
T["cuts"] = [round(L[3] - .35, 3), round(L[8] - .45, 3), round(L[12] - .5, 3), round(L[14] - .45, 3), round(E[15] + 1.0, 3)]
T["who"] = WHO
T["lines"] = [{"s": ln["start"], "e": ln["end"]} for ln in LINES]
CU = T["cuts"]
A = []


def add(js):
    A.append("      " + js)


def show(sel, t, d=.35, frm="opacity:0,y:14", to="opacity:1,y:0", ease="power2.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def hide(sel, t, d=.3, props="opacity:0"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


def setText(sel, txt, t):
    add(f'tl.set("{sel}",{{textContent:{json.dumps(txt)}}},{t:.3f});')


# the tracker: place and day
HUD = [(L[0] - .3, "NEW YORK", "1"), (CU[0], "LAS VEGAS", "4"), (CU[1], "MIAMI", "12"), (CU[2], "HOME", "21"), (CU[3], "HOME", "30")]
NAMES = {"alex": "ALEX", "jay": "JAY", "phone": "THE PHONE", "dealer": "DEALER", "driver": "DRIVER"}


def story():
    # title card, then it lifts
    show("#title", 0.0, .01, "opacity:1", "opacity:1")
    show(".t1", .05, .4, "opacity:0,y:18")
    show(".t2", .35, .45, "opacity:0,scale:.9", "opacity:1,scale:1")
    show(".t3", .7, .4, "opacity:0,y:18")
    hide("#title", L[0] - .45, .4, "opacity:0,y:-30")
    # the tracker
    show("#hud", L[0] - .3, .4, "opacity:0,x:-30", "opacity:1,x:0")
    for k, (t0, place, day) in enumerate(HUD):
        setText(".h-place", place, t0); setText(".h-day", day, t0)
        if k:
            add(f'tl.fromTo("#hud",{{opacity:.15}},{{opacity:1,duration:.5,immediateRender:false}},{t0 + .02:.3f});')
    add(f'tl.fromTo("#hud .h-day",{{color:"#FFFDF6"}},{{color:"#E8473B",duration:.3,immediateRender:false}},{E[15] - .25:.3f});')
    hide("#hud", CU[4] - .1, .4, "opacity:0,x:-30")
    # the next day
    show("#stamp", E[1] + .25, .35, "opacity:0,y:-10")
    hide("#stamp", E[1] + 1.35, .3)
    # the end card: the title again, the question, the follow prompt
    show("#endc", CU[4] + .25, .6, "opacity:0", "opacity:1")
    show(".e1", CU[4] + .35, .5, "opacity:0,y:18")
    show(".e2", T["look"] - .1, .4, "opacity:0,y:14")
    show(".e3", T["follow"] - .1, .4, "opacity:0,y:14")


def captions():
    html = []
    for k, ln in enumerate(LINES):
        cid = f"c{k}"
        text = ln["text"]
        parts = [text] if len(text) < 52 else [p for p in re.split(r"(?<=[.?!,])\s+(?=[A-Z])", text) if p]
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        wi = 0
        nxt = LINES[k + 1]["start"] if k + 1 < len(LINES) else DUR
        for j, p in enumerate(parts):
            n = len(p.split())
            a0 = ws[min(wi, len(ws) - 1)]["s"] - .1
            z = ws[wi + n]["s"] - .1 if wi + n < len(ws) else min(ln["end"] + .35, nxt - .08)
            wi += n
            pid = f"{cid}_{j}"
            if k == len(LINES) - 1:          # the last line is on the end card already
                continue
            who = LINES[k]["speaker"]
            tag = "VOICE AT THE DOOR" if LINES[k]["take"] == "14" else NAMES[who]
            html.append(f'<div class="cap sp-{who}" id="{pid}"><span class="who">{tag}</span>{p}</div>')
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
#ui { z-index: 5; }
#title, #hud, #endc, .cap, #stamp { opacity: 0; }
.shadow { text-shadow: 0 3px 18px rgba(0,0,0,.55), 0 1px 3px rgba(0,0,0,.6); }
#title { position: absolute; left: 70px; right: 70px; top: 520px; text-align: center; color: #FFFDF6; font-family: "Garamond", serif; }
#title .t1, #title .t3 { display: block; font: 500 82px/1.1 "Garamond"; letter-spacing: -.5px; }
#title .t2 { display: block; font: 700 104px/1.12 "Garamond"; color: #F2C94C; }
#hud { position: absolute; left: 72px; top: 960px; color: #FFFDF6; }
#hud .h-place { display: block; font: 800 40px/1 "Manrope"; letter-spacing: 3px; }
#hud .lab { display: block; margin-top: 14px; font: 800 28px/1 "Manrope"; letter-spacing: 3px; color: rgba(255,253,246,.85); }
#hud .h-row { display: block; margin-top: 6px; font: 600 54px/1 "Garamond"; }
#hud .h-row small { font-size: 30px; color: rgba(255,253,246,.75); }
#hud .h-c { display: inline-block; color: #F2C94C; font-weight: 700; }
.cap { position: absolute; left: 80px; right: 80px; top: 1320px; text-align: center; color: #FFFDF6; font: italic 500 56px/1.2 "Garamond"; }
.cap .who { display: block; margin-bottom: 8px; font: 800 28px/1 "Manrope"; font-style: normal; letter-spacing: 4px; color: rgba(255,253,246,.8); }
.cap.sp-phone { color: #A8F0FF; } .cap.sp-phone .who { color: #7FE3FF; }
.cap.sp-jay .who { color: #F2C94C; } .cap.sp-driver .who, .cap.sp-dealer .who { color: #F2B98A; }
#stamp { position: absolute; left: 0; right: 0; top: 330px; text-align: center; color: #FFFDF6; font: italic 500 64px/1.1 "Garamond"; opacity: 0; }
#stamp b { display: block; margin-top: 10px; font: 800 30px/1 "Manrope"; letter-spacing: 6px; font-style: normal; color: #F2C94C; }
#endc { position: absolute; left: 70px; right: 70px; top: 560px; text-align: center; color: #FFFDF6; }
#endc .e1 { display: block; font: 500 76px/1.12 "Garamond"; }
#endc .e1 b { color: #F2C94C; font-weight: 700; }
#endc .e2 { display: block; margin-top: 46px; font: italic 500 64px/1.1 "Garamond"; color: #F2C94C; }
#endc .e3 { display: block; margin-top: 70px; font: 800 30px/1.4 "Manrope"; letter-spacing: 5px; }
#endc .e3 span { display: block; font: 800 40px/1.3 "Manrope"; letter-spacing: 2px; color: #FFFDF6; }
"""


def main():
    story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, **T}
    ui = ('<div id="title" class="shadow"><span class="t1">What if your phone</span><span class="t1">could see</span>'
          '<span class="t2">24 hours</span><span class="t3">into the future?</span></div>'
          '<div id="hud" class="shadow"><span class="h-place">NEW YORK</span><span class="lab">DAY</span>'
          '<span class="h-row"><span class="h-day">1</span> <small>/ 30</small></span></div>'
          '<div id="stamp" class="shadow">The next day<b>9:13 AM</b></div>'
          '<div id="endc" class="shadow"><span class="e1">What if your phone could see <b>24 hours</b> into the future?</span>'
          '<span class="e2">Would you look?</span>'
          '<span class="e3">FOLLOW FOR MORE WHAT-IFS<span>@nxtlvlsocial.ai</span></span></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Future 9x16</title>
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
    <script type="module" src="assets/js/future.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
