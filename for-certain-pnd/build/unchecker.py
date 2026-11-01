"""Remove a fake transparency checkerboard that ChatGPT painted into an RGB image, and give back a real cut-out
(RGBA). The checker squares are white and light grey and nearly colourless; the subject is not. Pixels that match
are background when they connect to the image border. A looser match in a thin band round the subject takes the
blended checker edge too. Warm-tinted off-white (sneakers) stays.

python3 build/unchecker.py IN.png OUT.png
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src)
if im.mode == "RGBA" and np.asarray(im)[..., 3].min() < 10:      # already a real cut-out
    im.save(dst)
    print("already transparent:", dst)
    sys.exit()
a = np.asarray(im.convert("RGB")).astype(int)
sat, br = a.max(2) - a.min(2), a.mean(2)


def border_connected(mask):
    lab, _ = ndimage.label(mask)
    ids = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    return np.isin(lab, list(ids))


bg = border_connected((sat <= 7) & (br >= 196))
band = ndimage.binary_dilation(bg, iterations=7) & ~bg
bg |= band & (sat <= 16) & (br >= 150)                  # the blended checker at the subject's edge
fg = ndimage.binary_opening(~bg, iterations=2)
lab, n = ndimage.label(fg)
fg = lab == (np.argmax(ndimage.sum(fg, lab, range(1, n + 1))) + 1)
fg = ndimage.binary_fill_holes(ndimage.binary_erosion(fg, iterations=1))
alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.9))
out = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
out.putalpha(alpha)
out.save(dst)
print("cut out:", dst, f"{fg.mean():.1%} subject")
