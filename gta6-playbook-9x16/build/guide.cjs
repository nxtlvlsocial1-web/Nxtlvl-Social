// The GTA6 keyword resource: "The GTA 6 Creator Playbook", a Miami-sunset themed PDF (owner asked for this theme
// instead of the Creators 100X default). Phone-friendly 4:5 pages (1080 x 1350), the owner's key art on the cover.
// v2 (owner: "fix the pdf design, it looks bad, don't write vice city, fix the alignment"): one strict grid on every
// page (80 px margins; a fixed 330 px header with the kicker and a 2-line title; a content column that fills the page
// evenly; a footer rule), fixed-size step badges aligned to the first line of text, one type family for titles (the
// accent word in colour, not a second font), and no "Vice City" anywhere.
// node build/guide.cjs [OUT.pdf]   (page images land in cache/guide/page-N.jpg; check them before delivery)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv.find((a) => a.endsWith(".pdf")) || path.join(ROOT, "renders", "ai-nxtlvl_gta6-creator-playbook.pdf");
const PNG = process.argv.includes("--png");
const A = (p) => "file://" + path.join(ROOT, p);

const PAGES = [];
const TOTAL = 9;
function page({ img, kicker, title, body }) {
  const n = PAGES.length + 1;
  PAGES.push(`<section class="pg"><header style="background-image:url('${A(img)}')"><div class="hs"></div>
    <div class="kick">${kicker}</div><h2>${title}</h2></header>
    <main>${body}</main>
    <footer><span>THE GTA 6 CREATOR PLAYBOOK</span><span>${String(n).padStart(2, "0")} / ${String(TOTAL).padStart(2, "0")}</span></footer></section>`);
}
const steps = (items, wide = false) => `<ol class="steps${wide ? " wide" : ""}">${items.map((s) =>
  `<li><span class="bd">${s[0]}</span><p>${s[1]}</p></li>`).join("")}</ol>`;
const note = (t, c = "") => `<div class="note ${c}">${t}</div>`;
const big = (t) => `<div class="big">${t}</div>`;

// 1 cover
PAGES.push(`<section class="pg cover"><div class="cbg" style="background-image:url('${A("cache/vc_14.5.png")}')"></div><div class="cs"></div>
  <div class="cwrap">
    <div class="ckick">CREATOR GUIDE · 2026</div>
    <h1>The <span class="acc">GTA 6</span><br>Creator Playbook</h1>
    <div class="cart"><img src="${A("assets/img/keyart.jpg")}"></div>
    <div class="csub">Clip it. Post it. <span class="acc">Get paid, not claimed.</span></div>
    <div class="cpills"><span>AI CLIPPING</span><span>SETTINGS</span><span>MUSIC</span><span>KEYWORDS</span><span>LAUNCH PLAN</span></div>
  </div></section>`);

// 2 the plan
page({ img: "cache/vc_28.5.png", kicker: "START HERE", title: 'The whole system<br><span class="acc">on one page</span>',
  body: steps([
    ["1", "<b>Clip with AI.</b> One tool turns a long stream or recording into ready-to-post vertical clips."],
    ["2", "<b>Fix one game setting.</b> In-game radio to zero before you record."],
    ["3", "<b>Follow the music rule.</b> Add songs inside the app, never baked into the file."],
    ["4", "<b>Use the keyword trick.</b> Say, show and write what people search."],
    ["5", "<b>Post in launch week.</b> GTA 6 drops November 19: be early, be consistent."],
  ]) + note("Each of the next pages is one of these five steps, in order. Set them up once, then repeat for every clip.") });

// 3 step 1
page({ img: "cache/vc_8.png", kicker: "STEP 01 · THE AI TOOL", title: 'OpusClip<br><span class="acc">clips it for you</span>',
  body: steps([
    ["1", "<b>Get the footage.</b> Stream from your PS5 or Xbox to Twitch or YouTube (built in, no capture card), or record your session."],
    ["2", "<b>Paste the link</b> into OpusClip at <b>opus.pro</b>: your VOD, a YouTube video or an uploaded file."],
    ["3", "<b>Set it up:</b> 9:16 vertical, clips of 15 to 60 seconds, captions on."],
    ["4", "<b>Sort by virality score</b> and keep the best 5 to 10."],
    ["5", "<b>Export and schedule.</b> One long session becomes a week of posts."],
  ]) + note("<b>Console player?</b> Eklipse (eklipse.gg) is built for gaming streams and works with console streams on Twitch or YouTube.")
    + note("<b>Clipping other streamers?</b> Only those who allow it or run a clipping program. Credit them; never re-upload a whole stream.", "warn") });

// 4 step 2
page({ img: "cache/vc_14.5.png", kicker: "STEP 02 · THE SETTING", title: 'In-game radio<br><span class="acc">to zero</span>',
  body: big("Audio settings → Radio / music volume → <b>0</b>") + steps([
    ["1", "<b>Why:</b> the radio plays licensed songs. Record them and your clip can be <b>claimed, muted or demonetised</b>."],
    ["2", "<b>Keep</b> dialogue and sound effects on. The cars, the chaos and the sirens are what people watch for."],
    ["3", "<b>Capture:</b> PS5 → Settings → Captures and Broadcasts. Xbox → Settings → Preferences → Capture & share."],
    ["4", "<b>Mic</b> on only if you commentate. Your voice over gameplay makes the clip yours."],
  ]) + note("<b>Rockstar's video rules:</b> don't post raw cutscenes or big story spoilers. Gameplay with your own commentary is the safe zone. Check Rockstar's video policy before you monetise.", "warn") });

// 5 step 3
page({ img: "cache/vc_28.5.png", kicker: "STEP 03 · THE MUSIC RULE", title: 'Add music<br><span class="acc">inside the app</span>',
  body: big("Never bake a copyrighted song <b>into the file</b>") + steps([
    ["1", "<b>Instagram:</b> post the clip without music, then add the song from the Reels audio picker."],
    ["2", "<b>TikTok:</b> business accounts use the Commercial Music Library."],
    ["3", "<b>YouTube Shorts:</b> add audio from Shorts' own library, or the free YouTube Audio Library."],
    ["4", "<b>Song already in the clip?</b> Remove it with Demucs (free and open source) or mute that part."],
    ["5", "<b>Mix it low:</b> music under the action, gameplay sound up."],
  ]) });

// 6 step 4
const KW = ["gta 6 gameplay", "gta 6 funny moments", "gta 6 police chase", "gta 6 best cars", "gta 6 money", "gta 6 map",
  "gta 6 secrets", "gta 6 easter eggs", "gta 6 hidden details", "gta 6 cheats", "gta 6 online", "gta 6 lucia", "gta 6 jason",
  "gta 6 fails", "gta 6 tips and tricks", "gta 6 best missions", "gta 6 vs gta 5", "gta 6 clips"];
page({ img: "cache/vc_8.png", kicker: "STEP 04 · THE KEYWORD TRICK", title: 'Say it. Show it.<br><span class="acc">Write it.</span>',
  body: steps.call(null, [
    ["1", "<b>Show it:</b> the search phrase as on-screen text in the first 2 seconds."],
    ["2", "<b>Write it:</b> the phrase in the first line of your caption."],
    ["3", "<b>Say it:</b> if you talk, say the phrase out loud. Platforms read captions and speech."],
    ["4", "<b>Finish</b> with 3 to 5 hashtags and one line of search phrases."],
  ]) + `<div class="kwbox"><div class="kwt">18 PHRASES TO BUILD CLIPS AROUND</div><div class="kw">${KW.map((k) => `<span>${k}</span>`).join("")}</div></div>` });

// 7 hooks
const HOOKS = ["This shouldn't be possible in GTA 6...", "Nobody noticed this in GTA 6", "GTA 6 police are actually insane",
  "Rockstar hid this in GTA 6", "Wait for the ending...", "POV: you finally got GTA 6", "GTA 5 vs GTA 6: look at this",
  "Rate this GTA 6 escape from 1 to 10", "I tried the craziest thing in GTA 6", "The most realistic thing in GTA 6"];
page({ img: "cache/vc_14.5.png", kicker: "BONUS", title: '10 hooks for<br><span class="acc">GTA clips</span>',
  body: `<ol class="hooks">${HOOKS.map((h, i) => `<li><span class="bd">${i + 1}</span><p>${h}</p></li>`).join("")}</ol>`
    + note("Hook on screen in the first second, then cut straight to the action. Only use a hook your clip delivers.") });

// 8 step 5
page({ img: "cache/vc_28.5.png", kicker: "STEP 05 · LAUNCH WEEK", title: 'Be early.<br><span class="acc">Be everywhere.</span>',
  body: steps([
    ["Day 0", "<b>Nov 19:</b> post your first clip the day it drops. First-look clips travel."],
    ["Day 1–3", "<b>2 to 3 clips a day</b> from your sessions. Same format, same hook style."],
    ["Day 4–7", "<b>Start a series:</b> \"GTA 6 police are insane, part 1, 2, 3\". Series bring people back."],
    ["Daily", "<b>Reply to comments</b> in the first hour and pin your best clip."],
    ["Weekly", "<b>Check Insights</b> and double down on the clip type and time that worked."],
  ], true) });

// 9 checklist
const CHECK = ["Stream or recording ready", "Clipped with OpusClip, best 5 to 10 kept", "In-game radio at 0 before recording",
  "No raw cutscenes or big spoilers", "Music added in the app, not in the file", "Search phrase on screen in the first 2 s",
  "Search phrase in the first caption line", "3 to 5 hashtags + search phrase line", "Posted, replied, pinned", "Repeat tomorrow"];
page({ img: "cache/vc_8.png", kicker: "BEFORE EVERY POST", title: 'The<br><span class="acc">checklist</span>',
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
