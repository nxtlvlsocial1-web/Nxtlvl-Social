"""Round 5 of the nxtlvl edits logo: six new lettermarks (U to Z), symbol only, no lettering.

Each concept comes in three colourways: pearl on rich black (the profile picture), ink on ivory and white on violet.
Run:  python3 build5.py && python3 sheet.py 5
"""
import os

import vector
from build import INK, MIST, OUT, S, VIOLET, write
from build2 import profile
from build3 import flat
from build4 import PEARL, centreline, contrast_outline, ground_ink, star4

TEXT = '#0B0816'
SERIF_UP = vector.Font(os.path.join(vector.REPO, 'website', 'fonts', 'instrument-serif-400.woff2'))

GROUNDS = {'pearl': ground_ink, 'light': flat(MIST), 'violet': flat(VIOLET)}


def paint(p, cw, w, h):
    """(defs, main fill, star fill, second tone) for a colourway, the pearl gradient running across the mark box."""
    if cw == 'pearl':
        stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in PEARL)
        defs = f'<linearGradient id="{p}pl" gradientUnits="userSpaceOnUse" x1="0" y1="{h}" x2="{w}" y2="0">{stops}</linearGradient>'
        return defs, f'url(#{p}pl)', '#FFFFFF', '#8F6BE0'
    if cw == 'light':
        return '', TEXT, VIOLET, '#6B5A8E'
    return '', '#FFFFFF', '#FFFFFF', '#C9A6FF'


# Each mark returns (defs, body, width, height) in its own box, top-left at 0, 0.

# --- U: Two Pillars --------------------------------------------------------------------------------------

def two_pillars(p, cw):
    """Two uprights whose angled ends lie on one diagonal: the eye draws the N. The right one stands higher."""
    a, W, H, top_l, top_r = 76, 250, 380, 84, 0
    m = (H - top_l) / W                                  # the implied diagonal: (0, top_l) to (W, H)
    w, h = W + 40, H
    defs, fill, star, _ = paint(p, cw, w, h)
    left = f'M0 {H}L{a} {H}L{a} {top_l + a * m:.1f}L0 {top_l}Z'
    right = f'M{W - a} {top_r}L{W} {top_r}L{W} {H}L{W - a} {top_l + (W - a) * m:.1f}Z'
    return defs, f'<path d="{left}" fill="{fill}"/><path d="{right}" fill="{fill}"/>' + star4(W + 22, 18, 18, star), w, h


# --- V: Reel Frame ---------------------------------------------------------------------------------------

def reel_frame(p, cw):
    """The refined N inside a 9:16 Reel frame; the star breaks the frame's top edge."""
    fw, fh, sw = 360, 640, 9
    k = 1.9
    base_y = fh - 128
    tip_y = 64                                            # where the right stem's point ends, inside the frame
    tip = 170 - (base_y - tip_y) / k                      # in N units
    pts = centreline(tip=tip)
    d = contrast_outline(pts, thick=7.5, hair=7.5, taper_out=60)
    ox = fw / 2 - 100 * k                                 # N spans x 40..160, centre 100
    oy = base_y - 170 * k
    sx, sy = ox + 160 * k, 0                              # the star sits on the frame line above the stem
    defs, fill, star, _ = paint(p, cw, fw, fh)
    gap = 34
    defs += (f'<mask id="{p}fm" maskUnits="userSpaceOnUse" x="-20" y="-20" width="{fw + 40}" height="{fh + 40}">'
             f'<rect x="-20" y="-20" width="{fw + 40}" height="{fh + 40}" fill="#fff"/>'
             f'<rect x="{sx - gap}" y="-20" width="{2 * gap}" height="40" fill="#000"/></mask>')
    frame = (f'<rect x="{sw / 2}" y="{sw / 2}" width="{fw - sw}" height="{fh - sw}" rx="58" fill="none" '
             f'stroke="{fill}" stroke-width="{sw}" mask="url(#{p}fm)"/>')
    n = f'<path d="{d}" transform="translate({ox:.1f} {oy:.1f}) scale({k})" fill="{fill}"/>'
    return defs, frame + n + star4(sx, sy + sw / 2, 24, star), fw, fh


# --- W: Folded N -----------------------------------------------------------------------------------------

def folded_n(p, cw):
    """An N folded from one ribbon: the uprights face forward, the diagonal is the ribbon's underside."""
    b, W, H, rise = 70, 300, 340, 50
    w, h = W + 30, H + rise
    defs, fill, star, _ = paint(p, cw, w, h)
    y0 = rise                                             # left upright top; the right one rises above it
    shade = {'pearl': ('#4A2A8C', '#8F6BE0'), 'light': ('#3A3150', '#7C6F98'), 'violet': ('#3B0890', '#A77BFF')}[cw]
    defs += (f'<linearGradient id="{p}bk" gradientUnits="userSpaceOnUse" x1="0" y1="{y0}" x2="{W}" y2="{y0 + H}">'
             f'<stop offset="0" stop-color="{shade[0]}"/><stop offset=".5" stop-color="{shade[1]}"/>'
             f'<stop offset="1" stop-color="{shade[0]}"/></linearGradient>')
    diag = f'M0 {y0}L{b} {y0}L{W} {y0 + H}L{W - b} {y0 + H}Z'
    left = f'M0 {y0}L{b} {y0}L{b} {y0 + H}L0 {y0 + H}Z'
    right = f'M{W - b} 0L{W} 0L{W} {y0 + H}L{W - b} {y0 + H}Z'
    body = (f'<path d="{diag}" fill="url(#{p}bk)"/>'
            f'<path d="{left}" fill="{fill}"/><path d="{right}" fill="{fill}"/>'
            + star4(W + 14, 14, 15, star))
    return defs, body, w, h


# --- X: Editorial N --------------------------------------------------------------------------------------

def editorial_n(p, cw):
    """A high-contrast serif capital N, like a magazine masthead, with the star at its top right."""
    size = 1000
    x0, y0, x1, y1 = SERIF_UP.bounds('N', size)
    d = SERIF_UP.path('N', size, -x0, -y0)
    w, h = x1 - x0 + 70, y1 - y0
    defs, fill, star, _ = paint(p, cw, w, h)
    return defs, f'<path d="{d}" fill="{fill}"/>' + star4(w - 22, 24, 30, star), w, h


# --- Y: N Disc -------------------------------------------------------------------------------------------

def n_disc(p, cw):
    """A solid disc with the refined N and the star cut out of it, like a coin or a seal."""
    R = 300
    k = 2.42
    pts = centreline(tip=26)
    d = contrast_outline(pts, thick=17, hair=17, taper_out=46)
    ox, oy = R - 100 * k, R - 92 * k - 2                  # keeps the star wholly inside the disc
    defs, fill, star, _ = paint(p, cw, 2 * R, 2 * R)
    defs += (f'<mask id="{p}dm" maskUnits="userSpaceOnUse" x="0" y="0" width="{2 * R}" height="{2 * R}">'
             f'<rect width="{2 * R}" height="{2 * R}" fill="#fff"/>'
             f'<path d="{d}" transform="translate({ox:.1f} {oy:.1f}) scale({k})" fill="#000"/>'
             + star4(ox + 160 * k, oy + 8 * k, 13 * k, '#000') + '</mask>')
    return defs, f'<circle cx="{R}" cy="{R}" r="{R}" fill="{fill}" mask="url(#{p}dm)"/>', 2 * R, 2 * R


# --- Z: NE Monogram --------------------------------------------------------------------------------------

def ne_monogram(p, cw):
    """N and E sharing one upright: the N's right stem is the E's spine. One even line, round ends."""
    t = 26
    L, M, Rx, E = 0, 0, 200, 330                          # x of the N's left stem, spine, E's arm ends
    top, base = 0, 360
    w, h = E + t, base + t
    defs, fill, star, _ = paint(p, cw, w, h)
    o = t / 2
    lines = [((o, base + o - 0), (o, top + o)), ((o, top + o), (Rx + o, base + o)), ((Rx + o, base + o), (Rx + o, top + o)),
             ((Rx + o, top + o), (E - 30 + o, top + o)), ((Rx + o, (top + base) / 2 + o), (E - 70 + o, (top + base) / 2 + o)),
             ((Rx + o, base + o), (E - 30 + o, base + o))]
    body = ''.join(f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" stroke="{fill}" stroke-width="{t}" '
                   f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>' for a, b in lines)
    return defs, body + star4(E + 2, top + o - 2, 24, star), w + 20, h


# ---------------------------------------------------------------------------------------------------------

CONCEPTS = [
    # slug, mark, size (fraction of the canvas, by the larger side), (dx, dy)
    ('u-two-pillars', two_pillars, .50, (0, 0)),
    ('v-reel-frame', reel_frame, .66, (0, 0)),
    ('w-folded-n', folded_n, .50, (0, 0)),
    ('x-editorial-n', editorial_n, .50, (0, 0)),
    ('y-n-disc', n_disc, .58, (0, 0)),
    ('z-ne-monogram', ne_monogram, .50, (0, 0)),
]


def main():
    for slug, mark, frac, shift in CONCEPTS:
        for cw, name in (('pearl', 'profile.svg'), ('light', 'alt-light.svg'), ('violet', 'alt-violet.svg')):
            write(os.path.join(OUT, slug, name), profile(lambda p, m=mark, c=cw: m(p, c), GROUNDS[cw], frac, shift))
    print('wrote', len(CONCEPTS), 'concepts to', OUT)


if __name__ == '__main__':
    main()
