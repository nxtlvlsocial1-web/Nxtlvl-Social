"""Creators 100X "Make AI interview you" (keyword NICHE, 9:16): writes index.html, plan/sfx_events.json and plan/edit.json from
plan/words.json.

Script approved by the owner on 2026-11-20 (plan/script.json), voiced with Kokoro af_heart (build/vo_kokoro.py), word times by
build/vo_words.py. An AI game show in the Creators 100X colours (off-white, hot pink, lime, ink):
  n0 hook: lights slam on; a chat box types "what should I post about?"; the AI host spins round: QUESTION 1 OF 10;
  n1 first peak: "give me content ideas" -> a wall of the same ideas everyone gets, stamped SEEN IT, buzzer;
  n2 release: the screen flips to the prompt itself, typed out big enough to screenshot (COPY THIS PROMPT);
  n3 build: question cards flip in, the contestant buzzes, the scoreboard lights up bulb by bulb;
  n4 peak: drumroll, a three-window slot machine spins and lands on three example niches, YOUR NICHE;
  n5 release: the contestant's answers fly into the winning niche; confetti and applause;
  n6 CTA: the scoreboard spells COMMENT NICHE, the free PDF pops up.
The niches are examples (labelled on screen); the prompt works the same in ChatGPT, Gemini or Claude.
python3 build/generate.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT  # noqa: E402
from chibi import DEFS as CHIBI_DEFS, seated  # noqa: E402

random.seed(42)
DUR = round(L1["n6"] + 1.6, 2)
T0 = {k: (L0[k], L1[k]) for k in LINES}

# ---- headlines ----------------------------------------------------------------------------------------------------------------
HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, top, line, size=88, after=0.0):
    spoken, k, out, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
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
            out.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTMLS.append(f'<div class="head" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .05, .3, "{opacity: 0, filter: 'blur(10px)', y: 22}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .25, .18, "{opacity: 0, filter: 'blur(12px)', y: -30}", "power2.in")
    OPEN[0] = hid


# ---- camera ---------------------------------------------------------------------------------------------------------------------
RIGS = (("#rbg", .45), ("#rw", 1.0))


def cam(t, cx, cy, z, d=.8, ease="power3.inOut", setonly=False):
    for sel, f in RIGS:
        zf = 1 + (z - 1) * f
        cxf, cyf = 540 + (cx - 540) * f, 960 + (cy - 960) * f
        props = f"x: {540 - cxf * zf:.1f}, y: {960 - cyf * zf:.1f}, scale: {zf:.4f}"
        js(f'gsap.set("{sel}", {{{props}}});' if setonly else f'tl.to("{sel}", {{{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def pop(sel, t, d=.4, frm="{opacity: 0, scale: .7, y: 40}", ease="back.out(1.8)"):
    ft(sel, t, d, frm, "{opacity: 1, scale: 1, y: 0, rotationY: 0}", ease)


def out(sel, t, d=.25, props="{opacity: 0, scale: .92, y: -30}"):
    to(sel, t, d, props, "power2.in")


def typewrite(prefix, words, t0, t1):
    n = len(words)
    for i in range(n):
        st(f"#{prefix}{i}", t0 + (t1 - t0) * i / max(n - 1, 1), "{opacity: 1}")


# =======================================================================================================================
# THE STUDIO (world rig)
RINGS = "".join(f'<i class="ring" style="width:{r}px;height:{r}px;border-width:{w}px;border-color:{c};opacity:{o}"></i>'
                for r, w, c, o in ((1500, 26, "#CCFB79", .55), (1180, 18, "#FE70B3", .45), (880, 14, "#CCFB79", .6), (620, 10, "#FE70B3", .5)))
GLOWS = ('<i class="glw" style="left:-420px;top:-260px;width:1100px;height:1100px;background:radial-gradient(closest-side,#CEFB8F,rgba(206,251,143,0))"></i>'
         '<i class="glw" style="left:520px;top:-300px;width:1100px;height:1100px;background:radial-gradient(closest-side,#FE70B3,rgba(254,112,179,0));opacity:.7"></i>'
         '<i class="glw" style="left:-460px;top:1100px;width:1000px;height:1000px;background:radial-gradient(closest-side,#FE70B3,rgba(254,112,179,0));opacity:.55"></i>'
         '<i class="glw" style="left:560px;top:1080px;width:1000px;height:1000px;background:radial-gradient(closest-side,#CEFB8F,rgba(206,251,143,0))"></i>')
MARQ = "".join(f'<i id="mq{i}" style="left:{60 + i * 64}px;top:1296px"></i>' for i in range(16))
BG = f'<div class="studio"></div>{GLOWS}<div style="position:absolute;inset:0">{RINGS}</div>'
BEAMS = "".join(f'<i class="beam" id="bm{i}" style="left:{x}px;transform:rotate({r}deg)"></i>' for i, (x, r) in enumerate(((120, -18), (960, 18), (540, 0))))
BULBS = "".join(f'<i class="bl" id="b{i}" style="left:{250 + i * 60}px"></i>' for i in range(10))
BOARD = f'<div class="board"><span class="lbl" id="blbl">Q 0/10</span>{BULBS}<div id="bmsg">COMMENT NICHE</div></div>'
HOST = ('<div id="host"><svg viewBox="0 0 280 370">'
        '<ellipse cx="140" cy="360" rx="110" ry="12" fill="#101111" opacity=".12"/>'
        '<g id="hbody"><path d="M40 40 H240 Q270 40 270 70 V230 Q270 260 240 260 H120 L70 310 L82 260 H40 Q10 260 10 230 V70 Q10 40 40 40 Z" fill="#101111"/>'
        '<path d="M44 52 H236 Q258 52 258 74 V112 Q140 92 22 118 V74 Q22 52 44 52 Z" fill="#fff" opacity=".12"/>'
        '<g id="heyes"><ellipse cx="102" cy="140" rx="20" ry="26" fill="#CCFB79"/><ellipse cx="178" cy="140" rx="20" ry="26" fill="#CCFB79"/>'
        '<circle cx="108" cy="132" r="7" fill="#fff"/><circle cx="184" cy="132" r="7" fill="#fff"/></g>'
        '<path id="hmouth" d="M108 196 Q140 226 172 196" stroke="#CCFB79" stroke-width="10" fill="none" stroke-linecap="round"/>'
        '<path id="hmouth2" d="M104 190 Q140 238 176 190 Z" fill="#CCFB79" opacity="0"/>'
        '<g id="hmic"><path d="M262 170 Q300 160 296 120" stroke="#101111" stroke-width="16" fill="none" stroke-linecap="round"/>'
        '<rect x="284" y="70" width="26" height="54" rx="13" fill="#FD0B68"/><rect x="290" y="118" width="14" height="22" fill="#101111"/></g></g></svg></div>')
PODS = ('<div class="pod" style="left:110px"><img src="assets/img/logo-mark.png" alt=""><b>A<em>I</em></b></div>'
        '<div class="pod" style="left:630px"><img src="assets/img/logo-mark.png" alt=""><b>YOU</b></div><i class="buzz" id="buzz"></i>')
CONT = '<div id="cont">' + seated("cb0", 660, 1140, 280, turn=True, phone=False) + '</div>'
WORLD = (f'{CHIBI_DEFS}<div class="floor"></div><i class="reflect"></i>{BEAMS}<div class="bulbrow">{MARQ}</div>{BOARD}'
         f'{CONT}{HOST}{PODS}')

# overlays (screen space)
Q_ME = "what should I post about?".split()
CHAT = ('<div class="ov chat" id="chat"><div class="bar"><i></i>AI chat</div>'
        '<div class="bub me" id="me" style="top:130px">' + " ".join(f'<span class="pw" id="cw{i}">{w}</span>' for i, w in enumerate(Q_ME)) + '<i class="caret"></i></div>'
        '<div class="bub ai" id="ai1" style="top:250px;width:640px">Before I answer, let me ask you 10 questions.</div>'
        '<div class="bub me" id="me2" style="top:130px">give me content ideas</div></div>')
QBIG = '<div class="ov qbig" id="qbig"><small>QUESTION 1 OF 10</small><b>Let\'s find out who you are.</b></div>'
IDEAS = ["Day in my life", "5 tips for…", "Morning routine", "What I eat in a day", "Get ready with me", "Q&amp;A time", "My desk setup", "Study with me", "Week in my life"]
WALL = '<div class="ov wall" id="wall">' + "".join(f'<div class="idea" id="id{i}" style="left:{(i % 3) * 324}px;top:{(i // 3) * 180}px"><i></i>{t}</div>'
                                                  for i, t in enumerate(IDEAS)) + '<div class="stamp" id="seen">SEEN IT</div></div>'
PROMPT_WORDS = [("Ask", 1), ("me", 1), ("10", 1), ("questions", 1), ("about", 0), ("my", 0), ("life,", 0), ("my", 0), ("skills", 0), ("and", 0), ("what", 0), ("I", 0),
                ("can't", 0), ("stop", 0), ("talking", 0), ("about.", 0), ("One", 1), ("question", 1), ("at", 1), ("a", 1), ("time,", 1), ("and", 0), ("wait", 0),
                ("for", 0), ("my", 0), ("answer.", 0), ("Then", 0), ("suggest", 0), ("3", 1), ("niches", 1), ("only", 1), ("I", 1), ("could", 1), ("own,", 1),
                ("with", 0), ("5", 0), ("reel", 0), ("ideas", 0), ("for", 0), ("each.", 0)]
PTXT = " ".join(f'<span class="pw{" mk" if m else ""}" id="pw{i}">{w}</span>' for i, (w, m) in enumerate(PROMPT_WORDS))
PROMPT = f'<div class="ov prompt" id="prompt"><div class="pill">COPY THIS PROMPT</div><div class="ptxt">{PTXT}</div></div>'
QS = [("Q 1/10", "What do friends always ask you for help with?", "cooking on a budget"),
      ("Q 4/10", "What could you talk about for an hour?", "hostel life hacks"),
      ("Q 7/10", "What did you learn the hard way?", "eating well when broke")]
QCARDS = "".join(f'<div class="ov qc" id="qc{i}"><small>{a}</small><b>{q}</b><u id="qa{i}">"{ans}"</u></div>' for i, (a, q, ans) in enumerate(QS))
NICHES = ["Budget meals for hostel students", "Gym tips for skinny beginners", "Aesthetic exam notes"]
FILL = ["Day in my life", "Travel vlogs", "Tech reviews", "Morning routine", "Book reviews", "Fitness tips", "Cooking hacks", "Study with me"]
SLOT = '<div class="ov slot" id="slot"><div class="lab">YOUR 3 NICHES</div>'
for w, niche in enumerate(NICHES):
    labels = random.sample(FILL, 6) + [niche]
    SLOT += (f'<div class="win" style="top:{100 + w * 148}px"><div class="strip" id="sp{w}">' + "".join(f"<p>{x}</p>" for x in labels) + '</div></div>')
SLOT += "".join(f'<i class="sl" style="left:{x}px;top:{y}px"></i>' for x, y in [(20 + i * 75, 14) for i in range(12)] + [(20 + i * 75, 528) for i in range(12)])
SLOT += '<div class="ex">EXAMPLES</div><div class="ystamp" id="ystamp">YOUR NICHE</div></div>'
CHIPS = "".join(f'<div class="chip" id="chp{i}" style="left:{x}px;top:{y}px">{t}</div>' for i, (t, x, y) in enumerate(
    (("cooking on a budget", 90, 1380), ("hostel life hacks", 560, 1440), ("eating well when broke", 200, 1530))))
PDF = ('<div class="ov pdf" id="pdf"><img src="assets/img/logo.png" alt=""><span class="k">FREE PROMPT PACK</span>'
       '<h3>Let AI <span>interview</span> you</h3><p>The prompt + 5 more to plan your first 10 reels.</p></div><div class="ov free" id="free">FREE PDF</div>')
COLS = ("#CCFB79", "#FD0B68", "#101111", "#FE70B3", "#ffffff", "#CEFB8F")
CONF = 70
CONFH = "".join(f'<i class="cf" id="cf{i}" style="background:{random.choice(COLS)};width:{random.randint(12, 20)}px;height:{random.randint(22, 34)}px"></i>' for i in range(CONF))

# =======================================================================================================================
# TIMELINE
cam(0, 540, 1000, 1.08, setonly=True)
js('tl.fromTo("#hand", {x: -3, y: 2}, {x: 3, y: -2, duration: 3.2, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false}, 0);')
js(f'tl.fromTo("#hbody", {{y: 0}}, {{y: -10, duration: .9, yoyo: true, repeat: {int(DUR / .9)}, ease: "sine.inOut", immediateRender: false}}, 0);')
for k in range(int(DUR / 2.6)):
    js(f'tl.fromTo("#heyes", {{scaleY: 1}}, {{scaleY: .1, duration: .07, yoyo: true, repeat: 1, transformOrigin: "50% 50%", immediateRender: false}}, {1.3 + k * 2.6:.2f});')
js(f'tl.to("#rbg .ring", {{rotation: "+=30", duration: {DUR}, ease: "none"}}, 0);')
for i in range(16):
    js(f'tl.fromTo("#mq{i}", {{backgroundColor: "#e9dcdf"}}, {{backgroundColor: "{"#CCFB79" if i % 2 else "#FD0B68"}", duration: .2, yoyo: true, repeat: {int(DUR / .4)}, '
       f'immediateRender: false}}, {(i % 2) * .2:.2f});')

# ---- n0 hook: lights slam on; the chat; the host spins round ---------------------------------------------------------------------
to("#dark", .05, .12, "{opacity: 0}", "power4.in")
sfx("clunk", .04)
for i in range(3):
    ft(f"#bm{i}", .05 + i * .06, .15, "{opacity: 0}", "{opacity: 1}", "power4.in")
head("h0", [[("I", ""), ("asked", ""), ("ChatGPT", "")], [("what", ""), ("I", ""), ("should", ""), ("post", "pk"), ("about.", "")]], 250, "n0", size=90)
pop("#chat", .2, .45)
pop("#me", .5, .25, "{opacity: 0, scale: .8, x: 30}")
typewrite("cw", Q_ME, T("n0", "what") - .05, T("n0", "about") + .1)
sfx("click", T("n0", "what"))
cam(.2, 540, 960, 1.0, 2.2, "sine.inOut")
t_ab = T("n0", "asked", 1)
js(f'tl.fromTo("#host", {{rotationY: 0}}, {{rotationY: 360, duration: .5, ease: "power2.inOut", immediateRender: false}}, {t_ab - .1:.3f});')
st("#hmouth", t_ab, "{opacity: 0}")
st("#hmouth2", t_ab, "{opacity: 1}")
pop("#ai1", t_ab, .3, "{opacity: 0, scale: .8, x: -30}")
sfx("whoosh", t_ab - .1)
t_q = T("n0", "ten")
out("#chat", t_q - .1, .2)
ft("#qbig", t_q - .05, .45, "{opacity: 0, rotationX: -90, transformPerspective: 900}", "{opacity: 1, rotationX: 0}", "back.out(1.6)")
sfx("quiz", t_q)
st("#blbl", t_q, '{textContent: "Q 1/10"}')

# ---- n1 first peak: the same ideas everyone gets -------------------------------------------------------------------------------
t_gv = T("n1", "Give")
head("h1", [[("\"Give", ""), ("me", ""), ("content", ""), ("ideas\"", "")], [("gets", ""), ("the", ""), ("same", "pk"), ("ideas", "")], [("as", ""), ("everyone", ""), ("else.", "")]],
     230, "n1", size=80)
out("#qbig", t_gv - .2, .2)
pop("#chat", t_gv - .15, .3)
st("#ai1", t_gv - .15, "{opacity: 0}")
st("#me", t_gv - .15, "{opacity: 0}")
pop("#me2", t_gv, .3, "{opacity: 0, scale: .8, x: 30}")
sfx("click", t_gv)
t_sm = T("n1", "gets")
out("#chat", t_sm - .2, .2)
for i in range(9):
    pop(f"#id{i}", t_sm - .1 + i * .06, .3, "{opacity: 0, scale: .5, y: 60}")
    if i % 3 == 0:
        sfx("pop", t_sm + i * .06)
pop("#wall", t_sm - .15, .01, "{opacity: 0}")
t_ev = T("n1", "everyone")
ft("#seen", t_ev - .05, .22, "{opacity: 0, scale: 2.4}", "{opacity: 1, scale: 1}", "power4.in")
sfx("buzzer", t_ev)
js(f'tl.fromTo("#punch", {{x: 0}}, {{keyframes: [{{x: -14, duration: .05}}, {{x: 12, duration: .05}}, {{x: -8, duration: .05}}, {{x: 0, duration: .05}}], immediateRender: false}}, {t_ev + .15:.3f});')
js(f'tl.fromTo("#host", {{rotation: 0}}, {{keyframes: [{{rotation: -8, duration: .12}}, {{rotation: 8, duration: .12}}, {{rotation: -5, duration: .12}}, {{rotation: 0, duration: .12}}], '
   f'transformOrigin: "50% 100%", immediateRender: false}}, {t_ev + .2:.3f});')

# ---- n2 release: flip it, the prompt ----------------------------------------------------------------------------------------------
t_fl = T("n2", "flip")
head("h2", [[("So", ""), ("flip", "pk"), ("it.", "")], [("Ask", ""), ("it", ""), ("to", ""), ("interview", "lm"), ("you.", "")]], 250, "n2", size=92)
js(f'tl.to("#wall", {{rotationY: 90, opacity: 0, duration: .3, ease: "power2.in", transformPerspective: 1200}}, {t_fl - .1:.3f});')
ft("#prompt", t_fl + .2, .4, "{opacity: 0, rotationY: -90, transformPerspective: 1200}", "{opacity: 1, rotationY: 0}", "power3.out")
sfx("whoosh_big", t_fl - .1)
typewrite("pw", PROMPT_WORDS, t_fl + .5, T0["n2"][1] - .05)
for k in range(8):
    sfx("tick", t_fl + .5 + k * (T0["n2"][1] - t_fl - .55) / 8)
cam(t_fl, 540, 980, 1.04, 3.5, "sine.inOut")

# ---- n3 build: the questions, the buzzer, the scoreboard ----------------------------------------------------------------------------
t_qa = T0["n3"][0]
head("h3", [[("About", ""), ("your", ""), ("life,", "")], [("your", ""), ("skills,", "lm"), ("what", ""), ("you", "")], [("can't", ""), ("stop", ""), ("talking", "pk"), ("about.", "")]],
     220, "n3", size=78)
out("#prompt", t_qa - .2, .25)
QT = [T("n3", "About") - .05, T("n3", "skills") - .15, T("n3", "can't") - .1]
for i, tq in enumerate(QT):
    ft(f"#qc{i}", tq, .35, "{opacity: 0, rotationX: -90, transformPerspective: 900}", "{opacity: 1, rotationX: 0}", "back.out(1.5)")
    sfx("quiz" if i == 0 else "flip", tq)
    ft(f"#qa{i}", tq + .45, .25, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.6)")
    js(f'tl.fromTo("#buzz", {{scaleY: 1}}, {{scaleY: .55, duration: .07, yoyo: true, repeat: 1, transformOrigin: "50% 100%", immediateRender: false}}, {tq + .35:.3f});')
    sfx("chime", tq + .45)
    if i < 2:
        out(f"#qc{i}", QT[i + 1] - .12, .14, "{opacity: 0, rotationX: 90}")
for b in range(10):
    tb = t_qa + .2 + b * (T0["n3"][1] - t_qa) / 10
    st(f"#b{b}", tb, '{backgroundColor: "#CCFB79", boxShadow: "0 0 16px rgba(204,251,121,.95)"}')
    st("#blbl", tb, f'{{textContent: "Q {b + 1}/10"}}')
    sfx("click", tb)
js(f'tl.to("#cb0 .cbs", {{"--arms": 1, duration: .15}}, {QT[0] + .35:.3f});')
js(f'tl.to("#cb0 .cbs", {{"--arms": 0, duration: .15}}, {QT[0] + .9:.3f});')
js(f'tl.fromTo("#cb0 .cbs", {{y: 0}}, {{y: -14, duration: .14, yoyo: true, repeat: 5, ease: "power1.out", immediateRender: false}}, {QT[1] + .3:.3f});')

# ---- n4 peak: drumroll, the slot machine -----------------------------------------------------------------------------------------
t_th = T0["n4"][0]
head("h4", [[("Then", ""), ("ask", ""), ("for", ""), ("three", "pk")], [("niches", ""), ("only", ""), ("you", "lm")], [("could", ""), ("own.", "")]], 220, "n4", size=82)
out("#qc2", t_th - .2, .2)
pop("#slot", t_th - .1, .4, "{opacity: 0, scale: .6, y: 120}")
sfx("drumroll", t_th)
sfx("slotspin", t_th + .3)
STOPS = [T("n4", "only") - .1, T("n4", "could") - .05, T("n4", "own") + .25]
for w, ts in enumerate(STOPS):
    js(f'tl.fromTo("#sp{w}", {{y: 0, filter: "blur(0px)"}}, {{keyframes: [{{filter: "blur(5px)", duration: .1}}, {{y: -{130 * 6}, duration: {ts - t_th - .3:.2f}, ease: "power1.inOut"}}, '
       f'{{filter: "blur(0px)", duration: .08}}], immediateRender: false}}, {t_th + .2:.3f});')
    sfx("clunk", ts)
t_ys = STOPS[2] + .25
ft("#ystamp", t_ys, .22, "{opacity: 0, scale: 2.4}", "{opacity: 1, scale: 1}", "power4.in")
sfx("stamp", t_ys)
st("#flash", t_ys, "{opacity: .35}")
to("#flash", t_ys + .02, .3, "{opacity: 0}")

# ---- n5 release: built from your answers; confetti ---------------------------------------------------------------------------------
t_bu = T0["n5"][0]
head("h5", [[("Built", ""), ("from", ""), ("your", "")], [("answers.", "lm")], [("Nobody", ""), ("can", ""), ("copy", "pk"), ("that.", "")]], 230, "n5", size=82)
for i in range(3):
    tc = t_bu + .05 + i * .15
    pop(f"#chp{i}", tc, .3, "{opacity: 0, scale: .5, y: 40}")
    js(f'tl.to("#chp{i}", {{x: {[300, -120, 220][i]}, y: {[-580, -640, -730][i]}, scale: .4, opacity: 0, duration: .45, ease: "power3.in"}}, {tc + .55:.3f});')
    sfx("pop", tc)
t_glow = t_bu + 1.25
js(f'tl.to("#slot", {{boxShadow: "0 30px 70px rgba(16,17,17,.32), 0 0 0 14px #CCFB79", duration: .3}}, {t_glow:.3f});')
js(f'tl.fromTo("#slot", {{scale: 1}}, {{scale: 1.05, duration: .2, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_glow:.3f});')
sfx("chime", t_glow)
t_nb = T("n5", "Nobody")
for i in range(CONF):
    x0, dx = random.uniform(0, 1080), random.uniform(-160, 160)
    t0 = t_nb - .2 + random.uniform(0, 1.2)
    js(f'tl.fromTo("#cf{i}", {{x: {x0:.0f}, y: -60, rotation: {random.randint(0, 180)}, rotationX: 0, opacity: 1}}, '
       f'{{x: {x0 + dx:.0f}, y: 2000, rotation: {random.randint(360, 900)}, rotationX: {random.choice((540, 720))}, opacity: 1, duration: {random.uniform(2.4, 3.6):.2f}, '
       f'ease: "none", immediateRender: false}}, {t0:.3f});')
sfx("applause", t_nb - .2)
js(f'tl.to("#cb0 .cbs", {{"--arms": 1, duration: .15}}, {t_nb - .2:.3f});')
js(f'tl.fromTo("#cb0 .cbs", {{y: 0}}, {{y: -18, duration: .2, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false}}, {t_nb - .1:.3f});')
js(f'tl.fromTo("#host", {{y: 0}}, {{y: -26, duration: .22, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}}, {t_nb:.3f});')

# ---- n6 CTA: COMMENT NICHE on the board, the free PDF -----------------------------------------------------------------------------
t_cm = T("n6", "Comment")
head("h6", [[("Comment", ""), ("NICHE", "pk")], [("I'll", ""), ("send", ""), ("the", ""), ("exact", ""), ("prompt", "lm")], [("plus", ""), ("five", ""), ("more.", "")]], 215, "n6", size=80)
out("#slot", t_cm - .25, .25)
st("#blbl", t_cm - .1, "{opacity: 0}")
js(f'tl.to(".board .bl", {{opacity: 0, duration: .15}}, {t_cm - .1:.3f});')
ft("#bmsg", t_cm, .3, "{opacity: 0, scale: 1.4}", "{opacity: 1, scale: 1}", "back.out(2)")
js(f'tl.fromTo("#bmsg", {{opacity: 1}}, {{opacity: .55, duration: .18, yoyo: true, repeat: 7, immediateRender: false}}, {t_cm + .6:.3f});')
sfx("quiz", t_cm)
t_pd = T("n6", "exact") - .1
ft("#pdf", t_pd, .5, "{opacity: 0, rotationY: -60, y: 120, transformPerspective: 1200}", "{opacity: 1, rotationY: 0, y: 0}", "back.out(1.5)")
ft("#free", t_pd + .35, .3, "{opacity: 0, scale: 2}", "{opacity: 1, scale: 1}", "back.out(2.5)")
sfx("whoosh", t_pd)
sfx("ding", t_pd + .4)
js(f'tl.fromTo("#pdf", {{rotation: -2}}, {{rotation: 2, duration: 1.2, yoyo: true, repeat: 2, ease: "sine.inOut", immediateRender: false}}, {t_pd + .5:.3f});')
st("#hmouth", t_cm, "{opacity: 1}")
st("#hmouth2", t_cm, "{opacity: 0}")
js(f'tl.to("#hmic", {{rotation: -25, svgOrigin: "262 170", duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {t_cm:.3f});')

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
        <div class="rig" id="rw" data-layout-allow-overflow data-layout-allow-overlap>{WORLD}</div>
      </div></div>
      {CHAT}{QBIG}{WALL}{PROMPT}{QCARDS}{SLOT}{CHIPS}{PDF}
      <div id="conf">{CONFH}</div>
      {chr(10).join(HTMLS)}
      <div id="dark"></div><div id="flash"></div><div id="grain"></div>
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
