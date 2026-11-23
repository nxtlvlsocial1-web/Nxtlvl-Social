"""Creedom remake 2, "Graded before anyone saw it" (Creators 100X, 9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

Built on .claude/skills/nxtlvl-social-video/references/reach-psychology.md after CHECK v1 flatlined (270 views, 4 s
average watch, 0 shares). Script: creedom-check-9x16/plan/script_remake_v2.md. The scores are an example (owner: make
them), shown with an EXAMPLE tag: 2.9 / 5 -> 4.4 / 5, flags at 0:01, 0:07, 0:14.
Frame 1: a reel on a phone and a score dial slamming to 2.9 (result-first hook); the three flagged seconds; the fix and
the climb to 4.4; Creedom only at about 65 %, in its pink world; the CTA (CHECK) and a cut back to the dial (loop).
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


# ---- top caption pills
PILLS = ["Scored <b>before</b><br>anyone saw it.", "Look where it<br>lost points.", "3 seconds cost it.", "Fix 3 seconds.",
         "It's <b>Creedom</b>.", 'Comment <b>CHECK</b>']
for k, (lid, txt) in enumerate(zip(IDS, PILLS)):
    HTML.append(f'<div class="pill" id="p{k}"><span>{txt}</span></div>')
    a, b = S[k], S[k + 1]
    ft(f"#p{k}", a - .06, .3, "{opacity: 0, y: 24, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.2)")
    if k < len(IDS) - 1:
        to(f"#p{k}", b - .12, .12, "{opacity: 0, y: -16}", "power2.in")

C = 540.35                                     # dial circumference (r = 86)
def dial_to(t, frm, score, d=.7, col="#ff2d55"):
    """the arc and the number move together; both are pure functions of the timeline position"""
    js(f'tl.to("#arc", {{strokeDashoffset: {C * (1 - score / 5):.1f}, stroke: "{col}", duration: {d}, ease: "power3.out"}}, {t:.3f});')
    js(f'(() => {{ const o = {{v: {frm}}}; tl.to(o, {{v: {score}, duration: {d}, ease: "power3.out", '
       f'onUpdate: () => {{ document.getElementById("score").textContent = o.v.toFixed(1); }}}}, {t:.3f}); }})();')

# ---- scene 1-2: phone + dial (result first), flags on the timeline
HTML.append('<div id="phone"><img id="frame" src="assets/img/demo_f01.jpg" alt=""><b class="ex">EXAMPLE</b></div>')
HTML.append('<div id="dial"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="trk"/><circle cx="100" cy="100" r="86" class="arc" id="arc"/></svg>'
            '<div class="sc"><b id="score">0.0</b><span>/ 5</span></div></div>')
HTML.append('<div id="tline"><i class="bar"></i>' + "".join(f'<i class="flag" id="fl{k}" style="left:{x}%"><em>{lab}</em></i>' for k, (x, lab) in enumerate([(5, "0:01"), (35, "0:07"), (70, "0:14")])) + '</div>')
st("#phone", 0, "{opacity: 1}")
st("#dial", 0, "{opacity: 1}")
ft("#phone", 0, .45, "{scale: 1.06, rotation: -4}", "{scale: 1, rotation: -3}", "power3.out")
ft("#dial", 0, .4, "{scale: .6}", "{scale: 1}", "back.out(2)")
js(f'tl.set("#arc", {{strokeDashoffset: {C:.1f}}}, 0);')
dial_to(.12, 0, 2.9, .55)
sfx("riser_short", 0)
sfx("buzzer", .62)
sfx("impact", .64)
ft("#dial", .66, .3, "{x: 0}", "{keyframes: [{x: -14, duration: .05}, {x: 12, duration: .05}, {x: -6, duration: .05}, {x: 0, duration: .1}]}", "none")
a1 = S[1]
ft("#tline", a1 + .1, .35, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}")
for k in range(3):
    ft(f"#fl{k}", a1 + .45 + k * .18, .3, "{opacity: 0, y: -30, scale: .5}", "{opacity: 1, y: 0, scale: 1}", "back.out(3)")
    sfx("pop", a1 + .45 + k * .18)

# ---- scene 3: each flagged second, frame + note
a2 = S[2]
NOTES = [("one", "demo_f01.jpg", "0:01", "Hook too slow"), ("seven", "demo_f07.jpg", "0:07", "A claim, no proof"), ("fourteen", "demo_f14.jpg", "0:14", "Loses trust")]
HTML.append('<div id="notes">' + "".join(f'<div class="note" id="n{k}"><b>{ts}</b><span>{txt}</span><i class="ok">&#10003;</i></div>' for k, (_, _, ts, txt) in enumerate(NOTES)) + '</div>')
to("#dial", a2 - .1, .4, "{x: 250, y: -330, scale: .55}", "power3.inOut")
for k, (word, img, ts, txt) in enumerate(NOTES):
    tw = wt("f02", word)
    st("#frame", tw - .05, f'{{attr: {{src: "assets/img/{img}"}}}}')
    ft("#phone", tw - .05, .3, "{scale: 1.05}", "{scale: 1}", "power2.out")
    ft(f"#n{k}", tw - .05, .35, "{opacity: 0, x: 60}", "{opacity: 1, x: 0}", "back.out(1.8)")
    ft(f"#fl{k}", tw - .05, .35, "{scale: 1.5}", "{scale: 1}", "back.out(2)")
    sfx("g_wrong" if k < 2 else "thump", tw)

# ---- scene 4: fix the three seconds, the dial climbs to 4.4
a3 = S[3]
tfix = wt("f03", "fix")
for k in range(3):
    st(f"#n{k}", tfix + .25 + k * .22, "{className: 'note fixed'}")
    ft(f"#n{k} .ok", tfix + .25 + k * .22, .3, "{scale: 0}", "{scale: 1}", "back.out(3)")
    st(f"#fl{k}", tfix + .25 + k * .22, "{className: 'flag fixed'}")
    sfx("click", tfix + .25 + k * .22)
t44 = wt("f03", "four")
to("#dial", t44 - .35, .35, "{x: 0, y: 0, scale: 1}", "power3.out")
dial_to(t44 - .05, 2.9, 4.4, .7, "#20c070")
sfx("g_levelup", t44)
sfx("sparkle", t44 + .1)

# ---- scene 5: Creedom reveal (pink world), CHECK card, Cree
a4 = S[4]
HTML.append('<div id="world"><i class="bl b1"></i><i class="bl b2"></i><i class="bl b3"></i></div>')
HTML.append('<div id="app"><img src="assets/img/creedom_logo.png" alt=""><div class="q">How can Cree help?</div>'
            '<div class="tile"><i>&#9654;</i><div><b>Check a reel before you post</b><span>Score out of 5, the exact second, and the fix</span></div></div>'
            '<div class="tile dim"><i>&#9998;</i><div><b>Get a script in your voice</b></div></div></div>')
HTML.append('<img id="cree" src="assets/img/poses/proud.png" alt="">')
ft("#world", a4 - .2, .5, "{opacity: 0}", "{opacity: 1}")
to("#phone", a4 - .2, .4, "{opacity: 0, x: -300}", "power2.in")
to("#tline", a4 - .2, .3, "{opacity: 0}")
to("#notes", a4 - .2, .3, "{opacity: 0, x: 200}", "power2.in")
to("#dial", a4 - .2, .5, "{x: 270, y: 640, scale: .5}", "power3.inOut")
ft("#app", a4, .5, "{opacity: 0, y: 80, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.5)")
ft("#cree", a4 + .3, .5, "{opacity: 0, x: 200, rotation: 12}", "{opacity: 1, x: 0, rotation: 0}", "back.out(1.6)")
sfx("whoosh_big", a4 - .2)
sfx("sparkle", a4 + .1)

# ---- scene 6: CTA (CHECK), share sticker, loop back to the 2.9 dial
a5 = S[5]
HTML.append('<div id="cta"><div class="share"><b>&#10148;</b><span>send to the friend who posts and prays</span></div>'
            '<div class="cbox"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div></div>')
to("#app", a5 - .1, .3, "{y: -60, scale: .9}", "power2.out")
ft("#cta", a5, .4, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(1.6)")
st("#cree", a5, '{attr: {src: "assets/img/poses/wave.png"}}')
tc = wt("f05", "comment")
st("#cph", tc + .1, "{opacity: 0}")
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 5, duration: .5, ease: "steps(5)", onUpdate: () => {{ document.getElementById("cty").textContent = "CHECK".slice(0, Math.round(o.n)); }}}}, {tc + .1:.3f}); }})();')
sfx("whoosh", a5 - .1)
sfx("typing", tc + .1)
sfx("click", tc + .7)
sfx("notify", tc + .9)
HTML.append('<div id="loop"><div class="lp"><img src="assets/img/demo_f01.jpg" alt=""></div><div class="ld"><b>2.9</b><span>/ 5</span></div></div>')
st("#loop", DUR - .4, "{opacity: 1}")

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
#phone {{ position: absolute; left: 100px; top: 560px; width: 428px; height: 760px; border-radius: 44px; overflow: hidden; background: #000; opacity: 0;
  border: 10px solid #16121a; box-shadow: 0 40px 90px rgba(22,18,26,.35); z-index: 12; transform: rotate(-3deg); }}
#phone img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ex {{ position: absolute; left: 18px; top: 18px; background: rgba(22,18,26,.75); color: #fff; font-family: Mono; font-weight: 700; font-size: 22px; letter-spacing: .14em;
  padding: 6px 14px; border-radius: 10px; }}
#dial {{ position: absolute; left: 520px; top: 700px; width: 460px; height: 460px; opacity: 0; z-index: 14; }}
#dial svg {{ width: 100%; height: 100%; transform: rotate(-90deg); filter: drop-shadow(0 24px 40px rgba(22,18,26,.22)); }}
.trk {{ fill: #fff; stroke: #ece6de; stroke-width: 16; }}
.arc {{ fill: none; stroke: #ff2d55; stroke-width: 16; stroke-linecap: round; stroke-dasharray: 540.35; }}
.sc {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 160px; gap: 10px; }}
.sc b {{ font-weight: 800; font-size: 150px; letter-spacing: -.04em; line-height: 1; }}
.sc span {{ font-weight: 700; font-size: 52px; color: #8a8290; }}
#tline {{ position: absolute; left: 90px; right: 90px; top: 1322px; height: 70px; opacity: 0; z-index: 13; }}
#tline .bar {{ position: absolute; left: 0; right: 0; top: 44px; height: 10px; border-radius: 6px; background: #e3ddd4; }}
.flag {{ position: absolute; top: 0; width: 26px; height: 60px; margin-left: -13px; opacity: 0; }}
.flag::before {{ content: ""; position: absolute; left: 11px; top: 0; width: 5px; height: 60px; background: #ff2d55; border-radius: 3px; }}
.flag em {{ position: absolute; left: 20px; top: -6px; font-style: normal; font-family: Mono; font-weight: 700; font-size: 26px; color: #fff; background: #ff2d55;
  padding: 3px 10px; border-radius: 8px; white-space: nowrap; }}
.flag.fixed::before, .flag.fixed em {{ background: #20c070; }}
#notes {{ position: absolute; left: 590px; right: 60px; top: 720px; display: flex; flex-direction: column; gap: 22px; z-index: 15; }}
.note {{ position: relative; background: #fff; border-radius: 24px; padding: 18px 22px 20px; border-left: 10px solid #ff2d55; box-shadow: 0 16px 36px rgba(22,18,26,.12); opacity: 0; }}
.note b {{ display: block; font-family: Mono; font-weight: 700; font-size: 30px; color: #ff2d55; }}
.note span {{ display: block; font-weight: 800; font-size: 38px; line-height: 1.1; letter-spacing: -.02em; }}
.note .ok {{ position: absolute; right: 16px; top: 16px; width: 50px; height: 50px; border-radius: 50%; background: #20c070; color: #fff; display: grid; place-items: center;
  font-style: normal; font-weight: 800; font-size: 32px; transform: scale(0); }}
.note.fixed {{ border-left-color: #20c070; }} .note.fixed b {{ color: #20c070; }}
#world {{ position: absolute; inset: 0; opacity: 0; z-index: 18; overflow: hidden;
  background: radial-gradient(120% 90% at 50% 30%, #ffffff 0%, #fbf0f6 55%, #f6e3ee 100%); }}
.bl {{ position: absolute; border-radius: 50%; filter: blur(90px); }}
.b1 {{ left: -160px; top: 200px; width: 620px; height: 620px; background: rgba(255,61,139,.35); }}
.b2 {{ right: -200px; top: 900px; width: 700px; height: 700px; background: rgba(160,100,255,.28); }}
.b3 {{ left: 200px; bottom: -200px; width: 600px; height: 500px; background: rgba(255,170,210,.4); }}
#app {{ position: absolute; left: 70px; right: 70px; top: 560px; opacity: 0; z-index: 20; border-radius: 40px; padding: 34px 36px 38px;
  background: linear-gradient(135deg, rgba(255,255,255,.88), rgba(255,255,255,.62)); border: 2px solid rgba(255,255,255,.95);
  box-shadow: 0 30px 80px rgba(160,20,90,.18); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); }}
#app img {{ height: 70px; display: block; }}
.q {{ margin: 26px 0 22px; font-family: Serif; font-style: italic; font-size: 64px; }}
.tile {{ display: flex; gap: 20px; align-items: center; background: #fff; border-radius: 26px; padding: 22px 24px; margin-top: 16px; border: 4px solid #ff3d8b;
  box-shadow: 0 14px 30px rgba(255,61,139,.18); }}
.tile i {{ width: 74px; height: 74px; border-radius: 20px; background: #ff3d8b; color: #fff; display: grid; place-items: center; font-style: normal; font-size: 34px; flex: none; }}
.tile b {{ display: block; font-weight: 800; font-size: 38px; letter-spacing: -.02em; }}
.tile span {{ display: block; font-weight: 600; font-size: 28px; color: #6b6470; }}
.tile.dim {{ border-color: transparent; opacity: .55; box-shadow: none; }}
.tile.dim i {{ background: #d9d2c8; }}
#cree {{ position: absolute; right: 30px; top: 1080px; width: 300px; opacity: 0; z-index: 22; filter: drop-shadow(0 20px 30px rgba(160,20,90,.25)); }}
#cta {{ position: absolute; left: 70px; right: 70px; top: 1150px; opacity: 0; z-index: 24; display: flex; flex-direction: column; gap: 22px; align-items: flex-start; }}
.share {{ display: flex; align-items: center; gap: 14px; background: {INK}; color: #fff; padding: 14px 26px; border-radius: 999px; font-weight: 700; font-size: 34px; }}
.share b {{ color: {PINK}; font-size: 36px; }}
.cbox {{ position: relative; width: 640px; height: 96px; border-radius: 48px; background: #fff; border: 2px solid rgba(22,18,26,.12); display: flex; align-items: center;
  gap: 18px; padding: 0 24px; font-weight: 800; font-size: 40px; box-shadow: 0 14px 34px rgba(22,18,26,.12); }}
.cbox .av {{ width: 58px; height: 58px; border-radius: 50%; background: linear-gradient(135deg, #ff3d8b, #a064ff); flex: none; }}
#cph {{ position: absolute; left: 100px; color: rgba(22,18,26,.4); font-weight: 600; }}
.send {{ margin-left: auto; color: {PINK}; }}
.cap {{ position: absolute; left: 70px; right: 70px; top: 1418px; text-align: center; font-weight: 800; font-size: 50px; line-height: 1.15; letter-spacing: -.02em;
  opacity: 0; z-index: 40; text-shadow: 0 0 18px rgba(255,255,255,.9), 0 0 4px rgba(255,255,255,.9); }}
.cw {{ color: rgba(22,18,26,.32); }}
#loop {{ position: absolute; inset: 0; opacity: 0; z-index: 58; background: #f4f1ec; }}
#loop .lp {{ position: absolute; left: 100px; top: 560px; width: 428px; height: 760px; border-radius: 44px; overflow: hidden; border: 10px solid #16121a; transform: rotate(-3deg); }}
#loop .lp img {{ width: 100%; height: 100%; object-fit: cover; }}
#loop .ld {{ position: absolute; left: 520px; top: 700px; width: 460px; height: 460px; border-radius: 50%; background: #fff; display: flex; align-items: baseline;
  justify-content: center; padding-top: 160px; gap: 10px; border: 16px solid #ff2d55; }}
#loop .ld b {{ font-weight: 800; font-size: 150px; letter-spacing: -.04em; line-height: 1; }} #loop .ld span {{ font-weight: 700; font-size: 52px; color: #8a8290; }}
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom remake: graded before anyone saw it 9x16</title>
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
