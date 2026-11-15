"""Creators 100X: the "write me a script" reel as a 2D paper cut-out story (1080x1920, 30 fps).

Owner's picks: "can't it be a visual storytelling concept in 2D": paper cut-out look, a new story-led script.
Story (plan/script.json, on our arc: hook dropped mid-story at Riya's low point, first peak by ~5 s):
  1 desk     Riya, a beginner creator, stares at her phone: 200 views. Again.
  2 wall     zoom out: her reel is one of a wall of identical AI reels ("Hey guys! Level up...")
  3 laptop   what she typed, letter tiles: "write me a reel script"; a little paper robot (the AI) pops out with a
             generic scroll, stamped GENERIC
  4 puzzle   a lightbulb; four puzzle pieces fly in and snap into a 2x2 board, one per part of the prompt
  5 payoff   the robot, happy now, unrolls a script that sounds like her; she reads it and smiles
  6 pop      the wall again; her next reel pops out of it in colour, hearts and comments
  7 CTA      Comment "PROMPT": she holds up the PDF, the robot waves
Look: brand colours (brands/creators-100x: off-white, lime, hot pink, ink) as coloured papers; every piece is hand-cut
(jittered polygon edges), sits on a soft drop shadow, the whole frame has a paper grain; motion is stop-motion (eases
stepped to 12 fps, and the characters "boil" a degree or two every other frame). Riya and the robot are ours.
Clock: the VO (build/vo_assemble.py -> plan/words.json, plan/lines.json).
python3 build/generate.py  ->  index.html, plan/edit.json, plan/sfx_events.json
"""
import html as H
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
LINES = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "plan", "lines.json")))}
DUR = round(LINES["r10"]["e"] + 1.6, 1)
INK, PINK, LIME, PAGE, KRAFT = "#101111", "#FD0B68", "#CCFB79", "#FDF4F4", "#D8B98C"
SKIN, SKIN_D, HAIR, BOTW, BOTG = "#C68A63", "#A86F4B", "#1B1514", "#F4F1EE", "#D9D3CE"
SHADOW = "rgba(60,30,30,.26)"
A, SFX, BODY, CAPS = [], [], [], []
R = random.Random(23)


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
    return LINES[f"r{i:02d}"][key]


def st(d):
    """stop-motion ease: d seconds stepped at 12 fps"""
    return f"steps({max(1, round(d * 12))})"


# ---------------------------------------------------------------- hand-cut paper shapes (SVG)
def jit(v, a):
    return v + R.uniform(-a, a)


def poly(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def cut_rect(x, y, w, h, r=0, a=1.6, step=34):
    """a rectangle cut by hand: points along the edges, each nudged; rounded corners as short arcs"""
    pts = []
    r = min(r, w / 2, h / 2)

    def edge(x0, y0, x1, y1):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            t = i / n
            pts.append((jit(x0 + (x1 - x0) * t, a), jit(y0 + (y1 - y0) * t, a)))

    def arc(cx, cy, a0):
        for k in range(4):
            ang = math.radians(a0 + k * 22.5)
            pts.append((jit(cx + r * math.cos(ang), a * .6), jit(cy + r * math.sin(ang), a * .6)))

    edge(x + r, y, x + w - r, y)
    if r:
        arc(x + w - r, y + r, -90)
    edge(x + w, y + r, x + w, y + h - r)
    if r:
        arc(x + w - r, y + h - r, 0)
    edge(x + w - r, y + h, x + r, y + h)
    if r:
        arc(x + r, y + h - r, 90)
    edge(x, y + h - r, x, y + r)
    if r:
        arc(x + r, y + r, 180)
    return poly(pts)


def cut_ellipse(cx, cy, rx, ry, a=1.4, n=40):
    return poly([(jit(cx + rx * math.cos(2 * math.pi * k / n), a), jit(cy + ry * math.sin(2 * math.pi * k / n), a)) for k in range(n)])


class Paper:
    """collects shapes; renders them twice: an offset shadow layer, then the coloured paper"""

    def __init__(self, dx=7, dy=9):
        self.items, self.dx, self.dy = [], dx, dy

    def add(self, kind, fill, *args, extra="", **kw):
        if kind == "rect":
            pts = cut_rect(*args, **kw)
        elif kind == "ell":
            pts = cut_ellipse(*args, **kw)
        else:
            pts = args[0]
        self.items.append((pts, fill, extra))
        return self

    def raw(self, svg):
        self.items.append((None, None, svg))
        return self

    def svg(self, shadow=True):
        sh = "".join(f'<polygon points="{p}"/>' for p, f, e in self.items if p) if shadow else ""
        body = "".join((f'<polygon points="{p}" fill="{f}" {e}/>' if p else e) for p, f, e in self.items)
        return (f'<g transform="translate({self.dx},{self.dy})" fill="{SHADOW}">{sh}</g>' if shadow else "") + body


def riya(mouth="sad", arm="phone"):
    """Riya, upper body (viewBox 600x820). ids: rh head group, ry eyes, rlid lids, mouths rm_sad/rm_smile/rm_open,
    rarm right arm group (pivot at the shoulder)"""
    # hair behind the head: a bob
    hb = Paper()
    hb.add("raw", None, cut_rect(155, 200, 290, 215, r=110))
    hb.items[-1] = (hb.items[-1][0], HAIR, "")
    body = Paper()
    body.add("rect", LIME, 130, 470, 340, 360, r=90)            # top
    body.add("rect", "#B8E86A", 260, 470, 80, 40, r=20)         # collar shade
    body.add("rect", SKIN, 268, 395, 64, 95, r=24)              # neck
    head = Paper()
    head.add("ell", SKIN, 300, 300, 112, 122)
    head.add("ell", SKIN, 190, 318, 18, 26)                     # ears
    head.add("ell", SKIN, 410, 318, 18, 26)
    head.add("ell", PINK, 190, 352, 9, 9)                       # earrings
    head.add("ell", PINK, 410, 352, 9, 9)
    head.add("raw", None, cut_rect(186, 168, 228, 92, r=46))   # bangs
    head.items[-1] = (head.items[-1][0], HAIR, "")
    head.add("ell", "#F28AA8", 246, 352, 18, 11, extra='opacity=".7"')   # cheeks
    head.add("ell", "#F28AA8", 354, 352, 18, 11, extra='opacity=".7"')
    face = (f'<g id="ry"><ellipse cx="262" cy="318" rx="10" ry="14" fill="{INK}"/><ellipse cx="338" cy="318" rx="10" ry="14" fill="{INK}"/>'
            f'<circle cx="265" cy="313" r="3.5" fill="#fff"/><circle cx="341" cy="313" r="3.5" fill="#fff"/></g>'
            f'<g id="rlid" transform="translate(0,318) scale(1,0) translate(0,-318)"><rect x="246" y="300" width="32" height="34" rx="14" fill="{SKIN}"/>'
            f'<rect x="322" y="300" width="32" height="34" rx="14" fill="{SKIN}"/></g>'
            f'<path id="rb_sad" d="M244 286 L276 280 M324 280 L356 286" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<path id="rb_up" d="M244 280 Q260 270 278 276 M322 276 Q340 270 356 280" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none" opacity="0"/>'
            f'<path id="rm_sad" d="M276 378 Q300 362 324 378" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none" opacity="{1 if mouth == "sad" else 0}"/>'
            f'<path id="rm_smile" d="M270 362 Q300 396 330 362 Z" fill="{INK}" opacity="{1 if mouth == "smile" else 0}"/>'
            f'<ellipse id="rm_open" cx="300" cy="372" rx="14" ry="17" fill="{INK}" opacity="{1 if mouth == "open" else 0}"/>')
    # arm: upper arm + forearm + hand, pivot at the right shoulder (440, 520)
    arm_p = Paper()
    arm_p.add("rect", LIME, 410, 500, 70, 170, r=34)
    arm_p.add("rect", SKIN, 418, 620, 54, 150, r=27)
    arm_p.add("ell", SKIN, 445, 780, 34, 32)
    larm = Paper()
    larm.add("rect", LIME, 118, 500, 70, 170, r=34)
    larm.add("rect", SKIN, 126, 620, 54, 150, r=27)
    larm.add("ell", SKIN, 152, 780, 34, 32)
    return (f'<svg class="riya" viewBox="0 0 600 820"><g class="boil">{hb.svg()}<g id="rlarm" style="transform-origin:150px 520px">{larm.svg()}</g>{body.svg()}'
            f'<g id="rh" style="transform-origin:300px 420px">{head.svg()}{face}</g>'
            f'<g id="rarm" style="transform-origin:445px 520px">{arm_p.svg()}</g></g></svg>')


def robot():
    """the AI: a paper robot (viewBox 320x420). ids: be_n neutral eyes, be_h happy eyes, bm mouth, barmL/barmR arms"""
    p = Paper()
    p.add("rect", BOTG, 150, 18, 20, 60, r=8)                   # antenna stick
    p.add("ell", PINK, 160, 22, 20, 20)
    p.add("rect", BOTW, 40, 70, 240, 170, r=40)                 # head
    p.add("rect", INK, 66, 96, 188, 118, r=26)                  # screen
    p.add("rect", BOTW, 84, 238, 152, 130, r=30)                # body
    p.add("ell", PINK, 160, 300, 22, 20)                        # chest light
    p.add("rect", BOTG, 100, 362, 44, 40, r=14)                 # feet
    p.add("rect", BOTG, 176, 362, 44, 40, r=14)
    eyes = (f'<g id="be_n"><rect x="104" y="128" width="30" height="40" rx="10" fill="{LIME}"/><rect x="186" y="128" width="30" height="40" rx="10" fill="{LIME}"/></g>'
            f'<g id="be_h" opacity="0"><path d="M100 160 Q119 128 138 160 M182 160 Q201 128 220 160" stroke="{LIME}" stroke-width="10" fill="none" stroke-linecap="round"/></g>'
            f'<path id="bm" d="M140 190 Q160 200 180 190" stroke="{LIME}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    al, ar = Paper(), Paper()
    al.add("rect", BOTG, 46, 250, 40, 100, r=20)
    ar.add("rect", BOTG, 234, 250, 40, 100, r=20)
    return (f'<svg class="bot" viewBox="0 0 320 420"><g class="boil"><g class="barmL" style="transform-origin:66px 260px">{al.svg()}</g>'
            f'<g class="barmR" style="transform-origin:254px 260px">{ar.svg()}</g>{p.svg()}{eyes}</g></svg>')


def phone_svg(color=False):
    p = Paper(5, 7)
    p.add("rect", INK, 0, 0, 200, 340, r=30)
    p.add("rect", "#ffffff" if not color else PAGE, 12, 14, 176, 312, r=20)
    return f'<svg class="phs" viewBox="-4 -4 214 356">{p.svg()}</svg>'


def torn_strip(text_html, cls="", sid=""):
    """a torn paper strip label (white paper, black type) with a matching shadow"""
    return f'<div class="strip {cls}" id="{sid}"><i class="ssh"></i><b>{text_html}</b></div>'


def scene(sid, bg, inner, z):
    """a full-frame scene card on coloured paper with a torn top edge (so cards visibly stack)"""
    top = [(0, 40)] + [(x, jit(16, 12)) for x in range(30, FW, 30)] + [(FW, 40), (FW, FH), (0, FH)]
    clip = "polygon(" + ",".join(f"{x:.0f}px {y:.0f}px" for x, y in top) + ")"
    BODY.append(f'<div class="scene" id="{sid}" style="z-index:{z}"><div class="sbg" style="background:{bg};clip-path:{clip}"></div>{inner}</div>')


def enter(sid, t, d=.45):
    """the next card slides up over the last one, stop-motion"""
    js(f'tl.fromTo("#{sid}", {{y: {FH}, rotation: 5, opacity: 1}}, {{y: 0, rotation: 0, duration: {d}, ease: "{st(d)}", immediateRender: false}}, {t - d:.3f});')
    sfx("whoosh", t - d, -6)


def leave(sid, t):
    js(f'tl.set("#{sid}", {{opacity: 0}}, {t + .02:.3f});')


def boil(sel, t0, t1, amp=1.2):
    """paper characters wobble a little every other frame"""
    t = t0
    while t < t1:
        org = "160 380" if sel.startswith("#b") else "300 760"
        js(f'tl.set("{sel}", {{svgOrigin: "{org}", rotation: {R.uniform(-amp, amp):.2f}, x: {R.uniform(-1.5, 1.5):.1f}, y: {R.uniform(-1.5, 1.5):.1f}}}, {t:.3f});')
        t += 2 / 12


def pop(sel, t, d=.32, frm=.2, rot=0):
    js(f'tl.fromTo("{sel}", {{scale: {frm}, opacity: 0, rotation: {rot - 12}}}, {{scale: 1, opacity: 1, rotation: {rot}, duration: {d}, ease: "{st(d)}", immediateRender: false}}, {t:.3f});')


def blink(t):
    js(f'tl.fromTo("#rlid", {{scaleY: 0}}, {{scaleY: 1, duration: .08, yoyo: true, repeat: 1, ease: "steps(1)", immediateRender: false}}, {t:.3f});')


def star(x, y, size, color, sid):
    return (f'<svg class="spark" id="{sid}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px" viewBox="0 0 24 24">'
            f'<path d="M12 0c.8 6.6 4.8 10.8 12 12-7.2 1.2-11.2 5.4-12 12-.8-6.6-4.8-10.8-12-12 7.2-1.2 11.2-5.4 12-12z" fill="{color}"/></svg>')


# ---------------------------------------------------------------- scenes
def sc_desk(t0, t1):
    win = Paper()
    win.add("rect", "#ffffff", 80, 470, 330, 360, r=16)
    win.add("rect", INK, 100, 490, 290, 320, r=8)
    win.add("ell", LIME, 300, 580, 46, 46)
    win.add("ell", INK, 320, 566, 40, 40)
    desk = Paper(0, -10)
    desk.add("rect", KRAFT, -20, 1250, 1120, 300, r=0, a=2.5)
    stars = "".join(star(x, y, s, LIME if k % 2 else "#ffffff", f"dsk{k}") for k, (x, y, s) in enumerate([(130, 520, 22), (220, 700, 16), (350, 760, 18)]))
    ph = (f'<div class="dphone" id="dphone">{phone_svg()}<div class="dps"><div class="dpv" id="dpv">200</div><div class="dpl">views</div>'
          f'<div class="dpbar"><i id="dpfill"></i></div></div></div>')
    inner = (f'<svg class="layer" viewBox="0 0 1080 1920">{win.svg()}</svg>{stars}'
             f'<div class="rwrap" id="r1" style="left:200px;top:610px;width:620px">{riya("sad")}</div>'
             f'<svg class="layer" viewBox="0 0 1080 1920" style="z-index:3">{desk.svg()}</svg>{ph}'
             + torn_strip('200 VIEWS. <span class="pk" id="again">AGAIN.</span>', "top", "s1lab")
             + '<div class="sigh" id="sigh">...</div>')
    scene("sc1", PAGE, inner, 1)
    js(f'tl.set("#sc1", {{opacity: 1}}, 0);')
    # frame 0: everything already there; the phone counts up to 200 and stalls
    js(f'tl.fromTo("#s1lab", {{scale: 1.25, rotation: -6}}, {{scale: 1, rotation: -2, duration: .4, ease: "{st(.4)}"}}, 0);')
    js(f'tl.fromTo("#again", {{opacity: 0, scale: 2}}, {{opacity: 1, scale: 1, duration: .25, ease: "{st(.25)}", immediateRender: false}}, {T("again") - .05:.3f});')
    js(f'tl.fromTo("#dphone", {{rotation: -8, y: 0}}, {{rotation: -3, y: -12, duration: 1.0, ease: "{st(1.0)}", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#dpfill", {{scaleX: .05}}, {{scaleX: .16, duration: {T("views") - .2:.3f}, ease: "{st(T("views") - .2)}", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#dphone", {{x: 0}}, {{x: 10, duration: .06, yoyo: true, repeat: 5, ease: "steps(1)", immediateRender: false}}, {T("again"):.3f});')
    js(f'tl.fromTo("#r1 #rh", {{rotation: 0, svgOrigin: "300 420"}}, {{rotation: -9, y: 18, duration: .4, ease: "{st(.4)}", svgOrigin: "300 420", immediateRender: false}}, {T("again"):.3f});')
    js(f'tl.fromTo("#sigh", {{opacity: 0, x: 0, y: 0}}, {{opacity: 1, x: -30, y: -40, duration: .6, ease: "{st(.6)}", immediateRender: false}}, {T("again") + .1:.3f});')
    js(f'tl.fromTo("#r1 #rarm", {{rotation: -132, svgOrigin: "445 520"}}, {{rotation: -128, duration: 1, ease: "{st(1)}", svgOrigin: "445 520", immediateRender: false}}, 0);')
    js(f'tl.set("#r1 #rlarm", {{svgOrigin: "150 520", rotation: 20}}, 0);')
    blink(1.3)
    for k in range(3):
        js(f'tl.fromTo("#dsk{k}", {{scale: .4, opacity: .4}}, {{scale: 1, opacity: 1, duration: .5, yoyo: true, repeat: 3, ease: "steps(3)", immediateRender: false}}, {k * .3:.3f});')
    boil("#r1 .boil", 0, t1)
    sfx("thud", T("again"), -6)
    leave("sc1", t1)


def wall_html(prefix, her_color=False):
    cards = ""
    for i in range(12):
        c, r = i % 4, i // 4
        her = (i == 5)
        cls = "wph her" if her else "wph"
        good = ('<div class="wps nw"><i class="wav"></i><b>Skipping the gym?</b><span>Your workout is too long.</span><em></em><em class="s"></em><u>3 tips, 30 s</u></div>' if her else "")
        cards += (f'<div class="{cls}" id="{prefix}p{i}" style="left:{95 + c * 230}px;top:{420 + r * 345}px">{phone_svg()}'
                  f'<div class="wps"><i class="wav"></i><b>Hey guys!</b><span>Level up your fitness journey...</span><em></em><em class="s"></em><u>5 amazing tips</u></div>{good}</div>')
    return f'<div class="wall" id="{prefix}wall">{cards}</div>'


def sc_wall(t0, t1):
    inner = wall_html("w1") + torn_strip('WRITTEN BY <span class="pk">AI.</span>', "top", "s2lab") + torn_strip('SO WAS <span class="pk">EVERYONE ELSE\'S.</span>', "top b", "s2lab2")
    scene("sc2", "#FFE3EE", inner, 2)
    enter("sc2", t0)
    # zoom out from her phone (card 5) to the whole wall
    js(f'tl.fromTo("#w1wall", {{scale: 2.7, x: -60, y: -260}}, {{scale: 1, x: 0, y: 0, duration: 1.2, ease: "{st(1.2)}", immediateRender: false}}, {t0 + .1:.3f});')
    pop("#s2lab", t0 + .1, rot=-2)
    t_so = T("so", L(1))
    js(f'tl.to("#s2lab", {{opacity: 0, duration: .01}}, {t_so - .05:.3f});')
    pop("#s2lab2", t_so - .05, rot=2)
    js(f'tl.fromTo("#w1wall .wph", {{y: 0}}, {{y: -26, duration: .12, yoyo: true, repeat: 1, stagger: .05, ease: "steps(2)", immediateRender: false}}, {t_so:.3f});')
    for k in range(4):
        sfx("pop", t_so + k * .15, -12)
    leave("sc2", t1)


def sc_laptop(t0, t1):
    lap = Paper()
    lap.add("rect", INK, 120, 600, 840, 540, r=34)
    lap.add("rect", "#ffffff", 150, 630, 780, 480, r=18)
    lap.add("raw", None, poly([(60, 1140), (1020, 1140), (1080, 1230), (0, 1230)]))
    lap.items[-1] = (lap.items[-1][0], LIME, "")
    letters = "write me a reel script"
    tiles = "".join(f'<b class="lt">{H.escape(ch) if ch != " " else "&nbsp;"}</b>' for ch in letters)
    scroll = (f'<div class="scrollA" id="scA"><i class="ssh"></i><div class="sci"><b>Hey guys!</b> Are you ready to level up your fitness journey? '
              f'Here are 5 amazing tips that will totally transform your body!</div><div class="gen" id="gen">GENERIC</div></div>')
    inner = (f'<div class="bwrap" id="b1" style="left:380px;top:300px;width:320px;transform:translateY(360px)">{robot()}</div>'
             f'<svg class="layer" viewBox="0 0 1080 1920" style="z-index:2">{lap.svg()}</svg>'
             f'<div class="pbar" id="pbar">{tiles}<i class="caret" id="caret"></i></div>{scroll}'
             + torn_strip('WHAT EVERY <span class="pk">BEGINNER</span> TYPES', "low", "s3lab"))
    scene("sc3", "#EAF8D5", inner, 3)
    enter("sc3", t0)
    pop("#s3lab", t0 + .1, rot=-2)
    t_w, t_end = T("typed") - .05, T("write") - .1
    js(f'tl.fromTo("#pbar .lt", {{opacity: 0, y: -40, rotation: -20}}, {{opacity: 1, y: 0, rotation: 0, duration: .12, ease: "steps(2)", stagger: {(t_end - t_w) / len(letters):.3f}, immediateRender: false}}, {t_w:.3f});')
    for k in range(len(letters)):
        if letters[k] != " ":
            sfx("key", t_w + k * (t_end - t_w) / len(letters), -4)
    js(f'tl.fromTo("#caret", {{opacity: 1}}, {{opacity: 0, duration: .25, yoyo: true, repeat: 9, ease: "steps(1)", immediateRender: false}}, {t0:.3f});')
    # the robot pops up from behind the screen with a generic scroll
    t_up = t_end + .15
    js(f'tl.fromTo("#b1", {{y: 360}}, {{y: 0, duration: .35, ease: "{st(.35)}", immediateRender: false}}, {t_up:.3f});')
    js(f'tl.fromTo("#scA", {{scaleY: 0, opacity: 0, rotation: 4}}, {{scaleY: 1, opacity: 1, rotation: 3, duration: .4, ease: "{st(.4)}", immediateRender: false}}, {t_up + .3:.3f});')
    pop("#gen", t_up + .75, rot=-10)
    js(f'tl.fromTo("#b1 .barmR", {{rotation: 0, svgOrigin: "254 260"}}, {{rotation: -40, duration: .3, ease: "{st(.3)}", svgOrigin: "254 260", immediateRender: false}}, {t_up + .25:.3f});')
    boil("#b1 .boil", t_up, t1)
    sfx("spring", t_up, -4)
    sfx("stamp", t_up + .75, -4)
    leave("sc3", t1)


PIECES = [("WHO SHE IS", LIME, "3K followers"), ("WHO IT'S FOR", PINK, "skip the gym"), ("THE HOOK", "#ffffff", "a mistake"), ("THE FORMAT", INK, "30 s, 3 tips")]


def piece_icon(i):
    if i == 0:      # mini Riya
        p = Paper(3, 4)
        p.add("rect", HAIR, 50, 30, 100, 90, r=45)
        p.add("ell", SKIN, 100, 78, 40, 44)
        p.add("rect", HAIR, 62, 34, 76, 30, r=15)
        return f'<svg viewBox="0 0 200 170">{p.svg()}<circle cx="86" cy="82" r="5" fill="{INK}"/><circle cx="114" cy="82" r="5" fill="{INK}"/><path d="M88 100 Q100 110 112 100" stroke="{INK}" stroke-width="4" fill="none"/></svg>'
    if i == 1:      # three sleepy people
        p = Paper(3, 4)
        for k, x in enumerate((50, 100, 150)):
            p.add("ell", ["#F6D2B8", SKIN, SKIN_D][k], x, 70, 26, 28)
            p.add("rect", "#ffffff", x - 28, 100, 56, 60, r=22)
        z = "".join(f'<path d="M{x - 12} 70 h10 M{x + 2} 70 h10" stroke="{INK}" stroke-width="4"/>' for x in (50, 100, 150))
        return f'<svg viewBox="0 0 200 170">{p.svg()}{z}<text x="160" y="40" font-size="26" font-weight="800" fill="{INK}">z</text></svg>'
    if i == 2:      # a hook
        return (f'<svg viewBox="0 0 200 170"><path d="M100 10 V95 a34 34 0 1 1 -60 -20" stroke="{SHADOW}" stroke-width="16" fill="none" stroke-linecap="round" transform="translate(4,5)"/>'
                f'<path d="M100 10 V95 a34 34 0 1 1 -60 -20" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M30 68 l14 -16 l6 22 z" fill="{INK}"/></svg>')
    p = Paper(3, 4)    # stopwatch
    p.add("ell", LIME, 100, 95, 58, 58)
    p.add("ell", "#ffffff", 100, 95, 46, 46)
    p.add("rect", LIME, 88, 22, 24, 18, r=6)
    return f'<svg viewBox="0 0 200 170">{p.svg()}<path d="M100 95 V62 M100 95 L122 108" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></svg>'


def sc_puzzle(t0, t1):
    slots = "".join(f'<div class="slot" style="left:{c * 345}px;top:{r * 345}px"><b>{i + 1}</b></div>' for i, (c, r) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]))
    pieces = ""
    for i, (lab, col, sub) in enumerate(PIECES):
        dark = col == INK
        pieces += (f'<div class="pz{" dark" if dark else ""}" id="pz{i}" style="background:{col}"><div class="pzi">{piece_icon(i)}</div>'
                   f'<b>{lab}</b><span>{sub}</span><i class="tab t{i}" style="background:{col}"></i></div>')
    bulb = Paper(3, 4)
    bulb.add("ell", "#FFF27A", 60, 55, 46, 50)
    bulb.add("rect", "#BDB6B0", 40, 98, 40, 30, r=8)
    rays = "".join(f'<path d="M60 55 L{60 + 85 * math.cos(math.radians(a)):.0f} {55 + 85 * math.sin(math.radians(a)):.0f}" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".85"/>'
                   for a in range(-160, 1, 32))
    inner = (f'<div class="board" id="board"><i class="ssh"></i>{slots}</div>{pieces}'
             f'<div class="bwrap" id="b2" style="left:40px;top:1090px;width:270px">{robot()}</div>'
             f'<div class="rwrap" id="r2" style="left:640px;top:1090px;width:420px">{riya("open")}</div>'
             f'<svg class="bulb" id="bulb" viewBox="-40 -40 200 200"><g id="brays">{rays}</g>{bulb.svg()}</svg>'
             + torn_strip('4 PIECES, <span class="pk">NOT 1</span>', "top", "s4lab"))
    scene("sc4", "#FFF6D6", inner, 4)
    enter("sc4", t0)
    pop("#s4lab", t0 + .1, rot=-2)
    t_time = T("time", L(3)) - .1
    pop("#bulb", t_time, rot=6)
    js(f'tl.fromTo("#brays", {{opacity: 0}}, {{opacity: 1, duration: .3, yoyo: true, repeat: 3, ease: "steps(2)", immediateRender: false}}, {t_time + .2:.3f});')
    js(f'tl.fromTo("#r2 #rarm", {{rotation: 0, svgOrigin: "445 520"}}, {{rotation: -150, duration: .3, ease: "{st(.3)}", svgOrigin: "445 520", immediateRender: false}}, {t_time:.3f});')
    sfx("ding", t_time, -4)
    js(f'tl.fromTo("#board", {{scale: .6, opacity: 0, rotation: -6}}, {{scale: 1, opacity: 1, rotation: -1, duration: .4, ease: "{st(.4)}", immediateRender: false}}, {t0 + .25:.3f});')
    # pieces fly in scattered on "four pieces", then each snaps into its slot on its line
    scat = [(-90, 300, -14), (840, 300, 12), (-100, 700, 10), (850, 690, -12)]
    slot_xy = [(180, 330), (525, 330), (180, 675), (525, 675)]
    t_four = T("four") - .05
    for i, (x, y, r) in enumerate(scat):
        js(f'tl.fromTo("#pz{i}", {{x: {x - slot_xy[i][0] + (200 if x > 500 else -300)}, y: {y - slot_xy[i][1]}, rotation: {r * 2}, opacity: 0}}, '
           f'{{x: {x - slot_xy[i][0]}, y: {y - slot_xy[i][1]}, rotation: {r}, opacity: 1, duration: .35, ease: "{st(.35)}", immediateRender: false}}, {t_four + i * .1:.3f});')
        sfx("pop", t_four + i * .1, -10)
    snaps = [T("who", L(4)), T("who", L(5)), T("the", L(6)), T("and", L(7))]
    for i, t in enumerate(snaps):
        js(f'tl.to("#pz{i}", {{x: 0, y: 0, rotation: 0, scale: 1.12, duration: .3, ease: "{st(.3)}"}}, {t:.3f});')
        js(f'tl.to("#pz{i}", {{scale: 1, duration: .15, ease: "steps(2)"}}, {t + .32:.3f});')
        js(f'tl.fromTo("#board", {{x: 0}}, {{x: 8, duration: .05, yoyo: true, repeat: 3, ease: "steps(1)", immediateRender: false}}, {t + .3:.3f});')
        sfx("snap", t + .3, -2)
    js(f'tl.set("#r2 #rm_open", {{opacity: 0}}, {snaps[3] + .4:.3f}); tl.set("#r2 #rm_smile", {{opacity: 1}}, {snaps[3] + .4:.3f});')
    js(f'tl.set("#r2 #rb_sad", {{opacity: 0}}, {t0:.3f}); tl.set("#r2 #rb_up", {{opacity: 1}}, {t0:.3f});')
    js(f'tl.set("#r2 #rm_sad", {{opacity: 0}}, {t0:.3f});')
    blink(t0 + 1.5)
    blink(snaps[2] + .8)
    boil("#b2 .boil", t0, t1)
    boil("#r2 .boil", t0, t1)
    leave("sc4", t1)


GOOD = ["Skipping the gym because you have no time?", "Your workout is too long.", "1. Ten minutes beats zero.", "2. Squats while the kettle boils.",
        "3. Take the stairs, every time."]


def sc_payoff(t0, t1):
    lines = "".join(f'<div class="gl" id="gl{i}">{H.escape(l)}</div>' for i, l in enumerate(GOOD))
    sparks = "".join(star(x, y, s, [PINK, INK, LIME][k % 3], f"pps{k}") for k, (x, y, s) in enumerate([(380, 250, 40), (980, 300, 34), (330, 1060, 30), (1000, 1150, 44), (560, 1320, 28)]))
    inner = (f'<div class="bwrap" id="b3" style="left:30px;top:330px;width:360px">{robot()}</div>'
             f'<div class="scrollB" id="scB"><i class="ssh"></i><div class="scin">{lines}</div><div class="sly" id="sly">SOUNDS LIKE HER</div></div>'
             f'<div class="rwrap" id="r3" style="left:20px;top:900px;width:430px">{riya("smile")}</div>{sparks}')
    scene("sc5", "#E9F9CF", inner, 5)
    enter("sc5", t0)
    js(f'tl.set("#b3 #be_n", {{opacity: 0}}, {t0:.3f}); tl.set("#b3 #be_h", {{opacity: 1}}, {t0:.3f});')
    js(f'tl.set("#r3 #rb_sad, #r3 #rm_sad, #r3 #rm_open", {{opacity: 0}}, {t0:.3f}); tl.set("#r3 #rb_up, #r3 #rm_smile", {{opacity: 1}}, {t0:.3f});')
    js(f'tl.fromTo("#scB", {{scaleY: 0, opacity: 1}}, {{scaleY: 1, duration: .6, ease: "{st(.6)}", immediateRender: false}}, {t0 + .2:.3f});')
    t_l = T("but", L(8))
    js(f'tl.fromTo("#scB .gl", {{opacity: 0, x: -30}}, {{opacity: 1, x: 0, duration: .15, ease: "steps(2)", stagger: .32, immediateRender: false}}, {t_l - .4:.3f});')
    t_like = T("sounded") - .05
    pop("#sly", t_like, d=.3, frm=2.2, rot=-6)
    js(f'tl.fromTo("#b3 .barmL", {{rotation: 0, svgOrigin: "66 260"}}, {{rotation: 30, svgOrigin: "66 260", duration: .25, yoyo: true, repeat: 3, ease: "steps(2)", immediateRender: false}}, {t0 + .3:.3f});')
    js(f'tl.fromTo("#b3 .barmR", {{rotation: 0, svgOrigin: "254 260"}}, {{rotation: -30, svgOrigin: "254 260", duration: .25, yoyo: true, repeat: 3, ease: "steps(2)", immediateRender: false}}, {t0 + .3:.3f});')
    js(f'tl.fromTo("#r3 #rh", {{rotation: 0, svgOrigin: "300 420"}}, {{rotation: 6, duration: .3, yoyo: true, repeat: 3, ease: "steps(2)", svgOrigin: "300 420", immediateRender: false}}, {t_like:.3f});')
    for k in range(5):
        js(f'tl.fromTo("#pps{k}", {{scale: 0, rotation: 0}}, {{scale: 1, rotation: 90, duration: .4, ease: "steps(4)", immediateRender: false}}, {t_like + k * .1:.3f});')
    sfx("ding", t0 + .3, -3)
    sfx("stamp", t_like, -2)
    boil("#b3 .boil", t0, t1)
    boil("#r3 .boil", t0, t1)
    leave("sc5", t1)


def sc_pop(t0, t1):
    hearts = "".join(f'<svg class="heart" id="ht{k}" style="left:{x}px;top:{y}px" viewBox="0 0 24 22"><path d="M12 21s-9-5.6-9-12A5 5 0 0 1 12 6a5 5 0 0 1 9 3c0 6.4-9 12-9 12z" fill="{PINK}"/></svg>'
                     for k, (x, y) in enumerate([(300, 900), (700, 820), (620, 1180), (360, 1260), (780, 1030), (250, 1080)]))
    bubbles = (f'<div class="bub" id="bu0" style="left:70px;top:560px">this is SO me</div>'
               f'<div class="bub" id="bu1" style="left:620px;top:1330px">saving this!</div>')
    inner = wall_html("w2") + hearts + bubbles + torn_strip('DIDN\'T <span class="pk">BLEND IN.</span>', "top", "s6lab")
    scene("sc6", "#FFE3EE", inner, 6)
    enter("sc6", t0, d=.35)
    pop("#s6lab", t0 + .05, rot=-2)
    t_b = T("blend") - .1
    js(f'tl.to("#w2wall .wph:not(.her)", {{opacity: .35, scale: .94, duration: .25, ease: "steps(3)"}}, {t_b:.3f});')
    js(f'tl.fromTo("#w2p5", {{scale: 1, x: 0, y: 0, rotation: 0}}, {{scale: 1.75, x: 210, y: -20, rotation: -4, duration: .35, ease: "{st(.35)}", immediateRender: false}}, {t_b:.3f});')
    js(f'tl.set("#w2p5 .wps:not(.nw)", {{opacity: 0}}, {t_b + .1:.3f}); tl.set("#w2p5 .nw", {{opacity: 1}}, {t_b + .1:.3f});')
    for k in range(6):
        js(f'tl.fromTo("#ht{k}", {{y: 0, scale: 0, opacity: 1}}, {{y: -260, scale: 1, opacity: 0, duration: 1.1, ease: "steps(10)", immediateRender: false}}, {t_b + .15 + k * .1:.3f});')
    pop("#bu0", t_b + .25, rot=-4)
    pop("#bu1", t_b + .45, rot=3)
    sfx("pop", t_b, -2)
    sfx("pop", t_b + .25, -8)
    sfx("pop", t_b + .45, -8)
    leave("sc6", t1)


def sc_cta(t0):
    tiles = "".join(f"<b>{c}</b>" for c in "PROMPT")
    inner = (torn_strip('Comment <span class="pk">"PROMPT"</span>', "cta", "s7lab")
             + f'<div class="cbox" id="cbox"><i class="ssh"></i><i class="cav"></i><span class="ct" id="ct">{tiles}</span><span class="snd" id="snd"></span></div>'
             f'<div class="cov" id="cov"><i class="ssh"></i><img src="assets/img/pdf_cover.png"><div class="free" id="free">FREE PDF</div></div>'
             f'<div class="rwrap" id="r4" style="left:-30px;top:1080px;width:440px">{riya("smile")}</div>'
             f'<div class="bwrap" id="b4" style="left:770px;top:1180px;width:280px">{robot()}</div>')
    scene("sc7", "#EAF8D5", inner, 7)
    enter("sc7", t0)
    pop("#s7lab", t0 + .05, rot=-2)
    js(f'tl.fromTo("#cbox", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: .3, ease: "{st(.3)}", immediateRender: false}}, {t0 + .15:.3f});')
    tp = T("prompt", L(10)) - .1
    js(f'tl.fromTo("#ct b", {{opacity: 0, y: -30}}, {{opacity: 1, y: 0, duration: .08, ease: "steps(1)", stagger: .07, immediateRender: false}}, {tp:.3f});')
    for k in range(6):
        sfx("key", tp + k * .07, -3)
    t_cov = T("send", L(10)) - .1
    js(f'tl.fromTo("#cov", {{y: 900, rotation: 10}}, {{y: 0, rotation: -4, duration: .45, ease: "{st(.45)}", immediateRender: false}}, {t_cov:.3f});')
    pop("#free", T("ten", L(10)), rot=8)
    js(f'tl.set("#r4 #rb_sad, #r4 #rm_sad, #r4 #rm_open", {{opacity: 0}}, {t0:.3f}); tl.set("#r4 #rb_up, #r4 #rm_smile", {{opacity: 1}}, {t0:.3f});')
    js(f'tl.fromTo("#r4 #rarm", {{rotation: 0, svgOrigin: "445 520"}}, {{rotation: -140, duration: .3, ease: "{st(.3)}", svgOrigin: "445 520", immediateRender: false}}, {t_cov:.3f});')
    js(f'tl.set("#b4 #be_n", {{opacity: 0}}, {t0:.3f}); tl.set("#b4 #be_h", {{opacity: 1}}, {t0:.3f});')
    js(f'tl.fromTo("#b4 .barmR", {{rotation: 0, svgOrigin: "254 260"}}, {{rotation: -70, duration: .2, yoyo: true, repeat: 9, ease: "steps(2)", svgOrigin: "254 260", immediateRender: false}}, {t0 + .4:.3f});')
    blink(t0 + 2.0)
    boil("#b4 .boil", t0, DUR)
    boil("#r4 .boil", t0, DUR)
    sfx("whoosh", t_cov, -4)
    sfx("pop", T("ten", L(10)), -5)


def caps():
    """subtitles as torn white paper strips, low; the keyword in pink"""
    KEY = {"again.", "ai.", "everyone", "write", "four", "who", "hook.", "format.", "her.", "blend", "comment", "prompt,"}
    chunks, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(w)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        txt = " ".join(x["w"] for x in cur)
        if nxt is None or nxt["line"] != w["line"] or w["w"][-1] in ".,?!:" or len(txt + " " + (nxt["w"] if nxt else "")) > 20:
            chunks.append(cur)
            cur = []
    for k, ch in enumerate(chunks):
        a = ch[0]["s"] - .04
        b = chunks[k + 1][0]["s"] - .04 if k + 1 < len(chunks) else DUR - .2
        if b - ch[-1]["e"] > .6:
            b = ch[-1]["e"] + .45
        txt = " ".join((f'<span class="pk">{H.escape(w["w"])}</span>' if norm(w["w"]) in {norm(x) for x in KEY} else H.escape(w["w"])) for w in ch)
        CAPS.append(f'<div class="cap" id="c{k}"><b style="transform:rotate({R.uniform(-1.6, 1.6):.1f}deg)">{txt}</b></div>')
        js(f'tl.fromTo("#c{k}", {{opacity: 0, scale: .7}}, {{opacity: 1, scale: 1, duration: .1, ease: "steps(1)", immediateRender: false}}, {max(0, a):.3f});')
        js(f'tl.set("#c{k}", {{opacity: 0}}, {b:.3f});')
    return len(chunks)


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {PAGE}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter", sans-serif; color: {INK}; background: {PAGE}; }}
.pk {{ color: {PINK}; }}
.scene {{ position: absolute; inset: 0; opacity: 0; transform-origin: 50% 100%; }}
.sbg {{ position: absolute; inset: 0; }}
.sbg::after {{ content: ""; position: absolute; inset: 0; box-shadow: inset 0 18px 30px -18px rgba(60,30,30,.35); }}
.layer {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; overflow: visible; }}
.rwrap, .bwrap {{ position: absolute; z-index: 2; }}
.riya, .bot {{ display: block; width: 100%; overflow: visible; }}
.boil {{ transform-origin: 50% 80%; }}
.spark {{ position: absolute; z-index: 4; }}
/* torn paper strips */
.strip {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; max-width: 980px; z-index: 6; transform: rotate(-2deg); }}
.strip b {{ position: relative; display: block; padding: 20px 40px 24px; background: #fff; font-weight: 800; font-size: 84px; line-height: 1.02; letter-spacing: -.03em; text-align: center;
  clip-path: polygon(0% 6%, 4% 0%, 9% 5%, 15% 1%, 22% 6%, 30% 0%, 38% 5%, 46% 1%, 55% 6%, 63% 0%, 71% 5%, 80% 1%, 88% 6%, 95% 0%, 100% 5%, 99% 50%, 100% 95%, 95% 100%,
    88% 95%, 80% 99%, 71% 94%, 63% 100%, 55% 95%, 46% 99%, 38% 94%, 30% 100%, 22% 95%, 15% 99%, 9% 94%, 4% 100%, 0% 95%, 1% 50%); }}
.strip .ssh {{ position: absolute; inset: 0; transform: translate(8px, 10px); background: {SHADOW}; clip-path: inherit; }}
.strip.top {{ top: 240px; }}
.strip.top.b {{ top: 240px; opacity: 0; }}
.strip.low {{ top: 1260px; }} .strip.low b {{ font-size: 60px; }}
.strip.cta {{ top: 240px; }} .strip.cta b {{ font-size: 84px; white-space: nowrap; }}
/* desk */
.dphone {{ position: absolute; left: 680px; top: 640px; width: 230px; z-index: 4; transform-origin: 50% 90%; }}
.phs {{ display: block; width: 100%; overflow: visible; }}
.dps {{ position: absolute; left: 20px; right: 20px; top: 70px; text-align: center; }}
.dpv {{ font-weight: 800; font-size: 82px; letter-spacing: -.04em; }}
.dpl {{ font-weight: 700; font-size: 30px; color: #8a8383; margin-top: -6px; }}
.dpbar {{ margin: 26px auto 0; width: 150px; height: 16px; border-radius: 8px; background: #eee8e8; overflow: hidden; }}
.dpbar i {{ display: block; height: 100%; background: {PINK}; transform-origin: 0 50%; }}
.sigh {{ position: absolute; left: 230px; top: 640px; z-index: 5; font-weight: 800; font-size: 90px; color: #8a8383; opacity: 0; }}
/* wall of reels */
.wall {{ position: absolute; inset: 0; transform-origin: 50% 40%; }}
.wph {{ position: absolute; width: 200px; transform-origin: 50% 50%; }}
.wps {{ position: absolute; left: 18px; right: 18px; top: 30px; display: flex; flex-direction: column; gap: 9px; }}
.wav {{ width: 40px; height: 40px; border-radius: 50%; background: #d6cfcf; }}
.wps b {{ font-weight: 800; font-size: 28px; color: #6f6969; }}
.wps span {{ font-weight: 600; font-size: 19px; line-height: 1.25; color: #9a9393; }}
.wps em {{ display: block; height: 11px; border-radius: 6px; background: #ece6e6; width: 92%; }} .wps em.s {{ width: 60%; }}
.wps u {{ text-decoration: none; font-weight: 700; font-size: 17px; color: #b0aaaa; margin-top: 18px; }}
.wph.her {{ z-index: 5; }}
.wps.nw {{ opacity: 0; background: {LIME}; border-radius: 14px; padding: 8px; }}
.wps.nw b {{ color: {INK}; font-size: 26px; }} .wps.nw span {{ color: {INK}; }} .wps.nw .wav {{ background: {PINK}; }} .wps.nw u {{ color: {INK}; }}
.wps.good b {{ color: {INK}; }} .wps.good span {{ color: {INK}; }} .wps.good .wav {{ background: {PINK}; }}
.heart {{ position: absolute; width: 70px; height: 64px; z-index: 6; opacity: 0; }}
.bub {{ position: absolute; z-index: 6; padding: 16px 26px; border-radius: 26px; background: #fff; font-weight: 800; font-size: 40px; box-shadow: 8px 10px 0 {SHADOW}; opacity: 0; }}
/* laptop */
.pbar {{ position: absolute; left: 190px; top: 760px; width: 700px; height: 120px; z-index: 3; display: flex; align-items: center; padding: 0 26px; border-radius: 26px;
  background: {PAGE}; border: 4px solid {INK}; }}
.lt {{ font-weight: 800; font-size: 46px; display: inline-block; }}
.caret {{ width: 5px; height: 54px; background: {PINK}; margin-left: 4px; }}
.scrollA {{ position: absolute; left: 420px; top: 560px; width: 560px; z-index: 4; transform-origin: 50% 0%; opacity: 0; }}
.scrollA .sci {{ position: relative; padding: 30px 34px; background: #ece8e4; font-weight: 600; font-size: 38px; line-height: 1.3; color: #6f6969;
  clip-path: polygon(0 2%, 50% 0, 100% 2%, 99% 98%, 50% 100%, 1% 98%); }}
.scrollA .sci b {{ color: #4f4a4a; }}
.scrollA .ssh, .scrollB .ssh, .cbox .ssh, .cov .ssh {{ position: absolute; inset: 0; transform: translate(9px, 11px); background: {SHADOW}; border-radius: 18px; }}
.gen {{ position: absolute; right: -10px; bottom: -40px; padding: 10px 26px; border: 7px solid {PINK}; color: {PINK}; background: rgba(255,255,255,.9); font-weight: 800; font-size: 54px;
  letter-spacing: .04em; border-radius: 16px; opacity: 0; }}
/* puzzle */
.board {{ position: absolute; left: 180px; top: 330px; width: 720px; height: 720px; z-index: 2; background: {KRAFT}; border-radius: 26px; transform-origin: 50% 50%; opacity: 0;
  box-shadow: 10px 12px 0 {SHADOW}; }}
.board .ssh {{ display: none; }}
.slot {{ position: absolute; width: 330px; height: 330px; margin: 15px; border: 5px dashed rgba(16,17,17,.35); border-radius: 22px; }}
.slot b {{ position: absolute; left: 0; right: 0; top: 110px; text-align: center; font-weight: 800; font-size: 90px; color: rgba(16,17,17,.18); }}
.pz {{ position: absolute; width: 330px; height: 330px; z-index: 3; border-radius: 22px; box-shadow: 9px 11px 0 {SHADOW}; display: flex; flex-direction: column; align-items: center;
  padding-top: 18px; opacity: 0; }}
#pz0 {{ left: 195px; top: 345px; }} #pz1 {{ left: 540px; top: 345px; }} #pz2 {{ left: 195px; top: 690px; }} #pz3 {{ left: 540px; top: 690px; }}
.pzi {{ width: 200px; height: 170px; }} .pzi svg {{ width: 200px; height: 170px; overflow: visible; }}
.pz b {{ font-weight: 800; font-size: 34px; letter-spacing: .02em; margin-top: 8px; }}
.pz span {{ font-weight: 700; font-size: 26px; opacity: .75; }}
.pz.dark b, .pz.dark span {{ color: {LIME}; }}
.tab {{ position: absolute; width: 70px; height: 70px; border-radius: 50%; }}
.tab.t0 {{ right: -34px; top: 130px; }} .tab.t1 {{ bottom: -34px; left: 130px; }} .tab.t2 {{ top: -34px; left: 130px; }} .tab.t3 {{ left: -34px; top: 130px; }}
.bulb {{ position: absolute; left: 760px; top: 1020px; width: 200px; height: 200px; z-index: 5; opacity: 0; overflow: visible; }}
/* payoff */
.scrollB {{ position: absolute; left: 420px; top: 400px; width: 620px; z-index: 3; transform-origin: 50% 0%; }}
.scin {{ position: relative; padding: 40px 38px 70px; background: #fff; border-radius: 18px; display: flex; flex-direction: column; gap: 14px; }}
.gl {{ font-weight: 800; font-size: 38px; line-height: 1.22; }}
.gl:nth-child(-n+2) {{ background: linear-gradient(transparent 55%, {LIME} 55%); }}
.sly {{ position: absolute; left: 50px; bottom: -48px; padding: 14px 30px; background: {LIME}; border: 6px solid {INK}; border-radius: 18px; font-weight: 800; font-size: 48px;
  letter-spacing: .03em; opacity: 0; box-shadow: 8px 10px 0 {SHADOW}; }}
/* CTA */
.cbox {{ position: absolute; left: 90px; right: 90px; top: 430px; height: 130px; z-index: 4; }}
.cbox::before {{ content: ""; position: absolute; inset: 0; background: #fff; border-radius: 999px; border: 5px solid {INK}; }}
.cbox .ssh {{ border-radius: 999px; }}
.cav {{ position: absolute; left: 24px; top: 28px; width: 74px; height: 74px; border-radius: 50%; background: {PINK}; }}
.ct {{ position: absolute; left: 124px; top: 30px; font-weight: 800; font-size: 60px; letter-spacing: .05em; }}
.ct b {{ display: inline-block; }}
.snd {{ position: absolute; right: 26px; top: 26px; width: 78px; height: 78px; border-radius: 50%; background: {PINK}; }}
.cov {{ position: absolute; left: 330px; top: 600px; width: 500px; z-index: 3; transform-origin: 50% 100%; }}
.cov img {{ position: relative; display: block; width: 500px; height: 625px; border-radius: 18px; border: 5px solid {INK}; }}
.free {{ position: absolute; right: -50px; top: -34px; padding: 12px 26px; background: {LIME}; border: 5px solid {INK}; border-radius: 999px; font-weight: 800; font-size: 40px; opacity: 0; }}
/* subtitles: torn white strips */
.cap {{ position: absolute; left: 0; right: 0; top: 1500px; text-align: center; z-index: 9; opacity: 0; }}
.cap b {{ display: inline-block; padding: 12px 30px 16px; background: {INK}; color: #fff; font-weight: 800; font-size: 58px; letter-spacing: -.01em; border-radius: 3px;
  box-shadow: 7px 9px 0 {SHADOW}; }}
.cap .pk {{ color: {LIME}; }}
#grain {{ position: absolute; inset: 0; z-index: 10; pointer-events: none; background: url(assets/img/paper.png); mix-blend-mode: multiply; opacity: .55; }}
"""


def main():
    t = [0, L(1) - .05, L(2) - .05, L(3) - .05, L(8) - .05, L(9) - .05, L(10) - .1, DUR]
    sc_desk(t[0], t[1])
    sc_wall(t[1], t[2])
    sc_laptop(t[2], t[3])
    sc_puzzle(t[3], t[4])
    sc_payoff(t[4], t[5])
    sc_pop(t[5], t[6])
    sc_cta(t[6])
    n = caps()
    page = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Creators 100X: Riya's prompt, a paper cut-out story 9x16</title>
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
    json.dump({"dur": DUR, "scenes": [round(x, 3) for x in t]}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
    print(f"wrote index.html: {len(A)} timeline lines, {n} captions, {len(SFX)} sfx, {DUR} s")


if __name__ == "__main__":
    main()
