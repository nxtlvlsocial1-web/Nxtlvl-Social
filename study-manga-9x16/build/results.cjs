// The two study images Canva could not make (credit quota cooldown): a labelled photosynthesis diagram and a one-page
// revision sheet for NCERT Class 10 "Life Processes", in the same clean infographic style as the Canva timeline and
// mind map (white page, rounded pastel cards, navy Inter type, colourful icons). Facts follow the NCERT chapter.
// node build/results.cjs   -> footage/results/4_diagram.png, 5_revision.png (1080 x 1440)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "footage", "results");
const BASE = `
@font-face { font-family: I; src: url("file:///usr/share/fonts/opentype/inter/Inter-Bold.otf"); font-weight: 700; }
@font-face { font-family: I; src: url("file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf"); font-weight: 600; }
@font-face { font-family: I; src: url("file:///usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"); font-weight: 800; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1080px; height: 1440px; background: #fffefc; font-family: I; color: #22284d; position: relative; overflow: hidden; }
.title { margin: 48px 50px 0; padding: 26px 30px 30px; border: 3px solid #22284d; border-radius: 26px; text-align: center; }
.title h1 { font-weight: 800; font-size: 62px; line-height: 1.05; letter-spacing: -.01em; }
.title .u { width: 380px; height: 8px; margin: 16px auto 0; border-radius: 99px; background: #f2735f; }
.foot { position: absolute; left: 0; right: 0; bottom: 40px; text-align: center; font-weight: 700; font-size: 30px; }
.foot span { display: inline-block; padding: 10px 30px; border: 2.5px solid #22284d; border-radius: 16px; }
`;

const DIAGRAM = `<!doctype html><html><head><meta charset="utf-8"><style>${BASE}
.stage { position: absolute; left: 0; right: 0; top: 230px; height: 860px; }
.lab { position: absolute; width: 330px; padding: 18px 22px; border-radius: 20px; font-size: 25px; font-weight: 600; line-height: 1.25; }
.lab b { display: block; font-weight: 800; font-size: 30px; margin-bottom: 4px; }
.eq { position: absolute; left: 50px; right: 50px; top: 1120px; padding: 26px 20px; border-radius: 22px; background: #eaf6ea; border: 2.5px solid #4caf50;
  text-align: center; font-weight: 800; font-size: 30px; }
.eq small { display: block; font-weight: 600; font-size: 23px; margin-top: 8px; color: #3b4370; }
</style></head><body>
<div class="title"><h1>Photosynthesis</h1><div class="u"></div></div>
<div class="stage">
<svg width="1080" height="860" viewBox="0 0 1080 860" style="position:absolute;left:0;top:0">
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="context-stroke"/></marker>
    <linearGradient id="lf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7ed36b"/><stop offset="1" stop-color="#2f9e44"/></linearGradient>
  </defs>
  <!-- sun -->
  <g transform="translate(150,120)"><circle r="58" fill="#ffd43b"/>
    <g stroke="#fab005" stroke-width="9" stroke-linecap="round">${[...Array(12)].map((_, i) => { const t = i * Math.PI / 6; return `<line x1="${Math.cos(t) * 74}" y1="${Math.sin(t) * 74}" x2="${Math.cos(t) * 98}" y2="${Math.sin(t) * 98}"/>`; }).join("")}</g></g>
  <!-- leaf -->
  <path d="M540 700 C 330 640, 300 360, 560 210 C 790 330, 780 620, 540 700 Z" fill="url(#lf)" stroke="#1e7b34" stroke-width="6"/>
  <path d="M540 700 C 545 560, 552 380, 560 225" stroke="#1e7b34" stroke-width="7" fill="none"/>
  ${[300, 380, 460, 540, 610].map((y, i) => `<path d="M${548 + i} ${y + 40} C ${500} ${y + 10}, ${450} ${y}, ${420 + i * 4} ${y - 20}" stroke="#1e7b34" stroke-width="4" fill="none"/><path d="M${552 + i} ${y + 30} C ${600} ${y}, ${650} ${y - 10}, ${680 - i * 4} ${y - 30}" stroke="#1e7b34" stroke-width="4" fill="none"/>`).join("")}
  <!-- stem -->
  <path d="M540 700 L 540 840" stroke="#1e7b34" stroke-width="12" stroke-linecap="round"/>
  <!-- arrows -->
  <path d="M215 190 L 430 330" stroke="#fab005" stroke-width="9" marker-end="url(#a)" fill="none"/>
  <path d="M120 470 L 400 470" stroke="#868e96" stroke-width="9" marker-end="url(#a)" fill="none"/>
  <path d="M540 850 L 540 760" stroke="#339af0" stroke-width="9" marker-end="url(#a)" fill="none"/>
  <path d="M690 300 L 900 210" stroke="#22b8cf" stroke-width="9" marker-end="url(#a)" fill="none"/>
  <path d="M700 560 L 910 620" stroke="#e8590c" stroke-width="9" marker-end="url(#a)" fill="none"/>
</svg>
<div class="lab" style="left:40px;top:250px;background:#fff4cc">Sunlight<b style="display:none"></b>Chlorophyll absorbs light energy</div>
<div class="lab" style="left:40px;top:510px;background:#f1f3f5"><b>CO₂ in</b>Carbon dioxide enters through the stomata</div>
<div class="lab" style="left:600px;top:740px;width:440px;background:#e7f5ff"><b>Water in</b>Water comes up from the roots through the xylem</div>
<div class="lab" style="left:700px;top:30px;background:#e3fafc"><b>Oxygen out</b>Oxygen is released into the air</div>
<div class="lab" style="left:700px;top:420px;background:#fff0e6"><b>Glucose made</b>Stored in the plant as starch</div>
</div>
<div class="eq">6CO₂ + 12H₂O → C₆H₁₂O₆ + 6O₂ + 6H₂O<small>in the presence of sunlight and chlorophyll</small></div>
<div class="foot"><span>NCERT Class 10 Science - Life Processes</span></div>
</body></html>`.replace('<div class="lab" style="left:40px;top:250px;background:#fff4cc">Sunlight<b style="display:none"></b>Chlorophyll absorbs light energy</div>',
  '<div class="lab" style="left:40px;top:250px;background:#fff4cc"><b>Sunlight</b>Chlorophyll absorbs the light energy</div>');

const REVISION = `<!doctype html><html><head><meta charset="utf-8"><style>${BASE}
.title h1 { font-size: 54px; }
.grid { position: absolute; left: 50px; right: 50px; top: 245px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.card { border-radius: 22px; padding: 22px 24px; }
.card h3 { font-weight: 800; font-size: 28px; margin-bottom: 10px; }
.card p, .card li { font-size: 22px; font-weight: 600; line-height: 1.32; }
.card ul, .card ol { padding-left: 26px; }
.card li { margin-bottom: 6px; }
.def { background: #e7f5ff; } .facts { background: #ebfbee; } .form { background: #fff4e6; grid-column: 1 / -1; } .qs { background: #f3f0ff; grid-column: 1 / -1; }
.form .f { text-align: center; font-weight: 800; font-size: 26px; padding: 6px 0; }
.qs li { margin-bottom: 10px; } .qs i { font-style: normal; color: #5f3dc4; font-weight: 700; display: block; }
</style></head><body>
<div class="title"><h1>Life Processes · Revision Sheet</h1><div class="u"></div></div>
<div class="grid">
  <div class="card def"><h3>Key definitions</h3><ul>
    <li><b>Nutrition:</b> taking in food for energy and growth.</li>
    <li><b>Respiration:</b> breaking down food to release energy.</li>
    <li><b>Transportation:</b> carrying food, oxygen and wastes around the body.</li>
    <li><b>Excretion:</b> removing harmful nitrogenous wastes.</li></ul></div>
  <div class="card facts"><h3>5 must-know facts</h3><ol>
    <li>ATP is the energy currency of the cell.</li>
    <li>Villi in the small intestine increase the area for absorption.</li>
    <li>Humans have double circulation: blood passes through the heart twice in one cycle.</li>
    <li>Xylem carries water; phloem carries food.</li>
    <li>The nephron is the filtering unit of the kidney.</li></ol></div>
  <div class="card form"><h3>Must-know formula: respiration</h3>
    <div class="f">Glucose → Pyruvate + energy &nbsp;(in the cytoplasm)</div>
    <div class="f">Pyruvate + O₂ → CO₂ + H₂O + energy &nbsp;(in the mitochondria)</div>
    <p style="text-align:center">Without oxygen: yeast makes ethanol + CO₂; muscles make lactic acid.</p></div>
  <div class="card qs"><h3>3 likely exam questions</h3><ol>
    <li>Why is diffusion not enough to supply oxygen in multicellular organisms like humans?<i>The body is large, so diffusion is too slow to reach every cell.</i></li>
    <li>Give two differences between aerobic and anaerobic respiration.<i>Aerobic uses oxygen and gives CO₂, water and more energy; anaerobic uses no oxygen and gives ethanol or lactic acid and less energy.</i></li>
    <li>What is the function of the nephron?<i>It filters the blood, removes urea as urine and reabsorbs useful substances like glucose and water.</i></li></ol></div>
</div>
<div class="foot"><span>NCERT Class 10 Science - Life Processes</span></div>
</body></html>`;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
  for (const [name, html] of [["4_diagram", DIAGRAM], ["5_revision", REVISION]]) {
    const f = path.join(ROOT, "cache", `${name}.html`);
    fs.writeFileSync(f, html);
    await p.goto("file://" + f);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(200);
    await p.screenshot({ path: path.join(OUT, `${name}.png`) });
    console.log("wrote", name);
  }
  await b.close();
})();
