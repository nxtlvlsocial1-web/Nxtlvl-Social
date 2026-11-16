// ---------------------------------------------------------------- textures: the calendar numbers, pillar icons, sticky notes, the
// prompt card and the three answers, the Day 9 card, the menu board, the clapperboard, the phone screen, the logo poster.
// Inter (OFL), drawn after the fonts load. Colours from brands/creators-100x/brand.md.
const text = (w, h, draw) => pix(w, h, draw, false);
const INK_S = "#101111", PINK_S = "#FD0B68", LIME_S = "#CCFB79", OFF_S = "#FDF4F4";
const F = (wt, px2) => `${wt} ${px2}px Inter, sans-serif`;
function wrap(g, s, x, y, maxW, lh) { const words = s.split(" "); let line = "", yy = y; for (const w of words) { const t = line ? line + " " + w : w; if (g.measureText(t).width > maxW && line) { g.fillText(line, x, yy); line = w; yy += lh; } else line = t; } g.fillText(line, x, yy); return yy; }
function pillT(g, x, y, s, bg, fg, sz = 22) { g.font = F(800, sz); const w = g.measureText(s).width + sz * 1.2; g.fillStyle = bg; rr(g, x, y, w, sz * 1.7, sz * .85); g.fill(); g.fillStyle = fg; g.fillText(s, x + sz * .6, y + sz * 1.22); return w; }
function icon(g, k, cx, cy, s) {     // 0 teach: a lightbulb, 1 story: a speech bubble, 2 proof: a star
  g.save(); g.translate(cx, cy); g.scale(s, s); g.lineWidth = 7; g.lineJoin = "round"; g.lineCap = "round";
  const col = k === 2 ? LIME_S : INK_S; g.strokeStyle = col; g.fillStyle = col;
  if (k === 0) { g.beginPath(); g.arc(0, -8, 22, Math.PI * .8, Math.PI * 2.2); g.lineTo(9, 22); g.lineTo(-9, 22); g.closePath(); g.stroke(); g.fillRect(-10, 26, 20, 6); g.fillRect(-7, 35, 14, 5); }
  if (k === 1) { rr(g, -28, -24, 56, 40, 12); g.stroke(); g.beginPath(); g.moveTo(-10, 16); g.lineTo(-18, 30); g.lineTo(2, 16); g.stroke(); for (const x of [-12, 0, 12]) { g.beginPath(); g.arc(x, -4, 4, 0, 7); g.fill(); } }
  if (k === 2) { g.beginPath(); for (let i = 0; i < 10; i++) { const r = i % 2 ? 13 : 30, a = -Math.PI / 2 + i * Math.PI / 5; g.lineTo(Math.cos(a) * r, Math.sin(a) * r); } g.closePath(); g.fill(); }
  g.restore();
}
const PROMPT_BLANKS = ["your niche", "who it's for", "your goal"];
const ANSWERS = [["NICHE", "Home workouts"], ["FOR", "Busy moms"], ["GOAL", "More clients"]];
async function buildTextures() {
  try { await Promise.all([800, 700, 600].map((w) => document.fonts.load(`${w} 40px Inter`))); } catch (e) {}
  const logoImg = await new Promise((res) => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = "assets/img/logo.png"; });
  // the board's day numbers (1-30 in each slot's top-left corner)
  TEX.calnums = text(1650, 1150, (g, w, h) => { g.clearRect(0, 0, w, h); const sx = w / 3.3, sy = h / 2.3; g.font = F(700, 26); g.fillStyle = "#A9A2A2";
    for (let i = 0; i < 30; i++) { const p = slotPos(i); const x = (p.x - (CAL.cx - 1.65)) * sx, y = (CAL.cy + 1.15 - p.y) * sy; g.fillText(String(i + 1), x - CAL.sw / 2 * sx + 14, y - CAL.sh / 2 * sy + 34); } });
  for (let k = 0; k < 3; k++) TEX["icon" + k] = text(128, 128, (g, w, h) => { g.clearRect(0, 0, w, h); icon(g, k, 64, 60, 1.25); });
  for (let k = 0; k < 3; k++) TEX["note" + k] = text(256, 256, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = INK_S; g.font = F(800, 30); g.fillText("STEP", 28, 62); g.font = F(800, 150); g.fillText(String(k + 1), 28, 210); });
  TEX.logo = text(512, 512, (g, w, h) => { g.fillStyle = OFF_S; rr(g, 0, 0, w, h, 40); g.fill(); if (logoImg) { const s = Math.min((w - 60) / logoImg.width, (h - 60) / logoImg.height); g.drawImage(logoImg, (w - logoImg.width * s) / 2, (h - logoImg.height * s) / 2, logoImg.width * s, logoImg.height * s); } });
  // the prompt card: the one prompt with three blanks (they fill in lime as she answers)
  const promptCard = (filled) => text(1000, 620, (g, w, h) => {
    g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); pillT(g, 40, 34, "THE PROMPT", INK_S, LIME_S, 26);
    g.font = F(800, 50); g.fillStyle = INK_S; let y = 170;
    const parts = [["I make ", 0], [" content for ", 1], [". My goal is ", 2], [". Plan my next 30 days.", -1]];
    let x = 44; const lh = 74;
    const put = (s, bg) => { for (const word of s.split(/(\s+)/)) { if (!word) continue; const ww = g.measureText(word).width; if (x + ww > w - 40 && word.trim()) { x = 44; y += lh; } if (bg && word.trim()) { g.fillStyle = bg; rr(g, x - 6, y - 46, ww + 12, 62, 12); g.fill(); g.fillStyle = INK_S; } if (word.trim()) g.fillText(word, x, y); x += ww; } };
    put("I make", null); put(" ", null);
    put(filled ? ANSWERS[0][1].toLowerCase() : "[" + PROMPT_BLANKS[0] + "]", LIME_S); put(" content for ", null);
    put(filled ? ANSWERS[1][1].toLowerCase() : "[" + PROMPT_BLANKS[1] + "]", LIME_S); put(". My goal is ", null);
    put(filled ? ANSWERS[2][1].toLowerCase() : "[" + PROMPT_BLANKS[2] + "]", LIME_S); put(". Plan my next 30 days.", null);
  });
  TEX.prompt = promptCard(false); TEX.promptFilled = promptCard(true);
  for (let k = 0; k < 3; k++) TEX["in" + k] = text(620, 200, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); pillT(g, 28, 30, ANSWERS[k][0], INK_S, LIME_S, 26); g.font = F(800, 58); g.fillStyle = INK_S; g.fillText(ANSWERS[k][1], 30, 158); });
  for (let k = 0; k < 3; k++) TEX["pill" + k] = text(460, 140, (g, w, h) => { g.clearRect(0, 0, w, h); const lab = ["TEACH", "STORY", "PROOF"][k]; g.fillStyle = [INK_S, "#FFFFFF", LIME_S][k]; rr(g, 0, 0, w, h, 70); g.fill(); g.font = F(800, 70); g.fillStyle = [LIME_S, PINK_S, INK_S][k]; const tw = g.measureText(lab).width; g.fillText(lab, (w - tw) / 2, 96); });
  TEX.menu = text(1700, 900, (g, w, h) => { g.fillStyle = INK_S; g.fillRect(0, 0, w, h); g.font = F(800, 96); g.fillStyle = LIME_S; g.fillText("THE MENU", 70, 140);
    const items = [["TEACH", "how-to tips", LIME_S], ["STORY", "your journey", PINK_S], ["PROOF", "results, wins", "#FFFFFF"]];
    items.forEach(([a, b, c], i) => { const y = 300 + i * 200; g.fillStyle = c; g.beginPath(); g.arc(110, y - 30, 26, 0, 7); g.fill(); g.font = F(800, 92); g.fillStyle = "#FFFFFF"; g.fillText(a, 170, y); g.font = F(600, 64); g.fillStyle = "#B9B9B9"; g.fillText(b, 720, y); });
    g.font = F(700, 46); g.fillStyle = "#8A8A8A"; g.fillText("never run out of dishes", 70, 860); });
  TEX.day9 = text(1150, 820, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = LIME_S; g.fillRect(0, 0, w, 16);
    pillT(g, 50, 60, "DAY 9", INK_S, LIME_S, 34); pillT(g, 270, 60, "TEACH", LIME_S, INK_S, 34);
    g.font = F(800, 78); g.fillStyle = INK_S; const y = wrap(g, "The 4-minute workout you can do while the kettle boils", 50, 250, w - 100, 92);
    g.font = F(700, 44); g.fillStyle = "#6A6A6A"; g.fillText("Format: tutorial", 50, y + 110); g.fillStyle = PINK_S; g.fillText("Hook: under 12 words", 50, y + 175); });
  TEX.clap = text(460, 260, (g, w, h) => { g.fillStyle = INK_S; g.fillRect(0, 0, w, h); g.font = F(800, 44); g.fillStyle = "#FFFFFF"; g.fillText("BATCH DAY", 24, 70); g.font = F(700, 34); g.fillStyle = LIME_S; g.fillText("7 POSTS · 1 AFTERNOON", 24, 140); g.fillStyle = "#777"; g.font = F(600, 28); g.fillText("SCENE 1-7   TAKE 1", 24, 210); });
  TEX.claptop = text(480, 50, (g, w, h) => { for (let i = 0; i < 12; i++) { g.fillStyle = i % 2 ? "#FFFFFF" : INK_S; g.beginPath(); g.moveTo(i * 44, h); g.lineTo(i * 44 + 22, 0); g.lineTo(i * 44 + 44, 0); g.lineTo(i * 44 + 22, h); g.fill(); } });
  TEX.tick = text(128, 128, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = LIME_S; g.beginPath(); g.arc(64, 64, 58, 0, 7); g.fill(); g.strokeStyle = INK_S; g.lineWidth = 14; g.lineCap = "round"; g.lineJoin = "round"; g.beginPath(); g.moveTo(36, 66); g.lineTo(56, 86); g.lineTo(94, 44); g.stroke(); });
  TEX.phone = text(132, 276, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#EEE"; g.fillRect(0, 0, w, 40); g.font = F(700, 13); g.fillStyle = "#888"; g.fillText("Last post", 14, 90); g.font = F(800, 30); g.fillStyle = PINK_S; g.fillText("14 days", 14, 128); g.font = F(700, 13); g.fillStyle = "#888"; g.fillText("ago", 14, 150); for (let i = 0; i < 3; i++) { g.fillStyle = "#E4E4E4"; g.fillRect(10 + i * 40, 180, 34, 44); } });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  TEX.ready = true;
}

const ready = (async () => {
  await buildTextures();
  scene.traverse((o) => { if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  RM.visible = true;
  renderer.compile(scene, camera);
  renderAt(window.CR_COVER ? window.CR_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["plan"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.CR_COVER ? window.CR_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C };
