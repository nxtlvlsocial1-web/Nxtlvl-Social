"""v10: the crumple of build/paper.py as a see-through texture for the gradient background (the paper colour and its
grid are gone; the owner asked for a gradient). Highlights become white, creases black, flat paper transparent, so the
folds catch the light over the gradient and move with the camera. Writes assets/img/crumple.png (2600x3900).

python3 build/crumple.py      (after build/paper.py)
"""
import os

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = np.asarray(Image.open(os.path.join(ROOT, "assets", "img", "paper.png")).convert("L"), np.float32)
d = L - np.median(L)
k = 255 / max(1.0, np.percentile(np.abs(d), 99.5))
a = np.clip(np.abs(d) * k, 0, 255)
rgb = np.where(d[..., None] > 0, 255, 0).astype(np.uint8) * np.ones(3, np.uint8)
out = np.dstack([rgb, a.astype(np.uint8)])
Image.fromarray(out, "RGBA").save(os.path.join(ROOT, "assets", "img", "crumple.png"), optimize=True)
print("wrote assets/img/crumple.png")
