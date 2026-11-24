"""AI.NXTLVL: "Your phone can run its own AI, with no internet" (Off Grid AI), 9:16. Writes index.html, plan/sfx_events.json,
plan/edit.json.

Recreates the owner's reference (a creator's talking-head reel about an offline AI phone app) with a better script and
elements, for AI.NXTLVL (brands/ai-nxtlvl/brand.md). The reference names the app "Private LM"; the app it shows is
Off Grid AI (github.com/off-grid-ai/OGAM, MIT, by Wednesday Solutions; facts from its README, plan/facts.md). The
reference's face and footage are not reused: the app footage is the project's own demo clips (MIT, assets/video/og_*).
Hook with proof on frame 1 (airplane mode on, the app answering); the name in line 2 (owner: get the tool fast); a
feature per line, each with a real clip and an element that pops out of the phone; privacy as the share trigger; CTA
OFFLINE. Voice: Kokoro am_michael (build/vo_kok.py). Look: AI.NXTLVL night + violet (build/kit_ai.py).
python3 build/generate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_ai import GREEN, INK, MUTE, PINK, STAR, Reel  # noqa: E402

R = Reel(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "AI.NXTLVL: Off Grid AI, offline AI on your phone 9x16")
S, wt, H = R.S, R.wt, R.HTML.append
for k in range(len(R.IDS)):
    R.push(S[k] - .1, S[k + 1], .035)
    if k:
        R.sfx("swish", S[k] - .16)
R.sfx("thump", .02)
R.topbar("OFFLINE", S[1] - .1, "assets/img/logo-wordmark.png")
R.sfx("pop", S[1] - .1)

# one phone for the whole reel; each scene puts a clip on its screen (real app footage from the project's demos)
CLIPS = [("og_text", 0, S[1] + .1), ("og_onboard", S[2] - .15, S[3]), ("og_text", S[3] - .1, S[4]), ("og_image", S[4] - .15, S[5]),
         ("og_vision", S[5] - .15, wt("f05", "documents") - .1), ("og_docs", wt("f05", "documents") - .1, S[6])]
vids = []
for k, (name, a, z) in enumerate(CLIPS):
    vids.append(f'<video class="cl" id="cl{k}" src="assets/video/{name}.mp4" data-start="{max(0, a):.3f}" data-duration="{z - max(0, a):.3f}" '
                f'data-track-index="{k + 1}" muted playsinline></video>')
H('<div class="stage" id="stg"><div class="phone" id="ph"><div class="isl"></div><div class="scr"><img id="poster" src="assets/img/og_text_first.jpg" alt="">'
  + "".join(vids) + '<img id="imgend" src="assets/img/og_image_last.jpg" alt=""></div></div></div>')
# phone poses change on each line (3D swing), and it leaves for the privacy and CTA scenes
POSES = [(-12, 6, -2), (14, 5, 2), (-14, 7, -2), (12, 5, 1), (-8, 6, -1), (10, 5, 1)]
R.ft("#ph", 0, 1.0, "{rotationY: -26, rotationX: 14, rotation: -5, y: 60}", f"{{rotationY: {POSES[0][0]}, rotationX: {POSES[0][1]}, rotation: {POSES[0][2]}, y: 0}}")
for k in range(1, 6):
    ry, rx, rz = POSES[k]
    R.to("#ph", S[k] - .25, .6, f"{{rotationY: {ry}, rotationX: {rx}, rotation: {rz}}}", "expo.inOut")
# the app's chat screen stays under the clips, so the phone never shows a blank screen between them

# ---- f00: hook + proof on frame 1: the phone in airplane mode, the app answering
H('<div class="hd" id="hk" style="top:300px;font-size:84px"><span class="ln"><span>Your phone can run</span></span><span class="ln"><span>its own AI.</span></span>'
  '<span class="ln"><span><em>No internet.</em></span></span></div>')
H('<div class="chip" id="air" style="left:600px;top:700px"><svg viewBox="0 0 24 24"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="currentColor"/></svg>Airplane mode</div>')
H('<div class="chip off" id="wifi" style="left:600px;top:800px"><svg viewBox="0 0 24 24"><path d="M2 8.8a15 15 0 0 1 20 0M5.5 12.3a10 10 0 0 1 13 0M9 15.8a5 5 0 0 1 6 0M12 19.5h.01" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M3 3l18 18" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>No Wi-Fi, no data</div>')
R.js('tl.fromTo("#hk .ln > span", {y: 10}, {y: 0, duration: .45, ease: "expo.out", stagger: .06, immediateRender: true}, 0);')
R.ft("#air", .25, .55, "{opacity: 1, x: 60, scale: .8}", "{x: 0, scale: 1}", "back.out(2)")
R.st("#air", 0, "{opacity: 0}")
R.sfx("click", .3)
tno = wt("f00", "no")
R.ft("#wifi", tno - .1, .55, "{opacity: 1, x: 60, scale: .8}", "{x: 0, scale: 1}", "back.out(2)")
R.st("#wifi", 0, "{opacity: 0}")
R.sfx("g_pop", tno)
R.leave("#hk", S[1] - .25, .3)
R.leave("#air", S[1] - .25, .3)
R.leave("#wifi", S[1] - .25, .3)

# ---- f01: the name: Off Grid, free and open source on GitHub (a repo card from the README facts)
H(R.lines_html("h1", ["It's called", "<em>Off Grid.</em>"], "hd").replace('id="h1"', 'id="h1" style="top:300px;font-size:96px"'))
H('<div class="repo soft" id="repo"><div class="rh"><svg viewBox="0 0 16 16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
  'github.com/<b>off-grid-ai/OGAM</b></div><div class="rb"><img src="assets/img/offgrid_logo.png" alt=""><div><b>Off Grid AI</b>'
  '<span>The Swiss Army Knife of On-Device AI</span></div></div><div class="rt"><i class="g">Free</i><i>Open source &middot; MIT</i><i>Android &middot; iOS &middot; Mac</i></div></div>')
R.mask_lines("#h1", S[1] - .05)
R.rise("#repo", wt("f01", "free") - .2, .7, 60, 10)
R.to("#stg", S[1] - .2, .6, "{x: 260, scale: .8, opacity: .35}", "expo.inOut")     # the phone steps back for the card
for k, w in enumerate(("free", "open", "github")):
    R.ft(f".rt i:nth-child({k + 1})", wt("f01", w) - .05, .4, "{opacity: 1, scale: .6}", "{scale: 1}", "back.out(3)")
    R.st(f".rt i:nth-child({k + 1})", 0, "{opacity: 0}")
    R.sfx("pop", wt("f01", w))
R.leave("#h1", S[2] - .22, .3)
R.leave("#repo", S[2] - .22, .3)
R.to("#stg", S[2] - .25, .6, "{x: 0, scale: 1, opacity: 1}", "expo.inOut")

# ---- f02: install it, it sets itself up for your phone (onboarding clip + the checks it runs, from the README)
H(R.lines_html("h2", ["Install it.", "<em>It sets itself up.</em>"], "hd").replace('id="h2"', 'id="h2" style="top:300px"'))
CHECKS = ["Checks your chip", "Picks the fastest backend", "Fits models to your RAM"]
H('<div id="checks">' + "".join(f'<div class="ck" id="ck{k}"><i>&#10003;</i>{c}</div>' for k, c in enumerate(CHECKS)) + '</div>')
R.mask_lines("#h2", S[2] - .05)
for k, w in enumerate(("sets", "up", "phone")):
    tk = wt("f02", w) - .05
    R.ft(f"#ck{k}", tk, .45, "{opacity: 1, x: 80}", "{x: 0}", "back.out(2)")
    R.st(f"#ck{k}", 0, "{opacity: 0}")
    R.sfx("g_tick", tk)
R.leave("#h2", S[3] - .22, .3)
for k in range(3):
    R.leave(f"#ck{k}", S[3] - .22, .3)

# ---- f03: chat with models like Qwen, Llama or Gemma, offline (text clip + model chips break out of the phone)
H(R.lines_html("h3", ["Chat with any model,", "<em>completely offline.</em>"], "hd").replace('id="h3"', 'id="h3" style="top:300px;font-size:80px"'))
R.mask_lines("#h3", S[3] - .05)
MODELS = [("Qwen 3", "qwen", -330, -40, -6), ("Llama 3.2", "llama", 330, 60, 5), ("Gemma 3", "gemma", -320, 300, 4)]
for k, (lab, w, x, y, r) in enumerate(MODELS):
    H(f'<div class="mdl" id="md{k}">{lab}</div>')
    tk = wt("f03", w) - .05
    R.ft(f"#md{k}", tk, .55, "{opacity: 1, x: 0, y: 0, scale: .3, rotation: 0}", f"{{x: {x}, y: {y}, scale: 1, rotation: {r}}}", "back.out(1.8)")
    R.st(f"#md{k}", 0, "{opacity: 0}")
    R.sfx("pop", tk)
H('<div class="chip off" id="off2" style="left:340px;top:1360px">Works offline</div>')
R.ft("#off2", wt("f03", "offline") - .1, .5, "{opacity: 1, y: 30}", "{y: 0}", "back.out(2)")
R.st("#off2", 0, "{opacity: 0}")
R.leave("#h3", S[4] - .22, .3)
for sel in ("#md0", "#md1", "#md2", "#off2"):
    R.leave(sel, S[4] - .22, .3)

# ---- f04: it makes images on your phone (image clip ends on the generated dog; the image pops out)
H(R.lines_html("h4", ["It even makes images,", "<em>right on your phone.</em>"], "hd").replace('id="h4"', 'id="h4" style="top:300px;font-size:80px"'))
H('<div class="imgpop soft" id="ipop"><img src="assets/img/og_image_last.jpg" alt=""><b>Generated on the phone</b></div>')
R.mask_lines("#h4", S[4] - .05)
tim = CLIPS[3][1] + 2.3                                         # the clip (4.6x) ends on the finished image
R.st("#imgend", tim - .05, "{opacity: 1}")
R.ft("#ipop", tim + .05, .6, "{opacity: 1, scale: .4, x: -140, y: 60, rotation: -8}", "{scale: 1, x: 0, y: 0, rotation: 4}", "back.out(1.7)")
R.st("#ipop", 0, "{opacity: 0}")
R.RISE_END["#ipop"] = tim + .65                                  # its exit waits for the entrance to finish
R.sfx("sparkle", tim + .05)
R.sfx("pop", tim + .1)
R.leave("#h4", S[5] - .22, .3)
R.leave("#ipop", S[5] - .22, .3)
R.st("#imgend", S[5] - .1, "{opacity: 0}")

# ---- f05: it reads photos and documents (vision clip, then the PDF clip; tags pop)
H(R.lines_html("h5", ["It reads your photos", "<em>and documents too.</em>"], "hd").replace('id="h5"', 'id="h5" style="top:300px;font-size:80px"'))
R.mask_lines("#h5", S[5] - .05)
for k, (lab, w, x, y) in enumerate((("Photos", "photos", 620, 700), ("PDFs", "documents", 620, 820))):
    H(f'<div class="chip" id="tg{k}" style="left:{x}px;top:{y}px">{lab}</div>')
    R.ft(f"#tg{k}", wt("f05", w) - .05, .45, "{opacity: 1, x: 60, scale: .8}", "{x: 0, scale: 1}", "back.out(2)")
    R.st(f"#tg{k}", 0, "{opacity: 0}")
    R.sfx("g_pop", wt("f05", w))
R.leave("#h5", S[6] - .22, .3)
for k in range(2):
    R.leave(f"#tg{k}", S[6] - .22, .3)

# ---- f06: your chats never leave your device (the phone shrinks into a lock; share line on screen)
a6 = S[6]
R.to("#stg", a6 - .25, .5, '{scale: .55, y: -40, opacity: 0, filter: "blur(10px)"}', "power3.in")
H('<div id="lock"><svg viewBox="0 0 64 64"><rect x="12" y="28" width="40" height="30" rx="8" fill="#7a2ffb"/><path d="M20 28v-8a12 12 0 0 1 24 0v8" fill="none" stroke="#b687f9" stroke-width="6" stroke-linecap="round"/>'
  '<circle cx="32" cy="42" r="4" fill="#fff"/></svg></div>')
H(R.lines_html("h6", ["Your chats", "<em>never leave your device.</em>"], "hd").replace('id="h6"', 'id="h6" style="top:960px;font-size:84px;text-align:center;left:60px;right:60px"'))
H('<div class="share" id="share">Send this to the friend who pays for AI every month.</div>')
R.ft("#lock", a6 - .05, .7, "{opacity: 1, scale: .3, rotation: -20}", "{scale: 1, rotation: 0}", "back.out(2)")
R.st("#lock", 0, "{opacity: 0}")
R.sfx("lock", a6 + .1)
R.mask_lines("#h6", a6 + .05)
R.rise("#share", wt("f06", "device") - .1, .6, 20, 6)
for sel in ("#lock", "#h6", "#share"):
    R.leave(sel, S[7] - .22, .3)

# ---- f07: CTA OFFLINE: the comment box types it; cut back to frame 1 so it loops
a7 = S[7]
H('<div class="cbox soft" id="cbox"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div>')
H('<div class="ctal" id="ctal">Comment <b>OFFLINE</b> and I\'ll send you the link</div>')
R.rise("#cbox", a7 - .05, .6, 40, 8)
R.rise("#ctal", a7 + .2, .6, 20, 6)
toff = wt("f07", "offline")
R.st("#cph", toff - .1, "{opacity: 0}")
R.typer("cty", toff - .1, "OFFLINE", .5)
R.sfx("typing", toff - .1)
R.ft("#cbox .send", toff + .55, .5, "{scale: 1.5}", "{scale: 1}", "back.out(3)")
R.sfx("notify", toff + .6)
H('<div id="loop"><div class="hd" style="top:300px;font-size:84px">Your phone can run<br>its own AI.<br><em>No internet.</em></div>'
  '<div class="lp"><img src="assets/img/og_text_first.jpg" alt=""></div></div>')
R.ft("#loop", R.DUR - .4, .35, "{opacity: 0}", "{opacity: 1}", "power2.inOut")

R.captions(top=1500, max_words=4)

R.write(f"""
.stage {{ top: 640px; }}
.phone {{ position: relative; margin: 0 auto; width: 400px; height: 860px; border-radius: 62px; background: #16131f; padding: 12px;
  box-shadow: 0 0 0 2px #2a2440, 0 60px 120px rgba(0,0,0,.7), 0 0 120px rgba(127,27,248,.35); transform-style: preserve-3d; }}
.isl {{ position: absolute; left: 50%; top: 24px; width: 110px; height: 32px; margin-left: -55px; border-radius: 20px; background: #000; z-index: 5; }}
.scr {{ position: relative; width: 100%; height: 100%; border-radius: 52px; overflow: hidden; background: #fff; }}
.scr img, .scr video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#imgend {{ opacity: 0; }}
.chip {{ position: absolute; display: flex; align-items: center; gap: 14px; background: #10022c; border: 2px solid {STAR}; color: {INK};
  font-family: Sat; font-weight: 700; font-size: 34px; padding: 14px 26px; border-radius: 999px; z-index: 25; box-shadow: 0 16px 40px rgba(0,0,0,.45); white-space: nowrap; }}
.chip svg {{ width: 34px; height: 34px; color: {PINK}; }}
.chip.off {{ border-color: {GREEN}; }} .chip.off svg {{ color: {GREEN}; }}
.repo {{ position: absolute; left: 70px; right: 70px; top: 640px; border-radius: 36px; padding: 34px 36px; background: #10022c; border: 2px solid #2b1460; z-index: 22; }}
.rh {{ display: flex; align-items: center; gap: 16px; font-family: Mono; font-size: 28px; color: rgba(255,255,255,.7); }}
.rh svg {{ width: 40px; height: 40px; color: #fff; }}
.rh b {{ color: #fff; font-weight: 700; }}
.rb {{ display: flex; align-items: center; gap: 24px; margin: 28px 0 26px; }}
.rb img {{ width: 120px; height: 120px; border-radius: 28px; }}
.rb b {{ display: block; font-family: Mont; font-weight: 800; font-size: 60px; letter-spacing: -.03em; }}
.rb span {{ display: block; font-family: Sat; font-weight: 500; font-size: 30px; color: rgba(255,255,255,.72); margin-top: 6px; }}
.rt {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.rt i {{ font-style: normal; font-family: Sat; font-weight: 700; font-size: 30px; padding: 10px 20px; border-radius: 999px; background: #1e0b4a; border: 2px solid #3a1d7a; }}
.rt i.g {{ background: {GREEN}; color: #062a1b; border-color: {GREEN}; font-weight: 900; }}
#checks {{ position: absolute; left: 560px; right: 50px; top: 760px; z-index: 22; display: flex; flex-direction: column; gap: 18px; }}
.ck {{ display: flex; align-items: center; gap: 14px; background: rgba(16,2,44,.92); border: 2px solid #2b1460; border-radius: 22px; padding: 18px 20px;
  font-family: Sat; font-weight: 700; font-size: 30px; line-height: 1.15; }}
.ck i {{ width: 44px; height: 44px; flex: none; border-radius: 50%; background: {GREEN}; color: #062a1b; display: grid; place-items: center; font-style: normal; font-weight: 900; font-size: 26px; }}
.mdl {{ position: absolute; left: 400px; top: 1000px; width: 280px; text-align: center; background: #fff; color: #10022c; font-family: Mont; font-weight: 800; font-size: 40px;
  padding: 20px 0; border-radius: 26px; z-index: 26; box-shadow: 0 30px 60px rgba(0,0,0,.5), 0 0 40px rgba(127,27,248,.4); }}
.imgpop {{ position: absolute; left: 560px; top: 700px; width: 440px; border-radius: 30px; overflow: hidden; background: #fff; z-index: 26; }}
.imgpop img {{ display: block; width: 100%; height: 520px; object-fit: cover; object-position: 50% 62%; }}
.imgpop b {{ display: block; padding: 18px 22px; font-family: Sat; font-weight: 900; font-size: 30px; color: #10022c; }}
#lock {{ position: absolute; left: 390px; top: 600px; width: 300px; height: 300px; z-index: 22; filter: drop-shadow(0 0 60px rgba(127,27,248,.6)); }}
#lock svg {{ width: 100%; height: 100%; }}
.share {{ position: absolute; left: 90px; right: 90px; top: 1260px; text-align: center; font-family: Sat; font-weight: 500; font-size: 40px; color: rgba(255,255,255,.75); z-index: 22; }}
.cbox {{ position: absolute; left: 110px; width: 860px; top: 820px; height: 140px; border-radius: 70px; background: #10022c; border: 2px solid {STAR}; display: flex; align-items: center;
  gap: 22px; padding: 0 32px; font-family: Sat; font-weight: 900; font-size: 60px; letter-spacing: .04em; z-index: 24; }}
.cbox .av {{ width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, {STAR}, {PINK}); flex: none; }}
#cph {{ position: absolute; left: 136px; color: rgba(255,255,255,.4); font-weight: 500; font-size: 46px; letter-spacing: 0; }}
.cbox .send {{ margin-left: auto; color: #d9c2ff; }}
.ctal {{ position: absolute; left: 0; right: 0; top: 1000px; text-align: center; font-family: Sat; font-weight: 700; font-size: 42px; color: rgba(255,255,255,.82); z-index: 24; }}
.ctal b {{ color: {PINK}; font-weight: 900; }}
#loop {{ position: absolute; inset: -60px; opacity: 0; z-index: 50; background: #07050f; }}
#loop .hd {{ transform: translate(60px, 60px); }}
#loop .lp {{ position: absolute; left: 400px; top: 700px; width: 400px; height: 860px; border-radius: 62px; overflow: hidden; border: 12px solid #16131f;
  transform: perspective(1900px) rotateY(-12deg) rotateX(6deg) translateY(60px); }}
#loop .lp img {{ width: 100%; height: 100%; object-fit: cover; }}
""")
