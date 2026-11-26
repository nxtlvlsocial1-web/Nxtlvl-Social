// node frames.js anim.html outDir count loopSeconds subFrames: one PNG per sub-frame, offset back by the blend window
// so the first GIF frame (t = 0) is the logo at rest.
const { chromium } = require('playwright');
const [, , src, out, count, T, SUB] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 512, height: 512 } });
  await p.goto('file://' + src);
  const n = +count, sub = +SUB;
  for (let i = 0; i < n; i++) {
    const t = ((i - (sub - 1)) / n) * +T;
    await p.evaluate((t) => window.setT(t), t);
    await p.screenshot({ path: `${out}/f${String(i + 1).padStart(4, '0')}.png` });
  }
  await b.close();
})();
