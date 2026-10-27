"""Instagram Growth Agent reel (Option A, "inside the phone"): writes index.html. 1080x1920, 30 fps, about 30 s.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D world lives in assets/js/world.js (Three.js, rendered on hf-seek). This file writes the composition: the canvas,
the cue times world.js reads (from build/words.json) and the HTML layer on one paused GSAP timeline: the hook headline,
the "Five moves" title, a chip for each move, the captions and the end card.

The claims on screen are the client's own, from their original cut of this reel (01c31278-Video-14931.mp4): the page went
from 339 to 2,400 followers, the five moves and the AGENT comment keyword (the course offer in the original is left out
of this cut, at the client's request). Comment handles, trend names and the script lines inside the phone are
illustrative UI, the same ones the original showed where it showed any.

Audio: assets/audio/mix.wav when build/audio.py has made it, otherwise the bare voice (assets/audio/voice.wav).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
VOICE_END = LINES[-1]["end"]
DUR = round(VOICE_END + 1.6, 2)          # the end card holds 1.6 s after the last word


def word(line, text, nth=1):
    """Start time of the nth word in a line that starts with `text` (case-insensitive)."""
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1]["s"]


T = {
    "l": [ln["start"] for ln in LINES], "e": [ln["end"] for ln in LINES],
    "claude": word(1, "claude"), "agent": word(1, "agent"),
    "three": word(2, "three"), "twenty": word(2, "twenty"), "followers": word(2, "followers"),
    "post": word(3, "post"), "grows": word(3, "grows"), "page": word(3, "page"),
    "moves": word(4, "moves"), "last": word(4, "last"), "smartest": word(4, "smartest"),
    "blowing": word(5, "blowing"), "niche": word(5, "niche"), "plans": word(6, "plans"), "visuals": word(6, "visuals"),
    "writes": word(7, "writes"), "script": word(7, "script"), "caption": word(7, "caption"),
    "replies": word(8, "replies"), "comments": word(8, "comments"), "five5": word(9, "five"),
    "studies": word(10, "studies"), "results": word(10, "results"), "rewrites": word(10, "rewrites"), "next": word(10, "next"),
    "agentcta": word(11, "agent"), "setup": word(11, "setup"), "end": DUR,
}
L, E = T["l"], T["e"]
T["in0"] = round(L[4] - .17, 3)          # through the screen into the phone
T["dark0"] = round(L[8] - .08, 3)        # the lights go out for move five
T["out1"] = round(L[10] - .1, 3)         # back out through the screen for the CTA
T["portal"] = round(word(1, "instagram") - .02, 3)   # the hook's tunnel ends: out through the screen

A = []


def add(js):
    A.append("      " + js)


def pop(sel, t, frm="scale:.6,opacity:0,y:30", d=.3, ease="back.out(2.2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def out(sel, t, d=.18):
    add(f'tl.to("{sel}",{{opacity:0,y:-24,scale:.96,duration:{d},ease:"power2.in"}},{t:.3f});')


# ---------------------------------------------------------------- hook headline, "Five moves", move chips
HOOK = ('<div id="hook"><div class="hl hl0"><span class="hw" id="hw0">I</span> <span class="hw" id="hw1">turned</span> '
        '<span class="hw serif" id="hw2">Claude</span> <span class="hw" id="hw3">into</span> <span class="hw" id="hw4">an</span></div>'
        '<div class="hl hl1"><span class="pill" id="hw5">Instagram growth agent</span></div></div>')
FIVE = ('<div id="five"><div class="fv-a">Five <span class="serif">moves.</span></div>'
        '<div class="fv-b">The last one\'s the <span class="serif">smartest.</span></div></div>')
MOVES = ["Spots what's <i>blowing up</i>", "Plans the <i>visuals</i>", "Writes script <i>+ caption</i>",
         "Replies to <i>comments</i>", "Studies results, <i>rewrites</i>"]


def chips():
    h = []
    for i, m in enumerate(MOVES):
        dash = "".join(f'<b class="{"on" if k <= i else ""}"></b>' for k in range(5))
        tag = f"MOVE {i + 1}/5" + (" · THE SMARTEST" if i == 4 else "")
        h.append(f'<div class="mv mv{i}{" dark" if i == 4 else ""}"><div class="mv-t mono">{tag}</div><div class="mv-d">{dash}</div>'
                 f'<div class="mv-h">{m}</div></div>')
    return "".join(h)




def head_tl():
    # the hook headline is on screen from frame 0; each word lands as it is spoken
    pop("#hook", 0, "opacity:0", .01, "none")
    ws = [w for w in WORDS if w["line"] == 1]
    for i in range(5):
        pop(f"#hw{i}", 0 if i < 3 else ws[i]["s"] - .06, "opacity:0,y:36,scale:.7", .22, "back.out(2.6)")
    pop("#hw5", ws[5]["s"] - .06, "opacity:0,scale:.4,rotation:-4", .32, "back.out(2.4)")
    add(f'tl.to("#hook",{{opacity:0,y:-60,scale:1.08,duration:.2,ease:"power3.in"}},{L[1] - .02:.3f});')
    # "Five moves. The last one's the smartest."
    pop("#five", L[3] - .05, "opacity:0", .01, "none")
    pop(".fv-a", L[3] - .05, "opacity:0,scale:1.6", .28, "expo.out")
    pop(".fv-b", T["last"] - .1, "opacity:0,y:30", .25)
    add(f'tl.fromTo(".fv-b .serif",{{color:"#1d1418"}},{{color:"#b4532f",duration:.15,immediateRender:false}},{T["smartest"]:.3f});')
    add(f'tl.to("#five",{{opacity:0,scale:1.3,duration:.22,ease:"power3.in"}},{T["in0"] - .25:.3f});')
    # one chip per move, from its line to the next; move five's on the dark until the CTA
    starts = [L[4], L[5], L[6], L[7], L[9]]
    ends = [L[5] - .3, L[6] - .3, L[7] - .3, T["dark0"] - .05, T["out1"] - .05]
    for i, (a, z) in enumerate(zip(starts, ends)):
        pop(f".mv{i}", a - .12, "x:-90,opacity:0,scale:.9", .24, "back.out(2)")
        out(f".mv{i}", z, .14)


# ---------------------------------------------------------------- end card
def endcard():
    ty = "".join(f'<span class="ty ty{i}">{c}</span>' for i, c in enumerate("AGENT"))
    return ('<div id="endc"><div class="ec-1">Comment</div><div class="ec-kw">' + ty + '<i class="cur"></i></div>'
            '<div class="ec-2">and I\'ll DM you my <span class="serif">whole setup</span></div></div>')


def endcard_tl():
    a = T["agentcta"] - .1
    pop("#endc", L[10] - .1, "opacity:0,y:40", .3, "back.out(1.8)")
    pop(".ec-1", L[10] - .08, "y:20,opacity:0", .22)
    pop(".ec-kw", a - .05, "scale:.6,opacity:0", .28, "back.out(2.2)")
    for i in range(5):                                   # typed in, letter by letter
        pop(f".ty{i}", a + .04 + i * .075, "opacity:0,y:-30,scale:1.4", .14, "back.out(3)")
    add(f'tl.fromTo(".cur",{{opacity:1}},{{opacity:0,duration:.22,yoyo:true,repeat:{int((DUR - a) / .44)},ease:"steps(1)",immediateRender:false}},{a:.3f});')
    pop(".ec-2", T["setup"] - .2, "y:20,opacity:0", .28)
    add(f'tl.to(".ec-kw",{{scale:.93,duration:.09,yoyo:true,repeat:1,ease:"power2.out"}},{VOICE_END - .05:.3f});')


# ---------------------------------------------------------------- captions: 1-3 words at a time, the spoken word lit
# One fixed place (y 1330, above the platform UI). Light scenes: a white glass box, ink text, the spoken word on a
# terracotta pill. The dark lab (move five): a dark box. "Five moves." and "AGENT" slam.
def captions():
    html = []
    for ln in LINES:
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        # phrases (split at punctuation), long ones halved, a lone "Two:" joined to what follows
        phr, cur = [], []
        for w in ws:
            cur.append(w)
            if re.search(r"[.,?!:…]$", w["w"]):
                phr.append(cur); cur = []
        if cur:
            phr.append(cur)
        chunks = []
        for p in phr:
            if chunks and len(chunks[-1]) == 1 and chunks[-1][0]["w"].endswith(":") and len(p) <= 4:
                chunks[-1] += p
            elif len(p) > 5:
                chunks += [p[:(len(p) + 1) // 2], p[(len(p) + 1) // 2:]]
            else:
                chunks.append(p)
        nxt_line = next((l2["start"] for l2 in LINES if l2["line"] == ln["line"] + 1), DUR)
        for ci, ch in enumerate(chunks):
            cid = f"c{ln['line']}_{ci}"
            spans = "".join(f'<span class="w" id="{cid}_{k}">{w["w"]}</span> ' for k, w in enumerate(ch))
            a = ch[0]["s"] - .05
            z = chunks[ci + 1][0]["s"] - .05 if ci + 1 < len(chunks) else min(ln["end"] + .3, nxt_line - .06)
            dark = T["dark0"] <= a < T["out1"]
            slam = (ln["line"] == 4 and ci == 0) or (ln["line"] == 11 and ci == 0) or (ln["line"] == 9)
            cls = ("dark " if dark else "") + ("slam" if slam else "")
            html.append(f'<div class="cap {cls}" id="{cid}"><span class="box">{spans.strip()}</span></div>')
            if slam:
                add(f'tl.fromTo("#{cid}",{{opacity:0,scale:1.9}},{{opacity:1,scale:1,duration:.2,ease:"expo.out",immediateRender:false}},{a:.3f});')
            else:
                add(f'tl.fromTo("#{cid}",{{opacity:0,y:16,scale:.94}},{{opacity:1,y:0,scale:1,duration:.13,ease:"back.out(2)",immediateRender:false}},{a:.3f});')
            add(f'tl.set("#{cid}",{{opacity:0}},{z:.3f});')
            for k, w in enumerate(ch):
                add(f'tl.set("#{cid}_{k}",{{backgroundColor:"#c25a37",color:"#ffffff"}},{w["s"]:.3f});')
                add(f'tl.set("#{cid}_{k}",{{backgroundColor:"rgba(217,119,87,0)",color:"{"#f6ece2" if dark else "#1d1418"}"}},{w["e"] + .02:.3f});')
    return "".join(html)


def fx_tl():
    # the portal cuts (into the phone, out of it) and the blackout are white / black flashes; ticks on the whip moves
    for t, o, d in ((T["in0"] - .04, 1.0, .32), (T["out1"] - .04, 1.0, .32), (T["claude"] - .02, .35, .2),
                    (T["followers"], .3, .3), (T["rewrites"], .35, .25), (T["next"] + .1, .25, .3), (T["portal"] - .03, 1.0, .35)):
        add(f'tl.set("#flash",{{opacity:{o}}},{t:.3f});tl.to("#flash",{{opacity:0,duration:{d}}},{t + .03:.3f});')
    for t in (L[5] - .14, L[6] - .14, L[7] - .14, T["grows"] - .1, L[3] - .1):
        add(f'tl.set("#flash",{{opacity:.14}},{t:.3f});tl.to("#flash",{{opacity:0,duration:.14}},{t + .01:.3f});')
    add(f'tl.set("#black",{{opacity:1}},{T["dark0"]:.3f});tl.to("#black",{{opacity:0,duration:.18}},{T["five5"] - .02:.3f});')
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')


CSS = """
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
@font-face { font-family: "ISerif"; font-style: italic; font-weight: 400; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #f2e8dc; }
body { font-family: "Montserrat", sans-serif; color: #1d1418; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #f2e8dc; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
.serif { font-family: "ISerif", serif; font-style: italic; font-weight: 400; letter-spacing: 0; }
#ui { z-index: 5; }
.top { position: absolute; left: 60px; right: 60px; top: 262px; display: flex; align-items: center; gap: 24px; }
.brand { font-size: 30px; letter-spacing: 5px; color: #1d1418; padding: 6px 18px; border-radius: 22px; background: rgba(255,251,246,.9); }
.brand b { color: #b4532f; }
.prog { flex: 1; height: 6px; border-radius: 3px; background: rgba(29,20,24,.12); overflow: hidden; }
.prog i { display: block; height: 100%; background: #d97757; transform-origin: 0 50%; transform: scaleX(0); }
/* everything that pops in later starts hidden here, never through a set at t=0 */
#hook, .hw, #five, .fv-a, .fv-b, .mv, #endc, .ec-1, .ec-kw, .ec-2, .ty { opacity: 0; }
#hook { position: absolute; left: 40px; right: 40px; top: 316px; text-align: center; }
.hl { display: block; font: 800 92px/1.05 "Montserrat"; letter-spacing: -3px; color: #1d1418; text-shadow: 0 4px 30px rgba(242,232,220,.9); }
.hw { display: inline-block; }
.hl .serif { font-size: 112px; color: #b4532f; }
.pill { display: inline-block; margin-top: 14px; padding: 6px 30px 14px; border-radius: 28px; background: #c25a37; color: #fff;
  font: 800 80px/1.05 "Montserrat"; letter-spacing: -2px; box-shadow: 0 16px 44px rgba(217,119,87,.45); }
#five { position: absolute; left: 40px; right: 40px; top: 318px; text-align: center; }
.fv-a { font: 800 140px/1 "Montserrat"; letter-spacing: -5px; color: #1d1418; }
.fv-a .serif { font-size: 168px; color: #b4532f; }
.fv-b { margin-top: 18px; font: 700 54px/1.1 "Montserrat"; color: #1d1418; }
.fv-b .serif { font-size: 70px; }
.mv { position: absolute; left: 60px; right: 60px; top: 312px; }
.mv-t { display: inline-block; padding: 8px 22px; border-radius: 30px; background: #1d1418; color: #f6ece2; font-size: 28px; letter-spacing: 3px; }
.mv-d { display: flex; gap: 10px; margin: 18px 0 10px 6px; }
.mv-d b { width: 54px; height: 8px; border-radius: 4px; background: rgba(29,20,24,.16); }
.mv-d b.on { background: #d97757; }
.mv-h { font: 800 74px/1.05 "Montserrat"; letter-spacing: -2.5px; color: #1d1418; text-shadow: 0 4px 26px rgba(242,232,220,.8); }
.mv-h i { font-family: "ISerif"; font-weight: 400; font-size: 88px; color: #b4532f; letter-spacing: 0; }
.mv.dark .mv-t { background: #c25a37; color: #fff; }
.mv.dark .mv-d b { background: rgba(246,236,226,.2); } .mv.dark .mv-d b.on { background: #f0a07c; }
.mv.dark .mv-h { color: #f6ece2; text-shadow: 0 4px 30px rgba(0,0,0,.8); }
.mv.dark .mv-h i { color: #f0a07c; }
#endc { position: absolute; left: 60px; right: 60px; top: 300px; text-align: center; }
.ec-1 { display: inline-block; padding: 10px 34px; border-radius: 24px; background: #1d1418; color: #f6ece2; font: 800 60px "Montserrat"; letter-spacing: 2px; }
.ec-kw { display: block; width: max-content; margin: 16px auto 14px; padding: 4px 54px 14px; border-radius: 34px; background: #c25a37;
  font: 800 150px/1.05 "Montserrat"; letter-spacing: 6px; color: #fff; box-shadow: 0 20px 60px rgba(217,119,87,.55); transform: rotate(-2deg); }
.ec-2 { display: inline-block; padding: 8px 26px 12px; border-radius: 22px; background: rgba(255,251,246,.92); font: 700 46px/1.2 "Montserrat"; color: #1d1418; box-shadow: 0 10px 30px rgba(120,70,40,.15); }
.ec-2 .serif { font-size: 60px; color: #b4532f; }
.ty { display: inline-block; }
.cur { display: inline-block; width: 10px; height: 118px; margin-left: 8px; vertical-align: -10px; border-radius: 5px; background: #fff; }
#caps { z-index: 6; }
.cap { position: absolute; left: 50px; right: 50px; top: 1330px; text-align: center; opacity: 0; }
.cap .box { display: inline-block; max-width: 980px; padding: 12px 20px 14px; border-radius: 26px; background: rgba(255,251,246,.92);
  box-shadow: 0 14px 40px rgba(120,70,40,.18); font: 800 62px/1.15 "Montserrat"; letter-spacing: -1px; color: #1d1418; }
.cap .w { display: inline-block; padding: 2px 12px 5px; border-radius: 16px; }
.cap.dark .box { background: rgba(18,10,16,.86); color: #f6ece2; box-shadow: 0 14px 40px rgba(0,0,0,.5); }
.cap.slam .box { font-size: 92px; letter-spacing: -2px; }
#fx { z-index: 7; }
#flash { position: absolute; inset: 0; background: #fff8f1; opacity: 0; }
#black { position: absolute; inset: 0; background: #07040a; opacity: 0; }
"""


def main():
    head_tl()
    endc = endcard()
    endcard_tl()
    caps = captions()
    fx_tl()
    mix = "mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "voice.wav"
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Instagram Growth Agent 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b>✦</b> AI.NXTLVL</span><span class="prog"><i></i></span></div>
        {HOOK}{FIVE}{chips()}{endc}
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{caps}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-ignore><div id="flash"></div><div id="black"></div></div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.GA_T = {json.dumps(T)};
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
