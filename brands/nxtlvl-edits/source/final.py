"""The @nxtlvlledits logo kit, from the chosen concept Y: the N Disc.

A solid disc with the refined N and the star cut out of it. Writes the SVG masters into brands/nxtlvl-edits/ and the
PNGs into brands/nxtlvl-edits/png/, then renders kit-preview.png.  Run:  python3 final.py
"""
import os
import re
import subprocess

from build import INK, VIOLET, svg, write
from build4 import PEARL, centreline, contrast_outline, star4

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, '..'))
PNG = os.path.join(KIT, 'png')
TEXT = '#0B0816'
R = 300                                            # the disc's radius in its own units (600 x 600 box)

FILLS = {'pearl': None, 'ink': TEXT, 'white': '#FFFFFF', 'violet': VIOLET}


def disc(p, kind='pearl', heavy=False):
    """The disc (600 x 600 box) with the N and the star cut out, so whatever is behind shows through.

    heavy=True thickens the cut and the star for 64 px and below.
    """
    k = 2.42
    thick, star_k = (22, 15) if heavy else (17, 13)
    d = contrast_outline(centreline(tip=26), thick=thick, hair=thick, taper_out=46)
    ox, oy = R - 100 * k, R - 92 * k - 2                         # the star stays wholly inside the disc
    if kind == 'pearl':
        stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in PEARL)
        defs = (f'<linearGradient id="{p}pl" gradientUnits="userSpaceOnUse" x1="0" y1="{2 * R}" x2="{2 * R}" y2="0">'
                f'{stops}</linearGradient>')
        fill = f'url(#{p}pl)'
    else:
        defs, fill = '', FILLS[kind]
    defs += (f'<mask id="{p}cut" maskUnits="userSpaceOnUse" x="0" y="0" width="{2 * R}" height="{2 * R}">'
             f'<rect width="{2 * R}" height="{2 * R}" fill="#fff"/>'
             f'<path d="{d}" transform="translate({ox:.1f} {oy:.1f}) scale({k})" fill="#000"/>'
             + star4(ox + 160 * k, oy + 8 * k, star_k * k, '#000') + '</mask>')
    return defs, f'<circle cx="{R}" cy="{R}" r="{R}" fill="{fill}" mask="url(#{p}cut)"/>'


def placed(p, kind, cx, cy, diameter, heavy=False):
    defs, body = disc(p, kind, heavy)
    k = diameter / (2 * R)
    return defs, f'<g transform="translate({cx - diameter / 2:.2f} {cy - diameter / 2:.2f}) scale({k:.4f})">{body}</g>'


def ground(w, h, rx=0, p='g'):
    """Ink with the faintest lift in the middle (the profile ground)."""
    defs = (f'<radialGradient id="{p}" cx=".5" cy=".46" r=".7"><stop offset="0" stop-color="#110A24"/>'
            f'<stop offset="1" stop-color="{INK}"/></radialGradient>')
    return defs, f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#{p})"/>'


def profile(size=1080):
    gd, g = ground(size, size)
    md, m = placed('m', 'pearl', size / 2, size / 2, .58 * size)
    return svg(size, size, gd + md, g + m)


def mark(kind, size=512):
    """The disc alone on a transparent background."""
    md, m = placed('m', kind, size / 2, size / 2, size)
    return svg(size, size, md, m)


def icon(size=1024):
    gd, g = ground(size, size, rx=round(size * .2237))
    md, m = placed('m', 'pearl', size / 2, size / 2, .64 * size)
    return svg(size, size, gd + md, g + m)


def favicon(size=64):
    """The disc with the heavier cut on an Ink circle, for 64 px and below: the N stays dark on light and dark tabs."""
    md, m = placed('m', 'pearl', size / 2, size / 2, .88 * size, heavy=True)
    return svg(size, size, md, f'<circle cx="{size / 2}" cy="{size / 2}" r="{size / 2}" fill="{INK}"/>' + m)


def highlight(with_disc=True):
    """Story highlight cover, 1080 x 1920; Instagram shows the centre as a circle."""
    gd, g = ground(1080, 1920)
    if not with_disc:
        return svg(1080, 1920, gd, g + star4(540, 960, 120, '#FFFFFF'))
    md, m = placed('m', 'pearl', 540, 960, 440)
    return svg(1080, 1920, gd + md, g + m)


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
.tile {{ border-radius: 28px; display: flex; align-items: center; justify-content: center; padding: 36px; flex: 1; min-width: 0; }}
.tile img {{ max-width: 100%; height: auto; }}
.dark {{ background: #05030C; }} .light {{ background: #FFFFFF; }} .mist {{ background: #F5F2FF; }} .deep {{ background: #5E0FC4; }}
.circle {{ border-radius: 50%; display: block; }}
.ig {{ display: flex; flex-direction: column; justify-content: center; gap: 28px; background: #fff; border-radius: 28px;
  padding: 32px 36px; flex: 1; align-self: stretch; }}
.ig b {{ display: block; font-weight: 600; font-size: 26px; }} .ig span {{ display: block; font-size: 21px; color: #6E6787; margin-top: 4px; }}
img {{ display: block; }}
</style></head><body>
<p class="kicker">@nxtlvlledits · logo</p>
<h1>The N Disc</h1>
<p class="lede">A solid pearl disc with the N and the star cut out of it, like a coin or a seal. The cut lets whatever is behind
show through, so the same disc works on black, on light backgrounds and over footage.</p>
<h2>Instagram profile picture</h2>
<div class="row">
  <img class="circle" src="../png/profile-1080.png" style="width:380px;height:380px">
  <div class="ig">
    <div class="row"><img class="circle" src="../png/profile-1080.png" style="width:110px;height:110px">
      <div><b>nxtlvlledits</b><span>profile size</span></div></div>
    <div class="row"><img class="circle" src="../png/profile-1080.png" style="width:56px;height:56px">
      <img class="circle" src="../png/profile-1080.png" style="width:32px;height:32px">
      <span style="font-size:20px;color:#6E6787">feed and comment sizes</span></div>
  </div>
</div>
<h2>The disc on its own (transparent PNGs)</h2>
<div class="row">
  <div class="tile dark"><img src="../mark-pearl.svg" style="width:190px"></div>
  <div class="tile deep"><img src="../mark-white.svg" style="width:190px"></div>
  <div class="tile light"><img src="../mark.svg" style="width:190px"></div>
  <div class="tile mist"><img src="../mark-violet.svg" style="width:190px"></div>
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
        'mark-pearl.svg': mark('pearl'), 'mark-white.svg': mark('white'), 'mark.svg': mark('ink'),
        'mark-violet.svg': mark('violet'),
        'icon.svg': icon(), 'favicon.svg': favicon(),
        'highlight-cover.svg': highlight(), 'highlight-cover-star.svg': highlight(False),
    }
    for name, text in files.items():
        write(os.path.join(KIT, name), text)

    def size_of(name):
        m = re.search(r'width="(\d+)" height="(\d+)"', files[name])
        return int(m.group(1)), int(m.group(2))

    jobs = [('profile.svg', 'profile-1080.png', 1), ('profile.svg', 'profile-320.png', 320 / 1080),
            ('icon.svg', 'icon-1024.png', 1), ('icon.svg', 'icon-512.png', .5), ('icon.svg', 'icon-192.png', 192 / 1024),
            ('icon.svg', 'icon-180.png', 180 / 1024), ('favicon.svg', 'icon-64.png', 1), ('favicon.svg', 'icon-48.png', .75),
            ('favicon.svg', 'icon-32.png', .5),
            ('mark-pearl.svg', 'mark-pearl-1024.png', 2), ('mark-white.svg', 'mark-white-1024.png', 2),
            ('mark.svg', 'mark-1024.png', 2), ('mark-violet.svg', 'mark-violet-1024.png', 2),
            ('highlight-cover.svg', 'highlight-cover.png', 1), ('highlight-cover-star.svg', 'highlight-cover-star.png', 1)]
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
