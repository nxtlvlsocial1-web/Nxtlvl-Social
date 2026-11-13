"""Creators 100X "STUDY" reel (9:16): writes index.html and plan/sfx_events.json from plan/words.json.

Look and pacing from the Creators 100X hook reel (reel-flop-9x16): an off-white ground with drifting lime, pink and
peach glows and grain; black Inter 800 headlines that rise in word by word on the voice, the key word in the red-pink
gradient; a numbered list whose active item turns pink and the rest go grey; a comment box that types the keyword and a
stack of comments flying up. The hero is an animated ChatGPT phone screen (dark theme, as in the owner's recording):
the chapter PDF attached, the prompt typed, "Creating image", then each result revealed top-down from a blur.
Results: 1 manga = the owner's real ChatGPT output; 2 timeline, 3 mind map = Canva; 4 diagram, 5 revision sheet =
build/results.cjs (Canva was on a credit cooldown). The owner chose to show all five inside the ChatGPT screen.
python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
INK, RED = "#121212", "#ff2a2a"
LEFT = 80
LINES = {}
for w in W:
    LINES.setdefault(w["line"], []).append(w)
L0 = {k: v[0]["t0"] for k, v in LINES.items()}
L1 = {k: v[-1]["t1"] for k, v in LINES.items()}
DUR = round(L1["s05"] + .6, 2)
JS, SFX, HTML = [], [], []


def T(line, word, n=0):
    hits = [w for w in LINES[line] if w["w"].lower().strip(".,:!?-").startswith(word.lower())]
    return hits[min(n, len(hits) - 1)]["t0"]


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def show(sel, t, d=.3, frm="{opacity: 0, y: 40}", to="{opacity: 1, y: 0}", ease="back.out(1.7)"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def hide(sel, t, d=.18):
    js(f'tl.to("{sel}", {{opacity: 0, duration: {d}, ease: "power2.in"}}, {t:.3f});')


WID = [0]
SPOKEN = {"10": "ten", "5": "five", "1": "one", "2": "two", "3": "three", "4": "four", "6": "six", "12": "twelve"}


def phrase(pid, rows, top, line, size=92, extra=""):
    """kinetic headline: rows of (text, cls) words; each word rises in on its spoken time (hook-reel style)"""
    out, spoken = [], [w for w in LINES[line]]
    k = 0
    html_rows = []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"w{WID[0]}"
            # match the word to its spoken time, in order
            t = None
            key = SPOKEN.get(word.lower().strip(".,:!?"), word.lower().strip(".,:!?"))
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?-")
                sw = SPOKEN.get(sw, sw)
                k += 1
                if sw.startswith(key.split("-")[0][:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="wm"><span class="w {cls}" id="{wid}">{word}</span></span>')
            out.append((wid, t))
        html_rows.append(f'<div class="ln">{"".join(ws)}</div>')
    HTML.append(f'<div class="ph" id="{pid}" style="top:{top}px;font-size:{size}px;{extra}">{"".join(html_rows)}</div>')
    for wid, t in out:
        js(f'tl.fromTo("#{wid}", {{opacity: 0, yPercent: 110}}, {{opacity: 1, yPercent: 0, duration: .28, ease: "power3.out", immediateRender: false}}, {t - .04:.3f});')
    return out


def scene_cut(t):
    js(f'tl.fromTo("#stage", {{scale: 1.05, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .35, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    sfx("whoosh", t - .1)


# ---- ChatGPT phone -------------------------------------------------------------------------------------------------
def phone(pid, top, scale, body, cls=""):
    HTML.append(f'<div class="phone {cls}" id="{pid}" style="top:{top}px;transform:translateX(-50%) scale({scale})">'
                '<div class="pbar"><span class="t">9:41</span><span class="isl"></span><span class="ic">&#9679;&#9679;&#9679;</span></div>'
                '<div class="ghead"><span class="hb">&#9776;</span><b>ChatGPT</b><span class="chev">&#8250;</span><span class="hb r">&#9998;</span></div>'
                f'<div class="gbody">{body}</div>'
                '<div class="ginput"><span class="plus">+</span><span class="ph2">Ask anything</span><span class="mic">&#127908;</span><span class="send">&#8593;</span></div>'
                '</div>')


PDF = '<div class="att"><div class="pdf">PDF</div><div><b>jesc105.pdf</b><span>Life Processes · PDF</span></div></div>'

# ---- S1 hook (s00): the chapter becomes a manga -------------------------------------------------------------------
S1, S2, S3, S4, S5, S6 = 0.0, L0["s01"] - .1, L0["s02"] - .1, L0["s03"] - .12, L0["s04"] - .1, L0["s05"] - .1
HTML.append('<div class="scn" id="sc1">')
phrase("p1", [[("I", ""), ("turned", ""), ("the", ""), ("hardest", "")], [("chapter", ""), ("in", ""), ("Class", ""), ("10", "")],
              [("Science", ""), ("into", ""), ("a", ""), ("manga.", "gr1")]], 190, "s00", 84)
phone("ph1", 560, .82, PDF + '<div class="ub" id="ub1">Turn this chapter into a 6-panel manga page. Each panel teaches one key idea, in order…</div>'
      '<div class="cr" id="cr1"><i></i>Creating image</div><div class="gimg" id="gi1"><img src="footage/results/1_manga.png"></div>')
HTML.append('<div class="stamp" id="one">1 PROMPT</div></div>')
show("#sc1", 0, .01, "{opacity: 0}", "{opacity: 1}", "none")
show("#ph1", .15, .5, "{opacity: 0, y: 160}", "{opacity: 1, y: 0}", "expo.out")
show("#ub1", T("s00", "chapter"), .3, "{opacity: 0, y: 30, scale: .95}", "{opacity: 1, y: 0, scale: 1}")
sfx("click", T("s00", "chapter"))
show("#cr1", T("s00", "Science") - .1, .2, "{opacity: 0}", "{opacity: 1}", "none")
t_m = T("s00", "manga")
hide("#cr1", t_m - .05, .1)
js(f'tl.fromTo("#gi1", {{opacity: 0, clipPath: "inset(0 0 100% 0)", filter: "blur(24px)"}}, {{opacity: 1, clipPath: "inset(0 0 0% 0)", filter: "blur(0px)", '
   f'duration: .9, ease: "power2.out", immediateRender: false}}, {t_m - .05:.3f});')
sfx("riser", t_m - .4)
sfx("impact", t_m)
show("#one", T("s00", "One"), .3, "{opacity: 0, scale: 2.2, rotation: -16}", "{opacity: 1, scale: 1, rotation: -6}", "expo.out")
sfx("stamp", T("s00", "One"))
hide("#sc1", S2 - .02, .08)

# ---- S2 contrast (s01): twelve pages vs six panels -----------------------------------------------------------------
lines_html = "".join(f'<i style="width:{w}%"></i>' for w in (92, 88, 95, 70, 90, 85, 93, 60, 88, 91, 76, 94, 83, 89, 64, 92, 87, 79, 90, 72))
HTML.append('<div class="scn" id="sc2">')
phrase("p2", [[("Same", ""), ("chapter.", "")]], 190, "s01", 110)
HTML.append(f'<div class="cmp l" id="cl"><div class="pg"><div class="pgt">6 &nbsp;Life Processes</div>{lines_html}</div>'
            f'<div class="pg p2"></div><div class="pg p3"></div><div class="cap"><b>12 pages</b><span id="fg">you forget by tomorrow</span></div></div>'
            '<div class="cmp r" id="cr"><img src="footage/results/1_manga.png"><div class="cap"><b class="pk">6 panels</b><span>you actually remember</span></div></div>'
            '<div class="vs" id="vs">vs</div></div>')
scene_cut(S2)
show("#sc2", S2, .01, "{opacity: 0}", "{opacity: 1}", "none")
show("#cl", T("s01", "Twelve") - .1, .4, "{opacity: 0, x: -120, rotation: -8}", "{opacity: 1, x: 0, rotation: -4}")
sfx("swish", T("s01", "Twelve") - .1)
js(f'tl.to("#cl", {{filter: "grayscale(1) blur(1.5px)", opacity: .55, duration: .5}}, {T("s01", "forget"):.3f});')
show("#vs", T("s01", "or") - .05, .25, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}")
sfx("pop", T("s01", "or"))
show("#cr", T("s01", "six") - .1, .45, "{opacity: 0, x: 140, rotation: 10}", "{opacity: 1, x: 0, rotation: 4}")
sfx("whoosh", T("s01", "six") - .15)
js(f'tl.fromTo("#cr", {{boxShadow: "0 30px 80px rgba(255,61,127,.0)"}}, {{boxShadow: "0 30px 90px rgba(255,61,127,.55)", duration: .5, yoyo: true, repeat: 1, '
   f'immediateRender: false}}, {T("s01", "remember"):.3f});')
sfx("ding", T("s01", "remember"))
hide("#sc2", S3 - .02, .08)

# ---- S3 (s02): five prompts, paste your chapter, pick one ----------------------------------------------------------
chips = "".join(f'<span class="chip" id="cp{i}">{c}</span>' for i, c in enumerate(["Manga", "Timeline", "Mind map", "Diagram", "Revision sheet"]))
HTML.append('<div class="scn" id="sc3">')
phrase("p3", [[("Here", ""), ("are", ""), ("5", "gr1"), ("prompts.", "gr1")]], 190, "s02", 96)
phone("ph3", 470, .82, f'<div class="att big" id="at3">{PDF}</div><div class="chips" id="chips">{chips}</div>')
HTML.append('<div class="cursor" id="cur3"><svg viewBox="0 0 24 24"><path d="M4 2l16 9-7 2-3 7z"/></svg></div></div>')
scene_cut(S3)
show("#sc3", S3, .01, "{opacity: 0}", "{opacity: 1}", "none")
show("#ph3", S3 + .05, .45, "{opacity: 0, y: 140}", "{opacity: 1, y: 0}", "expo.out")
show("#at3", T("s02", "Paste") - .05, .3, "{opacity: 0, y: 60, scale: .9}", "{opacity: 1, y: 0, scale: 1}")
sfx("pop", T("s02", "Paste"))
for i in range(5):
    t = T("s02", "five") + .08 * i
    show(f"#cp{i}", t, .25, "{opacity: 0, y: 30, scale: .8}", "{opacity: 1, y: 0, scale: 1}")
    sfx("tick", t)
t_pick = T("s02", "pick")
js(f'tl.fromTo("#cur3", {{opacity: 0, x: 300, y: 300}}, {{opacity: 1, x: 0, y: 0, duration: .35, ease: "power3.out", immediateRender: false}}, {t_pick - .35:.3f});')
js(f'tl.to("#cp0", {{backgroundColor: "#ff3d7f", color: "#fff", scale: 1.08, duration: .15}}, {t_pick:.3f});')
sfx("click", t_pick)
hide("#sc3", S4 - .02, .08)

# ---- S4 (s03): the five, one by one, each generated in the ChatGPT screen ------------------------------------------
ITEMS = [("Manga", "1_manga", "manga"), ("Timeline", "2_timeline", "timeline"), ("Mind map", "3_mindmap", "mind"),
         ("Labelled diagram", "4_diagram", "labeled"), ("Revision sheet", "5_revision", "revision")]
NUMW = ["One", "two", "three", "four", "five"]
lst = "".join(f'<div class="li" id="li{i}"><span class="n">{i + 1}</span>{name}</div>' for i, (name, _, _) in enumerate(ITEMS))
body = "".join(f'<div class="ub sm" id="u4{i}">{name} prompt</div><div class="gimg g4" id="g4{i}"><img src="footage/results/{img}.png"></div>'
               for i, (name, img, _) in enumerate(ITEMS))
HTML.append(f'<div class="scn" id="sc4"><div class="lst" id="lst">{lst}</div>')
phone("ph4", 600, .8, body + '<div class="cr" id="cr4"><i></i>Creating image</div>')
HTML.append('</div>')
scene_cut(S4)
show("#sc4", S4, .01, "{opacity: 0}", "{opacity: 1}", "none")
show("#lst", S4 + .02, .3, "{opacity: 0, x: -60}", "{opacity: 1, x: 0}")
show("#ph4", S4 + .05, .45, "{opacity: 0, y: 160}", "{opacity: 1, y: 0}", "expo.out")
times = [T("s03", NUMW[i]) for i in range(5)]
for i in range(5):
    t = times[i]
    t_next = times[i + 1] if i < 4 else S5
    js(f'tl.to(".li", {{color: "#b9b9b2", scale: 1, duration: .15}}, {t - .05:.3f});')
    js(f'tl.to("#li{i}", {{color: "{INK}", scale: 1.06, duration: .2, ease: "back.out(2)"}}, {t - .05:.3f});')
    js(f'tl.set("#li{i} .n", {{backgroundColor: "#ff3d7f", color: "#fff"}}, {t - .05:.3f});')
    if i:
        hide(f"#u4{i - 1}", t - .08, .08)
        hide(f"#g4{i - 1}", t - .08, .08)
    show(f"#u4{i}", t - .02, .22, "{opacity: 0, y: 30, scale: .95}", "{opacity: 1, y: 0, scale: 1}")
    show("#cr4", t + .12, .12, "{opacity: 0}", "{opacity: 1}", "none")
    hide("#cr4", t + .42, .08)
    js(f'tl.fromTo("#g4{i}", {{opacity: 0, clipPath: "inset(0 0 100% 0)", filter: "blur(20px)"}}, {{opacity: 1, clipPath: "inset(0 0 0% 0)", filter: "blur(0px)", '
       f'duration: .6, ease: "power2.out", immediateRender: false}}, {t + .45:.3f});')
    js(f'tl.fromTo("#g4{i} img", {{scale: 1.0}}, {{scale: 1.08, duration: {max(.6, t_next - t - .45):.3f}, ease: "none", immediateRender: false}}, {t + .45:.3f});')
    sfx("pop", t)
    sfx("shutter", t + .45)
hide("#sc4", S5 - .02, .08)

# ---- S5 (s04): number five, the night before the exam ---------------------------------------------------------------
HTML.append('<div class="scn" id="sc5">')
phrase("p5", [[("Number", ""), ("5", "gr1")], [("is", ""), ("the", ""), ("one", ""), ("you", ""), ("want", "")],
              [("the", ""), ("night", ""), ("before", ""), ("the", ""), ("exam.", "gr1")]], 190, "s04", 80)
HTML.append('<div class="rev" id="rev"><img src="footage/results/5_revision.png"><div class="mk" id="mk"></div></div>'
            '<div class="clock" id="clock">&#9790; 11:47 PM</div></div>')
scene_cut(S5)
show("#sc5", S5, .01, "{opacity: 0}", "{opacity: 1}", "none")
show("#rev", S5 + .05, .5, "{opacity: 0, y: 200, rotation: 6}", "{opacity: 1, y: 0, rotation: -2}", "expo.out")
js(f'tl.fromTo("#rev img", {{scale: 1}}, {{scale: 1.12, duration: {S6 - S5:.3f}, ease: "none", immediateRender: false}}, {S5:.3f});')
js(f'tl.fromTo("#mk", {{scaleX: 0}}, {{scaleX: 1, duration: .45, ease: "power2.out", immediateRender: false}}, {T("s04", "want"):.3f});')
sfx("swish", T("s04", "want"))
show("#clock", T("s04", "night"), .3, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}")
sfx("tick", T("s04", "night"))
hide("#sc5", S6 - .02, .08)

# ---- S6 CTA (s05): comment study --------------------------------------------------------------------------------------
avatars = "".join(f'<div class="cm" id="cm{i}"><i style="background:{c}"></i><b>{n}</b><span>STUDY</span></div>'
                  for i, (n, c) in enumerate([("riya.k", "#ffb3c7"), ("aarav_10", "#b2f2bb"), ("sneha.studies", "#a5d8ff"),
                                              ("kabir", "#ffd8a8"), ("ananya_p", "#d0bfff"), ("rohan.s", "#ffc9c9")]))
HTML.append('<div class="scn" id="sc6">')
phrase("p6", [[("Comment", "")], [("STUDY", "gr1 big")]], 230, "s05", 120)
HTML.append('<div class="sub" id="sub6">and I\'ll send you all 5 prompts, ready to copy.</div>'
            '<div class="cbox" id="cbox"><i></i><span id="ctx">Add a comment…</span><b id="csend">&#10148;</b></div>'
            f'<div class="cms">{avatars}</div></div>')
scene_cut(S6)
show("#sc6", S6, .01, "{opacity: 0}", "{opacity: 1}", "none")
show("#cbox", T("s05", "Comment") + .1, .3, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}")
t_ty = T("s05", "study") + .1
js(f'const ty = {{n: 0}}; tl.to(ty, {{n: 5, duration: .5, ease: "steps(5)", onUpdate: () => {{ const e = document.getElementById("ctx"); '
   f'e.textContent = "STUDY".slice(0, Math.round(ty.n)) || "Add a comment…"; e.style.color = ty.n > 0 ? "{INK}" : "#9b9ca3"; }}}}, {t_ty:.3f});')
for k in range(5):
    sfx("tick", t_ty + .1 * k)
js(f'tl.fromTo("#csend", {{scale: 1}}, {{scale: 1.3, duration: .12, yoyo: true, repeat: 1, immediateRender: false}}, {t_ty + .6:.3f});')
sfx("click", t_ty + .6)
show("#sub6", T("s05", "send") - .05, .3)
for i in range(6):
    t = t_ty + .75 + .22 * i
    js(f'tl.fromTo("#cm{i}", {{opacity: 0, y: 80, scale: .8}}, {{opacity: 1, y: 0, scale: 1, duration: .3, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    if i % 2 == 0:
        sfx("pop", t)

CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #f4f4f1; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: {INK}; background: #f4f4f1; }}
#bg {{ position: absolute; inset: 0; background: radial-gradient(120% 80% at 50% 40%, #fbfbf9 0%, #f2f2ee 60%, #e9e9e4 100%); }}
.glow {{ position: absolute; border-radius: 50%; filter: blur(110px); }}
.g1 {{ width: 900px; height: 900px; left: -380px; top: -260px; background: rgba(176,206,120,.55); }}
.g2 {{ width: 980px; height: 980px; left: 420px; top: 1160px; background: rgba(240,150,170,.5); }}
.g3 {{ width: 700px; height: 700px; left: 560px; top: 260px; background: rgba(255,190,200,.28); }}
#grain {{ position: absolute; inset: 0; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: multiply; }}
#stage {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.scn {{ position: absolute; inset: 0; opacity: 0; }}
.ph {{ position: absolute; left: {LEFT}px; right: {LEFT}px; font-weight: 800; z-index: 5; }}
.ln {{ white-space: nowrap; line-height: 1.04; letter-spacing: -.035em; }}
.wm {{ display: inline-block; overflow: hidden; vertical-align: top; padding: 0 .02em .1em; margin: 0 .2em -.1em 0; }}
.w {{ display: inline-block; opacity: 0; }}
.gr1 {{ background-image: linear-gradient(90deg, #ff2a2a, #ff3d7f 70%, #d02cff); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.w.big {{ font-size: 1.9em; letter-spacing: -.05em; line-height: .95; }}
/* ChatGPT phone, dark theme */
.phone {{ position: absolute; left: 50%; width: 900px; height: 1500px; border-radius: 80px; background: #212121; overflow: hidden; transform-origin: 50% 0;
  box-shadow: 0 0 0 14px #0d0d0d, 0 50px 120px rgba(0,0,0,.35); opacity: 0; z-index: 4; color: #ececec; }}
.pbar {{ height: 80px; display: flex; align-items: center; justify-content: space-between; padding: 0 70px; font-weight: 700; font-size: 32px; }}
.pbar .isl {{ width: 220px; height: 56px; border-radius: 40px; background: #000; }}
.pbar .ic {{ font-size: 18px; letter-spacing: 4px; }}
.ghead {{ height: 90px; display: flex; align-items: center; gap: 16px; padding: 0 40px; font-size: 36px; }}
.ghead b {{ font-weight: 700; }}
.ghead .chev {{ color: #9b9b9b; font-size: 40px; }}
.ghead .hb {{ color: #cfcfcf; font-size: 40px; }}
.ghead .r {{ margin-left: auto; }}
.gbody {{ position: absolute; left: 0; right: 0; top: 190px; bottom: 150px; padding: 20px 40px; display: flex; flex-direction: column; align-items: flex-end; gap: 22px; }}
.att {{ display: flex; align-items: center; gap: 20px; padding: 18px 24px; border-radius: 26px; background: #2f2f2f; border: 1px solid #3d3d3d; }}
.att .pdf {{ width: 66px; height: 66px; border-radius: 14px; background: #ff5a5f; color: #fff; font-weight: 800; font-size: 22px; display: flex; align-items: center; justify-content: center; }}
.att b {{ display: block; font-size: 30px; font-weight: 700; }}
.att span {{ display: block; font-size: 24px; color: #9b9b9b; }}
.att.big {{ padding: 0; background: none; border: 0; opacity: 0; }}
.ub {{ max-width: 680px; padding: 24px 30px; border-radius: 34px; background: #303030; font-size: 30px; line-height: 1.35; font-weight: 500; opacity: 0; }}
.ub.sm {{ position: absolute; right: 40px; top: 20px; }}
.cr {{ align-self: flex-start; display: flex; align-items: center; gap: 16px; font-size: 32px; font-weight: 600; color: #b4b4b4; opacity: 0;
  background: linear-gradient(90deg, #8e8e8e 0%, #fff 50%, #8e8e8e 100%); background-size: 200% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.cr i {{ width: 22px; height: 22px; border-radius: 50%; background: #ececec; display: inline-block; }}
#cr4 {{ position: absolute; left: 40px; top: 150px; }}
.gimg {{ align-self: flex-start; width: 820px; border-radius: 28px; overflow: hidden; opacity: 0; background: #fff; }}
.gimg img {{ display: block; width: 100%; transform-origin: 50% 20%; }}
.g4 {{ position: absolute; left: 40px; top: 150px; }}
.ginput {{ position: absolute; left: 30px; right: 30px; bottom: 40px; height: 96px; border-radius: 50px; background: #303030; display: flex; align-items: center; gap: 22px;
  padding: 0 18px 0 30px; font-size: 32px; color: #9b9b9b; }}
.ginput .plus {{ font-size: 44px; color: #ececec; }}
.ginput .mic {{ margin-left: auto; font-size: 30px; filter: grayscale(1); }}
.ginput .send {{ width: 66px; height: 66px; border-radius: 50%; background: #ececec; color: #212121; font-size: 36px; font-weight: 800; display: flex; align-items: center; justify-content: center; }}
.chips {{ position: absolute; left: 40px; right: 40px; bottom: 30px; display: flex; flex-wrap: wrap; gap: 16px; }}
.chip {{ padding: 18px 28px; border-radius: 999px; background: #2f2f2f; border: 1px solid #424242; font-size: 30px; font-weight: 600; color: #ececec; opacity: 0; }}
.cursor {{ position: absolute; left: 260px; top: 1330px; width: 90px; height: 90px; opacity: 0; z-index: 8; }}
.cursor svg {{ width: 100%; height: 100%; fill: #fff; stroke: {INK}; stroke-width: 1.4; filter: drop-shadow(0 6px 14px rgba(0,0,0,.4)); }}
.stamp {{ position: absolute; left: 600px; top: 470px; padding: 14px 30px; border-radius: 18px; border: 8px solid {RED}; color: {RED}; font-weight: 800; font-size: 64px;
  letter-spacing: .02em; background: rgba(255,255,255,.85); opacity: 0; z-index: 9; }}
/* S2 compare */
.cmp {{ position: absolute; top: 520px; width: 470px; opacity: 0; z-index: 4; }}
.cmp.l {{ left: 50px; }} .cmp.r {{ right: 50px; border-radius: 24px; overflow: hidden; background: #fff; box-shadow: 0 30px 80px rgba(0,0,0,.18); }}
.cmp.r img {{ display: block; width: 100%; }}
.pg {{ position: relative; height: 620px; border-radius: 18px; background: #fff; padding: 34px 30px; box-shadow: 0 20px 50px rgba(0,0,0,.15); z-index: 3; }}
.pg.p2, .pg.p3 {{ position: absolute; left: 14px; top: 14px; width: 100%; z-index: 2; }}
.pg.p3 {{ left: 28px; top: 28px; z-index: 1; }}
.pgt {{ font-weight: 800; font-size: 30px; margin-bottom: 18px; }}
.pg i {{ display: block; height: 11px; border-radius: 6px; background: #d9d9d4; margin-bottom: 15px; }}
.cap {{ margin-top: 60px; text-align: center; }}
.cmp.r .cap {{ margin: 0; padding: 26px 10px 30px; }}
.cap b {{ display: block; font-weight: 800; font-size: 56px; letter-spacing: -.03em; }}
.cap span {{ display: block; font-weight: 700; font-size: 32px; color: #66665f; margin-top: 6px; }}
.cap .pk {{ color: #ff3d7f; }}
.vs {{ position: absolute; left: 50%; top: 780px; transform: translateX(-50%); width: 130px; height: 130px; border-radius: 50%; background: {INK}; color: #fff;
  font-weight: 800; font-size: 54px; display: flex; align-items: center; justify-content: center; opacity: 0; z-index: 6; }}
/* S4 list */
.lst {{ position: absolute; left: {LEFT}px; top: 170px; opacity: 0; z-index: 5; }}
.li {{ display: flex; align-items: center; gap: 22px; font-weight: 800; font-size: 54px; letter-spacing: -.03em; color: #b9b9b2; margin-bottom: 12px; transform-origin: 0 50%; }}
.li .n {{ width: 62px; height: 62px; border-radius: 50%; background: #e4e4df; color: #66665f; font-size: 32px; display: flex; align-items: center; justify-content: center; }}
/* S5 revision */
.rev {{ position: absolute; left: 110px; top: 620px; width: 860px; height: 1146px; border-radius: 28px; overflow: hidden; background: #fff; box-shadow: 0 40px 110px rgba(0,0,0,.25); opacity: 0; z-index: 4; }}
.rev img {{ display: block; width: 100%; transform-origin: 50% 70%; }}
.mk {{ position: absolute; left: 30px; top: 616px; width: 520px; height: 44px; background: rgba(255,224,102,.65); transform-origin: left center; mix-blend-mode: multiply; }}
.clock {{ position: absolute; right: 70px; top: 540px; padding: 16px 28px; border-radius: 999px; background: {INK}; color: #fff; font-weight: 800; font-size: 40px; opacity: 0; z-index: 6; }}
/* S6 CTA */
.sub {{ position: absolute; left: {LEFT}px; right: {LEFT}px; top: 640px; font-weight: 700; font-size: 46px; line-height: 1.25; color: #3a3a35; opacity: 0; }}
.cbox {{ position: absolute; left: 70px; right: 70px; top: 820px; height: 120px; border-radius: 60px; background: rgba(255,255,255,.85); box-shadow: 0 20px 60px rgba(0,0,0,.12);
  display: flex; align-items: center; gap: 24px; padding: 0 20px 0 26px; opacity: 0; }}
.cbox i {{ width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #ff9ec0, #c9a7ff); }}
.cbox span {{ font-weight: 700; font-size: 46px; color: #9b9ca3; }}
.cbox b {{ margin-left: auto; width: 84px; height: 84px; border-radius: 50%; background: #ff3d7f; color: #fff; font-size: 40px; display: flex; align-items: center; justify-content: center; }}
.cms {{ position: absolute; left: 70px; right: 70px; top: 1010px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
.cm {{ display: flex; align-items: center; gap: 14px; padding: 16px 20px; border-radius: 26px; background: rgba(255,255,255,.8); box-shadow: 0 10px 30px rgba(0,0,0,.08); opacity: 0; }}
.cm i {{ width: 56px; height: 56px; border-radius: 50%; flex: none; }}
.cm b {{ font-size: 24px; font-weight: 700; color: #66665f; }}
.cm span {{ margin-left: auto; font-weight: 800; font-size: 32px; color: #ff3d7f; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>STUDY: chapter to manga 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg"></div><div class="glow g1" id="g1"></div><div class="glow g2" id="g2"></div><div class="glow g3" id="g3"></div>
      <div id="stage">
        {chr(10).join(HTML)}
      </div>
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.fromTo("#g1", {{x: 0, y: 0}}, {{x: 260, y: 180, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);
      tl.fromTo("#g2", {{x: 0, y: 0}}, {{x: -320, y: -260, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);
      tl.fromTo("#g3", {{x: 0, y: 0, scale: 1}}, {{x: -200, y: 300, scale: 1.3, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);
      tl.fromTo(".cr", {{backgroundPosition: "200% 0"}}, {{backgroundPosition: "-200% 0", duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);
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
json.dump({"dur": DUR, "scenes": {"hook": [S1, S2], "contrast": [S2, S3], "prompts": [S3, S4], "five": [S4, S5], "exam": [S5, S6], "cta": [S6, DUR]}},
          open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
