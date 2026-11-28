"""Creedom "The First 3 Seconds", Vox-style cut-out version (HyperFrames, 1080x1920).

Same voice and timing as creedom-hook-history-9x16 (Brian, as recorded). Writes index.html and plan/sfx_events.json.

Engagement design (psychology):
- Pattern interrupt at least every ~2 s: a new cut-out, stamp, note or transition on the spoken word.
- Colour arc: muted archive paper (past, low arousal) -> Vox yellow (attention) -> hot Creedom pink at TODAY (novelty spike,
  the payoff colour). Red is only for verdicts (THE HARD WAY, TESTED LIVE); pink only for the answer (TEST FIRST, Creedom).
- Progress bar at the top (1918 -> 1930s -> 1941 -> TODAY -> YOU): goal-gradient / open loop, viewers stay to finish it.
- Match cuts (headline -> film frame, into the TV screen -> out of the phone) give continuity and a satisfying "click".
- Countdown 3-2-1, count-ups and a reward beat (score + sparkle + ding) at the end.
- Faces and crowds (newsboy, cinema crowd) for social proof; motion keeps moving forward (slow push on every scene).
"""
import json
import math
import pathlib
import random

P = pathlib.Path(__file__).resolve().parent.parent
words = json.loads((P / "assets/audio/words.json").read_text())
tm = json.loads((P / "assets/audio/timing.json").read_text())
SEG = {s["id"]: s for s in tm["segments"]}
DUR = tm["total_duration"]
L = lambda i: SEG[i]["start"]
E = lambda i: SEG[i]["end"]


def T(i, w, nth=0):
    return [x["s"] for x in words[str(i)] if x["w"].startswith(w)][nth]


INK, CREAM, YEL, RED, PINK, PINKBG = "#1e1a16", "#efe6d2", "#f2c230", "#c8321e", "#F343A2", "#fdf1f6"

TL, SFX = [], []
FIRST, EARLY = {}, {}


def js(d):
    out = []
    for k, v in d.items():
        out.append(f"{k}: {json.dumps(v) if isinstance(v, str) else v}")
    return "{" + ", ".join(out) + "}"


def _rec(sel, props, t, kind):
    for k, v in props.items():
        key = (sel, k)
        if key not in EARLY or t < EARLY[key][0]:
            EARLY[key] = (t, kind, v)


def to(sel, frm, too, t, d, ease="power3.out", pre=True):
    TL.append(f'tl.fromTo("{sel}", {js(frm)}, {{...{js(too)}, duration: {d:.3f}, ease: "{ease}", immediateRender: false}}, {t:.3f});')
    if pre:
        _rec(sel, frm, t, "from")


def st(sel, props, t):
    TL.append(f'tl.set("{sel}", {js(props)}, {max(0, t):.3f});')
    _rec(sel, props, t, "set")


def sfx(kind, t, gain=0.0):
    SFX.append({"kind": kind, "t": round(max(0, t), 3), "gain": gain})


def show(sel, t):
    st(sel, {"opacity": 1}, t)


def hide(sel, t):
    st(sel, {"opacity": 0}, t)


def pop(sel, t, d=0.45, rot=0, y=60, sc=0.6, s="pop"):
    to(sel, {"opacity": 0, "scale": sc, "y": y, "rotation": rot - 8}, {"opacity": 1, "scale": 1, "y": 0, "rotation": rot}, t, d, "back.out(1.8)")
    if s:
        sfx(s, t)


def drop(sel, t, rot=0, s="slap"):
    to(sel, {"opacity": 0, "scale": 1.35, "rotation": rot + 10, "y": -40}, {"opacity": 1, "scale": 1, "rotation": rot, "y": 0}, t, 0.32, "power4.out")
    if s:
        sfx(s, t + 0.12)


def boil(sel, t0, t1, amp=1.0, seed=1):
    r = random.Random(seed)
    t = t0
    while t < t1:
        st(sel, {"rotation": round(r.uniform(-amp, amp), 2), "x": round(r.uniform(-2, 2), 1), "y": round(r.uniform(-2, 2), 1)}, t)
        t += 1 / 8


def stamp(sel, t, rot=-10):
    to(sel, {"opacity": 0, "scale": 2.4, "rotation": rot - 14}, {"opacity": 1, "scale": 1, "rotation": rot}, t, 0.16, "power4.in")
    sfx("stamp", t + 0.12)
    shake(t + 0.14, 10)


def draw(sel, t, d=0.45):
    to(sel, {"strokeDashoffset": 1}, {"strokeDashoffset": 0}, t, d, "power1.inOut")
    sfx("scribble", t)


def shake(t, amp=12, dur=0.26):
    n = 8
    for k in range(n):
        a = amp * (1 - k / n)
        st("#cam", {"x": round(a * math.sin(k * 2.3), 1), "y": round(a * math.cos(k * 1.7), 1)}, t + k * dur / n)
    st("#cam", {"x": 0, "y": 0}, t + dur)


def flash(t, a=0.75):
    to("#flash", {"opacity": a}, {"opacity": 0}, t, 0.22, "power2.out", pre=False)


def slow_push(sel, t0, t1, s0=1.0, s1=1.06):
    to(sel, {"scale": s0}, {"scale": s1}, t0, max(0.1, t1 - t0), "none")


def type_on(sel, t, n, cps=28):
    """Reveal a text letter by letter (each letter is a span .ch)."""
    for k in range(n):
        st(f"{sel} .ch{k}", {"opacity": 1}, t + k / cps)
    if n:
        sfx("type", t)


def letters(text, cls=""):
    return "".join(f'<span class="lt ch{k} {cls}" style="opacity:0">{c if c != " " else "&nbsp;"}</span>' for k, c in enumerate(text))


def roll(sel, a, b, t, d):
    TL.append(f'tl.fromTo(__rv["{sel}"] = __rv["{sel}"] || {{v: {a}}}, {{v: {a}}}, {{v: {b}, duration: {d:.3f}, ease: "power2.out", immediateRender: false, '
              f'onUpdate: () => {{ document.querySelector("{sel}").textContent = Math.round(__rv["{sel}"].v); }}}}, {t:.3f});')
    sfx("tick", t)


def count(sel, a, b, t, d, dec=1):
    TL.append(f'tl.fromTo(__rv["{sel}"] = __rv["{sel}"] || {{v: {a}}}, {{v: {a}}}, {{v: {b}, duration: {d:.3f}, ease: "power2.out", immediateRender: false, '
              f'onUpdate: () => {{ document.querySelector("{sel}").textContent = __rv["{sel}"].v.toFixed({dec}); }}}}, {t:.3f});')


# ------------------------------------------------------------------ transitions
def slap_rip(t, prev, nxt, bg=None):
    to("#tear", {"x": 1300, "opacity": 1}, {"x": 0, "opacity": 1}, t - 0.42, 0.22, "power3.out")
    sfx("slap", t - 0.3)
    hide(prev, t - 0.18); show(nxt, t - 0.18)
    if bg:
        st("#bg", {"backgroundColor": bg}, t - 0.18)
    to("#tA", {"y": 0, "rotation": 0}, {"y": -1500, "rotation": -9}, t - 0.12, 0.55, "power2.in")
    to("#tB", {"y": 0, "rotation": 0}, {"y": 1500, "rotation": 7}, t - 0.12, 0.55, "power2.in")
    sfx("tear", t - 0.13)
    hide("#tear", t + 0.5)


def block_wipe(t, prev, nxt, colour, bg):
    st("#wipe", {"backgroundColor": colour}, t - 0.5)
    to("#wipe", {"y": 2000}, {"y": -2600}, t - 0.45, 0.7, "power2.inOut")
    hide(prev, t - 0.12); show(nxt, t - 0.12)
    st("#bg", {"backgroundColor": bg}, t - 0.12)
    sfx("whoosh", t - 0.4)


# ------------------------------------------------------------------ HTML pieces
H = []


def el(html):
    H.append(html)


def cut(id_, src, x, y, w, rot=0, z=5, extra=""):
    """A cut-out: outer div moves (#id), inner img boils (#id_i). (x, y) is the top-left in px."""
    return (f'<div class="ct" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z};opacity:0;transform:rotate({rot}deg)">'
            f'<img id="{id_}_i" src="assets/img/{src}" style="width:100%">{extra}</div>')


def tape(id_, text, x, y, rot=-3, z=20, bg="#f7f1e3", fg=INK, size=40):
    return (f'<div class="tape" id="{id_}" style="left:{x}px;top:{y}px;z-index:{z};opacity:0;transform:rotate({rot}deg);background:{bg};color:{fg};font-size:{size}px">'
            f'{text}</div>')


def stamp_el(id_, text, x, y, colour=RED, size=96, z=40, rot=-10):
    return (f'<div class="stamp" id="{id_}" style="left:{x}px;top:{y}px;z-index:{z};opacity:0;color:{colour};border-color:{colour};font-size:{size}px;'
            f'transform:translate(-50%,-50%) rotate({rot}deg)">{text}</div>')


def scribble(id_, d, x, y, w, h, colour=RED, sw=9, z=30, vb=None):
    vb = vb or f"0 0 {w} {h}"
    return (f'<svg class="scr" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}" viewBox="{vb}">'
            f'<path d="{d}" pathLength="1" stroke="{colour}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round" '
            f'style="stroke-dasharray:1;stroke-dashoffset:1" id="{id_}_p"/></svg>')


def hand(id_, text, x, y, colour=RED, size=46, rot=-4, z=30):
    return (f'<div class="hand" id="{id_}" style="left:{x}px;top:{y}px;z-index:{z};color:{colour};font-size:{size}px;transform:rotate({rot}deg)">'
            f'{letters(text)}</div>')


# ================================================================== SCENES
# ---- S0 title (0 -> L3)
s0 = []
s0.append(f'<div class="t-first">THE FIRST</div>')
s0.append(f'<div class="t-three" id="t3"><i id="t3bar"></i><span>3 SECONDS</span></div>')
s0.append(cut("c0n", "news.png", 40, 960, 330, -9, 6))
s0.append(cut("c0p", "poster.png", 385, 900, 300, 4, 7))
s0.append(cut("c0t", "tv.png", 720, 930, 300, 7, 6))
s0.append(hand("h0", "every screen. one rule.", 190, 800, INK, 50, -3))
s0.append(scribble("sc0", "M10,30 C200,5 420,50 650,18", 210, 880, 660, 50, RED, 8))
s0.append(stamp_el("st0", "THE HARD WAY", 540, 1170, RED, 110))
el(f'<div class="sc" id="s0" style="opacity:1"><div class="kb" id="kb0">{"".join(s0)}</div></div>')
# frame one: title, cut-outs already landing
to("#t3bar", {"scaleX": 0.7}, {"scaleX": 1}, 0.0, 0.3, "power3.out")
for k, (sel, rot) in enumerate((("#c0n", -9), ("#c0p", 4), ("#c0t", 7))):
    to(sel, {"opacity": 1, "y": 0 if k == 0 else 70, "rotation": rot - 6 * k}, {"opacity": 1, "y": 0, "rotation": rot}, 0.0, 0.35 + 0.1 * k, "back.out(1.6)")
    boil(sel + "_i", 0.0, L(3), 0.8, seed=k)
sfx("pop", 0.12); sfx("pop", 0.24)
type_on("#h0", T(1, "same") - 0.15, len("every screen. one rule."), 30)
draw("#sc0_p", T(1, "rule") - 0.1, 0.4)
stamp("#st0", T(2, "hard"))
slow_push("#kb0", 0, L(3), 1.0, 1.07)

# ---- S1 1918 (L3 -> L4)
s1 = []
s1.append('<div class="dots"></div>')
s1.append(f'<div class="year" id="y1"><span id="y1v">1890</span></div>')
s1.append(cut("c1n", "news.png", 170, 520, 740, -3, 5))
s1.append(cut("c1b", "newsboy.png", 40, 1010, 380, -7, 9, extra=f'<div class="cap-tape" style="background:{YEL}">NEWSBOY, 1910</div>'))
s1.append(f'<div class="ct" id="hlw" style="left:120px;top:575px;width:840px;z-index:12;opacity:0">'
          f'<img src="assets/img/headline.png" style="width:100%"><i class="hl" id="hl1"></i></div>')
s1.append(scribble("sc1", "M30,70 C10,10 300,-4 520,10 C760,24 830,60 800,95 C760,140 200,150 60,120 C20,110 25,90 40,75",
                   110, 690, 860, 170, RED, 9, 13))
s1.append(f'<div class="callout" id="co1" style="left:470px;top:1040px;opacity:0;transform:rotate(3deg)"><b>BIGGEST LETTERS</b><span>= the first thing you see</span></div>')
el(f'<div class="sc" id="s1"><div class="kb" id="kb1">{"".join(s1)}</div></div>')
slap_rip(L(3), "#s0", "#s1", YEL)
pop("#y1", L(3) - 0.1, 0.35, 0, 30, 0.7, None)
roll("#y1v", 1890, 1918, L(3) - 0.05, 0.75)
drop("#c1n", L(3) + 0.08, -3)
boil("#c1n_i", L(3), L(4), 0.6, 3)
to("#c1b", {"opacity": 0, "x": -420, "rotation": -20}, {"opacity": 1, "x": 0, "rotation": -7}, T(3, "newspapers") + 0.25, 0.45, "back.out(1.4)")
sfx("whoosh", T(3, "newspapers") + 0.25)
boil("#c1b_i", T(3, "newspapers") + 0.3, L(4), 0.8, 4)
to("#hlw", {"opacity": 0, "scale": 0.88, "y": 0, "rotation": -3}, {"opacity": 1, "scale": 1.08, "y": 40, "rotation": -1.5}, T(3, "headline") - 0.35, 0.45, "back.out(1.5)")
sfx("tear", T(3, "headline") - 0.35)
to("#hl1", {"scaleX": 0}, {"scaleX": 1}, T(3, "headline") - 0.05, 0.4, "power2.out")
sfx("scribble", T(3, "headline") - 0.05)
draw("#sc1_p", T(3, "biggest") - 0.1, 0.45)
pop("#co1", T(3, "letters") - 0.05, 0.4, 3, 60, 0.6)
slow_push("#kb1", L(3), L(4), 1.0, 1.06)

# ---- S2 silent era + 1930s (L4 -> L7)
s2 = []
s2.append('<i id="beam"></i>')
s2.append(f'<div id="ybg"></div>')
s2.append(f'<div class="ttl" id="ttl2">{letters("THE SILENT ERA")}</div>')
frames = []
labels = ["FEATURE · REEL 1", "FEATURE · REEL 2", "FEATURE · REEL 3", "", "TRAILER"]
for k in range(5):
    if k < 3:
        inner = f'<img src="assets/img/frame{k}.jpg"><small>{labels[k]}</small>'
        cls = ""
    elif k == 3:
        inner = '<b class="end">THE END</b>'
        cls = " endf"
    else:
        inner = '<b class="ca1">COMING</b><b class="ca2">ATTRACTIONS</b><small>TRAILER</small>'
        cls = " trf"
    frames.append(f'<div class="fr{cls}" id="fr{k}" style="top:{40 + k * 400}px">{inner}</div>')
s2.append(f'<div id="strip"><div id="stripin">{"".join(frames)}</div></div>')
s2.append(scribble("sc2", "M20,10 C120,60 130,300 30,380", 640, 0, 160, 400, YEL, 10, 30))
s2.append(hand("h2", "after the film!", 690, 0, YEL, 44, -6))
s2.append(f'<div class="bigword" id="bw2" style="opacity:0">TRAILER</div>')
s2.append(hand("h2b", "it trailed the movie", 610, 0, CREAM, 40, -3))
s2.append(stamp_el("st2", "1930s", 860, 585, INK, 90, 40, 8))
s2.append(scribble("sc2b", "M60,880 C10,600 20,300 80,40 M40,110 L80,40 L125,105", 620, 0, 160, 900, INK, 12, 30, "0 0 160 900"))
s2.append(tape("tp2", "MOVED TO THE FRONT", 630, 0, -4, 35, INK, YEL, 44))
s2.append(cut("c2c", "crowd.png", 560, 0, 470, 4, 20, extra=f'<div class="cap-tape" style="background:{CREAM}">GRAUMAN\'S EGYPTIAN, 1926</div>'))
eyes = "".join(f'<i class="eye" id="eye{k}" style="left:{x}px;top:{y}px"></i>' for k, (x, y) in enumerate(((600, 0), (930, 0), (560, 0), (980, 0), (770, 0))))
s2.append(eyes)
el(f'<div class="sc" id="s2"><div class="kb" id="kb2">{"".join(s2)}</div></div>')

# match cut: headline flies at the camera, flash, the projector room
to("#hlw", {"scale": 1.08, "opacity": 1}, {"scale": 3.6, "opacity": 0}, L(4) - 0.28, 0.3, "power2.in")
sfx("whoosh", L(4) - 0.3)
flash(L(4) - 0.04, 0.85)
hide("#s1", L(4) - 0.03); show("#s2", L(4) - 0.03)
st("#bg", {"backgroundColor": "#191512"}, L(4) - 0.03)
sfx("projector", L(4) - 0.05)
type_on("#ttl2", L(4) + 0.05, len("THE SILENT ERA"), 32)
# the strip scrolls up like film through a gate
STRIP_TOP0 = 520
to("#stripin", {"y": 0}, {"y": -1040}, L(4), T(4, "after") - L(4), "power1.inOut")
# positions after the scroll: END frame at 520+40+1200-1040 = 720, trailer at 1120
endy, try_ = STRIP_TOP0 + 40 + 1200 - 1040, STRIP_TOP0 + 40 + 1600 - 1040
st("#sc2", {"top": endy + 130}, 0); st("#h2", {"top": endy + 80}, 0)
draw("#sc2_p", T(4, "after") - 0.1, 0.4)
type_on("#h2", T(4, "after"), len("after the film!"), 30)
pop("#bw2", T(5, "trailers") - 0.12, 0.35, -4, 40, 0.5, "pop")
st("#bw2", {"top": try_ - 30}, 0)
st("#h2b", {"top": try_ + 150}, 0)
type_on("#h2b", T(5, "trailers") + 0.2, len("it trailed the movie"), 34)
hide("#h2", L(6)); hide("#sc2", L(6)); hide("#bw2", L(6)); hide("#h2b", L(6))
# 1930s: yellow block slides in behind the strip; the trailer frame jumps to the front
to("#ybg", {"xPercent": 100}, {"xPercent": 0}, L(6) - 0.15, 0.35, "power3.inOut")
sfx("whoosh", L(6) - 0.15)
st("#ttl2", {"color": INK}, L(6) + 0.1)
to("#beam", {"opacity": 0.85}, {"opacity": 0}, L(6), 0.3, "none")
stamp("#st2", T(6, "1930") - 0.05, 8)
tf = T(6, "front") - 0.3
to("#fr4", {"y": 0, "scale": 1}, {"y": -1600, "scale": 1}, tf, 0.55, "power3.inOut")
for k in range(4):
    to(f"#fr{k}", {"y": 0}, {"y": 400}, tf + 0.05, 0.5, "power3.inOut")
to("#stripin", {"y": -1040}, {"y": -1040 + 1040 - 40}, tf, 0.6, "power3.inOut")   # show the top of the strip again
sfx("slap", tf + 0.45)
st("#sc2b", {"top": 380}, 0)
draw("#sc2b_p", tf + 0.05, 0.45)
st("#tp2", {"top": 700}, 0)
pop("#tp2", tf + 0.3, 0.35, -4, 30, 0.6, None)
st("#c2c", {"top": 800}, 0)
to("#c2c", {"opacity": 0, "y": 500, "rotation": 14}, {"opacity": 1, "y": 0, "rotation": 4}, T(6, "more") - 0.12, 0.45, "back.out(1.4)")
sfx("whoosh", T(6, "more") - 0.12)
boil("#c2c_i", T(6, "more"), L(7), 0.7, 6)
for k, yv in enumerate((760, 820, 1210, 1180, 740)):
    st(f"#eye{k}", {"top": yv}, 0)
    pop(f"#eye{k}", T(6, "people") + 0.06 * k, 0.3, 0, 20, 0.3, "pop" if k == 0 else None)
slow_push("#kb2", L(4), L(7), 1.0, 1.05)
for k in range(int((L(6) - L(4)) * 12)):          # projector flicker
    st("#beam", {"opacity": round(random.Random(k).uniform(0.55, 0.95), 2)}, L(4) + k / 12)

# ---- S3 1941 (L7 -> L9)
s3 = []
s3.append('<div class="grid"></div>')
s3.append(f'<div class="year" id="y3"><span id="y3v">1918</span></div>')
s3.append(f'<div class="dateline" id="dl3">{letters("JULY 1, 1941  ·  NEW YORK")}</div>')
s3.append(cut("c3a", "rcaad.png", 60, 610, 300, -8, 4))
s3.append(f'<div class="ct" id="c3t" style="left:150px;top:640px;width:560px;z-index:8;opacity:0">'
          f'<img id="c3t_i" src="assets/img/tv.png" style="width:100%"><div id="scr"><i id="static"></i><div id="scron"><i id="mclk"><b id="mhand"></b></i><span>ON AIR</span></div></div></div>')
s3.append('<div id="ring"><svg viewBox="0 0 300 300"><circle cx="150" cy="150" r="128" stroke="#d9cdb4" stroke-width="22" fill="none"/>'
          f'<circle id="ringp" cx="150" cy="150" r="128" stroke="{RED}" stroke-width="22" fill="none" pathLength="1" '
          'style="stroke-dasharray:1;stroke-dashoffset:0" transform="rotate(-90 150 150)" stroke-linecap="round"/></svg><b id="ringv">10</b><small>SECONDS</small></div>')
s3.append(f'<div class="sticky" id="stk3">cost:<br><b>$9</b></div>')
s3.append(stamp_el("st3", "10 SECONDS", 430, 1220, RED, 100))
el(f'<div class="sc" id="s3"><div class="kb" id="kb3">{"".join(s3)}</div></div>')
block_wipe(L(7), "#s2", "#s3", YEL, CREAM)
st("#ttl2", {"color": CREAM}, 0)
pop("#y3", L(7) - 0.08, 0.35, 0, 30, 0.7, None)
roll("#y3v", 1918, 1941, L(7) - 0.05, T(7, "1941") - L(7) + 0.45)
type_on("#dl3", T(7, "america") - 0.15, len("JULY 1, 1941  ·  NEW YORK"), 30)
to("#c3t", {"opacity": 0, "y": -900, "rotation": -6}, {"opacity": 1, "y": 0, "rotation": -2}, L(7) + 0.2, 0.5, "bounce.out")
sfx("slap", L(7) + 0.5)
boil("#c3t_i", L(7) + 0.7, L(9), 0.5, 8)
pop("#c3a", T(7, "america"), 0.35, -8, 40, 0.6, None)
st("#static", {"opacity": 1}, T(7, "tv") - 0.15)
sfx("static", T(7, "tv") - 0.15)
for k in range(int(0.55 * 24)):
    st("#static", {"backgroundPosition": f"{random.Random(k).randint(0, 300)}px {random.Random(k + 50).randint(0, 300)}px"}, T(7, "tv") - 0.15 + k / 24)
to("#scron", {"opacity": 0}, {"opacity": 1}, T(7, "ad") + 0.25, 0.2, "power1.out")
hide("#static", T(7, "ad") + 0.35)
to("#mhand", {"rotation": 0}, {"rotation": 360}, T(7, "ad") + 0.25, 6, "none")
pop("#ring", T(7, "ran") - 0.15, 0.4, 0, 40, 0.5)
roll("#ringv", 10, 0, T(7, "10"), E(8) - T(7, "10"))
to("#ringp", {"strokeDashoffset": 0}, {"strokeDashoffset": 1}, T(7, "10"), E(8) - T(7, "10"), "none")
sfx("clock", T(7, "ran") - 0.1)
to("#stk3", {"opacity": 0, "rotation": 30, "scale": 0.4}, {"opacity": 1, "rotation": 6, "scale": 1}, T(8, "sell") - 0.1, 0.35, "back.out(2)")
sfx("pop", T(8, "sell") - 0.1)
stamp("#st3", T(8, "watch") - 0.05, -8)
slow_push("#kb3", L(7), L(9), 1.0, 1.05)

# ---- S4 TODAY (L9 -> L11)
s4 = []
s4.append('<div class="pdots"></div>')
feed = []
for side, x in ((0, 40), (1, 820)):
    for k in range(7):
        a, b = [("#ff8a50", PINK), ("#4a6ee6", "#28c8be"), ("#9650dc", PINK), ("#ffaa3c", "#f0505a")][(k + 2 * side) % 4]
        feed.append(f'<i class="fc" style="left:{x}px;top:{k * 520 - 300}px;background:linear-gradient(140deg,{a},{b})"></i>')
s4.append(f'<div id="feedL">{"".join(f for f in feed[:7])}</div><div id="feedR">{"".join(f for f in feed[7:])}</div>')
s4.append(f'<div class="todayb" id="tdy">TODAY</div>')
s4.append('<div id="phone"><div id="pscr"><div class="reel r1" id="reel1"><b>wait for it...</b><i class="ic a"></i><i class="ic b"></i><i class="ic c"></i>'
          '<i class="bar1" id="pbar"></i></div><div class="reel r2" id="reel2"><b>your next reel</b><i class="ic a"></i><i class="ic b"></i><i class="ic c"></i></div>'
          '<i id="scan"></i></div><i class="notch"></i><i id="thumb"></i></div>')
for k, n in enumerate(("3", "2", "1")):
    s4.append(f'<div class="cd" id="cd{k}">{n}</div>')
s4.append(stamp_el("st4a", "TESTED LIVE", 230, 520, RED, 62, 60, -12))
s4.append(stamp_el("st4b", "TESTED LIVE", 850, 520, RED, 62, 60, 8))
s4.append(stamp_el("st4c", "TESTED LIVE", 230, 1130, RED, 62, 60, -6))
s4.append(stamp_el("st4d", "TEST FIRST", 540, 470, PINK, 96, 70, -8))
s4.append(cut("c4n", "news.png", 40, 360, 300, -8, 30))
s4.append(cut("c4p", "poster.png", 720, 350, 270, 7, 30))
s4.append(cut("c4t", "tv.png", 70, 900, 290, -5, 30))
s4.append(cut("c4c", "crowd.png", 720, 920, 300, 6, 30))
# scan HUD
s4.append(f'<div id="scanlab">SCANNING THE FIRST 3 SECONDS</div><div id="segs">' +
          "".join(f'<div class="seg"><small id="sgl{k}">0:0{k + 1}</small><i><b id="sg{k}"></b></i></div>' for k in range(3)) + '</div>')
s4.append('<div id="brk"><i class="b1"></i><i class="b2"></i><i class="b3"></i><i class="b4"></i></div>')
# Creedom card
s4.append('<div id="card"><img src="assets/img/logo_creedom.png" class="lg"><span class="ra">REEL ANALYZER</span>'
          '<small class="hsc">HOOK SCORE</small><div class="score"><b id="scv">0.0</b><span>/ 5</span></div><i class="ex">EXAMPLE</i>'
          '<div class="stars">' + "".join(f'<i id="sr{k}"></i>' for k in range(5)) + '</div>'
          '<div class="flag" id="flg"><i>0:02</i><b>Weak hook</b><span>Fix: show the result first</span></div>'
          '<div class="chk" id="chk"><b>CHECKED BEFORE YOU POST</b></div></div>')
s4.append('<div id="spark">' + "".join(f'<i class="sp" id="sp{k}"></i>' for k in range(14)) + '</div>')
s4.append(f'<div id="endl"><span>Test your hook before you post</span><b>creedom.ai</b></div>')
el(f'<div class="sc" id="s4"><div class="kb" id="kb4">{"".join(s4)}</div></div>')

# zoom THROUGH the TV screen ... and out of the phone
ZT = L(9)
to("#s3", {"scale": 1}, {"scale": 9}, ZT - 0.42, 0.4, "power3.in")
sfx("riser", ZT - 0.9)
flash(ZT - 0.04, 0.95)
hide("#s3", ZT - 0.03); show("#s4", ZT - 0.03)
st("#bg", {"backgroundColor": PINK}, ZT - 0.03)
st("#paper", {"opacity": 0.28}, ZT - 0.03)
to("#phone", {"scale": 3.4, "y": 0}, {"scale": 1, "y": 0}, ZT - 0.02, 0.55, "power3.out")
sfx("boom", ZT)
to("#tdy", {"opacity": 0, "scale": 2.2}, {"opacity": 1, "scale": 1}, T(9, "today") - 0.05, 0.25, "power4.in")
sfx("stamp", T(9, "today") + 0.15)
to("#feedL", {"y": 0, "opacity": 0}, {"y": -900, "opacity": 1}, T(9, "today") + 0.2, T(10, "moves") - T(9, "today") - 0.3, "none")
to("#feedR", {"y": -400, "opacity": 0}, {"y": -1300, "opacity": 1}, T(9, "today") + 0.2, T(10, "moves") - T(9, "today") - 0.3, "none")
to("#feedL", {"y": -900}, {"y": -2400}, T(10, "moves") - 0.1, 1.2, "power2.in")
to("#feedR", {"y": -1300}, {"y": -2900}, T(10, "moves") - 0.1, 1.2, "power2.in")
to("#pbar", {"scaleX": 0}, {"scaleX": 1}, ZT, T(10, "moves") - ZT, "none")
t3 = T(9, "three")
for k, tt in enumerate((t3, t3 + 0.5, T(10, "before"))):
    to(f"#cd{k}", {"opacity": 0, "scale": 2.6}, {"opacity": 1, "scale": 1}, tt - 0.05, 0.2, "power4.in")
    sfx("impact", tt + 0.1)
    hide(f"#cd{k}", (t3 + 0.5 - 0.05) if k == 0 else (T(10, "before") - 0.05) if k == 1 else T(10, "moves") + 0.1)
tm_ = T(10, "moves") - 0.15
to("#thumb", {"opacity": 0, "y": 260}, {"opacity": 1, "y": -380}, tm_ - 0.2, 0.5, "power2.inOut")
hide("#thumb", tm_ + 0.4)
to("#reel1", {"yPercent": 0}, {"yPercent": -100}, tm_, 0.4, "power3.inOut")
to("#reel2", {"yPercent": 100}, {"yPercent": 0}, tm_, 0.4, "power3.inOut")
sfx("swipe", tm_ - 0.05)
slow_push("#kb4", ZT, L(11), 1.0, 1.04)

# TESTED LIVE (L11): tear to a collage; the eras pinned around a small phone
slap_rip(L(11), "#s4", "#s4", CREAM)
st("#paper", {"opacity": 0.6}, L(11) - 0.18)
hide("#tdy", L(11) - 0.18); hide("#feedL", L(11) - 0.18); hide("#feedR", L(11) - 0.18); st(".pdots", {"opacity": 0}, L(11) - 0.18)
st("#phone", {"scale": 0.5}, L(11) - 0.18)
for k, (sel, rot) in enumerate((("#c4n", -8), ("#c4p", 7), ("#c4t", -5), ("#c4c", 6))):
    to(sel, {"opacity": 0, "scale": 1.5, "rotation": rot + 12}, {"opacity": 1, "scale": 1, "rotation": rot}, L(11) - 0.05 + 0.08 * k, 0.3, "power4.out")
    boil(sel + "_i", L(11), L(13), 0.8, 20 + k)
sfx("slap", L(11) + 0.05)
for sel, w in (("#st4a", "tested"), ("#st4b", "live"), ("#st4c", "audience")):
    stamp(sel, T(11, w) - 0.05, -8)
# "You don't have to": the past dims, the phone grows, TEST FIRST in pink
for sel in ("#c4n", "#c4p", "#c4t", "#c4c", "#st4a", "#st4b", "#st4c"):
    to(sel, {"filter": "grayscale(0) brightness(1)"}, {"filter": "grayscale(1) brightness(0.55)"}, L(12) - 0.05, 0.3, "power2.out")
to("#phone", {"scale": 0.5}, {"scale": 0.72}, L(12) - 0.05, 0.4, "back.out(1.6)")
stamp("#st4d", T(12, "have") - 0.05, -8)

# SCAN (L13): iris to clean pink; full phone, scan, brackets, segments
st("#iris", {"opacity": 1}, L(13) - 0.12)
to("#iris", {"clipPath": "circle(0% at 50% 48%)"}, {"clipPath": "circle(140% at 50% 48%)"}, L(13) - 0.12, 0.55, "power2.inOut")
sfx("whoosh", L(13) - 0.12)
for sel in ("#c4n", "#c4p", "#c4t", "#c4c", "#st4a", "#st4b", "#st4c", "#st4d"):
    hide(sel, L(13) + 0.3)
st("#bg", {"backgroundColor": PINKBG}, L(13) + 0.3); hide("#iris", L(13) + 0.45)
st("#paper", {"opacity": 0.22}, L(13) + 0.3)
to("#phone", {"scale": 0.72}, {"scale": 0.92}, L(13) + 0.1, 0.5, "power3.out")
show("#scanlab", L(13) + 0.25); show("#segs", L(13) + 0.25); show("#brk", L(13) + 0.25)
pop("#scanlab", L(13) + 0.25, 0.35, 0, 30, 0.8, None)
to("#brk", {"scale": 1.25, "opacity": 0}, {"scale": 1, "opacity": 1}, L(13) + 0.3, 0.35, "power3.out")
sfx("scan", L(13) + 0.3)
st("#scan", {"opacity": 1}, L(13) + 0.3)
for k in range(5):
    to("#scan", {"top": -120}, {"top": 1030}, L(13) + 0.3 + k * 0.75, 0.75, "none")
hide("#scan", L(14) - 0.1)
seg_t = [L(13) + 0.6, T(13, "tested") - 0.1, T(13, "anyone") + 0.0]
for k, tt in enumerate(seg_t):
    to(f"#sg{k}", {"scaleX": 0}, {"scaleX": 1}, tt, 0.55, "power1.inOut")
    st(f"#sgl{k}", {"color": PINK}, tt + 0.55)
    sfx("tick", tt + 0.5)

# CREEDOM card (L14)
for sel in ("#scanlab", "#segs", "#brk"):
    hide(sel, L(14) - 0.05)
to("#phone", {"y": 0, "scale": 0.92, "opacity": 1}, {"y": -380, "scale": 0.75, "opacity": 0}, L(14) - 0.1, 0.5, "power3.inOut")
flash(L(14) - 0.05, 0.35)
to("#card", {"opacity": 0, "y": 700, "rotation": 6}, {"opacity": 1, "y": 0, "rotation": 0}, T(14, "cred") - 0.2, 0.55, "back.out(1.3)")
sfx("whoosh", T(14, "cred") - 0.2)
count("#scv", 0, 4.2, T(14, "scored") - 0.1, 0.9)
sfx("tick", T(14, "scored") - 0.1)
for k in range(5):
    to(f"#sr{k}", {"scale": 0}, {"scale": 1 if k < 4 else 0.45}, T(14, "scored") + 0.1 + 0.12 * k, 0.25, "back.out(2)")
to("#flg", {"opacity": 0, "x": -80}, {"opacity": 1, "x": 0}, T(14, "hook") - 0.1, 0.35, "power3.out")
sfx("pop", T(14, "hook") - 0.1)
to("#chk", {"opacity": 0, "scaleX": 0.2}, {"opacity": 1, "scaleX": 1}, T(14, "post") - 0.1, 0.4, "back.out(1.6)")
sfx("ding", T(14, "post"))
rr = random.Random(5)
for k in range(14):
    ang = rr.uniform(0, 2 * math.pi); dist = rr.uniform(300, 620)
    to(f"#sp{k}", {"opacity": 1, "x": 0, "y": 0, "scale": 0.4, "rotation": 0},
       {"opacity": 0, "x": round(math.cos(ang) * dist), "y": round(math.sin(ang) * dist), "scale": 1.2, "rotation": rr.randint(-200, 200)},
       T(14, "post") + 0.05, 0.9, "power3.out", pre=False)
sfx("sparkle", T(14, "post") + 0.05)
to("#endl", {"opacity": 0, "y": 60}, {"opacity": 1, "y": 0}, E(14) + 0.35, 0.45, "power3.out")
to("#card", {"y": 0}, {"y": -170}, E(14) + 0.1, 0.5, "power3.inOut")

# ------------------------------------------------------------------ HUD progress (goal gradient)
stops = [("1918", L(3)), ("1930s", L(6)), ("1941", L(7)), ("TODAY", L(9)), ("YOU", L(13))]
hud = '<div id="hud"><i id="hudl"></i><i id="hudf"></i>' + "".join(
    f'<div class="hs" id="hs{k}" style="left:{30 + k * 210}px"><i></i><span>{n}</span></div>' for k, (n, _) in enumerate(stops)) + '</div>'
to("#hudf", {"scaleX": 0}, {"scaleX": 1}, 0, DUR - 1.0, "none")
for k, (n, t) in enumerate(stops):
    col = PINK if k >= 3 else YEL
    st(f"#hs{k} i", {"backgroundColor": col, "scale": 1.35}, t)
    st(f"#hs{k} i", {"scale": 1}, t + 0.15)
    st(f"#hs{k} span", {"color": "#ffffff"}, t)

# ------------------------------------------------------------------ captions (word by word, above Instagram's UI)
script = json.loads((P / "plan/script.json").read_text())
caps = []
cn = 0
CAPT = []
lines = [l for t in script["takes"] for l in t["lines"]]
for ln in lines:
    disp = ln["text"].replace("Creedom,", "Creedom").split()
    wt = words[str(ln["id"])]
    assert len(disp) == len(wt), ln["id"]
    col, fg = (YEL, INK) if ln["id"] <= 8 else (PINK, "#ffffff")
    chunks, cur = [], []
    for i, w in enumerate(disp):
        cur.append(i)
        if len(cur) == 3 or sum(len(disp[j]) for j in cur) > 13 or w[-1] in ".,?":
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    for ch in chunks:
        cid = f"cp{cn}"; cn += 1
        spans = "".join(f'<span id="{cid}w{a}">{disp[i].upper().strip(".,")}</span>' for a, i in enumerate(ch))
        caps.append(f'<div class="cap" id="{cid}">{spans}</div>')
        t0 = wt[ch[0]]["s"] - 0.05
        last = ch[-1]
        t1 = wt[last + 1]["s"] - 0.05 if last + 1 < len(wt) else wt[last]["e"] + 0.3
        CAPT.append([cid, t0, t1])
        for a, i in enumerate(ch):
            ws = wt[i]["s"]; we = wt[i + 1]["s"] if i + 1 < len(wt) else wt[i]["e"] + 0.3
            st(f"#{cid}w{a}", {"backgroundColor": col, "color": fg, "scale": 1.08}, ws)
            st(f"#{cid}w{a}", {"backgroundColor": "rgba(0,0,0,0)", "color": "#f6f3ec", "scale": 1}, we)

for k, (cid, t0, t1) in enumerate(CAPT):
    if k + 1 < len(CAPT):
        t1 = min(t1, CAPT[k + 1][1] - 0.01)
    show(f"#{cid}", t0); hide(f"#{cid}", t1)

# grain boil 12 fps
for k in range(int(DUR * 12)):
    st("#grain", {"backgroundPosition": f"{random.Random(900 + k).randint(0, 540)}px {random.Random(1900 + k).randint(0, 960)}px"}, k / 12)

# ------------------------------------------------------------------ CSS
CSS = f"""
@font-face {{ font-family: Bebas; src: url("assets/fonts/BebasNeue.ttf"); }}
@font-face {{ font-family: Poppins; font-weight: 600; src: url("assets/fonts/Poppins-SemiBold.ttf"); }}
@font-face {{ font-family: Poppins; font-weight: 700; src: url("assets/fonts/Poppins-Bold.ttf"); }}
@font-face {{ font-family: Poppins; font-weight: 800; src: url("assets/fonts/Poppins-ExtraBold.ttf"); }}
@font-face {{ font-family: Mono; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
@font-face {{ font-family: Hand; src: url("assets/fonts/HomemadeApple.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {CREAM}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
#bg {{ position: absolute; inset: 0; background: {CREAM}; }}
#cam {{ position: absolute; inset: 0; }}
.sc {{ position: absolute; inset: 0; opacity: 0; }}
#s3 {{ transform-origin: 431px 767px; }}
.kb {{ position: absolute; inset: 0; transform-origin: 540px 900px; }}
#paper {{ position: absolute; inset: 0; background: url(assets/img/paper.jpg); mix-blend-mode: multiply; opacity: .6; z-index: 80; pointer-events: none; }}
#grain {{ position: absolute; inset: -200px; background: url(assets/img/grain0.png); z-index: 81; pointer-events: none; mix-blend-mode: overlay; }}
#vig {{ position: absolute; inset: 0; z-index: 82; background: radial-gradient(75% 60% at 50% 45%, rgba(0,0,0,0) 55%, rgba(20,10,5,.38) 100%); }}
#flash {{ position: absolute; inset: 0; background: #fffaf0; opacity: 0; z-index: 95; }}
#tear {{ position: absolute; inset: 0; z-index: 90; opacity: 0; }}
#tA, #tB {{ position: absolute; left: -210px; width: 1500px; height: 2000px; }}
#tA {{ top: -40px; }} #tB {{ top: -40px; }}
#wipe {{ position: absolute; left: -100px; top: 0; width: 1280px; height: 2400px; z-index: 90; background: {YEL};
  clip-path: polygon(0 3%, 8% 1.5%, 16% 3.5%, 25% 1%, 34% 3%, 45% .8%, 55% 3.2%, 66% 1.2%, 77% 3.4%, 88% 1%, 100% 3%, 100% 97%, 90% 99%, 78% 96.8%, 66% 99.2%, 54% 97%, 42% 99%, 30% 96.6%, 18% 99%, 8% 97%, 0 99%); }}
#iris {{ position: absolute; inset: 0; z-index: 3; background: {PINKBG}; opacity: 0; clip-path: circle(0% at 50% 48%); }}
.ct {{ position: absolute; filter: drop-shadow(0 18px 22px rgba(0,0,0,.35)); }}
.ct img {{ display: block; }}
.cap-tape {{ position: absolute; left: 50%; bottom: -22px; transform: translateX(-50%) rotate(-2deg); font: 34px Bebas; letter-spacing: .06em; color: {INK};
  padding: 6px 18px; white-space: nowrap; box-shadow: 0 6px 10px rgba(0,0,0,.25); }}
.tape {{ position: absolute; font-family: Bebas; letter-spacing: .06em; padding: 10px 26px; white-space: nowrap; box-shadow: 0 8px 14px rgba(0,0,0,.25); }}
.stamp {{ position: absolute; font-family: Bebas; letter-spacing: .05em; border: 9px solid; border-radius: 16px; padding: 4px 26px 0; white-space: nowrap;
  mix-blend-mode: multiply; }}
.scr {{ position: absolute; overflow: visible; }}
.hand {{ position: absolute; font-family: Hand; white-space: nowrap; }}
.lt {{ display: inline-block; }}
/* S0 */
.t-first {{ position: absolute; top: 345px; width: 100%; text-align: center; font: 170px Bebas; color: {INK}; letter-spacing: .04em; }}
.t-three {{ position: absolute; top: 500px; left: 50%; transform: translateX(-50%); font: 230px Bebas; color: {INK}; white-space: nowrap; padding: 0 40px; }}
.t-three i {{ position: absolute; left: 0; right: 0; top: 18%; bottom: 14%; background: {YEL}; transform-origin: 0 50%; z-index: -1; }}
.t-three span {{ position: relative; }}
/* S1 */
.dots {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(30,26,22,.16) 3px, transparent 3.5px); background-size: 22px 22px; }}
.year {{ position: absolute; top: 345px; left: 50%; transform: translateX(-50%); background: {INK}; color: {YEL}; font: 150px Bebas; padding: 6px 40px 0; z-index: 30; opacity: 0; }}
#y3 {{ background: {YEL}; color: {INK}; }}
.hl {{ position: absolute; left: 3%; width: 94%; top: 30%; height: 34%; background: rgba(242,194,48,.75); mix-blend-mode: multiply; transform-origin: 0 50%; transform: scaleX(0); }}
.callout {{ position: absolute; z-index: 25; background: #fffaf0; padding: 22px 30px; box-shadow: 0 14px 24px rgba(0,0,0,.3); border-left: 14px solid {RED}; }}
.callout b {{ display: block; font: 64px Bebas; color: {INK}; letter-spacing: .03em; }}
.callout span {{ font: 40px Hand; color: {RED}; }}
/* S2 */
#beam {{ position: absolute; left: -200px; top: -200px; width: 1600px; height: 2400px; z-index: 1;
  background: conic-gradient(from 160deg at 85% 0%, rgba(255,235,190,0) 0deg, rgba(255,235,190,.16) 14deg, rgba(255,235,190,.05) 30deg, rgba(255,235,190,0) 40deg); }}
#ybg {{ position: absolute; inset: 0; background: {YEL}; z-index: 2; }}
.ttl {{ position: absolute; top: 340px; width: 100%; text-align: center; font: 110px Bebas; color: {CREAM}; letter-spacing: .06em; z-index: 10; }}
#strip {{ position: absolute; left: 90px; top: 520px; width: 520px; height: 820px; overflow: hidden; z-index: 10; background: #120f0c;
  box-shadow: 0 20px 40px rgba(0,0,0,.5); }}
#strip:before, #strip:after {{ content: ""; position: absolute; top: 0; bottom: 0; width: 44px; z-index: 3;
  background: repeating-linear-gradient(#120f0c 0 18px, #d9ccb2 18px 46px, #120f0c 46px 64px); background-size: 20px 64px; background-repeat: repeat-y; background-position: center; }}
#strip:before {{ left: 0; }} #strip:after {{ right: 0; }}
#stripin {{ position: absolute; inset: 0; }}
.fr {{ position: absolute; left: 60px; width: 400px; height: 360px; overflow: hidden; background: #0c0a08; }}
.fr img {{ width: 100%; height: 100%; object-fit: cover; }}
.fr small {{ position: absolute; left: 14px; bottom: 10px; font: 22px Mono; color: #eadfc6; }}
.endf .end {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font: italic 76px Georgia, serif; color: #efe6d2; }}
.trf {{ background: {YEL}; border: 10px solid {INK}; }}
.trf .ca1 {{ position: absolute; top: 70px; width: 100%; text-align: center; font: 100px Bebas; color: {INK}; }}
.trf .ca2 {{ position: absolute; top: 175px; width: 100%; text-align: center; font: 70px Bebas; color: {RED}; }}
.trf small {{ color: {INK}; }}
.bigword {{ position: absolute; left: 640px; z-index: 20; font: 130px Bebas; background: {YEL}; color: {INK}; padding: 4px 22px 0; transform-origin: 0 50%; }}
.eye {{ position: absolute; width: 74px; height: 46px; z-index: 30; opacity: 0; background: #fffaf0; border: 6px solid {INK}; border-radius: 50%/60%;
  box-shadow: 0 6px 10px rgba(0,0,0,.25); }}
.eye:after {{ content: ""; position: absolute; left: 50%; top: 50%; width: 24px; height: 24px; margin: -12px; border-radius: 50%; background: {INK}; }}
/* S3 */
.grid {{ position: absolute; inset: 0; background-image: linear-gradient(rgba(30,26,22,.07) 2px, transparent 2px), linear-gradient(90deg, rgba(30,26,22,.07) 2px, transparent 2px);
  background-size: 60px 60px; }}
.dateline {{ position: absolute; top: 520px; width: 100%; text-align: center; font: 40px Mono; color: {INK}; z-index: 20; }}
#scr {{ position: absolute; left: 35.2%; top: 10.8%; width: 30%; height: 9%; overflow: hidden; border-radius: 18px; background: #2b2b2b; }}
#static {{ position: absolute; inset: 0; opacity: 0; background-image: url(assets/img/grain1.png), url(assets/img/grain2.png); background-size: 120px 120px; filter: contrast(3) brightness(1.6); }}
#scron {{ position: absolute; inset: 0; opacity: 0; background: #dfe8de; display: flex; align-items: center; justify-content: center; gap: 12px;
  box-shadow: inset 0 0 22px rgba(160,200,255,.9); }}
#scron span {{ font: 30px Bebas; color: {RED}; }}
#mclk {{ position: relative; width: 40px; height: 40px; border: 4px solid #333; border-radius: 50%; }}
#mhand {{ position: absolute; left: 16px; top: 4px; width: 4px; height: 14px; background: #333; transform-origin: 2px 14px; }}
#ring {{ position: absolute; left: 700px; top: 660px; width: 320px; height: 320px; z-index: 20; opacity: 0; }}
#ring b {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font: 150px Bebas; color: {INK}; padding-top: 10px; }}
#ring small {{ position: absolute; left: 0; right: 0; bottom: 64px; text-align: center; font: 34px Bebas; letter-spacing: .14em; color: {INK}; }}
.sticky {{ position: absolute; left: 760px; top: 1020px; width: 240px; height: 230px; background: #ffe56a; z-index: 25; opacity: 0; font: 46px Hand; color: {INK};
  padding: 28px 0 0 30px; box-shadow: 0 16px 22px rgba(0,0,0,.3); line-height: 1.1; }}
.sticky b {{ font: 110px Bebas; color: {RED}; }}
/* S4 */
.pdots {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.22) 4px, transparent 4.5px); background-size: 28px 28px; }}
#feedL, #feedR {{ position: absolute; inset: 0; opacity: 0; }}
.fc {{ position: absolute; width: 220px; height: 400px; border-radius: 28px; opacity: .5; box-shadow: 0 10px 20px rgba(0,0,0,.2); }}
.todayb {{ position: absolute; top: 345px; left: 50%; margin-left: -210px; width: 420px; text-align: center; background: {INK}; color: #fff; font: 128px Bebas;
  padding-top: 8px; z-index: 30; opacity: 0; }}
#phone {{ position: absolute; left: 270px; top: 480px; width: 540px; height: 1080px; border-radius: 74px; background: #0e0e10; z-index: 20;
  box-shadow: 0 40px 70px rgba(0,0,0,.45); transform-origin: 540px 1020px; transform-origin: 50% 50%; }}
#pscr {{ position: absolute; left: 20px; top: 20px; right: 20px; bottom: 20px; border-radius: 58px; overflow: hidden; }}
.reel {{ position: absolute; inset: 0; }}
.r1 {{ background: linear-gradient(150deg, #ff8a50, {PINK}); }}
.r2 {{ background: linear-gradient(150deg, #3c64e6, #22c4b6); }}
.reel b {{ position: absolute; left: 50%; top: 34%; transform: translateX(-50%); background: #fff; color: #1a1020; font: 800 40px Poppins; padding: 22px 30px;
  border-radius: 22px; white-space: nowrap; }}
.ic {{ position: absolute; right: 30px; width: 46px; height: 46px; border-radius: 50%; background: rgba(255,255,255,.9); }}
.ic.a {{ top: 58%; }} .ic.b {{ top: 65%; }} .ic.c {{ top: 72%; }}
.bar1 {{ position: absolute; left: 0; bottom: 0; height: 14px; width: 100%; background: #fff; transform-origin: 0 50%; }}
.notch {{ position: absolute; left: 50%; top: 34px; width: 150px; height: 40px; margin-left: -75px; background: #0e0e10; border-radius: 22px; }}
#thumb {{ position: absolute; left: 290px; top: 760px; width: 150px; height: 150px; border-radius: 50%; background: rgba(255,224,200,.92); border: 6px solid #fff;
  opacity: 0; box-shadow: 0 10px 20px rgba(0,0,0,.3); }}
#scan {{ position: absolute; left: 0; right: 0; height: 120px; top: -120px; opacity: 0;
  background: linear-gradient(rgba(243,67,162,0), rgba(243,67,162,.65)); border-bottom: 8px solid #ffe3f2; }}
.cd {{ position: absolute; left: 800px; top: 640px; width: 230px; height: 260px; text-align: center; font: 250px Bebas; color: #fff; background: {INK};
  padding-top: 18px; z-index: 40; opacity: 0; }}
#scanlab {{ position: absolute; top: 352px; width: 100%; text-align: center; font: 800 52px Poppins; color: #1a1020; z-index: 40; opacity: 0; }}
#segs {{ position: absolute; top: 425px; left: 170px; width: 740px; display: flex; gap: 22px; z-index: 40; opacity: 0; }}
.seg {{ flex: 1; text-align: center; }}
.seg small {{ display: block; font: 700 40px Poppins; color: #b49ab0; margin-bottom: 8px; }}
.seg i {{ display: block; height: 26px; border-radius: 13px; background: #f4cfe2; overflow: hidden; }}
.seg b {{ display: block; height: 100%; background: {PINK}; transform-origin: 0 50%; transform: scaleX(0); }}
#brk {{ position: absolute; left: 236px; top: 510px; width: 608px; height: 1030px; z-index: 39; opacity: 0; }}
#brk i {{ position: absolute; width: 110px; height: 110px; border: 14px solid {PINK}; }}
#brk .b1 {{ left: 0; top: 0; border-right: 0; border-bottom: 0; }} #brk .b2 {{ right: 0; top: 0; border-left: 0; border-bottom: 0; }}
#brk .b3 {{ left: 0; bottom: 0; border-right: 0; border-top: 0; }} #brk .b4 {{ right: 0; bottom: 0; border-left: 0; border-top: 0; }}
#card {{ position: absolute; left: 90px; top: 640px; width: 900px; height: 660px; background: #fff; border-radius: 48px; border: 6px solid {PINK}; z-index: 50;
  box-shadow: 0 40px 70px rgba(120,20,80,.35); opacity: 0; padding: 44px 54px; font-family: Poppins; color: #1a1020; }}
#card .lg {{ height: 60px; }}
#card .ra {{ position: absolute; right: 54px; top: 60px; font: 600 30px Poppins; color: #8a6a86; letter-spacing: .06em; }}
#card .hsc {{ display: block; margin-top: 46px; font: 600 34px Poppins; color: #8a6a86; letter-spacing: .06em; }}
#card .score {{ display: flex; align-items: baseline; gap: 16px; }}
#card .score b {{ font: 800 170px Poppins; line-height: 1; }}
#card .score span {{ font: 700 64px Poppins; color: #8a6a86; }}
#card .ex {{ position: absolute; right: 54px; top: 190px; background: #1a1020; color: #ffc6e0; font: 700 32px Poppins; font-style: normal; padding: 10px 26px; border-radius: 30px; }}
#card .stars {{ position: absolute; right: 54px; top: 270px; display: flex; gap: 10px; }}
#card .stars i {{ width: 40px; height: 40px; border-radius: 50%; background: {PINK}; transform: scale(0); box-shadow: 0 0 0 6px #f6d6e7; }}
.flag {{ margin-top: 30px; display: flex; align-items: center; gap: 22px; background: #fdf1f6; border-radius: 26px; padding: 18px 22px; opacity: 0; }}
.flag i {{ font-style: normal; background: {PINK}; color: #fff; font: 700 34px Poppins; padding: 10px 18px; border-radius: 16px; }}
.flag b {{ font: 700 38px Poppins; }}
.flag span {{ font: 600 30px Poppins; color: #8a6a86; margin-left: auto; }}
.chk {{ margin-top: 24px; background: #1a1020; border-radius: 40px; text-align: center; padding: 20px; opacity: 0; transform-origin: 50% 50%; }}
.chk b {{ font: 700 38px Poppins; color: #ffc6e0; letter-spacing: .03em; }}
#spark {{ position: absolute; left: 540px; top: 1180px; z-index: 55; }}
.sp {{ position: absolute; width: 26px; height: 26px; opacity: 0; background: {PINK}; clip-path: polygon(50% 0, 62% 38%, 100% 50%, 62% 62%, 50% 100%, 38% 62%, 0 50%, 38% 38%); }}
.sp:nth-child(3n) {{ background: {YEL}; }} .sp:nth-child(3n+1) {{ background: #fff; }}
#endl {{ position: absolute; top: 1200px; width: 100%; text-align: center; z-index: 55; opacity: 0; }}
#endl span {{ display: block; font: 700 46px Poppins; color: #1a1020; }}
#endl b {{ display: block; font: 800 104px Poppins; color: {PINK}; }}
/* HUD + captions */
#hud {{ position: absolute; left: 70px; top: 252px; width: 940px; height: 70px; z-index: 96; }}
#hudl, #hudf {{ position: absolute; left: 44px; right: 44px; top: 18px; height: 8px; border-radius: 4px; background: rgba(20,14,10,.35); }}
#hudf {{ background: linear-gradient(90deg, {YEL} 0%, {YEL} 60%, {PINK} 72%, {PINK} 100%); transform-origin: 0 50%; }}
.hs {{ position: absolute; top: 0; width: 88px; text-align: center; }}
.hs i {{ display: block; width: 26px; height: 26px; margin: 9px auto 0; border-radius: 50%; background: #3a3129; border: 4px solid #fffaf0; }}
.hs span {{ display: inline-block; margin-top: 4px; font: 30px Bebas; letter-spacing: .08em; color: rgba(255,250,240,.75); background: rgba(20,14,10,.55);
  padding: 2px 10px 0; border-radius: 6px; }}
.cap {{ position: absolute; left: 0; right: 0; top: 1370px; text-align: center; z-index: 97; opacity: 0; font: 98px Bebas; letter-spacing: .02em; }}
.cap span {{ display: inline-block; color: #f6f3ec; margin: 0 8px; padding: 6px 14px 0; border-radius: 12px; background: rgba(0,0,0,0);
  text-shadow: 0 4px 0 rgba(0,0,0,.55), 0 0 18px rgba(0,0,0,.55); }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>Creedom: The First 3 Seconds (Vox cut-out) 9x16</title>
<script src="assets/vendor/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="42" data-width="1080" data-height="1920">
  <div id="bg"></div>
  <div id="cam">
    {"".join(H)}
    <div id="iris"></div>
  </div>
  <div id="paper"></div><div id="grain"></div><div id="vig"></div>
  <div id="tear"><img id="tA" src="assets/img/tearA.png"><img id="tB" src="assets/img/tearB.png"></div>
  <div id="wipe"></div>
  <div id="flash"></div>
  {hud}
  {"".join(caps)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const __rv = {{}};
const tl = gsap.timeline({{paused: true}});
{chr(10).join(TL)}
{chr(10).join(f'gsap.set("{sel}", {{{k}: {json.dumps(v) if isinstance(v, str) else v}}});' for (sel, k), (t, kind, v) in sorted(EARLY.items()) if kind == "from")}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
(P / "index.html").write_text(html)
(P / "plan/sfx_events.json").write_text(json.dumps(sorted(SFX, key=lambda e: e["t"]), indent=0))
print(f"index.html: {len(TL)} timeline entries, {len(SFX)} sfx events, {cn} caption chunks, duration {DUR}")
