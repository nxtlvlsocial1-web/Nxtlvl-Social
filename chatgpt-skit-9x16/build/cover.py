"""The skit cover: Marcus grinning at his desk with Byte beside him, the comment-style hook on top and the promise below.

python3 build/cover.py      (from the project root; needs node + the preinstalled Playwright)
Writes renders/nxtlvl_chatgpt-skit_reels_9x16_cover.png (1080x1920).
"""
import base64
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_chatgpt-skit_reels_9x16_cover.png")
PLATE = os.path.join(ROOT, "cover", "plate.png")
PLATE_T = 52.0                      # "you just saved me a fortune": Marcus grinning, Byte smug
PLATE_CAM = {"cam": [0.4, 1.85, 3.25], "look": [0.38, 1.62, -0.5], "fov": 50}

GRAB = r"""
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dir, out, t, cam] = process.argv.slice(1);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.wav': 'audio/wav' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { window.SK_COVER = { t: 0 }; });
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.skit, null, { timeout: 120000 });
  await p.evaluate(() => window.__hf.buildReady.skit);
  await p.evaluate(([t, cam]) => { for (const id of ['ui', 'caps', 'cms', 'panel', 'end', 'endc']) { const e = document.getElementById(id); if (e) e.style.display = 'none'; } window.SK_COVER = { t: +t, ...JSON.parse(cam) }; window.STACK_DEBUG.renderAt(+t); }, [t, cam]);
  await p.screenshot({ path: out });
  await b.close(); srv.close();
});
"""

SHOOT = r"""
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: process.argv[2] }); await b.close(); })();
"""


def main():
    os.makedirs(os.path.dirname(PLATE), exist_ok=True); os.makedirs(os.path.dirname(OUT), exist_ok=True)
    subprocess.run(["node", "-e", GRAB, ROOT, PLATE, str(PLATE_T), json.dumps(PLATE_CAM)], check=True)
    img = "data:image/png;base64," + base64.b64encode(open(PLATE, "rb").read()).decode()
    fonts = os.path.join(ROOT, "assets", "fonts")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Garamond"; font-weight: 400 800; src: url("file://{fonts}/EBGaramond.ttf"); }}
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("file://{fonts}/manrope.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000 url({img}) center / cover; position: relative; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(5,8,16,.82) 0%, rgba(5,8,16,.55) 24%, rgba(5,8,16,0) 38%, rgba(5,8,16,0) 70%, rgba(5,8,16,.75) 85%, rgba(5,8,16,.92) 100%); }}
.top {{ position: absolute; left: 60px; right: 60px; top: 150px; text-align: center; color: #FFFDF6; text-shadow: 0 4px 24px rgba(0,0,0,.7); }}
.chip {{ display: inline-block; padding: 10px 26px; border-radius: 40px; background: #F2C94C; color: #1E1B18; font: 800 36px/1 "Manrope"; letter-spacing: 6px; text-shadow: none; }}
.l1, .l3 {{ display: block; margin-top: 18px; font: 500 76px/1.06 "Garamond"; }} .l3 {{ margin-top: 0; }}
.l2 {{ display: block; font: 700 118px/1.0 "Garamond"; color: #F2C94C; }}
.bot {{ position: absolute; left: 60px; right: 60px; bottom: 130px; text-align: center; color: #FFFDF6; text-shadow: 0 3px 16px rgba(0,0,0,.7); }}
.bot b {{ display: block; font: 800 54px/1.2 "Manrope"; }} .bot span {{ display: block; margin-top: 14px; font: 800 30px/1 "Manrope"; letter-spacing: 5px; color: #F2C94C; }}
</style></head><body><div class="shade"></div>
<div class="top"><span class="chip">FREE · 4 STEPS</span><span class="l1">ChatGPT keeps</span><span class="l2">recommending</span><span class="l3">your competitor?</span></div>
<div class="bot"><b>Here's how to claim your business</b><span>REAL ESTATE · NEW FEATURE</span></div>
</body></html>"""
    src = os.path.join(ROOT, "cover", "cover.html")
    open(src, "w").write(doc)
    subprocess.run(["node", "-e", SHOOT, src, OUT], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
