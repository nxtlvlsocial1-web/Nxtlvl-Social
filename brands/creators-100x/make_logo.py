"""Cut the Creators 100X logo out of the supplied square artwork (logo-square.png, light gradient background) into
transparent PNGs: logo.png (tile + wordmark) and logo-mark.png (the tile). Pixels are un-mixed from the light
background (alpha = how far a pixel is from it), the rounded black tile is kept fully opaque (its white bolt half
must not turn transparent), faint background residue is cut. For light backgrounds (the brand's own).
python3 brands/creators-100x/make_logo.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
src = np.asarray(Image.open(os.path.join(D, "logo-square.png")).convert("RGB")).astype(float)
X0, Y0, X1, Y1 = 150, 470, 1110, 815
a = src[Y0:Y1, X0:X1]
h, w, _ = a.shape
bg = np.array([253, 245, 244], float)
al = np.clip((bg - a) / bg, 0, 1).max(axis=2) * 1.06
al = np.where(al < .08, 0, np.clip((al - .08) / .92, 0, 1))
m = Image.new("L", (w * 4, h * 4), 0)       # the tile, drawn 4x and scaled down for a smooth edge, 3 px inside its rim
ImageDraw.Draw(m).rounded_rectangle(((163 - X0) * 4, (491 - Y0) * 4, (478 - X0) * 4, (797 - Y0) * 4), radius=89 * 4, fill=255)
tile = np.asarray(m.resize((w, h), Image.LANCZOS)).astype(float) / 255
inside = tile > .99
al = np.where(inside, 1, np.where(tile > 0, np.maximum(al * (1 - tile), 0) + tile * np.clip((bg - a).max(axis=2) / 200, 0, 1), al))
rgb = np.clip((a - (1 - al[..., None]) * bg) / np.maximum(al, 1e-3)[..., None], 0, 255)
rgb = np.where(tile[..., None] > 0, np.minimum(a, 40) * (1 - inside[..., None]) + a * inside[..., None], rgb)
out = Image.fromarray(np.dstack([rgb, al * 255]).astype(np.uint8), "RGBA")
full = out.crop(out.getbbox())
full.save(os.path.join(D, "logo.png"))
out.crop((160 - X0, 488 - Y0, 482 - X0, 801 - Y0)).save(os.path.join(D, "logo-mark.png"))
print("logo.png", full.size)
