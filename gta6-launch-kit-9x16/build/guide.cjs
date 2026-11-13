// The KIT keyword resource for the GTA 6 Launch Kit reel (AI.NXTLVL): "The GTA 6 Launch Kit" PDF, in the same
// Miami-sunset design as the first GTA guide (../gta6-playbook-9x16/build/guide.cjs: strict grid, 80 px margins,
// rasterised pages so iPhone viewers draw it exactly; no "Vice City" text, per the owner). New content: thumbnail,
// title and hook prompts for launch-week uploads. Images and fonts come from ../gta6-playbook-9x16 (the official
// promo stills and the owner's key art).
// node build/guide.cjs [OUT.pdf]   (page images land in cache/guide/page-N.jpg; check them before delivery)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const SRC = path.resolve(ROOT, "..", "gta6-playbook-9x16");
const OUT = process.argv.find((a) => a.endsWith(".pdf")) || path.join(ROOT, "renders", "ai-nxtlvl_gta6-launch-kit.pdf");
const A = (p) => "file://" + path.join(SRC, p);

const PAGES = [];
const TOTAL = 9;
function page({ img, kicker, title, body }) {
  const n = PAGES.length + 1;
  PAGES.push(`<section class="pg"><header style="background-image:url('${A(img)}')"><div class="hs"></div>
    <div class="kick">${kicker}</div><h2>${title}</h2></header>
    <main>${body}</main>
    <footer><span>THE GTA 6 LAUNCH KIT</span><span>${String(n).padStart(2, "0")} / ${String(TOTAL).padStart(2, "0")}</span></footer></section>`);
}
const steps = (items, wide = false) => `<ol class="steps${wide ? " wide" : ""}">${items.map((s) =>
  `<li><span class="bd">${s[0]}</span><p>${s[1]}</p></li>`).join("")}</ol>`;
const note = (t, c = "") => `<div class="note ${c}">${t}</div>`;
const big = (t) => `<div class="big">${t}</div>`;
const prompt = (label, t) => `<div class="pr"><div class="prl">${label}</div><p>${t}</p></div>`;

// 1 cover
PAGES.push(`<section class="pg cover"><div class="cbg" style="background-image:url('${A("cache/vc_23.5.png")}')"></div><div class="cs"></div>
  <div class="cwrap">
    <div class="ckick">LAUNCH WEEK · NOV 19</div>
    <h1>The <span class="acc">GTA 6</span><br>Launch Kit</h1>
    <div class="cart"><img src="${A("assets/img/keyart.jpg")}"></div>
    <div class="csub">Thumbnail. Title. Hook. <span class="acc">With AI.</span></div>
    <div class="cpills"><span>THUMBNAIL PROMPTS</span><span>TITLE FORMULAS</span><span>10 HOOKS</span><span>CHECKLIST</span></div>
  </div></section>`);

// 2 the system
page({ img: "cache/vc_28.5.png", kicker: "START HERE", title: 'The whole kit<br><span class="acc">on one page</span>',
  body: steps([
    ["1", "<b>Grab one frame</b> from your clip: the chase, the crash, the close call."],
    ["2", "<b>One prompt</b> turns that frame into a thumbnail."],
    ["3", "<b>Ask for ten titles</b> and keep the one with the phrase people search."],
    ["4", "<b>Hook on screen</b> in the first second of the clip."],
    ["5", "<b>Description and tags</b> from one more prompt, then post."],
  ]) + note("Everything here works in <b>ChatGPT</b> or <b>Gemini</b>: both can edit an image you upload. Copy a prompt, replace the [brackets], go.") });

// 3 the frame
page({ img: "cache/vc_14.5.png", kicker: "STEP 01 · THE FRAME", title: 'Grab the<br><span class="acc">one frame</span>',
  body: steps([
    ["1", "<b>PS5:</b> press the Create button and choose Take Screenshot. Or pause your recording and screenshot it."],
    ["2", "<b>Xbox Series X|S:</b> press the Share button on the controller to save a screenshot."],
    ["3", "<b>Pick the peak:</b> mid-chase, mid-crash, the split second before it goes wrong."],
    ["4", "<b>One subject,</b> big and sharp. No menus, no map, no pause screen."],
  ]) + note("<b>Skip cutscenes and story spoilers.</b> Gameplay moments are yours to show; spoilers get you reported and unfollowed.", "warn") });

// 4 the thumbnail prompt
page({ img: "cache/vc_23.5.png", kicker: "STEP 02 · THE THUMBNAIL", title: 'One prompt,<br><span class="acc">one thumbnail</span>',
  body: prompt("UPLOAD YOUR FRAME, THEN PASTE",
    "Turn this gameplay frame into a YouTube thumbnail, 16:9. Keep the scene and the main subject exactly as they are, just sharper and brighter. "
    + "Add two bold words in white with a thick dark outline: <b>[YOUR 2 WORDS]</b>. Push the colours to a neon sunset (pink, orange, cyan), "
    + "add a soft glow behind the subject and zoom in slightly on the action. No other text, no logos.")
    + steps([
      ["1", "<b>Two words</b> that tease the moment: NO WAY, TOO FAST, HOW?!, 6 STARS."],
      ["2", "<b>Not happy?</b> Reply “bigger text, more contrast” or “zoom in more” instead of starting over."],
    ]) });

// 5 variations + rules
page({ img: "cache/vc_8.png", kicker: "STEP 02 · VARIATIONS AND RULES", title: 'Three more<br><span class="acc">styles</span>',
  body: steps([
    ["A", "<b>Circle and arrow:</b> “Add a red circle and an arrow pointing at [the thing], keep everything else.”"],
    ["B", "<b>Versus:</b> “Split this frame with [second frame]: left GTA 5, right GTA 6, the word VS in the middle.”"],
    ["C", "<b>Shorts cover:</b> “Same thumbnail as a 9:16 cover, text in the middle third.”"],
  ]) + `<div class="rules"><div class="kwt">THE RULES</div><ul class="check slim">${["Three words at most", "Readable on a phone at thumbnail size",
    "1280 x 720 for YouTube", "No Rockstar logo, nothing that looks official", "Never promise what the clip doesn't show"].map((c) => `<li><i></i><p>${c}</p></li>`).join("")}</ul></div>` });

// 6 titles
const FORM = ["GTA 6 [thing] is actually insane", "I tried [crazy idea] in GTA 6", "GTA 6: [number] details nobody noticed",
  "GTA 6 vs GTA 5: [thing]", "The most realistic [thing] in GTA 6", "GTA 6 police chase, but [twist]", "Don't do this in GTA 6", "GTA 6 [thing] in 60 seconds"];
page({ img: "cache/vc_28.5.png", kicker: "STEP 03 · THE TITLE", title: 'Ten titles,<br><span class="acc">keep one</span>',
  body: prompt("PASTE", "Write 10 YouTube titles for my GTA 6 clip where <b>[what happens]</b>. Each under 60 characters, starting with “GTA 6” "
    + "or ending with it, using the search phrase <b>[phrase]</b>. Curious, never misleading. Rank them by how likely people are to click.")
    + `<div class="kwbox"><div class="kwt">8 TITLE FORMULAS</div><ol class="forms">${FORM.map((f) => `<li>${f}</li>`).join("")}</ol></div>` });

// 7 hooks
const HOOKS = ["This went wrong in 2 seconds", "GTA 6 did NOT have to go this hard", "Watch the background", "I can't believe this worked",
  "The police in GTA 6 are different", "Nobody is talking about this", "Wait for it...", "Rate this escape from 1 to 10",
  "GTA 6 physics are unreal", "This is my new favourite thing in GTA 6"];
page({ img: "cache/vc_14.5.png", kicker: "STEP 04 · THE HOOK", title: 'Ten hooks for<br><span class="acc">the first second</span>',
  body: `<ol class="hooks">${HOOKS.map((h, i) => `<li><span class="bd">${i + 1}</span><p>${h}</p></li>`).join("")}</ol>`
    + note("On screen at 0:01, big, in the middle third. Then cut straight to the action.") });

// 8 description + tags
const KW = ["gta 6 gameplay", "gta 6 police chase", "gta 6 funny moments", "gta 6 physics", "gta 6 best cars", "gta 6 map",
  "gta 6 secrets", "gta 6 easter eggs", "gta 6 tips", "gta 6 money", "gta 6 stunts", "gta 6 fails",
  "gta 6 realistic", "gta 6 vs gta 5", "gta 6 shorts", "gta 6 online", "gta 6 lucia", "gta 6 jason"];
page({ img: "cache/vc_23.5.png", kicker: "STEP 05 · DESCRIPTION AND TAGS", title: 'Let AI write<br><span class="acc">the rest</span>',
  body: prompt("PASTE", "Write a YouTube description for my GTA 6 clip titled <b>[title]</b>: the first line repeats its search phrase, then two "
    + "short lines on what happens, then 3 hashtags. After that, give me 15 tags people actually search.")
    + `<div class="kwbox"><div class="kwt">18 SEARCH PHRASES TO BUILD AROUND</div><div class="kw">${KW.map((k) => `<span>${k}</span>`).join("")}</div></div>` });

// 9 checklist
const CHECK = ["One sharp frame, no menus or spoilers", "Thumbnail: two or three words, readable on a phone", "No Rockstar logo or official-looking art",
  "Title has the search phrase", "Hook on screen at 0:01", "Description: search phrase in line one", "Tags and 3 hashtags",
  "In-game radio off, music added in the app", "Posted in launch week, replied to comments", "Repeat for every clip"];
page({ img: "cache/vc_8.png", kicker: "BEFORE EVERY UPLOAD", title: 'The<br><span class="acc">checklist</span>',
  body: `<ul class="check">${CHECK.map((c) => `<li><i></i><p>${c}</p></li>`).join("")}</ul>` });

const CSS = `
@font-face { font-family: M; src: url("${A("assets/fonts/montserrat.ttf")}"); font-weight: 100 900; }
@font-face { font-family: J; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
@page { size: 1080px 1350px; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --m: 80px; --pink: #ff4fa3; --cyan: #3ef0ff; --orange: #ffb36b; --violet: #7f1bf8; --ink: #12062e; }
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
