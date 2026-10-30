"""Ashke (Karan Aujla, Mxrci) lyric video, 16:9, 60 s from 2:14 of the song: writes index.html.

python3 build/generate.py      (from the project root; needs plan/words_scribe.json and plan/beats_raw.json)

An original animation inspired by the music video's world (an old-money English estate), not built from its footage.
Layers, bottom to top, inside #stage (which the scene transitions push, zoom and whip):
  scene backgrounds in CSS (dusk sky, burgundy, champagne, striped polo lawn, the tartan of his jacket, lake, velvet,
  night road, wood, emerald), 2D decor (twinkling stars, speed lines, sparkles), and the 3D world
  (assets/js/world3d.js: one hero object per lyric section, the camera cutting to a new angle every two beats).
Above the stage: liquid-glass lyric cards (words blur in on their syllable, keywords in gold Playfair italic), a
gold art-deco frame, and the transitions: zoom-through, whip, gold slices, liquid-gold blobs, iris, glass panes with
3D glass shards. Lyric timings: ElevenLabs Scribe word timestamps; the romanized Punjabi is ours, from that transcript.
"""
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 60.0
W = json.load(open(os.path.join(ROOT, "plan", "words_scribe.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
PERIOD = 60 / BEATS["bpm"]
R = random.Random(7)
A, HIDE = [], []

GOLD, CREAM = "#f1cf7a", "#f6efe2"

# (first word, last word, romanized words, alignment, hero). Words marked * are keywords.
LYRICS = [
    (3, 6, "Main *seedha turiya jaavan", "c", False),
    (7, 10, "Tu takdi *tedi *tedi", "l", False),
    (11, 15, "Tu body kar layi *slim", "r", False),
    (16, 21, "Tere te main karda kamm *shady", "c", True),
    (22, 27, "Saada taan tora fera hai na", "l", False),
    (28, 31, "Main nahi launda *gedi", "r", False),
    (32, 35, "*Kaaran, jutti te *asla", "c", False),
    (36, 40, "Nahi ae tinn ikki dukki", "l", False),
    (41, 43, "Nahi leeda *latta", "r", False),
    (44, 50, "Top da rakhaan main jaana chadh ke", "c", False),
    (51, 54, "Kacchi oh *chabb jaa", "l", False),
    (55, 61, "Peene haan chaa nahi, udda kaadh ke", "r", False),
    (62, 64, "*Jatt khulla *ghummda", "c", True),
    (65, 71, "*Vairi nu rakhaan main udda taad ke", "l", False),
    (72, 75, "Nahi taan full *baggy", "r", False),
    (76, 80, "*Patthraan 'ch aaya munda paadh ke", "c", False),
    (81, 83, "Kardi meri *adeeta", "l", False),
    (84, 88, "Nahi saada khul gaya *chaaka", "r", False),
    (89, 94, "Tu dil kardi ae *chori", "c", False),
    (95, 100, "Nahi taan main maari da *daaka", "c", True),
    (101, 104, "*Bebe kehndi tainu vyahna", "l", False),
    (105, 109, "Te mera *shastar dena thaaka", "r", False),
    (110, 114, "Dass ki kar lena kaama", "c", False),
    (115, 119, "Nahi mera baaja yaala *raakha", "l", False),
    (120, 122, "Raahan vich *rode", "r", False),
    (123, 128, "Behna ji yaarana bhena kass ke", "c", False),
    (129, 131, "*Jatt mudhto *zehri", "c", True),
    (132, 137, "*Naagni reha koi saanu dass ke", "l", False),
    (138, 141, "*Baape di saanu bakhshe", "r", False),
    (142, 145, "Chanattiyan gaani lass ke", "c", False),
    (146, 148, "Nahi *mod te paundi", "l", False),
    (149, 153, "Chhumbar de naale kehki *Ashke", "c", False),
    (154, 156, "Nahi *mod te paundi", "r", False),
]

# one 3D scene per lyric section: (kind, start, transition into it, 2D decor)
SCENES = [
    ("intro", 0.0, None, "stars"), ("manor", 1.9, "flash", "stars"), ("shades", 6.8, "zoom", "sparkles"),
    ("car", 9.04, "whip", "streaks"), ("polo", 14.3, "pane", "streaks"), ("tea", 21.2, "pane", None),
    ("boat", 23.4, "blob", None), ("watch", 27.0, "slices", "sparkles"), ("diamond", 34.2, "zoom", "sparkles"),
    ("rings", 37.76, "blob", "sparkles"), ("road", 41.3, "whip", "streaks"), ("chess", 46.3, "slices", None),
    ("snake", 49.85, "pane", "sparkles"), ("finale", 57.0, "iris", "stars"),
]
DAAKA = W[100]["s"]          # the diamond shatters on "daaka"
PANES = [s[1] for s in SCENES if s[2] == "pane"] + [DAAKA]

BG = {
    "intro": "radial-gradient(ellipse at 50% 45%, #163a2c 0, #071510 70%)",
    "manor": "linear-gradient(180deg, #121833 0%, #3a2546 38%, #b4643c 66%, #3a2216 82%, #120c08 100%)",
    "shades": "radial-gradient(ellipse at 50% 45%, #7a1a28 0, #2a070d 75%)",
    "car": "radial-gradient(ellipse at 50% 40%, #fbf4e4 0, #e2d2ae 55%, #a8895a 100%)",
    "polo": "linear-gradient(180deg, #b9cbd6 0%, #e7e1cf 36%, rgba(0,0,0,0) 36.1%), repeating-linear-gradient(90deg, #2f6e3c 0 180px, #265c32 180px 360px)",
    "tea": ("repeating-linear-gradient(0deg, rgba(40,52,92,.55) 0 22px, rgba(0,0,0,0) 22px 120px), "
            "repeating-linear-gradient(90deg, rgba(40,52,92,.55) 0 22px, rgba(0,0,0,0) 22px 120px), "
            "repeating-linear-gradient(0deg, rgba(196,140,62,.45) 60px 66px, rgba(0,0,0,0) 66px 120px), "
            "repeating-linear-gradient(90deg, rgba(196,140,62,.45) 60px 66px, rgba(0,0,0,0) 66px 120px), #c9b48d"),
    "boat": "linear-gradient(180deg, #cfd9d4 0%, #9fb6b1 30%, #2a5560 31%, #0b2a33 100%)",
    "watch": "radial-gradient(ellipse at 50% 45%, #134a36 0, #04140e 75%)",
    "diamond": "radial-gradient(ellipse at 50% 40%, #2a3554 0, #070a14 70%)",
    "rings": "radial-gradient(ellipse at 50% 45%, #fbefe2 0, #e3c7a6 60%, #a77d54 100%)",
    "road": "radial-gradient(ellipse at 50% 30%, #3a2a1a 0, #0a0b10 60%)",
    "chess": "radial-gradient(ellipse at 50% 40%, #4a2a16 0, #160a05 75%)",
    "snake": "radial-gradient(ellipse at 50% 50%, #0f4a35 0, #020806 75%)",
    "finale": "linear-gradient(180deg, #121833 0%, #3a2546 40%, #b4643c 70%, #120c08 100%)",
}


def js(s):
    A.append("      " + s)


def scene_bounds():
    out = []
    for i, (k, a, tr, deco) in enumerate(SCENES):
        b = SCENES[i + 1][1] if i + 1 < len(SCENES) else DUR
        out.append({"k": k, "a": a, "b": b, "tr": tr, "deco": deco})
    return out


def backgrounds(sc):
    out = []
    for s in sc:
        out.append(f'<i class="bg" id="bg-{s["k"]}" style="background:{BG[s["k"]]}"></i>')
        HIDE.append(f'#bg-{s["k"]}')
        js(f'tl.set("#bg-{s["k"]}", {{opacity: 1}}, {s["a"]:.3f});')
        js(f'tl.set("#bg-{s["k"]}", {{opacity: 0}}, {s["b"]:.3f});')
        js(f'tl.fromTo("#bg-{s["k"]}", {{scale: 1.1}}, {{scale: 1, duration: {s["b"] - s["a"]:.3f}, ease: "none", immediateRender: false}}, {s["a"]:.3f});')
    return "".join(out)


def decor(sc):
    """2D layers: twinkling stars, speed lines, sparkles; shown with the scenes that use them."""
    stars = "".join(f'<i style="left:{R.randint(20, 1900)}px;top:{R.randint(20, 520)}px;width:{R.choice([2, 3, 4])}px;height:{R.choice([2, 3, 4])}px"></i>' for _ in range(60))
    streaks = "".join(f'<i style="top:{R.randint(60, 1020)}px;left:{R.randint(-400, 1600)}px;width:{R.randint(200, 700)}px"></i>' for _ in range(16))
    sparks = "".join(f'<i style="left:{R.randint(120, 1800)}px;top:{R.randint(80, 760)}px"></i>' for _ in range(18))
    html = (f'<div class="deco" id="d-stars">{stars}</div><div class="deco" id="d-streaks">{streaks}</div>'
            f'<div class="deco" id="d-sparkles">{sparks}</div>')
    for d in ["stars", "streaks", "sparkles"]:
        HIDE.append(f"#d-{d}")
    for s in sc:
        if s["deco"]:
            js(f'tl.set("#d-{s["deco"]}", {{opacity: 1}}, {s["a"]:.3f});')
            js(f'tl.set("#d-{s["deco"]}", {{opacity: 0}}, {s["b"]:.3f});')
    js(f'tl.fromTo("#d-streaks i", {{x: 0}}, {{x: -2600, duration: .9, ease: "none", stagger: {{each: .05, repeat: {int(DUR / .9)}}}, immediateRender: false}}, 0);')
    js(f'tl.fromTo("#d-stars i", {{opacity: .2}}, {{opacity: 1, duration: .5, yoyo: true, repeat: {int(DUR / .5)}, stagger: {{each: .07, from: "random"}}, ease: "sine.inOut", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#d-sparkles i", {{scale: 0, rotation: 0}}, {{scale: 1, rotation: 90, duration: .35, yoyo: true, repeat: {int(DUR / .35)}, stagger: {{each: .13, from: "random"}}, ease: "sine.inOut", immediateRender: false}}, 0);')
    return html


def lyric_lines():
    out = []
    for li, (i0, i1, text, align, hero) in enumerate(LYRICS):
        toks = text.split()
        n = i1 - i0 + 1
        slots = [i0 + round(k * (n - 1) / max(1, len(toks) - 1)) for k in range(len(toks))] if len(toks) > 1 else [i0]
        a = W[i0]["s"] - .08
        b = (W[LYRICS[li + 1][0]]["s"] - .1) if li + 1 < len(LYRICS) else DUR
        words = []
        for k, tok in enumerate(toks):
            key = tok.startswith("*")
            tok = tok.lstrip("*")
            t = W[slots[k]]["s"]
            wid = f"w{li}_{k}"
            if key:
                letters = "".join(f'<b>{c}</b>' for c in tok)
                words.append(f'<span class="k" id="{wid}">{letters}</span>')
                js(f'tl.fromTo("#{wid} b", {{opacity: 0, y: 40, rotationX: -80, filter: "blur(10px)"}}, '
                   f'{{opacity: 1, y: 0, rotationX: 0, filter: "blur(0px)", duration: .28, stagger: .035, ease: "expo.out", immediateRender: false}}, {t:.3f});')
                js(f'tl.fromTo("#{wid}", {{textShadow: "0 0 60px rgba(241,207,122,.95)"}}, {{textShadow: "0 0 18px rgba(241,207,122,.35)", duration: .6, ease: "power2.out", immediateRender: false}}, {t + .1:.3f});')
            else:
                words.append(f'<span class="s" id="{wid}">{tok}</span>')
                js(f'tl.fromTo("#{wid}", {{opacity: 0, y: 24, filter: "blur(14px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: .22, ease: "expo.out", immediateRender: false}}, {t:.3f});')
        out.append(f'<div class="line {align}{" hero" if hero else ""}" id="ln{li}"><div class="glass" id="gl{li}"><i class="sheen" id="sh{li}"></i></div>'
                   f'<div class="txt">{" ".join(words)}</div></div>')
        HIDE.append(f"#ln{li}")
        js(f'tl.set("#ln{li}", {{opacity: 1}}, {a:.3f});')
        js(f'tl.fromTo("#gl{li}", {{scaleX: .25, scaleY: .5, borderRadius: "999px"}}, {{scaleX: 1, scaleY: 1, borderRadius: "46px", duration: .5, ease: "elastic.out(1, .55)", immediateRender: false}}, {a:.3f});')
        js(f'tl.fromTo("#sh{li}", {{x: "-120%"}}, {{x: "220%", duration: .7, ease: "power2.inOut", immediateRender: false}}, {a + .1:.3f});')
        if b < DUR:
            js(f'tl.to("#ln{li} .txt", {{opacity: 0, y: -26, filter: "blur(16px)", scale: 1.06, duration: .14, ease: "power2.in"}}, {b - .14:.3f});')
            js(f'tl.to("#gl{li}", {{scaleX: 1.15, scaleY: .1, opacity: 0, duration: .16, ease: "power3.in"}}, {b - .14:.3f});')
            js(f'tl.set("#ln{li}", {{opacity: 0}}, {b + .03:.3f});')
    return "".join(out)


def transitions(sc):
    """Scene changes: zoom-through, whip, gold slices, liquid-gold blobs, iris, flash, glass panes. Every camera cut
    inside a scene (every two beats) gets a small punch-in."""
    for s in sc:
        a, kind = s["a"], s["tr"]
        if kind == "zoom":
            js(f'tl.to("#stage", {{scale: 1.9, filter: "blur(16px)", duration: .12, ease: "power3.in"}}, {a - .12:.3f});')
            js(f'tl.fromTo("#stage", {{scale: .6, filter: "blur(16px)"}}, {{scale: 1, filter: "blur(0px)", duration: .3, ease: "expo.out", immediateRender: false}}, {a:.3f});')
        elif kind == "whip":
            js(f'tl.to("#stage", {{x: -1100, filter: "blur(24px)", duration: .12, ease: "power3.in"}}, {a - .12:.3f});')
            js(f'tl.fromTo("#stage", {{x: 1100, filter: "blur(24px)"}}, {{x: 0, filter: "blur(0px)", duration: .26, ease: "expo.out", immediateRender: false}}, {a:.3f});')
        elif kind == "slices":
            for i in range(9):
                d = (i % 3) * .012 + i * .006
                js(f'tl.fromTo("#sl{i}", {{x: {-2100 if i % 2 else 2100}}}, {{x: 0, duration: .14, ease: "power3.in", immediateRender: false}}, {a - .16 + d:.3f});')
                js(f'tl.to("#sl{i}", {{x: {2100 if i % 2 else -2100}, duration: .18, ease: "power3.out"}}, {a + .02 + d:.3f});')
        elif kind == "blob":
            for i in range(7):
                d = i * .02
                js(f'tl.fromTo("#bl{i}", {{scale: 0}}, {{scale: 1, duration: .2, ease: "power2.in", immediateRender: false}}, {a - .22 + d:.3f});')
                js(f'tl.to("#bl{i}", {{scale: 0, duration: .3, ease: "power3.out"}}, {a + .04 + d:.3f});')
        elif kind == "iris":
            js(f'tl.set("#iris", {{opacity: 1, scale: 0}}, {a - .2:.3f});')
            js(f'tl.to("#iris", {{scale: 1, duration: .2, ease: "power3.in"}}, {a - .2 + .001:.3f});')
            js(f'tl.to("#iris", {{scale: 0, duration: .3, ease: "expo.out"}}, {a:.3f});')
            js(f'tl.set("#iris", {{opacity: 0}}, {a + .31:.3f});')
            js(f'tl.set("#flash", {{opacity: .8}}, {a:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: .3}}, {a + .01:.3f});')
        elif kind == "flash":
            js(f'tl.set("#flash", {{opacity: 1}}, {a - .04:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: .25, ease: "power2.out"}}, {a:.3f});')
        # camera cuts inside the scene: a quick punch-in each time
        t = a + 2 * PERIOD
        while t < s["b"] - .2:
            js(f'tl.fromTo("#stage", {{scale: 1.07}}, {{scale: 1, duration: .25, ease: "expo.out", immediateRender: false}}, {t:.3f});')
            t += 2 * PERIOD
    for i, t in enumerate(PANES):
        d = 1 if i % 2 == 0 else -1
        js(f'tl.set("#pane", {{opacity: 1, x: {-2400 * d}, skewX: {-14 * d}}}, {t - .3:.3f});')
        js(f'tl.to("#pane", {{x: {2400 * d}, duration: .55, ease: "power3.inOut"}}, {t - .3:.3f});')
        js(f'tl.set("#pane", {{opacity: 0}}, {t + .26:.3f});')
        js(f'tl.set("#flash", {{opacity: .6}}, {t:.3f});')
        js(f'tl.to("#flash", {{opacity: 0, duration: .2}}, {t + .01:.3f});')
    # kicks shake the stage
    for k in [k for k in BEATS["kicks"] if k < 57][::2]:
        js(f'tl.to("#shake", {{x: {R.choice([-12, 12])}, y: {R.choice([-8, 8])}, duration: .03}}, {k:.3f});')
        js(f'tl.to("#shake", {{x: 0, y: 0, duration: .16, ease: "power2.out"}}, {k + .03:.3f});')


def frame_fx():
    js('tl.set("#bars i", {scaleY: 0}, 0);')
    js('tl.to("#bars i", {scaleY: 1, duration: .5, ease: "expo.out"}, 57.0);')
    g = random.Random(3)
    for f in range(int(DUR * 15)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 15:.3f});')
    js('tl.fromTo("#tag", {opacity: 0, x: -40}, {opacity: 1, x: 0, duration: .6, ease: "expo.out"}, .2);')
    js('tl.fromTo("#frame", {opacity: 0, scale: 1.04}, {opacity: 1, scale: 1, duration: .8, ease: "expo.out"}, .1);')


CSS = f"""
@font-face {{ font-family: "Playfair Display"; font-weight: 900; font-style: italic; src: url("assets/fonts/PlayfairDisplay/PlayfairDisplay-900Italic.ttf"); }}
@font-face {{ font-family: "Playfair Display"; font-weight: 700; font-style: italic; src: url("assets/fonts/PlayfairDisplay/PlayfairDisplay-700Italic.ttf"); }}
@font-face {{ font-family: "Inter Display"; font-weight: 600; src: url("assets/fonts/InterDisplay/InterDisplay-SemiBold.otf"); }}
@font-face {{ font-family: "Inter Display"; font-weight: 500; src: url("assets/fonts/InterDisplay/InterDisplay-Medium.otf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
#shake {{ position: absolute; inset: 0; }}
#stage {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
.bg {{ position: absolute; inset: -60px; display: block; opacity: 0; }}
.deco {{ position: absolute; inset: 0; pointer-events: none; opacity: 0; }}
#d-stars i {{ position: absolute; display: block; background: #fff6dc; border-radius: 50%; box-shadow: 0 0 8px #fff2c8; }}
#d-streaks i {{ position: absolute; display: block; height: 3px; border-radius: 3px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,246,220,.85)); }}
#d-sparkles i {{ position: absolute; display: block; width: 34px; height: 34px; margin: -17px; transform: scale(0);
  background: radial-gradient(circle, #fff 0, #fff 8%, rgba(241,207,122,0) 9%),
    linear-gradient(0deg, rgba(0,0,0,0) 46%, {GOLD} 50%, rgba(0,0,0,0) 54%), linear-gradient(90deg, rgba(0,0,0,0) 46%, {GOLD} 50%, rgba(0,0,0,0) 54%); }}
#gl3d {{ position: absolute; inset: 0; width: 1920px; height: 1080px; pointer-events: none; }}
#frame {{ position: absolute; inset: 34px; z-index: 5; pointer-events: none; border: 1.5px solid rgba(241,207,122,.55); opacity: 0; }}
#frame::before, #frame::after {{ content: ""; position: absolute; width: 90px; height: 90px; border: 3px solid {GOLD}; }}
#frame::before {{ left: -12px; top: -12px; border-right: 0; border-bottom: 0; }}
#frame::after {{ right: -12px; bottom: -12px; border-left: 0; border-top: 0; }}
#lyrics {{ position: absolute; inset: 0; z-index: 6; pointer-events: none; }}
.line {{ position: absolute; bottom: 120px; display: flex; justify-content: center; opacity: 0; perspective: 900px; }}
.line.c {{ left: 50%; transform: translateX(-50%); }}
.line.l {{ left: 150px; }}
.line.r {{ right: 150px; }}
.line .glass {{ position: absolute; inset: -26px -54px; border-radius: 46px; overflow: hidden; transform-origin: 50% 50%;
  backdrop-filter: blur(24px) saturate(1.4) brightness(.72);
  background: linear-gradient(135deg, rgba(255,255,255,.2), rgba(24,16,8,.45) 55%, rgba(24,16,8,.55));
  border: 1.5px solid rgba(255,255,255,.38); box-shadow: inset 0 1px 0 rgba(255,255,255,.6), inset 0 -18px 40px rgba(0,0,0,.12), 0 24px 70px rgba(0,0,0,.4); }}
.line .sheen {{ position: absolute; top: -20%; bottom: -20%; left: 0; width: 34%; display: block; transform: skewX(-18deg);
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.34), rgba(255,255,255,0)); }}
.line .txt {{ position: relative; display: flex; align-items: baseline; gap: 18px; white-space: nowrap; }}
.line .s {{ display: inline-block; font: 600 54px/1.1 "Inter Display"; color: {CREAM}; letter-spacing: .5px; text-shadow: 0 3px 18px rgba(0,0,0,.45); }}
.line .k {{ display: inline-block; font: italic 900 88px/1 "Playfair Display"; color: {GOLD}; letter-spacing: .5px; -webkit-text-stroke: 1.5px rgba(46,26,4,.7); }}
.line .k b {{ display: inline-block; font-weight: 900; transform-origin: 50% 80%; }}
.line.hero .k {{ font-size: 150px; }}
.line.hero .s {{ font-size: 62px; }}
#slices {{ position: absolute; inset: 0; z-index: 8; pointer-events: none; }}
#slices i {{ position: absolute; left: 0; width: 1920px; height: 122px; display: block; transform: translateX(2100px); }}
#goo {{ position: absolute; inset: 0; z-index: 8; pointer-events: none; filter: url(#gooey); }}
#goo i {{ position: absolute; display: block; border-radius: 50%; background: linear-gradient(135deg, #f7dc8f, #b8862e); transform: scale(0); }}
#iris {{ position: absolute; left: 960px; top: 540px; width: 2400px; height: 2400px; margin: -1200px; border-radius: 50%; z-index: 8;
  background: radial-gradient(circle, #f7e6b0 0, #c9963a 60%, #6b4512 100%); opacity: 0; pointer-events: none; }}
#pane {{ position: absolute; top: -100px; left: 560px; width: 820px; height: 1280px; z-index: 8; opacity: 0; pointer-events: none;
  backdrop-filter: blur(30px) saturate(1.7) brightness(1.15);
  background: linear-gradient(90deg, rgba(255,255,255,.35), rgba(255,255,255,.06) 18%, rgba(255,255,255,.04) 82%, rgba(255,255,255,.4));
  border-left: 2px solid rgba(255,255,255,.7); border-right: 2px solid rgba(255,255,255,.7); }}
#flash {{ position: absolute; inset: 0; z-index: 9; background: #fff6e4; opacity: 0; pointer-events: none; }}
#vig {{ position: absolute; inset: 0; z-index: 10; pointer-events: none; background: radial-gradient(ellipse 75% 75% at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,.45) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1960px; height: 1120px; z-index: 11; pointer-events: none; opacity: .08;
  background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
#bars i {{ position: absolute; left: 0; right: 0; height: 110px; background: #000; z-index: 12; display: block; }}
#bars i:first-child {{ top: 0; transform-origin: 50% 0; }}
#bars i:last-child {{ bottom: 0; transform-origin: 50% 100%; }}
#tag {{ position: absolute; left: 70px; top: 64px; z-index: 7; display: flex; align-items: center; gap: 14px; padding: 12px 26px; border-radius: 999px;
  backdrop-filter: blur(16px) saturate(1.4) brightness(.7); background: rgba(16,10,4,.45); border: 1.5px solid rgba(255,255,255,.32); opacity: 0; }}
#tag b {{ font: italic 700 34px/1 "Playfair Display"; color: {GOLD}; }}
#tag span {{ font: 500 22px/1 "Inter Display"; color: {CREAM}; letter-spacing: 4px; }}
"""


def main():
    sc = scene_bounds()
    bgs = backgrounds(sc)
    deco = decor(sc)
    lines = lyric_lines()
    transitions(sc)
    frame_fx()
    slices = "".join(f'<i id="sl{i}" style="top:{i * 120}px;background:{["#f1cf7a", "#f6efe2", "#14100a"][i % 3]}"></i>' for i in range(9))
    blobs = "".join(f'<i id="bl{i}" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px"></i>'
                    for i, (x, y, r) in enumerate([(960, 540, 700), (300, 260, 420), (1650, 300, 460), (420, 900, 480), (1500, 880, 520), (960, 120, 380), (960, 980, 400)]))
    CT = {"dur": DUR, "scenes": [{"k": s["k"], "a": s["a"], "b": s["b"]} for s in sc], "panes": PANES, "daaka": DAAKA,
          "period": PERIOD, "beats": BEATS["beats"]}
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
    <svg width="0" height="0" style="position:absolute"><filter id="gooey"><feGaussianBlur in="SourceGraphic" stdDeviation="22" result="b"/>
      <feColorMatrix in="b" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 30 -12"/></filter></svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="30" data-width="1920" data-height="1080">
      <div id="shake"><div id="stage">
        <div id="bgs">{bgs}</div>
        {deco}
        <canvas id="gl3d" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2"></canvas>
      </div></div>
      <div id="frame"></div>
      <div id="lyrics" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{lines}</div>
      <div id="tag"><b>Ashke</b><span>KARAN AUJLA</span></div>
      <div id="slices">{slices}</div>
      <div id="goo">{blobs}</div>
      <div id="iris"></div>
      <div id="pane"></div>
      <div id="flash"></div>
      <div id="vig"></div>
      <div id="grain"></div>
      <div id="bars"><i></i><i></i></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.AK_T = {json.dumps(CT)};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(HIDE)}, {{opacity: 0}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="assets/js/world3d.js"></script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(LYRICS)} lyric lines, {len(sc)} scenes")


if __name__ == "__main__":
    main()
