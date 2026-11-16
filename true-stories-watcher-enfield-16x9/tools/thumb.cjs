// YouTube thumbnail (1280x720): two rendered stills split on a diagonal + title in the film's font.
// Usage: node tools/thumb.cjs <left.png> <right.png> <out.png>
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const [L, R, out] = process.argv.slice(2);
const b64 = (f) => fs.readFileSync(path.resolve(f)).toString("base64");
const font = b64(path.join(ROOT, "assets/fonts/poppins-latin-800-normal.woff2"));
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:P;src:url(data:font/woff2;base64,${font}) format("woff2");font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:720px;overflow:hidden;background:#000;font-family:P}
.l,.r{position:absolute;top:0;height:720px;background-size:cover;background-repeat:no-repeat}
.l{left:0;width:742px;background-image:url(data:image/png;base64,${b64(L)});background-position:42% 50%;clip-path:polygon(0 0,742px 0,538px 100%,0 100%);filter:brightness(1.5) saturate(1.2) contrast(1.08)}
.r{left:538px;width:742px;background-image:url(data:image/png;base64,${b64(R)});background-position:22% 30%;clip-path:polygon(204px 0,100% 0,100% 100%,0 100%);filter:saturate(1.2) contrast(1.1)}
.cut{position:absolute;left:0;top:0;width:1280px;height:720px}
.shade{position:absolute;left:0;right:0;top:0;height:300px;background:linear-gradient(180deg,rgba(0,0,0,.75),rgba(0,0,0,0))}
.t{position:absolute;left:0;right:0;top:26px;text-align:center;font-size:118px;line-height:1;color:#fff;letter-spacing:-.01em;
  -webkit-text-stroke:14px #0a0a0a;paint-order:stroke fill;text-shadow:0 8px 0 rgba(0,0,0,.8)}
.t b{color:#ffcc1f}
.tag{position:absolute;bottom:34px;font-size:40px;color:#fff;padding:10px 22px;border-radius:10px;-webkit-text-stroke:0}
.tl{left:34px;background:#d9302a}.tr{right:34px;background:#2f6fe0}
</style></head><body>
<div class="l"></div><div class="r"></div>
<svg class="cut" viewBox="0 0 1280 720"><line x1="742" y1="0" x2="538" y2="720" stroke="#ffcc1f" stroke-width="10"/></svg>
<div class="shade"></div>
<div class="t">BOTH ARE <b>REAL</b></div>
<div class="tag tl">THE WATCHER · USA</div><div class="tag tr">ENFIELD · UK</div>
</body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  await p.setContent(html);
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: out });
  await b.close();
  console.log("thumbnail:", out);
})();
