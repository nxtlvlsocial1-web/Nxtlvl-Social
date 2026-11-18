"""Apoorva AI true-or-false quiz (9:16): writes index.html, plan/sfx_events.json and plan/edit.json from plan/events.json.

Layout (agreed plan): the talking head full frame; a 6-box tracker at the top (the next box fills with a green T or a
red F on each reveal); the difficulty tag under it (Warm-up, Easy, Medium, Medium, Hard, Boss level); the question
card in the lower middle (words appear as they are asked); a 1.2 s lock-in before every reveal (3-2-1 tick ring, slow
push-in on her stare, vignette); a TRUE / FALSE stamp and a one-line "why" chip on each reveal. Q2 keeps her live flip
(box 2 goes green T on "True", glitches, flips to red F on "Sorry, false, false"). Q6 (Boss level) is left as an
audience poll: box 6 pulses "?" and the CTA asks viewers to comment TRUE or FALSE.
python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "plan", "events.json")))
DUR = E["dur"]
P = {p["label"]: p for p in E["pieces"]}
INK, GREEN, RED, GOLD, WHITE = "#0E0F12", "#16A34A", "#E11D48", "#F5B400", "#FFFFFF"
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


# ---- questions -------------------------------------------------------------------------------------------------------------
QS = [
    # (n, tag, tag colour, question text shown, question piece, lock piece, answer piece(s), answer word, T/F, why)
    (1, "WARM-UP", "#22C55E", "Does NVIDIA manufacture chips?", "q1", "lock1", "a1", "False", "F", "NVIDIA designs the chips. TSMC makes them."),
    (2, "EASY", "#84CC16", "It's AI, so it gives the same answer every time.", "q2", "lock2", "a2b", "True", "T", "Same prompt, different answers: AI samples."),
    (3, "MEDIUM", "#F59E0B", "A model on its own can't tell you today's news.", "q3", "lock3", "a3", "True", "T", "Live news needs search or tools."),
    (4, "MEDIUM", "#F59E0B", "Longer prompt, better answer.", "q4", "lock4", "a4", "False", "F", "Clear beats long."),
    (5, "HARD", "#F97316", "Ask AI to double-check itself and it catches every mistake.", "q5", "lock5", "a5", "False", "F", "AI can miss its own mistakes."),
    (6, "BOSS LEVEL", "#A855F7", "A model that's 99% accurate can still be useless.", "q6", "lock6", None, None, "?", None),
]

boxes = "".join(f'<div class="bx{" boss" if n == 6 else ""}" id="bx{n}"><span class="bn">{n}</span><b class="bt" id="bt{n}"></b><i class="bf" id="bf{n}"></i></div>' for n in range(1, 7))
HTML.append(f'<div id="trk"><div class="tl">AI: TRUE OR FALSE</div><div class="row">{boxes}</div></div>')
HTML.append('<div id="tag"><i id="tagdot"></i><span id="tagtx"></span><em id="tagq"></em></div>')
for n, tag, col, q, ql, ll, al, aw, tf, why in QS:
    words = q.split()
    HTML.append(f'<div class="qc{" bossc" if n == 6 else ""}" id="qc{n}"><div class="qn">QUESTION {n}</div><div class="qt">' +
                " ".join(f'<span class="qw">{w}</span>' for w in words) + "</div>"
                + (f'<div class="stamp {"st" if tf == "T" else "sf"}" id="sp{n}">{"TRUE" if tf == "T" else "FALSE"}</div>' if tf in "TF" else "")
                + (f'<div class="why" id="why{n}">{why}</div>' if why else "") + "</div>")
HTML.append('<div class="stamp sf" id="sp2f">FALSE</div>')
HTML.append('<div id="lk"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" class="rt"/><circle cx="60" cy="60" r="52" class="rf" id="rf" pathLength="1000"/></svg>'
            '<b class="ln" id="ln3">3</b><b class="ln" id="ln2">2</b><b class="ln" id="ln1">1</b></div><div id="lkt">LOCK IN YOUR ANSWER</div>')
# hook and CTA
HTML.append('<div id="hk"><div class="hk1">Apoorva, quick:</div><div class="hk2">TRUE <em>or</em> FALSE?</div>'
            '<div class="hk3">6 AI questions. Score yourself.</div></div><div id="bosstz">Q6 = BOSS LEVEL</div>')
HTML.append('<div id="cta"><div class="c1">BOSS LEVEL</div><div class="c2">TRUE <em>or</em> FALSE?</div>'
            '<div class="cbar"><i></i><span id="cph">Add a comment…</span><span id="cty">' + "".join(f"<i>{c}</i>" for c in "TRUE or FALSE") +
            '</span></div><div class="c3">Comment your answer. How many did you get right?</div></div>')

# ---- hook ---------------------------------------------------------------------------------------------------------------------
st("#hk", 0, "{opacity: 1}")
ft("#hk .hk1", 0, .35, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
ft("#hk .hk2", .25, .45, "{opacity: 0, scale: 1.6}", "{opacity: 1, scale: 1}", "back.out(1.8)")
ft("#hk .hk3", .7, .35, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "power3.out")
ft("#trk", .15, .5, "{opacity: 0, y: -120}", "{opacity: 1, y: 0}", "back.out(1.6)")
ft(".bx", .3, .35, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1, stagger: .05}", "back.out(2.4)")
ft("#bosstz", .9, .3, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(3)")
js('tl.fromTo("#bosstz", {scale: 1}, {scale: 1.08, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}, 1.2);')
sfx("impact", 0)
sfx("whoosh", .15)
for k in range(6):
    sfx("tick", .3 + .05 * k)
sfx("pop", .9)
hk_out = P["q1"]["t0"] - .05
to("#hk", hk_out, .25, "{opacity: 0, y: -40}", "power2.in")
to("#bosstz", hk_out, .2, "{opacity: 0, scale: .6}", "power2.in")

# ---- each question ----------------------------------------------------------------------------------------------------------
for i, (n, tag, col, q, ql, ll, al, aw, tf, why) in enumerate(QS):
    t_q = P[ql]["t0"]
    t_lk, t_rv = P[ll]["t0"], P[ll]["t1"]
    # tag + question card in
    st("#tagtx", t_q - .02, f'{{textContent: "{tag}"}}')
    st("#tagq", t_q - .02, f'{{textContent: "{n} / 6"}}')
    st("#tagdot", t_q - .02, f"{{background: '{col}', boxShadow: '0 0 14px {col}'}}")
    ft("#tag", t_q - .02, .35, "{opacity: 0, scale: .7, y: -20}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.6)")
    st(f"#bx{n}", t_q, "{borderColor: '#FFFFFF', boxShadow: '0 0 0 5px rgba(255,255,255,.35), 0 10px 30px rgba(0,0,0,.35)'}")
    ft(f"#qc{n}", t_q, .4, "{opacity: 0, y: 140, rotation: -3}", "{opacity: 1, y: 0, rotation: 0}", "back.out(1.5)")
    sfx("whoosh" if n != 6 else "riser", t_q - .05)
    # words appear as they are asked (question words from the edit; the card text is the clean spelling)
    qws = P[ql]["words"]
    for k in range(len(q.split())):
        tw = qws[min(k, len(qws) - 1)]["t0"] if qws else t_q + .1 * k
        ft(f"#qc{n} .qw:nth-child({k + 1})", tw - .04, .22, "{opacity: 0, y: 18}", "{opacity: 1, y: 0}", "power3.out")
    if n == 6:
        ft("#qc6", t_q + .1, .3, "{boxShadow: '0 0 0 0 rgba(168,85,247,0)'}", "{boxShadow: '0 0 0 10px rgba(168,85,247,.45)'}", "power2.out")
        sfx("sparkle", t_q + .2)
    # lock-in: 3-2-1 ring, push-in on her stare, vignette
    ft("#lk", t_lk, .2, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.5)")
    ft("#lkt", t_lk, .2, "{opacity: 0, y: 12}", "{opacity: 1, y: 0}", "power2.out")
    ft("#rf", t_lk, LK := (t_rv - t_lk), "{strokeDashoffset: 0}", "{strokeDashoffset: 1000}", "none")
    for k, num in enumerate((3, 2, 1)):
        tk = t_lk + LK / 3 * k
        st(".ln", tk, "{opacity: 0}")
        ft(f"#ln{num}", tk, .18, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "back.out(3)")
        sfx("tick", tk)
    st(".ln", t_rv, "{opacity: 0}")
    ft("#cam", t_lk, LK, "{scale: 1}", "{scale: 1.09}", "sine.inOut")
    ft("#vig", t_lk, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
    to("#lk", t_rv - .02, .15, "{opacity: 0, scale: .6}", "power2.in")
    to("#lkt", t_rv - .02, .15, "{opacity: 0}")
    to("#vig", t_rv, .3, "{opacity: 0}")
    to("#cam", t_rv, .35, "{scale: 1}", "power3.out")
    if n == 6:
        continue
    # reveal
    t_a = wt(al, aw) - .03
    ft(f"#sp{n}", t_a, .22, "{opacity: 0, scale: 2.4, rotation: -20}", "{opacity: 1, scale: 1, rotation: -8}", "power4.in")
    st(f"#bt{n}", t_a + .1, f'{{textContent: "{tf}"}}')
    ft(f"#bf{n}", t_a + .1, .3, "{scaleY: 0}", "{scaleY: 1}", "back.out(2)")
    st(f"#bx{n}", t_a + .1, f"{{borderColor: '{GREEN if tf == 'T' else RED}', boxShadow: 'none'}}")
    ft(f"#bt{n}", t_a + .15, .3, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}", "back.out(3)")
    ft("#punch", t_a + .2, .08, "{scale: 1}", "{scale: 1.04}", "power2.out")
    to("#punch", t_a + .28, .3, "{scale: 1}", "power3.out")
    sfx("stamp", t_a + .2)
    sfx("ding" if tf == "T" else "buzzer", t_a + .25)
    if n == 2:
        continue                      # Q2's why chip comes after her flip
    t_w = t_a + .45
    ft(f"#why{n}", t_w, .35, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "back.out(2)")
    sfx("pop", t_w)

# ---- Q2: her live flip, True -> "Sorry, false, false" ---------------------------------------------------------------------
t_sorry = wt("a2c", "Sorry") - .05
st("#bf2", 0, f"{{background: '{GREEN}'}}")
js(f'tl.fromTo("#bx2", {{x: 0}}, {{keyframes: [{{x: -10, duration: .04}}, {{x: 9, duration: .04}}, {{x: -6, duration: .04}}, {{x: 4, duration: .04}}, {{x: 0, duration: .04}}], immediateRender: false}}, {t_sorry:.3f});')
js(f'tl.fromTo("#qc2", {{x: 0, filter: "none"}}, {{keyframes: [{{x: -14, filter: "drop-shadow(6px 0 0 rgba(225,29,72,.8)) drop-shadow(-6px 0 0 rgba(0,180,255,.8))", duration: .05}}, {{x: 10, duration: .05}}, {{x: 0, filter: "none", duration: .06}}], immediateRender: false}}, {t_sorry:.3f});')
to("#sp2", t_sorry + .05, .15, "{opacity: 0, scale: .6}", "power2.in")
t_f2 = wt("a2c", "false") - .03
ft("#sp2f", t_f2, .22, "{opacity: 0, scale: 2.4, rotation: 20}", "{opacity: 1, scale: 1, rotation: -8}", "power4.in")
js(f'tl.to("#bx2", {{rotationY: 180, duration: .28, ease: "power2.inOut"}}, {t_f2:.3f});')
st("#bt2", t_f2 + .14, '{textContent: "F", rotationY: 180}')
st("#bf2", t_f2 + .14, f"{{background: '{RED}'}}")
st("#bx2", t_f2 + .14, f"{{borderColor: '{RED}'}}")
ft("#why2", t_f2 + .45, .35, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "back.out(2)")
sfx("pop", t_f2 + .45)
sfx("boing", t_sorry)
sfx("stamp", t_f2 + .2)
sfx("buzzer", t_f2 + .25)
ft("#plot", t_sorry, .25, "{opacity: 0, scale: .5, rotation: -10}", "{opacity: 1, scale: 1, rotation: 6}", "back.out(3)")
to("#plot", t_f2 + .5, .2, "{opacity: 0}")
HTML.append('<div id="plot">WAIT...</div>')

# ---- card exits ----------------------------------------------------------------------------------------------------------------
for i, (n, *_r) in enumerate(QS[:-1]):
    t_next = P[QS[i + 1][4]]["t0"]
    to(f"#qc{n}", t_next - .12, .2, "{opacity: 0, y: -60, scale: .94}", "power2.in")
    to("#tag", t_next - .12, .12, "{opacity: 0}")
    if n == 2:
        to("#sp2f", t_next - .12, .2, "{opacity: 0}")

# ---- boss level: poll, "?" box, CTA ------------------------------------------------------------------------------------------
t_cta = P["cta"]["t0"]
st("#bt6", t_cta - .1, '{textContent: "?"}')
ft("#bt6", t_cta - .1, .3, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}", "back.out(3)")
js(f'tl.fromTo("#bx6", {{scale: 1}}, {{scale: 1.12, duration: .3, yoyo: true, repeat: {int((DUR - t_cta) / .3)}, ease: "sine.inOut", immediateRender: false}}, {t_cta:.3f});')
to("#qc6", t_cta - .05, .25, "{opacity: 0, y: -60}", "power2.in")
to("#tag", t_cta - .05, .15, "{opacity: 0}")
ft("#cta", t_cta, .45, "{opacity: 0, y: 160}", "{opacity: 1, y: 0}", "back.out(1.5)")
ft("#cta .c2", t_cta + .15, .4, "{scale: 1.5}", "{scale: 1}", "back.out(2)")
t_ty = wt("cta", "comment") - .1
st("#cph", t_ty, "{opacity: 0}")
js(f'tl.fromTo("#cty i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .05, immediateRender: false}}, {t_ty:.3f});')
sfx("typing", t_ty)
sfx("impact", t_cta)
sfx("msg", t_ty + .8)
ft("#cta .c3", t_ty + .6, .4, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "power3.out")

CSS = f"""
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: Mono; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: {INK}; background: #000; }}
#punch, #cam {{ position: absolute; inset: 0; transform-origin: 50% 32%; }}
#ar {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
#vig {{ position: absolute; inset: 0; opacity: 0; pointer-events: none; background: radial-gradient(70% 55% at 50% 34%, rgba(0,0,0,0) 45%, rgba(0,0,0,.62) 100%); }}
#shade {{ position: absolute; left: 0; right: 0; top: 0; height: 520px; background: linear-gradient(180deg, rgba(0,0,0,.45), rgba(0,0,0,0)); pointer-events: none; }}
#shadeb {{ position: absolute; left: 0; right: 0; bottom: 0; height: 900px; background: linear-gradient(0deg, rgba(0,0,0,.5), rgba(0,0,0,0)); pointer-events: none; }}
/* tracker */
#trk {{ position: absolute; left: 0; right: 0; top: 196px; text-align: center; opacity: 0; z-index: 20; }}
#trk .tl {{ display: inline-block; font: 22px Mono; letter-spacing: .2em; color: #fff; padding: 8px 18px; border-radius: 999px; background: rgba(14,15,18,.72); margin-bottom: 14px; }}
#trk .row {{ display: flex; gap: 16px; justify-content: center; perspective: 600px; }}
.bx {{ position: relative; width: 116px; height: 116px; border-radius: 26px; border: 5px solid rgba(255,255,255,.75); background: rgba(14,15,18,.45);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); overflow: hidden; opacity: 0; }}
.bx.boss {{ border-color: {GOLD}; }}
.bn {{ position: absolute; left: 10px; top: 6px; font: 18px Mono; color: rgba(255,255,255,.75); z-index: 3; }}
.bf {{ position: absolute; inset: 0; transform-origin: 50% 100%; transform: scaleY(0); }}
#bf1, #bf4, #bf5 {{ background: {RED}; }}
#bf3 {{ background: {GREEN}; }}
.bt {{ position: absolute; inset: 0; display: grid; place-items: center; font-weight: 800; font-size: 72px; color: #fff; z-index: 2; opacity: 0; }}
#bt6 {{ color: {GOLD}; }}
/* difficulty tag */
#tag {{ position: absolute; left: 50%; top: 420px; transform: translateX(-50%); display: flex; align-items: center; gap: 14px; padding: 14px 28px; border-radius: 999px;
  background: {INK}; color: #fff; font-weight: 800; font-size: 34px; letter-spacing: .06em; opacity: 0; z-index: 20; white-space: nowrap; }}
#tag i {{ width: 18px; height: 18px; border-radius: 50%; }}
#tag em {{ font-style: normal; font: 22px Mono; color: rgba(255,255,255,.6); letter-spacing: .1em; }}
/* question cards */
.qc {{ position: absolute; left: 70px; right: 70px; top: 1170px; padding: 34px 40px 40px; border-radius: 38px; background: {WHITE}; opacity: 0; z-index: 15;
  box-shadow: 0 30px 80px rgba(0,0,0,.4); }}
.qc.bossc {{ background: linear-gradient(135deg, #1B1030, #2A1450); color: #fff; border: 4px solid #A855F7; }}
.qn {{ font: 22px Mono; letter-spacing: .18em; color: #6B7280; margin-bottom: 12px; }}
.bossc .qn {{ color: #D8B4FE; }}
.qt {{ font-weight: 800; font-size: 60px; line-height: 1.08; letter-spacing: -.03em; }}
.qw {{ display: inline-block; opacity: 0; }}
.stamp {{ position: absolute; right: 30px; top: -64px; padding: 10px 26px; border-radius: 18px; font-weight: 800; font-size: 76px; letter-spacing: .02em; opacity: 0;
  background: #fff; z-index: 3; }}
.stamp.st {{ color: {GREEN}; border: 8px solid {GREEN}; }}
.stamp.sf {{ color: {RED}; border: 8px solid {RED}; }}
#sp2f {{ position: absolute; right: 100px; top: 1106px; z-index: 30; }}
.why {{ margin-top: 22px; display: inline-block; padding: 12px 22px; border-radius: 16px; background: {INK}; color: #fff; font-weight: 700; font-size: 34px; opacity: 0; }}
#plot {{ position: absolute; left: 90px; top: 1090px; padding: 10px 22px; border-radius: 14px; background: {GOLD}; color: {INK}; font-weight: 800; font-size: 44px; opacity: 0; z-index: 31; }}
/* lock-in */
#lk {{ position: absolute; left: 50%; top: 960px; width: 170px; height: 170px; margin-left: -85px; opacity: 0; z-index: 25; }}
#lk svg {{ position: absolute; inset: 0; width: 100%; height: 100%; transform: rotate(-90deg); }}
#lk .rt {{ fill: rgba(14,15,18,.7); stroke: rgba(255,255,255,.25); stroke-width: 9; }}
#lk .rf {{ fill: none; stroke: {GOLD}; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 1000; }}
.ln {{ position: absolute; inset: 0; display: grid; place-items: center; font-weight: 800; font-size: 96px; color: #fff; opacity: 0; }}
#lkt {{ position: absolute; left: 0; right: 0; top: 1140px; text-align: center; font: 24px Mono; letter-spacing: .2em; color: #fff; opacity: 0; z-index: 25;
  text-shadow: 0 2px 10px rgba(0,0,0,.7); }}
/* hook and CTA */
#hk {{ position: absolute; left: 60px; right: 60px; top: 1120px; text-align: center; color: #fff; opacity: 0; z-index: 20; text-shadow: 0 4px 24px rgba(0,0,0,.6); }}
.hk1 {{ font-weight: 700; font-size: 50px; opacity: 0; }}
.hk2 {{ font-weight: 800; font-size: 112px; letter-spacing: -.04em; line-height: 1; margin: 8px 0 18px; opacity: 0; }}
.hk2 em, .c2 em {{ font-style: normal; font-weight: 600; font-size: .6em; color: {GOLD}; }}
.hk3 {{ display: inline-block; padding: 12px 24px; border-radius: 999px; background: #fff; color: {INK}; font-weight: 800; font-size: 34px; text-shadow: none; opacity: 0; }}
#bosstz {{ position: absolute; right: 70px; top: 430px; padding: 10px 20px; border-radius: 14px; background: #A855F7; color: #fff; font-weight: 800; font-size: 30px; opacity: 0; z-index: 21; }}
#cta {{ position: absolute; left: 60px; right: 60px; top: 1060px; text-align: center; color: #fff; opacity: 0; z-index: 20; }}
#cta .c1 {{ display: inline-block; padding: 10px 22px; border-radius: 14px; background: #A855F7; font-weight: 800; font-size: 34px; letter-spacing: .08em; }}
#cta .c2 {{ font-weight: 800; font-size: 108px; letter-spacing: -.04em; line-height: 1.02; margin: 14px 0 22px; text-shadow: 0 4px 24px rgba(0,0,0,.6); }}
#cta .cbar {{ display: flex; align-items: center; gap: 18px; height: 110px; padding: 0 26px; border-radius: 60px; background: #fff; color: {INK}; font-weight: 800; font-size: 44px; text-align: left; }}
#cta .cbar > i {{ width: 68px; height: 68px; border-radius: 50%; background: linear-gradient(135deg, {GREEN}, {RED}); flex: none; }}
#cph {{ position: absolute; margin-left: 86px; font-weight: 600; color: #9CA3AF; }}
#cty i {{ font-style: normal; opacity: 0; }}
#cta .c3 {{ margin-top: 22px; font-weight: 700; font-size: 38px; opacity: 0; text-shadow: 0 2px 14px rgba(0,0,0,.7); }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Apoorva: AI true or false 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="punch"><div id="cam">
        <video id="ar" src="assets/video/aroll.mp4" data-start="0" data-duration="{DUR:.3f}" data-track-index="1" muted playsinline></video>
      </div></div>
      <div id="vig"></div><div id="shade"></div><div id="shadeb"></div>
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
