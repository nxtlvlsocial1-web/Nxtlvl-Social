"""The Reel's cover: writes cover.html and screenshots it to renders/nxtlvl_hallmark-noir_reels_9x16_v1_cover.png.

python3 build/cover.py [out.png]      (from the project root, after build/generate.py; needs node + Playwright)

A still of the 3D world (the opening frame: the detective under his fedora, rain on the window, the violet
NXTLVLSOCIAL.AI neon) under the case-file headline: why every AI website looks the same, and the fix below it.
Everything that matters sits inside the middle 1080x1440, the 3:4 crop the profile grid shows.
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
T.pop("ev", None)
OUT = os.path.join(ROOT, "renders", "nxtlvl_hallmark-noir_reels_9x16_v1_cover.png")
AT = 0.9

CSS = """
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "ISerif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #050608; font-family: "Montserrat", sans-serif; color: #F4F1EA; }
#gl { position: absolute; inset: 0; width: 1080px; height: 1920px; display: block; }
.st { position: absolute; left: 0; right: 0; top: 0; height: 820px; background: linear-gradient(180deg, rgba(4,5,7,.95) 0%, rgba(4,5,7,.82) 55%, rgba(4,5,7,0) 100%); }
.sb { position: absolute; left: 0; right: 0; bottom: 0; height: 760px; background: linear-gradient(0deg, rgba(4,5,7,.96) 0%, rgba(4,5,7,.82) 50%, rgba(4,5,7,0) 100%); }
.k { position: absolute; left: 80px; top: 285px; font: 700 32px "JBMono"; letter-spacing: 8px; color: #B687F9; }
.h { position: absolute; left: 80px; right: 80px; top: 345px; font: 800 104px/1.0 "Montserrat"; letter-spacing: -3.5px; }
.h em { display: block; font: 400 140px/1 "ISerif"; font-style: italic; letter-spacing: -1px; color: #C7A2FF; text-shadow: 0 0 40px rgba(167,91,252,.55); }
.foot { position: absolute; left: 80px; right: 80px; top: 1330px; }
.card { display: inline-block; padding: 22px 30px; border-radius: 22px; background: #F4F1EA; color: #111; font: 800 46px/1.15 "Montserrat"; letter-spacing: -1px; box-shadow: 0 24px 60px rgba(0,0,0,.6); }
.card b { font-family: "ISerif"; font-style: italic; font-weight: 400; font-size: 58px; color: #6a2bd0; }
.sub { margin-top: 22px; font: 700 30px "JBMono"; letter-spacing: 3px; color: #d8d2c4; }
"""

HTML = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Hallmark noir cover</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <canvas id="gl"></canvas>
    <div class="st"></div><div class="sb"></div>
    <div class="k">CASE FILE No. 047</div>
    <div class="h">Why every AI website looks <em>the same.</em></div>
    <div class="foot"><div class="card">The fix: <b>Hallmark</b></div><div class="sub">A FREE CLAUDE CODE SKILL</div></div>
    <script>window.NOIR_T = {json.dumps(T)};</script>
    <script type="module" src="assets/js/world.js"></script>
  </body>
</html>
"""

SHOT = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', (e) => console.error('pageerror', e.message));
  await p.goto(process.argv[1], { waitUntil: 'load' });
  await p.waitForFunction(() => window.__done === true, null, { timeout: 240000 });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: process.argv[2] });
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""


def main():
    open(os.path.join(ROOT, "cover.html"), "w", encoding="utf-8").write(HTML)
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    os.makedirs(os.path.dirname(out), exist_ok=True)
    srv = subprocess.Popen(["python3", "-m", "http.server", "8768", "--bind", "127.0.0.1"], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1)
        subprocess.run(["node", "-e", SHOT, f"http://127.0.0.1:8768/cover.html?t={AT}", out], check=True)
    finally:
        srv.terminate()
    print("wrote", out)


if __name__ == "__main__":
    main()
