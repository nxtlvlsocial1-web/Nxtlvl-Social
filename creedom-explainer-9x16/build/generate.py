"""Creedom explainer reel, 9:16 (1080x1920). Writes index.html and plan/sfx_events.json.

Owner's brief: an explainer on creedom.ai from the owner's script, paced like the Nxtlvl promo (kinetic word slams,
a word that drops into a coloured pill, floating UI cards, 3D-tilted phone, number counters, logo sting), using the
owner's screen recording of the app where the script needs it, highly interactive from the hook to the end, with the
mascot Cree animated and expressive, colours from the Creedom logo (magenta -> pink -> coral on white/blush), original
music (build/music.py) and an ElevenLabs female voiceover (Hallie, eleven_v3; build/vo_tight.py).
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
A, HIDE, EL, CUES = [], [], [], []
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


def out(sel, t, x=0, y=-80, d=.3, scale=1, blur=12):
    js(f'tl.to("{sel}", {{opacity: 0, x: {x}, y: {y}, scale: {scale}, filter: "blur({blur}px)", duration: {d}, ease: "power2.in"}}, {t:.3f});')


def slam(text, x, y, t, size=150, cls="", w=FW, align="center", t1=None, letters=True):
    """The promo's word slam: letters fly in from blur with their tracking closing in."""
    i = nid("k")
    if letters:
        inner = "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in text)
    else:
        inner = text
    put(f'<div class="slam {cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;text-align:{align};font-size:{size}px">{inner}</div>')
    show(f"#{i}", t - .02, t1)
    if letters:
        n = len(text)
        js(f'tl.fromTo("#{i} .ch", {{opacity: 0, x: (k) => (k - {n / 2}) * 26, y: 40, filter: "blur(10px)"}}, {{opacity: 1, x: 0, y: 0, filter: "blur(0px)", '
           f'duration: .45, ease: "expo.out", stagger: .025, immediateRender: false}}, {t:.3f});')
    else:
        js(f'tl.fromTo("#{i}", {{scale: 1.4, filter: "blur(14px)"}}, {{scale: 1, filter: "blur(0px)", duration: .4, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    return i


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


# ------------------------------------------------------------------------------------------------ pieces
def card(html, x, y, w, t, t1=None, cls="card", rot=0, z=5, enter="fly"):
    i = nid("c")
    put(f'<div class="{cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z};transform:rotate({rot}deg)">{html}</div>')
    show(f"#{i}", t - .01, t1)
    if enter == "fly":
        fly(f"#{i}", t, y=120)
    elif enter == "pop":
        pop(f"#{i}", t, rot=rot)
    elif enter == "left":
        fly(f"#{i}", t, x=-500, y=0, rot=-10)
    elif enter == "right":
        fly(f"#{i}", t, x=500, y=0, rot=10)
    return i


def float_idle(sel, t, t1, amp=10, period=1.6):
    reps = max(1, int((t1 - t) / period))
    js(f'tl.to("{sel}", {{y: "-={amp}", duration: {period / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: {reps}}}, {t + .6:.3f});')


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
        put(f'<div class="cap" id="{i}">{spans}</div>')
        show(f"#{i}", t0, min(t1, W("Comment") - .9))
        js(f'tl.fromTo("#{i}", {{y: 24, opacity: 0}}, {{y: 0, opacity: 1, duration: .18, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
        for k in c:
            tk = VO[k]["s"] - .03
            js(f'tl.set("#{i}w{k}", {{attr: {{class: "cw on"}}}}, {tk:.3f});')
            nxt = VO[k + 1]["s"] - .03 if k + 1 < len(VO) else t1
            if k != c[-1]:
                js(f'tl.set("#{i}w{k}", {{attr: {{class: "cw"}}}}, {nxt:.3f});')


def phone(t, t1, clips, x=320, y=500, w=440, tilt=True):
    """The app on a phone: clips = [(file, start, dur)]; it swoops in tilted and settles flat."""
    h = round(w * 1434 / 660)
    vids = "".join(f'<video id="pv{k}" class="pv" src="assets/video/{f}" data-start="{s:.3f}" data-duration="{d:.3f}" data-track-index="{2 + k}" muted playsinline></video>'
                   for k, (f, s, d) in enumerate(clips))
    put(f'<div id="phone" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="scr">{vids}</div><i class="isl"></i></div>')
    show("#phone", t, t1)
    for k, (f, s, d) in enumerate(clips):
        show(f"#pv{k}", s, s + d)
        js(f'tl.fromTo("#pv{k}", {{scale: 1.06, filter: "blur(6px)"}}, {{scale: 1, filter: "blur(0px)", duration: .3, ease: "power3.out", immediateRender: false}}, {s:.3f});')
    if tilt:
        js(f'tl.fromTo("#phone", {{y: 900, rotationX: 38, rotationY: -18, rotation: -8, scale: .8}}, {{y: 0, rotationX: 0, rotationY: 0, rotation: 0, scale: 1, '
           f'duration: .9, ease: "expo.out", immediateRender: false}}, {t:.3f});')


# ------------------------------------------------------------------------------------------------ the scenes
def scenes():
    t_reel = W("reel")                     # 4.064
    t_up = W("uploaded")
    t_flop = W("flopped")
    t_cr = W("Creedom's")
    t_wat = W("watched")
    t_sec2 = W("second", 2)
    t_it = W("It", 3)               # "and it watched it" come first
    t_hook = W("hook")
    t_ene = W("energy")
    t_drop = W("dropped")
    t_mid = W("middle")
    t_swp = W("swiped")
    t_also = W("also")
    t_new = W("new")
    t_fix = W("fix")
    t_you = W("You")
    t_free = W("free")
    t_audit = W("audit")
    t_acc = W("account")
    t_type = W("type")
    t_hand = W("handle")
    t_20 = W("20")
    t_score = W("score")
    t_100 = W("100")
    t_first = W("first")
    t_fix2 = W("fix", 2)
    t_com = W("Comment")
    t_cree = W("CREE")
    t_send = W("send")
    t_link = W("link")
    S2, S3, S4, S5, S6, S7 = t_up - .25, t_it - .2, t_also - .3, t_you - .25, t_com - .9, VDUR + .05

    # ---- S1 the hook: "This AI told me the exact second people stopped watching my reel."
    js('tl.fromTo("#flash", {opacity: 1}, {opacity: 0, duration: .35, ease: "power2.out", immediateRender: false}, 0);')
    a = slam("THIS AI TOLD ME", 0, 300, W("This"), size=70, cls="dark", t1=S2)
    b = slam("THE EXACT", 0, 390, W("the"), size=130, cls="dark", t1=S2)
    c = slam("SECOND", 0, 515, W("second"), size=190, cls="grad", t1=S2)
    cue(W("second"), "hit")
    js(f'tl.to("#{c}", {{scale: 1.06, duration: .1, yoyo: true, repeat: 1, ease: "power2.out"}}, {W("second") + .4:.3f});')
    # the retention graph: the line runs, then falls off a cliff where people left
    g = nid("g")
    put(f'<div class="card graph" id="{g}" style="left:150px;top:780px;width:780px"><div class="gh"><span class="gt">Retention</span>'
        f'<span class="gp" id="{g}p">100%</span></div>'
        f'<svg viewBox="0 0 700 300" class="gs"><path class="gl0" d="M 0 280 H 700"/>'
        f'<path class="gline" id="{g}l" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M 0 30 C 80 34 160 40 240 52 C 300 60 330 66 360 70 '
        f'C 380 74 395 150 410 230 C 430 250 520 258 700 262"/>'
        f'<circle class="gdot" id="{g}d" cx="372" cy="80" r="16"/></svg>'
        f'<div class="gtag" id="{g}t">0:07 &middot; they left here</div></div>')
    show(f"#{g}", 2.5, S2)
    fly(f"#{g}", 2.5, y=200)
    js(f'tl.fromTo("#{g}l", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 1.4, ease: "power1.inOut", immediateRender: false}}, 2.7);')
    js(f'tl.fromTo("#{g}p", {{textContent: 100}}, {{textContent: 38, duration: 1.4, ease: "power2.in", snap: {{textContent: 1}}, modifiers: {{textContent: (v) => Math.round(v) + "%"}}, '
       f'immediateRender: false}}, 2.7);')
    pop(f"#{g}d", W("stopped") - .05, frm=0)
    js(f'tl.to("#{g}d", {{scale: 1.5, opacity: .6, duration: .3, yoyo: true, repeat: 3}}, {W("stopped") + .3:.3f});')
    pop(f"#{g}t", W("stopped") + .05, frm=.4)
    cue(W("stopped") - .05, "alert")
    for k in range(3):                     # people swipe away
        s = nid("sw")
        put(f'<div class="swipe" id="{s}" style="left:{660 + k * 50}px;top:{1010 + k * 60}px">&larr;</div>')
        show(f"#{s}", W("watching") + k * .12, S2)
        js(f'tl.fromTo("#{s}", {{opacity: 0, x: 0}}, {{keyframes: [{{opacity: 1, duration: .1}}, {{x: -520, opacity: 0, duration: .5, ease: "power2.in"}}]}}, '
           f'{W("watching") + k * .12:.3f});')
        cue(W("watching") + k * .12, "swish") if k == 0 else None
    # Cree: pops up waving, points at the graph, then is shocked where people left
    cree_set(0, 860, 1600, .42)
    js(f'tl.fromTo("#cree", {{opacity: 0, y: 1500}}, {{opacity: 1, y: {1300 - PCY}, duration: .6, ease: "back.out(1.6)", immediateRender: false}}, {W("AI") - .1:.3f});')
    cue(W("AI") - .1, "pop")
    cree_wiggle(W("AI") + .4, n=3, amp=8)
    pose(1.55, "think")
    pose(2.6, "point", flip=True)
    pose(W("stopped") - .1, "shock", flip=False)
    cree_face(W("stopped"), "sweat", d=1.2)
    cree_say(W("stopped") + .05, "!", d=1.0)
    cree_hop(W("stopped") - .1, h=40)
    for s in (a, b, c):
        out(f"#{s}", S2 - .3, y=-120)
    out(f"#{g}", S2 - .3, y=200)

    # ---- S2: "I uploaded a reel that flopped into Creedom's Reel Analyzer, and it watched it second by second."
    r = nid("reel")
    put(f'<div class="reel" id="{r}"><div class="rv"><i class="play"></i></div><div class="rm"><b>my_reel.mp4</b>'
        f'<span class="views">312 views <em>&darr; 84%</em></span></div><div class="stampf" id="{r}s">FLOPPED</div></div>')
    show(f"#{r}", S2, t_cr + .5)
    fly(f"#{r}", S2 + .05, y=300, rot=-8)
    cue(S2, "whoosh")
    js(f'tl.to("#{r}", {{rotationX: 65, y: 120, duration: .45, ease: "bounce.out", transformPerspective: 1200}}, {t_flop:.3f});')
    pop(f"#{r}s", t_flop + .05, frm=2.4, d=.3, ease="back.out(2)", rot=-12)
    cue(t_flop + .05, "stamp")
    js(f'tl.to("#{r}", {{rotationX: 0, y: 0, scale: .22, x: 0, opacity: .0, duration: .45, ease: "power3.in"}}, {t_cr + .05:.3f});')
    slam("FLOPPED.", 0, 360, t_flop, size=140, cls="dark", t1=t_cr - .05)
    cree_walk(S2 + .05, t_flop - .1, (860, 1300, .42), (800, 1260, .5), end="sad")
    cree_say(t_flop + .1, "...", d=.9, size=70)
    pose(t_cr, "present")                  # "Creedom's Reel Analyzer": ta-da, towards the phone
    # the app: Creedom's Reel Analyzer
    ch = nid("chip")
    put(f'<div class="chip" id="{ch}"><img src="assets/img/cree.png" alt=""><span>Creedom &middot; <b>Reel Analyzer</b></span></div>')
    show(f"#{ch}", t_cr, S3 - .1)
    pop(f"#{ch}", t_cr, frm=.5)
    cue(t_cr, "pop")
    phone(t_cr - .15, S5 - .15, [("c1_pick.mp4", t_cr - .15, 2.0), ("c2_steps.mp4", t_cr + 1.85, 2.0),
                                 ("c3_score.mp4", S3 - .2, 6.6), ("c4_fixes.mp4", S4 - .2, 4.1)])
    cue(t_cr - .15, "whoosh_big")
    # second by second: a filmstrip of seconds runs past while Cree scans with a magnifier
    fs = nid("fs")
    cells = "".join(f'<span class="fc">0:{k:02d}</span>' for k in range(0, 31))
    put(f'<div class="film" id="{fs}"><div class="fin" id="{fs}i">{cells}</div></div>')
    show(f"#{fs}", t_wat - .1, S3 - .1)
    fly(f"#{fs}", t_wat - .1, y=60)
    js(f'tl.fromTo("#{fs}i", {{x: 0}}, {{x: -2300, duration: {S3 - t_wat:.2f}, ease: "none", immediateRender: false}}, {t_wat - .1:.3f});')
    cree_to(t_wat - .3, 880, 1180, .44, d=.5)
    pose(t_wat, "mag")                     # he inspects the reel second by second
    js(f'tl.fromTo("#creef", {{rotation: 0}}, {{rotation: -6, duration: .45, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, {t_wat + .3:.3f});')
    cue(t_wat, "pop")
    sc = slam("SECOND BY SECOND", 0, 360, t_sec2, size=96, cls="grad", t1=S3 - .1)
    cue(t_sec2, "tick")

    # ---- S3: "It told me my hook worked, but my energy dropped in the middle, and that's exactly where people swiped away."
    hk = card('<div class="pill ok"><svg viewBox="0 0 40 40"><path d="M 9 21 L 17 29 L 32 12" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" '
              'stroke-linejoin="round"/></svg>HOOK WORKED</div>', 40, 470, 360, t_hook, S4 - .2, cls="tag", rot=-6, enter="pop")
    cue(t_hook, "success")
    cree_to(S3, 870, 1280, .42, d=.5)
    pose(S3, "stand")
    pose(t_hook, "cheer")
    cree_hop(t_hook + .05, h=50, n=2)
    pose(t_ene - .2, "think")
    # energy: bars that sag in the middle
    bars = "".join(f'<i class="eb" id="eb{k}" style="height:{h}px"></i>' for k, h in enumerate([150, 170, 160, 175, 165, 150, 140, 150, 165, 170]))
    en = card(f'<div class="et">ENERGY</div><div class="ebars">{bars}</div><div class="edrop" id="edrop">&darr; dropped here</div>', 640, 560, 400, t_ene - .25,
              S4 - .2, cls="card energy", rot=4, enter="right")
    cue(t_ene - .25, "whoosh")
    js('tl.to(["#eb3", "#eb4", "#eb5", "#eb6"], {height: (k) => [70, 34, 26, 58][k], background: "#ff4d6d", duration: .5, ease: "bounce.out", stagger: .05}, '
       f'{t_drop:.3f});')
    pop("#edrop", t_drop + .15, frm=.5)
    cue(t_drop, "drop")
    pose(t_drop, "sad")
    cree_face(t_drop, "sweat", d=1.4)
    js(f'tl.to("#creeb", {{y: 30, scaleY: .9, duration: .25, ease: "power2.out", yoyo: true, repeat: 1}}, {t_drop:.3f});')
    # swiped away: thumbs flick a stack of reels off to the left
    for k in range(4):
        s = nid("sc")
        put(f'<div class="mini" id="{s}" style="left:{90 + k * 24}px;top:{920 + k * 20}px;z-index:{6 + k}"><i class="play"></i></div>')
        show(f"#{s}", t_swp - .6, S4)
        pop(f"#{s}", t_swp - .6 + k * .05, frm=.6)
        js(f'tl.to("#{s}", {{x: -700, rotation: -35, opacity: 0, filter: "blur(10px)", duration: .45, ease: "power3.in"}}, {t_swp + k * .12:.3f});')
        if k % 2 == 0:
            cue(t_swp + k * .12, "swish")
    slam("SWIPED AWAY", 0, 360, t_swp - .1, size=110, cls="dark", t1=S4 - .2)
    pose(t_swp - .05, "shock")
    cree_say(t_swp, "!?", d=.9, size=80)

    # ---- S4: "It also gave me new hooks and showed me what to fix before I post the next one."
    hooks = [("01", "Stanford just open-sourced a real Jarvis"), ("02", "Stop paying for AI assistants"), ("03", "This open-source AI sorts your day")]
    for k, (n, txt) in enumerate(hooks):
        card(f'<div class="hn">HOOK {n}</div><div class="htx">{txt}</div>', 30 + (k % 2) * 20, 430 + k * 175, 330, t_new + k * .18, S5 - .2,
             cls="card hookc", rot=[-5, 3, -2][k], enter="left")
        cue(t_new + k * .18, "pop")
    fx = card('<div class="et">FIX BEFORE YOU POST</div><div class="fxl" id="fx1"><b>&#10003;</b> Caption at 0:12</div>'
              '<div class="fxl" id="fx2"><b>&#10003;</b> Caption at 0:20</div><div class="fxl" id="fx3"><b>&#10003;</b> Save-worthy CTA</div>',
              690, 520, 360, t_fix - .2, S5 - .2, cls="card fixc", rot=4, enter="right")
    for k in range(3):
        fly(f"#fx{k + 1}", t_fix + .1 + k * .25, x=40, y=0, blur=6, d=.35)
        cue(t_fix + .1 + k * .25, "tick")
    slam("NEW HOOKS", 0, 360, t_new, size=110, cls="grad", t1=t_fix - .05)
    slam("WHAT TO FIX", 0, 360, t_fix, size=110, cls="dark", t1=S5 - .2)
    cree_walk(S4, t_new - .1, (870, 1280, .42), (720, 1320, .45))
    pose(t_new, "cheer")
    cree_hop(t_new, h=70, n=3, period=.4)
    pose(t_new + 1.25, "proud")
    pose(t_fix, "point", flip=False)       # "what to fix": at the checklist
    for k in range(10):                    # confetti
        cf = nid("cf")
        put(f'<i class="conf" id="{cf}" style="left:{820 + RND.uniform(-140, 140):.0f}px;top:1100px;background:{["#F515E8", "#F5876C", "#FFC83D", "#54d6a0"][k % 4]}"></i>')
        show(f"#{cf}", t_new, t_new + 1.6)
        js(f'tl.fromTo("#{cf}", {{x: 0, y: 0, rotation: 0}}, {{x: {RND.uniform(-260, 260):.0f}, y: {RND.uniform(-520, -260):.0f}, rotation: {RND.uniform(-600, 600):.0f}, '
           f'duration: 1.5, ease: "power2.out", immediateRender: false}}, {t_new:.3f});')
    cue(t_new, "sparkle")

    # ---- S5: the free account audit
    js(f'tl.fromTo("#wipe", {{scaleY: 0, transformOrigin: "50% 100%"}}, {{scaleY: 1, duration: .32, ease: "power3.in", immediateRender: false}}, {S5 - .3:.3f});')
    js(f'tl.set("#wipe", {{transformOrigin: "50% 0%"}}, {S5 + .02:.3f});')
    js(f'tl.to("#wipe", {{scaleY: 0, duration: .4, ease: "power3.out"}}, {S5 + .03:.3f});')
    HIDE.append("#wipe")
    js(f'tl.set("#wipe", {{opacity: 1}}, {S5 - .3:.3f});')
    js(f'tl.set("#wipe", {{opacity: 0}}, {S5 + .5:.3f});')
    cue(S5 - .3, "whoosh_big")
    f1 = slam("FREE", 0, 330, t_free, size=230, cls="grad", t1=t_type - .3)
    f2 = slam("ACCOUNT AUDIT", 0, 560, t_audit, size=110, cls="dark", t1=t_type - .3)
    cue(t_free, "hit")
    js(f'tl.to("#{f1}", {{rotation: -4, scale: 1.08, duration: .12, yoyo: true, repeat: 1}}, {t_acc:.3f});')
    # the audit card
    au = nid("au")
    put(f'<div class="card audit" id="{au}"><div class="ah"><img src="assets/img/cree.png" alt=""><b>Account Audit</b><span class="free">FREE</span></div>'
        f'<div class="inp"><span class="at">@</span><span id="{au}h"></span><i class="caret" id="{au}c"></i></div>'
        f'<div class="btn" id="{au}b">Audit my account</div>'
        f'<div class="ring" id="{au}r"><svg viewBox="0 0 200 200"><circle class="rb" cx="100" cy="100" r="82"/>'
        f'<circle class="rf" id="{au}rf" cx="100" cy="100" r="82" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg>'
        f'<div class="rval"><span id="{au}n">20</span><small id="{au}u">sec</small></div></div>'
        f'<div class="first" id="{au}f"><div class="fl">FIRST THING TO FIX</div><div class="fv">Show the payoff in your first 2 seconds</div></div></div>')
    show(f"#{au}", t_type - .35, S6)
    fly(f"#{au}", t_type - .35, y=300)
    cue(t_type - .35, "whoosh")
    handle = "yourhandle"
    for k in range(len(handle) + 1):
        js(f'tl.set("#{au}h", {{textContent: "{handle[:k]}"}}, {t_hand - .1 + k * .07:.3f});')
    for k in range(0, len(handle), 2):
        cue(t_hand - .1 + k * .07, "type")
    js(f'tl.fromTo("#{au}c", {{opacity: 1}}, {{opacity: 0, duration: .2, repeat: 9, yoyo: true, ease: "steps(1)", immediateRender: false}}, {t_type - .3:.3f});')
    js(f'tl.fromTo("#{au}b", {{scale: 1}}, {{keyframes: [{{scale: .92, duration: .08}}, {{scale: 1, duration: .15}}], immediateRender: false}}, {t_20 - .4:.3f});')
    cue(t_20 - .4, "click")
    # the 20-second ring races down, then becomes the score dial
    js(f'tl.to(["#{au} .inp", "#{au}b"], {{opacity: 0, scaleY: .2, duration: .25, ease: "power2.in"}}, {t_20 - .35:.3f});')
    js(f'tl.set(["#{au} .inp", "#{au}b"], {{display: "none"}}, {t_20 - .1:.3f});')
    js(f'tl.set("#{au}r", {{display: "block", opacity: 1}}, {t_20 - .3:.3f});')
    pop(f"#{au}r", t_20 - .3, frm=.5)
    js(f'tl.fromTo("#{au}rf", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: {t_score - t_20 + .2:.2f}, ease: "power1.inOut", immediateRender: false}}, {t_20 - .1:.3f});')
    js(f'tl.fromTo("#{au}n", {{textContent: 20}}, {{textContent: 0, duration: {t_score - t_20 + .2:.2f}, ease: "none", snap: {{textContent: 1}}, immediateRender: false}}, {t_20 - .1:.3f});')
    js(f'tl.set("#{au}u", {{textContent: "/100"}}, {t_score - .02:.3f});')
    js(f'tl.set("#{au}rf", {{strokeDashoffset: 1, stroke: "url(#gr)"}}, {t_score - .02:.3f});')
    js(f'tl.fromTo("#{au}n", {{textContent: 0}}, {{textContent: 78, duration: .9, ease: "power2.out", snap: {{textContent: 1}}, immediateRender: false}}, {t_score:.3f});')
    js(f'tl.fromTo("#{au}rf", {{strokeDashoffset: 1}}, {{strokeDashoffset: .22, duration: .9, ease: "power2.out", immediateRender: false}}, {t_score:.3f});')
    js(f'tl.fromTo("#{au}r", {{scale: 1}}, {{scale: 1.08, duration: .12, yoyo: true, repeat: 1}}, {t_100 + .1:.3f});')
    cue(t_score, "rise")
    cue(t_100 + .1, "ding")
    fly(f"#{au}f", t_first - .1, y=60)
    js(f'tl.set("#{au}f", {{display: "block"}}, {t_first - .12:.3f});')
    cue(t_first - .1, "pop")
    js(f'tl.fromTo("#{au}f", {{boxShadow: "0 0 0 0 rgba(245,21,232,.0)"}}, {{boxShadow: "0 0 0 14px rgba(245,21,232,.25)", duration: .4, yoyo: true, repeat: 2, '
       f'immediateRender: false}}, {t_fix2:.3f});')
    cree_walk(S5 + .05, t_free + .3, (-200, 1380, .42), (840, 1380, .42), end="wave")   # he strolls in under FREE
    pose(t_acc - .1, "proud")
    cree_to(t_type - .45, 930, 640, .34, d=.5)
    pose(t_type - .3, "phone")             # types the handle
    sw = prop('<svg viewBox="0 0 200 220"><circle cx="100" cy="125" r="80" fill="#fff" stroke="#2b1530" stroke-width="14"/>'
              '<rect x="85" y="18" width="30" height="28" rx="6" fill="#2b1530"/><path id="swh" d="M 100 125 L 100 70" stroke="#F515E8" stroke-width="12" '
              'stroke-linecap="round"/></svg>', t_20 - .3, t_score + .2, cls="prop watch")
    js(f'tl.fromTo("#swh", {{rotation: 0, transformOrigin: "100px 125px"}}, {{rotation: 1080, duration: {t_score - t_20 + .3:.2f}, ease: "none", immediateRender: false}}, '
       f'{t_20 - .3:.3f});')
    pose(t_20 - .3, "think")
    cree_wiggle(t_20 - .2, n=4, amp=6, period=.25)
    pose(t_score + .2, "cheer")
    cree_hop(t_100, h=60, n=2)
    pose(t_first - .1, "point", flip=True)  # at "first thing to fix"
    cree_say(t_first, "!", d=.8)

    # ---- S6: the CTA, "Comment "CREE" and I'll send you the link."
    js(f'tl.fromTo("#ctabg", {{opacity: 0, scale: 1.2}}, {{opacity: 1, scale: 1, duration: .45, ease: "power3.out", immediateRender: false}}, {S6:.3f});')
    HIDE.append("#ctabg")
    cue(S6, "whoosh_big")
    cree_to(S6, 540, 820, .95, d=.7, ease="back.out(1.4)")
    pose(S6, "wave", flip=False)
    cree_wiggle(S6 + .7, n=4, amp=9)
    pose(t_cree - .15, "phone")            # he types CREE himself
    k1 = slam("COMMENT", 0, 1180, t_com, size=120, cls="white", t1=S7)
    cb = nid("cb")
    put(f'<div class="cbar" id="{cb}"><span class="cav"></span><span class="ctx" id="{cb}t"></span><i class="caret dark" id="{cb}c"></i>'
        f'<span class="cpost" id="{cb}p">Post</span><svg class="heart" id="{cb}h" viewBox="0 0 40 36"><path d="M20 34 C 8 25 1 18 1 10 A 9 9 0 0 1 20 6 A 9 9 0 0 1 39 10 '
        f'C 39 18 32 25 20 34 Z" fill="#ff2d6f"/></svg></div>')
    show(f"#{cb}", t_com + .1, S7)
    fly(f"#{cb}", t_com + .1, y=200)
    for k in range(5):
        js(f'tl.set("#{cb}t", {{textContent: "{"CREE"[:k]}"}}, {t_cree + k * .16:.3f});')
        if k:
            cue(t_cree + k * .16, "type")
    js(f'tl.fromTo("#{cb}p", {{scale: 1}}, {{keyframes: [{{scale: .85, duration: .08}}, {{scale: 1.1, duration: .15}}, {{scale: 1, duration: .1}}], immediateRender: false}}, '
       f'{t_cree + .8:.3f});')
    pop(f"#{cb}h", t_cree + .85, frm=0, ease="back.out(3)")
    cue(t_cree + .85, "pop")
    # I'll send you the link: a paper plane flies out with a dotted trail, the DM lands
    pl = nid("pl")
    put(f'<svg class="plane" id="{pl}" viewBox="0 0 100 100"><path d="M 5 45 L 95 8 L 62 92 L 46 60 Z" fill="#fff"/><path d="M 46 60 L 95 8" stroke="#F54BA8" '
        f'stroke-width="5"/></svg>')
    show(f"#{pl}", t_send - .2, S7)
    js(f'tl.fromTo("#{pl}", {{x: 0, y: 0, rotation: -10, scale: .5}}, {{x: 560, y: -900, rotation: 18, scale: 1.1, duration: .9, ease: "power2.in", immediateRender: false}}, '
       f'{t_send - .2:.3f});')
    cue(t_send - .2, "whoosh")
    dm = card('<div class="dmh"><img src="assets/img/cree.png" alt=""><b>Creedom</b></div><div class="dmt">Here\'s your link &#128279;</div>', 560, 300, 440,
              t_link - .05, S7, cls="card dm", rot=3, enter="pop")
    cue(t_link - .05, "notify")
    pose(t_send - .25, "point", flip=False)  # the plane goes up and right
    pose(t_link - .05, "cheer")
    cree_say(t_link, "♥", d=.8)
    cree_hop(t_link + .1, h=80, n=2)

    # ---- S7: the logo
    js(f'tl.fromTo("#logo", {{opacity: 0}}, {{opacity: 1, duration: .3, ease: "power2.out", immediateRender: false}}, {S7:.3f});')
    HIDE.append("#logo")
    js(f'tl.set("#cree", {{opacity: 0}}, {S7 + .1:.3f});')
    js(f'tl.fromTo("#lgm", {{scale: 0, rotation: -40, y: 80}}, {{scale: 1, rotation: 0, y: 0, duration: .6, ease: "back.out(2)", immediateRender: false}}, {S7 + .05:.3f});')
    js(f'tl.fromTo("#lgw", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", duration: .55, ease: "power3.out", immediateRender: false}}, {S7 + .3:.3f});')
    js(f'tl.fromTo("#lgt", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: .4, ease: "power3.out", immediateRender: false}}, {S7 + .7:.3f});')
    js(f'tl.fromTo("#lgm", {{rotation: 0}}, {{keyframes: [{{rotation: 10, duration: .14}}, {{rotation: -8, duration: .14}}, {{rotation: 6, duration: .12}}, '
       f'{{rotation: 0, duration: .1}}], immediateRender: false}}, {S7 + .7:.3f});')
    cue(S7 + .05, "logo")
    for k in range(8):
        sp = nid("sp")
        ang = k / 8 * 6.283
        put(f'<svg class="spk" id="{sp}" viewBox="-50 -50 100 100" style="left:{540 + math.cos(ang) * 60 - 30:.0f}px;top:{860 + math.sin(ang) * 60 - 30:.0f}px">'
            f'<path d="M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z" fill="{["#F515E8", "#F5876C", "#FFC83D"][k % 3]}"/></svg>')
        show(f"#{sp}", S7 + .3, DUR)
        js(f'tl.fromTo("#{sp}", {{x: 0, y: 0, scale: 0}}, {{x: {math.cos(ang) * 330:.0f}, y: {math.sin(ang) * 240:.0f}, scale: 1, opacity: 0, duration: 1.1, '
           f'ease: "power2.out", immediateRender: false}}, {S7 + .3:.3f});')

    # Cree idles: a slow bob and a blink every couple of seconds the whole way
    js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -10, duration: .8, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .8)}, immediateRender: false}}, 0);')
    for tb in [1.2, 2.2, 6.9, 8.0, 9.3, 12.95, 15.2, 20.4, 23.4, 26.0, 30.8, 33.0]:   # only while an open-eyed pose shows
        cree_face(tb, "blink")


CSS = f"""
@font-face {{ font-family: "Outfit"; font-weight: 600; src: url("assets/fonts/Outfit-600.woff2"); }}
@font-face {{ font-family: "Outfit"; font-weight: 800; src: url("assets/fonts/Outfit-800.woff2"); }}
@font-face {{ font-family: "Outfit"; font-weight: 900; src: url("assets/fonts/Outfit-900.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/Inter-700.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #fff6fb; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #fff6fb; font-family: "Outfit"; color: #1d0f24; }}
#bg {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(245,75,168,.22) 2px, transparent 2.5px); background-size: 46px 46px; }}
.blob {{ position: absolute; width: 900px; height: 900px; border-radius: 50%; filter: blur(110px); opacity: .32; }}
.slam {{ position: absolute; opacity: 0; font-weight: 900; line-height: .95; letter-spacing: -.02em; white-space: nowrap; z-index: 8; }}
.slam .ch {{ display: inline-block; }}
.slam.dark {{ color: #1d0f24; }}
.slam.white {{ z-index: 22; color: #fff; text-shadow: 0 8px 30px rgba(120,0,80,.35); }}
.slam.grad .ch {{ background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; filter: drop-shadow(0 8px 18px rgba(245,21,232,.25)); }}
.card {{ position: absolute; opacity: 0; background: #fff; border-radius: 34px; padding: 28px 30px; box-shadow: 0 24px 60px rgba(150,20,100,.16), 0 4px 14px rgba(150,20,100,.08);
  border: 1.5px solid rgba(245,75,168,.14); }}
.graph .gh {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; }}
.gt {{ font: 800 40px/1 "Outfit"; color: #1d0f24; }}
.gp {{ font: 900 56px/1 "Outfit"; background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.gs {{ width: 100%; height: 300px; overflow: visible; }}
.gl0 {{ stroke: #f1dbe8; stroke-width: 4; }}
.gline {{ fill: none; stroke: url(#gr); stroke-width: 12; stroke-linecap: round; stroke-linejoin: round; }}
.gdot {{ fill: #ff2d55; opacity: 0; transform-box: fill-box; transform-origin: center; }}
.gtag {{ position: absolute; left: 330px; top: 92px; opacity: 0; background: #1d0f24; color: #fff; font: 800 30px/1 "Outfit"; padding: 14px 20px; border-radius: 16px; }}
.swipe {{ position: absolute; opacity: 0; font: 900 90px/1 "Outfit"; color: #ff2d55; z-index: 9; }}
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
#bub {{ position: absolute; left: 560px; top: 20px; width: 200px; height: 170px; opacity: 0; background: #fff; border-radius: 50% 50% 50% 12px;
  box-shadow: 0 14px 30px rgba(150,20,100,.2); display: grid; place-items: center; transform-origin: 0 100%; }}
#bubt {{ font: 900 96px/1 "Outfit"; color: #F515E8; }}
.prop {{ position: absolute; opacity: 0; transform-origin: 50% 80%; }}
.prop.watch {{ left: 40px; top: 110px; width: 230px; height: 250px; }}
.prop svg {{ width: 100%; height: 100%; }}
.reel {{ position: absolute; left: 290px; top: 560px; width: 500px; opacity: 0; z-index: 7; background: #fff; border-radius: 34px; overflow: hidden;
  box-shadow: 0 30px 70px rgba(150,20,100,.22); transform-origin: 50% 100%; }}
.rv {{ height: 560px; background: linear-gradient(160deg,#3a2140,#7a3060 60%,#c0567a); display: grid; place-items: center; }}
.play {{ display: block; width: 0; height: 0; border-left: 70px solid rgba(255,255,255,.9); border-top: 44px solid transparent; border-bottom: 44px solid transparent; margin-left: 20px; }}
.rm {{ padding: 22px 28px 26px; display: flex; flex-direction: column; gap: 6px; }}
.rm b {{ font: 800 36px/1.1 "Outfit"; }}
.views {{ font: 600 32px/1.1 "Outfit"; color: #7b6a80; }}
.views em {{ font-style: normal; color: #ff2d55; font-weight: 800; }}
.stampf {{ position: absolute; left: 60px; top: 220px; opacity: 0; font: 900 96px/1.1 "Outfit"; color: #ff2d55; border: 10px solid #ff2d55; border-radius: 18px;
  padding: 0 24px; background: rgba(255,255,255,.85); }}
.chip {{ position: absolute; left: 0; right: 0; margin: 0 auto; top: 245px; width: max-content; opacity: 0; z-index: 9; display: flex; align-items: center; gap: 16px;
  background: #fff; border-radius: 999px; padding: 12px 34px 12px 14px; box-shadow: 0 14px 34px rgba(150,20,100,.18); font: 600 40px/1 "Outfit"; }}
.chip img {{ width: 64px; height: 64px; object-fit: contain; }}
.chip b {{ font-weight: 900; background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; }}
#phone {{ position: absolute; opacity: 0; z-index: 6; border-radius: 76px; background: #160b18; padding: 16px; box-shadow: 0 50px 110px rgba(120,10,80,.32), 0 0 0 4px #3a2a3c inset;
  transform-style: preserve-3d; perspective: 1400px; }}
#phone .scr {{ position: relative; width: 100%; height: 100%; border-radius: 62px; overflow: hidden; background: #fff; }}
.pv {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; }}
.isl {{ position: absolute; left: 50%; top: 30px; width: 150px; height: 42px; margin-left: -75px; border-radius: 22px; background: #000; }}
.film {{ position: absolute; left: 0; top: 560px; width: {FW}px; height: 70px; opacity: 0; z-index: 4; overflow: visible; }}
.fin {{ display: flex; gap: 14px; padding-left: 40px; }}
.fc {{ flex: 0 0 auto; width: 140px; height: 70px; border-radius: 16px; background: #1d0f24; color: #fff; font: 800 30px/70px "Outfit"; text-align: center; }}
.film .fc:nth-child(3n) {{ background: linear-gradient(90deg,#F515E8,#F5876C); }}
.tag {{ position: absolute; opacity: 0; z-index: 9; }}
.pill {{ display: inline-flex; align-items: center; gap: 14px; font: 900 44px/1 "Outfit"; color: #fff; padding: 22px 30px; border-radius: 999px;
  box-shadow: 0 16px 34px rgba(0,0,0,.18); }}
.pill.ok {{ background: #18b26b; }}
.pill svg {{ width: 48px; height: 48px; }}
.energy .et, .fixc .et {{ font: 900 30px/1 "Outfit"; letter-spacing: .08em; color: #7b6a80; margin-bottom: 16px; }}
.ebars {{ display: flex; align-items: flex-end; gap: 12px; height: 180px; }}
.eb {{ display: block; flex: 1; border-radius: 10px; background: linear-gradient(180deg,#F515E8,#F5876C); }}
.edrop {{ opacity: 0; margin-top: 14px; font: 900 34px/1 "Outfit"; color: #ff2d55; text-align: center; }}
.mini {{ position: absolute; opacity: 0; width: 200px; height: 330px; border-radius: 26px; background: linear-gradient(160deg,#3a2140,#a2406e); display: grid; place-items: center;
  box-shadow: 0 18px 40px rgba(0,0,0,.25); }}
.mini .play {{ border-left-width: 40px; border-top-width: 26px; border-bottom-width: 26px; margin-left: 12px; }}
.hookc {{ padding: 22px 24px; z-index: 9; }}
.hn {{ font: 900 26px/1 "Outfit"; letter-spacing: .1em; background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; margin-bottom: 10px; }}
.htx {{ font: 800 34px/1.15 "Outfit"; color: #1d0f24; }}
.fixc {{ z-index: 9; }}
.fxl {{ opacity: 0; font: 800 34px/1.2 "Outfit"; padding: 10px 0; display: flex; gap: 14px; align-items: center; }}
.fxl b {{ display: inline-grid; place-items: center; width: 44px; height: 44px; border-radius: 50%; background: #18b26b; color: #fff; font-size: 26px; }}
.conf {{ position: absolute; opacity: 0; width: 22px; height: 34px; border-radius: 6px; z-index: 21; }}
#wipe {{ position: absolute; inset: 0; z-index: 30; opacity: 0; background: {GRAD}; }}
.audit {{ left: 90px; top: 700px; width: 900px; padding: 40px 44px; z-index: 7; }}
.inp, .btn {{ overflow: hidden; }}
.ah {{ display: flex; align-items: center; gap: 18px; font: 900 48px/1 "Outfit"; }}
.ah img {{ width: 84px; height: 84px; object-fit: contain; }}
.free {{ margin-left: auto; font: 900 30px/1 "Outfit"; color: #fff; background: {GRAD}; padding: 12px 22px; border-radius: 999px; }}
.inp {{ margin-top: 32px; height: 110px; border-radius: 28px; background: #fbeef6; border: 3px solid #f6cfe4; display: flex; align-items: center; padding: 0 34px;
  font: 800 52px/1 "Outfit"; color: #1d0f24; }}
.at {{ color: #F515E8; margin-right: 6px; }}
.caret {{ display: inline-block; width: 5px; height: 60px; background: #F515E8; margin-left: 4px; }}
.btn {{ margin-top: 22px; height: 100px; border-radius: 28px; background: {GRAD}; color: #fff; font: 900 44px/100px "Outfit"; text-align: center;
  box-shadow: 0 16px 34px rgba(245,21,232,.3); }}
.ring {{ position: relative; width: 300px; height: 300px; margin: 30px auto 0; opacity: 0; display: none; }}
.ring svg {{ width: 100%; height: 100%; }}
.rb {{ fill: none; stroke: #f6dcea; stroke-width: 22; }}
.rf {{ fill: none; stroke: #1d0f24; stroke-width: 22; stroke-linecap: round; }}
.rval {{ position: absolute; inset: 0; display: flex; align-items: baseline; justify-content: center; padding-top: 92px; }}
.rval span {{ font: 900 110px/1 "Outfit"; color: #1d0f24; }}
.rval small {{ font: 800 40px/1 "Outfit"; color: #7b6a80; margin-left: 4px; }}
.first {{ display: none; opacity: 0; margin-top: 26px; border-radius: 26px; padding: 24px 28px; background: #fff3fa; border: 3px solid #F54BA8; }}
.fl {{ font: 900 28px/1 "Outfit"; letter-spacing: .1em; color: #F515E8; margin-bottom: 10px; }}
.fv {{ font: 800 40px/1.15 "Outfit"; }}
#ctabg {{ position: absolute; inset: 0; z-index: 15; opacity: 0; background: radial-gradient(circle at 50% 40%, #ff7ad9 0%, #F515E8 40%, #c4128f 100%); }}
#ctabg::after {{ content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.25) 2px, transparent 2.5px); background-size: 46px 46px; }}
.cbar {{ position: absolute; left: 90px; top: 1340px; width: 900px; height: 130px; opacity: 0; z-index: 22; background: #fff; border-radius: 999px; display: flex;
  align-items: center; padding: 0 26px; gap: 20px; box-shadow: 0 24px 50px rgba(80,0,60,.3); }}
.cav {{ width: 84px; height: 84px; border-radius: 50%; background: url(assets/img/cree.png) center/86% no-repeat, #ffe3f3; flex: 0 0 auto; }}
.ctx {{ font: 900 64px/1 "Outfit"; color: #1d0f24; letter-spacing: .04em; }}
.caret.dark {{ background: #1d0f24; height: 64px; }}
.cpost {{ margin-left: auto; font: 900 44px/1 "Outfit"; color: #F515E8; }}
.heart {{ position: absolute; right: -40px; top: -96px; width: 110px; height: 100px; opacity: 0; }}
.plane {{ position: absolute; left: 700px; top: 1320px; width: 120px; height: 120px; opacity: 0; z-index: 23; filter: drop-shadow(0 10px 18px rgba(80,0,60,.35)); }}
.dm {{ z-index: 22; padding: 22px 26px; }}
.dmh {{ display: flex; align-items: center; gap: 12px; font: 900 34px/1 "Outfit"; }}
.dmh img {{ width: 56px; height: 56px; object-fit: contain; }}
.dmt {{ margin-top: 12px; font: 800 38px/1.2 "Outfit"; color: #1d0f24; }}
.cap {{ position: absolute; left: 60px; right: 60px; top: 1500px; opacity: 0; text-align: center; z-index: 25; font: 800 54px/1.25 "Outfit"; color: #1d0f24; }}
.cw {{ display: inline-block; padding: 2px 14px 6px; border-radius: 16px; }}
.cw.on {{ background: {GRAD}; color: #fff; box-shadow: 0 10px 22px rgba(245,21,232,.3); }}
#logo {{ position: absolute; inset: 0; z-index: 40; opacity: 0; background: #fff; }}
#lgm {{ position: absolute; left: 80px; top: 720px; width: 260px; height: 260px; object-fit: contain; }}
#lgw {{ position: absolute; left: 350px; top: 775px; font: 800 150px/1 "Outfit"; letter-spacing: -.02em; background: linear-gradient(90deg,#F515E8,#F5876C);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-bottom: 16px; }}
#lgt {{ position: absolute; left: 0; right: 0; top: 1020px; text-align: center; font: 600 46px/1.2 "Outfit"; color: #7b6a80; opacity: 0; }}
.spk {{ position: absolute; width: 60px; height: 60px; z-index: 41; opacity: 0; }}
#flash {{ position: absolute; inset: 0; z-index: 50; background: #fff; opacity: 0; }}
"""


def main():
    scenes()
    caption_track()
    blobs = "".join(f'<i class="blob" style="left:{x}px;top:{y}px;background:{c}"></i>' for x, y, c in [(-300, -200, "#F515E8"), (500, 1100, "#F5876C"), (400, 300, "#ffb3e6")])
    for k, (x, y) in enumerate([(220, 260), (-200, -240), (-160, 180)]):
        js(f'tl.to(".blob:nth-child({k + 1})", {{x: {x}, y: {y}, duration: {DUR:.1f}, ease: "sine.inOut"}}, 0);')
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
      <div id="blobs">{blobs}</div><div id="bg"></div>
      {"".join(EL)}
      <div id="ctabg"></div>
      {cree}
      <div id="wipe"></div>
      <div id="logo"><img id="lgm" src="assets/img/cree.png" alt="Cree"><div id="lgw">Creedom</div><div id="lgt">creedom.ai</div></div>
      <div id="flash"></div>
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
