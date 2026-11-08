"""The reel cover (1080x1920 PNG): your hand holding the phone on the New York street, the screen showing tomorrow
(9:14 AM, a man drops his coffee), the man himself behind it, under the serif hook, with four prediction chips that end on
the black screen. Everything that matters sits inside the 3:4 profile-grid crop (y 240-1680).

python3 build/cover.py      (after build/generate.py; needs npx and the HyperFrames CLI)
  1. renders the plate: writes cover/index.html with window.FUTURE_COVER (the reel's time) and no overlays, snapshots
     it, keeps the PNG in cover/assets/plates/
  2. writes the final cover/index.html (the plate, a shade, the headline, the chips), snapshots it and copies the PNG to
     renders/nxtlvl_ai-future_reels_9x16_cover.png
cover/assets is a copy of the reel's assets plus the plate (git-ignored), because a project only serves its own folder.
"""
import glob
import json
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cover")
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
CLI = ["npx", "--yes", "hyperframes@0.8.203"]

PLATES = {"street": (round(T["l"][0] + 1.6, 2), {"ap": .16})}

HEAD = """<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI Future cover</title>
    <script type="importmap">{"imports":{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
@font-face { font-family: "Garamond"; font-weight: 400 800; src: url("assets/fonts/EBGaramond.ttf"); }
@font-face { font-family: "Garamond"; font-style: italic; font-weight: 400 800; src: url("assets/fonts/EBGaramond-Italic.ttf"); }
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0B0A12; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0B0A12; color: #FFFDF6; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.plate { position: absolute; inset: 0; width: 1080px; height: 1920px; }
.shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(8,8,14,.88) 0%, rgba(8,8,14,.62) 24%, rgba(8,8,14,0) 36%, rgba(8,8,14,0) 66%, rgba(8,8,14,.78) 78%, rgba(8,8,14,.9) 100%); }
.head { position: absolute; left: 60px; right: 60px; top: 262px; text-align: center; text-shadow: 0 4px 20px rgba(0,0,0,.6); }
.head .k { display: block; font: 800 26px/1 "Manrope"; letter-spacing: 7px; color: rgba(255,253,246,.85); }
.head b { display: block; margin-top: 18px; font: 500 78px/1.04 "Garamond"; letter-spacing: -.5px; }
.head b span { color: #F2C94C; font-weight: 700; }
.chips { position: absolute; left: 50px; right: 50px; top: 1430px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
.chip { padding: 18px 22px; border-radius: 22px; background: rgba(16,18,28,.82); border: 2px solid rgba(255,253,246,.22); display: flex; align-items: center; gap: 16px; }
.chip i { flex: none; width: 46px; height: 46px; border-radius: 50%; background: #3FA372; color: #fff; font: 800 28px/46px "Manrope"; text-align: center; font-style: normal; }
.chip.q i { background: #C8372D; }
.chip span { font: 800 22px/1.15 "Manrope"; letter-spacing: 1px; }
.chip span small { display: block; font: italic 500 30px/1.1 "Garamond"; letter-spacing: 0; color: rgba(255,253,246,.85); }
    </style>
  </head>
  <body>
"""


def plate_html(t, cam):
    return HEAD + f"""    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="1" data-track-index="0"></canvas>
    </div>
    <script>
      window.CT = {json.dumps(T)};
      window.FUTURE_COVER = {json.dumps({"t": t, **cam})};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, 1);
      window.__timelines["cover"] = tl;
    </script>
    <script type="module" src="assets/js/future.js"></script>
  </body>
</html>
"""


FINAL = HEAD + """    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <div class="clip" data-start="0" data-duration="1" data-track-index="0">
        <img class="plate" src="assets/plates/street.png" alt="" />
        <div class="shade"></div>
      </div>
      <div class="clip" data-start="0" data-duration="1" data-track-index="1">
        <div class="head"><span class="k">WHAT IF</span><b>your phone could see <span>24&nbsp;hours</span> into the future?</b></div>
        <div class="chips">
          <div class="chip"><i>&#10003;</i><span>DAY 1 &middot; 9:14 AM<small>the coffee drops</small></span></div>
          <div class="chip"><i>&#10003;</i><span>DAY 4 &middot; LAS VEGAS<small>black 17</small></span></div>
          <div class="chip"><i>&#10003;</i><span>DAY 12 &middot; NOON<small>the bridge falls</small></span></div>
          <div class="chip q"><i>?</i><span>DAY 30<small>there is no tomorrow</small></span></div>
        </div>
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.set({}, {}, 1);
      window.__timelines["cover"] = tl;
    </script>
  </body>
</html>
"""


def snap(dst):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([*CLI, "snapshot", OUT, "--at=0.5", "--no-end", "--timeout", "180000", "-o", d], check=True,
                       capture_output=True, env={**os.environ, "HYPERFRAMES_NO_TELEMETRY": "1"})
        shutil.copy(glob.glob(os.path.join(d, "frame-*.png"))[0], dst)


def main():
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, "assets")
    shutil.rmtree(dst, ignore_errors=True)
    for d in ("vendor", "fonts", "js"):
        shutil.copytree(os.path.join(ROOT, "assets", d), os.path.join(dst, d))
    for f in ("hyperframes.json", "meta.json"):
        shutil.copy(os.path.join(ROOT, f), os.path.join(OUT, f))
    os.makedirs(os.path.join(dst, "plates"))
    html = os.path.join(OUT, "index.html")
    for name, (t, cam) in PLATES.items():
        open(html, "w", encoding="utf-8", newline="\n").write(plate_html(t, cam))
        snap(os.path.join(dst, "plates", name + ".png"))
        print("plate", name, "at t =", t)
    open(html, "w", encoding="utf-8", newline="\n").write(FINAL)
    out = os.path.join(ROOT, "renders", "nxtlvl_ai-future_reels_9x16_cover.png")
    snap(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
