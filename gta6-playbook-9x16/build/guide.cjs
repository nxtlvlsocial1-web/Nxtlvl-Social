// The GTA6 keyword resource: "The GTA 6 Creator Playbook", a Vice City / Miami themed PDF (owner: "make the gta 6 vice
// city miami themed pdf guide for all of that"; this one is themed on purpose instead of the Creators 100X default).
// Phone-friendly 4:5 pages (1080 x 1350), sunset gradients, neon pink and cyan, palm-and-skyline art from Rockstar's
// own GTA VI album reel, the owner's key art on the cover. Delivers everything the reel teases.
// node build/guide.cjs [OUT.pdf] [--png]   (--png also writes cache/guide/page-N.png previews to check before delivery)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const OUT = process.argv.find((a) => a.endsWith(".pdf")) || path.join(ROOT, "renders", "ai-nxtlvl_gta6-creator-playbook.pdf");
const PNG = process.argv.includes("--png");
const A = (p) => "file://" + path.join(ROOT, p);

const PAGES = [];
const page = (html, cls = "") => PAGES.push(`<section class="pg ${cls}">${html}<div class="ft"><span>THE GTA 6 CREATOR PLAYBOOK</span><b>${PAGES.length + 1}</b></div></section>`);
const band = (img, kicker, title) => `<div class="band" style="background-image:url('${A(img)}')"><div class="bshade"></div>
  <div class="kick">${kicker}</div><h2>${title}</h2></div>`;
const steps = (items) => `<ol class="steps">${items.map((s) => `<li><span>${s[0]}</span><div>${s[1]}</div></li>`).join("")}</ol>`;
const note = (t, c = "") => `<div class="note ${c}">${t}</div>`;

// 1 cover
PAGES.push(`<section class="pg cover"><div class="cbg" style="background-image:url('${A("cache/vc_14.5.png")}')"></div><div class="cshade"></div>
  <div class="ckick">VICE CITY EDITION</div>
  <h1>The <em>GTA 6</em><br>Creator Playbook</h1>
  <div class="cart"><img src="${A("assets/img/keyart.jpg")}"></div>
  <div class="csub">Clip it. Post it. <i>Get paid, not claimed.</i></div>
  <div class="cpills"><span>AI CLIPPING</span><span>SETTINGS</span><span>MUSIC</span><span>KEYWORDS</span><span>LAUNCH PLAN</span></div></section>`);

// 2 the plan
page(band("cache/vc_28.5.png", "START HERE", "The whole system <em>on one page</em>") +
  steps([
    ["01", "<b>Clip with AI.</b> One tool turns a long stream or recording into ready-to-post vertical clips."],
    ["02", "<b>Fix one game setting.</b> In-game radio to zero before you record."],
    ["03", "<b>Follow the music rule.</b> Add songs inside the app, never baked into the file."],
    ["04", "<b>Use the keyword trick.</b> Say, show and write what people search."],
    ["05", "<b>Post in launch week.</b> GTA 6 drops November 19: be early, be consistent."],
  ]) + note("Every page after this one is one of these five steps, in order. Do them once, then repeat them for every clip."));

// 3 step 1: the clipping tool
page(band("cache/vc_8.png", "STEP 01 · THE AI TOOL", "OpusClip <em>clips it for you</em>") +
  steps([
    ["1", "<b>Get the footage.</b> Stream from your PS5 or Xbox to Twitch or YouTube (built in, no capture card), or record your session."],
    ["2", "<b>Paste the link</b> into OpusClip (<b>opus.pro</b>): your VOD, your YouTube video, or an uploaded file."],
    ["3", "<b>Set it up:</b> 9:16 vertical, clip length 15 to 60 s, captions on."],
    ["4", "<b>Sort by virality score</b> and keep the best 5 to 10. Trim the first second if the action starts late."],
    ["5", "<b>Export and schedule.</b> One long session becomes a week of posts."],
  ]) +
  note("<b>Console player?</b> Eklipse (eklipse.gg) is built for gaming streams and works with console streams on Twitch or YouTube.") +
  note("<b>Clipping other streamers?</b> Only clip streamers who allow it or run a clipping program (some pay clippers per view). Credit them, and never re-upload a whole stream.", "warn"));

// 4 step 2: the game setting
page(band("cache/vc_14.5.png", "STEP 02 · THE SETTING", "Radio to <em>zero</em>") +
  `<div class="big">In-game radio / music volume <b>→ 0</b></div>` +
  steps([
    ["1", "<b>Why:</b> GTA's radio plays licensed songs. Record them and your clip can be <b>claimed, muted or demonetised</b>, and the money goes to the label."],
    ["2", "<b>Keep</b> dialogue and sound effects on: the cars, the chaos and the sirens are what people watch for."],
    ["3", "<b>Capture settings:</b> PS5 → Settings → Captures and Broadcasts. Xbox → Settings → Preferences → Capture & share. Record at the highest resolution you can."],
    ["4", "<b>Mic:</b> on only if you commentate. Your voice over gameplay makes the clip yours."],
  ]) +
  note("<b>Rockstar's video rules:</b> don't post raw cutscenes or big story spoilers. Gameplay with your own commentary is the safe zone. Check Rockstar's video policy before you monetise.", "warn"));

// 5 step 3: the music rule
page(band("cache/vc_28.5.png", "STEP 03 · THE MUSIC RULE", "Add music <em>in the app</em>") +
  `<div class="big">Never bake a copyrighted song <b>into the file</b></div>` +
  steps([
    ["1", "<b>Instagram:</b> post the clip without music, then add the song from the Reels audio picker. It stays licensed and links your reel to the song's page."],
    ["2", "<b>TikTok:</b> business accounts use the Commercial Music Library."],
    ["3", "<b>YouTube Shorts:</b> add audio from Shorts' own library, or use the free YouTube Audio Library."],
    ["4", "<b>Already has a song in it?</b> Remove it with Demucs (free, open source: github.com/facebookresearch/demucs), or mute that part."],
    ["5", "<b>Keep it under the action:</b> music low, gameplay sound up."],
  ]));

// 6 step 4: the keyword trick
const KW = ["gta 6 gameplay", "gta 6 funny moments", "gta 6 police chase", "gta 6 best cars", "gta 6 money",
  "gta 6 map", "gta 6 secrets", "gta 6 easter eggs", "gta 6 hidden details", "gta 6 cheats",
  "gta 6 vice city", "gta 6 lucia", "gta 6 jason", "gta 6 fails", "gta 6 tips and tricks",
  "gta 6 best missions", "gta 6 vs gta 5", "gta 6 realistic", "gta 6 best weapons", "gta 6 clips"];
page(band("cache/vc_8.png", "STEP 04 · THE KEYWORD TRICK", "Say it. Show it. <em>Write it.</em>") +
  steps([
    ["1", "<b>Show it:</b> the exact search phrase as on-screen text in the first 2 seconds."],
    ["2", "<b>Write it:</b> the phrase in the first line of your caption, not buried at the end."],
    ["3", "<b>Say it:</b> if you talk, say the phrase out loud. Platforms read captions and speech to work out what a video is about."],
    ["4", "<b>Finish the caption</b> with 3 to 5 hashtags and one line of search phrases."],
  ]) + `<div class="kwt">20 PHRASES TO BUILD CLIPS AROUND</div><div class="kw">${KW.map((k) => `<span>${k}</span>`).join("")}</div>`);

// 7 hooks
const HOOKS = ["This shouldn't be possible in GTA 6...", "Nobody noticed this in GTA 6", "GTA 6 police are actually insane",
  "Rockstar hid this in Vice City", "Wait for the ending...", "POV: you finally got GTA 6", "GTA 5 vs GTA 6: look at this",
  "Rate this GTA 6 escape from 1 to 10", "I tried the craziest thing in GTA 6", "The most realistic thing in GTA 6"];
page(band("cache/vc_14.5.png", "BONUS", "10 hooks for <em>GTA clips</em>") +
  `<ol class="hooks">${HOOKS.map((h) => `<li>${h}</li>`).join("")}</ol>` +
  note("Put the hook on screen in the first second, then cut straight to the action. Only use a hook your clip actually delivers."));

// 8 step 5: launch week
page(band("cache/vc_28.5.png", "STEP 05 · LAUNCH WEEK", "Be early. <em>Be everywhere.</em>") +
  steps([
    ["Day 0", "<b>Nov 19:</b> post your first clip the day it drops. First impressions and \"first look\" clips travel."],
    ["Day 1–3", "<b>2 to 3 clips a day</b> from your sessions. Same format, same hook style, so people recognise you."],
    ["Day 4–7", "<b>Start a series:</b> \"GTA 6 police are insane, part 1, 2, 3\". Series bring people back."],
    ["Daily", "<b>Reply to comments</b> in the first hour, and pin your best clip to your profile."],
    ["Weekly", "<b>Check Insights:</b> double down on the clip type and posting time that worked best."],
  ]));

// 9 checklist
const CHECK = ["Stream or recording ready", "Clipped with OpusClip, best 5 to 10 kept", "In-game radio at 0 before recording",
  "No raw cutscenes or big spoilers", "Music added in the app, not in the file", "Search phrase on screen in the first 2 s",
  "Search phrase in the first caption line", "3 to 5 hashtags + search phrase line", "Posted, replied, pinned", "Repeat tomorrow"];
page(band("cache/vc_8.png", "BEFORE EVERY POST", "The <em>checklist</em>") +
  `<ul class="check">${CHECK.map((c) => `<li>${c}</li>`).join("")}</ul>` +
  `<div class="end">See you in <em>Vice City.</em></div>`);

const CSS = `
@font-face { font-family: M; src: url("${A("assets/fonts/montserrat.ttf")}"); font-weight: 100 900; }
@font-face { font-family: S; src: url("${A("assets/fonts/InstrumentSerif-Italic.ttf")}"); font-style: italic; }
@font-face { font-family: J; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
@page { size: 1080px 1350px; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: M; color: #fff; background: #12062e; }
.pg { position: relative; width: 1080px; height: 1350px; overflow: hidden; page-break-after: always;
  background: radial-gradient(70% 45% at 0% 100%, rgba(255,79,163,.35), transparent 70%), radial-gradient(60% 40% at 100% 70%, rgba(62,240,255,.18), transparent 70%),
  linear-gradient(180deg, #1b0840, #12062e 60%, #0b0420); }
.band { position: relative; height: 360px; background-size: cover; background-position: center 60%; display: flex; flex-direction: column;
  justify-content: flex-end; padding: 0 70px 34px; }
.bshade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(18,6,46,.05), rgba(18,6,46,.25) 50%, rgba(18,6,46,.95)); }
.kick { position: relative; font-family: J; font-size: 26px; letter-spacing: .16em; color: #3ef0ff; text-shadow: 0 0 18px rgba(62,240,255,.7); margin-bottom: 10px; }
h2 { position: relative; font-weight: 900; font-size: 70px; line-height: 1.02; letter-spacing: -.03em; text-shadow: 0 6px 30px rgba(18,6,46,.8); }
h2 em, h1 em, .end em { font-family: S; font-weight: 400; letter-spacing: 0; color: #ff4fa3; text-shadow: 0 0 24px rgba(255,79,163,.8); }
.steps { list-style: none; padding: 34px 70px 0; }
.steps li { display: flex; gap: 26px; align-items: flex-start; margin-bottom: 24px; font-size: 31px; line-height: 1.3; font-weight: 500; color: #efe6ff; }
.steps li span { flex: none; min-width: 74px; padding: 8px 14px; border-radius: 14px; text-align: center; font-weight: 900; font-size: 28px;
  background: linear-gradient(135deg, #ff4fa3, #7f1bf8); box-shadow: 0 0 22px rgba(255,79,163,.5); color: #fff; }
.steps li b, .note b, .big b { color: #fff; font-weight: 800; }
.note { margin: 6px 70px 18px; padding: 22px 28px; border-radius: 22px; font-size: 27px; line-height: 1.35; color: #e8dcff;
  background: rgba(62,240,255,.08); border: 2px solid rgba(62,240,255,.45); }
.note.warn { background: rgba(255,179,107,.1); border-color: rgba(255,179,107,.6); }
.big { margin: 30px 70px 0; padding: 24px 30px; border-radius: 22px; font-weight: 800; font-size: 40px; line-height: 1.15;
  background: linear-gradient(90deg, rgba(255,79,163,.25), rgba(127,27,248,.25)); border: 2px solid #ff4fa3; box-shadow: 0 0 40px rgba(255,79,163,.3); }
.big b { color: #3ef0ff; text-shadow: 0 0 18px rgba(62,240,255,.7); }
.kwt { margin: 10px 70px 14px; font-family: J; font-size: 24px; letter-spacing: .14em; color: #ffb36b; }
.kw { margin: 0 70px; display: flex; flex-wrap: wrap; gap: 12px; }
.kw span { padding: 10px 18px; border-radius: 999px; font-size: 24px; font-weight: 700; background: rgba(255,255,255,.08); border: 1.5px solid rgba(255,79,163,.6); }
.hooks { padding: 34px 70px 10px 130px; font-size: 34px; font-weight: 800; line-height: 1.2; }
.hooks li { margin-bottom: 18px; padding-left: 10px; }
.hooks li::marker { color: #ff4fa3; font-weight: 900; }
.check { list-style: none; padding: 34px 70px 0; }
.check li { position: relative; padding: 14px 0 14px 70px; font-size: 32px; font-weight: 700; border-bottom: 1.5px solid rgba(255,255,255,.1); }
.check li::before { content: ""; position: absolute; left: 0; top: 14px; width: 40px; height: 40px; border-radius: 10px; border: 3px solid #3ef0ff;
  box-shadow: 0 0 14px rgba(62,240,255,.6); }
.end { position: absolute; left: 0; right: 0; bottom: 110px; text-align: center; font-weight: 900; font-size: 64px; }
.ft { position: absolute; left: 70px; right: 70px; bottom: 34px; display: flex; justify-content: space-between; font-family: J; font-size: 20px;
  letter-spacing: .14em; color: rgba(255,255,255,.45); }
.ft b { color: #ff4fa3; }
.cover .ft { display: none; }
.cbg { position: absolute; inset: 0; background-size: cover; background-position: center; }
.cshade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(18,6,46,.55), rgba(18,6,46,.1) 40%, rgba(18,6,46,.85)); }
.ckick { position: absolute; left: 0; right: 0; top: 80px; text-align: center; font-family: J; font-size: 30px; letter-spacing: .3em; color: #3ef0ff;
  text-shadow: 0 0 20px rgba(62,240,255,.8); }
h1 { position: absolute; left: 0; right: 0; top: 140px; text-align: center; font-weight: 900; font-size: 104px; line-height: .98; letter-spacing: -.035em;
  text-shadow: 0 8px 40px rgba(18,6,46,.7); }
h1 em { font-size: 118px; }
.cart { position: absolute; left: 80px; top: 430px; width: 920px; height: 613px; border-radius: 28px; overflow: hidden; transform: rotate(-2deg);
  box-shadow: 0 0 0 6px #fff, 0 0 90px rgba(255,79,163,.8); }
.cart img { width: 100%; height: 100%; object-fit: cover; }
.csub { position: absolute; left: 0; right: 0; top: 1110px; text-align: center; font-weight: 800; font-size: 46px; }
.csub i { font-family: S; font-weight: 400; font-size: 54px; color: #ff4fa3; }
.cpills { position: absolute; left: 50px; right: 50px; top: 1200px; display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.cpills span { padding: 10px 18px; border-radius: 999px; font-family: J; font-size: 22px; letter-spacing: .08em; background: rgba(18,6,46,.7); border: 2px solid #3ef0ff; }
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
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  await p.pdf({ path: OUT, width: "1080px", height: "1350px", printBackground: true, pageRanges: "" });
  if (PNG) {
    const d = path.join(ROOT, "cache", "guide");
    fs.mkdirSync(d, { recursive: true });
    const n = await p.evaluate(() => document.querySelectorAll(".pg").length);
    for (let i = 0; i < n; i++) {
      const el = (await p.$$(".pg"))[i];
      await el.screenshot({ path: path.join(d, `page-${i + 1}.png`) });
    }
  }
  await b.close();
  console.log("wrote", OUT, PAGES.length, "pages");
})();
