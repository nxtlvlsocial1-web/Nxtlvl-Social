"""Photocopy textures for the collage strips and panels, all procedural.

python3 build/textures.py      (from the project root; needs Pillow and numpy)

Writes assets/img/tex/: diamond.png (diamond-plate metal), blocks.png (black and white pixel-block mosaic),
news.png (greeked newspaper columns: headline bars and lines of "text", no real copy). Halftone dots, hazard stripes,
line patterns and the starbursts are CSS / SVG in generate.py.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "tex")


def photocopy(img, contrast=1.9, noise=10, seed=0):
    a = np.asarray(img.convert("L"), dtype=np.float32)
    a = (a - 128) * contrast + 128
    a += np.random.default_rng(seed).normal(0, noise, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def diamond(w=720, h=720, cell=60):
    g = random.Random(1)
    base = (np.random.default_rng(2).normal(92, 20, (h, w))).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(base).filter(ImageFilter.GaussianBlur(1.2))
    d = ImageDraw.Draw(img)
    for j in range(-1, h // cell + 2):
        for i in range(-1, w // cell + 2):
            cx, cy = i * cell + (cell / 2 if j % 2 else 0), j * cell
            ang = math.radians(45 if (i + j) % 2 else -45)
            L, T = cell * .42, cell * .09
            ux, uy, vx, vy = math.cos(ang), math.sin(ang), -math.sin(ang), math.cos(ang)
            pts = [(cx + ux * L, cy + uy * L), (cx + vx * T, cy + vy * T), (cx - ux * L, cy - uy * L), (cx - vx * T, cy - vy * T)]
            d.polygon([(x + 3, y + 3) for x, y in pts], fill=30)            # shadow side
            d.polygon(pts, fill=g.randint(215, 245))                          # lit ridge
    return photocopy(img.filter(ImageFilter.GaussianBlur(.6)), 1.5, 9, 3)


def blocks(w=640, h=1080, bs=40):
    g = random.Random(7)
    img = Image.new("L", (w, h), 240)
    d = ImageDraw.Draw(img)
    for y in range(0, h, bs):
        x, run = 0, g.random() < .5
        while x < w:
            n = g.choice([1, 1, 2, 3, 5])
            if run:
                d.rectangle([x, y, x + n * bs - 1, y + bs // 2 * g.choice([1, 2]) - 1], fill=15)
            x += n * bs
            run = not run
    return photocopy(img, 1.2, 6, 8)


def news(w=760, h=560):
    g = random.Random(11)
    img = Image.new("L", (w, h), 232)
    d = ImageDraw.Draw(img)
    d.rectangle([20, 18, w - 20, 70], fill=25)                               # masthead bar
    for k in range(9):
        d.rectangle([40 + k * 72, 30, 40 + k * 72 + 52, 58], fill=225)       # masthead "letters"
    cols = 4
    cw = (w - 40) // cols
    for c in range(cols):
        x0, y = 20 + c * cw + 8, 90
        if c == 1:
            d.rectangle([x0, y, x0 + cw - 16, y + 120], fill=60)             # a photo block
            y += 132
        while y < h - 16:
            if g.random() < .07:
                d.rectangle([x0, y, x0 + int((cw - 16) * g.uniform(.6, 1)), y + 12], fill=20)   # subhead
                y += 22
                continue
            x = x0
            while x < x0 + cw - 20:
                ww = g.randint(10, 46)
                d.rectangle([x, y, min(x + ww, x0 + cw - 16), y + 5], fill=g.randint(40, 90))  # a word
                x += ww + 6
            y += 11
    return photocopy(img, 1.4, 12, 12)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    diamond().save(os.path.join(OUT, "diamond.png"))
    blocks().save(os.path.join(OUT, "blocks.png"))
    news().save(os.path.join(OUT, "news.png"))
    print("wrote", OUT)
