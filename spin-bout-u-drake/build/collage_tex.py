"""Textures for the v9 collage (the Ashke edit's structure in the Spin Bout U colours), all procedural, plus sticker
versions of the cut-outs. Ported from ../ashke-lyric-9x16/build/paper.py, scraps.py and cutouts.py, recoloured.

python3 build/collage_tex.py      (from the project root; after build/assets.py and build/anime.py)

Writes assets/img/collage/: paper.png (a big crumpled maroon sheet for the camera to travel over),
scrap/{mag,black,maroon,white}-{0..3}.png (torn crumpled paper with the pale core along the tear), tex/speckle.png,
tex/grunge.png, and sticker/<name>.png (each cut-out with an off-white paper border and a soft shadow).
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(ROOT, "assets", "img", "collage")
COLORS = {"mag": (176, 25, 79), "black": (30, 28, 29), "maroon": (95, 27, 48), "white": (240, 238, 233)}
STICKERS = {   # name: source cut-out
    "drake_back_jacket": "cut/drake_back_jacket", "drake_laugh_hands": "cut/drake_laugh_hands", "drake_chanel_night": "cut/drake_chanel_night",
    "drake_nocta_red": "cut/drake_nocta_red", "drake_boat_sunset": "cut/drake_boat_sunset", "cat_black_collar": "cut/cat_black_collar",
    "cat_white_dumb": "cut/cat_white_dumb", "hand_phone_sticker": "cut/hand_phone_sticker",
    "crew": "anime/cut/crew", "finale": "anime/cut/finale", "snotty": "anime/cut/snotty", "spin": "anime/cut/spin", "spirit": "anime/cut/spirit",
}


def paper():
    H, W = 3900, 2600
    rng = np.random.default_rng(12)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    h = np.zeros((H, W), np.float32)
    for _ in range(110):
        a = rng.uniform(0, np.pi)
        n = np.array([np.cos(a), np.sin(a)], np.float32)
        p0 = np.array([rng.uniform(0, W), rng.uniform(0, H)], np.float32)
        d = (x - p0[0]) * n[0] + (y - p0[1]) * n[1]
        h += rng.uniform(.01, .04) * np.abs(d) * (1 if rng.random() < .5 else -1) * np.exp(-np.abs(d) / rng.uniform(250, 900))
    gy, gx = np.gradient(h)
    shade = np.clip(1 + .75 * (-.6 * gx - .8 * gy), .8, 1.12)
    sh = Image.fromarray(((shade - .78) / .36 * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
    shade = np.array(sh, np.float32) / 255 * .42 + .76
    fib = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    fib = np.array(Image.fromarray(((fib * 18) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 128 - 1
    stain = np.array(Image.fromarray((rng.random((30, 20)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    base = np.array([92, 27, 47], np.float32)
    img = base[None, None, :] * shade[..., None] * (1 + .05 * fib[..., None]) * (.88 + .16 * stain[..., None])
    im = Image.fromarray(img.clip(0, 255).astype(np.uint8))
    im.save(os.path.join(C, "paper.png"), optimize=True)
    return im.convert("L")


def crumple(P, w, h, seed):
    g = random.Random(seed)
    x, y = g.randint(0, P.size[0] - w), g.randint(0, P.size[1] - h)
    a = np.asarray(P.crop((x, y, x + w, y + h)), np.float32)
    a = (a - a.mean()) * 2.6
    a = np.asarray(Image.fromarray(np.clip(a + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32) - 128
    return a + np.random.default_rng(seed).normal(0, 9, a.shape)


def torn_edge(w, h, seed, jag=22):
    g = random.Random(seed)
    n = g.randint(7, 11)
    pts = []
    for k in range(n):
        a = (k + g.uniform(-.3, .3)) / n * math.pi * 2
        r = g.uniform(.72, 1.0)
        pts.append((w / 2 + max(-1, min(1, math.cos(a) * 1.25)) * w * .47 * r, h / 2 + max(-1, min(1, math.sin(a) * 1.25)) * h * .46 * r))
    m = Image.new("L", (w, h))
    ImageDraw.Draw(m).polygon(pts, fill=255)
    noise = np.random.default_rng(seed).random((h // 6 + 1, w // 6 + 1))
    noise = np.asarray(Image.fromarray((noise * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    d = ndimage.distance_transform_edt(np.asarray(m) > 0) - ndimage.distance_transform_edt(np.asarray(m) == 0)
    return d + (noise - .5) * jag


def scrap(P, kind, w, h, seed):
    edge = torn_edge(w, h, seed)
    alpha = (edge > 0).astype(np.float32)
    core = ((edge > 0) & (edge < 6 + 5 * np.random.default_rng(seed + 1).random(edge.shape))).astype(np.float32)
    shade = crumple(P, w, h, seed)
    rgb = np.array(COLORS[kind], np.float32)[None, None, :] + shade[..., None] * (1.3 if kind == "black" else 1.0)
    rgb = rgb * (1 - core[..., None]) + np.array([236, 234, 228], np.float32) * core[..., None]
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    im.putalpha(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7)))
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
    a = np.clip(a + (rng.random((h, w)) < .02) * .25, 0, 1)
    im = Image.new("RGBA", (w, h), (40, 38, 36, 0))
    im.putalpha(Image.fromarray((a * 200).astype(np.uint8)))
    return im


def grunge(w=800, h=400, seed=5):
    rng = np.random.default_rng(seed)
    n = rng.random((h // 4, w // 4))
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    holes = (n > .78) | (rng.random((h, w)) > .985)
    for _ in range(40):
        y, x0 = rng.integers(0, h), rng.integers(0, w)
        holes[y:y + 1, x0:x0 + rng.integers(20, 160)] = True
    im = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    im.putalpha(Image.fromarray((~holes * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6)))
    return im


def sticker(name, src):
    im = Image.open(os.path.join(ROOT, "assets", "img", src + ".png")).convert("RGBA")
    s = min(1.0, 1100 / im.size[1])
    im = im.resize((round(im.size[0] * s), round(im.size[1] * s)), Image.LANCZOS)
    m = im.split()[3]
    B = 18
    W, H = im.size[0] + 2 * B + 30, im.size[1] + 2 * B + 30
    mm = Image.new("L", (W, H))
    mm.paste(m, (B, B))
    border = mm.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(1))
    shadow = border.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * .5))
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.paste((8, 6, 7, 255), (12, 16), shadow)
    c.paste((242, 240, 234, 255), (0, 0), border)
    c.paste(im, (B, B), m)
    c.save(os.path.join(C, "sticker", f"{name}.png"), optimize=True)


if __name__ == "__main__":
    for d in ("scrap", "tex", "sticker"):
        os.makedirs(os.path.join(C, d), exist_ok=True)
    P = paper()
    for kind in COLORS:
        for k, (w, h) in enumerate([(1000, 700), (900, 520), (700, 700), (1200, 460)]):
            scrap(P, kind, w, h, 31 * k + len(kind)).save(os.path.join(C, "scrap", f"{kind}-{k}.png"), optimize=True)
    speckle().save(os.path.join(C, "tex", "speckle.png"), optimize=True)
    grunge().save(os.path.join(C, "tex", "grunge.png"), optimize=True)
    for n, s in STICKERS.items():
        sticker(n, s)
    print("wrote", C)
