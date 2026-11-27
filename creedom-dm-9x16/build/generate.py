"""Creedom "The DM you'll get? I didn't send it." (9:16, playbook script 4, keyword DM): writes index.html, plan/sfx_events.json, plan/edit.json.
Voice: the owner's ElevenLabs take (voice "Lima", Eleven v4), used exactly as recorded (loudness only). No music.
The CTA is the demo: comment DM and Creedom's own Comments-to-DM automation replies. A 5-step tracker (COMMENT / DM / STORY /
LIVE / STARTERS) ticks as each trigger is shown; logs and handles are illustrations, labelled EXAMPLE.
python3 build/generate.py"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import ROOT, LINES, L0, L1, T, JS, SFX, js, sfx, ft, to, st  # noqa: E402
from fx import cree_html, pose, cree_hop, sparkle, P, sweat, say, cree_wiggle, blink, PCX, PCY, cree_to  # noqa: E402

random.seed(9)
DUR = round(L1["d9"] + 1.4, 2)
HTMLS, OPEN, WID, FIRST = [], [None], [0], {}


def ft2(sel, t, d, frm, to_, ease="power3.out"):
    ft(sel, t, d, frm, to_, ease)
    if "opacity: 0" in frm and (sel not in FIRST or t < FIRST[sel][0]):
        FIRST[sel] = (t, frm)


def pop(sel, t, d=.32, frm="{opacity: 0, scale: .4}", ease="back.out(2.4)"):
    ft2(sel, t, d, frm, "{opacity: 1, scale: 1, rotation: 0}", ease)


def head(hid, rows, line, size=80, after=0.0):
    spoken, k, out_, rws = [w for w in LINES[line] if w["t0"] >= after - 1e-3], 0, [], []
    for row in rows:
        ws = []
        for word in row:
            cls = "pk" if word.startswith("*") else ""
            word = word.lstrip("*")
            WID[0] += 1
            wid = f"h{WID[0]}"
            key, t = word.lower().strip(".,:!?\""), None
            while k < len(spoken):
                sw = spoken[k]["w"].lower().strip(".,:!?\"")
                k += 1
                if sw.startswith(key[:4]) or key.startswith(sw[:4]):
                    t = spoken[k - 1]["t0"]
                    break
            t = spoken[-1]["t0"] if t is None else t
            ws.append(f'<span class="hw {cls}" id="{wid}">{word}</span>')
            out_.append((wid, t))
        rws.append(f'<div class="hl">{" ".join(ws)}</div>')
    HTMLS.append(f'<div class="head" id="{hid}" style="font-size:{size}px">{"".join(rws)}</div>')
    for wid, t in out_:
        ft2(f"#{wid}", t - .05, .26, "{opacity: 0, filter: 'blur(10px)', y: 24}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
    first = min(t for _, t in out_)
    if OPEN[0]:
        to(f"#{OPEN[0]}", first - .18, .14, "{opacity: 0, filter: 'blur(12px)', y: -30}", "power2.in")
    OPEN[0] = hid


def flash(t, o=.5, d=.25, col="#fff"):
    js(f'tl.set("#flash", {{background: "{col}", opacity: {o}}}, {t:.3f});')
    to("#flash", t + .02, d, "{opacity: 0}", "power2.out")


def punch(t, k=1.04):
    js(f'tl.fromTo("#stage", {{scale: 1}}, {{scale: {k}, duration: .1, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t:.3f});')


SC = []


def scene(sid, t, frm="{opacity: 0, scale: 1.06}"):
    for s in SC:
        if s != sid:
            to(f"#{s}", t - .12, .14, "{opacity: 0}", "power1.in")
    ft2(f"#{sid}", t, .3, frm, "{opacity: 1, scale: 1, x: 0, y: 0}", "power3.out")


BURST = [0]


def burst(t, x, y, cols=("#2fbf71", "#F343A2", "#ffd23f", "#ffffff"), n=14, r=(90, 190)):
    """a ring of particles exploding out from (x, y)"""
    BURST[0] += 1
    b = BURST[0]
    for k in range(n):
        a = 2 * math.pi * k / n + random.uniform(-.2, .2)
        d = random.uniform(*r)
        sz = random.randint(10, 20)
        HTMLS.append(f'<i class="pt" id="pt{b}_{k}" style="left:{x - sz / 2:.0f}px;top:{y - sz / 2:.0f}px;width:{sz}px;height:{sz}px;'
                     f'background:{random.choice(cols)};border-radius:{random.choice(("50%", "4px"))}"></i>')
        js(f'tl.fromTo("#pt{b}_{k}", {{opacity: 1, x: 0, y: 0, scale: 1.2, rotation: 0}}, {{opacity: 0, x: {math.cos(a) * d:.0f}, y: {math.sin(a) * d:.0f}, scale: .3, '
           f'rotation: {random.randint(-180, 180)}, duration: .6, ease: "power3.out", immediateRender: false}}, {t:.3f});')
    HTMLS.append(f'<i class="rip" id="rip{b}" style="left:{x - 60}px;top:{y - 60}px"></i>')
    js(f'tl.fromTo("#rip{b}", {{opacity: .9, scale: .2}}, {{opacity: 0, scale: 2.2, duration: .55, ease: "power2.out", immediateRender: false}}, {t:.3f});')


def shake(t, a=14):
    js(f'tl.fromTo("#stage", {{x: 0}}, {{keyframes: [{{x: {-a}, duration: .04}}, {{x: {a}, duration: .05}}, {{x: {-a * .6:.0f}, duration: .05}}, {{x: {a * .4:.0f}, duration: .05}}, {{x: 0, duration: .05}}], immediateRender: false}}, {t:.3f});')


BADGE_XY = {"ob0": (1000, 742), "ob1": (1022, 1168), "ob2": (948, 658), "ob3": (788, 658)}


def badge(bid, ok, t):
    pop(f"#{bid}", t, .32, "{opacity: 0, scale: 2.2, rotation: -25}")
    sfx("ding" if ok else "error", t)
    if ok and bid in BADGE_XY:
        burst(t + .05, *BADGE_XY[bid])
    if not ok:
        shake(t)


CHECK_SVG = '<svg viewBox="0 0 48 48"><path d="M12 25 L21 34 L37 15" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
X_SVG = '<svg viewBox="0 0 48 48"><path d="M14 14 L34 34 M34 14 L14 34" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>'
OK = lambda i: f'<i class="okb" id="{i}">{CHECK_SVG}</i>'
NO = lambda i: f'<i class="nob" id="{i}">{X_SVG}</i>'
AVATAR = ('<svg class="avs" viewBox="0 0 200 260"><circle cx="100" cy="92" r="52" fill="#ffd9c2"/><path d="M48 80 Q52 30 100 32 Q150 30 152 82 Q140 56 100 58 Q62 56 48 80 Z" fill="#3a2440"/>'
          '<circle cx="82" cy="94" r="6" fill="#1a1020"/><circle cx="118" cy="94" r="6" fill="#1a1020"/><ellipse class="mouth" cx="100" cy="120" rx="12" ry="6" fill="#b0405e"/>'
          '<path d="M30 260 Q34 170 100 166 Q166 170 170 260 Z" fill="#F343A2"/></svg>')

# ---------------------------------------------------------------- times
def W(line, word, n=0):
    return T(line, word, n)


t0 = dict(dm=W("d0", "DM"), reel=W("d0", "reel"), msg=W("d0", "message"), ten=W("d0", "ten"), idid=W("d0", "didn't"), send=W("d0", "send"))
t1 = dict(t=L0["d1"], cr=W("d1", "Creedom"), did=W("d1", "did"), set=W("d1", "set"), rule=W("d1", "rule"), once=W("d1", "once"))
t2 = dict(t=L0["d2"], one=W("d2", "one"), five=W("d2", "five"), places=W("d2", "places"), rep=W("d2", "replies"))
TR = [dict(n=L0[k], a=W(k, a), b=W(k, b)) for k, a, b in (("d3", "Someone", "link"), ("d4", "Someone", "instant"), ("d5", "They", "answers"),
                                                           ("d6", "Everyone", "message"), ("d7", "Questions", "chat"))]
t8 = dict(t=L0["d8"], logged=W("d8", "logged"), tap=W("d8", "tap"), pauses=W("d8", "pauses"), runs=W("d8", "runs"), meta=W("d8", "Meta's"))
t9 = dict(t=L0["d9"], dm=W("d9", "DM"), now=W("d9", "now"), watch=W("d9", "watch"), inbox=W("d9", "inbox"))
TICK = [TR[0]["b"] + .3, TR[1]["b"] + .4, TR[2]["b"] + .3, TR[3]["b"] + .3, W("d7", "chat") + .2]

# ---------------------------------------------------------------- captions
head("h0", [["*Comment", "*DM", "on"], ["this", "reel."]], "d0", 96)
head("h0b", [["The", "message", "you", "get"], ["in", "*ten", "*seconds?"]], "d0", 84, after=t0["msg"] - .25)
head("h0c", [["I", "*didn't", "send", "it."]], "d0", 100, after=t0["idid"] - .25)
head("h1", [["A", "tool", "called"], ["*Creedom", "did."]], "d1", 96)
head("h1b", [["I", "set", "the", "rule"], ["*once."]], "d1", 96, after=t1["set"] - .1)
head("h2", [["And", "comments", "are", "only"], ["one", "of", "*five", "places"], ["it", "replies."]], "d2", 80)
head("h3", [["Someone", "comments"], ["a", "word,", "they", "get"], ["the", "*link."]], "d3", 82, after=TR[0]["a"])
head("h4", [["Someone", "messages"], ["a", "word,"], ["*instant", "*reply."]], "d4", 82, after=TR[1]["a"])
head("h5", [["They", "reply", "to", "your"], ["story,", "it", "*answers."]], "d5", 86, after=TR[2]["a"])
head("h6", [["Everyone", "who"], ["comments", "on", "your"], ["Live", "gets", "a", "*message."]], "d6", 80, after=TR[3]["a"])
head("h7", [["Questions", "people", "*tap"], ["to", "start", "a", "*chat."]], "d7", 86, after=TR[4]["a"])
head("h8", [["Every", "send", "is", "*logged."]], "d8", 90)
head("h8b", [["One", "*tap", "pauses", "it."]], "d8", 90, after=t8["tap"] - .2)
head("h8c", [["And", "it", "runs", "through"], ["*Meta's", "*own", "*platform."]], "d8", 84, after=W("d8", "And"))
head("h9", [["Comment", "*DM", "right", "now"], ["and", "watch", "your", "*inbox."]], "d9", 88)

# ---------------------------------------------------------------- the 5-step tracker
NAMES = ["COMMENT", "DM", "STORY", "LIVE", "STARTERS"]
TRK = '<div id="trk">' + "".join(f'<div class="tc" id="tc{i}"><i class="box" id="tb{i}"><u id="tk{i}">{CHECK_SVG}</u></i><b>{n}</b></div>' for i, n in enumerate(NAMES)) + '</div>'
pop("#trk", t2["five"], .35, "{opacity: 0, y: -20, scale: .8}")
for i in range(5):
    pop(f"#tc{i}", t2["five"] + .08 + i * .09, .3, "{opacity: 0, scale: .4}")
    sfx("pop", t2["five"] + .08 + i * .09)
    js(f'tl.to("#tc{i}", {{scale: 1.1, backgroundColor: "#1a1020", color: "#ffffff", duration: .2, ease: "back.out(3)"}}, {TR[i]["n"]:.3f});')
    pop(f"#tk{i}", TICK[i], .3, "{opacity: 0, scale: 2.4, rotation: -30}")
    js(f'tl.to("#tc{i}", {{scale: 1, backgroundColor: "#2fbf71", color: "#ffffff", duration: .25}}, {TICK[i]:.3f});')
    js(f'tl.to("#tb{i}", {{backgroundColor: "#ffffff", borderColor: "#ffffff", duration: .2}}, {TICK[i]:.3f});')
    sfx("coin", TICK[i])
    burst(TICK[i] + .05, (190, 362, 520, 668, 852)[i], 489, n=10, r=(50, 110))
to("#trk", t9["t"] - .2, .25, "{opacity: 0, y: -30}", "power2.in")

ENV = '<svg viewBox="0 0 64 48" class="env"><rect x="2" y="2" width="60" height="44" rx="8" fill="#fff" stroke="#1a1020" stroke-width="4"/><path d="M4 6 L32 28 L60 6" fill="none" stroke="#1a1020" stroke-width="4"/></svg>'
PLANE = '<svg viewBox="0 0 48 48" class="plane"><path d="M4 22 L44 4 L30 44 L22 28 Z" fill="#fff" stroke="#1a1020" stroke-width="3" stroke-linejoin="round"/></svg>'
LOGO = '<img class="clogo2" src="assets/img/creedom_logo.png" alt="">'
AV = lambda c="#ffb3d6": f'<i class="av" style="background:{c}"></i>'

# =====================================================================================================================
# s0: comment typed, the DM lands, the 10-second ring, "not me"
S0 = ('<div class="scene" id="s0" style="opacity:1"><div class="post" id="post0"><div class="rthumb"><i class="dish"></i><b>3 meals under 100</b></div>'
      '<div class="csheet"><small>Comments</small><div class="cmt" id="cmt0">' + AV("#c9b3ff") + '<b>you</b><span>DM</span></div>'
      '<div class="cin">' + AV("#c9b3ff") + '<span id="cin">' + "".join(f'<u id="ct{k}" style="opacity:0">{c}</u>' for k, c in enumerate("DM")) + '</span><em id="cpost">Post</em></div></div></div>'
      '<div class="notif" id="notif">' + LOGO + '<div><b>creedom.ai</b><span>Here\'s your link. Tap to open.</span></div><small>now</small></div>'
      '<div class="ring10" id="ring10"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" fill="#fff" stroke="#f3d6e6" stroke-width="16"/>'
      '<circle id="r10" cx="100" cy="100" r="86" fill="none" stroke="#F343A2" stroke-width="16" stroke-linecap="round" pathLength="1" stroke-dasharray="1" transform="rotate(-90 100 100)"/></svg>'
      '<b id="r10n">10</b><small>SEC</small></div>'
      '<div class="sender" id="sender"><small>SENT BY</small><b id="sq">?</b></div><div class="notme" id="notme"><span>NOT ME</span></div></div>')
SC.append("s0")
ft2("#post0", 0, .01, "{opacity: 0}", "{opacity: 1}")
js('gsap.set("#post0", {opacity: 1});')
for k in range(2):
    st(f"#ct{k}", t0["dm"] + k * .12, "{opacity: 1}")
    sfx("typing", t0["dm"] + k * .12)
js(f'tl.fromTo("#cpost", {{scale: 1}}, {{keyframes: [{{scale: .8, duration: .08}}, {{scale: 1, duration: .14}}], immediateRender: false}}, {t0["reel"]:.3f});')
sfx("click", t0["reel"])
ft2("#cmt0", t0["reel"] + .1, .35, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(2)")
js(f'tl.set("#ct0, #ct1", {{opacity: 0}}, {t0["reel"] + .1:.3f});')
ft2("#notif", t0["msg"] - .1, .45, "{opacity: 0, y: -260}", "{opacity: 1, y: 0}", "back.out(1.6)")
sfx("msg", t0["msg"] - .05); punch(t0["msg"], 1.03)
js(f'tl.fromTo("#notif", {{rotation: -1.5}}, {{rotation: 1.5, duration: .12, yoyo: true, repeat: 3, immediateRender: false}}, {t0["msg"] + .35:.3f});')
pop("#ring10", t0["ten"] - .1, .35, "{opacity: 0, scale: .3, rotation: -60}")
js(f'tl.fromTo("#r10", {{strokeDashoffset: 0}}, {{strokeDashoffset: 1, duration: {t0["idid"] - t0["ten"]:.2f}, ease: "none", immediateRender: false}}, {t0["ten"]:.3f});')
js(f'(() => {{ const o = {{v: 10}}; tl.to(o, {{v: 0, duration: {t0["idid"] - t0["ten"]:.2f}, ease: "none", onUpdate: () => {{ document.getElementById("r10n").textContent = Math.ceil(o.v); }}}}, {t0["ten"]:.3f}); }})();')
for k in range(4):
    sfx("tick", t0["ten"] + k * .25)
pop("#sender", t0["idid"] - .15, .35, "{opacity: 0, scale: .4, x: -60}")
js(f'tl.fromTo("#sq", {{scale: 1}}, {{scale: 1.4, duration: .15, yoyo: true, repeat: 3, immediateRender: false}}, {t0["idid"] + .1:.3f});')
ft2("#notme", t0["send"], .22, "{opacity: 0, scale: 2.6, rotation: -24}", "{opacity: 1, scale: 1, rotation: -9}", "power4.out")
sfx("stamp", t0["send"] + .04); shake(t0["send"] + .04, 10)

# s1: Creedom did; the rule snaps together
S1 = ('<div class="scene" id="s1"><div class="crhero" id="crhero"><i class="glow"></i>' + LOGO + '<span>sent it for you</span></div>'
      '<div class="rule" id="rule"><small>THE RULE</small><div class="rrow">'
      '<span class="blk b0" id="rb0">IF a comment says</span><span class="blk b1" id="rb1">DM</span></div>'
      '<i class="rarr" id="rarr"></i><div class="rrow"><span class="blk b2" id="rb2">SEND</span><span class="blk b3" id="rb3">your link</span></div>'
      '<div class="once" id="once">SET ONCE</div></div></div>')
SC.append("s1")
scene("s1", t1["t"] - .1)
ft2("#crhero", t1["cr"] - .05, .45, "{opacity: 0, scale: 2.4}", "{opacity: 1, scale: 1}", "back.out(1.8)")
sfx("impact", t1["cr"]); sfx("whoosh_big", t1["cr"] - .15); flash(t1["cr"], .45); burst(t1["cr"] + .05, 540, 820, n=20, r=(160, 320))
js(f'tl.to("#crhero", {{y: -170, scale: .62, duration: .4, ease: "power3.inOut"}}, {t1["set"] - .2:.3f});')
for k, tk in enumerate((t1["set"], t1["set"] + .22, t1["rule"], t1["rule"] + .2)):
    ft2(f"#rb{k}", tk, .3, "{opacity: 0, x: " + ("-220" if k % 2 == 0 else "220") + ", rotation: " + ("-8" if k % 2 == 0 else "8") + "}", "{opacity: 1, x: 0, rotation: 0}", "back.out(2.2)")
    sfx("snap", tk + .2)
ft2("#rule", t1["set"] - .05, .3, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.6)")
pop("#rarr", t1["rule"] - .05, .25, "{opacity: 0, scale: .3}")
ft2("#once", t1["once"], .22, "{opacity: 0, scale: 2.4, rotation: -18}", "{opacity: 1, scale: 1, rotation: -6}", "power4.out")
sfx("stamp", t1["once"] + .04); punch(t1["once"] + .04, 1.03)

# s2: five places, a hub with spokes
ICONS = {
    "COMMENT": '<path d="M10 12 H54 V40 H28 L16 52 V40 H10 Z" fill="none" stroke="#1a1020" stroke-width="5" stroke-linejoin="round"/>',
    "DM": '<path d="M6 30 L58 8 L40 58 L30 36 Z" fill="none" stroke="#1a1020" stroke-width="5" stroke-linejoin="round"/>',
    "STORY": '<circle cx="32" cy="32" r="24" fill="none" stroke="#F343A2" stroke-width="5" stroke-dasharray="10 5"/><circle cx="32" cy="32" r="12" fill="#ffb3d6"/>',
    "LIVE": '<rect x="6" y="18" width="52" height="28" rx="8" fill="#ff3b4e"/><text x="32" y="38" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="16" fill="#fff">LIVE</text>',
    "STARTERS": '<rect x="6" y="10" width="40" height="14" rx="7" fill="#c9b3ff"/><rect x="14" y="28" width="44" height="14" rx="7" fill="#ffb3d6"/><rect x="6" y="46" width="30" height="12" rx="6" fill="#ffd27a"/>',
}
HUBPOS = [(540, 820), (860, 1000), (760, 1390), (320, 1390), (220, 1000)]
S2 = ('<div class="scene" id="s2"><svg class="spokes" viewBox="0 0 1080 1920">' + "".join(f'<line id="sp{i}" x1="540" y1="1130" x2="{x}" y2="{y}" stroke="#F343A2" stroke-width="6" stroke-dasharray="14 12" pathLength="1"/>' for i, (x, y) in enumerate(HUBPOS)) + '</svg>'
      + "".join(f'<i class="pulse" id="pl{i}"></i>' for i in range(5))
      + '<div class="hub" id="hub">' + LOGO + '</div>'
      + "".join(f'<div class="node" id="nd{i}" style="left:{x - 95}px;top:{y - 95}px"><svg viewBox="0 0 64 64">{ICONS[n]}</svg><b>{n}</b><em>{i + 1}</em></div>' for i, (n, (x, y)) in enumerate(zip(NAMES, HUBPOS)))
      + '</div>')
SC.append("s2")
scene("s2", t2["t"] - .1)
pop("#hub", t2["t"], .4, "{opacity: 0, scale: .3}")
pop("#nd0", t2["one"] - .05, .35)
sfx("pop", t2["one"])
js(f'tl.fromTo("#nd0", {{boxShadow: "0 0 0 0 rgba(243,67,162,.0)"}}, {{boxShadow: "0 0 0 18px rgba(243,67,162,.3)", duration: .3, yoyo: true, repeat: 3, immediateRender: false}}, {t2["one"]:.3f});')
for i in range(1, 5):
    pop(f"#nd{i}", t2["five"] + i * .1, .35)
    sfx("pop", t2["five"] + i * .1)
for i, (x, y) in enumerate(HUBPOS):
    ft2(f"#sp{i}", t2["places"] + i * .06, .35, "{strokeDashoffset: 1, opacity: 0}", "{strokeDashoffset: 0, opacity: 1}", "power2.out")
    js(f'tl.fromTo("#pl{i}", {{opacity: 1, x: 540, y: 1130, scale: 1}}, {{opacity: 1, x: {x}, y: {y}, scale: .6, duration: .5, repeat: 2, ease: "power1.in", immediateRender: false}}, {t2["rep"] - .2 + i * .05:.3f});')
js(f'gsap.set(".pulse", {{opacity: 0}}); tl.set(".pulse", {{opacity: 0}}, {TR[0]["n"] - .2:.3f});')
sfx("riser_short", t2["places"] - .1)


# check title cards (1 COMMENT -> DM ...)
def title(i, t, name):
    HTMLS.append(f'<div class="ttl" id="tt{i}"><i class="band"></i>' + "".join(f'<i class="stk" style="top:{20 + k * 52}px;width:{random.randint(180, 420)}px"></i>' for k in range(5))
                 + f'<b>{i + 1}</b><span>{name}</span></div>')
    js(f'tl.fromTo("#tt{i} .stk", {{x: -500}}, {{x: 1400, duration: .55, stagger: .04, ease: "power2.in", immediateRender: false}}, {t - .05:.3f});')
    js(f'tl.fromTo("#tt{i} .band", {{scaleX: 0}}, {{scaleX: 1, duration: .25, ease: "power3.out", immediateRender: false}}, {t - .05:.3f});')
    ft2(f"#tt{i}", t - .05, .25, "{opacity: 0}", "{opacity: 1}", "power2.out")
    js(f'tl.fromTo("#tt{i} b", {{scale: 3, rotation: -15}}, {{scale: 1, rotation: 0, duration: .35, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#tt{i} span", {{x: 200, opacity: 0}}, {{x: 0, opacity: 1, duration: .3, ease: "power3.out", immediateRender: false}}, {t + .08:.3f});')
    to(f"#tt{i}", t + .75, .2, "{opacity: 0, scale: 1.2}", "power2.in")
    for sc_ in SC:
        js(f'tl.to("#{sc_}", {{opacity: 0, duration: .15}}, {t + .05:.3f});')
    sfx("whoosh", t - .05); sfx("impact", t); flash(t, .3)


# s3 COMMENT -> DM: the word flies along a dotted path into the inbox
S3 = ('<div class="scene" id="s3"><b class="ghost">1</b><div class="cpost" id="cp3"><div class="rthumb"><i class="dish"></i></div><div class="cb" id="cb3">' + AV("#c9b3ff") + '<span>DM</span></div></div>'
      '<svg class="path3" viewBox="0 0 1080 1920"><path id="pa3" d="M330 980 C 460 760, 700 760, 760 1060" fill="none" stroke="#F343A2" stroke-width="7" stroke-dasharray="4 18" stroke-linecap="round"/></svg>'
      '<div class="fly" id="fly3">DM</div><div class="inbox" id="ib3">' + ENV + '<b>INBOX</b></div>'
      '<div class="dmb" id="dm3">' + LOGO + '<p>Here\'s the link you asked for</p><span class="lnk" id="lk3">creedom.ai/start</span></div></div>')
SC.append("s3")
title(0, TR[0]["n"], "COMMENT TO DM")
scene("s3", TR[0]["n"] + .7)
ft2("#cp3", TR[0]["n"] + .75, .4, "{opacity: 0, x: -300}", "{opacity: 1, x: 0}", "back.out(1.5)")
ft2("#ib3", TR[0]["n"] + .85, .4, "{opacity: 0, x: 300}", "{opacity: 1, x: 0}", "back.out(1.5)")
pop("#cb3", TR[0]["a"], .3)
sfx("pop", TR[0]["a"])
ft2("#pa3", TR[0]["a"] + .2, .5, "{opacity: 0, strokeDashoffset: 200}", "{opacity: 1, strokeDashoffset: 0}", "power1.out")
js(f'tl.fromTo("#fly3", {{opacity: 1, x: 300, y: 950, scale: .6, rotation: -20}}, {{keyframes: [{{x: 520, y: 780, scale: 1.2, rotation: 0, duration: .4, ease: "power1.out"}}, '
   f'{{x: 730, y: 1030, scale: .4, rotation: 25, duration: .4, ease: "power1.in"}}, {{opacity: 0, duration: .05}}], immediateRender: false}}, {W("d3", "word") - .1:.3f});')
js(f'gsap.set("#fly3", {{opacity: 0}});')
sfx("sent", W("d3", "word"))
js(f'tl.fromTo("#ib3", {{scale: 1}}, {{scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false}}, {W("d3", "word") + .7:.3f});')
ft2("#dm3", W("d3", "get") - .1, .4, "{opacity: 0, y: 80, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
sfx("msg", W("d3", "get"))
pop("#lk3", TR[0]["b"] - .05, .3, "{opacity: 0, scale: 1.8}")
burst(TR[0]["b"] + .1, 540, 1500)

# s4 DM -> DM: keyword in, instant reply out, a lightning "0.4s"
S4 = ('<div class="scene" id="s4"><b class="ghost">2</b><div class="chat" id="chat4"><div class="chd">' + AV("#ffd27a") + '<b>maya</b><em>EXAMPLE</em></div>'
      '<div class="ub" id="ub4">PRICE</div><div class="typ" id="typ4"><i></i><i></i><i></i></div>'
      '<div class="ab" id="ab4">' + LOGO + '<p>Here are the plans, and the free one to start.</p></div></div>'
      '<div class="bolt" id="bolt4"><svg viewBox="0 0 60 100"><path d="M36 0 L4 58 H28 L20 100 L56 38 H32 Z" fill="#ffd23f" stroke="#1a1020" stroke-width="4" stroke-linejoin="round"/></svg><b>INSTANT</b></div></div>')
SC.append("s4")
title(1, TR[1]["n"], "DM TO DM")
scene("s4", TR[1]["n"] + .7)
ft2("#chat4", TR[1]["n"] + .75, .4, "{opacity: 0, y: 200}", "{opacity: 1, y: 0}", "back.out(1.5)")
ft2("#ub4", TR[1]["a"] + .1, .35, "{opacity: 0, x: 200, scale: .6}", "{opacity: 1, x: 0, scale: 1}", "back.out(2)")
sfx("sent", TR[1]["a"] + .1)
pop("#typ4", W("d4", "word") - .1, .2)
js(f'tl.fromTo("#typ4 i", {{y: 0}}, {{y: -12, duration: .14, yoyo: true, repeat: 3, stagger: .07, immediateRender: false}}, {W("d4", "word"):.3f});')
to("#typ4", TR[1]["b"] - .1, .1, "{opacity: 0}")
ft2("#ab4", TR[1]["b"], .35, "{opacity: 0, x: -200, scale: .6}", "{opacity: 1, x: 0, scale: 1}", "back.out(2)")
sfx("msg", TR[1]["b"])
ft2("#bolt4", TR[1]["b"] + .05, .3, "{opacity: 0, scale: 2.4, rotation: -30}", "{opacity: 1, scale: 1, rotation: 8}", "back.out(2.4)")
flash(TR[1]["b"] + .05, .4, .2, "#fff6c2"); shake(TR[1]["b"] + .05, 8)
burst(TR[1]["b"] + .1, 860, 1290, cols=("#ffd23f", "#ffffff", "#F343A2"))

# s5 STORY -> DM
S5 = ('<div class="scene" id="s5"><b class="ghost">3</b><div class="story" id="story5"><div class="sbar"><i id="sbf"></i></div>'
      '<div class="sav">' + AV("#ff8ac2") + '<b>your.page</b></div><div class="sbody"><span>New recipe<br>drops Friday</span></div>'
      '<div class="srep" id="srep">' + "".join(f'<u id="sr{k}" style="opacity:0">{c}</u>' for k, c in enumerate("want this!")) + '</div></div>'
      '<i class="sarr" id="sarr"></i><div class="dmb sm" id="dm5">' + LOGO + '<p>Here you go. The recipe link:</p><span class="lnk">creedom.ai/recipe</span></div></div>')
SC.append("s5")
title(2, TR[2]["n"], "STORY TO DM")
scene("s5", TR[2]["n"] + .7)
ft2("#story5", TR[2]["n"] + .75, .45, "{opacity: 0, scale: .6, rotation: -6}", "{opacity: 1, scale: 1, rotation: -3}", "back.out(1.6)")
js(f'tl.fromTo("#sbf", {{width: "0%"}}, {{width: "100%", duration: 3.2, ease: "none", immediateRender: false}}, {TR[2]["n"] + .8:.3f});')
for k in range(10):
    st(f"#sr{k}", TR[2]["a"] + k * .07, "{opacity: 1}")
    if k % 3 == 0:
        sfx("typing", TR[2]["a"] + k * .07)
pop("#sarr", W("d5", "story") - .05, .3, "{opacity: 0, scale: .3, rotation: -40}")
sfx("sent", W("d5", "story"))
ft2("#dm5", TR[2]["b"] - .1, .4, "{opacity: 0, y: 120, scale: .7}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
sfx("msg", TR[2]["b"])
burst(TR[2]["b"] + .1, 560, 1520)

# s6 LIVE -> DM: comments rain, each becomes an envelope, the counter climbs
LCM = ["DM", "link pls", "me!", "DM", "want it", "DM", "how?", "DM"]
S6 = ('<div class="scene" id="s6"><b class="ghost">4</b><div class="live" id="live6"><span class="lv" id="lv6">LIVE</span><div class="lbody">' + AV("#ff8ac2") + '</div>'
      + "".join(f'<div class="lc" id="lc{k}">{AV(random.choice(("#c9b3ff", "#ffd27a", "#b8f0cc", "#ffb3d6")))}<span>{c}</span></div>' for k, c in enumerate(LCM))
      + '</div>' + "".join(f'<i class="envf" id="ev{k}">{ENV}</i>' for k in range(8))
      + '<div class="ctr" id="ctr6">' + ENV + '<b id="ctrn">0</b><small>DMs SENT</small></div></div>')
SC.append("s6")
title(3, TR[3]["n"], "LIVE TO DM")
scene("s6", TR[3]["n"] + .7)
ft2("#live6", TR[3]["n"] + .75, .4, "{opacity: 0, x: -300}", "{opacity: 1, x: 0}", "back.out(1.5)")
js(f'tl.fromTo("#lv6", {{scale: 1}}, {{scale: 1.15, duration: .35, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}}, {TR[3]["n"] + .8:.3f});')
pop("#ctr6", TR[3]["a"], .35)
for k in range(8):
    tk = TR[3]["a"] + .1 + k * .22
    ft2(f"#lc{k}", tk, .3, "{opacity: 0, y: 80}", "{opacity: 1, y: 0}", "back.out(2)")
    js(f'tl.fromTo("#ev{k}", {{opacity: 1, x: 300, y: {1250 - (k % 4) * 60}, scale: .5, rotation: -20}}, {{opacity: 0, x: 820, y: 1000, scale: .9, rotation: 20, duration: .45, ease: "power2.in", immediateRender: false}}, {tk + .15:.3f});')
    js(f'tl.set("#ctrn", {{textContent: "{k + 1}"}}, {tk + .6:.3f});')
    js(f'tl.fromTo("#ctr6", {{scale: 1}}, {{scale: 1.1, duration: .08, yoyo: true, repeat: 1, immediateRender: false}}, {tk + .6:.3f});')
    sfx("tick", tk + .6) if k % 2 else sfx("pop", tk)
js(f'gsap.set(".envf", {{opacity: 0}});')
burst(TR[3]["b"] + .1, 830, 1040)

# s7 inbox starters: four chips, one gets tapped
CH = ["What do you do?", "Is it free?", "Get my audit", "Talk to a human"]
S7 = ('<div class="scene" id="s7"><b class="ghost">5</b><div class="chat empty" id="chat7"><div class="chd">' + LOGO + '<b>New message</b></div>'
      '<small class="tap2">TAP A QUESTION TO START</small>' + "".join(f'<div class="chip" id="ch{k}">{c}</div>' for k, c in enumerate(CH))
      + '<div class="ub small" id="ub7">Get my audit</div><div class="ab small" id="ab7">' + LOGO + '<p>On it. Drop your handle here.</p></div></div>'
      '<svg id="fing" viewBox="0 0 60 80" width="100" height="134"><path d="M20 76 L20 30 Q20 20 28 20 Q36 20 36 30 L36 44 L50 47 Q58 49 57 58 L54 76 Z" fill="#ffd9c2" stroke="#1a1020" stroke-width="4" stroke-linejoin="round"/></svg></div>')
SC.append("s7")
title(4, TR[4]["n"], "INBOX STARTERS")
scene("s7", TR[4]["n"] + .7)
ft2("#chat7", TR[4]["n"] + .75, .4, "{opacity: 0, y: 200}", "{opacity: 1, y: 0}", "back.out(1.5)")
for k in range(4):
    ft2(f"#ch{k}", TR[4]["a"] + k * .12, .3, "{opacity: 0, x: 120, scale: .7}", "{opacity: 1, x: 0, scale: 1}", "back.out(2)")
    sfx("pop", TR[4]["a"] + k * .12)
ft2("#fing", W("d7", "tap") - .3, .35, "{opacity: 0, x: 900, y: 1700}", "{opacity: 1, x: 640, y: 1270}", "power2.out")
js(f'tl.to("#ch2", {{scale: .92, backgroundColor: "#F343A2", color: "#ffffff", duration: .1, yoyo: true, repeat: 1}}, {W("d7", "tap"):.3f});')
sfx("click", W("d7", "tap"))
to("#fing", W("d7", "tap") + .35, .2, "{opacity: 0}")
to("#ch0, #ch1, #ch2, #ch3", W("d7", "start") - .1, .2, "{opacity: 0, x: -60}", "power2.in")
ft2("#ub7", W("d7", "start"), .3, "{opacity: 0, x: 200}", "{opacity: 1, x: 0}", "back.out(2)")
sfx("sent", W("d7", "start"))
ft2("#ab7", W("d7", "chat") + .05, .3, "{opacity: 0, x: -200}", "{opacity: 1, x: 0}", "back.out(2)")
sfx("msg", W("d7", "chat") + .05)

# s8 the twist: activity log, the pause toggle, Meta's platform
LOG = [("14:02", "@maya", "Comment to DM"), ("14:02", "@rohan", "Story to DM"), ("14:03", "@aisha", "DM to DM"), ("14:05", "@dev", "Live to DM"), ("14:06", "@sara", "Comment to DM")]
S8 = ('<div class="scene" id="s8"><div class="log" id="log8"><div class="lh"><b>Activity log</b><em>EXAMPLE</em></div><div class="lrows">'
      + "".join(f'<div class="lr" id="lr{k}"><small>{a}</small><b>{b}</b><span>{c}</span><i>Sent</i></div>' for k, (a, b, c) in enumerate(LOG)) + '</div></div>'
      '<div class="tog" id="tog8"><b>Auto-replies</b><div class="sw" id="sw8"><i id="knob8"></i></div><span id="tgl">ON</span></div>'
      '<div class="meta" id="meta8"><svg viewBox="0 0 48 48"><rect x="10" y="22" width="28" height="22" rx="5" fill="#1a1020"/><path d="M16 22 V16 Q16 8 24 8 Q32 8 32 16 V22" fill="none" stroke="#1a1020" stroke-width="5"/></svg>'
      '<div><b>Runs through Meta\'s own platform</b><span>No password sharing</span></div></div></div>')
SC.append("s8")
scene("s8", t8["t"] - .1)
ft2("#log8", t8["t"], .4, "{opacity: 0, y: 100}", "{opacity: 1, y: 0}", "back.out(1.5)")
for k in range(5):
    ft2(f"#lr{k}", t8["t"] + .2 + k * .16, .3, "{opacity: 0, x: 120}", "{opacity: 1, x: 0}", "back.out(1.8)")
    sfx("tick", t8["t"] + .2 + k * .16)
js(f'tl.fromTo(".lr i", {{scale: 1}}, {{scale: 1.2, duration: .1, yoyo: true, repeat: 1, stagger: .08, immediateRender: false}}, {t8["logged"]:.3f});')
sfx("ding2", t8["logged"])
ft2("#tog8", t8["tap"] - .3, .35, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2)")
js(f'tl.to("#knob8", {{x: -96, duration: .25, ease: "back.out(2)"}}, {t8["pauses"]:.3f});')
js(f'tl.to("#sw8", {{backgroundColor: "#c9c9d1", duration: .2}}, {t8["pauses"]:.3f});')
js(f'tl.set("#tgl", {{textContent: "PAUSED"}}, {t8["pauses"] + .1:.3f});')
js(f'tl.to(".lr i", {{backgroundColor: "#c9c9d1", duration: .2}}, {t8["pauses"] + .1:.3f});')
sfx("toggle", t8["pauses"])
js(f'tl.to("#knob8", {{x: 0, duration: .25, ease: "back.out(2)"}}, {t8["runs"] - .2:.3f});')
js(f'tl.to("#sw8", {{backgroundColor: "#2fbf71", duration: .2}}, {t8["runs"] - .2:.3f});')
js(f'tl.set("#tgl", {{textContent: "ON"}}, {t8["runs"] - .1:.3f});')
js(f'tl.to(".lr i", {{backgroundColor: "#2fbf71", duration: .2}}, {t8["runs"] - .1:.3f});')
sfx("toggle", t8["runs"] - .2)
ft2("#meta8", t8["meta"] - .1, .4, "{opacity: 0, y: 80, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.8)")
sfx("ding", t8["meta"])
burst(t8["meta"] + .2, 540, 1560, cols=("#2fbf71", "#ffffff", "#F343A2"))

# s9 CTA: COMMENT DM, the inbox counter
S9 = ('<div class="scene" id="s9"><div class="bigcta" id="bigcta"><span>COMMENT</span><b>DM</b></div>'
      '<div class="cbox" id="cbox"><i class="cav"></i><span id="cbt">' + "".join(f'<span id="cg{k}" style="opacity:0">{c}</span>' for k, c in enumerate("DM"))
      + '</span><b class="csend" id="csend">Post</b></div>'
      '<div class="ibx" id="ibx">' + ENV + '<i class="badge9" id="bdg"><b id="bdgn">0</b></i><small>WATCH YOUR INBOX</small></div></div>')
SC.append("s9")
scene("s9", t9["t"] - .1, "{opacity: 0, y: 200}")
ft2("#bigcta", t9["t"], .45, "{opacity: 0, scale: 2.4}", "{opacity: 1, scale: 1}", "back.out(1.8)")
sfx("impact", t9["t"] + .02); flash(t9["t"], .35)
ft2("#cbox", t9["dm"] + .1, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.8)")
for k in range(2):
    st(f"#cg{k}", t9["dm"] + .3 + k * .1, "{opacity: 1}")
    sfx("typing", t9["dm"] + .3 + k * .1)
js(f'tl.fromTo("#csend", {{scale: 1}}, {{keyframes: [{{scale: .85, duration: .08}}, {{scale: 1, duration: .15}}], immediateRender: false}}, {t9["now"]:.3f});')
sfx("click", t9["now"])
pop("#ibx", t9["watch"] - .2, .4, "{opacity: 0, scale: .4, y: 60}")
js(f'tl.fromTo("#ibx", {{rotation: -6}}, {{rotation: 6, duration: .08, yoyo: true, repeat: 7, immediateRender: false}}, {t9["inbox"]:.3f});')
for k in range(3):
    js(f'tl.set("#bdgn", {{textContent: "{k + 1}"}}, {t9["inbox"] + k * .2:.3f});')
    pop("#bdg", t9["inbox"] + k * .2, .2, "{opacity: 0, scale: 2}") if k == 0 else js(f'tl.fromTo("#bdg", {{scale: 1.5}}, {{scale: 1, duration: .18, immediateRender: false}}, {t9["inbox"] + k * .2:.3f});')
    sfx("msg" if k == 0 else "tick", t9["inbox"] + k * .2)
for k in range(26):
    x0 = random.randint(60, 1020)
    HTMLS.append(f'<i class="cf" id="cfx{k}" style="background:{random.choice(("#ff5fb7", "#F343A2", "#ffd27a", "#2fbf71", "#ffffff"))};'
                 f'width:{random.randint(12, 20)}px;height:{random.randint(22, 32)}px"></i>')
    js(f'tl.fromTo("#cfx{k}", {{x: {x0}, y: -60, rotation: {random.randint(0, 180)}, opacity: 1}}, {{x: {x0 + random.uniform(-160, 160):.0f}, y: 2000, '
       f'rotation: {random.randint(360, 900)}, duration: {random.uniform(1.6, 2.4):.2f}, ease: "power1.in", immediateRender: false}}, {t9["inbox"] + random.uniform(0, .3):.3f});')

# =====================================================================================================================
# Cree, the host
CR = P(935, 1815, .3)
js(f'gsap.set("#cree", {{x: {CR[0] - PCX:.0f}, y: {CR[1] - PCY:.0f}, scale: {CR[2]}, opacity: 1}});')
js('gsap.set("#cree .cpose", {opacity: 0}); gsap.set("#cp-phone", {opacity: 1});')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -7, duration: .6, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .6)}, immediateRender: false}}, 0);')
for k in range(int(DUR / 2.7)):
    blink(1.2 + k * 2.7)
pose(t0["msg"], "shock"); cree_wiggle(t0["msg"], 2, 6)
pose(t0["idid"], "think", flip=True); say(t0["send"] + .1, "?", .7, left=True)
pose(t1["cr"], "cheer", flip=True); cree_hop(t1["cr"] + .05, 70); sparkle(t1["cr"], .9)
pose(t1["set"], "present", flip=True)
pose(t2["t"], "point", flip=True)
for i in range(5):
    pose(TR[i]["a"], ("phone", "phone", "mag", "shock", "think")[i], flip=True)
    pose(TICK[i], "proud"); cree_hop(TICK[i], 60)
pose(t8["t"], "present", flip=True)
pose(t8["pauses"], "stand")
pose(t8["meta"], "proud"); cree_hop(t8["meta"] + .1, 60)
pose(t9["t"], "wave", flip=True)
cree_hop(t9["inbox"], 70, 2)

# background: blobs, dot grid, floating doodles, sheens, ghost numerals
BG = "".join(f'<i class="blob" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{c}"></i>'
             for x, y, r, c in ((-120, 200, 520, "rgba(255,150,200,.35)"), (700, 1300, 600, "rgba(243,67,162,.22)"), (680, -100, 420, "rgba(255,210,120,.25)")))
js(f'tl.fromTo(".blob", {{x: 0, y: 0}}, {{x: (i) => [80, -90, 60][i], y: (i) => [-60, 80, 70][i], duration: {DUR / 2:.2f}, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#dots", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "0px 240px", duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
SH = ["M0,-22 V22 M-22,0 H22", "M-20,0 A20,20 0 1,0 20,0 A20,20 0 1,0 -20,0", "M-24,8 Q-12,-12 0,8 T24,8", "M0,-22 L19,11 L-19,11 Z"]
for k in range(12):
    x, y = random.randint(40, 1040), random.randint(560, 1820)
    HTMLS.append(f'<svg class="fsh" id="fs{k}" style="left:{x}px;top:{y}px" viewBox="-30 -30 60 60"><path d="{SH[k % 4]}" fill="none" '
                 f'stroke="{random.choice(("#F343A2", "#ffb3d6", "#ffd23f", "#c9b3ff"))}" stroke-width="5" stroke-linecap="round"/></svg>')
    js(f'tl.fromTo("#fs{k}", {{y: 0, rotation: 0}}, {{y: {random.randint(-160, -60)}, rotation: {random.choice((-1, 1)) * random.randint(90, 270)}, duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
for sid, t0_ in (("s3", TR[0]["n"]), ("s4", TR[1]["n"]), ("s5", TR[2]["n"]), ("s6", TR[3]["n"]), ("s7", TR[4]["n"])):
    js(f'tl.fromTo("#{sid} .ghost", {{y: 80, opacity: 0}}, {{y: -60, opacity: 1, duration: 3.5, ease: "power1.out", immediateRender: false}}, {t0_ + .5:.3f});')

POST = " ".join(f'gsap.set("{sel}", {frm});' for sel, (t, frm) in sorted(FIRST.items(), key=lambda kv: kv[1][0]) if t > 0.0)
POST += (' gsap.set(".tc", {backgroundColor: "#ffffff", color: "#1a1020", scale: 1}); gsap.set(".tc .box", {backgroundColor: "rgba(0,0,0,0)", borderColor: "#d9c4d0"});'
         ' gsap.set("#s0", {opacity: 1}); gsap.set("#post0", {opacity: 1}); gsap.set("#knob8", {x: 0}); gsap.set("#sw8", {backgroundColor: "#2fbf71"});'
         ' gsap.set(".lr i", {backgroundColor: "#2fbf71"}); gsap.set("#fly3, .envf, .pulse", {opacity: 0});')
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: The DM you'll get? I didn't send it. 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="bg" id="bgl">{BG}</div><div class="bg" id="dots"></div>
      <div id="stage">{S0}{S1}{S2}{S3}{S4}{S5}{S6}{S7}{S8}{S9}</div>
      {TRK}
      <div style="position:absolute;inset:0;z-index:33;pointer-events:none">{cree_html()}</div>
      {chr(10).join(HTMLS)}
      <div id="flash"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      tl.progress(1, true).progress(0, true);
      {POST}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "lines": L0}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
