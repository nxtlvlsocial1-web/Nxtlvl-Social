"""Calligraphic Ganesh ji and the faceless couple illustrations (our own drawing).

Brush strokes are filled outlines built from a centre line and a width profile, so they taper like
a pen stroke instead of having a constant SVG stroke width.
"""
import math
import re

# ------------------------------------------------------------------ brush strokes
def _cubics(d):
    nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
    p0 = (nums[0], nums[1])
    out, i = [], 2
    while i + 5 < len(nums) + 1 and i + 6 <= len(nums):
        c1, c2, p3 = (nums[i], nums[i + 1]), (nums[i + 2], nums[i + 3]), (nums[i + 4], nums[i + 5])
        out.append((p0, c1, c2, p3))
        p0 = p3
        i += 6
    return out


def _bez(seg, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = seg
    u = 1 - t
    x = u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3
    y = u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3
    return x, y


def brush(d, wmax, wmin=1.2, shape="swell"):
    """Filled outline for a cubic centre line. shape: swell (thin-thick-thin) or taper (thick to thin)."""
    segs = _cubics(d)
    pts = []
    for s in segs:
        for k in range(40):
            pts.append(_bez(s, k / 40))
    pts.append(segs[-1][3])
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        t = i / (n - 1)
        if shape == "taper":
            w = wmin + (wmax - wmin) * (1 - t) ** 0.8 * min(1, t * 12 + .35)
        else:
            w = wmin + (wmax - wmin) * math.sin(math.pi * t) ** 0.65
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    ring = left + right[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ring) + " Z"


# centre lines for a seated Ganesh in a 400x500 box
GANESH = [
    ("M168 72 C170 40 230 40 232 72", 7, "swell"),                          # crown dome
    ("M160 82 C185 72 215 72 240 82", 4.5, "swell"),                        # crown band
    ("M200 38 C192 30 197 18 200 12 C203 18 208 30 200 38", 3.5, "swell"),  # crown jewel
    ("M156 94 C175 84 225 84 244 94", 3.5, "swell"),                        # forehead
    ("M158 92 C118 58 66 70 64 122 C62 162 90 190 110 205 C122 214 121 230 108 240", 11, "swell"),
    ("M242 92 C282 58 336 72 338 124 C340 165 310 190 292 202 C280 210 282 226 296 234", 11, "swell"),
    ("M140 122 C122 114 106 126 110 142", 3.2, "swell"),
    ("M260 122 C278 114 294 126 290 142", 3.2, "swell"),
    ("M300 140 C312 132 324 142 318 154 C312 164 298 158 302 148", 2.6, "swell"),
    ("M100 140 C88 132 76 142 82 154 C88 164 102 158 98 148", 2.6, "swell"),
    ("M160 132 C170 121 186 123 192 133 C184 139 168 139 160 132", 2.6, "swell"),
    ("M208 133 C214 123 230 121 240 132 C232 139 216 139 208 133", 2.6, "swell"),
    ("M200 112 C196 160 192 210 198 255 C204 300 236 330 270 322 C300 314 306 280 284 268 "
     "C266 258 252 276 266 290 C276 300 292 292 290 280", 12, "taper"),     # trunk
    ("M216 142 C214 186 216 226 228 260", 4, "swell"),
    ("M236 192 C252 198 258 214 250 230", 4.5, "swell"),                    # tusk
    ("M112 240 C96 272 92 312 104 348", 8, "swell"),                        # body left
    ("M118 302 C132 288 150 292 152 308 C154 322 140 332 128 328", 4.5, "swell"),  # blessing hand
    ("M300 234 C330 262 345 302 335 338", 8, "swell"),                      # body right
    ("M68 382 C58 422 100 447 160 442 C220 438 280 427 325 402 C355 384 352 347 325 337", 12, "swell"),  # lap
    ("M150 397 C190 382 240 382 285 397", 4, "swell"),
    ("M246 432 C238 457 246 482 268 490 C290 496 312 482 306 462 C302 448 290 442 280 447", 7, "swell"),  # foot
    ("M68 382 C80 362 100 354 120 358", 4, "swell"),
]


def ganesh_brush(col="#e8701a", cls="gb"):
    paths = "".join(f'<path class="{cls}" d="{brush(d, w, shape=s)}"/>' for d, w, s in GANESH)
    return (f'<svg viewBox="0 0 400 500" width="400" height="500"><g fill="{col}">{paths}'
            f'<circle cx="200" cy="108" r="5"/><circle cx="176" cy="131" r="2.6"/>'
            f'<circle cx="224" cy="131" r="2.6"/></g></svg>')


# ------------------------------------------------------------------ faceless couples
SKIN, SKIN_D = "#e2a988", "#c98b6b"
HAIR = "#2b1d1a"


def groom(pal, flip=False):
    """Standing groom in a sherwani, ~520 tall, feet at y=0, centred on x=0. Faces right unless flipped."""
    coat, trim, stole, pants, shoe = pal
    s = -1 if flip else 1
    buttons = "".join(f'<circle cx="{4 * s}" cy="{-420 + i * 26}" r="3.2" fill="{trim}"/>' for i in range(8))
    return (f'<g transform="scale({s} 1)">'
            # legs
            f'<path d="M-30 -150 L-34 -12 L-14 -12 L-6 -150 Z" fill="{pants}"/>'
            f'<path d="M6 -150 L14 -12 L34 -12 L30 -150 Z" fill="{pants}"/>'
            f'<path d="M-40 -14 C-40 -2 -10 0 -10 -8 L-12 -16 Z" fill="{shoe}"/>'
            f'<path d="M12 -16 L10 -8 C10 0 44 -2 42 -14 Z" fill="{shoe}"/>'
            # coat (knee length, slight flare)
            f'<path d="M-48 -430 C-60 -330 -66 -230 -64 -150 L64 -150 C66 -230 60 -330 48 -430 '
            f'C30 -446 -30 -446 -48 -430 Z" fill="{coat}"/>'
            f'<path d="M-64 -158 L64 -158 L64 -146 L-64 -146 Z" fill="{trim}"/>'
            f'<path d="M0 -440 L0 -150" stroke="{trim}" stroke-width="3" opacity=".8"/>{buttons}'
            # stole over the left shoulder
            f'<path d="M-46 -432 C-20 -380 10 -300 30 -200 L48 -204 C34 -300 4 -390 -26 -440 Z" fill="{stole}" '
            f'opacity=".95"/>'
            # arms: back arm down, front arm reaching forward to hold hands
            f'<path d="M-50 -420 C-70 -360 -74 -300 -70 -250 L-52 -248 C-52 -300 -44 -360 -36 -410 Z" fill="{coat}"/>'
            f'<circle cx="-61" cy="-242" r="11" fill="{SKIN}"/>'
            f'<path d="M44 -424 C66 -380 78 -330 88 -286 L106 -270 L92 -262 L72 -290 C60 -330 46 -370 34 -404 Z" '
            f'fill="{coat}"/>'
            f'<circle cx="100" cy="-268" r="11" fill="{SKIN}"/>'
            # neck, collar, head, hair (no face drawn)
            f'<rect x="-11" y="-470" width="22" height="34" fill="{SKIN_D}"/>'
            f'<path d="M-22 -440 L0 -428 L22 -440 L22 -432 L0 -420 L-22 -432 Z" fill="{trim}"/>'
            f'<ellipse cx="2" cy="-498" rx="34" ry="40" fill="{SKIN}"/>'
            f'<path d="M-34 -500 C-38 -546 10 -556 34 -530 C42 -520 40 -506 36 -498 C30 -520 0 -526 -20 -514 '
            f'C-28 -508 -32 -502 -34 -500 Z" fill="{HAIR}"/>'
            f'<path d="M-34 -500 C-36 -486 -34 -474 -28 -466 L-26 -496 Z" fill="{HAIR}"/>'
            f'<ellipse cx="-30" cy="-494" rx="6" ry="10" fill="{SKIN_D}"/></g>')


def bride(pal, flip=False):
    """Standing bride in a lehenga with a dupatta, ~480 tall, feet at y=0. Faces left unless flipped."""
    skirt, border, blouse, dupatta, jewel = pal
    s = -1 if flip else 1
    motifs = "".join(f'<circle cx="{x * (1 - .12 * row)}" cy="{-52 - row * 26}" r="4.5" fill="{border}" opacity=".9"/>'
                     for row in (0, 1) for x in range(-108, 112, 24))
    return (f'<g transform="scale({s} 1)">'
            # lehenga: flared skirt to the ground with a border
            f'<path d="M-40 -270 C-70 -200 -112 -90 -130 -4 C-60 8 60 8 130 -4 C112 -90 70 -200 40 -270 Z" '
            f'fill="{skirt}"/>'
            f'<path d="M-130 -4 C-60 8 60 8 130 -4 L126 -34 C60 -24 -60 -24 -126 -34 Z" fill="{border}"/>'
            f'{motifs}'
            f'<path d="M-40 -270 C-20 -262 20 -262 40 -270 L40 -258 C20 -250 -20 -250 -40 -258 Z" fill="{border}"/>'
            # blouse and midriff
            f'<path d="M-34 -380 C-44 -330 -44 -300 -40 -270 L40 -270 C44 -300 44 -330 34 -380 Z" fill="{SKIN}"/>'
            f'<path d="M-36 -386 C-44 -350 -42 -326 -38 -310 L38 -310 C42 -326 44 -350 36 -386 '
            f'C20 -398 -20 -398 -36 -386 Z" fill="{blouse}"/>'
            # arms: front arm reaching towards the groom
            f'<path d="M-34 -380 C-56 -340 -72 -300 -86 -270 L-74 -262 C-60 -292 -44 -326 -26 -360 Z" fill="{SKIN}"/>'
            f'<path d="M-82 -280 L-70 -272" stroke="{jewel}" stroke-width="6"/>'
            f'<path d="M34 -380 C46 -330 50 -290 46 -250 L34 -250 C36 -290 32 -330 24 -364 Z" fill="{SKIN}"/>'
            f'<path d="M34 -262 L47 -262" stroke="{jewel}" stroke-width="6"/>'
            # neck, head, hair bun with flowers, maang tikka (no face drawn)
            f'<rect x="-10" y="-418" width="20" height="34" fill="{SKIN_D}"/>'
            f'<path d="M-24 -392 Q0 -372 24 -392" stroke="{jewel}" stroke-width="5" fill="none"/>'
            f'<ellipse cx="-2" cy="-446" rx="30" ry="36" fill="{SKIN}"/>'
            f'<path d="M30 -446 C34 -488 -6 -500 -28 -476 C-36 -466 -34 -454 -32 -446 C-22 -466 6 -472 24 -458 Z" '
            f'fill="{HAIR}"/>'
            f'<circle cx="34" cy="-450" r="20" fill="{HAIR}"/>'
            f'<circle cx="46" cy="-462" r="5" fill="#fff"/><circle cx="50" cy="-448" r="5" fill="#fff"/>'
            f'<circle cx="44" cy="-436" r="5" fill="#fff"/>'
            f'<path d="M-2 -480 L-2 -466" stroke="{jewel}" stroke-width="2.5"/><circle cx="-2" cy="-462" r="4.5" '
            f'fill="{jewel}"/>'
            f'<circle cx="24" cy="-432" r="5" fill="{jewel}"/>'
            # sheer dupatta over head and back
            f'<path d="M-30 -470 C-10 -500 36 -496 52 -470 C70 -420 76 -330 70 -200 C66 -150 60 -120 52 -96 '
            f'L30 -100 C42 -200 44 -320 30 -420 C20 -450 -6 -460 -30 -456 Z" fill="{dupatta}" opacity=".55"/>'
            f'<path d="M52 -96 L30 -100" stroke="{border}" stroke-width="5"/></g>')


COUPLE1 = {"groom": ("#f6ead2", "#c9973f", "#f2b8a0", "#efe3cc", "#a8782c"),
           "bride": ("#f4a7b9", "#d4a24c", "#e98aa2", "#fbd3dc", "#d4a24c")}
COUPLE2 = {"groom": ("#a9c8b0", "#c9973f", "#f6ead2", "#efe9dc", "#7a5a2a"),
           "bride": ("#c8a2d8", "#d4a24c", "#b07fc6", "#ecd8f4", "#d4a24c")}


def couple(pal, cls):
    """Groom on the left, bride on the right, holding hands between them. Origin at their feet."""
    return (f'<g class="{cls}">'
            f'<g class="{cls}-g"><g transform="translate(-95 0)">{groom(pal["groom"])}</g></g>'
            f'<g class="{cls}-b"><g transform="translate(95 0)">{bride(pal["bride"])}</g></g>'
            f'<circle class="{cls}-h" cx="10" cy="-268" r="13" fill="{SKIN}"/></g>')
