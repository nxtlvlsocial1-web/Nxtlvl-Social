"""Creedom remake 1 v4, "What went wrong" (304 views), Creators 100X 9:16: writes index.html, plan/sfx_events.json, plan/edit.json.

v4 (owner, after v1-v3 "dull", "generic"): clean premium minimal on the Glacier background, Unbounded + Satoshi
(build/kit_min.py), the owner's ElevenLabs take ("Blondie - Intense Woman", build/vo_el2.py). The label says WHAT WENT
WRONG (owner: no death wording). Story (reach-psychology.md): the real 304 card on frame 1, the irony, 5 s of a 37.5 s
reel, the old opening freezing where most viewers left, problem first / tool last, this reel's own clock, Creedom at
about 70 %, CTA CREE, a cut back to frame 1 so it loops. v1-v3 (pink kinetic) are in git history.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_min import GREEN, INK, MUTE, PINK, RED, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: what went wrong v4 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.push(S[k] - .1, S[k + 1], .04)
    if k:
        R.sfx("swish", S[k] - .16)

# ---- f00: the real insights card and 304 are on screen at frame 1
H('<div class="num" id="n304" style="top:300px;font-size:300px;color:' + RED + '">304</div>')
H('<div class="hd" id="vw" style="top:640px">views.</div>')
H('<div class="stage" style="top:830px"><div class="card soft" id="ins"><img src="assets/img/insights_cards.jpg" alt="">'
  '<svg viewBox="0 0 100 100" preserveAspectRatio="none"><rect id="o304" x="1.4" y="1" width="47" height="46.5" rx="4" pathLength="1" /></svg></div></div>')
R.kicker("WHAT WENT WRONG", .1, S[6] - .2)
R.st("#n304, #ins", 0, "{opacity: 1}")
R.counter("n304", 0, .3, 299, 304)
R.ft("#n304", 0, .7, "{y: 24}", "{y: 0}")
R.ft("#ins", 0, 1.1, "{y: 50, rotationX: 24, rotationY: -18}", "{y: 0, rotationX: 12, rotationY: -10}")
R.float3d("#ins", 1.1, S[1], (12, 7), (-10, -4), (1.2, 0))
R.rise("#vw", .3, .8, 40, 8)
R.draw("#o304", .7, .8)
R.sfx("tick", .5)
for sel in ("#n304", "#vw", "#ins"):
    R.leave(sel, S[1] - .18)

# ---- f01: the irony, the old cover on a phone
H(R.lines_html("h1", ["It was a reel", "<em>about why people</em>", f'<b style="color:{RED}">stop watching.</b>'], "hd") .replace('id="h1"', 'id="h1" style="top:300px"'))
H('<div class="stage" style="top:740px"><div class="phone soft" id="oldp"><img src="assets/img/old_cover.png" alt=""><i class="hide"></i></div></div>')
R.mask_lines("#h1", S[1] - .02)
R.rise("#oldp", S[1] + .25, 1.0, 120, 14)
R.float3d("#oldp", S[1] + .25, S[2], (8, 4), (16, 8), (-2, 0))
for sel in ("#h1", "#oldp"):
    R.leave(sel, S[2] - .18)
R.sfx("swish", wt("f01", "stop") - .05)

# ---- f02: 5 seconds of a 37.5 s reel
H('<div class="lab" id="avl" style="top:420px">AVERAGE WATCH TIME</div>')
H('<div id="five"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" class="trk"/><circle cx="100" cy="100" r="96" class="arc" id="farc" pathLength="1"/></svg>'
  '<b><i id="fn">0</i><small>s</small></b></div>')
H('<div class="sub" id="of375" style="top:1260px">of a <b>37.5 s</b> reel.</div>')
tf = wt("f02", "five")
R.rise("#avl", S[2] + .05, .7, 20, 6)
R.rise("#five", S[2] + .1, .9, 50, 10)
t5a, t5d = S[2] + .35, max(1.0, tf + .3 - S[2] - .35)
R.js(f'tl.fromTo("#farc", {{strokeDashoffset: 1}}, {{strokeDashoffset: {1 - 5 / 37.5:.4f}, duration: {t5d:.3f}, ease: "steps(5)", immediateRender: false}}, {t5a:.3f});')
R.counter("fn", t5a, t5d, 0, 5, "Math.round(o.v)", "steps(5)")
for k in range(1, 6):
    R.sfx("tick", t5a + k * t5d / 5 - .02)
R.rise("#of375", tf + .35, .8, 30, 8)
for sel in ("#avl", "#five", "#of375"):
    R.leave(sel, S[3] - .18)

# ---- f03: the old first sentence plays on a phone (2x, the timer counts its real seconds) and freezes where most left
a3 = S[3]
OLD_LEN = 2.2
tq = max(a3 + .25, R.L["f03"][1] + .12 - OLD_LEN + .1)
H('<div class="lab" id="fsl" style="top:380px">YOUR FIRST SENTENCE</div>')
H(f'<div class="stage" style="top:450px"><div class="phone big soft" id="ph"><img id="opre" src="assets/img/old_first.jpg" alt="">'
  f'<video id="ov" src="assets/video/old_open_2x.mp4" data-start="{tq - .1:.3f}" data-duration="{OLD_LEN:.2f}" data-track-index="1" muted playsinline></video>'
  '<img id="ofz" src="assets/img/old_freeze.jpg" alt=""><div id="otm"><span id="otn">0.0</span> s</div><b id="x2">2x</b></div></div>')
H(f'<div class="pill" id="left" style="top:1270px"><i style="background:{RED}"></i>Most viewers left here</div>')
R.rise("#fsl", a3 + .05, .7, 20, 6)
R.rise("#ph", a3 + .05, 1.0, 140, 14)
R.float3d("#ph", a3 + .05, S[4], (6, 3), (-12, -5), (1, -.5))
R.counter("otn", tq - .1, OLD_LEN - .05, 0, 4.3, "o.v.toFixed(1)", "none")
tfz = tq - .1 + OLD_LEN
R.st("#ofz", tfz - .05, "{opacity: 1}")
R.ft("#ofz", tfz - .05, .6, '{filter: "grayscale(0) brightness(1)"}', '{filter: "grayscale(.9) brightness(.8)"}', "power2.out")
R.rise("#left", tfz, .7, 30, 8)
R.sfx("click", tfz)
for sel in ("#fsl", "#ph", "#left"):
    R.leave(sel, S[4] - .18)

# ---- f04: nobody cares about the tool (struck through); their reel; problem first, tool last (the rows swap)
H(f'<div class="num" id="tool" style="top:360px;font-size:210px;color:rgba(16,19,28,.3)">Tool<i id="strike"></i></div>')
H('<div class="num" id="their" style="top:360px;font-size:190px;line-height:.98">Their<br>reel.</div>')
H('<div id="rows" style="top:880px"><div class="row" id="rT"><b>1</b><span>Tool</span><em>"This AI told me..."</em></div>'
  f'<div class="row" id="rP"><b>2</b><span>Problem</span><em>"Your reel lost them at 0:05"</em></div></div>')
ttool = wt("f04", "tool")
R.rise("#tool", S[4] + .02, .8, 40, 10)
R.ft("#strike", ttool + .05, .5, "{scaleX: 0}", "{scaleX: 1}", "power3.inOut")
R.sfx("click", ttool + .05)
tth = wt("f04", "they")
R.leave("#tool", tth - .12, .3)
R.rise("#their", tth, .8, 40, 10)
tpr, tfi = wt("f04", "problem"), wt("f04", "first")
R.rise("#rows", tpr - .3, .8, 40, 8)
R.to("#rT", tfi + .05, .7, "{y: 170}", "expo.inOut")
R.to("#rP", tfi + .05, .7, "{y: -170}", "expo.inOut")
R.st("#rT b", tfi + .4, '{textContent: "2"}')
R.st("#rP b", tfi + .4, '{textContent: "1"}')
R.st("#rP", tfi + .4, "{className: 'row on'}")
R.sfx("swish", tfi)
R.sfx("ding", tfi + .45)
for sel in ("#their", "#rows"):
    R.leave(sel, S[5] - .18)

# ---- f05: this reel's own clock; still no app name
H('<div class="lab" id="thl" style="top:400px">THIS REEL</div>')
H('<div class="num" id="clk" style="top:470px;font-size:280px">0:00</div>')
H('<div id="bar" style="top:830px"><i id="barf"></i></div>')
H('<div class="pill" id="noname" style="top:930px">App name <span class="blur">Cxxxxxx</span></div>')
a5, a6 = S[5], S[6]
R.rise("#thl", a5 + .02, .7, 20, 6)
R.rise("#clk", a5 + .02, .8, 40, 10)
R.rise("#bar", a5 + .1, .7, 20, 6)
R.counter("clk", a5, a6 - a5, a5, a6, '"0:" + String(Math.floor(o.v)).padStart(2, "0")', "none")
R.ft("#barf", a5, a6 - a5, f"{{scaleX: {a5 / R.DUR:.3f}}}", f"{{scaleX: {a6 / R.DUR:.3f}}}", "none")
R.rise("#noname", wt("f05", "named") - .1, .7, 30, 8)
for k in range(int(a6 - a5) + 1):
    R.sfx("tick", a5 + k + .02)
for sel in ("#thl", "#clk", "#bar", "#noname"):
    R.leave(sel, a6 - .18)

# ---- f06: Creedom (about 70 % in): the logo, then the analyser card on the old reel
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div class="stage" style="top:470px"><div class="an soft" id="an"><div class="anh"><img src="assets/img/creedom_logo.png" alt=""><span>REEL ANALYZER</span></div>'
  '<div class="chart"><svg viewBox="0 0 600 260" preserveAspectRatio="none"><path id="ret" d="M0,30 C60,32 90,36 110,44 C130,54 140,160 160,190 C200,215 300,222 600,230" pathLength="1"/></svg>'
  '<i id="drop"></i><b id="dropl">Viewers leave at 0:05</b></div>'
  '<div class="why" id="why"><b>WHY</b><span>The hook names a tool, not the viewer\'s problem.</span></div></div></div>')
H('<img id="cree" src="assets/img/poses/mag.png" alt="">')
R.kicker("CREEDOM", a6 - .05, S[7] - .2, PINK)
R.ft("#logo", a6 - .02, 1.0, '{opacity: 1, scale: .9, filter: "blur(14px)"}', '{scale: 1, filter: "blur(0px)"}', "expo.out")
R.st("#logo", 0, "{opacity: 0}")
R.sfx("sparkle", a6)
tsh = wt("f06", "shows")
R.leave("#logo", tsh - .1, .35, -60)
R.rise("#an", tsh, 1.0, 120, 12)
R.float3d("#an", tsh, S[7], (8, 4), (-10, -4), (1, 0))
R.draw("#ret", tsh + .35, .9)
tex = wt("f06", "exact")
R.ft("#drop", tex - .05, .5, "{opacity: 1, scale: 0}", "{scale: 1}", "back.out(3)")
R.st("#drop", 0, "{opacity: 0}")
R.rise("#dropl", tex + .05, .6, 16, 6)
R.sfx("click", tex)
R.rise("#why", wt("f06", "why") - .15, .7, 20, 6)
R.rise("#cree", wt("f06", "why") - .05, .9, 60, 10)
for sel in ("#an", "#cree"):
    R.leave(sel, S[7] - .18)

# ---- f07: CTA (CREE), the comment field types it; cut back to frame 1 so it loops
a7 = S[7]
H(R.lines_html("h7", ["Send this to the friend", "<em>whose reels keep flopping.</em>"], "hd").replace('id="h7"', 'id="h7" style="top:330px"'))
H('<div class="cbox soft" id="cbox" style="top:760px"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>')
H('<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.mask_lines("#h7", a7 - .02)
tc = wt("f07", "comment")
R.rise("#cbox", tc - .4, .8, 40, 8)
R.rise("#cree2", tc - .2, .9, 60, 10)
R.st("#cph", tc + .15, "{opacity: 0}")
R.typer("cty", tc + .15, "CREE", .4)
R.sfx("typing", tc + .15)
R.ft("#cbox .send", tc + .7, .5, "{scale: 1.5}", "{scale: 1}", "back.out(3)")
R.sfx("notify", tc + .75)
H('<div id="loop"><div class="num" style="top:300px;font-size:300px;color:' + RED + '">304</div><div class="hd" style="top:640px">views.</div>'
  '<div class="stage" style="top:830px"><div class="card soft" style="transform:rotateX(24deg) rotateY(-18deg) translateY(50px)"><img src="assets/img/insights_cards.jpg" alt=""></div></div></div>')
R.ft("#loop", R.DUR - .45, .4, "{opacity: 0}", "{opacity: 1}", "power2.inOut")

R.captions(top=1470)

R.write(f"""
.lab {{ position: absolute; left: 90px; font-family: Mono; font-size: 28px; letter-spacing: .24em; color: {MUTE}; z-index: 20; }}
.sub {{ position: absolute; left: 90px; right: 90px; font-family: Sat; font-weight: 500; font-size: 64px; letter-spacing: -.02em; color: {MUTE}; z-index: 20; }}
.sub b {{ font-weight: 900; color: {INK}; }}
.card {{ position: relative; margin: 0 auto; width: 880px; border-radius: 34px; overflow: hidden; opacity: 0; transform-style: preserve-3d; }}
.card img {{ display: block; width: 100%; }}
.card svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
#o304 {{ fill: none; stroke: {RED}; stroke-width: .6; stroke-dasharray: 1; stroke-dashoffset: 1; vector-effect: non-scaling-stroke; stroke-width: 5; }}
.phone {{ position: relative; margin: 0 auto; width: 340px; height: 604px; border-radius: 48px; overflow: hidden; background: #000; border: 10px solid {INK}; opacity: 0; }}
.phone.big {{ width: 420px; height: 746px; border-radius: 56px; }}
.phone img, .phone video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.hide {{ position: absolute; left: 22%; right: 22%; top: 83%; height: 8%; border-radius: 12px; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: rgba(255,220,236,.55); }}
#ofz {{ opacity: 0; }}
#otm {{ position: absolute; left: 50%; top: 24px; transform: translateX(-50%); background: rgba(16,19,28,.82); color: #fff; font-family: Mono; font-size: 38px; padding: 8px 22px; border-radius: 999px; }}
#x2 {{ position: absolute; right: 20px; bottom: 20px; background: rgba(16,19,28,.82); color: #fff; font-family: Mono; font-size: 28px; padding: 6px 14px; border-radius: 10px; }}
.pill {{ position: absolute; left: 50%; transform: translateX(-50%); white-space: nowrap; display: flex; align-items: center; gap: 18px; background: #fff; padding: 22px 36px;
  border-radius: 999px; font-family: Sat; font-weight: 700; font-size: 46px; box-shadow: 0 20px 50px rgba(40,50,90,.16); z-index: 22; }}
.pill i {{ width: 16px; height: 16px; border-radius: 50%; }}
.pill .blur {{ font-family: Mono; color: {MUTE}; filter: blur(8px); }}
#five {{ position: absolute; left: 190px; top: 500px; width: 700px; height: 700px; z-index: 20; }}
#five svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
#five .trk {{ fill: none; stroke: rgba(16,19,28,.1); stroke-width: 2; }}
#five .arc {{ fill: none; stroke: {RED}; stroke-width: 4; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: 1; }}
#five b {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 175px; font-family: Unb; font-weight: 900; color: {INK}; }}
#five b i {{ font-style: normal; font-size: 330px; line-height: 1; letter-spacing: -.06em; }}
#five b small {{ font-size: 110px; color: {MUTE}; }}
#strike {{ position: absolute; left: -10px; right: -10px; top: 52%; height: 10px; background: {RED}; border-radius: 5px; transform-origin: left center; transform: scaleX(0); }}
#rows {{ position: absolute; left: 90px; right: 90px; z-index: 20; height: 340px; }}
.row {{ position: absolute; left: 0; right: 0; height: 150px; display: flex; align-items: center; gap: 30px; border-top: 2px solid rgba(16,19,28,.1); }}
#rT {{ top: 0; }} #rP {{ top: 170px; border-bottom: 2px solid rgba(16,19,28,.1); }}
.row b {{ font-family: Unb; font-weight: 900; font-size: 54px; width: 70px; color: {MUTE}; }}
.row span {{ font-family: Sat; font-weight: 900; font-size: 72px; letter-spacing: -.03em; }}
.row em {{ margin-left: auto; font-style: normal; font-family: Sat; font-weight: 500; font-size: 34px; color: {MUTE}; max-width: 360px; text-align: right; line-height: 1.15; }}
.row.on b {{ color: {GREEN}; }}
#bar {{ position: absolute; left: 90px; right: 90px; height: 6px; background: rgba(16,19,28,.1); border-radius: 3px; z-index: 20; }}
#barf {{ position: absolute; inset: 0; background: {INK}; transform-origin: left center; border-radius: 3px; }}
#logo {{ position: absolute; left: 140px; right: 140px; top: 640px; height: 280px; display: grid; place-items: center; z-index: 25; }}
#logo img {{ width: 100%; }}
.an {{ position: relative; margin: 0 auto; width: 900px; border-radius: 40px; padding: 38px 40px 44px; background: rgba(255,255,255,.92); opacity: 0; }}
.anh {{ display: flex; align-items: center; justify-content: space-between; }}
.anh img {{ height: 64px; }}
.anh span {{ font-family: Mono; font-size: 26px; letter-spacing: .18em; color: {MUTE}; }}
.chart {{ position: relative; margin-top: 30px; height: 320px; border-radius: 26px; background: #f4f6fb; padding: 22px; }}
.chart svg {{ width: 100%; height: 100%; overflow: visible; }}
#ret {{ fill: none; stroke: {INK}; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: 1; vector-effect: non-scaling-stroke; }}
#drop {{ position: absolute; left: 31%; top: 33%; width: 30px; height: 30px; border-radius: 50%; background: {RED}; box-shadow: 0 0 0 12px rgba(226,57,47,.16); }}
#dropl {{ position: absolute; left: 37%; top: 9%; background: {INK}; color: #fff; font-family: Sat; font-weight: 700; font-size: 34px; padding: 10px 20px; border-radius: 14px; }}
.why {{ margin-top: 28px; display: flex; gap: 22px; align-items: baseline; }}
.why b {{ font-family: Mono; font-size: 26px; letter-spacing: .16em; color: {PINK}; }}
.why span {{ font-family: Sat; font-weight: 700; font-size: 44px; line-height: 1.15; letter-spacing: -.02em; }}
#cree {{ position: absolute; right: 70px; top: 1150px; width: 230px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
#cree2 {{ position: absolute; right: 90px; top: 960px; width: 260px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
.cbox {{ position: absolute; left: 90px; width: 820px; height: 140px; border-radius: 70px; background: #fff; display: flex; align-items: center; gap: 24px; padding: 0 34px;
  font-family: Sat; font-weight: 900; font-size: 64px; letter-spacing: .02em; z-index: 22; }}
.cbox .av {{ width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 142px; color: rgba(16,19,28,.35); font-weight: 500; font-size: 48px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: {PINK}; font-size: 54px; }}
#loop {{ position: absolute; inset: -60px; opacity: 0; z-index: 50; background: linear-gradient(180deg, #f7f8fc, #eceff7); }}
#loop > * {{ margin-left: 0; }}
#loop .num, #loop .hd {{ transform: translate(60px, 60px); }}
#loop .stage {{ transform: translateY(60px); }}
""")
