"""Round 2 of the nxtlvl edits logo concepts: eight more directions (E to L), same family and wordmark as round 1.

Run:  python3 build2.py && python3 sheet.py 2
"""
import os
import re

from build import (DEEP, INK, LIFT, MIST, OUT, PALE, S, SERIF, STAR_SRC, VIOLET, WM_D, WM_H, WM_W, edits,
                   edits_box, ground_family, ground_glow, ground_violet, lockup_parts, star, svg, wordmark, write)


def ground_light():
    """Mist, with violet light from two corners (a light profile picture, unlike the main account's dark one)."""
    defs = (f'<radialGradient id="gl0" cx=".02" cy=".02" r=".8"><stop offset="0" stop-color="{LIFT}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{LIFT}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="gl1" cx=".98" cy=".98" r=".8"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>')
    body = (f'<rect width="{S}" height="{S}" fill="{MIST}"/><rect width="{S}" height="{S}" fill="url(#gl0)"/>'
            f'<rect width="{S}" height="{S}" fill="url(#gl1)"/>')
    return defs, body


def glow(p, cx, cy, r, colour=PALE, strength=.55):
    return (f'<radialGradient id="{p}glow" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{colour}" stop-opacity="{strength}"/><stop offset=".45" stop-color="{LIFT}" stop-opacity=".2"/>'
            f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>',
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{p}glow)"/>')


def diag(p, c0, c1, c2=None, x1=0, y1=1, x2=1, y2=0):
    stops = f'<stop offset="0" stop-color="{c0}"/>' + (f'<stop offset=".55" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
                                                      if c2 else f'<stop offset="1" stop-color="{c1}"/>')
    return f'<linearGradient id="{p}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{stops}</linearGradient>'


# Each mark returns (defs, body, width, height) in its own box, top-left at 0, 0.

# --- E: Play Star ----------------------------------------------------------------------------------------

def play_star(p):
    r = 52                                        # corner rounding (round stroke join)
    tri = f'M{r} {r}L{r} {560 - r}L{498 - r} 280Z'
    cx = (r + r + 498 - r) / 3                     # centroid
    defs = (diag(f'{p}pf', VIOLET, LIFT, '#EBDDFF')
            + f'<mask id="{p}m" maskUnits="userSpaceOnUse" x="-10" y="-10" width="530" height="580">'
              f'<rect x="-10" y="-10" width="530" height="580" fill="#fff"/>{star(cx + 8, 280, 112, "#000")}</mask>')
    body = (f'<g mask="url(#{p}m)"><path d="{tri}" fill="url(#{p}pf)" stroke="url(#{p}pf)" stroke-width="{2 * r}" '
            f'stroke-linejoin="round"/></g>')
    return defs, body, 498, 560


# --- F: Film nx ------------------------------------------------------------------------------------------

def _wordmark_letters(maxx):
    """Subpaths of the traced wordmark that lie left of maxx (wordmark units), e.g. 'nx'."""
    out = []
    for sub in re.findall(r'M[^M]*', WM_D):
        xs = [float(v) for v in re.findall(r'([-\d.]+) [-\d.]+', sub)]
        if max(xs) <= maxx:
            out.append(sub)
    return ''.join(out)


NX = _wordmark_letters(215)                       # n and x


def film_nx(p):
    w, h = 640, 470
    holes = ''
    for i in range(6):
        x = 52 + i * 98
        holes += f'<rect x="{x}" y="26" width="46" height="40" rx="10" fill="#000"/><rect x="{x}" y="{h - 66}" width="46" height="40" rx="10" fill="#000"/>'
    defs = (diag(f'{p}ff', DEEP, VIOLET, LIFT)
            + f'<mask id="{p}m" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">'
              f'<rect width="{w}" height="{h}" fill="#fff"/>{holes}</mask>')
    # nx in the window: x-height 23..100 of the wordmark box, n+x span 0..210 wide
    k = 300 / 210
    nx = (f'<path d="{NX}" transform="translate({w / 2 - 105 * k:.1f} {h / 2 - 61.5 * k:.1f}) scale({k:.4f})" '
          f'fill="#FFFFFF" fill-rule="evenodd"/>')
    body = (f'<rect width="{w}" height="{h}" rx="44" fill="url(#{p}ff)" mask="url(#{p}m)"/>'
            f'<rect x="34" y="92" width="{w - 68}" height="{h - 184}" rx="26" fill="{INK}"/>'
            + nx + star(w - 92, 140, 30, PALE))
    return defs, body, w, h


# --- G: ne Monogram --------------------------------------------------------------------------------------

N_ONLY = _wordmark_letters(100)


def ne_monogram(p):
    kn = 4.6                                       # n: 0..93 wide, 23..100 high in wordmark units
    nw, nh = 93 * kn, 77 * kn
    size = nh / 0.525 * 1.02
    ex0, ey0, ex1, ey1 = SERIF.bounds('e', size)
    ex = nw - 34 - ex0                              # the e just bites into the n's right stem
    base = nh - ey1
    e = SERIF.path('e', size, ex, base)
    w = ex + ex1 + 40
    defs = (diag(f'{p}ef', LIFT, PALE, '#FFFFFF')
            + f'<mask id="{p}m" maskUnits="userSpaceOnUse" x="-10" y="-200" width="{w + 20:.0f}" height="800">'
              f'<rect x="-10" y="-200" width="{w + 20:.0f}" height="800" fill="#fff"/>'
              f'<path d="{e}" fill="#000" stroke="#000" stroke-width="34" stroke-linejoin="round"/></mask>')
    body = (f'<g mask="url(#{p}m)"><path d="{N_ONLY}" transform="translate(0 {-23 * kn:.1f}) scale({kn})" fill="#FFFFFF"/></g>'
            f'<path d="{e}" fill="url(#{p}ef)"/>' + star(ex + ex1 + 4, base + ey0 - 30, 34, PALE))
    return defs, body, w, nh


# --- H: Star in Frame ------------------------------------------------------------------------------------

def star_frame(p):
    box, arm, sw = 640, 120, 16
    star_defs = open(os.path.join(STAR_SRC, 'star-defs.svgfrag')).read()
    paths = open(os.path.join(STAR_SRC, 'star-paths.svgfrag')).read()
    corners = ''
    for cx, cy, sx, sy in ((0, 0, 1, 1), (box, 0, -1, 1), (0, box, 1, -1), (box, box, -1, -1)):
        x, y = cx + sx * sw / 2, cy + sy * sw / 2
        corners += (f'<path d="M{x} {y + sy * arm}V{y + sy * 30}Q{x} {y} {x + sx * 30} {y}H{x + sx * arm}" fill="none" '
                    f'stroke="{PALE}" stroke-width="{sw}" stroke-linecap="round"/>')
    gdefs, gbody = glow(p, 140, 60, 46)
    k = 2.9
    mark = (f'<g transform="translate({box / 2} {box / 2}) scale({k}) translate(-94.5 -105.5)">{gbody}{paths}</g>')
    rec = f'<circle cx="74" cy="74" r="15" fill="#FF4D6D"/>'
    return star_defs + gdefs, corners + rec + mark, box, box


# --- I: Beat Bars ----------------------------------------------------------------------------------------

def beat_bars(p):
    bw, gap = 66, 30
    heights = (150, 250, 190, 330, 440)
    base = 600
    colours = (DEEP, VIOLET, VIOLET, LIFT, '#FFFFFF')
    defs, body = '', ''
    for i, (h, c) in enumerate(zip(heights, colours)):
        x = i * (bw + gap)
        defs += diag(f'{p}b{i}', c, '#FFFFFF' if i == 4 else LIFT if i < 3 else PALE, x1=0, y1=1, x2=0, y2=0)
        body += f'<rect x="{x}" y="{base - h}" width="{bw}" height="{h}" rx="{bw / 2}" fill="url(#{p}b{i})"/>'
    sx = 4 * (bw + gap) + bw / 2
    gdefs, gbody = glow(p, sx, 76, 110)
    return defs + gdefs, gbody + body + star(sx, 76, 60, '#FFFFFF'), 4 * (bw + gap) + bw, base


# --- J: Clapper ------------------------------------------------------------------------------------------

def clapper(p):
    w = 580

    def stripes(x0, y0, ww, hh, clip):
        s = ''
        for i in range(-2, 9):
            x = x0 + i * 96
            s += f'<path d="M{x} {y0 + hh}L{x + 48} {y0}H{x + 96}L{x + 48} {y0 + hh}Z" fill="{INK}"/>'
        return f'<g clip-path="url(#{clip})"><rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" fill="#FFFFFF"/>{s}</g>'

    defs = (diag(f'{p}cb', DEEP, VIOLET, LIFT)
            + f'<clipPath id="{p}c1"><rect x="0" y="0" width="{w}" height="96" rx="22"/></clipPath>'
            + f'<clipPath id="{p}c2"><rect x="0" y="212" width="{w}" height="96" rx="22"/></clipPath>')
    arm = f'<g transform="rotate(-15 26 190)">{stripes(0, 0, w, 96, f"{p}c1")}</g>'
    band = stripes(0, 212, w, 96, f'{p}c2')
    body = (f'<rect x="0" y="212" width="{w}" height="400" rx="40" fill="url(#{p}cb)"/>' + band
            + f'<rect x="0" y="290" width="{w}" height="20" fill="url(#{p}cb)"/>'
            + f'<circle cx="26" cy="188" r="20" fill="{PALE}"/>' + arm
            + star(w / 2, 460, 92, '#FFFFFF'))
    return defs, body, w, 612


# --- L: Cut Star, light ----------------------------------------------------------------------------------

def cut_star_light(p):
    paths = re.findall(r'<path[^>]*/>', open(os.path.join(STAR_SRC, 'star-paths.svgfrag')).read())
    trails = ''.join(paths[:3])
    for old, new in (('url(#mt0)', f'url(#{p}t0)'), ('url(#mt1)', f'url(#{p}t1)'), ('url(#mt2)', f'url(#{p}t2)')):
        trails = trails.replace(old, new)
    head = paths[3].replace('fill="#FFFFFF"', f'fill="url(#{p}hd)"')

    def trail(id_, c, x1, y1, x2, y2):
        return (f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
                f'<stop offset="0" stop-color="{c}" stop-opacity="0"/><stop offset=".55" stop-color="{c}" stop-opacity=".9"/>'
                f'<stop offset="1" stop-color="{c}"/></linearGradient>')
    cuts = ''.join(f'<line x1="0" y1="{c}" x2="200" y2="{200 + c}" stroke="#000" stroke-width="5"/>' for c in (30, 64))
    defs = (trail(f'{p}t0', DEEP, 28.3, 171.7, 121.6, 78.4) + trail(f'{p}t1', LIFT, 69.3, 164.7, 121.6, 112.3)
            + trail(f'{p}t2', '#B98AFF', 43.8, 122.2, 82.0, 84.0)
            + diag(f'{p}hd', DEEP, VIOLET)
            + f'<mask id="{p}cut" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200">'
              f'<rect width="200" height="200" fill="#fff"/>{cuts}</mask>')
    k = 3.825
    body = f'<g transform="scale({k}) translate(-22.6 -33.6)"><g mask="url(#{p}cut)">{trails}</g>{head}</g>'
    return defs, body, 143.8 * k, 143.8 * k


# --- K: Violet badge (wordmark only) ---------------------------------------------------------------------

def violet_stack(p):
    wm_w = 560
    wm_h = wm_w * WM_H / WM_W
    size = 330
    ex0, ey0, ex1, ey1 = edits_box(size)
    gap = 74
    w = max(wm_w, ex1 - ex0)
    base = wm_h + gap - ey0
    body = (wordmark((w - wm_w) / 2, 0, wm_h, '#FFFFFF')
            + edits(w / 2 - (ex0 + ex1) / 2, base, size, '#FFFFFF', '#FFFFFF', star_scale=2.3))
    return '', body, w, base + ey1


# ---------------------------------------------------------------------------------------------------------

CONCEPTS = [
    # slug, mark, ground, mark size in the profile (fraction of the canvas, by the larger side), (dx, dy), lockup look
    ('e-play-star', play_star, ground_glow, .50, (34, 0), 'dark'),
    ('f-film-nx', film_nx, ground_family, .62, (0, 0), 'dark'),
    ('g-ne-monogram', ne_monogram, ground_glow, .60, (0, 20), 'dark'),
    ('h-star-frame', star_frame, ground_family, .62, (0, 0), 'dark'),
    ('i-beat-bars', beat_bars, ground_glow, .50, (0, 0), 'dark'),
    ('j-clapper', clapper, ground_family, .52, (0, 0), 'dark'),
    ('k-violet-stack', violet_stack, ground_violet, .56, (0, 0), 'violet'),
    ('l-cut-star-light', cut_star_light, ground_light, .50, (0, 0), 'light'),
]

LOOKS = {   # lockup background, wordmark, edits, star over the i
    'dark': (INK, '#FFFFFF', '#FFFFFF', LIFT),
    'violet': (VIOLET, '#FFFFFF', '#FFFFFF', '#FFFFFF'),
    'light': (MIST, '#0B0816', '#0B0816', VIOLET),
}


def profile(mark, ground, frac, shift):
    gdefs, gbody = ground()
    mdefs, body, w, h = mark('p')
    k = frac * S / max(w, h)
    dx, dy = shift
    g = f'<g transform="translate({S / 2 - w * k / 2 + dx:.1f} {S / 2 - h * k / 2 + dy:.1f}) scale({k:.4f})">{body}</g>'
    return svg(S, S, gdefs + mdefs, gbody + g)


def lockup(mark, look, wordmark_only, height=118, pad=110, mark_h=200):
    bg, wf, ef, sf = LOOKS[look]
    _, word_w = lockup_parts(0, 0, height, wf, ef, sf)
    mdefs, body, w, h = mark('l')
    if wordmark_only:
        lead, mark_svg = 0, ''
    else:
        k = mark_h / max(w, h) if w <= h else min(mark_h / h, mark_h * 1.35 / w)
        lead = w * k + 0.5 * mark_h
    W = int(pad * 2 + lead + word_w)
    H = int(max(mark_h, height * 1.12) + pad * 2)
    if not wordmark_only:
        mark_svg = f'<g transform="translate({pad} {H / 2 - h * k / 2:.1f}) scale({k:.4f})">{body}</g>'
    word, _ = lockup_parts(pad + lead, H / 2 - height / 2 + height * 0.06, height, wf, ef, sf)
    return svg(W, H, mdefs, f'<rect width="{W}" height="{H}" fill="{bg}"/>' + mark_svg + word)


def main():
    for slug, mark, ground, frac, shift, look in CONCEPTS:
        write(os.path.join(OUT, slug, 'profile.svg'), profile(mark, ground, frac, shift))
        write(os.path.join(OUT, slug, 'lockup.svg'), lockup(mark, look, slug == 'k-violet-stack'))
    print('wrote', len(CONCEPTS), 'concepts to', OUT)


if __name__ == '__main__':
    main()
