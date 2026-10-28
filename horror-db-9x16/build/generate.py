"""03:07 AM (horror short): writes index.html. 1080x1920, 30 fps, about 45 s.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D world lives in assets/js/world.js (Three.js, rendered on hf-seek). This file writes the composition: the canvas,
the cue times world.js reads (from build/words.json and voice/lines.json) and the HTML layer on one paused GSAP
timeline: the CCTV HUD (REC, camera label, a clock that ticks from 03:07:14), the hook title, the narrator's cold open
(serif subtitles), the captions (typed monospace, the speaker in front: THE DEV in bone white, CLAUDE in coral), the
case-file tags that pin each story beat (what was deleted, the dead backup, the snapshot, the restore), the black-outs
and the CTA card.

The topic (a developer deletes production; Claude had quietly kept a copy) is the same as the @base.learn reel the client
referenced; the script, the characters' lines and the horror treatment are original.

Audio: assets/audio/mix.wav when build/audio.py has made it, otherwise the bare voice (assets/audio/voice.wav).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
DLG = [ln for ln in LINES if ln["who"] != "narr"]           # the dialogue, lines 1..15 (world.js indexes these)
NARR = [ln for ln in LINES if ln["who"] == "narr"]          # the narrator's cold open, lines 101..
WORDS = json.load(open(os.path.join(B, "words.json")))
VOICE_END = LINES[-1]["end"]
DUR = round(VOICE_END + 1.25, 2)         # the CTA holds 1.25 s after the last word


def word(line, text, nth=1):
    """Start time of the nth word in a line (1-based) that starts with `text` (case-insensitive)."""
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1]["s"]


T = {
    "l": [ln["start"] for ln in DLG], "e": [ln["end"] for ln in DLG], "who": [ln["who"] for ln in DLG],
    "n": [[ln["start"], ln["end"]] for ln in NARR],
    "enter": round(NARR[-1]["end"] + .3, 3),        # the Enter key, after "...connected to production."; the screen floods red
    "rows": word(4, "rows"), "march": word(6, "march"), "checked": word(6, "checked"), "nine": word(7, "nine"),
    "snapshot": word(9, "snapshot"), "friday": word(11, "friday"), "revoked": word(14, "revoked"), "backup": word(15, "backup"),
    "end": DUR,
}
L, E = T["l"], T["e"]
T["eyes"] = round(L[8] - .6, 3)                   # in the blackout before "Before you told me...", two eyes open
T["restore"] = round(L[11], 3)                   # "Restoring now."
T["done"] = round(L[12] - .35, 3)                # the restore hits 100 % just before "Thank you."
T["cut"] = round(T["revoked"] + .55, 3)          # the lights go out on "revoked"
T["cta"] = round(L[14] - .5, 3)

# case-file tags: (start, end, (label, text, style)), one story fact each, under the HUD
TAGS = [
    (T["enter"] + .35, L[1] - .15, ("CASE 0307", "PRODUCTION DATABASE: DELETED", "")),
    (L[3] + .2, L[4] - .15, ("ROWS LOST", "1,204,883 · ALL OF THEM", "")),
    (T["march"] + .05, L[6] - .15, ("LAST WORKING BACKUP", "3 MARCH · 239 DAYS AGO", "")),
    (T["nine"] + .2, E[6] + .3, ("RIGHT NOW", "900 CUSTOMERS ONLINE", "")),
    (T["snapshot"] + .1, L[10] - .15, ("FOUND", "SNAPSHOT BY CLAUDE · 9:40 PM", "claude")),
    (T["done"] + .1, L[13] - .15, ("RESTORED", "1,204,883 ROWS · NONE LOST", "good")),
    (T["revoked"] + .05, T["cut"] + 1.2, ("CLAUDE", "PROD ACCESS: REVOKED", "claude")),     # stays up in the dark
]
A = []


def add(js):
    A.append("      " + js)


def pop(sel, t, frm="opacity:0,y:20", d=.3, ease="power2.out"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{opacity:1,x:0,y:0,scale:1,duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def out(sel, t, d=.2):
    add(f'tl.to("{sel}",{{opacity:0,duration:{d},ease:"power1.in"}},{t:.3f});')


# ---------------------------------------------------------------- the HUD, the hook title, the CTA
HUD = ('<div id="hud"><div class="rec"><i></i>REC</div><div class="cam mono" id="cam">CAM 03 · FLOOR 4</div>'
       '<div class="clock mono"><span id="clk">03:07:14</span> AM</div></div>')
HOOK = ('<div id="hook"><div class="hk-a">03:07 AM.</div></div>')
CTA = ('<div id="cta"><div class="c1 mono">COMMENT</div><div class="c2">' + "".join(f'<span class="cl cl{i}">{c}</span>' for i, c in enumerate("BACKUP")) +
       '</div><div class="c3">for the setup that <span class="serif">saved him</span></div><div class="c4 mono">✦ NXTLVLSOCIAL.AI</div></div>')
CAMS = [(0, "CAM 01 · DESK 12"), (L[1] - .05, "CAM 03 · FLOOR 4"), (L[2] - .05, "CAM 01 · DESK 12"), (L[4] - .05, "CAM 07 · SERVER ROOM B"),
        (L[6] - .05, "CAM 01 · DESK 12"), (L[8] - 1.4, "CAM 01 · SIGNAL LOST"), (L[8] - .1, "CAM 01 · DESK 12"), (L[11] - .05, "CAM 03 · FLOOR 4"),
        (T["cut"], "CAM 03 · SIGNAL LOST")]


def tags_html():
    return "".join(f'<div class="tag {c}" id="tag{i}"><small>{k}</small>{txt}</div>' for i, (_, _, (k, txt, c)) in enumerate(TAGS))


def hud_tl():
    pop("#hud", 0, "opacity:0", .01, "none")
    add(f'tl.fromTo(".rec i",{{opacity:1}},{{opacity:.1,duration:.5,yoyo:true,repeat:{int(DUR / 1)},ease:"steps(1)",immediateRender:false}},0);')
    # the clock: 03:07:14 at frame 0, real seconds after that
    add('(()=>{const o={v:0};tl.to(o,{v:%s,duration:%s,ease:"none",onUpdate:()=>{const s=14+Math.floor(o.v);'
        'document.getElementById("clk").textContent="03:"+String(7+Math.floor(s/60)).padStart(2,"0")+":"+String(s%%60).padStart(2,"0");}},0);})();' % (DUR, DUR))
    for t, s in CAMS:
        add(f'tl.set("#cam",{{textContent:"{s}"}},{max(0, t):.3f});')
    # the hook title: on from frame 0, gone as the dialogue starts
    pop("#hook", 0, "opacity:0", .01, "none")
    pop(".hk-a", 0, "opacity:0,scale:1.15", .18, "power3.out")
    add(f'tl.to("#hook",{{opacity:0,duration:.15,ease:"power2.in"}},{T["enter"] - .05:.3f});')
    for i, (a, z, _) in enumerate(TAGS):
        pop(f"#tag{i}", a, "opacity:0,x:-30", .25, "power3.out")
        add(f'tl.to("#tag{i}",{{opacity:0,duration:.2}},{z:.3f});')
    # the HUD fades for the CTA
    out("#hud", T["cta"] - .1, .3)
    pop("#cta", T["cta"], "opacity:0", .4, "none")
    pop(".c1", T["cta"] + .05, "opacity:0,y:10", .3)
    a = T["backup"] - .08
    for i in range(6):
        pop(f".cl{i}", a + i * .07, "opacity:0,scale:1.6", .12, "power4.out")
    add(f'tl.fromTo(".c2",{{textShadow:"0 0 0px rgba(240,120,90,0)"}},{{textShadow:"0 0 40px rgba(240,120,90,.9)",duration:.4,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{a + .45:.3f});')
    pop(".c3", a + .55, "opacity:0,y:14", .35)
    pop(".c4", a + .95, "opacity:0", .4)


# ---------------------------------------------------------------- captions: typed on, the speaker first
def captions():
    html = []
    first_claude = True
    for i, ln in enumerate(LINES):
        if ln["line"] == 101:                       # "Three-oh-seven A.M." is the hook title already
            continue
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        cid = f"c{ln['line']}"
        if ln["who"] == "narr":
            who = ""
        elif ln["who"] == "dev":
            who = '<b class="who mono">THE DEV</b>'
        else:
            who = f'<b class="who mono">CLAUDE{" · HIS AI AGENT" if first_claude else ""}</b>'
            first_claude = False
        spans = " ".join(f'<span class="w" id="{cid}_{k}">{w["w"]}</span>' for k, w in enumerate(ws))
        html.append(f'<div class="cap {ln["who"]}" id="{cid}"><span class="box">{who}{spans}</span></div>')
        nxt = LINES[i + 1]["start"] if i + 1 < len(LINES) else DUR
        a, z = ws[0]["s"] - .12, min(ln["end"] + .55, nxt - .08)
        add(f'tl.fromTo("#{cid}",{{opacity:0}},{{opacity:1,duration:.08,immediateRender:false}},{a:.3f});')
        add(f'tl.to("#{cid}",{{opacity:0,duration:.12}},{z:.3f});')
        for k, w in enumerate(ws):
            add(f'tl.fromTo("#{cid}_{k}",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:.12,immediateRender:false}},{w["s"] - .04:.3f});')
    return "".join(html)


def fx_tl():
    # hard cuts get a white tick; the blackout before the eyes and the cut on "revoked" are true black
    for t in (L[1] - .05, L[2] - .05, L[4] - .05, L[6] - .05, L[11] - .05):
        add(f'tl.set("#flash",{{opacity:.25}},{t:.3f});tl.to("#flash",{{opacity:0,duration:.12}},{t + .01:.3f});')
    add(f'tl.set("#flash",{{opacity:.9}},{T["enter"]:.3f});tl.to("#flash",{{opacity:0,duration:.25}},{T["enter"] + .02:.3f});')
    add(f'tl.set("#black",{{opacity:1}},{E[7] + .35:.3f});tl.to("#black",{{opacity:0,duration:.05}},{T["eyes"] - .05:.3f});')
    add(f'tl.set("#black",{{opacity:1}},{T["cut"]:.3f});')
    add(f'tl.set("#black",{{opacity:0}},{T["cta"] - .2:.3f});')


CSS = """
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
@font-face { font-family: "ISerif"; font-style: italic; font-weight: 400; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #050508; }
body { font-family: "Montserrat", sans-serif; color: #ece6dc; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #050508; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
.serif { font-family: "ISerif", serif; font-style: italic; font-weight: 400; }
#scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0px, rgba(0,0,0,.18) 2px, rgba(0,0,0,0) 3px, rgba(0,0,0,0) 5px);
  mix-blend-mode: multiply; }
#ui { z-index: 5; }
#hud, #hook, #cta, .c1, .c3, .c4, .cl, .hk-a { opacity: 0; }
#hud { position: absolute; inset: 0; }
.rec { position: absolute; left: 64px; top: 262px; display: flex; align-items: center; gap: 14px; font: 800 36px "Montserrat"; letter-spacing: 3px; color: #ff4d4d;
  text-shadow: 0 0 12px rgba(255,60,60,.6); padding: 4px 14px; margin-left: -14px; border-radius: 10px; background: rgba(0,0,0,.4); }
.rec i { width: 22px; height: 22px; border-radius: 50%; background: #ff3b3b; box-shadow: 0 0 16px #ff3b3b; }
.cam { position: absolute; right: 64px; top: 266px; font-size: 30px; letter-spacing: 3px; color: rgba(236,230,220,.85); text-shadow: 0 0 8px rgba(0,0,0,.9); }
.clock { position: absolute; right: 64px; top: 312px; font-size: 30px; letter-spacing: 3px; color: rgba(236,230,220,.85); text-shadow: 0 0 8px rgba(0,0,0,.9); }
#hook { position: absolute; left: 60px; right: 60px; top: 380px; text-align: center; }
.hk-a { font: 800 132px/1 "Montserrat"; letter-spacing: -4px; color: #f2ede6; text-shadow: 0 0 40px rgba(255,60,60,.35), 0 8px 40px rgba(0,0,0,.9); }
.tag { position: absolute; left: 64px; top: 372px; opacity: 0; padding: 12px 20px 12px 18px; border-radius: 8px; background: rgba(10,4,4,.8);
  border-left: 6px solid #ff3b3b; font: 700 32px/1.2 "JBMono"; letter-spacing: 1px; color: #f4e8e2; text-shadow: 0 0 10px rgba(0,0,0,.8); }
.tag small { display: block; font-size: 28px; letter-spacing: 4px; color: #ff6f6f; margin-bottom: 4px; }
.tag.good { border-left-color: #3dff8a; } .tag.good small { color: #7dffb0; }
.tag.claude { border-left-color: #ff7a59; } .tag.claude small { color: #ff9a7a; }
#caps { z-index: 8; }
.cap { position: absolute; left: 50px; right: 50px; top: 1300px; text-align: center; opacity: 0; }
.cap .box { display: inline-block; max-width: 980px; padding: 14px 24px 18px; border-radius: 14px; background: rgba(6,6,10,.72);
  border-left: 6px solid rgba(236,230,220,.7); font: 700 52px/1.25 "JBMono"; color: #ece6dc; text-align: left; text-shadow: 0 2px 10px rgba(0,0,0,.8); }
.cap.claude .box { border-left-color: #ff7a59; color: #ffb59c; text-shadow: 0 0 18px rgba(255,110,80,.45); }
.cap .who { display: block; font-size: 28px; letter-spacing: 6px; opacity: .65; margin-bottom: 6px; }
.cap.claude .who { color: #ff7a59; opacity: .9; }
.cap .w { display: inline; opacity: 0; }
.cap.narr .box { background: rgba(4,4,6,.55); border-left: none; padding: 12px 28px 16px; font: 400 66px/1.15 "ISerif"; font-style: italic;
  color: #f2ede6; text-align: center; text-shadow: 0 2px 18px rgba(0,0,0,.95); }
#cta { position: absolute; left: 60px; right: 60px; top: 640px; text-align: center; isolation: isolate; }
#cta::before { content: ""; position: absolute; left: -60px; right: -60px; top: -90px; bottom: -80px; z-index: -1;
  background: radial-gradient(ellipse 62% 58% at 50% 50%, rgba(4,2,2,.86) 0%, rgba(4,2,2,.7) 55%, rgba(4,2,2,0) 100%); }
.c1 { font-size: 46px; letter-spacing: 14px; color: rgba(236,230,220,.75); }
.c2 { margin: 18px 0 22px; font: 800 176px/1 "Montserrat"; letter-spacing: 6px; color: #ff8467; }
.cl { display: inline-block; }
.c3 { font: 600 52px/1.2 "Montserrat"; color: #ece6dc; }
.c3 .serif { font-size: 66px; color: #ffc2ad; }
.c4 { margin-top: 60px; font-size: 30px; letter-spacing: 6px; color: rgba(236,230,220,.8); }
#fx { z-index: 7; }
#flash { position: absolute; inset: 0; background: #fff6f0; opacity: 0; }
#black { position: absolute; inset: 0; background: #000; opacity: 0; }
"""


def main():
    hud_tl()
    caps = captions()
    fx_tl()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>03:07 AM 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="scanl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore><div id="scan"></div></div>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2" data-layout-allow-overflow>{HUD}{HOOK}{CTA}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{tags_html()}{caps}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-ignore><div id="flash"></div><div id="black"></div></div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.HR_T = {json.dumps(T)};
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
    json.dump(T, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, audio {mix}")


if __name__ == "__main__":
    main()
