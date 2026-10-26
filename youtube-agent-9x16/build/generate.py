"""YouTube Agent Skill reel: writes index.html. 1080x1920, 30 fps, about 35 s.

python3 build/generate.py      (from the project root, after build/voice.py and build/timing.py)

The 3D world lives in assets/js/world.js (Three.js, rendered on hf-seek). This file writes the composition: the canvas,
the cue times world.js reads (from build/words.json), the speaker envelopes for the mouths, and the HTML layer on one
paused GSAP timeline: the top bar, the 3 AM hook stamp, the "free" pill, the skill chip for each station, the captions
and the end card with the DM.

Every claim on screen is from the repo's README (github.com/Jakeschincariol/youtube-agent-skill, MIT): eleven skills,
21 hook formulas, title and thumbnail linted as a pair, an edit decision list (it marks the cuts, it doesn't edit),
replies in your voice and which one to pin, "one anchor, one cheap one, three Shorts", outliers ranked by the multiple
over each channel's own median, and the install is pasting one link. The multiples on the city towers are illustrative.

Audio: assets/audio/mix.wav when build/audio.py has made it, otherwise the bare voice (assets/audio/voice.wav).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
ENV = json.load(open(os.path.join(B, "env.json")))
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
    "free": word(2, "free"), "eleven": word(3, "eleven"), "twentyone": word(4, "twenty"),
    "blowing": word(10, "blowing"), "niche": word(10, "niche"), "writes": word(10, "writes"), "voice": word(10, "voice"),
    "setup": word(11, "setup"), "paste": word(11, "paste"), "link": word(11, "link"),
    "youtube": word(12, "youtube"), "end": DUR,
}
L, E = T["l"], T["e"]

A = []


def add(js):
    A.append("      " + js)


def pop(sel, t, frm="scale:.6,opacity:0,y:30", d=.35, ease="back.out(2.2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def out(sel, t, d=.2):
    add(f'tl.to("{sel}",{{opacity:0,y:-20,duration:{d},ease:"power2.in"}},{t:.3f});')


# ---------------------------------------------------------------- hook stamp, "free" pill, skill chips
HOOK = '<div id="clock"><span class="dig">03<i class="colon">:</i>00</span><span class="am">AM</span></div>'
FREE = '<div id="free"><b>FREE</b><span>open source · MIT licence</span></div>'
CHIPS = [("/yt-script", "21 hook formulas"), ("/yt-package", "title + thumbnail, linted as a pair"), ("/yt-edit", "marks every cut: an edit list"),
         ("/yt-comment", "replies in your voice"), ("/yt-plan", "1 anchor · 1 cheap one · 3 Shorts"), ("/yt-viral", "beat their own channel, ranked")]


def chips():
    h = []
    for i, (c, d) in enumerate(CHIPS):
        n = f'<em class="n">{i + 1 if i < 5 else 6}</em>'
        d = d if i else '<b class="cnt">0</b> hook formulas'
        h.append(f'<div class="chip ch{i}">{n}<span class="cmd mono">{c}</span><span class="cd">{d}</span></div>')
    return "".join(h)


def hook_tl():
    # the 3 AM stamp: slammed in on the first word, the colon blinking, glitched out when Claude arrives
    pop("#clock", .08, "scale:1.6,opacity:0", .28, "back.out(2.6)")
    add(f'tl.fromTo(".colon",{{opacity:1}},{{opacity:.15,duration:.25,yoyo:true,repeat:{int(L[1] / .5)},ease:"steps(1)",immediateRender:false}},.1);')
    add('tl.fromTo("#clock",{x:0},{x:12,duration:.04,yoyo:true,repeat:7,immediateRender:false},1.18);')
    add(f'tl.to("#clock",{{opacity:0,scale:1.3,duration:.18,ease:"power3.in"}},{L[1] - .2:.3f});')
    pop("#free", T["free"] - .04, "scale:1.8,opacity:0,rotation:-6", .3, "back.out(2.8)")
    out("#free", L[2] + .3, .2)
    # skill chips: one per station line, and /yt-viral for the city
    starts = [L[3], L[4], L[5], L[6], L[7], T["blowing"] - .1]
    ends = [L[4] - .12, L[5] - .12, L[6] - .12, L[7] - .12, E[7] + .2, L[10] - .15]
    for i, (a, z) in enumerate(zip(starts, ends)):
        pop(f".ch{i}", a - .1, "x:-80,opacity:0,scale:.9", .3, "back.out(2)")
        out(f".ch{i}", z, .15)
    add('(()=>{const o={v:0};tl.to(o,{v:21,duration:1.0,ease:"power2.out",onUpdate:()=>{document.querySelector(".cnt").textContent=Math.round(o.v);}},%.3f);})();'
        % (T["twentyone"] - .25))


# ---------------------------------------------------------------- end card + DM
def endcard():
    ty = "".join(f'<span class="ty ty{i}">{c}</span>' for i, c in enumerate("YOUTUBE"))
    return ('<div id="endc"><div class="ec-1">Comment</div><div class="ec-kw">' + ty + '<i class="cur"></i></div>'
            '<div class="ec-2">and I\'ll DM you the free repo + the full guide</div>'
            '<div class="ec-3">Send this to a creator who\'s still up at 3 AM</div><div class="ec-h mono">✦ @ai.nxtlvl</div></div>'
            '<div id="dm"><div class="dmav">✦</div><div class="tbody"><div class="thead"><b>ai.nxtlvl</b><span>now</span></div>'
            '<div class="ttext">Sent you the YouTube Agent Skill + the full guide</div></div><div class="dmok">✓</div></div>')


def endcard_tl():
    a = T["youtube"] - .12
    pop("#endc", a - .1, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-1", a - .05, "y:20,opacity:0", .25)
    pop(".ec-kw", a - .02, "scale:.6,opacity:0", .3, "back.out(2.2)")
    for i in range(7):                                    # typed in, letter by letter
        pop(f".ty{i}", a + .1 + i * .07, "opacity:0,y:-30,scale:1.4", .14, "back.out(3)")
    add(f'tl.fromTo(".cur",{{opacity:1}},{{opacity:0,duration:.22,yoyo:true,repeat:{int((DUR - a) / .44)},ease:"steps(1)",immediateRender:false}},{a:.3f});')
    pop(".ec-2", a + .55, "y:20,opacity:0", .3)
    pop(".ec-3", a + .95, "y:20,opacity:0", .35)
    pop(".ec-h", a + 1.25, "y:20,opacity:0", .3)
    add(f'tl.to(".ec-kw",{{scale:.94,duration:.09,yoyo:true,repeat:1,ease:"power2.out"}},{VOICE_END - .05:.3f});')
    pop("#dm", VOICE_END + .1, "y:60,opacity:0,scale:.9", .38, "back.out(2)")
    pop(".dmok", VOICE_END + .45, "scale:0,opacity:0", .3, "back.out(3)")


# ---------------------------------------------------------------- captions: 2-3 words at a time, the spoken word lit
# One fixed place (y 1330, above the platform UI) on a dark glass box; Montserrat ExtraBold; the spoken word sits on a
# violet pill. The dot says who talks (grey: the creator, coral: Claude). The whisper is set lighter; "Virality." slams.
def captions():
    html = []
    for ln in LINES:
        ws = [w for w in WORDS if w["line"] == ln["line"]]
        chunks, cur = [], []
        for w in ws:
            cur.append(w)
            if len(cur) == 3 or re.search(r"[.,?!…]$", w["w"]):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        nxt_line = next((l2["start"] for l2 in LINES if l2["line"] == ln["line"] + 1), DUR)
        for ci, ch in enumerate(chunks):
            cid = f"c{ln['line']}_{ci}"
            spans = "".join(f'<span class="w" id="{cid}_{k}">{w["w"]}</span> ' for k, w in enumerate(ch))
            cls = ln["speaker"] + (" whisper" if ln["line"] == 9 else "") + (" slam" if ln["line"] == 10 and ci == 0 else "")
            html.append(f'<div class="cap {cls}" id="{cid}"><span class="box"><i class="dot"></i>{spans.strip()}</span></div>')
            a = ch[0]["s"] - .05
            z = chunks[ci + 1][0]["s"] - .05 if ci + 1 < len(chunks) else min(ln["end"] + .35, nxt_line - .06)
            if "slam" in cls:
                add(f'tl.fromTo("#{cid}",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:.22,ease:"expo.out",immediateRender:false}},{a:.3f});')
            else:
                add(f'tl.fromTo("#{cid}",{{opacity:0,y:18,scale:.94}},{{opacity:1,y:0,scale:1,duration:.14,ease:"back.out(2)",immediateRender:false}},{a:.3f});')
            add(f'tl.set("#{cid}",{{opacity:0}},{z:.3f});')
            for k, w in enumerate(ch):
                add(f'tl.set("#{cid}_{k}",{{backgroundColor:"#7B2FFB",color:"#ffffff"}},{w["s"]:.3f});')
                add(f'tl.set("#{cid}_{k}",{{backgroundColor:"rgba(123,47,251,0)",color:"#EDE8F7"}},{w["e"] + .02:.3f});')
    return "".join(html)


def fx_tl():
    # whips on the station changes, flashes on the burst, the drop and the landing
    for t in (L[3] - .3, L[4] - .3, L[5] - .3, L[6] - .3, L[7] - .3):
        add(f'tl.set("#whip",{{opacity:.7,x:300}},{t:.3f});tl.to("#whip",{{opacity:0,x:-300,duration:.22,ease:"power2.out"}},{t + .01:.3f});')
    for t, o in ((L[1] - .1, .6), (T["free"] - .02, .25), (T["eleven"] - .02, .35), (L[9], .85), (L[10] - .02, .7), (T["youtube"], .25)):
        add(f'tl.set("#flash",{{opacity:{o}}},{t:.3f});tl.to("#flash",{{opacity:0,duration:.4}},{t + .02:.3f});')
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')


CSS = """
@font-face { font-family: "Poppins"; font-weight: 600; src: url("assets/fonts/poppins-600.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #07050d; }
body { font-family: "Poppins", sans-serif; color: #f4f1fa; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #07050d; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
#ui { z-index: 5; }
.top { position: absolute; left: 60px; right: 60px; top: 262px; display: flex; align-items: center; gap: 24px; }
.brand { font-size: 28px; letter-spacing: 5px; color: #f4f1fa; text-shadow: 0 2px 12px rgba(0,0,0,.6); }
.brand b { color: #b89bff; }
.prog { flex: 1; height: 6px; border-radius: 3px; background: rgba(244,241,250,.18); overflow: hidden; }
.prog i { display: block; height: 100%; background: linear-gradient(90deg, #7b2ffb, #d97757); transform-origin: 0 50%; transform: scaleX(0); }
/* everything that pops in later starts hidden here, never through a set at t=0 */
#clock, #free, .chip, #endc, .ec-1, .ec-kw, .ec-2, .ec-3, .ec-h, #dm, .dmok, .ty { opacity: 0; }
#clock { position: absolute; left: 0; right: 0; top: 330px; text-align: center; font: 800 150px/1 "JBMono"; color: #ff3b46;
  text-shadow: 0 0 40px rgba(255,59,70,.75), 0 6px 24px rgba(0,0,0,.6); letter-spacing: 4px; }
#clock .am { font-size: 64px; margin-left: 18px; vertical-align: 52px; }
#clock i { font-style: normal; }
#free { position: absolute; left: 50%; top: 340px; width: 700px; margin-left: -350px; padding: 16px 0 20px; border-radius: 40px; text-align: center;
  background: linear-gradient(90deg, #7b2ffb, #d97757); box-shadow: 0 16px 50px rgba(123,47,251,.55); }
#free b { display: block; font: 800 96px/1 "Poppins"; letter-spacing: 6px; }
#free span { font: 700 32px "Poppins"; color: #fff3ea; }
.chip { position: absolute; left: 60px; top: 318px; display: flex; align-items: center; gap: 18px; padding: 10px 30px 10px 12px; border-radius: 40px;
  background: rgba(14,9,26,.86); border: 2px solid rgba(240,160,124,.55); box-shadow: 0 12px 34px rgba(0,0,0,.45); max-width: 960px; }
.chip .n { font: 800 30px "Poppins"; font-style: normal; width: 56px; height: 56px; border-radius: 50%; background: #d97757; color: #fff;
  display: flex; align-items: center; justify-content: center; flex: none; }
.chip .cmd { font-size: 36px; color: #f0a07c; }
.chip .cd { font: 700 32px "Poppins"; color: #f4f1fa; white-space: nowrap; }
.chip .cnt { color: #ffc24a; }
.ch5 { border-color: rgba(56,214,245,.6); } .ch5 .n { background: #38d6f5; color: #07050d; } .ch5 .cmd { color: #38d6f5; }
#dm { position: absolute; left: 60px; right: 60px; top: 1470px; min-height: 136px; border-radius: 36px; display: flex; align-items: center; gap: 24px;
  padding: 20px 30px; background: rgba(28,22,40,.9); border: 1px solid rgba(255,255,255,.14); box-shadow: 0 24px 60px rgba(0,0,0,.5); }
.dmav { flex: none; width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(160deg, #a98bff, #7b2ffb);
  display: flex; align-items: center; justify-content: center; font: 800 40px "Poppins"; color: #fff; }
.tbody { flex: 1; min-width: 0; }
.thead { display: flex; align-items: baseline; justify-content: space-between; }
.thead b { font: 700 32px "Poppins"; color: #fff; }
.thead span { font: 600 26px "Poppins"; color: rgba(244,241,250,.55); }
.ttext { font: 600 30px/1.3 "Poppins"; color: #e4dcf5; margin-top: 4px; }
.dmok { flex: none; width: 56px; height: 56px; border-radius: 50%; background: #3fd69b; color: #07050d; display: flex; align-items: center;
  justify-content: center; font: 800 32px "Poppins"; }
.ty { display: inline-block; }
.cur { display: inline-block; width: 9px; height: 100px; margin-left: 8px; vertical-align: -8px; border-radius: 5px; background: #fff; }
#caps { z-index: 6; }
.cap { position: absolute; left: 50px; right: 50px; top: 1330px; text-align: center; opacity: 0; }
.cap .box { display: inline-block; max-width: 980px; padding: 14px 22px 16px; border-radius: 28px; background: rgba(10,6,20,.84);
  border: 1px solid rgba(169,139,255,.3); box-shadow: 0 14px 40px rgba(0,0,0,.45); font: 800 60px/1.15 "Montserrat"; letter-spacing: -.5px; color: #EDE8F7; }
.cap .w { display: inline-block; padding: 2px 12px 4px; border-radius: 16px; }
.cap .dot { display: inline-block; width: 18px; height: 18px; border-radius: 50%; margin: 0 6px 0 4px; vertical-align: 10px; background: #9a98a6; }
.cap.claude .dot { background: #d97757; box-shadow: 0 0 14px #d97757; }
.cap.whisper .box { font-weight: 600; font-style: italic; letter-spacing: 1px; background: rgba(10,6,20,.7); }
.cap.slam .box { font-size: 96px; letter-spacing: 2px; border-color: rgba(56,214,245,.7); box-shadow: 0 0 60px rgba(56,214,245,.45); }
#endc { position: absolute; left: 60px; right: 60px; top: 330px; padding: 40px 36px 36px; border-radius: 40px; text-align: center;
  background: linear-gradient(160deg, rgba(42,22,82,.86), rgba(14,8,30,.9)); border: 2px solid rgba(240,160,124,.5);
  box-shadow: 0 30px 80px rgba(0,0,0,.5); }
.ec-1 { font: 700 52px "Poppins"; }
.ec-kw { display: inline-block; margin: 12px 0 10px; padding: 6px 44px; border-radius: 40px; background: linear-gradient(90deg, #7b2ffb, #d97757);
  font: 800 118px/1.1 "Poppins"; letter-spacing: 3px; color: #fff; box-shadow: 0 16px 50px rgba(123,47,251,.6); }
.ec-2 { font: 700 40px/1.25 "Poppins"; color: #f4f1fa; }
.ec-3 { margin-top: 18px; font: 600 32px "Poppins"; color: #d9ccff; }
.ec-h { margin-top: 16px; font-size: 30px; color: #f0a07c; letter-spacing: 3px; }
#fx { z-index: 7; }
#flash { position: absolute; inset: 0; background: #fff3ea; opacity: 0; }
#whip { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(90deg, rgba(255,255,255,0) 0 22px,
  rgba(240,160,124,.5) 22px 26px, rgba(255,255,255,0) 26px 70px); }
#vig { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(7,5,13,.55) 0%, rgba(7,5,13,0) 18%, rgba(7,5,13,0) 66%, rgba(7,5,13,.5) 100%); }
"""


def main():
    hook_tl()
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
    <title>YouTube Agent Skill 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="vigl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore><div id="vig"></div></div>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2" data-layout-allow-overflow>
        <div class="top"><span class="brand mono"><b>●</b> AI.NXTLVL</span><span class="prog"><i></i></span></div>
        {HOOK}{FREE}{chips()}{endc}
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{caps}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-ignore><div id="whip"></div><div id="flash"></div></div>
      <audio id="mix" src="assets/audio/{mix}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.YT_T = {json.dumps(T)};
      window.YT_ENV = {json.dumps(ENV, separators=(",", ":"))};
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
