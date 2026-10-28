"""The Reel's cover: writes cover.html and screenshots it to renders/nxtlvl_horror-db_reels_9x16_v1_cover.png.

python3 build/cover.py      (from the project root, after build/generate.py; needs node + the preinstalled Playwright)

A still of the 3D world in the blackout: the developer alone at desk 12, seen from behind and above like the CCTV,
with Claude's two coral eyes open on his dead monitor. Over it, the CCTV chrome and the story in two lines: what he
did (deleted production, 3:07 AM) and the turn (Claude kept a copy). Everything that matters sits inside the middle
1080x1440, the 3:4 crop the profile grid shows.
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
OUT = os.path.join(ROOT, "renders", "nxtlvl_horror-db_reels_9x16_v1_cover.png")
COVER = {"t": round(T["eyes"] + 1.6, 3), "cam": [.78, 2.02, 1.75], "look": [-.04, 1.1, -.22], "fov": 36}

CSS = """
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
@font-face { font-family: "ISerif"; font-style: italic; font-weight: 400; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #050508; font-family: "Montserrat", sans-serif; color: #ece6dc; }
#gl { position: absolute; inset: 0; width: 1080px; height: 1920px; display: block; }
#scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0px, rgba(0,0,0,.18) 2px, rgba(0,0,0,0) 3px, rgba(0,0,0,0) 5px);
  mix-blend-mode: multiply; }
.fade { position: absolute; left: 0; right: 0; top: 0; height: 820px;
  background: linear-gradient(180deg, rgba(5,5,8,.96) 0%, rgba(5,5,8,.86) 62%, rgba(5,5,8,0) 100%); }
.fadeb { position: absolute; left: 0; right: 0; bottom: 0; height: 760px;
  background: linear-gradient(0deg, rgba(5,5,8,.97) 0%, rgba(5,5,8,.85) 55%, rgba(5,5,8,0) 100%); }
.hud { position: absolute; left: 64px; right: 64px; top: 262px; display: flex; justify-content: space-between; align-items: center; }
.rec { display: flex; align-items: center; gap: 14px; font: 800 36px "Montserrat"; letter-spacing: 3px; color: #ff4d4d; text-shadow: 0 0 12px rgba(255,60,60,.6); }
.rec i { width: 22px; height: 22px; border-radius: 50%; background: #ff3b3b; box-shadow: 0 0 16px #ff3b3b; }
.cam { font: 700 30px "JBMono"; letter-spacing: 3px; color: rgba(236,230,220,.85); }
.head { position: absolute; left: 50px; right: 50px; top: 360px; text-align: center; }
.time { font: 800 150px/1 "Montserrat"; letter-spacing: -5px; color: #f2ede6; text-shadow: 0 0 40px rgba(255,60,60,.35); }
.l1 { margin-top: 26px; font: 700 64px/1.1 "Montserrat"; letter-spacing: -1px; color: #ece6dc; }
.l1 b { color: #ff5a5a; font-weight: 800; }
.foot { position: absolute; left: 60px; right: 60px; top: 1330px; text-align: center; }
.l2 { font: 400 112px/1 "ISerif"; font-style: italic; color: #ffb59c; text-shadow: 0 0 30px rgba(255,110,80,.45); }
.l3 { margin-top: 26px; display: inline-block; padding: 10px 24px; border-radius: 10px; border-left: 6px solid #ff7a59; background: rgba(12,8,8,.8);
  font: 700 34px "JBMono"; letter-spacing: 2px; color: #ece6dc; }
.brand { position: absolute; left: 0; right: 0; top: 1620px; text-align: center; font: 700 28px "JBMono"; letter-spacing: 6px; color: rgba(236,230,220,.75); }
.brand b { color: #ff7a59; }
"""

HTML = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>3 AM database horror cover</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <canvas id="gl"></canvas>
    <div id="scan"></div>
    <div class="fade"></div>
    <div class="fadeb"></div>
    <div class="hud"><div class="rec"><i></i>REC</div><div class="cam">CAM 01 · DESK 12</div></div>
    <div class="head">
      <div class="time">03:07 AM.</div>
      <div class="l1">He just deleted <b>production.</b></div>
    </div>
    <div class="foot">
      <div class="l2">Claude kept a copy.</div>
      <div class="l3">1.2M rows · backup dead since March</div>
    </div>
    <div class="brand"><b>✦</b> NXTLVLSOCIAL.AI</div>
    <script>
      window.HR_T = {json.dumps(T)};
      window.HR_COVER = {json.dumps(COVER)};
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
    srv = subprocess.Popen(["python3", "-m", "http.server", "8766", "--bind", "127.0.0.1"], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1)
        subprocess.run(["node", "-e", SHOT, "http://127.0.0.1:8766/cover.html", out], check=True)
    finally:
        srv.terminate()
    print("wrote", out)


if __name__ == "__main__":
    main()
