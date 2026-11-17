"""v4 (owner on v3: scripts come in FRONT of the person; "Not one fit" -> "Not one worked"; "off the rack" -> "off the
shelf", so the rails became shelves; "@write-script" is typed on screen, not spoken: the line is now "...and typed this").

Creators 100X x Creedom "@write-script" reel, v2 "MADE TO MEASURE" (9:16): writes index.html, plan/sfx_events.json
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
from fx import cree_html, cree_to, pose, cree_walk, cree_hop, cree_wiggle, cree_tilt, blink, sweat, say, sparkle, P, PCX, PCY  # noqa: E402

random.seed(23)
INK, PINK, LIME, PAPER = "#101111", "#F343A2", "#CCFB79", "#FDF4F4"   # v3: Creedom magenta
DUR = round(L1["m07"] + .9, 2)
BEAT = 60 / 117.45                       # "Swinging Around" from 0.58 s, on a beat
HB = BEAT / 2


def snap(t):
    return round(t / HB) * HB


S = {k: (0.0 if k == "m00" else snap(L0[k] - .1)) for k in LINES}
S["m04"] = snap(max(T("m04", "measurements") + .3, T("m03", "this") + 2.1))
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
    sfx("fabric", t - .3)
    sfx("swish", t - .05)


def curtain(t):
    """the fitting-room curtain closes on the cut and opens on the next scene"""
    ft("#curL", t - .3, .3, "{xPercent: -101}", "{xPercent: 0}", "power3.in")
    ft("#curR", t - .3, .3, "{xPercent: 101}", "{xPercent: 0}", "power3.in")
    to("#curL", t + .1, .38, "{xPercent: -101}", "power3.out")
    to("#curR", t + .1, .38, "{xPercent: 101}", "power3.out")
    js(f'tl.fromTo(".fold", {{skewX: 0}}, {{skewX: 4, duration: .19, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {t - .3:.3f});')
    sfx("cloth", t - .32)
    sfx("rail", t - .1)
    sfx("fabric", t + .1)


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
        sfx("snip", t + .02 + .11 * k)
    sfx("whoosh", t + .3)


def ink(t, on):
    to("#dark", t - .05, .25, f"{{opacity: {1 if on else 0}}}", "power2.inOut")


# ---- shared drawings ---------------------------------------------------------------------------------------------------
HANGER = ('<svg class="hgr" viewBox="0 0 200 92"><path d="M100 40 V30 C100 24 112 22 112 12 C112 4 106 0 100 0 C93 0 88 5 88 11"/>'
          '<path d="M100 40 L190 84 C194 86 193 90 188 90 H12 C7 90 6 86 10 84 Z"/></svg>')
FIG = ('<svg class="fig" viewBox="0 0 400 600"><circle cx="200" cy="112" r="80"/>'
       '<path d="M52 600 C52 380 110 252 200 252 C290 252 348 380 348 600 Z"/></svg>')
SCISSORS = ('<svg viewBox="-60 -60 120 120"><g class="bl"><path d="M0 0 L58 -8 L58 -2 Z" fill="#101111"/><circle cx="-30" cy="18" r="16" fill="none" '
            'stroke="#F343A2" stroke-width="8"/><path d="M0 0 L-18 10" stroke="#F343A2" stroke-width="8"/></g><g class="bl b2"><path d="M0 0 L58 8 L58 2 Z" '
            'fill="#101111"/><circle cx="-30" cy="-18" r="16" fill="none" stroke="#F343A2" stroke-width="8"/><path d="M0 0 L-18 -10" stroke="#F343A2" '
            'stroke-width="8"/></g><circle r="5" fill="#CCFB79" stroke="#101111" stroke-width="2"/></svg>')
FIG0 = FIG.replace('class="fig"', 'class="fig" id="fig0"')
FIG1 = FIG.replace('class="fig"', 'class="fig" id="fig1"')
STAR = '<svg viewBox="-50 -50 100 100"><path d="M0 -50 C6 -10 10 -6 50 0 C10 6 6 10 0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z"/></svg>'


def garment(gid, cls, face_a="", face_b="", lines=3):
    faces = (f'<b class="fa">{face_a}</b>' if face_a else "") + (f'<b class="fb">{face_b}</b>' if face_b else "")
    return f'<div class="gar {cls}" id="{gid}">{HANGER}<div class="gcard">{faces}{"<i></i>" * lines}</div></div>'


# ---- the person in the mirror (v3): a flat cartoon with blinking eyes, brows and mouths for expressions, arms that move ---
SKIN, HAIR, TEE = "#F2C3A0", "#2A1B17", "#3A2F4A"


def person(pid):
    return (f'<svg class="psn" id="{pid}" viewBox="0 0 400 640">'
            f'<g id="{pid}_bd"><path d="M84 640 C84 430 122 334 200 334 C278 334 316 430 316 640 Z" fill="{TEE}"/>'
            f'<path d="M168 334 Q200 372 232 334" fill="none" stroke="#5c4d72" stroke-width="10" stroke-linecap="round"/>'
            f'<rect x="178" y="262" width="44" height="82" rx="18" fill="{SKIN}"/>'
            f'<g id="{pid}_aL"><rect x="98" y="342" width="50" height="200" rx="25" fill="{TEE}"/><circle cx="123" cy="548" r="28" fill="{SKIN}"/></g>'
            f'<g id="{pid}_aR"><rect x="252" y="342" width="50" height="200" rx="25" fill="{TEE}"/><circle cx="277" cy="548" r="28" fill="{SKIN}"/></g>'
            f'<g id="{pid}_hd"><circle cx="200" cy="168" r="106" fill="{HAIR}"/><circle cx="110" cy="182" r="18" fill="{SKIN}"/><circle cx="290" cy="182" r="18" fill="{SKIN}"/>'
            f'<ellipse cx="200" cy="182" rx="92" ry="100" fill="{SKIN}"/>'
            f'<path d="M106 160 C108 86 166 56 214 62 C268 68 300 104 296 160 C262 128 214 118 166 132 C142 140 122 148 106 160 Z" fill="{HAIR}"/>'
            '<circle cx="146" cy="214" r="16" fill="#f59bb1" opacity=".7"/><circle cx="254" cy="214" r="16" fill="#f59bb1" opacity=".7"/>'
            '<ellipse cx="164" cy="186" rx="11" ry="15" fill="#1b1b1b"/><ellipse cx="236" cy="186" rx="11" ry="15" fill="#1b1b1b"/>'
            '<circle cx="168" cy="180" r="4" fill="#fff"/><circle cx="240" cy="180" r="4" fill="#fff"/>'
            f'<g id="{pid}_lid" opacity="0"><ellipse cx="164" cy="186" rx="15" ry="19" fill="{SKIN}"/><ellipse cx="236" cy="186" rx="15" ry="19" fill="{SKIN}"/>'
            '<path d="M150 188 Q164 196 178 188 M222 188 Q236 196 250 188" fill="none" stroke="#1b1b1b" stroke-width="5" stroke-linecap="round"/></g>'
            + "".join(f'<g class="{pid}_br" id="{pid}_br_{n}" opacity="{1 if n == "calm" else 0}"><path d="{d}" fill="none" stroke="{HAIR}" stroke-width="8" stroke-linecap="round"/></g>'
                      for n, d in (("calm", "M146 152 Q164 142 182 150 M218 150 Q236 142 254 152"), ("worry", "M146 156 L182 142 M218 142 L254 156"),
                                   ("annoy", "M146 142 L182 154 M218 154 L254 142"), ("happy", "M146 146 Q164 132 182 144 M218 144 Q236 132 254 146")))
            + "".join(f'<g class="{pid}_mo" id="{pid}_mo_{n}" opacity="{1 if n == "flat" else 0}">{m}</g>'
                      for n, m in (("flat", '<path d="M182 238 Q200 246 218 238" fill="none" stroke="#7a1d36" stroke-width="7" stroke-linecap="round"/>'),
                                   ("frown", '<path d="M178 248 Q200 230 222 248" fill="none" stroke="#7a1d36" stroke-width="7" stroke-linecap="round"/>'),
                                   ("o", '<ellipse cx="200" cy="242" rx="14" ry="18" fill="#7a1d36"/>'),
                                   ("smile", '<path d="M170 228 Q200 272 230 228 Z" fill="#7a1d36"/><path d="M182 236 Q200 246 218 236" fill="none" stroke="#fff" stroke-width="5"/>')))
            + "</g></g></svg>")


def person_setup(pid):
    js(f'tl.set("#{pid}_aL", {{svgOrigin: "123 362"}}, 0);')
    js(f'tl.set("#{pid}_aR", {{svgOrigin: "277 362"}}, 0);')
    js(f'tl.set("#{pid}_hd", {{svgOrigin: "200 290"}}, 0);')
    js(f'tl.set("#{pid}_bd", {{svgOrigin: "200 640"}}, 0);')


def face(pid, t, mouth, brow):
    st(f".{pid}_mo", t, "{opacity: 0}")
    st(f"#{pid}_mo_{mouth}", t, "{opacity: 1}")
    st(f".{pid}_br", t, "{opacity: 0}")
    st(f"#{pid}_br_{brow}", t, "{opacity: 1}")


def arms(pid, t, l, r, d=.25):
    js(f'tl.to("#{pid}_aL", {{rotation: {l}, svgOrigin: "123 362", duration: {d}, ease: "back.out(2)"}}, {t:.3f});')
    js(f'tl.to("#{pid}_aR", {{rotation: {r}, svgOrigin: "277 362", duration: {d}, ease: "back.out(2)"}}, {t:.3f});')


def head_tilt(pid, t, a, d=.25):
    js(f'tl.to("#{pid}_hd", {{rotation: {a}, svgOrigin: "200 290", duration: {d}, ease: "back.out(2)"}}, {t:.3f});')


def person_idle(pid, t0, t1):
    person_setup(pid)
    js(f'tl.fromTo("#{pid}_bd", {{scaleY: 1}}, {{scaleY: 1.012, svgOrigin: "200 640", duration: .9, yoyo: true, repeat: {int((t1 - t0) / .9)}, ease: "sine.inOut", immediateRender: false}}, {t0:.3f});')
    t = t0 + .9
    while t < t1 - .2:
        st(f"#{pid}_lid", t, "{opacity: 1}")
        st(f"#{pid}_lid", t + .1, "{opacity: 0}")
        t += 1.7


# =======================================================================================================================
# 0 FITTING ROOM (v3: a cartoon person tries on the scripts, Cree the tailor hands them over)
s0, e0 = S["m00"], END["m00"]
tries = "".join(garment(f"try{k}", "try", "Hey guys!" if k % 2 == 0 else "Let's dive in!") for k in range(4))
pile = "".join(f'<div class="pile" id="pl{k}" style="left:{150 + 95 * k}px;--r:{random.randint(-30, 30)}deg"><i></i><i></i></div>' for k in range(6))
cnts = "".join(f'<b class="cn" id="cn{k}">{37 + k}</b>' for k in range(4))
HTML.append(f'<div class="scn" id="s0"><div class="mirror" id="mir0"><i class="mshine" id="msh0"></i></div>{person("p0")}'
            f'{tries}{pile}<div class="cnt" id="cnt"><span>SCRIPT</span><span class="cns">{cnts}</span><span>/ 40</span></div>'
            '<div class="nope" id="nope">DIDN\'T WORK</div></div>')
head("h0a", [[("I", ""), ("tried", ""), ("on", ""), ("40", "pk hl", "forty|40")], [("AI", ""), ("scripts.", "")]], 130, "m00", 104)
head("h0b", [[("Not", ""), ("one", "pk"), ("worked.", "hl")]], 130, "m00", 116, after=T("m00", "Not") - .2)
scene("s0", s0, e0)
sfx("impact", 0)
sfx("fabric", .05)
ft("#mir0", 0, .5, "{opacity: 0, scale: .9, y: 60}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.5)")
ft("#p0", .1, .45, "{opacity: 0, y: 120}", "{opacity: 1, y: 0}", "back.out(1.6)")
ft("#cnt", .25, .4, "{opacity: 0, x: 80}", "{opacity: 1, x: 0}", "back.out(2)")
person_idle("p0", 0, e0)
t_not = T("m00", "Not")
gap = (t_not - .35) / 4
MISFIT = ["{scale: 1.75, y: 60}", "{scale: .42, y: 90}", "{rotation: 28, x: 40, skewX: 10}", "{scaleX: 2.1, scaleY: .62}"]
FACES = [("o", "worry"), ("frown", "annoy"), ("flat", "worry"), ("frown", "annoy")]
for k in range(4):
    t = .3 + gap * k
    ft(f"#try{k}", t, .26, "{opacity: 1, y: -1000, rotation: -10}", "{opacity: 1, y: 0, rotation: 0}", "back.out(1.3)")
    arms("p0", t + .1, -22, 22, .2)
    to(f"#try{k}", t + .26, .14, MISFIT[k], "back.out(2.5)")
    face("p0", t + .3, *FACES[k])
    head_tilt("p0", t + .3, (-8, 8)[k % 2])
    to(f"#try{k}", t + gap * .78, .22, f"{{x: {(-1, 1)[k % 2] * 1500}, y: 200, rotation: {(-1, 1)[k % 2] * 50}}}", "power2.in")
    arms("p0", t + gap * .74, 50 if k % 2 == 0 else -10, 10 if k % 2 == 0 else -50, .14)
    st(f"#try{k}", t + gap * .78 + .23, "{opacity: 0}")
    st(".cn", t, "{opacity: 0}")
    st(f"#cn{k}", t, "{opacity: 1}")
    ft(f"#cn{k}", t, .25, "{yPercent: 80}", "{yPercent: 0}", "back.out(2.5)")
    sfx("hanger", t + .2)
    sfx("boing" if k in (0, 3) else "cloth", t + .28)
    sfx("swish", t + gap * .78)
st(".cn", t_not - .2, "{opacity: 0}")
st("#cn3", t_not - .2, "{opacity: 1}")
ft("#nope", t_not + .05, .24, "{opacity: 0, scale: 2.4, rotation: -26}", "{opacity: 1, scale: 1, rotation: -10}", "power4.in")
sfx("stamp", t_not + .25)
punch(t_not + .28, 1.06)
for k in range(6):
    ft(f"#pl{k}", t_not + .05 * k, .35, "{opacity: 0, y: -500}", "{opacity: 1, y: 0}", "bounce.out")
face("p0", t_not, "frown", "worry")
arms("p0", t_not + .1, 42, -42, .25)                      # the shrug
js(f'tl.fromTo("#p0_hd", {{rotation: 0}}, {{keyframes: [{{rotation: -9, duration: .1}}, {{rotation: 9, duration: .1}}, {{rotation: -6, duration: .1}}, {{rotation: 0, duration: .1}}], immediateRender: false}}, {t_not + .35:.3f});')
ft("#msh0", .5, 1.1, "{xPercent: -150}", "{xPercent: 350}", "power2.inOut")
head_out("h0a", t_not - .3)
head_out("h0b", e0 - .28)
# Cree, the tailor, hands the scripts over from the right and is shocked when none fit
C0 = P(915, 1470, .46)
js(f'tl.set("#cree", {{x: {1300 - PCX}, y: {C0[1] - PCY:.0f}, scale: {C0[2]}, opacity: 1}}, 0);')
cree_walk(.05, .45, (1300, C0[1], C0[2]), C0, end="present", end_flip=True)
for k in range(1, 4):
    pose(.3 + gap * k - .05, "present" if k % 2 else "point", flip=True)
pose(t_not - .05, "shock")
cree_hop(t_not, 60)
say(t_not + .05, "!", .7, left=True)
sweat(t_not + .15, .9)
pose(t_not + .7, "sad")

# =======================================================================================================================
# 1 OFF THE RACK: rails of identical scripts, one size fits all, zoom out to every creator on earth
s1, e1 = S["m01"], END["m01"]
rails = ""
for r in range(5):
    gs = "".join(garment(f"rg{r}_{i}", "rg", "Hey guys!", "Let's dive in!") for i in range(11))
    rails += f'<div class="rail" style="top:{r * 420}px"><i class="bar"></i><div class="rtrack" id="rt{r}">{gs}</div></div>'
HTML.append(f'<div class="scn" id="s1"><div id="rails">{rails}</div>'
            '<div class="bigtag" id="bigtag"><i class="hole"></i><span>ONE SIZE</span><b>FITS ALL</b></div></div>')
head("h1a", [[("Off", ""), ("the", ""), ("shelf.", "hl")]], 130, "m01", 120)
head("h1b", [[("Every", "pk"), ("creator.", "")], [("On", ""), ("earth.", "hl")]], 130, "m01", 104, after=T("m01", "every") - .2)
scene("s1", s1, e1)
fabric(s1)
st("#cree", s1, "{opacity: 0}")
sfx("rail", s1 + .2)
sfx("rail", s1 + 2.6)
for r in range(5):
    x0 = -260 - 90 * r
    d = 1 if r % 2 == 0 else -1
    ft(f"#rt{r}", s1, e1 - s1 + .2, f"{{x: {x0}}}", f"{{x: {x0 - 420 * d}}}", "none")
js(f'tl.fromTo(".rg", {{rotation: -2}}, {{rotation: 2, duration: .5, yoyo: true, repeat: {int((e1 - s1) / .5)}, ease: "sine.inOut", stagger: {{each: .04, from: "random"}}, immediateRender: false}}, {s1:.3f});')
t_rk = T("m01", "shelf")
ft("#bigtag", t_rk - .1, 1.0, "{opacity: 1, y: -900, rotation: -40}", "{opacity: 1, y: 0, rotation: 0}", "elastic.out(1, .45)")
sfx("whoosh", t_rk - .1)
sfx("hanger", t_rk + .25)
sfx("boing", t_rk + .3)
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
js(f'tl.fromTo(".vb", {{backgroundColor: "#F343A2"}}, {{backgroundColor: "#CCFB79", duration: .2, yoyo: true, repeat: 1, stagger: .02, immediateRender: false}}, {T("m02", "talk"):.3f});')
head_out("h2", e2 - .28)

# =======================================================================================================================
# 3 THE APP (v3: "show the exact UI of that screenshot and animate it"): Creedom's home screen from the owner's screenshot
# (native 1320 x 1734, shown 760 px wide); "@write-script" types and snaps into a pill, the request follows, it sends,
# the home screen turns into the chat and Cree answers that it will take your measurements first
s3, e3 = S["m03"], END["m03"]
APP_S = 760 / 1320
I_BOLT = '<svg class="ic" viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/></svg>'
I_FILM = ('<svg class="ic" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 3v18M17 3v18M3 8h4M3 12h4M3 16h4'
          'M17 8h4M17 12h4M17 16h4"/></svg>')
I_PEN = '<svg class="ic" viewBox="0 0 24 24"><path d="M4 20h4L19 9l-4-4L4 16v4zM14 6l4 4M13 20h7"/></svg>'
I_SEND = '<svg class="ic" viewBox="0 0 24 24"><path d="M21 3 10 14M21 3l-7 18-4-7-7-4 18-7z"/></svg>'
I_IG = '<svg class="ig" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="16.9" cy="7.1" r=".6"/></svg>'
CARDS = [(I_BOLT, "Ideas tuned to your account"), (I_FILM, "Check a reel before you post"), (I_PEN, "Get a script in your voice"),
         (I_SEND, "Send a DM to your comments")]
cards = "".join(f'<div class="uc" id="uc{i}" style="left:{(62, 668)[i % 2]}px;top:{(895, 1213)[i // 2]}px">{ic}<div>{tx}</div></div>'
                for i, (ic, tx) in enumerate(CARDS))
CHIPS = [("Audit my Instagram profile", 305, 660), ("Use one of my Reels and give me insights", 459, 970), ("Analyse one of my latest reels", 613, 735)]
chips = "".join(f'<div class="uchip" id="uh{i}" style="top:{y}px;width:{w}px;margin-left:{-w // 2}px">{tx}</div>' for i, (tx, y, w) in enumerate(CHIPS))
REQ = " my 5am routine reel"
c1 = "".join(f"<i>{c}</i>" for c in "@write-script")
c2 = "".join(f'<i>{"&nbsp;" if c == " " else c}</i>' for c in REQ)
HTML.append('<div class="scn" id="s3">')
head("h3", [[("I", ""), ("opened", ""), ("Creedom,", "pk")], [("and", ""), ("typed", "hl"), ("this:", "")]], 110, "m03", 84)
HTML.append(f'<div class="app" id="app"><div class="appi" style="transform:scale({APP_S:.5f})">'
            '<div class="ucirc" style="left:50px"><i></i><i></i><i></i></div>'
            f'<div class="uacct">{I_IG}<span>creators.100x</span><svg class="chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></div>'
            '<div class="ucirc ued" style="left:1140px"><svg viewBox="0 0 24 24"><path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg></div>'
            f'<div class="uhome" id="uhome"><div class="utitle">How can Cree help?</div>{chips}<div class="ustart">START SOMETHING</div>{cards}</div>'
            '<div class="uchat" id="uchat"><div class="umsg me" id="um1"><b class="mp">@write-script</b>' + REQ + '</div>'
            '<div class="umsg cr" id="um2"><i class="uav"></i><div class="udots" id="udots"><i></i><i></i><i></i></div>'
            '<span id="um2t">On it. First, I\'ll take your measurements: your openers, your pauses, your words.</span></div></div>'
            f'<div class="uin" id="uin"><div class="uplus">+</div><div class="utext"><div class="utrack" id="utrack"><i class="cur2" id="cur2"></i>'
            f'<span class="ty" id="ws1">{c1}</span><span class="wpill" id="wpill">@write-script</span><span class="ty" id="ws2">{c2}</span></div></div>'
            '<div class="usend" id="usend"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div></div>'
            '<i class="ash" id="ash"></i></div></div></div>')
scene("s3", s3, e3)
tapewipe(s3)
ink(s3, False)
ft("#app", s3 + .02, .6, "{opacity: 0, y: 260, rotationX: 24, scale: .9}", "{opacity: 1, y: 0, rotationX: 0, scale: 1}", "back.out(1.3)")
ft(".uchip", s3 + .25, .4, "{opacity: 0, y: 40, scale: .9}", "{opacity: 1, y: 0, scale: 1, stagger: .07}", "back.out(1.8)")
ft(".uc", s3 + .45, .4, "{opacity: 0, y: 50, scale: .9}", "{opacity: 1, y: 0, scale: 1, stagger: .06}", "back.out(1.6)")
sfx("rail", s3 + .25)
t_cr = T("m03", "Creedom")
to("#uc2", t_cr - .05, .35, "{borderColor: '#F343A2', boxShadow: '0 0 0 8px rgba(243,67,162,.22), 0 24px 60px rgba(243,67,162,.3)', scale: 1.05}", "back.out(2)")
ft("#ash", t_cr, .9, "{xPercent: -160}", "{xPercent: 460}", "power2.inOut")
sfx("sparkle", t_cr)
t_ty = T("m03", "typed")
to("#uin", t_ty - .1, .3, "{boxShadow: '0 0 0 12px rgba(243,67,162,.18), 0 20px 50px rgba(243,67,162,.35)'}")
js(f'tl.fromTo("#cur2", {{opacity: 1}}, {{opacity: 0, duration: .2, ease: "steps(1)", yoyo: true, repeat: 3, immediateRender: false}}, {t_ty - .1:.3f});')
t_at = T("m03", "this") - .05      # v4: "@write-script" is typed on screen, not spoken
st("#cur2", t_at, "{opacity: 0}")
js(f'tl.fromTo("#ws1 i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: {.45 / 13:.3f}, immediateRender: false}}, {t_at:.3f});')
sfx("typing", t_at)
t_pill = t_at + .5
st("#ws1", t_pill, "{opacity: 0}")
ft("#wpill", t_pill, .35, "{opacity: 0, scale: 1.4}", "{opacity: 1, scale: 1}", "back.out(2.6)")
sfx("pop", t_pill)
t_req = t_pill + .15
js(f'tl.fromTo("#ws2 i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: {.7 / len(REQ):.3f}, immediateRender: false}}, {t_req:.3f});')
ft("#utrack", t_req + .2, .55, "{x: 0}", "{x: -330}", "power1.inOut")
sfx("typing", t_req + .05)
t_send = t_req + .78
to("#usend", t_send, .1, "{scale: .86}")
to("#usend", t_send + .1, .25, "{scale: 1.1, background: 'linear-gradient(135deg, #EE688B, #F343A2)'}", "back.out(3)")
sfx("click", t_send)
sfx("msg", t_send + .08)
st("#utrack", t_send + .12, "{opacity: 0}")
to("#uhome", t_send + .05, .3, "{opacity: 0, y: -120}", "power2.in")
ft("#um1", t_send + .12, .4, "{opacity: 0, y: 160, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
ft("#um2", t_send + .3, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.8)")
js(f'tl.fromTo("#udots i", {{y: 0}}, {{y: -14, duration: .14, yoyo: true, repeat: 3, stagger: .07, ease: "sine.inOut", immediateRender: false}}, {t_send + .35:.3f});')
st("#udots", t_send + .75, "{opacity: 0}")
ft("#um2t", t_send + .75, .4, "{opacity: 0, clipPath: 'inset(0 100% 0 0)'}", "{opacity: 1, clipPath: 'inset(0 0% 0 0)'}", "power1.out")
sfx("msg", t_send + .75)
tilt_app = js(f'tl.fromTo("#app", {{rotationY: 0, transformPerspective: 1400}}, {{rotationY: -4, transformPerspective: 1400, duration: 1.2, yoyo: true, repeat: 2, ease: "sine.inOut", immediateRender: false}}, {s3 + .7:.3f});')
head_out("h3", L0["m04"] - .25)
# Cree under the app: types on his phone, cheers at the pill, points at the answer
C3 = P(890, 1612, .4)
st("#cree", s3 - .1, "{opacity: 1}")
cree_walk(s3 - .1, s3 + .4, (1300, C3[1], C3[2]), C3, end="stand", end_flip=True)
pose(t_ty - .1, "phone", flip=True)
pose(t_pill - .05, "cheer")
cree_hop(t_pill, 70)
pose(t_send + .3, "point", flip=True)
sparkle(t_pill + .05, .8)

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
st("#app", s4, "{opacity: 0}")
ft("#tape", s4 + .02, .55, "{scaleX: 0}", "{scaleX: 1}", "power3.out")
sfx("tape", s4)
t_ms = max(T("m04", "measurements"), s4 + .45)
for i in range(3):
    ft(f"#th{i}", t_ms - .4 + .08 * i, .45, "{opacity: 0, y: 140, rotation: (i - 1) * 8}".replace("(i - 1) * 8", str((i - 1) * 8)), "{opacity: 1, y: 0, rotation: " + str((i - 1) * 3) + "}", "back.out(1.6)")
    sfx("cloth" if i == 1 else "pop", t_ms - .4 + .08 * i)
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
C4 = P(955, 1612, .34)
cree_to(s4 - .05, *C4, d=.01)
pose(s4, "mag", flip=True)
js(f'tl.fromTo("#creef", {{rotation: 0, y: 0}}, {{rotation: -8, y: -20, duration: .45, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}}, {s4 + .3:.3f});')
pose(T("m04", "pause") - .05, "think", flip=True)
pose(T("m04", "words") - .05, "point", flip=True)
pose(T("m04", "stop") - .05, "proud")

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
st("#cree", s5, "{opacity: 0}")
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
    sfx("snip", t_cu - .1 + .16 * k)
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
    sfx("sew", t)
js(f'tl.fromTo("#needle i", {{y: 0}}, {{y: 26, duration: .05, yoyo: true, repeat: {int(1.4 / .05)}, ease: "none", immediateRender: false}}, {t_st - .1:.3f});')
st("#needle", t_st + .9, "{opacity: 0}")
punch(T("m05", "voice"), 1.05)
sfx("sparkle", T("m05", "voice"))
head_out("h5b", e5 - .3)

# =======================================================================================================================
# 6 IT FITS: back in the mirror, the tailored script fits
s6, e6 = S["m06"], END["m06"]
stars = "".join(f'<div class="spk" id="sp{i}" style="left:{x}px;top:{y}px;width:{z}px;height:{z}px;color:{c}">{STAR}</div>'
                for i, (x, y, z, c) in enumerate([(130, 600, 90, LIME), (640, 540, 110, PINK), (690, 980, 70, LIME), (90, 1080, 76, PINK), (560, 760, 56, LIME)]))
HTML.append(f'<div class="scn" id="s6"><div class="mirror" id="mir1"><i class="mshine" id="msh1"></i></div>{person("p1")}'
            '<div class="gar fit" id="fitg">' + HANGER + '<div class="gcard pinkc"><u>MADE TO MEASURE</u><i></i><i></i><i></i></div></div>'
            f'{stars}<div class="hw6" id="hw6">…on a really good day.</div></div>')
head("h6", [[("Sounds", ""), ("like", ""), ("me.", "pk hl")]], 150, "m06", 124)
scene("s6", s6, e6)
curtain(s6)
st("#p1", s6, "{opacity: 1}")
person_idle("p1", s6, e6)
face("p1", s6, "smile", "happy")
st("#mir1", s6, "{opacity: 1}")
t_sd = T("m06", "sounds")
ft("#fitg", t_sd - .1, .5, "{opacity: 1, y: -1000}", "{opacity: 1, y: 0}", "back.out(1.2)")
sfx("hanger", t_sd + .3)
sfx("cloth", t_sd + .35)
arms("p1", t_sd + .3, -22, 22, .25)
arms("p1", T("m06", "me"), 150, -150, .3)
js(f'tl.fromTo("#p1, #fitg", {{y: 0}}, {{y: -26, duration: .18, yoyo: true, repeat: 3, ease: "power1.out", immediateRender: false}}, {T("m06", "me") + .05:.3f});')
for i in range(5):
    t = T("m06", "me") + .06 * i
    ft(f"#sp{i}", t, .4, "{opacity: 0, scale: 0, rotation: -90}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(3)")
    js(f'tl.to("#sp{i}", {{rotation: 180, duration: {e6 - t:.2f}, ease: "none"}}, {t + .4:.3f});')
sfx("sparkle", T("m06", "me"))
ft("#msh1", T("m06", "me"), 1.0, "{xPercent: -150}", "{xPercent: 350}", "power2.inOut")
t_rl = T("m06", "really")
ft("#hw6", t_rl - .2, .8, "{clipPath: 'inset(0 100% 0 0)', opacity: 1}", "{clipPath: 'inset(0 0% 0 0)', opacity: 1}", "power1.inOut")
punch(T("m06", "day"), 1.04)
head_out("h6", e6 - .3)
C6 = P(915, 1470, .46)
cree_to(s6 - .05, *C6, d=.01)
pose(s6, "proud", flip=True)
st("#cree", s6, "{opacity: 1}")
pose(T("m06", "me") - .05, "cheer")
cree_hop(T("m06", "me"), 100, 2)
sparkle(T("m06", "me") + .1, 1.0, 140)
pose(t_rl, "wave", flip=True)

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
sfx("typing", t_c2)
to("#csend", t_c2 + .48, .1, "{scale: .8}")
to("#csend", t_c2 + .58, .25, "{scale: 1.12, backgroundColor: '#F343A2'}", "back.out(3)")
sfx("click", t_c2 + .48)
ft("#csub", T("m07", "send") - .1, .45, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(1.8)")
t_lk = T("m07", "link")
ft("#csubhl", t_lk, .3, "{scaleX: 0}", "{scaleX: 1}", "power2.out")
ft("#dm2", t_lk - .1, .6, "{opacity: 0, y: -260}", "{opacity: 1, y: 0}", "back.out(1.6)")
sfx("msg", t_lk)
js(f'tl.fromTo("#ctag", {{rotation: 0}}, {{rotation: 4, duration: .9, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_sk + 1.0:.3f});')
C7 = P(540, 1600, .4)
st("#cree", s7 - .05, "{opacity: 0}")
cree_to(s7 - .05, *C7, d=.01)
st("#cree", s7 + .25, "{opacity: 1}")
pose(s7 + .25, "wave")
cree_hop(s7 + .25, 80)
pose(t_sk - .05, "cheer")
cree_hop(t_sk + .1, 90)
pose(t_c2 - .05, "phone")
pose(t_lk - .05, "point", flip=True)
cree_wiggle(t_lk + .1, 3, 6)
for tb in (1.4, 6.0, 13.2, 17.5, 21.0, 29.8):
    blink(tb)
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -9, duration: .8, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .8)}, immediateRender: false}}, 0);')
HTML.append(cree_html())

# ---- background (v3, owner: "keep the Creedom background as it is, that pink type of background"): the light and dark
# fluid worlds of the v1 / CHECK reels, pink blobs drifting under big frosted panes
LB = [(-200, -150, 760, "rgba(238,104,139,.55)"), (520, 260, 820, "rgba(255,190,214,.75)"), (-260, 980, 900, "rgba(217,194,255,.6)"),
      (480, 1280, 820, "rgba(255,216,194,.6)")]
DB = [(-220, -120, 800, "rgba(177,71,107,.55)"), (480, 900, 900, "rgba(243,67,162,.38)"), (-200, 1300, 760, "rgba(120,40,200,.35)")]
blobs_l = "".join(f'<i class="bl" id="lb{i}" style="left:{x}px;top:{y}px;width:{z}px;height:{z}px;background:{c}"></i>' for i, (x, y, z, c) in enumerate(LB))
blobs_d = "".join(f'<i class="bl" id="db{i}" style="left:{x}px;top:{y}px;width:{z}px;height:{z}px;background:{c}"></i>' for i, (x, y, z, c) in enumerate(DB))
for pre, n in (("lb", len(LB)), ("db", len(DB))):
    for i in range(n):
        js(f'tl.fromTo("#{pre}{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
           f'duration: {DUR / 3:.2f}, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false}}, 0);')
PANES = [(-300, 330, 560, 340, -18), (830, 1500, 600, 360, 16), (690, -170, 520, 300, 24), (-330, 1560, 600, 320, -10)]
panes = "".join(f'<i class="pane" id="pn{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>' for i, (x, y, w, h, r) in enumerate(PANES))
for i, (x, y, w, h, r) in enumerate(PANES):
    js(f'tl.fromTo("#pn{i}", {{rotation: {r}, x: 0, y: 0}}, {{rotation: {r + random.choice((-1, 1)) * random.randint(8, 14)}, x: {random.randint(-80, 80)}, '
       f'y: {random.randint(-160, 160)}, duration: {DUR / 4:.2f}, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, 0);')

CSS = open(os.path.join(ROOT, "build", "style2.css")).read() + open(os.path.join(ROOT, "build", "style_v1parts.css")).read() + open(os.path.join(ROOT, "build", "style3.css")).read()
for k, v in (("$INK", INK), ("$PINK", PINK), ("$LIME", LIME), ("$PAPER", PAPER)):
    CSS = CSS.replace(k, v)

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: @write-script, made to measure v4 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="world" id="light">{blobs_l}</div>
      <div class="world" id="dark">{blobs_d}</div>
      <div id="panes">{panes}</div>
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
