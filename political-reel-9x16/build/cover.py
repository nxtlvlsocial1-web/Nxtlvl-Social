"""Cover for the Diwali opinion reel, 9:16 (1080x1920): renders/cover.html, then a screenshot to
renders/nxtlvl_diwali-opinion_cover_9x16.jpg. Everything that matters sits inside the 3:4 grid crop (y 240-1680),
which also keeps it clear of the Reels top bar and caption area.
Layout after the owner's reference (a red sheet with the minister's quote, the key words on black tape) in the reel's
paper-collage style: the quote on torn red paper with his black-and-white print, then her photo print and the title.
python3 build/cover.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUOTE = ('दिवाली के मौके पर कुछ भी खरीदना हो तो <b>जय श्री राम</b> वाले से ही खरीदना है, उसके <b>माथे पर टीका</b> '
         'लगा होना चाहिए या उसको <b>हनुमान चालीसा</b> आनी चाहिए')

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Mukta"; font-weight: 800; src: url("../assets/fonts/Mukta-800-devanagari.woff2"); }}
@font-face {{ font-family: "Anton"; src: url("../assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("../assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #efebe4; position: relative; font-family: "Inter"; }}
#paper {{ position: absolute; inset: -300px; background: url(../assets/img/paper/paper.png) 0 0 / 1700px auto; filter: sepia(.06) saturate(.8) brightness(1.06); }}
#grid {{ position: absolute; inset: 0; opacity: .55; background-image: linear-gradient(rgba(70,90,130,.22) 1.5px, transparent 1.5px),
  linear-gradient(90deg, rgba(70,90,130,.22) 1.5px, transparent 1.5px); background-size: 72px 72px; }}
.scrap {{ position: absolute; filter: drop-shadow(0 14px 18px rgba(0,0,0,.3)); }}
#quote {{ position: absolute; left: 92px; top: 440px; width: 640px; color: #fff; font: 800 64px/1.22 "Mukta"; text-shadow: 0 3px 10px rgba(0,0,0,.25); }}
#quote b {{ font-weight: 800; background: #111; padding: 0 .14em; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}
#qm {{ position: absolute; left: 88px; top: 352px; font: 800 180px/1 "Mukta"; color: #fff; opacity: .9; }}
#by {{ position: absolute; left: 110px; top: 945px; font: 800 44px/1 "Mukta"; color: #fff; font-style: italic; opacity: .95; }}
.print {{ position: absolute; background: #f6f3ec; padding: 14px 14px 44px; box-shadow: 0 18px 34px rgba(0,0,0,.35); }}
.print img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.bw img {{ filter: grayscale(1) contrast(1.25) brightness(1.05); }}
.tape {{ position: absolute; left: 50%; top: -22px; width: 170px; height: 46px; margin-left: -85px; background: rgba(238,228,196,.8); transform: rotate(-3deg); }}
.ring {{ position: absolute; fill: none; stroke: #e3202f; stroke-width: 8; stroke-linecap: round; }}
.lab {{ position: absolute; font-family: "Anton"; line-height: 1; padding: .08em .2em .1em; white-space: nowrap; box-shadow: 0 10px 18px rgba(0,0,0,.25); }}
.black {{ background: #111; color: #fff; }}
.red {{ background: #e3202f; color: #fff; }}
.white {{ background: #fbf9f4; color: #111; }}
.diya {{ position: absolute; }}
#title {{ position: absolute; left: 0; width: 1080px; top: 1060px; text-align: center; }}
#title > div {{ margin-bottom: 12px; }}
#title .lab {{ position: relative; display: inline-block; }}
.star {{ position: absolute; }}
</style></head><body>
<div id="paper"></div><div id="grid"></div>
<img class="scrap" src="../assets/img/paper/scrap/red-1.png" style="left:-260px;top:210px;width:1480px;height:875px;object-fit:fill;transform:rotate(-2deg)">
<div id="qm">&ldquo;</div>
<div id="quote">{QUOTE}</div>
<div id="by">&mdash; नितेश राणे</div>
<div class="print bw" style="left:752px;top:560px;width:270px;height:320px;transform:rotate(5deg)"><img src="../assets/img/ref/speaker_face.jpg"><i class="tape"></i></div>
<svg class="ring" viewBox="0 0 300 230" style="left:720px;top:520px;width:340px;height:370px"><path d="M 150 14 C 250 10 300 62 296 116 C 292 180 222 222 146 220 C 62 218 6 172 8 112 C 10 50 70 12 160 14 C 222 16 266 36 286 64"/></svg>
<div id="title">
  <div><span class="lab black" style="font-size:150px;transform:rotate(-3deg)">DIWALI</span></div>
  <div><span class="lab white" style="font-size:96px;transform:rotate(2deg)">BRINGS ALL</span></div>
  <div><span class="lab black" style="font-size:114px;transform:rotate(-2deg)">RELIGIONS</span></div>
  <div><span class="lab red" style="font-size:128px;transform:rotate(1.5deg)">TOGETHER</span></div>
</div>
{"".join(f'<svg class="diya" viewBox="0 0 160 130" style="left:{x}px;top:{y}px;width:{w}px"><ellipse cx="80" cy="52" rx="44" ry="44" fill="rgba(255,190,80,.5)"/><path d="M 8 78 C 24 124 136 124 152 78 C 120 92 40 92 8 78 Z" fill="#b8521f"/><path d="M 8 78 C 40 92 120 92 152 78" fill="none" stroke="#e2a33a" stroke-width="6"/><path d="M 80 80 C 58 62 68 34 80 12 C 92 34 102 62 80 80 Z" fill="#ff9a1a"/><path d="M 80 78 C 70 66 74 50 80 38 C 86 50 90 66 80 78 Z" fill="#fff1a8"/></svg>' for x, y, w in [(90, 1380, 140), (850, 1390, 140)])}
{"".join(f'<svg class="star" viewBox="-50 -50 100 100" style="left:{x}px;top:{y}px;width:{s}px"><path d="M0 -48 C6 -8 8 -6 48 0 C8 6 6 8 0 48 C-6 8 -8 6 -48 0 C-8 -6 -6 -8 0 -48 Z" fill="{c}"/></svg>' for x, y, s, c in [(930, 1060, 56, "#d9a520"), (120, 1100, 44, "#e3202f"), (900, 1330, 36, "#111"), (130, 1380, 40, "#d9a520"), (990, 1560, 34, "#e3202f")])}
</body></html>"""


SHOT = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1080, height: 1920}, deviceScaleFactor: 1});
  await p.goto('file://' + process.argv[1]); await p.waitForTimeout(1500);
  await p.screenshot({path: process.argv[2]}); await b.close();
})();
"""


def main():
    import subprocess
    from PIL import Image
    out = os.path.join(ROOT, "renders")
    os.makedirs(out, exist_ok=True)
    page_path = os.path.join(out, "cover.html")
    open(page_path, "w", encoding="utf-8").write(HTML)
    png = os.path.join(out, "nxtlvl_diwali-opinion_cover_9x16.png")
    subprocess.run(["node", "-e", SHOT, page_path, png], check=True)     # Node's Playwright (the pre-installed browser)
    Image.open(png).convert("RGB").save(png[:-4] + ".jpg", quality=94)
    print("cover written:", png[:-4] + ".jpg")


main()
