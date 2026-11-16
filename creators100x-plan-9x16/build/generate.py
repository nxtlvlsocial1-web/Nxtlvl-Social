"""Creators 100X "30 days in 1 prompt" reel: writes index.html. 1080x1920, 30 fps, about 50 s. Page: Creators 100X.

The 3D film (assets/js/plan.js, Three.js, drawn on hf-seek) plays full frame: Jules, a fitness creator who hasn't posted
in two weeks, and Volt, the Creators 100X tile come to life as her AI sidekick, plan 30 days of content with one prompt in
three steps (the inputs, three pillars, the month) on a giant calendar wall, then the honest beat (batch-film the week in
one afternoon), the punchline and the end card. This file adds the HTML layer in the brand (brands/creators-100x/brand.md):
the hook line on frame 0, the step pill with a 3-part progress bar, captions a few words at a time (Jules in white boxes,
Volt in ink boxes with lime), the BATCH IT stamp, and the end card (logo, a comment box typing PLAN, the PDF cover,
"Follow for the next one").

python3 build/generate.py      (from the project root, after build/voice.py; build/audio.py writes the mix)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
CU = json.load(open(os.path.join(B, "cues.json")))
WORDS = json.load(open(os.path.join(B, "words.json")))
ENV = json.load(open(os.path.join(B, "env.json"))) if os.path.exists(os.path.join(B, "env.json")) else {}
LN, SPK = CU["lines"], CU["speaker"]
DUR = round(LN["15"][1] + 2.4, 2)
Ls = lambda k: LN[k][0]  # noqa: E731
Le = lambda k: LN[k][1]  # noqa: E731
A, HIDE, EV = [], [], []


def add(js):
    A.append("      " + js)


def wd(k, txt, end=False):
    for w in WORDS:
        if w["take"] == k and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(txt):
            return w["e" if end else "s"]
    raise SystemExit(f"no word {txt!r} in line {k}")


def ui():
    h = []
    # the hook line, on screen from frame 0
    h.append('<div class="hook" id="hook"><span>14 DAYS.</span><span><b>0</b> POSTS.</span></div>')
    add(f'tl.to("#hook",{{opacity:0,y:-20,duration:.25}},{Le("01") + .1:.3f});')
    add(f'tl.fromTo("#hook span:nth-child(2)",{{scale:1}},{{scale:1.06,duration:.4,yoyo:true,repeat:1,ease:"sine.inOut"}},.4);')
    # "30 days. 1 prompt." on Volt's question
    h.append('<div class="big" id="big30"><span><b>30</b> DAYS.</span><span>1 PROMPT.</span></div>')
    HIDE.append("#big30"); t30 = wd("02", "thirty")
    add(f'tl.fromTo("#big30",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.4)"}},{t30 - .05:.3f});')
    add(f'tl.to("#big30",{{opacity:0,duration:.2}},{Le("02") + .3:.3f});')
    EV.append([round(t30 - .05, 3), "pop"])
    # the step pill and its progress bar
    steps = [("04", "STEP 1/3", "YOUR INPUTS"), ("06", "STEP 2/3", "3 PILLARS"), ("09", "STEP 3/3", "30 DAYS")]
    h.append('<div class="step" id="step"><b id="stepn">STEP 1/3</b><span id="stept">YOUR INPUTS</span><div class="bar"><i id="sb0"></i><i id="sb1"></i><i id="sb2"></i></div></div>')
    HIDE.append("#step")
    add(f'tl.fromTo("#step",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{Ls("04") - .1:.3f});')
    for i, (k, n, s) in enumerate(steps):
        t = Ls(k) - .1
        add(f'tl.set("#stepn",{{textContent:"{n}"}},{t:.3f}); tl.set("#stept",{{textContent:"{s}"}},{t:.3f});')
        add(f'tl.fromTo("#sb{i}",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power2.out"}},{t:.3f});')
        add(f'tl.fromTo("#step",{{scale:1.12}},{{scale:1,duration:.3,ease:"back.out(2)"}},{t:.3f});')
        EV.append([round(t, 3), "step"])
    add(f'tl.to("#step",{{opacity:0,duration:.2}},{Le("10") + .2:.3f});')
    # the honest beat: BATCH IT
    h.append('<div class="stamp" id="stamp">BATCH IT</div>')
    HIDE.append("#stamp"); ta = wd("11", "afternoon")
    add(f'tl.fromTo("#stamp",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-8,duration:.2,ease:"power4.in"}},{ta + .05:.3f});')
    add(f'tl.to("#stamp",{{opacity:0,duration:.2}},{Le("11") + .5:.3f});')
    EV.append([round(ta + .25, 3), "stamp"])
    # the end card
    h.append('<div id="endc"><img class="logo" src="assets/img/logo.png" alt="Creators 100X"/>'
             '<div class="cbox"><div class="av"></div><div class="ty"><b id="typed">' + "".join(f"<s>{c}</s>" for c in "PLAN") + '</b><i class="cur"></i></div><div class="post" id="postb">Post</div></div>'
             '<div class="pdf"><img src="assets/img/pdf_cover.png" alt="The 30-day content plan prompt"/></div>'
             '<div class="fol">Follow for the next one</div></div>')
    te = Ls("15") - .2
    HIDE.extend(["#endc .logo", "#endc .cbox", "#endc .pdf", "#endc .fol", "#typed s"])
    add(f'tl.fromTo("#endc .logo",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,ease:"back.out(2)"}},{te:.3f});')
    add(f'tl.fromTo("#endc .cbox",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{te + .1:.3f});')
    tp = wd("15", "plan")
    add(f'tl.to("#typed s",{{opacity:1,duration:.01,stagger:.09}},{tp - .1:.3f});')
    add(f'tl.to("#postb",{{scale:1.08,background:"#FD0B68",duration:.15}},{tp + .4:.3f});')
    add(f'tl.fromTo("#endc .pdf",{{opacity:0,y:60,rotation:6}},{{opacity:1,y:0,rotation:-4,duration:.45,ease:"back.out(1.8)"}},{tp + .3:.3f});')
    add(f'tl.fromTo("#endc .fol",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{Le("15") + .2:.3f});')
    EV.extend([[round(tp - .1, 3), "typing"], [round(tp + .4, 3), "click"], [round(tp + .3, 3), "whoosh"]])
    return "".join(h)


def captions():
    html, allch = [], []
    for k, (a, z) in LN.items():
        if k == "15":          # the end card's comment box says it
            continue
        ws = [w for w in WORDS if w["take"] == k]
        chunks, cur = [], []
        for w in ws:
            cur.append(w)
            if len(" ".join(x["w"] for x in cur)) > 15 or re.search(r"[.!?,:]$", w["w"]) and len(cur) > 1:
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        for j, ch in enumerate(chunks):
            allch.append((k, j, ch, z))
    for n, (k, j, ch, z) in enumerate(allch):
        nxt = allch[n + 1][2][0]["s"] if n + 1 < len(allch) else DUR
        last = n + 1 < len(allch) and allch[n + 1][0] == k
        t1 = min(nxt - .07, (nxt - .07) if last else z + .2)
        pid = f"c{k}_{j}"
        spans = "".join(f'<span id="{pid}w{i}">{x["w"]} </span>' for i, x in enumerate(ch))
        html.append(f'<div class="cap {SPK[k]}" id="{pid}" style="top:1300px">{spans}</div>')
        add(f'tl.fromTo("#{pid}",{{opacity:0,y:18,scale:.94}},{{opacity:1,y:0,scale:1,duration:.12,ease:"back.out(2)"}},{max(ch[0]["s"] - .04, 0):.3f});')
        for i, x in enumerate(ch):
            add(f'tl.fromTo("#{pid}w{i}",{{opacity:.35}},{{opacity:1,duration:.08}},{x["s"] - .02:.3f});')
        add(f'tl.set("#{pid}",{{opacity:0}},{t1:.3f});')
        HIDE.append(f"#{pid}")
    return "".join(html)


CSS = """
@font-face { font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2") format("woff2"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #FDF4F4; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #FDF4F4; font-family: "Inter", sans-serif; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.hook { position: absolute; left: 70px; top: 290px; display: flex; flex-direction: column; gap: 6px; }
.hook span { display: inline-block; align-self: flex-start; font: 800 104px/1 "Inter"; letter-spacing: -4px; color: #101111; background: #FFFFFF; padding: 12px 26px 18px; border-radius: 22px; box-shadow: 0 14px 40px rgba(16,17,17,.18); transform-origin: 0 50%; }
.hook b { color: #FD0B68; }
.big { position: absolute; left: 0; right: 0; top: 300px; display: flex; flex-direction: column; align-items: center; gap: 8px; }
.big span { font: 800 110px/1 "Inter"; letter-spacing: -4px; color: #CCFB79; background: #101111; padding: 14px 30px 20px; border-radius: 24px; box-shadow: 0 16px 40px rgba(16,17,17,.3); }
.big b { color: #FD0B68; }
.step { position: absolute; left: 50%; top: 280px; width: 560px; margin-left: -280px; padding: 18px 28px 20px; border-radius: 28px; background: #101111; box-shadow: 0 14px 40px rgba(16,17,17,.3); display: flex; flex-wrap: wrap; align-items: center; gap: 16px; transform-origin: 50% 50%; }
.step b { font: 800 34px/1 "Inter"; color: #CCFB79; letter-spacing: 1px; } .step span { font: 800 34px/1 "Inter"; color: #FFFFFF; letter-spacing: 1px; }
.step .bar { width: 100%; display: flex; gap: 10px; } .step .bar i { flex: 1; height: 10px; border-radius: 6px; background: #CCFB79; transform-origin: 0 50%; transform: scaleX(0); }
.stamp { position: absolute; left: 50%; top: 240px; width: 600px; margin-left: -300px; text-align: center; font: 800 120px/1 "Inter"; letter-spacing: -3px; color: #FD0B68; border: 12px solid #FD0B68; border-radius: 30px; padding: 22px 0 30px; background: rgba(253,244,244,.92); box-shadow: 0 0 40px rgba(253,11,104,.35); }
.cap { position: absolute; left: 70px; right: 70px; text-align: center; font: 800 62px/1.18 "Inter"; letter-spacing: -1.5px; }
.cap span { display: inline-block; white-space: pre; padding: 6px 4px 10px; }
.cap.jules span { color: #101111; background: #FFFFFF; } .cap.jules span:first-child { border-radius: 16px 0 0 16px; padding-left: 18px; } .cap.jules span:last-child { border-radius: 0 16px 16px 0; padding-right: 14px; }
.cap.volt span { color: #CCFB79; background: #101111; } .cap.volt span:first-child { border-radius: 16px 0 0 16px; padding-left: 18px; } .cap.volt span:last-child { border-radius: 0 16px 16px 0; padding-right: 14px; }
.cap { filter: drop-shadow(0 10px 24px rgba(16,17,17,.22)); }
#endc { position: absolute; inset: 0; }
#endc .logo { position: absolute; left: 50%; top: 200px; width: 460px; margin-left: -230px; filter: drop-shadow(0 8px 30px rgba(16,17,17,.18)); }
#endc .cbox { position: absolute; left: 100px; right: 100px; top: 400px; display: flex; align-items: center; gap: 18px; padding: 18px 22px; border-radius: 28px; background: #FFFFFF; box-shadow: 0 16px 40px rgba(16,17,17,.22); }
#endc .av { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #CCFB79, #FD0B68); flex: none; }
#endc .ty { flex: 1; display: flex; align-items: center; } #endc .ty b { font: 800 54px/1 "Inter"; color: #101111; letter-spacing: 2px; } #endc .ty s { text-decoration: none; }
#endc .cur { display: inline-block; width: 5px; height: 54px; background: #FD0B68; margin-left: 6px; }
#endc .post { font: 800 36px/1 "Inter"; color: #fff; background: #101111; padding: 16px 26px; border-radius: 18px; }
#endc .pdf { position: absolute; right: 80px; top: 545px; width: 230px; } #endc .pdf img { width: 230px; border-radius: 18px; box-shadow: 0 20px 50px rgba(16,17,17,.3); }
#endc .fol { position: absolute; left: 90px; top: 575px; font: 800 44px/1.15 "Inter"; color: #101111; background: #CCFB79; padding: 16px 24px 20px; border-radius: 20px; max-width: 600px; white-space: nowrap; }
"""


def main():
    h = ui()
    caps = captions()
    add("gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ",{opacity:0});")
    A.insert(0, A.pop())
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"lines": LN, "speaker": SPK, "end": DUR, "words": WORDS, "julesEnv": ENV.get("jules", []), "voltEnv": ENV.get("volt", []), "l": [], "e": [], "cuts": []}
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creators 100X plan 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-hold data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>{h}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4">{caps}</div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.CT = {json.dumps(ct)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true, defaults: {{ immediateRender: false }} }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/plan.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"ev": sorted(EV), "end": DUR}, open(os.path.join(B, "ev.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
