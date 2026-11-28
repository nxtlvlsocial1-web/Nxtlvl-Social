"""Vox-style paper kit from the archive images: stickers (white border), torn-edge photos, halftone, paper, grain, tear pieces."""
import pathlib, random
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageEnhance, ImageChops
P = pathlib.Path(__file__).resolve().parent.parent
R, O = P / "assets/raw", P / "assets/img"
rng = random.Random(7)

def tone(im, warm=(36, 28, 22), light=(242, 232, 212), contrast=1.25):
    g = ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(contrast)
    return ImageOps.colorize(g, warm, light)

def sticker(src, dst, border=16, size=1100, colour=False):
    im = Image.open(R / src).convert("RGBA"); im.thumbnail((size, size))
    a = im.split()[3].point(lambda v: 255 if v > 110 else 0)
    rgb = im.convert("RGB") if colour else tone(im.convert("RGB"))
    pad = border * 3
    W, H = im.width + 2 * pad, im.height + 2 * pad
    alpha = Image.new("L", (W, H), 0); alpha.paste(a, (pad, pad))
    outline = alpha.filter(ImageFilter.MaxFilter(border * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 90 else 0)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste((250, 247, 240, 255), (0, 0), outline)
    body = Image.new("RGBA", (W, H), (0, 0, 0, 0)); body.paste(rgb, (pad, pad)); body.putalpha(alpha)
    out = Image.alpha_composite(out, body)
    out.save(O / dst, optimize=True); print(dst, out.size)

def torn_mask(w, h, amp=14, step=18, seed=1):
    r = random.Random(seed)
    pts = []
    for x in range(0, w + step, step): pts.append((min(x, w), r.uniform(0, amp)))
    for y in range(0, h + step, step): pts.append((w - r.uniform(0, amp), min(y, h)))
    for x in range(w, -step, -step): pts.append((max(x, 0), h - r.uniform(0, amp)))
    for y in range(h, -step, -step): pts.append((r.uniform(0, amp), max(y, 0)))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon(pts, fill=255)
    return m

def torn(src, dst, size=1100, crop=None, colour=False, border=18, seed=1, halftone=False, contrast=1.25):
    im = Image.open(R / src).convert("RGB")
    if crop:
        W0, H0 = im.size; im = im.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    im.thumbnail((size, size))
    if halftone:
        im = halftone_img(im)
    elif not colour:
        im = tone(im, contrast=contrast)
    else:
        im = ImageEnhance.Color(im).enhance(0.8)
    W, H = im.width + 2 * border, im.height + 2 * border
    base = Image.new("RGB", (W, H), (250, 247, 240)); base.paste(im, (border, border))
    out = base.convert("RGBA"); out.putalpha(torn_mask(W, H, seed=seed))
    out.save(O / dst, optimize=True); print(dst, out.size)

def halftone_img(im, cell=9, ink=(30, 24, 20), paper=(240, 228, 206)):
    g = ImageOps.grayscale(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.9)).enhance(1.15))
    w, h = g.size
    out = Image.new("RGB", (w, h), paper); d = ImageDraw.Draw(out)
    a = np.asarray(g, np.float32) / 255
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            v = 1 - a[y:y + cell, x:x + cell].mean()
            r = cell * 0.72 * v ** 0.8
            if r > 0.4:
                cx, cy = x + cell / 2 + (cell / 2 if (y // cell) % 2 else 0), y + cell / 2
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ink)
    return out

sticker("tv_cut.png", "tv.png", size=1000)
torn("newsboy.jpg", "newsboy.png", size=900, crop=(0.05, 0.02, 0.95, 0.80), seed=8)
torn("P01_NYTimes_Page1_11_11_1918.jpg", "news.png", size=1150, seed=2, contrast=1.1)
torn("P01_NYTimes_Page1_11_11_1918.jpg", "headline.png", size=1400, crop=(0.02, 0.093, 0.98, 0.168), seed=3, contrast=1.15)
torn("P02_Cabiria_1914_poster_restored.jpg", "poster.png", size=1000, colour=True, seed=4)
torn("P03_EgyptianTheater_ext_1926.jpg", "crowd.png", size=1000, crop=(0.0, 0.08, 1.0, 0.92), seed=5, contrast=1.15)
torn("P05_1939_RCA_Television_Advertisement.jpg", "rcaad.png", size=800, seed=6, contrast=1.1)
# film frames: sepia crops of the poster
po = Image.open(R / "P02_Cabiria_1914_poster_restored.jpg").convert("RGB")
for i, (l, t) in enumerate(((0.10, 0.30), (0.25, 0.50), (0.05, 0.72))):
    W0, H0 = po.size; cw = W0 * 0.6; ch = cw * 0.72
    fr = po.crop((int(l * W0), int(t * H0), int(l * W0 + cw), int(t * H0 + ch))).resize((620, 446))
    tone(fr, warm=(40, 26, 14), light=(236, 214, 170)).save(O / f"frame{i}.jpg", quality=88)
# paper texture (multiply overlay) and three grain frames
nr = np.random.default_rng(3)
n = nr.normal(0, 1, (960, 540)).astype(np.float32)
fib = np.asarray(Image.fromarray(((n * 0.5 + 0.5).clip(0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)).resize((1080, 1920)), np.float32)
tex = (236 + (fib - 128) * 0.18).clip(200, 255).astype(np.uint8)
Image.fromarray(tex).convert("RGB").save(O / "paper.jpg", quality=85)
for k in range(3):
    g = (128 + nr.normal(0, 40, (960, 540))).clip(0, 255).astype(np.uint8)
    a = np.full_like(g, 34)
    Image.fromarray(np.dstack([g, g, g, a])).save(O / f"grain{k}.png")
# torn paper wipe pieces (top and bottom halves, jagged diagonal edge)
for name, top in (("tearA", True), ("tearB", False)):
    W, H = 1500, 2000
    m = Image.new("L", (W, H), 0); r = random.Random(11)
    edge = [(x, 1000 + r.uniform(-34, 34) + (x - W / 2) * 0.12) for x in range(0, W + 30, 30)]
    poly = ([(0, 0), (W, 0)] + edge[::-1]) if top else ([(0, H), (W, H)] + edge[::-1])
    ImageDraw.Draw(m).polygon(poly if top else [(0, H)] + edge + [(W, H)], fill=255)
    paper = Image.new("RGB", (W, H), (239, 230, 212))
    pt = Image.open(O / "paper.jpg").resize((W, H)); paper = ImageChops.multiply(paper, pt)
    lip = m.filter(ImageFilter.MaxFilter(9)); edge_img = Image.new("RGBA", (W, H), (255, 252, 244, 0)); edge_img.putalpha(ImageChops.subtract(lip, m))
    out = paper.convert("RGBA"); out.putalpha(m); out = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), out)
    out = Image.alpha_composite(out, edge_img)
    out.save(O / f"{name}.png", optimize=True)
print("kit done")
