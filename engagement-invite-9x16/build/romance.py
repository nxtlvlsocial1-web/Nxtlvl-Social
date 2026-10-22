"""Night scenes and closer couple poses for v5 (our own drawing): stargazing on a palace rooftop,
sitting by a moonlit pond, and an embrace. Faces are drawn in profile: closed, smiling eyes and a blush.
"""
import math
import random

import art
import figures as fg

SK, SKD, HAIR = fg.SKIN, fg.SKIN_D, fg.HAIR


# ------------------------------------------------------------------ poses
def _arm(d, w, col, wmin=None):
    """A sleeve or forearm as a tapered brush stroke along a cubic centre line."""
    return f'<path d="{fg.brush(d, w, wmin or w * .7, shape="taper")}" fill="{col}"/>'


def _profile_face(cx, cy, f, her=False):
    """Content, in-love profile: a closed smiling eye, a blush on the cheek and a soft smile near the front."""
    line = fg.LINE
    ex, ey = cx + 17 * f, cy - 4
    out = (f'<path d="M{ex - 7 * f} {ey} C{ex - 3 * f} {ey + 5} {ex + 3 * f} {ey + 5} {ex + 7 * f} {ey}" stroke="{line}" '
           f'stroke-width="3.2" stroke-linecap="round" fill="none"/>'
           f'<path d="M{ex - 6 * f} {ey - 12} Q{ex} {ey - 16} {ex + 7 * f} {ey - 12}" stroke="{HAIR}" '
           f'stroke-width="{2.4 if her else 3.4}" stroke-linecap="round" fill="none"/>'
           f'<ellipse cx="{cx + 14 * f}" cy="{cy + 11}" rx="8" ry="5" fill="{fg.BLUSH}" opacity="{.6 if her else .45}"/>'
           f'<path d="M{cx + 18 * f} {cy + 19} Q{cx + 24 * f} {cy + 24} {cx + 29 * f} {cy + 17}" '
           f'stroke="{"#c2385b" if her else "#7a2e2a"}" stroke-width="3" stroke-linecap="round" fill="none"/>')
    if her:
        out += (f'<path d="M{ex + 7 * f} {ey} L{ex + 11 * f} {ey + 3} M{ex + 4 * f} {ey + 3} L{ex + 6 * f} {ey + 7}" '
                f'stroke="{line}" stroke-width="2" stroke-linecap="round"/>')
    return out


def _groom_profile_head(cx, cy, facing=1):
    """Head in profile with short, neat hair covering the back and top; no ear."""
    f = facing
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="38" fill="{SK}"/>{_profile_face(cx, cy, f)}'
            f'<path d="M{cx + 6 * f} {cy - 37} C{cx - 30 * f} {cy - 44} {cx - 42 * f} {cy - 10} {cx - 34 * f} {cy + 18} '
            f'C{cx - 28 * f} {cy + 30} {cx - 18 * f} {cy + 32} {cx - 12 * f} {cy + 26} C{cx - 18 * f} {cy + 8} '
            f'{cx - 14 * f} {cy - 12} {cx + 2 * f} {cy - 20} C{cx + 16 * f} {cy - 26} {cx + 30 * f} {cy - 22} '
            f'{cx + 34 * f} {cy - 12} C{cx + 30 * f} {cy - 32} {cx + 20 * f} {cy - 38} {cx + 6 * f} {cy - 37} Z" '
            f'fill="{HAIR}"/>')


def _bride_profile_head(cx, cy, facing, jewel):
    f = facing
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="34" fill="{SK}"/>{_profile_face(cx, cy, f, True)}'
            f'<path d="M{cx + 4 * f} {cy - 33} C{cx - 30 * f} {cy - 40} {cx - 40 * f} {cy - 8} {cx - 30 * f} {cy + 16} '
            f'C{cx - 18 * f} {cy + 8} {cx - 12 * f} {cy - 10} {cx + 2 * f} {cy - 18} C{cx + 18 * f} {cy - 26} '
            f'{cx + 28 * f} {cy - 18} {cx + 30 * f} {cy - 8} C{cx + 26 * f} {cy - 28} {cx + 16 * f} {cy - 34} '
            f'{cx + 4 * f} {cy - 33} Z" fill="{HAIR}"/>'
            f'<circle cx="{cx - 30 * f}" cy="{cy + 4}" r="17" fill="{HAIR}"/>'
            + "".join(f'<circle cx="{cx - 30 * f + 19 * math.cos(a):.0f}" cy="{cy + 4 + 19 * math.sin(a):.0f}" r="3.6" '
                      f'fill="#fff"/>' for a in [k / 8 * math.tau for k in range(8)]) +
            f'<path d="M{cx + 8 * f} {cy - 34} L{cx + 10 * f} {cy - 22}" stroke="{jewel}" stroke-width="2"/>'
            f'<circle cx="{cx + 10 * f}" cy="{cy - 19}" r="4" fill="{jewel}"/>')


def back_seated(pal):
    """Seen from behind, sitting close on a parapet (top edge at y=0), her head resting on his shoulder."""
    coat, trim, stole, pants, shoe = pal["groom"]
    skirt, border, blouse, dup, jewel = pal["bride"]
    return (
        # her lehenga spreading over the parapet
        f'<path d="M-10 -110 C-40 -60 -60 -10 -70 30 C10 46 140 46 180 30 C160 -20 130 -70 90 -110 Z" fill="{skirt}"/>'
        f'<path d="M-70 30 C10 46 140 46 180 30 L176 14 C130 28 10 28 -66 14 Z" fill="{border}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{border}"/>' for x, y in
                  [(-20, 0), (20, 6), (60, 8), (100, 6), (140, 0), (10, -40), (60, -36), (110, -40)]) +
        # her back, leaning in towards him
        f'<g transform="translate(-14 0) rotate(-10 50 -110)">'
        f'<path d="M10 -110 C2 -150 4 -200 20 -236 C40 -250 80 -250 98 -236 C110 -200 110 -150 100 -110 Z" fill="{SK}"/>'
        f'<path d="M14 -170 C10 -200 14 -222 22 -234 C42 -248 78 -248 96 -234 C102 -220 104 -196 102 -170 Z" fill="{blouse}"/>'
        f'<path d="M38 -170 L38 -150 M76 -170 L76 -150" stroke="{jewel}" stroke-width="2"/>'
        f'<path d="M90 -236 C130 -180 140 -100 150 20 L130 24 C120 -80 110 -170 80 -230 Z" fill="{dup}" opacity=".55"/></g>'
        # him, from behind
        f'<path d="M-180 30 C-192 -90 -182 -190 -160 -246 C-136 -266 -64 -266 -40 -246 C-22 -190 -18 -90 -26 30 Z" '
        f'fill="{coat}"/>'
        f'<path d="M-180 22 L-26 22 L-26 34 L-180 34 Z" fill="{trim}"/>'
        f'<path d="M-102 -262 L-102 28" stroke="{trim}" stroke-width="2.5" opacity=".6"/>'
        f'<path d="M-170 -238 C-140 -180 -120 -120 -110 -40 L-94 -44 C-106 -120 -126 -184 -148 -250 Z" fill="{stole}" '
        f'opacity=".9"/>'
        f'<rect x="-114" y="-292" width="24" height="34" fill="{SKD}"/>'
        f'<ellipse cx="-102" cy="-320" rx="40" ry="44" fill="{HAIR}"/>'
        f'<path d="M-140 -330 C-136 -360 -70 -364 -64 -330" stroke="#3a2a26" stroke-width="3" fill="none" opacity=".6"/>'
        # her head resting on his shoulder
        f'<g transform="translate(-52 16) rotate(-34 30 -250)"><rect x="20" y="-280" width="20" height="30" fill="{SKD}"/>'
        f'<ellipse cx="30" cy="-304" rx="32" ry="36" fill="{HAIR}"/>'
        f'<circle cx="30" cy="-280" r="18" fill="{HAIR}"/>'
        + "".join(f'<circle cx="{30 + 20 * math.cos(a):.0f}" cy="{-280 + 20 * math.sin(a):.0f}" r="4.5" fill="#fff"/>'
                  for a in [i / 9 * math.tau for i in range(9)]) +
        f'</g>')


def side_seated(pal):
    """Side view, sitting close on a stone bench (seat top at y=-150): she leans her head on his shoulder,
    her hand resting over his on his knee."""
    coat, trim, stole, pants, shoe = pal["groom"]
    skirt, border, blouse, dup, jewel = pal["bride"]
    return (
        f'<rect x="-170" y="-166" width="380" height="22" rx="6" fill="#a8927a"/>'
        f'<rect x="-160" y="-146" width="360" height="146" fill="#8a7764"/>'
        f'<path d="M-160 -100 H200 M-160 -50 H200" stroke="#6b5a4a" stroke-width="3"/>'
        # him: thigh along the bench, shin down, torso upright
        f'<path d="M-98 -170 L20 -170 C30 -170 34 -160 30 -146 L-98 -140 Z" fill="{pants}"/>'
        f'<path d="M6 -150 L10 -8 L32 -8 L30 -150 Z" fill="{pants}"/>'
        f'<path d="M6 -14 C6 0 46 2 54 -8 L32 -18 Z" fill="{shoe}"/>'
        f'<path d="M-128 -150 C-136 -240 -130 -330 -112 -394 C-92 -408 -48 -408 -30 -394 C-18 -330 -16 -240 -20 -150 Z" '
        f'fill="{coat}"/>'
        f'<path d="M-128 -158 L-20 -158 L-20 -146 L-128 -146 Z" fill="{trim}"/>'
        f'<path d="M-112 -390 C-90 -320 -70 -260 -56 -170 L-40 -172 C-54 -260 -76 -330 -92 -396 Z" fill="{stole}"/>'
        f'<rect x="-82" y="-430" width="22" height="34" fill="{SKD}"/>'
        f'{_groom_profile_head(-66, -462, 1)}'
        # his near arm resting forward on his knee
        + _arm("M-52 -386 C-40 -330 -30 -260 -6 -200 C2 -184 10 -176 18 -172", 26, coat) +
        f'<ellipse cx="20" cy="-170" rx="14" ry="10" fill="{SK}"/>'
        # her: lehenga over the bench, torso, head on his shoulder
        f'<path d="M40 -250 C20 -190 0 -120 -14 -10 C50 4 160 4 186 -10 C170 -110 140 -190 110 -250 Z" fill="{skirt}"/>'
        f'<path d="M-14 -10 C50 4 160 4 186 -10 L182 -30 C150 -18 50 -18 -10 -30 Z" fill="{border}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{border}"/>' for x, y in
                  [(10, -50), (50, -46), (90, -44), (130, -46), (166, -50), (40, -100), (90, -96), (140, -100)]) +
        f'<g transform="rotate(-12 80 -250)">'
        f'<path d="M50 -250 C44 -290 46 -330 58 -360 C74 -372 102 -372 114 -360 C122 -330 122 -290 114 -250 Z" fill="{SK}"/>'
        f'<path d="M52 -300 C48 -326 52 -346 60 -358 C76 -370 100 -370 112 -358 C118 -346 120 -326 116 -300 Z" fill="{blouse}"/>'
        f'<path d="M106 -362 C140 -300 150 -200 160 -40 L138 -36 C132 -180 120 -290 94 -356 Z" fill="{dup}" opacity=".55"/>'
        f'</g>'
        f'<rect x="40" y="-396" width="18" height="34" fill="{SKD}" transform="rotate(-28 50 -380)"/>'
        f'<g transform="rotate(-14 0 -418)">{_bride_profile_head(-2, -418, -1, jewel)}</g>'
        # her near arm reaching to rest her hand on his
        + _arm("M64 -330 C50 -290 40 -230 30 -180", 15, SK) +
        f'<path d="M30 -196 L44 -192" stroke="{jewel}" stroke-width="6"/>'
        f'<ellipse cx="24" cy="-176" rx="13" ry="9" fill="{SK}"/>')


def embrace(pal):
    """Standing embrace, side view: he faces right, she faces left with her head on his chest.
    His arm curves round her back; her hand rests on his back. Feet at y=0."""
    coat, trim, stole, pants, shoe = pal["groom"]
    skirt, border, blouse, dup, jewel = pal["bride"]
    return (
        # his far arm, mostly hidden behind her: only the hand on her back shows
        f'<ellipse cx="96" cy="-300" rx="11" ry="14" fill="{SKD}"/>'
        # him
        f'<path d="M-86 -150 L-90 -12 L-66 -12 L-58 -150 Z" fill="{pants}"/>'
        f'<path d="M-50 -150 L-46 -12 L-22 -12 L-24 -150 Z" fill="{pants}"/>'
        f'<path d="M-92 -16 C-92 0 -56 2 -52 -8 L-64 -18 Z" fill="{shoe}"/>'
        f'<path d="M-48 -16 C-48 0 -10 2 -4 -8 L-20 -18 Z" fill="{shoe}"/>'
        f'<path d="M-114 -150 C-122 -260 -118 -360 -100 -430 C-80 -446 -30 -446 -12 -430 C2 -360 6 -260 0 -150 Z" '
        f'fill="{coat}"/>'
        f'<path d="M-114 -158 L0 -158 L0 -146 L-114 -146 Z" fill="{trim}"/>'
        f'<path d="M-98 -428 C-70 -350 -50 -270 -36 -170 L-20 -174 C-34 -270 -56 -350 -78 -434 Z" fill="{stole}"/>'
        f'<rect x="-62" y="-470" width="22" height="34" fill="{SKD}"/>'
        f'<g transform="rotate(16 -50 -500)">{_groom_profile_head(-44, -500, 1)}</g>'
        # her
        f'<path d="M10 -270 C-10 -200 -40 -90 -54 -4 C20 10 140 10 170 -4 C150 -90 120 -200 90 -270 Z" fill="{skirt}"/>'
        f'<path d="M-54 -4 C20 10 140 10 170 -4 L166 -26 C130 -14 20 -14 -50 -26 Z" fill="{border}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{border}"/>' for x, y in
                  [(-20, -46), (20, -42), (60, -40), (100, -42), (140, -46), (10, -100), (60, -96), (110, -100)]) +
        f'<path d="M14 -270 C8 -310 10 -350 22 -384 C40 -398 72 -398 86 -384 C94 -350 94 -310 86 -270 Z" fill="{SK}"/>'
        f'<path d="M16 -320 C12 -348 16 -370 24 -382 C42 -396 70 -396 84 -382 C90 -370 92 -348 88 -320 Z" fill="{blouse}"/>'
        f'<rect x="20" y="-420" width="18" height="30" fill="{SKD}" transform="rotate(-16 29 -404)"/>'
        f'<g transform="rotate(-20 20 -440)">{_bride_profile_head(12, -446, -1, jewel)}</g>'
        f'<path d="M84 -384 C120 -320 136 -200 150 -40 L128 -36 C120 -180 104 -300 70 -378 Z" fill="{dup}" opacity=".55"/>'
        # his near arm: down from the shoulder, elbow out, forearm across her back
        + _arm("M-30 -414 C-10 -380 0 -350 14 -334 C34 -314 60 -312 86 -318", 26, coat, 20) +
        f'<ellipse cx="92" cy="-318" rx="13" ry="11" fill="{SK}"/>'
        # her near arm: from her shoulder, bent, hand on his upper back
        + _arm("M30 -376 C10 -360 -20 -352 -50 -356 C-70 -358 -86 -362 -98 -366", 16, SK, 12) +
        f'<path d="M-6 -362 L-8 -348" stroke="{jewel}" stroke-width="7"/>'
        f'<ellipse cx="-104" cy="-366" rx="11" ry="10" fill="{SK}"/>')


# ------------------------------------------------------------------ night worlds
def _stars(seed, n=70, ymax=1100):
    r = random.Random(seed)
    return "".join(
        f'<g class="star" data-o="{x:.0f} {y:.0f}"><path d="M{x:.0f} {y - s:.0f} L{x + s * .3:.1f} {y - s * .3:.1f} '
        f'L{x + s:.0f} {y:.0f} L{x + s * .3:.1f} {y + s * .3:.1f} L{x:.0f} {y + s:.0f} L{x - s * .3:.1f} {y + s * .3:.1f} '
        f'L{x - s:.0f} {y:.0f} L{x - s * .3:.1f} {y - s * .3:.1f} Z" fill="#fff1b8"/></g>'
        for x, y, s in ((r.uniform(20, 1060), r.uniform(80, ymax), r.uniform(4, 11)) for _ in range(n)))


def moon(x, y, r=110):
    mid = f"m{x}{y}"
    return (f'<defs><mask id="{mid}"><circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>'
            f'<circle cx="{x + r * .42:.0f}" cy="{y - r * .18:.0f}" r="{r * .92:.0f}" fill="#000"/></mask></defs>'
            f'<g class="moon"><circle cx="{x}" cy="{y}" r="{r * 3}" fill="url(#moonglow)"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff4d6" mask="url(#{mid})"/></g>')


def _sky_layers(sid, sun_x):
    """Afternoon and dusk skies over the night sky, plus a setting sun; the timeline fades them out."""
    return (f'<rect class="dusk" width="1080" height="1920" fill="url(#dusk-{sid})"/>'
            f'<rect class="day" width="1080" height="1920" fill="url(#day-{sid})"/>'
            f'<g class="sun"><circle cx="{sun_x}" cy="700" r="260" fill="url(#sunglow-{sid})"/>'
            f'<circle cx="{sun_x}" cy="700" r="90" fill="#ffe8a3"/></g>')


def _top_shade(sid):
    return (f'<defs><linearGradient id="ts-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0510" '
            f'stop-opacity=".9"/><stop offset=".55" stop-color="#2a0510" stop-opacity=".55"/><stop offset="1" '
            f'stop-color="#2a0510" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="1080" height="820" fill="url(#ts-{sid})"/>')


def _day_defs(sid):
    return (f'<linearGradient id="day-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e7a35a"/>'
            f'<stop offset=".5" stop-color="#f6c98a"/><stop offset="1" stop-color="#fde3b5"/></linearGradient>'
            f'<linearGradient id="dusk-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f0a2a"/>'
            f'<stop offset=".45" stop-color="#9b1c31"/><stop offset=".75" stop-color="#e8590c"/>'
            f'<stop offset="1" stop-color="#fab005"/></linearGradient>'
            f'<radialGradient id="sunglow-{sid}"><stop offset="0" stop-color="#fff3bf" stop-opacity=".9"/>'
            f'<stop offset="1" stop-color="#fff3bf" stop-opacity="0"/></radialGradient>')


def _night_defs(sid):
    return (_day_defs(sid) +f'<linearGradient id="nightsky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1920">'
            f'<stop offset="0" stop-color="#0d0620"/><stop offset=".5" stop-color="#2a0b2e"/>'
            f'<stop offset="1" stop-color="#4a0d1f"/></linearGradient>'
            f'<radialGradient id="moonglow"><stop offset="0" stop-color="#fff1b8" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="#fff1b8" stop-opacity="0"/></radialGradient>')


def rooftop(sid):
    """Palace rooftop at night: crescent moon, stars, chhatri silhouettes, a parapet with lanterns."""
    chhatris = "".join(
        f'<g transform="translate({x} 1330) scale({s})"><rect x="-60" y="-120" width="120" height="120" fill="#1a0614"/>'
        f'<path d="M-70 -120 C-70 -200 70 -200 70 -120 Z" fill="#1a0614"/><path d="M0 -190 L0 -220" stroke="#e9c46a" '
        f'stroke-width="4"/>' + "".join(f'<path d="M{ax} 0 L{ax} -50 C{ax} -70 {ax + 24} -70 {ax + 24} -50 L{ax + 24} 0 Z" '
                                       f'fill="#ffb347" opacity=".5"/>' for ax in (-48, -12, 24)) + '</g>'
        for x, s in [(110, .9), (330, .6), (760, .6), (980, .9)])
    lanterns = "".join(f'<g transform="translate({x} 1420)"><circle class="lglow" r="46" fill="#ffcf6b" opacity=".22"/>'
                       f'<path d="M-14 -24 L14 -24 L18 0 L14 24 L-14 24 L-18 0 Z" fill="#7a1022" stroke="#e9c46a" '
                       f'stroke-width="2"/><path d="M-9 -16 L9 -16 L12 0 L9 16 L-9 16 L-12 0 Z" fill="#ffd166"/></g>'
                       for x in (120, 960))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920"><defs>{_night_defs(sid)}</defs>'
            f'<rect width="1080" height="1920" fill="url(#nightsky)"/>{_sky_layers(sid, 300)}{_stars(len(sid) + 3)}'
            f'{moon(850, 840, 95)}'
            f'<path class="shoot" d="M0 0 L-260 120" stroke="url(#shootg)" stroke-width="5" stroke-linecap="round" '
            f'transform="translate(1000 640)"/>'
            f'<defs><linearGradient id="shootg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
            f'{chhatris}<rect x="0" y="1330" width="1080" height="590" fill="#2a0712"/>'
            f'<rect x="0" y="1440" width="1080" height="40" fill="#5a0b17"/>'
            f'<rect x="0" y="1440" width="1080" height="6" fill="#e9c46a"/>'
            + "".join(f'<path d="M{x} 1480 l0 120 M{x + 20} 1480 l0 120" stroke="#3f0712" stroke-width="12"/>'
                      for x in range(10, 1080, 70)) +
            f'<rect x="0" y="1600" width="1080" height="320" fill="#3a0812"/>{lanterns}{_top_shade(sid)}</svg>')


def pond(sid):
    """Moonlit pond: moon and its reflection, lotus pads, floating diyas, fireflies, palace beyond."""
    r = random.Random(17)
    pads = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * .3:.0f}" fill="#1f4a3a"/>'
                   for x, y, w in [(140, 1560, 60), (900, 1600, 70), (680, 1720, 54), (260, 1800, 66), (980, 1820, 50)])
    lotuses = "".join(f'<g transform="translate({x} {y})">{_lotus()}</g>' for x, y in [(150, 1552), (905, 1590), (265, 1790)])
    diyas = "".join(f'<g class="fdiya" data-o="{x} {y}"><g transform="translate({x} {y}) scale(.45)">{art.diya(90)}'
                    f'</g></g>' for x, y in [(420, 1640), (600, 1600), (780, 1700), (520, 1770)])
    flies = "".join(f'<circle class="fly" cx="{r.uniform(60, 1020):.0f}" cy="{r.uniform(900, 1500):.0f}" r="4" '
                    f'fill="#fff3a0"/>' for _ in range(22))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920"><defs>{_night_defs(sid)}'
            f'<linearGradient id="water-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1035"/>'
            f'<stop offset="1" stop-color="#0b0618"/></linearGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#nightsky)"/>{_sky_layers(sid, 820)}{_stars(len(sid) + 9, 50, 900)}'
            f'{moon(230, 800, 80)}'
            f'<g fill="#1a0614"><path d="M0 1260 L0 1140 L120 1140 L120 1060 C120 980 260 980 260 1060 L260 1140 L420 1140 '
            f'L420 1000 C420 880 660 880 660 1000 L660 1140 L820 1140 L820 1060 C820 980 960 980 960 1060 L960 1140 '
            f'L1080 1140 L1080 1260 Z"/></g>'
            + "".join(f'<rect x="{x}" y="1150" width="18" height="34" fill="#ffb347" opacity=".55"/>'
                      for x in range(30, 1060, 60)) +
            f'<rect x="0" y="1260" width="1080" height="660" fill="url(#water-{sid})"/>'
            f'<g class="reflect" opacity=".5"><ellipse cx="230" cy="1420" rx="70" ry="16" fill="#fff4d6"/>'
            f'<ellipse cx="230" cy="1460" rx="50" ry="8" fill="#fff4d6" opacity=".7"/>'
            f'<ellipse cx="230" cy="1490" rx="34" ry="5" fill="#fff4d6" opacity=".5"/></g>'
            + "".join(f'<path class="ripple" d="M{x} {y} q40 -8 80 0" stroke="#7d6aa8" stroke-width="2" fill="none" opacity=".5"/>'
                      for x, y in [(80, 1330), (500, 1380), (820, 1340), (360, 1480), (700, 1520), (120, 1660)]) +
            f'{pads}{lotuses}{diyas}'
            f'<path d="M600 1500 L1080 1500 L1080 1920 L520 1920 Z" fill="#6b5a4a"/>'
            f'<path d="M600 1500 L1080 1500 L1080 1530 L590 1530 Z" fill="#8a7764"/>'
            f'{flies}{_top_shade(sid)}</svg>')


def _lotus():
    return ('<path d="M0 0 C-8 -10 -8 -22 0 -30 C8 -22 8 -10 0 0 Z" fill="#f9a8d4"/>'
            '<path d="M0 0 C-16 -6 -22 -16 -20 -24 C-10 -20 -4 -12 0 0 Z" fill="#fbcfe8"/>'
            '<path d="M0 0 C16 -6 22 -16 20 -24 C10 -20 4 -12 0 0 Z" fill="#fbcfe8"/>')


def heart_mask_svg():
    return ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 90'>"
            "<path d='M50 88 C20 64 0 46 0 26 C0 10 12 0 27 0 C38 0 46 6 50 14 C54 6 62 0 73 0 C88 0 100 10 100 26 "
            "C100 46 80 64 50 88 Z' fill='black'/></svg>")


def walkway(sid):
    """Night palace path running towards the camera, lamps on both sides, palace facade at the end."""
    lamps = []
    for k in range(6):
        t = k / 5
        y = 1270 + (t ** 1.6) * 560
        s = .35 + t * .9
        for side in (-1, 1):
            x = 540 + side * (150 + t * 470)
            lamps.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"><rect x="-6" y="-240" width="12" '
                         f'height="240" fill="#c9973f"/><circle class="lglow" cy="-255" r="70" fill="#ffcf6b" opacity=".25"/>'
                         f'<circle cy="-255" r="22" fill="#ffd98a"/></g>')
    windows = "".join(f'<rect x="{x}" y="{y}" width="34" height="56" rx="16" fill="#ffb347" opacity=".75"/>'
                      for x in range(260, 820, 70) for y in (1000, 1110))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920"><defs>{_night_defs(sid)}'
            f'<linearGradient id="path-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4a3a"/>'
            f'<stop offset="1" stop-color="#d9c4a0"/></linearGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#nightsky)"/>{_stars(len(sid) + 21, 60, 820)}'
            f'{moon(830, 700, 70)}'
            f'<g fill="#1a0614"><path d="M180 1270 L180 980 L300 980 L300 900 C300 820 420 820 420 900 L420 940 '
            f'C420 800 660 800 660 940 L660 900 C660 820 780 820 780 900 L780 980 L900 980 L900 1270 Z"/></g>{windows}'
            f'<rect x="0" y="1260" width="1080" height="660" fill="#2a0712"/>'
            f'<path d="M470 1265 L610 1265 L1180 1920 L-100 1920 Z" fill="url(#path-{sid})"/>'
            f'<path d="M505 1265 L575 1265 L860 1920 L220 1920 Z" fill="#9b1028"/>'
            f'<path d="M505 1265 L220 1920 M575 1265 L860 1920" stroke="#e9c46a" stroke-width="4"/>'
            f'{"".join(lamps)}{_top_shade(sid)}</svg>')
