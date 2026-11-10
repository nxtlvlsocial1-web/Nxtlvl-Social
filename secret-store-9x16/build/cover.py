"""The Secret Free Store cover: a 3D frame of the vault (no overlays) with the title, the swap list teaser and the CTA.

python3 build/cover.py      (from the project root; needs node + the preinstalled Playwright)
Writes renders/nxtlvl_secret-store_reels_9x16_cover.png (1080x1920). Keep the title inside the middle 3:4 (the grid crop).
"""
import base64
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_secret-store_reels_9x16_cover.png")
PLATE = os.path.join(ROOT, "cover", "plate.png")
K = json.load(open(os.path.join(ROOT, "build", "cues.json")))["k"]
PLATE_T = K["openG"] + 1.1          # the legendary chest open, coins in the air, the bot dancing

GRAB = r"""
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dir, out, t] = process.argv.slice(1);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.wav': 'audio/wav', '.png': 'image/png', '.webp': 'image/webp' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { window.STORE_COVER = { t: 0 }; });
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.store, null, { timeout: 180000 });
  await p.evaluate(() => window.__hf.buildReady.store);
  await p.evaluate((t) => { document.getElementById('ui').style.display = 'none'; document.getElementById('caps').style.display = 'none'; window.STORE_COVER.t = +t; window.STORE_DEBUG.renderAt(+t); }, t);
  await p.screenshot({ path: out });
  await b.close(); srv.close();
});
"""

SHOOT = r"""
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300); await p.screenshot({ path: process.argv[2] }); await b.close(); })();
"""


def main():
    os.makedirs(os.path.dirname(PLATE), exist_ok=True); os.makedirs(os.path.dirname(OUT), exist_ok=True)
    subprocess.run(["node", "-e", GRAB, ROOT, PLATE, str(PLATE_T)], check=True)
    img = "data:image/png;base64," + base64.b64encode(open(PLATE, "rb").read()).decode()
    fonts = os.path.join(ROOT, "assets", "fonts")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("file://{fonts}/manrope.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 700; src: url("file://{fonts}/jbmono-bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000 url({img}) center / cover; position: relative; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(8,6,4,.9) 0%, rgba(8,6,4,.72) 30%, rgba(8,6,4,0) 50%, rgba(8,6,4,0) 70%, rgba(8,6,4,.8) 90%); }}
.top {{ position: absolute; left: 60px; right: 60px; top: 300px; text-align: center; color: #FFFFFF; }}
.chip {{ display: inline-block; padding: 10px 24px; border-radius: 30px; background: #0E1220; color: #6FF7FF; font: 700 34px/1 "JBMono"; letter-spacing: 6px; border: 3px solid #45F3FF; }}
.l1 {{ display: block; margin-top: 26px; font: 800 92px/1 "Manrope"; text-shadow: 0 6px 30px rgba(0,0,0,.6); }}
.l2 {{ display: block; font: 800 150px/1.02 "Manrope"; letter-spacing: -3px; color: #FFB08F; -webkit-text-stroke: 5px #0E1220; paint-order: stroke fill; }}
.l3 {{ display: inline-block; margin-top: 22px; padding: 12px 28px; border-radius: 20px; background: rgba(14,18,32,.88); font: 800 52px/1.1 "Manrope"; }}
.l3 b {{ color: #FFD966; }}
.bot {{ position: absolute; left: 0; right: 0; bottom: 430px; text-align: center; }}
.bot span {{ display: inline-block; padding: 14px 32px; border-radius: 22px; background: linear-gradient(180deg, #FFE08A, #F2A93B); color: #2A1500; font: 800 56px/1 "Manrope"; letter-spacing: 3px; box-shadow: 0 0 50px rgba(255,194,51,.7); }}
</style></head><body><div class="shade"></div>
<div class="top"><span class="chip">PART 2</span><span class="l1">THE SECRET</span><span class="l2">FREE STORE</span><span class="l3"><b>9 free repos</b> hiding on GitHub</span></div>
<div class="bot"><span>COMMENT "REPO"</span></div>
</body></html>"""
    src = os.path.join(ROOT, "cover", "cover.html")
    open(src, "w").write(doc)
    subprocess.run(["node", "-e", SHOOT, src, OUT], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
