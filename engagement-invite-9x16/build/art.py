"""Hand-drawn SVG art for the engagement invite (all our own drawing, no third-party images).

Every function returns an SVG fragment string in the 1080x1920 frame unless it says otherwise.
"""
import math
import random

# palette: pastel sky, sandstone, leaf greens, peacock blues, rose and marigold accents
SKY1, SKY2, SKY3 = "#cfe9f1", "#e9f5f3", "#fbf3e6"
HILL1, HILL2, HILL3 = "#a9d3d6", "#8fc3c4", "#7fb5ad"
SAND, SAND2, SAND_D = "#f1dcc0", "#e5c39b", "#c99a6b"
CREAM, CREAM_D = "#fbf4e8", "#e8dcc6"
LEAF1, LEAF2, LEAF3, LEAF_D = "#9cc27a", "#6fa457", "#4e8a45", "#2f5f34"
PEA_B, PEA_T, PEA_G, PEA_D = "#1f5fa8", "#1f9a9a", "#4e9a4e", "#123e6e"
ROSE, ROSE_L, ROSE_D = "#e86b8f", "#f6b3c6", "#b83a64"
MARI, MARI_D, MARI_L = "#f6a623", "#e07b16", "#ffd166"
GOLD, GOLD_D = "#c9973f", "#9c6f24"
MAROON = "#7d1d3f"


def rng(seed):
    return random.Random(seed)


# ------------------------------------------------------------------ Ganesh ji (line art)
# Drawn in a 400x440 box, centre x = 200. Each stroke has pathLength=1 so the
# timeline can draw it on with stroke-dashoffset.
GANESH_PATHS = [
    # crown (mukut)
    "M150 152 C150 112 172 82 200 44 C228 82 250 112 250 152",
    "M146 152 Q200 168 254 152",
    "M152 132 Q200 146 248 132",
    "M164 112 Q200 124 236 112",
    "M200 44 L200 30",
    # forehead and head outline
    "M146 156 C140 172 140 188 146 204",
    "M254 156 C260 172 260 188 254 204",
    # left ear, scalloped
    "M146 168 C118 146 82 150 68 172 C58 188 62 200 58 214 C54 230 66 246 74 256 "
    "C84 270 104 278 122 274 C132 272 140 266 146 258",
    "M138 186 C118 174 96 180 88 198 C82 214 88 232 102 242 C114 250 128 248 136 240",
    # right ear, mirrored
    "M254 168 C282 146 318 150 332 172 C342 188 338 200 342 214 C346 230 334 246 326 256 "
    "C316 270 296 278 278 274 C268 272 260 266 254 258",
    "M262 186 C282 174 304 180 312 198 C318 214 312 232 298 242 C286 250 272 248 264 240",
    # eyes and brows
    "M160 204 Q172 193 186 204 Q172 211 160 204 Z",
    "M240 204 Q228 193 214 204 Q228 211 240 204 Z",
    "M158 190 Q172 180 188 188",
    "M242 190 Q228 180 212 188",
    # tilak
    "M188 160 Q200 182 212 160",
    "M200 166 L200 182",
    # trunk, curling to the viewer's right
    "M184 214 C178 262 186 306 212 336 C236 362 274 360 284 334 C292 314 272 298 256 308 "
    "C246 315 250 330 262 328",
    "M216 214 C220 252 230 286 250 304",
    "M185 240 Q200 247 217 240",
    "M187 262 Q201 270 221 262",
    "M193 284 Q207 292 229 282",
    # tusk
    "M232 236 C246 246 252 262 248 278 C240 268 232 256 228 244",
    # jaw / cheeks
    "M146 258 C152 280 166 292 182 290",
    "M254 258 C250 276 242 286 232 290",
    # necklace and lotus seat
    "M126 384 C150 360 176 356 200 368 C224 356 250 360 274 384",
    "M200 368 C188 388 188 404 200 418 C212 404 212 388 200 368 Z",
    "M168 372 C150 392 156 408 176 414",
    "M232 372 C250 392 244 408 224 414",
    "M110 418 Q200 436 290 418",
]
GANESH_DOTS = [(200, 26, 5), (174, 203, 3.2), (226, 203, 3.2), (200, 154, 3), (176, 128, 2.4), (224, 128, 2.4),
               (200, 120, 2.6)]


def ganesh(stroke=MARI_D, width=4.2, cls="gl"):
    paths = "".join(f'<path class="{cls}" pathLength="1" d="{d}"/>' for d in GANESH_PATHS)
    dots = "".join(f'<circle class="{cls}-dot" cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in GANESH_DOTS)
    return (f'<svg viewBox="0 0 400 440" width="400" height="440" fill="none" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{paths}'
            f'<g fill="{stroke}" stroke="none">{dots}</g></svg>')


# ------------------------------------------------------------------ small motifs
def rose(cx, cy, r, col=ROSE, light=ROSE_L, dark=ROSE_D, cls=""):
    """Top-down peony / rose: rings of round petals."""
    out = [f'<g class="{cls}" transform="translate({cx} {cy})">']
    for ring, (rr, n, c) in enumerate([(r, 8, light), (r * 0.72, 7, col), (r * 0.45, 6, dark)]):
        for i in range(n):
            a = (i / n) * math.tau + ring * 0.4
            px, py = math.cos(a) * rr * 0.55, math.sin(a) * rr * 0.55
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rr * 0.52:.1f}" fill="{c}"/>')
    out.append(f'<circle r="{r * 0.18:.1f}" fill="{MARI_L}"/></g>')
    return "".join(out)


def leaf(x, y, length, angle, col=LEAF2, vein=LEAF_D, width=0.32):
    w = length * width
    return (f'<g transform="translate({x} {y}) rotate({angle})">'
            f'<path d="M0 0 C{w:.1f} {-length * 0.3:.1f} {w:.1f} {-length * 0.7:.1f} 0 {-length:.1f} '
            f'C{-w:.1f} {-length * 0.7:.1f} {-w:.1f} {-length * 0.3:.1f} 0 0 Z" fill="{col}"/>'
            f'<path d="M0 0 L0 {-length * 0.92:.1f}" stroke="{vein}" stroke-width="2" opacity=".55"/></g>')


def banana_leaf(x, y, length, angle, col=LEAF1, dark=LEAF3):
    """Long banana leaf with torn slits, like the pichwai backdrops."""
    w = length * 0.2
    slits = "".join(
        f'<path d="M0 {-length * t:.1f} L{w * 0.95 * s:.1f} {-length * t - 18:.1f}" stroke="{dark}" '
        f'stroke-width="2.4" opacity=".55"/>'
        for t in (0.25, 0.4, 0.55, 0.7, 0.82) for s in (1, -1))
    return (f'<g transform="translate({x} {y}) rotate({angle})">'
            f'<path d="M0 0 C{w:.1f} {-length * 0.25:.1f} {w * 1.1:.1f} {-length * 0.75:.1f} 0 {-length:.1f} '
            f'C{-w * 1.1:.1f} {-length * 0.75:.1f} {-w:.1f} {-length * 0.25:.1f} 0 0 Z" fill="{col}"/>'
            f'{slits}<path d="M0 0 L0 {-length:.1f}" stroke="{dark}" stroke-width="4"/></g>')


def tree(x, y, scale, seed, cls=""):
    """Pichwai-style tree: a trunk and clusters of rounded foliage."""
    r = rng(seed)
    out = [f'<g class="{cls}" transform="translate({x} {y}) scale({scale})">',
           '<path d="M-14 0 C-10 -120 -8 -200 -4 -300 L6 -300 C10 -200 12 -120 16 0 Z" fill="#8a5a3c"/>',
           '<path d="M0 -180 C30 -210 50 -230 70 -260" stroke="#8a5a3c" stroke-width="10" fill="none"/>',
           '<path d="M0 -150 C-30 -180 -55 -200 -75 -230" stroke="#8a5a3c" stroke-width="10" fill="none"/>']
    for cx, cy, cr in [(0, -330, 95), (-80, -250, 70), (78, -275, 72), (-40, -410, 70), (45, -400, 72),
                       (0, -470, 55), (-95, -330, 55), (100, -350, 55)]:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{cr}" fill="{LEAF3}"/>')
    for cx, cy, cr in [(0, -330, 95), (-80, -250, 70), (78, -275, 72), (-40, -410, 70), (45, -400, 72),
                       (0, -470, 55), (-95, -330, 55), (100, -350, 55)]:
        for _ in range(9):
            a = r.uniform(0, math.tau)
            d = r.uniform(0, cr * 0.75)
            out.append(f'<circle cx="{cx + math.cos(a) * d:.0f}" cy="{cy + math.sin(a) * d:.0f}" '
                       f'r="{r.uniform(9, 15):.0f}" fill="{r.choice([LEAF1, LEAF2, "#b5d48f"])}"/>')
    out.append('</g>')
    return "".join(out)


def peacock(x, y, scale, flip=False, cls=""):
    """Side-on peacock perched with its tail trailing down."""
    sx = -scale if flip else scale
    eyes = "".join(
        f'<g transform="translate({ex} {ey}) rotate({ea})"><ellipse rx="15" ry="20" fill="{PEA_G}"/>'
        f'<ellipse rx="10" ry="14" fill="{MARI_L}"/><ellipse rx="7" ry="10" fill="{PEA_T}"/>'
        f'<ellipse rx="4" ry="6" fill="{PEA_D}"/></g>'
        for ex, ey, ea in [(-95, 70, 20), (-130, 125, 25), (-160, 185, 28), (-70, 130, 15), (-105, 195, 20),
                           (-135, 250, 24), (-80, 255, 12)])
    feathers = "".join(f'<path d="M-30 20 Q{-60 - i * 12} {120 + i * 25} {-90 - i * 16} {230 + i * 30}" '
                       f'stroke="{LEAF3}" stroke-width="3" fill="none" opacity=".7"/>' for i in range(5))
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({sx} {scale})">'
            f'<path d="M-20 10 C-80 60 -150 160 -190 300 C-140 310 -80 300 -40 270 C-30 180 -10 90 10 30 Z" '
            f'fill="{LEAF2}"/>{feathers}{eyes}'
            f'<path d="M-40 20 C-40 -20 0 -45 40 -35 C60 -30 70 -10 60 10 C40 40 -10 45 -40 20 Z" fill="{PEA_B}"/>'
            f'<path d="M-20 0 C0 -20 30 -25 50 -15" stroke="{PEA_T}" stroke-width="6" fill="none" opacity=".8"/>'
            f'<path d="M30 -30 C40 -70 45 -100 60 -120 C70 -130 85 -128 88 -115 C90 -100 75 -90 70 -70 '
            f'C66 -50 62 -30 55 -15 Z" fill="{PEA_B}"/>'
            f'<path d="M86 -116 L104 -110 L86 -104 Z" fill="{SAND_D}"/>'
            f'<circle cx="78" cy="-115" r="3.2" fill="#fff"/><circle cx="78.6" cy="-115" r="1.7" fill="#111"/>'
            f'<path d="M66 -128 L58 -152 M72 -130 L70 -156 M78 -129 L82 -153" stroke="{PEA_D}" stroke-width="2"/>'
            f'<circle cx="58" cy="-154" r="4" fill="{PEA_T}"/><circle cx="70" cy="-158" r="4" fill="{PEA_T}"/>'
            f'<circle cx="82" cy="-155" r="4" fill="{PEA_T}"/>'
            f'<path d="M0 40 L-6 62 M20 40 L22 62" stroke="{SAND_D}" stroke-width="4"/></g>')


def chhatri(x, y, s, col=CREAM, shade=CREAM_D):
    """Domed pavilion (chhatri)."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-110" y="0" width="220" height="26" fill="{shade}"/>'
            f'<rect x="-100" y="-160" width="20" height="160" fill="{col}"/><rect x="-35" y="-160" width="20" '
            f'height="160" fill="{col}"/><rect x="15" y="-160" width="20" height="160" fill="{col}"/>'
            f'<rect x="80" y="-160" width="20" height="160" fill="{col}"/>'
            f'<path d="M-80 -150 Q-57 -110 -35 -150 M-15 -150 Q0 -115 15 -150 M35 -150 Q57 -110 80 -150" '
            f'stroke="{shade}" stroke-width="5" fill="none"/>'
            f'<rect x="-125" y="-185" width="250" height="28" fill="{shade}"/>'
            f'<path d="M-105 -185 C-105 -290 105 -290 105 -185 Z" fill="{col}"/>'
            f'<path d="M-60 -195 C-60 -255 60 -255 60 -195" stroke="{shade}" stroke-width="4" fill="none"/>'
            f'<path d="M0 -268 L0 -310" stroke="{GOLD}" stroke-width="6"/><circle cy="-312" r="8" fill="{GOLD}"/>'
            f'</g>')


def balustrade(y, h=150):
    posts = "".join(f'<rect x="{x}" y="{y + 30}" width="22" height="{h - 50}" rx="10" fill="{CREAM}"/>'
                    for x in range(12, 1080, 44))
    return (f'<rect x="0" y="{y}" width="1080" height="30" fill="{CREAM}"/>'
            f'<rect x="0" y="{y + 26}" width="1080" height="6" fill="{CREAM_D}"/>{posts}'
            f'<rect x="0" y="{y + h - 24}" width="1080" height="24" fill="{CREAM_D}"/>')


def toran(y=0):
    """Marigold garland swags with mango leaves along the top edge."""
    out = []
    swags = [(0, 270), (270, 540), (540, 810), (810, 1080)]
    for a, b in swags:
        for i in range(25):
            t = i / 24
            x = a + (b - a) * t
            sag = math.sin(t * math.pi) * 95
            out.append(f'<circle cx="{x:.0f}" cy="{y + 40 + sag:.0f}" r="17" fill="{MARI if i % 2 else MARI_D}"/>'
                       f'<circle cx="{x:.0f}" cy="{y + 40 + sag:.0f}" r="7" fill="{MARI_L}" opacity=".7"/>')
    for x in (0, 270, 540, 810, 1080):
        for k, a in enumerate((-25, 0, 25)):
            out.append(leaf(x + a * 0.8, y + 50, 120, 180 + a, col=LEAF2 if k % 2 else LEAF3))
        out.append(f'<circle cx="{x}" cy="{y + 40}" r="24" fill="{ROSE_D}"/><circle cx="{x}" cy="{y + 40}" '
                   f'r="11" fill="{MARI_L}"/>')
        # hanging marigold string
        for j in range(5):
            out.append(f'<circle cx="{x}" cy="{y + 80 + j * 30}" r="13" fill="{MARI if j % 2 else MARI_D}"/>')
        out.append(f'<path d="M{x - 10} {y + 230} L{x} {y + 262} L{x + 10} {y + 230} Z" fill="{ROSE}"/>')
    return f'<g id="toran">{"".join(out)}</g>'


def hills():
    return (f'<path d="M0 1330 C160 1250 300 1290 420 1240 C560 1180 700 1260 840 1210 C950 1175 1020 1200 1080 1190 '
            f'L1080 1600 L0 1600 Z" fill="{HILL1}" opacity=".75"/>'
            f'<path d="M0 1400 C140 1340 260 1380 380 1340 C520 1300 640 1370 780 1330 C900 1300 1000 1330 1080 1310 '
            f'L1080 1600 L0 1600 Z" fill="{HILL2}" opacity=".8"/>'
            f'<path d="M0 1470 C180 1430 320 1460 470 1430 C620 1400 760 1450 900 1420 C980 1405 1040 1415 1080 1410 '
            f'L1080 1600 L0 1600 Z" fill="{HILL3}" opacity=".85"/>')


def clouds():
    out = []
    for cx, cy, s, o in [(200, 520, 1.0, .75), (860, 430, 1.25, .7), (560, 760, .8, .55), (120, 940, .9, .5),
                         (930, 1010, .85, .5)]:
        out.append(f'<g class="cloud" transform="translate({cx} {cy}) scale({s})" opacity="{o}">'
                   f'<ellipse rx="120" ry="30" fill="#fff"/><ellipse cx="-40" cy="-20" rx="60" ry="34" fill="#fff"/>'
                   f'<ellipse cx="35" cy="-26" rx="70" ry="40" fill="#fff"/></g>')
    return "".join(out)


def bird(cls, s=1.0):
    return (f'<g class="{cls}"><path d="M0 0 Q12 -12 24 0 Q36 -12 48 0" transform="scale({s})" stroke="#2c3a4f" '
            f'stroke-width="3.5" fill="none" stroke-linecap="round"/></g>')


def background():
    """The full persistent scene, back to front, as one SVG."""
    trees_l = tree(60, 1650, 0.9, 3, "tree-l") + tree(165, 1710, 0.72, 4, "tree-l2")
    trees_r = tree(1020, 1650, 0.9, 5, "tree-r") + tree(915, 1710, 0.72, 6, "tree-r2")
    bananas = (banana_leaf(0, 1560, 380, 8) + banana_leaf(30, 1600, 330, 32, col=LEAF2) +
               banana_leaf(1080, 1560, 380, -8) + banana_leaf(1050, 1600, 330, -32, col=LEAF2))
    roses = "".join(rose(x, y, r, cls="bg-rose") for x, y, r in
                    [(60, 1300, 34), (130, 1385, 26), (1020, 1300, 34), (950, 1385, 26), (40, 1560, 30),
                     (1040, 1560, 30)])
    return (f'<svg id="bgsvg" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY1}"/>'
            f'<stop offset=".55" stop-color="{SKY2}"/><stop offset="1" stop-color="{SKY3}"/></linearGradient>'
            f'<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6d8" '
            f'stop-opacity=".95"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>'
            f'</defs><rect width="1080" height="1920" fill="url(#sky)"/>'
            f'<g id="sunglow"><circle cx="540" cy="820" r="520" fill="url(#sun)"/></g>'
            f'<g id="clouds">{clouds()}</g>{hills()}'
            f'<g id="chhatri-l">{chhatri(190, 1560, 0.95)}</g><g id="chhatri-r">{chhatri(900, 1580, 0.7)}</g>'
            f'{balustrade(1560)}<rect x="0" y="1710" width="1080" height="210" fill="#b9cf8f"/>'
            f'<rect x="0" y="1710" width="1080" height="14" fill="#9fbd76"/>'
            f'</svg>')


def foreground():
    """Trees, flowers and peacocks that sit in front of the text arch."""
    trees_l = tree(55, 1700, 0.8, 3, "tree-l") + tree(160, 1740, 0.62, 4, "tree-l2")
    trees_r = tree(1025, 1700, 0.8, 5, "tree-r") + tree(920, 1740, 0.62, 6, "tree-r2")
    bananas = (banana_leaf(0, 1590, 300, 8) + banana_leaf(30, 1620, 270, 32, col=LEAF2) +
               banana_leaf(1080, 1590, 300, -8) + banana_leaf(1050, 1620, 270, -32, col=LEAF2))
    roses = "".join(rose(x, y, r, cls="bg-rose") for x, y, r in
                    [(50, 1420, 30), (120, 1490, 24), (1030, 1420, 30), (960, 1490, 24), (40, 1580, 28),
                     (1040, 1580, 28)])
    return (f'<svg id="fgsvg" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<g id="trees-l">{trees_l}</g><g id="trees-r">{trees_r}</g>'
            f'<g id="bananas">{bananas}</g><g id="roses">{roses}</g>'
            f'<g id="pea-l">{peacock(215, 1575, 0.9)}</g><g id="pea-r">{peacock(870, 1580, 0.82, flip=True)}</g>'
            f'{toran()}</svg>')


# ------------------------------------------------------------------ the palace doors (intro)
def door_panel(side):
    """One door leaf, 540x1920, drawn so the arch meets in the middle."""
    w = 540
    inner_edge = w if side == "l" else 0
    outer = 0 if side == "l" else w
    sgn = 1 if side == "l" else -1
    # arch top: the two leaves together form one pointed Mughal arch
    arch = (f'M{outer} 1920 L{outer} 520 C{outer} 360 {outer + sgn * 260} 300 {inner_edge} 180 '
            f'L{inner_edge} 1920 Z')
    studs = "".join(f'<circle cx="{outer + sgn * x}" cy="{y}" r="7" fill="{GOLD}"/>'
                    for y in range(640, 1800, 110) for x in (95, 270, 445))
    panels = "".join(
        f'<rect x="{min(outer + sgn * 70, outer + sgn * 470)}" y="{y}" width="400" height="{h}" rx="16" '
        f'fill="none" stroke="{SAND_D}" stroke-width="6"/>'
        for y, h in [(600, 520), (1170, 560)])
    lattice = "".join(
        f'<path d="M{outer + sgn * (110 + i * 64)} 640 l{sgn * 32} 40 l{-sgn * 32} 40 l{-sgn * 32} -40 Z" '
        f'fill="none" stroke="{SAND_D}" stroke-width="3" opacity=".7"/>' for i in range(6))
    ring_x = inner_edge - sgn * 60
    return (f'<svg viewBox="0 0 {w} 1920" width="{w}" height="1920">'
            f'<path d="{arch}" fill="#f6c99a"/><path d="{arch}" fill="none" stroke="{SAND_D}" stroke-width="10"/>'
            f'{panels}{lattice}{studs}'
            f'<circle cx="{ring_x}" cy="1150" r="30" fill="none" stroke="{GOLD_D}" stroke-width="9"/>'
            f'<circle cx="{ring_x}" cy="1118" r="12" fill="{GOLD_D}"/></svg>')


def door_frame():
    """Ornate sandstone arch around the doors, with a jaali border and roses."""
    jaali = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{SAND_D}" stroke-width="3"/>'
                    for x in (30, 1050) for y in range(240, 1900, 34))
    flowers = "".join(rose(x, y, r) for x, y, r in [(120, 300, 40), (960, 300, 40), (60, 420, 30), (1020, 420, 30)])
    vines = (leaf(150, 340, 90, -60) + leaf(930, 340, 90, 60) + leaf(95, 470, 80, -120) +
             leaf(985, 470, 80, 120))
    return (f'<svg viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<path fill-rule="evenodd" fill="{SAND2}" d="M0 0 H1080 V1920 H0 Z '
            f'M60 1920 L60 520 C60 360 320 300 540 170 C760 300 1020 360 1020 520 L1020 1920 Z"/>'
            f'<path d="M60 1920 L60 520 C60 360 320 300 540 170 C760 300 1020 360 1020 520 L1020 1920" '
            f'fill="none" stroke="{GOLD}" stroke-width="8"/>'
            f'<path d="M0 120 Q540 40 1080 120" stroke="{SAND_D}" stroke-width="6" fill="none"/>'
            f'{jaali}{vines}{flowers}</svg>')


# ------------------------------------------------------------------ decorative bits for the cards
def divider(width=520, col=GOLD):
    h = width / 2
    return (f'<svg viewBox="0 0 {width} 40" width="{width}" height="40" fill="none" stroke="{col}" '
            f'stroke-width="2.4" stroke-linecap="round">'
            f'<path class="dv" pathLength="1" d="M{h - 40} 20 L20 20"/><path class="dv" pathLength="1" '
            f'd="M{h + 40} 20 L{width - 20} 20"/>'
            f'<path d="M{h} 6 L{h + 14} 20 L{h} 34 L{h - 14} 20 Z" fill="{col}"/>'
            f'<circle cx="{h - 28}" cy="20" r="4" fill="{col}"/><circle cx="{h + 28}" cy="20" r="4" fill="{col}"/>'
            f'</svg>')


def rings(size=170):
    """Two interlocked engagement rings with a solitaire, drawn as strokes."""
    return (f'<svg viewBox="0 0 220 170" width="{size}" height="{size * 170 / 220:.0f}" fill="none" '
            f'stroke="{GOLD}" stroke-width="7" stroke-linecap="round">'
            f'<circle class="rg" pathLength="1" cx="85" cy="105" r="50"/>'
            f'<circle class="rg" pathLength="1" cx="140" cy="105" r="50"/>'
            f'<path class="rg-gem" d="M70 46 L85 30 L100 46 L85 60 Z" fill="#dff3ff" stroke="{GOLD_D}" stroke-width="3"/>'
            f'<path class="rg-gem" d="M85 30 L85 60 M70 46 L100 46" stroke="#9ccbe0" stroke-width="2"/></svg>')


def wreath(seed, size=520):
    """Floral ring for a monogram: a thin gold circle with roses and leaves around it."""
    r = rng(seed)
    c = size / 2
    rad = size * 0.4
    parts = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
             f'<circle class="wr" pathLength="1" cx="{c}" cy="{c}" r="{rad}" fill="none" stroke="{GOLD}" '
             f'stroke-width="4"/>'
             f'<circle class="wr" pathLength="1" cx="{c}" cy="{c}" r="{rad - 14}" fill="none" stroke="{GOLD}" '
             f'stroke-width="1.6" opacity=".7"/>']
    # leaves hugging the ring on the lower left and upper right arcs
    for a0, a1 in [(110, 250), (290, 410)]:
        for i in range(9):
            a = math.radians(a0 + (a1 - a0) * i / 8)
            x, y = c + math.cos(a) * rad, c + math.sin(a) * rad
            ang = math.degrees(a) + r.choice((60, 120))
            parts.append(f'<g class="wr-leaf">{leaf(round(x), round(y), r.uniform(46, 62), round(ang), col=r.choice([LEAF1, LEAF2, LEAF3]))}</g>')
    for deg, rr in [(225, 46), (200, 30), (250, 30), (45, 46), (20, 30), (70, 30)]:
        a = math.radians(deg)
        parts.append(rose(round(c + math.cos(a) * rad), round(c + math.sin(a) * rad), rr, cls="wr-rose"))
    parts.append('</svg>')
    return "".join(parts)


def pin(size=70):
    return (f'<svg viewBox="0 0 60 80" width="{size}" height="{size * 80 / 60:.0f}">'
            f'<path d="M30 78 C30 78 4 46 4 28 A26 26 0 0 1 56 28 C56 46 30 78 30 78 Z" fill="{ROSE_D}"/>'
            f'<circle cx="30" cy="28" r="10" fill="#fff"/></svg>')


def diya(size=110):
    return (f'<svg viewBox="0 0 120 110" width="{size}" height="{size * 110 / 120:.0f}">'
            f'<g class="flame"><path d="M60 8 C72 30 74 44 60 56 C46 44 48 30 60 8 Z" fill="{MARI_L}"/>'
            f'<path d="M60 26 C66 38 66 46 60 52 C54 46 54 38 60 26 Z" fill="#fff4c2"/></g>'
            f'<path d="M8 64 Q60 70 112 64 C104 96 80 106 60 106 C40 106 16 96 8 64 Z" fill="{MARI_D}"/>'
            f'<path d="M8 64 Q60 76 112 64" stroke="{GOLD_D}" stroke-width="4" fill="none"/>'
            f'<path d="M30 84 Q60 92 90 84" stroke="{MARI_L}" stroke-width="3" fill="none"/></svg>')


def petal_shapes():
    return [f'<svg viewBox="0 0 30 40" width="30" height="40"><path d="M15 0 C30 12 26 34 15 40 C4 34 0 12 15 0 Z" '
            f'fill="{c}"/></svg>' for c in (ROSE_L, ROSE, "#f8c9d6", MARI_L, "#fde2e4")]


def sparkle(col="#fff8dc"):
    return (f'<svg viewBox="0 0 40 40" width="40" height="40"><path d="M20 0 L24 16 L40 20 L24 24 L20 40 L16 24 '
            f'L0 20 L16 16 Z" fill="{col}"/></svg>')


# ------------------------------------------------------------------ palace and hill vignettes
def palace(x, y, s):
    """Palace facade: arcaded base, a big central dome and corner chhatris."""
    arches = "".join(f'<path d="M{ax} 0 L{ax} -70 C{ax} -96 {ax + 44} -96 {ax + 44} -70 L{ax + 44} 0 Z" fill="#e7d6bd"/>'
                     for ax in range(-170, 171, 68))
    upper = "".join(f'<path d="M{ax} -150 L{ax} -186 C{ax} -202 {ax + 28} -202 {ax + 28} -186 L{ax + 28} -150 Z" '
                    f'fill="#e7d6bd"/>' for ax in range(-120, 121, 52))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-200" y="-130" width="400" height="130" fill="{CREAM}"/>{arches}'
            f'<rect x="-210" y="-138" width="420" height="14" fill="{CREAM_D}"/>'
            f'<rect x="-150" y="-215" width="300" height="80" fill="{CREAM}"/>{upper}'
            f'<rect x="-160" y="-222" width="320" height="12" fill="{CREAM_D}"/>'
            f'<path d="M-80 -222 C-90 -320 90 -320 80 -222 Z" fill="{CREAM}"/>'
            f'<path d="M-40 -232 C-44 -290 44 -290 40 -232" stroke="{CREAM_D}" stroke-width="4" fill="none"/>'
            f'<path d="M0 -300 L0 -336" stroke="{GOLD}" stroke-width="5"/><circle cy="-338" r="7" fill="{GOLD}"/>'
            f'{chhatri(-185, -135, .42)}{chhatri(185, -135, .42)}</g>')


def vignette(vid, w, h, inner, sun=True):
    """A Mughal-arch window (w x h, origin top-left) painted with sky, hills, palace and a garden floor.
    `inner` is drawn on top, in the same coordinates, clipped to the window."""
    cx = w / 2
    arch = (f'M0 {h} L0 {h * .28:.0f} C0 {h * .13:.0f} {w * .3:.0f} {h * .07:.0f} {cx:.0f} 0 '
            f'C{w * .7:.0f} {h * .07:.0f} {w} {h * .13:.0f} {w} {h * .28:.0f} L{w} {h} Z')
    gy = h * .78
    sunel = (f'<circle cx="{cx:.0f}" cy="{h * .38:.0f}" r="{w * .45:.0f}" fill="url(#vsun-{vid})"/>' if sun else "")
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs><clipPath id="vclip-{vid}"><path d="{arch}"/></clipPath>'
            f'<linearGradient id="vsky-{vid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe2ee"/>'
            f'<stop offset=".7" stop-color="#fbeedd"/></linearGradient>'
            f'<radialGradient id="vsun-{vid}"><stop offset="0" stop-color="#fff3cf"/><stop offset="1" '
            f'stop-color="#fff3cf" stop-opacity="0"/></radialGradient></defs>'
            f'<g clip-path="url(#vclip-{vid})">'
            f'<rect width="{w}" height="{h}" fill="url(#vsky-{vid})"/>{sunel}'
            f'<path d="M0 {gy - 120:.0f} C{w * .2:.0f} {gy - 190:.0f} {w * .4:.0f} {gy - 140:.0f} {w * .55:.0f} '
            f'{gy - 200:.0f} C{w * .7:.0f} {gy - 250:.0f} {w * .85:.0f} {gy - 160:.0f} {w} {gy - 190:.0f} L{w} {h} L0 {h} Z" '
            f'fill="{HILL1}"/>'
            f'<path d="M0 {gy - 60:.0f} C{w * .25:.0f} {gy - 120:.0f} {w * .5:.0f} {gy - 70:.0f} {w * .7:.0f} '
            f'{gy - 110:.0f} C{w * .85:.0f} {gy - 135:.0f} {w * .95:.0f} {gy - 90:.0f} {w} {gy - 100:.0f} L{w} {h} '
            f'L0 {h} Z" fill="{HILL2}"/>'
            f'{palace(cx, gy - 30, w / 900)}'
            f'<rect x="0" y="{gy - 34:.0f}" width="{w}" height="18" fill="{CREAM_D}"/>'
            f'<rect x="0" y="{gy - 16:.0f}" width="{w}" height="{h - gy + 16:.0f}" fill="#f3e6cf"/>'
            f'<path d="M0 {gy + 40:.0f} L{w} {gy + 40:.0f}" stroke="{SAND2}" stroke-width="3" opacity=".6"/>'
            f'{tree(40, gy - 10, .42, 21)}{tree(w - 40, gy - 10, .42, 22)}'
            f'{inner}</g>'
            f'<path d="{arch}" fill="none" stroke="{GOLD}" stroke-width="6"/>'
            f'<path d="{arch}" fill="none" stroke="#fff6e4" stroke-width="2" transform="translate({w * .02:.1f} '
            f'{h * .015:.1f}) scale(.96 .97)"/></svg>')
