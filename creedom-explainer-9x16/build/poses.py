"""Cut the generated Cree poses (cache/poses/raw/<name>.png, Cree on plain white) out of their background.

Owner: "make him walk, stand on two legs, move his hands, make his face expressive" and "make him exactly like that i
sent", so every pose is a render of the same 3D mascot (generated from the mascot image as the reference) rather
than a redraw.

Background removal: flood fill from the image border over near-white pixels, then a soft alpha ramp on the edge
so the pink body keeps a clean anti-aliased outline. Every pose is cropped to its bounding box and scaled with one
shared scale (the standing pose sets it), then padded onto one canvas (POSE_W x POSE_H) with the feet on one baseline,
so swapping poses never makes Cree jump.

Writes assets/img/poses/<name>.png and plan/poses.json: per pose its box on the canvas and its eyes (for the blink lids).
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "cache", "poses", "raw")
OUT = os.path.join(ROOT, "assets", "img", "poses")
POSE_W, POSE_H = 820, 820   # canvas of every pose; feet sit on BASE
BASE = 800
BODY_H = 600                # height of the standing pose (head top to feet); every pose gets the same scale
ADJ = {}                    # per-pose scale fixes where a generation framed Cree bigger or smaller
FIT_H = {"walk": 610, "pass": 610}  # framed differently (two to an image): scaled to this height instead


def cut(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    h, w, _ = im.shape
    # distance from pure white: background is ~0, the pink body is far
    d = np.sqrt(((255 - im) ** 2).sum(-1))
    near = d < 60
    lab, _ = ndimage.label(near)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    # soft edge: alpha ramps from the bg mask over ~2.5 px, and near-white fringe pixels fade
    dist = ndimage.distance_transform_edt(~bg)
    alpha = np.clip(dist / 2.5, 0, 1)
    fringe = np.clip((d - 18) / 50, 0, 1)
    alpha = np.where(dist < 4, np.minimum(alpha, np.maximum(fringe, alpha * .6)), alpha)
    # drop small specks
    lab2, n = ndimage.label(alpha > .5)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(alpha), lab2, range(1, n + 1))
        keep = np.isin(lab2, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * .02])
        alpha = alpha * ndimage.binary_dilation(keep, iterations=4)
    # un-premultiply the white fringe so edges don't glow white over coloured backgrounds
    a = alpha[..., None]
    rgb = np.where(a > .01, (im - 255 * (1 - a)) / np.maximum(a, .01), im)
    rgb = np.clip(rgb, 0, 255)
    rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    ys, xs = np.where(alpha > .5)
    return Image.fromarray(rgba).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


NOBLINK = {"cheer", "proud", "shock", "pass"}   # eyes closed, narrowed or tiny; pass: a 3/4 eye overlaps the beak


def eyes(rgba):
    """Find the two eyes in a cut pose: [(cx, cy, rx, ry, top colour, bottom colour), ...], left to right. The eye is
    everything that is not body pink (white, pale-pink rim, pupil) connected to a big dark pupil; the lid colours are
    the body just above and just beside it, so the closed lid matches the 3D shading."""
    a = np.asarray(rgba).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    lum = rgb.mean(-1)
    dark = (lum < 55) & (al > 200)
    lab, n = ndimage.label(dark)
    if n < 2:
        return [], []
    sizes = ndimage.sum(dark, lab, range(1, n + 1))
    order = np.argsort(sizes)[::-1]
    big = [i + 1 for i in order[:2] if sizes[i] > max(300, sizes[order[0]] * .35)]
    if len(big) < 2:
        return [], []
    body = (rgb[..., 0] > 150) & (rgb[..., 1] < 135) & (al > 200)
    noteye = body | (al < 128)
    out, pupils = [], []
    for i in big:
        pm = lab == i
        pupils.append(float(pm.sum()))
        r = int(np.sqrt(pm.sum() / np.pi))
        zone = ndimage.binary_dilation(pm, iterations=int(r * 1.3))
        el, _ = ndimage.label(~noteye & zone)
        keep = np.isin(el, np.unique(el[pm]))
        ys, xs = np.where(keep)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2

        def sample(y, xa, xb):
            y = int(np.clip(y, 0, rgb.shape[0] - 3))
            patch = rgb[y:y + 3, int(xa):int(xb)].reshape(-1, 3)
            m = body[y:y + 3, int(xa):int(xb)].reshape(-1)
            px = patch[m] if m.sum() > 3 else patch
            return "#%02x%02x%02x" % tuple(int(v) for v in np.median(px, 0))
        top = sample(y0 - 12, cx - rx * .4, cx + rx * .4)
        bot = sample(cy + ry * .3, x0 - 16, x0 - 6) if cx < rgb.shape[1] / 2 else sample(cy + ry * .3, x1 + 6, x1 + 16)
        tr, tg, tb = (int(top[k:k + 2], 16) for k in (1, 3, 5))
        if not (tr > 200 and tg < 150 and tb > 120):   # the lid would not be body pink (e.g. the eye behind the lens)
            continue
        out.append([round(cx), round(cy), round(rx), round(ry), top, bot])
    return sorted(out), pupils


def main(names=None):
    os.makedirs(OUT, exist_ok=True)
    files = sorted(f for f in os.listdir(RAW) if f.endswith(".png"))
    meta = {}
    ref_cut = cut(os.path.join(RAW, "stand.png"))
    ref = ref_cut.height
    for f in files:
        name = f[:-4]
        if names and name not in names:
            continue
        c = cut(os.path.join(RAW, f))
        s = BODY_H / ref * ADJ.get(name, 1)
        if name in FIT_H:
            s = FIT_H[name] / c.height
        s = min(s, (POSE_W - 10) / c.width, (POSE_H - 30) / c.height)
        c = c.resize((round(c.width * s), round(c.height * s)), Image.LANCZOS)
        canvas = Image.new("RGBA", (POSE_W, POSE_H), (0, 0, 0, 0))
        canvas.paste(c, ((POSE_W - c.width) // 2, BASE - c.height), c)
        canvas.save(os.path.join(OUT, name + ".png"), optimize=True)
        ex = (POSE_W - c.width) // 2
        ey = BASE - c.height
        meta[name] = {"box": [ex, ey, c.width, c.height], "eyes": [] if name in NOBLINK else eyes(canvas)[0]}
        print(name, c.size)
    with open(os.path.join(ROOT, "plan", "poses.json"), "w") as fh:
        json.dump(meta, fh, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
