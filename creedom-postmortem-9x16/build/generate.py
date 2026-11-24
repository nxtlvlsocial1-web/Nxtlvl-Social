"""Creedom remake 1 v5, "What went wrong" (304 views), Creators 100X 9:16: writes index.html, plan/sfx_events.json, plan/edit.json.

v5 (owner: v4 "perfect except not engaging in the first 7 seconds and boring after"; "can't use ElevenLabs anymore"):
the v6 script ("The only video you need to stop the scroll", about 19 s, plan/elevenlabs_vo_v6.md wording with "video"
in the hook), voiced with Kokoro af_heart (build/vo_kok.py). Same clean premium minimal look (Glacier, Unbounded +
Satoshi, build/kit_min.py), but the hook text and the real 304 card are on frame 1, the irony lands by 6 s, and inside
every scene the lens moves in on a detail or a new element lands every 1-2 s, with sound hits on the beats.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_min import GREEN, INK, MUTE, PINK, RED, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: what went wrong v5 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.push(S[k] - .1, S[k + 1], .035)
    if k:
        R.sfx("swish", S[k] - .16)
R.sfx("thump", .02)

# ---- f00: the hook line and the real 304 card, both on frame 1; the lens moves in on 304 at "stop the scroll"
H('<div class="hd" id="hk" style="top:300px;font-size:100px"><span class="ln"><span>The only video</span></span><span class="ln"><span>you need to</span></span>'
  f'<span class="ln"><span style="color:{RED}">stop the scroll.</span></span></div>')
H('<div class="stage" style="top:800px"><div class="card soft" id="ins"><img src="assets/img/insights_cards.jpg" alt="">'
  '<svg viewBox="0 0 100 100" preserveAspectRatio="none"><rect id="o304" x="1.4" y="1" width="47" height="46.5" rx="4" pathLength="1" /></svg></div></div>')
R.kicker("WHAT WENT WRONG", .1, S[3] - .2)
R.js('tl.fromTo("#hk .ln > span", {y: 12, filter: "blur(3px)"}, {y: 0, filter: "blur(0px)", duration: .45, ease: "expo.out", stagger: .06, immediateRender: true}, 0);')   # readable on frame 1
R.st("#ins", 0, "{opacity: 1}")
R.ft("#ins", 0, 1.0, "{y: 40, rotationX: 22, rotationY: -16}", "{y: 0, rotationX: 10, rotationY: -8}")
R.draw("#o304", .5, .7)
R.sfx("tick", .55)
tst = wt("f00", "stop")
R.to("#ins", tst - .1, .7, "{scale: 1.28, x: 120, y: -10}", "expo.inOut")      # the card (not the hook) moves in on 304
R.sfx("swish", tst - .1)
R.leave("#hk", S[1] - .25, .3)
R.leave("#ins", S[1] - .25, .3)

# ---- f01: 304 counts in, views; the old cover slides in; "stop watching." lands red (the irony, by 6 s)
H(f'<div class="num" id="n304" style="top:310px;font-size:200px;color:{RED}">0</div>')
H('<div class="hd" id="vw" style="top:530px">views,</div>')
H('<div class="stage" style="top:330px"><div class="phone soft" id="oldp" style="left:330px"><img src="assets/img/old_cover.png" alt=""><i class="hide"></i></div></div>')
H('<div class="hd" id="irony" style="top:960px;font-size:84px"><span class="ln"><span><em>on a reel about</em></span></span><span class="ln"><span><em>why people</em></span></span>'
  f'<span class="ln"><span style="color:{RED}">stop watching.</span></span></div>')
t304 = wt("f01", "304")
R.rise("#n304", t304 - .05, .6, 40, 8)
R.counter("n304", t304 - .05, .55, 0, 304)
R.sfx("tick", t304 + .4)
R.rise("#vw", wt("f01", "views") - .05, .6, 30, 6)
ton = wt("f01", "on")
R.rise("#oldp", ton - .1, .9, 120, 12)
R.float3d("#oldp", ton - .1, S[2], (6, 3), (-16, -8), (3, 1))
R.sfx("swish", ton - .1)
tsw = wt("f01", "stop")
R.mask_lines("#irony", wt("f01", "about") - .1)
R.ft("#irony .ln:nth-child(3) > span", tsw, .45, "{scale: 1.12}", "{scale: 1}", "back.out(2.5)")
R.sfx("thump", tsw)
R.focus(tsw - .05, 1.06, 0, -30, .5, "expo.out")
for sel in ("#n304", "#vw", "#oldp", "#irony"):
    R.leave(sel, S[2] - .22, .3)
R.focus(S[2] - .2, 1.0, 0, 0, .4)

# ---- f02: the old first line plays on a phone (2x, the timer counts its real seconds), freezes on "They"; 5 s lands
tthey, tfive = wt("f02", "they"), wt("f02", "five")
OLD_LEN = 2.2
tv = max(S[2] - .1, tthey - OLD_LEN)
H('<div class="lab" id="fsl" style="top:330px">YOUR FIRST LINE</div>')
H(f'<div class="stage" style="top:400px"><div class="phone big soft" id="ph"><img id="opre" src="assets/img/old_first.jpg" alt="">'
  f'<video id="ov" src="assets/video/old_open_2x.mp4" data-start="{tv:.3f}" data-duration="{OLD_LEN:.2f}" data-track-index="1" muted playsinline></video>'
  '<img id="ofz" src="assets/img/old_freeze.jpg" alt=""><div id="otm"><span id="otn">0.0</span> s</div><b id="x2">2x</b></div></div>')
H(f'<div id="five"><b><i id="fn">0</i><small>s</small></b><span>average watch</span></div>')
R.rise("#fsl", S[2] + .02, .6, 20, 6)
R.rise("#ph", S[2] - .02, .8, 140, 12)
R.float3d("#ph", S[2], S[3], (5, 2), (-10, -4), (1, -.5))
R.counter("otn", tv, OLD_LEN - .05, 0, 4.3, "o.v.toFixed(1)", "none")
R.focus(S[2] + .5, 1.22, 0, 150, .8)                         # in on the timer while the old line plays
R.ft("#otm", wt("f02", "this") - .05, .4, "{scale: 1.25}", "{scale: 1}", "back.out(2.5)")
R.st("#ofz", tthey - .03, "{opacity: 1}")
R.ft("#ofz", tthey - .03, .5, '{filter: "grayscale(0) brightness(1)"}', '{filter: "grayscale(.9) brightness(.8)"}', "power2.out")
R.focus(tthey - .05, 1.0, 0, 0, .5)
R.sfx("click", tthey)
R.rise("#five", tfive - .15, .5, 30, 8)
R.counter("fn", tfive - .1, .5, 0, 5, "Math.round(o.v)", "steps(5)")
R.sfx("thump", tfive)
for sel in ("#fsl", "#ph", "#five"):
    R.leave(sel, S[3] - .22, .3)

# ---- f03: nobody cares about your tool (struck through); say their problem first (rows swap); save this
H(f'<div class="num" id="tool" style="top:360px;font-size:210px;color:rgba(16,19,28,.3)">Tool<i id="strike"></i></div>')
H('<div id="rows" style="top:700px"><div class="row" id="rT"><b>1</b><span>Tool</span><em>"This AI told me..."</em></div>'
  f'<div class="row" id="rP"><b>2</b><span>Problem</span><em>"Your reel loses people at 0:05"</em></div></div>')
H(f'<div class="save" id="save" style="top:1090px"><i></i>SAVE THIS</div>')
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
R.rise("#save", tprob + .4, .5, 16, 6)
for sel in ("#tool", "#rows", "#save"):
    R.leave(sel, S[4] - .22, .3)

# ---- f04: Creedom (about 72 % in): the logo, the analyser card, the drop point
a4 = S[4]
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div class="stage" style="top:420px"><div class="an soft" id="an"><div class="anh"><img src="assets/img/creedom_logo.png" alt=""><span>REEL ANALYZER</span></div>'
  '<div class="chart"><svg viewBox="0 0 600 260" preserveAspectRatio="none"><path id="ret" d="M0,30 C60,32 90,36 110,44 C130,54 140,160 160,190 C200,215 300,222 600,230" pathLength="1"/></svg>'
  '<i id="drop"></i><b id="dropl">Viewers leave at 0:05</b></div>'
  '<div class="why" id="why"><b>WHY</b><span>The hook names a tool, not the viewer\'s problem.</span></div></div></div>')
H('<img id="cree" src="assets/img/poses/mag.png" alt="">')
R.kicker("CREEDOM", a4 - .05, S[5] - .2, PINK)
R.st("#logo", 0, "{opacity: 0}")
R.ft("#logo", a4 - .05, .8, '{opacity: 1, scale: .9, filter: "blur(14px)"}', '{scale: 1, filter: "blur(0px)"}', "expo.out")
R.sfx("sparkle", a4)
tsh = wt("f04", "shows")
R.leave("#logo", tsh - .12, .3, -60)
R.rise("#an", tsh - .05, .8, 120, 12)
R.float3d("#an", tsh, S[5], (8, 4), (-10, -4), (1, 0))
R.draw("#ret", tsh + .2, .7)
tex = wt("f04", "exact")
R.ft("#drop", tex - .05, .45, "{opacity: 1, scale: 0}", "{scale: 1}", "back.out(3)")
R.st("#drop", 0, "{opacity: 0}")
R.focus(tex - .05, 1.14, 110, 40, .6)                         # in on the drop point
R.sfx("click", tex)
R.rise("#dropl", wt("f04", "people") - .1, .5, 16, 6)
R.focus(wt("f04", "leave") + .05, 1.0, 0, 0, .5)
R.rise("#why", wt("f04", "leave") + .1, .5, 20, 6)
R.rise("#cree", wt("f04", "leave"), .7, 60, 10)
for sel in ("#an", "#cree"):
    R.leave(sel, S[5] - .22, .3)

# ---- f05: CTA (CREE) + the share line on screen; the comment field types it; cut back to frame 1 so it loops
a5 = S[5]
H(R.lines_html("h5", ["Send this to the friend", "<em>whose reels keep flopping.</em>"], "hd").replace('id="h5"', 'id="h5" style="top:330px;font-size:84px"'))
H('<div class="cbox soft" id="cbox" style="top:720px"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>')
H('<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.mask_lines("#h5", a5 - .1)
R.rise("#cbox", a5 + .05, .6, 40, 8)
R.rise("#cree2", a5 + .3, .7, 60, 10)
tcr = wt("f05", "cree")
R.st("#cph", tcr - .1, "{opacity: 0}")
R.typer("cty", tcr - .1, "CREE", .35)
R.sfx("typing", tcr - .1)
R.ft("#cbox .send", tcr + .45, .5, "{scale: 1.5}", "{scale: 1}", "back.out(3)")
R.sfx("notify", tcr + .5)
H('<div id="loop"><div class="hd" style="top:300px;font-size:100px">The only video<br>you need to<br><span style="color:' + RED + '">stop the scroll.</span></div>'
  '<div class="stage" style="top:800px"><div class="card" style="opacity:1;transform:rotateX(22deg) rotateY(-16deg) translateY(40px)"><img src="assets/img/insights_cards.jpg" alt=""></div></div></div>')
R.ft("#loop", R.DUR - .4, .35, "{opacity: 0}", "{opacity: 1}", "power2.inOut")

R.captions(top=1470)

R.write(f"""
.lab {{ position: absolute; left: 90px; font-family: Mono; font-size: 28px; letter-spacing: .24em; color: {MUTE}; z-index: 20; }}
.card {{ position: relative; margin: 0 auto; width: 880px; border-radius: 34px; overflow: hidden; opacity: 0; transform-style: preserve-3d; }}
.card img {{ display: block; width: 100%; }}
.card svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
#o304 {{ fill: none; stroke: {RED}; stroke-dasharray: 1; stroke-dashoffset: 1; vector-effect: non-scaling-stroke; stroke-width: 5; }}
.phone {{ position: relative; margin: 0 auto; width: 320px; height: 569px; border-radius: 46px; overflow: hidden; background: #000; border: 10px solid {INK}; opacity: 0; }}
#oldp {{ margin: 0 0 0 auto; right: 80px; left: auto !important; }}
.phone.big {{ width: 420px; height: 746px; border-radius: 56px; }}
.phone img, .phone video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.hide {{ position: absolute; left: 22%; right: 22%; top: 83%; height: 8%; border-radius: 12px; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: rgba(255,220,236,.55); }}
#ofz {{ opacity: 0; }}
#otm {{ position: absolute; left: 50%; top: 24px; transform: translateX(-50%); background: rgba(16,19,28,.82); color: #fff; font-family: Mono; font-size: 38px; padding: 8px 22px; border-radius: 999px; }}
#x2 {{ position: absolute; right: 20px; bottom: 20px; background: rgba(16,19,28,.82); color: #fff; font-family: Mono; font-size: 28px; padding: 6px 14px; border-radius: 10px; }}
.quote {{ position: absolute; left: 0; right: 0; text-align: center; font-family: Sat; font-weight: 700; font-size: 54px; letter-spacing: -.02em; color: {INK}; z-index: 22; }}
#five {{ position: absolute; left: 730px; top: 380px; width: 270px; height: 270px; border-radius: 50%; background: #fff; display: flex; flex-direction: column; align-items: center;
  justify-content: center; z-index: 24; box-shadow: 0 30px 60px rgba(40,50,90,.18); opacity: 0; }}
#five b {{ font-family: Unb; font-weight: 900; color: {RED}; line-height: 1; }}
#five b i {{ font-style: normal; font-size: 120px; letter-spacing: -.06em; }}
#five b small {{ font-size: 50px; }}
#five span {{ font-family: Mono; font-size: 20px; letter-spacing: .14em; color: {MUTE}; margin-top: 8px; text-transform: uppercase; }}
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
#cree {{ position: absolute; right: 70px; top: 1120px; width: 230px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
#cree2 {{ position: absolute; right: 90px; top: 920px; width: 260px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
.cbox {{ position: absolute; left: 90px; width: 820px; height: 140px; border-radius: 70px; background: #fff; display: flex; align-items: center; gap: 24px; padding: 0 34px;
  font-family: Sat; font-weight: 900; font-size: 64px; letter-spacing: .02em; z-index: 22; }}
.cbox .av {{ width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 142px; color: rgba(16,19,28,.35); font-weight: 500; font-size: 48px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: {PINK}; font-size: 54px; }}
#loop {{ position: absolute; inset: -60px; opacity: 0; z-index: 50; background: linear-gradient(180deg, #f7f8fc, #eceff7); }}
#loop .hd {{ transform: translate(60px, 60px); }}
#loop .stage {{ transform: translateY(60px); }}
""")
