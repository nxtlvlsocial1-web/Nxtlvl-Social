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
                f'<div class="miss" id="miss">{miss}</div><div class="stamp grey" id="stA">GENERIC</div>'
                f'<div class="mq" id="mq"><div class="mqlab">Everyone else\'s reels</div><div class="mqrow" id="mqrow">'
                + "".join(f'<div class="rc"><i class="rav"></i><b>Hey guys!</b><span>Level up your fitness journey...</span><i class="rl"></i><i class="rl s"></i><em>5 amazing tips</em></div>' for _ in range(8))
                + '</div></div></div>')
    # hook line, readable on frame 0
    BODY.append(f'<div class="hook" id="hook"><span>STOP TYPING</span><span class="pk big">THIS</span></div>'
                f'<svg class="harrow" id="harrow" viewBox="0 0 160 200"><path d="M40 10 C 130 40, 140 120, 70 180"/><path d="M48 160 L70 182 L96 160"/></svg>'
                f'<div class="stop" id="stop">STOP</div>')
    # frame 0 is mid-story: the prompt is half typed already
    # v3 (owner: "make the hook more engaging, people may skip"): the command lands on frame 0 with the prompt already
    # on screen; on "Stop" a pink STOP stamp slams onto it (punch-in + shake), the arrow points at it, then it is sent
    t_stop = T("stop") + .02
    js(f'tl.fromTo("#stop", {{opacity: 0, scale: 3.2, rotation: -30}}, {{opacity: 1, scale: 1, rotation: -12, duration: .26, ease: "back.out(1.7)", immediateRender: false}}, {t_stop:.3f});')
    js(f'tl.fromTo("#wa", {{scale: 1.07}}, {{scale: 1, duration: .35, ease: "power3.out", immediateRender: false}}, {t_stop + .2:.3f});')
    js(f'tl.fromTo("#tp", {{x: 0}}, {{x: 12, duration: .04, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false}}, {t_stop + .2:.3f});')
    js(f'tl.fromTo("#hook .big", {{scale: 1.5, opacity: 0}}, {{scale: 1, opacity: 1, duration: .3, ease: "back.out(2.2)", immediateRender: false}}, {T("this") - .05:.3f});')
    js(f'tl.fromTo("#harrow", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(2)", immediateRender: false}}, {T("this"):.3f});')
    js(f'tl.fromTo("#harrow", {{y: 0}}, {{y: 14, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}}, {T("this") + .3:.3f});')
    js(f'tl.to("#stop, #harrow", {{opacity: 0, scale: .7, duration: .2}}, {T("it's") - .1:.3f});')
    sfx("stamp", t_stop, 0)
    sfx("whoosh", 0.0, -6)
    t_send = T("chatgpt") + .1
    sfx("send", t_send)
    js(f'tl.fromTo("#dotsA", {{opacity: 0}}, {{opacity: 1, duration: .15}}, {t_send + .05:.3f}); tl.set("#dotsA", {{opacity: 0}}, {t_send + .4:.3f});')
    js(f'tl.fromTo("#dotsA i", {{y: 0}}, {{y: -10, duration: .18, yoyo: true, repeat: 3, stagger: .08, ease: "sine.inOut", immediateRender: false}}, {t_send + .05:.3f});')
    t_r = t_send + .4
    js(f'tl.set("#rbA", {{opacity: 1}}, {t_r:.3f});')
    reveal("#rbA .wa2", t_r, T("everyone") - .1, kind="stream")
    sfx("ding", t_r, -4)
    # "The same script everyone else got": copies fan out behind the window
    t_same = T("everyone") - .3
    # v3: identical "reels" scroll under the window from frame 0 (everyone posts the same script)
    js(f'tl.fromTo("#mqrow", {{x: 0}}, {{x: -1140, duration: {t_split:.3f}, ease: "none", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#mq .rc", {{borderColor: "rgba(16,17,17,.08)"}}, {{borderColor: "{PINK}", duration: .2, stagger: .05, immediateRender: false}}, {T("everyone") - .1:.3f});')
    js(f'tl.set("#gw", {{display: "none"}}, 0);')
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
                f'<img class="pg pg2" id="pg2" src="assets/img/pdf_p2.png"><img class="pg pg3" id="pg3" src="assets/img/pdf_p3.png">'
                f'<div class="cov" id="cov"><img src="assets/img/pdf_cover.png"><div class="free" id="free">FREE PDF</div></div>'
                f'<svg class="arrow" id="arrow" viewBox="0 0 120 120"><path d="M20 110 C 90 100, 100 60, 72 22"/><path d="M52 36 L72 18 L88 40"/></svg>'
                + star("cspk", "cs0", 870, 560, 54, PINK) + star("cspk", "cs1", 180, 650, 40, INK) + star("cspk", "cs2", 900, 1330, 46, INK) + '</div>')
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
    for k, (r, x) in enumerate(((-14, -190), (12, 190))):
        js(f'tl.fromTo("#pg{k + 2}", {{y: 700, x: 0, rotation: 0, opacity: 0}}, {{y: 30, x: {x}, rotation: {r}, opacity: 1, duration: .7, ease: "back.out(1.3)", immediateRender: false}}, {t_cov + .15:.3f});')
    js(f'tl.fromTo("#arrow", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false}}, {t_cta + .35:.3f});')
    js(f'tl.fromTo("#arrow", {{y: 0}}, {{y: -16, duration: .3, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}}, {t_cta + .7:.3f});')
    js(f'tl.fromTo(".cspk", {{scale: 0, rotation: 0}}, {{scale: 1, rotation: 120, duration: .6, stagger: .2, ease: "back.out(2.5)", immediateRender: false}}, {T("ten", L(7)):.3f});')
    return t_split, t_cta


BEAT = 60 / 117.45                           # the music's grid; the bed starts on a beat, so beats fall on n * BEAT


def star(cls, sid, x, y, size, color):
    return (f'<svg class="{cls}" id="{sid}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px" viewBox="0 0 24 24">'
            f'<path d="M12 0c.8 6.6 4.8 10.8 12 12-7.2 1.2-11.2 5.4-12 12-.8-6.6-4.8-10.8-12-12 7.2-1.2 11.2-5.4 12-12z" fill="{color}"/></svg>')


def extras(t_split, t_cta):
    """v2 (owner: "few visual elements, add more; not a single frame should feel dull"): a living background (drifting
    lime / pink blobs, a moving dot grid, beat-timed sparkles), a camera that keeps pushing in, a cursor in the hook,
    cliche stickers around the generic script, prompt-strength meters (0/4 above, filling to 4/4 below), shimmering
    placeholder lines where the good reply will land, chip bursts, a flash on the split, confetti on the payoff, and in
    the CTA a turning sunburst, fanned PDF pages, a bouncing arrow and sparkles"""
    t6 = L(6) - .05
    t_like = T("sounds", L(6)) - .05
    # ---- background (behind everything)
    blobs = [(-160, 380, 520, LIME), (720, 260, 460, "#FE70B3"), (640, 1250, 560, LIME), (-200, 1450, 480, "#FE70B3"), (300, 820, 380, LIME)]
    bg = "".join(f'<i class="blob" id="bl{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px;--c:{c}"></i>' for i, (x, y, w, c) in enumerate(blobs))
    sp = [(110, 520, 46), (930, 640, 38), (160, 1720, 40), (960, 1600, 52), (520, 140, 34), (60, 1180, 30), (1000, 1080, 34), (420, 1840, 30)]
    bg += "".join(star("spk", f"sk{i}", x, y, w, PINK if i % 2 else INK) for i, (x, y, w) in enumerate(sp))
    BODY.insert(0, f'<div class="bg" id="bg"><i class="dotgrid" id="dg"></i>{bg}</div>')
    for i, (x, y, w, c) in enumerate(blobs):
        dx, dy = (-1) ** i * (90 + 20 * i), (-1) ** (i + 1) * (70 + 15 * i)
        js(f'tl.fromTo("#bl{i}", {{x: 0, y: 0}}, {{x: {dx}, y: {dy}, duration: {DUR / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false}}, 0);')
    js(f'tl.fromTo("#dg", {{y: 0}}, {{y: -180, duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
    n = 0
    t = BEAT * 2
    while t < DUR - .6:
        i = n % len(sp)
        js(f'tl.fromTo("#sk{i}", {{scale: 0, rotation: 0, opacity: 0}}, {{scale: 1, rotation: 90, opacity: 1, duration: {BEAT * 1.2:.3f}, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
        js(f'tl.to("#sk{i}", {{scale: 0, opacity: 0, duration: {BEAT:.3f}, ease: "power2.in"}}, {t + BEAT * 1.6:.3f});')
        n += 1
        t += BEAT * 2
    # beat pulse on the blobs (every bar)
    t = 0.0
    while t < DUR - .5:
        js(f'tl.fromTo(".blob", {{scale: 1.08}}, {{scale: 1, duration: {BEAT * 1.5:.3f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')
        t += BEAT * 4
    # ---- camera: a slow push in every section, reset on each cut
    for a, b in ((0, t_split), (t_split, t6), (t6, t_cta), (t_cta, DUR)):
        js(f'tl.fromTo("#cam", {{scale: 1}}, {{scale: 1.035, duration: {b - a:.3f}, ease: "none", immediateRender: false}}, {a:.3f});')
    # ---- hook: a cursor clicks send; cliche stickers pop around the generic script
    BODY.append('<svg class="cursor" id="cursor" viewBox="0 0 24 24"><path d="M3 2l7.5 19 2.6-7.6L21 10.8z"/></svg>')
    t_send = T("chatgpt") + .1
    js(f'tl.fromTo("#cursor", {{x: 0, y: 0, opacity: 1}}, {{x: 120, y: -330, duration: {t_send - .15:.3f}, ease: "power2.inOut", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#cursor", {{scale: 1}}, {{scale: .78, duration: .08, yoyo: true, repeat: 1, immediateRender: false}}, {t_send - .1:.3f});')
    js(f'tl.to("#cursor", {{x: 260, y: 300, opacity: 0, duration: .6, ease: "power2.in"}}, {t_send + .4:.3f});')
    cl = [("Hey guys!", 50, 1630, -8), ("Level up", 700, 1620, 7), ("Game changer", 80, 1770, 5), ("Amazing tips", 640, 1770, -6),
          ("Transform your body", 290, 1700, 3), ("Your journey", 380, 1850, -4)]
    BODY.append("".join(f'<div class="cliche" id="cl{i}" style="left:{x}px;top:{y}px;--r:{r}deg">{H.escape(w)}<i></i></div>' for i, (w, x, y, r) in enumerate(cl)))
    t_same = T("everyone") - .3
    for i, (w, x, y, r) in enumerate(cl):
        a = t_same + i * .1
        js(f'tl.fromTo("#cl{i}", {{opacity: 0, scale: .2, rotation: 0}}, {{opacity: 1, scale: 1, rotation: {r}, duration: .35, ease: "back.out(2.6)", immediateRender: false}}, {a:.3f});')
        js(f'tl.fromTo("#cl{i} i", {{scaleX: 0}}, {{scaleX: 1, duration: .2, ease: "power2.out", immediateRender: false}}, {T("everyone") + .15 + i * .05:.3f});')
        js(f'tl.to("#cl{i}", {{opacity: 0, scale: .6, duration: .2}}, {t_split - .25:.3f});')
    # ---- split: a white flash
    BODY.append('<i class="flash" id="flash"></i>')
    js(f'tl.fromTo("#flash", {{opacity: .85}}, {{opacity: 0, duration: .35, ease: "power2.out", immediateRender: false}}, {t_split + .12:.3f});')
    # ---- prompt-strength meters
    seg = lambda cls: "".join(f'<i class="{cls}"></i>' for _ in range(4))
    BODY.append(f'<div class="meter top" id="mtA"><span>PROMPT STRENGTH</span><div class="segs">{seg("sg")}</div><b>0/4</b></div>')
    BODY.append(f'<div class="meter bot" id="mtB"><span>PROMPT STRENGTH</span><div class="segs">{seg("sg")}</div>'
                + "".join(f'<b class="cnt" id="cn{k}">{k}/4</b>' for k in range(5)) + '</div>')
    js(f'tl.fromTo("#mtA, #mtB", {{opacity: 0, y: -14}}, {{opacity: 1, y: 0, duration: .3, stagger: .08, immediateRender: false}}, {t_split + .5:.3f});')
    js(f'tl.to("#mtA", {{y: -{SEAM}, duration: .5, ease: "expo.in"}}, {t_cta - .25:.3f}); tl.to("#mtB", {{y: {FH - SEAM}, duration: .5, ease: "expo.in"}}, {t_cta - .25:.3f});')
    cues = [T("first"), T("then"), T("now"), T("and", L(5))]
    js('tl.set("#cn0", {opacity: 1}, 0);')
    for k, c in enumerate(cues, 1):
        js(f'tl.fromTo("#mtB .sg:nth-child({k})", {{backgroundColor: "rgba(16,17,17,.12)", scaleY: 1}}, {{backgroundColor: "{LIME}", scaleY: 1.5, duration: .2, ease: "back.out(3)", immediateRender: false}}, {c:.3f});')
        js(f'tl.to("#mtB .sg:nth-child({k})", {{scaleY: 1, duration: .2}}, {c + .25:.3f});')
        js(f'tl.set("#cn{k - 1}", {{opacity: 0}}, {c:.3f}); tl.set("#cn{k}", {{opacity: 1}}, {c:.3f});')
        # a burst from the chip
        js(f'tl.fromTo("#bu{k - 1} i", {{x: 0, y: 0, opacity: 1, scale: 1}}, {{x: (j) => Math.cos(j * 1.047) * 70, y: (j) => Math.sin(j * 1.047) * 70, opacity: 0, scale: .3, '
           f'duration: .45, ease: "power2.out", immediateRender: false}}, {c:.3f});')
    for k in range(4):
        BODY.append(f'<div class="burst" id="bu{k}" style="left:{60 + 120 + k * 243}px;top:{SEAM + 6 + 148}px">' + "".join(f'<i style="--c:{PINK if j % 2 else LIME}"></i>' for j in range(6)) + '</div>')
    js(f'tl.to(".burst", {{y: {FH - SEAM}, duration: .01}}, {t_cta - .25:.3f});')
    # ---- shimmering placeholder lines where the good reply will appear (until it streams in)
    BODY.append('<div class="skel" id="skel">' + "".join(f'<i style="width:{w}%"><b></b></i>' for w in (88, 64, 76, 52)) + '</div>')
    js(f'tl.fromTo("#skel", {{opacity: 0}}, {{opacity: 1, duration: .3, immediateRender: false}}, {T("a", L(2)) + .3:.3f}); tl.set("#skel", {{opacity: 0}}, {t6 + .55:.3f});')
    js(f'tl.fromTo("#skel b", {{x: -260}}, {{x: 900, duration: 1.2, repeat: {int((t6 - T("a", L(2))) / 1.2) + 1}, ease: "sine.inOut", immediateRender: false}}, {T("a", L(2)) + .3:.3f});')
    js(f'tl.fromTo("#skel", {{y: 0}}, {{y: 150, duration: .01, immediateRender: false}}, {T("busy") - .05:.3f});')
    js(f'tl.to("#skel", {{y: 230, duration: .01}}, {T("open") - .05:.3f}); tl.to("#skel", {{y: 300, duration: .01}}, {T("thirty", L(5)) - .05:.3f});')
    # ---- payoff: the good window punches, confetti
    js(f'tl.fromTo("#wbw", {{scale: 1}}, {{scale: 1.035, duration: .14, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_like:.3f});')
    conf = ""
    for i in range(26):
        x = R.randint(60, 1020)
        conf += f'<i class="cf" id="cf{i}" style="left:{x}px;--c:{[LIME, PINK, INK][i % 3]};--w:{R.randint(14, 24)}px"></i>'
    BODY.append(f'<div class="conf" id="conf">{conf}</div>')
    js(f'tl.set("#conf", {{opacity: 1}}, {t_like:.3f}); tl.set("#conf", {{opacity: 0}}, {t_cta:.3f});')
    for i in range(26):
        d = R.uniform(.9, 1.5)
        js(f'tl.fromTo("#cf{i}", {{y: {R.randint(900, 1000)}, x: 0, rotation: 0, opacity: 1}}, {{y: {R.randint(1500, 1900)}, x: {R.randint(-120, 120)}, rotation: {R.randint(-540, 540)}, '
           f'opacity: 0, duration: {d:.2f}, ease: "power1.in", immediateRender: false}}, {t_like + R.uniform(0, .25):.3f});')
    # ---- CTA: sunburst, fanned pages, arrow, sparkles
    BODY.append(f'<div class="ctabg" id="ctabg"><i class="rays" id="rays"></i></div>')
    js(f'tl.fromTo("#ctabg", {{opacity: 0}}, {{opacity: 1, duration: .4, immediateRender: false}}, {t_cta:.3f});')
    js(f'tl.fromTo("#rays", {{rotation: 0}}, {{rotation: 40, duration: {DUR - t_cta:.3f}, ease: "none", immediateRender: false}}, {t_cta:.3f});')
    return t6


def caps(t_split, t_cta):
    """short captions (up to ~20 characters, one line): on the seam during the split, low otherwise; the keyword of each
    chunk in lime"""
    KEY = {"stop", "chatgpt.", "prompt.", "prompt,", "same", "ai.", "who", "hook.", "format.", "you.", "watch.", "everyone", "comment", "prompt", "copy."}
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
.mq {{ position: absolute; left: 0; top: 1130px; width: {FW}px; }}
.mqlab {{ margin-left: 60px; font-weight: 800; font-size: 28px; letter-spacing: .06em; color: #8d8686; text-transform: uppercase; }}
.mqrow {{ display: flex; gap: 24px; margin-top: 14px; padding-left: 60px; }}
.rc {{ flex: none; width: 260px; height: 300px; border-radius: 24px; background: #fff; border: 4px solid rgba(16,17,17,.08); padding: 20px 18px; display: flex; flex-direction: column;
  gap: 10px; box-shadow: 0 12px 26px rgba(16,17,17,.08); }}
.rav {{ width: 46px; height: 46px; border-radius: 50%; background: linear-gradient(135deg, #d9d4d4, #bfb8b8); }}
.rc b {{ font-weight: 800; font-size: 30px; color: #6f6969; }}
.rc span {{ font-weight: 600; font-size: 22px; color: #9a9393; line-height: 1.25; }}
.rl {{ height: 12px; border-radius: 6px; background: #eeeaea; width: 90%; }} .rl.s {{ width: 60%; }}
.rc em {{ font-style: normal; font-weight: 700; font-size: 20px; color: #b0aaaa; margin-top: auto; }}
.same {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1080px; z-index: 3; padding: 14px 28px; border-radius: 999px; background: {INK}; color: #fff;
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
.hook span.big {{ font-size: 150px; margin-top: 6px; }}
.harrow {{ position: absolute; left: 790px; top: 330px; width: 150px; height: 190px; fill: none; stroke: {PINK}; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round;
  opacity: 0; z-index: 6; }}
.stop {{ position: absolute; left: 640px; top: 560px; padding: 10px 34px 14px; border-radius: 26px; background: {PINK}; color: #fff; border: 7px solid #fff;
  font-weight: 800; font-size: 92px; letter-spacing: .04em; opacity: 0; z-index: 6; box-shadow: 0 18px 40px rgba(253,11,104,.45); }}
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
#cam {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.bg {{ position: absolute; inset: 0; overflow: hidden; }}
.dotgrid {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH + 200}px; opacity: .28;
  background-image: radial-gradient(rgba(16,17,17,.35) 2px, transparent 2.5px); background-size: 46px 46px; }}
.blob {{ position: absolute; border-radius: 50%; background: radial-gradient(circle, var(--c) 0%, transparent 68%); opacity: .55; }}
.spk {{ position: absolute; opacity: 0; }}
.cursor {{ position: absolute; left: 560px; top: 1050px; width: 74px; height: 74px; fill: {INK}; stroke: #fff; stroke-width: 1.6; z-index: 6;
  filter: drop-shadow(0 8px 14px rgba(16,17,17,.3)); transform-origin: 20% 10%; }}
.cliche {{ position: absolute; padding: 14px 26px; border-radius: 999px; background: #fff; border: 3px solid #c9c4c4; color: #8d8686; font-weight: 800; font-size: 38px;
  white-space: nowrap; opacity: 0; box-shadow: 0 10px 24px rgba(16,17,17,.08); }}
.cliche i {{ position: absolute; left: 14px; right: 14px; top: 50%; height: 6px; margin-top: -3px; border-radius: 3px; background: {PINK}; transform-origin: 0 50%; }}
.flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 7; }}
.meter {{ position: absolute; right: 60px; display: flex; align-items: center; gap: 12px; font-weight: 800; opacity: 0; z-index: 4; }}
.meter span {{ font-size: 20px; letter-spacing: .08em; color: #7a7474; }}
.meter b {{ font-size: 30px; width: 54px; text-align: right; }}
.meter.top {{ top: 230px; }} .meter.top b {{ color: {PINK}; }}
.meter.bot {{ top: {SEAM + 6 + 62}px; }}
.meter.bot .cnt {{ position: absolute; right: 0; opacity: 0; }}
.meter.bot .segs {{ margin-right: 66px; }}
.segs {{ display: flex; gap: 6px; }}
.sg {{ width: 34px; height: 16px; border-radius: 5px; background: rgba(16,17,17,.12); }}
.burst {{ position: absolute; width: 0; height: 0; z-index: 5; }}
.burst i {{ position: absolute; left: -7px; top: -7px; width: 14px; height: 14px; border-radius: 50%; background: var(--c); opacity: 0; }}
.skel {{ position: absolute; left: 100px; width: 880px; top: {SEAM + 6 + 205 + 210}px; display: flex; flex-direction: column; gap: 18px; opacity: 0; z-index: 3; }}
.skel i {{ display: block; height: 30px; border-radius: 15px; background: #eeeaea; overflow: hidden; position: relative; }}
.skel b {{ position: absolute; top: 0; left: 0; width: 220px; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,.95), transparent); }}
.conf {{ position: absolute; inset: 0; opacity: 0; z-index: 6; pointer-events: none; }}
.cf {{ position: absolute; top: 0; width: var(--w); height: calc(var(--w) * .5); border-radius: 3px; background: var(--c); }}
.ctabg {{ position: absolute; inset: 0; opacity: 0; z-index: 6; overflow: hidden; }}
.rays {{ position: absolute; left: -460px; top: -40px; width: 2000px; height: 2000px; border-radius: 50%;
  background: repeating-conic-gradient(from 0deg, rgba(204,251,121,.38) 0deg 9deg, rgba(253,244,244,0) 9deg 22deg); }}
.pg {{ position: absolute; left: 290px; top: 640px; width: 500px; height: 625px; border-radius: 22px; box-shadow: 0 24px 60px rgba(16,17,17,.22), 0 0 0 3px {INK};
  opacity: 0; transform-origin: 50% 100%; }}
.arrow {{ position: absolute; left: 60px; top: 525px; width: 130px; height: 130px; z-index: 3; fill: none; stroke: {PINK}; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
.cspk {{ position: absolute; z-index: 2; }}
#grain {{ position: absolute; inset: 0; opacity: .045; background: url(assets/img/grain.png); mix-blend-mode: multiply; z-index: 9; pointer-events: none; }}
"""


def main():
    t_split, t_cta = build()
    extras(t_split, t_cta)
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
      <div id="cam">{"".join(BODY)}</div>
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
