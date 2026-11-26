"""Creators 100X x Creedom "Stop using ChatGPT for your reels" (9:16), v2: writes index.html, plan/sfx_events.json, plan/edit.json.
v2 (owner: "remove the background song and also remove this mobile phone concept ... add different animations to display how
creedom is better then chatgpt"): no phone; every beat gets its own full-frame animation. ChatGPT scenes are plain grey with
OpenAI's logo as a label only (never defaced); Creedom scenes flood pink and show the real thing.
  hook   VS split (ChatGPT vs Cree), a STOP stamp, the scoreboard
  r1     a wheel of generic tips spins and lands on a guess; the reel sits behind a NOT SEEN curtain   -> NEVER SAW YOUR REEL
  c1     a film strip of the reel scrolls past a playhead; the retention line drops at 0:03, viewers fall off; the fix
  r2     identical grey idea cards and a faceless profile                                                -> DOESN'T KNOW YOUR ACCOUNT
  c2     your profile grid is scanned, the most-saved tiles glow, "post this next" flies into the grid
  r3     "Looks great!" next to a play counter stuck at 0:00                                              -> HASN'T WATCHED IT
  c3     a gauge sweeps to 3.8 / 5, score chips pop, the fix, POST gets pressed
  end    ChatGPT writes a script (great for writing); Creedom = your Instagram coach, CREEDOM WINS 3 : 0; GROW comment box
Replies, scores and timestamps are illustrations, labelled EXAMPLE. Cree reacts throughout. phone version: generate_phone_v1.py
python3 build/generate.py"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import ROOT, LINES, L0, L1, T, JS, SFX, js, sfx, ft, to, st  # noqa: E402
from fx import cree_html, pose, cree_hop, sparkle, P, sweat, say, cree_wiggle, blink, PCX, PCY, cree_to  # noqa: E402

random.seed(21)
DUR = round(L1["v6"] + 1.3, 2)
HTMLS, OPEN, WID = [], [None], [0]
FIRST = {}


def ft2(sel, t, d, frm, to_, ease="power3.out"):
    ft(sel, t, d, frm, to_, ease)
    if "opacity: 0" in frm and (sel not in FIRST or t < FIRST[sel][0]):
        FIRST[sel] = (t, frm)


def pop(sel, t, d=.32, frm="{opacity: 0, scale: .4}", ease="back.out(2.4)"):
    ft2(sel, t, d, frm, "{opacity: 1, scale: 1, rotation: 0}", ease)


def head(hid, rows, line, size=78, after=0.0):
    spoken, k, out_, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
    for row in rows:
        ws = []
        for word in row:
            cls = "pk" if word.startswith("*") else ("gr" if word.startswith("~") else "")
            word = word.lstrip("*~")
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?\""), None
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
    HTMLS.append(f'<div class="head" id="{hid}" style="font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out_:
        ft2(f"#{wid}", t - .05, .28, "{opacity: 0, filter: 'blur(10px)', y: 24}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out_)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .2, .15, "{opacity: 0, filter: 'blur(12px)', y: -30}", "power2.in")
    OPEN[0] = hid


def flash(t, o=.55, d=.28):
    st("#flash", t, f"{{opacity: {o}}}")
    to("#flash", t + .02, d, "{opacity: 0}", "power2.out")


def punch(t, k=1.04):
    js(f'tl.fromTo("#stage", {{scale: 1}}, {{scale: {k}, duration: .1, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t:.3f});')


SCENES = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]


def scene(sid, t, side):
    """cut to a scene: side 'g' (grey ChatGPT room) or 'c' (Creedom pink)"""
    for s in SCENES:
        if s != sid:
            st(f"#{s}", t, "{opacity: 0}")
    ft2(f"#{sid}", t, .3, "{opacity: 0, scale: 1.08}", "{opacity: 1, scale: 1}", "power3.out")
    st("#bgg", t, f"{{opacity: {1 if side == 'g' else 0}}}")
    if side == "c":
        flash(t, .45, .3)
        js(f'tl.fromTo("#wipe", {{clipPath: "circle(0% at 85% 92%)", opacity: 1}}, {{clipPath: "circle(150% at 85% 92%)", duration: .4, ease: "power3.out", immediateRender: false}}, {t - .05:.3f});')
        st("#wipe", t + .4, "{opacity: 0}")
        sfx("whoosh_big", t - .05)
    else:
        sfx("swish", t)


def stamp(sid, text, t):
    HTMLS.append(f'<div class="stamp" id="{sid}"><span>{text}</span></div>')
    ft2(f"#{sid}", t, .22, "{opacity: 0, scale: 2.4, rotation: -20}", "{opacity: 1, scale: 1, rotation: -7}", "power4.out")
    sfx("stamp", t + .04)
    punch(t + .04, 1.035)
    return sid


LOGO = '<img class="glogo" src="assets/img/chatgpt_logo.png" alt="">'
GBADGE = f'<div class="badge g">{LOGO}<b>ChatGPT</b></div>'
CBADGE = '<div class="badge c"><img src="assets/img/creedom_logo.png" alt=""><em>EXAMPLE</em></div>'

# ---------------------------------------------------------------- times
t_stop, t_gpt0, t_why = L0["v0"], T("v0", "ChatGPT"), T("v0", "Here's")
r1 = dict(t=L0["v1"], guess=T("v1", "guesses"), never=T("v1", "never"), seen=T("v1", "seen"))
c1 = dict(t=L0["v2"], sec=T("v2", "second"), where=T("v2", "where"), leave=T("v2", "leave"))
r2 = dict(t=L0["v3"], know=T("v3", "doesn't"), acct=T("v3", "account"))
c2 = dict(t=T("v3", "Creedom"), reads=T("v3", "reads"), tells=T("v3", "tells"))
r3 = dict(t=L0["v4"], post=T("v4", "post"), hasnt=T("v4", "hasn't"), watched=T("v4", "watched"))
c3 = dict(t=T("v4", "Creedom"), scores=T("v4", "scores"), before=T("v4", "before"), hit=T("v4", "hit"))
t_writer, t_great, t_coach, t_coachw = L0["v5"], T("v5", "great"), T("v5", "Creedom"), T("v5", "coach")
t_cm, t_g = L0["v6"], T("v6", "GROW")

# ---------------------------------------------------------------- headlines
head("h0", [["*Stop", "using", "~ChatGPT"], ["for", "your", "reels."]], "v0", 92)
head("h0b", [["Here's", "*why."]], "v0", 110, after=t_why)
head("h1", [["Ask", "it", "why", "your"], ["reel", "flopped,", "and", "it"], ["*guesses."]], "v1", 80)
head("h1b", [["It's", "*never", "*seen"], ["your", "reel."]], "v1", 92, after=r1["never"] - .25)
head("h2", [["*Creedom", "watches", "it,"], ["second", "by", "second,"]], "v2", 84)
head("h2b", [["and", "shows", "you", "where"], ["people", "*leave."]], "v2", 84, after=T("v2", "and"))
head("h3", [["Ask", "it", "what", "to", "post", "next."], ["It", "doesn't", "know"], ["your", "*account."]], "v3", 76)
head("h3b", [["*Creedom", "reads", "your", "page,"], ["and", "tells", "you."]], "v3", 84, after=c2["t"])
head("h4", [["Ask", "if", "your", "reel"], ["is", "ready", "to", "post."], ["It", "*hasn't", "*watched", "it."]], "v4", 76)
head("h4b", [["*Creedom", "scores", "it,"], ["before", "you", "hit", "post."]], "v4", 84, after=c3["t"])
head("h5", [["~ChatGPT", "is", "a"], ["great", "writer."]], "v5", 88)
head("h5b", [["*Creedom", "is", "your"], ["Instagram", "*coach."]], "v5", 92, after=t_coach)
head("h6", [["Comment", "*GROW"], ["and", "I'll", "send", "you", "Creedom."]], "v6", 84)

# =====================================================================================================================
# s0: the VS split
S0 = ('<div class="scene" id="s0"><div class="half l" id="hl"><div class="lcirc" id="lc">' + LOGO + '</div><b>ChatGPT</b></div>'
      '<div class="half r" id="hr"><b>Creedom</b></div><div class="vs" id="vs">VS</div></div>')
scene("s0", 0, "g")
js('gsap.set("#bgg", {opacity: 0});')
ft2("#hl", 0, .45, "{opacity: 0, x: -540}", "{opacity: 1, x: 0}", "power4.out")
ft2("#hr", .05, .45, "{opacity: 0, x: 540}", "{opacity: 1, x: 0}", "power4.out")
pop("#vs", .35, .4, "{opacity: 0, scale: 3, rotation: -30}")
sfx("whoosh_big", 0); sfx("impact", .38)
HTMLS.append('<div class="stamp big" id="stopst"><span>STOP</span></div>')
ft2("#stopst", t_stop + .55, .22, "{opacity: 0, scale: 2.6, rotation: -24}", "{opacity: 1, scale: 1, rotation: -10}", "power4.out")
sfx("stamp", t_stop + .6); punch(t_stop + .6, 1.05)
to("#stopst", t_why - .2, .2, "{opacity: 0, scale: .8}", "power2.in")
js(f'tl.fromTo("#vs", {{rotation: -6}}, {{rotation: 6, duration: .25, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false}}, .8);')

# scoreboard
SCORE = ('<div id="score"><span class="sg">' + LOGO + '<b>ChatGPT</b><em>0</em></span><i>:</i>'
         '<span class="scc"><em>' + "".join(f'<u id="sn{k}">{k}</u>' for k in range(4)) + '</em><b>Creedom</b></span><div class="win" id="win">CREEDOM WINS</div></div>')
pop("#score", t_why, .35, "{opacity: 0, scale: .5, y: -20}")
sfx("ding2", t_why)

# =====================================================================================================================
# s1: the guess wheel + the reel it never saw
TIPS = ["Stronger hook", "Trending audio", "Post at 6 PM", "More hashtags", "Be consistent", "Add captions"]
segs, labels = "", ""
for k, tip in enumerate(TIPS):
    a0, a1 = math.radians(k * 60 - 90), math.radians(k * 60 - 30)
    x0, y0, x1, y1 = 300 + 290 * math.cos(a0), 300 + 290 * math.sin(a0), 300 + 290 * math.cos(a1), 300 + 290 * math.sin(a1)
    segs += f'<path d="M300,300 L{x0:.1f},{y0:.1f} A290,290 0 0 1 {x1:.1f},{y1:.1f} Z" fill="{("#d9dae0", "#c6c7cf", "#e6e7ec")[k % 3]}" stroke="#fff" stroke-width="6"/>'
    am = k * 60 - 60                                   # the segment's centre line
    rot = am + (180 if math.cos(math.radians(am - 90)) < 0 else 0)   # radial text, kept upright where the wheel stops
    cx, cy = 300 + 172 * math.cos(math.radians(am)), 300 + 172 * math.sin(math.radians(am))
    labels += (f'<text x="{cx:.1f}" y="{cy:.1f}" transform="rotate({rot} {cx:.1f} {cy:.1f})" text-anchor="middle" dominant-baseline="middle" '
               f'font-family="Inter" font-weight="800" font-size="28" fill="#4a4a55">{tip}</text>')
S1 = (f'<div class="scene" id="s1">{GBADGE}<div class="wheelw"><svg id="wheel" viewBox="0 0 600 600">{segs}{labels}<circle cx="300" cy="300" r="46" fill="#fff" stroke="#c6c7cf" stroke-width="6"/></svg>'
      '<i class="pin"></i></div><div class="gtag" id="gtag">A GUESS</div>'
      '<div class="rcard" id="rc1"><div class="thumb"><i></i><b>Your reel</b></div><div class="curt" id="curt"><span>NOT SEEN</span></div></div></div>')
scene("s1", r1["t"] - .1, "g")
js('gsap.set("#wheel", {transformOrigin: "50% 50%"});')
# lands with "Trending audio" (segment 1, centre line at 0 deg) right under the pin at the top: rotate -> 360*4 - 90
js(f'tl.fromTo("#wheel", {{rotation: 0}}, {{rotation: {360 * 4 - 90}, duration: {r1["guess"] - r1["t"] + .25:.2f}, ease: "power3.out", immediateRender: false}}, {r1["t"] + .05:.3f});')
for k in range(10):
    sfx("tick", r1["t"] + .05 + k * .07 * (1 + k * .18))
pop("#gtag", r1["guess"] + .2, .35, "{opacity: 0, scale: .4, rotation: 10}")
sfx("error", r1["guess"] + .2)
js(f'tl.to(".wheelw", {{x: -230, scale: .62, duration: .45, ease: "power3.inOut"}}, {r1["never"] - .3:.3f});')
to("#gtag", r1["never"] - .3, .2, "{opacity: 0}")
ft2("#rc1", r1["never"] - .15, .45, "{opacity: 0, x: 400, rotation: 10}", "{opacity: 1, x: 0, rotation: 3}", "back.out(1.6)")
ft2("#curt", r1["seen"], .3, "{opacity: 0, scaleY: 0}", "{opacity: 1, scaleY: 1}", "power3.out")
sfx("close", r1["seen"])
stamp("stp1", "NEVER SAW YOUR REEL", r1["seen"] + .3)
to("#stp1", c1["t"] - .2, .15, "{opacity: 0}")

# =====================================================================================================================
# s2: the film strip + retention line, people leave at 0:03
FR = "".join(f'<div class="fr" style="background:{("#ff9ec9", "#ffb3d6", "#ff8ac2", "#ffc6e0")[k % 4]}"><i></i><span>0:{k:02d}</span></div>' for k in range(12))
DOTS = "".join(f'<i class="vd" id="vd{k}" style="left:{random.randint(120, 300)}px;top:{random.randint(20, 70)}px"></i>' for k in range(14))
S2 = (f'<div class="scene" id="s2">{CBADGE}<div class="strip"><div class="film" id="film">{FR}</div><i class="playhead"></i></div>'
      '<div class="retw"><svg viewBox="0 0 900 360" class="ret"><line x1="0" y1="340" x2="900" y2="340" stroke="#e9c3d6" stroke-width="3"/>'
      '<path id="rline" d="M0 30 L250 36 C285 40 300 250 340 270 C460 300 700 306 900 312" fill="none" stroke="#F343A2" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/>'
      '<circle id="rdot" cx="300" cy="150" r="18" fill="#ff3b4e"/></svg>' + DOTS +
      '<div class="leave" id="leave"><small>0:03</small>PEOPLE LEAVE HERE</div></div>'
      '<div class="fixc" id="fix1"><small>THE FIX</small>Open on the finished dish.</div></div>')
scene("s2", c1["t"] - .05, "c")
js(f'tl.fromTo("#film", {{x: 0}}, {{x: -1300, duration: {c1["where"] - c1["t"] + .2:.2f}, ease: "none", immediateRender: false}}, {c1["t"]:.3f});')
ft2("#rline", c1["sec"] - .2, c1["where"] - c1["sec"] + .3, "{strokeDashoffset: 1, opacity: 0}", "{strokeDashoffset: 0, opacity: 1}", "none")
pop("#rdot", c1["where"] - .05, .3)
for k in range(14):
    ft2(f"#vd{k}", c1["where"] + k * .03, .7, "{opacity: 1, y: 0}", "{opacity: 0, y: 340, rotation: 160}", "power2.in")
js(f'gsap.set(".vd", {{opacity: 0}}); tl.set(".vd", {{opacity: 1}}, {c1["sec"]:.3f});')
pop("#leave", c1["where"], .35, "{opacity: 0, scale: .5, y: 20}")
sfx("error", c1["where"]); sfx("swish", c1["where"] + .1)
pop("#fix1", c1["leave"] + .1, .4, "{opacity: 0, scale: .6, y: 40}")
sfx("ding", c1["leave"] + .1)
for k in range(6):
    sfx("tick", c1["sec"] + k * .2)

# =====================================================================================================================
# s3: identical generic ideas + a faceless profile
IDEAS = ["Day in my life", "Morning routine", "GRWM", "Top 5 tips", "Q&A", "Behind the scenes"]
S3 = (f'<div class="scene" id="s3">{GBADGE}<div class="ideas">' + "".join(f'<div class="idea" id="id{k}">{s}</div>' for k, s in enumerate(IDEAS)) + '</div>'
      '<div class="faceless" id="fless"><i class="av"></i><b>@???</b><div class="fgrid">' + "<i></i>" * 6 + '</div><span>?</span></div></div>')
scene("s3", r2["t"] - .1, "g")
for k in range(6):
    pop(f"#id{k}", r2["t"] + .2 + k * .1, .3, "{opacity: 0, scale: .3, rotation: -8}")
    sfx("pop", r2["t"] + .2 + k * .1)
js(f'tl.to(".ideas", {{y: -40, scale: .78, duration: .4, ease: "power3.inOut"}}, {r2["know"] - .2:.3f});')
ft2("#fless", r2["know"], .45, "{opacity: 0, y: 300}", "{opacity: 1, y: 0}", "back.out(1.6)")
stamp("stp2", "DOESN'T KNOW YOUR ACCOUNT", r2["acct"] + .1)
to("#stp2", c2["t"] - .2, .15, "{opacity: 0}")

# =====================================================================================================================
# s4: your page gets read; most-saved tiles glow; POST THIS NEXT flies in
TILES = "".join(f'<div class="tile{" hot" if k in (1, 4) else ""}" id="tl{k}" style="background:{("#ffd08a", "#ff9ec9", "#c9e6ff", "#d8f5c4", "#ff8ac2", "#e7d7ff", "#ffe39a", "#ffc6e0", "#cfd3da")[k]}">'
                f'{"<em>2.1K saves</em>" if k == 1 else "<em>1.8K saves</em>" if k == 4 else ""}</div>' for k in range(9))
S4 = (f'<div class="scene" id="s4">{CBADGE}<div class="page"><div class="ph"><i class="av"></i><b>@your.page</b></div><div class="pgrid" id="pgrid">{TILES}</div>'
      '<i class="scan" id="scan"></i></div><div class="nextc" id="nextc"><small>POST THIS NEXT</small>One-pan dinners, part 2<em>because your saves say so</em></div></div>')
scene("s4", c2["t"] - .05, "c")
for k in range(9):
    pop(f"#tl{k}", c2["t"] + .05 + k * .04, .25, "{opacity: 0, scale: .5}")
ft2("#scan", c2["reads"], .8, "{opacity: 0, y: 0}", "{opacity: 1, y: 600}", "power1.inOut")
to("#scan", c2["reads"] + .8, .15, "{opacity: 0}")
sfx("riser_short", c2["reads"])
for k in (1, 4):
    js(f'tl.to("#tl{k}", {{scale: 1.12, boxShadow: "0 0 0 8px #F343A2, 0 20px 40px rgba(243,67,162,.45)", duration: .25, ease: "back.out(3)"}}, {c2["reads"] + .5 + (k == 4) * .15:.3f});')
    ft2(f"#tl{k} em", c2["reads"] + .55 + (k == 4) * .15, .25, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "back.out(2)")
    sfx("pop", c2["reads"] + .5 + (k == 4) * .15)
ft2("#nextc", c2["tells"] - .1, .45, "{opacity: 0, x: 600, rotation: 12}", "{opacity: 1, x: 0, rotation: -2}", "back.out(1.5)")
sfx("ding", c2["tells"])

# =====================================================================================================================
# s5: "Looks great!" vs a play counter stuck at 0:00
S5 = (f'<div class="scene" id="s5">{GBADGE}<div class="lg" id="lg"><span class="lgav">' + LOGO + '</span><b>Looks great!</b><small>EXAMPLE REPLY</small></div>'
      '<div class="rcard big" id="rc3"><div class="thumb"><i></i><b>Your reel</b></div><i class="play"></i></div>'
      '<div class="watched" id="wat">WATCHED <b>0:00</b> / 0:30</div></div>')
scene("s5", r3["t"] - .1, "g")
ft2("#rc3", r3["t"] + .1, .45, "{opacity: 0, y: 200, rotation: -6}", "{opacity: 1, y: 0, rotation: -3}", "back.out(1.6)")
pop("#lg", r3["post"] + .1, .4, "{opacity: 0, scale: .3, rotation: 12}")
sfx("pop", r3["post"] + .1)
pop("#wat", r3["hasnt"], .3, "{opacity: 0, scale: .6}")
js(f'tl.fromTo("#wat b", {{opacity: 1}}, {{opacity: .2, duration: .2, yoyo: true, repeat: 5, immediateRender: false}}, {r3["hasnt"] + .2:.3f});')
stamp("stp3", "HASN'T WATCHED IT", r3["watched"] + .15)
to("#stp3", c3["t"] - .2, .15, "{opacity: 0}")

# =====================================================================================================================
# s6: the gauge to 3.8 / 5, score chips, POST pressed
TICKS = "".join(f'<line x1="{300 + 230 * math.cos(math.radians(180 + k * 18)):.1f}" y1="{300 + 230 * math.sin(math.radians(180 + k * 18)):.1f}" '
                f'x2="{300 + 260 * math.cos(math.radians(180 + k * 18)):.1f}" y2="{300 + 260 * math.sin(math.radians(180 + k * 18)):.1f}" stroke="#e5b8cf" stroke-width="6"/>' for k in range(11))
S6 = (f'<div class="scene" id="s6">{CBADGE}<div class="gauge"><svg viewBox="0 0 600 340"><path d="M60,300 A240,240 0 0 1 540,300" fill="none" stroke="#f6d9e8" stroke-width="44" stroke-linecap="round"/>'
      '<path id="garc" d="M60,300 A240,240 0 0 1 540,300" fill="none" stroke="#F343A2" stroke-width="44" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
      f'{TICKS}<g id="needle"><path d="M300,300 L300,96" stroke="#1a1020" stroke-width="14" stroke-linecap="round"/><circle cx="300" cy="300" r="26" fill="#1a1020"/></g></svg>'
      '<div class="gnw"><b id="gnum">0.0</b><small>/ 5</small></div></div>'
      '<div class="chips">' + "".join(f'<span id="ch{k}"><b>{n}</b>{v}</span>' for k, (n, v) in enumerate((("Hook", 3), ("Pacing", 4), ("Visuals", 4), ("CTA", 4)))) + '</div>'
      '<div class="fixc small" id="fix3"><small>FIX AT 0:14</small>Show the tool\'s name on screen.</div><div class="postb" id="postb">POST</div></div>')
scene("s6", c3["t"] - .05, "c")
js('gsap.set("#needle", {svgOrigin: "300 300", rotation: -90});')
js(f'tl.fromTo("#needle", {{rotation: -90}}, {{rotation: {-90 + 180 * 3.8 / 5:.1f}, duration: .9, ease: "elastic.out(1, .5)", immediateRender: false}}, {c3["scores"]:.3f});')
ft2("#garc", c3["scores"], .7, "{strokeDashoffset: 1, opacity: 0}", f"{{strokeDashoffset: {1 - 3.8 / 5:.2f}, opacity: 1}}", "power2.out")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 3.8, duration: .7, ease: "power2.out", onUpdate: () => {{ document.getElementById("gnum").textContent = o.v.toFixed(1); }}}}, {c3["scores"]:.3f}); }})();')
sfx("riser_short", c3["scores"] - .1)
for k in range(4):
    pop(f"#ch{k}", c3["scores"] + .4 + k * .08, .3, "{opacity: 0, scale: .4, y: 20}")
    sfx("pop", c3["scores"] + .4 + k * .08)
pop("#fix3", c3["before"], .35, "{opacity: 0, scale: .6, y: 30}")
pop("#postb", c3["hit"] - .05, .3)
js(f'tl.fromTo("#postb", {{scale: 1}}, {{keyframes: [{{scale: .85, duration: .08}}, {{scale: 1.1, duration: .14}}, {{scale: 1, duration: .1}}], immediateRender: false}}, {c3["hit"] + .3:.3f});')
sfx("click", c3["hit"] + .3); sfx("ding", c3["hit"] + .35)

# =====================================================================================================================
# s7: ChatGPT writes a script (credit where it's due)
SCRIPT = "Hook: Stop scrolling, this one is for you. Problem: you post every day and nothing grows. Fix: open on the result.".split()
S7 = (f'<div class="scene" id="s7"><div class="bigg"><span>{LOGO}</span></div><div class="paper" id="paper"><small>REEL SCRIPT</small><p>'
      + " ".join(f'<span id="sw{k}" style="opacity:0">{w}</span>' for k, w in enumerate(SCRIPT)) + '</p></div><div class="good" id="good">GREAT FOR: WRITING</div></div>')
scene("s7", t_writer - .1, "g")
ft2("#paper", t_writer, .4, "{opacity: 0, y: 200, rotation: 4}", "{opacity: 1, y: 0, rotation: -2}", "back.out(1.5)")
for k in range(len(SCRIPT)):
    st(f"#sw{k}", t_writer + .2 + k * .09, "{opacity: 1}")
    if k % 3 == 0:
        sfx("typing", t_writer + .2 + k * .09)
pop("#good", t_great, .35, "{opacity: 0, scale: .5, rotation: 6}")
sfx("ding2", t_great)

# =====================================================================================================================
# s8: Creedom = your Instagram coach; CREEDOM WINS
S8 = ('<div class="scene" id="s8"><div class="coach" id="coach"><small>CREEDOM IS</small><b>YOUR<br>INSTAGRAM<br>COACH</b>'
      '<span>watches your reels · reads your page · scores before you post</span></div><div class="rays" id="rays"></div></div>')
scene("s8", t_coach - .05, "c")
pop("#coach", t_coach, .45, "{opacity: 0, scale: .4, rotation: -6}")
ft2("#rays", t_coach, .5, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}", "power3.out")
js(f'tl.fromTo("#rays", {{rotation: 0}}, {{rotation: 60, duration: 3, ease: "none", immediateRender: false}}, {t_coach:.3f});')
sfx("sparkle", t_coachw)
pop("#win", t_coachw, .4, "{opacity: 0, scale: 2, rotation: -10}")
sfx("applause", t_coachw + .05)
punch(t_coachw, 1.05)

# the scoreboard ticks to Creedom on each answer
for k, t in enumerate((c1["leave"] + .2, c2["tells"] + .3, c3["hit"] + .4), start=1):
    st(f"#sn{k - 1}", t, "{opacity: 0}")
    ft2(f"#sn{k}", t, .35, "{opacity: 0, scale: 2.2, y: -20}", "{opacity: 1, scale: 1, y: 0}", "back.out(3)")
    js(f'tl.fromTo(".scc", {{scale: 1}}, {{scale: 1.14, duration: .12, yoyo: true, repeat: 1, immediateRender: false}}, {t:.3f});')
    sfx("coin", t)

# =====================================================================================================================
# CTA
CBOX = ('<div class="cbox" id="cbox"><i class="cav"></i><span id="cbt">' + "".join(f'<span id="cg{k}" style="opacity:0">{c}</span>' for k, c in enumerate("GROW"))
        + '</span><b class="csend" id="csend">Post</b></div><div class="sent" id="sent">Sent! Now check your DMs</div>')
to("#s8", t_cm - .2, .25, "{opacity: 0, scale: .9}", "power2.in")
to("#score", t_cm - .2, .3, "{opacity: 0, y: -30}", "power2.in")
ft2("#cbox", t_cm + .1, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.8)")
for k in range(4):
    st(f"#cg{k}", t_g + k * .1, "{opacity: 1}")
    sfx("tick", t_g + k * .1)
js(f'tl.fromTo("#csend", {{scale: 1}}, {{keyframes: [{{scale: .85, duration: .08}}, {{scale: 1, duration: .15}}], immediateRender: false}}, {t_g + .55:.3f});')
sfx("click", t_g + .55)
ft2("#sent", t_g + .7, .3, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "back.out(2)")
sfx("ding", t_g + .75)
for k in range(24):
    x0 = random.randint(60, 1020)
    HTMLS.append(f'<i class="cf" id="cf{k}" style="background:{random.choice(("#ff5fb7", "#F343A2", "#ffd27a", "#1a1020", "#ffffff"))};'
                 f'width:{random.randint(12, 20)}px;height:{random.randint(22, 32)}px"></i>')
    js(f'tl.fromTo("#cf{k}", {{x: {x0}, y: -60, rotation: {random.randint(0, 180)}, opacity: 1}}, {{x: {x0 + random.uniform(-160, 160):.0f}, y: 2000, '
       f'rotation: {random.randint(360, 900)}, duration: {random.uniform(1.6, 2.4):.2f}, ease: "power1.in", immediateRender: false}}, {t_coachw + random.uniform(0, .3):.3f});')

# =====================================================================================================================
# Cree: in the Creedom half for the hook, bottom right for the rounds, centre for the coach and the CTA
CH, CC, CR = P(800, 1330, .5), P(540, 1690, .42), P(935, 1815, .3)
js(f'gsap.set("#cree", {{x: {CH[0] - PCX:.0f}, y: {CH[1] - PCY:.0f}, scale: {CH[2]}, opacity: 1}});')
js('gsap.set("#cree .cpose", {opacity: 0}); gsap.set("#cp-stand", {opacity: 1});')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -7, duration: .6, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .6)}, immediateRender: false}}, 0);')
for k in range(int(DUR / 2.6)):
    blink(1.3 + k * 2.6)
pose(.4, "cheer", flip=False)
cree_hop(.45, 70)
pose(t_gpt0, "point", flip=True)
cree_to(r1["t"] - .2, CR[0], CR[1], CR[2], .45)
pose(r1["guess"], "think", flip=True)
pose(r1["seen"] + .3, "shock"); cree_wiggle(r1["seen"] + .3, 2, 6); sweat(r1["seen"] + .35, .8)
pose(c1["t"], "mag", flip=True)
pose(c1["leave"] + .1, "proud"); cree_hop(c1["leave"] + .15, 60); say(c1["leave"] + .25, "!", .7, left=True)
pose(r2["know"], "think", flip=True)
pose(r2["acct"] + .15, "shock"); cree_wiggle(r2["acct"] + .15, 2, 6)
pose(c2["t"], "present", flip=True)
pose(c2["tells"] + .1, "proud"); cree_hop(c2["tells"] + .15, 60)
pose(r3["post"], "think", flip=True)
pose(r3["watched"] + .2, "sad")
pose(c3["t"], "present", flip=True)
pose(c3["hit"] + .3, "cheer"); cree_hop(c3["hit"] + .35, 60)
pose(t_writer, "stand")
cree_to(t_coach - .1, CC[0], CC[1], CC[2], .45, "back.out(1.4)")
pose(t_coach, "cheer", flip=False)
cree_hop(t_coachw, 90, 2)
sparkle(t_coachw, 1.0)
pose(t_cm, "wave", flip=False)
cree_hop(t_g + .75, 70, 2)

POST = " ".join(f'gsap.set("{sel}", {frm});' for sel, (t, frm) in sorted(FIRST.items(), key=lambda kv: kv[1][0]) if t > 0.0)
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: Stop using ChatGPT for your reels 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="bg" id="bgl"></div><div class="bg" id="bgg"></div><div class="bg" id="wipe"></div>
      <div id="stage">{S0}{S1}{S2}{S3}{S4}{S5}{S6}{S7}{S8}{CBOX}</div>
      {SCORE}
      <div style="position:absolute;inset:0;z-index:33;pointer-events:none">{cree_html()}</div>
      {chr(10).join(HTMLS)}
      <div id="flash"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      tl.progress(1, true).progress(0, true);
      {POST}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "lines": L0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
