// Screenshot build/cover.html to the reel cover PNG. Run from the project root: node build/cover.mjs
import { createRequire } from "module";
import path from "path";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto("file://" + path.join(root, "build", "cover.html"));
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(root, "renders", "vitonnix_biotin_reels_9x16_v1_cover.png") });
await browser.close();
console.log("cover written");
