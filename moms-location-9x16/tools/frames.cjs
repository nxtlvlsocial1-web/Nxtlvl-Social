// Quick look at the 3D stage without the full HyperFrames runtime.
// Usage: node tools/frames.cjs <outDir> <t1,t2,...> [scale=0.5]
// Serves this project through Playwright routing, calls the stage's renderAt(t) and saves each frame
// plus a contact sheet. Captions/end card are hidden; use `npx hyperframes snapshot` for the real composite.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const out = path.resolve(process.argv[2] || "frames");
const times = (process.argv[3] || "1").split(",").map(Number);
const scale = Number(process.argv[4] || 0.5);
const types = { ".html": "text/html", ".js": "text/javascript", ".woff2": "font/woff2", ".json": "application/json", ".wav": "audio/wav" };

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
  page.on("pageerror", (e) => console.log("pageerror:", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.log("console:", m.text()); });
  await page.addInitScript(() => { window.__timelines = {}; });
  await page.route("http://stage.local/**", (route) => {
    const rel = decodeURIComponent(new URL(route.request().url()).pathname);
    const file = path.join(ROOT, rel);
    if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return route.fulfill({ status: 404, body: "" });
    route.fulfill({ status: 200, body: fs.readFileSync(file), contentType: types[path.extname(file)] || "application/octet-stream" });
  });
  await page.goto(`http://stage.local/index.html?scale=${scale}`);
  await page.addStyleTag({ content: "#endcard,#captions{display:none!important}" });
  await page.waitForFunction("window.__counter", null, { timeout: 120000 });
  const files = [];
  for (const t of times) {
    const t0 = Date.now();
    await page.evaluate((tt) => window.__counter.renderAt(tt), t);
    const f = path.join(out, `t${String(t.toFixed(2)).padStart(7, "0")}.png`);
    await page.locator("#stage").screenshot({ path: f });
    files.push(f);
    console.log(`t=${t} ${Date.now() - t0}ms`);
  }
  await browser.close();
  if (files.length > 1) {
    const cols = Math.min(files.length, Number(process.env.COLS || 4));
    const TW = Number(process.env.TW || 360), TH = Math.round(TW * 16 / 9);
    const args = [];
    files.forEach((f) => args.push("-i", f));
    const rows = Math.ceil(files.length / cols);
    const pad = rows * cols - files.length;
    let fc = files.map((_, i) => `[${i}:v]scale=${TW}:-1,drawtext=text='${times[i]}':x=10:y=10:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.5[v${i}]`).join(";");
    let inputs = files.map((_, i) => `[v${i}]`).join("");
    for (let p = 0; p < pad; p++) { fc += `;color=c=black:s=${TW}x${TH}[p${p}]`; inputs += `[p${p}]`; }
    fc += `;${inputs}xstack=inputs=${rows * cols}:layout=${Array.from({ length: rows * cols }, (_, i) => `${(i % cols) * TW}_${Math.floor(i / cols) * TH}`).join("|")}[o]`;
    execFileSync("ffmpeg", ["-v", "error", "-y", ...args, "-filter_complex", fc, "-map", "[o]", "-frames:v", "1", path.join(out, "sheet.jpg")]);
    console.log("sheet:", path.join(out, "sheet.jpg"));
  }
})();
