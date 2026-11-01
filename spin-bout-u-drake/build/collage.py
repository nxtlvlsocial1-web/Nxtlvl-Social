"""Spin Bout U (Drake & 21 Savage) lyric edit, 1:1, 60 s from the 2:13 bass drop, v9: writes index.html.

python3 build/collage.py      (from the project root; after build/assets.py, anime.py, clips90.py, collage_tex.py and
node build/render3d.cjs for the 3D elements)

The owner asked for the Ashke edit's structure (../ashke-lyric-9x16, square cut in ../ashke-lyric-1x1) in this edit's
colours. So this is the Ashke engine, ported: one big crumpled paper sheet that a virtual camera travels over (here
maroon, under soft blind shadows and faint grid lines); each lyric line is built up on it with one of the nine scene
recipes (torn paper scraps, a cut-out sticker with a paper border, photo prints with a border, labels that type on
letter by letter behind a cursor block or slam in big, stamped words, 3D words, a keyword filled with a picture that
the camera zooms into, marker circles, stars, a doodle sticker for the line); the camera never stops, glides through
each scene's labels on a time-aware spline, whips into the next scene at peak speed with directional motion blur and
punches in on every beat, stepped at 15 fps; three single-frame stills before most cuts; one-step invert, white and
split flashes. Colours: black, maroon, magenta, off-white; type Anton. Pictures: the owner's photos in the opening,
the anime art (stills and the owner's animated clips), the 3D elements. Captions are the owner's lyrics on their sung
words; every cuss word shows only as a blurred ****.
"""
import json
import math
import os
import random
import re
import sys

from PIL import Image, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doodles import ICON, WORD, svg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR, FPS = 60.0, 30
STEP = 1 / 15
FW = FH = 1080
CY, ZOOM, VTRACK = 540, .64, .55          # the board is 1080x1920 (the Ashke layouts); the square camera pulls back
L = json.load(open(os.path.join(ROOT, "plan", "lines.json")))
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats.json")))
PERIOD = 60 / BEATS["bpm"]
G3T = {e["kind"]: e["t0"] for e in json.load(open(os.path.join(ROOT, "plan", "g3d.json")))}   # the 3D clips' start times
INK, MAR, MAG, WHT = "#151314", "#5f1b30", "#b0194f", "#f2f1ec"
ANTON = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Anton.ttf"), 100)
CURSE = {"ass", "hoes", "nigga", "niggas", "shitll", "shit"}
KEY = {0: {"jealous"}, 1: {"vogue"}, 2: {"90s"}, 3: {"vogue"}, 4: {"runway"}, 5: {"row"}, 6: {"home"}, 7: {"toes"}, 8: {"go"},
       9: {"globe"}, 10: {"road"}, 11: {"feel"}, 12: {"dropped"}, 13: {"smoke"}, 14: {"block"}, 15: {"feel"}, 16: {"body"},
       17: {"snotty"}, 18: {"body"}}
PHRASES = {("for", "you"), ("baby", "girl"), ("front", "row"), ("sent", "home"), ("ten", "toes"), ("these", "days"), ("the", "way"),
           ("make", "me")}
RECIPE = {-1: "R1", 0: "R2", 1: "R3", 2: "R5", 3: "R4", 4: "R6", 5: "R8", 6: "R2", 7: "R1", 8: "R7", 9: "R3", 10: "R9", 11: "R2",
          12: "R5", 13: "R6", 14: "R4", 15: "R8", 16: "R3", 17: "R1", 18: "R9"}
CUTOUT = {1: "cat_black_collar", 3: "hand_phone_sticker", 5: "drake_chanel_night", 6: "cat_white_dumb",
          17: "snotty"}
AF, PR, AV = "assets/img/anime/full/", "assets/img/print/", "assets/video/anime/"
CL = "assets/video/clips/"                                # the owner's Drake clips, cut by build/clips_drake.py
CARD1 = {0: AV + "jealous.mp4", 2: PR + "envogue_funky_divas.jpg", 4: CL + "b_phone1.mp4",
         11: AV + "her_blush.mp4"}
CARD2 = {1: PR + "vogue_cat_cover.jpg", 3: "assets/img/collage/call_vogue.jpg", 9: AF + "jet.jpg", 10: AV + "road.mp4",
         16: CL + "a_close.mp4"}
CUTPRINT = {14: None, 9: None, 16: None, 7: CL + "b_phone2.mp4", 5: CL + "b_seated.mp4", 15: CL + "a_walk2.mp4"}     # recipes with a cut-out slot that use a picture instead
FILL = {6: PR + "cat_white_dumb.jpg", 11: AF + "her_blush.jpg"}
G3D_AT = {9: ("globe", 120, 620, 860), 15: ("heart", 140, 470, 800),
          16: ("body", 0, 700, 1080), 17: ("tissue", 0, 1200, 360)}
STILLS = [AF + n + ".jpg" for n in ("her_blush", "jet", "road", "finale", "snotty")] + [PR + "vogue_cat_cover.jpg", PR + "rolex_cat_ad.jpg", PR + "envogue_funky_divas.jpg"]
A, HIDE, PAN, SCREEN = [], [], [], []
CAMKEYS, FLASH = {}, []
LOCKS, CAMSTATE = [], {}
CUES = []           # (t, kind, len) moments for the sound design, written to plan/sfx_events.json     # screen-pinned layers inside the board; the camera per 15 fps frame (fx, fy, scale, rot)
NID, VTR = [0], [1]
R = random.Random(23)


_STEPS = re.compile(r'ease: "steps\(\d+\)"')


def js(s):
    """Timeline line. v12: every stepped ease becomes a smooth one (expo out for short entrances, power2 out for long
    moves), the premium After Effects feel the owner asked for instead of the 15 fps steps."""
    if 'ease: "steps(' in s:
        m = re.search(r'duration: ([\d.]+)', s)
        d = float(m.group(1)) if m else .3
        s = _STEPS.sub('ease: "expo.out"' if d <= .5 else 'ease: "power2.out"', s)
    if "ease: \"" in s and "duration:" in s:             # v16: the curve is kept, time steps on twos (15 fps)
        m = re.search(r'duration: ([\d.]+)', s)
        d = float(m.group(1)) if m else .3
        s = re.sub(r'ease: "([^"]+)"', lambda mm: f'ease: SE("{mm.group(1)}", {max(2, round(d * 15))})', s)
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def lt(li):
    return L[li]["start"]


def scenes():
    out = [(0.0, lt(0) - .06, -1)]
    for li in range(len(L)):
        a = lt(li) - .06
        b = (lt(li + 1) - .06) if li + 1 < len(L) else DUR
        out.append((a, b, li))
    return out


def groups_of(li):
    """Labels of one or two words (keywords on their own, cuss words as ****); one- and two-letter words ride along."""
    ws = []
    for w, s, e in L[li]["words"]:
        core = re.sub(r"[^a-z0-9]", "", w.lower())
        txt = "****" if core in CURSE else w.rstrip(",.")
        ws.append((txt.upper(), core in KEY.get(li, ()), s))
    j = 0                                   # natural phrases stay together on one label
    while j < len(ws) - 1:
        pair = (ws[j][0].lower().strip("'"), ws[j + 1][0].lower().strip("'"))
        if pair in PHRASES:
            ws[j:j + 2] = [(ws[j][0] + " " + ws[j + 1][0], ws[j][1] or ws[j + 1][1], ws[j][2])]
        j += 1
    groups, cur = [], []
    for w in ws:
        if w[1]:
            if cur:
                groups.append(cur)
                cur = []
            groups.append([w])
        else:
            cur.append(w)
            if len(cur) == 2 or sum(len(x[0]) for x in cur) > 10 or " " in w[0]:
                groups.append(cur)
                cur = []
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        txt = " ".join(x[0] for x in g)
        if out and len(txt) <= 2 and not g[0][1]:
            out[-1] = (out[-1][0] + " " + txt, out[-1][1], out[-1][2])
            continue
        out.append((txt, g[0][1], g[0][2]))
    return out


SERIF_F = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "PlayfairDisplay-BoldItalic.woff2"), 100)
SERIF = {"FOR YOU", "BABY GIRL", "THE WAY", "THESE DAYS", "FOR REAL", "YEAH", "EVEN IF", "BUT JUST", "AND I", "DOWN TO"}


def tw(text, size):
    if text and text == text.lower() and text.upper() in SERIF:
        return SERIF_F.getlength(text) * size / 100
    return ANTON.getlength(text) * size / 100


def fit(text, maxw, size):
    return min(size, maxw / (tw(text, 100) / 100 + .56))


def star_path(n=7, r1=48, r2=22, seed=0):
    g = random.Random(seed)
    pts = []
    for k in range(n * 2):
        r = r1 * g.uniform(.9, 1) if k % 2 == 0 else r2
        a = k / (n * 2) * math.pi * 2 - math.pi / 2
        pts.append(f"{math.cos(a) * r:.1f} {math.sin(a) * r:.1f}")
    return "M" + " L".join(pts) + " Z"


CIRC = ('<svg class="circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path pathLength="400" '
        'd="M50 7 C93 3 106 88 50 94 S-8 14 62 8"/></svg>')


# ------------------------------------------------------------------------------------------------ elements
def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {t0:.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')


def scrap(kind, k, x, y, w, rot, t0, t1, z=1):
    kind = {"red": "mag", "grey": "maroon"}.get(kind, kind)
    i = nid("sc")
    PAN.append(f'<img class="el" id="{i}" src="assets/img/collage/scrap/{kind}-{k}.png" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;'
               f'transform:rotate({rot:.1f}deg);z-index:{z}" alt="">')
    show(f"#{i}", t0, t1)
    return i


def printel(src, x, y, w, h, rot, t0, t1, red=False, z=2):
    """A photo print with an off-white border; a video when src is an animated clip (it plays from t0)."""
    if not src or t1 - t0 < .15:
        return
    i = nid("pr")
    if src.endswith(".mp4"):
        n = float(os.popen(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{os.path.join(ROOT, src)}"').read() or 0)
        VTR[0] += 1
        media = (f'<video id="v{i}" class="clip" src="{src}" data-start="{t0:.3f}" data-duration="{min(n, t1 - t0):.3f}" '
                 f'data-track-index="{VTR[0]}" muted playsinline></video>')
    else:
        media = f'<img src="{src}" alt="">'
    live = "/clips/" in src
    vf = ('<div class="vf"><b class="c1"></b><b class="c2"></b><b class="c3"></b><b class="c4"></b>'
          '<span class="rec"><i></i>REC</span><span class="tc">00:00:00:00</span><em class="pf"></em><em class="pf"></em></div>') if live else ""
    PAN.append(f'<div class="print el" id="{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;'
               f'transform:rotate({rot:.1f}deg);z-index:{z}">{media}<i style="opacity:{.85 if red else 0}"></i>{vf}</div>')
    show(f"#{i}", t0, t1)
    if live:
        clip_fx(i, w, h, t0, t1)
    return i
    js(f'tl.fromTo("#{i}", {{x: {R.choice([-120, 120])}}}, {{x: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')


def clip_fx(i, w, h, t0, t1):
    """Camcorder look on the owner's Drake clips: the REC dot blinks, the timecode runs, and paparazzi flashes pop
    on the beats at random spots."""
    k, t = 0, t0
    while t < t1:
        js(f'tl.set("#{i} .rec i", {{opacity: {k % 2}}}, {t:.3f});')
        t, k = t + .5, k + 1
    for f in range(int((t1 - t0) * 15) + 1):
        tt = t0 + f / 15
        s_ = f / 15
        js(f'tl.set("#{i} .tc", {{textContent: "00:00:{int(s_):02d}:{int(s_ * 30) % 30:02d}"}}, {tt:.3f});')
    g = random.Random(int(t0 * 100))
    for n_, bt in enumerate([b for b in BEATS["beats"] if t0 + .1 < b < t1 - .1][:6]):
        sel = f"#{i} .pf:nth-of-type({n_ % 2 + 1})"
        js(f'tl.set("{sel}", {{left: "{g.uniform(10, 75):.0f}%", top: "{g.uniform(8, 60):.0f}%", opacity: 1, scale: 1}}, {bt:.3f});')
        js(f'tl.to("{sel}", {{opacity: 0, scale: 1.6, duration: .2, ease: "power2.out"}}, {bt + 1 / 30:.3f});')
        CUES.append((bt, "camera", 0))


def phone_screen(t0, t1):
    """The dialing screen inside the blank phone sticker: Vogue, calling..., pulsing rings round the avatar, a
    running timer once it connects on VOGUE. Coordinates are the sticker's own pixels (screen 250 x 548, tilted 9 deg)."""
    i = nid("ps")
    html = (f'<div class="pscreen" id="{i}"><div class="ps-glow"></div><span class="ps-top">calling</span>'
            f'<div class="ps-av"><b class="ring"></b><b class="ring"></b><span>V</span></div>'
            f'<span class="ps-name">Vogue</span><span class="ps-sub">mobile</span>'
            f'<div class="ps-btns"><i></i><i></i><i class="end"></i></div></div>')
    kw = next((s_ for w_, s_ in words_of(3) if w_ == "vogue"), t1 - .4)
    k, t = 0, t0
    while t < kw:
        js(f'tl.set("#{i} .ps-top", {{textContent: "calling{"." * (k % 4)}"}}, {t:.3f});')
        js(f'tl.fromTo("#{i} .ring", {{scale: 1, opacity: .9}}, {{scale: 1.9, opacity: 0, duration: .55, ease: "power2.out", stagger: .18, immediateRender: false}}, {t:.3f});')
        t, k = t + PERIOD / 2, k + 1
    for f in range(int((t1 - kw) * 15) + 1):
        js(f'tl.set("#{i} .ps-top", {{textContent: "00:{f // 15:02d}"}}, {kw + f / 15:.3f});')
    js(f'tl.set("#{i} .ps-av", {{borderColor: "#36d07a"}}, {kw:.3f});')
    CUES.extend([(t0 + .05, "phone", kw - t0 - .1), (kw, "connect", 0)])
    js(f'tl.fromTo("#{i} .ps-av", {{scale: 1.25}}, {{scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false}}, {kw:.3f});')
    return html


def cutout(li, x, y, w, rot, t0, t1, rise=0, z=3):
    """The line's cut-out sticker in a slot w wide (at most 1.15 w tall); a picture print where the line has none."""
    if li in CUTPRINT:
        src = CUTPRINT[li]
        if src:
            printel(src, x + w * .08, y, w * .84, w * .84, rot, t0, t1, z=z)
        return
    name = CUTOUT.get(li)
    if not name:
        return
    p = os.path.join(ROOT, "assets", "img", "collage", "sticker", f"{name}.png")
    iw, ih = Image.open(p).size
    fw = min(w, w * 1.15 * iw / ih)
    x, w = x + (w - fw) / 2, fw
    i = nid("ct")
    if li == 3:              # the blank phone gets a live dialing screen, scaled with the sticker
        sc_ = w / iw
        PAN.append(f'<div class="el" id="{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{ih * sc_:.0f}px;'
                   f'transform:rotate({rot:.1f}deg);z-index:{z}"><img src="assets/img/collage/sticker/{name}.png" style="width:100%;display:block" alt="">'
                   f'<div style="position:absolute;left:0;top:0;width:{iw}px;height:{ih}px;transform:scale({sc_:.4f});transform-origin:0 0">'
                   f'{phone_screen(t0, t1)}</div></div>')
    else:
        PAN.append(f'<img class="el" id="{i}" src="assets/img/collage/sticker/{name}.png" style="left:{x:.0f}px;top:{y:.0f}px;'
                   f'width:{w:.0f}px;transform:rotate({rot:.1f}deg);z-index:{z}" alt="">')
    show(f"#{i}", t0, t1)
    if rise:
        js(f'tl.fromTo("#{i}", {{y: {rise}}}, {{y: 0, duration: .4, ease: "steps(6)", immediateRender: false}}, {t0:.3f});')


def g3el(li, t0, t1):
    """The line's 3D element (transparent WebM), on the board with the rest."""
    if li not in G3D_AT:
        return
    kind, x, y, w = G3D_AT[li]
    i = nid("g3")
    ts = G3T[kind]
    VTR[0] += 1
    PAN.append(f'<div class="el g3b" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px;z-index:4">'
               f'<video id="v{i}" class="clip" src="assets/video/g3d/g3{kind}.webm" data-start="{ts:.3f}" data-duration="{max(.2, t1 - ts):.3f}" '
               f'data-track-index="{VTR[0]}" muted playsinline></video></div>')
    show(f"#{i}", max(t0, ts), t1)


def star(x, y, size, t0, t1, color=WHT, n=7, seed=0):
    i = nid("st")
    PAN.append(f'<svg class="el" id="{i}" viewBox="-50 -50 100 100" style="left:{x:.0f}px;top:{y:.0f}px;width:{size}px;height:{size}px;z-index:4">'
               f'<path d="{star_path(n, seed=seed)}" fill="{color}"/></svg>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i}", {{scale: 0, rotation: -40}}, {{scale: 1, rotation: 0, duration: .134, ease: "steps(2)", immediateRender: false}}, {t0:.3f});')


def label(text, style, x, y, size, rot, t, t1, mode="type", circle=False, anchor="center", z=5):
    """A label. v12 modes, from the owner's text presets: blur (Blur Reveal: letters sharpen out of a blur behind a
    glowing smear), cascade (Gold Text: letters pop up one by one with overshoot), slide (Slide Up: words rise out of a
    blur, used for the serif phrases), flicker (neon flicker, for stamps), fall (letters drop and bounce with the owner's
    gravity expression), slam and pop. "type" picks one of them."""
    i = nid("lb")
    if style in ("blk", "wht", "magw") and text in SERIF:
        style, text = "ser", text.lower()
    size = min(size * 1.12, fit(text, 980, 999))
    w = tw(text, size) + size * .56
    left = x - w / 2 if anchor == "center" else x
    letters = "".join(f'<span class="ch{" cz" if c == "*" else ""}">{c if c != " " else "&nbsp;"}</span>' for c in text)
    if mode == "type":
        mode = ("track" if style == "ser" else "flicker" if style == "stamp"
                else ("slamx", "scramble", "flip3d", "cascade", "blur")[NID[0] % 5])
    smear = '<i class="smear"></i>' if mode == "blur" else ""
    PAN.append(f'<div class="lw" data-layout-allow-overlap style="left:{left:.0f}px;top:{y:.0f}px;transform:rotate({rot:.1f}deg);z-index:{z}">'
               f'<div class="lb {style}" id="{i}" style="font-size:{size:.0f}px">{letters}{smear}{CIRC if circle else ""}</div></div>')
    show(f"#{i}", t, t1)
    n = max(1, len(text))
    sharp = f"#{i} .ch:not(.cz)"
    if style in ("blk", "wht", "mag", "magw", "mb", "blkm"):          # the box wipes open first
        js(f'tl.fromTo("#{i}", {{clipPath: "inset(-20% 100% -20% 0%)"}}, {{clipPath: "inset(-20% -10% -20% 0%)", duration: .2, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    if mode == "blur":
        js(f'tl.fromTo("{sharp}", {{opacity: 0, filter: "blur(16px)", x: {-size * .22:.0f}}}, {{opacity: 1, filter: "blur(0px)", x: 0, duration: .22, ease: "expo.out", stagger: {min(.016, .16 / n):.3f}, immediateRender: false}}, {t:.3f});')
        js(f'tl.fromTo("#{i} .cz", {{opacity: 0}}, {{opacity: 1, duration: .3, immediateRender: false}}, {t + .1:.3f});')
        js(f'tl.fromTo("#{i} .smear", {{x: {-size * .6:.0f}, opacity: 1}}, {{x: {w:.0f}, opacity: 0, duration: .5, ease: "power2.out", immediateRender: false}}, {t:.3f});')
        done = t + .35
    elif mode == "cascade":
        js(f'tl.fromTo("#{i} .ch", {{yPercent: 115, opacity: 0, rotation: 10}}, {{yPercent: 0, opacity: 1, rotation: 0, duration: .26, ease: "back.out(2.6)", stagger: {min(.018, .18 / n):.3f}, immediateRender: false}}, {t:.3f});')
        done = t + .4
    elif mode == "slide":
        js(f'tl.fromTo("{sharp}", {{y: {size * .55:.0f}, opacity: 0, filter: "blur(10px)"}}, {{y: 0, opacity: 1, filter: "blur(0px)", duration: .4, ease: "expo.out", stagger: {min(.02, .22 / n):.3f}, immediateRender: false}}, {t:.3f});')
        done = t + .4
    elif mode == "slamx":                                    # letters slam in huge and spun, settle on twos
        js(f'tl.fromTo("#{i} .ch", {{scale: 2.6, rotation: (k) => [-24, 18, -12, 26, -8][k % 5], opacity: 0}}, '
           f'{{scale: 1, rotation: 0, opacity: 1, duration: .18, ease: "back.out(2.6)", stagger: {min(.016, .16 / n):.3f}, immediateRender: false}}, {t:.3f});')
        done = t + .2
    elif mode == "scramble":                                 # text decodes from random glyphs (AE text scramble)
        G = "#%&@$*?!/<>XZ0123456789"
        rr = random.Random(int(t * 1000))
        for f_ in range(4):
            js(f'tl.set("#{i} .ch:not(.cz)", {{textContent: (k) => "{"".join(rr.choice(G) for _ in range(40))}"[(k * 7 + {f_ * 3}) % 40]}}, {t + f_ / 15:.3f});')
        for k, c in enumerate(text):
            if c != "*":                                     # spaces come back as no-break spaces
                ch = "\\u00a0" if c == " " else c.replace(chr(34), "")
                js(f'tl.set("#{i} .ch:nth-child({k + 1})", {{textContent: "{ch}"}}, {t + 4 / 15 + k * .012:.3f});')
        done = t + .3
    elif mode == "flip3d":                                   # letters flip up out of the page
        js(f'tl.fromTo("#{i} .ch", {{rotationX: -95, transformPerspective: 500, transformOrigin: "50% 100%", opacity: 0}}, '
           f'{{rotationX: 0, opacity: 1, duration: .26, ease: "back.out(1.8)", stagger: {min(.018, .18 / n):.3f}, immediateRender: false}}, {t:.3f});')
        done = t + .25
    elif mode == "track":                                    # tracking in: wide and blurred to tight
        js(f'tl.fromTo("{sharp}", {{x: (k) => (k - {(n - 1) / 2:.1f}) * {size * .32:.0f}, filter: "blur(8px)", opacity: 0}}, '
           f'{{x: 0, filter: "blur(0px)", opacity: 1, duration: .28, ease: "expo.out", immediateRender: false}}, {t:.3f});')
        js(f'tl.fromTo("#{i} .cz", {{opacity: 0}}, {{opacity: 1, duration: .2, immediateRender: false}}, {t + .08:.3f});')
        done = t + .25
    elif mode == "flicker":
        for k, o in enumerate([1, 0, 1, .3, 1]):
            js(f'tl.set("#{i}", {{opacity: {o}}}, {t + k / 30:.3f});')
        done = t + .27
    elif mode == "fall":
        for k in range(len(text)):
            path = phys(-(380 + 45 * k), 900, g_m=55, bounce=.42, drag=.1, dur=1.0)
            t0 = t + .035 * k
            js(f'tl.set("#{i} .ch:nth-child({k + 1})", {{y: {path[0][2]:.0f}}}, {t - .001:.3f});')
            for (dt, px, py) in path[1:]:
                js(f'tl.set("#{i} .ch:nth-child({k + 1})", {{y: {py:.0f}}}, {t0 + dt:.3f});')
        done = t + .5
    elif mode == "slam":
        js(f'tl.fromTo("#{i}", {{scale: 1.65}}, {{scale: 1, duration: .22, ease: "back.out(2.2)", immediateRender: false}}, {t:.3f});')
        done = t + .25
    else:
        js(f'tl.fromTo("#{i}", {{scale: 1.4}}, {{scale: 1, duration: .2, ease: "back.out(2.2)", immediateRender: false}}, {t:.3f});')
        done = t + .2
    if circle:
        js(f'tl.fromTo("#{i} .circ path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {done + .05:.3f});')
    return i, w


def phys(y0, vy0, vx0=0.0, g_m=50.0, bounce=.42, drag=.1, fric=.3, dur=1.0, dt=1 / 30):
    """The owner's After Effects gravity expression, ported frame for frame: gravity (m/s2 x 100 px), bounce %,
    air drag % per second, ground friction on each bounce. The floor is y = 0 (the element's resting place).
    Returns [(t, x, y)] per 30 fps frame; settles to exactly 0 once the bounces die out."""
    g = g_m * 100
    x, y, vx, vy = 0.0, float(y0), float(vx0), float(vy0)
    out = [(0.0, x, y)]
    for k in range(1, int(dur / dt) + 1):
        vy += g * dt
        vx *= 1 - drag * dt
        vy *= 1 - drag * dt
        x += vx * dt
        y += vy * dt
        if y >= 0:
            y = -y
            vy = -vy * bounce
            vx *= 1 - fric
            if abs(vy) < 120:
                y, vy = 0.0, 0.0
        out.append((k * dt, x, y))
        if y == 0 and vy == 0:
            break
    return out


def ghost(text, x, y, size, t0, t1):
    i = nid("gh")
    PAN.append(f'<div class="lw" data-layout-allow-overlap style="left:{x - 700:.0f}px;top:{y:.0f}px;width:1400px;z-index:1;text-align:center"><div class="ghost" id="{i}" '
               f'style="font-size:{size}px">{text}&nbsp;{text}</div></div>')
    show(f"#{i}", t0, t1)


def para(lines, x, y, t0, t1):
    i = nid("pa")
    PAN.append(f'<div class="para el" id="{i}" style="left:{x}px;top:{y:.0f}px">{"<br>".join(lines)}</div>')
    show(f"#{i}", t0, t1)


def rect_outline(x, y, w, h, t0, t1):
    i = nid("ro")
    PAN.append(f'<i class="el rline" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>')
    show(f"#{i}", t0, t1)


def arc(x, y, size, t0, t1):
    i = nid("ar")
    PAN.append(f'<svg class="el" id="{i}" viewBox="0 0 100 100" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:4;overflow:visible">'
               f'<path pathLength="400" d="M8 70 C4 20 60 -6 96 30" fill="none" stroke="{WHT}" stroke-width="3.2" stroke-linecap="round" '
               f'stroke-dasharray="400"/></svg>')
    show(f"#{i}", t0, t1)
    js(f'tl.fromTo("#{i} path", {{strokeDashoffset: 400}}, {{strokeDashoffset: 0, duration: .27, ease: "steps(4)", immediateRender: false}}, {t0:.3f});')


def block(x, y, w, h, t0, t1, cls="magblk"):
    i = nid("bk")
    PAN.append(f'<i class="el {cls}" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>')
    show(f"#{i}", t0, t1)


def flame(x, y, t0, t1):
    i = nid("fl")
    PAN.append(f'<svg class="el" id="{i}" viewBox="0 0 100 120" style="left:{x}px;top:{y}px;width:150px;height:180px;z-index:4">'
               '<path d="M50 4 C62 30 88 42 80 78 C76 100 60 114 46 114 C26 112 12 96 16 74 C20 56 34 52 34 36 C44 46 46 56 46 64 '
               f'C56 52 58 30 50 4 Z M40 112 C30 96 38 84 48 72 C50 86 62 92 56 112" fill="{MAG}" stroke="{WHT}" stroke-width="5" '
               'stroke-linejoin="round"/></svg>')
    show(f"#{i}", t0, t1)


def cam(si, t, fx, fy, s=1.0, rot=0.0, dur=.35):
    CAMKEYS.setdefault(si, []).append((t, fx, fy, s, rot, dur * .6))


# ------------------------------------------------------------------------------------------------ recipes (Ashke)
def r1(si, a, b, li, gs):
    if li < 0:                         # v16 intro: the owner's clean photo (black on black) is the whole background
        i = nid("ib")
        PAN.append(f'<img class="el" id="{i}" src="assets/img/src/drake_back_black.jpg" style="left:-455px;top:-1264px;'
                   f'width:1800px;z-index:0" alt="">')
        show(f"#{i}", a, b)
    else:
        scrap("red", 0, 30, 230, 1020, -7, a, b)
        scrap("black", 3, 600, 40, 560, 14, a, b)
        cutout(li, 120, 150, 840, -2, a, b, rise=320)
    g3el(li, a, b)
    cam(si, a, 540, 700, 1.08, -2, .01)
    y = 1000
    for k, (txt, key, t) in enumerate(gs):
        if k == 0:
            size = fit(txt, 900, 160)
            label(txt, "blk", 540, y, size, -2, t, b, mode="slam")
            y += size * 1.12 + 26
            cam(si, t, 540, 900, 1.0, -1, .3)
        else:
            size = fit(txt, 760, 118)
            label(txt, "magw", 560, y, size, -1.5, t, b, mode="type", circle=key)
            y += size * 1.12 + 22
            cam(si, t, 540, 960 + (y - 1200) * .3, 1.02, 0, .4)
    if li < 0:
        para(["SPIN BOUT U · DRAKE & 21 SAVAGE"], 110, y + 30, gs[min(1, len(gs) - 1)][2], b)
    printel(CARD2.get(li), 620, 1380, 380, 450, 7, a + PERIOD * .5, b)
    star(60, max(1530, y + 190), 230, a + PERIOD, b, seed=si)
    star(290, max(1700, y + 330), 110, a + PERIOD * 1.5, b, color=MAG, seed=si + 1)
    if b - a > 1.4:
        FLASH.append((a + PERIOD * 2, "invert"))


def r2(si, a, b, li, gs):
    kw = next((g for g in reversed(gs) if g[1]), gs[-1])
    ki = gs.index(kw)
    if kw[2] - .067 > a + .1:
        printel(CARD1.get(li), 60, 580, 960, 1060, 2, a, kw[2] - .067)
    scrap("black", 1, -80, 1500, 900, -4, a, b)
    cam(si, a, 540, 860, 1.12, 1.5, .01)
    y = 520
    for k, (txt, key, t) in enumerate(gs[:ki]):
        size = fit(txt, 820, 120)
        label(txt, "blk", 540 - 60 * k, y, size, -2, t, b)
        y += size * 1.15 + 18
        cam(si, t, 540, 760 + 60 * k, 1.1, 1, .3)
    FLASH.append((kw[2] - .067, "white"))
    scrap("black", 3, -60, 760, 1200, -5, kw[2], b)
    size = fit(kw[0], 1060, 330)
    after_n = len(gs) - ki - 1
    if li == 6:
        td = next(g[2] for g in gs if g[0].startswith("DUMB"))
        cutout(li, 600, 1080, 460, 6, td, b, z=8)
        cam(si, td, 640, 1120, 1.05, 2, .25)
    else:
        cutout(li, 540 - 220, 860 + size * 1.25 + 150 * after_n, 440, 2, kw[2], b, z=2)
    _, fw = label(kw[0], f"fill f{li}" if li in FILL else "w3d", 540, 860, size, -3, kw[2], b, mode="slamx" if li not in FILL else "pop", z=6)
    cam(si, kw[2], 540, 960, 1.0, 0, .2)
    zt = kw[2] + .4
    after = gs[ki + 1:]
    back = min(b - .1, (after[0][2] - .05) if after else kw[2] + 1.0, zt + .55)
    if back - zt > .2:
        cam(si, zt, 540 + fw * .22, 860 + size * .5, 2.6, -2, .27)
        cam(si, back, 540, 1000, 1.0, 0, .27)
    y = 860 + size + 20
    for txt, key, t in after:
        sz = fit(txt, 820, 120)
        label(txt, "wht", 560, y, sz, 2, t, b)
        y += sz * 1.15 + 18
        cam(si, max(t, back + .05), 540, 1080, 1.0, 0, .35)


def r3(si, a, b, li, gs):
    kw = next((g for g in gs if g[1]), gs[-1])
    scrap("grey", 0, -80, 880, 1240, 3, a, b)
    scrap("black", 2, 720, 120, 420, -10, a, b)
    g0 = gs[0]
    size = fit(g0[0], 860, 140)
    label(g0[0], "mb", 520, 520, size, -2, g0[2], b)
    cam(si, a, 540, 560, 1.45, -2, .01)
    rest = [g for g in gs[1:] if g is not kw]
    t_pull = rest[0][2] if rest else (kw[2] if kw is not g0 else a + .6)
    block(170, 960, 740, 560, t_pull, b)
    printel(CARD2.get(li), 700, 70, 340, 400, 8, t_pull, b)
    cutout(li, 150, 640, 780, 1, t_pull, b)
    g3el(li, t_pull, b)
    cam(si, t_pull, 540, 1000, 1.0, 0, .4)
    for k, (txt, key, t) in enumerate(rest):
        label(txt, "blk", 300 + 60 * k, 700 + 130 * k, fit(txt, 600, 100), -4, t, b)
    if kw is not g0:
        scrap("white", 1, 140, 1320, 800, -3, kw[2], b, z=4)
        label(kw[0], "m3d", 540, 1390, fit(kw[0], 760, 200), -3, kw[2], b, z=6)
        ghost(kw[0], 540, 1640, 250, kw[2], b)
        cam(si, kw[2], 540, 1090, 1.03, 0, .35)


def r4(si, a, b, li, gs):
    kw = next((g for g in gs if g[1]), gs[-1])
    g0 = gs[0]
    FLASH.append((a, "invert"))
    label(g0[0], "stamp", 540, 260, fit(g0[0], 1000, 300), 0, g0[2], b, z=4)
    if li != 14:
        rect_outline(200, 560, 680, 560, a + .134, b)
    scrap("red", 1, 560, 760, 520, 6, a + .134, b)
    cam(si, a, 540, 430, 1.3, 0, .01)
    mids = [g for g in gs[1:] if g is not kw]
    t_cut = min(mids[0][2] if mids else (kw[2] if kw is not g0 else a + .5), a + .45)
    cutout(li, 150, 480, 780, -1, t_cut, b)
    g3el(li, a + .134, b)
    if li == 3:
        printel(CARD2[li], 20, 420, 300, 650, -8, t_cut + PERIOD / 2, b, z=4)
    else:
        printel(CARD2.get(li), 30, 560, 300, 360, -8, t_cut + PERIOD / 2, b)
    cam(si, t_cut, 540, 820, 1.18, 0, .35)
    for k, (txt, key, t) in enumerate(mids):
        label(txt, "blk", 780, 1180 + 120 * k, fit(txt, 520, 96), 4, t, b, z=6)
    if kw is not g0:
        scrap("black", 0, -90, 1300, 1260, -3, kw[2] - .067, b, z=4)
        label(kw[0], "w3d", 540, 1420, fit(kw[0], 820, 220), -2, kw[2], b, z=6)
        cam(si, kw[2], 540, 1250, 1.15, 0, .3)
        if b - kw[2] > .7:
            cam(si, kw[2] + .45, 540, 960, .92, 0, .4)


def r5(si, a, b, li, gs):
    g0 = gs[0]
    scrap("red", 2, 20, 600, 700, -9, a, b)
    printel(CARD1.get(li), 120, 520, 640, 760, -5, a, b)
    g3el(li, a, b)
    cam(si, a, 520, 860, 1.05, -1, .01)
    label(g0[0], "stamp", 540, 260, fit(g0[0], 1000, 270), -1, g0[2], b, z=4)
    cam(si, g0[2], 540, 620, 1.0, 0, .3)
    rest = gs[1:]
    y = 1320
    for k, (txt, key, t) in enumerate(rest):
        if k == 0:
            FLASH.append((t, "invert"))
        sz = fit(txt, 760, 118)
        label(txt, "blk" if (key or k % 2 == 0) else "wht", 430 + (k % 2) * 120, y, sz, -3 + 5 * (k % 2), t, b, circle=key, z=6,
              mode="fall" if (li == 12 and key) else "type")
        y += sz * 1.15 + 22
        cam(si, t, 520, min(1250, 1000 + 70 * k), 1.0, 0, .35)
    tc = rest[len(rest) // 2][2] if rest else a + .8
    if li in CARD2 and li not in (12,):
        printel(CARD2[li], 500, 700, 560, 700, 6, tc, b, red=True)
        cam(si, tc + .1, 640, 1100, 1.0, 1, .4)


def r6(si, a, b, li, gs):
    kw = gs[-1]
    printel(CARD1.get(li), 400, 170, 660, 760, 9, a, b)
    scrap("black", 1, 90, 960, 780, -4, a, b)
    cam(si, a, 600, 640 if li == 13 else 860, 1.0, 1, .01)
    rest = [g for g in gs if g is not kw]
    y = 1040
    for k, (txt, key, t) in enumerate(rest):
        sz = fit(txt, 760, 150)
        label(txt, "wht" if k == 0 else "blk", 400 + 120 * (k % 2), y, sz, -3 + 4 * k, t, b, circle=key, z=6)
        y += sz * 1.15 + 20
        cam(si, t, 480, 1000 + 40 * k, 1.0, 0, .35)
    label(kw[0], "mlet", 560, y + 20, fit(kw[0], 900, 240), -6, kw[2], b, circle=kw[1], z=6)
    star(720, y + 240, 90, kw[2] + .2, b, color=MAG, n=6, seed=si)
    star(830, y + 300, 60, kw[2] + .27, b, color=WHT, n=6, seed=si + 5)
    cam(si, kw[2], 540, min(1250, y + 60), 1.08, -1, .35)


def r7(si, a, b, li, gs):
    kw = gs[-1]
    rest = gs[:-1]
    scrap("black", 2, 260, 110, 480, 8, a, b)
    cam(si, a, 540, 760, 1.0, 0, .01)
    y = 330
    for k, (txt, key, t) in enumerate(rest):
        sz = fit(txt, 760, 112 if k == 0 else 108)
        label(txt, "mtyp" if k == 0 else "blk", 560 + (40, -40)[k % 2], y, sz, (-6, 3)[k % 2], t, b, z=6)
        cam(si, t, 560, y + 260, 1.1, -1, .3)
        y += sz * 1.3 + 24
    ksz = fit(kw[0], 900, 180)
    label(kw[0], "wht", 540, y + 10, ksz, -2, kw[2], b, circle=kw[1], z=6)
    cam(si, kw[2], 540, y + 300, 1.04, 0, .35)
    printel(CARD1.get(li), 140, y + ksz * 1.35 + 40, 760, 660, -3, a, b)


def r8(si, a, b, li, gs):
    kw = next((g for g in reversed(gs) if g[1]), gs[-1])
    g0 = gs[0]
    FLASH.append((a, "invert"))
    t2 = gs[1][2] if len(gs) > 1 else a + .9
    scrap("red", 0, -60, 1080, 960, -8, a, t2)
    scrap("black", 2, -160, 720, 420, 4, a, t2)
    cutout(li, 90, 260, 900, 0, a, t2)
    flame(800, 1260, a + .2, t2)
    label(g0[0], "magw", 540, 1270, fit(g0[0], 900, 150), -2, g0[2], t2, z=6)
    cam(si, a, 540, 960, 1.0, 0, .01)
    cam(si, g0[2], 540, 1060, 1.05, 0, .3)
    scrap("red", 3, -40, 1180, 1000, -6, t2, b)
    if li != 15:                       # the heart takes this slot on the second "the way"
        cutout(li, 280, 640, 540, 0, t2, b)
    g3el(li, t2, b)
    printel(CARD2.get(li), 660, 1060, 360, 430, 8, t2 + .1, b)
    flame(760, 1380, t2, b)
    label(g0[0], "magw", 540, 220, fit(g0[0], 800, 120), -4, t2, b, mode="pop", z=6)
    for k, (txt, key, t) in enumerate(g for g in gs[1:] if g is not kw):
        label(txt, "blkm", 540, 420 + 150 * k, fit(txt, 900, 130), -2, t, b, z=6)
    if kw is not g0:
        label(kw[0], "stamp", 540, 1420, fit(kw[0], 1000, 250), -3, kw[2], b, z=5)
    cam(si, t2, 540, 880, 1.0, 0, .01)
    cam(si, t2 + .3, 540, 920, 1.04, 0, .5)


def r9(si, a, b, li, gs):
    FLASH.append((a, "split"))
    if li == 18:
        hero = printel(CL + "a_walk.mp4", 30, 260, 1020, 1240, -2, a, b, z=2)
        for k_, (sx, sy, ss) in enumerate([(820, 330, 120), (180, 520, 80), (860, 820, 70)]):
            star(sx, sy, ss, a + .6 + .12 * k_, b, color=(WHT, MAG, WHT)[k_], seed=si + k_)
    else:
        printel(CARD2.get(li), 600, 60, 440, 550, 7, a + .067, b)
    scrap("grey", 3, -160, -90, 1000, 5, a, b)
    scrap("grey", 1, 420, 1560, 860, -7, a, b)
    scrap("black", 2, -120, 880, 760, 3, a, b)            # dark under the stamp: the stamp is off-white here
    kw = next((g for g in reversed(gs) if g[1]), gs[-1]) if gs else None
    rest = [g for g in gs if g is not kw]
    styles = ["magw", "mag", "w3d", "blk"]
    y = 980 if li == 18 else 560 if len(rest) > 2 else 700
    cam(si, a, 470, y + 120, 1.15, -1, .01)
    for k, (txt, key, t) in enumerate(rest):
        x = 540 + (-80, 80)[k % 2]
        sz = fit(txt, 820, (170, 140, 190, 130)[k % 4])
        label(txt, styles[k % 4], x, y, sz, (-2, 3, -2, -3)[k % 4], t, b, z=6)
        cam(si, t, (x + 540) / 2, y + sz * .6, 1.12, (-2, 3, -2, -3)[k % 4] * .3, .3)
        y += sz * 1.3 + 34
    if kw:
        sz = fit(kw[0], 1000, 290)
        label(kw[0], "stamp", 540, y + 10, sz, -2, kw[2], b, circle=kw[1], z=5)
        cam(si, kw[2], 540, y + sz * .6, 1.0, 0, .4)
    if li in CUTOUT:
        cutout(li, 600, 40, 440, 6, a + .067, b, z=4)


ICON_AT = {"R1": (800, 1500, 8), "R2": (60, 300, -8), "R3": (790, 330, 10), "R4": (90, 1100, -10), "R5": (810, 1520, 8),
           "R6": (60, 1540, -6), "R7": (60, 300, -8), "R8": (90, 960, -10), "R9": (780, 1460, 10)}


ICON_LI = {14: (830, 760, 8), 16: (30, 250, -8), 7: (760, 700, 8), 0: (800, 1480, 8)}


def lyric_icons():
    for si, (a, b, li) in enumerate(scenes()):
        if li in FOOT:
            continue
        gs = groups_of(li) if li >= 0 else [("", True, a + 1.2)]
        kws = [g for g in gs if g[1]]
        t = (kws[-1] if kws else gs[len(gs) // 2])[2]
        rec = RECIPE[li]
        if rec == "R8" and len(gs) > 1:
            t = max(t, gs[1][2])
        if t >= b - .15:
            t = max(a + .2, b - .5)
        x, y, rot = ICON_LI.get(li, ICON_AT[rec])
        i = nid("ic")
        PAN.append(f'<div class="el" id="{i}" style="left:{x}px;top:{y}px;width:230px;height:230px;z-index:7;transform:rotate({rot}deg)">'
                   f'{svg(ICON[li])}<b class="itag">{WORD[li]}</b></div>')
        show(f"#{i}", t, b)
        g = random.Random(si * 7 + 1)
        path = phys(-420, 1300, vx0=g.choice([-1, 1]) * g.uniform(220, 420), g_m=48, bounce=.45, drag=.15, fric=.35, dur=1.1)
        x_end = path[-1][1]
        first = next((dt for dt, px, py in path[1:] if py >= -2), .2)
        CUES.append((t + first, "sticker", 0))
        for (dt, px, py) in path:
            spin = (rot - 28 * (1 if x_end > 0 else -1)) + 28 * (1 if x_end > 0 else -1) * min(1, dt / .5)
            js(f'tl.set("#{i}", {{x: {px - x_end:.0f}, y: {py:.0f}, rotation: {spin:.1f}}}, {t + dt:.3f});')


def transition_frames():
    """Three single-frame stills (one 30 fps frame each) right before most cuts: the Ashke transitions' frame pacing."""
    k = 0
    for si, (a, b, li) in enumerate(scenes()):
        if si == 0 or RECIPE[li] in ("R4", "R8", "R9"):
            continue
        for j in range(3):
            src = STILLS[k % len(STILLS)]
            k += 1
            i = nid("tf")
            rot = (-4, 5, -2)[j]
            w = (820, 700, 900)[j] * .82
            SCREEN.append(f'<div class="tframe" id="{i}" style="left:{540 - w / 2:.0f}px;top:{CY - w * 1.25 / 2:.0f}px;width:{w:.0f}px;height:{w * 1.25:.0f}px;'
                          f'transform:rotate({rot}deg)"><img src="{src}" alt=""></div>')
            t0 = a - (3 - j) / 30
            show(f"#{i}", t0, t0 + 1 / 30)


FOOT = {11: "f_hook1", 15: "f_hook2", 18: "f_end"}     # v17: full-screen footage, Eimantas style
LOOKS = {"grade": "contrast(1.14) saturate(1.2) sepia(.2) hue-rotate(-8deg)",
         "thr": "grayscale(1) contrast(4.2) brightness(1.06)",
         "red": "grayscale(1) contrast(1.8) brightness(.95)",
         "bw": "grayscale(1) contrast(1.35) brightness(.98)"}


def footage_scene(si, a, b, li, gs):
    """From "the way" on (owner), the edit cuts back and forth between the collage and the walking clip full screen,
    treated like the Eimantas reference: footage held on 12 fps, looks cut on the beat (warm grade / stark B/W
    threshold / red monochrome / B/W), white streak glitches, small red serif lyrics appearing word by word as they are
    sung, the keyword big in the centre; the last shot double-exposes the intro photo."""
    src = f"{CL}{FOOT[li]}.mp4"
    n = float(os.popen(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{os.path.join(ROOT, src)}"').read() or 0)
    i = nid("ft")
    VTR[0] += 1
    dbl = (f'<img class="fdbl" src="assets/img/src/drake_back_black.jpg" alt="">' if li == 18 else "")
    streaks = "".join(f'<i class="fst" style="left:{x}px"></i>' for x in (140, 610, 880))
    SCREEN.append(f'<div class="foot el" id="{i}"><video id="v{i}" src="{src}" data-start="{a:.3f}" data-duration="{min(n, b - a):.3f}" '
                  f'data-track-index="{VTR[0]}" muted playsinline></video><div class="fred"></div>{dbl}{streaks}'
                  f'<div class="fcap"></div><div class="fkey"></div></div>')
    show(f"#{i}", a, b)
    order = (["grade", "thr", "red", "grade", "bw", "thr", "red", "grade"] if li != 18 else ["bw", "thr", "bw", "red"])
    beats = [a] + [t for t in BEATS["beats"][::2] if a + .3 < t < b - .1]
    for k, t in enumerate(beats):
        look = order[k % len(order)]
        js(f'tl.set("#v{i}", {{filter: "{LOOKS[look]}"}}, {t:.3f});')
        js(f'tl.set("#{i} .fred", {{opacity: {1 if look == "red" else 0}}}, {t:.3f});')
        if k and k % 2 == 0:                                 # white streak glitch for two frames on the switch
            js(f'tl.set("#{i} .fst", {{opacity: 1, x: (j) => [0, -40, 30][j] + {k * 37 % 90 - 45}}}, {t:.3f});')
            js(f'tl.set("#{i} .fst", {{opacity: 0}}, {t + 2 / 30:.3f});')
            CUES.append((t, "streak", 0))
    # captions: words of each group appear as they are sung, small red serif; the keyword big in the centre
    words = list(words_of(li))
    wi = 0
    for gk, (txt, key, t) in enumerate(gs):
        toks = txt.split()
        t_end = gs[gk + 1][2] if gk + 1 < len(gs) else b
        times = []
        for _ in toks:
            times.append(words[wi][1] if wi < len(words) else t)
            wi += 1
        box = "fkey" if key else "fcap"
        spans = "".join(f'<span class="fw{" cz" if "*" in w else ""}">{w}</span>' for w in toks)
        j = nid("fc")
        SCREEN.append(f'<div class="{box}-line el" id="{j}">{spans}</div>')
        show(f"#{j}", t, t_end if not key else min(t_end, t + 1.2))
        js(f'tl.set("#{j} .fw", {{display: "none"}}, {t - .001:.3f});')     # words join the line as sung, centred
        for w_, tw in enumerate(times):
            js(f'tl.set("#{j} .fw:nth-child({w_ + 1})", {{display: "inline"}}, {max(t, tw):.3f});')
        if key:
            FLASH.append((t, "white"))
            js(f'tl.fromTo("#{j}", {{scale: 1.5}}, {{scale: 1, duration: .2, ease: "expo.out", immediateRender: false}}, {t:.3f});')


def cut_bursts():
    """v16: every cut is a short burst instead of one clean cut, rotating the owner's three references:
    ink (Eimantas: a grunge ink matte eats the frame and recedes off the next shot), tear (YouMotion: a torn paper sheet
    slides across in stepped frames), stutter (Eimantas / YouMotion: B/W threshold still, invert, duotone still, white
    blast, one frame each), slam (Jennifer: two stop-motion stills slammed in). Section changes get ink + stutter."""
    big = {6, 10, 11, 15, 17, 18}
    SCREEN.append('<svg id="ink" viewBox="0 0 1080 1080" preserveAspectRatio="none"><rect width="1080" height="1080" fill="#0b0608" filter="url(#inkf)"/></svg>')
    HIDE.append("#ink")
    order = ["tear", "stutter", "ink", "slam"]
    k = 0
    for si, (a, b, li) in enumerate(scenes()):
        if si == 0:
            continue
        styles = ["ink", "stutter"] if li in big else [order[si % 4]]
        for st in styles:
            if st == "ink":                                  # coverage 100% -> 0 over 4 frames after the cut
                js(f'tl.set("#ink", {{opacity: 1}}, {a - 1 / 30:.3f});')
                for j, ic in enumerate([1.2, .55, -.1, -.6, -1.4]):
                    js(f'tl.set("#inkA", {{attr: {{intercept: {ic}}}}}, {a - 1 / 30 + j / 15:.3f});')
                    js(f'tl.set("#inkT", {{attr: {{seed: {si * 7 + j}}}}}, {a - 1 / 30 + j / 15:.3f});')
                js(f'tl.set("#ink", {{opacity: 0}}, {a + 4 / 15:.3f});')
            elif st == "tear":
                i = nid("tr")
                kind = ("black", "mag", "white")[si % 3]
                SCREEN.append(f'<img class="tear" id="{i}" src="assets/img/collage/scrap/{kind}-{si % 4}.png" alt="">')
                HIDE.append(f"#{i}")
                js(f'tl.set("#{i}", {{opacity: 1}}, {a - 3 / 15:.3f});')
                for j, x in enumerate([-1900, -1100, -400, 300, 1100]):
                    js(f'tl.set("#{i}", {{x: {x}, rotation: {(-8, -5, -3, -1, 2)[j]}}}, {a - 3 / 15 + j / 15:.3f});')
                js(f'tl.set("#{i}", {{opacity: 0}}, {a + 2 / 15:.3f});')
            elif st == "stutter":
                for j, kind in enumerate(["thr", "inv", "duo", "white"]):
                    t0 = a - (4 - j) / 30
                    if kind in ("thr", "duo"):
                        src = STILLS[k % len(STILLS)]
                        k += 1
                        i = nid("tf")
                        SCREEN.append(f'<div class="tframe {kind}" id="{i}" style="left:0;top:0;width:1080px;height:1080px;padding:0">'
                                      f'<img src="{src}" alt=""></div>')
                        show(f"#{i}", t0, t0 + 1 / 30)
                    elif kind == "inv":
                        FLASH.append((t0, "invert"))
                    else:
                        FLASH.append((t0, "white"))
            else:                                            # slam: two stop-motion stills
                for j in range(2):
                    src = STILLS[k % len(STILLS)]
                    k += 1
                    i = nid("tf")
                    w = (760, 880)[j]
                    SCREEN.append(f'<div class="tframe" id="{i}" style="left:{540 - w / 2:.0f}px;top:{540 - w * 1.2 / 2:.0f}px;width:{w}px;'
                                  f'height:{w * 1.2:.0f}px;transform:rotate({(-6, 4)[j]}deg)"><img src="{src}" alt=""></div>')
                    t0 = a - (2 - j) * 2 / 30
                    show(f"#{i}", t0, t0 + 2 / 30)


# ------------------------------------------------------------------------------------------------ camera (Ashke)
DIRS = [(0, 1), (0, 1), (1, .3), (0, 1), (-.8, .6), (0, -1), (.7, .7), (0, 1), (-1, 0), (0, 1), (.6, .8), (1, 0)]


def camera():
    plans = []
    for si, (a, b, li) in enumerate(scenes()):
        keys = sorted(CAMKEYS.get(si, [(a, 540, 960, 1.0, 0, .01)]))
        d = DIRS[si % len(DIRS)]
        n = math.hypot(*d)
        d = (d[0] / n, d[1] / n)
        pts = [(a, keys[0][1], keys[0][2], keys[0][3], keys[0][4])]
        for (tk, kx, ky, ks, kr, kd) in keys[1:]:
            tt = min(max(tk + .06, pts[-1][0] + .07), b - .05)
            if tt > pts[-1][0] + .05:
                pts.append((tt, kx, ky, ks, kr))
        lx, ly, ls, lr = pts[-1][1:]
        run = min(440, 520 * (b - pts[-1][0]))
        pts.append((b + .001, lx + d[0] * run, ly + d[1] * run, ls, lr))
        plans.append(dict(a=a, b=b, li=li, d=d, pts=pts))
    tend = DUR - .5
    E, X, TAU = 720, 620, .05

    def herm(pts, t, idx):
        T = [p[0] for p in pts]
        k = max(0, min(len(pts) - 2, max(i for i in range(len(pts)) if T[i] <= t + 1e-9)))
        t0, t1 = T[k], T[k + 1]
        u = max(0, min(1, (t - t0) / max(1e-6, t1 - t0)))

        def tan(m):
            lo, hi = max(0, m - 1), min(len(pts) - 1, m + 1)
            return (pts[hi][idx] - pts[lo][idx]) / max(1e-6, T[hi] - T[lo])
        p0, p1 = pts[k][idx], pts[k + 1][idx]
        m0, m1 = tan(k) * (t1 - t0), tan(k + 1) * (t1 - t0)
        h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
        return h00 * p0 + h10 * m0 + h01 * p1 + h11 * m1

    def focus(si, t):
        p = plans[si]
        fx, fy, s, rot = (herm(p["pts"], t, i) for i in (1, 2, 3, 4))
        u = max(0, t - p["a"])
        e = math.exp(-u / TAU)
        fx -= p["d"][0] * E * e
        fy -= p["d"][1] * E * e
        rot += 3 * e * (1 if si % 2 else -1)
        if si + 1 < len(plans):
            nd = plans[si + 1]["d"]
            x = math.exp(-max(0, p["b"] - t) / TAU)
            fx += nd[0] * X * x
            fy += nd[1] * X * x
            rot += 2 * x * (1 if si % 2 else -1)
        return fx, fy, s, rot

    td = next(s_ for w, s_ in words_of(12) if w == "dropped")       # dropped: the frame falls out and slams back in
    DROP = {round(td * 30) + k: y for k, y in enumerate([210, 420, 710, 1000, 120, -760, -480, -200, -75, 50, 11, -28, -8, 12, 0])}
    blurred = False
    for f in range(int(DUR * 30)):
        t = math.floor(f / 2) / 15                           # v16: the camera holds every other frame (on twos)
        si = max(i for i, p in enumerate(plans) if p["a"] <= t + 1e-6)
        fx, fy, s, rot = focus(si, t)
        px, py, _, _ = focus(si, max(plans[si]["a"], t - STEP)) if t - STEP >= plans[si]["a"] else focus(si, t + STEP)
        vx, vy = (fx - px) * s, (fy - py) * s
        if t - STEP < plans[si]["a"]:
            vx, vy = -vx, -vy
        lb = max([bt for bt in BEATS["beats"] if bt <= t + 1e-6] or [-9])
        s *= 1 + .34 * math.exp(-(t - plans[si]["a"]) / .055)         # zoom snap into every scene
        fy = 960 + (fy - 960) * VTRACK
        dy = DROP.get(f, 0)
        if dy:
            fy -= dy / (s * 1.06 * ZOOM)
        CAMSTATE[f] = (fx, fy, s * 1.06 * ZOOM, rot)
        if f % 2 == 0:
            js(f'tl.set("#pan", {{x: {540 - fx:.1f}, y: {CY - fy:.1f}}}, {t:.3f});')
            js(f'tl.set("#cam", {{scale: {s * 1.06 * ZOOM:.4f}, rotation: {rot:.2f}}}, {t:.3f});')
        sp = math.hypot(vx, vy)
        if sp > 90:
            k = min(13, sp * .045)
            js(f'tl.set("#mbg", {{attr: {{stdDeviation: "{abs(vx) / sp * k:.1f} {abs(vy) / sp * k:.1f}"}}}}, {t:.3f});')
            if not blurred:
                js(f'tl.set("#cam", {{filter: "url(#mb)"}}, {t:.3f});')
                blurred = True
        elif blurred:
            js(f'tl.set("#cam", {{filter: "none"}}, {t:.3f});')
            blurred = False


# ------------------------------------------------------------------------------------------------ lyric concepts
def conc(html, t0, t1, z=5):
    i = nid("cc")
    PAN.append(html.replace("ID", i).replace("ZZ", str(z)))
    show(f"#{i}", t0, t1)
    return i


def words_of(li):
    return [(w.lower().strip(",.'"), s) for w, s, e in L[li]["words"]]


def concepts():
    """Motion-graphics concepts drawn from what each line says, where the removed anime pictures were."""
    sc = {li: (a, b) for a, b, li in scenes()}
    # ten toes: footsteps march up the page one per beat, a 10 counter ticks with them and slams
    a, b = sc[7]
    steps = [t for t in BEATS["beats"] if a + .05 < t < b - .1][:10]
    for k, t in enumerate(steps):
        x, y = 60 + k * 92, (1600 if k % 2 == 0 else 1660)
        i = conc(f'<svg class="el" id="ID" viewBox="0 0 120 120" style="left:{x}px;top:{y}px;width:170px;height:170px;z-index:ZZ;'
                 f'transform:rotate({78 if k % 2 == 0 else 102}deg)">' + svg_foot(k % 2) + '</svg>', t, b)
        CUES.append((t, "step", 0))
        js(f'tl.fromTo("#{i}", {{scale: 1.8}}, {{scale: 1, duration: .134, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
    cnt = conc(f'<div class="el counter" id="ID" style="left:840px;top:1330px;z-index:ZZ;font-size:230px">1</div>', steps[0] if steps else a, b, z=6)
    for k, t in enumerate(steps):
        js(f'tl.set("#{cnt}", {{textContent: "{k + 1}"}}, {t:.3f});')
        js(f'tl.fromTo("#{cnt}", {{scale: 1.5}}, {{scale: 1, duration: .134, ease: "steps(2)", immediateRender: false}}, {t:.3f});')
    # wherever I say go: a GPS route draws across, pins drop on each "go", a compass needle snaps round
    a, b = sc[8]
    gos = [s_ for w, s_ in words_of(8) if w == "go"]
    route = "M120 1500 C 160 1420, 190 1360, 250 1330 S 600 1250, 700 1170 S 860 1080, 900 1060"
    rt = conc(f'<svg class="el" id="ID" viewBox="0 0 1080 1920" style="left:0;top:0;width:1080px;height:1920px;z-index:ZZ;overflow:visible">'
              f'<path d="{route}" pathLength="1000" fill="none" stroke="{WHT}" stroke-width="16" stroke-dasharray="1000" stroke-linecap="round"/>'
              f'<path d="{route}" pathLength="1000" fill="none" stroke="{MAG}" stroke-width="8" stroke-dasharray="14 18" stroke-linecap="round"/></svg>', a, b, z=4)
    js(f'tl.fromTo("#{rt} path", {{strokeDashoffset: 1000}}, {{strokeDashoffset: 0, duration: {max(.4, gos[-1] - a):.2f}, ease: "steps({max(4, round((gos[-1] - a) * 15))})", immediateRender: false}}, {a:.3f});')
    for k, (t, (px, py)) in enumerate(zip([a + .2] + gos, [(120, 1500), (250, 1330), (900, 1060)])):
        CUES.append((t + .2, "pin", 0))
        i = conc(f'<svg class="el" id="ID" viewBox="0 0 100 130" style="left:{px - 60}px;top:{py - 150}px;width:120px;height:156px;z-index:ZZ">'
                 f'<path d="M50 125 C20 80 6 62 6 44 A44 44 0 1 1 94 44 C94 62 80 80 50 125 Z" fill="{MAG}" stroke="{WHT}" stroke-width="8"/>'
                 f'<circle cx="50" cy="44" r="16" fill="{WHT}"/></svg>', t, b, z=6)
        js(f'tl.fromTo("#{i}", {{y: -260, scale: 1.3}}, {{y: 0, scale: 1, duration: .2, ease: "steps(3)", immediateRender: false}}, {t:.3f});')
    cp = conc(f'<svg class="el" id="ID" viewBox="-110 -110 220 220" style="left:600px;top:1180px;width:400px;height:400px;z-index:ZZ">'
              f'<circle r="100" fill="{INK}" stroke="{WHT}" stroke-width="8"/>'
              + "".join(f'<text x="{78 * math.sin(k * math.pi / 2):.0f}" y="{-78 * math.cos(k * math.pi / 2) + 9:.0f}" fill="{WHT}" font-family="Anton" font-size="28" text-anchor="middle">{d}</text>'
                        for k, d in enumerate("NESW")) +
              f'<g class="ndl"><path d="M0 -70 L14 0 L0 12 L-14 0 Z" fill="{MAG}"/><path d="M0 70 L14 0 L0 -12 L-14 0 Z" fill="{WHT}"/></g></svg>', a, b, z=5)
    ang = 0
    for k, t in enumerate([a] + gos + [b - .3]):
        ang += 160 + 70 * k
        CUES.append((t, "tick", 0))
        js(f'tl.to("#{cp} .ndl", {{rotation: {ang}, svgOrigin: "0 0", duration: .2, ease: "back.out(3)"}}, {t:.3f});')
    # comin' out my body: glowing wisps rising out of the 3D BODY
    a, b = sc[16]
    g = random.Random(16)
    for k in range(14):
        x = g.uniform(160, 920)
        i = conc(f'<i class="el wisp" id="ID" style="left:{x:.0f}px;top:1300px;width:{g.uniform(30, 70):.0f}px;height:{g.uniform(120, 260):.0f}px;z-index:ZZ"></i>', a, b, z=5)
        per = g.uniform(1.2, 2.0)
        st = a - g.uniform(0, per)
        while st < b:
            nn = max(2, round(per * 15))
            js(f'tl.fromTo("#{i}", {{y: 0, opacity: .9, scaleY: .6}}, {{y: -900, opacity: 0, scaleY: 1.4, duration: {per:.2f}, ease: "steps({nn})", immediateRender: false}}, {max(a, st):.3f});')
            st += per


def svg_foot(right):
    s_ = -1 if right else 1
    return (f'<g transform="translate(60 60) scale({s_} 1) translate(-60 -60)">'
            f'<path d="M48 42 C30 50 32 96 50 106 C68 114 80 96 76 72 C74 56 64 38 48 42 Z" fill="{WHT}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="62" cy="14" r="9" fill="{MAG}" stroke="{INK}" stroke-width="4"/><circle cx="78" cy="22" r="7" fill="{MAG}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="88" cy="35" r="6" fill="{MAG}" stroke="{INK}" stroke-width="4"/><circle cx="44" cy="20" r="8" fill="{MAG}" stroke="{INK}" stroke-width="4"/></g>')


def finishing():
    """The After Effects pass on the cuts: a bloom burst on some cuts (random), a light leak sweep on others, a colour
    split on every whip."""
    g = random.Random(31)
    for si, (a, b, li) in enumerate(scenes()):
        if si == 0:
            continue
        r = g.random()
        fil = []
        for k in range(4):
            parts = []
            if r < .6:
                parts.append("url(#bloom)")
            if k < 2:
                parts.append("url(#rgbsplit)")
            fil.append(" ".join(parts) or "url(#dglow)")
        for k in range(4):
            t = a - STEP + k * STEP
            js(f'tl.set("#glow", {{filter: "{fil[k]}"}}, {t:.3f});')
            js(f'tl.set("#blg", {{attr: {{stdDeviation: {[26, 20, 13, 7][k]}}}}}, {t:.3f});')
            js(f'tl.set("#rgbR", {{attr: {{dx: {[30, 16, 0, 0][k]}}}}}, {t:.3f});')
            js(f'tl.set("#rgbB", {{attr: {{dx: {[-30, -16, 0, 0][k]}}}}}, {t:.3f});')
        js(f'tl.set("#glow", {{filter: "url(#dglow)"}}, {a + 3 * STEP:.3f});')
        if r >= .45:
            js(f'tl.set("#leak", {{opacity: 1}}, {a - STEP:.3f});')
            js(f'tl.fromTo("#leak", {{x: {-900 if si % 2 else 900}, opacity: 1}}, {{x: {900 if si % 2 else -900}, opacity: 0, duration: .5, ease: "steps(8)", immediateRender: false}}, {a - STEP:.3f});')


# ------------------------------------------------------------------------------------------------ full-screen lyric effects
def locked(inner, t0, t1, z=5):
    """A full-screen layer pinned to the screen but living in the board under the lyric labels, so the words stay
    readable while the whole picture burns / fills with smoke. pin_locks() counter-moves it against the camera."""
    i = nid("lk")
    PAN.insert(0, f'<div class="el lock" id="{i}" style="z-index:{z}">{inner}</div>')
    show(f"#{i}", t0, t1)
    LOCKS.append((i, t0, t1))
    return i


def pin_locks():
    for i, t0, t1 in LOCKS:
        for f in range(int(t0 * 30) - 1, int(t1 * 30) + 2):
            if f in CAMSTATE:
                fx, fy, S, rot = CAMSTATE[f]
                js(f'tl.set("#{i}", {{x: {fx - 540:.1f}, y: {fy - CY:.1f}, scale: {1 / S:.4f}, rotation: {-rot:.2f}}}, {f / 30:.3f});')


def front_layer(gid, fil, t0, t1, y_from, y_to, t_full, L, drift, z=5, extra=""):
    """A procedural noise front sweeping up the screen (filter fil maps the swept value to colour)."""
    svg = (f'<svg viewBox="-80 -80 1240 1240" style="position:absolute;left:-80px;top:-80px;width:1240px;height:1240px;overflow:visible">'
           f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{y_from - L / 2:.0f}" x2="0" y2="{y_from + L / 2:.0f}">'
           f'<stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient></defs>'
           f'<rect x="-80" y="-80" width="1240" height="1240" fill="url(#{gid})" filter="url(#{fil})"/></svg>{extra}')
    i = locked(svg, t0, t1, z)
    n = max(1, round((t_full - t0) * 30))
    for k in range(n + 1):
        u = k / n
        yf = y_from + (y_to - y_from) * (1 - (1 - u) ** 1.35)
        js(f'tl.set("#{gid}", {{attr: {{y1: {yf - L / 2:.0f}, y2: {yf + L / 2:.0f}}}}}, {t0 + k / 30:.3f});')
    off = {"firef": "fireo", "smk2": "smko"}[fil]
    m = max(1, round((t1 - t0) * 30))
    for k in range(m + 1):
        js(f'tl.set("#{off}", {{attr: {{dx: {drift[0] * k / m:.0f}, dy: {drift[1] * k / m:.0f}}}}}, {t0 + k / 30:.3f});')
    return i


def lighter_throw(a, b):
    """Burn somebody block, with the live pixel mascot (owner): he walks in, cocks a lit lighter back and flings it;
    it arcs with the gravity expression, bounces once, and the fire starts where it lands. He stays in front of the
    flames, rim-lit orange. Returns the landing time."""
    tw = next(s_ for w, s_ in words_of(14) if w == "burn")
    S, X0, Y0 = 11, 20, 540
    dr, dhtml = sprite("drake", 0, 0, S)
    w = nid("pw")
    PAN.append(f'<div class="el pxone" id="{w}" style="left:{X0}px;top:{Y0}px;z-index:6">{dhtml}</div>')
    show(f"#{w}", a, b)
    t_in = walk_in(dr, -420, a, .3, S)
    idle(dr, "drake", t_in, tw - .22, S)
    set_frame(dr, "drake", DFR["windup"], tw - .22, S)
    set_frame(dr, "drake", DFR["throw"], tw, S)
    set_frame(dr, "drake", DFR["idle0"], tw + .45, S)
    idle(dr, "drake", tw + .45, b, S)
    hand = (X0 + 29 * S, Y0 + 12 * S)
    floor = 1250
    path = phys(-(floor - hand[1]), -720, vx0=600, g_m=65, bounce=.28, drag=.1, fric=.5, dur=1.2)
    land = next(t_ for t_, x_, y_ in path[1:] if y_ >= -1)
    j = nid("lt")
    PAN.append(f'<img class="el px pxo" id="{j}" src="{PX}lighter.png" style="left:{hand[0] - 20:.0f}px;top:{hand[1] - 72:.0f}px;width:40px;z-index:7" alt="">')
    show(f"#{j}", tw, b)
    x_end = 0
    for (t_, x_, y_) in path:
        js(f'tl.set("#{j}", {{x: {x_:.0f}, y: {y_ + (floor - hand[1]):.0f}, rotation: {min(1, t_ / .55) * 610:.0f}}}, {tw + t_:.3f});')
        x_end = x_
    k_ = nid("ig")
    lx, ly = hand[0] + x_end, floor + 30
    PAN.append(f'<i class="el shock" id="{k_}" style="left:{lx - 160:.0f}px;top:{ly - 60:.0f}px;width:320px;height:120px;z-index:6;border-color:#ffb347"></i>')
    show(f"#{k_}", tw + land, tw + land + .5)
    js(f'tl.fromTo("#{k_}", {{scale: .2, opacity: 1}}, {{scale: 3, opacity: 0, duration: .45, ease: "power2.out", immediateRender: false}}, {tw + land:.3f});')
    CUES.extend([(a, "pixel_walk", .3), (tw - .22, "lighter", 0), (tw, "throw", 0), (tw + land, "ignite", 0),
                 (tw + land + .05, "fire", b - tw - land)])
    js(f'tl.set("#{dr}", {{filter: "drop-shadow(4px 0 0 #f2f1ec) drop-shadow(-4px 0 0 #f2f1ec) drop-shadow(0 4px 0 #f2f1ec) '
       f'drop-shadow(0 -4px 0 #f2f1ec) drop-shadow(0 0 26px rgba(255,120,40,.95)) drop-shadow(0 0 60px rgba(255,60,20,.6))"}}, {tw + land:.3f});')
    return tw + land


PX = "assets/img/pixel/"
SPR = {"drake": (44, 40, 11), "girl": (28, 40, 7), "girl2": (28, 40, 7), "guy": (24, 40, 3)}   # frame counts of the sheets
DFR = {n: k for k, n in enumerate(["idle0", "idle1", "walk0", "walk1", "walk2", "walk3", "aim", "shoot", "drop", "windup", "throw"])}


def sprite(name, x, y, S, extra=""):
    """A sprite-sheet character inside a game screen; frames switch with set_frame()."""
    fw, fh, n = SPR[name]
    i = nid("sp")
    return i, (f'<div class="spr" id="{i}" style="left:{x}px;top:{y}px;width:{fw * S}px;height:{fh * S}px;'
               f'background-image:url({PX}{name}_sheet.png);background-size:{fw * S * n}px {fh * S}px;{extra}"></div>')


def set_frame(i, name, k, t, S):
    js(f'tl.set("#{i}", {{backgroundPosition: "{-k * SPR[name][0] * S}px 0px"}}, {t:.3f});')


def game_box(x, y, w, h, t0, t1, inner, score=None):
    """v15: the pixel scene sits straight on the collage (owner: no box, this is not an explainer). Same inner
    coordinates as the old game screen, so the staging is kept; the sprites carry a white sticker outline."""
    i = nid("gb")
    PAN.append(f'<div class="pxstage el" id="{i}" style="left:{x + 14}px;top:{y + 14}px;width:{w - 28}px;height:{h - 28}px;z-index:5">'
               f'{inner}</div>')
    show(f"#{i}", t0, t1)
    return i


def walk_in(i, x_from, t0, dur, S, frames_to=None):
    js(f'tl.fromTo("#{i}", {{x: {x_from}}}, {{x: 0, duration: {dur:.2f}, ease: "power2.out", immediateRender: false}}, {t0:.3f});')
    k, t = 0, t0
    while t < t0 + dur:
        set_frame(i, "drake", DFR[f"walk{k % 4}"], t, S)
        t, k = t + .075, k + 1
    return t0 + dur


def idle(i, name, t0, t1, S, frames=(0, 1)):
    k, t = 0, t0
    while t < t1:
        set_frame(i, name, frames[k % 2], t, S)
        t, k = t + .25, k + 1


def pixel_shot(a, b, tb):
    """Smoke a n**** top: the live pixel mascot walks in, aims, BANG on the beat with recoil, the guy flashes white
    and drops, then the smoke takes the screen (the smoke layer sits above this game screen)."""
    S, FL = 9, 590
    dr, dhtml = sprite("drake", 60, FL - 38 * S, S)
    gu, ghtml = sprite("guy", 690, FL - 38 * S, S, "transform-origin:108px 342px")
    ids = {k: nid("px") for k in ("fl", "bang", "bul", "st")}
    tipx, tipy = 60 + 37 * S, FL - 38 * S + 12.5 * S
    stars = "".join(f'<i style="left:{20 + 34 * k}px;top:{(k % 2) * 18}px"></i>' for k in range(4))
    inner = (dhtml + ghtml +
             f'<img id="{ids["fl"]}" class="px" src="assets/img/collage/pixel/flash_px.png" style="left:{tipx - 6:.0f}px;top:{tipy - 27:.0f}px;width:54px;opacity:0">'
             f'<img id="{ids["bang"]}" class="px" src="assets/img/collage/pixel/bang_px.png" style="left:360px;top:90px;width:260px;opacity:0">'
             f'<i id="{ids["bul"]}" class="bullet" style="left:{tipx:.0f}px;top:{tipy - 3:.0f}px;opacity:0"></i>'
             f'<div id="{ids["st"]}" class="pxstars" style="left:780px;top:430px;opacity:0">{stars}</div>')
    game_box(60, 110, 960, 660, a, b, inner, score="1UP  SMOKE")
    t_in = walk_in(dr, -360, a + .05, .45, S)
    idle(dr, "drake", t_in, max(t_in, tb - .3), S)
    set_frame(dr, "drake", DFR["aim"], max(t_in, tb - .3), S)
    idle(gu, "guy", a, tb + .07, S)
    js(f'tl.fromTo("#{gu}", {{x: 420}}, {{x: 0, duration: .4, ease: "power2.out", immediateRender: false}}, {a + .1:.3f});')
    set_frame(dr, "drake", DFR["shoot"], tb, S)
    set_frame(dr, "drake", DFR["aim"], tb + 2 / 30, S)
    set_frame(dr, "drake", DFR["shoot"], tb + 4 / 30, S)
    set_frame(dr, "drake", DFR["aim"], tb + 6 / 30, S)
    for k, o in enumerate([1, 1, 0, 0, 1, 0]):
        js(f'tl.set("#{ids["fl"]}", {{opacity: {o}}}, {tb + k / 30:.3f});')
    js(f'tl.set("#{ids["bang"]}", {{opacity: 1}}, {tb:.3f});')
    js(f'tl.fromTo("#{ids["bang"]}", {{scale: 0, rotation: -12}}, {{scale: 1, rotation: 0, duration: .25, ease: "back.out(3)", immediateRender: false}}, {tb:.3f});')
    js(f'tl.set("#{ids["bang"]}", {{opacity: 0}}, {tb + .55:.3f});')
    js(f'tl.set("#{ids["bul"]}", {{opacity: 1}}, {tb:.3f});')
    js(f'tl.fromTo("#{ids["bul"]}", {{x: 0, y: 0, rotation: -6.4}}, {{x: 380, y: -45, rotation: -6.4, duration: .07, ease: "none", immediateRender: false}}, {tb:.3f});')
    js(f'tl.set("#{ids["bul"]}", {{opacity: 0}}, {tb + .08:.3f});')
    for k, fr in enumerate([2, 0, 2, 0, 2]):
        set_frame(gu, "guy", fr, tb + .07 + k / 30, S)
    js(f'tl.to("#{gu}", {{rotation: 84, x: 40, duration: .32, ease: "power2.in"}}, {tb + .24:.3f});')
    js(f'tl.set("#{ids["st"]}", {{opacity: 1}}, {tb + .56:.3f});')
    k, t = 0, tb + .56
    while t < b:
        js(f'tl.set("#{ids["st"]} i", {{y: {(k % 2) * 8 - 4}}}, {t:.3f});')
        t, k = t + .1, k + 1
    FLASH.append((tb, "white"))
    CUES.extend([(a + .05, "pixel_walk", .45), (tb, "pixel_shot", 0), (tb + .07, "pixel_hit", 0), (tb + .58, "pixel_fall", 0)])


def phone_throw(a, b):
    """Jealous (owner): two pixel girls, mad, wind up and fling their phones; the phones arc down with the gravity
    expression and smash on the floor (a white crack burst). Straight on the collage above the keyword."""
    S, FL, X0, Y0 = 8, 470, 60, 250
    tj = next(s_ for w, s_ in words_of(0) if w == "jealous")
    g1, h1 = sprite("girl", 640, FL - 38 * S, S)
    g2, h2 = sprite("girl2", 120, FL - 38 * S, S, "transform:scaleX(-1)")
    ph = [nid("ph"), nid("ph")]
    ck = [nid("ck"), nid("ck")]
    starts = [(640 + 4 * S, FL - 38 * S + 6 * S), (120 + 24 * S, FL - 38 * S + 6 * S)]
    inner = h1 + h2 + "".join(
        f'<img id="{ph[k]}" class="px" src="{PX}phone.png" style="left:{starts[k][0] - 28:.0f}px;top:{starts[k][1] - 44:.0f}px;width:56px;opacity:0">'
        f'<img id="{ck[k]}" class="px" src="{PX}crack.png" style="left:{starts[k][0] - 63:.0f}px;top:{FL - 70:.0f}px;width:126px;opacity:0">' for k in range(2))
    game_box(X0 - 14, Y0 - 14, 988, 560, a, b, inner)
    for gid, name in ((g1, "girl"), (g2, "girl2")):
        idle(gid, name, a, tj + .1, S, frames=(6, 6))
    for k, (gid, name) in enumerate(((g1, "girl"), (g2, "girl2"))):
        tw = tj + .15 + .22 * k
        set_frame(gid, name, 4, tw - .2, S)
        set_frame(gid, name, 5, tw, S)
        set_frame(gid, name, 6, tw + .4, S)
        idle(gid, name, tw + .4, b, S, frames=(6, 6))
        vx = (-420, 420)[k]
        path = phys(-(FL - 30 - starts[k][1]), -520, vx0=vx, g_m=60, bounce=.3, drag=.1, fric=.6, dur=1.0)
        land = next(t_ for t_, x_, y_ in path[1:] if y_ >= -1)
        js(f'tl.set("#{ph[k]}", {{opacity: 1}}, {tw:.3f});')
        for (t_, x_, y_) in path:
            js(f'tl.set("#{ph[k]}", {{x: {x_:.0f}, y: {y_ + FL - 30 - starts[k][1]:.0f}, rotation: {min(1, t_ / .5) * (-540, 540)[k]:.0f}}}, {tw + t_:.3f});')
        xl = path[-1][1]
        js(f'tl.set("#{ck[k]}", {{x: {xl:.0f}, opacity: 1}}, {tw + land:.3f});')
        js(f'tl.fromTo("#{ck[k]}", {{scale: .3}}, {{scale: 1.2, duration: .2, ease: "back.out(2)", immediateRender: false}}, {tw + land:.3f});')
        js(f'tl.to("#{ck[k]}", {{opacity: 0, duration: .3}}, {tw + land + .5:.3f});')
        CUES.extend([(tw, "phone_throw", 0), (tw + land, "phone_smash", 0)])


def diamond_drop(a, b):
    """Somethin' gettin' dropped for you, baby girl: the mascot walks up to the pixel girl and drops a handful of
    diamonds at her feet (they bounce with the owner's gravity expression and twinkle), she cheers, hearts float up,
    the counter ticks."""
    S, FL = 9, 570
    td = next(s_ for w, s_ in words_of(12) if w == "dropped")
    tf = next((s_ for w, s_ in words_of(12) if w == "for"), td + .45)
    tg = next((s_ for w, s_ in words_of(12) if w == "baby"), tf + .5)
    dr, dhtml = sprite("drake", 110, FL - 38 * S, S)
    gi, ghtml = sprite("girl", 610, FL - 38 * S, S)
    hx, hy = 110 + 30 * S, FL - 38 * S + 22 * S
    g = random.Random(12)
    dia, sp = [], []
    for k in range(8):
        dia.append(nid("dm"))
        sp.append(nid("sk"))
    inner = dhtml + ghtml + "".join(
        f'<img id="{dia[k]}" class="px" src="{PX}diamond.png" style="left:{hx - 36:.0f}px;top:{hy - 24:.0f}px;width:72px;opacity:0">'
        f'<img id="{sp[k]}" class="px" src="{PX}sparkle.png" style="left:{hx - 10:.0f}px;top:{hy - 30:.0f}px;width:30px;opacity:0">' for k in range(8))
    hearts = [nid("ht") for _ in range(5)]
    inner += "".join(f'<img id="{h}" class="px" src="{PX}heart.png" style="left:{700 + 30 * (k % 3) - 30:.0f}px;top:{FL - 38 * S - 20:.0f}px;width:70px;opacity:0">'
                     for k, h in enumerate(hearts))
    game_box(100, 480, 880, 640, a, b, inner, score="1UP  ICE")
    t_in = walk_in(dr, -380, a + .1, .5, S)
    idle(dr, "drake", t_in, td - .2, S)
    idle(gi, "girl", a, tf, S)
    set_frame(dr, "drake", DFR["drop"], td - .2, S)
    rest_y = FL - 64 - (hy - 24)
    for k in range(8):
        t0 = td + .045 * k + (.5 if k >= 5 else 0)
        path = phys(-rest_y - 10, -260 - 40 * (k % 3), vx0=150 + 32 * k, g_m=42, bounce=.45, drag=.1, fric=.35, dur=1.2)
        js(f'tl.set("#{dia[k]}", {{opacity: 1}}, {t0:.3f});')
        for (dt, px_, py_) in path:
            js(f'tl.set("#{dia[k]}", {{x: {px_:.0f}, y: {py_ + rest_y:.0f}, rotation: {(1 - min(1, dt / .6)) * 90 * (1 if k % 2 else -1):.0f}}}, {t0 + dt:.3f});')
        land = t0 + path[-1][0]
        xe = path[-1][1]
        js(f'tl.set("#{sp[k]}", {{x: {xe + 20:.0f}, y: {rest_y - 4:.0f}}}, {land:.3f});')
        tt, m = land, 0
        while tt < b:
            js(f'tl.set("#{sp[k]}", {{opacity: {(1, 0, .6, 0)[m % 4]}, scale: {(1.2, .6, 1, .6)[m % 4]}}}, {tt:.3f});')
            tt, m = tt + .12 + .02 * (k % 3), m + 1
        CUES.append((land, "diamond", 0))
    set_frame(dr, "drake", DFR["idle0"], td + .7, S)
    idle(dr, "drake", td + .7, b, S)
    idle(gi, "girl", tf, b, S, frames=(2, 3))
    for k, h in enumerate(hearts):
        th = (tf if k < 3 else tg) + .12 * (k % 3)
        js(f'tl.set("#{h}", {{opacity: 1}}, {th:.3f});')
        js(f'tl.fromTo("#{h}", {{y: 0, x: 0, scale: .4}}, {{y: -260, x: {(k % 3 - 1) * 60}, scale: 1.1, duration: .9, ease: "power2.out", immediateRender: false}}, {th:.3f});')
        js(f'tl.to("#{h}", {{opacity: 0, duration: .2}}, {th + .7:.3f});')
        CUES.append((th, "heart", 0))
    CUES.extend([(a + .1, "pixel_walk", .5), (td - .2, "pixel_hold", 0)])


def context_fx():
    """The lyric lines that say something physical happen to the whole screen: smoke fills it, burn sets it on fire,
    dropped drops the frame, comin' out my body lifts a ghost of the whole picture out of itself."""
    sc = {li: (a, b) for a, b, li in scenes()}
    # smoke a top: smoke billows up from the bottom and swallows the whole frame, swirling until the cut
    a, b = sc[13]
    tb = next(s_ for w, s_ in words_of(13) if w not in ("smoke", "a"))      # the bang lands on the third word
    ts = next((s_ for w, s_ in words_of(13) if w == "top"), tb + .45)
    front_layer("smg", "smk2", ts, b, 1400, -700, ts + 1.1, 1100, (140, -520), z=4)
    CUES.append((ts, "smoke", min(2.4, b - ts)))
    pixel_shot(a, b, tb)
    # burn somebody block: a fire front sweeps up the whole screen and leaves it charred, embers flying
    diamond_drop(*sc[12])
    phone_throw(*sc[0])
    a, b = sc[14]
    tl_ = lighter_throw(a, b)
    g = random.Random(14)
    em = "".join(f'<i class="ember" style="position:absolute;left:{g.uniform(0, 1080):.0f}px;top:{g.uniform(700, 1250):.0f}px;'
                 f'width:{g.uniform(7, 16):.0f}px;height:{g.uniform(7, 16):.0f}px"></i>' for _ in range(36))
    bi = front_layer("fig", "firef", tl_, b, 1350, -520, b - .12, 900, (0, -620), z=4, extra=f'<div class="embers">{em}</div>')
    n = max(2, round((b - tl_) * 15))
    js(f'tl.fromTo("#{bi} .ember", {{y: 0, x: 0}}, {{y: (k) => -700 - (k * 137) % 600, x: (k) => (k * 53) % 160 - 80, duration: {b - tl_:.2f}, ease: "steps({n})", '
       f'stagger: .012, immediateRender: false}}, {tl_:.3f});')
    SCREEN.append('<div id="heat"></div>')
    HIDE.append("#heat")
    js(f'tl.set("#heat", {{opacity: .35, background: "#ffb070"}}, {tl_:.3f});')                  # the ignition flash
    js(f'tl.set("#heat", {{background: "radial-gradient(ellipse 90% 70% at 50% 100%, rgba(255,150,60,.55), rgba(255,110,40,.12) 50%, rgba(0,0,0,0) 85%)"}}, {tl_ + STEP:.3f});')
    for k in range(1, n):
        t = tl_ + k * STEP
        js(f'tl.set("#heat", {{opacity: {.1 + .12 * abs(math.sin(k * 2.3)) * abs(math.sin(k * .7 + 1)):.2f}}}, {t:.3f});')
    for tw in [s_ for w, s_ in words_of(14) if w == "burn"]:   # one bloom hit, not a constant wash
        for k, sd in enumerate([18, 11]):
            js(f'tl.set("#glow", {{filter: "url(#bloom)"}}, {tw + k * STEP + .002:.3f});')
            js(f'tl.set("#blg", {{attr: {{stdDeviation: {sd}}}}}, {tw + k * STEP + .002:.3f});')
        js(f'tl.set("#glow", {{filter: "url(#dglow)"}}, {tw + 2 * STEP + .002:.3f});')
    js(f'tl.set("#heat", {{opacity: 0}}, {b:.3f});')
    # somethin' gettin' dropped: the whole frame falls out the bottom, slams back in from the top and judders
    a, b = sc[12]
    td = next(s_ for w, s_ in words_of(12) if w == "dropped")
    for k, dx in enumerate([22, 26, 16, 8]):
        js(f'tl.set("#glow", {{filter: "url(#rgbsplit)"}}, {td + k * STEP:.3f});')
        js(f'tl.set("#rgbR", {{attr: {{dx: 0, dy: {dx}}}}}, {td + k * STEP:.3f});')
        js(f'tl.set("#rgbB", {{attr: {{dx: 0, dy: {-dx}}}}}, {td + k * STEP:.3f});')
    js(f'tl.set("#glow", {{filter: "url(#dglow)"}}, {td + 4 * STEP:.3f});')
    js(f'tl.set("#rgbR", {{attr: {{dy: 0}}}}, {td + 4 * STEP:.3f});')
    js(f'tl.set("#rgbB", {{attr: {{dy: 0}}}}, {td + 4 * STEP:.3f});')
    FLASH.append((td + 3 * STEP, "white"))
    CUES.append((td + 3 * STEP, "boom", 0))
    # comin' out my body: a ghost of the whole picture lifts up out of it on "out", again on "body"
    a, b = sc[16]
    for tw in [s_ for w, s_ in words_of(16) if w in ("out", "body")]:
        CUES.append((tw, "ghost", .4))
        m = 12
        for k in range(m + 1):
            u = k / m
            t = tw + k * STEP
            d = 260 * u ** .7
            al = .6 * (1 - u)
            js(f'tl.set("#fx", {{filter: "url(#ghostf)"}}, {t:.3f});')
            js(f'tl.set("#gho1", {{attr: {{dy: {-d:.0f}, dx: {8 * math.sin(k):.0f}}}}}, {t:.3f});')
            js(f'tl.set("#gho2", {{attr: {{dy: {-d * 1.9:.0f}, dx: {-10 * math.sin(k):.0f}}}}}, {t:.3f});')
            js(f'tl.set("#ghc1", {{attr: {{values: "0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 {al:.2f} 0"}}}}, {t:.3f});')
            js(f'tl.set("#ghc2", {{attr: {{values: "0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 {al * .55:.2f} 0"}}}}, {t:.3f});')
        js(f'tl.set("#fx", {{filter: "none"}}, {tw + (m + 1) * STEP:.3f});')


BURNS = {11: "burn5", 15: "burn12", 17: "burn5", 18: "burn12", 6: "burn1", 10: "burn2"}


def film_burns():
    for a, b, li in scenes():
        if li not in BURNS:
            continue
        name = BURNS[li]
        src = f"assets/video/burn/{name}.mp4"
        d = {"burn1": .96, "burn2": .84, "burn5": .92, "burn12": .88}[name]
        t0 = max(0, a - d * .45)
        i = nid("fb")
        VTR[0] += 1
        SCREEN.append(f'<div class="burnv el" id="{i}"><video id="v{i}" src="{src}" data-start="{t0:.3f}" data-duration="{d:.3f}" '
                      f'data-track-index="{VTR[0]}" muted playsinline></video></div>')
        show(f"#{i}", t0, t0 + d)


def tables(rows):
    return "".join(f'<feFunc{c} type="table" tableValues="{" ".join(f"{v:g}" for v in vals)}"/>' for c, vals in zip("RGBA", rows))


FIRE_T = tables([[.69] * 9 + [.69, 1, 1, .95, .55, .22, .12, .08, .07, .06, .06, .06],
                 [.10] * 9 + [.10, .9, .62, .3, .1, .05, .035, .03, .025, .02, .02, .02],
                 [.31] * 9 + [.31, .55, .15, .06, .06, .05, .04, .035, .03, .03, .03, .03],
                 [0] * 8 + [0, .55, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
SMOKE_T = tables([[.96] * 9 + [.96, .94, .9, .78, .66, .74, .88, .96, .86, .72, .8, .92],
                  [.86] * 9 + [.86, .84, .79, .64, .52, .6, .76, .86, .74, .58, .66, .82],
                  [.9] * 9 + [.9, .88, .84, .7, .58, .66, .8, .9, .79, .64, .72, .86],
                  [0] * 8 + [.08, .25, .45, .62, .55, .5, .66, .82, .9, .84, .72, .8, .9]])
FX_DEFS = f"""
      <filter id="inkf" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB">
      <feTurbulence id="inkT" type="fractalNoise" baseFrequency="0.012 0.018" numOctaves="4" seed="1" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.4 0 0 0 0" result="na"/>
      <feComponentTransfer in="na" result="m"><feFuncA id="inkA" type="linear" slope="9" intercept="1.2"/></feComponentTransfer>
      <feComposite in="SourceGraphic" in2="m" operator="in"/></filter>
      <filter id="dglow" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  .3 .59 .11 0 0" result="lum"/>
      <feComponentTransfer in="lum" result="mask"><feFuncA type="linear" slope="3.2" intercept="-2.3"/></feComponentTransfer>
      <feComposite in="SourceGraphic" in2="mask" operator="in" result="hi"/>
      <feGaussianBlur in="hi" stdDeviation="4" result="b1"/><feGaussianBlur in="hi" stdDeviation="14" result="b2"/>
      <feGaussianBlur in="hi" stdDeviation="38" result="b3"/>
      <feComposite in="b1" in2="b2" operator="arithmetic" k2="0.55" k3="0.45" result="m1"/>
      <feComposite in="m1" in2="b3" operator="arithmetic" k2="1" k3="0.35" result="gl"/>
      <feBlend in="SourceGraphic" in2="gl" mode="screen"/></filter>
      <filter id="firef" filterUnits="objectBoundingBox" x="0" y="0" width="1" height="1.6" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.010 0.004" numOctaves="4" seed="11" result="n0"/>
      <feOffset id="fireo" in="n0" dx="0" dy="0" result="n1"/>
      <feColorMatrix in="n1" type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" result="n"/>
      <feComposite in="SourceGraphic" in2="n" operator="arithmetic" k1="0" k2="0.6" k3="0.4" k4="0" result="v"/>
      <feComponentTransfer in="v" result="c">{FIRE_T}</feComponentTransfer>
      <feComposite in="c" in2="SourceAlpha" operator="in"/></filter>
      <filter id="smk2" filterUnits="objectBoundingBox" x="-0.2" y="0" width="1.4" height="1.6" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.005 0.006" numOctaves="5" seed="3" result="n0"/>
      <feOffset id="smko" in="n0" dx="0" dy="0" result="n1"/>
      <feColorMatrix in="n1" type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" result="n"/>
      <feComposite in="SourceGraphic" in2="n" operator="arithmetic" k1="0" k2="0.6" k3="0.4" k4="0" result="v"/>
      <feComponentTransfer in="v" result="c">{SMOKE_T}</feComponentTransfer>
      <feGaussianBlur in="c" stdDeviation="2" result="cb"/>
      <feComposite in="cb" in2="SourceAlpha" operator="in"/></filter>
      <filter id="ghostf" x="-5%" y="-60%" width="110%" height="170%" color-interpolation-filters="sRGB">
      <feOffset id="gho1" in="SourceGraphic" dx="0" dy="0" result="o1"/>
      <feColorMatrix id="ghc1" in="o1" type="matrix" values="0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 0 0" result="c1"/>
      <feGaussianBlur in="c1" stdDeviation="3" result="g1"/>
      <feOffset id="gho2" in="SourceGraphic" dx="0" dy="0" result="o2"/>
      <feColorMatrix id="ghc2" in="o2" type="matrix" values="0.7 0 0 0 0.25  0 0.6 0 0 0.2  0 0 0.7 0 0.3  0 0 0 0 0" result="c2"/>
      <feGaussianBlur in="c2" stdDeviation="9" result="g2"/>
      <feBlend in="g2" in2="SourceGraphic" mode="screen" result="s1"/><feBlend in="g1" in2="s1" mode="screen"/></filter>"""


# The lively gradient behind the collage (screen space, under the moving paper): big soft colour blobs drifting on
# slow loops, a little brighter on every beat. (x, y, radius, colour, drift x, drift y, period s, phase)
BLOBS = [(300, 300, 480, "#b0194f", 260, 180, 9.0, 0.0), (1100, 380, 400, "#e0336f", -240, 220, 11.0, 1.7),
         (700, 1150, 620, "#2e0818", 200, -260, 13.0, 3.1), (200, 1100, 440, "#5a1660", 220, -160, 10.0, 4.4),
         (1150, 1200, 460, "#8c1442", -260, -200, 12.0, 2.2), (740, 640, 300, "#ff5c8a", 180, 160, 7.5, 5.0)]


def background():
    js('tl.set("#bg", {filter: "saturate(1.1)"}, 0);')     # v16: no beat throb


def flicker_hits():
    """Keyword flicker (the Sapphire S_Flicker hits in the owner's reel project): a quick white flicker over the
    frame when each line's keyword lands."""
    for a, b, li in scenes():
        if li < 0:
            continue
        for txt, key, t in groups_of(li):
            if key:
                for k, o in enumerate([.42, 0, .26, 0, .12, 0]):
                    js(f'tl.set("#flash", {{opacity: {o}}}, {t + k / 30:.3f});')
                CUES.append((t, "keyword", 0))


def sound_cues():
    """Every cut, flash and element moment for the sound design -> plan/sfx_events.json (read by the real-sfx skill)."""
    big = {11, 15, 17, 18, 6, 10}                           # section changes with a film burn
    for si, (a, b, li) in enumerate(scenes()):
        if si:
            CUES.append((a, "whoosh_big" if li in big else ("whoosh" if si % 2 else "swish"), .35))
    for t, kind in FLASH:
        CUES.append((t, {"invert": "glitch", "white": "hit", "split": "glitch"}[kind], 0))
    ev = sorted(({"t": round(t, 3), "type": k} | ({"len": round(d, 2)} if d else {}) for t, k, d in CUES), key=lambda e: e["t"])
    json.dump(ev, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    return ev


def flashes():
    SCREEN.append('<div id="flash"></div><div id="split"><i></i></div>')
    HIDE.extend(["#flash", "#split"])
    for t, kind in FLASH:
        if kind == "invert":
            js(f'tl.set("#fx", {{filter: "invert(1)"}}, {t:.3f});')
            js(f'tl.set("#fx", {{filter: "none"}}, {t + STEP:.3f});')
        elif kind == "white":
            js(f'tl.set("#flash", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#flash", {{opacity: 0}}, {t + STEP:.3f});')
        elif kind == "split":
            js(f'tl.set("#split", {{opacity: 1}}, {t:.3f});')
            js(f'tl.set("#split", {{opacity: 0}}, {t + STEP:.3f});')


SP = "url(assets/img/collage/tex/speckle.png) 0 0 / 300px auto"
GR = "url(assets/img/collage/tex/grunge.png)"
CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Archivo Black"; src: url("assets/fonts/ArchivoBlack.ttf"); }}
@font-face {{ font-family: "Playfair"; src: url("assets/fonts/PlayfairDisplay-BoldItalic.woff2"); font-style: italic; font-weight: 800; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: {INK}; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: {INK}; }}
#fx {{ position: absolute; inset: 0; }}
#cam {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; transform-origin: 540px {CY}px; }}
#pan {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {FH}px; }}
#bg {{ position: absolute; inset: -200px; overflow: hidden; background: radial-gradient(ellipse at 50% 50%, #2a0818, #0c0408 75%); }}
.blob {{ position: absolute; display: block; border-radius: 50%; mix-blend-mode: screen; filter: blur(60px); opacity: .62; }}
{"".join(f'#bl{k} {{ left: {x}px; top: {y}px; width: {r * 2}px; height: {r * 2}px; margin: -{r}px 0 0 -{r}px; background: radial-gradient(circle, {c} 0%, {c}aa 35%, rgba(0,0,0,0) 70%); }}' for k, (x, y, r, c, *_) in enumerate(BLOBS))}
#paper {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; background: url(assets/img/collage/shade.png); opacity: .85; }}
#grid {{ position: absolute; left: -760px; top: -1000px; width: 2600px; height: 3900px; pointer-events: none; opacity: .3; }}
#grid line {{ stroke: {WHT}; stroke-width: 1.6; }}
#board {{ position: absolute; inset: 0; }}
#blinds {{ position: absolute; left: -1100px; top: -1300px; width: 3300px; height: 4500px; z-index: 9; pointer-events: none; mix-blend-mode: multiply;
  background: repeating-linear-gradient(-32deg, rgba(20,6,12,0) 0px, rgba(20,6,12,0) 70px, rgba(20,6,12,.38) 150px, rgba(20,6,12,.42) 210px,
  rgba(20,6,12,0) 290px, rgba(20,6,12,0) 330px); }}
.el {{ position: absolute; opacity: 0; }}
img.el {{ display: block; height: auto; }}
.g3b video {{ width: 100%; height: 100%; display: block; }}
.print {{ position: absolute; background: {WHT}; padding: 16px; box-shadow: 0 14px 26px rgba(0,0,0,.5); z-index: 2; }}
.print img, .print video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.print i {{ position: absolute; inset: 16px; background: {MAG}; mix-blend-mode: multiply; }}
.lw {{ position: absolute; transform-origin: 50% 50%; }}
.lb {{ position: relative; display: inline-block; font: 400 120px/1.12 "Anton"; white-space: nowrap; opacity: 0; padding: .04em .28em 0;
  letter-spacing: .01em; }}
.lb .ch {{ display: inline-block; white-space: pre; }}
.ser {{ background: none; color: #fff4f7; padding: 0 .12em; font-family: "Playfair"; font-style: italic; font-weight: 800; letter-spacing: 0; line-height: 1.15;
  text-shadow: 0 2px 12px rgba(10,2,6,.75), 0 0 16px rgba(255,140,180,.8), 0 0 38px rgba(255,60,120,.5), 4px 6px 0 rgba(20,6,12,.6); }}
.smear {{ position: absolute; left: 0; top: 0; width: 1.3em; height: 100%; opacity: 0; pointer-events: none; mix-blend-mode: screen; filter: blur(12px);
  background: radial-gradient(ellipse at 50% 50%, rgba(255,214,170,.95), rgba(255,90,140,.7) 40%, rgba(0,0,0,0) 72%); }}
.lb .cz {{ filter: blur(.08em); }}
.lb .cur {{ display: inline-block; width: .42em; height: .78em; margin-left: .06em; vertical-align: -.02em; background: rgba(160,150,150,.9); }}
.blk {{ background: {SP}, {INK}; color: {WHT}; box-shadow: 0 12px 22px rgba(0,0,0,.4); }}
.wht {{ background: {SP}, {WHT}; color: {INK}; box-shadow: 0 12px 22px rgba(0,0,0,.35); }}
.magw {{ background: {SP}, {WHT}; color: {MAG}; box-shadow: 0 12px 22px rgba(0,0,0,.35); }}
.magw .cur {{ background: {MAG}; }}
.mag {{ background: {SP}, {MAG}; color: #fff; box-shadow: 0 12px 22px rgba(0,0,0,.35); }}
.mb {{ background: {MAG}; color: #fff; text-shadow: 4px 4px 0 {INK}; box-shadow: 18px 16px 0 {INK}; }}
.blkm {{ background: {INK}; color: #fff; box-shadow: 16px 18px 0 {MAG}; }}
.mtyp {{ background: none; color: {MAG}; padding: 0; -webkit-mask-image: {GR}; mask-image: {GR}; }}
.stamp {{ background: none; color: {WHT}; padding: 0; line-height: 1.08;
  -webkit-mask-image: {GR}; mask-image: {GR}; -webkit-mask-size: 520px auto; mask-size: 520px auto; }}
.stamp .cur {{ background: rgba(240,236,236,.55); }}
.w3d {{ background: none; color: {WHT}; padding: 0; -webkit-text-stroke: 2px #2a2a2a;
  text-shadow: {", ".join(f"{k}px {k}px 0 rgb({int(214 - 13 * k)},{int(208 - 13.5 * k)},{int(200 - 13.5 * k)})" for k in range(1, 13))}, 14px 18px 18px rgba(0,0,0,.55), 0 0 30px rgba(255,255,255,.18); }}
.m3d {{ background: none; color: {MAG}; padding: 0; -webkit-text-stroke: 2px #5c0a28;
  text-shadow: {", ".join(f"{k}px {k}px 0 rgb({int(160 - 11 * k)},{int(22 - 1.4 * k)},{int(70 - 4.6 * k)})" for k in range(1, 13))}, 14px 18px 18px rgba(0,0,0,.5), 0 0 30px rgba(255,80,140,.25); }}
.mlet {{ background: none; color: {MAG}; padding: 0; text-shadow: 5px 5px 0 rgba(10,10,10,.85);
  -webkit-mask-image: {GR}; mask-image: {GR}; -webkit-mask-size: 700px auto; mask-size: 700px auto; }}
.fill {{ color: transparent; padding: 0; line-height: 1.1; background-size: cover; background-position: 50% 40%;
  -webkit-background-clip: text; background-clip: text; -webkit-text-stroke: 5px {WHT}; filter: drop-shadow(8px 10px 0 rgba(10,10,10,.85)); }}
{"".join(f'.f{li} {{ background-image: url({src}); }}' for li, src in FILL.items())}
.ghost {{ font: 400 250px/1.15 "Anton"; color: rgba(242,241,236,.12); white-space: nowrap; opacity: 0; }}
.para {{ font: 400 38px/1.3 "Archivo Black"; color: {WHT}; z-index: 5; }}
.itag {{ position: absolute; left: 50%; top: 212px; transform: translateX(-50%) rotate(-3deg); font: 400 50px/1.2 "Anton"; white-space: nowrap;
  background: {MAG}; color: #fff; padding: 0 .3em; box-shadow: 0 8px 14px rgba(0,0,0,.35); }}
.rline {{ border: 9px solid {WHT}; z-index: 2; }}
.magblk {{ z-index: 2; background: repeating-linear-gradient(90deg, rgba(0,0,0,.25) 0 3px, rgba(0,0,0,0) 3px 9px),
  radial-gradient(ellipse at 40% 40%, #c21d57, #3d0a1b); }}
.circ {{ position: absolute; left: -10%; top: -22%; width: 120%; height: 144%; overflow: visible; pointer-events: none; }}
.circ path {{ fill: none; stroke: {WHT}; stroke-width: 5.5; stroke-linecap: round; vector-effect: non-scaling-stroke; stroke-dasharray: 400; }}
.tframe {{ position: absolute; z-index: 15; opacity: 0; background: {WHT}; padding: 18px; box-shadow: 0 18px 40px rgba(0,0,0,.55); }}
.tframe img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#flash {{ position: absolute; inset: 0; z-index: 20; background: {WHT}; opacity: 0; }}
#split {{ position: absolute; inset: 0; z-index: 20; background: {MAG}; opacity: 0; }}
#split i {{ position: absolute; left: 50%; top: 0; width: 50%; height: 100%; background: {INK}; }}
#glow {{ position: absolute; inset: 0; filter: url(#dglow); }}
#fluid {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }}
.burnv {{ position: absolute; inset: 0; z-index: 16; mix-blend-mode: screen; pointer-events: none; }}
.burnv video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#leak {{ position: absolute; inset: -200px; z-index: 17; opacity: 0; pointer-events: none; mix-blend-mode: screen;
  background: radial-gradient(ellipse 35% 60% at 50% 50%, rgba(255,170,120,.85), rgba(255,60,140,.5) 45%, rgba(0,0,0,0) 75%); }}
.counter {{ font: 400 300px/1 "Anton"; color: {WHT}; -webkit-text-stroke: 6px {INK}; paint-order: stroke fill; text-shadow: 14px 14px 0 {MAG}; }}
.shock {{ border-radius: 50%; border: 10px solid {WHT}; box-shadow: 0 0 30px 6px rgba(255,140,190,.8); }}
.ring {{ border-radius: 50%; border: 12px solid {MAG}; box-shadow: 0 0 34px 8px rgba(255,90,150,.7); }}
.ember {{ border-radius: 50%; background: #ffb36b; box-shadow: 0 0 12px 5px #ff4f7a; }}
.wisp {{ border-radius: 50%; background: radial-gradient(ellipse, rgba(255,230,240,.9), rgba(255,120,170,.4) 50%, rgba(0,0,0,0) 72%); filter: blur(6px); }}
.lock {{ left: 0; top: 0; width: {FW}px; height: {FH}px; transform-origin: 540px 540px; pointer-events: none; }}
.embers {{ position: absolute; inset: 0; }}
#heat {{ position: absolute; inset: 0; z-index: 16; opacity: 0; pointer-events: none; mix-blend-mode: screen; }}
.vf {{ position: absolute; inset: 34px; pointer-events: none; font: 400 22px/1 "Archivo Black"; color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,.7); }}
.vf b {{ position: absolute; width: 44px; height: 44px; border: 0 solid rgba(255,255,255,.92); }}
.vf .c1 {{ left: 0; top: 0; border-width: 5px 0 0 5px; }} .vf .c2 {{ right: 0; top: 0; border-width: 5px 5px 0 0; }}
.vf .c3 {{ left: 0; bottom: 0; border-width: 0 0 5px 5px; }} .vf .c4 {{ right: 0; bottom: 0; border-width: 0 5px 5px 0; }}
.vf .rec {{ position: absolute; left: 60px; top: 14px; letter-spacing: .06em; }}
.vf .rec i {{ display: inline-block; width: 16px; height: 16px; border-radius: 50%; background: #ff2b4f; margin-right: 10px; box-shadow: 0 0 12px #ff2b4f; }}
.vf .tc {{ position: absolute; right: 60px; bottom: 14px; font-size: 18px; letter-spacing: .08em; }}
.vf .pf {{ position: absolute; width: 230px; height: 230px; margin: -115px 0 0 -115px; opacity: 0; mix-blend-mode: screen;
  background: radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(255,240,250,.7) 18%, rgba(255,200,230,.15) 45%, rgba(0,0,0,0) 70%); }}
.pscreen {{ position: absolute; left: 292px; top: 82px; width: 250px; height: 548px; transform: rotate(9.3deg); border-radius: 30px; overflow: hidden;
  background: linear-gradient(180deg, #1d1620, #0b090d 70%); color: #fff; font-family: "Archivo Black"; text-align: center; }}
.ps-glow {{ position: absolute; left: -40%; top: -10%; width: 180%; height: 60%; background: radial-gradient(ellipse, rgba(176,25,79,.55), rgba(0,0,0,0) 65%); }}
.ps-top {{ position: absolute; left: 0; right: 0; top: 54px; font-size: 18px; color: #c9c0c6; letter-spacing: .06em; }}
.ps-av {{ position: absolute; left: 70px; top: 120px; width: 110px; height: 110px; border-radius: 50%; border: 4px solid rgba(255,255,255,.5);
  background: linear-gradient(135deg, #b0194f, #5f1b30); }}
.ps-av span {{ position: absolute; left: 0; right: 0; top: 18px; font-size: 56px; }}
.ps-av .ring {{ position: absolute; inset: -6px; border-radius: 50%; border: 3px solid rgba(255,140,190,.9); }}
.ps-name {{ position: absolute; left: 0; right: 0; top: 258px; font-size: 44px; line-height: 1; }}
.ps-sub {{ position: absolute; left: 0; right: 0; top: 318px; font-size: 16px; line-height: 1; color: #b9aeb5; }}
.ps-btns {{ position: absolute; left: 0; right: 0; bottom: 56px; display: flex; justify-content: space-around; padding: 0 22px; }}
.ps-btns i {{ width: 54px; height: 54px; border-radius: 50%; background: rgba(255,255,255,.18); }}
.ps-btns .end {{ background: #ff3b46; box-shadow: 0 0 18px rgba(255,59,70,.7); }}
.gbox {{ background: #141213; padding: 14px; border-radius: 26px; box-shadow: 0 0 0 6px {WHT}, 0 0 0 12px {MAG}, 0 24px 40px rgba(0,0,0,.55); }}
.gscr {{ position: absolute; inset: 14px; overflow: hidden; border-radius: 14px;
  background: radial-gradient(ellipse at 50% 30%, #3a1430, #160810 75%); }}
.gscan {{ position: absolute; inset: 0; pointer-events: none; opacity: .35;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,.55) 0 3px, rgba(0,0,0,0) 3px 7px); }}
.gfloor {{ position: absolute; left: 0; right: 0; bottom: 0; height: 64px; image-rendering: pixelated;
  background: repeating-linear-gradient(90deg, #5f1b30 0 28px, #3b0f1f 28px 56px); border-top: 7px solid #f2f1ec; }}
.gscore {{ position: absolute; left: 22px; top: 16px; font: 400 26px/1 "Archivo Black"; color: #ffd640; letter-spacing: .12em;
  text-shadow: 3px 3px 0 #141213; }}
.gcount {{ position: absolute; right: 26px; top: 14px; font: 400 34px/1 "Archivo Black"; color: #bfefff; text-shadow: 3px 3px 0 #141213; }}
.spr {{ position: absolute; image-rendering: pixelated; background-repeat: no-repeat; background-position: 0 0;
  filter: drop-shadow(4px 0 0 #f2f1ec) drop-shadow(-4px 0 0 #f2f1ec) drop-shadow(0 4px 0 #f2f1ec) drop-shadow(0 -4px 0 #f2f1ec)
  drop-shadow(10px 14px 0 rgba(20,6,12,.45)); }}
.pxstage {{ overflow: visible; }}
.pxone {{ position: absolute; width: 0; height: 0; overflow: visible; }}
.pxstage .px, .pxo {{ filter: drop-shadow(3px 0 0 #f2f1ec) drop-shadow(-3px 0 0 #f2f1ec) drop-shadow(0 3px 0 #f2f1ec) drop-shadow(0 -3px 0 #f2f1ec); }}
.pxw {{ position: absolute; inset: 0; }}
.px {{ position: absolute; image-rendering: pixelated; display: block; height: auto; }}
.bullet {{ position: absolute; width: 46px; height: 7px; background: #ffd640; box-shadow: 0 0 10px #ffb000; }}
.pxstars {{ position: absolute; width: 170px; height: 40px; }}
.pxstars i {{ position: absolute; width: 14px; height: 14px; background: #ffd640; box-shadow: 0 0 0 4px #141213; }}
.pxground {{ position: absolute; left: 0; right: 0; top: 508px; height: 12px; background: repeating-linear-gradient(90deg, #f2f1ec 0 24px, #b0194f 24px 48px);
  image-rendering: pixelated; opacity: .9; }}
.foot {{ position: absolute; inset: 0; z-index: 15; background: #000; overflow: hidden; }}
.foot video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }}
.fred {{ position: absolute; inset: 0; background: #ff1e2e; mix-blend-mode: multiply; opacity: 0; }}
.fdbl {{ position: absolute; left: -210px; top: -1000px; width: 1500px; mix-blend-mode: screen; opacity: .45; filter: grayscale(1) contrast(1.4); }}
.fst {{ position: absolute; top: 0; width: 6px; height: 1080px; background: #fff; opacity: 0; box-shadow: 0 0 14px #fff; }}
.fcap-line {{ position: absolute; left: 60px; right: 60px; top: 900px; z-index: 16; text-align: center; font: italic 800 46px/1.1 "Playfair";
  letter-spacing: .06em; text-transform: uppercase; color: #ff2a3c; text-shadow: 0 0 18px rgba(255,30,50,.65), 0 3px 10px rgba(0,0,0,.8); }}
.fkey-line {{ position: absolute; left: 0; right: 0; top: 430px; z-index: 16; text-align: center; font: 400 190px/1 "Anton"; color: #fff;
  letter-spacing: .01em; text-shadow: 0 0 30px rgba(255,40,60,.7), 8px 8px 0 #ff1e2e; }}
.fw {{ margin: 0 .16em; }}
.fw.cz {{ filter: blur(.1em); }}
#ink {{ position: absolute; inset: 0; width: 1080px; height: 1080px; z-index: 19; opacity: 0; pointer-events: none; }}
.tear {{ position: absolute; left: 0; top: -300px; width: 1900px; height: auto; z-index: 19; opacity: 0; pointer-events: none;
  filter: drop-shadow(0 20px 30px rgba(0,0,0,.55)); }}
.tframe.thr img {{ filter: grayscale(1) contrast(5) brightness(1.1); }}
.tframe.duo img {{ filter: invert(1) sepia(1) saturate(4) hue-rotate(130deg) contrast(1.4); }}
#vig {{ position: absolute; inset: 0; z-index: 18; pointer-events: none; background: radial-gradient(ellipse 80% 75% at 50% 48%, rgba(0,0,0,0) 55%, rgba(0,0,0,.4) 100%); }}
#grain {{ position: absolute; left: 0; top: 0; width: 1120px; height: 1120px; z-index: 18; pointer-events: none; opacity: .08; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
"""


def main():
    builders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6, "R7": r7, "R8": r8, "R9": r9}
    for si, (a, b, li) in enumerate(scenes()):
        gs = [("SPIN BOUT U", False, .3), ("DRAKE", True, 1.1), ("21 SAVAGE", False, 1.6)] if li < 0 else groups_of(li)
        if li in FOOT:
            footage_scene(si, a, b, li, gs)
        else:
            builders[RECIPE[li]](si, a, b, li, gs)
    lyric_icons()
    cut_bursts()
    concepts()
    camera()
    background()
    finishing()
    context_fx()
    film_burns()
    pin_locks()
    flashes()
    ev = sound_cues()
    g = random.Random(3)
    for f in range(int(DUR * 15)):
        js(f'tl.set("#grain", {{x: {g.randint(-40, 0)}, y: {g.randint(-40, 0)}}}, {f / 15:.3f});')
    gl = random.Random(4)
    grid = "".join(f'<line x1="{x + gl.uniform(-8, 8):.0f}" y1="-20" x2="{x + gl.uniform(-40, 40):.0f}" y2="3920"/>' for x in range(260, 2600, 390)) + \
           "".join(f'<line x1="-20" y1="{y + gl.uniform(-8, 8):.0f}" x2="2620" y2="{y + gl.uniform(-40, 40):.0f}"/>' for y in range(200, 3900, 420))
    html = f"""<!doctype html>
<html lang="en" data-resolution="square">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Spin Bout U collage lyric edit 1x1</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute"><filter id="mb" x="-5%" y="-5%" width="110%" height="110%">
      <feGaussianBlur id="mbg" stdDeviation="0 0"/></filter>
      <filter id="bloom" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feGaussianBlur id="blg" in="SourceGraphic" stdDeviation="20" result="b"/>
      <feColorMatrix in="b" type="matrix" values=".95 0 0 0 0  0 .72 0 0 0  0 0 .9 0 0  0 0 0 1 0" result="bb"/>
      <feBlend in="SourceGraphic" in2="bb" mode="screen"/></filter>
      <filter id="rgbsplit" color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r"/>
      <feOffset id="rgbR" in="r" dx="0" dy="0" result="r2"/>
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g"/>
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b2"/>
      <feOffset id="rgbB" in="b2" dx="0" dy="0" result="b3"/>
      <feBlend in="r2" in2="g" mode="screen" result="rg"/><feBlend in="rg" in2="b3" mode="screen"/></filter>
      <filter id="smokef" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="4" seed="6"/>
      <feOffset id="smo" dx="0" dy="0" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="140" xChannelSelector="R" yChannelSelector="G"/>
      <feGaussianBlur stdDeviation="3"/></filter>{FX_DEFS}</svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="glow"><div id="fx">
        <div id="bg"><video id="fluid" src="assets/video/fluid_bg.mp4" data-start="0" data-duration="{DUR}" data-track-index="90" muted playsinline></video></div>
        <div id="cam"><div id="pan">
          <div id="paper"></div>
          <div id="board">
            {"".join(PAN)}
          </div>
        </div></div>
        <div id="blinds"></div>
        {"".join(SCREEN)}
      </div></div>
      <div id="leak"></div>
      <div id="vig"></div>
      <div id="grain"></div>
      <audio id="song" src="assets/audio/section.wav" data-start="0" data-duration="{DUR}" data-track-index="0" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const SE = (n, k) => {{ const f = gsap.parseEase(n); return (p) => p >= 1 ? 1 : f(Math.floor(p * k) / k); }};
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
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(scenes())} scenes")


if __name__ == "__main__":
    main()
