"""Fable 5.2 week reel (AI.NXTLVL, 9:16): writes index.html and plan/sfx_events.json from plan/words.json.

Owner: "recreate this with better visuals and script" (reference: an illustrated fox reel about Fable 5.2's launch
week). Our version: the approved script (accurate: Fable 5.2 costs nothing extra on Claude Pro until Mon 16 Nov,
11:59 pm PT, then usage credits), AI.NXTLVL's look (night #07050f, violet glows in opposite corners, dark glass panels,
Montserrat 800 + Instrument Serif Italic accents + JetBrains Mono labels), and real-looking examples of the three
builds instead of illustrations: an original low-poly 3D owl that builds itself (Three.js, assets/js/twin.js), the
hard questions and a 12-month 2027 board, and a SKILL.md that a cheaper model picks up. Cuts on the music's half-beat
grid ("Monotony" by Spencer Newton, 117.5 bpm, from 18.548 s), whips, punch-ins, light streaks.
python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
NIGHT, DEEP, VIO, ELEC, STAR, LAV = "#07050f", "#10022c", "#7f1bf8", "#6008f2", "#7a2ffb", "#b687f9"
GOLD, RED = "#ffb547", "#ff4d6d"
LINES = {}
for w in W:
    LINES.setdefault(w["line"], []).append(w)
L0 = {k: v[0]["t0"] for k, v in LINES.items()}
L1 = {k: v[-1]["t1"] for k, v in LINES.items()}
DUR = round(L1["f05"] + 1.0, 2)
JS, SFX, HTML = [], [], []
BEAT = 60 / 117.45
HB = BEAT / 2


def snap(t):
    return round(t / HB) * HB


def T(line, word, n=0):
    k = word.lower()
    hits = [w for w in LINES[line] if w["w"].lower().strip(".,:!?'").startswith(k)]
    return hits[min(n, len(hits) - 1)]["t0"]


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0, t), 3)})


def ft(sel, t, d, frm, to, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


WID = [0]


def head(hid, rows, top, line, size=86, after=0.0):
    """headline, centred: every word blurs into focus on its spoken time; ('word', cls) with cls '' / 'it' / 'it red'"""
    spoken, k, out, rws = [w for w in LINES[line] if w["t0"] >= after], 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?'"), None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?'")
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="hw {cls}" id="{wid}">{word}</span>')
            out.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTML.append(f'<div class="head" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .06, .4, "{opacity: 0, filter: 'blur(12px)', y: 24}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")


def head_out(hid, t):
    to(f"#{hid}", t, .22, "{opacity: 0, filter: 'blur(14px)', y: -36}", "power2.in")


def streak(t):
    for i in range(3):
        ft(f"#stk{i}", t - .14 + .05 * i, .36, "{xPercent: -260, opacity: 1}", "{xPercent: 260, opacity: 1}", "power2.inOut")


def whip(t, d=1):
    ft("#cam", t - .15, .15, "{x: 0, filter: 'blur(0px)'}", f"{{x: {-440 * d}, filter: 'blur(22px)'}}", "power2.in")
    ft("#cam", t, .24, f"{{x: {440 * d}, filter: 'blur(22px)'}}", "{x: 0, filter: 'blur(0px)'}", "power3.out")
    streak(t)
    sfx("riser_short", t - .9)
    sfx("whoosh", t - .16)


def zoom(t):
    ft("#cam", t - .18, .2, "{scale: 1, filter: 'blur(0px)'}", "{scale: 1.55, filter: 'blur(14px)'}", "power2.in")
    ft("#cam", t + .02, .34, "{scale: .84, filter: 'blur(14px)'}", "{scale: 1, filter: 'blur(0px)'}", "expo.out")
    streak(t)
    sfx("riser", t - .8)
    sfx("whoosh_big", t - .15)


def punch(t, k=1.05):
    ft("#punch", t - .03, .08, "{scale: 1}", f"{{scale: {k}}}", "power2.out")
    to("#punch", t + .05, .4, "{scale: 1}", "power3.out")
    st("#flash", t - .03, "{opacity: .3}")
    to("#flash", t - .02, .3, "{opacity: 0}", "power2.out")
    sfx("thump", t - .02)


def scene(sid, t0, t1):
    st(f"#{sid}", t0, "{opacity: 1}")
    st(f"#{sid}", t1, "{opacity: 0}")
    ft("#drift", t0, t1 - t0, "{scale: 1}", "{scale: 1.03}", "none")


SH = '<i class="sh"></i>'


def shine(sel, t, d=.8):
    ft(f"{sel} > .sh", t, d, "{xPercent: -160, opacity: 1}", "{xPercent: 420, opacity: 1}", "power2.inOut")


def pop(sel, t, d=.4, y=40):
    ft(sel, t, d, f"{{opacity: 0, y: {y}, scale: .9, filter: 'blur(8px)'}}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)'}", "back.out(1.6)")


SA = 0.0
SB, SC, SD, SE, SF = (snap(L0[k] - .1) for k in ("f01", "f02", "f03", "f04", "f05"))

# ---- A hook: the meter that flips from "$0 extra" to paid credits ------------------------------------------------------------
HTML.append('<div class="scn" id="sa">')
head("ha", [[("Fable", ""), ("5.2", "it")], [("costs", ""), ("nothing", ""), ("extra", "")], [("until", ""), ("Monday.", "it")]], 220, "f00", 92)
HTML.append(f'<div class="meter glass" id="meter">{SH}<div class="mlab"><b>CLAUDE PRO</b><span>FABLE 5.2</span></div>'
            '<div class="mval"><span id="m0">$0</span><em id="m0e">extra</em></div>'
            '<div class="mbar"><i id="mfill"></i></div>'
            '<div class="mend"><span>ENDS</span><b>MON 16 NOV · 11:59 PM PT</b></div>'
            '<div class="paid" id="paid">PAID CREDITS</div></div>'
            f'<div class="pick glass" id="pick">{SH}<div class="pkh">MODEL</div>'
            '<div class="po on" id="po0"><b>Fable 5.2</b><span id="poz">included until Mon</span><i>&#10003;</i></div>'
            '<div class="po"><b>Opus 5.5</b></div><div class="po"><b>Sonnet 5.5</b></div></div></div>')
scene("sa", SA, SB)
ft("#meter", 0, .55, "{opacity: 1, y: 160, rotationX: 18, scale: .92}", "{opacity: 1, y: 0, rotationX: 0, scale: 1}", "expo.out")
streak(.08)
sfx("impact", 0)
shine("#meter", .45)
t_fb = T("f00", "fable")
ft("#pick", t_fb - .05, .45, "{opacity: 0, y: 80, scale: .94}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.6)")
shine("#pick", t_fb + .35, .7)
sfx("click", t_fb + .1)
ft("#mfill", .2, 1.6, "{scaleX: .08}", "{scaleX: 1}", "power2.out")
t_mon = T("f00", "monday")
punch(t_mon)
t_paid = T("f00", "paid")
to("#mfill", t_paid - .1, .45, f"{{background: '{RED}', scaleX: .18}}", "power3.in")
ft("#paid", t_paid - .05, .35, "{opacity: 0, scale: 1.8, rotation: -14}", "{opacity: 1, scale: 1, rotation: -6}", "back.out(1.8)")
to("#m0", t_paid - .05, .2, "{opacity: .25}")
to("#m0e", t_paid - .05, .2, "{opacity: .25}")
sfx("stamp", t_paid)
st("#poz", t_paid, '{textContent: "now uses paid credits"}')
to("#po0", t_paid, .25, f"{{borderColor: '{RED}', background: 'rgba(255,77,109,.14)'}}")
js(f'tl.fromTo("#meter", {{x: 0}}, {{keyframes: [{{x: -14, duration: .05}}, {{x: 12, duration: .05}}, {{x: -8, duration: .05}}, {{x: 0, duration: .05}}], immediateRender: false}}, {t_paid:.3f});')
head_out("ha", SB - .25)

# ---- B don't burn it on emails, build these three --------------------------------------------------------------------------
MAILS = [("Re: Q4 numbers", "Can you rewrite this so it sounds..."), ("Follow-up", "Just circling back on..."), ("Quick question", "Could you make this email...")]
mails = "".join(f'<div class="mail glass" id="ml{i}">{SH}<i></i><div><b>{a}</b><span>{b}</span></div><u id="mx{i}"></u></div>' for i, (a, b) in enumerate(MAILS))
TILES = [("01", "3D twin"), ("02", "Your 2027"), ("03", "Skill file")]
tiles = "".join(f'<div class="tile glass" id="tl{i}">{SH}<em>{n}</em><b>{t}</b></div>' for i, (n, t) in enumerate(TILES))
HTML.append(f'<div class="scn" id="sb"><div class="mails">{mails}</div><div class="tiles">{tiles}</div>')
head("hb", [[("Don't", ""), ("burn", ""), ("the", ""), ("week", "")], [("on", ""), ("emails.", "it")]], 220, "f01", 88)
head("hb2", [[("Build", ""), ("these", ""), ("three.", "it")]], 240, "f01", 104, after=T("f01", "build") - .05)
HTML.append('</div>')
scene("sb", SB, SC)
whip(SB)
for i in range(3):
    pop(f"#ml{i}", SB + .05 + .1 * i, .4, 60)
t_em = T("f01", "emails")
for i in range(3):
    ft(f"#mx{i}", t_em + .05 * i, .25, "{scaleX: 0}", "{scaleX: 1}", "power3.out")
    to(f"#ml{i}", t_em + .35 + .06 * i, .3, f"{{x: {(-900, 900, -900)[i]}, opacity: 0, rotation: {(-8, 8, -6)[i]}}}", "power3.in")
sfx("scratch", t_em)
sfx("swish", t_em + .35)
t_bu = T("f01", "build")
head_out("hb", t_bu - .2)
for i in range(3):
    ft(f"#tl{i}", t_bu + .1 + .12 * i, .45, "{opacity: 0, y: 120, rotationX: 40, scale: .8}", "{opacity: 1, y: 0, rotationX: 0, scale: 1}", "back.out(1.7)")
    shine(f"#tl{i}", t_bu + .4 + .12 * i, .6)
    sfx("pop", t_bu + .1 + .12 * i)
punch(T("f01", "three"))

# ---- C one: your 3D twin ------------------------------------------------------------------------------------------------------
QS = ["Night owl or early bird?", "Calm or chaos?", "Lead or support?", "City or forest?", "Fast or careful?"]
qs = "".join(f'<div class="q glass" id="q{i}" style="{("left:60px" if i % 2 == 0 else "right:60px")};top:{560 + 150 * i}px">{SH}<i>&#10003;</i>{s}</div>'
             for i, s in enumerate(QS))
HTML.append(f'<div class="scn" id="sc"><div class="num">01</div><div class="tag glass">EXAMPLE OUTPUT</div>{qs}</div>')
head("hc", [[("Your", ""), ("3D", "it"), ("twin.", "it")]], 220, "f02", 104)
scene("sc", SC, SD)
zoom(SC)
t_an = T("f02", "answer")
for i in range(5):
    t = t_an + .25 * i
    ft(f"#q{i}", t, .35, f"{{opacity: 0, x: {(-120, 120)[i % 2]}, filter: 'blur(8px)'}}", "{opacity: 1, x: 0, filter: 'blur(0px)'}", "back.out(1.6)")
    sfx("tick", t + .1)
t_codes = T("f02", "codes")
for i in range(5):
    to(f"#q{i}", t_codes + .1 + .05 * i, .35, f"{{opacity: .0, scale: .6, x: {(260, -260)[i % 2]}, y: {(1100 - (560 + 150 * i)) * .35:.0f}}}", "power2.in")
TWIN = [SC + .05, t_codes - .1, t_codes + 1.3, SD + .05]
sfx("riser_short", t_codes - .6)
sfx("success", t_codes + 1.3)
punch(T("f02", "built"))
head_out("hc", SD - .25)

# ---- D two: your 2027 ---------------------------------------------------------------------------------------------------------
QQ = ["What are you pretending not to know?", "What would you quit if nobody was watching?", "What does a great December 2027 look like?"]
bub = "".join(f'<div class="bub glass" id="bq{i}">{SH}<em>FABLE</em>{s}</div>' for i, s in enumerate(QQ))
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
GOALS = ["Pick one goal", "Daily habit", "First 30 days", "Cut 1 thing", "Ship v1", "Review", "Level up", "Learn 1 skill", "Build", "Test it", "Prepare", "Celebrate"]
cells = "".join(f'<div class="mo glass" id="mo{i}"><b>{m}</b><span>{g}</span></div>' for i, (m, g) in enumerate(zip(MONTHS, GOALS)))
HTML.append(f'<div class="scn" id="sd"><div class="num">02</div><div class="bubs">{bub}</div><div class="board"><div class="btitle">2027 · <em>month by month</em></div>{cells}</div></div>')
head("hd", [[("Your", ""), ("2027.", "it")]], 220, "f03", 110)
scene("sd", SD, SE)
whip(SD, -1)
t_asks = T("f03", "asks")
for i in range(3):
    t = t_asks + .45 * i
    ft(f"#bq{i}", t, .4, "{opacity: 0, y: 60, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.7)")
    sfx("notify", t)
t_turns = T("f03", "turns")
for i in range(3):
    to(f"#bq{i}", t_turns - .15, .3, "{opacity: 0, y: -60, filter: 'blur(10px)'}", "power2.in")
ft(".board", t_turns, .4, "{opacity: 0, y: 80}", "{opacity: 1, y: 0}", "expo.out")
for i in range(12):
    t = t_turns + .25 + .11 * i
    ft(f"#mo{i}", t, .35, "{opacity: 0, scale: .6, rotationY: 70}", "{opacity: 1, scale: 1, rotationY: 0}", "back.out(1.8)")
    if i % 3 == 0:
        sfx("pop", t)
punch(T("f03", "month"))
head_out("hd", SE - .25)

# ---- E three: the one that lasts (SKILL.md) -------------------------------------------------------------------------------------
CODE = ["---", "name: think-like-fable", "description: How Fable plans, checks and writes.", "  Use it on every task.", "---",
        "1. Restate the goal in one line.", "2. List what could go wrong first.", "3. Draft, then critique the draft.", "4. Ship the shortest version that works."]
code = "".join(f'<div class="cl" id="cl{i}"><i>{i + 1}</i><span>{c}</span></div>' for i, c in enumerate(CODE))
HTML.append(f'<div class="scn" id="se"><div class="num">03</div><div class="ed glass" id="ed">{SH}<div class="edt"><i></i><i></i><i></i><b>SKILL.md</b></div>{code}</div>'
            '<div class="models"><div class="mdl glass" id="md0">Sonnet 5.5</div><div class="mdl glass" id="md1">Opus 5.5</div></div>'
            '<div class="link" id="lnk"></div><div class="after glass" id="aft"><i>&#10003;</i>Still works after Monday</div></div>')
head("he", [[("The", ""), ("one", ""), ("that", "")], [("lasts.", "it")]], 220, "f04", 100)
scene("se", SE, SF)
zoom(SE)
ft("#ed", SE + .05, .5, "{opacity: 0, y: 120, rotationX: 30}", "{opacity: 1, y: 0, rotationX: 0}", "expo.out")
shine("#ed", SE + .5, 1.0)
t_wr = T("f04", "write")
for i in range(len(CODE)):
    t = t_wr + .18 * i
    ft(f"#cl{i}", t, .2, "{opacity: 0, x: -30}", "{opacity: 1, x: 0}", "power2.out")
    if i % 2 == 0:
        sfx("tick", t)
t_ch = T("f04", "cheaper")
for i in range(2):
    pop(f"#md{i}", t_ch + .12 * i, .4, 50)
ft("#lnk", t_ch + .3, .5, "{scaleY: 0}", "{scaleY: 1}", "power3.out")
sfx("swish", t_ch)
t_af = T("f04", "after")
pop("#aft", t_af, .45, 40)
sfx("success", t_af + .1)
punch(t_af + .05)
head_out("he", SF - .25)

# ---- F CTA ---------------------------------------------------------------------------------------------------------------------
HTML.append('<div class="scn" id="sf"><div class="cm" id="cmh">Comment</div><div class="kw" id="kw">FABLE</div>'
            f'<div class="cbox glass" id="cbox">{SH}<i></i><span id="ctx">Add a comment…</span><b id="csend">&#10148;</b></div>'
            f'<div class="pdf glass" id="pdf">{SH}<div class="pk">FREE GUIDE</div><div class="pt">The Fable Week<br><em>Prompts</em></div>'
            '<div class="pl"><span>3D twin</span><span>2027 plan</span><span>Skill file</span></div></div></div>')
scene("sf", SF, DUR + 1)
whip(SF)
t_c = T("f05", "comment")
ft("#cmh", t_c - .05, .4, "{opacity: 0, filter: 'blur(12px)', y: 26}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
t_k = T("f05", "fable")
ft("#kw", t_k - .08, .6, "{opacity: 0, scale: 1.6, scaleX: 1.9, filter: 'blur(22px)'}", "{opacity: 1, scale: 1, scaleX: 1, filter: 'blur(0px)'}", "expo.out")
sfx("impact", t_k)
punch(t_k, 1.07)
ft("#cbox", t_k + .25, .4, "{opacity: 0, y: 50, filter: 'blur(8px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "expo.out")
t_ty = t_k + .45
js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: 5, duration: .4, ease: "steps(5)", onUpdate: () => {{ const e = document.getElementById("ctx"); '
   f'e.textContent = "FABLE".slice(0, Math.round(o.n)) || "Add a comment…"; e.style.color = o.n > 0 ? "#fff" : "rgba(255,255,255,.5)"; }}}}, {t_ty:.3f}); }})();')
for k in range(5):
    sfx("tick", t_ty + .08 * k)
to("#csend", t_ty + .45, .1, "{scale: 1.3}")
to("#csend", t_ty + .55, .15, "{scale: 1}")
sfx("click", t_ty + .45)
t_se = T("f05", "send")
ft("#pdf", t_se - .1, .6, "{opacity: 0, y: 260, rotation: 6, scale: .85}", "{opacity: 1, y: 0, rotation: -3, scale: 1}", "back.out(1.5)")
shine("#pdf", t_se + .4, .8)
sfx("swish", t_se - .1)

# ---- the 3D twin canvas (scene C) -------------------------------------------------------------------------------------------------
# the canvas exists only in its own scene (HyperFrames hides a clip outside its window; a style set from the module
# was not enough, so the owl stayed on screen over the later scenes)
TW = (f'<canvas id="twin" class="clip" width="1080" height="1080" data-start="{TWIN[0]:.3f}" data-duration="{TWIN[3] - TWIN[0]:.3f}" '
      'data-track-index="3"></canvas>')

# ---- background glows -------------------------------------------------------------------------------------------------------------
for i, (x, y, s, c) in enumerate([(-260, -220, 900, VIO), (560, 1260, 960, ELEC), (380, 520, 600, STAR)]):
    js(f'tl.fromTo("#gl{i}", {{x: 0, y: 0, scale: 1}}, {{x: {(-120, 140, 160)[i]}, y: {(160, -140, 120)[i]}, scale: {(1.2, .85, 1.25)[i]}, duration: {DUR / 3:.2f}, '
       f'ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false}}, 0);')
glows = "".join(f'<i class="glw" id="gl{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>'
                for i, (x, y, s, c) in enumerate([(-260, -220, 900, VIO), (560, 1260, 960, ELEC), (380, 520, 600, STAR)]))

CSS = f"""
@font-face {{ font-family: M; src: url("assets/fonts/montserrat.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: S; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: J; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: M; color: #fff; background: {NIGHT}; }}
.glw {{ position: absolute; border-radius: 50%; filter: blur(120px); opacity: .55; }}
#gridbg {{ position: absolute; inset: 0; opacity: .07; background-image: linear-gradient(rgba(182,135,249,.6) 1px, transparent 1px), linear-gradient(90deg, rgba(182,135,249,.6) 1px, transparent 1px);
  background-size: 90px 90px; mask-image: radial-gradient(70% 60% at 50% 50%, #000, transparent); -webkit-mask-image: radial-gradient(70% 60% at 50% 50%, #000, transparent); }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 46%; }}
#punch {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#drift {{ position: absolute; inset: 0; perspective: 1600px; }}
.scn {{ position: absolute; inset: 0; opacity: 0; perspective: 1600px; }}
#flash {{ position: absolute; inset: 0; z-index: 48; pointer-events: none; opacity: 0; background: rgba(214,190,255,.9); mix-blend-mode: soft-light; }}
.stk {{ position: absolute; left: 0; width: 60%; height: 10px; z-index: 51; pointer-events: none; opacity: 0; border-radius: 10px;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.95) 50%, rgba(255,255,255,0)); box-shadow: 0 0 30px 6px rgba(160,100,255,.6); }}
#stk0 {{ top: 520px; }} #stk1 {{ top: 960px; height: 16px; }} #stk2 {{ top: 1400px; height: 6px; }}
#grain {{ position: absolute; inset: 0; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: overlay; pointer-events: none; z-index: 60; }}
.brandbar {{ position: absolute; left: 60px; top: 90px; z-index: 40; display: flex; align-items: center; gap: 14px; font-family: J; font-size: 24px; letter-spacing: .12em; color: {LAV}; }}
.brandbar img {{ height: 40px; }}
/* glass */
.glass {{ background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.03)); border: 1.5px solid rgba(255,255,255,.2);
  backdrop-filter: blur(22px) saturate(1.5); -webkit-backdrop-filter: blur(22px) saturate(1.5);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,.3), 0 30px 90px rgba(0,0,0,.55); overflow: hidden; }}
.sh {{ position: absolute; top: -30%; bottom: -30%; left: 0; width: 30%; pointer-events: none; opacity: 0; z-index: 5;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.22) 50%, rgba(255,255,255,0)); }}
/* headlines */
.head {{ position: absolute; left: 50px; right: 50px; font-weight: 800; letter-spacing: -.035em; line-height: 1.04; z-index: 20; text-align: center; }}
.hl {{ white-space: nowrap; }}
.hw {{ display: inline-block; opacity: 0; }}
.hw.it {{ font-family: S; font-style: italic; font-weight: 400; letter-spacing: -.01em; font-size: 1.12em; color: {LAV}; padding-right: .04em; }}
.num {{ position: absolute; right: 60px; top: 1500px; font-weight: 900; font-size: 260px; line-height: 1; color: rgba(182,135,249,.12); letter-spacing: -.05em; }}
.tag {{ position: absolute; left: 50%; top: 1560px; transform: translateX(-50%); padding: 10px 22px; border-radius: 999px; font-family: J; font-size: 22px; letter-spacing: .16em; color: {LAV}; }}
/* A meter */
.meter {{ position: absolute; left: 90px; right: 90px; top: 640px; padding: 46px 50px 50px; border-radius: 44px; z-index: 12; }}
.mlab {{ display: flex; justify-content: space-between; font-family: J; font-size: 24px; letter-spacing: .14em; color: {LAV}; }}
.mlab b {{ color: #fff; }}
.mval {{ margin: 26px 0 30px; display: flex; align-items: baseline; gap: 22px; }}
.mval span {{ font-weight: 900; font-size: 190px; line-height: .9; letter-spacing: -.05em; }}
.mval em {{ font-family: S; font-style: italic; font-size: 84px; color: {LAV}; }}
.mbar {{ height: 26px; border-radius: 14px; background: rgba(255,255,255,.08); overflow: hidden; }}
.mbar i {{ display: block; height: 100%; border-radius: 14px; background: linear-gradient(90deg, {VIO}, {LAV}); transform-origin: left center; transform: scaleX(.08); box-shadow: 0 0 24px {STAR}; }}
.mend {{ margin-top: 28px; display: flex; justify-content: space-between; align-items: center; font-family: J; font-size: 24px; color: rgba(255,255,255,.6); letter-spacing: .1em; }}
.mend b {{ color: #fff; font-size: 26px; }}
.paid {{ position: absolute; right: 40px; top: 120px; padding: 14px 26px; border: 6px solid {RED}; border-radius: 18px; color: {RED}; font-weight: 900; font-size: 54px;
  letter-spacing: .02em; background: rgba(20,4,20,.75); opacity: 0; }}
.pick {{ position: absolute; left: 90px; right: 90px; top: 1130px; padding: 26px 30px 30px; border-radius: 34px; opacity: 0; }}
.pkh {{ font-family: J; font-size: 22px; letter-spacing: .16em; color: {LAV}; margin-bottom: 16px; }}
.po {{ display: flex; align-items: center; gap: 18px; padding: 20px 24px; border-radius: 20px; font-size: 38px; border: 1.5px solid transparent; color: rgba(255,255,255,.45); }}
.po.on {{ color: #fff; background: rgba(122,47,251,.22); border-color: rgba(182,135,249,.6); }}
.po span {{ font-family: J; font-size: 22px; color: {LAV}; letter-spacing: .06em; }}
.po i {{ margin-left: auto; width: 40px; height: 40px; border-radius: 50%; background: {STAR}; font-style: normal; font-size: 22px; display: flex; align-items: center; justify-content: center; }}
/* B mails, tiles */
.mails {{ position: absolute; left: 90px; right: 90px; top: 620px; display: flex; flex-direction: column; gap: 22px; }}
.mail {{ position: relative; display: flex; align-items: center; gap: 24px; padding: 28px 32px; border-radius: 28px; opacity: 0; }}
.mail > i {{ width: 64px; height: 64px; border-radius: 16px; background: linear-gradient(135deg, {VIO}, {ELEC}); flex: none; }}
.mail b {{ display: block; font-size: 36px; font-weight: 700; }} .mail span {{ display: block; font-size: 28px; color: rgba(255,255,255,.55); margin-top: 4px; }}
.mail u {{ position: absolute; left: 24px; right: 24px; top: 50%; height: 6px; border-radius: 3px; background: {RED}; transform: scaleX(0); transform-origin: left center; }}
.tiles {{ position: absolute; left: 70px; right: 70px; top: 620px; display: flex; flex-direction: column; gap: 26px; }}
.tile {{ position: relative; display: flex; align-items: center; gap: 30px; padding: 34px 40px; border-radius: 32px; opacity: 0; }}
.tile em {{ font-style: normal; font-family: J; font-size: 34px; color: {LAV}; }}
.tile b {{ font-size: 64px; font-weight: 800; letter-spacing: -.03em; }}
/* C questions */
.q {{ position: absolute; display: flex; align-items: center; gap: 16px; padding: 18px 26px; border-radius: 999px; font-size: 32px; font-weight: 700; opacity: 0; z-index: 14; }}
.q i {{ width: 40px; height: 40px; border-radius: 50%; background: {STAR}; color: #fff; font-style: normal; font-size: 22px; display: flex; align-items: center; justify-content: center; }}
#twin {{ position: absolute; left: 0; top: 520px; width: 1080px; height: 1080px; z-index: 13; filter: drop-shadow(0 0 40px rgba(122,47,251,.55)); }}
/* D */
.bubs {{ position: absolute; left: 70px; right: 70px; top: 560px; display: flex; flex-direction: column; gap: 26px; }}
.bub {{ position: relative; padding: 28px 34px; border-radius: 30px 30px 30px 8px; font-size: 40px; font-weight: 700; line-height: 1.22; opacity: 0; }}
.bub em {{ display: block; font-style: normal; font-family: J; font-size: 20px; letter-spacing: .16em; color: {LAV}; margin-bottom: 10px; }}
.bub:nth-child(2) {{ margin-left: 80px; }}
.board {{ position: absolute; left: 70px; right: 70px; top: 560px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; opacity: 0; }}
.btitle {{ grid-column: 1 / -1; font-weight: 800; font-size: 44px; margin-bottom: 8px; }}
.btitle em {{ font-family: S; font-weight: 400; color: {LAV}; }}
.mo {{ padding: 20px 20px 22px; border-radius: 22px; opacity: 0; }}
.mo b {{ display: block; font-family: J; font-size: 24px; color: {LAV}; letter-spacing: .12em; }}
.mo span {{ display: block; margin-top: 8px; font-size: 27px; font-weight: 700; }}
/* E editor */
.ed {{ position: absolute; left: 60px; right: 60px; top: 520px; padding: 0 0 26px; border-radius: 30px; opacity: 0; background: rgba(12,4,30,.78); }}
.edt {{ display: flex; align-items: center; gap: 10px; padding: 20px 26px; border-bottom: 1px solid rgba(255,255,255,.1); margin-bottom: 16px; }}
.edt i {{ width: 16px; height: 16px; border-radius: 50%; background: rgba(255,255,255,.25); }}
.edt b {{ margin-left: 16px; font-family: J; font-size: 24px; color: {LAV}; letter-spacing: .06em; }}
.cl {{ display: flex; gap: 22px; padding: 4px 30px; font-family: J; font-size: 27px; line-height: 1.45; opacity: 0; }}
.cl i {{ font-style: normal; width: 30px; color: rgba(255,255,255,.3); text-align: right; flex: none; }}
.cl:nth-child(-n+6) span {{ color: {LAV}; }}
.models {{ position: absolute; left: 60px; right: 60px; top: 1300px; display: flex; justify-content: center; gap: 30px; }}
.mdl {{ padding: 22px 38px; border-radius: 999px; font-weight: 800; font-size: 38px; opacity: 0; }}
.link {{ position: absolute; left: 538px; top: 1210px; width: 4px; height: 90px; background: linear-gradient({LAV}, {STAR}); transform-origin: top center; transform: scaleY(0); box-shadow: 0 0 16px {STAR}; }}
.after {{ position: absolute; left: 50%; top: 1440px; transform: translateX(-50%); display: flex; align-items: center; gap: 16px; padding: 18px 30px; border-radius: 999px; font-weight: 800; font-size: 34px; white-space: nowrap; opacity: 0; }}
.after i {{ width: 42px; height: 42px; border-radius: 50%; background: #2fbf71; font-style: normal; font-size: 24px; display: flex; align-items: center; justify-content: center; }}
/* F CTA */
.cm {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-family: S; font-style: italic; font-size: 110px; color: {LAV}; opacity: 0; }}
.kw {{ position: absolute; left: 0; right: 0; top: 450px; text-align: center; font-weight: 900; font-size: 236px; letter-spacing: -.03em; line-height: 1.1; opacity: 0;
  color: #fff; text-shadow: 0 0 60px rgba(122,47,251,.8); }}
.cbox {{ position: absolute; left: 90px; right: 90px; top: 790px; height: 124px; border-radius: 70px; display: flex; align-items: center; gap: 22px; padding: 0 20px 0 24px; opacity: 0; }}
.cbox > i {{ width: 78px; height: 78px; border-radius: 50%; background: linear-gradient(135deg, {VIO}, {ELEC}); flex: none; }}
.cbox span {{ font-weight: 700; font-size: 50px; color: rgba(255,255,255,.5); }}
.cbox b {{ margin-left: auto; width: 88px; height: 88px; border-radius: 50%; background: #fff; color: {STAR}; font-size: 42px; display: flex; align-items: center; justify-content: center; flex: none; }}
.pdf {{ position: absolute; left: 50%; top: 990px; width: 560px; margin-left: -280px; padding: 40px 40px 44px; border-radius: 34px; opacity: 0;
  background: linear-gradient(160deg, rgba(127,27,248,.55), rgba(16,2,44,.85)); }}
.pk {{ font-family: J; font-size: 22px; letter-spacing: .18em; color: {LAV}; }}
.pt {{ margin-top: 14px; font-weight: 900; font-size: 64px; line-height: 1.02; letter-spacing: -.03em; }}
.pt em {{ font-family: S; font-weight: 400; color: {LAV}; }}
.pl {{ margin-top: 24px; display: flex; flex-wrap: wrap; gap: 10px; }}
.pl span {{ padding: 8px 16px; border-radius: 999px; font-family: J; font-size: 20px; border: 1.5px solid rgba(182,135,249,.6); }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Fable 5.2 week 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      {glows}<div id="gridbg"></div>
      <div class="brandbar"><img src="assets/img/logo-wordmark.png" alt=""></div>
      <div id="cam"><div id="punch"><div id="drift">
        {chr(10).join(HTML)}
        {TW}
      </div></div></div>
      <div id="flash"></div><div id="stk0" class="stk"></div><div id="stk1" class="stk"></div><div id="stk2" class="stk"></div><div id="grain"></div>
    </div>
    <script>
      window.FB_T = {{"twin": {json.dumps([round(x, 3) for x in TWIN])}}};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set(".stk", {{rotation: -24, xPercent: -260}}, 0);
      tl.set(".sh", {{skewX: -18, xPercent: -160}}, 0);
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/twin.js"></script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {"hook": [SA, SB], "emails": [SB, SC], "twin": [SC, SD], "plan": [SD, SE], "skill": [SE, SF], "cta": [SF, DUR]}},
          open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
