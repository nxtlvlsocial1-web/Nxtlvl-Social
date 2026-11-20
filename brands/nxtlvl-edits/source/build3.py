"""Round 3 of the nxtlvl edits logo concepts: minimal and classy (M to T).

Flat grounds, no glows; one or two colours (Ink and Mist) with a single violet accent at most; hairlines, the serif
and plenty of empty space. Same wordmark as rounds 1 and 2, set in one colour.
Run:  python3 build3.py && python3 sheet.py 3
"""
import math
import os

import build2
import vector
from build import (INK, LIFT, MIST, OUT, PALE, S, SERIF, SPARK, VIOLET, WM_H, WM_W, WM_XH, _smooth_n_points, edits,
                   edits_box, lockup_parts, star, svg, wordmark, write)
from build2 import profile

NIGHT = '#1A0B3B'                                  # the darkest violet of the brand grounds, used flat
SANS = vector.sans(500)


def flat(colour):
    return lambda: ('', f'<rect width="{S}" height="{S}" fill="{colour}"/>')


build2.LOOKS.update({   # lockup background, wordmark, edits, star over the i
    'ink': (INK, MIST, MIST, LIFT),
    'mist': (MIST, INK, INK, VIOLET),
    'night': (NIGHT, MIST, MIST, PALE),
})


# Each mark returns (defs, body, width, height) in its own box, top-left at 0, 0.

# --- M: Serif e ------------------------------------------------------------------------------------------

def serif_e(p, fill=MIST, accent=LIFT):
    size = 1000
    x0, y0, x1, y1 = SERIF.bounds('e', size)
    d = SERIF.path('e', size, -x0, -y0)
    w, h = x1 - x0, y1 - y0
    return '', f'<path d="{d}" fill="{fill}"/>' + star(w + 26, 30, 30, accent), w + 60, h


# --- N: Seal ---------------------------------------------------------------------------------------------

def seal(p, fill=MIST, accent=MIST):
    r_out, r_in, r_text, size = 470, 356, 390, 56
    c = r_out
    text = 'NXTLVL  ·  EDITS  ·  NXTLVL  ·  EDITS  ·  '
    names, xs, s = SANS._layout(text, size, 0.0, None)
    adv = [SANS.hmtx[n][0] * s for n in names]
    total = sum(adv)
    out, a = '', -90.0
    for ch, w in zip(text, adv):
        ang = a + (w / 2) / total * 360
        if ch != ' ':
            d = SANS.path(ch, size, -w / 2, 0)
            out += (f'<path d="{d}" transform="translate({c} {c}) rotate({ang + 90:.3f}) translate(0 {-r_text:.1f})" '
                    f'fill="{fill}"/>')
        a += w / total * 360
    rings = (f'<circle cx="{c}" cy="{c}" r="{r_out - 5}" fill="none" stroke="{fill}" stroke-width="10"/>'
             f'<circle cx="{c}" cy="{c}" r="{r_in}" fill="none" stroke="{fill}" stroke-width="5"/>')
    return '', rings + out + star(c, c, 150, accent), 2 * r_out, 2 * r_out


# --- O: Split Star ---------------------------------------------------------------------------------------

def split_star(p, fill=INK):
    r, gap, slip = 300, 18, 14
    c = r
    # the cut runs from bottom left to top right through the centre; each half slips along it
    half_a = f'M{-r} {-r}L{3 * r} {-r}L{-r} {3 * r}Z'            # above the line x + y = 2r (in box units)
    half_b = f'M{3 * r} {-r}L{3 * r} {3 * r}L{-r} {3 * r}Z'
    defs = (f'<clipPath id="{p}a"><path d="{half_a}" transform="translate({-gap / 2 / math.sqrt(2):.2f} {-gap / 2 / math.sqrt(2):.2f})"/></clipPath>'
            f'<clipPath id="{p}b"><path d="{half_b}" transform="translate({gap / 2 / math.sqrt(2):.2f} {gap / 2 / math.sqrt(2):.2f})"/></clipPath>')
    st = f'<path d="{SPARK}" transform="translate({c} {c}) scale({r})" fill="{fill}"/>'
    s = slip / math.sqrt(2)
    body = (f'<g transform="translate({-s:.2f} {s:.2f})"><g clip-path="url(#{p}a)">{st}</g></g>'
            f'<g transform="translate({s:.2f} {-s:.2f})"><g clip-path="url(#{p}b)">{st}</g></g>')
    return defs, body, 2 * r, 2 * r


# --- P: Editorial Stack ----------------------------------------------------------------------------------

def editorial_stack(p, fill=INK, accent=VIOLET):
    size = 360
    ex0, ey0, ex1, ey1 = edits_box(size)
    ew = ex1 - ex0
    wm_w = ew * 0.56
    wm_h = wm_w * WM_H / WM_W
    gap = 92
    base = wm_h + gap - ey0
    body = (wordmark((ew - wm_w) / 2, 0, wm_h, fill)
            + edits(-ex0, base, size, fill, accent, star_scale=2.1))
    return '', body, ew, base + ey1


# --- Q: Sliced edits -------------------------------------------------------------------------------------

def sliced_word(p, x, base, size, fill, accent, gap, slip):
    """'edits' (star over the i) with its baseline origin at (x, base), cut once through the x-height; the top slips."""
    ex0, ey0, ex1, ey1 = edits_box(size)
    cut = base - 0.27 * size
    word = edits(x, base, size, fill, accent, star_scale=2.1)
    x0, x1 = x + ex0 - 50, x + ex1 + slip + 50
    defs = (f'<clipPath id="{p}t"><rect x="{x0:.1f}" y="{base - size * 1.2:.1f}" width="{x1 - x0:.1f}" '
            f'height="{size * 1.2 - (base - cut) - gap / 2:.1f}"/></clipPath>'
            f'<clipPath id="{p}b"><rect x="{x0:.1f}" y="{cut + gap / 2:.1f}" width="{x1 - x0:.1f}" height="{size:.1f}"/></clipPath>')
    body = (f'<g transform="translate({slip} 0)"><g clip-path="url(#{p}t)">{word}</g></g>'
            f'<g clip-path="url(#{p}b)">{word}</g>')
    return defs, body


def sliced_edits(p, fill=MIST, accent=LIFT):
    size = 400
    ex0, ey0, ex1, ey1 = edits_box(size)
    base = -ey0 + 40                                     # room for the star over the i
    defs, body = sliced_word(p, -ex0, base, size, fill, accent, gap=10, slip=7)
    return defs, body, ex1 - ex0 + 7, base + ey1


def sliced_lockup(height=118, pad=110):
    """nxtlvl + the sliced edits on one line, on Ink."""
    bg, wf, ef, sf = build2.LOOKS['ink']
    _, word_w = lockup_parts(0, 0, height, wf, ef, sf)
    W, H = int(pad * 2 + word_w + 4), int(height * 1.12 + pad * 2)
    x, y = pad, H / 2 - height / 2 + height * 0.06
    wm_w = WM_W * height / WM_H
    xh = height * (WM_H - WM_XH) / WM_H
    size = xh / 0.516 * 0.94
    ex0, _, _, _ = edits_box(size)
    defs, body = sliced_word('l', x + wm_w + 0.40 * height - ex0, y + height, size, ef, sf, gap=5, slip=4)
    return svg(W, H, defs, f'<rect width="{W}" height="{H}" fill="{bg}"/>' + wordmark(x, y, height, wf) + body)


# --- R: Monoline N ---------------------------------------------------------------------------------------

def monoline_n(p, fill=MIST, accent=LIFT):
    pts, _ = _smooth_n_points()
    d = 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts[::4]) + f'L{pts[-1][0]} {pts[-1][1]}'
    body = (f'<path d="{d}" transform="translate(-36 -26)" fill="none" stroke="{fill}" stroke-width="7" '
            f'stroke-linecap="round" stroke-linejoin="round"/>' + star(180 - 36, 22 - 26 + 8, 11, accent))
    return '', body, 124, 135


# --- S: ne Ligature --------------------------------------------------------------------------------------

def ne_ligature(p, fill=MIST, accent=PALE):
    size = 1000
    kern = {'ne': -0.05}
    x0, y0, x1, y1 = SERIF.bounds('ne', size, kern=kern)
    d = SERIF.path('ne', size, -x0, -y0, kern=kern)
    w, h = x1 - x0, y1 - y0
    return '', f'<path d="{d}" fill="{fill}"/>' + star(w + 20, 26, 26, accent), w + 50, h


# --- T: Cut Line -----------------------------------------------------------------------------------------

def cut_line(p, fill=MIST, accent=LIFT):
    w, y, gap, t = 640, 236, 40, 12
    c = w / 2
    body = (f'<rect x="0" y="{y - t / 2}" width="{c - gap / 2}" height="{t}" rx="{t / 2}" fill="{fill}"/>'
            f'<rect x="{c + gap / 2}" y="{y - t / 2}" width="{c - gap / 2}" height="{t}" rx="{t / 2}" fill="{fill}"/>'
            f'<rect x="0" y="{y - 34}" width="{t}" height="68" rx="{t / 2}" fill="{fill}"/>'
            f'<rect x="{w - t}" y="{y - 34}" width="{t}" height="68" rx="{t / 2}" fill="{fill}"/>'
            + star(c, 96, 96, accent))
    return '', body, w, y + 34


# ---------------------------------------------------------------------------------------------------------

CONCEPTS = [
    # slug, mark, ground, mark size (fraction of the canvas, by the larger side), (dx, dy), lockup look
    ('m-serif-e', serif_e, flat(INK), .40, (0, 30), 'ink'),
    ('n-seal', seal, flat(INK), .80, (0, 0), 'ink'),
    ('o-split-star', lambda p: split_star(p, INK), flat(MIST), .44, (0, 0), 'mist'),
    ('p-editorial-stack', editorial_stack, flat(MIST), .56, (0, 0), 'mist'),
    ('q-sliced-edits', sliced_edits, flat(INK), .60, (0, 0), 'ink'),
    ('r-monoline-n', monoline_n, flat(INK), .44, (0, 10), 'ink'),
    ('s-ne-ligature', ne_ligature, flat(NIGHT), .50, (0, 40), 'night'),
    ('t-cut-line', cut_line, flat(INK), .58, (0, 0), 'ink'),
]
WORDMARK_ONLY = {'p-editorial-stack'}


def main():
    for slug, mark, ground, frac, shift, look in CONCEPTS:
        write(os.path.join(OUT, slug, 'profile.svg'), profile(mark, ground, frac, shift))
        lock = sliced_lockup() if slug == 'q-sliced-edits' else build2.lockup(mark, look, slug in WORDMARK_ONLY)
        write(os.path.join(OUT, slug, 'lockup.svg'), lock)
    print('wrote', len(CONCEPTS), 'concepts to', OUT)


if __name__ == '__main__':
    main()
