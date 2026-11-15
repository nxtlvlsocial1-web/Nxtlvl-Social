"""Cover for the GTA 6 chat-clipper reel (1080x1920 PNG), built from the reel's own pieces: the Miami art backdrop,
torn-paper headline, the skydive stream card (Rockstar's official clip, a still) with chat bubbles bursting off it, a
spike graph sticker, FREE TOOL sticker, and the three viewers losing it (build/people.py). Headline, card and faces sit
inside the centre 1080x1440 so the 3:4 profile crop keeps them.
python3 build/cover.py  ->  renders/ai-nxtlvl_gta6-chat-clipper_reels_9x16_v3_cover.png
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_vox as G  # noqa: E402
from people import person, CAST  # noqa: E402

ROOT = G.ROOT
OUT = os.path.join(ROOT, "renders", "ai-nxtlvl_gta6-chat-clipper_reels_9x16_v3_cover.png")
NAVY, RED, YEL, PAPER = G.NAVY, G.RED, G.YEL, G.PAPER

bubs = [("LMAO", 50, 1175, -10), ("CLIP IT", 300, 1215, 6), ("KEKW", 610, 1185, -4), ("NO WAY", 790, 1250, 9), ("???", 90, 1290, 5), ("W", 560, 1290, -8)]
bub_html = "".join(f'<div class="bub" style="opacity:1;left:{x}px;top:{y}px;transform:rotate({r}deg)">{w}</div>' for w, x, y, r in bubs)
crowd = (person("cv1", dict(CAST["viewer_b"]), propL="phone", rotL=-160, width=420, style="left:-40px;top:1330px;opacity:1;z-index:7")
         + person("cv2", dict(CAST["viewer_c"]), width=420, style="left:330px;top:1370px;opacity:1;z-index:7")
         + person("cv3", dict(CAST["viewer_d"]), width=420, style="left:700px;top:1330px;opacity:1;z-index:7"))
spike = (f'<svg viewBox="0 0 300 140" style="width:100%;display:block"><path d="M10 120 H290" stroke="{NAVY}" stroke-width="5"/>'
         f'<path d="M10 112 L60 108 L100 114 L140 104 L160 18 L180 106 L230 110 L290 108" fill="none" stroke="{RED}" stroke-width="9" stroke-linejoin="round"/></svg>'
         f'<div class="cap2" style="margin-top:4px">chat / 10 s</div>')
body = f"""
<img class="cbg" src="../assets/img/cover_bg.jpg">
<div id="tint"></div><div id="halftone"></div>
<div class="strip" style="opacity:1;top:250px;transform:rotate(-2.5deg)"><b style="font-size:122px">CHAT FINDS</b></div>
<div class="strip" style="opacity:1;top:392px;transform:rotate(1.5deg)"><b style="font-size:122px">YOUR <span class="hl">GTA 6</span></b></div>
<div class="strip" style="opacity:1;top:534px;transform:rotate(-1deg)"><b style="font-size:122px">CLIPS</b></div>
<div class="card media" style="opacity:1;left:70px;top:690px;width:760px;transform:rotate(-2deg)"><div class="cin">
  <div class="vbox169"><img src="../assets/img/cover_stream.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"><div class="live">LIVE</div></div>
  <div class="cap2">GTA 6 stream · hour 4 of 6</div></div></div>
<div class="card" style="opacity:1;left:720px;top:600px;width:320px;transform:rotate(6deg);z-index:6"><div class="cin">{spike}</div></div>
<div class="sticker" style="opacity:1;left:690px;top:950px;font-size:62px;transform:rotate(8deg)">FREE TOOL</div>
{bub_html}
{crowd}
<img class="brand" src="../assets/img/logo-wordmark.png">
<div id="fringe"></div><div id="grain"></div>
"""
css = G.CSS.replace('url("assets/fonts/', 'url("../assets/fonts/').replace("url(assets/img/", "url(../assets/img/") + f"""
.cbg {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
#cv1 .armL {{ transform-box: view-box; transform-origin: 155px 520px; transform: rotate(150deg); }}
#cv1 .armR, #cv2 .armR, #cv3 .armR {{ transform-box: view-box; transform-origin: 445px 520px; transform: rotate(-160deg); }}
#cv2 .armL, #cv3 .armL {{ transform-box: view-box; transform-origin: 155px 520px; transform: rotate(160deg); }}
"""
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body><div id="root">{body}</div></body></html>"""
os.makedirs(os.path.join(ROOT, "cache"), exist_ok=True)
page = os.path.join(ROOT, "cache", "cover.html")
open(page, "w", encoding="utf-8").write(html)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});
await p.goto('file://{page}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);await p.screenshot({{path:'{OUT}'}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
print("wrote", OUT)
