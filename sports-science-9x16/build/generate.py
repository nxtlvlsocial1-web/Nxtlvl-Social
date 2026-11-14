"""Sports Science Technology: "Performance Has No Fixed Body Type" 9:16 explainer (1080x1920, 30 fps, 60 s).

Client brief (PDF, 10 pages): IG / FB Reels, 55-60 s, English VO + English subtitles (max 2 lines, inside safe zones),
premium sports-documentary look: deep navy, matte black, white type, restrained royal-blue accents, Montserrat / Inter.
Six scenes, on-screen text exactly as the brief gives it; the VO is the brief's master script, verbatim.
Guardrails: no ranking of body types (the three figures are the same size, colour and pose and carry a "broad
descriptive categories" note), no invented scores or data (the assessment HUD only names what is being assessed),
the official logo is placed in post (an empty logo slot on the end card; set LOGO=path/to/logo.png to drop it in).
Footage: Pexels (graded vertical proxies, build/prep_footage.py); body figures: build/bodies.py.
Clock: the VO (build/vo_assemble.py -> plan/words.json, plan/lines.json).
python3 build/generate.py  ->  index.html, plan/edit.json, plan/sfx_events.json
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
DUR = 60.0
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
LINES = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "plan", "lines.json")))}
NAVY, INK, BLUE, BLUE_L, MIST = "#0A1632", "#06080E", "#2F5BFF", "#7E9BFF", "#C9D4F2"
LOGO = os.environ.get("LOGO", "assets/img/sst_logo.jpg")   # the client's official logo (owner-supplied), placed unmodified on a white card            # the client's official logo file, when we have it (never recreated)
PREVIEW = os.environ.get("PREVIEW", "1") == "1"
A, SFX, SHOTS, OVER, CAPS = [], [], [], [], []


def js(s):
    A.append("      " + s)


def sfx(kind, t, gain=0.0):
    SFX.append({"type": kind, "t": round(max(0.0, t), 3), "gain": gain})


def norm(w):
    return w.lower().strip(".,?!:'\"")


def T(word, after=0.0, key="s"):
    for w in WORDS:
        if w["s"] >= after - .05 and norm(w["w"]) == norm(word):
            return w[key]
    raise KeyError(word)


def L(i, key="s"):
    return LINES[f"s{i:02d}"][key]


# ---------------------------------------------------------------- shots
def shot(sid, t0, t1, vid, at=0.0, pos="50% 50%", push=(1.03, 1.1), box=None, z=1, shade=True, extra=""):
    """a graded vertical clip, visible t0..t1, slow push-in. box=(top, height) for a split panel"""
    style = f"top:{box[0]}px;height:{box[1]}px;" if box else ""
    sh = '<i class="shade"></i>' if shade else ""
    SHOTS.append(f'<div class="shot" id="{sid}" style="{style}z-index:{z}"><video id="{sid}v" src="assets/video/{vid}.mp4" '
                 f'data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-media-start="{at:.3f}" data-track-index="{len(SHOTS) % 4}" '
                 f'muted playsinline style="object-position:{pos}"></video>{sh}{extra}</div>')
    js(f'tl.set("#{sid}", {{opacity: 1}}, {t0:.3f}); tl.set("#{sid}", {{opacity: 0}}, {t1:.3f});')
    js(f'tl.fromTo("#{sid}v", {{scale: {push[0]}}}, {{scale: {push[1]}, duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')


def headline(hid, lines, t0, t1, top, size=86, accent=(), cls="", stagger=.12):
    """a Montserrat headline; each line slides up out of its own mask. accent: indexes of lines in royal blue"""
    inner = "".join(f'<span class="ln"><span class="in{" ac" if i in accent else ""}">{t}</span></span>' for i, t in enumerate(lines))
    OVER.append(f'<div class="hl {cls}" id="{hid}" style="top:{top}px;font-size:{size}px">{inner}</div>')
    js(f'tl.set("#{hid}", {{opacity: 1}}, {t0:.3f});')
    js(f'tl.fromTo("#{hid} .in", {{yPercent: 112}}, {{yPercent: 0, duration: .55, ease: "expo.out", stagger: {stagger}, immediateRender: false}}, {t0:.3f});')
    if t1 is not None:
        js(f'tl.to("#{hid}", {{opacity: 0, duration: .22, ease: "power2.in"}}, {t1 - .22:.3f});')


def tag(tid, text, t0, t1, top, left=None, cls=""):
    pos = f"left:{left}px;" if left is not None else "left:0;right:0;text-align:center;"
    OVER.append(f'<div class="tag {cls}" id="{tid}" style="top:{top}px;{pos}"><b>{text}</b></div>')
    d = max(.12, min(.3, t1 - t0 - .16))
    js(f'tl.fromTo("#{tid}", {{opacity: 0, y: 26}}, {{opacity: 1, y: 0, duration: {d:.2f}, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
    js(f'tl.set("#{tid}", {{opacity: 0}}, {t1:.3f});')


# ---------------------------------------------------------------- scene 1: the question (0 - s02)
def scene1():
    t1 = L(2) - .05
    panels = [("8459966", 2.0, "50% 40%"), ("7187114", 4.2, "46% 40%"), ("15172075", .6, "52% 40%")]
    html = ""
    for i, (vid, at, pos) in enumerate(panels):
        html += (f'<div class="pane" id="pn{i}" style="left:{i * 360}px"><video id="pn{i}v" src="assets/video/{vid}.mp4" data-start="0" '
                 f'data-duration="{t1:.3f}" data-media-start="{at:.3f}" data-track-index="{i}" muted playsinline style="object-position:{pos}"></video></div>')
    SHOTS.append(f'<div class="shot" id="s1" style="opacity:1;z-index:1">{html}<i class="pdiv" style="left:359px"></i><i class="pdiv" style="left:719px"></i>'
                 f'<i class="shade dark"></i></div>')
    for i in range(3):
        js(f'tl.fromTo("#pn{i}", {{clipPath: "inset(0 0 {40 + i * 15}% 0)"}}, {{clipPath: "inset(0 0 0% 0)", duration: .6, ease: "expo.out"}}, {i * .1:.3f});')
        js(f'tl.fromTo("#pn{i}v", {{scale: 1.18}}, {{scale: 1.04, duration: {t1:.3f}, ease: "power2.out", immediateRender: false}}, 0);')
    js(f'tl.set("#s1", {{opacity: 0}}, {t1:.3f});')
    # the brief's opening text, over the three athletes; first line already in at frame 0
    # the hook is readable on frame 0 (no line reveal): it settles from a slight scale instead
    OVER.append('<div class="hl" id="h1" style="top:640px;font-size:92px;opacity:1"><span class="ln"><span class="in">DOES AN ATHLETE</span></span>'
                '<span class="ln"><span class="in">HAVE TO LOOK</span></span><span class="ln"><span class="in ac">A CERTAIN WAY?</span></span></div>')
    js('tl.fromTo("#h1", {scale: 1.08}, {scale: 1, duration: 1.2, ease: "expo.out"}, 0);')
    js(f'tl.to("#h1", {{opacity: 0, duration: .22, ease: "power2.in"}}, {t1 - .17:.3f});')
    sfx("whoosh_soft", 0.0, -6)


# ---------------------------------------------------------------- scene 2: body types (s02 - s04)
def scene2():
    t0, t_but, t1 = L(2) - .05, T("but") - .1, L(4) - .1
    figs = [("ecto", "ECTOMORPH", T("ectomorph,")), ("meso", "MESOMORPH", T("mesomorph")), ("endo", "ENDOMORPH", T("endomorph.") + .18)]
    cols = "".join(f'<div class="fig" id="f_{k}" style="left:{30 + i * 340}px"><img src="assets/img/body_{k}.svg">'
                   f'<b>{lab}</b></div>' for i, (k, lab, _) in enumerate(figs))
    OVER.append(f'<div class="board" id="bt"><i class="grid"></i><i class="sweep" id="sweep"></i>{cols}'
                f'<div class="note" id="btn">Broad descriptive categories, not rankings.</div></div>')
    js(f'tl.set("#bt", {{opacity: 1}}, {t0:.3f});')
    js(f'tl.fromTo("#sweep", {{x: -900}}, {{x: 1300, duration: 3.2, ease: "power1.inOut", immediateRender: false}}, {t0:.3f});')
    for k, lab, tw in figs:
        js(f'tl.fromTo("#f_{k}", {{opacity: 0, y: 70}}, {{opacity: 1, y: 0, duration: .6, ease: "expo.out", immediateRender: false}}, {tw - .12:.3f});')
        js(f'tl.fromTo("#f_{k} img", {{clipPath: "inset(0 0 100% 0)"}}, {{clipPath: "inset(0 0 0% 0)", duration: .8, ease: "power3.out", immediateRender: false}}, {tw - .12:.3f});')
        js(f'tl.fromTo("#f_{k} b", {{opacity: 0, y: 18}}, {{opacity: 1, y: 0, duration: .45, ease: "power3.out", immediateRender: false}}, {tw + .05:.3f});')
    js(f'tl.fromTo("#btn", {{opacity: 0}}, {{opacity: 1, duration: .4}}, {T("endomorph.") + .6:.3f});')
    # "Different shapes. Different physical characteristics."
    headline("h2a", ["DIFFERENT PHYSIQUES."], T("different", L(3) - .1), t_but + .05, 250, 78)
    js(f'tl.to(".fig", {{y: -14, duration: 1.4, ease: "sine.inOut", stagger: .15, yoyo: true, repeat: 1}}, {L(3):.3f});')
    js(f'tl.to("#bt", {{opacity: 0, duration: .3, ease: "power2.in"}}, {t_but - .05:.3f});')
    js(f'tl.set("#bt", {{opacity: 0}}, {t1:.3f});')
    # "But body shape alone does not determine sporting ability": cricketers of different builds at the crease
    shot("s2b", t_but, t1, "12460907", at=1.0, pos="50% 50%", push=(1.12, 1.2))
    headline("h2b", ["NO FIXED DEFINITION", "OF ATHLETIC POTENTIAL."], T("does", t_but) - .2, t1 + .02, 300, 70, accent=(1,))
    sfx("impact_soft", t0, -10)


# ---------------------------------------------------------------- scene 3: performance (s04 - s06)
def scene3():
    t0, t_its, t5, t1 = L(4) - .1, T("it's") - .1, L(5) - .1, L(6) - .1
    t_do = T("do.")
    shot("s3a", t0, T("how", t0) - .1, "8533122", at=12.6, pos="50% 50%")
    shot("s3b", T("how", t0) - .1, t_its, "15172075", at=3.2, pos="50% 45%")
    shot("s3c", t_its, t5, "6388432", at=2.5, pos="50% 50%", push=(1.06, 1.14))
    headline("h3a", ["PHYSIQUE IS ONE PART."], T("what", t0) - .1, t_its + .1, 280, 74)
    headline("h3b", ["PERFORMANCE", "IS THE FOCUS."], t_its, t5 + .05, 280, 90, accent=(0,))
    # the qualities, one hard cut each on the word
    q = [("strength,", "5837709", 6.0, "STRENGTH", "55% 50%"), ("speed,", "8533918", 3.0, "SPEED", "50% 50%"),
         ("endurance,", "4468823", 5.0, "ENDURANCE", "50% 40%"), ("agility,", "6077692", 3.0, "AGILITY", "50% 50%"),
         ("mobility", "8459966", 1.2, "MOBILITY", "50% 40%")]
    times = [T(w, t5) - .06 for w, *_ in q] + [T("and,", t5) - .02]
    for i, (w, vid, at, lab, pos) in enumerate(q):
        a, b = (t5 if i == 0 else times[i]), times[i + 1]
        shot(f"s3q{i}", a, b, vid, at=at, pos=pos, push=(1.1, 1.16))
        tag(f"tq{i}", lab, a + .02, b, 820, cls="big")
    t_game = T("game", t5) - .08
    shot("s3d", times[-1], t_game, "6237084", at=1.6, pos="50% 60%", push=(1.04, 1.1))
    shot("s3e", t_game, t1, "15172075", at=5.6, pos="50% 45%", push=(1.08, 1.0))
    headline("h3c", ["GAME OUTPUT"], t_game, t1 + .02, 820, 104, accent=(0,), cls="mid")
    js(f'tl.fromTo("#h3c .in", {{textShadow: "0 0 0px rgba(47,91,255,0)"}}, {{textShadow: "0 0 40px rgba(47,91,255,.85)", duration: .5, yoyo: true, repeat: 1, immediateRender: false}}, {t_game + .3:.3f});')
    sfx("tick", t5, -16)
    sfx("whoosh_soft", t_game, -10)


# ---------------------------------------------------------------- scene 4: bodybuilding vs sport (s06 - s08)
def scene4():
    t0, t_sp, t7, t1 = L(6) - .1, T("sports", L(6)) - .1, L(7) - .1, L(8) - .1
    top, bot = (0, 958), (962, 958)
    shot("s4top", t0, t7, "5319745", at=2.0, pos="50% 30%", push=(1.02, 1.08), box=top, z=2)
    sp = [("12460907", 5.0, "50% 50%"), ("6084027", 2.0, "50% 50%"), ("10340699", 6.0, "50% 35%"), ("8456204", 7.0, "50% 75%"), ("15172075", 7.4, "50% 40%")]
    span = (t7 - t0) / len(sp)
    for i, (vid, at, pos) in enumerate(sp):
        shot(f"s4b{i}", t0 + i * span, t0 + (i + 1) * span, vid, at=at, pos=pos, push=(1.04, 1.1), box=bot, z=2)
    OVER.append('<i class="seam" id="seam"></i>')
    js(f'tl.fromTo("#seam", {{opacity: 1, scaleX: 0}}, {{scaleX: 1, duration: .5, ease: "expo.out", immediateRender: false}}, {t0:.3f}); tl.set("#seam", {{opacity: 0}}, {t7:.3f});')
    OVER.append(f'<div class="duo" id="d_top" style="top:770px"><span>BODYBUILDING</span><b>PHYSIQUE</b></div>')
    OVER.append(f'<div class="duo" id="d_bot" style="top:1000px"><span>SPORTS</span><b>GAME PERFORMANCE</b></div>')
    for did, t in (("d_top", T("bodybuilding,") - .1), ("d_bot", t_sp)):
        js(f'tl.fromTo("#{did}", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: .45, ease: "expo.out", immediateRender: false}}, {t:.3f});')
        js(f'tl.to("#{did}", {{opacity: 0, duration: .2}}, {t7 - .2:.3f});')
    # "Every sport has different physical demands. Every athlete has different needs."
    t_ev2 = T("every", t7 + .5) - .1
    shot("s4c", t7, T("demands.") + .2, "10340699", at=3.0, pos="50% 40%", push=(1.1, 1.18))
    shot("s4d", T("demands.") + .2, t_ev2, "6084027", at=6.0, pos="45% 50%")
    shot("s4e", t_ev2, T("needs.") - .05, "16408434", at=.3, pos="50% 50%")
    shot("s4f", T("needs.") - .05, t1, "4745804", at=2.0, pos="50% 45%")
    headline("h4", ["DIFFERENT GOALS."], t7 + .05, t1 + .02, 270, 80)
    headline("h4b", ["DIFFERENT TRAINING", "REQUIREMENTS."], t_ev2, t1 + .02, 370, 80, accent=(1,))
    sfx("whoosh_soft", t0, -8)


# ---------------------------------------------------------------- scene 5: assessment (s08 - s10)
HUD_N = [0]


def hud(label, t0, t1, rx=540, ry=900):
    """corner brackets, a scan line, a pulsing REC dot, the test name and a tracking ring. No numbers: the brief forbids
    invented scores"""
    n = HUD_N[0]
    HUD_N[0] += 1
    OVER.append(f'<div class="hud" id="hd{n}"><i class="cb tl"></i><i class="cb tr"></i><i class="cb bl"></i><i class="cb br"></i>'
                f'<i class="scan" id="hds{n}"></i><div class="hlab"><i class="rec"></i>{label}</div>'
                f'<svg class="ring" id="hdr{n}" style="left:{rx - 150}px;top:{ry - 150}px" viewBox="0 0 300 300"><circle cx="150" cy="150" r="120"/>'
                f'<circle class="dash" cx="150" cy="150" r="138"/><path d="M150 18v26M150 256v26M18 150h26M256 150h26"/></svg></div>')
    js(f'tl.set("#hd{n}", {{opacity: 1}}, {t0:.3f}); tl.set("#hd{n}", {{opacity: 0}}, {t1:.3f});')
    js(f'tl.fromTo("#hd{n} .cb", {{scale: 1.6, opacity: 0}}, {{scale: 1, opacity: 1, duration: .4, ease: "expo.out", immediateRender: false}}, {t0:.3f});')
    js(f'tl.fromTo("#hds{n}", {{y: 260}}, {{y: 1560, duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    js(f'tl.fromTo("#hdr{n}", {{rotation: 0, scale: .6, opacity: 0}}, {{rotation: 90, scale: 1, opacity: 1, duration: {t1 - t0:.3f}, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
    js(f'tl.fromTo("#hd{n} .rec", {{opacity: 1}}, {{opacity: .2, duration: .4, yoyo: true, repeat: {int((t1 - t0) / .4)}, ease: "steps(1)", immediateRender: false}}, {t0:.3f});')


def scene5():
    t0, t9, t1 = L(8) - .1, L(9) - .1, L(10) - .1
    t_need = T("needs", t0) - .1
    shot("s5a", t0, t_need, "9431556", at=0.3, pos="50% 50%")
    shot("s5b", t_need, t9, "6078634", at=1.5, pos="50% 50%")
    t_sport, t_cont, t_ath = T("sport-specific") - .1, T("continuous") - .05, T("athletes", t9) - .1
    shot("s5c", t9, t_sport, "6388432", at=8.0, pos="50% 50%", push=(1.06, 1.12))
    hud("JUMP ASSESSMENT", t9, t_sport, 540, 980)
    shot("s5d", t_sport, t_cont, "9943211", at=4.0, pos="50% 60%", push=(1.06, 1.12))
    hud("MOBILITY &amp; AGILITY SCREEN", t_sport, t_cont, 540, 1150)
    shot("s5e", t_cont, t_ath, "4468823", at=9.0, pos="50% 40%", push=(1.04, 1.1))
    hud("CONDITIONING", t_cont, t_ath, 540, 820)
    shot("s5f", t_ath, T("physical", t_ath) - .1, "5837709", at=14.0, pos="55% 50%")
    shot("s5g", T("physical", t_ath) - .1, t1, "8456207", at=4.0, pos="50% 60%")
    headline("h5a", ["ASSESS."], T("assessments,") - .1, t1 + .02, 270, 96)
    headline("h5b", ["UNDERSTAND."], T("fitness") - .05, t1 + .02, 380, 96)
    headline("h5c", ["DEVELOP."], T("training,") - .05, t1 + .02, 490, 96, accent=(0,))
    sfx("tick", t9, -14)


# ---------------------------------------------------------------- scene 6: montage + end card (s10 - end)
def scene6():
    t0, t11 = L(10) - .1, L(11) - .15
    d2, d3, one = T("different", t0 + .5) - .08, T("different", T("sports.", t0)) - .08, T("one") - .08
    shot("s6a", t0, d2, "8459966", at=14.0, pos="50% 40%")
    shot("s6b", d2, d3, "12460907", at=9.0, pos="50% 50%")
    shot("s6c", d3, one, "7187114", at=12.0, pos="50% 40%")
    shot("s6d", one, t11 + .4, "8533122", at=14.0, pos="50% 50%", push=(1.04, 1.14))
    headline("h6", ["PERFORMANCE", "HAS NO FIXED", "BODY TYPE."], one, t11 + .3, 290, 98, accent=(2,))
    # end card: navy panel wipes up; the official logo goes in the slot (placed in post unless LOGO is set)
    logo = (f'<div class="logo"><img src="{LOGO}"></div>' if LOGO else
            ('<div class="slot"><span>OFFICIAL LOGO</span></div>' if PREVIEW else '<div class="slot blank"></div>'))
    OVER.append(f'<div class="end" id="end"><i class="grid"></i><i class="glow"></i>{logo}'
                f'<div class="en" id="en1">SPORTS SCIENCE<br>TECHNOLOGY</div><i class="rule" id="enr"></i>'
                f'<div class="et" id="en2">UNDERSTANDING THE ATHLETE<br>BEYOND PHYSIQUE.</div></div>')
    js(f'tl.fromTo("#end", {{opacity: 1, clipPath: "inset(100% 0 0 0)"}}, {{clipPath: "inset(0% 0 0 0)", duration: .6, ease: "expo.inOut", immediateRender: false}}, {t11 - .1:.3f});')
    js(f'tl.fromTo("#end .slot, #end .logo", {{opacity: 0, scale: .92}}, {{opacity: 1, scale: 1, duration: .6, ease: "expo.out", immediateRender: false}}, {t11 + .3:.3f});')
    js(f'tl.fromTo("#en1", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: .6, ease: "expo.out", immediateRender: false}}, {t11 + .15:.3f});')
    js(f'tl.fromTo("#enr", {{scaleX: 0}}, {{scaleX: 1, duration: .7, ease: "expo.out", immediateRender: false}}, {T("understanding") - .1:.3f});')
    js(f'tl.fromTo("#en2", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .6, ease: "expo.out", immediateRender: false}}, {T("understanding") - .05:.3f});')
    js(f'tl.fromTo("#end .glow", {{opacity: 0, scale: .8}}, {{opacity: 1, scale: 1.1, duration: {DUR - t11:.3f}, ease: "sine.out", immediateRender: false}}, {t11:.3f});')
    sfx("impact_soft", t11 + .1, -6)
    return t11


# ---------------------------------------------------------------- subtitles
def caps(t_end):
    """English subtitles from the VO words: phrases of up to 2 lines x ~26 characters, broken at punctuation, shown
    from the phrase's first word to the next phrase. They stop where the end card puts the same words on screen"""
    MAXL = 28
    SMALL = {"to", "a", "an", "the", "and", "of", "your", "how", "what", "does", "not", "their", "at", "in", "is", "are", "has",
             "can", "be", "but", "or", "where", "that's", "why", "every", "about", "must", "keep", "just", "most"}
    chunks, cur = [], []

    def lines_of(ws):
        out, ln = [], ""
        for w in ws:
            t = (ln + " " + w["w"]).strip()
            if len(t) > MAXL and ln:
                out.append(ln)
                ln = w["w"]
            else:
                ln = t
        out.append(ln)
        return out

    for i, w in enumerate(WORDS):
        if w["s"] >= t_end - .05:
            break
        cur.append(w)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        brk = w["w"][-1] in ".?!" or (w["w"][-1] in ",:" and len(" ".join(x["w"] for x in cur)) > 18)
        new_line = nxt is None or nxt["line"] != w["line"]
        if brk or new_line or len(lines_of(cur + ([nxt] if nxt else []))) > 2:
            carry = []
            while not (brk or new_line) and len(cur) > 2 and norm(cur[-1]["w"]) in SMALL:
                carry.insert(0, cur.pop())
            chunks.append(cur)
            cur = carry
    if cur:
        chunks.append(cur)
    for k, ch in enumerate(chunks):
        a = ch[0]["s"] - .05
        nxt = chunks[k + 1][0]["s"] - .05 if k + 1 < len(chunks) else None
        b = min(nxt, ch[-1]["e"] + .6) if nxt else min(t_end - .2, ch[-1]["e"] + .6)
        if nxt and nxt - ch[-1]["e"] < .7:
            b = nxt
        txt = "<br>".join(lines_of(ch))
        CAPS.append(f'<div class="cap" id="c{k}"><b>{txt}</b></div>')
        js(f'tl.set("#c{k}", {{opacity: 1}}, {max(0, a):.3f}); tl.set("#c{k}", {{opacity: 0}}, {b:.3f});')
    return len(chunks)


CSS = f"""
@font-face {{ font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: {INK}; font-family: "Inter", sans-serif; color: #fff; }}
.shot {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; overflow: hidden; opacity: 0; }}
.shot video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(6,8,14,.62) 0%, rgba(6,8,14,.12) 30%, rgba(6,8,14,.06) 55%, rgba(6,8,14,.55) 100%); }}
.shade.dark {{ background: linear-gradient(180deg, rgba(10,22,50,.35) 0%, rgba(6,8,14,.55) 45%, rgba(6,8,14,.7) 100%); }}
.pane {{ position: absolute; top: 0; width: 360px; height: {FH}px; overflow: hidden; }}
.pane video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.pdiv {{ position: absolute; top: 0; width: 2px; height: {FH}px; background: rgba(126,155,255,.55); z-index: 2; }}
.hl {{ position: absolute; left: 60px; right: 60px; z-index: 6; opacity: 0; font-family: "Montserrat", sans-serif; font-weight: 800;
  line-height: 1.02; letter-spacing: -.01em; text-align: center; text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,.45); }}
.hl .ln {{ display: block; overflow: hidden; padding: .04em 0 .06em; }}
.hl .in {{ display: inline-block; }}
.hl .ac {{ color: {BLUE_L}; }}
.tag {{ position: absolute; z-index: 6; opacity: 0; }}
.tag b {{ display: inline-block; font-family: "Montserrat", sans-serif; font-weight: 800; letter-spacing: .12em; }}
.tag.big b {{ font-size: 96px; padding: 6px 30px 10px; text-shadow: 0 6px 30px rgba(0,0,0,.5); }}
.tag.big b::after {{ content: ""; display: block; height: 8px; margin: 10px auto 0; width: 120px; background: {BLUE}; border-radius: 4px; }}
/* body-type board */
.board {{ position: absolute; inset: 0; z-index: 3; opacity: 0; background: radial-gradient(90% 60% at 50% 45%, #13265a 0%, {NAVY} 55%, {INK} 100%); overflow: hidden; }}
.grid {{ position: absolute; inset: 0; opacity: .22; background-image: linear-gradient(rgba(126,155,255,.35) 1px, transparent 1px),
  linear-gradient(90deg, rgba(126,155,255,.35) 1px, transparent 1px); background-size: 90px 90px; }}
.sweep {{ position: absolute; top: 0; left: 0; width: 380px; height: {FH}px; background: linear-gradient(90deg, transparent, rgba(126,155,255,.18), transparent); }}
.fig {{ position: absolute; top: 440px; width: 340px; text-align: center; opacity: 0; }}
.fig img {{ width: 300px; height: 780px; display: block; margin: 0 auto; filter: drop-shadow(0 0 26px rgba(47,91,255,.45)); }}
.fig b {{ display: block; margin-top: 26px; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 34px; letter-spacing: .14em; color: #fff; }}
.note {{ position: absolute; left: 0; right: 0; top: 1330px; text-align: center; font-size: 28px; font-weight: 500; color: {MIST}; opacity: 0; letter-spacing: .02em; }}
/* bodybuilding vs sport */
.seam {{ position: absolute; left: 0; top: 957px; width: {FW}px; height: 6px; background: {BLUE}; z-index: 5; opacity: 0; box-shadow: 0 0 24px rgba(47,91,255,.8); }}
.duo {{ position: absolute; left: 60px; z-index: 6; opacity: 0; padding: 18px 28px 20px; border-left: 8px solid {BLUE}; background: rgba(6,8,14,.62); }}
.duo span {{ display: block; font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 30px; letter-spacing: .2em; color: {MIST}; }}
.duo b {{ display: block; margin-top: 4px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 60px; letter-spacing: .01em; }}
/* assessment HUD */
.hud {{ position: absolute; inset: 0; z-index: 5; opacity: 0; pointer-events: none; }}
.cb {{ position: absolute; width: 90px; height: 90px; border: 0 solid rgba(255,255,255,.9); }}
.cb.tl {{ left: 60px; top: 240px; border-top-width: 5px; border-left-width: 5px; }}
.cb.tr {{ right: 60px; top: 240px; border-top-width: 5px; border-right-width: 5px; }}
.cb.bl {{ left: 60px; top: 1570px; border-bottom-width: 5px; border-left-width: 5px; }}
.cb.br {{ right: 60px; top: 1570px; border-bottom-width: 5px; border-right-width: 5px; }}
.scan {{ position: absolute; left: 60px; right: 60px; top: 0; height: 3px; background: linear-gradient(90deg, transparent, {BLUE_L}, transparent); box-shadow: 0 0 18px {BLUE}; }}
.hlab {{ position: absolute; left: 0; right: 0; top: 1170px; text-align: center; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 34px;
  letter-spacing: .18em; color: #fff; text-shadow: 0 3px 16px rgba(0,0,0,.6); }}
.hlab .rec {{ display: inline-block; width: 18px; height: 18px; border-radius: 50%; background: {BLUE_L}; margin-right: 18px; vertical-align: 3px; box-shadow: 0 0 14px {BLUE}; }}
.ring {{ position: absolute; width: 300px; height: 300px; fill: none; stroke: rgba(126,155,255,.9); stroke-width: 3; }}
.ring .dash {{ stroke-dasharray: 10 14; stroke: rgba(255,255,255,.55); stroke-width: 2; }}
/* end card */
.end {{ position: absolute; inset: 0; z-index: 8; opacity: 0; background: radial-gradient(80% 50% at 50% 42%, #15296a 0%, {NAVY} 60%, {INK} 100%); text-align: center; }}
.end .glow {{ position: absolute; left: 140px; top: 300px; width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, rgba(47,91,255,.28), transparent 65%); }}
.slot {{ position: absolute; left: 290px; top: 560px; width: 500px; height: 260px; border-radius: 28px; border: 3px dashed rgba(201,212,242,.45); display: grid; place-items: center; }}
.slot span {{ font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 26px; letter-spacing: .22em; color: rgba(201,212,242,.6); }}
.slot.blank {{ border-color: transparent; }}
.logo {{ position: absolute; left: 150px; top: 430px; width: 780px; height: 450px; border-radius: 30px; background: #fff; padding: 22px 28px;
  box-shadow: 0 30px 80px rgba(0,0,0,.45), 0 0 0 3px rgba(126,155,255,.35); }}
.logo img {{ display: block; width: 100%; height: 100%; object-fit: contain; }}
.en {{ position: absolute; left: 0; right: 0; top: 960px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 70px; line-height: 1.06; letter-spacing: .04em; opacity: 0; }}
.rule {{ position: absolute; left: 440px; top: 1140px; width: 200px; height: 6px; border-radius: 3px; background: {BLUE}; transform-origin: center; }}
.et {{ position: absolute; left: 0; right: 0; top: 1185px; font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 38px; line-height: 1.3; letter-spacing: .12em; color: {MIST}; opacity: 0; }}
/* subtitles: bottom, inside the Reels safe zone (above the caption / buttons area) */
.cap {{ position: absolute; left: 70px; right: 70px; top: 1400px; text-align: center; z-index: 7; opacity: 0; }}
.cap b {{ display: inline-block; padding: 12px 26px 14px; border-radius: 14px; background: rgba(6,8,14,.66); font-weight: 600; font-size: 46px; line-height: 1.22;
  letter-spacing: -.005em; color: #fff; }}
#grain {{ position: absolute; inset: 0; opacity: .06; background: url(assets/img/grain.png); mix-blend-mode: overlay; z-index: 9; pointer-events: none; }}
#vig {{ position: absolute; inset: 0; z-index: 9; pointer-events: none; background: radial-gradient(120% 80% at 50% 50%, transparent 60%, rgba(0,0,0,.35) 100%); }}
"""


def main():
    scene1()
    scene2()
    scene3()
    scene4()
    scene5()
    t11 = scene6()
    n_caps = caps(t11 + .1)
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Sports Science Technology: Performance has no fixed body type 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      {"".join(SHOTS)}
      {"".join(OVER)}
      {"".join(CAPS)}
      <div id="vig"></div>
      <div id="grain"></div>
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
    json.dump(sorted(SFX, key=lambda e: e["t"]), open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    json.dump({"dur": DUR, "end_card": round(t11, 3), "logo": LOGO or None, "preview": PREVIEW},
              open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
    print(f"wrote index.html: {len(A)} timeline lines, {len(SHOTS)} shots, {n_caps} subtitles, {len(SFX)} sfx, {DUR} s")


if __name__ == "__main__":
    main()
