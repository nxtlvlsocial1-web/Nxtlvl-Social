// The CHAT keyword resource for the GTA 6 chat-clipper reel (AI.NXTLVL): "The GTA 6 Chat Clipper" setup guide, in
// the same design as the earlier GTA guides (../gta6-launch-kit-9x16/build/guide.cjs). It walks a beginner through
// TwitchDownloader (free, open source), Python, FFmpeg and our one-file tool (tool/chat_clips.py, sent with it).
// Images and fonts come from ../gta6-playbook-9x16 (official promo stills, the owner's key art).
// node build/guide.cjs [OUT.pdf]   (page images land in cache/guide/page-N.jpg; check them before delivery)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const SRC = path.resolve(ROOT, "..", "gta6-playbook-9x16");
const OUT = process.argv.find((a) => a.endsWith(".pdf")) || path.join(ROOT, "renders", "ai-nxtlvl_gta6-chat-clipper-guide.pdf");
const A = (p) => "file://" + path.join(SRC, p);

const PAGES = [];
const TOTAL = 8;
function page({ img, kicker, title, body }) {
  const n = PAGES.length + 1;
  PAGES.push(`<section class="pg"><header style="background-image:url('${A(img)}')"><div class="hs"></div>
    <div class="kick">${kicker}</div><h2>${title}</h2></header>
    <main>${body}</main>
    <footer><span>THE GTA 6 CHAT CLIPPER</span><span>${String(n).padStart(2, "0")} / ${String(TOTAL).padStart(2, "0")}</span></footer></section>`);
}
const steps = (items, wide = false) => `<ol class="steps${wide ? " wide" : ""}">${items.map((s) =>
  `<li><span class="bd">${s[0]}</span><p>${s[1]}</p></li>`).join("")}</ol>`;
const note = (t, c = "") => `<div class="note ${c}">${t}</div>`;
const big = (t) => `<div class="big">${t}</div>`;
const prompt = (label, t) => `<div class="pr"><div class="prl">${label}</div><p>${t}</p></div>`;

// 1 cover
PAGES.push(`<section class="pg cover"><div class="cbg" style="background-image:url('${A("cache/vc_23.5.png")}')"></div><div class="cs"></div>
  <div class="cwrap">
    <div class="ckick">FREE TOOL · SETUP GUIDE</div>
    <h1>The <span class="acc">GTA 6</span><br>Chat Clipper</h1>
    <div class="cart"><img src="${A("assets/img/keyart.jpg")}"></div>
    <div class="csub">Let chat find your clips. <span class="acc">One command.</span></div>
    <div class="cpills"><span>FREE</span><span>1 FILE</span><span>VERTICAL CLIPS</span><span>NO AI NEEDED</span></div>
  </div></section>`);

// 2 how it works
page({ img: "cache/vc_28.5.png", kicker: "HOW IT WORKS", title: 'Chat already<br><span class="acc">found the clip</span>',
  body: steps([
    ["1", "When something crazy happens on stream, <b>chat explodes</b>: hundreds of LMAOs, KEKWs and “CLIP IT” in ten seconds."],
    ["2", "<b>TwitchDownloader</b> (free, open source) saves the stream's whole chat as a file."],
    ["3", "<b>chat_clips.py</b> counts the chat every 10 seconds and finds the spikes. Hype words count double."],
    ["4", "Chat reacts after the moment, so every clip <b>starts 20 seconds early</b>."],
    ["5", "It cuts each spike into a <b>vertical 1080x1920 clip</b>, ready to post."],
  ]) + note("You need: a computer (Windows, Mac or Linux), <b>Python 3</b>, <b>FFmpeg</b> and <b>TwitchDownloader</b>. All free. Setup takes about 10 minutes, once.") });

// 3 install
page({ img: "cache/vc_14.5.png", kicker: "STEP 01 · SET UP ONCE", title: 'Install the<br><span class="acc">three free tools</span>',
  body: steps([
    ["1", "<b>Python 3:</b> download from python.org. On Windows, tick “Add Python to PATH” in the installer."],
    ["2", "<b>FFmpeg:</b> Windows: <b>winget install ffmpeg</b> in Terminal. Mac: <b>brew install ffmpeg</b>. Linux: <b>sudo apt install ffmpeg</b>."],
    ["3", "<b>TwitchDownloader:</b> get it from its GitHub page (lay295/TwitchDownloader). Windows has an app; the CLI works on Mac and Linux too."],
    ["4", "Put <b>chat_clips.py</b> (the file I sent you) in a new folder, for example <b>Clips</b>."],
  ]) + note("Check it works: open Terminal in that folder and run <b>python chat_clips.py --help</b> (on Mac: <b>python3</b>).") });

// 4 download chat + video
page({ img: "cache/vc_8.png", kicker: "STEP 02 · GET THE STREAM", title: 'Download the<br><span class="acc">chat and the VOD</span>',
  body: steps([
    ["1", "Copy the stream's VOD link from Twitch (the past broadcast, not the live page)."],
    ["2", "In TwitchDownloader, <b>Chat Download</b>: paste the link, format <b>JSON</b>, save as <b>chat.json</b> in your Clips folder."],
    ["3", "<b>VOD Download</b>: same link, save as <b>stream.mp4</b>. 720p is plenty for vertical clips and downloads faster."],
  ]) + prompt("OR, IN TERMINAL (TWITCHDOWNLOADER CLI)", "TwitchDownloaderCLI chatdownload --id <b>[VOD ID]</b> -o chat.json<br>TwitchDownloaderCLI videodownload --id <b>[VOD ID]</b> -q 720p60 -o stream.mp4")
  + note("<b>Only clip streams you own, or where the streamer allows clipping.</b> Many streamers run clip programs: ask first, credit them, and you stay safe.", "warn") });

// 5 run
page({ img: "cache/vc_23.5.png", kicker: "STEP 03 · ONE COMMAND", title: 'Find the moments,<br><span class="acc">cut the clips</span>',
  body: prompt("FIRST, JUST LIST THE MOMENTS (FAST, NO VIDEO NEEDED)", "python chat_clips.py chat.json")
  + prompt("THEN CUT THEM", "python chat_clips.py chat.json stream.mp4")
  + steps([
    ["1", "You get a <b>clips</b> folder: clip_01, clip_02... each 40 seconds, vertical, with a <b>moments.csv</b> list."],
    ["2", "Tip: only want a 6-hour stream's best parts? List first, then download just those minutes of the VOD."],
  ]) });

// 6 options
page({ img: "cache/vc_28.5.png", kicker: "TUNE IT", title: 'Options for<br><span class="acc">better clips</span>',
  body: steps([
    ["--top 15", "how many clips (default 10)"],
    ["--pre 25", "more lead-in before the spike, for slow-building moments (default 20 s)"],
    ["--length 30", "shorter clips (default 40 s)"],
    ["--crop", "fill the frame by cropping the centre instead of the blurred background"],
    ["--window 15", "for small streams with a slow chat"],
  ], true).replace('class="steps wide"', 'class="steps wide opts"') + prompt("EXAMPLE", "python chat_clips.py chat.json stream.mp4 --top 15 --pre 25 --crop") });

// 7 post
page({ img: "cache/vc_14.5.png", kicker: "STEP 04 · POST", title: 'Make each clip<br><span class="acc">postable</span>',
  body: steps([
    ["1", "<b>Watch the first 3 seconds</b> of each clip. Trim the start until the action begins in the first second."],
    ["2", "<b>Add captions:</b> CapCut's auto captions are free and quick. Big words, centred, short lines."],
    ["3", "<b>Hook on screen</b> in second one: what is about to happen, in five words."],
    ["4", "<b>Credit the streamer</b> in the caption and tag them. It is the right thing and it gets reposts."],
  ]) + big("A 6-hour stream becomes <b>10 clips</b> in the time it takes to make a coffee.") });

// 8 checklist
page({ img: "cache/vc_8.png", kicker: "BEFORE YOU POST", title: 'The <span class="acc">checklist</span>',
  body: `<ol class="check">${[
    "I have permission to clip this stream (or it is mine)",
    "The clip starts on the action, not before it",
    "Captions on, readable on a phone",
    "A hook on screen in the first second",
    "The streamer is credited and tagged",
    "No story spoilers in the title or cover",
  ].map((t) => `<li><i></i><p>${t}</p></li>`).join("")}</ol>` + note("Questions? Comment on the reel. Not affiliated with Rockstar Games or Twitch.") });

const CSS = `
.steps.opts li { grid-template-columns: 210px 1fr !important; } .steps.opts .bd { width: 210px !important; font-size: 22px; white-space: nowrap; justify-content: center; }

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
