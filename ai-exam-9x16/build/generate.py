"""AI Exam reel ("My exam is Monday. I have 300 pages of notes."): writes index.html. 1080x1920, 30 fps, about 48 s.
Account: @nxtlvlsocial.ai. A two-character skit: YOU (the student) and HOOT (an AI study owl). Every step is a real,
free tool: NotebookLM (Google) turns notes into an Audio Overview (a podcast-style summary), flashcards and quizzes.
Keyword CTA: comment EXAM for the setup guide, plus a share prompt.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D (assets/js/exam.js) is a soft low-poly, flat-shaded world in the style of the owner's reference: a dusk study
desk by a city window, a night bus, an exam hall. This file writes the HTML layer: dialogue captions in dark pills
with a speaker tag, the STEP cards in the card band (y 430-860), a top bar, and the share + comment end card.
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
SCENE_STARTS = [6, 7, 9, 10, 14, 17, 18]          # the lines that open a new scene
T = {
    "monday": word(1, "monday"), "and3": word(3, "and"), "three": word(3, "three"), "pages": word(3, "pages"), "notes": word(3, "notes"), "give": word(4, "give"), "all": word(5, "all"),
    "step1": word(6, "step"), "notebooklm": word(6, "notebooklm"), "free": word(6, "free"), "drop": word(6, "drop"), "everything": word(6, "everything"),
    "step2": word(7, "step"), "podcast": word(7, "podcast"), "podcast8": word(8, "podcast"), "twenty": word(9, "twenty"), "bus": word(9, "bus"),
    "step3": word(10, "step"), "flashcards": word(10, "flashcards"), "test": word(10, "test"), "sixty": word(11, "sixty"),
    "step4": word(12, "step"), "weak": word(12, "weak"), "seven": word(12, "seven"), "ninety": word(13, "ninety"), "ninety2": word(13, "ninety", 2),
    "last": word(14, "last"), "small": word(14, "small"), "bag": word(14, "bag"), "take": word(14, "take"), "no": word(15, "no"), "please": word(16, "please"),
    "need": word(17, "need"), "every": word(17, "every"), "answer": word(17, "answer"),
    "send": word(18, "send"), "friend": word(18, "friend"), "follow": word(18, "follow"), "commentk": word(18, "comment"), "examk": word(18, "exam", 2), "setup": word(18, "setup"),
    "end": DUR,
}
T["cuts"] = [round(L[k - 1] - .12, 3) for k in SCENE_STARTS]
T["lines"] = [{"s": ln["start"], "e": ln["end"], "who": ln["speaker"]} for ln in LINES]
T["focus"] = [
    {"who": "you", "a": 0.0, "b": round(E[0] + .1, 3)},
    {"who": "owl", "a": round(L[1] - .1, 3), "b": round(E[1] + .15, 3)},
    {"who": "owl", "a": round(L[3] - .1, 3), "b": round(E[3] + .15, 3)},
    {"who": "you", "a": round(L[7] - .1, 3), "b": round(E[7] + .15, 3)},
    {"who": "you", "a": round(L[10] - .1, 3), "b": round(E[10] + .1, 3)},
    {"who": "owl", "a": round(L[14] - .1, 3), "b": round(E[14] + .2, 3)},
]
F = T["focus"]
TAGS = [("tg-you", .35, F[0]["b"] - .15, "YOU", "exam on Monday"),
        ("tg-owl", F[1]["a"] + .15, F[1]["b"] - .1, "HOOT", "your AI study buddy")]
A = []


def add(js):
    A.append("      " + js)


def pop(sel, t, frm="scale:.6,opacity:0", d=.3, ease="back.out(2.2)", to="scale:1,opacity:1,x:0,y:0,rotation:0"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def out(sel, t, d=.22, props="opacity:0,y:-24"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.in"}},{t:.3f});')


def count(sel, t, a, b, d, fmt="Math.round(o.v)", ease="power2.out"):
    add('(()=>{const o={v:%s};tl.to(o,{v:%s,duration:%.3f,ease:"%s",onUpdate:()=>{document.querySelectorAll("%s").forEach(e=>e.textContent=%s)}},%.3f);})();'
        % (a, b, d, ease, sel, fmt, t))


def steps(n):
    return '<span class="steps">' + "".join(f'<i class="{"on" if k < n else ""}"></i>' for k in range(4)) + '</span>'


SOURCES = [("Lecture notes.pdf", "120 pages"), ("Slides, weeks 1-12.pdf", "96 pages"), ("Photos of my notebook", "84 pages")]
CARDS = (
    '<div class="card c-notes"><span class="mono lab">THE SITUATION</span>'
    '<div class="srow"><span>Exam</span><b class="coral">Monday</b></div><div class="srow"><span>Notes</span><b><i class="pg">0</i> pages</b></div></div>'
    f'<div class="card step c-s1">{steps(1)}<span class="mono lab">STEP 1/4</span><b class="sh">Upload your notes</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">NotebookLM &middot; Sources</span></div>'
    + "".join(f'<div class="src s{k}"><span class="doc"></span><span class="sn">{n}</span><span class="sp mono">{p}</span><b class="ok">&#10003;</b></div>' for k, (n, p) in enumerate(SOURCES))
    + '<div class="tot mono"><span>Added</span><b><i class="tp">0</i> pages</b></div></div></div>'
    f'<div class="card step c-s2">{steps(2)}<span class="mono lab">STEP 2/4</span><b class="sh">Turn them into a podcast</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">Audio Overview</span></div>'
    '<div class="player"><span class="play"></span><em class="wave">' + "".join(f'<i class="wv wv{k}"></i>' for k in range(28)) + '</em></div>'
    '<div class="tot mono"><span>Deep dive</span><b>20 min</b></div></div></div>'
    f'<div class="card step c-s3">{steps(3)}<span class="mono lab">STEP 3/4</span><b class="sh">Flashcards + a practice test</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">Study tools</span></div>'
    '<div class="tot mono"><span>Flashcards</span><b><i class="fc">0</i></b></div><div class="tot mono"><span>Practice test</span><b class="red"><i class="sc">0</i>%</b></div></div></div>'
    f'<div class="card step c-s4">{steps(4)}<span class="mono lab">STEP 4/4</span><b class="sh">Fix your weak spots</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">Practice test &middot; retake</span></div>'
    '<div class="tot mono"><span>Weakest</span><b class="red">Chapter 7</b></div><div class="tot mono"><span>Score</span><b class="green"><i class="sc2">62</i>%</b></div></div></div>'
)
CARDS += "".join(f'<div class="ptag {c}"><span class="mono">{a}</span><b>{b}</b></div>' for c, _, _, a, b in TAGS)


def story():
    pop(".c-notes", T["and3"] - .1, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".pg", T["three"] if "three" in T else T["and3"] + .2, 0, 300, .8, "Math.round(o.v)", "power2.out")
    out(".c-notes", E[4] + .1)
    pop(".c-s1", T["step1"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    for k in range(3):
        pop(f".s{k}", T["drop"] - .1 + k * .25, "x:-30,opacity:0", .25, "back.out(2)")
    count(".tp", T["drop"], 0, 300, 1.0, "Math.round(o.v)", "power2.out")
    out(".c-s1", E[5] + .1)
    pop(".c-s2", T["step2"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    for k in range(28):
        add(f'tl.fromTo(".wv{k}",{{scaleY:.2}},{{scaleY:{.3 + .7 * abs(((k * 7) % 11) / 10 - .4):.2f},duration:.12,yoyo:true,repeat:{int((E[8] - T["podcast"]) / .12)},ease:"sine.inOut",immediateRender:false}},{T["podcast"] + k * .01:.3f});')
    out(".c-s2", E[8] + .1)
    pop(".c-s3", T["step3"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".fc", T["flashcards"], 0, 50, .7, "Math.round(o.v)", "power2.out")
    count(".sc", T["sixty"] - .1, 0, 62, .7, "Math.round(o.v)", "power2.out")
    out(".c-s3", L[11] - .25)
    pop(".c-s4", T["step4"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".sc2", T["ninety"] - .1, 62, 91, .6, "Math.round(o.v)", "power3.out")
    add(f'tl.fromTo(".c-s4 .green",{{scale:1.4}},{{scale:1,duration:.35,ease:"back.out(3)",immediateRender:false}},{T["ninety"] + .5:.3f});')
    out(".c-s4", E[12] + .15)
    for c, a, b, _, _ in TAGS:
        pop(f".{c}", a, "y:24,opacity:0", .25, "back.out(2)")
        out(f".{c}", b, .18)
    # the end card: share it, comment EXAM, follow
    pop("#endc", T["send"] - .3, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-box", T["follow"] - .2, "y:20,opacity:0", .3, "back.out(2)")
    for k, ch in enumerate("EXAM"):
        add(f'tl.set(".ec-typed",{{textContent:"{"EXAM"[:k + 1]}"}},{T["commentk"] + .15 + k * .12:.3f});')
    add(f'tl.fromTo(".ec-heart",{{scale:1}},{{scale:1.5,duration:.15,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{T["examk"] + .3:.3f});')
    add(f'tl.set(".ec-heart",{{color:"#E8735A"}},{T["examk"] + .3:.3f});')
    pop(".ec-2", T["setup"] - .3, "y:20,opacity:0", .3)
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')


def captions():
    html = []
    for k, ln in enumerate(LINES):
        cid = f"c{k}"
        spk = "YOU" if ln["speaker"] == "you" else "HOOT"
        text = ln["text"]
        # long CTA line: split into its phrases so each fits in one pill
        parts = [text] if len(text) < 60 else [p for p in re.split(r"(?<=[.?!])\s+", text) if p]
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        wi = 0
        nxt = LINES[k + 1]["start"] if k + 1 < len(LINES) else DUR
        for j, p in enumerate(parts):
            n = len(p.split())
            a0 = ws[wi]["s"] - .08
            z = ws[wi + n]["s"] - .08 if wi + n < len(ws) else min(ln["end"] + .25, nxt - .05)
            wi += n
            pid = f"{cid}_{j}"
            html.append(f'<div class="cap {ln["speaker"]}" id="{pid}"><span class="who mono">{spk}</span><span class="txt">{p}</span></div>')
            add(f'tl.fromTo("#{pid}",{{opacity:0,y:12,scale:.96}},{{opacity:1,y:0,scale:1,duration:.14,ease:"power2.out",immediateRender:false}},{a0:.3f});')
            add(f'tl.set("#{pid}",{{opacity:0}},{z:.3f});')
    return "".join(html)


CSS = """
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "Serif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #2B2440; }
body { font-family: "Manrope", sans-serif; color: #1E1B18; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #2B2440; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
#ui { z-index: 5; }
.top { position: absolute; left: 50px; right: 50px; top: 150px; height: 64px; display: flex; justify-content: space-between; align-items: center;
  padding: 0 24px; border-radius: 32px; background: rgba(255,253,248,.92); border: 3px solid #1E1B18; }
.brand { font-size: 22px; letter-spacing: 3px; display: flex; align-items: center; gap: 12px; }
.brand b { width: 14px; height: 14px; border-radius: 50%; background: #E8735A; }
.live { font-size: 20px; letter-spacing: 2px; color: #6B5BD6; }
.prog { width: 110px; height: 18px; border-radius: 9px; border: 3px solid #1E1B18; overflow: hidden; }
.prog i { display: block; height: 100%; background: #6B5BD6; transform-origin: 0 50%; transform: scaleX(0); }
.card, #endc, .ec-box, .ec-2, .ptag { opacity: 0; }
.card { position: absolute; left: 0; right: 0; margin: 0 auto; width: 820px; top: 430px; padding: 24px 30px 26px;
  border-radius: 28px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; }
.card .lab { display: block; font-size: 22px; letter-spacing: 4px; color: #6B5BD6; }
.card .sh { display: block; font: 800 50px/1.08 "Manrope"; letter-spacing: -1.5px; margin: 2px 0 14px; }
.steps { display: flex; gap: 8px; margin-bottom: 14px; } .steps i { flex: 1; height: 8px; border-radius: 4px; background: #E4D9C7; } .steps i.on { background: #6B5BD6; }
.app { border: 2px solid #1E1B18; border-radius: 18px; overflow: hidden; background: #F7F3FF; }
.ab { display: flex; align-items: center; gap: 8px; padding: 10px 16px; background: #EDE7FB; border-bottom: 2px solid #1E1B18; }
.ab i { width: 13px; height: 13px; border-radius: 50%; background: #E8735A; } .ab i:nth-child(2) { background: #F2B33D; } .ab i:nth-child(3) { background: #3FA372; }
.ab span { margin-left: 10px; font-size: 20px; letter-spacing: 1px; color: #3a3530; }
.src { display: flex; align-items: center; gap: 14px; padding: 12px 18px; border-bottom: 1px solid #DCD3EE; font: 700 30px "Manrope"; opacity: 0; }
.src .doc { width: 26px; height: 32px; border-radius: 4px; background: #6B5BD6; }
.src .sn { flex: 1; } .src .sp { font-size: 22px; color: #5b5650; } .src .ok { color: #3FA372; font-size: 30px; }
.tot { display: flex; justify-content: space-between; align-items: baseline; padding: 14px 18px; font-size: 24px; letter-spacing: 1px; color: #3a3530; }
.tot b { font: 800 46px "Manrope"; letter-spacing: -1px; color: #1E1B18; } .tot b i { font-style: normal; }
.tot b.red { color: #D9483B; } .tot b.green { color: #3FA372; display: inline-block; } .coral { color: #D45C40; }
.player { display: flex; align-items: center; gap: 18px; padding: 18px; }
.play { width: 0; height: 0; border-left: 34px solid #6B5BD6; border-top: 21px solid transparent; border-bottom: 21px solid transparent; }
.wave { display: flex; gap: 6px; align-items: center; height: 80px; }
.wv { display: block; width: 12px; height: 80px; border-radius: 6px; background: #6B5BD6; transform: scaleY(.2); }
.c-notes { width: 640px; } .srow { display: flex; justify-content: space-between; align-items: baseline; padding: 6px 0; font: 700 34px "Manrope"; color: #5b5650; }
.srow b { font: 800 56px "Manrope"; letter-spacing: -1.5px; color: #1E1B18; } .srow b i { font-style: normal; } .srow b.coral { color: #D45C40; }
.ptag { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1190px; padding: 12px 28px 14px; border-radius: 24px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 6px 7px 0 #1E1B18; text-align: center; }
.ptag span { display: block; font-size: 22px; letter-spacing: 5px; color: #6B5BD6; }
.ptag b { display: block; font: 800 36px/1.15 "Manrope"; letter-spacing: -1px; }
#caps { z-index: 6; }
.cap { position: absolute; left: 0; right: 0; top: 262px; display: flex; flex-direction: column; align-items: center; gap: 8px; opacity: 0; }
.cap .who { padding: 4px 14px; border-radius: 10px; font-size: 20px; letter-spacing: 3px; color: #fff; background: #E8735A; }
.cap.owl .who { background: #6B5BD6; }
.cap .txt { max-width: 900px; padding: 12px 28px 16px; border-radius: 22px; background: rgba(24,20,30,.82); color: #fff; text-align: center;
  font: 800 52px/1.18 "Manrope"; letter-spacing: -1px; }
#endc { position: absolute; left: 60px; right: 60px; top: 470px; padding: 44px 40px 40px; border-radius: 40px; text-align: center;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 12px 13px 0 #1E1B18; }
.ec-1 { font: 800 50px/1.1 "Manrope"; letter-spacing: -1.5px; }
.ec-1 em { display: block; font: italic 62px/1.1 "Serif"; color: #6B5BD6; margin-top: 6px; }
.ec-box { display: flex; align-items: center; gap: 18px; width: 640px; margin: 30px auto 14px; padding: 16px 24px; border-radius: 26px; border: 3px solid #1E1B18;
  background: #fff; text-align: left; box-shadow: 6px 7px 0 #1E1B18; }
.ec-box .av { width: 52px; height: 52px; border-radius: 50%; background: linear-gradient(135deg, #F2B33D, #E8735A); flex: none; }
.ec-box .fld { flex: 1; } .ec-box .fld span { display: block; font-size: 18px; letter-spacing: 1px; color: #8a847c; }
.ec-typed { font: 800 52px "Manrope"; letter-spacing: 2px; } .ec-typed::after { content: "|"; color: #6B5BD6; font-weight: 400; }
.ec-heart { font-size: 44px; color: #8a847c; display: inline-block; }
.ec-h { font-size: 30px; letter-spacing: 3px; margin-top: 14px; }
.ec-2 { font: italic 46px "Serif"; color: #D45C40; margin-top: 8px; }
"""


def main():
    story()
    caps = captions()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    ct = {"l": L, "e": E, **T}
    endc = ('<div id="endc"><div class="ec-1">Send this to a friend<em>with an exam this week</em></div>'
            '<div class="ec-box"><i class="av"></i><span class="fld"><span class="mono">you &middot; now</span><b class="ec-typed"></b></span><b class="ec-heart">&#9829;</b></div>'
            '<div class="ec-h mono">FOLLOW @NXTLVLSOCIAL.AI &middot; COMMENT EXAM</div>'
            '<div class="ec-2">I&rsquo;ll DM you the setup</div></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Exam 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b></b>NXTLVLSOCIAL.AI</span><span class="live mono">AI STUDY HACK</span><span class="prog"><i></i></span></div>
        {CARDS}{endc}
      </div>
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
    <script type="module" src="assets/js/exam.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
