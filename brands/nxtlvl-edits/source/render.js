// Renders SVG/HTML files to PNG.  node render.js <in> <out.png> <width> <height> [scale]  (pairs can repeat)
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const args = process.argv.slice(2);
  const browser = await chromium.launch();
  for (let i = 0; i < args.length; i += 5) {
    const [src, out, w, h, scale] = args.slice(i, i + 5);
    const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +(scale || 1) });
    await page.goto('file://' + path.resolve(src));
    await page.evaluate(() => document.fonts && document.fonts.ready);
    await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: +w, height: +h } });
    await page.close();
    console.log('rendered', out);
  }
  await browser.close();
})();
