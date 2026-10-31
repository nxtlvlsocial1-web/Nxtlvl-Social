"""Anime illustrations for the v3 edit: cut-outs and full frames from the Canva-generated art (plan/anime.json).

python3 build/anime.py      (from the project root; needs Pillow, numpy, scipy)

Input: assets/img/anime/src/<name>.png or .jpg (downloaded from the owner's Canva account; kept out of git).
Output, for every image:
  assets/img/anime/full/<name>.jpg   the whole picture at 1280 px, as painted (a light levels stretch only)
  assets/img/anime/cut/<name>.png    white-background pictures only: the characters cut out. The background is the
                                     flat paper colour (read off the top corners) joined to the frame edge, after closing small gaps in the ink
                                     lines (manga line art on white has skin and highlights that are white too, so a
                                     plain white key would punch holes in faces). A missing source gets a grey
                                     placeholder with its name so the edit can be laid out before the art arrives.
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "assets", "img", "anime")
SIZE = 1280
PAPER = np.array([242, 240, 235], np.float32)
INK = np.array([13, 13, 13], np.float32)


def load(name):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(D, "src", f"{name}.{ext}")
        if os.path.exists(p):
            return Image.open(p).convert("RGB"), False
    im = Image.new("RGB", (SIZE, SIZE), (120, 120, 120))
    d = ImageDraw.Draw(im)
    d.ellipse((340, 200, 940, 1240), fill=(70, 70, 70))
    f = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Anton.ttf"), 120)
    d.text((SIZE / 2, 120), name.upper(), font=f, fill=(230, 230, 230), anchor="mm")
    return im, True


def tone(im):
    """The 90s cel look stays as painted: only a gentle levels stretch so the blacks sit with the edit's black."""
    a = np.asarray(im, np.float32) / 255
    lo = np.percentile(a.mean(-1), 1)
    out = ((a - lo) / max(.5, 1 - lo)).clip(0, 1)
    return Image.fromarray((out * 255).astype(np.uint8))


def cutout(im, key=60, holes=True):
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(2.5)), np.float32)     # paper grain off
    k = max(4, im.size[0] // 40)                 # the flat paper colour, read off the top corners
    paper = np.median(np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3)]), 0)
    ink = np.abs(a - paper).sum(-1) > key
    s = im.size[0] / 1280
    gap = max(1, round(3 * s))
    closed = ndimage.binary_dilation(ink, iterations=gap)
    lab, n = ndimage.label(~closed)
    edge = set(np.unique(np.concatenate([lab[0], lab[:, 0], lab[:, -1]]))) - {0}     # not the bottom edge: figures run off it
    bg = np.isin(lab, list(edge))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))   # big enclosed paper patches (between arms) go too
    if holes:
        bg |= np.isin(lab, [k + 1 for k, v in enumerate(sizes) if v > lab.size * .004])
    bg = ndimage.binary_dilation(bg, iterations=gap) & ~ink    # give back what the closing took
    m = ~bg
    lab, n = ndimage.label(m)                        # drop specks
    if n > 1:
        sizes = ndimage.sum(np.ones_like(m), lab, range(1, n + 1))
        keep = [k + 1 for k, v in enumerate(sizes) if v > m.size * .002]
        m = np.isin(lab, keep)
    mm = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8 * max(1, s)))
    out = im.convert("RGBA")
    out.putalpha(mm)
    box = mm.point(lambda v: 255 if v > 60 else 0).getbbox()
    return out.crop(box) if box else out


def main():
    spec = json.load(open(os.path.join(ROOT, "plan", "anime.json")))
    for d in ("full", "cut"):
        os.makedirs(os.path.join(D, d), exist_ok=True)
    for it in spec["images"]:
        name = it["name"]
        im, ph = load(name)
        im = im.resize((SIZE, round(SIZE * im.size[1] / im.size[0])), Image.LANCZOS)
        t = im if ph else tone(im)
        t.save(os.path.join(D, "full", f"{name}.jpg"), quality=92)
        if it["bg"] == "white":
            c = cutout(im, it.get("key", 60), it.get("holes", True)) if not ph else im.convert("RGBA")
            if not ph:
                rgb = tone(c.convert("RGB")).convert("RGBA")
                rgb.putalpha(c.split()[3])
                c = rgb
            c.save(os.path.join(D, "cut", f"{name}.png"), optimize=True)
        print(name, "placeholder" if ph else "ok")


if __name__ == "__main__":
    main()
