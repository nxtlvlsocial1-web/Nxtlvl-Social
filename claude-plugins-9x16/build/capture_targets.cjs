// For each beat: open the page, find the sentence that proves the line, take a 1100x1300 crop centred on it (2x) and save
// the sentence's box in that crop, so the composition can zoom to it and frame it exactly (plan/targets.json).
// node build/capture_targets.cjs
const { chromium } = require('playwright');
const fs = require('fs');
const T = JSON.parse(fs.readFileSync(__dirname + '/../plan/targets_in.json', 'utf8'));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 1300 }, deviceScaleFactor: 2, colorScheme: 'light' });
  const OUTP = __dirname + '/../plan/targets.json'; const out = fs.existsSync(OUTP) ? JSON.parse(fs.readFileSync(OUTP, 'utf8')) : {}; let last = '';
  for (const t of T) {
    try {
      if (t.url !== last) { await p.goto(t.url, { waitUntil: 'domcontentloaded', timeout: 45000 }); await p.waitForTimeout(3000); last = t.url;
        if (t.click) { try { await p.click(t.click, { timeout: 4000 }); await p.waitForTimeout(800); } catch (e) {} } }
      const loc = p.getByText(new RegExp(t.find, 'i')).filter({ visible: true }).first();
      await loc.scrollIntoViewIfNeeded({ timeout: 10000 });
      const bb0 = await loc.boundingBox();
      const sy = await p.evaluate((y) => { window.scrollBy(0, y - 520); return window.scrollY; }, bb0.y);
      await p.waitForTimeout(500);
      const bb = await loc.boundingBox();
      await p.screenshot({ path: `assets/img/shots/${t.id}.png` });
      out[t.id] = { x: bb.x * 2, y: bb.y * 2, w: bb.width * 2, h: bb.height * 2, W: 2200, H: 2600, url: t.url };
      console.log(t.id, 'ok', JSON.stringify(out[t.id]));
    } catch (e) { console.log(t.id, 'FAIL', e.message.slice(0, 140)); }
  }
  fs.writeFileSync(__dirname + '/../plan/targets.json', JSON.stringify(out, null, 1));
  await b.close();
})();
