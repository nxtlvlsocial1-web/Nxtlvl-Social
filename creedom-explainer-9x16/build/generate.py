"""Creedom explainer reel, 9:16 (1080x1920). Writes index.html and plan/sfx_events.json.

v4, after "it still doesn't feel that engaging": rebuilt on the reference promo's own grammar (a new idea every
half second to second): full-screen word beats that fly past the camera, background flips, glitch hits, warp rays,
diagonal tickers, a word rolling in a pill, a 3D wall of cards, step beats and a slot-machine score, on a dark plum
ground with Creedom's magenta -> coral glow. Captions sit out where the big type already says the words.

Owner's brief: an explainer on creedom.ai from the owner's script, paced like the Nxtlvl promo, using the owner's
screen recording of the app where the script needs it, highly interactive from the hook to the end, with the mascot
Cree animated and expressive, colours from the Creedom logo (magenta -> pink -> coral on white/blush), original music
(build/music.py) and an ElevenLabs female voiceover (Hallie, eleven_v3; build/vo_tight.py).

v3, after the owner's notes ("text animations on those top texts are really poor", "frames cluttered and out of
proportion, use the space properly, nothing collapsing on each other", "crop the notch, build a clean notch", "very
static, not much motion, add glass fluid UI type animations"):
  * a fixed layout grid: headline band y 230-620, stage y 630-1170 (cards, phone), Cree in his own spot under or
    beside the stage, captions y 1500. Cards never sit on the phone: when the phone is on screen it takes the left
    column and the cards the right one.
  * headlines: words rise out of a mask one after another, accent words in the gradient with a light sweep, a punch
    and a drawn underline; words leave the same way (or slide off for "swiped away").
  * glass UI: frosted cards (backdrop blur, white rim, inner glow) that land with a 3D liquid pop and a light sweep,
    then float; a liquid blob wipe into the audit; the CTA colour floods out from Cree; the background is morphing
    blurred colour blobs plus drifting glass orbs; a slow camera push per scene and a whip between scenes.
  * the phone draws its own clean island; the recording's status bar is painted out (build/clips.py).
Timings come from the voiceover's word timings (plan/vo_tight.json).

python3 build/generate.py
"""
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 40
VO = json.load(open(os.path.join(ROOT, "plan", "vo_tight.json")))
VDUR = 35.43
DUR = 37.5
A, HIDE, EL, CUES, CAPS = [], [], [], [], []
NID = [0]
RND = random.Random(9)
GRAD = "linear-gradient(90deg,#F515E8 0%,#F54BA8 50%,#F5876C 100%)"
INK, PINK = "#0b0b0b", "#e0187e"   # creedom.ai ink and accent pink


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def cue(t, kind):
    CUES.append((round(t, 3), kind))


def W(text, n=1):
    """Start time of the n-th occurrence of a word (punctuation ignored)."""
    k = 0
    for w in VO:
        if w["text"].strip('.,"\'!?').lower() == text.lower():
            k += 1
            if k == n:
                return w["s"]
    raise KeyError(text)


def show(sel, t0, t1=None):
    js(f'tl.set("{sel}", {{opacity: 1}}, {max(0, t0):.3f});')
    if t1 is not None and t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')
    HIDE.append(sel)


def put(html):
    EL.append(html)


def pop(sel, t, frm=.3, d=.5, ease="back.out(1.8)", rot=0):
    js(f'tl.fromTo("{sel}", {{opacity: 0, scale: {frm}, rotation: {rot - 12}}}, {{opacity: 1, scale: 1, rotation: {rot}, duration: {d}, ease: "{ease}", '
       f'immediateRender: false}}, {t:.3f});')


def fly(sel, t, x=0, y=120, d=.55, blur=14, rot=0, ease="expo.out"):
    js(f'tl.fromTo("{sel}", {{opacity: 0, x: {x}, y: {y}, rotation: {rot}, filter: "blur({blur}px)"}}, {{opacity: 1, x: 0, y: 0, rotation: 0, '
       f'filter: "blur(0px)", duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def float_idle(sel, t, t1, amp=10, period=1.8):
    """A slow hover while something sits on screen (ends back where it started)."""
    reps = int((t1 - t) / (period / 2))
    reps -= 1 - reps % 2          # odd repeat count: the yoyo ends at the start value
    if reps >= 1:
        js(f'tl.fromTo("{sel}", {{y: 0}}, {{y: {-amp}, duration: {period / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: {reps}, immediateRender: false}}, {t:.3f});')


# ------------------------------------------------------------------------------------------------ kinetic type
def headline(lines, y, out=None, how="up", z=8):
    """Headline in the top band, set like the website: Fraunces, the first of two lines in warm grey and the second in
    ink. lines = [(text, size, t, accent)] with accent words in [brackets] (accent: pink / red / green / white).
    Inside each word's mask the letters rise in reading order; accent words land with a small punch and a drawn
    underline. out = when the letters leave (how: up, or left = slide off to the left)."""
    i = nid("h")
    rows = []
    for k, (text, size, t, acc) in enumerate(lines):
        ws = []
        for n, w in enumerate(text.split(" ")):
            a = w.startswith("[")
            w = w.replace("[", "").replace("]", "")
            ws.append(f'<span class="wm"><span class="wi{" acc " + acc if a else ""}" id="{i}l{k}w{n}">{chars(w)}</span></span>')
        tone = " grey" if len(lines) > 1 and k == 0 else ""
        under = ('<svg class="uline" viewBox="0 0 600 40" preserveAspectRatio="none"><path id="{0}u{1}" d="M 8 30 C 160 6 430 6 592 20" pathLength="1" '
                 'stroke-dasharray="1" stroke-dashoffset="1"/></svg>').format(i, k) if acc == "pink" and "[" in text and k == len(lines) - 1 else ""
        rows.append(f'<div class="hl{tone}" id="{i}l{k}" style="font-size:{size}px"><span class="hli">{" ".join(ws)}{under}</span></div>')
    put(f'<div class="head" id="{i}" style="top:{y}px;z-index:{z}">{"".join(rows)}</div>')
    show(f"#{i}", lines[0][2], out + .6 if out else None)
    for k, (text, size, t, acc) in enumerate(lines):
        show(f"#{i}l{k}", t)
        n = len(text.replace("[", "").replace("]", ""))
        st = min(.035, .45 / max(1, n))
        js(f'tl.fromTo("#{i}l{k} .ch", {{yPercent: 115, rotation: 6}}, {{yPercent: 0, rotation: 0, duration: .65, ease: "expo.out", stagger: {st:.3f}, '
           f'immediateRender: false}}, {t:.3f});')
        if "[" in text:
            first = [m for m, w in enumerate(text.split(" ")) if w.startswith("[")][0]
            ta = t + st * len(" ".join(text.split(" ")[:first])) + .3
            js(f'tl.fromTo("#{i}l{k} .acc", {{scale: 1}}, {{keyframes: [{{scale: 1.1, duration: .12, ease: "power2.out"}}, {{scale: 1, duration: .5, '
               f'ease: "elastic.out(1, .45)"}}], immediateRender: false}}, {ta:.3f});')
            if acc == "pink" and k == len(lines) - 1:
                js(f'tl.fromTo("#{i}u{k}", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .5, ease: "power2.out", immediateRender: false}}, {ta + .1:.3f});')
    if out:
        if how == "left":
            js(f'tl.to("#{i} .ch", {{x: -1300, rotation: -10, filter: "blur(12px)", duration: .5, ease: "power3.in", stagger: .012}}, {out:.3f});')
        else:
            js(f'tl.to("#{i} .ch", {{yPercent: -130, duration: .38, ease: "power3.in", stagger: .008}}, {out:.3f});')
            if lines[-1][3] == "pink" and "[" in lines[-1][0]:
                js(f'tl.to("#{i} .uline", {{opacity: 0, duration: .2}}, {out:.3f});')
    return i


# ------------------------------------------------------------------------------------------------ glass UI
def glass(html, x, y, w, t, t1=None, cls="", z=9, enter="liquid", rot=0, flt=True):
    """A frosted-glass card: lands with a 3D liquid pop (or slides in from a side), a light sweep crosses it, then it
    floats until it leaves (gout)."""
    i = nid("g")
    vis = "opacity:1;" if t <= 0 else ""
    put(f'<div class="glass {cls}" id="{i}" style="{vis}left:{x}px;top:{y}px;width:{w}px;z-index:{z}">{html}<i class="shine" data-layout-allow-overflow id="{i}s"></i></div>')
    if t <= 0:                      # on screen from frame 0: visible in CSS (the renderer skips sets at 0 s)
        if t1:
            js(f'tl.set("#{i}", {{opacity: 0}}, {t1:.3f});')
        t = .01
    else:
        show(f"#{i}", t, t1)
    if enter == "settle":
        js(f'tl.fromTo("#{i}", {{transformPerspective: 1200, scale: .9, rotationX: 18}}, {{scale: 1, rotationX: 0, duration: 1.1, ease: "power3.out", transformPerspective: 1200, '
           f'immediateRender: false}}, {t:.3f});')
    elif enter == "liquid":
        js(f'tl.fromTo("#{i}", {{transformPerspective: 1200, scale: .7, y: 90, rotationX: 32, rotation: {rot - 5}}}, {{scale: 1, y: 0, '
           f'rotationX: 0, rotation: {rot}, duration: .8, ease: "back.out(1.5)", transformPerspective: 1200, immediateRender: false}}, {t:.3f});')
        js(f'tl.fromTo("#{i}", {{opacity: 0, filter: "blur(12px)"}}, {{opacity: 1, filter: "blur(0px)", duration: .45, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    else:
        dx = 640 if enter == "right" else -640
        js(f'tl.fromTo("#{i}", {{transformPerspective: 1200, opacity: 0, x: {dx}, rotation: {rot + (10 if dx > 0 else -10)}, rotationY: {-35 if dx > 0 else 35}, filter: "blur(10px)"}}, '
           f'{{opacity: 1, x: 0, rotation: {rot}, rotationY: 0, filter: "blur(0px)", duration: .75, ease: "expo.out", transformPerspective: 1200, '
           f'immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#{i}s", {{xPercent: 0}}, {{xPercent: 420, duration: 1.0, ease: "power2.inOut", immediateRender: false}}, {t + .3:.3f});')
    if flt and t1:
        float_idle(f"#{i}", t + .9, t1 - 1.0, amp=9, period=2.0 + RND.uniform(-.3, .3))
    return i


def gout(sel, t, to="right", d=.45, y0=0):
    dx = {"right": 760, "left": -760, "down": 0, "up": 0}[to]
    dy = {"right": 0, "left": 0, "down": 500, "up": -400}[to]
    js(f'tl.to("{sel}", {{opacity: 0, x: {dx}, y: {y0 + dy}, rotation: {8 if dx >= 0 else -8}, scale: .9, filter: "blur(10px)", duration: {d}, '
       f'ease: "power3.in"}}, {t:.3f});')


def whip(t):
    """Camera whip between scenes: a quick push with motion blur."""
    js(f'tl.fromTo("#cam2", {{scale: 1, filter: "blur(0px)"}}, {{keyframes: [{{scale: 1.07, filter: "blur(9px)", duration: .16, ease: "power2.in"}}, '
       f'{{scale: 1, filter: "blur(0px)", duration: .3, ease: "power3.out"}}], immediateRender: false}}, {t:.3f});')
    cue(t, "whoosh")


def push(t0, t1, s0, s1):
    """Slow camera drift through a scene: in on one scene, out on the next, so the cuts never jump."""
    js(f'tl.fromTo("#cam", {{scale: {s0}}}, {{scale: {s1}, duration: {t1 - t0:.2f}, ease: "sine.inOut", immediateRender: false}}, {t0:.3f});')


def liquid(t, x, y, t_out):
    """Liquid blob wipe: a morphing gradient blob swells from (x, y) to cover the frame, then rises off it."""
    js(f'tl.set("#lq", {{x: {x - 1400}, y: {y - 1400}, scale: 0, opacity: 1, rotation: 0}}, {t:.3f});')
    js(f'tl.to("#lq", {{scale: 1.4, rotation: 40, borderRadius: "56% 44% 48% 52% / 46% 58% 42% 54%", duration: {t_out - t:.2f}, ease: "power3.in"}}, {t:.3f});')
    js(f'tl.to("#lq", {{y: {y - 1400 - 3200}, rotation: 80, borderRadius: "42% 58% 60% 40% / 55% 45% 55% 45%", duration: .55, ease: "power3.inOut"}}, {t_out:.3f});')
    js(f'tl.set("#lq", {{opacity: 0}}, {t_out + .56:.3f});')
    HIDE.append("#lq")
    cue(t, "whoosh_big")


def sparkle(x, y, t, n=8, r=180, z=24):
    """A burst of little four-point stars."""
    for k in range(n):
        sp = nid("sp")
        ang = k / n * 6.283 + RND.uniform(-.2, .2)
        c = ["#F515E8", "#F5876C", "#FFC83D", "#ffffff"][k % 4]
        put(f'<svg class="spk" id="{sp}" viewBox="-50 -50 100 100" style="left:{x - 22:.0f}px;top:{y - 22:.0f}px;z-index:{z}">'
            f'<path d="M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z" fill="{c}"/></svg>')
        show(f"#{sp}", t, t + 1.0)
        rr = r * RND.uniform(.7, 1.1)
        js(f'tl.fromTo("#{sp}", {{x: 0, y: 0, scale: 0, rotation: 0}}, {{x: {math.cos(ang) * rr:.0f}, y: {math.sin(ang) * rr:.0f}, scale: {RND.uniform(.6, 1.1):.2f}, '
           f'rotation: 180, opacity: 0, duration: .9, ease: "power2.out", immediateRender: false}}, {t:.3f});')


# ------------------------------------------------------------------------------------------------ Cree, the mascot
# Owner: "make him walk, stand on two legs, move his hands, make his face expressive" and "make him exactly like that
# i sent". So Cree is the mascot's own 3D render in thirteen poses (generated from the mascot image as the reference,
# cut out by build/poses.py): stand, walk + pass (a two-frame walk cycle), wave, point (right), present (left),
# cheer, shock, sad, mag (magnifying glass), phone (typing), think, proud. Every pose sits on one 820 x 820 canvas
# with the feet on y 800, so a pose swap never moves him; the body centre is (410, 500). Blinks: a shaded lid with
# a lash line over each open eye (plan/poses.json has the eyes).
POSES = json.load(open(os.path.join(ROOT, "plan", "poses.json")))
PCX, PCY = 410, 500


def cree_html():
    parts = []
    for name, m in POSES.items():
        defs, lids = "", ""
        for k, (cx, cy, rx, ry, top, bot) in enumerate(m["eyes"]):
            defs += (f'<linearGradient id="lg{name}{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
                     f'<stop offset="1" stop-color="{bot}"/></linearGradient>')
            lids += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 8}" ry="{ry + 8}" fill="url(#lg{name}{k})"/>'
                     f'<path d="M {cx - rx * .8:.0f} {cy + ry * .05:.0f} Q {cx} {cy + ry * .55:.0f} {cx + rx * .8:.0f} {cy + ry * .05:.0f}" fill="none" '
                     f'stroke="#2a0c22" stroke-width="9" stroke-linecap="round"/>')
        svg = f'<svg viewBox="0 0 820 820" class="clids"><defs>{defs}</defs><g class="lidg">{lids}</g></svg>' if lids else ""
        parts.append(f'<div class="cpose" id="cp-{name}"><img src="assets/img/poses/{name}.png" alt="">{svg}</div>')
    sweat = ('<svg viewBox="0 0 820 820" class="csw"><path class="sweat" d="M 690 190 C 675 220 665 240 665 255 A 25 25 0 0 0 715 255 C 715 240 705 220 690 190 Z" '
             'fill="#7fd3ff" stroke="#3aa6e6" stroke-width="5"/></svg>')
    return (f'<div id="cree"><div id="creeb"><div id="creef"><div id="creep">{"".join(parts)}</div></div>{sweat}</div>'
            f'<div id="bub"><span id="bubt">!</span></div></div>')


def cree_to(t, x, y, s, d=.6, rot=0, ease="power3.inOut"):
    """Move Cree (body centre at x, y in frame px; s = scale of the 820 px pose canvas)."""
    js(f'tl.to("#cree", {{x: {x - PCX:.0f}, y: {y - PCY:.0f}, scale: {s}, rotation: {rot}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def cree_set(t, x, y, s, rot=0):
    js(f'tl.set("#cree", {{x: {x - PCX:.0f}, y: {y - PCY:.0f}, scale: {s}, rotation: {rot}}}, {t:.3f});')


def pose(t, name, flip=None, squash=True):
    """Swap to a pose (flip: True faces him the other way, None keeps the current facing), with a little squash."""
    js(f'tl.set("#cree .cpose", {{opacity: 0}}, {t:.3f});')
    js(f'tl.set("#cp-{name}", {{opacity: 1}}, {t:.3f});')
    if flip is not None:
        js(f'tl.set("#creef", {{scaleX: {-1 if flip else 1}}}, {t:.3f});')
    if squash:
        js(f'tl.fromTo("#creep", {{scaleX: 1.07, scaleY: .9}}, {{scaleX: 1, scaleY: 1, duration: .28, ease: "back.out(3)", immediateRender: false}}, {t:.3f});')


def cree_walk(t0, t1, frm, to, end="stand", step=.15):
    """Walk from frm (x, y, s) to to (x, y, s): stride and pass frames alternate with a bob, facing the way he goes."""
    n = max(2, round((t1 - t0) / step))
    n += n % 2
    st = (t1 - t0) / n
    flip = to[0] < frm[0]
    js(f'tl.fromTo("#cree", {{x: {frm[0] - PCX:.0f}, y: {frm[1] - PCY:.0f}, scale: {frm[2]}}}, {{x: {to[0] - PCX:.0f}, y: {to[1] - PCY:.0f}, scale: {to[2]}, '
       f'duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    for k in range(n):
        pose(t0 + k * st, "walk" if k % 2 == 0 else "pass", flip=flip if k == 0 else None, squash=False)
    js(f'tl.fromTo("#creef", {{y: 0}}, {{y: -22, duration: {st / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: {2 * n - 1}, immediateRender: false}}, {t0:.3f});')
    js(f'tl.fromTo("#creef", {{rotation: -4}}, {{rotation: 4, duration: {st:.3f}, ease: "sine.inOut", yoyo: true, repeat: {n - 1}, immediateRender: false}}, {t0:.3f});')
    js(f'tl.to("#creef", {{rotation: 0, duration: .12}}, {t1:.3f});')
    pose(t1, end, flip=False)


def cree_hop(t, h=60, n=1, period=.36):
    for k in range(n):
        tk = t + k * period
        js(f'tl.fromTo("#creeb", {{y: 0, scaleY: 1, scaleX: 1}}, {{keyframes: [{{scaleY: .86, scaleX: 1.1, y: 10, duration: .07}}, '
           f'{{scaleY: 1.08, scaleX: .94, y: {-h}, duration: .14, ease: "power2.out"}}, {{scaleY: 1, scaleX: 1, y: 0, duration: .13, ease: "power2.in"}}, '
           f'{{scaleY: .92, scaleX: 1.06, y: 0, duration: .04}}, {{scaleY: 1, scaleX: 1, duration: .06}}], immediateRender: false}}, {tk:.3f});')


def cree_wiggle(t, n=3, amp=10, period=.22):
    js(f'tl.fromTo("#creeb", {{rotation: 0}}, {{keyframes: [' + ", ".join(f'{{rotation: {amp if k % 2 == 0 else -amp}, duration: {period / 2:.2f}}}' for k in range(n * 2))
       + f', {{rotation: 0, duration: .1}}], immediateRender: false}}, {t:.3f});')


def cree_face(t, mode, d=None):
    """blink (the lids of whichever pose is showing) or sweat (a drop that slides down); d = how long it stays."""
    if mode == "blink":
        js(f'tl.set("#cree .lidg", {{opacity: 1}}, {t:.3f});')
        js(f'tl.set("#cree .lidg", {{opacity: 0}}, {t + .11:.3f});')
        return
    js(f'tl.fromTo("#cree .sweat", {{opacity: 0, y: -20, scale: .4}}, {{opacity: 1, y: 0, scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#cree .sweat", {{y: 40, duration: {(d or 1) - .2:.2f}, ease: "power1.in"}}, {t + .25:.3f});')
    if d:
        js(f'tl.to("#cree .sweat", {{opacity: 0, duration: .1}}, {t + d:.3f});')


def cree_say(t, text, d=1.0, size=96):
    """A speech bubble next to Cree's head."""
    js(f'tl.set("#bubt", {{textContent: "{text}", fontSize: {size}}}, {t - .01:.3f});')
    js(f'tl.fromTo("#bub", {{opacity: 0, scale: .2, rotation: -30}}, {{opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(2.4)", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#bub", {{opacity: 0, scale: .6, duration: .2, ease: "power2.in"}}, {t + d:.3f});')


def prop(html, t, t1, cls="prop"):
    """Something Cree holds or wears (positioned inside #cree, in art coordinates)."""
    i = nid("pr")
    put_cree.append(f'<div class="{cls}" id="{i}">{html}</div>')
    show(f"#{i}", t, t1)
    js(f'tl.fromTo("#{i}", {{scale: .2, rotation: -40}}, {{scale: 1, rotation: 0, duration: .4, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    return i


put_cree = []


def caption_track():
    """Word captions under everything: up to four words, the spoken word in a gradient pill (the promo's pill)."""
    chunks, cur = [], []
    for k, w in enumerate(VO):
        cur.append(k)
        if len(cur) >= 4 or w["text"][-1] in ",.!?" or w["text"].endswith('"'):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    chunks = [c for c in chunks if VO[c[0]]["s"] < W("Comment") - .9 and not any(a <= VO[c[0]]["s"] < b for a, b in NOCAP)]
    for n, c in enumerate(chunks):
        t0 = VO[c[0]]["s"] - .05
        t1 = VO[chunks[n + 1][0]]["s"] - .05 if n + 1 < len(chunks) else VDUR + .2
        t1 = min([t1] + [a - .05 for a, b in NOCAP if a > t0])         # step aside for the big type
        i = nid("cap")
        spans = " ".join(f'<span class="cw" id="{i}w{k}">{VO[k]["text"]}</span>' for k in c)
        CAPS.append(f'<div class="cap" id="{i}">{spans}</div>')
        show(f"#{i}", t0, min(t1, W("Comment") - .9))
        js(f'tl.fromTo("#{i}", {{y: 24, opacity: 0}}, {{y: 0, opacity: 1, duration: .18, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
        for k in c:
            tk = VO[k]["s"] - .03
            js(f'tl.set("#{i}w{k}", {{attr: {{class: "cw on"}}}}, {tk:.3f});')
            nxt = VO[k + 1]["s"] - .03 if k + 1 < len(VO) else t1
            if k != c[-1]:
                js(f'tl.set("#{i}w{k}", {{attr: {{class: "cw"}}}}, {nxt:.3f});')


# ------------------------------------------------------------------------------------------------ v4 motion kit
# The reference promo's grammar: full-screen word beats that fly past the camera, background flips, glitch hits,
# warp rays, diagonal tickers, a word that rolls inside a pill, a 3D wall of cards, step beats and a slot-machine
# number. Dark plum ground with Creedom's magenta -> coral glow so the pink mascot and the UI pop.
NOCAP = []          # windows where the big type already says the words: no captions there


def chars(text, cls="ch"):
    return "".join(f'<span class="{cls}">{c if c != " " else "&nbsp;"}</span>' for c in text)


def beat(text, t, t_out, size, style="ink", y=820, through=True, sub=None):
    """A full-screen word beat in the website's serif (Fraunces): the letters arrive in reading order, each rising and
    un-blurring a moment after the one before it (the small line above first), then the word leaves letter by letter."""
    i = nid("b")
    body = f'<span class="bw">{chars(text)}</span>'
    if sub:
        body = f'<span class="bsub" style="font-size:{sub[1]}px">{chars(sub[0], "ch sc")}</span><br>' + body
    put(f'<div class="beat {style}" id="{i}" style="top:{y}px;font-size:{size}px">{body}</div>')
    show(f"#{i}", t, t_out + .45)
    nch = len(text) + (len(sub[0]) if sub else 0)
    t_exit = t_out - (.06 if style == "white" else .12)
    avail = t_exit - t - .02                       # the entrance must be over before the exit starts (or it pulls letters back)
    st = min(.05, .32 / max(1, nch), avail * .35 / max(1, nch - 1))
    dur = max(.18, min(.55, avail - st * (nch - 1)))
    js(f'tl.fromTo("#{i} .ch", {{transformPerspective: 800, opacity: 0, yPercent: 70, rotationX: -70, filter: "blur(10px)"}}, {{opacity: 1, yPercent: 0, rotationX: 0, '
       f'filter: "blur(0px)", duration: {dur:.3f}, ease: "expo.out", stagger: {st:.3f}, transformPerspective: 800, immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#{i}", {{scale: 1.05}}, {{scale: 1, duration: {max(.3, t_out - t):.2f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    d_out = .08 if style == "white" else .16         # out fast, so the next word lands on a clean frame
    js(f'tl.to("#{i} .ch", {{opacity: 0, yPercent: {-60 if through else 60}, filter: "blur(8px)", duration: {d_out}, ease: "power2.in", '
       f'stagger: .008}}, {t_exit:.3f});')
    return i


def flip(t, t1, bg, fade=.12):
    """Background flip: the whole ground turns a colour (white flash, magenta) for a beat."""
    i = nid("f")
    FLIPS.append(f'<div class="flip" id="{i}" style="background:{bg}"></div>')
    js(f'tl.fromTo("#{i}", {{opacity: 0}}, {{opacity: 1, duration: .06, immediateRender: false}}, {t:.3f});')
    if t1 < DUR:
        js(f'tl.to("#{i}", {{opacity: 0, duration: {fade}}}, {t1:.3f});')
    HIDE.append(f"#{i}")
    return i


FLIPS = []


def glitch(t, strong=1.0):
    """Glitch hit: RGB split, a sideways jitter and torn colour bands, about a fifth of a second."""
    a = 14 * strong
    js(f'tl.fromTo("#cam2", {{x: 0, filter: "drop-shadow(0px 0 0 rgba(0,240,255,0)) drop-shadow(0px 0 0 rgba(255,0,200,0))"}}, {{keyframes: ['
       f'{{x: {-a:.0f}, filter: "drop-shadow({a:.0f}px 0 0 rgba(0,240,255,.75)) drop-shadow({-a:.0f}px 0 0 rgba(255,0,200,.75))", duration: .05}}, '
       f'{{x: {a * .7:.0f}, filter: "drop-shadow({-a * .7:.0f}px 0 0 rgba(0,240,255,.6)) drop-shadow({a * .7:.0f}px 0 0 rgba(255,0,200,.6))", duration: .05}}, '
       f'{{x: {-a * .4:.0f}, duration: .04}}, {{x: 0, filter: "drop-shadow(0px 0 0 rgba(0,240,255,0)) drop-shadow(0px 0 0 rgba(255,0,200,0))", duration: .06}}], '
       f'immediateRender: false}}, {t:.3f});')
    for k in range(4):
        g = nid("gb")
        y, h = RND.uniform(150, 1750), RND.choice([10, 18, 34, 60])
        GBANDS.append(f'<i class="gband" id="{g}" style="top:{y:.0f}px;height:{h}px;background:{["#00f0ff", "#ff2bd6", "#ffffff", "#F5876C"][k]}"></i>')
        js(f'tl.fromTo("#{g}", {{opacity: 0, x: {RND.uniform(-300, 300):.0f}}}, {{keyframes: [{{opacity: .85, duration: .03}}, {{x: {RND.uniform(-300, 300):.0f}, duration: .08}}, '
           f'{{opacity: 0, duration: .04}}], immediateRender: false}}, {t + k * .02:.3f});')
        HIDE.append(f"#{g}")
    cue(t, "swish")


GBANDS = []


def rays(t0, t1, n=44, cx=540, cy=820, color="rgba(255,190,240,.85)"):
    """Warp streaks rushing out from the centre."""
    i = nid("ry")
    lines = ""
    for k in range(n):
        ang = RND.uniform(0, 360)
        lines += f'<i class="ray" style="left:{cx}px;top:{cy}px;transform:rotate({ang:.0f}deg)"><i class="rl" id="{i}r{k}" style="background:linear-gradient(90deg,transparent,{color})"></i></i>'
    put(f'<div class="rays" id="{i}"{" style=\"opacity:1\"" if t0 <= 0 else ""}>{lines}</div>')
    if t0 <= 0:
        RAYS0.append(f"#{i}")
    else:
        show(f"#{i}", t0, t1)
    if t0 > 0 or t1 < DUR:
        js(f'tl.to("#{i}", {{opacity: 0, duration: .25}}, {t1 - .25:.3f});')
    for k in range(n):
        d = RND.uniform(.5, .95)
        reps = max(0, int((t1 - t0) / d) - 1)
        js(f'tl.fromTo("#{i}r{k}", {{x: {RND.uniform(30, 260):.0f}, scaleX: .3}}, {{x: 1250, scaleX: 1.6, duration: {d:.2f}, ease: "power2.in", repeat: {reps}, '
           f'immediateRender: false}}, {max(.01, t0) + RND.uniform(0, d):.3f});')
    return i


RAYS0 = []


def ticker(y, rot, words, t0, t1, dirn=1, style="mag"):
    i = nid("tk")
    txt = " &#10022; ".join(words * 6)
    put(f'<div class="tkw {style}" id="{i}" style="top:{y}px"><div class="tki" id="{i}i">{txt}</div></div>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i}", {{scaleY: 0, rotation: {rot}}}, {{scaleY: 1, rotation: {rot}, duration: .3, ease: "expo.out", immediateRender: false}}, {t0:.3f});')
    js(f'tl.fromTo("#{i}i", {{x: {-200 if dirn > 0 else -1400}}}, {{x: {-1400 if dirn > 0 else -200}, duration: {t1 - t0:.2f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    js(f'tl.to("#{i}", {{scaleY: 0, duration: .22, ease: "power2.in"}}, {t1 - .22:.3f});')
    return i


def slot_html(i, digits):
    cols = ""
    for k, d in enumerate(digits):
        stack = "".join(f"<b>{n % 10}</b>" for n in range(30))
        cols += f'<span class="sw"><span class="sc" id="{i}d{k}">{stack}</span></span>'
    return cols


def slot_roll(i, digits, t, d=1.1):
    for k, dg in enumerate(digits):
        idx = 20 + int(dg)
        js(f'tl.fromTo("#{i}d{k}", {{yPercent: 0}}, {{yPercent: {-idx / 30 * 100:.3f}, duration: {d + k * .25:.2f}, ease: "back.out(1.1)", immediateRender: false}}, {t:.3f});')


# ------------------------------------------------------------------------------------------------ the phone
PHONE = {}


def phone_build(clips, x, y, w):
    PHONE.update(x=x, y=y, w=w)
    h = round(w * 1434 / 660)
    vids = "".join(f'<video id="pv{k}" class="pv" src="assets/video/{f}" data-start="{s:.3f}" data-duration="{d:.3f}" data-track-index="{2 + k}" muted playsinline></video>'
                   for k, (f, s, d) in enumerate(clips))
    put(f'<div id="phone" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div id="phonei"><div class="scr">{vids}'
        f'<i class="scan" data-layout-allow-overflow id="scan"></i><i class="refl" data-layout-allow-overflow id="refl"></i></div><i class="isl"></i></div></div>')
    for k, (f, s, d) in enumerate(clips):
        show(f"#pv{k}", s, s + d)
        js(f'tl.fromTo("#pv{k}", {{scale: 1.08, filter: "blur(8px)"}}, {{scale: 1, filter: "blur(0px)", duration: .35, ease: "power3.out", immediateRender: false}}, {s:.3f});')
        js(f'tl.fromTo("#refl", {{xPercent: -160}}, {{xPercent: 260, duration: .9, ease: "power2.inOut", immediateRender: false}}, {s + .05:.3f});')


def phone_in(t, t1):
    show("#phone", t, t1)
    js(f'tl.fromTo("#phone", {{transformPerspective: 1400, opacity: 0, y: 1000, rotationX: 40, rotationY: -20, rotation: -10, scale: .75}}, {{opacity: 1, y: 0, rotationX: 0, '
       f'rotationY: 0, rotation: 0, scale: 1, duration: .85, ease: "expo.out", transformPerspective: 1400, immediateRender: false}}, {t:.3f});')
    reps = int((t1 - t - 1) / 2.4)
    reps -= 1 - reps % 2
    if reps >= 1:
        js(f'tl.fromTo("#phonei", {{transformPerspective: 1400, rotationY: -6, y: 0}}, {{rotationY: 6, y: -14, duration: 2.4, ease: "sine.inOut", yoyo: true, '
           f'repeat: {reps}, transformPerspective: 1400, immediateRender: false}}, {t + .85:.3f});')


# ------------------------------------------------------------------------------------------------ the scenes
def scenes():
    t_told, t_me, t_the, t_exact, t_sec, t_ppl, t_stop = W("told"), W("me"), W("the"), W("exact"), W("second"), W("people"), W("stopped")
    t_up, t_flop, t_cr, t_rl, t_and, t_wat, t_sec2 = W("uploaded"), W("flopped"), W("Creedom's"), W("Reel", 1), W("and"), W("watched"), W("second", 2)
    t_it, t_hook, t_ene, t_drop, t_mid, t_ppl2, t_swp = W("It", 3), W("hook"), W("energy"), W("dropped"), W("middle"), W("people", 2), W("swiped")
    t_also, t_new, t_what, t_fix = W("also"), W("new"), W("what"), W("fix")
    t_you, t_free, t_audit, t_acc, t_just, t_type, t_hand = W("You"), W("free"), W("audit"), W("account"), W("Just"), W("type"), W("handle")
    t_20, t_score, t_100, t_first, t_fix2 = W("20"), W("score"), W("100"), W("first"), W("fix", 2)
    t_com, t_cree, t_send, t_link = W("Comment"), W("CREE"), W("send"), W("link")
    S2, S3, S4, S5, S6, S7 = t_up - .25, t_it - .2, t_also - .3, t_you - .25, t_com - .9, VDUR + .05
    for k, (a, b) in enumerate([(0, S2), (S2, t_cr), (t_cr, S3), (S3, S4), (S4, S5), (S5, S6), (S6, S7)]):
        push(a, b, *((1, 1.04) if k % 2 == 0 else (1.04, 1)))

    # ---- S1 the hook: "This AI told me the exact second people stopped watching my reel."
    # Owner's reference (a picker-wheel title): a drum of lines in a tight grotesk; the line in focus in the brand
    # gradient, the ones it has passed above it in fading grey, the next one waiting faint below, a 3D curve on the
    # drum; every turn is a fast upward scroll with a vertical motion blur that settles; a small block beside it
    # (here the rest of the sentence) lights up word by word as it is spoken.
    NOCAP.append((0, S2 - .1))
    items = ["This AI", "told me", "the exact", "second."]
    turns = [.02, t_told - .06, t_the - .06, t_sec - .06]
    H, FY, XR = 142, 640, 650                         # row height, focus line centre, right edge of the drum
    rows = "".join(f'<div class="di" id="di{k}" style="top:{k * H}px"><span class="dg">{w}</span><span class="dc" id="dc{k}">{w}</span></div>'
                   for k, w in enumerate(items))
    put(f'<div class="drumw" id="drw" style="top:{FY - H // 2}px;width:{XR}px"><div class="drum" id="drum">{rows}</div></div>')
    show("#drw", .02, S2 - .02)

    def look(d):
        """scale, opacity, rotationX, pull toward the focus line for a row d rows from the focus."""
        sc = {0: 1, -1: .8, 1: .8, -2: .66, 2: .66}.get(d, .56)
        op = {0: 1, -1: .62, -2: .34, 1: .26, 2: .1}.get(d, .14 if d < 0 else 0)
        pull = 0 if d == 0 else -math.copysign(1, d) * (1 - sc) * H * .55 * min(abs(d), 2)
        return sc, op, 0, pull          # no tilt: pivoting on the right edge skewed the rows like italics
    for k in range(len(items)):
        sc, op, rx, pull = look(k)
        js(f'tl.fromTo("#di{k}", {{transformPerspective: 900, scale: {sc}, opacity: 0, rotationX: {rx}, y: {pull:.0f}}}, {{transformPerspective: 900, scale: {sc}, '
           f'opacity: {op}, rotationX: {rx}, y: {pull:.0f}, duration: .5, ease: "expo.out", immediateRender: false}}, .02);')
        js(f'tl.fromTo("#dc{k}", {{opacity: 0}}, {{opacity: {1 if k == 0 else 0}, duration: .3, immediateRender: false}}, .02);')
    js(f'tl.fromTo("#drum", {{y: {H * 1.7:.0f}}}, {{y: 0, duration: .62, ease: "expo.out", immediateRender: false}}, .02);')
    js('tl.fromTo("#vbg", {attr: {stdDeviation: "0 22"}}, {attr: {stdDeviation: "0 0"}, duration: .45, ease: "power2.out", immediateRender: false}, .02);')
    cue(.02, "whoosh")
    for f, tf in list(enumerate(turns))[1:]:
        js(f'tl.to("#drum", {{y: {-f * H}, duration: .5, ease: "expo.out"}}, {tf:.3f});')
        js(f'tl.fromTo("#vbg", {{attr: {{stdDeviation: "0 18"}}}}, {{attr: {{stdDeviation: "0 0"}}, duration: .34, ease: "power2.out", immediateRender: false}}, {tf:.3f});')
        for k in range(len(items)):
            sc, op, rx, pull = look(k - f)
            js(f'tl.to("#di{k}", {{transformPerspective: 900, scale: {sc}, opacity: {op}, rotationX: {rx}, y: {pull:.0f}, duration: .5, ease: "expo.out"}}, {tf:.3f});')
            js(f'tl.to("#dc{k}", {{opacity: {1 if k == f else 0}, duration: .25}}, {tf:.3f});')
        cue(tf, "swish" if f < len(items) - 1 else "hit")
    js(f'tl.fromTo("#di3", {{scale: 1}}, {{keyframes: [{{scale: 1.07, duration: .14, ease: "power2.out"}}, {{scale: 1, duration: .5, ease: "elastic.out(1, .5)"}}], '
       f'immediateRender: false}}, {turns[3] + .3:.3f});')
    # the block beside it: the rest of the sentence, each word lights up as it is said
    words = [("people", t_ppl), ("stopped", t_stop), ("watching", W("watching")), ("my reel.", W("my", 2))]
    blk = "".join(f'<div class="bwm"><span class="bwl" id="bwl{k}">{w}</span></div>' for k, (w, _) in enumerate(words))
    put(f'<div class="dblock" id="dblk" style="left:{XR + 30}px;top:{FY - H // 2 + 6}px">{blk}</div>')
    show("#dblk", .25, S2 - .02)
    js('tl.fromTo(".bwl", {yPercent: 110, filter: "blur(6px)"}, {yPercent: 0, filter: "blur(0px)", duration: .55, ease: "expo.out", stagger: .07, immediateRender: false}, .25);')
    for k, (w, tw) in enumerate(words):
        js(f'tl.to("#bwl{k}", {{color: "{PINK if k < 3 else "#e11d48"}", duration: .15}}, {tw - .03:.3f});')
        js(f'tl.fromTo("#bwl{k}", {{scale: 1}}, {{keyframes: [{{scale: 1.12, duration: .1}}, {{scale: 1, duration: .3, ease: "power2.out"}}], immediateRender: false}}, {tw - .03:.3f});')
    # out: the drum keeps turning up and away, the block lifts off
    js(f'tl.to("#drum", {{y: {-(len(items) + 2) * H}, opacity: 0, duration: .45, ease: "power3.in"}}, {S2 - .45:.3f});')
    js(f'tl.fromTo("#vbg", {{attr: {{stdDeviation: "0 0"}}}}, {{attr: {{stdDeviation: "0 24"}}, duration: .45, ease: "power3.in", immediateRender: false}}, {S2 - .45:.3f});')
    js(f'tl.to(".bwl", {{yPercent: -110, filter: "blur(6px)", duration: .35, ease: "power3.in", stagger: .04}}, {S2 - .45:.3f});')
    # the retention line: neon, full width, it crashes where people left
    av = "".join(f'<i class="av" id="av{k}"><svg viewBox="0 0 40 40"><circle cx="20" cy="14" r="8"/><path d="M 5 38 C 6 26 34 26 35 38 Z"/></svg></i>' for k in range(7))
    g = glass(f'<div class="gh"><span class="gt">RETENTION</span><span class="gp" id="gp">100%</span></div><div class="avs">{av}</div>'
              f'<svg viewBox="0 0 700 240" class="gs"><path class="gl0" d="M 0 230 H 700"/>'
              f'<path class="gline" id="gl" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M 0 24 C 80 28 160 34 240 44 C 300 50 330 54 360 58 '
              f'C 380 62 395 130 410 190 C 430 206 520 212 700 216"/><circle class="gdot" id="gd" cx="372" cy="66" r="16"/></svg>'
              f'<div class="gtag" id="gtag">0:07 &middot; they left here</div>', 70, 880, 690, t_ppl, S2 - .2, cls="graph", flt=False)
    js(f'tl.fromTo("#gl", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .8, ease: "power1.inOut", immediateRender: false}}, {t_ppl + .1:.3f});')
    js(f'tl.fromTo("#gp", {{textContent: 100}}, {{textContent: 38, duration: .8, ease: "power2.in", snap: {{textContent: 1}}, '
       f'modifiers: {{textContent: (v) => Math.round(v) + "%"}}, immediateRender: false}}, {t_ppl + .1:.3f});')
    js(f'tl.fromTo(".av", {{opacity: 0, y: 30, scale: .5}}, {{opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)", stagger: .04, immediateRender: false}}, {t_ppl:.3f});')
    flip(t_stop, t_stop + .1, "#ff2d55", fade=.15)
    pop("#gd", t_stop - .02, frm=0)
    js(f'tl.to("#gd", {{scale: 1.6, opacity: .5, duration: .25, yoyo: true, repeat: 3}}, {t_stop + .25:.3f});')
    pop("#gtag", t_stop + .05, frm=.4)
    cue(t_stop - .02, "alert")
    js(f'tl.to(["#av2", "#av3", "#av4", "#av5", "#av6"], {{keyframes: [{{background: "rgba(255,45,85,.95)", duration: .1}}, {{x: -60, y: 140, rotation: -40, '
       f'opacity: 0, duration: .5, ease: "power2.in"}}], stagger: .07}}, {t_stop + .2:.3f});')
    cue(t_stop + .25, "swish")
    js(f'tl.fromTo("#{g}", {{x: 0}}, {{keyframes: [{{x: -16, duration: .04}}, {{x: 14, duration: .04}}, {{x: -8, duration: .04}}, {{x: 0, duration: .04}}], '
       f'immediateRender: false}}, {t_stop:.3f});')
    gout(f"#{g}", S2 - .35, to="down")
    cree_set(0, 880, 1700, .38)
    js(f'tl.fromTo("#cree", {{opacity: 0, y: 1700 - {PCY}}}, {{opacity: 1, y: {1330 - PCY}, duration: .45, ease: "back.out(1.8)", immediateRender: false}}, {t_stop - .15:.3f});')
    pose(t_stop - .15, "shock", squash=False)
    cue(t_stop - .15, "pop")
    cree_face(t_stop, "sweat", d=1.2)
    cree_say(t_stop + .05, "!", d=1.0)

    # ---- S2a: "I uploaded a reel that flopped"
    hf = headline([("I uploaded a reel", 76, t_up, None), ("that [flopped.]", 118, t_flop, "red")], 240, out=t_cr - .4)
    js(f'tl.fromTo("#{hf}l1", {{x: 0}}, {{keyframes: [{{x: -16, duration: .05}}, {{x: 16, duration: .05}}, {{x: -10, duration: .05}}, {{x: 8, duration: .05}}, '
       f'{{x: 0, duration: .05}}], immediateRender: false}}, {t_flop + .35:.3f});')
    r = glass(f'<div class="rv" id="rv"><i class="play"></i><div class="up" id="up"><div class="upt">Uploading <b id="upn">0%</b></div>'
              f'<div class="upb"><i id="upf"></i></div></div></div><div class="rm"><b>my_reel.mp4</b><span class="views"><b id="vn">0</b> views '
              f'<em id="vd">&darr; 84%</em></span></div><div class="stampf" id="stamp">FLOPPED</div>', 220, 600, 460, S2 + .05, t_cr - .1, cls="reel", flt=False)
    cue(S2 + .05, "whoosh")
    js(f'tl.fromTo("#upf", {{scaleX: 0}}, {{scaleX: 1, duration: .55, ease: "power2.inOut", immediateRender: false}}, {t_up + .05:.3f});')
    js(f'tl.fromTo("#upn", {{textContent: 0}}, {{textContent: 100, duration: .55, ease: "power2.inOut", snap: {{textContent: 1}}, modifiers: {{textContent: (v) => Math.round(v) + "%"}}, '
       f'immediateRender: false}}, {t_up + .05:.3f});')
    js(f'tl.to("#up", {{opacity: 0, y: 30, duration: .2}}, {t_up + .65:.3f});')
    js(f'tl.fromTo("#vn", {{textContent: 0}}, {{textContent: 312, duration: .45, ease: "power2.out", snap: {{textContent: 1}}, immediateRender: false}}, {t_up + .7:.3f});')
    pop("#vd", t_flop, frm=.4)
    flip(t_flop, t_flop + .08, "#ff2d55", fade=.2)
    js(f'tl.to("#{r}", {{rotationX: 18, y: 40, duration: .45, ease: "bounce.out", transformPerspective: 1200}}, {t_flop:.3f});')
    js(f'tl.to("#rv", {{filter: "grayscale(.85) brightness(.75)", duration: .3}}, {t_flop:.3f});')
    pop("#stamp", t_flop + .05, frm=2.6, d=.28, ease="back.out(2)", rot=-12)
    cue(t_flop + .05, "stamp")
    js(f'tl.to("#{r}", {{x: 220, y: 300, scale: .15, rotation: 25, opacity: 0, duration: .4, ease: "power3.in"}}, {t_cr - .5:.3f});')
    cree_walk(S2 + .05, t_flop - .1, (880, 1330, .38), (860, 1320, .40), end="sad")
    cree_say(t_flop + .1, "...", d=.8, size=70)

    # ---- S2b: "into Creedom's Reel Analyzer, and it watched it second by second."
    glitch(t_cr - .12, .9)
    flip(t_cr - .1, t_cr - .02, INK, fade=.1)
    phone_build([("c1_pick.mp4", t_cr - .1, 2.0), ("c2_steps.mp4", t_cr + 1.9, 2.0),
                 ("c4_fixes.mp4", t_what - .3, S5 - t_what + .1)], 330, 540, 420)
    phone_in(t_cr - .1, S3 - .05)
    cue(t_cr - .1, "whoosh_big")
    tk1 = ticker(760, -14, ["REEL ANALYZER", "SECOND BY SECOND", "HOOK SCORE", "RETENTION"], t_cr - .05, t_wat + .1, 1, "mag")
    tk2 = ticker(1060, 9, ["CREEDOM", "AI FEEDBACK", "WHAT TO FIX", "NEW HOOKS"], t_cr + .05, t_wat + .1, -1, "ink")
    ch = glass('<img src="assets/img/cree.png" alt=""><span>Creedom &middot; <b>Reel Analyzer</b></span>', 0, 250, 0, t_cr, t_wat - .1, cls="chip", flt=False)
    js(f'tl.to("#{ch}", {{opacity: 0, y: -40, filter: "blur(8px)", duration: .25}}, {t_wat - .35:.3f});')
    cue(t_cr, "pop")
    pose(t_cr, "present")
    cree_to(t_cr - .1, 940, 1350, .36, d=.45)
    # it watched it second by second: the camera dives into the screen, timestamps tick out around it
    js(f'tl.to("#phone", {{scale: 1.18, y: -58, duration: .7, ease: "expo.inOut"}}, {t_wat - .25:.3f});')
    show("#scan", t_wat, S3)
    js(f'tl.fromTo("#scan", {{yPercent: -100}}, {{yPercent: 900, duration: .6, ease: "none", repeat: 2, immediateRender: false}}, {t_wat:.3f});')
    headline([("[Second] by [second].", 96, t_sec2 - .1, "pink")], 230, out=S3 - .35)
    cue(t_sec2, "tick")
    for k in range(8):
        tc = nid("ts")
        side = -1 if k % 2 == 0 else 1
        x = 540 + side * RND.uniform(360, 430) - 80
        y = 600 + k * 82
        put(f'<div class="tchip" id="{tc}" style="left:{x:.0f}px;top:{y:.0f}px">0:0{k + 1}</div>')
        tt = t_wat + .05 + k * .2
        show(f"#{tc}", tt, S3 - .1)
        js(f'tl.fromTo("#{tc}", {{opacity: 0, scale: .3, x: {-side * 120}}}, {{opacity: 1, scale: 1, x: 0, duration: .3, ease: "back.out(2.4)", immediateRender: false}}, {tt:.3f});')
        js(f'tl.to("#{tc}", {{opacity: 0, scale: .6, y: -40, duration: .2}}, {S3 - .3:.3f});')
        if k % 2 == 0:
            cue(tt, "tick")
    cree_to(t_wat - .3, 930, 1360, .36, d=.4)
    pose(t_wat, "mag")
    js(f'tl.fromTo("#creef", {{rotation: 0}}, {{rotation: -6, duration: .45, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, {t_wat + .3:.3f});')
    js(f'tl.to("#phone", {{scale: 2.4, opacity: 0, filter: "blur(16px)", duration: .35, ease: "power3.in"}}, {S3 - .3:.3f});')
    glitch(S3 - .1)

    # ---- S3: "It told me my [hook worked], but my [energy dropped] in the middle, and that's exactly where [people swiped] away."
    headline([("It told me my", 92, t_it, None)], 350, out=S4 - .4)
    put('<div class="pill" id="pill"><div class="pst" id="pst"><div class="pw">HOOK WORKED &#10003;</div><div class="pw">ENERGY DROPPED &darr;</div>'
        '<div class="pw">PEOPLE SWIPED &larr;</div></div><i class="shine" data-layout-allow-overflow id="pills"></i></div>')
    show("#pill", t_hook - .05, S4 - .3)
    js(f'tl.fromTo("#pill", {{opacity: 0, scaleX: .2, scaleY: .6}}, {{opacity: 1, scaleX: 1, scaleY: 1, duration: .45, ease: "back.out(1.8)", immediateRender: false}}, {t_hook - .05:.3f});')
    for k, (tt, col) in enumerate([(t_ene, "#e11d48"), (t_ppl2, "#0b0b0b")]):
        js(f'tl.to("#pst", {{yPercent: {-(k + 1) * 100 / 3:.3f}, duration: .45, ease: "back.inOut(1.6)"}}, {tt - .05:.3f});')
        js(f'tl.to("#pill", {{background: "{col}", boxShadow: "0 20px 60px {col}88", duration: .3}}, {tt - .05:.3f});')
        js(f'tl.fromTo("#pills", {{xPercent: 0}}, {{xPercent: 420, duration: .7, ease: "power2.inOut", immediateRender: false}}, {tt + .2:.3f});')
        cue(tt - .05, "whoosh")
    js(f'tl.fromTo("#pills", {{xPercent: 0}}, {{xPercent: 420, duration: .7, ease: "power2.inOut", immediateRender: false}}, {t_hook + .3:.3f});')
    js(f'tl.to("#pill", {{opacity: 0, scale: .6, y: -60, duration: .3, ease: "power2.in"}}, {S4 - .45:.3f});')
    cue(t_hook, "success")
    # visual 1: the hook score ring
    hk = glass('<div class="hring"><svg viewBox="0 0 200 200"><circle class="hb" cx="100" cy="100" r="80"/><circle class="hf" id="hkr" cx="100" cy="100" r="80" '
               'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg><div class="hv"><b id="hkn">0</b><small>/100</small></div></div>'
               '<div class="hkt"><div class="hkl">HOOK &middot; 0:00-0:03</div><div class="hkv">Strong start</div></div>', 140, 760, 800, t_hook + .05, t_ene - .1,
               cls="hookbig", flt=False)
    js(f'tl.fromTo("#hkr", {{strokeDashoffset: 1}}, {{strokeDashoffset: .08, duration: .9, ease: "power3.out", immediateRender: false}}, {t_hook + .25:.3f});')
    js(f'tl.fromTo("#hkn", {{textContent: 0}}, {{textContent: 92, duration: .9, ease: "power3.out", snap: {{textContent: 1}}, immediateRender: false}}, {t_hook + .25:.3f});')
    gout(f"#{hk}", t_ene - .3, to="left")
    # visual 2: the energy bars crash in the middle
    bars = "".join(f'<i class="eb" id="eb{k}" style="height:{h}px"></i>' for k, h in enumerate([210, 240, 225, 245, 230, 215, 200, 215, 235, 245]))
    en = glass(f'<div class="et">ENERGY</div><div class="ebars">{bars}<i class="emid" id="emid"></i></div><div class="edrop" id="edrop">&darr; dropped at 0:07</div>',
               140, 760, 800, t_ene - .15, t_ppl2 - .1, cls="energy", enter="right", flt=False)
    js('tl.to(["#eb3", "#eb4", "#eb5", "#eb6"], {height: (k) => [90, 40, 30, 70][k], background: "#ff2d55", boxShadow: "0 0 24px rgba(255,45,85,.8)", '
       f'duration: .5, ease: "bounce.out", stagger: .05}}, {t_drop:.3f});')
    flip(t_drop, t_drop + .06, "#ff2d55", fade=.15)
    pop("#emid", t_mid - .05, frm=.4)
    pop("#edrop", t_drop + .2, frm=.5)
    cue(t_drop, "drop")
    gout(f"#{en}", t_ppl2 - .35, to="left")
    # visual 3: the reels get flicked away
    for k in range(5):
        s = nid("sc")
        put(f'<div class="mini" id="{s}" style="left:{300 + k * 40}px;top:{690 + k * 14}px;z-index:{12 + k}"><i class="play"></i></div>')
        show(f"#{s}", t_ppl2 - .1, S4)
        pop(f"#{s}", t_ppl2 - .1 + k * .05, frm=.5, rot=-8 + k * 4)
        js(f'tl.to("#{s}", {{x: -900, rotation: -40, opacity: 0, filter: "blur(10px)", duration: .4, ease: "power3.in"}}, {t_swp + .05 + k * .1:.3f});')
        if k % 2 == 0:
            cue(t_swp + .05 + k * .1, "swish")
    vc = nid("vc")
    put(f'<div class="vcount" id="{vc}">&minus;62% viewers</div>')
    show(f"#{vc}", t_swp + .3, S4 - .2)
    pop(f"#{vc}", t_swp + .3, frm=.3)
    cree_to(S3, 900, 1360, .36, d=.4)
    pose(S3, "stand")
    pose(t_hook, "cheer")
    cree_hop(t_hook + .05, h=50, n=2)
    pose(t_ene - .2, "think")
    pose(t_drop, "sad")
    cree_face(t_drop, "sweat", d=1.4)
    pose(t_swp - .05, "shock")
    cree_say(t_swp, "!?", d=.9, size=80)
    glitch(S4 - .2)

    # ---- S4: "It also gave me new hooks and showed me what to fix before I post the next one."
    hooks = ["Stanford just open-sourced a real Jarvis", "Stop paying for AI assistants", "This open-source AI sorts your day", "Nobody tells you this about reels",
             "I tested 5 hooks so you don't have to", "Your first 2 seconds decide it"]
    cells = ""
    for k in range(30):
        kind = k % 3
        if kind == 0:
            cells += f'<div class="wc"><div class="hn">HOOK {k // 3 + 1:02d}</div><div class="wt">{hooks[(k // 3) % len(hooks)]}</div></div>'
        elif kind == 1:
            cells += f'<div class="wc wv"><i class="play"></i><b>{RND.choice(["12.4K", "48K", "9.1K", "103K", "27K"])} views</b></div>'
        else:
            cells += f'<div class="wc wg"><b>+{RND.choice([38, 52, 71, 64, 90])}%</b><span>retention</span></div>'
    put(f'<div class="wall" data-layout-allow-occlusion data-layout-allow-overlap aria-hidden="true" id="wall"><div class="wallp"><div class="wallg" id="wallg">{cells}</div></div></div>')
    show("#wall", S4, t_what)
    js(f'tl.fromTo("#wall", {{opacity: 0, scale: 1.3}}, {{opacity: 1, scale: 1, duration: .6, ease: "expo.out", immediateRender: false}}, {S4:.3f});')
    js(f'tl.fromTo("#wallg", {{y: 0}}, {{y: -700, duration: {t_what - S4:.2f}, ease: "none", immediateRender: false}}, {S4:.3f});')
    js(f'tl.to("#wall", {{opacity: 0, scale: 1.6, filter: "blur(10px)", duration: .35, ease: "power2.in"}}, {t_what - .35:.3f});')
    put('<div class="wallfade" id="wallfade"></div>')
    show("#wallfade", S4, t_what)
    beat("hooks.", t_new, t_what - .35, 260, style="pink", y=680, sub=("New", 160))
    cue(t_new, "hit")
    sparkle(540, 860, t_new + .2, n=12, r=380)
    for k in range(14):                    # confetti
        cf = nid("cf")
        put(f'<i class="conf" id="{cf}" style="left:{540 + RND.uniform(-160, 160):.0f}px;top:900px;background:{["#F515E8", "#F5876C", "#FFC83D", "#54d6a0"][k % 4]}"></i>')
        show(f"#{cf}", t_new + .1, t_new + 1.7)
        js(f'tl.fromTo("#{cf}", {{x: 0, y: 0, rotation: 0}}, {{x: {RND.uniform(-460, 460):.0f}, y: {RND.uniform(-520, 380):.0f}, rotation: {RND.uniform(-600, 600):.0f}, '
           f'opacity: 0, duration: 1.5, ease: "power2.out", immediateRender: false}}, {t_new + .1:.3f});')
    cue(t_new + .1, "sparkle")
    # what to fix: the phone back with the fixes, check chips fly out beside it
    glitch(t_what - .3, .8)
    show("#phone", t_what - .3, S5 - .3)
    js(f'tl.fromTo("#phone", {{transformPerspective: 1400, opacity: 0, x: -600, scale: .9, rotationY: 40, filter: "blur(0px)"}}, {{opacity: 1, x: {70 - PHONE["x"]}, y: -60, scale: .85, '
       f'rotationY: 0, duration: .6, ease: "expo.out", transformPerspective: 1400, immediateRender: false}}, {t_what - .3:.3f});')
    js(f'tl.to("#phone", {{y: 700, rotation: -12, opacity: 0, duration: .4, ease: "power3.in"}}, {S5 - .5:.3f});')
    headline([("What to [fix].", 136, t_what - .05, "pink")], 280, out=S5 - .5)
    for k, txt in enumerate(["Caption at 0:12", "Caption at 0:20", "Save-worthy CTA"]):
        fc = nid("fc")
        put(f'<div class="fixchip" id="{fc}" style="top:{700 + k * 150}px"><b>&#10003;</b>{txt}</div>')
        tt = t_fix + k * .28
        show(f"#{fc}", tt, S5 - .3)
        js(f'tl.fromTo("#{fc}", {{transformPerspective: 1000, opacity: 0, x: 500, rotationY: -50, scale: .8}}, {{opacity: 1, x: 0, rotationY: 0, scale: 1, duration: .5, '
           f'ease: "expo.out", transformPerspective: 1000, immediateRender: false}}, {tt:.3f});')
        js(f'tl.to("#{fc}", {{opacity: 0, x: 400, duration: .3, ease: "power2.in"}}, {S5 - .5 + k * .04:.3f});')
        cue(tt, "tick")
    cree_to(S4 + .1, 880, 1380, .36, d=.4)
    pose(t_new, "cheer")
    cree_hop(t_new, h=70, n=3, period=.4)
    pose(t_new + 1.25, "proud")
    pose(t_fix, "point", flip=True)

    # ---- S5: the free account audit
    NOCAP.append((t_you - .1, t_just - .1))
    liquid(S5 - .6, 540, 2350, S5 - .05)
    flip(S5 - .1, t_just - .15, "radial-gradient(circle at 50% 40%, #fff6fa 0%, #ffd3ea 55%, #ffa6d4 100%)", fade=.2)
    rays(S5, t_just - .2, n=36, cy=760, color="rgba(255,255,255,.95)")
    beat("Free.", t_free, t_audit - .03, 340, style="pink", y=540)
    cue(t_free, "hit")
    sparkle(540, 700, t_free + .15, n=12, r=420)
    beat("audit.", t_audit, t_just - .2, 270, style="ink", y=620, sub=("Account", 150), through=False)
    cue(t_audit, "whoosh")
    glitch(t_just - .2)
    # the steps, one beat each (the reference's Brief / Create / Launch)
    steps = [("@", "Type your handle", t_type - .3), ("&#9201;", "About 20 seconds", t_20 - .3), ("&#9733;", "Your score", t_score - .15), ("&#10003;", "First thing to fix", t_first - .2)]
    ends = [t_20 - .35, t_score - .2, t_first - .25, S6 - .1]
    for k, ((ic, title, tt), te) in enumerate(zip(steps, ends)):
        st = nid("st")
        put(f'<div class="step" id="{st}"><span class="sic">{ic}</span><span class="stx">{chars(title)}</span></div>')
        js(f'tl.fromTo("#{st} .ch", {{opacity: 0, yPercent: 60, filter: "blur(8px)"}}, {{opacity: 1, yPercent: 0, filter: "blur(0px)", duration: .45, ease: "expo.out", '
           f'stagger: .022, immediateRender: false}}, {tt + .08:.3f});')
        show(f"#{st}", tt, te)
        js(f'tl.fromTo("#{st}", {{opacity: 0, y: 60, scale: .9}}, {{opacity: 1, y: 0, scale: 1, duration: .45, ease: "expo.out", immediateRender: false}}, {tt:.3f});')
        js(f'tl.to("#{st}", {{opacity: 0, y: -50, duration: .22, ease: "power2.in"}}, {te - .22:.3f});')
        dots = "".join(f'<i class="{"on" if j == k else ""}"></i>' for j in range(4))
        dd = nid("dt")
        put(f'<div class="dots" id="{dd}">{dots}</div>')
        show(f"#{dd}", tt, te)
    flip(t_score - .15, t_first - .25, "radial-gradient(circle at 50% 45%, #ffffff 0%, #ffe6f2 75%)", fade=.2)
    # 1: the handle types into a glass bar
    hb = glass('<span class="at">@</span><span id="auh"></span><i class="caret" id="auc"></i>', 110, 800, 860, t_type - .2, t_20 - .35, cls="hbar", flt=False)
    handle = "yourhandle"
    for k in range(len(handle) + 1):
        js(f'tl.set("#auh", {{textContent: "{handle[:k]}"}}, {t_hand - .1 + k * .07:.3f});')
    for k in range(0, len(handle), 2):
        cue(t_hand - .1 + k * .07, "type")
    js(f'tl.fromTo("#auc", {{opacity: 1}}, {{opacity: 0, duration: .2, repeat: 7, yoyo: true, ease: "steps(1)", immediateRender: false}}, {t_type - .2:.3f});')
    js(f'tl.to("#{hb}", {{scale: .9, opacity: 0, duration: .22}}, {t_20 - .57:.3f});')
    # 2: the 20-second countdown ring
    cd = nid("cd")
    put(f'<div class="cdown" id="{cd}"><svg viewBox="0 0 200 200"><circle class="cb" cx="100" cy="100" r="86"/><circle class="cf" id="{cd}f" cx="100" cy="100" r="86" '
        f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="0" transform="rotate(-90 100 100)"/></svg><div class="cv"><b id="{cd}n">20</b><small>sec</small></div></div>')
    show(f"#{cd}", t_20 - .3, t_score - .2)
    pop(f"#{cd}", t_20 - .3, frm=.4)
    js(f'tl.fromTo("#{cd}f", {{strokeDashoffset: 0}}, {{strokeDashoffset: 1, duration: {t_score - t_20:.2f}, ease: "none", immediateRender: false}}, {t_20 - .1:.3f});')
    js(f'tl.fromTo("#{cd}n", {{textContent: 20}}, {{textContent: 0, duration: {t_score - t_20:.2f}, ease: "none", snap: {{textContent: 1}}, immediateRender: false}}, {t_20 - .1:.3f});')
    js(f'tl.to("#{cd}", {{scale: 1.4, opacity: 0, filter: "blur(10px)", duration: .22}}, {t_score - .42:.3f});')
    cue(t_20 - .3, "pop")
    # 3: the score rolls like a slot machine
    sl = nid("sl")
    put(f'<div class="score" id="{sl}"><span class="slot">{slot_html(sl, "78")}</span><span class="of">/100</span></div>')
    show(f"#{sl}", t_score - .1, t_first - .25)
    pop(f"#{sl}", t_score - .1, frm=.5)
    slot_roll(sl, "78", t_score - .05, d=.9)
    js(f'tl.fromTo("#{sl}", {{scale: 1}}, {{scale: 1.12, duration: .12, yoyo: true, repeat: 1}}, {t_100 + .1:.3f});')
    sparkle(540, 900, t_100 + .1, n=14, r=420)
    cue(t_score - .05, "rise")
    cue(t_100 + .1, "ding")
    js(f'tl.to("#{sl}", {{scale: .8, opacity: 0, y: -60, duration: .22}}, {t_first - .47:.3f});')
    # 4: the first fix
    ff = glass('<div class="fl">FIRST THING TO FIX</div><div class="fv">Show the payoff in your first 2 seconds</div>', 110, 760, 860, t_first - .1, S6, cls="first", flt=False)
    cue(t_first - .1, "pop")
    js(f'tl.fromTo("#{ff}", {{boxShadow: "0 0 0 0 rgba(245,21,232,0)"}}, {{boxShadow: "0 0 0 16px rgba(245,21,232,.35)", duration: .35, yoyo: true, repeat: 3, '
       f'immediateRender: false}}, {t_fix2:.3f});')
    cree_walk(S5 + .05, t_free + .3, (-220, 1360, .38), (860, 1360, .38), end="wave")
    pose(t_acc - .1, "proud")
    pose(t_type - .3, "phone")
    pose(t_20 - .3, "think")
    cree_wiggle(t_20 - .2, n=4, amp=6, period=.25)
    pose(t_score + .2, "cheer")
    cree_hop(t_100, h=60, n=2)
    pose(t_first - .1, "point", flip=True)
    cree_say(t_first, "!", d=.8)

    # ---- S6: the CTA, "Comment "CREE" and I'll send you the link."
    flip(S6 - .1, DUR, "radial-gradient(circle at 50% 38%, #fff4fa 0%, #ffcfe7 50%, #ff97cc 100%)", fade=.2)
    glitch(S6 - .1, 1.2)
    rays(S6, S7, n=40, cy=620, color="rgba(255,255,255,.95)")
    gout(f"#{ff}", S6 - .1, to="up", d=.3)
    cree_to(S6 + .1, 540, 640, .66, d=.6, ease="back.out(1.4)")
    pose(S6 + .1, "wave", flip=False)
    cree_wiggle(S6 + .7, n=4, amp=9)
    beat("Comment", t_com - .02, S7 - .1, 200, style="ink", y=1020, through=False)
    cue(t_com, "hit")
    cb = nid("cb")
    put(f'<div class="cbig" id="{cb}"><span class="ctx" id="{cb}t"></span><i class="caret big" id="{cb}c"></i>'
        f'<svg class="heart" id="{cb}h" viewBox="0 0 40 36"><path d="M20 34 C 8 25 1 18 1 10 A 9 9 0 0 1 20 6 A 9 9 0 0 1 39 10 C 39 18 32 25 20 34 Z" fill="#ff2d6f"/></svg></div>')
    show(f"#{cb}", t_cree - .1, S7)
    js(f'tl.fromTo("#{cb}", {{transformPerspective: 1200, opacity: 0, y: 160, scale: .7, rotationX: 50}}, {{opacity: 1, y: 0, scale: 1, rotationX: 0, duration: .55, '
       f'ease: "back.out(1.7)", transformPerspective: 1200, immediateRender: false}}, {t_cree - .1:.3f});')
    for k in range(5):
        js(f'tl.set("#{cb}t", {{textContent: "{"CREE"[:k]}"}}, {t_cree + .1 + k * .2:.3f});')
        if k:
            cue(t_cree + .1 + k * .2, "type")
            js(f'tl.fromTo("#{cb}t", {{scale: 1.15}}, {{scale: 1, duration: .18, ease: "power2.out", immediateRender: false}}, {t_cree + .1 + k * .2:.3f});')
    pop(f"#{cb}h", t_cree + 1.0, frm=0, ease="back.out(3)")
    cue(t_cree + 1.0, "pop")
    for k in range(8):
        hh = nid("hh")
        put(f'<svg class="gheart" id="{hh}" viewBox="0 0 40 36" style="left:{760 + RND.uniform(-80, 180):.0f}px;top:1300px"><path d="M20 34 C 8 25 1 18 1 10 A 9 9 0 0 1 20 6 '
            f'A 9 9 0 0 1 39 10 C 39 18 32 25 20 34 Z"/></svg>')
        show(f"#{hh}", t_cree + 1.05 + k * .1, S7)
        js(f'tl.fromTo("#{hh}", {{y: 0, x: 0, scale: .3, rotation: 0}}, {{y: {RND.uniform(-760, -460):.0f}, x: {RND.uniform(-140, 120):.0f}, scale: {RND.uniform(.8, 1.4):.2f}, '
           f'rotation: {RND.uniform(-30, 30):.0f}, opacity: 0, duration: 1.7, ease: "power1.out", immediateRender: false}}, {t_cree + 1.05 + k * .1:.3f});')
    pose(t_cree - .1, "phone")
    pl = nid("pl")
    put(f'<svg class="plane" id="{pl}" viewBox="0 0 100 100"><path d="M 5 45 L 95 8 L 62 92 L 46 60 Z" fill="#fff"/><path d="M 46 60 L 95 8" stroke="#F54BA8" '
        f'stroke-width="5"/></svg>')
    show(f"#{pl}", t_send - .2, S7)
    js(f'tl.fromTo("#{pl}", {{x: 0, y: 0, rotation: -10, scale: .5}}, {{x: 160, y: -1100, rotation: 18, scale: 1.1, duration: .8, ease: "power2.in", immediateRender: false}}, '
       f'{t_send - .2:.3f});')
    cue(t_send - .2, "whoosh")
    glass('<div class="dmh"><img src="assets/img/cree.png" alt=""><b>Creedom</b></div><div class="dmt">Here\'s your link &#128279;</div>', 60, 200, 420,
          t_link - .05, S7, cls="dm", z=22, rot=-3, flt=False)
    cue(t_link - .05, "notify")
    pose(t_send - .25, "point", flip=False)
    pose(t_link - .05, "cheer")
    cree_say(t_link, "♥", d=.8)
    cree_hop(t_link + .1, h=80, n=2)

    # ---- S7: the logo, star and grid floor
    js(f'tl.fromTo("#logo", {{opacity: 0}}, {{opacity: 1, duration: .12, immediateRender: false}}, {S7 - .05:.3f});')
    HIDE.append("#logo")
    glitch(S7 - .05, 1.3)
    js(f'tl.set("#cree", {{opacity: 0}}, {S7 + .1:.3f});')
    js(f'tl.fromTo("#lgm", {{scale: 0, rotation: -40, y: 80}}, {{scale: 1, rotation: 0, y: 0, duration: .6, ease: "back.out(2)", immediateRender: false}}, {S7 + .05:.3f});')
    js(f'tl.fromTo("#lgw", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", duration: .5, ease: "power3.out", immediateRender: false}}, {S7 + .2:.3f});')
    js(f'tl.fromTo("#lgt", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: .35, ease: "power3.out", immediateRender: false}}, {S7 + .35:.3f});')
    js(f'tl.fromTo("#lgs", {{scale: 0, rotation: -90}}, {{scale: 1, rotation: 0, duration: .6, ease: "back.out(2.5)", immediateRender: false}}, {S7 + .45:.3f});')
    js(f'tl.to("#lgs", {{rotation: 30, scale: 1.15, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 1}}, {S7 + 1.05:.3f});')
    js(f'tl.fromTo("#lgf", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "0px 240px", duration: {DUR - S7:.2f}, ease: "none", immediateRender: false}}, {S7:.3f});')
    cue(S7 + .05, "logo")
    sparkle(540, 860, S7 + .3, n=12, r=380, z=41)

    js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -10, duration: .8, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .8)}, immediateRender: false}}, 0);')
    for tb in [6.9, 8.0, 12.95, 15.2, 20.4, 23.4, 26.0, 30.8, 33.0]:
        cree_face(tb, "blink")


def background():
    """The website's ground: warm off-white melting into pink, slow pink glows, drifting glass orbs, and (in the hook,
    like the creedom.ai hero) the creator worries floating past in faint grey."""
    blobs = [(-360, -300, 1000, "#ffb3d9", .45), (520, 1150, 1000, "#ffc2a6", .38), (300, 520, 760, "#ffd1ea", .4), (-300, 1300, 800, "#f9a8d4", .32)]
    html = ""
    for k, (x, y, s, c, o) in enumerate(blobs):
        html += f'<i class="blob" data-layout-allow-overflow id="bl{k}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c};opacity:{o}"></i>'
        js(f'tl.to("#bl{k}", {{x: {RND.uniform(-260, 260):.0f}, y: {RND.uniform(-300, 300):.0f}, duration: {DUR:.1f}, ease: "sine.inOut"}}, 0);')
        js(f'tl.fromTo("#bl{k}", {{scale: 1}}, {{scale: 1.25, duration: {3.4 + k * .8:.1f}, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / (3.4 + k * .8))}, '
           f'immediateRender: false}}, 0);')
    for k in range(8):
        s = RND.choice([46, 64, 90, 120])
        x, y = RND.uniform(-20, FW - 80), RND.uniform(200, FH - 200)
        html += f'<i class="orb" id="ob{k}" style="left:{x:.0f}px;top:{y:.0f}px;width:{s}px;height:{s}px"></i>'
        js(f'tl.to("#ob{k}", {{y: {-RND.uniform(260, 620):.0f}, duration: {DUR:.1f}, ease: "none"}}, 0);')
        js(f'tl.fromTo("#ob{k}", {{x: -24}}, {{x: 24, duration: {RND.uniform(2.6, 4.2):.1f}, ease: "sine.inOut", yoyo: true, repeat: 11, immediateRender: false}}, 0);')
    worries = ["Why did my views drop?", "Algorithm changed again", "Is my content bad?", "No clarity", "What should I post?", "200 views", "Drowning in drafts",
               "Why isn't this working?", "Am I even good at this?", "15 hours, 200 views"]
    spots = [(60, 250), (640, 330), (90, 600), (700, 640), (40, 1060), (720, 1000), (380, 1240), (80, 1380), (660, 1330), (330, 470)]
    # (the drifting worries came out of the hook in v6: the owner's title reference is a clean ground)
    return html


STAR = "M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z"
CSS = f"""
@font-face {{ font-family: "Fraunces"; font-weight: 600; src: url("assets/fonts/fraunces-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Fraunces"; font-weight: 600; font-style: italic; src: url("assets/fonts/fraunces-latin-600-italic.woff2"); }}
@font-face {{ font-family: "Fraunces"; font-weight: 700; src: url("assets/fonts/fraunces-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Manrope"; font-weight: 500; src: url("assets/fonts/manrope-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Manrope"; font-weight: 700; src: url("assets/fonts/manrope-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Manrope"; font-weight: 800; src: url("assets/fonts/manrope-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #f6f6f3; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #f6f6f3; font-family: "Manrope"; color: {INK}; }}
#bgl {{ position: absolute; inset: 0; overflow: hidden; background: linear-gradient(180deg, #f8f7f4 0%, #fbeff5 55%, #ffe1ee 100%); }}
#dots {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(11,11,11,.06) 2px, transparent 2.5px); background-size: 46px 46px; }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(110px); }}
.orb {{ position: absolute; border-radius: 50%; z-index: 1; border: 2px solid rgba(255,255,255,.8);
  background: radial-gradient(circle at 32% 28%, rgba(255,255,255,.95) 0 8%, rgba(255,255,255,.35) 24%, rgba(255,190,225,.2) 62%, rgba(240,50,140,.14) 100%);
  box-shadow: inset -6px -8px 18px rgba(240,50,140,.14), 0 10px 24px rgba(200,40,120,.1); }}
.worry {{ position: absolute; font: 600 34px/1.15 "Manrope"; color: rgba(11,11,11,.2); white-space: nowrap; }}
.flip {{ position: absolute; inset: 0; opacity: 0; }}
#cam, #cam2 {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#cam {{ z-index: 2; }}
.star0 {{ position: absolute; left: 440px; top: 720px; width: 200px; height: 200px; z-index: 5; filter: drop-shadow(0 0 30px rgba(240,50,140,.6)); }}
.rays {{ position: absolute; inset: 0; opacity: 0; z-index: 1; pointer-events: none; }}
.ray {{ position: absolute; width: 0; height: 0; transform-origin: 0 0; }}
.rl {{ position: absolute; left: 0; top: -2px; width: 200px; height: 4px; border-radius: 2px; transform-origin: 0 50%; }}
.gband {{ position: absolute; left: -300px; right: -300px; opacity: 0; z-index: 45; mix-blend-mode: multiply; }}
/* the hook: a picker wheel (owner's reference) */
.drumw {{ position: absolute; left: 0; height: 142px; opacity: 0; z-index: 9; }}
.drum {{ position: absolute; left: 0; right: 0; top: 0; filter: url(#vblur); }}
.di {{ position: absolute; right: 0; height: 142px; white-space: nowrap; text-align: right; font: 700 128px/142px "Inter"; letter-spacing: -.045em; color: #161616;
  transform-origin: 100% 50%; opacity: 0; }}
.dg {{ display: inline-block; padding-right: .08em; }}
.dc {{ position: absolute; right: 0; top: 0; opacity: 0; padding-right: .08em; background: linear-gradient(95deg,#F515E8 0%,#e0187e 45%,#F5876C 100%); -webkit-background-clip: text;
  background-clip: text; color: transparent; }}
.dblock {{ position: absolute; opacity: 0; z-index: 9; font: 600 58px/1.06 "Inter"; letter-spacing: -.03em; color: #161616; }}
.bwm {{ overflow: hidden; padding: 0 .4em .08em 0; margin-right: -.4em; }}
.bwl {{ display: inline-block; transform-origin: 0 60%; }}
/* word beats: the website's serif, letters in reading order */
.beat {{ position: absolute; left: 0; right: 0; opacity: 0; z-index: 9; text-align: center; font-family: "Fraunces"; font-weight: 600; line-height: .98;
  letter-spacing: -.035em; white-space: nowrap; color: {INK}; transform-origin: 50% 50%; }}
.beat .ch {{ display: inline-block; transform-origin: 50% 100%; }}
.beat.grey {{ color: #7a7a73; }}
.beat.pink {{ color: {PINK}; }}
.beat.white {{ color: #fff; }}
.bsub {{ display: inline-block; letter-spacing: -.02em; line-height: 1.1; color: #7a7a73; }}
.beat.white .bsub {{ color: rgba(255,255,255,.6); }}
.bw {{ display: inline-block; }}
.clock {{ position: absolute; left: 0; right: 0; top: 1040px; opacity: 0; z-index: 9; text-align: center; font: 700 90px/1 "Manrope"; letter-spacing: .04em;
  color: rgba(11,11,11,.75); font-variant-numeric: tabular-nums; }}
/* headlines */
.head {{ position: absolute; left: 0; right: 0; opacity: 0; text-align: center; }}
.hl {{ opacity: 0; font-family: "Fraunces"; font-weight: 600; line-height: 1.02; letter-spacing: -.03em; word-spacing: .06em; white-space: nowrap; color: {INK};
  transform-origin: 50% 60%; }}
.hl.grey {{ color: #7a7a73; }}
.hli {{ position: relative; display: inline-block; }}
.wm {{ display: inline-block; overflow: hidden; vertical-align: top; padding: .06em .04em .2em; margin: -.06em -.04em -.2em; }}
.wi {{ display: inline-block; transform-origin: 50% 80%; }}
.wi .ch {{ display: inline-block; }}
.acc.pink {{ color: {PINK}; font-style: italic; }}
.acc.red {{ color: #e11d48; font-style: italic; }}
.acc.green {{ color: #15a05a; font-style: italic; }}
.acc.white {{ color: #fff; }}
.uline {{ position: absolute; left: 4%; right: 4%; bottom: -.16em; width: 92%; height: .2em; overflow: visible; }}
.uline path {{ fill: none; stroke: url(#gr); stroke-width: 9; stroke-linecap: round; }}
/* light glass */
.glass {{ position: absolute; opacity: 0; border-radius: 40px; padding: 28px 32px; overflow: hidden; color: {INK};
  background: linear-gradient(140deg, rgba(255,255,255,.88) 0%, rgba(255,255,255,.58) 55%, rgba(255,236,246,.7) 100%);
  border: 2px solid rgba(255,255,255,.95); backdrop-filter: blur(22px) saturate(1.5); -webkit-backdrop-filter: blur(22px) saturate(1.5);
  box-shadow: 0 30px 70px rgba(170,20,110,.15), 0 6px 18px rgba(170,20,110,.07), inset 0 2px 0 rgba(255,255,255,.95); }}
.shine {{ position: absolute; top: -30%; bottom: -30%; left: -48%; width: 40%; pointer-events: none;
  background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.85) 50%, rgba(255,255,255,0) 100%); transform: skewX(-18deg); }}
.glass.chip {{ left: 0 !important; right: 0; width: max-content !important; margin: 0 auto; padding: 12px 34px 12px 14px; border-radius: 999px; display: flex;
  align-items: center; gap: 16px; font: 500 38px/1 "Manrope"; z-index: 9; }}
.chip img {{ width: 64px; height: 64px; object-fit: contain; }}
.chip b {{ font: 600 40px/1 "Fraunces"; color: {PINK}; font-style: italic; }}
/* retention */
.graph .gh {{ display: flex; justify-content: space-between; align-items: baseline; }}
.gt {{ font: 800 30px/1 "Manrope"; letter-spacing: .12em; color: #7a7a73; }}
.gp {{ font: 600 76px/1 "Fraunces"; color: {PINK}; }}
.avs {{ display: flex; gap: 14px; margin: 18px 0 6px; }}
.av {{ display: grid; place-items: center; width: 64px; height: 64px; border-radius: 50%; opacity: 0; background: linear-gradient(140deg,#F54BA8,#F5876C);
  box-shadow: 0 8px 18px rgba(245,75,168,.3), inset 0 2px 0 rgba(255,255,255,.5); }}
.av svg {{ width: 36px; height: 36px; fill: #fff; }}
.gs {{ width: 100%; height: 284px; overflow: visible; }}
.gl0 {{ stroke: rgba(11,11,11,.1); stroke-width: 4; }}
.gline {{ fill: none; stroke: url(#gr); stroke-width: 12; stroke-linecap: round; stroke-linejoin: round; filter: drop-shadow(0 6px 10px rgba(240,50,140,.35)); }}
.gdot {{ fill: #e11d48; opacity: 0; transform-box: fill-box; transform-origin: center; }}
.gtag {{ position: absolute; left: 300px; top: 176px; opacity: 0; background: {INK}; color: #fff; font: 800 30px/1 "Manrope"; padding: 14px 20px; border-radius: 16px; }}
/* the flopped reel */
.glass.reel {{ padding: 0; }}
.rv {{ position: relative; height: 470px; background: linear-gradient(160deg,#3a2140,#7a3060 60%,#c0567a); display: grid; place-items: center; }}
.play {{ display: block; width: 0; height: 0; border-left: 70px solid rgba(255,255,255,.92); border-top: 44px solid transparent; border-bottom: 44px solid transparent; margin-left: 20px; }}
.up {{ position: absolute; left: 30px; right: 30px; bottom: 30px; padding: 18px 22px; border-radius: 22px; background: rgba(255,255,255,.22); border: 1.5px solid rgba(255,255,255,.5); }}
.upt {{ font: 800 30px/1 "Manrope"; color: #fff; margin-bottom: 12px; }}
.upb {{ height: 12px; border-radius: 6px; background: rgba(255,255,255,.3); overflow: hidden; }}
.upb i {{ display: block; height: 100%; background: linear-gradient(90deg,#F515E8,#F5876C); transform-origin: 0 50%; }}
.rm {{ padding: 22px 28px 26px; display: flex; flex-direction: column; gap: 6px; }}
.rm > b {{ font: 800 36px/1.1 "Manrope"; }}
.views {{ font: 500 32px/1.1 "Manrope"; color: #7a7a73; }}
.views b {{ color: {INK}; }}
.views em {{ display: inline-block; opacity: 0; font-style: normal; color: #e11d48; font-weight: 800; }}
.stampf {{ position: absolute; left: 50px; top: 200px; opacity: 0; font: 800 72px/1.1 "Manrope"; color: #e11d48; border: 10px solid #e11d48; border-radius: 18px;
  padding: 0 22px; background: rgba(255,255,255,.92); }}
/* the phone */
#phone {{ position: absolute; opacity: 0; z-index: 6; }}
#phonei {{ position: absolute; inset: 0; border-radius: 72px; background: #160b18; padding: 14px;
  box-shadow: 0 50px 110px rgba(120,10,80,.3), 0 0 0 4px #3a2a3c inset, 0 0 0 2px rgba(255,255,255,.4); }}
#phone .scr {{ position: relative; width: 100%; height: 100%; border-radius: 58px; overflow: hidden; background: #fdfdfd; }}
.pv {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; }}
.isl {{ position: absolute; left: 50%; top: 26px; width: 120px; height: 35px; margin-left: -60px; border-radius: 18px; background: #050305; }}
.scan {{ position: absolute; left: 0; right: 0; top: 0; height: 11%; opacity: 0; mix-blend-mode: multiply;
  background: linear-gradient(180deg, rgba(245,21,232,0), rgba(245,21,232,.22) 70%, rgba(245,21,232,.6) 100%); }}
.refl {{ position: absolute; top: -10%; bottom: -10%; left: 0; width: 45%; pointer-events: none;
  background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0)); transform: skewX(-16deg); }}
.tkw {{ position: absolute; left: -310px; width: 1700px; height: 96px; overflow: hidden; opacity: 0; z-index: 4; display: flex; align-items: center; }}
.tkw.mag {{ background: linear-gradient(90deg,#F515E8,#F54BA8,#F5876C); box-shadow: 0 20px 50px rgba(245,21,232,.3); }}
.tkw.ink {{ background: {INK}; box-shadow: 0 20px 50px rgba(0,0,0,.25); }}
.tki {{ white-space: nowrap; font: 800 46px/96px "Manrope"; letter-spacing: .08em; color: #fff; }}
.tchip {{ position: absolute; opacity: 0; z-index: 10; padding: 14px 24px; border-radius: 18px; font: 800 40px/1 "Manrope"; color: {INK};
  background: rgba(255,255,255,.85); border: 2px solid #fff; box-shadow: 0 10px 26px rgba(200,40,120,.2); }}
.tchip:nth-of-type(odd) {{ background: {INK}; color: #fff; border-color: {INK}; }}
/* findings */
#pill {{ position: absolute; left: 130px; width: 820px; top: 500px; height: 150px; border-radius: 999px; overflow: hidden; opacity: 0; z-index: 9;
  background: #15a05a; box-shadow: 0 20px 50px rgba(21,160,90,.35); }}
.pst {{ position: absolute; left: 0; right: 0; top: 0; }}
.pw {{ height: 150px; display: grid; place-items: center; font: 800 62px/1 "Manrope"; color: #fff; letter-spacing: -.01em; white-space: nowrap; }}
.glass.hookbig {{ display: flex; align-items: center; gap: 40px; }}
.hring {{ position: relative; width: 260px; height: 260px; flex: 0 0 auto; }}
.hring svg {{ width: 100%; height: 100%; overflow: visible; }}
.hb {{ fill: none; stroke: rgba(21,160,90,.14); stroke-width: 18; }}
.hf {{ fill: none; stroke: #15a05a; stroke-width: 18; stroke-linecap: round; }}
.hv {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 78px; }}
.hv b {{ font: 600 104px/1 "Fraunces"; }}
.hv small {{ font: 700 30px/1 "Manrope"; color: #7a7a73; }}
.hkl {{ font: 800 28px/1 "Manrope"; letter-spacing: .1em; color: #7a7a73; }}
.hkv {{ font: 600 64px/1.08 "Fraunces"; margin-top: 10px; }}
.et {{ font: 800 28px/1 "Manrope"; letter-spacing: .12em; color: #7a7a73; margin-bottom: 16px; }}
.ebars {{ position: relative; display: flex; align-items: flex-end; gap: 12px; height: 250px; }}
.eb {{ display: block; flex: 1; border-radius: 10px; background: linear-gradient(180deg,#F515E8,#F5876C); }}
.emid {{ position: absolute; left: 214px; width: 308px; top: -12px; bottom: -12px; border: 4px dashed rgba(11,11,11,.55); border-radius: 22px; opacity: 0; }}
.edrop {{ opacity: 0; margin-top: 14px; font: 800 36px/1 "Manrope"; color: #e11d48; text-align: center; }}
.mini {{ position: absolute; opacity: 0; width: 210px; height: 330px; border-radius: 28px; background: linear-gradient(160deg,#5a1d63,#c0367e); display: grid; place-items: center;
  box-shadow: 0 18px 40px rgba(80,0,50,.3); border: 2px solid rgba(255,255,255,.6); }}
.mini .play {{ border-left-width: 44px; border-top-width: 28px; border-bottom-width: 28px; margin-left: 12px; }}
.vcount {{ position: absolute; left: 0; right: 0; top: 1110px; opacity: 0; z-index: 12; text-align: center; font: 600 84px/1 "Fraunces"; color: #e11d48; font-style: italic; }}
.wall {{ position: absolute; left: -420px; top: 120px; width: 1920px; height: 1900px; opacity: 0; z-index: 3; }}
.wallp {{ position: absolute; inset: 0; transform: perspective(1500px) rotateX(46deg) rotateZ(-20deg); }}
.wallg {{ display: grid; grid-template-columns: repeat(5, 340px); gap: 26px; }}
.wc {{ height: 230px; border-radius: 32px; padding: 24px; background: rgba(255,255,255,.82); border: 2px solid #fff; box-shadow: 0 16px 40px rgba(170,20,110,.12); }}
.wc .hn {{ font: 800 22px/1 "Manrope"; letter-spacing: .12em; color: {PINK}; margin-bottom: 12px; }}
.wt {{ font: 600 32px/1.15 "Fraunces"; }}
.wv {{ display: grid; place-items: center; gap: 10px; background: linear-gradient(160deg,#5a1d63,#c0367e); color: #fff; }}
.wv b {{ font: 800 32px/1 "Manrope"; }}
.wg {{ display: flex; flex-direction: column; justify-content: center; }}
.wg b {{ font: 600 84px/1 "Fraunces"; color: #15a05a; }}
.wg span {{ font: 700 28px/1 "Manrope"; color: #7a7a73; }}
.wallfade {{ position: absolute; inset: 0; z-index: 5; opacity: 0; background: radial-gradient(ellipse at 50% 44%, rgba(248,247,244,.95) 0%, rgba(248,247,244,.7) 32%, rgba(248,247,244,0) 68%); }}
.fixchip {{ position: absolute; left: 520px; width: 470px; opacity: 0; z-index: 9; display: flex; gap: 18px; align-items: center; padding: 26px 28px; border-radius: 30px;
  font: 800 40px/1.1 "Manrope"; background: rgba(255,255,255,.88); border: 2px solid #fff; box-shadow: 0 20px 50px rgba(170,20,110,.15); }}
.fixchip b {{ display: grid; place-items: center; width: 58px; height: 58px; border-radius: 50%; background: #15a05a; color: #fff; font-size: 32px; flex: 0 0 auto; }}
.conf {{ position: absolute; opacity: 0; width: 22px; height: 34px; border-radius: 6px; z-index: 21; }}
#lq {{ position: absolute; left: 0; top: 0; width: 2800px; height: 2800px; z-index: 30; opacity: 0; border-radius: 50%;
  background: radial-gradient(circle at 40% 35%, #ffe3f1 0%, #ffb8dc 40%, #ff8cc8 70%, #F5876C 100%); }}
/* the audit steps */
.step {{ position: absolute; left: 0; right: 0; top: 420px; display: flex; justify-content: center; align-items: center; gap: 26px; opacity: 0; z-index: 9; }}
.sic {{ display: grid; place-items: center; width: 112px; height: 112px; border-radius: 32px; background: {INK}; color: #fff; font: 800 58px/1 "Manrope";
  box-shadow: 0 16px 36px rgba(0,0,0,.2); }}
.stx {{ font: 600 70px/1 "Fraunces"; letter-spacing: -.02em; }}
.dots {{ position: absolute; left: 0; right: 0; top: 1200px; display: flex; justify-content: center; gap: 14px; opacity: 0; z-index: 9; }}
.dots i {{ display: block; width: 70px; height: 8px; border-radius: 4px; background: rgba(11,11,11,.14); }}
.dots i.on {{ background: linear-gradient(90deg,#F515E8,#F5876C); }}
.glass.hbar {{ display: flex; align-items: center; height: 160px; padding: 0 44px; border-radius: 44px; font: 700 74px/1 "Manrope"; }}
.at {{ color: {PINK}; margin-right: 8px; }}
.caret {{ display: inline-block; width: 6px; height: 76px; background: {PINK}; margin-left: 6px; }}
.cdown {{ position: absolute; left: 330px; top: 620px; width: 420px; height: 420px; opacity: 0; z-index: 9; }}
.cdown svg {{ width: 100%; height: 100%; overflow: visible; }}
.cb {{ fill: none; stroke: rgba(240,50,140,.14); stroke-width: 16; }}
.cf {{ fill: none; stroke: url(#gr); stroke-width: 16; stroke-linecap: round; }}
.cv {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 128px; }}
.cv b {{ font: 600 160px/1 "Fraunces"; font-variant-numeric: tabular-nums; }}
.cv small {{ font: 700 42px/1 "Manrope"; color: #7a7a73; margin-left: 6px; }}
.score {{ position: absolute; left: 0; right: 0; top: 660px; opacity: 0; z-index: 9; text-align: center; font: 600 330px/1 "Fraunces"; color: {INK}; }}
.slot {{ display: inline-flex; vertical-align: bottom; }}
.sw {{ display: inline-block; height: 1em; overflow: hidden; line-height: 1; }}
.sc {{ display: flex; flex-direction: column; }}
.sc b {{ display: block; height: 1em; line-height: 1em; font-weight: 600; }}
.of {{ font: 700 90px/1 "Manrope"; color: #7a7a73; margin-left: 12px; }}
.glass.first {{ padding: 38px 42px; z-index: 9; }}
.fl {{ font: 800 30px/1 "Manrope"; letter-spacing: .12em; color: {PINK}; margin-bottom: 16px; }}
.fv {{ font: 600 64px/1.1 "Fraunces"; }}
/* the CTA: a black pill like the website's button */
.cbig {{ position: absolute; left: 160px; width: 760px; top: 1230px; height: 190px; border-radius: 999px; opacity: 0; z-index: 22; display: flex; align-items: center;
  justify-content: center; gap: 8px; background: {INK}; box-shadow: 0 30px 70px rgba(60,0,40,.35); }}
.ctx {{ font: 800 124px/1 "Manrope"; color: #fff; letter-spacing: .08em; transform-origin: 50% 60%; display: inline-block; }}
.caret.big {{ height: 116px; width: 9px; background: #ff7ad9; }}
.heart {{ position: absolute; right: -70px; top: -40px; width: 110px; height: 100px; opacity: 0; }}
.gheart {{ position: absolute; width: 70px; height: 64px; opacity: 0; z-index: 21; overflow: visible; }}
.gheart path {{ fill: rgba(255,255,255,.6); stroke: #fff; stroke-width: 2; }}
.plane {{ position: absolute; left: 990px; top: 1180px; width: 120px; height: 120px; opacity: 0; z-index: 23; filter: drop-shadow(0 10px 18px rgba(80,0,60,.3)); }}
.glass.dm {{ padding: 22px 26px; }}
.dmh {{ display: flex; align-items: center; gap: 12px; font: 600 36px/1 "Fraunces"; }}
.dmh img {{ width: 56px; height: 56px; object-fit: contain; }}
.dmt {{ margin-top: 12px; font: 700 36px/1.2 "Manrope"; }}
/* captions */
.cap {{ position: absolute; left: 60px; right: 60px; top: 1510px; opacity: 0; text-align: center; z-index: 25; font: 800 52px/1.25 "Manrope"; color: {INK}; }}
.cw {{ display: inline-block; padding: 2px 14px 6px; border-radius: 16px; }}
.cw.on {{ background: {GRAD}; color: #fff; box-shadow: 0 10px 22px rgba(245,21,232,.3); }}
/* logo */
#logo {{ position: absolute; inset: 0; z-index: 40; opacity: 0; overflow: hidden; background: radial-gradient(circle at 50% 42%, #ffffff 0%, #fbf3f6 55%, #ffe1ee 100%); }}
#lgf {{ position: absolute; left: -50%; right: -50%; bottom: -12%; height: 52%; transform: perspective(600px) rotateX(62deg); transform-origin: 50% 0;
  background-image: linear-gradient(rgba(240,50,140,.32) 2px, transparent 2px), linear-gradient(90deg, rgba(240,50,140,.32) 2px, transparent 2px); background-size: 120px 120px;
  -webkit-mask-image: linear-gradient(transparent, #000 45%); mask-image: linear-gradient(transparent, #000 45%); }}
#lgm {{ position: absolute; left: 100px; top: 715px; width: 250px; height: 250px; object-fit: contain; filter: drop-shadow(0 20px 30px rgba(200,40,120,.25)); }}
#lgw {{ position: absolute; left: 360px; top: 760px; font: 700 168px/1 "Fraunces"; letter-spacing: -.04em; color: {INK}; padding-bottom: 20px; }}
#lgs {{ position: absolute; left: 930px; top: 690px; width: 100px; height: 100px; }}
#lgt {{ position: absolute; left: 0; right: 0; top: 1030px; text-align: center; font: 500 46px/1.2 "Manrope"; color: #7a7a73; opacity: 0; }}
.spk {{ position: absolute; width: 44px; height: 44px; opacity: 0; }}
/* Cree */
#cree {{ position: absolute; left: 0; top: 0; width: 820px; height: 820px; z-index: 20; opacity: 0; transform-origin: 410px 500px; filter: drop-shadow(0 24px 30px rgba(200,40,120,.22)); }}
#creeb {{ position: absolute; inset: 0; transform-origin: 50% 97.5%; }}
#creef {{ position: absolute; inset: 0; transform-origin: 50% 60%; }}
#creep {{ position: absolute; inset: 0; transform-origin: 50% 97.5%; }}
.cpose {{ position: absolute; inset: 0; opacity: 0; }}
#cp-shock {{ opacity: 1; }}
.cpose img, .clids, .csw {{ position: absolute; inset: 0; width: 820px; height: 820px; }}
.csw {{ overflow: visible; }}
.lidg {{ opacity: 0; }}
.sweat {{ opacity: 0; transform-box: fill-box; transform-origin: 50% 0; }}
#bub {{ position: absolute; left: 560px; top: 20px; width: 200px; height: 170px; opacity: 0; background: #fff; border-radius: 50% 50% 50% 12px;
  box-shadow: 0 14px 30px rgba(150,20,100,.2); display: grid; place-items: center; transform-origin: 0 100%; }}
#bubt {{ font: 600 96px/1 "Fraunces"; color: #c40db8; }}
.prop {{ position: absolute; opacity: 0; transform-origin: 50% 80%; }}
.prop svg {{ width: 100%; height: 100%; }}
"""


def main():
    bg = background()
    scenes()
    caption_track()
    cree = cree_html().replace('<div id="bub">', "".join(put_cree) + '<div id="bub">')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Creedom explainer 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><defs><filter id="vblur" x="-10%" y="-60%" width="120%" height="220%"><feGaussianBlur id="vbg" stdDeviation="0 0"/></filter><linearGradient id="gr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F515E8"/>
      <stop offset=".5" stop-color="#F54BA8"/><stop offset="1" stop-color="#F5876C"/></linearGradient></defs></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="bgl">{bg}{"".join(FLIPS)}<div id="dots"></div></div>
      <div id="cam"><div id="cam2">
      {"".join(EL)}
      {cree}
      </div></div>
      {"".join(CAPS)}
      <div id="lq"></div>
      <div id="logo"><div id="lgf"></div><img id="lgm" src="assets/img/cree.png" alt="Cree"><div id="lgw">creedom</div>
        <svg id="lgs" viewBox="-50 -50 100 100"><path d="{STAR}" fill="url(#gr)"/></svg><div id="lgt">creedom.ai</div></div>
      {"".join(GBANDS)}
      <audio id="mix" src="assets/audio/bed.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(list(dict.fromkeys(HIDE)))}, {{opacity: 0}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    ev = sorted(({"t": t, "type": k} for t, k in CUES if 0 <= t < DUR), key=lambda e: e["t"])
    json.dump(ev, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(ev)} sound moments, {DUR} s")


if __name__ == "__main__":
    main()
