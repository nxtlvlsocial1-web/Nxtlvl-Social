"""AI Posts reel ("LUMI. I haven't posted in three weeks."): writes index.html. 1080x1920, 30 fps, about 60 s.
Account: @nxtlvlsocial.ai. A two-character skit: YOU (a creator who stopped posting) and LUMI (our AI ring light). Every
step is a real, free workflow: a phone voice memo (iPhone Voice Memos and Pixel Recorder transcribe), a prompt in
ChatGPT (or Claude), hooks + captions + carousel slides, and scheduling in Meta Business Suite (free).
Keyword CTA: comment POSTS for the 30-day content prompt, plus a share prompt.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D (assets/js/posts.js) is the soft low-poly, flat-shaded world of the AI Exam reel: a creator's desk by a city
window at dusk, the same desk at night, and the next morning. This file writes the HTML layer: dialogue captions in
dark pills with a speaker tag, the STEP cards in the card band (y 430-860), a top bar, and the share + comment end card.
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
SCENE_STARTS = [6, 7, 9, 10, 12, 14, 17, 18]      # the lines that open a new scene
T = {
    "three": word(1, "three"), "weeks": word(1, "weeks"), "twenty": word(2, "twenty"), "counted": word(2, "counted"),
    "zero": word(3, "zero"), "ideas3": word(3, "ideas"), "talk": word(4, "talk"), "anything": word(4, "anything"), "morning": word(5, "morning"),
    "step1": word(6, "step"), "record": word(6, "record"), "memo": word(6, "memo"), "phone": word(6, "phone"), "text": word(6, "text"),
    "step2": word(7, "step"), "paste": word(7, "paste"), "prompt": word(7, "prompt"), "thirty7": word(7, "thirty"),
    "thirty8": word(8, "thirty"), "coffee": word(8, "coffee"), "rant": word(8, "rant"),
    "step3": word(9, "step"), "hook": word(9, "hook"), "caption": word(9, "caption"), "slides": word(9, "slides"),
    "step4": word(10, "step"), "schedule": word(10, "schedule"), "thirty10": word(10, "thirty"), "free": word(10, "free"),
    "month": word(11, "month"), "night": word(11, "night"),
    "wait": word(12, "wait"), "eighty": word(12, "eighty"), "views": word(12, "views"), "coffee12": word(12, "coffee"),
    "rant13": word(13, "rant"), "hook13": word(13, "hook"),
    "just": word(14, "just"), "forever": word(14, "forever"), "no": word(15, "no"), "why": word(16, "why"),
    "follow17": word(17, "follow"), "voice": word(17, "voice"), "content": word(17, "content"),
    "send": word(18, "send"), "creator": word(18, "creator"), "follow": word(18, "follow"), "commentk": word(18, "comment"), "postsk": word(18, "posts"), "promptk": word(18, "prompt"),
    "end": DUR,
}
T["cuts"] = [round(L[k - 1] - .12, 3) for k in SCENE_STARTS]
T["lines"] = [{"s": ln["start"], "e": ln["end"], "who": ln["speaker"]} for ln in LINES]
T["focus"] = [
    {"who": "you", "a": 0.0, "b": round(E[0] + .1, 3)},
    {"who": "lumi", "a": round(L[1] - .1, 3), "b": round(E[1] + .15, 3)},
    {"who": "lumi", "a": round(L[3] - .1, 3), "b": round(E[3] + .15, 3)},
    {"who": "you", "a": round(L[7] - .1, 3), "b": round(E[7] + .15, 3)},
    {"who": "you", "a": round(L[11] - .1, 3), "b": round(E[11] + .1, 3)},
    {"who": "lumi", "a": round(L[14] - .1, 3), "b": round(E[14] + .2, 3)},
]
F = T["focus"]
TAGS = [("tg-you", .35, F[0]["b"] - .15, "YOU", "last post: 23 days ago"),
        ("tg-lumi", F[1]["a"] + .15, F[1]["b"] - .1, "LUMI", "your AI content buddy")]
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


TRANSCRIPT = ["so every morning I make coffee first,", "before I even look at my phone,", "and honestly that one rule changed..."]
IDEAS = ["My 6 AM coffee rule", "Why I stopped checking my phone first", "The 2-minute morning reset"]
CARDS = (
    '<div class="card c-sit"><span class="mono lab">THE SITUATION</span>'
    '<div class="srow"><span>Last post</span><b class="coral"><i class="dd">0</i> days ago</b></div><div class="srow"><span>Ideas</span><b><i class="id0">0</i></b></div></div>'
    f'<div class="card step c-s1">{steps(1)}<span class="mono lab">STEP 1/4</span><b class="sh">Record a voice memo</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">Voice Memos &middot; Transcript</span></div>'
    '<div class="player"><span class="rec"></span><em class="wave">' + "".join(f'<i class="wv wv{k}"></i>' for k in range(26)) + '</em><b class="mono tm">2:00</b></div>'
    + "".join(f'<div class="ln l{k}">{x}</div>' for k, x in enumerate(TRANSCRIPT)) + '</div></div>'
    f'<div class="card step c-s2">{steps(2)}<span class="mono lab">STEP 2/4</span><b class="sh">30 post ideas</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">ChatGPT &middot; my prompt</span></div>'
    + "".join(f'<div class="src s{k}"><span class="num mono">{k + 1}</span><span class="sn">{n}</span></div>' for k, n in enumerate(IDEAS))
    + '<div class="tot mono"><span>Ideas</span><b><i class="ic">0</i></b></div></div></div>'
    f'<div class="card step c-s3">{steps(3)}<span class="mono lab">STEP 3/4</span><b class="sh">Hook, caption, slides</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">Post 1 of 30</span></div>'
    '<div class="tot mono r1"><span>Hook</span><b class="small">&ldquo;I drank coffee wrong for 10 years&rdquo;</b></div>'
    '<div class="tot mono r2"><span>Caption</span><b class="green">&#10003;</b></div><div class="tot mono r3"><span>Slides</span><b><i class="sl">0</i></b></div></div></div>'
    f'<div class="card step c-s4">{steps(4)}<span class="mono lab">STEP 4/4</span><b class="sh">Schedule all 30</b>'
    '<div class="app"><div class="ab"><i></i><i></i><i></i><span class="mono">Meta Business Suite &middot; Planner</span></div>'
    '<div class="tot mono"><span>Scheduled</span><b><i class="sc">0</i>/30</b></div><div class="tot mono"><span>Cost</span><b class="green">free</b></div></div></div>'
    '<div class="card c-stats"><span class="mono lab">THE NEXT MORNING</span>'
    '<div class="srow"><span>Coffee post</span><b class="coral"><i class="vw">0</i> views</b></div><div class="srow"><span>Likes</span><b><i class="lk">0</i></b></div></div>'
)
CARDS += "".join(f'<div class="ptag {c}"><span class="mono">{a}</span><b>{b}</b></div>' for c, _, _, a, b in TAGS)


def story():
    pop(".c-sit", T["three"] - .1, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".dd", T["three"], 0, 23, .8)
    add(f'tl.fromTo(".c-sit .coral",{{scale:1.25}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{T["counted"]:.3f});')
    out(".c-sit", E[4] + .1)
    pop(".c-s1", T["step1"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    for k in range(26):
        add(f'tl.fromTo(".wv{k}",{{scaleY:.2}},{{scaleY:{.3 + .7 * abs(((k * 7) % 11) / 10 - .4):.2f},duration:.12,yoyo:true,repeat:{max(1, int((E[5] - T["record"]) / .12))},ease:"sine.inOut",immediateRender:false}},{T["record"] + k * .01:.3f});')
    for k in range(3):
        pop(f".l{k}", T["phone"] - .2 + k * .35, "x:-24,opacity:0", .25, "power2.out")
    out(".c-s1", E[5] + .1)
    pop(".c-s2", T["step2"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    for k in range(3):
        pop(f".s{k}", T["thirty7"] - .1 + k * .2, "x:-30,opacity:0", .25, "back.out(2)")
    count(".ic", T["thirty7"] - .1, 0, 30, .9)
    add(f'tl.fromTo(".c-s2 .s0",{{backgroundColor:"rgba(232,115,90,0)"}},{{backgroundColor:"rgba(232,115,90,.22)",duration:.25,immediateRender:false}},{T["coffee"] - .1:.3f});')
    out(".c-s2", E[7] + .1)
    pop(".c-s3", T["step3"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    pop(".r1", T["hook"] - .1, "x:-24,opacity:0", .25, "power2.out")
    pop(".r2", T["caption"] - .1, "x:-24,opacity:0", .25, "power2.out")
    pop(".r3", T["slides"] - .1, "x:-24,opacity:0", .25, "power2.out")
    count(".sl", T["slides"], 0, 7, .5)
    out(".c-s3", E[8] + .1)
    pop(".c-s4", T["step4"] - .15, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".sc", T["schedule"], 0, 30, 1.4, "Math.round(o.v)", "power1.inOut")
    add(f'tl.fromTo(".c-s4 .green",{{scale:1.4}},{{scale:1,duration:.35,ease:"back.out(3)",immediateRender:false}},{T["free"]:.3f});')
    out(".c-s4", E[10] + .15)
    pop(".c-stats", T["wait"] - .1, "y:40,opacity:0", .3, "back.out(1.8)")
    count(".vw", T["eighty"] - .15, 0, 80000, 1.0, "Math.round(o.v).toLocaleString(\'en-US\')", "power3.out")
    count(".lk", T["eighty"], 0, 6200, 1.0, "Math.round(o.v).toLocaleString(\'en-US\')", "power3.out")
    out(".c-stats", E[12] + .15)
    for c, a, b, _, _ in TAGS:
        pop(f".{c}", a, "y:24,opacity:0", .25, "back.out(2)")
        out(f".{c}", b, .18)
    # the end card: share it, comment POSTS, follow
    pop("#endc", T["send"] - .3, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-box", T["follow"] - .2, "y:20,opacity:0", .3, "back.out(2)")
    for k in range(5):
        add(f'tl.set(".ec-typed",{{textContent:"{"POSTS"[:k + 1]}"}},{T["commentk"] + .15 + k * .1:.3f});')
    add(f'tl.fromTo(".ec-heart",{{scale:1}},{{scale:1.5,duration:.15,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{T["postsk"] + .3:.3f});')
    add(f'tl.set(".ec-heart",{{color:"#E8735A"}},{T["postsk"] + .3:.3f});')
    pop(".ec-2", T["promptk"] - .3, "y:20,opacity:0", .3)
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')


def captions():
    html = []
    for k, ln in enumerate(LINES):
        cid = f"c{k}"
        spk = "YOU" if ln["speaker"] == "you" else "LUMI"
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
.tot b.red { color: #D9483B; } .tot b.green { color: #2B8758; display: inline-block; } .coral { color: #D45C40; }
.player { display: flex; align-items: center; gap: 18px; padding: 18px; }
.rec { width: 34px; height: 34px; border-radius: 50%; background: #E8735A; flex: none; box-shadow: 0 0 0 6px rgba(232,115,90,.25); }
.tm { margin-left: auto; font-size: 26px; }
.ln { padding: 8px 18px; font: 600 28px/1.25 "Manrope"; color: #3a3530; opacity: 0; }
.src .num { width: 40px; height: 40px; border-radius: 50%; background: #6B5BD6; color: #fff; display: grid; place-items: center; font-size: 22px; flex: none; }
.tot b.small { font: 800 30px/1.2 "Manrope"; letter-spacing: -.5px; max-width: 520px; text-align: right; }
.r1, .r2, .r3 { opacity: 0; }
.wave { display: flex; gap: 6px; align-items: center; height: 70px; }
.wv { display: block; width: 10px; height: 70px; border-radius: 6px; background: #6B5BD6; transform: scaleY(.2); }
.c-sit, .c-stats { width: 680px; } .srow { display: flex; justify-content: space-between; align-items: baseline; padding: 6px 0; font: 700 34px "Manrope"; color: #5b5650; }
.srow b { font: 800 56px "Manrope"; letter-spacing: -1.5px; color: #1E1B18; } .srow b i { font-style: normal; } .srow b.coral { color: #D45C40; }
.ptag { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1190px; padding: 12px 28px 14px; border-radius: 24px;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 6px 7px 0 #1E1B18; text-align: center; }
.ptag.tg-lumi { top: 1560px; }
.ptag span { display: block; font-size: 22px; letter-spacing: 5px; color: #6B5BD6; }
.ptag b { display: block; font: 800 36px/1.15 "Manrope"; letter-spacing: -1px; }
#caps { z-index: 6; }
.cap { position: absolute; left: 0; right: 0; top: 262px; display: flex; flex-direction: column; align-items: center; gap: 8px; opacity: 0; }
.cap .who { padding: 4px 14px; border-radius: 10px; font-size: 20px; letter-spacing: 3px; color: #fff; background: #C9503A; }
.cap.lumi .who { background: #6B5BD6; }
.cap .txt { max-width: 900px; padding: 12px 28px 16px; border-radius: 22px; background: rgba(24,20,30,.82); color: #fff; text-align: center;
  font: 800 52px/1.18 "Manrope"; letter-spacing: -1px; }
#endc { position: absolute; left: 60px; right: 60px; top: 470px; padding: 44px 40px 40px; border-radius: 40px; text-align: center;
  background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 12px 13px 0 #1E1B18; }
.ec-1 { font: 800 50px/1.1 "Manrope"; letter-spacing: -1.5px; }
.ec-1 em { display: block; font: italic 62px/1.1 "Serif"; color: #6B5BD6; margin-top: 6px; }
.ec-box { display: flex; align-items: center; gap: 18px; width: 640px; margin: 30px auto 14px; padding: 16px 24px; border-radius: 26px; border: 3px solid #1E1B18;
  background: #fff; text-align: left; box-shadow: 6px 7px 0 #1E1B18; }
.ec-box .av { width: 52px; height: 52px; border-radius: 50%; background: linear-gradient(135deg, #F2B33D, #E8735A); flex: none; }
.ec-box .fld { flex: 1; } .ec-box .fld span { display: block; font-size: 18px; letter-spacing: 1px; color: #5f5a54; }
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
    endc = ('<div id="endc"><div class="ec-1">Send this to a creator<em>who hasn&rsquo;t posted in weeks</em></div>'
            '<div class="ec-box"><i class="av"></i><span class="fld"><span class="mono">you &middot; now</span><b class="ec-typed"></b></span><b class="ec-heart">&#9829;</b></div>'
            '<div class="ec-h mono">FOLLOW @NXTLVLSOCIAL.AI &middot; COMMENT POSTS</div>'
            '<div class="ec-2">I&rsquo;ll DM you the prompt</div></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Posts 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b></b>NXTLVLSOCIAL.AI</span><span class="live mono">AI CONTENT HACK</span><span class="prog"><i></i></span></div>
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
    <script type="module" src="assets/js/posts.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(ct, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
