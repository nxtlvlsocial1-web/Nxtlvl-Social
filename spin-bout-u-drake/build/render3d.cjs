// Pre-renders the 3D scenes (plan/g3d.json) to assets/video/g3d/<id>.mp4: every 20 fps frame is drawn in headless
// Chromium (SwiftShader WebGL), read back from the canvas (no page screenshots: those deadlock with SwiftShader WebGL)
// and encoded with ffmpeg. The 3D frame is 1240x1240, the clip's holder overhangs the frame by 80 px each side so the
// layer camera can move it without showing an edge.
//   node build/render3d.cjs [id ...]      (from the project root; serves the project on 127.0.0.1:8766 itself)
const { chromium } = require("playwright");
const http = require("http"), fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const ROOT = path.resolve(__dirname, "..");
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".ttf": "font/ttf" };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]));
  fs.readFile(f, (err, data) => { if (err) { res.writeHead(404); res.end(); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(data); });
}).listen(8766, "127.0.0.1");
(async () => {
  const only = process.argv.slice(2);
  const scenes = JSON.parse(fs.readFileSync(path.join(ROOT, "plan", "g3d.json"))).filter((s) => !only.length || only.includes(s.id));
  const b = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const p = await b.newPage();
  p.on("pageerror", (e) => console.log("pageerror", String(e).slice(0, 300)));
  await p.goto("http://127.0.0.1:8766/build/g3d_page.html");
  await p.waitForFunction(() => window.__g3dDraw, null, { timeout: 120000 });
  await p.evaluate(() => window.__g3dResize && window.__g3dResize(1240));
  const outDir = path.join(ROOT, "assets", "video", "g3d");
  fs.mkdirSync(outDir, { recursive: true });
  for (const s of scenes) {
    const dir = path.join(ROOT, "cache", "g3d", s.id);
    fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const n = Math.round((s.t1 - s.t0) * 20);
    for (let f = 0; f < n; f++) {
      const url = await p.evaluate((t) => { window.__g3dDraw(t); return window.__g3dCanvas.toDataURL("image/png"); }, s.t0 + f / 20 + 0.0001);
      fs.writeFileSync(path.join(dir, `f${String(f).padStart(4, "0")}.png`), Buffer.from(url.split(",")[1], "base64"));
    }
    execFileSync("ffmpeg", ["-v", "error", "-y", "-framerate", "20", "-i", path.join(dir, "f%04d.png"), "-c:v", "libx264", "-preset", "slow",
      "-crf", "14", "-pix_fmt", "yuv420p", "-r", "20", path.join(outDir, `${s.id}.mp4`)]);
    console.log(s.id, s.kind, n, "frames");
  }
  await b.close(); server.close();
})();
