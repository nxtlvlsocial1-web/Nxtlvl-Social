"""Scene 'worlds' for v3, after the two new references (our own drawing):

- palace world: a cusped Mughal arch draped with flowers and hanging strands, a balustrade over a
  lotus lake, shrubs and a peacock. Each scene gets its own palette (mint, haldi, sangeet, wedding).
- garden world: an airy ivory page with wisteria at the top and a painted garden vignette
  (gazebo, fountain, swans) rising from the bottom.
- the marble pillar that sweeps across between scenes.
- couples on a swing and dancing.
"""
import math
import random

import art
import elements as el
import figures as fg

THEMES = {
    "mint":    dict(sky=("#bfe3d9", "#e9f4e6"), fl=("#e0457b", "#ffffff", "#f59fb8"), hang=None,
                    lake=("#4f8aa0", "#2f6075"), text="dark"),
    "haldi":   dict(sky=("#bfe0f2", "#fbf0cf"), fl=("#f59e0b", "#fde047", "#fb923c"), hang="amaltas",
                    lake=("#4f8aa0", "#2f6075"), text="dark"),
    "sangeet": dict(sky=("#4b2a63", "#8b5a92"), fl=("#93c5fd", "#e0e7ff", "#60a5fa"), hang="bluebells",
                    lake=("#3b5f7a", "#22384d"), text="light"),
    "wedding": dict(sky=("#f7c6cf", "#fde7df"), fl=("#be185d", "#f472b6", "#fbcfe8"), hang="bougain",
                    lake=("#4f8aa0", "#2f6075"), text="dark"),
}

FRAME1, FRAME2, FRAME_D = "#e3cfa3", "#bfa070", "#8e7346"


def _arch_points(n=11):
    """Points along a pointed arch from the left spring (92, 560) through the apex to (988, 560)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        if t <= .5:
            u = t / .5
            p0, p1, p2, p3 = (92, 560), (92, 330), (330, 240), (540, 150)
        else:
            u = (t - .5) / .5
            p0, p1, p2, p3 = (540, 150), (750, 240), (988, 330), (988, 560)
        w = 1 - u
        x = w ** 3 * p0[0] + 3 * w * w * u * p1[0] + 3 * w * u * u * p2[0] + u ** 3 * p3[0]
        y = w ** 3 * p0[1] + 3 * w * w * u * p1[1] + 3 * w * u * u * p2[1] + u ** 3 * p3[1]
        pts.append((x, y))
    return pts


def opening_path():
    """The cusped (multifoil) opening: a run of lobes between cusp points."""
    pts = _arch_points()
    d = f"M92 1560 L92 {pts[0][1]:.0f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ch = math.hypot(x1 - x0, y1 - y0)
        d += f" A{ch * .58:.0f} {ch * .58:.0f} 0 0 1 {x1:.0f} {y1:.0f}"
    d += " L988 1560 Z"
    return d


def _garland(theme, seed):
    r = random.Random(seed)
    pts = _arch_points(40)
    c1, c2, c3 = THEMES[theme]["fl"]
    out = []
    for i, (x, y) in enumerate(pts):
        for _ in range(2):
            out.append(art.leaf(round(x + r.uniform(-18, 18)), round(y + r.uniform(-14, 6)), r.uniform(34, 52),
                                r.choice((150, 180, 210, 120, 240)), col=r.choice([art.LEAF2, art.LEAF3, el.LEAF_T])))
    for i, (x, y) in enumerate(pts):
        if i % 1 == 0:
            col = (c1, c2, c3)[i % 3]
            out.append(el.flower5(round(x + r.uniform(-10, 10)), round(y + r.uniform(-6, 10)), r.uniform(18, 26), col,
                                  centre="#facc15" if col != c2 else c1))
    # heavier clusters at the shoulders and apex
    for x, y in [(120, 470), (960, 470), (220, 300), (860, 300), (540, 170)]:
        for k in range(6):
            a = k / 6 * math.tau
            out.append(el.flower5(round(x + math.cos(a) * 26), round(y + math.sin(a) * 20), 24,
                                  (c1, c2, c3)[k % 3], centre="#facc15"))
    return f'<g class="garland">{"".join(out)}</g>'


def _hangers(kind, seed):
    if not kind:
        return ""
    r = random.Random(seed)
    pts = _arch_points(24)[2:-2]
    out = []
    for i, (x, y) in enumerate(pts):
        ln = r.uniform(90, 260) * (1.2 if abs(x - 540) < 260 else .8)
        if kind == "amaltas":
            cols = ("#facc15", "#fbbf24", "#fde047")
        elif kind == "bluebells":
            cols = ("#93c5fd", "#c7d2fe", "#60a5fa")
        else:
            cols = ("#db2777", "#f472b6", "#be185d")
        beads = "".join(
            f'<ellipse cx="{x + math.sin(j * .9) * 5:.0f}" cy="{y + 10 + j * 13:.0f}" rx="{max(2.5, 7.5 - j * 0.28):.1f}" '
            f'ry="6" fill="{cols[(i + j) % 3]}"/>' for j in range(int(ln / 13)))
        out.append(f'<g class="hang" data-o="{x:.0f} {y:.0f}">'
                   f'<path d="M{x:.0f} {y:.0f} L{x:.0f} {y + ln:.0f}" stroke="#6b8e4e" stroke-width="2"/>{beads}</g>')
    return f'<g class="hangers">{"".join(out)}</g>'


def _lake(theme):
    a, b = THEMES[theme]["lake"]
    pads = "".join(
        f'<g transform="translate({x} {y})"><ellipse rx="44" ry="13" fill="#3f7a4a"/>'
        f'<path d="M0 0 L40 -4 L40 4 Z" fill="{b}"/>'
        f'{"" if k % 2 else _lotus()}</g>'
        for k, (x, y) in enumerate([(170, 1780), (420, 1850), (690, 1790), (900, 1870), (300, 1900), (560, 1745)]))
    ripples = "".join(f'<path d="M{x} {y} q30 -6 60 0" stroke="#bcd8e4" stroke-width="2" fill="none" opacity=".5"/>'
                      for x, y in [(80, 1740), (480, 1800), (760, 1740), (240, 1860), (840, 1820), (620, 1900)])
    return (f'<defs><linearGradient id="lake-{theme}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset="1" stop-color="{b}"/></linearGradient></defs>'
            f'<rect x="0" y="1690" width="1080" height="230" fill="url(#lake-{theme})"/>{ripples}{pads}')


def _lotus():
    return ('<g transform="translate(0 -6)"><path d="M0 0 C-8 -10 -8 -22 0 -30 C8 -22 8 -10 0 0 Z" fill="#f9a8d4"/>'
            '<path d="M0 0 C-16 -6 -22 -16 -20 -24 C-10 -20 -4 -12 0 0 Z" fill="#fbcfe8"/>'
            '<path d="M0 0 C16 -6 22 -16 20 -24 C10 -20 4 -12 0 0 Z" fill="#fbcfe8"/></g>')


def _baluster_row(y):
    posts = "".join(
        f'<path d="M{x} {y + 34} C{x - 9} {y + 50} {x - 11} {y + 74} {x - 4} {y + 92} C{x - 10} {y + 104} {x - 9} '
        f'{y + 116} {x - 6} {y + 124} L{x + 6} {y + 124} C{x + 9} {y + 116} {x + 10} {y + 104} {x + 4} {y + 92} '
        f'C{x + 11} {y + 74} {x + 9} {y + 50} {x} {y + 34} Z" fill="#f8f5ef"/>' for x in range(24, 1080, 36))
    return (f'<rect x="0" y="{y + 30}" width="1080" height="96" fill="#a9cbd6"/>'
            f'<rect x="0" y="{y}" width="1080" height="34" fill="#fbf9f4"/>'
            f'<rect x="0" y="{y + 30}" width="1080" height="5" fill="#d9d2c4"/>{posts}'
            f'<rect x="0" y="{y + 124}" width="1080" height="26" fill="#ece6da"/>')


def _shrubs(seed, dark=False):
    r = random.Random(seed)
    cols = ("#3d6b3f", "#4f7d47", "#2f5734") if not dark else ("#2f4f3a", "#3b5f45", "#22402d")
    out = []
    for x in list(range(-20, 300, 46)) + list(range(780, 1110, 46)) + list(range(300, 790, 70)):
        h = r.uniform(80, 170) if (x < 300 or x > 780) else r.uniform(40, 80)
        for k in range(5):
            out.append(f'<circle cx="{x + r.uniform(-24, 24):.0f}" cy="{1540 - h + r.uniform(0, h):.0f}" '
                       f'r="{r.uniform(22, 40):.0f}" fill="{r.choice(cols)}"/>')
    return "".join(out)


def palace(theme, sid, fl_seed=1):
    t = THEMES[theme]
    s1, s2 = t["sky"]
    side = (art.banana_leaf(110, 1420, 300, 12, col=art.LEAF1) + art.banana_leaf(150, 1440, 220, 50, col=art.LEAF2) +
            art.banana_leaf(970, 1420, 300, -12, col=art.LEAF1) + art.banana_leaf(930, 1440, 220, -50, col=art.LEAF2))
    blooms = "".join(el.flower5(x, y, 22, t["fl"][k % 3], centre="#facc15")
                     for k, (x, y) in enumerate([(150, 1180), (190, 1230), (130, 1270), (930, 1180), (890, 1230),
                                                 (950, 1270), (175, 1320), (905, 1320)]))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<defs><linearGradient id="sky-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{s1}"/>'
            f'<stop offset="1" stop-color="{s2}"/></linearGradient>'
            f'<linearGradient id="frm-{sid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{FRAME2}"/>'
            f'<stop offset=".08" stop-color="{FRAME1}"/><stop offset=".92" stop-color="{FRAME1}"/>'
            f'<stop offset="1" stop-color="{FRAME2}"/></linearGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#sky-{sid})"/>'
            f'<g class="w-far">{_shrubs(fl_seed, theme == "sangeet")}</g>'
            f'<g class="w-side">{side}{blooms}</g>'
            f'{_baluster_row(1540)}{_lake(theme)}'
            f'<path fill-rule="evenodd" fill="url(#frm-{sid})" d="M0 0 H1080 V1560 H0 Z {opening_path()}"/>'
            f'<path d="{opening_path()}" fill="none" stroke="{FRAME_D}" stroke-width="5"/>'
            f'<path d="M40 0 V1560 M1040 0 V1560" stroke="{FRAME_D}" stroke-width="3" opacity=".5"/>'
            f'<rect x="0" y="540" width="100" height="34" fill="{FRAME_D}" opacity=".55"/>'
            f'<rect x="980" y="540" width="100" height="34" fill="{FRAME_D}" opacity=".55"/>'
            + "".join(f'<path d="M{x} {y} l12 16 l-12 16 l-12 -16 Z" fill="none" stroke="{FRAME_D}" stroke-width="2.5" opacity=".55"/>'
                      for x in (46, 1034) for y in range(640, 1500, 70)) +
            f'<path d="M0 30 H1080" stroke="{FRAME_D}" stroke-width="3" opacity=".4"/>'
            f'{_hangers(t["hang"], fl_seed + 7)}{_garland(theme, fl_seed)}'
            f'<g class="w-pea">{art.peacock(215, 1548, .8)}</g></svg>')


# ------------------------------------------------------------------ garden world (WedMeGood style)
PAINT = ('<filter id="paint" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" '
         'baseFrequency=".035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="7"/>'
         '<feGaussianBlur stdDeviation=".6"/></filter>')


def wisteria(seed=5):
    r = random.Random(seed)
    out = []
    for i in range(30):
        x = r.uniform(-20, 1100)
        ln = r.uniform(90, 230)
        for j in range(int(ln / 11)):
            out.append(f'<ellipse cx="{x + r.uniform(-9, 9):.0f}" cy="{j * 11 + r.uniform(0, 6):.0f}" '
                       f'rx="{max(3, 11 - j * 11 / ln * 8):.1f}" ry="6" fill="{r.choice(["#b4a0d8", "#c9b8e8", "#9d86c9", "#e2d6f3"])}" '
                       f'opacity=".85"/>')
        for _ in range(2):
            out.append(art.leaf(round(x + r.uniform(-30, 30)), round(r.uniform(0, 40)), r.uniform(40, 60),
                                r.choice((160, 200, 180)), col=r.choice(["#7d9b6a", "#5f8253"])))
    return f'<g class="wisteria">{"".join(out)}</g>'


def gazebo(x, y, s=1.0):
    c, d = "#f3dcd8", "#d8b4ae"
    cols = "".join(f'<rect x="{cx}" y="-230" width="16" height="230" fill="{c}"/>'
                   f'<rect x="{cx}" y="-230" width="5" height="230" fill="{d}" opacity=".6"/>' for cx in (-110, -48, 32, 94))
    vines = "".join(art.rose(cx, cy, 14, col="#f9a8d4", light="#fce7f3", dark="#db2777")
                    for cx, cy in [(-100, -170), (-96, -90), (102, -150), (98, -60), (-40, -246), (40, -246)])
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#paint)">'
            f'<ellipse cx="0" cy="6" rx="150" ry="16" fill="#e7d3c8"/>'
            f'<rect x="-140" y="-14" width="280" height="22" fill="{d}"/>{cols}'
            f'<rect x="-130" y="-252" width="260" height="24" fill="{c}"/>'
            f'<path d="M-120 -252 C-120 -360 120 -360 120 -252 Z" fill="{c}"/>'
            f'<path d="M-60 -262 C-60 -330 60 -330 60 -262" stroke="{d}" stroke-width="5" fill="none"/>'
            f'<path d="M0 -340 L0 -380" stroke="{d}" stroke-width="6"/><circle cy="-384" r="9" fill="{d}"/>'
            f'{vines}</g>')


def fountain(x, y, s=1.0):
    c, d = "#f1ddd6", "#d4b0a6"
    drops = "".join(f'<path d="M{dx} -150 Q{dx * 2.2} -120 {dx * 3.2} -60" stroke="#bfe3f2" stroke-width="4" '
                    f'fill="none" opacity=".8"/>' for dx in (-14, -7, 7, 14))
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#paint)">'
            f'<ellipse cx="0" cy="0" rx="200" ry="40" fill="{d}"/><ellipse cx="0" cy="-12" rx="190" ry="34" fill="{c}"/>'
            f'<ellipse cx="0" cy="-16" rx="160" ry="22" fill="#a9d6ea"/>'
            f'<path d="M-24 -20 L-14 -120 L14 -120 L24 -20 Z" fill="{c}"/>'
            f'<ellipse cx="0" cy="-124" rx="80" ry="18" fill="{d}"/><ellipse cx="0" cy="-130" rx="74" ry="13" fill="#bfe3f2"/>'
            f'<path d="M-10 -136 L-6 -176 L6 -176 L10 -136 Z" fill="{c}"/><ellipse cx="0" cy="-180" rx="26" ry="8" fill="{d}"/>'
            f'{drops}<path class="spray" d="M0 -186 C-4 -200 4 -212 0 -224" stroke="#bfe3f2" stroke-width="5" fill="none"/></g>')


def swan(x, y, s=1.0, flip=False):
    sx = -s if flip else s
    return (f'<g class="swan" transform="translate({x} {y}) scale({sx} {s})">'
            f'<path d="M-50 0 C-50 -26 -10 -34 30 -20 C44 -14 52 -4 50 4 C20 12 -30 12 -50 0 Z" fill="#fff"/>'
            f'<path d="M-40 -10 C-20 -30 10 -30 26 -18" stroke="#e5e7eb" stroke-width="4" fill="none"/>'
            f'<path d="M30 -18 C40 -40 30 -60 40 -74 C46 -82 58 -80 60 -72" stroke="#fff" stroke-width="10" '
            f'stroke-linecap="round" fill="none"/>'
            f'<path d="M60 -74 L74 -68 L60 -66 Z" fill="#f97316"/><circle cx="56" cy="-74" r="2" fill="#111"/></g>')


def garden_vignette(kind, sid):
    """Painted garden band for the bottom of the ivory page (1080 x 760, origin y=1160)."""
    r = random.Random(len(kind) + 11)
    trees = "".join(
        f'<g filter="url(#paint)">{art.tree(x, y, s, r.randint(0, 99))}</g>'
        for x, y, s in [(70, 1720, .75), (1010, 1720, .75), (250, 1660, .45), (830, 1660, .45)])
    bushes = "".join(
        f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{c}" opacity=".9"/>'
        for x, y, rr, c in [(160, 1700, 70, "#7ea36b"), (300, 1720, 60, "#5f8a55"), (780, 1720, 60, "#5f8a55"),
                            (920, 1700, 70, "#7ea36b"), (40, 1760, 70, "#4f7d47"), (1040, 1760, 70, "#4f7d47")])
    flowers = "".join(el.flower5(x, y, 14, c, centre="#facc15") for x, y, c in
                      [(120, 1800, "#f9a8d4"), (180, 1830, "#c4b5fd"), (260, 1810, "#f9a8d4"), (820, 1810, "#f9a8d4"),
                       (900, 1830, "#c4b5fd"), (960, 1800, "#f9a8d4"), (380, 1860, "#fbcfe8"), (700, 1860, "#fbcfe8")])
    if kind == "gazebo":
        centre = (f'<path d="M140 1800 C380 1765 700 1765 940 1800 L940 1920 L140 1920 Z" fill="#9fd3ea" opacity=".9"/>'
                  f'{gazebo(540, 1770, 1.25)}{swan(330, 1880, 1.0)}{swan(760, 1895, .9, True)}')
    else:
        centre = fountain(540, 1810, 1.35)
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<defs>{PAINT}</defs><rect width="1080" height="1920" fill="#f7f3ec"/>'
            f'<rect x="0" y="1760" width="1080" height="160" fill="#efe3cf"/>'
            f'<g class="gv-back">{trees}{bushes}</g><g class="gv-centre">{centre}</g><g>{flowers}</g>'
            f'{wisteria()}</svg>')


# ------------------------------------------------------------------ the pillar wipe
def pillar():
    flutes = "".join(f'<rect x="{x}" y="0" width="14" height="1920" fill="{c}"/>'
                     for x, c in zip(range(20, 240, 30), ["#e5e5e5", "#cfcfcf", "#e9e9e9", "#c8c8c8", "#e3e3e3",
                                                          "#cdcdcd", "#e7e7e7", "#d2d2d2"]))
    vine = "".join(art.leaf(x, y, 60, a, col=c, vein="#2a0e0e")
                   for x, y, a, c in [(60, 200, 40, "#4a1f1f"), (200, 360, -30, "#5b2626"), (40, 620, 60, "#3d1a1a"),
                                      (210, 820, -50, "#4a1f1f"), (70, 1100, 30, "#5b2626"), (190, 1320, -40, "#3d1a1a"),
                                      (50, 1580, 50, "#4a1f1f"), (200, 1760, -20, "#5b2626")])
    return (f'<svg viewBox="0 0 260 1920" width="260" height="1920">'
            f'<defs><linearGradient id="pil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a9a9a"/>'
            f'<stop offset=".35" stop-color="#f4f4f4"/><stop offset=".7" stop-color="#e2e2e2"/>'
            f'<stop offset="1" stop-color="#8d8d8d"/></linearGradient></defs>'
            f'<rect width="260" height="1920" fill="url(#pil)"/>{flutes}'
            f'<rect width="260" height="1920" fill="url(#pil)" opacity=".55"/>'
            f'<path d="M30 0 C200 300 40 600 220 900 C60 1200 220 1500 40 1920" stroke="#3a1616" stroke-width="10" '
            f'fill="none"/>{vine}</svg>')


# ------------------------------------------------------------------ couples in action
def swing_couple(pal_g, pal_b):
    """Couple on a jhoola. Origin = seat centre; ropes run up 900 px."""
    coat, trim, stole, pants, shoe = pal_g
    skirt, border, blouse, dup, jewel = pal_b
    sk, skd, hair = fg.SKIN, fg.SKIN_D, fg.HAIR
    return (
        f'<path d="M-180 0 L-180 -1300 M180 0 L180 -1300" stroke="#c9a15b" stroke-width="7"/>'
        + "".join(f'<circle cx="{x}" cy="{-y}" r="6" fill="#f59e0b"/>' for x in (-180, 180) for y in range(120, 1300, 90)) +
        # groom, seated (left)
        f'<rect x="-120" y="10" width="22" height="140" rx="8" fill="{pants}"/>'
        f'<rect x="-88" y="10" width="22" height="140" rx="8" fill="{pants}"/>'
        f'<ellipse cx="-110" cy="152" rx="20" ry="9" fill="{shoe}"/><ellipse cx="-76" cy="152" rx="20" ry="9" fill="{shoe}"/>'
        f'<path d="M-140 10 C-150 -60 -148 -150 -130 -200 C-110 -214 -70 -214 -50 -200 C-34 -150 -34 -60 -42 10 Z" '
        f'fill="{coat}"/>'
        f'<path d="M-91 -205 L-91 10" stroke="{trim}" stroke-width="3"/>'
        f'<path d="M-138 -196 C-110 -140 -80 -80 -60 -20 L-46 -26 C-64 -90 -96 -150 -118 -206 Z" fill="{stole}"/>'
        f'<rect x="-100" y="-238" width="18" height="30" fill="{skd}"/>'
        f'<ellipse cx="-90" cy="-268" rx="30" ry="36" fill="{sk}"/>'
        f'<path d="M-120 -270 C-124 -312 -60 -318 -58 -278 C-66 -296 -100 -298 -120 -270 Z" fill="{hair}"/>'
        # his arm across to her hand
        f'<path d="M-52 -180 C-20 -140 0 -100 10 -70 L24 -76 C14 -110 -10 -150 -40 -196 Z" fill="{coat}"/>'
        # bride, seated (right), head on his shoulder
        f'<path d="M-30 -40 C-60 40 -70 120 -60 170 C10 186 120 186 150 170 C160 110 130 30 100 -40 Z" fill="{skirt}"/>'
        f'<path d="M-60 170 C10 186 120 186 150 170 L148 150 C110 162 0 162 -58 150 Z" fill="{border}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{border}"/>' for x, y in
                  [(-30, 120), (10, 130), (50, 132), (90, 128), (125, 118), (-10, 70), (40, 80), (90, 74)]) +
        f'<path d="M-6 -40 C-14 -100 -10 -150 6 -190 C30 -200 66 -200 84 -186 C96 -150 98 -90 92 -40 Z" fill="{sk}"/>'
        f'<path d="M-4 -150 C-8 -170 0 -190 10 -196 C34 -204 70 -202 86 -190 C92 -176 92 -160 90 -150 Z" fill="{blouse}"/>'
        f'<g transform="rotate(-22 30 -205)"><rect x="22" y="-228" width="16" height="26" fill="{skd}"/>'
        f'<ellipse cx="30" cy="-256" rx="27" ry="32" fill="{sk}"/>'
        f'<path d="M58 -256 C62 -296 0 -304 -2 -262 C8 -280 40 -284 58 -256 Z" fill="{hair}"/>'
        f'<circle cx="62" cy="-250" r="16" fill="{hair}"/><circle cx="30" cy="-286" r="4" fill="{jewel}"/></g>'
        f'<path d="M20 -40 C40 -120 70 -180 110 -200 C130 -120 140 -40 150 60 L120 70 C110 0 100 -80 92 -150 Z" '
        f'fill="{dup}" opacity=".6"/>'
        f'<circle cx="16" cy="-70" r="11" fill="{sk}"/>'
        # seat on top of their laps
        f'<rect x="-190" y="-6" width="380" height="22" rx="6" fill="#a07a3c"/>'
        f'<rect x="-190" y="-6" width="380" height="7" rx="3" fill="#c9a15b"/>')


def dholak(x, y, s=1.0):
    """Barrel drum lying on its side, with lacing."""
    laces = "".join(f'<path d="M{-52 + k * 15} -30 L{-44 + k * 15} 30" stroke="#f5e6c8" stroke-width="2"/>' for k in range(7))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-60 -34 C-20 -46 20 -46 60 -34 L60 34 C20 46 -20 46 -60 34 Z" fill="#8a3b12"/>'
            f'<path d="M-60 -6 C-20 4 20 4 60 -6" stroke="#c2410c" stroke-width="6" fill="none"/>{laces}'
            f'<ellipse cx="-60" cy="0" rx="14" ry="34" fill="#f3e3c3"/><ellipse cx="60" cy="0" rx="14" ry="34" fill="#e9d3a8"/>'
            f'<ellipse cx="-60" cy="0" rx="14" ry="34" fill="none" stroke="#5b2509" stroke-width="3"/>'
            f'<ellipse cx="60" cy="0" rx="14" ry="34" fill="none" stroke="#5b2509" stroke-width="3"/></g>')


def sangeet_couple(pal_g, pal_b):
    """The same hand-holding couple as the other scenes, with dholaks and music notes around them.
    Origin at their feet."""
    notes = "".join(f'<text class="note" x="{x}" y="{y}" font-size="{fs}" fill="{c}" font-family="serif">{t}</text>'
                    for x, y, fs, c, t in [(-230, -430, 64, "#f5d58a", "♪"), (210, -470, 56, "#fde68a", "♫"),
                                           (-170, -560, 48, "#fbcfe8", "♫"), (250, -330, 52, "#f5d58a", "♪"),
                                           (0, -640, 44, "#fde68a", "♪")])
    return (f'<g class="sg-notes">{notes}</g>'
            f'<g class="dsway">{fg.couple({"groom": pal_g, "bride": pal_b}, "cs")}</g>'
            f'{dholak(-205, -36, .95)}{dholak(300, -36, 1.0)}')
