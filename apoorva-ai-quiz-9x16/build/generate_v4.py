"""Apoorva AI true-or-false quiz (9:16), v3 "editorial": writes index.html, plan/sfx_events.json and plan/edit.json.

v3 (owner on v2: "it doesn't give a leader vibe"; difficulty levels should be "displayed somewhere so that viewer looks
forward to the end"; the red and green background after every answer compromises quality; the question box "looks like
AI slop"; then "Dont add those title and company name, remove the mascot"):
- a broadcast / editorial look: no boxes, no pills, no mascot, no confetti, no full-frame colour flashes;
- a labelled level ladder at the top for the whole video (WARM-UP, EASY, MEDIUM, MEDIUM, HARD, BOSS) with a progress
  line; the current level is lit, answered levels fill green T / coral F, the boss box is gold with a crown and a "?";
- an editorial lower third on a soft dark gradient: a kicker ("Q3 / MEDIUM") on a thin rule, the question in a serif,
  word by word; the lock-in fills the rule over 1.2 s with a small 3 / 2 / 1 and a slow push-in on her stare;
- the answer as one bold word ("FALSE.") with a coloured underline, then the "why" line in serif italic;
- a light grade (contrast, warmth), a fixed soft vignette and fine grain; restrained sounds (tick, low hit, click).
python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "plan", "events.json")))
DUR = E["dur"]
P = {p["label"]: p for p in E["pieces"]}
OFF, GOLD, GREEN, CORAL = "#F6F1E7", "#E8B04B", "#3DDC97", "#FF5A5F"
JS, SFX, HTML = [], [], []


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


def wt(label, word, n=0):
    hits = [w for w in P[label]["words"] if w["w"].lower().strip(".,?!").startswith(word.lower())]
    return hits[min(n, len(hits) - 1)]["t0"]


LEVELS = ["WARM-UP", "EASY", "MEDIUM", "MEDIUM", "HARD", "BOSS"]
QS = [
    (1, "Does NVIDIA manufacture chips?", "q1", "lock1", "a1", "False", "F", "NVIDIA designs the chips. TSMC makes them."),
    (2, "It's AI, so it gives the same answer every time.", "q2", "lock2", "a2b", "True", "T", "Same prompt, different answers: AI samples."),
    (3, "A model on its own can't tell you today's news.", "q3", "lock3", "a3", "True", "T", "Live news needs search or tools."),
    (4, "Longer prompt, better answer.", "q4", "lock4", "a4", "False", "F", "Clear beats long."),
    (5, "Ask AI to double-check itself and it catches every mistake.", "q5", "lock5", "a5", "False", "F", "AI can miss its own mistakes."),
    (6, "A model that's 99% accurate can still be useless.", "q6", "lock6", None, None, "?", None),
]

# ---- level ladder -------------------------------------------------------------------------------------------------------------
lad = "".join(f'<div class="lv{" boss" if n == 6 else ""}" id="lv{n}"><div class="bx" id="bx{n}"><i class="bf" id="bf{n}"></i><b class="bt" id="bt{n}">'
              f'{"" if n < 6 else ""}</b>{"<svg class=crown viewBox=&quot;0 0 40 24&quot;></svg>" if False else ""}</div><span class="ll" id="ll{n}">{LEVELS[n - 1]}</span></div>'
              for n in range(1, 7))
CROWN = '<svg id="crown" viewBox="0 0 40 22"><path d="M3 20 L6 5 L14 13 L20 2 L26 13 L34 5 L37 20 Z" fill="#E8B04B"/></svg>'
HTML.append(f'<div id="lad"><div class="rail"><i id="railf"></i></div><div class="row">{lad}</div>{CROWN}</div>')
# ---- lower thirds (v4, after the owner's Canva design: torn newsprint, bold serif, red kicker, rule, mustard bar) ----
HTML.append('<div id="sheet"><img src="assets/img/paper.png"><svg class="reg" viewBox="0 0 60 60"><path d="M30 0 V60 M0 30 H60" stroke="#B8902F" stroke-width="1.5"/>'
            '<circle cx="30" cy="30" r="9" fill="none" stroke="#B8902F" stroke-width="1.5"/></svg></div>')
for n, q, ql, ll, al, aw, tf, why in QS:
    lvl = LEVELS[n - 1] if n < 6 else "BOSS LEVEL"
    HTML.append(f'<div class="lt{" bosslt" if n == 6 else ""}" id="lt{n}"><div class="kick" id="kk{n}">' + "".join(f"<i>{c}</i>" for c in f"Q{n} / {lvl}") + '</div>'
                f'<div class="q" id="q{n}">' + " ".join(f'<span class="w">{w}</span>' for w in q.split()) + "</div>"
                f'<div class="rule"><i id="ru{n}"></i></div><div class="tf" id="tf{n}">TRUE OR FALSE?</div><div class="bar"><i id="rf{n}"></i></div>'
                + (f'<div class="why" id="why{n}">{why}</div>' if tf in "TF" else "") + "</div>")
    if tf in "TF":
        HTML.append(f'<div class="stp {"sT" if tf == "T" else "sF"}" id="an{n}"><b>{"TRUE" if tf == "T" else "FALSE"}</b></div>')
HTML.append('<div class="stp sF" id="an2f" style="right:262px;top:1560px"><b>FALSE</b></div><div id="wait">WAIT.</div>')
HTML.append('<div class="lt" id="hk"><div class="kick">' + "".join(f"<i>{c}</i>" for c in "TRUE OR FALSE") + '</div>'
            '<div class="q hq"><span class="w">Six</span> <span class="w">AI</span> <span class="w">myths.</span> <span class="w red">No</span> <span class="w red">prep.</span></div>'
            '<div class="rule"><i id="ruh"></i></div><div class="tf">SCORE YOURSELF AS YOU GO</div></div>')
HTML.append('<div class="lt bosslt" id="cta"><div class="kick">' + "".join(f"<i>{c}</i>" for c in "BOSS LEVEL") + '</div>'
            '<div class="q">True or false? <span class="red">Comment below.</span></div><div class="rule"><i id="ruc"></i></div>'
            '<div class="cline"><span id="cph">Add a comment\u2026</span><span id="cty">' + "".join(f"<i>{c}</i>" for c in "TRUE or FALSE") + '</span></div></div>')
for k in (3, 2, 1):
    HTML.append(f'<b class="cnt" id="c{k}">{k}</b>')

# ---- hook ---------------------------------------------------------------------------------------------------------------------
INKR, INKG, MUST = "#B3261E", "#24663A", "#C8962E"
ft("#lad", 0, .5, "{opacity: 0, y: -30}", "{opacity: 1, y: 0}", "power3.out")
ft(".lv", .1, .35, "{opacity: 0, y: -14}", "{opacity: 1, y: 0, stagger: .06}", "power3.out")
ft("#crown", .55, .35, "{opacity: 0, y: -16}", "{opacity: 1, y: 0}", "back.out(2)")
js('tl.fromTo("#bx6", {boxShadow: "0 0 0 0 rgba(232,176,75,0)"}, {boxShadow: "0 0 18px 2px rgba(232,176,75,.7)", duration: .6, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}, .6);')
# the newsprint sheet tears up from the bottom and stays for the whole reel
ft("#sheet", 0, .55, "{y: 520, rotation: 2}", "{y: 0, rotation: 0}", "back.out(1.2)")
sfx("whoosh", 0)
sfx("swish", .05)


def kicker(sel, t):
    js(f'tl.fromTo("{sel} i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .028, immediateRender: false}}, {t:.3f});')


def words(sel, times):
    for k, tw in enumerate(times):
        js(f'tl.fromTo("{sel} .w:nth-child({k + 1})", {{opacity: 0, scale: 1.18, y: -4}}, {{opacity: 1, scale: 1, y: 0, duration: .14, ease: "power3.out", immediateRender: false}}, {tw:.3f});')


st("#hk", .25, "{opacity: 1}")
kicker("#hk .kick", .3)
words("#hk .q", [.5 + .13 * k for k in range(5)])
ft("#ruh", .45, .5, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
ft("#hk .tf", 1.1, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
sfx("thump", .5)
to("#hk", P["q1"]["t0"] - .15, .16, "{opacity: 0}", "power2.in")


def light(n, t):
    for m in range(1, 7):
        st(f"#ll{m}", t, f"{{color: '{OFF if m == n else 'rgba(246,241,231,.7)'}'}}")
    st(f"#bx{n}", t, f"{{borderColor: '{OFF}'}}")
    ft(f"#bx{n}", t, .3, "{scale: 1.18}", "{scale: 1}", "back.out(3)")
    to("#railf", t, .5, f"{{scaleX: {(n - .5) / 6:.3f}}}", "power2.out")


def stamp(sel, t, rot):
    ft(sel, t, .16, f"{{opacity: 0, scale: 2.2, rotation: {rot - 12}}}", f"{{opacity: 1, scale: 1, rotation: {rot}}}", "power4.in")
    ft("#sheet", t + .16, .2, "{y: 0}", "{keyframes: [{y: 6, duration: .05}, {y: -3, duration: .05}, {y: 0, duration: .1}]}", "none")
    sfx("stamp", t + .14)


# ---- questions ----------------------------------------------------------------------------------------------------------------
for n, q, ql, ll, al, aw, tf, why in QS:
    t_q, t_lk, t_rv = P[ql]["t0"], P[ll]["t0"], P[ll]["t1"]
    LK = t_rv - t_lk
    light(n, t_q)
    st(f"#lt{n}", t_q - .02, "{opacity: 1}")
    kicker(f"#kk{n}", t_q)
    ft(f"#ru{n}", t_q + .1, .45, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
    ft(f"#tf{n}", t_q + .3, .25, "{opacity: 0}", "{opacity: 1}", "power2.out")
    sfx("typing", t_q)
    if n == 6:
        sfx("riser", t_q - .1)
        sfx("thump", t_q + .1)
    qws = P[ql]["words"]
    words(f"#q{n}", [(qws[min(k, len(qws) - 1)]["t0"] if qws else t_q + .1 * k) - .04 for k in range(len(q.split()))])
    # lock-in: the mustard bar fills, red rubber-stamp numerals thump onto the paper, push-in on her stare
    ft(f"#rf{n}", t_lk, LK, "{scaleX: 0}", "{scaleX: 1}", "none")
    for k, num in enumerate((3, 2, 1)):
        tk = t_lk + LK / 3 * k
        st(".cnt", tk, "{opacity: 0}")
        ft(f"#c{num}", tk, .12, f"{{opacity: 0, scale: 1.8, rotation: {-14 + 6 * k}}}", f"{{opacity: .92, scale: 1, rotation: {-8 + 6 * k}}}", "power4.in")
        sfx("tick", tk)
    st(".cnt", t_rv, "{opacity: 0}")
    ft("#cam", t_lk, LK, "{scale: 1}", "{scale: 1.07}", "sine.inOut")
    ft("#vigl", t_lk, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
    to("#vigl", t_rv, .3, "{opacity: 0}")
    to("#cam", t_rv, .35, "{scale: 1}", "power3.out")
    if n == 6:
        continue
    # reveal: an inked rubber stamp lands on the sheet, the ladder box fills, then the why line types on
    t_a = wt(al, aw) - .03
    stamp(f"#an{n}", t_a - .1, -7 if tf == "F" else 5)
    col = INKG if tf == "T" else INKR
    st(f"#bf{n}", t_a + .1, f"{{background: '{col}'}}")
    ft(f"#bf{n}", t_a + .1, .3, "{scaleY: 0}", "{scaleY: 1}", "power3.out")
    st(f"#bt{n}", t_a + .14, f'{{textContent: "{tf}"}}')
    ft(f"#bt{n}", t_a + .14, .25, "{opacity: 0}", "{opacity: 1}")
    st(f"#bx{n}", t_a + .1, f"{{borderColor: '{col}'}}")
    sfx("impact", t_a + .04)
    sfx("click", t_a + .12)
    if n == 2:
        continue
    to(f"#tf{n}", t_a + .45, .15, "{opacity: 0}")
    to(f"#lt{n} .bar", t_a + .45, .15, "{opacity: 0}")
    ft(f"#why{n}", t_a + .5, .5, "{opacity: 0, clipPath: 'inset(0 100% 0 0)'}", "{opacity: 1, clipPath: 'inset(0 0% 0 0)'}", "none")
    sfx("typing", t_a + .5)

# ---- Q2: her live flip: TRUE is stamped, crossed out by hand, FALSE is stamped over it ---------------------------------
t_sorry = wt("a2c", "Sorry") - .05
ft("#wait", t_sorry, .14, "{opacity: 0, scale: 1.6, rotation: -14}", "{opacity: 1, scale: 1, rotation: -6}", "power4.in")
ft("#an2 .x", t_sorry + .1, .25, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
sfx("swish", t_sorry)
t_f2 = wt("a2c", "false") - .03
to("#an2", t_f2 - .02, .2, "{opacity: .35}", "power2.out")
stamp("#an2f", t_f2 - .08, -7)
js(f'tl.to("#bx2", {{rotationY: 180, duration: .26, ease: "power2.inOut"}}, {t_f2:.3f});')
st("#bt2", t_f2 + .13, '{textContent: "F", rotationY: 180}')
st("#bf2", t_f2 + .13, f"{{background: '{INKR}'}}")
st("#bx2", t_f2 + .13, f"{{borderColor: '{INKR}'}}")
to("#wait", t_f2 + .45, .2, "{opacity: 0}")
sfx("impact", t_f2 + .04)
to("#tf2", t_f2 + .5, .15, "{opacity: 0}")
to("#lt2 .bar", t_f2 + .5, .15, "{opacity: 0}")
ft("#why2", t_f2 + .55, .5, "{opacity: 0, clipPath: 'inset(0 100% 0 0)'}", "{opacity: 1, clipPath: 'inset(0 0% 0 0)'}", "none")
sfx("typing", t_f2 + .55)

# ---- exits: stamps and text lift off, the sheet stays -------------------------------------------------------------------
for i, (n, *_r) in enumerate(QS[:-1]):
    t_next = P[QS[i + 1][2]]["t0"]
    to(f"#lt{n}", t_next - .14, .14, "{opacity: 0}", "power2.in")
    if QS[i][6] in "TF":
        to(f"#an{n}", t_next - .14, .14, "{opacity: 0}", "power2.in")
    if n == 2:
        to("#an2f", t_next - .14, .14, "{opacity: 0}", "power2.in")
    ft("#sheet", t_next - .1, .3, "{y: 0}", "{keyframes: [{y: 14, duration: .1}, {y: 0, duration: .2}]}", "none")

# ---- boss: poll and CTA -----------------------------------------------------------------------------------------------------
t_cta = P["cta"]["t0"]
st("#bt6", t_cta - .1, '{textContent: "?"}')
ft("#bt6", t_cta - .1, .3, "{opacity: 0}", "{opacity: 1}")
js(f'tl.fromTo("#bx6", {{boxShadow: "0 0 0 0 rgba(232,176,75,0)"}}, {{boxShadow: "0 0 20px 3px rgba(232,176,75,.8)", duration: .4, yoyo: true, repeat: {int((DUR - t_cta) / .4)}, ease: "sine.inOut", immediateRender: false}}, {t_cta:.3f});')
to("#lt6", t_cta - .1, .16, "{opacity: 0}", "power2.in")
st("#cta", t_cta, "{opacity: 1}")
kicker("#cta .kick", t_cta)
ft("#cta .q", t_cta + .12, .3, "{opacity: 0, scale: 1.08}", "{opacity: 1, scale: 1}", "power3.out")
ft("#ruc", t_cta + .2, .45, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
ft("#cta .cline", t_cta + .35, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
t_ty = wt("cta", "comment") - .1
st("#cph", t_ty, "{opacity: 0}")
js(f'tl.fromTo("#cty i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .05, immediateRender: false}}, {t_ty:.3f});')
sfx("thump", t_cta)
sfx("typing", t_ty)
sfx("click", t_ty + .75)

CSS = f"""
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: Serif; src: url("assets/fonts/InstrumentSerif-Regular.ttf"); }}
@font-face {{ font-family: Gloock; src: url("assets/fonts/Gloock-Regular.ttf"); }}
@font-face {{ font-family: Cond; font-weight: 700; src: url("assets/fonts/BigShoulders-Bold.ttf"); }}
@font-face {{ font-family: Plex; font-style: italic; src: url("assets/fonts/IBMPlexSerif-Italic.ttf"); }}
@font-face {{ font-family: Bask; src: url("assets/fonts/LibreBaskerville-Regular.ttf"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: {OFF}; background: #000; }}
#punch, #cam {{ position: absolute; inset: 0; transform-origin: 50% 32%; }}
#ar {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; filter: contrast(1.07) saturate(1.04) sepia(.06); }}
#vig {{ position: absolute; inset: 0; pointer-events: none; background: radial-gradient(85% 60% at 50% 36%, rgba(0,0,0,0) 55%, rgba(0,0,0,.38) 100%); }}
#vigl {{ position: absolute; inset: 0; opacity: 0; pointer-events: none; background: radial-gradient(65% 50% at 50% 34%, rgba(0,0,0,0) 45%, rgba(0,0,0,.5) 100%); }}
#top {{ position: absolute; left: 0; right: 0; top: 0; height: 420px; background: linear-gradient(180deg, rgba(8,8,10,.62), rgba(8,8,10,0)); }}
#bot {{ position: absolute; left: 0; right: 0; bottom: 0; height: 780px; background: linear-gradient(0deg, rgba(8,8,10,.86) 0%, rgba(8,8,10,.6) 45%, rgba(8,8,10,0) 100%); }}
#grain {{ position: absolute; inset: 0; opacity: .06; background: url(assets/img/grain.png); mix-blend-mode: overlay; pointer-events: none; }}
/* level ladder */
#lad {{ position: absolute; left: 0; right: 0; top: 256px; opacity: 0; z-index: 20; }}
#lad .rail {{ position: absolute; left: 150px; right: 150px; top: 34px; height: 2px; background: rgba(246,241,231,.25); }}
#railf {{ position: absolute; inset: 0; background: {OFF}; transform-origin: 0 50%; transform: scaleX(0); }}
#lad .row {{ position: relative; display: flex; justify-content: center; gap: 14px; perspective: 600px; }}
.lv {{ display: flex; flex-direction: column; align-items: center; gap: 10px; width: 120px; opacity: 0; }}
.bx {{ position: relative; width: 68px; height: 68px; border-radius: 6px; border: 2px solid rgba(246,241,231,.45); background: rgba(8,8,10,.55); overflow: hidden; }}
.lv.boss .bx {{ border-color: {GOLD}; }}
.bf {{ position: absolute; inset: 0; transform-origin: 50% 100%; transform: scaleY(0); }}
.bt {{ position: absolute; inset: 0; display: grid; place-items: center; font-weight: 800; font-size: 34px; color: #0B0B0C; opacity: 0; }}
#bt6 {{ color: {GOLD}; }}
.ll {{ font-weight: 800; font-size: 20px; letter-spacing: .12em; text-shadow: 0 1px 6px rgba(0,0,0,.8), 0 0 2px rgba(0,0,0,.9); color: rgba(246,241,231,.7); white-space: nowrap; }}
.lv.boss .ll {{ color: {GOLD} !important; }}
#crown {{ position: absolute; left: 50%; top: -24px; width: 40px; height: 22px; margin-left: {3 * 67 + 0}px; opacity: 0; }}
/* v4 lower third: torn newsprint (after the owner's Canva design) */
#bot {{ height: 520px !important; }}
#sheet {{ position: absolute; left: -10px; right: -10px; top: 1352px; height: 640px; z-index: 12; filter: drop-shadow(0 -10px 24px rgba(0,0,0,.35)); }}
#sheet img {{ width: 100%; height: 100%; }}
#sheet .reg {{ position: absolute; right: 236px; top: 236px; width: 44px; height: 44px; opacity: .8; }}
.lt {{ position: absolute; left: 68px; right: 214px; top: 1404px; opacity: 0; z-index: 15; color: #17130F; }}
.kick {{ font-family: Cond; font-weight: 700; font-size: 30px; letter-spacing: .08em; color: #B3261E; }}
.kick i {{ font-style: normal; opacity: 0; }}
.q {{ margin-top: 6px; font-family: Gloock; font-size: 60px; line-height: 1.02; letter-spacing: -.012em; color: #17130F; }}
.q .w {{ display: inline-block; opacity: 0; transform-origin: 50% 70%; }}
.red, .q .red {{ color: #B3261E; }}
.rule {{ position: relative; height: 3px; margin: 16px 0 10px; }}
.rule i {{ position: absolute; inset: 0; background: #17130F; transform-origin: 0 50%; transform: scaleX(0); }}
.tf {{ font-family: Bask; font-size: 24px; letter-spacing: .14em; color: #17130F; opacity: 0; }}
.bar {{ position: relative; width: 150px; height: 7px; margin-top: 10px; background: rgba(200,150,46,.3); }}
.bar i {{ position: absolute; inset: 0; background: #C8962E; transform-origin: 0 50%; transform: scaleX(0); }}
.why {{ position: absolute; left: 0; right: 0; bottom: -64px; font-family: Plex; font-style: italic; font-size: 35px; line-height: 1.2; color: #3A2F25; opacity: 0; }}
.stp {{ position: absolute; right: 224px; top: 1548px; z-index: 18; opacity: 0; padding: 4px 18px; border: 7px solid currentColor; border-radius: 10px;
  -webkit-mask: url(assets/img/ink.png) center / 100% 100%; mask: url(assets/img/ink.png) center / 100% 100%; mix-blend-mode: multiply; }}
.stp b {{ font-family: Cond; font-weight: 700; font-size: 76px; letter-spacing: .04em; line-height: 1; }}
.sT {{ color: #24663A; }} .sF {{ color: #B3261E; }}
.stp .x {{ position: absolute; left: -10px; right: -10px; top: 50%; height: 9px; margin-top: -4px; background: #17130F; transform: scaleX(0) rotate(-6deg); transform-origin: 0 50%; }}
#wait {{ position: absolute; right: 236px; top: 1488px; z-index: 19; font-family: Cond; font-weight: 700; font-size: 40px; color: #B3261E; padding: 0 10px; border: 4px solid #B3261E;
  opacity: 0; background: rgba(238,228,210,.9); }}
.cnt {{ position: absolute; right: 250px; top: 1440px; font-family: Cond; font-weight: 700; font-size: 120px; line-height: 1; color: #B3261E; opacity: 0; z-index: 17;
  -webkit-mask: url(assets/img/ink.png) center / 300% 300%; mask: url(assets/img/ink.png) center / 300% 300%; }}
.bosslt .kick {{ color: #B8902F; }}
.cline {{ margin-top: 6px; padding: 10px 0; border-bottom: 2px solid #17130F; font-family: Bask; font-size: 30px; letter-spacing: .06em; color: #17130F; opacity: 0; }}
#cph {{ position: absolute; color: rgba(23,19,15,.4); }}
#cty i {{ font-style: normal; opacity: 0; }}
"""
# the Q2 answer carries a strike line for her flip
HTML = [h.replace('<div class="stp sT" id="an2"><b>TRUE</b>', '<div class="stp sT" id="an2"><b>TRUE</b><i class="x"></i>') for h in HTML]
# the crown sits over box 6 (6 boxes of 112 px + 22 px gaps, centred)
CSS = CSS.replace(f"margin-left: {3 * 67 + 0}px", f"margin-left: {int(2.5 * 134 - 20)}px")

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Apoorva: AI true or false v4 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="punch"><div id="cam">
        <video id="ar" src="assets/video/aroll.mp4" data-start="0" data-duration="{DUR:.3f}" data-track-index="1" muted playsinline></video>
      </div></div>
      <div id="vig"></div><div id="vigl"></div><div id="top"></div><div id="bot"></div><div id="grain"></div>
      {chr(10).join(HTML)}
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
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
