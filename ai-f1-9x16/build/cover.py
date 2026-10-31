"""The reel cover (1080x1920 PNG): the whole race in one frame. Two plates split on a diagonal: lap 3 in the rain on
the left (#7 on wets carving through the spray), the finish on the right (#11 taking the flag as #7 moves aside),
under the hook headline, with a four-stop race timeline. Everything that matters sits inside the 3:4 profile-grid crop
(y 240-1680).

python3 build/cover.py      (after build/generate.py; needs npx and the HyperFrames CLI)
  1. renders each plate: writes cover/index.html with window.F1_COVER (the reel's time, a pinned camera) and no
     overlays, snapshots it, keeps the PNG in cover/assets/plates/
  2. writes the final cover/index.html (the two plates, the diagonal, the cards), snapshots it and copies the PNG to
     renders/nxtlvl_ai-f1_reels_9x16_cover.png
cover/assets is a copy of the reel's assets plus the plates (git-ignored), because a project only serves its own folder.
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

PLATES = {"rain": (14.6, {"cam": [23.0, 4.6, -12.0], "look": [18.4, 0, -24.5], "fov": 42}),
          "finish": (40.35, {"cam": [21.7, 2.2, -18.5], "look": [21.5, .9, -1.5], "fov": 27})}

HEAD = """<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI F1 cover</title>
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
.plate { position: absolute; inset: 0; width: 1080px; height: 1920px; }
.finish { clip-path: polygon(640px 0, 1080px 0, 1080px 1920px, 400px 1920px); }
.top { position: absolute; left: 60px; right: 60px; top: 262px; display: flex; justify-content: space-between; align-items: center;
  font-size: 28px; letter-spacing: 4px; }
.pill { padding: 10px 20px; border-radius: 28px; background: #FFFDF8; border: 3px solid #1E1B18; display: flex; align-items: center; gap: 12px; }
.pill i { width: 16px; height: 16px; border-radius: 50%; background: #E8735A; }
.pill.w { color: #A8452F; }
.card { position: absolute; left: 60px; right: 60px; top: 340px; padding: 28px 34px 32px; border-radius: 34px; background: #FFFDF8;
  border: 3px solid #1E1B18; box-shadow: 10px 11px 0 #1E1B18; text-align: center; }
.card b { display: block; font: 800 92px/1.0 "Manrope"; letter-spacing: -3.5px; }
.card em { display: block; margin-top: 12px; font: italic 70px/1 "Serif"; color: #D45C40; }
.tag { position: absolute; padding: 12px 22px; border-radius: 24px; background: #FFFDF8; border: 3px solid #1E1B18; box-shadow: 6px 7px 0 #1E1B18;
  font-size: 28px; letter-spacing: 2px; display: flex; align-items: center; gap: 12px; white-space: nowrap; }
.tag i { width: 22px; height: 22px; border-radius: 50%; border: 3px solid #1E1B18; }
.tag.ok { left: 60px; top: 820px; color: #3A7BD5; border-color: #3A7BD5; box-shadow: 6px 7px 0 #3A7BD5; } .tag.ok i { background: #3A7BD5; border-color: #3A7BD5; }
.tag.bad { right: 60px; top: 1250px; color: #A8452F; } .tag.bad i { background: #F2B33D; }
.tl { position: absolute; left: 50px; right: 50px; top: 1468px; padding: 20px 20px 22px; border-radius: 30px; background: #FFFDF8;
  border: 3px solid #1E1B18; box-shadow: 8px 9px 0 #1E1B18; display: flex; justify-content: space-between; }
.st { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center; position: relative; }
.st + .st::before { content: ""; position: absolute; left: -2px; top: 6px; bottom: 6px; width: 2px; background: #E4D9C7; }
.st i { width: 26px; height: 26px; border-radius: 50%; border: 3px solid #1E1B18; }
.st .h { font-size: 28px; letter-spacing: 1px; }
.st .d { font: 700 24px/1.15 "Manrope"; color: #3a3530; }
.st.g i { background: #3FA372; } .st.r i { background: #D9483B; } .st.r .h { color: #D9483B; } .st.b i { background: #3A7BD5; } .st.y i { background: #F2B33D; }
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
      window.F1_COVER = {json.dumps({"t": t, **cam})};
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, 1);
      window.__timelines["cover"] = tl;
    </script>
    <script type="module" src="assets/js/track.js"></script>
  </body>
</html>
"""


FINAL = HEAD + """    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <div class="clip" data-start="0" data-duration="1" data-track-index="0">
        <img class="plate" src="assets/plates/rain.png" alt="" />
        <img class="plate finish" src="assets/plates/finish.png" alt="" />
        <svg class="plate" viewBox="0 0 1080 1920"><line x1="640" y1="0" x2="400" y2="1920" stroke="#FFFDF8" stroke-width="12"/>
          <line x1="640" y1="0" x2="400" y2="1920" stroke="#1E1B18" stroke-width="4"/></svg>
      </div>
      <div class="clip" data-start="0" data-duration="1" data-track-index="1">
        <div class="top mono"><span class="pill"><i></i>NXTLVLSOCIAL.AI</span><span class="pill w">WHAT IF</span></div>
        <div class="card"><b>An AI ran an F1 team for one race</b><em>then it told him to lose</em></div>
        <div class="tag ok mono"><i></i>LAP 3 &middot; ONLY ONE ON WETS</div>
        <div class="tag bad mono"><i></i>LAST LAP &middot; LET HIM THROUGH</div>
        <div class="tl">
          <div class="st r"><i></i><span class="h mono">LAP 1</span><span class="d">boxed,<br />drops to P20</span></div>
          <div class="st b"><i></i><span class="h mono">LAP 3</span><span class="d">rain: 6 cars<br />in one lap</span></div>
          <div class="st g"><i></i><span class="h mono">LAP 40</span><span class="d">dodges<br />the crash: P1</span></div>
          <div class="st y"><i></i><span class="h mono">FINAL</span><span class="d">gives the win<br />away</span></div>
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
    out = os.path.join(ROOT, "renders", "nxtlvl_ai-f1_reels_9x16_cover.png")
    snap(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
