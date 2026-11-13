// The FABLE keyword resource for the Fable 5.2 week reel (AI.NXTLVL): "The Fable Week Prompts", the three builds
// from the reel as copy-paste prompts, in AI.NXTLVL's look (night background, violet glows, the nxtlvl wordmark).
// Same layout system as the GTA guides (strict grid, 80 px margins, pages rasterised so phones draw them exactly).
// Facts: Fable 5.2 is included with Claude Pro at no extra cost until Mon 16 Nov 2026, 11:59 pm PT (up to half of the
// weekly limit), then it uses paid usage credits; the Free plan does not include it.
// node build/guide.cjs [OUT.pdf]   (page images land in cache/guide/page-N.jpg; check them before delivery)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv.find((a) => a.endsWith(".pdf")) || path.join(ROOT, "renders", "ai-nxtlvl_fable-week-prompts.pdf");
const A = (p) => "file://" + path.join(ROOT, p);
const SRC = ROOT;

const PAGES = [];
const TOTAL = 6;
function page({ kicker, title, body }) {
  const n = PAGES.length + 1;
  PAGES.push(`<section class="pg"><header><div class="hs"></div><img class="wm" src="${A("assets/img/logo-wordmark.png")}">
    <div class="kick">${kicker}</div><h2>${title}</h2></header>
    <main>${body}</main>
    <footer><span>THE FABLE WEEK PROMPTS · AI.NXTLVL</span><span>${String(n).padStart(2, "0")} / ${String(TOTAL).padStart(2, "0")}</span></footer></section>`);
}
const steps = (items) => `<ol class="steps">${items.map((s) => `<li><span class="bd">${s[0]}</span><p>${s[1]}</p></li>`).join("")}</ol>`;
const note = (t, c = "") => `<div class="note ${c}">${t}</div>`;
const prompt = (label, t) => `<div class="pr"><div class="prl">${label}</div><p>${t}</p></div>`;

// 1 cover
PAGES.push(`<section class="pg cover"><div class="cglow"></div>
  <div class="cwrap">
    <img class="cwm" src="${A("assets/img/logo-wordmark.png")}">
    <div class="ckick">FABLE 5.2 · LAUNCH WEEK</div>
    <h1>The Fable Week<br><span class="acc">Prompts</span></h1>
    <div class="csub">Three things to build before <span class="acc">Monday night.</span></div>
    <div class="cards"><div><em>01</em><b>Your 3D twin</b></div><div><em>02</em><b>Your 2027 plan</b></div><div><em>03</em><b>A Skill that lasts</b></div></div>
    <div class="cpills"><span>COPY</span><span>PASTE</span><span>BUILD</span></div>
  </div></section>`);

// 2 before you start
page({ kicker: "BEFORE YOU START", title: 'Use the week<br><span class="acc">well</span>',
  body: steps([
    ["1", "<b>You need Claude Pro</b> (or a Team seat). Fable isn't on the Free plan."],
    ["2", "<b>Pick Fable 5.2</b> in the model menu before you send the prompt."],
    ["3", "<b>No extra cost until Mon 16 Nov, 11:59 pm PT,</b> up to half of your weekly limit. After that, Fable uses paid credits."],
    ["4", "<b>One prompt per chat.</b> Answer its questions honestly; the output is only as good as your answers."],
    ["5", "<b>Save everything:</b> download the files and copy the plan before Monday."],
  ]) + note("Replace every <b>[bracket]</b> with your own details before you send.") });

// 3 prompt 1
page({ kicker: "BUILD 01 · YOUR 3D TWIN", title: 'An animal that\'s<br><span class="acc">built like you</span>',
  body: prompt("COPY AND PASTE",
    "Ask me 5 quick personality questions, one at a time, and wait for each answer. Then pick the animal that matches me and build it "
    + "as an interactive 3D low-poly model in a single HTML file with Three.js: faceted shapes, my colours <b>[two colours]</b>, a glowing "
    + "ring under it, a slow turntable spin and drag to rotate. Under it, one line on why this animal is me.")
    + steps([
      ["+", "<b>Open the artifact</b> to spin it, then share it or screenshot it for your story."],
      ["+", "<b>Not quite you?</b> Reply \"rounder and softer\" or \"more fierce\" and it rebuilds it."],
    ]) });

// 4 prompt 2
page({ kicker: "BUILD 02 · YOUR 2027", title: 'The questions<br><span class="acc">nobody asks you</span>',
  body: prompt("COPY AND PASTE",
    "Be a blunt but kind coach. Ask me 7 hard questions about my work, health, money and relationships, one at a time, and push back "
    + "when an answer is vague. Then build my 2027 plan: one main goal, three supporting goals, and a month-by-month plan from January "
    + "to December with one focus and one habit per month. End with the first three things I do this week. Make it a printable one-page document.")
    + note("The questions are the point. Give real answers, not the ones that sound good.") });

// 5 prompt 3
page({ kicker: "BUILD 03 · THE ONE THAT LASTS", title: 'Fable writes<br><span class="acc">its own Skill</span>',
  body: prompt("COPY AND PASTE",
    "Write a Claude Skill that captures exactly how you approach <b>[my main task: writing posts / coding / research]</b>. Output a "
    + "SKILL.md with a name and a description that says when to use it, then step-by-step instructions, a quality checklist and two short "
    + "examples. Make it specific enough that a smaller model can follow it and get close to your result.")
    + steps([
      ["1", "<b>Save it</b> as SKILL.md in a folder, and zip the folder."],
      ["2", "<b>Upload it</b> in Claude under Settings, then Capabilities, then Skills."],
      ["3", "<b>After Monday,</b> Sonnet or Opus use the Skill, so the way Fable works stays with you."],
    ]) });

// 6 checklist
const CHECK = ["On Claude Pro, Fable 5.2 selected", "3D twin built and saved", "2027 plan answered honestly and downloaded",
  "SKILL.md written, zipped and uploaded", "All three done before Mon 16 Nov, 11:59 pm PT", "Follow @ai.nxtlvl for the next one"];
page({ kicker: "BEFORE MONDAY", title: 'The<br><span class="acc">checklist</span>',
  body: `<ul class="check">${CHECK.map((c) => `<li><i></i><p>${c}</p></li>`).join("")}</ul>` });

const CSS = `
@font-face { font-family: M; src: url("${A("assets/fonts/montserrat.ttf")}"); font-weight: 100 900; }
@font-face { font-family: S; font-style: italic; src: url("${A("assets/fonts/InstrumentSerif-Italic.ttf")}"); }
@font-face { font-family: J; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
@page { size: 1080px 1350px; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --m: 80px; --pink: #b687f9; --cyan: #b687f9; --orange: #ffb547; --violet: #6008f2; --ink: #07050f; }
body { font-family: M; color: #fff; background: var(--ink); }
.pg { position: relative; width: 1080px; height: 1350px; overflow: hidden; page-break-after: always; display: flex; flex-direction: column;
  background: radial-gradient(80% 40% at 0% 100%, rgba(255,79,163,.22), transparent 70%), radial-gradient(70% 35% at 100% 60%, rgba(62,240,255,.1), transparent 70%),
  linear-gradient(180deg, #1b0840, var(--ink) 55%, #0b0420); }
.acc { color: #ff7a8f; }   /* v3: solid colour; gradient text (background-clip) prints as solid boxes in iOS PDF viewers */
header { position: relative; flex: none; height: 330px; padding: 0 var(--m) 40px; background-size: cover; background-position: center 62%;
  display: flex; flex-direction: column; justify-content: flex-end; }
.hs { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(18,6,46,.15) 0%, rgba(18,6,46,.45) 45%, var(--ink) 100%); }
.kick { position: relative; align-self: flex-start; font-family: J; font-size: 22px; letter-spacing: .16em; color: var(--ink); background: var(--cyan);
  padding: 8px 14px; border-radius: 8px; margin-bottom: 18px; }
h2 { position: relative; font-weight: 900; font-size: 64px; line-height: 1.04; letter-spacing: -.03em; }
main { flex: 1; min-height: 0; padding: 36px var(--m) 24px; display: flex; flex-direction: column; justify-content: flex-start; gap: 30px; overflow: hidden; }
footer { flex: none; margin: 0 var(--m); padding: 22px 0 34px; border-top: 1.5px solid rgba(255,255,255,.15); display: flex; justify-content: space-between;
  font-family: J; font-size: 18px; letter-spacing: .14em; color: rgba(255,255,255,.5); }
.steps, .hooks, .check { list-style: none; display: flex; flex-direction: column; gap: 30px; }
.steps li, .hooks li { display: grid; grid-template-columns: 56px 1fr; column-gap: 26px; align-items: start; }
.steps.wide li { grid-template-columns: 150px 1fr; }
.bd { height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 26px; color: #fff;
  background: linear-gradient(135deg, var(--pink), var(--violet)); white-space: nowrap; }
.steps p, .hooks p, .check p { font-size: 30px; line-height: 1.32; font-weight: 500; color: #ece2ff; padding-top: 6px; }
.steps b, .note b, .big b { color: #fff; font-weight: 800; }
.hooks { gap: 16px; }
.hooks li { align-items: center; }
.hooks p { font-weight: 800; color: #fff; padding-top: 0; font-size: 32px; }
.hooks .bd { height: 52px; }
.note { padding: 24px 28px; border-radius: 18px; font-size: 26px; line-height: 1.38; color: #e6daff; background: rgba(62,240,255,.07);
  border-left: 6px solid var(--cyan); }
.note.warn { background: rgba(255,179,107,.08); border-left-color: var(--orange); }
.big { padding: 26px 30px; border-radius: 18px; font-weight: 800; font-size: 36px; line-height: 1.2; text-align: center;
  background: linear-gradient(90deg, rgba(255,79,163,.22), rgba(127,27,248,.22)); border: 2px solid var(--pink); }
.big b { color: var(--cyan); }
.kwbox { padding: 26px 28px; border-radius: 18px; background: rgba(255,255,255,.04); border: 1.5px solid rgba(255,255,255,.12); }
.kwt { font-family: J; font-size: 20px; letter-spacing: .14em; color: var(--orange); margin-bottom: 16px; }
.kw { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px 12px; }
.kw span { padding: 9px 12px; border-radius: 10px; font-size: 19px; white-space: nowrap; font-weight: 700; background: rgba(255,79,163,.1); border: 1.5px solid rgba(255,79,163,.45); }
.check { gap: 0; }
.check li { display: grid; grid-template-columns: 44px 1fr; column-gap: 26px; align-items: center; padding: 20px 0; border-bottom: 1.5px solid rgba(255,255,255,.1); }
.check li:last-child { border-bottom: 0; }
.check i { width: 44px; height: 44px; border-radius: 10px; border: 3px solid var(--cyan); }
.check p { padding-top: 0; font-weight: 700; color: #fff; font-size: 31px; }
.cover { justify-content: center; }
.cbg { position: absolute; inset: 0; background-size: cover; background-position: center; }
.cs { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(18,6,46,.7) 0%, rgba(18,6,46,.25) 40%, rgba(18,6,46,.9) 100%); }
.cwrap { position: relative; height: 100%; padding: 90px var(--m); display: flex; flex-direction: column; align-items: center; justify-content: space-between; text-align: center; }
.ckick { font-family: J; font-size: 24px; letter-spacing: .24em; color: var(--ink); background: var(--cyan); padding: 9px 18px; border-radius: 8px; }
h1 { font-weight: 900; font-size: 96px; line-height: 1.0; letter-spacing: -.035em; text-shadow: 0 8px 40px rgba(18,6,46,.6); }
.cart { width: 920px; height: 613px; border-radius: 26px; overflow: hidden; box-shadow: 0 0 0 5px #fff, 0 0 80px rgba(255,79,163,.6); }
.cart img { width: 100%; height: 100%; object-fit: cover; display: block; }
.csub { font-weight: 800; font-size: 44px; }
.cpills { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.cpills span { padding: 10px 18px; border-radius: 999px; font-family: J; font-size: 21px; letter-spacing: .08em; background: rgba(18,6,46,.75); border: 2px solid var(--cyan); }
.pr { padding: 26px 30px 28px; border-radius: 18px; background: rgba(255,255,255,.05); border: 2px dashed rgba(62,240,255,.55); }
.prl { font-family: J; font-size: 19px; letter-spacing: .16em; color: var(--cyan); margin-bottom: 12px; }
.pr p { font-family: J; font-size: 24px; line-height: 1.5; color: #f1eaff; }
.pr b { color: var(--orange); font-weight: 700; }
.rules { padding: 22px 28px 6px; border-radius: 18px; background: rgba(255,255,255,.04); border: 1.5px solid rgba(255,255,255,.12); }
.pg:last-child .check li { padding: 16px 0; }
.check.slim li { padding: 13px 0; } .check.slim p { font-size: 27px; } .check.slim i { width: 34px; height: 34px; }
.forms { list-style: none; counter-reset: f; display: flex; flex-direction: column; gap: 12px; }
.forms li { counter-increment: f; font-size: 27px; font-weight: 700; color: #fff; display: grid; grid-template-columns: 44px 1fr; }
.forms li::before { content: counter(f); color: var(--pink); font-weight: 900; }
.pg { background: radial-gradient(70% 40% at 0% 0%, rgba(127,27,248,.35), transparent 70%), radial-gradient(70% 40% at 100% 100%, rgba(96,8,242,.35), transparent 70%), #07050f !important; }
header { background: none !important; height: 300px; }
.hs { display: none; }
.wm { position: absolute; right: 80px; top: 70px; height: 40px; }
.acc { font-family: S; font-style: italic; font-weight: 400; color: #b687f9; letter-spacing: -.01em; }
h2 .acc { font-size: 1.12em; }
.kick { color: #07050f !important; background: #b687f9 !important; }
.bd { background: linear-gradient(135deg, #7f1bf8, #6008f2) !important; }
.cover { background: #07050f !important; }
.cglow { position: absolute; inset: 0; background: radial-gradient(60% 40% at 15% 10%, rgba(127,27,248,.6), transparent 70%), radial-gradient(60% 40% at 90% 95%, rgba(96,8,242,.6), transparent 70%); }
.cwm { height: 64px; }
.cover h1 { font-size: 104px; }
.cover h1 .acc { font-size: 1.12em; }
.ckick { background: #b687f9 !important; }
.cards { display: flex; flex-direction: column; gap: 18px; width: 100%; }
.cards div { display: flex; align-items: center; gap: 26px; padding: 26px 34px; border-radius: 26px; background: rgba(255,255,255,.06); border: 1.5px solid rgba(182,135,249,.35); text-align: left; }
.cards em { font-style: normal; font-family: J; font-size: 30px; color: #b687f9; }
.cards b { font-size: 46px; font-weight: 800; letter-spacing: -.02em; }
.cpills span { border-color: #b687f9 !important; }
`;

(async () => {
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${PAGES.join("")}</body></html>`;
  const f = path.join(ROOT, "cache", "guide.html");
  fs.writeFileSync(f, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  // nothing may spill past its page: report any page whose content overflows
  const over = await p.evaluate(() => [...document.querySelectorAll(".pg main")].map((m, i) => (m.scrollHeight > m.clientHeight + 1 ? i + 2 : 0)).filter(Boolean));
  if (over.length) console.log("WARNING overflow on pages", over.join(", "));
  // v3: every page is rasterised at 2x and the PDF is built from those images, so it looks the same in every viewer
  // (the owner's phone drew CSS effects differently from Chrome)
  const d = path.join(ROOT, "cache", "guide");
  fs.rmSync(d, { recursive: true, force: true });
  fs.mkdirSync(d, { recursive: true });
  const p2 = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p2.goto("file://" + f);
  await p2.evaluate(() => document.fonts.ready);
  await p2.waitForTimeout(400);
  const els = await p2.$$(".pg");
  const imgs = [];
  for (let i = 0; i < els.length; i++) {
    const out = path.join(d, `page-${String(i + 1).padStart(2, "0")}.jpg`);
    await els[i].screenshot({ path: out, type: "jpeg", quality: 90 });
    imgs.push(out);
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
