"""Procedural crumpled paper (no stock images): random folds give a faceted height field, shaded by one light, plus
fibre noise and soft stains. Writes assets/img/paper.png (2040x1150, a little larger than the frame so it can drift)
and assets/img/paper-dark.png (the same sheet in charcoal).

python3 build/paper.py
"""
import os

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H, W = 1150, 2040
rng = np.random.default_rng(12)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
h = np.zeros((H, W), np.float32)
for _ in range(70):   # folds: a crease line with a slope change across it
    a = rng.uniform(0, np.pi)
    n = np.array([np.cos(a), np.sin(a)], np.float32)
    p0 = np.array([rng.uniform(0, W), rng.uniform(0, H)], np.float32)
    d = (x - p0[0]) * n[0] + (y - p0[1]) * n[1]
    h += rng.uniform(.01, .04) * np.abs(d) * (1 if rng.random() < .5 else -1) * np.exp(-np.abs(d) / rng.uniform(250, 900))
gy, gx = np.gradient(h)
shade = 1 + .75 * (-.6 * gx - .8 * gy)
shade = np.clip(shade, .84, 1.07)
sh = Image.fromarray(((shade - .8) / .3 * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
shade = np.array(sh, np.float32) / 255 * .3 + .8
fib = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
fib = np.array(Image.fromarray(((fib * 18) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 128 - 1
stain = np.array(Image.fromarray((rng.random((12, 20)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
base = np.array([232, 227, 219], np.float32)
img = base[None, None, :] * shade[..., None] * (1 + .035 * fib[..., None]) * (.94 + .08 * stain[..., None])
Image.fromarray(img.clip(0, 255).astype(np.uint8)).save(os.path.join(ROOT, "assets", "img", "paper.png"), optimize=True)
dark = np.array([38, 34, 32], np.float32)[None, None, :] * shade[..., None] * (1 + .08 * fib[..., None])
Image.fromarray(dark.clip(0, 255).astype(np.uint8)).save(os.path.join(ROOT, "assets", "img", "paper-dark.png"), optimize=True)
print("wrote assets/img/paper.png and paper-dark.png")
