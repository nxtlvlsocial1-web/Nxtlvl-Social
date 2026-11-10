"""LinkedIn banners, set 2: in the look of the v2 launch film (nxtlvl-launch-16x9).

Three options (D colour blocks, E film slate, F price board), each in the company-page size (1128x191) and the
personal-profile size (1584x396), rendered at 1x and 2x. The bottom-left corner stays clear: LinkedIn puts the page
logo or profile photo there.  Run:  python3 v2.py   (needs Playwright)
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
FONTS = os.path.join(REPO, 'website', 'fonts')
SERIF_IT = os.path.join(REPO, 'brands', 'nxtlvl-edits', 'source', 'fonts', 'instrument-serif-italic-400.woff2')
RENDER = os.path.join(REPO, 'brands', 'nxtlvl-edits', 'source', 'render.js')

INK, VIOLET, LIFT, PALE, MIST, TEXT = '#05030C', '#7D18FC', '#A95CFF', '#D8BBFF', '#F5F2FF', '#0B0816'
SPARK = 'M0-1C.06-.34.34-.06 1 0 .34.06.06.34 0 1-.06.34-.34.06-1 0-.34-.06-.06-.34 0-1Z'
SIZES = {'company': (1128, 191), 'personal': (1584, 396)}
SERVICES = ['Design', 'Reels', 'Automation', 'Websites']


def page(w, h, css, body):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Archivo"; src: url("file://{FONTS}/archivo-variable.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
@font-face {{ font-family: "Instrument Sans"; src: url("file://{FONTS}/instrument-sans-400.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Instrument Sans"; src: url("file://{FONTS}/instrument-sans-600.woff2") format("woff2"); font-weight: 600; }}
@font-face {{ font-family: "Serif Italic"; src: url("file://{SERIF_IT}") format("woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
body {{ position: relative; font-family: "Instrument Sans", sans-serif; -webkit-font-smoothing: antialiased; }}
.abs {{ position: absolute; }}
.sans {{ font-family: "Archivo", sans-serif; font-weight: 900; font-stretch: 112%; letter-spacing: -.04em; line-height: 1; white-space: nowrap; }}
.ser {{ font-family: "Serif Italic", serif; line-height: 1; white-space: nowrap; }}
.cap {{ font-family: "Instrument Sans", sans-serif; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; white-space: nowrap; }}
{css}
</style></head><body>{body}</body></html>'''


def star(x, y, r, fill, extra=''):
    return f'<svg class="abs" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;overflow:visible{extra}" viewBox="-1 -1 2 2"><path d="{SPARK}" fill="{fill}"/></svg>'


def corners(w, h, inset, size, colour, stroke):
    out = ''
    for sx, sy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        x = inset if sx == 0 else w - inset - size
        y = inset if sy == 0 else h - inset - size
        bw = f'{stroke}px {stroke if sx else 0}px {stroke if sy else 0}px {0 if sx else stroke}px'
        bw = (f'{0 if sy else stroke}px {stroke if sx else 0}px {stroke if sy else 0}px {0 if sx else stroke}px')
        out += f'<div class="abs" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;border:solid {colour};border-width:{bw}"></div>'
    return out


# --- D: colour blocks ------------------------------------------------------------------------------------

def blocks(kind):
    w, h = SIZES[kind]
    c = kind == 'company'
    a, b = (280, 830) if c else (430, 1150)               # block edges: violet | mist | ink
    hs, ss = (44, 52) if c else (78, 92)                  # headline sizes
    hx, hy = (a + 40, 30) if c else (a + 56, 82)
    lock_w = 170 if c else 280
    sv = 16 if c else 25
    rows = ''.join(f'<div class="cap" style="font-size:{sv}px;color:{MIST};margin-bottom:{8 if c else 16}px"><b style="color:{LIFT};margin-right:{10 if c else 16}px">0{i + 1}</b>{s}</div>'
                   for i, s in enumerate(SERVICES))
    body = (f'<div class="abs" style="left:0;top:0;width:{a}px;height:{h}px;background:{VIOLET}"></div>'
            f'<div class="abs" style="left:{a}px;top:0;width:{b - a}px;height:{h}px;background:{MIST}"></div>'
            f'<div class="abs" style="left:{b}px;top:0;width:{w - b}px;height:{h}px;background:radial-gradient({w - b}px {h}px at 60% 40%, #2A0E62, {INK})"></div>'
            # the lockup sits high in the violet block, clear of the logo / photo
            f'<img class="abs" src="file://{HERE}/shooting-star.svg" style="left:{18 if c else 34}px;top:{14 if c else 30}px;width:{lock_w * .32:.0f}px">'
            f'<img class="abs" src="file://{HERE}/nxtlvl-wordmark.png" style="left:{18 + lock_w * .36 if c else 34 + lock_w * .36:.0f}px;top:{24 if c else 46}px;width:{lock_w * .6:.0f}px">'
            f'<div class="abs" style="left:{18 + lock_w * .36 if c else 34 + lock_w * .36:.0f}px;top:{24 + lock_w * .6 * 165 / 720 + 6 if c else 46 + lock_w * .6 * 165 / 720 + 10:.0f}px;font-size:{20 if c else 32}px;color:{MIST};letter-spacing:.02em">social</div>'
            f'<div class="sans abs" style="left:{hx}px;top:{hy}px;font-size:{hs}px;color:{TEXT};line-height:1.04">Your entire<br>creative team,</div>'
            f'<div class="ser abs" style="left:{hx}px;top:{hy + hs * 2.1:.0f}px;font-size:{ss}px;color:{VIOLET}">in one studio.</div>'
            f'<div class="abs" style="left:{b + (34 if c else 56)}px;top:{30 if c else 74}px">{rows}</div>'
            f'<div class="abs" style="left:{b + (34 if c else 56)}px;top:{h - (32 if c else 70)}px;font-size:{15 if c else 23}px;font-weight:600;color:{PALE}">nxtlvlsocial.ai</div>'
            + star(b - (40 if c else 70), h - (40 if c else 70), 12 if c else 20, VIOLET))
    return page(w, h, '', body)


# --- E: film slate ---------------------------------------------------------------------------------------

def slate(kind):
    w, h = SIZES[kind]
    c = kind == 'company'
    lab = 13 if c else 19
    ins = 14 if c else 26
    cx = 640 if c else 960                                # headline centre, pushed right of the logo / photo
    hs, ss = (54, 64) if c else (96, 112)
    hy = 52 if c else 120
    sv = 15 if c else 22
    t = lambda x, y, txt, align='left': (f'<div class="cap abs" style="{align}:{x}px;top:{y}px;font-size:{lab}px;color:{MIST};letter-spacing:.24em">{txt}</div>')
    body = (f'<div class="abs" style="inset:0;background:radial-gradient({w * .7:.0f}px {h * 1.4:.0f}px at 58% 30%, #2A0E62, {INK} 70%)"></div>'
            + corners(w, h, ins, 14 if c else 24, MIST, 2 if c else 3)
            + t(ins + (24 if c else 40), ins + (2 if c else 4), 'NXTLVL SOCIAL ✦')
            + f'<div class="cap abs" style="right:{ins + (24 if c else 40)}px;top:{ins + (2 if c else 4)}px;font-size:{lab}px;color:{MIST};letter-spacing:.24em">'
              f'<i style="display:inline-block;width:{8 if c else 12}px;height:{8 if c else 12}px;border-radius:50%;background:#FF4D6D;margin-right:10px;vertical-align:1px"></i>REC 00:24:15</div>'
            + t(ins + (24 if c else 40), h - ins - lab - (2 if c else 4), 'NXTLVLSOCIAL.AI', 'right')
            + f'<div class="abs" style="left:{cx}px;top:{hy}px;transform:translateX(-50%);display:flex;align-items:baseline;gap:{14 if c else 24}px">'
              f'<span class="sans" style="font-size:{hs}px;color:{MIST}">Your brand,</span><span class="ser" style="font-size:{ss}px;color:{PALE}">next level.</span></div>'
            + f'<div class="cap abs" style="left:{cx}px;top:{hy + hs + (26 if c else 50)}px;transform:translateX(-50%);font-size:{sv}px;color:{PALE};letter-spacing:.3em">'
              + f' <b style="color:{LIFT}">✦</b> '.join(SERVICES) + '</div>')
    return page(w, h, '', body)


# --- F: price board --------------------------------------------------------------------------------------

def prices(kind):
    w, h = SIZES[kind]
    c = kind == 'company'
    x0 = 240 if c else 470
    tw, th, gap = (190, 66, 12) if c else (250, 120, 18)
    ty = 66 if c else 156
    tiles = ''
    for i, (lab, val, unit) in enumerate((('Design', '$5', '/mo'), ('Reels', '$15', '/mo'), ('Automation', '$49', '/mo'), ('Websites', 'custom', 'quote'))):
        num = (f'<span class="sans" style="font-size:{28 if c else 54}px;color:#FFFFFF">{val}</span><span class="ser" style="font-size:{20 if c else 32}px;color:{PALE};margin-left:4px">{unit}</span>'
               if val.startswith('$') else f'<span class="ser" style="font-size:{26 if c else 42}px;color:#FFFFFF">custom quote</span>')
        tiles += (f'<div class="abs" style="left:{x0 + i * (tw + gap)}px;top:{ty}px;width:{tw}px;height:{th}px;border-radius:{14 if c else 22}px;'
                  f'background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.28);padding:{8 if c else 18}px {14 if c else 24}px">'
                  f'<div class="cap" style="font-size:{11 if c else 17}px;color:{PALE};margin-bottom:{4 if c else 10}px">{lab}</div><div style="white-space:nowrap">{num}</div></div>')
    body = (f'<div class="abs" style="inset:0;background:radial-gradient({w * .6:.0f}px {h * 1.6:.0f}px at 78% 0%, #B57BFF, {VIOLET} 45%, #4B0BA8)"></div>'
            f'<img class="abs" src="file://{HERE}/shooting-star.svg" style="left:{-30 if c else -40}px;top:{-40 if c else -70}px;width:{200 if c else 380}px;opacity:.22">'
            f'<div class="abs" style="left:{x0}px;top:{18 if c else 58}px;display:flex;align-items:baseline;gap:{10 if c else 16}px">'
            f'<span class="sans" style="font-size:{32 if c else 50}px;color:#FFFFFF">Your entire creative team,</span>'
            f'<span class="ser" style="font-size:{38 if c else 58}px;color:{MIST}">from $5 a month.</span></div>'
            + tiles
            + f'<div class="abs" style="right:{22 if c else 56}px;top:{ty + th + (12 if c else 26)}px;font-size:{14 if c else 22}px;font-weight:600;color:{MIST};white-space:nowrap">'
              f'No contracts · Cancel any month · <b>nxtlvlsocial.ai</b></div>')
    return page(w, h, '', body)


def main():
    jobs = []
    for opt, fn in (('editorial-blocks', blocks), ('film-slate', slate), ('price-board', prices)):
        for kind, (w, h) in SIZES.items():
            src = os.path.join(HERE, f'{opt}-{w}x{h}.html')
            with open(src, 'w') as f:
                f.write(fn(kind))
            jobs += [src, os.path.join(OUT, f'{opt}-{w}x{h}.png'), str(w), str(h), '1',
                     src, os.path.join(OUT, f'{opt}-{w}x{h}@2x.png'), str(w), str(h), '2']
    subprocess.run(['node', RENDER] + jobs, check=True, stdout=subprocess.DEVNULL)
    print('rendered', len(jobs) // 5, 'files to', OUT)


if __name__ == '__main__':
    main()
