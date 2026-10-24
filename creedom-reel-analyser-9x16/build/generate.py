"""Creedom reel analyser reel. 1080x1920, 33.6 s, cut to the Nota 3 voiceover.

python3 -I build/generate.py      (run from the project root)

Look: Creedom's app (paper #F6F6F4, ink #0B0B0B, pink, serif numerals) on the soft grid-and-pastel-glow background
of the reference covers. Headline with an italic-serif accent, one hero object, word-by-word captions with a pill on
the spoken word, and the pink bird as the lead: it never stands still (bob, sway, breathing, wing flutter) and changes
gesture on every line (walk, jump, flap, wave, scratch head, shrug, droop, scan, surf, startle, point). Every cut is a
whip pan; one dark beat for the twist. No account handles on screen.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing import DUR, KEY, SCENES, words  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = {k: (a, z) for k, a, z in SCENES}
PINK, PINKT, INK, PAPER, GREEN = "#E2557D", "#C93A6D", "#0B0B0B", "#F6F6F4", "#3E8E62"
TWIST = S["twist"]
# the hook clip also carries the "why" line, and "next" carries "numbers ≠ reasons"
SPAN = {"hook": (S["hook"][0], S["why"][1]), "next": (S["next"][0], S["nums"][1])}
CUTS = [S[k][0] for k in ("next", "read", "score", "analyse", "twist", "reasons", "cta")]

T = []


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
    """Headline: heavy sans line, then the italic-serif pink accent with a hand-drawn underline."""
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
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,rotationY:0,duration:{d},ease:"{ease}"}},{t:.2f});')


def out(sel, t, to="opacity:0,y:-30", d=.25):
    add(f'tl.to("{sel}",{{{to},duration:{d},ease:"power2.in"}},{t:.2f});')


def shine(sel, t):
    add(f'tl.fromTo("{sel} > .shine",{{xPercent:-160}},{{xPercent:260,duration:.7,ease:"power2.inOut"}},{t:.2f});')


def ring(cls, t, scale=3.2, d=.7):
    add(f'tl.fromTo(".{cls}",{{scale:.2,opacity:.9}},{{scale:{scale},opacity:0,duration:{d},ease:"power2.out"}},{t:.2f});')


def counter(sel, a, z, t, d, fmt="comma", ease="power2.out"):
    f = {"comma": "Math.round(o.v).toLocaleString('en-US')", "int": "Math.round(o.v)"}[fmt]
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


def magnifier(s=150):
    return (f'<svg viewBox="0 0 150 150" width="{s}" height="{s}"><path d="M92 92 L138 138" stroke="#8a5a2b" '
            f'stroke-width="16" stroke-linecap="round"/><circle cx="62" cy="62" r="44" fill="rgba(220,240,255,.45)" '
            f'stroke="#f2b134" stroke-width="12"/><path d="M40 48 C46 36 58 30 70 32" stroke="#fff" stroke-width="6" '
            f'fill="none" stroke-linecap="round" opacity=".9"/></svg>')


def bubble(inner, w=150, h=120, cls=""):
    return (f'<div class="bub {cls}" data-layout-ignore style="width:{w}px;height:{h}px">{inner}'
            f'<svg class="tail" viewBox="0 0 60 50" width="60" height="50"><circle cx="20" cy="12" r="11" fill="#fff" '
            f'stroke="{INK}" stroke-width="4"/><circle cx="6" cy="38" r="6" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            f'</svg></div>')


def cloud():
    drops = "".join(f'<i class="drop" style="left:{x}px"></i>' for x in (40, 80, 120, 60, 100))
    return (f'<div id="cloud" data-layout-ignore><svg viewBox="0 0 180 90" width="180" height="90"><path d="M30 80 C8 80 4 52 '
            f'26 46 C24 22 54 12 70 30 C80 6 122 8 126 36 C150 30 170 50 156 70 C152 78 146 80 140 80 Z" fill="#c9ccd6"/>'
            f'</svg>{drops}</div>')


def bird_rig():
    """The bird split into body + two wings (so it can wave and flap), lids, props and sparkles.
    Box is 300x318 (the 604x640 cut-out at half size). Bubbles sit outside the flip so their text never mirrors."""
    sp = "".join(f'<div class="bsp bsp{i}" style="left:{x}px;top:{y}px">{star(s, c)}</div>'
                 for i, (x, y, s, c) in enumerate([(-40, 40, 54, PINK), (270, -10, 44, "#f2b134"),
                                                   (290, 170, 36, PINK), (-20, 210, 34, "#f2b134")]))
    return (f'<div id="birdpos"><div id="bshadow"></div><div id="bflip"><div id="bwig"><div id="bidle"><div id="bbreath">'
            f'<div id="wingL"><div id="wingLi"><img src="assets/img/bird_wingl.png" width="300" height="318" alt=""></div></div>'
            f'<img id="bimg" src="assets/img/bird_body.png" width="300" height="318" alt="">'
            f'<div id="wingR"><div id="wingRi"><img src="assets/img/bird_wing.png" width="300" height="318" alt=""></div></div>'
            f'<div class="lid lidl"></div><div class="lid lidr"></div>'
            f'<div id="sweat"><svg viewBox="0 0 30 44" width="30" height="44"><path d="M15 0 C22 14 30 22 30 30 '
            f'C30 38 23 44 15 44 C7 44 0 38 0 30 C0 22 8 14 15 0 Z" fill="#7cc8ff"/></svg></div>'
            f'<div id="mag">{magnifier(150)}</div></div></div></div></div>'
            f'{bubble("<b>?</b>", 130, 120, "bq")}{bubble("<b>!</b>", 120, 120, "bx")}'
            f'{bubble("<i>CREEDOM</i>", 300, 110, "bc")}{cloud()}{sp}</div>')


# ------------------------------------------------------------------ scenes
def cover(cls, img, cnt_cls, label):
    return (f'<div class="cover card {cls}"><img src="assets/img/{img}" alt=""><i class="shine"></i></div>'
            f'<div class="vbar {cls}-v">{play(26, "#fff")}<span class="{cnt_cls}">0</span><span class="plab">{label}</span></div>')


def scenes():
    r = random.Random(4)
    burst = "".join(f'<div class="bst" data-x="{r.uniform(-360, 360):.0f}" data-y="{r.uniform(-460, -120):.0f}" '
                    f'data-r="{r.uniform(-90, 90):.0f}">{heart(r.choice([34, 44, 56])) if i % 3 else play(36, PINK)}</div>'
                    for i in range(18))
    ticker = " • ".join(["126,000 PLAYS", "85x YOUR USUAL", "+1 VIRAL REEL", "WHY?"] * 4)
    qrain = "".join(f'<div class="qr" style="left:{x}px;top:{y}px;font-size:{s}px">?</div>'
                    for x, y, s in [(110, 560, 120), (420, 470, 90), (900, 520, 110), (640, 900, 80), (150, 980, 70)])
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
        f'<div class="qrain" data-layout-ignore>{qrain}</div>'
    )))
    tiles = [("PLAYS", "126K"), ("PLAYS", "4.3K"), ("REACH", "↑ ↓"), ("SAVES", "?"), ("SHARES", "?"), ("WATCH TIME", "?")]
    out_.append(clip("next", (
        '<div class="ghost" data-layout-ignore>4K</div>' +
        hl("next", "The next one?", "~4K.") + hl("nums", "Numbers ≠", "reasons.") +
        '<div class="mini card"><img src="assets/img/cover_yt.jpg" alt=""><div class="mono">126K plays</div></div>' +
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
        '<div class="appic cr"><img src="assets/img/bird.png" alt=""></div></div>'
        '<div class="reading mono">READING YOUR PAGE</div>'
        '<div class="give">Give me <i>20 seconds.</i></div>'
        '<div class="rbar"><div class="rfill"></div></div>'
        '<div class="ticks card">' + "".join(f'<div class="trow {c}">{tick(46)}<span>{t}</span></div>' for t, c in rows) +
        '<i class="shine"></i></div><div class="chip stopw">⏱ <span class="cnt-s">0</span>s</div><div class="rg20 pring" '
        'data-layout-ignore></div>'
    )))
    thumbs = "".join(f'<div class="th th{i}" style="left:{120 + (i % 3) * 290}px;top:{450 + (i // 3) * 340}px">'
                     f'<img src="assets/img/post{i + 1}.jpg" alt=""></div>' for i in range(6))
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
        timeline("tl-a")
    )))
    out_.append(clip("twist", (
        '<div class="ghost gw" data-layout-ignore>0:34</div><div class="spot" data-layout-ignore></div>' +
        hl("twist", "Buried at", "0:34.") + timeline("tl-b") +
        '<div class="chip pinkchip besth">★ BEST HOOK</div><div class="rg34 pring" data-layout-ignore></div>' +
        confetti("cf34", 30, 8, 420, -380)
    ), "dark"))
    out_.append(clip("reasons", (
        '<div class="ghost" data-layout-ignore>✓</div>' + hl("reasons", "Now I edit with", "reasons.") +
        '<div class="gcard card"><div class="mono">GUESSES</div><div class="dice"><span class="d1">🎲</span> '
        '<span class="d2">🎲</span></div><div class="gq2"><span>?</span> <span>?</span> <span>?</span></div>'
        '<div class="strike"></div></div>'
        '<div class="rcard card"><div class="mono pk">REASONS · FROM CREEDOM</div>'
        f'<div class="rr rr0">{tick(40)}<span>Lead with the Congress tracker</span></div>'
        f'<div class="rr rr1">{tick(40)}<span>Trim two tool cards (0:10–0:19)</span></div>'
        f'<div class="rr rr2">{tick(40)}<span>Keep the 0:03 simulation proof</span></div><i class="shine"></i></div>'
    )))
    chips = "".join(f'<div class="kc kc{i}" data-layout-ignore style="left:{x}px;top:{y}px">{w}</div>' for i, (x, y, w) in enumerate(
        [(70, 330, "CREEDOM"), (820, 300, "creedom 🙏"), (60, 700, "CREEDOM"), (840, 690, "CREEDOM!"),
         (110, 1120, "creedom"), (60, 1250, "CREEDOM 🔥")]))
    out_.append(clip("cta", (
        chips + '<div class="cmt"><svg viewBox="0 0 40 40" width="48" height="48"><path d="M4 6 H36 V28 H16 L8 36 V28 H4 Z" '
        'fill="#fff"/></svg>COMMENT</div><div class="kw">CREEDOM</div><div class="rgkw pring" data-layout-ignore></div>'
        '<div class="cbox card"><div class="mono">COMMENT TO GET THE LINK</div><div class="cin"><span class="typed"></span>'
        '<span class="caret"></span></div><div class="send"><svg viewBox="0 0 40 40" width="40" height="40"><path d="M4 20 '
        'L36 6 L28 36 L19 23 Z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/></svg></div>'
        '<div class="dm">✓ Link lands in your DMs</div><i class="shine"></i></div>'
        '<div class="plane" data-layout-ignore><svg viewBox="0 0 60 60" width="70" height="70"><path d="M4 30 L56 6 L44 54 '
        f'L30 36 Z" fill="{PINK}"/><path d="M30 36 L56 6" stroke="#fff" stroke-width="3"/></svg></div>' +
        confetti("cfkw", 40, 11) +
        '<div class="endlock"><img src="assets/img/bird.png" alt=""><span>creedom</span></div>'
        '<div class="endsub">Comment <b>CREEDOM</b> for the link</div>'
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
            add(f'tl.set("{sel}",{{backgroundColor:"{PINK}",color:"#ffffff"}},{s:.3f});')
            add(f'tl.set("{sel}",{{backgroundColor:"rgba(226,85,125,0)",color:"{past}"}},{e:.3f});')


# ------------------------------------------------------------------ the bird
def bird_tl():
    def mv(t, x, y, s, d=.5, ease="power3.inOut"):
        add(f'tl.to("#birdpos",{{x:{x},y:{y},scale:{s},duration:{d},ease:"{ease}"}},{t:.2f});')

    def face(t, d):
        add(f'tl.to("#bflip",{{scaleX:{d},duration:.16,ease:"power2.inOut"}},{t:.2f});')

    def hop(t, h=60):
        add(f'tl.to("#bwig",{{y:-{h},duration:.18,ease:"power2.out",yoyo:true,repeat:1}},{t:.2f});')
        add(f'tl.to("#bwig",{{scaleY:.86,scaleX:1.1,duration:.08,yoyo:true,repeat:1}},{t + .36:.2f});')

    def walk(t, d, step=.2):
        n = max(2, int(d / step))
        add(f'tl.to("#bwig",{{rotation:7,y:-14,duration:{step / 2:.3f},ease:"sine.inOut",yoyo:true,repeat:{n - 1}}},{t:.2f});')
        add(f'tl.to("#bwig",{{rotation:0,y:0,duration:.1}},{t + n * step / 2 + .01:.2f});')

    def flap(t, n=4, a=28):
        add(f'tl.to("#wingR",{{rotation:{a},duration:.07,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')
        add(f'tl.to("#wingL",{{rotation:-{a},duration:.07,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')

    def wave(t, n=3):
        add(f'tl.fromTo("#wingR",{{rotation:-12}},{{rotation:24,duration:.16,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1},'
            f'immediateRender:false}},{t:.2f});tl.to("#wingR",{{rotation:0,duration:.12}},{t + n * .32 + .01:.2f});')

    def tilt(t, a, d=.3):
        add(f'tl.to("#bwig",{{rotation:{a},duration:{d},ease:"back.out(2)"}},{t:.2f});')

    def wings(t, r, l, d=.25):
        add(f'tl.to("#wingR",{{rotation:{r},duration:{d},ease:"back.out(2)"}},{t:.2f});')
        add(f'tl.to("#wingL",{{rotation:{l},duration:{d},ease:"back.out(2)"}},{t:.2f});')

    def blink(t):
        add(f'tl.to(".lid",{{scaleY:1,duration:.06,yoyo:true,repeat:1}},{t:.2f});')

    def show(sel, t, on=True, d=.3):
        if on:
            add(f'tl.to("{sel}",{{opacity:1,scale:1,duration:{d},ease:"back.out(3)"}},{t:.2f});')
        else:
            add(f'tl.to("{sel}",{{opacity:0,scale:.5,duration:.2,ease:"power2.in"}},{t:.2f});')

    add('tl.set("#birdpos",{x:1160,y:1010,scale:.85},0);tl.set(".lid",{scaleY:0},0);tl.set("#wipe",{scale:0},0);')
    add('tl.set("#sweat,#mag,.bub,.bsp,#cloud",{opacity:0,scale:.5},0);tl.set("#bflip",{scaleX:-1},0);')
    # always alive: bob, sway, breathing, wing flutter (on their own wrappers, under the gestures)
    add(f'tl.to("#bidle",{{y:-8,duration:.42,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .42) - 1}}},0);')
    add(f'tl.fromTo("#bidle",{{rotation:-3}},{{rotation:3,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / 1.3) - 1}}},0);')
    add(f'tl.to("#bbreath",{{scaleY:1.025,scaleX:.985,duration:.8,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .8) - 1}}},0);')
    add(f'tl.fromTo("#wingRi",{{rotation:-4}},{{rotation:9,duration:.45,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .45) - 1}}},0);')
    add(f'tl.fromTo("#wingLi",{{rotation:4}},{{rotation:-7,duration:.5,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .5) - 1}}},0);')
    for t in (2.6, 6.2, 9.0, 13.2, 16.6, 20.6, 25.4, 28.8, 32.4):
        blink(t)
    # 1 hook: waddles in from the right, turns to camera, jumps and flaps on "85x"
    mv(.1, 660, 1010, .85, 1.0, "power1.out")
    walk(.1, 1.0)
    face(1.12, 1)
    hop(1.3, 110)
    flap(1.3, 4)
    show(".bsp", 1.4)
    add('tl.to(".bsp",{rotation:120,duration:1.2,ease:"none"},1.4);')
    show(".bsp", 2.6, False)
    wave(2.3, 2)
    # 2 why: scratches its head with the wing, head tilt, "?" bubble
    tilt(3.65, -11)
    wings(3.7, -38, 0)
    add('tl.to("#wingR",{rotation:-28,duration:.12,yoyo:true,repeat:7},3.95);')
    show(".bq", 3.9)
    show(".bq", 5.45, False)
    tilt(5.3, 0, .25)
    wings(5.3, 0, 0, .2)
    # 3 next: walks a little, droops with a rain cloud and sweat, wings hang
    face(5.6, -1)
    mv(5.6, 740, 1010, .82, .7, "power1.inOut")
    walk(5.6, .7)
    face(6.4, 1)
    add('tl.to("#bwig",{scaleY:.9,scaleX:1.06,duration:.3,ease:"power2.out"},6.9);')
    wings(6.9, 22, -18, .4)
    show("#sweat", 7.0)
    add('tl.to("#sweat",{y:40,duration:.9,ease:"power1.in"},7.1);')
    show("#cloud", 6.95)
    add('tl.fromTo("#cloud .drop",{y:0,opacity:1},{y:90,opacity:0,duration:.35,stagger:.07,repeat:2,ease:"power1.in"},7.05);')
    show("#sweat", 8.0, False)
    show("#cloud", 8.0, False)
    add('tl.to("#bwig",{scaleY:1,scaleX:1,duration:.25},8.05);')
    wings(8.05, 0, 0, .2)
    # 4 numbers: startled by the tiles, then a big shrug
    mv(8.1, 770, 1060, .75, .4)
    add('tl.to("#bwig",{scaleY:1.14,scaleX:.9,y:-30,duration:.12,yoyo:true,repeat:1},8.4);')
    wings(9.25, 45, -40, .2)
    add('tl.to("#bwig",{rotation:8,duration:.09,ease:"sine.inOut",yoyo:true,repeat:5},9.3);')
    wings(9.95, 0, 0, .2)
    # 5 read: magnifier, waddles left along the ticks card scanning, turns back and hops at "20 s"
    mv(10.45, 800, 1130, .72, .5)
    show("#mag", 10.8)
    face(11.0, -1)
    mv(11.0, 520, 1130, .72, 1.6, "sine.inOut")
    walk(11.0, 1.6, .26)
    add('tl.to("#mag",{rotation:-14,y:-20,duration:.4,ease:"sine.inOut",yoyo:true,repeat:3},11.0);')
    face(12.7, 1)
    hop(12.85, 70)
    show("#mag", 13.8, False)
    # 6 score: perched by the black card, jumps, spins and flaps on 82, then waves
    mv(13.9, 730, 1100, .7, .45)
    hop(15.35, 140)
    add('tl.to("#bflip",{rotation:360,duration:.55,ease:"power2.inOut"},15.35);tl.set("#bflip",{rotation:0},15.95);')
    flap(15.35, 5, 34)
    show(".bsp", 15.45)
    add('tl.to(".bsp",{rotation:220,duration:1.3,ease:"none"},15.45);')
    show(".bsp", 16.8, False)
    wave(16.1, 2)
    # 7 analyse: points at the chat with a wing, then surfs the playhead down the timeline
    mv(17.05, 760, 1060, .6, .45)
    face(17.3, -1)
    wings(17.4, 40, 0, .25)
    add('tl.to("#wingR",{rotation:30,duration:.15,yoyo:true,repeat:5},17.65);')
    wings(18.9, 0, 0, .2)
    face(19.6, 1)
    mv(19.85, -60, 330, .42, .4)
    tilt(20.2, 12)
    wings(20.2, 35, -30, .2)
    add('tl.to("#birdpos",{y:960,duration:1.05,ease:"power1.inOut"},20.25);')
    tilt(21.25, 0, .2)
    wings(21.25, 0, 0, .2)
    # 8 twist: magnifier on the 0:34 row, startled "!", then flaps up after it
    mv(21.35, -60, 822, .45, .4)
    show("#mag", 21.6)
    add('tl.to("#mag",{x:40,duration:.4,ease:"sine.inOut",yoyo:true,repeat:3},21.8);')
    show(".bx", 23.4)
    add('tl.to("#bwig",{scaleY:1.18,scaleX:.88,y:-60,duration:.13,yoyo:true,repeat:1},23.35);')
    wings(23.35, 45, -42, .15)
    show("#mag", 24.3, False)
    show(".bx", 24.5, False)
    flap(24.65, 5, 32)
    mv(24.7, -60, 372, .45, .55, "power3.inOut")
    wings(25.4, 0, 0, .2)
    wave(25.62, 2)
    # 9 reasons: stands on the guesses card, jumps across to the reasons card, cheers
    mv(26.3, 150, 332, .5, .45)
    face(26.6, 1)
    tilt(26.6, -8, .2)
    tilt(26.95, 0, .1)
    add('tl.to("#birdpos",{x:700,duration:.6,ease:"power2.inOut"},27.0);')
    add('tl.to("#birdpos",{y:200,duration:.3,ease:"power2.out",yoyo:true,repeat:1},27.0);')
    flap(27.0, 4)
    add('tl.to("#birdpos",{y:282,duration:.15,ease:"power2.out"},27.62);')
    hop(28.4, 70)
    wave(28.75, 2)
    # 10 cta: thought bubble, points at the comment box, then waves goodbye at the centre
    mv(29.4, 730, 1080, .7, .45)
    show(".bc", 29.9)
    face(30.1, -1)
    wings(30.15, 42, 0, .25)
    add('tl.to("#wingR",{rotation:32,duration:.15,yoyo:true,repeat:5},30.4);')
    show(".bc", 32.0, False)
    face(32.0, 1)
    wings(32.0, 0, 0, .15)
    mv(32.1, 390, 900, 1.05, .5, "back.out(1.4)")
    hop(32.15, 60)
    wave(32.55, 3)
    add('tl.set("#bshadow",{opacity:.0},0);tl.to("#bshadow",{opacity:1,duration:.3},.6);')


# ------------------------------------------------------------------ scene timelines
def timeline():
    # whip pan on every cut: blur out to the left, in from the right
    for t in CUTS:
        add(f'tl.to("#cam",{{x:-140,filter:"blur(10px)",duration:.12,ease:"power2.in"}},{t - .12:.2f});')
        add(f'tl.fromTo("#cam",{{x:160,filter:"blur(12px)"}},{{x:0,filter:"blur(0px)",duration:.3,ease:"power3.out",'
            f'immediateRender:false}},{t:.2f});')
        add(f'tl.fromTo("#whip",{{opacity:.9,x:300}},{{opacity:0,x:-300,duration:.28,ease:"power2.out",immediateRender:false}},'
            f'{t - .08:.2f});')
    # slow push-in inside each scene so nothing is ever static
    for k, a, z in SCENES:
        add(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.035,duration:{z - a - .05:.2f},ease:"none",immediateRender:false}},{a:.2f});')
    # 1 hook
    hl_in("hook", .05)
    pop(".cv-a", .15, "y:260,opacity:0,rotation:-8,rotationY:40,scale:.8", .6)
    shine(".cv-a", .7)
    pop(".cv-a-v", .5, "y:40,opacity:0,scale:.8", .35)
    counter(".cnt-a", 0, 126000, .4, 2.6, "comma", "expo.out")
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
    add('tl.fromTo(".qr",{opacity:0,scale:.2,rotation:-30},{opacity:1,scale:1,rotation:(i)=>[-12,10,-8,14,-6][i],duration:.45,'
        'stagger:.12,ease:"back.out(2.5)"},3.75);')
    add('tl.to(".qr",{y:-40,duration:.8,ease:"sine.inOut",yoyo:true,repeat:1},4.4);')
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
    add(f'tl.fromTo("#wipe",{{scale:0}},{{scale:1,duration:.38,ease:"power3.in",immediateRender:false}},{t - .35:.2f});')
    add(f'tl.to("#wipe",{{opacity:0,duration:.3}},{t + .05:.2f});tl.set("#wipe",{{scale:0,opacity:1}},{t + .4:.2f});')
    pop(".appic.ig", t + .05, "scale:0,opacity:0,rotation:-30", .45, "back.out(2.6)")
    pop(".appic.cr", t + .15, "scale:0,opacity:0,rotation:30", .45, "back.out(2.6)")
    add(f'tl.fromTo(".dash",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power2.out"}},{t + .3:.2f});')
    add(f'tl.fromTo(".dash path",{{strokeDashoffset:0}},{{strokeDashoffset:-260,duration:3.2,ease:"none"}},{t + .3:.2f});')
    pop(".lpill", t + .55, "scale:.3,opacity:0", .4, "back.out(3)")
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
    add(f'tl.fromTo(".th",{{opacity:0,y:300,rotation:(i)=>(i%2?14:-14),scale:.5}},{{opacity:1,y:0,rotation:(i)=>(i%2?2:-2),'
        f'scale:1,duration:.4,stagger:.07,ease:"back.out(1.8)"}},{t + .15:.2f});')
    add(f'tl.to(".th",{{x:(i)=>[300,10,-280,300,10,-280][i],y:(i)=>(i<3?260:-80),scale:.15,opacity:0,rotation:180,'
        f'duration:.45,stagger:.03,ease:"power3.in"}},{t + 1.0:.2f});')
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
    # 8 twist
    t = S["twist"][0]
    add(f'tl.to("#dark",{{opacity:1,duration:.4,ease:"power2.out"}},{t - .1:.2f});')
    add(f'tl.to("#dark",{{opacity:0,duration:.35,ease:"power2.in"}},{S["twist"][1] - .1:.2f});')
    add(f'tl.fromTo(".spot",{{rotation:-25,opacity:0}},{{rotation:20,opacity:1,duration:1.6,ease:"sine.inOut"}},{t + .1:.2f});')
    add('tl.to(".spot",{rotation:0,duration:.5,ease:"power2.out"},23.2);')
    hl_in("twist", t + .3)
    add(f'tl.to(".tl-b .tr:not(.tr3)",{{opacity:.28,duration:.4}},{t + .5:.2f});')
    add(f'tl.to(".tl-b .tr3",{{scale:1.06,backgroundColor:"#FEF0F4",boxShadow:"0 0 0 4px {PINK}, 0 20px 60px rgba(226,85,125,.55)",'
        f'duration:.45,ease:"back.out(2)"}},23.3);')
    pop(".besth", 23.45, "scale:.3,opacity:0,rotation:-12", .4, "back.out(3)")
    ring("rg34", 23.4, 3.6)
    add('tl.to("#punch",{scale:1.09,duration:.25,ease:"power2.out",yoyo:true,repeat:1},23.4);')
    add('tl.to(".tl-b .tr3",{y:-450,duration:.6,ease:"power3.inOut"},24.7);')
    add('tl.to(".tl-b .tr0, .tl-b .tr1, .tl-b .tr2",{y:150,duration:.6,ease:"power3.inOut"},24.7);')
    add('tl.to(".besth",{y:-450,duration:.6,ease:"power3.inOut"},24.7);')
    add('tl.to(".tl-b .tt3",{opacity:0,duration:.15},24.9);')
    add('(()=>{const o={v:0};tl.to(o,{v:1,duration:.01,onUpdate:()=>{document.querySelector(".tl-b .tt3").textContent='
        'o.v>.5?"0:00–0:07":"0:34–0:41";}},25.05);})();')
    add('tl.to(".tl-b .tt3",{opacity:1,duration:.2},25.06);')
    confetti_tl("cf34", 25.25)
    # 9 reasons
    t = S["reasons"][0]
    hl_in("reasons", t + .05)
    pop(".gcard", t + .15, "x:-200,opacity:0,rotation:-14,scale:.85", .45)
    pop(".rcard", t + .35, "x:200,opacity:0,rotation:14,scale:.85", .45)
    add('tl.to(".d1",{rotation:360,duration:.5,ease:"power2.out",repeat:2},26.5);tl.to(".d2",{rotation:-360,duration:.5,'
        'ease:"power2.out",repeat:2},26.6);')
    add('tl.to(".gq2 span",{y:-16,duration:.3,stagger:.1,yoyo:true,repeat:3,ease:"sine.inOut"},26.6);')
    shine(".rcard", 27.0)
    for i, tt in enumerate((26.9, 27.35, 27.8)):
        pop(f".rr{i}", tt, "x:40,opacity:0", .3)
        add(f'tl.fromTo(".rr{i} .tk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.25}},{tt + .1:.2f});')
    add('tl.fromTo(".strike",{scaleX:0},{scaleX:1,duration:.3,ease:"power3.out"},28.4);')
    add('tl.to(".gcard",{opacity:.45,filter:"grayscale(1)",rotation:-8,y:40,duration:.3},28.5);')
    add('tl.to(".rcard",{scale:1.05,duration:.2,yoyo:true,repeat:1},28.5);')
    # 10 cta
    t = S["cta"][0]
    pop(".cmt", t + .05, "y:-120,opacity:0,rotation:-20,scale:.7", .45, "bounce.out")
    pop(".kw", 29.75, "scale:2.4,opacity:0,rotation:8", .45, "back.out(1.8)")
    ring("rgkw", 29.85, 3)
    confetti_tl("cfkw", 29.85)
    add('tl.to("#punch",{scale:1.08,duration:.2,ease:"power2.out",yoyo:true,repeat:1},29.8);')
    add('tl.fromTo(".kc",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.35,stagger:.08,ease:"back.out(2)"},29.9);')
    add('tl.to(".kc",{y:(i)=>(i%2?-34:34),x:(i)=>(i%3?16:-16),rotation:(i)=>(i%2?6:-6),duration:2.0,ease:"sine.inOut"},30.2);')
    add('tl.to(".kw",{scale:1.04,duration:.3,yoyo:true,repeat:3,ease:"sine.inOut"},30.4);')
    pop(".cbox", 30.0, "y:120,opacity:0,scale:.9", .45)
    shine(".cbox", 30.4)
    word = "CREEDOM"
    add(f'(()=>{{const o={{v:0}};tl.to(o,{{v:{len(word)},duration:{len(word) * .1:.2f},ease:"none",onUpdate:()=>{{'
        f'document.querySelector(".typed").textContent="{word}".slice(0,Math.floor(o.v+.001));}}}},30.25);}})();')
    add(f'tl.to(".caret",{{opacity:0,duration:.01,yoyo:true,repeat:{int((DUR - 30.2) / .5) * 2 - 1},repeatDelay:.49}},30.2);')
    add('tl.to(".send",{scale:1.18,duration:.15,yoyo:true,repeat:3},31.0);')
    add('tl.fromTo(".plane",{x:0,y:0,opacity:0,rotation:0,scale:.6},{x:260,y:-560,opacity:1,rotation:-25,scale:1.1,duration:.8,'
        'ease:"power2.in"},31.05);tl.to(".plane",{opacity:0,duration:.2},31.86);')
    pop(".dm", 31.25, "opacity:0,y:20", .3)
    out(".cmt, .kw, .kc, .cbox", 32.0, "opacity:0,y:-40,scale:.9", .3)
    pop(".endlock", 32.15, "scale:.4,opacity:0,y:60", .5, "back.out(2.4)")
    pop(".endsub", 32.45, "opacity:0,y:30", .4)
    # background and always-on pieces
    add(f'tl.fromTo(".pfill",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none"}},0);')
    add(f'tl.fromTo("#gridl",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"0px -324px",duration:{DUR},ease:"none"}},0);')
    for i, (dx, dy, d) in enumerate([(220, 160, 7), (-200, 220, 9), (160, -240, 8)]):
        add(f'tl.fromTo(".blob{i}",{{x:0,y:0}},{{x:{dx},y:{dy},duration:{d},ease:"sine.inOut",yoyo:true,repeat:{int(DUR / d)}}},0);')
    add(f'document.querySelectorAll(".tw").forEach((e,i)=>tl.fromTo(e,{{scale:.3,opacity:.15}},{{scale:1,opacity:.9,'
        f'duration:.7,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .7) - 2}}},i*.23));')
    caption_tl()
    bird_tl()
    return "\n".join(T)


def background():
    r = random.Random(6)
    blobs = "".join(f'<div class="blob blob{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></div>'
                    for i, (x, y, s, c) in enumerate([(-260, -160, 900, "#F9C6D3"), (520, 900, 1000, "#F8D9C2"),
                                                      (420, -200, 760, "#DAD6F6")]))
    twinkles = "".join(f'<div class="tw" style="left:{r.uniform(40, 1000):.0f}px;top:{r.uniform(150, 1750):.0f}px">'
                       f'{star(r.choice([18, 24, 30]), r.choice([PINK, "#F2B134", "#B39DDB"]))}</div>' for _ in range(14))
    return (f'<div id="paper"></div><div id="blobs">{blobs}</div><div id="gridl"></div>'
            f'<div id="twk" data-layout-ignore>{twinkles}</div><div id="dark"></div>')


CSS = """
@font-face { font-family: "Fraunces"; font-weight: 100 900; src: url("assets/fonts/fraunces.ttf"); }
@font-face { font-family: "Fraunces"; font-style: italic; font-weight: 100 900; src: url("assets/fonts/fraunces-italic.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 100 800; src: url("assets/fonts/jbmono.ttf"); }
:root { --pink: #E2557D; --pinkt: #C93A6D; --ink: #0B0B0B; --paper: #F6F6F4; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--paper); }
body { font-family: "Manrope", sans-serif; color: var(--ink); }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--paper); }
.clip { position: absolute; inset: 0; }
#cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
#punch { position: absolute; inset: 0; transform-origin: 50% 45%; perspective: 1400px; }
.mono { font: 600 24px "JBMono"; letter-spacing: 5px; color: #6b6b66; }
/* background: the reference covers' soft pastel glow on a fine grid */
#paper { position: absolute; inset: 0; background: var(--paper); }
#blobs { position: absolute; inset: 0; filter: blur(90px); opacity: .85; }
.blob { position: absolute; border-radius: 50%; }
#gridl { position: absolute; inset: 0; background-image: linear-gradient(rgba(11,11,11,.055) 1.5px, transparent 1.5px),
  linear-gradient(90deg, rgba(11,11,11,.055) 1.5px, transparent 1.5px); background-size: 54px 54px; }
.tw { position: absolute; }
#dark { position: absolute; inset: 0; opacity: 0;
  background: radial-gradient(90% 60% at 50% 45%, #3a1d26 0%, #1b0f14 55%, #0d0709 100%); }
.ghost { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font: italic 600 520px/1 "Fraunces";
  color: rgba(11,11,11,.045); letter-spacing: -20px; white-space: nowrap; }
.ghost.gw { color: rgba(255,255,255,.05); font-size: 400px; }
#whip { position: absolute; inset: 0; opacity: 0; z-index: 41; background: repeating-linear-gradient(0deg,
  rgba(255,255,255,0) 0 22px, rgba(255,255,255,.55) 22px 26px, rgba(255,255,255,0) 26px 70px); }
/* progress pill */
.pill { position: absolute; right: 56px; top: 56px; width: 300px; height: 56px; border-radius: 28px; background: rgba(255,255,255,.85);
  box-shadow: 0 6px 24px rgba(0,0,0,.08); display: flex; align-items: center; gap: 14px; padding: 0 18px; }
.pill img { width: 36px; height: 38px; }
.ptrack { flex: 1; height: 10px; border-radius: 5px; background: #ebe8e4; overflow: hidden; }
.pfill { width: 100%; height: 100%; background: var(--pink); transform-origin: 0 50%; }
/* headline */
.hl { position: absolute; left: 0; width: 1080px; text-align: center; z-index: 6; }
.l1 { font: 800 84px/1.05 "Manrope"; letter-spacing: -3px; }
.l2 { font: italic 600 112px/1.05 "Fraunces"; letter-spacing: -3px; color: var(--pinkt); }
.hw, .acc { display: inline-block; }
.acc { position: relative; }
.sw { position: absolute; left: 4%; bottom: -14px; width: 92%; height: 34px; overflow: visible; }
.dark .l1, .dark .hl { color: #fff; }
.dark .l2 { color: #FF8FAE; }
/* cards */
.card { background: #fff; border-radius: 34px; box-shadow: 0 24px 60px rgba(11,11,11,.12), 0 2px 0 rgba(11,11,11,.04);
  overflow: hidden; }
.shine { position: absolute; top: -20%; left: 0; width: 38%; height: 140%; transform: rotate(18deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.75), rgba(255,255,255,0)); pointer-events: none; }
.chip { position: absolute; border-radius: 40px; font: 800 34px "Manrope"; padding: 14px 28px; white-space: nowrap; }
.pinkchip { background: var(--pink); color: #fff; }
.redchip { background: #fde8e8; color: #c43c3c; }
.pring { position: absolute; width: 220px; height: 220px; border-radius: 50%; border: 8px solid var(--pink); opacity: 0; }
.conf { position: absolute; left: 540px; top: 900px; }
.conf i { position: absolute; left: 0; top: 0; opacity: 0; }
.sticker { position: absolute; font-size: 96px; }
/* hook */
.ticker { position: absolute; left: -40px; top: 420px; width: 1160px; height: 64px; background: var(--ink); color: #fff;
  overflow: hidden; transform: rotate(-2deg); font: 700 28px "JBMono"; letter-spacing: 3px; white-space: nowrap; }
.tk-in { position: absolute; left: 0; top: 14px; }
.cover { position: absolute; left: 80px; top: 540px; width: 440px; height: 501px; border-radius: 36px; }
.cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.vbar { position: absolute; left: 110px; top: 1062px; height: 76px; display: flex; align-items: center; gap: 12px; padding: 0 28px;
  border-radius: 38px; background: var(--ink); color: #fff; font: 800 44px "Manrope"; }
.plab { font: 600 24px "Manrope"; opacity: .8; }
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
.qr { position: absolute; font: italic 700 100px "Fraunces"; color: var(--pinkt); opacity: 0; }
/* next */
.mini { position: absolute; left: 60px; top: 560px; width: 220px; padding: 14px; transform: rotate(-4deg); }
.mini img { width: 100%; border-radius: 18px; display: block; }
.mini .mono { margin-top: 10px; font-size: 20px; letter-spacing: 2px; color: var(--pinkt); }
.cv-b { left: 330px; top: 520px; width: 440px; height: 495px; }
.cv-b-v { left: 360px; top: 1040px; }
.lowk { left: 60px; top: 900px; }
.arrowdn { position: absolute; left: 140px; top: 990px; font: 800 120px "Manrope"; color: #c43c3c; }
.grid6 { position: absolute; left: 90px; top: 520px; width: 900px; display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
.tile { height: 170px; padding: 26px 30px; position: relative; }
.tile .mono { font-size: 22px; }
.tv { font: italic 700 60px "Fraunces"; margin-top: 4px; }
.tb { height: 10px; border-radius: 5px; background: #eee; margin-top: 10px; }
/* read */
.link { position: absolute; left: 0; width: 1080px; top: 170px; height: 170px; }
.appic { position: absolute; top: 20px; width: 150px; height: 150px; border-radius: 40px; display: flex; align-items: center;
  justify-content: center; box-shadow: 0 20px 50px rgba(11,11,11,.15); }
.appic.ig { left: 170px; background: linear-gradient(135deg, #FEDA75, #FA7E1E 30%, #D62976 60%, #962FBF 85%, #4F5BD5); }
.appic.cr { left: 760px; background: #fff; }
.appic.cr img { width: 112px; height: 119px; }
.dash { position: absolute; left: 330px; top: 85px; transform-origin: 0 50%; }
.lpill { position: absolute; left: 395px; top: 70px; background: var(--ink); color: #fff; font: 700 30px "Manrope"; padding: 10px 26px;
  border-radius: 30px; white-space: nowrap; }
.reading { position: absolute; left: 0; width: 1080px; top: 382px; text-align: center; font-size: 30px; letter-spacing: 8px; color: #555; }
.give { position: absolute; left: 0; width: 1080px; top: 430px; text-align: center; font: 700 96px "Fraunces"; letter-spacing: -2px; }
.give i { color: var(--pinkt); }
.rbar { position: absolute; left: 120px; top: 600px; width: 840px; height: 14px; border-radius: 7px; background: #ebe8e4; overflow: hidden; }
.rfill { width: 100%; height: 100%; background: var(--pink); transform-origin: 0 50%; }
.ticks { position: absolute; left: 100px; top: 680px; width: 880px; padding: 34px 40px; }
.trow { display: flex; align-items: center; gap: 24px; font: 500 40px "Manrope"; color: #444; padding: 20px 0; }
.stopw { left: 720px; top: 990px; background: var(--ink); color: #fff; }
.rg20 { left: 740px; top: 920px; }
/* score */
.th { position: absolute; width: 230px; height: 320px; border-radius: 24px; overflow: hidden; box-shadow: 0 18px 40px rgba(11,11,11,.18); }
.th img { width: 100%; height: 100%; object-fit: cover; }
.scard { position: absolute; left: 90px; top: 450px; width: 900px; height: 640px; border-radius: 44px; background: var(--ink); color: #fff;
  padding: 50px 56px; box-shadow: 0 40px 80px rgba(11,11,11,.3); overflow: hidden; }
.scard .mono { color: #b9b9b2; }
.snum { font: 600 230px/1 "Fraunces"; margin-top: 10px; }
.snum small { font-size: 74px; color: #9a9a92; margin-left: 10px; }
.ring { position: absolute; right: 56px; top: 90px; }
.sl2 { color: #FF8FAE !important; margin-top: 34px; }
.sins { font: 600 50px/1.2 "Fraunces"; margin-top: 14px; }
.sins i { color: #ffb3c6; }
.scard .shine { background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.18), rgba(255,255,255,0)); }
.rg82 { left: 230px; top: 640px; }
.cf82 { left: 300px; top: 760px; }
/* analyse */
.ubub { position: absolute; right: 70px; top: 470px; width: 760px; background: var(--ink); color: #fff; border-radius: 40px 40px 10px 40px;
  padding: 34px 40px; font: 600 42px/1.3 "Manrope"; }
.ubt { display: block; }
.onit { position: absolute; left: 70px; top: 760px; width: 760px; padding: 34px 40px; }
.oh { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.oh img { width: 44px; height: 46px; }
.orow { display: flex; align-items: center; gap: 20px; font: 500 34px "Manrope"; color: #444; padding: 12px 0; }
.scanph { position: absolute; left: 850px; top: 780px; width: 180px; height: 290px; border-radius: 22px; overflow: hidden;
  box-shadow: 0 18px 40px rgba(11,11,11,.2); }
.scanph img { width: 100%; height: 100%; object-fit: cover; }
.scanl { position: absolute; left: 0; right: 0; top: -6px; height: 6px; background: var(--pink); box-shadow: 0 0 20px var(--pink); }
.tlc { position: absolute; left: 190px; top: 440px; width: 840px; height: 880px; padding: 34px 40px; overflow: visible; }
.tlh { display: flex; justify-content: space-between; align-items: center; }
.sc42 { font: 700 32px "Manrope"; color: var(--ink); }
.sc42 small { color: #888; font-size: 24px; }
.tline { position: absolute; left: 62px; top: 140px; width: 4px; height: 640px; background: #e4e1dc; transform-origin: 50% 0; }
.phd { position: absolute; left: 52px; top: 140px; width: 24px; height: 24px; border-radius: 50%; background: var(--pink);
  box-shadow: 0 0 0 8px rgba(226,85,125,.25); opacity: 0; z-index: 3; }
.tr { position: absolute; left: 30px; width: 780px; height: 120px; border-radius: 26px; display: flex; align-items: center; gap: 22px;
  padding: 0 30px; background: #fff; }
.dot { width: 26px; height: 26px; border-radius: 50%; flex: none; }
.tr b { font: 800 34px "Manrope"; letter-spacing: -1px; white-space: nowrap; }
.tt { font: 500 24px "JBMono"; color: #888; white-space: nowrap; }
.ts { margin-left: auto; font: 700 36px "Fraunces"; color: #555; }
.besth { left: 640px; top: 978px; z-index: 5; font-size: 26px; padding: 8px 20px; }
.spot { position: absolute; left: 240px; top: -300px; width: 600px; height: 1800px; transform-origin: 50% 0;
  background: linear-gradient(180deg, rgba(255,214,230,.22), rgba(255,214,230,0) 80%); clip-path: polygon(45% 0, 55% 0, 100% 100%, 0 100%); }
.rg34 { left: 620px; top: 960px; }
.cf34 { left: 600px; top: 620px; }
/* reasons */
.gcard { position: absolute; left: 70px; top: 640px; width: 440px; height: 520px; padding: 40px; transform: rotate(-3deg); }
.dice { font-size: 110px; margin-top: 50px; text-align: center; }
.dice span { display: inline-block; }
.gq2 { font: italic 700 90px "Fraunces"; color: #bbb; text-align: center; margin-top: 30px; }
.gq2 span { display: inline-block; }
.strike { position: absolute; left: 30px; top: 250px; width: 380px; height: 14px; border-radius: 7px; background: var(--pink);
  transform: rotate(-14deg); transform-origin: 0 50%; }
.rcard { position: absolute; left: 540px; top: 600px; width: 480px; height: 600px; padding: 40px 34px; transform: rotate(2deg);
  box-shadow: 0 0 0 4px var(--pink), 0 30px 70px rgba(226,85,125,.3); }
.pk { color: var(--pinkt) !important; font-size: 21px; letter-spacing: 3px; }
.rr { display: flex; align-items: flex-start; gap: 16px; font: 700 36px/1.25 "Manrope"; margin-top: 34px; }
.rr svg { flex: none; margin-top: 2px; }
/* cta */
.cmt { position: absolute; left: 270px; top: 300px; display: flex; align-items: center; gap: 18px; background: var(--ink); color: #fff;
  font: 800 70px "Manrope"; letter-spacing: -1px; padding: 22px 46px; border-radius: 26px; transform: rotate(-3deg); }
.kw { position: absolute; left: 90px; top: 450px; width: 900px; text-align: center; background: var(--pink); color: #fff;
  font: 800 150px "Manrope"; letter-spacing: -5px; border-radius: 40px; padding: 18px 0; box-shadow: 0 30px 70px rgba(226,85,125,.45); }
.rgkw { left: 430px; top: 450px; }
.cfkw { left: 540px; top: 560px; }
.kc { position: absolute; background: #fff; border-radius: 30px; padding: 10px 22px; font: 700 26px "Manrope";
  box-shadow: 0 10px 26px rgba(11,11,11,.1); color: #444; }
.cbox { position: absolute; left: 90px; top: 760px; width: 900px; height: 300px; padding: 36px 40px; }
.cin { margin-top: 20px; width: 680px; height: 104px; border-radius: 22px; border: 4px solid var(--pink); display: flex; align-items: center;
  padding: 0 30px; font: 700 64px "JBMono"; letter-spacing: 6px; }
.caret { width: 5px; height: 64px; background: var(--ink); margin-left: 6px; }
.send { position: absolute; right: 40px; top: 100px; width: 120px; height: 104px; border-radius: 22px; background: var(--ink);
  display: flex; align-items: center; justify-content: center; }
.dm { margin-top: 22px; font: 600 30px "Manrope"; color: var(--pinkt); }
.plane { position: absolute; left: 860px; top: 880px; opacity: 0; }
.endlock { position: absolute; left: 0; width: 1080px; top: 330px; display: flex; justify-content: center; align-items: center; gap: 24px;
  font: 600 130px "Fraunces"; letter-spacing: -3px; }
.endlock img { width: 150px; height: 159px; }
.endsub { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font: 700 46px "Manrope"; color: #333; }
.endsub b { color: #fff; background: var(--pink); padding: 4px 18px; border-radius: 16px; }
/* bird */
#birdlayer { z-index: 20; }
#birdpos { position: absolute; left: 0; top: 0; width: 300px; height: 318px; transform-origin: 50% 100%; }
#bshadow { position: absolute; left: 40px; top: 300px; width: 220px; height: 40px; border-radius: 50%;
  background: radial-gradient(closest-side, rgba(243,67,162,.35), rgba(243,67,162,0)); }
#bflip, #bwig, #bidle, #bbreath { position: absolute; inset: 0; transform-origin: 50% 100%; }
#bflip { transform-origin: 50% 60%; }
#bimg { position: absolute; left: 0; top: 0; filter: drop-shadow(0 18px 24px rgba(160,20,90,.25)); }
#wingR, #wingRi { position: absolute; inset: 0; transform-origin: 266px 154px; }
#wingL, #wingLi { position: absolute; inset: 0; transform-origin: 47px 209px; }
#wingR img, #wingL img { position: absolute; left: 0; top: 0; }
.lid { position: absolute; background: #f2499f; border-radius: 50%; transform-origin: 50% 0; }
.lidl { left: 70px; top: 70px; width: 76px; height: 72px; }
.lidr { left: 170px; top: 54px; width: 72px; height: 70px; }
#sweat { position: absolute; left: 250px; top: 30px; }
#mag { position: absolute; left: 150px; top: 140px; transform-origin: 30% 30%; }
.bub { position: absolute; left: 190px; top: -130px; background: #fff; border: 4px solid var(--ink); border-radius: 50px;
  display: flex; align-items: center; justify-content: center; font: 800 80px "Manrope"; color: var(--pinkt); }
.bub .tail { position: absolute; left: 6px; bottom: -48px; }
.bub i { font: 800 52px "JBMono"; font-style: normal; letter-spacing: 2px; }
.bc { left: -200px; top: -150px; }
.bsp { position: absolute; }
#cloud { position: absolute; left: 60px; top: -150px; width: 180px; height: 200px; }
.drop { position: absolute; top: 80px; width: 8px; height: 22px; border-radius: 4px; background: #7cc8ff; }
/* captions */
#caps { z-index: 30; }
.cap { position: absolute; left: 0; width: 1080px; top: 1400px; text-align: center; opacity: 0; white-space: nowrap; }
.cw { display: inline-block; font: 800 64px "Manrope"; letter-spacing: -1.5px; padding: 2px 14px; border-radius: 16px; opacity: 0; }
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
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-allow-overflow>{background()}</div>
      <div id="cam" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-allow-overflow>
        <div id="punch">{scenes()}</div>
      </div>
      <div id="hud" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5">
        <div class="pill"><img src="assets/img/bird.png" alt=""><div class="ptrack"><div class="pfill"></div></div></div>
      </div>
      <div id="birdlayer" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6" data-layout-allow-overflow>{bird_rig()}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{captions()}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8" data-layout-allow-overflow><div id="wipe"></div><div id="whip"></div></div>
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
    print("wrote index.html", len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
