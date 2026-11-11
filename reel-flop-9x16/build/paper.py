"""Paper textures for the papercraft look (v4, owner's reference: crumpled-paper worlds, cut-out props; owner picked
black/white papercraft, props built in code). Made procedurally here, so they are ours:
  * crumple: a jittered Voronoi of facets, each lit slightly differently from one light direction, softened; crease
    lines where facets meet;
  * fibres: fine grain at two scales;
  * a vignette.
Writes assets/img/paper_{light,mid,dark}.jpg (1080x1920) and paper_tile.jpg (a 512 px tile for props).
python3 build/paper.py
"""
import os

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")


def crumple(w, h, n, seed, strength):
    r = np.random.default_rng(seed)
    pts = r.uniform([0, 0], [w, h], size=(n, 2))
    yy, xx = np.mgrid[0:h, 0:w]
    d, idx = cKDTree(pts).query(np.c_[xx.ravel(), yy.ravel()], k=2)
    idx = idx[:, 0].reshape(h, w)
    edge = (d[:, 1] - d[:, 0]).reshape(h, w)
    normal = r.normal(0, 1, size=(n, 2))
    light = normal @ np.array([.6, -.8])
    shade = light[idx] * strength
    shade = ndimage.gaussian_filter(shade, 4)
    crease = np.exp(-edge / .9) * strength * 1.1
    return shade - crease


def grain(w, h, seed):
    r = np.random.default_rng(seed)
    g = ndimage.gaussian_filter(r.normal(0, 1, (h, w)), .7) * 2.2 + ndimage.gaussian_filter(r.normal(0, 1, (h, w)), 2.5) * 3.0
    return g


def make(name, base, w=1080, h=1920, seed=1, strength=6.0, vign=.22):
    img = np.full((h, w), float(base))
    # crumple at two scales, computed small and upscaled (fast)
    def up(a):
        return ndimage.zoom(a, (h / a.shape[0], w / a.shape[1]), order=1)[:h, :w]
    img += up(crumple(w // 3, h // 3, 45, seed, strength * 1.3))
    img += up(crumple(w // 2, h // 2, 140, seed + 7, strength * .35))
    r = np.random.default_rng(seed + 9)
    mott = up(ndimage.gaussian_filter(r.normal(0, 1, (h // 8, w // 8)), 5)) * 9 + up(ndimage.gaussian_filter(r.normal(0, 1, (h // 4, w // 4)), 3)) * 3
    img += mott
    img += grain(w, h, seed + 3)
    yy, xx = np.mgrid[0:h, 0:w]
    v = ((xx - w / 2) / (w * .75)) ** 2 + ((yy - h * .45) / (h * .7)) ** 2
    img *= 1 - vign * np.clip(v, 0, 1.4)
    rgb = np.stack([img, img * .995, img * .985], -1)           # a hint of paper warmth, still reads black/white
    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name), quality=88)


def main():
    os.makedirs(OUT, exist_ok=True)
    make("paper_light.jpg", 236, seed=1)
    make("paper_mid.jpg", 172, seed=2)
    make("paper_dark.jpg", 52, seed=3, strength=4.0, vign=.3)
    make("paper_tile.jpg", 244, w=512, h=512, seed=4, strength=4.0, vign=0)
    print("wrote paper textures")


if __name__ == "__main__":
    main()
