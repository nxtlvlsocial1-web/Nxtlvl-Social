
// ---------------------------------------------------------------- textures (no words anywhere in the 3D world; words live in the HTML layer)
const text = (w, h, draw) => pix(w, h, draw, false);
function buildTextures() {
  TEX.sky = text(1024, 768, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#0B1440"); gr.addColorStop(.6, "#1D2C6E"); gr.addColorStop(1, "#33407E"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 220; i++) { const x = hash(i * 3.1) * w, y = hash(i * 7.7) * h * .85, r = hash(i * 1.9) * 1.8 + .5; g.fillStyle = `rgba(255,250,240,${.35 + hash(i) * .65})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
    const mx = 640, my = 220; const mg = g.createRadialGradient(mx, my, 20, mx, my, 110); mg.addColorStop(0, "rgba(255,248,230,.35)"); mg.addColorStop(1, "rgba(255,248,230,0)"); g.fillStyle = mg; g.fillRect(mx - 120, my - 120, 240, 240);
    g.fillStyle = "#FFF6E2"; g.beginPath(); g.arc(mx, my, 46, 0, 7); g.fill(); g.fillStyle = "#1D2C6E"; g.beginPath(); g.arc(mx + 20, my - 12, 42, 0, 7); g.fill();
  });
  for (let k = 0; k < 3; k++) TEX["cloud" + k] = text(512, 160, (g, w, h) => { g.clearRect(0, 0, w, h); for (let i = 0; i < 9; i++) { const x = 60 + i * 48 + hash(i + k * 9) * 30, y = 90 + Math.sin(i) * 14, r = 34 + hash(i * 3 + k) * 26; const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, "rgba(120,130,190,.55)"); gr.addColorStop(1, "rgba(120,130,190,0)"); g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); } });
  TEX.posters = text(600, 440, (g, w, h) => {
    g.clearRect(0, 0, w, h); g.fillStyle = "#C9BBDD"; g.fillRect(0, 0, w, h);
    const art = (x, y, ww, hh, c1, c2, k) => { g.fillStyle = "#FFFFFF"; g.fillRect(x - 8, y - 8, ww + 16, hh + 16); const gr = g.createLinearGradient(x, y, x + ww, y + hh); gr.addColorStop(0, c1); gr.addColorStop(1, c2); g.fillStyle = gr; g.fillRect(x, y, ww, hh);
      g.fillStyle = "rgba(255,255,255,.7)"; if (k === 0) { g.beginPath(); g.arc(x + ww / 2, y + hh * .45, ww * .26, 0, 7); g.fill(); } else if (k === 1) { g.beginPath(); g.moveTo(x + ww * .2, y + hh * .8); g.lineTo(x + ww * .5, y + hh * .3); g.lineTo(x + ww * .8, y + hh * .8); g.fill(); } else { for (let i = 0; i < 4; i++) g.fillRect(x + ww * .2 + i * ww * .16, y + hh * (.75 - i * .12), ww * .1, hh * (.1 + i * .12)); } };
    art(30, 40, 170, 230, "#2A1E5A", "#E8577E", 0); art(240, 70, 130, 170, "#F2C94C", "#F38BA0", 1); art(410, 30, 150, 220, "#5B7FC4", "#B79CFF", 2); art(260, 280, 110, 120, "#7FC8A9", "#3E7CB1", 0);
  });
  for (let k = 0; k < 4; k++) TEX["thumb" + k] = text(160, 260, (g, w, h) => {
    const P = [["#F343A2", "#FF9A6A"], ["#7A5CFF", "#FF8CC6"], ["#F2C94C", "#E8735A"], ["#3EC6C0", "#7A5CFF"]][k];
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, P[0]); gr.addColorStop(1, P[1]); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,.88)"; g.beginPath(); g.arc(w / 2, h * .42, 30, 0, 7); g.fill();
    g.fillStyle = P[0]; g.beginPath(); g.moveTo(w / 2 - 9, h * .42 - 15); g.lineTo(w / 2 - 9, h * .42 + 15); g.lineTo(w / 2 + 15, h * .42); g.fill();
    g.fillStyle = "rgba(255,255,255,.7)"; rr(g, 16, h - 50, w - 32, 12, 6); g.fill(); rr(g, 16, h - 30, w * .5, 12, 6); g.fill();
  });
  TEX.knit = text(256, 256, (g, w, h) => { g.fillStyle = "#E9A0B8"; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 16) for (let x = 0; x < w; x += 16) { g.fillStyle = (x / 16 + y / 16) % 2 ? "#E393AE" : "#EEADC2"; g.beginPath(); g.ellipse(x + 4, y + 8, 4, 7, -.5, 0, 7); g.fill(); g.beginPath(); g.ellipse(x + 12, y + 8, 4, 7, .5, 0, 7); g.fill(); } });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; if (key === "knit") { m.map.wrapS = m.map.wrapT = THREE.RepeatWrapping; m.map.repeat.set(3, 3); } m.needsUpdate = true; } }
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
