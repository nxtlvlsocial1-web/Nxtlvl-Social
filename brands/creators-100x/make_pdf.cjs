// Creators 100X branded PDF maker: a content JSON -> a phone-friendly PDF (4:5 pages, 1080 x 1350) in the brand
// (brand.md): the soft lime / pink corner gradient, black + hot pink + lime, Inter, the logo on the cover and in every
// footer. Use it for every Creators 100X lead magnet / automation PDF.
//
//   node brands/creators-100x/make_pdf.cjs CONTENT.json OUT.pdf
//
// CONTENT.json:
// { "title": ["20 HOOKS", "THAT WORK"],      cover title lines; wrap a word in *stars* for hot pink
//   "kicker": "Free swipe file",             small label above the title
//   "subtitle": "...", "tagline": "...",     cover lines under the title
//   "blocks": [                              the pages after the cover, in order
//     { "type": "text", "heading": "...", "intro": "...", "steps": [["title", "body"], ...], "note": "..." },
//     { "type": "cards", "heading": "...", "per_page": 4,
//       "items": [{ "tag": "Result first", "line": "I got [result] in [time]...", "example": "...", "why": "..." }] },
//     { "type": "checklist", "heading": "...", "items": ["...", ...], "closing": "..." } ] }
// In card lines, [square brackets] mark the blanks to fill in (highlighted lime).
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const D = __dirname;
const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) {
  console.error("usage: node make_pdf.cjs CONTENT.json OUT.pdf");
  process.exit(1);
}
const C = JSON.parse(fs.readFileSync(inPath, "utf8"));
const W = 1080, H = 1350;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const pink = (s) => esc(s).replace(/\*([^*]+)\*/g, '<span class="pk">$1</span>');
const blanks = (s) => esc(s).replace(/\[([^\]]+)\]/g, '<span class="bl">$1</span>');
const logo = "file://" + path.join(D, "logo.png");
const mark = "file://" + path.join(D, "logo-mark.png");

const pages = [];
let pageNo = 1;
const foot = () => `<div class="foot"><img src="${mark}"><span>Creators 100X</span><b>${String(++pageNo).padStart(2, "0")}</b></div>`;

// cover
pages.push(`<section class="pg cover"><img class="clogo" src="${logo}">
  <div class="ck">${esc(C.kicker || "")}</div>
  <h1>${(C.title || []).map((l) => `<span>${pink(l)}</span>`).join("")}</h1>
  <p class="csub">${esc(C.subtitle || "")}</p>
  <div class="ctag"><i></i>${esc(C.tagline || "")}</div></section>`);

let n = 0;
for (const b of C.blocks || []) {
  if (b.type === "text") {
    const steps = (b.steps || []).map(([t, body], i) => `<div class="st"><b>${i + 1}</b><div><h3>${esc(t)}</h3><p>${blanks(body)}</p></div></div>`).join("");
    pages.push(`<section class="pg"><div class="body"><h2>${pink(b.heading)}</h2>${b.intro ? `<p class="lead">${esc(b.intro)}</p>` : ""}
      <div class="steps">${steps}</div>${b.note ? `<div class="note">${blanks(b.note)}</div>` : ""}</div>${foot()}</section>`);
  } else if (b.type === "cards") {
    const per = b.per_page || 4;
    for (let i = 0; i < b.items.length; i += per) {
      const cards = b.items.slice(i, i + per).map((it) => {
        n += 1;
        return `<div class="card"><div class="ch"><b class="num">${String(n).padStart(2, "0")}</b><span class="tag">${esc(it.tag)}</span></div>
          <p class="line">${blanks(it.line)}</p>
          <p class="ex"><em>Example</em>${esc(it.example)}</p>
          <p class="why"><em>Why it works</em>${esc(it.why)}</p></div>`;
      }).join("");
      const first = i === 0;
      pages.push(`<section class="pg"><div class="body"><h2 class="sm">${pink(b.heading)}${first ? "" : ` <span class="cont">(continued)</span>`}</h2><div class="cards">${cards}</div></div>${foot()}</section>`);
    }
  } else if (b.type === "checklist") {
    const items = b.items.map((t) => `<li><i></i><span>${blanks(t)}</span></li>`).join("");
    pages.push(`<section class="pg last"><div class="body" data-limit="490"><h2>${pink(b.heading)}</h2><ul class="chk">${items}</ul>
      ${b.closing ? `<p class="closing">${pink(b.closing)}</p>` : ""}</div><img class="elogo" src="${logo}">${foot()}</section>`);
  }
}

const font = (w) => `@font-face { font-family: "Inter"; font-weight: ${w}; src: url("file://${path.join(D, "fonts", `inter-latin-${w}-normal.woff2`)}"); }`;
const css = `
${font(600)} ${font(700)} ${font(800)}
@page { size: ${W}px ${H}px; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { background: #fdf4f4; font-family: Inter, sans-serif; color: #101111; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.pg { position: relative; width: ${W}px; height: ${H}px; overflow: hidden; padding: 96px 90px 150px; page-break-after: always;
  background:
    radial-gradient(60% 45% at 0% 0%, rgba(204,251,121,.85), rgba(204,251,121,0) 70%),
    radial-gradient(60% 45% at 100% 0%, rgba(254,112,179,.75), rgba(254,112,179,0) 70%),
    radial-gradient(60% 45% at 0% 100%, rgba(254,121,186,.7), rgba(254,121,186,0) 70%),
    radial-gradient(60% 45% at 100% 100%, rgba(203,251,144,.8), rgba(203,251,144,0) 70%),
    #fdf4f4; }
.pg:not(.cover) { background:
    radial-gradient(45% 30% at 100% 0%, rgba(254,112,179,.45), rgba(254,112,179,0) 70%),
    radial-gradient(45% 30% at 0% 100%, rgba(204,251,121,.55), rgba(204,251,121,0) 70%),
    #fdf6f5; }
.pk { color: #fd0b68; }
.bl { background: #ccfb79; border-radius: 10px; padding: 0 10px; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
/* cover */
.cover { display: flex; flex-direction: column; justify-content: center; padding: 90px; }
.clogo { position: absolute; left: 90px; top: 90px; width: 330px; }
.ck { display: inline-block; align-self: flex-start; padding: 12px 26px; border-radius: 999px; background: #101111; color: #ccfb79; font-weight: 700; font-size: 30px; letter-spacing: .06em; text-transform: uppercase; }
h1 { margin-top: 34px; font-weight: 800; font-size: 150px; line-height: .92; letter-spacing: -.045em; }
h1 span { display: block; }
.csub { margin-top: 46px; font-size: 42px; font-weight: 600; line-height: 1.3; color: #2b2b2b; max-width: 860px; }
.ctag { position: absolute; left: 90px; bottom: 96px; display: flex; align-items: center; gap: 16px; font-size: 30px; font-weight: 700; }
.ctag i { width: 18px; height: 18px; border-radius: 50%; background: #fd0b68; box-shadow: 0 0 0 7px rgba(253,11,104,.18); }
/* pages */
h2 { font-weight: 800; font-size: 70px; line-height: 1.02; letter-spacing: -.035em; }
h2.sm { font-size: 54px; }
.cont { font-size: 30px; font-weight: 600; color: #8a8580; letter-spacing: 0; }
.lead { margin-top: 24px; font-size: 32px; font-weight: 600; line-height: 1.4; color: #3a3a3a; }
.steps { margin-top: 36px; display: flex; flex-direction: column; gap: 22px; }
.st { display: flex; gap: 28px; align-items: flex-start; padding: 28px 34px; border-radius: 36px; background: rgba(255,255,255,.78); box-shadow: 0 18px 50px rgba(16,17,17,.07); }
.st > b { flex: none; width: 74px; height: 74px; border-radius: 22px; background: #101111; color: #ccfb79; display: grid; place-items: center; font-size: 40px; font-weight: 800; }
.st h3 { font-size: 36px; font-weight: 800; letter-spacing: -.02em; }
.st p { margin-top: 8px; font-size: 28px; font-weight: 600; line-height: 1.45; color: #3a3a3a; }
.note { margin-top: 28px; padding: 26px 34px; border-radius: 30px; background: #101111; color: #fff; font-size: 28px; font-weight: 600; line-height: 1.45; }
.note .bl { color: #101111; }
.cards { margin-top: 36px; display: flex; flex-direction: column; gap: 28px; }
.card { padding: 34px 38px 32px; border-radius: 32px; background: rgba(255,255,255,.84); box-shadow: 0 16px 44px rgba(16,17,17,.07); }
.ch { display: flex; align-items: center; gap: 18px; }
.num { font-size: 40px; font-weight: 800; color: #fd0b68; letter-spacing: -.02em; }
.tag { padding: 6px 18px; border-radius: 999px; background: #101111; color: #ccfb79; font-size: 22px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; }
.line { margin-top: 16px; font-size: 40px; font-weight: 800; line-height: 1.3; letter-spacing: -.015em; }
.ex, .why { margin-top: 14px; font-size: 27px; font-weight: 600; line-height: 1.4; color: #3a3a3a; }
.ex em, .why em { display: inline-block; margin-right: 12px; font-style: normal; font-weight: 800; color: #101111; }
.why { color: #6a6560; margin-top: 6px; }
.chk { margin-top: 46px; list-style: none; display: flex; flex-direction: column; gap: 26px; }
.chk li { display: flex; gap: 26px; align-items: flex-start; font-size: 36px; font-weight: 700; line-height: 1.35; }
.chk li i { flex: none; margin-top: 6px; width: 42px; height: 42px; border-radius: 12px; border: 5px solid #101111; background: #fff; }
.closing { margin-top: 56px; font-size: 46px; font-weight: 800; line-height: 1.2; letter-spacing: -.02em; }
.elogo { position: absolute; left: 90px; bottom: 150px; width: 300px; }
.foot { position: absolute; left: 90px; right: 90px; bottom: 56px; display: flex; align-items: center; gap: 14px; font-size: 24px; font-weight: 700; color: #4a4642; }
.foot img { width: 44px; }
.foot b { margin-left: auto; font-weight: 800; color: #101111; }
`;

const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${pages.join("")}</body></html>`;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const tmp = path.join(path.dirname(path.resolve(outPath)), ".pdf_build.html");
  fs.writeFileSync(tmp, html);
  await page.goto("file://" + tmp);
  await page.evaluate(() => document.fonts.ready);
  const fitted = await page.evaluate(([H]) => {
    const out = [];
    document.querySelectorAll(".pg").forEach((pg, i) => {
      const body = pg.querySelector(".body");
      if (!body) return;
      const limit = pg.getBoundingClientRect().top + H - Number(body.dataset.limit || 130);
      let z = 1;
      while (body.getBoundingClientRect().bottom > limit && z > .6) { z -= .02; body.style.zoom = z; }
      if (z < 1) out.push(`page ${i + 1}: ${Math.round(z * 100)}%`);
    });
    return out;
  }, [H]);
  if (fitted.length) console.log("fitted to the page:", fitted.join(", "));
  await page.pdf({ path: outPath, width: `${W}px`, height: `${H}px`, printBackground: true, preferCSSPageSize: true });
  if (process.argv.includes("--png")) {      // page previews for checking
    const n = await page.evaluate(() => document.querySelectorAll(".pg").length);
    for (let i = 0; i < n; i++) {
      await page.evaluate((k) => window.scrollTo(0, k * 1350), i);
      await page.screenshot({ path: outPath.replace(/\.pdf$/, `_p${i + 1}.png`), clip: { x: 0, y: i * H, width: W, height: H }, fullPage: true });
    }
  }
  fs.unlinkSync(tmp);
  await browser.close();
  console.log(`wrote ${outPath}: ${pages.length} pages`);
})();
