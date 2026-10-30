"""The nxtlvl edits logo kit, from the chosen concept R1 (Pearl): the refined Monoline N.

Writes the kit into brands/nxtlvl-edits/ (SVG masters) and brands/nxtlvl-edits/png/, then renders the PNGs and
kit-preview.png.  Run:  python3 final.py
"""
import os
import subprocess

from build import INK, LIFT, MIST, PALE, VIOLET, WM_H, WM_W, WM_XH, edits, edits_box, svg, wordmark, write
from build4 import BOX, MONO, refined_n

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..'))
PNG = os.path.join(KIT, 'png')
TEXT = '#0B0816'                                   # Ink text, as in the main kit
HEAVY = dict(thick=15, hair=15, taper_out=46)      # small sizes (favicon, 32-64 px): a heavier line and star
LOCKUP = dict(thick=11.5, hair=11.5, taper_out=50) # next to the bold wordmark the line needs a little more weight

# body of the N in mark units: arch top at y 40, baseline 170 (BOX starts at y -14)
N_TOP, N_BASE = 40 - BOX[1], 170 - BOX[1]

LOOKS = {
    # name: (line, star, wordmark, edits, star over the i)
    'pearl': ('pearl', '#FFFFFF', MIST, MIST, PALE),           # on dark: the profile look
    'colour': (TEXT, VIOLET, TEXT, TEXT, VIOLET),              # on light
    'white': ('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF'),
    'black': (TEXT, TEXT, TEXT, TEXT, TEXT),
}


def ground(size, rx=0, p='g'):
    """Ink with the faintest lift in the middle (the profile ground)."""
    defs = (f'<radialGradient id="{p}" cx=".5" cy=".46" r=".7"><stop offset="0" stop-color="#110A24"/>'
            f'<stop offset="1" stop-color="{INK}"/></radialGradient>')
    w, h = size
    return defs, f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#{p})"/>'


def mark_at(look, x, y, n_height, p='m', pen=MONO, star_r=13.5):
    """The mark placed so the body of the N (arch top to baseline) is n_height tall, its box top-left at (x, y)."""
    line, star_fill = LOOKS[look][:2]
    defs, body, w, h = refined_n(p, line, star_fill, pen, star_r)
    k = n_height / (N_BASE - N_TOP)
    return defs, f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f})">{body}</g>', w * k, h * k


def centred(look, size, frac, p='m', pen=MONO, star_r=13.5, dy=0):
    """Mark centred in a size x size square, its full height frac of the square."""
    _, _, w, h = refined_n(p, 'pearl', '#fff', pen, star_r)
    n_height = frac * size * (N_BASE - N_TOP) / h
    k = n_height / (N_BASE - N_TOP)
    return mark_at(look, size / 2 - w * k / 2, size / 2 - h * k / 2 + dy, n_height, p, pen, star_r)


def words(look, x, y, height):
    """'nxtlvl edits' on one line, wordmark top-left at (x, y). Returns (svg, width)."""
    _, _, wf, ef, sf = LOOKS[look]
    wm_w = WM_W * height / WM_H
    xh = height * (WM_H - WM_XH) / WM_H
    size = xh / 0.516 * 0.94
    ex0, _, ex1, _ = edits_box(size)
    gap = 0.40 * height
    ex = x + wm_w + gap - ex0
    return wordmark(x, y, height, wf) + edits(ex, y + height, size, ef, sf), wm_w + gap + (ex1 - ex0)


def logo(look, height=118, margin=24):
    """Horizontal: the mark on the wordmark's baseline, the N as tall as the lettering, the star rising above it."""
    defs, m, mw, mh = mark_at(look, margin, margin, height, pen=LOCKUP, star_r=15)
    star_rise = mh - height                       # the star and tip stand above the wordmark
    text, tw = words(look, margin + mw + 0.55 * height, margin + star_rise, height)
    w, h = margin * 2 + mw + 0.55 * height + tw, margin * 2 + mh
    return svg(round(w), round(h), defs, m + text)


def logo_stacked(look, height=118, margin=24):
    """Stacked: the mark above, centred over 'nxtlvl edits'."""
    _, tw = words(look, 0, 0, height)
    n_h = 2.3 * height
    _, _, mw, mh = mark_at(look, 0, 0, n_h)
    w = margin * 2 + max(tw, mw)
    defs, m, _, _ = mark_at(look, w / 2 - mw / 2 + 0.06 * mw, margin, n_h)
    text, _ = words(look, w / 2 - tw / 2, margin + mh + 0.5 * height, height)
    return svg(round(w), round(margin * 2 + mh + 0.5 * height + height * 1.02), defs, m + text)


def mark_file(look, size=512):
    defs, m, _, _ = centred(look, size, .86)
    return svg(size, size, defs, m)


def profile(size=1080):
    gdefs, g = ground((size, size))
    mdefs, m, _, _ = centred('pearl', size, .52, dy=4 * size / 1080)
    return svg(size, size, gdefs + mdefs, g + m)


def icon(size=1024, heavy=False):
    """Rounded square for app icons and favicons; heavy=True for 64 px and below."""
    gdefs, g = ground((size, size), rx=round(size * 0.2237))
    mdefs, m, _, _ = centred('pearl', size, .62 if heavy else .56, pen=HEAVY if heavy else MONO, star_r=19 if heavy else 13.5)
    return svg(size, size, gdefs + mdefs, g + m)


def highlight(with_mark=True):
    """Story highlight cover, 1080 x 1920; Instagram shows the centre as a circle."""
    gdefs, g = ground((1080, 1920))
    if not with_mark:
        from build4 import star4
        return svg(1080, 1920, gdefs, g + star4(540, 960, 120, '#FFFFFF'))
    mdefs, m, _, _ = centred('pearl', 1080, .46, dy=420 + 4)
    return svg(1080, 1920, gdefs + mdefs, g + m)


def kit_page():
    """The whole kit on one page (rendered to ../kit-preview.png)."""
    fonts = '../../../website/fonts'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Instrument Sans"; src: url("{fonts}/instrument-sans-400.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Instrument Sans"; src: url("{fonts}/instrument-sans-600.woff2") format("woff2"); font-weight: 600; }}
@font-face {{ font-family: "Serif Italic"; src: url("fonts/instrument-serif-italic-400.woff2") format("woff2"); }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; background: #EEEAF6; font-family: "Instrument Sans", sans-serif; color: #0B0816; padding: 72px 60px 64px; }}
.kicker {{ font-weight: 600; font-size: 20px; letter-spacing: .18em; text-transform: uppercase; color: #7D18FC; }}
h1 {{ font-family: "Serif Italic", serif; font-weight: 400; font-size: 76px; line-height: 1.02; margin: 14px 0 16px; }}
.lede {{ font-size: 24px; line-height: 1.45; color: #4A4360; margin-bottom: 40px; }}
h2 {{ font-weight: 600; font-size: 20px; letter-spacing: .14em; text-transform: uppercase; color: #6E6787; margin: 40px 0 16px; }}
.row {{ display: flex; gap: 24px; align-items: center; }}
.tile {{ border-radius: 28px; display: flex; align-items: center; justify-content: center; padding: 44px; }}
.dark {{ background: #05030C; }} .light {{ background: #FFFFFF; }} .violet {{ background: #7D18FC; }} .deep {{ background: #5E0FC4; }}
.circle {{ border-radius: 50%; display: block; }}
.ig {{ display: flex; align-items: center; gap: 20px; background: #fff; border-radius: 28px; padding: 32px 36px; flex: 1; align-self: stretch; }}
.ig b {{ display: block; font-weight: 600; font-size: 26px; }} .ig span {{ display: block; font-size: 21px; color: #6E6787; margin-top: 4px; }}
img {{ display: block; }}
.tile {{ min-width: 0; }} .tile img {{ max-width: 100%; height: auto; }}
</style></head><body>
<p class="kicker">nxtlvl edits · logo kit</p>
<h1>The Monoline N, Pearl</h1>
<p class="lede">One fine line, the right stem climbing past the left and ending in the star. Pearl on rich black for the profile,
Ink and violet on light backgrounds, single colour where only one will do.</p>
<h2>Instagram profile picture</h2>
<div class="row">
  <img class="circle" src="../png/profile-1080.png" style="width:380px;height:380px">
  <div class="ig" style="flex-direction:column;align-items:flex-start;justify-content:center;gap:28px">
    <div class="row"><img class="circle" src="../png/profile-1080.png" style="width:110px;height:110px">
      <div><b>nxtlvlledits</b><span>nxtlvl edits</span></div></div>
    <div class="row"><img class="circle" src="../png/profile-1080.png" style="width:56px;height:56px">
      <img class="circle" src="../png/profile-1080.png" style="width:32px;height:32px">
      <span style="font-size:20px;color:#6E6787">feed and comment sizes</span></div>
  </div>
</div>
<h2>Logo</h2>
<div class="tile dark"><img src="../logo-pearl.svg" style="width:760px"></div>
<div class="row" style="margin-top:24px">
  <div class="tile light" style="flex:1"><img src="../logo.svg" style="width:480px"></div>
  <div class="tile light" style="flex:1"><img src="../logo-mono-black.svg" style="width:480px"></div>
</div>
<div class="row" style="margin-top:24px">
  <div class="tile violet" style="flex:1"><img src="../logo-mono-white.svg" style="width:480px"></div>
  <div class="tile dark" style="flex:1"><img src="../logo-pearl-stacked.svg" style="width:300px"></div>
</div>
<h2>Mark</h2>
<div class="row">
  <div class="tile light" style="flex:1;padding:28px"><img src="../mark.svg" style="width:200px"></div>
  <div class="tile dark" style="flex:1;padding:28px"><img src="../mark-pearl.svg" style="width:200px"></div>
  <div class="tile deep" style="flex:1;padding:28px"><img src="../mark-white.svg" style="width:200px"></div>
  <div class="tile light" style="flex:1;padding:28px"><img src="../mark-black.svg" style="width:200px"></div>
</div>
<h2>App icon, favicon and story highlight covers</h2>
<div class="row" style="align-items:flex-end">
  <img src="../png/icon-1024.png" style="width:220px"><img src="../png/icon-180.png" style="width:120px">
  <img src="../png/icon-64.png" style="width:64px"><img src="../png/icon-32.png" style="width:32px">
  <div style="flex:1"></div>
  <img src="../png/highlight-cover.png" style="width:200px;border-radius:20px">
  <img src="../png/highlight-cover-star.png" style="width:200px;border-radius:20px">
</div>
</body></html>'''


def main():
    files = {
        'profile.svg': profile(),
        'mark.svg': mark_file('colour'), 'mark-pearl.svg': mark_file('pearl'),
        'mark-white.svg': mark_file('white'), 'mark-black.svg': mark_file('black'),
        'logo.svg': logo('colour'), 'logo-pearl.svg': logo('pearl'),
        'logo-stacked.svg': logo_stacked('colour'), 'logo-pearl-stacked.svg': logo_stacked('pearl'),
        'logo-mono-black.svg': logo('black'), 'logo-mono-white.svg': logo('white'),
        'icon.svg': icon(), 'favicon.svg': icon(64, heavy=True),
        'highlight-cover.svg': highlight(), 'highlight-cover-star.svg': highlight(False),
    }
    for name, text in files.items():
        write(os.path.join(KIT, name), text)

    def size_of(name):
        import re
        m = re.search(r'width="(\d+)" height="(\d+)"', files[name])
        return int(m.group(1)), int(m.group(2))

    jobs = [('profile.svg', 'profile-1080.png', 1), ('profile.svg', 'profile-320.png', 320 / 1080),
            ('icon.svg', 'icon-1024.png', 1), ('icon.svg', 'icon-512.png', .5), ('icon.svg', 'icon-192.png', 192 / 1024),
            ('icon.svg', 'icon-180.png', 180 / 1024), ('favicon.svg', 'icon-64.png', 1), ('favicon.svg', 'icon-48.png', .75),
            ('favicon.svg', 'icon-32.png', .5),
            ('mark.svg', 'mark-1024.png', 2), ('mark-pearl.svg', 'mark-pearl-1024.png', 2),
            ('mark-white.svg', 'mark-white-1024.png', 2), ('mark-black.svg', 'mark-black-1024.png', 2),
            ('highlight-cover.svg', 'highlight-cover.png', 1), ('highlight-cover-star.svg', 'highlight-cover-star.png', 1)]
    jobs += [(n, n.replace('.svg', '@4x.png'), 4) for n in files if n.startswith('logo')]
    os.makedirs(PNG, exist_ok=True)
    args = []
    for src, out, scale in jobs:
        w, h = size_of(src)
        args += [os.path.join(KIT, src), os.path.join(PNG, out), str(w), str(h), str(scale)]
    subprocess.run(['node', os.path.join(HERE, 'render.js')] + args, check=True, stdout=subprocess.DEVNULL)
    html = os.path.join(HERE, 'kit.html')
    write(html, kit_page())
    from sheet import render_sheet
    render_sheet(html, os.path.join(KIT, 'kit-preview.png'))
    print('kit ->', KIT)


if __name__ == '__main__':
    main()
