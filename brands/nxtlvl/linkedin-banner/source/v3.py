"""LinkedIn banners, set 3: the three set-2 layouts in the colours of the Shooting Star logo.

The logo's own ground (near-black #0A0620 to #05030C, violet light from the top-left #7E1AF6 and bottom-right
#5E06F2), the star and its white / lilac / violet trails, and white type with a lilac gradient accent. Each option in
the company-page (1128x191) and personal-profile (1584x396) sizes at 1x and 2x; bottom-left kept clear.
Run:  python3 v3.py   (needs Playwright)
"""
import os
import subprocess

from v2 import HERE, OUT, RENDER, SERVICES, SIZES, corners, page, star

WHITE, LILAC, LIFT, PALE = '#FFFFFF', '#B98AFF', '#A95CFF', '#D8BBFF'
GRAD = 'linear-gradient(95deg, #FFFFFF 0%, #EAD9FF 30%, #C9A6FF 62%, #A95CFF 100%)'
CSS = f'.grad {{ background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: .08em; }}'


def ground(w, h):
    """The logo's ground: dark base, violet light in from the top-left and bottom-right corners."""
    gw, gh = (760, 420) if h < 300 else (1100, 820)
    return (f'<div class="abs" style="inset:0;background:linear-gradient(160deg, #0A0620 0%, #05030C 55%, #05030C 100%)"></div>'
            f'<div class="abs" style="inset:0;background:radial-gradient({gw}px {gh}px at 0% 0%, rgba(126,26,246,.78), rgba(126,26,246,0))"></div>'
            f'<div class="abs" style="inset:0;background:radial-gradient({gw}px {gh}px at 100% 100%, rgba(94,6,242,.72), rgba(94,6,242,0))"></div>')


def dust(w, h, n, seed):
    """A few fixed specks of starlight (deterministic positions)."""
    out, x = '', seed
    for i in range(n):
        x = (x * 9301 + 49297) % 233280
        px, py = x % w, (x // w * 37 + i * 53) % h
        out += f'<i class="abs" style="left:{px}px;top:{py}px;width:2px;height:2px;border-radius:50%;background:{PALE};opacity:{.25 + (i % 4) * .15:.2f}"></i>'
    return out


def streak(left, top, size, opacity=1.0):
    """The Shooting Star itself (the logo artwork), star at the top right of its box, trails to the bottom left."""
    return f'<img class="abs" src="file://{HERE}/shooting-star.svg" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;opacity:{opacity}">'


# --- G: logo streak + columns ----------------------------------------------------------------------------

def streak_columns(kind):
    w, h = SIZES[kind]
    c = kind == 'company'
    hx = 330 if c else 520
    hs, ss = (42, 50) if c else (76, 90)
    col = 870 if c else 1200
    sv = 15 if c else 24
    rows = ''.join(f'<div class="cap" style="font-size:{sv}px;color:{WHITE};margin-bottom:{8 if c else 16}px"><b style="color:{LILAC};margin-right:{10 if c else 16}px">0{i + 1}</b>{s}</div>'
                   for i, s in enumerate(SERVICES))
    body = (ground(w, h) + dust(w, h, 26 if c else 40, 7)
            + streak(-4 if c else -20, 4 if c else 12, 250 if c else 460)
            + f'<div class="sans abs" style="left:{hx}px;top:{30 if c else 84}px;font-size:{hs}px;color:{WHITE};line-height:1.04">Your entire<br>creative team,</div>'
            + f'<div class="ser abs grad" style="left:{hx}px;top:{(30 if c else 84) + hs * 2.1:.0f}px;font-size:{ss}px">in one studio.</div>'
            + f'<div class="abs" style="left:{col - (36 if c else 60)}px;top:{24 if c else 60}px;width:1.5px;height:{h - (48 if c else 120)}px;background:linear-gradient(180deg, rgba(216,187,255,0), rgba(216,187,255,.45), rgba(216,187,255,0))"></div>'
            + f'<div class="abs" style="left:{col}px;top:{28 if c else 74}px">{rows}</div>'
            + f'<div class="abs" style="left:{col}px;top:{h - (34 if c else 72)}px;font-size:{15 if c else 23}px;font-weight:600;color:{PALE}">nxtlvlsocial.ai</div>')
    return page(w, h, CSS, body)


# --- H: film slate ---------------------------------------------------------------------------------------

def slate(kind):
    w, h = SIZES[kind]
    c = kind == 'company'
    lab, ins = (13, 14) if c else (19, 26)
    cx = 640 if c else 960
    hs, ss = (54, 64) if c else (96, 112)
    hy = 50 if c else 118
    sv = 15 if c else 22
    t = lambda side, x, y, txt: f'<div class="cap abs" style="{side}:{x}px;top:{y}px;font-size:{lab}px;color:{WHITE};letter-spacing:.24em">{txt}</div>'
    body = (ground(w, h) + dust(w, h, 30 if c else 46, 3)
            + streak(w - (300 if c else 400), 6 if c else 70, 250 if c else 360, .28)
            + corners(w, h, ins, 14 if c else 24, 'rgba(255,255,255,.85)', 2 if c else 3)
            + t('left', ins + (24 if c else 40), ins + (2 if c else 4), 'NXTLVL SOCIAL ✦')
            + f'<div class="cap abs" style="right:{ins + (24 if c else 40)}px;top:{ins + (2 if c else 4)}px;font-size:{lab}px;color:{WHITE};letter-spacing:.24em">'
              f'<i style="display:inline-block;width:{8 if c else 12}px;height:{8 if c else 12}px;border-radius:50%;background:#FF4D6D;margin-right:10px;vertical-align:1px"></i>REC 00:24:15</div>'
            + t('right', ins + (24 if c else 40), h - ins - lab - (2 if c else 4), 'NXTLVLSOCIAL.AI')
            + f'<div class="abs" style="left:{cx}px;top:{hy}px;transform:translateX(-50%);display:flex;align-items:baseline;gap:{14 if c else 24}px">'
              f'<span class="sans" style="font-size:{hs}px;color:{WHITE}">Your brand,</span><span class="ser grad" style="font-size:{ss}px">next level.</span></div>'
            + star(cx + (300 if c else 530), hy - (2 if c else 4), 11 if c else 20, WHITE, ';filter:drop-shadow(0 0 8px #D8BBFF)')
            + f'<div class="cap abs" style="left:{cx}px;top:{hy + hs + (28 if c else 52)}px;transform:translateX(-50%);font-size:{sv}px;color:{PALE};letter-spacing:.3em">'
              + f' <b style="color:{LILAC}">✦</b> '.join(SERVICES) + '</div>')
    return page(w, h, CSS, body)


# --- I: price board --------------------------------------------------------------------------------------

def prices(kind):
    w, h = SIZES[kind]
    c = kind == 'company'
    x0 = 240 if c else 470
    tw, th, gap = (190, 66, 12) if c else (250, 120, 18)
    ty = 66 if c else 156
    tiles = ''
    for i, (lab, val) in enumerate((('Design', '$5'), ('Reels', '$15'), ('Automation', '$49'), ('Websites', None))):
        num = (f'<span class="sans" style="font-size:{28 if c else 54}px;color:{WHITE}">{val}</span><span class="ser" style="font-size:{20 if c else 32}px;color:{PALE};margin-left:4px">/mo</span>'
               if val else f'<span class="ser grad" style="font-size:{26 if c else 42}px">custom quote</span>')
        tiles += (f'<div class="abs" style="left:{x0 + i * (tw + gap)}px;top:{ty}px;width:{tw}px;height:{th}px;border-radius:{14 if c else 22}px;'
                  f'background:linear-gradient(160deg, rgba(126,26,246,.22), rgba(10,6,32,.6));border:1.5px solid rgba(185,138,255,.45);padding:{8 if c else 18}px {14 if c else 24}px">'
                  f'<div class="cap" style="font-size:{11 if c else 17}px;color:{LILAC};margin-bottom:{4 if c else 10}px">{lab}</div><div style="white-space:nowrap">{num}</div></div>')
    body = (ground(w, h) + dust(w, h, 26 if c else 40, 11)
            + streak(-30 if c else -40, 4 if c else 12, 250 if c else 440, .95)
            + f'<div class="abs" style="left:{x0}px;top:{18 if c else 58}px;display:flex;align-items:baseline;gap:{10 if c else 16}px">'
              f'<span class="sans" style="font-size:{32 if c else 50}px;color:{WHITE}">Your entire creative team,</span>'
              f'<span class="ser grad" style="font-size:{38 if c else 58}px">from $5 a month.</span></div>'
            + tiles
            + f'<div class="abs" style="right:{22 if c else 56}px;top:{ty + th + (12 if c else 26)}px;font-size:{14 if c else 22}px;font-weight:600;color:{PALE};white-space:nowrap">'
              f'No contracts · Cancel any month · <b style="color:{WHITE}">nxtlvlsocial.ai</b></div>')
    return page(w, h, CSS, body)


def main():
    jobs = []
    for opt, fn in (('logo-streak', streak_columns), ('logo-slate', slate), ('logo-prices', prices)):
        for kind, (w, h) in SIZES.items():
            src = os.path.join(HERE, f'{opt}-{w}x{h}.html')
            with open(src, 'w') as f:
                f.write(fn(kind))
            jobs += [src, os.path.join(OUT, f'{opt}-{w}x{h}.png'), str(w), str(h), '1',
                     src, os.path.join(OUT, f'{opt}-{w}x{h}@2x.png'), str(w), str(h), '2']
    subprocess.run(['node', RENDER] + jobs, check=True, stdout=subprocess.DEVNULL)
    for f in os.listdir(HERE):
        if f.endswith('.html'):
            os.remove(os.path.join(HERE, f))
    print('rendered', len(jobs) // 5, 'files to', OUT)


if __name__ == '__main__':
    main()
