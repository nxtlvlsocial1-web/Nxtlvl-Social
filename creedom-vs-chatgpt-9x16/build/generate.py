"""Creators 100X x Creedom "Stop using ChatGPT for your reels" (9:16): writes index.html, plan/sfx_events.json, plan/edit.json.
Three rounds on one phone. Each round a question goes to a ChatGPT chat (OpenAI's logo as its label only, never defaced): it
answers with a generic example reply, a thumb flicks the reply away and a red stamp names why ("it has never seen your reel").
The phone flips to Creedom, which does the real thing (second-by-second timeline, what to post next from your page, a score
before you post); the scoreboard ticks to Creedom. Then "ChatGPT is a great writer. Creedom is your Instagram coach." and the
GROW comment box. Replies, scores and timestamps are illustrations, labelled EXAMPLE. Cree reacts bottom right throughout.
python3 build/generate.py"""
import json
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
    """fromTo that also records the entrance start state, re-applied after the timeline reset"""
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


def flip_to(side, t):
    """flip the phone: side 'g' (ChatGPT) or 'c' (Creedom)"""
    js(f'tl.to("#pw", {{rotationY: 90, duration: .14, ease: "power2.in"}}, {t:.3f});')
    st("#sg", t + .14, f"{{opacity: {1 if side == 'g' else 0}}}")
    st("#sc", t + .14, f"{{opacity: {1 if side == 'c' else 0}}}")
    js(f'tl.fromTo("#pw", {{rotationY: -90}}, {{rotationY: 0, duration: .22, ease: "back.out(1.6)", immediateRender: false}}, {t + .14:.3f});')
    sfx("whoosh", t)
    if side == "c":
        flash(t + .14, .35, .25)


LOGO = '<img class="glogo" src="assets/img/chatgpt_logo.png" alt="">'

# ---------------------------------------------------------------- the ChatGPT screen (three rounds of chat)
ROUNDS = [
    ("Why did my reel flop?", "Reels can underperform for many reasons! Try a stronger hook, trending audio and posting at peak times.", "NEVER SAW YOUR REEL"),
    ("What should I post next?", "Here are some ideas that do well: a day in my life, a morning routine, GRWM, and top 5 tips in your niche.", "DOESN'T KNOW YOUR ACCOUNT"),
    ("Is my reel ready to post?", "Looks great! Just make sure your hook is strong and your caption is engaging.", "HASN'T WATCHED IT"),
]
SG = '<div class="scrn" id="sg" style="opacity:1"><div class="ghead">' + LOGO + '<b>ChatGPT</b></div>'
for i, (q, a, _) in enumerate(ROUNDS):
    SG += (f'<div class="ground" id="gr{i}"><div class="ubub" id="gq{i}">' + "".join(f'<span id="gq{i}c{k}" style="opacity:0">{c}</span>' for k, c in enumerate(q)) + '</div>'
           f'<div class="dots" id="gd{i}"><i></i><i></i><i></i></div>'
           f'<div class="abub" id="ga{i}"><span class="av">{LOGO}</span><p>{a}</p><em>EXAMPLE REPLY</em></div></div>')
SG += ('<div class="ground" id="gr3"><div class="ubub" style="opacity:1">Write my reel script</div><div class="abub ok" id="ga3"><span class="av">' + LOGO + '</span>'
       '<p id="gw">' + " ".join(f'<span id="gw{k}" style="opacity:0">{w}</span>' for k, w in enumerate("Hook: Stop scrolling, this one is for you. Problem: you post every day and nothing grows. Fix: ...".split())) + '</p></div>'
       '<div class="good" id="good">GREAT FOR: WRITING</div></div>')
SG += '<div class="gin">Message ChatGPT</div></div>'

# ---------------------------------------------------------------- the Creedom screen (three answers)
SEG = "".join(f'<i id="sg{k}" class="{"bad" if k == 1 else ""}"></i>' for k in range(15))
TOP = [("Hostel pasta, 1 pan", "2.1K saves", "#ffd08a"), ("5 meals under 100", "1.8K saves", "#ff9ec9"), ("Grocery haul", "240 saves", "#cfd3da")]
SC = ('<div class="scrn" id="sc"><div class="chead"><img src="assets/img/creedom_logo.png" alt=""><span class="ex">EXAMPLE</span></div>'
      # answer 1: second by second
      '<div class="cans" id="ca0"><div class="thumb"><i></i><b>My budget meal hack</b></div><div class="clab" id="c0l">WATCHING YOUR REEL<br><span>SECOND BY SECOND</span></div>'
      f'<div class="tline">{SEG}<u id="phd"></u></div><div class="tlab"><span>0:00</span><span>0:15</span><span>0:30</span></div>'
      '<div class="leave" id="leave"><small>0:03 · PEOPLE LEAVE HERE</small>Your hook shows the result too late.</div>'
      '<div class="fix" id="fix0"><small>FIX</small>Open on the finished dish.</div></div>'
      # answer 2: reads your page
      '<div class="cans" id="ca1"><div class="clab">READING <span>@YOUR.PAGE</span></div>'
      + "".join(f'<div class="top" id="tp{i}"><i style="background:{c}"></i><b>{n}</b><small>{s}</small></div>' for i, (n, s, c) in enumerate(TOP))
      + '<div class="next" id="next"><small>POST THIS NEXT</small>One-pan dinners, part 2<em>Your saves say this is what they want</em></div></div>'
      # answer 3: score before you post
      '<div class="cans" id="ca2"><div class="thumb"><i></i><b>My budget meal hack</b></div><div class="clab">CHECKING BEFORE<br><span>YOU POST</span></div>'
      '<div class="ring"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" stroke="#f3d6e6" stroke-width="18" fill="none"/>'
      '<circle id="rarc" cx="100" cy="100" r="84" stroke="#F343A2" stroke-width="18" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg>'
      '<b id="rnum">0.0</b><small>/ 5</small></div>'
      '<div class="fix" id="fix2"><small>FIX AT 0:14</small>Show the tool\'s name on screen.</div>'
      '<div class="post" id="post">Then post it</div></div>'
      # coach
      '<div class="cans" id="ca3"><div class="coach" id="coach">BUILT FOR:<b>YOUR REELS</b><span>watches them · reads your page · scores before you post</span></div></div>'
      '</div>')
PHONE = (f'<div id="pw"><div id="ph"><div id="scr"><i class="isl"></i><div class="sbar"><span>9:41</span><span>5G</span></div>{SG}{SC}'
         '</div></div></div>')
STAMPS = '<div class="stamp big" id="stopst"><span>STOP</span></div>' + "".join(f'<div class="stamp" id="stamp{i}"><span>{s}</span></div>' for i, (_, _, s) in enumerate(ROUNDS))
THUMB = '<svg id="flick" viewBox="0 0 120 160" width="150" height="200"><path d="M40 150 L40 60 Q40 40 55 40 Q70 40 70 60 L70 90 L96 96 Q112 100 110 118 L104 150 Z" fill="#ffd9c2" stroke="#1a1020" stroke-width="6" stroke-linejoin="round"/></svg>'
SCORE = ('<div id="score"><span class="sg">' + LOGO + '<b>ChatGPT</b><em id="sgn">0</em></span><i>:</i>'
         '<span class="scc"><em id="scn">' + "".join(f'<u id="sn{k}">{k}</u>' for k in range(4)) + '</em><b>Creedom</b></span></div>')
CBOX = ('<div class="cbox" id="cbox"><i class="cav"></i><span id="cbt">' + "".join(f'<span id="cg{k}" style="opacity:0">{c}</span>' for k, c in enumerate("GROW"))
        + '</span><b class="csend" id="csend">Post</b></div><div class="sent" id="sent">Sent! Now check your DMs</div>')

# ---------------------------------------------------------------- times
t_stop, t_gpt0, t_why = L0["v0"], T("v0", "ChatGPT"), T("v0", "Here's")
R = []
for ln, ask_end_word, bad_word, bad_end in (("v1", "flopped", "guesses", "never"), ("v3", "next", None, "account"), ("v4", "post", None, "watched")):
    qend = T(ln, ask_end_word) + .25
    ans = T(ln, bad_word) if bad_word else qend + .2      # rounds 2 and 3: the reply lands right after the question
    R.append(dict(ask=L0[ln], qend=qend, ans=ans, stamp=T(ln, bad_end)))
C1 = dict(t=L0["v2"], sec=T("v2", "second"), leave=T("v2", "where"))
C2 = dict(t=T("v3", "Creedom"), reads=T("v3", "reads"), tells=T("v3", "tells"))
C3 = dict(t=T("v4", "Creedom"), scores=T("v4", "scores"), before=T("v4", "before"))
t_writer, t_coach = L0["v5"], T("v5", "Creedom")
t_cm = L0["v6"]

# ---------------------------------------------------------------- headlines
head("h0", [["*Stop", "using", "~ChatGPT"], ["for", "your", "reels."]], "v0", 92)
head("h0b", [["Here's", "*why."]], "v0", 110, after=t_why)
head("h1", [["Ask", "it", "why", "your"], ["reel", "flopped,", "and", "it"], ["*guesses."]], "v1", 80)
head("h1b", [["It's", "*never", "*seen"], ["your", "reel."]], "v1", 92, after=T("v1", "It's"))
head("h2", [["*Creedom", "watches", "it,"], ["second", "by", "second,"]], "v2", 84)
head("h2b", [["and", "shows", "you", "where"], ["people", "*leave."]], "v2", 84, after=T("v2", "and"))
head("h3", [["Ask", "it", "what", "to", "post", "next."], ["It", "doesn't", "know"], ["your", "*account."]], "v3", 76)
head("h3b", [["*Creedom", "reads", "your", "page,"], ["and", "tells", "you."]], "v3", 84, after=C2["t"])
head("h4", [["Ask", "if", "your", "reel"], ["is", "ready", "to", "post."], ["It", "*hasn't", "*watched", "it."]], "v4", 76)
head("h4b", [["*Creedom", "scores", "it,"], ["before", "you", "hit", "post."]], "v4", 84, after=C3["t"])
head("h5", [["~ChatGPT", "is", "a"], ["great", "writer."]], "v5", 88)
head("h5b", [["*Creedom", "is", "your"], ["Instagram", "*coach."]], "v5", 92, after=t_coach)
head("h6", [["Comment", "*GROW"], ["and", "I'll", "send", "you", "Creedom."]], "v6", 84)

# ---------------------------------------------------------------- choreography
js('gsap.set("#pw", {transformPerspective: 1800, transformOrigin: "50% 50%"}); gsap.set("#stage", {transformOrigin: "540px 1100px"});')
ft2("#pw", 0, .5, "{opacity: 0, y: 260, rotation: -8}", "{opacity: 1, y: 0, rotation: 0}", "back.out(1.5)")
sfx("whoosh_big", 0)
js(f'tl.fromTo("#ph", {{rotation: -.6}}, {{rotation: .6, duration: 1.9, yoyo: true, repeat: {int(DUR / 1.9)}, ease: "sine.inOut", immediateRender: false}}, 0);')
punch(t_stop, 1.05)
ft2("#stopst", t_stop + .05, .22, "{opacity: 0, scale: 2.6, rotation: -24}", "{opacity: 1, scale: 1, rotation: -10}", "power4.out")
sfx("stamp", t_stop + .1)
to("#stopst", t_why - .25, .2, "{opacity: 0, scale: .8}", "power2.in")
sfx("impact", t_stop + .02)
pop("#score", t_why, .35, "{opacity: 0, scale: .5, y: -20}")
sfx("ding2", t_why)
st("#gr0", 0, "{opacity: 1}")

for i, r in enumerate(R):
    if i:
        flip_to("g", r["ask"] - .2)
        st(f"#gr{i - 1}", r["ask"] - .06, "{opacity: 0}")
        st(f"#gr{i}", r["ask"] - .06, "{opacity: 1}")
    q = ROUNDS[i][0]
    ft2(f"#gq{i}", r["ask"], .25, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
    for k in range(len(q)):
        tk = r["ask"] + (r["qend"] - r["ask"]) * k / len(q)
        st(f"#gq{i}c{k}", tk, "{opacity: 1}")
        if k % 4 == 0:
            sfx("typing", tk)
    pop(f"#gd{i}", r["qend"] + .02, .2)
    to(f"#gd{i}", r["ans"] - .08, .1, "{opacity: 0}")
    js(f'tl.fromTo("#gd{i} i", {{y: 0}}, {{y: -10, duration: .16, yoyo: true, repeat: 3, stagger: .08, immediateRender: false}}, {r["qend"]:.3f});')
    ft2(f"#ga{i}", r["ans"], .35, "{opacity: 0, y: 40, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
    sfx("pop", r["ans"])
    # the flick + the stamp
    ft2("#flick", r["stamp"] - .3, .2, "{opacity: 0, x: 760, y: 1240, rotation: 20}", "{opacity: 1, x: 640, y: 1130, rotation: 0}", "power2.out")
    js(f'tl.to("#flick", {{x: 300, y: 1060, rotation: -30, duration: .16, ease: "power3.in"}}, {r["stamp"] - .08:.3f});')
    to("#flick", r["stamp"] + .1, .15, "{opacity: 0}")
    js(f'tl.to("#ga{i}", {{x: -760, rotation: -14, opacity: 0, duration: .32, ease: "power3.in"}}, {r["stamp"] - .02:.3f});')
    sfx("whoosh", r["stamp"] - .05)
    ft2(f"#stamp{i}", r["stamp"] + .1, .22, "{opacity: 0, scale: 2.4, rotation: -20}", "{opacity: 1, scale: 1, rotation: -8}", "power4.out")
    sfx("stamp", r["stamp"] + .14)
    punch(r["stamp"] + .14, 1.035)
    to(f"#stamp{i}", [C1, C2, C3][i]["t"] - .2, .15, "{opacity: 0, scale: .8}", "power2.in")

# Creedom answer 1: second by second, people leave at 0:03
flip_to("c", C1["t"] - .15)
st("#ca0", C1["t"], "{opacity: 1}")
js(f'tl.fromTo("#phd", {{left: "0%"}}, {{left: "100%", duration: {C1["leave"] - C1["sec"]:.2f}, ease: "none", immediateRender: false}}, {C1["sec"]:.3f});')
for k in range(15):
    tk = C1["sec"] + (C1["leave"] - C1["sec"]) * (k + .5) / 15
    ft2(f"#sg{k}", tk, .15, "{opacity: .15, scaleY: .4}", "{opacity: 1, scaleY: 1}", "back.out(3)")
    if k % 3 == 0:
        sfx("tick", tk)
pop("#leave", C1["leave"], .35, "{opacity: 0, scale: .6, y: 30}")
sfx("error", C1["leave"])
pop("#fix0", T("v2", "leave"), .35, "{opacity: 0, scale: .6, y: 30}")
sfx("ding", T("v2", "leave"))
# Creedom answer 2: reads your page, post this next
flip_to("c", C2["t"] - .15)
st("#ca0", C2["t"], "{opacity: 0}")
st("#ca1", C2["t"], "{opacity: 1}")
for i in range(3):
    ft2(f"#tp{i}", C2["reads"] + i * .14, .3, "{opacity: 0, x: 80}", "{opacity: 1, x: 0}", "back.out(1.8)")
    sfx("pop", C2["reads"] + i * .14)
js(f'tl.to("#tp0, #tp1", {{borderColor: "#F343A2", duration: .2}}, {C2["tells"] - .3:.3f});')
pop("#next", C2["tells"], .4, "{opacity: 0, scale: .6, y: 40}")
sfx("ding", C2["tells"])
# Creedom answer 3: the score before you post
flip_to("c", C3["t"] - .15)
st("#ca1", C3["t"], "{opacity: 0}")
st("#ca2", C3["t"], "{opacity: 1}")
ft2("#rarc", C3["scores"], .8, "{strokeDashoffset: 1, opacity: 0}", "{strokeDashoffset: .24, opacity: 1}", "power2.out")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 3.8, duration: .8, ease: "power2.out", onUpdate: () => {{ document.getElementById("rnum").textContent = o.v.toFixed(1); }}}}, {C3["scores"]:.3f}); }})();')
sfx("riser_short", C3["scores"])
pop("#fix2", C3["scores"] + .7, .35, "{opacity: 0, scale: .6, y: 30}")
sfx("pop", C3["scores"] + .7)
pop("#post", C3["before"], .35)
js(f'tl.fromTo("#post", {{scale: 1}}, {{scale: 1.08, duration: .2, yoyo: true, repeat: 3, immediateRender: false}}, {C3["before"] + .35:.3f});')
sfx("ding", C3["before"])

# the scoreboard ticks to Creedom on each answer
for k, t in enumerate((C1["leave"] + .2, C2["tells"] + .2, C3["before"] + .2), start=1):
    st(f"#sn{k - 1}", t, "{opacity: 0}")
    ft2(f"#sn{k}", t, .35, "{opacity: 0, scale: 2.2, y: -20}", "{opacity: 1, scale: 1, y: 0}", "back.out(3)")
    js(f'tl.fromTo(".scc", {{scale: 1}}, {{scale: 1.12, duration: .12, yoyo: true, repeat: 1, immediateRender: false}}, {t:.3f});')
    sfx("coin", t)

# ChatGPT is a great writer -> Creedom is your Instagram coach
flip_to("g", t_writer - .25)
st("#gr2", t_writer - .1, "{opacity: 0}")
st("#gr3", t_writer - .1, "{opacity: 1}")
for k in range(18):
    st(f"#gw{k}", t_writer + .1 + k * .1, "{opacity: 1}")
    if k % 3 == 0:
        sfx("typing", t_writer + .1 + k * .1)
pop("#good", T("v5", "writer"), .35, "{opacity: 0, scale: .5, rotation: 6}")
sfx("ding2", T("v5", "writer"))
flip_to("c", t_coach - .2)
st("#ca2", t_coach, "{opacity: 0}")
st("#ca3", t_coach, "{opacity: 1}")
pop("#coach", t_coach + .05, .45, "{opacity: 0, scale: .5}")
sfx("sparkle", T("v5", "coach"))
punch(T("v5", "coach"), 1.05)

# CTA: the phone steps back, the comment box types GROW
to("#pw", t_cm - .25, .45, "{y: 1500, rotation: 10, opacity: 0}", "power3.in")
to("#score", t_cm - .25, .3, "{opacity: 0, y: -30}", "power2.in")
ft2("#cbox", t_cm + .1, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.8)")
t_g = T("v6", "GROW")
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
       f'rotation: {random.randint(360, 900)}, duration: {random.uniform(1.6, 2.4):.2f}, ease: "power1.in", immediateRender: false}}, {t_g + .75 + random.uniform(0, .3):.3f});')

# ---------------------------------------------------------------- Cree, bottom right, from frame 0
CR = (935, 1815, .3)
_x, _y, _s = P(*CR)
js(f'gsap.set("#cree", {{x: {_x - PCX:.0f}, y: {_y - PCY:.0f}, scale: {_s}, opacity: 1}});')
js('gsap.set("#cree .cpose", {opacity: 0}); gsap.set("#cp-shock", {opacity: 1});')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -7, duration: .6, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .6)}, immediateRender: false}}, 0);')
for k in range(int(DUR / 2.6)):
    blink(1.3 + k * 2.6)
pose(t_gpt0, "point", flip=True)
say(t_why, "?", .8, left=True)
for i, r in enumerate(R):
    pose(r["ans"], "think" if i != 1 else "mag", flip=True)
    pose(r["stamp"] + .1, "shock")
    cree_wiggle(r["stamp"] + .1, 2, 6)
    pose([C1, C2, C3][i]["t"], "present", flip=True)
    pose([C1["leave"], C2["tells"], C3["before"]][i] + .1, "proud")
    cree_hop([C1["leave"], C2["tells"], C3["before"]][i] + .15, 60)
    say([C1["leave"], C2["tells"], C3["before"]][i] + .25, "!", .7, left=True)
sweat(R[0]["stamp"] + .2, .9)
pose(t_writer, "stand")
pose(t_coach, "cheer")
cree_hop(t_coach + .1, 80, 2)
sparkle(T("v5", "coach"), 1.0)
pose(t_cm, "wave", flip=False)
_cx, _cy, _cs = P(540, 1640, .5)
cree_to(t_cm - .1, _cx, _cy, _cs, .5, "back.out(1.4)")
cree_hop(t_g + .75, 70, 2)

# re-apply entrance start states after the reset (GSAP's reset can leave entrance + exit elements visible)
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
      <div class="bg" id="bgl"></div>
      <div id="stage">{PHONE}{STAMPS}{THUMB}{CBOX}</div>
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
