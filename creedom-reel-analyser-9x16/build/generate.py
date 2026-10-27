"""Creedom reel analyser reel. 1080x1920, 33.6 s, cut to the Nota 3 voiceover.

python3 -I build/generate.py      (run from the project root)

Look: Creedom's app (paper #F6F6F4, ink #0B0B0B, pink) on the soft grid-and-pastel-glow background of the reference
covers. All type is Google Sans, the face of the Creedom wordmark; headlines carry one accent in the wordmark's
magenta-to-coral gradient, one hero object, word-by-word captions with a pill on
the spoken word, and the pink bird as the lead: it never stands still (bob, sway, breathing, wing flutter) and changes
gesture on every line (walk, jump, flap, wave, scratch head, shrug, droop, scan, surf, startle, point). Every cut is a
whip pan; one dark beat for the twist. No account handles on screen.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing import DUR, KEY, SCENES, words  # noqa: E402
import bird  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = {k: (a, z) for k, a, z in SCENES}
CGD = "linear-gradient(90deg, #C82BC4, #D23C93 50%, #CF6448)"
PINK, PINKT, INK, PAPER, GREEN = "#E2557D", "#C93A6D", "#0B0B0B", "#F6F6F4", "#3E8E62"
TWIST = S["twist"]
# the hook clip also carries the "why" line, and "next" carries "numbers ≠ reasons"
SPAN = {"hook": (S["hook"][0], S["why"][1]), "next": (S["next"][0], S["nums"][1])}
# giant words behind the action: (start, hold)
KIN_WORDS = ["85x", "WHY?", "~4K", "≠", "20s", "82", "0:34"]
KIN = [(1.3, 1.6), (4.6, .9), (7.1, .8), (9.5, .8), (12.8, 1.0), (15.35, 1.4), (23.35, 1.2)]
CUTS = [S[k][0] for k in ("next", "read", "score", "analyse", "twist", "reasons", "cta")]

T = []
EV = []   # (time, kind[, length]) for every visual event; audio.py gives each one its sound


def ev(t, kind, d=0):
    EV.append((round(t, 3), kind, round(d, 3)))


def add(js):
    T.append("      " + js)


def clip(sid, inner, cls=""):
    a, z = SPAN.get(sid, S[sid])
    return (f'<div id="sc-{sid}" class="clip scene {cls}" data-start="{a}" data-duration="{round(z - a, 3)}" '
            f'data-track-index="{2 + list(S).index(sid) % 2}" data-layout-allow-overflow>{inner}</div>')


def swoosh():
    return ('<svg class="sw" viewBox="0 0 400 40" preserveAspectRatio="none"><path d="M6 28 C90 8 220 6 394 18" '
            f'stroke="{PINK}" stroke-width="9" fill="none" stroke-linecap="round" pathLength="1"/></svg>')


def hl(sid, l1, l2, y=170):
    """Headline: bold line, then the accent in the wordmark gradient with a hand-drawn underline."""
    w1 = "".join(f'<span class="hw">{w}</span> ' for w in l1.split())
    return (f'<div class="hl hl-{sid}" style="top:{y}px"><div class="l1">{w1}</div>'
            f'<div class="l2"><span class="acc">{l2}{swoosh()}</span></div></div>')


def hl_in(sid, t):
    add(f'tl.fromTo(".hl-{sid} .hw",{{y:70,opacity:0,rotation:6}},{{y:0,opacity:1,rotation:0,duration:.45,stagger:.07,'
        f'ease:"back.out(2.2)"}},{t:.2f});')
    add(f'tl.fromTo(".hl-{sid} .acc",{{scale:.3,opacity:0,rotation:-10}},{{scale:1,opacity:1,rotation:0,duration:.55,'
        f'ease:"back.out(2.6)"}},{t + .22:.2f});')
    add(f'tl.fromTo(".hl-{sid} .sw path",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.45,'
        f'ease:"power2.out"}},{t + .55:.2f});')


def pop(sel, t, frm="scale:.6,opacity:0,y:40", d=.45, ease="back.out(2)"):
    ev(t, "pop")
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,rotationY:0,rotationX:0,duration:{d},ease:"{ease}"}},{t:.2f});')


def out(sel, t, to="opacity:0,y:-30", d=.25):
    ev(t, "swish")
    add(f'tl.to("{sel}",{{{to},duration:{d},ease:"power2.in"}},{t:.2f});')


def shine(sel, t):
    ev(t + .15, "glint")
    add(f'tl.fromTo("{sel} > .shine",{{xPercent:-160}},{{xPercent:260,duration:.7,ease:"power2.inOut"}},{t:.2f});')


def ring(cls, t, scale=3.2, d=.7):
    ev(t, "ring")
    add(f'tl.fromTo(".{cls}",{{scale:.2,opacity:.9}},{{scale:{scale},opacity:0,duration:{d},ease:"power2.out"}},{t:.2f});')


def counter(sel, a, z, t, d, fmt="comma", ease="power2.out"):
    f = {"comma": "Math.round(o.v).toLocaleString('en-US')", "int": "Math.round(o.v)"}[fmt]
    ev(t, "count", d * .8)
    add(f'(()=>{{const o={{v:{a}}};tl.to(o,{{v:{z},duration:{d},ease:"{ease}",onUpdate:()=>{{'
        f'document.querySelectorAll("{sel}").forEach(e=>e.textContent={f});}}}},{t:.2f});}})();')


def confetti(cls, n, seed, spread=520, up=-560):
    r = random.Random(seed)
    cols = [PINK, "#F7B267", "#7CC8FF", "#3E8E62", "#F343A2", "#FFD166", "#B39DDB"]
    return f'<div class="conf {cls}" data-layout-ignore>' + "".join(
        f'<i style="background:{r.choice(cols)};width:{r.choice([12, 16, 20])}px;height:{r.choice([10, 22, 28])}px;'
        f'border-radius:{r.choice(["3px", "50%"])}" data-x="{r.uniform(-spread, spread):.0f}" '
        f'data-y="{r.uniform(up, up * .2):.0f}" data-r="{r.uniform(-540, 540):.0f}"></i>' for _ in range(n)) + '</div>'


def confetti_tl(cls, t):
    add(f'document.querySelectorAll(".{cls} i").forEach((e,i)=>{{tl.fromTo(e,{{x:0,y:0,opacity:1,rotation:0,scale:.4}},'
        f'{{x:+e.dataset.x,y:+e.dataset.y,rotation:+e.dataset.r,scale:1,duration:.75,ease:"power3.out"}},{t:.2f}+i*.004);'
        f'tl.to(e,{{y:"+=520",opacity:0,duration:1.1,ease:"power1.in"}},{t + .72:.2f}+i*.004);}});')


# ------------------------------------------------------------------ small art
def ig_icon(s=46, col=INK):
    return (f'<svg viewBox="0 0 48 48" width="{s}" height="{s}"><rect x="4" y="4" width="40" height="40" rx="12" '
            f'fill="none" stroke="{col}" stroke-width="4"/><circle cx="24" cy="24" r="9" fill="none" stroke="{col}" '
            f'stroke-width="4"/><circle cx="35" cy="13" r="2.6" fill="{col}"/></svg>')


def star(s, col=PINK):
    return (f'<svg viewBox="-50 -50 100 100" width="{s}" height="{s}"><path d="M0 -50 C6 -10 10 -6 50 0 C10 6 6 10 '
            f'0 50 C-6 10 -10 6 -50 0 C-10 -6 -6 -10 0 -50 Z" fill="{col}"/></svg>')


def heart(s, col=PINK):
    return (f'<svg viewBox="0 0 40 36" width="{s}" height="{s * .9:.0f}"><path d="M20 35 C8 26 0 19 0 10 C0 4 5 0 10 0 '
            f'C14 0 18 2 20 6 C22 2 26 0 30 0 C35 0 40 4 40 10 C40 19 32 26 20 35 Z" fill="{col}"/></svg>')


def play(s, col=INK):
    return f'<svg viewBox="0 0 40 40" width="{s}" height="{s}"><path d="M10 5 L35 20 L10 35 Z" fill="{col}"/></svg>'


def tick(s=40):
    return (f'<svg viewBox="0 0 40 40" width="{s}" height="{s}"><circle cx="20" cy="20" r="19" fill="#e6f2ea"/>'
            f'<path class="tk" d="M11 20.5 L17.5 27 L29 14" stroke="{GREEN}" stroke-width="3.6" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>')


def comment_ic(s, col=INK):
    return (f'<svg viewBox="0 0 40 40" width="{s}" height="{s}"><path d="M4 6 H36 V28 H16 L8 36 V28 H4 Z" fill="{col}"/></svg>')


# ------------------------------------------------------------------ depth fields: things flying past the camera
LATER = []   # timeline code registered while the HTML is built; timeline() adds it


def depth(cls, items, seed, t0, t1, life=1.3, rev=False, spread=(760, 1150), vp=(540, 900), zmax=2.3, sound_every=3):
    """Fake 3D fly-through: each item starts tiny at the vanishing point and accelerates out past the camera
    (or, with rev, streams in from the edges and shrinks into the point)."""
    import math
    r = random.Random(seed)
    html = [f'<div class="df {cls}" data-layout-ignore style="left:{vp[0]}px;top:{vp[1]}px">']
    n = len(items)
    for i, it in enumerate(items):
        a = (i * 2.399 + r.uniform(-.3, .3)) % math.tau          # golden-angle spread so items never bunch up
        k = r.uniform(.6, 1.0)
        dx, dy = math.cos(a) * spread[0] * k, math.sin(a) * spread[1] * k
        ts = t0 + (t1 - t0 - life) * i / max(1, n - 1)
        html.append(f'<div class="dfi dfi{i}">{it}</div>')
        sel = f".{cls} .dfi{i}"
        near = f'x:{dx * 1.5:.0f},y:{dy * 1.5:.0f},scale:{zmax}'
        far = f'x:{dx * .05:.0f},y:{dy * .05:.0f},scale:.05'
        a_, b_ = (near, far) if rev else (far, near)
        LATER.append(f'tl.fromTo("{sel}",{{{a_},xPercent:-50,yPercent:-50}},{{{b_},xPercent:-50,yPercent:-50,duration:{life},'
                     f'ease:"{"power2.out" if rev else "power2.in"}",immediateRender:false}},{ts:.2f});')
        LATER.append(f'tl.to("{sel}",{{opacity:1,duration:{life * .25:.2f}}},{ts:.2f});'
                     f'tl.to("{sel}",{{opacity:0,duration:{life * .22:.2f}}},{ts + life * .78:.2f});')
        if i % sound_every == 0:
            ev(ts + life * (.25 if rev else .7), "fly")
    return "".join(html) + "</div>"


def mini_reel(img):
    return f'<div class="mreel"><img src="assets/img/{img}" alt=""></div>'


# ------------------------------------------------------------------ the film strip (inside the reel)
# (time, icon, label, score out of 5, segment colour)
FRAMES = [("0:00", "⚡", "Hook", 3, "#3E8E62"), ("0:05", "🧩", "Skills grid", 2, "#C8902E"), ("0:10", "🧩", "Skills grid", 2, "#C8902E"),
          ("0:15", "🗂️", "Tool tour", 3, "#C8902E"), ("0:19", "⏳", "Time machine", 3, "#3E8E62"),
          ("0:24", "⏳", "Simulation", 3, "#3E8E62"), ("0:29", "📈", "Simulation", 3, "#3E8E62"),
          ("0:34", "🏛️", "Congress tracker", 5, "#F2B134"), ("0:41", "👋", "Close", 2, "#3E8E62")]
FR_W, FR_GAP, FR_PAD = 230, 40, 40
FR_X0 = 540 - (FR_PAD + FR_W / 2)       # strip x that puts frame 0 under the lens


def frame_html(i, cls="fr"):
    ts, ic, lab, sc, col = FRAMES[i]
    dots = "".join(f'<i class="{"on" if k < sc else ""}"></i>' for k in range(5))
    return (f'<div class="{cls} {cls}{i}" style="--c:{col}"><div class="frt">{ts}</div><div class="fri">{ic}</div>'
            f'<div class="frl">{lab}</div><div class="frs">{dots}</div></div>')


def strip():
    w = FR_PAD * 2 + len(FRAMES) * FR_W + (len(FRAMES) - 1) * FR_GAP
    att = [.5, .32, .28, .36, .42, .4, .48, .97, .3]
    pts = " ".join(f'{FR_PAD + FR_W / 2 + i * (FR_W + FR_GAP):.0f},{70 - v * 62:.0f}' for i, v in enumerate(att))
    frames = "".join(f'<div class="frw" style="left:{FR_PAD + i * (FR_W + FR_GAP)}px">{frame_html(i)}</div>' for i in range(len(FRAMES)))
    return (f'<div class="fsw"><div class="fs3d"><div class="fsr" style="width:{w}px">{frames}'
            f'<svg class="attw" viewBox="0 0 {w} 80" width="{w}" height="80"><polyline class="att" points="{pts}" '
            f'fill="none" stroke="#FF5FA2" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" pathLength="1"/></svg>'
            f'</div></div></div>')


# live reactions drifting up both edges, Instagram-live style: (start time, side)
REACT_T = [round(.9 + i * .62, 2) for i in range(52) if not (S["twist"][0] - .3 < .9 + i * .62 < S["twist"][1] - .6)]


REACT_SW = []


def reactions():
    r = random.Random(12)
    out_ = []
    REACT_SW.clear()
    for i, t in enumerate(REACT_T):
        side = i % 2
        x = r.uniform(24, 110) if side == 0 else r.uniform(950, 1010)
        kind = r.choice(["h", "h", "h", "p", "c", "s"])
        col = r.choice([PINK, "#E235DD", "#E68B70", "#F343A2"])
        art = {"h": heart(r.choice([46, 56, 64]), col), "p": play(44, col), "c": comment_ic(44, col),
               "s": star(48, "#F2B134")}[kind]
        REACT_SW.append(r.uniform(-60, 60))
        out_.append(f'<div class="rx rx{i}" style="left:{x:.0f}px">{art}</div>')
    return "".join(out_)


# ------------------------------------------------------------------ scenes
def cover(cls, img, cnt_cls, label):
    return (f'<div class="cover card {cls}"><img src="assets/img/{img}" alt=""><i class="shine"></i></div>'
            f'<div class="vbar {cls}-v">{play(26, "#fff")}<span class="{cnt_cls}">0</span><span class="plab">{label}</span></div>')


# the analysed reel's segments (label, width, colour): before, the best part sits at 0:34
SEGS = [("Hook", 120, "#3E8E62"), ("Skills", 230, "#C8902E"), ("Time machine", 250, "#3E8E62"), ("★ Congress", 160, "#E2557D"),
        ("Close", 80, "#7a7a74")]
SEG_AFTER = [3, 0, 1, 2, 4]


def scenes():
    r = random.Random(4)
    burst = "".join(f'<div class="bst" data-x="{r.uniform(-360, 360):.0f}" data-y="{r.uniform(-460, -120):.0f}" '
                    f'data-r="{r.uniform(-90, 90):.0f}">{heart(r.choice([34, 44, 56])) if i % 3 else play(36, PINK)}</div>'
                    for i in range(18))
    ticker = " • ".join(["366K PLAYS", "85x YOUR USUAL", "+1 VIRAL REEL", "WHY?"] * 4)
    out_ = []
    out_.append(clip("hook", (
        '<div class="ghost" data-layout-ignore>85x</div>'
        f'<div class="ticker" data-layout-ignore><div class="tk-in">{ticker} • {ticker}</div></div>' +
        hl("hook", "One reel did", "85x.") + hl("why", "And I had", "no idea why.") +
        cover("cv-a", "cover_yt.jpg", "cnt-a", "plays") +
        f'<div class="burst" data-layout-ignore>{burst}</div><div class="rg85 pring" data-layout-ignore></div>'
        f'<div class="chart card"><div class="mono">PLAYS · LAST 30 DAYS</div><svg viewBox="0 0 380 250" width="380" '
        f'height="250"><path d="M0 230 H380" stroke="#e6e6e2" stroke-width="2"/><path class="spk" '
        f'd="M0 230 L60 222 L120 226 L180 214 L240 220 L300 205 L330 40 L360 8" stroke="{PINK}" stroke-width="7" '
        f'fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>'
        f'<circle class="spkdot" cx="360" cy="8" r="11" fill="{PINK}"/></svg>'
        f'<div class="chip pinkchip c85">85x your usual</div><i class="shine"></i></div>'
        '<div class="sticker st-eyes" data-layout-ignore>👀</div><div class="sticker st-fire" data-layout-ignore>🔥</div>'
    )))
    tiles = [("PLAYS", "366K"), ("PLAYS", "4.3K"), ("REACH", "↑ ↓"), ("SAVES", "?"), ("SHARES", "?"), ("WATCH TIME", "?")]
    out_.append(clip("next", (
        '<div class="ghost" data-layout-ignore>4K</div>' +
        hl("next", "The next one?", "~4K.") + hl("nums", "Numbers ≠", "reasons.") +
        '<div class="mini card"><img src="assets/img/cover_yt.jpg" alt=""><div class="mono">366K plays</div></div>' +
        cover("cv-b", "cover_adobe.jpg", "cnt-b", "plays") +
        '<div class="chip redchip lowk">↓ low thousands</div><div class="arrowdn" data-layout-ignore>↓</div>'
        '<div class="grid6">' + "".join(f'<div class="tile card t{i}"><div class="mono">{a}</div><div class="tv tv{i}">{b}</div>'
                                        f'<div class="tb" style="width:{40 + (i * 37) % 50}%"></div></div>'
                                        for i, (a, b) in enumerate(tiles)) + '</div>'
    )))
    rows = [("Found your page: 6,205 followers", "r1"), ("Scanned 6 recent posts", "r2"), ("Creator audit ready", "r3")]
    out_.append(clip("read", (
        '<div class="ghost" data-layout-ignore>20</div>'
        '<div class="link"><div class="appic ig">' + ig_icon(92, "#fff") + '</div>'
        '<svg class="dash" viewBox="0 0 420 20" width="420" height="20"><path d="M0 10 H420" stroke="' + PINK + '" '
        'stroke-width="5" stroke-dasharray="14 12" fill="none"/></svg>'
        '<div class="lpill">◉ Public data only</div>'
        '<div class="radar"></div><div class="rpulse rp0"></div><div class="rpulse rp1"></div><div class="rpulse rp2"></div>'
        '<div class="appic cr"><img src="assets/img/bird.png" alt=""></div>'
        + "".join(f'<i class="ddot dd{i}"></i>' for i in range(6)) +
        '<div class="orbit">' + "".join(f'<div class="ob ob{i}">{star(42 if i % 2 else 34, "#F2B134" if i % 2 else PINK)}</div>'
                                        for i in range(4)) + '</div></div>'
        '<div class="crlogo"><img src="assets/img/creedom_logo.png" alt="Creedom"></div><div class="reading mono">READING YOUR PAGE</div>'
        '<div class="give">Give me <i>20 seconds.</i></div>'
        '<div class="rbar"><div class="rfill"></div></div>'
        '<div class="ticks card">' + "".join(f'<div class="trow {c}">{tick(46)}<span>{t}</span></div>' for t, c in rows) +
        '<i class="shine"></i></div><div class="chip stopw">⏱ <span class="cnt-s">0</span>s</div><div class="rg20 pring" '
        'data-layout-ignore></div>'
    )))
    thumbs = ('<div class="orb3d"><div class="orbr">' + "".join(
        f'<div class="th th{i}" style="transform:rotateY({i * 60}deg) translateZ(400px)"><img src="assets/img/post{i + 1}.jpg" alt=""></div>'
        for i in range(6)) + '</div></div><div class="rays rays82" data-layout-ignore></div>')
    out_.append(clip("score", (
        '<div class="ghost" data-layout-ignore>82</div>' + hl("score", "Content", "score.") + thumbs +
        '<div class="scard"><div class="mono sl">YOUR CONTENT SCORE</div>'
        '<div class="snum"><span class="cnt-sc">0</span><small>/ 100</small></div>'
        '<svg class="ring" viewBox="0 0 200 200" width="200" height="200"><circle cx="100" cy="100" r="80" '
        'stroke="#2a2a2a" stroke-width="16" fill="none"/><circle class="rg" cx="100" cy="100" r="80" stroke="' + PINK +
        '" stroke-width="16" fill="none" stroke-linecap="round" pathLength="1" transform="rotate(-90 100 100)"/></svg>'
        '<div class="mono sl2">YOUR TOP INSIGHT</div><div class="sins">The next job is <i>repeatability.</i></div>'
        '<i class="shine"></i></div><div class="rg82 pring" data-layout-ignore></div>' + confetti("cf82", 46, 5)
    )))
    tl_rows = [("Hook", "0:00–0:05", "5", GREEN), ("Skills Grid &amp; Tour", "0:05–0:19", "3", "#C8902E"),
               ("Time Machine Simulation", "0:19–0:34", "5", GREEN), ("Safety &amp; Congress Tracker", "0:34–0:41", "4", GREEN),
               ("Close", "0:41–0:46", "4", GREEN)]

    def timeline(cls):
        return (f'<div class="tlc card {cls}"><div class="tlh"><span class="mono">SECOND BY SECOND</span>'
                f'<span class="sc42">4.2<small>/5</small> · Very good</span></div><div class="tline"></div>'
                f'<div class="phd"></div>' +
                "".join(f'<div class="tr tr{i}" style="top:{120 + i * 150}px"><span class="dot" style="background:{c}"></span>'
                        f'<b>{n}</b><span class="tt tt{i}">{t}</span><span class="ts">{s}</span></div>'
                        for i, (n, t, s, c) in enumerate(tl_rows)) + '</div>')
    out_.append(clip("analyse", (
        '<div class="ghost" data-layout-ignore>▶</div>' + hl("analyse", "Then its", "reel analyser.") +
        '<div class="ubub"><span class="ubt">Check “Comment TRADE and I\'ll DM you all 11 skills.”</span></div>'
        '<div class="onit card"><div class="mono oh"><img src="assets/img/bird.png" alt=""> CREEDOM · ON IT</div>' +
        "".join(f'<div class="orow o{i}">{tick(40)}<span>{t}</span></div>' for i, t in enumerate(
            ["Working out what you need…", "Sending the reel to the feedback engine…", "Watching the whole video…"])) +
        '<i class="shine"></i></div><div class="scanph"><img src="assets/img/post2.jpg" alt=""><div class="scanl"></div></div>' +
        depth("dfa", [f'<div class="mfr" style="--c:{FRAMES[i % 9][4]}">{FRAMES[i % 9][1]}</div>' for i in range(10)], 24, 18.1,
              19.75, .75, rev=True, spread=(620, 700), vp=(940, 925), zmax=1.6, sound_every=2) +
        timeline("tl-a")
    )))
    out_.append(clip("twist", (
        '<div class="ghost gw" data-layout-ignore>0:34</div><div class="rays rays34" data-layout-ignore></div>' + strip() +
        '<div class="fdim" data-layout-ignore></div>'
        '<div class="lensg"><div class="lens"><div class="lensin">' + strip() + '</div><div class="lglint"></div></div>'
        '<div class="lring"></div><div class="lhandle"></div></div>' +
        hl("twist", "Buried at", "0:34.") + '<div class="scanlab">◉ SCANNING FRAME BY FRAME…</div>' +
        f'<div class="flycard">{frame_html(7, "fc")}</div>'
        '<div class="chip pinkchip besth">★ BEST HOOK</div><div class="chip newh">✓ NOW AT 0:00</div>'
        '<div class="rg34 pring" data-layout-ignore></div>' + confetti("cf34", 34, 8, 460, -420)
    ), "dark"))
    out_.append(clip("reasons", (
        '<div class="ghost" data-layout-ignore>✓</div>' + hl("reasons", "Now I edit with", "reasons.") +
        '<div class="segbar">' + "".join(f'<div class="seg sg{i}" style="width:{w}px;background:{c}">{lab}</div>' for i, (lab, w, c) in
                                         enumerate(SEGS)) + '</div>' +
        '<div class="gcard card"><div class="mono">GUESSES</div><div class="dice"><span class="d1">🎲</span> '
        '<span class="d2">🎲</span></div><div class="gq2"><span>?</span> <span>?</span> <span>?</span></div>'
        '<div class="strike"></div></div>'
        '<div class="rcard card"><div class="mono pk">REASONS · FROM CREEDOM</div>'
        f'<div class="rr rr0">{tick(40)}<span>Lead with the Congress tracker</span></div>'
        f'<div class="rr rr1">{tick(40)}<span>Trim two tool cards (0:10–0:19)</span></div>'
        f'<div class="rr rr2">{tick(40)}<span>Keep the 0:03 simulation proof</span></div><i class="shine"></i></div>'
    )))
    out_.append(clip("cta", (
        '<div class="cmt"><svg viewBox="0 0 40 40" width="48" height="48"><path d="M4 6 H36 V28 H16 L8 36 V28 H4 Z" '
        'fill="#fff"/></svg>COMMENT</div>'
        '<div class="cbox card"><div class="mono">TYPE THIS UNDER THE REEL</div><div class="cin"><span class="typed"></span>'
        '<span class="caret"></span></div><div class="send"><svg viewBox="0 0 40 40" width="48" height="48"><path d="M4 20 '
        'L36 6 L28 36 L19 23 Z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/></svg></div>'
        '<div class="dm">✓ The link lands in your DMs</div><i class="shine"></i></div><div class="rgkw pring" data-layout-ignore></div>'
        '<div class="plane" data-layout-ignore><svg viewBox="0 0 60 60" width="70" height="70"><path d="M4 30 L56 6 L44 54 '
        f'L30 36 Z" fill="{PINK}"/><path d="M30 36 L56 6" stroke="#fff" stroke-width="3"/></svg></div>' +
        confetti("cfkw", 40, 11) + depth("dfh", [heart(r.choice([50, 64, 80]), r.choice([PINK, "#E235DD", "#E68B70"])) for _ in range(10)],
                                         25, 32.0, DUR, 1.3, zmax=2.2, sound_every=4) +
        '<div class="endlock"><img src="assets/img/creedom_logo.png" alt="Creedom"><div class="eshine"><i></i></div></div>'
        + "".join(f'<div class="esp esp{i}" data-layout-ignore style="left:{x}px;top:{y}px">{star(sz, c)}</div>'
                  for i, (x, y, sz, c) in enumerate([(130, 330, 40, PINK), (930, 350, 34, "#F2B134"), (240, 520, 26, "#E68B70"),
                                                     (860, 520, 44, "#E235DD"), (540, 300, 24, "#F2B134"), (60, 460, 30, "#E235DD")])) +
        '<div class="endsub">Your reels, <b>explained.</b></div>'
    )))
    return "".join(out_)


# ------------------------------------------------------------------ captions
def caption_chunks():
    """Group the spoken words into on-screen lines of at most 4 words, never across a phrase."""
    ws = words()
    chunks, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        if len(cur) == 4 or nxt is None or nxt[0] - w[1] > .2:
            chunks.append(cur)
            cur = []
    return chunks


def captions():
    html = []
    for ci, ch in enumerate(caption_chunks()):
        html.append(f'<div class="cap cap{ci}">' + "".join(
            f'<span class="cw cw{ci}_{wi}">{w.rstrip(".,:?")}</span> ' for wi, (_, _, w) in enumerate(ch)) + '</div>')
    return "".join(html)


def caption_tl():
    chunks = caption_chunks()
    for ci, ch in enumerate(chunks):
        a = ch[0][0]
        z = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else DUR
        z = min(z, ch[-1][1] + .6)
        add(f'tl.set(".cap{ci}",{{opacity:1}},{a:.3f});tl.set(".cap{ci}",{{opacity:0}},{z:.3f});')
        for wi, (s, e, w) in enumerate(ch):
            dark = TWIST[0] <= s < TWIST[1]
            ink = "#ffffff" if dark else INK
            past = ("#FF8FAE" if dark else PINKT) if w in KEY else ink
            sel = f".cw{ci}_{wi}"
            add(f'tl.fromTo("{sel}",{{opacity:0,y:18,scale:.85}},{{opacity:1,y:0,scale:1,duration:.16,ease:"back.out(3)",'
                f'immediateRender:false}},{s:.3f});')
            add(f'tl.set("{sel}",{{backgroundImage:"{CGD}",color:"#ffffff"}},{s:.3f});')
            add(f'tl.set("{sel}",{{backgroundImage:"none",color:"{past}"}},{e:.3f});')


# ------------------------------------------------------------------ scene timelines
def timeline():
    add('tl.set("#wipe",{scale:0},0);tl.set("#speed, #flash",{opacity:0},0);')
    # a different transition on every cut: whips (left / up), zoom-throughs and a spin
    for t, kind in zip(CUTS, ["whipx", "whipx", "zoom", "whipy", "zoom", "spin", "whipy"]):
        if kind == "whipx":
            add(f'tl.to("#cam",{{x:-160,filter:"blur(12px)",duration:.12,ease:"power2.in"}},{t - .12:.2f});')
            add(f'tl.fromTo("#cam",{{x:180,filter:"blur(14px)"}},{{x:0,filter:"blur(0px)",duration:.44,ease:"expo.out",immediateRender:false}},{t:.2f});')
        elif kind == "whipy":
            add(f'tl.to("#cam",{{y:-200,filter:"blur(12px)",duration:.12,ease:"power2.in"}},{t - .12:.2f});')
            add(f'tl.fromTo("#cam",{{y:240,filter:"blur(14px)"}},{{y:0,filter:"blur(0px)",duration:.46,ease:"expo.out",immediateRender:false}},{t:.2f});')
        elif kind == "zoom":
            add(f'tl.to("#cam",{{scale:1.7,filter:"blur(16px)",opacity:.4,duration:.14,ease:"power2.in"}},{t - .14:.2f});')
            add(f'tl.fromTo("#cam",{{scale:.7,filter:"blur(14px)",opacity:.4}},{{scale:1,filter:"blur(0px)",opacity:1,duration:.48,'
                f'ease:"expo.out",immediateRender:false}},{t:.2f});')
        else:
            add(f'tl.to("#cam",{{rotation:8,scale:1.25,filter:"blur(12px)",duration:.13,ease:"power2.in"}},{t - .13:.2f});')
            add(f'tl.fromTo("#cam",{{rotation:-8,scale:.8,filter:"blur(12px)"}},{{rotation:0,scale:1,filter:"blur(0px)",duration:.5,'
                f'ease:"back.out(1.4)",immediateRender:false}},{t:.2f});')
        add(f'tl.fromTo("#whip",{{opacity:.9,x:300}},{{opacity:0,x:-300,duration:.28,ease:"power2.out",immediateRender:false}},{t - .08:.2f});')
    # impacts on the big beats: punch-in, camera shake, white flash, speed-line burst
    for t, k in [(1.35, 1), (7.25, .6), (8.35, .8), (12.85, .7), (15.4, 1), (23.4, 1), (24.75, .7), (25.3, .8), (30.72, 1), (32.2, .6)]:
        add(f'tl.fromTo("#shake",{{x:0,y:0,rotation:0}},{{x:{14 * k:.0f},y:{-10 * k:.0f},rotation:{1.4 * k:.1f},duration:.04,'
            f'ease:"none",yoyo:true,repeat:5,immediateRender:false}},{t:.2f});')
        add(f'tl.set("#flash",{{opacity:{.55 * k:.2f}}},{t:.2f});tl.to("#flash",{{opacity:0,duration:.25,ease:"power2.out"}},{t + .01:.2f});')
        add(f'tl.set("#speed",{{scale:.5,opacity:{.9 * k:.2f},rotation:0}},{t:.2f});tl.to("#speed",{{scale:1.5,opacity:0,rotation:8,'
            f'duration:.45,ease:"power2.out"}},{t + .01:.2f});')
    # giant kinetic words racing past behind the content on the key lines
    for i, (t, d) in enumerate(KIN):
        add(f'tl.fromTo(".kin{i}",{{scale:2.6,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:0,duration:.35,ease:"expo.out"}},{t:.2f});')
        add(f'tl.to(".kin{i}",{{scale:.85,opacity:0,duration:.35,ease:"power2.in"}},{t + d:.2f});')
    # a tiny kick on every highlighted word
    hits = [t for t, _ in [(1.33, 0), (15.4, 0), (23.4, 0), (29.8, 0)]]
    for (st, en, w) in words():
        if w in KEY and all(abs(st - h) > .45 for h in hits):
            add(f'tl.to("#punch",{{scale:1.025,duration:.08,ease:"power2.out",yoyo:true,repeat:1}},{st:.2f});')
    # cards float in 3D so the frame never sits still (each starts once its entrance has landed)
    for sel, a, t0, t1 in ((".cv-a", 6, 1.0, 5.6), (".chart", 6, 1.1, 5.6), (".cv-b", 6, 6.45, 8.1), (".scard", 4, 15.85, 17.1),
                           (".tl-a", 3, 20.35, 21.3), (".rcard", 5, 27.15, 29.4), (".gcard", 5, 26.95, 28.4), (".cbox", 3, 30.5, 32.0)):
        n = max(1, int((t1 - t0) / 1.2))
        add(f'tl.fromTo("{sel}",{{rotationY:{-a}}},{{rotationY:{a},duration:1.2,ease:"sine.inOut",yoyo:true,repeat:{n - 1},'
            f'immediateRender:false}},{t0:.2f});')
    # rising particles
    add(f'document.querySelectorAll(".pt").forEach((e,i)=>tl.fromTo(e,{{y:0,opacity:0}},{{y:-900,opacity:.8,duration:{{}},'
        f'ease:"none",repeat:4}},i*.37));'.replace("{{}}", "4.2"))
    # slow push-in inside each scene so nothing is ever static
    for k, a, z in SCENES:
        add(f'tl.fromTo("#shake",{{scale:1}},{{scale:1.035,duration:{z - a - .05:.2f},ease:"none",immediateRender:false}},{a:.2f});')
    # 1 hook
    hl_in("hook", .05)
    pop(".cv-a", .15, "y:260,opacity:0,rotation:-8,rotationY:40,scale:.8", .6)
    shine(".cv-a", .7)
    pop(".cv-a-v", .5, "y:40,opacity:0,scale:.8", .35)
    counter(".cnt-a", 0, 366000, .4, 2.6, "comma", "expo.out")
    pop(".chart", .55, "x:200,opacity:0,scale:.8,rotationY:-40", .5)
    shine(".chart", 1.0)
    add('tl.fromTo(".spk",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:1.1,ease:"power3.in"},.75);')
    pop(".spkdot", 1.8, "scale:0,opacity:0", .3)
    pop(".c85", 1.4, "scale:.3,opacity:0,rotation:-10", .45, "back.out(3)")
    ring("rg85", 1.4)
    add('document.querySelectorAll(".bst").forEach((e,i)=>{tl.fromTo(e,{x:0,y:0,opacity:0,scale:.3},{x:+e.dataset.x,'
        'y:+e.dataset.y,opacity:1,scale:1,rotation:+e.dataset.r,duration:.9,ease:"power3.out"},1.35+i*.03);'
        'tl.to(e,{opacity:0,duration:.4},2.4+i*.03);});')
    add('tl.fromTo("#sc-hook .ghost",{scale:.8,opacity:0},{scale:1,opacity:1,duration:1.2,ease:"power2.out"},0);')
    add('tl.fromTo(".ticker",{opacity:0,y:-30},{opacity:1,y:0,duration:.3},.3);tl.fromTo(".tk-in",{x:0},{x:-1400,duration:5.2,ease:"none"},.3);')
    pop(".st-eyes", 1.55, "scale:0,opacity:0,rotation:-40", .4, "back.out(3)")
    pop(".st-fire", 1.75, "scale:0,opacity:0,rotation:40", .4, "back.out(3)")
    add('tl.to(".st-eyes, .st-fire",{y:-14,duration:.5,ease:"sine.inOut",yoyo:true,repeat:5},2.2);')
    add('tl.to("#punch",{scale:1.07,duration:.22,ease:"power2.out",yoyo:true,repeat:1},1.33);')
    # 2 why (same clip)
    out(".hl-hook, .ticker, .st-eyes, .st-fire", 3.4)
    hl_in("why", 3.6)
    add('tl.to(".cv-a, .cv-a-v, .chart",{filter:"grayscale(1) brightness(1.05)",opacity:.5,rotation:(i)=>[-4,-4,5][i],'
        'y:30,duration:.5},3.6);')
    add('tl.to("#sc-hook .ghost",{opacity:0,duration:.3},3.5);')
    # 3 next
    hl_in("next", S["next"][0] + .05)
    pop(".mini", 5.7, "x:-200,opacity:0,scale:.8,rotation:-20", .45)
    pop(".cv-b", 5.85, "y:300,opacity:0,rotation:6,rotationY:-40,scale:.8", .55)
    shine(".cv-b", 6.3)
    pop(".cv-b-v", 6.0, "y:40,opacity:0,scale:.8", .35)
    counter(".cnt-b", 0, 4335, 6.0, 1.6, "comma", "power1.out")
    pop(".lowk", 7.2, "scale:.3,opacity:0", .4, "back.out(3)")
    pop(".arrowdn", 7.25, "y:-80,opacity:0", .35, "bounce.out")
    add('tl.to(".arrowdn",{y:24,duration:.25,yoyo:true,repeat:3,ease:"sine.inOut"},7.6);')
    add('tl.to(".cv-b",{x:-6,duration:.05,yoyo:true,repeat:5},7.4);')
    # 4 numbers
    out(".hl-next", 8.05)
    out(".mini, .cv-b, .cv-b-v, .lowk, .arrowdn", 8.1, "opacity:0,scale:.85")
    hl_in("nums", 8.25)
    add('tl.fromTo(".tile",{opacity:0,scale:.4,y:-300,rotation:(i)=>[-12,8,-6,10,-9,7][i]},{opacity:1,scale:1,y:0,rotation:(i)=>'
        '[-4,3,-2,4,-3,2][i],duration:.45,stagger:.07,ease:"back.out(2)"},8.3);')
    add('(()=>{const o={v:0};const g=["?","%","↑","—","#","∞","?"];tl.to(o,{v:30,duration:1.0,ease:"none",onUpdate:()=>{'
        'const k=Math.floor(o.v);[3,4,5].forEach((j,n)=>{document.querySelector(".tv"+j).textContent=g[(k+n*3)%g.length];});}},8.6);})();')
    add('tl.to(".grid6",{x:8,duration:.05,yoyo:true,repeat:7},9.0);')
    add('tl.to(".tile",{filter:"blur(14px)",opacity:.2,scale:.8,y:(i)=>(i%2?60:-60),x:(i)=>(i%2?80:-80),rotation:(i)=>(i%2?20:-20),'
        'duration:.5,stagger:.03,ease:"power2.in"},9.5);')
    # 5 read
    t = S["read"][0]
    for k in range(6):
        tk = t - .55 + k * .07
        add(f'tl.fromTo(".prg{k}",{{scale:.05,opacity:0}},{{scale:6,opacity:1,duration:.5,ease:"power2.in",immediateRender:false}},{tk:.2f});'
            f'tl.to(".prg{k}",{{opacity:0,duration:.12}},{tk + .42:.2f});')
    ev(t - .55, "portal")
    add(f'tl.fromTo(".radar",{{rotation:0,opacity:0}},{{rotation:900,opacity:1,duration:3.3,ease:"none",immediateRender:false}},{t + .3:.2f});')
    for k in range(3):
        add(f'tl.fromTo(".rp{k}",{{scale:.6,opacity:.9}},{{scale:2.6,opacity:0,duration:1.1,repeat:2,ease:"power2.out",immediateRender:false}},'
            f'{t + .4 + k * .37:.2f});')
    add(f'tl.fromTo("#wipe",{{scale:0}},{{scale:1,duration:.38,ease:"power3.in",immediateRender:false}},{t - .35:.2f});')
    add(f'tl.to("#wipe",{{opacity:0,duration:.3}},{t + .05:.2f});tl.set("#wipe",{{scale:0,opacity:1}},{t + .4:.2f});')
    pop(".appic.ig", t + .05, "scale:0,opacity:0,rotation:-30", .45, "back.out(2.6)")
    pop(".appic.cr", t + .15, "scale:0,opacity:0,rotation:30", .45, "back.out(2.6)")
    add(f'tl.fromTo(".dash",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power2.out"}},{t + .3:.2f});')
    add(f'tl.fromTo(".dash path",{{strokeDashoffset:0}},{{strokeDashoffset:-260,duration:3.2,ease:"none"}},{t + .3:.2f});')
    pop(".lpill", t + .55, "scale:.3,opacity:0", .4, "back.out(3)")
    pop(".crlogo", t + .2, "opacity:0,scale:.6", .4, "back.out(2.4)")
    pop(".reading", t + .3, "opacity:0,y:20", .35)
    pop(".give", t + .4, "opacity:0,y:40,scale:.9", .5)
    pop(".rbar", t + .6, "opacity:0,scaleX:.6", .3)
    add(f'tl.fromTo(".rfill",{{scaleX:0}},{{scaleX:1,duration:2.9,ease:"power1.inOut"}},{t + .7:.2f});')
    pop(".ticks", t + .85, "y:120,opacity:0,scale:.9", .45)
    shine(".ticks", 11.3)
    for i, tt in enumerate((11.5, 12.15, 12.95)):
        pop(f".trow.r{i + 1}", tt, "x:-60,opacity:0", .35)
        add(f'tl.fromTo(".trow.r{i + 1} .tk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.3}},{tt + .1:.2f});')
    pop(".stopw", 12.8, "scale:.3,opacity:0,rotation:-15", .4, "back.out(3)")
    ring("rg20", 12.85)
    counter(".cnt-s", 0, 20, 12.82, .7, "int", "power1.out")
    add('tl.fromTo("#sc-read .ghost",{opacity:0,scale:.8},{opacity:1,scale:1,duration:1,ease:"power2.out"},12.8);')
    # 6 score
    t = S["score"][0]
    hl_in("score", t + .05)
    add(f'tl.fromTo(".orb3d",{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.4,ease:"back.out(1.6)",immediateRender:false}},{t + .1:.2f});')
    add(f'tl.fromTo(".orbr",{{rotationY:0}},{{rotationY:300,duration:1.25,ease:"power1.inOut",immediateRender:false}},{t + .1:.2f});')
    ev(t + .15, "swirl")
    add(f'tl.to(".orb3d",{{scale:.15,opacity:0,duration:.3,ease:"power3.in"}},{t + 1.05:.2f});')
    add('tl.fromTo(".rays82",{opacity:0,rotation:0,scale:.5},{opacity:.85,rotation:60,scale:1,duration:1.6,ease:"power2.out",'
        'immediateRender:false},15.37);tl.to(".rays82",{opacity:0,duration:.4},16.75);')
    pop(".scard", t + 1.3, "y:300,opacity:0,scale:.85,rotationX:40", .5)
    shine(".scard", 15.5)
    counter(".cnt-sc", 0, 82, 15.37, 1.0, "int", "expo.out")
    add('tl.fromTo(".rg",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:.18,duration:1.0,ease:"expo.out"},15.37);')
    add('tl.to("#punch",{scale:1.08,duration:.22,ease:"power2.out",yoyo:true,repeat:1},15.4);')
    ring("rg82", 15.45, 4)
    confetti_tl("cf82", 15.45)
    pop(".sl2", 16.0, "opacity:0,y:20", .3)
    pop(".sins", 16.15, "opacity:0,y:30", .4)
    # 7 analyse
    t = S["analyse"][0]
    hl_in("analyse", t + .05)
    pop(".ubub", t + .2, "x:200,opacity:0,scale:.85", .45)
    add(f'tl.fromTo(".ubt",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.6,ease:"none"}},{t + .35:.2f});')
    pop(".onit", t + .7, "y:100,opacity:0,scale:.9", .45)
    shine(".onit", 18.1)
    for i, tt in enumerate((18.0, 18.5, 19.0)):
        pop(f".orow.o{i}", tt, "x:-40,opacity:0", .3)
        add(f'tl.fromTo(".orow.o{i} .tk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.25}},{tt + .15:.2f});')
    pop(".scanph", 18.2, "scale:.5,opacity:0,rotation:8", .4)
    add('tl.fromTo(".scanl",{y:0},{y:300,duration:.6,ease:"none",repeat:1},18.4);')
    out(".ubub, .onit, .scanph", 19.75, "opacity:0,y:-60,scale:.9", .3)
    pop(".tl-a", 19.85, "y:200,opacity:0,scale:.9", .45)
    add('tl.fromTo(".tl-a .tline",{scaleY:0},{scaleY:1,duration:1.1,ease:"power1.inOut"},20.0);')
    add('tl.fromTo(".tl-a .phd",{y:0,opacity:1},{y:640,duration:1.05,ease:"power1.inOut"},20.25);')
    add('tl.fromTo(".tl-a .tr",{opacity:0,x:60},{opacity:1,x:0,duration:.3,stagger:.2,ease:"back.out(2)"},20.0);')
    # 8 twist: inside the reel. The film strip scrolls frame by frame under the giant lens, stops on 0:34, and that
    # frame lifts out and flies back to 0:00
    t = S["twist"][0]
    step = FR_W + FR_GAP
    add(f'tl.to("#dark",{{opacity:1,duration:.4,ease:"power2.out"}},{t - .1:.2f});')
    add(f'tl.to("#dark",{{opacity:0,duration:.35,ease:"power2.in"}},{S["twist"][1] - .1:.2f});')
    pop(".scanlab", t + .25, "opacity:0,y:-20,scale:.9", .35)
    add('tl.to(".scanlab",{opacity:.45,duration:.25,yoyo:true,repeat:5,ease:"sine.inOut"},21.8);')
    out(".scanlab", 23.15, "opacity:0,y:-20", .15)
    hl_in("twist", 23.2)
    add(f'tl.set(".fsr",{{x:{FR_X0}}},0);')
    add(f'tl.fromTo(".fsw",{{scale:.35,opacity:0}},{{scale:1,opacity:1,duration:.7,ease:"expo.out",immediateRender:false}},{t:.2f});')
    add(f'tl.fromTo(".fdim",{{opacity:0}},{{opacity:1,duration:.5,immediateRender:false}},{t + .25:.2f});')
    add(f'tl.fromTo(".lensg",{{scale:.4,opacity:0,rotation:-25}},{{scale:1,opacity:1,rotation:0,duration:.55,ease:"back.out(1.8)",'
        f'immediateRender:false}},{t + .2:.2f});')
    ev(t + .2, "pop")
    add('tl.fromTo(".lglint",{xPercent:-160},{xPercent:260,duration:.6,ease:"power2.inOut",repeat:2,repeatDelay:.45},21.7);')
    add('tl.fromTo(".att",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:1.9,ease:"none",immediateRender:false},21.5);')
    for k in range(1, 8):
        tk = 21.6 + (k - 1) * .235
        add(f'tl.to(".fsr",{{x:{FR_X0 - k * step:.0f},duration:.15,ease:"power2.inOut"}},{tk:.2f});')
        ev(tk + .15, "tick")
    # found it
    add('tl.to(".fr7",{boxShadow:"0 0 0 7px #F2B134, 0 0 80px 18px rgba(242,177,52,.85)",scale:1.06,duration:.25,ease:"back.out(3)"},23.33);')
    add('tl.to(".lring",{borderColor:"#FF5FA2",boxShadow:"0 0 0 6px rgba(255,95,162,.35), 0 0 90px rgba(255,95,162,.9)",duration:.2},23.33);')
    add('tl.fromTo(".lensg",{scale:1},{scale:1.07,duration:.12,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false},23.33);')
    add('tl.fromTo(".rays34",{opacity:0,rotation:0,scale:.6},{opacity:1,rotation:50,scale:1,duration:1.3,ease:"power2.out",immediateRender:false},23.33);')
    pop(".besth", 23.45, "scale:.3,opacity:0,y:30", .4, "back.out(3)")
    ring("rg34", 23.4, 3.6)
    # lift out, rewind underneath, drop into 0:00
    add('tl.to(".lensg, .fdim, .besth",{opacity:0,duration:.22},24.5);')
    add('tl.set(".fr7",{opacity:0},24.6);tl.set(".flycard",{opacity:1},24.6);')
    add('tl.fromTo(".flycard",{scale:.8,y:0,rotation:0},{scale:1.15,y:-170,rotation:-6,duration:.3,ease:"back.out(2)",immediateRender:false},24.6);')
    ev(24.6, "pop")
    add(f'tl.to(".fsr",{{x:{FR_X0:.0f},duration:.5,ease:"power3.inOut"}},24.78);')
    add('tl.to(".rays34",{opacity:0,duration:.3},24.6);')
    add('tl.fromTo("#whip",{opacity:.4,x:-300},{opacity:0,x:300,duration:.3,ease:"power2.out",immediateRender:false},24.8);')
    add('tl.to(".flycard",{scale:.8,y:0,rotation:0,duration:.2,ease:"power3.in"},25.1);')
    add('tl.set(".fr0",{opacity:0},25.3);')
    add('(()=>{const o={v:0};tl.to(o,{v:1,duration:.01,onUpdate:()=>{document.querySelector(".flycard .frt").textContent='
        'o.v>.5?"0:00":"0:34";}},25.3);})();')
    add('tl.to(".flycard .fc",{boxShadow:"0 0 0 7px #FF5FA2, 0 0 70px 14px rgba(255,95,162,.8)",duration:.2},25.3);')
    pop(".newh", 25.42, "scale:.3,opacity:0,y:-30", .4, "back.out(3)")
    ring("rg34", 25.3, 3.0)
    confetti_tl("cf34", 25.3)
    # 9 reasons
    t = S["reasons"][0]
    hl_in("reasons", t + .05)
    pop(".gcard", t + .15, "x:-200,opacity:0,rotation:-14,scale:.85", .45)
    pop(".rcard", t + .35, "x:200,opacity:0,rotation:14,scale:.85", .45)
    add('tl.to(".d1",{rotation:360,duration:.5,ease:"power2.out",repeat:2},26.5);tl.to(".d2",{rotation:-360,duration:.5,'
        'ease:"power2.out",repeat:2},26.6);')
    add('tl.to(".gq2 span",{y:-16,duration:.3,stagger:.1,yoyo:true,repeat:3,ease:"sine.inOut"},26.6);')
    shine(".rcard", 27.0)
    gap = 10
    before, x = [], 0
    for _, w, _ in SEGS:
        before.append(x)
        x += w + gap
    after, x = [0] * len(SEGS), 0
    for k in SEG_AFTER:
        after[k] = x
        x += SEGS[k][1] + gap
    for k in range(len(SEGS)):
        add(f'tl.set(".sg{k}",{{x:{before[k]}}},0);')
    add(f'tl.fromTo(".seg",{{opacity:0,scaleY:.2,y:-30}},{{opacity:1,scaleY:1,y:0,duration:.3,stagger:.06,ease:"back.out(2.4)"}},{t + .2:.2f});')
    ev(t + .2, "pop")
    add('tl.to(".sg3",{y:-46,scale:1.08,duration:.18,ease:"power2.out"},27.0);')
    for k in range(len(SEGS)):
        add(f'tl.to(".sg{k}",{{x:{after[k]},duration:.5,ease:"power3.inOut"}},27.15);')
    ev(27.15, "swish")
    add('tl.to(".sg3",{y:0,scale:1,duration:.22,ease:"back.out(3)"},27.62);')
    ev(27.65, "pop")
    for i, tt in enumerate((26.9, 27.35, 27.8)):
        pop(f".rr{i}", tt, "x:40,opacity:0", .3)
        add(f'tl.fromTo(".rr{i} .tk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.25}},{tt + .1:.2f});')
    add('tl.fromTo(".strike",{scaleX:0},{scaleX:1,duration:.3,ease:"power3.out"},28.4);')
    add('tl.to(".gcard",{opacity:.45,filter:"grayscale(1)",rotation:-8,y:40,duration:.3},28.5);')
    add('tl.to(".rcard",{scale:1.05,duration:.2,yoyo:true,repeat:1},28.5);')
    # 10 cta: one keyword, typed big into the comment box, sent; then the brand end card
    t = S["cta"][0]
    pop(".cmt", t + .05, "y:-120,opacity:0,rotation:-20,scale:.7", .45, "bounce.out")
    pop(".cbox", 29.75, "y:160,opacity:0,scale:.85", .5, "back.out(1.8)")
    shine(".cbox", 30.3)
    word = "CREEDOM"
    add(f'(()=>{{const o={{v:0}};tl.to(o,{{v:{len(word)},duration:{len(word) * .1:.2f},ease:"none",onUpdate:()=>{{'
        f'document.querySelector(".typed").textContent="{word}".slice(0,Math.floor(o.v+.001));}}}},29.95);}})();')
    add(f'tl.to(".caret",{{opacity:0,duration:.01,yoyo:true,repeat:{int((DUR - 29.9) / .5) * 2 - 1},repeatDelay:.49}},29.9);')
    ring("rgkw", 30.7, 3)
    confetti_tl("cfkw", 30.75)
    add('tl.to("#punch",{scale:1.06,duration:.2,ease:"power2.out",yoyo:true,repeat:1},30.7);')
    add('tl.to(".send",{scale:1.18,duration:.15,yoyo:true,repeat:3},31.0);')
    add('tl.fromTo(".plane",{x:0,y:0,opacity:0,rotation:0,scale:.6},{x:200,y:-460,opacity:1,rotation:-25,scale:1.1,duration:.8,'
        'ease:"power2.in"},31.05);tl.to(".plane",{opacity:0,duration:.2},31.86);')
    pop(".dm", 31.25, "opacity:0,y:20", .3)
    out(".cmt, .cbox", 32.0, "opacity:0,y:-40,scale:.9", .3)
    pop(".endlock", 32.15, "scale:.4,opacity:0,y:60", .5, "back.out(2.4)")
    pop(".endsub", 32.45, "opacity:0,y:30", .4)
    # background and always-on pieces
    add(f'tl.fromTo(".pfill",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none"}},0);')
    add(f'tl.fromTo("#gridl",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"0px -1080px",duration:{DUR},ease:"none"}},0);')
    for i, (dx, dy, d) in enumerate([(220, 160, 7), (-200, 220, 9), (160, -240, 8)]):
        add(f'tl.fromTo(".blob{i}",{{x:0,y:0}},{{x:{dx},y:{dy},duration:{d},ease:"sine.inOut",yoyo:true,repeat:{int(DUR / d)}}},0);')
    add(f'document.querySelectorAll(".tw").forEach((e,i)=>tl.fromTo(e,{{scale:.3,opacity:.15}},{{scale:1,opacity:.9,'
        f'duration:.7,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .7) - 2}}},i*.23));')
    for js in LATER:
        add(js)
    # ---- extra motion so no second sits still
    # live reactions rising up the edges
    for i, t in enumerate(REACT_T):
        add(f'tl.fromTo(".rx{i}",{{y:0,x:0,scale:.3,rotation:-12}},{{y:-640,x:{REACT_SW[i]:.0f},scale:1,rotation:12,duration:2.4,'
            f'ease:"power1.out",immediateRender:false}},{t:.2f});')
        add(f'tl.to(".rx{i}",{{opacity:.92,duration:.22}},{t:.2f});tl.to(".rx{i}",{{opacity:0,duration:.5}},{t + 1.85:.2f});')
        if i % 2 == 0:
            ev(t, "bubble")
    # data streaming from Instagram into Creedom, sparkles orbiting the Creedom icon
    t = S["read"][0]
    add(f'tl.fromTo(".ddot",{{x:0,opacity:0,scale:.4}},{{x:560,opacity:1,scale:1,duration:.9,ease:"power1.inOut",stagger:{{each:.15,'
        f'repeat:3}},immediateRender:false}},{t + .5:.2f});')
    add(f'tl.to(".ddot",{{opacity:0,duration:.2}},{S["read"][1] - .3:.2f});')
    for k in range(4):
        ev(t + .55 + k * .9, "data")
    add(f'tl.fromTo(".orbit",{{rotation:0,opacity:0}},{{rotation:540,opacity:1,duration:3.4,ease:"none",immediateRender:false}},{t + .3:.2f});')
    add(f'tl.to(".orbit",{{opacity:0,duration:.2}},{S["read"][1] - .3:.2f});')
    # the twist: a scanner sweeps the timeline while a heartbeat builds
    add('tl.set(".laser",{opacity:0},0);')
    add('tl.fromTo(".laser",{y:0,opacity:1},{y:600,opacity:1,duration:.7,ease:"sine.inOut",yoyo:true,repeat:1,immediateRender:false},21.6);')
    add('tl.to(".laser",{opacity:0,duration:.2},23.0);')
    ev(21.6, "scan", 1.4)
    for hb in (21.85, 22.4, 22.95):
        add(f'tl.to("#punch",{{scale:1.018,duration:.09,ease:"power2.out",yoyo:true,repeat:1}},{hb:.2f});')
        ev(hb, "heart")
    # end card: a shimmer runs across the wordmark and sparkles twinkle round it
    add('tl.fromTo(".eshine i",{xPercent:-120},{xPercent:420,duration:.8,ease:"power2.inOut",repeat:1,repeatDelay:.15},32.45);')
    ev(32.5, "glint")
    add('tl.fromTo(".esp",{scale:0,opacity:0,rotation:-90},{scale:1,opacity:1,rotation:0,duration:.4,stagger:.07,ease:"back.out(3)"},32.3);')
    add('tl.to(".esp",{scale:.5,opacity:.4,duration:.35,stagger:.05,yoyo:true,repeat:3,ease:"sine.inOut"},32.75);')
    # headline accents breathe once they have landed
    add(f'tl.fromTo(".hl .acc",{{y:0}},{{y:-8,duration:.9,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .9) - 2},immediateRender:false}},.9);')
    caption_tl()
    bird.perform(add, DUR)
    return "\n".join(T)


def kin_html():
    """The backdrop layer, behind every scene: giant outline words and the fly-throughs (a tunnel of reels, a field of
    question marks, a storm of stats), so they always pass behind the content."""
    reels = ["post1.jpg", "post3.jpg", "post4.jpg", "post5.jpg", "post6.jpg", "cover_adobe.jpg", "post2.jpg", "cover_yt.jpg"] * 2
    stats = ["366K", "4.3K", "12%", "0.8s", "↑", "↓", "#", "%", "2.1K", "∞", "38%", "?", "+214", "−9%"]
    return ("".join(f'<div class="kin kin{i}">{w}</div>' for i, w in enumerate(KIN_WORDS)) +
            depth("dft", [mini_reel(x) for x in reels[:16]], 21, 0.0, 1.7, .85, spread=(950, 950), vp=(540, 1080), zmax=3.4) +
            depth("dfq", ['<b class="qm">?</b>'] * 14, 22, S["why"][0] + .05, S["why"][1] + .1, 1.4, zmax=3.2) +
            depth("dfn", [f'<b class="nm">{x}</b>' for x in stats], 23, S["nums"][0] + .05, S["nums"][1] + .1, 1.2, zmax=2.4))


def speed_html():
    import math
    lines = "".join(f'<line x1="{math.cos(a) * 260:.0f}" y1="{math.sin(a) * 260:.0f}" x2="{math.cos(a) * 1300:.0f}" '
                    f'y2="{math.sin(a) * 1300:.0f}" stroke="#E235DD" stroke-width="{3 + (i % 3) * 2}" opacity=".5"/>'
                    for i, a in enumerate(k / 40 * math.tau for k in range(40)))
    return (f'<svg id="speed" viewBox="-1300 -1300 2600 2600" width="2600" height="2600" data-layout-ignore>'
            f'<g>{lines}</g></svg>')


def background():
    r = random.Random(6)
    blobs = "".join(f'<div class="blob blob{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></div>'
                    for i, (x, y, s, c) in enumerate([(-260, -160, 900, "#F9C6D3"), (520, 900, 1000, "#F8D9C2"),
                                                      (420, -200, 760, "#DAD6F6")]))
    twinkles = "".join(f'<div class="tw" style="left:{r.uniform(40, 1000):.0f}px;top:{r.uniform(150, 1750):.0f}px">'
                       f'{star(r.choice([18, 24, 30]), r.choice([PINK, "#F2B134", "#B39DDB"]))}</div>' for _ in range(14))
    pts = "".join(f'<i class="pt" style="left:{r.uniform(20, 1060):.0f}px;top:{r.uniform(1000, 1950):.0f}px;'
                  f'width:{r.choice([6, 8, 10, 14])}px;height:{r.choice([6, 8, 10, 14])}px"></i>' for _ in range(26))
    return (f'<div id="paper"></div><div id="blobs">{blobs}</div><div id="gridl"></div><div id="pts" data-layout-ignore>{pts}</div>'
            f'<div id="twk" data-layout-ignore>{twinkles}</div><div id="dark"></div>')


CSS = """
@font-face { font-family: "Google Sans"; font-weight: 400 700; src: url("assets/fonts/googlesans.ttf"); }
:root { --cg: linear-gradient(90deg, #E235DD, #E34CB7 45%, #E68B70); --cgd: linear-gradient(90deg, #C82BC4, #D23C93 50%, #CF6448); --pink: #E2557D; --pinkt: #C93A6D; --ink: #0B0B0B; --paper: #F6F6F4; }
* { margin: 0; padding: 0; box-sizing: border-box; }
i, em { font-style: normal; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--paper); }
body { font-family: "Google Sans", sans-serif; color: var(--ink); }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--paper); }
.clip { position: absolute; inset: 0; }
#cam { position: absolute; inset: 0; transform-origin: 50% 45%; z-index: 2; }
#punch { position: absolute; inset: 0; transform-origin: 50% 45%; perspective: 1400px; }
.mono { font: 600 24px "Google Sans"; letter-spacing: 5px; color: #6b6b66; }
/* background: the reference covers' soft pastel glow on a fine grid */
#paper { position: absolute; inset: 0; background: var(--paper); }
#blobs { position: absolute; inset: 0; filter: blur(90px); opacity: .85; }
.blob { position: absolute; border-radius: 50%; }
#gridl { position: absolute; inset: 0; background-image: linear-gradient(rgba(11,11,11,.055) 1.5px, transparent 1.5px),
  linear-gradient(90deg, rgba(11,11,11,.055) 1.5px, transparent 1.5px); background-size: 54px 54px; }
.tw { position: absolute; }
#dark { position: absolute; inset: 0; opacity: 0;
  background: radial-gradient(90% 60% at 50% 45%, #3a1d26 0%, #1b0f14 55%, #0d0709 100%); }
.ghost { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font: 600 520px/1 "Google Sans";
  color: rgba(11,11,11,.045); letter-spacing: -20px; white-space: nowrap; }
.ghost.gw { color: rgba(255,255,255,.05); font-size: 400px; }
#shake { position: absolute; inset: 0; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 42; }
#speed { position: absolute; left: -760px; top: -340px; opacity: 0; z-index: 39; }
#kin { z-index: 1; }
.kin { position: absolute; left: -200px; width: 1480px; top: 760px; text-align: center; font: 700 360px/1 "Google Sans"; letter-spacing: -10px;
  color: transparent; -webkit-text-stroke: 5px rgba(226,53,160,.28); white-space: nowrap; opacity: 0; }
.pt { position: absolute; border-radius: 50%; background: radial-gradient(circle, #ffffff, rgba(226,53,160,.5)); opacity: 0; }
#whip { position: absolute; inset: 0; opacity: 0; z-index: 41; background: repeating-linear-gradient(0deg,
  rgba(255,255,255,0) 0 22px, rgba(255,255,255,.55) 22px 26px, rgba(255,255,255,0) 26px 70px); }
/* progress pill */
.pill { position: absolute; right: 56px; top: 56px; width: 300px; height: 56px; border-radius: 28px; background: rgba(255,255,255,.85);
  box-shadow: 0 6px 24px rgba(0,0,0,.08); display: flex; align-items: center; gap: 14px; padding: 0 18px; }
.pill img { width: 36px; height: 38px; }
.ptrack { flex: 1; height: 10px; border-radius: 5px; background: #ebe8e4; overflow: hidden; }
.pfill { width: 100%; height: 100%; background: var(--cg); transform-origin: 0 50%; }
/* headline */
.hl { position: absolute; left: 0; width: 1080px; text-align: center; z-index: 6; }
.l1 { font: 700 84px/1.05 "Google Sans"; letter-spacing: -3px; }
.l2 { font: 600 112px/1.05 "Google Sans"; letter-spacing: -3px; color: var(--pinkt); }
.hw, .acc { display: inline-block; }
.acc { background: var(--cgd); -webkit-background-clip: text; background-clip: text; color: transparent; padding: 0 10px; }
.dark .acc { background: var(--cg); -webkit-background-clip: text; background-clip: text; }
.acc { position: relative; }
.sw { position: absolute; left: 4%; bottom: -14px; width: 92%; height: 34px; overflow: visible; }
.dark .l1, .dark .hl { color: #fff; }
.dark .l2 { color: #FF8FAE; }
/* cards */
.card { background: #fff; border-radius: 34px; box-shadow: 0 24px 60px rgba(11,11,11,.12), 0 2px 0 rgba(11,11,11,.04);
  overflow: hidden; }
.shine { position: absolute; top: -20%; left: 0; width: 38%; height: 140%; transform: rotate(18deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.75), rgba(255,255,255,0)); pointer-events: none; }
.chip { position: absolute; border-radius: 40px; font: 700 34px "Google Sans"; padding: 14px 28px; white-space: nowrap; }
.pinkchip { background: var(--pink); color: #fff; }
.redchip { background: #fde8e8; color: #c43c3c; }
.pring { position: absolute; width: 220px; height: 220px; border-radius: 50%; border: 8px solid #E235DD; opacity: 0; }
.conf { position: absolute; left: 540px; top: 900px; }
.conf i { position: absolute; left: 0; top: 0; opacity: 0; }
.sticker { position: absolute; font-size: 96px; }
/* hook */
.ticker { position: absolute; left: -40px; top: 420px; width: 1160px; height: 64px; background: var(--ink); color: #fff;
  overflow: hidden; transform: rotate(-2deg); font: 700 28px "Google Sans"; letter-spacing: 3px; white-space: nowrap; }
.tk-in { position: absolute; left: 0; top: 14px; }
.cover { position: absolute; left: 80px; top: 540px; width: 440px; height: 501px; border-radius: 36px; }
.cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.vbar { position: absolute; left: 110px; top: 1062px; height: 76px; display: flex; align-items: center; gap: 12px; padding: 0 28px;
  border-radius: 38px; background: var(--ink); color: #fff; font: 700 44px "Google Sans"; }
.plab { font: 600 24px "Google Sans"; opacity: .8; }
.chart { position: absolute; left: 560px; top: 580px; width: 440px; height: 420px; padding: 34px 30px; }
.chart .mono { font-size: 20px; letter-spacing: 3px; white-space: nowrap; }
.chart svg { margin-top: 26px; }
.c85 { left: 60px; top: 330px; font-size: 32px; }
.burst { position: absolute; left: 300px; top: 820px; }
.bst { position: absolute; left: 0; top: 0; }
.rg85 { left: 680px; top: 820px; }
.st-eyes { left: 470px; top: 500px; }
.st-fire { left: 900px; top: 1000px; }
.qrain { position: absolute; inset: 0; }
.qr { position: absolute; font: 700 100px "Google Sans"; color: var(--pinkt); opacity: 0; }
/* next */
.mini { position: absolute; left: 60px; top: 560px; width: 220px; padding: 14px; transform: rotate(-4deg); }
.mini img { width: 100%; border-radius: 18px; display: block; }
.mini .mono { margin-top: 10px; font-size: 20px; letter-spacing: 2px; color: var(--pinkt); }
.cv-b { left: 330px; top: 520px; width: 440px; height: 495px; }
.cv-b-v { left: 360px; top: 1040px; }
.lowk { left: 60px; top: 900px; }
.arrowdn { position: absolute; left: 140px; top: 990px; font: 700 120px "Google Sans"; color: #c43c3c; }
.grid6 { position: absolute; left: 90px; top: 520px; width: 900px; display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
.tile { height: 170px; padding: 26px 30px; position: relative; }
.tile .mono { font-size: 22px; }
.tv { font: 700 60px "Google Sans"; margin-top: 4px; }
.tb { height: 10px; border-radius: 5px; background: #eee; margin-top: 10px; }
/* read */
.link { position: absolute; left: 0; width: 1080px; top: 170px; height: 170px; }
.appic { position: absolute; top: 20px; width: 150px; height: 150px; border-radius: 40px; display: flex; align-items: center;
  justify-content: center; box-shadow: 0 20px 50px rgba(11,11,11,.15); }
.appic.ig { left: 170px; background: linear-gradient(135deg, #FEDA75, #FA7E1E 30%, #D62976 60%, #962FBF 85%, #4F5BD5); }
.appic.cr { left: 760px; background: #fff; }
.appic.cr img { width: 112px; height: 119px; }
.dash { position: absolute; left: 330px; top: 85px; transform-origin: 0 50%; }
.lpill { position: absolute; left: 395px; top: 70px; background: var(--ink); color: #fff; font: 600 30px "Google Sans"; padding: 10px 26px;
  border-radius: 30px; white-space: nowrap; }
.crlogo { position: absolute; left: 0; width: 1080px; top: 345px; text-align: center; }
.crlogo img { width: 230px; height: auto; }
.reading { position: absolute; left: 0; width: 1080px; top: 400px; text-align: center; font-size: 30px; letter-spacing: 8px; color: #555; }
.give { position: absolute; left: 0; width: 1080px; top: 445px; text-align: center; font: 700 96px "Google Sans"; letter-spacing: -2px; }
.give i { color: var(--pinkt); }
.rbar { position: absolute; left: 120px; top: 600px; width: 840px; height: 14px; border-radius: 7px; background: #ebe8e4; overflow: hidden; }
.rfill { width: 100%; height: 100%; background: var(--cg); transform-origin: 0 50%; }
.ticks { position: absolute; left: 100px; top: 680px; width: 880px; padding: 34px 40px; }
.trow { display: flex; align-items: center; gap: 24px; font: 500 40px "Google Sans"; color: #444; padding: 20px 0; }
.stopw { left: 720px; top: 990px; background: var(--ink); color: #fff; }
.rg20 { left: 740px; top: 920px; }
/* score */
.th { position: absolute; left: -115px; top: -160px; width: 230px; height: 320px; border-radius: 24px; overflow: hidden; box-shadow: 0 18px 40px rgba(11,11,11,.18); }
.th img { width: 100%; height: 100%; object-fit: cover; }
.scard { position: absolute; left: 90px; top: 450px; width: 900px; height: 640px; border-radius: 44px; background: var(--ink); color: #fff;
  padding: 50px 56px; box-shadow: 0 40px 80px rgba(11,11,11,.3); overflow: hidden; }
.scard .mono { color: #b9b9b2; }
.snum { font: 600 230px/1 "Google Sans"; margin-top: 10px; }
.snum small { font-size: 74px; color: #9a9a92; margin-left: 10px; }
.ring { position: absolute; right: 56px; top: 90px; }
.sl2 { color: #FF8FAE !important; margin-top: 34px; }
.sins { font: 600 50px/1.2 "Google Sans"; margin-top: 14px; }
.sins i { color: #ffb3c6; }
.scard .shine { background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.18), rgba(255,255,255,0)); }
.rg82 { left: 230px; top: 640px; }
.cf82 { left: 300px; top: 760px; }
/* analyse */
.ubub { position: absolute; right: 70px; top: 470px; width: 760px; background: var(--ink); color: #fff; border-radius: 40px 40px 10px 40px;
  padding: 34px 40px; font: 600 42px/1.3 "Google Sans"; }
.ubt { display: block; }
.onit { position: absolute; left: 70px; top: 760px; width: 760px; padding: 34px 40px; }
.oh { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.oh img { width: 44px; height: 46px; }
.orow { display: flex; align-items: center; gap: 20px; font: 500 34px "Google Sans"; color: #444; padding: 12px 0; }
.scanph { position: absolute; left: 850px; top: 780px; width: 180px; height: 290px; border-radius: 22px; overflow: hidden;
  box-shadow: 0 18px 40px rgba(11,11,11,.2); }
.scanph img { width: 100%; height: 100%; object-fit: cover; }
.scanl { position: absolute; left: 0; right: 0; top: -6px; height: 6px; background: var(--pink); box-shadow: 0 0 20px var(--pink); }
.tlc { position: absolute; left: 190px; top: 440px; width: 840px; height: 880px; padding: 34px 40px; overflow: visible; }
.tlh { display: flex; justify-content: space-between; align-items: center; }
.sc42 { font: 700 32px "Google Sans"; color: var(--ink); }
.sc42 small { color: #888; font-size: 24px; }
.tline { position: absolute; left: 62px; top: 140px; width: 4px; height: 640px; background: #e4e1dc; transform-origin: 50% 0; }
.phd { position: absolute; left: 52px; top: 140px; width: 24px; height: 24px; border-radius: 50%; background: var(--pink);
  box-shadow: 0 0 0 8px rgba(226,85,125,.25); opacity: 0; z-index: 3; }
.tr { position: absolute; left: 30px; width: 780px; height: 120px; border-radius: 26px; display: flex; align-items: center; gap: 22px;
  padding: 0 30px; background: #fff; }
.dot { width: 26px; height: 26px; border-radius: 50%; flex: none; }
.tr b { font: 700 34px "Google Sans"; letter-spacing: -1px; white-space: nowrap; }
.tt { font: 500 24px "Google Sans"; color: #888; white-space: nowrap; }
.ts { margin-left: auto; font: 700 36px "Google Sans"; color: #555; }
.spot { position: absolute; left: 240px; top: -300px; width: 600px; height: 1800px; transform-origin: 50% 0;
  background: linear-gradient(180deg, rgba(255,214,230,.22), rgba(255,214,230,0) 80%); clip-path: polygon(45% 0, 55% 0, 100% 100%, 0 100%); }
/* reasons */
.gcard { position: absolute; left: 70px; top: 640px; width: 440px; height: 520px; padding: 40px; transform: rotate(-3deg); }
.dice { font-size: 110px; margin-top: 50px; text-align: center; }
.dice span { display: inline-block; }
.gq2 { font: 700 90px "Google Sans"; color: #bbb; text-align: center; margin-top: 30px; }
.gq2 span { display: inline-block; }
.strike { position: absolute; left: 30px; top: 250px; width: 380px; height: 14px; border-radius: 7px; background: var(--pink);
  transform: rotate(-14deg); transform-origin: 0 50%; }
.rcard { position: absolute; left: 540px; top: 600px; width: 480px; height: 600px; padding: 40px 34px; transform: rotate(2deg);
  box-shadow: 0 0 0 4px var(--pink), 0 30px 70px rgba(226,85,125,.3); }
.pk { color: var(--pinkt) !important; font-size: 21px; letter-spacing: 3px; }
.rr { display: flex; align-items: flex-start; gap: 16px; font: 700 36px/1.25 "Google Sans"; margin-top: 34px; }
.rr svg { flex: none; margin-top: 2px; }
/* cta */
.cmt { position: absolute; left: 270px; top: 300px; display: flex; align-items: center; gap: 18px; background: var(--ink); color: #fff;
  font: 700 70px "Google Sans"; letter-spacing: -1px; padding: 22px 46px; border-radius: 26px; transform: rotate(-3deg); }
.kw { position: absolute; left: 90px; top: 450px; width: 900px; text-align: center; background: var(--cgd); color: #fff;
  font: 700 160px "Google Sans"; letter-spacing: -3px; border-radius: 40px; padding: 18px 0; box-shadow: 0 30px 70px rgba(226,85,125,.45); }
.kc { position: absolute; background: #fff; border-radius: 30px; padding: 10px 22px; font: 700 26px "Google Sans";
  box-shadow: 0 10px 26px rgba(11,11,11,.1); color: #444; }
.endlock { position: absolute; left: 0; width: 1080px; top: 340px; display: flex; justify-content: center; align-items: center; }
.endlock img { width: 760px; height: auto; }
.endsub b { color: #fff; background: var(--cgd); font-family: "Google Sans"; font-weight: 700; padding: 4px 18px; border-radius: 16px; }
/* live reactions, data dots, orbit, scanner, end shimmer */
.rx { position: absolute; top: 1290px; opacity: 0; filter: drop-shadow(0 6px 12px rgba(226,53,160,.25)); }
.ddot { position: absolute; left: 232px; top: 82px; width: 26px; height: 26px; z-index: 3; border-radius: 50%; background: var(--pink);
  box-shadow: 0 0 14px rgba(226,53,160,.8); opacity: 0; }
.orbit { position: absolute; left: 835px; top: 95px; width: 0; height: 0; z-index: 3; }
.ob { position: absolute; }
.ob0 { left: 100px; top: -20px; } .ob1 { left: -20px; top: 100px; } .ob2 { left: -140px; top: -20px; } .ob3 { left: -20px; top: -140px; }
.laser { position: absolute; left: 200px; top: 560px; width: 820px; height: 6px; border-radius: 3px; background: #FF8FAE;
  box-shadow: 0 0 24px 6px rgba(255,92,150,.6); opacity: 0; z-index: 4; }
.endlock { overflow: visible; }
.eshine { position: absolute; left: 160px; top: 0; width: 760px; height: 142px; overflow: hidden;
  -webkit-mask: url("assets/img/creedom_logo.png") center / 100% 100% no-repeat; mask: url("assets/img/creedom_logo.png") center / 100% 100% no-repeat; }
.eshine i { position: absolute; left: 0; top: -20%; width: 12%; height: 140%; transform: skewX(-18deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0)); mix-blend-mode: screen; }
.esp { position: absolute; opacity: 0; }
/* depth fields */
.df { position: absolute; width: 0; height: 0; }
.dfi { position: absolute; left: 0; top: 0; opacity: 0; }
.mreel { width: 150px; height: 240px; border-radius: 22px; overflow: hidden; background: #fff; box-shadow: 0 18px 40px rgba(11,11,11,.25); }
.mreel img { width: 100%; height: 100%; object-fit: cover; display: block; }
.qm { display: block; font: 700 150px "Google Sans"; background: var(--cg); -webkit-background-clip: text; background-clip: text; color: transparent; }
.nm { display: block; font: 700 80px "Google Sans"; color: rgba(11,11,11,.62); white-space: nowrap; letter-spacing: -2px; }
.mfr { width: 70px; height: 110px; border-radius: 12px; background: linear-gradient(160deg, var(--c), #1a1420); display: flex;
  align-items: center; justify-content: center; font-size: 38px; box-shadow: 0 8px 20px rgba(0,0,0,.25); }
/* read: portal, radar, pulses */
.portal { position: absolute; left: 540px; top: 960px; width: 0; height: 0; z-index: 39; }
.prg { position: absolute; left: -300px; top: -300px; width: 600px; height: 600px; border-radius: 50%; border: 26px solid #E235DD; opacity: 0; }
.radar { position: absolute; left: 685px; top: -55px; width: 300px; height: 300px; border-radius: 50%; opacity: 0;
  background: conic-gradient(from 0deg, rgba(226,53,160,0) 0deg, rgba(226,53,160,.45) 70deg, rgba(226,53,160,0) 71deg); }
.rpulse { position: absolute; left: 760px; top: 20px; width: 150px; height: 150px; border-radius: 40px; border: 5px solid #E235DD; opacity: 0; }
/* score: orbit and rays */
.orb3d { position: absolute; left: 0; top: 420px; width: 1080px; height: 700px; perspective: 1100px; }
.orbr { position: absolute; left: 540px; top: 350px; width: 0; height: 0; transform-style: preserve-3d; }
.rays { position: absolute; border-radius: 50%; opacity: 0;
  background: repeating-conic-gradient(from 0deg, rgba(255,205,110,.55) 0deg 7deg, rgba(255,205,110,0) 7deg 20deg);
  -webkit-mask: radial-gradient(circle, #000 30%, transparent 72%); mask: radial-gradient(circle, #000 30%, transparent 72%); }
.rays82 { left: -460px; top: -230px; width: 2000px; height: 2000px; }
.rays34 { left: -160px; top: 200px; width: 1400px; height: 1400px; }
/* twist: the film strip, the lens, the flying frame */
.fsw { position: absolute; inset: 0; perspective: 1100px; perspective-origin: 540px 900px; transform-origin: 540px 900px; }
.fs3d { position: absolute; inset: 0; transform-origin: 540px 900px; transform: rotateY(-18deg) rotateX(6deg); transform-style: preserve-3d; }
.fsr { position: absolute; left: 0; top: 650px; height: 540px; border-radius: 18px; background: #120d16; border-top: 4px solid #2a2030;
  border-bottom: 4px solid #2a2030; box-shadow: 0 40px 100px rgba(0,0,0,.6); }
.fsr::before { content: ""; position: absolute; left: 0; right: 0; top: 14px; height: 20px;
  background: repeating-linear-gradient(90deg, #3a2e40 0 24px, transparent 24px 46px); }
.frw { position: absolute; top: 50px; width: 230px; height: 400px; }
.fr, .fc { position: relative; width: 230px; height: 400px; border-radius: 20px; overflow: hidden; color: #fff;
  background: linear-gradient(165deg, var(--c) 0%, #2a1c30 58%, #17101b 100%); box-shadow: 0 0 0 2px rgba(255,255,255,.08); }
.frt { position: absolute; left: 16px; top: 14px; font: 700 30px "Google Sans"; background: rgba(0,0,0,.4); padding: 2px 12px; border-radius: 10px; }
.fri { position: absolute; left: 0; right: 0; top: 104px; text-align: center; font-size: 120px; line-height: 1; }
.frl { position: absolute; left: 6px; right: 6px; bottom: 66px; text-align: center; font: 700 28px/1.1 "Google Sans"; }
.frs { position: absolute; left: 0; right: 0; bottom: 30px; display: flex; justify-content: center; gap: 8px; }
.frs i { width: 16px; height: 16px; border-radius: 50%; background: rgba(255,255,255,.22); }
.frs i.on { background: #fff; }
.attw { position: absolute; left: 0; top: 455px; }
.fdim { position: absolute; inset: 0; opacity: 0; background: radial-gradient(circle at 540px 900px, rgba(10,5,12,0) 0,
  rgba(10,5,12,0) 215px, rgba(10,5,12,.55) 330px, rgba(10,5,12,.82) 760px); }
.lensg { position: absolute; inset: 0; transform-origin: 540px 900px; opacity: 0; }
.lens { position: absolute; inset: 0; clip-path: circle(205px at 540px 900px); background: #150e19; }
.lensin { position: absolute; inset: 0; transform: scale(1.3); transform-origin: 540px 900px; }
.lglint { position: absolute; left: 400px; top: 680px; width: 110px; height: 440px; transform: rotate(25deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.25), rgba(255,255,255,0)); }
.lring { position: absolute; left: 325px; top: 685px; width: 430px; height: 430px; border-radius: 50%; border: 18px solid #F2B134;
  box-shadow: 0 0 0 6px rgba(242,177,52,.25), 0 0 60px rgba(242,177,52,.5), inset 0 0 30px rgba(0,0,0,.45); }
.lhandle { position: absolute; left: 368px; top: 1052px; width: 44px; height: 230px; border-radius: 22px;
  background: linear-gradient(90deg, #7a4a1f, #b3773a, #7a4a1f); transform-origin: 22px 0; transform: rotate(45deg); }
.flycard { position: absolute; left: 396px; top: 650px; width: 288px; height: 500px; opacity: 0; z-index: 5; }
.flycard .fc { transform: scale(1.252); transform-origin: 0 0; }
.besth { left: 372px; top: 600px; z-index: 6; font-size: 34px; padding: 10px 26px; background: #F2B134; color: #1a1208; opacity: 0; }
.newh { left: 372px; top: 1185px; z-index: 6; font-size: 34px; padding: 10px 26px; background: #3E8E62; color: #fff; opacity: 0; }
.rg34 { left: 430px; top: 790px; }
.cf34 { left: 540px; top: 900px; }
.scanlab { position: absolute; left: 0; width: 1080px; top: 230px; text-align: center; font: 700 40px "Google Sans"; letter-spacing: 6px;
  color: #FF8FAE; opacity: 0; }
/* reasons: segment bar */
.segbar { position: absolute; left: 100px; top: 1236px; width: 880px; height: 76px; }
.seg { position: absolute; left: 0; top: 0; height: 76px; border-radius: 18px; color: #fff; font: 700 28px "Google Sans"; display: flex;
  align-items: center; justify-content: center; white-space: nowrap; box-shadow: 0 10px 24px rgba(11,11,11,.15); }
/* cta */
.cbox { position: absolute; left: 70px; top: 440px; width: 940px; height: 380px; padding: 40px 44px; }
.cin { margin-top: 24px; width: 700px; height: 150px; border-radius: 26px; border: 5px solid var(--pink); display: flex; align-items: center;
  padding: 0 34px; font: 700 100px "Google Sans"; letter-spacing: 4px; }
.caret { width: 6px; height: 90px; background: var(--ink); margin-left: 8px; }
.send { position: absolute; right: 44px; top: 116px; width: 130px; height: 150px; border-radius: 26px; background: var(--ink);
  display: flex; align-items: center; justify-content: center; }
.dm { margin-top: 26px; font: 700 34px "Google Sans"; color: var(--pinkt); }
.plane { position: absolute; left: 870px; top: 580px; opacity: 0; }
.rgkw { left: 330px; top: 520px; }
.cfkw { left: 540px; top: 640px; }
.endsub { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font: 700 56px "Google Sans"; color: #333; }
.endsub b { color: #fff; background: var(--cgd); padding: 4px 22px; border-radius: 18px; }
/* captions */
#caps { z-index: 30; }
.cap { position: absolute; left: 0; width: 1080px; top: 1400px; text-align: center; opacity: 0; white-space: nowrap; }
.cw { display: inline-block; font: 700 64px "Google Sans"; letter-spacing: -1.5px; padding: 2px 14px; border-radius: 16px; opacity: 0; }
#wipe { position: absolute; left: -400px; top: -100px; width: 1880px; height: 1880px; border-radius: 50%; background: var(--pink); z-index: 40; }
"""


def main():
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom reel analyser 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}{bird.CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="60" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-allow-overflow>{background()}</div>
      <div id="kin" class="clip" data-start="0" data-duration="{DUR}" data-track-index="9" data-layout-ignore>{kin_html()}</div>
      <div id="cam" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-allow-overflow>
        <div id="punch"><div id="shake">{scenes()}</div></div>
      </div>
      <div id="hud" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5">
        <div class="pill"><img src="assets/img/bird.png" alt=""><div class="ptrack"><div class="pfill"></div></div></div>
      </div>
      <div id="react" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-ignore>{reactions()}</div>
      <div id="birdlayer" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6" data-layout-allow-overflow>{bird.rig(star)}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{captions()}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8" data-layout-allow-overflow><div class="portal" data-layout-ignore>{"".join(f'<i class="prg prg{k}" style="border-color:{c}"></i>' for k, c in enumerate(["#E235DD", "#E68B70", "#F343A2", "#E235DD", "#F7B267", "#E34CB7"]))}</div><div id="wipe"></div><div id="whip"></div><div id="flash"></div>{speed_html()}</div>
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="32.13" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{timeline()}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    import json
    json.dump(sorted(EV), open(os.path.join(ROOT, "build", "sfx_events.json"), "w"))
    print("wrote index.html", len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
