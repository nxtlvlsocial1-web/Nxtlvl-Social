"""Creators 100X "STUDY" reel v2 (9:16): writes index.html and plan/sfx_events.json from plan/words.json.

v2 (owner: "the video feels very dull, so less animation going on"): something moves at every moment.
  * a hand-held camera drift on the whole stage, drifting study doodles (stars, sparks, pencils, rings), glows
  * hook: the chapter is typed into the ChatGPT screen, the manga is generated, then its six panels BURST out of the
    phone and fan across the screen; "1 PROMPT" slams with a camera punch and flash
  * contrast: a stack of pages fans out with a 1-12 page counter, crumples grey under a red scribble X and falls away;
    the six panels fly in and snap into a grid with a sparkle burst and a tick stamp
  * prompts: the PDF uploads with a progress bar, the five format chips cascade in, a cursor taps one
  * the five: a giant rolling number 01-05 and a slammed label per format, each result generated on the phone and
    then thrown out of it to full size; progress dots fill
  * payoff: the revision sheet with the camera panning from section to section while highlighter boxes draw on
    each one, a ticking 11:47 PM clock
  * CTA: a keyword slot-reel rolling to STUDY with a confetti burst, the keyword typed and sent, comments flying
    in with hearts and a climbing comment counter
Look from the Creators 100X hook reel (reel-flop-9x16): off-white ground, lime/pink/peach glows, grain, black Inter 800,
red-pink gradient accents. Voice v2: Kokoro af_heart (build/vo_kokoro.py), the hook reel's approved voice.
python3 build/generate.py
"""
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
INK, RED, PINK, LIME = "#121212", "#ff2a2a", "#ff3d7f", "#b8e05a"
LEFT = 80
random.seed(7)
LINES = {}
for w in W:
    LINES.setdefault(w["line"], []).append(w)
L0 = {k: v[0]["t0"] for k, v in LINES.items()}
L1 = {k: v[-1]["t1"] for k, v in LINES.items()}
DUR = round(L1["s05"] + .7, 2)
JS, SFX, HTML = [], [], []
SPOKEN = {"10": "ten", "5": "five", "1": "one", "2": "two", "3": "three", "4": "four", "6": "six", "12": "twelve"}


def norm(s):
    s = s.lower().strip(".,:!?-")
    return SPOKEN.get(s, s)


def T(line, word, n=0):
    k = norm(word)
    hits = [w for w in LINES[line] if norm(w["w"]).startswith(k[:5])]
    return hits[min(n, len(hits) - 1)]["t0"]


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def fromto(sel, t, d, frm, to, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def setp(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


WID = [0]


def phrase(pid, rows, top, line, size=96, extra=""):
    """kinetic headline: each word pops up on its spoken time with an overshoot; ('word', cls) rows"""
    spoken = LINES[line]
    k, out, html_rows = 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"w{WID[0]}"
            key, t = norm(word), None
            while k < len(spoken):
                sw = norm(spoken[k]["w"])
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="wm"><span class="w {cls}" id="{wid}">{word}</span></span>')
            out.append((wid, t, cls))
        html_rows.append(f'<div class="ln">{"".join(ws)}</div>')
    HTML.append(f'<div class="ph" id="{pid}" style="top:{top}px;font-size:{size}px;{extra}">{"".join(html_rows)}</div>')
    for wid, t, cls in out:
        fromto(f"#{wid}", t - .05, .32, "{opacity: 0, yPercent: 120, rotation: 8, scale: .8}", "{opacity: 1, yPercent: 0, rotation: 0, scale: 1}", "back.out(2.2)")
        if "gr1" in cls:
            fromto(f"#{wid}", t + .27, .3, "{scale: 1.18}", "{scale: 1}", "elastic.out(1,.4)")
    return {wid: t for wid, t, _ in out}


def scene(sid, t0, t1, whip=1):
    """scene in with a whip-pan (blur + slide) and a gradient wipe band; scene out hard at t1"""
    fromto(f"#{sid}", t0, .01, "{opacity: 0}", "{opacity: 1}", "none")
    fromto("#stage", t0, .4, f"{{x: {160 * whip}, filter: 'blur(14px)'}}", "{x: 0, filter: 'blur(0px)'}", "expo.out")
    fromto("#wipe", t0 - .14, .32, f"{{xPercent: {-110 * whip}}}", f"{{xPercent: {110 * whip}}}", "power2.inOut")
    sfx("whoosh", t0 - .14)
    setp(f"#{sid}", t1 - .01, "{opacity: 0}")


def punch(t, amt=1.06):
    fromto("#cam", t, .45, f"{{scale: {amt}}}", "{scale: 1}", "expo.out")
    setp("#flash", t, "{opacity: .7}")
    to("#flash", t + .02, .23, "{opacity: 0}")


def burst(bid, x, y, t, n=14, colors=(PINK, LIME, "#ffb36b", "#7f1bf8"), dist=260):
    """confetti / sparkle burst from (x, y)"""
    parts = []
    for i in range(n):
        a = 2 * math.pi * i / n + random.uniform(-.2, .2)
        r = dist * random.uniform(.6, 1.1)
        c = colors[i % len(colors)]
        shape = "border-radius:50%" if i % 3 == 0 else ("transform:rotate(45deg)" if i % 3 == 1 else "border-radius:3px")
        parts.append((f"{bid}{i}", math.cos(a) * r, math.sin(a) * r, c, shape))
    HTML.append("".join(f'<i class="cf" id="{p}" style="left:{x}px;top:{y}px;background:{c};{s}"></i>' for p, _, _, c, s in parts))
    for p, dx, dy, _, _ in parts:
        fromto(f"#{p}", t, .7, "{opacity: 1, x: 0, y: 0, scale: 1.4}", f"{{opacity: 0, x: {dx:.0f}, y: {dy + 120:.0f}, scale: .4, rotation: {random.randint(-200, 200)}}}", "power2.out")


S1, S2, S3, S4, S5, S6 = 0.0, L0["s01"] - .1, L0["s02"] - .1, L0["s03"] - .14, L0["s04"] - .1, L0["s05"] - .1


def phone(pid, top, scale, body):
    HTML.append(f'<div class="phone" id="{pid}" style="top:{top}px;--s:{scale}">'
                '<div class="pbar"><span>9:41</span><span class="isl"></span><span class="ic">&#9679;&#9679;&#9679;</span></div>'
                '<div class="ghead"><span class="hb">&#9776;</span><b>ChatGPT</b><span class="chev">&#8250;</span><span class="hb r">&#9998;</span></div>'
                f'<div class="gbody">{body}</div>'
                f'<div class="ginput"><span class="plus">+</span><span class="itx" id="{pid}_in">Ask anything</span><span class="send" id="{pid}_send">&#8593;</span></div>'
                '</div>')


def typer(el, text, t, d, placeholder="Ask anything"):
    js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: {len(text)}, duration: {d:.2f}, ease: "none", onUpdate: () => {{ const e = document.getElementById("{el}"); '
       f'const k = Math.round(o.n); e.textContent = k ? {json.dumps(text)}.slice(0, k) : {json.dumps(placeholder)}; e.style.color = k ? "#ececec" : "#9b9b9b"; }}}}, {t:.3f}); }})();')


PDF = '<div class="att"><div class="pdf">PDF</div><div><b>jesc105.pdf</b><span>Life Processes · 12 pages</span></div></div>'

# ---- global: camera drift and doodles ----------------------------------------------------------------------------------
DOODLES = [("star", 70, 1480, PINK), ("ring", 900, 1580, LIME), ("spark", 930, 330, "#ffb36b"), ("star", 960, 980, "#7f1bf8"),
           ("ring", 60, 760, PINK), ("spark", 140, 1780, "#7f1bf8"), ("star", 520, 1820, LIME), ("pencil", 860, 1250, INK)]
SVG = {
    "star": '<svg viewBox="0 0 24 24"><path d="M12 1l3 8 8 .5-6.2 5 2.2 8L12 18l-7 4.5 2.2-8L1 9.5 9 9z"/></svg>',
    "ring": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke-width="4"/></svg>',
    "spark": '<svg viewBox="0 0 24 24"><path d="M12 0l2.2 9.8L24 12l-9.8 2.2L12 24l-2.2-9.8L0 12l9.8-2.2z"/></svg>',
    "pencil": '<svg viewBox="0 0 24 24"><path d="M3 21l1.5-5L16 4.5l3.5 3.5L8 19.5zM17.5 3l3.5 3.5"/></svg>',
}
dood = "".join(f'<div class="dd {k}" id="dd{i}" style="left:{x}px;top:{y}px;color:{c};fill:{c};stroke:{c}">{SVG[k]}</div>' for i, (k, x, y, c) in enumerate(DOODLES))

# ---- S1 hook -------------------------------------------------------------------------------------------------------------
HTML.append('<div class="scn" id="sc1">')
phrase("p1", [[("I", ""), ("made", ""), ("the", ""), ("hardest", "hl")], [("chapter", ""), ("in", ""), ("Class", ""), ("10", "")],
              [("Science", ""), ("into", ""), ("a", ""), ("manga.", "gr1")]], 180, "s00", 88)
HTML.append('<svg class="scrib" id="scr1" viewBox="0 0 400 40" style="left:470px;top:278px;width:330px"><path d="M5 25 C 90 8, 200 38, 395 14" /></svg>')
phone("ph1", 560, .8, PDF + '<div class="ub" id="ub1">Turn this chapter into a 6-panel manga page…</div>'
      '<div class="cr" id="cr1"><i></i>Creating image</div><div class="gimg" id="gi1"><img src="footage/results/1_manga.png"></div>')
PAN = [(-330, -30, -14), (330, -60, 12), (-360, 330, 9), (360, 300, -10), (-300, 690, -7), (330, 660, 13)]
for i in range(6):
    HTML.append(f'<div class="pan" id="pn{i}"><img src="assets/img/panels/p{i + 1}.png"></div>')
HTML.append('<div class="stamp" id="one">1 PROMPT</div></div>')
scene("sc1", S1, S2)
fromto("#ph1", .05, .7, "{opacity: 0, y: 500, rotationX: 40, scale: .7}", "{opacity: 1, y: 0, rotationX: 0, scale: 1}", "expo.out")
fromto("#ph1 .att", .45, .35, "{opacity: 0, y: -80, scale: .6}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
sfx("pop", .45)
typer("ph1_in", "Turn this chapter into a manga", .6, .7)
for k in range(6):
    sfx("tick", .6 + .12 * k)
fromto("#ph1_send", 1.35, .12, "{scale: 1}", "{scale: 1.35}", "power2.out")
to("#ph1_send", 1.47, .12, "{scale: 1}")
sfx("click", 1.35)
setp("#ph1_in", 1.4, '{textContent: "Ask anything", color: "#9b9b9b"}')
fromto("#ub1", 1.4, .3, "{opacity: 0, y: 60, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
fromto("#cr1", 1.7, .15, "{opacity: 0}", "{opacity: 1}", "none")
t_m = T("s00", "manga")
setp("#cr1", t_m - .25, "{opacity: 0}")
fromto("#gi1", t_m - .25, .55, "{opacity: 0, clipPath: 'inset(0 0 100% 0)', filter: 'blur(26px)'}", "{opacity: 1, clipPath: 'inset(0 0 0% 0)', filter: 'blur(0px)'}", "power2.out")
sfx("riser", t_m - .6)
fromto("#scr1", T("s00", "hardest") + .1, .35, "{strokeDashoffset: 500}", "{strokeDashoffset: 0}", "power2.out")
# the six panels burst out of the phone
for i, (dx, dy, rot) in enumerate(PAN):
    t = t_m + .32 + .05 * i
    fromto(f"#pn{i}", t, .55, "{opacity: 0, x: 0, y: 260, scale: .3, rotation: 0}", f"{{opacity: 1, x: {dx}, y: {dy}, scale: 1, rotation: {rot}}}", "back.out(1.6)")
    js(f'tl.to("#pn{i}", {{y: "+=24", rotation: "+={-rot / 3:.0f}", duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 1}}, {t + .55:.3f});')
sfx("impact", t_m + .32)
burst("b1", 540, 1100, t_m + .35, 18)
t_one = T("s00", "One")
fromto("#one", t_one, .3, "{opacity: 0, scale: 2.6, rotation: -20}", "{opacity: 1, scale: 1, rotation: -6}", "expo.out")
punch(t_one)
sfx("stamp", t_one)

# ---- S2 contrast ---------------------------------------------------------------------------------------------------------
HTML.append('<div class="scn" id="sc2">')
phrase("p2", [[("Same", ""), ("chapter.", "")]], 180, "s01", 120)
pg = "".join(f'<i style="width:{w}%"></i>' for w in (92, 88, 95, 70, 90, 85, 93, 60, 88, 91, 76, 94, 83, 89, 64, 92))
HTML.append('<div class="stackw" id="stk">' + "".join(f'<div class="pg" id="pg{i}"><div class="pgt">Life Processes</div>{pg}</div>' for i in range(5))
            + '<svg class="xx" id="xx" viewBox="0 0 100 100"><path d="M12 12 L88 88 M88 12 L12 88"/></svg></div>'
            '<div class="cnt l" id="cnt12"><b id="n12">1</b><span>pages</span><em id="fg">you forget by tomorrow</em></div>')
GRID = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
HTML.append('<div class="grid6" id="g6">' + "".join(f'<div class="gp" id="gp{i}" style="left:{c * 232}px;top:{r * 160}px"><img src="assets/img/panels/p{i + 1}.png"></div>' for i, (c, r) in enumerate(GRID))
            + '<div class="tick" id="tk">&#10003;</div></div>'
            '<div class="cnt r" id="cnt6"><b class="pk">6</b><span>panels</span><em>you actually remember</em></div><div class="vs" id="vs">vs</div></div>')
scene("sc2", S2, S3, -1)
t12 = T("s01", "Twelve")
for i in range(5):
    fromto(f"#pg{i}", t12 - .15 + .05 * i, .45, "{opacity: 0, x: -300, rotation: -30}", f"{{opacity: 1, x: {i * 14}, rotation: {-8 + i * 4}}}", "back.out(1.6)")
sfx("swish", t12 - .15)
js(f'(() => {{ const o = {{v: 1}}; tl.to(o, {{v: 12, duration: .5, ease: "power1.out", onUpdate: () => {{ document.getElementById("n12").textContent = Math.round(o.v); }}}}, {t12:.3f}); }})();')
fromto("#cnt12", t12, .3, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(2)")
t_fg = T("s01", "forget")
fromto("#xx", t_fg, .3, "{opacity: 1, strokeDashoffset: 300}", "{opacity: 1, strokeDashoffset: 0}", "power2.out")
sfx("buzzer", t_fg + .05)
to("#stk", t_fg + .1, .3, "{filter: 'grayscale(1)', scale: .92}")
t_tm = T("s01", "tomorrow")
for i in range(5):
    to(f"#pg{i}", t_tm + .05 * i, .6, f"{{y: 1100, rotation: {random.randint(-60, 60)}, opacity: 0}}", "power2.in")
to("#xx", t_tm, .3, "{opacity: 0}")
to("#cnt12", t_tm + .3, .3, "{opacity: .35}")
fromto("#vs", T("s01", "or") - .05, .3, "{opacity: 0, scale: .2, rotation: -90}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(2.5)")
sfx("pop", T("s01", "or"))
t6 = T("s01", "six")
for i in range(6):
    fromto(f"#gp{i}", t6 - .1 + .06 * i, .4, f"{{opacity: 0, x: {random.choice([-1, 1]) * 500}, y: {random.randint(-400, 400)}, rotation: {random.randint(-50, 50)}, scale: .5}}",
           "{opacity: 1, x: 0, y: 0, rotation: 0, scale: 1}", "back.out(1.7)")
    if i % 2 == 0:
        sfx("tick", t6 - .1 + .06 * i)
fromto("#cnt6", t6, .3, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(2)")
t_rm = T("s01", "remember")
fromto("#tk", t_rm, .35, "{opacity: 0, scale: 3, rotation: -30}", "{opacity: 1, scale: 1, rotation: 0}", "expo.out")
burst("b2", 790, 1010, t_rm + .05, 16)
sfx("ding", t_rm)
punch(t_rm, 1.04)

# ---- S3 five prompts -----------------------------------------------------------------------------------------------------
chips = "".join(f'<span class="chip" id="cp{i}">{c}</span>' for i, c in enumerate(["Manga", "Timeline", "Mind map", "Diagram", "Revision sheet"]))
HTML.append('<div class="scn" id="sc3">')
phrase("p3", [[("Here", ""), ("are", ""), ("5", "gr1 xl"), ("prompts.", "gr1")]], 160, "s02", 100)
phone("ph3", 470, .8, '<div class="att big" id="at3"><div class="pdf">PDF</div><div><b>jesc105.pdf</b><span>Uploading…</span>'
      '<div class="prog"><i id="pb3"></i></div></div></div>' + f'<div class="chips">{chips}</div>')
HTML.append('<div class="cursor" id="cur3"><svg viewBox="0 0 24 24"><path d="M4 2l16 9-7 2-3 7z"/></svg></div><div class="rip" id="rip3"></div></div>')
scene("sc3", S3, S4)
fromto("#ph3", S3 + .05, .5, "{opacity: 0, y: 300, rotation: -6}", "{opacity: 1, y: 0, rotation: 0}", "expo.out")
for i in range(5):
    t = T("s02", "five") + .07 * i
    fromto(f"#cp{i}", t, .35, "{opacity: 0, y: 120, scale: .4, rotation: -20}", "{opacity: 1, y: 0, scale: 1, rotation: 0}", "back.out(2.4)")
    sfx("tick", t)
t_p = T("s02", "Paste")
fromto("#at3", t_p - .1, .35, "{opacity: 0, y: -120, scale: .5}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
fromto("#pb3", t_p, .55, "{scaleX: 0}", "{scaleX: 1}", "power1.inOut")
sfx("pop", t_p - .1)
t_pk = T("s02", "pick")
fromto("#cur3", t_pk - .4, .4, "{opacity: 0, x: 380, y: 380}", "{opacity: 1, x: 0, y: 0}", "power3.out")
to("#cur3", t_pk, .08, "{scale: .8}")
to("#cur3", t_pk + .08, .1, "{scale: 1}")
fromto("#rip3", t_pk, .5, "{opacity: .9, scale: .2}", "{opacity: 0, scale: 2.6}", "power2.out")
to("#cp0", t_pk, .18, f"{{backgroundColor: '{PINK}', color: '#fff', scale: 1.12}}", "back.out(3)")
sfx("click", t_pk)

# ---- S4 the five ---------------------------------------------------------------------------------------------------------
ITEMS = [("MANGA", "1_manga"), ("TIMELINE", "2_timeline"), ("MIND MAP", "3_mindmap"), ("DIAGRAM", "4_diagram"), ("REVISION<br>SHEET", "5_revision")]
NUMW = ["1", "2", "3", "4", "5"]
times = [T("s03", n) for n in NUMW]
HTML.append('<div class="scn" id="sc4"><div class="bignum"><div class="reel" id="reel">' + "".join(f'<b>0{i + 1}</b>' for i in range(5)) + '</div></div>'
            + "".join(f'<div class="lab4" id="lb{i}">{name}</div>' for i, (name, _) in enumerate(ITEMS))
            + '<div class="dots">' + "".join(f'<i id="dt{i}"></i>' for i in range(5)) + '</div>')
phone("ph4", 640, .62, '<div class="cr" id="cr4"><i></i>Creating image</div>' + "".join(f'<div class="gimg g4" id="g4{i}"><img src="footage/results/{img}.png"></div>' for i, (_, img) in enumerate(ITEMS)))
HTML.append("".join(f'<div class="out" id="o4{i}"><img src="footage/results/{img}.png"></div>' for i, (_, img) in enumerate(ITEMS)) + '</div>')
scene("sc4", S4, S5)
fromto("#ph4", S4 + .02, .45, "{opacity: 0, y: 400}", "{opacity: 1, y: 0}", "expo.out")
for i in range(5):
    t = times[i]
    tn = times[i + 1] if i < 4 else S5
    to("#reel", t - .1, .35, f"{{yPercent: {-i * 20}}}", "back.out(1.4)")
    side = -1 if i % 2 == 0 else 1
    fromto(f"#lb{i}", t - .05, .35, f"{{opacity: 0, x: {side * 600}, skewX: {side * -20}}}", "{opacity: 1, x: 0, skewX: 0}", "expo.out")
    if i < 4:
        to(f"#lb{i}", tn - .12, .12, "{opacity: 0}")
    to(f"#dt{i}", t, .2, f"{{backgroundColor: '{PINK}', scale: 1.3}}", "back.out(3)")
    fromto("#cr4", t + .02, .12, "{opacity: 0}", "{opacity: 1}", "none")
    setp("#cr4", t + .3, "{opacity: 0}")
    fromto(f"#g4{i}", t + .3, .35, "{opacity: 0, clipPath: 'inset(0 0 100% 0)'}", "{opacity: 1, clipPath: 'inset(0 0 0% 0)'}", "power2.out")
    # the result is thrown out of the phone to full size, then the next one comes
    rot = random.choice([-6, -4, 4, 6])
    fromto(f"#o4{i}", t + .55, .4, "{opacity: 0, scale: .35, y: 520, rotation: 0}", f"{{opacity: 1, scale: 1, y: 0, rotation: {rot}}}", "back.out(1.5)")
    js(f'tl.to("#o4{i} img", {{scale: 1.08, duration: {max(.4, tn - t - .55):.2f}, ease: "none"}}, {t + .55:.3f});')
    setp(f"#o4{i}", tn - .08, "{opacity: 0}")
    setp(f"#g4{i}", tn - .08, "{opacity: 0}")
    sfx("pop", t)
    sfx("shutter", t + .55)
    punch(t + .55, 1.03)
fromto("#ph4", S4 + .5, S5 - S4 - .5, "{rotation: -2}", "{rotation: 2}", "sine.inOut")

# ---- S5 payoff -----------------------------------------------------------------------------------------------------------
HTML.append('<div class="scn" id="sc5">')
phrase("p5", [[("Number", ""), ("5", "gr1 xl")], [("is", ""), ("the", ""), ("one", ""), ("you", ""), ("want", "")],
              [("the", ""), ("night", ""), ("before", ""), ("the", ""), ("exam.", "gr1")]], 160, "s04", 78)
HTML.append('<div class="revw" id="revw"><div class="rev" id="rev"><img src="footage/results/5_revision.png">'
            '<svg class="box" id="bx1" viewBox="0 0 100 100" preserveAspectRatio="none" style="left:44px;top:240px;width:478px;height:330px"><rect x="2" y="2" width="96" height="96" rx="6"/></svg>'
            '<svg class="box" id="bx2" viewBox="0 0 100 100" preserveAspectRatio="none" style="left:538px;top:240px;width:500px;height:330px"><rect x="2" y="2" width="96" height="96" rx="6"/></svg>'
            '<svg class="box" id="bx3" viewBox="0 0 100 100" preserveAspectRatio="none" style="left:44px;top:830px;width:992px;height:420px"><rect x="2" y="2" width="96" height="96" rx="4"/></svg>'
            '</div></div><div class="clock" id="clock"><div class="face"><i id="hand"></i></div>11:47 PM</div></div>')
scene("sc5", S5, S6)
fromto("#revw", S5 + .05, .5, "{opacity: 0, y: 500, rotation: 10, scale: .8}", "{opacity: 1, y: 0, rotation: -2, scale: 1}", "expo.out")
sfx("whoosh_big", S5)
for bx, w, (x, y, sc) in (("#bx1", "Number", (180, 80, 1.25)), ("#bx2", "want", (-200, 80, 1.25)), ("#bx3", "night", (0, -330, 1.18))):
    t = T("s04", w)
    to("#rev", t, .5, f"{{x: {x}, y: {y}, scale: {sc}}}", "power3.inOut")
    fromto(bx, t + .2, .45, "{opacity: 1, strokeDashoffset: 420}", "{opacity: 1, strokeDashoffset: 0}", "power2.out")
    sfx("swish", t + .2)
fromto("#clock", T("s04", "night"), .35, "{opacity: 0, scale: .3, rotation: -40}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(2.5)")
fromto("#hand", T("s04", "night"), 1.2, "{rotation: 0}", "{rotation: 360}", "none")
sfx("tick", T("s04", "night"))
t_ex = T("s04", "exam")
fromto("#p5", t_ex + .1, .4, "{x: -14}", "{x: 0}", "elastic.out(1,.25)")
punch(t_ex + .1, 1.04)

# ---- S6 CTA ---------------------------------------------------------------------------------------------------------------
ROLL = ["MANGA", "NOTES", "GUIDE", "PROMPTS", "STUDY"]
avatars = "".join(f'<div class="cm" id="cm{i}"><i style="background:{c}"></i><b>{n}</b><span>STUDY</span></div>'
                  for i, (n, c) in enumerate([("riya.k", "#ffb3c7"), ("aarav_10", "#b2f2bb"), ("sneha.studies", "#a5d8ff"),
                                              ("kabir", "#ffd8a8"), ("ananya_p", "#d0bfff"), ("rohan.s", "#ffc9c9")]))
hearts = "".join(f'<div class="ht" id="ht{i}" style="left:{900 + random.randint(-40, 40)}px">&#10084;</div>' for i in range(7))
HTML.append('<div class="scn" id="sc6">')
phrase("p6", [[("Comment", "")]], 200, "s05", 110)
HTML.append('<div class="slot"><div class="sreel" id="sreel">' + "".join(f'<b class="{"gr1" if w == "STUDY" else "gry"}">{w}</b>' for w in ROLL) + '</div></div>'
            '<div class="sub" id="sub6">and I\'ll send you all <b>5 prompts</b>, ready to copy.</div>'
            '<div class="cbox" id="cbox"><i></i><span id="ctx">Add a comment…</span><b id="csend">&#10148;</b></div>'
            f'<div class="cms">{avatars}</div><div class="ccount" id="ccount"><span id="cnum">0</span> comments</div>{hearts}</div>')
scene("sc6", S6, DUR + 1)
t_st = T("s05", "STUDY")
fromto("#sreel", S6 + .05, t_st - S6 - .05, "{yPercent: 0}", f"{{yPercent: {-80}}}", "power3.inOut")
for k in range(4):
    sfx("tick", S6 + .1 + k * (t_st - S6) / 4)
fromto("#sreel", t_st, .4, "{scale: 1.25}", "{scale: 1}", "elastic.out(1,.35)")
burst("b6", 540, 520, t_st, 22, dist=380)
sfx("impact", t_st)
punch(t_st, 1.05)
fromto("#cbox", t_st + .15, .3, "{opacity: 0, y: 80}", "{opacity: 1, y: 0}", "back.out(2)")
t_ty = t_st + .35
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 5, duration: .45, ease: "steps(5)", onUpdate: () => {{ const e = document.getElementById("ctx"); '
   f'e.textContent = "STUDY".slice(0, Math.round(o.n)) || "Add a comment…"; e.style.color = o.n > 0 ? "{INK}" : "#9b9ca3"; }}}}, {t_ty:.3f}); }})();')
for k in range(5):
    sfx("tick", t_ty + .09 * k)
fromto("#csend", t_ty + .5, .12, "{scale: 1}", "{scale: 1.35}", "power2.out")
to("#csend", t_ty + .62, .12, "{scale: 1}")
sfx("click", t_ty + .5)
fromto("#sub6", T("s05", "send") - .05, .3, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
for i in range(6):
    t = t_ty + .65 + .2 * i
    fromto(f"#cm{i}", t, .35, f"{{opacity: 0, x: {-200 if i % 2 == 0 else 200}, scale: .7}}", "{opacity: 1, x: 0, scale: 1}", "back.out(2)")
    if i % 2 == 0:
        sfx("pop", t)
fromto("#ccount", t_ty + .65, .3, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 1284, duration: 1.8, ease: "power2.out", onUpdate: () => {{ document.getElementById("cnum").textContent = Math.round(o.v).toLocaleString("en-US"); }}}}, {t_ty + .65:.3f}); }})();')
for i in range(7):
    t = t_ty + .7 + .22 * i
    fromto(f"#ht{i}", t, 1.4, "{opacity: 0, y: 0, scale: .5}", f"{{opacity: 0, y: -520, scale: 1.3, x: {random.randint(-80, 80)}, keyframes: {{opacity: [0, 1, 1, 0]}}}}", "power1.out")

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
.g1 {{ width: 900px; height: 900px; left: -380px; top: -260px; background: rgba(176,206,120,.6); }}
.g2 {{ width: 980px; height: 980px; left: 420px; top: 1160px; background: rgba(240,150,170,.55); }}
.g3 {{ width: 700px; height: 700px; left: 560px; top: 260px; background: rgba(255,190,200,.32); }}
#grain {{ position: absolute; inset: 0; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: multiply; pointer-events: none; }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 40; pointer-events: none; }}
#wipe {{ position: absolute; top: 0; bottom: 0; left: 0; width: 140%; background: linear-gradient(90deg, transparent, rgba(255,61,127,.85) 30%, rgba(208,44,255,.85) 60%, transparent);
  z-index: 39; pointer-events: none; filter: blur(8px); }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#stage {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.scn {{ position: absolute; inset: 0; opacity: 0; }}
.dd {{ position: absolute; width: 70px; height: 70px; opacity: .55; z-index: 1; }}
.dd svg {{ width: 100%; height: 100%; stroke-width: 2.2; }}
.dd.ring svg, .dd.pencil svg {{ fill: none; }}
.ph {{ position: absolute; left: {LEFT}px; right: {LEFT}px; font-weight: 800; z-index: 6; }}
.ln {{ white-space: nowrap; line-height: 1.04; letter-spacing: -.035em; }}
.wm {{ display: inline-block; overflow: hidden; vertical-align: top; padding: 0 .04em .12em; margin: 0 .16em -.12em 0; }}
.w {{ display: inline-block; opacity: 0; transform-origin: 50% 90%; }}
.gr1 {{ background-image: linear-gradient(90deg, #ff2a2a, #ff3d7f 70%, #d02cff); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.w.xl {{ font-size: 1.35em; line-height: .9; }}
.w.hl {{ position: relative; }}
.scrib {{ position: absolute; height: 40px; z-index: 7; overflow: visible; }}
.scrib path {{ fill: none; stroke: {RED}; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 500; stroke-dashoffset: 500; }}
.cf {{ position: absolute; width: 22px; height: 22px; opacity: 0; z-index: 30; }}
/* ChatGPT phone */
.phone {{ position: absolute; left: 50%; width: 900px; height: 1500px; margin-left: -450px; border-radius: 80px; background: #212121; overflow: hidden;
  transform: scale(var(--s)); transform-origin: 50% 0; box-shadow: 0 0 0 14px #0d0d0d, 0 50px 120px rgba(0,0,0,.35); opacity: 0; z-index: 4; color: #ececec; }}
.pbar {{ height: 80px; display: flex; align-items: center; justify-content: space-between; padding: 0 70px; font-weight: 700; font-size: 32px; }}
.pbar .isl {{ width: 220px; height: 56px; border-radius: 40px; background: #000; }}
.pbar .ic {{ font-size: 18px; letter-spacing: 4px; }}
.ghead {{ height: 90px; display: flex; align-items: center; gap: 16px; padding: 0 40px; font-size: 36px; }}
.ghead b {{ font-weight: 700; }}
.ghead .chev, .ghead .hb {{ color: #a0a0a0; font-size: 40px; }}
.ghead .r {{ margin-left: auto; }}
.gbody {{ position: absolute; left: 0; right: 0; top: 190px; bottom: 150px; padding: 20px 40px; display: flex; flex-direction: column; align-items: flex-end; gap: 22px; }}
.att {{ display: flex; align-items: center; gap: 20px; padding: 18px 24px; border-radius: 26px; background: #2f2f2f; border: 1px solid #3d3d3d; opacity: 0; }}
.att .pdf {{ width: 66px; height: 66px; border-radius: 14px; background: #ff5a5f; color: #fff; font-weight: 800; font-size: 22px; display: flex; align-items: center; justify-content: center; flex: none; }}
.att b {{ display: block; font-size: 30px; font-weight: 700; }}
.att span {{ display: block; font-size: 24px; color: #9b9b9b; }}
.prog {{ width: 300px; height: 8px; border-radius: 4px; background: #444; margin-top: 10px; overflow: hidden; }}
.prog i {{ display: block; height: 100%; background: {PINK}; transform-origin: left; transform: scaleX(0); }}
.ub {{ max-width: 680px; padding: 24px 30px; border-radius: 34px; background: #303030; font-size: 30px; line-height: 1.35; font-weight: 500; opacity: 0; }}
.cr {{ align-self: flex-start; display: flex; align-items: center; gap: 16px; font-size: 32px; font-weight: 600; opacity: 0;
  background: linear-gradient(90deg, #8e8e8e 0%, #fff 50%, #8e8e8e 100%); background-size: 200% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.cr i {{ width: 22px; height: 22px; border-radius: 50%; background: #ececec; display: inline-block; }}
#cr4 {{ position: absolute; left: 40px; top: 40px; }}
.gimg {{ align-self: flex-start; width: 820px; border-radius: 28px; overflow: hidden; opacity: 0; background: #fff; }}
.gimg img {{ display: block; width: 100%; }}
.g4 {{ position: absolute; left: 40px; top: 30px; }}
.ginput {{ position: absolute; left: 30px; right: 30px; bottom: 40px; height: 96px; border-radius: 50px; background: #303030; display: flex; align-items: center; gap: 22px;
  padding: 0 18px 0 30px; font-size: 32px; color: #9b9b9b; }}
.ginput .plus {{ font-size: 44px; color: #ececec; }}
.ginput .itx {{ flex: 1; white-space: nowrap; overflow: hidden; }}
.ginput .send {{ width: 66px; height: 66px; border-radius: 50%; background: #ececec; color: #212121; font-size: 36px; font-weight: 800; display: flex; align-items: center; justify-content: center; }}
.chips {{ position: absolute; left: 40px; right: 40px; bottom: 30px; display: flex; flex-wrap: wrap; gap: 16px; }}
.chip {{ padding: 20px 30px; border-radius: 999px; background: #2f2f2f; border: 1px solid #424242; font-size: 32px; font-weight: 700; color: #ececec; opacity: 0; }}
.cursor {{ position: absolute; left: 230px; top: 1290px; width: 96px; height: 96px; opacity: 0; z-index: 8; }}
.cursor svg {{ width: 100%; height: 100%; fill: #fff; stroke: {INK}; stroke-width: 1.4; filter: drop-shadow(0 6px 14px rgba(0,0,0,.4)); }}
.rip {{ position: absolute; left: 190px; top: 1255px; width: 110px; height: 110px; border-radius: 50%; border: 6px solid {PINK}; opacity: 0; z-index: 7; }}
.pan {{ position: absolute; left: 360px; top: 980px; width: 380px; border-radius: 16px; overflow: hidden; background: #fff; box-shadow: 0 0 0 5px #fff, 0 24px 60px rgba(0,0,0,.3); opacity: 0; z-index: 8; }}
.pan img {{ display: block; width: 100%; }}
.stamp {{ position: absolute; left: 540px; top: 820px; padding: 16px 34px; border-radius: 20px; border: 9px solid {RED}; color: {RED}; font-weight: 800; font-size: 76px;
  background: rgba(255,255,255,.92); opacity: 0; z-index: 12; white-space: nowrap; }}
/* S2 */
.stackw {{ position: absolute; left: 60px; top: 470px; width: 440px; height: 560px; z-index: 4; }}
.pg {{ position: absolute; left: 0; top: 0; width: 420px; height: 560px; border-radius: 18px; background: #fff; padding: 30px 26px; box-shadow: 0 18px 44px rgba(0,0,0,.16); opacity: 0; }}
.pgt {{ font-weight: 800; font-size: 28px; margin-bottom: 16px; }}
.pg i {{ display: block; height: 11px; border-radius: 6px; background: #d9d9d4; margin-bottom: 14px; }}
.xx {{ position: absolute; left: 40px; top: 60px; width: 360px; height: 360px; opacity: 0; z-index: 9; overflow: visible; }}
.xx path {{ fill: none; stroke: {RED}; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 300; stroke-dashoffset: 300; }}
.cnt {{ position: absolute; top: 1080px; width: 460px; text-align: center; opacity: 0; z-index: 5; }}
.cnt.l {{ left: 50px; }} .cnt.r {{ right: 50px; }}
.cnt b {{ display: block; font-weight: 800; font-size: 150px; letter-spacing: -.05em; line-height: 1; }}
.cnt .pk {{ color: {PINK}; }}
.cnt span {{ display: block; font-weight: 800; font-size: 50px; }}
.cnt em {{ display: block; font-style: normal; font-weight: 700; font-size: 32px; color: #66665f; margin-top: 8px; }}
.grid6 {{ position: absolute; right: 60px; top: 500px; width: 456px; height: 476px; z-index: 4; }}
.gp {{ position: absolute; width: 224px; height: 152px; border-radius: 12px; overflow: hidden; background: #fff; box-shadow: 0 0 0 4px #fff, 0 12px 30px rgba(0,0,0,.2); opacity: 0; }}
.gp img {{ width: 100%; height: 100%; object-fit: cover; }}
.tick {{ position: absolute; right: -24px; bottom: -40px; width: 130px; height: 130px; border-radius: 50%; background: #2fbf71; color: #fff; font-size: 80px; font-weight: 800;
  display: flex; align-items: center; justify-content: center; box-shadow: 0 14px 40px rgba(47,191,113,.5); opacity: 0; }}
.vs {{ position: absolute; left: 50%; top: 690px; margin-left: -70px; width: 140px; height: 140px; border-radius: 50%; background: {INK}; color: #fff;
  font-weight: 800; font-size: 58px; display: flex; align-items: center; justify-content: center; opacity: 0; z-index: 6; }}
/* S4 */
.bignum {{ position: absolute; right: 70px; top: 150px; height: 300px; overflow: hidden; z-index: 6; }}
.reel {{ display: flex; flex-direction: column; }}
.reel b {{ display: block; height: 300px; font-weight: 800; font-size: 290px; line-height: 300px; letter-spacing: -.06em;
  background-image: linear-gradient(180deg, #ff2a2a, #ff3d7f 60%, #d02cff); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.lab4 {{ position: absolute; left: {LEFT}px; top: 330px; font-weight: 800; font-size: 96px; line-height: .95; letter-spacing: -.04em; opacity: 0; z-index: 7; white-space: nowrap; }}
.dots {{ position: absolute; left: {LEFT}px; top: 470px; display: flex; gap: 16px; z-index: 6; }}
.dots i {{ width: 26px; height: 26px; border-radius: 50%; background: #d9d9d4; }}
.out {{ position: absolute; left: 120px; top: 560px; width: 840px; border-radius: 26px; overflow: hidden; background: #fff; box-shadow: 0 0 0 6px #fff, 0 40px 110px rgba(0,0,0,.3);
  opacity: 0; z-index: 9; }}
.out img {{ display: block; width: 100%; transform-origin: 50% 30%; }}
/* S5 */
.revw {{ position: absolute; left: 90px; top: 560px; width: 900px; height: 1200px; border-radius: 28px; overflow: hidden; background: #fff; box-shadow: 0 40px 110px rgba(0,0,0,.25); opacity: 0; z-index: 4; }}
.rev {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1440px; transform-origin: 50% 40%; transform: scale(.833); margin-left: -90px; margin-top: -120px; }}
.rev img {{ display: block; width: 100%; }}
.box {{ position: absolute; overflow: visible; opacity: 0; }}
.box rect {{ fill: rgba(255,224,102,.18); stroke: {PINK}; stroke-width: 1.4; vector-effect: non-scaling-stroke; stroke-dasharray: 420; stroke-dashoffset: 420; }}
.box rect {{ stroke-width: 7px; }}
.clock {{ position: absolute; right: 70px; top: 470px; display: flex; align-items: center; gap: 16px; padding: 14px 28px 14px 16px; border-radius: 999px; background: {INK}; color: #fff;
  font-weight: 800; font-size: 44px; opacity: 0; z-index: 8; }}
.clock .face {{ position: relative; width: 60px; height: 60px; border-radius: 50%; border: 5px solid #fff; }}
.clock .face i {{ position: absolute; left: 50%; top: 8px; width: 5px; height: 21px; margin-left: -2.5px; background: {LIME}; border-radius: 3px; transform-origin: 50% 100%; }}
/* S6 */
.slot {{ position: absolute; left: {LEFT}px; top: 330px; height: 240px; overflow: hidden; z-index: 6; }}
.sreel {{ display: flex; flex-direction: column; transform-origin: 0 50%; }}
.sreel b {{ display: block; height: 240px; font-weight: 800; font-size: 220px; line-height: 240px; letter-spacing: -.05em; }}
.sreel .gry {{ color: #c9c9c2; }}
.sub {{ position: absolute; left: {LEFT}px; right: {LEFT}px; top: 610px; font-weight: 700; font-size: 48px; line-height: 1.25; color: #3a3a35; opacity: 0; }}
.sub b {{ color: {PINK}; }}
.cbox {{ position: absolute; left: 70px; right: 70px; top: 800px; height: 124px; border-radius: 62px; background: rgba(255,255,255,.9); box-shadow: 0 20px 60px rgba(0,0,0,.12);
  display: flex; align-items: center; gap: 24px; padding: 0 20px 0 26px; opacity: 0; }}
.cbox i {{ width: 74px; height: 74px; border-radius: 50%; background: linear-gradient(135deg, #ff9ec0, #c9a7ff); }}
.cbox span {{ font-weight: 800; font-size: 50px; color: #9b9ca3; }}
.cbox b {{ margin-left: auto; width: 88px; height: 88px; border-radius: 50%; background: {PINK}; color: #fff; font-size: 42px; display: flex; align-items: center; justify-content: center; }}
.cms {{ position: absolute; left: 70px; right: 70px; top: 990px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
.cm {{ display: flex; align-items: center; gap: 14px; padding: 18px 20px; border-radius: 26px; background: rgba(255,255,255,.85); box-shadow: 0 10px 30px rgba(0,0,0,.08); opacity: 0; }}
.cm i {{ width: 58px; height: 58px; border-radius: 50%; flex: none; }}
.cm b {{ font-size: 25px; font-weight: 700; color: #66665f; }}
.cm span {{ margin-left: auto; font-weight: 800; font-size: 34px; color: {PINK}; }}
.ccount {{ position: absolute; right: 70px; top: 1330px; padding: 12px 24px; border-radius: 999px; background: {INK}; color: #fff; font-weight: 800; font-size: 34px; opacity: 0; }}
.ht {{ position: absolute; top: 1300px; font-size: 64px; color: {PINK}; opacity: 0; z-index: 9; }}
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
      <div id="cam"><div id="drift">{dood}<div id="stage">
        {chr(10).join(HTML)}
      </div></div></div>
      <div id="wipe"></div><div id="flash"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set("#wipe", {{xPercent: -110}}, 0);
      tl.fromTo("#g1", {{x: 0, y: 0}}, {{x: 300, y: 220, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);
      tl.fromTo("#g2", {{x: 0, y: 0}}, {{x: -360, y: -300, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);
      tl.fromTo("#g3", {{x: 0, y: 0, scale: 1}}, {{x: -240, y: 360, scale: 1.35, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);
      tl.fromTo("#drift", {{rotation: -.6, scale: 1, x: -8}}, {{rotation: .6, scale: 1.03, x: 8, duration: {DUR / 4:.2f}, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, 0);
      tl.fromTo(".dd", {{rotation: 0, y: 0}}, {{rotation: 200, y: -60, duration: {DUR:.2f}, ease: "none", stagger: .3, immediateRender: false}}, 0);
      tl.fromTo(".cr", {{backgroundPosition: "200% 0"}}, {{backgroundPosition: "-200% 0", duration: 1.2, ease: "none", repeat: {int(DUR / 1.2)}, immediateRender: false}}, 0);
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
