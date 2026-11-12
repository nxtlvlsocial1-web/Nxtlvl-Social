// Cover for the GTA 6 creator playbook reel: the owner's GTA VI key art over a Vice City-graded frame of Rockstar's
// helicopter shot, with the hook. Headline, art and tag line sit inside Instagram's 3:4 profile-grid crop (y 240..1680).
// node build/cover.cjs [OUT.png]
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv[2] || path.join(ROOT, "renders", "nxtlvl_gta6-playbook_reels_9x16_v1_cover.png");
const A = (p) => "file://" + path.join(ROOT, p);
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: M; src: url("${A("assets/fonts/montserrat.ttf")}"); font-weight: 100 900; }
@font-face { font-family: S; src: url("${A("assets/fonts/InstrumentSerif-Italic.ttf")}"); font-style: italic; }
@font-face { font-family: J; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
* { margin: 0; box-sizing: border-box; }
body { width: 1080px; height: 1920px; overflow: hidden; background: #07050f; font-family: M; color: #fff; position: relative; }
.bg { position: absolute; inset: -40px; background: url("${A("cache/cover_bg.png")}") center/cover; filter: blur(6px) saturate(1.3) brightness(.75); }
.grade { position: absolute; inset: 0; background: linear-gradient(175deg, rgba(127,27,248,.75), rgba(255,79,163,.55) 50%, rgba(255,179,107,.55));
  mix-blend-mode: soft-light; }
.dark { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(16,2,44,.75), rgba(16,2,44,.15) 35%, rgba(16,2,44,.25) 65%, rgba(7,5,15,.85)); }
.leak { position: absolute; width: 900px; height: 900px; border-radius: 50%; filter: blur(60px); mix-blend-mode: screen; }
.l1 { left: -300px; top: 150px; background: radial-gradient(circle, rgba(255,79,163,.55), transparent 65%); }
.l2 { right: -320px; bottom: 120px; background: radial-gradient(circle, rgba(127,27,248,.6), transparent 65%); }
.head { position: absolute; left: 40px; right: 40px; top: 270px; text-align: center; font-weight: 900; text-transform: uppercase;
  letter-spacing: -.035em; line-height: 1.02; white-space: nowrap; }
.head .a { font-size: 108px; text-shadow: 0 8px 40px rgba(7,5,15,.8); }
.head .b { font-size: 100px; background: linear-gradient(90deg, #ffb36b, #ff4fa3 45%, #b687f9); -webkit-background-clip: text; color: transparent;
  filter: drop-shadow(0 8px 30px rgba(7,5,15,.8)); }
.head .c { font-size: 108px; text-shadow: 0 8px 40px rgba(7,5,15,.8); }
.head i { font-family: S; font-weight: 400; text-transform: none; letter-spacing: 0; color: #b687f9; }
.art { position: absolute; left: 70px; top: 700px; width: 940px; height: 627px; border-radius: 30px; overflow: hidden; transform: rotate(-3deg);
  box-shadow: 0 0 0 6px rgba(255,255,255,.92), 0 0 110px rgba(255,79,163,.8), 0 40px 90px rgba(7,5,15,.7); }
.art img { width: 100%; height: 100%; object-fit: cover; }
.save { position: absolute; left: 50%; top: 1395px; transform: translateX(-50%); display: flex; align-items: center; gap: 14px; padding: 18px 36px;
  border-radius: 999px; background: #fff; color: #07050f; font-weight: 900; font-size: 44px; letter-spacing: .06em; white-space: nowrap;
  box-shadow: 0 14px 50px rgba(127,27,248,.6); }
.save svg { width: 42px; height: 42px; fill: #7f1bf8; }
.tags { position: absolute; left: 0; right: 0; top: 1525px; text-align: center; font-family: J; font-size: 30px; letter-spacing: .12em; color: #ffb36b;
  text-shadow: 0 4px 20px rgba(7,5,15,.9); }
</style></head><body>
<div class="bg"></div><div class="grade"></div><div class="dark"></div><div class="leak l1"></div><div class="leak l2"></div>
<div class="head"><div class="a">The only</div><div class="b">GTA 6 creator</div><div class="c">video <i>you'll need.</i></div></div>
<div class="art"><img src="${A("assets/img/keyart.jpg")}"></div>
<div class="save"><svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z"/></svg>SAVE THIS BEFORE NOV 19</div>
<div class="tags">AI CLIPPING · SETTINGS · MUSIC · KEYWORDS</div>
</body></html>`;
(async () => {
  const f = path.join(ROOT, "cache", "cover.html");
  fs.writeFileSync(f, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: OUT });
  await b.close();
  console.log("wrote", OUT);
})();
