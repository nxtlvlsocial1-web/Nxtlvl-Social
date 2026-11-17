// Canvas textures for Respawn: the sunset city, the hospital, the radio, the heart monitor, Lily's drawing.
// Every texture is drawn from a seed, so each render paints identical pixels.
import * as THREE from "three";
import { rng } from "./util.js";

const F = (w, s) => `${w} ${s}px Poppins, sans-serif`;

function canvas(w, h) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  return [c, c.getContext("2d")];
}
function tex(c, { repeat = [1, 1], srgb = true, clamp = false } = {}) {
  const t = new THREE.CanvasTexture(c);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = clamp ? THREE.ClampToEdgeWrapping : THREE.RepeatWrapping;
  t.repeat.set(repeat[0], repeat[1]);
  t.anisotropy = 8;
  t.needsUpdate = true;
  return t;
}

// sky dome: vertical gradient, horizon at v = 0.5, optional clouds lit from below
export function sunsetSky({ seed = 3 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(512, 1024);
  const gr = g.createLinearGradient(0, 0, 0, 1024);
  gr.addColorStop(0.0, "#1c1840");
  gr.addColorStop(0.2, "#3b2466");
  gr.addColorStop(0.34, "#8a3a7c");
  gr.addColorStop(0.43, "#e8607a");
  gr.addColorStop(0.48, "#ff9a5a");
  gr.addColorStop(0.505, "#ffd38a");
  gr.addColorStop(0.53, "#c85a5a");
  gr.addColorStop(1.0, "#2a1530");
  g.fillStyle = gr;
  g.fillRect(0, 0, 512, 1024);
  // long thin clouds, warm undersides
  for (let i = 0; i < 26; i++) {
    const y = 240 + r() * 220, x = r() * 512, w = 60 + r() * 180, h = 4 + r() * 9;
    const k = (y - 240) / 220;
    g.fillStyle = `rgba(${Math.round(255)},${Math.round(150 + k * 70)},${Math.round(150 - k * 40)},${0.18 + r() * 0.22})`;
    g.beginPath();
    g.ellipse(x, y, w, h, 0, 0, Math.PI * 2);
    g.fill();
    g.beginPath();
    g.ellipse(x - 512, y, w, h, 0, 0, Math.PI * 2);
    g.fill();
  }
  return tex(c, { clamp: false });
}

// the sky glitching into a hospital ceiling: square acoustic tiles with pinholes and a strip light
export function ceilingSky() {
  const [c, g] = canvas(512, 512);
  const r = rng(77);
  g.fillStyle = "#9aa3a6";
  g.fillRect(0, 0, 512, 512);
  for (let y = 0; y < 512; y += 64)
    for (let x = 0; x < 512; x += 64) {
      g.fillStyle = `rgb(${226 + r() * 10},${229 + r() * 8},${226 + r() * 6})`;
      g.fillRect(x + 3, y + 3, 58, 58);
      g.fillStyle = "rgba(90,96,98,0.35)";
      for (let i = 0; i < 40; i++) g.fillRect(x + 6 + r() * 52, y + 6 + r() * 52, 2, 2);
    }
  g.fillStyle = "#f6fbff";
  g.fillRect(131, 195, 122, 58);
  return tex(c, { repeat: [16, 8] });
}

// pastel art-deco facade: base colour, horizontal bands, window grid, optional lit windows
export function facade({ base = "#f2a7b8", trim = "#ffffff", glass = "#2d6f7c", floors = 5, cols = 4, seed = 1, lit = 0.25 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 512);
  g.fillStyle = base;
  g.fillRect(0, 0, 256, 512);
  const fh = 512 / floors;
  for (let f = 0; f < floors; f++) {
    const y = f * fh;
    g.fillStyle = trim;
    g.globalAlpha = 0.9;
    g.fillRect(0, y + fh - 8, 256, 6);
    g.globalAlpha = 1;
    if (f === floors - 1) continue; // ground floor: shopfront drawn below
    const cw = 256 / cols;
    for (let k = 0; k < cols; k++) {
      const x = k * cw + cw * 0.18, w = cw * 0.64, h = fh * 0.52;
      const on = r() < lit;
      g.fillStyle = on ? "#ffd58a" : glass;
      g.fillRect(x, y + fh * 0.2, w, h);
      g.fillStyle = "rgba(255,255,255,0.25)";
      g.fillRect(x, y + fh * 0.2, w, 3);
      g.fillStyle = trim;
      g.fillRect(x - 3, y + fh * 0.2 + h, w + 6, 5);
    }
  }
  // ground floor shopfront: wide glass and a dark door
  const y0 = (floors - 1) * fh;
  g.fillStyle = "#1f3a44";
  g.fillRect(14, y0 + fh * 0.18, 228, fh * 0.72);
  g.fillStyle = "rgba(255,210,150,0.35)";
  g.fillRect(14, y0 + fh * 0.18, 228, fh * 0.72);
  g.fillStyle = "#121a1e";
  g.fillRect(108, y0 + fh * 0.3, 40, fh * 0.6);
  // rounded deco fins on top
  g.fillStyle = trim;
  g.fillRect(0, 0, 256, 10);
  return tex(c);
}

// neon sign: glowing tube letters on dark backing (used as an emissive map)
export function neon(text, color = "#ff4fa3", { w = 512, h = 160 } = {}) {
  const [c, g] = canvas(w, h);
  g.fillStyle = "#14101a";
  g.fillRect(0, 0, w, h);
  g.font = F(800, Math.round(h * 0.56));
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.shadowColor = color;
  g.shadowBlur = 24;
  g.strokeStyle = color;
  g.lineWidth = 7;
  g.strokeText(text, w / 2, h / 2 + 4);
  g.shadowBlur = 0;
  g.strokeStyle = "#ffffff";
  g.lineWidth = 2.5;
  g.strokeText(text, w / 2, h / 2 + 4);
  return tex(c, { clamp: true });
}

export function hospitalSign() {
  const [c, g] = canvas(1024, 200);
  g.fillStyle = "#1f5fa8";
  g.fillRect(0, 0, 1024, 200);
  g.fillStyle = "#ffffff";
  g.fillRect(28, 28, 144, 144);
  g.fillStyle = "#1f5fa8";
  g.font = F(800, 130);
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText("H", 100, 108);
  g.fillStyle = "#ffffff";
  g.font = F(800, 112);
  g.textAlign = "left";
  g.fillText("HOSPITAL", 214, 108);
  return tex(c, { clamp: true });
}

export function roofH() {
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#1f5fa8";
  g.fillRect(0, 0, 256, 256);
  g.fillStyle = "#ffffff";
  g.font = F(800, 220);
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText("H", 128, 140);
  return tex(c, { clamp: true });
}

// hospital facade: off-white with long blue window bands
export function hospitalFacade() {
  const [c, g] = canvas(512, 512);
  g.fillStyle = "#e9e4da";
  g.fillRect(0, 0, 512, 512);
  for (let f = 0; f < 6; f++) {
    const y = 20 + f * 72;
    g.fillStyle = "#3d6f96";
    g.fillRect(10, y, 492, 34);
    g.fillStyle = "rgba(255,255,255,0.22)";
    g.fillRect(10, y, 492, 4);
    g.fillStyle = "#e9e4da";
    for (let x = 10; x < 512; x += 62) g.fillRect(x, y, 5, 34);
  }
  return tex(c);
}

// road: asphalt with a dashed yellow centre line and white edge lines (v runs along the road)
export function road({ seed = 9 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 512);
  g.fillStyle = "#3a3a40";
  g.fillRect(0, 0, 256, 512);
  for (let i = 0; i < 9000; i++) {
    const v = Math.floor(40 + r() * 45);
    g.fillStyle = `rgba(${v},${v},${v + 4},0.55)`;
    g.fillRect(r() * 256, r() * 512, 1 + r() * 2, 1 + r() * 2);
  }
  g.fillStyle = "#f2c94c";
  g.fillRect(122, 0, 5, 512);
  g.fillRect(130, 0, 5, 512);
  g.fillStyle = "#e9e9e4";
  for (const x of [14, 238]) g.fillRect(x, 0, 5, 512);
  for (let y = 0; y < 512; y += 128) {
    g.fillRect(66, y, 4, 64);
    g.fillRect(186, y, 4, 64);
  }
  return tex(c);
}

export function sand({ seed = 21, repeat = [8, 8] } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#e8c995";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 9000; i++) {
    const k = r();
    g.fillStyle = k < 0.5 ? `rgba(160,120,70,${r() * 0.25})` : `rgba(255,245,220,${r() * 0.35})`;
    g.fillRect(r() * 256, r() * 256, 1 + r() * 2, 1 + r() * 2);
  }
  return tex(c, { repeat });
}

export function sea({ seed = 22, repeat = [6, 6] } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#2d6f8e";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 260; i++) {
    g.fillStyle = `rgba(${r() < 0.5 ? "255,190,140" : "180,230,255"},${0.12 + r() * 0.25})`;
    g.fillRect(r() * 256, r() * 256, 10 + r() * 40, 2);
  }
  return tex(c, { repeat });
}

export function bark({ repeat = [1, 6] } = {}) {
  const [c, g] = canvas(64, 64);
  g.fillStyle = "#8a6a48";
  g.fillRect(0, 0, 64, 64);
  g.fillStyle = "#6e5236";
  g.fillRect(0, 0, 64, 10);
  g.fillStyle = "rgba(255,230,190,0.18)";
  g.fillRect(0, 10, 64, 4);
  return tex(c, { repeat });
}

// car radio display: amber LCD, big frequency or scrolling text, optional static
export function makeRadioScreen() {
  const [c, g] = canvas(512, 192);
  const t = tex(c, { clamp: true });
  let key = "";
  function set(top, big, noise = 0, seed = 1) {
    const k = top + "|" + big + "|" + noise.toFixed(2) + "|" + seed;
    if (k === key) return;
    key = k;
    g.fillStyle = "#170c04";
    g.fillRect(0, 0, 512, 192);
    g.fillStyle = "rgba(255,160,60,0.07)";
    for (let y = 0; y < 192; y += 4) g.fillRect(0, y, 512, 2);
    g.textBaseline = "middle";
    g.shadowColor = "#ffae4a";
    g.shadowBlur = 14;
    g.fillStyle = "#ffb453";
    g.font = F(700, 30);
    g.textAlign = "left";
    g.fillText(top, 26, 36);
    g.font = F(800, big.length > 9 ? 58 : 84);
    g.textAlign = "center";
    g.fillText(big, 256, 122);
    g.shadowBlur = 0;
    if (noise > 0) {
      const r = rng(seed);
      for (let i = 0; i < 1400 * noise; i++) {
        const v = r() < 0.5 ? "255,190,110" : "10,6,2";
        g.fillStyle = `rgba(${v},${0.25 + r() * 0.6})`;
        g.fillRect(r() * 512, r() * 192, 2 + r() * 10, 2);
      }
    }
    t.needsUpdate = true;
  }
  set("FM", "88.1");
  return { texture: t, set };
}

// heart monitor: black panel, sweeping green trace, readouts. set(time, {bpm, rhythm})
export function makeMonitor() {
  const [c, g] = canvas(512, 320);
  const t = tex(c, { clamp: true });
  let key = "";
  const beat = (x) => {
    // one PQRST complex on x in [0, 1)
    const p = 0.12 * Math.exp(-(((x - 0.12) / 0.035) ** 2));
    const q = -0.12 * Math.exp(-(((x - 0.255) / 0.012) ** 2));
    const rr = 1.0 * Math.exp(-(((x - 0.28) / 0.014) ** 2));
    const s = -0.25 * Math.exp(-(((x - 0.305) / 0.014) ** 2));
    const tt = 0.22 * Math.exp(-(((x - 0.5) / 0.06) ** 2));
    return p + q + rr + s + tt;
  };
  function set(time, { bpm = 42, color = "#3dff7a", label = "HR" } = {}) {
    const k = (Math.round(time * 24) / 24).toFixed(3) + bpm + color;
    if (k === key) return;
    key = k;
    g.fillStyle = "#04100a";
    g.fillRect(0, 0, 512, 320);
    g.strokeStyle = "rgba(61,255,122,0.08)";
    g.lineWidth = 1;
    for (let x = 0; x < 512; x += 32) { g.beginPath(); g.moveTo(x, 20); g.lineTo(x, 230); g.stroke(); }
    for (let y = 20; y < 232; y += 32) { g.beginPath(); g.moveTo(0, y); g.lineTo(512, y); g.stroke(); }
    // sweeping trace: 4 s across the screen, erase bar ahead of the pen
    const span = 4, pen = ((time % span) / span) * 512, period = 60 / bpm;
    g.strokeStyle = color;
    g.lineWidth = 4;
    g.shadowColor = color;
    g.shadowBlur = 12;
    g.beginPath();
    let first = true;
    for (let x = 0; x < 512; x += 2) {
      if (x > pen && x < pen + 26) { first = true; continue; }
      const tx = x <= pen ? time - (pen - x) / 512 * span : time - span - (pen - x) / 512 * span;
      const secs = ((tx % period) + period) % period; // seconds since the last beat
      const xb = secs / Math.min(period, 0.7); // the complex lasts 0.7 s, then the line is flat
      const y = 150 - (xb < 1 ? beat(xb) : 0) * 110;
      if (first) { g.moveTo(x, y); first = false; } else g.lineTo(x, y);
    }
    g.stroke();
    g.shadowBlur = 0;
    g.fillStyle = color;
    g.font = F(800, 64);
    g.textBaseline = "middle";
    g.textAlign = "left";
    g.fillText(`${label} ${bpm}`, 24, 276);
    g.fillStyle = "#5fd7ff";
    g.font = F(800, 46);
    g.textAlign = "right";
    g.fillText("SpO2 96", 492, 280);
    t.needsUpdate = true;
  }
  set(0);
  return { texture: t, set };
}

// Lily's drawing taped to the wall: house, Daddy and Lily holding hands, a heart, crayon words
export function crayonDrawing() {
  const r = rng(31);
  const [c, g] = canvas(512, 384);
  g.fillStyle = "#fbf8f0";
  g.fillRect(0, 0, 512, 384);
  const crayon = (col, w, pts) => {
    g.strokeStyle = col;
    g.lineWidth = w;
    g.lineCap = "round";
    g.lineJoin = "round";
    for (let pass = 0; pass < 2; pass++) {
      g.beginPath();
      pts.forEach(([x, y], i) => {
        const jx = x + (r() - 0.5) * 3, jy = y + (r() - 0.5) * 3;
        if (i) g.lineTo(jx, jy); else g.moveTo(jx, jy);
      });
      g.stroke();
    }
  };
  // sun
  crayon("#f4b400", 6, Array.from({ length: 25 }, (_, i) => [70 + Math.cos(i / 24 * 6.283) * 30, 70 + Math.sin(i / 24 * 6.283) * 30]));
  for (let i = 0; i < 8; i++) { const a = i / 8 * 6.283; crayon("#f4b400", 4, [[70 + Math.cos(a) * 40, 70 + Math.sin(a) * 40], [70 + Math.cos(a) * 54, 70 + Math.sin(a) * 54]]); }
  // house
  crayon("#d9534f", 6, [[300, 250], [300, 170], [380, 120], [460, 170], [460, 250], [300, 250]]);
  crayon("#4a90d9", 5, [[365, 250], [365, 205], [395, 205], [395, 250]]);
  // Daddy (tall) and Lily (small) holding hands
  const person = (x, top, h, col) => {
    crayon(col, 5, Array.from({ length: 21 }, (_, i) => [x + Math.cos(i / 20 * 6.283) * h * 0.13, top + h * 0.13 + Math.sin(i / 20 * 6.283) * h * 0.13]));
    crayon(col, 5, [[x, top + h * 0.26], [x, top + h * 0.7]]);
    crayon(col, 5, [[x, top + h * 0.7], [x - h * 0.14, top + h]]);
    crayon(col, 5, [[x, top + h * 0.7], [x + h * 0.14, top + h]]);
  };
  person(130, 140, 130, "#2b5c9e");
  person(215, 190, 80, "#d6458a");
  crayon("#2b5c9e", 5, [[130, 190], [175, 225], [215, 228]]);
  crayon("#d6458a", 5, [[215, 228], [250, 220]]);
  // heart
  crayon("#e0245e", 6, [[255, 120], [240, 100], [252, 86], [266, 98], [280, 86], [292, 100], [277, 120], [266, 132], [255, 120]]);
  // words, wobbly crayon letters
  g.fillStyle = "#3b6fd1";
  g.font = F(800, 40);
  g.textBaseline = "middle";
  const words = "COME HOME DADDY";
  let x = 50;
  for (const ch of words) {
    g.save();
    g.translate(x, 330 + (r() - 0.5) * 8);
    g.rotate((r() - 0.5) * 0.25);
    g.fillText(ch, 0, 0);
    g.restore();
    x += ch === " " ? 18 : 29;
  }
  return tex(c, { clamp: true });
}

export function schoolSign() {
  const [c, g] = canvas(256, 256);
  g.clearRect(0, 0, 256, 256);
  g.save();
  g.translate(128, 128);
  g.rotate(Math.PI / 4);
  g.fillStyle = "#c8e02a";
  g.fillRect(-84, -84, 168, 168);
  g.strokeStyle = "#1b1b1b";
  g.lineWidth = 6;
  g.strokeRect(-76, -76, 152, 152);
  g.restore();
  g.fillStyle = "#1b1b1b";
  g.font = F(800, 40);
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText("SCHOOL", 128, 132);
  return tex(c, { clamp: true });
}

// one soft vertical streak for rain quads
export function streak() {
  const [c, g] = canvas(16, 128);
  const gr = g.createLinearGradient(0, 0, 0, 128);
  gr.addColorStop(0, "rgba(220,230,255,0)");
  gr.addColorStop(0.5, "rgba(220,230,255,0.9)");
  gr.addColorStop(1, "rgba(220,230,255,0)");
  g.fillStyle = gr;
  g.fillRect(6, 0, 4, 128);
  return tex(c, { clamp: true });
}

export function plate(text) {
  const [c, g] = canvas(256, 128);
  g.fillStyle = "#f4f1e8";
  g.fillRect(0, 0, 256, 128);
  g.strokeStyle = "#2a3a6a";
  g.lineWidth = 6;
  g.strokeRect(6, 6, 244, 116);
  g.fillStyle = "#2a3a6a";
  g.font = F(800, 64);
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText(text, 128, 70);
  return tex(c, { clamp: true });
}

// blank speed-limit style sign (generic): white panel with a number
export function speedSign(n = 30) {
  const [c, g] = canvas(128, 160);
  g.fillStyle = "#f2f2ee";
  g.fillRect(0, 0, 128, 160);
  g.strokeStyle = "#1b1b1b";
  g.lineWidth = 5;
  g.strokeRect(6, 6, 116, 148);
  g.fillStyle = "#1b1b1b";
  g.font = F(800, 22);
  g.textAlign = "center";
  g.fillText("SPEED", 64, 34);
  g.fillText("LIMIT", 64, 58);
  g.font = F(800, 64);
  g.fillText(String(n), 64, 118);
  return tex(c, { clamp: true });
}
