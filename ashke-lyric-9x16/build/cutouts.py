"""Photocopied cut-out stickers of Karan, like the cut-out people in the owner's YouMotion reference.

python3 build/cutouts.py [--sheet]      (from the project root; needs ffmpeg, Pillow, numpy, scipy, onnxruntime and
cache/models/u2net_human_seg.onnx, the rembg human-segmentation model from github.com/danielgatis/rembg releases)

For each pick (source clip, time, where Karan stands across the frame) the frame is segmented locally (no upload), the
person nearest that point is kept, and the cut-out is photocopied (grey, auto-levels inside the person, hard curve,
sharpened, fine grain), given a white paper border and a soft baked shadow. Writes assets/img/cut/<name>.png (and
<name>-red.png, the red duotone variant). --sheet also writes cache/cut_sheet.png to check them.
Sources stay out of git: assets/video/src/estate.mp4 and tour.mp4 (the owner's clips) and the music video.
"""
import os
import subprocess
import sys

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "assets", "video")
SRC = {"estate": os.path.join(V, "src", "estate.mp4"), "tour": os.path.join(V, "src", "tour.mp4"), "mv": os.path.join(V, "music-video-src.mp4")}
OUT = os.path.join(ROOT, "assets", "img", "cut")
# name: (source, time s, x of Karan as a fraction of the frame width)
PICKS = {   # Karan only. (src, time, x of Karan, optional x window that clips away anyone standing next to him)
    "suit": ("estate", 1.8, .52), "plaid": ("estate", 42.9, .55, (.36, .78)), "poster": ("tour", 2.2, .5),
    "selfie_a": ("tour", 10.6, .5), "selfie_b": ("tour", 11.4, .52), "selfie_c": ("tour", 12.4, .5), "mic": ("tour", 41.6, .45),
    "walk": ("tour", 44.8, .5), "walk_b": ("tour", 45.6, .5), "arms": ("tour", 49.2, .5), "back": ("tour", 50.4, .5),
    "stage": ("tour", 54.2, .5),
}
_sess = None


def grab(src, t):
    p = os.path.join(ROOT, "cache", "cut_frame.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", SRC[src], "-frames:v", "1", p], check=True)
    return Image.open(p).convert("RGB")


def person_mask(img, fx, win=None):
    global _sess
    if _sess is None:
        _sess = ort.InferenceSession(os.path.join(ROOT, "cache", "models", "u2net_human_seg.onnx"))
    x = np.asarray(img.resize((320, 320), Image.LANCZOS), np.float32) / 255
    x = (x - [.485, .456, .406]) / [.229, .224, .225]
    out = _sess.run(None, {"input.1": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    m = np.asarray(Image.fromarray((out * 255).astype(np.uint8)).resize(img.size, Image.LANCZOS), np.float32) / 255
    lab, n = ndimage.label(m > .5)
    if n > 1:                       # keep the person standing nearest fx
        best, bd = 1, 1e9
        for k in range(1, n + 1):
            ys, xs = np.nonzero(lab == k)
            if len(xs) < 2000:
                continue
            d = abs(xs.mean() / img.size[0] - fx)
            if d < bd:
                best, bd = k, d
        keep = ndimage.binary_dilation(lab == best, iterations=3)
        m = m * keep
    m = np.maximum(m * (m > .5), ndimage.binary_fill_holes(m > .5).astype(np.float32))   # drop the haze, fill holes
    if win:                         # clip away anyone touching him
        w = m.shape[1]
        m[:, : int(win[0] * w)] = 0
        m[:, int(win[1] * w):] = 0
    return Image.fromarray((m.clip(0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))


def photocopy(img, m, seed):
    g = np.asarray(img.convert("L"), np.float32)
    inside = g[np.asarray(m) > 128]
    lo, hi = np.percentile(inside, 2), np.percentile(inside, 98)
    g = ((g - lo) / max(1, hi - lo)).clip(0, 1)
    mean = g[np.asarray(m) > 128].mean()
    g = g ** (1.1 if mean > .45 else max(.55, np.log(.48) / np.log(max(mean, .05))))   # lift dark shots so faces read
    g = (g - .5) * 1.55 + .52
    g = g.clip(0, 1) * 255
    im = Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.UnsharpMask(3, 160, 2))
    a = np.asarray(im, np.float32) + np.random.default_rng(seed).normal(0, 7, g.shape)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def sticker(name, src, t, fx, seed, win=None):
    img = grab(src, t)
    m = person_mask(img, fx, win)
    bbox = m.point(lambda v: 255 if v > 100 else 0).getbbox()
    pad = 40
    box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(img.size[0], bbox[2] + pad), min(img.size[1], bbox[3] + pad))
    img, m = img.crop(box), m.crop(box)
    s = min(1.6, 1000 / img.size[1])
    size = (round(img.size[0] * s), round(img.size[1] * s))
    img, m = img.resize(size, Image.LANCZOS), m.resize(size, Image.LANCZOS)
    pc = photocopy(img, m, seed)
    B = 18                                   # white paper border and room for the shadow
    W, H = size[0] + 2 * B + 30, size[1] + 2 * B + 30
    mm = Image.new("L", (W, H))
    mm.paste(m, (B, B))
    border = mm.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(1))
    shadow = border.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * .42))
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.paste((10, 10, 10, 255), (12, 16), shadow)
    canvas.paste((244, 242, 236, 255), (0, 0), border)
    canvas.paste(pc.convert("RGB"), (B, B), m)
    out = canvas
    out.save(os.path.join(OUT, f"{name}.png"), optimize=True)
    # red duotone variant: blacks stay black, lights go red
    r = np.asarray(out, np.float32).copy()
    lum = r[..., :3].mean(-1, keepdims=True) / 255
    paper = (np.abs(r[..., :3] - [244, 242, 236]).sum(-1, keepdims=True) < 6)
    red = np.concatenate([lum * 232, lum * 30, lum * 40], -1)
    r[..., :3] = np.where(paper, r[..., :3], red)
    Image.fromarray(r.clip(0, 255).astype(np.uint8), "RGBA").save(os.path.join(OUT, f"{name}-red.png"), optimize=True)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    made = []
    for k, (name, pick) in enumerate(PICKS.items()):
        made.append((name, sticker(name, *pick[:3], k, pick[3] if len(pick) > 3 else None)))
        print(name)
    if "--sheet" in sys.argv:
        th = [im.copy() for _, im in made]
        for im in th:
            im.thumbnail((300, 380))
        sheet = Image.new("RGB", (6 * 300, ((len(th) + 5) // 6) * 380), (200, 190, 180))
        for i, im in enumerate(th):
            sheet.paste(im, ((i % 6) * 300, (i // 6) * 380), im)
        sheet.save(os.path.join(ROOT, "cache", "cut_sheet.png"))
