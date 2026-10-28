"""The Reel's cover: writes cover.html and screenshots it to renders/nxtlvl_haunted-db_reels_9x16_v1_cover.png.

python3 build/cover.py [out.png]      (from the project root, after build/generate.py; needs node + Playwright)

A still of the 3D world just after Enter: the haunted house at night, the sheet ghost drifting past its top-floor
windows as they go dark, under the ai.nxtlvl explainer type: the story in one line (he deleted production) and the
promise below (the setup that saved him, three steps). Everything that matters sits inside the middle 1080x1440,
the 3:4 crop the profile grid shows.
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
OUT = os.path.join(ROOT, "renders", "nxtlvl_haunted-db_reels_9x16_v1_cover.png")
COVER = {"t": round(T["press"] + 1.0, 3), "cam": [0, 3.6, 15.5], "look": [0, 7.4, 0], "fov": 50}

CSS = """
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "ISerif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #070a14; font-family: "Manrope", sans-serif; color: #F1E9DC; }
#gl { position: absolute; inset: 0; width: 1080px; height: 1920px; display: block; }
.st { position: absolute; left: 0; right: 0; top: 0; height: 760px; background: linear-gradient(180deg, rgba(5,6,12,.94) 0%, rgba(5,6,12,.78) 55%, rgba(5,6,12,0) 100%); }
.sb { position: absolute; left: 0; right: 0; bottom: 0; height: 820px; background: linear-gradient(0deg, rgba(5,6,12,.95) 0%, rgba(5,6,12,.8) 50%, rgba(5,6,12,0) 100%); }
.top { position: absolute; left: 70px; right: 70px; top: 262px; display: flex; align-items: center; gap: 14px; font: 700 30px "JBMono"; letter-spacing: 4px; }
.top i { width: 18px; height: 18px; border-radius: 50%; background: #E8735A; box-shadow: 0 0 14px #E8735A; }
.hl { position: absolute; left: 70px; right: 70px; top: 330px; }
.k { font: 700 34px "JBMono"; letter-spacing: 6px; color: #FF9A7F; }
.l1 { margin-top: 12px; font: 800 96px/1.02 "Manrope"; letter-spacing: -3.5px; }
.l2 { font: 400 168px/1 "ISerif"; font-style: italic; color: #FF8A6E; letter-spacing: -2px; }
.foot { position: absolute; left: 70px; right: 70px; top: 1290px; }
.card { display: inline-flex; align-items: center; gap: 22px; padding: 22px 30px; border-radius: 26px; background: #FFFDF8; color: #1E1B18;
  box-shadow: 0 24px 60px rgba(0,0,0,.6); font: 800 46px/1.15 "Manrope"; letter-spacing: -1px; }
.card b { font-family: "ISerif"; font-style: italic; font-weight: 400; color: #D45C40; font-size: 58px; }
.steps { margin-top: 26px; display: flex; gap: 14px; }
.steps span { padding: 12px 20px; border-radius: 30px; background: rgba(241,233,220,.14); border: 2px solid rgba(241,233,220,.35); font: 700 28px "JBMono"; letter-spacing: 1px; }
.steps span:first-child { background: #D45C40; border-color: #D45C40; color: #fff; }
"""

HTML = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Haunted database explainer cover</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <canvas id="gl"></canvas>
    <div class="st"></div><div class="sb"></div>
    <div class="top"><i></i>AI.NXTLVL</div>
    <div class="hl"><div class="k">03:07 AM</div><div class="l1">He deleted</div><div class="l2">production.</div></div>
    <div class="foot"><div class="card">The setup that <b>saved him</b></div>
      <div class="steps"><span>1 SNAPSHOT</span><span>2 BLOCK PROD</span><span>3 BACKUP ALARM</span></div></div>
    <script>
      window.HH_T = {json.dumps(T)};
      window.HH_COVER = {json.dumps(COVER)};
    </script>
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
  await p.waitForFunction(() => window.__coverDone === true, null, { timeout: 180000 });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: process.argv[2] });
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""


def main():
    open(os.path.join(ROOT, "cover.html"), "w", encoding="utf-8").write(HTML)
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    os.makedirs(os.path.dirname(out), exist_ok=True)
    srv = subprocess.Popen(["python3", "-m", "http.server", "8767", "--bind", "127.0.0.1"], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1)
        subprocess.run(["node", "-e", SHOT, "http://127.0.0.1:8767/cover.html", out], check=True)
    finally:
        srv.terminate()
    print("wrote", out)


if __name__ == "__main__":
    main()
