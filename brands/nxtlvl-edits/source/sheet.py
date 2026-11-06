"""Renders the concepts to PNG and lays them out on comparison sheets.

Run after build.py / build2.py:  python3 sheet.py      (round 1 -> ../concepts-preview.png)
                                 python3 sheet.py 2    (round 2 -> ../concepts-preview-2a.png and -2b.png)
                                 python3 sheet.py 3    (round 3 -> ../concepts-preview-3a.png and -3b.png)
                                 python3 sheet.py 4    (R refined -> ../concepts-preview-4.png)
                                 python3 sheet.py 5    (round 5 -> ../concepts-preview-5a.png and -5b.png)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
CONCEPTS = os.path.join(ROOT, 'concepts')
FONTS = '../../../website/fonts'                       # relative to sheet.html, which lives here
HANDLE = 'nxtlvlledits'

ITEMS = [
    ('a-cut-star', 'A', 'Cut Star',
     'The Nxtlvl Social star, sliced by two razor cuts that run through all three trails, like one cut through '
     'every track of a timeline. The closest sibling to the main account.'),
    ('b-clip-n', 'B', 'Clip N',
     'The Smooth N from the Nxtlvl logo, cut into three clips. Same brand, edited.'),
    ('c-timeline-steps', 'C', 'Timeline Steps',
     'Three clips on a timeline, each track a step higher (the next level), with a star-headed playhead '
     'cutting through them. The most "editor" of the four.'),
    ('d-wordmark', 'D', 'Wordmark',
     'nxtlvl over edits in the serif from the ad, the i dotted with the star, inside camera viewfinder '
     'corners with a REC dot. Says the name outright.'),
]

ITEMS_2 = [
    ('e-play-star', 'E', 'Play Star',
     'A rounded play button in the brand gradient with the Nxtlvl star cut out of it. Says "video" from across the room.'),
    ('f-film-nx', 'F', 'Film nx',
     'A film frame with sprocket holes, "nx" from the original logo lettering in the window, and a small star.'),
    ('g-ne-monogram', 'G', 'ne Monogram',
     'The "n" from the nxtlvl lettering with an "e" for edits in the serif biting into it. Two fonts, one mark.'),
    ('h-star-frame', 'H', 'Star in Frame',
     'The Shooting Star, unchanged, inside camera viewfinder corners with a REC dot. Main account\'s star, now on camera.'),
    ('i-beat-bars', 'I', 'Beat Bars',
     'Audio levels that climb to the next level; the tallest bar wears the star, so the last bar reads like an "i".'),
    ('j-clapper', 'J', 'Clapper',
     'A film clapperboard in the brand violet with the star on the board. The classic "we make videos" sign.'),
    ('k-violet-stack', 'K', 'Violet Stack',
     'D\'s wordmark without the frame, white on full violet. Stands out in a dark feed and next to the main account.'),
    ('l-cut-star-light', 'L', 'Cut Star, Light',
     'A\'s Cut Star in violet on a light ground, so the edits account looks related to the main one, not identical.'),
]

ITEMS_3 = [
    ('m-serif-e', 'M', 'Serif e',
     'One italic "e" for edits in the serif, Mist on Ink, with a tiny violet star. Nothing else.'),
    ('n-seal', 'N', 'Seal',
     'A fine double ring with NXTLVL · EDITS set around it and the star at the centre, like a maker\'s stamp.'),
    ('o-split-star', 'O', 'Split Star',
     'The Nxtlvl star cut once on the diagonal, its halves slipping along the cut. Ink on Mist.'),
    ('p-editorial-stack', 'P', 'Editorial Stack',
     'nxtlvl small over edits large in the serif, Ink on Mist, like a magazine masthead.'),
    ('q-sliced-edits', 'Q', 'Sliced edits',
     'The word edits with one hairline cut through it, the top half nudged over: the edit, done to the name itself.'),
    ('r-monoline-n', 'R', 'Monoline N',
     'The Smooth N from the main logo drawn as a single fine line, with the violet star at its tip.'),
    ('s-ne-ligature', 'S', 'ne Ligature',
     'n and e in the serif, set tight like a monogram on flat night violet, with a small star.'),
    ('t-cut-line', 'T', 'Cut Line',
     'A timeline reduced to one line with a single cut in it, and the star above the cut.'),
]

ITEMS_4 = [
    ('r1-monoline-pearl', 'R1', 'Pearl',
     'The refined line: exact turns, one straight diagonal, the right stem climbing past the left and tapering to a '
     'needle point under the star. Pearl sheen on rich black. The pick for the profile picture.'),
    ('r2-monoline-medallion', 'R2', 'Medallion',
     'R1 inside a fine double ring, like a hallmark or a watch dial. Most "luxury" of the set.'),
    ('r3-monoline-night', 'R3', 'Night',
     'R1 on deep night violet, the same violet world as Nxtlvl Social but quieter.'),
    ('r4-monoline-ivory', 'R4', 'Ivory',
     'Ink line on ivory with a violet star, like letterpress on good paper. Stands out in a dark feed.'),
    ('r5-monoline-pen', 'R5', 'Broad Pen',
     'The same N drawn with a broad pen: thick uprights and diagonal, hairline turns. Bolder, more fashion-house.'),
]

ITEMS_5 = [
    ('u-two-pillars', 'U', 'Two Pillars',
     'Two uprights with angled ends on one invisible diagonal: your eye draws the N. The right one stands higher.'),
    ('v-reel-frame', 'V', 'Reel Frame',
     'The fine N inside a 9:16 Reel frame, its star breaking through the top edge.'),
    ('w-folded-n', 'W', 'Folded N',
     'An N folded from a single ribbon: the uprights face you, the diagonal is the ribbon\'s shaded underside.'),
    ('x-editorial-n', 'X', 'Editorial N',
     'A tall, high-contrast serif capital N, like a fashion-magazine masthead, with the star at its corner.'),
    ('y-n-disc', 'Y', 'N Disc',
     'A solid disc with the N and the star cut out of it, like a coin or a wax seal. The boldest at small sizes.'),
    ('z-ne-monogram', 'Z', 'NE Monogram',
     'N and E sharing one upright, drawn in one even line: nxtlvl edits in two letters.'),
]

ROUNDS = {
    '1': [(ITEMS, 'concepts-preview.png', 'nxtlvl edits · logo concepts', 'Four directions for the edits account')],
    '2': [(ITEMS_2[:4], 'concepts-preview-2a.png', 'nxtlvl edits · more variations (1 of 2)', 'Eight more directions: E to H'),
          (ITEMS_2[4:], 'concepts-preview-2b.png', 'nxtlvl edits · more variations (2 of 2)', 'Eight more directions: I to L')],
    '3': [(ITEMS_3[:4], 'concepts-preview-3a.png', 'nxtlvl edits · minimal and classy (1 of 2)', 'Minimal and classy: M to P'),
          (ITEMS_3[4:], 'concepts-preview-3b.png', 'nxtlvl edits · minimal and classy (2 of 2)', 'Minimal and classy: Q to T')],
    '4': [(ITEMS_4, 'concepts-preview-4.png', 'nxtlvl edits · R, refined', 'The Monoline N, made premium')],
    '5': [(ITEMS_5[:3], 'concepts-preview-5a.png', '@nxtlvlledits · new lettermarks (1 of 2)', 'Something else: U to W'),
          (ITEMS_5[3:], 'concepts-preview-5b.png', '@nxtlvlledits · new lettermarks (2 of 2)', 'Something else: X to Z')],
}

BEFORE_AFTER = '''
  <section class="ba">
    <figure><img src="../concepts/r-monoline-n/profile.svg" alt=""><figcaption>Before</figcaption></figure>
    <span class="arrow">→</span>
    <figure><img src="../concepts/r1-monoline-pearl/profile.svg" alt=""><figcaption>After</figcaption></figure>
    <ul>
      <li>Rebuilt from exact turns and one straight diagonal, so it reads as an N, not a squiggle</li>
      <li>Right stem climbs past the left (the next level) and tapers to a point</li>
      <li>The star sits right on the tip, as if the line ends in a spark</li>
      <li>Pearl sheen instead of flat white; a richer black</li>
    </ul>
  </section>'''


def size_of(svg_path):
    m = re.search(r'width="(\d+)" height="(\d+)"', open(svg_path).read())
    return int(m.group(1)), int(m.group(2))


def card(slug, letter, name, idea):
    if not os.path.exists(os.path.join(CONCEPTS, slug, 'lockup.svg')):
        return card_alts(slug, letter, name, idea)
    lw, lh = size_of(os.path.join(CONCEPTS, slug, 'lockup.svg'))
    bg = re.search(r'</defs><rect width="\d+" height="\d+" fill="([^"]+)"', open(os.path.join(CONCEPTS, slug, 'lockup.svg')).read()).group(1)
    return f'''
  <section class="card">
    <img class="big" src="../concepts/{slug}/profile.svg" alt="">
    <div class="info">
      <p class="tag">{letter}</p>
      <h2>{name}</h2>
      <p class="idea">{idea}</p>
      <div class="ig">
        <img class="av110" src="../concepts/{slug}/profile.svg" alt="">
        <div><b>{HANDLE}</b><span>nxtlvl edits</span></div>
        <img class="av56" src="../concepts/{slug}/profile.svg" alt="">
        <img class="av32" src="../concepts/{slug}/profile.svg" alt="">
      </div>
    </div>
    <div class="lockup" style="background:{bg}"><img src="../concepts/{slug}/lockup.svg" style="width:{lw / 1600 * 100:.2f}%;aspect-ratio:{lw}/{lh}" alt=""></div>
  </section>'''


LEDE = ("Each one is from the Nxtlvl Social family (the star, the N, the wordmark, the violet), with an editor's cut. "
        "Shown as the Instagram profile picture at full size and at the sizes people actually see it.")
LEDE_4 = ("R, taken further: a cleaner N, a finer finish and five ways to wear it. "
          "Shown at full size and at the sizes people actually see it.")
LEDE_5 = ("New directions, symbol only. Each one on rich black (the profile picture), then on ivory and on violet, "
          "to show it holds up anywhere.")
LEDE_3 = ("Flat colour, no glow, one violet accent at most: Ink, Mist and the serif, with plenty of empty space. "
          "Still the Nxtlvl family, quieter. Shown at full size and at the sizes people actually see it.")


def card_alts(slug, letter, name, idea):
    """A card for a symbol-only concept: the lockup strip becomes the mark on ivory and on violet."""
    return f'''
  <section class="card">
    <img class="big" src="../concepts/{slug}/profile.svg" alt="">
    <div class="info">
      <p class="tag">{letter}</p>
      <h2>{name}</h2>
      <p class="idea">{idea}</p>
      <div class="ig">
        <img class="av110" src="../concepts/{slug}/profile.svg" alt="">
        <div><b>{HANDLE}</b><span>profile size</span></div>
        <img class="av56" src="../concepts/{slug}/profile.svg" alt="">
        <img class="av32" src="../concepts/{slug}/profile.svg" alt="">
      </div>
    </div>
    <div class="alts"><div style="background:#F5F2FF"><img src="../concepts/{slug}/alt-light.svg" alt=""></div><div style="background:#7D18FC"><img src="../concepts/{slug}/alt-violet.svg" alt=""></div></div>
  </section>'''


FOOTER = ('<b>Every concept uses the same wordmark:</b> "nxtlvl" in the original logo lettering, then "edits" in Instrument Serif '
          'Italic with the star over the i. Pick one from any round, or mix two (say one mark with another\'s colours), and I\'ll make the full kit.')
FOOTER_5 = ('<b>Symbol only, no lettering.</b> Pick one, or mix two (say the Disc with the Editorial N inside it), '
            'and I\'ll make the full kit the way I did for the Pearl N.')


def page(items, kicker, title, lede=LEDE, extra='', footer=FOOTER):
    cards = ''.join(card(*it) for it in items)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Archivo"; src: url("{FONTS}/archivo-variable.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
@font-face {{ font-family: "Instrument Sans"; src: url("{FONTS}/instrument-sans-400.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Instrument Sans"; src: url("{FONTS}/instrument-sans-600.woff2") format("woff2"); font-weight: 600; }}
@font-face {{ font-family: "Serif Italic"; src: url("fonts/instrument-serif-italic-400.woff2") format("woff2"); }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; background: #EEEAF6; font-family: "Instrument Sans", sans-serif; color: #0B0816; padding: 72px 60px 64px; }}
header {{ margin-bottom: 44px; }}
.kicker {{ font-weight: 600; font-size: 20px; letter-spacing: .18em; text-transform: uppercase; color: #7D18FC; }}
h1 {{ font-family: "Serif Italic", serif; font-weight: 400; font-size: 76px; line-height: 1.02; margin-top: 14px; }}
.lede {{ font-size: 25px; line-height: 1.45; color: #4A4360; margin-top: 16px; max-width: 980px; }}
.card {{ background: #FFFFFF; border-radius: 36px; padding: 40px; margin-bottom: 32px; display: grid;
  grid-template-columns: 380px 1fr; column-gap: 44px; row-gap: 32px; box-shadow: 0 18px 50px rgba(40, 10, 90, .08); }}
.big {{ width: 380px; height: 380px; border-radius: 50%; display: block; }}
.tag {{ display: inline-flex; width: 52px; height: 52px; border-radius: 50%; background: #0B0816; color: #fff; align-items: center;
  justify-content: center; font-family: "Archivo"; font-weight: 800; font-size: 26px; }}
h2 {{ font-family: "Archivo"; font-weight: 800; font-stretch: 108%; font-size: 46px; letter-spacing: -.02em; margin-top: 14px; }}
.idea {{ font-size: 23px; line-height: 1.45; color: #4A4360; margin-top: 10px; }}
.ig {{ display: flex; align-items: center; gap: 18px; margin-top: 26px; padding-top: 24px; border-top: 1px solid #ECE7F5; }}
.ig img {{ border-radius: 50%; display: block; }}
.av110 {{ width: 110px; height: 110px; }}
.av56 {{ width: 56px; height: 56px; margin-left: auto; }}
.av32 {{ width: 32px; height: 32px; }}
.ig b {{ display: block; font-weight: 600; font-size: 24px; }}
.ig span {{ display: block; font-size: 20px; color: #6E6787; margin-top: 4px; }}
.lockup {{ grid-column: 1 / -1; background: #05030C; border-radius: 22px; display: flex; justify-content: center; align-items: center; }}
.lockup img {{ display: block; }}
.alts {{ grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
.alts > div {{ border-radius: 22px; overflow: hidden; display: flex; justify-content: center; }}
.alts img {{ width: 320px; height: 320px; display: block; }}
.ba {{ display: grid; grid-template-columns: 250px 40px 250px 1fr; align-items: center; gap: 24px; background: #fff;
  border-radius: 36px; padding: 36px 40px; margin-bottom: 32px; box-shadow: 0 18px 50px rgba(40, 10, 90, .08); }}
.ba figure {{ margin: 0; text-align: center; }}
.ba img {{ width: 250px; height: 250px; border-radius: 50%; display: block; }}
.ba figcaption {{ font-weight: 600; font-size: 20px; letter-spacing: .14em; text-transform: uppercase; color: #6E6787; margin-top: 14px; }}
.ba .arrow {{ font-size: 40px; color: #7D18FC; text-align: center; }}
.ba ul {{ margin: 0; padding-left: 22px; font-size: 21px; line-height: 1.45; color: #4A4360; }}
.ba li + li {{ margin-top: 8px; }}
footer {{ font-size: 21px; line-height: 1.5; color: #4A4360; margin-top: 12px; }}
footer b {{ color: #0B0816; }}
</style></head><body>
  <header>
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </header>{extra}{cards}
  <footer>{footer}</footer>
</body></html>
'''


def render_sheet(html, png):
    subprocess.run(['node', '-e', f'''
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1200, height: 800 }}, deviceScaleFactor: 1.5 }});
  await p.goto('file://{html}');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({{ path: '{png}', fullPage: true }});
  await b.close();
}})();'''], check=True)


def main(round_):
    for items, out, kicker, title in ROUNDS[round_]:
        args = []
        for slug, *_ in items:
            d = os.path.join(CONCEPTS, slug)
            args += [os.path.join(d, 'profile.svg'), os.path.join(d, 'profile-1080.png'), '1080', '1080', '1']
            if os.path.exists(os.path.join(d, 'lockup.svg')):
                lw, lh = size_of(os.path.join(d, 'lockup.svg'))
                args += [os.path.join(d, 'lockup.svg'), os.path.join(d, 'lockup.png'), str(lw), str(lh), '1.5']
            else:
                for alt in ('alt-light', 'alt-violet'):
                    args += [os.path.join(d, f'{alt}.svg'), os.path.join(d, f'{alt}-1080.png'), '1080', '1080', '1']
        subprocess.run(['node', os.path.join(HERE, 'render.js')] + args, check=True, stdout=subprocess.DEVNULL)
        html = os.path.join(HERE, 'sheet.html')
        with open(html, 'w') as f:
            lede = {'3': LEDE_3, '4': LEDE_4, '5': LEDE_5}.get(round_, LEDE)
            f.write(page(items, kicker, title, lede, BEFORE_AFTER if round_ == '4' else '', FOOTER_5 if round_ == '5' else FOOTER))
        render_sheet(html, os.path.join(ROOT, out))
        print('sheet ->', os.path.join(ROOT, out))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '1')
