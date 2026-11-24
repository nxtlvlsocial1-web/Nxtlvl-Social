"""Creedom remake 2 v5, "Graded before anyone saw it" (Creators 100X, 9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

v5 (owner: v4 "perfect except not engaging in the first 7 seconds and boring after"; "can't use ElevenLabs anymore"):
the v6 script ("The only video you need before you hit post", about 20 s), voiced with Kokoro af_heart
(build/vo_kok.py). Same clean premium minimal look (Glacier, Unbounded + Satoshi, build/kit_min.py). The hook text and
the example reel (EXAMPLE tag) are on frame 1 with a Post button pressed on "post"; the score lands by 4 s; inside every
scene the lens moves in on a detail or a new element lands every 1-2 s, with sound hits on the beats.
The scores are an example (owner: make them): 2.9 / 5 -> 4.4 / 5, flags at 0:01, 0:07, 0:14.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_min import GREEN, INK, MUTE, PINK, RED, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: graded before anyone saw it v5 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.push(S[k] - .1, S[k + 1], .035)
    if k:
        R.sfx("swish", S[k] - .16)
R.sfx("thump", .02)


def ring_to(t, frm, score, d=.7, col=RED):
    R.js(f'tl.to("#arc", {{strokeDashoffset: {1 - score / 5:.4f}, stroke: "{col}", duration: {d}, ease: "power3.out"}}, {t:.3f});')
    R.counter("score", t, d, frm, score, "o.v.toFixed(1)", "power3.out")


# ---- f00: hook text + the example reel on a phone + a Post button, all on frame 1; the button is pressed on "post"
H('<div class="hd" id="hk" style="top:280px;font-size:92px"><span class="ln"><span>The only video</span></span><span class="ln"><span>you need before</span></span>'
  f'<span class="ln"><span style="color:{RED}">you hit post.</span></span></div>')
H('<div class="stage" style="top:620px"><div class="phone soft" id="ph"><img id="frame" src="assets/img/demo_f01.jpg" alt=""><b class="ex">EXAMPLE</b></div></div>')
H('<div class="post" id="post" style="top:1130px"><i></i>Post reel</div>')
R.js('tl.fromTo("#hk .ln > span", {y: 12, filter: "blur(3px)"}, {y: 0, filter: "blur(0px)", duration: .45, ease: "expo.out", stagger: .06, immediateRender: true}, 0);')
R.st("#ph, #post", 0, "{opacity: 1}")
R.ft("#ph", 0, 1.0, "{y: 50, rotationY: 26, rotationX: 8}", "{y: 0, rotationY: 16, rotationX: 4}")
R.float3d("#ph", 1.0, S[3], (4, 2), (16, 10), (-1, 0))
R.ft("#post", .1, .6, "{x: 60}", "{x: 0}")
tpo = wt("f00", "post")
R.ft("#post", tpo - .05, .35, "{scale: .9}", "{scale: 1}", "back.out(3)")
R.st("#post", tpo, "{className: 'post hold'}")
R.sfx("click", tpo)
R.leave("#hk", S[1] - .25, .3)

# ---- f01: the score lands (2.9, red) before posting; "before anyone saw it" takes the hook's place
H('<div id="sc"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" class="trk"/><circle cx="100" cy="100" r="96" class="arc" id="arc" pathLength="1"/></svg>'
  '<div class="n"><b id="score">0.0</b><span>out of 5</span></div></div>')
H(R.lines_html("hb", ["Before anyone", "<em>saw it.</em>"], "hd").replace('id="hb"', 'id="hb" style="top:300px;font-size:92px"'))
tsc = wt("f01", "scored")
R.rise("#sc", tsc - .15, .6, 40, 8)
R.js('tl.set("#arc", {strokeDashoffset: 1}, 0);')
ring_to(tsc, 0, 2.9, .9)
R.sfx("tick", tsc + .85)
R.to("#sc", wt("f01", "out") - .1, .6, "{scale: 1.12}", "expo.out")       # the score grows (the lens would crop the text)
R.mask_lines("#hb", wt("f01", "before") - .1)
R.ft("#post", wt("f01", "before"), .4, "{x: 0}", "{keyframes: [{x: -10, duration: .06}, {x: 9, duration: .06}, {x: -5, duration: .06}, {x: 0, duration: .1}]}", "none")
R.sfx("thump", wt("f01", "before"))
R.leave("#hb", S[2] - .22, .3)
R.leave("#post", S[2] - .22, .3)

# ---- f02: each flagged second: the phone cuts to it, a row and a tick on the timeline land
a2 = S[2]
R.to("#sc", a2 - .2, .6, "{x: 80, y: -330, scale: .62}", "expo.inOut")
H('<div id="tline" style="top:1330px"><i class="bar"></i>' + "".join(
    f'<i class="tk" id="tk{k}" style="left:{x}%"><em>{lab}</em></i>' for k, (x, lab) in enumerate([(6, "0:01"), (40, "0:07"), (78, "0:14")])) + '</div>')
NOTES = [("one", "demo_f01.jpg", "0:01", "Slow hook"), ("seven", "demo_f07.jpg", "0:07", "No proof"), ("fourteen", "demo_f14.jpg", "0:14", "Lost trust")]
H('<div id="list" style="top:700px">' + "".join(
    f'<div class="row" id="r{k}"><b>{ts}</b><span>{txt}</span><i class="dot"></i><i class="ok">&#10003;</i></div>' for k, (_, _, ts, txt) in enumerate(NOTES)) + '</div>')
R.rise("#tline", a2 - .05, .5, 16, 6)
for k, (word, img, ts, txt) in enumerate(NOTES):
    tw = wt("f02", word)
    R.st("#frame", tw - .05, f'{{attr: {{src: "assets/img/{img}"}}}}')
    R.ft("#frame", tw - .05, .6, "{scale: 1.1}", "{scale: 1}", "expo.out")
    R.rise(f"#r{k}", tw - .05, .5, 30, 8)
    R.ft(f"#tk{k}", tw - .05, .45, "{scale: 1.5}", "{scale: 1}", "back.out(2.5)")
    R.st(f"#tk{k}", tw - .05, "{className: 'tk on'}")
    R.sfx("click", tw)
    R.focus(tw - .05, 1.06 + .02 * k, 0, -10 * k, .45, "expo.out")

# ---- f03: fix those three: the dots turn into green checks, the score climbs to 4.4
a3 = S[3]
R.focus(a3 - .1, 1.0, 0, 0, .4)
tfx = wt("f03", "three")
for k in range(3):
    tk = tfx - .1 + k * .14
    R.st(f"#r{k}", tk, "{className: 'row fixed'}")
    R.ft(f"#r{k} .ok", tk, .4, "{opacity: 1, scale: 0}", "{scale: 1}", "back.out(3)")
    R.st(f"#tk{k}", tk, "{className: 'tk fixed'}")
    R.sfx("click", tk)
t44 = wt("f03", "4.4")
R.to("#sc", wt("f03", "scores") - .3, .5, "{x: 80, y: -330, scale: .78}", "expo.inOut")
ring_to(t44 - .1, 2.9, 4.4, .8, GREEN)
R.sfx("thump", t44)
R.sfx("g_correct", t44 + .15)

# ---- f04: Creedom (about 74 % in): the logo, then the app card
a4 = S[4]
for sel in ("#ph", "#sc", "#list", "#tline"):
    R.leave(sel, a4 - .22, .3)
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div class="stage" style="top:480px"><div class="app soft" id="app"><img src="assets/img/creedom_logo.png" alt=""><div class="q">How can Cree help?</div>'
  '<div class="tile" id="t1"><i>&#10003;</i><div><b>Check a reel before you post</b><span>Score out of 5, the exact second, and the fix</span></div></div>'
  '<div class="tile dim"><i>&#9998;</i><div><b>Get a script in your voice</b></div></div></div></div>')
H('<img id="cree" src="assets/img/poses/proud.png" alt="">')
R.kicker("CREEDOM", a4 - .05, S[5] - .2, PINK)
R.st("#logo", 0, "{opacity: 0}")
R.ft("#logo", a4 - .05, .8, '{opacity: 1, scale: .9, filter: "blur(14px)"}', '{scale: 1, filter: "blur(0px)"}', "expo.out")
R.sfx("sparkle", a4)
tit = wt("f04", "it")
R.leave("#logo", tit - .12, .3, -60)
R.rise("#app", tit - .05, .8, 120, 12)
R.float3d("#app", tit, S[5], (8, 4), (-10, -4), (1, 0))
R.rise("#cree", tit + .3, .7, 60, 10)
tbf = wt("f04", "before")
R.ft("#t1", tbf - .05, .45, "{scale: 1.05}", "{scale: 1}", "back.out(2)")
R.focus(tbf - .05, 1.1, 0, 40, .5, "expo.out")
R.sfx("click", tbf)
for sel in ("#app", "#cree"):
    R.leave(sel, S[5] - .22, .3)
R.focus(S[5] - .2, 1.0, 0, 0, .4)

# ---- f05: CTA (CHECK) + the share line on screen; the comment field types it; cut back to frame 1 so it loops
a5 = S[5]
H(R.lines_html("h5", ["Send this to the friend", "<em>who posts and prays.</em>"], "hd").replace('id="h5"', 'id="h5" style="top:330px;font-size:84px"'))
H('<div class="cbox soft" id="cbox" style="top:720px"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>')
H('<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.mask_lines("#h5", a5 - .1)
R.rise("#cbox", a5 + .05, .6, 40, 8)
R.rise("#cree2", a5 + .3, .7, 60, 10)
tck = wt("f05", "check")
R.st("#cph", tck - .1, "{opacity: 0}")
R.typer("cty", tck - .1, "CHECK", .4)
R.sfx("typing", tck - .1)
R.ft("#cbox .send", tck + .5, .5, "{scale: 1.5}", "{scale: 1}", "back.out(3)")
R.sfx("notify", tck + .55)
H('<div id="loop"><div class="hd" style="top:280px;font-size:92px">The only video<br>you need before<br><span style="color:' + RED + '">you hit post.</span></div>'
  '<div class="lp"><img src="assets/img/demo_f01.jpg" alt=""></div></div>')
R.ft("#loop", R.DUR - .4, .35, "{opacity: 0}", "{opacity: 1}", "power2.inOut")

R.captions(top=1470)

R.write(f"""
.phone {{ position: relative; left: 100px; width: 380px; height: 676px; border-radius: 52px; overflow: hidden; background: #000; border: 10px solid {INK}; opacity: 0; }}
.phone img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.ex {{ position: absolute; left: 22px; top: 22px; background: rgba(16,19,28,.72); color: #fff; font-family: Mono; font-size: 22px; letter-spacing: .18em; padding: 6px 12px; border-radius: 8px; }}
.post {{ position: absolute; left: 560px; display: flex; align-items: center; gap: 18px; background: {INK}; color: #fff; padding: 26px 44px; border-radius: 999px; font-family: Sat;
  font-weight: 700; font-size: 46px; opacity: 0; z-index: 22; box-shadow: 0 20px 50px rgba(40,50,90,.2); }}
.post i {{ width: 18px; height: 18px; border-radius: 50%; background: #8ea2ff; }}
.post.hold {{ background: #2a2f3d; }}
.post.hold i {{ background: {RED}; }}
#sc {{ position: absolute; left: 560px; top: 660px; width: 420px; height: 420px; opacity: 0; z-index: 20; transform-origin: 50% 50%; }}
#sc svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
#sc .trk {{ fill: none; stroke: rgba(16,19,28,.1); stroke-width: 2; }}
#sc .arc {{ fill: none; stroke: {RED}; stroke-width: 4; stroke-linecap: round; stroke-dasharray: 1; }}
#sc .n {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
#sc .n b {{ font-family: Unb; font-weight: 900; font-size: 140px; letter-spacing: -.06em; line-height: 1; }}
#sc .n span {{ font-family: Sat; font-weight: 500; font-size: 40px; color: {MUTE}; margin-top: 10px; }}
#tline {{ position: absolute; left: 100px; width: 380px; height: 70px; opacity: 0; z-index: 20; }}
#tline .bar {{ position: absolute; left: 0; right: 0; top: 30px; height: 3px; background: rgba(16,19,28,.14); border-radius: 2px; }}
.tk {{ position: absolute; top: 18px; width: 0; }}
.tk::before {{ content: ""; position: absolute; left: -9px; top: 3px; width: 18px; height: 18px; border-radius: 50%; background: #fff; border: 3px solid rgba(16,19,28,.3); }}
.tk em {{ position: absolute; left: -40px; top: 36px; width: 80px; text-align: center; font-style: normal; font-family: Mono; font-size: 24px; color: rgba(16,19,28,.78); }}
.tk.on::before {{ background: {RED}; border-color: {RED}; }}
.tk.fixed::before {{ background: {GREEN}; border-color: {GREEN}; }}
#list {{ position: absolute; left: 560px; right: 70px; z-index: 20; }}
.row {{ position: relative; display: flex; flex-direction: column; padding: 24px 60px 24px 0; border-top: 2px solid rgba(16,19,28,.1); opacity: 0; }}
.row:last-child {{ border-bottom: 2px solid rgba(16,19,28,.1); }}
.row b {{ font-family: Mono; font-size: 30px; color: {RED}; }}
.row span {{ font-family: Sat; font-weight: 900; font-size: 56px; letter-spacing: -.02em; line-height: 1.05; margin-top: 4px; }}
.row .dot {{ position: absolute; right: 8px; top: 50%; margin-top: -8px; width: 16px; height: 16px; border-radius: 50%; background: {RED}; }}
.row .ok {{ position: absolute; right: 0; top: 50%; margin-top: -22px; width: 44px; height: 44px; border-radius: 50%; background: {GREEN}; color: #fff; display: grid; place-items: center;
  font-style: normal; font-weight: 900; font-size: 26px; opacity: 0; }}
.row.fixed b {{ color: {GREEN}; }} .row.fixed .dot {{ opacity: 0; }}
#logo {{ position: absolute; left: 140px; right: 140px; top: 640px; height: 280px; display: grid; place-items: center; z-index: 25; }}
#logo img {{ width: 100%; }}
.app {{ position: relative; margin: 0 auto; width: 900px; border-radius: 40px; padding: 40px 40px 44px; background: rgba(255,255,255,.92); opacity: 0; }}
.app img {{ height: 70px; display: block; }}
.q {{ margin: 26px 0 24px; font-family: Sat; font-weight: 900; font-size: 64px; letter-spacing: -.03em; }}
.tile {{ display: flex; gap: 24px; align-items: center; background: #f4f6fb; border-radius: 28px; padding: 26px 28px; margin-top: 16px; border: 2px solid {GREEN}; }}
.tile i {{ width: 80px; height: 80px; border-radius: 22px; background: {GREEN}; color: #fff; display: grid; place-items: center; font-style: normal; font-size: 38px; flex: none; }}
.tile b {{ display: block; font-family: Sat; font-weight: 900; font-size: 44px; letter-spacing: -.02em; line-height: 1.08; }}
.tile span {{ display: block; font-family: Sat; font-weight: 500; font-size: 32px; color: {MUTE}; margin-top: 6px; }}
.tile.dim {{ border-color: transparent; opacity: .55; }}
.tile.dim i {{ background: #cfd4e0; color: {INK}; }}
#cree {{ position: absolute; right: 70px; top: 1130px; width: 240px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
#cree2 {{ position: absolute; right: 90px; top: 920px; width: 260px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
.cbox {{ position: absolute; left: 90px; width: 820px; height: 140px; border-radius: 70px; background: #fff; display: flex; align-items: center; gap: 24px; padding: 0 34px;
  font-family: Sat; font-weight: 900; font-size: 64px; letter-spacing: .02em; z-index: 22; }}
.cbox .av {{ width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 142px; color: rgba(16,19,28,.35); font-weight: 500; font-size: 48px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: {PINK}; font-size: 54px; }}
#loop {{ position: absolute; inset: -60px; opacity: 0; z-index: 50; background: linear-gradient(180deg, #f7f8fc, #eceff7); }}
#loop .hd {{ transform: translate(60px, 60px); }}
#loop .lp {{ position: absolute; left: 160px; top: 680px; width: 380px; height: 676px; border-radius: 52px; overflow: hidden; border: 10px solid {INK};
  transform: perspective(1900px) rotateY(26deg) rotateX(8deg) translateY(50px); }}
#loop .lp img {{ width: 100%; height: 100%; object-fit: cover; }}
""")
