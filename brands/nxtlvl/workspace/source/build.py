"""Google Workspace logo (Admin console > Account > Personalization): Shooting Star + nxtlvl social wordmark,
transparent PNG at 320 x 132 (Google's size, under 30 KB), light and dark versions, with and without the
"AI-driven creative" tagline.  Run: python3 workspace/source/build.py  (from brands/nxtlvl)
"""
import os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
RENDER = os.path.abspath(os.path.join(KIT, '..', 'nxtlvl-edits', 'source', 'render.js'))

star = open(os.path.join(KIT, 'shooting-star', 'instagram-profile.svg')).read()
paths = re.findall(r'<path[^>]*/>', star[star.find('</defs>'):])            # trail, trail, trail, star
logo = open(os.path.join(KIT, 'logo.svg')).read()
word = re.findall(r'<path d="M[^"]+"[^>]*/>', logo)[-2:]                      # "nxtlvl", "social"
word = [re.sub(r' fill="[^"]*"', '', w) for w in word]

def lockup(ink, soft, mid, low, tag):
    defs = (f'<linearGradient id="t0" gradientUnits="userSpaceOnUse" x1="28.3" y1="171.7" x2="121.6" y2="78.4">'
            f'<stop offset="0" stop-color="{ink}" stop-opacity="0"/><stop offset=".55" stop-color="{ink}" stop-opacity=".9"/><stop offset="1" stop-color="{ink}"/></linearGradient>'
            f'<linearGradient id="t1" gradientUnits="userSpaceOnUse" x1="69.3" y1="164.7" x2="121.6" y2="112.3">'
            f'<stop offset="0" stop-color="{low}" stop-opacity="0"/><stop offset=".55" stop-color="{low}" stop-opacity=".9"/><stop offset="1" stop-color="{low}"/></linearGradient>'
            f'<linearGradient id="t2" gradientUnits="userSpaceOnUse" x1="43.8" y1="122.2" x2="82.0" y2="84.0">'
            f'<stop offset="0" stop-color="{mid}" stop-opacity="0"/><stop offset=".55" stop-color="{mid}" stop-opacity=".9"/><stop offset="1" stop-color="{mid}"/></linearGradient>')
    p = [re.sub(r'fill="[^"]*"', f'fill="url(#t{i})"', paths[i]) for i in range(3)]
    p.append(re.sub(r'fill="[^"]*"', f'fill="{ink}"', paths[3]))
    # mark: 147.8 units -> 100, centred on y 50; wordmark x 121 -> 112, cap band y 28..73 -> centred
    mark = f'<g transform="translate(0 0) scale(0.6766) translate(-20.6 -31.6)">{"".join(p)}</g>'
    wy = 0 if not tag else -12
    words = (f'<g transform="translate(-9 {wy - 0.5})"><g fill="{ink}">{word[0]}</g><g fill="{soft}">{word[1]}</g></g>')
    tagline = ''
    if tag:
        tagline = (f'<text x="113" y="84" font-family="Instrument Sans" font-size="21" letter-spacing="2.2" '
                   f'fill="{soft}">AI-DRIVEN CREATIVE</text>')
    return defs, mark + words + tagline

FONT = os.path.abspath(os.path.join(KIT, '..', '..', 'website', 'fonts'))
def page(defs, body):
    face = ''
    for f in sorted(os.listdir(FONT)) if os.path.isdir(FONT) else []:
        if f.startswith('instrument-sans') and ('500' in f or '400' in f) and f.endswith('.woff2'):
            face = f'@font-face{{font-family:"Instrument Sans";src:url("file://{FONT}/{f}")}}'; break
    # 410 x 100 artwork fitted inside 320 x 132 with a small margin
    return (f'<!doctype html><html><head><style>{face}html,body{{margin:0;background:transparent}}'
            f'svg{{display:block}}</style></head><body><svg xmlns="http://www.w3.org/2000/svg" width="320" height="132" '
            f'viewBox="-8 -16 426 132"><defs>{defs}</defs>{body}</svg></body></html>')

VARIANTS = {   # name: ink, soft, mid trail, low trail, tagline
    'workspace-logo-light': ('#0B0816', '#6B6391', '#7D18FC', '#A95CFF', False),
    'workspace-logo-light-tagline': ('#0B0816', '#6B6391', '#7D18FC', '#A95CFF', True),
    'workspace-logo-dark': ('#FFFFFF', '#D8BBFF', '#B98AFF', '#A95CFF', False),
    'workspace-logo-dark-tagline': ('#FFFFFF', '#D8BBFF', '#B98AFF', '#A95CFF', True),
}
args = []
for name, v in VARIANTS.items():
    h = os.path.join(HERE, name + '.html')
    open(h, 'w').write(page(*lockup(*v)))
    args += [h, os.path.join(OUT, name + '.png'), '320', '132', '1']
subprocess.run(['node', RENDER, *args], check=True)
for name in VARIANTS:   # quantise to stay well under Google's 30 KB
    png = os.path.join(OUT, name + '.png')
    subprocess.run(['python3', '-c', f'from PIL import Image; im=Image.open("{png}"); im.quantize(colors=128, method=Image.Quantize.FASTOCTREE).save("{png}", optimize=True)'], check=True)
    print(name, os.path.getsize(png), 'bytes')
