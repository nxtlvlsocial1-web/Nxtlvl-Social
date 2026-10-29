"""Vitonnix SubliSpray reel: writes index.html. 1080x1920, 30 fps, about 25 s.

python3 build/generate.py      (from the project root, after build/voice.py; build/audio.py adds the music mix)

Everything on screen is built in code: the bottles are inline SVG (no product photos were available in this session,
and we only use images we have rights to), the mist is radial-gradient circles, the icons are CSS shapes. One paused
GSAP timeline drives it all; captions are word-highlighted from build/words.json.

Brand colours are the placeholder kit in brands/vitonnix/brand.md. Swap them when the real kit arrives.
Claims on screen are limited to format and convenience plus facts from the client's press (three doctor founders,
developed in the UK, sold on Tata 1mg). No absorption or efficacy claims.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
LINES = json.load(open(os.path.join(ROOT, "voice", "lines.json")))["lines"]
WORDS = json.load(open(os.path.join(B, "words.json")))
VOICE_END = LINES[-1]["end"]
DUR = round(VOICE_END + 2.0, 2)
FPS = 30

INK, TEAL, MIST, WHITE = "#0b3c49", "#0e7c86", "#eaf6f7", "#ffffff"
SUN, CORAL, VIOLET = "#f2b134", "#e4572e", "#7b5ea7"
AUDIO = "assets/audio/mix.wav" if os.path.exists(os.path.join(ROOT, "assets", "audio", "mix.wav")) else "assets/audio/voice.wav"


def word(line, text, nth=1, key="s"):
    hits = [w for w in WORDS if w["line"] == line and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(text.lower())]
    if len(hits) < nth:
        raise SystemExit(f"cue word {text!r} not found in line {line}")
    return hits[nth - 1][key]


L = [ln["start"] for ln in LINES]
E = [ln["end"] for ln in LINES]
T = {
    "still": word(1, "still"), "swallowing": word(1, "swallowing"), "your": word(1, "your"), "vitamins": word(1, "vitamins"),
    "meet": word(2, "meet"), "vitonnix": word(2, "vitonnix"), "sublispray": word(2, "sublispray"),
    "vitamins2": word(3, "vitamins"), "spray": word(3, "spray"), "not": word(3, "not"), "swallow": word(3, "swallow"),
    "two": word(4, "two"), "sprays": word(4, "sprays"), "tongue": word(4, "tongue"), "done": word(4, "done"),
    "pills": word(5, "pills"), "water": word(5, "water"), "chalky": word(5, "chalky"), "aftertaste": word(5, "aftertaste"),
    "vitd": word(6, "vitamin"), "d": word(6, "d"), "b12": word(6, "b12"), "biotin": word(6, "biotin"),
    "one": word(7, "one"), "bottle": word(7, "bottle"), "wherever": word(7, "wherever"), "day": word(7, "day"), "takes": word(7, "takes"),
    "created": word(8, "created"), "three": word(8, "three"), "doctors": word(8, "doctors"), "developed": word(8, "developed"), "uk": word(8, "uk"),
    "available": word(9, "available"), "tata": word(9, "tata"), "g": word(9, "g"),
    "comment": word(10, "comment"), "spraykw": word(10, "spray"), "dm": word(10, "dm"), "link": word(10, "link"),
    "end": DUR,
}
json.dump({"l": L, "e": E, **T}, open(os.path.join(B, "cues.json"), "w"))

# scene windows (clip data-start / data-duration)
S_HOOK = (0, L[1])
S_HERO = (L[1], L[4])            # bottle hero through "done."
S_NO = (L[4], L[5])              # dark "No pills" scene
S_TRIO = (L[5], L[7])            # three bottles + "wherever"
S_TRUST = (L[7], L[8])           # doctors / UK
S_SHOP = (L[8], L[9])            # Tata 1mg
S_END = (L[9], DUR)

tw = []  # timeline lines


def J(o):
    return json.dumps(o, separators=(",", ":"))


def fromTo(sel, a, b, t, dur=.3, ease="back.out(2)"):
    b = {**b, "duration": dur, "ease": ease, "immediateRender": False}
    tw.append(f'tl.fromTo({J(sel)},{J(a)},{J(b)},{t:.3f});')


def to(sel, b, t, dur=.2, ease="power3.in"):
    b = {**b, "duration": dur, "ease": ease}
    tw.append(f'tl.to({J(sel)},{J(b)},{t:.3f});')


def set_(sel, b, t):
    tw.append(f'tl.set({J(sel)},{J(b)},{t:.3f});')


def pop(sel, t, dur=.26, y=34, scale=.72, ease="back.out(2.4)"):
    fromTo(sel, {"opacity": 0, "y": y, "scale": scale}, {"opacity": 1, "y": 0, "scale": 1}, t, dur, ease)


def flash(t, a=1.0, d=.3):
    set_("#flash", {"opacity": a}, t)
    to("#flash", {"opacity": 0}, t + .02, d, "power2.out")


def bottle(id_, accent, name, sub, x, y, scale=1.0, extra="", text=None):
    text = text or accent
    """An inline-SVG spray bottle. viewBox 300x700; scaled by CSS width."""
    w = int(300 * scale)
    return f'''<div id="{id_}" class="bottle {extra}" data-layout-ignore style="left:{x}px;top:{y}px;width:{w}px;height:{int(700 * scale)}px">
<svg viewBox="0 0 300 700" width="{w}" height="{int(700 * scale)}" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="{id_}-body" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#f7fbfb"/><stop offset="1" stop-color="#d9e8eb"/></linearGradient>
<linearGradient id="{id_}-cap" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity=".85"/><stop offset=".6" stop-color="#cfe6ea" stop-opacity=".55"/><stop offset="1" stop-color="#9fc6cc" stop-opacity=".6"/></linearGradient>
<linearGradient id="{id_}-acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity=".78"/></linearGradient>
</defs>
<ellipse cx="150" cy="684" rx="110" ry="12" fill="#0b3c49" opacity=".12"/>
<rect x="60" y="190" width="180" height="486" rx="42" fill="url(#{id_}-body)" stroke="#c9dde1" stroke-width="2"/>
<rect x="60" y="190" width="180" height="486" rx="42" fill="none" stroke="#ffffff" stroke-width="6" opacity=".55"/>
<rect x="78" y="212" width="18" height="430" rx="9" fill="#ffffff" opacity=".7"/>
<rect x="60" y="296" width="180" height="20" fill="url(#{id_}-acc)"/>
<rect x="60" y="326" width="180" height="214" fill="#ffffff" opacity=".9"/>
<text x="150" y="372" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" letter-spacing="3" fill="{INK}">VITONNIX</text>
<text x="150" y="404" text-anchor="middle" font-family="Montserrat" font-weight="600" font-size="15" letter-spacing="4" fill="{TEAL}">SUBLISPRAY</text>
<rect x="88" y="420" width="124" height="4" rx="2" fill="{accent}"/>
<text x="150" y="468" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="{text}">{name}</text>
<text x="150" y="500" text-anchor="middle" font-family="Montserrat" font-weight="600" font-size="17" fill="{INK}" opacity=".75">{sub}</text>
<text x="150" y="526" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="13" letter-spacing="3" fill="{INK}" opacity=".55">ORAL SPRAY</text>
<rect x="60" y="540" width="180" height="20" fill="url(#{id_}-acc)"/>
<path d="M96 190 C96 160 112 148 150 148 C188 148 204 160 204 190 Z" fill="{accent}"/>
<rect x="104" y="150" width="92" height="20" rx="8" fill="{accent}"/>
<rect x="92" y="38" width="116" height="122" rx="30" fill="url(#{id_}-cap)" stroke="#b9d7dc" stroke-width="2"/>
<rect x="104" y="48" width="14" height="100" rx="7" fill="#ffffff" opacity=".8"/>
<rect x="139" y="14" width="22" height="40" rx="6" fill="{INK}"/>
<rect x="128" y="8" width="44" height="14" rx="7" fill="{INK}"/>
</svg></div>'''


def mist(id_, x, y, n=7):
    """Mist puff emitter positioned at (x,y) of the frame; circles are tweened later with puff()."""
    dots = "".join(f'<i class="md md{i}"></i>' for i in range(n))
    return f'<div id="{id_}" class="mist" style="left:{x}px;top:{y}px">{dots}</div>'


def puff(id_, t, dirx=0, diry=-1, spread=260, n=7, dur=.62, big=1.0):
    import math
    for i in range(n):
        a = (i / max(1, n - 1) - .5) * 1.25               # fan angle
        bx, by = dirx, diry
        ca, sa = math.cos(a), math.sin(a)
        dx, dy = (bx * ca - by * sa) * spread * (0.6 + 0.5 * ((i * 7) % 5) / 4), (bx * sa + by * ca) * spread * (0.6 + 0.5 * ((i * 3) % 5) / 4)
        fromTo(f"#{id_} .md{i}", {"x": 0, "y": 0, "scale": .15, "opacity": .95},
               {"x": round(dx, 1), "y": round(dy, 1), "scale": round(1.4 * big + .25 * (i % 3), 2), "opacity": 0}, t + .02 * i, dur, "power2.out")


# ---------------------------------------------------------------- captions
caps_html, k = [], 0
CWORDS = []
for w in WORDS:
    if w["line"] == 9 and w["w"] in ("M", "G."):
        CWORDS[-1]["w"] = "1mg." if w["w"] == "G." else "1mg"
        CWORDS[-1]["e"] = w["e"]
        continue
    CWORDS.append(dict(w))
for ln in LINES:
    ws = [w for w in CWORDS if w["line"] == ln["line"]]
    # chunk into <= 4 words, breaking at punctuation
    chunks, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= 4 or re.search(r"[.?!,]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    dark = ln["line"] == 5
    slam = ln["line"] in (1, 4, 10) and len(chunks)
    for ci, ch in enumerate(chunks):
        cid = f"c{ln['line']}_{ci}"
        start = ch[0]["s"] - .05
        nxt = None
        # the chunk stays until the next chunk starts (or the line ends + tail)
        if ci + 1 < len(chunks):
            nxt = chunks[ci + 1][0]["s"] - .05
        else:
            nxt = min(ch[-1]["e"] + .45, (LINES[ln["line"]]["start"] - .06) if ln["line"] < len(LINES) else DUR)
        spans = " ".join(f'<span class="w" id="{cid}_{wi}">{w["w"]}</span>' for wi, w in enumerate(ch))
        cls = "cap" + (" dark" if dark else "") + (" slam" if (slam and ci == 0 and ln["line"] in (1, 10)) else "")
        caps_html.append(f'<div class="{cls}" id="{cid}"><span class="box">{spans}</span></div>')
        if "slam" in cls:
            fromTo(f"#{cid}", {"opacity": 0, "scale": 1.7}, {"opacity": 1, "scale": 1}, max(0, start), .2, "expo.out")
        else:
            fromTo(f"#{cid}", {"opacity": 0, "y": 18, "scale": .94}, {"opacity": 1, "y": 0, "scale": 1}, max(0, start), .13, "back.out(2)")
        set_(f"#{cid}", {"opacity": 0}, nxt)
        hi_bg, off_fg = TEAL, (MIST if dark else INK)
        for wi, w in enumerate(ch):
            set_(f"#{cid}_{wi}", {"backgroundColor": hi_bg, "color": "#ffffff"}, w["s"])
            set_(f"#{cid}_{wi}", {"backgroundColor": "rgba(14,124,134,0)", "color": off_fg}, max(w["s"] + .06, w["e"]))

# ---------------------------------------------------------------- scenes
# HOOK
set_("#hk0", {"opacity": 1}, 0); set_("#hk1", {"opacity": 1}, 0)
fromTo("#hk0", {"scale": 1.18, "y": -10}, {"scale": 1, "y": 0}, 0, .3, "back.out(2)")
fromTo("#hk1", {"scale": 1.12, "y": -10}, {"scale": 1, "y": 0}, T["swallowing"], .26, "back.out(2)")
pop("#hk2", T["your"], .22)
fromTo("#hk3", {"opacity": 0, "scale": .4, "rotation": -6}, {"opacity": 1, "scale": 1, "rotation": 0}, T["vitamins"], .32, "back.out(2.4)")
# capsule drops in and bounces, then wobbles
fromTo("#cap", {"y": -900, "rotation": -40, "opacity": 1}, {"y": 0, "rotation": 8}, 0.02, .6, "bounce.out")
fromTo("#cap", {"rotation": 8}, {"rotation": -6}, T["vitamins"], .25, "power1.inOut")
fromTo("#qm", {"opacity": 0, "scale": .3, "rotation": 20}, {"opacity": 1, "scale": 1, "rotation": 0}, T["vitamins"] + .12, .3, "back.out(3)")
to("#hookwrap", {"opacity": 0, "y": -80, "scale": 1.06}, L[1] - .16, .16)
flash(L[1] - .02, 1.0, .34)

# HERO: bottle rises
fromTo("#b1", {"y": 1200, "rotation": -14, "opacity": 1}, {"y": 0, "rotation": 0}, L[1] - .02, .6, "back.out(1.4)")
pop("#meet", T["meet"], .22)
fromTo("#wm", {"opacity": 0, "scale": .6, "y": 30}, {"opacity": 1, "scale": 1, "y": 0}, T["vitonnix"], .3, "back.out(2.2)")
fromTo("#wm2", {"opacity": 0, "x": -60}, {"opacity": 1, "x": 0}, T["sublispray"], .3, "back.out(2)")
puff("m1", T["sublispray"] + .05, 0, -1, 230, big=.9)
flash(T["sublispray"] + .02, .35, .25)
# "Spray, not swallow"
to("#heromeet", {"opacity": 0, "y": -40}, L[2] - .02, .16)
pop("#sp0", T["vitamins2"], .22)
fromTo("#sp1", {"opacity": 0, "scale": .3, "rotation": -8}, {"opacity": 1, "scale": 1, "rotation": 0}, T["spray"], .3, "back.out(2.6)")
fromTo("#b1", {"rotation": 0, "y": 0}, {"rotation": -22, "y": -40}, T["spray"] - .1, .22, "power2.out")
puff("m1", T["spray"] + .06, .55, -.85, 330, big=1.3)
flash(T["spray"] + .04, .4, .28)
fromTo("#b1", {"rotation": -22, "y": -40}, {"rotation": 0, "y": 0}, T["not"] - .05, .32, "power2.inOut")
pop("#sp2", T["not"], .22)
fromTo("#sp3", {"opacity": 0, "scale": 1.6}, {"opacity": 1, "scale": 1}, T["swallow"], .24, "expo.out")
fromTo("#sp3 i", {"scaleX": 0}, {"scaleX": 1}, T["swallow"] + .18, .18, "power3.out")
# "Two quick sprays... done."
to("#herospray", {"opacity": 0, "y": -40}, L[3] - .02, .16)
pop("#tw0", T["two"], .22)
fromTo("#b1", {"rotation": 0, "y": 0}, {"rotation": -26, "y": -30}, T["two"] - .05, .22, "power2.out")
fromTo("#n1", {"opacity": 0, "scale": .3}, {"opacity": 1, "scale": 1}, T["two"] + .02, .26, "back.out(3)")
puff("m1", T["two"] + .04, .6, -.8, 300, dur=.4, big=1.2)
fromTo("#n2", {"opacity": 0, "scale": .3}, {"opacity": 1, "scale": 1}, T["sprays"] + .02, .26, "back.out(3)")
puff("m1", T["sprays"] + .06, .6, -.8, 300, dur=.4, big=1.2)
to("#n1", {"opacity": 0, "y": -30}, T["tongue"] + .1, .18); to("#n2", {"opacity": 0, "y": -30}, T["tongue"] + .1, .18)
fromTo("#b1", {"rotation": -26, "y": -30}, {"rotation": 0, "y": 0}, T["tongue"] - .02, .34, "power2.inOut")
pop("#tw1", T["tongue"], .22)
fromTo("#done", {"opacity": 0, "scale": 2.2, "rotation": -12}, {"opacity": 1, "scale": 1, "rotation": -6}, T["done"], .26, "expo.out")
flash(T["done"] + .02, .5, .3)
fromTo("#b1", {"scale": 1}, {"scale": 1.04}, T["done"], .12, "power2.out")
fromTo("#b1", {"scale": 1.04}, {"scale": 1}, T["done"] + .12, .2, "power2.inOut")

# NO scene (dark)
set_("#dark", {"opacity": 1}, L[4] - .04)
to("#dark", {"opacity": 0}, L[5] - .06, .18, "power2.out")
flash(L[4] - .02, .9, .3)
for i, key in enumerate(("pills", "water", "chalky")):
    fromTo(f"#no{i}", {"opacity": 0, "x": -140, "scale": .9}, {"opacity": 1, "x": 0, "scale": 1}, T[key] - .04, .26, "back.out(2)")
    tt = T["aftertaste"] + .12 if key == "chalky" else T[key] + .22
    fromTo(f"#no{i} .strike", {"scaleX": 0}, {"scaleX": 1}, tt, .18, "power3.out")
    fromTo(f"#no{i} .nos", {"opacity": 0, "scale": 1.8, "rotation": -14}, {"opacity": 1, "scale": 1, "rotation": -8}, tt + .04, .22, "expo.out")
pop("#nohead", T["pills"] - .1, .22)

# TRIO
flash(L[5] - .02, 1.0, .34)
pop("#trhead", T["vitd"], .24)
for i, key in enumerate(("d", "b12", "biotin")):
    fromTo(f"#tb{i}", {"opacity": 0, "y": 420, "rotation": -10 + 10 * i}, {"opacity": 1, "y": 0, "rotation": 0}, T[key] - .04, .42, "back.out(1.6)")
    fromTo(f"#tt{i}", {"opacity": 0, "y": 30, "scale": .8}, {"opacity": 1, "y": 0, "scale": 1}, T[key] + .18, .24, "back.out(2.2)")
    flash(T[key] + .02, .25, .22)
# "wherever your day takes you": bottles shrink to a row, chips rise
to("#trhead", {"opacity": 0, "y": -40}, L[6] - .02, .16)
pop("#whhead", T["one"], .24)
fromTo("#trio", {"scale": 1, "y": 0}, {"scale": .72, "y": -150}, T["bottle"], .5, "power3.inOut")
for i, key in enumerate(("wherever", "day", "takes")):
    fromTo(f"#ch{i}", {"opacity": 0, "y": 120, "scale": .7, "rotation": -8 + 8 * i}, {"opacity": 1, "y": 0, "scale": 1, "rotation": -3 + 3 * i}, T[key], .34, "back.out(2.2)")

# TRUST
flash(L[7] - .02, 1.0, .34)
fromTo("#bd0", {"opacity": 0, "x": -200, "rotation": -4}, {"opacity": 1, "x": 0, "rotation": -2}, T["created"], .36, "back.out(1.8)")
for i in range(3):
    fromTo(f"#dr{i}", {"opacity": 0, "y": 60, "scale": .5}, {"opacity": 1, "y": 0, "scale": 1}, T["three"] + .09 * i, .28, "back.out(2.6)")
fromTo("#bd1", {"opacity": 0, "x": 200, "rotation": 4}, {"opacity": 1, "x": 0, "rotation": 2}, T["developed"], .36, "back.out(1.8)")
fromTo("#ukpin", {"opacity": 0, "y": -80, "scale": .5}, {"opacity": 1, "y": 0, "scale": 1}, T["uk"], .3, "bounce.out")
fromTo("#b2", {"opacity": 0, "y": 500, "rotation": 8}, {"opacity": 1, "y": 0, "rotation": 0}, L[7] + .1, .55, "back.out(1.4)")

# SHOP
flash(L[8] - .02, .8, .3)
fromTo("#b3", {"opacity": 0, "y": 700, "rotation": -10}, {"opacity": 1, "y": 0, "rotation": 0}, L[8] - .02, .55, "back.out(1.4)")
pop("#avhead", T["available"], .24)
fromTo("#tag", {"opacity": 0, "scale": .3, "rotation": 14}, {"opacity": 1, "scale": 1, "rotation": -4}, T["tata"], .34, "back.out(2.4)")
fromTo("#tag", {"rotation": -4}, {"rotation": 3}, T["g"], .3, "power1.inOut")
puff("m3", T["available"] + .1, 0, -1, 220, big=.9)

# END CARD
flash(L[9] - .02, 1.0, .34)
fromTo("#ec0", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, T["comment"], .22, "back.out(2.2)")
fromTo("#eckw", {"opacity": 0, "scale": .6}, {"opacity": 1, "scale": 1}, T["spraykw"] - .02, .28, "back.out(2.2)")
for i in range(5):
    fromTo(f".ty{i}", {"opacity": 0, "y": -30, "scale": 1.4}, {"opacity": 1, "y": 0, "scale": 1}, T["spraykw"] + .06 + .07 * i, .14, "back.out(3)")
fromTo(".cur", {"opacity": 1}, {"opacity": 0, "duration": .22, "yoyo": True, "repeat": 9, "ease": "steps(1)"}, T["spraykw"], .22, "steps(1)")
fromTo("#ec1", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, T["dm"] - .1, .28, "back.out(2.2)")
fromTo("#ecwm", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, T["dm"], .3, "back.out(2)")
fromTo("#b4", {"opacity": 0, "y": 500, "rotation": -8}, {"opacity": 1, "y": 0, "rotation": 0}, L[9] + .05, .55, "back.out(1.4)")
puff("m4", T["spraykw"] + .1, 0, -1, 240, big=1.0)
to("#eckw", {"scale": .94, "duration": .09, "yoyo": True, "repeat": 1, "ease": "power2.out"}, T["link"] + .4, .09, "power2.out")
fromTo(".prog i", {"scaleX": 0}, {"scaleX": 1}, 0, DUR, "none")
tw.append(f"tl.set({{}}, {{}}, {DUR});")


def clip(id_, win, track, inner, extra=""):
    s, e = win
    return f'<div id="{id_}" class="clip" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="{track}" data-layout-allow-overflow {extra}>{inner}</div>'


hook_inner = f'''<div id="hookwrap">
<div class="hl"><span class="hw" id="hk0">Still</span> <span class="hw" id="hk1">swallowing</span></div>
<div class="hl"><span class="hw" id="hk2">your</span> <span class="hw pill" id="hk3">vitamins?</span></div>
<div id="cap"><i class="c1"></i><i class="c2"></i><b></b></div>
<div id="qm">?</div>
</div>'''

hero_inner = f'''<div id="heromeet" class="head">
<div class="eyebrow" id="meet">MEET</div>
<div class="wm" id="wm">VITONNIX</div>
<div class="wm2" id="wm2">SubliSpray<sup>®</sup></div>
</div>
<div id="herospray" class="head">
<div class="eyebrow" id="sp0">VITAMINS YOU</div>
<div class="big teal" id="sp1">SPRAY.</div>
<div class="row"><span class="eyebrow" id="sp2">NOT</span> <span class="strikeword" id="sp3">swallow<i></i></span></div>
</div>
<div id="herotwo" class="head">
<div class="big" id="tw0" style="font-size:96px">Two quick sprays</div>
<div class="eyebrow" id="tw1">UNDER YOUR TONGUE</div>
</div>
<div id="done">DONE.</div>
<div class="num" id="n1" style="left:600px;top:560px">1</div>
<div class="num" id="n2" style="left:720px;top:470px">2</div>
{bottle("b1", TEAL, "Vitamin D", "sunshine support", 390, 560, 1.04)}
{mist("m1", 552, 575)}'''


def noitem(i, label, icon):
    return f'<div class="noitem" id="no{i}"><span class="ico {icon}"></span><span class="lbl">{label}</span><i class="strike"></i><b class="nos">NO</b></div>'


no_inner = f'''<div class="head dark"><div class="big light" id="nohead">Say no to</div></div>
<div id="nolist">{noitem(0, "Pills", "i-pill")}{noitem(1, "Water", "i-glass")}{noitem(2, "Chalky aftertaste", "i-tongue")}</div>'''

trio_inner = f'''<div class="head"><div class="big" id="trhead">Pick yours</div></div>
<div class="head"><div class="big" id="whhead">Fits your pocket</div></div>
<div id="trio">
{bottle("tb0", SUN, "Vitamin D", "sunshine support", 60, 620, .78, text="#a8720f")}
{bottle("tb1", CORAL, "Vitamin B12", "everyday essential", 423, 560, .78)}
{bottle("tb2", VIOLET, "Biotin", "hair, skin and nails", 786, 620, .78)}
<div class="tt" id="tt0" style="left:60px;top:1210px;color:#a8720f">Vitamin D</div>
<div class="tt" id="tt1" style="left:423px;top:1150px;color:{CORAL}">B12</div>
<div class="tt" id="tt2" style="left:786px;top:1210px;color:{VIOLET}">Biotin</div>
</div>
<div id="chips"><span class="chip" id="ch0">Desk</span><span class="chip" id="ch1">Gym bag</span><span class="chip" id="ch2">Travel</span></div>'''

trust_inner = f'''<div class="badge" id="bd0"><span class="bk">CREATED BY</span><span class="bv">3 doctors</span><span class="drs"><i id="dr0"></i><i id="dr1"></i><i id="dr2"></i></span></div>
<div class="badge r" id="bd1"><span class="bk">DEVELOPED IN</span><span class="bv">the UK</span><span id="ukpin" class="pin"></span></div>
{bottle("b2", TEAL, "Vitamin D", "sunshine support", 290, 700, .92)}'''

shop_inner = f'''<div class="head"><div class="big" id="avhead">Available now</div></div>
{bottle("b3", TEAL, "Vitamin D", "sunshine support", 250, 560, 1.04)}
{mist("m3", 412, 575)}
<div id="tag"><span class="tk">AVAILABLE ON</span><span class="tv">Tata 1mg</span></div>'''

end_inner = f'''<div id="endc">
<div class="ec0" id="ec0">Comment</div>
<div class="eckw" id="eckw"><span class="ty ty0">S</span><span class="ty ty1">P</span><span class="ty ty2">R</span><span class="ty ty3">A</span><span class="ty ty4">Y</span><i class="cur"></i></div>
<div class="ec1" id="ec1">and we'll DM you the link</div>
</div>
{bottle("b4", TEAL, "Vitamin D", "sunshine support", 435, 830, .7)}
{mist("m4", 540, 842)}
<div id="ecwm">VITONNIX <span>SubliSpray<sup>®</sup></span></div>'''

css = f"""
@font-face {{ font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {MIST}; }}
body {{ font-family: "Montserrat", sans-serif; color: {INK}; }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {MIST}; }}
.clip {{ position: absolute; inset: 0; }}
#bg {{ background: radial-gradient(900px 700px at 50% 38%, #ffffff 0%, {MIST} 60%, #d8ecef 100%); }}
#bg .blob {{ position: absolute; border-radius: 50%; filter: blur(60px); opacity: .55; }}
#bg .bl1 {{ left: -200px; top: 200px; width: 700px; height: 700px; background: #bfe6ea; }}
#bg .bl2 {{ right: -260px; top: 900px; width: 760px; height: 760px; background: #d6f0f2; }}
#dark {{ position: absolute; inset: 0; background: radial-gradient(900px 800px at 50% 40%, #11515f 0%, {INK} 70%); opacity: 0; }}
.top {{ position: absolute; left: 60px; right: 60px; top: 262px; display: flex; align-items: center; gap: 24px; z-index: 9; }}
.brand {{ font-size: 28px; font-weight: 800; letter-spacing: 5px; color: {INK}; padding: 8px 20px; border-radius: 24px; background: rgba(255,255,255,.9); box-shadow: 0 8px 24px rgba(11,60,73,.10); }}
.brand b {{ color: {TEAL}; }}
.prog {{ flex: 1; height: 6px; border-radius: 3px; background: rgba(11,60,73,.12); overflow: hidden; }}
.prog i {{ display: block; height: 100%; background: {TEAL}; transform-origin: 0 50%; }}
/* everything that pops in later starts hidden here */
.hw, #cap, #qm, #meet, #wm, #wm2, #sp0, #sp1, #sp2, #sp3, #tw0, #tw1, #done, .num, .noitem, .nos, #nohead, #trhead, #whhead,
.bottle, .tt, .chip, .badge, .drs i, .pin, #avhead, #tag, #ec0, #eckw, .ty, #ec1, #ecwm, .cap {{ opacity: 0; }}
#b1 {{ opacity: 1; }}
#hookwrap {{ position: absolute; inset: 0; }}
.hl {{ display: block; text-align: center; font-weight: 800; font-size: 104px; line-height: 1.04; letter-spacing: -3px; }}
.hl:first-child {{ position: absolute; left: 40px; right: 40px; top: 330px; }}
.hl:nth-child(2) {{ position: absolute; left: 40px; right: 40px; top: 446px; }}
.hw {{ display: inline-block; }}
.pill {{ padding: 2px 34px 12px; border-radius: 40px; background: {TEAL}; color: #fff; box-shadow: 0 18px 50px rgba(14,124,134,.35); }}
#cap {{ position: absolute; left: 340px; top: 760px; width: 400px; height: 160px; }}
#cap i {{ position: absolute; top: 0; width: 200px; height: 160px; }}
#cap .c1 {{ left: 0; border-radius: 80px 0 0 80px; background: linear-gradient(180deg, #ff8a6b, {CORAL}); }}
#cap .c2 {{ left: 200px; border-radius: 0 80px 80px 0; background: linear-gradient(180deg, #ffffff, #dfe9eb); }}
#cap b {{ position: absolute; left: 40px; top: 24px; width: 120px; height: 22px; border-radius: 11px; background: rgba(255,255,255,.55); }}
#qm {{ position: absolute; left: 700px; top: 620px; font-size: 300px; font-weight: 900; color: {TEAL}; line-height: 1; }}
.head {{ position: absolute; left: 60px; right: 60px; top: 300px; text-align: center; }}
.eyebrow {{ display: inline-block; font-weight: 800; font-size: 34px; letter-spacing: 6px; padding: 8px 26px; border-radius: 30px; background: {INK}; color: {MIST}; }}
.head.dark .eyebrow {{ background: {MIST}; color: {INK}; }}
.wm {{ margin-top: 16px; font-weight: 900; font-size: 128px; letter-spacing: 4px; line-height: 1; color: {INK}; }}
.wm2 {{ margin-top: 4px; font-weight: 700; font-size: 68px; letter-spacing: -1px; color: {TEAL}; }}
sup {{ font-size: .4em; vertical-align: top; }}
.big {{ margin-top: 12px; font-weight: 900; font-size: 112px; letter-spacing: -4px; line-height: 1; color: {INK}; }}
.big.teal {{ color: {TEAL}; }}
.big.light {{ color: {MIST}; }}
.row {{ margin-top: 18px; display: flex; justify-content: center; align-items: center; gap: 20px; }}
.strikeword {{ position: relative; display: inline-block; font-weight: 800; font-size: 72px; letter-spacing: -2px; color: rgba(11,60,73,.55); }}
.strikeword i {{ position: absolute; left: -6px; right: -6px; top: 50%; height: 10px; margin-top: -5px; border-radius: 5px; background: {CORAL}; transform-origin: 0 50%; }}
.num {{ position: absolute; width: 150px; height: 150px; border-radius: 50%; background: {TEAL}; color: #fff; font-weight: 900; font-size: 96px; line-height: 150px; text-align: center; box-shadow: 0 18px 50px rgba(14,124,134,.4); }}
#done {{ position: absolute; left: 150px; right: 150px; top: 1080px; text-align: center; font-weight: 900; font-size: 150px; letter-spacing: -4px; color: #fff; background: {TEAL}; border-radius: 40px; padding: 10px 0 24px; box-shadow: 0 30px 80px rgba(14,124,134,.45); }}
.bottle {{ position: absolute; filter: drop-shadow(0 30px 40px rgba(11,60,73,.22)); transform-origin: 50% 85%; }}
.mist {{ position: absolute; width: 0; height: 0; pointer-events: none; }}
.mist .md {{ position: absolute; left: -70px; top: -70px; width: 140px; height: 140px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.95) 0%, rgba(214,240,243,.7) 40%, rgba(214,240,243,0) 70%); opacity: 0; }}
#nolist {{ position: absolute; left: 90px; right: 90px; top: 560px; display: flex; flex-direction: column; gap: 44px; }}
.noitem {{ position: relative; display: flex; align-items: center; gap: 34px; height: 190px; padding: 0 44px; border-radius: 44px; background: rgba(255,255,255,.08); border: 2px solid rgba(255,255,255,.14); }}
.noitem .lbl {{ font-weight: 800; font-size: 74px; letter-spacing: -2px; color: {MIST}; }}
.noitem .strike {{ position: absolute; left: 30px; right: 30px; top: 50%; height: 14px; margin-top: -7px; border-radius: 7px; background: {CORAL}; transform-origin: 0 50%; }}
.noitem .nos {{ position: absolute; right: 36px; top: -34px; padding: 6px 26px 10px; border-radius: 22px; background: {CORAL}; color: #fff; font-weight: 900; font-size: 56px; letter-spacing: 2px; box-shadow: 0 16px 40px rgba(228,87,46,.45); }}
.ico {{ position: relative; display: block; width: 130px; height: 130px; flex: none; }}
.i-pill::before {{ content: ""; position: absolute; left: 10px; top: 45px; width: 110px; height: 44px; border-radius: 22px; background: linear-gradient(90deg, {CORAL} 50%, #fff 50%); transform: rotate(-28deg); }}
.i-glass::before {{ content: ""; position: absolute; left: 30px; top: 14px; width: 70px; height: 104px; border-radius: 6px 6px 22px 22px; background: linear-gradient(180deg, rgba(255,255,255,.25) 0 40%, #7fd3dc 40%); border: 4px solid rgba(255,255,255,.7); }}
.i-tongue::before {{ content: ""; position: absolute; left: 20px; top: 30px; width: 90px; height: 76px; border-radius: 45px 45px 50px 50px; background: #f08a9b; }}
.i-tongue::after {{ content: ""; position: absolute; left: 60px; top: 46px; width: 10px; height: 50px; border-radius: 5px; background: rgba(255,255,255,.5); }}
#trio {{ position: absolute; inset: 0; transform-origin: 50% 900px; }}
.tt {{ position: absolute; width: 234px; text-align: center; font-weight: 900; font-size: 44px; letter-spacing: -1px; }}
#chips {{ position: absolute; left: 60px; right: 60px; top: 1180px; display: flex; justify-content: center; gap: 22px; }}
.chip {{ display: inline-block; padding: 14px 40px 20px; border-radius: 40px; background: #fff; color: {INK}; font-weight: 800; font-size: 50px; letter-spacing: -1px; box-shadow: 0 16px 40px rgba(11,60,73,.14); border: 3px solid {TEAL}; }}
.badge {{ position: absolute; left: 70px; top: 380px; padding: 26px 40px 30px; border-radius: 36px; background: #fff; box-shadow: 0 24px 60px rgba(11,60,73,.16); border-left: 14px solid {TEAL}; }}
.badge.r {{ left: auto; right: 70px; top: 600px; border-left: 0; border-right: 14px solid {CORAL}; text-align: right; }}
.badge .bk {{ display: block; font-weight: 800; font-size: 28px; letter-spacing: 5px; color: {TEAL}; }}
.badge.r .bk {{ color: {CORAL}; }}
.badge .bv {{ display: block; font-weight: 900; font-size: 92px; letter-spacing: -3px; line-height: 1.05; color: {INK}; }}
.drs {{ display: flex; gap: 14px; margin-top: 16px; }}
.drs i {{ display: block; width: 74px; height: 74px; border-radius: 50%; background: {TEAL}; position: relative; }}
.drs i::before, .drs i::after {{ content: ""; position: absolute; left: 50%; top: 50%; background: #fff; border-radius: 4px; transform: translate(-50%,-50%); }}
.drs i::before {{ width: 36px; height: 10px; }} .drs i::after {{ width: 10px; height: 36px; }}
.pin {{ position: absolute; left: -56px; top: -40px; width: 90px; height: 90px; border-radius: 50% 50% 50% 0; background: {CORAL}; transform: rotate(-45deg); box-shadow: 0 16px 40px rgba(228,87,46,.4); }}
.pin::after {{ content: ""; position: absolute; left: 27px; top: 27px; width: 36px; height: 36px; border-radius: 50%; background: #fff; }}
#tag {{ position: absolute; left: 590px; top: 1120px; padding: 20px 36px 26px; border-radius: 30px; background: #fff; border: 4px solid {INK}; box-shadow: 0 24px 60px rgba(11,60,73,.2); transform-origin: 20% 0; }}
#tag .tk {{ display: block; font-weight: 800; font-size: 24px; letter-spacing: 5px; color: {TEAL}; }}
#tag .tv {{ display: block; font-weight: 900; font-size: 72px; letter-spacing: -2px; color: {INK}; line-height: 1.05; }}
#endc {{ position: absolute; left: 60px; right: 60px; top: 300px; text-align: center; }}
.ec0 {{ display: inline-block; padding: 10px 34px; border-radius: 24px; background: {INK}; color: {MIST}; font-weight: 800; font-size: 60px; letter-spacing: 2px; }}
.eckw {{ display: block; width: max-content; margin: 16px auto 14px; padding: 4px 54px 14px; border-radius: 34px; background: {TEAL}; font-weight: 900; font-size: 170px; letter-spacing: 8px; color: #fff; box-shadow: 0 20px 60px rgba(14,124,134,.5); line-height: 1.05; }}
.ty {{ display: inline-block; }}
.cur {{ display: inline-block; width: 12px; height: 130px; margin-left: 8px; vertical-align: -14px; border-radius: 6px; background: #fff; }}
.ec1 {{ display: inline-block; padding: 8px 26px 12px; border-radius: 22px; background: rgba(255,255,255,.92); font-weight: 700; font-size: 46px; color: {INK}; box-shadow: 0 10px 30px rgba(11,60,73,.12); }}
#ecwm {{ position: absolute; left: 0; right: 0; top: 1466px; text-align: center; font-weight: 900; font-size: 44px; letter-spacing: 6px; color: {INK}; }}
#ecwm span {{ color: {TEAL}; letter-spacing: 0; font-weight: 700; }}
#caps {{ z-index: 6; }}
.cap {{ position: absolute; left: 50px; right: 50px; top: 1330px; text-align: center; }}
.cap .box {{ display: inline-block; max-width: 980px; padding: 12px 20px 14px; border-radius: 26px; background: rgba(255,255,255,.94); box-shadow: 0 14px 40px rgba(11,60,73,.16); font-weight: 800; font-size: 62px; line-height: 1.15; letter-spacing: -1px; color: {INK}; }}
.cap .w {{ display: inline-block; padding: 2px 12px 5px; border-radius: 16px; }}
.cap.dark .box {{ background: rgba(6,32,40,.88); color: {MIST}; box-shadow: 0 14px 40px rgba(0,0,0,.5); }}
.cap.slam .box {{ font-size: 86px; letter-spacing: -2px; }}
#fx {{ z-index: 7; }}
#flash {{ position: absolute; inset: 0; background: #ffffff; opacity: 0; }}
"""

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Vitonnix SubliSpray 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" data-layout-ignore><div class="blob bl1"></div><div class="blob bl2"></div><div id="dark"></div></div>
      <div id="ui" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-allow-overflow><div class="top"><span class="brand"><b>+</b> VITONNIX</span><span class="prog"><i></i></span></div></div>
      {clip("s-hook", S_HOOK, 2, hook_inner)}
      {clip("s-hero", S_HERO, 2, hero_inner)}
      {clip("s-no", S_NO, 2, no_inner)}
      {clip("s-trio", S_TRIO, 2, trio_inner)}
      {clip("s-trust", S_TRUST, 2, trust_inner)}
      {clip("s-shop", S_SHOP, 2, shop_inner)}
      {clip("s-end", S_END, 2, end_inner)}
      <div id="caps" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3">{"".join(caps_html)}</div>
      <div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-layout-ignore><div id="flash"></div></div>
      <audio id="mix" src="{AUDIO}" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in tw)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(html)
print(f"index.html written: {DUR}s, {len(tw)} tweens, audio {AUDIO}")
