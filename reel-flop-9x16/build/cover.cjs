// Cover for the hook reel (v13): the reel's own replay moment ("This video already lost you." over the greyed, stamped
// SKIPPED reel), taken from index.html at that instant and re-laid out for a cover: the headline lower and the card
// smaller, so headline, card and stamp all sit inside Instagram's 3:4 profile-grid crop (y 240..1680).
// node build/cover.cjs [OUT.png]
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv[2] || path.join(ROOT, "renders", "nxtlvl_reel-flop_reels_9x16_v13_cover.png");
const T = 7.95; // headline complete, stamp landed, chip in (build/generate.py, intro(): the replay)

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto("file://" + path.join(ROOT, "index.html"));
  await page.waitForFunction(() => window.__timelines && window.__timelines.main && document.fonts.status === "loaded");
  await page.evaluate((t) => {
    const M = window.__timelines.main;
    M.seek(t, false);
    gsap.set("#intro", { scale: 0.5, y: 268, rotation: -3 });
    gsap.set("#rpst", { y: 120, backgroundColor: "#ffffff" });
    gsap.set("#rpch", { y: 90 });
    document.querySelector(".rph").style.top = "280px";
  }, T);
  await page.waitForTimeout(300);
  await page.screenshot({ path: OUT });
  await browser.close();
  console.log("wrote", OUT);
})();
