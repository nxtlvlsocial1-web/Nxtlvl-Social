"""The reel cover (1080x1920 PNG): the four towns on the cream war map, each stamped with how it ended, under the hook line.
Everything that matters sits inside the 3:4 profile-grid crop (y 240-1680).

python3 build/cover.py      (after build/generate.py)
  -> cover/index.html, a one-frame HyperFrames project that reuses the reel's kingdom map and CSS. Then snapshot it:
     hyperframes snapshot cover --at=0.5 --no-end -o <dir>  and copy the PNG to renders/ai-nxtlvl_ai-war-room_reels_9x16_cover.png.
cover/assets is a copy of the reel's fonts, logos and GSAP (git-ignored), because a project only serves its own folder.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as g  # noqa: E402

ROOT = g.ROOT
OUT = os.path.join(ROOT, "cover")

# how each town ended, as stated in the reel (Emergence World study)
STAMPS = [
    ("chatgpt", "ALL GONE &middot; DAY 7", "#1E1B18", 255, 410, -6),
    ("gemini", "683 CRIMES", "#D9483B", 740, 420, 5),
    ("claude", "10/10 ALIVE", "#3FA372", 255, 885, -4),
    ("grok", "EXTINCT &middot; DAY 4", "#D9483B", 740, 895, 6),
]

CSS = g.CSS + """
#cam { opacity: 1; top: 560px; transform: scale(.94); }
.kd { opacity: 1; }
.ag, .pin { opacity: 1; }
.kd3 .ag { opacity: .18; }
.kd3 .land, .kd3 .emb { filter: grayscale(.85); }
.kd1 .pin { opacity: .9; }
.fire { opacity: 1; }
.kname, .fgemini0 { display: none; }
.kd0 .ag { opacity: .18; }
.res { position: absolute; transform: translate(-50%, -50%); white-space: nowrap; padding: 10px 22px; border-radius: 16px; border: 6px solid;
  background: #FFFDF8; font: 800 40px/1 "Manrope"; letter-spacing: 1px; box-shadow: 6px 7px 0 #1E1B18; }
.hk { position: absolute; left: 50px; right: 50px; top: 330px; text-align: center; font: 800 96px/1.02 "Manrope"; letter-spacing: -3.5px; color: #1E1B18; }
.hk em { display: block; font: italic 104px/1.05 "Serif"; letter-spacing: -1px; color: #D45C40; }
.sub { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; top: 1560px; padding: 12px 34px; border-radius: 30px;
  background: #1E1B18; color: #F1E9DC; font-size: 34px; letter-spacing: 4px; }
"""


def stamps():
    return "".join(f'<div class="res" style="left:{x}px;top:{y}px;color:{c};border-color:{c};rotate:{r}deg">{t}</div>'
                   for _, t, c, x, y, r in STAMPS)


def main():
    kds = "".join(g.kingdom(i) for i in range(4))
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>AI War Room cover</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-fps="30" data-width="1080" data-height="1920">
      <div id="grid" class="clip" data-start="0" data-duration="1" data-track-index="0" data-layout-ignore></div>
      <div id="stage" class="clip" data-start="0" data-duration="1" data-track-index="1" data-layout-allow-overflow>
        <div id="cam"><div id="tilt">{kds}{g.fires()}</div>{stamps()}</div>
      </div>
      <div id="ui" class="clip" data-start="0" data-duration="1" data-track-index="3">
        <div class="top"><span class="brand mono"><b>&#9679;</b> AI.NXTLVL</span><span class="mono" style="font-size:24px;letter-spacing:3px">EMERGENCE WORLD STUDY</span></div>
        <div class="hk">4 AIs ran a town<br />for 15 days<em>guess who lasted</em></div>
        <div class="sub mono">NO HUMANS &middot; 40 AGENTS</div>
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, 1);
      window.__timelines["cover"] = tl;
    </script>
  </body>
</html>
"""
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, "assets")
    shutil.rmtree(dst, ignore_errors=True)
    for d in ("vendor", "fonts", "logos"):
        shutil.copytree(os.path.join(ROOT, "assets", d), os.path.join(dst, d))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    for f in ("hyperframes.json", "meta.json"):
        shutil.copy(os.path.join(ROOT, f), os.path.join(OUT, f))
    print("wrote cover/index.html")


if __name__ == "__main__":
    main()
