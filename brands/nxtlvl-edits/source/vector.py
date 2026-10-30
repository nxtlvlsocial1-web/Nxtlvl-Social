"""Vector helpers for the nxtlvl edits logos: outline text with fontTools, trace the nxtlvl wordmark to a path.

Everything ends up as plain SVG paths, so the logo files open anywhere without fonts.
"""
import os

import numpy as np
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


class Font:
    """A font whose text can be turned into an SVG path (no kerning; pass per-pair tweaks via `kern`)."""

    def __init__(self, path, axes=None):
        f = TTFont(path)
        if axes:
            f = instantiateVariableFont(f, axes)
        self.glyphs = f.getGlyphSet()
        self.cmap = f.getBestCmap()
        self.hmtx = f['hmtx']
        self.upem = f['head'].unitsPerEm

    def _layout(self, text, size, tracking, kern):
        s = size / self.upem
        names = [self.cmap[ord(c)] for c in text]
        xs, x = [], 0.0
        for i, n in enumerate(names):
            xs.append(x)
            x += self.hmtx[n][0] * s + tracking * size
            if kern and i + 1 < len(text):
                x += kern.get(text[i:i + 2], 0) * size
        return names, xs, s

    def bounds(self, text, size, tracking=0.0, kern=None):
        """Ink box (x0, y0, x1, y1) of the text set at the origin, y down."""
        names, xs, s = self._layout(text, size, tracking, kern)
        pen = BoundsPen(self.glyphs)
        for n, x in zip(names, xs):
            self.glyphs[n].draw(TransformPen(pen, (s, 0, 0, -s, x, 0)))
        return pen.bounds

    def path(self, text, size, x=0.0, y=0.0, tracking=0.0, kern=None):
        """SVG path data for the text with its baseline origin at (x, y)."""
        names, xs, s = self._layout(text, size, tracking, kern)
        pen = SVGPathPen(self.glyphs, ntos=lambda v: f'{v:.2f}'.rstrip('0').rstrip('.'))
        for n, gx in zip(names, xs):
            self.glyphs[n].draw(TransformPen(pen, (s, 0, 0, -s, x + gx, y)))
        return pen.getCommands()


def serif_italic():
    return Font(os.path.join(HERE, 'fonts', 'instrument-serif-italic-400.woff2'))


def sans(weight):
    return Font(os.path.join(REPO, 'website', 'fonts', f'instrument-sans-{weight}.woff2'))


def archivo(wght=700, wdth=108):
    return Font(os.path.join(REPO, 'website', 'fonts', 'archivo-variable.woff2'), {'wght': wght, 'wdth': wdth})


# --- the nxtlvl wordmark (website/logo.png), traced with marching squares ---------------------------------

# corners tl=8, tr=4, br=2, bl=1 -> edges joined inside the cell (T, R, B, L); saddles 5 and 10 handled below
_CASES = {1: [('L', 'B')], 2: [('B', 'R')], 3: [('L', 'R')], 4: [('T', 'R')], 6: [('T', 'B')], 7: [('T', 'L')],
          8: [('T', 'L')], 9: [('T', 'B')], 11: [('T', 'R')], 12: [('L', 'R')], 13: [('B', 'R')], 14: [('L', 'B')]}


def _rdp(pts, tol):
    """Douglas-Peucker on an open polyline (numpy array of points)."""
    keep = np.zeros(len(pts), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2:
            continue
        p, q = pts[a], pts[b]
        seg = pts[a + 1:b]
        d = q - p
        n = np.hypot(*d)
        dist = (np.abs(d[0] * (seg[:, 1] - p[1]) - d[1] * (seg[:, 0] - p[0])) / n if n
                else np.hypot(seg[:, 0] - p[0], seg[:, 1] - p[1]))
        i = int(np.argmax(dist))
        if dist[i] > tol:
            m = a + 1 + i
            keep[m] = True
            stack += [(a, m), (m, b)]
    return pts[keep]


def trace(alpha, thr=127.5, tol=0.35):
    """Closed outlines (lists of (x, y) in pixel units) of the area where alpha > thr."""
    a = np.pad(alpha.astype(float), 1)
    b = a > thr
    case = b[:-1, :-1] * 8 + b[:-1, 1:] * 4 + b[1:, 1:] * 2 + b[1:, :-1] * 1

    def key(i, j, e):
        return {'T': ('h', i, j), 'B': ('h', i + 1, j), 'L': ('v', i, j), 'R': ('v', i, j + 1)}[e]

    def point(k):
        kind, i, j = k
        if kind == 'h':
            v0, v1 = a[i, j], a[i, j + 1]
            return (j + (thr - v0) / (v1 - v0), i)
        v0, v1 = a[i, j], a[i + 1, j]
        return (j, i + (thr - v0) / (v1 - v0))

    links = {}
    for i, j in zip(*np.nonzero((case > 0) & (case < 15))):
        c = int(case[i, j])
        if c in (5, 10):
            centre = a[i:i + 2, j:j + 2].mean() > thr
            segs = [('T', 'L'), ('B', 'R')] if (c == 5) == centre else [('T', 'R'), ('L', 'B')]
        else:
            segs = _CASES[c]
        for e0, e1 in segs:
            k0, k1 = key(i, j, e0), key(i, j, e1)
            links.setdefault(k0, []).append(k1)
            links.setdefault(k1, []).append(k0)

    loops, seen = [], set()
    for start in links:
        if start in seen:
            continue
        loop, prev, cur = [], None, start
        while True:
            seen.add(cur)
            loop.append(point(cur))
            nxt = [k for k in links[cur] if k != prev]
            prev, cur = cur, nxt[0]
            if cur == start:
                break
        pts = np.array(loop + [loop[0]]) - 1.0          # undo the padding
        pts = _rdp(pts, tol)[:-1]
        if len(pts) >= 3:
            loops.append(pts)
    return loops


def wordmark():
    """The nxtlvl wordmark as (path data, width, height, x-height top) in a box with its top-left at 0, 0, height 100.

    Source: brands/nxtlvl/card-skin/source/nxtlvl-wordmark-mask.png (website/logo.png upscaled 3x, Lanczos).
    """
    cache = os.path.join(HERE, 'nxtlvl-wordmark.svgfrag')
    if not os.path.exists(cache):
        src = os.path.join(REPO, 'brands', 'nxtlvl', 'card-skin', 'source', 'nxtlvl-wordmark-mask.png')
        alpha = np.array(Image.open(src))[:, :, 3]
        loops = trace(alpha)
        allpts = np.vstack(loops)
        x0, y0 = allpts.min(0)
        x1, y1 = allpts.max(0)
        s = 100.0 / (y1 - y0)
        d = ''.join('M' + 'L'.join(f'{(x - x0) * s:.2f} {(y - y0) * s:.2f}' for x, y in lp) + 'Z' for lp in loops)
        # x-height: top of the n (first letter)
        n = alpha[:, :441]
        xh = (np.nonzero((n > 127).any(1))[0].min() - y0) * s
        with open(cache, 'w') as f:
            f.write(f'{(x1 - x0) * s:.2f} {xh:.2f}\n{d}\n')
    w, xh = open(cache).readline().split()
    d = open(cache).read().split('\n')[1]
    return d, float(w), 100.0, float(xh)
