"""The Creedom cover: Cree in his hero landing beside the stunned creator, the wish hook on top and the payoff below.

python3 build/cover.py      (from the project root; needs node + the preinstalled Playwright)
Writes renders/nxtlvl_creedom-i-wish_reels_9x16_cover.png (1080x1920).
"""
import base64
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_creedom-i-wish_reels_9x16_cover.png")
PLATE = os.path.join(ROOT, "cover", "plate.png")
import sys
PLATE_T = float(sys.argv[1]) if len(sys.argv) > 1 else 30.9   # the superhero landing (dust settled): Cree on the desk, moon in the window
PLATE_CAM = {}

GRAB = r"""
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dir, out, t, cam] = process.argv.slice(1);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json', '.mjs': 'text/javascript' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { window.CR_COVER = { t: 0 }; });
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.cree, null, { timeout: 120000 });
  await p.evaluate(() => window.__hf.buildReady.cree);
  await p.evaluate(([t, cam]) => { for (const id of ['ui', 'caps', 'endc', 'kw', 'tg1', 'tg2', 'tg3', 'k1', 'k2', 'k3', 'k4', 'k5']) { const e = document.getElementById(id); if (e) e.style.display = 'none'; } window.CR_COVER = { t: +t, ...JSON.parse(cam) }; window.STACK_DEBUG.renderAt(+t); }, [t, cam]);
  await p.screenshot({ path: out });
  await b.close(); srv.close();
});
"""

SHOOT = r"""
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: process.argv[2] }); await b.close(); })();
"""


def plate(t, out):
    subprocess.run(["node", "-e", GRAB, ROOT, out, str(t), json.dumps(PLATE_CAM)], check=True)


def main():
    os.makedirs(os.path.dirname(PLATE), exist_ok=True); os.makedirs(os.path.dirname(OUT), exist_ok=True)
    subprocess.run(["node", "-e", GRAB, ROOT, PLATE, str(PLATE_T), json.dumps(PLATE_CAM)], check=True)
    img = "data:image/png;base64," + base64.b64encode(open(PLATE, "rb").read()).decode()
    fonts = os.path.join(ROOT, "assets", "fonts")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "GSans"; font-weight: 400 800; src: url("file://{fonts}/googlesans.ttf"); }}
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("file://{fonts}/manrope.ttf"); }}
@font-face {{ font-family: "Fraunces"; font-style: italic; font-weight: 400 900; src: url("file://{fonts}/fraunces-italic.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000 url({img}) center / cover; position: relative; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,6,30,.80) 0%, rgba(10,6,30,.62) 22%, rgba(10,6,30,.10) 40%, rgba(10,6,30,0) 60%, rgba(10,6,30,.55) 74%, rgba(10,6,30,.88) 88%, rgba(10,6,30,.95) 100%); }}
.top {{ position: absolute; left: 60px; right: 60px; top: 270px; text-align: center; color: #FFFFFF; text-shadow: 0 6px 30px rgba(0,0,0,.65); }}
.chip {{ display: inline-block; padding: 12px 30px; border-radius: 44px; background: #FF2E93; color: #FFFFFF; font: 800 34px/1 "Manrope"; letter-spacing: 7px; text-shadow: none; box-shadow: 0 8px 30px rgba(255,46,147,.45); }}
.l1 {{ display: block; margin-top: 30px; font: 700 112px/1.0 "GSans"; letter-spacing: -2px; }}
.l1 b {{ color: #FFD84D; }}
.l2 {{ display: block; margin-top: 8px; font: italic 800 128px/1.02 "Fraunces"; color: #FF5BAE; text-shadow: 0 6px 34px rgba(255,46,147,.55), 0 4px 18px rgba(0,0,0,.6); }}
.bot {{ position: absolute; left: 70px; right: 70px; top: 1385px; text-align: center; color: #FFFFFF; text-shadow: 0 4px 18px rgba(0,0,0,.75); }}
.bot b {{ display: block; font: 700 56px/1.15 "GSans"; }}
.bot span {{ display: block; margin-top: 18px; font: 800 28px/1 "Manrope"; letter-spacing: 6px; color: #FFD84D; }}
</style></head><body><div class="shade"></div>
<div class="top"><span class="chip">3 WISHES</span><span class="l1"><b>42</b> views?</span><span class="l2">Make a wish.</span></div>
<div class="bot"><b>Then he flew in and fixed everything</b><span>REELS · VIEWS · DM AUTOMATION</span></div>
</body></html>"""
    src = os.path.join(ROOT, "cover", "cover.html")
    open(src, "w").write(doc)
    subprocess.run(["node", "-e", SHOOT, src, OUT], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
