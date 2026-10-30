"""R refined: the Monoline N made premium.

The N is rebuilt from exact parts (two uprights, two round turns, one straight diagonal tangent to both), so it reads
as an N rather than a squiggle. The right upright climbs past the left (the next level) and tapers to a needle point
with the star just above it, as if the line ends in a spark. One fine, even line in a pearl sheen (white to lilac) on
Ink, plus a medallion, night-violet, ivory and a broad-pen (thick and thin) version.
Run:  python3 build4.py && python3 sheet.py 4
"""
import math
import os

import numpy as np

import build2
from build import INK, LIFT, MIST, OUT, PALE, S, VIOLET, write
from build2 import profile
from build3 import NIGHT, flat
from vector import _rdp

IVORY = MIST


def centreline(xl=40, xr=160, top=40, base=170, r=22, tip=14, step=0.2):
    """The Smooth N rebuilt from exact parts: left upright, a round turn over the top, one straight diagonal, a round
    turn at the bottom, and a right upright that climbs well past the left one (the next level) to a point."""
    c1 = np.array([xl + r, top + r])
    c2 = np.array([xr - r, base - r])
    d = c2 - c1
    theta = math.atan2(d[1], d[0]) + math.asin(2 * r / math.hypot(*d))      # the diagonal: tangent to both turns
    a1, a2 = theta - math.pi / 2, theta + math.pi / 2

    def line(p, q):
        n = max(2, int(math.dist(p, q) / step))
        return [(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n + 1)]

    def arc(c, a0, a1_):
        n = max(8, int(abs(a1_ - a0) * r / step))
        return [(c[0] + r * math.cos(a0 + (a1_ - a0) * i / n), c[1] + r * math.sin(a0 + (a1_ - a0) * i / n)) for i in range(n + 1)]

    e1 = tuple(c1 + r * np.array([math.cos(a1), math.sin(a1)]))
    s2 = tuple(c2 + r * np.array([math.cos(a2), math.sin(a2)]))
    return (line((xl, base), (xl, c1[1])) + arc(c1, math.pi, a1 + 2 * math.pi)[1:] + line(e1, s2)[1:]
            + arc(c2, a2, 0.0)[1:] + line((xr, c2[1]), (xr, tip))[1:])


def contrast_outline(pts, thick=16.0, hair=3.0, nib=0.0, taper_in=0.0, taper_out=44.0):
    """Outline (path data) of a broad-pen stroke along pts: width follows the stroke direction against the nib angle."""
    p = np.array(pts)
    seg = np.diff(p, axis=0)
    acc = np.concatenate([[0], np.cumsum(np.hypot(seg[:, 0], seg[:, 1]))])
    total = acc[-1]
    tan = np.gradient(p, axis=0)
    tan /= np.hypot(tan[:, 0], tan[:, 1])[:, None]
    theta = np.arctan2(tan[:, 1], tan[:, 0])
    width = hair + (thick - hair) * np.abs(np.sin(theta - nib)) ** 1.6
    f_in = np.clip(0.82 + 0.18 * acc / taper_in, 0, 1) if taper_in else 1.0
    f_out = np.sin(np.clip((total - acc) / taper_out, 0, 1) * np.pi / 2)    # eases in, ends in a sharp point
    width = width * f_in * f_out
    normal = np.stack([-tan[:, 1], tan[:, 0]], 1)
    left = p + normal * (width / 2)[:, None]
    right = p - normal * (width / 2)[:, None]
    left, right = _rdp(left, 0.01), _rdp(right, 0.01)
    ring = np.vstack([left, right[::-1]])
    return 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in ring) + 'Z'


def star4(x, y, r, fill, waist=.34):
    """A four-point star a touch slimmer than the brand spark (waist = how far the curves pull in)."""
    w = waist
    d = f'M0-1C{.06 * w / .34:.3f}-{w:.3f} {w:.3f}-{.06 * w / .34:.3f} 1 0 {w:.3f} {.06 * w / .34:.3f} {.06 * w / .34:.3f} {w:.3f} 0 1-{.06 * w / .34:.3f} {w:.3f}-{w:.3f} {.06 * w / .34:.3f}-1 0-{w:.3f}-{.06 * w / .34:.3f}-{.06 * w / .34:.3f}-{w:.3f} 0-1Z'
    return f'<path d="{d}" transform="translate({x:.2f} {y:.2f}) scale({r:.2f})" fill="{fill}"/>'


PEARL = ((0, '#C9AEFF'), (.28, '#FFFFFF'), (.5, '#E4D3FF'), (.68, '#FFFFFF'), (1, '#B794F6'))
FOIL = ((0, VIOLET), (.4, LIFT), (.62, '#E9DAFF'), (1, VIOLET))


def sheen(id_, stops, x1=40, y1=160, x2=165, y2=30):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


# the N (200-unit box): uprights x 40 and 160, baseline 170, right stem tip 14, star above it
BOX = (30, -14, 170, 170)                   # x0, y0, x1, y1 of the mark incl. the star


MONO = dict(thick=8.5, hair=8.5, taper_out=52)        # one even line
PEN = dict(thick=16, hair=3.0, taper_out=44)          # broad pen: thick uprights and diagonal, hairline turns


def refined_n(p, stroke='pearl', star_fill='#FFFFFF', pen=MONO, star_r=13.5):
    d = contrast_outline(centreline(), **pen)
    if stroke in ('pearl', 'foil'):
        defs, fill = sheen(f'{p}sh', PEARL if stroke == 'pearl' else FOIL), f'url(#{p}sh)'
    else:
        defs, fill = '', stroke
    x0, y0, x1, y1 = BOX
    body = (f'<g transform="translate({-x0} {-y0})"><path d="{d}" fill="{fill}"/>'
            + star4(160, -2, star_r, star_fill) + '</g>')
    return defs, body, x1 - x0, y1 - y0


def medallion(p, stroke='pearl', ring=PALE):
    """The refined N inside a fine double ring."""
    defs, body, w, h = refined_n(p, stroke)
    R = 150
    k = 0.92 * R / max(w, h) * 1.05
    rings = (f'<circle cx="{R}" cy="{R}" r="{R - 2}" fill="none" stroke="{ring}" stroke-opacity=".55" stroke-width="2.4"/>'
             f'<circle cx="{R}" cy="{R}" r="{R - 11}" fill="none" stroke="{ring}" stroke-opacity=".3" stroke-width="1"/>')
    g = f'<g transform="translate({R - w * k / 2:.2f} {R - h * k / 2 + 2:.2f}) scale({k:.4f})">{body}</g>'
    return defs, rings + g, 2 * R, 2 * R


def ground_ink():
    """Ink with the faintest lift in the middle, so the black reads rich rather than flat."""
    defs = (f'<radialGradient id="gi" cx=".5" cy=".46" r=".7"><stop offset="0" stop-color="#110A24"/>'
            f'<stop offset="1" stop-color="{INK}"/></radialGradient>')
    return defs, f'<rect width="{S}" height="{S}" fill="url(#gi)"/>'


def ground_night():
    defs = (f'<radialGradient id="gn" cx=".5" cy=".42" r=".75"><stop offset="0" stop-color="#2A1260"/>'
            f'<stop offset="1" stop-color="{NIGHT}"/></radialGradient>')
    return defs, f'<rect width="{S}" height="{S}" fill="url(#gn)"/>'


build2.LOOKS.update({'pearl': (INK, MIST, MIST, PALE), 'ivory': (IVORY, INK, INK, VIOLET), 'night': (NIGHT, MIST, MIST, PALE)})

CONCEPTS = [
    # slug, mark, ground, size, (dx, dy), lockup look
    ('r1-monoline-pearl', lambda p: refined_n(p, 'pearl'), ground_ink, .52, (0, 4), 'pearl'),
    ('r2-monoline-medallion', lambda p: medallion(p, 'pearl'), ground_ink, .78, (0, 0), 'pearl'),
    ('r3-monoline-night', lambda p: refined_n(p, 'pearl'), ground_night, .52, (0, 4), 'night'),
    ('r4-monoline-ivory', lambda p: refined_n(p, INK, VIOLET), flat(IVORY), .52, (0, 4), 'ivory'),
    ('r5-monoline-pen', lambda p: refined_n(p, 'pearl', pen=PEN), ground_ink, .52, (0, 4), 'pearl'),
]


def main():
    for slug, mark, ground, frac, shift, look in CONCEPTS:
        write(os.path.join(OUT, slug, 'profile.svg'), profile(mark, ground, frac, shift))
        write(os.path.join(OUT, slug, 'lockup.svg'), build2.lockup(mark, look, False))
    print('wrote', len(CONCEPTS), 'concepts to', OUT)


if __name__ == '__main__':
    main()
