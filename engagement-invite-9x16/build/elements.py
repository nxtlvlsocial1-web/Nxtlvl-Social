"""Royal motifs for the invite (our own drawing, styled after the client's references): decorated
elephants, a line-art chhatri pavilion, a flower bouquet, watercolour arch florals and the
ring-exchange hands.
"""
import math
import random

import art

MAROON_E, MAROON_E2 = "#5b1d36", "#7a2a4a"
MAGENTA, TEAL, GOLD, GOLD_L = "#c2185b", "#2a9d8f", "#c9973f", "#f2c96b"
BLUE, BLUE_D, PEACH, PEACH_D, PINK = "#9db4cf", "#6f8fb0", "#f6c1a1", "#e9967a", "#f4a7b9"
LEAF_T, LEAF_T2 = "#7aa39a", "#4f7f74"


# ------------------------------------------------------------------ decorated elephant
def elephant(flip=False):
    """Side-on elephant with raised trunk and a jhool (caparison); 300 x 250, feet on y=0, faces right."""
    s = -1 if flip else 1
    checks = "".join(
        f'<rect x="{-92 + i * 22}" y="{-178 + j * 22}" width="14" height="14" rx="3" '
        f'fill="{[GOLD_L, PINK, "#fff"][(i + j) % 3]}" opacity=".9"/>' for i in range(6) for j in range(3))
    bells = "".join(f'<circle cx="{-96 + i * 20}" cy="-106" r="5" fill="{GOLD}"/>' for i in range(8))
    legs = "".join(f'<rect x="{x}" y="-78" width="34" height="78" rx="10" fill="{MAROON_E}"/>'
                   f'<rect x="{x - 2}" y="-22" width="38" height="8" rx="3" fill="{GOLD}"/>'
                   for x in (-104, -62, 30, 70))
    return (f'<g transform="scale({s} 1)">'
            f'{legs}'
            f'<path d="M-130 -110 C-140 -190 -70 -230 10 -222 C80 -216 120 -180 118 -110 C116 -70 80 -60 0 -62 '
            f'C-80 -62 -126 -70 -130 -110 Z" fill="{MAROON_E2}"/>'
            f'<path d="M-140 -120 C-150 -110 -152 -96 -146 -84" stroke="{MAROON_E}" stroke-width="7" fill="none"/>'
            # head, ear, trunk raised in a curl, tusk
            f'<path d="M84 -200 C120 -236 176 -226 186 -186 C194 -156 186 -120 170 -100 C160 -84 150 -84 140 -96 '
            f'C126 -112 104 -130 92 -150 Z" fill="{MAROON_E2}"/>'
            f'<path d="M172 -112 C202 -140 214 -192 236 -224 C246 -238 264 -234 260 -218 C256 -206 242 -208 240 -216" '
            f'stroke="{MAROON_E2}" stroke-width="24" stroke-linecap="round" fill="none"/>'
            f'<path d="M160 -104 C176 -92 194 -94 206 -106" stroke="#fff6e6" stroke-width="8" stroke-linecap="round" '
            f'fill="none"/>'
            f'<path d="M86 -196 C60 -190 50 -150 62 -120 C74 -96 100 -98 110 -118 C118 -140 112 -176 86 -196 Z" '
            f'fill="{MAROON_E}"/>'
            f'<circle cx="158" cy="-176" r="5" fill="#fff"/><circle cx="159" cy="-176" r="2.6" fill="#1b0b12"/>'
            # forehead cloth (mukhpatta)
            f'<path d="M150 -226 C170 -224 186 -206 188 -186 L170 -160 C160 -176 150 -196 140 -214 Z" fill="{GOLD}"/>'
            f'<circle cx="170" cy="-196" r="7" fill="{MAGENTA}"/><circle cx="170" cy="-174" r="5" fill="{TEAL}"/>'
            # jhool over the back
            f'<path d="M-108 -214 C-60 -232 40 -232 70 -214 L66 -110 C30 -96 -70 -96 -104 -110 Z" fill="{MAGENTA}"/>'
            f'<path d="M-100 -204 C-56 -220 34 -220 62 -204 L58 -122 C26 -110 -64 -110 -96 -122 Z" fill="none" '
            f'stroke="{TEAL}" stroke-width="6"/>'
            f'{checks}{bells}'
            f'<path d="M-108 -214 C-60 -232 40 -232 70 -214" stroke="{GOLD}" stroke-width="7" fill="none"/>'
            f'<path d="M-104 -110 C-70 -96 30 -96 66 -110" stroke="{GOLD}" stroke-width="6" fill="none"/>'
            f'<path d="M-20 -232 L-20 -250 M-6 -232 L-4 -252" stroke="{GOLD}" stroke-width="4"/>'
            f'</g>')


# ------------------------------------------------------------------ line-art chhatri pavilion
def pavilion(inner=""):
    """Gold line pavilion, 440 x 540, origin top-left. `inner` sits inside the scalloped arch (centre 220, 395)."""
    c = GOLD
    spires = "".join(
        f'<path d="M{x} {y0} L{x} {y0 - 30} M{x - 9} {y0 - 6} L{x} {y0 - 44} L{x + 9} {y0 - 6} Z" fill="none"/>'
        f'<circle cx="{x}" cy="{y0 - 48}" r="3.5" fill="{c}"/>' for x, y0 in ((160, 96), (220, 82), (280, 96)))
    domes = "".join(f'<path d="M{x - 20} {y0 + 30} C{x - 20} {y0} {x + 20} {y0} {x + 20} {y0 + 30}"/>'
                    for x, y0 in ((160, 96), (220, 82), (280, 96)))
    roof_lines = "".join(f'<path d="M{220 + k * 22} 126 L{220 + k * 34} 210"/>' for k in range(-5, 6))
    diamonds = "".join(f'<path d="M{x} 226 L{x + 10} 238 L{x} 250 L{x - 10} 238 Z"/>' for x in range(80, 370, 32))
    scallop = ("M110 540 L110 330 C110 320 120 312 128 308 C130 290 150 280 162 286 C168 268 190 262 200 270 "
               "C206 254 234 254 240 270 C250 262 272 268 278 286 C290 280 310 290 312 308 C320 312 330 320 330 330 "
               "L330 540")
    return (f'<svg viewBox="0 0 440 560" width="440" height="560" fill="none" stroke="{c}" stroke-width="3.2" '
            f'stroke-linejoin="round" stroke-linecap="round">'
            f'<g class="pv-draw">{spires}{domes}'
            f'<path d="M120 126 L320 126 L380 210 L60 210 Z"/>{roof_lines}'
            f'<rect x="54" y="212" width="332" height="52"/>{diamonds}'
            f'<path d="M70 264 L70 540 M370 264 L370 540 M86 264 L86 540 M354 264 L354 540"/>'
            f'<path d="{scallop}"/></g>'
            f'<g stroke="none">{inner}</g></svg>')


# ------------------------------------------------------------------ flowers
def flower5(cx, cy, r, col, centre="#e36f4c", cls=""):
    petals = "".join(
        f'<ellipse cx="{cx + math.cos(a) * r * .55:.1f}" cy="{cy + math.sin(a) * r * .55:.1f}" rx="{r * .5:.1f}" '
        f'ry="{r * .38:.1f}" transform="rotate({math.degrees(a):.0f} {cx + math.cos(a) * r * .55:.1f} '
        f'{cy + math.sin(a) * r * .55:.1f})" fill="{col}"/>'
        for a in (i / 5 * math.tau - math.pi / 2 for i in range(5)))
    return (f'<g class="{cls}">{petals}<circle cx="{cx}" cy="{cy}" r="{r * .22:.1f}" fill="{centre}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .1:.1f}" fill="{GOLD_L}"/></g>')


def bouquet(seed=4):
    """Low spray of peonies, blue flowers and leaves, 360 x 170, origin at its bottom centre."""
    r = random.Random(seed)
    out = []
    for i in range(14):
        a = -math.pi * (0.08 + 0.84 * i / 13)
        out.append(art.leaf(round(math.cos(a) * 120), round(math.sin(a) * 40 - 20), r.uniform(60, 90),
                            round(math.degrees(a) + 90), col=r.choice([LEAF_T, LEAF_T2, art.LEAF1])))
    for x, y, rr, kind in [(-120, -40, 34, "b"), (120, -40, 34, "b"), (-70, -70, 46, "p"), (70, -70, 46, "p"),
                           (0, -90, 56, "r"), (-30, -30, 34, "r2"), (40, -28, 30, "b"), (-150, -10, 26, "p")]:
        if kind == "b":
            out.append(flower5(x, y, rr, BLUE, centre=BLUE_D))
        elif kind == "p":
            out.append(art.rose(x, y, rr, col=PEACH, light="#fde0cf", dark=PEACH_D))
        else:
            out.append(art.rose(x, y, rr, col=PINK, light="#fbd3dc", dark=art.ROSE))
    return f'<g>{"".join(out)}</g>'


def arch_florals():
    """Watercolour-style flower clusters that sit on the arch line (arch coordinates, 860 x 1260)."""
    out = []
    spots = [(430, 0, 1.0), (128, 160, .9), (732, 160, .9), (0, 520, 1.0), (860, 520, 1.0), (0, 980, .85),
             (860, 980, .85)]
    for k, (x, y, s) in enumerate(spots):
        r = random.Random(30 + k)
        g = []
        for i in range(7):
            a = r.uniform(0, math.tau)
            g.append(art.leaf(round(x + math.cos(a) * 20), round(y + math.sin(a) * 20), r.uniform(44, 64) * s,
                              round(math.degrees(a) + 90), col=r.choice([LEAF_T, LEAF_T2])))
        g.append(flower5(x - 18 * s, y - 6, 26 * s, BLUE, centre=BLUE_D))
        g.append(art.rose(round(x + 16 * s), round(y + 10), round(24 * s), col=PEACH, light="#fde0cf", dark=PEACH_D))
        g.append(art.rose(round(x - 4), round(y + 30 * s), round(16 * s), col=PINK, light="#fbd3dc", dark=art.ROSE))
        out.append(f'<g class="afl">{"".join(g)}</g>')
    return "".join(out)


# ------------------------------------------------------------------ ring-exchange hands
def hands_medallion(size=380):
    """Pink watercolour circle with his hand (watch) holding hers (ring), drawn in a 380 box."""
    blots = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{o}"/>'
        for x, y, rx, ry, c, o in [(190, 190, 185, 185, "#f3c6d2", 1), (130, 120, 120, 80, "#e9a3b8", .55),
                                   (260, 260, 130, 90, "#e48fa9", .45), (250, 110, 100, 60, "#f7d6df", .7),
                                   (110, 270, 110, 70, "#efb3c4", .55), (200, 200, 90, 60, "#fbe1e8", .5)])
    skin, skin2 = "#f2c4a6", "#e8b08f"
    return (f'<svg viewBox="0 0 380 380" width="{size}" height="{size}">'
            f'<defs><clipPath id="hm-c"><circle cx="190" cy="190" r="184"/></clipPath>'
            f'<filter id="hm-b"><feGaussianBlur stdDeviation="9"/></filter></defs>'
            f'<g clip-path="url(#hm-c)"><g filter="url(#hm-b)">{blots}</g>'
            f'<g transform="translate(-52 -70) scale(1.28)">'
            # his hand, palm up, from the left with a leather watch
            f'<g class="hm-his">'
            f'<path d="M-20 250 C40 236 90 230 130 226 C160 222 196 214 228 206 C250 200 268 204 268 214 '
            f'C268 224 250 230 232 236 C246 238 254 246 248 254 C240 262 214 258 196 256 C170 262 150 274 120 282 '
            f'C80 292 30 300 -20 304 Z" fill="{skin}"/>'
            f'<path d="M196 256 C214 252 236 248 248 254" stroke="{skin2}" stroke-width="3" fill="none"/>'
            f'<rect x="58" y="226" width="34" height="70" rx="6" fill="#4a2e22" transform="rotate(-8 75 261)"/>'
            f'<rect x="66" y="252" width="20" height="16" rx="3" fill="#b8b8c0" transform="rotate(-8 76 260)"/></g>'
            # her hand, palm down, from the right, resting on his fingers
            f'<g class="hm-her">'
            f'<path d="M400 130 C350 146 310 160 280 172 C256 180 236 186 210 196 C190 202 172 206 160 214 '
            f'C150 222 156 232 170 230 C186 228 200 224 214 220 C206 230 210 238 222 236 C240 232 262 222 284 214 '
            f'C320 204 360 196 400 190 Z" fill="#f5d0b8"/>'
            f'<path d="M214 220 C230 214 248 208 262 204" stroke="{skin2}" stroke-width="2.6" fill="none"/>'
            f'<path d="M330 152 C336 168 340 182 342 196" stroke="#c9c9d2" stroke-width="3" fill="none"/>'
            f'<circle cx="341" cy="190" r="4" fill="#e6e6ee"/></g>'
            f'<g class="hm-ring"><ellipse cx="196" cy="210" rx="7" ry="11" fill="none" stroke="#d8d8e2" '
            f'stroke-width="4" transform="rotate(-20 196 210)"/>'
            f'<path d="M196 190 L204 198 L196 206 L188 198 Z" fill="#f4fbff" stroke="#9ccbe0" stroke-width="2"/></g>'
            f'</g></g><circle cx="190" cy="190" r="184" fill="none" stroke="{GOLD}" stroke-width="5"/>'
            f'<circle cx="190" cy="190" r="174" fill="none" stroke="#fff3e6" stroke-width="2" opacity=".9"/></svg>')
