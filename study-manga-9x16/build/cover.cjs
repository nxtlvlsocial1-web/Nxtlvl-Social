// Cover for the Creators 100X STUDY reel, in the reel's look (off-white ground, lime/pink glows, black Inter 800, red-pink
// gradient accent): the hook headline over the owner's real ChatGPT manga, its panels fanned out, a "1 PROMPT" stamp.
// Headline, panels and stamp sit inside Instagram's 3:4 profile-grid crop (y 240..1680).
// node build/cover.cjs [OUT.png]
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv[2] || path.join(ROOT, "renders", "creators100x_study-manga_reels_9x16_v1_cover.png");
const A = (p) => "file://" + path.join(ROOT, p);
const pans = [[110, 820, -10], [560, 790, 8], [80, 1110, 6], [590, 1090, -7], [330, 950, -2]];
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: I; font-weight: 800; src: url("${A("assets/fonts/inter-latin-800-normal.woff2")}"); }
@font-face { font-family: I; font-weight: 700; src: url("${A("assets/fonts/inter-latin-700-normal.woff2")}"); }
* { margin: 0; box-sizing: border-box; }
body { width: 1080px; height: 1920px; overflow: hidden; font-family: I; color: #121212; position: relative;
  background: radial-gradient(120% 80% at 50% 40%, #fbfbf9 0%, #f2f2ee 60%, #e9e9e4 100%); }
.g { position: absolute; border-radius: 50%; filter: blur(110px); }
.g1 { width: 900px; height: 900px; left: -380px; top: -200px; background: rgba(176,206,120,.6); }
.g2 { width: 980px; height: 980px; left: 420px; top: 1160px; background: rgba(240,150,170,.55); }
.g3 { width: 700px; height: 700px; left: 560px; top: 300px; background: rgba(255,190,200,.32); }
.grain { position: absolute; inset: 0; opacity: .05; background: url("${A("assets/img/grain.png")}"); mix-blend-mode: multiply; }
.h { position: absolute; left: 80px; right: 60px; top: 330px; font-weight: 800; font-size: 104px; line-height: 1.02; letter-spacing: -.04em; }
.h .gr { background-image: linear-gradient(90deg, #ff2a2a, #ff3d7f 70%, #d02cff); -webkit-background-clip: text; color: transparent; }
.kick { position: absolute; left: 80px; top: 285px; font-weight: 700; font-size: 32px; letter-spacing: .14em; color: #66665f; }
.p { position: absolute; width: 400px; border-radius: 16px; overflow: hidden; box-shadow: 0 0 0 6px #fff, 0 24px 60px rgba(0,0,0,.25); }
.p img { display: block; width: 100%; }
.stamp { position: absolute; left: 600px; top: 690px; padding: 14px 32px; border-radius: 20px; border: 9px solid #ff2a2a; color: #ff2a2a; font-weight: 800;
  font-size: 72px; background: rgba(255,255,255,.94); transform: rotate(-7deg); white-space: nowrap; }
.save { position: absolute; left: 80px; top: 1500px; display: flex; align-items: center; gap: 14px; padding: 18px 34px; border-radius: 999px; background: #121212;
  color: #fff; font-weight: 800; font-size: 44px; letter-spacing: .04em; }
.save b { color: #ff3d7f; }
</style></head><body>
<div class="g g1"></div><div class="g g2"></div><div class="g g3"></div>
<div class="kick">CLASS 10 · LIFE PROCESSES</div>
<div class="h">Your hardest chapter,<br>as a <span class="gr">manga.</span></div>
${pans.map(([x, y, r], i) => `<div class="p" style="left:${x}px;top:${y}px;transform:rotate(${r}deg)"><img src="${A(`assets/img/panels/p${[1, 2, 3, 4, 6][i]}.png`)}"></div>`).join("")}
<div class="stamp">1 PROMPT</div>
<div class="save">5 PROMPTS · COMMENT <b>STUDY</b></div>
<div class="grain"></div></body></html>`;
(async () => {
  const f = path.join(ROOT, "cache", "cover.html");
  fs.writeFileSync(f, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  await p.screenshot({ path: OUT });
  await b.close();
  console.log("wrote", OUT);
})();
