"""Cover for the Riya paper cut-out reel (1080x1920 PNG), built from the reel's own pieces (build/generate.py):
Riya with her 200-views phone, the robot with the GENERIC scroll, the wall of identical reels behind, a torn-paper
headline. The headline, faces and the fix label sit inside the centre 1080x1350 so the 4:5 grid crop and the 3:4
profile crop keep them.
python3 build/cover.py  ->  renders/creators100x_riya-paper-story_reels_9x16_v1_cover.png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as G  # noqa: E402

ROOT = G.ROOT
OUT = os.path.join(ROOT, "renders", "creators100x_riya-paper-story_reels_9x16_v1_cover.png")

wall = G.wall_html("cw")
ph = (f'<div class="dphone" style="left:520px;top:900px;width:240px;transform:rotate(-6deg)">{G.phone_svg()}'
      f'<div class="dps"><div class="dpv">200</div><div class="dpl">views</div><div class="dpbar"><i style="transform:scaleX(.16)"></i></div></div></div>')
scroll = ('<div class="scrollA" style="left:600px;top:1180px;width:420px;opacity:1;transform:rotate(5deg)"><i class="ssh"></i><div class="sci" style="font-size:30px">'
          '<b>Hey guys!</b> Are you ready to level up your fitness journey?</div><div class="gen" style="opacity:1;font-size:44px;bottom:-34px">GENERIC</div></div>')
body = f"""
<div class="scene" style="opacity:1;z-index:1"><div class="sbg" style="background:#FFE3EE"></div><div class="fade">{wall}</div></div>
<div class="scene" style="opacity:1;z-index:2">
  <div class="rwrap" id="cr" style="left:10px;top:820px;width:640px">{G.riya("sad")}</div>
  {ph}
  <div class="bwrap" id="cb" style="left:720px;top:780px;width:300px">{G.robot()}</div>
  {scroll}
  {G.torn_strip('WHY HER AI SCRIPTS<br>GOT <span class="pk">200 VIEWS</span>', "top", "ch")}
  <div class="fix"><b>+ THE 4-PART FIX</b></div>
</div>
<div id="grain"></div>
"""
css = G.CSS + """
.fade { position: absolute; inset: 0; opacity: .45; }
.fade .wall { transform: scale(1.05); }
#ch { top: 330px; } #ch b { font-size: 82px; }
.fix { position: absolute; left: 0; right: 0; top: 1500px; text-align: center; z-index: 7; }
.fix b { display: inline-block; padding: 18px 40px 22px; background: #CCFB79; border: 6px solid #101111; border-radius: 22px; font-weight: 800; font-size: 64px;
  letter-spacing: .02em; transform: rotate(-3deg); box-shadow: 10px 12px 0 rgba(60,30,30,.26); }
"""
page = f"""<!doctype html><html><head><meta charset="UTF-8"><style>{css}</style></head><body>
<div id="root" style="width:1080px;height:1920px">{body}</div>
<script>
  // static poses: her right arm up holding the phone, robot arm out with the scroll
  document.querySelector('#cr #rarm').setAttribute('transform', 'rotate(-128)');
  document.querySelector('#cr #rh').setAttribute('transform', 'rotate(-6)');
  document.querySelector('#cb .barmR').setAttribute('transform', 'rotate(-40)');
</script></body></html>"""
html_p = os.path.join(ROOT, "cache", "cover.html")
open(html_p, "w").write(page)
js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1080, height: 1920 }} }});
  await p.goto('file://{html_p}'); await p.waitForTimeout(600);
  await p.screenshot({{ path: '{OUT}' }}); await b.close();
}})();"""
subprocess.run(["node", "-e", js], check=True, cwd=ROOT)
print("wrote", OUT)
