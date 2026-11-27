"""Creedom "4 checks before you post" (9:16, playbook script 3, keyword CHECK): writes index.html, plan/sfx_events.json, plan/edit.json.
Voice: the owner's ElevenLabs take (voice "Lima", Eleven v4), pauses trimmed, 18% faster. No music.
A checklist tracker (HOOK / PACING / AUDIO / ENDING) stays on screen and ticks as each check passes; every check gets its own
bad-vs-good animation; Creedom's Reel Analyzer (recreated, labelled EXAMPLE) does the twist; a CHECK comment box closes.
python3 build/generate.py"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
VERSION = os.environ.get("VERSION", "A")        # v3: A = "Comment CHECK" CTA, B = "Install Creedom" CTA (owner, 27 Nov)
os.environ.setdefault("WORDS", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plan", f"words_{VERSION}.json"))
from fx import ROOT, LINES, L0, L1, T, JS, SFX, js, sfx, ft, to, st  # noqa: E402
from fx import cree_html, pose, cree_hop, sparkle, P, sweat, say, cree_wiggle, blink, PCX, PCY, cree_to  # noqa: E402

random.seed(4)
DUR = round(L1["k8"] + 1.4, 2)
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
t_dont, t_post, t_until, t_four, t_chk = L0["k0"], T("k0", "post"), T("k0", "until"), T("k0", "four"), T("k0", "checks")
t_ai, t_scores, t_hit = L0["k2"] - .05, L0["k2"] + .1, T("k2", "nobody")     # v3: line 2 ("AI reel analyzer scores") was cut
t_num4, t_nobody = T("k2", "four"), T("k2", "nobody")
H = dict(n=L0["k3"], q=T("k3", "Does"), sense=T("k3", "scrolling"), mute=T("k3", "sound"), andd=T("k3", "And"))
Pc = dict(n=L0["k4"], q=T("k4", "Does"), change=T("k4", "change"), two=T("k4", "two"))
A = dict(n=L0["k5"], q=T("k5", "Can"), hear=T("k5", "hear"), voice=T("k5", "voice"), music=T("k5", "music"))
E = dict(n=L0["k6"], q=T("k6", "Does"), rewatch=T("k6", "rewatch"), comment=T("k6", "engage"), follow=T("k6", "follow"), orr=T("k6", "Or", 1), stop=T("k6", "stop"))
Y = dict(t=L0["k7"], upload=T("k7", "upload"), creedom=T("k7", "Creedom"), score=T("k7", "score"), each=T("k7", "each"), sec=T("k7", "each") + .25, before=T("k7", "before"))
t_cm, t_check = L0["k8"], T("k8", "CHECK" if VERSION == "A" else "Install")
TICK = [H["mute"] + .55, Pc["two"] + .55, A["music"] + .45, E["stop"] + .45]

# ---------------------------------------------------------------- captions
head("h0", [["Don't", "*post", "your", "next", "reel"], ["until", "it", "passes"], ["these", "*4", "*checks."]], "k0", 84)
head("h2", [["And", "number", "*four"], ["is", "the", "one", "almost"], ["*nobody", "checks."]], "k2", 84)
head("h3", [["Does", "your", "hook", "*stop"], ["people", "from", "*scrolling?"]], "k3", 84, after=H["q"])
head("h3b", [["*AND", "do", "that"], ["when", "watching"], ["without", "*sound?"]], "k3", 84, after=H["andd"])
head("h4", [["Does", "something", "*change"], ["every", "*two", "*seconds?"]], "k4", 84, after=Pc["q"])
head("h5", [["Can", "people", "actually"], ["*hear", "your", "*voice"], ["over", "the", "music?"]], "k5", 80, after=A["q"])
head("h6", [["Does", "it", "give", "people", "a"], ["reason", "to", "*rewatch,"], ["*engage", "or", "*follow?"]], "k6", 78, after=E["q"])
head("h6b", [["Or", "does", "it", "just"], ["stop", "*abruptly?"]], "k6", 96, after=E["orr"])
head("h7", [["Check", "all", "*four", "yourself."]], "k7", 84)
head("h7b", [["Or", "upload", "your", "video", "to"], ["*Creedom's", "Reel", "Analyzer"]], "k7", 78, after=T("k7", "Or"))
head("h7c", [["and", "get", "a", "*score"], ["for", "each", "check."]], "k7", 80, after=T("k7", "and"))
head("h7d", [["Do", "this"], ["*before", "*posting."]], "k7", 104, after=T("k7", "Do"))
if VERSION == "A":
    head("h8", [["Comment", "*CHECK"], ["and", "I'll", "DM", "you", "the"], ["*checklist."]], "k8", 84)
else:
    head("h8", [["*Install", "Creedom", "and"], ["check", "your", "next", "reel"], ["*before", "*posting."]], "k8", 80)

# ---------------------------------------------------------------- the tracker (always on, ticks per check)
NAMES = ["HOOK", "PACING", "AUDIO", "ENDING"]
TRK = '<div id="trk">' + "".join(f'<div class="tc" id="tc{i}"><i class="box" id="tb{i}"><u id="tk{i}">{CHECK_SVG}</u></i><b>{n}</b></div>' for i, n in enumerate(NAMES)) + '</div>'
pop("#trk", t_chk + .05, .35, "{opacity: 0, y: -20, scale: .8}")
for i in range(4):
    pop(f"#tc{i}", t_chk + .1 + i * .1, .3, "{opacity: 0, scale: .4}")
    sfx("pop", t_chk + .1 + i * .1)
for i, tn in enumerate((H["n"], Pc["n"], A["n"], E["n"])):
    js(f'tl.to("#tc{i}", {{scale: 1.12, backgroundColor: "#1a1020", color: "#ffffff", duration: .2, ease: "back.out(3)"}}, {tn:.3f});')
    pop(f"#tk{i}", TICK[i], .3, "{opacity: 0, scale: 2.4, rotation: -30}")
    js(f'tl.to("#tc{i}", {{scale: 1, backgroundColor: "#2fbf71", color: "#ffffff", duration: .25}}, {TICK[i]:.3f});')
    js(f'tl.to("#tb{i}", {{backgroundColor: "#ffffff", borderColor: "#ffffff", duration: .2}}, {TICK[i]:.3f});')
    sfx("coin", TICK[i])
    burst(TICK[i] + .05, (260, 436, 608, 784)[i], 489, n=10, r=(50, 110))
js(f'tl.fromTo("#tc3", {{boxShadow: "0 0 0 0 rgba(243,67,162,0)"}}, {{boxShadow: "0 0 0 14px rgba(243,67,162,.35)", duration: .35, yoyo: true, repeat: 5, immediateRender: false}}, {t_num4 + .2:.3f});')
to("#trk", t_cm - .2, .25, "{opacity: 0, y: -30}", "power2.in")

# =====================================================================================================================
# s0: the editor, the Post button, NOT YET, the giant 4
CLIPS = "".join(f'<i style="width:{w}px;background:{c}"></i>' for w, c in ((150, "#ff8ac2"), (90, "#ffb86b"), (180, "#8a6bff"), (120, "#2fbf71"), (140, "#ff5fb7")))
S0 = ('<div class="scene" id="s0" style="opacity:1"><div class="ed" id="ed"><i class="sheen"></i><div class="edtop"><i></i><i></i><i></i><span>my_reel_final_v3.mp4</span></div>'
      '<div class="prev"><div class="rthumb"><i class="dish"></i><b>3 meals under 100</b></div><u class="rec">● 0:12 / 0:30</u></div>'
      f'<div class="tlw"><div class="tlclips">{CLIPS}</div><div class="tlclips aud">{"".join("<i></i>" for _ in range(28))}</div><i class="edph" id="edph"></i></div>'
      '<div class="postbtn" id="postbtn">Post</div></div>'
      '<svg id="cursor" viewBox="0 0 60 80" width="90" height="120"><path d="M8 4 L8 64 L22 50 L32 74 L42 70 L32 46 L52 46 Z" fill="#fff" stroke="#1a1020" stroke-width="5" stroke-linejoin="round"/></svg>'
      '<div class="notyet" id="notyet"><span>NOT YET</span></div>'
      '<svg class="ring4" id="ring4" viewBox="0 0 400 400"><circle cx="200" cy="200" r="180" fill="none" stroke="#F343A2" stroke-width="10" stroke-dasharray="26 22"/>'
      '<circle cx="200" cy="200" r="150" fill="none" stroke="#ffd23f" stroke-width="4" stroke-dasharray="4 14"/></svg>'
      '<div class="big4" id="big4"><b>4</b><span>CHECKS</span></div></div>')
SC.append("s0")
js(f'tl.fromTo("#edph", {{left: "6%"}}, {{left: "88%", duration: {t_four:.2f}, ease: "none", immediateRender: false}}, 0);')
js(f'tl.fromTo(".tlclips.aud i", {{scaleY: .3}}, {{scaleY: 1, duration: .18, yoyo: true, repeat: 15, stagger: {{each: .04, from: "random"}}, ease: "sine.inOut", immediateRender: false}}, 0);')
ft2("#cursor", t_post - .2, .5, "{opacity: 0, x: 980, y: 1700}", "{opacity: 1, x: 770, y: 1400}", "power2.out")
js(f'tl.to("#postbtn", {{scale: 1.08, boxShadow: "0 0 0 14px rgba(243,67,162,.35)", duration: .2, yoyo: true, repeat: 1}}, {t_post + .15:.3f});')
ft2("#notyet", t_until - .05, .22, "{opacity: 0, scale: 2.6, rotation: -24}", "{opacity: 1, scale: 1, rotation: -9}", "power4.out")
sfx("stamp", t_until); punch(t_until, 1.04); sfx("whoosh", t_post - .2)
js(f'tl.to("#cursor", {{x: 1000, y: 1800, opacity: 0, duration: .3, ease: "power2.in"}}, {t_until + .05:.3f});')
js(f'tl.to("#ed", {{scale: .9, opacity: .25, filter: "blur(6px)", duration: .35}}, {t_four - .1:.3f});')
to("#notyet", t_four - .1, .2, "{opacity: 0, scale: .8}")
ft2("#big4", t_four, .4, "{opacity: 0, scale: 3.5, rotation: -12}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(1.7)")
sfx("impact", t_four + .02); sfx("shutter", t_four); sfx("whoosh_big", t_four - .1); punch(t_four + .05, 1.06); flash(t_four, .5)
ft2("#ring4", t_four + .05, .5, "{opacity: 0, scale: .2, rotation: -90}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(1.6)")
js(f'tl.to("#ring4", {{rotation: 200, duration: 3, ease: "none"}}, {t_four + .55:.3f});')
burst(t_four + .1, 540, 960, n=22, r=(220, 420))
js(f'tl.fromTo("#big4 b", {{rotation: -4}}, {{rotation: 4, duration: .3, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, {t_four + .4:.3f});')

# =====================================================================================================================
# s1: the analyzer scans the reel; four meters with "?"; s2 meter four in the spotlight
METERS = "".join(f'<div class="mt" id="mt{i}"><i class="sheen"></i><b>{n}</b><div class="mbar"><i class="shim"></i></div><span>?</span></div>' for i, n in enumerate(NAMES))
S1 = ('<div class="scene" id="s1"><div class="aichip" id="aichip">AI REEL ANALYZER</div><div class="vf"><div class="rthumb"><i class="dish"></i><b>3 meals under 100</b></div>'
      '<i class="cor c1"></i><i class="cor c2"></i><i class="cor c3"></i><i class="cor c4"></i><i class="laser" id="laser"></i></div>'
      f'<div class="meters">{METERS}</div><i class="spot" id="spot"></i><div class="skip" id="skip"><i></i>most creators skip this</div></div>')
SC.append("s1")
scene("s1", t_ai - .05)
pop("#aichip", t_ai + .1, .3)
js(f'tl.fromTo("#laser", {{y: 0}}, {{y: 600, duration: .9, yoyo: true, repeat: 2, ease: "sine.inOut", immediateRender: false}}, {t_ai + .2:.3f});')
sfx("scanner", t_ai + .2)
for i in range(4):
    ft2(f"#mt{i}", t_scores + i * .12, .35, "{opacity: 0, x: 120}", "{opacity: 1, x: 0}", "back.out(1.8)")
    sfx("pop", t_scores + i * .12)
js(f'tl.fromTo(".shim", {{x: -200}}, {{x: 400, duration: .8, repeat: 4, ease: "none", immediateRender: false}}, {t_scores:.3f});')
for i in range(3):
    js(f'tl.to("#mt{i}", {{opacity: .3, duration: .25}}, {t_num4 + .1:.3f});')
js(f'tl.to("#mt3", {{scale: 1.12, x: -20, duration: .3, ease: "back.out(2)"}}, {t_num4 + .1:.3f});')
ft2("#spot", t_num4, .4, "{opacity: 0}", "{opacity: 1}", "power2.out")
js(f'tl.fromTo("#mt3 span", {{scale: 1}}, {{scale: 1.5, duration: .25, yoyo: true, repeat: 3, immediateRender: false}}, {t_num4 + .4:.3f});')
pop("#skip", t_nobody, .35, "{opacity: 0, scale: .4, rotation: 6}")
sfx("ding2", t_num4 + .1); sfx("swish", t_nobody)

# =====================================================================================================================
# title cards for each check
def title(i, t, name):
    HTMLS.append(f'<div class="ttl" id="tt{i}"><i class="band"></i>' + "".join(f'<i class="stk" style="top:{20 + k * 52}px;width:{random.randint(180, 420)}px"></i>' for k in range(5))
                 + f'<b>{i + 1}</b><span>{name}</span></div>')
    js(f'tl.fromTo("#tt{i} .stk", {{x: -500}}, {{x: 1400, duration: .55, stagger: .04, ease: "power2.in", immediateRender: false}}, {t - .05:.3f});')
    js(f'tl.fromTo("#tt{i} .band", {{scaleX: 0}}, {{scaleX: 1, duration: .25, ease: "power3.out", immediateRender: false}}, {t - .05:.3f});')
    ft2(f"#tt{i}", t - .05, .25, "{opacity: 0}", "{opacity: 1}", "power2.out")
    js(f'tl.fromTo("#tt{i} b", {{scale: 3, rotation: -15}}, {{scale: 1, rotation: 0, duration: .35, ease: "back.out(2)", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#tt{i} span", {{x: 200, opacity: 0}}, {{x: 0, opacity: 1, duration: .3, ease: "power3.out", immediateRender: false}}, {t + .08:.3f});')
    to(f"#tt{i}", t + .62, .2, "{opacity: 0, scale: 1.2}", "power2.in")
    for sc_ in SC:                                   # clear the previous scene under the title card
        js(f'tl.to("#{sc_}", {{opacity: 0, duration: .15}}, {t + .05:.3f});')
    sfx("whoosh", t - .05); sfx("impact", t)
    flash(t, .35)


# s3 HOOK: muted first frame, bad vs good
S3 = ('<div class="scene" id="s3"><b class="ghost">1</b><div class="mute" id="mute"><svg viewBox="0 0 64 64"><path d="M10 24 H22 L36 12 V52 L22 40 H10 Z" fill="#1a1020"/>'
      '<path d="M44 24 L58 40 M58 24 L44 40" stroke="#e0283e" stroke-width="6" stroke-linecap="round"/></svg>SOUND OFF</div>'
      f'<div class="fr2 l" id="fr0">{AVATAR}<div class="huh" id="huh">huh?</div>{NO("nb0")}<small>talking, nothing on screen</small></div>'
      f'<div class="fr2 r" id="fr1">{AVATAR}<div class="hook" id="hookt">3 MEALS<br>UNDER 100</div><i class="arr" id="arr"></i>{OK("ob0")}<small>the payoff, in text</small></div></div>')
SC.append("s3")
title(0, H["n"], "HOOK")
scene("s3", H["n"] + .55)
pop("#mute", H["n"] + .65, .3)
ft2("#fr0", H["q"] - .1, .4, "{opacity: 0, x: -300, rotation: -6}", "{opacity: 1, x: 0, rotation: -2}", "back.out(1.5)")
ft2("#fr1", H["q"] + .1, .4, "{opacity: 0, x: 300, rotation: 6}", "{opacity: 1, x: 0, rotation: 2}", "back.out(1.5)")
js(f'tl.fromTo(".mouth", {{scaleY: 1}}, {{scaleY: .2, duration: .12, yoyo: true, repeat: 15, transformOrigin: "50% 50%", immediateRender: false}}, {H["q"]:.3f});')
pop("#huh", H["sense"] - .1, .3, "{opacity: 0, scale: .3, rotation: -12}")
badge("nb0", False, H["sense"])
ft2("#hookt", H["mute"] - .15, .3, "{opacity: 0, scale: 2, y: -20}", "{opacity: 1, scale: 1, y: 0}", "back.out(2)")
pop("#arr", H["mute"] + .1, .25)
badge("ob0", True, H["mute"] + .25)
HTMLS.append('<div class="andst" id="andst"><span>AND</span></div>')
ft2("#andst", H["andd"] - .05, .25, "{opacity: 0, scale: 2.6, rotation: -20}", "{opacity: 1, scale: 1, rotation: -8}", "back.out(2.4)")
to("#andst", H["andd"] + .9, .2, "{opacity: 0, scale: .8}")
sfx("stamp", H["andd"])
js(f'tl.fromTo("#mute", {{scale: 1}}, {{scale: 1.25, duration: .18, yoyo: true, repeat: 3, immediateRender: false}}, {T("k3", "without"):.3f});')

# s4 PACING: one long clip vs a cut every two seconds
CUTS = "".join(f'<i style="background:{c}"><u id="cut{k}">CUT</u></i>' for k, c in enumerate(("#ff8ac2", "#ffb86b", "#8a6bff", "#2fbf71")))
S4 = ('<div class="scene" id="s4"><b class="ghost">2</b>'
      f'<div class="row bad" id="rw0">{NO("nb1")}<small>one 8-second shot</small><div class="lane"><i class="long"><span>zzz</span></i><u class="ph" id="ph0"></u></div><div class="lab"><span>0s</span><span>8s</span></div></div>'
      '<div class="watch" id="watch"><svg viewBox="0 0 100 100"><circle cx="50" cy="55" r="38" fill="#fff" stroke="#1a1020" stroke-width="6"/><rect x="42" y="6" width="16" height="10" rx="3" fill="#1a1020"/>'
      '<path id="whand" d="M50 55 L50 26" stroke="#F343A2" stroke-width="6" stroke-linecap="round"/></svg><b>every 2s</b></div>'
      f'<div class="row good" id="rw1">{OK("ob1")}<small>a change every 2 seconds</small><div class="lane cuts">{CUTS}<u class="ph" id="ph1"></u></div><div class="lab"><span>0s</span><span>2</span><span>4</span><span>6</span><span>8s</span></div></div></div>')
SC.append("s4")
title(1, Pc["n"], "PACING")
scene("s4", Pc["n"] + .55)
ft2("#rw0", Pc["n"] + .6, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.6)")
ft2("#rw1", Pc["q"], .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.6)")
pop("#watch", Pc["q"] + .1, .3)
span = Pc["two"] + .5 - Pc["q"]
js(f'tl.fromTo("#ph0", {{left: "0%"}}, {{left: "100%", duration: {span:.2f}, ease: "none", immediateRender: false}}, {Pc["q"]:.3f});')
js(f'tl.fromTo("#ph1", {{left: "0%"}}, {{left: "100%", duration: {span:.2f}, ease: "none", immediateRender: false}}, {Pc["q"]:.3f});')
js(f'tl.fromTo("#whand", {{rotation: 0}}, {{rotation: 720, svgOrigin: "50 55", duration: {span:.2f}, ease: "none", immediateRender: false}}, {Pc["q"]:.3f});')
for k in range(1, 4):
    tk = Pc["q"] + span * k / 4
    pop(f"#cut{k}", tk, .2, "{opacity: 0, scale: 2}")
    js(f'tl.to("#cut{k}", {{opacity: 0, duration: .2}}, {tk + .35:.3f});')
    sfx("click", tk)
    js(f'tl.fromTo("#rw1 .cuts i:nth-child({k + 1})", {{scale: 1}}, {{scale: 1.1, duration: .08, yoyo: true, repeat: 1, immediateRender: false}}, {tk:.3f});')
js(f'tl.fromTo(".long span", {{y: 0, opacity: .3}}, {{y: -14, opacity: 1, duration: .4, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {Pc["q"]:.3f});')
badge("nb1", False, Pc["change"])
badge("ob1", True, Pc["two"] + .1)

# s5 AUDIO: the mixer -- music down, voice up
WAVE = lambda n, cls: "".join(f'<i class="{cls}" style="height:{random.randint(30, 100)}%"></i>' for _ in range(n))
LEDS = "".join(f'<i class="led" id="led{k}"></i>' for k in range(10))
S5 = ('<div class="scene" id="s5"><b class="ghost">3</b><div class="mixer" id="mixer"><div class="fad"><div class="slot"><i class="knob" id="kv"></i></div><b>VOICE</b></div>'
      '<div class="fad"><div class="slot"><i class="knob pk" id="km"></i></div><b>MUSIC</b></div><div class="leds">' + LEDS + '</div></div>'
      f'<div class="waves"><div class="wv"><b>VOICE</b><div class="bars v" id="wvv">{WAVE(26, "v")}</div></div>'
      f'<div class="wv"><b>MUSIC</b><div class="bars m" id="wvm">{WAVE(26, "m")}</div></div></div>'
      f'<div class="cant" id="cant">can\'t hear you</div>{NO("nb2")}{OK("ob2")}</div>')
SC.append("s5")
title(2, A["n"], "AUDIO")
scene("s5", A["n"] + .55)
js('gsap.set("#kv", {y: 220}); gsap.set("#km", {y: 20}); gsap.set("#wvv", {scaleY: .25}); gsap.set("#wvm", {scaleY: 1});')
js(f'tl.fromTo("#wvv i, #wvm i", {{scaleY: .5}}, {{scaleY: 1, duration: .14, yoyo: true, repeat: 23, stagger: {{each: .02, from: "random"}}, ease: "sine.inOut", immediateRender: false}}, {A["n"] + .55:.3f});')
for k in range(10):
    js(f'tl.set("#led{k}", {{backgroundColor: "{"#e0283e" if k >= 7 else "#f2b134"}"}}, {A["q"] + k * .03:.3f});')
pop("#cant", A["q"] + .1, .3, "{opacity: 0, scale: .4, rotation: -8}")
badge("nb2", False, A["q"] + .2)
t_mix = A["voice"] - .1
js(f'tl.to("#km", {{y: 220, duration: .45, ease: "power3.inOut"}}, {t_mix:.3f});')
js(f'tl.to("#kv", {{y: 20, duration: .45, ease: "power3.inOut"}}, {t_mix + .1:.3f});')
js(f'tl.to("#wvm", {{scaleY: .25, duration: .45}}, {t_mix:.3f});')
js(f'tl.to("#wvv", {{scaleY: 1, duration: .45}}, {t_mix + .1:.3f});')
to("#cant, #nb2", t_mix, .2, "{opacity: 0}")
for k in range(10):
    js(f'tl.set("#led{k}", {{backgroundColor: "{"#2fbf71" if k < 7 else "#e9d2de"}"}}, {t_mix + .45 + k * .03:.3f});')
sfx("swish", t_mix)
badge("ob2", True, A["music"])

# s6 ENDING: loop + comments (good) vs a hard stop (bad)
S6 = ('<div class="scene" id="s6"><b class="ghost">4</b><i class="spot sp6" id="spot6"></i><div class="endreel" id="endreel"><i class="sheen"></i><div class="rthumb"><i class="dish"></i><b>3 meals under 100</b></div>'
      '<div class="prog"><i id="pfill"></i></div><svg class="loop" id="loop" viewBox="0 0 200 200"><path d="M160 100 A60 60 0 1 1 130 48" fill="none" stroke="#2fbf71" stroke-width="14" stroke-linecap="round"/>'
      '<path d="M118 28 L140 50 L112 62 Z" fill="#2fbf71"/></svg><div class="x2" id="x2">x2</div></div>'
      '<div class="cm" id="cm0">wait, again?</div><div class="cm" id="cm1">part 2??</div><div class="cm" id="cm2">saving this</div>' + OK("ob3") + NO("nb3") +
      '<div class="theend" id="theend"><b>THE END</b><svg viewBox="0 0 80 120" class="swipe"><path d="M40 110 L40 20 M18 42 L40 18 L62 42" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      '<small>viewer swipes away</small></div></div>')
SC.append("s6")
title(3, E["n"], "ENDING")
scene("s6", E["n"] + .55)
ft2("#spot6", E["n"] + .55, .4, "{opacity: 0}", "{opacity: 1}")
ft2("#endreel", E["n"] + .6, .4, "{opacity: 0, y: 200}", "{opacity: 1, y: 0}", "back.out(1.5)")
js(f'tl.fromTo("#pfill", {{width: "0%"}}, {{width: "100%", duration: {E["rewatch"] - E["n"] - .7:.2f}, ease: "none", immediateRender: false}}, {E["n"] + .7:.3f});')
ft2("#loop", E["rewatch"] - .05, .5, "{opacity: 0, rotation: -200, scale: .4}", "{opacity: 1, rotation: 0, scale: 1}", "back.out(1.6)")
pop("#x2", E["rewatch"] + .3, .3, "{opacity: 0, scale: 2.4}")
sfx("swish", E["rewatch"]); sfx("coin", E["rewatch"] + .3)
for k in range(3):
    ft2(f"#cm{k}", E["comment"] + k * .15, .3, "{opacity: 0, y: 40, scale: .6}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.2)")
    sfx("pop", E["comment"] + k * .15)
badge("ob3", True, E["follow"] + .3)
HTMLS.append('<div class="folb" id="folb"><span id="folt">Follow</span></div>')
pop("#folb", E["follow"] - .05, .3, "{opacity: 0, scale: .4, y: 40}")
js(f'tl.set("#folt", {{textContent: "Following"}}, {E["follow"] + .3:.3f});')
js(f'tl.to("#folb", {{backgroundColor: "#ffffff", color: "#1a1020", duration: .15}}, {E["follow"] + .3:.3f});')
sfx("click", E["follow"] + .3)
to("#folb", E["stop"] - .1, .1, "{opacity: 0}")
# "or does it just stop?": a hard cut to black
ft2("#theend", E["stop"] - .05, .05, "{opacity: 0}", "{opacity: 1}", "none")
js(f'tl.fromTo("#theend b", {{scale: 1.4, opacity: 0}}, {{scale: 1, opacity: 1, duration: .25, ease: "power3.out", immediateRender: false}}, {E["stop"]:.3f});')
js(f'tl.fromTo("#theend .swipe", {{y: 120, opacity: 0}}, {{y: -60, opacity: 1, duration: .45, ease: "power2.out", immediateRender: false}}, {E["stop"] + .2:.3f});')
sfx("powerdown", E["stop"] - .05)
js(f'tl.set("#h6b", {{color: "#ffffff", textShadow: "0 0 24px rgba(0,0,0,.6)"}}, {E["stop"] - .06:.3f});')
badge("nb3", False, E["stop"] + .2)
to("#theend", E["stop"] + .75, .2, "{opacity: 0}")

# =====================================================================================================================
# s7 check all four: the clipboard
S7 = ('<div class="scene" id="s7"><div class="clip" id="clipb"><i class="sheen"></i><i class="clamp"></i><small>BEFORE YOU POST</small>'
      + "".join(f'<div class="crow"><i class="box" id="cb{i}"><u id="ck{i}">{CHECK_SVG}</u></i><b>{n}</b></div>' for i, n in enumerate(NAMES))
      + '</div><div class="save" id="save"><svg viewBox="0 0 40 52"><path d="M4 4 H36 V48 L20 36 L4 48 Z" fill="#fff"/></svg>SAVE THIS</div></div>')
SC.append("s7")
scene("s7", Y["t"] - .05, "{opacity: 0, y: 300, rotation: 4}")
for i in range(4):
    tk = Y["t"] + .2 + i * .16
    pop(f"#ck{i}", tk, .25, "{opacity: 0, scale: 2.4}")
    js(f'tl.to("#cb{i}", {{backgroundColor: "#2fbf71", borderColor: "#2fbf71", duration: .15}}, {tk:.3f});')
    sfx("tick", tk)
pop("#save", T("k7", "yourself"), .35, "{opacity: 0, scale: .4, rotation: -10}")
sfx("ding", T("k7", "yourself")); sfx("sparkle", T("k7", "yourself") + .1)

# s8 Creedom's Reel Analyzer (recreated, EXAMPLE)
CATS = [("Hook", 4), ("Pacing", 3), ("Audio", 4), ("Ending", 2)]
SEGS = "".join(f'<i id="sg{k}" style="background:{"#ff3b4e" if k in (6, 13) else "#2fbf71"}"></i>' for k in range(15))
S8 = ('<div class="scene" id="s8"><div class="cz"><i class="sheen"></i><div class="czh"><img src="assets/img/creedom_logo.png" alt=""><b>Reel Analyzer</b><em>EXAMPLE</em></div>'
      '<div class="up" id="up"><small>UPLOADING YOUR CUT</small><div class="upbar"><i id="upf"></i></div><b id="upp">0%</b></div>'
      '<div class="res" id="res"><div class="rthumb sm"><i class="dish"></i></div><div class="sc"><b id="scn">0.0</b><small>/ 5</small></div>'
      '<div class="cats">' + "".join(f'<div class="cat" id="ct{i}"><b>{n}</b><div class="cbar"><i id="cf{i}" style="background:{"#ff3b4e" if v <= 2 else "#F343A2"}"></i></div><span>{v}</span></div>' for i, (n, v) in enumerate(CATS)) + '</div></div>'
      f'<div class="sbs" id="sbs"><small>SECOND BY SECOND</small><div class="segs">{SEGS}<u id="sph"></u></div>'
      '<div class="flag f1" id="fl0"><b>0:12</b> energy dips</div><div class="flag f2" id="fl1"><b>0:28</b> ending just stops, loop it</div></div></div></div>')
SC.append("s8")
scene("s8", Y["upload"] - .25, "{opacity: 0, x: 600}")
ft2("#up", Y["upload"] - .1, .3, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "back.out(1.6)")
js(f'tl.fromTo("#upf", {{width: "0%"}}, {{width: "100%", duration: {Y["creedom"] - Y["upload"] + .3:.2f}, ease: "power2.inOut", immediateRender: false}}, {Y["upload"]:.3f});')
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 100, duration: {Y["creedom"] - Y["upload"] + .3:.2f}, ease: "power2.inOut", onUpdate: () => {{ document.getElementById("upp").textContent = Math.round(o.v) + "%"; }}}}, {Y["upload"]:.3f}); }})();')
sfx("riser_short", Y["upload"])
to("#up", Y["score"] - .45, .2, "{opacity: 0, y: -20}")
ft2("#res", Y["score"] - .35, .35, "{opacity: 0, scale: .85}", "{opacity: 1, scale: 1}", "back.out(1.6)")
js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 3.6, duration: .7, ease: "power2.out", onUpdate: () => {{ document.getElementById("scn").textContent = o.v.toFixed(1); }}}}, {Y["score"] - .2:.3f}); }})();')
for i, (n, v) in enumerate(CATS):
    js(f'tl.fromTo("#cf{i}", {{width: "0%"}}, {{width: "{v * 20}%", duration: .4, ease: "power3.out", immediateRender: false}}, {Y["each"] - .1 + i * .1:.3f});')
    sfx("pop", Y["each"] - .1 + i * .1)
ft2("#sbs", Y["sec"] - .15, .3, "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", "back.out(1.6)")
js(f'tl.fromTo("#sph", {{left: "0%"}}, {{left: "100%", duration: {t_cm - Y["sec"] + .1:.2f}, ease: "none", immediateRender: false}}, {Y["sec"]:.3f});')
for k in range(15):
    ft2(f"#sg{k}", Y["sec"] + (t_cm - Y["sec"]) * k / 15, .12, "{opacity: .15, scaleY: .4}", "{opacity: 1, scaleY: 1}", "back.out(3)")
pop("#fl0", Y["sec"] + (t_cm - Y["sec"]) * 6 / 15, .3, "{opacity: 0, scale: .5, y: 20}")
pop("#fl1", Y["sec"] + (t_cm - Y["sec"]) * 13 / 15, .3, "{opacity: 0, scale: .5, y: 20}")
sfx("error", Y["sec"] + (t_cm - Y["sec"]) * 6 / 15)
HTMLS.append('<div class="stamp bypost" id="bypost"><span>BEFORE YOU POST</span></div>')
ft2("#bypost", Y["before"] - .05, .22, "{opacity: 0, scale: 2.4, rotation: -20}", "{opacity: 1, scale: 1, rotation: -7}", "power4.out")
sfx("stamp", Y["before"]); punch(Y["before"], 1.035)
to("#bypost", t_cm - .2, .15, "{opacity: 0}")

if VERSION == "A":
    # s9 CTA: CHECK typed, the checklist PDF
    S9 = ('<div class="scene" id="s9"><div class="cbox" id="cbox"><i class="cav"></i><span id="cbt">' + "".join(f'<span id="cg{k}" style="opacity:0">{c}</span>' for k, c in enumerate("CHECK"))
          + '</span><b class="csend" id="csend">Post</b></div><div class="sent" id="sent">Sent! Now check your DMs</div>'
          '<div class="pdf" id="pdf"><i class="sheen"></i><small>FREE CHECKLIST</small><b>4 checks<br>before you<br><em>post</em></b>'
          + "".join(f'<div class="prow"><i>{CHECK_SVG}</i>{n.title()}</div>' for n in NAMES) + '<span>Creedom</span></div></div>')
    SC.append("s9")
    scene("s9", t_cm - .1, "{opacity: 0, y: 200}")
    ft2("#cbox", t_cm, .35, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}", "back.out(1.8)")
    for k in range(5):
        st(f"#cg{k}", t_check + k * .08, "{opacity: 1}")
        sfx("tick", t_check + k * .08)
    js(f'tl.fromTo("#csend", {{scale: 1}}, {{keyframes: [{{scale: .85, duration: .08}}, {{scale: 1, duration: .15}}], immediateRender: false}}, {t_check + .5:.3f});')
    sfx("click", t_check + .5)
    ft2("#sent", t_check + .62, .3, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "back.out(2)")
    ft2("#pdf", T("k8", "DM") - .05, .5, "{opacity: 0, y: 500, rotation: 12}", "{opacity: 1, y: 0, rotation: -3}", "back.out(1.5)")
    sfx("whoosh", T("k8", "DM") - .05); sfx("chime", T("k8", "checklist"))
else:
    # s9 (version B): the Creedom app card, Install tapped, a download ring, Open; then a check before posting
    S9 = ('<div class="scene" id="s9"><div class="appc" id="appc"><div class="atile"><img src="assets/img/creedom_logo.png" alt=""></div>'
          '<div class="ainfo"><b>Creedom</b><span>AI coach for creators</span><small>Reel Analyzer · free to start</small></div>'
          '<div class="inst" id="inst"><span id="instt">Install</span><svg class="iring" id="iring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" fill="none" stroke="#f6d9e8" stroke-width="10"/>'
          '<circle id="iarc" cx="50" cy="50" r="38" fill="none" stroke="#F343A2" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 50 50)"/></svg></div></div>'
          '<svg id="fing9" viewBox="0 0 60 80" width="100" height="134"><path d="M20 76 L20 30 Q20 20 28 20 Q36 20 36 30 L36 44 L50 47 Q58 49 57 58 L54 76 Z" fill="#ffd9c2" stroke="#1a1020" stroke-width="4" stroke-linejoin="round"/></svg>'
          '<div class="nxt" id="nxt"><div class="rthumb sm2"><i class="dish"></i></div><div class="nxi"><small>YOUR NEXT REEL</small>'
          + "".join(f'<div class="nrow" id="nr{i}"><i>{CHECK_SVG}</i>{n.title()}</div>' for i, n in enumerate(NAMES)) + '</div></div>'
          '<div class="stamp bypost2" id="bypost2"><span>BEFORE POSTING</span></div></div>')
    SC.append("s9")
    scene("s9", t_cm - .1, "{opacity: 0, y: 200}")
    t_inst, t_chk2, t_bef = T("k8", "Install"), T("k8", "check"), T("k8", "before")
    ft2("#appc", t_cm - .05, .45, "{opacity: 0, y: 160, scale: .8}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.6)")
    sfx("whoosh", t_cm - .1)
    ft2("#fing9", t_inst + .05, .3, "{opacity: 0, x: 980, y: 1500}", "{opacity: 1, x: 760, y: 1010}", "power2.out")
    js(f'tl.to("#inst", {{scale: .9, duration: .08, yoyo: true, repeat: 1}}, {t_inst + .35:.3f});')
    sfx("click", t_inst + .35)
    to("#fing9", t_inst + .6, .2, "{opacity: 0}")
    js(f'tl.set("#instt", {{opacity: 0}}, {t_inst + .45:.3f}); tl.set("#iring", {{opacity: 1}}, {t_inst + .45:.3f});')
    js(f'tl.to("#inst", {{backgroundColor: "#ffffff", duration: .1}}, {t_inst + .45:.3f});')
    js(f'tl.fromTo("#iarc", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: .75, ease: "power1.inOut", immediateRender: false}}, {t_inst + .45:.3f});')
    sfx("riser_short", t_inst + .4)
    js(f'tl.set("#iring", {{opacity: 0}}, {t_inst + 1.22:.3f}); tl.set("#instt", {{opacity: 1, textContent: "Open"}}, {t_inst + 1.22:.3f});')
    js(f'tl.to("#inst", {{backgroundColor: "#2fbf71", duration: .2}}, {t_inst + 1.22:.3f});')
    sfx("ding", t_inst + 1.22); burst(t_inst + 1.25, 820, 960)
    js(f'tl.to("#appc", {{y: -150, scale: .82, duration: .4, ease: "power3.inOut"}}, {t_chk2 - .1:.3f});')
    ft2("#nxt", t_chk2, .4, "{opacity: 0, y: 200}", "{opacity: 1, y: 0}", "back.out(1.6)")
    for i in range(4):
        pop(f"#nr{i} i", t_chk2 + .35 + i * .16, .25, "{opacity: 0, scale: 2.2}")
        sfx("tick", t_chk2 + .35 + i * .16)
    ft2("#bypost2", t_bef - .05, .22, "{opacity: 0, scale: 2.4, rotation: -20}", "{opacity: 1, scale: 1, rotation: -7}", "power4.out")
    sfx("stamp", t_bef); punch(t_bef, 1.04)
for k in range(26):
    x0 = random.randint(60, 1020)
    HTMLS.append(f'<i class="cf" id="cfx{k}" style="background:{random.choice(("#ff5fb7", "#F343A2", "#ffd27a", "#2fbf71", "#ffffff"))};'
                 f'width:{random.randint(12, 20)}px;height:{random.randint(22, 32)}px"></i>')
    js(f'tl.fromTo("#cfx{k}", {{x: {x0}, y: -60, rotation: {random.randint(0, 180)}, opacity: 1}}, {{x: {x0 + random.uniform(-160, 160):.0f}, y: 2000, '
       f'rotation: {random.randint(360, 900)}, duration: {random.uniform(1.6, 2.4):.2f}, ease: "power1.in", immediateRender: false}}, {(T("k8", "checklist") if VERSION == "A" else T("k8", "before") + .2) + random.uniform(0, .3):.3f});')

# =====================================================================================================================
# Cree, the host: bottom right, reacting; centre for the CTA
CR, CC = P(935, 1815, .3), P(860, 1820, .36)
js(f'gsap.set("#cree", {{x: {CR[0] - PCX:.0f}, y: {CR[1] - PCY:.0f}, scale: {CR[2]}, opacity: 1}});')
js('gsap.set("#cree .cpose", {opacity: 0}); gsap.set("#cp-shock", {opacity: 1});')
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -7, duration: .6, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .6)}, immediateRender: false}}, 0);')
for k in range(int(DUR / 2.7)):
    blink(1.1 + k * 2.7)
cree_wiggle(t_until, 2, 7)
pose(t_four, "cheer", flip=True); cree_hop(t_four + .05, 70)
pose(t_ai, "mag", flip=True)
pose(t_num4, "point", flip=True); say(t_nobody, "!", .7, left=True)
for (bad_t, good_t, tick_t) in ((H["sense"], H["mute"] + .25, TICK[0]), (Pc["change"], Pc["two"] + .1, TICK[1]), (A["q"] + .2, A["music"], TICK[2])):
    pose(bad_t, "shock"); cree_wiggle(bad_t, 2, 6)
    pose(good_t, "proud"); cree_hop(tick_t, 60)
pose(E["rewatch"], "proud"); cree_hop(E["comment"] + .45, 60)
pose(E["stop"], "sad"); sweat(E["stop"] + .05, .8)
pose(Y["t"], "cheer"); cree_hop(T("k7", "yourself"), 70); sparkle(T("k7", "yourself"), .9)
pose(Y["upload"], "present", flip=True)
pose(t_cm, "wave", flip=True)
cree_hop(t_check + .62, 70, 2)

# drifting background dots and soft blobs
BG = "".join(f'<i class="blob" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{c}"></i>'
             for x, y, r, c in ((-120, 200, 520, "rgba(255,150,200,.35)"), (700, 1300, 600, "rgba(243,67,162,.22)"), (680, -100, 420, "rgba(255,210,120,.25)")))
js(f'tl.fromTo(".blob", {{x: 0, y: 0}}, {{x: (i) => [80, -90, 60][i], y: (i) => [-60, 80, 70][i], duration: {DUR / 2:.2f}, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#dots", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "0px 240px", duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')

SH = ["M0,-22 V22 M-22,0 H22", "M-20,0 A20,20 0 1,0 20,0 A20,20 0 1,0 -20,0", "M-24,8 Q-12,-12 0,8 T24,8", "M0,-22 L19,11 L-19,11 Z"]
for k in range(12):
    x, y = random.randint(40, 1040), random.randint(560, 1820)
    HTMLS.append(f'<svg class="fsh" id="fs{k}" style="left:{x}px;top:{y}px" viewBox="-30 -30 60 60"><path d="{SH[k % 4]}" fill="none" '
                 f'stroke="{random.choice(("#F343A2", "#ffb3d6", "#ffd23f", "#c9b3ff"))}" stroke-width="5" stroke-linecap="round"/></svg>')
    js(f'tl.fromTo("#fs{k}", {{y: 0, rotation: 0}}, {{y: {random.randint(-160, -60)}, rotation: {random.choice((-1, 1)) * random.randint(90, 270)}, '
       f'duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
for sel, t in ((".ed .sheen", .3), ("#mt3 .sheen", t_num4 + .1), (".cz .sheen", Y["score"] - .3), (".clip .sheen", Y["t"] + .9), *(((".pdf .sheen", T("k8", "DM") + .4),) if VERSION == "A" else ()), (".endreel .sheen", E["rewatch"])):
    js(f'tl.fromTo("{sel}", {{x: -700}}, {{x: 1400, duration: .8, ease: "power2.inOut", immediateRender: false}}, {t:.3f});')
for sid, t0 in (("s3", H["n"]), ("s4", Pc["n"]), ("s5", A["n"]), ("s6", E["n"])):
    js(f'tl.fromTo("#{sid} .ghost", {{y: 80, opacity: 0}}, {{y: -60, opacity: 1, duration: 3.5, ease: "power1.out", immediateRender: false}}, {t0 + .5:.3f});')

POST = " ".join(f'gsap.set("{sel}", {frm});' for sel, (t, frm) in sorted(FIRST.items(), key=lambda kv: kv[1][0]) if t > 0.0)
POST += (' gsap.set(".tc", {backgroundColor: "#ffffff", color: "#1a1020", scale: 1}); gsap.set(".tc .box", {backgroundColor: "rgba(0,0,0,0)", borderColor: "#d9c4d0"});'
         ' gsap.set(".led", {backgroundColor: "#e9d2de"}); gsap.set(".clip .box", {backgroundColor: "rgba(0,0,0,0)", borderColor: "#d9c4d0"});'
         ' gsap.set("#kv", {y: 220}); gsap.set("#km", {y: 20}); gsap.set("#wvv", {scaleY: .25}); gsap.set("#wvm", {scaleY: 1});'
         ' gsap.set("#ed", {scale: 1, opacity: 1, filter: "blur(0px)"}); gsap.set("#s0", {opacity: 1});')
CSS = open(os.path.join(ROOT, "build", "style.css")).read()
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: 4 checks before you post 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="bg" id="bgl">{BG}</div><div class="bg" id="dots"></div>
      <div id="stage">{S0}{S1}{S3}{S4}{S5}{S6}{S7}{S8}{S9}</div>
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
