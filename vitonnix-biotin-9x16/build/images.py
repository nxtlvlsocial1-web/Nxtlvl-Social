"""Prepare the client's images for the Vitonnix Biotin reel.

python3 -I build/images.py source     (from the project root; needs Pillow, numpy, scipy)

Sources are Vitonnix's own marketing images, supplied by the client on 29 Oct 2026:
  2.webp  lifestyle post "A Spray a Day for Stunning Hair, Skin and Nails" (woman + three benefit icons)
  3.webp  Biotin packshot in a white capsule card, with food photos
  4.webp  spray mist post "9X better absorption"
  5.png   "Your health, our promise" certification badges
Baked-in text is removed from the mist shot (normalized-convolution fill) so we can set our own type and drop the
"hasle-free" typo. Writes assets/img/*.png|jpg.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import binary_dilation, gaussian_filter

SRC = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)


def circle_crop(im, cx, cy, r, size=None):
    box = (cx - r, cy - r, cx + r, cy + r)
    c = im.crop(box).convert("RGBA")
    m = Image.new("L", (2 * r * 4, 2 * r * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * r * 4 - 1, 2 * r * 4 - 1), fill=255)
    m = m.resize((2 * r, 2 * r), Image.LANCZOS)
    c.putalpha(m)
    if size:
        c = c.resize((size, size), Image.LANCZOS)
    return c


def fill(img, mask):
    """Fill masked pixels from their surroundings: coarse-to-fine normalized convolution, plus matched grain."""
    out = img.copy()
    known = (~mask).astype(np.float64)
    num = np.stack([gaussian_filter(out[..., c] * known, 60) for c in range(3)], -1)
    den = gaussian_filter(known, 60)[..., None] + 1e-9
    out[mask] = (num / den)[mask]                       # coarse fill from the surroundings
    for sigma in (30, 15, 7, 3):                        # then relax it toward the edges
        est = np.stack([gaussian_filter(out[..., c], sigma) for c in range(3)], -1)
        out[mask] = est[mask]
    rng = np.random.default_rng(3)
    out[mask] += rng.normal(0, 2.0, (mask.sum(), 3))
    return np.clip(out, 0, 255)


# --- mist shot without text
im = np.asarray(Image.open(os.path.join(SRC, "4.webp")).convert("RGB")).astype(np.float64)
H, W, _ = im.shape
lum = im @ np.array([.299, .587, .114])
mask = np.zeros((H, W), bool)
for x0, y0, x1, y1 in [(755, 140, 995, 292), (50, 680, 335, 1012)]:          # text on smooth plum: whole box
    mask[y0:y1, x0:x1] = True
for x0, y0, x1, y1 in [(556, 158, 790, 190), (552, 156, 586, 256)]:          # dashed connector, top
    mask[y0:y1, x0:x1] |= lum[y0:y1, x0:x1] > 150
for x0, y0, x1, y1 in [(160, 486, 410, 580), (166, 276, 196, 486), (166, 274, 240, 302)]:   # text + dashes over mist
    mask[y0:y1, x0:x1] |= lum[y0:y1, x0:x1] > 150
mask = binary_dilation(mask, iterations=5)
clean = fill(im, mask)
Image.fromarray(clean.astype(np.uint8)).save(os.path.join(OUT, "mist.jpg"), quality=93)

# --- packshot in its white capsule card, corners transparent
im3 = Image.open(os.path.join(SRC, "3.webp")).convert("RGBA")
x0, y0, x1, y1 = 798, 512, 1202, 1638
card = im3.crop((x0, y0, x1, y1))
w, h = card.size
m = Image.new("L", (w * 4, h * 4), 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 4 - 1, h * 4 - 1), radius=w * 2, fill=255)
card.putalpha(m.resize((w, h), Image.LANCZOS))
card.save(os.path.join(OUT, "packshot.png"))

# --- lifestyle photo, right side (no baked-in text)
im2 = Image.open(os.path.join(SRC, "2.webp")).convert("RGB")
im2.crop((452, 0, 1080, 668)).save(os.path.join(OUT, "glow.jpg"), quality=94)
for name, cx in (("ic-hair", 180), ("ic-nail", 530), ("ic-skin", 877)):
    circle_crop(im2, cx, 781, 101, 240).save(os.path.join(OUT, name + ".png"))

# --- certification badges
im5 = Image.open(os.path.join(SRC, "5.png")).convert("RGB")
cols = (165, 410, 660, 905)
names = [["b-easy", "b-efficacy", "b-absorb", "b-nongmo"], ["b-fssc", "b-sugar", "b-gmp", "b-fssai"]]
for row, cy in enumerate((488, 779)):
    for col, cx in enumerate(cols):
        circle_crop(im5, cx, cy, 98, 260).save(os.path.join(OUT, names[row][col] + ".png"))
print("images written:", sorted(os.listdir(OUT)))
