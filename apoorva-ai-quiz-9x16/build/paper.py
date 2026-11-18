"""Paper strip for the v4 lower third (after the owner's Canva design DAHbRZ-IIlc): warm newsprint with fibre noise and a
torn top edge (alpha), 1080 x 640. Also a torn-ink stamp texture mask. python3 build/paper.py"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)
W, H = 1080, 640
base = np.array([238, 228, 210], dtype=np.float32)
noise = rng.normal(0, 1, (H, W)).astype(np.float32)
img = Image.fromarray(((noise - noise.min()) / (noise.ptp()) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
n1 = np.asarray(img, dtype=np.float32) / 255 - .5
blot = Image.fromarray(((rng.random((H // 40, W // 40)) * 255)).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
n2 = np.asarray(blot, dtype=np.float32) / 255 - .5
y = np.linspace(0, 1, H)[:, None]
rgb = base[None, None, :] + (n1 * 14)[..., None] + (n2 * 18)[..., None] - (y * 10)[..., None]
# torn top edge: a jagged line with small fibres
xs = np.arange(W)
edge = 34 + 8 * np.sin(xs / 37.0) + 5 * np.sin(xs / 11.0 + 1) + np.cumsum(rng.normal(0, 1.4, W)) * .35
edge = edge - edge.min() + 14
alpha = np.zeros((H, W), dtype=np.float32)
for x in range(W):
    e = int(edge[x])
    alpha[e:, x] = 1
    alpha[max(0, e - 3):e, x] = rng.random(min(3, e)) * .7
a = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6))
# a lighter fibrous rim just under the tear
rim = np.zeros((H, W), dtype=np.float32)
for x in range(W):
    e = int(edge[x])
    rim[e:e + 6, x] = 1
rgb = rgb + (rim * 14)[..., None]
out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
out.putalpha(a)
out.save(os.path.join(ROOT, "assets", "img", "paper.png"))
# ink texture for rubber stamps: speckled mask (white = ink)
m = rng.random((240, 640))
ink = (m > .12).astype(np.float32)
ink = Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8))
ink.save(os.path.join(ROOT, "assets", "img", "ink.png"))
print("ok")
