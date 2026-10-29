"""The haunted-house explainer (ai.nxtlvl style, 3D + 2D): writes index.html and build/cues.json. 1080x1920, 30 fps.

python3 build/generate.py      (from the project root, after build/voice.py)

The 3D world (assets/js/world.js, Three.js, rendered on hf-seek) is the production database as a Victorian haunted house:
rooms are tables, candles are rows, DROP DATABASE is a sheet ghost; the pixel mascot walks the house with a lantern.
This file writes the 2D explainer layer over it, in the ai.nxtlvl explainer language turned to night: the "● AI.NXTLVL"
top bar and progress pill, headlines with one coral italic-serif word, "STEP 1/3" headers, white cards (the typed
command, the row counter, the snapshot, a polaroid, the session check), stamps, word-by-word captions with the spoken
word on a coral pill, and the CTA ending on the real Prod Guard PDF cover. Every visual event is logged to
cues.json["ev"] so build/audio.py can give it a sound.
"""
import json
import os
import random
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
DUR = round(E[-1] + 1.6, 2)

CREAM, INK, CORAL, CORAL_D, CORAL_T = "#F1E9DC", "#1E1B18", "#E8735A", "#B9523D", "#D45C40"
GREEN, AMBER, TERM, CARD, CARD_B, RED = "#3FA372", "#F2B33D", "#1B1A1F", "#FFFDF8", "#E2D6C3", "#D9483B"


def word(li, text, nth=1):
    hits = [w for w in WORDS if w["line"] == li + 1 and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not in line {li + 1}")
    return hits[nth - 1]["s"]


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
# lightning flashes world.js draws and audio.py answers with thunder: [time, flash, thunder gain]
T["lightning"] = [[.35, 1, .8], [.62, .6, 0], [T["press"], 1, 1], [round(T["dead"] - .05, 3), .85, .7], [round(SC[4][0] + .25, 3), .7, .55],
                  [SC[6][0], 1, .9], [round(SC[6][0] + .35, 3), .7, 0], [T["touch"], .8, .7], [round(SC[7][0] + .7, 3), .45, .4]]
# bat flights (world.js draws one flock per entry, audio.py gives each a flutter): the opening, out of the chimney on
# Enter, past the camera at the twist, circling the moon in the CTA
T["bats"] = [.15, round(T["press"] + .15, 3), round(SC[6][0] + .3, 3), round(SC[7][0] + .2, 3)]
# the heartbeat under the deletion, shared by the vignette here and the thumps in audio.py
T["hb"] = []
_u = T["press"] + .5
while _u < SC[2][0] - .3:
    T["hb"].append(round(_u, 3))
    _u += 60 / (88 + (_u - T["press"]) * 4)
A, EV, HIDE = [], [], []


def add(js):
    A.append("      " + js)


def ev(t, kind):
    EV.append([round(t, 3), kind])


def pop(sel, t, frm="opacity:0,y:30,scale:.9", d=.35, ease="back.out(1.8)"):
    if "opacity:0" in frm and t > .05:
        HIDE.append(sel)
    add(f'tl.fromTo("{sel}",{{{frm}}},{{opacity:1,x:0,y:0,scale:1,rotation:0,duration:{d},ease:"{ease}",immediateRender:false}},{t:.3f});')


def to(sel, t, props, d=.3, ease="power2.out"):
    add(f'tl.to("{sel}",{{{props},duration:{d},ease:"{ease}"}},{t:.3f});')


def setp(sel, t, props):
    add(f'tl.set("{sel}",{{{props}}},{t:.3f});')


def shake(sel, t, n=6, amp=8, d=.05):
    add(f'tl.to("{sel}",{{x:"+={amp}",duration:{d},yoyo:true,repeat:{n},ease:"sine.inOut"}},{t:.3f});')


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


def check_svg(c=GREEN, s=44):
    return (f'<svg viewBox="0 0 44 44" width="{s}" height="{s}"><circle cx="22" cy="22" r="22" fill="{c}"/>'
            f'<path d="M12 23 L19 30 L32 15" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def scene(k, sid, inner):
    a, z = SC[k]
    return (f'<div id="{sid}" class="clip scene" data-start="{a}" data-duration="{round(z - a, 3)}" '
            f'data-track-index="{3 + k % 2}" data-layout-allow-overflow><div class="inner">{inner}</div></div>')


def scene_tl(k, sid):
    a, z = SC[k]
    if k:
        add(f'tl.fromTo("#{sid} .inner",{{opacity:0}},{{opacity:1,duration:.2,ease:"power2.out",immediateRender:false}},{a:.3f});')
        ev(a, "whoosh")
    if k < len(SC) - 1:
        add(f'tl.to("#{sid} .inner",{{opacity:0,duration:.14,ease:"power2.in"}},{z - .14:.3f});')


# S1 hook: the typed command, Enter, the house goes dark
CMD = "DROP DATABASE app;"
S1 = (hl("He just deleted", "production.") +
      '<div class="term" id="term"><div class="bar"><i></i><i></i><i></i><span>prod-db-01</span><b class="ptag">PRODUCTION</b></div>'
      '<div class="tl">prod=# ' + "".join(f'<span class="ch" id="ch{i}">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(CMD)) +
      '<span class="cur" id="cur"></span></div></div><div class="stamp" id="stamp1">DELETED</div>')


def s1_tl():
    a = SC[0][0]
    add(f'tl.fromTo("#s1 .acc",{{scale:1.12}},{{scale:1,duration:.5,ease:"back.out(2)",immediateRender:false}},0);')
    t0, t1 = a + .3, T["press"] - .45
    for i in range(len(CMD)):
        t = t0 + (t1 - t0) * i / len(CMD)
        setp(f"#ch{i}", t, "opacity:1")
        if i % 3 == 0:
            ev(t, "type")
    add(f'tl.fromTo("#cur",{{opacity:1}},{{opacity:0,duration:.25,yoyo:true,repeat:{int((T["press"] - a) / .25)},ease:"steps(1)",immediateRender:false}},{a:.3f});')
    p = T["press"]
    setp("#cur", p, "opacity:0")
    setp("#term .tl", p + .08, 'visibility:"hidden"')   # the command vanishes under the stamp
    add(f'tl.to("#term",{{backgroundColor:"#3A1513",duration:.08}},{p:.3f});')
    shake("#term", p + .02, 7, 10)
    pop("#stamp1", p + .12, "opacity:0,scale:2.4,rotation:-20", .25, "power4.out")
    ev(p, "press"); ev(p + .12, "stamp")


# S2 the loss: the counter drains as the ghost goes room to room; then the backups' grave
S2 = (hl("1.2 million rows.", "Gone.") +
      '<div class="card cnt" id="cnt"><div class="lab">ROWS IN PRODUCTION</div><div class="num" id="num">1,204,883</div>'
      '<div class="drain"><i id="drainbar"></i></div></div>'
      '<div class="chip red big" id="dead">DEAD · 239 DAYS · NOBODY CHECKED</div>')


def s2_tl():
    a = SC[1][0]
    hl_tl("s2", a)
    pop("#cnt", a + .05, "opacity:0,y:50", .35, "power3.out")
    r, g = a + .3, T["gone"]
    add('(()=>{const o={v:1204883};tl.to(o,{v:0,duration:%.3f,ease:"power1.in",onUpdate:()=>{document.getElementById("num").textContent=Math.round(o.v).toLocaleString("en-US");}},%.3f);})();' % (g - r, r))
    add(f'tl.fromTo("#drainbar",{{scaleX:1}},{{scaleX:0,duration:{g - r:.3f},ease:"power1.in",immediateRender:false}},{r:.3f});')
    add(f'tl.to("#num",{{color:"{RED}",duration:.1}},{g - .05:.3f});')
    shake("#cnt", g, 5, 8)
    ev(r, "rattle"); ev(g, "thud")
    to("#cnt", T["backups"] - .2, "opacity:0,y:40", .15)
    pop("#dead", T["dead"], "opacity:0,scale:2,rotation:-10", .3, "power4.out")
    ev(T["dead"], "stamp")


# S3 the copy: the snapshot card, the three steps
S3 = (hl("But his AI had a", "copy.") +
      f'<div class="card snap" id="snap"><div class="dbi"></div><div><div class="mono big2">snapshot_0306.dump</div>'
      f'<div class="sub">1,204,883 rows · all of them</div></div><div class="ok">{check_svg()}</div></div>'
      '<div class="steps" id="steps3">' + "".join(f'<div class="st" id="st{i}">{i + 1}</div>' for i in range(3)) + '</div>')


def s3_tl():
    a = SC[2][0]
    hl_tl("s3", a)
    c = T["copy"]
    pop("#snap", c - .05, "opacity:0,y:120,scale:.6,rotation:8", .5, "back.out(1.6)")
    ev(c - .05, "sparkle")
    h = T["heres"]
    to("#snap", h - .05, "opacity:0,y:-40", .25, "power2.in")
    for i in range(3):
        pop(f"#st{i}", h + .1 + i * .14, "opacity:0,scale:0", .3, "back.out(3)")
        ev(h + .1 + i * .14, "tick")


# S4 step 1: the snapshot hook (the polaroid before the ghost)
S4 = (hl("One: a snapshot", "hook.", "STEP 1/3", 1) +
      '<div class="chipcmd" id="cmd4">DROP TABLE orders <b>→ prod-guard.sh</b></div>'
      '<div class="polaroid" id="pol"><div class="pimg">' + "".join(f'<i style="left:{14 + (i % 9) * 30}px;top:{30 + (i // 9) * 46}px"></i>' for i in range(27)) +
      f'</div><div class="pcap">orders · snapshot saved {check_svg(GREEN, 34)}</div></div>')


def s4_tl():
    a = SC[3][0]
    hl_tl("s4", a, True)
    b = T["before"]
    add(f'tl.fromTo("#cmd4",{{opacity:0,x:-420}},{{opacity:1,x:0,duration:.45,ease:"power3.out",immediateRender:false}},{b - .1:.3f});')
    ev(b - .1, "slide")
    k = T["backs"] - .1
    pop("#pol", k + .05, "opacity:0,y:120,rotation:-20,scale:.6", .45, "back.out(1.6)")
    add(f'tl.set("#pol",{{rotation:4}},{k + .5:.3f});')
    ev(k, "shutter"); ev(k + .1, "ding")
    to("#cmd4", T["first"] - .1, "opacity:0,x:300", .3, "power2.in")
    ev(T["first"] - .1, "ghost")


# S5 step 2: the warded door
S5 = (hl("Two: production", "blocked.", "STEP 2/3", 2) +
      '<div class="chipcmd red" id="cmd5">DROP DATABASE</div><div class="stamp big" id="stamp5">DENIED</div>')


def s5_tl():
    a = SC[4][0]
    hl_tl("s5", a, True)
    d = T["destructive"] - .1
    add(f'tl.fromTo("#cmd5",{{opacity:0,x:-420}},{{opacity:1,x:0,duration:.4,ease:"power3.out",immediateRender:false}},{d:.3f});')
    ev(d, "ghost")
    ev(T["prod"] - .05, "ward")
    r = T["refused"]
    add(f'tl.to("#cmd5",{{x:-60,rotation:-10,duration:.4,ease:"back.out(2)"}},{r - .1:.3f});')
    pop("#stamp5", r + .02, "opacity:0,scale:2.4,rotation:-24", .25, "power4.out")
    ev(r - .12, "clang"); ev(r + .02, "stamp")


# S6 step 3: the clock and the session check
S6 = (hl("Three: a backup", "alarm.", "STEP 3/3", 3) +
      '<div class="card sess" id="sess"><div class="shead"><i></i>CLAUDE CODE · SESSION START</div>'
      '<div class="srow" id="warn"><b class="chip amber">WARNING</b><span>No backup newer than 26h</span></div>'
      '<div class="srow" id="okrow"><b class="chip green">OK</b><span>Backup 3 hours old</span></div></div>')


def s6_tl():
    a = SC[5][0]
    hl_tl("s6", a, True)
    pop("#sess", a + .1, "opacity:0,y:50", .35, "power3.out")
    pop("#warn", T["alarm"] - .05, "opacity:0,x:-30", .3)
    HIDE.append("#okrow")
    ev(T["alarm"] - .05, "alarm")
    f = T["fresh"] - .1
    to("#warn", f, "opacity:0,x:40", .2)
    pop("#okrow", f + .1, "opacity:0,x:-30", .3)
    ev(f + .1, "chime")


# S7 the twist: boarded up, read-only
S7 = (hl("Read-only", "production.") +
      "".join(f'<div class="denied" id="d{i}">{c} · permission denied</div>' for i, c in enumerate(["DELETE", "DROP", "TRUNCATE"])))


def s7_tl():
    a = SC[6][0]
    ev(a, "drop")
    hl_tl("s7", a)
    r = T["readonly"] - .15
    for i in range(6):
        ev(r + i * .09, "board")
    ev(T["readonly"] + .3, "lock")
    c = T["cant"] - .1
    for i in range(3):
        pop(f"#d{i}", c + i * .3, "opacity:0,scale:.6,x:-40", .25, "back.out(2)")
        ev(c + i * .3, "bonk")


# S8 CTA
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
    for i in range(6):
        setp(f"#cc{i}", T["backup"] + .05 + i * .09, "opacity:1")
        ev(T["backup"] + .05 + i * .09, "key")
    HIDE.extend(f"#cc{i}" for i in range(6))
    s = T["send"] - .1
    add(f'tl.to("#send",{{scale:.85,duration:.08,yoyo:true,repeat:1,ease:"power2.inOut"}},{s:.3f});')
    ev(s, "send")
    add(f'tl.fromTo("#pdf",{{opacity:0,y:200,rotation:18,scale:.6}},{{opacity:1,y:0,rotation:-5,scale:1,duration:.6,ease:"back.out(1.5)",immediateRender:false}},{s + .15:.3f});')
    HIDE.append("#pdf")
    add(f'tl.to("#pdf",{{y:-10,duration:.8,yoyo:true,repeat:{max(1, int((DUR - s - .8) / .8))},ease:"sine.inOut"}},{s + .8:.3f});')
    ev(s + .15, "flip"); ev(s + .5, "sparkle")


def glitch(sel, t, n=7):
    """A few frames of RGB-split jitter on a headline, then back to rest."""
    r = random.Random(round(t * 1000))
    for i in range(n):
        dx, sk = r.uniform(-16, 16), r.uniform(-9, 9)
        sp = r.uniform(4, 9)
        setp(sel, t + i / 30, f'x:{dx:.1f},skewX:{sk:.1f},textShadow:"-{sp:.1f}px 0 rgba(255,40,70,.85), {sp:.1f}px 0 rgba(40,220,255,.8)"')
    setp(sel, t + n / 30, 'x:0,skewX:0,textShadow:"0 4px 30px rgba(0,0,0,.6)"')
    ev(t, "glitch")


# the film layer: a red vignette that breathes in the hook and beats with the heart after Enter, film flicker,
# scratches and dust; and a spider that drops on its thread in the attic
SPIDER_LEGS = "".join(f'<path d="{d}"/>' for d in ("M29 36 Q14 22 5 30", "M28 42 Q10 37 2 46", "M28 48 Q10 54 4 64", "M30 54 Q18 68 12 78"))
FX = ('<div class="vig" id="vig"></div><div class="flick" id="flick"></div>' +
      "".join(f'<i class="scr" id="scr{i}"></i>' for i in range(3)) + "".join(f'<i class="dust" id="du{i}"></i>' for i in range(6)) +
      '<div id="spider"><i class="thr" id="thr"></i><svg id="spb" viewBox="0 0 72 80" width="72" height="80">'
      f'<g id="lgL" fill="none" stroke="#E8DCCB" stroke-width="3" stroke-linecap="round">{SPIDER_LEGS}</g>'
      f'<g transform="translate(72 0) scale(-1 1)"><g id="lgR" fill="none" stroke="#E8DCCB" stroke-width="3" stroke-linecap="round">{SPIDER_LEGS}</g></g>'
      '<ellipse cx="36" cy="48" rx="13" ry="16" fill="#241A20" stroke="#E8DCCB" stroke-width="2.5"/>'
      '<circle cx="36" cy="28" r="9" fill="#241A20" stroke="#E8DCCB" stroke-width="2.5"/>'
      '<circle cx="32.5" cy="27" r="2.4" fill="#FF4A3A"/><circle cx="39.5" cy="27" r="2.4" fill="#FF4A3A"/></svg></div>')


def fx_tl():
    r = random.Random(31)
    p = T["press"]
    # the vignette: slow breathing before Enter, the heartbeat after it
    n = max(1, int(p / .9) - 1)
    add(f'tl.fromTo("#vig",{{opacity:0}},{{opacity:.35,duration:.9,yoyo:true,repeat:{n},ease:"sine.inOut",immediateRender:false}},0);')
    for u in T["hb"]:
        add(f'tl.to("#vig",{{opacity:1,duration:.05}},{u:.3f});tl.to("#vig",{{opacity:.55,duration:.12}},{u + .05:.3f});'
            f'tl.to("#vig",{{opacity:.85,duration:.04}},{u + .18:.3f});tl.to("#vig",{{opacity:.4,duration:.3}},{u + .22:.3f});')
    to("#vig", SC[2][0] - .25, "opacity:0", .4)
    # flicker: a dark frame or two every second or so
    t = .4
    while t < SC[7][0] + .5:
        add(f'tl.set("#flick",{{opacity:{r.uniform(.08, .2):.2f}}},{t:.3f});tl.set("#flick",{{opacity:0}},{t + r.choice((1, 2)) / 30:.3f});')
        t += r.uniform(.7, 1.9)
    # scratches: short bursts, a new position every few frames
    for i in range(3):
        t, on = r.uniform(0, 2), False
        while t < DUR - .5:
            if r.random() < .3:
                add(f'tl.set("#scr{i}",{{x:{r.uniform(40, 1040):.0f},opacity:{r.uniform(.25, .6):.2f},scaleX:{r.choice((1, 1, 2))}}},{t:.3f});')
                on = True
            elif on:
                setp(f"#scr{i}", t, "opacity:0"); on = False
            t += r.choice((2, 3, 4)) / 30
        if on:
            setp(f"#scr{i}", t, "opacity:0")
    # dust: a speck for two frames
    for i in range(6):
        t = r.uniform(0, 1.5)
        while t < DUR - .3:
            sz = r.uniform(.6, 2.2)
            add(f'tl.set("#du{i}",{{x:{r.uniform(20, 1060):.0f},y:{r.uniform(80, 1840):.0f},scale:{sz:.2f},opacity:{r.uniform(.4, .9):.2f}}},{t:.3f});'
                f'tl.set("#du{i}",{{opacity:0}},{t + 2 / 30:.3f});')
            t += r.uniform(.5, 1.6)
    # the spider: drops into the attic scene, sways, climbs back when step 1 starts
    a, up = SC[2][0] + .35, SC[3][0] + .45
    add(f'tl.fromTo("#thr",{{scaleY:0}},{{scaleY:.72,duration:.75,ease:"back.out(1.4)",immediateRender:false}},{a:.3f});')
    add(f'tl.fromTo("#spb",{{y:0}},{{y:720,duration:.75,ease:"back.out(1.4)",immediateRender:false}},{a:.3f});')
    sway = up - a - .8
    add(f'tl.fromTo("#spider",{{rotation:-3}},{{rotation:3,duration:.8,yoyo:true,repeat:{max(1, int(sway / .8) - 1)},ease:"sine.inOut",immediateRender:false}},{a + .75:.3f});')
    for g, k in (("#lgL", 1), ("#lgR", -1)):
        for t0, d in ((a, .75), (up, .45)):
            add(f'tl.fromTo("{g}",{{rotation:0}},{{rotation:{8 * k},svgOrigin:"36 44",duration:.07,yoyo:true,repeat:{int(d / .07) // 2 * 2 + 1},ease:"none",immediateRender:false}},{t0:.3f});')
    add(f'tl.to("#thr",{{scaleY:0,duration:.45,ease:"power3.in"}},{up:.3f});')
    add(f'tl.to("#spb",{{y:0,duration:.45,ease:"power3.in"}},{up:.3f});')
    ev(a, "spider"); ev(up, "skitter")
    # glitches: Enter, the dead backups, the twist
    glitch("#s1 .hl", p + .03)
    glitch("#s2 .hl", T["dead"] - .02, 6)
    glitch("#s7 .hl", SC[6][0] + .55, 6)


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
                f'tl.set("#w{ci}_{k}",{{backgroundColor:"rgba(212,92,64,0)",color:"{CREAM}"}},{end - .02:.3f});')
    return "".join(html)


CSS = f"""
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }}
@font-face {{ font-family: "ISerif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 400; src: url("assets/fonts/JetBrainsMono-Regular.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #070a14; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #070a14; font-family: "Manrope", sans-serif; color: {CREAM}; }}
.clip {{ position: absolute; inset: 0; }}
#gl {{ width: 1080px; height: 1920px; display: block; }}
.mono {{ font-family: "JBMono", monospace; }}
.scrim {{ position: absolute; left: 0; right: 0; }}
.scrim.top {{ top: 0; height: 720px; background: linear-gradient(180deg, rgba(5,6,12,.92) 0%, rgba(5,6,12,.75) 45%, rgba(5,6,12,0) 100%); }}
.scrim.bot {{ bottom: 0; height: 760px; background: linear-gradient(0deg, rgba(5,6,12,.9) 0%, rgba(5,6,12,.62) 40%, rgba(5,6,12,0) 100%); }}
.top {{ position: absolute; left: 70px; right: 70px; top: 262px; display: flex; justify-content: space-between; align-items: center; }}
.brand {{ font: 700 30px "JBMono"; letter-spacing: 4px; color: {CREAM}; display: flex; align-items: center; gap: 14px; }}
.brand i {{ width: 18px; height: 18px; border-radius: 50%; background: {CORAL}; box-shadow: 0 0 14px {CORAL}; }}
.prog {{ width: 220px; height: 26px; border-radius: 13px; border: 3px solid {CREAM}; overflow: hidden; }}
.prog i {{ display: block; width: 100%; height: 100%; background: {CORAL}; transform-origin: 0 50%; transform: scaleX(0); }}
.hl {{ position: absolute; left: 70px; right: 70px; top: 340px; text-shadow: 0 4px 30px rgba(0,0,0,.6); }}
.kick {{ display: flex; align-items: center; gap: 18px; margin-bottom: 14px; font: 700 28px "JBMono"; letter-spacing: 4px; color: #FF9A7F; }}
.segs {{ display: flex; gap: 8px; }} .segs i {{ width: 54px; height: 10px; border-radius: 5px; background: rgba(241,233,220,.25); }} .segs i.on {{ background: {CORAL}; }}
.l1 {{ font: 800 76px/1.05 "Manrope"; letter-spacing: -2.5px; color: {CREAM}; }}
.hw {{ display: inline-block; }}
.acc {{ display: inline-block; font: 400 128px/1 "ISerif"; font-style: italic; color: #FF8A6E; letter-spacing: -1px; }}
.card {{ position: absolute; background: {CARD}; border: 3px solid {CARD_B}; border-radius: 28px; box-shadow: 0 24px 60px rgba(0,0,0,.5); color: {INK}; }}
.lab {{ font: 700 28px "JBMono"; letter-spacing: 3px; color: #8A7F70; }}
.chip {{ display: inline-block; padding: 8px 18px; border-radius: 30px; font: 700 28px "JBMono"; letter-spacing: 2px; color: #fff; }}
.chip.red {{ background: {RED}; }} .chip.amber {{ background: {AMBER}; color: {INK}; }} .chip.green {{ background: {GREEN}; }}
.chip.big {{ position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1180px; font-size: 32px; padding: 14px 28px; box-shadow: 0 12px 30px rgba(0,0,0,.5); }}
/* S1 */
.term {{ position: absolute; left: 110px; top: 1090px; width: 860px; height: 200px; border-radius: 24px; background: {TERM}; overflow: hidden;
  border: 2px solid #3A3842; box-shadow: 0 24px 60px rgba(0,0,0,.6); }}
.bar {{ height: 58px; display: flex; align-items: center; gap: 12px; padding: 0 24px; background: #26252C; }}
.bar i {{ width: 16px; height: 16px; border-radius: 50%; background: #4A4852; }} .bar i:first-child {{ background: {RED}; }}
.bar span {{ margin-left: 12px; font: 400 28px "JBMono"; color: #A9A4B4; }}
.ptag {{ margin-left: auto; padding: 4px 14px; border-radius: 10px; background: {RED}; font: 700 28px "JBMono"; letter-spacing: 2px; color: #fff; }}
.tl {{ padding: 36px 30px; font: 700 48px "JBMono"; color: #F4EEE6; white-space: nowrap; }}
.ch {{ opacity: 0; }}
.cur {{ display: inline-block; width: 24px; height: 50px; margin-left: 4px; vertical-align: -8px; background: #F4EEE6; }}
.stamp {{ position: absolute; right: 40px; top: 70px; opacity: 0; padding: 4px 24px; border: 8px solid {RED}; border-radius: 16px; color: {RED};
  font: 800 72px/1.1 "Manrope"; letter-spacing: 2px; transform: rotate(-8deg); background: rgba(255,250,245,.94); }}
#stamp1 {{ right: 150px; top: 1160px; }}   /* outside the terminal so it can overhang its edge */
.stamp.big {{ right: auto; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1080px; font-size: 96px; }}
/* S2 */
.cnt {{ left: 210px; top: 1060px; width: 660px; height: 250px; padding: 30px 38px; }}
.num {{ margin-top: 8px; font: 800 100px/1 "Manrope"; letter-spacing: -4px; }}
.drain {{ margin-top: 22px; height: 20px; border-radius: 10px; background: #EFE6D8; overflow: hidden; }}
.drain i {{ display: block; height: 100%; width: 100%; background: {RED}; transform-origin: 0 50%; }}
/* S3 */
.snap {{ left: 110px; top: 1080px; width: 860px; height: 200px; padding: 26px 34px; display: flex; align-items: center; gap: 26px; border: 5px solid {CORAL};
  box-shadow: 0 0 60px rgba(232,115,90,.55), 0 24px 60px rgba(0,0,0,.5); }}
.dbi {{ width: 84px; height: 100px; border-radius: 42px / 16px; border: 6px solid {INK}; background: #FBE3DD; }}
.big2 {{ font-size: 42px; font-weight: 700; }}
.sub {{ margin-top: 6px; font: 600 32px "Manrope"; color: #6E6458; }}
.ok {{ margin-left: auto; }}
.steps {{ position: absolute; left: 0; right: 0; top: 1110px; display: flex; justify-content: center; gap: 60px; }}
.st {{ width: 130px; height: 130px; border-radius: 50%; background: {CREAM}; color: {INK}; display: flex; align-items: center; justify-content: center;
  font: 400 96px/1 "ISerif"; font-style: italic; box-shadow: 0 16px 40px rgba(0,0,0,.5); }}
.st:nth-child(1) {{ background: {CORAL_T}; color: #fff; }}
/* S4 */
.chipcmd {{ position: absolute; left: 70px; top: 1250px; padding: 16px 24px; border-radius: 18px; background: {CREAM}; color: {INK}; font: 700 32px "JBMono";
  white-space: nowrap; box-shadow: 0 12px 30px rgba(0,0,0,.5); }}
.chipcmd b {{ color: {CORAL_T}; }}
.chipcmd.red {{ background: {RED}; color: #fff; top: 1235px; left: 90px; font-size: 34px; }}
.polaroid {{ position: absolute; left: 600px; top: 960px; width: 340px; padding: 16px 16px 0; background: #FBF8F2; border-radius: 8px; box-shadow: 0 24px 60px rgba(0,0,0,.6);
  transform: rotate(4deg); }}
.pimg {{ position: relative; height: 200px; border-radius: 4px; background: linear-gradient(180deg, #2a3a30, #1a2420); overflow: hidden; }}
.pimg i {{ position: absolute; width: 10px; height: 16px; border-radius: 50% 50% 40% 40%; background: #FFC070; box-shadow: 0 0 10px #FFB050, 0 0 22px rgba(255,170,80,.6); }}
.pcap {{ display: flex; align-items: center; justify-content: center; gap: 10px; height: 64px; font: 700 28px "JBMono"; color: {INK}; }}
/* S6 */
.sess {{ left: 70px; top: 1060px; width: 940px; height: 230px; padding: 28px 36px; }}
.shead {{ display: flex; align-items: center; gap: 14px; font: 700 28px "JBMono"; letter-spacing: 3px; color: #8A7F70; }}
.shead i {{ width: 16px; height: 16px; border-radius: 50%; background: {CORAL}; }}
.srow {{ position: absolute; left: 36px; right: 36px; top: 110px; display: flex; align-items: center; gap: 22px; font: 700 44px "Manrope"; letter-spacing: -1px; }}
.srow .chip {{ font-size: 30px; padding: 10px 20px; }}
/* S7 */
.denied {{ position: absolute; left: 70px; padding: 12px 22px; border-radius: 14px; background: {RED}; color: #fff; font: 700 32px "JBMono";
  box-shadow: 0 12px 30px rgba(0,0,0,.5); }}
#d0 {{ top: 1060px; }} #d1 {{ top: 1150px; left: 300px; }} #d2 {{ top: 1240px; left: 160px; }}
/* S8 */
.cta {{ position: absolute; left: 0; right: 0; top: 340px; text-align: center; }}
.cchip {{ display: inline-block; padding: 12px 30px; border-radius: 40px; background: {CREAM}; color: {INK}; font: 700 34px "JBMono"; letter-spacing: 8px; }}
.cword {{ margin: 22px auto 0; display: table; padding: 10px 48px 22px; border-radius: 40px; background: {CORAL_T}; color: #fff; font: 800 150px/1.05 "Manrope"; letter-spacing: -3px;
  box-shadow: 0 18px 0 {CORAL_D}, 0 0 80px rgba(232,115,90,.5); }}
.cbox {{ left: 70px; top: 700px; width: 940px; height: 132px; padding: 0 26px; display: flex; align-items: center; gap: 22px; border-radius: 66px; }}
.av {{ width: 76px; height: 76px; border-radius: 50%; background: linear-gradient(135deg, {CORAL}, {AMBER}); }}
.ctext {{ flex: 1; font: 800 54px "Manrope"; letter-spacing: 2px; }}
.cc {{ opacity: 0; }}
.ccur {{ display: inline-block; width: 4px; height: 52px; background: {CORAL}; vertical-align: -6px; margin-left: 4px; }}
.send {{ width: 88px; height: 88px; border-radius: 50%; background: {CORAL_T}; display: flex; align-items: center; justify-content: center; }}
.pdf {{ position: absolute; left: 110px; top: 880px; width: 300px; }}
.pdf img {{ width: 300px; height: 424px; display: block; border-radius: 14px; box-shadow: 0 26px 60px rgba(0,0,0,.6); }}
.pdftag {{ position: absolute; left: 120px; top: -30px; padding: 10px 20px; border-radius: 30px; background: {GREEN}; color: #fff; font: 700 28px "JBMono"; letter-spacing: 2px;
  white-space: nowrap; transform: rotate(4deg); }}
/* film layer */
.vig {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse 80% 62% at 50% 50%, rgba(90,0,0,0) 52%, rgba(120,6,6,.6) 100%); }}
.flick {{ position: absolute; inset: 0; opacity: 0; background: #000; }}
.scr {{ position: absolute; left: 0; top: 0; width: 2px; height: 1920px; opacity: 0;
  background: linear-gradient(180deg, rgba(241,233,220,0), rgba(241,233,220,.5) 15%, rgba(241,233,220,.3) 70%, rgba(241,233,220,0)); }}
.dust {{ position: absolute; left: 0; top: 0; width: 5px; height: 5px; border-radius: 50%; opacity: 0; background: rgba(241,233,220,.8); }}
#spider {{ position: absolute; left: 984px; top: 0; width: 72px; height: 1px; transform-origin: 36px 0; }}
.thr {{ position: absolute; left: 35px; top: 0; width: 2px; height: 1000px; background: rgba(241,233,220,.6); transform-origin: 50% 0; transform: scaleY(0); }}
#spb {{ position: absolute; left: 0; top: -82px; }}
/* captions */
.cap {{ position: absolute; left: 60px; right: 60px; top: 1330px; text-align: center; opacity: 0; font: 800 60px/1.25 "Manrope"; letter-spacing: -1px; color: {CREAM};
  text-shadow: 0 3px 16px rgba(0,0,0,.7); }}
.cw {{ display: inline-block; padding: 2px 12px 6px; border-radius: 16px; }}
"""


def main():
    s1_tl(); s2_tl(); s3_tl(); s4_tl(); s5_tl(); s6_tl(); s7_tl(); s8_tl(); fx_tl()
    sids = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
    for k, sid in enumerate(sids):
        scene_tl(k, sid)
    caps = captions()
    add(f'tl.to(".prog i",{{scaleX:1,duration:{DUR},ease:"none"}},0);')
    A.insert(0, "      gsap.set(" + json.dumps(list(dict.fromkeys(HIDE))) + ",{opacity:0});")
    scenes = "".join(scene(k, sid, html) for k, (sid, html) in enumerate(zip(sids, [S1, S2, S3, S4, S5, S6, S7, S8])))
    has_mix = os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav"))
    has_vo = os.path.exists(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    audio = (f'<audio id="mix" src="assets/audio/{"mix" if has_mix else "voice"}.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>'
             if has_mix or has_vo else "")
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Haunted database explainer 9x16</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"></canvas>
      <div id="scrims" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore><div class="scrim top"></div><div class="scrim bot"></div></div>
      {scenes}
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5" data-layout-ignore>{FX}</div>
      <div id="chrome" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6"><div class="top"><div class="brand"><i></i>AI.NXTLVL</div><div class="prog"><i></i></div></div></div>
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7">{caps}</div>
      {audio}
    </div>
    <script>
      window.HH_T = {json.dumps(T)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/world.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    T["ev"] = sorted(EV)
    json.dump(T, open(os.path.join(B, "cues.json"), "w"), indent=1)
    print(f"wrote index.html {len(html) // 1024} KB, {DUR} s, {len(EV)} sound events, audio: {'mix' if has_mix else 'voice' if has_vo else 'none'}")


if __name__ == "__main__":
    main()
