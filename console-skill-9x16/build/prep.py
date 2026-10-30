"""Image prep: everything the composition loads from assets/img/.

python3 build/prep.py      (from the project root; needs Pillow and numpy)

- <name>-bg.jpg: a blurred, darkened 1080x1920 cover of each scene image, the ground the sharp art sits on when the
  art doesn't fill the portrait frame (the reference's object-on-dark-ground look).
- grain-<n>.png: 4 pixel-grain frames (2 px grain), cycled on twos as the film texture; vignette.png.
- cover-gow2-<n>.png: the God of War II cover at 4 pixelation steps for the "sharper graphics" beat.
- apple-white.png, deck-logo.png: the supplied logos keyed for dark screens; clap.png; wordmark.png.
"""
import os

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "src")
OUT = os.path.join(ROOT, "assets", "img")
SCENES = ["boy-at-pc", "bg-ps2-desk", "pc-monitor-desk", "disc-bell-jar", "disc-case", "laptop-desk", "bg-spotlight-room",
          "bg-desk-wide", "phone-desk", "hands-controller", "bg-crt-tv", "hand-magnifier", "handheld-hands", "hourglass",
          "boy-trophy", "calendar-pages"]


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def main():
    os.makedirs(OUT, exist_ok=True)
    for n in SCENES:
        im = Image.open(os.path.join(SRC, n + ".png")).convert("RGB")
        im.save(os.path.join(OUT, n + ".jpg"), quality=93, subsampling=0)
        bg = cover(im.resize((im.width // 8, im.height // 8), Image.BILINEAR), 270, 480).filter(ImageFilter.GaussianBlur(9))
        bg = ImageEnhance.Brightness(bg).enhance(.42).resize((1080, 1920), Image.BICUBIC)
        bg.save(os.path.join(OUT, n + "-bg.jpg"), quality=88)
    # pixel grain: 540x960 noise, shown at 2x with pixelated rendering
    rng = np.random.default_rng(7)
    for i in range(4):
        g = rng.normal(128, 38, (960, 540)).clip(0, 255).astype(np.uint8)
        a = np.full((960, 540), 46, np.uint8)
        Image.fromarray(np.dstack([g, g, g, a]), "RGBA").save(os.path.join(OUT, f"grain-{i}.png"))
    yy, xx = np.mgrid[0:960, 0:540]
    d = np.sqrt(((xx - 270) / 270) ** 2 + ((yy - 470) / 520) ** 2)
    a = (np.clip((d - .55) / .7, 0, 1) ** 1.6 * 235).astype(np.uint8)
    z = np.zeros_like(a)
    Image.fromarray(np.dstack([z, z, z, a]), "RGBA").resize((1080, 1920), Image.BICUBIC).save(os.path.join(OUT, "vignette.png"))
    # cover pixelation steps (smallest first), the last is the source itself
    c = Image.open(os.path.join(SRC, "cover-god-of-war-2.webp")).convert("RGB")
    for i, w in enumerate([10, 20, 40]):
        c.resize((w, round(w * c.height / c.width)), Image.BOX).save(os.path.join(OUT, f"cover-gow2-{i}.png"))
    c.save(os.path.join(OUT, "cover-gow2-3.png"))
    for n in ["god-hand", "gta-vcs", "resident-evil-4", "god-of-war-2"]:
        Image.open(os.path.join(SRC, f"cover-{n}.webp")).convert("RGB").save(os.path.join(OUT, f"cover-{n}.png"))
    # logos keyed for dark screens
    ap = np.asarray(Image.open(os.path.join(SRC, "logo-apple.png")).convert("L"), np.float32)
    alpha = (255 - ap).clip(0, 255).astype(np.uint8)
    w = np.full_like(alpha, 245)
    Image.fromarray(np.dstack([w, w, w, alpha]), "RGBA").save(os.path.join(OUT, "apple-white.png"))
    dk = np.asarray(Image.open(os.path.join(SRC, "logo-unknown-circle.png")).convert("RGB"), np.float32)
    white = (dk.min(axis=2) > 225)
    rgb = dk.copy()
    dark = dk.max(axis=2) < 60
    rgb[dark] = [240, 240, 240]          # the black arc reads white on a dark screen
    al = np.where(white, 0, 255).astype(np.uint8)
    Image.fromarray(np.dstack([rgb.astype(np.uint8), al]), "RGBA").save(os.path.join(OUT, "deck-logo.png"))
    Image.open(os.path.join(SRC, "hand-clap.png")).save(os.path.join(OUT, "clap.png"))
    Image.open(os.path.join(ROOT, "..", "brands", "ai-nxtlvl", "logo-wordmark.png")).save(os.path.join(OUT, "wordmark.png"))
    print("wrote", len(os.listdir(OUT)), "files to assets/img")


if __name__ == "__main__":
    main()
