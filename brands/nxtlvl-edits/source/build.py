"""Logo concepts for nxtlvl edits, the editing account of Nxtlvl Social.

Four profile marks, each with the same wordmark: "nxtlvl" (the original logo artwork, traced) + "edits" in Instrument
Serif Italic, whose i is dotted with the Nxtlvl star. All files are pure vector (text outlined, no fonts needed).
Run:  python3 build.py && node render-all.js
"""
import math
import os
import re

from fontTools.pens.recordingPen import RecordingPen

import vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', 'concepts'))
STAR_SRC = os.path.join(vector.REPO, 'brands', 'nxtlvl', 'card-skin', 'source')

INK, VIOLET, LIFT, DEEP, PALE, MIST = '#05030C', '#7D18FC', '#A95CFF', '#5E0FC4', '#D8BBFF', '#F5F2FF'
SPARK = 'M0-1C.06-.34.34-.06 1 0 .34.06.06.34 0 1-.06.34-.34.06-1 0-.34-.06-.06-.34 0-1Z'   # four-point star, r=1
S = 1080                                                                                   # profile canvas

SERIF = vector.serif_italic()
WM_D, WM_W, WM_H, WM_XH = vector.wordmark()          # wordmark path in a box 0..WM_W x 0..100, x-height top at WM_XH


def svg(w, h, defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{body}</svg>\n')


def star(x, y, r, fill):
    return f'<path d="{SPARK}" transform="translate({x:.2f} {y:.2f}) scale({r:.2f})" fill="{fill}"/>'


# --- shared backgrounds ----------------------------------------------------------------------------------

def ground_family(p=''):
    """The Shooting Star profile ground: near black, violet light from two corners."""
    defs = (f'<linearGradient id="{p}bg" x1=".329" y1=".03" x2=".671" y2=".97"><stop offset="0" stop-color="#0A0620"/>'
            f'<stop offset=".55" stop-color="{INK}"/><stop offset="1" stop-color="{INK}"/></linearGradient>'
            f'<radialGradient id="{p}g0" cx=".05" cy=".05" r=".72"><stop offset="0" stop-color="#7E1AF6" stop-opacity=".8"/>'
            f'<stop offset="1" stop-color="#7E1AF6" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{p}g1" cx=".95" cy=".95" r=".72"><stop offset="0" stop-color="#5E06F2" stop-opacity=".8"/>'
            f'<stop offset="1" stop-color="#5E06F2" stop-opacity="0"/></radialGradient>')
    body = (f'<rect width="{S}" height="{S}" fill="url(#{p}bg)"/><rect width="{S}" height="{S}" fill="url(#{p}g0)"/>'
            f'<rect width="{S}" height="{S}" fill="url(#{p}g1)"/>')
    return defs, body


def ground_glow():
    """Near black with one soft violet light behind the mark."""
    defs = (f'<radialGradient id="gw" cx=".5" cy=".46" r=".62"><stop offset="0" stop-color="#3A0B86"/>'
            f'<stop offset=".55" stop-color="#14072E"/><stop offset="1" stop-color="{INK}"/></radialGradient>')
    return defs, f'<rect width="{S}" height="{S}" fill="url(#gw)"/>'


def ground_violet():
    """Full brand violet, lighter top right."""
    defs = (f'<radialGradient id="gv" cx=".82" cy=".14" r="1.05"><stop offset="0" stop-color="#B57BFF"/>'
            f'<stop offset=".35" stop-color="{VIOLET}"/><stop offset=".75" stop-color="{DEEP}"/>'
            f'<stop offset="1" stop-color="#3B0890"/></radialGradient>')
    return defs, f'<rect width="{S}" height="{S}" fill="url(#gv)"/>'


# --- the wordmark: nxtlvl + edits (star over the i) ------------------------------------------------------

def _i_dot(size):
    """Centre and radius of the dot on the italic i, relative to the i's origin."""
    rec = RecordingPen()
    SERIF.glyphs[SERIF.cmap[ord('i')]].draw(rec)
    contours, cur = [], []
    for op, pts in rec.value:
        cur += [p for p in pts if p is not None]
        if op in ('closePath', 'endPath'):
            contours.append(cur)
            cur = []
    dot = max(contours, key=lambda c: min(p[1] for p in c))      # the contour that sits highest
    xs, ys = [p[0] for p in dot], [p[1] for p in dot]
    k = size / SERIF.upem
    return (min(xs) + max(xs)) / 2 * k, -(min(ys) + max(ys)) / 2 * k, (max(xs) - min(xs)) / 2 * k


EDITS_KERN = {'ed': -0.004, 'dı': -0.02, 'ıt': 0.0, 'ts': 0.006}


def edits(x, baseline, size, fill, star_fill, star_scale=2.2):
    """'edits' with its baseline origin at (x, baseline); the i is dotless and wears a four-point star instead."""
    text = 'edıts'
    d = SERIF.path(text, size, x, baseline, kern=EDITS_KERN)
    names, xs, _ = SERIF._layout(text, size, 0.0, EDITS_KERN)
    dx, dy, r = _i_dot(size)
    return f'<path d="{d}" fill="{fill}"/>' + star(x + xs[2] + dx, baseline + dy, r * star_scale, star_fill)


def edits_box(size):
    x0, y0, x1, y1 = SERIF.bounds('edits', size, kern={'ed': -0.004, 'di': -0.02, 'ts': 0.006})
    return x0, y0, x1, y1


def wordmark(x, y, height, fill):
    """The nxtlvl wordmark with its top-left at (x, y)."""
    k = height / WM_H
    return f'<path d="{WM_D}" transform="translate({x:.2f} {y:.2f}) scale({k:.4f})" fill="{fill}" fill-rule="evenodd"/>'


def lockup_parts(x, y, height, word_fill, edits_fill, star_fill, gap=0.40):
    """'nxtlvl edits' on one line, wordmark top-left at (x, y). Returns (svg, width)."""
    wm_w = WM_W * height / WM_H
    xh = height * (WM_H - WM_XH) / WM_H                 # wordmark x-height
    size = xh / 0.516 * 0.94                           # serif x-height a touch under the wordmark's
    ex0, _, ex1, _ = edits_box(size)
    ex = x + wm_w + gap * height - ex0
    body = wordmark(x, y, height, word_fill) + edits(ex, y + height, size, edits_fill, star_fill)
    return body, wm_w + gap * height + (ex1 - ex0)


# --- A: Cut Star -----------------------------------------------------------------------------------------

def concept_a():
    defs, ground = ground_family()
    star_defs = open(os.path.join(STAR_SRC, 'star-defs.svgfrag')).read()
    paths = re.findall(r'<path[^>]*/>', open(os.path.join(STAR_SRC, 'star-paths.svgfrag')).read())
    trails, head = ''.join(paths[:3]), paths[3]
    # trails run along x + y = const, so a cut line y - x = c slices all three at once, like a razor
    # through every track of a timeline
    cuts = ''.join(f'<line x1="0" y1="{c}" x2="200" y2="{200 + c}" stroke="#000" stroke-width="5"/>' for c in (30, 64))
    defs += (star_defs + f'<mask id="cut" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200">'
             f'<rect width="200" height="200" fill="#fff"/>{cuts}</mask>'
             f'<radialGradient id="glow" cx="140" cy="60" r="46" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{PALE}" stop-opacity=".55"/>'
             f'<stop offset=".45" stop-color="{LIFT}" stop-opacity=".22"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>')
    k = 1.4166 * S / 400
    mark = (f'<g transform="translate({S / 2} {S / 2}) scale({k:.4f}) translate(-94.5 -105.5)">'
            f'<circle cx="140" cy="60" r="46" fill="url(#glow)"/><g mask="url(#cut)">{trails}</g>{head}</g>')
    return svg(S, S, defs, ground + mark), mark_lockup_a(star_defs, trails, head)


def mark_lockup_a(star_defs, trails, head):
    cuts = ''.join(f'<line x1="0" y1="{c}" x2="200" y2="{200 + c}" stroke="#000" stroke-width="5"/>' for c in (30, 64))
    defs = (star_defs + f'<mask id="cut" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200">'
            f'<rect width="200" height="200" fill="#fff"/>{cuts}</mask>')
    # mark box in its own units: x 22..167, y 33..178
    def draw(x, y, h):
        k = h / 145.0
        return f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f}) translate(-22 -33)"><g mask="url(#cut)">{trails}</g>{head}</g>', 145 * k
    return defs, draw


# --- B: Clip N -------------------------------------------------------------------------------------------

def _smooth_n_points(step=0.2):
    """The Smooth N centre line (logo.svg, 200-unit box) as a dense polyline."""
    def cubic(p0, p1, p2, p3):
        n = 400
        return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
                      for a, b, c, d in zip(p0, p1, p2, p3)) for t in (i / n for i in range(n + 1))]

    def line(p, q):
        n = max(2, int(math.dist(p, q) / step))
        return [(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n + 1)]

    pts = (line((46, 154), (46, 92)) + cubic((46, 92), (46, 52), (76, 46), (100, 72))[1:]
           + line((100, 72), (112, 86))[1:] + cubic((112, 86), (136, 112), (154, 108), (154, 78))[1:]
           + line((154, 78), (154, 36))[1:])
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    return pts, acc


def clip_n_defs(p=''):
    """The N's gradient: violet bottom left, through Lift, to near white top right."""
    return (f'<linearGradient id="{p}ng" x1="20" y1="170" x2="190" y2="20" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" stop-color="{LIFT}"/>'
            f'<stop offset="1" stop-color="#E9DAFF"/></linearGradient>')


def clip_n(p='', gap=9.0, width=32):
    """The Smooth N razor-cut into three clips: flat cuts across both stems, round outer ends. 200-unit box."""
    pts, acc = _smooth_n_points()
    total = acc[-1]
    bounds = [0.0, 50.0, total - 30.0, total]          # cuts at y 104 on the left stem and y 66 on the right
    colours = [f'url(#{p}ng)'] * 3
    out = []
    for i, colour in enumerate(colours):
        a = bounds[i] + (gap / 2 if i > 0 else 0)
        b = bounds[i + 1] - (gap / 2 if i < len(colours) - 1 else 0)
        seg = [p for p, s in zip(pts, acc) if a <= s <= b]
        d = 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in seg)
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linejoin="round"/>')
        if i == 0:
            out.append(f'<circle cx="{seg[0][0]:.2f}" cy="{seg[0][1]:.2f}" r="{width / 2}" fill="{colour}"/>')
        if i == len(colours) - 1:
            out.append(f'<circle cx="{seg[-1][0]:.2f}" cy="{seg[-1][1]:.2f}" r="{width / 2}" fill="{colour}"/>')
    spark = (f'<path transform="translate(184 22) scale(1.05) translate(-12 -11.5)" '
             f'd="M12 0c.5 6.4 5.1 11 11.5 11.5C17.1 12 12.5 16.6 12 23c-.5-6.4-5.1-11-11.5-11.5C6.9 11 11.5 6.4 12 0z" fill="{PALE}"/>')
    return ''.join(out) + spark


def concept_b():
    defs, ground = ground_glow()
    k = 3.55
    # N box in its units: x 30..196, y 10..170  -> centre (113, 90)
    mark = f'<g transform="translate({S / 2} {S / 2 + 8}) scale({k}) translate(-113 -92)">{clip_n()}</g>'
    return svg(S, S, defs + clip_n_defs(), ground + mark)


# --- C: Timeline Steps ----------------------------------------------------------------------------------

STEPS_W, STEPS_H = 580, 520                            # local box of the mark


def timeline_steps(p=''):
    """Three clips on a timeline, each track a step higher (the next level), cut by a star-headed playhead.

    Returns (defs, body) in a local box 0..580 x 0..520; the playhead star sits at the top.
    """
    px, cut = 350, 26
    bars = ((0, 382, 420, DEEP, VIOLET), (130, 266, 380, VIOLET, LIFT), (260, 150, 320, '#FFFFFF', MIST))
    defs = (f'<mask id="{p}ph" maskUnits="userSpaceOnUse" x="-20" y="-20" width="620" height="560">'
            f'<rect x="-20" y="-20" width="620" height="560" fill="#fff"/>'
            f'<rect x="{px - cut / 2}" y="-20" width="{cut}" height="560" fill="#000"/></mask>'
            f'<linearGradient id="{p}pl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/>'
            f'<stop offset=".8" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="{p}hg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{PALE}" stop-opacity=".6"/>'
            f'<stop offset=".5" stop-color="{LIFT}" stop-opacity=".18"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>')
    rects = ''
    for i, (x, y, w, c0, c1) in enumerate(bars):
        defs += (f'<linearGradient id="{p}b{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c0}"/>'
                 f'<stop offset="1" stop-color="{c1}"/></linearGradient>')
        rects += f'<rect x="{x}" y="{y}" width="{w}" height="92" rx="22" fill="url(#{p}b{i})"/>'
    body = (f'<circle cx="{px}" cy="46" r="120" fill="url(#{p}hg)"/>'
            f'<g mask="url(#{p}ph)">{rects}</g>'
            f'<rect x="{px - 4.5}" y="46" width="9" height="474" rx="4.5" fill="url(#{p}pl)"/>'
            + star(px, 46, 50, '#FFFFFF'))
    return defs, body


def concept_c():
    defs, ground = ground_glow()
    mdefs, mark = timeline_steps()
    k = 1.0
    body = ground + f'<g transform="translate({S / 2 - STEPS_W * k / 2:.1f} {S / 2 - STEPS_H * k / 2 + 6:.1f}) scale({k})">{mark}</g>'
    return svg(S, S, defs + mdefs, body)


# --- D: Wordmark -----------------------------------------------------------------------------------------

def concept_d():
    defs, ground = ground_family()
    wm_w = 520
    wm_h = wm_w * WM_H / WM_W
    size = 300
    ex0, ey0, ex1, ey1 = edits_box(size)
    gap = 54
    total = wm_h + gap + (ey1 - ey0)
    top = S / 2 - total / 2 - 6
    wm_x = S / 2 - wm_w / 2
    ex = S / 2 - (ex0 + ex1) / 2
    base = top + wm_h + gap - ey0
    defs += (f'<linearGradient id="ed" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/>'
             f'<stop offset="1" stop-color="{PALE}"/></linearGradient>')
    # viewfinder corners around the stack
    bx0, by0, bx1, by1 = S / 2 - 345, top - 92, S / 2 + 345, base + ey1 + 86
    arm, sw = 74, 10
    corners = ''
    for cx, cy, sx, sy in ((bx0, by0, 1, 1), (bx1, by0, -1, 1), (bx0, by1, 1, -1), (bx1, by1, -1, -1)):
        corners += (f'<path d="M{cx:.1f} {cy + sy * arm:.1f}V{cy + sy * 18:.1f}Q{cx:.1f} {cy:.1f} {cx + sx * 18:.1f} {cy:.1f}'
                    f'H{cx + sx * arm:.1f}" fill="none" stroke="{PALE}" stroke-opacity=".7" stroke-width="{sw}" stroke-linecap="round"/>')
    rec = (f'<circle cx="{bx0 + 34:.1f}" cy="{by0 + 40:.1f}" r="9" fill="#FF4D6D"/>')
    body = (ground + corners + rec + wordmark(wm_x, top, wm_h, '#FFFFFF')
            + edits(ex, base, size, 'url(#ed)', LIFT, star_scale=2.6))
    return svg(S, S, defs, body)


# --- lockups ---------------------------------------------------------------------------------------------

def lockup(draw, mark_w, mark_h, height=118, pad=110):
    """Mark + 'nxtlvl edits' on one line, on Ink. draw(x, y) draws the mark (mark_w x mark_h) at top-left (x, y)."""
    _, word_w = lockup_parts(0, 0, height, '#FFFFFF', '#FFFFFF', LIFT)
    lead = mark_w + 0.55 * mark_h if draw else 0
    w = int(pad * 2 + lead + word_w)
    h = int(max(mark_h, height * 1.12) + pad * 2)
    word, _ = lockup_parts(pad + lead, h / 2 - height / 2 + height * 0.06, height, '#FFFFFF', '#FFFFFF', LIFT)
    return w, h, (draw(pad, h / 2 - mark_h / 2) if draw else '') + word


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(text)


def main():
    a_profile, (a_defs, a_draw) = concept_a()
    profiles = {'a-cut-star': a_profile, 'b-clip-n': concept_b(), 'c-timeline-steps': concept_c(), 'd-wordmark': concept_d()}
    for slug, text in profiles.items():
        write(os.path.join(OUT, slug, 'profile.svg'), text)

    mark_h = 190
    marks = {
        'a-cut-star': (a_defs, lambda x, y: a_draw(x, y - 15, mark_h + 30)[0], mark_h + 30, mark_h),
        'b-clip-n': (clip_n_defs('l'), lambda x, y: f'<g transform="translate({x} {y}) scale({mark_h / 160:.4f}) translate(-30 -10)">{clip_n("l")}</g>', 166 * mark_h / 160, mark_h),
        'c-timeline-steps': (timeline_steps('l')[0], lambda x, y: f'<g transform="translate({x} {y}) scale({mark_h / STEPS_H:.4f})">{timeline_steps("l")[1]}</g>', STEPS_W * mark_h / STEPS_H, mark_h),
        'd-wordmark': ('', None, 0, 0),
    }
    for slug, (mdefs, draw, mw, mh) in marks.items():
        w, h, body = lockup(draw, mw, mh)
        write(os.path.join(OUT, slug, 'lockup.svg'), svg(w, h, mdefs, f'<rect width="{w}" height="{h}" fill="{INK}"/>' + body))
    print('wrote', OUT)


if __name__ == '__main__':
    main()
