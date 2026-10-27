"""The reel cover (1080x1920 PNG): Claude in the producer headset, proud, over the 3 AM studio, under the hook line.
Everything that matters sits inside the 3:4 profile-grid crop (y 240-1680).

python youtube-agent-9x16/build/cover.py      (after generate.py)
  -> cover/index.html, a one-frame HyperFrames project that reuses assets/js/world.js with window.YT_COVER set.
     Then snapshot it:  hyperframes snapshot cover --at=0.5 --no-end -o <dir>  and copy the PNG to
     renders/nxtlvl_youtube-agent_reels_9x16_cover.png.
cover/assets is a copy of the reel's assets (git-ignored), because a project only serves its own folder.
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cover")
T = json.load(open(os.path.join(ROOT, "build", "cues.json")))
ENV = json.load(open(os.path.join(ROOT, "build", "env.json")))

# "for free": Claude's proud, happy-eyed beat, framed close and low so it fills the middle of the cover
COVER = {"t": round(T["free"] + .15, 2), "cam": [.18, 1.18, 1.55], "look": [-.1, 1.5, -.3], "fov": 42}

HTML = """<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>YouTube Agent Skill cover</title>
    <script type="importmap">{"imports":{"three":"./assets/vendor/three/three.module.min.js","three/addons/":"./assets/vendor/three/addons/"}}</script>
    <style>
@font-face { font-family: "Poppins"; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }
@font-face { font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }
@font-face { font-family: "Montserrat"; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }
@font-face { font-family: "JBMono"; font-weight: 700; src: url("assets/fonts/jbmono-bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #06050b; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #06050b; color: #fff; font-family: "Poppins", sans-serif; }
.clip { position: absolute; inset: 0; }
#gl { width: 1080px; height: 1920px; display: block; }
.shade { background: linear-gradient(180deg, rgba(6,5,11,.97) 0%, rgba(6,5,11,.9) 30%, rgba(6,5,11,.5) 39%, rgba(6,5,11,0) 47%, rgba(6,5,11,0) 72%, rgba(6,5,11,.82) 86%, rgba(6,5,11,.94) 100%); }
.brand { position: absolute; left: 0; right: 0; top: 290px; text-align: center; font: 700 30px "JBMono"; letter-spacing: 6px; }
.brand b { color: #b89bff; }
.h { position: absolute; left: 40px; right: 40px; top: 345px; text-align: center; font: 900 118px/1 "Montserrat"; letter-spacing: -4px;
  text-shadow: 0 10px 50px rgba(0,0,0,.75); }
.h u { text-decoration: none; display: inline-block; margin-top: 12px; padding: 4px 30px 14px; border-radius: 30px;
  background: linear-gradient(90deg, #ff3b46, #d97757); box-shadow: 0 16px 50px rgba(255,59,70,.45); }
.chip { position: absolute; left: 0; right: 0; top: 1520px; text-align: center; }
.chip span { display: inline-block; padding: 14px 38px; border-radius: 44px; background: linear-gradient(90deg, #7b2ffb, #d97757);
  font: 800 50px "Poppins"; box-shadow: 0 12px 44px rgba(123,47,251,.5); }
.og { position: absolute; left: 0; right: 0; top: 1625px; text-align: center; font: 700 30px "JBMono"; letter-spacing: 5px; color: #f0a07c; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <canvas id="gl" class="clip" data-start="0" data-duration="1" data-track-index="0"></canvas>
      <div class="clip shade" data-start="0" data-duration="1" data-track-index="1" data-layout-ignore></div>
      <div class="clip" data-start="0" data-duration="1" data-track-index="2">
        <div class="brand"><b>&#9679;</b> NXTLVLSOCIAL.AI</div>
        <div class="h">Claude runs<br />your <u>YouTube</u></div>
        <div class="chip"><span>11 free skills &middot; 1 link to set up</span></div>
        <div class="og">YOUTUBE AGENT SKILL &middot; OPEN SOURCE</div>
      </div>
    </div>
    <script>
      window.YT_T = @T@;
      window.YT_ENV = @ENV@;
      window.YT_COVER = @COVER@;
      window.__timelines = window.__timelines || {};
    </script>
    <script type="module" src="assets/js/world.js"></script>
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
