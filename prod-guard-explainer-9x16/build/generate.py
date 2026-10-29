"""Prod Guard explainer (ai.nxtlvl 2D style): writes index.html and build/cues.json. 1080x1920, 30 fps, about 38 s.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3 AM production-database story, told as an ai.nxtlvl explainer instead of a 3D short: cream paper with a faint
grid, ink type, one coral accent, white UI cards with soft shadows, a giant faint word behind every scene, headlines
with one italic-serif accent word, "STEP 1/3" headers, word-by-word captions with the spoken word on a coral pill, and
the coral pixel mascot reacting on every line. One dark beat for the twist (read-only production). The CTA ends on the
real Prod Guard PDF cover (horror-db-9x16/lead-magnet), the thing the BACKUP DM sends.

Scenes follow the voiceover's eight lines: hook, loss, the copy, step 1 (snapshot hook), step 2 (production block),
step 3 (backup alarm), twist (read-only login), CTA. Every visual event is logged to cues.json["ev"] so build/audio.py
can give it a sound.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
DUR = round(E[-1] + 1.6, 2)

CREAM, GRID, INK, CORAL, CORAL_D = "#F1E9DC", "#E4D9C7", "#1E1B18", "#E8735A", "#B9523D"
GREEN, AMBER, TERM, CARD, CARD_B, RED = "#3FA372", "#F2B33D", "#1B1A1F", "#FFFDF8", "#E2D6C3", "#D9483B"
CORAL_T = "#D45C40"   # coral for text and for pills under white text (3:1 on cream)


def word(li, text, nth=1):
    hits = [w for w in WORDS if w["line"] == li + 1 and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not in line {li + 1}")
    return hits[nth - 1]["s"]


# scene k runs from just before line k to just before line k+1
SC = []
for k in range(len(LINES)):
    a = 0 if k == 0 else round(L[k] - .12, 3)
    z = DUR if k == len(LINES) - 1 else round(L[k + 1] - .12, 3)
    SC.append((a, z))
T = {
    "l": L, "e": E, "end": DUR, "scenes": SC,
    "press": round(word(0, "deleted") - .05, 3), "rows": word(1, "rows"), "gone": word(1, "gone"),
    "backups": word(1, "backups"), "dead": word(1, "dead"), "copy": word(2, "copy"), "heres": word(2, "here"),
    "before": word(3, "before"), "backs": word(3, "backs"), "first": word(3, "first"),
    "destructive": word(4, "destructive"), "prod": word(4, "prod", 2), "refused": word(4, "refused"),
    "alarm": word(5, "alarm"), "fresh": word(5, "backups"),
    "nobody": word(6, "nobody"), "readonly": word(6, "read"), "cant": word(6, "can"), "touch": word(6, "touch"),
    "comment": word(7, "comment"), "backup": word(7, "backup"), "send": word(7, "send"),
}
TWIST = SC[6]
A, EV = [], []


def add(js):
    A.append("      " + js)


def ev(t, kind):
    EV.append([round(t, 3), kind])


HIDE = []


def pop(sel, t, frm="opacity:0,y:30,scale:.9", d=.35, ease="back.out(1.8)"):
    if "opacity:0" in frm and t > .05:
        HIDE.append(sel)
    add(f'tl.fromTo("{sel}",{{{frm}}},{{opacity:1,x:0,y:0,scale:1,rotation:0,duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def to(sel, t, props, d=.3, ease="power2.out"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"{ease}"}},{t:.3f});')


def setp(sel, t, props):
    add(f'tl.set("{sel}",{{{props}}},{t:.3f});')


# ---------------------------------------------------------------- the mascot: a coral pixel creature, 16 x 13 at 14 px
PX = 14
SPRITE = [
    ".......ss.......",
    "......ssss......",
    ".......aa.......",
    "...BBBBBBBBBB...",
    "..BBBBBBBBBBBB..",
    "..BBBBBBBBBBBB..",
    "..BBBBBBBBBBBB..",
    "..BBBBBBBBBBBB..",
    "..BBBBBBBBBBBB..",
    "..BBBBBBBBBBBB..",
    "..DDDDDDDDDDDD..",
    "...LL......LL...",
    "...LL......LL...",
]
COL = {"s": "#F7C6B6", "a": CORAL_D, "B": CORAL, "D": CORAL_D, "L": CORAL_D}


def rects(cells, color, cls=""):
    return "".join(f'<rect x="{c * PX}" y="{r * PX}" width="{PX}" height="{PX}" fill="{color}"/>' for r, c in cells)


def mascot():
    body = []
    for r, row in enumerate(SPRITE):
        for c, ch in enumerate(row):
            if ch in COL:
                body.append(f'<rect x="{c * PX}" y="{r * PX}" width="{PX + .5}" height="{PX + .5}" fill="{COL[ch]}"/>')
    eyes_open = rects([(5, 4), (5, 5), (6, 4), (6, 5), (5, 10), (5, 11), (6, 10), (6, 11)], INK)
    eyes_shut = rects([(6, 4), (6, 5), (6, 10), (6, 11)], INK)
    eyes_happy = rects([(5, 4), (6, 3), (5, 5), (6, 6), (5, 10), (6, 9), (5, 11), (6, 12)], INK)
    eyes_wide = rects([(4, 4), (4, 5), (5, 4), (5, 5), (6, 4), (6, 5), (4, 10), (4, 11), (5, 10), (5, 11), (6, 10), (6, 11)], INK) + \
        rects([(4, 5), (4, 11)], "#fff")
    smile = rects([(8, 6), (8, 9), (9, 7), (9, 8)], INK)
    frown = rects([(9, 6), (9, 9), (8, 7), (8, 8)], INK)
    arm = lambda side: (f'<g class="m-arm" id="m-arm{side}">' +  # noqa: E731
                        rects([(7, 0), (7, 1), (8, 0), (8, 1)] if side == "L" else [(7, 14), (7, 15), (8, 14), (8, 15)], CORAL) + "</g>")
    sweat = rects([(1, 14), (2, 13), (2, 14), (3, 13), (3, 14)], "#7CC4F2")
    return (f'<div id="mascot"><svg viewBox="0 0 {16 * PX} {13 * PX}" width="{16 * PX}" height="{13 * PX}" shape-rendering="crispEdges">'
            f'<g id="m-body">{"".join(body)}{arm("L")}{arm("R")}'
            f'<g id="m-eo">{eyes_open}</g><g id="m-es" style="opacity:0">{eyes_shut}</g><g id="m-eh" style="opacity:0">{eyes_happy}</g>'
            f'<g id="m-ew" style="opacity:0">{eyes_wide}</g><g id="m-sm" style="opacity:0">{smile}</g><g id="m-fr" style="opacity:0">{frown}</g>'
            f'<g id="m-sw" style="opacity:0">{sweat}</g></g></svg><div id="m-shadow"></div></div>')


FACES = {"open": "m-eo", "shut": "m-es", "happy": "m-eh", "wide": "m-ew"}


def face(t, eyes="open", mouth=None, sweat=False):
    for k, i in FACES.items():
        setp(f"#{i}", t, f"opacity:{1 if k == eyes else 0}")
    setp("#m-sm", t, f"opacity:{1 if mouth == 'smile' else 0}")
    setp("#m-fr", t, f"opacity:{1 if mouth == 'frown' else 0}")
    setp("#m-sw", t, f"opacity:{1 if sweat else 0}")


def hop(t, x, y, s=1.0, d=.42):
    """The mascot hops to (x, y): an arc up and a squash on landing."""
    add(f'tl.to("#mascot",{{x:{x},duration:{d},ease:"power1.inOut"}},{t:.3f});')
    add(f'tl.to("#mascot",{{y:"-=90",duration:{d / 2},ease:"power2.out"}},{t:.3f});')
    add(f'tl.to("#mascot",{{y:{y},duration:{d / 2},ease:"power2.in"}},{t + d / 2:.3f});')
    add(f'tl.to("#mascot",{{scale:{s},duration:{d},ease:"power1.inOut"}},{t:.3f});')
    add(f'tl.fromTo("#m-body",{{scaleY:.78,scaleX:1.15}},{{scaleY:1,scaleX:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{t + d:.3f});')
    ev(t, "hop"); ev(t + d, "land")


def arms(t, l=0, r=0, d=.2):
    add(f'tl.to("#m-armL",{{rotation:{l},duration:{d},ease:"back.out(2)"}},{t:.3f});')
    add(f'tl.to("#m-armR",{{rotation:{r},duration:{d},ease:"back.out(2)"}},{t:.3f});')


def wave(t, n=4):
    add(f'tl.to("#m-armR",{{rotation:-70,duration:.16,yoyo:true,repeat:{n * 2 - 1},ease:"sine.inOut"}},{t:.3f});')


def shake(sel, t, n=6, amp=8, d=.05):
    add(f'tl.to("{sel}",{{x:"+={amp}",duration:{d},yoyo:true,repeat:{n},ease:"sine.inOut"}},{t:.3f});')


# ---------------------------------------------------------------- building blocks
def hl(l1, l2, kicker=None, step=0):
    k = ""
    if kicker:
        segs = "".join(f'<i class="{"on" if i < step else ""}"></i>' for i in range(3))
        k = f'<div class="kick"><span>{kicker}</span><b class="segs">{segs}</b></div>'
    w1 = " ".join(f'<span class="hw">{w}</span>' for w in l1.split())
    return f'<div class="hl">{k}<div class="l1">{w1}</div><div class="l2"><span class="acc">{l2}</span></div></div>'


def hl_tl(sid, t, kick=False):
    if kick:
        pop(f"#{sid} .kick", t + .02, "opacity:0,x:-30", .3, "power3.out")
    if t > .05:
        HIDE.append(f"#{sid} .hw")
    add(f'tl.fromTo("#{sid} .hw",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.32,stagger:.06,ease:"back.out(2)",immediateRender:false}},{t + .05:.3f});')
    pop(f"#{sid} .acc", t + .3, "opacity:0,scale:.6,rotation:-6", .45, "back.out(2.4)")
    ev(t + .05, "pop"); ev(t + .3, "accent")


def db_svg(label, color=INK, fill=CARD, w=200, h=240, tag=None, tagc=RED):
    rx, ry = w / 2 - 6, 26
    cy = [ry + 6, h / 2, h - ry - 6]
    bands = "".join(f'<path d="M6 {y} A{rx} {ry} 0 0 0 {w - 6} {y}" fill="none" stroke="{color}" stroke-width="6"/>' for y in cy[1:])
    t = (f'<div class="dbtag" style="background:{tagc}">{tag}</div>' if tag else "")
    return (f'<div class="db" style="width:{w}px">{t}<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<path d="M6 {cy[0]} L6 {cy[2]} A{rx} {ry} 0 0 0 {w - 6} {cy[2]} L{w - 6} {cy[0]}" fill="{fill}" stroke="{color}" stroke-width="6"/>'
            f'<ellipse cx="{w / 2}" cy="{cy[0]}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{color}" stroke-width="6"/>{bands}</svg>'
            f'<div class="dblabel">{label}</div></div>')


def check_svg(c=GREEN, s=44):
    return (f'<svg viewBox="0 0 44 44" width="{s}" height="{s}"><circle cx="22" cy="22" r="22" fill="{c}"/>'
            f'<path d="M12 23 L19 30 L32 15" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ---------------------------------------------------------------- scenes
def scene(k, sid, inner):
    a, z = SC[k]
    return (f'<div id="{sid}" class="clip scene" data-start="{a}" data-duration="{round(z - a, 3)}" '
            f'data-track-index="{3 + k % 2}" data-layout-allow-overflow><div class="inner">{inner}</div></div>')


def scene_tl(k, sid):
    a, z = SC[k]
    if k:
        add(f'tl.fromTo("#{sid} .inner",{{x:300,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"power3.out",immediateRender:false}},{a:.3f});')
        ev(a, "whoosh")
    if k < len(SC) - 1:
        add(f'tl.to("#{sid} .inner",{{x:-260,opacity:0,duration:.16,ease:"power2.in"}},{z - .16:.3f});')


GIANT = [("3 AM", 0), ("1.2M", 1), ("MARCH", 1), ("COPY", 2), ("HOOK", 3), ("PROD", 4), ("ALARM", 5), ("LOCKED", 6), ("BACKUP", 7)]


def giant_tl():
    html = []
    times = {0: [SC[0][0]], 1: [SC[1][0], T["backups"] - .1], 2: [SC[2][0]], 3: [SC[3][0]], 4: [SC[4][0]], 5: [SC[5][0]], 6: [SC[6][0]], 7: [SC[7][0]]}
    used = {}
    for i, (w, k) in enumerate(GIANT):
        j = used.get(k, 0); used[k] = j + 1
        a = times[k][j]
        z = times[k][j + 1] if j + 1 < len(times[k]) else SC[k][1]
        html.append(f'<div class="giant" id="g{i}">{w}</div>')
        add(f'tl.fromTo("#g{i}",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:.5,ease:"power3.out",immediateRender:false}},{a:.3f});')
        add(f'tl.to("#g{i}",{{opacity:0,duration:.15}},{z - .15:.3f});')
    return "".join(html)


# S1 hook: the terminal, the Enter key, the stamp
CMD = "DROP DATABASE app;"
S1 = (hl("He just deleted", "production.") +
      '<div class="term" id="term"><div class="bar"><i></i><i></i><i></i><span>zsh · prod-db-01</span><b class="ptag">PRODUCTION</b></div>'
      '<div class="tbody"><div class="tl dim">$ psql -h prod-db-01</div><div class="tl">prod=# ' +
      "".join(f'<span class="ch" id="ch{i}">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(CMD)) +
      '<span class="cur" id="cur"></span></div><div class="tl red" id="tout">DROP DATABASE</div></div>'
      '<div class="stamp" id="stamp1">DELETED</div></div>'
      '<div class="key" id="key"><span>ENTER</span><svg viewBox="0 0 40 30" width="44" height="33"><path d="M34 4 V16 H8 M14 9 L7 16 L14 23" stroke="#1E1B18" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')


def s1_tl():
    a = SC[0][0]
    add(f'tl.fromTo("#s1 .acc",{{scale:1.12}},{{scale:1,duration:.5,ease:"back.out(2)",immediateRender:false}},0);')
    t0, t1 = a + .35, T["press"] - .55
    for i in range(len(CMD)):
        t = t0 + (t1 - t0) * i / len(CMD)
        setp(f"#ch{i}", t, "opacity:1")
        if i % 3 == 0:
            ev(t, "type")
    add(f'tl.fromTo("#cur",{{opacity:1}},{{opacity:0,duration:.25,yoyo:true,repeat:{int((T["press"] - a) / .25)},ease:"steps(1)",immediateRender:false}},{a:.3f});')
    p = T["press"]
    add(f'tl.to("#key",{{y:14,boxShadow:"0 2px 0 #B8AC98",duration:.07,ease:"power2.in"}},{p:.3f});')
    add(f'tl.to("#key",{{y:0,boxShadow:"0 14px 0 #B8AC98",duration:.18,ease:"back.out(2)"}},{p + .14:.3f});')
    setp("#cur", p, "opacity:0")
    pop("#tout", p + .05, "opacity:0", .05, "none")
    add(f'tl.to("#term",{{backgroundColor:"#3A1513",duration:.08}},{p:.3f});')
    shake("#term", p + .02, 7, 10)
    pop("#stamp1", p + .12, "opacity:0,scale:2.4,rotation:-20", .25, "power4.out")
    ev(p, "press"); ev(p + .12, "stamp")


# S2 loss: rows drain to zero, the dead backup
S2 = (hl("1.2 million rows.", "Gone.") +
      '<div class="card cnt" id="cnt"><div class="lab">ROWS IN PRODUCTION</div><div class="num" id="num">1,204,883</div>'
      '<div class="drain"><i id="drainbar"></i></div></div>'
      '<div class="card bk" id="bk"><svg class="cal" data-layout-ignore viewBox="0 0 120 130" width="120" height="130"><rect x="4" y="12" width="112" height="114" rx="14" fill="#fff" stroke="#1E1B18" stroke-width="6"/>'
      f'<path d="M4 26 a14 14 0 0 1 14 -14 h84 a14 14 0 0 1 14 14 v20 h-112z" fill="{RED}"/><rect x="28" y="2" width="10" height="22" rx="5" fill="#1E1B18"/><rect x="82" y="2" width="10" height="22" rx="5" fill="#1E1B18"/>'
      '<text x="60" y="40" font-family="JBMono" font-size="20" font-weight="700" fill="#fff" text-anchor="middle">MAR</text>'
      '<text x="60" y="104" font-family="Manrope" font-size="54" font-weight="800" fill="#1E1B18" text-anchor="middle">03</text></svg>'
      '<div class="bktext"><div class="lab">LAST WORKING BACKUP</div><div class="big">3 March</div></div>'
      '<div class="chip red" id="dead">DEAD · 239 DAYS</div></div>')


def s2_tl():
    a = SC[1][0]
    hl_tl("s2", a)
    pop("#cnt", a + .05, "opacity:0,y:50", .35, "power3.out")
    r, g = T["rows"], T["gone"]
    add('(()=>{const o={v:1204883};tl.to(o,{v:0,duration:%.3f,ease:"power2.in",onUpdate:()=>{document.getElementById("num").textContent=Math.round(o.v).toLocaleString("en-US");}},%.3f);})();' % (g - r, r))
    add(f'tl.fromTo("#drainbar",{{scaleX:1}},{{scaleX:0,duration:{g - r:.3f},ease:"power2.in",immediateRender:false}},{r:.3f});')
    add(f'tl.to("#num",{{color:"{RED}",duration:.1}},{g - .05:.3f});')
    shake("#cnt", g, 5, 8)
    ev(r, "rattle"); ev(g, "thud")
    pop("#bk", T["backups"] - .15, "opacity:0,x:500", .4, "power3.out")
    ev(T["backups"] - .15, "slide")
    pop("#dead", T["dead"], "opacity:0,scale:2,rotation:-12", .3, "power4.out")
    ev(T["dead"], "stamp")


# S3 the copy: the snapshot card, the three steps
S3 = (hl("But his AI had a", "copy.") +
      '<div class="glow" id="glow3"></div>'
      f'<div class="card snap" id="snap">{db_svg("", INK, CARD, 90, 108)}<div><div class="mono big2">snapshot_0306.dump</div>'
      f'<div class="sub">1,204,883 rows · before the cleanup</div></div><div class="ok">{check_svg()}</div></div>'
      '<div class="steps" id="steps3">' + "".join(f'<div class="st" id="st{i}">{i + 1}</div>' for i in range(3)) + '</div>')


def s3_tl():
    a = SC[2][0]
    hl_tl("s3", a)
    c = T["copy"]
    pop("#glow3", c - .1, "opacity:0,scale:.3", .5, "power3.out")
    pop("#snap", c - .05, "opacity:0,y:120,scale:.6,rotation:8", .5, "back.out(1.6)")
    ev(c - .05, "sparkle")
    h = T["heres"]
    to("#snap", h - .05, "y:-70,scale:.86", .35, "power3.inOut")
    to("#glow3", h - .05, "opacity:0", .3)
    for i in range(3):
        pop(f"#st{i}", h + .1 + i * .14, "opacity:0,scale:0", .3, "back.out(3)")
        ev(h + .1 + i * .14, "tick")


# S4 step 1: the snapshot hook
S4 = (hl("One: a snapshot", "hook.", "STEP 1/3", 1) +
      '<div class="chipcmd" id="cmd4">DROP TABLE</div>'
      '<div class="gate" id="gate"><div class="gbar">HOOK</div><div class="gbody"><svg viewBox="0 0 96 76" width="104" height="82">'
      '<rect x="4" y="16" width="88" height="56" rx="10" fill="#1E1B18"/><rect x="30" y="6" width="36" height="16" rx="5" fill="#1E1B18"/>'
      f'<circle cx="48" cy="44" r="18" fill="{CREAM}"/><circle cx="48" cy="44" r="10" fill="#1E1B18"/><circle cx="76" cy="28" r="4" fill="{CORAL}"/></svg>'
      '<div class="mono gname">prod-guard.sh</div></div><div class="flash" id="flash4"></div></div>'
      f'<div class="dbwrap" id="db4">{db_svg("app_dev")}</div>'
      f'<div class="card toast" id="toast4">{check_svg()}<div><div class="tt">Snapshot saved</div><div class="mono ts">.snapshots/snapshot_0307.dump</div></div></div>')


def s4_tl():
    a = SC[3][0]
    hl_tl("s4", a, True)
    pop("#gate", a + .1, "opacity:0,y:50", .35)
    pop("#db4", a + .2, "opacity:0,y:50", .35)
    b = T["before"]
    add(f'tl.fromTo("#cmd4",{{opacity:0,x:-420}},{{opacity:1,x:0,duration:.45,ease:"power3.out",immediateRender:false}},{b - .1:.3f});')
    ev(b - .1, "slide")
    k = T["backs"] - .1
    add(f'tl.fromTo("#flash4",{{opacity:0}},{{opacity:1,duration:.05,yoyo:true,repeat:1,ease:"none",immediateRender:false}},{k:.3f});')
    pop("#toast4", k + .12, "opacity:0,y:40,scale:.9", .35)
    ev(k, "shutter"); ev(k + .12, "ding")
    f = T["first"] - .15
    to("#cmd4", f, "x:660,scale:.5,opacity:0", .45, "power2.in")
    shake("#db4", f + .45, 4, 6)
    ev(f, "whoosh"); ev(f + .45, "thud")


# S5 step 2: production is blocked
S5 = (hl("Two: production", "blocked.", "STEP 2/3", 2) +
      '<div class="chipcmd red" id="cmd5">DROP DATABASE</div>'
      '<div class="shield" id="shield"><svg viewBox="0 0 160 190" width="170" height="202"><path d="M80 6 L150 32 V92 C150 140 118 170 80 184 C42 170 10 140 10 92 V32 Z" '
      f'fill="{CORAL}" stroke="{INK}" stroke-width="7"/><path d="M48 96 L72 120 L114 72" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
      f'<div class="dbwrap" id="db5">{db_svg("prod-db-01", INK, "#FBE3DD", tag="PRODUCTION")}</div>'
      '<div class="stamp big" id="stamp5">DENIED</div>')


def s5_tl():
    a = SC[4][0]
    hl_tl("s5", a, True)
    pop("#db5", a + .15, "opacity:0,y:50", .35)
    d = T["destructive"] - .1
    add(f'tl.fromTo("#cmd5",{{opacity:0,x:-420}},{{opacity:1,x:0,duration:.4,ease:"power3.out",immediateRender:false}},{d:.3f});')
    ev(d, "slide")
    p = T["prod"] - .05
    pop("#shield", p, "opacity:0,scale:0,rotation:-30", .35, "back.out(2.5)")
    ev(p, "shield")
    r = T["refused"]
    add(f'tl.to("#cmd5",{{x:260,duration:.16,ease:"power2.in"}},{r - .2:.3f});')
    add(f'tl.to("#cmd5",{{x:-40,rotation:-12,duration:.4,ease:"back.out(2)"}},{r - .04:.3f});')
    shake("#shield", r - .04, 3, 6)
    pop("#stamp5", r + .05, "opacity:0,scale:2.4,rotation:-24", .25, "power4.out")
    ev(r - .04, "clang"); ev(r + .05, "stamp")


# S6 step 3: the backup alarm
S6 = (hl("Three: a backup", "alarm.", "STEP 3/3", 3) +
      '<div class="card sess" id="sess"><div class="shead"><i></i>CLAUDE CODE · SESSION START</div>'
      '<div class="srow" id="warn"><b class="chip amber">WARNING</b><span>No backup newer than 26h</span></div>'
      f'<div class="srow" id="okrow"><b class="chip green">OK</b><span>Backup 3 hours old</span></div></div>'
      '<div class="clock" id="clock"><svg viewBox="0 0 160 170" width="170" height="180">'
      f'<circle cx="38" cy="30" r="22" fill="{CORAL}" stroke="{INK}" stroke-width="6"/><circle cx="122" cy="30" r="22" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
      f'<circle cx="80" cy="92" r="62" fill="{CARD}" stroke="{INK}" stroke-width="8"/><path d="M80 92 V56 M80 92 L104 106" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
      f'<path d="M36 150 L26 166 M124 150 L134 166" stroke="{INK}" stroke-width="8" stroke-linecap="round"/></svg></div>')


def s6_tl():
    a = SC[5][0]
    hl_tl("s6", a, True)
    pop("#sess", a + .1, "opacity:0,y:50", .35, "power3.out")
    pop("#warn", a + .3, "opacity:0,x:-30", .3)
    setp("#okrow", a, "opacity:0")
    al = T["alarm"] - .05
    pop("#clock", al, "opacity:0,scale:0", .3, "back.out(3)")
    n = max(1, int((T["fresh"] - .2 - al - .3) / .05) // 2 * 2 - 1)
    add(f'tl.to("#clock",{{rotation:9,duration:.05,yoyo:true,repeat:{n},ease:"none"}},{al + .3:.3f});')
    ev(al, "alarm")
    f = T["fresh"] - .1
    to("#warn", f, "opacity:0,x:40", .2)
    pop("#okrow", f + .1, "opacity:0,x:-30", .3)
    to("#clock", f + .05, "rotation:0,scale:.8,opacity:.5", .3)
    ev(f + .1, "chime")


# S7 twist: read-only production (dark)
S7 = (hl("Read-only", "production.") +
      f'<div class="dbwrap dark" id="db7">{db_svg("production", CREAM, TERM, 260, 300)}</div>'
      '<div class="lock" id="lock"><svg viewBox="0 0 120 150" width="132" height="165">'
      f'<path d="M28 66 V44 a32 32 0 0 1 64 0 V66" stroke="{CREAM}" stroke-width="14" fill="none"/>'
      f'<rect x="8" y="62" width="104" height="84" rx="14" fill="{CORAL}" stroke="{CREAM}" stroke-width="6"/><circle cx="60" cy="98" r="10" fill="{TERM}"/><rect x="55" y="98" width="10" height="24" rx="4" fill="{TERM}"/></svg></div>' +
      "".join(f'<div class="chipcmd ghost" id="b{i}">{c}</div><div class="denied" id="d{i}">permission denied</div>'
              for i, c in enumerate(["DELETE", "DROP", "TRUNCATE"])))


def s7_tl():
    a, z = SC[6]
    add(f'tl.to("#bgdark",{{opacity:1,duration:.25}},{a:.3f});')
    add(f'tl.to("#bgdark",{{opacity:0,duration:.25}},{z - .05:.3f});')
    setp("#root", a, f'"--ink":"{CREAM}"')
    setp("#root", z, f'"--ink":"{INK}"')
    ev(a, "drop")
    hl_tl("s7", a)
    pop("#db7", a + .1, "opacity:0,y:60", .4, "power3.out")
    r = T["readonly"] - .1
    add(f'tl.fromTo("#lock",{{opacity:0,y:-500}},{{opacity:1,y:0,duration:.32,ease:"power4.in",immediateRender:false}},{r:.3f});')
    shake("#db7", r + .32, 3, 6)
    ev(r + .3, "lock")
    c = T["cant"] - .2
    for i in range(3):
        t = c + i * .32
        side = -1 if i != 1 else 1
        add(f'tl.fromTo("#b{i}",{{opacity:0,x:{side * 520}}},{{opacity:1,x:0,duration:.22,ease:"power2.in",immediateRender:false}},{t:.3f});')
        add(f'tl.to("#b{i}",{{x:{side * 140},rotation:{side * 14},opacity:.0,duration:.4,ease:"power2.out"}},{t + .22:.3f});')
        pop(f"#d{i}", t + .22, "opacity:0,scale:.6", .2)
        ev(t + .22, "bonk")


# S8 CTA: comment BACKUP, the PDF
S8 = ('<div class="cta"><div class="cchip" id="cchip">COMMENT</div><div class="cword" id="cword">BACKUP</div></div>'
      '<div class="card cbox" id="cbox"><i class="av"></i><div class="ctext">' +
      "".join(f'<span class="cc" id="cc{i}">{c}</span>' for i, c in enumerate("BACKUP")) +
      '<span class="ccur" id="ccur"></span></div><div class="send" id="send"><svg viewBox="0 0 40 40" width="40" height="40"><path d="M8 20 H30 M21 11 L30 20 L21 29" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>'
      '<div class="pdf" id="pdf"><img src="assets/img/pdf-cover-1.png" alt=""><div class="pdftag">FREE PDF · 6 PAGES</div></div>')


def s8_tl():
    a = SC[7][0]
    pop("#cchip", a + .02, "opacity:0,y:-30", .3)
    pop("#cword", T["backup"] - .05, "opacity:0,scale:2.2,rotation:-8", .32, "power4.out")
    ev(T["backup"] - .05, "slam")
    pop("#cbox", a + .1, "opacity:0,y:50", .35, "power3.out")
    t0 = T["backup"] + .05
    for i in range(6):
        setp(f"#cc{i}", t0 + i * .09, "opacity:1")
        ev(t0 + i * .09, "key")
    s = T["send"] - .1
    add(f'tl.to("#send",{{scale:.85,duration:.08,yoyo:true,repeat:1,ease:"power2.inOut"}},{s:.3f});')
    ev(s, "send")
    add(f'tl.fromTo("#pdf",{{opacity:0,y:200,rotation:18,scale:.6}},{{opacity:1,y:0,rotation:-5,scale:1,duration:.6,ease:"back.out(1.5)",immediateRender:false}},{s + .15:.3f});')
    add(f'tl.to("#pdf",{{y:-10,duration:.8,yoyo:true,repeat:{max(1, int((DUR - s - .8) / .8))},ease:"sine.inOut"}},{s + .8:.3f});')
    ev(s + .15, "flip"); ev(s + .5, "sparkle")


# ---------------------------------------------------------------- the mascot's path through the video
def mascot_tl():
    add('gsap.set("#m-armL",{svgOrigin:"28 105"});gsap.set("#m-armR",{svgOrigin:"196 105"});gsap.set("#m-body",{svgOrigin:"112 182"});')
    setp("#mascot", 0, "x:330,y:1130,scale:1")
    face(0, "open")
    # idle: a gentle bob all the way through, and a blink every few seconds
    add(f'tl.to("#m-body",{{y:-6,duration:.38,yoyo:true,repeat:{int(DUR / .38)},ease:"sine.inOut"}},0);')
    # S1: watches the command, jumps on Enter, panics
    hop(T["press"] - .5, 678, 993)
    face(T["press"] + .1, "wide", "frown", True)
    arms(T["press"] + .1, 30, -30)
    # S2: beside the counter, sweating
    hop(SC[1][0] + .05, 770, 770, .9)
    shake("#mascot", T["gone"], 5, 6)
    # S3: center stage with the copy
    hop(SC[2][0] + .05, 410, 1030, 1.15)
    face(T["copy"] - .1, "happy", "smile")
    arms(T["copy"] - .1, 60, -60)
    arms(T["heres"] + .2, 0, 0)
    # S4: on top of the gate, a thumbs-up when the snapshot lands
    hop(SC[3][0] + .05, 418, 604, .95)
    face(SC[3][0] + .2, "open")
    arms(T["backs"], 0, -80)
    face(T["backs"] + .1, "happy", "smile")
    # S5: arms crossed under the shield
    hop(SC[4][0] + .05, 405, 1105, .85)
    face(SC[4][0] + .3, "open")
    arms(T["prod"], -110, 110)
    face(T["refused"], "happy", "smile")
    # S6: covers its ears at the alarm, happy at "fresh"
    hop(SC[5][0] + .05, 760, 1080, .9)
    face(T["alarm"], "shut", "frown")
    arms(T["alarm"], -150, 150)
    face(T["fresh"], "happy", "smile")
    arms(T["fresh"], 0, 0)
    # S7: on guard by the locked database
    hop(SC[6][0] + .05, 760, 1060, .9)
    face(SC[6][0] + .3, "open")
    face(T["touch"], "happy", "smile")
    # S8: waving beside the PDF
    hop(SC[7][0] + .05, 770, 1110, .95)
    face(SC[7][0] + .3, "happy", "smile")
    wave(T["send"] + .2, 5)
    # blinks wherever the face is plain
    for t in [2.2, 5.1, 9.3, 14.6, 20.4, 23.1, 27.8, 33.5]:
        if t < DUR - .5:
            add(f'tl.set("#m-eo",{{scaleY:.1,transformOrigin:"50% 42%"}},{t:.3f});tl.set("#m-eo",{{scaleY:1}},{t + .1:.3f});')


# ---------------------------------------------------------------- captions: phrase chunks, the spoken word on a coral pill
def captions():
    html, chunks = [], []
    for li in range(len(LINES)):
        ws = [w for w in WORDS if w["line"] == li + 1]
        cur = []
        for w in ws:
            cur.append(w)
            if len(cur) >= 4 or re.search(r"[.,?!:]$|\.\.\.$", w["w"]):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
    for ci, ch in enumerate(chunks):
        spans = " ".join(f'<span class="cw" id="w{ci}_{k}">{w["w"]}</span>' for k, w in enumerate(ch))
        html.append(f'<div class="cap" id="cap{ci}">{spans}</div>')
        a = ch[0]["s"] - .06
        z = chunks[ci + 1][0]["s"] - .06 if ci + 1 < len(chunks) else DUR
        z = min(z, ch[-1]["e"] + .9)
        add(f'tl.fromTo("#cap{ci}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.12,ease:"power2.out",immediateRender:false}},{a:.3f});')
        add(f'tl.set("#cap{ci}",{{opacity:0}},{z:.3f});')
        for k, w in enumerate(ch):
            end = ch[k + 1]["s"] if k + 1 < len(ch) else min(z, w["e"] + .25)
            add(f'tl.set("#w{ci}_{k}",{{backgroundColor:"{CORAL_T}",color:"#fff"}},{w["s"] - .02:.3f});'
                f'tl.set("#w{ci}_{k}",{{backgroundColor:"rgba(232,115,90,0)",color:"var(--ink)"}},{end - .02:.3f});')
    return "".join(html)


CSS = f"""
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }}
@font-face {{ font-family: "ISerif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 400; src: url("assets/fonts/JetBrainsMono-Regular.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {CREAM}; }}
#root {{ --ink: {INK}; position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {CREAM}; font-family: "Manrope", sans-serif; color: {INK}; }}
.clip {{ position: absolute; inset: 0; }}
.mono {{ font-family: "JBMono", monospace; }}
#bg {{ background-color: {CREAM}; background-image: linear-gradient({GRID} 2px, transparent 2px), linear-gradient(90deg, {GRID} 2px, transparent 2px);
  background-size: 60px 60px; background-position: 30px 0; }}
#bgdark {{ position: absolute; inset: 0; opacity: 0; background-color: {TERM}; background-image: linear-gradient(#2A2830 2px, transparent 2px),
  linear-gradient(90deg, #2A2830 2px, transparent 2px); background-size: 60px 60px; background-position: 30px 0; }}
.giant {{ position: absolute; left: 0; right: 0; top: 760px; text-align: center; opacity: 0; font: 800 330px/1 "Manrope"; letter-spacing: -10px;
  color: transparent; -webkit-text-stroke: 4px rgba(30,27,24,.08); white-space: nowrap; }}
#g7 {{ -webkit-text-stroke-color: rgba(241,233,220,.08); font-size: 300px; }}
/* chrome */
.top {{ position: absolute; left: 70px; right: 70px; top: 262px; display: flex; justify-content: space-between; align-items: center; }}
.brand {{ font: 700 30px "JBMono"; letter-spacing: 4px; color: var(--ink); display: flex; align-items: center; gap: 14px; }}
.brand i {{ width: 18px; height: 18px; border-radius: 50%; background: {CORAL}; }}
.prog {{ width: 220px; height: 26px; border-radius: 13px; border: 3px solid var(--ink); overflow: hidden; }}
.prog i {{ display: block; width: 100%; height: 100%; background: {CORAL}; transform-origin: 0 50%; transform: scaleX(0); }}
/* headline */
.hl {{ position: absolute; left: 70px; right: 70px; top: 340px; }}
.kick {{ display: flex; align-items: center; gap: 18px; margin-bottom: 14px; font: 700 28px "JBMono"; letter-spacing: 4px; color: {CORAL_D}; }}
.segs {{ display: flex; gap: 8px; }} .segs i {{ width: 54px; height: 10px; border-radius: 5px; background: rgba(30,27,24,.15); }} .segs i.on {{ background: {CORAL}; }}
.l1 {{ font: 800 76px/1.05 "Manrope"; letter-spacing: -2.5px; color: var(--ink); }}
.hw {{ display: inline-block; }}
.l2 {{ margin-top: 2px; }}
.acc {{ display: inline-block; font: 400 128px/1 "ISerif"; font-style: italic; color: {CORAL_T}; letter-spacing: -1px; }}
/* cards */
.card {{ position: absolute; background: {CARD}; border: 3px solid {CARD_B}; border-radius: 28px; box-shadow: 0 18px 40px rgba(60,40,20,.12); }}
.lab {{ font: 700 28px "JBMono"; letter-spacing: 3px; color: #8A7F70; }}
.chip {{ display: inline-block; padding: 8px 18px; border-radius: 30px; font: 700 26px "JBMono"; letter-spacing: 2px; color: #fff; }}
.chip.red {{ background: {RED}; }} .chip.amber {{ background: {AMBER}; color: {INK}; }} .chip.green {{ background: {GREEN}; }}
/* S1 */
.term {{ position: absolute; left: 70px; top: 620px; width: 940px; height: 340px; border-radius: 28px; background: {TERM}; overflow: hidden;
  box-shadow: 0 24px 50px rgba(30,20,10,.25); }}
.bar {{ height: 64px; display: flex; align-items: center; gap: 12px; padding: 0 26px; background: #26252C; }}
.bar i {{ width: 18px; height: 18px; border-radius: 50%; background: #4A4852; }} .bar i:first-child {{ background: {RED}; }}
.bar span {{ margin-left: 14px; font: 400 28px "JBMono"; color: #A9A4B4; }}
.ptag {{ margin-left: auto; padding: 6px 16px; border-radius: 10px; background: {RED}; font: 700 28px "JBMono"; letter-spacing: 2px; color: #fff; }}
.tbody {{ padding: 26px 34px; }}
.tl {{ font: 700 44px/1.6 "JBMono"; color: #F4EEE6; white-space: nowrap; }}
.tl.dim {{ font-weight: 400; color: #8E899A; font-size: 36px; }}
.tl.red {{ color: #FF6B5E; opacity: 0; }}
.ch {{ opacity: 0; }}
.cur {{ display: inline-block; width: 24px; height: 46px; margin-left: 4px; vertical-align: -6px; background: #F4EEE6; }}
.stamp {{ position: absolute; right: 110px; bottom: 40px; opacity: 0; padding: 6px 26px; border: 8px solid {RED}; border-radius: 16px; color: {RED};
  font: 800 76px/1.1 "Manrope"; letter-spacing: 2px; transform: rotate(-8deg); background: rgba(255,250,245,.92); }}
.stamp.big {{ right: auto; left: 250px; bottom: auto; top: 625px; font-size: 96px; }}
.key {{ position: absolute; left: 640px; top: 1170px; width: 300px; height: 132px; border-radius: 26px; background: {CARD}; border: 4px solid {INK};
  box-shadow: 0 14px 0 #B8AC98; display: flex; align-items: center; justify-content: center; gap: 16px; font: 800 44px "Manrope"; letter-spacing: 2px; }}
/* S2 */
.cnt {{ left: 70px; top: 650px; width: 640px; height: 300px; padding: 34px 38px; }}
.num {{ margin-top: 12px; font: 800 104px/1 "Manrope"; letter-spacing: -4px; }}
.drain {{ margin-top: 26px; height: 22px; border-radius: 11px; background: #EFE6D8; overflow: hidden; }}
.drain i {{ display: block; height: 100%; width: 100%; background: {RED}; transform-origin: 0 50%; }}
.bk {{ left: 70px; top: 1000px; width: 940px; height: 210px; padding: 30px 36px; display: flex; align-items: center; gap: 30px; }}
.bk .big {{ font: 800 64px/1.1 "Manrope"; letter-spacing: -1.5px; }}
.bk .chip {{ position: absolute; right: 30px; top: -26px; font-size: 30px; padding: 12px 24px; }}
/* S3 */
.glow {{ position: absolute; left: 140px; top: 640px; width: 800px; height: 640px; opacity: 0;
  background: radial-gradient(circle, rgba(232,115,90,.35), rgba(232,115,90,0) 65%); }}
.snap {{ left: 110px; top: 690px; width: 860px; height: 220px; padding: 30px 36px; display: flex; align-items: center; gap: 30px; border: 5px solid {CORAL}; }}
.big2 {{ font-size: 44px; font-weight: 700; }}
.sub {{ margin-top: 8px; font: 600 34px "Manrope"; color: #6E6458; }}
.ok {{ margin-left: auto; }}
.steps {{ position: absolute; left: 0; right: 0; top: 860px; display: flex; justify-content: center; gap: 60px; }}
.st {{ width: 130px; height: 130px; border-radius: 50%; background: {INK}; color: {CREAM}; display: flex; align-items: center; justify-content: center;
  font: 400 96px/1 "ISerif"; font-style: italic; }}
.st:nth-child(1) {{ background: {CORAL_T}; }}
/* S4 / S5 diagrams */
.chipcmd {{ position: absolute; left: 70px; top: 905px; padding: 18px 26px; border-radius: 18px; background: {INK}; color: {CREAM}; font: 700 38px "JBMono";
  white-space: nowrap; box-shadow: 0 12px 24px rgba(30,20,10,.18); }}
.chipcmd.red {{ background: {RED}; color: #fff; }}
.gate {{ position: absolute; left: 400px; top: 790px; width: 280px; height: 290px; border-radius: 28px; background: {CARD}; border: 4px solid {INK}; overflow: hidden;
  box-shadow: 0 18px 36px rgba(60,40,20,.15); }}
.gbar {{ height: 64px; background: {CORAL_T}; color: #fff; font: 800 34px/64px "Manrope"; letter-spacing: 6px; text-align: center; }}
.gbody {{ display: flex; flex-direction: column; align-items: center; gap: 14px; padding-top: 34px; }}
.gname {{ font-size: 28px; font-weight: 700; }}
.flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
.dbwrap {{ position: absolute; left: 770px; top: 800px; }}
.db {{ position: relative; display: flex; flex-direction: column; align-items: center; }}
.dblabel {{ margin-top: 10px; font: 700 28px "JBMono"; color: var(--ink); }}
.dbtag {{ position: absolute; top: -48px; padding: 6px 14px; border-radius: 10px; color: #fff; font: 700 28px "JBMono"; letter-spacing: 2px; white-space: nowrap; }}
.toast {{ left: 70px; top: 1120px; width: 940px; height: 150px; padding: 26px 34px; display: flex; align-items: center; gap: 26px; }}
.tt {{ font: 800 46px "Manrope"; }} .ts {{ font-size: 28px; color: #6E6458; margin-top: 4px; }}
.shield {{ position: absolute; left: 470px; top: 820px; }}
#db5 {{ top: 830px; }}
/* S6 */
.sess {{ left: 70px; top: 650px; width: 940px; height: 330px; padding: 34px 38px; }}
.shead {{ display: flex; align-items: center; gap: 14px; font: 700 28px "JBMono"; letter-spacing: 3px; color: #8A7F70; }}
.shead i {{ width: 16px; height: 16px; border-radius: 50%; background: {CORAL}; }}
.srow {{ position: absolute; left: 38px; right: 38px; top: 150px; display: flex; align-items: center; gap: 24px; font: 700 46px "Manrope"; letter-spacing: -1px; }}
.srow .chip {{ font-size: 30px; padding: 12px 22px; }}
.clock {{ position: absolute; left: 150px; top: 1030px; }}
/* S7 */
#db7 {{ left: 410px; top: 760px; }}
.lock {{ position: absolute; left: 474px; top: 890px; }}
.chipcmd.ghost {{ top: 0; left: 0; background: {CREAM}; color: {TERM}; opacity: 0; }}
#b0 {{ left: 90px; top: 760px; }} #b1 {{ left: 700px; top: 900px; }} #b2 {{ left: 90px; top: 1050px; }}
.denied {{ position: absolute; opacity: 0; padding: 6px 14px; border-radius: 10px; background: {RED}; color: #fff; font: 700 28px "JBMono"; }}
#d0 {{ left: 120px; top: 850px; }} #d1 {{ left: 720px; top: 990px; }} #d2 {{ left: 120px; top: 1140px; }}
/* S8 */
.cta {{ position: absolute; left: 0; right: 0; top: 340px; text-align: center; }}
.cchip {{ display: inline-block; padding: 12px 30px; border-radius: 40px; background: {INK}; color: {CREAM}; font: 700 34px "JBMono"; letter-spacing: 8px; }}
.cword {{ margin: 22px auto 0; display: table; padding: 10px 48px 22px; border-radius: 40px; background: {CORAL_T}; color: #fff; font: 800 150px/1.05 "Manrope"; letter-spacing: -3px;
  box-shadow: 0 18px 0 {CORAL_D}; }}
.cbox {{ left: 70px; top: 700px; width: 940px; height: 132px; padding: 0 26px; display: flex; align-items: center; gap: 22px; border-radius: 66px; }}
.av {{ width: 76px; height: 76px; border-radius: 50%; background: linear-gradient(135deg, {CORAL}, {AMBER}); }}
.ctext {{ flex: 1; font: 800 54px "Manrope"; letter-spacing: 2px; }}
.cc {{ opacity: 0; }}
.ccur {{ display: inline-block; width: 4px; height: 52px; background: {CORAL}; vertical-align: -6px; margin-left: 4px; }}
.send {{ width: 88px; height: 88px; border-radius: 50%; background: {CORAL}; display: flex; align-items: center; justify-content: center; }}
.pdf {{ position: absolute; left: 150px; top: 880px; width: 300px; opacity: 0; }}
.pdf img {{ width: 300px; height: 424px; display: block; border-radius: 14px; box-shadow: 0 26px 50px rgba(40,20,60,.35); }}
.pdftag {{ position: absolute; left: 120px; top: -30px; padding: 10px 20px; border-radius: 30px; background: {GREEN}; color: #fff; font: 700 26px "JBMono"; letter-spacing: 2px;
  white-space: nowrap; transform: rotate(4deg); font-size: 28px; }}
/* mascot */
#mascot {{ position: absolute; left: 0; top: 0; width: 224px; height: 182px; transform-origin: 50% 100%; }}
#mascot svg {{ display: block; overflow: visible; }}
#m-body {{ transform-origin: 112px 182px; }}
#m-armL {{ transform-origin: 28px 105px; }} #m-armR {{ transform-origin: 196px 105px; }}
#m-shadow {{ position: absolute; left: 32px; right: 32px; bottom: -14px; height: 16px; border-radius: 50%; background: rgba(30,20,10,.14); }}
/* captions */
.cap {{ position: absolute; left: 60px; right: 60px; top: 1330px; text-align: center; opacity: 0; font: 800 60px/1.25 "Manrope"; letter-spacing: -1px; color: var(--ink); }}
.cw {{ display: inline-block; padding: 2px 12px 6px; border-radius: 16px; }}
.cw.on {{ background: {CORAL_T}; color: #fff; }}
#flashfx {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
"""


def main():
    s1_tl(); s2_tl(); s3_tl(); s4_tl(); s5_tl(); s6_tl(); s7_tl(); s8_tl()
    sids = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
    for k, sid in enumerate(sids):
        scene_tl(k, sid)
    giant = giant_tl()
    mascot_tl()
    caps = captions()
    add(f'tl.to(".prog i",{{scaleX:1,duration:{DUR},ease:"none"}},0);')
    A.insert(0, "      gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ",{opacity:0});")
    scenes = "".join(scene(k, sid, html) for k, (sid, html) in enumerate(zip(sids, [S1, S2, S3, S4, S5, S6, S7, S8])))
    has_mix = os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav"))
    audio = (f'<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>' if has_mix else
             f'<audio id="vo" src="assets/audio/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>'
             if os.path.exists(os.path.join(ROOT, "assets", "audio", "voice.wav")) else "")
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Prod Guard explainer 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-ignore><div id="bgdark"></div></div>
      <div id="giants" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore>{giant}</div>
      {scenes}
      <div id="mlayer" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5" data-layout-allow-overflow>{mascot()}</div>
      <div id="chrome" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6"><div class="top"><div class="brand"><i></i>AI.NXTLVL</div><div class="prog"><i></i></div></div></div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{caps}</div>
      {audio}
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
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    T["ev"] = sorted(EV)
    json.dump(T, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, {len(EV)} sound events, audio: {'mix' if has_mix else 'voice' if audio else 'none'}")


if __name__ == "__main__":
    main()
