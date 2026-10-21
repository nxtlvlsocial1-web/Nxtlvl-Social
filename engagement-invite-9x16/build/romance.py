"""Night scenes and closer couple poses for v5 (our own drawing): stargazing on a palace rooftop,
sitting by a moonlit pond, and an embrace. Faces are left blank, as in the rest of the invite.
"""
import math
import random

import art
import figures as fg

SK, SKD, HAIR = fg.SKIN, fg.SKIN_D, fg.HAIR


# ------------------------------------------------------------------ poses
def back_seated(pal):
    """Seen from behind, sitting on a parapet (top edge at y=0): her head on his shoulder, his arm around her."""
    coat, trim, stole, pants, shoe = pal["groom"]
    skirt, border, blouse, dup, jewel = pal["bride"]
    return (
        # her lehenga spreading over the parapet
        f'<path d="M10 -110 C-20 -60 -40 -10 -50 30 C30 46 160 46 200 30 C180 -20 150 -70 110 -110 Z" fill="{skirt}"/>'
        f'<path d="M-50 30 C30 46 160 46 200 30 L196 14 C150 28 30 28 -46 14 Z" fill="{border}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{border}"/>' for x, y in
                  [(0, 0), (40, 6), (80, 8), (120, 6), (160, 0), (30, -40), (80, -36), (130, -40)]) +
        # him, from behind
        f'<path d="M-170 30 C-182 -90 -172 -190 -150 -246 C-126 -266 -54 -266 -30 -246 C-12 -190 -8 -90 -16 30 Z" '
        f'fill="{coat}"/>'
        f'<path d="M-170 22 L-16 22 L-16 34 L-170 34 Z" fill="{trim}"/>'
        f'<path d="M-92 -262 L-92 28" stroke="{trim}" stroke-width="2.5" opacity=".6"/>'
        f'<path d="M-160 -238 C-130 -180 -110 -120 -100 -40 L-84 -44 C-96 -120 -116 -184 -138 -250 Z" fill="{stole}" '
        f'opacity=".9"/>'
        f'<rect x="-104" y="-292" width="24" height="34" fill="{SKD}"/>'
        f'<ellipse cx="-92" cy="-318" rx="40" ry="44" fill="{HAIR}"/>'
        f'<ellipse cx="-132" cy="-312" rx="7" ry="12" fill="{SK}"/><ellipse cx="-52" cy="-312" rx="7" ry="12" fill="{SK}"/>'
        # her back: blouse, bare midriff, head tilted onto his shoulder, bun with gajra
        f'<path d="M30 -110 C22 -150 24 -200 40 -236 C60 -250 100 -250 118 -236 C130 -200 130 -150 120 -110 Z" fill="{SK}"/>'
        f'<path d="M34 -170 C30 -200 34 -222 42 -234 C62 -248 98 -248 116 -234 C122 -220 124 -196 122 -170 Z" '
        f'fill="{blouse}"/>'
        f'<path d="M58 -170 L58 -150 M96 -170 L96 -150" stroke="{jewel}" stroke-width="2"/>'
        f'<g transform="rotate(-24 70 -250)"><rect x="60" y="-282" width="20" height="30" fill="{SKD}"/>'
        f'<ellipse cx="70" cy="-306" rx="32" ry="36" fill="{HAIR}"/>'
        f'<circle cx="70" cy="-282" r="18" fill="{HAIR}"/>'
        + "".join(f'<circle cx="{70 + 20 * math.cos(a):.0f}" cy="{-282 + 20 * math.sin(a):.0f}" r="4.5" fill="#fff"/>'
                  for a in [i / 9 * math.tau for i in range(9)]) +
        f'</g>'
        f'<path d="M110 -236 C150 -180 160 -100 170 20 L150 24 C140 -80 130 -170 100 -230 Z" fill="{dup}" opacity=".55"/>'
        # his arm around her waist
        f'<path d="M-34 -200 C0 -176 50 -150 112 -128" stroke="{coat}" stroke-width="20" stroke-linecap="round" fill="none"/>'
        f'<path d="M-34 -200 C0 -176 50 -150 112 -128" stroke="{trim}" stroke-width="2" fill="none" opacity=".5"/>'
        f'<ellipse cx="118" cy="-126" rx="11" ry="9" fill="{SK}"/>')


def side_seated(pal):
    """Side view, sitting close on a stone bench (seat top at y=-150): he faces right, she faces left and
    leans into him; heads touching; his arm around her shoulders."""
    coat, trim, stole, pants, shoe = pal["groom"]
    skirt, border, blouse, dup, jewel = pal["bride"]
    return (
        # stone bench they sit on
        f'<rect x="-170" y="-166" width="380" height="22" rx="6" fill="#a8927a"/>'
        f'<rect x="-160" y="-146" width="360" height="146" fill="#8a7764"/>'
        f'<path d="M-160 -100 H200 M-160 -50 H200" stroke="#6b5a4a" stroke-width="3"/>'
        # him
        f'<path d="M-98 -168 L14 -168 L14 -134 L-98 -134 Z" fill="{pants}" rx="10"/>'
        f'<path d="M-4 -150 L4 -8 L26 -8 L22 -150 Z" fill="{pants}"/>'
        f'<path d="M0 -14 C0 0 40 2 48 -8 L26 -18 Z" fill="{shoe}"/>'
        f'<path d="M-128 -150 C-136 -240 -130 -330 -112 -394 C-92 -408 -48 -408 -30 -394 C-18 -330 -16 -240 -20 -150 Z" '
        f'fill="{coat}"/>'
        f'<path d="M-128 -158 L-20 -158 L-20 -146 L-128 -146 Z" fill="{trim}"/>'
        f'<path d="M-112 -390 C-90 -320 -70 -260 -56 -170 L-40 -172 C-54 -260 -76 -330 -92 -396 Z" fill="{stole}"/>'
        f'<rect x="-82" y="-430" width="22" height="34" fill="{SKD}"/>'
        f'<g transform="rotate(10 -66 -460)"><ellipse cx="-62" cy="-462" rx="34" ry="38" fill="{SK}"/>'
        f'<path d="M-96 -462 C-100 -506 -30 -514 -28 -476 C-40 -492 -70 -494 -84 -478 C-90 -470 -94 -462 -96 -462 Z" '
        f'fill="{HAIR}"/><path d="M-96 -462 C-98 -444 -92 -432 -86 -426 L-80 -458 Z" fill="{HAIR}"/></g>'
        # her
        f'<path d="M30 -250 C10 -190 -10 -120 -24 -10 C40 4 150 4 176 -10 C160 -110 130 -190 100 -250 Z" fill="{skirt}"/>'
        f'<path d="M-24 -10 C40 4 150 4 176 -10 L172 -30 C140 -18 40 -18 -20 -30 Z" fill="{border}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{border}"/>' for x, y in
                  [(0, -50), (40, -46), (80, -44), (120, -46), (156, -50), (30, -100), (80, -96), (130, -100)]) +
        f'<path d="M40 -250 C34 -290 36 -330 48 -360 C64 -372 92 -372 104 -360 C112 -330 112 -290 104 -250 Z" fill="{SK}"/>'
        f'<path d="M42 -300 C38 -326 42 -346 50 -358 C66 -370 90 -370 102 -358 C108 -346 110 -326 106 -300 Z" fill="{blouse}"/>'
        f'<g transform="rotate(-16 70 -380)"><rect x="60" y="-408" width="18" height="30" fill="{SKD}"/>'
        f'<ellipse cx="62" cy="-432" rx="30" ry="34" fill="{SK}"/>'
        f'<path d="M92 -432 C96 -472 30 -480 30 -444 C44 -458 74 -460 92 -432 Z" fill="{HAIR}"/>'
        f'<circle cx="96" cy="-428" r="16" fill="{HAIR}"/><circle cx="108" cy="-438" r="4" fill="#fff"/>'
        f'<circle cx="110" cy="-424" r="4" fill="#fff"/><circle cx="62" cy="-466" r="4" fill="{jewel}"/></g>'
        f'<path d="M96 -362 C130 -300 140 -200 150 -40 L128 -36 C122 -180 110 -290 84 -356 Z" fill="{dup}" opacity=".55"/>'
        # her hand on his knee, his arm over her shoulders
        f'<path d="M50 -300 C30 -250 10 -200 0 -166" stroke="{SK}" stroke-width="14" stroke-linecap="round" fill="none"/>'
        f'<path d="M-40 -380 C0 -394 60 -380 104 -344" stroke="{coat}" stroke-width="26" stroke-linecap="round" fill="none"/>'
        f'<circle cx="108" cy="-338" r="12" fill="{SK}"/>')


def embrace(pal):
    """Standing embrace, side view: he faces right, she faces left with her head on his chest. Feet at y=0."""
    coat, trim, stole, pants, shoe = pal["groom"]
    skirt, border, blouse, dup, jewel = pal["bride"]
    return (
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
        f'<g transform="rotate(14 -50 -500)"><ellipse cx="-44" cy="-500" rx="34" ry="38" fill="{SK}"/>'
        f'<path d="M-78 -500 C-82 -544 -12 -552 -10 -514 C-22 -530 -52 -532 -66 -516 C-72 -508 -76 -500 -78 -500 Z" '
        f'fill="{HAIR}"/><path d="M-78 -500 C-80 -482 -74 -470 -68 -464 L-62 -496 Z" fill="{HAIR}"/></g>'
        # her
        f'<path d="M10 -270 C-10 -200 -40 -90 -54 -4 C20 10 140 10 170 -4 C150 -90 120 -200 90 -270 Z" fill="{skirt}"/>'
        f'<path d="M-54 -4 C20 10 140 10 170 -4 L166 -26 C130 -14 20 -14 -50 -26 Z" fill="{border}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{border}"/>' for x, y in
                  [(-20, -46), (20, -42), (60, -40), (100, -42), (140, -46), (10, -100), (60, -96), (110, -100)]) +
        f'<path d="M14 -270 C8 -310 10 -350 22 -384 C40 -398 72 -398 86 -384 C94 -350 94 -310 86 -270 Z" fill="{SK}"/>'
        f'<path d="M16 -320 C12 -348 16 -370 24 -382 C42 -396 70 -396 84 -382 C90 -370 92 -348 88 -320 Z" fill="{blouse}"/>'
        f'<g transform="rotate(-18 30 -400)"><rect x="24" y="-426" width="18" height="30" fill="{SKD}"/>'
        f'<ellipse cx="22" cy="-450" rx="30" ry="34" fill="{SK}"/>'
        f'<path d="M52 -450 C56 -490 -10 -498 -10 -462 C4 -476 34 -478 52 -450 Z" fill="{HAIR}"/>'
        f'<circle cx="56" cy="-446" r="16" fill="{HAIR}"/><circle cx="68" cy="-456" r="4" fill="#fff"/>'
        f'<circle cx="70" cy="-442" r="4" fill="#fff"/><circle cx="22" cy="-484" r="4" fill="{jewel}"/></g>'
        f'<path d="M84 -384 C120 -320 136 -200 150 -40 L128 -36 C120 -180 104 -300 70 -378 Z" fill="{dup}" opacity=".55"/>'
        # arms: his around her back, hers around his waist
        f'<path d="M-20 -400 C30 -392 70 -370 92 -330" stroke="{coat}" stroke-width="26" stroke-linecap="round" fill="none"/>'
        f'<circle cx="94" cy="-326" r="12" fill="{SK}"/>'
        f'<path d="M24 -330 C-10 -310 -60 -296 -104 -290" stroke="{SK}" stroke-width="15" stroke-linecap="round" fill="none"/>'
        f'<path d="M-6 -316 L-12 -300" stroke="{jewel}" stroke-width="7"/>'
        f'<circle cx="-106" cy="-290" r="10" fill="{SK}"/>')


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


def _night_defs(sid):
    return (f'<linearGradient id="nightsky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1920">'
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
    lanterns = "".join(f'<g transform="translate({x} 1420)"><circle r="46" fill="#ffcf6b" opacity=".22"/>'
                       f'<path d="M-14 -24 L14 -24 L18 0 L14 24 L-14 24 L-18 0 Z" fill="#7a1022" stroke="#e9c46a" '
                       f'stroke-width="2"/><path d="M-9 -16 L9 -16 L12 0 L9 16 L-9 16 L-12 0 Z" fill="#ffd166"/></g>'
                       for x in (120, 960))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920"><defs>{_night_defs(sid)}</defs>'
            f'<rect width="1080" height="1920" fill="url(#nightsky)"/>{_stars(len(sid) + 3)}'
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
            f'<rect x="0" y="1600" width="1080" height="320" fill="#3a0812"/>{lanterns}</svg>')


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
            f'<rect width="1080" height="1920" fill="url(#nightsky)"/>{_stars(len(sid) + 9, 50, 900)}'
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
            f'{flies}</svg>')


def _lotus():
    return ('<path d="M0 0 C-8 -10 -8 -22 0 -30 C8 -22 8 -10 0 0 Z" fill="#f9a8d4"/>'
            '<path d="M0 0 C-16 -6 -22 -16 -20 -24 C-10 -20 -4 -12 0 0 Z" fill="#fbcfe8"/>'
            '<path d="M0 0 C16 -6 22 -16 20 -24 C10 -20 4 -12 0 0 Z" fill="#fbcfe8"/>')


def heart_mask_svg():
    return ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 90'>"
            "<path d='M50 88 C20 64 0 46 0 26 C0 10 12 0 27 0 C38 0 46 6 50 14 C54 6 62 0 73 0 C88 0 100 10 100 26 "
            "C100 46 80 64 50 88 Z' fill='black'/></svg>")
