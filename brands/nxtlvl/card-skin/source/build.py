"""Build the debit-card skin designs for Rishabh Rana (CMO, Nxtlvl Social).

Writes one HTML page per option into ./html/, then render.js turns them into print files.
Units: 10 CSS px = 1 mm. The canvas is the card plus 2 mm bleed on every side:
  card (ISO/IEC 7810 ID-1) 85.60 x 53.98 mm  ->  canvas 89.6 x 58.0 mm = 896 x 580 px
The "nxtlvl" wordmark is the original logo artwork (website/logo.png, as nxtlvl-wordmark-mask.png), used as a
mask so it can be filled with metal or foil gradients.
Run:  python3 build.py && node render.js && python3 finish.py
"""
import base64
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'website', 'fonts'))
MASK = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, 'nxtlvl-wordmark-mask.png'), 'rb').read()).decode()
WORD_RATIO = 2148 / 477                 # wordmark width / height
NAME, TITLE, ROLE = 'Rishabh Rana', 'Chief Marketing Officer', 'CMO'

W, H, BLEED = 896, 580, 20            # canvas px, bleed px (2 mm)
SAFE = BLEED + 30                       # 3 mm inside the cut line

STAR_DEFS = open(os.path.join(HERE, 'star-defs.svgfrag')).read()
STAR_PATHS = open(os.path.join(HERE, 'star-paths.svgfrag')).read()
SPARK = 'M0-1C.06-.34.34-.06 1 0 .34.06.06.34 0 1-.06.34-.34.06-1 0-.34-.06-.06-.34 0-1Z'   # four-point star, r=1


def star(x, y, scale, opacity=1.0):
    """The Shooting Star mark with its star head at (x, y); scale 1 = mark units (trail ~166 long)."""
    return (f'<g transform="translate({x} {y}) scale({scale}) translate(-140 -60)" opacity="{opacity}">'
            f'{STAR_PATHS}</g>')


def guilloche(y0, lines, gap, colour, opacity, width=0.7, seed=0):
    """Fine security-print wave lines, the kind used on banknotes and premium cards."""
    out = []
    for i in range(lines):
        pts = []
        for x in range(-20, W + 21, 6):
            y = (y0 + i * gap + 26 * math.sin(x / 92 + i * 0.32 + seed)
                 + 11 * math.sin(x / 37 - i * 0.21 + seed * 2))
            pts.append(f'{x},{y:.1f}')
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colour}" stroke-width="{width}"/>')
    return f'<g opacity="{opacity}">{"".join(out)}</g>'


def sparkles(seed, box, n, colour='#FFFFFF'):
    """A scatter of tiny four-point stars and dots inside box=(x0, y0, x1, y1)."""
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(box[0], box[2]), r.uniform(box[1], box[3])
        if r.random() < 0.3:
            s = r.uniform(3, 7)
            out.append(f'<path d="{SPARK}" transform="translate({x:.1f} {y:.1f}) scale({s:.2f})" fill="{colour}" opacity="{r.uniform(.5, .95):.2f}"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(.6, 1.5):.2f}" fill="{colour}" opacity="{r.uniform(.25, .8):.2f}"/>')
    return ''.join(out)


def grain(opacity, seed=3, freq=0.85, blend='overlay'):
    return (f'<svg class="layer" style="mix-blend-mode:{blend}" viewBox="0 0 {W} {H}"><filter id="n{seed}">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="2" seed="{seed}" stitchTiles="stitch"/>'
            f'<feColorMatrix type="saturate" values="0"/></filter>'
            f'<rect width="{W}" height="{H}" filter="url(#n{seed})" opacity="{opacity}"/></svg>')


def lockup(x, y, height, fill, social_colour, shadow='none'):
    """The original nxtlvl wordmark (filled with `fill`, any CSS background) plus 'social' set wide to match."""
    w = height * WORD_RATIO
    return (f'<div class="t" style="left:{x}px;top:{y}px;display:flex;align-items:flex-end;gap:{height * .42:.1f}px;filter:{shadow}">'
            f'<div style="width:{w:.1f}px;height:{height}px;background:{fill};-webkit-mask:url({MASK}) center/100% 100% no-repeat"></div>'
            f'<div style="font-family:Archivo;font-weight:500;font-stretch:125%;font-size:{height * 1.02:.1f}px;line-height:.74;'
            f'letter-spacing:.01em;color:{social_colour}">social</div></div>')


HEAD = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Archivo;src:url('file://{FONTS}/archivo-variable.woff2') format('woff2');font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:'Instrument Sans';src:url('file://{FONTS}/instrument-sans-500.woff2') format('woff2');font-weight:500}}
@font-face{{font-family:'Instrument Sans';src:url('file://{FONTS}/instrument-sans-600.woff2') format('woff2');font-weight:600}}
@font-face{{font-family:'Instrument Serif';src:url('file://{FONTS}/instrument-serif-400.woff2') format('woff2');font-weight:400}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.c{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.c>svg,.layer{{position:absolute;inset:0;width:{W}px;height:{H}px}}
.t{{position:absolute;white-space:nowrap;-webkit-font-smoothing:antialiased}}
.name{{font-family:Archivo;font-weight:600;font-stretch:125%;letter-spacing:.13em}}
.title{{font-family:'Instrument Sans';font-weight:500;letter-spacing:.03em}}
</style></head><body><div class="c">"""
TAIL = '</div></body></html>'
SVG_OPEN = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs>{STAR_DEFS}'

SILVER = 'linear-gradient(100deg,#FFFFFF 0%,#E9E1FA 38%,#B9A9D9 52%,#FFFFFF 66%,#D8BBFF 100%)'
CHROME = 'linear-gradient(180deg,#FFFFFF 0%,#D9D4E4 44%,#8E87A3 50%,#ECE8F4 62%,#BDB5CF 100%)'


def option_a():
    """Shooting star: deep ink, violet light, a glowing star with lens flare, a sparkle field and fine wave lines."""
    svg = (SVG_OPEN + """
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B0624"/><stop offset=".55" stop-color="#05030C"/><stop offset="1" stop-color="#0A0420"/></linearGradient>
      <radialGradient id="gTR" cx="1" cy="0" r=".8"><stop offset="0" stop-color="#7E1AF6" stop-opacity=".85"/><stop offset=".5" stop-color="#5E06F2" stop-opacity=".25"/><stop offset="1" stop-color="#5E06F2" stop-opacity="0"/></radialGradient>
      <radialGradient id="gBL" cx="0" cy="1" r=".75"><stop offset="0" stop-color="#5E06F2" stop-opacity=".6"/><stop offset="1" stop-color="#5E06F2" stop-opacity="0"/></radialGradient>
      <radialGradient id="halo" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(765 128) scale(170)">
        <stop offset="0" stop-color="#F1E6FF" stop-opacity=".75"/><stop offset=".25" stop-color="#C79BFF" stop-opacity=".35"/><stop offset="1" stop-color="#7D18FC" stop-opacity="0"/></radialGradient>
      <linearGradient id="flare" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C79BFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".85"/><stop offset="1" stop-color="#C79BFF" stop-opacity="0"/></linearGradient>
      </defs>
      <rect width="896" height="580" fill="url(#bg)"/><rect width="896" height="580" fill="url(#gTR)"/><rect width="896" height="580" fill="url(#gBL)"/>"""
           + guilloche(300, 22, 9, '#A95CFF', .16, seed=.4)
           + sparkles(11, (420, 30, 880, 330), 70) + sparkles(12, (30, 120, 400, 400), 18, '#D8BBFF')
           + '<circle cx="765" cy="128" r="170" fill="url(#halo)"/>'
           + star(765, 128, 3.35)
           + '<rect x="560" y="126.6" width="410" height="2.8" fill="url(#flare)"/>'
           + '</svg>')
    text = (lockup(SAFE, SAFE + 2, 30, SILVER, '#D8BBFF', 'drop-shadow(0 0 6px rgba(169,92,255,.45))') + f"""
      <div class="t name" style="left:{SAFE}px;top:446px;font-size:28px;color:#F5F2FF">{NAME.upper()}</div>
      <div class="t title" style="left:{SAFE + 1}px;top:488px;font-size:18px;color:#C9A6FF">{TITLE}</div>
      <div class="t" style="right:{SAFE + 2}px;top:470px;padding-right:8px;font-family:'Instrument Serif';font-style:italic;font-size:52px;line-height:1;
        background:{SILVER};-webkit-background-clip:text;color:transparent">{ROLE}</div>""")
    return svg + text + grain(.10)


def option_b():
    """Holo foil: iridescent violet with glossy light bands, an embossed watermark star and a foil wordmark."""
    svg = (SVG_OPEN + """
      <linearGradient id="bg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#3A0790"/><stop offset=".4" stop-color="#7D18FC"/><stop offset=".72" stop-color="#B26BFF"/><stop offset="1" stop-color="#E3C6FF"/></linearGradient>
      <linearGradient id="iri" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#FF7AD9" stop-opacity=".0"/><stop offset=".3" stop-color="#FF7AD9" stop-opacity=".22"/>
        <stop offset=".5" stop-color="#7FE3FF" stop-opacity=".2"/><stop offset=".7" stop-color="#B8FFCE" stop-opacity=".12"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
      <linearGradient id="band" x1="0" y1="0" x2="1" y2=".55">
        <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".34" stop-color="#FFFFFF" stop-opacity="0"/>
        <stop offset=".44" stop-color="#FFFFFF" stop-opacity=".34"/><stop offset=".47" stop-color="#FFFFFF" stop-opacity=".08"/>
        <stop offset=".55" stop-color="#FFFFFF" stop-opacity=".2"/><stop offset=".62" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
      <filter id="dk"><feColorMatrix type="matrix" values="0 0 0 0 .1  0 0 0 0 .01  0 0 0 0 .25  0 0 0 .32 0"/></filter>
      <radialGradient id="dark" cx=".05" cy="1" r=".85"><stop offset="0" stop-color="#14033A" stop-opacity=".75"/><stop offset="1" stop-color="#14033A" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="896" height="580" fill="url(#bg)"/><rect width="896" height="580" fill="url(#iri)"/><rect width="896" height="580" fill="url(#dark)"/>"""
           + guilloche(40, 30, 8, '#FFFFFF', .10, 0.6, seed=1.7)
           + f'<g transform="translate(3 4)" filter="url(#dk)">{star(740, 150, 5.4)}</g>'
           + star(740, 150, 5.4, .2)
           + '<rect width="896" height="580" fill="url(#band)"/>'
           + sparkles(21, (470, 30, 880, 300), 26)
           + '</svg>')
    shade = 'drop-shadow(0 2px 3px rgba(30,0,70,.45))'
    text = (lockup(SAFE, SAFE + 2, 30, 'linear-gradient(100deg,#FFFFFF,#FFF0FF 45%,#E2F7FF 70%,#FFFFFF)', '#FFFFFF', shade) + f"""
      <div class="t name" style="left:{SAFE}px;top:446px;font-size:28px;color:#FFFFFF;filter:{shade}">{NAME.upper()}</div>
      <div class="t title" style="left:{SAFE + 1}px;top:488px;font-size:18px;color:#F3E8FF;filter:{shade}">{TITLE}</div>
      <div class="t" style="right:{SAFE + 10}px;top:470px;font-family:'Instrument Serif';font-style:italic;font-size:52px;line-height:1;color:#FFFFFF;filter:{shade}">{ROLE}</div>""")
    return svg + text + grain(.12, seed=5)


def option_c():
    """Black metal: brushed graphite, a violet edge glow, a chrome wordmark and a glowing star."""
    svg = (SVG_OPEN + """
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#16131F"/><stop offset=".5" stop-color="#0A0811"/><stop offset="1" stop-color="#05040A"/></linearGradient>
      <linearGradient id="spec" x1="0" y1="0" x2="1" y2=".75">
        <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".3" stop-color="#FFFFFF" stop-opacity="0"/>
        <stop offset=".42" stop-color="#E9E1FA" stop-opacity=".09"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
      <radialGradient id="gBR" cx="1" cy="1" r=".9"><stop offset="0" stop-color="#6A12F5" stop-opacity=".55"/><stop offset=".55" stop-color="#5E06F2" stop-opacity=".12"/><stop offset="1" stop-color="#5E06F2" stop-opacity="0"/></radialGradient>
      <radialGradient id="sh" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(795 104) scale(80)">
        <stop offset="0" stop-color="#C79BFF" stop-opacity=".55"/><stop offset="1" stop-color="#7D18FC" stop-opacity="0"/></radialGradient>
      <linearGradient id="hair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C79BFF" stop-opacity=".9"/><stop offset=".5" stop-color="#7D18FC" stop-opacity=".25"/><stop offset="1" stop-color="#C79BFF" stop-opacity=".9"/></linearGradient>
      <filter id="brush"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.9" numOctaves="2" seed="8"/><feColorMatrix type="saturate" values="0"/></filter>
      </defs>
      <rect width="896" height="580" fill="url(#bg)"/>
      <rect width="896" height="580" filter="url(#brush)" opacity=".10" style="mix-blend-mode:screen"/>
      <rect width="896" height="580" fill="url(#gBR)"/><rect width="896" height="580" fill="url(#spec)"/>
      <rect x="55" y="55" width="786" height="470" rx="22" fill="none" stroke="url(#hair)" stroke-width="1.6"/>
      <circle cx="795" cy="104" r="80" fill="url(#sh)"/>""" + star(800, 98, 0.66) + '</svg>')
    text = (lockup(84, 82, 26, CHROME, '#E6DEF5') + f"""
      <div class="t" style="left:82px;top:398px;font-family:'Instrument Serif';font-size:70px;line-height:1;
        background:{CHROME};-webkit-background-clip:text;color:transparent">{NAME}</div>
      <div class="t" style="left:86px;top:482px;font-family:'Instrument Sans';font-weight:600;font-size:15px;letter-spacing:.24em;color:#C9A6FF">{TITLE.upper()}</div>""")
    return svg + text + grain(.07, seed=9)


OPTIONS = {'a-shooting-star': option_a, 'b-violet-foil': option_b, 'c-black-edition': option_c}

if __name__ == '__main__':
    out = os.path.join(HERE, 'html')
    os.makedirs(out, exist_ok=True)
    for slug, fn in OPTIONS.items():
        open(os.path.join(out, f'{slug}.html'), 'w').write(HEAD + fn() + TAIL)
        print('wrote', slug)
