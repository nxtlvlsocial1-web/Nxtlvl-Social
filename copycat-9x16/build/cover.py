"""The Copycat cover: Kane at his desk, the blinds behind him; the WHAT IF title and the three clues.

python3 build/cover.py      (from the project root; needs node + the preinstalled Playwright)
Writes renders/nxtlvl_copycat_reels_9x16_cover.png (1080x1920).
"""
import base64
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_copycat_reels_9x16_cover.png")
PLATE = os.path.join(ROOT, "cover", "plate.png")
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
PLATE_T = T["l"][1] + 1.0           # "Then we watch her": Kane at his desk in the light through the blinds
PLATE_CAM = {"cam": [0.75, 1.32, 0.7], "look": [0, 1.45, -2.0], "fov": 54}   # the board's red string glows behind the title

GRAB = r"""
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dir, out, t, cam] = process.argv.slice(1);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.wav': 'audio/wav' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { window.CC_COVER = { t: 0 }; });
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.copycat, null, { timeout: 120000 });
  await p.evaluate(() => window.__hf.buildReady.copycat);
  await p.evaluate(([t, cam]) => { document.getElementById('ui').style.display = 'none'; document.getElementById('caps').style.display = 'none'; window.CC_COVER = { t: +t, ...JSON.parse(cam) }; window.STACK_DEBUG.renderAt(+t); }, [t, cam]);
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
    tools = "".join(f"<span>{n}</span>" for n in ["changedetection.io", "RSSHub", "Miniflux", "Ollama"])
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Garamond"; font-weight: 400 800; src: url("file://{fonts}/EBGaramond.ttf"); }}
@font-face {{ font-family: "Garamond"; font-style: italic; font-weight: 400 800; src: url("file://{fonts}/EBGaramond-Italic.ttf"); }}
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("file://{fonts}/manrope.ttf"); }}
@font-face {{ font-family: "JBMono"; font-weight: 700; src: url("file://{fonts}/jbmono-bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000 url({img}) center / cover; position: relative; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(4,4,6,.9) 0%, rgba(4,4,6,.7) 22%, rgba(4,4,6,0) 36%, rgba(4,4,6,0) 70%, rgba(4,4,6,.8) 84%, rgba(4,4,6,.95) 100%); }}
.top {{ position: absolute; left: 60px; right: 60px; top: 110px; text-align: center; color: #F4F1EA; text-shadow: 0 4px 24px rgba(0,0,0,.8); }}
.chip {{ display: inline-block; padding: 10px 26px; border: 3px solid #F4F1EA; font: 700 36px/1 "JBMono"; letter-spacing: 8px; }}
.l1 {{ display: block; margin-top: 26px; font: 500 78px/1.06 "Garamond"; }}
.l2 {{ display: block; font: italic 700 126px/1.0 "Garamond"; color: #FFFFFF; }}
.l3 {{ display: block; font: 500 78px/1.06 "Garamond"; }} .l3 b {{ color: #FF3B30; font-weight: 700; }}
.ex {{ position: absolute; left: 70px; right: 70px; bottom: 120px; text-align: center; }}
.ex .st {{ display: inline-block; padding: 8px 18px; border: 4px solid #FF3B30; color: #FF3B30; font: 700 34px/1 "JBMono"; letter-spacing: 6px; transform: rotate(-3deg); }}
.ex .tl {{ margin-top: 26px; display: flex; flex-wrap: wrap; justify-content: center; gap: 12px 14px; }}
.ex .tl span {{ padding: 10px 16px; background: #E4D7B4; color: #1E1B18; font: 700 30px/1 "JBMono"; }}
.ex .ft {{ margin-top: 24px; font: 800 30px/1.2 "Manrope"; letter-spacing: 3px; color: #F4F1EA; }}
</style></head><body><div class="shade"></div>
<div class="top"><span class="chip">WHAT IF</span><span class="l1">you could see</span><span class="l2">every move</span><span class="l3">your <b>competitor</b> makes?</span></div>
<div class="ex"><span class="st">3 CLUES</span><div class="tl">{tools}</div><div class="ft">FREE · OPEN SOURCE · PUBLIC PAGES ONLY</div></div>
</body></html>"""
    src = os.path.join(ROOT, "cover", "cover.html")
    open(src, "w").write(doc)
    subprocess.run(["node", "-e", SHOOT, src, OUT], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
