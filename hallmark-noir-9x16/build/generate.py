"""The Hallmark noir: writes index.html and build/cues.json. 1080x1920, 30 fps, NXTLVLSOCIAL.AI.

python3 build/generate.py      (from the project root, after build/voice.py)

The film is all 3D (assets/js/world.js, Three.js, rendered on hf-seek). This file times it to the voiceover: every cue
(she walks in, the loupe finds each giveaway, the call, the deal, the book, the new page, the stamp) is a word time from
build/words.json, the 14 cuts sit just before the words they belong to, and the lightning lands on cuts. The only 2D
here is what social video needs on top: word-by-word captions with the spoken word in lavender, and the CTA. Every
sound-worthy event goes to cues.json["ev"] for build/audio.py.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
VOICE_END = LINES[-1]["end"]
DUR = round(VOICE_END + 2.0, 2)
WHITE, LAV, VIOLET = "#F4F1EA", "#B687F9", "#A75BFC"


def word(li, text, nth=1):
    hits = [w for w in WORDS if w["line"] == li + 1 and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not in line {li + 1}")
    return hits[nth - 1]["s"]


r3 = lambda x: round(x, 3)  # noqa: E731
T = {
    "end": DUR,
    "enter": word(0, "she"), "arrive": r3(word(0, "website") + .5), "place": r3(word(0, "website") + .65),
    "fine": word(1, "fine"), "two": word(2, "two"), "reviews": word(2, "reviews"), "labels": word(2, "labels"),
    "culprit": word(3, "culprit"), "defaults": word(3, "defaults"),
    "called": word(4, "called"), "hallmark": word(4, "hallmark"),
    "deals": word(5, "deals"), "checks": word(5, "checks"), "every": word(5, "every"),
    "same": word(6, "same"), "same2": word(6, "same", 2),
    "no": word(7, "no"), "designed": word(7, "designed"),
    "comment": word(8, "comment"), "closed": word(8, "closed"),
}
CUT = [0,
       word(0, "she") - .15,          # 1  the door: she walks in
       word(1, "it") - .1,            # 2  over his shoulder: the site
       word(1, "that") - .1,          # 3  his face in the screen glow
       word(1, "it", 2) - .1,         # 4  the corkboard: every other one in town
       word(2, "two") - .45,          # 5  the evidence, through the glass
       word(3, "claude") - .3,        # 6  the culprit
       word(4, "so") - .15,           # 7  the call
       word(4, "hallmark") - .3,      # 8  the card
       word(5, "it") - .2,            # 9  the deal and the book
       word(6, "same") - .35,         # 10 same prompt: his hands on the keys
       word(7, "no") - .15,           # 11 the new page, in colour
       word(7, "this") - .2,          # 12 the two of them
       word(8, "comment") - .25,      # 13 the stamp
       word(8, "closed") + .9]        # 14 case closed, the neon
T["cut"] = [r3(c) for c in CUT]
T["lightning"] = [[.25, 1], [.55, .6], [T["cut"][4] + .05, .7], [T["cut"][6] + .05, .8], [T["cut"][10] + .1, .45], [T["cut"][14] + .1, .6]]
T["lightning"] = [[r3(a), k] for a, k in T["lightning"]]
EV = []


def ev(t, kind):
    EV.append([r3(t), kind])


# sound events, from the same cues world.js uses
ev(T["enter"] - .55, "door"); ev(T["arrive"] + .95, "doorclose")
for i in range(5):
    ev(T["enter"] + .1 + i * .45, "step")
ev(T["place"] + .55, "laptop"); ev(T["place"] + .9, "chime")
for k in ("two", "reviews", "labels"):
    ev(T[k] - .25, "loupe"); ev(T[k] + .5, "marker")
ev(T["culprit"] - .15, "brim")
ev(T["called"] - .4, "handset")
for i in range(3):
    ev(T["called"] + .15 + i * .42, "dial")
ev(T["hallmark"] - .25, "card")
for i in range(5):
    ev(T["deals"] - .1 + i * .2, "deal")
ev(T["checks"], "book")
for i in range(6):
    ev(T["every"] - .35 + i * .26, "tick")
for i in range(18):
    ev(T["same"] - .05 + i * .07, "key")
ev(T["no"] - .1, "reveal"); ev(T["designed"], "warm")
ev(T["comment"] - .2, "lift"); ev(T["closed"], "stamp")
for c in T["cut"][1:]:
    ev(c, "cut")


A, HIDE = [], []


def add(js):
    A.append("      " + js)


def captions():
    html, chunks = [], []
    for li in range(len(LINES)):
        ws = [w for w in WORDS if w["line"] == li + 1]
        cur = []
        for w in ws:
            cur.append(w)
            if len(cur) >= 4 or re.search(r"[.,?!:]$", w["w"]):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
    for ci, ch in enumerate(chunks):
        spans = " ".join(f'<span class="cw" id="w{ci}_{k}">{w["w"]}</span>' for k, w in enumerate(ch))
        html.append(f'<div class="cap" id="cap{ci}"><span class="box">{spans}</span></div>')
        a = ch[0]["s"] - .06
        z = chunks[ci + 1][0]["s"] - .06 if ci + 1 < len(chunks) else DUR
        z = min(z, ch[-1]["e"] + .9)
        add(f'tl.fromTo("#cap{ci}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.14,ease:"power2.out",immediateRender:false}},{a:.3f});')
        add(f'tl.set("#cap{ci}",{{opacity:0}},{z:.3f});')
        for k, w in enumerate(ch):
            end = ch[k + 1]["s"] if k + 1 < len(ch) else min(z, w["e"] + .25)
            add(f'tl.set("#w{ci}_{k}",{{color:"{LAV}",textShadow:"0 0 22px rgba(167,91,252,.75), 0 3px 14px rgba(0,0,0,.8)"}},{w["s"] - .02:.3f});'
                f'tl.set("#w{ci}_{k}",{{color:"{WHITE}",textShadow:"0 3px 14px rgba(0,0,0,.8)"}},{end - .02:.3f});')
    return "".join(html)


def cta():
    a = T["comment"] - .1
    HIDE.extend(["#cta .cc", "#cta .cw2", "#cta .cs", "#cta .handle"])
    add(f'tl.fromTo("#cta .cc",{{opacity:0,y:-24}},{{opacity:1,y:0,duration:.35,ease:"power3.out",immediateRender:false}},{a:.3f});')
    add(f'tl.fromTo("#cta .cw2",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.45,ease:"power4.out",immediateRender:false}},{T["comment"] + .35:.3f});')
    add(f'tl.fromTo("#cta .cs",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.4,ease:"power2.out",immediateRender:false}},{T["comment"] + .9:.3f});')
    add(f'tl.fromTo("#cta .handle",{{opacity:0}},{{opacity:1,duration:.5,ease:"power2.out",immediateRender:false}},{T["cut"][14]:.3f});')
    ev(T["comment"] + .35, "slam")


CSS = f"""
@font-face {{ font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: "ISerif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 400; src: url("assets/fonts/JetBrainsMono-Regular.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #050608; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #050608; font-family: "Montserrat", sans-serif; color: {WHITE}; }}
.clip {{ position: absolute; inset: 0; }}
#gl {{ width: 1080px; height: 1920px; display: block; }}
.cap {{ position: absolute; left: 70px; right: 70px; top: 1350px; text-align: center; opacity: 0; font: 700 58px/1.22 "Montserrat"; letter-spacing: -.5px; color: {WHITE};
  text-shadow: 0 3px 14px rgba(0,0,0,.8); }}
.cw {{ display: inline-block; }}
.box {{ display: inline; padding: 4px 18px 8px; border-radius: 16px; background: rgba(6,6,8,.66); -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
#cta {{ text-align: center; }}
#cta .cc {{ position: absolute; left: 0; right: 0; top: 330px; margin: 0 auto; width: fit-content; padding: 12px 34px; border: 3px solid {WHITE}; border-radius: 40px;
  font: 700 34px "JBMono"; letter-spacing: 10px; background: rgba(5,6,8,.55); }}
#cta .cw2 {{ position: absolute; left: 0; right: 0; top: 410px; font: 800 150px/1 "Montserrat"; letter-spacing: 6px; color: #fff;
  text-shadow: 0 0 30px rgba(167,91,252,.95), 0 0 80px rgba(167,91,252,.6), 0 6px 20px rgba(0,0,0,.8); }}
#cta .cs {{ position: absolute; left: 0; right: 0; top: 590px; font: 400 64px "ISerif"; font-style: italic; color: {WHITE}; text-shadow: 0 3px 14px rgba(0,0,0,.9); }}
#cta .handle {{ position: absolute; left: 0; right: 0; top: 1520px; font: 700 30px "JBMono"; letter-spacing: 8px; color: {LAV}; text-shadow: 0 0 16px rgba(167,91,252,.7); }}
"""


def main():
    caps = captions()
    cta()
    A.insert(0, "      gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ",{opacity:0});")
    has_mix = os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav"))
    has_vo = os.path.exists(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    audio = (f'<audio id="mix" src="assets/audio/{"mix" if has_mix else "voice"}.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>'
             if has_mix or has_vo else "")
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Hallmark noir 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="cta" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5" data-layout-ignore><div class="cc">COMMENT</div><div class="cw2">HALLMARK</div><div class="cs">and I'll send you the install.</div><div class="handle">NXTLVLSOCIAL.AI</div></div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{caps}</div>
      {audio}
    </div>
    <script>
      window.NOIR_T = {json.dumps(T)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/world.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    T["ev"] = sorted(EV)
    json.dump(T, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, {len(EV)} sound events, audio: {'mix' if has_mix else 'voice' if has_vo else 'none'}")
    print("cuts", T["cut"])


if __name__ == "__main__":
    main()
