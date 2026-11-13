// The script and transcript of the GTA 6 Launch Kit reel as a clean, phone-readable PDF (A4), from plan/script.json and
// the same text as transcript.md, in the Launch Kit's sunset colours. node build/transcript_pdf.cjs
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..");
const SRC = path.resolve(ROOT, "..", "gta6-playbook-9x16");
const A = (p) => "file://" + path.join(SRC, p);
const OUT = path.join(ROOT, "renders", "ai-nxtlvl_gta6-launch-kit_script-transcript.pdf");
const S = JSON.parse(fs.readFileSync(path.join(ROOT, "plan", "script.json"), "utf8"));
const ROWS = [
  ["0:00-0:05", "Hook (mid-story)", 0, "SAME GAMEPLAY. / WHO GETS CLICKED?", "A wall of identical GTA 6 thumbnails scrolling; one lights up, the rest grey out."],
  ["0:05-0:09", "First peak: contrast", 1, "1 HOUR (struck out) → 30 SEC", "Split screen: a cluttered editing timeline vs a timer racing to 0:30."],
  ["0:09-0:13", "Release: step 1", 2, "STEP 1 · GRAB ONE FRAME", "Official GTA 6 promo footage (audio muted) freezes on a chase frame; a frame-grab flash."],
  ["0:13-0:18", "Peak: step 2", 3, "STEP 2 · ONE PROMPT", "The prompt types into a chat box; the frame becomes a finished thumbnail with \"NO WAY\" in big type."],
  ["0:18-0:25", "Release: step 3", 4, "STEP 3 · 10 TITLES / gta 6 police chase", "Ten titles stream in; nine fade, the one with the search phrase moves into a YouTube upload card."],
  ["0:25-0:29", "Peak: step 4", 5, "STEP 4 · HOOK IN 1 SECOND", "A phone plays the clip with \"Rockstar hid this in GTA 6\" on screen at 0:01."],
  ["0:29-0:35", "CTA", 6, "Comment \"KIT\" / the PDF cover", "Comment box types KIT; the Launch Kit PDF cover slides up. Small: Not affiliated with Rockstar Games."],
];
const DESC = `Comment "KIT" and I'll send you the GTA 6 Launch Kit: every prompt, the title formulas and ten hooks.

Next week, everyone uploads the same GTA 6 gameplay. The thumbnail, the title and the first second decide who gets the views.

The 4-step system:
1. Grab one frame from your clip (the chase, the crash, the close call)
2. One AI prompt turns it into a thumbnail
3. Ask AI for ten titles and keep the one with the search phrase
4. Put the hook on screen in the first second

Save this before November 19.

Not affiliated with Rockstar Games.

#gta6 #gtavi #youtubethumbnail #aitools #gamingcreator
gta 6 thumbnail, how to make a youtube thumbnail with ai, gta 6 youtube title ideas, gta 6 content ideas, chatgpt thumbnail prompt, ai thumbnail maker, gta 6 shorts ideas, gaming youtube tips, how to get more views on youtube, gta 6 release date`;
const DM = `Here's the GTA 6 Launch Kit: [PDF LINK]
1. Open the PDF and copy the thumbnail prompt on page 4.
2. Upload one frame from your gameplay with it in ChatGPT or Gemini.
3. Use the title prompt on page 6, then pick a hook from page 7.`;
const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: M; src: url("${A("assets/fonts/montserrat.ttf")}"); font-weight: 100 900; }
@font-face { font-family: J; src: url("${A("assets/fonts/JetBrainsMono-Bold.ttf")}"); }
@page { size: A4; margin: 16mm 15mm 18mm; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: M; color: #1d1433; font-size: 10.5pt; line-height: 1.5; }
.top { padding: 20px 24px; border-radius: 14px; color: #fff; background: linear-gradient(120deg, #1b0840, #5a1270 60%, #ff4fa3); margin-bottom: 18px; }
.k { font-family: J; font-size: 8pt; letter-spacing: .16em; color: #3ef0ff; }
h1 { font-weight: 900; font-size: 24pt; line-height: 1.1; margin: 6px 0 8px; letter-spacing: -.02em; }
.meta { display: flex; flex-wrap: wrap; gap: 6px; }
.meta span { font-size: 8.5pt; font-weight: 700; padding: 3px 10px; border-radius: 99px; background: rgba(255,255,255,.16); }
h2 { font-weight: 900; font-size: 13pt; margin: 20px 0 8px; color: #5a1270; break-after: avoid; }
p.lead { color: #4a3d63; }
.vo { border-left: 4px solid #ff4fa3; background: #fbf3fa; padding: 12px 16px; border-radius: 0 10px 10px 0; }
.vo p { margin: 3px 0; font-size: 11pt; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; }
th { text-align: left; font-family: J; font-size: 7.5pt; letter-spacing: .1em; color: #fff; background: #2a0f52; padding: 7px 8px; }
td { vertical-align: top; padding: 8px; border-bottom: 1px solid #e7dff0; }
tr { break-inside: avoid; }
td.t { font-family: J; font-size: 8pt; white-space: nowrap; color: #5a1270; }
td.b { font-weight: 700; width: 92px; }
td.os { font-weight: 800; color: #c2185b; width: 120px; }
pre { font-family: M; white-space: pre-wrap; font-size: 9.5pt; line-height: 1.45; background: #f6f3fa; border: 1px solid #e3d9ef; border-radius: 10px; padding: 12px 14px; break-inside: avoid; }
ul { margin-left: 18px; } li { margin: 3px 0; }
</style></head><body>
<div class="top"><div class="k">AI.NXTLVL · REEL SCRIPT</div><h1>GTA 6 Launch Kit</h1>
<div class="meta"><span>About 35 s · 97 words</span><span>CTA keyword: KIT</span><span>Lead magnet: The GTA 6 Launch Kit PDF</span></div></div>
<p class="lead">The first GTA reel was about clipping. This one is about packaging the clip: in launch week everyone uploads the same gameplay,
so the thumbnail, the title and the hook decide who gets the views. Arc: hook dropped mid-story, first peak by about 5 s, then peak, release, peak, release, CTA.</p>
<h2>Voiceover</h2><div class="vo">${S.map((l) => `<p>${esc(l.text)}</p>`).join("")}</div>
<h2>Transcript</h2>
<table><tr><th>TIME</th><th>BEAT</th><th>VOICEOVER</th><th>ON SCREEN</th><th>VISUAL</th></tr>
${ROWS.map(([t, b, i, os, v]) => `<tr><td class="t">${t}</td><td class="b">${b}</td><td>“${esc(S[i].text)}”</td><td class="os">${esc(os)}</td><td>${esc(v)}</td></tr>`).join("")}</table>
<h2>Post description (ready to paste)</h2><pre>${esc(DESC)}</pre>
<h2>Keyword auto-DM (once the PDF is hosted)</h2><pre>${esc(DM)}</pre>
<h2>Production notes</h2><ul>
<li>Footage: Rockstar Games' official GTA 6 promo clips only, audio muted, plus our own motion graphics. The thumbnail shown being made is our own example.</li>
<li>GTA 6 is out November 19, 2026, on PS5 and Xbox Series X|S.</li>
<li>Voice: same style as the first GTA reel unless you pick another.</li></ul>
</body></html>`;
(async () => {
  const f = path.join(ROOT, "cache", "transcript.html");
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, html);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: OUT, format: "A4", printBackground: true, margin: { top: "16mm", bottom: "18mm", left: "15mm", right: "15mm" } });
  await b.close();
  console.log("wrote", OUT);
})();
