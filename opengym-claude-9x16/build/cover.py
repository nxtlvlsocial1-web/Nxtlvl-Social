"""The reel cover (1080x1920 PNG): the muscle-map hero frame with NXT, under the brief's headline.

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

# legs pulsing red, all three labels up, NXT pointing at the hologram
COVER = {"t": round(T["untrained"] + .55, 2), "cam": [.12, 1.15, 5.0], "look": [.3, .92, -.15], "fov": 42, "shift": .12, "holoYaw": .2}

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
.shade { background: linear-gradient(180deg, rgba(7,5,13,.92) 0%, rgba(7,5,13,.75) 22%, rgba(7,5,13,0) 40%, rgba(7,5,13,0) 78%, rgba(7,5,13,.55) 100%); }
.brand { position: absolute; left: 0; right: 0; top: 300px; text-align: center; font: 700 30px "JBMono"; letter-spacing: 6px; }
.brand b { color: #7b2ffb; }
.h { position: absolute; left: 60px; right: 60px; top: 352px; text-align: center; font: 800 112px/1.02 "Poppins"; letter-spacing: -3px;
  text-shadow: 0 8px 40px rgba(0,0,0,.6); }
.h em { font-style: normal; color: #a98bff; }
.chip { position: absolute; left: 0; right: 0; top: 610px; text-align: center; }
.chip span { display: inline-block; padding: 12px 34px; border-radius: 40px; background: #3fd69b; color: #07050d; font: 800 44px "Poppins";
  box-shadow: 0 12px 40px rgba(63,214,155,.45); }
.mm { position: absolute; right: 60px; display: flex; align-items: center; gap: 16px; padding: 12px 30px 12px 22px; border-radius: 40px;
  background: rgba(7,5,13,.8); border: 3px solid var(--c); color: var(--c); font: 800 44px "Poppins"; box-shadow: 0 10px 34px rgba(0,0,0,.4); }
.mm i { width: 22px; height: 22px; border-radius: 50%; background: var(--c); box-shadow: 0 0 16px var(--c); }
.mm0 { --c: #3fd69b; top: 1300px; } .mm1 { --c: #ffc24a; top: 1395px; } .mm2 { --c: #ff6b6b; top: 1490px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="1" data-track-index="0"></canvas>
      <div class="clip shade" data-start="0" data-duration="1" data-track-index="1" data-layout-ignore></div>
      <div class="clip" data-start="0" data-duration="1" data-track-index="2">
        <div class="brand"><b>●</b> AI.NXTLVL</div>
        <div class="h">Claude wrote<br /><em>my gym plan.</em></div>
        <div class="chip"><span>free app tracks every set</span></div>
        <div class="mm mm0"><i></i>WORKED</div><div class="mm mm1"><i></i>RECOVERING</div><div class="mm mm2"><i></i>UNTRAINED</div>
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
