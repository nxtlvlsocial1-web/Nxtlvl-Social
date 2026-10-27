"""Rebuild the bird's body and feet layers so the legs read as real feet.

python3 -I build/bird_clean.py      (run from the project root; needs numpy, scipy and Pillow)

The first cut-out left the body with a recoloured blob where the planted foot was, a ragged bottom right where the
kicked foot was removed and a dent where the raised wing was. Here the lower body is regrown: the silhouette is
completed with an ellipse fitted to the clean edge, and the missing pixels are painted from a smooth shading model
(a cubic in x and y plus rim darkening) fitted to the bird's own clean pink pixels. Both feet are made from the one
foot the original art shows in full (the kicked one), cleaned of body pixels, so each foot is a whole rounded 3D shape
that can lift, roll and step.

Writes assets/img/bird_core.png (backs up the old one once as bird_core_v4.png), bird_foot.png and bird_foot_up.png.
"""
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")


def load(name):
    return np.array(Image.open(os.path.join(IMG, name)).convert("RGBA")).astype(np.float64)


def save(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(IMG, name))


def body():
    src = os.path.join(IMG, "bird_core_v4.png")
    if not os.path.exists(src):
        os.rename(os.path.join(IMG, "bird_core.png"), src)
    a = load("bird_core_v4.png")
    H, W = a.shape[:2]
    al = a[..., 3]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)

    # silhouette: fit an ellipse to the clean left and right edges between y 200 and 470
    pts = []
    for y in range(200, 471, 4):
        xs = np.where(al[y] > 128)[0]
        if len(xs):
            pts += [(xs.min(), y), (xs.max(), y)]
    P = np.array(pts, float)
    # x^2, y^2, x, y, 1 (axis-aligned ellipse)
    A = np.c_[P[:, 0] ** 2, P[:, 1] ** 2, P[:, 0], P[:, 1], np.ones(len(P))]
    _, _, vt = np.linalg.svd(A)
    a2, b2, c1, d1, e0 = vt[-1]
    cx, cy = -c1 / (2 * a2), -d1 / (2 * b2)
    k = a2 * cx ** 2 + b2 * cy ** 2 - e0
    rx, ry = np.sqrt(k / a2), np.sqrt(k / b2)
    ry = min(ry, 565 - cy)                       # the body sits on y ~565, its original floor line
    print(f"ellipse centre ({cx:.0f},{cy:.0f}) radii ({rx:.0f},{ry:.0f})")
    r = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    ell = np.clip((1 - r) * ry / 1.5 + .5, 0, 1)  # anti-aliased, ~1.5 px edge

    # which pixels are clean body: pink hue, opaque, outside the face, above the damaged bottom
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    pink = (R > 170) & (G < 140) & (B > 90) & (R - G > 90) & (al > 250)
    face = (xx > 120) & (xx < 500) & (yy > 90) & (yy < 350)
    clean = pink & ~face & (yy > 60) & (yy < 470) & (r < .97) & ~((xx > 470) & (yy < 260))

    # shading model: cubic in normalised x, y plus rim darkening terms in r
    u, v = (xx - cx) / rx, (yy - cy) / ry

    def feats(m):
        U, V, Rr = u[m], v[m], r[m]
        cols = [np.ones_like(U), U, V, U * U, U * V, V * V, U ** 3, U * U * V, U * V * V, V ** 3,
                Rr ** 2, Rr ** 4, Rr ** 8, Rr ** 16]
        return np.stack(cols, 1)
    X = feats(clean)
    model = np.zeros((H, W, 3))
    inside = r < 1.6
    Xi = feats(inside)
    for ch in range(3):
        coef, *_ = np.linalg.lstsq(X, a[..., ch][clean], rcond=None)
        model[..., ch][inside] = Xi @ coef
    err = np.abs(X @ np.linalg.lstsq(X, a[..., 0][clean], rcond=None)[0] - a[..., 0][clean]).mean()
    print(f"shading model mean error (red) {err:.1f}")

    # keep the original above the damage (the bottom, lower on the left than on the right where the kicked foot was
    # cut away) and away from the dent the raised wing left; regrow the rest, with a soft seam
    line = np.interp(xx, [0, 430, 490, W], [495, 495, 405, 405])
    keep = np.clip((line - yy) / 30, 0, 1)
    keep[(xx > 488) & (yy > 95) & (yy < 270)] = 0
    keep[(xx < 150) & (yy > 240) & (yy < 490)] = 0     # the seam where the left wing was cut away
    # holes inside the outline (left by the first cut along the wing) are filled and painted too
    solid = np.zeros((H, W), bool)
    for y in range(H):
        xs = np.where(al[y] > 128)[0]
        if len(xs):
            solid[y, xs.min() + 3:xs.max() - 2] = True
    solid &= (yy < 440) | (r < 1)                   # the old foot stays out of the outline
    hole = solid & (al < 250)
    keep[hole] = 0
    keep = np.array(Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))) / 255.
    keep[face & (yy < 340)] = 1                       # never touch the face
    keep = np.where(al > 8, keep, 0)                  # nothing to keep where the cut-out was empty

    # a little noise so the painted area matches the render's grain
    rng = np.random.default_rng(3)
    model += rng.normal(0, 1.2, model.shape)
    out = np.zeros_like(a)
    for ch in range(3):
        out[..., ch] = a[..., ch] * keep + model[..., ch] * (1 - keep)
    alpha = al * keep + ell * 255 * (1 - keep)
    # by the old wing the outline is already right; only the colour of the stub's strip is repainted
    stub = (xx > 440) & (yy >= 60) & (yy < 300)
    alpha[stub] = al[stub]
    alpha[solid] = 255
    out[..., 3] = alpha
    save(out, "bird_core.png")


def feet():
    """The kicked foot, cleaned: its outline becomes a fitted ellipse (smooth, anti-aliased) and the colour is spread
    outwards from the clean interior so the new edge never shows the old fringe."""
    f = np.pad(load("bird_footr_up.png"), ((40, 40), (40, 40), (0, 0)))   # room for the fitted outline
    R, G, B, A = f[..., 0], f[..., 1], f[..., 2], f[..., 3]
    orange = (R > 150) & (G > 70) & (B < 110) & (G / np.maximum(R, 1) > .38) & (A > 200)
    ys, xs = np.nonzero(orange)
    c = np.array([xs.mean(), ys.mean()])
    cov = np.cov(np.stack([xs - c[0], ys - c[1]]))
    w, v = np.linalg.eigh(cov)
    H, W = A.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    d = np.stack([xx - c[0], yy - c[1]], -1)
    u0, u1 = d @ v[:, 1], d @ v[:, 0]                     # along the major and minor axes
    a, b = 2.0 * np.sqrt(w[1]) * .98, 2.0 * np.sqrt(w[0]) * .98   # a uniform ellipse has variance r^2/4
    r = np.sqrt((u0 / a) ** 2 + (u1 / b) ** 2)
    alpha = np.clip((1 - r) * b / 1.2 + .5, 0, 1)
    # colour: clean interior pixels, spread outwards by normalised blur
    core = (orange & (r < .9)).astype(np.float64)
    rgb = np.zeros((H, W, 3))
    for ch in range(3):
        num = gaussian_filter(f[..., ch] * core, 5)
        den = gaussian_filter(core, 5)
        spread = num / np.maximum(den, 1e-3)
        rgb[..., ch] = np.where(core > 0, f[..., ch], spread)
    # a little rim darkening so the edge reads round, like the render
    rgb *= (1 - .16 * np.clip((r - .75) / .25, 0, 1) ** 2)[..., None]
    out = np.dstack([rgb, alpha * 255])
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
    img = img.crop(img.getbbox())
    img.save(os.path.join(IMG, "bird_foot_up.png"))
    flat = img.rotate(-38, resample=Image.BICUBIC, expand=True)
    flat = flat.crop(flat.getbbox())
    flat.save(os.path.join(IMG, "bird_foot.png"))
    print("foot", img.size, "flat", flat.size, f"ellipse {a:.0f}x{b:.0f}")


if __name__ == "__main__":
    body()
    feet()
