"""Displacement maps that bring the anime illustrations to life (wind in hair and clothes, breathing edges).

python3 build/animaps.py      (after build/anime.py)

For every image in plan/anime.json writes assets/img/anime/map/<name>.png, an RGB displacement map for an SVG
feDisplacementMap (R = x shift, G = y shift, 128 = still). The motion is strongest at the outline of the figure
(outer hair strands, hoodie edges, the dress hem) and grows with height above the feet, so faces and the middle of
the drawing stay put while the edges flutter. Two smooth noise fields give each region its own direction, so one
animated filter scale reads as wind rather than a slide. Full-frame pictures use the subject found by the local
u2net model (cache/models/u2net.onnx) as the figure. For the smoke and fire pictures it also writes
assets/img/anime/flow/<name>.png, the smoke or flame area (alpha) that a drifting noise field makes flow.
"""
import json
import os

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "assets", "img", "anime")
_S = []


def subject(img):
    if not _S:
        _S.append(ort.InferenceSession(os.path.join(ROOT, "cache", "models", "u2net.onnx")))
    x = np.asarray(img.convert("RGB").resize((320, 320), Image.LANCZOS), np.float32) / 255
    x = (x - [.485, .456, .406]) / [.229, .224, .225]
    out = _S[0].run(None, {"input.1": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    return np.asarray(Image.fromarray((out * 255).astype(np.uint8)).resize(img.size, Image.LANCZOS), np.float32) / 255 > .5


def noise(shape, sigma, seed):
    n = ndimage.gaussian_filter(np.random.default_rng(seed).normal(0, 1, shape), sigma)
    return n / (np.abs(n).max() + 1e-6)


def make(img, alpha, seed):
    H, W = alpha.shape
    inside = alpha
    d = ndimage.distance_transform_edt(inside)
    edge = np.exp(-d / (W * .035))                      # the outline moves, the middle holds
    ys = np.nonzero(inside.any(1))[0]
    top, bot = (ys.min(), ys.max()) if len(ys) else (0, H)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    h = ((bot - yy) / max(1, bot - top)).clip(0, 1) ** 1.3   # feet anchored, heads and hair move most
    w = h * (.25 + .75 * edge)
    w = ndimage.gaussian_filter(w * ndimage.binary_dilation(inside, iterations=int(W * .03)), W * .006)
    n1, n2 = noise((H, W), W * .05, seed), noise((H, W), W * .05, seed + 1)
    dx = (.45 + .55 * n1) * w                            # mostly one way (wind), each region its own amount
    dy = .35 * n2 * w
    m = np.stack([128 + 127 * dx.clip(-1, 1), 128 + 127 * dy.clip(-1, 1), np.full_like(dx, 128)], -1)
    return Image.fromarray(m.astype(np.uint8))


def flow_mask(im, person, kind):
    """Where smoke or fire should flow: white with the region in the alpha channel."""
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    mx, mn = a.max(-1), a.min(-1)
    sat = (mx - mn) / (mx + 1e-6)
    if kind == "fire":
        m = (a[..., 0] > .55) & (sat > .45) & (a[..., 0] >= a[..., 1])      # reds, oranges, yellows
    else:
        m = (sat < .35) & (mx > .22) & (mx < .9)                            # the grey-blue smoke
    m &= ~ndimage.binary_dilation(person, iterations=int(im.size[0] * .02))
    m = ndimage.binary_opening(m, iterations=2)
    al = ndimage.gaussian_filter(m.astype(np.float32), im.size[0] * .01)
    out = np.zeros((*m.shape, 4), np.uint8)
    out[..., :3] = 255
    out[..., 3] = (al.clip(0, 1) * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


FLOW = {"smoke": "smoke", "fire": "fire"}


def main():
    spec = json.load(open(os.path.join(ROOT, "plan", "anime.json")))
    os.makedirs(os.path.join(D, "map"), exist_ok=True)
    for k, it in enumerate(spec["images"]):
        name = it["name"]
        cut = os.path.join(D, "cut", f"{name}.png")
        if it["bg"] == "white" and os.path.exists(cut):
            im = Image.open(cut)
            alpha = np.asarray(im.split()[3]) > 128
        else:
            im = Image.open(os.path.join(D, "full", f"{name}.jpg"))
            alpha = subject(im)
        make(im, alpha, 10 + k).save(os.path.join(D, "map", f"{name}.png"))
        if name in FLOW:
            os.makedirs(os.path.join(D, "flow"), exist_ok=True)
            flow_mask(im, alpha, FLOW[name]).save(os.path.join(D, "flow", f"{name}.png"))
        print(name)


if __name__ == "__main__":
    main()
