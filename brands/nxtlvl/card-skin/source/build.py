"""Build the debit-card skin designs for Rishabh Rana (CMO, Nxtlvl Social).

Writes one HTML page per option into ./html/, then render.js turns them into print files.
Units: 10 CSS px = 1 mm. The canvas is the card plus 2 mm bleed on every side:
  card (ISO/IEC 7810 ID-1) 85.60 x 53.98 mm  ->  canvas 89.6 x 58.0 mm = 896 x 580 px
Run:  python3 build.py && node render.js
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'website', 'fonts'))
NAME, TITLE, ROLE = 'Rishabh Rana', 'Chief Marketing Officer', 'CMO'

W, H, BLEED = 896, 580, 20            # canvas px, bleed px (2 mm)
SAFE = BLEED + 30                       # 3 mm inside the cut line

STAR_DEFS = open(os.path.join(HERE, 'star-defs.svgfrag')).read()
STAR_PATHS = open(os.path.join(HERE, 'star-paths.svgfrag')).read()


def star(x, y, scale, opacity=1.0, extra=''):
    """The Shooting Star mark with its star head at (x, y); scale 1 = mark units (trail ~166 long)."""
    return (f'<g transform="translate({x} {y}) scale({scale}) translate(-140 -60)" opacity="{opacity}" {extra}>'
            f'{STAR_PATHS}</g>')


HEAD = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Archivo;src:url('file://{FONTS}/archivo-variable.woff2') format('woff2');font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:'Instrument Sans';src:url('file://{FONTS}/instrument-sans-400.woff2') format('woff2');font-weight:400}}
@font-face{{font-family:'Instrument Sans';src:url('file://{FONTS}/instrument-sans-500.woff2') format('woff2');font-weight:500}}
@font-face{{font-family:'Instrument Sans';src:url('file://{FONTS}/instrument-sans-600.woff2') format('woff2');font-weight:600}}
@font-face{{font-family:'Instrument Serif';src:url('file://{FONTS}/instrument-serif-400.woff2') format('woff2');font-weight:400}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.c{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.c>svg,.layer{{position:absolute;inset:0;width:{W}px;height:{H}px}}
.t{{position:absolute;white-space:nowrap;-webkit-font-smoothing:antialiased}}
.word{{font-family:Archivo;font-weight:700;font-stretch:108%;letter-spacing:-.03em}}
.word i{{font-family:'Instrument Sans';font-style:normal;font-weight:400;letter-spacing:0;margin-left:.18em}}
</style></head><body><div class="c">"""
TAIL = '</div></body></html>'
SVG_OPEN = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs>{STAR_DEFS}'


def option_a():
    """Shooting star: ink black, violet corner light, a big star streaking up to the top-right."""
    svg = (SVG_OPEN + """
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0620"/><stop offset=".6" stop-color="#05030C"/></linearGradient>
      <radialGradient id="gTR" cx="1" cy="0" r=".75"><stop offset="0" stop-color="#7E1AF6" stop-opacity=".75"/><stop offset="1" stop-color="#7E1AF6" stop-opacity="0"/></radialGradient>
      <radialGradient id="gBL" cx="0" cy="1" r=".7"><stop offset="0" stop-color="#5E06F2" stop-opacity=".55"/><stop offset="1" stop-color="#5E06F2" stop-opacity="0"/></radialGradient>
      <radialGradient id="halo" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(765 128) scale(135)">
        <stop offset="0" stop-color="#D8BBFF" stop-opacity=".55"/><stop offset=".4" stop-color="#A95CFF" stop-opacity=".2"/><stop offset="1" stop-color="#7D18FC" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="896" height="580" fill="url(#bg)"/><rect width="896" height="580" fill="url(#gTR)"/><rect width="896" height="580" fill="url(#gBL)"/>
      <circle cx="765" cy="128" r="135" fill="url(#halo)"/>""" + star(765, 128, 3.35) + '</svg>')
    text = f"""
      <div class="t word" style="left:{SAFE}px;top:{SAFE}px;font-size:31px;color:#F5F2FF">nxtlvl<i>social</i></div>
      <div class="t" style="left:{SAFE}px;top:438px;font-family:Archivo;font-weight:600;font-stretch:112%;font-size:35px;letter-spacing:.07em;color:#F5F2FF">{NAME.upper()}</div>
      <div class="t" style="left:{SAFE}px;top:486px;font-family:'Instrument Sans';font-weight:500;font-size:19px;letter-spacing:.02em;color:#D8BBFF">{TITLE}</div>
      <div class="t" style="right:{SAFE + 10}px;top:478px;font-family:'Instrument Serif';font-style:italic;font-size:46px;color:#F5F2FF;opacity:.92">{ROLE}</div>"""
    return svg + text


def option_b():
    """Violet foil: the brand gradient with a soft holographic sheen and a large watermark star."""
    svg = (SVG_OPEN + """
      <linearGradient id="bg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#4A0AA0"/><stop offset=".45" stop-color="#7D18FC"/><stop offset="1" stop-color="#B57CFF"/></linearGradient>
      <linearGradient id="sheen" x1="0" y1="0" x2="1" y2=".6">
        <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".38" stop-color="#FFFFFF" stop-opacity="0"/>
        <stop offset=".5" stop-color="#F5F2FF" stop-opacity=".28"/><stop offset=".56" stop-color="#9FE7FF" stop-opacity=".12"/>
        <stop offset=".64" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
      <radialGradient id="dark" cx=".05" cy="1" r=".8"><stop offset="0" stop-color="#1A0640" stop-opacity=".7"/><stop offset="1" stop-color="#1A0640" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="896" height="580" fill="url(#bg)"/><rect width="896" height="580" fill="url(#dark)"/>
      <rect width="896" height="580" fill="url(#sheen)"/>""" + star(760, 120, 5.6, .16) + '</svg>')
    text = f"""
      <div class="t word" style="left:{SAFE}px;top:{SAFE}px;font-size:31px;color:#FFFFFF">nxtlvl<i>social</i></div>
      <div class="t" style="left:{SAFE}px;top:438px;font-family:Archivo;font-weight:600;font-stretch:112%;font-size:35px;letter-spacing:.07em;color:#FFFFFF">{NAME.upper()}</div>
      <div class="t" style="left:{SAFE}px;top:486px;font-family:'Instrument Sans';font-weight:500;font-size:19px;letter-spacing:.02em;color:#EBDCFF">{TITLE}</div>
      <div class="t" style="right:{SAFE + 10}px;top:478px;font-family:'Instrument Serif';font-style:italic;font-size:46px;color:#FFFFFF">{ROLE}</div>"""
    return svg + text


def option_c():
    """Black edition: matte black, a fine violet frame, serif name, a small star in the corner."""
    svg = (SVG_OPEN + """
      <radialGradient id="gBR" cx="1" cy="1" r=".85"><stop offset="0" stop-color="#5E06F2" stop-opacity=".38"/><stop offset="1" stop-color="#5E06F2" stop-opacity="0"/></radialGradient>
      <linearGradient id="streak" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".47" stop-color="#FFFFFF" stop-opacity="0"/>
        <stop offset=".52" stop-color="#C9A6FF" stop-opacity=".07"/><stop offset=".6" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
      <linearGradient id="hair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A95CFF" stop-opacity=".9"/><stop offset=".5" stop-color="#7D18FC" stop-opacity=".35"/><stop offset="1" stop-color="#A95CFF" stop-opacity=".9"/></linearGradient>
      </defs>
      <rect width="896" height="580" fill="#07050F"/><rect width="896" height="580" fill="url(#gBR)"/><rect width="896" height="580" fill="url(#streak)"/>
      <rect x="55" y="55" width="786" height="470" rx="22" fill="none" stroke="url(#hair)" stroke-width="2"/>""" + star(790, 110, 0.62) + '</svg>')
    text = f"""
      <div class="t word" style="left:84px;top:80px;font-size:27px;color:#F5F2FF">nxtlvl<i>social</i></div>
      <div class="t" style="left:84px;top:404px;font-family:'Instrument Serif';font-size:66px;line-height:1;color:#F5F2FF">{NAME}</div>
      <div class="t" style="left:86px;top:482px;font-family:'Instrument Sans';font-weight:600;font-size:15px;letter-spacing:.2em;color:#C9A6FF">{TITLE.upper()}</div>"""
    return svg + text


OPTIONS = {'a-shooting-star': option_a, 'b-violet-foil': option_b, 'c-black-edition': option_c}

if __name__ == '__main__':
    out = os.path.join(HERE, 'html')
    os.makedirs(out, exist_ok=True)
    for slug, fn in OPTIONS.items():
        open(os.path.join(out, f'{slug}.html'), 'w').write(HEAD + fn() + TAIL)
        print('wrote', slug)
