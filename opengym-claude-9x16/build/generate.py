"""openGym x Claude reel: writes index.html. 1080x1920, 30 fps, under 35 s.

python opengym-claude-9x16/build/generate.py      (after voice/make_voices.py assemble and build/timing.py)

The 3D world lives in assets/js/opengym.js (Three.js, rendered on hf-seek). This file writes the composition: the
canvas, the cue times opengym.js reads (all snapped to the real word timings in build/words.json), the speaker
envelopes for the mouths, and the HTML layer on one paused GSAP timeline: the top bar, the step chip, the glass UI
panel with its screens, the captions and the end card.

The panel screens are MOCKS (no screen recordings were supplied): a fictional "FitPro" paywall, the openGym repo card,
the AI Coach and a guided workout, drawn in the same layout so real recordings can replace them later. Every claim on
them is from SCRIPT.md's fact table (openGym README + CHANGELOG, v1.4.2).
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
DUR = round(VOICE_END + 1.5, 2)          # end card held 1.5 s after the last word (it is up from "Comment GYM")
assert DUR < 35, f"reel is {DUR} s; the voice must end by 33.5 s"


def word(line, text, nth=1):
    """Start time of the nth word in a line that starts with `text` (case-insensitive)."""
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1]["s"]


T = {
    "l": [ln["start"] for ln in LINES], "e": [ln["end"] for ln in LINES],
    "free": word(2, "free"), "claude": word(2, "claude"),
    "x": [word(4, "subscription"), word(4, "ads"), word(4, "account")],
    "coachClaude": word(5, "claude"),
    "g": [word(6, "four"), word(6, "dumbbells"), word(6, "build")],
    "approve": word(7, "approve"),
    "demos": word(8, "fifty"), "demosEnd": word(8, "demos"), "weights": word(8, "weights"), "ready": word(8, "weight", 2),
    "worked": word(10, "worked"), "recovering": word(10, "recovering"), "untrained": word(10, "untrained"), "legs": word(10, "legs"),
    "gym": word(12, "gym"), "prompt": word(12, "prompt"),
    "beat0": 0.0, "end": DUR,
}
L, E = T["l"], T["e"]

A = []


def add(js):
    A.append("      " + js)


def pop(sel, t, frm="scale:.6,opacity:0,y:30", d=.35, ease="back.out(2.2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,rotationX:0,duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def out(sel, t, d=.2):
    add(f'tl.to("{sel}",{{opacity:0,y:-20,duration:{d},ease:"power2.in"}},{t:.3f});')


def setv(sel, t, props):
    add(f'tl.set("{sel}",{{{props}}},{t:.3f});')


# ---------------------------------------------------------------- panel screens (MOCKS)
def screens():
    h = []
    h.append('<div class="scr" id="s-pay"><div class="appbar"><span class="appname">FitPro</span><span class="pill red">PREMIUM</span></div>'
             '<div class="paylock">🔒</div><div class="ptitle">Upgrade to Pro</div><div class="psub">Your free trial has ended.</div>'
             '<div class="plist"><div class="pl">🔒 Workout history</div><div class="pl">🔒 Custom routines</div><div class="pl">🔒 Progress charts</div></div>'
             '<div class="pbtn">Upgrade now</div></div>')
    h.append('<div class="scr" id="s-repo"><div class="repo-h mono">github.com/DuarteSantos8/<b>openGym</b></div>'
             '<div class="repo-t">openGym</div><div class="repo-d">Free, open-source gym tracker.</div>'
             '<div class="repo-row"><span class="pill vio">AGPL-3.0</span><span class="pill grn">free · no paid tier</span></div>'
             '<div class="quote">“No account on someone else’s server, no subscription, no ads, no telemetry.”<span class="mono">README</span></div></div>')
    h.append('<div class="scr" id="s-coach"><div class="appbar"><span class="appname">openGym</span><span class="pill vio">AI COACH</span></div>'
             '<div class="crow"><span class="pill vio cp1">Anthropic · Claude</span><span class="pill gold cp2">🔑 your own key</span></div>'
             '<div class="cdesc">Drafts a week of routines. You approve every change.</div>'
             '<div class="clab mono goal-l">YOUR GOAL</div><div class="goalbox"><span class="ph">Tell your coach your goal…</span>' + "".join(f'<span class="gchip gc{i}">{s}</span>' for i, s in enumerate(["4 days", "dumbbells", "build muscle"])) + '</div>'
             '<div class="cbtn">✦ Draft my week</div>'
             '<div class="week">' + "".join(f'<div class="wr wr{i}"><b>{d}</b><span>{r}</span></div>' for i, (d, r) in enumerate([("MON", "Upper"), ("TUE", "Lower"), ("THU", "Upper"), ("FRI", "Lower")])) + '</div>'
             '<div class="abtn">Approve</div><div class="abtn2">✓ Approved · you approve every change</div></div>')
    h.append('<div class="scr" id="s-train"><div class="appbar"><span class="appname">Guided workout</span><span class="pill vio">TRAIN</span></div>'
             '<div class="tx"><div class="demo"><svg viewBox="0 0 200 200" width="150" height="150"><circle cx="100" cy="40" r="20" fill="#d9ccff"/>'
             '<path d="M100 62 L100 130 M100 130 L80 190 M100 130 L120 190" stroke="#d9ccff" stroke-width="12" stroke-linecap="round" fill="none"/>'
             '<path d="M100 72 L78 110" stroke="#d9ccff" stroke-width="11" stroke-linecap="round"/>'
             '<g class="fa" style="transform-origin:78px 110px"><path d="M78 110 L78 150" stroke="#a98bff" stroke-width="11" stroke-linecap="round"/>'
             '<rect x="62" y="146" width="32" height="12" rx="5" fill="#7b2ffb"/></g></svg></div>'
             '<div class="tinfo"><div class="ename">Dumbbell Curl</div><div class="lib"><b class="cnt">0</b> exercises with demos</div></div></div>'
             '<div class="sets"><div class="srow sr0"><span>SET 1</span><b>12.5 kg × 10</b><em>pre-filled ✓</em></div>'
             '<div class="srow sr1"><span>SET 2</span><b>12.5 kg × 10</b><em>pre-filled ✓</em></div></div>'
             '<div class="next"><span>Next session</span><b>15 kg</b><i>↑ +2.5 kg</i></div></div>')
    return "".join(h)


TOASTS = ('<div class="toast t1"><div class="ticon"><span class="tlock">🔒</span></div><div class="tbody"><div class="thead"><b>FitPro</b><span>now</span></div>'
          '<div class="ttext">Your free trial has ended. Upgrade to Pro to keep your workouts.</div></div></div>'
          '<div class="toast t2"><div class="ticon"><span>%</span></div><div class="tbody"><div class="thead"><b>FitPro</b><span>now</span></div>'
          '<div class="ttext">Progress charts are locked. Unlock them with Pro.</div></div></div>')


def screens_tl():
    # panel: hidden through the hook (two paywall notifications and the 3D card carry it), up with the repo card at
    # line 4, folds away at line 9
    add(f'tl.fromTo("#panel",{{rotationX:70,opacity:0,y:60,scale:.9}},{{rotationX:0,opacity:1,y:0,scale:1,duration:.38,ease:"back.out(1.6)",immediateRender:false}},{L[3]:.3f});')
    add(f'tl.to("#panel",{{rotationX:-75,opacity:0,y:-80,scale:.9,duration:.32,ease:"power3.in"}},{L[8] - .05:.3f});')
    # initial states live in the CSS: a set at t=0 is reverted when the renderer seeks back to 0 and not replayed
    # hook: the paywall arrives as phone notifications, buzzing with the phone (0.0 and 1.1 s), swiped away on "Delete it"
    add('tl.fromTo(".t1",{x:0},{x:10,duration:.035,yoyo:true,repeat:9,immediateRender:false},0.05);')
    pop(".t2", 1.1, "y:-60,opacity:0,scale:.92", .35, "back.out(1.8)")
    add('tl.fromTo(".t2",{x:0},{x:10,duration:.035,yoyo:true,repeat:7,immediateRender:false},1.45);')
    add('tl.fromTo(".tlock",{rotation:0},{rotation:16,duration:.05,yoyo:true,repeat:11,immediateRender:false},0.05);')
    add(f'tl.to(".t1",{{x:-1150,rotation:-6,duration:.32,ease:"power3.in"}},{L[1] + .02:.3f});')
    add(f'tl.to(".t2",{{x:-1150,rotation:-6,duration:.32,ease:"power3.in"}},{L[1] + .1:.3f});')
    setv("#s-pay", L[1] + .3, "opacity:0")
    # repo
    setv("#s-repo", L[3] + .01, "opacity:1")
    pop(".repo-t", L[3], "y:30,opacity:0", .3)
    pop(".repo-row", L[3] + .25, "y:20,opacity:0", .3)
    pop(".quote", T["x"][0] - .1, "y:30,opacity:0", .35)
    setv("#s-repo", L[4] - .05, "opacity:0")
    # coach
    add(f'tl.fromTo("#s-coach",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.3,ease:"power3.out",immediateRender:false}},{L[4] - .05:.3f});')
    pop(".cp1", L[4] + .05, "scale:.5,opacity:0", .25)
    pop(".cp2", T["coachClaude"] + .1, "scale:.5,opacity:0", .3)
    pop(".cdesc", L[4] + .1, "opacity:0,y:10", .25)
    pop(".goal-l", L[4] + .15, "opacity:0,y:10", .2)
    pop(".goalbox", L[4] + .15, "opacity:0,y:10", .2)
    pop(".cbtn", L[4] + .2, "opacity:0,y:20", .25)
    add(f'tl.to(".goalbox .ph",{{opacity:0,duration:.12}},{T["g"][0] - .08:.3f});')
    for i, t in enumerate(T["g"]):
        pop(f".gc{i}", t, "scale:.3,opacity:0,y:20", .3, "back.out(3)")
    add(f'tl.to(".cbtn",{{scale:.92,duration:.08,yoyo:true,repeat:1}},{L[6] + .05:.3f});')
    add(f'tl.to(".cdesc, .goal-l, .goalbox, .cbtn",{{opacity:0,y:-20,duration:.2}},{L[6] + .2:.3f});')
    for i in range(4):
        pop(f".wr{i}", L[6] + .35 + i * .22, "x:80,opacity:0", .3, "back.out(2)")
    pop(".abtn", L[6] + .9, "opacity:0,y:20", .3)
    add(f'tl.to(".abtn",{{opacity:0,scale:.9,duration:.1}},{T["approve"] - .02:.3f});')
    pop(".abtn2", T["approve"], "scale:1.6,opacity:0", .25, "back.out(2.5)")
    setv("#s-coach", L[7] - .05, "opacity:0")
    # train
    add(f'tl.fromTo("#s-train",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.3,ease:"power3.out",immediateRender:false}},{L[7] - .05:.3f});')
    reps = int((L[8] - L[7]) / .5) + 1
    add(f'tl.fromTo(".fa",{{rotation:0}},{{rotation:130,duration:.5,yoyo:true,repeat:{reps},ease:"sine.inOut",immediateRender:false}},{L[7]:.3f});')
    add('(()=>{const o={v:0};tl.to(o,{v:5632,duration:%.2f,ease:"power2.out",onUpdate:()=>{document.querySelector(".cnt").textContent=Math.round(o.v).toLocaleString("en-US");}},%.3f);})();'
        % (max(.4, T["demosEnd"] - T["demos"] + .2), T["demos"]))
    pop(".sr0", T["weights"], "x:-60,opacity:0", .3)
    pop(".sr1", T["weights"] + .18, "x:-60,opacity:0", .3)
    pop(".next", T["ready"] - .1, "scale:.5,opacity:0,y:30", .35, "back.out(2.6)")
    # step chip
    pop(".step1", L[4] - .05, "opacity:0,y:-20", .3)
    out(".step1", L[7] - .2, .15)
    pop(".step2", L[7] - .05, "opacity:0,y:-20", .3)
    out(".step2", L[8] - .1, .15)


# ---------------------------------------------------------------- end card
def endcard():
    return ('<div id="endc"><div class="ec-1">Comment</div><div class="ec-gym"><span class="ty ty0">G</span><span class="ty ty1">Y</span>'
            '<span class="ty ty2">M</span><i class="cur"></i></div><div class="ec-2">for the links + my Claude prompt</div>'
            '<div class="ec-3">Send this to your gym buddy who still pays for an app</div><div class="ec-h mono">✦ @ai.nxtlvl</div></div>'
            '<div id="dm"><div class="dmav">✦</div><div class="tbody"><div class="thead"><b>ai.nxtlvl</b><span>now</span></div>'
            '<div class="ttext">Sent you the openGym links + the Claude prompt</div></div><div class="dmok">✓</div></div>')


def endcard_tl():
    a = T["gym"] - .05
    pop("#endc", a - .1, "opacity:0,scale:.9,y:40", .35, "back.out(1.8)")
    pop(".ec-1", a - .05, "y:20,opacity:0", .25)
    pop(".ec-gym", a - .02, "scale:.6,opacity:0", .3, "back.out(2.2)")
    for i in range(3):                                    # typed in, letter by letter
        pop(f".ty{i}", a + .12 + i * .13, "opacity:0,y:-30,scale:1.4", .16, "back.out(3)")
    add(f'tl.fromTo(".cur",{{opacity:1}},{{opacity:0,duration:.22,yoyo:true,repeat:{int((DUR - a) / .44)},ease:"steps(1)",immediateRender:false}},{a:.3f});')
    pop(".ec-2", a + .3, "y:20,opacity:0", .3)
    pop(".ec-3", a + .7, "y:20,opacity:0", .35)
    pop(".ec-h", a + 1.0, "y:20,opacity:0", .3)
    add(f'tl.to(".ec-gym",{{scale:.94,duration:.09,yoyo:true,repeat:1,ease:"power2.out"}},{VOICE_END - .05:.3f});')   # sent
    pop("#dm", VOICE_END + .1, "y:60,opacity:0,scale:.9", .38, "back.out(2)")
    pop(".dmok", VOICE_END + .45, "scale:0,opacity:0", .3, "back.out(3)")


# ---------------------------------------------------------------- captions: 2-3 words at a time, the spoken word lit
# One fixed place, the lower third (y 1330, above the platform UI), on a dark glass box so no 3D background can wash them
# out; Montserrat ExtraBold; the spoken word sits on a violet pill. The speaker dot says who talks (grey human, violet NXT).
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
            html.append(f'<div class="cap {ln["speaker"]}" id="{cid}"><span class="box"><i class="dot"></i>{spans.strip()}</span></div>')
            a = ch[0]["s"] - .05
            z = chunks[ci + 1][0]["s"] - .05 if ci + 1 < len(chunks) else min(ln["end"] + .35, nxt_line - .06)
            add(f'tl.fromTo("#{cid}",{{opacity:0,y:18,scale:.94}},{{opacity:1,y:0,scale:1,duration:.14,ease:"back.out(2)",immediateRender:false}},{a:.3f});')
            add(f'tl.set("#{cid}",{{opacity:0}},{z:.3f});')
            for k, w in enumerate(ch):
                add(f'tl.set("#{cid}_{k}",{{backgroundColor:"#7B2FFB",color:"#ffffff"}},{w["s"]:.3f});')
                add(f'tl.set("#{cid}_{k}",{{backgroundColor:"rgba(123,47,251,0)",color:"#EDE8F7"}},{w["e"] + .02:.3f});')
    return "".join(html)


MM = "".join(f'<div class="mm mm{i}"><i></i>{s}</div>' for i, s in enumerate(["WORKED", "RECOVERING", "UNTRAINED"]))


def mm_tl():
    for i, k in enumerate(("worked", "recovering", "untrained")):
        pop(f".mm{i}", T[k], "x:-80,opacity:0,scale:.7", .3, "back.out(2.4)")
    add(f'tl.to(".mm2",{{scale:1.08,duration:.18,yoyo:true,repeat:5,ease:"sine.inOut"}},{T["untrained"] + .35:.3f});')
    out(".mm", L[10] - .05, .2)


def fx_tl():
    for t in (L[2], L[8], L[10]):
        add(f'tl.set("#whip",{{opacity:.8,x:300}},{t - .04:.3f});tl.to("#whip",{{opacity:0,x:-300,duration:.22,ease:"power2.out"}},{t - .03:.3f});')
    for t, o in ((L[1] - .12, .4), (T["free"] - .02, .35), (T["approve"], .2), (T["untrained"], .15)):
        add(f'tl.set("#flash",{{opacity:{o}}},{t:.3f});tl.to("#flash",{{opacity:0,duration:.35}},{t + .02:.3f});')
    add(f'tl.fromTo(".prog i",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none",immediateRender:false}},0);')


CSS = """
@font-face { font-family: "Poppins"; font-weight: 600; src: url("assets/fonts/poppins-600.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }
@font-face { font-family: "Lora"; font-style: italic; font-weight: 400 700; src: url("assets/fonts/lora-italic.ttf"); }
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #07050d; }
body { font-family: "Poppins", sans-serif; color: #f4f1fa; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #07050d; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
#ui { z-index: 5; perspective: 1400px; }
.top { position: absolute; left: 60px; right: 60px; top: 262px; display: flex; align-items: center; gap: 24px; }
.brand { font-size: 28px; letter-spacing: 5px; color: #f4f1fa; text-shadow: 0 2px 12px rgba(0,0,0,.6); }
.brand b { color: #7b2ffb; }
.prog { flex: 1; height: 6px; border-radius: 3px; background: rgba(244,241,250,.18); overflow: hidden; }
.prog i { display: block; height: 100%; background: linear-gradient(90deg, #7b2ffb, #a98bff); transform-origin: 0 50%; transform: scaleX(0); }
.step { position: absolute; left: 60px; top: 316px; padding: 6px 22px; border-radius: 22px; font: 700 28px "JBMono"; letter-spacing: 3px;
  background: #7b2ffb; color: #fff; box-shadow: 0 8px 28px rgba(123,47,251,.55); opacity: 0; }
#panel { position: absolute; left: 60px; top: 380px; width: 960px; height: 560px; border-radius: 36px; overflow: hidden;
  background: linear-gradient(160deg, rgba(42,22,82,.72), rgba(14,8,30,.78)); border: 2px solid rgba(169,139,255,.38);
  -webkit-backdrop-filter: blur(22px) saturate(1.3); backdrop-filter: blur(22px) saturate(1.3);
  box-shadow: 0 30px 80px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.12); transform-origin: 50% 0%; }
/* everything that pops in later starts hidden here, never through a set at t=0 */
.repo-t, .repo-row, .cp1, .cp2, .cdesc, .goal-l, .goalbox, .ec-1, .ec-gym, .ec-2, .ec-3, .ec-h, .mm { opacity: 0; }
.scr { position: absolute; inset: 0; padding: 34px 44px; opacity: 0; }
#panel { opacity: 0; }
.toast, #dm { position: absolute; left: 60px; right: 60px; min-height: 136px; border-radius: 36px; display: flex; align-items: center; gap: 24px;
  padding: 20px 30px; background: rgba(28,22,40,.88); border: 1px solid rgba(255,255,255,.14); -webkit-backdrop-filter: blur(24px);
  backdrop-filter: blur(24px); box-shadow: 0 24px 60px rgba(0,0,0,.5); }
.t1 { top: 330px; } .t2 { top: 490px; opacity: 0; }
.ticon, .dmav { flex: none; width: 84px; height: 84px; border-radius: 22px; background: linear-gradient(160deg, #ff5a6a, #c0142d);
  display: flex; align-items: center; justify-content: center; font: 800 44px "Poppins"; color: #fff; }
.tbody { flex: 1; min-width: 0; }
.thead { display: flex; align-items: baseline; justify-content: space-between; }
.thead b { font: 700 32px "Poppins"; color: #fff; }
.thead span { font: 600 26px "Poppins"; color: rgba(244,241,250,.55); }
.ttext { font: 600 30px/1.3 "Poppins"; color: #e4dcf5; margin-top: 4px; }
#dm { top: 1130px; opacity: 0; }
.dmav { border-radius: 50%; background: linear-gradient(160deg, #a98bff, #7b2ffb); font-size: 40px; }
.dmok { flex: none; width: 56px; height: 56px; border-radius: 50%; background: #3fd69b; color: #07050d; display: flex; align-items: center;
  justify-content: center; font: 800 32px "Poppins"; opacity: 0; }
.ty { display: inline-block; opacity: 0; }
.cur { display: inline-block; width: 10px; height: 118px; margin-left: 10px; vertical-align: -10px; border-radius: 5px; background: #fff; }
.appbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.appname { font: 800 40px "Poppins"; letter-spacing: -1px; }
.pill { display: inline-block; padding: 6px 18px; border-radius: 20px; font: 700 28px "JBMono"; letter-spacing: 1px; }
.pill.red { background: #ff4458; color: #fff; }
.pill.vio { background: rgba(123,47,251,.85); color: #fff; }
.pill.grn { background: rgba(63,214,155,.18); color: #3fd69b; border: 2px solid #3fd69b; }
.pill.gold { background: rgba(255,194,74,.16); color: #ffc24a; border: 2px solid #ffc24a; }
.paylock { position: absolute; right: 60px; top: 110px; font-size: 110px; }
.ptitle { font: 800 72px/1.05 "Poppins"; color: #fff; letter-spacing: -2px; margin-top: 10px; }
.psub { font: 600 32px "Poppins"; color: #ffb3bb; margin: 4px 0 12px; }
.pl { font: 600 30px "Poppins"; color: rgba(244,241,250,.7); padding: 3px 0; }
.pbtn { position: absolute; left: 44px; right: 44px; bottom: 36px; height: 84px; border-radius: 42px; background: linear-gradient(90deg, #ff4458, #c0142d);
  display: flex; align-items: center; justify-content: center; font: 800 38px "Poppins"; box-shadow: 0 10px 34px rgba(255,68,88,.5); }
.repo-h { font-size: 30px; color: #a98bff; letter-spacing: 0; }
.repo-h b { color: #fff; }
.repo-t { font: 800 84px/1.05 "Poppins"; letter-spacing: -3px; margin-top: 8px; color: #fff; }
.repo-d { font: 600 36px "Poppins"; color: #d9ccff; }
.repo-row { display: flex; gap: 16px; margin-top: 16px; }
.quote { position: absolute; left: 44px; right: 44px; bottom: 26px; padding: 16px 26px; border-radius: 24px; background: rgba(7,5,13,.45);
  border-left: 6px solid #3fd69b; font: italic 500 32px/1.28 "Lora"; color: #f4f1fa; opacity: 0; }
.quote span { display: block; margin-top: 4px; font-size: 26px; letter-spacing: 3px; color: #a98bff; font-style: normal; }
.crow { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.clab { font-size: 28px; letter-spacing: 2px; color: #a98bff; }
.cdesc { margin-top: 16px; font: italic 500 34px/1.25 "Lora"; color: #d9ccff; }
.goal-l { margin-top: 18px; }
.goalbox { position: relative; }
.goalbox .ph { position: absolute; left: 26px; top: 50%; transform: translateY(-50%); color: rgba(217,204,255,.5); font: 600 30px "Poppins"; }
.mm { position: absolute; left: 60px; display: flex; align-items: center; gap: 16px; padding: 12px 30px 12px 22px; border-radius: 40px;
  background: rgba(7,5,13,.78); border: 3px solid var(--c); color: var(--c); font: 800 44px "Poppins"; box-shadow: 0 10px 34px rgba(0,0,0,.4); }
.mm i { width: 22px; height: 22px; border-radius: 50%; background: var(--c); box-shadow: 0 0 16px var(--c); }
.mm0 { --c: #3fd69b; top: 990px; } .mm1 { --c: #ffc24a; top: 1085px; } .mm2 { --c: #ff6b6b; top: 1180px; }
.goalbox { margin-top: 12px; min-height: 92px; border-radius: 24px; border: 2px dashed rgba(169,139,255,.5); padding: 14px; display: flex; gap: 14px; }
.gchip { padding: 12px 24px; border-radius: 30px; background: rgba(63,214,155,.16); border: 2px solid #3fd69b; color: #fff; font: 700 32px "Poppins"; opacity: 0; }
.cbtn { margin-top: 22px; height: 84px; border-radius: 42px; background: linear-gradient(90deg, #7b2ffb, #a98bff); display: flex; align-items: center;
  justify-content: center; font: 800 38px "Poppins"; box-shadow: 0 10px 34px rgba(123,47,251,.5); opacity: 0; }
.week { position: absolute; left: 44px; right: 44px; top: 170px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.wr { height: 92px; border-radius: 22px; background: rgba(244,241,250,.08); border: 2px solid rgba(169,139,255,.45); display: flex; align-items: center;
  gap: 18px; padding: 0 24px; font: 700 36px "Poppins"; opacity: 0; }
.wr b { font: 700 28px "JBMono"; color: #a98bff; letter-spacing: 2px; }
.abtn, .abtn2 { position: absolute; left: 44px; right: 44px; bottom: 40px; height: 84px; border-radius: 42px; display: flex; align-items: center;
  justify-content: center; font: 800 36px "Poppins"; opacity: 0; }
.abtn { background: rgba(244,241,250,.12); border: 2px solid rgba(244,241,250,.4); }
.abtn2 { background: #3fd69b; color: #07050d; font-size: 32px; box-shadow: 0 10px 34px rgba(63,214,155,.45); }
.tx { display: flex; gap: 30px; align-items: center; }
.demo { position: relative; width: 170px; height: 170px; border-radius: 28px; background: rgba(7,5,13,.55); border: 2px solid rgba(169,139,255,.35);
  display: flex; align-items: center; justify-content: center; }
.ename { font: 800 50px "Poppins"; letter-spacing: -1px; }
.lib { font: 600 30px "Poppins"; color: #d9ccff; margin-top: 6px; }
.lib b { font: 800 44px "Poppins"; color: #fff; }
.sets { margin-top: 22px; display: flex; flex-direction: column; gap: 12px; }
.srow { display: flex; align-items: center; gap: 22px; height: 64px; border-radius: 20px; padding: 0 24px; background: rgba(244,241,250,.08); opacity: 0; }
.srow span { font: 700 28px "JBMono"; color: #a98bff; letter-spacing: 2px; }
.srow b { font: 800 34px "Poppins"; }
.srow em { margin-left: auto; font: 700 28px "Poppins"; font-style: normal; color: #3fd69b; }
.next { position: absolute; right: 44px; bottom: 22px; display: flex; align-items: center; gap: 16px; padding: 6px 26px; border-radius: 30px;
  background: #3fd69b; color: #07050d; opacity: 0; box-shadow: 0 10px 34px rgba(63,214,155,.45); }
.next span { font: 700 28px "Poppins"; } .next b { font: 800 38px "Poppins"; } .next i { font: 800 30px "Poppins"; font-style: normal; }
#caps { z-index: 6; }
.cap { position: absolute; left: 50px; right: 50px; top: 1330px; text-align: center; opacity: 0; }
.cap .box { display: inline-block; max-width: 980px; padding: 14px 22px 16px; border-radius: 28px; background: rgba(10,6,20,.84);
  border: 1px solid rgba(169,139,255,.3);
  box-shadow: 0 14px 40px rgba(0,0,0,.45); font: 800 60px/1.15 "Montserrat"; letter-spacing: -.5px; color: #EDE8F7; }
.cap .w { display: inline-block; padding: 2px 12px 4px; border-radius: 16px; }
.cap .dot { display: inline-block; width: 18px; height: 18px; border-radius: 50%; margin: 0 6px 0 4px; vertical-align: 10px; background: #9a98a6; }
.cap.nxt .dot { background: #a98bff; box-shadow: 0 0 14px #a98bff; }
#endc { position: absolute; left: 60px; right: 60px; top: 330px; padding: 44px 40px 40px; border-radius: 40px; text-align: center;
  background: linear-gradient(160deg, rgba(42,22,82,.8), rgba(14,8,30,.85)); border: 2px solid rgba(169,139,255,.45);
  -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px); box-shadow: 0 30px 80px rgba(0,0,0,.5); opacity: 0; }
.ec-1 { font: 700 52px "Poppins"; }
.ec-gym { display: inline-block; margin: 12px 0 8px; padding: 6px 60px; border-radius: 40px; background: linear-gradient(90deg, #7b2ffb, #a98bff);
  font: 800 150px/1.1 "Poppins"; letter-spacing: 4px; color: #fff; box-shadow: 0 16px 50px rgba(123,47,251,.6); }
.ec-2 { font: 700 46px "Poppins"; color: #f4f1fa; }
.ec-3 { margin-top: 22px; font: italic 500 35px "Lora"; color: #d9ccff; }
.ec-h { margin-top: 18px; font-size: 30px; color: #a98bff; letter-spacing: 3px; }
#fx { z-index: 7; }
#flash { position: absolute; inset: 0; background: #efe6ff; opacity: 0; }
#whip { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(90deg, rgba(255,255,255,0) 0 22px,
  rgba(217,204,255,.5) 22px 26px, rgba(255,255,255,0) 26px 70px); }
#vig { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(7,5,13,.55) 0%, rgba(7,5,13,0) 18%, rgba(7,5,13,0) 70%, rgba(7,5,13,.5) 100%); }
"""


def main():
    scr = screens()
    screens_tl()
    endc = endcard()
    endcard_tl()
    caps = captions()
    mm_tl()
    fx_tl()
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>openGym x Claude 9x16</title>
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
        <div class="step step1">STEP 1/2 · CLAUDE COACH</div><div class="step step2">STEP 2/2 · TRAIN</div>
        {TOASTS}<div id="panel">{scr}</div>{endc}{MM}
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{caps}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-ignore><div id="whip"></div><div id="flash"></div></div>
      <audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.OG_T = {json.dumps(T)};
      window.OG_ENV = {json.dumps(ENV, separators=(",", ":"))};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/opengym.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(T, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s")


if __name__ == "__main__":
    main()
