"""python3 build/sheet.py <dir> [cols]  -> <dir>/sheet.png: the PNGs in a grid, each labelled with its time."""
import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 3
fs = sorted(f for f in glob.glob(os.path.join(d, "t*.png")))
ims = [Image.open(f).convert("RGB") for f in fs]
w, h = 360, 640
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
for k, (f, im) in enumerate(zip(fs, ims)):
    im = im.resize((w, h))
    dr = ImageDraw.Draw(im); dr.rectangle([0, 0, 90, 26], fill=(0, 0, 0)); dr.text((6, 6), os.path.basename(f)[1:-4], fill=(255, 255, 0))
    sheet.paste(im, ((k % cols) * w, (k // cols) * h))
sheet.save(os.path.join(d, "sheet.png"))
print(len(ims), "frames")
