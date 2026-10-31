"""From each <option>_print-bleed.png make: the trim-size PNG, a 600 dpi PDF, a cut guide and a preview mockup.
Also writes ../all-options-preview.png. Run after render.js."""
import glob
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PX = 600 / 25.4                       # px per mm at 600 dpi
BLEED = round(2 * PX)                 # 47
TRIM_W, TRIM_H = round(85.6 * PX), round(53.98 * PX)   # 2022 x 1275
RADIUS = 3.18                         # ID-1 corner radius, mm
CHIP = (8.6, 18.15, 21.6, 29.65)      # chip cut-out on the card face, mm from the card's top-left corner
SAFE = 3.0                            # keep text this far inside the cut line, mm


def mm(v):
    return round(v * PX)


def rounded_mask(size, r):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def chip(card):
    """Draw a gold EMV chip in the cut-out so the preview reads like the finished card."""
    d = ImageDraw.Draw(card)
    x0, y0, x1, y1 = (mm(v) for v in CHIP)
    d.rounded_rectangle((x0, y0, x1, y1), mm(1.8), fill=(28, 24, 34))          # the card showing through the cut
    g = Image.new('RGB', (x1 - x0 - mm(1.2), y1 - y0 - mm(1.2)))
    gd = ImageDraw.Draw(g)
    for i in range(g.height):                                                   # gold gradient
        t = i / g.height
        gd.line((0, i, g.width, i), fill=(int(226 - 40 * t), int(196 - 45 * t), int(120 - 40 * t)))
    w, h = g.size
    for fx in (0.33, 0.67):
        gd.line((int(w * fx), 0, int(w * fx), h), fill=(150, 118, 60), width=4)
    for fy in (0.25, 0.5, 0.75):
        gd.line((0, int(h * fy), int(w * 0.33), int(h * fy)), fill=(150, 118, 60), width=4)
        gd.line((int(w * 0.67), int(h * fy), w, int(h * fy)), fill=(150, 118, 60), width=4)
    gd.rounded_rectangle((int(w * .33), int(h * .3), int(w * .67), int(h * .7)), 10, outline=(150, 118, 60), width=4)
    card.paste(g, (x0 + mm(0.6), y0 + mm(0.6)), rounded_mask(g.size, mm(1.3)))


def guides(bleed_img):
    img = bleed_img.convert('RGB').copy()
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    W, H = img.size
    trim = (BLEED, BLEED, BLEED + TRIM_W, BLEED + TRIM_H)
    shade = Image.new('L', img.size, 120)
    ImageDraw.Draw(shade).rounded_rectangle(trim, mm(RADIUS), fill=0)
    ov.paste((255, 255, 255, 255), (0, 0), shade)                               # bleed area washed out
    d.rounded_rectangle(trim, mm(RADIUS), outline=(0, 200, 255, 255), width=5)  # cut line
    s = mm(SAFE)
    d.rectangle((trim[0] + s, trim[1] + s, trim[2] - s, trim[3] - s), outline=(255, 0, 170, 255), width=3)
    c = [BLEED + mm(v) for v in CHIP]
    d.rounded_rectangle(c, mm(1.8), outline=(255, 60, 60, 255), width=5)
    try:
        f = ImageFont.truetype('DejaVuSans-Bold.ttf', 34)
    except OSError:
        f = ImageFont.load_default()
    d.text((c[0], c[3] + 10), 'chip cut-out', fill=(255, 60, 60, 255), font=f)
    d.text((trim[0] + 12, H - BLEED + 4), 'cyan = cut line   magenta = safe zone (3 mm)   grey = 2 mm bleed', fill=(0, 140, 200, 255), font=f)
    img.paste(ov, (0, 0), ov)
    return img


def mockup(trim_img, width=1500, bg=((236, 233, 243), (214, 208, 226))):
    card = trim_img.convert('RGB').copy()
    chip(card)
    scale = width / card.width
    card = card.resize((width, round(card.height * scale)), Image.LANCZOS)
    mask = rounded_mask(card.size, round(mm(RADIUS) * scale))
    pad = 160
    W, H = card.width + pad * 2, card.height + pad * 2
    sheet = Image.new('RGB', (W, H))
    sd = ImageDraw.Draw(sheet)
    for y in range(H):
        t = y / H
        sd.line((0, y, W, y), fill=tuple(int(bg[0][i] + (bg[1][i] - bg[0][i]) * t) for i in range(3)))
    shadow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((pad + 10, pad + 40, pad + card.width - 10, pad + card.height + 30), 40, fill=150)
    shadow = shadow.filter(ImageFilter.GaussianBlur(38))
    sheet.paste((40, 20, 70), (0, 0), shadow)
    sheet.paste(card, (pad, pad), mask)
    return sheet


def main():
    previews = []
    for p in sorted(glob.glob(os.path.join(HERE, '..', '*', '*_print-bleed.png'))):
        folder, slug = os.path.dirname(p), os.path.basename(p).replace('_print-bleed.png', '')
        bleed = Image.open(p).convert('RGB')
        trim = bleed.crop((BLEED, BLEED, BLEED + TRIM_W, BLEED + TRIM_H))
        trim.save(os.path.join(folder, f'{slug}_card-size.png'), dpi=(600, 600))
        bleed.save(p, dpi=(600, 600))
        bleed.save(os.path.join(folder, f'{slug}_print.pdf'), 'PDF', resolution=600.0)
        guides(bleed).save(os.path.join(folder, f'{slug}_cut-guide.png'))
        m = mockup(trim)
        m.save(os.path.join(folder, f'{slug}_preview.png'))
        previews.append(m)
        print('finished', slug)
    w = max(m.width for m in previews) // 2
    small = [m.resize((w, round(m.height * w / m.width)), Image.LANCZOS) for m in previews]
    sheet = Image.new('RGB', (w, sum(s.height for s in small)), (225, 221, 233))
    y = 0
    for s in small:
        sheet.paste(s, (0, y)); y += s.height
    sheet.save(os.path.join(HERE, '..', 'all-options-preview.png'))


if __name__ == '__main__':
    main()
