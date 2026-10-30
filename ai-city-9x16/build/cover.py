"""The reel cover (1080x1920 PNG): the whole city at noon under the AI orb, with the hook as the headline.
Everything that matters sits inside the 3:4 profile-grid crop (y 240-1680).

python3 build/cover.py      (after build/generate.py)
  -> cover/index.html, a one-frame HyperFrames project that reuses assets/js/city.js with window.CITY_COVER set (the
     city's time and a pinned camera). Then snapshot it:  hyperframes snapshot cover --at=0.5 --no-end -o <dir>  and
     copy the PNG to renders/ai-nxtlvl_ai-city_reels_9x16_cover.png.
cover/assets is a copy of the reel's assets (git-ignored), because a project only serves its own folder.
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cover")
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))

COVER = {"t": round(T["grid"] + .6, 2), "cam": [17, 25, 33], "look": [0, 5.2, -2.5], "fov": 38}

HTML = """<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI City cover</title>
    <script type="importmap">{"imports":{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}</script>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
@font-face { font-family: "Manrope"; font-weight: 200 800; src: url("assets/fonts/manrope.ttf"); }
@font-face { font-family: "Serif"; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #F1E9DC; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #F1E9DC; color: #1E1B18; font-family: "Manrope", sans-serif; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.mono { font-family: "JBMono", monospace; font-weight: 700; }
.top { position: absolute; left: 60px; right: 60px; top: 270px; display: flex; justify-content: space-between; align-items: center; font-size: 28px; letter-spacing: 4px; }
.top .b { display: flex; align-items: center; gap: 12px; } .top .b i { width: 16px; height: 16px; border-radius: 50%; background: #E8735A; }
.top .w { color: #A8452F; }
.card { position: absolute; left: 60px; right: 60px; top: 330px; padding: 30px 36px 34px; border-radius: 34px; background: #FFFDF8; border: 3px solid #1E1B18;
  box-shadow: 10px 11px 0 #1E1B18; text-align: center; }
.card b { display: block; font: 800 98px/1.0 "Manrope"; letter-spacing: -3.5px; }
.card em { display: block; margin-top: 10px; font: italic 76px/1 "Serif"; color: #D45C40; }
.chip { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1530px; padding: 14px 32px; border-radius: 34px;
  background: #1E1B18; color: #F1E9DC; font-size: 34px; letter-spacing: 4px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="1" data-track-index="0"></canvas>
      <div class="clip" data-start="0" data-duration="1" data-track-index="2">
        <div class="top mono"><span class="b"><i></i>AI.NXTLVL</span><span class="w">WHAT IF</span></div>
        <div class="card"><b>One AI runs a city for 24 hours</b><em>what could go wrong?</em></div>
        <div class="chip mono">NO MAYOR &middot; NO COPS &middot; ONE AI</div>
      </div>
    </div>
    <script>
      window.CT = @CT@;
      window.CITY_COVER = @COVER@;
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.set({}, {}, 1);
      window.__timelines["cover"] = tl;
    </script>
    <script type="module" src="assets/js/city.js"></script>
  </body>
</html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, "assets")
    shutil.rmtree(dst, ignore_errors=True)
    for d in ("vendor", "fonts", "js"):
        shutil.copytree(os.path.join(ROOT, "assets", d), os.path.join(dst, d))
    html = HTML.replace("@CT@", json.dumps(T)).replace("@COVER@", json.dumps(COVER))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    for f in ("hyperframes.json", "meta.json"):
        shutil.copy(os.path.join(ROOT, f), os.path.join(OUT, f))
    print("wrote cover/index.html at t =", COVER["t"])


if __name__ == "__main__":
    main()
