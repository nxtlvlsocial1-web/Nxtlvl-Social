"""The Reel's cover (1080x1920), in the video's own look, saying in one glance what the video is about.

python3 build/cover.py      (from the project root; writes build/cover.html and renders/<name>_cover.png with Playwright)

Everything that matters sits inside the profile grid's 3:4 centre crop (y 240 to 1680): the headline (PS2 games become
real PC games), proof (real RE4 gameplay in the GAME.EXE window, "not an emulator"), who does it (the Claude crab and
"11 free Claude skills") and where it runs (Windows, Mac, Linux, Steam Deck).
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mascots import pixel_map  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_console-continue_reels_9x16_v2_cover.png")


def pixel_svg(name, pose="stand", cell=20, flip=False):
    """A pixel actor as an inline SVG, drawn exactly like the video's actors (outline included)."""
    m = pixel_map(name, pose)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.03" height="1.03" fill="{c}"/>' for x, y, c in m["cells"])
    tr = f' style="transform:scaleX(-1)"' if flip else ""
    return (f'<svg viewBox="0 0 {m["w"]} {m["h"]}" width="{m["w"] * cell}" height="{m["h"] * cell}" shape-rendering="crispEdges"{tr}>'
            f'{rects}</svg>')


HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Anton"; src: url("../assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Lilita One"; src: url("../assets/fonts/LilitaOne.ttf"); }}
@font-face {{ font-family: "Rubik"; font-weight: 800; src: url("../assets/fonts/Rubik-ExtraBold.ttf"); }}
@font-face {{ font-family: "Chakra Petch"; font-weight: 700; src: url("../assets/fonts/ChakraPetch-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; position: relative;
  background: radial-gradient(circle at 50% 42%, #f0414a 0, #b3121f 45%, #4f0610 100%); font-family: "Rubik"; }}
.grain {{ position: absolute; inset: 0; background: url("../assets/img/grain.png"); opacity: .09; mix-blend-mode: overlay; }}
.vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse 80% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.45) 100%); }}
.head {{ position: absolute; left: 40px; right: 40px; top: 250px; transform: rotate(-4deg); display: flex; flex-direction: column; align-items: center; }}
.s {{ font: 800 66px/1 "Rubik"; color: #fff; text-shadow: 0 5px 0 #4a0610; }}
.b {{ font: 400 158px/.92 "Anton"; white-space: nowrap; color: #fff; letter-spacing: 2px; text-shadow: 0 9px 0 #4a0610, 0 0 50px rgba(0,0,0,.3); }}
.b.acc {{ color: #ffd36e; }}
.b .hol {{ color: #4a0610; -webkit-text-stroke: 5px #ffd36e; }}
.win {{ position: absolute; left: 150px; top: 730px; width: 780px; transform: rotate(3deg); border: 6px solid #1d1a26; border-radius: 26px; overflow: hidden;
  background: #fff; box-shadow: 0 30px 60px rgba(0,0,0,.45); }}
.wt {{ height: 58px; background: #7a2ffb; color: #fff; font: 700 32px/58px "Chakra Petch"; letter-spacing: 3px; padding-left: 22px; }}
.wt span {{ font-size: 22px; opacity: .85; margin-left: 14px; }}
.win img {{ display: block; width: 100%; height: 400px; object-fit: cover; object-position: 40% 50%; }}
.stk {{ position: absolute; right: 64px; top: 690px; transform: rotate(8deg); font: 400 44px/1 "Anton"; letter-spacing: 1px; color: #1d1a26;
  background: #ffd36e; border: 5px solid #1d1a26; border-radius: 16px; padding: 14px 24px; }}
.stk b {{ color: #e8344e; font-weight: 400; }}
.ps2 {{ position: absolute; left: 58px; top: 800px; width: 150px; height: 150px; background: #fff; border: 5px solid #1d1a26; border-radius: 30px;
  display: flex; align-items: center; justify-content: center; transform: rotate(-8deg); box-shadow: 0 14px 30px rgba(0,0,0,.35); }}
.ps2 img {{ height: 112px; }}
.cast {{ position: absolute; left: 0; right: 0; top: 1170px; height: 300px; }}
.cast > * {{ position: absolute; bottom: 0; }}
.pill {{ position: absolute; left: 50%; top: 1478px; transform: translateX(-50%) rotate(-2deg); white-space: nowrap; font: 400 58px/1 "Lilita One";
  color: #fff; background: #D97757; border: 5px solid #1d1a26; border-radius: 999px; padding: 16px 40px; box-shadow: 0 10px 0 #4a0610; }}
.plat {{ position: absolute; left: 0; right: 0; top: 1590px; display: flex; justify-content: center; gap: 22px; }}
.plat i {{ width: 92px; height: 92px; background: #fff; border-radius: 26px; border: 4px solid #1d1a26; display: flex; align-items: center; justify-content: center; }}
.plat img {{ max-width: 68px; max-height: 68px; }}
.plat i.wide img {{ max-width: 82px; }}
</style></head><body>
<div class="head">
  <div class="s">your old</div>
  <div class="b">PS2 GAMES</div>
  <div class="s">now run as</div>
  <div class="b acc">REAL PC <span class="hol">G</span>AMES</div>
</div>
<div class="win"><div class="wt">GAME.EXE<span>NATIVE PC BUILD</span></div><img src="../assets/img/cover-re4.jpg" alt=""></div>
<div class="ps2"><img src="../assets/img/ps2-logo.png" alt=""></div>
<div class="stk"><b>NOT</b> AN EMULATOR</div>
<div class="cast">
  <div style="left:60px">{pixel_svg("rook", "cheer", 13)}</div>
  <div style="left:350px">{pixel_svg("crab", "cheer", 19)}</div>
  <div style="left:820px">{pixel_svg("dash", "cheer", 13, flip=True)}</div>
</div>
<div class="pill">11 free Claude skills</div>
<div class="plat"><i><img src="../assets/img/windows-logo.png" alt=""></i><i><img src="../assets/img/apple.png" alt=""></i>
  <i class="wide"><img src="../assets/img/linux-logo.png" alt=""></i><i><img src="../assets/img/deck-logo.png" alt=""></i></div>
<div class="vig"></div><div class="grain"></div>
</body></html>"""

SHOT = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + process.argv[1]);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({ path: process.argv[2] });
  await b.close();
})();
"""

if __name__ == "__main__":
    page = os.path.join(ROOT, "build", "cover.html")
    open(page, "w", encoding="utf-8").write(HTML)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    subprocess.run(["node", "-e", SHOT, page, OUT], check=True)
    print("wrote", OUT)
