// Renders renders/cover.png (1080x1920) from build/cover.html.   node build/cover.cjs   (from the project root)
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const ROOT = path.join(__dirname, '..'), OUT = path.join(ROOT, 'renders', 'cover.png'), T = 1.95; // the grid is full, just before it bursts
const types = { '.html': 'text/html', '.js': 'text/javascript', '.woff2': 'font/woff2', '.png': 'image/png' };
const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0, async () => {
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', (e) => console.error('page error:', e.message));
  await p.goto(`http://localhost:${srv.address().port}/build/cover.html`);
  await p.waitForFunction(() => window.SCENE3D, null, { timeout: 120000 });
  await p.evaluate(async (t) => { await document.fonts.ready; await window.SCENE3D.ready; window.SCENE3D.renderAt(t); }, T);
  await p.screenshot({ path: OUT });
  await b.close(); srv.close(); console.log('wrote', OUT);
});
