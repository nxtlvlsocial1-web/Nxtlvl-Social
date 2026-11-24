"""Creedom remake 2 v6, "Graded before anyone saw it" (Creators 100X, 9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

v6 (owner, on v5: fix the first-frame pile-up; no background music; "viewers should get what Creedom does as soon as
possible, even if they don't watch the whole video"): tool first. Line 1 says what Creedom does while a reel and its
score are on frame 1; the Creedom logo bar with the comment keyword stays at the top the whole reel; the three flags and
the fix are the proof; the name and CTA close it (about 16.5 s). Elements that appear later are hidden in CSS from
frame 0 (build/kit_min.py). The scores are an example (EXAMPLE tag): 2.9 / 5 -> 4.4 / 5, flags at 0:01, 0:07, 0:14.
Voice: Kokoro af_heart (build/vo_kok.py). Look: Glacier, Unbounded + Satoshi.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_min import GREEN, INK, MUTE, PINK, RED, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: graded before anyone saw it v6 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.push(S[k] - .1, S[k + 1], .035)
    if k:
        R.sfx("swish", S[k] - .16)
R.sfx("thump", .02)
R.topbar("CHECK", S[1] - .1)
R.sfx("pop", S[1] - .1)


def ring_to(t, frm, score, d=.7, col=RED):
    R.js(f'tl.to("#arc", {{strokeDashoffset: {1 - score / 5:.4f}, stroke: "{col}", duration: {d}, ease: "power3.out"}}, {t:.3f});')
    R.counter("score", t, d, frm, score, "o.v.toFixed(1)", "power3.out")


# ---- f00: what Creedom does, said in line 1, with a reel and its score ring on frame 1 (visible in CSS from frame 0)
H('<div class="hd" id="hk" style="top:330px;font-size:88px"><span class="ln"><span>This tool scores</span></span><span class="ln"><span>your reel before</span></span>'
  f'<span class="ln"><span style="color:{RED}">you post it.</span></span></div>')
H('<div class="stage" style="top:640px"><div class="phone soft" id="ph"><img id="frame" src="assets/img/demo_f01.jpg" alt=""><b class="ex">EXAMPLE</b></div></div>')
H('<div id="sc"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" class="trk"/><circle cx="100" cy="100" r="96" class="arc" id="arc" pathLength="1"/></svg>'
  '<div class="n"><b id="score">?</b><span>out of 5</span></div></div>')
R.js('tl.fromTo("#hk .ln > span", {y: 10}, {y: 0, duration: .45, ease: "expo.out", stagger: .06, immediateRender: true}, 0);')
R.ft("#ph", 0, 1.0, "{y: 50, rotationY: 26, rotationX: 8}", "{y: 0, rotationY: 16, rotationX: 4}")
R.float3d("#ph", 1.0, S[3], (4, 2), (16, 10), (-1, 0))
tsc = wt("f00", "scores")
ring_to(tsc, 0, 2.9, 1.1)                                        # the tool scores it while the line says so
R.sfx("tick", tsc + 1.0)
R.to("#sc", wt("f00", "post") - .1, .5, "{scale: 1.1}", "expo.out")
R.leave("#hk", S[1] - .25, .3)

# ---- f01: "this one got 2.9 out of 5": the score pulses, "before posting" takes the hook's place
H(R.lines_html("hb", ["Scored before", f'<span style="color:{RED}">anyone saw it.</span>'], "hd").replace('id="hb"', 'id="hb" style="top:330px;font-size:88px"'))
R.mask_lines("#hb", S[1] - .05)
t29 = wt("f01", "2.9")
R.ft("#sc", t29 - .05, .5, "{scale: 1.24}", "{scale: 1.1}", "back.out(2.5)")
R.sfx("thump", t29)
R.leave("#hb", S[2] - .22, .3)

# ---- f02: each flagged second: the phone cuts to it, a row and a tick on the timeline land
a2 = S[2]
R.to("#sc", a2 - .2, .6, "{x: 80, y: -170, scale: .62}", "expo.inOut")
H('<div id="tline" style="top:1350px"><i class="bar"></i>' + "".join(
    f'<i class="tk" id="tk{k}" style="left:{x}%"><em>{lab}</em></i>' for k, (x, lab) in enumerate([(6, "0:01"), (40, "0:07"), (78, "0:14")])) + '</div>')
NOTES = [("one", "demo_f01.jpg", "0:01", "Slow hook"), ("seven", "demo_f07.jpg", "0:07", "No proof"), ("fourteen", "demo_f14.jpg", "0:14", "Lost trust")]
H('<div id="list" style="top:860px">' + "".join(
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

# ---- f03: fix those three: the dots turn into green checks, the score climbs to 4.4
tfx = wt("f03", "three")
for k in range(3):
    tk = tfx - .1 + k * .14
    R.st(f"#r{k}", tk, "{className: 'row fixed'}")
    R.ft(f"#r{k} .ok", tk, .4, "{opacity: 1, scale: 0}", "{scale: 1}", "back.out(3)")
    R.st(f"#tk{k}", tk, "{className: 'tk fixed'}")
    R.sfx("click", tk)
t44 = wt("f03", "4.4")
R.to("#sc", wt("f03", "scores") - .3, .5, "{x: 80, y: -170, scale: .8}", "expo.inOut")
ring_to(t44 - .1, 2.9, 4.4, .8, GREEN)
R.sfx("thump", t44)
R.sfx("g_correct", t44 + .15)

# ---- f04: the name, the comment field types CHECK, the share line; cut back to frame 1 so it loops
a4 = S[4]
for sel in ("#ph", "#sc", "#list", "#tline"):
    R.leave(sel, a4 - .22, .3)
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div class="cbox soft" id="cbox" style="top:800px"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>')
H('<div class="sub" id="share" style="top:1000px">Send this to the friend<br>who posts and prays.</div>')
H('<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.ft("#logo", a4 - .05, .8, '{opacity: 1, scale: .9, filter: "blur(14px)"}', '{scale: 1, filter: "blur(0px)"}', "expo.out")
R.st("#logo", 0, "{opacity: 0}")
R.sfx("sparkle", wt("f04", "creedom"))
tcm = wt("f04", "comment")
R.to("#logo", tcm - .3, .5, "{y: -230, scale: .7}", "expo.inOut")
R.rise("#cbox", tcm - .2, .6, 40, 8)
R.rise("#cree2", tcm, .7, 60, 10)
tck = wt("f04", "check")
R.st("#cph", tck - .1, "{opacity: 0}")
R.typer("cty", tck - .1, "CHECK", .4)
R.sfx("typing", tck - .1)
R.ft("#cbox .send", tck + .5, .5, "{scale: 1.5}", "{scale: 1}", "back.out(3)")
R.sfx("notify", tck + .55)
R.rise("#share", tck + .3, .6, 20, 6)
H('<div id="loop"><div class="hd" style="top:330px;font-size:88px">This tool scores<br>your reel before<br><span style="color:' + RED + '">you post it.</span></div>'
  '<div class="lp"><img src="assets/img/demo_f01.jpg" alt=""></div></div>')
R.ft("#loop", R.DUR - .4, .35, "{opacity: 0}", "{opacity: 1}", "power2.inOut")

R.captions(top=1470)

R.write(f"""
.sub {{ position: absolute; left: 90px; right: 90px; font-family: Sat; font-weight: 500; font-size: 48px; line-height: 1.15; letter-spacing: -.02em; color: {MUTE}; z-index: 20; }}
.phone {{ position: relative; left: 100px; width: 380px; height: 676px; border-radius: 52px; overflow: hidden; background: #000; border: 10px solid {INK}; }}
.phone img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.ex {{ position: absolute; left: 22px; top: 22px; background: rgba(16,19,28,.72); color: #fff; font-family: Mono; font-size: 22px; letter-spacing: .18em; padding: 6px 12px; border-radius: 8px; }}
#sc {{ position: absolute; left: 560px; top: 700px; width: 420px; height: 420px; z-index: 20; transform-origin: 50% 50%; }}
#sc svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
#sc .trk {{ fill: none; stroke: rgba(16,19,28,.1); stroke-width: 2; }}
#sc .arc {{ fill: none; stroke: {RED}; stroke-width: 4; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: 1; }}
#sc .n {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
#sc .n b {{ font-family: Unb; font-weight: 900; font-size: 140px; letter-spacing: -.06em; line-height: 1; }}
#sc .n span {{ font-family: Sat; font-weight: 500; font-size: 40px; color: {MUTE}; margin-top: 10px; }}
#tline {{ position: absolute; left: 100px; width: 380px; height: 70px; z-index: 20; }}
#tline .bar {{ position: absolute; left: 0; right: 0; top: 30px; height: 3px; background: rgba(16,19,28,.14); border-radius: 2px; }}
.tk {{ position: absolute; top: 18px; width: 0; }}
.tk::before {{ content: ""; position: absolute; left: -9px; top: 3px; width: 18px; height: 18px; border-radius: 50%; background: #fff; border: 3px solid rgba(16,19,28,.3); }}
.tk em {{ position: absolute; left: -40px; top: 36px; width: 80px; text-align: center; font-style: normal; font-family: Mono; font-size: 24px; color: rgba(16,19,28,.78); }}
.tk.on::before {{ background: {RED}; border-color: {RED}; }}
.tk.fixed::before {{ background: {GREEN}; border-color: {GREEN}; }}
#list {{ position: absolute; left: 560px; right: 70px; z-index: 20; }}
.row {{ position: relative; display: flex; flex-direction: column; padding: 24px 60px 24px 0; border-top: 2px solid rgba(16,19,28,.1); }}
.row:last-child {{ border-bottom: 2px solid rgba(16,19,28,.1); }}
.row b {{ font-family: Mono; font-size: 30px; color: {RED}; }}
.row span {{ font-family: Sat; font-weight: 900; font-size: 56px; letter-spacing: -.02em; line-height: 1.05; margin-top: 4px; }}
.row .dot {{ position: absolute; right: 8px; top: 50%; margin-top: -8px; width: 16px; height: 16px; border-radius: 50%; background: {RED}; }}
.row .ok {{ position: absolute; right: 0; top: 50%; margin-top: -22px; width: 44px; height: 44px; border-radius: 50%; background: {GREEN}; color: #fff; display: grid; place-items: center;
  font-style: normal; font-weight: 900; font-size: 26px; opacity: 0; }}
.row.fixed b {{ color: {GREEN}; }} .row.fixed .dot {{ opacity: 0; }}
#logo {{ position: absolute; left: 140px; right: 140px; top: 560px; height: 280px; display: grid; place-items: center; z-index: 25; }}
#logo img {{ width: 100%; }}
#cree2 {{ position: absolute; right: 90px; top: 1060px; width: 250px; z-index: 26; filter: drop-shadow(0 20px 30px rgba(40,50,90,.2)); }}
.cbox {{ position: absolute; left: 90px; width: 820px; height: 140px; border-radius: 70px; background: #fff; display: flex; align-items: center; gap: 24px; padding: 0 34px;
  font-family: Sat; font-weight: 900; font-size: 64px; letter-spacing: .02em; z-index: 22; }}
.cbox .av {{ width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 142px; color: rgba(16,19,28,.35); font-weight: 500; font-size: 48px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: {PINK}; font-size: 54px; }}
#loop {{ position: absolute; inset: -60px; opacity: 0; z-index: 50; background: linear-gradient(180deg, #f7f8fc, #eceff7); }}
#loop .hd {{ transform: translate(60px, 60px); }}
#loop .lp {{ position: absolute; left: 160px; top: 700px; width: 380px; height: 676px; border-radius: 52px; overflow: hidden; border: 10px solid {INK};
  transform: perspective(1900px) rotateY(26deg) rotateX(8deg) translateY(50px); }}
#loop .lp img {{ width: 100%; height: 100%; object-fit: cover; }}
""")
