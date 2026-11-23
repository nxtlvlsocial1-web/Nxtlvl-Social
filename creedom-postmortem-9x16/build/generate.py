"""Creedom remake 1 v2, "The 304-view post-mortem" (Creators 100X, 9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

v2 (owner: "very dull and slow animated feel"): bright pink and fast. The moving pink world sits behind every frame; a
camera punch, a whip, a slam or a pop lands about every 0.7-1 s; giant words on the key beats; punchy 1-3 word captions.
Story unchanged (reach-psychology.md): real 304 card on frame 1, the irony, 5 s, the old opening freezing where the
average viewer left, problem first / tool last, this reel's own clock, Creedom at about 65 %, CTA CREE, loop to frame 1.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import INK, PINK, SUN, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: 304-view post-mortem v2 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.drift(S[k] - .05, S[k + 1] - S[k] + .05, rot=1.6 if k % 2 else -1.6, z=.06)

# ---- f00: the real insights card is on screen at frame 1; 304 counts up and slams
H('<div id="ins" class="card0"><img src="assets/img/insights_cards.jpg" alt=""><i class="ring" id="r304"></i><i class="ring" id="r5"></i></div>')
R.st("#ins", 0, "{opacity: 1}")
R.ft("#ins", 0, .45, "{scale: 1.3, rotation: -8, y: 60}", "{scale: 1, rotation: -2.5, y: 0}", "expo.out")
R.pop_in("#r304", .2, .3, 1.4)
sl = R.slam('<b id="n304">0</b> views.', .06, S[1] - .5, top=300, size=190, rot=-3, sfx="impact")
R.counter("n304", .06, .5, 0, 304, ease="power3.out")
R.burst(.06, 540, 400, 1.1)
R.sfx("riser_short", 0)
tg = wt("f00", "views")
R.to("#ins", tg, .25, "{rotation: 2, scale: 1.04}", "back.out(2)")
R.punch(tg, .05)

# ---- f01: whip to the old cover; the irony slams on "stop watching"
a1 = S[1]
H('<div id="old"><img src="assets/img/old_cover.png" alt=""><i class="hide"></i></div>')
R.whip_out("#ins", a1 - .12)
R.whip_in("#old", a1 - .02, rot=4)
R.sfx("whoosh", a1 - .12)
tr = wt("f01", "reel")
R.to("#old", tr, .3, "{rotation: -4, scale: 1.05}", "back.out(2.5)")
R.punch(tr, .05)
R.sfx("swish", tr)
tsw = wt("f01", "stop")
R.slam("the <em>irony.</em>", tsw - .02, max(.4, S[2] - tsw - .45), top=290, size=170, rot=-6, sfx="thump")
R.sfx("screech", tsw - .15)
R.burst(tsw, 540, 380, 1.0, SUN)

# ---- f02: average watch, a giant 5 s timer ticking
a2 = S[2]
H('<div id="avg"><span>AVERAGE WATCH TIME</span></div>'
  '<div id="five"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="88" class="trk"/><circle cx="100" cy="100" r="88" class="arc" id="farc"/></svg>'
  '<b><i id="fn">0</i><small>s</small></b></div>')
R.zoom_out("#old", a2 - .12)
R.flash(a2 - .04, .7)
R.sfx("whoosh_big", a2 - .14)
R.pop_in("#avg", a2, .3, .5, -3)
R.pop_in("#five", a2 + .05, .38, .3, 0, "back.out(1.8)")
tf = wt("f02", "five")
t5a, t5d = a2 + .3, max(.9, tf + .5 - a2 - .3)      # the timer runs the whole line and lands 5 on "five"
R.js(f'tl.fromTo("#farc", {{strokeDashoffset: 553}}, {{strokeDashoffset: 0, duration: {t5d:.3f}, ease: "steps(5)", immediateRender: false}}, {t5a:.3f});')
R.counter("fn", t5a, t5d, 0, 5, "Math.round(o.v)", "steps(5)")
for k in range(1, 6):
    R.sfx("tick", t5a + k * t5d / 5 - .02)
    R.punch(t5a + k * t5d / 5 - .02, .03, .15)
R.slam("5 <em>seconds.</em>", tf + .62, max(.35, S[3] - tf - 1.0), top=1170, size=150, rot=3, sfx="impact")

# ---- f03: the old opening plays on a phone under a timer, then freezes where they left
a3 = S[3]
# the old first sentence runs 4.3 s, longer than this line: it plays at 2x (the timer counts its real seconds, a 2x chip
# says so) and freezes just after the line ends, in the pause build/vo_pick.py leaves after f03
OLD_LEN = 2.2
tq = max(a3 + .25, R.L["f03"][1] + .12 - OLD_LEN + .1)
H(f'<div id="phone"><img id="opre" src="assets/img/old_first.jpg" alt=""><video id="ov" src="assets/video/old_open_2x.mp4" data-start="{tq - .1:.3f}" data-duration="{OLD_LEN:.2f}" data-track-index="1" muted playsinline></video>'
  '<img id="ofz" src="assets/img/old_freeze.jpg" alt=""><div id="otm"><span id="otn">0.0</span>s</div><b id="x2">2x</b><b class="stamp" id="left">THEY LEFT<br>HERE</b></div>')
H('<div id="mini"><b>5s</b><span>avg watch</span></div>')
R.to("#avg", a3 - .12, .15, "{opacity: 0, y: -60}", "power2.in")
R.zoom_out("#five", a3 - .12)
R.ft("#phone", a3 - .02, .36, '{opacity: 1, y: 1300, rotation: 8, filter: "blur(20px)"}', '{y: 0, rotation: -2, filter: "blur(0px)"}', "expo.out")
R.sfx("whoosh", a3 - .1)
R.pop_in("#mini", a3 + .3, .3, .4, 6)
R.sfx("pop", a3 + .3)
tsen = wt("f03", "sentence")
R.to("#phone", tsen, .3, "{rotation: 2, scale: 1.04}", "back.out(2)")
R.punch(tsen, .05)
R.counter("otn", tq - .1, OLD_LEN - .05, 0, 4.3, "o.v.toFixed(1)", "none")
R.ft("#phone", tq - .1, OLD_LEN, "{scale: 1.04}", "{scale: 1.16}", "none")
R.sfx("typing", tq)
tfz = tq - .1 + OLD_LEN
R.st("#ofz", tfz - .05, "{opacity: 1}")
R.flash(tfz - .03, .9, .16)
R.ft("#left", tfz, .22, "{opacity: 0, scale: 2.6, rotation: -22}", "{opacity: 1, scale: 1, rotation: -9}", "power4.out")
R.sfx("stamp", tfz + .05)
R.shake(tfz + .06, 22, 2)
R.punch(tfz + .04, .12)
R.ft("#mini", tfz + .05, .3, "{scale: 1.5}", "{scale: 1}", "back.out(3)")

# ---- f04: nobody cares about the TOOL (struck out); THEIR REEL; problem first, tool last (cards swap)
a4 = S[4]
H('<div id="tool"><b>TOOL</b><i id="strike"></i></div>')
H('<div id="swap"><div class="card" id="cTool"><i>1</i><b>TOOL</b><span>"This AI told me..."</span></div>'
  '<div class="card hot" id="cProb"><i>2</i><b>PROBLEM</b><span>"Your reel lost them at 0:05"</span></div></div>')
R.whip_out("#phone", a4 - .14, -1)
R.to("#mini", a4 - .14, .15, "{opacity: 0, scale: .4}", "power2.in")
R.whip_in("#tool", a4 - .03, 1, rot=-3)
R.sfx("whoosh", a4 - .14)
tno = wt("f04", "tool")
R.ft("#strike", tno - .02, .2, "{scaleX: 0}", "{scaleX: 1}", "power4.out")
R.sfx("g_wrong", tno)
R.shake(tno + .05, 12, 1)
R.punch(tno + .02, .06)
tth = wt("f04", "they")
R.zoom_out("#tool", tth - .1)
tpr = wt("f04", "problem")
R.slam("their <em>reel.</em>", tth, max(.35, tpr - tth - .4), top=640, size=210, rot=-4, sfx="impact")
R.burst(tth, 540, 760, 1.2, SUN)
R.pop_in("#swap", tpr - .06, .3, .7, 0, "back.out(2)")
R.sfx("pop", tpr - .06)
tfi = wt("f04", "first")
R.to("#cTool", tfi, .32, "{y: 300, rotation: -3}", "back.out(1.8)")
R.to("#cProb", tfi, .32, "{y: -300, rotation: 3, scale: 1.06}", "back.out(1.8)")
R.st("#cTool i", tfi + .15, '{textContent: "2"}')
R.st("#cProb i", tfi + .15, '{textContent: "1"}')
R.sfx("whoosh", tfi - .05)
R.sfx("ding", tfi + .3)
R.punch(tfi + .25, .06)

# ---- f05: this reel's own clock, and still no app name
a5 = S[5]
H('<div id="bigclock"><div class="dial"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="trk"/><circle cx="100" cy="100" r="86" class="arc" id="arc"/></svg>'
  '<b id="clock2">0:00</b></div><div class="nope" id="nope"><span>APP NAME</span><i>?</i></div></div>')
R.whip_out("#swap", a5 - .14, -1)
R.pop_in("#bigclock", a5 - .02, .35, .3, 0, "back.out(1.8)")
R.burst(a5, 540, 860, 1.1)
R.sfx("whoosh", a5 - .14)
R.counter("clock2", a5, S[6] - a5, a5, S[6], '"0:" + String(Math.floor(o.v)).padStart(2, "0")', "none")
R.ft("#arc", a5, S[6] - a5, "{strokeDashoffset: 540}", "{strokeDashoffset: 120}", "none")
for k in range(int(S[6] - a5) + 1):
    R.sfx("tick", a5 + k + .02)
tse = wt("f05", "seventeen")
R.ft(".dial", tse, .3, "{scale: 1.18}", "{scale: 1}", "back.out(3)")
R.punch(tse, .07)
R.sfx("thump", tse)
tna = wt("f05", "named")
R.ft("#nope", tna, .3, "{x: 0}", "{keyframes: [{x: -18, duration: .05}, {x: 16, duration: .05}, {x: -10, duration: .05}, {x: 6, duration: .05}, {x: 0, duration: .1}]}", "none")
R.sfx("buzzer", tna)

# ---- f06: Creedom (about 65 % in): flash, logo slam, confetti, the analyser card, Cree with the magnifier
a6 = S[6]
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div id="an"><div class="anh"><img src="assets/img/creedom_logo.png" alt=""><span>REEL ANALYZER</span></div>'
  '<div class="chart"><svg viewBox="0 0 600 260" preserveAspectRatio="none"><path id="ret" d="M0,40 C60,42 90,46 110,52 C130,60 140,160 160,190 C200,215 300,222 600,230" fill="none" stroke="#ff3d8b" stroke-width="8" stroke-linecap="round"/></svg>'
  '<i id="drop"></i><b id="dropl">viewers left at 0:05</b></div>'
  '<div class="why" id="why"><b>WHY</b><span>The hook names a tool. It never shows the viewer\'s problem.</span></div></div>')
H('<img id="cree" src="assets/img/poses/mag.png" alt="">')
R.zoom_out("#bigclock", a6 - .14)
R.flash(a6 - .06, .95, .25)
R.ft("#logo", a6 - .04, .3, "{opacity: 0, scale: 3, rotation: -12}", "{opacity: 1, scale: 1, rotation: -3}", "power4.out")
R.burst(a6, 540, 800, 1.4, SUN)
R.confetti(a6, 40, 3, 540, 800)
R.shake(a6 + .05, 16, 1.4)
R.punch(a6 + .02, .1)
R.sfx("whoosh_big", a6 - .2)
R.sfx("impact", a6 - .02)
R.sfx("sparkle", a6 + .05)
tsh = wt("f06", "shows")
R.to("#logo", tsh - .12, .18, "{y: -900, scale: .5, opacity: 0}", "power3.in")
R.ft("#an", tsh - .04, .36, '{opacity: 1, y: 1200, rotation: 6, filter: "blur(20px)"}', '{y: 0, rotation: -1.5, filter: "blur(0px)"}', "expo.out")
R.sfx("whoosh", tsh - .12)
R.js(f'tl.fromTo("#ret", {{strokeDasharray: 900, strokeDashoffset: 900}}, {{strokeDashoffset: 0, duration: .7, ease: "power2.out", immediateRender: false}}, {tsh + .2:.3f});')
tex = wt("f06", "exact")
R.pop_in("#drop", tex - .05, .3, 0, 0, "back.out(4)")
R.pop_in("#dropl", tex + .05, .28, .5, -2)
R.sfx("pop", tex - .05)
R.punch(tex, .05)
R.ft("#cree", tsh + .1, .4, "{opacity: 0, x: 300, rotation: 20}", "{opacity: 1, x: 0, rotation: 0}", "back.out(2)")
R.sfx("g_pop", tsh + .1)
twy = wt("f06", "why")
R.pop_in("#why", twy - .1, .3, .7, 0, "back.out(2)")
R.punch(twy, .05)

# ---- f07: CTA (CREE): share sticker, giant comment box typing CREE, Cree waves; flash cut back to frame 1 (loop)
a7 = S[7]
H('<div id="share"><b>&#10148;</b><span>send this to the friend<br>whose reels keep flopping</span></div>'
  '<div id="cbox"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>'
  '<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.whip_out("#an", a7 - .14, -1)
R.to("#cree", a7 - .14, .15, "{opacity: 0, x: 300}", "power2.in")
R.pop_in("#share", a7 - .02, .32, .4, -3)
R.burst(a7, 540, 640, 1.0)
R.sfx("whoosh", a7 - .14)
R.sfx("pop", a7)
tfr = wt("f07", "friend")
R.ft("#share", tfr, .3, "{scale: 1.12}", "{scale: 1}", "back.out(3)")
R.punch(tfr, .05)
tc = wt("f07", "comment")
R.pop_in("#cbox", tc - .08, .32, .5, 0, "back.out(2.2)")
R.ft("#cree2", tc - .02, .4, "{opacity: 0, x: 300, rotation: 20}", "{opacity: 1, x: 0, rotation: 0}", "back.out(2)")
R.st("#cph", tc + .12, "{opacity: 0}")
R.typer("cty", tc + .12, "CREE", .4)
R.sfx("typing", tc + .12)
R.ft("#cbox", tc + .6, .3, "{scale: 1.12}", "{scale: 1}", "back.out(3)")
R.sfx("click", tc + .6)
R.sfx("notify", tc + .8)
R.punch(tc + .6, .06)
H('<div id="loop"><img src="assets/img/insights_cards.jpg" alt=""></div>')
R.flash(R.DUR - .36, .9, .2)
R.st("#loop", R.DUR - .3, "{opacity: 1}")

R.captions(top=1440, max_words=3)

R.write(f"""
.card0 {{ position: absolute; left: 70px; right: 70px; top: 640px; opacity: 0; border-radius: 38px; overflow: hidden; background: #0d0f14;
  border: 8px solid #fff; box-shadow: 0 18px 0 {INK}, 0 40px 80px rgba(70,0,35,.4); z-index: 10; }}
.card0 img {{ display: block; width: 100%; }}
.ring {{ position: absolute; border: 8px solid {SUN}; border-radius: 26px; opacity: 0; box-shadow: 0 0 34px rgba(255,225,77,.7); }}
#r304 {{ left: 18px; top: -2px; width: 440px; height: 196px; }}
#r5 {{ left: 18px; top: 200px; width: 440px; height: 196px; }}
#old {{ position: absolute; left: 250px; top: 520px; width: 580px; opacity: 0; z-index: 12; }}
#old img {{ width: 100%; border-radius: 34px; display: block; border: 8px solid #fff; box-shadow: 0 18px 0 {INK}, 0 40px 80px rgba(70,0,35,.4); }}
.hide {{ position: absolute; left: 22%; right: 22%; top: 83%; height: 8%; border-radius: 16px; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); background: rgba(255,220,236,.6); }}
#avg {{ position: absolute; left: 0; right: 0; top: 400px; text-align: center; opacity: 0; z-index: 20; }}
#avg span {{ display: inline-block; background: {INK}; color: #fff; font-family: Mono; font-weight: 700; font-size: 44px; letter-spacing: .12em; padding: 16px 34px; border-radius: 20px;
  box-shadow: 0 10px 0 rgba(22,18,26,.35); }}
#five {{ position: absolute; left: 190px; top: 520px; width: 700px; height: 700px; opacity: 0; z-index: 20; }}
#five svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
#five .trk {{ fill: #fff; stroke: rgba(22,18,26,.12); stroke-width: 16; }}
#five .arc {{ fill: none; stroke: {INK}; stroke-width: 16; stroke-linecap: round; stroke-dasharray: 553; }}
#five b {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 170px; font-weight: 800; color: {PINK}; }}
#five b i {{ font-style: normal; font-size: 360px; line-height: 1; letter-spacing: -.06em; }}
#five b small {{ font-size: 140px; color: {INK}; }}
#phone {{ position: absolute; left: 270px; top: 330px; width: 540px; height: 960px; border-radius: 54px; overflow: hidden; background: #000; opacity: 0;
  border: 12px solid {INK}; box-shadow: 0 22px 0 rgba(22,18,26,.45), 0 50px 100px rgba(70,0,35,.45); z-index: 16; }}
#opre, #ov, #ofz {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#x2 {{ position: absolute; right: 22px; bottom: 22px; background: {INK}; color: #fff; font-family: Mono; font-weight: 700; font-size: 34px; padding: 6px 16px; border-radius: 12px; }}
#ofz {{ opacity: 0; filter: grayscale(.8) brightness(.75); }}
#otm {{ position: absolute; left: 50%; top: 26px; transform: translateX(-50%); background: {PINK}; color: #fff; font-family: Mono; font-weight: 700;
  font-size: 50px; padding: 8px 26px; border-radius: 999px; border: 4px solid #fff; }}
.stamp {{ position: absolute; left: 30px; right: 30px; top: 360px; text-align: center; border: 10px solid #ff2d55; color: #ff2d55; background: rgba(255,255,255,.94);
  font-weight: 800; font-size: 76px; line-height: 1; letter-spacing: .02em; padding: 18px 0; border-radius: 22px; opacity: 0; }}
#mini {{ position: absolute; left: 740px; top: 1100px; width: 250px; height: 250px; border-radius: 50%; background: {SUN}; border: 8px solid {INK}; opacity: 0; z-index: 18;
  display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 12px 0 {INK}; }}
#mini b {{ font-size: 110px; font-weight: 800; line-height: .9; letter-spacing: -.05em; }}
#mini span {{ font-family: Mono; font-weight: 700; font-size: 24px; letter-spacing: .08em; }}
#tool {{ position: absolute; left: 140px; right: 140px; top: 640px; height: 360px; border-radius: 44px; background: #fff; opacity: 0; z-index: 16; display: grid; place-items: center;
  box-shadow: 0 18px 0 {INK}, 0 40px 80px rgba(70,0,35,.35); }}
#tool b {{ font-size: 230px; font-weight: 800; letter-spacing: -.05em; }}
#strike {{ position: absolute; left: 40px; right: 40px; top: 170px; height: 30px; background: #ff2d55; border-radius: 15px; transform: rotate(-8deg) scaleX(0); transform-origin: left center; }}
#swap {{ position: absolute; left: 90px; right: 90px; top: 520px; height: 720px; opacity: 0; z-index: 16; }}
.card {{ position: absolute; left: 0; right: 0; height: 260px; border-radius: 40px; background: #fff; box-shadow: 0 16px 0 {INK}, 0 36px 70px rgba(70,0,35,.3);
  display: flex; flex-direction: column; justify-content: center; padding: 0 40px 0 180px; }}
.card i {{ position: absolute; left: 40px; top: 50%; margin-top: -56px; width: 112px; height: 112px; border-radius: 50%; background: #ece6ee; display: grid;
  place-items: center; font-style: normal; font-weight: 800; font-size: 64px; }}
.card b {{ font-weight: 800; font-size: 84px; letter-spacing: -.03em; line-height: 1; }}
.card span {{ font-family: Serif; font-style: italic; font-size: 46px; color: #6b6470; margin-top: 8px; }}
#cTool {{ top: 60px; }} #cProb {{ top: 360px; }}
.card.hot {{ background: {SUN}; }} .card.hot i {{ background: {INK}; color: #fff; }}
#bigclock {{ position: absolute; left: 0; right: 0; top: 470px; display: flex; flex-direction: column; align-items: center; gap: 44px; opacity: 0; z-index: 16; }}
.dial {{ position: relative; width: 600px; height: 600px; }}
.dial svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
.dial .trk {{ fill: #fff; stroke: rgba(22,18,26,.12); stroke-width: 14; }}
.dial .arc {{ fill: none; stroke: {INK}; stroke-width: 14; stroke-linecap: round; stroke-dasharray: 540; }}
.dial b {{ position: absolute; inset: 0; display: grid; place-items: center; font-family: Mono; font-weight: 700; font-size: 180px; color: {PINK}; }}
.nope {{ display: flex; align-items: center; gap: 20px; background: {INK}; padding: 20px 40px; border-radius: 26px; box-shadow: 0 12px 0 rgba(22,18,26,.35); }}
.nope span {{ font-family: Mono; font-weight: 700; font-size: 46px; letter-spacing: .14em; color: #fff; filter: blur(3px); }}
.nope i {{ font-style: normal; font-weight: 800; font-size: 76px; color: {SUN}; }}
#logo {{ position: absolute; left: 90px; right: 90px; top: 640px; height: 300px; border-radius: 50px; background: #fff; opacity: 0; z-index: 30; display: grid; place-items: center;
  box-shadow: 0 18px 0 {INK}, 0 40px 90px rgba(70,0,35,.4); }}
#logo img {{ width: 78%; }}
#an {{ position: absolute; left: 60px; right: 60px; top: 470px; opacity: 0; z-index: 20; border-radius: 44px; padding: 36px 38px 40px; background: #fff;
  box-shadow: 0 18px 0 {INK}, 0 40px 90px rgba(70,0,35,.35); }}
.anh {{ display: flex; align-items: center; justify-content: space-between; }}
.anh img {{ height: 70px; }}
.anh span {{ font-family: Mono; font-weight: 700; font-size: 28px; letter-spacing: .16em; color: {PINK}; }}
.chart {{ position: relative; margin-top: 26px; height: 320px; border-radius: 26px; background: #fff3f8; padding: 20px; }}
.chart svg {{ width: 100%; height: 100%; }}
#drop {{ position: absolute; left: 31%; top: 34%; width: 40px; height: 40px; border-radius: 50%; background: {PINK}; box-shadow: 0 0 0 12px rgba(255,61,139,.25); opacity: 0; }}
#dropl {{ position: absolute; left: 38%; top: 10%; background: {INK}; color: #fff; font-weight: 800; font-size: 38px; padding: 10px 20px; border-radius: 16px; opacity: 0; }}
.why {{ margin-top: 26px; display: flex; gap: 20px; align-items: baseline; opacity: 0; }}
.why b {{ font-family: Mono; font-weight: 700; font-size: 30px; letter-spacing: .14em; color: {PINK}; }}
.why span {{ font-weight: 800; font-size: 42px; line-height: 1.15; }}
#cree, #cree2 {{ position: absolute; right: 20px; top: 1060px; width: 330px; opacity: 0; z-index: 24; filter: drop-shadow(0 16px 0 rgba(22,18,26,.25)); }}
#cree2 {{ top: 1000px; }}
#share {{ position: absolute; left: 70px; right: 70px; top: 470px; opacity: 0; z-index: 24; display: flex; align-items: center; gap: 26px; background: {INK}; color: #fff;
  padding: 30px 40px; border-radius: 40px; font-weight: 800; font-size: 54px; line-height: 1.1; box-shadow: 0 14px 0 rgba(22,18,26,.35); }}
#share b {{ color: {SUN}; font-size: 80px; }}
#cbox {{ position: absolute; left: 60px; width: 760px; top: 860px; height: 150px; border-radius: 75px; background: #fff; display: flex; align-items: center; opacity: 0; z-index: 24;
  gap: 24px; padding: 0 34px; font-weight: 800; font-size: 72px; letter-spacing: .02em; box-shadow: 0 16px 0 {INK}, 0 36px 70px rgba(70,0,35,.3); }}
#cbox .av {{ width: 90px; height: 90px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 150px; color: rgba(22,18,26,.35); font-weight: 600; font-size: 52px; }}
#cbox .send {{ margin-left: auto; color: {PINK}; }}
#loop {{ position: absolute; inset: 0; opacity: 0; z-index: 46; background: {PINK}; }}
#loop img {{ position: absolute; left: 70px; top: 640px; width: 940px; border-radius: 38px; border: 8px solid #fff; transform: rotate(-8deg) scale(1.3); }}
""")
