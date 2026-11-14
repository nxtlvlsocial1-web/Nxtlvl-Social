// Cree 3D model sheet: everything a 3D artist needs to build, rig and animate Creedom's mascot (Creedom's own art).
// Story concepts and the recommended script + shot list, art direction, the Cree character sheet (Creedom's own mascot:
// the client's 3D render poses from creedom-explainer-9x16), worlds and props, render spec and an AI prompt pack.
// Creedom look: blush-white paper, ink #0b0b0b, the wordmark's magenta -> pink -> coral, Manrope + Fraunces italic.
// Phone-friendly 1080 x 1350 pages, rasterised so every viewer draws them the same.
// node build/guide.cjs   -> renders/creedom_cree-3d-model-sheet.pdf (page images in cache/guide/)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "renders", "creedom_cree-3d-model-sheet.pdf");
const A = (p) => "file://" + path.join(ROOT, p);
const PAGES = [];
const TOTAL = 7;

function page({ kicker, title, body, cls = "" }) {
  const n = PAGES.length + 1;
  PAGES.push(`<section class="pg ${cls}"><header><div class="kick">${kicker}</div><h2>${title}</h2>
    <img class="wm" src="${A("assets/img/wordmark.png")}"></header>
    <main>${body}</main>
    <footer><span>CREE · 3D MODEL SHEET</span><span>${String(n).padStart(2, "0")} / ${String(TOTAL).padStart(2, "0")}</span></footer></section>`);
}
const steps = (items) => `<ol class="steps">${items.map((s) => `<li><span class="bd">${s[0]}</span><p>${s[1]}</p></li>`).join("")}</ol>`;
const note = (t, c = "") => `<div class="note ${c}">${t}</div>`;
const kv = (rows) => `<div class="kv">${rows.map(([k, v]) => `<div class="k">${k}</div><div class="v">${v}</div>`).join("")}</div>`;
const pose = (n, cap) => `<figure><img src="${A(`assets/img/poses/${n}.png`)}"><figcaption>${cap}</figcaption></figure>`;

const img = (p, cls = "") => `<img class="${cls}" src="${A(p)}">`;
// 1 cover
PAGES.push(`<section class="pg cover"><div class="cglow"></div><div class="cwrap">
  <img class="cwm" src="${A("assets/img/wordmark.png")}">
  <div class="ckick">REFERENCE FOR THE 3D BUILD</div>
  <h1>Cree<br><em>model sheet</em></h1>
  <img class="chero" src="${A("assets/img/mascot_src.png")}">
  <div class="csub">How Cree looks, measures and moves, and how to <em>build him in 3D.</em></div>
  <div class="cpills"><span>PROPORTIONS</span><span>COLOURS</span><span>13 POSES</span><span>RIG PLAN</span></div>
</div></section>`);

// 2 how he was made
page({ kicker: "01 · HOW CREE WAS MADE SO FAR", title: 'What exists <em>today</em>',
  body: steps([
    ["1", "<b>The original:</b> one 3D-style render of Cree waving (00_cree_original.png). This is the master reference."],
    ["2", "<b>13 poses</b> were generated from that image as the reference, as 2D renders of the same character, then cut out onto transparent backgrounds (poses/)."],
    ["3", "<b>In the reels he is animated in 2D:</b> pose swaps on the script beats, squash and stretch, a 2-frame walk cycle, blinks and a sweat drop drawn on top."],
    ["4", "<b>An older cut-out puppet</b> splits him into layers: body, wings, beak and feet (rig_layers/), with the face redrawn so he can emote."],
  ]) + note("<b>There is no 3D mesh yet.</b> For a true 3D render he has to be modelled (or generated with an image-to-3D tool) from these references, then rigged. Pages 5 to 7 show how.", "warn") });

// 3 proportions
page({ kicker: "02 · PROPORTIONS", title: 'Measured from<br><em>the front</em>',
  body: img("cache/pack/01_proportions_front.png", "wide") + kv([
    ["Overall", "As wide as he is tall (arms included). One egg-shaped body, head and body in one form, no neck."],
    ["Eyes", "Centres 31% down from the top; each eye about 23% of his width; centres 36% of his width apart."],
    ["Beak", "Centred, just below the eye line, between the eyes. Small, rounded, open in a smile."],
    ["Arms and feet", "Short rounded wing-arms at about two-thirds of his height; two stubby oval feet set slightly apart."],
  ]) });

// 4 colours and materials
page({ kicker: "03 · COLOURS AND MATERIALS", title: 'Surface and <em>colour</em>',
  body: `<div class="swatches">${[["#F343A2", "Body base"], ["#E0187E", "Body shadow"], ["#FF8CC6", "Body highlight"], ["#FFC21A", "Beak and feet"], ["#F2A516", "Beak and feet shadow"], ["#D81F3C", "Mouth inside"], ["#FFFFFF", "Eye white and catchlights"], ["#0B0B0B", "Pupil"]].map(([c, n]) => `<div><i style="background:${c}"></i><b>${c}</b><span>${n}</span></div>`).join("")}</div>`
    + kv([
      ["Body", "Soft matte, velvety plush-toy surface with light subsurface scattering so the pink glows at the edges. No feathers, no fur strands."],
      ["Eyes", "Glossy: clear coat over a black pupil with two white catchlights (one large upper right, one small lower left). Pale pink rim around the white."],
      ["Beak and feet", "Semi-gloss, like smooth vinyl. Slightly warmer than the body light."],
      ["Lighting test", "Warm key, soft fill, pink rim. He should read as a premium designer toy."],
    ]) });

// 5 pose library
const P13 = [["stand", "Stand"], ["walk", "Walk A"], ["pass", "Walk B"], ["wave", "Wave"], ["point", "Point"], ["present", "Present"], ["cheer", "Cheer"], ["shock", "Shock"], ["sad", "Sad"], ["mag", "Magnifier"], ["phone", "Phone"], ["think", "Think"], ["proud", "Proud"]];
page({ kicker: "04 · POSE LIBRARY", title: '13 poses <em>on model</em>',
  body: `<div class="p13">${P13.map(([n, c]) => pose(n, c)).join("")}</div>`
    + note("Use these as acting and expression targets for the 3D rig. Walk A and Walk B are the two frames of his walk.") });

// 6 build and rig
page({ kicker: "05 · BUILD AND RIG", title: 'Building him <em>in 3D</em>',
  body: steps([
    ["1", "<b>Block out:</b> one sphere scaled to an egg (slightly heavier at the bottom), two eye spheres set into the face, a rounded cone for the beak, flattened capsules for the arms, two ovals for the feet."],
    ["2", "<b>Sculpt</b> soft, toy-like forms; keep the silhouette clean from the front and the side. Match the pose sheet before adding detail."],
    ["3", "<b>Rig:</b> root, a body bone with squash-and-stretch, 2 arm bones each, 2 foot bones, eye bones for look direction, blend shapes for blink, lids, brows, smile and beak open."],
    ["4", "<b>Animate</b> with bouncy timing: anticipation, squash on landing, a small waddle. Arms act like hands; he never flaps or flies."],
    ["5", "<b>Check every shot</b> against the original image: colour, eye size and the no-neck egg shape are the parts people recognise."],
  ]) });

// 7 faster route + files
page({ kicker: "06 · FASTER ROUTE AND THE FILES", title: 'Image-to-3D and<br><em>what is in the pack</em>',
  body: steps([
    ["1", "<b>Image-to-3D:</b> feed 00_cree_original.png (or stand.png) into an image-to-3D tool to get a starter mesh (GLB). Expect to clean up the eyes and beak and re-topologise before rigging."],
    ["2", "<b>Then rig and animate</b> as on the previous page. Generated meshes are a starting point, not final quality."],
  ]) + kv([
    ["00 original", "<b>00_cree_original.png</b>: the master reference (waving)."],
    ["01 proportions", "<b>01_proportions_front.png</b>: measured front view."],
    ["poses/", "13 transparent poses + poses_eyes_and_boxes.json (eye centres and sizes per pose, on an 820 x 820 canvas, feet at y 800)."],
    ["rig_layers/", "The 2D cut-out puppet layers (body, wings, beak, feet)."],
    ["brand/", "Cree icon and the Creedom wordmark for end cards."],
    ["Story guide", "<b>creedom_3d-storytelling-guide.pdf</b>: story, shot list and art direction."],
  ]) });

const CSS = `
@font-face { font-family: M; font-weight: 800; src: url("${A("assets/fonts/manrope-latin-800-normal.woff2")}"); }
@font-face { font-family: M; font-weight: 700; src: url("${A("assets/fonts/manrope-latin-700-normal.woff2")}"); }
@font-face { font-family: M; font-weight: 500; src: url("${A("assets/fonts/manrope-latin-500-normal.woff2")}"); }
@font-face { font-family: F; font-style: italic; src: url("${A("assets/fonts/fraunces-latin-600-italic.woff2")}"); }
@font-face { font-family: J; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --m: 80px; --mag: #e0187e; --pink: #f343a2; --coral: #e68b70; --ink: #0b0b0b; --paper: #fff7fa; --mute: #5b4a55; }
body { font-family: M; color: var(--ink); background: var(--paper); }
.pg { position: relative; width: 1080px; height: 1350px; overflow: hidden; display: flex; flex-direction: column;
  background: radial-gradient(60% 30% at 100% 0%, rgba(243,67,162,.14), transparent 70%), radial-gradient(60% 30% at 0% 100%, rgba(230,139,112,.14), transparent 70%), var(--paper); }
header { position: relative; flex: none; padding: 70px var(--m) 30px; }
.wm { position: absolute; right: var(--m); top: 72px; height: 40px; }
.kick { display: inline-block; font-family: J; font-size: 21px; letter-spacing: .16em; color: #fff; background: var(--mag); padding: 8px 14px; border-radius: 8px; margin-bottom: 20px; }
h2 { font-weight: 800; font-size: 62px; line-height: 1.04; letter-spacing: -.03em; }
h2 em, h1 em, .csub em { font-family: F; font-style: italic; font-weight: 600; color: var(--mag); letter-spacing: -.01em; }
main { flex: 1; min-height: 0; padding: 20px var(--m) 20px; display: flex; flex-direction: column; gap: 26px; overflow: hidden; }
footer { flex: none; margin: 0 var(--m); padding: 20px 0 32px; border-top: 1.5px solid rgba(11,11,11,.12); display: flex; justify-content: space-between;
  font-family: J; font-size: 17px; letter-spacing: .14em; color: rgba(11,11,11,.45); }
.bd { flex: none; min-width: 52px; height: 52px; padding: 0 12px; border-radius: 14px; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; font-size: 25px; color: #fff;
  background: linear-gradient(135deg, var(--pink), var(--coral)); }
.steps { list-style: none; display: flex; flex-direction: column; gap: 24px; }
.steps li { display: grid; grid-template-columns: 52px 1fr; column-gap: 24px; align-items: start; }
.steps p { font-size: 29px; line-height: 1.34; font-weight: 500; color: #2a1f26; padding-top: 6px; }
b { font-weight: 800; color: var(--ink); }
.note { padding: 22px 26px; border-radius: 18px; font-size: 25px; line-height: 1.38; color: #3a2b34; background: rgba(243,67,162,.08); border-left: 6px solid var(--pink); }
.note.warn { background: rgba(230,139,112,.12); border-left-color: var(--coral); }
.kv { display: grid; grid-template-columns: 210px 1fr; gap: 18px 26px; align-items: start; }
.kv .k { font-family: J; font-size: 20px; letter-spacing: .1em; color: var(--mag); padding-top: 7px; text-transform: uppercase; }
.kv .v { font-size: 27px; line-height: 1.36; font-weight: 500; color: #2a1f26; }
.sw { display: inline-block; width: 34px; height: 34px; border-radius: 9px; vertical-align: middle; margin-right: 6px; border: 2px solid rgba(11,11,11,.1); }
.cons { display: flex; flex-direction: column; gap: 14px; }
.con { padding: 18px 24px; border-radius: 22px; background: #fff; border: 2px solid rgba(11,11,11,.08); }
.con.rec { border-color: var(--pink); box-shadow: 0 16px 40px rgba(243,67,162,.18); }
.ch { display: flex; align-items: center; gap: 18px; margin-bottom: 10px; }
.ch b { font-size: 34px; letter-spacing: -.02em; }
.ch i { margin-left: auto; font-style: normal; font-family: J; font-size: 17px; letter-spacing: .14em; color: #fff; background: var(--mag); padding: 6px 12px; border-radius: 8px; }
.con p { font-size: 24px; line-height: 1.38; color: #3a2b34; font-weight: 500; }
.vo { display: flex; flex-direction: column; gap: 14px; }
.vl { display: grid; grid-template-columns: 96px 1fr; gap: 20px; align-items: baseline; padding: 14px 0; border-bottom: 1.5px solid rgba(11,11,11,.08); }
.vl span { font-family: J; font-size: 22px; color: var(--mag); }
.vl p { font-size: 30px; line-height: 1.3; font-weight: 700; }
.shots { display: flex; flex-direction: column; gap: 12px; }
.shot { padding: 16px 22px; border-radius: 20px; background: #fff; border: 2px solid rgba(11,11,11,.07); }
.sh1 { display: flex; align-items: center; gap: 16px; margin-bottom: 7px; }
.sh1 em { font-style: normal; font-family: J; font-size: 21px; color: var(--mag); }
.shot p { font-size: 21px; line-height: 1.3; font-weight: 500; color: #2a1f26; }
.shot q { display: block; margin-top: 5px; font-family: F; font-style: italic; font-size: 23px; color: var(--mute); quotes: none; }
.poses { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
figure { background: #fff; border-radius: 20px; border: 2px solid rgba(11,11,11,.07); padding: 10px 10px 12px; text-align: center; }
figure img { width: 100%; height: 190px; object-fit: contain; }
figcaption { font-family: J; font-size: 18px; letter-spacing: .1em; color: var(--mag); text-transform: uppercase; }
.dd { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
.dd > div { padding: 24px 26px; border-radius: 20px; }
.do { background: rgba(47,191,113,.1); border: 2px solid rgba(47,191,113,.45); }
.dont { background: rgba(230,60,90,.08); border: 2px solid rgba(230,60,90,.4); }
.dd b { font-family: J; font-size: 22px; letter-spacing: .14em; }
.dd ul { margin: 12px 0 0 26px; } .dd li { font-size: 25px; line-height: 1.36; margin: 6px 0; font-weight: 500; color: #2a1f26; }
.check { list-style: none; } .check li { display: grid; grid-template-columns: 38px 1fr; gap: 20px; align-items: center; padding: 12px 0; border-bottom: 1.5px solid rgba(11,11,11,.08); }
.check i { width: 38px; height: 38px; border-radius: 10px; border: 3px solid var(--pink); } .check p { font-size: 26px; font-weight: 700; }
.pr { padding: 22px 26px; border-radius: 18px; background: #fff; border: 2px dashed rgba(224,24,126,.45); }
.prl { font-family: J; font-size: 18px; letter-spacing: .14em; color: var(--mag); margin-bottom: 10px; }
.pr p { font-family: J; font-size: 21px; line-height: 1.5; color: #2a1f26; }
.cover { background: var(--paper); }
.cglow { position: absolute; inset: 0; background: radial-gradient(55% 35% at 50% 58%, rgba(243,67,162,.35), transparent 70%), radial-gradient(60% 30% at 100% 0%, rgba(230,139,112,.25), transparent 70%); }
.cwrap { position: relative; height: 100%; padding: 90px var(--m); display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; }
.cwm { height: 74px; }
.ckick { font-family: J; font-size: 20px; letter-spacing: .14em; color: #fff; background: var(--mag); padding: 9px 16px; border-radius: 8px; }
h1 { font-weight: 800; font-size: 108px; line-height: 1; letter-spacing: -.04em; }
.chero { width: 470px; height: 470px; object-fit: contain; filter: drop-shadow(0 30px 50px rgba(224,24,126,.35)); }
.csub { font-size: 38px; font-weight: 700; line-height: 1.25; max-width: 860px; }
.cpills { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
.cpills span { padding: 9px 16px; border-radius: 999px; font-family: J; font-size: 19px; letter-spacing: .08em; border: 2px solid var(--pink); color: var(--mag); background: #fff; }
.wide { width: 100%; height: 500px; object-fit: contain; background: #fff7fa; border-radius: 20px; border: 2px solid rgba(11,11,11,.07); }
.swatches { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.swatches div { background: #fff; border-radius: 18px; border: 2px solid rgba(11,11,11,.07); padding: 12px; }
.swatches i { display: block; height: 80px; border-radius: 12px; border: 2px solid rgba(11,11,11,.08); margin-bottom: 8px; }
.swatches b { display: block; font-family: J; font-size: 19px; } .swatches span { display: block; font-size: 18px; color: #5b4a55; font-weight: 500; }
.p13 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.p13 figure img { height: 150px; }
`;

(async () => {
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${PAGES.join("")}</body></html>`;
  const f = path.join(ROOT, "cache", "guide.html");
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const over = await p.evaluate(() => [...document.querySelectorAll(".pg main")].map((m, i) => (m.scrollHeight > m.clientHeight + 1 ? i + 2 : 0)).filter(Boolean));
  if (over.length) console.log("WARNING overflow on pages", over.join(", "));
  const d = path.join(ROOT, "cache", "msheet");
  fs.rmSync(d, { recursive: true, force: true });
  fs.mkdirSync(d, { recursive: true });
  const els = await p.$$(".pg");
  const imgs = [];
  for (let i = 0; i < els.length; i++) {
    const o = path.join(d, `page-${String(i + 1).padStart(2, "0")}.jpg`);
    await els[i].screenshot({ path: o, type: "jpeg", quality: 90 });
    imgs.push(o);
  }
  const ih = path.join(ROOT, "cache", "guide_img.html");
  fs.writeFileSync(ih, `<!doctype html><html><head><style>@page { size: 1080px 1350px; margin: 0; } * { margin: 0; padding: 0; }
    img { display: block; width: 1080px; height: 1350px; page-break-after: always; }</style></head><body>${imgs.map((x) => `<img src="file://${x}">`).join("")}</body></html>`);
  const p3 = await b.newPage();
  await p3.goto("file://" + ih);
  await p3.waitForTimeout(300);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  await p3.pdf({ path: OUT, width: "1080px", height: "1350px", printBackground: true });
  await b.close();
  console.log("wrote", OUT, PAGES.length, "pages");
})();
