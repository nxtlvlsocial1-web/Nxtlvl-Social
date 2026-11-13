// Cover for the Creators 100X x Creedom CHECK reel, in the reel's look: light pink fluid glass world, the hook headline
// (Inter 700 + Instrument Serif italic accents), the demo reel on a phone with a glass "4.2/5" score badge and a
// "0:14 Loses trust" flag, and Cree (the 3D Creedom mascot, cheer pose) beside it. Everything important sits inside
// Instagram's 3:4 profile-grid crop (y 240..1680).   node build/cover.cjs [OUT.png]
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv[2] || path.join(ROOT, "renders", "creators100x_creedom-check_reels_9x16_v1_cover.png");
const A = (p) => "file://" + path.join(ROOT, p);
const glass = `background: linear-gradient(135deg, rgba(255,255,255,.66), rgba(255,255,255,.24)); backdrop-filter: blur(26px) saturate(1.7);
  border: 2px solid rgba(255,255,255,.9); box-shadow: inset 0 2px 0 #fff, 0 30px 80px rgba(120,20,60,.22);`;
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: I; font-weight: 700; src: url("${A("assets/fonts/inter-latin-700-normal.woff2")}"); }
@font-face { font-family: I; font-weight: 800; src: url("${A("assets/fonts/inter-latin-800-normal.woff2")}"); }
@font-face { font-family: S; font-style: italic; src: url("${A("assets/fonts/InstrumentSerif-Italic.ttf")}"); }
@font-face { font-family: M; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
* { margin: 0; box-sizing: border-box; }
body { width: 1080px; height: 1920px; overflow: hidden; font-family: I; color: #0B0B0B; position: relative;
  background: radial-gradient(120% 90% at 50% 30%, #ffffff 0%, #fbf3f6 55%, #f6e9ef 100%); }
.bl { position: absolute; border-radius: 50%; filter: blur(90px); }
.pane { position: absolute; border-radius: 70px; ${glass} box-shadow: inset 0 2px 0 rgba(255,255,255,.6); background: linear-gradient(135deg, rgba(255,255,255,.34), rgba(255,255,255,.06)); }
.h { position: absolute; left: 50px; right: 50px; top: 270px; text-align: center; font-weight: 700; font-size: 100px; line-height: 1.02; letter-spacing: -.035em; }
.h i { font-family: S; font-weight: 400; font-size: 1.14em; letter-spacing: -.01em; color: #B1476B; }
.h i.pk { background: linear-gradient(90deg, #EE688B, #F343A2); -webkit-background-clip: text; color: transparent; }
.phone { position: absolute; left: 150px; top: 690px; width: 470px; height: 836px; border-radius: 66px; padding: 13px; transform: rotate(-4deg);
  background: linear-gradient(150deg, rgba(255,255,255,.95), rgba(230,210,220,.6) 40%, rgba(255,255,255,.8)); box-shadow: 0 50px 120px rgba(120,20,60,.32), inset 0 2px 0 #fff; }
.scr { position: relative; width: 100%; height: 100%; border-radius: 54px; overflow: hidden; }
.scr img { width: 100%; height: 100%; object-fit: cover; display: block; }
.isl { position: absolute; left: 50%; top: 28px; width: 130px; height: 36px; margin-left: -65px; border-radius: 26px; background: #000; }
.cap { position: absolute; left: 20px; right: 20px; top: 250px; text-align: center; color: #fff; font-weight: 800; font-size: 38px; text-shadow: 0 4px 20px rgba(0,0,0,.5); }
.score { position: absolute; left: 520px; top: 640px; width: 300px; height: 300px; border-radius: 50%; ${glass} display: flex; flex-direction: column; align-items: center; justify-content: center; }
.score svg { position: absolute; inset: 16px; transform: rotate(-90deg); }
.score b { font-weight: 800; font-size: 104px; letter-spacing: -.04em; line-height: 1; }
.score b span { font-family: S; font-weight: 400; font-size: 58px; margin-left: 6px; color: #B1476B; }
.score em { font-style: normal; font-family: M; font-size: 16px; letter-spacing: .22em; color: #9a6a7e; margin-top: 10px; }
.flag { position: absolute; left: 470px; top: 1360px; padding: 20px 30px; border-radius: 999px; ${glass} display: flex; align-items: center; gap: 16px; font-weight: 700; font-size: 38px; }
.flag i { width: 22px; height: 22px; border-radius: 50%; background: #F343A2; box-shadow: 0 0 14px #F343A2; }
.flag em { font-style: normal; font-family: M; font-size: 30px; color: #8a5a6e; }
.cree { position: absolute; left: 560px; top: 870px; width: 520px; height: 520px; filter: drop-shadow(0 24px 30px rgba(200,40,120,.25)); }
.cta { position: absolute; left: 0; right: 0; margin: 0 auto; width: 560px; top: 1545px; text-align: center; padding: 20px 0; white-space: nowrap; border-radius: 999px;
  background: #0B0B0B; color: #fff; font-weight: 800; font-size: 42px; letter-spacing: .03em; }
.cta b { background: linear-gradient(90deg, #EE688B, #F343A2); -webkit-background-clip: text; color: transparent; }
.grain { position: absolute; inset: 0; opacity: .045; background: url("${A("assets/img/grain.png")}"); mix-blend-mode: overlay; }
</style></head><body>
<i class="bl" style="left:-200px;top:-150px;width:760px;height:760px;background:rgba(238,104,139,.55)"></i>
<i class="bl" style="left:520px;top:260px;width:820px;height:820px;background:rgba(255,190,214,.75)"></i>
<i class="bl" style="left:-260px;top:980px;width:900px;height:900px;background:rgba(217,194,255,.6)"></i>
<i class="bl" style="left:480px;top:1280px;width:820px;height:820px;background:rgba(255,216,194,.6)"></i>
<i class="pane" style="left:-300px;top:330px;width:560px;height:340px;transform:rotate(-18deg)"></i>
<i class="pane" style="left:830px;top:1500px;width:600px;height:360px;transform:rotate(16deg)"></i>
<div class="h">An app that <i>rates</i><br>your reel <i class="pk">before</i><br>you post.</div>
<div class="phone"><div class="scr"><img src="${A("assets/img/demo_f04.jpg")}"><div class="cap">3 AI tools I use daily</div></div><div class="isl"></div></div>
<div class="score"><svg width="268" height="268" viewBox="0 0 200 200"><circle cx="100" cy="100" r="88" fill="none" stroke="rgba(177,71,107,.15)" stroke-width="9"/>
<circle cx="100" cy="100" r="88" fill="none" stroke="#EE688B" stroke-width="9" stroke-linecap="round" stroke-dasharray="553" stroke-dashoffset="88"/></svg>
<b>4.2<span>/5</span></b><em>EXAMPLE REEL</em></div>
<img class="cree" src="${A("assets/img/poses/cheer.png")}">
<div class="flag"><i></i><em>0:14</em>Loses trust</div>
<div class="cta">COMMENT <b>CHECK</b></div>
<div class="grain"></div></body></html>`;
(async () => {
  const f = path.join(ROOT, "cache", "cover.html");
  fs.mkdirSync(path.dirname(f), { recursive: true });
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
