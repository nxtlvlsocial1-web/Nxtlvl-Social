"""Apoorva AI true-or-false quiz (9:16), v2: writes index.html, plan/sfx_events.json and plan/edit.json from plan/events.json.

v2 (owner on v1: "Remove the background music and fix this alignment her face got covered with this, so adjust all these
overlays accordingly, make them small... can you use better sfx for this context, the video still feels very dull...
maybe add a little cute mascot that reacts and does his thing as per the script"):
- no music (build/render_*.sh mix with --no-music);
- everything off her face: a slim tracker at the very top; one compact card at the bottom (y 1420-1620) that holds the
  question number, the difficulty tag, the question, the 3-2-1 ring, the TRUE / FALSE stamp and then the "why" line;
- "Bit", a small original robot mascot, sits on the card's top-left corner and reacts: waves in the hook, thinks while
  each question is asked, sweats through the lock-in, cheers on TRUE, wags "nope" on FALSE, gasps and facepalms at
  Apoorva's flip, puts on a crown for the boss level and points at the comment box;
- more energy: confetti on TRUE, a red edge flash on FALSE, a green edge flash on TRUE, card bounce and shake;
- game-show sounds (CC0 OpenGameArt: Kenney interface sounds, menu / level-up pack, firework pop, completion ding).
python3 build/generate.py
"""
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "plan", "events.json")))
DUR = E["dur"]
P = {p["label"]: p for p in E["pieces"]}
INK, GREEN, RED, GOLD = "#0E0F12", "#16A34A", "#E11D48", "#F5B400"
JS, SFX, HTML = [], [], []
random.seed(5)


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


def wt(label, word, n=0):
    hits = [w for w in P[label]["words"] if w["w"].lower().strip(".,?!").startswith(word.lower())]
    return hits[min(n, len(hits) - 1)]["t0"]


QS = [
    (1, "WARM-UP", "#22C55E", "Does NVIDIA manufacture chips?", "q1", "lock1", "a1", "False", "F", "NVIDIA designs the chips. TSMC makes them."),
    (2, "EASY", "#84CC16", "It's AI, so it gives the same answer every time.", "q2", "lock2", "a2b", "True", "T", "Same prompt, different answers: AI samples."),
    (3, "MEDIUM", "#F59E0B", "A model on its own can't tell you today's news.", "q3", "lock3", "a3", "True", "T", "Live news needs search or tools."),
    (4, "MEDIUM", "#F59E0B", "Longer prompt, better answer.", "q4", "lock4", "a4", "False", "F", "Clear beats long."),
    (5, "HARD", "#F97316", "Ask AI to double-check itself and it catches every mistake.", "q5", "lock5", "a5", "False", "F", "AI can miss its own mistakes."),
    (6, "BOSS LEVEL", "#A855F7", "A model that's 99% accurate can still be useless.", "q6", "lock6", None, None, "?", None),
]

# ==== the mascot "Bit" (original, drawn here) =================================================================================
EYES = {
    "norm": '<ellipse cx="80" cy="102" rx="9" ry="12" fill="#6EF0FF"/><ellipse cx="120" cy="102" rx="9" ry="12" fill="#6EF0FF"/>',
    "up": '<ellipse cx="82" cy="94" rx="8" ry="11" fill="#6EF0FF"/><ellipse cx="122" cy="94" rx="8" ry="11" fill="#6EF0FF"/>',
    "happy": '<path d="M70 106 Q80 90 90 106 M110 106 Q120 90 130 106" fill="none" stroke="#6EF0FF" stroke-width="7" stroke-linecap="round"/>',
    "wide": '<circle cx="80" cy="101" r="14" fill="#6EF0FF"/><circle cx="120" cy="101" r="14" fill="#6EF0FF"/><circle cx="80" cy="101" r="5" fill="#1E2433"/><circle cx="120" cy="101" r="5" fill="#1E2433"/>',
    "squint": '<path d="M70 102 L90 98 M110 98 L130 102" fill="none" stroke="#6EF0FF" stroke-width="7" stroke-linecap="round"/>',
    "shut": '<path d="M70 102 Q80 108 90 102 M110 102 Q120 108 130 102" fill="none" stroke="#6EF0FF" stroke-width="6" stroke-linecap="round"/>',
}
MOUTHS = {
    "smile": '<path d="M88 120 Q100 128 112 120" fill="none" stroke="#6EF0FF" stroke-width="5" stroke-linecap="round"/>',
    "grin": '<path d="M84 117 Q100 134 116 117 Z" fill="#6EF0FF"/>',
    "o": '<ellipse cx="100" cy="122" rx="7" ry="8" fill="#6EF0FF"/>',
    "flat": '<path d="M90 122 L110 122" stroke="#6EF0FF" stroke-width="5" stroke-linecap="round"/>',
    "wavy": '<path d="M86 122 Q92 116 98 122 T110 122 T116 120" fill="none" stroke="#6EF0FF" stroke-width="4" stroke-linecap="round"/>',
}
BIT = ('<div id="bit"><div id="bitb"><svg viewBox="0 0 200 240" overflow="visible">'
       '<ellipse cx="100" cy="232" rx="54" ry="8" fill="rgba(0,0,0,.25)"/>'
       '<rect x="74" y="200" width="18" height="30" rx="9" fill="#C9D3E3" stroke="#1E2433" stroke-width="4"/>'
       '<rect x="108" y="200" width="18" height="30" rx="9" fill="#C9D3E3" stroke="#1E2433" stroke-width="4"/>'
       '<g id="bitaL"><rect x="34" y="150" width="22" height="56" rx="11" fill="#C9D3E3" stroke="#1E2433" stroke-width="4"/></g>'
       '<g id="bitaR"><rect x="144" y="150" width="22" height="56" rx="11" fill="#C9D3E3" stroke="#1E2433" stroke-width="4"/></g>'
       '<rect x="58" y="140" width="84" height="70" rx="24" fill="#EEF2F8" stroke="#1E2433" stroke-width="4"/>'
       '<circle cx="100" cy="174" r="10" fill="#A855F7"/>'
       '<g id="bith"><line x1="100" y1="52" x2="100" y2="22" stroke="#1E2433" stroke-width="5"/>'
       '<circle id="bitbulb" cx="100" cy="17" r="10" fill="#FACC15" stroke="#1E2433" stroke-width="4"/>'
       '<rect x="28" y="50" width="144" height="100" rx="40" fill="#FFFFFF" stroke="#1E2433" stroke-width="4"/>'
       '<rect x="46" y="68" width="108" height="66" rx="26" fill="#1E2433"/>'
       '<circle cx="40" cy="112" r="7" fill="#FF8FB1"/><circle cx="160" cy="112" r="7" fill="#FF8FB1"/>'
       + "".join(f'<g class="be" id="be_{k}" opacity="{1 if k == "norm" else 0}">{v}</g>' for k, v in EYES.items())
       + "".join(f'<g class="bm" id="bm_{k}" opacity="{1 if k == "smile" else 0}">{v}</g>' for k, v in MOUTHS.items())
       + '<g id="bitlid" opacity="0"><rect x="66" y="88" width="68" height="28" fill="#1E2433"/>' + EYES["shut"] + '</g>'
       '<g id="bitcrown" opacity="0"><path d="M58 52 L66 18 L84 40 L100 10 L116 40 L134 18 L142 52 Z" fill="#FACC15" stroke="#1E2433" stroke-width="4" stroke-linejoin="round"/>'
       '<circle cx="100" cy="36" r="5" fill="#E11D48"/></g>'
       '<path id="bitsweat" opacity="0" d="M170 70 C164 82 160 90 160 96 A10 10 0 0 0 180 96 C180 90 176 82 170 70 Z" fill="#7FD3FF" stroke="#2B8FD6" stroke-width="3"/>'
       '</g></svg></div><div id="bitbub"><span id="bitbt">?</span></div></div>')


def face(t, eyes, mouth):
    st(".be", t, "{opacity: 0}")
    st(f"#be_{eyes}", t, "{opacity: 1}")
    st(".bm", t, "{opacity: 0}")
    st(f"#bm_{mouth}", t, "{opacity: 1}")


def arms(t, l, r, d=.25, ease="back.out(2)"):
    js(f'tl.to("#bitaL", {{rotation: {l}, svgOrigin: "45 154", duration: {d}, ease: "{ease}"}}, {t:.3f});')
    js(f'tl.to("#bitaR", {{rotation: {r}, svgOrigin: "155 154", duration: {d}, ease: "{ease}"}}, {t:.3f});')


def hop(t, h=46, n=1):
    for k in range(n):
        tk = t + .34 * k
        js(f'tl.fromTo("#bitb", {{y: 0, scaleY: 1, scaleX: 1}}, {{keyframes: [{{scaleY: .86, scaleX: 1.1, y: 6, duration: .06}}, '
           f'{{scaleY: 1.08, scaleX: .94, y: {-h}, duration: .13, ease: "power2.out"}}, {{scaleY: 1, scaleX: 1, y: 0, duration: .12, ease: "power2.in"}}, '
           f'{{scaleY: .92, scaleX: 1.06, duration: .03}}, {{scaleY: 1, scaleX: 1, duration: .05}}], immediateRender: false}}, {tk:.3f});')
    sfx("boing", t)


def bubble(t, text, d=.9):
    st("#bitbt", t - .01, f'{{textContent: "{text}"}}')
    ft("#bitbub", t, .3, "{opacity: 0, scale: .2, rotation: -30}", "{opacity: 1, scale: 1, rotation: 0}", "back.out(2.6)")
    to("#bitbub", t + d, .18, "{opacity: 0, scale: .6}", "power2.in")


def sweat(t, d=.9):
    ft("#bitsweat", t, .2, "{opacity: 0, y: -10}", "{opacity: 1, y: 0}", "back.out(2)")
    to("#bitsweat", t + .2, d - .2, "{y: 26}", "power1.in")
    st("#bitsweat", t + d, "{opacity: 0}")


def head_tilt(t, a, d=.25):
    js(f'tl.to("#bith", {{rotation: {a}, svgOrigin: "100 150", duration: {d}, ease: "back.out(2)"}}, {t:.3f});')


def blink(t):
    st("#bitlid", t, "{opacity: 1}")
    st("#bitlid", t + .1, "{opacity: 0}")


# ==== layout =====================================================================================================================
boxes = "".join(f'<div class="bx{" boss" if n == 6 else ""}" id="bx{n}"><span class="bn">{n}</span><i class="bf" id="bf{n}"></i><b class="bt" id="bt{n}"></b></div>' for n in range(1, 7))
HTML.append(f'<div id="trk">{boxes}</div>')
for n, tag, col, q, ql, ll, al, aw, tf, why in QS:
    HTML.append(f'<div class="qc{" bossc" if n == 6 else ""}" id="qc{n}"><div class="qh"><span class="qn">Q{n}</span><span class="qtag" style="--c:{col}"><i></i>{tag}</span>'
                f'<span class="lkt" id="lkt{n}">LOCK IN</span></div><div class="qt" id="qt{n}">' + " ".join(f'<span class="qw">{w}</span>' for w in q.split()) + "</div>"
                + (f'<div class="why" id="why{n}">{why}</div>' if why else "")
                + (f'<div class="stamp {"st" if tf == "T" else "sf"}" id="sp{n}">{"TRUE" if tf == "T" else "FALSE"}</div>' if tf in "TF" else "")
                + "</div>")
HTML.append('<div class="stamp sf" id="sp2f">FALSE</div><div id="plot">WAIT...</div>')
HTML.append('<div id="lk"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" class="rt"/><circle cx="60" cy="60" r="52" class="rf" id="rf" pathLength="1000"/></svg>'
            '<b class="ln" id="ln3">3</b><b class="ln" id="ln2">2</b><b class="ln" id="ln1">1</b></div>')
HTML.append('<div class="qc hookc" id="hk"><div class="qh"><span class="qn">6 QUESTIONS</span><span class="qtag" style="--c:#A855F7"><i></i>Q6 = BOSS LEVEL</span></div>'
            '<div class="qt hkt"><span class="qw">Apoorva,</span> <span class="qw">quick:</span> <span class="qw tt">TRUE</span> <span class="qw">or</span> <span class="qw ff">FALSE?</span></div>'
            '<div class="hk3">Score yourself as you go.</div></div>')
HTML.append('<div class="qc ctac" id="cta"><div class="qh"><span class="qtag" style="--c:#A855F7"><i></i>BOSS LEVEL</span></div>'
            '<div class="qt">TRUE <em>or</em> FALSE? Comment below.</div>'
            '<div class="cbar"><i></i><span id="cph">Add a comment…</span><span id="cty">' + "".join(f"<i>{c}</i>" for c in "TRUE or FALSE") + '</span></div></div>')
CONF = "".join(f'<i class="cf" style="background:{random.choice(["#22C55E", "#FACC15", "#38BDF8", "#F472B6", "#A855F7", "#FFFFFF"])};'
               f'width:{random.randint(10, 18)}px;height:{random.randint(14, 26)}px;border-radius:{random.choice(["3px", "50%"])}"></i>' for _ in range(28))
HTML.append(f'<div id="conf">{CONF}</div><div id="edge"></div>')
HTML.append(BIT)

# ---- hook ---------------------------------------------------------------------------------------------------------------------
ft("#trk", .05, .45, "{opacity: 0, y: -80}", "{opacity: 1, y: 0}", "back.out(1.6)")
ft(".bx", .15, .3, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1, stagger: .05}", "back.out(2.6)")
ft("#hk", 0, .4, "{opacity: 0, y: 120}", "{opacity: 1, y: 0}", "back.out(1.6)")
hw = P["hook"]["words"]
for k in range(5):
    tw = hw[min(k, len(hw) - 1)]["t0"]
    ft(f"#hk .qw:nth-child({k + 1})", tw - .05, .22, "{opacity: 0, y: 16}", "{opacity: 1, y: 0}", "power3.out")
ft("#hk .hk3", 1.2, .3, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}", "power3.out")
sfx("g_swish", 0)
for k in range(6):
    sfx("g_tick", .15 + .05 * k)
to("#hk", P["q1"]["t0"] - .12, .2, "{opacity: 0, y: 40}", "power2.in")
# Bit pops onto the card and waves
ft("#bit", .35, .4, "{opacity: 0, y: 120, scale: .4}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.2)")
sfx("g_pickup", .4)
face(.35, "happy", "grin")
arms(.6, 0, -150, .25)
js('tl.fromTo("#bitaR", {rotation: -150}, {rotation: -120, svgOrigin: "155 154", duration: .14, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}, .85);')
arms(1.75, 0, 0, .2)
js(f'tl.fromTo("#bitb", {{y: 0}}, {{y: -5, duration: .7, yoyo: true, repeat: {int(DUR / .7)}, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#bitbulb", {{fill: "#FACC15"}}, {{fill: "#FFF5B0", duration: .5, yoyo: true, repeat: {int(DUR / .5)}, ease: "sine.inOut", immediateRender: false}}, 0);')

# ---- questions ------------------------------------------------------------------------------------------------------------------
for i, (n, tag, col, q, ql, ll, al, aw, tf, why) in enumerate(QS):
    t_q, t_lk, t_rv = P[ql]["t0"], P[ll]["t0"], P[ll]["t1"]
    LK = t_rv - t_lk
    st(f"#bx{n}", t_q, "{borderColor: '#FFFFFF', boxShadow: '0 0 0 4px rgba(255,255,255,.4), 0 0 24px rgba(255,255,255,.5)'}")
    ft(f"#qc{n}", t_q, .38, "{opacity: 0, y: 120, rotation: -2}", "{opacity: 1, y: 0, rotation: 0}", "back.out(1.6)")
    sfx("g_question" if n != 6 else "g_levelup", t_q)
    qws = P[ql]["words"]
    for k in range(len(q.split())):
        tw = qws[min(k, len(qws) - 1)]["t0"] if qws else t_q + .1 * k
        ft(f"#qc{n} .qw:nth-child({k + 1})", tw - .04, .2, "{opacity: 0, y: 14}", "{opacity: 1, y: 0}", "power3.out")
    # Bit thinks
    face(t_q + .1, "up", "flat")
    arms(t_q + .1, 0, -120, .25)
    head_tilt(t_q + .1, -8)
    bubble(t_q + .25, "?", .8)
    if n == 6:
        ft("#qc6", t_q + .1, .3, "{boxShadow: '0 0 0 0 rgba(168,85,247,0)'}", "{boxShadow: '0 0 0 8px rgba(168,85,247,.55)'}", "power2.out")
        st("#bitcrown", t_q + .3, "{opacity: 1}")
        ft("#bitcrown", t_q + .3, .35, "{y: -120}", "{y: 0}", "bounce.out")
        face(t_q + .3, "squint", "grin")
        sfx("g_drop", t_q + .55)
    # lock-in: ring inside the card's right side, push-in on her stare, Bit sweats
    ft("#lk", t_lk, .2, "{opacity: 0, scale: .5}", "{opacity: 1, scale: 1}", "back.out(2.5)")
    ft(f"#lkt{n}", t_lk, .2, "{opacity: 0}", "{opacity: 1}", "power2.out")
    ft("#rf", t_lk, LK, "{strokeDashoffset: 0}", "{strokeDashoffset: 1000}", "none")
    for k, num in enumerate((3, 2, 1)):
        tk = t_lk + LK / 3 * k
        st(".ln", tk, "{opacity: 0}")
        ft(f"#ln{num}", tk, .16, "{opacity: 0, scale: 1.8}", "{opacity: 1, scale: 1}", "back.out(3)")
        sfx("g_tick", tk)
    st(".ln", t_rv, "{opacity: 0}")
    ft("#cam", t_lk, LK, "{scale: 1}", "{scale: 1.09}", "sine.inOut")
    ft("#vig", t_lk, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
    to("#lk", t_rv - .02, .14, "{opacity: 0, scale: .5}", "power2.in")
    to(f"#lkt{n}", t_rv - .02, .12, "{opacity: 0}")
    to("#vig", t_rv, .3, "{opacity: 0}")
    to("#cam", t_rv, .35, "{scale: 1}", "power3.out")
    face(t_lk, "wide", "wavy")
    arms(t_lk, 20, -20, .2)
    head_tilt(t_lk, 0, .15)
    sweat(t_lk + .1, LK - .1)
    js(f'tl.fromTo("#bitb", {{x: 0}}, {{x: 3, duration: .05, yoyo: true, repeat: {int(LK / .05) - 1}, ease: "none", immediateRender: false}}, {t_lk:.3f});')
    if n == 6:
        continue
    # reveal
    t_a = wt(al, aw) - .03
    ft(f"#sp{n}", t_a, .2, "{opacity: 0, scale: 2.4, rotation: -20}", "{opacity: 1, scale: 1, rotation: -8}", "power4.in")
    st(f"#bt{n}", t_a + .1, f'{{textContent: "{tf}"}}')
    st(f"#bf{n}", t_a + .1, f"{{background: '{GREEN if tf == 'T' else RED}'}}")
    ft(f"#bf{n}", t_a + .1, .28, "{scaleY: 0}", "{scaleY: 1}", "back.out(2)")
    st(f"#bx{n}", t_a + .1, f"{{borderColor: '{GREEN if tf == 'T' else RED}', boxShadow: 'none'}}")
    ft(f"#bt{n}", t_a + .14, .28, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}", "back.out(3)")
    ft(f"#bx{n}", t_a + .1, .3, "{scale: 1.35}", "{scale: 1}", "back.out(3)")
    ft("#punch", t_a + .18, .07, "{scale: 1}", "{scale: 1.035}", "power2.out")
    to("#punch", t_a + .25, .3, "{scale: 1}", "power3.out")
    st("#edge", t_a + .15, f"{{opacity: 1, boxShadow: 'inset 0 0 140px 30px {GREEN if tf == 'T' else RED}'}}")
    to("#edge", t_a + .15 + .02, .5, "{opacity: 0}", "power2.out")
    sfx("stamp", t_a + .18)
    sfx("g_correct" if tf == "T" else "g_wrong", t_a + .22)
    if tf == "T":
        for k in range(28):
            ang, dist = random.uniform(-160, -20), random.uniform(160, 420)
            import math
            dx, dy = math.cos(math.radians(ang)) * dist, math.sin(math.radians(ang)) * dist
            js(f'tl.fromTo("#conf .cf:nth-child({k + 1})", {{opacity: 1, x: 0, y: 0, rotation: 0}}, {{keyframes: [{{x: {dx:.0f}, y: {dy:.0f}, rotation: {random.randint(-360, 360)}, duration: .45, ease: "power3.out"}}, '
               f'{{y: {dy + 260:.0f}, opacity: 0, duration: .7, ease: "power1.in"}}], immediateRender: false}}, {t_a + .15:.3f});')
        sfx("g_pop", t_a + .15)
        face(t_a + .1, "happy", "grin")
        arms(t_a + .1, 150, -150, .2)
        hop(t_a + .12, 50, 2)
        arms(t_a + .9, 0, 0, .2)
    else:
        face(t_a + .1, "squint", "smile")
        arms(t_a + .1, 0, -100, .2)
        js(f'tl.fromTo("#bitaR", {{rotation: -100}}, {{rotation: -70, svgOrigin: "155 154", duration: .12, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_a + .32:.3f});')
        js(f'tl.fromTo("#bith", {{rotation: 0}}, {{rotation: 8, svgOrigin: "100 150", duration: .12, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}}, {t_a + .32:.3f});')
        bubble(t_a + .3, "NOPE", .7)
        arms(t_a + .9, 0, 0, .2)
    if n == 2:
        continue
    t_w = t_a + .5
    to(f"#qt{n}", t_w, .2, "{opacity: 0, y: -10}", "power2.in")
    to(f"#sp{n}", t_w, .2, "{opacity: 0, scale: .7}", "power2.in")
    ft(f"#why{n}", t_w + .1, .3, "{opacity: 0, y: 14}", "{opacity: 1, y: 0}", "back.out(2)")
    sfx("g_pickup", t_w + .1)
    face(t_w + .4, "norm", "smile")
    blink(t_w + .8)

# ---- Q2: Apoorva's flip ---------------------------------------------------------------------------------------------------------
t_sorry = wt("a2c", "Sorry") - .05
js(f'tl.fromTo("#bx2", {{x: 0}}, {{keyframes: [{{x: -9, duration: .04}}, {{x: 8, duration: .04}}, {{x: -5, duration: .04}}, {{x: 0, duration: .04}}], immediateRender: false}}, {t_sorry:.3f});')
js(f'tl.fromTo("#qc2", {{x: 0, filter: "none"}}, {{keyframes: [{{x: -12, filter: "drop-shadow(6px 0 0 rgba(225,29,72,.8)) drop-shadow(-6px 0 0 rgba(0,180,255,.8))", duration: .05}}, {{x: 9, duration: .05}}, {{x: 0, filter: "none", duration: .06}}], immediateRender: false}}, {t_sorry:.3f});')
to("#sp2", t_sorry + .05, .15, "{opacity: 0, scale: .6}", "power2.in")
ft("#plot", t_sorry, .22, "{opacity: 0, scale: .5, rotation: -10}", "{opacity: 1, scale: 1, rotation: 6}", "back.out(3)")
face(t_sorry, "wide", "o")
arms(t_sorry, -40, 40, .15)
hop(t_sorry, 30)
bubble(t_sorry + .05, "!?", .6)
t_f2 = wt("a2c", "false") - .03
ft("#sp2f", t_f2, .2, "{opacity: 0, scale: 2.4, rotation: 20}", "{opacity: 1, scale: 1, rotation: -8}", "power4.in")
js(f'tl.to("#bx2", {{rotationY: 180, duration: .26, ease: "power2.inOut"}}, {t_f2:.3f});')
st("#bt2", t_f2 + .13, '{textContent: "F", rotationY: 180}')
st("#bf2", t_f2 + .13, f"{{background: '{RED}'}}")
st("#bx2", t_f2 + .13, f"{{borderColor: '{RED}'}}")
st("#edge", t_f2 + .1, f"{{opacity: 1, boxShadow: 'inset 0 0 140px 30px {RED}'}}")
to("#edge", t_f2 + .1 + .02, .5, "{opacity: 0}", "power2.out")
to("#plot", t_f2 + .4, .2, "{opacity: 0}")
face(t_f2 + .1, "shut", "flat")
arms(t_f2 + .1, 0, -165, .2)                      # facepalm
sfx("g_wrong", t_f2 + .22)
sfx("stamp", t_f2 + .18)
to("#qt2", t_f2 + .55, .2, "{opacity: 0, y: -10}", "power2.in")
to("#sp2f", t_f2 + .55, .2, "{opacity: 0, scale: .7}", "power2.in")
ft("#why2", t_f2 + .65, .3, "{opacity: 0, y: 14}", "{opacity: 1, y: 0}", "back.out(2)")
sfx("g_pickup", t_f2 + .65)
arms(t_f2 + 1.0, 0, 0, .2)
face(t_f2 + 1.0, "norm", "smile")

# ---- card exits ---------------------------------------------------------------------------------------------------------------
for i, (n, *_r) in enumerate(QS[:-1]):
    t_next = P[QS[i + 1][4]]["t0"]
    to(f"#qc{n}", t_next - .12, .18, "{opacity: 0, y: 60, scale: .95}", "power2.in")
    if n == 2:
        to("#sp2f", t_next - .12, .18, "{opacity: 0}")

# ---- boss level poll + CTA ---------------------------------------------------------------------------------------------------
t_cta = P["cta"]["t0"]
st("#bt6", t_cta - .1, '{textContent: "?"}')
ft("#bt6", t_cta - .1, .3, "{opacity: 0, scale: .3}", "{opacity: 1, scale: 1}", "back.out(3)")
js(f'tl.fromTo("#bx6", {{scale: 1}}, {{scale: 1.14, duration: .3, yoyo: true, repeat: {int((DUR - t_cta) / .3)}, ease: "sine.inOut", immediateRender: false}}, {t_cta:.3f});')
to("#qc6", t_cta - .05, .2, "{opacity: 0, y: 60}", "power2.in")
ft("#cta", t_cta, .4, "{opacity: 0, y: 120}", "{opacity: 1, y: 0}", "back.out(1.6)")
t_ty = wt("cta", "comment") - .1
st("#cph", t_ty, "{opacity: 0}")
js(f'tl.fromTo("#cty i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .05, immediateRender: false}}, {t_ty:.3f});')
sfx("g_levelup", t_cta)
sfx("typing", t_ty)
sfx("g_complete", t_ty + .8)
face(t_cta, "happy", "grin")
arms(t_cta + .1, 0, -95, .25)                     # points along the comment bar
js(f'tl.fromTo("#bitaR", {{rotation: -95}}, {{rotation: -80, svgOrigin: "155 154", duration: .25, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false}}, {t_cta + .4:.3f});')
hop(t_ty + .8, 40, 2)
for tb in (2.6, 7.8, 15.6, 20.9, 26.9, 33.5):
    blink(tb)

CSS = f"""
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: Mono; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: {INK}; background: #000; }}
#punch, #cam {{ position: absolute; inset: 0; transform-origin: 50% 32%; }}
#ar {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
#vig {{ position: absolute; inset: 0; opacity: 0; pointer-events: none; background: radial-gradient(70% 55% at 50% 34%, rgba(0,0,0,0) 45%, rgba(0,0,0,.6) 100%); }}
#shade {{ position: absolute; left: 0; right: 0; top: 0; height: 300px; background: linear-gradient(180deg, rgba(0,0,0,.4), rgba(0,0,0,0)); }}
#shadeb {{ position: absolute; left: 0; right: 0; bottom: 0; height: 640px; background: linear-gradient(0deg, rgba(0,0,0,.55), rgba(0,0,0,0)); }}
#edge {{ position: absolute; inset: 0; opacity: 0; pointer-events: none; z-index: 40; }}
/* slim tracker at the very top */
#trk {{ position: absolute; left: 0; right: 0; top: 150px; display: flex; gap: 12px; justify-content: center; perspective: 600px; opacity: 0; z-index: 20; }}
.bx {{ position: relative; width: 84px; height: 84px; border-radius: 20px; border: 4px solid rgba(255,255,255,.8); background: rgba(14,15,18,.4);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); overflow: hidden; opacity: 0; }}
.bx.boss {{ border-color: {GOLD}; }}
.bn {{ position: absolute; left: 7px; top: 3px; font: 15px Mono; color: rgba(255,255,255,.8); z-index: 3; }}
.bf {{ position: absolute; inset: 0; transform-origin: 50% 100%; transform: scaleY(0); }}
.bt {{ position: absolute; inset: 0; display: grid; place-items: center; font-weight: 800; font-size: 52px; color: #fff; z-index: 2; opacity: 0; }}
#bt6 {{ color: {GOLD}; }}
/* the compact bottom card */
.qc {{ position: absolute; left: 60px; right: 60px; top: 1420px; min-height: 196px; padding: 22px 30px 26px; border-radius: 30px; background: #fff; opacity: 0; z-index: 15;
  box-shadow: 0 24px 60px rgba(0,0,0,.4); }}
.qc.bossc {{ background: linear-gradient(135deg, #1B1030, #2A1450); color: #fff; border: 4px solid #A855F7; }}
.qh {{ display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }}
.qn {{ font: 22px Mono; letter-spacing: .14em; color: #6B7280; }}
.bossc .qn {{ color: #D8B4FE; }}
.qtag {{ display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 999px; background: {INK}; color: #fff; font-weight: 800; font-size: 22px; letter-spacing: .06em; }}
.qtag i {{ width: 12px; height: 12px; border-radius: 50%; background: var(--c); box-shadow: 0 0 10px var(--c); }}
.bossc .qtag {{ background: #A855F7; }}
.lkt {{ margin-left: auto; margin-right: 120px; font: 20px Mono; letter-spacing: .16em; color: {RED}; opacity: 0; }}
.qt {{ font-weight: 800; font-size: 46px; line-height: 1.1; letter-spacing: -.025em; padding-right: 210px; }}
.qw {{ display: inline-block; opacity: 0; }}
.why {{ position: absolute; left: 30px; right: 30px; top: 70px; font-weight: 800; font-size: 40px; line-height: 1.12; letter-spacing: -.02em; opacity: 0; }}
.why::before {{ content: "WHY: "; color: #A855F7; }}
.stamp {{ position: absolute; right: 22px; top: 50%; margin-top: -38px; padding: 6px 16px; border-radius: 14px; font-weight: 800; font-size: 48px; opacity: 0; background: #fff; z-index: 3; }}
.stamp.st {{ color: {GREEN}; border: 6px solid {GREEN}; }}
.stamp.sf {{ color: {RED}; border: 6px solid {RED}; }}
#sp2f {{ position: absolute; right: 82px; top: 1480px; margin-top: 0; z-index: 30; }}
#plot {{ position: absolute; right: 80px; top: 1360px; padding: 8px 18px; border-radius: 12px; background: {GOLD}; color: {INK}; font-weight: 800; font-size: 34px; opacity: 0; z-index: 31; }}
#lk {{ position: absolute; right: 82px; top: 1462px; width: 112px; height: 112px; opacity: 0; z-index: 25; }}
#lk svg {{ position: absolute; inset: 0; width: 100%; height: 100%; transform: rotate(-90deg); }}
#lk .rt {{ fill: {INK}; stroke: rgba(0,0,0,.15); stroke-width: 9; }}
#lk .rf {{ fill: none; stroke: {GOLD}; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 1000; }}
.ln {{ position: absolute; inset: 0; display: grid; place-items: center; font-weight: 800; font-size: 60px; color: #fff; opacity: 0; }}
/* hook + CTA cards */
.hookc .hkt {{ font-size: 52px; padding-right: 0; }}
.hookc .tt {{ color: {GREEN}; }} .hookc .ff {{ color: {RED}; }}
.hk3 {{ margin-top: 8px; font-weight: 700; font-size: 28px; color: #6B7280; opacity: 0; }}
.ctac {{ background: linear-gradient(135deg, #1B1030, #2A1450); color: #fff; border: 4px solid #A855F7; }}
.ctac .qt {{ font-size: 48px; padding-right: 0; }}
.ctac .qt em {{ font-style: normal; color: {GOLD}; }}
.cbar {{ display: flex; align-items: center; gap: 14px; height: 76px; margin-top: 14px; padding: 0 20px; border-radius: 40px; background: #fff; color: {INK}; font-weight: 800; font-size: 32px; }}
.cbar > i {{ width: 46px; height: 46px; border-radius: 50%; background: linear-gradient(135deg, {GREEN}, {RED}); flex: none; }}
#cph {{ position: absolute; margin-left: 60px; font-weight: 600; color: #9CA3AF; }}
#cty i {{ font-style: normal; opacity: 0; }}
/* confetti from the card */
#conf {{ position: absolute; left: 540px; top: 1440px; width: 0; height: 0; z-index: 35; }}
.cf {{ position: absolute; opacity: 0; }}
/* Bit */
#bit {{ position: absolute; left: 56px; top: 1196px; width: 196px; height: 235px; z-index: 32; opacity: 0; }}
#bitb {{ position: absolute; inset: 0; transform-origin: 50% 100%; }}
#bitb svg {{ width: 100%; height: 100%; overflow: visible; }}
#bitbub {{ position: absolute; left: 160px; top: -40px; min-width: 70px; height: 62px; padding: 0 14px; border-radius: 31px 31px 31px 8px; background: #fff; display: grid; place-items: center;
  font-weight: 800; font-size: 32px; color: #A855F7; opacity: 0; transform-origin: 0 100%; box-shadow: 0 8px 24px rgba(0,0,0,.3); white-space: nowrap; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Apoorva: AI true or false v2 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="punch"><div id="cam">
        <video id="ar" src="assets/video/aroll.mp4" data-start="0" data-duration="{DUR:.3f}" data-track-index="1" muted playsinline></video>
      </div></div>
      <div id="vig"></div><div id="shade"></div><div id="shadeb"></div>
      {chr(10).join(HTML)}
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
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
