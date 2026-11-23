"""Creators 100X x Creedom "The refresh spiral" (9:16, POV): writes index.html, plan/sfx_events.json and plan/edit.json from
plan/words.json.

Concept C from the owner's storytelling blueprint (relatable -> conflict -> realisation -> action), script approved 2026-11-23,
voiced by the owner in ElevenLabs (Blondie, Eleven v4; build/vo_tight.py trims the pauses, build/vo_words_direct.py the word
times). Literal on purpose: a phone in your hand, the views you refresh, the moment people leave.
  r0 relatable: the reel is shared at 9 pm; refresh, refresh, refresh (the clock jumps five minutes each time);
  r1: 12 views... 19... 23;
  r2 conflict: the Notes app: "why does the algorithm hate me"; THE ALGORITHM villain card;
  r3 realisation (the music cuts out): the villain is crossed out; the reel's retention line falls off a cliff at 0:02,
     little viewers walk out, PEOPLE LEFT HERE;
  r4: push in on 0:02; "?" ... unless something showed you;
  r5 action (the music comes back): Creedom checks the reel: 0:01 weak hook, 0:02 people leave here, FIX, a score (example); Post;
  r6 CTA: COMMENT GROW, Cree waves.
python3 build/generate.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT  # noqa: E402
from fx import cree_html, cree_to, pose, cree_hop, sparkle, P, sweat, say, cree_wiggle, blink  # noqa: E402

random.seed(5)
DUR = round(L1["r6"] + 1.15, 2)
T0 = {k: (L0[k], L1[k]) for k in LINES}

HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, line, size=84, after=0.0, dark=False):
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
    HTMLS.append(f'<div class="head{" dk" if dark else ""}" id="{hid}" style="font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out_:
        ft(f"#{wid}", t - .05, .28, "{opacity: 0, filter: 'blur(10px)', y: 24}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out_)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .22, .16, "{opacity: 0, filter: 'blur(12px)', y: -30}", "power2.in")
    OPEN[0] = hid


STAT = []


def stat(t, text, cls=""):
    i = len(STAT)
    STAT.append(f'<div class="stat {cls}" id="st{i}"><span>{text}</span></div>')
    if i:
        to(f"#st{i - 1}", t - .05, .15, "{opacity: 0, y: -14}", "power2.in")
    ft(f"#st{i}", t, .3, "{opacity: 0, y: 14, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")


def flash(t, o=.6, d=.3):
    st("#flash", t, f"{{opacity: {o}}}")
    to("#flash", t + .02, d, "{opacity: 0}", "power2.out")


def screen(sid, t):
    for s in ("s1", "s2", "s3", "s4", "s5"):
        st(f"#{s}", t, f"{{opacity: {1 if s == sid else 0}}}")


def tap(t, x, y):
    js(f'tl.fromTo("#tap", {{opacity: 0, scale: 1.6, left: {x}, top: {y}}}, {{keyframes: [{{opacity: 1, scale: 1, duration: .14}}, {{scale: .8, duration: .06}}, '
       f'{{opacity: 0, scale: 1.4, duration: .18}}], immediateRender: false}}, {t - .12:.3f});')
    sfx("click", t)


def pw(t, props, d=.5, ease="power3.inOut"):
    js(f'tl.to("#pw", {{{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


# =======================================================================================================================
# THE PHONE
BOK = "".join(f'<i class="bok" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{c};opacity:{o}"></i>'
              for x, y, r, c, o in ((60, 300, 120, "#ffb86b", .25), (880, 520, 160, "#ffd27a", .18), (120, 1400, 180, "#8a6bff", .2), (900, 1500, 140, "#ff8ac2", .2),
                                    (720, 180, 90, "#ffd27a", .2)))
THUMB = '<div class="thumb" style="{}"><i></i><b>My budget meal hack</b></div>'
S1 = ('<div class="scrn" id="s1" style="opacity:1"><div class="s1top">New reel</div>' + THUMB.format("left:36px;top:150px;width:190px;height:330px")
      + '<div class="cap">My budget meal hack that changed everything... #foodie #budget</div><div class="share">Share</div></div>')
COUNTS = [("0", 0), ("4", T("r0", "refresh") + .1), ("6", T("r0", "Every")), ("7", T("r0", "five") + .3), ("9", T("r0", "minutes")),
          ("12", T("r1", "12")), ("19", T("r1", "19")), ("23", T("r1", "23") + .25)]
CLOCKS = ["9:00 PM", "9:05 PM", "9:10 PM", "9:15 PM", "9:20 PM", "9:40 PM", "10:15 PM", "11:30 PM"]
S2 = ('<div class="scrn" id="s2">' + THUMB.format("left:214px;top:110px;width:200px;height:200px;border-radius:24px")
      + '<div class="ins"><small>Views</small><div class="vnum">' + "".join(f'<b id="vn{i}">{c}</b>' for i, (c, _) in enumerate(COUNTS))
      + '</div><div class="vsub">in the last hour</div></div><i class="spin" id="spin"></i><div class="clock">'
      + "".join(f'<b id="ck{i}">{c}</b>' for i, c in enumerate(CLOCKS)) + '</div>'
      '<div class="goal"><span>GOAL: 10,000 VIEWS</span><div class="gtrack"><i id="gfill"></i></div><b id="gpct">0%</b></div></div>')
NOTE = "why does the algorithm hate me".split()
S3 = ('<div class="scrn" id="s3"><div class="notes"><small>Notes · 11:42 PM</small>' + " ".join(f'<span id="nw{i}" style="opacity:0">{w}</span>' for i, w in enumerate(NOTE))
      + '</div></div>')
PEOPLE = "".join(f'<i id="pp{i}" style="left:{40 + (i % 5) * 18}px;top:{232 + (i // 5) * 40}px"></i>' for i in range(10))
S4 = ('<div class="scrn" id="s4"><div class="rlab">YOUR REEL · WHO KEPT WATCHING</div>'
      '<svg class="rgraph" viewBox="0 0 588 620"><defs><linearGradient id="rf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff3b4e" stop-opacity=".45"/>'
      '<stop offset="1" stop-color="#ff3b4e" stop-opacity="0"/></linearGradient></defs>'
      '<line x1="0" y1="40" x2="588" y2="40" stroke="#2a2a33" stroke-width="2"/><line x1="0" y1="600" x2="588" y2="600" stroke="#2a2a33" stroke-width="2"/>'
      '<path id="rarea" d="M0 40 L96 44 C112 52 112 470 140 500 C220 540 400 552 588 560 L588 600 L0 600 Z" fill="url(#rf)" opacity="0"/>'
      '<path id="rline" d="M0 40 L96 44 C112 52 112 470 140 500 C220 540 400 552 588 560" fill="none" stroke="#ff3b4e" stroke-width="8" stroke-linecap="round" '
      'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
      '<text x="0" y="640" fill="#6a6a74" font-family="Mono" font-size="24">0:00</text><text x="104" y="640" fill="#ff3b4e" font-family="Mono" font-size="24">0:02</text>'
      '<text x="520" y="640" fill="#6a6a74" font-family="Mono" font-size="24">0:30</text></svg>'
      f'<i class="mark" id="mark"></i><div class="ppl">{PEOPLE}</div><div class="left" id="leftl">PEOPLE LEFT HERE<br>0:02</div><div class="qq" id="qq">?</div></div>')
S5 = ('<div class="scrn" id="s5"><div class="cr"><i class="dot"></i>Creedom</div>'
      '<div class="chk">' + THUMB.format("") + '<div class="aft" id="aft"><i class="dish"></i><b>Hostel budget meal: 3 steps</b></div><span class="ba" id="ba">AFTER</span>' + '<i class="scanl" id="scanl"></i><div class="meta" id="meta">Checking your reel<small id="mts">BEFORE YOU POST</small></div>'
      '<div class="score" id="score">4.6<span> / 5</span></div></div>'
      '<div class="row bad" id="rw0" style="top:500px"><small>0:01 · WEAK HOOK</small>You\'re talking. Nothing on screen moves.</div>'
      '<div class="row bad" id="rw1" style="top:660px"><small>0:02 · PEOPLE LEAVE HERE</small>Most viewers would scroll past.</div>'
      '<div class="row fix" id="rw2" style="top:820px"><small>→ FIX</small>Open on the finished dish. Then explain.</div>'
      '<div class="ex5" id="ex5">EXAMPLE</div><div class="post" id="post">Post reel</div>'
      '<div class="ana5" id="ana5"><small>WATCHING YOUR REEL, SECOND BY SECOND</small><b id="apct">0%</b><div class="tlin">'
      + "".join(f'<i id="seg{k}" style="background:{"#ff3b4e" if k < 2 else "#2fbf71"}"></i>' for k in range(15)) + '<u id="phd"></u></div>'
      '<div class="tlab"><span>0:00</span><span>0:15</span><span>0:30</span></div></div></div>')
PHONE = (f'<div id="pw"><div id="ph"><div id="scr"><i class="isl"></i><div class="sbar" id="sbar"><span id="sbt">9:00</span><span>5G</span></div>'
         f'{S1}{S2}{S3}{S4}{S5}<div class="toast" id="toast">Your reel is live</div></div></div><i class="tap" id="tap"></i></div>')
VILLAIN = ('<div class="villain" id="vil"><svg class="face" viewBox="0 0 320 240"><rect x="20" y="20" width="280" height="200" rx="60" fill="#ff3b4e"/>'
           '<path d="M70 80 L140 110 M250 80 L180 110" stroke="#2a0008" stroke-width="16" stroke-linecap="round"/>'
           '<circle cx="110" cy="130" r="18" fill="#2a0008"/><circle cx="210" cy="130" r="18" fill="#2a0008"/>'
           '<path d="M100 190 Q160 160 220 190" stroke="#2a0008" stroke-width="12" fill="none" stroke-linecap="round"/></svg>'
           '<span>THE ALGORITHM</span><i class="x" id="vx"></i></div>')
CTA = '<div class="cta" id="cta"><b>COMMENT <em>GROW</em></b><small id="ctas">and I\'ll send you Creedom</small></div>'

# =======================================================================================================================
# TIMELINE
CF = (930, 1810, .32)
js(f'tl.fromTo("#ph", {{y: 0, rotation: -.6}}, {{y: -8, rotation: .6, duration: 2.1, yoyo: true, repeat: {int(DUR / 2.1)}, ease: "sine.inOut", immediateRender: false}}, 0);')

# ---- r0 relatable: share, refresh, refresh ------------------------------------------------------------------------------------------
ft("#pw", 0, .5, "{y: 380, rotationX: 24, scale: .92, transformPerspective: 1600}", "{y: 0, rotationX: 0, scale: 1}", "back.out(1.3)")
sfx("whoosh", 0)
head("h0", [[("You", ""), ("post", ""), ("a", ""), ("reel…", "")], [("and", ""), ("then", ""), ("you", ""), ("refresh.", "pk")]], "r0", size=86)
stat(.1, "POV: 9:00 PM")
tap(T("r0", "post") + .1, 330, 1080)
ft("#toast", T("r0", "post") + .2, .25, "{opacity: 0, y: -30}", "{opacity: 1, y: 0}", "back.out(2)")
to("#toast", 1.1, .2, "{opacity: 0, y: -30}")
screen("s2", 1.2)
st("#vn0", 1.2, "{opacity: 1}")
st("#ck0", 1.2, "{opacity: 1}")
for i in range(1, len(COUNTS)):
    t = COUNTS[i][1]
    js(f'tl.fromTo("#spin", {{opacity: 1, rotation: 0}}, {{rotation: 540, opacity: 0, duration: .45, ease: "power2.out", immediateRender: false}}, {t - .4:.3f});')
    js(f'tl.fromTo("#s2 .ins", {{y: 0}}, {{keyframes: [{{y: 60, duration: .2, ease: "power2.out"}}, {{y: 0, duration: .25, ease: "back.out(2)"}}], immediateRender: false}}, {t - .4:.3f});')
    st(f"#vn{i - 1}", t, "{opacity: 0}")
    ft(f"#vn{i}", t, .25, "{opacity: 0, scale: 1.25}", "{opacity: 1, scale: 1}", "back.out(2.5)")
    st(f"#ck{i - 1}", t, "{opacity: 0}")
    st(f"#ck{i}", t, "{opacity: 1}")
    st("#sbt", t, f'{{textContent: "{CLOCKS[i].split()[0]}"}}')
    sfx("swish", t - .4)
    sfx("tick", t)
head("h0b", [[("Every.", ""), ("Five.", "pk"), ("Minutes.", "")]], "r0", size=94, after=T("r0", "Every") - .05)
stat(T("r0", "refresh"), "REFRESHING…")

# ---- r1: 12 views. 19. 23. -----------------------------------------------------------------------------------------------------------
head("h1", [[("12", ""), ("views…", "dim")], [("19…", ""), ("23.", "")]], "r1", size=120)
pw(T("r1", "12") - .2, "scale: 1.08", .4)
js(f'tl.to("#vn5, #vn6, #vn7", {{color: "#9a9a9a", duration: .3}}, {T("r1", "23"):.3f});')
sfx("error", T("r1", "23") + .3)

# ---- r2 conflict: the algorithm hates you --------------------------------------------------------------------------------------------
t2 = T0["r2"][0]
head("h2", [[("And", ""), ("then", ""), ("you", ""), ("tell", ""), ("yourself", "")], [("the", ""), ("algorithm", "rd")], [("hates", ""), ("you.", "")]], "r2", size=84)
pw(t2 - .2, "scale: 1", .4)
screen("s3", t2 - .1)
st("#sbt", t2 - .1, '{textContent: "11:42"}')
for i in range(len(NOTE)):
    st(f"#nw{i}", t2 + .02 + i * .26, "{opacity: 1}")
    sfx("tick", t2 + .02 + i * .26)
t_ht = T("r2", "hates")
ft("#vil", t_ht - .1, .35, "{opacity: 0, scale: .3, rotation: -12}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(2.2)")
js(f'tl.fromTo("#vil", {{x: 0}}, {{keyframes: [{{x: -10, duration: .05}}, {{x: 10, duration: .05}}, {{x: -6, duration: .05}}, {{x: 0, duration: .05}}], repeat: 2, '
   f'immediateRender: false}}, {t_ht + .3:.3f});')
sfx("buzzer", t_ht)
stat(t_ht, "IT'S THE ALGORITHM?", "rd")

# ---- r3 realisation (the music cuts out): people did, in the first two seconds -------------------------------------------------------
t3 = T0["r3"][0]
head("h3", [[("But", ""), ("the", ""), ("algorithm", "")], [("didn't", ""), ("skip", ""), ("your", ""), ("reel.", "")]], "r3", size=86)
flash(t3 - .05, .5, .3)
sfx("impact", t3)
to("#bgr", t3, .3, "{opacity: 1}")
t_dn = T("r3", "didn't")
js(f'tl.to("#vx", {{scaleX: 1, duration: .25, ease: "power3.out"}}, {t_dn:.3f});')
sfx("stamp", t_dn + .1)
to("#vil", T("r3", "reel") - .05, .4, "{opacity: 0, y: 400, rotation: 20}", "power2.in")
screen("s4", t3 + .2)
st("#sbt", t3 + .2, '{textContent: "11:43"}')
ft("#rline", t3 + .4, 1.6, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "power1.inOut")
ft("#rarea", t3 + 1.2, .6, "{opacity: 0}", "{opacity: 1}", "power2.out")
t_pp = T("r3", "People")
head("h3b", [[("People", "rd"), ("did.", "")], [("In", ""), ("the", ""), ("first", "")], [("two", "rd"), ("seconds.", "rd")]], "r3", size=90, after=t_pp - .05)
for i in range(10):
    js(f'tl.fromTo("#pp{i}", {{opacity: 0, x: 0, y: 0}}, {{keyframes: [{{opacity: 1, duration: .15}}, {{x: {random.randint(160, 260)}, y: {random.randint(-90, 40)}, opacity: 0, duration: .8, '
       f'ease: "power1.in"}}], immediateRender: false}}, {t_pp + i * .07:.3f});')
sfx("steps", t_pp)
t_2s = T("r3", "two")
ft("#mark", t_2s - .1, .25, "{opacity: 0, scaleY: 0}", "{opacity: 1, scaleY: 1}", "power3.out")
ft("#leftl", t_2s, .3, "{opacity: 0, scale: .6, x: -20}", "{opacity: 1, scale: 1, x: 0}", "back.out(2.4)")
sfx("error", t_2s)
stat(t3 + .1, "THE TRUTH", "rd")

# ---- r4: you'd never know why ------------------------------------------------------------------------------------------------------
t4 = T0["r4"][0]
head("h4", [[("And", ""), ("you'd", ""), ("never", ""), ("know", ""), ("why…", "rd")], [("unless", ""), ("something", "")], [("showed", ""), ("you.", "pk")]], "r4", size=78)
js(f'tl.to("#pw", {{scale: 1.45, x: 260, y: 220, duration: 2.4, ease: "sine.inOut"}}, {t4:.3f});')
ft("#qq", T("r4", "why") - .05, .35, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1}", "back.out(3)")
js(f'tl.fromTo("#qq", {{scale: 1}}, {{scale: 1.15, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {T("r4", "why") + .3:.3f});')
sfx("riser", T("r4", "unless") - .3)

# ---- r5 action (the music comes back): Creedom checks before you post -----------------------------------------------------------------
t5 = T0["r5"][0]
head("h5", [[("So", ""), ("now", ""), ("I", ""), ("check", "pk"), ("every", "")], [("reel", ""), ("with", ""), ("Creedom", "pk")], [("before", ""), ("I", ""), ("post.", "")]],
     "r5", size=80, dark=True)
flash(t5 - .05, .8, .35)
sfx("whoosh_big", t5 - .2)
to("#bgr", t5 - .05, .2, "{opacity: 0}")
to("#bgl", t5 - .05, .2, "{opacity: 1}")
pw(t5 - .1, "scale: 1, x: 0, y: 0", .5)
screen("s5", t5)
st("#sbar", t5, '{color: "#111"}')
stat(t5, "CREEDOM CHECK", "pk")
t_ck = T("r5", "check")
js(f'tl.fromTo("#scanl", {{opacity: 1, y: 0}}, {{y: 294, duration: .55, repeat: 2, yoyo: true, ease: "sine.inOut", immediateRender: false}}, {t_ck:.3f});')
st("#scanl", t_ck + 1.7, "{opacity: 0}")
sfx("glitch", t_ck)
t_sh = T("r5", "shows")
head("h5b", [[("It", ""), ("shows", ""), ("me", ""), ("exactly", "")], [("where", ""), ("people", ""), ("would", ""), ("leave,", "rd")], [("and", ""), ("how", ""), ("to", ""), ("fix", "pk"), ("it.", "")]],
     "r5", size=74, after=t_sh - .05, dark=True)
st("#mts", t_sh - .2, '{textContent: "2 PROBLEMS FOUND"}')
ft("#rw0", t_sh, .3, "{opacity: 0, x: 40}", "{opacity: 1, x: 0}", "back.out(1.8)")
sfx("error", t_sh)
ft("#rw1", T("r5", "where") - .05, .3, "{opacity: 0, x: 40}", "{opacity: 1, x: 0}", "back.out(1.8)")
sfx("error", T("r5", "where"))
t_fx = T("r5", "how")
ft("#rw2", t_fx - .1, .3, "{opacity: 0, x: 40}", "{opacity: 1, x: 0}", "back.out(1.8)")
sfx("chime", t_fx)
ft("#score", t_fx + .2, .3, "{opacity: 0, scale: 1.4}", "{opacity: 1, scale: 1}", "back.out(2.4)")
ft("#ex5", t_fx + .3, .2, "{opacity: 0}", "{opacity: 1}", "power2.out")
ft("#post", t_fx + .25, .25, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(2)")
tap(T0["r5"][1] + .05, 330, 1085)
sfx("ding", T0["r5"][1] + .1)

# ---- r6 CTA ---------------------------------------------------------------------------------------------------------------------------
t6 = T0["r6"][0]
head("h6", [[("Comment", ""), ("GROW", "pk")], [("and", ""), ("I'll", ""), ("send", ""), ("it", ""), ("to", ""), ("you.", "")]], "r6", size=90, dark=True)
to(f"#st{len(STAT) - 1}", t6 - .2, .2, "{opacity: 0}")
pw(t6 - .25, "scale: .62, y: 560, x: -150, rotation: -6", .5)
ft("#cta", t6 - .05, .35, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.2)")
js(f'tl.fromTo("#cta b", {{scale: 1}}, {{scale: 1.05, duration: .35, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {T("r6", "GROW") + .3:.3f});')
sfx("pop", t6)
sfx("ding2", T("r6", "GROW"))
cree_to(t6 - .1, *P(*CF), d=.4, ease="power3.inOut")
pose(t6 - .05, "wave", flip=False)
cree_hop(T("r6", "GROW") + .1, 40, 2)
sparkle(t6 + .2, .6)


# ---- Cree all the way through (owner: "add the Creedom mascot like we do") -----------------------------------------------------------
CR = (930, 1810, .3)               # bottom right, beside the phone
CL = (150, 1810, .3)               # bottom left (while the phone pushes right in r4)
_x, _y, _s = P(*CR)                 # on screen from the first frame (set outside the timeline so the start state sticks)
js(f'gsap.set("#cree", {{x: {_x - 410:.0f}, y: {_y - 500:.0f}, scale: {_s}, opacity: 1}});')
js('gsap.set("#cree .cpose", {opacity: 0}); gsap.set("#cp-phone", {opacity: 1});')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -7, duration: .6, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .6)}, immediateRender: false}}, 0);')
for k in range(int(DUR / 2.4)):
    blink(1.4 + k * 2.4)
pose(T("r0", "Every"), "think")
cree_wiggle(T("r0", "minutes"), 2, 6)
pose(T("r1", "12"), "stand")
pose(T("r1", "23"), "sad")
sweat(T("r1", "23"), .9)
pose(T("r2", "hates") - .05, "shock")
cree_hop(T("r2", "hates"), 50, 1)
say(T("r2", "hates") + .1, "!", .6, left=True)
pose(T0["r3"][0] + .1, "stand")
pose(T("r3", "People") - .1, "mag", flip=True)
cree_wiggle(T("r3", "two"), 2, 5)
cree_to(T0["r4"][0] - .1, *P(*CL), d=.5)
pose(T0["r4"][0] + .2, "point", flip=False)
say(T("r4", "why"), "?", .8)
cree_to(T0["r5"][0] - .2, *P(*CR), d=.45)
pose(T0["r5"][0] - .1, "present", flip=True)
pose(T("r5", "fix") + .1, "proud")
cree_hop(T("r5", "fix") + .15, 45, 2)
sparkle(T("r5", "fix") + .1, .7)

# =======================================================================================================================
# ENERGY PASS (owner, 2026-11-23: "very dull animations, make it more attractive and fast pace with so many animations")
ICON_REF = ('<svg viewBox="0 0 100 100"><path d="M78 30 A36 36 0 1 0 84 62" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>'
            '<path d="M70 14 L82 32 L62 38 Z" fill="currentColor"/></svg>')
ICON_EYE = ('<svg viewBox="0 0 100 60"><path d="M4 30 Q50 -14 96 30 Q50 74 4 30 Z" fill="none" stroke="currentColor" stroke-width="8"/>'
            '<circle cx="50" cy="30" r="13" fill="currentColor"/></svg>')
ICON_HEART = '<svg viewBox="0 0 40 36"><path d="M20 34 C4 22 0 14 4 8 C8 1 17 2 20 9 C23 2 32 1 36 8 C40 14 36 22 20 34 Z" fill="currentColor"/></svg>'
ICON_BOLT = '<svg viewBox="0 0 60 100"><path d="M36 0 L4 58 H28 L20 100 L56 38 H32 Z" fill="#ffd23f"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="#2fbf71"/><path d="M13 25 L21 33 L36 16" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FXB, FXF = "", ""
# refresh arrows orbiting the phone, sad notifications
for k in range(3):
    FXF += f'<i class="orb" id="ob{k}">{ICON_REF}</i>'
    js(f'tl.fromTo("#ob{k}", {{opacity: 0, rotation: {k * 120}, scale: .4}}, {{keyframes: [{{opacity: 1, scale: 1, duration: .25}}, {{rotation: {k * 120 + 720}, duration: {T0["r1"][1] - 1.6:.2f}, ease: "none"}}, '
       f'{{opacity: 0, scale: .4, duration: .2}}], immediateRender: false}}, {T("r0", "refresh") - .1 + k * .25:.3f});')
NOTIFS = [("eye", "Seen by 4", 120, 760), ("heart", "0 new likes", 660, 1060), ("eye", "No new views", 90, 1180), ("heart", "1 like · from mom", 600, 1330)]
for k, (ic, txt, x, y) in enumerate(NOTIFS):
    FXF += f'<div class="nt" id="nt{k}" style="left:{x}px;top:{y}px"><i>{ICON_EYE if ic == "eye" else ICON_HEART}</i>{txt}</div>'
    tk = (T("r1", "12"), T("r1", "views") + .3, T("r1", "19"), T("r1", "23"))[k]
    ft(f"#nt{k}", tk, .3, "{opacity: 0, scale: .5, y: 30}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.6)")
    js(f'tl.to("#nt{k}", {{y: -40, opacity: 0, duration: .25, ease: "power2.in"}}, {T0["r2"][0] - .4:.3f});')
    sfx("pop", tk)
# little "+n" pops from the counter
for i in range(1, len(COUNTS)):
    d = int(COUNTS[i][0]) - int(COUNTS[i - 1][0])
    FXF += f'<b class="plus" id="pl{i}">+{d}</b>'
    js(f'tl.fromTo("#pl{i}", {{opacity: 0, y: 0, scale: .5}}, {{keyframes: [{{opacity: 1, y: -40, scale: 1, duration: .25, ease: "back.out(3)"}}, {{opacity: 0, y: -110, duration: .45}}], '
       f'immediateRender: false}}, {COUNTS[i][1]:.3f});')
# the phone never sits still: a 3D sway, and a punch on every beat
js(f'tl.fromTo("#ph", {{rotationY: -6, rotationX: 3, transformPerspective: 1600}}, {{rotationY: 6, rotationX: -3, duration: 1.3, yoyo: true, repeat: {int(DUR / 1.3)}, '
   f'ease: "sine.inOut", immediateRender: false}}, 0);')
BEATS = [T("r0", "post"), T("r0", "refresh"), T("r0", "Every"), T("r0", "five"), T("r0", "minutes"), T("r1", "12"), T("r1", "19"), T("r1", "23"),
         T("r2", "algorithm"), T("r2", "hates"), T("r3", "But"), T("r3", "People"), T("r3", "two"), T("r4", "why"), T("r5", "check"), T("r5", "Creedom"),
         T("r5", "where"), T("r5", "fix"), T("r6", "GROW")]
for t in BEATS:
    js(f'tl.fromTo("#punch", {{scale: 1}}, {{keyframes: [{{scale: 1.045, duration: .06, ease: "power2.out"}}, {{scale: 1, duration: .3, ease: "power3.out"}}], immediateRender: false}}, {t - .02:.3f});')
# conflict: lightning, red alarm, shake
for k, (x, y, r) in enumerate(((90, 560, -15), (860, 620, 18), (130, 1180, 10), (840, 1240, -12))):
    FXF += f'<i class="bolt" id="bt{k}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{ICON_BOLT}</i>'
    js(f'tl.fromTo("#bt{k}", {{opacity: 0, scale: .3}}, {{keyframes: [{{opacity: 1, scale: 1.1, duration: .1}}, {{opacity: .2, duration: .08}}, {{opacity: 1, duration: .08}}, '
       f'{{opacity: 0, scale: .8, duration: .4}}], immediateRender: false}}, {T("r2", "hates") + k * .06:.3f});')
js(f'tl.fromTo("#alarm", {{opacity: 0}}, {{opacity: .55, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}}, {T("r2", "algorithm"):.3f});')
js(f'tl.fromTo("#punch", {{x: 0, y: 0}}, {{keyframes: [{{x: -16, y: 6, duration: .04}}, {{x: 14, y: -6, duration: .04}}, {{x: -10, y: 4, duration: .04}}, {{x: 8, duration: .04}}, '
   f'{{x: 0, y: 0, duration: .04}}], immediateRender: false}}, {T("r2", "hates") + .05:.3f});')
# realisation: glitch hit, siren, viewers leave with trails
for k in range(6):
    FXF += f'<i class="gl" id="gl{k}" style="top:{random.randint(300, 1600)}px;height:{random.randint(16, 70)}px;background:{random.choice(("#ff3b4e", "#00e5ff", "#ffffff"))}"></i>'
    js(f'tl.fromTo("#gl{k}", {{opacity: 0, x: 0}}, {{keyframes: [{{opacity: .8, x: {random.choice((-80, 80))}, duration: .05}}, {{opacity: 0, duration: .05}}, '
       f'{{opacity: .6, x: {random.choice((-40, 40))}, duration: .05}}, {{opacity: 0, duration: .05}}], immediateRender: false}}, {T0["r3"][0] - .05 + k * .03:.3f});')
sfx("glitch", T0["r3"][0])
js(f'tl.fromTo("#siren", {{opacity: 0}}, {{opacity: .5, duration: .3, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false}}, {T("r3", "People"):.3f});')
for k in range(8):
    FXF += f'<i class="walk" id="wk{k}" style="left:{250 + (k % 4) * 30}px;top:{820 + (k // 4) * 60}px"></i>'
    js(f'tl.fromTo("#wk{k}", {{opacity: 0, x: 0, y: 0}}, {{keyframes: [{{opacity: 1, duration: .1}}, {{x: {random.randint(520, 760)}, y: {random.randint(-160, 120)}, opacity: 0, '
       f'duration: .7, ease: "power2.in"}}], immediateRender: false}}, {T("r3", "People") + k * .05:.3f});')
# action: spin into Creedom, burst rings, checkmark confetti, FIXED stamp
js(f'tl.fromTo("#pw", {{rotationY: 0, transformPerspective: 1600}}, {{rotationY: 360, duration: .55, ease: "power3.inOut", immediateRender: false}}, {T0["r5"][0] - .25:.3f});')
for k in range(3):
    FXF += f'<i class="ring" id="rg{k}"></i>'
    js(f'tl.fromTo("#rg{k}", {{opacity: .9, scale: .2}}, {{opacity: 0, scale: {3 + k}, duration: .7, ease: "power2.out", immediateRender: false}}, {T0["r5"][0] + k * .1:.3f});')
for k in range(14):
    FXF += f'<i class="ck" id="ck_{k}">{ICON_CHECK}</i>'
    a = random.uniform(0, 6.28)
    js(f'tl.fromTo("#ck_{k}", {{opacity: 0, x: 0, y: 0, scale: .3, rotation: 0}}, {{keyframes: [{{opacity: 1, scale: 1, x: {math.cos(a) * 300:.0f}, y: {math.sin(a) * 300 - 80:.0f}, '
       f'rotation: {random.randint(-90, 90)}, duration: .45, ease: "power3.out"}}, {{opacity: 0, y: {math.sin(a) * 300 + 120:.0f}, duration: .5, ease: "power2.in"}}], '
       f'immediateRender: false}}, {T("r5", "fix") + k * .015:.3f});')
FXF += '<div class="fixed" id="fixed">FIXED</div>'
ft("#fixed", T("r5", "fix") + .15, .22, "{opacity: 0, scale: 2.6, rotation: -20}", "{opacity: 1, scale: 1, rotation: -10}", "power4.in")
to("#fixed", T0["r6"][0] - .3, .2, "{opacity: 0}")
sfx("stamp", T("r5", "fix") + .3)
js(f'tl.fromTo("#post", {{scale: 1}}, {{scale: 1.06, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {T("r5", "fix") + .5:.3f});')
# CTA confetti
for k in range(50):
    FXF += f'<i class="cf" id="cf{k}" style="background:{random.choice(("#ff5fb7", "#F343A2", "#ffd27a", "#1a1020", "#ffffff"))};width:{random.randint(12, 20)}px;height:{random.randint(22, 32)}px"></i>'
    x0 = random.uniform(0, 1080)
    js(f'tl.fromTo("#cf{k}", {{x: {x0:.0f}, y: -60, rotation: {random.randint(0, 180)}, opacity: 1}}, {{x: {x0 + random.uniform(-160, 160):.0f}, y: 2000, rotation: {random.randint(360, 900)}, '
       f'rotationX: 720, opacity: 1, duration: {random.uniform(2.2, 3.2):.2f}, ease: "none", immediateRender: false}}, {T0["r6"][0] + random.uniform(0, .8):.3f});')

# the check is live: % counts up, the timeline fills second by second, 0:00-0:02 lights red
t_a0, t_a1 = T0["r5"][0] + .35, T("r5", "shows") - .3
ft("#ana5", t_a0 - .1, .3, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "power3.out")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 100, duration: {t_a1 - t_a0:.2f}, ease: "none", onUpdate: () => {{ document.getElementById("apct").textContent = Math.round(o.v) + "%"; }}}}, {t_a0:.3f}); }})();')
js(f'tl.fromTo("#phd", {{left: "0%"}}, {{left: "100%", duration: {t_a1 - t_a0:.2f}, ease: "none", immediateRender: false}}, {t_a0:.3f});')
for k in range(15):
    tk = t_a0 + (t_a1 - t_a0) * (k + .5) / 15
    ft(f"#seg{k}", tk, .15, "{opacity: .15, scaleY: .4}", "{opacity: 1, scaleY: 1}", "back.out(3)")
    if k < 2:
        sfx("error", tk)
    elif k % 3 == 0:
        sfx("tick", tk)
to("#ana5", t_a1 + .1, .2, "{opacity: 0, y: -20}", "power2.in")

# ---- more visual concepts -------------------------------------------------------------------------------------------------------
# a finger pulls to refresh on every refresh
FINGER = ('<svg viewBox="0 0 80 120"><path d="M30 8 Q30 0 38 0 Q46 0 46 8 V54 L60 50 Q72 48 74 60 L70 96 Q66 116 46 118 H34 Q20 116 16 100 L8 70 Q6 60 16 60 '
          'Q24 60 30 70 Z" fill="#ffd9c2" stroke="#c98d74" stroke-width="3"/></svg>')
FXF += f'<i class="finger" id="fing">{FINGER}</i>'
for i in range(1, len(COUNTS)):
    t = COUNTS[i][1]
    js(f'tl.fromTo("#fing", {{opacity: 0, y: 0, x: 0}}, {{keyframes: [{{opacity: 1, duration: .08}}, {{y: 170, duration: .3, ease: "power2.inOut"}}, {{opacity: 0, duration: .1}}], '
       f'immediateRender: false}}, {t - .5:.3f});')
# the goal bar crawls
for i, (c, t) in enumerate(COUNTS):
    pct = int(c) / 10000 * 100
    js(f'tl.to("#gfill", {{width: "{max(pct * 4, .6):.2f}%", duration: .3, ease: "power2.out"}}, {t:.3f});')
    st("#gpct", t, f'{{textContent: "{pct:.2f}%"}}')
# "People did": three viewers' phones swipe her reel away
for k, (x, y, r) in enumerate(((22, 860, -6), (884, 960, 6), (40, 1320, 4))):
    FXF += (f'<div class="mini" id="mi{k}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"><div class="ms"><div class="mr" id="mr{k}"><i></i><b>My budget meal hack</b></div>'
            f'<div class="mn" id="mn{k}"></div></div><i class="mt" id="mt{k}"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="rgba(255,255,255,.85)"/></svg></i></div>')
    tk = T("r3", "People") + k * .18
    ft(f"#mi{k}", tk - .15, .3, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2)")
    js(f'tl.fromTo("#mt{k}", {{opacity: 0, y: 0}}, {{keyframes: [{{opacity: 1, duration: .08}}, {{y: -120, duration: .25, ease: "power2.in"}}, {{opacity: 0, duration: .08}}], '
       f'immediateRender: false}}, {tk + .3:.3f});')
    js(f'tl.to("#mr{k}", {{y: -300, duration: .25, ease: "power2.in"}}, {tk + .38:.3f});')
    ft(f"#mn{k}", tk + .38, .25, "{y: 300}", "{y: 0}", "power2.out")
    sfx("swish", tk + .38)
    to(f"#mi{k}", T0["r4"][0] - .2, .25, "{opacity: 0, scale: .6}", "power2.in")
# the fix flips the first frame: before -> after
t_fx2 = T("r5", "fix")
js(f'tl.fromTo("#s5 .chk .thumb", {{rotationY: 0, transformPerspective: 800}}, {{rotationY: 90, duration: .15, ease: "power2.in", immediateRender: false}}, {t_fx2 - .1:.3f});')
ft("#aft", t_fx2 + .05, .2, "{opacity: 0, rotationY: -90, transformPerspective: 800}", "{opacity: 1, rotationY: 0}", "power2.out")
ft("#ba", t_fx2 + .2, .25, "{opacity: 0, scale: 1.6}", "{opacity: 1, scale: 1}", "back.out(2.5)")
# CTA: a comment box types GROW and sends
FXF += ('<div class="cbox" id="cbox"><i class="cav"></i><span id="cbt"><span id="cg0" style="opacity:0">G</span><span id="cg1" style="opacity:0">R</span>'
        '<span id="cg2" style="opacity:0">O</span><span id="cg3" style="opacity:0">W</span></span><b class="csend" id="csend">Post</b></div>'
        '<div class="sent" id="sent">Sent! Now check your DMs</div>')
t_cm = T0["r6"][0]
ft("#cbox", t_cm + .2, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.8)")
for k in range(4):
    st(f"#cg{k}", t_cm + .5 + k * .12, "{opacity: 1}")
    sfx("tick", t_cm + .5 + k * .12)
js(f'tl.fromTo("#csend", {{scale: 1}}, {{keyframes: [{{scale: .85, duration: .08}}, {{scale: 1, duration: .15}}], immediateRender: false}}, {t_cm + 1.05:.3f});')
sfx("click", t_cm + 1.05)
ft("#sent", t_cm + 1.2, .3, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "back.out(2)")
sfx("ding", t_cm + 1.25)

# backdrop drift
js(f'tl.fromTo("#bgn .bok", {{x: 0, y: 0}}, {{x: (i) => [60, -80, 70, -60, 50][i], y: (i) => [-90, 70, -60, 80, -40][i], duration: {DUR / 2:.2f}, yoyo: true, repeat: 1, '
   f'ease: "sine.inOut", immediateRender: false}}, 0);')

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: The refresh spiral 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="bg" id="bgn">{BOK}</div><div class="bg" id="bgr"></div><div class="bg" id="bgl"></div>
      <div id="punch">
      <div class="fxb">{FXB}</div>{PHONE}{VILLAIN}<div class="fxf">{FXF}</div></div><div id="alarm"></div><div id="siren"></div>{CTA}
      <div style="position:absolute;inset:0;z-index:33;pointer-events:none">{cree_html()}</div>
      {"".join(STAT)}
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
json.dump({"dur": DUR, "music_cut": round(t3, 3), "music_switch": round(t5, 3), "lines": T0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
