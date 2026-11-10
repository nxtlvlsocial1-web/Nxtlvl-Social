"""Creedom explainer reel, 9:16 (1080x1920). Writes index.html and plan/sfx_events.json.

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
FW, FH, FPS = 1080, 1920, 30
VO = json.load(open(os.path.join(ROOT, "plan", "vo_tight.json")))
VDUR = 35.43
DUR = 37.5
A, HIDE, EL, CUES, CAPS = [], [], [], [], []
NID = [0]
RND = random.Random(9)
GRAD = "linear-gradient(90deg,#F515E8 0%,#F54BA8 50%,#F5876C 100%)"


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
    """Headline in the top band. lines = [(text, size, t, accent)] with accent words in [brackets]; accent is the
    accent style (grad / red / green / white). Each word rises out of its own mask, one after another; accent words
    land with a light sweep and a punch, and the gradient ones get a drawn underline. out = when the words leave
    (how: up = back down into the mask upwards, left = slide off to the left)."""
    i = nid("h")
    rows = []
    for k, (text, size, t, acc) in enumerate(lines):
        ws = []
        for n, w in enumerate(text.split(" ")):
            a = w.startswith("[")
            w = w.strip("[]")
            ws.append(f'<span class="wm"><span class="wi{" acc " + acc if a else ""}" id="{i}l{k}w{n}">{w}</span></span>')
        under = ('<svg class="uline" viewBox="0 0 600 40" preserveAspectRatio="none"><path id="{0}u{1}" d="M 8 30 C 160 6 430 6 592 20" pathLength="1" '
                 'stroke-dasharray="1" stroke-dashoffset="1"/></svg>').format(i, k) if acc == "grad" and "[" in text and k == len(lines) - 1 else ""
        rows.append(f'<div class="hl" id="{i}l{k}" style="font-size:{size}px"><span class="hli">{" ".join(ws)}{under}</span></div>')
    put(f'<div class="head" id="{i}" style="top:{y}px;z-index:{z}">{"".join(rows)}</div>')
    t_end = out + .6 if out else None
    show(f"#{i}", lines[0][2], t_end)
    for k, (text, size, t, acc) in enumerate(lines):
        show(f"#{i}l{k}", t)
        js(f'tl.fromTo("#{i}l{k} .wi", {{yPercent: 118, rotation: 8}}, {{yPercent: 0, rotation: 0, duration: .7, ease: "expo.out", stagger: .085, '
           f'immediateRender: false}}, {t:.3f});')
        js(f'tl.fromTo("#{i}l{k}", {{scale: 1.08}}, {{scale: 1, duration: 1.1, ease: "power3.out", immediateRender: false}}, {t:.3f});')
        if "[" in text:
            ta = t + .085 * [n for n, w in enumerate(text.split(" ")) if w.startswith("[")][0] + .28
            js(f'tl.fromTo("#{i}l{k} .acc", {{backgroundPosition: "100% 0%"}}, {{backgroundPosition: "0% 0%", duration: 1.1, ease: "power2.out", '
               f'immediateRender: false}}, {ta:.3f});')
            js(f'tl.fromTo("#{i}l{k} .acc", {{scale: 1}}, {{keyframes: [{{scale: 1.12, duration: .12, ease: "power2.out"}}, {{scale: 1, duration: .5, '
               f'ease: "elastic.out(1, .45)"}}], immediateRender: false}}, {ta:.3f});')
            if acc == "grad" and k == len(lines) - 1:
                js(f'tl.fromTo("#{i}u{k}", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .5, ease: "power2.out", immediateRender: false}}, {ta + .1:.3f});')
    if out:
        if how == "left":
            js(f'tl.to("#{i} .wi", {{x: -1300, rotation: -10, filter: "blur(12px)", duration: .5, ease: "power3.in", stagger: .05}}, {out:.3f});')
        else:
            js(f'tl.to("#{i} .wi", {{yPercent: -150, y: 0, rotation: -6, duration: .4, ease: "power3.in", stagger: .03}}, {out:.3f});')
            if lines[-1][3] == "grad" and "[" in lines[-1][0]:
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
    chunks = [c for c in chunks if VO[c[0]]["s"] < W("Comment") - .9]
    for n, c in enumerate(chunks):
        t0 = VO[c[0]]["s"] - .05
        t1 = VO[chunks[n + 1][0]]["s"] - .05 if n + 1 < len(chunks) else VDUR + .2
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


# ------------------------------------------------------------------------------------------------ the phone
PHX, PHY, PHW = 350, 630, 370
PHH = round(PHW * 1434 / 660)


def phone(t, t1, clips):
    """The app on a phone with a clean island (the recording's own status bar is painted out). It swoops in tilted,
    then sways gently in 3D; a light reflection sweeps the glass on every new clip."""
    vids = "".join(f'<video id="pv{k}" class="pv" src="assets/video/{f}" data-start="{s:.3f}" data-duration="{d:.3f}" data-track-index="{2 + k}" muted playsinline></video>'
                   for k, (f, s, d) in enumerate(clips))
    put(f'<div id="phone" style="left:{PHX}px;top:{PHY}px;width:{PHW}px;height:{PHH}px"><div id="phonei"><div class="scr">{vids}'
        f'<i class="scan" data-layout-allow-overflow id="scan"></i><i class="refl" data-layout-allow-overflow id="refl"></i></div><i class="isl"></i></div></div>')
    show("#phone", t, t1)
    js(f'tl.fromTo("#phone", {{transformPerspective: 1400, y: 900, rotationX: 38, rotationY: -18, rotation: -8, scale: .8}}, {{y: 0, rotationX: 0, rotationY: 0, rotation: 0, scale: 1, '
       f'duration: .9, ease: "expo.out", transformPerspective: 1400, immediateRender: false}}, {t:.3f});')
    reps = int((t1 - t - 1) / 2.4)
    reps -= 1 - reps % 2
    js(f'tl.fromTo("#phonei", {{transformPerspective: 1400, rotationY: -6, y: 0}}, {{rotationY: 6, y: -14, duration: 2.4, ease: "sine.inOut", yoyo: true, repeat: {reps}, '
       f'transformPerspective: 1400, immediateRender: false}}, {t + .9:.3f});')
    for k, (f, s, d) in enumerate(clips):
        show(f"#pv{k}", s, s + d)
        js(f'tl.fromTo("#pv{k}", {{scale: 1.08, filter: "blur(8px)"}}, {{scale: 1, filter: "blur(0px)", duration: .35, ease: "power3.out", immediateRender: false}}, {s:.3f});')
        js(f'tl.fromTo("#refl", {{xPercent: -160}}, {{xPercent: 260, duration: .9, ease: "power2.inOut", immediateRender: false}}, {s + .05:.3f});')


# ------------------------------------------------------------------------------------------------ the scenes
def scenes():
    t_up, t_flop, t_cr, t_wat, t_sec2 = W("uploaded"), W("flopped"), W("Creedom's"), W("watched"), W("second", 2)
    t_it, t_hook, t_ene, t_drop, t_swp = W("It", 3), W("hook"), W("energy"), W("dropped"), W("swiped")
    t_also, t_new, t_fix = W("also"), W("new"), W("fix")
    t_you, t_free, t_audit, t_acc, t_type, t_hand = W("You"), W("free"), W("audit"), W("account"), W("type"), W("handle")
    t_20, t_score, t_100, t_first, t_fix2 = W("20"), W("score"), W("100"), W("first"), W("fix", 2)
    t_com, t_cree, t_send, t_link = W("Comment"), W("CREE"), W("send"), W("link")
    S2, S3, S4, S5, S6, S7 = t_up - .25, t_it - .2, t_also - .3, t_you - .25, t_com - .9, VDUR + .05
    for k, (a, b) in enumerate([(0, S2), (S2, t_cr), (t_cr, S3), (S3, S4), (S4, S5), (S5, S6), (S6, S7)]):
        push(a, b, *((1, 1.04) if k % 2 == 0 else (1.04, 1)))

    # ---- S1 the hook: "This AI told me the exact second people stopped watching my reel."
    headline([("THIS AI TOLD ME", 70, W("This"), None), ("THE EXACT", 124, W("the"), None), ("[SECOND]", 188, W("second"), "grad")], 236, out=S2 - .4)
    cue(W("second"), "hit")
    sparkle(540, 520, W("second") + .35, n=10, r=300)
    # retention: a glass card that is already on screen at 0 s; the line runs, then falls off a cliff where people left
    av = "".join(f'<i class="av" id="av{k}"><svg viewBox="0 0 40 40"><circle cx="20" cy="14" r="8"/><path d="M 5 38 C 6 26 34 26 35 38 Z"/></svg></i>' for k in range(7))
    g = glass(f'<div class="gh"><span class="gt">Retention</span><span class="gp" id="gp">100%</span></div><div class="avs">{av}</div>'
              f'<svg viewBox="0 0 700 240" class="gs"><path class="gl0" d="M 0 230 H 700"/>'
              f'<path class="gline" id="gl" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M 0 24 C 80 28 160 34 240 44 C 300 50 330 54 360 58 '
              f'C 380 62 395 130 410 190 C 430 206 520 212 700 216"/><circle class="gdot" id="gd" cx="372" cy="66" r="16"/></svg>'
              f'<div class="gtag" id="gtag">0:07 &middot; they left here</div>', 110, 690, 860, 0, S2 - .3, cls="graph", flt=False, enter="settle")
    js(f'tl.fromTo("#gl", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 1.5, ease: "power1.inOut", immediateRender: false}}, 1.7);')
    js('tl.fromTo("#gp", {textContent: 100}, {textContent: 38, duration: 1.5, ease: "power2.in", snap: {textContent: 1}, '
       'modifiers: {textContent: (v) => Math.round(v) + "%"}, immediateRender: false}, 1.7);')
    js('tl.fromTo(".av", {opacity: 0, y: 30, scale: .5}, {opacity: 1, y: 0, scale: 1, duration: .5, ease: "back.out(2)", stagger: .07, immediateRender: false}, .5);')
    pop("#gd", W("stopped") - .05, frm=0)
    js(f'tl.to("#gd", {{scale: 1.6, opacity: .5, duration: .3, yoyo: true, repeat: 3}}, {W("stopped") + .3:.3f});')
    pop("#gtag", W("stopped") + .05, frm=.4)
    cue(W("stopped") - .05, "alert")
    # the viewers who leave: five of the seven turn red and drop out of the row
    js(f'tl.to(["#av2", "#av3", "#av4", "#av5", "#av6"], {{keyframes: [{{background: "rgba(255,45,85,.9)", duration: .12}}, {{x: -60, y: 120, rotation: -40, '
       f'opacity: 0, duration: .55, ease: "power2.in"}}], stagger: .08}}, {W("watching"):.3f});')
    cue(W("watching"), "swish")
    gout(f"#{g}", S2 - .4, to="down")
    whip(S2 - .15)
    # Cree: pops up waving, thinks, points at the graph, then is shocked where people left
    cree_set(0, 880, 1600, .40)
    js(f'tl.fromTo("#cree", {{opacity: 0, y: 1500}}, {{opacity: 1, y: {1320 - PCY}, duration: .6, ease: "back.out(1.6)", immediateRender: false}}, {W("AI") - .1:.3f});')
    cue(W("AI") - .1, "pop")
    cree_wiggle(W("AI") + .4, n=3, amp=8)
    pose(1.55, "think")
    pose(2.6, "point", flip=True)
    pose(W("stopped") - .1, "shock", flip=False)
    cree_face(W("stopped"), "sweat", d=1.2)
    cree_say(W("stopped") + .05, "!", d=1.0)
    cree_hop(W("stopped") - .1, h=40)

    # ---- S2a: "I uploaded a reel that flopped"
    hf = headline([("I UPLOADED A REEL", 66, t_up, None), ("THAT [FLOPPED.]", 96, t_flop, "red")], 260, out=t_cr - .4)
    js(f'tl.fromTo("#{hf}l1", {{x: 0}}, {{keyframes: [{{x: -14, duration: .05}}, {{x: 14, duration: .05}}, {{x: -10, duration: .05}}, {{x: 8, duration: .05}}, '
       f'{{x: 0, duration: .05}}], immediateRender: false}}, {t_flop + .4:.3f});')
    r = glass(f'<div class="rv" id="rv"><i class="play"></i><div class="up" id="up"><div class="upt">Uploading <b id="upn">0%</b></div>'
              f'<div class="upb"><i id="upf"></i></div></div></div><div class="rm"><b>my_reel.mp4</b><span class="views"><b id="vn">0</b> views '
              f'<em id="vd">&darr; 84%</em></span></div><div class="stampf" id="stamp">FLOPPED</div>', 170, 650, 440, S2 + .05, t_cr - .1, cls="reel")
    cue(S2 + .05, "whoosh")
    js(f'tl.fromTo("#upf", {{scaleX: 0}}, {{scaleX: 1, duration: .7, ease: "power2.inOut", immediateRender: false}}, {t_up + .1:.3f});')
    js(f'tl.fromTo("#upn", {{textContent: 0}}, {{textContent: 100, duration: .7, ease: "power2.inOut", snap: {{textContent: 1}}, modifiers: {{textContent: (v) => Math.round(v) + "%"}}, '
       f'immediateRender: false}}, {t_up + .1:.3f});')
    js(f'tl.to("#up", {{opacity: 0, y: 30, duration: .25}}, {t_up + .85:.3f});')
    js(f'tl.fromTo("#vn", {{textContent: 0}}, {{textContent: 312, duration: .6, ease: "power2.out", snap: {{textContent: 1}}, immediateRender: false}}, {t_up + .9:.3f});')
    pop("#vd", t_flop, frm=.4)
    js(f'tl.to("#{r}", {{rotationX: 18, y: 40, duration: .45, ease: "bounce.out", transformPerspective: 1200}}, {t_flop:.3f});')
    js(f'tl.to("#rv", {{filter: "grayscale(.85) brightness(.8)", duration: .4}}, {t_flop:.3f});')
    pop("#stamp", t_flop + .05, frm=2.4, d=.3, ease="back.out(2)", rot=-12)
    cue(t_flop + .05, "stamp")
    # the flop gets sucked into the analyzer's phone
    js(f'tl.to("#{r}", {{x: 300, y: 260, scale: .2, rotation: 20, opacity: 0, duration: .45, ease: "power3.in"}}, {t_cr - .55:.3f});')
    cree_walk(S2 + .05, t_flop - .1, (880, 1320, .40), (840, 1310, .42), end="sad")
    cree_say(t_flop + .1, "...", d=.9, size=70)

    # ---- S2b: "into Creedom's Reel Analyzer, and it watched it second by second."
    ch = glass('<img src="assets/img/cree.png" alt=""><span>Creedom &middot; <b>Reel Analyzer</b></span>', 0, 250, 0, t_cr, S3 - .1, cls="chip", flt=False)
    cue(t_cr, "pop")
    phone(t_cr - .2, S5 - .1, [("c1_pick.mp4", t_cr - .2, 2.0), ("c2_steps.mp4", t_cr + 1.8, 2.0),
                               ("c3_score.mp4", S3 - .2, 6.6), ("c4_fixes.mp4", S4 - .2, 4.6)])
    cue(t_cr - .2, "whoosh_big")
    pose(t_cr, "present")
    cree_to(t_cr - .1, 890, 1310, .42, d=.5)
    # second by second: the scan bar sweeps the screen, a glass filmstrip of seconds runs under the headline
    show("#scan", t_wat, S3)
    js(f'tl.fromTo("#scan", {{yPercent: -100}}, {{yPercent: 900, duration: .65, ease: "none", repeat: 2, immediateRender: false}}, {t_wat:.3f});')
    fs = nid("fs")
    cells = "".join(f'<span class="fc">0:{k:02d}</span>' for k in range(0, 31))
    put(f'<div class="film" id="{fs}"><div class="fin" id="{fs}i">{cells}</div></div>')
    show(f"#{fs}", t_wat - .1, S3 - .1)
    fly(f"#{fs}", t_wat - .1, y=40)
    js(f'tl.fromTo("#{fs}i", {{x: 0}}, {{x: -1900, duration: {S3 - t_wat + .4:.2f}, ease: "none", immediateRender: false}}, {t_wat - .1:.3f});')
    js(f'tl.to("#{fs}", {{opacity: 0, y: -30, duration: .25}}, {S3 - .35:.3f});')
    js(f'tl.to("#{ch}", {{opacity: 0, y: -40, filter: "blur(8px)", duration: .3}}, {S3 - .4:.3f});')
    headline([("[SECOND] BY [SECOND]", 78, t_sec2, "grad")], 344, out=S3 - .4)
    cue(t_sec2, "tick")
    cree_to(t_wat - .3, 900, 1290, .42, d=.4)
    pose(t_wat, "mag")
    js(f'tl.fromTo("#creef", {{rotation: 0}}, {{rotation: -6, duration: .45, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, {t_wat + .3:.3f});')
    cue(t_wat, "pop")

    # ---- S3: "It told me my hook worked, but my energy dropped in the middle, and that's exactly where people swiped away."
    # the phone takes the left column; the findings come in on the right
    js(f'tl.to("#phone", {{x: {60 - PHX}, duration: .7, ease: "expo.inOut"}}, {S3 - .25:.3f});')
    headline([("HOOK [WORKED]", 108, t_hook, "green")], 330, out=t_ene - .45)
    he = headline([("ENERGY [DROPPED]", 86, t_ene - .1, "red")], 340, out=t_swp - .45)
    js(f'tl.to("#{he}l0w1", {{y: 22, rotation: 4, duration: .6, ease: "bounce.out"}}, {t_drop + .1:.3f});')
    headline([("SWIPED [AWAY]", 108, t_swp - .1, "red")], 330, out=S4 - .45, how="left")
    hk = glass('<div class="hkr"><i class="ok"><svg viewBox="0 0 40 40"><path d="M 9 21 L 17 29 L 32 12" fill="none" stroke="#fff" stroke-width="6" '
               'stroke-linecap="round" stroke-linejoin="round"/></svg></i><div><div class="hkl">HOOK &middot; 0:00-0:03</div><div class="hkv">Strong start</div></div>'
               '<b class="hks" id="hks">92</b></div><div class="hkbar"><i id="hkf"></i></div>', 470, 640, 560, t_hook, S4 - .3, cls="hook", enter="right")
    js(f'tl.fromTo("#hkf", {{scaleX: 0}}, {{scaleX: .92, duration: .8, ease: "power3.out", immediateRender: false}}, {t_hook + .3:.3f});')
    js(f'tl.fromTo("#hks", {{textContent: 0}}, {{textContent: 92, duration: .8, ease: "power3.out", snap: {{textContent: 1}}, immediateRender: false}}, {t_hook + .3:.3f});')
    cue(t_hook, "success")
    bars = "".join(f'<i class="eb" id="eb{k}" style="height:{h}px"></i>' for k, h in enumerate([150, 170, 160, 175, 165, 150, 140, 150, 165, 170]))
    en = glass(f'<div class="et">ENERGY</div><div class="ebars">{bars}</div><div class="edrop" id="edrop">&darr; dropped at 0:07</div>', 470, 830, 560,
               t_ene - .25, S4 - .3, cls="energy", enter="right")
    cue(t_ene - .25, "whoosh")
    js('tl.to(["#eb3", "#eb4", "#eb5", "#eb6"], {height: (k) => [70, 34, 26, 58][k], background: "#ff4d6d", duration: .5, ease: "bounce.out", stagger: .05}, '
       f'{t_drop:.3f});')
    pop("#edrop", t_drop + .15, frm=.5)
    cue(t_drop, "drop")
    gout(f"#{hk}", S4 - .35, to="right")
    gout(f"#{en}", S4 - .3, to="right")
    # swiped away: reels flick off the phone screen to the left
    for k in range(4):
        s = nid("sc")
        put(f'<div class="mini" id="{s}" style="left:{150 + k * 18}px;top:{820 + k * 16}px;z-index:{12 + k}"><i class="play"></i></div>')
        show(f"#{s}", t_swp - .3, S4)
        pop(f"#{s}", t_swp - .3 + k * .05, frm=.6)
        js(f'tl.to("#{s}", {{x: -760, rotation: -35, opacity: 0, filter: "blur(10px)", duration: .45, ease: "power3.in"}}, {t_swp + .1 + k * .12:.3f});')
        if k % 2 == 0:
            cue(t_swp + .1 + k * .12, "swish")
    cree_walk(S3 - .25, S3 + .45, (900, 1290, .42), (800, 1320, .38))
    pose(t_hook, "cheer")
    cree_hop(t_hook + .05, h=50, n=2)
    pose(t_ene - .2, "think")
    pose(t_drop, "sad")
    cree_face(t_drop, "sweat", d=1.4)
    js(f'tl.to("#creeb", {{y: 30, scaleY: .9, duration: .25, ease: "power2.out", yoyo: true, repeat: 1}}, {t_drop:.3f});')
    pose(t_swp - .05, "shock")
    cree_say(t_swp, "!?", d=.9, size=80)

    # ---- S4: "It also gave me new hooks and showed me what to fix before I post the next one."
    headline([("NEW [HOOKS]", 130, t_new, "grad")], 316, out=t_fix - .45)
    headline([("WHAT TO [FIX]", 110, t_fix - .05, "grad")], 320, out=S5 - .5)
    hooks = [("01", "Stanford just open-sourced a real Jarvis"), ("02", "Stop paying for AI assistants"), ("03", "This open-source AI sorts your day")]
    hcs = []
    for k, (n, txt) in enumerate(hooks):
        hcs.append(glass(f'<div class="hn">HOOK {n}</div><div class="htx">{txt}</div>', 470, 630 + k * 172, 560, t_new + k * .16, t_fix + .3, cls="hookc", enter="right",
                         rot=[-2, 1.5, -1][k]))
        cue(t_new + k * .16, "pop")
    for k, h in enumerate(hcs):
        gout(f"#{h}", t_fix - .35 + k * .06, to="right")
    fx = glass('<div class="et">FIX BEFORE YOU POST</div><div class="fxl" id="fx1"><b>&#10003;</b> Caption at 0:12</div>'
               '<div class="fxl" id="fx2"><b>&#10003;</b> Caption at 0:20</div><div class="fxl" id="fx3"><b>&#10003;</b> Save-worthy CTA</div>',
               470, 660, 560, t_fix - .05, S5 - .2, cls="fixc", enter="right", rot=1.5)
    for k in range(3):
        fly(f"#fx{k + 1}", t_fix + .2 + k * .25, x=40, y=0, blur=6, d=.35)
        cue(t_fix + .2 + k * .25, "tick")
    gout(f"#{fx}", S5 - .45, to="right")
    js(f'tl.to("#phone", {{y: 700, rotation: -10, opacity: 0, duration: .45, ease: "power3.in"}}, {S5 - .5:.3f});')
    pose(t_new, "cheer")
    cree_hop(t_new, h=70, n=3, period=.4)
    for k in range(12):                    # confetti
        cf = nid("cf")
        put(f'<i class="conf" id="{cf}" style="left:{800 + RND.uniform(-120, 120):.0f}px;top:1180px;background:{["#F515E8", "#F5876C", "#FFC83D", "#54d6a0"][k % 4]}"></i>')
        show(f"#{cf}", t_new, t_new + 1.6)
        js(f'tl.fromTo("#{cf}", {{x: 0, y: 0, rotation: 0}}, {{x: {RND.uniform(-280, 220):.0f}, y: {RND.uniform(-560, -300):.0f}, rotation: {RND.uniform(-600, 600):.0f}, '
           f'duration: 1.5, ease: "power2.out", immediateRender: false}}, {t_new:.3f});')
    cue(t_new, "sparkle")
    pose(t_new + 1.25, "proud")
    pose(t_fix, "point", flip=True)        # "what to fix": at the fixes on the phone

    # ---- S5: the free account audit (a liquid wipe in)
    liquid(S5 - .62, 540, 2350, S5 - .05)   # a liquid wave rises from the bottom edge
    headline([("[FREE]", 236, t_free, "grad"), ("ACCOUNT AUDIT", 88, t_audit, None)], 236, out=t_type - .5)
    cue(t_free, "hit")
    sparkle(540, 360, t_free + .35, n=10, r=320)
    au = glass('<div class="ah"><img src="assets/img/cree.png" alt=""><b>Account Audit</b><span class="free">FREE</span></div>'
               '<div class="inp" id="auin"><span class="at">@</span><span id="auh"></span><i class="caret" id="auc"></i></div>'
               '<div class="btn" id="aub">Audit my account</div>'
               '<div class="ring" id="aur"><svg viewBox="0 0 200 200"><circle class="rb" cx="100" cy="100" r="82"/>'
               '<circle class="rf" id="aurf" cx="100" cy="100" r="82" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg>'
               '<div class="rval"><span id="aun">20</span><small id="auu">sec</small></div></div>'
               '<div class="first" id="auf"><div class="fl">FIRST THING TO FIX</div><div class="fv">Show the payoff in your first 2 seconds</div></div>',
               90, 650, 900, t_acc - .15, S6 + .2, cls="audit", flt=False)
    cue(t_acc - .15, "whoosh")
    js(f'tl.to("#{au}", {{y: -120, duration: .6, ease: "expo.inOut"}}, {t_type - .45:.3f});')
    handle = "yourhandle"
    for k in range(len(handle) + 1):
        js(f'tl.set("#auh", {{textContent: "{handle[:k]}"}}, {t_hand - .1 + k * .07:.3f});')
    for k in range(0, len(handle), 2):
        cue(t_hand - .1 + k * .07, "type")
    js(f'tl.fromTo("#auc", {{opacity: 1}}, {{opacity: 0, duration: .2, repeat: 9, yoyo: true, ease: "steps(1)", immediateRender: false}}, {t_type - .3:.3f});')
    js(f'tl.fromTo("#aub", {{scale: 1}}, {{keyframes: [{{scale: .92, duration: .08}}, {{scale: 1, duration: .15}}], immediateRender: false}}, {t_20 - .4:.3f});')
    cue(t_20 - .4, "click")
    js(f'tl.to(["#auin", "#aub"], {{opacity: 0, scaleY: .2, duration: .25, ease: "power2.in"}}, {t_20 - .35:.3f});')
    js(f'tl.set(["#auin", "#aub"], {{display: "none"}}, {t_20 - .1:.3f});')
    js(f'tl.set("#aur", {{display: "block", opacity: 1}}, {t_20 - .3:.3f});')
    pop("#aur", t_20 - .3, frm=.5)
    js(f'tl.fromTo("#aurf", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: {t_score - t_20 + .2:.2f}, ease: "power1.inOut", immediateRender: false}}, {t_20 - .1:.3f});')
    js(f'tl.fromTo("#aun", {{textContent: 20}}, {{textContent: 0, duration: {t_score - t_20 + .2:.2f}, ease: "none", snap: {{textContent: 1}}, immediateRender: false}}, {t_20 - .1:.3f});')
    js(f'tl.set("#auu", {{textContent: "/100"}}, {t_score - .02:.3f});')
    js(f'tl.set("#aurf", {{strokeDashoffset: 1, stroke: "url(#gr)"}}, {t_score - .02:.3f});')
    js(f'tl.fromTo("#aun", {{textContent: 0}}, {{textContent: 78, duration: .9, ease: "power2.out", snap: {{textContent: 1}}, immediateRender: false}}, {t_score:.3f});')
    js(f'tl.fromTo("#aurf", {{strokeDashoffset: 1}}, {{strokeDashoffset: .22, duration: .9, ease: "power2.out", immediateRender: false}}, {t_score:.3f});')
    js(f'tl.fromTo("#aur", {{scale: 1}}, {{scale: 1.08, duration: .12, yoyo: true, repeat: 1}}, {t_100 + .1:.3f});')
    sparkle(540, 780, t_100 + .1, n=10, r=260)
    cue(t_score, "rise")
    cue(t_100 + .1, "ding")
    js(f'tl.set("#auf", {{display: "block"}}, {t_first - .12:.3f});')
    fly("#auf", t_first - .1, y=60)
    cue(t_first - .1, "pop")
    js(f'tl.fromTo("#auf", {{boxShadow: "0 0 0 0 rgba(245,21,232,.0)"}}, {{boxShadow: "0 0 0 14px rgba(245,21,232,.25)", duration: .4, yoyo: true, repeat: 2, '
       f'immediateRender: false}}, {t_fix2:.3f});')
    cree_walk(S5 + .05, t_free + .35, (-220, 1330, .40), (840, 1330, .40), end="wave")   # he strolls in under FREE
    pose(t_acc - .1, "proud")
    cree_to(t_type - .45, 880, 1340, .38, d=.5)
    pose(t_type - .3, "phone")
    sw = prop('<svg viewBox="0 0 200 220"><circle cx="100" cy="125" r="80" fill="#fff" stroke="#2b1530" stroke-width="14"/>'
              '<rect x="85" y="18" width="30" height="28" rx="6" fill="#2b1530"/><path id="swh" d="M 100 125 L 100 70" stroke="#F515E8" stroke-width="12" '
              'stroke-linecap="round"/></svg>', t_20 - .3, t_score + .2, cls="prop watch")
    js(f'tl.fromTo("#swh", {{rotation: 0, transformOrigin: "100px 125px"}}, {{rotation: 1080, duration: {t_score - t_20 + .3:.2f}, ease: "none", immediateRender: false}}, '
       f'{t_20 - .3:.3f});')
    pose(t_20 - .3, "think")
    cree_wiggle(t_20 - .2, n=4, amp=6, period=.25)
    pose(t_score + .2, "cheer")
    cree_hop(t_100, h=60, n=2)
    pose(t_first - .1, "point", flip=True)
    cree_say(t_first, "!", d=.8)

    # ---- S6: the CTA, "Comment "CREE" and I'll send you the link." The colour floods out from Cree.
    js(f'tl.fromTo("#ctabg", {{opacity: 1, clipPath: "circle(0px at 880px 1300px)"}}, {{opacity: 1, clipPath: "circle(2300px at 880px 1300px)", duration: .7, ease: "power3.in", '
       f'immediateRender: false}}, {S6 - .1:.3f});')
    HIDE.append("#ctabg")
    cue(S6 - .1, "whoosh_big")
    gout(f"#{au}", S6 - .05, to="up", d=.4, y0=-120)
    cree_to(S6 + .2, 540, 800, .9, d=.7, ease="back.out(1.4)")
    pose(S6 + .2, "wave", flip=False)
    cree_wiggle(S6 + .9, n=4, amp=9)
    headline([("[COMMENT]", 132, t_com, "white")], 1140, out=None, z=22)
    cb = nid("cb")
    put(f'<div class="cbar" id="{cb}"><span class="cav"></span><span class="ctx" id="{cb}t"></span><i class="caret dark" id="{cb}c"></i>'
        f'<span class="cpost" id="{cb}p">Post</span><svg class="heart" id="{cb}h" viewBox="0 0 40 36"><path d="M20 34 C 8 25 1 18 1 10 A 9 9 0 0 1 20 6 A 9 9 0 0 1 39 10 '
        f'C 39 18 32 25 20 34 Z" fill="#ff2d6f"/></svg></div>')
    show(f"#{cb}", t_com + .1, S7)
    js(f'tl.fromTo("#{cb}", {{transformPerspective: 1200, opacity: 0, y: 200, scale: .8, rotationX: 40}}, {{opacity: 1, y: 0, scale: 1, rotationX: 0, duration: .7, ease: "back.out(1.6)", '
       f'transformPerspective: 1200, immediateRender: false}}, {t_com + .1:.3f});')
    for k in range(5):
        js(f'tl.set("#{cb}t", {{textContent: "{"CREE"[:k]}"}}, {t_cree + k * .16:.3f});')
        if k:
            cue(t_cree + k * .16, "type")
    js(f'tl.fromTo("#{cb}p", {{scale: 1}}, {{keyframes: [{{scale: .85, duration: .08}}, {{scale: 1.1, duration: .15}}, {{scale: 1, duration: .1}}], immediateRender: false}}, '
       f'{t_cree + .8:.3f});')
    pop(f"#{cb}h", t_cree + .85, frm=0, ease="back.out(3)")
    cue(t_cree + .85, "pop")
    for k in range(7):                     # glass hearts float up from the comment
        hh = nid("hh")
        put(f'<svg class="gheart" id="{hh}" viewBox="0 0 40 36" style="left:{700 + RND.uniform(-60, 220):.0f}px;top:1290px"><path d="M20 34 C 8 25 1 18 1 10 A 9 9 0 0 1 20 6 '
            f'A 9 9 0 0 1 39 10 C 39 18 32 25 20 34 Z"/></svg>')
        show(f"#{hh}", t_cree + .9 + k * .12, S7)
        js(f'tl.fromTo("#{hh}", {{y: 0, x: 0, scale: .3, rotation: 0}}, {{y: {RND.uniform(-700, -420):.0f}, x: {RND.uniform(-120, 120):.0f}, scale: {RND.uniform(.8, 1.4):.2f}, '
           f'rotation: {RND.uniform(-30, 30):.0f}, opacity: 0, duration: 1.8, ease: "power1.out", immediateRender: false}}, {t_cree + .9 + k * .12:.3f});')
    pose(t_cree - .15, "phone")
    pl = nid("pl")
    put(f'<svg class="plane" id="{pl}" viewBox="0 0 100 100"><path d="M 5 45 L 95 8 L 62 92 L 46 60 Z" fill="#fff"/><path d="M 46 60 L 95 8" stroke="#F54BA8" '
        f'stroke-width="5"/></svg>')
    show(f"#{pl}", t_send - .2, S7)
    js(f'tl.fromTo("#{pl}", {{x: 0, y: 0, rotation: -10, scale: .5}}, {{x: 220, y: -1000, rotation: 18, scale: 1.1, duration: .9, ease: "power2.in", immediateRender: false}}, '
       f'{t_send - .2:.3f});')
    cue(t_send - .2, "whoosh")
    glass('<div class="dmh"><img src="assets/img/cree.png" alt=""><b>Creedom</b></div><div class="dmt">Here\'s your link &#128279;</div>', 560, 290, 440,
          t_link - .05, S7, cls="dm", z=22, rot=3)
    cue(t_link - .05, "notify")
    pose(t_send - .25, "point", flip=False)
    pose(t_link - .05, "cheer")
    cree_say(t_link, "♥", d=.8)
    cree_hop(t_link + .1, h=80, n=2)

    # ---- S7: the logo
    js(f'tl.fromTo("#logo", {{opacity: 1, clipPath: "circle(0px at 540px 860px)"}}, {{opacity: 1, clipPath: "circle(1400px at 540px 860px)", duration: .55, ease: "power3.in", '
       f'immediateRender: false}}, {S7 - .2:.3f});')
    HIDE.append("#logo")
    js(f'tl.set("#cree", {{opacity: 0}}, {S7 + .4:.3f});')
    js(f'tl.fromTo("#lgm", {{scale: 0, rotation: -40, y: 80}}, {{scale: 1, rotation: 0, y: 0, duration: .6, ease: "back.out(2)", immediateRender: false}}, {S7 + .05:.3f});')
    js(f'tl.fromTo("#lgw", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", duration: .55, ease: "power3.out", immediateRender: false}}, {S7 + .25:.3f});')
    js(f'tl.fromTo("#lgt", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: .4, ease: "power3.out", immediateRender: false}}, {S7 + .45:.3f});')
    js(f'tl.fromTo("#lgm", {{rotation: 0}}, {{keyframes: [{{rotation: 10, duration: .14}}, {{rotation: -8, duration: .14}}, {{rotation: 6, duration: .12}}, '
       f'{{rotation: 0, duration: .1}}], immediateRender: false}}, {S7 + .7:.3f});')
    cue(S7 + .05, "logo")
    sparkle(540, 860, S7 + .3, n=12, r=380, z=41)

    # Cree idles: a slow bob and a blink every couple of seconds the whole way
    js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -10, duration: .8, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .8)}, immediateRender: false}}, 0);')
    for tb in [1.2, 2.2, 6.9, 8.0, 9.3, 12.95, 15.2, 20.4, 23.4, 26.0, 30.8, 33.0]:   # only while an open-eyed pose shows
        cree_face(tb, "blink")


def background():
    """Morphing blurred colour blobs and drifting glass orbs: the frame is never still."""
    blobs = [(-320, -260, 980, "#F515E8"), (520, 1080, 1000, "#F5876C"), (380, 260, 760, "#ffb3e6"), (-260, 1300, 820, "#c86bff")]
    html = ""
    for k, (x, y, s, c) in enumerate(blobs):
        html += f'<i class="blob" data-layout-allow-overflow id="bl{k}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>'
        dx, dy = RND.uniform(-260, 260), RND.uniform(-300, 300)
        js(f'tl.to("#bl{k}", {{x: {dx:.0f}, y: {dy:.0f}, rotation: {RND.choice([-1, 1]) * 120}, duration: {DUR:.1f}, ease: "sine.inOut"}}, 0);')
        js(f'tl.fromTo("#bl{k}", {{borderRadius: "50% 50% 50% 50% / 50% 50% 50% 50%"}}, {{borderRadius: "38% 62% 57% 43% / 61% 39% 58% 42%", duration: {3.2 + k * .7:.1f}, '
           f'ease: "sine.inOut", yoyo: true, repeat: {int(DUR / (3.2 + k * .7))}, immediateRender: false}}, 0);')
    for k in range(9):
        s = RND.choice([46, 64, 90, 120, 150])
        x, y = RND.uniform(-40, FW - 60), RND.uniform(200, FH - 200)
        html += f'<i class="orb" id="ob{k}" style="left:{x:.0f}px;top:{y:.0f}px;width:{s}px;height:{s}px"></i>'
        js(f'tl.to("#ob{k}", {{y: {-RND.uniform(260, 620):.0f}, duration: {DUR:.1f}, ease: "none"}}, 0);')
        js(f'tl.fromTo("#ob{k}", {{x: -24}}, {{x: 24, duration: {RND.uniform(2.6, 4.2):.1f}, ease: "sine.inOut", yoyo: true, repeat: 11, immediateRender: false}}, 0);')
    return html


CSS = f"""
@font-face {{ font-family: "Outfit"; font-weight: 600; src: url("assets/fonts/Outfit-600.woff2"); }}
@font-face {{ font-family: "Outfit"; font-weight: 800; src: url("assets/fonts/Outfit-800.woff2"); }}
@font-face {{ font-family: "Outfit"; font-weight: 900; src: url("assets/fonts/Outfit-900.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #fff6fb; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #fff6fb; font-family: "Outfit"; color: #1d0f24; }}
#cam, #cam2 {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
#cam {{ z-index: 2; }}
#bgl {{ position: absolute; inset: 0; overflow: hidden; }}
#dots {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(245,75,168,.2) 2px, transparent 2.5px); background-size: 46px 46px; }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(100px); opacity: .34; }}
.orb {{ position: absolute; border-radius: 50%; z-index: 1; border: 2px solid rgba(255,255,255,.75);
  background: radial-gradient(circle at 32% 28%, rgba(255,255,255,.95) 0 8%, rgba(255,255,255,.35) 22%, rgba(255,190,230,.18) 60%, rgba(245,75,168,.16) 100%);
  box-shadow: inset -8px -10px 24px rgba(245,75,168,.18), 0 14px 30px rgba(200,40,140,.12); }}
/* kinetic type */
.head {{ position: absolute; left: 0; right: 0; opacity: 0; text-align: center; }}
.hl {{ opacity: 0; font-weight: 900; line-height: .98; letter-spacing: -.025em; word-spacing: .16em; white-space: nowrap; color: #1d0f24; transform-origin: 50% 60%; }}
.hli {{ position: relative; display: inline-block; }}
.wm {{ display: inline-block; overflow: hidden; vertical-align: top; padding: .08em .05em .16em; margin: -.08em -.05em -.16em; }}
.wi {{ display: inline-block; transform-origin: 50% 80%; }}
.acc {{ background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; padding: 0 .02em; }}
.acc.grad {{ background-image: linear-gradient(90deg,#F515E8 0%,#F54BA8 30%,#F5876C 50%,#ff9fe4 60%,#F515E8 72%,#F54BA8 100%); }}
.acc.red {{ background-image: linear-gradient(90deg,#ff2d55 0%,#ff4d6d 45%,#ff8da3 58%,#ff2d55 70%,#e0143c 100%); }}
.acc.green {{ background-image: linear-gradient(90deg,#10a35f 0%,#22c47a 45%,#5fdc9e 58%,#10a35f 70%,#0b8a50 100%); }}
.acc.white {{ background-image: linear-gradient(90deg,#ffffff 0%,#ffffff 45%,#ffd6f3 55%,#ffffff 66%,#ffffff 100%); filter: drop-shadow(0 10px 26px rgba(110,0,70,.35)); }}
.uline {{ position: absolute; left: 4%; right: 4%; bottom: -.14em; width: 92%; height: .2em; overflow: visible; }}
.uline path {{ fill: none; stroke: url(#gr); stroke-width: 9; stroke-linecap: round; }}
/* glass */
.glass {{ position: absolute; opacity: 0; border-radius: 40px; padding: 28px 32px; overflow: hidden;
  background: linear-gradient(140deg, rgba(255,255,255,.84) 0%, rgba(255,255,255,.52) 55%, rgba(255,236,248,.66) 100%);
  border: 2px solid rgba(255,255,255,.92); backdrop-filter: blur(22px) saturate(1.5); -webkit-backdrop-filter: blur(22px) saturate(1.5);
  box-shadow: 0 30px 70px rgba(170,20,110,.17), 0 6px 18px rgba(170,20,110,.08), inset 0 2px 0 rgba(255,255,255,.95), inset 0 -26px 50px rgba(245,75,168,.07); }}
.shine {{ position: absolute; top: -30%; bottom: -30%; left: -48%; width: 40%; pointer-events: none;
  background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.8) 50%, rgba(255,255,255,0) 100%); transform: skewX(-18deg); }}
.glass.chip {{ left: 0 !important; right: 0; width: max-content !important; margin: 0 auto; padding: 12px 34px 12px 14px; border-radius: 999px; display: flex;
  align-items: center; gap: 16px; font: 600 40px/1 "Outfit"; z-index: 9; }}
.chip img {{ width: 64px; height: 64px; object-fit: contain; }}
.chip b {{ font-weight: 900; background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; }}
/* retention */
.graph .gh {{ display: flex; justify-content: space-between; align-items: baseline; }}
.gt {{ font: 800 42px/1 "Outfit"; }}
.gp {{ font: 900 60px/1 "Outfit"; background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.avs {{ display: flex; gap: 14px; margin: 18px 0 6px; }}
.av {{ display: grid; place-items: center; width: 60px; height: 60px; border-radius: 50%; opacity: 0; background: linear-gradient(140deg,#F54BA8,#F5876C);
  box-shadow: 0 8px 18px rgba(245,75,168,.3), inset 0 2px 0 rgba(255,255,255,.5); }}
.av svg {{ width: 34px; height: 34px; fill: #fff; }}
.gs {{ width: 100%; height: 272px; overflow: visible; }}
.gl0 {{ stroke: #f1dbe8; stroke-width: 4; }}
.gline {{ fill: none; stroke: url(#gr); stroke-width: 12; stroke-linecap: round; stroke-linejoin: round; }}
.gdot {{ fill: #ff2d55; opacity: 0; transform-box: fill-box; transform-origin: center; }}
.gtag {{ position: absolute; left: 450px; top: 196px; opacity: 0; background: #1d0f24; color: #fff; font: 800 30px/1 "Outfit"; padding: 14px 20px; border-radius: 16px; }}
/* the flopped reel */
.glass.reel {{ padding: 0; }}
.rv {{ position: relative; height: 470px; background: linear-gradient(160deg,#3a2140,#7a3060 60%,#c0567a); display: grid; place-items: center; }}
.play {{ display: block; width: 0; height: 0; border-left: 70px solid rgba(255,255,255,.9); border-top: 44px solid transparent; border-bottom: 44px solid transparent; margin-left: 20px; }}
.up {{ position: absolute; left: 30px; right: 30px; bottom: 30px; padding: 18px 22px; border-radius: 22px; background: rgba(255,255,255,.22);
  border: 1.5px solid rgba(255,255,255,.5); backdrop-filter: blur(10px); }}
.upt {{ font: 800 30px/1 "Outfit"; color: #fff; margin-bottom: 12px; }}
.upb {{ height: 12px; border-radius: 6px; background: rgba(255,255,255,.3); overflow: hidden; }}
.upb i {{ display: block; height: 100%; background: linear-gradient(90deg,#F515E8,#F5876C); transform-origin: 0 50%; }}
.rm {{ padding: 22px 28px 26px; display: flex; flex-direction: column; gap: 6px; }}
.rm > b {{ font: 800 36px/1.1 "Outfit"; }}
.views {{ font: 600 32px/1.1 "Outfit"; color: #7b6a80; }}
.views b {{ color: #1d0f24; }}
.views em {{ display: inline-block; opacity: 0; font-style: normal; color: #ff2d55; font-weight: 800; }}
.stampf {{ position: absolute; left: 50px; top: 200px; opacity: 0; font: 900 72px/1.1 "Outfit"; color: #ff2d55; border: 10px solid #ff2d55; border-radius: 18px;
  padding: 0 22px; background: rgba(255,255,255,.88); }}
/* the phone */
#phone {{ position: absolute; opacity: 0; z-index: 6; }}
#phonei {{ position: absolute; inset: 0; border-radius: 72px; background: #160b18; padding: 14px;
  box-shadow: 0 50px 110px rgba(120,10,80,.32), 0 0 0 4px #3a2a3c inset, 0 0 0 2px rgba(255,255,255,.35); }}
#phone .scr {{ position: relative; width: 100%; height: 100%; border-radius: 58px; overflow: hidden; background: #fdfdfd; }}
.pv {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; }}
.isl {{ position: absolute; left: 50%; top: 26px; width: 112px; height: 33px; margin-left: -56px; border-radius: 17px; background: #050305; }}
.scan {{ position: absolute; left: 0; right: 0; top: 0; height: 11%; opacity: 0; mix-blend-mode: multiply;
  background: linear-gradient(180deg, rgba(245,21,232,0), rgba(245,21,232,.22) 70%, rgba(245,21,232,.6) 100%); }}
.refl {{ position: absolute; top: -10%; bottom: -10%; left: 0; width: 45%; pointer-events: none;
  background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0)); transform: skewX(-16deg); }}
.film {{ position: absolute; left: 0; top: 458px; width: {FW}px; height: 70px; opacity: 0; z-index: 4; }}
.fin {{ display: flex; gap: 14px; padding-left: 40px; }}
.fc {{ flex: 0 0 auto; width: 140px; height: 70px; border-radius: 18px; font: 800 30px/66px "Outfit"; text-align: center; color: #1d0f24;
  background: rgba(255,255,255,.62); border: 2px solid rgba(255,255,255,.95); box-shadow: 0 10px 24px rgba(170,20,110,.12); }}
.film .fc:nth-child(3n) {{ background: linear-gradient(90deg,#F515E8,#F5876C); color: #fff; border-color: rgba(255,255,255,.6); }}
/* findings */
.hkr {{ display: flex; align-items: center; gap: 20px; }}
.ok {{ display: grid; place-items: center; width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(140deg,#22c47a,#10a35f); flex: 0 0 auto;
  box-shadow: 0 10px 22px rgba(16,163,95,.35); }}
.ok svg {{ width: 44px; height: 44px; }}
.hkl {{ font: 900 26px/1 "Outfit"; letter-spacing: .08em; color: #7b6a80; }}
.hkv {{ font: 900 40px/1.15 "Outfit"; margin-top: 6px; }}
.hks {{ margin-left: auto; font: 900 64px/1 "Outfit"; color: #10a35f; }}
.hkbar {{ margin-top: 18px; height: 14px; border-radius: 7px; background: rgba(16,163,95,.14); overflow: hidden; }}
.hkbar i {{ display: block; height: 100%; background: linear-gradient(90deg,#22c47a,#10a35f); transform-origin: 0 50%; }}
.et {{ font: 900 30px/1 "Outfit"; letter-spacing: .08em; color: #7b6a80; margin-bottom: 16px; }}
.ebars {{ display: flex; align-items: flex-end; gap: 12px; height: 180px; }}
.eb {{ display: block; flex: 1; border-radius: 10px; background: linear-gradient(180deg,#F515E8,#F5876C); }}
.edrop {{ opacity: 0; margin-top: 14px; font: 900 34px/1 "Outfit"; color: #ff2d55; text-align: center; }}
.mini {{ position: absolute; opacity: 0; width: 200px; height: 330px; border-radius: 26px; background: linear-gradient(160deg,#3a2140,#a2406e); display: grid; place-items: center;
  box-shadow: 0 18px 40px rgba(0,0,0,.25); border: 2px solid rgba(255,255,255,.5); }}
.mini .play {{ border-left-width: 40px; border-top-width: 26px; border-bottom-width: 26px; margin-left: 12px; }}
.glass.hookc {{ padding: 22px 28px; }}
.hn {{ font: 900 26px/1 "Outfit"; letter-spacing: .1em; background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; margin-bottom: 10px; }}
.htx {{ font: 800 34px/1.15 "Outfit"; }}
.fxl {{ opacity: 0; font: 800 36px/1.2 "Outfit"; padding: 10px 0; display: flex; gap: 14px; align-items: center; }}
.fxl b {{ display: inline-grid; place-items: center; width: 46px; height: 46px; border-radius: 50%; background: #18b26b; color: #fff; font-size: 26px; }}
.conf {{ position: absolute; opacity: 0; width: 22px; height: 34px; border-radius: 6px; z-index: 21; }}
#lq {{ position: absolute; left: 0; top: 0; width: 2800px; height: 2800px; z-index: 30; opacity: 0; border-radius: 50%;
  background: radial-gradient(circle at 40% 35%, #ff8be0 0%, #F515E8 35%, #F54BA8 62%, #F5876C 100%); }}
/* the audit */
.glass.audit {{ padding: 40px 44px; z-index: 7; overflow: visible; }}
.ah {{ display: flex; align-items: center; gap: 18px; font: 900 48px/1 "Outfit"; }}
.ah img {{ width: 84px; height: 84px; object-fit: contain; }}
.free {{ margin-left: auto; font: 900 30px/1 "Outfit"; color: #fff; background: {GRAD}; padding: 12px 22px; border-radius: 999px; }}
.inp {{ margin-top: 32px; height: 110px; border-radius: 28px; background: rgba(255,255,255,.7); border: 3px solid #f6cfe4; display: flex; align-items: center; padding: 0 34px;
  font: 800 52px/1 "Outfit"; overflow: hidden; }}
.at {{ color: #F515E8; margin-right: 6px; }}
.caret {{ display: inline-block; width: 5px; height: 60px; background: #F515E8; margin-left: 4px; }}
.btn {{ margin-top: 22px; height: 100px; border-radius: 28px; background: {GRAD}; color: #fff; font: 900 44px/100px "Outfit"; text-align: center; overflow: hidden;
  box-shadow: 0 16px 34px rgba(245,21,232,.3); }}
.ring {{ position: relative; width: 300px; height: 300px; margin: 30px auto 0; opacity: 0; display: none; }}
.ring svg {{ width: 100%; height: 100%; }}
.rb {{ fill: none; stroke: rgba(245,75,168,.16); stroke-width: 22; }}
.rf {{ fill: none; stroke: #1d0f24; stroke-width: 22; stroke-linecap: round; }}
.rval {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 92px; }}
.rval span {{ font: 900 110px/1 "Outfit"; }}
.rval small {{ font: 800 40px/1 "Outfit"; color: #7b6a80; margin-left: 4px; }}
.first {{ display: none; opacity: 0; margin-top: 26px; border-radius: 26px; padding: 22px 28px; background: rgba(255,243,250,.85); border: 3px solid #F54BA8; }}
.fl {{ font: 900 28px/1 "Outfit"; letter-spacing: .1em; color: #F515E8; margin-bottom: 10px; }}
.fv {{ font: 800 40px/1.15 "Outfit"; }}
/* the CTA */
#ctabg {{ position: absolute; inset: 0; z-index: 15; opacity: 0; background: radial-gradient(circle at 50% 40%, #ff7ad9 0%, #F515E8 40%, #c4128f 100%); }}
#ctabg::after {{ content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.25) 2px, transparent 2.5px); background-size: 46px 46px; }}
.cbar {{ position: absolute; left: 90px; top: 1310px; width: 900px; height: 130px; opacity: 0; z-index: 22; border-radius: 999px; display: flex; align-items: center;
  padding: 0 26px; gap: 20px; background: rgba(255,255,255,.88); border: 2px solid rgba(255,255,255,.95); box-shadow: 0 24px 50px rgba(80,0,60,.3), inset 0 2px 0 #fff; }}
.cav {{ width: 84px; height: 84px; border-radius: 50%; background: url(assets/img/cree.png) center/86% no-repeat, #ffe3f3; flex: 0 0 auto; }}
.ctx {{ font: 900 64px/1 "Outfit"; letter-spacing: .04em; }}
.caret.dark {{ background: #1d0f24; height: 64px; }}
.cpost {{ margin-left: auto; font: 900 44px/1 "Outfit"; color: #c40db8; }}
.heart {{ position: absolute; right: -30px; top: -90px; width: 110px; height: 100px; opacity: 0; }}
.gheart {{ position: absolute; width: 70px; height: 64px; opacity: 0; z-index: 21; overflow: visible; }}
.gheart path {{ fill: rgba(255,255,255,.55); stroke: rgba(255,255,255,.95); stroke-width: 2; }}
.plane {{ position: absolute; left: 980px; top: 1200px; width: 120px; height: 120px; opacity: 0; z-index: 23; filter: drop-shadow(0 10px 18px rgba(80,0,60,.35)); }}
.glass.dm {{ padding: 22px 26px; }}
.dmh {{ display: flex; align-items: center; gap: 12px; font: 900 34px/1 "Outfit"; }}
.dmh img {{ width: 56px; height: 56px; object-fit: contain; }}
.dmt {{ margin-top: 12px; font: 800 38px/1.2 "Outfit"; }}
/* captions */
.cap {{ position: absolute; left: 60px; right: 60px; top: 1500px; opacity: 0; text-align: center; z-index: 25; font: 800 54px/1.25 "Outfit"; color: #1d0f24; }}
.cw {{ display: inline-block; padding: 2px 14px 6px; border-radius: 16px; }}
.cw.on {{ background: {GRAD}; color: #fff; box-shadow: 0 10px 22px rgba(245,21,232,.3); }}
/* logo */
#logo {{ position: absolute; inset: 0; z-index: 40; opacity: 0; background: radial-gradient(circle at 50% 45%, #ffffff 0%, #fff3fa 70%, #ffe6f4 100%); }}
#lgm {{ position: absolute; left: 80px; top: 720px; width: 260px; height: 260px; object-fit: contain; }}
#lgw {{ position: absolute; left: 350px; top: 775px; font: 800 150px/1 "Outfit"; letter-spacing: -.02em; background: linear-gradient(90deg,#F515E8,#F5876C);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-bottom: 16px; }}
#lgt {{ position: absolute; left: 0; right: 0; top: 1020px; text-align: center; font: 600 46px/1.2 "Outfit"; color: #7b6a80; opacity: 0; }}
.spk {{ position: absolute; width: 44px; height: 44px; opacity: 0; }}
/* Cree */
#cree {{ position: absolute; left: 0; top: 0; width: 820px; height: 820px; z-index: 20; opacity: 0; transform-origin: 410px 500px; }}
#creeb {{ position: absolute; inset: 0; transform-origin: 50% 97.5%; }}
#creef {{ position: absolute; inset: 0; transform-origin: 50% 60%; }}
#creep {{ position: absolute; inset: 0; transform-origin: 50% 97.5%; }}
.cpose {{ position: absolute; inset: 0; opacity: 0; }}
#cp-wave {{ opacity: 1; }}
.cpose img, .clids, .csw {{ position: absolute; inset: 0; width: 820px; height: 820px; }}
.csw {{ overflow: visible; }}
.lidg {{ opacity: 0; }}
.sweat {{ opacity: 0; transform-box: fill-box; transform-origin: 50% 0; }}
#bub {{ position: absolute; left: 560px; top: 20px; width: 200px; height: 170px; opacity: 0; background: rgba(255,255,255,.92); border-radius: 50% 50% 50% 12px;
  border: 2px solid #fff; box-shadow: 0 14px 30px rgba(150,20,100,.2); display: grid; place-items: center; transform-origin: 0 100%; }}
#bubt {{ font: 900 96px/1 "Outfit"; color: #c40db8; }}
.prop {{ position: absolute; opacity: 0; transform-origin: 50% 80%; }}
.prop.watch {{ left: 40px; top: 110px; width: 230px; height: 250px; }}
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
    <svg width="0" height="0" style="position:absolute"><defs><linearGradient id="gr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F515E8"/>
      <stop offset=".5" stop-color="#F54BA8"/><stop offset="1" stop-color="#F5876C"/></linearGradient></defs></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="bgl">{bg}<div id="dots"></div></div>
      <div id="cam"><div id="cam2">
      {"".join(EL)}
      <div id="ctabg"></div>
      {cree}
      </div></div>
      {"".join(CAPS)}
      <div id="lq"></div>
      <div id="logo"><img id="lgm" src="assets/img/cree.png" alt="Cree"><div id="lgw">Creedom</div><div id="lgt">creedom.ai</div></div>
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
