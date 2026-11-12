"""GTA 6 creator playbook reel (AI.NXTLVL, 9:16): writes index.html and plan/sfx_events.json from plan/words.json.

Look: the AI.NXTLVL kit (near-black, violet star, Montserrat 800, Instrument Serif Italic accents, JetBrains Mono
labels) over Rockstar's own Vice City art (the GTA VI: The Album reel, owner's pick for the background) and their
GTA 6 footage (official promo clips, muted: CLAUDE.md exception). The proof beat is the owner's screen recording of
GTA clip pages (views on every tile). The AI clipper and the game setting stay unnamed / blurred on purpose (owner:
"keep the suspense", the comment unlocks them).

Beats (script in build/vo.py): p00 hook, p01-p02 proof, p03 step 1, p04 step 2, p05 locked cards, p06 CTA.
python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
VO = json.load(open(os.path.join(ROOT, "plan", "vo_pick.json")))
FPS = 30
NIGHT, DEEP, VIOLET, STAR, LAV = "#07050f", "#10022c", "#7f1bf8", "#7a2ffb", "#b687f9"
PINK, ORANGE, GREEN, RED = "#ff4fa3", "#ffb36b", "#38e08c", "#ff3b5c"

# Whisper's spelling where the take's word count differs from the script: "8 -hour" -> "8-hour"
_W = []
for w in W:
    if _W and w["w"].startswith("-") and _W[-1]["line"] == w["line"]:
        _W[-1] = {**_W[-1], "w": _W[-1]["w"] + w["w"], "t1": w["t1"]}
        continue
    _W.append(dict(w))
W = _W
ALIAS = {"eight": "8", "ten": "10"}
LINES = {}
for w in W:
    LINES.setdefault(w["line"], []).append(w)
L0 = {k: v[0]["t0"] for k, v in LINES.items()}
L1 = {k: v[-1]["t1"] for k, v in LINES.items()}
END = round(L1["p06"] + .45, 2)          # a beat on the end card after "early."
DUR = END


def T(line, word, n=0):
    """time a word starts (the n-th match in that line)"""
    keys = (word.lower(), ALIAS.get(word.lower(), word.lower()))
    hits = [w for w in LINES[line] if w["w"].lower().strip(".,:!?'\"").startswith(keys)]
    return hits[min(n, len(hits) - 1)]["t0"]


S1, S2, S3, S4, S5, S6 = L0["p01"] - .08, L0["p03"] - .08, L0["p04"] - .08, L0["p05"] - .08, L0["p06"] - .12, END
JS, SFX = [], []


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def show(sel, t, d=.3, frm="{opacity: 0, y: 40}", to="{opacity: 1, y: 0}", ease="back.out(1.7)"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def hide(sel, t, d=.2):
    js(f'tl.to("{sel}", {{opacity: 0, duration: {d}, ease: "power2.in"}}, {t:.3f});')


def cut(t, big=False):
    """scene change: a white flash, a punch-in on the stage, a whoosh"""
    js(f'tl.fromTo("#flash", {{opacity: .85}}, {{opacity: 0, duration: .22, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#stage", {{scale: 1.08}}, {{scale: 1, duration: .45, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    sfx("whoosh_big" if big else "whoosh", t - .12)


# ---- scenes ---------------------------------------------------------------------------------------------------------
HTML = []

# v2 (owner: "use the best of the best scenes from all of the videos... add more animations or clips and improve
# background"): the picture is a run of Rockstar plates (build/clips.sh), cut on the words; behind the panels they play
# blurred and dark so the panels read, and a Vice City grade, drifting light leaks and film grain sit over everything.
PLATES = []


def plate(vid, src, t0, t1, media=0.0, cls="full", push=(1.0, 1.07)):
    HTML.append(f'<video id="{vid}" class="{cls}" src="assets/video/{src}.mp4" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
                f'data-media-start="{media:.3f}" data-track-index="{1 + len(PLATES) % 2}" muted playsinline></video>')
    js(f'tl.fromTo("#{vid}", {{scale: {push[0]}}}, {{scale: {push[1]}, duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    PLATES.append((vid, src, t0, t1))


def mini_cut(t):
    js(f'tl.fromTo("#flash", {{opacity: .45}}, {{opacity: 0, duration: .14, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    sfx("swish", t - .06)


_tg, _td, _ts, _to = .0, T("p00", "drops"), T("p00", "Save"), T("p00", "only")
plate("h1", "c_flip", 0, _td + .25, .0, push=(1.12, 1.0))
plate("h2", "r_sky", _td + .25, _ts - .05, .5)
plate("h3", "c_heli", _ts - .05, _to - .05, .2)
plate("h4", "c_scoot", _to - .05, S1, .3)
for t in (_td + .25, _ts - .05, _to - .05):
    mini_cut(t)
_tp, _tst, _tm = T("p01", "police"), T("p01", "streamer"), T("p02", "Millions")
plate("pr1", "proof", S1, _tp - .05, .4)
plate("pr2", "c_truck", _tp - .05, _tst - .05, .3, push=(1.15, 1.02))
plate("vproof", "proof", _tst - .05, S2, 2.6)
mini_cut(_tp - .05)
mini_cut(_tst - .05)
_t1h = T("p03", "ten")
plate("s1a", "c_boat", S2, _t1h - .3, .2, "full plate")
plate("s1b", "c_ball", _t1h - .3, S3, .1, "full plate")
_tcl = T("p04", "claimed")
plate("s2a", "c_cops", S3, _tcl - .1, .1, "full plate")
plate("s2b", "c_truck", _tcl - .1, S4, 1.0, "full plate")
_tkw = T("p05", "keyword")
plate("s3a", "c_gym", S4, _tkw - .1, .2, "full plate")
plate("s3b", "c_dive", _tkw - .1, S5, .0, "full plate")
plate("cta1", "vc_full", S5, S6, 26.4, push=(1.0, 1.06))
HTML.append('<div id="grade" class="full"></div><div id="leak1" class="leak"></div><div id="leak2" class="leak"></div>'
            '<div id="tint" class="full"></div><div id="vig" class="full"></div><div id="grain" class="full"></div>')
js(f'tl.fromTo("#leak1", {{x: -420, y: -260, opacity: .55}}, {{x: 380, y: 520, opacity: .85, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#leak2", {{x: 420, y: 1500, opacity: .35}}, {{x: -360, y: 900, opacity: .7, duration: {DUR:.2f}, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#grain", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "1536px 1024px", duration: {DUR:.2f}, '
   f'ease: "steps({int(DUR * 12)})", immediateRender: false}}, 0);')

# hook
HTML.append('<div class="sc" id="hook">'
            '<div id="gta"><img id="kart" src="assets/img/keyart.jpg"><div id="shine"></div></div>'
            '<div class="chip date" id="date">DROPS NOV 19</div>'
            '<div class="chip save" id="save"><svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z"/></svg>SAVE THIS</div>'
            '<div id="only"><div class="l1">THE ONLY</div><div class="l2">GTA 6 CREATOR</div><div class="l3">VIDEO <i>you\'ll need.</i></div></div>'
            '<img id="rlogo" src="assets/img/rockstar_logo.jpg">'
            '</div>')
t_gta, t_nine, t_save, t_only = T("p00", "GTA"), T("p00", "nineteenth"), T("p00", "Save"), T("p00", "only")
show("#gta", t_gta, .4, "{opacity: 0, scale: 1.7, rotation: -14}", "{opacity: 1, scale: 1, rotation: -3}", "expo.out")
js(f'tl.fromTo("#kart", {{scale: 1.0}}, {{scale: 1.14, duration: {S1 - t_gta:.3f}, ease: "none", immediateRender: false}}, {t_gta:.3f});')
js(f'tl.fromTo("#gta", {{boxShadow: "0 0 0 4px rgba(255,255,255,.9), 0 0 40px rgba(255,79,163,.4)"}}, '
   f'{{boxShadow: "0 0 0 4px rgba(255,255,255,.9), 0 0 110px rgba(255,79,163,.9)", duration: .5, yoyo: true, repeat: 5, immediateRender: false}}, {t_gta + .4:.3f});')
sfx("impact", t_gta)
js(f'tl.fromTo("#shine", {{x: -900}}, {{x: 900, duration: .7, ease: "power2.inOut", immediateRender: false}}, {t_gta + .35:.3f});')
sfx("whoosh_big", t_gta - .15)
show("#rlogo", t_gta + .15, .3, "{opacity: 0, scale: .6, rotation: -12}", "{opacity: 1, scale: 1, rotation: 0}")
show("#date", t_nine, .28)
sfx("pop", t_nine)
js(f'tl.to("#gta", {{y: -480, scale: .5, rotation: 0, duration: .4, ease: "expo.inOut"}}, {t_save - .05:.3f});')
hide("#date", t_save - .05, .15)
show("#save", t_save, .3, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}")
sfx("click", t_save)
show("#only .l1", t_only - .02, .25)
show("#only .l2", t_only + .12, .25)
show("#only .l3", T("p00", "video") - .02, .3)
sfx("swish", t_only)
hide("#hook", S1 - .05, .08)

# proof: the clip pages, views on every tile
HTML.append('<div class="sc" id="proof"><div class="lab" id="plab">GTA RP CLIP PAGES</div>'
            '<div class="tag" id="tg1">POLICE CHASE</div><div class="tag" id="tg2">STREAMER LOSING IT</div>'
            '<div class="tag hot" id="tg3">CLIPPED IN MINUTES</div>'
            '<div id="views"><div id="vnum">0</div><div id="vlab">VIEWS</div></div>'
            + "".join(f'<div class="vb" id="vb{i}" style="left:{x}px;top:{y}px">&#9654; {v}</div>'
                      for i, (x, y, v) in enumerate([(90, 1050, "23.4M"), (640, 980, "30.5M"), (360, 1180, "12.1M"), (720, 1240, "20.3M"),
                                                     (120, 1300, "4.8M"), (560, 1120, "6.9M")]))
            + '</div>')
cut(S1, True)
show("#plab", S1 + .1, .3)
show("#tg1", T("p01", "police"), .28, "{opacity: 0, x: -80}", "{opacity: 1, x: 0}")
sfx("screech", T("p01", "police"))
show("#tg2", T("p01", "streamer"), .28, "{opacity: 0, x: 80}", "{opacity: 1, x: 0}")
sfx("pop", T("p01", "streamer"))
show("#tg3", T("p01", "clipped"), .28, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}")
sfx("shutter", T("p01", "clipped"))
for i, t in enumerate([T("p01", "grew"), T("p01", "exactly"), T("p01", "chase"), T("p01", "losing"), T("p01", "clipped"), T("p01", "minutes")]):
    show(f"#vb{i}", t, .25, "{opacity: 0, scale: .4, y: 40}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.5)")
    js(f'tl.to("#vb{i}", {{y: -260, opacity: 0, duration: 1.4, ease: "power1.in"}}, {t + .35:.3f});')
    sfx("pop", t)
t_mil = T("p02", "Millions")
js(f'tl.to(["#tg1", "#tg2", "#tg3"], {{opacity: 0, y: -40, duration: .18, stagger: .04}}, {t_mil - .2:.3f});')
js(f'tl.to("#vproof", {{filter: "brightness(.45) blur(6px)", duration: .3}}, {t_mil - .1:.3f});')
show("#views", t_mil, .35, "{opacity: 0, scale: 1.7}", "{opacity: 1, scale: 1}", "expo.out")
js(f'const vc = {{v: 0}}; tl.to(vc, {{v: 30.5, duration: .9, ease: "power3.out", onUpdate: () => {{ '
   f'document.getElementById("vnum").textContent = vc.v.toFixed(1) + "M"; }}}}, {t_mil:.3f});')
sfx("impact", t_mil)
sfx("cash", t_mil + .75)
hide("#proof", S2 - .05, .08)

# step 1: the AI clipper (name blurred)
thumbs = "".join(f'<div class="th" id="th{i}"><div class="im" style="background-position:{(i % 5) * 25}% {(i // 5) * 100}%"></div>'
                 f'<span>READY</span></div>' for i in range(10))
HTML.append('<div class="sc" id="st1"><div class="step">STEP <b>01</b></div>'
            '<div class="panel" id="tool"><div class="ph"><div class="dot"></div><div class="blurname">Clipr Pro AI</div>'
            '<div class="tiny" id="pct">CLIPPING 0%</div></div>'
            '<div id="bar"><div class="bt">STREAM.mp4</div><div class="bd">8:00:00</div><div id="wave"></div><div id="scan"></div></div>'
            f'<div id="grid">{thumbs}</div></div></div>')
cut(S2)
show("#st1 .step", S2 + .05, .3, "{opacity: 0, x: -60}", "{opacity: 1, x: 0}")
show("#tool", S2 + .12, .4, "{opacity: 0, y: 80, scale: .94}", "{opacity: 1, y: 0, scale: 1}")
t_8h = T("p03", "eight")
js(f'tl.fromTo("#scan", {{x: 0}}, {{x: 860, duration: {max(.6, T("p03", "ten") - t_8h):.3f}, ease: "none", immediateRender: false}}, {t_8h:.3f});')
sfx("riser_short", t_8h)
js(f'const pc = {{v: 0}}; tl.to(pc, {{v: 100, duration: {max(.6, T("p03", "ten") - t_8h):.3f}, ease: "power1.inOut", onUpdate: () => {{ '
   f'document.getElementById("pct").textContent = "CLIPPING " + Math.round(pc.v) + "%"; }}}}, {t_8h:.3f});')
js(f'tl.set("#pct", {{color: "{GREEN}"}}, {T("p03", "ten"):.3f});')
t_ten = T("p03", "ten")
js(f'tl.to("#bar", {{scaleY: .4, opacity: .35, duration: .25, ease: "power2.in"}}, {t_ten - .05:.3f});')
for i in range(10):
    t = t_ten + .06 * i
    show(f"#th{i}", t, .25, "{opacity: 0, scale: .4, y: -60}", "{opacity: 1, scale: 1, y: 0}")
    if i % 2 == 0:
        sfx("tick", t)
js(f'tl.to(".th span", {{opacity: 1, duration: .15, stagger: .05}}, {T("p03", "ready"):.3f});')
sfx("notify", T("p03", "ready"))
hide("#st1", S3 - .05, .08)

# step 2: the one game setting (blurred), paid or claimed
HTML.append('<div class="sc" id="st2"><div class="step">STEP <b>02</b></div>'
            '<div class="panel" id="set"><div class="sh">SETTINGS <span>/ AUDIO</span></div>'
            '<div class="row"><span>Master Volume</span><i style="--v:.8"></i></div>'
            '<div class="row key" id="keyrow"><span class="blurname">In-game Radio</span><i style="--v:.6"></i><em>?</em></div>'
            '<div class="row"><span>Dialogue</span><i style="--v:.9"></i></div>'
            '<div class="row"><span>Subtitles</span><i style="--v:.5"></i></div></div>'
            '<svg id="cursor" viewBox="0 0 24 24"><path d="M4 2l16 9-7 2-3 7z"/></svg><div id="ripple"></div>'
            '<div class="stamp paid" id="paid">PAID</div><div class="stamp claimed" id="claimed">CLAIMED</div></div>')
cut(S3)
show("#st2 .step", S3 + .05, .3, "{opacity: 0, x: -60}", "{opacity: 1, x: 0}")
show("#set", S3 + .1, .4, "{opacity: 0, y: 80, scale: .94}", "{opacity: 1, y: 0, scale: 1}")
t_set = T("p04", "setting")
js(f'tl.fromTo("#keyrow", {{boxShadow: "0 0 0 0 rgba(255,79,163,0)"}}, {{boxShadow: "0 0 0 6px rgba(255,79,163,.9), 0 0 60px rgba(255,79,163,.6)", '
   f'duration: .3, immediateRender: false}}, {t_set:.3f});')
sfx("click", t_set)
js(f'tl.fromTo("#cursor", {{opacity: 0, x: 380, y: 420}}, {{opacity: 1, x: 0, y: 0, duration: .45, ease: "power3.out", immediateRender: false}}, {t_set - .45:.3f});')
js(f'tl.to("#cursor", {{scale: .8, duration: .07, yoyo: true, repeat: 1}}, {t_set:.3f});')
js(f'tl.fromTo("#ripple", {{opacity: .9, scale: .2}}, {{opacity: 0, scale: 2.4, duration: .45, ease: "power2.out", immediateRender: false}}, {t_set:.3f});')
t_paid, t_cl = T("p04", "paid"), T("p04", "claimed")
show("#paid", t_paid, .25, "{opacity: 0, scale: 2.2, rotation: -24}", "{opacity: 1, scale: 1, rotation: -12}", "expo.out")
sfx("cash", t_paid)
js(f'tl.to("#paid", {{opacity: 0, scale: .8, duration: .15}}, {t_cl - .08:.3f});')
show("#claimed", t_cl, .25, "{opacity: 0, scale: 2.2, rotation: 20}", "{opacity: 1, scale: 1, rotation: 8}", "expo.out")
sfx("stamp", t_cl)
sfx("buzzer", t_cl + .05)
js(f'tl.fromTo("#stage", {{x: -14}}, {{x: 0, duration: .3, ease: "elastic.out(1, .3)", immediateRender: false}}, {t_cl:.3f});')
hide("#st2", S4 - .05, .08)

# the music rule and the keyword trick: locked
lines = "".join(f'<div class="fl" style="width:{w}%"></div>' for w in (92, 78, 85, 60))
HTML.append('<div class="sc" id="st3">'
            f'<div class="lock" id="lk1"><div class="lt">THE <b>MUSIC RULE</b></div><div class="fx">{lines}</div>'
            '<svg class="pad" viewBox="0 0 24 24"><path d="M7 10V7a5 5 0 0 1 10 0v3h1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V11a1 1 0 0 1 1-1zm2 0h6V7a3 3 0 0 0-6 0z"/></svg></div>'
            f'<div class="lock" id="lk2"><div class="lt">THE <b>KEYWORD TRICK</b></div><div class="fx">{lines}</div>'
            '<svg class="pad" viewBox="0 0 24 24"><path d="M7 10V7a5 5 0 0 1 10 0v3h1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V11a1 1 0 0 1 1-1zm2 0h6V7a3 3 0 0 0-6 0z"/></svg></div>'
            '<div id="miss">MOST GTA PAGES WILL MISS THIS</div></div>')
cut(S4)
t_mus, t_key, t_miss = T("p05", "music"), T("p05", "keyword"), T("p05", "miss")
show("#lk1", t_mus - .1, .35, "{opacity: 0, x: -200, rotation: -6}", "{opacity: 1, x: 0, rotation: -3}")
sfx("lock", t_mus + .15)
show("#lk2", t_key - .1, .35, "{opacity: 0, x: 200, rotation: 6}", "{opacity: 1, x: 0, rotation: 3}")
sfx("lock", t_key + .15)
for sel, t in (("#lk1 .pad", t_mus + .15), ("#lk2 .pad", t_key + .15)):
    js(f'tl.fromTo("{sel}", {{rotation: -16}}, {{rotation: 0, duration: .6, ease: "elastic.out(1.2,.3)", immediateRender: false}}, {t:.3f});')
js(f'tl.fromTo(".fx", {{opacity: .55}}, {{opacity: 1, duration: .09, yoyo: true, repeat: 15, ease: "steps(1)", immediateRender: false}}, {t_mus:.3f});')
show("#miss", t_miss - .25, .3, "{opacity: 0, scale: 1.4}", "{opacity: 1, scale: 1}")
sfx("riser", S5 - 1.0)
hide("#st3", S5 - .05, .08)

# CTA
HTML.append('<div class="sc" id="cta"><div id="ctadim"></div><div class="ct1">COMMENT</div><div id="kw">GTA6</div>'
            '<div class="ct2">and I\'ll send you <i>all of it.</i></div>'
            '<div id="follow"><span>+</span> FOLLOW <b>· BE EARLY</b></div>'
            '<div id="cbox"><div id="ctext">Add a comment...</div><div id="csend">&#10148;</div></div>'
            '<div id="dm"><div class="dmi">&#9993;</div><div><b>New message</b><span>Your GTA 6 playbook is here</span></div></div>'
            '</div>')   # owner: no "Rockstar x nxtlvl" row, no page tag
cut(S5, True)
sfx("impact", S5)
show("#ctadim", S5, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
show(".ct1", S5 + .05, .3)
show("#kw", T("p06", "GTA") - .05, .4, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "expo.out")
js(f'tl.fromTo("#kw", {{textShadow: "0 0 0px {PINK}"}}, {{textShadow: "0 0 50px {PINK}", duration: .6, yoyo: true, repeat: 3, '
   f'immediateRender: false}}, {T("p06", "GTA") + .35:.3f});')
show("#cbox", T("p06", "GTA") + .05, .3, "{opacity: 0, y: 60}", "{opacity: 1, y: 0}")
_ty = T("p06", "GTA") + .35
js(f'const ty = {{n: 0}}; tl.to(ty, {{n: 4, duration: .5, ease: "steps(4)", onUpdate: () => {{ const e = document.getElementById("ctext"); '
   f'e.textContent = "GTA6".slice(0, Math.round(ty.n)) || "Add a comment..."; e.style.color = ty.n > 0 ? "#fff" : "rgba(255,255,255,.5)"; }}}}, {_ty:.3f});')
for k in range(4):
    sfx("tick", _ty + .125 * k)
js(f'tl.fromTo("#csend", {{scale: 1}}, {{scale: 1.35, duration: .12, yoyo: true, repeat: 1, immediateRender: false}}, {_ty + .6:.3f});')
sfx("click", _ty + .6)
show("#dm", T("p06", "send") + .1, .4, "{opacity: 0, y: -160}", "{opacity: 1, y: 0}", "back.out(1.6)")
sfx("notify", T("p06", "send") + .15)
show(".ct2", T("p06", "send"), .3)
show("#follow", T("p06", "follow"), .3, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}")
sfx("click", T("p06", "follow"))
js(f'tl.to("#follow", {{scale: .92, duration: .08, yoyo: true, repeat: 1}}, {T("p06", "follow") + .45:.3f});')

# captions: the spoken words, 2-3 at a time, under the action (not on the hook or the CTA, which carry their own type)
KEY = {"police", "chase", "streamer", "minutes", "millions", "ai", "8-hour", "10", "setting", "paid", "claimed", "music",
       "keyword", "miss"}
caps = []
for lid in ("p01", "p02", "p03", "p04", "p05"):
    ws = LINES[lid]
    grp = []
    for w in ws:
        grp.append(w)
        end_punct = w["w"][-1] in ",.:!?"
        if len(grp) == 3 or end_punct or w is ws[-1]:
            caps.append(grp)
            grp = []
for i, g in enumerate(caps):
    t0, t1 = g[0]["t0"] - .03, (caps[i + 1][0]["t0"] - .03) if i + 1 < len(caps) else g[-1]["t1"] + .2
    t1 = min(t1, g[-1]["t1"] + .35)
    words = " ".join(f'<span class="{"k" if w["w"].lower().strip(".,:!?").replace("…", "") in KEY else ""}">'
                     f'{w["w"].strip(".,:")}</span>' for w in g)
    HTML.append(f'<div class="cap" id="cap{i}">{words}</div>')
    show(f"#cap{i}", t0, .14, "{opacity: 0, scale: .85, y: 12}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.4)")
    js(f'tl.set("#cap{i}", {{opacity: 0}}, {t1:.3f});')

CSS = f"""
@font-face {{ font-family: "Montserrat"; src: url("assets/fonts/montserrat.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: "Serif"; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); font-style: italic; }}
@font-face {{ font-family: "Mono"; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); font-weight: 700; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; font-family: Montserrat; color: #fff; }}
#stage {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.full {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
.plate {{ filter: blur(3px) brightness(.72) saturate(1.3); }}
#grade {{ background: linear-gradient(170deg, rgba(127,27,248,.38) 0%, rgba(255,79,163,.22) 45%, rgba(255,179,107,.2) 100%);
  mix-blend-mode: soft-light; }}
.leak {{ position: absolute; left: 0; top: 0; width: 900px; height: 900px; border-radius: 50%; mix-blend-mode: screen; pointer-events: none;
  filter: blur(40px); }}
#leak1 {{ background: radial-gradient(circle, rgba(255,79,163,.55), rgba(255,79,163,0) 65%); }}
#leak2 {{ background: radial-gradient(circle, rgba(127,27,248,.6), rgba(127,27,248,0) 65%); }}
#grain {{ background-image: url("assets/img/grain.png"); background-size: 512px 512px; opacity: .07; mix-blend-mode: overlay; }}
#shine {{ position: absolute; top: -40px; bottom: -40px; left: 50%; width: 180px; margin-left: -90px; opacity: .9;
  background: linear-gradient(100deg, transparent, rgba(255,255,255,.85), transparent); mix-blend-mode: overlay; }}
#gta {{ overflow: hidden; }}
#hook #gta {{ left: 50px; right: auto; top: 560px; text-align: left; width: 980px; height: 653px; border-radius: 30px; overflow: hidden; line-height: 0; }}
#kart {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.vb {{ position: absolute; padding: 12px 22px; border-radius: 999px; background: rgba(7,5,15,.8); border: 2px solid {PINK}; font-weight: 900;
  font-size: 40px; color: #fff; box-shadow: 0 10px 40px rgba(255,79,163,.45); }}
#pct {{ font-weight: 700; }}
#cursor {{ position: absolute; left: 820px; top: 700px; width: 80px; height: 80px; fill: #fff; stroke: {NIGHT}; stroke-width: 1.2;
  filter: drop-shadow(0 6px 14px rgba(0,0,0,.6)); z-index: 12; }}
#ripple {{ position: absolute; left: 790px; top: 670px; width: 90px; height: 90px; border-radius: 50%; border: 5px solid {PINK}; z-index: 11; }}
#cbox {{ top: 1250px; left: 90px; right: 90px; display: flex; align-items: center; justify-content: space-between; padding: 26px 34px;
  border-radius: 999px; background: rgba(255,255,255,.12); border: 2px solid rgba(255,255,255,.35); text-align: left; }}
#ctext {{ font-weight: 800; font-size: 46px; color: rgba(255,255,255,.5); }}
#csend {{ width: 76px; height: 76px; border-radius: 50%; background: {PINK}; color: #fff; font-size: 40px; line-height: 76px; text-align: center; }}
#dm {{ top: 200px; left: 70px; right: 70px; display: flex; align-items: center; gap: 24px; padding: 26px 30px; border-radius: 30px;
  background: rgba(255,255,255,.95); color: {NIGHT}; text-align: left; box-shadow: 0 20px 60px rgba(7,5,15,.6); }}
#dm .dmi {{ width: 84px; height: 84px; border-radius: 22px; background: linear-gradient(135deg, {VIOLET}, {PINK}); color: #fff; font-size: 46px;
  line-height: 84px; text-align: center; flex: none; }}
#dm b {{ display: block; font-size: 38px; font-weight: 900; }}
#dm span {{ display: block; font-size: 34px; font-weight: 600; opacity: .75; }}
#tint {{ background: linear-gradient(180deg, rgba(16,2,44,.55) 0%, rgba(16,2,44,.05) 30%, rgba(16,2,44,.1) 60%, rgba(7,5,15,.75) 100%); }}
#vig {{ background: radial-gradient(120% 80% at 50% 45%, transparent 55%, rgba(7,5,15,.7) 100%); }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; mix-blend-mode: screen; }}
#topbar {{ position: absolute; left: 56px; right: 56px; top: 92px; display: flex; align-items: center; justify-content: space-between; z-index: 40; }}
#topbar .h {{ font-family: Mono; font-size: 30px; letter-spacing: .14em; color: #fff; padding: 10px 18px; border-radius: 12px;
  background: rgba(16,2,44,.55); border: 2px solid rgba(182,135,249,.5); }}
#topbar .h b {{ color: {LAV}; }}
#topbar img {{ height: 52px; filter: drop-shadow(0 4px 16px rgba(0,0,0,.6)); }}
.sc {{ position: absolute; inset: 0; z-index: 10; }}
.sc > * {{ opacity: 0; }}
#hook > * {{ position: absolute; }}
#gta {{ left: 0; right: 0; top: 520px; text-align: center; font-weight: 900; line-height: .8; letter-spacing: -.04em; }}
#gta span {{ font-size: 250px; background: linear-gradient(180deg, #fff 20%, {LAV}); -webkit-background-clip: text; color: transparent;
  filter: drop-shadow(0 10px 40px rgba(127,27,248,.7)); }}
#gta b {{ font-size: 330px; margin-left: 20px; background: linear-gradient(160deg, {ORANGE}, {PINK} 50%, {VIOLET}); -webkit-background-clip: text;
  color: transparent; filter: drop-shadow(0 10px 50px rgba(255,79,163,.7)); }}
.chip {{ left: 50%; transform: translateX(-50%); padding: 18px 34px; border-radius: 999px; font-weight: 800; font-size: 44px; letter-spacing: .06em; white-space: nowrap; }}
.chip.date {{ top: 900px; background: {PINK}; color: {NIGHT}; box-shadow: 0 12px 50px rgba(255,79,163,.6); }}
.chip.save {{ top: 640px; background: #fff; color: {NIGHT}; display: flex; align-items: center; gap: 14px; }}
.chip.save svg {{ width: 44px; height: 44px; fill: {VIOLET}; }}
#only {{ opacity: 1; left: 40px; right: 40px; top: 780px; text-align: center; font-weight: 900; line-height: 1.04; white-space: nowrap; letter-spacing: -.035em; text-transform: uppercase; }}
#only > div {{ opacity: 0; }}
#only .l1 {{ font-size: 104px; text-shadow: 0 8px 40px rgba(7,5,15,.8); }}
#only .l2 {{ font-size: 96px; filter: drop-shadow(0 8px 30px rgba(7,5,15,.8)); background: linear-gradient(90deg, {ORANGE}, {PINK} 45%, {LAV}); -webkit-background-clip: text; color: transparent; }}
#only .l3 {{ font-size: 104px; text-shadow: 0 8px 40px rgba(7,5,15,.8); }}
#only i {{ font-family: Serif; font-weight: 400; text-transform: none; letter-spacing: 0; font-size: 104px; color: {LAV}; }}
#rlogo {{ right: 70px; top: 300px; width: 130px; height: 130px; border-radius: 28px; box-shadow: 0 12px 40px rgba(0,0,0,.5); }}
#proof > * {{ position: absolute; }}
.lab {{ left: 56px; top: 200px; font-family: Mono; font-size: 32px; letter-spacing: .14em; padding: 10px 18px; border-radius: 10px; background: {VIOLET}; }}
.tag {{ left: 70px; padding: 22px 34px; border-radius: 22px; font-weight: 900; font-size: 60px; letter-spacing: -.01em; background: rgba(16,2,44,.85);
  border: 3px solid {LAV}; box-shadow: 0 14px 50px rgba(0,0,0,.5); }}
#tg1 {{ top: 470px; }} #tg2 {{ top: 640px; left: auto; right: 70px; }}
#tg3 {{ top: 810px; left: 50%; margin-left: -330px; background: {PINK}; border-color: #fff; color: {NIGHT}; }}
#views {{ left: 0; right: 0; top: 560px; text-align: center; }}
#vnum {{ font-weight: 900; font-size: 300px; letter-spacing: -.05em; line-height: 1; background: linear-gradient(180deg, #fff, {PINK});
  -webkit-background-clip: text; color: transparent; filter: drop-shadow(0 12px 60px rgba(255,79,163,.6)); }}
#vlab {{ font-family: Mono; font-size: 64px; letter-spacing: .4em; color: {LAV}; margin-top: 10px; }}
.step {{ position: absolute; left: 70px; top: 230px; font-family: Mono; font-size: 40px; letter-spacing: .2em; color: {LAV}; }}
.step b {{ font-family: Montserrat; font-weight: 900; font-size: 130px; letter-spacing: -.04em; color: #fff; vertical-align: -22px; margin-left: 8px; }}
.panel {{ position: absolute; left: 60px; right: 60px; top: 470px; padding: 34px; border-radius: 36px; background: rgba(16,2,44,.82);
  border: 2px solid rgba(182,135,249,.45); box-shadow: 0 30px 90px rgba(7,5,15,.7), inset 0 1px 0 rgba(255,255,255,.12); backdrop-filter: blur(14px); }}
.ph {{ display: flex; align-items: center; gap: 18px; margin-bottom: 26px; }}
.ph .dot {{ width: 22px; height: 22px; border-radius: 50%; background: {GREEN}; box-shadow: 0 0 16px {GREEN}; }}
.blurname {{ font-weight: 800; font-size: 44px; filter: blur(11px); }}
.ph .tiny {{ margin-left: auto; font-family: Mono; font-size: 26px; color: {LAV}; letter-spacing: .12em; }}
#bar {{ position: relative; height: 150px; border-radius: 20px; background: linear-gradient(90deg, rgba(127,27,248,.35), rgba(255,79,163,.35));
  overflow: hidden; transform-origin: 50% 0; }}
#bar .bt, #bar .bd {{ position: absolute; top: 16px; font-family: Mono; font-size: 28px; }}
#bar .bt {{ left: 20px; }} #bar .bd {{ right: 20px; color: {ORANGE}; }}
#wave {{ position: absolute; left: 20px; right: 20px; bottom: 18px; height: 70px;
  background: repeating-linear-gradient(90deg, rgba(255,255,255,.75) 0 4px, transparent 4px 11px);
  -webkit-mask: linear-gradient(180deg, transparent, #000 30%, #000 70%, transparent); opacity: .65; }}
#scan {{ position: absolute; left: 20px; top: 0; bottom: 0; width: 6px; background: #fff; box-shadow: 0 0 24px #fff, 0 0 60px {PINK}; }}
#grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-top: 22px; }}
.th {{ position: relative; aspect-ratio: 9 / 16; border-radius: 14px; overflow: hidden; opacity: 0; border: 2px solid rgba(255,255,255,.25); }}
.th .im {{ position: absolute; inset: 0; background-image: url("assets/img/thumbs.jpg"); background-size: 500% 200%; }}
.th span {{ position: absolute; left: 6px; right: 6px; bottom: 8px; text-align: center; padding: 4px 0; border-radius: 8px; background: {GREEN};
  color: {NIGHT}; font-weight: 900; font-size: 20px; opacity: 0; }}
.sh {{ font-family: Mono; font-size: 34px; letter-spacing: .14em; margin-bottom: 18px; }}
.sh span {{ color: {LAV}; }}
.row {{ display: flex; align-items: center; gap: 20px; padding: 26px 22px; border-radius: 18px; font-weight: 700; font-size: 42px; margin-top: 10px;
  background: rgba(255,255,255,.05); }}
.row span {{ width: 430px; }}
.row i {{ flex: 1; height: 16px; border-radius: 99px; background: linear-gradient(90deg, {LAV} calc(var(--v) * 100%), rgba(255,255,255,.15) 0); }}
.row.key {{ background: rgba(255,79,163,.16); }}
.row em {{ font-style: normal; font-weight: 900; color: {PINK}; font-size: 50px; }}
.stamp {{ position: absolute; left: 50%; top: 1060px; margin-left: -330px; width: 660px; text-align: center; padding: 18px 0; border-radius: 22px;
  font-weight: 900; font-size: 128px; letter-spacing: .04em; border: 10px solid; background: rgba(7,5,15,.55); }}
.stamp.paid {{ color: {GREEN}; border-color: {GREEN}; box-shadow: 0 0 80px rgba(56,224,140,.5); }}
.stamp.claimed {{ color: {RED}; border-color: {RED}; box-shadow: 0 0 80px rgba(255,59,92,.55); }}
.lock {{ position: absolute; left: 80px; right: 80px; height: 340px; border-radius: 34px; padding: 40px; background: rgba(16,2,44,.85);
  border: 3px solid rgba(182,135,249,.6); box-shadow: 0 30px 90px rgba(7,5,15,.7); overflow: hidden; }}
#lk1 {{ top: 330px; }} #lk2 {{ top: 760px; }}
.lt {{ font-weight: 800; font-size: 58px; letter-spacing: -.01em; }}
.lt b {{ font-weight: 900; background: linear-gradient(90deg, {ORANGE}, {PINK}); -webkit-background-clip: text; color: transparent; }}
.fx {{ margin-top: 30px; filter: blur(9px); }}
.fl {{ height: 26px; border-radius: 12px; background: rgba(255,255,255,.55); margin-top: 18px; }}
.pad {{ position: absolute; right: 50px; top: 120px; width: 150px; height: 150px; fill: #fff; filter: drop-shadow(0 0 30px {PINK}); }}
#miss {{ position: absolute; left: 0; right: 0; top: 1200px; text-align: center; font-family: Mono; font-size: 40px; letter-spacing: .1em; color: {ORANGE}; }}
#cta > * {{ position: absolute; left: 0; right: 0; text-align: center; }}
#ctadim {{ top: 0; bottom: 0; background: radial-gradient(90% 55% at 50% 42%, rgba(7,5,15,.82), rgba(16,2,44,.55) 70%, rgba(7,5,15,.4)); }}
.ct1 {{ top: 470px; font-family: Mono; font-size: 64px; letter-spacing: .4em; }}
#kw {{ top: 570px; font-weight: 900; font-size: 300px; letter-spacing: -.05em; line-height: 1;
  background: linear-gradient(170deg, #fff 10%, {ORANGE} 35%, {PINK} 60%, {VIOLET}); -webkit-background-clip: text; color: transparent;
  filter: drop-shadow(0 0 2px #fff) drop-shadow(0 16px 60px rgba(255,79,163,.8)); }}
.ct2 {{ top: 930px; font-weight: 800; font-size: 64px; }}
.ct2 i {{ font-family: Serif; font-weight: 400; font-size: 80px; color: {LAV}; }}
#follow {{ top: 1100px; left: 50%; right: auto; margin-left: -310px; width: 620px; padding: 26px 0; border-radius: 999px; background: #fff; color: {NIGHT};
  font-weight: 900; font-size: 50px; box-shadow: 0 16px 60px rgba(127,27,248,.6); }}
#follow span {{ color: {VIOLET}; }} #follow b {{ color: {PINK}; font-weight: 900; }}
#brand {{ top: 1300px; display: flex; align-items: center; justify-content: center; gap: 30px; }}
#brand .rl {{ width: 110px; height: 110px; border-radius: 24px; }}
#brand span {{ font-size: 50px; color: {LAV}; }}
#brand .wm {{ height: 74px; }}
.cap {{ position: absolute; left: 60px; right: 60px; top: 1390px; text-align: center; font-weight: 900; font-size: 74px; line-height: 1.05;
  letter-spacing: -.02em; text-transform: uppercase; z-index: 30; opacity: 0; text-shadow: 0 6px 30px rgba(7,5,15,.9), 0 2px 0 rgba(7,5,15,.9); }}
.cap .k {{ color: {PINK}; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>GTA 6 creator playbook 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="{FPS}" data-width="1080" data-height="1920">
      <div id="stage">
        {chr(10).join(HTML)}
      </div>
      <div id="flash"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {"hook": [0, S1], "proof": [S1, S2], "step1": [S2, S3], "step2": [S3, S4], "locked": [S4, S5], "cta": [S5, S6]}},
          open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(caps)} captions, {len(SFX)} sfx")
