"""The Autopilot cover: Rosa waking at dawn with the six neon tools behind her, the WHAT IF title and the night's tally.

python3 build/cover.py      (from the project root; needs node + the preinstalled Playwright)
Writes renders/nxtlvl_autopilot_reels_9x16_cover.png (1080x1920).
"""
import base64
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_autopilot_reels_9x16_cover.png")
PLATE = os.path.join(ROOT, "cover", "plate.png")
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
PLATE_T = T["l"][2] + .75         # "Wait... who answered all of these?": her face, the signs still lit

GRAB = r"""
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dir, out, t] = process.argv.slice(1);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.wav': 'audio/wav' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { window.AP_COVER = { t: 0 }; });
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.autopilot, null, { timeout: 120000 });
  await p.evaluate(() => window.__hf.buildReady.autopilot);
  await p.evaluate((t) => { document.getElementById('ui').style.display = 'none'; document.getElementById('caps').style.display = 'none'; window.AP_COVER = { t: +t }; window.STACK_DEBUG.renderAt(+t); }, t);
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
    subprocess.run(["node", "-e", GRAB, ROOT, PLATE, str(PLATE_T)], check=True)
    img = "data:image/png;base64," + base64.b64encode(open(PLATE, "rb").read()).decode()
    fonts = os.path.join(ROOT, "assets", "fonts")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Garamond"; font-weight: 400 800; src: url("file://{fonts}/EBGaramond.ttf"); }}
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("file://{fonts}/manrope.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000 url({img}) center / cover; position: relative; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(5,6,12,.8) 0%, rgba(5,6,12,.55) 25%, rgba(5,6,12,0) 40%, rgba(5,6,12,0) 66%, rgba(5,6,12,.72) 82%, rgba(5,6,12,.92) 100%); }}
.top {{ position: absolute; left: 60px; right: 60px; top: 105px; text-align: center; color: #FFFDF6; text-shadow: 0 4px 24px rgba(0,0,0,.75); }}
.chip {{ display: inline-block; padding: 10px 26px; border-radius: 40px; background: #F2C94C; color: #1E1B18; font: 800 36px/1 "Manrope"; letter-spacing: 6px; text-shadow: none; }}
.l1 {{ display: block; margin-top: 24px; font: 500 76px/1.06 "Garamond"; }}
.l2 {{ display: block; font: 700 124px/1.0 "Garamond"; color: #F2C94C; }}
.l3 {{ display: block; font: 500 76px/1.06 "Garamond"; }}
.clock {{ position: absolute; left: 0; right: 0; bottom: 300px; text-align: center; font: 800 34px/1 "Manrope"; letter-spacing: 5px; color: #C9C3FF; text-shadow: 0 3px 14px rgba(0,0,0,.8); }}
.tally {{ position: absolute; left: 90px; right: 90px; bottom: 120px; display: flex; justify-content: space-between; align-items: flex-end; color: #FFFDF6; text-shadow: 0 3px 16px rgba(0,0,0,.7); }}
.tally div {{ text-align: center; flex: 1; }}
.tally b {{ display: block; font: 800 84px/1 "Manrope"; }}
.tally small {{ display: block; margin-top: 10px; font: 800 24px/1 "Manrope"; letter-spacing: 4px; color: #D8D4E8; }}
.tally .g b {{ color: #5BE38A; }}
</style></head><body><div class="shade"></div>
<div class="top"><span class="chip">WHAT IF</span><span class="l1">your marketing</span><span class="l2">ran itself</span><span class="l3">while you slept?</span></div>
<div class="clock">11:04 PM &#8594; 6:58 AM</div>
<div class="tally"><div><b>1,147</b><small>HANDLED</small></div><div><b>63</b><small>BOOKINGS</small></div><div class="g"><b>$0</b><small>IN SOFTWARE</small></div></div>
</body></html>"""
    src = os.path.join(ROOT, "cover", "cover.html")
    open(src, "w").write(doc)
    subprocess.run(["node", "-e", SHOOT, src, OUT], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
