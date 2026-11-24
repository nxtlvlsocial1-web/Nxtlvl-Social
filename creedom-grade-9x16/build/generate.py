"""Creedom remake 2 v4, "Graded before anyone saw it" (Creators 100X, 9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

v4 (owner, after v1-v3 "dull", "generic"): clean premium minimal on the Glacier background, Unbounded + Satoshi
(build/kit_min.py, same as creedom-postmortem-9x16), the owner's ElevenLabs take ("Blondie - Intense Woman",
build/vo_el2.py). The scores are an example (owner: make them), shown with an EXAMPLE tag: 2.9 / 5 -> 4.4 / 5, flags at
0:01, 0:07, 0:14. Frame 1: the reel on a phone and its score; Harsh; each flagged second as a clean list; the fix and the
climb to 4.4; Creedom at about 65 %; CTA CHECK; a cut back to frame 1 so it loops. v1-v3 (pink kinetic) are in git history.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_min import GREEN, INK, MUTE, PINK, RED, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: graded before anyone saw it v4 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.push(S[k] - .1, S[k + 1], .04)
    if k:
        R.sfx("swish", S[k] - .16)


def ring_to(t, frm, score, d=.8, col=RED):
    """the ring and the number move together, pure functions of the timeline"""
    R.js(f'tl.to("#arc", {{strokeDashoffset: {1 - score / 5:.4f}, stroke: "{col}", duration: {d}, ease: "power3.out"}}, {t:.3f});')
    R.counter("score", t, d, frm, score, "o.v.toFixed(1)", "power3.out")


# ---- f00: phone + score at frame 1
H('<div class="stage" style="top:430px"><div class="phone soft" id="ph"><img id="frame" src="assets/img/demo_f01.jpg" alt=""><b class="ex">EXAMPLE</b></div></div>')
H('<div id="sc"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" class="trk"/><circle cx="100" cy="100" r="96" class="arc" id="arc" pathLength="1"/></svg>'
  '<div class="n"><b id="score">2.6</b><span>out of 5</span></div></div>')
R.kicker("REEL SCORE  /  EXAMPLE", .1, S[4] - .2)
R.st("#ph, #sc", 0, "{opacity: 1}")
R.ft("#ph", 0, 1.1, "{y: 60, rotationY: 26, rotationX: 8}", "{y: 0, rotationY: 16, rotationX: 4}")
R.float3d("#ph", 1.1, S[2], (4, 2), (16, 10), (-1, 0))
R.ft("#sc", 0, .9, "{y: 30}", "{y: 0}")
R.js(f'tl.set("#arc", {{strokeDashoffset: {1 - 2.6 / 5:.3f}}}, 0);')
ring_to(.05, 2.6, 2.9, .6)
R.sfx("tick", .6)
tb = wt("f00", "before")
H(R.lines_html("hb", ["Before anyone", "<em>saw it.</em>"], "hd").replace('id="hb"', 'id="hb" style="top:1190px"'))
R.mask_lines("#hb", tb - .05)
R.leave("#hb", S[1] - .18)

# ---- f01: Harsh. Then where it lost points: a timeline under the phone
H(f'<div class="num" id="harsh" style="top:1190px;font-size:150px;color:{RED}">Harsh.</div>')
H('<div id="tline" style="top:1190px"><i class="bar"></i>' + "".join(
    f'<i class="tk" id="tk{k}" style="left:{x}%"><em>{lab}</em></i>' for k, (x, lab) in enumerate([(6, "0:01"), (40, "0:07"), (78, "0:14")])) + '</div>')
R.rise("#harsh", S[1] - .02, .7, 40, 10)
R.sfx("click", S[1])
tlk = wt("f01", "look")
R.leave("#harsh", tlk - .12, .3)
R.rise("#tline", tlk, .7, 20, 6)
for k in range(3):
    R.ft(f"#tk{k}", tlk + .25 + k * .14, .5, "{opacity: 1, y: -24}", "{y: 0}", "expo.out")
    R.st(f"#tk{k}", 0, "{opacity: 0}")
    R.sfx("tick", tlk + .25 + k * .14)

# ---- f02: each flagged second: the phone cuts to it, a row appears
a2 = S[2]
R.to("#sc", a2 - .15, .7, "{x: 80, y: -170, scale: .66}", "expo.inOut")
NOTES = [("one", "demo_f01.jpg", "0:01", "Hook too slow"), ("seven", "demo_f07.jpg", "0:07", "A claim, no proof"), ("fourteen", "demo_f14.jpg", "0:14", "Loses trust")]
H('<div id="list" style="top:760px">' + "".join(
    f'<div class="row" id="r{k}"><b>{ts}</b><span>{txt}</span><i class="dot"></i><i class="ok">&#10003;</i></div>' for k, (_, _, ts, txt) in enumerate(NOTES)) + '</div>')
for k, (word, img, ts, txt) in enumerate(NOTES):
    tw = wt("f02", word)
    R.st("#frame", tw - .05, f'{{attr: {{src: "assets/img/{img}"}}}}')
    R.ft("#frame", tw - .05, .6, "{scale: 1.08}", "{scale: 1}", "expo.out")
    R.rise(f"#r{k}", tw - .05, .7, 30, 8)
    R.ft(f"#tk{k}", tw - .05, .5, "{scale: 1.35}", "{scale: 1}", "back.out(2.5)")
    R.st(f"#tk{k}", tw - .05, "{className: 'tk on'}")
    R.sfx("click", tw)

# ---- f03: fix those three seconds: the dots turn into green checks, the score climbs to 4.4
a3 = S[3]
tfx = wt("f03", "three")
for k in range(3):
    tk = tfx + k * .18
    R.st(f"#r{k}", tk, "{className: 'row fixed'}")
    R.ft(f"#r{k} .ok", tk, .45, "{opacity: 1, scale: 0}", "{scale: 1}", "back.out(3)")
    R.st(f"#tk{k}", tk, "{className: 'tk fixed'}")
    R.sfx("click", tk)
t44 = wt("f03", "4.4")
R.to("#sc", t44 - .45, .6, "{x: 80, y: -170, scale: .8}", "expo.inOut")
ring_to(t44 - .05, 2.9, 4.4, .9, GREEN)
R.sfx("g_correct", t44 + .1)

# ---- f04: Creedom (about 65 % in): the logo, then the app card
a4 = S[4]
for sel in ("#ph", "#sc", "#list", "#tline"):
    R.leave(sel, a4 - .2)
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div class="stage" style="top:500px"><div class="app soft" id="app"><img src="assets/img/creedom_logo.png" alt=""><div class="q">How can Cree help?</div>'
  '<div class="tile" id="t1"><i>&#10003;</i><div><b>Check a reel before you post</b><span>Score out of 5, the exact second, and the fix</span></div></div>'
  '<div class="tile dim"><i>&#9998;</i><div><b>Get a script in your voice</b></div></div></div></div>')
H('<img id="cree" src="assets/img/poses/proud.png" alt="">')
R.kicker("CREEDOM", a4 - .05, S[5] - .2, PINK)
R.st("#logo", 0, "{opacity: 0}")
R.ft("#logo", a4 - .02, 1.0, '{opacity: 1, scale: .9, filter: "blur(14px)"}', '{scale: 1, filter: "blur(0px)"}', "expo.out")
R.sfx("sparkle", a4)
tup = wt("f04", "upload")
R.leave("#logo", tup - .1, .35, -60)
R.rise("#app", tup, 1.0, 120, 12)
R.float3d("#app", tup, S[5], (8, 4), (-10, -4), (1, 0))
R.rise("#cree", tup + .4, .9, 60, 10)
tex = wt("f04", "exact")
R.ft("#t1", tex - .05, .5, "{scale: 1.04}", "{scale: 1}", "back.out(2)")
R.sfx("click", tex)
for sel in ("#app", "#cree"):
    R.leave(sel, S[5] - .18)

# ---- f05: CTA (CHECK), the comment field types it; cut back to frame 1 so it loops
a5 = S[5]
H(R.lines_html("h5", ["Send this to the friend", "<em>who posts and prays.</em>"], "hd").replace('id="h5"', 'id="h5" style="top:330px"'))
H('<div class="cbox soft" id="cbox" style="top:760px"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>')
H('<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.mask_lines("#h5", a5 - .02)
tc = wt("f05", "comment")
R.rise("#cbox", tc - .4, .8, 40, 8)
R.rise("#cree2", tc - .2, .9, 60, 10)
R.st("#cph", tc + .15, "{opacity: 0}")
R.typer("cty", tc + .15, "CHECK", .45)
R.sfx("typing", tc + .15)
R.ft("#cbox .send", tc + .75, .5, "{scale: 1.5}", "{scale: 1}", "back.out(3)")
R.sfx("notify", tc + .8)
H('<div id="loop"><div class="lp"><img src="assets/img/demo_f01.jpg" alt=""></div><div class="ln2"><b>2.9</b><span>out of 5</span></div></div>')
R.ft("#loop", R.DUR - .45, .4, "{opacity: 0}", "{opacity: 1}", "power2.inOut")

R.captions(top=1470)

R.write(f"""
.phone {{ position: relative; left: 100px; width: 400px; height: 711px; border-radius: 54px; overflow: hidden; background: #000; border: 10px solid {INK}; opacity: 0; }}
.phone img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.ex {{ position: absolute; left: 22px; top: 22px; background: rgba(16,19,28,.72); color: #fff; font-family: Mono; font-size: 22px; letter-spacing: .18em; padding: 6px 12px; border-radius: 8px; }}
#sc {{ position: absolute; left: 560px; top: 440px; width: 440px; height: 440px; opacity: 0; z-index: 20; transform-origin: 50% 50%; }}
#sc svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
#sc .trk {{ fill: none; stroke: rgba(16,19,28,.1); stroke-width: 2; }}
#sc .arc {{ fill: none; stroke: {RED}; stroke-width: 4; stroke-linecap: round; stroke-dasharray: 1; }}
#sc .n {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
#sc .n b {{ font-family: Unb; font-weight: 900; font-size: 150px; letter-spacing: -.06em; line-height: 1; }}
#sc .n span {{ font-family: Sat; font-weight: 500; font-size: 40px; color: {MUTE}; margin-top: 10px; }}
#tline {{ position: absolute; left: 100px; width: 400px; height: 70px; opacity: 0; z-index: 20; }}
#tline .bar {{ position: absolute; left: 0; right: 0; top: 30px; height: 3px; background: rgba(16,19,28,.14); border-radius: 2px; }}
.tk {{ position: absolute; top: 18px; width: 0; }}
.tk::before {{ content: ""; position: absolute; left: -9px; top: 3px; width: 18px; height: 18px; border-radius: 50%; background: #fff; border: 3px solid rgba(16,19,28,.3); }}
.tk em {{ position: absolute; left: -40px; top: 36px; width: 80px; text-align: center; font-style: normal; font-family: Mono; font-size: 24px; color: rgba(16,19,28,.78); }}
.tk.on::before {{ background: {RED}; border-color: {RED}; }}
.tk.fixed::before {{ background: {GREEN}; border-color: {GREEN}; }}
#list {{ position: absolute; left: 560px; right: 70px; z-index: 20; }}
.row {{ position: relative; display: flex; flex-direction: column; padding: 22px 60px 22px 0; border-top: 2px solid rgba(16,19,28,.1); opacity: 0; }}
.row:last-child {{ border-bottom: 2px solid rgba(16,19,28,.1); }}
.row b {{ font-family: Mono; font-size: 28px; color: {RED}; }}
.row span {{ font-family: Sat; font-weight: 900; font-size: 46px; letter-spacing: -.02em; line-height: 1.1; margin-top: 4px; }}
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
#cree2 {{ position: absolute; right: 90px; top: 960px; width: 260px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
.cbox {{ position: absolute; left: 90px; width: 820px; height: 140px; border-radius: 70px; background: #fff; display: flex; align-items: center; gap: 24px; padding: 0 34px;
  font-family: Sat; font-weight: 900; font-size: 64px; letter-spacing: .02em; z-index: 22; }}
.cbox .av {{ width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 142px; color: rgba(16,19,28,.35); font-weight: 500; font-size: 48px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: {PINK}; font-size: 54px; }}
#loop {{ position: absolute; inset: -60px; opacity: 0; z-index: 50; background: linear-gradient(180deg, #f7f8fc, #eceff7); }}
#loop .lp {{ position: absolute; left: 160px; top: 490px; width: 400px; height: 711px; border-radius: 54px; overflow: hidden; border: 10px solid {INK};
  transform: perspective(1900px) rotateY(26deg) rotateX(8deg) translateY(60px); }}
#loop .lp img {{ width: 100%; height: 100%; object-fit: cover; }}
#loop .ln2 {{ position: absolute; left: 620px; top: 500px; width: 440px; height: 440px; border-radius: 50%; border: 4px solid {RED}; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
#loop .ln2 b {{ font-family: Unb; font-weight: 900; font-size: 150px; letter-spacing: -.06em; line-height: 1; }}
#loop .ln2 span {{ font-family: Sat; font-weight: 500; font-size: 40px; color: {MUTE}; margin-top: 10px; }}
""")
