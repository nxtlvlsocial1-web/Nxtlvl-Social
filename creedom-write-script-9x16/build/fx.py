"""Shared animation helpers for the Creedom @write-script reel, taken from creedom-check-9x16/build/generate.py
(glass headlines, shines, whips, liquid-glass morphs, punch-ins, and the Cree mascot rig with its thirteen poses).
generate.py does `from fx import *`; JS, SFX and HTML are the shared output lists."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
PINK, MAG, ROSE, INK = "#EE688B", "#F343A2", "#B1476B", "#0B0B0B"
LINES = {}
for w in W:
    LINES.setdefault(w["line"], []).append(w)
L0 = {k: v[0]["t0"] for k, v in LINES.items()}
L1 = {k: v[-1]["t1"] for k, v in LINES.items()}
JS, SFX, HTML = [], [], []


def T(line, word, n=0):
    k = word.lower()
    hits = [w for w in LINES[line] if w["w"].lower().strip(".,:!?").startswith(k)]
    return hits[min(n, len(hits) - 1)]["t0"]


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def ft(sel, t, d, frm, to, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


WID = [0]


def head(hid, rows, top, line, size=88, dark=False, after=0.0):
    """premium headline, centred: every word blurs into focus on its spoken time; ('word', cls) with cls '' or 'it'"""
    spoken, k, out, rws = [w for w in LINES[line] if w["t0"] >= after], 0, [], []
    for row in rows:
        ws = []
        for word, cls in row:
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?"), None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?")
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            if t is None:
                t = spoken[-1]["t0"]
            ws.append(f'<span class="hw {cls}" id="{wid}">{word}</span>')
            out.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTML.append(f'<div class="head {"dk" if dark else ""}" id="{hid}" style="top:{top}px;font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out:
        ft(f"#{wid}", t - .06, .5, "{opacity: 0, filter: 'blur(14px)', y: 26}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    return out


def head_out(hid, t):
    to(f"#{hid}", t, .3, "{opacity: 0, filter: 'blur(16px)', y: -40}", "power2.in")


SH = '<i class="sh"></i>'                       # specular shine bar inside a glass object


def shine(sel, t, d=.9):
    ft(f"{sel} > .sh", t, d, "{xPercent: -160, opacity: 1}", "{xPercent: 420, opacity: 1}", "power2.inOut")


def tilt(sel, t0, t1, a=4, per=1.7):
    """slow 3D drift so the glass catches the light (rotation only, so it never fights the position tweens)"""
    n = max(1, int((t1 - t0) / per))
    js(f'tl.fromTo("{sel}", {{rotationX: 0, rotationY: 0, transformPerspective: 1400}}, {{rotationX: {a * .6:.1f}, rotationY: {-a}, transformPerspective: 1400, duration: {per:.2f}, ease: "sine.inOut", '
       f'yoyo: true, repeat: {n - 1}, immediateRender: false}}, {t0:.3f});')


# v6 (owner: "it still feels very slow"): voice ~1.12x faster, a punchy CC BY track ("Corporate Music" by Ruslan Latypov,
# 99.4 bpm, strong kick) with every scene cut on its half-beat grid, 0.3 s whips and zooms instead of 0.5 s glides,
# a punch-in + glass flash on every key word, the score scene split in two shots, light streaks on cuts, overshoot
# entrances, faster panes, more mascot poses, a riser into every cut and deep hits on the hook and CHECK.
BEAT = 60 / 99.384
HB = BEAT / 2


def snap(t):
    """nearest half-beat of the song (it starts on a beat at reel t = 0)"""
    return round(t / HB) * HB


def sweep(t):
    """frosted-glass panel sweeping across the frame (scene change)"""
    ft("#sweep", t - .16, .36, "{xPercent: -170}", "{xPercent: 170}", "power2.inOut")
    sfx("whoosh_big", t - .2)


def streak(t):
    """three glass light streaks flying through the cut"""
    for i in range(3):
        ft(f"#stk{i}", t - .14 + .05 * i, .38, "{xPercent: -260, opacity: 1}", "{xPercent: 260, opacity: 1}", "power2.inOut")


def whip(t, d=1):
    """fast whip pan with motion blur: out to one side, in from the other (0.38 s in all)"""
    ft("#cam", t - .16, .16, "{x: 0, filter: 'blur(0px)'}", f"{{x: {-460 * d}, filter: 'blur(24px)'}}", "power2.in")
    ft("#cam", t, .24, f"{{x: {460 * d}, filter: 'blur(24px)'}}", "{x: 0, filter: 'blur(0px)'}", "power3.out")
    streak(t)
    sfx("riser_short", t - .9)
    sfx("whoosh", t - .18)


def punch(t, k=1.055):
    """punch-in with a soft glass flash on a key word"""
    ft("#punch", t - .03, .08, "{scale: 1}", f"{{scale: {k}}}", "power2.out")
    to("#punch", t + .05, .42, "{scale: 1}", "power3.out")
    st("#flash", t - .03, "{opacity: .38}")
    to("#flash", t - .02, .32, "{opacity: 0}", "power2.out")
    sfx("thump", t - .02)


LIQ = [0]


def liquid(t):
    """liquid-glass morph: an organic glass drop grows over the frame, the scene changes under it, and it melts away"""
    LIQ[0] += 1
    r0, r1 = "50% 50% 50% 50% / 50% 50% 50% 50%", ("42% 58% 63% 37% / 41% 44% 56% 59%", "58% 42% 38% 62% / 55% 61% 39% 45%")[LIQ[0] % 2]
    ft("#liq", t - .42, .45, f"{{scale: .04, rotation: 0, borderRadius: '{r0}'}}", f"{{scale: 4.4, opacity: 1, rotation: {(90, -90)[LIQ[0] % 2]}, borderRadius: '{r1}'}}", "power2.in")
    to("#liq", t + .03, .35, "{opacity: 0, filter: 'blur(30px)'}", "power2.out")
    st("#liq", t - .42, "{filter: 'blur(0px)', opacity: 1}")
    st("#liq", t + .4, "{scale: .04, filter: 'blur(0px)'}")
    streak(t)
    sfx("riser_short", t - .9)
    sfx("whoosh", t - .4)
    sfx("swish", t - .05)


def zoom_through(t):
    ft("#cam", t - .18, .2, "{scale: 1, filter: 'blur(0px)'}", "{scale: 1.6, filter: 'blur(14px)'}", "power2.in")
    ft("#cam", t + .02, .34, "{scale: .82, filter: 'blur(14px)'}", "{scale: 1, filter: 'blur(0px)'}", "expo.out")
    streak(t)
    sfx("riser", t - .8)
    sfx("whoosh", t - .15)


def mode(t, dark):
    """crossfade between the light and the dark fluid worlds"""
    to("#dark", t - .08, .3, f"{{opacity: {1 if dark else 0}}}", "power2.inOut")


def scene(sid, t0, t1):
    st(f"#{sid}", t0, "{opacity: 1}")
    st(f"#{sid}", t1, "{opacity: 0}")
    ft("#drift", t0, t1 - t0, "{scale: 1}", "{scale: 1.035}", "none")      # slow push-in on every scene


# ---- the Creedom mascot, Cree (not a bird): the full 3D mascot from the creedom-explainer reel ------------------------------
# v5 (owner: "when i say the mascot looks bad then it is bad, look how full he looks in the previous video, make him
# like that"): the cut-out rig is gone; Cree is the mascot's own 3D render in thirteen poses (creedom-explainer-9x16,
# assets/img/poses, plan/poses.json): stand, walk + pass (walk cycle), wave, point (to his left = frame right), present,
# cheer, shock, sad, mag (magnifying glass), phone (typing), think, proud. Every pose sits on one 820 x 820 canvas with
# the feet on y 800, so a pose swap never moves him; the body centre is (410, 500). He swaps poses on the script beats,
# walks between scenes, hops with squash and stretch, blinks, sweats, and gets glass "?" and "!" bubbles.
POSES = json.load(open(os.path.join(ROOT, "plan", "poses.json")))
PCX, PCY = 410, 500
CS = .52                                         # his scale: 600 px pose height -> ~312 px on screen


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
    sp = "".join(f'<div class="csp" style="left:{x}px;top:{y}px">{star(z, c)}</div>'
                 for x, y, z, c in [(40, 170, 110, PINK), (680, 110, 90, "#f2b134"), (720, 440, 70, PINK), (60, 470, 64, "#f2b134")])
    return (f'<div id="cree"><i id="cshadow"></i><div id="creeb"><div id="creef"><div id="creep">{"".join(parts)}</div></div>{sweat}</div>'
            f'{sp}<div id="bub"><span id="bubt">!</span></div></div>')


def cree_to(t, x, y, s=CS, d=.6, ease="power3.inOut"):
    """Move Cree (body centre at x, y in frame px; s = scale of the 820 px pose canvas)."""
    js(f'tl.to("#cree", {{x: {x - PCX:.0f}, y: {y - PCY:.0f}, scale: {s}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def pose(t, name, flip=None, squash=True):
    """Swap to a pose (flip: True faces him the other way, None keeps the current facing), with a little squash."""
    js(f'tl.set("#cree .cpose", {{opacity: 0}}, {t:.3f});')
    js(f'tl.set("#cp-{name}", {{opacity: 1}}, {t:.3f});')
    if flip is not None:
        js(f'tl.set("#creef", {{scaleX: {-1 if flip else 1}}}, {t:.3f});')
    if squash:
        js(f'tl.fromTo("#creep", {{scaleX: 1.07, scaleY: .9}}, {{scaleX: 1, scaleY: 1, duration: .28, ease: "back.out(3)", immediateRender: false}}, {t:.3f});')


def cree_walk(t0, t1, frm, to, end="stand", step=.15, end_flip=False):
    """Walk from frm (x, y, s) to to (x, y, s): stride and pass frames alternate with a bob, facing the way he goes."""
    n = max(2, round((t1 - t0) / step))
    n += n % 2
    stp = (t1 - t0) / n
    flip = to[0] < frm[0]
    js(f'tl.fromTo("#cree", {{x: {frm[0] - PCX:.0f}, y: {frm[1] - PCY:.0f}, scale: {frm[2]}}}, {{x: {to[0] - PCX:.0f}, y: {to[1] - PCY:.0f}, scale: {to[2]}, '
       f'duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    for k in range(n):
        pose(t0 + k * stp, "walk" if k % 2 == 0 else "pass", flip=flip if k == 0 else None, squash=False)
    js(f'tl.fromTo("#creef", {{y: 0}}, {{y: -22, duration: {stp / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: {2 * n - 1}, immediateRender: false}}, {t0:.3f});')
    js(f'tl.fromTo("#creef", {{rotation: -4}}, {{rotation: 4, duration: {stp:.3f}, ease: "sine.inOut", yoyo: true, repeat: {n - 1}, immediateRender: false}}, {t0:.3f});')
    js(f'tl.to("#creef", {{rotation: 0, y: 0, duration: .12}}, {t1:.3f});')
    pose(t1, end, flip=end_flip)
    sfx("swish", t0)


def cree_hop(t, h=70, n=1, period=.36):
    for k in range(n):
        tk = t + k * period
        js(f'tl.fromTo("#creeb", {{y: 0, scaleY: 1, scaleX: 1}}, {{keyframes: [{{scaleY: .86, scaleX: 1.1, y: 10, duration: .07}}, '
           f'{{scaleY: 1.08, scaleX: .94, y: {-h}, duration: .14, ease: "power2.out"}}, {{scaleY: 1, scaleX: 1, y: 0, duration: .13, ease: "power2.in"}}, '
           f'{{scaleY: .92, scaleX: 1.06, y: 0, duration: .04}}, {{scaleY: 1, scaleX: 1, duration: .06}}], immediateRender: false}}, {tk:.3f});')
        js(f'tl.fromTo("#cshadow", {{scale: 1, opacity: 1}}, {{scale: .7, opacity: .5, duration: .21, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false}}, {tk + .07:.3f});')
    sfx("pop", t)


def cree_wiggle(t, n=3, amp=8, period=.22):
    js(f'tl.fromTo("#creeb", {{rotation: 0}}, {{keyframes: [' + ", ".join(f'{{rotation: {amp if k % 2 == 0 else -amp}, duration: {period / 2:.2f}}}' for k in range(n * 2))
       + f', {{rotation: 0, duration: .1}}], immediateRender: false}}, {t:.3f});')


def cree_tilt(t, a, d=.35):
    js(f'tl.to("#creef", {{rotation: {a}, duration: {d}, ease: "back.out(2)"}}, {t:.3f});')


def blink(t):
    js(f'tl.set("#cree .lidg", {{opacity: 1}}, {t:.3f});')
    js(f'tl.set("#cree .lidg", {{opacity: 0}}, {t + .11:.3f});')


def sweat(t, d=1.0):
    js(f'tl.fromTo("#cree .sweat", {{opacity: 0, y: -20, scale: .4}}, {{opacity: 1, y: 0, scale: 1, duration: .25, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#cree .sweat", {{y: 40, duration: {d - .2:.2f}, ease: "power1.in"}}, {t + .25:.3f});')
    js(f'tl.to("#cree .sweat", {{opacity: 0, duration: .1}}, {t + d:.3f});')


def say(t, text, d=.9, left=False):
    """A glass thought bubble by his head (left=True puts it on his other side, for when he stands at the right edge)."""
    js(f'tl.set("#bubt", {{textContent: "{text}"}}, {t - .01:.3f});')
    js(f'tl.set("#bub", {{x: {-560 if left else 0}}}, {t - .01:.3f});')
    js(f'tl.fromTo("#bub", {{opacity: 0, scale: .2, rotation: -30}}, {{opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(2.4)", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#bub", {{opacity: 0, scale: .6, duration: .2, ease: "power2.in"}}, {t + d:.3f});')
    sfx("pop", t)


def sparkle(t, d=1.0, rot=120):
    js(f'tl.fromTo("#cree .csp", {{opacity: 0, scale: .3}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(3)", stagger: .05, immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#cree .csp", {{rotation: "+={rot}", duration: {d}, ease: "none"}}, {t:.3f});')
    js(f'tl.to("#cree .csp", {{opacity: 0, scale: .5, duration: .2, ease: "power2.in"}}, {t + d:.3f});')


def star(sz, col=PINK):
    return (f'<svg viewBox="-50 -50 100 100" width="{sz}" height="{sz}"><path d="M0 -50 C6 -10 10 -6 50 0 C10 6 6 10 '
            f'0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z" fill="{col}"/></svg>')





def P(cx, feet, s=CS):
    """frame position of his body centre from where his feet stand"""
    return (cx, feet - (800 - PCY) * s, s)


