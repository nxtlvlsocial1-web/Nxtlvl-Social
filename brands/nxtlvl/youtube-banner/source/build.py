"""YouTube channel banner for the AI creator page (@ai.nxtlvl), 2560 x 1440, in the Shooting Star logo's colours.

Everything that must be read sits in YouTube's all-device safe area (1235 x 338, centred); the wider desktop band
(2560 x 423) and the full TV frame carry only the logo's ground and starlight.
Run:  python3 youtube-banner/source/build.py   (from brands/nxtlvl; needs Playwright)
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
LI = os.path.abspath(os.path.join(HERE, '..', '..', 'linkedin-banner', 'source'))
sys.path.insert(0, LI)
from v2 import page, star, RENDER   # noqa: E402
from v3 import dust, CSS            # noqa: E402

W, H = 2560, 1440
SX, SY, SW, SH = (W - 1235) // 2, (H - 338) // 2, 1235, 338      # safe area: 662, 551
WHITE, LILAC, PALE = '#FFFFFF', '#B98AFF', '#D8BBFF'
STAR_SVG = os.path.join(LI, 'shooting-star.svg')


def ground():
    return ('<div class="abs" style="inset:0;background:linear-gradient(160deg, #0A0620 0%, #05030C 55%, #05030C 100%)"></div>'
            '<div class="abs" style="inset:0;background:radial-gradient(1500px 1000px at 18% 30%, rgba(126,26,246,.62), rgba(126,26,246,0))"></div>'
            '<div class="abs" style="inset:0;background:radial-gradient(1500px 1000px at 86% 72%, rgba(94,6,242,.58), rgba(94,6,242,0))"></div>')


def banner():
    mark = 290
    mx, my = SX + 30, SY + (SH - mark) // 2 + 4
    tx = mx + mark + 40
    body = (ground() + dust(W, H, 90, 11)
            + star(2140, 600, 22, PALE, ';opacity:.55') + star(420, 860, 16, PALE, ';opacity:.45') + star(2330, 900, 12, LILAC, ';opacity:.5')
            + f'<img class="abs" src="file://{STAR_SVG}" style="left:{mx}px;top:{my}px;width:{mark}px;height:{mark}px">'
            + f'<div class="sans abs" style="left:{tx}px;top:{SY + 18}px;font-size:84px;color:{WHITE};word-spacing:.14em">Discover the</div>'
            + f'<div class="ser abs grad" style="left:{tx - 4}px;top:{SY + 104}px;font-size:122px">world of AI.</div>'
            + f'<div class="cap abs" style="left:{tx}px;top:{SY + 246}px;font-size:30px;color:{PALE}">AI tools<b style="color:{LILAC};margin:0 18px">·</b>Automation'
              f'<b style="color:{LILAC};margin:0 18px">·</b>Innovation</div>'
            + f'<div class="abs" style="left:{tx}px;top:{SY + 292}px;font-size:30px;font-weight:600;color:{WHITE};opacity:.9;white-space:nowrap">'
              f'@ai.nxtlvl<span style="color:{LILAC};margin:0 14px">/</span><span style="color:{PALE};font-weight:400">New videos every week</span></div>')
    return page(W, H, CSS, body)


html = os.path.join(HERE, 'banner.html')
open(html, 'w').write(banner())
png = os.path.join(OUT, 'youtube-banner-2560x1440.png')
subprocess.run(['node', RENDER, html, png, str(W), str(H), '1'], check=True)
# YouTube's limit is 6 MB; a JPEG copy keeps it small for slow uploads
subprocess.run(['python3', '-c', f'from PIL import Image; Image.open("{png}").convert("RGB").save("{png[:-4]}.jpg", quality=92)'], check=True)
print('wrote', png)
