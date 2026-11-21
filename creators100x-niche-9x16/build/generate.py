"""Creators 100X "Make AI interview you" (keyword NICHE, 9:16), v3 "the real conversation": writes index.html,
plan/sfx_events.json and plan/edit.json from plan/words.json.

Owner on v2 (2026-11-21): "Still very dull and messy element placements and why is chatgpt in green color?" So v3 shows the
conversation the way it really looks: a ChatGPT-style chat in dark mode (neutral greys and white, no logo) on a phone in the
centre of the Creators 100X brand backdrop, with one strict layout (headline band 190..470, status pill 480..540, phone
560..1750) and the key moments lifting out of the phone as big cards. Same approved script and Kokoro af_heart voice.
  n0 hook: the phone springs in; "what should I post about?" is typed and sent; ChatGPT answers with 10 questions of its own;
  n1 first peak: a new chat, "give me content ideas", the generic list everyone gets; SEEN IT stamp, buzzer;
  n2 release, on the music's drop: the phone flips; the prompt lifts out as a big card, typed (COPY THIS PROMPT), then is sent;
  n3 build: the interview plays out in the chat, question by question, answer by answer (QUESTION 1/10 -> 10/10);
  n4 peak: "3 niches only you could own" streams in, and the three lift out of the phone as cards (examples);
  n5 release: the answers fly into niche 1; 100% YOURS;
  n6 CTA: the phone drops away; the free PDF and COMMENT NICHE.
python3 build/generate.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, ROOT  # noqa: E402

random.seed(3)
DUR = round(L1["n6"] + 1.6, 2)
T0 = {k: (L0[k], L1[k]) for k in LINES}

# ---- headlines (top band) ---------------------------------------------------------------------------------------------------------
HTMLS, OPEN, WID = [], [None], [0]


def head(hid, rows, line, size=84, after=0.0):
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
    HTMLS.append(f'<div class="head" id="{hid}" style="font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out_:
        ft(f"#{wid}", t - .05, .3, "{opacity: 0, filter: 'blur(10px)', y: 24}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out_)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .25, .18, "{opacity: 0, filter: 'blur(12px)', y: -30}", "power2.in")
    OPEN[0] = hid


STAT = []


def stat(t, text, t_out=None):
    i = len(STAT)
    STAT.append(f'<div class="stat" id="st{i}"><span>{text}</span></div>')
    if i:
        to(f"#st{i - 1}", t - .05, .15, "{opacity: 0, y: -14}", "power2.in")
    ft(f"#st{i}", t, .3, "{opacity: 0, y: 14, scale: .9}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
    if t_out:
        to(f"#st{i}", t_out, .2, "{opacity: 0, y: -14}", "power2.in")


# ---- chat helpers ------------------------------------------------------------------------------------------------------------------
def words(prefix, text):
    """'a *b* c' -> spans with ids prefix0..; *x* bold, _x_ lime highlight"""
    out_, n = [], 0
    for w in text.split():
        cls, inner = "w", w
        if inner.startswith("*") and inner.rstrip(".,:").endswith("*"):
            inner = "<b>" + inner.strip("*").replace("*", "") + "</b>"
        if inner.startswith("_") and inner.rstrip(".,:").endswith("_"):
            inner = f'<span class="hlite">{inner.strip("_").replace("_", "")}</span>'
        out_.append(f'<span class="{cls}" id="{prefix}{n}">{inner}</span>')
        n += 1
    return " ".join(out_), n


def stream(prefix, n, t0, t1):
    for i in range(n):
        st(f"#{prefix}{i}", t0 + (t1 - t0) * i / max(n - 1, 1), "{opacity: 1}")


def bubble(sel, t):
    ft(sel, t, .35, "{opacity: 0, y: 30, scale: .9, transformOrigin: '100% 100%'}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")


def tap(t):
    js(f'tl.fromTo("#cur", {{opacity: 0, scale: 1.6}}, {{keyframes: [{{opacity: 1, scale: 1, duration: .14}}, {{scale: .8, duration: .06}}, {{opacity: 0, scale: 1.4, duration: .18}}], '
       f'immediateRender: false}}, {t - .12:.3f});')
    sfx("click", t)


def pw(t, props, d=.6, ease="power3.inOut"):
    js(f'tl.to("#pw", {{{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def flash(t, o=.7, d=.35):
    st("#flash", t, f"{{opacity: {o}}}")
    to("#flash", t + .02, d, "{opacity: 0}", "power2.out")


def screen_in(sid, t, d=.4):
    ft(f"#{sid}", t, d, "{opacity: 0, x: 120}", "{opacity: 1, x: 0}", "power3.out")


def screen_out(sid, t, d=.3):
    to(f"#{sid}", t, d, "{opacity: 0, x: -120}", "power2.in")


# =======================================================================================================================
# CONTENT
INP = {}


def inp_text(key, text):
    h, n = words(f"i{key}", text)
    INP[key] = (h, n)
    return n


n_i1 = inp_text("a", "what should I post about?")
n_i2 = inp_text("b", "give me content ideas")

# s1: the hook chat
s1_ai, n_s1 = words("s1a", "Before I answer, let me ask you _10_ _questions_ first. *Question* *1:* What do friends always ask you for help with?")
S1 = (f'<div class="screen" id="s1"><div class="empty" id="s1e">What can I help with?</div><div class="feed">'
      f'<div class="m u" id="s1u" style="opacity:0">what should I post about?</div><div class="dots3" id="s1d" style="opacity:0"><i></i><i></i><i></i></div>'
      f'<div class="m a">{s1_ai}</div></div></div>')
# s2: what most people type
s2_ai, n_s2 = words("s2a", "Sure! Here are some content ideas for you:")
IDEAS = ["Day in my life", "Morning routine", "What I eat in a day", "Get ready with me", "Q&amp;A with followers", "My desk setup tour", "Study with me"]
S2 = (f'<div class="screen" id="s2" style="opacity:0"><div class="feed"><div class="m u" id="s2u" style="opacity:0">give me content ideas</div>'
      f'<div class="m a" id="s2l">{s2_ai}<ol>' + "".join(f'<li class="w" id="s2i{i}">{t}</li>' for i, t in enumerate(IDEAS)) + '</ol></div></div></div>')
# s3: the prompt, sent
PROMPT = ("Ask me 10 questions about my life, my skills and what I can't stop talking about. One question at a time, and wait for my answer. "
          "Then suggest 3 niches only I could own, with 5 reel ideas for each.")
S3 = (f'<div class="screen" id="s3" style="opacity:0"><div class="feed"><div class="m u" id="s3u" style="opacity:0;max-width:520px">{PROMPT}</div>'
      f'<div class="dots3" id="s3d" style="opacity:0"><i></i><i></i><i></i></div></div></div>')
# s4: the interview
INTV = [("a", "Love it. *Question* *1:* What do friends always ask you for help with?"), ("u", "Cooking cheap meals for my hostel friends"),
        ("a", "*Question* *4:* What could you talk about for an hour?"), ("u", "Hostel life hacks, honestly"),
        ("a", "*Question* *7:* What did you learn the hard way?"), ("u", "How to eat well when you're broke")]
S4 = '<div class="screen" id="s4" style="opacity:0"><div class="feed" id="f4">'
N4 = []
for i, (who, text) in enumerate(INTV):
    if who == "a":
        h, n = words(f"s4m{i}w", text)
        S4 += f'<div class="m a" id="s4m{i}">{h}</div>'
        N4.append(n)
    else:
        S4 += f'<div class="m u" id="s4m{i}" style="opacity:0">{text}</div>'
        N4.append(0)
S4 += '</div></div>'
# s5: the result
s5_ai, n_s5 = words("s5a", "Based on your answers, here are _3_ _niches_ _only_ _you_ _could_ _own:_")
NICHES = ["Budget meals for hostel students", "Gym tips for skinny beginners", "Aesthetic exam notes"]
S5 = (f'<div class="screen" id="s5" style="opacity:0"><div class="feed"><div class="m a">{s5_ai}<ol>'
      + "".join(f'<li class="w" id="s5i{i}"><b>{t}</b></li>' for i, t in enumerate(NICHES)) + '</ol></div></div></div>')
INPUT = ('<div class="inp" id="inp"><span class="plus">+</span><span class="ph" id="iph">Ask anything</span>'
         f'<span id="ia" style="position:absolute;left:76px;top:26px;right:96px">{INP["a"][0]}</span>'
         f'<span id="ib" style="position:absolute;left:76px;top:26px;right:96px">{INP["b"][0]}</span><i class="send"></i></div>')
PHONE = (f'<div id="pw"><div id="phone"><div id="scr"><div class="sbar"><span>9:41</span><span>5G</span></div><i class="island"></i>'
         f'<div class="cbar"><i class="ic l"></i>ChatGPT <small>&#9662;</small><i class="ic r"></i></div>'
         f'{S1}{S2}{S3}{S4}{S5}{INPUT}</div></div><i class="cur" id="cur" style="left:554px;top:1098px"></i></div>')

# pop-outs
PW_ = []
for i, w in enumerate(PROMPT.split()):
    mk = w.strip(".,") in ("Ask", "me", "10", "questions", "One", "question", "at", "a", "time", "3", "niches", "only", "I", "could", "own") and i not in (7, 8, 11, 33)
    PW_.append(f'<span class="w{" mk" if mk else ""}" id="pp{i}">{w}</span>')
POPS = (f'<div class="pop card pcard" id="pcard"><span class="tag">COPY THIS PROMPT</span><div class="txt">{" ".join(PW_)}</div></div>'
        + "".join(f'<div class="pop card ncard{" p" if i == 1 else ""}" id="nc{i}" style="top:{640 + i * 180}px"><b>{i + 1}</b>{t}</div>' for i, t in enumerate(NICHES))
        + '<div class="pop nex" id="nex">EXAMPLES</div><div class="pop stamp" id="seen"><b>SEEN IT</b></div>'
        + '<div class="pop yours" id="yours"><span>100% YOURS</span></div>'
        + "".join(f'<div class="pop" id="an{i}" style="left:{x}px;top:{y}px"><span class="hlite" style="display:inline-block;padding:14px 24px;border-radius:30px;'
                  f'font:700 36px Inter;box-shadow:0 10px 24px rgba(16,17,17,.15)">{t}</span></div>'
                  for i, (t, x, y) in enumerate((("cooks for friends", 120, 1420), ("always broke", 560, 1480), ("hostel life", 260, 1560)))))
CTA = ('<img id="blogo" src="assets/img/logo.png" alt=""><div class="pop pdf" id="pdf"><img src="assets/img/logo.png" alt=""><span class="k">FREE PROMPT PACK</span>'
       '<h3>Let AI <span>interview</span> you</h3><p>The prompt + 5 more to plan your first 10 reels.</p></div><div class="pop free" id="free">FREE PDF</div>'
       '<div class="pop kw" id="kw"><span>COMMENT NICHE</span></div>')
BACK = ('<div class="dots" id="dots"></div>'
        '<i class="glo" id="g0" style="left:-380px;top:-300px;width:1100px;height:1100px;background:radial-gradient(closest-side,#CEFB8F,rgba(206,251,143,0))"></i>'
        '<i class="glo" id="g1" style="left:420px;top:-260px;width:1100px;height:1100px;background:radial-gradient(closest-side,#FE70B3,rgba(254,112,179,0));opacity:.75"></i>'
        '<i class="glo" id="g2" style="left:-420px;top:1180px;width:1100px;height:1100px;background:radial-gradient(closest-side,#FE70B3,rgba(254,112,179,0));opacity:.6"></i>'
        '<i class="glo" id="g3" style="left:400px;top:1150px;width:1100px;height:1100px;background:radial-gradient(closest-side,#CEFB8F,rgba(206,251,143,0))"></i>')
COLS = ("#CCFB79", "#FD0B68", "#101111", "#FE70B3", "#ffffff")
CONF = 70
CONFH = "".join(f'<i class="cf" id="cf{i}" style="background:{random.choice(COLS)};width:{random.randint(12, 20)}px;height:{random.randint(22, 34)}px"></i>' for i in range(CONF))

# =======================================================================================================================
# TIMELINE
# always alive: the backdrop drifts, the phone floats
for i, (dx, dy) in enumerate(((120, 80), (-110, 90), (100, -80), (-120, -70))):
    js(f'tl.fromTo("#g{i}", {{x: 0, y: 0, scale: 1}}, {{x: {dx}, y: {dy}, scale: 1.15, duration: {DUR / 2:.2f}, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#dots", {{y: 0}}, {{y: -46 * 6, duration: {DUR}, ease: "none", immediateRender: false}}, 0);')
js(f'tl.fromTo("#phone", {{y: 0, rotation: -.6}}, {{y: -10, rotation: .6, duration: 2.2, yoyo: true, repeat: {int(DUR / 2.2)}, ease: "sine.inOut", immediateRender: false}}, 0);')

# ---- n0 hook -----------------------------------------------------------------------------------------------------------------------
ft("#pw", 0, .6, "{y: 420, rotationX: 28, scale: .92, transformPerspective: 1600}", "{y: 0, rotationX: 0, scale: 1}", "back.out(1.3)")
sfx("whoosh_big", 0)
head("h0", [[("I", ""), ("asked", ""), ("ChatGPT", "")], [("what", ""), ("I", ""), ("should", ""), ("post", "pk"), ("about.", "")]], "n0", size=86)
st("#iph", .35, "{opacity: 0}")
stream("ia", n_i1, .4, 1.75)
for k in range(5):
    sfx("tick", .45 + k * .28)
tap(1.95)
st("#ia", 2.0, "{opacity: 0}")
st("#iph", 2.0, "{opacity: 1}")
to("#s1e", 1.95, .2, "{opacity: 0}")
bubble("#s1u", 2.0)
sfx("whoosh", 2.0)
ft("#s1d", 2.25, .15, "{opacity: 0}", "{opacity: 1}")
js('tl.fromTo("#s1d i", {opacity: .3}, {opacity: 1, duration: .15, yoyo: true, repeat: 2, stagger: .08, immediateRender: false}, 2.25);')
st("#s1d", T("n0", "It") - .02, "{opacity: 0, height: 0, marginTop: 0}")
stream("s1a", n_s1, T("n0", "It") - .05, T0["n0"][1] + .4)
t_ten = T("n0", "ten")
pw(T("n0", "It") - .2, "scale: 1.14, y: 70", .6, "power3.inOut")
pw(t_ten - .05, "scale: 1.2, y: 70", .2, "power2.out")
pw(t_ten + .2, "scale: 1.14, y: 70", .4, "power3.out")
sfx("ping", t_ten)
stat(T("n0", "asked", 1), "IT ASKED ME BACK")

# ---- n1 first peak: what most people type ------------------------------------------------------------------------------------------
t_gv = T("n1", "Give")
head("h1", [[("\"Give", ""), ("me", ""), ("content", ""), ("ideas\"", "")], [("gets", ""), ("the", ""), ("same", "pk"), ("ideas", "")], [("as", ""), ("everyone", ""), ("else.", "")]],
     "n1", size=80)
stat(t_gv - .1, "WHAT MOST PEOPLE TYPE")
screen_out("s1", t_gv - .25)
pw(t_gv - .25, "scale: 1, y: 0", .45)
pw(T("n1", "gets") - .2, "scale: 1.12, y: 60", .6)
screen_in("s2", t_gv - .05)
sfx("swish", t_gv - .2)
st("#iph", t_gv, "{opacity: 0}")
stream("ib", n_i2, t_gv, t_gv + .5)
tap(t_gv + .62)
st("#ib", t_gv + .66, "{opacity: 0}")
st("#iph", t_gv + .66, "{opacity: 1}")
bubble("#s2u", t_gv + .68)
t_l = T("n1", "gets") - .2
stream("s2a", n_s2, t_l, t_l + .35)
for i in range(len(IDEAS)):
    ft(f"#s2i{i}", t_l + .4 + i * .16, .2, "{opacity: 0, x: -14}", "{opacity: 1, x: 0}", "power2.out")
    sfx("tick", t_l + .4 + i * .16)
t_ev = T("n1", "everyone")
js(f'tl.to("#s2l", {{color: "#6a6a6a", duration: .2}}, {t_ev:.3f});')
ft("#seen", t_ev - .05, .22, "{opacity: 0, scale: 2.4}", "{opacity: 1, scale: 1}", "power4.in")
sfx("buzzer", t_ev)
sfx("stamp", t_ev)
js(f'tl.fromTo("#pw", {{x: 0}}, {{keyframes: [{{x: -18, duration: .05}}, {{x: 16, duration: .05}}, {{x: -10, duration: .05}}, {{x: 6, duration: .05}}, {{x: 0, duration: .05}}], '
   f'immediateRender: false}}, {t_ev + .12:.3f});')

# ---- n2 release, on the drop: flip it; the prompt lifts out --------------------------------------------------------------------
t_fl = T("n2", "flip")
head("h2", [[("So", ""), ("flip", "pk"), ("it.", "")], [("Ask", ""), ("it", ""), ("to", ""), ("interview", "lm"), ("you.", "")]], "n2", size=92)
stat(t_fl - .1, "THE FLIP")
to("#seen", t_fl - .2, .2, "{opacity: 0, scale: 1.6}", "power2.in")
pw(t_fl - .3, "scale: 1, y: 0", .2)
js(f'tl.fromTo("#pw", {{rotationY: 0, transformPerspective: 1600}}, {{rotationY: 360, duration: .6, ease: "power3.inOut", immediateRender: false}}, {t_fl - .2:.3f});')
st("#s2", t_fl + .1, "{opacity: 0}")
st("#s3", t_fl + .1, "{opacity: 1}")
flash(t_fl + .05, .6, .3)
sfx("whoosh_big", t_fl - .2)
sfx("impact", t_fl + .05)
st("#iph", t_fl + .1, "{opacity: 1}")
t_pc = t_fl + .45
ft("#dim", t_pc, .3, "{opacity: 0}", "{opacity: .7}", "power2.out")
ft("#pcard", t_pc, .5, "{opacity: 0, scale: .5, y: 300, rotationX: -30, transformPerspective: 1400}", "{opacity: 1, scale: 1, y: 0, rotationX: 0}", "back.out(1.4)")
sfx("whoosh", t_pc)
stream("pp", len(PROMPT.split()), t_pc + .3, t_pc + 1.6)
for k in range(8):
    sfx("tick", t_pc + .3 + k * .16)
js(f'tl.fromTo("#pcard", {{rotationX: 0, rotationY: 0, transformPerspective: 1600}}, {{rotationX: 3, rotationY: -4, duration: 1.5, yoyo: true, repeat: 1, ease: "sine.inOut", '
   f'immediateRender: false}}, {t_pc + .5:.3f});')
t_snd = T0["n2"][1] + .05
to("#pcard", t_snd, .35, "{opacity: 0, scale: .35, y: 520, x: 120}", "power3.in")
to("#dim", t_snd, .3, "{opacity: 0}")
bubble("#s3u", t_snd + .3)
sfx("whoosh", t_snd)

# ---- n3 build: the interview ---------------------------------------------------------------------------------------------------------
t_qa = T0["n3"][0]
head("h3", [[("About", ""), ("your", ""), ("life,", "")], [("your", ""), ("skills,", "lm"), ("what", ""), ("you", "")], [("can't", ""), ("stop", ""), ("talking", "pk"), ("about.", "")]],
     "n3", size=78)
st("#s3", t_qa - .05, "{opacity: 0}")
st("#s4", t_qa - .05, "{opacity: 1}")
pw(t_qa - .1, "scale: 1.12, y: 70", .5)
QT = [t_qa, T("n3", "life") + .1, T("n3", "skills") + .05, T("n3", "what") + .1, T("n3", "can't") + .1, T("n3", "talking") + .05]
SCROLL = [0, 0, -205, 0, -500, 0]
QLAB = ["QUESTION 1/10", None, "QUESTION 4/10", None, "QUESTION 7/10", None]
for i, (who, text) in enumerate(INTV):
    ti = QT[i]
    if who == "a":
        stream(f"s4m{i}w", N4[i], ti, ti + .42)
        sfx("ping", ti)
    else:
        bubble(f"#s4m{i}", ti)
        sfx("pop", ti)
    if SCROLL[i]:
        js(f'tl.to("#f4", {{y: {SCROLL[i]}, duration: .35, ease: "power3.out"}}, {ti - .05:.3f});')
    if QLAB[i]:
        stat(ti, QLAB[i])
stat(T0["n3"][1] - .15, "10/10 ANSWERED")
sfx("chime", T0["n3"][1] - .15)

# ---- n4 peak: three niches, lifted out ---------------------------------------------------------------------------------------------
t_th = T0["n4"][0]
head("h4", [[("Then", ""), ("ask", ""), ("for", ""), ("three", "pk")], [("niches", ""), ("only", ""), ("you", "lm")], [("could", ""), ("own.", "")]], "n4", size=82)
stat(t_th - .1, "YOUR RESULT")
screen_out("s4", t_th - .2, .2)
screen_in("s5", t_th - .05, .3)
pw(t_th - .2, "scale: 1, y: 0", .4)
sfx("drumroll", t_th - .1)
stream("s5a", n_s5, t_th, t_th + .6)
NT = [T("n4", "only") - .1, T("n4", "could") - .05, T("n4", "own") + .2]
for i, tn in enumerate(NT):
    ft(f"#s5i{i}", tn - .3, .2, "{opacity: 0}", "{opacity: 1}", "power2.out")
    ft(f"#nc{i}", tn, .5, "{opacity: 0, scale: .45, y: " + str(1250 - (640 + i * 180)) + ", rotationX: -50, transformPerspective: 1200}",
       "{opacity: 1, scale: 1, y: 0, rotationX: 0}", "back.out(1.5)")
    sfx("stamp2" if i < 2 else "stamp", tn + .15)
ft("#dim", NT[0], .3, "{opacity: 0}", "{opacity: .72}", "power2.out")
ft("#nex", NT[2] + .4, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
flash(NT[2] + .15, .35, .3)

# ---- n5 release: built from your answers ------------------------------------------------------------------------------------------
t_bu = T0["n5"][0]
head("h5", [[("Built", ""), ("from", ""), ("your", "")], [("answers.", "lm")], [("Nobody", ""), ("can", ""), ("copy", "pk"), ("that.", "")]], "n5", size=84)
stat(t_bu - .1, "BUILT FROM YOU")
for i in range(3):
    tc = t_bu + .05 + i * .14
    ft(f"#an{i}", tc, .3, "{opacity: 0, scale: .5, y: 40}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.4)")
    js(f'tl.to("#an{i}", {{x: {[180, -220, 60][i]}, y: {[-760, -820, -900][i]}, scale: .3, opacity: 0, duration: .45, ease: "power3.in"}}, {tc + .5:.3f});')
    sfx("pop", tc)
t_hit = t_bu + 1.05
js(f'tl.to("#nc0", {{scale: 1.06, boxShadow: "0 40px 90px rgba(16,17,17,.28), 0 0 0 8px #CCFB79", duration: .25, ease: "back.out(2)"}}, {t_hit:.3f});')
for i in (1, 2):
    js(f'tl.to("#nc{i}", {{opacity: .35, scale: .96, duration: .3}}, {t_hit:.3f});')
sfx("chime", t_hit)
t_nb = T("n5", "Nobody")
ft("#yours", t_nb - .05, .3, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "back.out(2.2)")
sfx("ding2", t_nb)
js(f'tl.fromTo("#yours span", {{scale: 1}}, {{scale: 1.05, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_nb + .3:.3f});')

# ---- n6 CTA ---------------------------------------------------------------------------------------------------------------------------
t_cm = T("n6", "Comment")
head("h6", [[("Comment", ""), ("NICHE", "pk")], [("I'll", ""), ("send", ""), ("the", ""), ("exact", ""), ("prompt", "lm")], [("plus", ""), ("five", ""), ("more.", "")]], "n6", size=78)
st("#st" + str(len(STAT) - 1), t_cm - .2, "{opacity: 0}")
for s in ("#nc0", "#nc1", "#nc2", "#nex", "#yours"):
    to(s, t_cm - .25, .25, "{opacity: 0, y: -60}", "power2.in")
to("#dim", t_cm - .25, .25, "{opacity: 0}")
pw(t_cm - .3, "y: 1400, rotationX: 20", .5, "power3.in")
sfx("whoosh_big", t_cm - .3)
ft("#blogo", t_cm, .4, "{opacity: 0, y: -30}", "{opacity: 1, y: 0}", "power3.out")
ft("#kw", t_cm + .1, .4, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2.2)")
js(f'tl.fromTo("#kw span", {{scale: 1}}, {{scale: 1.05, duration: .35, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}}, {t_cm + .6:.3f});')
sfx("ding", t_cm + .1)
t_pd = T("n6", "exact") - .15
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
      {BACK}
      {PHONE}
      <div id="dim"></div>
      {POPS}
      {CTA}
      {"".join(STAT)}
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
