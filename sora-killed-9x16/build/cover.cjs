// Snapshot cover.html to renders/nxtlvl_sora-killed_shorts_9x16_v2_cover.png (and a JPG for upload).
// node build/cover.cjs        (run from the project root)
const { chromium } = require("playwright");
const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".ttf": "font/ttf", ".png": "image/png", ".woff2": "font/woff2", ".json": "application/json" };

(async () => {
  const server = http.createServer((req, res) => {
    const f = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]));
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
    fs.createReadStream(f).pipe(res);
  }).listen(0);
  const port = server.address().port;
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on("pageerror", (e) => console.error("page error:", e.message));
  await page.goto(`http://localhost:${port}/cover.html`);
  await page.waitForFunction(() => window.__coverDone === true, null, { timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  fs.mkdirSync(path.join(ROOT, "renders"), { recursive: true });
  const out = path.join(ROOT, "renders", "nxtlvl_sora-killed_shorts_9x16_v2_cover");
  await page.screenshot({ path: out + ".png" });
  await page.screenshot({ path: out + ".jpg", type: "jpeg", quality: 92 });
  console.log("wrote", out + ".png/.jpg");
  await browser.close();
  server.close();
})();
