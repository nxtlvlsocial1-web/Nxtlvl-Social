"""Vitonnix Biotin reel: writes index.html. 1080x1920, 30 fps, about 24.7 s.

python3 build/generate.py      (from the project root, after build/voice.py and build/images.py;
                                build/audio.py writes the music mix and this picks it up on the next run)

Look: the client's own plum world (colours sampled from their creatives, see brands/vitonnix/brand.md), Fraunces for
display, Montserrat for UI and captions, Great Vibes for script accents. A persistent background layer (radial plum,
breathing magenta glows, ghost type, twinkling sparkles, grain) sits under ten scenes cut on the voiceover:

  1 hook      pills rain, "Still swallowing biotin pills?"        6 benefits  lifestyle photo in an arch, hair/skin/nails icons
  2 glow-up   the big capsule cracks into sparkles, mist photo     7 flavour   lychee and mint orbit the pack, sugar/GMO badges
  3 reveal    packshot + "Vitonnix Biotin" (music drop)           8 trust     FSSAI, GMP, FSSC 22000 badges stamp in
  4 one spray mist photo push-in, giant "1 spray", DONE stamp      9 origin    3 doctors card, UK flag, Sublispray tech
  5 stat      9X slot-roll counter with ring                      10 CTA       Comment BIOTIN, Tata 1mg tag, wordmark

Images are the client's own (build/images.py). Stats on screen are the client's: 9X better absorption (their claim,
see caption.md for the substantiation note), lychee and mint flavour and "Sublispray UK technology" (from the pack),
no added sugar, non-GMO, FSSAI, GMP and ISO FSSC 22000 v6 (their "Your health, our promise" badges), three doctor
founders and Tata 1mg (press coverage).
"""
import json
import math
import os
import random
import re
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
VOICE_END = LINES[-1]["end"]
DUR = round(VOICE_END + 2.0, 2)
FPS = 30
AUDIO = "assets/audio/mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "assets/audio/voice.wav"
PACK_AR = 404 / 1126                      # packshot card aspect (w/h)
rnd = random.Random(42)

C = dict(PLUM="#890045", DEEP="#5a0230", DARK="#33001b", MAG="#c2187a", PINK="#ff5fae", BLUSH="#fff0f6",
         INK="#3b0020", GOLD="#ffd27a")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def word(line, text, nth=1, exact=False, key="s"):
    hits = [w for w in WORDS if w["line"] == line and ((norm(w["w"]) == text) if exact else norm(w["w"]).startswith(text))]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1][key]


L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
T = {
    "still": word(1, "still"), "swallowing": word(1, "swallowing"), "biotin1": word(1, "biotin"), "pills": word(1, "pills"),
    "heres": word(2, "heres"), "glow": word(2, "glow"),
    "vitonnix": word(3, "vitonnix"), "biotin2": word(3, "biotin"),
    "one": word(4, "one"), "spray": word(4, "spray"), "under": word(4, "under"), "tongue": word(4, "tongue"), "done": word(4, "done"),
    "fine": word(5, "fine"), "mist": word(5, "mist"), "nine": word(5, "nine"), "x": word(5, "x", exact=True),
    "better": word(5, "better"), "absorption": word(5, "absorption"),
    "made": word(6, "made"), "hair": word(6, "hair"), "skin": word(6, "skin"), "nails": word(6, "nails"),
    "lychee": word(7, "lychee"), "mint": word(7, "mint"), "flavour": word(7, "flavour"), "no": word(7, "no", exact=True),
    "sugar": word(7, "sugar"),
    "fssai": word(8, "f", exact=True), "gmp": word(8, "g", exact=True), "certified": word(8, "certified"),
    "created": word(9, "created"), "three": word(9, "three"), "doctors": word(9, "doctors"), "uk": word(9, "uk", exact=True),
    "sublispray": word(9, "sublispray"), "technology": word(9, "technology"),
    "comment": word(10, "comment"), "biotin3": word(10, "biotin"), "dm": word(10, "dm"), "link": word(10, "link"),
    "end": DUR,
}
json.dump({"l": L, "e": E, **T}, open(os.path.join(B, "cues.json"), "w"), indent=0)

# scene windows; the hook clip runs under the glow-up so the capsule can crack across the cut
W1 = (0, L[2] + .05)
W_MIST1 = (L[1] - .06, L[2] + .05)
W3 = (L[2], L[3])
W4 = (L[3], L[4])
W5 = (L[4], L[5])
W6 = (L[5], L[6])
W7 = (L[6], L[7])
W8 = (L[7], L[8])
W9 = (L[8], L[9])
W10 = (L[9], DUR)

tw = []


def J(o):
    return json.dumps(o, separators=(",", ":"))


def fromTo(sel, a, b, t, dur=.3, ease="back.out(2)"):
    tw.append(f"tl.fromTo({J(sel)},{J(a)},{J({**b, 'duration': dur, 'ease': ease, 'immediateRender': False})},{t:.3f});")


def to(sel, b, t, dur=.2, ease="power3.in"):
    tw.append(f"tl.to({J(sel)},{J({**b, 'duration': dur, 'ease': ease})},{t:.3f});")


def set_(sel, b, t):
    tw.append(f"tl.set({J(sel)},{J(b)},{max(0, t):.3f});")


def pop(sel, t, dur=.28, y=40, scale=.7, ease="back.out(2.4)"):
    fromTo(sel, {"opacity": 0, "y": y, "scale": scale}, {"opacity": 1, "y": 0, "scale": 1}, t, dur, ease)


def flash(t, a=1.0, d=.3, color="w"):
    sel = "#flash" if color == "w" else "#flashp"
    set_(sel, {"opacity": a}, t)
    to(sel, {"opacity": 0}, t + .02, d, "power2.out")


STAR = '<svg viewBox="0 0 40 40" width="100%" height="100%"><path d="M20 0C21.6 13 27 18.4 40 20 27 21.6 21.6 27 20 40 18.4 27 13 21.6 0 20 13 18.4 18.4 13 20 0Z" fill="currentColor"/></svg>'


def star(cls, x, y, size, color):
    return f'<i class="star {cls}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;color:{color}">{STAR}</i>'


def pack(id_, x, y, h, extra=""):
    w = round(h * PACK_AR)
    return (f'<div id="{id_}" class="pack in {extra}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<img src="assets/img/packshot.png" alt="" width="{w}" height="{h}"><i class="sheen"></i></div>')


def capsule(id_, x, y, w, h, cls="pl"):
    return (f'<div id="{id_}" class="{cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<b class="hl" style="border-radius:{h / 2}px 0 0 {h / 2}px"></b><b class="hr" style="border-radius:0 {h / 2}px {h / 2}px 0"></b>'
            f'<i class="shine"></i></div>')


# ------------------------------------------------------------------ background layer (whole film)
bg_stars = []
for i in range(34):
    x, y = rnd.uniform(30, 1030), rnd.uniform(120, 1820)
    size = rnd.choice([10, 12, 14, 18, 22, 28, 34])
    col = rnd.choice([C["BLUSH"], C["PINK"], C["GOLD"], C["BLUSH"]])
    bg_stars.append(star(f"bs bs{i}", round(x), round(y), size, col))
    period = rnd.uniform(1.1, 2.4)
    t0 = rnd.uniform(0, period)
    reps = int((DUR - t0) / period)
    tw.append(f'tl.fromTo(".bs{i}",{{"opacity":0.05,"scale":0.3,"rotation":0}},{{"opacity":{rnd.uniform(.55, .95):.2f},"scale":1,"rotation":45,'
              f'"duration":{period / 2:.2f},"ease":"sine.inOut","yoyo":true,"repeat":{reps * 2 - 1},"immediateRender":false}},{t0:.2f});')
fromTo("#bgstars", {"y": 0}, {"y": -160}, 0, DUR, "none")
fromTo("#g1", {"scale": 1, "x": 0}, {"scale": 1.25, "x": 120}, 0, DUR / 2, "sine.inOut")
fromTo("#g1", {"scale": 1.25, "x": 120}, {"scale": 1, "x": 0}, DUR / 2, DUR / 2, "sine.inOut")
fromTo("#g2", {"scale": 1.2, "y": 0}, {"scale": .9, "y": -200}, 0, DUR, "sine.inOut")
fromTo("#ghost", {"x": 0}, {"x": -520}, 0, DUR, "none")

# ------------------------------------------------------------------ 1 hook
rain = []
for i in range(13):
    x = rnd.uniform(-40, 980)
    y0 = rnd.uniform(-420, 1500) if i < 8 else rnd.uniform(-900, -250)
    w = rnd.choice([120, 140, 160, 190])
    rain.append(capsule(f"rp{i}", round(x), 0, w, round(w * .4), "pl rp"))
    d = rnd.uniform(1.7, 2.6)
    r0 = rnd.uniform(-60, 60)
    fromTo(f"#rp{i}", {"y": round(y0), "rotation": round(r0)}, {"y": round(y0 + 2300 * d / 2.2), "rotation": round(r0 + rnd.choice([-1, 1]) * rnd.uniform(140, 320))},
           0, d, "power1.in")
set_(".rp", {"opacity": .85}, 0)
to("#rain", {"opacity": 0}, L[1] - .1, .25, "power1.out")

set_("#h1a", {"opacity": 1}, 0)
fromTo("#h1a", {"scale": 1.14, "x": -20}, {"scale": 1, "x": 0}, 0, .35, "back.out(1.8)")
set_("#h1b", {"opacity": 1}, 0)
fromTo("#h1b", {"scale": 1.2, "x": 30}, {"scale": 1, "x": 0}, T["swallowing"] - .05, .32, "back.out(2)")
fromTo("#h1c", {"opacity": 0, "rotation": -14, "scale": .5}, {"opacity": 1, "rotation": -5, "scale": 1}, T["biotin1"], .4, "elastic.out(1,.6)")
fromTo("#h1c", {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, T["biotin1"], .55, "power2.out")
to("#hook", {"opacity": 0, "y": -90, "scale": 1.05}, L[1] - .08, .18, "power3.in")

set_("#big", {"opacity": 1}, 0)
fromTo("#big", {"y": -1100, "rotation": -35}, {"y": 0, "rotation": -8}, 0, .7, "bounce.out")
fromTo("#big", {"rotation": -8}, {"rotation": 6}, T["pills"], .09, "power1.inOut")
fromTo("#big", {"rotation": 6}, {"rotation": -6}, T["pills"] + .09, .09, "power1.inOut")
fromTo("#big", {"rotation": -6}, {"rotation": 0, "scale": 1.12}, T["pills"] + .18, .25, "back.out(3)")
fromTo("#crack", {"strokeDashoffset": 300}, {"strokeDashoffset": 0}, L[1] - .14, .12, "power2.in")
set_("#crack", {"opacity": 1}, L[1] - .14)
fromTo("#big .hl", {"x": 0, "rotation": 0}, {"x": -760, "y": 260, "rotation": -70}, L[1], .55, "power3.in")
fromTo("#big .hr", {"x": 0, "rotation": 0}, {"x": 760, "y": -160, "rotation": 80}, L[1], .55, "power3.in")
set_("#crack", {"opacity": 0}, L[1] + .05)
set_("#big .shine", {"opacity": 0}, L[1])
burst = []
for i in range(30):
    a = i / 30 * 2 * math.pi + rnd.uniform(-.1, .1)
    dist = rnd.uniform(260, 720)
    size = rnd.choice([14, 18, 24, 30, 40])
    burst.append(star(f"bu bu{i}", 540 - size // 2, 990 - size // 2, size, rnd.choice([C["BLUSH"], C["PINK"], C["GOLD"]])))
    fromTo(f".bu{i}", {"x": 0, "y": 0, "scale": .2, "opacity": 1, "rotation": 0},
           {"x": round(math.cos(a) * dist), "y": round(math.sin(a) * dist), "scale": rnd.uniform(.8, 1.6), "opacity": 0, "rotation": 180},
           L[1] + .01, rnd.uniform(.6, 1.0), "expo.out")
flash(L[1] + .01, .9, .35)

# 2 glow-up (inside the hook clip, over the mist photo)
fromTo("#mistw", {"opacity": 0, "scale": 1.18}, {"opacity": 1, "scale": 1}, L[1] - .02, .5, "power2.out")
fromTo("#mistw", {"scale": 1}, {"scale": 1.06}, L[1] + .48, L[2] - L[1] - .4, "none")
pop("#g2a", T["heres"] - .04, .26, y=-30)
fromTo("#g2b", {"opacity": 0, "scale": .82, "y": 20}, {"opacity": 1, "scale": 1, "y": 0}, T["glow"] - .05, .35, "power3.out")
fromTo("#g2b", {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, T["glow"] - .05, .55, "power2.inOut")
for i, (x, y, s) in enumerate([(150, 470, 60), (880, 420, 44), (820, 690, 70), (210, 720, 40)]):
    fromTo(f".gs{i}", {"opacity": 0, "scale": 0, "rotation": -90}, {"opacity": 1, "scale": 1, "rotation": 0}, T["glow"] + .2 + .08 * i, .35, "back.out(3)")
to("#glowup", {"opacity": 0, "scale": 1.25}, L[2] - .14, .16, "power2.in")

# ------------------------------------------------------------------ 3 reveal (the drop)
flash(L[2] - .01, 1.0, .4)
fromTo("#r-glow", {"opacity": 0, "scale": .4}, {"opacity": 1, "scale": 1}, L[2], .6, "expo.out")
fromTo("#r-glow", {"rotation": 0}, {"rotation": 40}, L[2], W3[1] - W3[0], "none")
fromTo("#p3", {"opacity": 1, "y": 900, "rotation": -10}, {"y": 0, "rotation": 0}, L[2], .6, "back.out(1.3)")
fromTo("#p3 .sheen", {"x": -260}, {"x": 520}, L[2] + .45, .7, "power2.inOut")
fromTo("#r-brand", {"opacity": 0, "scaleX": 1.6, "x": -30}, {"opacity": 1, "scaleX": 1, "x": 0}, T["vitonnix"], .5, "power3.out")
fromTo("#r-name", {"opacity": 0, "scale": 1.5, "filter": "blur(14px)"}, {"opacity": 1, "scale": 1, "filter": "blur(0px)"}, T["biotin2"] - .04, .4, "expo.out")
fromTo("#r-sub", {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0}, T["biotin2"] + .1, .35, "power3.out")
fromTo("#r-chip", {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, T["biotin2"] + .2, .35, "back.out(2)")
for i in range(6):
    fromTo(f".os{i}", {"opacity": 0, "scale": 0}, {"opacity": 1, "scale": 1}, L[2] + .3 + .07 * i, .3, "back.out(3)")
fromTo("#orbit", {"rotation": 0}, {"rotation": 60}, L[2], W3[1] - W3[0], "none")

# ------------------------------------------------------------------ 4 one spray
flash(L[3] - .01, .5, .25, "p")
fromTo("#mist2", {"scale": 1.0, "x": 0}, {"scale": 1.1, "x": -30}, L[3], W4[1] - W4[0], "power1.out")
spray = []
for i in range(26):
    a = math.radians(rnd.uniform(-160, -110))
    dist = rnd.uniform(240, 640)
    size = rnd.choice([10, 14, 18, 24])
    spray.append(star(f"sp sp{i}", 712 - size // 2, 930 - size // 2, size, rnd.choice([C["BLUSH"], C["PINK"], C["GOLD"]])))
    t0 = T["spray"] + rnd.uniform(0, .5)
    fromTo(f".sp{i}", {"x": 0, "y": 0, "opacity": 1, "scale": .3}, {"x": round(math.cos(a) * dist), "y": round(math.sin(a) * dist), "opacity": 0, "scale": 1.3},
           t0, rnd.uniform(.7, 1.1), "power2.out")
fromTo("#one", {"opacity": 0, "scale": 2.4, "rotation": -10}, {"opacity": 1, "scale": 1, "rotation": 0}, T["one"] - .04, .35, "expo.out")
fromTo("#onespray", {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}, T["spray"] - .02, .3, "power3.out")
fromTo("#onespray", {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, T["spray"] - .02, .45, "power2.out")
fromTo("#tongue", {"opacity": 0, "x": -80}, {"opacity": 1, "x": 0}, T["under"] - .02, .3, "back.out(2)")
fromTo("#done", {"opacity": 0, "scale": 2.6, "rotation": -18}, {"opacity": 1, "scale": 1, "rotation": -7}, T["done"], .26, "expo.out")
flash(T["done"] + .02, .35, .25)

# ------------------------------------------------------------------ 5 stat: 9X
flash(L[4] - .01, .9, .3)
fromTo("#s5in", {"clipPath": "circle(0% at 50% 45%)"}, {"clipPath": "circle(80% at 50% 45%)"}, L[4] - .02, .5, "power3.out")
pop("#finemist", T["fine"] - .04, .3, y=-30, scale=.9)
roll_start, roll_end = L[4] + .25, T["nine"] + .08
fromTo("#reel", {"yPercent": 0}, {"yPercent": -88.889}, roll_start, roll_end - roll_start, "power3.inOut")
fromTo("#digit", {"opacity": 0, "scale": .6}, {"opacity": 1, "scale": 1}, roll_start - .05, .3, "back.out(2)")
fromTo("#xmark", {"opacity": 0, "scale": 2.2, "rotation": 30}, {"opacity": 1, "scale": 1, "rotation": 0}, T["x"] - .02, .3, "expo.out")
fromTo("#ring", {"strokeDashoffset": 2262}, {"strokeDashoffset": 0}, roll_start, T["absorption"] + .4 - roll_start, "power2.inOut")
fromTo("#ringwrap", {"rotation": -90}, {"rotation": 30}, L[4], W5[1] - W5[0], "none")
fromTo("#bettr", {"opacity": 0, "y": 50}, {"opacity": 1, "y": 0}, T["better"] - .05, .3, "back.out(2)")
fromTo("#absorb", {"opacity": 0, "scaleX": 1.5}, {"opacity": 1, "scaleX": 1}, T["absorption"] - .04, .4, "power3.out")
flash(T["nine"] + .08, .45, .3)
fromTo("#stat", {"scale": 1}, {"scale": 1.06}, T["nine"] + .08, .1, "power2.out")
fromTo("#stat", {"scale": 1.06}, {"scale": 1}, T["nine"] + .18, .25, "power2.inOut")

# ------------------------------------------------------------------ 6 hair, skin, nails
flash(L[5] - .01, .7, .3, "p")
fromTo("#arch", {"opacity": 0, "y": 260, "scale": .9}, {"opacity": 1, "y": 0, "scale": 1}, L[5] - .02, .5, "power3.out")
fromTo("#arch img", {"scale": 1.18}, {"scale": 1.02}, L[5], W6[1] - W6[0], "power1.out")
pop("#madefor", T["made"] - .04, .3, y=-30)
for i, k in enumerate(("hair", "skin", "nails")):
    fromTo(f"#ic{i}", {"opacity": 0, "y": 120, "scale": .4, "rotation": -30 + 30 * i},
           {"opacity": 1, "y": 0, "scale": 1, "rotation": 0}, T[k] - .03, .4, "back.out(2.2)")
    fromTo(f"#il{i}", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, T[k] + .12, .3, "power3.out")

# ------------------------------------------------------------------ 7 flavour + no added sugar
flash(L[6] - .01, .6, .3)
fromTo("#p7", {"opacity": 1, "y": 700, "rotation": 8}, {"y": 0, "rotation": 0}, L[6] - .02, .55, "back.out(1.4)")
fromTo("#p7 .sheen", {"x": -260}, {"x": 520}, L[6] + .5, .7, "power2.inOut")
fromTo("#fl-a", {"opacity": 0, "y": -40}, {"opacity": 1, "y": 0}, T["lychee"] - .04, .35, "back.out(2)")
fromTo("#fl-a", {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, T["lychee"] - .04, .6, "power2.out")
pop("#fl-b", T["flavour"] - .04, .3, y=30)
for i, (sel, t) in enumerate([("#ly0", T["lychee"]), ("#ly1", T["lychee"] + .12), ("#mi0", T["mint"]), ("#mi1", T["mint"] + .1), ("#mi2", T["mint"] + .2)]):
    fromTo(sel, {"opacity": 0, "scale": 0, "rotation": -90 + 40 * i}, {"opacity": 1, "scale": 1, "rotation": 0}, t, .45, "back.out(2.5)")
    fromTo(sel, {"y": 0}, {"y": -40 if i % 2 else 36}, t + .45, 1.2, "sine.inOut")
to("#flav", {"opacity": 0, "scale": .3}, T["no"] - .15, .22, "back.in(2)")
for i, (sel, t) in enumerate([("#bsug", T["no"] - .02), ("#bgmo", T["sugar"] - .05)]):
    fromTo(sel, {"opacity": 0, "scale": 2.4, "rotation": -25 if i else 25}, {"opacity": 1, "scale": 1, "rotation": -6 if i else 6}, t, .28, "expo.out")
pop("#nl1", T["no"] + .15, .3, y=24)
pop("#nl0", T["sugar"] + .05, .3, y=24)

# ------------------------------------------------------------------ 8 certified
flash(L[7] - .01, .9, .3)
fromTo("#cert-h", {"opacity": 0, "x": -120}, {"opacity": 1, "x": 0}, L[7], .4, "power3.out")
fromTo("#tick", {"strokeDashoffset": 120}, {"strokeDashoffset": 0}, T["certified"] + .05, .35, "power2.out")
for i, t in enumerate((T["fssai"], T["gmp"], T["certified"] - .05)):
    fromTo(f"#cb{i}", {"opacity": 0, "scale": 2.6, "rotation": -30 + 25 * i}, {"opacity": 1, "scale": 1, "rotation": -4 + 4 * i}, t - .02, .26, "expo.out")
    fromTo(f"#cl{i}", {"opacity": 0, "y": 24}, {"opacity": 1, "y": 0}, t + .18, .3, "power3.out")
    flash(t + .02, .22, .2, "p")

# ------------------------------------------------------------------ 9 doctors + UK
flash(L[8] - .01, .8, .3)
fromTo("#doc", {"opacity": 0, "x": -300, "rotation": -6}, {"opacity": 1, "x": 0, "rotation": -2}, T["created"] - .05, .45, "back.out(1.6)")
for i in range(3):
    fromTo(f"#dr{i}", {"opacity": 0, "scale": 0, "y": 40}, {"opacity": 1, "scale": 1, "y": 0}, T["three"] + .1 * i, .3, "back.out(3)")
fromTo("#uk", {"opacity": 0, "x": 300, "rotation": 6}, {"opacity": 1, "x": 0, "rotation": 2}, T["uk"] - .15, .45, "back.out(1.6)")
for k in range(4):
    fromTo("#flag", {"skewY": -4 if k % 2 == 0 else 4}, {"skewY": 4 if k % 2 == 0 else -4}, T["uk"] + .3 + .45 * k, .45, "sine.inOut")
pop("#uk-tech", T["sublispray"] - .02, .32, y=30)
fromTo("#p9", {"opacity": 1, "y": 700, "rotation": -6}, {"y": 0, "rotation": -4}, L[8] + .15, .6, "back.out(1.3)")

# ------------------------------------------------------------------ 10 CTA
flash(L[9] - .01, 1.0, .35)
fromTo("#c-glow", {"opacity": 0, "scale": .4}, {"opacity": 1, "scale": 1}, L[9], .6, "expo.out")
fromTo("#p10", {"opacity": 1, "y": 800, "rotation": 10}, {"y": 0, "rotation": 4}, L[9] + .05, .6, "back.out(1.3)")
fromTo("#p10 .sheen", {"x": -260}, {"x": 520}, L[9] + .7, .7, "power2.inOut")
fromTo("#ctaa", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, T["comment"] - .05, .3, "back.out(2)")
fromTo("#kw", {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, T["biotin3"] - .06, .3, "back.out(2.2)")
for i in range(6):
    fromTo(f".ty{i}", {"opacity": 0, "y": -40, "scale": 1.5}, {"opacity": 1, "y": 0, "scale": 1}, T["biotin3"] + .02 + .065 * i, .16, "back.out(3)")
tw.append(f'tl.fromTo(".cur",{{"opacity":1}},{{"opacity":0,"duration":0.22,"yoyo":true,"repeat":13,"ease":"steps(1)","immediateRender":false}},{T["biotin3"]:.3f});')
fromTo("#ctab", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, T["dm"] - .12, .3, "back.out(2)")
fromTo("#tag", {"opacity": 0, "scale": .3, "rotation": 20}, {"opacity": 1, "scale": 1, "rotation": -5}, T["link"] - .1, .4, "back.out(2.4)")
fromTo("#wm", {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, T["link"] - .2, .45, "power3.out")
fromTo("#kw", {"scale": 1}, {"scale": .94}, VOICE_END + .5, .1, "power2.out")
fromTo("#kw", {"scale": .94}, {"scale": 1}, VOICE_END + .6, .2, "back.out(3)")
for i in range(6):
    fromTo(f".cs{i}", {"opacity": 0, "scale": 0}, {"opacity": 1, "scale": 1}, L[9] + .4 + .1 * i, .3, "back.out(3)")
fromTo("#corbit", {"rotation": 0}, {"rotation": 50}, L[9], W10[1] - W10[0], "none")
fromTo(".prog i", {"scaleX": 0}, {"scaleX": 1}, 0, DUR, "none")

# ------------------------------------------------------------------ captions
CW = []
for w in WORDS:
    w = dict(w)
    n = norm(w["w"])
    prev = CW[-1] if CW else None
    if w["line"] == 8 and len(n) == 1 and prev and prev["line"] == 8 and prev.get("acro") and len(prev["w"]) < (5 if prev["w"].startswith("F") else 3):
        prev["w"] += w["w"].upper()
        prev["e"] = w["e"]
        continue
    if w["line"] == 8 and len(n) == 1:
        w["acro"] = True
        w["w"] = w["w"].upper()
    if n == "x" and prev and norm(prev["w"]) == "nine":
        prev["w"] = "9X"
        prev["e"] = w["e"]
        continue
    if n == "sublispray":
        w["w"] = "Sublispray®"
    CW.append(w)
caps_html = []
for ln in LINES:
    if ln["line"] == 10:                       # the CTA card shows these exact words
        continue
    ws = [w for w in CW if w["line"] == ln["line"]]
    chunks, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= 3 or re.search(r"[.?!,]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    for ci, ch in enumerate(chunks):
        cid = f"c{ln['line']}_{ci}"
        start = ch[0]["s"] - .05
        if ci + 1 < len(chunks):
            end = chunks[ci + 1][0]["s"] - .05
        else:
            end = min(ch[-1]["e"] + .4, (LINES[ln["line"]]["start"] - .06) if ln["line"] < len(LINES) else DUR)
        spans = " ".join(f'<span class="w" id="{cid}_{wi}">{w["w"]}</span>' for wi, w in enumerate(ch))
        caps_html.append(f'<div class="cap" id="{cid}"><span class="box">{spans}</span></div>')
        fromTo(f"#{cid}", {"opacity": 0, "y": 22, "scale": .92}, {"opacity": 1, "y": 0, "scale": 1}, max(0, start), .14, "back.out(2.2)")
        set_(f"#{cid}", {"opacity": 0}, end)
        for wi, w in enumerate(ch):
            set_(f"#{cid}_{wi}", {"backgroundColor": C["PLUM"], "color": C["BLUSH"]}, w["s"])
            set_(f"#{cid}_{wi}", {"backgroundColor": "rgba(137,0,69,0)", "color": C["INK"]}, max(w["s"] + .08, w["e"]))
tw.append(f"tl.set({{}}, {{}}, {DUR});")

# ------------------------------------------------------------------ HTML
UKFLAG = ('<svg viewBox="0 0 60 30" width="300" height="150"><clipPath id="ukc-s"><path d="M0,0 v30 h60 v-30 z"/></clipPath>'
          '<clipPath id="ukc-t"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath><g clip-path="url(#ukc-s)">'
          '<path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/>'
          '<path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#ukc-t)" stroke="#C8102E" stroke-width="4"/>'
          '<path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>')
LEAF = '<svg viewBox="0 0 100 60" width="100%" height="100%"><path d="M2 30C20 2 70 -4 98 30 70 64 20 58 2 30Z" fill="#3fae6a"/><path d="M6 30C40 26 70 28 96 30" stroke="#bff0cf" stroke-width="3" fill="none"/></svg>'


def clip(id_, win, track, inner, z, extra=""):
    s, e = win
    return (f'<div id="{id_}" class="clip" style="z-index:{z}" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{track}" data-layout-allow-overflow {extra}>{inner}</div>')


bg_inner = f'''<div class="base"></div><div class="glow" id="g1"></div><div class="glow" id="g2"></div>
<div id="ghost">Biotin Biotin Biotin</div><div id="bgstars">{"".join(bg_stars)}</div><div class="grain"></div>'''

s1_inner = f'''<div id="rain">{"".join(rain)}</div>
<div id="hook"><div class="h1" id="h1a">Still</div><div class="h1" id="h1b">swallowing</div><div class="script in" id="h1c">biotin pills?</div></div>
<div id="big"><b class="hl"></b><b class="hr"></b><i class="shine"></i>
<svg id="crackw" viewBox="0 0 60 180" width="60" height="180"><path id="crack" d="M30 0 L22 30 L36 58 L20 92 L38 124 L24 152 L32 180" stroke="#2a0016" stroke-width="5" fill="none" stroke-dasharray="300" stroke-dashoffset="300" stroke-linejoin="round"/></svg></div>
<div id="burst">{"".join(burst)}</div>
<div id="glowup"><div class="eyebrow light" id="g2a">HERE'S THE</div><div class="script huge" id="g2b">glow-up</div>
{star("gs gs0", 150, 470, 60, C["GOLD"])}{star("gs gs1", 880, 420, 44, C["BLUSH"])}{star("gs gs2", 820, 690, 70, C["PINK"])}{star("gs gs3", 210, 720, 40, C["BLUSH"])}</div>'''

mist1_inner = '<div id="mistw" class="photo in"><img src="assets/img/mist.jpg" alt="" width="1350" height="1350"></div><div class="vign"></div>'

orbit = "".join(star(f"os os{i}", round(260 + 250 * math.cos(i / 6 * 2 * math.pi) - 15), round(250 + 250 * math.sin(i / 6 * 2 * math.pi) - 15), [30, 22, 36, 18, 28, 24][i], [C["GOLD"], C["BLUSH"], C["PINK"]][i % 3]) for i in range(6))
s3_inner = f'''<div id="r-glow" class="halo" style="left:-40px;top:420px;width:640px;height:640px"></div>
<div id="orbit" style="left:30px;top:500px">{orbit}</div>
{pack("p3", 140, 400, 900)}
<div id="r-title"><div id="r-brand" class="in">VITONNIX</div><div id="r-name" class="in">Biotin</div>
<div id="r-sub" class="in">Sublingual oral spray</div><div id="r-chip" class="chip in">Lychee &amp; mint</div></div>'''

s4_inner = f'''<div id="mist2" class="photo"><img src="assets/img/mist.jpg" alt="" width="1350" height="1350"></div><div class="vign"></div>
<div id="spray">{"".join(spray)}</div>
<div id="one" class="in">1</div><div id="onespray" class="script in">spray</div>
<div id="tongue" class="eyebrow in">UNDER YOUR TONGUE</div><div id="done" class="in">Done.</div>'''

digits = "".join(f"<b>{d}</b>" for d in range(1, 10))
s5_inner = f'''<div id="s5in"><div class="halo" style="left:90px;top:380px;width:900px;height:900px"></div>
<div id="finemist" class="script mid in">A fine mist for</div>
<div id="ringwrap"><svg viewBox="0 0 760 760" width="760" height="760"><circle cx="380" cy="380" r="360" stroke="rgba(255,240,246,.14)" stroke-width="10" fill="none"/>
<circle id="ring" cx="380" cy="380" r="360" stroke="{C["PINK"]}" stroke-width="14" fill="none" stroke-linecap="round" stroke-dasharray="2262" stroke-dashoffset="2262"/></svg></div>
<div id="stat"><span id="digit" class="in"><span id="reel">{digits}</span></span><span id="xmark" class="in">X</span></div>
<div id="bettr" class="in">better</div><div id="absorb" class="in">ABSORPTION</div></div>'''

icons = "".join(f'<div class="ic in" id="ic{i}" style="left:{x}px"><img src="assets/img/{n}.png" alt="" width="210" height="210"></div>'
                f'<div class="il in" id="il{i}" style="left:{x - 40}px">{lab}</div>'
                for i, (x, n, lab) in enumerate([(120, "ic-hair", "Hair"), (435, "ic-skin", "Skin"), (750, "ic-nail", "Nails")]))
s6_inner = f'''<div id="arch" class="in"><img src="assets/img/glow.jpg" alt="" width="760" height="808"></div>
<div id="madefor" class="eyebrow in">MADE FOR YOUR</div>{icons}'''

s7_inner = f'''<div class="halo" style="left:160px;top:420px;width:760px;height:760px"></div>
<div id="fl-title"><div id="fl-a" class="script mid in">Lychee &amp; mint</div><div id="fl-b" class="eyebrow light in">FLAVOUR</div></div>
{pack("p7", 410, 560, 660)}
<div id="flav"><div class="lychee in" id="ly0" style="left:90px;top:620px;width:190px;height:190px"></div>
<div class="lychee in" id="ly1" style="left:200px;top:880px;width:130px;height:130px"></div>
<div class="leaf in" id="mi0" style="left:760px;top:560px;width:220px;height:132px">{LEAF}</div>
<div class="leaf in" id="mi1" style="left:820px;top:820px;width:170px;height:102px">{LEAF}</div>
<div class="leaf in" id="mi2" style="left:700px;top:1000px;width:140px;height:84px">{LEAF}</div></div>
<div class="badge in" id="bgmo" style="left:60px;top:700px"><img src="assets/img/b-nongmo.png" alt="" width="270" height="270"></div>
<div class="badge in" id="bsug" style="left:750px;top:700px"><img src="assets/img/b-sugar.png" alt="" width="270" height="270"></div>
<div class="blab in" id="nl0" style="left:30px;top:990px">Non-GMO</div><div class="blab in" id="nl1" style="left:720px;top:990px">No added sugar</div>'''

s8_inner = f'''<div class="halo" style="left:90px;top:520px;width:900px;height:900px"></div>
<div id="cert-h" class="in"><span class="serif-it">Certified</span><svg viewBox="0 0 100 80" width="110" height="88"><path id="tick" d="M8 42 L36 70 L92 10" stroke="{C["PINK"]}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="120" stroke-dashoffset="120"/></svg></div>
<div class="badge in" id="cb0" style="left:110px;top:520px"><img src="assets/img/b-fssai.png" alt="" width="330" height="330"></div>
<div class="blab in" id="cl0" style="left:110px;top:860px">FSSAI</div>
<div class="badge in" id="cb1" style="left:640px;top:520px"><img src="assets/img/b-gmp.png" alt="" width="330" height="330"></div>
<div class="blab in" id="cl1" style="left:640px;top:860px">GMP</div>
<div class="badge in" id="cb2" style="left:375px;top:900px"><img src="assets/img/b-fssc.png" alt="" width="330" height="330"></div>
<div class="blab in" id="cl2" style="left:240px;top:1240px;width:600px">ISO FSSC 22000 v6</div>'''

s9_inner = f'''{pack("p9", 90, 760, 540)}
<div id="doc" class="card in"><span class="k">CREATED BY</span><span class="v">3 doctors</span>
<span class="drs"><i id="dr0" class="in"></i><i id="dr1" class="in"></i><i id="dr2" class="in"></i></span></div>
<div id="uk" class="card r in"><div id="flag">{UKFLAG}</div><span class="v small">Developed in the UK</span>
<span id="uk-tech" class="k in">SUBLISPRAY® TECHNOLOGY</span></div>'''

cstars = "".join(star(f"cs cs{i}", round(200 + 230 * math.cos(i / 6 * 2 * math.pi) - 14), round(230 + 230 * math.sin(i / 6 * 2 * math.pi) - 14), [28, 20, 34, 18, 26, 22][i], [C["GOLD"], C["BLUSH"], C["PINK"]][i % 3]) for i in range(6))
s10_inner = f'''<div id="c-glow" class="halo" style="left:180px;top:620px;width:720px;height:720px"></div>
<div id="corbit" style="left:340px;top:750px">{cstars}</div>
{pack("p10", 437, 700, 580)}
<div id="cta"><div id="ctaa" class="eyebrow light in">COMMENT</div>
<div id="kw" class="in"><span class="ty ty0">B</span><span class="ty ty1">I</span><span class="ty ty2">O</span><span class="ty ty3">T</span><span class="ty ty4">I</span><span class="ty ty5">N</span><i class="cur"></i></div>
<div id="ctab" class="in">and we'll DM you the link</div></div>
<div id="tag" class="in"><span class="k">AVAILABLE ON</span><span class="v">Tata 1mg</span></div>
<div id="wm" class="in"><span class="serif-it">Vitonnix</span> <span class="script">Future of Vitamins</span></div>'''

CSS = Template(r"""
@font-face { font-family: "Fraunces"; font-weight: 600; src: url("assets/fonts/fraunces-600.ttf"); }
@font-face { font-family: "Fraunces"; font-weight: 800; src: url("assets/fonts/fraunces-800.ttf"); }
@font-face { font-family: "Fraunces"; font-weight: 900; src: url("assets/fonts/fraunces-900.ttf"); }
@font-face { font-family: "Fraunces"; font-style: italic; font-weight: 500; src: url("assets/fonts/fraunces-500i.ttf"); }
@font-face { font-family: "Fraunces"; font-style: italic; font-weight: 700; src: url("assets/fonts/fraunces-700i.ttf"); }
@font-face { font-family: "Great Vibes"; font-weight: 400; src: url("assets/fonts/greatvibes-400.ttf"); }
@font-face { font-family: "Montserrat"; font-weight: 500; src: url("assets/fonts/montserrat-500.ttf"); }
@font-face { font-family: "Montserrat"; font-weight: 700; src: url("assets/fonts/montserrat-700.ttf"); }
@font-face { font-family: "Montserrat"; font-weight: 800; src: url("assets/fonts/montserrat-800.ttf"); }
@font-face { font-family: "Montserrat"; font-weight: 900; src: url("assets/fonts/montserrat-900.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: ${DARK}; }
body { font-family: "Montserrat", sans-serif; color: ${BLUSH}; }
#root { position: relative; width: 100%; height: 100%; overflow: hidden; background: ${DARK}; }
.clip { position: absolute; inset: 0; }
.in { opacity: 0; }
/* background layer */
.base { position: absolute; inset: 0; background: radial-gradient(1150px 1250px at 50% 44%, ${PLUM} 0%, ${DEEP} 52%, ${DARK} 100%); }
.glow { position: absolute; border-radius: 50%; filter: blur(90px); }
#g1 { left: -260px; top: 260px; width: 820px; height: 820px; background: rgba(255,95,174,.34); }
#g2 { left: 420px; top: 1120px; width: 900px; height: 900px; background: rgba(194,24,122,.42); }
#ghost { position: absolute; left: 0; top: 1500px; white-space: nowrap; font-family: "Fraunces"; font-style: italic; font-weight: 700; font-size: 380px; line-height: 1; color: rgba(255,95,174,.10); }
#bgstars { position: absolute; inset: 0; }
.star { position: absolute; display: block; opacity: 0; }
.star svg { display: block; filter: drop-shadow(0 0 10px rgba(255,180,220,.8)); }
.grain { position: absolute; inset: 0; opacity: .13; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='240' height='240' filter='url(%23n)' opacity='.9'/></svg>"); }
.top { position: absolute; left: 60px; right: 60px; top: 262px; display: flex; align-items: center; gap: 22px; }
.brand { font-weight: 800; font-size: 28px; letter-spacing: 6px; color: ${PLUM}; padding: 8px 22px; border-radius: 24px; background: ${BLUSH}; box-shadow: 0 10px 30px rgba(20,0,10,.35); }
.prog { flex: 1; height: 6px; border-radius: 3px; background: rgba(255,240,246,.18); overflow: hidden; }
.prog i { display: block; height: 100%; background: ${PINK}; transform-origin: 0 50%; }
/* type system */
.h1 { position: absolute; left: 70px; font-family: "Fraunces"; font-weight: 900; font-size: 150px; line-height: 1; letter-spacing: -4px; color: ${BLUSH}; text-shadow: 0 10px 40px rgba(30,0,15,.55); }
#h1a { top: 320px; } #h1b { top: 470px; }
.script { font-family: "Great Vibes"; font-weight: 400; color: ${PINK}; line-height: 1.1; text-shadow: 0 0 30px rgba(255,95,174,.55); }
#h1c { position: absolute; left: 90px; top: 650px; font-size: 168px; }
.script.huge { font-size: 290px; color: ${BLUSH}; text-shadow: 0 6px 30px rgba(51,0,27,.7), 0 0 50px rgba(255,95,174,.9), 0 0 120px rgba(255,95,174,.6); }
.script.mid { font-size: 150px; }
.eyebrow { display: inline-block; font-weight: 800; font-size: 38px; letter-spacing: 8px; padding: 10px 28px; border-radius: 40px; background: ${BLUSH}; color: ${PLUM}; }
.eyebrow.light { background: transparent; color: ${BLUSH}; padding: 0; text-shadow: 0 4px 20px rgba(30,0,15,.6); }
.chip { display: inline-block; padding: 12px 30px 14px; border-radius: 40px; background: ${PLUM}; color: ${BLUSH}; font-weight: 800; font-size: 38px; border: 3px solid rgba(255,240,246,.35); }
.serif-it { font-family: "Fraunces"; font-style: italic; font-weight: 700; }
.halo { position: absolute; border-radius: 50%; background: radial-gradient(circle, rgba(255,95,174,.55) 0%, rgba(194,24,122,.25) 40%, rgba(194,24,122,0) 70%); }
/* capsules */
.pl { position: absolute; }
.pl b { position: absolute; top: 0; width: 50%; height: 100%; }
.pl .hl { left: 0; background: linear-gradient(180deg, #c0136d 0%, ${PLUM} 70%, #5e0030 100%); }
.pl .hr { right: 0; background: linear-gradient(180deg, #ffffff 0%, #f6dde8 70%, #e2bccd 100%); }
.pl .shine { position: absolute; left: 10%; top: 16%; width: 46%; height: 16%; border-radius: 99px; background: rgba(255,255,255,.55); }
#rain { position: absolute; inset: 0; }
.rp { opacity: 0; filter: drop-shadow(0 14px 18px rgba(20,0,10,.4)); }
#big { position: absolute; left: 310px; top: 900px; width: 460px; height: 180px; opacity: 0; filter: drop-shadow(0 30px 40px rgba(20,0,10,.55)); }
#big b { position: absolute; top: 0; width: 230px; height: 180px; }
#big .hl { left: 0; border-radius: 90px 0 0 90px; background: linear-gradient(180deg, #d0167a 0%, ${PLUM} 70%, #5e0030 100%); }
#big .hr { left: 230px; border-radius: 0 90px 90px 0; background: linear-gradient(180deg, #ffffff 0%, #f6dde8 70%, #e2bccd 100%); }
#big .shine { position: absolute; left: 40px; top: 26px; width: 210px; height: 26px; border-radius: 13px; background: rgba(255,255,255,.5); }
#crackw { position: absolute; left: 200px; top: 0; }
#crack { opacity: 0; }
#burst { position: absolute; inset: 0; }
#glowup { position: absolute; inset: 0; }
#g2a { position: absolute; left: 0; right: 0; top: 400px; text-align: center; opacity: 0; font-size: 44px; }
#g2b { position: absolute; left: 0; right: 0; top: 440px; text-align: center; opacity: 0; }
.photo { position: absolute; left: -270px; top: 160px; width: 1350px; height: 1350px; transform-origin: 72% 60%; }
.photo img { display: block; width: 100%; height: 100%;
  -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 14%, #000 86%, transparent 100%); mask-image: linear-gradient(180deg, transparent 0%, #000 14%, #000 86%, transparent 100%); }
.vign { position: absolute; inset: 0; background: radial-gradient(900px 1300px at 50% 50%, rgba(51,0,27,0) 55%, rgba(51,0,27,.75) 100%); }
/* packshot */
.pack { position: absolute; transform-origin: 50% 80%; filter: drop-shadow(0 40px 60px rgba(20,0,10,.55)); overflow: hidden; border-radius: 999px; }
.pack img { display: block; width: 100%; height: 100%; }
.sheen { position: absolute; top: -10%; left: 0; width: 120px; height: 120%; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.65), rgba(255,255,255,0)); transform-origin: 50% 50%; }
/* 3 reveal */
#orbit, #corbit { position: absolute; width: 0; height: 0; }
#r-title { position: absolute; left: 510px; right: 50px; top: 520px; }
#r-brand { transform-origin: 0 50%; font-weight: 700; font-size: 46px; letter-spacing: 12px; color: ${BLUSH}; }
#r-name { font-family: "Fraunces"; font-style: italic; font-weight: 700; font-size: 165px; line-height: 1; color: ${PINK}; margin-top: 6px; text-shadow: 0 0 40px rgba(255,95,174,.5); transform-origin: 0 50%; }
#r-sub { font-weight: 700; font-size: 40px; color: ${BLUSH}; margin-top: 28px; }
#r-chip { margin-top: 30px; }
/* 4 one spray */
#spray { position: absolute; inset: 0; }
#one { position: absolute; left: 60px; top: 300px; font-family: "Fraunces"; font-weight: 900; font-size: 560px; line-height: .9; color: ${BLUSH}; text-shadow: 0 20px 80px rgba(30,0,15,.6); transform-origin: 50% 60%; }
#onespray { position: absolute; left: 340px; top: 560px; font-size: 230px; color: ${BLUSH}; text-shadow: 0 0 40px rgba(255,95,174,.9); }
#tongue { position: absolute; left: 70px; top: 860px; }
#done { position: absolute; left: 80px; top: 1070px; padding: 6px 44px 18px; border-radius: 30px; background: ${PINK}; color: ${DARK};
  font-family: "Fraunces"; font-style: italic; font-weight: 700; font-size: 128px; line-height: 1.1; box-shadow: 0 24px 70px rgba(255,95,174,.55); }
/* 5 stat */
#s5in { position: absolute; inset: 0; }
#ghost5 { position: absolute; left: -40px; top: 1150px; font-family: "Fraunces"; font-weight: 900; font-size: 250px; color: rgba(255,95,174,.10); letter-spacing: -6px; white-space: nowrap; }
#finemist { position: absolute; left: 0; right: 0; top: 310px; text-align: center; font-size: 120px; }
#ringwrap { position: absolute; left: 160px; top: 470px; width: 760px; height: 760px; }
#stat { position: absolute; left: 0; right: 0; top: 560px; height: 560px; display: flex; justify-content: center; align-items: center; gap: 0;
  font-family: "Fraunces"; font-weight: 900; font-size: 500px; line-height: 1; color: ${BLUSH}; text-shadow: 0 20px 90px rgba(255,95,174,.55); }
#digit { display: block; height: 500px; overflow: hidden; }
#reel { display: block; }
#reel b { display: block; height: 500px; line-height: 500px; font-weight: 900; }
#xmark { display: block; color: ${PINK}; font-style: italic; font-size: 400px; margin-left: 8px; }
#bettr { position: absolute; left: 0; right: 0; top: 1060px; text-align: center; font-family: "Fraunces"; font-style: italic; font-weight: 500; font-size: 96px; color: ${BLUSH}; }
#absorb { position: absolute; left: 0; right: 0; top: 1180px; text-align: center; font-weight: 900; font-size: 74px; letter-spacing: 6px; color: ${PINK}; }
/* 6 benefits */
#arch { position: absolute; left: 160px; top: 330px; width: 760px; height: 808px; border-radius: 380px 380px 48px 48px; overflow: hidden;
  border: 8px solid ${BLUSH}; box-shadow: 0 40px 90px rgba(20,0,10,.6); }
#arch img { display: block; width: 100%; height: 100%; object-fit: cover; transform-origin: 55% 35%; }
#madefor { position: absolute; left: 0; right: 0; width: max-content; margin: 0 auto; top: 372px; }
.ic { position: absolute; top: 1010px; width: 210px; height: 210px; border-radius: 50%; box-shadow: 0 20px 50px rgba(20,0,10,.55); }
.ic img { display: block; width: 100%; height: 100%; }
.il { position: absolute; top: 1222px; width: 290px; text-align: center; font-family: "Fraunces"; font-style: italic; font-weight: 700; font-size: 58px; color: ${BLUSH}; text-shadow: 0 4px 20px rgba(30,0,15,.6); }
/* 7 flavour */
#fl-title { position: absolute; left: 0; right: 0; top: 300px; text-align: center; }
#fl-a { font-size: 150px; }
#fl-b { margin-top: -6px; font-size: 40px; letter-spacing: 14px; }
.lychee { position: absolute; border-radius: 50%;
  background: radial-gradient(circle at 34% 30%, #ff8f9f 0%, #e23a55 35%, #a3122f 80%, #6e0a20 100%);
  box-shadow: inset 0 -10px 24px rgba(60,0,15,.5), 0 20px 40px rgba(20,0,10,.45); }
.lychee::after { content: ""; position: absolute; inset: 0; border-radius: 50%; opacity: .45;
  background: radial-gradient(circle, rgba(255,210,220,.9) 0 2px, transparent 3px) 0 0 / 18px 18px; }
.leaf { position: absolute; filter: drop-shadow(0 14px 20px rgba(20,0,10,.45)); }
.leaf svg { display: block; }
.badge { position: absolute; border-radius: 50%; filter: drop-shadow(0 24px 40px rgba(20,0,10,.55)); }
.badge img { display: block; }
#nosugar { position: absolute; left: 0; right: 0; width: max-content; margin: 0 auto; top: 1210px; }
.chip.big { font-size: 40px; background: ${BLUSH}; color: ${PLUM}; border: 0; }
/* 8 certified */
#cert-h { position: absolute; left: 70px; top: 320px; display: flex; align-items: center; gap: 24px; font-size: 150px; line-height: 1.05; color: ${BLUSH}; }
.blab { position: absolute; width: 330px; text-align: center; font-weight: 800; font-size: 40px; letter-spacing: 3px; color: ${BLUSH}; }
/* 9 doctors + UK */
.card { position: absolute; padding: 28px 44px 34px; border-radius: 40px; background: ${BLUSH}; color: ${INK}; box-shadow: 0 30px 70px rgba(20,0,10,.55); }
#doc { left: 70px; top: 330px; }
#uk { right: 70px; top: 700px; text-align: right; display: flex; flex-direction: column; align-items: flex-end; }
.card .k { display: block; font-weight: 800; font-size: 30px; letter-spacing: 6px; color: ${PLUM}; }
.card .v { display: block; font-family: "Fraunces"; font-weight: 900; font-size: 116px; line-height: 1.04; letter-spacing: -3px; color: ${INK}; }
.card .v.small { font-size: 54px; letter-spacing: -1px; margin: 18px 0 8px; }
#flag { width: 300px; height: 150px; border-radius: 14px; overflow: hidden; transform-origin: 0 50%; box-shadow: 0 10px 24px rgba(20,0,10,.3); }
#flag svg { display: block; }
.drs { display: flex; gap: 16px; margin-top: 16px; }
.drs i { display: block; width: 84px; height: 84px; border-radius: 50%; background: ${PLUM}; position: relative; }
.drs i::before, .drs i::after { content: ""; position: absolute; background: ${BLUSH}; border-radius: 5px; }
.drs i::before { left: 22px; top: 37px; width: 40px; height: 10px; } .drs i::after { left: 37px; top: 22px; width: 10px; height: 40px; }
/* 10 CTA */
#cta { position: absolute; left: 0; right: 0; top: 300px; text-align: center; }
#ctaa { font-size: 46px; letter-spacing: 12px; }
#kw { display: block; width: max-content; margin: 14px auto 18px; padding: 8px 56px 22px; border-radius: 40px; background: ${PINK}; color: ${DARK};
  font-family: "Fraunces"; font-weight: 900; font-size: 168px; line-height: 1.05; letter-spacing: 6px; box-shadow: 0 24px 80px rgba(255,95,174,.6); }
.ty { display: inline-block; }
.cur { display: inline-block; width: 12px; height: 132px; margin-left: 10px; vertical-align: -12px; border-radius: 6px; background: ${DARK}; }
#ctab { display: inline-block; padding: 10px 30px 14px; border-radius: 30px; background: ${BLUSH}; color: ${PLUM}; font-weight: 800; font-size: 46px; }
#tag { position: absolute; left: 640px; top: 980px; padding: 18px 34px 24px; border-radius: 28px; background: ${BLUSH}; border: 5px solid ${PLUM};
  box-shadow: 0 24px 60px rgba(20,0,10,.5); transform-origin: 20% 0; }
#tag .k { display: block; font-weight: 800; font-size: 28px; letter-spacing: 5px; color: ${PLUM}; }
#tag .v { display: block; font-family: "Fraunces"; font-weight: 900; font-size: 70px; line-height: 1.05; color: ${INK}; }
#wm { position: absolute; left: 0; right: 0; top: 1330px; text-align: center; font-size: 84px; color: ${BLUSH}; }
#wm .script { font-size: 76px; }
/* captions */
#caps .cap { position: absolute; left: 50px; right: 50px; top: 1330px; text-align: center; opacity: 0; }
#caps .box { display: inline-block; max-width: 980px; padding: 12px 22px 16px; border-radius: 28px; background: rgba(255,240,246,.96);
  box-shadow: 0 16px 44px rgba(20,0,10,.45); font-weight: 800; font-size: 60px; line-height: 1.15; letter-spacing: -1px; color: ${INK}; }
#caps .w { display: inline-block; padding: 2px 12px 6px; border-radius: 16px; }
#fx { z-index: 9; pointer-events: none; }
#flash { position: absolute; inset: 0; background: #fff6fa; opacity: 0; }
#flashp { position: absolute; inset: 0; background: ${PINK}; opacity: 0; mix-blend-mode: screen; }
""").substitute(C)

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Vitonnix Biotin 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="1080" data-height="1920">
      {clip("bg", (0, DUR), 0, bg_inner, 0, "data-layout-ignore")}
      {clip("s-mist1", W_MIST1, 1, mist1_inner, 1)}
      {clip("s1", W1, 2, s1_inner, 3)}
      {clip("s3", W3, 2, s3_inner, 3)}
      {clip("s4", W4, 2, s4_inner, 3)}
      {clip("s5", W5, 2, s5_inner, 3)}
      {clip("s6", W6, 2, s6_inner, 3)}
      {clip("s7", W7, 2, s7_inner, 3)}
      {clip("s8", W8, 2, s8_inner, 3)}
      {clip("s9", W9, 2, s9_inner, 3)}
      {clip("s10", W10, 2, s10_inner, 3)}
      {clip("ui", (0, DUR), 3, '<div class="top"><span class="brand">VITONNIX</span><span class="prog"><i></i></span></div>', 6)}
      {clip("caps", (0, DUR), 4, "".join(caps_html), 7)}
      {clip("fx", (0, DUR), 5, '<div id="flash"></div><div id="flashp"></div>', 9, "data-layout-ignore")}
      <audio id="mix" src="{AUDIO}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(tw)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(html)
print(f"index.html written: {DUR}s, {len(tw)} timeline calls, audio {AUDIO}")
