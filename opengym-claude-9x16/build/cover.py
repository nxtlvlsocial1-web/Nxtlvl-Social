"""The reel cover (1080x1920 PNG): NXT in muscle mode, mid-flex as the paywall shatters, under the hook line.
Everything that matters sits inside the 3:4 profile-grid crop (y 240-1680).

python opengym-claude-9x16/build/cover.py      (after generate.py)
  -> cover/index.html, a one-frame HyperFrames project that reuses assets/js/opengym.js with window.OG_COVER set.
     Then snapshot it:  hyperframes snapshot cover --at=0.5 --no-end -o <dir>  and copy the PNG to
     renders/nxtlvl_opengym-claude_reels_9x16_cover.png.
cover/assets is a copy of the reel's assets (git-ignored), because a project only serves its own folder.
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cover")
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
ENV = json.load(open(os.path.join(ROOT, "build", "env.json")))

# muscle mode with the code hologram behind it ("Claude helped build it"); camera pulled back so the arms read
COVER = {"t": round(T["claude"] + .25, 2), "cam": [1.3, 1.36, 4.6], "look": [1.18, 1.5, -.2], "fov": 40, "shift": .1}

HTML = """<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>openGym x Claude cover</title>
    <script type="importmap">{"imports":{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}</script>
    <style>
@font-face { font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #07050d; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #07050d; color: #f4f1fa; font-family: "Poppins", sans-serif; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.shade { background: linear-gradient(180deg, rgba(7,5,13,.96) 0%, rgba(7,5,13,.9) 30%, rgba(7,5,13,.55) 38%, rgba(7,5,13,0) 46%, rgba(7,5,13,0) 70%, rgba(7,5,13,.8) 86%, rgba(7,5,13,.92) 100%); }
.brand { position: absolute; left: 0; right: 0; top: 300px; text-align: center; font: 700 30px "JBMono"; letter-spacing: 6px; }
.brand b { color: #7b2ffb; }
.h { position: absolute; left: 50px; right: 50px; top: 340px; text-align: center; font: 800 132px/.98 "Poppins"; letter-spacing: -4px;
  text-shadow: 0 10px 50px rgba(0,0,0,.7); }
.h em { font-style: normal; color: #a98bff; }
.chip { position: absolute; left: 0; right: 0; top: 640px; text-align: center; }
.chip span { display: inline-block; padding: 14px 36px; border-radius: 44px; background: #3fd69b; color: #07050d; font: 800 46px "Poppins";
  box-shadow: 0 12px 44px rgba(63,214,155,.45); }
.nos { position: absolute; left: 0; right: 0; top: 1545px; display: flex; justify-content: center; gap: 18px; }
.nos span { display: flex; align-items: center; gap: 12px; padding: 12px 26px 12px 22px; border-radius: 40px; background: rgba(7,5,13,.82);
  border: 3px solid #ff6b6b; color: #f4f1fa; font: 700 38px "Poppins"; box-shadow: 0 10px 34px rgba(0,0,0,.45); }
.nos b { color: #ff6b6b; font: 800 40px "Poppins"; }
.og { position: absolute; left: 0; right: 0; top: 1636px; text-align: center; font: 700 30px "JBMono"; letter-spacing: 5px; color: #d9ccff; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="1" data-track-index="0"></canvas>
      <div class="clip shade" data-start="0" data-duration="1" data-track-index="1" data-layout-ignore></div>
      <div class="clip" data-start="0" data-duration="1" data-track-index="2">
        <div class="brand"><b>●</b> AI.NXTLVL</div>
        <div class="h">Delete your<br /><em>gym app.</em></div>
        <div class="chip"><span>Claude helped build a free one</span></div>
        <div class="nos"><span><b>&#10005;</b>subscription</span><span><b>&#10005;</b>ads</span><span><b>&#10005;</b>account</span></div>
        <div class="og">OPENGYM &middot; OPEN SOURCE</div>
      </div>
    </div>
    <script>
      window.OG_T = @T@;
      window.OG_ENV = @ENV@;
      window.OG_COVER = @COVER@;
      window.__timelines = window.__timelines || {};
    </script>
    <script type="module" src="assets/js/opengym.js"></script>
  </body>
</html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, "assets")
    shutil.rmtree(dst, ignore_errors=True)
    for d in ("vendor", "fonts", "js"):
        shutil.copytree(os.path.join(ROOT, "assets", d), os.path.join(dst, d))
    html = HTML.replace("@T@", json.dumps(T)).replace("@ENV@", json.dumps(ENV, separators=(",", ":"))).replace("@COVER@", json.dumps(COVER))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    for f in ("hyperframes.json", "meta.json"):
        shutil.copy(os.path.join(ROOT, f), os.path.join(OUT, f))
    print("wrote cover/index.html at t =", COVER["t"])


if __name__ == "__main__":
    main()
