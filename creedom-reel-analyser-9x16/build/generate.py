"""Creedom reel analyser reel for @ai.nxtlvl. 1080x1920, 33.6 s, cut to the Nota 3 voiceover.

python3 -I build/generate.py      (run from the project root)

Look: Creedom's own app (paper #F6F6F4, ink #0B0B0B, pink #EE688B, serif numerals) in the layout of the
@ai.nxtlvl reference reels: status row, headline with an italic-serif accent, one hero object, word-by-word captions
with a pill on the spoken word, and the pink bird as the character who reacts to every line. One dark beat for the
twist ("buried at 0:34").
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing import DUR, KEY, SCENES, words  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = {k: (a, z) for k, a, z in SCENES}
PINK, INK, PAPER, GREEN = "#E2557D", "#0B0B0B", "#F6F6F4", "#3E8E62"
TWIST = S["twist"]

T = []


def add(js):
    T.append("      " + js)


# the hook clip also carries the "why" line, and "next" carries "numbers ≠ reasons"
SPAN = {"hook": (S["hook"][0], S["why"][1]), "next": (S["next"][0], S["nums"][1])}


def clip(sid, inner, cls=""):
    a, z = SPAN.get(sid, S[sid])
    return (f'<div id="sc-{sid}" class="clip scene {cls}" data-start="{a}" data-duration="{round(z - a, 3)}" '
            f'data-track-index="{2 + list(S).index(sid) % 2}" data-layout-allow-overflow>{inner}</div>')


def hl(sid, l1, l2, y=170):
    """Headline: heavy sans line, then the italic-serif pink accent."""
    w1 = "".join(f'<span class="hw">{w}</span> ' for w in l1.split())
    return (f'<div class="hl hl-{sid}" style="top:{y}px"><div class="l1">{w1}</div>'
            f'<div class="l2"><span class="acc">{l2}</span></div></div>')


def hl_in(sid, t):
    add(f'tl.fromTo(".hl-{sid} .hw",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.45,stagger:.07,ease:"back.out(2)"}},{t:.2f});')
    add(f'tl.fromTo(".hl-{sid} .acc",{{scale:.4,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:0,duration:.55,'
        f'ease:"back.out(2.6)"}},{t + .22:.2f});')


def pop(sel, t, frm="scale:.6,opacity:0,y:40", d=.45, ease="back.out(2)"):
    add(f'tl.fromTo("{sel}",{{{frm}}},{{scale:1,opacity:1,x:0,y:0,rotation:0,duration:{d},ease:"{ease}"}},{t:.2f});')


def out(sel, t, to="opacity:0,y:-30", d=.25):
    add(f'tl.to("{sel}",{{{to},duration:{d},ease:"power2.in"}},{t:.2f});')


def counter(sel, a, z, t, d, fmt="comma", ease="power2.out"):
    f = {"comma": "Math.round(o.v).toLocaleString('en-US')", "int": "Math.round(o.v)",
         "k": "(o.v>=1000?(o.v/1000).toFixed(1).replace('.0','')+'K':Math.round(o.v))"}[fmt]
    add(f'(()=>{{const o={{v:{a}}};tl.to(o,{{v:{z},duration:{d},ease:"{ease}",onUpdate:()=>{{'
        f'document.querySelectorAll("{sel}").forEach(e=>e.textContent={f});}}}},{t:.2f});}})();')


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


def bird_rig():
    """The one bird pose plus lids, props and sparkles. Box is 300x318 (image 604x640 scaled)."""
    sp = "".join(f'<div class="bsp bsp{i}" style="left:{x}px;top:{y}px">{star(s, c)}</div>'
                 for i, (x, y, s, c) in enumerate([(-40, 40, 54, PINK), (270, -10, 44, "#f2b134"),
                                                   (290, 170, 36, PINK), (-20, 210, 34, "#f2b134")]))
    return (f'<div id="birdpos"><div id="bshadow"></div><div id="bwig"><div id="bbreath">'
            f'<img id="bimg" src="assets/img/bird.png" width="300" height="318" alt="">'
            f'<div class="lid lidl"></div><div class="lid lidr"></div>'
            f'<div id="sweat"><svg viewBox="0 0 30 44" width="30" height="44"><path d="M15 0 C22 14 30 22 30 30 '
            f'C30 38 23 44 15 44 C7 44 0 38 0 30 C0 22 8 14 15 0 Z" fill="#7cc8ff"/></svg></div>'
            f'<div id="mag">{magnifier(150)}</div></div></div>'
            f'{bubble("<b>?</b>", 130, 120, "bq")}{bubble("<b>!</b>", 120, 120, "bx")}'
            f'{bubble("<i>CREEDOM</i>", 300, 110, "bc")}{sp}</div>')


# ------------------------------------------------------------------ scenes
def phone(cls, img, cnt_cls, label):
    return (f'<div class="phone {cls}"><img src="assets/img/{img}" alt=""><div class="pbar">{play(26, "#fff")}'
            f'<span class="{cnt_cls}">0</span><span class="plab">{label}</span></div></div>')


def scenes():
    r = random.Random(4)
    burst = "".join(f'<div class="bst" data-x="{r.uniform(-330, 330):.0f}" data-y="{r.uniform(-420, -120):.0f}" '
                    f'data-r="{r.uniform(-90, 90):.0f}">{heart(r.choice([34, 44, 56])) if i % 3 else play(36, PINK)}</div>'
                    for i in range(16))
    spike = ("M0 230 L60 222 L120 226 L180 214 L240 220 L300 205 L330 40 L360 8")
    out_ = []
    out_.append(clip("hook", (
        '<div class="ghost" data-layout-ignore>85x</div>' +
        hl("hook", "One reel did", "85x.") + hl("why", "And I had", "no idea why.") +
        phone("ph-a", "post6.jpg", "cnt-a", "plays") +
        f'<div class="burst">{burst}</div>'
        f'<div class="chart card"><div class="mono">PLAYS · LAST 30 DAYS</div><svg viewBox="0 0 380 250" width="380" '
        f'height="250"><path d="M0 230 H380" stroke="#e6e6e2" stroke-width="2"/><path class="spk" d="{spike}" '
        f'stroke="{PINK}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>'
        f'<circle class="spkdot" cx="360" cy="8" r="11" fill="{PINK}"/></svg>'
        f'<div class="chip pinkchip c85">85x your usual</div></div>'
        '<div class="ghost gq" data-layout-ignore>?</div>'
    )))
    tiles = [("PLAYS", "126K"), ("PLAYS", "~3K"), ("REACH", "↑ ↓"), ("SAVES", "?"), ("SHARES", "?"), ("WATCH TIME", "?")]
    out_.append(clip("next", (
        '<div class="ghost" data-layout-ignore>3K</div>' +
        hl("next", "The next one?", "~3K.") + hl("nums", "Numbers ≠", "reasons.") +
        '<div class="mini card"><img src="assets/img/post6.jpg" alt=""><div class="mono">126K plays</div></div>' +
        phone("ph-b", "post1.jpg", "cnt-b", "plays") +
        '<div class="chip redchip lowk">↓ low thousands</div>'
        '<div class="grid6">' + "".join(f'<div class="tile card t{i}"><div class="mono">{a}</div><div class="tv">{b}</div>'
                                        f'<div class="tb" style="width:{40 + (i * 37) % 50}%"></div></div>'
                                        for i, (a, b) in enumerate(tiles)) + '</div>'
    )))
    rows = [("Found Nxtlvl.ai: 6,205 followers", "r1"), ("Scanned 6 recent posts", "r2"), ("Creator audit ready", "r3")]
    out_.append(clip("read", (
        '<div class="ghost" data-layout-ignore>20</div>'
        f'<div class="crhead"><img src="assets/img/bird.png" alt=""><span>creedom</span></div>'
        '<div class="reading mono">READING @AI.NXTLVL</div>'
        '<div class="give">Give me <i>20 seconds.</i></div>'
        '<div class="pub">◉ Public data only · nothing to connect</div>'
        '<div class="rbar"><div class="rfill"></div></div>'
        '<div class="ticks card">' + "".join(f'<div class="trow {c}">{tick(46)}<span>{t}</span></div>' for t, c in rows) +
        '</div><div class="chip stopw">⏱ <span class="cnt-s">0</span>s</div>'
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
        '<div class="mono sl2">YOUR TOP INSIGHT</div><div class="sins">The next job is <i>repeatability.</i></div></div>'
    )))
    tl_rows = [("Hook", "0:00–0:05", "5", GREEN), ("Skills Grid &amp; Tour", "0:05–0:19", "3", "#C8902E"),
               ("Time Machine Simulation", "0:19–0:34", "5", GREEN), ("Safety &amp; Congress Tracker", "0:34–0:41", "4", GREEN),
               ("Close", "0:41–0:46", "4", GREEN)]

    def timeline(cls):
        return (f'<div class="tlc card {cls}"><div class="tlh"><span class="mono">SECOND BY SECOND</span>'
                f'<span class="sc42">4.2<small>/5</small> · Very good</span></div><div class="tline"></div>' +
                "".join(f'<div class="tr tr{i}" style="top:{120 + i * 150}px"><span class="dot" style="background:{c}"></span>'
                        f'<b>{n}</b><span class="tt tt{i}">{t}</span><span class="ts">{s}</span></div>'
                        for i, (n, t, s, c) in enumerate(tl_rows)) + '</div>')
    out_.append(clip("analyse", (
        '<div class="ghost" data-layout-ignore>▶</div>' + hl("analyse", "Then its", "reel analyser.") +
        '<div class="ubub">Check “Comment TRADE and I\'ll DM you all 11 skills.”</div>'
        '<div class="onit card"><div class="mono oh"><img src="assets/img/bird.png" alt=""> CREEDOM · ON IT</div>' +
        "".join(f'<div class="orow o{i}">{tick(40)}<span>{t}</span></div>' for i, t in enumerate(
            ["Working out what you need…", "Sending the reel to the feedback engine…", "Watching the whole video…"])) +
        '</div><div class="scanph"><img src="assets/img/post2.jpg" alt=""><div class="scanl"></div></div>' +
        timeline("tl-a")
    )))
    out_.append(clip("twist", (
        '<div class="ghost gw" data-layout-ignore>0:34</div>' + hl("twist", "Buried at", "0:34.") + timeline("tl-b") +
        '<div class="chip pinkchip besth">★ BEST HOOK</div><div class="slot0"></div>'
    ), "dark"))
    out_.append(clip("reasons", (
        '<div class="ghost" data-layout-ignore>✓</div>' + hl("reasons", "Now I edit with", "reasons.") +
        '<div class="gcard card"><div class="mono">GUESSES</div><div class="dice">🎲 🎲</div>'
        '<div class="gq2">?  ?  ?</div><div class="strike"></div></div>'
        '<div class="rcard card"><div class="mono pk">REASONS · FROM CREEDOM</div>'
        f'<div class="rr rr0">{tick(40)}<span>Lead with the Congress tracker</span></div>'
        f'<div class="rr rr1">{tick(40)}<span>Trim two tool cards (0:10–0:19)</span></div>'
        f'<div class="rr rr2">{tick(40)}<span>Keep the 29% honesty beat</span></div></div>'
    )))
    r2 = random.Random(9)
    chips = "".join(f'<div class="kc kc{i}" data-layout-ignore style="left:{x}px;top:{y}px">{w}</div>' for i, (x, y, w) in enumerate(
        [(70, 330, "CREEDOM"), (820, 300, "creedom 🙏"), (60, 700, "CREEDOM"), (840, 690, "CREEDOM!"),
         (110, 1120, "creedom"), (800, 1180, "CREEDOM 🔥")]))
    out_.append(clip("cta", (
        chips + '<div class="cmt"><svg viewBox="0 0 40 40" width="48" height="48"><path d="M4 6 H36 V28 H16 L8 36 V28 H4 Z" '
        'fill="#fff"/></svg>COMMENT</div><div class="kw">CREEDOM</div>'
        '<div class="cbox card"><div class="mono">COMMENT TO GET THE LINK</div><div class="cin"><span class="typed"></span>'
        '<span class="caret"></span></div><div class="send"><svg viewBox="0 0 40 40" width="40" height="40"><path d="M4 20 '
        'L36 6 L28 36 L19 23 Z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/></svg></div>'
        '<div class="dm">✓ Link lands in your DMs</div></div>'
        f'<div class="endig">{ig_icon(120)}<div>@AI.NXTLVL</div></div>'
    )))
    _ = r2
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
            past = ("#FF8FAE" if dark else "#D9467A") if w in KEY else ink
            sel = f".cw{ci}_{wi}"
            add(f'tl.fromTo("{sel}",{{opacity:0,y:18,scale:.85}},{{opacity:1,y:0,scale:1,duration:.16,ease:"back.out(3)",'
                f'immediateRender:false}},{s:.3f});')
            add(f'tl.set("{sel}",{{backgroundColor:"{PINK}",color:"#ffffff"}},{s:.3f});')
            add(f'tl.set("{sel}",{{backgroundColor:"rgba(226,85,125,0)",color:"{past}"}},{e:.3f});')


# ------------------------------------------------------------------ the bird
def bird_tl():
    def mv(t, x, y, s, d=.5, ease="power3.inOut"):
        add(f'tl.to("#birdpos",{{x:{x},y:{y},scale:{s},duration:{d},ease:"{ease}"}},{t:.2f});')

    def hop(t, h=60):
        add(f'tl.to("#bwig",{{y:-{h},duration:.18,ease:"power2.out",yoyo:true,repeat:1}},{t:.2f});')
        add(f'tl.to("#bwig",{{scaleY:.86,scaleX:1.1,duration:.08,yoyo:true,repeat:1}},{t + .36:.2f});')

    def wiggle(t, n=3, a=8):
        add(f'tl.to("#bwig",{{rotation:{a},duration:.1,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')

    def blink(t):
        add(f'tl.to(".lid",{{scaleY:1,duration:.06,yoyo:true,repeat:1}},{t:.2f});')

    def show(sel, t, on=True, d=.3):
        if on:
            add(f'tl.to("{sel}",{{opacity:1,scale:1,duration:{d},ease:"back.out(3)"}},{t:.2f});')
        else:
            add(f'tl.to("{sel}",{{opacity:0,scale:.5,duration:.2,ease:"power2.in"}},{t:.2f});')

    add('tl.set("#birdpos",{x:640,y:2000,scale:.9},0);tl.set(".lid",{scaleY:0},0);tl.set("#wipe",{scale:0},0);')
    add('tl.set("#sweat,#mag,.bub,.bsp",{opacity:0,scale:.5},0);')
    # idle breathing all the way through
    add(f'tl.to("#bbreath",{{scaleY:1.025,scaleX:.985,duration:.8,ease:"sine.inOut",yoyo:true,repeat:{int(DUR / .8) - 1}}},0);')
    for t in (2.6, 6.2, 9.0, 13.2, 16.6, 20.6, 25.4, 28.8, 32.4):
        blink(t)
    # 1 hook: pops up from below, rides the spike
    mv(.25, 640, 1040, .9, .55, "back.out(1.6)")
    hop(1.3, 90)
    show(".bsp", 1.4)
    show(".bsp", 2.6, False)
    # 2 why: lands, tilts head, "?" bubble
    mv(3.4, 700, 1010, .85, .4)
    add('tl.to("#bwig",{rotation:-12,duration:.35,ease:"back.out(2)"},3.75);')
    show(".bq", 3.9)
    show(".bq", 5.5, False)
    add('tl.to("#bwig",{rotation:0,duration:.25},5.55);')
    # 3 next: droops, sweat
    add('tl.to("#bwig",{scaleY:.9,scaleX:1.06,duration:.3,ease:"power2.out"},6.9);')
    show("#sweat", 7.0)
    add('tl.to("#sweat",{y:40,duration:.9,ease:"power1.in"},7.1);')
    show("#sweat", 8.1, False)
    add('tl.to("#bwig",{scaleY:1,scaleX:1,duration:.25},8.1);')
    # 4 numbers: shrug
    mv(8.1, 760, 1060, .75, .4)
    wiggle(9.4, 3, 9)
    # 5 read: magnifier, scans the ticks card
    mv(10.45, 800, 1130, .72, .5)
    show("#mag", 10.9)
    add('tl.to("#mag",{x:-60,y:-30,rotation:-14,duration:.5,ease:"sine.inOut",yoyo:true,repeat:4},11.2);')
    show("#mag", 13.85, False)
    # 6 score: perched beside the black card, cheers on 82
    mv(13.9, 800, 1130, .7, .45)
    hop(15.4, 110)
    show(".bsp", 15.45)
    add('tl.to(".bsp",{rotation:180,duration:1.2,ease:"none"},15.45);')
    show(".bsp", 16.9, False)
    # 7 analyse: small, left of the timeline, rides the playhead down
    mv(17.05, 760, 1180, .6, .45)
    mv(19.85, -60, 330, .42, .4)
    add('tl.to("#birdpos",{y:960,duration:1.05,ease:"power1.inOut"},20.25);')
    # 8 twist: magnifier on the 0:34 row, "!" then follows it to the top
    mv(21.35, -60, 822, .45, .4)
    show("#mag", 21.6)
    add('tl.to("#mag",{x:40,duration:.4,ease:"sine.inOut",yoyo:true,repeat:3},21.8);')
    show(".bx", 23.4)
    hop(23.4, 80)
    show("#mag", 24.3, False)
    show(".bx", 24.5, False)
    mv(24.7, -60, 372, .45, .55, "power3.inOut")
    # 9 reasons: stands on the guesses card, hops to the reasons card
    mv(26.3, 150, 332, .5, .45)
    add('tl.to("#birdpos",{x:700,duration:.6,ease:"power2.inOut"},27.0);')
    add('tl.to("#birdpos",{y:200,duration:.3,ease:"power2.out",yoyo:true,repeat:1},27.0);')
    add('tl.to("#birdpos",{y:282,duration:.15,ease:"power2.out"},27.62);')
    hop(28.4, 70)
    # 10 cta: thought bubble, points, waves goodbye
    mv(29.4, 730, 1080, .7, .45)
    show(".bc", 29.9)
    wiggle(30.4, 2, 6)
    show(".bc", 32.0, False)
    mv(32.1, 390, 780, 1.1, .5, "back.out(1.4)")
    wiggle(32.6, 3, 7)
    # shadow follows the scale, lighter when the bird is in the air
    add('tl.set("#bshadow",{opacity:.0},0);tl.to("#bshadow",{opacity:1,duration:.3},.6);')


# ------------------------------------------------------------------ scene timelines
def timeline():
    a = S["hook"][0]
    # 1 hook
    hl_in("hook", .05)
    pop(".ph-a", .15, "y:260,opacity:0,rotation:-8,scale:.8", .55)
    counter(".cnt-a", 0, 126000, .4, 2.6, "comma", "expo.out")
    pop(".chart", .55, "x:200,opacity:0,scale:.8", .5)
    add(f'tl.fromTo(".spk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.1,ease:"power3.in"}},.75);')
    pop(".spkdot", 1.8, "scale:0,opacity:0", .3)
    pop(".c85", 1.4, "scale:.3,opacity:0,rotation:-10", .45, "back.out(3)")
    add('document.querySelectorAll(".bst").forEach((e,i)=>{tl.fromTo(e,{x:0,y:0,opacity:0,scale:.3},{x:+e.dataset.x,'
        'y:+e.dataset.y,opacity:1,scale:1,rotation:+e.dataset.r,duration:.9,ease:"power3.out"},1.35+i*.03);'
        'tl.to(e,{opacity:0,duration:.4},2.4+i*.03);});')
    add('tl.fromTo("#sc-hook .ghost",{scale:.8,opacity:0},{scale:1,opacity:1,duration:1.2,ease:"power2.out"},0);')
    add('tl.to("#cam",{scale:1.06,duration:.25,ease:"power2.out",yoyo:true,repeat:1},1.33);')
    # 2 why (same clip)
    out(".hl-hook", 3.4)
    hl_in("why", 3.6)
    add('tl.to(".ph-a, .chart",{filter:"grayscale(1) brightness(1.05)",opacity:.55,duration:.4},3.6);')
    add('tl.to("#sc-hook .ghost:not(.gq)",{opacity:0,duration:.3},3.5);')
    add('tl.fromTo(".gq",{scale:.6,opacity:0},{scale:1,opacity:1,duration:.6,ease:"back.out(2)"},3.7);')
    # 3 next
    hl_in("next", S["next"][0] + .05)
    pop(".mini", 5.7, "x:-200,opacity:0,scale:.8", .45)
    pop(".ph-b", 5.85, "y:300,opacity:0,rotation:6,scale:.8", .5)
    counter(".cnt-b", 0, 3000, 6.0, 1.6, "k", "power1.out")
    pop(".lowk", 7.2, "scale:.3,opacity:0", .4, "back.out(3)")
    add('tl.to(".ph-b",{x:-6,duration:.05,yoyo:true,repeat:5},7.4);')
    # 4 numbers
    out(".hl-next", 8.05)
    out(".mini, .ph-b, .lowk", 8.1, "opacity:0,scale:.85")
    hl_in("nums", 8.25)
    add('tl.fromTo(".tile",{opacity:0,scale:.4,rotation:(i)=>[-12,8,-6,10,-9,7][i]},{opacity:1,scale:1,rotation:(i)=>'
        '[-4,3,-2,4,-3,2][i],duration:.4,stagger:.07,ease:"back.out(2)"},8.3);')
    add('tl.to(".grid6",{x:8,duration:.05,yoyo:true,repeat:7},9.0);')
    add('tl.to(".grid6",{filter:"blur(14px)",opacity:.25,scale:.94,duration:.5,ease:"power2.in"},9.5);')
    # 5 read
    t = S["read"][0]
    add(f'tl.fromTo("#wipe",{{scale:0}},{{scale:1,duration:.38,ease:"power3.in"}},{t - .35:.2f});')
    add(f'tl.to("#wipe",{{opacity:0,duration:.3}},{t + .05:.2f});tl.set("#wipe",{{scale:0,opacity:1}},{t + .4:.2f});')
    pop(".crhead", t + .05, "y:-40,opacity:0", .4)
    pop(".reading", t + .25, "opacity:0,y:20", .35)
    pop(".give", t + .35, "opacity:0,y:40,scale:.9", .5)
    pop(".pub", t + .7, "opacity:0,y:20", .35)
    pop(".rbar", t + .6, "opacity:0,scaleX:.6", .3)
    add(f'tl.fromTo(".rfill",{{scaleX:0}},{{scaleX:1,duration:2.9,ease:"power1.inOut"}},{t + .7:.2f});')
    pop(".ticks", t + .85, "y:120,opacity:0,scale:.9", .45)
    for i, tt in enumerate((11.5, 12.15, 12.95)):
        pop(f".trow.r{i + 1}", tt, "x:-60,opacity:0", .35)
        add(f'tl.fromTo(".trow.r{i + 1} .tk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.3}},{tt + .1:.2f});')
    pop(".stopw", 12.8, "scale:.3,opacity:0,rotation:-15", .4, "back.out(3)")
    counter(".cnt-s", 0, 20, 12.82, .7, "int", "power1.out")
    add('tl.fromTo("#sc-read .ghost",{opacity:0,scale:.8},{opacity:1,scale:1,duration:1,ease:"power2.out"},12.8);')
    # 6 score
    t = S["score"][0]
    hl_in("score", t + .05)
    add(f'tl.fromTo(".th",{{opacity:0,y:200,rotation:(i)=>(i%2?8:-8),scale:.6}},{{opacity:1,y:0,rotation:(i)=>(i%2?2:-2),'
        f'scale:1,duration:.4,stagger:.08,ease:"back.out(1.8)"}},{t + .15:.2f});')
    add(f'tl.to(".th",{{x:(i)=>[300,10,-280,300,10,-280][i],y:(i)=>(i<3?260:-80),scale:.15,opacity:0,rotation:0,'
        f'duration:.45,stagger:.03,ease:"power3.in"}},{t + 1.0:.2f});')
    pop(".scard", t + 1.3, "y:300,opacity:0,scale:.85", .5)
    counter(".cnt-sc", 0, 82, 15.37, 1.0, "int", "expo.out")
    add(f'tl.fromTo(".rg",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:.18,duration:1.0,ease:"expo.out"}},15.37);')
    add('tl.to("#cam",{scale:1.05,duration:.22,ease:"power2.out",yoyo:true,repeat:1},15.4);')
    pop(".sl2", 16.0, "opacity:0,y:20", .3)
    pop(".sins", 16.15, "opacity:0,y:30", .4)
    # 7 analyse
    t = S["analyse"][0]
    hl_in("analyse", t + .05)
    pop(".ubub", t + .2, "x:200,opacity:0,scale:.85", .45)
    pop(".onit", t + .7, "y:100,opacity:0,scale:.9", .45)
    for i, tt in enumerate((18.0, 18.5, 19.0)):
        pop(f".orow.o{i}", tt, "x:-40,opacity:0", .3)
        add(f'tl.fromTo(".orow.o{i} .tk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.25}},{tt + .15:.2f});')
    pop(".scanph", 18.2, "scale:.5,opacity:0,rotation:8", .4)
    add('tl.fromTo(".scanl",{y:0},{y:300,duration:.8,ease:"none",repeat:1},18.5);')
    out(".ubub, .onit, .scanph", 19.75, "opacity:0,y:-60,scale:.9", .3)
    pop(".tl-a", 19.85, "y:200,opacity:0,scale:.9", .45)
    add('tl.fromTo(".tl-a .tline",{scaleY:0},{scaleY:1,duration:1.1,ease:"power1.inOut"},20.0);')
    add('tl.fromTo(".tl-a .tr",{opacity:0,x:60},{opacity:1,x:0,duration:.3,stagger:.2,ease:"back.out(2)"},20.0);')
    # 8 twist
    t = S["twist"][0]
    add(f'tl.to("#dark",{{opacity:1,duration:.4,ease:"power2.out"}},{t - .1:.2f});')
    add(f'tl.to("#dark",{{opacity:0,duration:.35,ease:"power2.in"}},{S["twist"][1] - .1:.2f});')
    add(f'tl.set("#hud",{{color:"#ffffff"}},{t:.2f});tl.set("#hud",{{color:"{INK}"}},{S["twist"][1]:.2f});')
    add(f'tl.set(".hudig path, .hudig rect, .hudig circle",{{attr:{{stroke:"#ffffff"}}}},{t:.2f});'
        f'tl.set(".hudig path, .hudig rect, .hudig circle",{{attr:{{stroke:"{INK}"}}}},{S["twist"][1]:.2f});')
    hl_in("twist", t + .3)
    add(f'tl.to(".tl-b .tr:not(.tr3)",{{opacity:.28,duration:.4}},{t + .5:.2f});')
    add(f'tl.to(".tl-b .tr3",{{scale:1.06,backgroundColor:"#FEF0F4",boxShadow:"0 0 0 4px {PINK}, 0 20px 60px rgba(238,104,139,.55)",'
        f'duration:.45,ease:"back.out(2)"}},23.3);')
    pop(".besth", 23.45, "scale:.3,opacity:0,rotation:-12", .4, "back.out(3)")
    add('tl.to("#cam",{scale:1.07,duration:.25,ease:"power2.out",yoyo:true,repeat:1},23.4);')
    # the 0:34 row lifts to the 0:00 slot; the others slide down one place
    add('tl.to(".tl-b .tr3",{y:-450,duration:.6,ease:"power3.inOut"},24.7);')
    add('tl.to(".tl-b .tr0, .tl-b .tr1, .tl-b .tr2",{y:150,duration:.6,ease:"power3.inOut"},24.7);')
    add('tl.to(".besth",{y:-450,duration:.6,ease:"power3.inOut"},24.7);')
    add('tl.to(".tl-b .tt3",{opacity:0,duration:.15},24.9);')
    add('(()=>{const o={v:0};tl.to(o,{v:1,duration:.01,onUpdate:()=>{document.querySelector(".tl-b .tt3").textContent='
        'o.v>.5?"0:00–0:07":"0:34–0:41";}},25.05);})();')
    add('tl.to(".tl-b .tt3",{opacity:1,duration:.2},25.06);')
    # 9 reasons
    t = S["reasons"][0]
    hl_in("reasons", t + .05)
    pop(".gcard", t + .15, "x:-200,opacity:0,rotation:-8,scale:.85", .45)
    pop(".rcard", t + .35, "x:200,opacity:0,rotation:8,scale:.85", .45)
    for i, tt in enumerate((26.9, 27.35, 27.8)):
        pop(f".rr{i}", tt, "x:40,opacity:0", .3)
        add(f'tl.fromTo(".rr{i} .tk",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.25}},{tt + .1:.2f});')
    add('tl.fromTo(".strike",{scaleX:0},{scaleX:1,duration:.3,ease:"power3.out"},28.4);')
    add('tl.to(".gcard",{opacity:.45,filter:"grayscale(1)",duration:.3},28.5);')
    add('tl.to(".rcard",{scale:1.04,duration:.2,yoyo:true,repeat:1},28.5);')
    # 10 cta
    t = S["cta"][0]
    pop(".cmt", t + .05, "y:-80,opacity:0,rotation:-12,scale:.7", .4)
    pop(".kw", 29.75, "scale:2.2,opacity:0,rotation:6", .45, "back.out(1.8)")
    add('tl.to("#cam",{scale:1.06,duration:.2,ease:"power2.out",yoyo:true,repeat:1},29.8);')
    add('tl.fromTo(".kc",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.35,stagger:.08,ease:"back.out(2)"},29.9);')
    add('tl.to(".kc",{y:(i)=>(i%2?-30:30),x:(i)=>(i%3?14:-14),duration:3.2,ease:"sine.inOut"},30.2);')
    pop(".cbox", 30.0, "y:120,opacity:0,scale:.9", .45)
    word = "CREEDOM"
    add(f'(()=>{{const o={{v:0}};tl.to(o,{{v:{len(word)},duration:{len(word) * .1:.2f},ease:"none",onUpdate:()=>{{'
        f'document.querySelector(".typed").textContent="{word}".slice(0,Math.floor(o.v+.001));}}}},30.25);}})();')
    add(f'tl.to(".caret",{{opacity:0,duration:.01,yoyo:true,repeat:{int((DUR - 30.2) / .5) * 2 - 1},repeatDelay:.49}},30.2);')
    add('tl.to(".send",{scale:1.18,duration:.15,yoyo:true,repeat:3},31.0);')
    pop(".dm", 31.25, "opacity:0,y:20", .3)
    out(".cmt, .kw, .kc, .cbox", 32.05, "opacity:0,y:-40", .3)
    pop(".endig", 32.25, "scale:.4,opacity:0", .5, "back.out(2.4)")
    # always on
    add(f'tl.fromTo(".pfill",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none"}},0);')
    add(f'tl.fromTo(".gly",{{y:0}},{{y:-160,duration:{DUR},ease:"none"}},0);')
    caption_tl()
    bird_tl()
    return "\n".join(T)


def glyphs():
    r = random.Random(2)
    g = ["▶", "♥", "%", "0:00", "{ }", "→", "✦", "#", "82", "0:34"]
    return "".join(f'<div class="gly" style="left:{r.uniform(20, 1000):.0f}px;top:{r.uniform(120, 1800):.0f}px;'
                   f'font-size:{r.uniform(28, 60):.0f}px">{r.choice(g)}</div>' for _ in range(22))


CSS = """
@font-face { font-family: "Fraunces"; font-weight: 100 900; src: url("assets/fonts/fraunces.ttf"); }
@font-face { font-family: "Fraunces"; font-style: italic; font-weight: 100 900; src: url("assets/fonts/fraunces-italic.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 100 800; src: url("assets/fonts/jbmono.ttf"); }
:root { --pink: #E2557D; --pinkt: #D9467A; --ink: #0B0B0B; --paper: #F6F6F4; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--paper); }
body { font-family: "Manrope", sans-serif; color: var(--ink); }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--paper); }
.clip { position: absolute; inset: 0; }
#cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
.mono { font: 600 24px "JBMono"; letter-spacing: 5px; color: #6b6b66; }
/* background */
#paper { position: absolute; inset: 0; background: var(--paper);
  background-image: radial-gradient(rgba(11,11,11,.09) 1.6px, transparent 1.7px); background-size: 34px 34px; }
.gly { position: absolute; font-family: "JBMono"; color: rgba(11,11,11,.07); }
#dark { position: absolute; inset: 0; opacity: 0;
  background: radial-gradient(90% 60% at 50% 45%, #3a1d26 0%, #1b0f14 55%, #0d0709 100%); }
.ghost { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font: italic 600 520px/1 "Fraunces";
  color: rgba(11,11,11,.045); letter-spacing: -20px; white-space: nowrap; }
.ghost.gw { color: rgba(255,255,255,.05); font-size: 400px; }
/* hud */
#hud { color: var(--ink); }
.hudl { position: absolute; left: 56px; top: 70px; font: 700 26px "JBMono"; letter-spacing: 4px; }
.hudl b { color: var(--pinkt); }
.pill { position: absolute; right: 56px; top: 56px; width: 300px; height: 56px; border-radius: 28px; background: rgba(255,255,255,.85);
  box-shadow: 0 6px 24px rgba(0,0,0,.08); display: flex; align-items: center; gap: 14px; padding: 0 18px; }
.pill img { width: 36px; height: 38px; }
.ptrack { flex: 1; height: 10px; border-radius: 5px; background: #ebe8e4; overflow: hidden; }
.pfill { width: 100%; height: 100%; background: var(--pink); transform-origin: 0 50%; }
.hudig { position: absolute; right: 62px; top: 150px; text-align: center; font: 700 20px "Manrope"; letter-spacing: 1px; }
/* headline */
.hl { position: absolute; left: 0; width: 1080px; text-align: center; z-index: 6; }
.l1 { font: 800 84px/1.05 "Manrope"; letter-spacing: -3px; }
.l2 { font: italic 600 112px/1.05 "Fraunces"; letter-spacing: -3px; color: var(--pinkt); }
.hw, .acc { display: inline-block; }
.dark .l1, .dark .hl { color: #fff; }
/* cards */
.card { background: #fff; border-radius: 34px; box-shadow: 0 24px 60px rgba(11,11,11,.12), 0 2px 0 rgba(11,11,11,.04); }
.chip { position: absolute; border-radius: 40px; font: 800 34px "Manrope"; padding: 14px 28px; white-space: nowrap; }
.pinkchip { background: var(--pink); color: #fff; }
.redchip { background: #fde8e8; color: #c43c3c; }
/* hook */
.phone { position: absolute; left: 110px; top: 520px; width: 380px; height: 640px; border-radius: 44px; overflow: hidden;
  background: #111; box-shadow: 0 30px 70px rgba(11,11,11,.25); border: 8px solid #111; }
.phone img { width: 100%; height: 100%; object-fit: cover; }
.pbar { position: absolute; left: 0; right: 0; bottom: 0; height: 120px; display: flex; align-items: center; gap: 12px;
  padding: 0 24px; background: linear-gradient(transparent, rgba(0,0,0,.85)); color: #fff; font: 800 46px "Manrope"; }
.plab { font: 600 24px "Manrope"; opacity: .8; }
.chart { position: absolute; left: 540px; top: 560px; width: 440px; height: 420px; padding: 34px 30px; }
.chart .mono { font-size: 20px; letter-spacing: 3px; white-space: nowrap; }
.chart svg { margin-top: 26px; }
.c85 { left: 60px; top: 330px; font-size: 32px; }
.burst { position: absolute; left: 300px; top: 820px; }
.bst { position: absolute; left: 0; top: 0; }
.gq { color: rgba(238,104,139,.12); top: 520px; font-size: 760px; }
/* next */
.mini { position: absolute; left: 70px; top: 560px; width: 210px; padding: 14px; transform: rotate(-4deg); }
.mini img { width: 100%; border-radius: 18px; display: block; }
.mini .mono { margin-top: 10px; font-size: 20px; letter-spacing: 2px; color: var(--pinkt); }
.ph-b { left: 330px; top: 530px; }
.lowk { left: 70px; top: 960px; }
.grid6 { position: absolute; left: 90px; top: 520px; width: 900px; display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
.tile { height: 170px; padding: 26px 30px; }
.tile .mono { font-size: 22px; }
.tv { font: italic 700 60px "Fraunces"; margin-top: 4px; }
.tb { height: 10px; border-radius: 5px; background: #eee; margin-top: 10px; }
/* read */
.crhead { position: absolute; left: 0; width: 1080px; top: 190px; display: flex; justify-content: center; align-items: center; gap: 18px;
  font: 600 72px "Fraunces"; }
.crhead img { width: 92px; height: 98px; }
.reading { position: absolute; left: 0; width: 1080px; top: 380px; text-align: center; font-size: 30px; letter-spacing: 8px; color: #555; }
.give { position: absolute; left: 0; width: 1080px; top: 430px; text-align: center; font: 700 96px "Fraunces"; letter-spacing: -2px; }
.give i { color: var(--pinkt); }
.pub { position: absolute; left: 0; width: 1080px; top: 568px; text-align: center; font: 500 34px "Manrope"; color: #666; }
.rbar { position: absolute; left: 120px; top: 650px; width: 840px; height: 12px; border-radius: 6px; background: #ebe8e4; overflow: hidden; }
.rfill { width: 100%; height: 100%; background: var(--pink); transform-origin: 0 50%; }
.ticks { position: absolute; left: 100px; top: 730px; width: 880px; padding: 34px 40px; }
.trow { display: flex; align-items: center; gap: 24px; font: 500 40px "Manrope"; color: #444; padding: 20px 0; }
.stopw { left: 720px; top: 1040px; background: var(--ink); color: #fff; }
/* score */
.th { position: absolute; width: 230px; height: 320px; border-radius: 24px; overflow: hidden; box-shadow: 0 18px 40px rgba(11,11,11,.18); }
.th img { width: 100%; height: 100%; object-fit: cover; }
.scard { position: absolute; left: 90px; top: 450px; width: 900px; height: 640px; border-radius: 44px; background: var(--ink); color: #fff;
  padding: 50px 56px; box-shadow: 0 40px 80px rgba(11,11,11,.3); }
.scard .mono { color: #b9b9b2; }
.snum { font: 600 230px/1 "Fraunces"; margin-top: 10px; }
.snum small { font-size: 74px; color: #9a9a92; margin-left: 10px; }
.ring { position: absolute; right: 56px; top: 90px; }
.sl2 { color: var(--pink) !important; margin-top: 34px; }
.sins { font: 600 50px/1.2 "Fraunces"; margin-top: 14px; }
.sins i { color: #ffb3c6; }
/* analyse */
.ubub { position: absolute; right: 70px; top: 470px; width: 760px; background: var(--ink); color: #fff; border-radius: 40px 40px 10px 40px;
  padding: 34px 40px; font: 600 42px/1.3 "Manrope"; }
.onit { position: absolute; left: 70px; top: 760px; width: 760px; padding: 34px 40px; }
.oh { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.oh img { width: 44px; height: 46px; }
.orow { display: flex; align-items: center; gap: 20px; font: 500 34px "Manrope"; color: #444; padding: 12px 0; }
.scanph { position: absolute; left: 850px; top: 780px; width: 180px; height: 290px; border-radius: 22px; overflow: hidden;
  box-shadow: 0 18px 40px rgba(11,11,11,.2); }
.scanph img { width: 100%; height: 100%; object-fit: cover; }
.scanl { position: absolute; left: 0; right: 0; top: -6px; height: 6px; background: var(--pink); box-shadow: 0 0 20px var(--pink); }
.tlc { position: absolute; left: 190px; top: 440px; width: 840px; height: 880px; padding: 34px 40px; }
.tlh { display: flex; justify-content: space-between; align-items: center; }
.sc42 { font: 700 32px "Manrope"; color: var(--ink); }
.sc42 small { color: #888; font-size: 24px; }
.tline { position: absolute; left: 62px; top: 140px; width: 4px; height: 640px; background: #e4e1dc; transform-origin: 50% 0; }
.tr { position: absolute; left: 30px; width: 780px; height: 120px; border-radius: 26px; display: flex; align-items: center; gap: 22px;
  padding: 0 30px; background: #fff; }
.dot { width: 26px; height: 26px; border-radius: 50%; flex: none; }
.tr b { font: 800 34px "Manrope"; letter-spacing: -1px; white-space: nowrap; }
.tt { font: 500 24px "JBMono"; color: #888; white-space: nowrap; }
.ts { margin-left: auto; font: 700 36px "Fraunces"; color: #555; }
.besth { left: 640px; top: 978px; z-index: 5; font-size: 26px; padding: 8px 20px; }
/* reasons */
.gcard { position: absolute; left: 70px; top: 640px; width: 440px; height: 520px; padding: 40px; transform: rotate(-3deg); }
.dice { font-size: 110px; margin-top: 50px; text-align: center; }
.gq2 { font: italic 700 90px "Fraunces"; color: #bbb; text-align: center; margin-top: 30px; }
.strike { position: absolute; left: 30px; top: 250px; width: 380px; height: 14px; border-radius: 7px; background: var(--pink);
  transform: rotate(-14deg); transform-origin: 0 50%; }
.rcard { position: absolute; left: 540px; top: 600px; width: 480px; height: 600px; padding: 40px 34px; transform: rotate(2deg);
  box-shadow: 0 0 0 4px var(--pink), 0 30px 70px rgba(238,104,139,.3); }
.pk { color: var(--pinkt) !important; font-size: 21px; letter-spacing: 3px; }
.rr { display: flex; align-items: flex-start; gap: 16px; font: 700 36px/1.25 "Manrope"; margin-top: 34px; }
.rr svg { flex: none; margin-top: 2px; }
/* cta */
.cmt { position: absolute; left: 270px; top: 300px; display: flex; align-items: center; gap: 18px; background: var(--ink); color: #fff;
  font: 800 70px "Manrope"; letter-spacing: -1px; padding: 22px 46px; border-radius: 26px; transform: rotate(-3deg); }
.kw { position: absolute; left: 90px; top: 450px; width: 900px; text-align: center; background: var(--pink); color: #fff;
  font: 800 150px "Manrope"; letter-spacing: -5px; border-radius: 40px; padding: 18px 0; box-shadow: 0 30px 70px rgba(238,104,139,.45); }
.kc { position: absolute; background: #fff; border-radius: 30px; padding: 10px 22px; font: 700 26px "Manrope";
  box-shadow: 0 10px 26px rgba(11,11,11,.1); color: #444; }
.cbox { position: absolute; left: 90px; top: 760px; width: 900px; height: 300px; padding: 36px 40px; }
.cin { margin-top: 20px; width: 680px; height: 104px; border-radius: 22px; border: 4px solid var(--pink); display: flex; align-items: center;
  padding: 0 30px; font: 700 64px "JBMono"; letter-spacing: 6px; }
.caret { width: 5px; height: 64px; background: var(--ink); margin-left: 6px; }
.send { position: absolute; right: 40px; top: 100px; width: 120px; height: 104px; border-radius: 22px; background: var(--ink);
  display: flex; align-items: center; justify-content: center; }
.dm { margin-top: 22px; font: 600 30px "Manrope"; color: var(--pinkt); }
.endig { position: absolute; left: 0; width: 1080px; top: 420px; text-align: center; font: 800 54px "Manrope"; letter-spacing: 2px; }
.endig div { margin-top: 18px; }
/* bird */
#birdlayer { z-index: 20; }
#birdpos { position: absolute; left: 0; top: 0; width: 300px; height: 318px; transform-origin: 50% 100%; }
#bshadow { position: absolute; left: 40px; top: 300px; width: 220px; height: 40px; border-radius: 50%;
  background: radial-gradient(closest-side, rgba(243,67,162,.35), rgba(243,67,162,0)); }
#bwig { position: absolute; inset: 0; transform-origin: 50% 100%; }
#bbreath { position: absolute; inset: 0; transform-origin: 50% 100%; }
#bimg { position: absolute; left: 0; top: 0; filter: drop-shadow(0 18px 24px rgba(160,20,90,.25)); }
.lid { position: absolute; background: #f2499f; border-radius: 50%; transform-origin: 50% 0; }
.lidl { left: 70px; top: 70px; width: 76px; height: 72px; }
.lidr { left: 170px; top: 54px; width: 72px; height: 70px; }
#sweat { position: absolute; left: 250px; top: 30px; }
#mag { position: absolute; left: 150px; top: 140px; transform-origin: 30% 30%; }
.bub { position: absolute; left: 190px; top: -130px; background: #fff; border: 4px solid var(--ink); border-radius: 50px;
  display: flex; align-items: center; justify-content: center; font: 800 80px "Manrope"; color: var(--pink); }
.bub .tail { position: absolute; left: 6px; bottom: -48px; }
.bub i { font: 800 52px "JBMono"; font-style: normal; letter-spacing: 2px; }
.bc { left: -200px; top: -150px; }
.bsp { position: absolute; }
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
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-allow-overflow>
        <div id="paper"></div><div id="glys" data-layout-ignore>{glyphs()}</div><div id="dark"></div>
      </div>
      <div id="cam" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-allow-overflow>
        {scenes()}
      </div>
      <div id="hud" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5">
        <div class="hudl"><b>●</b> AI.NXTLVL</div>
        <div class="pill"><img src="assets/img/bird.png" alt=""><div class="ptrack"><div class="pfill"></div></div></div>
        <div class="hudig">{ig_icon(46)}<div>@AI.NXTLVL</div></div>
      </div>
      <div id="birdlayer" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6" data-layout-allow-overflow>{bird_rig()}</div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{captions()}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="8" data-layout-allow-overflow><div id="wipe"></div></div>
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
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
