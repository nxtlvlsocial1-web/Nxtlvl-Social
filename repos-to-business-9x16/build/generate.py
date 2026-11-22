"""AI.NXTLVL "6 free GitHub projects you can turn into businesses" (9:16): writes index.html, plan/sfx_events.json, plan/edit.json.

Owner: "recreate this more engaging, 3D render under 50 s, with caption, title and all" (reference: a 69 s flat 2D
"6 open-source projects you can turn into businesses" reel). The 3D (assets/js/scene.js) is timed to the voice through
window.RB_T; this file lays the type over it on one paused GSAP timeline:
  top bar (wordmark, series line) and a shelf of six slots that fills 0/6 -> 6/6 as each repo is covered;
  per repo: "01 / 06", the name in its accent colour, a licence chip (facts checked, plan/facts.md), the business idea
  pill on the business line; Remotion gets its licence footnote;
  karaoke captions (spoken words timed by Whisper, shown in the script's spelling); the close lines; the CTA comment bar.
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
ACC = ["#ff4d6d", "#3d8bff", "#9b5cff", "#22d3ee", "#ff3b30", "#f5b941"]


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
L = [[LW[i][0]["t0"], LW[i][-1]["t1"]] for i in IDS]
END = L[-1][1]
DUR = round(END + 1.6, 2)
L.append([DUR, DUR])                      # sentinel: "next line" after the CTA
REPOS = [  # name, licence chip, business idea, the word the business line starts on
    ("AutoClip", "MIT LICENCE", "Clipping service for creators", ("f01", "sell")),
    ("Remotion", "FREE: SOLO & TEAMS OF 3", "Video factory for agencies", ("f02", "run")),
    ("OpenHands", "MIT LICENCE", "Apps for local businesses", ("f03", "build")),
    ("PersonaLive", "APACHE-2.0", "Your own virtual influencer", ("f04", "launch")),
    ("RedInk", "FREE ON GITHUB", "Post-writing service for brands", ("f05", "sell")),
    ("MuMuAINovel", "FREE ON GITHUB", "AI publishing studio", ("f06", "start")),
]
BIZ = [wt(l, w) for _, _, _, (l, w) in REPOS]
T = {"lines": [[round(a, 3), round(b, 3)] for a, b in L], "biz": [round(b, 3) for b in BIZ],
     "close": L[7][0], "pack": wt("f07", "packaging"), "cta": L[8][0], "end": DUR}

# ---- top bar and shelf
HTML.append('<div id="bar"><img src="assets/img/logo-wordmark.png" alt=""><span>6 FREE REPOS &#8594; 6 BUSINESSES</span></div>')
slots = "".join(f'<div class="slot" id="slot{k}" style="--c:{ACC[k]}"><b>{k + 1:02d}</b><i>{REPOS[k][0]}</i></div>' for k in range(6))
HTML.append(f'<div id="shelf">{slots}<div id="cnt"><span id="cntn">0</span>/6</div></div>')
ft("#bar", 0, .4, "{opacity: 0, y: -20}", "{opacity: 1, y: 0}")
ft("#shelf", .2, .45, "{opacity: 0, y: -20}", "{opacity: 1, y: 0}")
for k in range(6):
    tf = L[k + 1][0] + 1.12                    # the opened cube lands in its slot
    ft(f"#slot{k}", tf, .35, "{scale: 1}", "{keyframes: [{scale: 1.25, duration: .12}, {scale: 1, duration: .23}]}", "none")
    st(f"#slot{k}", tf, "{className: 'slot on'}")
    st("#cntn", tf, f'{{textContent: "{k + 1}"}}')
    sfx("click", tf)

# ---- hook title
HTML.append('<div class="ttl" id="t-hook"><div class="big">6 free GitHub projects</div><div class="sub">you can turn into a <i>business</i></div></div>')
ft("#t-hook .big", .0, .4, "{opacity: 0, y: 30, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
ft("#t-hook .sub", wt("f00", "could") - .1, .4, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "back.out(1.8)")
to("#t-hook", L[1][0] - .15, .15, "{opacity: 0, y: -30, filter: 'blur(8px)'}", "power2.in")

# ---- per repo: number, name, licence chip, business pill
for k, (name, lic, biz, _) in enumerate(REPOS):
    a, b = L[k + 1][0], L[k + 2][0]
    note = '<div class="note">Free for individuals and teams up to 3. Companies need a licence.</div>' if name == "Remotion" else ""
    HTML.append(f'<div class="ttl repo" id="t{k}" style="--c:{ACC[k]}"><div class="num">{k + 1:02d} / 06</div>'
                f'<div class="name">{name}</div><div class="lic">{lic}</div>{note}</div>')
    HTML.append(f'<div class="biz" id="b{k}" style="--c:{ACC[k]}"><span>BUSINESS IDEA</span><b>{biz}</b></div>')
    ft(f"#t{k} .num", a - .15, .3, "{opacity: 0, x: -30}", "{opacity: 1, x: 0}")
    ft(f"#t{k} .name", a - .1, .45, "{opacity: 0, y: 40, scale: .85, rotationX: -60}", "{opacity: 1, y: 0, scale: 1, rotationX: 0}", "back.out(1.7)")
    ft(f"#t{k} .lic", a + .35, .3, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.5)")
    if note:
        ft(f"#t{k} .note", a + .6, .35, "{opacity: 0}", "{opacity: 1}")
    ft(f"#b{k}", BIZ[k] - .08, .4, "{opacity: 0, y: 30, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
    to(f"#t{k}", b - .2, .18, "{opacity: 0, y: -30, filter: 'blur(8px)'}", "power2.in")
    to(f"#b{k}", b - .2, .18, "{opacity: 0, y: 20}", "power2.in")
    # sound: drop in, land, lid, the diorama, the business line, the exit
    sfx("whoosh", a - .32)
    sfx("thump", a + .22)
    sfx("g_pickup", a + .3)
    sfx("riser_short", a - .05)
    sfx("ding", BIZ[k] - .02)
    sfx("swish", b - .45)
    special = {0: [("pop", a + 1.1 + i * .45) for i in range(3)],
               1: [("tick", a + 1.4 + i * .55) for i in range(5)],
               2: [("typing", a + 1.1)] + [("pop", BIZ[k] + i * .15) for i in range(3)],
               3: [("notify", a + 1.2)],
               4: [("g_drop", a + 1.22), ("sparkle", a + 1.4)],
               5: [("g_swish", a + .8), ("g_swish", a + 1.35)]}[k]
    for kind, tt in special:
        sfx(kind, tt)

# ---- close
HTML.append('<div class="ttl" id="t-close"><div class="big">The code is <span class="v">free.</span></div>'
            '<div class="sub" id="t-close2">The money is in <i>packaging.</i></div></div>')
c0, cp = L[7][0], T["pack"]
ft("#t-close .big", c0 - .1, .4, "{opacity: 0, y: 30, scale: .92}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
ft("#t-close2", wt("f07", "money") - .1, .4, "{opacity: 0, y: 24}", "{opacity: 1, y: 0}", "back.out(1.8)")
to("#t-close", L[8][0] - .15, .15, "{opacity: 0, y: -30, filter: 'blur(8px)'}", "power2.in")
sfx("whoosh_big", c0 - .25)
for k in range(6):
    sfx("g_drop", c0 + .55 + k * .14)
sfx("impact", cp + .6)
sfx("cash", cp + .6)

# ---- CTA: comment bar types REPOS
HTML.append('<div id="cta"><div class="ct1">Comment <b>REPOS</b></div><div class="ct2">and I\'ll send you all six links</div>'
            '<div class="cbox"><span class="av"></span><span id="cph">Add a comment&#8230;</span><span id="cty"></span><span class="send">&#10148;</span></div></div>')
ca = L[8][0]
ft("#cta", ca - .1, .45, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(1.6)")
tr = wt("f08", "repos")
st("#cph", tr - .05, "{opacity: 0}")
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 5, duration: .5, ease: "steps(5)", onUpdate: () => {{ document.getElementById("cty").textContent = "REPOS".slice(0, Math.round(o.n)); }}}}, {tr - .05:.3f}); }})();')
ft(".send", tr + .55, .3, "{scale: 1}", "{keyframes: [{scale: 1.4, duration: .12}, {scale: 1, duration: .18}]}", "none")
sfx("typing", tr - .05)
sfx("click", tr + .55)
sfx("notify", tr + .75)

# ---- hook sounds
for k in range(6):
    sfx("g_drop", .5 + k * .09)
sfx("riser", L[1][0] - 1.0)

# ---- karaoke captions: the spoken words timed by Whisper, shown in the script's spelling, 3-5 words a card
CAP = []
for ln in SCRIPT:
    if ln["id"] == "f08":                      # the CTA card carries its own words
        continue
    disp, ws = ln["display"].split(), LW[ln["id"]]
    n, m = len(disp), len(ws)
    timed = []
    for i, dw in enumerate(disp):              # display word i -> spoken word (same index when counts match)
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
    ft(f"#cap{ci}", t0 - .06, .16, "{y: 14, scale: .96}", "{y: 0, scale: 1}", "power2.out")
    st(f"#cap{ci}", min(nxt - .08, t1 + .9, L[8][0] - .15), "{opacity: 0}")
    for k, (_, a, _) in enumerate(chunk):
        st(f"#c{ci}_{k}", a - .03, "{color: '#ffffff', scale: 1.08}")
        to(f"#c{ci}_{k}", a + .08, .15, "{scale: 1}")

CSS = """
@font-face { font-family: Mont; font-weight: 800; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #07050f; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Mont; color: #fff; background: #07050f; }
#gl { position: absolute; inset: 0; width: 1080px; height: 1920px; }
#bar { position: absolute; left: 66px; right: 66px; top: 258px; height: 40px; display: flex; align-items: center; justify-content: space-between; opacity: 0;
  font-family: Mono; font-weight: 700; font-size: 22px; letter-spacing: .12em; color: #b687f9; }
#bar img { height: 34px; }
#shelf { position: absolute; left: 66px; right: 66px; top: 318px; display: flex; gap: 10px; align-items: center; opacity: 0; }
.slot { flex: 1; height: 58px; border-radius: 14px; border: 2px dashed rgba(182,135,249,.35); display: flex; flex-direction: column; align-items: center;
  justify-content: center; font-family: Mono; font-weight: 700; color: rgba(182,135,249,.5); background: rgba(16,2,44,.45); }
.slot b { font-size: 20px; line-height: 1; }
.slot i { font-style: normal; font-size: 11px; letter-spacing: .02em; opacity: 0; max-width: 100%; overflow: hidden; white-space: nowrap; }
.slot.on { border: 2px solid var(--c); background: color-mix(in srgb, var(--c) 30%, #10022c); color: #fff; box-shadow: 0 0 18px color-mix(in srgb, var(--c) 60%, transparent); }
.slot.on i { opacity: .95; }
#cnt { width: 86px; text-align: right; font-family: Mono; font-weight: 700; font-size: 30px; color: #fff; }
.ttl { position: absolute; left: 66px; right: 66px; top: 410px; text-align: center; perspective: 900px; }
.ttl .big { font-weight: 800; font-size: 84px; line-height: 1.02; letter-spacing: -.035em; opacity: 0; text-shadow: 0 6px 30px rgba(0,0,0,.6); }
.ttl .sub { margin-top: 10px; font-weight: 800; font-size: 62px; letter-spacing: -.03em; opacity: 0; color: #e9dcff; }
.ttl i, .ttl .sub i { font-family: Serif; font-style: italic; font-weight: 400; color: #b687f9; font-size: 1.18em; letter-spacing: -.01em; }
.v { color: #b687f9; }
.repo .num { font-family: Mono; font-weight: 700; font-size: 28px; letter-spacing: .2em; color: var(--c); opacity: 0; }
.repo .name { margin-top: 6px; font-weight: 800; font-size: 104px; line-height: 1; letter-spacing: -.045em; color: #fff; opacity: 0;
  text-shadow: 0 0 40px color-mix(in srgb, var(--c) 55%, transparent), 0 6px 26px rgba(0,0,0,.6); }
.repo .lic { display: inline-block; margin-top: 18px; padding: 8px 18px; border-radius: 999px; border: 2px solid var(--c); color: var(--c); font-family: Mono;
  font-weight: 700; font-size: 22px; letter-spacing: .12em; opacity: 0; background: rgba(7,5,15,.55); }
.note { margin-top: 12px; font-family: Mono; font-weight: 700; font-size: 20px; color: rgba(255,255,255,.7); opacity: 0; }
.biz { position: absolute; left: 50%; top: 1222px; transform: translateX(-50%); min-width: 620px; padding: 16px 30px 18px; border-radius: 26px; text-align: center; opacity: 0;
  background: linear-gradient(160deg, rgba(26,14,52,.94), rgba(14,6,30,.94)); border: 2px solid var(--c); box-shadow: 0 0 34px color-mix(in srgb, var(--c) 45%, transparent); }
.biz span { display: block; font-family: Mono; font-weight: 700; font-size: 20px; letter-spacing: .2em; color: var(--c); }
.biz b { display: block; margin-top: 4px; font-weight: 800; font-size: 44px; letter-spacing: -.02em; white-space: nowrap; }
.cap { position: absolute; left: 70px; right: 70px; top: 1374px; text-align: center; font-weight: 800; font-size: 54px; line-height: 1.12; letter-spacing: -.02em;
  opacity: 0; text-shadow: 0 4px 18px rgba(0,0,0,.85); }
.cw { display: inline-block; color: rgba(255,255,255,.42); }
#cta { position: absolute; left: 66px; right: 66px; top: 1190px; text-align: center; opacity: 0; }
.ct1 { font-weight: 800; font-size: 70px; letter-spacing: -.03em; }
.ct1 b { color: #b687f9; }
.ct2 { margin-top: 4px; font-family: Serif; font-style: italic; font-size: 46px; color: #e9dcff; }
.cbox { margin: 22px auto 0; width: 820px; height: 92px; border-radius: 46px; background: rgba(255,255,255,.08); border: 2px solid rgba(182,135,249,.5);
  display: flex; align-items: center; gap: 18px; padding: 0 22px; font-weight: 800; font-size: 36px; text-align: left; position: relative; }
.cbox .av { width: 54px; height: 54px; border-radius: 50%; background: linear-gradient(135deg, #7f1bf8, #6008f2); flex: none; }
#cph { position: absolute; left: 96px; color: rgba(255,255,255,.45); font-weight: 600; }
#cty { color: #fff; }
.send { margin-left: auto; color: #b687f9; font-size: 40px; display: inline-block; }
"""
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI.NXTLVL 6 free repos to businesses 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920"></canvas>
      {chr(10).join(HTML)}
    </div>
    <script>window.RB_T = {json.dumps(T)};</script>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/scene.js"></script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, {len(CAP)} caption cards")
