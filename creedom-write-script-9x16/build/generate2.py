"""Creators 100X x Creedom "@write-script" reel, v2 "MADE TO MEASURE" (9:16): writes index.html, plan/sfx_events.json
and plan/edit.json from plan/words.json.

Owner on v1: "it looks like the rebranding or part 2 of the earlier video... change the voiceover style, make it more
expressive, add different concepts, use a different video or none at all, explain with more animation elements, try
something unique." So v2 shares nothing with the CHECK reel: no glass, no fluid blobs, no Cree, no phone mockup
look, no stock footage, a new voice (Chatterbox, af_bella timbre, build/vo2.py) and new music ("Swinging Around").

Concept: AI scripts are off the rack (one size fits all); Creedom's write-script is a tailor. Everything is drawn in
code on sewing-pattern paper in the Creators 100X palette (off-white, ink, hot pink, lime):
  0 fitting room: a figure in a mirror tries on script after script, none fit ("DOESN'T FIT");
  1 clothes rails of identical scripts ("Hey guys!", "Let's dive in!"), a swinging ONE SIZE FITS ALL tag, zoom out;
  2 (ink) a live voice waveform vs the flat line of an off-the-rack script;
  3 a bold flat phone: @write-script types into Creedom, a tape measure shoots out;
  4 the tape measures our reels, a tailor's ticket fills in by hand (opener, pauses, words);
  5 scissors cut HOOK / STORY / CTA pattern pieces, a needle stitches them in pink thread;
  6 back in the mirror: the tailored script fits, sparkles, "on a really good day";
  7 CTA: a swinging SCRIPT tag, the comment types in, the DM arrives.
Transitions: fabric swipe, fitting-room curtain, tape-measure wipe, scissor cut.
python3 build/generate2.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, HTML, ROOT, punch, scene  # noqa: E402

random.seed(23)
INK, PINK, LIME, PAPER = "#101111", "#FD0B68", "#CCFB79", "#FDF4F4"
DUR = round(L1["m07"] + .9, 2)
BEAT = 60 / 117.45                       # "Swinging Around" from 0.58 s, on a beat
HB = BEAT / 2


def snap(t):
    return round(t / HB) * HB


S = {k: (0.0 if k == "m00" else snap(L0[k] - .1)) for k in LINES}
K = ["m00", "m01", "m02", "m03", "m04", "m05", "m06", "m07"]
END = {k: (S[K[i + 1]] if i + 1 < len(K) else DUR) for i, k in enumerate(K)}

# ---- headlines: words rise out of a mask on their spoken time; pk = pink, hl = lime highlighter, hw = handwriting ------
WID = [0]


def head(hid, rows, top, line, size=96, after=0.0, dark=False):
    spoken, k, out, html = [w for w in LINES[line] if w["t0"] >= after], 0, [], []
    for row in rows:
        ws = []
        for item in row:
            word, cls = item[0], item[1]
            keys = (item[2] if len(item) > 2 else word).lower().strip(".,:!?\"").split("|")
            WID[0] += 1
            wid = f"w{WID[0]}"
            t = None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?\"")
                k += 1
                if any(sw.startswith(x[:4]) or x.startswith(sw[:4]) for x in keys if x):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            hlb = '<i class="hlb"></i>' if "hl" in cls else ""
            ws.append(f'<span class="wm"><span class="wi {cls}" id="{wid}">{hlb}<em>{word}</em></span></span>')
            out.append((wid, t, "hl" in cls))
        html.append(f'<div class="hr">{" ".join(ws)}</div>')
    HTML.append(f'<div class="head {"dk" if dark else ""}" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(html)}</div>')
    for wid, t, hl in out:
        ft(f"#{wid}", t - .06, .4, "{yPercent: 118, rotation: 7, opacity: 1}", "{yPercent: 0, rotation: 0, opacity: 1}", "back.out(1.7)")
        if hl:
            ft(f"#{wid} .hlb", t + .14, .32, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
    return out


def head_out(hid, t):
    to(f"#{hid}", t, .24, "{y: -60, opacity: 0}", "power2.in")


# ---- transitions -------------------------------------------------------------------------------------------------------
def fabric(t):
    """a hot-pink fabric panel with stitched edges sweeps across the cut"""
    ft("#fab", t - .3, .62, "{x: -1500, rotation: -6}", "{x: 1500, rotation: -6}", "power2.inOut")
    sfx("whoosh_big", t - .32)
    sfx("swish", t - .05)


def curtain(t):
    """the fitting-room curtain closes on the cut and opens on the next scene"""
    ft("#curL", t - .3, .3, "{xPercent: -101}", "{xPercent: 0}", "power3.in")
    ft("#curR", t - .3, .3, "{xPercent: 101}", "{xPercent: 0}", "power3.in")
    to("#curL", t + .1, .38, "{xPercent: -101}", "power3.out")
    to("#curR", t + .1, .38, "{xPercent: 101}", "power3.out")
    js(f'tl.fromTo(".fold", {{skewX: 0}}, {{skewX: 4, duration: .19, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {t - .3:.3f});')
    sfx("whoosh_big", t - .32)
    sfx("click", t - .02)
    sfx("swish", t + .1)


def tapewipe(t):
    """a lime tape measure flies across the frame"""
    ft("#tapew", t - .32, .62, "{x: -1700}", "{x: 1700}", "power2.inOut")
    sfx("whoosh", t - .3)
    sfx("riser_short", t - .9)


def scissorcut(t):
    """two pattern-paper halves close on a diagonal seam, scissors snip along it, the halves part on the new scene"""
    ft("#cutA", t - .28, .26, "{x: -1600, y: -1600}", "{x: 0, y: 0}", "power3.in")
    ft("#cutB", t - .28, .26, "{x: 1600, y: 1600}", "{x: 0, y: 0}", "power3.in")
    js(f'tl.fromTo("#seamsc", {{x: -620, y: 1100, opacity: 1}}, {{x: 620, y: -1100, opacity: 1, duration: .34, ease: "none", immediateRender: false}}, {t - .02:.3f});')
    js(f'tl.fromTo("#seamsc .bl", {{rotation: -14}}, {{rotation: 14, duration: .06, yoyo: true, repeat: 5, ease: "none", immediateRender: false}}, {t - .02:.3f});')
    st("#seamsc", t + .33, "{opacity: 0}")
    to("#cutA", t + .32, .34, "{x: -1600, y: -1600}", "power2.in")
    to("#cutB", t + .32, .34, "{x: 1600, y: 1600}", "power2.in")
    sfx("impact", t - .03)
    for k in range(3):
        sfx("shutter", t + .02 + .11 * k)
    sfx("whoosh", t + .3)


def ink(t, on):
    to("#inkw", t - .05, .25, f"{{opacity: {1 if on else 0}}}", "power2.inOut")


# ---- shared drawings ---------------------------------------------------------------------------------------------------
HANGER = ('<svg class="hgr" viewBox="0 0 200 92"><path d="M100 40 V30 C100 24 112 22 112 12 C112 4 106 0 100 0 C93 0 88 5 88 11"/>'
          '<path d="M100 40 L190 84 C194 86 193 90 188 90 H12 C7 90 6 86 10 84 Z"/></svg>')
FIG = ('<svg class="fig" viewBox="0 0 400 600"><circle cx="200" cy="112" r="80"/>'
       '<path d="M52 600 C52 380 110 252 200 252 C290 252 348 380 348 600 Z"/></svg>')
SCISSORS = ('<svg viewBox="-60 -60 120 120"><g class="bl"><path d="M0 0 L58 -8 L58 -2 Z" fill="#101111"/><circle cx="-30" cy="18" r="16" fill="none" '
            'stroke="#FD0B68" stroke-width="8"/><path d="M0 0 L-18 10" stroke="#FD0B68" stroke-width="8"/></g><g class="bl b2"><path d="M0 0 L58 8 L58 2 Z" '
            'fill="#101111"/><circle cx="-30" cy="-18" r="16" fill="none" stroke="#FD0B68" stroke-width="8"/><path d="M0 0 L-18 -10" stroke="#FD0B68" '
            'stroke-width="8"/></g><circle r="5" fill="#CCFB79" stroke="#101111" stroke-width="2"/></svg>')
FIG0 = FIG.replace('class="fig"', 'class="fig" id="fig0"')
FIG1 = FIG.replace('class="fig"', 'class="fig" id="fig1"')
STAR = '<svg viewBox="-50 -50 100 100"><path d="M0 -50 C6 -10 10 -6 50 0 C10 6 6 10 0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z"/></svg>'


def garment(gid, cls, face_a="", face_b="", lines=3):
    faces = (f'<b class="fa">{face_a}</b>' if face_a else "") + (f'<b class="fb">{face_b}</b>' if face_b else "")
    return f'<div class="gar {cls}" id="{gid}">{HANGER}<div class="gcard">{faces}{"<i></i>" * lines}</div></div>'


# =======================================================================================================================
# 0 FITTING ROOM: script after script, none fit
s0, e0 = S["m00"], END["m00"]
tries = "".join(garment(f"try{k}", "try", "Hey guys!" if k % 2 == 0 else "Let's dive in!") for k in range(4))
pile = "".join(f'<div class="pile" id="pl{k}" style="left:{250 + 95 * k}px;--r:{random.randint(-30, 30)}deg"><i></i><i></i></div>' for k in range(6))
cnts = "".join(f'<b class="cn" id="cn{k}">{37 + k}</b>' for k in range(4))
HTML.append(f'<div class="scn" id="s0"><div class="mirror" id="mir0"><i class="mshine" id="msh0"></i></div>{FIG0}'
            f'{tries}{pile}<div class="cnt" id="cnt"><span>SCRIPT</span><span class="cns">{cnts}</span><span>/ 40</span></div>'
            '<div class="nope" id="nope">DOESN\'T FIT</div></div>')
head("h0a", [[("I", ""), ("tried", ""), ("on", ""), ("40", "pk hl", "forty|40")], [("AI", ""), ("scripts.", "")]], 130, "m00", 104)
head("h0b", [[("Not", ""), ("one", "pk"), ("fit.", "hl")]], 130, "m00", 124, after=T("m00", "Not") - .2)
scene("s0", s0, e0)
sfx("impact", 0)
ft("#mir0", 0, .5, "{opacity: 0, scale: .9, y: 60}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.5)")
ft("#fig0", .1, .45, "{opacity: 0, y: 80}", "{opacity: 1, y: 0}", "back.out(1.6)")
ft("#cnt", .25, .4, "{opacity: 0, x: 80}", "{opacity: 1, x: 0}", "back.out(2)")
t_not = T("m00", "Not")
gap = (t_not - .35) / 4
MISFIT = ["{scale: 1.75, y: 60}", "{scale: .42, y: 90}", "{rotation: 28, x: 40, skewX: 10}", "{scaleX: 2.1, scaleY: .62}"]
for k in range(4):
    t = .3 + gap * k
    ft(f"#try{k}", t, .26, "{opacity: 1, y: -1000, rotation: -10}", "{opacity: 1, y: 0, rotation: 0}", "back.out(1.3)")
    to(f"#try{k}", t + .26, .14, MISFIT[k], "back.out(2.5)")
    to(f"#try{k}", t + gap * .78, .22, f"{{x: {(-1, 1)[k % 2] * 950}, y: 200, rotation: {(-1, 1)[k % 2] * 50}}}", "power2.in")
    st(".cn", t, "{opacity: 0}")
    st(f"#cn{k}", t, "{opacity: 1}")
    ft(f"#cn{k}", t, .25, "{yPercent: 80}", "{yPercent: 0}", "back.out(2.5)")
    sfx("swish", t)
    sfx("pop", t + .26)
    sfx("whoosh", t + gap * .78)
st(".cn", t_not - .2, "{opacity: 0}")
st("#cn3", t_not - .2, "{opacity: 1}")
ft("#nope", t_not + .05, .24, "{opacity: 0, scale: 2.4, rotation: -26}", "{opacity: 1, scale: 1, rotation: -10}", "power4.in")
sfx("stamp", t_not + .25)
punch(t_not + .28, 1.06)
for k in range(6):
    ft(f"#pl{k}", t_not + .05 * k, .35, "{opacity: 0, y: -500}", "{opacity: 1, y: 0}", "bounce.out")
js(f'tl.fromTo("#fig0", {{x: 0}}, {{keyframes: [{{x: -16, duration: .06}}, {{x: 14, duration: .06}}, {{x: -8, duration: .06}}, {{x: 0, duration: .06}}]}}, {t_not + .3:.3f});')
ft("#msh0", .5, 1.1, "{xPercent: -150}", "{xPercent: 350}", "power2.inOut")
head_out("h0a", t_not - .3)
head_out("h0b", e0 - .28)

# =======================================================================================================================
# 1 OFF THE RACK: rails of identical scripts, one size fits all, zoom out to every creator on earth
s1, e1 = S["m01"], END["m01"]
rails = ""
for r in range(5):
    gs = "".join(garment(f"rg{r}_{i}", "rg", "Hey guys!", "Let's dive in!") for i in range(11))
    rails += f'<div class="rail" style="top:{r * 420}px"><i class="bar"></i><div class="rtrack" id="rt{r}">{gs}</div></div>'
HTML.append(f'<div class="scn" id="s1"><div id="rails">{rails}</div>'
            '<div class="bigtag" id="bigtag"><i class="hole"></i><span>ONE SIZE</span><b>FITS ALL</b></div></div>')
head("h1a", [[("Off", ""), ("the", ""), ("rack.", "hl")]], 130, "m01", 120)
head("h1b", [[("Every", "pk"), ("creator.", "")], [("On", ""), ("earth.", "hl")]], 130, "m01", 104, after=T("m01", "every") - .2)
scene("s1", s1, e1)
fabric(s1)
for r in range(5):
    x0 = -260 - 90 * r
    d = 1 if r % 2 == 0 else -1
    ft(f"#rt{r}", s1, e1 - s1 + .2, f"{{x: {x0}}}", f"{{x: {x0 - 420 * d}}}", "none")
js(f'tl.fromTo(".rg", {{rotation: -5}}, {{rotation: 5, duration: .5, yoyo: true, repeat: {int((e1 - s1) / .5)}, ease: "sine.inOut", stagger: {{each: .04, from: "random"}}, immediateRender: false}}, {s1:.3f});')
t_rk = T("m01", "rack")
ft("#bigtag", t_rk - .1, 1.0, "{opacity: 1, y: -900, rotation: -40}", "{opacity: 1, y: 0, rotation: 0}", "elastic.out(1, .45)")
sfx("whoosh", t_rk - .1)
sfx("thump", t_rk + .25)
t_h = T("m01", "hook")
ft(".rg .fa", t_h - .05, .25, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1, stagger: {each: .012, from: 'random'}}", "back.out(2)")
sfx("pop", t_h)
t_dv = T("m01", "dive")
to(".rg .fa", t_dv - .25, .15, "{opacity: 0}")
ft(".rg .fb", t_dv - .15, .25, "{opacity: 0, rotationX: 90}", "{opacity: 1, rotationX: 0, stagger: {each: .012, from: 'random'}}", "back.out(2)")
sfx("pop", t_dv - .1)
punch(t_dv, 1.04)
t_ev = T("m01", "every")
head_out("h1a", t_ev - .3)
to("#bigtag", t_ev - .1, .4, "{y: 700, rotation: 30, opacity: 0}", "power2.in")
to("#rails", t_ev, 1.1, "{scale: .42}", "power3.inOut")
sfx("riser", t_ev - .4)
head_out("h1b", e1 - .28)

# =======================================================================================================================
# 2 (ink) NEVER HEARD YOU: your live voice vs the flat line
s2, e2 = S["m02"], END["m02"]
bars = "".join(f'<i class="vb" id="vb{i}"></i>' for i in range(28))
HTML.append(f'<div class="scn" id="s2"><div class="vrow" id="vyou"><u class="lab lime">YOU</u><div class="bars">{bars}</div></div>'
            '<div class="vrow" id="vai"><u class="lab grey">OFF-THE-RACK SCRIPT</u><div class="flat"><i id="flatl"></i></div><em>no voice</em></div></div>')
head("h2", [[("None", ""), ("of", ""), ("them", "")], [("ever", ""), ("heard", "hl"), ("you.", "pk")]], 200, "m02", 108, dark=True)
scene("s2", s2, e2)
curtain(s2)
ink(s2, True)
ft("#vyou", s2 + .15, .4, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.6)")
for i in range(28):
    hs = [round(random.uniform(.15, 1.0), 2) for _ in range(6)]
    kf = ", ".join(f"{{scaleY: {h}, duration: {random.uniform(.12, .2):.2f}}}" for h in hs)
    js(f'tl.fromTo("#vb{i}", {{scaleY: .1}}, {{keyframes: [{kf}], repeat: {int((e2 - s2) / .9) + 1}, yoyo: true, ease: "sine.inOut", immediateRender: false}}, {s2 + .2 + .01 * i:.3f});')
t_hd = T("m02", "heard")
ft("#vai", t_hd - .35, .4, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.6)")
ft("#flatl", t_hd - .2, .5, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
sfx("buzzer", t_hd)
punch(t_hd, 1.05)
js(f'tl.fromTo(".vb", {{backgroundColor: "#FD0B68"}}, {{backgroundColor: "#CCFB79", duration: .2, yoyo: true, repeat: 1, stagger: .02, immediateRender: false}}, {T("m02", "talk"):.3f});')
head_out("h2", e2 - .28)

# =======================================================================================================================
# 3 THE PHONE: @write-script, then a tape measure shoots out
s3, e3 = S["m03"], END["m03"]
chars = "".join(f"<i>{c}</i>" for c in "@write-script")
HTML.append('<div class="scn" id="s3"><div class="bphone" id="bphone"><div class="bscr"><img class="blogo" src="assets/img/creedom_logo.png">'
            '<div class="btitle">How can Cree help?</div><div class="bcard" id="bcard"><svg viewBox="0 0 24 24"><path d="M4 20h4L19 9l-4-4L4 16v4zM14 6l4 4"/></svg>'
            'Get a script<br>in your voice</div><div class="bin" id="bin"><i class="bcur" id="bcur"></i>'
            f'<span class="bty" id="bty">{chars}</span><span class="bpill" id="bpill">@write-script</span><b class="bsend" id="bsend">'
            '<svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></b></div></div></div><div class="tapeshot" id="tapeshot"></div></div>')
head("h3", [[("I", ""), ("opened", ""), ("Creedom,", "pk")], [("and", ""), ("typed:", "hl")]], 130, "m03", 96)
scene("s3", s3, e3)
tapewipe(s3)
ink(s3, False)
ft("#bphone", s3 + .05, .55, "{opacity: 0, y: 500, rotation: 12}", "{opacity: 1, y: 0, rotation: -4}", "back.out(1.4)")
t_cr = T("m03", "Creedom")
to("#bphone", t_cr, .35, "{rotation: 0, scale: 1.02}", "back.out(2)")
ft("#bcard", t_cr + .05, .4, "{scale: .8, opacity: 0}", "{scale: 1, opacity: 1}", "back.out(2.5)")
sfx("pop", t_cr + .05)
t_ty = T("m03", "typed")
js(f'tl.fromTo("#bcur", {{opacity: 1}}, {{opacity: 0, duration: .2, ease: "steps(1)", yoyo: true, repeat: 5, immediateRender: false}}, {t_ty - .2:.3f});')
t_at = T("m03", "at")
st("#bcur", t_at, "{opacity: 0}")
t_end = max(L1["m03"] - .1, t_at + .5)
js(f'tl.fromTo("#bty i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: {(t_end - t_at) / 13:.3f}, immediateRender: false}}, {t_at:.3f});')
for k in range(0, 13, 2):
    sfx("tick", t_at + (t_end - t_at) / 13 * k)
st("#bty", t_end + .08, "{opacity: 0}")
ft("#bpill", t_end + .08, .35, "{opacity: 0, scale: 1.5}", "{opacity: 1, scale: 1}", "back.out(2.6)")
sfx("pop", t_end + .08)
to("#bsend", t_end + .3, .1, "{scale: .8}")
to("#bsend", t_end + .4, .25, "{scale: 1.15, backgroundColor: '#FD0B68'}", "back.out(3)")
sfx("click", t_end + .3)
ft("#tapeshot", t_end + .45, .35, "{scaleX: 0}", "{scaleX: 1}", "power3.out")
sfx("riser_short", t_end - .3)
head_out("h3", e3 - .3)

# =======================================================================================================================
# 4 MEASUREMENTS: the tape measures our reels, the tailor's ticket fills in by hand
s4, e4 = S["m04"], END["m04"]
nums = "".join(f'<span style="left:{i * 40}px">{i}</span>' for i in range(0, 24))
thumbs = "".join(f'<div class="rth" id="th{i}"><img src="assets/img/reel{j}.jpg"><b class="pin" id="pin{i}">{lab}</b></div>'
                 for i, (j, lab) in enumerate([(1, "opener"), (3, "pause"), (0, "words")]))
ROWS = [("OPENER", "“Here’s the thing…”"), ("PAUSES", "right after the hook"), ("WORDS", "“honestly”, “low-key”")]
rows = "".join(f'<div class="trow" id="tr{i}"><u>{a}</u><i class="dots"></i><span class="hand" id="hd{i}">{b}</span></div>' for i, (a, b) in enumerate(ROWS))
HTML.append(f'<div class="scn" id="s4"><div class="tape" id="tape">{nums}</div><div class="thumbs">{thumbs}</div>'
            f'<div class="ticket" id="ticket"><i class="punchhole"></i><div class="thd">MEASUREMENTS <em>@creators.100x</em></div>{rows}</div></div>')
head("h4", [[("It", ""), ("takes", ""), ("your", "")], [("measurements.", "hl")]], 130, "m04", 96)
scene("s4", s4, e4)
st("#bphone", s4, "{opacity: 0}")
ft("#tape", s4 + .02, .55, "{scaleX: 0}", "{scaleX: 1}", "power3.out")
for k in range(6):
    sfx("tick", s4 + .05 + .08 * k)
t_ms = T("m04", "measurements")
for i in range(3):
    ft(f"#th{i}", t_ms - .4 + .08 * i, .45, "{opacity: 0, y: 140, rotation: (i - 1) * 8}".replace("(i - 1) * 8", str((i - 1) * 8)), "{opacity: 1, y: 0, rotation: " + str((i - 1) * 3) + "}", "back.out(1.6)")
    sfx("shutter", t_ms - .4 + .08 * i)
ft("#ticket", t_ms + .1, .5, "{opacity: 0, y: 300, rotation: 8}", "{opacity: 1, y: 0, rotation: -2}", "back.out(1.4)")
sfx("swish", t_ms + .1)
for i, key in enumerate(("open", "pause", "words")):
    t = T("m04", key) - .05
    ft(f"#pin{i}", t, .3, "{opacity: 0, scale: .3, y: -40}", "{opacity: 1, scale: 1, y: 0}", "back.out(3)")
    ft(f"#hd{i}", t + .05, .55, "{clipPath: 'inset(0 100% 0 0)'}", "{clipPath: 'inset(0 0% 0 0)'}", "power1.inOut")
    ft(f"#tr{i} .dots", t, .3, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
    sfx("pop", t)
    sfx("swish", t + .1)
punch(T("m04", "stop"), 1.05)
js(f'tl.fromTo("#ticket", {{rotation: -2}}, {{rotation: 1, duration: .8, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_ms + .7:.3f});')
head_out("h4", e4 - .3)

# =======================================================================================================================
# 5 CUT AND STITCH: scissors cut the pattern pieces, a needle stitches them in pink thread
s5, e5 = S["m05"], END["m05"]
PIECES = [("hook", "HOOK", 470, 210, ["Here’s the thing nobody tells you…"]),
          ("story", "STORY", 720, 290, ["I stared at a blank page for an hour.", "Then I stopped writing like a robot."]),
          ("cta", "CTA", 1050, 200, ["Save this for your next shoot."])]
pcs = ""
for pid, lab, y, h, ls in PIECES:
    w = 800
    rect = f'x="4" y="4" width="{w - 8}" height="{h - 8}" rx="18"'
    srect = f'x="18" y="18" width="{w - 36}" height="{h - 36}" rx="10"'
    pcs += (f'<div class="pc" id="pc_{pid}" style="top:{y}px;height:{h}px"><svg class="pcs" viewBox="0 0 {w} {h}">'
            f'<rect class="dash" {rect}/><rect class="cut" id="cut_{pid}" pathLength="1" {rect}/></svg>'
            f'<svg class="stitch" id="sti_{pid}" viewBox="0 0 {w} {h}"><rect {srect}/></svg>'
            f'<u class="plab" id="pl_{pid}">{lab}</u><div class="ptx" id="tx_{pid}">' + "".join(f"<p>{x}</p>" for x in ls) + "</div></div>")
HTML.append(f'<div class="scn" id="s5"><div class="sheet" id="sheet"></div>{pcs}<div class="scis" id="scis">{SCISSORS}</div>'
            '<div class="needle" id="needle"><i></i></div></div>')
head("h5a", [[("It", ""), ("cuts", "pk"), ("to", ""), ("fit.", "hl")]], 130, "m05", 120)
head("h5b", [[("Stitched", "pk"), ("in", "")], [("your", ""), ("voice.", "hl")]], 130, "m05", 104, after=T("m05", "stitched") - .25)
scene("s5", s5, e5)
scissorcut(s5)
ft("#sheet", s5 + .1, .45, "{opacity: 0, scale: .92}", "{opacity: 1, scale: 1}", "back.out(1.4)")
ft(".pc", s5 + .25, .35, "{opacity: 0}", "{opacity: 1, stagger: .08}", "power2.out")
t_cu = T("m05", "cuts")
# scissors: around the HOOK piece (x 140..940), then across STORY and CTA
X0, X1 = 140, 940
path = [(X0, 470), (X1, 470), (X1, 680), (X0, 680), (X0, 470), (X0, 720), (X1, 720), (X0, 1050), (X1, 1050)]
st("#scis", t_cu - .1, f"{{opacity: 1, x: {X0}, y: 470}}")
dur_cut = max(1.2, T("m05", "Hook") - t_cu - .15)
seg = dur_cut / (len(path) - 1)
kf = ", ".join(f"{{x: {x}, y: {y}, duration: {seg:.3f}}}" for x, y in path[1:])
js(f'tl.to("#scis", {{keyframes: [{kf}], ease: "none"}}, {t_cu - .1:.3f});')
js(f'tl.fromTo("#scis .bl", {{rotation: -16}}, {{rotation: 16, duration: .07, yoyo: true, repeat: {int(dur_cut / .07)}, ease: "none", immediateRender: false}}, {t_cu - .1:.3f});')
js(f'tl.fromTo("#scis .b2", {{rotation: 16}}, {{rotation: -16, duration: .07, yoyo: true, repeat: {int(dur_cut / .07)}, ease: "none", immediateRender: false}}, {t_cu - .1:.3f});')
ft("#cut_hook", t_cu - .1, seg * 4, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "none")
ft("#cut_story", t_cu - .1 + seg * 4, seg * 2.5, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "none")
ft("#cut_cta", t_cu - .1 + seg * 6.5, seg * 1.5, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", "none")
for k in range(int(dur_cut / .16)):
    sfx("shutter" if k % 2 == 0 else "click", t_cu - .1 + .16 * k)
st("#scis", t_cu - .1 + dur_cut + .05, "{opacity: 0}")
for pid, key in (("hook", "Hook"), ("story", "story"), ("cta", "call")):
    t = T("m05", key) - .05
    to(f"#pc_{pid}", t, .3, "{y: -10, boxShadow: '14px 14px 0 #101111', backgroundColor: '#FFFFFF'}", "back.out(2.5)")
    ft(f"#pl_{pid}", t, .3, "{opacity: 0, scale: .3, rotation: -20}", "{opacity: 1, scale: 1, rotation: -4}", "back.out(3)")
    sfx("pop", t)
    punch(t + .02, 1.025)
head_out("h5a", T("m05", "stitched") - .3)
t_st = T("m05", "stitched")
for i, (pid, lab, y, h, ls) in enumerate(PIECES):
    t = t_st - .1 + .32 * i
    ft(f"#sti_{pid}", t, .45, "{clipPath: 'inset(0 100% 0 0)'}", "{clipPath: 'inset(0 0% 0 0)'}", "none")
    ft(f"#needle", t, .45, f"{{opacity: 1, x: {X0}, y: {y + 20}}}", f"{{opacity: 1, x: {X1}, y: {y + 20}}}", "none")
    ft(f"#tx_{pid} p", t + .05, .3, "{opacity: 0, x: -30}", "{opacity: 1, x: 0, stagger: .1}", "power2.out")
    for k in range(4):
        sfx("tick", t + .1 * k)
js(f'tl.fromTo("#needle i", {{y: 0}}, {{y: 26, duration: .05, yoyo: true, repeat: {int(1.4 / .05)}, ease: "none", immediateRender: false}}, {t_st - .1:.3f});')
st("#needle", t_st + .9, "{opacity: 0}")
punch(T("m05", "voice"), 1.05)
sfx("ding", T("m05", "voice"))
head_out("h5b", e5 - .3)

# =======================================================================================================================
# 6 IT FITS: back in the mirror, the tailored script fits
s6, e6 = S["m06"], END["m06"]
stars = "".join(f'<div class="spk" id="sp{i}" style="left:{x}px;top:{y}px;width:{z}px;height:{z}px;color:{c}">{STAR}</div>'
                for i, (x, y, z, c) in enumerate([(190, 600, 90, LIME), (820, 560, 110, PINK), (860, 1000, 70, LIME), (150, 1080, 76, PINK), (700, 760, 56, LIME)]))
HTML.append(f'<div class="scn" id="s6"><div class="mirror" id="mir1"><i class="mshine" id="msh1"></i></div>{FIG1}'
            '<div class="gar fit" id="fitg">' + HANGER + '<div class="gcard pinkc"><u>MADE TO MEASURE</u><i></i><i></i><i></i></div></div>'
            f'{stars}<div class="hw6" id="hw6">…on a really good day.</div></div>')
head("h6", [[("Sounds", ""), ("like", ""), ("me.", "pk hl")]], 150, "m06", 124)
scene("s6", s6, e6)
curtain(s6)
st("#fig1", s6, "{opacity: 1}")
st("#mir1", s6, "{opacity: 1}")
t_sd = T("m06", "sounds")
ft("#fitg", t_sd - .1, .5, "{opacity: 1, y: -1000}", "{opacity: 1, y: 0}", "back.out(1.2)")
sfx("whoosh", t_sd - .1)
sfx("success", t_sd + .35)
js(f'tl.fromTo("#fig1, #fitg", {{y: 0}}, {{y: -26, duration: .18, yoyo: true, repeat: 3, ease: "power1.out", immediateRender: false}}, {T("m06", "me") + .05:.3f});')
for i in range(5):
    t = T("m06", "me") + .06 * i
    ft(f"#sp{i}", t, .4, "{opacity: 0, scale: 0, rotation: -90}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(3)")
    js(f'tl.to("#sp{i}", {{rotation: 180, duration: {e6 - t:.2f}, ease: "none"}}, {t + .4:.3f});')
sfx("ding", T("m06", "me"))
ft("#msh1", T("m06", "me"), 1.0, "{xPercent: -150}", "{xPercent: 350}", "power2.inOut")
t_rl = T("m06", "really")
ft("#hw6", t_rl - .2, .8, "{clipPath: 'inset(0 100% 0 0)', opacity: 1}", "{clipPath: 'inset(0 0% 0 0)', opacity: 1}", "power1.inOut")
punch(T("m06", "day"), 1.04)
head_out("h6", e6 - .3)

# =======================================================================================================================
# 7 CTA: the SCRIPT tag, the comment, the DM
s7 = S["m07"]
cty = "".join(f"<i>{c}</i>" for c in "SCRIPT")
HTML.append('<div class="scn" id="s7"><div class="dm2" id="dm2"><img src="assets/img/c100x_mark.png"><div><b>creators.100x</b><span>sent you the link</span></div><em>now</em></div>'
            '<div class="cmt" id="cmt">Comment</div><div class="ctag" id="ctag"><i class="hole"></i><b>SCRIPT</b>'
            '<span class="cbadge"><img src="assets/img/creedom_logo.png">@write-script</span></div><i class="cstring" id="cstring"></i>'
            f'<div class="cbar" id="cbar"><i class="cav"></i><span class="cph" id="cph">Add a comment…</span><span class="cty" id="cty">{cty}</span>'
            '<b class="csend" id="csend"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></b></div>'
            '<div class="csub" id="csub">and I\'ll send you the <span class="hlw"><i class="hlb" id="csubhl"></i><em>link.</em></span></div></div>')
scene("s7", s7, DUR + 1)
fabric(s7)
t_cm = T("m07", "Comment")
ft("#cmt", t_cm - .05, .4, "{opacity: 0, yPercent: 60}", "{opacity: 1, yPercent: 0}", "back.out(2)")
t_sk = T("m07", "Script")
ft("#cstring", t_sk - .15, .3, "{scaleY: 0}", "{scaleY: 1}", "power2.out")
ft("#ctag", t_sk - .15, 1.1, "{opacity: 1, y: -800, rotation: -35}", "{opacity: 1, y: 0, rotation: 0}", "elastic.out(1, .4)")
sfx("impact", t_sk)
sfx("thump", t_sk + .1)
punch(t_sk + .1, 1.07)
ft("#cbar", t_sk + .3, .45, "{opacity: 0, y: 120}", "{opacity: 1, y: 0}", "back.out(1.6)")
t_c2 = t_sk + .65
st("#cph", t_c2, "{opacity: 0}")
js(f'tl.fromTo("#cty i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .07, immediateRender: false}}, {t_c2:.3f});')
for k in range(6):
    sfx("tick", t_c2 + .07 * k)
to("#csend", t_c2 + .48, .1, "{scale: .8}")
to("#csend", t_c2 + .58, .25, "{scale: 1.12, backgroundColor: '#FD0B68'}", "back.out(3)")
sfx("click", t_c2 + .48)
ft("#csub", T("m07", "send") - .1, .45, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(1.8)")
t_lk = T("m07", "link")
ft("#csubhl", t_lk, .3, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
ft("#dm2", t_lk - .1, .6, "{opacity: 0, y: -260}", "{opacity: 1, y: 0}", "back.out(1.6)")
sfx("notify", t_lk)
js(f'tl.fromTo("#ctag", {{rotation: 0}}, {{rotation: 4, duration: .9, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_sk + 1.0:.3f});')

# ---- background: pattern paper, corner glows that drift, a ruler down the edge ---------------------------------------------------
ruler = "".join(f'<span style="top:{i * 80}px">{i}</span>' for i in range(0, 24))
for gid in ("gl0", "gl1", "gl2", "gl3"):
    js(f'tl.fromTo("#{gid}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-160, 160)}, y: {random.randint(-200, 200)}, scale: {random.uniform(.85, 1.3):.2f}, '
       f'duration: {DUR / 3:.2f}, yoyo: true, repeat: 2, ease: "sine.inOut", immediateRender: false}}, 0);')

CSS = open(os.path.join(ROOT, "build", "style2.css")).read()
for k, v in (("$INK", INK), ("$PINK", PINK), ("$LIME", LIME), ("$PAPER", PAPER)):
    CSS = CSS.replace(k, v)

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: @write-script, made to measure 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="world" id="paper"><i class="glow" id="gl0"></i><i class="glow" id="gl1"></i><i class="glow" id="gl2"></i><i class="glow" id="gl3"></i>
        <div class="grid"></div><div class="ruler">{ruler}</div></div>
      <div class="world" id="inkw"><div class="grid gdk"></div></div>
      <div id="cam"><div id="punch"><div id="drift">
        {chr(10).join(HTML)}
      </div></div></div>
      <div id="flash"></div>
      <div id="fab"><i></i></div>
      <div id="curL" class="cur"><i class="fold"></i></div><div id="curR" class="cur"><i class="fold"></i></div>
      <div id="tapew"></div>
      <div id="cutA" class="cut"></div><div id="cutB" class="cut"></div><div id="seamsc">{SCISSORS}</div>
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set("#curL", {{xPercent: -101}}, 0);
      tl.set("#curR", {{xPercent: 101}}, 0);
      tl.set("#fab", {{x: -1500, rotation: -6}}, 0);
      tl.set("#tapew", {{x: -1700}}, 0);
      tl.set("#cutA", {{x: -1600, y: -1600}}, 0);
      tl.set("#cutB", {{x: 1600, y: 1600}}, 0);
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
json.dump({"dur": DUR, "scenes": {k: [S[k], END[k]] for k in K}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx; cuts {[round(S[k], 2) for k in K]}")
