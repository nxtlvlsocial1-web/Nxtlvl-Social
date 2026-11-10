// Renders html/*.html to 600 dpi print PNGs (with 2 mm bleed) in ../<option>/. Then run finish.py.
// 10 CSS px = 1 mm, so 600 dpi = 600 / 254 device pixels per CSS px.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 896, height: 580 }, deviceScaleFactor: 600 / 254 });
  const dir = path.join(__dirname, 'html');
  for (const f of fs.readdirSync(dir).filter((n) => n.endsWith('.html'))) {
    const slug = f.replace('.html', '');
    await page.goto('file://' + path.join(dir, f));
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(__dirname, '..', slug);
    fs.mkdirSync(out, { recursive: true });
    await page.screenshot({ path: path.join(out, `${slug}_print-bleed.png`), clip: { x: 0, y: 0, width: 896, height: 580 } });
    console.log('rendered', slug);
  }
  await browser.close();
})();
