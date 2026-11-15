"""Creators 100X: "Stop typing 'write me a script'" 9:16 reel (1080x1920, 30 fps, 30 s), for beginner creators using AI.

Owner's picks: topic 1 (the 4-part prompt formula), visual style B (before / after split screen): the top half is
"what beginners do" (greyed out, glitchy, a one-line prompt and a generic answer), the bottom half "what works" (full
colour, the prompt built in four parts as the voice names them, each part lighting a chip and striking out the matching
"missing" chip above; then a script that sounds like a person). Hook full screen with the line on screen from frame 0;
CTA full screen: comment "PROMPT", the PDF cover (brands/creators-100x/pdf/creators100x_10-prompts-that-sound-like-you).
Brand: brands/creators-100x/brand.md (off-white page, lime and pink corner glows, ink type, one hot-pink accent per
line, lime highlighter, black pills with lime text), Inter 800/700/600. The chat window is a generic "AI chat", no
product's branding. The example prompts and answers are our own writing.
Clock: the VO (build/vo_assemble.py -> plan/words.json, plan/lines.json); cuts snap to the music's beat grid.
python3 build/generate.py  ->  index.html, plan/edit.json, plan/sfx_events.json
"""
import html as H
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
LINES = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "plan", "lines.json")))}
DUR = 30.0
INK, PINK, LIME, PAGE, GREY = "#101111", "#FD0B68", "#CCFB79", "#FDF4F4", "#8A8A8A"
SEAM = 960                                   # the split line
A, SFX, BODY, CAPS = [], [], [], []
R = random.Random(11)


def js(s):
    A.append("      " + s)


def sfx(kind, t, gain=0.0):
    SFX.append({"type": kind, "t": round(max(0.0, t), 3), "gain": gain})


def norm(w):
    return w.lower().strip(".,?!:'\"")


def T(word, after=0.0, key="s"):
    for w in WORDS:
        if w["s"] >= after - .05 and norm(w["w"]) == norm(word):
            return w[key]
    raise KeyError(word)


def L(i, key="s"):
    return LINES[f"p{i:02d}"][key]


def words_html(text, cls):
    """each word in its own span (for typing / streaming reveals); \n = line break"""
    out = []
    for i, line in enumerate(text.split("\n")):
        if i:
            out.append("<br>")
        out.append(" ".join(f'<span class="{cls}">{H.escape(w)}</span>' for w in line.split(" ")))
    return "".join(out)


def reveal(sel, t0, t1, n_hint=None, kind="type"):
    """word-by-word reveal of sel's spans between t0 and t1 (typing = keystroke sounds, stream = a soft tick at start)"""
    js(f'tl.fromTo("{sel}", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: {{amount: {max(.05, t1 - t0):.3f}}}, immediateRender: false}}, {t0:.3f});')
    if kind == "type":
        t = t0
        while t < t1:
            sfx("key", t, -4 + R.uniform(-3, 2))
            t += R.uniform(.07, .12)


def ic(name, cls="ic"):
    P = {"x": '<path d="M6 6l12 12M18 6L6 18"/>', "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
         "send": '<path d="M4 12l16-8-6 16-3-7z"/>', "spark": '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/>'}
    return f'<svg class="{cls}" viewBox="0 0 24 24">{P[name]}</svg>'


def window(wid, inner, extra=""):
    return (f'<div class="win" id="{wid}" {extra}><div class="wh"><span class="wdot">{ic("spark", "sp")}</span><b>AI chat</b>'
            f'<i></i><i></i><i></i></div><div class="wb">{inner}</div></div>')


# ---------------------------------------------------------------- copy (our own examples)
BAD_PROMPT = "Write me a reel script about fitness."
BAD_REPLY = "Hey guys! Are you ready to level up your fitness journey? Here are 5 amazing tips that will totally transform your body!"
PARTS = [("WHO YOU ARE", "I'm a fitness creator with 3K followers."),
         ("WHO IT'S FOR", "Write for busy beginners who skip the gym."),
         ("THE HOOK", "Open with a mistake they're making."),
         ("THE FORMAT", "30 seconds. 3 tips. One line each.")]
MISSING = ["No voice", "No audience", "No hook", "No format"]
GOOD_REPLY = ["Skipping the gym because you have no time?", "Your workout is too long.",
              "1. Ten minutes beats zero.", "2. Squats while the kettle boils.", "3. Take the stairs, every time."]


def build():
    t_split = L(1) - .1
    t_cta = L(7) - .12
    # ---------------- TOP: what beginners do (full screen during the hook)
    ghosts = "".join(f'<div class="ghost" id="gh{i}" style="--r:{r}deg;--x:{x}px;--y:{y}px">{H.escape(BAD_REPLY)}</div>'
                     for i, (r, x, y) in enumerate([(-6, -60, 70), (5, 70, 120), (-3, -20, 170)]))
    win_a = window("wa", f'<div class="ub" id="ubA">{words_html(BAD_PROMPT, "wa1")}</div>'
                         f'<div class="dots" id="dotsA"><i></i><i></i><i></i></div>'
                         f'<div class="rb" id="rbA">{words_html(BAD_REPLY, "wa2")}</div>')
    miss = "".join(f'<div class="mc" id="mc{i}">{ic("x")}<span>{m}</span></div>' for i, m in enumerate(MISSING))
    BODY.append(f'<div class="panel" id="tp"><div class="lab grey" id="tpl">{ic("x")}WHAT BEGINNERS DO</div>'
                f'<div class="gwrap" id="gw">{ghosts}</div>{win_a}<div class="same" id="same">Same script as everyone else</div>'
                f'<div class="miss" id="miss">{miss}</div><div class="stamp grey" id="stA">GENERIC</div></div>')
    # hook line, readable on frame 0
    BODY.append(f'<div class="hook" id="hook"><span>STOP TYPING</span><span class="pk">"WRITE ME A SCRIPT"</span></div>')
    # frame 0 is mid-story: the prompt is half typed already
    t_send = T("script.") + .2
    js(f'tl.fromTo("#ubA .wa1:nth-child(n+4)", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: {{amount: {t_send - .5:.3f}}}, immediateRender: false}}, .25);')
    t = .25
    while t < t_send:
        sfx("key", t, -5 + R.uniform(-3, 2))
        t += R.uniform(.07, .12)
    sfx("send", t_send)
    js(f'tl.fromTo("#dotsA", {{opacity: 0}}, {{opacity: 1, duration: .15}}, {t_send + .05:.3f}); tl.set("#dotsA", {{opacity: 0}}, {T("ai") + .1:.3f});')
    js(f'tl.fromTo("#dotsA i", {{y: 0}}, {{y: -10, duration: .18, yoyo: true, repeat: 3, stagger: .08, ease: "sine.inOut", immediateRender: false}}, {t_send + .05:.3f});')
    t_r = T("ai") + .1
    js(f'tl.set("#rbA", {{opacity: 1}}, {t_r:.3f});')
    reveal("#rbA .wa2", t_r, T("this.") + .35, kind="stream")
    sfx("ding", t_r, -4)
    # "The same script everyone else got": copies fan out behind the window
    t_same = T("same") - .05
    js(f'tl.fromTo("#gw .ghost", {{opacity: 0, x: 0, y: 0, rotation: 0}}, {{opacity: .55, x: (i, el) => +el.style.getPropertyValue("--x").replace("px",""), '
       f'y: (i, el) => +el.style.getPropertyValue("--y").replace("px",""), rotation: (i, el) => +el.style.getPropertyValue("--r").replace("deg",""), '
       f'duration: .45, stagger: .12, ease: "back.out(1.6)", immediateRender: false}}, {t_same:.3f});')
    js(f'tl.fromTo("#same", {{opacity: 0, scale: .6}}, {{opacity: 1, scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false}}, {T("everyone") - .05:.3f});')
    for i in range(3):
        sfx("pop", t_same + i * .12, -10)
    js(f'tl.fromTo("#hook span", {{yPercent: 0}}, {{yPercent: -120, duration: .35, ease: "power3.in", stagger: .05, immediateRender: false}}, {t_split - .35:.3f});')
    js(f'tl.set("#hook", {{opacity: 0}}, {t_split:.3f});')
    # ---------------- SPLIT ("Same AI. One better prompt. Watch.")
    js(f'tl.to("#gw, #same", {{opacity: 0, duration: .2}}, {t_split - .2:.3f});')
    js(f'tl.fromTo("#tp", {{clipPath: "inset(0px 0px 0px 0px)"}}, {{clipPath: "inset(0px 0px {FH - SEAM + 6}px 0px)", duration: .55, ease: "expo.inOut", immediateRender: false}}, {t_split:.3f});')
    js(f'tl.fromTo("#wa", {{y: 0, scale: 1}}, {{y: -250, scale: .72, duration: .55, ease: "expo.inOut", immediateRender: false}}, {t_split:.3f});')
    js(f'tl.fromTo("#wa", {{filter: "grayscale(0)", opacity: 1}}, {{filter: "grayscale(1)", opacity: .78, duration: .5, immediateRender: false}}, {t_split + .2:.3f});')
    js(f'tl.fromTo("#tpl", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: .3, immediateRender: false}}, {t_split + .4:.3f});')
    js(f'tl.fromTo("#miss .mc", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .3, stagger: .06, immediateRender: false}}, {t_split + .5:.3f});')
    sfx("whoosh", t_split, -3)
    # ---------------- BOTTOM: what works
    chips = "".join(f'<div class="pc" id="pc{i}"><b>{i + 1}</b>{lab}</div>' for i, (lab, _) in enumerate(PARTS))
    lines = "".join(f'<div class="pl" id="pl{i}"><b>{i + 1}</b><span>{words_html(txt, f"wb{i}")}</span></div>' for i, (_, txt) in enumerate(PARTS))
    reply = "".join(f'<div class="gl">{words_html(l, "wr")}</div>' for l in GOOD_REPLY)
    win_b = window("wbw", f'<div class="ub good" id="ubB">{lines}<span class="cur" id="curB"></span></div>'
                          f'<div class="dots" id="dotsB"><i></i><i></i><i></i></div><div class="rb good" id="rbB">{reply}</div>')
    BODY.append(f'<div class="panel low" id="bp"><div class="lab" id="bpl">{ic("check")}WHAT WORKS</div><div class="pcs">{chips}</div>{win_b}'
                f'<div class="stamp lime" id="stB">{ic("check")}SOUNDS LIKE YOU</div></div>')
    BODY.append('<i class="seamline" id="seam"></i>')
    js(f'tl.fromTo("#bp", {{y: {FH - SEAM}}}, {{y: 0, duration: .55, ease: "expo.inOut", immediateRender: false}}, {t_split:.3f});')
    js(f'tl.fromTo("#seam", {{scaleX: 0, opacity: 1}}, {{scaleX: 1, duration: .5, ease: "expo.out", immediateRender: false}}, {t_split + .3:.3f});')
    js(f'tl.fromTo("#bpl", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .3, immediateRender: false}}, {t_split + .45:.3f});')
    js(f'tl.fromTo(".pc", {{opacity: 0, y: 16}}, {{opacity: 1, y: 0, duration: .3, stagger: .06, immediateRender: false}}, {t_split + .55:.3f});')
    # each part: typed on its spoken phrase, chip lights up, the matching "missing" chip above is struck
    starts = [T("a", L(2)), T("busy"), T("open"), T("thirty", L(5))]
    ends = [T("followers.", key="e"), T("gym.", key="e"), T("making.", key="e"), T("each.", key="e")]
    cues = [T("first"), T("then"), T("now"), T("and", L(5))]
    for i in range(4):
        a, b = starts[i] - .05, ends[i] + .05
        js(f'tl.set("#pl{i}", {{display: "flex"}}, {a:.3f});')
        if i == 0:
            js(f'tl.fromTo("#ubB", {{opacity: 0, scale: .9}}, {{opacity: 1, scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false}}, {a - .05:.3f});')
        reveal(f"#pl{i} .wb{i}", a, b)
        js(f'tl.fromTo("#pc{i}", {{backgroundColor: "rgba(16,17,17,0)", color: "{INK}", scale: 1}}, {{backgroundColor: "{INK}", color: "{LIME}", scale: 1.08, '
           f'duration: .25, ease: "back.out(2.4)", immediateRender: false}}, {cues[i]:.3f});')
        js(f'tl.to("#pc{i}", {{scale: 1, duration: .2}}, {cues[i] + .3:.3f});')
        js(f'tl.fromTo("#mc{i}", {{backgroundColor: "rgba(255,255,255,.6)", color: "{GREY}"}}, {{backgroundColor: "{PINK}", color: "#ffffff", duration: .2, immediateRender: false}}, {cues[i] + .15:.3f});')
        js(f'tl.fromTo("#mc{i}", {{x: 0}}, {{x: 8, duration: .05, yoyo: true, repeat: 3, immediateRender: false}}, {cues[i] + .15:.3f});')
        sfx("pop", cues[i], -6)
        sfx("error", cues[i] + .15, -12)
    js(f'tl.set("#curB", {{opacity: 0}}, {ends[3] + .1:.3f});')
    # ---------------- PAYOFF ("Same AI. Thirty more seconds of typing. And now it actually sounds like you.")
    t6 = L(6) - .05
    js(f'tl.set("#dotsB", {{opacity: 1}}, {t6:.3f}); tl.set("#dotsB", {{opacity: 0}}, {t6 + .55:.3f});')
    js(f'tl.fromTo("#dotsB i", {{y: 0}}, {{y: -10, duration: .18, yoyo: true, repeat: 1, stagger: .08, immediateRender: false}}, {t6:.3f});')
    js(f'tl.set("#rbB", {{opacity: 1}}, {t6 + .55:.3f});')
    reveal("#rbB .wr", t6 + .55, T("and", L(6) + 1) - .1, kind="stream")
    sfx("ding", t6 + .55, -3)
    # the generic one above glitches out
    js(f'tl.fromTo("#wa", {{x: 0}}, {{x: 14, duration: .04, yoyo: true, repeat: 7, ease: "steps(1)", immediateRender: false}}, {t6:.3f});')
    js(f'tl.fromTo("#stA", {{opacity: 0, scale: 1.8, rotation: -14}}, {{opacity: 1, scale: 1, rotation: -8, duration: .3, ease: "back.out(2)", immediateRender: false}}, {t6 + .15:.3f});')
    sfx("glitch", t6, -6)
    sfx("stamp", t6 + .2, -6)
    t_like = T("sounds", L(6)) - .05
    js(f'tl.fromTo("#stB", {{opacity: 0, scale: 1.8, rotation: 12}}, {{opacity: 1, scale: 1, rotation: 6, duration: .32, ease: "back.out(2.2)", immediateRender: false}}, {t_like:.3f});')
    sfx("stamp", t_like + .05, -3)
    # ---------------- CTA ("Comment PROMPT, and I'll send you ten prompts like this, ready to copy.")
    js(f'tl.to("#tp", {{y: -{SEAM}, duration: .5, ease: "expo.in"}}, {t_cta - .25:.3f}); tl.to("#bp", {{y: {FH - SEAM}, duration: .5, ease: "expo.in"}}, {t_cta - .25:.3f});')
    js(f'tl.set("#seam", {{opacity: 0}}, {t_cta - .25:.3f});')
    BODY.append(f'<div class="cta" id="cta"><div class="ch1" id="ch1">Comment <span class="pk">"PROMPT"</span></div>'
                f'<div class="cbox" id="cbox"><i class="av"></i><span class="ct" id="ct">{"".join(f"<b>{c}</b>" for c in "PROMPT")}</span>'
                f'<span class="cur2" id="cur2"></span><span class="snd" id="snd">{ic("send")}</span></div>'
                f'<div class="cov" id="cov"><img src="assets/img/pdf_cover.png"><div class="free" id="free">FREE PDF</div></div></div>')
    js(f'tl.fromTo("#cta", {{opacity: 0}}, {{opacity: 1, duration: .25}}, {t_cta:.3f});')
    js(f'tl.fromTo("#ch1", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: .45, ease: "back.out(1.8)", immediateRender: false}}, {t_cta + .05:.3f});')
    js(f'tl.fromTo("#cbox", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: .45, ease: "back.out(1.8)", immediateRender: false}}, {t_cta + .15:.3f});')
    tp = T("prompt", L(7)) - .1
    js(f'tl.fromTo("#ct b", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .07, immediateRender: false}}, {tp:.3f});')
    for k in range(6):
        sfx("key", tp + k * .07, -3)
    js(f'tl.fromTo("#snd", {{scale: 1}}, {{scale: 1.35, duration: .15, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {tp + .6:.3f});')
    sfx("send", tp + .6, -2)
    t_cov = T("send", L(7)) - .1
    js(f'tl.fromTo("#cov", {{y: 700, rotation: 8, opacity: 0}}, {{y: 0, rotation: -3, opacity: 1, duration: .7, ease: "back.out(1.4)", immediateRender: false}}, {t_cov:.3f});')
    js(f'tl.fromTo("#free", {{scale: 0}}, {{scale: 1, duration: .35, ease: "back.out(2.5)", immediateRender: false}}, {T("ten", L(7)):.3f});')
    js(f'tl.to("#cov", {{y: -14, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 1}}, {t_cov + .8:.3f});')
    sfx("whoosh", t_cov, -4)
    sfx("pop", T("ten", L(7)), -5)
    return t_split, t_cta


def caps(t_split, t_cta):
    """short captions (up to ~20 characters, one line): on the seam during the split, low otherwise; the keyword of each
    chunk in lime"""
    KEY = {"prompt.", "prompt,", "same", "ai.", "who", "hook.", "format.", "you.", "watch.", "everyone", "comment", "prompt", "copy."}
    chunks, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(w)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        txt = " ".join(x["w"] for x in cur)
        if (nxt is None or nxt["line"] != w["line"] or w["w"][-1] in ".,?!:" or
                len(txt + " " + (nxt["w"] if nxt else "")) > 20):
            chunks.append(cur)
            cur = []
    for k, ch in enumerate(chunks):
        a = ch[0]["s"] - .04
        b = chunks[k + 1][0]["s"] - .04 if k + 1 < len(chunks) else DUR - .2
        if b - ch[-1]["e"] > .6:
            b = ch[-1]["e"] + .45
        txt = " ".join((f'<em>{H.escape(w["w"])}</em>' if norm(w["w"]) in {norm(x) for x in KEY} else H.escape(w["w"])) for w in ch)
        pos = "seam" if t_split <= a < t_cta else "low"
        CAPS.append(f'<div class="cap {pos}" id="c{k}"><b>{txt}</b></div>')
        js(f'tl.fromTo("#c{k}", {{opacity: 0, scale: .86}}, {{opacity: 1, scale: 1, duration: .12, ease: "back.out(2)", immediateRender: false}}, {max(0, a):.3f});')
        js(f'tl.set("#c{k}", {{opacity: 0}}, {b:.3f});')
    return len(chunks)


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {PAGE}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter", sans-serif; color: {INK};
  background: radial-gradient(60% 34% at 0% 0%, rgba(206,251,143,.85), transparent 70%), radial-gradient(60% 34% at 100% 0%, rgba(254,112,179,.7), transparent 70%),
  radial-gradient(60% 34% at 0% 100%, rgba(254,112,179,.7), transparent 70%), radial-gradient(60% 34% at 100% 100%, rgba(206,251,143,.85), transparent 70%), {PAGE}; }}
.pk {{ color: {PINK}; }}
.ic {{ width: 34px; height: 34px; fill: none; stroke: currentColor; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; flex: none; }}
/* panels */
.panel {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; }}
.panel.low {{ top: {SEAM + 6}px; height: {FH - SEAM - 6}px; transform: translateY({FH - SEAM}px); background: linear-gradient(180deg, rgba(204,251,121,.28), rgba(253,244,244,0) 40%); }}
#tp {{ background: rgba(235,232,232,.0); }}
.seamline {{ position: absolute; left: 0; top: {SEAM - 3}px; width: {FW}px; height: 8px; background: {INK}; opacity: 0; z-index: 5; transform-origin: center; }}
.lab {{ position: absolute; left: 60px; display: flex; align-items: center; gap: 12px; padding: 12px 24px 12px 18px; border-radius: 999px;
  font-weight: 800; font-size: 32px; letter-spacing: .04em; background: {INK}; color: {LIME}; opacity: 0; }}
.lab.grey {{ top: 222px; background: #d9d6d6; color: #5d5d5d; }}
#bpl {{ top: 56px; }}
/* chat windows */
.win {{ position: absolute; left: 70px; width: 940px; border-radius: 34px; background: #fff; box-shadow: 0 30px 70px rgba(16,17,17,.16), 0 0 0 2px rgba(16,17,17,.06);
  overflow: hidden; transform-origin: 50% 0%; }}
#wa {{ top: 560px; }}
#wbw {{ top: 205px; }}
.wh {{ display: flex; align-items: center; gap: 14px; padding: 20px 28px; border-bottom: 2px solid #f1eded; }}
.wh b {{ font-size: 30px; font-weight: 800; margin-right: auto; }}
.wh i {{ width: 14px; height: 14px; border-radius: 50%; background: #e3dede; }}
.wdot {{ width: 46px; height: 46px; border-radius: 14px; background: {INK}; display: grid; place-items: center; }}
.sp {{ width: 28px; height: 28px; fill: {LIME}; stroke: none; }}
.wb {{ padding: 26px 28px 30px; display: flex; flex-direction: column; gap: 18px; }}
.ub {{ align-self: flex-end; max-width: 86%; padding: 18px 26px; border-radius: 28px 28px 8px 28px; background: {INK}; color: #fff; font-weight: 700; font-size: 38px; line-height: 1.25; }}
#ubA .wa1:nth-child(n+4) {{ opacity: 0; }}
.ub.good {{ max-width: 100%; align-self: stretch; transform-origin: 100% 0%; font-size: 31px; padding: 18px 22px; display: flex; flex-direction: column; gap: 8px; }}
.pl {{ display: none; align-items: flex-start; gap: 14px; }}
#ubB {{ opacity: 0; }}
.pl b {{ flex: none; width: 38px; height: 38px; border-radius: 50%; background: {PINK}; color: #fff; font-size: 24px; display: grid; place-items: center; margin-top: 1px; }}
.cur {{ position: absolute; }}
.rb {{ align-self: flex-start; max-width: 92%; padding: 20px 26px; border-radius: 28px 28px 28px 8px; background: #f3f0f0; font-weight: 600; font-size: 34px; line-height: 1.3; opacity: 0; }}
.rb.good {{ max-width: 100%; background: rgba(204,251,121,.45); font-size: 31px; font-weight: 700; display: flex; flex-direction: column; gap: 6px; }}
.dots {{ align-self: flex-start; display: flex; gap: 10px; padding: 20px 26px; border-radius: 28px; background: #f3f0f0; opacity: 0; }}
.dots i {{ width: 14px; height: 14px; border-radius: 50%; background: #b9b3b3; }}
.ghost {{ position: absolute; left: 150px; top: 820px; width: 780px; padding: 22px 28px; border-radius: 26px; background: #ece8e8; color: #9a9393; font-weight: 600; font-size: 30px;
  line-height: 1.3; opacity: 0; box-shadow: 0 14px 30px rgba(16,17,17,.08); }}
.same {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1225px; padding: 14px 28px; border-radius: 999px; background: {INK}; color: #fff;
  font-weight: 800; font-size: 36px; opacity: 0; }}
.miss {{ position: absolute; left: 60px; right: 60px; top: 735px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.mc {{ display: flex; align-items: center; gap: 12px; padding: 14px 20px; border-radius: 18px; background: rgba(255,255,255,.6); color: {GREY}; font-weight: 800; font-size: 32px; opacity: 0; }}
.pcs {{ position: absolute; left: 60px; right: 60px; top: 126px; display: flex; gap: 12px; }}
.pc {{ flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 12px 6px; border-radius: 16px; border: 3px solid {INK}; font-weight: 800; font-size: 21px;
  letter-spacing: .02em; white-space: nowrap; opacity: 0; }}
.pc b {{ font-size: 22px; color: {PINK}; }}
.stamp {{ position: absolute; display: flex; align-items: center; gap: 12px; padding: 14px 30px; border-radius: 20px; font-weight: 800; font-size: 50px; letter-spacing: .04em; opacity: 0; }}
.stamp.grey {{ left: 600px; top: 330px; border: 6px solid #6e6969; color: #6e6969; background: rgba(255,255,255,.85); }}
.stamp.lime {{ right: 40px; top: 78px; font-size: 44px; background: {LIME}; color: {INK}; border: 5px solid {INK}; box-shadow: 0 16px 34px rgba(16,17,17,.2); }}
.stamp.lime .ic {{ width: 46px; height: 46px; stroke-width: 3.6; color: {PINK}; }}
/* hook */
.hook {{ position: absolute; left: 50px; right: 50px; top: 250px; text-align: center; z-index: 6; }}
.hook span {{ display: block; font-weight: 800; font-size: 104px; line-height: 1.0; letter-spacing: -.04em; }}
.hook span.pk {{ font-size: 82px; margin-top: 10px; }}
/* CTA */
.cta {{ position: absolute; inset: 0; z-index: 7; opacity: 0; }}
.ch1 {{ position: absolute; left: 0; right: 0; top: 250px; text-align: center; font-weight: 800; font-size: 104px; letter-spacing: -.04em; }}
.cbox {{ position: absolute; left: 90px; right: 90px; top: 420px; display: flex; align-items: center; gap: 22px; padding: 22px 26px; border-radius: 999px; background: #fff;
  box-shadow: 0 20px 50px rgba(16,17,17,.14), 0 0 0 3px {INK}; }}
.av {{ width: 66px; height: 66px; border-radius: 50%; background: linear-gradient(135deg, {LIME}, {PINK}); flex: none; }}
.ct {{ font-weight: 800; font-size: 50px; letter-spacing: .04em; }}
.cur2 {{ width: 4px; height: 52px; background: {PINK}; margin-left: -14px; }}
.snd {{ margin-left: auto; width: 76px; height: 76px; border-radius: 50%; background: {PINK}; display: grid; place-items: center; }}
.snd .ic {{ width: 40px; height: 40px; color: #fff; fill: #fff; stroke-width: 2; }}
.cov {{ position: absolute; left: 230px; top: 600px; width: 620px; transform-origin: 50% 100%; }}
.cov img {{ width: 620px; height: 775px; display: block; border-radius: 26px; box-shadow: 0 34px 80px rgba(16,17,17,.28), 0 0 0 3px {INK}; }}
.free {{ position: absolute; right: -40px; top: -30px; padding: 14px 26px; border-radius: 999px; background: {LIME}; border: 4px solid {INK}; font-weight: 800; font-size: 38px;
  transform: rotate(8deg); }}
/* captions */
.cap {{ position: absolute; left: 0; right: 0; text-align: center; z-index: 8; opacity: 0; }}
.cap.seam {{ top: {SEAM - 46}px; }}
.cap.low {{ top: 1500px; }}
.cap b {{ display: inline-block; padding: 12px 30px 16px; border-radius: 22px; background: {INK}; color: #fff; font-weight: 800; font-size: 56px; letter-spacing: -.01em;
  box-shadow: 0 14px 34px rgba(16,17,17,.28); }}
.cap em {{ font-style: normal; color: {LIME}; }}
#grain {{ position: absolute; inset: 0; opacity: .045; background: url(assets/img/grain.png); mix-blend-mode: multiply; z-index: 9; pointer-events: none; }}
"""


def main():
    t_split, t_cta = build()
    n = caps(t_split, t_cta)
    page = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Creators 100X: stop typing write me a script 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      {"".join(BODY)}
      {"".join(CAPS)}
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
    json.dump(sorted(SFX, key=lambda e: e["t"]), open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    json.dump({"dur": DUR, "split": round(t_split, 3), "cta": round(t_cta, 3)}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
    print(f"wrote index.html: {len(A)} timeline lines, {n} captions, {len(SFX)} sfx, {DUR} s")


if __name__ == "__main__":
    main()
