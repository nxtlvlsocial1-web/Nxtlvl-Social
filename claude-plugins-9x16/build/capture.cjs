// Our own captures of the public pages each plugin lives on (the reference reel's look, rebuilt from fresh screenshots).
// node build/capture.cjs  -> assets/img/shots/<name>_top.png (the page as it opens) and <name>_readme.png (the README)
const { chromium } = require('playwright');
const PAGES = JSON.parse(require('fs').readFileSync(__dirname + '/../plan/pages.json', 'utf8'));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  for (const { name, url } of PAGES) {
    try {
      await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 }); await p.waitForTimeout(3000);
      await p.screenshot({ path: `assets/img/shots/${name}_top.png` });
      const art = await p.$('article.markdown-body');
      if (art) await art.screenshot({ path: `assets/img/shots/${name}_readme.png` });
      else await p.screenshot({ path: `assets/img/shots/${name}_readme.png`, fullPage: true });
      console.log(name, 'ok', art ? 'readme' : 'fullpage');
    } catch (e) { console.log(name, 'FAIL', e.message.slice(0, 120)); }
  }
  await b.close();
})();
