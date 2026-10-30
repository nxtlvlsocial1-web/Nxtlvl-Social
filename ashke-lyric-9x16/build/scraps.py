"""Torn, crumpled paper scraps and print textures for the YouMotion-style collage, all procedural.

python3 build/scraps.py      (from the project root; after build/paper.py; needs Pillow, numpy, scipy)

Writes assets/img/scrap/: red-*, black-*, grey-*, white-* (crumpled paper torn to a ragged shape, the white paper core
showing along the tear, as PNG with alpha), and assets/img/tex/speckle.png (photocopy specks for the labels) and
grunge.png (an ink mask: mostly solid with worn holes, for the big stamped words).
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "scrap")
TEX = os.path.join(ROOT, "assets", "img", "tex")
PAPER = Image.open(os.path.join(ROOT, "assets", "img", "paper.png")).convert("L")
COLORS = {"red": (214, 36, 44), "black": (36, 34, 33), "grey": (176, 172, 166), "white": (240, 238, 233)}


def crumple(w, h, seed):
    """Crumple shading: a crop of the big procedural sheet, contrast pushed so the folds read at scrap size."""
    g = random.Random(seed)
    x, y = g.randint(0, PAPER.size[0] - w), g.randint(0, PAPER.size[1] - h)
    a = np.asarray(PAPER.crop((x, y, x + w, y + h)), np.float32)
    a = (a - a.mean()) * 1.4
    a = np.asarray(Image.fromarray(np.clip(a + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32) - 128
    a += np.random.default_rng(seed).normal(0, 9, a.shape)
    return a


def torn_mask(w, h, seed, jag=22):
    g = random.Random(seed)
    pts = []
    n = g.randint(7, 11)                 # few corners: torn paper is angular, not round
    for k in range(n):
        a = (k + g.uniform(-.3, .3)) / n * math.pi * 2
        r = g.uniform(.72, 1.0)
        pts.append((w / 2 + max(-1, min(1, math.cos(a) * 1.25)) * w * .47 * r, h / 2 + max(-1, min(1, math.sin(a) * 1.25)) * h * .46 * r))
    m = Image.new("L", (w, h))
    ImageDraw.Draw(m).polygon(pts, fill=255)
    # ragged fibre edge: displace the edge with noise
    noise = np.random.default_rng(seed).random((h // 6 + 1, w // 6 + 1))
    noise = np.asarray(Image.fromarray((noise * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    d = ndimage.distance_transform_edt(np.asarray(m) > 0) - ndimage.distance_transform_edt(np.asarray(m) == 0)
    edge = d + (noise - .5) * jag
    return edge


def scrap(kind, w, h, seed):
    edge = torn_mask(w, h, seed)
    alpha = (edge > 0).astype(np.float32)
    core = ((edge > 0) & (edge < 6 + 5 * np.random.default_rng(seed + 1).random(edge.shape))).astype(np.float32)
    shade = crumple(w, h, seed)
    col = np.array(COLORS[kind], np.float32)
    k = 1.0 if kind != "black" else 1.3
    rgb = col[None, None, :] + shade[..., None] * k
    if kind == "black":
        rgb += (np.clip(shade, 0, None)[..., None] * 1.5)      # crumple highlights on black paper
    rgb = rgb * (1 - core[..., None]) + np.array([236, 234, 228], np.float32) * core[..., None]   # white paper core at the tear
    a = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    im.putalpha(a)
    return im


def speckle(w=600, h=600, seed=3):
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w), np.float32)
    for _ in range(900):
        x, y, r = rng.integers(0, w), rng.integers(0, h), rng.uniform(.4, 1.8)
        yy, xx = np.ogrid[-3:4, -3:4]
        blob = np.exp(-(xx ** 2 + yy ** 2) / (2 * r * r)) * rng.uniform(.3, .9)
        x0, y0 = max(0, x - 3), max(0, y - 3)
        sub = a[y0:y + 4, x0:x + 4]
        sub += blob[: sub.shape[0], : sub.shape[1]]
    fine = rng.random((h, w)) < .02
    a = np.clip(a + fine * .25, 0, 1)
    im = Image.new("RGBA", (w, h), (40, 38, 36, 0))
    im.putalpha(Image.fromarray((a * 200).astype(np.uint8)))
    return im


def grunge(w=800, h=400, seed=5):
    rng = np.random.default_rng(seed)
    n = rng.random((h // 4, w // 4))
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    fine = rng.random((h, w))
    holes = (n > .78) | (fine > .985)
    scratches = np.zeros((h, w), bool)
    for _ in range(40):
        y = rng.integers(0, h)
        x0 = rng.integers(0, w)
        scratches[y:y + 1, x0:x0 + rng.integers(20, 160)] = True
    m = ~(holes | scratches)
    a = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))
    im = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    im.putalpha(a)
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sizes = [(1000, 700), (900, 520), (700, 700), (1200, 460)]
    for kind in COLORS:
        for k, (w, h) in enumerate(sizes):
            scrap(kind, w, h, 31 * k + len(kind)).save(os.path.join(OUT, f"{kind}-{k}.png"), optimize=True)
    speckle().save(os.path.join(TEX, "speckle.png"), optimize=True)
    grunge().save(os.path.join(TEX, "grunge.png"), optimize=True)
    print("wrote", OUT, "and tex/speckle.png, tex/grunge.png")
