"""Image treatments for the Spin Bout U edit, from the owner's photos in assets/img/src/ (kept out of git).

python3 build/assets.py [--sheet]      (from the project root; needs Pillow, numpy, scipy, onnxruntime and the rembg
models cache/models/u2net_human_seg.onnx (people) and cache/models/u2net.onnx (cats, the phone sticker))

The look follows the owner's references (a Spin Bout U edit and an MJ "Smooth Criminal" edit): hard black-and-white
photos with a coarse 45-degree halftone screen in the mid-tones and shadows. Writes assets/img/cut/<name>.png (the
subject cut out, local segmentation, no upload) and assets/img/print/<name>.jpg (the whole photo in the same look).
"""
import os
import sys

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "img", "src")
# name: (model, x of the subject as a fraction or None, keep only the largest blob)
CUTS = {"drake_laugh_hands": ("human", .5), "drake_chanel_night": ("human", .5), "drake_nocta_red": ("human", .5),
        "drake_back_jacket": ("human", .5), "drake_boat_sunset": ("human", .55), "cat_black_collar": ("general", .5),
        "cat_white_dumb": ("general", .5), "hand_phone_sticker": ("general", .5)}
PRINTS = ["vogue_cat_cover", "envogue_funky_divas", "rolex_cat_ad", "drake_boat_sunset", "drake_back_jacket",
          "drake_chanel_night", "drake_nocta_red", "drake_laugh_hands", "cat_black_collar", "cat_white_dumb"]
_S = {}


def session(kind):
    if kind not in _S:
        f = "u2net_human_seg.onnx" if kind == "human" else "u2net.onnx"
        _S[kind] = ort.InferenceSession(os.path.join(ROOT, "cache", "models", f))
    return _S[kind]


def mask(img, kind, fx):
    x = np.asarray(img.resize((320, 320), Image.LANCZOS), np.float32) / 255
    x = (x - [.485, .456, .406]) / [.229, .224, .225]
    out = session(kind).run(None, {"input.1": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    m = np.asarray(Image.fromarray((out * 255).astype(np.uint8)).resize(img.size, Image.LANCZOS), np.float32) / 255
    lab, n = ndimage.label(m > .5)
    if n > 1:                                    # keep the blob nearest fx (the subject), drop stray bits
        sizes = ndimage.sum(np.ones_like(m), lab, range(1, n + 1))
        best = max(range(1, n + 1), key=lambda k: sizes[k - 1] - 1e5 * abs(np.nonzero(lab == k)[1].mean() / img.size[0] - fx))
        m = m * ndimage.binary_dilation(lab == best, iterations=4)
    m = np.maximum(m * (m > .45), ndimage.binary_fill_holes(m > .5).astype(np.float32))
    return Image.fromarray((m.clip(0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))


def halftone(img, cell=7, mix=.42, lift=1.0, inside=None):
    """Hard B&W with a 45-degree clustered-dot screen blended in (the references' grit)."""
    g = np.asarray(img.convert("L"), np.float32) / 255
    ref = g[inside > 128] if inside is not None else g.ravel()
    lo, hi = np.percentile(ref, 1.5), np.percentile(ref, 99)
    g = ((g - lo) / max(.05, hi - lo)).clip(0, 1)
    mean = ref.mean() if inside is None else ((ref - lo) / max(.05, hi - lo)).clip(0, 1).mean()
    if mean < .38:                               # dark night shots: lift so faces read
        g = g ** max(.6, np.log(.45) / np.log(max(mean, .05)))
    g = ((g - .5) * 1.35 + .5).clip(0, 1) ** lift
    h, w = g.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = (xx + yy) / (cell * 1.414), (xx - yy) / (cell * 1.414)
    d = np.sqrt((u - np.round(u)) ** 2 + (v - np.round(v)) ** 2) / .7071      # 0 at a dot centre, 1 at the corner
    dots = (g > d).astype(np.float32)
    out = g * (1 - mix) + dots * mix
    out = np.where(g > .82, g, out)              # highlights stay clean
    im = Image.fromarray((out.clip(0, 1) * 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(2, 120, 2))
    return im


def cut(name, kind, fx):
    img = Image.open(os.path.join(SRC, f"{name}.jpg")).convert("RGB")
    s = min(1.0, 1500 / max(img.size))
    img = img.resize((round(img.size[0] * s), round(img.size[1] * s)), Image.LANCZOS)
    m = mask(img, kind, fx)
    box = m.point(lambda v: 255 if v > 90 else 0).getbbox()
    img, m = img.crop(box), m.crop(box)
    ht = halftone(img, inside=np.asarray(m)).convert("RGBA")
    ht.putalpha(m)
    ht.save(os.path.join(ROOT, "assets", "img", "cut", f"{name}.png"), optimize=True)
    return ht


def prints():
    for name in PRINTS:
        img = Image.open(os.path.join(SRC, f"{name}.jpg")).convert("RGB")
        s = min(1.0, 1400 / max(img.size))
        img = img.resize((round(img.size[0] * s), round(img.size[1] * s)), Image.LANCZOS)
        mix = .2 if name in ("vogue_cat_cover", "rolex_cat_ad", "cat_white_dumb") else .42      # the magazine pages are type: light screen
        halftone(img, mix=mix).save(os.path.join(ROOT, "assets", "img", "print", f"{name}.jpg"), quality=90)


if __name__ == "__main__":
    for d in ("cut", "print"):
        os.makedirs(os.path.join(ROOT, "assets", "img", d), exist_ok=True)
    made = [(n, cut(n, *v)) for n, v in CUTS.items()]
    prints()
    if "--sheet" in sys.argv:
        th = []
        for n, im in made:
            im = im.copy()
            im.thumbnail((300, 420))
            th.append(im)
        sheet = Image.new("RGB", (4 * 310, 2 * 430), (162, 37, 73))
        for i, im in enumerate(th):
            sheet.paste(im, ((i % 4) * 310, (i // 4) * 430), im)
        sheet.save(os.path.join(ROOT, "cache", "cut_sheet.png"))
    print("wrote assets/img/cut and assets/img/print")
