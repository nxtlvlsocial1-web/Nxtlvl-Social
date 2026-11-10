"""The Zero Stack cover: a 3D frame of Maya on day 1 (no overlays), the WHAT IF title and the wall of cancellations.

python3 build/cover.py      (from the project root; needs node + the preinstalled Playwright)
Writes renders/nxtlvl_zero-stack_reels_9x16_cover.png (1080x1920).
"""
import base64
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_zero-stack_reels_9x16_cover.png")
PLATE = os.path.join(ROOT, "cover", "plate.png")
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
PLATE_T = T["l"][4] + .9          # "My launch is in 30 days": her hands to her mouth

GRAB = r"""
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [dir, out, t] = process.argv.slice(1);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.wav': 'audio/wav' };
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(() => { window.STACK_COVER = { t: 0 }; });
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.stack, null, { timeout: 120000 });
  await p.evaluate(() => window.__hf.buildReady.stack);
  await p.evaluate((t) => { document.getElementById('ui').style.display = 'none'; document.getElementById('caps').style.display = 'none'; window.STACK_COVER.t = +t; window.STACK_DEBUG.renderAt(+t); }, t);
  await p.screenshot({ path: out });
  await b.close(); srv.close();
});
"""

SHOOT = r"""
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: process.argv[2] }); await b.close(); })();
"""

APPS = [("Adobe Creative Cloud", "#E1251B", "A"), ("Canva Pro", "#00B8C4", "C"), ("Mailchimp", "#F2C11B", "M"), ("ChatGPT Plus", "#10A37F", "C")]


def main():
    os.makedirs(os.path.dirname(PLATE), exist_ok=True); os.makedirs(os.path.dirname(OUT), exist_ok=True)
    subprocess.run(["node", "-e", GRAB, ROOT, PLATE, str(PLATE_T)], check=True)
    img = "data:image/png;base64," + base64.b64encode(open(PLATE, "rb").read()).decode()
    fonts = os.path.join(ROOT, "assets", "fonts")
    notes = "".join(f'<div class="note" style="transform:rotate({r}deg)"><span class="ic" style="background:{c};{"color:#1E1B18;" if c == "#F2C11B" else ""}">{i}</span>'
                    f'<span class="tx"><b>{n}</b><i>Your subscription has been cancelled.</i></span></div>'
                    for (n, c, i), r in zip(APPS, (-2, 1.5, -1, 2)))
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Garamond"; font-weight: 400 800; src: url("file://{fonts}/EBGaramond.ttf"); }}
@font-face {{ font-family: "Manrope"; font-weight: 200 800; src: url("file://{fonts}/manrope.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000 url({img}) center / cover; position: relative; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(5,6,12,.88) 0%, rgba(5,6,12,.55) 24%, rgba(5,6,12,0) 40%, rgba(5,6,12,0) 58%, rgba(5,6,12,.7) 78%, rgba(5,6,12,.92) 100%); }}
.top {{ position: absolute; left: 70px; right: 70px; top: 250px; text-align: center; color: #FFFDF6; text-shadow: 0 4px 24px rgba(0,0,0,.6); }}
.chip {{ display: inline-block; padding: 10px 26px; border-radius: 40px; background: #F2C94C; color: #1E1B18; font: 800 36px/1 "Manrope"; letter-spacing: 6px; text-shadow: none; }}
.l1 {{ display: block; margin-top: 26px; font: 500 78px/1.08 "Garamond"; }}
.l2 {{ display: block; font: 700 128px/1.0 "Garamond"; color: #F2C94C; }}
.l3 {{ display: block; font: 500 78px/1.08 "Garamond"; }}
.notes {{ position: absolute; left: 90px; right: 90px; top: 1270px; }}
.note {{ height: 92px; margin-bottom: 14px; border-radius: 24px; background: rgba(250,250,252,.95); box-shadow: 0 12px 30px rgba(0,0,0,.45);
  display: flex; align-items: center; gap: 20px; padding: 0 24px; }}
.ic {{ width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font: 800 30px/1 "Manrope"; color: #fff; flex: none; }}
.tx b {{ display: block; font: 800 30px/1.1 "Manrope"; color: #14161C; }}
.tx i {{ display: block; font: 600 24px/1.2 "Manrope"; font-style: normal; color: #C0392B; margin-top: 4px; }}
.bill {{ position: absolute; left: 0; right: 0; bottom: 120px; text-align: center; color: #FFFDF6; font: 800 44px/1 "Manrope"; letter-spacing: 2px; text-shadow: 0 3px 16px rgba(0,0,0,.6); }}
.bill s {{ color: #FF8A80; }} .bill b {{ color: #5BE38A; }}
</style></head><body><div class="shade"></div>
<div class="top"><span class="chip">WHAT IF</span><span class="l1">every app you pay for</span><span class="l2">vanished</span><span class="l3">overnight?</span></div>
<div class="notes">{notes}</div>
<div class="bill"><s>$374.86/mo</s> &#8594; <b>$0</b></div>
</body></html>"""
    src = os.path.join(ROOT, "cover", "cover.html")
    open(src, "w").write(doc)
    subprocess.run(["node", "-e", SHOOT, src, OUT], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
