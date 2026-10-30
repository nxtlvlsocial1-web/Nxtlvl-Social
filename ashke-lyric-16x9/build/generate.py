"""Ashke (Karan Aujla, Mxrci) lyric edit, 16:9, 60 s from 2:14 of the song: writes index.html.

python3 build/generate.py      (from the project root; after build/paper.py, build/footage.py and build/audio.py)

A fusion of the music video with the owner's collage references (the YouMotion paper-zine lyric edit for the look, the
J3nn1f3rJun1p3r punk collage for the frame pacing): the video, cut on every half beat, photocopied in black and white and
stepped to 15 fps (assets/video/bw_main.mp4), sits in a torn paper card that jumps to a new layout on every line. Each
line is a scene built piece by piece on the half beats: texture panels (hazard stripes, halftone, diamond plate, pixel
blocks, newsprint, lines), a starburst, the barcode ticket, a road-sign arrow. Lyrics are tape labels that slam in on
their sung word; keywords are huge red letters on a starburst or white on red tape, circled in blue. Velocity strips
shoot across every two beats; scene changes are slanted texture-strip wipes, paper tears and flashes. Everything moves
in stepped frames with hard edges and hard shadows, no blur.
Lyric timings: ElevenLabs Scribe word timestamps; the romanized Punjabi is ours (confirmed by the owner).
"""
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 60.0
W = json.load(open(os.path.join(ROOT, "plan", "words_scribe.json")))
SHOTS = json.load(open(os.path.join(ROOT, "plan", "shots.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
R = random.Random(21)
A, HIDE, WIPE = [], [], []
RED, INK, PAPER, BLUE = "#e3262e", "#141414", "#efece6", "#2aa7d8"

# (first word, last word, romanized words, side of the photo card: l / r / full). Words marked * are keywords.
LYRICS = [
    (3, 6, "Main *seedha turiya jaavan", "l"), (7, 10, "Tu takdi tedi *tedi", "r"), (11, 15, "Tu body kar layi *slim", "l"),
    (16, 21, "Tere te main karda kamm *shady", "full"), (22, 27, "Saada taan tora fera hai na", "r"), (28, 31, "Main nahi launda *gedi", "l"),
    (32, 35, "*Kaaran, jutti te *asla", "r"), (36, 40, "Nahi ae tinn ikki *dukki", "l"), (41, 43, "Nahi leeda *latta", "r"),
    (44, 50, "Top da rakhaan main jaana *chadh ke", "l"), (51, 54, "Kacchi oh *chabb jaa", "r"), (55, 61, "Peene haan *chaa nahi, udda kaadh ke", "l"),
    (62, 64, "*Jatt khulla *ghummda", "full"), (65, 71, "*Vairi nu rakhaan main udda taad ke", "r"), (72, 75, "Nahi taan full *baggy", "l"),
    (76, 80, "*Patthraan 'ch aaya munda paadh ke", "r"), (81, 83, "Kardi meri *adeeta", "l"), (84, 88, "Nahi saada khul gaya *chaaka", "r"),
    (89, 94, "Tu dil kardi ae *chori", "l"), (95, 100, "Nahi taan main maari da *daaka", "full"), (101, 104, "*Bebe kehndi tainu vyahna", "r"),
    (105, 109, "Te mera *shastar dena thaaka", "l"), (110, 114, "Dass ki kar lena *kaama", "r"), (115, 119, "Nahi mera *baaja yaala raakha", "l"),
    (120, 122, "Raahan vich *rode", "r"), (123, 128, "Behna ji *yaarana bhena kass ke", "l"), (129, 131, "*Jatt mudhto *zehri", "full"),
    (132, 137, "*Naagni reha koi saanu dass ke", "r"), (138, 141, "*Baape di saanu bakhshe", "l"), (142, 145, "Chanattiyan *gaani lass ke", "r"),
    (146, 148, "Nahi *mod te paundi", "l"), (149, 153, "Chhumbar de naale kehki *Ashke", "full"), (154, 156, "Nahi mod te paundi", "full"),
]


def js(s):
    A.append("      " + s)


def line_times(li):
    a = W[LYRICS[li][0]]["s"] - .06
    b = (W[LYRICS[li + 1][0]]["s"] - .06) if li + 1 < len(LYRICS) else DUR
    return a, b


def word_slots(li):
    i0, i1, text, _ = LYRICS[li]
    toks = text.split()
    n = i1 - i0 + 1
    slots = [i0 + round(k * (n - 1) / max(1, len(toks) - 1)) for k in range(len(toks))] if len(toks) > 1 else [i0]
    return [(tok.lstrip("*"), tok.startswith("*"), W[s]["s"]) for tok, s in zip(toks, slots)]


def side_at(t):
    if t < line_times(0)[0]:
        return "full"
    for li in range(len(LYRICS)):
        a, b = line_times(li)
        if a <= t < b:
            return LYRICS[li][3]
    return "full"


def torn(w, h, jag=10, seed=0):
    """A torn-paper polygon (CSS clip-path in %): the four edges are jagged at random."""
    g = random.Random(seed)
    pts = []
    for (x0, y0, x1, y1) in [(0, 0, 100, 0), (100, 0, 100, 100), (100, 100, 0, 100), (0, 100, 0, 0)]:
        n = 14
        for k in range(n):
            u = k / n
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            jx = g.uniform(0, jag) * 100 / w if x0 == x1 else 0
            jy = g.uniform(0, jag) * 100 / h if y0 == y1 else 0
            x += jx if x0 == 0 and x1 == 0 else -jx if x0 == 100 else 0
            y += jy if y0 == 0 and y1 == 0 else -jy if y0 == 100 else 0
            pts.append(f"{x:.2f}% {y:.2f}%")
    return "polygon(" + ", ".join(pts) + ")"


def blob_path(cx, cy, rx, ry, seed, n=22):
    """A torn paper shape as an SVG path (red or black scraps)."""
    import math
    g = random.Random(seed)
    pts = []
    for k in range(n):
        a = k / n * math.pi * 2
        r = 1 + g.uniform(-.18, .12)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + " Z"


CARD = {   # left, top, width, height, rotation
    "l": [(110, 120, 780, 840, -3), (140, 90, 740, 900, 2), (90, 150, 820, 780, -1.5)],
    "r": [(1030, 120, 780, 840, 3), (1050, 90, 740, 900, -2), (1010, 150, 820, 780, 1.5)],
    "full": [(-40, -30, 2000, 1140, 1), (-30, -40, 1980, 1160, -1), (-50, -20, 2020, 1120, .6)],
}
PERIOD = 60 / BEATS["bpm"]
TEX = ["hz", "dots", "lines", "dia", "blocks", "news", "hz2", "dotsb", "grid"]
STAIR = {"r": "polygon(0 0, 100% 0, 100% 18%, 88% 18%, 88% 41%, 100% 41%, 100% 63%, 92% 63%, 92% 82%, 100% 82%, 100% 100%, 0 100%)",
         "l": "polygon(0 0, 100% 0, 100% 100%, 0 100%, 0 82%, 8% 82%, 8% 63%, 0 63%, 0 41%, 12% 41%, 12% 18%, 0 18%)"}
SLANT = "polygon(7% 0, 100% 0, 93% 100%, 0 100%)"
NPNL = 6


def scenes():
    """One scene per lyric line (plus the intro); the scene is the unit the layout holds for, like the reference."""
    out = [(0.0, line_times(0)[0], "full", -1)]
    for li in range(len(LYRICS)):
        a, b = line_times(li)
        out.append((a, b, LYRICS[li][3], li))
    return out


def card_track():
    """The photo card jumps to a new size, tilt and torn edge on every new line (and mid-line in long lines); inside,
    the footage cuts on every half beat. The card bumps on every beat; sometimes it turns red (multiply)."""
    starts = []
    for a, b, side, li in scenes():
        starts.append(a)
        if b - a > 2.4:
            mid = min(BEATS["beats"], key=lambda bt: abs(bt - (a + b) / 2))
            if a + .5 < mid < b - .5:
                starts.append(mid)
    for i, t in enumerate(starts):
        side = side_at(t + .01)
        x, y, w, h, rot = R.choice(CARD[side])
        rot += R.uniform(-1.5, 1.5)
        clip = torn(w, h, 14 if side != "full" else 0, seed=i)
        js(f'tl.set("#card", {{left: {x}, top: {y}, width: {w}, height: {h}, rotation: {rot:.2f}, clipPath: "{clip}"}}, {t:.3f});')
        js(f'tl.fromTo("#card", {{scale: 1.12}}, {{scale: 1, duration: .1, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
        js(f'tl.set("#tint", {{opacity: {.85 if (i % 4 == 2 and side != "full") else 0}}}, {t:.3f});')
        if side != "full":
            cx = x + w * R.uniform(.25, .75)
            cy = y + h * R.uniform(.3, .8)
            js(f'tl.set("#redp", {{attr: {{d: "{blob_path(cx, cy, w * .55, h * .38, i)}"}}, opacity: 1}}, {t:.3f});')
        else:
            js(f'tl.set("#redp", {{opacity: 0}}, {t:.3f});')
    for bt in BEATS["beats"]:
        if bt < DUR - .2 and all(abs(bt - s) > .1 for s in starts):
            js(f'tl.fromTo("#card", {{scale: 1.04}}, {{scale: 1, duration: .067, ease: "steps(1)", immediateRender: false}}, {bt:.3f});')


def panel_slots(side, cx, cy, cw, ch):
    """Where the texture panels go for a scene: behind the card, framing the lyric side (top band, bottom band, the far
    edge strip) and a small square by the card's corner. Order = build order."""
    lx = 970 if side == "l" else 0
    far = 1690 if side == "l" else 0
    return [
        (cx + (-70 if side == "l" else 160), cy + 180, cw * .62, ch * .85, R.uniform(-4, 4)),          # behind the card
        (far, -40, 230, 1160, 0),                                                                     # far edge strip
        (lx - 20, -30, 980, R.choice([150, 190]), R.uniform(-3, 3)),                                   # top band
        (lx - 30, R.choice([880, 900]), 1000, 230, R.uniform(-3, 3)),                                 # bottom band
        (cx + (cw - 120 if side == "l" else -140), cy - 60, 260, 260, R.uniform(-10, 10)),           # corner square
        (cx + (-60 if side == "l" else cw - 300), cy + ch - 160, 360, 220, R.uniform(-6, 6)),       # lower corner
    ]


def props():
    html = "".join(f'<i class="pnl" id="pn{k}"></i>' for k in range(NPNL))
    HIDE.extend([f"#pn{k}" for k in range(NPNL)])
    bars = "".join(f'<rect x="{x}" y="0" width="{w}" height="60"/>' for x, w in zip(range(0, 230, 9), [3, 5, 2, 7, 3, 2, 6, 3, 4, 2, 5, 3, 7, 2, 3, 6, 2, 4, 3, 5, 2, 6, 3, 2, 5, 3]))
    html += (f'<div class="prop tick" id="tick" data-layout-ignore><svg viewBox="0 0 232 60" width="232" height="60">{bars}</svg>'
             '<div><b>ASHKE</b><small>KARAN AUJLA &#183; MXRCI &#183; 0214-0314 &#183; P-POP</small></div></div>')
    html += ('<div class="prop" id="arrow"><svg viewBox="-50 -50 100 100" width="230" height="230"><circle r="46" fill="#f4f2ec" stroke="#141414" stroke-width="7"/>'
             '<path d="M-24 18 L14 -20 L2 -20 L2 -30 L30 -30 L30 -2 L20 -2 L20 -14 L-18 24 Z" fill="#141414"/></svg></div>')
    for k in range(2):
        html += f'<svg class="prop bstb" id="bst{k}" viewBox="-50 -50 100 100"><path d="{burst_path(90 + k, 11)}"/></svg>'
    HIDE.extend(["#tick", "#arrow", "#bst0", "#bst1"])
    return html


def scene_builds():
    """Each scene is built piece by piece, like the reference: two texture panels at once, then one more element on
    every half beat (panels, a starburst, the barcode ticket, the road-sign arrow). Everything clears at the next scene."""
    for si, (a, b, side, li) in enumerate(scenes()):
        if side == "full":
            for k in range(NPNL):
                js(f'tl.set("#pn{k}", {{opacity: 0}}, {a:.3f});')
            continue
        cx, cy, cw, ch, _ = CARD[side][0]
        slots = panel_slots(side, cx, cy, cw, ch)
        texs = R.sample(TEX, NPNL)
        t = a
        for k, (x, y, w, h, rot) in enumerate(slots):
            if k >= 2:
                t += PERIOD / 2
            clip = STAIR[side] if k == 1 else R.choice(["none", SLANT, "none"])
            when = a if k < 2 else t
            if when >= b - .08:
                js(f'tl.set("#pn{k}", {{opacity: 0}}, {a:.3f});')
                continue
            js(f'tl.set("#pn{k}", {{opacity: 1, left: {x:.0f}, top: {y:.0f}, width: {w:.0f}, height: {h:.0f}, rotation: {rot:.1f}, '
               f'className: "pnl {texs[k]}", clipPath: "{clip}"}}, {when:.3f});')
            js(f'tl.fromTo("#pn{k}", {{x: {R.choice([-140, 140])}}}, {{x: 0, duration: .067, ease: "steps(1)", immediateRender: false}}, {when:.3f});')
            if b < DUR:
                js(f'tl.set("#pn{k}", {{opacity: 0}}, {b:.3f});')
        # one prop per scene, on the next half beat, cycling
        prop = ["#tick", "#arrow", "#bst0", "#tick", "#bst1", "#arrow"][si % 6]
        tp = a + PERIOD * R.choice([1, 1.5, 2])
        if tp < b - .2:
            px = R.randint(1180, 1560) if side == "l" else R.randint(80, 520)
            py = R.choice([60, 760])
            js(f'tl.set("{prop}", {{opacity: 1, left: {px}, top: {py}, rotation: {R.randint(-14, 14)}}}, {tp:.3f});')
            js(f'tl.fromTo("{prop}", {{scale: 1.5}}, {{scale: 1, duration: .067, ease: "steps(1)", immediateRender: false}}, {tp:.3f});')
            js(f'tl.set("{prop}", {{opacity: 0}}, {b:.3f});')
    js('tl.to("#arrow svg", {rotation: 720, duration: 60, ease: "steps(240)"}, 0);')


def still_cards():
    """Photocopied stills as secondary cards on the lyric side, hard white borders, swapping every couple of beats."""
    html = ""
    t, k = line_times(0)[0], 0
    while t < 57.0:
        side = side_at(t + .01)
        if side != "full":
            sid = f"st{k}"
            x = R.randint(1180, 1500) if side == "l" else R.randint(120, 440)
            y = R.choice([90, 600])
            rot = R.uniform(-9, 9)
            html += (f'<div class="still" id="{sid}" style="left:{x}px;top:{y}px;transform:rotate({rot:.1f}deg)">'
                     f'<img src="assets/img/stills/s{k % 20:02d}.jpg" alt=""></div>')
            HIDE.append(f"#{sid}")
            js(f'tl.set("#{sid}", {{opacity: 1}}, {t:.3f});')
            js(f'tl.fromTo("#{sid}", {{x: {R.choice([-300, 300])}}}, {{x: 0, duration: .1, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
            js(f'tl.set("#{sid}", {{opacity: 0}}, {t + 1.3:.3f});')
            k += 1
        t += 2 * PERIOD
    return html


def burst_path(seed, n=13):
    """A jagged starburst (the reference's black spiky shapes)."""
    import math
    g = random.Random(seed)
    pts = []
    for k in range(n * 2):
        r = g.uniform(40, 50) if k % 2 == 0 else g.uniform(14, 26)
        a = k / (n * 2) * math.pi * 2 + g.uniform(-.08, .08)
        pts.append(f"{math.cos(a) * r:.1f} {math.sin(a) * r:.1f}")
    return "M" + " L".join(pts) + " Z"


def labels():
    """Each lyric line as a stack of tape labels slamming in on the sung word (from the side, two stepped frames);
    keywords are huge red letters on a white starburst, or white on red tape, circled in blue."""
    out = []
    styles = ["blk", "wht", "red", "blk", "wht", "wht"]
    for li, (i0, i1, text, side) in enumerate(LYRICS):
        a, b = line_times(li)
        ws = word_slots(li)
        if li == len(LYRICS) - 1:
            ws = []                     # the last line: the title card owns the screen
        if li == len(LYRICS) - 2:
            ws = [w for w in ws if w[0] != "Ashke"]   # "Ashke" becomes the title card itself
        groups, cur = [], []
        for w in ws:
            if w[1]:
                if cur:
                    groups.append(cur)
                    cur = []
                groups.append([w])
            else:
                cur.append(w)
                if len(cur) == 2 or sum(len(x[0]) for x in cur) > 10:
                    groups.append(cur)
                    cur = []
        if cur:
            groups.append(cur)
        cx = 1420 if side == "l" else 500 if side == "r" else 960
        rows = []
        for gi, grp in enumerate(groups):
            key = grp[0][1]
            txt = " ".join(x[0] for x in grp)
            lid = f"lb{li}_{gi}"
            rot = R.uniform(-5, 5)
            dx = R.randint(-70, 70) if side != "full" else R.randint(-160, 160)
            if key:
                circ = (f'<svg class="circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path pathLength="400" '
                        f'd="M52 6 C95 4 104 90 50 95 S-6 12 60 9"/></svg>')
                if gi % 2:
                    rows.append(f'<div class="lb kw kwr" id="{lid}" style="transform:translateX({dx}px) rotate({rot:.1f}deg)">{txt}{circ}</div>')
                else:
                    bst = f'<svg class="bst" viewBox="-50 -50 100 100" preserveAspectRatio="none"><path d="{burst_path(li * 7 + gi)}"/></svg>'
                    rows.append(f'<div class="lb kw" id="{lid}" style="transform:translateX({dx}px) rotate({rot:.1f}deg)">{bst}<span>{txt}</span>{circ}</div>')
                js(f'tl.fromTo("#{lid} .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .2, ease: "steps(3)", immediateRender: false}}, {grp[0][2] + .1:.3f});')
            else:
                st = styles[(li + gi) % len(styles)]
                rows.append(f'<div class="lb {st}" id="{lid}" style="transform:translateX({dx}px) rotate({rot:.1f}deg)">{txt}</div>')
            HIDE.append(f"#{lid}")
            t = grp[0][2]
            js(f'tl.set("#{lid}", {{opacity: 1}}, {t:.3f});')
            if key:
                js(f'tl.fromTo("#{lid}", {{scale: 1.7}}, {{scale: 1, duration: .1, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
            else:
                js(f'tl.fromTo("#{lid}", {{x: {R.choice([-620, 620])}}}, {{x: 0, duration: .1, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
        top = "full" if side == "full" else "side"
        out.append(f'<div class="stack {top}" id="sk{li}" style="left:{cx - 450}px">{"".join(rows)}</div>')
        HIDE.append(f"#sk{li}")
        js(f'tl.set("#sk{li}", {{opacity: 1}}, {a:.3f});')
        if b < DUR:
            js(f'tl.set("#sk{li}", {{opacity: 0}}, {b:.3f});')
    return "".join(out)


def velocity():
    """Velocity strips: full-width bands of texture (or ASHKE / KARAN AUJLA type) that shoot across the frame in five
    stepped frames, with speed lines; every two beats, every half beat in the bursts."""
    html = ""
    for k in range(3):
        html += f'<div class="vs" id="vs{k}"><b>{"ASHKE &#9679; KARAN AUJLA &#9679; MXRCI &#9679; " * 6}</b></div>'
        HIDE.append(f"#vs{k}")
    html += '<svg id="spd" viewBox="0 0 1920 300" preserveAspectRatio="none">' + "".join(
        f'<rect x="{R.randint(0, 900)}" y="{y}" width="{R.randint(500, 1100)}" height="{R.choice([3, 5, 8])}"/>' for y in range(10, 300, 36)) + '</svg>'
    HIDE.append("#spd")
    beats = [bt for bt in BEATS["beats"] if 2.2 < bt < 57.5]
    times = []
    for i, bt in enumerate(beats):
        burst = 14.3 <= bt < 16.3 or 44.8 <= bt < 46.3 or 48.5 <= bt < 50.0
        if burst:
            times += [bt, bt + PERIOD / 2]
        elif i % 2 == 0:
            times.append(bt)
    kinds = ["hz", "type", "dots", "blocks", "type", "lines", "hz2", "news"]
    for n, t in enumerate(times):
        vid = f"#vs{n % 3}"
        d = 1 if n % 2 == 0 else -1
        h = R.choice([70, 100, 130, 160])
        y = R.choice([R.randint(20, 220), R.randint(800, 1000 - h)])
        rot = R.uniform(-6, 6)
        js(f'tl.set("{vid}", {{opacity: 1, top: {y}, height: {h}, rotation: {rot:.1f}, className: "vs {kinds[n % len(kinds)]}"}}, {t:.3f});')
        js(f'tl.fromTo("{vid}", {{x: {-2700 if d > 0 else 1950}}}, {{x: {1950 if d > 0 else -2700}, duration: .3, ease: "steps(5)", immediateRender: false}}, {t:.3f});')
        js(f'tl.set("{vid}", {{opacity: 0}}, {t + .3:.3f});')
        js(f'tl.set("#spd", {{opacity: 1, top: {max(0, y - 90)}, scaleX: {d}, rotation: {rot:.1f}}}, {t + .067:.3f});')
        js(f'tl.set("#spd", {{opacity: 0}}, {t + .2:.3f});')
    return html


def accents():
    """Black stars popping, the scene transitions (slanted texture-strip wipe, paper tear, white flash, red flash) and
    the 15 fps stop-motion boil."""
    html = ""
    for k in range(6):
        html += f'<svg class="star" id="sr{k}" viewBox="-50 -50 100 100"><path d="{star_path()}"/></svg>'
        HIDE.append(f"#sr{k}")
    t, k = 2.0, 0
    while t < 57:
        x, y = R.choice([(80, 880), (1760, 860), (1700, 90), (60, 70), (900, 950), (1800, 520)])
        sz = R.choice([90, 120, 150])
        sid = f"#sr{k % 6}"
        js(f'tl.set("{sid}", {{opacity: 1, left: {x}, top: {y}, width: {sz}, height: {sz}, scale: 0, rotation: {R.randint(0, 60)}}}, {t:.3f});')
        js(f'tl.to("{sid}", {{scale: 1, duration: .067, ease: "steps(1)"}}, {t + .001:.3f});')
        js(f'tl.set("{sid}", {{opacity: 0}}, {t + 1.0:.3f});')
        t += R.choice([PERIOD / 2, PERIOD, PERIOD])
        k += 1
    # the strip wipe: eight texture strips land one frame apart (slanted, vertical or horizontal), then the new scene
    WIPE.append('<div id="wipe">' + "".join(f'<i class="ws" id="ws{k}" style="left:{k * 300}px"></i>' for k in range(8)) + '</div>')
    HIDE.extend([f"#ws{k}" for k in range(8)])
    for li in range(1, len(LYRICS)):
        a = line_times(li)[0]
        kind = ["wipe", "cut", "wipe", "tear", "wipe", "flash", "wipe", "cut"][li % 8]
        if LYRICS[li][3] == "full":
            kind = "red"
        if kind == "wipe":
            rot = R.choice([0, 90, 16, -16, 74])
            d = R.choice([-1, 1])
            js(f'tl.set("#wipe", {{rotation: {rot}}}, {a - .3:.3f});')
            order = list(range(8)) if d > 0 else list(range(7, -1, -1))
            for j, k in enumerate(order):
                tk = a - .3 + j * .033
                js(f'tl.set("#ws{k}", {{opacity: 1, className: "ws {R.choice(TEX)}"}}, {tk:.3f});')
                js(f'tl.fromTo("#ws{k}", {{y: {R.choice([-2400, 2400])}}}, {{y: 0, duration: .067, ease: "steps(1)", immediateRender: false}}, {tk:.3f});')
            js(f'tl.set({json.dumps([f"#ws{k}" for k in range(8)])}, {{opacity: 0}}, {a:.3f});')
        elif kind == "tear":
            d = R.choice([-1, 1])
            js(f'tl.fromTo("#tear", {{x: {-2400 * d}}}, {{x: {2400 * d}, duration: .2, ease: "steps(4)", immediateRender: false}}, {a - .1:.3f});')
        elif kind == "flash":
            js(f'tl.set("#flash", {{opacity: .9}}, {a:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {a + .067:.3f});')
        elif kind == "red":
            js(f'tl.set("#redflash", {{opacity: 1}}, {a - .067:.3f});')
            js(f'tl.set("#redflash", {{opacity: 0}}, {a + .033:.3f});')
    # stop-motion boil at 15 fps (every second frame), harder on the beats
    g = random.Random(5)
    for f in range(int(DUR * 15)):
        t = f / 15
        hit = any(0 <= t - bt < .07 for bt in BEATS["beats"])
        amp = 9 if hit else 1.5
        js(f'tl.set("#collage", {{x: {g.uniform(-amp, amp):.1f}, y: {g.uniform(-amp, amp):.1f}, rotation: {g.uniform(-.2, .2) * (3 if hit else 1):.2f}}}, {t:.3f});')
        if f % 2 == 0:
            js(f'tl.set("#paper", {{x: {g.randint(-30, 0)}, y: {g.randint(-30, 0)}}}, {t:.3f});')
    return html


def star_path():
    import math
    pts = []
    for k in range(16):
        r = 48 if k % 2 == 0 else 20
        a = k / 16 * math.pi * 2
        pts.append(f"{math.cos(a) * r:.1f} {math.sin(a) * r:.1f}")
    return "M" + " L".join(pts) + " Z"


def ending():
    """Title card: ASHKE in red, circled, KARAN AUJLA on a black label, the credit line in typewriter."""
    t = W[153]["s"]
    HIDE.extend(["#endt", "#endk"])
    js(f'tl.set("#endt", {{opacity: 1}}, {t:.3f});')
    js(f'tl.set("#sk{len(LYRICS) - 2}", {{opacity: 0}}, {t:.3f});')        # the title card replaces the line's labels
    js(f'tl.fromTo("#endt", {{scale: 2.2, rotation: -8}}, {{scale: 1, rotation: -3, duration: .14, ease: "steps(4)", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#endt .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .4, ease: "power2.out", immediateRender: false}}, {t + .2:.3f});')
    js(f'tl.set("#endk", {{opacity: 1}}, {t + .45:.3f});')
    js(f'tl.fromTo("#endk", {{x: -120}}, {{x: 0, duration: .1, ease: "steps(3)", immediateRender: false}}, {t + .45:.3f});')
    # the same title card opens the edit, before the first lyric
    a0 = line_times(0)[0]
    HIDE.extend(["#opt", "#opk"])
    js('tl.set("#opt", {opacity: 1}, .15);')
    js('tl.fromTo("#opt", {scale: 2.2, rotation: -8}, {scale: 1, rotation: -3, duration: .14, ease: "steps(4)", immediateRender: false}, .15);')
    js('tl.fromTo("#opt .circ path", {strokeDashoffset: 400}, {strokeDashoffset: 0, duration: .4, ease: "power2.out", immediateRender: false}, .45);')
    js('tl.set("#opk", {opacity: 1}, .6);')
    js('tl.fromTo("#opk", {x: -120}, {x: 0, duration: .1, ease: "steps(3)", immediateRender: false}, .6);')
    js(f'tl.set(["#opt", "#opk"], {{opacity: 0}}, {a0:.3f});')
    return ('<div id="opt" class="lb kw end"><span>ASHKE</span><svg class="circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path pathLength="400" '
            'd="M52 6 C95 4 104 90 50 95 S-6 12 60 9"/></svg></div><div id="opk" class="lb blk endk">KARAN AUJLA · MXRCI</div>'
            '<div id="endt" class="lb kw end"><span>ASHKE</span><svg class="circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path pathLength="400" '
            'd="M52 6 C95 4 104 90 50 95 S-6 12 60 9"/></svg></div><div id="endk" class="lb blk endk">KARAN AUJLA · MXRCI</div>')


CSS = f"""
@font-face {{ font-family: "Bebas Neue"; src: url("assets/fonts/BebasNeue/BebasNeue-400.ttf"); }}
@font-face {{ font-family: "Oswald"; font-weight: 700; src: url("assets/fonts/Oswald/Oswald-700.ttf"); }}
@font-face {{ font-family: "Special Elite"; src: url("assets/fonts/SpecialElite/SpecialElite-400.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {PAPER}; }}
#root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: {PAPER}; }}
#paper {{ position: absolute; left: -40px; top: -40px; width: 2040px; height: 1150px; background: url(assets/img/paper.png); }}
#grid {{ position: absolute; inset: 0; pointer-events: none; opacity: .5; }}
#grid line {{ stroke: #3b3835; stroke-width: 1.4; }}
#collage {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
#redsvg {{ position: absolute; inset: 0; width: 1920px; height: 1080px; overflow: visible; }}
#redp {{ fill: {RED}; filter: drop-shadow(8px 8px 0 {INK}); }}
#cardw {{ position: absolute; inset: 0; filter: drop-shadow(12px 12px 0 {INK}); }}
#card {{ position: absolute; left: 110px; top: 120px; width: 780px; height: 840px; overflow: hidden; background: #111; }}
#card video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#tint {{ position: absolute; inset: 0; background: {RED}; mix-blend-mode: multiply; opacity: 0; }}
.still {{ position: absolute; width: 320px; height: 220px; overflow: hidden; border: 9px solid #f4f2ec; box-shadow: 9px 9px 0 {INK}; z-index: 2; }}
.still img {{ width: 100%; height: 100%; object-fit: cover; }}
.edge {{ position: absolute; left: -40px; right: -40px; height: 90px; background: url(assets/img/paper.png) 0 0 / 1020px auto; filter: drop-shadow(0 5px 0 {INK}); }}
.edge.top {{ top: -30px; clip-path: polygon({", ".join(f"{k * 100 / 40:.1f}% {random.Random(k).uniform(55, 100):.0f}%" for k in range(41))}, 100% 0, 0 0); }}
.edge.bot {{ bottom: -30px; clip-path: polygon({", ".join(f"{k * 100 / 40:.1f}% {random.Random(k + 77).uniform(0, 45):.0f}%" for k in range(41))}, 100% 100%, 0 100%); }}
#lyrics {{ position: absolute; inset: 0; z-index: 5; pointer-events: none; }}
.stack {{ position: absolute; top: 0; height: 1080px; width: 900px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; opacity: 0; }}
.lb {{ position: relative; display: inline-block; font: 400 96px/1 "Bebas Neue"; letter-spacing: 1px; padding: 10px 26px 4px; white-space: nowrap; filter: url(#rough); }}
.lb.blk {{ background: {INK}; color: {PAPER}; }}
.lb.wht {{ background: #f7f5f0; color: {INK}; box-shadow: 0 6px 12px rgba(0,0,0,.18); }}
.lb.red {{ background: {RED}; color: #fff; }}
.lb.kw {{ font: 700 190px/.9 "Oswald"; text-transform: uppercase; color: #d11a22; letter-spacing: -2px; padding: 0 30px; text-shadow: 7px 7px 0 #141414, -1px -1px 0 #141414; }}
.lb.kw span {{ position: relative; }}
.bst {{ position: absolute; left: -14%; top: -40%; width: 128%; height: 180%; z-index: -1; overflow: visible; }}
.bst path {{ fill: #f7f5f0; stroke: {INK}; stroke-width: 2.4; vector-effect: non-scaling-stroke; }}
.lb.kw.kwr {{ background: {RED}; color: #fff; text-shadow: none; padding: 8px 34px 0; }}
.stack.full .lb {{ font-size: 120px; }}
.stack.full .lb.kw {{ font-size: 260px; }}
.circ {{ position: absolute; left: -12%; top: -24%; width: 124%; height: 148%; overflow: visible; pointer-events: none; }}
.circ path {{ fill: none; stroke: {BLUE}; stroke-width: 5; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
.pnl {{ position: absolute; left: 0; top: 0; width: 300px; height: 300px; box-shadow: 10px 10px 0 {INK}; }}
.hz {{ background: repeating-linear-gradient(45deg, {INK} 0 34px, #f2f0ea 34px 68px); }}
.hz2 {{ background: repeating-linear-gradient(-50deg, #f2f0ea 0 22px, {INK} 22px 64px); }}
.dots {{ background: #f2f0ea radial-gradient(circle, {INK} 0 37%, transparent 39%) 0 0 / 22px 22px; }}
.dotsb {{ background: {INK} radial-gradient(circle, #f2f0ea 0 30%, transparent 32%) 0 0 / 18px 18px; }}
.lines {{ background: repeating-linear-gradient(0deg, {INK} 0 7px, #f2f0ea 7px 20px); }}
.dia {{ background: url(assets/img/tex/diamond.png) 0 0 / 300px 300px; }}
.blocks {{ background: url(assets/img/tex/blocks.png) center / cover; }}
.news {{ background: url(assets/img/tex/news.png) center / cover; }}
.grid {{ background: #f2f0ea linear-gradient({INK} 0 3px, transparent 3px) 0 0 / 60px 60px, linear-gradient(90deg, {INK} 0 3px, transparent 3px) 0 0 / 60px 60px; }}
.prop {{ position: absolute; opacity: 0; z-index: 3; }}
.tick {{ display: flex; gap: 18px; align-items: center; padding: 16px 26px; background: #f4f2ec; border: 4px solid {INK}; box-shadow: 10px 10px 0 {INK}; }}
.tick svg rect {{ fill: {INK}; }}
.tick b {{ display: block; font: 700 64px/1 "Oswald"; color: {INK}; letter-spacing: 1px; }}
.tick small {{ display: block; font: 400 17px/1.2 "Special Elite"; color: {INK}; margin-top: 4px; }}
.bstb {{ width: 300px; height: 300px; overflow: visible; }}
.bstb path {{ fill: {INK}; }}
.vs {{ position: absolute; left: 0; top: 0; width: 2600px; height: 120px; z-index: 4; opacity: 0; overflow: hidden; box-shadow: 0 8px 0 {INK}; }}
.vs b {{ display: none; }}
.vs.type {{ background: {INK}; }}
.vs.type b {{ display: block; white-space: nowrap; font: 400 120px/1 "Bebas Neue"; color: #f4f2ec; letter-spacing: 4px; padding-top: 6px; }}
#spd {{ position: absolute; left: 0; top: 0; width: 1920px; height: 300px; z-index: 4; opacity: 0; }}
#spd rect {{ fill: {INK}; }}
#wipe {{ position: absolute; left: -240px; top: -660px; width: 2400px; height: 2400px; z-index: 8; pointer-events: none; }}
.ws {{ position: absolute; top: 0; width: 304px; height: 2400px; opacity: 0; }}
.star {{ position: absolute; opacity: 0; fill: {INK}; }}
#tear {{ position: absolute; top: -60px; left: -100px; width: 2120px; height: 1200px; z-index: 8; pointer-events: none; transform: translateX(-2400px);
  background: url(assets/img/paper.png);
  clip-path: polygon({", ".join(f"{random.Random(k).uniform(0, 4):.1f}% {k * 100 / 30:.1f}%" for k in range(31))}, {", ".join(f"{100 - random.Random(k + 9).uniform(0, 4):.1f}% {100 - k * 100 / 30:.1f}%" for k in range(31))}); }}
#flash {{ position: absolute; inset: 0; z-index: 9; background: #fff; opacity: 0; }}
#redflash {{ position: absolute; inset: 0; z-index: 9; background: {RED}; opacity: 0; mix-blend-mode: multiply; }}
#vig {{ position: absolute; inset: 0; z-index: 11; pointer-events: none; background: radial-gradient(ellipse 80% 80% at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,.16) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1960px; height: 1120px; z-index: 12; pointer-events: none; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
#opt, #endt {{ position: absolute; left: 0; right: 0; top: 300px; margin: 0 auto; width: fit-content; z-index: 6; opacity: 0; font-size: 300px; }}
#opk, #endk {{ position: absolute; left: 0; right: 0; top: 700px; margin: 0 auto; width: fit-content; z-index: 6; opacity: 0; font-size: 80px; }}
"""


def main():
    card_track()
    pr = props()
    scene_builds()
    st = still_cards()
    vel = velocity()
    lb = labels()
    acc = accents()
    end = ending()
    gl = random.Random(4)
    grid = "".join(f'<line x1="{x + gl.uniform(-8, 8):.0f}" y1="-20" x2="{x + gl.uniform(-30, 30):.0f}" y2="1100"/>' for x in range(180, 1920, 260)) + \
           "".join(f'<line x1="-20" y1="{y + gl.uniform(-8, 8):.0f}" x2="1940" y2="{y + gl.uniform(-25, 25):.0f}"/>' for y in range(150, 1080, 240))
    g = random.Random(3)
    for f in range(int(DUR * 15)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 15:.3f});')
    html = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Ashke collage lyric edit 16x9</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1920" data-height="1080">
      <div id="paper"></div>
      <svg id="grid" viewBox="0 0 1920 1080">{grid}</svg>
      <div id="collage">
        {pr}
        <svg id="redsvg" viewBox="0 0 1920 1080"><path id="redp" d="M0 0"/></svg>
        <div id="cardw"><div id="card"><video id="vid" class="clip" src="assets/video/bw_main.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" muted playsinline></video><i id="tint"></i></div></div>
        {st}
        {acc}
        {vel}
        <div class="edge top"></div><div class="edge bot"></div>
      </div>
      <div id="lyrics" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{lb}{end}</div>
      <div id="tear"></div>
      {"".join(WIPE)}
      <div id="flash"></div>
      <div id="redflash"></div>
      <div id="vig"></div>
      <div id="grain"></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
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
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SHOTS)} shots, {len(LYRICS)} lines")


if __name__ == "__main__":
    main()
