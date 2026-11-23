"""Creedom remake 2 v2, "Graded before anyone saw it" (Creators 100X, 9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

v2 (owner: "very dull and slow animated feel"): bright pink and fast, on the shared kinetic kit (build/kit.py, same as
creedom-postmortem-9x16). The scores are an example (owner: make them), shown with an EXAMPLE tag: 2.9 / 5 -> 4.4 / 5,
flags at 0:01, 0:07, 0:14. Frame 1: a reel on a phone and the dial slamming to 2.9; HARSH; each flagged second with a
giant timestamp; the fix and the climb to 4.4 with confetti; Creedom at about 60 %; CTA CHECK; loop back to the 2.9 dial.
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import INK, PINK, SUN, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creedom remake: graded before anyone saw it v2 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
RED, GREEN = "#ff2d55", "#14c27a"
for k in range(len(R.IDS)):
    R.drift(S[k] - .05, S[k + 1] - S[k] + .05, rot=1.6 if k % 2 else -1.6, z=.06)

C = 540.35                                     # dial circumference (r = 86)
def dial_to(t, frm, score, d=.6, col=RED):
    """the arc and the number move together; both are pure functions of the timeline position"""
    R.js(f'tl.to("#arc", {{strokeDashoffset: {C * (1 - score / 5):.1f}, stroke: "{col}", duration: {d}, ease: "power3.out"}}, {t:.3f});')
    R.counter("score", t, d, frm, score, "o.v.toFixed(1)", "power3.out")

# ---- f00: phone + dial at frame 1, the dial slams to 2.9
H('<div id="phone"><img id="frame" src="assets/img/demo_f01.jpg" alt=""><b class="ex">EXAMPLE</b></div>')
H('<div id="dial"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="trk"/><circle cx="100" cy="100" r="86" class="arc" id="arc"/></svg>'
  '<div class="sc"><b id="score">0.0</b><span>/ 5</span></div></div>')
R.st("#phone", 0, "{opacity: 1}")
R.st("#dial", 0, "{opacity: 1}")
R.ft("#phone", 0, .4, "{scale: 1.25, rotation: -10, x: -80}", "{scale: 1, rotation: -4, x: 0}", "expo.out")
R.ft("#dial", 0, .4, "{scale: .3, rotation: 30}", "{scale: 1, rotation: 0}", "back.out(1.8)")
R.js(f'tl.set("#arc", {{strokeDashoffset: {C:.1f}}}, 0);')
dial_to(.1, 0, 2.9, .5)
R.sfx("riser_short", 0)
R.sfx("buzzer", .58)
R.sfx("impact", .6)
R.shake(.62, 20, 1.6)
R.punch(.6, .1)
R.burst(.6, 760, 880, 1.0, RED)
tb = wt("f00", "before")
R.slam("before anyone<br><em>saw it.</em>", tb, max(.35, S[1] - tb - .45), top=250, size=120, rot=-3, sfx="thump")

# ---- f01: HARSH, then the timeline with three flags
a1 = S[1]
H('<div id="tline"><i class="bar"></i>' + "".join(f'<i class="flag" id="fl{k}" style="left:{x}%"><em>{lab}</em></i>' for k, (x, lab) in enumerate([(6, "0:01"), (40, "0:07"), (78, "0:14")])) + '</div>')
R.slam("HARSH.", a1, max(.3, wt("f01", "look") - a1 - .35), top=720, size=280, rot=-5, col=SUN, sfx="impact")
R.burst(a1, 540, 860, 1.3, SUN)
R.sfx("g_wrong", a1 + .05)
tl_ = wt("f01", "look")
R.to("#phone, #dial", a1 - .04, .2, "{opacity: .25, scale: .9}", "power2.out")      # HARSH sits on top: the scene steps back
R.to("#phone, #dial", tl_ - .1, .25, "{opacity: 1, scale: 1}", "back.out(2)")
R.pop_in("#tline", tl_ - .05, .3, .6, 0, "back.out(2)")
R.sfx("whoosh", tl_ - .1)
for k in range(3):
    R.ft(f"#fl{k}", tl_ + .2 + k * .14, .28, "{opacity: 0, y: -60, scale: .3}", "{opacity: 1, y: 0, scale: 1}", "back.out(3.5)")
    R.sfx("pop", tl_ + .2 + k * .14)
R.punch(wt("f01", "points"), .06)

# ---- f02: each flagged second: phone frame cuts, giant timestamp, a note card
a2 = S[2]
NOTES = [("one", "demo_f01.jpg", "0:01", "Hook too slow"), ("seven", "demo_f07.jpg", "0:07", "A claim, no proof"), ("fourteen", "demo_f14.jpg", "0:14", "Loses trust")]
H('<div id="notes">' + "".join(f'<div class="note" id="n{k}"><b>{ts}</b><span>{txt}</span><i class="ok">&#10003;</i></div>' for k, (_, _, ts, txt) in enumerate(NOTES)) + '</div>')
R.to("#dial", a2 - .12, .3, "{x: 150, y: -380, scale: .44}", "power3.inOut")
R.to("#phone", a2 - .12, .3, "{x: -20, y: -60, rotation: -3}", "power3.inOut")
R.sfx("swish", a2 - .12)
for k, (word, img, ts, txt) in enumerate(NOTES):
    tw = wt("f02", word)
    R.st("#frame", tw - .05, f'{{attr: {{src: "assets/img/{img}"}}}}')
    R.ft("#phone", tw - .05, .3, "{scale: 1.12}", "{scale: 1}", "expo.out")
    R.flash(tw - .05, .35, .12)
    R.slam(ts, tw - .02, .3, top=250, size=170, rot=-4 + 4 * k, col=SUN, sfx="g_wrong" if k < 2 else "thump", shake=False)
    R.ft(f"#n{k}", tw + .08, .3, "{opacity: 0, x: 400, rotation: 8}", "{opacity: 1, x: 0, rotation: 0}", "back.out(2)")
    R.ft(f"#fl{k}", tw, .3, "{scale: 1.8}", "{scale: 1}", "back.out(3)")
    R.sfx("swish", tw + .08)
    twd = R.LW["f02"][[w["t0"] for w in R.LW["f02"]].index(tw) + 2]["t0"] if k < 2 else wt("f02", "trust")
    R.punch(twd, .05)

# ---- f03: fix the three seconds: checks pop green, the dial flies back big and climbs to 4.4
a3 = S[3]
tfix = wt("f03", "three")
for k in range(3):
    tk = tfix + k * .16
    R.st(f"#n{k}", tk, "{className: 'note fixed'}")
    R.ft(f"#n{k} .ok", tk, .3, "{scale: 0, rotation: -90}", "{scale: 1, rotation: 0}", "back.out(3.5)")
    R.ft(f"#n{k}", tk, .25, "{scale: 1.12}", "{scale: 1}", "back.out(3)")
    R.st(f"#fl{k}", tk, "{className: 'flag fixed'}")
    R.sfx("g_correct" if k == 2 else "click", tk)
t44 = wt("f03", "scores") + .35          # "four point four" (Whisper writes "4 .4.")
R.to("#notes", t44 - .5, .22, '{x: 700, opacity: 0, filter: "blur(16px)"}', "power3.in")
R.to("#phone", t44 - .5, .22, '{x: -700, opacity: 0, filter: "blur(16px)"}', "power3.in")
R.to("#tline", t44 - .5, .18, "{opacity: 0, y: 80}", "power2.in")
R.to("#dial", t44 - .42, .35, "{x: -230, y: -60, scale: 1.3}", "back.out(1.6)")
R.sfx("whoosh", t44 - .5)
dial_to(t44 - .05, 2.9, 4.4, .6, GREEN)
R.flash(t44 + .5, .6, .2)
R.burst(t44 + .5, 540, 880, 1.5, SUN)
R.confetti(t44 + .5, 40, 5, 540, 860)
R.shake(t44 + .52, 14, 1.2)
R.punch(t44 + .5, .1)
R.sfx("g_levelup", t44 + .45)
R.sfx("sparkle", t44 + .55)

# ---- f04: Creedom (about 60 % in): flash, logo slam, the app card, Cree
a4 = S[4]
H('<div id="logo"><img src="assets/img/creedom_logo.png" alt=""></div>')
H('<div id="app"><img src="assets/img/creedom_logo.png" alt=""><div class="q">How can Cree help?</div>'
  '<div class="tile" id="t1"><i>&#9654;</i><div><b>Check a reel before you post</b><span>Score out of 5, the exact second, and the fix</span></div></div>'
  '<div class="tile dim"><i>&#9998;</i><div><b>Get a script in your voice</b></div></div></div>')
H('<img id="cree" src="assets/img/poses/proud.png" alt="">')
R.zoom_out("#dial", a4 - .14)
R.flash(a4 - .06, .95, .25)
R.ft("#logo", a4 - .04, .3, "{opacity: 0, scale: 3, rotation: -12}", "{opacity: 1, scale: 1, rotation: -3}", "power4.out")
R.burst(a4, 540, 800, 1.3)
R.shake(a4 + .05, 16, 1.4)
R.punch(a4 + .02, .1)
R.sfx("whoosh_big", a4 - .2)
R.sfx("impact", a4 - .02)
tup = wt("f04", "upload")
R.to("#logo", tup - .12, .18, "{y: -900, scale: .5, opacity: 0}", "power3.in")
R.ft("#app", tup - .04, .36, '{opacity: 1, y: 1200, rotation: 6, filter: "blur(20px)"}', '{y: 0, rotation: -1.5, filter: "blur(0px)"}', "expo.out")
R.sfx("whoosh", tup - .12)
R.ft("#cree", tup + .15, .4, "{opacity: 0, x: 300, rotation: 20}", "{opacity: 1, x: 0, rotation: 0}", "back.out(2)")
R.sfx("g_pop", tup + .15)
tex = wt("f04", "exact")
R.ft("#t1", tex - .05, .3, "{scale: 1.1}", "{scale: 1}", "back.out(3)")
R.punch(tex, .06)
R.sfx("pop", tex - .05)
tfx = wt("f04", "fix")
R.ft("#t1", tfx - .05, .3, "{scale: 1.1}", "{scale: 1}", "back.out(3)")
R.punch(tfx, .05)
R.sfx("ding", tfx)

# ---- f05: CTA (CHECK): share sticker, giant comment box, Cree waves; flash cut back to the 2.9 dial (loop)
a5 = S[5]
H('<div id="share"><b>&#10148;</b><span>send this to the friend<br>who posts and prays</span></div>'
  '<div id="cbox"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>'
  '<img id="cree2" src="assets/img/poses/wave.png" alt="">')
R.whip_out("#app", a5 - .14, -1)
R.to("#cree", a5 - .14, .15, "{opacity: 0, x: 300}", "power2.in")
R.pop_in("#share", a5 - .02, .32, .4, -3)
R.burst(a5, 540, 640, 1.0)
R.sfx("whoosh", a5 - .14)
R.sfx("pop", a5)
tpr = wt("f05", "prays")
R.ft("#share", tpr, .3, "{scale: 1.12}", "{scale: 1}", "back.out(3)")
R.punch(tpr, .05)
tc = wt("f05", "comment")
R.pop_in("#cbox", tc - .08, .32, .5, 0, "back.out(2.2)")
R.ft("#cree2", tc - .02, .4, "{opacity: 0, x: 300, rotation: 20}", "{opacity: 1, x: 0, rotation: 0}", "back.out(2)")
R.st("#cph", tc + .12, "{opacity: 0}")
R.typer("cty", tc + .12, "CHECK", .45)
R.sfx("typing", tc + .12)
R.ft("#cbox", tc + .65, .3, "{scale: 1.12}", "{scale: 1}", "back.out(3)")
R.sfx("click", tc + .65)
R.sfx("notify", tc + .85)
R.punch(tc + .65, .06)
H('<div id="loop" data-layout-allow-overlap><div class="lp"><img src="assets/img/demo_f01.jpg" alt=""></div><div class="ld"><b>2.9</b><span>/ 5</span></div></div>')
R.flash(R.DUR - .36, .9, .2)
R.st("#loop", R.DUR - .3, "{opacity: 1}")

R.captions(top=1440, max_words=3)

SHADOW = f"0 18px 0 {INK}, 0 40px 80px rgba(70,0,35,.4)"
R.write(f"""
#phone {{ position: absolute; left: 60px; top: 500px; width: 450px; height: 800px; border-radius: 50px; overflow: hidden; background: #000; opacity: 0;
  border: 12px solid {INK}; box-shadow: 0 22px 0 rgba(22,18,26,.45), 0 50px 100px rgba(70,0,35,.45); z-index: 12; }}
#phone img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ex {{ position: absolute; left: 18px; top: 18px; background: rgba(22,18,26,.8); color: #fff; font-family: Mono; font-weight: 700; font-size: 24px; letter-spacing: .14em;
  padding: 6px 14px; border-radius: 10px; }}
#dial {{ position: absolute; left: 540px; top: 640px; width: 490px; height: 490px; opacity: 0; z-index: 14; }}
#dial svg {{ width: 100%; height: 100%; transform: rotate(-90deg); filter: drop-shadow(0 16px 0 {INK}); }}
#dial .trk {{ fill: #fff; stroke: rgba(22,18,26,.1); stroke-width: 16; }}
#dial .arc {{ fill: none; stroke: {RED}; stroke-width: 16; stroke-linecap: round; stroke-dasharray: {C}; }}
#dial .sc {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 165px; gap: 8px; }}
#dial .sc b {{ font-weight: 800; font-size: 170px; letter-spacing: -.05em; line-height: 1; }}
#dial .sc span {{ font-weight: 800; font-size: 54px; color: #8a8290; }}
#tline {{ position: absolute; left: 70px; right: 70px; top: 1340px; height: 60px; opacity: 0; z-index: 16; }}
#tline .bar {{ position: absolute; left: 0; right: 0; top: 24px; height: 14px; border-radius: 7px; background: #fff; box-shadow: 0 6px 0 {INK}; }}
.flag {{ position: absolute; top: -34px; width: 0; opacity: 0; }}
.flag em {{ position: absolute; left: -62px; width: 124px; text-align: center; font-style: normal; font-family: Mono; font-weight: 700; font-size: 32px; color: #fff;
  background: {RED}; padding: 6px 0; border-radius: 12px; box-shadow: 0 6px 0 {INK}; }}
.flag.fixed em {{ background: {GREEN}; }}
#notes {{ position: absolute; left: 525px; top: 560px; width: 470px; z-index: 18; display: flex; flex-direction: column; gap: 26px; }}
.note {{ position: relative; opacity: 0; background: #fff; border-radius: 28px; padding: 20px 26px; box-shadow: 0 12px 0 {INK}; border-left: 16px solid {RED}; }}
.note b {{ display: block; font-family: Mono; font-weight: 700; font-size: 34px; color: {RED}; }}
.note span {{ display: block; font-weight: 800; font-size: 46px; letter-spacing: -.02em; line-height: 1.05; }}
.note .ok {{ position: absolute; right: 18px; top: 50%; margin-top: -34px; width: 68px; height: 68px; border-radius: 50%; background: {GREEN}; color: #fff; display: grid;
  place-items: center; font-style: normal; font-weight: 800; font-size: 40px; transform: scale(0); }}
.note.fixed {{ border-left-color: {GREEN}; }} .note.fixed b {{ color: {GREEN}; }}
#logo {{ position: absolute; left: 90px; right: 90px; top: 640px; height: 300px; border-radius: 50px; background: #fff; opacity: 0; z-index: 30; display: grid; place-items: center;
  box-shadow: {SHADOW}; }}
#logo img {{ width: 78%; }}
#app {{ position: absolute; left: 60px; right: 60px; top: 480px; opacity: 0; z-index: 20; border-radius: 44px; padding: 36px 38px 40px; background: #fff; box-shadow: {SHADOW}; }}
#app img {{ height: 74px; display: block; }}
.q {{ margin: 26px 0 22px; font-family: Serif; font-style: italic; font-size: 72px; }}
.tile {{ display: flex; gap: 22px; align-items: center; background: {SUN}; border-radius: 28px; padding: 24px 26px; margin-top: 16px; box-shadow: 0 10px 0 {INK}; }}
.tile i {{ width: 82px; height: 82px; border-radius: 22px; background: {INK}; color: #fff; display: grid; place-items: center; font-style: normal; font-size: 38px; flex: none; }}
.tile b {{ display: block; font-weight: 800; font-size: 44px; letter-spacing: -.02em; line-height: 1.05; }}
.tile span {{ display: block; font-weight: 600; font-size: 30px; color: #4b4450; margin-top: 4px; }}
.tile.dim {{ background: #f3eef2; box-shadow: none; opacity: .6; }}
.tile.dim i {{ background: #cfc6cc; color: {INK}; }}
#cree, #cree2 {{ position: absolute; right: 20px; top: 1060px; width: 330px; opacity: 0; z-index: 24; filter: drop-shadow(0 16px 0 rgba(22,18,26,.25)); }}
#cree2 {{ top: 1000px; }}
#share {{ position: absolute; left: 70px; right: 70px; top: 470px; opacity: 0; z-index: 24; display: flex; align-items: center; gap: 26px; background: {INK}; color: #fff;
  padding: 30px 40px; border-radius: 40px; font-weight: 800; font-size: 54px; line-height: 1.1; box-shadow: 0 14px 0 rgba(22,18,26,.35); }}
#share b {{ color: {SUN}; font-size: 80px; }}
#cbox {{ position: absolute; left: 60px; width: 760px; top: 860px; height: 150px; border-radius: 75px; background: #fff; display: flex; align-items: center; opacity: 0; z-index: 24;
  gap: 24px; padding: 0 34px; font-weight: 800; font-size: 72px; letter-spacing: .02em; box-shadow: {SHADOW}; }}
#cbox .av {{ width: 90px; height: 90px; border-radius: 50%; background: linear-gradient(135deg, {PINK}, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 150px; color: rgba(22,18,26,.35); font-weight: 600; font-size: 52px; }}
#cbox .send {{ margin-left: auto; color: {PINK}; }}
#loop {{ position: absolute; inset: 0; opacity: 0; z-index: 46; background: {PINK}; }}
#loop .lp {{ position: absolute; left: 60px; top: 500px; width: 450px; height: 800px; border-radius: 50px; overflow: hidden; border: 12px solid {INK}; transform: rotate(-10deg) scale(1.25); }}
#loop .lp img {{ width: 100%; height: 100%; object-fit: cover; }}
#loop .ld {{ position: absolute; left: 540px; top: 640px; width: 490px; height: 490px; border-radius: 50%; background: #fff; display: flex; align-items: baseline;
  justify-content: center; padding-top: 165px; gap: 8px; border: 16px solid {RED}; }}
#loop .ld b {{ font-weight: 800; font-size: 170px; letter-spacing: -.05em; line-height: 1; }} #loop .ld span {{ font-weight: 800; font-size: 54px; color: #8a8290; }}
""")
