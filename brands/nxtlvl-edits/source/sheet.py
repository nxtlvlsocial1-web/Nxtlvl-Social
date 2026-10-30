"""Renders every concept to PNG and lays them out on one comparison sheet (../concepts-preview.png).

Run after build.py:  python3 sheet.py
"""
import os
import re
import subprocess

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


def size_of(svg_path):
    m = re.search(r'width="(\d+)" height="(\d+)"', open(svg_path).read())
    return int(m.group(1)), int(m.group(2))


def card(slug, letter, name, idea):
    lw, lh = size_of(os.path.join(CONCEPTS, slug, 'lockup.svg'))
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
    <div class="lockup"><img src="../concepts/{slug}/lockup.svg" style="width:{lw / 1382 * 100:.2f}%;aspect-ratio:{lw}/{lh}" alt=""></div>
  </section>'''


def page():
    cards = ''.join(card(*it) for it in ITEMS)
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
footer {{ font-size: 21px; line-height: 1.5; color: #4A4360; margin-top: 12px; }}
footer b {{ color: #0B0816; }}
</style></head><body>
  <header>
    <p class="kicker">nxtlvl edits · logo concepts</p>
    <h1>Four directions for the edits account</h1>
    <p class="lede">Each one is from the Nxtlvl Social family (the star, the N, the wordmark, the violet), with an editor's cut.
    Shown as the Instagram profile picture at full size and at the sizes people actually see it.</p>
  </header>{cards}
  <footer><b>Every concept uses the same wordmark:</b> "nxtlvl" in the original logo lettering, then "edits" in Instrument Serif
  Italic with the star over the i. Pick one (or mix, e.g. A's star with D's wordmark) and I'll make the full kit.</footer>
</body></html>
'''


def main():
    html = os.path.join(HERE, 'sheet.html')
    with open(html, 'w') as f:
        f.write(page())
    args = []
    for slug, *_ in ITEMS:
        d = os.path.join(CONCEPTS, slug)
        args += [os.path.join(d, 'profile.svg'), os.path.join(d, 'profile-1080.png'), '1080', '1080', '1']
        lw, lh = size_of(os.path.join(d, 'lockup.svg'))
        args += [os.path.join(d, 'lockup.svg'), os.path.join(d, 'lockup.png'), str(lw), str(lh), '1.5']
    subprocess.run(['node', os.path.join(HERE, 'render.js')] + args, check=True)
    # full-page sheet: measure the height first
    subprocess.run(['node', '-e', f'''
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1200, height: 800 }}, deviceScaleFactor: 1.5 }});
  await p.goto('file://{html}');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({{ path: '{os.path.join(ROOT, "concepts-preview.png")}', fullPage: true }});
  await b.close();
}})();'''], check=True)
    print('sheet ->', os.path.join(ROOT, 'concepts-preview.png'))


if __name__ == '__main__':
    main()
