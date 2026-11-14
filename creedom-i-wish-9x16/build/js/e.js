
// ---------------------------------------------------------------- textures (no text anywhere in the 3D world; words live in the HTML layer)
const text = (w, h, draw) => pix(w, h, draw, false);
function buildTextures() {
  TEX.night = text(512, 512, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#0E0A2A"); gr.addColorStop(.7, "#2A1A4A"); gr.addColorStop(1, "#4A2456"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 90; i++) { const x = hash(i * 3.1) * w, y = hash(i * 7.7) * h * .7, r = hash(i * 1.9) * 1.6 + .4; g.fillStyle = `rgba(255,240,250,${.4 + hash(i) * .6})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
    const mg = g.createRadialGradient(360, 120, 10, 360, 120, 120); mg.addColorStop(0, "rgba(255,240,220,.55)"); mg.addColorStop(1, "rgba(255,240,220,0)"); g.fillStyle = mg; g.fillRect(200, 0, 312, 260);
    g.fillStyle = "#FFF4E2"; g.beginPath(); g.arc(360, 120, 42, 0, 7); g.fill(); g.fillStyle = "rgba(220,200,190,.5)"; g.beginPath(); g.arc(348, 110, 9, 0, 7); g.arc(372, 132, 6, 0, 7); g.fill();
    for (let b = 0; b < 7; b++) { const x0 = b * 78 - 8, top = 330 + (b * 41 % 110); g.fillStyle = ["#1A1230", "#22183A", "#1E1534"][b % 3]; g.fillRect(x0, top, 72, h - top); for (let i = 0; i < 3; i++) for (let j = 0; j < 6; j++) { g.fillStyle = (b * 7 + i * 3 + j) % 4 ? "#FFC98A" : "#3A2A50"; g.fillRect(x0 + 10 + i * 20, top + 14 + j * 26, 10, 13); } }
  });
  TEX.posters = text(512, 360, (g, w, h) => {
    g.fillStyle = "#6E5A86"; g.fillRect(0, 0, w, h);
    const art = (x, y, ww, hh, c1, c2, k) => { const gr = g.createLinearGradient(x, y, x + ww, y + hh); gr.addColorStop(0, c1); gr.addColorStop(1, c2); g.fillStyle = "#FFF8F2"; g.fillRect(x - 8, y - 8, ww + 16, hh + 16); g.fillStyle = gr; g.fillRect(x, y, ww, hh);
      g.fillStyle = "rgba(255,255,255,.75)"; if (k === 0) { g.beginPath(); g.arc(x + ww / 2, y + hh / 2, ww * .28, 0, 7); g.fill(); } else if (k === 1) { g.beginPath(); g.moveTo(x + ww * .38, y + hh * .3); g.lineTo(x + ww * .38, y + hh * .7); g.lineTo(x + ww * .7, y + hh * .5); g.fill(); } else { for (let i = 0; i < 4; i++) g.fillRect(x + ww * .2 + i * ww * .16, y + hh * (.7 - i * .12), ww * .1, hh * (.12 + i * .12)); } };
    art(30, 40, 140, 190, "#F343A2", "#FF9A6A", 0); art(200, 70, 120, 150, "#5B7FC4", "#B79CFF", 1); art(352, 30, 130, 200, "#F2C94C", "#F343A2", 2);
  });
  for (let k = 0; k < 4; k++) TEX["thumb" + k] = text(128, 220, (g, w, h) => {
    const P = [["#F343A2", "#FF9A6A"], ["#7A5CFF", "#FF8CC6"], ["#F2C94C", "#E8735A"], ["#3EC6C0", "#7A5CFF"]][k];
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, P[0]); gr.addColorStop(1, P[1]); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,.85)"; g.beginPath(); g.arc(w / 2, h * .42, 26, 0, 7); g.fill();
    g.fillStyle = P[0]; g.beginPath(); g.moveTo(w / 2 - 8, h * .42 - 13); g.lineTo(w / 2 - 8, h * .42 + 13); g.lineTo(w / 2 + 13, h * .42); g.fill();
    g.fillStyle = "rgba(255,255,255,.7)"; rr(g, 14, h - 44, w - 28, 10, 5); g.fill(); rr(g, 14, h - 26, w * .5, 10, 5); g.fill();
  });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  TEX.ready = true;
}

const ready = (async () => {
  buildTextures();
  scene.traverse((o) => { if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  RM.visible = true;
  renderer.compile(scene, camera);
  renderAt(window.CR_COVER ? window.CR_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["cree"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.CR_COVER ? window.CR_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C };
