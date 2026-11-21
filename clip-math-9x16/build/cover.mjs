// Renders cover/cover.html to out/cover.png at exactly 1080x1920 with the preinstalled Playwright.
// Run from the project root: node build/cover.mjs
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const root = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.join(root, "cover/cover.html"));
await p.evaluate(() => document.fonts.ready);
const box = await p.evaluate(() => [...document.querySelectorAll(".wrap > span")].map((e) => { const r = e.getBoundingClientRect(); return [e.className, Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; }));
console.log(JSON.stringify(box));
await p.screenshot({ path: path.join(root, "out/cover.png") });
await b.close();
console.log("wrote out/cover.png");
