// node build/snap.cjs <out_dir> <scale> <t1> <t2> ...  : renders frames of index.html (3D + HTML at that time) to PNGs
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const root = path.resolve(__dirname, '..');
const [out, scale, ...ts] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.wav': 'audio/wav', '.png': 'image/png', '.webp': 'image/webp', '.mp3': 'audio/mpeg' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: +scale || .5 });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message)); p.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto(`http://localhost:${srv.address().port}/index.html`);
  await p.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.store, null, { timeout: 180000 });
  await p.evaluate(() => window.__hf.buildReady.store);
  for (const t of ts) {
    const t0 = Date.now();
    await p.evaluate((t) => { window.__timelines.main.seek(+t); window.STORE_DEBUG.renderAt(+t); }, t);
    await p.screenshot({ path: path.join(out, `t${(+t).toFixed(2).padStart(6, '0')}.png`) });
    console.log('t', t, Date.now() - t0, 'ms');
  }
  await b.close(); srv.close();
});
