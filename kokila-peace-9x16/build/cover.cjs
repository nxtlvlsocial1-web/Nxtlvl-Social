// Cover for the Dr Kokila reel: the hook question over Deepinder wearing the Temple device (Raj Shamani podcast,
// cut straight from the original screen recording) and Dr Kokila below, in the reel's navy / blue / yellow and Inter.
// Headline, device and both faces sit inside Instagram's 3:4 profile-grid crop (y 240..1680).
// node build/cover.cjs [OUT.png]
const path = require("path");
const fs = require("fs");
const { execFileSync } = require("child_process");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv[2] || path.join(ROOT, "renders", "nxtlvl_kokila-peace_reels_9x16_v1_cover.png");
const W = path.join(ROOT, "cache", "cov");
fs.mkdirSync(W, { recursive: true });
fs.mkdirSync(path.dirname(OUT), { recursive: true });
const ff = (args) => execFileSync("ffmpeg", ["-v", "error", "-y", ...args]);

// Deepinder at 46.0 s of the recording: facing the camera, mouth closed, the device on his temple
const DEEP_T = 46.0, DEEP = [1346, 773, 917, 0];          // crop w, h, x, y in the 2868x1320 recording
ff(["-ss", String(DEEP_T), "-i", path.join(ROOT, "footage", "podcast_rec.mp4"), "-frames:v", "1", "-vf",
    `crop=${DEEP.join(":")},scale=1080:620:flags=lanczos,eq=brightness=0.07:contrast=1.16:saturation=1.15:gamma=1.12,unsharp=5:5:0.4`,
    path.join(W, "deep.png")]);
// Dr Kokila at 45.5 s of the cut: eyes to the lens, a slight smile
ff(["-ss", "45.5", "-i", path.join(ROOT, "assets", "video", "tight.mp4"), "-frames:v", "1", "-vf",
    "crop=1080:740:0:620", path.join(W, "kokila.png")]);

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Inter; font-weight: 700; src: url("../../assets/fonts/inter-latin-700-normal.woff2"); }
@font-face { font-family: Inter; font-weight: 800; src: url("../../assets/fonts/inter-latin-800-normal.woff2"); }
* { margin: 0; box-sizing: border-box; }
body { width: 1080px; height: 1920px; overflow: hidden; background: #0E1A3A; font-family: Inter; }
.bg { position: absolute; inset: 0 0 auto 0; height: 560px;
      background: radial-gradient(120% 90% at 50% 0%, #2448E8 0%, #13245F 55%, #0E1A3A 100%); }
.head { position: absolute; left: 56px; right: 56px; top: 262px; color: #fff; font-weight: 800; font-size: 86px;
        line-height: 1.04; letter-spacing: -0.02em; text-align: center; }
.head .p { background: #FFD23F; color: #0E1A3A; border-radius: 16px; padding: 0 14px; }
.head em { font-style: normal; color: #FFD23F; }
.panel { position: absolute; left: 0; width: 1080px; overflow: hidden; }
.panel img { display: block; width: 1080px; }
#deep { top: 560px; height: 620px; }
#kok { top: 1180px; height: 740px; }
.seam { position: absolute; left: 0; width: 1080px; height: 8px; background: linear-gradient(90deg, #2448E8, #FFD23F, #2448E8); z-index: 3; }
.ring { position: absolute; width: 118px; height: 118px; border: 7px solid #FFD23F; border-radius: 50%;
        box-shadow: 0 0 0 4px rgba(14,26,58,.35), 0 0 34px rgba(255,210,63,.55); z-index: 4; }
.tag { position: absolute; padding: 12px 22px; border-radius: 999px; background: #FFD23F; color: #0E1A3A;
       font-weight: 800; font-size: 34px; z-index: 4; white-space: nowrap; }
.credit { position: absolute; right: 22px; top: 578px; padding: 7px 14px; border-radius: 999px; background: rgba(0,0,0,.55);
          color: #fff; font-size: 24px; font-weight: 700; z-index: 4; }
.name { position: absolute; left: 44px; top: 1560px; padding: 14px 26px 16px; border-radius: 20px; background: #fff; color: #0E1A3A; z-index: 4; }
.name span { display: block; font-size: 22px; font-weight: 800; color: #2448E8; letter-spacing: .1em; text-transform: uppercase; }
.name b { display: block; font-size: 44px; font-weight: 800; }
</style></head><body>
<div class="bg"></div>
<div class="head">Can an <span class="p">₹85,000</span> device measure your <em>peace&nbsp;of&nbsp;mind?</em></div>
<div class="panel" id="deep"><img src="deep.png"></div>
<div class="panel" id="kok"><img src="kokila.png"></div>
<div class="seam" style="top:556px"></div><div class="seam" style="top:1176px"></div>
<div class="ring" id="ring"></div><div class="tag" id="tag">The Temple device</div>
<div class="credit">Source: Raj Shamani podcast</div>
<div class="name"><span>Doctor's take</span><b>Dr S Kokila</b></div>
</body></html>`;
fs.writeFileSync(path.join(W, "cover.html"), html);

// device centre in the 1080x620 panel (measured on the frame), and the tag beside it
const DEV = { x: +(process.env.DEV_X || 646), y: +(process.env.DEV_Y || 306) };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto("file://" + path.join(W, "cover.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate((d) => {
    const r = document.getElementById("ring"), t = document.getElementById("tag");
    r.style.left = d.x - 59 + "px"; r.style.top = 560 + d.y - 59 + "px";
    t.style.left = d.x + 80 + "px"; t.style.top = 560 + d.y - 30 + "px";
    if (d.x + 80 + t.offsetWidth > 1050) { t.style.left = d.x - 80 - t.offsetWidth + "px"; }
  }, DEV);
  await page.waitForTimeout(200);
  await page.screenshot({ path: OUT });
  await browser.close();
  console.log("wrote", OUT);
})();
