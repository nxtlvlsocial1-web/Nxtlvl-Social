"""Ashke (Karan Aujla, Mxrci) lyric edit, 16:9, 60 s from 2:14 of the song: writes index.html.

python3 build/generate.py      (from the project root; after build/paper.py, build/footage.py and build/audio.py)

A fusion of the music video with the owner's collage reference (YouMotion paper-zine lyric edit): the video, cut on the
beat and photocopied in black and white (assets/video/bw_main.mp4), sits in torn paper cards that jump to a new size,
tilt and torn edge on every cut, over red torn shapes, on crumpled paper with window-blind shadows and a hand-drawn
grid. Lyrics are stacked tape labels (black, white, red) in condensed type that snap in on their sung word; keywords
are huge distressed red letters circled in blue; a small typewriter caption repeats the line. Black stars, torn paper
edges, photocopied stills as secondary cards, paper-tear wipes and red flashes; hit lines go full-bleed.
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
A, HIDE = [], []
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


def card_track():
    """On every cut (and every new lyric line) the photo card jumps to a new size, tilt and torn edge; sometimes it
    turns red (multiply)."""
    starts = sorted(set([s["a"] for s in SHOTS] + [round(line_times(li)[0], 3) for li in range(len(LYRICS))]))
    for i, t in enumerate(starts):
        side = side_at(t + .01)
        x, y, w, h, rot = R.choice(CARD[side])
        rot += R.uniform(-1.2, 1.2)
        clip = torn(w, h, 14 if side != "full" else 0, seed=i)
        js(f'tl.set("#card", {{left: {x}, top: {y}, width: {w}, height: {h}, rotation: {rot:.2f}, clipPath: "{clip}"}}, {t:.3f});')
        js(f'tl.fromTo("#card", {{scale: 1.07}}, {{scale: 1, duration: .16, ease: "power3.out", immediateRender: false}}, {t:.3f});')
        js(f'tl.set("#tint", {{opacity: {.85 if (i % 5 == 2 and side != "full") else 0}}}, {t:.3f});')
        # the red torn shape behind the card
        if side != "full":
            cx = x + w * R.uniform(.25, .75)
            cy = y + h * R.uniform(.3, .8)
            js(f'tl.set("#redp", {{attr: {{d: "{blob_path(cx, cy, w * .55, h * .38, i)}"}}, opacity: 1}}, {t:.3f});')
        else:
            js(f'tl.set("#redp", {{opacity: 0}}, {t:.3f});')


def still_cards():
    """Photocopied stills as secondary cards on the lyric side, swapping every couple of beats."""
    html = ""
    t, k = line_times(0)[0], 0
    while t < 57.0:
        side = side_at(t + .01)
        if side != "full":
            sid = f"st{k}"
            x = 1240 if side == "l" else 160
            y = R.choice([60, 640])
            rot = R.uniform(-8, 8)
            html += (f'<div class="still" id="{sid}" style="left:{x}px;top:{y}px;transform:rotate({rot:.1f}deg);'
                     f'clip-path:{torn(300, 210, 8, k + 500)}"><img src="assets/img/stills/s{k % 20:02d}.jpg" alt=""></div>')
            HIDE.append(f"#{sid}")
            js(f'tl.set("#{sid}", {{opacity: 1}}, {t:.3f});')
            js(f'tl.fromTo("#{sid}", {{x: {R.choice([-60, 60])}, scale: 1.1}}, {{x: 0, scale: 1, duration: .12, ease: "power3.out", immediateRender: false}}, {t:.3f});')
            js(f'tl.set("#{sid}", {{opacity: 0}}, {t + 1.3:.3f});')
            k += 1
        t += 1.35
    return html


def labels():
    """Each lyric line as a stack of tape labels, snapping in on the sung word, keyword huge in red, circled in blue."""
    out = []
    styles = ["blk", "wht", "red", "blk", "bare", "wht"]
    for li, (i0, i1, text, side) in enumerate(LYRICS):
        a, b = line_times(li)
        ws = word_slots(li)
        # group connector words into labels of at most two words; keywords get their own
        if li == len(LYRICS) - 1:
            ws = []                     # the last line lives in the caption only: the title card owns the screen
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
                cls = "kw" + (" kwr" if gi % 2 else "")
                circ = (f'<svg class="circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path pathLength="400" '
                        f'd="M52 6 C95 4 104 90 50 95 S-6 12 60 9"/></svg>')
                rows.append(f'<div class="lb {cls}" id="{lid}" style="transform:translateX({dx}px) rotate({rot:.1f}deg)">{txt}{circ}</div>')
                js(f'tl.fromTo("#{lid} .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .3, ease: "power2.out", immediateRender: false}}, {grp[0][2] + .1:.3f});')
            else:
                st = styles[(li + gi) % len(styles)]
                rows.append(f'<div class="lb {st}" id="{lid}" style="transform:translateX({dx}px) rotate({rot:.1f}deg)">{txt}</div>')
            HIDE.append(f"#{lid}")
            t = grp[0][2]
            js(f'tl.set("#{lid}", {{opacity: 1}}, {t:.3f});')
            js(f'tl.fromTo("#{lid}", {{x: {R.choice([-90, 90])}, scale: 1.25}}, {{x: 0, scale: 1, duration: .1, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
        small = text.replace("*", "").lower()
        cap = f'<div class="cap8" style="{"left:1240px" if side == "l" else "left:180px" if side == "r" else "left:120px"}">{small}</div>'
        top = "full" if side == "full" else "side"
        out.append(f'<div class="stack {top}" id="sk{li}" style="left:{cx - 450}px">{"".join(rows)}</div>{cap.replace("cap8", f"cap8 cp{li}")}')
        HIDE.extend([f"#sk{li}", f".cp{li}"])
        js(f'tl.set("#sk{li}", {{opacity: 1}}, {a:.3f});')
        js(f'tl.set(".cp{li}", {{opacity: 1}}, {a + .1:.3f});')
        if b < DUR:
            js(f'tl.set("#sk{li}", {{opacity: 0}}, {b:.3f});')
            js(f'tl.set(".cp{li}", {{opacity: 0}}, {b:.3f});')
    return "".join(out)


def accents():
    """Black stars popping, the paper-tear wipe and red flashes on the line changes, stop-motion jitter."""
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
        js(f'tl.to("{sid}", {{scale: 1, duration: .1, ease: "steps(2)"}}, {t + .001:.3f});')
        js(f'tl.set("{sid}", {{opacity: 0}}, {t + 1.1:.3f});')
        t += R.choice([.674, 1.348])
        k += 1
    for li in range(1, len(LYRICS)):
        a = line_times(li)[0]
        kind = ["tear", "flash", "cut", "tear", "red", "cut"][li % 6]
        if LYRICS[li][3] == "full":
            kind = "red"
        if kind == "tear":
            d = R.choice([-1, 1])
            js(f'tl.fromTo("#tear", {{x: {-2400 * d}}}, {{x: {2400 * d}, duration: .3, ease: "power2.inOut", immediateRender: false}}, {a - .15:.3f});')
        elif kind == "flash":
            js(f'tl.set("#flash", {{opacity: .9}}, {a:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {a + .067:.3f});')
        elif kind == "red":
            js(f'tl.set("#redflash", {{opacity: 1}}, {a - .067:.3f});')
            js(f'tl.set("#redflash", {{opacity: 0}}, {a + .033:.3f});')
    # stop-motion boil: everything paper jitters a little at 12 fps, harder on the beats
    g = random.Random(5)
    for f in range(int(DUR * 12)):
        t = f / 12
        hit = any(0 <= t - bt < .09 for bt in BEATS["beats"])
        amp = 10 if hit else 2
        js(f'tl.set("#collage", {{x: {g.uniform(-amp, amp):.1f}, y: {g.uniform(-amp, amp):.1f}, rotation: {g.uniform(-.25, .25) * (3 if hit else 1):.2f}}}, {t:.3f});')
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
#redp {{ fill: {RED}; filter: drop-shadow(0 6px 10px rgba(0,0,0,.25)); }}
#cardw {{ position: absolute; inset: 0; filter: drop-shadow(0 14px 18px rgba(0,0,0,.4)); }}
#card {{ position: absolute; left: 110px; top: 120px; width: 780px; height: 840px; overflow: hidden; background: #111; }}
#card video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#tint {{ position: absolute; inset: 0; background: {RED}; mix-blend-mode: multiply; opacity: 0; }}
.still {{ position: absolute; width: 300px; height: 210px; overflow: hidden; filter: drop-shadow(0 8px 10px rgba(0,0,0,.35)); }}
.still img {{ width: 100%; height: 100%; object-fit: cover; }}
.edge {{ position: absolute; left: -40px; right: -40px; height: 90px; background: url(assets/img/paper.png) 0 0 / 1020px auto; filter: drop-shadow(0 4px 6px rgba(0,0,0,.3)); }}
.edge.top {{ top: -30px; clip-path: polygon({", ".join(f"{k * 100 / 40:.1f}% {random.Random(k).uniform(55, 100):.0f}%" for k in range(41))}, 100% 0, 0 0); }}
.edge.bot {{ bottom: -30px; clip-path: polygon({", ".join(f"{k * 100 / 40:.1f}% {random.Random(k + 77).uniform(0, 45):.0f}%" for k in range(41))}, 100% 100%, 0 100%); }}
#lyrics {{ position: absolute; inset: 0; z-index: 5; pointer-events: none; }}
.stack {{ position: absolute; top: 0; height: 1080px; width: 900px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; opacity: 0; }}
.lb {{ position: relative; display: inline-block; font: 400 96px/1 "Bebas Neue"; letter-spacing: 1px; padding: 10px 26px 4px; white-space: nowrap; filter: url(#rough); }}
.lb.blk {{ background: {INK}; color: {PAPER}; }}
.lb.wht {{ background: #f7f5f0; color: {INK}; box-shadow: 0 6px 12px rgba(0,0,0,.18); }}
.lb.red {{ background: {RED}; color: #fff; }}
.lb.bare {{ color: {INK}; font-size: 110px; padding: 0 10px; }}
.lb.kw {{ font: 700 190px/.9 "Oswald"; text-transform: uppercase; color: #d11a22; letter-spacing: -2px; padding: 0 30px; text-shadow: 7px 7px 0 #141414, -1px -1px 0 #141414; }}
.lb.kw.kwr {{ background: {RED}; color: #fff; text-shadow: none; padding: 8px 34px 0; }}
.stack.full .lb {{ font-size: 120px; }}
.stack.full .lb.kw {{ font-size: 260px; }}
.circ {{ position: absolute; left: -12%; top: -24%; width: 124%; height: 148%; overflow: visible; pointer-events: none; }}
.circ path {{ fill: none; stroke: {BLUE}; stroke-width: 5; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
.cap8 {{ position: absolute; top: 980px; width: 600px; font: 400 28px/1.25 "Special Elite"; color: {INK}; opacity: 0; }}
.star {{ position: absolute; opacity: 0; fill: {INK}; }}
#tear {{ position: absolute; top: -60px; left: -100px; width: 2120px; height: 1200px; z-index: 8; pointer-events: none; transform: translateX(-2400px);
  background: url(assets/img/paper.png); filter: drop-shadow(0 0 20px rgba(0,0,0,.4));
  clip-path: polygon({", ".join(f"{random.Random(k).uniform(0, 4):.1f}% {k * 100 / 30:.1f}%" for k in range(31))}, {", ".join(f"{100 - random.Random(k + 9).uniform(0, 4):.1f}% {100 - k * 100 / 30:.1f}%" for k in range(31))}); }}
#flash {{ position: absolute; inset: 0; z-index: 9; background: #fff; opacity: 0; }}
#redflash {{ position: absolute; inset: 0; z-index: 9; background: {RED}; opacity: 0; mix-blend-mode: multiply; }}
#blinds {{ position: absolute; left: -400px; top: -400px; width: 2800px; height: 1900px; z-index: 10; pointer-events: none; opacity: .32; mix-blend-mode: multiply;
  background: repeating-linear-gradient(-32deg, rgba(40,32,26,0) 0 70px, rgba(40,32,26,.75) 110px 150px, rgba(40,32,26,0) 190px 230px); filter: blur(18px); }}
#vig {{ position: absolute; inset: 0; z-index: 11; pointer-events: none; background: radial-gradient(ellipse 80% 80% at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,.28) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1960px; height: 1120px; z-index: 12; pointer-events: none; opacity: .12; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
#opt, #endt {{ position: absolute; left: 0; right: 0; top: 300px; margin: 0 auto; width: fit-content; z-index: 6; opacity: 0; font-size: 300px; }}
#opk, #endk {{ position: absolute; left: 0; right: 0; top: 700px; margin: 0 auto; width: fit-content; z-index: 6; opacity: 0; font-size: 80px; }}
"""


def main():
    card_track()
    st = still_cards()
    lb = labels()
    acc = accents()
    end = ending()
    gl = random.Random(4)
    grid = "".join(f'<line x1="{x + gl.uniform(-8, 8):.0f}" y1="-20" x2="{x + gl.uniform(-30, 30):.0f}" y2="1100"/>' for x in range(180, 1920, 260)) + \
           "".join(f'<line x1="-20" y1="{y + gl.uniform(-8, 8):.0f}" x2="1940" y2="{y + gl.uniform(-25, 25):.0f}"/>' for y in range(150, 1080, 240))
    g = random.Random(3)
    for f in range(int(DUR * 12)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 12:.3f});')
    js(f'tl.fromTo("#blinds", {{x: 0}}, {{x: 160, duration: {DUR}, ease: "sine.inOut"}}, 0);')
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
      <feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1920" data-height="1080">
      <div id="paper"></div>
      <svg id="grid" viewBox="0 0 1920 1080">{grid}</svg>
      <div id="collage">
        <svg id="redsvg" viewBox="0 0 1920 1080"><path id="redp" d="M0 0"/></svg>
        <div id="cardw"><div id="card"><video id="vid" class="clip" src="assets/video/bw_main.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" muted playsinline></video><i id="tint"></i></div></div>
        {st}
        {acc}
        <div class="edge top"></div><div class="edge bot"></div>
      </div>
      <div id="lyrics" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{lb}{end}</div>
      <div id="tear"></div>
      <div id="flash"></div>
      <div id="redflash"></div>
      <div id="blinds"></div>
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
