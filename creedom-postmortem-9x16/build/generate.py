"""Creedom remake 1, "The 304-view post-mortem" (Creators 100X, 9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

Built on .claude/skills/nxtlvl-social-video/references/reach-psychology.md after the original explainer flatlined
(304 views, 5 s average watch). Script: creedom-explainer-9x16/plan/script_remake_v2.md.
Frame 1 is the real insights card (own-flop post-mortem hook); the old reel's opening plays under a timer to show where
the average viewer left; the lesson; a callback to this reel's own timer; Creedom only at about 65 %, in its pink world;
the CTA (CREE) and a cut back to the 304 card so the reel loops. Native-looking caption pills, karaoke captions.
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
SCRIPT = json.load(open(os.path.join(ROOT, "plan", "script.json")))
LW = {}
for w in W:
    LW.setdefault(w["line"], []).append(w)
JS, SFX, HTML = [], [], []
PINK, INK = "#ff3d8b", "#16121a"


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


def wt(line, word, n=0):
    hits = [w for w in LW[line] if re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(word.lower())]
    if not hits:
        raise SystemExit(f"{line}: no word starting {word!r}")
    return hits[min(n, len(hits) - 1)]["t0"]


IDS = [ln["id"] for ln in SCRIPT]
L = {i: (LW[i][0]["t0"], LW[i][-1]["t1"]) for i in IDS}
S = [L[i][0] for i in IDS] + [L[IDS[-1]][1] + 1.2]
DUR = round(S[-1], 2)

# ---- top caption pills (native "classic" text: dark type on white rounded boxes), one per line
PILLS = ["304 views.", "It was about why people<br>stop watching.", "Average watch: <b>5 seconds</b>",
         "That's my first sentence.", "Problem first.<br>Tool last.", '<span id="clock">0:00</span> and no app name yet',
         "It's <b>Creedom</b>.", 'Comment <b>CREE</b>']
for k, (lid, txt) in enumerate(zip(IDS, PILLS)):
    HTML.append(f'<div class="pill{" big" if k == 0 else ""}" id="p{k}"><span>{txt}</span></div>')
    a, b = S[k], S[k + 1]
    ft(f"#p{k}", a - .06, .3, "{opacity: 0, y: 24, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.2)")
    if k < len(IDS) - 1:
        to(f"#p{k}", b - .12, .12, "{opacity: 0, y: -16}", "power2.in")
# the live clock on the callback line shows this reel's own elapsed time
js(f'(() => {{ const o = {{v: {S[5]:.3f}}}; tl.to(o, {{v: {S[6]:.3f}, duration: {S[6] - S[5]:.3f}, ease: "none", onUpdate: () => {{ const s = Math.floor(o.v); '
   f'document.getElementById("clock").textContent = "0:" + String(s).padStart(2, "0"); }}}}, {S[5]:.3f}); }})();')

# ---- scene 1-3: the real insights card, the old cover, the 5 s ring
HTML.append('<div id="ins"><img src="assets/img/insights_cards.jpg" alt=""><i class="ring" id="r304"></i><i class="ring" id="r5"></i></div>')
HTML.append('<div id="old"><img src="assets/img/old_cover.png" alt=""><i class="hide"></i><b class="tape" id="irony">the irony</b></div>')   # the old wordmark is blurred: no product name before the reveal
HTML.append('<div id="t5"><b id="t5n">0</b><span>s</span></div>')
st("#ins", 0, "{opacity: 1}")
ft("#ins", 0, .5, "{scale: 1.08, y: 20}", "{scale: 1, y: 0}", "power3.out")
ft("#r304", .25, .35, "{opacity: 0, scale: 1.3}", "{opacity: 1, scale: 1}", "back.out(2)")
sfx("impact", .02)
sfx("pop", .3)
# f01: the old cover slams in beside it; record scratch on "stop watching"
a1 = S[1]
to("#ins", a1 - .05, .4, "{x: -150, y: -40, scale: .78, rotation: -3, opacity: .55}", "power3.out")
ft("#old", a1 + .05, .45, "{opacity: 0, x: 420, rotation: 18, scale: .7}", "{opacity: 1, x: 0, rotation: 5, scale: 1}", "back.out(1.6)")
sfx("whoosh", a1)
tsw = wt("f01", "stop")
ft("#irony", tsw - .05, .3, "{opacity: 0, scale: 1.8, rotation: -20}", "{opacity: 1, scale: 1, rotation: -8}", "back.out(2.4)")
sfx("screech", tsw - .1)
sfx("thump", tsw)
# f02: the cover leaves, the 5 s card comes back with its ring and a counting timer
a2 = S[2]
to("#old", a2 - .1, .35, "{opacity: 0, x: 500, rotation: 25}", "power2.in")
to("#ins", a2, .45, "{x: 0, y: 0, scale: 1, rotation: 0, opacity: 1}", "power3.out")
to("#r304", a2, .2, "{opacity: 0}")
tfive = wt("f02", "five")
ft("#r5", tfive - .1, .35, "{opacity: 0, scale: 1.3}", "{opacity: 1, scale: 1}", "back.out(2)")
ft("#t5", tfive - .05, .35, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2.5)")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 5, duration: .6, ease: "steps(5)", onUpdate: () => {{ document.getElementById("t5n").textContent = Math.round(o.v); }}}}, {tfive:.3f}); }})();')
sfx("pop", tfive)
for k in range(5):
    sfx("tick", tfive + k * .12)

# ---- scene 4: the old reel's first sentence plays under a timer, then freezes where the average viewer left
a3 = S[3]
tq = wt("f03", "this")                    # the quote starts: play the old opening from 0 with it
OLD_LEN = 4.4
HTML.append(f'<div id="phone"><video id="ov" src="assets/video/old_open.mp4" data-start="{tq - .1:.3f}" data-duration="{OLD_LEN:.2f}" data-track-index="1" muted playsinline></video>'
            '<img id="ofz" src="assets/img/old_freeze.jpg" alt=""><div id="otm"><span id="otn">0.0</span>s</div><b class="stamp" id="left">THEY LEFT HERE</b></div>')
to("#ins", a3 - .1, .3, "{opacity: 0, y: -60, scale: .9}", "power2.in")
to("#t5", a3 - .1, .3, "{opacity: 0, scale: .6}", "power2.in")
ft("#phone", a3 - .05, .4, "{opacity: 0, y: 120, scale: .85}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.5)")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 4.3, duration: {OLD_LEN - .1:.2f}, ease: "none", onUpdate: () => {{ document.getElementById("otn").textContent = o.v.toFixed(1); }}}}, {tq - .1:.3f}); }})();')
tfz = tq - .1 + OLD_LEN
st("#ofz", tfz - .05, "{opacity: 1}")
ft("#left", tfz, .3, "{opacity: 0, scale: 2, rotation: -16}", "{opacity: 1, scale: 1, rotation: -8}", "power4.in")
ft("#phone", tfz + .2, .25, "{x: 0}", "{keyframes: [{x: -8, duration: .05}, {x: 8, duration: .05}, {x: 0, duration: .15}]}", "none")
sfx("whoosh", a3 - .1)
sfx("typing", tq)
sfx("stamp", tfz + .18)
to("#phone", S[4] - .12, .25, "{opacity: 0, y: -80, scale: .9}", "power2.in")

# ---- scene 5: the lesson, the TOOL and PROBLEM cards swap order
a4 = S[4]
HTML.append('<div id="swap"><div class="card" id="cTool"><i>1</i><b>TOOL</b><span>"This AI told me..."</span></div>'
            '<div class="card hot" id="cProb"><i>2</i><b>PROBLEM</b><span>"Your reel lost them at 0:05"</span></div></div>')
ft("#swap", a4 - .05, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.6)")
tpf = wt("f04", "problem")
to("#cTool", tpf - .05, .5, "{y: 250, rotation: -2}", "back.out(1.4)")
to("#cProb", tpf - .05, .5, "{y: -250, rotation: 2}", "back.out(1.4)")
st("#cTool i", tpf + .2, '{textContent: "2"}')
st("#cProb i", tpf + .2, '{textContent: "1"}')
sfx("whoosh", tpf - .1)
sfx("ding", tpf + .35)
to("#swap", S[5] - .12, .2, "{opacity: 0, scale: .9}", "power2.in")

# ---- scene 6: the callback, this reel's own clock ticking
a5 = S[5]
HTML.append('<div id="bigclock"><div class="dial"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="trk"/><circle cx="100" cy="100" r="86" class="arc" id="arc"/></svg>'
            '<b id="clock2">0:00</b></div><div class="nope"><span>APP NAME</span><i>?</i></div></div>')
ft("#bigclock", a5 - .05, .4, "{opacity: 0, scale: .7}", "{opacity: 1, scale: 1}", "back.out(1.8)")
js(f'(() => {{ const o = {{v: {a5:.3f}}}; tl.to(o, {{v: {S[6]:.3f}, duration: {S[6] - a5:.3f}, ease: "none", onUpdate: () => {{ const s = Math.floor(o.v); '
   f'document.getElementById("clock2").textContent = "0:" + String(s).padStart(2, "0"); }}}}, {a5:.3f}); }})();')
ft("#arc", a5, S[6] - a5, "{strokeDashoffset: 540}", "{strokeDashoffset: 120}", "none")
for k in range(int(S[6] - a5)):
    sfx("tick", a5 + k + .02)
to("#bigclock", S[6] - .15, .2, "{opacity: 0, scale: 1.2}", "power2.in")

# ---- scene 7: Creedom reveal in its pink world, the analyser card, Cree with the magnifier
a6 = S[6]
HTML.append('<div id="world"><i class="bl b1"></i><i class="bl b2"></i><i class="bl b3"></i></div>')
HTML.append('<div id="an"><div class="anh"><img src="assets/img/creedom_logo.png" alt=""><span>REEL ANALYZER</span></div>'
            '<div class="chart"><svg viewBox="0 0 600 260" preserveAspectRatio="none"><path id="ret" d="M0,40 C60,42 90,46 110,52 C130,60 140,160 160,190 C200,215 300,222 600,230" fill="none" stroke="#ff3d8b" stroke-width="7" stroke-linecap="round"/></svg>'
            '<i id="drop"></i><b id="dropl">viewers left at 0:05</b></div>'
            '<div class="why"><b>WHY</b><span>The hook names a tool. It never shows the viewer\'s problem.</span></div></div>')
HTML.append('<img id="cree" src="assets/img/poses/mag.png" alt="">')
ft("#world", a6 - .2, .5, "{opacity: 0}", "{opacity: 1}", "power2.out")
ft("#an", a6, .5, "{opacity: 0, y: 80, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.5)")
js(f'tl.fromTo("#ret", {{strokeDasharray: 900, strokeDashoffset: 900}}, {{strokeDashoffset: 0, duration: .9, ease: "power2.out", immediateRender: false}}, {a6 + .4:.3f});')
tex = wt("f06", "exact")
ft("#drop", tex - .1, .3, "{opacity: 0, scale: 0}", "{opacity: 1, scale: 1}", "back.out(3)")
ft("#dropl", tex, .3, "{opacity: 0, y: 14}", "{opacity: 1, y: 0}")
ft(".why", wt("f06", "why") - .15, .35, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}")
ft("#cree", a6 + .3, .5, "{opacity: 0, x: 200, rotation: 12}", "{opacity: 1, x: 0, rotation: 0}", "back.out(1.6)")
sfx("whoosh_big", a6 - .2)
sfx("sparkle", a6 + .1)
sfx("pop", tex - .05)

# ---- scene 8: CTA, comment box types CREE, share sticker, then the cut back to frame 1 (loop)
a7 = S[7]
HTML.append('<div id="cta"><div class="share"><b>&#10148;</b><span>send to the friend whose reels keep flopping</span></div>'
            '<div class="cbox"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div></div>')
to("#an", a7 - .1, .3, "{y: -60, scale: .86, opacity: .9}", "power2.out")
ft("#cta", a7, .4, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(1.6)")
st("#cree", a7, '{attr: {src: "assets/img/poses/wave.png"}}')
tc = wt("f07", "comment")
st("#cph", tc + .1, "{opacity: 0}")
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 4, duration: .45, ease: "steps(4)", onUpdate: () => {{ document.getElementById("cty").textContent = "CREE".slice(0, Math.round(o.n)); }}}}, {tc + .1:.3f}); }})();')
sfx("whoosh", a7 - .1)
sfx("typing", tc + .1)
sfx("click", tc + .65)
sfx("notify", tc + .85)
tl_end = DUR - .4
st("#loop", tl_end, "{opacity: 1}")
HTML.append('<div id="loop"><img src="assets/img/insights_cards.jpg" alt=""></div>')

# ---- karaoke captions
CAP = []
for ln in SCRIPT:
    disp, ws = ln["display"].replace('"', "").split(), LW[ln["id"]]
    n, m = len(disp), len(ws)
    timed = []
    for i, dw in enumerate(disp):
        j = i if n == m else round(i * (m - 1) / max(1, n - 1))
        timed.append((dw, ws[j]["t0"], ws[min(m - 1, j)]["t1"]))
    chunk = []
    for i, x in enumerate(timed):
        chunk.append(x)
        if len(chunk) >= 5 or x[0][-1] in ".,?!" and len(chunk) >= 2 or i == len(timed) - 1:
            CAP.append(chunk); chunk = []
for ci, chunk in enumerate(CAP):
    spans = " ".join(f'<span class="cw" id="c{ci}_{k}">{w}</span>' for k, (w, _, _) in enumerate(chunk))
    HTML.append(f'<div class="cap" id="cap{ci}">{spans}</div>')
    t0, t1 = chunk[0][1], chunk[-1][2]
    nxt = CAP[ci + 1][0][1] if ci + 1 < len(CAP) else DUR
    st(f"#cap{ci}", t0 - .06, "{opacity: 1}")
    st(f"#cap{ci}", min(nxt - .08, t1 + .8), "{opacity: 0}")
    for k, (_, a, _) in enumerate(chunk):
        st(f"#c{ci}_{k}", a - .03, f"{{color: '{INK}'}}")

CSS = f"""
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #f4f1ec; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: {INK};
  background: radial-gradient(70% 40% at 80% 20%, rgba(255,61,139,.10), rgba(0,0,0,0)), radial-gradient(60% 40% at 10% 85%, rgba(140,90,255,.08), rgba(0,0,0,0)), #f4f1ec; }}
#grain {{ position: absolute; inset: 0; background: url(assets/img/grain.png); opacity: .05; mix-blend-mode: multiply; pointer-events: none; z-index: 60; }}
.pill {{ position: absolute; left: 0; right: 0; top: 300px; text-align: center; opacity: 0; z-index: 30; }}
.pill span {{ display: inline; background: #fff; padding: 10px 22px; border-radius: 18px; font-weight: 800; font-size: 54px; line-height: 1.5;
  letter-spacing: -.02em; box-decoration-break: clone; -webkit-box-decoration-break: clone; box-shadow: 0 8px 24px rgba(22,18,26,.10); }}
.pill.big span {{ font-size: 96px; padding: 8px 30px; }}
.pill b {{ color: {PINK}; }}
#ins {{ position: absolute; left: 70px; right: 70px; top: 640px; opacity: 0; border-radius: 34px; overflow: hidden; background: #0d0f14;
  box-shadow: 0 30px 70px rgba(22,18,26,.28); z-index: 10; }}
#ins img {{ display: block; width: 100%; }}
.ring {{ position: absolute; border: 7px solid {PINK}; border-radius: 26px; opacity: 0; box-shadow: 0 0 30px rgba(255,61,139,.6); }}
#r304 {{ left: 22px; top: 2px; width: 440px; height: 196px; }}
#r5 {{ left: 22px; top: 204px; width: 440px; height: 196px; }}
#old {{ position: absolute; left: 470px; top: 560px; width: 480px; opacity: 0; z-index: 12; }}
#old img {{ width: 100%; border-radius: 30px; box-shadow: 0 30px 70px rgba(22,18,26,.3); display: block; }}
.hide {{ position: absolute; left: 22%; right: 22%; top: 83%; height: 8%; border-radius: 16px; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); background: rgba(255,220,236,.55); }}
.tape {{ position: absolute; left: -90px; top: 60px; background: #ffd23f; color: {INK}; font-weight: 800; font-size: 46px; padding: 10px 26px; opacity: 0;
  box-shadow: 0 10px 24px rgba(0,0,0,.18); font-family: Serif; font-style: italic; font-weight: 400; font-size: 60px; }}
#t5 {{ position: absolute; right: 90px; top: 1130px; width: 220px; height: 220px; border-radius: 50%; background: {PINK}; color: #fff; display: grid;
  place-items: center; grid-auto-flow: column; justify-content: center; align-items: baseline; padding-top: 52px; opacity: 0; z-index: 14;
  box-shadow: 0 20px 50px rgba(255,61,139,.45); font-weight: 800; }}
#t5 b {{ font-size: 110px; line-height: 1; }} #t5 span {{ font-size: 54px; }}
#phone {{ position: absolute; left: 310px; top: 500px; width: 460px; height: 818px; border-radius: 46px; overflow: hidden; background: #000; opacity: 0;
  border: 10px solid #16121a; box-shadow: 0 40px 90px rgba(22,18,26,.35); z-index: 16; }}
#ov, #ofz {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#ofz {{ opacity: 0; filter: grayscale(.6) brightness(.8); }}
#otm {{ position: absolute; left: 50%; top: 24px; transform: translateX(-50%); background: rgba(22,18,26,.85); color: #fff; font-family: Mono; font-weight: 700;
  font-size: 40px; padding: 8px 22px; border-radius: 999px; }}
.stamp {{ position: absolute; left: 40px; right: 40px; top: 420px; text-align: center; border: 8px solid #ff2d55; color: #ff2d55; background: rgba(255,255,255,.9);
  font-weight: 800; font-size: 56px; letter-spacing: .04em; padding: 10px 0; border-radius: 18px; opacity: 0; }}
#swap {{ position: absolute; left: 110px; right: 110px; top: 640px; height: 640px; opacity: 0; z-index: 16; }}
.card {{ position: absolute; left: 0; right: 0; height: 220px; border-radius: 34px; background: #fff; box-shadow: 0 24px 60px rgba(22,18,26,.14);
  display: flex; flex-direction: column; justify-content: center; padding: 0 40px 0 150px; }}
.card i {{ position: absolute; left: 34px; top: 50%; margin-top: -48px; width: 96px; height: 96px; border-radius: 50%; background: #e9e4dc; display: grid;
  place-items: center; font-style: normal; font-weight: 800; font-size: 52px; }}
.card b {{ font-weight: 800; font-size: 64px; letter-spacing: -.02em; }}
.card span {{ font-family: Serif; font-style: italic; font-size: 40px; color: #6b6470; }}
#cTool {{ top: 60px; }} #cProb {{ top: 360px; }}
.card.hot {{ border: 5px solid {PINK}; }} .card.hot i {{ background: {PINK}; color: #fff; }}
#bigclock {{ position: absolute; left: 0; right: 0; top: 600px; display: flex; flex-direction: column; align-items: center; gap: 40px; opacity: 0; z-index: 16; }}
.dial {{ position: relative; width: 460px; height: 460px; }}
.dial svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
.trk {{ fill: #fff; stroke: #e6e0d8; stroke-width: 14; }}
.arc {{ fill: none; stroke: {PINK}; stroke-width: 14; stroke-linecap: round; stroke-dasharray: 540; }}
.dial b {{ position: absolute; inset: 0; display: grid; place-items: center; font-family: Mono; font-weight: 700; font-size: 130px; }}
.nope {{ display: flex; align-items: center; gap: 16px; background: #fff; padding: 16px 30px; border-radius: 22px; box-shadow: 0 14px 34px rgba(22,18,26,.12); }}
.nope span {{ font-family: Mono; font-weight: 700; font-size: 34px; letter-spacing: .14em; color: #8a8290; filter: blur(1.5px); }}
.nope i {{ font-style: normal; font-weight: 800; font-size: 56px; color: {PINK}; }}
#world {{ position: absolute; inset: 0; opacity: 0; z-index: 18; overflow: hidden;
  background: radial-gradient(120% 90% at 50% 30%, #ffffff 0%, #fbf0f6 55%, #f6e3ee 100%); }}
.bl {{ position: absolute; border-radius: 50%; filter: blur(90px); }}
.b1 {{ left: -160px; top: 200px; width: 620px; height: 620px; background: rgba(255,61,139,.35); }}
.b2 {{ right: -200px; top: 900px; width: 700px; height: 700px; background: rgba(160,100,255,.28); }}
.b3 {{ left: 200px; bottom: -200px; width: 600px; height: 500px; background: rgba(255,170,210,.4); }}
#an {{ position: absolute; left: 70px; right: 70px; top: 560px; opacity: 0; z-index: 20; border-radius: 40px; padding: 34px 36px 38px;
  background: linear-gradient(135deg, rgba(255,255,255,.88), rgba(255,255,255,.62)); border: 2px solid rgba(255,255,255,.95);
  box-shadow: 0 30px 80px rgba(160,20,90,.18); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); }}
.anh {{ display: flex; align-items: center; justify-content: space-between; }}
.anh img {{ height: 64px; }}
.anh span {{ font-family: Mono; font-weight: 700; font-size: 26px; letter-spacing: .16em; color: {PINK}; }}
.chart {{ position: relative; margin-top: 26px; height: 300px; border-radius: 24px; background: #fff; padding: 20px; }}
.chart svg {{ width: 100%; height: 100%; }}
#drop {{ position: absolute; left: 31%; top: 34%; width: 34px; height: 34px; border-radius: 50%; background: {PINK}; box-shadow: 0 0 0 10px rgba(255,61,139,.25); opacity: 0; }}
#dropl {{ position: absolute; left: 38%; top: 12%; background: {INK}; color: #fff; font-weight: 800; font-size: 32px; padding: 8px 18px; border-radius: 14px; opacity: 0; }}
.why {{ margin-top: 24px; display: flex; gap: 18px; align-items: baseline; opacity: 0; }}
.why b {{ font-family: Mono; font-weight: 700; font-size: 26px; letter-spacing: .14em; color: {PINK}; }}
.why span {{ font-weight: 700; font-size: 36px; line-height: 1.2; }}
#cree {{ position: absolute; right: 30px; top: 1010px; width: 300px; opacity: 0; z-index: 22; filter: drop-shadow(0 20px 30px rgba(160,20,90,.25)); }}
#cta {{ position: absolute; left: 70px; right: 70px; top: 1150px; opacity: 0; z-index: 24; display: flex; flex-direction: column; gap: 22px; align-items: flex-start; }}
.share {{ display: flex; align-items: center; gap: 14px; background: {INK}; color: #fff; padding: 14px 26px; border-radius: 999px; font-weight: 700; font-size: 34px; }}
.share b {{ color: {PINK}; font-size: 36px; }}
.cbox {{ position: relative; width: 640px; height: 96px; border-radius: 48px; background: #fff; border: 2px solid rgba(22,18,26,.12); display: flex; align-items: center;
  gap: 18px; padding: 0 24px; font-weight: 800; font-size: 40px; box-shadow: 0 14px 34px rgba(22,18,26,.12); }}
.cbox .av {{ width: 58px; height: 58px; border-radius: 50%; background: linear-gradient(135deg, #ff3d8b, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 100px; color: rgba(22,18,26,.4); font-weight: 600; }}
.send {{ margin-left: auto; color: {PINK}; }}
.cap {{ position: absolute; left: 70px; right: 70px; top: 1400px; text-align: center; font-weight: 800; font-size: 50px; line-height: 1.15; letter-spacing: -.02em;
  opacity: 0; z-index: 40; text-shadow: 0 0 18px rgba(255,255,255,.9), 0 0 4px rgba(255,255,255,.9); }}
.cw {{ color: rgba(22,18,26,.32); }}
#loop {{ position: absolute; inset: 0; opacity: 0; z-index: 58; background: #f4f1ec; }}
#loop img {{ position: absolute; left: 70px; right: 70px; top: 640px; width: 940px; border-radius: 34px; }}
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom remake: 304-view post-mortem 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      {chr(10).join(HTML)}
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {len(CAP)} caption cards; line starts {[round(x, 2) for x in S]}")
