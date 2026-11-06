"""Surrender ad (Kanak Kesar, The Conscious Millionaire), 9:16 talking head: writes index.html.

The owner's two references:
- The ElevenLabs reel (reference/ref_elevenlabs.mp4). Copied:
  - The pink dotted background.
  - The two-screen Before / After opening.
  - The split layout: top half a screen, bottom half the face, a black-box white caption on the seam.
  - Full-frame punch sections: small script word plus a big condensed word, red on the key word.
  - Its transitions frame by frame:
    - Into a split: the bottom face starts close (1.55x, blurred) and settles in 0.38 s.
    - Split to full: both halves zoom-blur, and the full frame lands from 1.18x.
    - Full to split: a two-frame magenta tint, then a warm flare whiting out the cut.
    - The CTA: an extreme punch-in, then a yellow line opening into the "COMMENT" box.
  - Its sound grammar (build/sfx_sheet.py).
- The Nxtlvl Social promo (reference/ref_nxtlvl_promo.mov). Copied:
  - The smoothness and pacing of its motion elements, in the top half's motion graphics: cards rise out of a blur
    with a slight 3D tilt on expo curves, staggered, and float.
  - Restyled to the pink with a liquid-glass finish.

The face never pulses: it moves only in the transitions.
Footage: assets/video/face_full.mp4 and face_split.mp4, crops of the tight cut (build/tight.py, every pause cut).
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words_tight.json")))
FW, FH, FPS = 1080, 1920, 30
DUR = 117.1                     # v2: repeats cut from the script (build/tight.py CUT_WORDS)
A, HIDE, TOP, POST, CUES = [], [], [], [], []
NID = [0]


def T(i):
    return W[i]["s"]


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


ROMAN = {
    "जब": "jab", "हम": "hum", "में": "mein", "कुछ": "kuch", "करना": "karna", "चाहते": "chahte", "हैं": "hain", "तो": "toh",
    "उसे": "use", "पाने": "paane", "के": "ke", "लिए": "liye", "बहुत": "bahut", "मेहनत": "mehnat", "करते": "karte", "वो": "woh",
    "हर": "har", "एक": "ek", "चीज": "cheez", "जिससे": "jisse", "हमें": "humein", "लगता": "lagta", "है": "hai", "कि": "ki",
    "मिल": "mil", "जाएगी": "jaayegi", "सारे": "saare", "लेते": "lete", "पे": "pe", "सारा": "saara", "लेकिन": "lekin",
    "बार-बार": "baar-baar", "करने": "karne", "हमारे": "humare", "नहीं": "nahi", "मिलते": "milte", "अंदर": "andar", "बन": "ban",
    "जाता": "jaata", "और": "aur", "हमारी": "humari", "ये": "ye", "बोलती": "bolti", "यार": "yaar", "मैंने": "maine", "सब": "sab",
    "कर": "kar", "लिया": "liya", "मेरे": "mere", "काम": "kaam", "करता": "karta", "फिर": "phir", "आपको": "aapko", "देती": "deti",
    "मुझे": "mujhe", "पता": "pata", "पहले": "pehle", "रखा": "rakha", "या": "ya", "इससे": "isse", "भी": "bhi", "खास": "khaas",
    "होने": "hone", "वाला": "waala", "यहीं": "yahin", "आपका": "aapka", "आपके": "aapke", "लेने": "lene", "लग": "lag", "से": "se",
    "सीखी": "seekhi", "अब": "ab", "का": "ka", "मतलब": "matlab", "होता": "hota", "आपने": "aapne", "हार": "haar", "मान": "maan",
    "ली": "li", "यहां": "yahan", "आप": "aap", "अपने": "apne", "को": "ko", "छोड़कर": "chhodkar", "नए": "naye", "साथ": "saath",
    "चीजों": "cheezon", "देखें": "dekhein", "क्योंकि": "kyunki", "मैं": "main", "बिल्कुल": "bilkul", "आपकी": "aapki", "था": "tha",
    "खाए": "khaaye", "किए": "kiye", "सारी": "saari", "चीजें": "cheezein", "की": "ki", "आने": "aane", "दी": "di", "थी": "thi",
    "इस": "is", "लगा": "laga", "मेरी": "meri", "बदल": "badal", "गई": "gayi", "देखता": "dekhta", "आज": "aaj", "अपनी": "apni",
    "तरह": "tarah", "करके": "karke", "सिर्फ": "sirf", "अपना": "apna", "हूं": "hoon", "जिसमें": "jismein", "हमारा": "humara",
    "रहेगा": "rahega", "करो": "karo", "उसके": "uske", "बाद": "baad", "तक": "tak", "अगर": "agar", "जानना": "jaanna", "कैसे": "kaise",
}


def word(i):
    if i == 181:
        return "Kanav"                      # the owner: his name is Kanav (Scribe heard "Kanak")
    t = re.sub(r"[,.।?!]", "", W[i]["text"]).strip()
    return ROMAN.get(t, t)


# ------------------------------------------------------------------------------------------------ layout timeline
# (kind, first word, end word); kind: intro / split / full. A section ends where the next starts.
SECTIONS = [("intro", 0, 18), ("split", 18, 80), ("full", 80, 104), ("split", 104, 135), ("full", 135, 164),
            ("split", 164, 177), ("full", 177, 214), ("split", 214, 254), ("full", 254, 278), ("split", 278, 313),
            ("full", 313, 334), ("split", 334, 367), ("split", 367, 412), ("split", 412, 440),
            ("cta", 440, None)]


def sec_times():
    out = []
    for k, (kind, a, b) in enumerate(SECTIONS):
        ta = 0.0 if a == 0 else T(a) - .04
        tb = DUR if b is None else T(b) - .04
        out.append((kind, ta, tb, a, b if b is not None else len(W)))
    return out


SECS = sec_times()
# key words (indices) shown in red in full sections and as the big word
RED = {99, 100, 137, 168, 170, 182, 213, 268, 273, 275, 318, 319, 329, 402, 456}


# ------------------------------------------------------------------------------------------------ helpers
def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {max(0, t0):.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')


ICON = {
    "target": '<circle cx="24" cy="24" r="18"/><circle cx="24" cy="24" r="11"/><circle cx="24" cy="24" r="4" fill="currentColor"/><path d="M24 24 L40 8 M34 8 h6 v6"/>',
    "book": '<path d="M8 10 q8-4 16 0 v28 q-8-4-16 0z M24 10 q8-4 16 0 v28 q-8-4-16 0z"/>',
    "layers": '<path d="M24 6 L42 15 L24 24 L6 15z M6 24 L24 33 L42 24 M6 33 L24 42 L42 33"/>',
    "play": '<rect x="5" y="10" width="38" height="28" rx="8" fill="currentColor" stroke="none"/><path d="M20 17 L31 24 L20 31z" fill="#fff" stroke="none"/>',
    "chat": '<path d="M8 10 h32 a4 4 0 0 1 4 4 v16 a4 4 0 0 1-4 4 H20 l-8 7 v-7 H8 a4 4 0 0 1-4-4 V14 a4 4 0 0 1 4-4z"/>',
    "bell": '<path d="M14 32 V22 a10 10 0 0 1 20 0 v10 l4 4 H10z M20 40 a4 4 0 0 0 8 0"/>',
    "x": '<path d="M13 13 L35 35 M35 13 L13 35"/>',
    "check": '<path d="M10 25 L20 35 L38 14"/>',
    "user": '<circle cx="24" cy="17" r="8"/><path d="M8 42 a16 14 0 0 1 32 0"/>',
    "eye": '<path d="M4 24 q20-22 40 0 q-20 22-40 0z"/><circle cx="24" cy="24" r="7"/>',
    "spark": '<path d="M24 4 C26 18 30 22 44 24 C30 26 26 30 24 44 C22 30 18 26 4 24 C18 22 22 18 24 4z" fill="currentColor" stroke="none"/>',
    "clock": '<circle cx="24" cy="24" r="18"/><path d="M24 13 V24 L32 29"/>',
    "brief": '<rect x="6" y="15" width="36" height="25" rx="5"/><path d="M17 15 V10 h14 v5 M6 26 h36"/>',
    "arrowup": '<path d="M10 36 L22 24 L28 30 L40 14 M31 14 h9 v9"/>',
    "brain": '<path d="M18 8 a7 7 0 0 0-7 7 a7 7 0 0 0-4 12 a7 7 0 0 0 7 11 h4z M30 8 a7 7 0 0 1 7 7 a7 7 0 0 1 4 12 a7 7 0 0 1-7 11 h-4z M24 8 v30"/>',
}


def icon(name, size=56, color="#ff2d55", stroke=3.4):
    return (f'<svg class="ic" viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="{stroke}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="color:{color}">{ICON[name]}</svg>')


def el(html, x, y, t0, t1, w=None, cls="glass", z=3, style="", rise=90, tilt=18, d=.5):
    """A motion element in the top stage: rises out of a blur with a slight 3D tilt (the promo's entrance), floats,
    leaves blurred upward."""
    i = nid("g")
    ws = f"width:{w}px;" if w else ""
    TOP.append(f'<div class="mg {cls}" id="{i}" style="left:{x}px;top:{y}px;{ws}z-index:{z};{style}">{html}</div>')
    HIDE.append(f"#{i}")
    js(f'tl.fromTo("#{i}", {{opacity: 0, y: {rise}, scale: .86, rotationX: {tilt}, filter: "blur(16px)"}}, '
       f'{{opacity: 1, y: 0, scale: 1, rotationX: 0, filter: "blur(0px)", duration: {d}, ease: "expo.out", immediateRender: false}}, {t0:.3f});')
    if "ic" in html and rise:                # v2: every card's icon pops in a beat after the card
        js(f'tl.fromTo("#{i} .ic", {{scale: 0, rotation: -35}}, {{scale: 1, rotation: 0, duration: .35, ease: "back.out(3)", immediateRender: false}}, {t0 + .12:.3f});')
    n = int((t1 - t0 - d) / 1.1)
    if n > 0:
        js(f'tl.to("#{i}", {{y: -9, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: {n - 1 if n % 2 == 0 else n}}}, {t0 + d:.3f});')
    js(f'tl.to("#{i}", {{opacity: 0, y: -60, scale: .94, filter: "blur(12px)", duration: .22, ease: "power2.in"}}, {t1 - .22:.3f});')
    CUES.append((t0, "pop"))
    return i


def counter(i, t0, d, to, sel=None):
    js(f'tl.fromTo("#{i} {sel or ".num"}", {{innerText: 0}}, {{innerText: {to}, snap: {{innerText: 1}}, duration: {d}, ease: "power3.out", immediateRender: false}}, {t0:.3f});')


# ------------------------------------------------------------------------------------------------ the top-half graphics
def graphics():
    s1 = SECS[1][2]
    # S1: achieve -> hard work -> try everything; then courses / programs / YouTube
    e1 = T(61) - .05
    el(f'<div class="row">{icon("target", 74)}<div><div class="h1">ACHIEVE</div><div class="sub">something big in life</div></div></div>',
       110, 150, T(24), e1, w=620)
    i = el('<div class="lbl">Hard work</div><div class="bar"><i></i></div><div class="pct"><span class="num">0</span>%</div>',
           400, 430, T(35), e1, w=560)
    js(f'tl.fromTo("#{i} .bar i", {{scaleX: 0}}, {{scaleX: .92, duration: 1.4, ease: "power3.out", immediateRender: false}}, {T(35) + .2:.3f});')
    counter(i, T(35) + .2, 1.4, 92)
    for k, (wi, txt) in enumerate([(43, "Try everything"), (46, "Every method"), (54, "Hope it works")]):
        el(f'{icon("check", 40, "#18b26b")}<span>{txt}</span>', 150 + 30 * k, 640 + 96 * k, T(wi), e1, cls="glass chip", rise=40)
    for k, (wi, ic, h, sub) in enumerate([(64, "book", "Courses", "bought"), (69, "layers", "Programs", "joined"),
                                          (72, "play", "YouTube", "content consumed")]):
        el(f'{icon(ic, 70, "#ff2d55")}<div class="h2">{h}</div><div class="sub">{sub}</div>', 110 + 300 * k, 230 + 70 * (k % 2),
           T(wi), SECS[1][2], w=280, cls="glass tall", style=f"transform:rotate({(-4, 2, 5)[k]}deg)")
    # S2: inner voice -> new opportunity
    s2a, s2b = SECS[3][1], SECS[3][2]
    e2 = T(131) - .05
    el(f'<div class="row">{icon("brain", 52, "#7a1238")}<div class="h3">Inner voice</div><div class="typing"><b></b><b></b><b></b></div></div>',
       110, 120, T(106), e2, w=860, cls="glass hdr")
    el('<div class="bub">"Yaar, maine sab kuch try kar liya..."</div>', 110, 300, T(112), e2, w=760, cls="glass bubble")
    i = el(f'<div class="bub">"...lekin mere liye kuch kaam nahi karta."</div><div class="xb">{icon("x", 46, "#fff", 5)}</div>',
           200, 500, T(119), e2, w=780, cls="glass bubble")
    js(f'tl.fromTo("#{i} .xb", {{scale: 0, rotation: -60}}, {{scale: 1, rotation: 0, duration: .45, ease: "back.out(2.4)", immediateRender: false}}, {T(124):.3f});')
    i = el(f'<div class="row">{icon("bell", 64, "#ff2d55")}<div><div class="h3">New opportunity</div><div class="sub">Life is knocking. Open it?</div></div></div>'
           f'<div class="btns"><span class="b1">Open</span><span class="b2">Ignore</span></div>', 120, 260, T(131), s2b, w=840, cls="glass notif")
    CUES.append((T(131), "notify"))
    # S3: past -> future
    s3b = SECS[5][2]
    el('<div class="pill">PAST</div>', 100, 330, T(168), s3b, cls="glass pillc dark")
    i = el('<svg class="arr" viewBox="0 0 300 60" width="300" height="60"><path d="M10 30 H270 M246 10 L272 30 L246 50" fill="none" stroke="#ff2d55" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>',
           390, 360, T(169), s3b, cls="bare")
    js(f'tl.to("#{i} path", {{strokeDashoffset: 0, duration: .55, ease: "power3.inOut"}}, {T(169) + .1:.3f});')
    el('<div class="pill">FUTURE</div>', 660, 330, T(170), s3b, cls="glass pillc")
    el(f'<div class="row">{icon("brief", 56, "#7a1238")}<div class="h3">Your past is making<br>your future decisions</div></div>', 170, 560, T(172), s3b, w=740)
    # S4: surrender != giving up -> let go of the past -> new perspective
    s4b = SECS[7][2]
    e4 = T(227) - .05
    el('<div class="big">SURRENDER</div>', 170, 170, T(215), e4, w=740, cls="glass center")
    i = el('<div class="big sm">Giving up</div><i class="strike"></i>', 270, 470, T(220), e4, w=540, cls="glass center")
    js(f'tl.fromTo("#{i} .strike", {{scaleX: 0}}, {{scaleX: 1, duration: .4, ease: "power3.out", immediateRender: false}}, {T(224):.3f});')
    el('<div class="neq">&ne;</div>', 470, 360, T(220), e4, cls="bare", rise=30)
    lg = T(245)
    for k, (wi, txt) in enumerate([(237, "Past negative<br>experiences"), (242, "Preconceived<br>judgments")]):
        j = el(f'{icon("x", 44, "#ff2d55")}<div class="h3">{txt}</div>', 90 + 470 * k, 200 + 60 * k, T(wi), lg + .6, w=430, cls="glass tall2")
        js(f'tl.to("#{j}", {{x: {(-220, 220)[k]}, y: -260, rotation: {(-14, 14)[k]}, duration: .9, ease: "power2.in"}}, {lg:.3f});')
    CUES.append((lg, "swish"))
    i = el(f'<div class="lens">{icon("eye", 120, "#ff2d55", 3)}<div class="spk">{icon("spark", 54, "#fff")}</div></div><div class="h3 c">New perspective</div>',
           330, 200, T(248), s4b, w=420, cls="glass round")
    js(f'tl.fromTo("#{i} .spk", {{scale: 0, rotation: -90}}, {{scale: 1, rotation: 0, duration: .6, ease: "back.out(2)", immediateRender: false}}, {T(248) + .3:.3f});')
    # S5: courses / YouTube / everything -> QUIT -> the teaching
    s5b = SECS[9][2]
    q = T(301)
    cards = []
    for k, (wi, ic, h) in enumerate([(292, "book", "Courses"), (295, "play", "YouTube content"), (299, "layers", "Everything else")]):
        cards.append(el(f'{icon(ic, 60, "#ff2d55")}<div class="h2">{h}</div>', 130 + 270 * k, 160 + 40 * k, T(wi), q + 1.1, w=300,
                        cls="glass tall", style=f"transform:rotate({(-6, 3, 7)[k]}deg)"))
    for k, c in enumerate(cards):
        js(f'tl.to("#{c}", {{y: 900, rotation: {(-30, 20, 40)[k]}, duration: .8, ease: "power3.in"}}, {q + .25 + .06 * k:.3f});')
    i = el('<div class="stamp">QUIT</div>', 300, 330, q, T(305), cls="bare", rise=0, tilt=0, d=.3)
    js(f'tl.fromTo("#{i} .stamp", {{scale: 2.2}}, {{scale: 1, duration: .32, ease: "back.out(2)", immediateRender: false}}, {q:.3f});')
    CUES.append((q, "stamp"))
    i = el(f'<div class="glow"></div>{icon("spark", 80, "#ff2d55")}<div class="h1">The teaching</div><div class="sub">that changed everything</div>',
           190, 230, T(309), s5b, w=700, cls="glass center")
    # S6: 25 crore in 25 months, selling skill
    s6b = SECS[11][2]
    i = el('<div class="money">&#8377;<span class="num">0</span><span class="unit">CRORE</span></div><div class="sub c">generated</div>',
           170, 110, T(339), s6b, w=740, cls="glass center")
    counter(i, T(339) + .1, 1.6, 25)
    CUES.append((T(339) + .1, "cash"))
    el(f'{icon("clock", 46, "#7a1238")}<span>in 25 months</span>', 330, 470, T(348), s6b, cls="glass chip", rise=40)
    for k, (wi, txt) in enumerate([(355, "Skill"), (358, "Expertise"), (360, "Courses"), (362, "Services")]):
        el(f'<span>{txt}</span>', (150, 560, 150, 560)[k] + (0, 0, 40, 40)[k], (620, 620, 740, 740)[k], T(wi), s6b, cls="glass chip sm", rise=40)
    i = el(f'{icon("check", 40, "#fff", 5)}<span>Sold</span>', 420, 860, T(365), s6b, cls="glass chip sold", rise=40)
    # S7: 100 serious people -> live done-with-you system
    s7b = SECS[12][2]
    e7 = T(383) - .05
    dots = "".join('<i></i>' for _ in range(100))
    i = el(f'<div class="hund"><span class="num">0</span></div><div class="grid">{dots}</div><div class="sub">serious people only</div>',
           70, 120, T(373), e7, w=520, cls="glass")
    counter(i, T(373) + .1, 1.0, 100)
    js(f'tl.fromTo("#{i} .grid i", {{opacity: .15, scale: .5}}, {{opacity: 1, scale: 1, duration: .25, stagger: .008, ease: "power2.out", immediateRender: false}}, {T(373) + .1:.3f});')
    for k, (wi, txt) in enumerate([(375, "Coaches"), (376, "Consultants"), (377, "Experts"), (379, "Service providers")]):
        el(f'{icon("user", 40, "#ff2d55")}<span>{txt}</span>', 600, 150 + 120 * k, T(wi), e7, cls="glass chip", rise=40)
    i = el('<div class="row"><i class="live"></i><div class="h3">LIVE</div></div><div class="h2">Done-with-you system</div>'
           '<div class="sub">We implement it together</div>', 190, 200, T(383), SECS[12][2], w=700, cls="glass center")
    js(f'tl.to("#{i} .live", {{opacity: .25, duration: .5, yoyo: true, repeat: {int((s7b - T(383)) / .5)}, ease: "sine.inOut"}}, {T(383):.3f});')
    # S8: goal -> 3 high-paying clients -> 10 lakh a month
    s8b = SECS[13][2]
    e8 = T(429) - .05
    el('<div class="h3 c">THE GOAL</div>', 390, 90, T(415), s8b, cls="glass chip", rise=30)
    av = []
    for k in range(3):
        av.append(el(f'{icon("user", 70, "#7a1238")}<div class="sub c">Client {k + 1}</div><div class="ok">{icon("check", 34, "#fff", 5)}</div>',
                     130 + 300 * k, 230, T(421) + .12 * k, e8, w=220, cls="glass av"))
    for k, a in enumerate(av):
        js(f'tl.fromTo("#{a} .ok", {{scale: 0}}, {{scale: 1, duration: .4, ease: "back.out(2.5)", immediateRender: false}}, {T(425) + .1 * k:.3f});')
    el('<div class="h3 c">high-paying</div>', 360, 560, T(422), e8, cls="glass chip", rise=30)
    i = el('<svg class="chart" viewBox="0 0 700 260" width="700" height="260"><path class="ln" d="M20 240 C150 230 220 200 300 170 S470 90 680 20" '
           'fill="none" stroke="#ff2d55" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>'
           '<div class="money sm">&#8377;<span class="num">0</span><span class="unit">LAKH / month</span></div>', 190, 220, T(431), s8b, w=760, cls="glass")
    js(f'tl.to("#{i} .ln", {{strokeDashoffset: 0, duration: 1.2, ease: "power3.inOut"}}, {T(431) + .1:.3f});')
    counter(i, T(431) + .1, 1.3, 10)
    CUES.append((T(431) + .1, "cash"))
    el(f'{icon("arrowup", 44, "#18b26b")}<span>Scale</span>', 420, 760, T(438), s8b, cls="glass chip", rise=40)


# ------------------------------------------------------------------------------------------------ captions
FUNC = {"ki", "ke", "ka", "ko", "se", "pe", "hai", "hain", "toh", "aur", "ek", "ye", "woh", "mein", "the", "of", "to", "a", "and", "is", "an", "your", "you", "i", "am", "or", "ya", "bhi"}


def chunks(a, b, maxw=3, maxc=16):
    """Phrases of up to maxw words; a chunk never ends on a short function word unless a sentence ends there (it rides
    into the next chunk instead), so the big word is always a meaningful one."""
    out, cur = [], []
    for i in range(a, b):
        if W[i].get("cut"):
            continue
        cur.append(i)
        txt = " ".join(word(j) for j in cur)
        end = W[i]["text"][-1] in ",.।?"
        if (len(cur) >= maxw or len(txt) >= maxc or end) and (end or word(i).lower() not in FUNC or len(cur) >= maxw + 2):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def seam_caps(a, b, tend):
    """Split sections: one to three words in a black box with white type, on the seam (the reference's labels)."""
    ch = chunks(a, b)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        i = nid("sc")
        POST.append(f'<div class="seam" id="{i}"><span>{" ".join(word(j) for j in c)}</span></div>')
        show(f"#{i}", t0, t1)
        js(f'tl.fromTo("#{i} span", {{scale: 1.12}}, {{scale: 1, duration: .16, ease: "power3.out", immediateRender: false}}, {t0:.3f});')


def full_caps(a, b, tend):
    """Full sections: a small script word over a big condensed word (red on key words), lower third."""
    ch = chunks(a, b, maxw=4, maxc=22)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        key = [j for j in c if j in RED]
        big = key if key else c[-1:] if len(word(c[-1])) > 2 or len(c) == 1 else c[-2:]
        small = [j for j in c if j not in big]
        red = bool(key)
        i = nid("fc")
        sm = " ".join(word(j) for j in small).lower()
        bg = " ".join(word(j) for j in big).upper()
        POST.append(f'<div class="fcap" id="{i}">' + (f'<div class="scr">{sm}</div>' if sm else "") +
                    f'<div class="bigw{" red" if red else ""}">{bg}</div></div>')
        show(f"#{i}", t0, t1)
        if sm:
            js(f'tl.fromTo("#{i} .scr", {{opacity: 0, x: -20, filter: "blur(6px)"}}, {{opacity: 1, x: 0, filter: "blur(0px)", duration: .18, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
        tb = T(big[0]) - .02
        js(f'tl.set("#{i} .bigw", {{opacity: 0}}, {t0 - .001:.3f});')
        js(f'tl.fromTo("#{i} .bigw", {{opacity: 0, scale: 1.3, filter: "blur(10px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "expo.out", immediateRender: false}}, {max(t0, tb):.3f});')
        if red:
            CUES.append((max(t0, tb), "hit"))


def intro_caps(a, b, tend):
    """Inside the After screen: a small white line over a bigger script line."""
    ch = chunks(a, b, maxw=3, maxc=18)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        i = nid("ic")
        small, big = c[:-1] if len(c) > 1 else [], c[-1:] if len(c) > 1 else c
        POST.append(f'<div class="icap" id="{i}"><div class="s1">{" ".join(word(j) for j in small)}</div>'
                    f'<div class="s2">{" ".join(word(j) for j in big)}</div></div>')
        show(f"#{i}", t0, t1)
        js(f'tl.fromTo("#{i} .s2", {{opacity: 0, y: 14, filter: "blur(8px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: .2, ease: "power3.out", immediateRender: false}}, {t0 + .05:.3f});')


# ------------------------------------------------------------------------------------------------ layout + transitions
def layout():
    for k, (kind, ta, tb, a, b) in enumerate(SECS):
        prev = SECS[k - 1][0] if k else None
        if kind == "intro":
            show("#intro", 0, tb)
            js(f'tl.fromTo("#cards", {{scale: 1}}, {{scale: .985, duration: {tb - .3:.2f}, ease: "none"}}, 0);')
            js(f'tl.to("#cards", {{scale: .9, x: -40, y: -40, filter: "blur(6px)", duration: .28, ease: "power2.in"}}, {tb - .28:.3f});')
            intro_caps(a, b, tb)
            continue
        if kind == "split":
            js(f'tl.set("#split", {{opacity: 1, scale: 1, filter: "blur(0px)"}}, {ta:.3f});')
            js(f'tl.fromTo("#stage", {{scale: 1.06, y: 34}}, {{scale: 1.13, y: 22, duration: {tb - ta:.2f}, ease: "none", immediateRender: false}}, {ta:.3f});')
            js(f'tl.set("#split", {{opacity: 0}}, {tb:.3f});')
            if prev in ("intro", "full"):
                # the reference: the face lands close and blurred and settles; the screen sharpens in
                js(f'tl.fromTo("#botin", {{scale: 1.55, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                js(f'tl.fromTo("#topin", {{scale: 1.14, filter: "blur(14px)"}}, {{scale: 1, filter: "blur(0px)", duration: .42, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                CUES.extend([(ta - .06, "whoosh_big"), (ta, "boom")])
            else:                                   # split to split: a quick push on both halves
                js(f'tl.fromTo("#botin", {{scale: 1.25, filter: "blur(6px)"}}, {{scale: 1, filter: "blur(0px)", duration: .3, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                js(f'tl.fromTo("#topin", {{x: 140, filter: "blur(12px)"}}, {{x: 0, filter: "blur(0px)", duration: .4, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                CUES.append((ta - .05, "whoosh"))
            seam_caps(a, b, tb)
            nxt = SECS[k + 1][0] if k + 1 < len(SECS) else None
            if nxt in ("full", "cta"):              # zoom-blur out of the split
                js(f'tl.to("#split", {{scale: 1.22, filter: "blur(16px)", duration: .2, ease: "power2.in"}}, {tb - .2:.3f});')
            continue
        # full / cta
        js(f'tl.set("#full", {{opacity: 1}}, {ta:.3f});')
        if tb < DUR:
            js(f'tl.set("#full", {{opacity: 0}}, {tb:.3f});')
        s0 = 1.8 if kind == "cta" else 1.18
        js(f'tl.fromTo("#fullin", {{scale: {s0}, filter: "blur(12px)"}}, {{scale: 1, filter: "blur(0px)", duration: {.45 if kind == "cta" else .3}, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
        CUES.append((ta - .12, "whoosh"))
        if kind == "cta":
            cta(ta, a)
            continue
        full_caps(a, b, tb)
        if a <= 181 < b:
            namecard(T(181) - .05, T(202) - .1)
        nxt = SECS[k + 1][0] if k + 1 < len(SECS) else None
        if nxt == "split":                          # the reference's colour flash into the next split
            js(f'tl.set("#tint", {{opacity: .55}}, {tb - .3:.3f});')
            js(f'tl.set("#tint", {{opacity: 0}}, {tb - .23:.3f});')
            js(f'tl.fromTo("#leak", {{opacity: 0, x: -500}}, {{opacity: 1, x: 0, duration: .22, ease: "power2.in", immediateRender: false}}, {tb - .2:.3f});')
            js(f'tl.to("#leak", {{opacity: 0, x: 400, duration: .28, ease: "power2.out"}}, {tb + .02:.3f});')
            js(f'tl.fromTo("#flash", {{opacity: 0}}, {{opacity: .85, duration: .06, immediateRender: false}}, {tb - .05:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: .25, ease: "power2.out"}}, {tb + .02:.3f});')
            CUES.append((tb - .3, "shimmer"))
    HIDE.extend(["#split", "#full", "#tint", "#leak", "#flash"])


def namecard(t0, t1):
    """A liquid-glass name card at the top of the frame while he introduces himself, and the teacher's name under it."""
    POST.append('<div id="name" class="glass"><div class="nm">Kanav Kesar</div><div class="nr">Founder &middot; The Conscious Millionaire</div>'
                '<div id="jk">Learned from J. Krishnamurti</div></div>')
    HIDE.extend(["#name", "#jk"])         # under the captions: his head fills the top of the full frame
    js(f'tl.fromTo("#name", {{opacity: 0, y: -60, filter: "blur(14px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: .5, ease: "expo.out", immediateRender: false}}, {t0:.3f});')
    js(f'tl.to("#name", {{opacity: 0, y: -40, filter: "blur(10px)", duration: .22, ease: "power2.in"}}, {t1 - .22:.3f});')
    tj = T(197) - .05
    js(f'tl.fromTo("#jk", {{opacity: 0, y: 16, filter: "blur(10px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: .4, ease: "expo.out", immediateRender: false}}, {tj:.3f});')
    CUES.extend([(t0, "pop"), (tj, "pop")])


def cta(ta, a):
    """The reference's CTA: a yellow line draws up and opens into the box; COMMENT, then "SURRENDER" slams;
    a line of yellow type underneath."""
    tc = T(455) - .1
    POST.append('<div id="ctabox"><i class="cl"></i><div class="cb"><div class="c1">COMMENT</div><div class="c2">"SURRENDER"</div></div></div>'
                '<div id="ctadm">DETAILS IN YOUR DM</div>')
    HIDE.extend(["#ctabox", "#ctadm"])
    js(f'tl.set("#ctabox", {{opacity: 1}}, {tc:.3f});')
    js(f'tl.fromTo("#ctabox .cl", {{scaleY: 0}}, {{scaleY: 1, duration: .14, ease: "power3.out", immediateRender: false}}, {tc:.3f});')
    js(f'tl.fromTo("#ctabox .cb", {{scaleX: .04}}, {{scaleX: 1, duration: .24, ease: "back.out(1.6)", immediateRender: false}}, {tc + .14:.3f});')
    js(f'tl.set("#ctabox .cl", {{opacity: 0}}, {tc + .2:.3f});')
    js(f'tl.fromTo("#ctabox .c2", {{scale: 1.7, opacity: 0}}, {{scale: 1, opacity: 1, duration: .26, ease: "back.out(2)", immediateRender: false}}, {T(456) - .02:.3f});')
    td = T(464) - .05
    js(f'tl.fromTo("#ctadm", {{opacity: 0, clipPath: "inset(0 100% 0 0)"}}, {{opacity: 1, clipPath: "inset(0 0% 0 0)", duration: .35, ease: "power3.out", immediateRender: false}}, {td:.3f});')
    CUES.extend([(tc, "riser_hit"), (T(456) - .02, "stamp"), (td, "swish")])
    # the words before the box as full captions
    full_caps(a, 454, tc)


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/Inter-700.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Kaushan"; src: url("assets/fonts/KaushanScript.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #f7b7c3; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter"; color: #3b0a1f; }}
#bg {{ position: absolute; inset: 0; background: radial-gradient(120% 75% at 50% 8%, #fff4f6 0%, #ffd6de 42%, #f7a2b4 100%); }}
#bg::after {{ content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(190,40,80,.17) 1.7px, transparent 2.1px);
  background-size: 26px 26px; -webkit-mask-image: linear-gradient(#000 20%, rgba(0,0,0,.35)); mask-image: linear-gradient(#000 20%, rgba(0,0,0,.35)); }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(90px); opacity: .3; }}
#intro {{ position: absolute; inset: 0; opacity: 0; }}
#cards {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.card {{ position: absolute; border-radius: 34px; overflow: hidden; box-shadow: 0 30px 60px rgba(120,20,50,.28), 0 0 0 1px rgba(255,255,255,.6); }}
.card video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#cbefore {{ left: 50px; top: 760px; width: 380px; height: 676px; }}
#cbefore video {{ filter: saturate(.45) contrast(.9) brightness(1.06); }}
#cafter {{ left: 460px; top: 500px; width: 570px; height: 1013px; }}
.tag {{ position: absolute; font: 800 54px/1 "Inter"; color: #1a0610; letter-spacing: -.01em; }}
#tbefore {{ left: 140px; top: 680px; font-size: 62px; }}
#tafter {{ left: 610px; top: 385px; font-size: 104px; }}
.icap {{ position: absolute; left: 480px; width: 530px; top: 1290px; text-align: center; opacity: 0; color: #fff; text-shadow: 0 3px 12px rgba(0,0,0,.45); }}
.icap .s1 {{ font: 700 42px/1.1 "Inter"; }}
.icap .s2 {{ font: 400 84px/1.05 "Kaushan"; color: #ffd0dc; }}
#split {{ position: absolute; inset: 0; opacity: 0; transform-origin: 50% 50%; }}
#top {{ position: absolute; left: 0; top: 0; width: {FW}px; height: 960px; overflow: hidden; }}
#topin {{ position: absolute; inset: 0; perspective: 1400px; transform-origin: 50% 50%; }}
#stage {{ position: absolute; left: 0; top: 0; width: 1080px; height: 960px; transform-origin: 50% 40%; }}
#bot {{ position: absolute; left: 0; top: 960px; width: {FW}px; height: 960px; overflow: hidden; background: #2a0d14; }}
#botin {{ position: absolute; inset: 0; transform-origin: 50% 35%; }}
#botin video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#seamline {{ position: absolute; left: 0; top: 957px; width: {FW}px; height: 6px; background: linear-gradient(90deg, #ff2d55, #ff7aa0, #ff2d55); z-index: 6; }}
#full {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; background: #2a0d14; }}
#fullin {{ position: absolute; inset: 0; transform-origin: 50% 30%; }}
#fullin video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.mg {{ position: absolute; opacity: 0; transform-origin: 50% 80%; }}
.glass {{ border-radius: 36px; padding: 30px 36px; overflow: hidden;
  background: linear-gradient(140deg, rgba(255,255,255,.62), rgba(255,255,255,.2) 55%, rgba(255,255,255,.34));
  border: 1.5px solid rgba(255,255,255,.8);
  box-shadow: inset 0 2px 0 rgba(255,255,255,.95), inset 0 -16px 40px rgba(255,80,130,.16), 0 30px 70px rgba(150,20,60,.24), 0 6px 18px rgba(150,20,60,.14);
  backdrop-filter: blur(22px) saturate(1.7); -webkit-backdrop-filter: blur(22px) saturate(1.7); }}
.glass::before {{ content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  background: linear-gradient(115deg, rgba(255,255,255,.75) 0%, rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.25) 100%); }}
.glass.dark {{ background: linear-gradient(140deg, rgba(90,10,40,.85), rgba(60,5,25,.7)); color: #fff; border-color: rgba(255,160,190,.5); }}
.bare {{ background: none; border: 0; }}
.row {{ display: flex; align-items: center; gap: 26px; position: relative; }}
.h1 {{ font: 800 76px/1 "Inter"; letter-spacing: -.03em; }}
.h2 {{ font: 800 44px/1.05 "Inter"; letter-spacing: -.02em; margin-top: 16px; }}
.h3 {{ font: 800 42px/1.12 "Inter"; letter-spacing: -.02em; }}
.c {{ text-align: center; }}
.sub {{ font: 500 30px/1.25 "Inter"; color: #7a3a52; margin-top: 8px; }}
.lbl {{ font: 700 32px/1 "Inter"; margin-bottom: 18px; }}
.bar {{ height: 26px; border-radius: 13px; background: rgba(255,255,255,.55); overflow: hidden; box-shadow: inset 0 2px 6px rgba(120,20,50,.15); }}
.bar i {{ display: block; height: 100%; background: linear-gradient(90deg, #ff5a86, #ff2d55); transform-origin: 0 50%; border-radius: 13px; }}
.pct {{ position: absolute; right: 36px; top: 26px; font: 800 36px/1 "Inter"; color: #ff2d55; }}
.chip {{ display: flex; align-items: center; gap: 16px; padding: 18px 32px; border-radius: 999px; font: 700 38px/1 "Inter"; }}
.chip.sm {{ font-size: 34px; padding: 18px 28px; }}
.chip.sold {{ background: linear-gradient(140deg, #ff4f7b, #ff2d55); color: #fff; border-color: rgba(255,255,255,.7); }}
.tall {{ height: 340px; display: flex; flex-direction: column; justify-content: flex-end; }}
.tall2 {{ min-height: 230px; display: flex; flex-direction: column; justify-content: space-between; }}
.hdr .typing {{ margin-left: auto; display: flex; gap: 10px; }}
.typing b {{ width: 16px; height: 16px; border-radius: 50%; background: #c46a8a; display: block; }}
.bubble .bub {{ font: 700 44px/1.2 "Inter"; color: #3b0a1f; }}
.xb {{ position: absolute; right: 22px; top: -4px; width: 74px; height: 74px; border-radius: 50%; background: #ff2d55; display: grid; place-items: center;
  box-shadow: 0 10px 24px rgba(255,45,85,.45); }}
.btns {{ display: flex; gap: 20px; margin-top: 26px; }}
.btns span {{ flex: 1; text-align: center; padding: 20px; border-radius: 22px; font: 800 34px/1 "Inter"; }}
.b1 {{ background: #ff2d55; color: #fff; }}
.b2 {{ background: rgba(255,255,255,.6); color: #7a3a52; }}
.pillc {{ border-radius: 999px; padding: 26px 46px; }}
.pill {{ font: 800 58px/1 "Inter"; letter-spacing: .02em; }}
.big {{ font: 800 96px/1 "Inter"; letter-spacing: -.03em; text-align: center; }}
.big.sm {{ font-size: 76px; color: #7a3a52; }}
.center {{ text-align: center; }}
.strike {{ position: absolute; left: 30px; right: 30px; top: 50%; height: 12px; margin-top: -6px; background: #ff2d55; border-radius: 6px; transform-origin: 0 50%; }}
.neq {{ font: 800 120px/1 "Inter"; color: #ff2d55; }}
.round {{ border-radius: 50%; width: 420px; height: 420px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.lens {{ position: relative; }}
.spk {{ position: absolute; right: -14px; top: -10px; width: 64px; height: 64px; border-radius: 50%; background: #ff2d55; display: grid; place-items: center; }}
.stamp {{ font: 400 230px/1 "Anton"; color: #ff2d55; border: 14px solid #ff2d55; padding: 6px 40px; border-radius: 24px; transform: rotate(-8deg);
  background: rgba(255,255,255,.35); text-shadow: 0 6px 0 rgba(120,0,30,.2); }}
.glow {{ position: absolute; left: 50%; top: 40%; width: 420px; height: 420px; margin: -210px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,90,140,.55), rgba(255,90,140,0) 70%); }}
.money {{ font: 800 150px/1 "Inter"; letter-spacing: -.04em; color: #ff2d55; display: flex; align-items: baseline; justify-content: center; gap: 10px; }}
.money .unit {{ font-size: 58px; color: #3b0a1f; letter-spacing: 0; margin-left: 14px; }}
.money.sm {{ font-size: 110px; justify-content: flex-start; margin-top: -40px; }}
.money.sm .unit {{ font-size: 44px; }}
.hund {{ font: 800 120px/1 "Inter"; color: #ff2d55; letter-spacing: -.04em; }}
.grid {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 10px; margin: 18px 0 6px; }}
.grid i {{ display: block; height: 30px; border-radius: 50%; background: #ff2d55; }}
.live {{ width: 26px; height: 26px; border-radius: 50%; background: #ff2d55; box-shadow: 0 0 0 8px rgba(255,45,85,.2); display: block; }}
.av {{ display: flex; flex-direction: column; align-items: center; padding: 34px 20px; }}
.ok {{ position: absolute; right: 16px; top: 16px; width: 54px; height: 54px; border-radius: 50%; background: #18b26b; display: grid; place-items: center; }}
.seam {{ position: absolute; left: 0; width: {FW}px; top: 905px; text-align: center; opacity: 0; z-index: 9; }}
.seam span {{ display: inline-block; background: #000; color: #fff; font: 800 50px/1 "Inter"; padding: 12px 24px 14px; border-radius: 8px; letter-spacing: -.01em; }}
.fcap {{ position: absolute; left: 110px; right: 80px; top: 1250px; opacity: 0; z-index: 9; }}
.fcap .scr {{ font: 400 74px/1.1 "Kaushan"; color: #fff; text-shadow: 0 4px 14px rgba(0,0,0,.55); margin-left: 6px; }}
.fcap .bigw {{ font: 400 150px/1 "Anton"; color: #fff; letter-spacing: .01em; text-shadow: 0 8px 26px rgba(0,0,0,.45); transform-origin: 0 60%; }}
.fcap .bigw.red {{ color: #ff2d3d; text-shadow: 0 4px 0 #fff, 0 10px 30px rgba(0,0,0,.45); }}
#name {{ position: absolute; left: 110px; top: 1470px; width: 860px; opacity: 0; z-index: 9; text-align: center; padding: 26px 34px 24px;
  background: linear-gradient(140deg, rgba(255,255,255,.9), rgba(255,240,244,.72)); }}
#name .nm {{ font: 800 74px/1 "Inter"; letter-spacing: -.03em; color: #3b0a1f; }}
#name .nr {{ font: 700 32px/1.2 "Inter"; color: #ff2d55; margin-top: 10px; }}
#jk {{ font: 600 28px/1.2 "Inter"; color: #7a3a52; margin-top: 8px; opacity: 0; }}
#ctabox {{ position: absolute; left: 150px; top: 760px; width: 780px; opacity: 0; transform: rotate(-6deg); z-index: 9; }}
#ctabox .cl {{ position: absolute; left: 50%; top: -10px; width: 12px; height: 300px; margin-left: -6px; background: #e8ff2a; transform-origin: 50% 100%; }}
#ctabox .cb {{ background: #e8ff2a; padding: 22px 30px 26px; text-align: center; box-shadow: 0 16px 40px rgba(0,0,0,.4); }}
#ctabox .c1 {{ font: 400 120px/1 "Anton"; color: #111; }}
#ctabox .c2 {{ font: 400 138px/1 "Anton"; color: #111; margin-top: 6px; }}
#ctadm {{ position: absolute; left: 0; width: {FW}px; top: 1180px; text-align: center; font: 400 96px/1 "Anton"; color: #e8ff2a; opacity: 0; z-index: 9;
  text-shadow: 0 6px 20px rgba(0,0,0,.6); }}
#tint {{ position: absolute; inset: 0; z-index: 20; opacity: 0; background: #d23cff; mix-blend-mode: screen; }}
#leak {{ position: absolute; left: -400px; top: -200px; width: 1900px; height: 2400px; z-index: 21; opacity: 0; mix-blend-mode: screen;
  background: radial-gradient(ellipse 40% 50% at 50% 50%, rgba(255,240,200,1), rgba(255,170,60,.85) 35%, rgba(255,120,40,0) 70%); }}
#flash {{ position: absolute; inset: 0; z-index: 22; opacity: 0; background: #fff8f0; }}
#grain {{ position: absolute; inset: 0; z-index: 23; pointer-events: none; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
"""


def main():
    graphics()
    layout()
    i_end = SECS[0][2]
    blobs = "".join(f'<i class="blob" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>'
                    for x, y, s, c in [(-120, 80, 520, "#ff6f95"), (620, 360, 560, "#ffffff"), (300, 620, 460, "#ff3d6e"), (760, -80, 420, "#ffb2c4")])
    for k, (x, y) in enumerate([(160, 260), (-140, -120), (120, -200), (-180, 180)]):
        js(f'tl.to(".blob:nth-child({k + 1})", {{x: {x}, y: {y}, duration: {DUR:.1f}, ease: "sine.inOut"}}, 0);')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Surrender ad 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="bg"></div>
      <div id="split">
        <div id="top"><div id="topin"><div id="blobs">{blobs}</div><div id="stage">{"".join(TOP)}</div></div></div>
        <div id="bot"><div id="botin"><video id="vsplit" class="clip" src="assets/video/face_split.mp4" data-start="0" data-duration="{DUR}" data-track-index="2" muted playsinline></video></div></div>
        <div id="seamline"></div>
      </div>
      <div id="full"><div id="fullin"><video id="vfull" class="clip" src="assets/video/face_full.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" muted playsinline></video></div></div>
      <div id="intro"><div id="cards">
        <div class="tag" id="tbefore">Before</div><div class="tag" id="tafter">After</div>
        <div class="card" id="cbefore"><video id="vbefore" class="clip" src="assets/video/face_full.mp4" data-start="0" data-duration="{i_end:.3f}" data-track-index="3" muted playsinline></video></div>
        <div class="card" id="cafter"><video id="vafter" class="clip" src="assets/video/face_full.mp4" data-start="0" data-duration="{i_end:.3f}" data-track-index="4" muted playsinline></video></div>
      </div></div>
      {"".join(POST)}
      <div id="tint"></div><div id="leak"></div><div id="flash"></div><div id="grain"></div>
      <audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(list(dict.fromkeys(HIDE)))}, {{opacity: 0}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    ev = sorted(({"t": round(t, 3), "type": k} for t, k in CUES if 0 <= t < DUR), key=lambda e: e["t"])
    json.dump(ev, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SECS)} sections, {len(ev)} sound moments")


if __name__ == "__main__":
    main()
