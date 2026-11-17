// Compose the cover/thumbnail: a rendered 1080x1920 still + title in the film's caption font.
// Usage: node tools/cover.cjs <background.png> <out.png> "LINE ONE|LINE TWO|*ACCENT LINE*" [titleTopPx=620]
// Lines are separated by "|"; wrap a line in *asterisks* to colour it with the accent.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const [bg, out, title = "NEVER LET HIM|FINISH|*COUNTING*", topArg] = process.argv.slice(2);
const TOP = Number(topArg || 620); // y of the title box (px)
const font = fs.readFileSync(path.join(ROOT, "assets/fonts/poppins-latin-800-normal.woff2")).toString("base64");
const img = fs.readFileSync(path.resolve(bg)).toString("base64");
const lines = title.split("|").map((l) => {
  const accent = /^\*.*\*$/.test(l);
  const text = l.replace(/^\*|\*$/g, "").replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
  return `<div class="l${accent ? " a" : ""}">${text}</div>`;
});

// optional glowing heartbeat line across the frame (ECG_Y = baseline y in px)
const ECG_Y = Number(process.env.ECG_Y || 0);
const ecg = (() => {
  if (!ECG_Y) return "";
  const pts = [];
  const beat = (x) => {
    const g = (c, w, a) => a * Math.exp(-(((x - c) / w) ** 2));
    return g(0.12, 0.04, 0.12) + g(0.28, 0.018, 1) + g(0.315, 0.016, -0.34) + g(0.55, 0.06, 0.22);
  };
  for (let i = 0; i <= 600; i++) {
    const k = i / 600, x = -20 + k * 1120;
    pts.push(`${x.toFixed(1)},${(ECG_Y - beat((k * 2.2 + 0.35) % 1) * 230).toFixed(1)}`);
  }
  const d = "M" + pts.join(" L");
  return `<svg class="ecg" width="1080" height="1920" viewBox="0 0 1080 1920"><path d="${d}" fill="none" stroke="#5dff9a" stroke-width="22" stroke-linejoin="round" opacity=".35" filter="url(#b)"/><path d="${d}" fill="none" stroke="#d9ffe6" stroke-width="7" stroke-linejoin="round"/><defs><filter id="b"><feGaussianBlur stdDeviation="9"/></filter></defs></svg>`;
})();

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:P;src:url(data:font/woff2;base64,${font}) format("woff2");font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#050608}
.bg{position:absolute;inset:0;background:url(data:image/png;base64,${img}) center/cover}
.shade{position:absolute;left:0;right:0;top:${TOP - 60}px;height:640px;
  background:linear-gradient(180deg,rgba(5,6,8,0) 0%,rgba(5,6,8,.45) 35%,rgba(5,6,8,.45) 65%,rgba(5,6,8,0) 100%)}
.t{position:absolute;left:60px;right:60px;top:${TOP}px;height:520px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:4px;font-family:P;font-weight:800;text-align:center}
.l{font-size:132px;line-height:1.0;letter-spacing:-0.01em;color:#fff;
  -webkit-text-stroke:16px #120c08;paint-order:stroke fill;
  text-shadow:0 10px 0 rgba(18,12,8,.85),0 0 40px rgba(0,0,0,.55)}
.l.a{color:#ffb21e;font-size:150px}
.ecg{position:absolute;left:0;top:0}
</style></head><body><div class="bg"></div>${ecg}<div class="shade"></div><div class="t">${lines.join("")}</div></body></html>`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.setContent(html, { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready);
  // shrink any line that would overflow the 960 px text box
  await p.evaluate(() => {
    document.querySelectorAll(".l").forEach((el) => {
      let s = parseFloat(getComputedStyle(el).fontSize);
      while (el.scrollWidth > 960 && s > 60) el.style.fontSize = (s -= 4) + "px";
    });
  });
  await p.screenshot({ path: path.resolve(out) });
  await b.close();
  console.log("cover:", path.resolve(out));
})();
