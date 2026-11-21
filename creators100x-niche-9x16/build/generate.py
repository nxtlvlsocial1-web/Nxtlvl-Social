"""Creators 100X "Make AI interview you" (keyword NICHE, 9:16), v2 "The Constellation of You": writes index.html,
plan/sfx_events.json and plan/edit.json from plan/words.json.

v1 (a light game-show set, build/generate_gameshow.py) was "very dull and boring" (owner, 2026-11-21). Same approved script and
Kokoro af_heart voice; a new look: deep space with neon glass in the Creators 100X lime and pink, a perspective grid floor, an AI
core of light, and a beat that lands on the music's drop.
  n0 hook: a glass chat pill types "what should I post about?"; the AI core flares; "10 QUESTIONS" blasts out with a shockwave;
  n1 first peak: a swarm of the same ideas everyone gets glitches out under SEEN IT (buzzer, RGB split, shake);
  n2 release ("So flip it", on the drop): warp streaks, white flash, the prompt itself on a glass panel, typed big enough to screenshot;
  n3 build: question cards fly in from deep space and out past the camera; every answer fires a star into a constellation;
  n4 peak: the constellation bursts into three glass niche cards (examples), shockwaves, drumroll;
  n5 release: the stars draw a glowing fingerprint, ONLY YOU; sparks;
  n6 CTA: a white flash into the bright Creators 100X brand frame: the free PDF and COMMENT NICHE.
python3 build/generate.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT  # noqa: E402

random.seed(7)
DUR = round(L1["n6"] + 1.6, 2)
T0 = {k: (L0[k], L1[k]) for k in LINES}

# ---- headlines --------------------------------------------------------------------------------------------------------------------
HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, top, line, size=86, after=0.0, dark=False):
    spoken, k, out_, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?…\""), None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?\"")
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="hw {cls}" id="{wid}">{word}</span>')
            out_.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTMLS.append(f'<div class="head{" dk" if dark else ""}" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out_:
        ft(f"#{wid}", t - .05, .3, "{opacity: 0, filter: 'blur(12px)', y: 26, scale: 1.15}", "{opacity: 1, filter: 'blur(0px)', y: 0, scale: 1}", "power3.out")
    first = min(t for _, t in out_)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .25, .18, "{opacity: 0, filter: 'blur(14px)', y: -34}", "power2.in")
    OPEN[0] = hid


# ---- camera: far stars, near stars + nebulae, the world -----------------------------------------------------------------------------
RIGS = (("#rbg", .25), ("#rmid", .6), ("#rw", 1.0))


def cam(t, cx, cy, z, d=.8, ease="power3.inOut", rot=0, setonly=False):
    for sel, f in RIGS:
        zf = 1 + (z - 1) * f
        cxf, cyf = 540 + (cx - 540) * f, 960 + (cy - 960) * f
        props = f"x: {540 - cxf * zf:.1f}, y: {960 - cyf * zf:.1f}, scale: {zf:.4f}, rotation: {rot * f:.2f}"
        js(f'gsap.set("{sel}", {{{props}}});' if setonly else f'tl.to("{sel}", {{{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def shake(t, amp=16, n=6, per=.04):
    ks = ", ".join(f'{{x: {random.choice((-1, 1)) * amp * (1 - k / n):.1f}, y: {random.choice((-1, 1)) * amp * .5 * (1 - k / n):.1f}, duration: {per}}}' for k in range(n))
    js(f'tl.fromTo("#punch", {{x: 0, y: 0}}, {{keyframes: [{ks}, {{x: 0, y: 0, duration: {per}}}], immediateRender: false}}, {t:.3f});')


def punch(t, k=1.06):
    js(f'tl.fromTo("#punch", {{scale: 1}}, {{keyframes: [{{scale: {k}, duration: .07, ease: "power2.out"}}, {{scale: 1, duration: .4, ease: "power3.out"}}], immediateRender: false}}, {t - .02:.3f});')


def flash(t, o=.7, d=.35):
    st("#flash", t, f"{{opacity: {o}}}")
    to("#flash", t + .02, d, "{opacity: 0}", "power2.out")


def shock(i, t, col="#CCFB79", s=4.0):
    js(f'tl.fromTo("#sh{i}", {{opacity: 1, scale: .2, borderColor: "{col}"}}, {{opacity: 0, scale: {s}, duration: .7, ease: "power2.out", immediateRender: false}}, {t:.3f});')


def typewrite(prefix, n, t0, t1):
    for i in range(n):
        st(f"#{prefix}{i}", t0 + (t1 - t0) * i / max(n - 1, 1), "{opacity: 1}")


# =======================================================================================================================
# THE COSMOS
def stars(n, size, col_p=(.75, .15, .10)):
    out_ = ""
    for _ in range(n):
        c = random.choices(("#ffffff", "#CCFB79", "#ff7ab0"), col_p)[0]
        s = random.uniform(*size)
        out_ += (f'<i class="st" style="left:{random.uniform(-500, 1580):.0f}px;top:{random.uniform(-500, 2420):.0f}px;width:{s:.1f}px;height:{s:.1f}px;'
                 f'background:{c};opacity:{random.uniform(.35, 1):.2f};box-shadow:0 0 {s * 3:.0f}px {c}"></i>')
    return out_


NEBS = ('<i class="neb" id="nb0" style="left:-420px;top:200px;width:1100px;height:1100px;background:radial-gradient(closest-side,rgba(204,251,121,.28),rgba(204,251,121,0))"></i>'
        '<i class="neb" id="nb1" style="left:420px;top:-120px;width:1200px;height:1200px;background:radial-gradient(closest-side,rgba(253,11,104,.32),rgba(253,11,104,0))"></i>'
        '<i class="neb" id="nb2" style="left:80px;top:1100px;width:1100px;height:1000px;background:radial-gradient(closest-side,rgba(110,80,255,.30),rgba(110,80,255,0))"></i>')
BG = f'<div class="space"></div>{stars(110, (1, 2.5))}'
MID = f'{NEBS}{stars(45, (2, 4))}<div class="horizon"></div><div class="grid" id="grid"></div>'
RINGS = "".join(f'<i class="rg" id="rg{i}" style="left:{-r}px;top:{-r}px;width:{2 * r}px;height:{2 * r}px;border-width:{w}px;border-color:{c}"></i>'
                for i, (r, w, c) in enumerate(((120, 4, "rgba(204,251,121,.9)"), (170, 3, "rgba(255,47,126,.85)"), (230, 2, "rgba(255,255,255,.35)"))))
CORE = f'<div id="core"><i class="cg" id="cg"></i>{RINGS}<div id="corb"><i></i><i></i></div></div>'
CS = [(250, 820), (390, 690), (560, 745), (720, 680), (870, 810), (840, 1010), (880, 1200), (670, 1300), (420, 1270), (215, 1100)]
LINKS = [(i, (i + 1) % 10) for i in range(10)] + [(0, 5), (2, 7), (3, 8), (1, 6)]
CONST = ('<svg class="lines" viewBox="0 0 1080 1920"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#CCFB79"/><stop offset="1" stop-color="#ff2f7e"/></linearGradient></defs>'
         + "".join(f'<line id="ln{k}" x1="{CS[a][0]}" y1="{CS[a][1]}" x2="{CS[b][0]}" y2="{CS[b][1]}" stroke="url(#lg)" stroke-width="3" pathLength="1" '
                   f'stroke-dasharray="1" stroke-dashoffset="1" opacity=".9"/>' for k, (a, b) in enumerate(LINKS)) + '</svg>'
         + "".join(f'<i class="cs" id="cs{i}" style="left:{x}px;top:{y}px"></i>' for i, (x, y) in enumerate(CS)))
WORLD = f'{CONST}{CORE}'
SHOCKS = "".join(f'<i class="shock" id="sh{i}"></i>' for i in range(4))

# overlays
Q_ME = "what should I post about?".split()
PILL = ('<div class="ov glass pill" id="pill"><small>YOU</small>' + " ".join(f'<span class="pw" id="cw{i}">{w}</span>' for i, w in enumerate(Q_ME))
        + '<i class="caret" id="caret"></i></div>'
        '<div class="ov glass pill ai" id="reply"><small>AI</small>Before I answer, let me ask you 10 questions.</div>')
BIG10 = '<div class="ov big10" id="big10">10<small>QUESTIONS</small></div>'
IDEAS = ["Day in my life", "5 tips for…", "Morning routine", "What I eat in a day", "Get ready with me", "Q&amp;A", "My desk setup", "Study with me"]
SWARM = ""
SW = []
for i in range(24):
    x, y = random.uniform(40, 760), random.uniform(560, 1500)
    SW.append((x, y))
    SWARM += f'<div class="swc" id="sw{i}" style="left:{x:.0f}px;top:{y:.0f}px">{IDEAS[i % len(IDEAS)]}</div>'
SEEN = '<div class="ov seen" id="seen"><b>SEEN IT</b></div>'
GBARS = "".join(f'<i class="gbar" id="gb{i}" style="top:{random.randint(500, 1500)}px;height:{random.randint(14, 60)}px;background:{c}"></i>'
                for i, c in enumerate(("rgba(0,255,255,.35)", "rgba(255,47,126,.4)", "rgba(204,251,121,.35)", "rgba(255,255,255,.25)", "rgba(0,255,255,.3)")))
WARP = '<div class="warp" id="warp">' + "".join(
    f'<i id="wp{i}" style="width:{random.randint(260, 760)}px;transform:rotate({i * 360 / 48 + random.uniform(-3, 3):.1f}deg) translateX({random.randint(60, 200)}px)"></i>'
    for i in range(48)) + '</div>'
PROMPT_WORDS = [("Ask", 1), ("me", 1), ("10", 1), ("questions", 1), ("about", 0), ("my", 0), ("life,", 0), ("my", 0), ("skills", 0), ("and", 0), ("what", 0), ("I", 0),
                ("can't", 0), ("stop", 0), ("talking", 0), ("about.", 0), ("One", 1), ("question", 1), ("at", 1), ("a", 1), ("time,", 1), ("and", 0), ("wait", 0),
                ("for", 0), ("my", 0), ("answer.", 0), ("Then", 0), ("suggest", 0), ("3", 1), ("niches", 1), ("only", 1), ("I", 1), ("could", 1), ("own,", 1),
                ("with", 0), ("5", 0), ("reel", 0), ("ideas", 0), ("for", 0), ("each.", 0)]
PTXT = " ".join(f'<span class="pw{" mk" if m else ""}" id="pw{i}">{w}</span>' for i, (w, m) in enumerate(PROMPT_WORDS))
PROMPT = f'<div class="ov glass prompt" id="prompt"><span class="tag">COPY THIS PROMPT</span><div class="ptxt">{PTXT}</div></div>'
QS = [("QUESTION 1 / 10", "What do friends always ask you for help with?", "cooking on a budget"),
      ("QUESTION 4 / 10", "What could you talk about for an hour?", "hostel life hacks"),
      ("QUESTION 7 / 10", "What did you learn the hard way?", "eating well when broke")]
QCARDS = "".join(f'<div class="ov glass qc" id="qc{i}"><small>{a}</small><b>{q}</b></div><div class="ov qa" id="qa{i}"><span>"{ans}"</span></div>'
                 for i, (a, q, ans) in enumerate(QS))
QN = '<div class="ov qn" id="qn"><span id="qnn">0</span> / 10 ANSWERED</div>'
NICHES = ["Budget meals for hostel students", "Gym tips for skinny beginners", "Aesthetic exam notes"]
NCARDS = ('<div class="ov nlab" id="nlab">YOUR 3 NICHES</div>'
          + "".join(f'<div class="ov glass niche{" p" if i == 1 else ""}" id="nc{i}" style="top:{660 + i * 170}px"><i></i>{t}</div>' for i, t in enumerate(NICHES))
          + '<div class="ov nex" id="nex">EXAMPLES</div>')
FP_ARCS = ""
for i in range(13):
    rx, ry = 34 + i * 21, 46 + i * 26
    gap, off = random.uniform(.16, .4), random.uniform(-.35, .35)
    a0, a1 = math.pi * (.5 + off + gap / 2), math.pi * (2.5 + off - gap / 2)
    x0, y0 = 300 + rx * math.cos(a0), 380 + ry * math.sin(a0)
    x1, y1 = 300 + rx * math.cos(a1), 380 + ry * math.sin(a1)
    FP_ARCS += (f'<path id="fa{i}" d="M{x0:.1f} {y0:.1f} A{rx} {ry} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="url(#fg)" stroke-width="9" stroke-linecap="round" '
                f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
FP = ('<svg class="ov fp" id="fp" viewBox="0 0 600 760"><defs><linearGradient id="fg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#CCFB79"/>'
      '<stop offset=".55" stop-color="#ffffff"/><stop offset="1" stop-color="#ff2f7e"/></linearGradient></defs>'
      f'<g style="filter:drop-shadow(0 0 10px rgba(204,251,121,.8))">{FP_ARCS}</g><rect id="fscan" x="0" y="40" width="600" height="8" fill="#CCFB79" opacity="0"/></svg>'
      '<div class="ov only" id="only"><span>ONLY YOU</span></div>')
CHIPS = "".join(f'<div class="chip" id="chp{i}" style="left:{x}px;top:{y}px">{t}</div>' for i, (t, x, y) in enumerate(
    (("cooking on a budget", 80, 1500), ("hostel life hacks", 600, 1560), ("eating well when broke", 250, 1660))))
CTA = ('<div id="brand"></div><img id="blogo" src="assets/img/logo.png" alt="">'
       '<div class="ov pdf" id="pdf"><img src="assets/img/logo.png" alt=""><span class="k">FREE PROMPT PACK</span>'
       '<h3>Let AI <span>interview</span> you</h3><p>The prompt + 5 more to plan your first 10 reels.</p></div><div class="ov free" id="free">FREE PDF</div>'
       '<div class="ov kw" id="kw"><span>COMMENT NICHE</span></div>')
COLS = ("#CCFB79", "#FD0B68", "#101111", "#FE70B3", "#ffffff")
CONF = 70
CONFH = "".join(f'<i class="cf" id="cf{i}" style="background:{random.choice(COLS)};width:{random.randint(12, 20)}px;height:{random.randint(22, 34)}px"></i>' for i in range(CONF))

# =======================================================================================================================
# TIMELINE
cam(0, 540, 1010, 1.25, setonly=True)
# always alive: rings spin, nebulae breathe, grid scrolls, core pulses, handheld drift
for i, (sp, d) in enumerate(((1, 9), (-1, 13), (1, 21))):
    js(f'tl.to("#rg{i}", {{rotation: {sp * 360 * DUR / d:.0f}, duration: {DUR}, ease: "none"}}, 0);')
js(f'tl.fromTo("#grid", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "0px 1200px", duration: {DUR}, ease: "none", immediateRender: false}}, 0);')
for i in range(3):
    js(f'tl.fromTo("#nb{i}", {{scale: 1, rotation: 0}}, {{scale: {1.15 + .05 * i}, rotation: {(-1) ** i * 20}, duration: {DUR / 2:.2f}, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#corb", {{scale: 1}}, {{scale: 1.06, duration: .45, yoyo: true, repeat: {int(DUR / .45)}, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#hand", {{x: -4, y: 3, rotation: -.3}}, {{x: 4, y: -3, rotation: .3, duration: 3.1, yoyo: true, repeat: {int(DUR / 3.1)}, ease: "sine.inOut", immediateRender: false}}, 0);')
for k in range(int(DUR / 3.2)):
    js(f'tl.fromTo("#corb i", {{scaleY: 1}}, {{scaleY: .12, duration: .07, yoyo: true, repeat: 1, transformOrigin: "50% 50%", immediateRender: false}}, {1.6 + k * 3.2:.2f});')

# ---- n0 hook ---------------------------------------------------------------------------------------------------------------------
cam(0, 540, 1000, 1.0, 2.6, "power2.out")
ft("#core", 0, .5, "{scale: .4, opacity: 0}", "{scale: 1, opacity: 1}", "back.out(1.6)")
shock(0, .05, "#ffffff", 5)
sfx("whoosh_big", 0)
head("h0", [[("I", ""), ("asked", ""), ("ChatGPT", "")], [("what", ""), ("I", ""), ("should", ""), ("post", "pk"), ("about.", "")]], 240, "n0", size=82)
ft("#pill", .25, .45, "{opacity: 0, y: 60, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.6)")
typewrite("cw", len(Q_ME), T("n0", "what") - .05, T("n0", "about") + .1)
js(f'tl.fromTo("#caret", {{opacity: 1}}, {{opacity: 0, duration: .25, yoyo: true, repeat: 9, ease: "steps(1)", immediateRender: false}}, .3);')
for k in range(5):
    sfx("tick", T("n0", "what") + k * .17)
t_ab = T("n0", "asked", 1)
ft("#reply", t_ab - .05, .4, "{opacity: 0, y: 60, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.6)")
js(f'tl.fromTo("#cg", {{scale: 1}}, {{scale: 1.5, duration: .25, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_ab - .05:.3f});')
sfx("ping", t_ab)
t_q = T("n0", "ten")
to("#pill", t_q - .2, .25, "{opacity: 0, y: -80, scale: .9}", "power2.in")
to("#reply", t_q - .2, .25, "{opacity: 0, y: 80, scale: .9}", "power2.in")
js(f'tl.to("#core", {{opacity: .2, duration: .2}}, {t_q - .1:.3f});')
ft("#big10", t_q - .05, .35, "{opacity: 0, scale: .2, filter: 'blur(20px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "back.out(2)")
shock(1, t_q, "#CCFB79", 5)
shake(t_q + .05, 12)
flash(t_q, .4)
sfx("impact", t_q)
sfx("riser", t_q + .2)
cam(t_q, 540, 1010, 1.12, 1.2, "power2.inOut")

# ---- n1 first peak: the swarm of the same ideas --------------------------------------------------------------------------------
t_gv = T("n1", "Give")
head("h1", [[("\"Give", ""), ("me", ""), ("content", ""), ("ideas\"", "")], [("gets", ""), ("the", ""), ("same", "pk"), ("ideas", "")], [("as", ""), ("everyone", ""), ("else.", "")]],
     220, "n1", size=82)
to("#big10", t_gv - .2, .25, "{opacity: 0, scale: 1.6, filter: 'blur(16px)'}", "power2.in")
js(f'tl.to("#core", {{opacity: 1, duration: .3}}, {t_gv - .15:.3f});')
cam(t_gv - .1, 540, 1040, 1.0, 1.2, "power2.out")
for i, (x, y) in enumerate(SW):
    tk = t_gv + .05 + i * .06
    ft(f"#sw{i}", tk, .45, f"{{opacity: 0, x: {540 - x - 120:.0f}, y: {1010 - y:.0f}, scale: .2}}", f"{{opacity: 1, x: 0, y: 0, scale: 1, rotation: {random.uniform(-8, 8):.1f}}}", "power3.out")
    js(f'tl.to("#sw{i}", {{x: "+={random.uniform(-30, 30):.0f}", y: "+={random.uniform(-30, 30):.0f}", duration: 2, ease: "sine.inOut"}}, {tk + .45:.3f});')
    if i % 4 == 0:
        sfx("pop", tk)
t_ev = T("n1", "everyone")
ft("#seen", t_ev - .05, .22, "{opacity: 0, scale: 2.6}", "{opacity: 1, scale: 1}", "power4.in")
sfx("buzzer", t_ev)
shake(t_ev + .1, 22, 8)
js(f'tl.to(".swc", {{color: "#5d5a78", borderColor: "rgba(255,255,255,.06)", duration: .2}}, {t_ev:.3f});')
for i in range(5):
    js(f'tl.fromTo("#gb{i}", {{opacity: 0, x: 0}}, {{keyframes: [{{opacity: 1, x: {random.choice((-60, 60))}, duration: .05}}, {{opacity: 0, x: 0, duration: .05}}, '
       f'{{opacity: .8, x: {random.choice((-30, 30))}, duration: .05}}, {{opacity: 0, duration: .05}}], immediateRender: false}}, {t_ev + .05 + i * .05:.3f});')
sfx("glitch", t_ev + .1)
js(f'tl.fromTo("#seen b", {{x: 0}}, {{keyframes: [{{x: -8, duration: .04}}, {{x: 8, duration: .04}}, {{x: 0, duration: .04}}], repeat: 2, immediateRender: false}}, {t_ev + .25:.3f});')

# ---- n2 release on the drop: flip it, warp, the prompt ---------------------------------------------------------------------------
t_fl = T("n2", "flip")
head("h2", [[("So", ""), ("flip", "pk"), ("it.", "")], [("Ask", ""), ("it", ""), ("to", ""), ("interview", "lm"), ("you.", "")]], 240, "n2", size=94)
for i, (x, y) in enumerate(SW):
    to(f"#sw{i}", t_fl - .15, .35, f"{{opacity: 0, x: {(x - 420) * 1.8:.0f}, y: {(y - 1010) * 1.8:.0f}, scale: 2}}", "power3.in")
to("#seen", t_fl - .15, .25, "{opacity: 0, scale: 1.8}", "power2.in")
js(f'tl.fromTo("#warp i", {{opacity: 0, scaleX: 0}}, {{keyframes: [{{opacity: 1, scaleX: 1, duration: .35, ease: "power3.out"}}, {{opacity: 0, scaleX: 1.6, duration: .3, ease: "power2.in"}}], '
   f'stagger: {{each: .004, from: "random"}}, immediateRender: false}}, {t_fl - .2:.3f});')
cam(t_fl - .25, 540, 1010, 1.7, .3, "power3.in", rot=180)
cam(t_fl + .05, 540, 1010, 1.0, .5, "power3.out", rot=0)
flash(t_fl + .02, .85, .4)
punch(t_fl + .05, 1.08)
sfx("whoosh_big", t_fl - .25)
sfx("impact", t_fl + .02)
ft("#prompt", t_fl + .25, .5, "{opacity: 0, scale: 1.35, filter: 'blur(24px)'}", "{opacity: 1, scale: 1, filter: 'blur(0px)'}", "power3.out")
typewrite("pw", len(PROMPT_WORDS), t_fl + .55, T0["n2"][1] - .05)
for k in range(10):
    sfx("tick", t_fl + .55 + k * (T0["n2"][1] - t_fl - .6) / 10)
js(f'tl.to("#core", {{opacity: .35, duration: .4}}, {t_fl + .2:.3f});')
js(f'tl.fromTo("#prompt", {{rotationX: 0, rotationY: 0, transformPerspective: 1400}}, {{rotationX: 4, rotationY: -5, duration: 1.6, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {t_fl + .8:.3f});')

# ---- n3 build: questions fly through; each answer fires a star -------------------------------------------------------------------
t_qa = T0["n3"][0]
head("h3", [[("About", ""), ("your", ""), ("life,", "")], [("your", ""), ("skills,", "lm"), ("what", ""), ("you", "")], [("can't", ""), ("stop", ""), ("talking", "pk"), ("about.", "")]],
     210, "n3", size=80)
to("#prompt", t_qa - .25, .3, "{opacity: 0, scale: .6, filter: 'blur(16px)'}", "power2.in")
js(f'tl.to("#core", {{opacity: .25, duration: .4}}, {t_qa - .2:.3f});')
js(f'tl.to("#core", {{opacity: 1, duration: .3}}, {T0["n3"][1]:.3f});')
ft("#qn", t_qa, .3, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "power2.out")
QT = [T("n3", "About") - .1, T("n3", "skills") - .2, T("n3", "can't") - .15, T0["n3"][1] + .1]
for i in range(3):
    tq, nx = QT[i], QT[i + 1]
    ft(f"#qc{i}", tq, .35, "{opacity: 0, scale: .15, filter: 'blur(18px)', y: 260}", "{opacity: 1, scale: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    ft(f"#qa{i}", tq + .4, .25, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2.6)")
    to(f"#qc{i}", nx - .2, .25, "{opacity: 0, scale: 2.4, filter: 'blur(14px)'}", "power2.in")
    to(f"#qa{i}", nx - .2, .2, "{opacity: 0, y: 60}", "power2.in")
    sfx("whoosh", tq)
    sfx("chime", tq + .42)
# ten stars light up and wire together through the build
t_s0, t_s1 = t_qa + .3, T0["n3"][1] + .25
for s in range(10):
    ts = t_s0 + s * (t_s1 - t_s0) / 10
    ft(f"#cs{s}", ts, .3, "{scale: 1, backgroundColor: '#3a3860'}", "{scale: 1.35, backgroundColor: '#ffffff', boxShadow: '0 0 0 4px #CCFB79, 0 0 30px 8px rgba(204,251,121,.9)'}", "back.out(3)")
    st("#qnn", ts, f'{{textContent: "{s + 1}"}}')
    if s:
        ft(f"#ln{s - 1}", ts - .05, .3, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "power2.out")
    sfx("click", ts)
for k in range(9, len(LINKS)):
    ft(f"#ln{k}", t_s1 + .02 * (k - 9), .35, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "power2.out")
cam(t_qa, 540, 1000, 1.06, T0["n3"][1] - t_qa, "sine.inOut")
to("#qn", T0["n3"][1] + .3, .2, "{opacity: 0}")

# ---- n4 peak: the constellation bursts into three niches ---------------------------------------------------------------------------
t_th = T0["n4"][0]
head("h4", [[("Then", ""), ("ask", ""), ("for", ""), ("three", "pk")], [("niches", ""), ("only", ""), ("you", "lm")], [("could", ""), ("own.", "")]], 210, "n4", size=82)
sfx("drumroll", t_th - .1)
js(f'tl.to(".cs", {{x: (i) => [290, 150, -20, -180, -330, -300, -340, -130, 120, 325][i], y: (i) => [190, 320, 265, 330, 200, 0, -190, -290, -260, -90][i], '
   f'duration: .55, ease: "power3.in"}}, {t_th + .2:.3f});')
js(f'tl.to(".lines", {{opacity: 0, duration: .3}}, {t_th + .2:.3f});')
js(f'tl.to("#cg", {{scale: 2.2, duration: .5, ease: "power2.in"}}, {t_th + .25:.3f});')
t_bx = T("n4", "only") - .15
flash(t_bx, .9, .4)
shock(2, t_bx, "#ffffff", 6)
shake(t_bx + .05, 18)
sfx("impact", t_bx)
js(f'tl.to(".cs", {{opacity: 0, duration: .1}}, {t_bx:.3f});')
js(f'tl.to("#core", {{opacity: 0, scale: .3, duration: .2}}, {t_bx:.3f});')
ft("#nlab", t_bx + .05, .3, "{opacity: 0, y: -20}", "{opacity: 1, y: 0}", "power2.out")
for i in range(3):
    tn = t_bx + .08 + i * .22
    ft(f"#nc{i}", tn, .45, "{opacity: 0, scale: .3, y: " + str(1010 - (660 + i * 170) - 70) + ", rotationX: -70, transformPerspective: 1000}",
       "{opacity: 1, scale: 1, y: 0, rotationX: 0}", "back.out(1.5)")
    sfx("stamp2" if i < 2 else "stamp", tn + .1)
    shock(3 if i % 2 else 1, tn + .1, "#ff2f7e" if i == 1 else "#CCFB79", 3.5)
ft("#nex", t_bx + .8, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
for i in range(3):
    js(f'tl.fromTo("#nc{i}", {{y: 0}}, {{y: -8, duration: 1.1, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {t_bx + .7 + i * .15:.3f});')

# ---- n5 release: built from your answers, the fingerprint --------------------------------------------------------------------------
t_bu = T0["n5"][0]
head("h5", [[("Built", ""), ("from", ""), ("your", "")], [("answers.", "lm")], [("Nobody", ""), ("can", ""), ("copy", "pk"), ("that.", "")]], 210, "n5", size=84)
for i in range(3):
    to(f"#nc{i}", t_bu - .2 + i * .05, .3, "{opacity: 0, scale: .4, y: " + str(1000 - (660 + i * 170) - 70) + "}", "power3.in")
to("#nlab", t_bu - .2, .2, "{opacity: 0}")
to("#nex", t_bu - .2, .2, "{opacity: 0}")
for i in range(3):
    tc = t_bu + i * .12
    ft(f"#chp{i}", tc, .3, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2.4)")
    js(f'tl.to("#chp{i}", {{x: {[380, -40, 200][i]}, y: {[-520, -580, -680][i]}, scale: .3, opacity: 0, duration: .45, ease: "power3.in"}}, {tc + .45:.3f});')
    sfx("pop", tc)
st("#fp", t_bu + .1, "{opacity: 1}")
for i in range(13):
    ft(f"#fa{i}", t_bu + .35 + i * .06, .5, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "power2.out")
sfx("riser_short", t_bu + .3)
js(f'tl.fromTo("#fscan", {{opacity: .9, y: 0}}, {{y: 680, duration: .9, ease: "sine.inOut", immediateRender: false}}, {t_bu + .5:.3f});')
st("#fscan", t_bu + 1.45, "{opacity: 0}")
t_nb = T("n5", "Nobody")
ft("#only", t_nb - .05, .3, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "back.out(2.2)")
sfx("chime", t_nb)
js(f'tl.fromTo("#fp", {{scale: 1}}, {{scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut", transformOrigin: "50% 50%", immediateRender: false}}, {t_nb:.3f});')
cam(t_bu, 540, 1010, 1.1, T0["n5"][1] - t_bu + .3, "sine.inOut")

# ---- n6 CTA: into the bright brand frame ------------------------------------------------------------------------------------------
t_cm = T("n6", "Comment")
flash(t_cm - .1, 1, .45)
sfx("whoosh_big", t_cm - .2)
st("#brand", t_cm - .08, "{opacity: 1}")
for s in ("#fp", "#only"):
    st(s, t_cm - .08, "{opacity: 0}")
head("h6", [[("Comment", ""), ("NICHE", "pk")], [("I'll", ""), ("send", ""), ("the", ""), ("exact", ""), ("prompt", "lm")], [("plus", ""), ("five", ""), ("more.", "")]],
     380, "n6", size=72, dark=True)
ft("#blogo", t_cm, .4, "{opacity: 0, y: -30}", "{opacity: 1, y: 0}", "power3.out")
ft("#kw", t_cm + .1, .4, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.2)")
js(f'tl.fromTo("#kw span", {{scale: 1}}, {{scale: 1.05, duration: .35, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}}, {t_cm + .6:.3f});')
sfx("ding", t_cm + .1)
t_pd = T("n6", "exact") - .1
ft("#pdf", t_pd, .55, "{opacity: 0, rotationY: -70, y: 140, transformPerspective: 1200}", "{opacity: 1, rotationY: 0, y: 0}", "back.out(1.5)")
ft("#free", t_pd + .35, .3, "{opacity: 0, scale: 2}", "{opacity: 1, scale: 1}", "back.out(2.5)")
sfx("whoosh", t_pd)
sfx("pop", t_pd + .4)
js(f'tl.fromTo("#pdf", {{rotation: -2}}, {{rotation: 2, duration: 1.1, yoyo: true, repeat: 2, ease: "sine.inOut", immediateRender: false}}, {t_pd + .55:.3f});')
for i in range(CONF):
    x0, dx = random.uniform(0, 1080), random.uniform(-160, 160)
    t0 = t_cm + random.uniform(0, 1.0)
    js(f'tl.fromTo("#cf{i}", {{x: {x0:.0f}, y: -60, rotation: {random.randint(0, 180)}, rotationX: 0, opacity: 1}}, '
       f'{{x: {x0 + dx:.0f}, y: 2000, rotation: {random.randint(360, 900)}, rotationX: {random.choice((540, 720))}, opacity: 1, duration: {random.uniform(2.4, 3.4):.2f}, '
       f'ease: "none", immediateRender: false}}, {t0:.3f});')
sfx("applause", t_cm + .2)

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creators 100X: Make AI interview you 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="punch"><div id="hand">
        <div class="rig" id="rbg" data-layout-allow-overflow>{BG}</div>
        <div class="rig" id="rmid" data-layout-allow-overflow>{MID}</div>
        <div class="rig" id="rw" data-layout-allow-overflow data-layout-allow-overlap>{WORLD}{SHOCKS}</div>
      </div></div>
      <div id="vig"></div>{WARP}
      {PILL}{BIG10}{SWARM}{SEEN}{GBARS}{PROMPT}{QCARDS}{QN}{NCARDS}{FP}{CHIPS}
      {CTA}
      <div id="conf">{CONFH}</div>
      {chr(10).join(HTMLS)}
      <div id="flash"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      tl.progress(1, true).progress(0, true);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "lines": T0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
