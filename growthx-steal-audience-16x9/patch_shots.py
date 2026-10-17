# Rebrands the supplied Ads Manager screenshots for GrowthX:
# swaps the account logo for the GX mark and the account name/handle for GrowthX's.
# Run: python3 patch_shots.py <dir with 2.png 3.png 4.png 5.png>
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shots")
MARK = Image.open(os.path.join(HERE, "brand", "logo-mark.png")).convert("RGB")
F = "/usr/share/fonts/opentype/inter/"


def logo(im, box, dim=1.0):
    x0, y0, x1, y1 = box
    m = MARK.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    if dim != 1.0:
        m = ImageEnhance.Brightness(m).enhance(dim)
    mask = Image.new("L", m.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, m.size[0] - 1, m.size[1] - 1], radius=5, fill=255)
    im.paste(m, (x0, y0), mask)


def text(im, box, bg, s, size, color, weight="Regular"):
    d = ImageDraw.Draw(im)
    d.rectangle(box, fill=bg)
    font = ImageFont.truetype(F + f"Inter-{weight}.otf", size)
    x0, y0, x1, y1 = box
    th = font.getbbox("Hg")[3]
    d.text((x0 + 2, y0 + (y1 - y0 - th) // 2 - 1), s, font=font, fill=color)


for name in ["2.png", "3.png"]:
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    logo(im, (221, 14, 249, 41))
    text(im, (303, 12, 510, 42), (255, 255, 255), "The GrowthX Studio", 17, (28, 30, 33))
    im.save(os.path.join(OUT, name))

im = Image.open(os.path.join(SRC, "4.png")).convert("RGB")
logo(im, (213, 3, 240, 29), dim=0.4)
text(im, (293, 3, 495, 28), (102, 102, 102), "The GrowthX Studio", 17, (12, 12, 13))
im.save(os.path.join(OUT, "4.png"))

im = Image.open(os.path.join(SRC, "5.png")).convert("RGB")
text(im, (1309, 490, 1418, 511), (98, 98, 99), "thegrowthxstudio", 14, (10, 10, 10))
im.save(os.path.join(OUT, "5.png"))
print("patched ->", OUT)
