"""Ashke (Karan Aujla, Mxrci) lyric video, 16:9, 60 s from 2:14 of the song: writes index.html.

python3 build/generate.py      (from the project root; needs plan/words_scribe.json and plan/beats_raw.json)

Style after the owner's two editing references (Video-77393, Video-7679): cream paper and warm black backgrounds, one
orange accent, small lines typed on with a cursor, huge words one at a time, hand-drawn orange circles, script accents,
an 8-bit cursor, 3D pixel icons (assets/js/world3d.js) with halftone halos, halftone planets (assets/js/halftone.js),
big 3D serif words with orbiting light arcs, and fast transitions (pixel mosaic, halftone dot wipe, orange pixel
wedge, black hole, starburst, glitch, flash). Every lyric line is its own composition. Lyric timings: ElevenLabs Scribe
word timestamps; the romanized Punjabi is ours, from that transcript.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import ICONS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 60.0
W = json.load(open(os.path.join(ROOT, "plan", "words_scribe.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
R = random.Random(11)
A, HIDE = [], []
ORANGE, CREAM, INK = "#ff5a1f", "#efe9df", "#17110f"

# (first word, last word, romanized words). Words marked * are keywords.
LYRICS = [
    (3, 6, "Main *seedha turiya jaavan"), (7, 10, "Tu takdi tedi *tedi"), (11, 15, "Tu body kar layi *slim"),
    (16, 21, "Tere te main karda kamm *shady"), (22, 27, "Saada taan tora fera hai na"), (28, 31, "Main nahi launda *gedi"),
    (32, 35, "*Kaaran, jutti te *asla"), (36, 40, "Nahi ae *tinn ikki dukki"), (41, 43, "Nahi leeda *latta"),
    (44, 50, "Top da rakhaan main jaana *chadh ke"), (51, 54, "Kacchi oh chabb jaa"), (55, 61, "Peene haan *chaa nahi, udda kaadh ke"),
    (62, 64, "Jatt khulla ghummda"), (65, 71, "*Vairi nu rakhaan main udda taad ke"), (72, 75, "Nahi taan full *baggy"),
    (76, 80, "Patthraan 'ch aaya munda *paadh ke"), (81, 83, "Kardi meri *adeeta"), (84, 88, "Nahi saada khul gaya *chaaka"),
    (89, 94, "Tu dil kardi ae *chori"), (95, 100, "Nahi taan main maari da Daaka"), (101, 104, "Bebe kehndi tainu *vyahna"),
    (105, 109, "Te mera *shastar dena thaaka"), (110, 114, "Dass ki kar lena kaama"), (115, 119, "Nahi mera *baaja yaala raakha"),
    (120, 122, "Raahan vich *rode"), (123, 128, "Behna ji *yaarana bhena kass ke"), (129, 131, "Jatt mudhto Zehri"),
    (132, 137, "*Naagni reha koi saanu dass ke"), (138, 141, "*Baape di saanu bakhshe"), (142, 145, "Chanattiyan *gaani lass ke"),
    (146, 148, "Nahi *mod te paundi"), (149, 153, "Chhumbar de naale kehki *Ashke"), (154, 156, "Nahi mod te paundi"),
]

# per line: background, text mode, transition in, and the visual
#   mode: type (typed line + cursor), big (huge words one by one), block (keyword with a block cursor),
#         hero (3D serif word + light arcs; `hero` names the word), glitch (typed, glitching)
#   extras: circle (scribble around the keyword), script (keyword handwritten), cursor (8-bit cursor clicks it)
SHOTS = [
    dict(bg="cream", mode="big", tr="flash"),
    dict(bg="cream", mode="type", tr=None, circle=True, icon=("eye", 960, 440, 30, "pop")),
    dict(bg="dark", mode="type", tr="hole", sphere=dict(x=960, y=440, r=230, fx="squish", word="slim")),
    dict(bg="dark", mode="block", tr="mosaic", icon=("sunglasses", 620, 520, 34, "pop")),
    dict(bg="cream", mode="type", tr="burst", ring=dict(names=["car", "watch", "crown", "diamond", "teacup", "heart", "ring", "shoe", "king", "chain"], x=960, y=400, r=500, s=14)),
    dict(bg="dark", mode="block", tr="wedge", icon=("car", -300, 520, 26, "drive", 620, 520)),
    dict(bg="cream", mode="type", tr="mosaic", train=[("car", 480), ("shoe", 960), ("shield", 1440)]),
    dict(bg="dark", mode="type", tr="hole", icon=("stones", 960, 450, 34, "scatter", "dukki")),
    dict(bg="cream", mode="type", tr="dots", circle=True, icon=("shirt", 960, 430, 30, "pop")),
    dict(bg="dark", mode="type", tr="flash", sphere=dict(x=960, y=420, r=250, fx="rise")),
    dict(bg="cream", mode="big", tr="glitch"),
    dict(bg="cream", mode="type", tr="mosaic", circle=True, icon=("teacup", 960, 430, 30, "pop")),
    dict(bg="dark", mode="hero", tr="burst", hero="Jatt"),
    dict(bg="cream", mode="type", tr="wedge", cursor=True, circle=True, icon=("eye", 960, 430, 30, "pop")),
    dict(bg="dark", mode="block", tr="mosaic", icon=("trousers", 620, 520, 30, "pop")),
    dict(bg="cream", mode="type", tr="hole", icon=("stones", 960, 440, 34, "scatter", "paadh")),
    dict(bg="dark", mode="type", tr="glitch", script=True, sphere=dict(x=960, y=430, r=170, fx="halo")),
    dict(bg="cream", mode="type", tr="dots", icon=("wheel", 960, 430, 26, "roll")),
    dict(bg="dark", mode="block", tr="mosaic", icon=("heart", 620, 520, 34, "away", "chori")),
    dict(bg="dark", mode="hero", tr="burst", hero="Daaka", icon=("diamond", 960, 440, 34, "scatter", "Daaka")),
    dict(bg="cream", mode="type", tr="flash", script=True, icon=("ring", 960, 420, 30, "pop")),
    dict(bg="dark", mode="glitch", tr="glitch"),
    dict(bg="cream", mode="big", tr="wedge"),
    dict(bg="dark", mode="type", tr="mosaic", icon=("falcon", 120, 440, 24, "fly", 1800, 380)),
    dict(bg="cream", mode="type", tr="dots", circle=True, icon=("stones", 1700, 440, 28, "slide", 220, 440)),
    dict(bg="dark", mode="type", tr="burst", ring=dict(names=["heart", "ring", "crown", "chain", "watch", "king"], x=960, y=400, r=430, s=16)),
    dict(bg="dark", mode="hero", tr="glitch", hero="Zehri", heroColor="red", heroFx="glitch"),
    dict(bg="dark", mode="type", tr="hole", icon=("snake", 960, 430, 30, "pop")),
    dict(bg="cream", mode="type", tr="flash", script=True, icon=("crown", 960, 420, 32, "pop")),
    dict(bg="cream", mode="type", tr="mosaic", circle=True, icon=("chain", 960, 420, 26, "spin")),
    dict(bg="dark", mode="type", tr="wedge", cursor=True, icon=("king", 960, 430, 30, "spin")),
    dict(bg="cream", mode="finale", tr="burst"),
    dict(bg="cream", mode="type", tr=None, keep=True, fin=True),
]

ICONS_SCHED, RINGS, SPHERES, WORDS3D = [], [], [], []


def js(s):
    A.append("      " + s)


def line_times(li):
    i0, i1, _ = LYRICS[li]
    a = W[i0]["s"] - .08
    b = (W[LYRICS[li + 1][0]]["s"] - .08) if li + 1 < len(LYRICS) else DUR
    return a, b


def word_slots(li):
    i0, i1, text = LYRICS[li]
    toks = text.split()
    n = i1 - i0 + 1
    slots = [i0 + round(k * (n - 1) / max(1, len(toks) - 1)) for k in range(len(toks))] if len(toks) > 1 else [i0]
    return [(tok.lstrip("*"), tok.startswith("*"), W[s]["s"], W[s]["e"]) for tok, s in zip(toks, slots)]


def blink(sel, t0, t1, per=.5):
    t, k = t0, 0
    while t < t1:
        js(f'tl.set("{sel}", {{opacity: {1 if k % 2 == 0 else 0}}}, {t:.3f});')
        t += per / 2
        k += 1


def scribble(kid, t):
    """A hand-drawn orange ellipse drawn around a word."""
    j = R.uniform
    d = (f"M {50 + j(-4, 4):.1f} {4 + j(-2, 2):.1f} C {96 + j(-3, 3):.1f} {2 + j(-3, 3):.1f}, {103:.1f} {92 + j(-4, 4):.1f}, {50:.1f} {96 + j(-2, 2):.1f} "
         f"S {-4 + j(-2, 2):.1f} {10:.1f}, {58 + j(-3, 3):.1f} {8 + j(-2, 2):.1f}")
    js(f'tl.fromTo("#{kid} .scr path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .35, ease: "power2.out", immediateRender: false}}, {t:.3f});')
    HIDE.append(f"#{kid} .scr")
    js(f'tl.set("#{kid} .scr", {{opacity: 1}}, {t:.3f});')
    return f'<svg class="scr" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="{d}" pathLength="400"/></svg>'


def text_line(li, shot, sid):
    """The lyric text of one line, in the shot's mode. Returns html."""
    a, b = line_times(li)
    words = word_slots(li)
    mode = shot["mode"]
    dark = shot["bg"] == "dark"
    col = CREAM if dark else INK
    parts = []
    if mode in ("type", "glitch", "hero", "block", "finale"):
        lead = [w for w in words if not (mode == "hero" and w[0] == shot.get("hero"))]
        if mode == "block":
            lead = [w for w in words if not w[1]]
        if mode == "finale":
            lead = [w for w in words if w[0] != "Ashke"]
        for k, (tok, key, ts, te) in enumerate(lead):
            wid = f"t{li}_{k}"
            letters = "".join(f"<b>{c}</b>" for c in tok)
            extra = ""
            cls = "kw" if key and mode != "block" else ""
            if key and shot.get("circle"):
                extra = scribble(wid, ts + .12)
            if key and shot.get("script"):
                cls = "kw scr8"
            parts.append(f'<span class="w {cls}" id="{wid}">{letters}{extra}</span>')
            d = min(.24, max(.08, te - ts))
            n = len(tok)
            js(f'tl.set("#{wid}", {{display: "inline-block"}}, {ts:.3f});')   # the word takes its place when typed
            if "scr8" in cls:
                HIDE.append(f"#{wid}")
                js(f'tl.set("#{wid}", {{opacity: 1}}, {ts:.3f});')
                js(f'tl.fromTo("#{wid}", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", duration: .45, ease: "power2.out", immediateRender: false}}, {ts:.3f});')
            else:
                for m in range(n):
                    js(f'tl.set("#{wid} b:nth-of-type({m + 1})", {{display: "inline"}}, {ts + d * m / n:.3f});')
        cls = f"tl {'dark' if dark else 'light'}{' gl' if mode == 'glitch' else ''}{' fin' if mode == 'finale' or shot.get('fin') else ''}{' low' if mode == 'hero' or shot.get('icon') or shot.get('ring') or shot.get('sphere') or shot.get('train') else ''}"
        if mode == "block":
            cls = f"tl {'dark' if dark else 'light'} blk"
        html = f'<div class="{cls}" id="ln{li}"><div class="row">{" ".join(parts)}<i class="caret" id="cr{li}"></i></div>'
        if mode == "block":
            kws = [w for w in words if w[1]]
            if kws:
                tok, _, ts, te = kws[0]
                html += f'<div class="bk" id="bk{li}">{tok}.<i class="blkc" id="bc{li}"></i></div>'
                js(f'tl.fromTo("#bk{li}", {{opacity: 0, x: -40, filter: "blur(10px)"}}, {{opacity: 1, x: 0, filter: "blur(0px)", duration: .25, ease: "expo.out", immediateRender: false}}, {ts:.3f});')
                blink(f"#bc{li}", ts, b, .4)
        html += "</div>"
        blink(f"#cr{li}", a, b, .5)
        if mode == "glitch":
            g = random.Random(li)
            t = a
            while t < b:
                js(f'tl.set("#ln{li} .row", {{x: {g.choice([0, 0, -14, 10, 22])}, skewX: {g.choice([0, 0, -12, 8])}}}, {t:.3f});')
                t += 1 / 12
        parts_html = html
    elif mode == "big":
        parts_html = f'<div class="big {"dark" if dark else "light"}" id="ln{li}">'
        for k, (tok, key, ts, te) in enumerate(words):
            nxt = words[k + 1][2] if k + 1 < len(words) else b
            parts_html += f'<span class="bw{" kwb" if key else ""}" id="bw{li}_{k}">{tok}</span>'
            HIDE.append(f"#bw{li}_{k}")
            js(f'tl.fromTo("#bw{li}_{k}", {{opacity: 0, scale: 1.25, filter: "blur(12px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .14, ease: "expo.out", immediateRender: false}}, {ts:.3f});')
            js(f'tl.set("#bw{li}_{k}", {{opacity: 0}}, {nxt - .02:.3f});')
        parts_html += '<i class="guide g1"></i><i class="guide g2"></i></div>'
    HIDE.append(f"#ln{li}")
    js(f'tl.set("#ln{li}", {{opacity: 1}}, {a:.3f});')
    if not shot.get("keepnext"):
        js(f'tl.set("#ln{li}", {{opacity: 0}}, {b:.3f});')
    return parts_html


def visuals(li, shot):
    """Icons, rings, trains, spheres and 3D words for one line (schedules for the JS layers) plus their DOM halos."""
    a, b = line_times(li)
    words = word_slots(li)
    wt = {w[0].lower().rstrip(","): w[2] for w in words}
    html = ""
    if "icon" in shot:
        ic = shot["icon"]
        name, x, y, s, fx = ic[:5]
        it = {"n": name, "a": round(a, 3), "b": round(b, 3), "fx": fx, "x": x, "y": y, "s": s}
        if fx in ("drive", "fly", "slide"):
            it["x2"], it["y2"] = ic[5], ic[6]
            it["dur"] = .5 if fx == "drive" else (b - a)
        if fx in ("scatter", "away"):
            it["t0"] = round(wt[ic[5].lower()] + (.35 if fx == "away" else .05), 3)
        ICONS_SCHED.append(it)
        if fx not in ("fly", "slide", "drive"):
            html += halo(f"ha{li}", x, y, ICONS[name]["w"] * s * 1.15, a, b)
        elif fx == "drive":
            html += halo(f"ha{li}", ic[5], ic[6], ICONS[name]["w"] * s * 1.1, a + .4, b)
    if "ring" in shot:
        r = dict(shot["ring"]); r.update(a=round(a, 3), b=round(b, 3), fast=round(b - .6, 3))
        RINGS.append(r)
    if "train" in shot:
        for k, (name, x) in enumerate(shot["train"]):
            ICONS_SCHED.append({"n": name, "a": round(a + k * .12, 3), "b": round(b, 3), "fx": "slide", "x": x + 260, "y": 450, "x2": x - 260, "y2": 450, "s": 22})
    if "sphere" in shot:
        sp = dict(shot["sphere"]); sp.update(a=round(a, 3), b=round(b, 3), color=ORANGE)
        if "word" in sp:
            sp["t0"] = round(wt[sp.pop("word")], 3)
        SPHERES.append(sp)
    if shot["mode"] == "hero":
        hw = shot["hero"]
        WORDS3D.append({"text": hw, "a": round(wt[hw.lower()] - .05, 3), "b": round(b, 3), "color": shot.get("heroColor", "cream"),
                        "fx": shot.get("heroFx", ""), "x": 960, "y": 430, "size": 1.0})
        html += arcs(f"arc{li}", wt[hw.lower()], b)
    return html


def halo(hid, x, y, size, a, b):
    HIDE.append(f"#{hid}")
    js(f'tl.fromTo("#{hid}", {{opacity: 0, scale: .3}}, {{opacity: 1, scale: 1, duration: .45, ease: "expo.out", immediateRender: false}}, {a:.3f});')
    js(f'tl.to("#{hid}", {{opacity: 0, scale: 1.4, duration: .2}}, {b - .2:.3f});')
    return f'<i class="halo" id="{hid}" style="left:{x - size / 2:.0f}px;top:{y - size / 2:.0f}px;width:{size:.0f}px;height:{size:.0f}px"></i>'


def arcs(aid, a, b):
    HIDE.append(f"#{aid}")
    js(f'tl.set("#{aid}", {{opacity: 1}}, {a:.3f});')
    js(f'tl.set("#{aid}", {{opacity: 0}}, {b:.3f});')
    js(f'tl.fromTo("#{aid} .e1", {{rotation: -30, svgOrigin: "500 300"}}, {{rotation: 330, svgOrigin: "500 300", duration: 2.4, ease: "none", repeat: 2, immediateRender: false}}, {a:.3f});')
    js(f'tl.fromTo("#{aid} .e2", {{rotation: 60, svgOrigin: "500 300"}}, {{rotation: -300, svgOrigin: "500 300", duration: 2.0, ease: "none", repeat: 2, immediateRender: false}}, {a:.3f});')
    js(f'tl.fromTo("#{aid} ellipse", {{strokeDashoffset: 1000}}, {{strokeDashoffset: 0, duration: .5, ease: "power2.out", immediateRender: false}}, {a:.3f});')
    e = ('<ellipse cx="500" cy="300" rx="430" ry="120" pathLength="1000" stroke-dasharray="420 580"/>')
    return f'<svg class="arcs" id="{aid}" viewBox="0 0 1000 600"><g class="e1">{e}</g><g class="e2">{e}</g></svg>'


def finale(li):
    """The end, as in the first reference: the title's letters scattered, circled in orange one by one, the 3D title,
    and a handwritten signature underlined."""
    a, b = line_times(li)
    t_ashke = word_slots(li)[-1][2]
    pos = [(300, 230), (1560, 260), (240, 820), (1650, 800), (960, 150)]
    html = '<div id="fin">'
    for i, (ch, (x, y)) in enumerate(zip("ASHKE", pos)):
        html += f'<span class="fl" id="fl{i}" style="left:{x}px;top:{y}px">{ch}{scribble(f"fl{i}", t_ashke + .1 + i * .12)}</span>'
        HIDE.append(f"#fl{i}")
        js(f'tl.fromTo("#fl{i}", {{opacity: 0, scale: 2, rotation: {R.randint(-40, 40)}}}, {{opacity: 1, scale: 1, rotation: {R.randint(-12, 12)}, duration: .3, ease: "expo.out", immediateRender: false}}, {a + i * .06:.3f});')
    html += '<div class="sig" id="sig"><span class="sg">Karan Aujla<i class="ul" id="ul"></i></span></div></div>'
    HIDE.append("#sig")
    js(f'tl.set("#sig", {{opacity: 1}}, {a + .35:.3f});')
    js(f'tl.fromTo("#sig .sg", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", duration: .9, ease: "power1.inOut", immediateRender: false}}, {a + .35:.3f});')
    js(f'tl.fromTo("#ul", {{scaleX: 0}}, {{scaleX: 1, duration: .35, ease: "power2.out", immediateRender: false}}, {a + 1.2:.3f});')
    WORDS3D.append({"text": "Ashke", "a": round(t_ashke - .05, 3), "b": DUR, "color": "orange", "fx": "", "x": 960, "y": 470, "size": 1.1})
    html += arcs("arcfin", t_ashke, DUR)
    return html


def transitions():
    bgs = [(0.0, "dark")]   # the intro
    for li, shot in enumerate(SHOTS):
        a, b = line_times(li)
        if not shot.get("keep"):
            bgs.append((a, shot["bg"]))
        kind = shot["tr"]
        if kind == "flash":
            js(f'tl.set("#flash", {{opacity: 1}}, {a - .03:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: .22, ease: "power2.out"}}, {a:.3f});')
        elif kind == "mosaic":
            for r in range(10):
                for c in range(18):
                    d1, d2 = R.uniform(0, .12), R.uniform(0, .12)
                    js(f'tl.set("#mo{r}_{c}", {{opacity: 1}}, {a - .16 + d1:.3f});')
                    js(f'tl.set("#mo{r}_{c}", {{opacity: 0}}, {a + .02 + d2:.3f});')
        elif kind == "dots":
            for c in range(24):
                t = a - .22 + c * .012
                js(f'tl.fromTo(".dd{c}", {{scale: 0}}, {{scale: 1, duration: .1, ease: "power2.in", immediateRender: false}}, {t:.3f});')
                js(f'tl.to(".dd{c}", {{scale: 0, duration: .14, ease: "power2.out"}}, {t + .24:.3f});')
        elif kind == "wedge":
            js(f'tl.fromTo("#wedge", {{x: -2600}}, {{x: 2600, duration: .42, ease: "power2.inOut", immediateRender: false}}, {a - .21:.3f});')
        elif kind == "hole":
            js(f'tl.set("#hole", {{opacity: 1, scale: 0}}, {a - .2:.3f});')
            js(f'tl.to("#hole", {{scale: 1, duration: .2, ease: "power3.in"}}, {a - .199:.3f});')
            js(f'tl.to("#hole", {{scale: 0, duration: .26, ease: "expo.out"}}, {a + .01:.3f});')
            js(f'tl.set("#hole", {{opacity: 0}}, {a + .28:.3f});')
        elif kind == "burst":
            js(f'tl.set("#burst", {{opacity: 1, scale: 0, rotation: 0}}, {a - .22:.3f});')
            js(f'tl.to("#burst", {{scale: 9, rotation: 40, duration: .24, ease: "power3.in"}}, {a - .219:.3f});')
            js(f'tl.set("#burst", {{opacity: 0}}, {a + .03:.3f});')
            js(f'tl.set("#flash", {{opacity: .7}}, {a:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: .2}}, {a + .01:.3f});')
        elif kind == "glitch":
            g = random.Random(int(a * 10))
            for f in range(4):
                js(f'tl.set("#glitch", {{opacity: 1}}, {a - .1 + f / 30:.3f});')
                for i in range(6):
                    js(f'tl.set("#gb{i}", {{y: {g.randint(0, 1040)}, height: {g.choice([8, 18, 40, 90])}, x: {g.randint(-80, 80)}, '
                       f'backgroundColor: "{g.choice([ORANGE, INK, CREAM, "#e2332d", "#2fe0ff"])}"}}, {a - .1 + f / 30:.3f});')
            js(f'tl.set("#glitch", {{opacity: 0}}, {a + .04:.3f});')
        # each new shot punches in
        js(f'tl.fromTo("#stage", {{scale: 1.06}}, {{scale: 1, duration: .3, ease: "expo.out", immediateRender: false}}, {a:.3f});')
    for i, (a, bg) in enumerate(bgs):
        b = bgs[i + 1][0] if i + 1 < len(bgs) else DUR
        js(f'tl.set("#bg-{bg}", {{opacity: 1}}, {a:.3f});')
        js(f'tl.set("#bg-{bg}", {{opacity: 0}}, {b:.3f});')
    # the 8-bit cursor clicks on the keyword
    for li, shot in enumerate(SHOTS):
        if shot.get("cursor"):
            ws = word_slots(li)
            kw = next(w for w in ws if w[1])
            t = kw[2]
            # estimate where the keyword sits on the centred line (Outfit 600 at 54 px: about 27 px a character)
            width = sum(len(w[0]) * 27 for w in ws) + 16 * (len(ws) - 1)
            x = 960 - width / 2
            for w in ws:
                if w is kw:
                    break
                x += len(w[0]) * 27 + 16
            tx, ty = x + len(kw[0]) * 27 * .7, 845
            js(f'tl.set("#cur", {{opacity: 1, x: {tx + 700:.0f}, y: {ty - 300:.0f}}}, {t - .4:.3f});')
            js(f'tl.to("#cur", {{x: {tx:.0f}, y: {ty:.0f}, duration: .32, ease: "power3.out"}}, {t - .399:.3f});')
            js(f'tl.to("#cur", {{scale: .8, duration: .06, yoyo: true, repeat: 1}}, {t - .05:.3f});')
            js(f'tl.set("#cur", {{opacity: 0}}, {line_times(li)[1]:.3f});')


def main():
    stage_html, top_html = "", ""
    for li, shot in enumerate(SHOTS):
        if shot["mode"] == "finale":
            stage_html += finale(li)
            top_html += text_line(li, dict(shot, mode="finale"), li)
        else:
            stage_html += visuals(li, shot)
            top_html += text_line(li, shot, li)
    # intro: before the first lyric, the 3D title and a typed credit
    WORDS3D.insert(0, {"text": "Ashke", "a": 0.0, "b": round(line_times(0)[0], 3), "color": "cream", "fx": "", "x": 960, "y": 470, "size": 1.0})
    SPHERES.insert(0, {"a": 0.0, "b": round(line_times(0)[0], 3), "x": 960, "y": 470, "r": 120, "fx": "halo", "color": ORANGE})
    intro = '<div class="tl dark low" id="intro"><div class="row"><span class="w">' + "".join(f"<b>{c}</b>" for c in "karan aujla") + '</span><i class="caret" id="crI"></i></div></div>'
    js('tl.set("#intro .w", {display: "inline-block"}, .5);')
    for m in range(11):
        js(f'tl.set("#intro b:nth-of-type({m + 1})", {{display: "inline"}}, {.5 + m * .06:.3f});')
    blink("#crI", 0, line_times(0)[0], .5)
    js(f'tl.set("#intro", {{opacity: 0}}, {line_times(0)[0]:.3f});')
    transitions()
    g = random.Random(3)
    for f in range(int(DUR * 12)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 12:.3f});')
    mos = "".join(f'<i id="mo{r}_{c}" style="left:{c * 107}px;top:{r * 108}px;background:{R.choice([ORANGE, CREAM, INK, INK, "#c43d12"])}"></i>' for r in range(10) for c in range(18))
    dots = "".join(f'<i class="dd{c}" style="left:{c * 84 + 6}px;top:{r * 84 + 6}px"></i>' for r in range(13) for c in range(24))
    gb = "".join(f'<b id="gb{i}"></b>' for i in range(6))
    CT = {"iconMaps": ICONS, "icons": ICONS_SCHED, "rings": RINGS, "spheres": SPHERES, "words3d": WORDS3D, "beats": BEATS["beats"]}
    html = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Ashke lyric video 16x9</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1920" data-height="1080">
      <div id="stage">
        <i class="bg" id="bg-cream"></i><i class="bg" id="bg-dark"></i>
        <canvas id="ht" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1"></canvas>
        {stage_html}
        <canvas id="gl3d" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2"></canvas>
      </div>
      <div id="lyrics" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{intro}{top_html}</div>
      <svg id="cur" viewBox="0 0 12 16" shape-rendering="crispEdges"><path d="M0 0h1v1h1v1h1v1h1v1h1v1h1v1h1v1h1v1h1v1h1v1h-4v1h1v1h1v2h-2v-1h-1v-1h-1v-1h-1v1h-1v1h-2z" fill="{INK}"/>
        <path d="M1 2h1v1h1v1h1v1h1v1h1v1h1v1h1v1h1v1h-4v1h1v1h1v1h-1v-1h-1v-1h-1v-1h-1v1h-1z" fill="{ORANGE}"/></svg>
      <div id="mosaic">{mos}</div>
      <div id="dots">{dots}</div>
      <div id="wedge"></div>
      <div id="hole"></div>
      <svg id="burst" viewBox="-50 -50 100 100">{"".join(f'<path d="M0 0 L{48 * __import__("math").cos(i * .5236 - .09):.1f} {48 * __import__("math").sin(i * .5236 - .09):.1f} L{48 * __import__("math").cos(i * .5236 + .09):.1f} {48 * __import__("math").sin(i * .5236 + .09):.1f}Z"/>' for i in range(12))}<circle r="9"/></svg>
      <div id="glitch">{gb}</div>
      <div id="flash"></div>
      <div id="vig"></div>
      <div id="grain"></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.AK_T = {json.dumps(CT)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(list(dict.fromkeys(HIDE)))}, {{opacity: 0}});
      gsap.set("#bg-dark", {{opacity: 1}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/halftone.js"></script>
    <script type="module" src="assets/js/world3d.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines; {len(ICONS_SCHED)} icons, {len(RINGS)} rings, {len(SPHERES)} spheres, {len(WORDS3D)} 3D words")


CSS = f"""
@font-face {{ font-family: "Outfit"; font-weight: 500; src: url("assets/fonts/Outfit/Outfit-500.ttf"); }}
@font-face {{ font-family: "Outfit"; font-weight: 600; src: url("assets/fonts/Outfit/Outfit-600.ttf"); }}
@font-face {{ font-family: "Outfit"; font-weight: 800; src: url("assets/fonts/Outfit/Outfit-800.ttf"); }}
@font-face {{ font-family: "Mrs Saint Delafield"; src: url("assets/fonts/MrsSaintDelafield/MrsSaintDelafield-400.ttf"); }}
@font-face {{ font-family: "Playfair Display"; font-weight: 900; font-style: italic; src: url("assets/fonts/PlayfairDisplay/PlayfairDisplay-900Italic.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
#stage {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
.bg {{ position: absolute; inset: -40px; display: block; opacity: 0; }}
#bg-cream {{ background: radial-gradient(ellipse 70% 70% at 50% 45%, #f2ede5 0, #e2dbd0 55%, #b9b1a5 100%); }}
#bg-dark {{ background: radial-gradient(ellipse 65% 65% at 50% 45%, #2a1d19 0, #160f0d 55%, #070505 100%); }}
#ht, #gl3d {{ position: absolute; inset: 0; width: 1920px; height: 1080px; pointer-events: none; }}
.halo {{ position: absolute; display: block; border-radius: 50%; opacity: 0; pointer-events: none;
  background: radial-gradient(circle, {ORANGE} 30%, rgba(0,0,0,0) 33%) 0 0 / 16px 16px;
  -webkit-mask-image: radial-gradient(circle, rgba(0,0,0,.9) 0, rgba(0,0,0,.5) 35%, rgba(0,0,0,0) 68%); mask-image: radial-gradient(circle, rgba(0,0,0,.9) 0, rgba(0,0,0,.5) 35%, rgba(0,0,0,0) 68%); }}
.arcs {{ position: absolute; left: 260px; top: 130px; width: 1400px; height: 840px; pointer-events: none; opacity: 0; overflow: visible; }}
.arcs ellipse {{ fill: none; stroke: #fff6ea; stroke-width: 3; stroke-linecap: round; filter: drop-shadow(0 0 8px rgba(255,240,220,.9)); }}
#lyrics {{ position: absolute; inset: 0; z-index: 5; pointer-events: none; }}
.tl {{ position: absolute; left: 0; right: 0; top: 500px; display: flex; flex-direction: column; align-items: center; opacity: 0; }}
.tl.low {{ top: 800px; }}
.tl.fin {{ top: 900px; }}
.tl .row {{ display: flex; align-items: baseline; gap: 16px; white-space: nowrap; }}
.tl .w {{ position: relative; display: none; font: 600 54px/1.15 "Outfit"; letter-spacing: -.5px; white-space: pre; }}
.tl .w b {{ font-weight: 600; display: none; }}
.tl.light .w {{ color: {INK}; }}
.tl.dark .w {{ color: {CREAM}; }}
.tl .kw {{ color: {ORANGE} !important; }}
.tl.light .kw {{ color: #cc3f0a !important; }}
.tl .kw.scr8 {{ font: 400 104px/1 "Mrs Saint Delafield"; opacity: 0; padding: 0 10px; }}
.tl .kw.scr8 b {{ font-weight: 400; display: inline; }}
.tl .caret {{ display: inline-block; width: 4px; height: 52px; background: currentColor; align-self: center; }}
.tl.light .caret {{ background: {INK}; }}
.tl.dark .caret {{ background: {CREAM}; }}
.tl.gl .w {{ text-shadow: 4px 0 0 rgba(226,51,45,.85), -4px 0 0 rgba(47,224,255,.7); }}
.tl.blk {{ left: 1000px; right: auto; top: 430px; align-items: flex-start; }}
.tl.blk .row .w {{ font-size: 46px; }}
.tl .bk {{ display: flex; align-items: center; gap: 18px; font: 800 132px/1 "Outfit"; color: {ORANGE}; letter-spacing: -3px; opacity: 0; }}
.tl .blkc {{ display: block; width: 64px; height: 100px; background: {CREAM}; }}
.scr {{ position: absolute; left: -22%; top: -38%; width: 144%; height: 176%; overflow: visible; opacity: 0; }}
.scr path {{ fill: none; stroke: {ORANGE}; stroke-width: 4; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
.big {{ position: absolute; inset: 0; opacity: 0; }}
.big .bw {{ position: absolute; left: 0; right: 0; top: 380px; text-align: center; font: 800 250px/1 "Outfit"; letter-spacing: -8px; }}
.big.light .bw {{ color: {INK}; }}
.big.dark .bw {{ color: {CREAM}; }}
.big .bw.kwb {{ color: {ORANGE}; }}
.big .guide {{ position: absolute; left: 0; right: 0; height: 0; border-top: 2px dashed rgba(255,90,31,.7); display: block; }}
.big .g1 {{ top: 390px; }}
.big .g2 {{ top: 650px; }}
#fin {{ position: absolute; inset: 0; }}
.fl {{ position: absolute; font: 600 64px/1 "Outfit"; color: {INK}; opacity: 0; }}
.sig {{ position: absolute; left: 0; right: 0; top: 640px; text-align: center; font: 400 130px/1.1 "Mrs Saint Delafield"; color: {INK}; opacity: 0; }}
.sig .sg {{ position: relative; display: inline-block; padding: 0 30px; }}
.sig .ul {{ position: absolute; left: 40px; right: 40px; bottom: 4px; height: 5px; background: {ORANGE}; display: block; transform-origin: 0 50%; transform: scaleX(0); }}
#cur {{ position: absolute; left: 0; top: 0; width: 72px; height: 96px; z-index: 6; opacity: 0; transform-origin: 0 0; }}
#mosaic {{ position: absolute; inset: 0; z-index: 8; pointer-events: none; }}
#mosaic i {{ position: absolute; width: 108px; height: 109px; display: block; opacity: 0; }}
#dots {{ position: absolute; inset: 0; z-index: 8; pointer-events: none; }}
#dots i {{ position: absolute; width: 74px; height: 74px; border-radius: 50%; background: {ORANGE}; display: block; transform: scale(0); }}
#wedge {{ position: absolute; top: -200px; left: 0; width: 2400px; height: 1480px; z-index: 8; pointer-events: none; transform: translateX(-2600px);
  background: {ORANGE}; clip-path: polygon(0 0, 70% 0, 100% 50%, 70% 100%, 0 100%, 30% 50%); }}
#hole {{ position: absolute; left: 960px; top: 540px; width: 2600px; height: 2600px; margin: -1300px; border-radius: 50%; z-index: 8; opacity: 0; pointer-events: none;
  background: radial-gradient(circle, #050303 0, #050303 62%, {ORANGE} 63%, rgba(255,90,31,0) 72%); }}
#burst {{ position: absolute; left: 760px; top: 340px; width: 400px; height: 400px; z-index: 8; opacity: 0; pointer-events: none; fill: {ORANGE}; overflow: visible; }}
#glitch {{ position: absolute; inset: 0; z-index: 9; opacity: 0; pointer-events: none; }}
#glitch b {{ position: absolute; left: -80px; right: -80px; display: block; }}
#flash {{ position: absolute; inset: 0; z-index: 9; background: #fff8ef; opacity: 0; pointer-events: none; }}
#vig {{ position: absolute; inset: 0; z-index: 10; pointer-events: none; background: radial-gradient(ellipse 80% 80% at 50% 50%, rgba(0,0,0,0) 62%, rgba(0,0,0,.35) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1960px; height: 1120px; z-index: 11; pointer-events: none; opacity: .1;
  background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
"""

if __name__ == "__main__":
    main()
