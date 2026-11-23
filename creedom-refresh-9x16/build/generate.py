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
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT  # noqa: E402
from fx import cree_html, cree_to, pose, cree_hop, sparkle, P  # noqa: E402

random.seed(5)
DUR = round(L1["r6"] + 1.6, 2)
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
COUNTS = [("0", 0), ("4", 2.0), ("6", T("r0", "Every")), ("7", T("r0", "five") + .3), ("9", T("r0", "minutes")),
          ("12", T("r1", "12")), ("19", T("r1", "19")), ("23", T("r1", "23") + .25)]
CLOCKS = ["9:00 PM", "9:05 PM", "9:10 PM", "9:15 PM", "9:20 PM", "9:40 PM", "10:15 PM", "11:30 PM"]
S2 = ('<div class="scrn" id="s2">' + THUMB.format("left:214px;top:110px;width:200px;height:200px;border-radius:24px")
      + '<div class="ins"><small>Views</small><div class="vnum">' + "".join(f'<b id="vn{i}">{c}</b>' for i, (c, _) in enumerate(COUNTS))
      + '</div><div class="vsub">in the last hour</div></div><i class="spin" id="spin"></i><div class="clock">'
      + "".join(f'<b id="ck{i}">{c}</b>' for i, c in enumerate(CLOCKS)) + '</div></div>')
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
      '<div class="chk">' + THUMB.format("") + '<i class="scanl" id="scanl"></i><div class="meta" id="meta">Checking your reel<small id="mts">BEFORE YOU POST</small></div>'
      '<div class="score" id="score">4.6<span> / 5</span></div></div>'
      '<div class="row bad" id="rw0" style="top:500px"><small>0:01 · WEAK HOOK</small>You\'re talking. Nothing on screen moves.</div>'
      '<div class="row bad" id="rw1" style="top:660px"><small>0:02 · PEOPLE LEAVE HERE</small>Most viewers would scroll past.</div>'
      '<div class="row fix" id="rw2" style="top:820px"><small>→ FIX</small>Open on the finished dish. Then explain.</div>'
      '<div class="ex5" id="ex5">EXAMPLE</div><div class="post" id="post">Post reel</div></div>')
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
CF = (900, 1760, .3)
js(f'tl.fromTo("#ph", {{y: 0, rotation: -.6}}, {{y: -8, rotation: .6, duration: 2.1, yoyo: true, repeat: {int(DUR / 2.1)}, ease: "sine.inOut", immediateRender: false}}, 0);')

# ---- r0 relatable: share, refresh, refresh ------------------------------------------------------------------------------------------
ft("#pw", 0, .5, "{y: 380, rotationX: 24, scale: .92, transformPerspective: 1600}", "{y: 0, rotationX: 0, scale: 1}", "back.out(1.3)")
sfx("whoosh", 0)
head("h0", [[("You", ""), ("post", ""), ("a", ""), ("reel…", "")], [("and", ""), ("then", ""), ("you", ""), ("refresh.", "pk")]], "r0", size=86)
stat(.1, "POV: 9:00 PM")
tap(T("r0", "post") + .1, 330, 1080)
ft("#toast", T("r0", "post") + .2, .25, "{opacity: 0, y: -30}", "{opacity: 1, y: 0}", "back.out(2)")
to("#toast", 1.4, .2, "{opacity: 0, y: -30}")
screen("s2", 1.45)
st("#vn0", 1.45, "{opacity: 1}")
st("#ck0", 1.45, "{opacity: 1}")
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
head("h0b", [[("Every.", ""), ("Five.", "pk"), ("Minutes.", "")]], "r0", size=108, after=T("r0", "Every") - .05)
stat(2.0, "REFRESHING…")

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
    st(f"#nw{i}", t2 + .35 + i * .24, "{opacity: 1}")
    sfx("tick", t2 + .35 + i * .24)
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
cree_to(t6 - .1, *P(CF[0], CF[1] + 300, CF[2]), d=.01)
st("#cree", t6 - .1, "{opacity: 1}")
pose(t6 - .1, "wave", flip=False, squash=False)
cree_to(t6 - .05, *P(*CF), d=.45, ease="back.out(1.8)")
cree_hop(T("r6", "GROW") + .1, 40, 2)
sparkle(t6 + .2, .6)

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
      {PHONE}{VILLAIN}{CTA}
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
