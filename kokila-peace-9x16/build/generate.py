"""Dr S Kokila: "Can an ₹85,000 device measure your peace of mind?" 9:16 talking head (1080x1920, 30 fps).

Match the owner's reference reel (instagram.com/reel/DbVgs57zdhq: picture-in-picture celebrity hook, proof, steps,
1-2 word blue pill captions, stock B-roll, a music bed) and beat it the way our faceless reels and the surrender reel do:
  * a split screen (top: a screen, bottom: her face) with the caption pill on the seam, cutting to full-frame face
    sections for the big lines, zoom-blur transitions between them (surrender-ad-9x16);
  * the cold open is Deepinder Goyal's own line from the Raj Shamani podcast ("...it measures blood flow to your
    brain", Temple on his temple) in the top half while she listens below, the owner's text hook on the seam;
  * every beat gets its own motion graphic in the top half instead of stock clips: the price tag, what Temple measures,
    "results pending", ₹85,000 falling to ₹0, the circle of people turning red then warm, a stress meter, a battery;
  * the lines she did not record are on screen as text (owner: "place them as texts whatever is missing"): "How do you
    feel afterwards? Drained. Anxious. Exhausted.", "As a doctor", "It's the company you keep." and the closing lines.
    No CTA (owner: "if there is no cta then don't add it").
Podcast footage: short, credited ("Source: Raj Shamani podcast"), graded up from the flat screen recording.
Clock: the tight cut (build/tight.py -> assets/video/tight.mp4), words from build/words_final.py.
python3 build/generate.py  ->  index.html, plan/sfx_events.json, plan/edit.json
"""
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WF = json.load(open(os.path.join(ROOT, "plan", "words_final.json")))
WT = json.load(open(os.path.join(ROOT, "plan", "words_tight.json")))
VDUR = round(WT["dur"], 2)                      # the face video
END = 0.0                                       # v2: no end cards (owner: remove what she does not say); the cut ends on her face
DUR = round(VDUR + END, 2)
BLUE, NAVY, YEL, CORAL, GREEN, CREAM = "#2448E8", "#0E1A3A", "#FFD23F", "#E8443A", "#13895A", "#FFF6EA"
A, SFX, TOPH, OVER, CAPS = [], [], [], [], []
R = random.Random(7)
SEAM = 920                                      # the split line: top 0..920 a screen, bottom 920..1920 her face


def js(s):
    A.append("      " + s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(max(0.0, t), 3)})


def norm(w):
    return w.lower().strip(".,?!'\"").replace("’", "'").replace("criticising", "criticizing")


def T(text, after=0.0, key="s"):
    """time of the first word `text` at or after `after`"""
    for w in WF:
        if w["s"] >= after - .05 and norm(w["w"]) == text:
            return w[key]
    raise KeyError(text)


def show(sel, t0, t1=None, d=.35, y=60, sc=.92, ease="back.out(1.8)"):
    js(f'tl.fromTo("{sel}", {{opacity: 0, y: {y}, scale: {sc}}}, {{opacity: 1, y: 0, scale: 1, duration: {d}, ease: "{ease}", immediateRender: false}}, {t0:.3f});')
    if t1 is not None:
        js(f'tl.to("{sel}", {{opacity: 0, y: -40, duration: .25, ease: "power2.in"}}, {t1 - .25:.3f});')


def pop(sel, t, d=.3):
    js(f'tl.fromTo("{sel}", {{opacity: 0, scale: .3}}, {{opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.6)", immediateRender: false}}, {t:.3f});')


def scene(sid, t0, t1, inner, cls="gfx"):
    """a top-half scene, visible t0..t1"""
    TOPH.append(f'<div class="ts {cls}" id="{sid}">{inner}</div>')
    js(f'tl.set("#{sid}", {{opacity: 1}}, {t0:.3f}); tl.set("#{sid}", {{opacity: 0}}, {t1:.3f});')


def avatar(c, skin="#ffd9bf", size=120, cid=""):
    return (f'<svg class="av" {f"id={cid!r}" if cid else ""} width="{size}" height="{size}" viewBox="0 0 40 40"><circle cx="20" cy="20" r="20" fill="{c}"/>'
            f'<circle cx="20" cy="16" r="7" fill="{skin}"/><path d="M7 35c2.5-7 8-9 13-9s10.5 2 13 9" fill="#fff" opacity=".92"/></svg>')


ICON = {
    "brain": '<path d="M9 4a3 3 0 0 0-3 3v1a3 3 0 0 0-2 5 3 3 0 0 0 2 5v1a3 3 0 0 0 6 0V4.5A2.5 2.5 0 0 0 9 4zM15 4a3 3 0 0 1 3 3v1a3 3 0 0 1 2 5 3 3 0 0 1-2 5v1a3 3 0 0 1-6 0V4.5A2.5 2.5 0 0 1 15 4z"/>',
    "pulse": '<path d="M2 12h4l2-6 4 12 3-9 2 3h5"/>',
    "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    "run": '<circle cx="14" cy="4" r="2"/><path d="M8 21l3-6 3 2v5M6 12l3-4h5l2 4 3 1M11 15l-3-2"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    "heart": '<path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8A8.5 8.5 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5z"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "spark": '<path d="M12 3l1.8 5.4L19 10l-5.2 1.6L12 17l-1.8-5.4L5 10l5.2-1.6z"/>',
}


def icon(n, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24">{ICON[n]}</svg>'


def clip(vid, t0, t1, media, extra=""):
    """a podcast clip in the top half (muted; its sound, where used, is in the mix), graded up from the flat recording"""
    return (f'<video class="pod" id="{vid}" src="footage/podcast_169.mp4" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
            f'data-media-start="{media:.3f}" data-track-index="{2 + len(TOPH) % 3}" muted playsinline></video>{extra}'
            '<div class="credit">Source: Raj Shamani podcast</div>')


# ---------------------------------------------------------------- the beats (times from her words)
t_l1 = T("deepinder")
t_measure, t_brain, t_stress, t_sleep, t_ex = T("measure"), T("brain's"), T("stress"), T("sleep"), T("exercise")
t_but, t_maybe, t_does, t_yet = T("but"), T("maybe"), T("does"), T("yet")
t_so, t_free, t_subs, t_time = T("so", t_yet), T("free"), T("subscription"), T("time", T("subscription"))
t_and3, t_people = T("and", t_time), T("people", t_time)
t_just, t_compl, t_crit, t_disr = T("just"), T("complaining"), T("criticizing"), T("disrespecting")
t_or = T("or", t_disr)
t_loving, t_supp, t_insp, t_best, t_self = T("loving"), T("supporting"), T("inspiring"), T("best"), T("yourself", T("best"))
t_because6 = T("because", t_self)
t_peace, t_mental, t_most = T("peace"), T("mental", T("peace")), T("most", T("peace"))
t_so7, t_beaut7 = T("so", t_most), T("beautiful", t_most)
t_because8, t_great, t_upgrade, t_device = T("because", t_beaut7), T("greatest"), T("upgrade"), T("device")
t_it8, t_beaut8, t_life8 = T("it", t_device), T("beautiful", t_device), T("life", T("beautiful", t_device), "e")
BEAT = None                                     # v2: the unrecorded text beat is gone
# v4: Deepinder's line plays full screen (podcast 47.15 s on; "...to your brain." ends ~2.62 s in), then black until she starts
BITE_LEN, ECHO_FROM = 2.62, 2.30               # the bite, and where his last word "brain" starts (its echo tail)
T_BLACK = 2.56
T_SPLIT = round(t_l1 - .06, 3)
HOOK_END = round(T("85") - .05, 3)               # the hook text holds until the price lands on "85,000"

# (mode, t0, t1): split / full / beat / end
SECTIONS = [("split", 0.0, t_but - .1), ("full", t_but - .1, t_does - .1), ("split", t_does - .1, t_because6 - .1),
            ("full", t_because6 - .1, t_so7 - .1), ("split", t_so7 - .1, DUR)]


BROLL = json.load(open(os.path.join(ROOT, "footage", "broll", "pexels.json")))


def broll(sid, t0, t1, vid, at=0.0, label=None, pos="50% 40%", extra=""):
    """v3 (client: "less animated explanations, more real-life reference video"): a Pexels clip in the top half"""
    lab = f'<div class="blab" id="{sid}l">{label}</div>' if label else ""
    scene(sid, t0, t1, f'<video class="br" id="{sid}v" src="footage/broll/{vid}.mp4" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
                       f'data-media-start="{at:.3f}" data-track-index="{2 + len(TOPH) % 3}" muted playsinline style="object-position:{pos}"></video>'
                       f'<i class="shade2"></i>{lab}{extra}', "vid")
    js(f'tl.fromTo("#{sid}v", {{scale: 1.0}}, {{scale: 1.08, duration: {t1 - t0:.3f}, ease: "none", immediateRender: false}}, {t0:.3f});')
    if label:
        show(f"#{sid}l", t0 + .05, d=.3, y=24)


def build_top():
    # the cold open: Deepinder's own line, the device on his temple
    # v4 (owner): Deepinder full screen while we hear him; as he stops, an instant black, then the split screen
    OVER.append(f'<div class="ov deep" id="deep" style="opacity:1"><video class="podfull" id="pA" src="footage/podcast_169.mp4" data-start="0" '
                f'data-duration="{T_BLACK:.3f}" data-media-start="47.150" data-track-index="5" muted playsinline></video>'
                '<div class="credit">Source: Raj Shamani podcast</div><div class="say" id="say0">"It measures blood flow to your brain."</div></div>'
                '<div class="ov blk" id="blk"></div>')
    js(f'tl.fromTo("#pA", {{scale: 1.0}}, {{scale: 1.06, duration: {T_BLACK:.3f}, ease: "none", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#say0", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .3, ease: "expo.out", immediateRender: false}}, 1.25);')
    js(f'tl.set("#deep", {{opacity: 0}}, {T_BLACK:.3f}); tl.set("#blk", {{opacity: 1}}, {T_BLACK:.3f}); tl.set("#blk", {{opacity: 0}}, {T_SPLIT:.3f});')
    js(f'tl.fromTo("#botin", {{scale: 1.3, filter: "blur(8px)"}}, {{scale: 1, filter: "blur(0px)", duration: .35, ease: "expo.out", immediateRender: false}}, {T_SPLIT:.3f});')
    js(f'tl.fromTo("#top", {{scale: 1.12, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {T_SPLIT:.3f});')
    js(f'tl.set("#seamline", {{opacity: 1}}, {T_SPLIT:.3f});')      # the seam only exists once the split screen does
    sfx("hit", T_SPLIT)
    # "Deepinder Goyal's Temple costs 85,000 rupees": the price tag counts up over his clip
    tag = (f'<div class="price glass" id="pr1"><div class="pl">{icon("card")} TEMPLE by Deepinder Goyal</div>'
           f'<div class="pv">₹<b id="pr1n">0</b></div></div>')
    scene("ts1", T_SPLIT, t_measure - .1, clip("pC", T_SPLIT, t_measure - .1, 29.0) + tag, "vid")
    pop("#pr1", T("costs") - .1)
    for k, v in enumerate(["0", "8,500", "21,000", "39,000", "57,000", "71,000", "80,500", "85,000"]):
        js(f'tl.set("#pr1n", {{textContent: "{v}"}}, {T("85") - .35 + k * .07:.3f});')
    js(f'tl.fromTo("#pr1", {{scale: 1}}, {{keyframes: {{scale: [1, 1.12, 1]}}, duration: .3, ease: "power2.out", immediateRender: false}}, {T("85") + .2:.3f});')
    sfx("ding", T("85") + .2)
    # "It can measure your brain's blood flow and how your body responds": the device; then real life, cut on each word
    scene("ts2", t_measure - .1, t_stress - .1, clip("pD", t_measure - .1, t_stress - .1, 33.8), "vid")
    # v5 (earshot: "salient hit density 2.0/s, high"): the quick footage cuts inside a line carry no whoosh
    broll("tb1", t_stress - .1, t_sleep - .05, "8632780", 1.0, "Stress")
    broll("tb2", t_sleep - .05, t_ex - .05, "6639660", 2.0, "Sleep")
    broll("tb3", t_ex - .05, t_but - .1, "4763892", 3.0, "Exercise", "50% 55%")
    # "Does it work? We don't know yet.": a skeptical pose with a smartwatch
    broll("tb4", t_does - .1, t_so - .1, "8165946", 2.0, "Results: not yet known")
    # "a tracker that is completely free ... no subscription ... not even your time": ₹85,000 falls to ₹0
    free = (f'<div class="price glass big" id="pr4"><div class="pl">{icon("heart")} A tracker that is</div><div class="pv">₹<b id="pr4n">85,000</b></div>'
            f'<div class="fr" id="fr4">FREE</div></div>'
            f'<div class="nochip glass" id="nc1">{icon("card")}<span>Subscription</span><i class="stk" id="st1"></i></div>'
            f'<div class="nochip glass" id="nc2">{icon("clock")}<span>Your time</span><i class="stk" id="st2"></i></div>')
    scene("ts4", t_so - .1, t_and3 - .1, free)
    show("#pr4", t_so - .1)
    for k, v in enumerate(["85,000", "61,000", "38,000", "17,000", "6,000", "900", "0"]):
        js(f'tl.set("#pr4n", {{textContent: "{v}"}}, {t_free - .45 + k * .07:.3f});')
    pop("#fr4", t_free + .05)
    sfx("success", t_free + .05)
    show("#nc1", t_subs - .2, y=40)
    js(f'tl.fromTo("#st1", {{scaleX: 0}}, {{scaleX: 1, duration: .25, ease: "power3.out", immediateRender: false}}, {t_subs + .55:.3f});')
    sfx("scratch", t_subs + .55)
    show("#nc2", t_time - .9, y=40)
    js(f'tl.fromTo("#st2", {{scaleX: 0}}, {{scaleX: 1, duration: .25, ease: "power3.out", immediateRender: false}}, {t_time + .1:.3f});')
    sfx("scratch", t_time + .1)
    # "And that tracker is the people around you.": friends at a table, the line on top
    broll("tb5", t_and3 - .1, t_just - .1, "9782812", 1.0, None, "50% 45%",
          '<div class="big3" id="b3">THE PEOPLE<br><em>AROUND YOU</em></div>')
    js(f'tl.fromTo("#b3", {{opacity: 0, scale: 1.3}}, {{opacity: 1, scale: 1, duration: .35, ease: "expo.out", immediateRender: false}}, {t_people - .05:.3f});')
    sfx("rise", t_people - 1.2)
    sfx("hit", t_people)
    sfx("sub", t_people)
    # "are the people in your life ... constantly complaining, criticizing and disrespecting you": real arguments
    broll("tb6", t_just - .1, t_crit - .1, "8135467", 2.0, None, "55% 40%")
    broll("tb7", t_crit - .1, t_disr - .1, "7640672", 4.0, None, "50% 35%")
    broll("tb8", t_disr - .1, t_or - .1, "5658237", 3.0, None, "50% 40%")
    js(f'tl.fromTo(".argue", {{opacity: 0}}, {{opacity: 1, duration: .3, immediateRender: false}}, {t_compl:.3f});')
    sfx("error", t_compl)
    # "or are the people ... loving you, supporting you and inspiring you to become the best version of yourself"
    broll("tb9", t_or - .1, t_loving - .1, "8888536", 4.0, None, "50% 40%")
    broll("tb10", t_loving - .1, t_supp - .1, "8058107", 4.0, None, "60% 40%")
    broll("tb11", t_supp - .1, t_insp - .1, "8416831", 2.0, None, "50% 45%")
    broll("tb12", t_insp - .1, t_because6 - .1, "9579386", 2.5, None, "45% 40%")
    sfx("sparkle", t_best)
    # "So surround yourself with people that make your life more beautiful": friends around a dinner table
    broll("tb13", t_so7 - .1, t_because8 - .1, "8773862", 1.0, None, "50% 45%")
    sfx("sparkle", t_beaut7)
    # "the greatest upgrade to your mental health may not be a device, it is simply the beautiful people in your life"
    broll("tb14", t_because8 - .1, t_it8 - .1, "7223986", 6.9, None, "50% 50%")
    broll("tb15", t_it8 - .1, DUR, "5899973", 3.0, None, "50% 40%")
    sfx("success", t_beaut8)


def build_overlays():
    """full-frame sections: her face, with as little type as possible"""
    # "But can you afford it? Maybe not."
    OVER.append(f'<div class="ov" id="o1"><div class="big1" id="o1a">₹85,000?</div><div class="stamp" id="o1b">MAYBE NOT.</div></div>')
    js(f'tl.set("#o1", {{opacity: 1}}, {t_but - .1:.3f}); tl.set("#o1", {{opacity: 0}}, {t_does - .1:.3f});')
    show("#o1a", T("afford") - .1, y=40)
    js(f'tl.fromTo("#o1b", {{opacity: 0, scale: 2.2, rotation: -14}}, {{opacity: 1, scale: 1, rotation: -6, duration: .22, ease: "back.out(1.6)", immediateRender: false}}, {t_maybe:.3f});')
    sfx("stamp", t_maybe + .05)
    # the doctor line: her name only
    OVER.append(f'<div class="ov" id="o4"><div class="namec glass" id="nm"><b>Dr S Kokila</b></div></div>')
    js(f'tl.set("#o4", {{opacity: 1}}, {t_because6 - .1:.3f}); tl.set("#o4", {{opacity: 0}}, {t_so7 - .1:.3f});')
    js(f'tl.fromTo("#nm", {{opacity: 0, x: -120}}, {{opacity: 1, x: 0, duration: .45, ease: "expo.out", immediateRender: false}}, {t_because6:.3f});')
    sfx("whoosh", t_because6)


def build_layout():
    for k, (mode, a, b) in enumerate(SECTIONS):
        if mode == "split":
            js(f'tl.set("#split", {{opacity: 1}}, {a:.3f}); tl.set("#split", {{opacity: 0}}, {b:.3f});')
            if k:
                js(f'tl.fromTo("#botin", {{scale: 1.45, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .4, ease: "expo.out", immediateRender: false}}, {a:.3f});')
                js(f'tl.fromTo("#top", {{scale: 1.12, filter: "blur(12px)"}}, {{scale: 1, filter: "blur(0px)", duration: .42, ease: "expo.out", immediateRender: false}}, {a:.3f});')
                sfx("whoosh", a - .08)
            js(f'tl.fromTo("#botin", {{scale: 1}}, {{scale: 1.06, duration: {b - a:.2f}, ease: "none", immediateRender: false}}, {a + .4:.3f});')
        elif mode in ("full", "beat"):
            js(f'tl.set("#full", {{opacity: 1}}, {a:.3f}); tl.set("#full", {{opacity: 0}}, {b:.3f});')
            js(f'tl.fromTo("#fullin", {{scale: 1.2, filter: "blur(14px)"}}, {{scale: 1.0, filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {a:.3f});')
            js(f'tl.fromTo("#fullv", {{scale: 1.0}}, {{scale: 1.1, duration: {b - a:.2f}, ease: "power1.inOut", immediateRender: false}}, {a:.3f});')
            js(f'tl.fromTo("#flash", {{opacity: .55}}, {{opacity: 0, duration: .25, ease: "power2.out", immediateRender: false}}, {a:.3f});')
            sfx("whoosh_big" if mode == "full" else "swish", a - .1)
            if mode == "beat":
                js(f'tl.fromTo("#fullv", {{filter: "blur(0px) saturate(1)"}}, {{filter: "blur(18px) saturate(.3)", duration: .4, immediateRender: false}}, {a:.3f});')
                js(f'tl.set("#fullv", {{filter: "none"}}, {b:.3f});')


# ---------------------------------------------------------------- captions: 1-3 words, the blue pill
KEY = {"temple", "85,000", "rupees", "brain's", "blood", "flow", "stress", "sleep", "exercise", "afford", "work", "free",
       "subscription", "time", "people", "complaining", "criticizing", "disrespecting", "loving", "supporting", "inspiring", "best", "peace",
       "mind", "mental", "health", "beautiful", "greatest", "upgrade", "device", "life"}


def caption_groups():
    ws = []
    for w in WF:
        if w["w"].startswith(",") and ws and ws[-1]["w"][-1:].isdigit():      # Whisper splits "85,000" in two
            ws[-1] = dict(ws[-1], w=ws[-1]["w"] + w["w"], e=w["e"])
            continue
        ws.append(dict(w))
    ws = [w for w in ws if w["s"] < VDUR - .05]
    groups, cur = [], []
    cuts = [s[1] for s in SECTIONS]
    for w in ws:
        brk = cur and (len(cur) >= 3 or cur[-1]["w"][-1] in ",.?!" or w["s"] - cur[-1]["e"] > .45
                       or any(cur[0]["s"] < c <= w["s"] for c in cuts) or sum(len(x["w"]) + 1 for x in cur) + len(w["w"]) > 18)
        if brk:
            groups.append(cur)
            cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    return groups


def mode_at(t):
    return next((m for m, a, b in SECTIONS if a <= t < b), "split")


def build_caps():
    gs = caption_groups()
    for k, g in enumerate(gs):
        t0 = g[0]["s"] - .05
        t1 = min(gs[k + 1][0]["s"] - .05 if k + 1 < len(gs) else VDUR, g[-1]["e"] + .6)
        if t0 < HOOK_END - .1:              # the hook text is on the seam then
            continue
        m = mode_at(g[0]["s"])
        txt = " ".join(f'<span class="{"k" if norm(w["w"]) in KEY else ""}">{w["w"].replace("85", "85").replace(",000", ",000")}</span>' for w in g)
        txt = txt.replace('</span> <span class="k">,000', ',000').replace('<span class="k">85</span> <span class="k">,000</span>', '<span class="k">85,000</span>')
        CAPS.append(f'<div class="cap {"seam" if m == "split" else "low"}" id="cp{k}"><b>{txt}</b></div>')
        js(f'tl.fromTo("#cp{k}", {{opacity: 0, scale: .82, y: 14}}, {{opacity: 1, scale: 1, y: 0, duration: .16, ease: "back.out(2.6)", immediateRender: false}}, {t0:.3f}); '
           f'tl.set("#cp{k}", {{opacity: 0}}, {t1:.3f});')


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: {NAVY}; font-family: Inter; color: {NAVY}; }}
video {{ display: block; }}
/* split: top a screen, bottom her face */
#split {{ position: absolute; inset: 0; opacity: 1; }}
#top {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {SEAM}px; overflow: hidden; transform-origin: 50% 70%;
  background: radial-gradient(70% 60% at 15% 10%, rgba(36,72,232,.18), transparent 70%), radial-gradient(60% 60% at 90% 90%, rgba(255,210,63,.35), transparent 70%), {CREAM}; }}
#bot {{ position: absolute; left: 0; top: {SEAM}px; width: {FW}px; height: {FH - SEAM}px; overflow: hidden; background: #222; }}
#botin {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH - SEAM}px; transform-origin: 50% 47%; }}
#botin video, #fullv {{ width: 100%; height: 100%; object-fit: cover; }}
#seamline {{ position: absolute; left: 0; top: {SEAM - 3}px; width: {FW}px; height: 6px; background: linear-gradient(90deg, {BLUE}, {YEL}, {BLUE}); z-index: 6; opacity: 0; }}
#full {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; }}
#fullin {{ position: absolute; inset: 0; transform-origin: 50% 40%; }}
#fullv {{ position: absolute; inset: 0; transform-origin: 50% 38%; }}
.ts {{ position: absolute; inset: 0; opacity: 0; }}
.deep {{ background: #000; z-index: 6; }}
.podfull {{ position: absolute; left: -1540px; top: 0; width: 3413px; height: 1920px; filter: brightness(1.42) contrast(1.18) saturate(1.18); transform-origin: 2080px 700px; }}
.deep .say {{ bottom: 330px; font-size: 52px; }}
.blk {{ background: #000; z-index: 9; }}
.br {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(1.08) contrast(1.05); }}
.shade2 {{ position: absolute; left: 0; right: 0; bottom: 0; height: 260px; background: linear-gradient(180deg, transparent, rgba(14,26,58,.45)); }}
.blab {{ position: absolute; left: 40px; top: 250px; padding: 12px 26px; border-radius: 18px; background: rgba(255,255,255,.9); color: {NAVY};
  font-size: 40px; font-weight: 800; opacity: 0; box-shadow: 0 12px 30px rgba(14,26,58,.25); }}
.big3 {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-size: 112px; font-weight: 800; line-height: .98; letter-spacing: -.04em;
  color: #fff; text-shadow: 0 10px 40px rgba(0,0,0,.6); opacity: 0; }}
.big3 em {{ font-style: normal; color: {YEL}; }}
.ts.vid {{ background: #000; }}
.pod {{ position: absolute; left: -461px; top: -60px; width: 1882px; height: 1058px; filter: brightness(1.42) contrast(1.18) saturate(1.18); }}
.credit {{ position: absolute; right: 24px; top: 24px; padding: 8px 16px; border-radius: 999px; background: rgba(0,0,0,.55); color: #fff; font-size: 28px; font-weight: 700; }}
.shade {{ position: absolute; left: 0; right: 0; bottom: 0; height: 520px; background: linear-gradient(180deg, transparent, rgba(14,26,58,.75)); }}
.say {{ position: absolute; left: 60px; right: 60px; bottom: 230px; text-align: center; color: #fff; font-size: 44px; font-weight: 700; font-style: italic;
  text-shadow: 0 3px 16px rgba(0,0,0,.8); opacity: 0; }}
.glass {{ border-radius: 34px; background: rgba(255,255,255,.82); border: 2px solid rgba(255,255,255,.95); box-shadow: 0 24px 60px rgba(14,26,58,.22); backdrop-filter: blur(14px); }}
.ic {{ width: 54px; height: 54px; fill: none; stroke: {BLUE}; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; flex: none; }}
.price {{ position: absolute; left: 40px; top: 560px; padding: 26px 36px; opacity: 0; }}
.price .pl {{ display: flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 700; color: #4a5370; }}
.price .pv {{ margin-top: 6px; font-size: 104px; font-weight: 800; letter-spacing: -.04em; line-height: 1; color: {NAVY}; }}
.price.big {{ left: 90px; right: 90px; top: 220px; text-align: center; padding: 36px; }}
.price.big .pl {{ justify-content: center; }}
.price.big .pv {{ font-size: 150px; }}
.fr {{ position: absolute; right: 40px; top: -36px; padding: 10px 28px; border-radius: 18px; background: {GREEN}; color: #fff; font-size: 54px; font-weight: 800; transform: rotate(6deg); opacity: 0; }}
.nochip {{ position: absolute; display: flex; align-items: center; gap: 18px; padding: 22px 34px; font-size: 42px; font-weight: 800; opacity: 0; }}
#nc1 {{ left: 90px; top: 560px; }} #nc2 {{ right: 90px; top: 700px; }}
.stk {{ position: absolute; left: 20px; right: 20px; top: 50%; height: 8px; border-radius: 4px; background: {CORAL}; transform: scaleX(0); transform-origin: left center; }}
.mchip {{ position: absolute; display: flex; align-items: center; gap: 16px; width: 460px; padding: 22px 28px; font-size: 38px; font-weight: 800; opacity: 0; }}
.pulse {{ position: absolute; left: 0; bottom: 20px; width: 1080px; height: 120px; fill: none; stroke: {YEL}; stroke-width: 6; stroke-linecap: round; stroke-linejoin: round; }}
.pulse path {{ stroke-dasharray: 1000; }}
.loader {{ position: absolute; left: 90px; right: 90px; top: 260px; padding: 44px 48px; opacity: 0; }}
.lt {{ font-size: 76px; font-weight: 800; letter-spacing: -.03em; }}
.lr {{ margin-top: 26px; display: flex; align-items: center; gap: 18px; font-size: 36px; font-weight: 700; color: #4a5370; }}
.lr b {{ margin-left: auto; color: {CORAL}; }}
.spin {{ width: 44px; height: 44px; border-radius: 50%; border: 6px solid rgba(36,72,232,.2); border-top-color: {BLUE}; }}
.bar {{ margin-top: 26px; height: 22px; border-radius: 11px; background: rgba(36,72,232,.12); overflow: hidden; }}
.bar i {{ display: block; height: 100%; background: {BLUE}; transform-origin: left center; transform: scaleX(0); }}
.ls {{ margin-top: 30px; font-size: 48px; font-weight: 800; color: {BLUE}; opacity: 0; }}
.rp {{ position: absolute; width: 140px; height: 140px; opacity: 0; }}
.rp .av, .you .av, .orb .av, .hpv .av {{ filter: drop-shadow(0 12px 22px rgba(14,26,58,.25)); }}
.mood {{ position: absolute; right: -8px; top: -8px; width: 58px; height: 58px; border-radius: 50%; display: grid; place-items: center; opacity: 0; }}
.mood svg {{ width: 34px; height: 34px; fill: none; stroke: #fff; stroke-width: 3; stroke-linecap: round; }}
.mood.bad {{ background: {CORAL}; }} .mood.good {{ background: {GREEN}; }}
.mood.good svg {{ fill: #fff; stroke: none; }}
.you {{ position: absolute; left: 455px; top: 385px; width: 170px; text-align: center; opacity: 0; }}
.you em {{ display: block; margin-top: 4px; font-style: normal; font-size: 32px; font-weight: 800; color: {BLUE}; }}
.meter {{ position: absolute; left: 90px; right: 90px; top: 760px; display: flex; align-items: center; gap: 22px; padding: 18px 30px; font-size: 34px; font-weight: 800; opacity: 0; }}
.mtr {{ flex: 1; height: 26px; border-radius: 13px; background: rgba(14,26,58,.1); overflow: hidden; }}
.mtr i {{ display: block; height: 100%; width: 100%; background: {YEL}; transform-origin: left center; transform: scaleX(.2); }}
.meter b {{ width: 90px; text-align: right; }}
.bub {{ position: absolute; padding: 14px 26px; border-radius: 26px; font-size: 38px; font-weight: 800; color: #fff; opacity: 0; box-shadow: 0 14px 30px rgba(14,26,58,.25); }}
.bub.red {{ background: {CORAL}; }} .bub.warm {{ background: {GREEN}; }}
#bw0, #wbg0 {{ left: 30px; top: 200px; }} #bw1, #wbg1 {{ right: 30px; top: 200px; }} #bw2, #wbg2 {{ right: 30px; top: 660px; }}
.circle.warm, .gfx.warm {{ background: radial-gradient(70% 60% at 50% 40%, rgba(255,210,63,.35), transparent 75%); }}
.upl {{ position: absolute; left: 0; right: 0; top: 768px; display: flex; justify-content: center; align-items: center; gap: 14px; font-size: 44px; font-weight: 800; color: {GREEN}; opacity: 0; }}
.upl svg {{ width: 56px; height: 56px; fill: none; stroke: {GREEN}; stroke-width: 3; }}
.hpv {{ position: absolute; width: 84px; height: 84px; opacity: 0; }}
.hcore {{ position: absolute; left: 470px; top: 350px; width: 140px; height: 140px; opacity: 0; }}
.hcore svg {{ width: 140px; height: 140px; fill: {CORAL}; stroke: none; filter: drop-shadow(0 14px 30px rgba(255,90,78,.45)); }}
.bigw {{ position: absolute; left: 0; right: 0; top: 760px; text-align: center; font-size: 84px; font-weight: 800; letter-spacing: -.03em; opacity: 0; }}
.bigw em, .big2 em, .e1 em, .e3 em {{ font-style: normal; color: {YEL}; }}
.bigw em {{ color: {BLUE}; }}
.upg {{ position: absolute; left: 70px; right: 70px; top: 220px; opacity: 0; }}
.ul {{ font-size: 70px; font-weight: 800; letter-spacing: -.03em; text-align: center; }}
.dev, .ppl {{ position: relative; margin-top: 40px; display: flex; align-items: center; gap: 28px; padding: 30px 36px; opacity: 0; }}
.dev b, .ppl b {{ display: block; font-size: 44px; font-weight: 800; }}
.dev span, .ppl span {{ display: block; margin-top: 4px; font-size: 30px; font-weight: 600; color: #4a5370; }}
.patch {{ flex: none; width: 90px; height: 64px; border-radius: 32px; background: linear-gradient(160deg, #fff, #d9dde6); box-shadow: inset 0 0 0 3px #c3c8d4; }}
.pps {{ display: flex; flex: none; }} .pps svg {{ margin-right: -26px; }}
.ppl {{ border-color: {GREEN}; }}
/* full-frame overlays */
.ov {{ position: absolute; inset: 0; opacity: 0; z-index: 4; }}
.big1 {{ position: absolute; left: 0; right: 0; top: 300px; text-align: center; font-size: 170px; font-weight: 800; letter-spacing: -.05em; color: #fff;
  text-shadow: 0 10px 40px rgba(0,0,0,.45); opacity: 0; }}
.stamp {{ position: absolute; left: 230px; top: 520px; padding: 14px 34px; border: 10px solid {CORAL}; border-radius: 24px; color: {CORAL}; background: rgba(255,255,255,.9);
  font-size: 92px; font-weight: 800; letter-spacing: .02em; opacity: 0; }}
.big2 {{ position: absolute; left: 0; right: 0; top: 140px; text-align: center; font-size: 118px; font-weight: 800; line-height: .98; letter-spacing: -.04em; color: #fff;
  text-shadow: 0 10px 40px rgba(0,0,0,.5); opacity: 0; }}
.orb {{ position: absolute; width: 120px; height: 120px; opacity: 0; }}
.beat {{ background: rgba(14,26,58,.72); }}
.q {{ position: absolute; left: 0; right: 0; top: 420px; text-align: center; font-size: 66px; font-weight: 800; color: #fff; opacity: 0; }}
.dw {{ position: absolute; left: 0; right: 0; text-align: center; font-size: 140px; font-weight: 800; letter-spacing: -.04em; color: #fff; opacity: 0; }}
#o3w0 {{ top: 620px; }} #o3w1 {{ top: 800px; color: {YEL}; }} #o3w2 {{ top: 980px; color: {CORAL}; }}
.bat {{ position: absolute; left: 400px; top: 1250px; display: flex; align-items: center; gap: 20px; }}
.bb {{ width: 220px; height: 110px; border: 8px solid #fff; border-radius: 22px; padding: 8px; display: flex; align-items: flex-end; }}
.bb i {{ display: block; width: 100%; height: 100%; border-radius: 10px; background: {GREEN}; transform-origin: left center; transform: scaleX(.8); }}
.bn {{ width: 16px; height: 46px; border-radius: 6px; background: #fff; margin-left: -12px; }}
.bat b {{ font-size: 52px; font-weight: 800; color: #fff; }}
.namec {{ position: absolute; left: 60px; top: 260px; padding: 22px 34px; opacity: 0; }}
.namec span {{ display: block; font-size: 30px; font-weight: 700; color: {BLUE}; text-transform: uppercase; letter-spacing: .08em; }}
.namec b {{ display: block; font-size: 58px; font-weight: 800; }}
.brainc {{ position: absolute; right: 60px; top: 470px; display: flex; align-items: center; gap: 20px; padding: 22px 30px; opacity: 0; }}
.brainc b {{ display: block; font-size: 38px; font-weight: 800; }} .brainc span {{ display: block; font-size: 28px; font-weight: 600; color: #4a5370; }}
.endc {{ background: rgba(14,26,58,0); }}
.e1, .e2, .e3 {{ position: absolute; left: 60px; right: 60px; text-align: center; color: #fff; font-weight: 800; letter-spacing: -.03em; opacity: 0; }}
.e1 {{ top: 760px; font-size: 112px; line-height: 1.02; }}
.e2 {{ top: 660px; font-size: 76px; line-height: 1.1; }}
.e3 {{ top: 900px; font-size: 76px; line-height: 1.1; }}
.sig {{ position: absolute; left: 0; right: 0; top: 1180px; text-align: center; color: {YEL}; font-size: 40px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; opacity: 0; }}
/* captions */
.cap {{ position: absolute; left: 0; right: 0; text-align: center; opacity: 0; z-index: 7; }}
.cap.seam {{ top: {SEAM - 52}px; }} .cap.low {{ top: 1380px; }}
.cap b {{ display: inline-block; padding: 12px 30px 16px; border-radius: 22px; background: {BLUE}; color: #fff; font-size: 62px; font-weight: 800; letter-spacing: -.01em;
  box-shadow: 0 14px 34px rgba(14,26,58,.35); }}
.cap .k {{ color: {YEL}; }}
.hook {{ position: absolute; left: 30px; right: 30px; top: {SEAM - 120}px; text-align: center; z-index: 7; }}
.hook b {{ display: inline-block; padding: 18px 30px 22px; border-radius: 26px; background: #fff; color: {NAVY}; font-size: 58px; font-weight: 800; line-height: 1.08;
  letter-spacing: -.02em; box-shadow: 0 18px 44px rgba(14,26,58,.4); }}
.hook em {{ font-style: normal; color: {BLUE}; }} .hook .y {{ background: {YEL}; border-radius: 12px; padding: 0 10px; }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 8; }}
#grain {{ position: absolute; inset: 0; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: overlay; z-index: 9; pointer-events: none; }}
"""


def main():
    build_top()
    build_overlays()
    build_layout()
    build_caps()
    # the hook text on the seam, from frame 0 (CSS-visible), out when she starts
    # v5 (owner: "remove it from Deepinder's full screen, add it after the transition"): on the seam from the split's
    # first frame until the price lands on "85,000"; her captions start after it
    js(f'tl.fromTo("#hook", {{opacity: 0, scale: 1.25}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(1.8)", immediateRender: false}}, {T_SPLIT:.3f});')
    js(f'tl.to("#hook", {{opacity: 0, y: -30, duration: .2, ease: "power2.in"}}, {HOOK_END - .2:.3f});')
    sfx("hit", 0.0)
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Dr Kokila: peace of mind 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="full"><div id="fullin"><video id="fullv" src="assets/video/tight.mp4" data-start="0" data-duration="{VDUR}" data-media-start="0" data-track-index="0" muted playsinline></video></div></div>
      <div id="split">
        <div id="top">{"".join(TOPH)}</div>
        <div id="bot"><div id="botin"><video id="botv" src="assets/video/tight_bot.mp4" data-start="0" data-duration="{VDUR}" data-media-start="0" data-track-index="1" muted playsinline></video></div></div>
        <i id="seamline"></i>
      </div>
      {"".join(OVER)}
      <div class="hook" id="hook" style="opacity:0"><b>Can an <span class="y">₹85,000</span> device<br>measure your <em>peace of mind?</em></b></div>
      {"".join(CAPS)}
      <div id="flash"></div>
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
    json.dump({"dur": DUR, "vdur": VDUR, "beat": None, "sections": SECTIONS, "bite": {"src": "assets/audio/deepinder_bite.wav", "at": 0.0, "len": BITE_LEN, "echo_from": ECHO_FROM}},
              open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
    print(f"wrote index.html: {len(A)} timeline lines, {len(CAPS)} captions, {len(SFX)} sfx, {DUR} s")


if __name__ == "__main__":
    main()
