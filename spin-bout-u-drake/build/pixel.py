"""Pixel-art sprites for the "smoke a n**** top" scene (v13): a pixelated Drake made from the arm-out cut-out, a random
guy drawn by hand, a pistol, a muzzle flash and pixel "BANG!" text. Writes small PNGs to assets/img/collage/pixel/
(the page scales them up with image-rendering: pixelated). Drake's sprite comes from the owner's photo, so the folder
stays out of git like the other cut-outs.

python3 build/pixel.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "collage", "pixel")
TONES = [(20, 18, 19), (95, 27, 48), (176, 25, 79), (217, 196, 205), (242, 241, 236)]   # ink, maroon, magenta, pink-grey, white


def drake(width=72):
    im = Image.open(os.path.join(ROOT, "assets", "img", "collage", "sticker", "drake_boat_sunset.png")).convert("RGBA")
    h = round(im.height * width / im.width)
    sm = im.resize((width, h), Image.BOX)
    px = sm.load()
    for y in range(h):
        for x in range(width):
            r, g, b, a = px[x, y]
            if a < 110:
                px[x, y] = (0, 0, 0, 0)
                continue
            lum = (r * .3 + g * .59 + b * .11) / 255
            k = 0 if lum < .2 else 1 if lum < .34 else 3 if lum < .7 else 4
            px[x, y] = TONES[k] + (255,)
    return sm


GUY = [   # 24 x 40, facing left (toward Drake)
    "........kkkkkk..........",
    "......kkccccccck........",
    ".....kcccccccccck.......",
    "....kkkkkccccccck.......",
    "........khhhhhhhk.......",
    ".......ksssshhhhhk......",
    ".......kseksssshhk......",
    ".......kssssssssk.......",
    "......kssssssssk........",
    ".......kssskkssk........",
    "........kssssssk........",
    ".........kkssskk........",
    "........kggkssk.........",
    "......kkgggggggkk.......",
    ".....kggggggggggggk.....",
    "....kgggggdggggggggk....",
    "...kggggggdgggggggggk...",
    "...kggggggdggggggggggk..",
    "..kgggggggdgggggggggggk.",
    "..kggggk.kdggggggkgggk..",
    "..kgggk..kdgggggggkggk..",
    "..kgggk..kdggggggk.kggk.",
    "..ksssk..kdggggggk.ksssk",
    "..ksssk..kgggggggk.ksssk",
    "...kkk...kgggggggk..kkk.",
    ".........kgggggggk......",
    ".........kggggggggk.....",
    "........kjjjjjjjjjk.....",
    "........kjjjjjjjjjk.....",
    "........kjjjjkjjjjk.....",
    "........kjjjjkjjjjk.....",
    "........kjjjjkjjjjk.....",
    "........kjjjjkjjjjk.....",
    "........kjjjjkjjjjk.....",
    "........kjjjjkjjjjk.....",
    "........kjjjjkjjjjk.....",
    ".......kwwwwkkwwwwk.....",
    "......kwwwwwkwwwwwk.....",
    "......kkkkkkkkkkkkk.....",
    "........................",
]
GUN = [
    "..kkkkkkkkkkk",
    ".kaaaaaaaaaaak",
    ".kaaaaaaaaaak.",
    ".kaakkkkkkkk..",
    ".kaak.k.......",
    "kaaak.k.......",
    "kaak..........",
    "kkk...........",
]
FLASH = [
    "....y....",
    ".y..y..y.",
    "..yyoyy..",
    ".yyowoyy.",
    "yyowwwoyy",
    ".yyowoyy.",
    "..yyoyy..",
    ".y..y..y.",
    "....y....",
]
PAL = {"k": (20, 18, 19), "c": (176, 25, 79), "h": (30, 18, 16), "s": (141, 90, 59), "e": (242, 241, 236),
       "g": (122, 127, 138), "d": (90, 94, 103), "j": (47, 79, 143), "w": (242, 241, 236), "a": (60, 60, 66),
       "y": (255, 214, 64), "o": (255, 140, 40)}


def grid(rows):
    w, h = max(len(r) for r in rows), len(rows)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in PAL:
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def text(s):
    f = ImageFont.load_default()
    w = int(f.getlength(s)) + 4
    im = Image.new("RGBA", (w, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1)):
        d.text((2 + dx, 1 + dy), s, font=f, fill=(20, 18, 19, 255))
    d.text((2, 1), s, font=f, fill=(255, 214, 64, 255))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    drake().save(os.path.join(OUT, "drake_px.png"))
    grid(GUY).save(os.path.join(OUT, "guy_px.png"))
    grid(GUN).save(os.path.join(OUT, "gun_px.png"))
    grid(FLASH).save(os.path.join(OUT, "flash_px.png"))
    text("BANG!").save(os.path.join(OUT, "bang_px.png"))
    print("wrote", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
