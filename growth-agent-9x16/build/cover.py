"""The Reel's cover: writes cover.html and screenshots it to renders/nxtlvl_growth-agent_reels_9x16_v1_cover.png.

python3 build/cover.py      (from the project root, after build/generate.py; needs node + the preinstalled Playwright)

A still of the 3D world at the 6,700 moment (the phone, Claude, the follower vortex, the confetti), seen from its own
camera with the odometer left out, under the cover's text: the result (339 -> 6,700 followers) as the headline and the
promise (a Claude Instagram growth agent, five moves) below. Everything that matters sits inside the middle 1080x1440,
the 3:4 crop the profile grid shows.
"""
import json
import os
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
OUT = os.path.join(ROOT, "renders", "nxtlvl_growth-agent_reels_9x16_v1_cover.png")
COVER = {"t": round(T["followers"] + .45, 3), "cam": [.38, 1.62, 4.25], "look": [0, 1.5, 0], "fov": 44,
         "claude": [.56, 1.5, .7], "claudeScale": .5, "hideOdo": True, "galaxy": .55}

CSS = """
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
@font-face { font-family: "ISerif"; font-style: italic; font-weight: 400; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #f2e8dc; font-family: "Montserrat", sans-serif; color: #1d1418; }
#gl { position: absolute; inset: 0; width: 1080px; height: 1920px; display: block; }
.fade { position: absolute; left: 0; right: 0; top: 0; height: 760px;
  background: linear-gradient(180deg, rgba(242,232,220,.97) 0%, rgba(242,232,220,.9) 58%, rgba(242,232,220,0) 100%); }
.head { position: absolute; left: 50px; right: 50px; top: 262px; text-align: center; }
.kick { display: inline-block; padding: 10px 26px; border-radius: 30px; background: #1d1418; color: #f6ece2;
  font: 700 30px "JBMono"; letter-spacing: 4px; }
.num { margin-top: 26px; font: 800 168px/1 "Montserrat"; letter-spacing: -7px; white-space: nowrap; }
.num .a { color: #1d1418; } .num .arr { display: inline-block; margin: 0 6px; color: #b4532f; font-weight: 700; transform: translateY(-10px); }
.num .b { display: inline-block; padding: 0 22px 14px; border-radius: 36px; background: #c25a37; color: #fff; box-shadow: 0 22px 60px rgba(194,90,55,.45);
  transform: rotate(-2deg); }
.fol { margin-top: 10px; font: 400 104px/1 "ISerif"; font-style: italic; color: #b4532f; }
.foot { position: absolute; left: 60px; right: 60px; top: 1350px; text-align: center; }
.card { display: inline-block; padding: 26px 40px 30px; border-radius: 40px; background: rgba(255,251,246,.95); box-shadow: 0 24px 60px rgba(120,70,40,.25); }
.l1 { font: 800 60px/1.1 "Montserrat"; letter-spacing: -1.5px; }
.l1 .serif { font: 400 74px/1 "ISerif"; font-style: italic; color: #b4532f; letter-spacing: 0; }
.l2 { margin-top: 18px; display: inline-flex; gap: 14px; align-items: center; font: 700 34px "JBMono"; color: #1d1418; letter-spacing: 2px; }
.l2 b { display: inline-block; padding: 6px 18px; border-radius: 22px; background: #1d1418; color: #f6ece2; }
.brand { position: absolute; left: 60px; top: 1610px; padding: 8px 20px; border-radius: 24px; background: rgba(255,251,246,.9);
  font: 700 28px "JBMono"; letter-spacing: 5px; }
.brand b { color: #b4532f; }
"""

HTML = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Instagram Growth Agent cover</title>
    <script type="importmap">{{"imports":{{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}}}</script>
    <style>{CSS}</style>
  </head>
  <body>
    <canvas id="gl"></canvas>
    <div class="fade"></div>
    <div class="head">
      <div class="kick">CLAUDE · INSTAGRAM GROWTH</div>
      <div class="num"><span class="a">339</span><span class="arr">→</span><span class="b">6,700</span></div>
      <div class="fol">followers</div>
    </div>
    <div class="foot"><div class="card">
      <div class="l1">I turned Claude into an</div>
      <div class="l1"><span class="serif">Instagram growth agent</span></div>
      <div class="l2"><b>5 MOVES</b> the last one's the smartest</div>
    </div></div>
    <div class="brand"><b>✦</b> NXTLVLSOCIAL.AI</div>
    <script>
      window.GA_T = {json.dumps(T)};
      window.GA_COVER = {json.dumps(COVER)};
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
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    srv = subprocess.Popen(["python3", "-m", "http.server", "8765", "--bind", "127.0.0.1"], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1)
        subprocess.run(["node", "-e", SHOT, "http://127.0.0.1:8765/cover.html", OUT], check=True)
    finally:
        srv.terminate()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
