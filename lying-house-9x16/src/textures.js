// Procedural canvas textures (seeded, so every render draws identical pixels).
import * as THREE from "three";
import { rng } from "./util.js";

function canvas(w, h) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  return [c, c.getContext("2d")];
}

function tex(c, { repeat = [1, 1], srgb = true, aniso = 8 } = {}) {
  const t = new THREE.CanvasTexture(c);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(repeat[0], repeat[1]);
  t.anisotropy = aniso;
  t.needsUpdate = true;
  return t;
}

const hsl = (h, s, l) => `hsl(${h},${s}%,${l}%)`;

export function woodFloor({ seed = 1, base = [28, 48, 33], plankW = 64, repeat = [6, 6] } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(512, 512);
  const rows = 512 / plankW;
  for (let row = 0; row < rows; row++) {
    let x = -r() * 300;
    while (x < 512) {
      const len = 180 + r() * 220;
      const l = base[2] + (r() - 0.5) * 9;
      g.fillStyle = hsl(base[0] + (r() - 0.5) * 6, base[1], l);
      g.fillRect(x, row * plankW, len, plankW);
      // grain
      for (let k = 0; k < 14; k++) {
        g.strokeStyle = `rgba(40,20,8,${0.05 + r() * 0.12})`;
        g.lineWidth = 1 + r() * 2;
        const y = row * plankW + r() * plankW;
        g.beginPath();
        g.moveTo(x, y);
        for (let s = 0; s <= 6; s++) g.lineTo(x + (len * s) / 6, y + Math.sin(s * 1.3 + k) * 3 * r());
        g.stroke();
      }
      g.fillStyle = "rgba(20,10,4,0.55)";
      g.fillRect(x, row * plankW, 3, plankW);
      x += len;
    }
    g.fillStyle = "rgba(20,10,4,0.6)";
    g.fillRect(0, row * plankW, 512, 3);
  }
  return tex(c, { repeat });
}

export function wallpaper({ seed = 2, color = [285, 22, 30], stripe = true, repeat = [8, 3] } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = hsl(...color);
  g.fillRect(0, 0, 256, 256);
  if (stripe) {
    for (let x = 0; x < 256; x += 32) {
      g.fillStyle = hsl(color[0], color[1], color[2] + 3);
      g.fillRect(x, 0, 12, 256);
    }
  }
  // fine noise / plaster speckle
  for (let i = 0; i < 4000; i++) {
    g.fillStyle = `rgba(${r() < 0.5 ? "0,0,0" : "255,255,255"},${r() * 0.05})`;
    g.fillRect(r() * 256, r() * 256, 2, 2);
  }
  return tex(c, { repeat });
}

export function plaster({ seed = 3, color = [35, 20, 82], repeat = [6, 6] } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = hsl(...color);
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 6000; i++) {
    g.fillStyle = `rgba(${r() < 0.5 ? "60,40,20" : "255,255,255"},${r() * 0.08})`;
    const s = 1 + r() * 3;
    g.fillRect(r() * 256, r() * 256, s, s);
  }
  return tex(c, { repeat });
}

// knitted fabric: rows of little V stitches
export function knit({ colors = ["#6b4a2e", "#8a6a3a", "#3f5b4e", "#9c3b2e"], band = 6, repeat = [4, 4], seed = 4 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  const st = 8;
  for (let y = 0; y < 256; y += st) {
    const ci = Math.floor(y / (st * band)) % colors.length;
    for (let x = 0; x < 256; x += st) {
      const alt = (Math.floor(x / st) + Math.floor(y / st)) % 7 === 0 && ci % 2 === 1;
      g.fillStyle = alt ? colors[(ci + 1) % colors.length] : colors[ci];
      g.beginPath();
      g.moveTo(x, y);
      g.lineTo(x + st / 2, y + st);
      g.lineTo(x + st, y);
      g.lineTo(x + st / 2, y + st * 0.45);
      g.closePath();
      g.fill();
      g.fillStyle = `rgba(0,0,0,${0.15 + r() * 0.1})`;
      g.fillRect(x + st / 2 - 0.5, y, 1, st);
    }
  }
  return tex(c, { repeat });
}

export function velvet({ color = [130, 25, 28], repeat = [2, 2], seed = 5 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = hsl(...color);
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 9000; i++) {
    g.fillStyle = `rgba(${r() < 0.5 ? "0,0,0" : "255,255,255"},${r() * 0.06})`;
    g.fillRect(r() * 256, r() * 256, 1 + r() * 2, 1);
  }
  return tex(c, { repeat });
}

export function rug({ seed = 6 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(512, 768);
  const bands = ["#7a2a1e", "#c8742f", "#e3b36a", "#a8432a", "#5a1f18"];
  for (let i = 0; i < 9; i++) {
    g.fillStyle = bands[i % bands.length];
    const m = i * 26;
    g.fillRect(m, m, 512 - 2 * m, 768 - 2 * m);
  }
  g.fillStyle = "#d9a35a";
  g.fillRect(240, 240, 32, 288);
  // weave noise
  for (let i = 0; i < 20000; i++) {
    g.fillStyle = `rgba(${r() < 0.5 ? "0,0,0" : "255,240,220"},${r() * 0.08})`;
    g.fillRect(r() * 512, r() * 768, 2, 1);
  }
  return tex(c, { repeat: [1, 1] });
}

export function siding({ color = [215, 25, 45], repeat = [3, 3], seed = 7 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  for (let y = 0; y < 256; y += 32) {
    g.fillStyle = hsl(color[0], color[1], color[2] + (r() - 0.5) * 4);
    g.fillRect(0, y, 256, 32);
    g.fillStyle = "rgba(0,0,0,0.35)";
    g.fillRect(0, y + 29, 256, 3);
    g.fillStyle = "rgba(255,255,255,0.08)";
    g.fillRect(0, y, 256, 3);
  }
  for (let i = 0; i < 3000; i++) {
    g.fillStyle = `rgba(0,0,0,${r() * 0.06})`;
    g.fillRect(r() * 256, r() * 256, 3, 1);
  }
  return tex(c, { repeat });
}

export function brick({ repeat = [3, 3], seed = 8 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#c9bfb2";
  g.fillRect(0, 0, 256, 256);
  for (let row = 0; row < 8; row++) {
    const off = row % 2 ? 32 : 0;
    for (let x = -off; x < 256; x += 64) {
      g.fillStyle = hsl(10 + r() * 10, 45, 32 + r() * 10);
      g.fillRect(x + 2, row * 32 + 2, 60, 28);
    }
  }
  return tex(c, { repeat });
}

export function asphalt({ repeat = [8, 8], seed = 9 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#2a2b30";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 12000; i++) {
    const v = Math.floor(30 + r() * 40);
    g.fillStyle = `rgba(${v},${v},${v + 4},0.5)`;
    g.fillRect(r() * 256, r() * 256, 1 + r() * 2, 1 + r() * 2);
  }
  return tex(c, { repeat });
}

export function concrete({ repeat = [4, 4], seed = 10 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#8d8a84";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 8000; i++) {
    g.fillStyle = `rgba(${r() < 0.5 ? "0,0,0" : "255,255,255"},${r() * 0.07})`;
    g.fillRect(r() * 256, r() * 256, 2, 2);
  }
  g.fillStyle = "rgba(0,0,0,0.35)";
  g.fillRect(0, 0, 256, 2);
  g.fillRect(0, 0, 2, 256);
  return tex(c, { repeat });
}

export function grass({ repeat = [6, 6], seed = 11 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#2f4a26";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 9000; i++) {
    g.strokeStyle = hsl(95 + r() * 25, 40, 20 + r() * 20);
    g.beginPath();
    const x = r() * 256, y = r() * 256;
    g.moveTo(x, y);
    g.lineTo(x + (r() - 0.5) * 3, y - 3 - r() * 5);
    g.stroke();
  }
  return tex(c, { repeat });
}

export function rice({ repeat = [3, 3], seed = 12 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#e9e2cf";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 1400; i++) {
    const x = r() * 256, y = r() * 256, a = r() * Math.PI;
    g.save();
    g.translate(x, y);
    g.rotate(a);
    g.fillStyle = r() < 0.5 ? "#f7f3e8" : "#d8cfb7";
    g.beginPath();
    g.ellipse(0, 0, 5, 2.2, 0, 0, Math.PI * 2);
    g.fill();
    g.fillStyle = "rgba(120,100,70,0.25)";
    g.fillRect(-4, 1.2, 8, 1);
    g.restore();
  }
  return tex(c, { repeat });
}

export function wicker({ repeat = [4, 2] } = {}) {
  const [c, g] = canvas(128, 128);
  g.fillStyle = "#a07a45";
  g.fillRect(0, 0, 128, 128);
  for (let y = 0; y < 128; y += 16) {
    for (let x = 0; x < 128; x += 16) {
      const o = ((x + y) / 16) % 2;
      g.fillStyle = o ? "#c49a5c" : "#7d5a2f";
      g.fillRect(x + 1, y + 1, 14, 14);
      g.fillStyle = "rgba(0,0,0,0.25)";
      g.fillRect(x, y + (o ? 0 : 14), 16, 2);
    }
  }
  return tex(c, { repeat });
}

export function denim({ color = "#2c3f63", repeat = [1, 1], seed = 13 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(128, 128);
  g.fillStyle = color;
  g.fillRect(0, 0, 128, 128);
  for (let i = 0; i < 128; i += 2) {
    g.strokeStyle = `rgba(255,255,255,${0.04 + r() * 0.04})`;
    g.beginPath();
    g.moveTo(i, 0);
    g.lineTo(i + 128, 128);
    g.stroke();
  }
  return tex(c, { repeat });
}

// hoodie front: kangaroo pocket + drawstrings + hood seam
export function hoodieFront({ color = "#e8732a", dark = "#b9541b" } = {}) {
  const [c, g] = canvas(256, 256);
  g.fillStyle = color;
  g.fillRect(0, 0, 256, 256);
  g.fillStyle = dark;
  g.beginPath();
  g.moveTo(60, 256);
  g.lineTo(78, 160);
  g.lineTo(178, 160);
  g.lineTo(196, 256);
  g.closePath();
  g.fill();
  g.fillStyle = color;
  g.fillRect(70, 170, 116, 86);
  g.strokeStyle = dark;
  g.lineWidth = 5;
  g.strokeRect(72, 172, 112, 84);
  // hood edge (V)
  g.beginPath();
  g.moveTo(70, 0);
  g.quadraticCurveTo(128, 70, 186, 0);
  g.lineWidth = 9;
  g.stroke();
  // drawstrings
  g.strokeStyle = "#f4efe6";
  g.lineWidth = 6;
  g.beginPath();
  g.moveTo(108, 40);
  g.lineTo(104, 110);
  g.moveTo(148, 40);
  g.lineTo(152, 110);
  g.stroke();
  // bottom rib
  g.fillStyle = dark;
  g.fillRect(0, 240, 256, 16);
  return tex(c, { repeat: [1, 1] });
}

export function cardiganFront() {
  const [c, g] = canvas(256, 256);
  const k = knit({ colors: ["#55704f", "#4a6345", "#6b4a2e", "#4a6345"], band: 4 }).image;
  g.drawImage(k, 0, 0);
  // white shirt V + buttons
  g.fillStyle = "#efe9dc";
  g.beginPath();
  g.moveTo(100, 0);
  g.lineTo(128, 120);
  g.lineTo(156, 0);
  g.fill();
  g.fillStyle = "#3a2a1a";
  for (let y = 140; y < 250; y += 34) {
    g.beginPath();
    g.arc(128, y, 7, 0, Math.PI * 2);
    g.fill();
  }
  g.strokeStyle = "rgba(0,0,0,0.35)";
  g.lineWidth = 4;
  g.beginPath();
  g.moveTo(128, 120);
  g.lineTo(128, 256);
  g.stroke();
  return tex(c);
}

export function scrubsFront({ color = "#2f9e9a" } = {}) {
  const [c, g] = canvas(256, 256);
  g.fillStyle = color;
  g.fillRect(0, 0, 256, 256);
  g.fillStyle = "#1f6e6b";
  g.beginPath();
  g.moveTo(84, 0);
  g.lineTo(128, 80);
  g.lineTo(172, 0);
  g.fill();
  g.fillStyle = color;
  g.beginPath();
  g.moveTo(96, 0);
  g.lineTo(128, 62);
  g.lineTo(160, 0);
  g.fill();
  g.fillStyle = "#e9e3d6"; // skin at the V
  g.beginPath();
  g.moveTo(102, 0);
  g.lineTo(128, 52);
  g.lineTo(154, 0);
  g.fill();
  g.strokeStyle = "#1f6e6b";
  g.lineWidth = 5;
  g.strokeRect(150, 120, 52, 46); // pocket
  g.fillStyle = "#f2f2f2"; // badge
  g.fillRect(64, 120, 44, 28);
  g.fillStyle = "#c33";
  g.fillRect(64, 120, 44, 7);
  return tex(c);
}

export function suitFront({ tie = "#7a1d2b" } = {}) {
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#2b2f3a";
  g.fillRect(0, 0, 256, 256);
  g.fillStyle = "#f3f0ea";
  g.beginPath();
  g.moveTo(90, 0);
  g.lineTo(128, 150);
  g.lineTo(166, 0);
  g.fill();
  // bow tie
  g.fillStyle = tie;
  g.beginPath();
  g.moveTo(100, 18);
  g.lineTo(128, 32);
  g.lineTo(100, 46);
  g.closePath();
  g.moveTo(156, 18);
  g.lineTo(128, 32);
  g.lineTo(156, 46);
  g.closePath();
  g.fill();
  g.fillStyle = "#1b1e26";
  g.fillRect(126, 150, 4, 106);
  return tex(c);
}

// --- faces --------------------------------------------------------------
// Drawn on a transparent 512x512 canvas wrapped around the front of the head.
const INK = "#1b1410";
function eyes(g, kind, { y = 228, dx = 74, lash = false } = {}) {
  g.fillStyle = INK;
  g.strokeStyle = INK;
  g.lineCap = "round";
  const L = 256 - dx, R = 256 + dx;
  if (kind === "dot") {
    for (const x of [L, R]) {
      g.beginPath();
      g.ellipse(x, y, 17, 25, 0, 0, Math.PI * 2);
      g.fill();
      g.fillStyle = "#fff";
      g.beginPath();
      g.arc(x + 6, y - 9, 6, 0, Math.PI * 2);
      g.fill();
      g.fillStyle = INK;
    }
    if (lash) {
      g.lineWidth = 7;
      for (const [x, s] of [[L, -1], [R, 1]]) {
        g.beginPath();
        g.moveTo(x + s * 14, y - 22);
        g.lineTo(x + s * 30, y - 34);
        g.stroke();
      }
    }
  } else if (kind === "closed") {
    g.lineWidth = 12;
    for (const x of [L, R]) {
      g.beginPath();
      g.arc(x, y - 8, 26, 0.15 * Math.PI, 0.85 * Math.PI);
      g.stroke();
    }
  } else if (kind === "wide") {
    for (const x of [L, R]) {
      g.fillStyle = "#fff";
      g.beginPath();
      g.ellipse(x, y, 34, 40, 0, 0, Math.PI * 2);
      g.fill();
      g.lineWidth = 7;
      g.stroke();
      g.fillStyle = INK;
      g.beginPath();
      g.arc(x, y + 4, 11, 0, Math.PI * 2);
      g.fill();
    }
  } else if (kind === "stern") {
    for (const x of [L, R]) {
      g.beginPath();
      g.ellipse(x, y + 6, 16, 18, 0, 0, Math.PI * 2);
      g.fill();
    }
    g.lineWidth = 14;
    g.beginPath();
    g.moveTo(L - 34, y - 46);
    g.lineTo(L + 26, y - 26);
    g.moveTo(R + 34, y - 46);
    g.lineTo(R - 26, y - 26);
    g.stroke();
  } else if (kind === "wink") {
    g.beginPath();
    g.ellipse(L, y, 17, 25, 0, 0, Math.PI * 2);
    g.fill();
    g.lineWidth = 12;
    g.beginPath();
    g.arc(R, y + 6, 24, 1.15 * Math.PI, 1.85 * Math.PI);
    g.stroke();
  } else if (kind === "up") {
    for (const x of [L, R]) {
      g.fillStyle = "#fff";
      g.beginPath();
      g.ellipse(x, y, 26, 30, 0, 0, Math.PI * 2);
      g.fill();
      g.lineWidth = 6;
      g.stroke();
      g.fillStyle = INK;
      g.beginPath();
      g.arc(x + 4, y - 14, 11, 0, Math.PI * 2);
      g.fill();
    }
  } else if (kind === "lash") {
    for (const x of [L, R]) {
      g.beginPath();
      g.ellipse(x, y, 17, 25, 0, 0, Math.PI * 2);
      g.fill();
    }
    g.lineWidth = 10;
    g.beginPath();
    g.moveTo(L - 34, y - 34);
    g.lineTo(L + 20, y - 42);
    g.moveTo(R + 34, y - 34);
    g.lineTo(R - 20, y - 42);
    g.stroke();
  } else if (kind === "worried") {
    for (const x of [L, R]) {
      g.beginPath();
      g.ellipse(x, y + 4, 16, 22, 0, 0, Math.PI * 2);
      g.fill();
    }
    g.lineWidth = 11;
    g.beginPath();
    g.moveTo(L - 30, y - 30);
    g.lineTo(L + 24, y - 48);
    g.moveTo(R + 30, y - 30);
    g.lineTo(R - 24, y - 48);
    g.stroke();
  }
}

function mouth(g, kind, { y = 322 } = {}) {
  g.strokeStyle = INK;
  g.fillStyle = INK;
  g.lineCap = "round";
  g.lineWidth = 12;
  if (kind === "smile") {
    g.beginPath();
    g.arc(256, y - 52, 64, 0.22 * Math.PI, 0.78 * Math.PI);
    g.stroke();
  } else if (kind === "grin") {
    g.beginPath();
    g.moveTo(186, y - 24);
    g.lineTo(326, y - 24);
    g.quadraticCurveTo(320, y + 64, 256, y + 64);
    g.quadraticCurveTo(192, y + 64, 186, y - 24);
    g.closePath();
    g.fill();
    g.fillStyle = "#fff";
    g.fillRect(200, y - 18, 112, 18);
  } else if (kind === "flat") {
    g.beginPath();
    g.moveTo(214, y);
    g.lineTo(298, y);
    g.stroke();
  } else if (kind === "o") {
    g.fillStyle = "#c0262b";
    g.beginPath();
    g.ellipse(256, y + 4, 26, 32, 0, 0, Math.PI * 2);
    g.fill();
    g.lineWidth = 9;
    g.stroke();
  } else if (kind === "bigO") {
    g.fillStyle = "#c0262b";
    g.beginPath();
    g.ellipse(256, y + 10, 42, 50, 0, 0, Math.PI * 2);
    g.fill();
    g.lineWidth = 10;
    g.stroke();
  } else if (kind === "wavy") {
    g.lineWidth = 10;
    g.beginPath();
    g.moveTo(206, y + 6);
    for (let i = 0; i <= 8; i++) g.lineTo(206 + i * 12.5, y + 6 + (i % 2 ? -10 : 10));
    g.stroke();
  } else if (kind === "smirk") {
    g.beginPath();
    g.moveTo(214, y + 4);
    g.quadraticCurveTo(270, y + 14, 306, y - 16);
    g.stroke();
  } else if (kind === "frown") {
    g.beginPath();
    g.arc(256, y + 56, 52, 1.25 * Math.PI, 1.75 * Math.PI);
    g.stroke();
  } else if (kind === "softsmile") {
    g.beginPath();
    g.arc(256, y - 40, 44, 0.28 * Math.PI, 0.72 * Math.PI);
    g.stroke();
  }
}

const FACE_DEFS = {
  smile: ["dot", "smile"],
  grin: ["dot", "grin"],
  sleep: ["closed", "softsmile"],
  snore: ["closed", "o"],
  bigSnore: ["closed", "bigO"],
  scared: ["wide", "wavy"],
  shock: ["wide", "o"],
  stern: ["stern", "flat"],
  frown: ["stern", "frown"],
  wink: ["wink", "grin"],
  worried: ["worried", "wavy"],
  determined: ["stern", "smirk"],
  sigh: ["closed", "flat"],
  flat: ["dot", "flat"],
  momSmile: ["dot", "smile", { lash: true }],
  momTalk: ["dot", "o", { lash: true }],
  eyeroll: ["up", "smirk"],
  forced: ["wide", "grin"],
  momStern: ["lash", "flat"],
  momSternTalk: ["lash", "o"],
  grin2: ["dot", "grin"],
  nervous: ["worried", "grin"],
};

export function faceTexture(name, { sweat = false, blush = false } = {}) {
  const [c, g] = canvas(512, 512);
  const [e, m, opt] = FACE_DEFS[name] || FACE_DEFS.smile;
  if (blush) {
    g.fillStyle = "rgba(230,90,90,0.35)";
    g.beginPath();
    g.ellipse(150, 300, 34, 20, 0, 0, Math.PI * 2);
    g.ellipse(362, 300, 34, 20, 0, 0, Math.PI * 2);
    g.fill();
  }
  eyes(g, e, opt);
  mouth(g, m);
  if (sweat) {
    g.fillStyle = "#6cc3ff";
    g.beginPath();
    g.moveTo(370, 150);
    g.quadraticCurveTo(392, 196, 370, 206);
    g.quadraticCurveTo(348, 196, 370, 150);
    g.fill();
  }
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function dogFace() {
  const [c, g] = canvas(256, 256);
  g.fillStyle = INK;
  for (const x of [80, 176]) {
    g.beginPath();
    g.arc(x, 100, 18, 0, Math.PI * 2);
    g.fill();
  }
  g.fillStyle = "#fff";
  for (const x of [86, 182]) {
    g.beginPath();
    g.arc(x, 93, 6, 0, Math.PI * 2);
    g.fill();
  }
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function clockFace() {
  const [c, g] = canvas(512, 512);
  g.fillStyle = "#f2e8d0";
  g.beginPath();
  g.arc(256, 256, 250, 0, Math.PI * 2);
  g.fill();
  g.strokeStyle = "#3a2a18";
  g.lineWidth = 10;
  g.stroke();
  g.fillStyle = "#2a1d10";
  g.font = "bold 58px Georgia, serif";
  g.textAlign = "center";
  g.textBaseline = "middle";
  const numerals = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"];
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    g.save();
    g.translate(256 + Math.sin(a) * 190, 256 - Math.cos(a) * 190);
    g.font = "bold 44px Georgia, serif";
    g.fillText(numerals[i], 0, 0);
    g.restore();
  }
  for (let i = 0; i < 60; i++) {
    const a = (i / 60) * Math.PI * 2;
    g.lineWidth = i % 5 ? 3 : 7;
    g.beginPath();
    g.moveTo(256 + Math.sin(a) * 232, 256 - Math.cos(a) * 232);
    g.lineTo(256 + Math.sin(a) * (i % 5 ? 220 : 212), 256 - Math.cos(a) * (i % 5 ? 220 : 212));
    g.stroke();
  }
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function skyGradient(stops, { stars = 0, seed = 14, moon = null } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 512);
  const gr = g.createLinearGradient(0, 0, 0, 512);
  for (const [o, col] of stops) gr.addColorStop(o, col);
  g.fillStyle = gr;
  g.fillRect(0, 0, 256, 512);
  for (let i = 0; i < stars; i++) {
    g.fillStyle = `rgba(255,255,240,${0.3 + r() * 0.7})`;
    const s = r() < 0.1 ? 2 : 1;
    g.fillRect(r() * 256, r() * 300, s, s);
  }
  if (moon) {
    const [mx, my, mr] = moon;
    const glow = g.createRadialGradient(mx, my, mr * 0.8, mx, my, mr * 4);
    glow.addColorStop(0, "rgba(220,230,255,0.45)");
    glow.addColorStop(1, "rgba(220,230,255,0)");
    g.fillStyle = glow;
    g.fillRect(0, 0, 256, 512);
    g.fillStyle = "#f4f1e4";
    g.beginPath();
    g.arc(mx, my, mr, 0, Math.PI * 2);
    g.fill();
  }
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function softDot(color = "255,255,255") {
  const [c, g] = canvas(64, 64);
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, `rgba(${color},1)`);
  gr.addColorStop(0.4, `rgba(${color},0.5)`);
  gr.addColorStop(1, `rgba(${color},0)`);
  g.fillStyle = gr;
  g.fillRect(0, 0, 64, 64);
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function zLetter() {
  const [c, g] = canvas(128, 128);
  g.fillStyle = "#f6f1e6";
  g.strokeStyle = "rgba(40,30,20,0.6)";
  g.lineWidth = 6;
  g.font = "800 112px Poppins, sans-serif";
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.strokeText("Z", 64, 68);
  g.fillText("Z", 64, 68);
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function cakeFrosting() {
  const [c, g] = canvas(256, 64);
  g.fillStyle = "#fbf7f0";
  g.fillRect(0, 0, 256, 64);
  g.fillStyle = "#f2b8c6";
  for (let x = 0; x < 256; x += 32) {
    g.beginPath();
    g.arc(x + 16, 6, 12, 0, Math.PI);
    g.fill();
  }
  return tex(c, { repeat: [3, 1] });
}

export function panelDoor({ color = "#2d4f7c" } = {}) {
  const [c, g] = canvas(256, 512);
  g.fillStyle = color;
  g.fillRect(0, 0, 256, 512);
  g.strokeStyle = "rgba(0,0,0,0.35)";
  g.lineWidth = 8;
  for (const [x, y, w, h] of [[32, 40, 84, 190], [140, 40, 84, 190], [32, 270, 84, 200], [140, 270, 84, 200]]) {
    g.strokeRect(x, y, w, h);
    g.strokeStyle = "rgba(255,255,255,0.12)";
    g.strokeRect(x + 6, y + 6, w - 12, h - 12);
    g.strokeStyle = "rgba(0,0,0,0.35)";
  }
  return tex(c);
}

// --- Lying House additions ------------------------------------------------
export function numberPlate(n) {
  const [c, g] = canvas(256, 128);
  const gr = g.createLinearGradient(0, 0, 0, 128);
  gr.addColorStop(0, "#f2d27a");
  gr.addColorStop(0.5, "#c99a3a");
  gr.addColorStop(1, "#8a6420");
  g.fillStyle = gr;
  g.fillRect(0, 0, 256, 128);
  g.strokeStyle = "#6e4e18";
  g.lineWidth = 8;
  g.strokeRect(6, 6, 244, 116);
  g.fillStyle = "#2a1c08";
  g.font = "800 92px Poppins, sans-serif";
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.fillText(String(n), 128, 70);
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function cloudsSky({ seed = 51 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(512, 512);
  const gr = g.createLinearGradient(0, 0, 0, 512);
  gr.addColorStop(0, "#3d8be0");
  gr.addColorStop(0.6, "#86c1f5");
  gr.addColorStop(1, "#d6ecff");
  g.fillStyle = gr;
  g.fillRect(0, 0, 512, 512);
  for (let k = 0; k < 9; k++) {
    const cx = r() * 512, cy = 60 + r() * 260, w = 50 + r() * 90;
    for (let b = 0; b < 7; b++) {
      g.fillStyle = `rgba(255,255,255,${0.55 + r() * 0.35})`;
      g.beginPath();
      g.ellipse(cx + (r() - 0.5) * w * 1.6, cy + (r() - 0.5) * w * 0.3, w * (0.35 + r() * 0.3), w * (0.22 + r() * 0.15), 0, 0, Math.PI * 2);
      g.fill();
    }
  }
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function paper() {
  const [c, g] = canvas(128, 128);
  g.fillStyle = "#f7f5ee";
  g.fillRect(0, 0, 128, 128);
  g.strokeStyle = "#9cc0e8";
  g.lineWidth = 2;
  for (let y = 18; y < 128; y += 12) {
    g.beginPath();
    g.moveTo(0, y);
    g.lineTo(128, y);
    g.stroke();
  }
  g.strokeStyle = "#e08a8a";
  g.beginPath();
  g.moveTo(18, 0);
  g.lineTo(18, 128);
  g.stroke();
  return tex(c);
}

export function meatloaf({ seed = 61 } = {}) {
  const r = rng(seed);
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#7a4528";
  g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 2500; i++) {
    g.fillStyle = r() < 0.5 ? "rgba(60,30,15,0.5)" : "rgba(160,100,60,0.4)";
    g.fillRect(r() * 256, r() * 256, 2 + r() * 4, 2 + r() * 3);
  }
  g.fillStyle = "#b5341f";
  g.fillRect(0, 0, 256, 54);
  for (let x = 0; x < 256; x += 16) {
    g.beginPath();
    g.arc(x + 8, 54, 10, 0, Math.PI);
    g.fill();
  }
  return tex(c);
}

// party number balloon ("3", "9"...): gold mylar glyph on transparency
export function numberBalloon(ch, color = "#f2c14e") {
  const [c, g] = canvas(256, 320);
  g.font = "800 300px Poppins, sans-serif";
  g.textAlign = "center";
  g.textBaseline = "middle";
  const gr = g.createLinearGradient(0, 0, 256, 320);
  gr.addColorStop(0, "#fff6cf");
  gr.addColorStop(0.35, color);
  gr.addColorStop(1, "#9a6a14");
  g.lineWidth = 26;
  g.lineJoin = "round";
  g.strokeStyle = color;
  g.strokeText(ch, 128, 175);
  g.fillStyle = gr;
  g.fillText(ch, 128, 175);
  const t = tex(c);
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

export function phoneScreen() {
  const [c, g] = canvas(64, 128);
  const gr = g.createLinearGradient(0, 0, 0, 128);
  gr.addColorStop(0, "#5ab0ff");
  gr.addColorStop(1, "#b05aff");
  g.fillStyle = gr;
  g.fillRect(0, 0, 64, 128);
  g.fillStyle = "rgba(255,255,255,0.8)";
  for (let y = 20; y < 120; y += 18) g.fillRect(8, y, 30 + (y % 3) * 8, 8);
  return tex(c);
}
