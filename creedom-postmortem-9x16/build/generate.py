"""Creedom remake 1 v6, "What went wrong" (304 views), Creators 100X 9:16: writes index.html, plan/sfx_events.json, plan/edit.json.

v6 (owner, on v5: fix the first-frame pile-up; no background music; "viewers should get what Creedom does as soon as
possible, even if they don't watch the whole video"): tool first. Line 1 says what Creedom does while its analyser
screen is on frame 1; the Creedom logo bar with the comment keyword stays at the top the whole reel; the 304 story is
the proof; the name and CTA close it (about 17 s). Elements that appear later are hidden in CSS from frame 0
(build/kit_min.py). Voice: Kokoro af_heart (build/vo_kok.py). Look: Glacier, Unbounded + Satoshi.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_min import GREEN, INK, MUTE, PINK, RED, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: what went wrong v6 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.push(S[k] - .1, S[k + 1], .035)
    if k:
        R.sfx("swish", S[k] - .16)
R.sfx("thump", .02)
R.topbar("CREE", S[1] - .1)
R.sfx("pop", S[1] - .1)

# ---- f00: what Creedom does, said in line 1, with its analyser screen on frame 1 (visible in CSS from frame 0)
H('<div class="hd" id="hk" style="top:330px;font-size:88px"><span class="ln"><span>This tool shows the</span></span><span class="ln"><span>exact second people</span></span>'
  f'<span class="ln"><span style="color:{RED}">leave your reel.</span></span></div>')
H('<div class="stage" style="top:720px"><div class="an soft" id="an0"><div class="anh"><img src="assets/img/creedom_logo.png" alt=""><span>REEL ANALYZER</span></div>'
  '<div class="chart"><svg viewBox="0 0 600 260" preserveAspectRatio="none"><path id="ret0" d="M0,30 C60,32 90,36 110,44 C130,54 140,160 160,190 C200,215 300,222 600,230" pathLength="1"/></svg>'
  '<i id="drop0"></i><b id="dl0">Viewers leave at 0:05</b></div></div></div>')
R.js('tl.fromTo("#hk .ln > span", {y: 10}, {y: 0, duration: .45, ease: "expo.out", stagger: .06, immediateRender: true}, 0);')
R.ft("#an0", 0, 1.0, "{y: 40, rotationX: 20, rotationY: -14}", "{y: 0, rotationX: 9, rotationY: -6}")
tex = wt("f00", "exact")
R.ft("#drop0", tex - .05, .45, "{opacity: 1, scale: 0}", "{scale: 1}", "back.out(3)")
R.st("#drop0", 0, "{opacity: 0}")
R.sfx("click", tex)
R.rise("#dl0", wt("f00", "second") + .05, .45, 16, 6)
R.to("#an0", wt("f00", "leave") - .1, .6, "{scale: 1.18, x: 90, y: -20}", "expo.inOut")      # in on the drop point
R.sfx("swish", wt("f00", "leave") - .1)
R.leave("#hk", S[1] - .25, .3)
R.leave("#an0", S[1] - .25, .3)

# ---- f01: the proof: the real insights card, 304 counts up, then 5 s average watch is outlined
H(f'<div class="num" id="n304" style="top:330px;font-size:200px;color:{RED}">0</div>')
H('<div class="hd" id="vw" style="top:550px">views.</div>')
H('<div class="stage" style="top:760px"><div class="card soft" id="ins"><img src="assets/img/insights_cards.jpg" alt="">'
  '<svg viewBox="0 0 100 100" preserveAspectRatio="none"><rect id="o304" x="1.4" y="1" width="47" height="46.5" rx="4" pathLength="1" />'
  '<rect id="o5" x="1.4" y="51.5" width="47" height="46.5" rx="4" pathLength="1" /></svg></div></div>')
t304 = wt("f01", "304")
R.rise("#n304", S[1] - .2, .6, 40, 8)
R.counter("n304", S[1] - .2, t304 + .45 - (S[1] - .2), 0, 304, "Math.round(o.v)", "power2.inOut")
R.rise("#ins", S[1] - .1, .8, 80, 10)
R.float3d("#ins", S[1], S[2], (10, 5), (-8, -3), (1, 0))
R.draw("#o304", t304, .6)
R.sfx("tick", t304 + .4)
R.rise("#vw", wt("f01", "views") - .05, .5, 30, 6)
tfv = wt("f01", "five")
R.draw("#o5", tfv - .1, .6)
R.to("#ins", tfv - .15, .6, "{scale: 1.16, x: 130, y: -70}", "expo.inOut")                 # in on "5s"
R.sfx("thump", tfv)
for sel in ("#n304", "#vw", "#ins"):
    R.leave(sel, S[2] - .22, .3)

# ---- f02: the old first line plays on a phone (2x, the timer counts its real seconds) and freezes after "told me"
OLD_LEN = 2.2
tme = R.L["f02"][1]
tv = max(S[2] - .1, tme + .15 - OLD_LEN)
H('<div class="lab" id="fsl" style="top:340px">YOUR FIRST LINE</div>')
H(f'<div class="stage" style="top:410px"><div class="phone big soft" id="ph"><img id="opre" src="assets/img/old_first.jpg" alt="">'
  f'<video id="ov" src="assets/video/old_open_2x.mp4" data-start="{tv:.3f}" data-duration="{OLD_LEN:.2f}" data-track-index="1" muted playsinline></video>'
  '<img id="ofz" src="assets/img/old_freeze.jpg" alt=""><div id="otm"><span id="otn">0.0</span> s</div><b id="x2">2x</b></div></div>')
H(f'<div class="pill" id="left" style="top:1200px"><i style="background:{RED}"></i>Most viewers left here</div>')
R.rise("#fsl", S[2] + .02, .6, 20, 6)
R.rise("#ph", S[2] - .02, .8, 140, 12)
R.float3d("#ph", S[2], S[3], (5, 2), (-10, -4), (1, -.5))
R.counter("otn", tv, OLD_LEN - .05, 0, 4.3, "o.v.toFixed(1)", "none")
R.to("#ph", tv, .7, "{scale: 1.12, y: 40}", "expo.inOut")                 # the phone (not the lens) moves in
tfz = tv + OLD_LEN
R.st("#ofz", tfz - .03, "{opacity: 1}")
R.ft("#ofz", tfz - .03, .5, '{filter: "grayscale(0) brightness(1)"}', '{filter: "grayscale(.9) brightness(.8)"}', "power2.out")
R.to("#ph", tfz - .05, .45, "{scale: 1, y: 0}", "expo.inOut")
R.rise("#left", tfz, .5, 20, 6)
R.sfx("click", tfz)
for sel in ("#fsl", "#ph", "#left"):
    R.leave(sel, S[3] - .22, .3)

# ---- f03: nobody cares about your tool (struck through); say their problem first (rows swap); save this
H(f'<div class="num" id="tool" style="top:360px;font-size:210px;color:rgba(16,19,28,.3)">Tool<i id="strike"></i></div>')
H('<div id="rows" style="top:700px"><div class="row" id="rT"><b>1</b><span>Tool</span><em>"This AI told me..."</em></div>'
  f'<div class="row" id="rP"><b>2</b><span>Problem</span><em>"Your reel loses people at 0:05"</em></div></div>')
H('<div class="save" id="save" style="top:1090px"><i></i>SAVE THIS</div>')
R.rise("#tool", S[3] - .02, .6, 40, 8)
ttool = wt("f03", "tool")
R.ft("#strike", ttool - .05, .4, "{scaleX: 0}", "{scaleX: 1}", "power3.inOut")
R.sfx("click", ttool)
tsay, tprob = wt("f03", "say"), wt("f03", "problem")
R.rise("#rows", tsay - .25, .6, 30, 6)
R.to("#rT", tprob, .6, "{y: 170}", "expo.inOut")
R.to("#rP", tprob, .6, "{y: -170}", "expo.inOut")
R.st("#rT b", tprob + .3, '{textContent: "2"}')
R.st("#rP b", tprob + .3, '{textContent: "1"}')
R.st("#rP", tprob + .3, "{className: 'row on'}")
R.sfx("swish", tprob)
R.sfx("ding", tprob + .35)
R.rise("#save", tprob + .35, .5, 16, 6)
for sel in ("#tool", "#rows", "#save"):
    R.leave(sel, S[4] - .22, .3)

# ---- f04: the name, the comment field types CREE, the share line; cut back to frame 1 so it loops
a4 = S[4]
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div class="cbox soft" id="cbox" style="top:800px"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>')
H('<div class="sub" id="share" style="top:1000px">Send this to the friend<br>whose reels keep flopping.</div>')
H('<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.ft("#logo", a4 - .05, .8, '{opacity: 1, scale: .9, filter: "blur(14px)"}', '{scale: 1, filter: "blur(0px)"}', "expo.out")
R.st("#logo", 0, "{opacity: 0}")
R.sfx("sparkle", wt("f04", "creedom"))
tcm = wt("f04", "comment")
R.to("#logo", tcm - .3, .5, "{y: -230, scale: .7}", "expo.inOut")
R.rise("#cbox", tcm - .2, .6, 40, 8)
R.rise("#cree2", tcm, .7, 60, 10)
tcr = wt("f04", "cree")
R.st("#cph", tcr - .1, "{opacity: 0}")
R.typer("cty", tcr - .1, "CREE", .35)
R.sfx("typing", tcr - .1)
R.ft("#cbox .send", tcr + .45, .5, "{scale: 1.5}", "{scale: 1}", "back.out(3)")
R.sfx("notify", tcr + .5)
R.rise("#share", tcr + .3, .6, 20, 6)
H('<div id="loop"><div class="hd" style="top:330px;font-size:88px">This tool shows the<br>exact second people<br><span style="color:' + RED + '">leave your reel.</span></div></div>')
R.ft("#loop", R.DUR - .4, .35, "{opacity: 0}", "{opacity: 1}", "power2.inOut")

R.captions(top=1470)

R.write(f"""
.lab {{ position: absolute; left: 90px; font-family: Mono; font-size: 28px; letter-spacing: .24em; color: {MUTE}; z-index: 20; }}
.sub {{ position: absolute; left: 90px; right: 90px; font-family: Sat; font-weight: 500; font-size: 48px; line-height: 1.15; letter-spacing: -.02em; color: {MUTE}; z-index: 20; }}
.card {{ position: relative; margin: 0 auto; width: 880px; border-radius: 34px; overflow: hidden; transform-style: preserve-3d; }}
.card img {{ display: block; width: 100%; }}
.card svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
.card rect {{ fill: none; stroke: {RED}; stroke-dasharray: 1; stroke-dashoffset: 1; vector-effect: non-scaling-stroke; stroke-width: 5; }}
.phone {{ position: relative; margin: 0 auto; width: 420px; height: 746px; border-radius: 56px; overflow: hidden; background: #000; border: 10px solid {INK}; }}
.phone img, .phone video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#ofz {{ opacity: 0; }}
#otm {{ position: absolute; left: 50%; top: 24px; transform: translateX(-50%); background: rgba(16,19,28,.82); color: #fff; font-family: Mono; font-size: 38px; padding: 8px 22px; border-radius: 999px; }}
#x2 {{ position: absolute; right: 20px; bottom: 20px; background: rgba(16,19,28,.82); color: #fff; font-family: Mono; font-size: 28px; padding: 6px 14px; border-radius: 10px; }}
.pill {{ position: absolute; left: 50%; transform: translateX(-50%); white-space: nowrap; display: flex; align-items: center; gap: 18px; background: #fff; padding: 22px 36px;
  border-radius: 999px; font-family: Sat; font-weight: 700; font-size: 46px; box-shadow: 0 20px 50px rgba(40,50,90,.16); z-index: 22; }}
.pill i {{ width: 16px; height: 16px; border-radius: 50%; }}
#strike {{ position: absolute; left: -10px; right: -10px; top: 52%; height: 10px; background: {RED}; border-radius: 5px; transform-origin: left center; transform: scaleX(0); }}
#rows {{ position: absolute; left: 90px; right: 90px; z-index: 20; height: 340px; }}
.row {{ position: absolute; left: 0; right: 0; height: 150px; display: flex; align-items: center; gap: 30px; border-top: 2px solid rgba(16,19,28,.1); }}
#rT {{ top: 0; }} #rP {{ top: 170px; border-bottom: 2px solid rgba(16,19,28,.1); }}
.row b {{ font-family: Unb; font-weight: 900; font-size: 54px; width: 70px; color: {MUTE}; }}
.row span {{ font-family: Sat; font-weight: 900; font-size: 72px; letter-spacing: -.03em; }}
.row em {{ margin-left: auto; font-style: normal; font-family: Sat; font-weight: 500; font-size: 34px; color: {MUTE}; max-width: 360px; text-align: right; line-height: 1.15; }}
.row.on b {{ color: {GREEN}; }}
.save {{ position: absolute; left: 90px; font-family: Mono; font-size: 36px; letter-spacing: .24em; color: {GREEN}; z-index: 20; display: flex; align-items: center; gap: 16px; }}
.save i {{ width: 28px; height: 34px; border: 4px solid {GREEN}; border-bottom: none; border-radius: 4px 4px 0 0; position: relative; }}
#logo {{ position: absolute; left: 140px; right: 140px; top: 560px; height: 280px; display: grid; place-items: center; z-index: 25; }}
#logo img {{ width: 100%; }}
.an {{ position: relative; margin: 0 auto; width: 900px; border-radius: 40px; padding: 38px 40px 44px; background: rgba(255,255,255,.92); }}
.anh {{ display: flex; align-items: center; justify-content: space-between; }}
.anh img {{ height: 64px; }}
.anh span {{ font-family: Mono; font-size: 26px; letter-spacing: .18em; color: {MUTE}; }}
.chart {{ position: relative; margin-top: 30px; height: 360px; border-radius: 26px; background: #f4f6fb; padding: 22px; }}
.chart svg {{ width: 100%; height: 100%; overflow: visible; }}
#ret0 {{ fill: none; stroke: {INK}; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: 0; vector-effect: non-scaling-stroke; }}
#drop0 {{ position: absolute; left: 31%; top: 33%; width: 32px; height: 32px; border-radius: 50%; background: {RED}; box-shadow: 0 0 0 12px rgba(226,57,47,.16); }}
#dl0 {{ position: absolute; left: 37%; top: 9%; background: {INK}; color: #fff; font-family: Sat; font-weight: 700; font-size: 36px; padding: 10px 20px; border-radius: 14px; }}
#cree2 {{ position: absolute; right: 90px; top: 1060px; width: 250px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
.cbox {{ position: absolute; left: 90px; width: 820px; height: 140px; border-radius: 70px; background: #fff; display: flex; align-items: center; gap: 24px; padding: 0 34px;
  font-family: Sat; font-weight: 900; font-size: 64px; letter-spacing: .02em; z-index: 22; }}
.cbox .av {{ width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 142px; color: rgba(16,19,28,.35); font-weight: 500; font-size: 48px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: {PINK}; font-size: 54px; }}
#loop {{ position: absolute; inset: -60px; opacity: 0; z-index: 50; background: linear-gradient(180deg, #f7f8fc, #eceff7); }}
#loop .hd {{ transform: translate(60px, 60px); }}
""")
