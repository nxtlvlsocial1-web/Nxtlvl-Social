"""Ashke (Karan Aujla, Mxrci) lyric edit, 9:16, 60 s from 2:14 of the song: writes index.html.

python3 build/generate.py      (from the project root; after build/paper.py, build/textures.py, build/footage.py and
build/audio.py)

The 9:16 version of the collage fusion, cut and camera-moved like the owner's YouMotion reference. Measured from that
reference (phase correlation, frame by frame): it moves at 15 fps; every lyric line is a scene; the camera whips into
the scene and settles (expo ease-out, roughly 450 px over half a second), tracks each new word as it lands (the
labels stack along the page and the camera follows them down), drifts or pushes in slowly while the line holds, then
accelerates out into a hard cut where the next scene picks up the same direction (a whip pan across the cut). Hit lines
zoom through their keyword. Some lines are type only, laid out down the page with the camera tracking word to word.
Everything else is the v4 collage: the music video photocopied in a torn card, texture panels, starbursts, stills,
the barcode ticket, the road-sign arrow, velocity strips; hard edges and hard shadows, no blur.
Fused with the owner's eimantasbitinas23 reference (cinema()): on the hit lines and the bursts the collage gives way to
full-bleed colour-graded footage (assets/video/cine.mp4: red monochrome, film colour with grain, one-bit threshold),
smooth at the full frame rate with a handheld drift, under flickering glass shards, torn paper slivers, a VHS scan line
and a red picture-in-picture still; black title cards flash in front of the hits, the bursts are flurries of 4-frame
cuts, two lines are a stop-motion photo grid on white paper, a red iris closes into the red segment, and torn paper
cards with a photocopied still tear back into the collage.
Lyric timings: ElevenLabs Scribe word timestamps; the romanized Punjabi is ours (confirmed by the owner).
"""
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR, FW, FH = 60.0, 1080, 1920
W = json.load(open(os.path.join(ROOT, "plan", "words_scribe.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
PERIOD = 60 / BEATS["bpm"]
R = random.Random(21)
A, HIDE = [], []
RED, INK, PAPER, BLUE = "#e3262e", "#141414", "#efece6", "#2aa7d8"

# (first word, last word, romanized words, layout: l = card on top, r = card below, full = big card). * = keyword
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
TXT = {4, 30}                      # type-only scenes: no card, the camera tracks the words down the page
CINE = {3, 7, 12, 19, 24, 26, 31, 32}   # full-bleed cinema (hit lines and bursts), see build/cine.py
GRID = {10, 17}                    # stop-motion photo grid on white paper
CARDS = {3: "KAMM\nSHADY", 12: "JATT\nKHULLA\nGHUMMDA", 19: "NAHI TAAN\nDAAKA", 26: "JATT\nMUDHTO\nZEHRI"}
# whip direction per scene (where the camera travels); mostly down the page like the reference, some sideways
DIRS = [(0, 1), (0, 1), (1, 0), (0, 1), (-.8, .6), (0, 1), (0, -1), (.7, .7), (0, 1), (-1, 0), (0, 1), (.6, .8)]
TEX = ["hz", "dots", "lines", "dia", "blocks", "news", "hz2", "dotsb", "grid"]
NPNL = 6


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


def torn(w, h, jag=10, seed=0):
    """A torn-paper polygon (CSS clip-path in %): the four edges are jagged at random."""
    g = random.Random(seed)
    pts = []
    for (x0, y0, x1, y1) in [(0, 0, 100, 0), (100, 0, 100, 100), (100, 100, 0, 100), (0, 100, 0, 0)]:
        for k in range(14):
            u = k / 14
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            jx = g.uniform(0, jag) * 100 / w if x0 == x1 else 0
            jy = g.uniform(0, jag) * 100 / h if y0 == y1 else 0
            x += jx if x0 == 0 and x1 == 0 else -jx if x0 == 100 else 0
            y += jy if y0 == 0 and y1 == 0 else -jy if y0 == 100 else 0
            pts.append(f"{x:.2f}% {y:.2f}%")
    return "polygon(" + ", ".join(pts) + ")"


def blob_path(cx, cy, rx, ry, seed, n=22):
    g = random.Random(seed)
    pts = []
    for k in range(n):
        a = k / n * math.pi * 2
        r = 1 + g.uniform(-.18, .12)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + " Z"


def star_path():
    pts = []
    for k in range(16):
        r = 48 if k % 2 == 0 else 20
        a = k / 16 * math.pi * 2
        pts.append(f"{math.cos(a) * r:.1f} {math.sin(a) * r:.1f}")
    return "M" + " L".join(pts) + " Z"


def burst_path(seed, n=13):
    g = random.Random(seed)
    pts = []
    for k in range(n * 2):
        r = g.uniform(40, 50) if k % 2 == 0 else g.uniform(14, 26)
        a = k / (n * 2) * math.pi * 2 + g.uniform(-.08, .08)
        pts.append(f"{math.cos(a) * r:.1f} {math.sin(a) * r:.1f}")
    return "M" + " L".join(pts) + " Z"


CIRC = ('<svg class="circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path pathLength="400" '
        'd="M52 6 C95 4 104 90 50 95 S-6 12 60 9"/></svg>')


# ---------------------------------------------------------------------------------------------------- scene layout
def groups_of(li):
    ws = word_slots(li)
    if li == len(LYRICS) - 1:
        return []                       # the last line: the title card owns the screen
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
    return groups


def layout(li):
    """Card rectangle and label positions (board coordinates; the frame is 0..1080 x 0..1920 at rest)."""
    side = LYRICS[li][3]
    grps = groups_of(li)
    big = side == "full"
    hts = [(235 if big else 165) if g[0][1] else (136 if big else 116) for g in grps]
    gap = 70 if li in TXT else 26
    zig = [-120, 130, -70, 150, -140, 60] if li not in TXT else [-170, 160, -110, 190, -160, 120]
    card = None
    if li in TXT:
        y = 330
    elif li in GRID:
        y = 1330
    elif side == "l":
        card = (60, 190, 960, 800)
        y = 1070
    elif side == "r":
        y = 250
    else:
        card = (-50, 110, 1180, 1220)
        y = 1170
    labels = []
    for k, (g, h) in enumerate(zip(grps, hts)):
        if g[0][1] and k:
            y += 34                     # room for the keyword's starburst and circle
        labels.append((540 + zig[k % len(zig)], y, h))
        y += h + gap
    if side == "r" and li not in TXT and li not in GRID:
        card = (60, max(y + 30, 1030), 960, 800)
    return card, labels, grps


def scenes():
    out = [(0.0, line_times(0)[0], -1)]
    for li in range(len(LYRICS)):
        a, b = line_times(li)
        out.append((a, b, li))
    return out


# ---------------------------------------------------------------------------------------------------- camera
def ease_out(u, p=4):
    return 1 - (1 - u) ** p


def camera():
    """The virtual camera, sampled at 15 fps: focus point (board coordinates at frame centre), scale and rotation.
    Entry whip (expo out), word tracking (power3 out), slow drift or push-in, exit whip (accelerating) into the cut."""
    plans = []
    for si, (a, b, li) in enumerate(scenes()):
        d = DIRS[si % len(DIRS)]
        n = math.hypot(*d)
        d = (d[0] / n, d[1] / n)
        if li < 0 or li in CINE:
            # cinema: the camera rests (the footage carries its own handheld drift); hit lines still zoom through
            zoom = None
            if li >= 0 and li < len(LYRICS) - 2 and LYRICS[li][3] == "full":
                _, labels, grps = layout(li)
                kws = [(x, y + h / 2) for (x, y, h), g in zip(labels, grps) if g[0][1]]
                zoom = kws[-1] if kws else None
            plans.append(dict(a=a, b=b, d=d, f0=(540, 960), keys=[], s0=1.0, push=0, drift=0, rot=0, zoom=zoom, cine=True,
                              nozip=zoom is None))
            continue
        if li in GRID:
            plans.append(dict(a=a, b=b, d=d, f0=(540, 960), keys=[], s0=1.0, push=.012, drift=0, rot=R.uniform(-1, 1), zoom=None))
            continue
        card, labels, grps = layout(li)
        side = LYRICS[li][3]
        if li in TXT:
            f0, s0 = (labels[0][0] * .5 + 270, labels[0][1] + 60) if labels else (540, 960), 1.22
        elif card is None:
            f0, s0 = (540, 960), 1.0
        elif side == "l":
            f0, s0 = (540, 900), 1.0
        elif side == "r":
            f0, s0 = (540, max(960, labels[0][1] + 700) if labels else 960), 1.0
        else:
            f0, s0 = (540, 940), 1.0
        keys = []
        for (x, y, h), g in zip(labels, grps):
            cy = y + h / 2
            if li in TXT:
                tgt = (x * .5 + 270, cy)
            else:
                tgt = (540 + (x - 540) * .25, f0[1] * .45 + cy * .55)
            keys.append((g[0][2], tgt))
        zoom = None
        if side == "full" and li < len(LYRICS) - 1:
            kws = [(x, y + h / 2) for (x, y, h), g in zip(labels, grps) if g[0][1]]
            zoom = kws[-1] if kws else None
        plans.append(dict(a=a, b=b, d=d, f0=f0, keys=keys, s0=s0, push=R.choice([.02, .05, .03]),
                          drift=R.choice([40, 0, 60, 30]), rot=R.uniform(-2.5, 2.5), zoom=zoom))
    E, X = 470, 360
    for f in range(int(DUR * 15)):
        t = f / 15
        si = max(i for i, p in enumerate(plans) if p["a"] <= t + 1e-6)
        p = plans[si]
        u = t - p["a"]
        d = p["d"]
        # entry whip: arrive from -d*E, expo out over .45 s
        e = 0 if p.get("cine") else 1 - ease_out(min(1, u / .45), 4)
        fx, fy = p["f0"][0] - d[0] * E * e, p["f0"][1] - d[1] * E * e
        rot = p["rot"] + 4 * e * (1 if si % 2 else -1)
        s = p["s0"] * (1 + .06 * e)
        # tracking: ease towards each word's target as it lands
        cur = p["f0"]
        for tk, tgt in p["keys"]:
            if t >= tk:
                v = ease_out(min(1, (t - tk) / .3), 3)
                cur = (cur[0] + (tgt[0] - cur[0]) * v, cur[1] + (tgt[1] - cur[1]) * v)
        fx += cur[0] - p["f0"][0]
        fy += cur[1] - p["f0"][1]
        # drift and push-in while the line holds
        fx += d[0] * p["drift"] * u
        fy += d[1] * p["drift"] * u
        s *= 1 + p["push"] * u
        rot += .5 * u * (1 if si % 3 else -1)
        # exit: accelerate out along the next scene's direction (or zoom through the keyword)
        if si + 1 < len(plans) and not p.get("nozip"):
            w = p["b"] - t
            if w < .2:
                v = ((.2 - w) / .2) ** 2
                if p["zoom"]:
                    zx, zy = p["zoom"]
                    fx, fy = fx + (zx - fx) * v, fy + (zy - fy) * v
                    s *= 1 + 1.8 * v
                else:
                    nd = plans[si + 1]["d"]
                    nn = math.hypot(*nd)
                    fx += nd[0] / nn * X * v
                    fy += nd[1] / nn * X * v
                    rot += 3 * v * (1 if si % 2 else -1)
        js(f'tl.set("#pan", {{x: {540 - fx:.1f}, y: {960 - fy:.1f}}}, {t:.3f});')
        js(f'tl.set("#cam", {{scale: {s:.4f}, rotation: {rot:.2f}}}, {t:.3f});')


# ---------------------------------------------------------------------------------------------------- layers
def card_track():
    """The footage card (and the red torn shape behind it) re-laid out on every scene; hidden in type-only scenes."""
    for i, (a, b, li) in enumerate(scenes()):
        card = None if li < 0 or li in CINE or li in GRID else layout(li)[0]
        if card is None:
            js(f'tl.set(["#cardw", "#redp"], {{opacity: 0}}, {a:.3f});')
            continue
        x, y, w, h = card
        full = w > 1100
        rot = R.uniform(-2.5, 2.5)
        clip = torn(w, h, 0 if full else 14, seed=i)
        js(f'tl.set("#cardw", {{opacity: 1}}, {a:.3f});')
        js(f'tl.set("#card", {{left: {x}, top: {y}, width: {w}, height: {h}, rotation: {rot:.2f}, clipPath: "{clip}"}}, {a:.3f});')
        js(f'tl.set("#tint", {{opacity: {.85 if (i % 4 == 2 and not full) else 0}}}, {a:.3f});')
        if not full:
            js(f'tl.set("#redp", {{attr: {{d: "{blob_path(x + w * R.uniform(.3, .7), y + h * R.uniform(.3, .7), w * .58, h * .45, i)}"}}, opacity: 1}}, {a:.3f});')
        else:
            js(f'tl.set("#redp", {{opacity: 0}}, {a:.3f});')
    for bt in BEATS["beats"]:
        if bt < DUR - .2 and all(abs(bt - s[0]) > .1 for s in scenes()):
            js(f'tl.fromTo("#card", {{scale: 1.035}}, {{scale: 1, duration: .067, ease: "steps(1)", immediateRender: false}}, {bt:.3f});')


def scene_builds():
    """Texture panels, stills, a prop and stars, built up on the half beats in each scene; all clear at the cut."""
    html = "".join(f'<i class="pnl" id="pn{k}"></i>' for k in range(NPNL))
    html += "".join(f'<svg class="star" id="sr{k}" viewBox="-50 -50 100 100"><path d="{star_path()}"/></svg>' for k in range(3))
    bars = "".join(f'<rect x="{x}" y="0" width="{w}" height="60"/>' for x, w in zip(range(0, 230, 9), [3, 5, 2, 7, 3, 2, 6, 3, 4, 2, 5, 3, 7, 2, 3, 6, 2, 4, 3, 5, 2, 6, 3, 2, 5, 3]))
    html += (f'<div class="prop tick" id="tick" data-layout-ignore><svg viewBox="0 0 232 60" width="232" height="60">{bars}</svg>'
             '<div><b>ASHKE</b><small>KARAN AUJLA &#183; MXRCI &#183; 0214-0314</small></div></div>')
    html += ('<div class="prop" id="arrow"><svg viewBox="-50 -50 100 100" width="220" height="220"><circle r="46" fill="#f4f2ec" stroke="#141414" stroke-width="7"/>'
             '<path d="M-24 18 L14 -20 L2 -20 L2 -30 L30 -30 L30 -2 L20 -2 L20 -14 L-18 24 Z" fill="#141414"/></svg></div>')
    html += "".join(f'<svg class="prop bstb" id="bst{k}" viewBox="-50 -50 100 100"><path d="{burst_path(90 + k, 11)}"/></svg>' for k in range(2))
    HIDE.extend([f"#pn{k}" for k in range(NPNL)] + [f"#sr{k}" for k in range(3)] + ["#tick", "#arrow", "#bst0", "#bst1"])
    sk = 0
    for si, (a, b, li) in enumerate(scenes()):
        allx = [f"#pn{k}" for k in range(NPNL)] + [f"#sr{k}" for k in range(3)] + ["#tick", "#arrow", "#bst0", "#bst1"]
        js(f'tl.set({json.dumps(allx)}, {{opacity: 0}}, {a:.3f});')
        if li < 0 or li in CINE or li in GRID:
            continue
        card, labels, _ = layout(li)
        ly0 = labels[0][1] if labels else 900
        ly1 = labels[-1][1] + labels[-1][2] if labels else 1100
        if card:
            cx, cy, cw, ch = card
            slots = [(cx + R.choice([-60, cw - 480]), cy + ch * .3, 540, ch * .85, R.uniform(-4, 4)),     # behind the card
                     (R.choice([-60, 900]), min(ly0, cy) - 120, 240, 2100, 0),                          # edge strip
                     (-30, ly0 - 70, 1140, 120, R.uniform(-3, 3)),                                       # band over the lyrics
                     (cx + cw - 150, cy - 70, 250, 250, R.uniform(-10, 10)),                             # corner square
                     (-30, ly1 + 20, 1140, 170, R.uniform(-3, 3)),                                       # band under the lyrics
                     (40, cy + ch - 120, 320, 220, R.uniform(-6, 6))]                                    # lower corner
        else:
            slots = [(-60, ly0 - 200, 260, 2000, 0), (880, ly0 - 300, 260, 2100, 0),
                     (-30, ly0 - 120, 1140, 110, R.uniform(-3, 3)), (700, ly1 + 10, 360, 300, R.uniform(-8, 8)),
                     (-30, ly1 + 160, 1140, 160, R.uniform(-3, 3)), (60, ly0 + 300, 280, 280, R.uniform(-8, 8))]
        texs = R.sample(TEX, NPNL)
        t = a
        for k, (x, y, w, h, rot) in enumerate(slots):
            when = a if k < 2 else t
            t += PERIOD / 2 if k >= 1 else 0
            if when >= b - .1:
                continue
            clip = "none" if k != 0 else R.choice(["none", "polygon(7% 0, 100% 0, 93% 100%, 0 100%)"])
            js(f'tl.set("#pn{k}", {{opacity: 1, left: {x:.0f}, top: {y:.0f}, width: {w:.0f}, height: {h:.0f}, rotation: {rot:.1f}, '
               f'className: "pnl {texs[k]}", clipPath: "{clip}"}}, {when:.3f});')
            js(f'tl.fromTo("#pn{k}", {{x: {R.choice([-160, 160])}}}, {{x: 0, duration: .067, ease: "steps(1)", immediateRender: false}}, {when:.3f});')
        # stills: one or two, on the side away from the zigzag, a beat in
        for j in range(2 if b - a > 2 else 1):
            ts = a + PERIOD * (1 + j * 1.5)
            if ts >= b - .25:
                break
            sid = f"#st{sk}"
            sx = R.choice([-30, 760])
            sy = R.randint(int(ly0), int(max(ly0 + 1, ly1 - 150)))
            html += (f'<div class="still" id="st{sk}" style="left:{sx}px;top:{sy}px;transform:rotate({R.uniform(-9, 9):.1f}deg)">'
                     f'<img src="assets/img/stills/s{sk % 20:02d}.jpg" alt=""></div>')
            HIDE.append(sid)
            js(f'tl.set("{sid}", {{opacity: 1}}, {ts:.3f});')
            js(f'tl.set("{sid}", {{opacity: 0}}, {b:.3f});')
            js(f'tl.fromTo("{sid}", {{x: {R.choice([-300, 300])}}}, {{x: 0, duration: .1, ease: "steps(2)", immediateRender: false}}, {ts:.3f});')
            sk += 1
        prop = ["#tick", "#arrow", "#bst0", "#tick", "#bst1", "#arrow"][si % 6]
        tp = a + PERIOD * R.choice([1, 2])
        if tp < b - .2:
            px = R.choice([30, 640]) if prop == "#tick" else R.choice([20, 840])
            py = R.choice([ly0 - 260, ly1 + 40])
            js(f'tl.set("{prop}", {{opacity: 1, left: {px}, top: {py:.0f}, rotation: {R.randint(-14, 14)}}}, {tp:.3f});')
            js(f'tl.fromTo("{prop}", {{scale: 1.5}}, {{scale: 1, duration: .067, ease: "steps(1)", immediateRender: false}}, {tp:.3f});')
        for k in range(2):
            ts = a + PERIOD * (.5 + k)
            if ts < b - .15:
                js(f'tl.set("#sr{k}", {{opacity: 1, left: {R.choice([40, 900])}, top: {R.randint(int(ly0) - 300, int(ly1) + 200)}, '
                   f'width: {R.choice([90, 130])}, height: {R.choice([90, 130])}, rotation: {R.randint(0, 60)}}}, {ts:.3f});')
                js(f'tl.fromTo("#sr{k}", {{scale: 0}}, {{scale: 1, duration: .067, ease: "steps(1)", immediateRender: false}}, {ts:.3f});')
    js('tl.to("#arrow svg", {rotation: 720, duration: 60, ease: "steps(240)"}, 0);')
    return html


def labels():
    """Tape labels at their own place on the page (the camera tracks them); slam in on the sung word."""
    out = []
    styles = ["blk", "wht", "red", "blk", "wht", "wht"]
    for li, (i0, i1, text, side) in enumerate(LYRICS):
        a, b = line_times(li)
        _, pos, grps = layout(li)
        rows = []
        for gi, (grp, (x, y, h)) in enumerate(zip(grps, pos)):
            key = grp[0][1]
            txt = " ".join(w[0] for w in grp)
            lid = f"lb{li}_{gi}"
            rot = R.uniform(-5, 5)
            big = " big" if side == "full" else ""
            if key and gi % 2:
                inner = f'<div class="lb kw kwr{big}" id="{lid}">{txt}{CIRC}</div>'
            elif key:
                bst = f'<svg class="bst" viewBox="-50 -50 100 100" preserveAspectRatio="none"><path d="{burst_path(li * 7 + gi)}"/></svg>'
                inner = f'<div class="lb kw{big}" id="{lid}">{bst}<span>{txt}</span>{CIRC}</div>'
            else:
                inner = f'<div class="lb {styles[(li + gi) % len(styles)]}{big}" id="{lid}">{txt}</div>'
            rows.append(f'<div class="lw" style="left:{x}px;top:{y}px;transform:rotate({rot:.1f}deg)">{inner}</div>')
            HIDE.append(f"#{lid}")
            t = grp[0][2]
            js(f'tl.set("#{lid}", {{opacity: 1}}, {t:.3f});')
            if key:
                js(f'tl.fromTo("#{lid}", {{scale: 1.7}}, {{scale: 1, duration: .1, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
                js(f'tl.fromTo("#{lid} .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .2, ease: "steps(3)", immediateRender: false}}, {t + .1:.3f});')
            else:
                js(f'tl.fromTo("#{lid}", {{x: {R.choice([-560, 560])}}}, {{x: 0, duration: .1, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
        out.append(f'<div class="stack" id="sk{li}">{"".join(rows)}</div>')
        HIDE.append(f"#sk{li}")
        js(f'tl.set("#sk{li}", {{opacity: 1}}, {a:.3f});')
        if b < DUR:
            js(f'tl.set("#sk{li}", {{opacity: 0}}, {b:.3f});')
    return "".join(out)


def in_cine(t):
    return any(a <= t < b and (li < 0 or li in CINE) for a, b, li in scenes())


def cine_spans():
    """Merged [a, b) spans where the cinema layer owns the screen, with the scene index that ends each span."""
    spans = []
    for a, b, li in scenes():
        if li < 0 or li in CINE:
            if spans and abs(spans[-1][1] - a) < 1e-6:
                spans[-1] = (spans[-1][0], b, li)
            else:
                spans.append((a, b, li))
    return spans


def cinema():
    """The eimantasbitinas23 layer: graded full-bleed footage with handheld drift, glass shards, torn slivers, a red
    picture-in-picture still, torn paper rips back into the collage. Returns (html inside the camera, screen html)."""
    g = random.Random(77)
    shard_pts = ["0,0 60,8 34,90", "0,10 80,0 70,40 10,60", "20,0 44,4 40,120 0,110", "0,0 120,20 100,34", "10,0 30,0 26,70 0,74", "0,30 90,0 60,60"]
    pan = '<div id="cine"><video id="cinev" class="clip" src="assets/video/cine.mp4" data-start="0" data-duration="60" data-track-index="2" muted playsinline></video>'
    for k, pts in enumerate(shard_pts):
        col = ["rgba(10,12,10,.85)", "rgba(40,190,90,.55)", "rgba(10,12,10,.7)"][k % 3]
        pan += f'<svg class="shard" id="sh{k}" viewBox="0 0 130 130"><polygon points="{pts}" fill="{col}" stroke="rgba(255,255,255,.5)" stroke-width="1.5"/></svg>'
    for k in range(3):
        pan += f'<i class="sliver" id="sv{k}" style="clip-path:{torn(60, 400, 26, 300 + k)}"></i>'
    pan += ('<div id="pip"><img id="pipa" src="assets/img/stills/s03.jpg" alt=""><img id="pipb" src="assets/img/stills/s11.jpg" alt=""><i></i></div>')
    HIDE.extend(["#cine", "#pip"] + [f"#sh{k}" for k in range(len(shard_pts))] + [f"#sv{k}" for k in range(3)])
    screen = '<div id="scan"></div>'
    HIDE.append("#scan")
    spans = cine_spans()
    rk = 0
    for a, b, li_end in spans:
        js(f'tl.set("#cine", {{opacity: 1}}, {a:.3f});')
        if b < DUR:
            js(f'tl.set("#cine", {{opacity: 0}}, {b:.3f});')
        js(f'tl.fromTo("#cinev", {{scale: 1}}, {{scale: 1.07, duration: {b - a:.3f}, ease: "none", immediateRender: false}}, {a:.3f});')
        # handheld drift at the full frame rate (the collage is stepped, the cinema is smooth)
        ph = g.uniform(0, 6)
        f = round(a * 30)
        while f < round(b * 30):
            t = f / 30
            js(f'tl.set("#cinev", {{x: {math.sin(t * 2.1 + ph) * 7 + g.uniform(-1.5, 1.5):.1f}, y: {math.cos(t * 1.7 + ph) * 9 + g.uniform(-1.5, 1.5):.1f}}}, {t:.3f});')
            f += 1
        # shards and slivers flicker every second frame
        f = round(a * 15)
        while f < round(b * 15):
            t = f / 15
            for k in range(len(shard_pts)):
                if g.random() < .3:
                    js(f'tl.set("#sh{k}", {{opacity: 1, left: {g.randint(-40, 1000)}, top: {g.randint(80, 1800)}, rotation: {g.randint(0, 360)}, scale: {g.uniform(.6, 1.8):.2f}}}, {t:.3f});')
                else:
                    js(f'tl.set("#sh{k}", {{opacity: 0}}, {t:.3f});')
            for k in range(3):
                if g.random() < .22:
                    js(f'tl.set("#sv{k}", {{opacity: 1, left: {g.randint(200, 840)}, top: {g.randint(500, 1500)}, rotation: {g.randint(-40, 40)}, scaleY: {g.uniform(.5, 1.3):.2f}}}, {t:.3f});')
                else:
                    js(f'tl.set("#sv{k}", {{opacity: 0}}, {t:.3f});')
            f += 1
        js(f'tl.set({json.dumps([f"#sh{k}" for k in range(len(shard_pts))] + [f"#sv{k}" for k in range(3)])}, {{opacity: 0}}, {b - .001:.3f});')
        # torn paper rip back into the collage (when the span does not end on a zoom-through)
        zoom_exit = li_end >= 0 and LYRICS[li_end][3] == "full" and li_end < len(LYRICS) - 2
        if b < DUR - .1 and not zoom_exit:
            rid = f"rp{rk}"
            pan += (f'<div class="rip" id="{rid}" style="clip-path:{torn(700, 900, 40, 700 + rk)}">'
                    f'<img src="assets/img/stills/s{(rk * 7 + 4) % 20:02d}.jpg" alt=""></div>')
            HIDE.append(f"#{rid}")
            for j, sc in enumerate([.45, .8, 1.3]):
                js(f'tl.set("#{rid}", {{opacity: 1, scale: {sc}, rotation: {(-6, 3, -2)[j]}}}, {b - .27 + j * .09:.3f});')
            js(f'tl.set("#{rid}", {{opacity: 0}}, {b:.3f});')
            rk += 1
    # red picture-in-picture still in the hit-line holds, swapping every 4 frames
    for li in CARDS:
        a, b = line_times(li)
        js(f'tl.set("#pip", {{opacity: 1}}, {a + .9:.3f});')
        js(f'tl.set("#pip", {{opacity: 0}}, {b - .3:.3f});')
        t, k = a + .9, 0
        while t < b - .3:
            js(f'tl.set("#pipa", {{opacity: {k % 2}}}, {t:.3f});')
            t, k = t + 4 / 30, k + 1
    # VHS scan line: mostly in the cinema, now and then over the collage
    f = 0
    while f < DUR * 15:
        t = f / 15
        p = .32 if in_cine(t) else .05
        if g.random() < p:
            js(f'tl.set("#scan", {{opacity: 1, left: {g.randint(40, 1040)}, scaleX: {g.choice([1, 1, 2])}}}, {t:.3f});')
        else:
            js(f'tl.set("#scan", {{opacity: 0}}, {t:.3f});')
        f += 1
    # black title cards before the hits (card, footage flash, card), and "karan aujla" out of the intro
    k = 0
    for li, txt in CARDS.items():
        a = line_times(li)[0]
        screen += f'<div class="bcard" id="bc{k}"><b>{"<br>".join(txt.split(chr(10)))}</b></div>'
        HIDE.append(f"#bc{k}")
        for t0 in (a, a + .4):
            js(f'tl.set("#bc{k}", {{opacity: 1}}, {t0:.3f});')
            js(f'tl.set("#bc{k}", {{opacity: 0}}, {t0 + .2:.3f});')
        k += 1
    screen += f'<div class="bcard low" id="bc{k}"><b>karan aujla</b></div>'
    HIDE.append(f"#bc{k}")
    a0 = line_times(0)[0]
    js(f'tl.set("#bc{k}", {{opacity: 1}}, {a0 - .3:.3f});')
    js(f'tl.set("#bc{k}", {{opacity: 0}}, {a0:.3f});')
    # red iris closing into the red segment (JATT KHULLA GHUMMDA)
    a12 = line_times(12)[0]
    screen += '<div id="iris"></div>'
    HIDE.append("#iris")
    js(f'tl.set("#iris", {{opacity: 1}}, {a12 - .3:.3f});')
    js(f'tl.fromTo("#iris", {{scale: 15}}, {{scale: 0, duration: .3, ease: "steps(4)", immediateRender: false}}, {a12 - .3:.3f});')
    js(f'tl.set("#iris", {{opacity: 0}}, {a12 + .067:.3f});')
    return pan + '</div>', screen


def photo_grid():
    """The reference's photo cluster on white paper: colour stills torn to size, two of them stop-motion (a new
    picture every second frame); the camera holds still while the line is sung under it."""
    html = ""
    tiles = [(150, 290, 420, 300), (530, 330, 410, 320), (110, 560, 360, 300), (440, 610, 290, 250), (700, 630, 300, 290),
             (120, 880, 430, 320), (570, 910, 380, 300)]
    for n, li in enumerate(sorted(GRID)):
        a, b = line_times(li)
        gid = f"pg{n}"
        inner = ""
        for k, (x, y, w, h) in enumerate(tiles):
            if k in (2, 5):
                imgs = "".join(f'<img class="fr" id="{gid}t{k}f{j}" src="assets/img/stills/c{(n * 5 + k + j * 3) % 14:02d}.jpg" alt="">' for j in range(3))
                f, j = round(a * 15), 0
                while f < round(b * 15):
                    for q in range(3):
                        js(f'tl.set("#{gid}t{k}f{q}", {{opacity: {1 if q == j % 3 else 0}}}, {f / 15:.3f});')
                    f, j = f + 1, j + 1
            else:
                imgs = f'<img src="assets/img/stills/c{(n * 5 + k) % 14:02d}.jpg" alt="">'
            inner += f'<div class="tile" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;clip-path:{torn(w, h, 6, 900 + n * 10 + k)}">{imgs}</div>'
        html += f'<div class="pgrid" id="{gid}">{inner}</div>'
        HIDE.append(f"#{gid}")
        js(f'tl.set("#{gid}", {{opacity: 1}}, {a:.3f});')
        js(f'tl.set("#{gid}", {{opacity: 0}}, {b:.3f});')
    return html


def velocity():
    """Velocity strips across the screen (screen space, over the camera): every four beats, every beat in the bursts."""
    html = "".join(f'<div class="vs" id="vs{k}"><b>{"ASHKE &#9679; KARAN AUJLA &#9679; MXRCI &#9679; " * 6}</b></div>' for k in range(2))
    HIDE.extend(["#vs0", "#vs1"])
    times = []
    for i, bt in enumerate(b for b in BEATS["beats"] if 2.2 < b < 57.5):
        if i % 4 == 2 and not in_cine(bt):
            times.append(bt)
    kinds = ["hz", "type", "dots", "blocks", "type", "lines", "hz2", "news"]
    for n, t in enumerate(times):
        vid = f"#vs{n % 2}"
        d = 1 if n % 2 == 0 else -1
        h = R.choice([80, 110, 140])
        y = R.choice([R.randint(120, 420), R.randint(1500, 1760 - h)])
        rot = R.uniform(-8, 8)
        js(f'tl.set("{vid}", {{opacity: 1, top: {y}, height: {h}, rotation: {rot:.1f}, className: "vs {kinds[n % len(kinds)]}"}}, {t:.3f});')
        js(f'tl.fromTo("{vid}", {{x: {-2700 if d > 0 else 1100}}}, {{x: {1100 if d > 0 else -2700}, duration: .3, ease: "steps(5)", immediateRender: false}}, {t:.3f});')
        js(f'tl.set("{vid}", {{opacity: 0}}, {t + .3:.3f});')
    return html


def flashes():
    """The reference's cut accents: mostly clean whip cuts; now and then a white or near-black frame, red into hits."""
    for li in range(1, len(LYRICS)):
        a = line_times(li)[0]
        kind = ["", "", "flash", "", "dark", "", "", "flash", "", "dark"][li % 10]
        if LYRICS[li][3] == "full":
            kind = "red"
        if kind == "flash":
            js(f'tl.set("#flash", {{opacity: .9}}, {a:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {a + .067:.3f});')
        elif kind == "dark":
            js(f'tl.set("#dark", {{opacity: .75}}, {a:.3f});')
            js(f'tl.set("#dark", {{opacity: 0}}, {a + .067:.3f});')
        elif kind == "red":
            js(f'tl.set("#redflash", {{opacity: 1}}, {a - .067:.3f});')
            js(f'tl.set("#redflash", {{opacity: 0}}, {a + .033:.3f});')
    g = random.Random(5)
    for f in range(int(DUR * 15)):
        t = f / 15
        hit = any(0 <= t - bt < .07 for bt in BEATS["beats"])
        amp = 7 if hit else 1.2
        js(f'tl.set("#collage", {{x: {g.uniform(-amp, amp):.1f}, y: {g.uniform(-amp, amp):.1f}}}, {t:.3f});')
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {t:.3f});')


def titles():
    """ASHKE circled + KARAN AUJLA · MXRCI: opens the edit and lands on "Ashke" at the end (screen space)."""
    t = W[153]["s"]
    a0 = line_times(0)[0]
    HIDE.extend(["#endt", "#endk", "#opt", "#opk"])
    js(f'tl.set("#endt", {{opacity: 1}}, {t:.3f});')
    js(f'tl.set("#sk{len(LYRICS) - 2}", {{opacity: 0}}, {t:.3f});')        # the title card replaces the line's labels
    js(f'tl.fromTo("#endt", {{scale: 2.2, rotation: -8}}, {{scale: 1, rotation: -3, duration: .14, ease: "steps(4)", immediateRender: false}}, {t:.3f});')
    js(f'tl.fromTo("#endt .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .4, ease: "power2.out", immediateRender: false}}, {t + .2:.3f});')
    js(f'tl.set("#endk", {{opacity: 1}}, {t + .45:.3f});')
    js(f'tl.fromTo("#endk", {{x: -120}}, {{x: 0, duration: .1, ease: "steps(3)", immediateRender: false}}, {t + .45:.3f});')
    js('tl.set("#opt", {opacity: 1}, .15);')
    js('tl.fromTo("#opt", {scale: 2.2, rotation: -8}, {scale: 1, rotation: -3, duration: .14, ease: "steps(4)", immediateRender: false}, .15);')
    js('tl.fromTo("#opt .circ path", {strokeDashoffset: 400}, {strokeDashoffset: 0, duration: .4, ease: "power2.out", immediateRender: false}, .45);')
    js('tl.set("#opk", {opacity: 1}, .6);')
    js('tl.fromTo("#opk", {x: -120}, {x: 0, duration: .1, ease: "steps(3)", immediateRender: false}, .6);')
    js(f'tl.set(["#opt", "#opk"], {{opacity: 0}}, {a0:.3f});')
    one = f'<span>ASHKE</span>{CIRC}'
    return (f'<div id="opt" class="lb kw end">{one}</div><div id="opk" class="lb blk endk">KARAN AUJLA · MXRCI</div>'
            f'<div id="endt" class="lb kw end">{one}</div><div id="endk" class="lb blk endk">KARAN AUJLA · MXRCI</div>')


CSS = f"""
@font-face {{ font-family: "Bebas Neue"; src: url("assets/fonts/BebasNeue/BebasNeue-400.ttf"); }}
@font-face {{ font-family: "Oswald"; font-weight: 700; src: url("assets/fonts/Oswald/Oswald-700.ttf"); }}
@font-face {{ font-family: "Inter Display"; font-weight: 500; src: url("assets/fonts/InterDisplay/InterDisplay-Medium.otf"); }}
@font-face {{ font-family: "Special Elite"; src: url("assets/fonts/SpecialElite/SpecialElite-400.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {PAPER}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: {PAPER}; }}
#cam {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; transform-origin: 540px 960px; }}
#pan {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; }}
#paper {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; background: url(assets/img/paper.png); }}
#grid {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; pointer-events: none; opacity: .5; }}
#grid line {{ stroke: #3b3835; stroke-width: 1.4; }}
#collage {{ position: absolute; inset: 0; }}
#redsvg {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; overflow: visible; }}
#redp {{ fill: {RED}; filter: drop-shadow(8px 8px 0 {INK}); }}
#cardw {{ position: absolute; inset: 0; filter: drop-shadow(12px 12px 0 {INK}); }}
#card {{ position: absolute; left: 60px; top: 190px; width: 960px; height: 800px; overflow: hidden; background: #111; }}
#card video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#tint {{ position: absolute; inset: 0; background: {RED}; mix-blend-mode: multiply; opacity: 0; }}
.still {{ position: absolute; width: 330px; height: 230px; overflow: hidden; border: 9px solid #f4f2ec; box-shadow: 9px 9px 0 {INK}; z-index: 2; }}
.still img {{ width: 100%; height: 100%; object-fit: cover; }}
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
.prop {{ position: absolute; left: 0; top: 0; opacity: 0; z-index: 3; }}
.tick {{ display: flex; gap: 18px; align-items: center; padding: 16px 26px; background: #f4f2ec; border: 4px solid {INK}; box-shadow: 10px 10px 0 {INK}; }}
.tick svg rect {{ fill: {INK}; }}
.tick b {{ display: block; font: 700 64px/1 "Oswald"; color: {INK}; letter-spacing: 1px; }}
.tick small {{ display: block; font: 400 17px/1.2 "Special Elite"; color: {INK}; margin-top: 4px; }}
.bstb {{ width: 280px; height: 280px; overflow: visible; }}
.bstb path {{ fill: {INK}; }}
.star {{ position: absolute; left: 0; top: 0; opacity: 0; fill: {INK}; z-index: 3; }}
#lyrics {{ position: absolute; inset: 0; z-index: 5; pointer-events: none; }}
.stack {{ position: absolute; inset: 0; opacity: 0; }}
.lw {{ position: absolute; width: 0; display: flex; justify-content: center; transform-origin: 0 50%; }}
.lb {{ position: relative; display: inline-block; font: 400 100px/1 "Bebas Neue"; letter-spacing: 1px; padding: 10px 26px 4px; white-space: nowrap; filter: url(#rough); }}
.lb.blk {{ background: {INK}; color: {PAPER}; }}
.lb.wht {{ background: #f7f5f0; color: {INK}; box-shadow: 8px 8px 0 {INK}; }}
.lb.red {{ background: {RED}; color: #fff; }}
.lb.big {{ font-size: 120px; }}
.lb.kw {{ font: 700 170px/.9 "Oswald"; text-transform: uppercase; color: #d11a22; letter-spacing: -2px; padding: 0 30px; text-shadow: 7px 7px 0 {INK}, -1px -1px 0 {INK}; }}
.lb.kw.big {{ font-size: 220px; }}
.lb.kw span {{ position: relative; }}
.bst {{ position: absolute; left: -14%; top: -40%; width: 128%; height: 180%; z-index: -1; overflow: visible; }}
.bst path {{ fill: #f7f5f0; stroke: {INK}; stroke-width: 2.4; vector-effect: non-scaling-stroke; }}
.lb.kw.kwr {{ background: {RED}; color: #fff; text-shadow: none; padding: 8px 34px 0; }}
.circ {{ position: absolute; left: -12%; top: -24%; width: 124%; height: 148%; overflow: visible; pointer-events: none; }}
.circ path {{ fill: none; stroke: {BLUE}; stroke-width: 5; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
.vs {{ position: absolute; left: 0; top: 0; width: 2600px; height: 120px; z-index: 6; opacity: 0; overflow: hidden; box-shadow: 0 8px 0 {INK}; }}
.vs b {{ display: none; }}
.vs.type {{ background: {INK}; }}
.vs.type b {{ display: block; white-space: nowrap; font: 400 110px/1 "Bebas Neue"; color: #f4f2ec; letter-spacing: 4px; padding-top: 6px; }}
#cine {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; overflow: hidden; background: #000; opacity: 0; }}
#cinev {{ position: absolute; left: -20px; top: -30px; width: 1120px; height: 1980px; object-fit: cover; }}
.shard {{ position: absolute; left: 0; top: 0; width: 130px; height: 130px; opacity: 0; overflow: visible; }}
.sliver {{ position: absolute; left: 0; top: 0; width: 60px; height: 400px; background: #f4f2ec; opacity: 0; filter: drop-shadow(3px 0 0 #111); }}
#pip {{ position: absolute; left: 60px; top: 300px; width: 330px; height: 210px; overflow: hidden; opacity: 0; }}
#pip img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: grayscale(1) contrast(1.4); }}
#pip i {{ position: absolute; inset: 0; background: #e01818; mix-blend-mode: multiply; }}
.rip {{ position: absolute; left: 190px; top: 510px; width: 700px; height: 900px; background: #f4f2ec; padding: 34px; opacity: 0; }}
.rip img {{ width: 100%; height: 100%; object-fit: cover; }}
.pgrid {{ position: absolute; left: -200px; top: -200px; width: 1480px; height: 2320px; background: #ecebe8; opacity: 0; }}
.tile {{ position: absolute; overflow: hidden; background: #111; margin: 200px 0 0 200px; }}
.tile img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#scan {{ position: absolute; left: 0; top: 0; width: 12px; height: {FH}px; z-index: 8; opacity: 0;
  background: repeating-linear-gradient(0deg, #fff 0 3px, #9fe 3px 5px, #222 5px 7px, #fff 7px 12px, #6cf 12px 13px); }}
.bcard {{ position: absolute; inset: 0; z-index: 8; background: #050505; opacity: 0; display: flex; align-items: center; justify-content: center; }}
.bcard b {{ font: 500 132px/1.06 "Inter Display"; color: #f1f1f1; text-align: center; letter-spacing: -1px; }}
.bcard.low b {{ font-size: 92px; letter-spacing: 0; }}
#iris {{ position: absolute; left: 440px; top: 860px; width: 200px; height: 200px; border-radius: 50%; z-index: 8; opacity: 0;
  box-shadow: 0 0 0 4000px {RED}, inset 0 0 30px 10px rgba(0,0,0,.45); }}
#flash {{ position: absolute; inset: 0; z-index: 9; background: #fff; opacity: 0; }}
#dark {{ position: absolute; inset: 0; z-index: 9; background: #111; opacity: 0; }}
#redflash {{ position: absolute; inset: 0; z-index: 9; background: {RED}; opacity: 0; mix-blend-mode: multiply; }}
#vig {{ position: absolute; inset: 0; z-index: 11; pointer-events: none; background: radial-gradient(ellipse 85% 80% at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,.16) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1120px; height: 1960px; z-index: 12; pointer-events: none; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
#opt, #endt {{ position: absolute; left: 0; right: 0; top: 640px; margin: 0 auto; width: fit-content; z-index: 7; opacity: 0; font-size: 250px; }}
#opk, #endk {{ position: absolute; left: 0; right: 0; top: 1000px; margin: 0 auto; width: fit-content; z-index: 7; opacity: 0; font-size: 76px; }}
"""


def main():
    card_track()
    sc = scene_builds()
    lb = labels()
    vel = velocity()
    cpan, cscreen = cinema()
    pg = photo_grid()
    flashes()
    camera()
    tt = titles()
    gl = random.Random(4)
    grid = "".join(f'<line x1="{x + gl.uniform(-8, 8):.0f}" y1="-20" x2="{x + gl.uniform(-30, 30):.0f}" y2="3920"/>' for x in range(150, 2600, 250)) + \
           "".join(f'<line x1="-20" y1="{y + gl.uniform(-8, 8):.0f}" x2="2620" y2="{y + gl.uniform(-25, 25):.0f}"/>' for y in range(140, 3900, 260))
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Ashke collage lyric edit 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{FW}" data-height="{FH}">
      <div id="cam"><div id="pan">
        <div id="paper"></div>
        <svg id="grid" viewBox="0 0 2600 3900">{grid}</svg>
        <div id="collage">
          {sc}
          {pg}
          <svg id="redsvg" viewBox="0 0 {FW} {FH}"><path id="redp" d="M0 0"/></svg>
          <div id="cardw"><div id="card"><video id="vid" class="clip" src="assets/video/bw_main.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" muted playsinline></video><i id="tint"></i></div></div>
        </div>
        {cpan}
        <div id="lyrics" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{lb}</div>
      </div></div>
      {vel}
      {cscreen}
      {tt}
      <div id="flash"></div>
      <div id="dark"></div>
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
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(LYRICS)} lines, {len(scenes())} scenes")


if __name__ == "__main__":
    main()
