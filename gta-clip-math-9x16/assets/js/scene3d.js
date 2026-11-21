// gta-clip-math-9x16: the 3D layer. A clean neon studio (glossy floor, rim light, bloom, drifting bokeh), extruded
// 3D numbers set in Barlow Condensed Black, and one hero object per beat, shot with a moving camera (a whip into every
// scene, slow push-ins, orbits, punch-ins on the hits). Only the top headlines, captions, the warning card and the
// comment box are HTML (index.html), so they stay crisp in the safe zones. Objects are placed in the pixel
// coordinates of the resting camera (helpers X, Y, L). Everything is a pure function of time t, drawn on hf-seek.
//   0-5     coin tower climbs with a 3D payout counter, bursts on the $225 slam; $1,000 is sliced in half
//   5-7     a paper receipt rises and prints          7-18   glossy bar, red glass cap with sparks, the 10% slice
//   18-21   3D clip timeline, everything past 250K goes grey and pays $0
//   21-23   pattern break: hot studio, black 3D words fly in from the right
//   23-34   phones count to 200K, stack into one $1,000 slab, -10% = $900, split screen, 4x stamp and a coin burst
//   34-37   warning sign          37-39.6  MATH drops in letter by letter, a heart pops
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { Font } from "three/addons/loaders/FontLoader.js";
import FONTDATA from "./bc900-font.js";

// register readiness first (synchronously), then wait for the fonts so every label and texture is drawn in them
let resolveReady;
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
const ready = new Promise((r) => { resolveReady = r; });
window.__hf.buildReady["scene3d"] = ready;
try { await Promise.all(["900 100px BC", "800 100px BC", "800 40px IN", "700 40px IN", "600 40px IN"].map((f) => document.fonts.load(f))); } catch (e) { /* fall back */ }

const W = 1080, H = 1920, FOV = 30, D = 20, END = 40, LOOP_AT = 39.62;
const COVER = !!window.COVER3D; // build/cover.html: still camera, the counters swapped for the 3D cover title
const U = H / (2 * D * Math.tan((FOV * Math.PI) / 360)); // pixels per world unit on the z = 0 plane (resting camera)
const X = (px) => (px - 540) / U, Y = (py) => (960 - py) / U, L = (px) => px / U;

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const o3 = (p) => 1 - Math.pow(1 - p, 3);
const i4 = (p) => p * p * p * p;
const io3 = (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
const ios = (p) => -(Math.cos(Math.PI * p) - 1) / 2;
const eo = (p) => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p));
const bOut = (p, s = 1.70158) => { const q = p - 1; return 1 + (s + 1) * q * q * q + s * q * q; };
const bIn = (p, s = 1.70158) => (s + 1) * p * p * p - s * p * p;
const lerp = (a, b, u) => a + (b - a) * u;
const hash = (i) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const bump = (t, a, d) => (t >= a && t < a + 2 * d ? Math.sin((Math.PI * (t - a)) / (2 * d)) : 0); // 0 -> 1 -> 0
const TAU = Math.PI * 2, DEG = Math.PI / 180;
const fmt = (n) => Math.round(n).toLocaleString("en-US");

// ---------------------------------------------------------------- renderer, scene, post
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.localClippingEnabled = true;
const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.6;
const camera = new THREE.PerspectiveCamera(FOV, W / H, 0.1, 200);
camera.position.set(0, 0, D);
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 }));
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloomPass = new UnrealBloomPass(new THREE.Vector2(W, H), 0.45, 0.5, 0.9);
composer.addPass(bloomPass);
composer.addPass(new OutputPass());

// ---------------------------------------------------------------- canvas textures
function cnv(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
function tex(c) { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; }
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function moneyFill(g, x0, x1) { const gr = g.createLinearGradient(x0, 0, x1, 0); gr.addColorStop(0, "#FF3D9A"); gr.addColorStop(1, "#FF8A3D"); return gr; }
function glowTex(color, a = 1) {
  const c = cnv(256, 256), g = c.getContext("2d"), gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, color.replace("A", a)); gr.addColorStop(0.45, color.replace("A", a * 0.35)); gr.addColorStop(1, color.replace("A", 0));
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return tex(c);
}
function vgrad(stops) { const c = cnv(4, 512), g = c.getContext("2d"), gr = g.createLinearGradient(0, 0, 0, 512); stops.forEach(([o, col]) => gr.addColorStop(o, col)); g.fillStyle = gr; g.fillRect(0, 0, 4, 512); return tex(c); }
const BG_NIGHT = vgrad([[0, "#0A0612"], [0.42, "#160A2E"], [0.56, "#1A0C36"], [1, "#2A0F4D"]]);
const BG_HOT = (() => { const c = cnv(512, 512), g = c.getContext("2d"), gr = g.createLinearGradient(0, 0, 512, 512); gr.addColorStop(0, "#FF3D9A"); gr.addColorStop(0.5, "#FF5C77"); gr.addColorStop(1, "#FF8A3D"); g.fillStyle = gr; g.fillRect(0, 0, 512, 512);
  g.fillStyle = "rgba(255,255,255,.09)"; for (let x = -512; x < 1024; x += 64) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x + 26, 0); g.lineTo(x + 26 + 120, 512); g.lineTo(x + 120, 512); g.fill(); } return tex(c); })();
scene.background = BG_NIGHT;
const FOG_NIGHT = new THREE.Color(0x1a0c36), FOG_HOT = new THREE.Color(0xff6a6a);
scene.fog = new THREE.Fog(0x1a0c36, 21, 46);

// ---------------------------------------------------------------- lights
const amb = new THREE.AmbientLight(0x8a70c0, 0.35); scene.add(amb);
const key = new THREE.DirectionalLight(0xffffff, 1.7); key.position.set(3, 6, 10); scene.add(key);
const rimP = new THREE.PointLight(0xff3d9a, 140, 40, 2); rimP.position.set(-6, 3.5, -1.5); scene.add(rimP);
const rimO = new THREE.PointLight(0xff8a3d, 80, 40, 2); rimO.position.set(6, -0.5, -1); scene.add(rimO);
const fillV = new THREE.PointLight(0x8b5cf6, 90, 40, 2); fillV.position.set(0, -4, 7); scene.add(fillV);
const capLight = new THREE.PointLight(0xff2b2b, 0, 6, 2); scene.add(capLight);
const sweep = new THREE.PointLight(0xffffff, 0, 5, 2); scene.add(sweep); // a glint that runs across the type on each hit
const SWEEPS = [[1.6, 770], [12.5, 900], [16.82, 1050], [19.86, 780], [21.68, 1084], [29.68, 925], [37.1, 545]];

// ---------------------------------------------------------------- environment
const FLOOR_Y = Y(1279);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(240, 240), new THREE.MeshStandardMaterial({ color: 0x0d0619, metalness: 0.35, roughness: 0.42, envMapIntensity: 0.12 }));
floor.rotation.x = -Math.PI / 2; floor.position.y = FLOOR_Y; scene.add(floor);
const GL = [
  { c: "rgba(139,92,246,A)", a: 0.55, s: 26, p: [-7, 9, -24], m: [2.6, 1.6], per: 20 },
  { c: "rgba(255,61,154,A)", a: 0.2, s: 24, p: [7, -6, -26], m: [-2.8, 2.0], per: 10 },
  { c: "rgba(255,138,61,A)", a: 0.07, s: 20, p: [2, 3, -28], m: [1.8, 2.4], per: 40 },
].map((o) => {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(o.c, o.a), blending: THREE.AdditiveBlending, depthWrite: false, fog: false, transparent: true }));
  s.scale.set(o.s, o.s, 1); s.position.set(...o.p); scene.add(s); return { s, o };
});
const NB = 70;
const bokeh = new THREE.Points(new THREE.BufferGeometry(), new THREE.PointsMaterial({ size: 0.22, map: glowTex("rgba(255,214,236,A)", 1), transparent: true, opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
const BP = new Float32Array(NB * 3), BB = [];
for (let i = 0; i < NB; i++) BB.push([(hash(i) - 0.5) * 30, (hash(i + 50) - 0.5) * 30, -6 - hash(i + 99) * 22, hash(i + 7) * TAU, 1 + Math.floor(hash(i + 3) * 3)]);
bokeh.geometry.setAttribute("position", new THREE.BufferAttribute(BP, 3)); scene.add(bokeh);

// ---------------------------------------------------------------- materials
const physical = (o) => new THREE.MeshPhysicalMaterial(Object.assign({ metalness: 0.2, roughness: 0.2, clearcoat: 1, clearcoatRoughness: 0.07 }, o));
const MONEY_STEPS = 6;
const MF = [], MS = [];
for (let k = 0; k < MONEY_STEPS; k++) {
  const c = new THREE.Color("#FF3D9A").lerp(new THREE.Color("#FF8A3D"), k / (MONEY_STEPS - 1));
  MF.push(physical({ color: c, emissive: c, emissiveIntensity: 0.3 }));
  MS.push(physical({ color: c.clone().multiplyScalar(0.42), emissive: c, emissiveIntensity: 0.08, roughness: 0.3 }));
}
const WF = physical({ color: 0xe2dbf4, emissive: 0x8b5cf6, emissiveIntensity: 0.04, roughness: 0.24 });
const WS = physical({ color: 0x5b3fb8, emissive: 0x8b5cf6, emissiveIntensity: 0.1, roughness: 0.3 });
const GF = physical({ color: 0xb9b3cc, emissive: 0x2a1446, emissiveIntensity: 0.1, roughness: 0.3 });
const GS = physical({ color: 0x4a4560, roughness: 0.4 });
const KF = physical({ color: 0x140a22, metalness: 0.4, roughness: 0.14 });
const KS = physical({ color: 0x2c1648, metalness: 0.3, roughness: 0.3 });
const roseSide = new THREE.MeshStandardMaterial({ color: 0xffa585, metalness: 1, roughness: 0.3 });
const roseFace = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0.24 });
const podMat = physical({ color: 0x1c1036, metalness: 0.55, roughness: 0.25, clearcoatRoughness: 0.15 });
const neonPink = new THREE.MeshBasicMaterial({ color: new THREE.Color(3.0, 0.6, 1.6), toneMapped: false });
const neonVio = new THREE.MeshBasicMaterial({ color: new THREE.Color(0.85, 0.5, 1.9), toneMapped: false });
const neonWhite = new THREE.MeshBasicMaterial({ color: new THREE.Color(1.35, 1.25, 1.5), toneMapped: false });
const neonOrange = new THREE.MeshBasicMaterial({ color: new THREE.Color(3.0, 1.3, 0.4), toneMapped: false });

// ---------------------------------------------------------------- extruded 3D type (Barlow Condensed Black)
const FONT = new Font(FONTDATA);
const RES = FONTDATA.resolution, CAPH = FONTDATA.capHeight / RES;
const DIGIT_HA = Math.max(...[..."0123456789"].map((d) => FONTDATA.glyphs[d].ha)) / RES; // tabular digits: counters don't jitter
const GLY = new Map();
function glyph(ch) {
  let g = GLY.get(ch);
  if (g) return g;
  const shapes = ch === " " ? [] : FONT.generateShapes(ch, 1);
  let geo = null;
  if (shapes.length) {
    geo = new THREE.ExtrudeGeometry(shapes, { depth: 0.13, bevelEnabled: true, bevelThickness: 0.028, bevelSize: 0.014, bevelSegments: 3, curveSegments: 7 });
    geo.translate(0, 0, -0.065);
  }
  const raw = (FONTDATA.glyphs[ch] ? FONTDATA.glyphs[ch].ha : 250) / RES;
  g = { geo, ha: raw, tab: /[0-9]/.test(ch) ? DIGIT_HA : raw, dx: /[0-9]/.test(ch) ? (DIGIT_HA - raw) / 2 : 0 };
  GLY.set(ch, g);
  return g;
}
const TEXTS = [];
class T3 {
  // style: "money" (pink to orange candy), "white", "grey", "black", or { face, side }
  constructor(o, parent = scene) {
    this.o = Object.assign({ size: 100, style: "white", align: "center", track: 0.01 }, o);
    this.g = new THREE.Group(); this.inner = new THREE.Group(); this.g.add(this.inner); parent.add(this.g);
    this.pool = []; this.str = null; this.w = 0; this.n = 0;
    TEXTS.push(this);
  }
  mats(i, n) {
    const s = this.o.style;
    if (s === "money") { const k = n > 1 ? Math.round((i / (n - 1)) * (MONEY_STEPS - 1)) : 0; return [MF[k], MS[k]]; }
    if (s === "white") return [WF, WS];
    if (s === "grey") return [GF, GS];
    if (s === "black") return [KF, KS];
    return [s.face, s.side];
  }
  set(str) {
    if (str === this.str) return this;
    this.str = str;
    const chars = Array.from(str), n = chars.length;
    let x = 0;
    chars.forEach((ch, i) => {
      const gl = glyph(ch);
      let m = this.pool[i];
      if (!m) { m = new THREE.Group(); const mesh = new THREE.Mesh(); m.add(mesh); m.userData.mesh = mesh; this.inner.add(m); this.pool[i] = m; }
      const mesh = m.userData.mesh;
      m.visible = !!gl.geo;
      if (gl.geo) { mesh.geometry = gl.geo; mesh.material = this.mats(i, n); }
      const ha = this.o.tab === false ? gl.ha : gl.tab;
      m.position.x = x + (this.o.tab === false ? 0 : gl.dx);
      m.userData.cx = m.position.x + gl.ha / 2; m.userData.ha = gl.ha;
      x += ha + this.o.track;
    });
    for (let i = n; i < this.pool.length; i++) this.pool[i].visible = false;
    this.n = n; this.w = x - this.o.track;
    const s = L(this.o.size);
    this.inner.scale.setScalar(s);
    this.inner.position.set(this.o.align === "center" ? (-this.w * s) / 2 : this.o.align === "right" ? -this.w * s : 0, (-CAPH * s) / 2, 0);
    return this;
  }
  restyle(st) { if (st !== this.o.style) { this.o.style = st; const str = this.str; this.str = null; this.set(str); } return this; }
  at(px, py, z = 0) { this.g.position.set(X(px), Y(py), z); return this; }
}

// flat labels (Inter), drawn once into a texture
function label(text, px, color, o = {}) {
  const S2 = 2, weight = o.weight || 800, family = o.family || "IN", track = o.track ?? 0.22;
  const c0 = cnv(8, 8), g0 = c0.getContext("2d"); g0.font = `${weight} ${px * S2}px ${family}`; g0.letterSpacing = `${px * S2 * track}px`;
  const tw = g0.measureText(text).width, padX = (o.padX ?? (o.pill ? 0.9 : 0.15)) * px * S2, padY = (o.pill ? 0.62 : 0.3) * px * S2;
  const w = Math.ceil(tw + padX * 2), h = Math.ceil(px * S2 + padY * 2);
  const c = cnv(w, h), g = c.getContext("2d");
  if (o.pill) { rr(g, 3, 3, w - 6, h - 6, (h - 6) / 2); g.fillStyle = o.pillFill || "rgba(139,92,246,.18)"; g.fill(); g.lineWidth = 4; g.strokeStyle = o.pillStroke || "rgba(139,92,246,.85)"; g.stroke(); }
  g.font = `${weight} ${px * S2}px ${family}`; g.letterSpacing = `${px * S2 * track}px`; g.textBaseline = "middle"; g.textAlign = "left";
  if (o.shadow) { g.shadowColor = o.shadow; g.shadowBlur = px * 0.5; }
  g.fillStyle = color; g.fillText(text, padX + px * S2 * track * 0.5, h / 2 + px * S2 * 0.04);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(L(w / S2), L(h / S2)), new THREE.MeshBasicMaterial({ map: tex(c), color: 0xe4e4e4, transparent: true, toneMapped: false, depthWrite: false }));
  m.userData.w = w / S2; m.userData.text = text; TEXTS.push({ label: m });
  if (o.parent) o.parent.add(m); else scene.add(m);
  return m;
}

// ---------------------------------------------------------------- 1-2. payout counters, coin tower, the sliced $1,000
const RC = L(100), TC = L(10), NCOIN = 30, BASE1 = Y(1225), CX = X(505);
const coinGeo = new THREE.CylinderGeometry(RC, RC, TC, 56, 1);
const coinsG = new THREE.Group(); scene.add(coinsG);
{ const m = new THREE.Mesh(new THREE.CylinderGeometry(L(150), L(162), L(54), 72), podMat); m.position.set(CX, BASE1 - L(27), 0); coinsG.add(m); }
{ const m = new THREE.Mesh(new THREE.TorusGeometry(L(150), L(2.6), 8, 120), neonPink); m.rotation.x = Math.PI / 2; m.position.set(CX, BASE1, 0); coinsG.add(m); }
const coins = [], ghosts = [];
for (let i = 0; i < NCOIN; i++) {
  const m = new THREE.Mesh(coinGeo, [roseSide, roseFace, roseFace]); coinsG.add(m); coins.push(m);
  const gm = new THREE.MeshStandardMaterial({ color: 0xcdbeff, emissive: 0x8b5cf6, emissiveIntensity: 0.45, transparent: true, opacity: 0, depthWrite: false, roughness: 0.2, metalness: 0 });
  const g = new THREE.Mesh(coinGeo, gm); coinsG.add(g); ghosts.push(g);
}
const stackPos = (i) => [CX + (hash(i * 2.3) - 0.5) * L(9), BASE1 + TC * (i + 0.5), (hash(i * 4.1) - 0.5) * L(6)];
const T1 = [];
for (let i = 0; i < NCOIN; i++) { const target = (i + 1) / NCOIN; let a = 0, b = 1; for (let k = 0; k < 30; k++) { const m = (a + b) / 2; if (io3(m) < target) a = m; else b = m; } T1.push(0.05 + 1.45 * b); }
const KEEP = 7; // $225 of $1,000 is about 7 of 30 coins

const s1G = new THREE.Group(); scene.add(s1G);
const s1ViewsLbl = label("VIEWS", 26, "#CDBEFF", { parent: s1G }); s1ViewsLbl.position.set(X(505), Y(446), 0);
const s1Views = new T3({ size: 150, style: "white" }, s1G);
const s1PayLbl = label("PAYOUT", 26, "#CDBEFF", { parent: s1G }); s1PayLbl.position.set(X(505), Y(652), 0);
const s1Money = new T3({ size: 240, style: "money" }, s1G);
const DIM = { face: physical({ color: 0xa79fc4, emissive: 0x3a2470, emissiveIntensity: 0.12 }), side: WS };

// scene 2: $1,000 cut in two along the strike
const cutTilt = -5 * DEG;
const halves = [0, 1].map((k) => {
  const plane = new THREE.Plane(), face = WF.clone(), side = WS.clone();
  face.clippingPlanes = [plane]; side.clippingPlanes = [plane]; face.transparent = side.transparent = true;
  const t = new T3({ size: 262, style: { face, side } }); t.set("$1,000");
  return { t, plane, face, side, sign: k === 0 ? 1 : -1 };
});
const strike = new THREE.Mesh(new RoundedBoxGeometry(1, L(26), L(26), 3, L(12)), new THREE.MeshStandardMaterial({ color: 0xff2b2b, emissive: 0xff2b2b, emissiveIntensity: 2.2, roughness: 0.2 }));
strike.geometry.translate(0.5, 0, 0); scene.add(strike);
const LOCAL_PLANE = new THREE.Plane(), M4 = new THREE.Matrix4();

function coinsAt(t) {
  coinsG.visible = t < 5.0;
  s1G.visible = t < 3.0 && !COVER;
  if (!coinsG.visible) return;
  for (let i = 0; i < NCOIN; i++) {
    const c = coins[i], [x, y, z] = stackPos(i);
    if (t < 1.62 || i < KEEP) {
      const land = t < 3 ? seg(t, T1[i] - 0.16, T1[i]) : 1, f = 1 - o3(land);
      c.visible = t >= T1[i] - 0.16 || t >= 3;
      const squash = 1 - 0.12 * bump(t, 1.62, 0.07);
      c.position.set(x, BASE1 + (y - BASE1) * squash + L(240) * f, z);
      c.rotation.set(f * 1.6 * (hash(i) - 0.5), hash(i) * TAU + f * 3, f * 1.2 * (hash(i * 3) - 0.5));
    } else {
      const dt = t - (1.62 + (i - KEEP) * 0.004);
      const a = hash(i * 3.1) * TAU, side = i % 2 ? 1 : -1;
      const vx = side * (2.2 + 3.4 * hash(i * 5.7)), vz = clamp(Math.sin(a) * 2.2, -2.5, 0.8), vy = 0.4 + 1.6 * hash(i * 7.3);
      c.visible = dt < 1.4;
      c.position.set(x + vx * dt, y + vy * dt - 8 * dt * dt, z + vz * dt);
      c.rotation.set(dt * (5 + 6 * hash(i)), hash(i) * TAU + dt * 2, dt * (4 + 5 * hash(i * 9)));
    }
  }
  for (let i = 0; i < NCOIN; i++) {
    const g = ghosts[i];
    g.visible = i >= KEEP && t >= 3.0 && t < 5.0;
    if (!g.visible) continue;
    const [x, y, z] = stackPos(i);
    const t0 = 3.88 + (NCOIN - 1 - i) * 0.012, u = seg(t, t0, t0 + 0.32);
    g.material.opacity = 0.2 * seg(t, 3.04, 3.16) * (1 - u);
    g.position.set(x + (hash(i * 8.8) - 0.5) * L(140) * u, y - L(70) * u * u, z);
    g.rotation.set(u * (hash(i) - 0.5) * 2, 0, u * (hash(i * 3) - 0.5) * 2);
  }
  if (t < 3.0) {
    // the counters: views spin to 1,000,000, money climbs to $1,000, then slams to $225 from in front of the lens
    const v = 1e6 * io3(seg(t, 0.05, 1.5));
    s1Views.set(fmt(v)).at(505, 530);
    s1Views.restyle(t >= 1.75 ? DIM : "white");
    s1Money.set("$" + fmt(t < 1.6 ? Math.min(1000, v / 1000) : 225));
    const su = seg(t, 1.6, 1.73), sl = t >= 1.6 && t < 1.73;
    s1Money.at(505, 770, sl ? lerp(7, 0, i4(su)) : 0);
    s1Money.g.rotation.set(sl ? lerp(-0.5, 0, i4(su)) : 0.05 * bump(t, 1.73, 0.1), 0.06 * Math.sin(t * 2.2), 0);
    s1Money.g.scale.setScalar(1 + 0.08 * bump(t, 1.73, 0.08) + 0.03 * bump(t, 2.15, 0.12));
  }
}

function strikeAt(t) {
  const on = t >= 3.0 && t < 5.0;
  halves.forEach((h) => { h.t.g.visible = on; });
  strike.visible = on && t >= 3.69 && t < 4.05;
  if (!on) return;
  const din = bOut(seg(t, 3.04, 3.32), 1.6);
  const su = seg(t, 3.86, 4.6), e = o3(su);
  halves.forEach((h, k) => {
    const g = h.t.g;
    const top = k === 0;
    g.position.set(X(505) + (top ? L(36) : -L(30)) * e, Y(615) + L(140) * (1 - din) + (top ? L(18) : -L(34)) * e, (top ? 0.2 : -0.1) * e);
    g.rotation.set(0, (top ? -0.1 : 0.08) * e, (top ? -0.05 : 0.04) * e + 0.03 * Math.sin((t - 3) * 2.6));
    const a = t < 3.04 ? 0 : lerp(1, 0.55, seg(t, 3.9, 4.4));
    h.face.opacity = h.side.opacity = a * clamp((t - 3.04) / 0.06);
    h.face.color.set(0xe2dbf4).lerp(new THREE.Color(0x9d96b5), seg(t, 3.9, 4.3));
    // the cut runs through the middle of the cap height, tilted with the strike, and travels with each half
    g.updateMatrixWorld(true);
    LOCAL_PLANE.setFromNormalAndCoplanarPoint(new THREE.Vector3(-Math.sin(cutTilt), Math.cos(cutTilt), 0).multiplyScalar(h.sign), new THREE.Vector3(0, 0, 0));
    h.plane.copy(LOCAL_PLANE).applyMatrix4(M4.copy(g.matrixWorld));
  });
  if (strike.visible) {
    const u = o3(seg(t, 3.69, 3.86));
    strike.position.set(X(505) - L(470) * Math.cos(cutTilt), Y(615) + L(140) * (1 - din) - L(470) * Math.sin(cutTilt), 0.45);
    strike.rotation.set(0, 0, cutTilt);
    strike.scale.set(Math.max(0.001, L(940) * u), 1, 1);
    strike.material.emissiveIntensity = 2.2 + 3 * bump(t, 3.84, 0.06);
    strike.material.opacity = 1 - seg(t, 3.9, 4.05); strike.material.transparent = true;
  }
}

// ---------------------------------------------------------------- 3. the receipt
const RW = 600, RH = 640, RS = 2;
const rcC = cnv(RW * RS, RH * RS), rcT = tex(rcC);
let rcKey = "";
function drawReceipt(rows, total) {
  const k = rows + "|" + total; if (k === rcKey) return; rcKey = k;
  const g = rcC.getContext("2d"), w = rcC.width, h = rcC.height, z = 28;
  g.clearRect(0, 0, w, h);
  g.beginPath(); g.moveTo(0, z);
  for (let x = 0; x <= w; x += z * 2) { g.lineTo(x + z, 0); g.lineTo(x + 2 * z, z); }
  g.lineTo(w, h - z);
  for (let x = w; x >= 0; x -= z * 2) { g.lineTo(x - z, h); g.lineTo(x - 2 * z, h - z); }
  g.closePath(); g.fillStyle = "#FBF8FF"; g.fill();
  g.fillStyle = "#2A0F4D"; g.font = "800 46px IN"; g.textAlign = "center"; g.textBaseline = "alphabetic";
  g.letterSpacing = "14px"; g.fillText("PAYOUT RECEIPT", w / 2 + 7, 140); g.letterSpacing = "0px";
  const dash = (y) => { g.save(); g.strokeStyle = "rgba(42,15,77,.35)"; g.lineWidth = 5; g.setLineDash([18, 14]); g.beginPath(); g.moveTo(70, y); g.lineTo(w - 70, y); g.stroke(); g.restore(); };
  dash(190);
  const R = [["VIEWS", "1,000,000"], ["RATE", "$?"], ["CAP", "$?"], ["PLATFORM FEE", "?%"]];
  R.forEach(([k2, v], i) => {
    if (i >= rows) return;
    const y = 300 + i * 118;
    g.textAlign = "left"; g.fillStyle = "#1A1030"; g.font = "700 54px IN"; g.fillText(k2, 80, y);
    g.textAlign = "right"; g.font = "800 92px BC"; g.fillText(v, w - 80, y + 8);
    const kw = (g.font = "700 54px IN", g.measureText(k2).width), vw = (g.font = "800 92px BC", g.measureText(v).width);
    g.save(); g.fillStyle = "rgba(42,15,77,.3)"; for (let x = 80 + kw + 24; x < w - 80 - vw - 24; x += 22) { g.beginPath(); g.arc(x, y - 6, 4, 0, TAU); g.fill(); } g.restore();
  });
  dash(790);
  if (total) {
    g.textAlign = "left"; g.fillStyle = "#1A1030"; g.font = "800 60px IN"; g.letterSpacing = "8px"; g.fillText("PAYOUT", 80, 960); g.letterSpacing = "0px";
    g.textAlign = "right"; g.font = "900 210px BC"; g.fillStyle = moneyFill(g, w - 560, w - 80); g.fillText("$???", w - 80, 1010);
  }
  g.fillStyle = "rgba(42,15,77,.55)";
  for (let i = 0, x = 260; x < w - 260; i++) { const bw = 4 + Math.floor(hash(i) * 3) * 4; g.fillRect(x, 1100, bw, 70); x += bw + 6 + Math.floor(hash(i + 40) * 3) * 4; }
  rcT.needsUpdate = true;
}
const rcGeo = new THREE.PlaneGeometry(L(RW), L(RH), 1, 24);
{ const p = rcGeo.attributes.position; for (let i = 0; i < p.count; i++) { const v = p.getY(i) / (L(RH) / 2); p.setZ(i, -0.18 * v * v); } rcGeo.computeVertexNormals(); }
const receipt = new THREE.Mesh(rcGeo, new THREE.MeshBasicMaterial({ map: rcT, color: 0xcdc7da, alphaTest: 0.5, side: THREE.DoubleSide }));
const rcShadow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex("rgba(0,0,0,A)", 0.85), transparent: true, depthWrite: false }));
const rcG = new THREE.Group(); rcG.add(rcShadow); rcG.add(receipt); scene.add(rcG);
rcShadow.scale.set(L(RW) * 1.5, L(RH) * 1.5, 1); rcShadow.position.set(0.2, -0.3, -0.8);
function receiptAt(t) {
  rcG.visible = t >= 5.0 && t < 7.0;
  if (!rcG.visible) return;
  const u = seg(t, 5.12, 5.54), e = bOut(u, 1.3);
  rcG.position.set(X(505), Y(935) - L(1000) * (1 - e), 0);
  rcG.rotation.set(lerp(1.15, -0.1, e) + 0.02 * Math.sin((t - 5) * 3), 0.06 * Math.sin((t - 5) * 2.2), lerp(-0.12, -0.04, e));
  const s = 1 + 0.04 * bump(t, 6.55, 0.12); rcG.scale.set(s, s, s);
  drawReceipt([5.46, 5.66, 5.86, 6.06].filter((x) => t >= x).length, t >= 6.28);
}

// ---------------------------------------------------------------- 4-6. bar chart with a 3D readout
const BW = L(220), BX = X(230), BASE4 = Y(1170), PXD = 1.88; // $250 = 470 px of bar
const gradTex = (stops) => { const c = cnv(4, 256), g = c.getContext("2d"), gr = g.createLinearGradient(0, 256, 0, 0); stops.forEach(([o, col]) => gr.addColorStop(o, col)); g.fillStyle = gr; g.fillRect(0, 0, 4, 256); return tex(c); };
const barTex = gradTex([[0, "#6D3FE0"], [0.55, "#FF3D9A"], [1, "#FF8A3D"]]);
const barMat = physical({ map: barTex, emissiveMap: barTex, emissive: 0xffffff, emissiveIntensity: 0.32, roughness: 0.16, metalness: 0.1, clearcoatRoughness: 0.08 });
const chartG = new THREE.Group(); scene.add(chartG);
const pod4 = new THREE.Mesh(new RoundedBoxGeometry(L(330), L(44), L(330), 4, L(12)), podMat); pod4.position.set(BX, BASE4 - L(22), 0); chartG.add(pod4);
const edge4 = new THREE.Mesh(new THREE.BoxGeometry(L(300), L(3), L(3)), neonPink); edge4.position.set(BX, BASE4 - L(2), L(165)); chartG.add(edge4);
const bar = new THREE.Mesh(new RoundedBoxGeometry(BW, 1, BW, 4, L(14)), barMat); chartG.add(bar);
let barH = -1;
function setBar(hpx) {
  const h = Math.max(1, Math.round(hpx));
  if (h !== barH) { barH = h; bar.geometry.dispose(); bar.geometry = new RoundedBoxGeometry(BW, L(h), BW, 4, Math.min(L(14), L(h) / 2.1)); }
  bar.position.set(BX, BASE4 + L(h) / 2, 0);
  bar.visible = hpx > 0.5;
}
const capMat = new THREE.MeshStandardMaterial({ color: 0xff2b2b, emissive: 0xff2b2b, emissiveIntensity: 1.0, transparent: true, opacity: 0.62, roughness: 0.08, metalness: 0 });
const cap = new THREE.Mesh(new RoundedBoxGeometry(L(330), L(16), L(330), 3, L(6)), capMat); chartG.add(cap);
const capLbl = label("CAP $250", 46, "#FF2B2B", { family: "BC", weight: 800, track: 0.02, shadow: "rgba(255,43,43,.6)", parent: chartG });
const sliceTex = barTex.clone(); sliceTex.repeat.set(1, 0.1); sliceTex.offset.set(0, 0.9); sliceTex.needsUpdate = true;
const sliceMat = physical({ map: sliceTex, emissiveMap: sliceTex, emissive: 0xffffff, emissiveIntensity: 0.4, roughness: 0.16, transparent: true });
const slice = new THREE.Mesh(new RoundedBoxGeometry(BW, L(47), BW, 3, L(10)), sliceMat); chartG.add(slice);
{
  const c = cnv(440, 96), g = c.getContext("2d"); g.fillStyle = "#0A0612"; g.font = "900 84px BC"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("−10%", 220, 52);
  const lbl = new THREE.Mesh(new THREE.PlaneGeometry(BW * 0.9, (BW * 0.9 * 96) / 440), new THREE.MeshBasicMaterial({ map: tex(c), transparent: true, toneMapped: false }));
  lbl.position.z = BW / 2 + 0.004; slice.add(lbl); slice.userData.lbl = lbl;
}
const slashGeo = new THREE.PlaneGeometry(L(330), L(7)); slashGeo.translate(L(165), 0, 0);
const slash = new THREE.Mesh(slashGeo, new THREE.MeshBasicMaterial({ color: new THREE.Color(3, 3, 3), toneMapped: false, transparent: true })); chartG.add(slash);
const RX = 650;
const pill = label("DYLAN PAGE CAMPAIGN", 22, "#CDBEFF", { pill: true, track: 0.18, parent: chartG }); pill.position.set(X(RX), Y(662), 0);
const roViewsLbl = label("VIEWS", 26, "#CDBEFF", { parent: chartG }); roViewsLbl.position.set(X(RX), Y(742), 0);
const roViews = new T3({ size: 128, style: "white" }, chartG);
const roPayLbl = label("PAYOUT", 26, "#CDBEFF", { parent: chartG }); roPayLbl.position.set(X(RX), Y(938), 0);
const roPay = new T3({ size: 200, style: "money" }, chartG);
const zeros = [0, 1, 2].map(() => { const m = label("+$0", 34, "#8E88A3", { track: 0.02, parent: chartG }); return m; });
const sparkGeo = new THREE.BoxGeometry(L(7), L(7), L(18));
const sparks = Array.from({ length: 26 }, (_, i) => { const m = new THREE.Mesh(sparkGeo, i % 3 ? neonOrange : neonPink); chartG.add(m); return m; });

function chartAt(t) {
  chartG.visible = t >= 7.0 && t < 18.0;
  capLight.intensity = 0;
  if (!chartG.visible) return;
  const ps = 0.6 + 0.4 * bOut(seg(t, 7.2, 7.45)); pod4.scale.set(ps, 1, ps); edge4.scale.set(ps, 1, 1);
  let v;
  if (t < 7.45) v = 0;
  else if (t < 10.9) v = 200000 * ios(seg(t, 7.45, 10.9));
  else if (t < 11.05) v = 200000;
  else if (t < 12.5) v = 200000 + 50000 * seg(t, 11.05, 12.5);
  else if (t < 14.85) v = 250000 + 750000 * Math.pow(seg(t, 12.5, 14.85), 2);
  else v = 1e6;
  const capped = Math.min(250, v / 1000);
  const pay = t < 16.0 ? capped : 250 - 25 * o3(seg(t, 16.0, 16.5));
  setBar((t >= 15.45 ? 225 : capped) * PXD);
  // readout
  const ri = bOut(seg(t, 7.28, 7.58), 1.6);
  [pill, roViewsLbl, roPayLbl].forEach((m, i) => { m.material.opacity = seg(t, 7.15 + i * 0.06, 7.3 + i * 0.06); });
  pill.scale.setScalar(0.5 + 0.5 * bOut(seg(t, 7.15, 7.43), 2.4));
  roViews.set(fmt(v)).at(RX, 822 + 80 * (1 - ri));
  roPay.set("$" + fmt(pay)).at(RX, 1052 + 80 * (1 - ri));
  roViews.g.visible = roPay.g.visible = t >= 7.28;
  const flip = seg(t, 16.72, 17.06);
  roPay.g.rotation.set(flip > 0 && flip < 1 ? TAU * o3(flip) : 0, 0.05 * Math.sin(t * 1.3), 0);
  roPay.g.scale.setScalar(1 + 0.12 * bump(t, 13.23, 0.13) + 0.08 * bump(t, 16.82, 0.14));
  // the cap drops in, then flares when the bar hits it, throwing sparks
  const cu = seg(t, 11.12, 11.34);
  cap.visible = capLbl.visible = t >= 11.12;
  const cy = L(380) * (1 - i4(cu)) + L(10) * bump(t, 11.34, 0.06);
  cap.position.set(BX, Y(700) + L(8) + cy, 0);
  capLbl.position.set(X(104) + L(capLbl.userData.w) / 2, Y(618) + cy, 0.2);
  capLbl.scale.setScalar(1 + 0.12 * bump(t, 12.5, 0.12));
  const flare = bump(t, 12.5, 0.12) + 0.5 * bump(t, 11.34, 0.08);
  capMat.emissiveIntensity = 1.0 + 1.6 * flare + (t >= 12.5 && t < 15.45 ? 0.3 + 0.15 * Math.sin(t * 9) : 0);
  capLight.position.set(BX, Y(700) + 0.3, 1.6);
  capLight.intensity = 3 * flare;
  sparks.forEach((s, i) => {
    const dt = t - 12.5; s.visible = dt >= 0 && dt < 0.8;
    if (!s.visible) return;
    const a = (i / sparks.length) * Math.PI + (hash(i) - 0.5) * 0.4, sp = 3 + 4 * hash(i * 7);
    s.position.set(BX + Math.cos(a) * sp * dt * (hash(i * 3) > 0.5 ? 1 : -1), Y(700) + Math.abs(Math.sin(a)) * sp * dt * 0.6 - 6 * dt * dt, (hash(i * 5) - 0.3) * dt * 3);
    s.rotation.set(dt * 9, dt * 7, a);
    s.scale.setScalar(Math.max(0.01, 1 - dt / 0.8));
  });
  zeros.forEach((z, i) => {
    const lt = t - 12.75 - i * 0.36, p = lt >= 0 && t < 15.0 ? (lt % 1.08) / 0.9 : 2;
    z.visible = p <= 1;
    if (z.visible) { z.material.opacity = p < 0.15 ? p / 0.15 : 1 - (p - 0.15) / 0.85; z.position.set(X(300) + L(z.userData.w) / 2, Y(660) + L(110) * p, 0.3); }
  });
  // 10% fee: a slash, then the top slice falls away
  slice.visible = t >= 15.45 && t < 16.25;
  if (slice.visible) {
    const fu = Math.pow(seg(t, 15.5, 16.25), 2);
    slice.position.set(BX + L(330) * fu, Y(723.5) - L(380) * fu, L(40) * fu);
    slice.rotation.set(1.2 * fu, 0.4 * fu, -0.66 * fu);
    sliceMat.opacity = 1 - seg(t, 16.13, 16.25);
    slice.userData.lbl.material.opacity = sliceMat.opacity;
  }
  slash.visible = t >= 15.36 && t < 15.68;
  slash.position.set(BX - L(165), Y(747), BW / 2 + 0.06);
  slash.scale.set(Math.max(0.001, o3(seg(t, 15.36, 15.46))), 1, 1);
  slash.material.opacity = 1 - seg(t, 15.5, 15.68);
}

// ---------------------------------------------------------------- 7. the clip as a 3D timeline
const tlG = new THREE.Group(); scene.add(tlG);
const TX0 = 130, TX1 = 880, TY = 945, TL = TX1 - TX0, T250 = TX0 + TL * 0.25;
const track = new THREE.Mesh(new RoundedBoxGeometry(L(TL), L(70), L(70), 4, L(18)), physical({ color: 0x24124a, metalness: 0.5, roughness: 0.25 }));
track.geometry.translate(L(TL) / 2, 0, 0); track.position.set(X(TX0), Y(TY), 0); tlG.add(track);
{ // film-frame texture on the track front
  const c = cnv(1660, 140), g = c.getContext("2d"); g.fillStyle = "#24124a"; g.fillRect(0, 0, 1660, 140);
  for (let x = 20; x < 1660; x += 120) { rr(g, x, 22, 100, 96, 14); g.fillStyle = "rgba(139,92,246,.35)"; g.fill(); }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(L(TL - 20), L(56)), new THREE.MeshBasicMaterial({ map: tex(c), transparent: true }));
  m.position.set(L(TL) / 2, 0, L(35) + 0.004); track.add(m);
}
const earn = new THREE.Mesh(new RoundedBoxGeometry(1, L(74), L(74), 3, L(16)), physical({ color: 0xff3d9a, emissive: 0xff3d9a, emissiveIntensity: 0.55, roughness: 0.15 }));
earn.geometry.translate(0.5, 0, 0); tlG.add(earn);
const greyM = new THREE.Mesh(new RoundedBoxGeometry(1, L(74), L(74), 3, L(16)), physical({ color: 0x5a5470, roughness: 0.45, metalness: 0.2, clearcoat: 0.3 }));
greyM.geometry.translate(0.5, 0, 0); tlG.add(greyM);
const phead = new THREE.Group(); tlG.add(phead);
{ const m = new THREE.Mesh(new THREE.CylinderGeometry(L(3.5), L(3.5), L(170), 12), neonWhite); phead.add(m); const h = new THREE.Mesh(new THREE.SphereGeometry(L(15), 20, 14), neonWhite); h.position.y = L(92); phead.add(h); }
const pin = new THREE.Group(); tlG.add(pin);
{ const m = new THREE.Mesh(new THREE.CylinderGeometry(L(5), L(5), L(186), 12), neonOrange); m.position.y = L(93); pin.add(m); }
const t225 = new T3({ size: 112, style: "money" }, tlG);
const tZero = new T3({ size: 180, style: "grey" }, tlG); tZero.set("$0");
const ticks = ["0", "250K", "500K", "750K", "1M"].map((s, i) => { const m = label(s, 26, i === 1 ? "#FF8A3D" : "#CDBEFF", { track: 0.04, parent: tlG }); m.position.set(X(TX0 + (TL * i) / 4), Y(1030), 0); return m; });
function timelineAt(t) {
  tlG.visible = t >= 18.0 && t < 21.0;
  if (!tlG.visible) return;
  const gr = o3(seg(t, 18.12, 18.44));
  track.scale.set(Math.max(0.001, gr), 1, 1);
  ticks.forEach((m, i) => { m.material.opacity = seg(t, 18.32 + i * 0.04, 18.5 + i * 0.04); });
  let px;
  if (t < 18.55) px = 0;
  else if (t < 19.4) px = (TL / 4) * io3(seg(t, 18.55, 19.4));
  else if (t < 19.5) px = TL / 4;
  else px = TL / 4 + (TL * 3) / 4 * seg(t, 19.5, 20.6);
  const ew = Math.min(px, TL / 4), gw = Math.max(0, px - TL / 4);
  earn.visible = ew > 1; earn.scale.set(L(ew), 1, 1); earn.position.set(X(TX0), Y(TY), 0.01);
  greyM.visible = gw > 1; greyM.scale.set(L(gw), 1, 1); greyM.position.set(X(T250), Y(TY), 0.01);
  phead.visible = t >= 18.45; phead.position.set(X(TX0 + px), Y(TY), L(50));
  pin.visible = t >= 19.4; pin.position.set(X(T250), Y(TY + 90), L(42)); pin.scale.set(1, Math.max(0.001, bOut(seg(t, 19.4, 19.58), 2.5)), 1);
  t225.set("$" + fmt(225 * io3(seg(t, 18.55, 19.4)))).at(TX0 + 112, 790);
  t225.g.visible = t >= 18.5;
  t225.g.scale.setScalar(0.6 + 0.4 * bOut(seg(t, 18.5, 18.7), 2));
  tZero.g.visible = t >= 19.86;
  const zu = seg(t, 19.86, 20.06);
  tZero.at(T250 + (TX1 - T250) / 2, 780, lerp(5, 0, i4(zu)));
  tZero.g.rotation.set(lerp(-0.6, 0, i4(zu)), 0, lerp(-14, -6, i4(zu)) * DEG);
}

// ---------------------------------------------------------------- 8. pattern break: hot studio, black words fly in from the right
const brG = new THREE.Group(); scene.add(brG);
const words = [["NOW", 21.12, 586], ["WATCH", 21.4, 832], ["THIS.", 21.68, 1078]].map(([s, t0w, y]) => ({ t: new T3({ size: 268, style: "black", tab: false }, brG).set(s), t0: t0w, y }));
function breakAt(t) {
  const on = t >= 21.0 && t < 23.0;
  brG.visible = on;
  scene.background = on ? BG_HOT : BG_NIGHT;
  scene.fog.color.copy(on ? FOG_HOT : FOG_NIGHT);
  floor.visible = !on;
  GL.forEach(({ s }) => { s.visible = !on; }); bokeh.visible = !on;
  amb.intensity = on ? 1.2 : 0.35; amb.color.set(on ? 0xffd0e0 : 0x8a70c0);
  if (!on) return;
  words.forEach((w, i) => {
    const u = seg(t, w.t0, w.t0 + (i === 2 ? 0.22 : 0.3)), e = i === 2 ? o3(u) : bOut(u, 1.4);
    w.t.g.visible = t >= w.t0;
    const drift = -L(14) * seg(t, 22.0, 23.0);
    w.t.at(505 + 820 * (1 - e), w.y, (i === 2 ? 3 : 1.5) * (1 - e));
    w.t.g.position.x += drift;
    w.t.g.rotation.set(0, -0.9 * (1 - e) + 0.08 * Math.sin((t - 21) * 2 + i), (1 - e) * 0.2);
    w.t.g.scale.setScalar(i === 2 ? 1 + 0.25 * (1 - e) + 0.06 * bump(t, 21.9, 0.1) : 1);
  });
}

// ---------------------------------------------------------------- 9-11. phones
const PW = L(168), PH = L(340);
const phoneBodyGeo = new RoundedBoxGeometry(PW, PH, L(16), 4, L(24));
const phoneGlowGeo = new RoundedBoxGeometry(PW * 1.035, PH * 1.02, L(6), 4, L(26));
const bodyMat = physical({ color: 0x221340, metalness: 0.7, roughness: 0.24, clearcoatRoughness: 0.12 });
const SCW = 360, SCH = Math.round((360 * (PH - L(16))) / (PW - L(16)));
function drawPhone(g, w, h, o) {
  g.clearRect(0, 0, w, h);
  rr(g, 0, 0, w, h, w * 0.13); g.save(); g.clip();
  const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#1F0E3E"); gr.addColorStop(1, "#3A1670"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
  const gl = g.createRadialGradient(w * 0.5, h * 0.42, 0, w * 0.5, h * 0.42, w * 0.9); gl.addColorStop(0, "rgba(139,92,246,.35)"); gl.addColorStop(1, "rgba(139,92,246,0)"); g.fillStyle = gl; g.fillRect(0, 0, w, h);
  g.fillStyle = "rgba(255,255,255,.18)"; rr(g, w / 2 - w * 0.13, h * 0.03, w * 0.26, h * 0.022, h * 0.011); g.fill();
  g.fillStyle = "rgba(205,190,255,.85)"; g.beginPath(); g.moveTo(w * 0.1, h * 0.085); g.lineTo(w * 0.1 + h * 0.045, h * 0.108); g.lineTo(w * 0.1, h * 0.131); g.closePath(); g.fill();
  g.textAlign = "center"; g.textBaseline = "alphabetic";
  if (o.top) { g.fillStyle = "#CDBEFF"; g.font = `800 ${Math.round(w * 0.075)}px IN`; g.letterSpacing = `${Math.round(w * 0.02)}px`; g.fillText(o.top, w / 2 + w * 0.01, h * 0.2); g.letterSpacing = "0px"; }
  g.fillStyle = "#FFFFFF"; g.shadowColor = "rgba(139,92,246,.9)"; g.shadowBlur = w * 0.06;
  g.font = `900 ${Math.round(w * o.vs)}px BC`; g.fillText(o.views, w / 2, h * o.vy); g.shadowBlur = 0;
  g.fillStyle = "#CDBEFF"; g.font = `700 ${Math.round(w * 0.066)}px IN`; g.letterSpacing = `${Math.round(w * 0.025)}px`; g.fillText("VIEWS", w / 2 + w * 0.012, h * (o.vy + 0.07)); g.letterSpacing = "0px";
  if (o.ma > 0) {
    g.save(); g.globalAlpha = o.ma; g.translate(w / 2, h * o.my); g.scale(o.ms, o.ms);
    g.font = `900 ${Math.round(w * o.mz)}px BC`; g.fillStyle = moneyFill(g, -w * 0.4, w * 0.4); g.shadowColor = "rgba(255,61,154,.8)"; g.shadowBlur = w * 0.05; g.fillText(o.money, 0, 0); g.restore();
  }
  g.restore();
}
function makePhone(sw = SCW, sh = SCH, bodyGeo = phoneBodyGeo, glowGeo = phoneGlowGeo, w = PW, h = PH, depth = L(16)) {
  const grp = new THREE.Group(), inner = new THREE.Group(); grp.add(inner);
  { const m = new THREE.Mesh(glowGeo, neonVio); m.position.z = -L(6); inner.add(m); }
  inner.add(new THREE.Mesh(bodyGeo, bodyMat));
  const c = cnv(sw, sh), tx = tex(c);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(w - L(16), h - L(16)), new THREE.MeshBasicMaterial({ map: tx, transparent: true, toneMapped: false }));
  scr.position.z = depth / 2 + 0.004; inner.add(scr);
  scene.add(grp);
  return { grp, inner, c, tx, key: "" };
}
function paint(p, o) { const k = JSON.stringify(o); if (k === p.key) return; p.key = k; drawPhone(p.c.getContext("2d"), p.c.width, p.c.height, o); p.tx.needsUpdate = true; }
const phones = [0, 1, 2, 3, 4].map(() => makePhone());
const P9 = [23.15, 23.7, 24.25, 24.8, 25.35];
const X9 = [145, 325, 505, 685, 865], Y9 = 800;
const X11 = [165, 335, 505, 675, 845], Y11 = 1120, S11 = 0.774;
const STACK = [-10, 4, 9, -5, 6];
const BPW = L(250), BPH = L(440);
const bigPhone = makePhone(420, Math.round((420 * (BPH - L(16))) / (BPW - L(16))), new RoundedBoxGeometry(BPW, BPH, L(18), 4, L(30)), new RoundedBoxGeometry(BPW * 1.03, BPH * 1.02, L(6), 4, L(32)), BPW, BPH, L(18));

// scene 10: the total slab with 3D numbers, the split screen, the 4x stamp and a coin burst
const slabG = new THREE.Group(); scene.add(slabG);
{ const m = new THREE.Mesh(new RoundedBoxGeometry(L(612), L(482), L(20), 4, L(46)), neonPink); m.position.z = -L(14); slabG.add(m); }
slabG.add(new THREE.Mesh(new RoundedBoxGeometry(L(600), L(470), L(40), 4, L(44)), physical({ color: 0x24124a, metalness: 0.55, roughness: 0.25, clearcoatRoughness: 0.1 })));
const slabViews = new T3({ size: 112, style: "white" }, slabG);
const slabLbl = label("VIEWS", 24, "#CDBEFF", { parent: slabG }); slabLbl.position.set(0, L(845 - 800), L(26));
const slabPay = new T3({ size: 180, style: "money" }, slabG);
const feeChip = label("−10%", 50, "#0A0612", { family: "BC", weight: 900, track: 0.02, pill: true, pillFill: "#FFFFFF", pillStroke: "#FFFFFF", parent: slabG });
const splitG = new THREE.Group(); scene.add(splitG);
const hL = new THREE.Group(), hR = new THREE.Group(); splitG.add(hL); splitG.add(hR);
{ const a = label("1 CLIP", 26, "#CDBEFF", { parent: hL }); a.position.set(X(290), Y(662), 0); const b = label("1M views", 28, "#CDBEFF", { weight: 600, track: 0.02, parent: hL }); b.position.set(X(290), Y(888), 0); }
{ const a = label("5 CLIPS", 26, "#CDBEFF", { parent: hR }); a.position.set(X(722), Y(662), 0); const b = label("1M views", 28, "#CDBEFF", { weight: 600, track: 0.02, parent: hR }); b.position.set(X(722), Y(888), 0); }
const sp225 = new T3({ size: 156, style: "grey" }, hL); sp225.set("$225").at(290, 772);
const sp900 = new T3({ size: 166, style: "money" }, hR); sp900.set("$900").at(722, 775);
const divider = new THREE.Mesh(new THREE.BoxGeometry(L(4), L(320), L(4)), neonVio); divider.position.set(X(505), Y(790), 0); splitG.add(divider);
const stampG = new THREE.Group(); splitG.add(stampG);
const st4 = new T3({ size: 240, style: "money", tab: false }, stampG); st4.set("4x");
const stMore = new T3({ size: 66, style: "white", tab: false }, stampG); stMore.set("MORE");
{ // the stamp frame: a glowing white rounded outline
  const w = L(440), h = L(236), r = L(34), sh = new THREE.Shape(), hole = new THREE.Path(), d = L(9);
  const rect = (p, x0, y0, x1, y1, rad) => { p.moveTo(x0 + rad, y0); p.lineTo(x1 - rad, y0); p.quadraticCurveTo(x1, y0, x1, y0 + rad); p.lineTo(x1, y1 - rad); p.quadraticCurveTo(x1, y1, x1 - rad, y1); p.lineTo(x0 + rad, y1); p.quadraticCurveTo(x0, y1, x0, y1 - rad); p.lineTo(x0, y0 + rad); p.quadraticCurveTo(x0, y0, x0 + rad, y0); };
  rect(sh, -w / 2, -h / 2, w / 2, h / 2, r); rect(hole, -w / 2 + d, -h / 2 + d, w / 2 - d, h / 2 - d, r - d); sh.holes.push(hole);
  const m = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: L(10), bevelEnabled: false, curveSegments: 8 }), neonWhite); m.position.z = -L(5); stampG.add(m);
  const back = new THREE.Mesh(new THREE.PlaneGeometry(w - d, h - d), new THREE.MeshBasicMaterial({ color: 0x0a0612, transparent: true, opacity: 0.55 })); back.position.z = -L(8); stampG.add(back);
}
const burst = Array.from({ length: 16 }, (_, i) => { const m = new THREE.Mesh(coinGeo, [roseSide, roseFace, roseFace]); scene.add(m); return m; });

function phonesAt(t) {
  const on9 = t >= 23.0 && t < 28.74, on11 = t >= 32.0 && t < 34.0;
  phones.forEach((p, i) => {
    p.grp.visible = on9 || on11;
    if (!p.grp.visible) return;
    if (on9) {
      const pp = P9[i], u = seg(t, pp, pp + 0.34);
      p.grp.visible = t >= pp;
      let x = X(X9[i]), y = Y(Y9) + L(320) * (1 - bOut(u, 2)) + L(6) * Math.sin(TAU * (t / 2.4) + i * 1.3);
      let s = (0.35 + 0.65 * bOut(u, 2)) * (1 + 0.07 * bump(t, 26.3 + i * 0.09, 0.12));
      let ry = (0 - X(X9[i])) * 0.12 + (1 - u) * 1.2 * (i % 2 ? 1 : -1), rz = (i % 2 ? 0.1 : -0.1) * (1 - u), z = 0;
      if (t >= 28.0) {
        const a = 28.02 + i * 0.03, fu = bIn(seg(t, a, a + 0.42), 1.2);
        x = lerp(x, X(505), fu); y = lerp(y, Y(845), fu); s = lerp(s, 0.9, fu); ry = lerp(ry, 0, fu); rz = lerp(rz, STACK[i] * DEG, fu); z = -0.05 * i * fu;
        s *= 1 - 0.7 * seg(t, 28.5, 28.74);
      }
      p.grp.position.set(x, y, z);
      p.grp.scale.setScalar(s);
      p.inner.rotation.set(0, ry, rz);
      const mu = seg(t, pp + 0.6, pp + 0.76);
      paint(p, { views: Math.round(200 * o3(seg(t, pp + 0.08, pp + 0.58))) + "K", vs: 0.36, vy: 0.45, money: "$200", ma: mu > 0 ? 1 : 0, ms: +(1.8 - 0.8 * i4(mu)).toFixed(2), my: 0.78, mz: 0.32 });
    } else {
      const a = 32.06 + i * 0.05, u = seg(t, a, a + 0.24);
      p.grp.visible = t >= a;
      const mv = bOut(seg(t, 32.9 + i * 0.04, 33.24 + i * 0.04), 2), bo = bump(t, 33.45 + i * 0.06, 0.12);
      p.grp.position.set(X(X11[i]), Y(Y11) + L(250) * mv + L(30) * bo, 0);
      p.grp.scale.setScalar(S11 * (0.3 + 0.7 * bOut(u, 2.4)) * (1 + 0.04 * mv));
      p.inner.rotation.set(0, (0 - X(X11[i])) * 0.06 + 0.3 * bo, 0);
      paint(p, { views: "200K", vs: 0.36, vy: 0.45, money: "$200", ma: 1, ms: 1, my: 0.78, mz: 0.32 });
    }
  });
  // scene 10a: total slab: 1,000,000 views, $1,000, minus 10% = $900
  slabG.visible = t >= 28.5 && t < 30.32;
  if (slabG.visible) {
    const s = (0.6 + 0.4 * bOut(seg(t, 28.5, 28.74), 2)) * (1 + 0.03 * bump(t, 29.68, 0.1));
    slabG.scale.setScalar(s);
    slabG.position.set(X(505) + L(700) * Math.pow(seg(t, 30.12, 30.32), 3), Y(845), -0.3);
    slabG.rotation.set(-0.04, 0.05 * Math.sin((t - 28.5) * 1.6) - 0.6 * Math.pow(seg(t, 30.12, 30.32), 2), 0);
    const c = o3(seg(t, 28.5, 28.95));
    slabViews.set(fmt(1e6 * c)); slabViews.g.position.set(0, L(845 - 722), L(28));
    slabPay.set("$" + fmt(t < 29.2 ? 1000 * c : 1000 - 100 * io3(seg(t, 29.2, 29.68)))); slabPay.g.position.set(0, L(845 - 930), L(28));
    const sl = t >= 29.68 && t < 29.82, su = seg(t, 29.68, 29.81);
    slabPay.g.position.z = sl ? lerp(L(28) + 3, L(28), i4(su)) : L(28);
    feeChip.visible = t >= 29.08;
    const fu = seg(t, 29.08, 29.28);
    feeChip.position.set(L(250), L(205), L(40) + 3 * (1 - i4(fu)));
    feeChip.rotation.set(0, 0, lerp(-30, 8, i4(fu)) * DEG);
    feeChip.scale.setScalar(lerp(2.2, 1, i4(fu)));
  }
  // scene 10b: split screen and the 4x stamp, then coins burst from behind it
  splitG.visible = t >= 30.2 && t < 32.0;
  if (splitG.visible) {
    const l = bOut(seg(t, 30.2, 30.5), 1.5), r = bOut(seg(t, 30.26, 30.56), 1.5);
    hL.position.set(-L(500) * (1 - l), 0, 0); hR.position.set(L(500) * (1 - r), 0, 0);
    hL.rotation.y = 0.5 * (1 - l); hR.rotation.y = -0.5 * (1 - r);
    divider.scale.set(1, Math.max(0.001, o3(seg(t, 30.3, 30.55))), 1);
    sp900.g.scale.setScalar(1 + 0.05 * Math.sin((t - 30.2) * 4) * seg(t, 30.6, 31));
    const su = seg(t, 30.92, 31.1);
    stampG.visible = t >= 30.92;
    stampG.position.set(X(505), Y(1095), lerp(9, 0, i4(su)));
    stampG.rotation.set(lerp(-0.8, 0, i4(su)), 0, lerp(-24, -7, i4(su)) * DEG);
    stampG.scale.setScalar(1 + 0.06 * bump(t, 31.6, 0.13) + 0.05 * bump(t, 31.1, 0.06));
    st4.g.position.set(-L(70), 0, 0); stMore.g.position.set(L(130), L(-20), 0);
  }
  burst.forEach((c, i) => {
    const dt = t - 31.1; c.visible = dt >= 0 && dt < 0.9 && t < 32.0;
    if (!c.visible) return;
    const a = Math.PI * (1.05 + 0.9 * (i / (burst.length - 1))) + (hash(i) - 0.5) * 0.2, sp = 4 + 3 * hash(i * 3);
    c.position.set(X(505) + Math.cos(a) * sp * dt * 1.3, Y(1095) + Math.sin(a) * sp * dt * 0.7 + 1.2 * dt - 7 * dt * dt, -1.4 - hash(i * 7) * dt * 2);
    c.rotation.set(dt * (6 + 5 * hash(i)), dt * 3, dt * (5 + 4 * hash(i * 2)));
  });
  // scene 11: one viral clip shrinks away; the five stay
  bigPhone.grp.visible = t >= 32.0 && t < 32.87;
  if (bigPhone.grp.visible) {
    const pu = bOut(seg(t, 32.0, 32.2), 2.4), su = Math.pow(seg(t, 32.42, 32.87), 3);
    bigPhone.grp.scale.setScalar((0.8 + 0.2 * pu) * (1 - 0.88 * su));
    bigPhone.grp.position.set(X(505), Y(785) + L(160) * su, 0);
    bigPhone.inner.rotation.set(0, 0.12 * Math.sin((t - 32) * 2.5) + su * 1.5, 0);
  }
}

// ---------------------------------------------------------------- 12. warning sign
const warnG = new THREE.Group(); scene.add(warnG);
{
  const w = L(210), h = L(184), r = L(26), sh = new THREE.Shape();
  const A = [0, h / 2], B = [w / 2, -h / 2], C = [-w / 2, -h / 2];
  const along = (p, q, d) => { const dx = q[0] - p[0], dy = q[1] - p[1], l = Math.hypot(dx, dy); return [p[0] + (dx / l) * d, p[1] + (dy / l) * d]; };
  const pts = [A, B, C];
  for (let i = 0; i < 3; i++) {
    const p = pts[i], n = pts[(i + 1) % 3], pr = pts[(i + 2) % 3];
    const a = along(p, pr, r), b = along(p, n, r);
    if (i === 0) sh.moveTo(a[0], a[1]); else sh.lineTo(a[0], a[1]);
    sh.quadraticCurveTo(p[0], p[1], b[0], b[1]);
  }
  sh.closePath();
  const geo = new THREE.ExtrudeGeometry(sh, { depth: L(26), bevelEnabled: true, bevelThickness: L(8), bevelSize: L(7), bevelSegments: 4, curveSegments: 10 });
  geo.translate(0, 0, -L(13));
  warnG.add(new THREE.Mesh(geo, physical({ color: 0xff8a3d, emissive: 0xff6a1d, emissiveIntensity: 0.1, metalness: 0.2, roughness: 0.22, clearcoatRoughness: 0.1 })));
  const ink = physical({ color: 0x1a0b2e, roughness: 0.3 });
  { const m = new THREE.Mesh(new RoundedBoxGeometry(L(22), L(72), L(14), 3, L(10)), ink); m.position.set(0, L(4), L(30)); warnG.add(m); }
  { const m = new THREE.Mesh(new THREE.SphereGeometry(L(12), 24, 16), ink); m.position.set(0, -L(54), L(30)); warnG.add(m); }
}
function warnAt(t) {
  warnG.visible = t >= 34.0 && t < 37.0;
  if (!warnG.visible) return;
  const u = seg(t, 34.0, 34.45);
  warnG.scale.setScalar(1.15 * (0.4 + 0.6 * bOut(u, 2)) * (1 + 0.15 * bump(t, 34.41, 0.12) + 0.15 * bump(t, 36.5, 0.12)));
  warnG.position.set(X(505), Y(392) + L(8) * Math.sin((t - 34) * 3), 0);
  warnG.rotation.set(0.1, -Math.PI * (1 - bOut(u, 1.6)) + 0.32 * Math.sin((t - 34) * 2.2) * u, 0.05 * Math.sin((t - 34) * 1.7));
}

// ---------------------------------------------------------------- 13. MATH, letter by letter, and a heart
const math = new T3({ size: 300, style: "money", tab: false, track: 0.03 }); math.set("MATH");
const MATH_T = [37.1, 37.18, 37.26, 37.34];
const heart = new THREE.Group(); scene.add(heart);
{
  const s = new THREE.Shape(), k = L(80) / 30;
  s.moveTo(0, -24 * k);
  s.bezierCurveTo(-18 * k, -10 * k, -30 * k, 0, -30 * k, 12 * k); s.bezierCurveTo(-30 * k, 22 * k, -22 * k, 28 * k, -15 * k, 28 * k); s.bezierCurveTo(-8 * k, 28 * k, -3 * k, 24 * k, 0, 18 * k);
  s.bezierCurveTo(3 * k, 24 * k, 8 * k, 28 * k, 15 * k, 28 * k); s.bezierCurveTo(22 * k, 28 * k, 30 * k, 22 * k, 30 * k, 12 * k); s.bezierCurveTo(30 * k, 0, 18 * k, -10 * k, 0, -24 * k);
  const g = new THREE.ExtrudeGeometry(s, { depth: L(30), bevelEnabled: true, bevelThickness: L(14), bevelSize: L(12), bevelSegments: 6, curveSegments: 18 });
  g.center();
  heart.add(new THREE.Mesh(g, physical({ color: 0xff3d9a, emissive: 0xff1f7a, emissiveIntensity: 0.3, metalness: 0.1, roughness: 0.2, clearcoatRoughness: 0.08 })));
}
function endAt(t) {
  math.g.visible = t >= 37.1 && t < LOOP_AT;
  if (math.g.visible) {
    math.at(505, 545);
    math.g.rotation.set(0, 0.1 * Math.sin((t - 37) * 1.8), 0);
    math.g.scale.setScalar(1 + 0.06 * bump(t, 37.51, 0.12) + 0.06 * bump(t, 39.0, 0.12));
    math.pool.forEach((p, i) => {
      const u = seg(t, MATH_T[i], MATH_T[i] + 0.3);
      p.visible = t >= MATH_T[i];
      p.position.y = 1.6 * (1 - bOut(u, 2.2));
      p.position.z = 0;
      p.rotation.set((1 - u) * -1.1, 0, (1 - u) * (i % 2 ? 0.4 : -0.4));
      p.userData.mesh.position.set(0, 0, 0);
    });
  }
  heart.visible = t >= 38.75 && t < LOOP_AT;
  if (heart.visible) {
    const u = seg(t, 38.75, 39.05);
    heart.scale.setScalar(Math.max(0.001, bOut(u, 4)));
    heart.position.set(X(850), Y(1196) + L(20) * u + L(6) * Math.sin((t - 38.75) * 4), 0.3);
    heart.rotation.set(0.1, (t - 38.75) * 2.2 - 0.6, -0.12);
  }
}

// ---------------------------------------------------------------- camera: a whip into each scene, slow push-ins, punch-ins on the hits
// [start, end, whip yaw, whip pitch, roll]
const SHOTS = [[0, 3, 0, 0], [3, 5, 0.34, 0.06], [5, 7, -0.28, -0.12], [7, 11, 0.36, 0.05], [11, 15, 0, 0], [15, 18, -0.16, 0],
  [18, 21, 0.34, 0.08], [21, 23, -0.22, 0, 0.05], [23, 28, 0, 0.32], [28, 32, -0.32, 0], [32, 34, 0.34, 0.05], [34, 37, -0.26, -0.06], [37, LOOP_AT, 0.32, 0.06]];
const PUNCH = [[1.73, 0.07], [3.86, 0.04], [12.5, 0.05], [16.82, 0.03], [19.86, 0.04], [21.68, 0.05], [29.68, 0.06], [31.1, 0.08], [34.02, 0.05], [37.3, 0.04]];
const SHAKES = window.HF_SHAKES || [];
const TGT = new THREE.Vector3();
function cameraAt(t, te) {
  if (COVER) { camera.position.set(0, 0, D); camera.up.set(0, 1, 0); camera.lookAt(0, 0, 0); return; }
  let yaw = 0, pitch = 0, dist = D, roll = 0;
  const s = SHOTS.find(([a, b]) => te >= a && te < b) || SHOTS[0];
  const [a, b, wy, wp, wr = 0] = s, w = 1 - eo(seg(te, a, a + 0.55));
  yaw += wy * w; pitch += wp * w; roll += wr * (0.6 + 0.4 * w);
  dist *= (1 + (a === 0 ? 0 : 0.12 * w)) * (1 - 0.045 * ios(seg(te, a, b)));
  yaw += 0.03 * Math.sin((TAU * te) / 10); pitch += 0.015 * Math.sin((TAU * te) / 8);
  if (te >= 7 && te < 18) yaw += 0.05 * Math.sin(((te - 7) / 11) * Math.PI) * (te < 11 ? 1 : -0.6); // slow orbit around the chart
  for (const [tp, k] of PUNCH) dist *= 1 - k * bump(te, tp, 0.12);
  let sx = 0, sy = 0;
  for (const [t0, amp, d] of SHAKES) { const dt = t - t0; if (dt >= 0 && dt < d) { const k = Math.exp(-dt * 7) * (1 - dt / d); sx += amp * k * Math.sin(dt * 90); sy += amp * 0.7 * k * Math.cos(dt * 73); } }
  const dx = 0.24 * Math.sin((TAU * te) / 20), dy = 0.14 * Math.sin((TAU * te) / 10);
  TGT.set(-sx / U, sy / U, 0);
  camera.position.set(TGT.x + dx + dist * Math.sin(yaw) * Math.cos(pitch), TGT.y + dy + dist * Math.sin(pitch), dist * Math.cos(yaw) * Math.cos(pitch));
  camera.up.set(Math.sin(roll), Math.cos(roll), 0);
  camera.lookAt(TGT);
}

// ---------------------------------------------------------------- frame
function renderAt(time) {
  const t = clamp(time, 0, END);
  const te = t >= LOOP_AT ? 0 : t; // the last frames repeat frame 0, so the reel cuts cleanly back to the start
  cameraAt(t, te);
  GL.forEach(({ s, o }) => { const ph = (TAU * te) / o.per; s.position.set(o.p[0] + o.m[0] * Math.sin(ph), o.p[1] + o.m[1] * Math.sin(ph * 0.5 + 1), o.p[2]); });
  for (let i = 0; i < NB; i++) { const [x, y, z, ph, k] = BB[i]; BP[i * 3] = x + 0.6 * Math.sin((TAU * k * te) / END + ph); BP[i * 3 + 1] = y + 1.2 * Math.sin((TAU * k * te) / END + ph * 1.7); BP[i * 3 + 2] = z; }
  bokeh.geometry.attributes.position.needsUpdate = true;
  sweep.intensity = 0;
  for (const [ts, py] of SWEEPS) { const u = seg(te, ts, ts + 0.7); if (u > 0 && u < 1) { sweep.intensity = 15 * Math.sin(Math.PI * u); sweep.position.set(lerp(-4.5, 4.5, u), Y(py) + 0.4, 1.6); } }
  breakAt(te); coinsAt(te); strikeAt(te); receiptAt(te); chartAt(te); timelineAt(te); phonesAt(te); warnAt(te); endAt(te);
  composer.render();
}

if (COVER) new T3({ size: 290, style: "money", tab: false, track: 0.02 }).set("= $225").at(505, 690);
{ // coin face: rose gold with an engraved $
  const c = cnv(512, 512), g = c.getContext("2d"), gr = g.createRadialGradient(200, 180, 10, 256, 256, 256);
  gr.addColorStop(0, "#FFE1CC"); gr.addColorStop(0.55, "#FFB08F"); gr.addColorStop(1, "#E9785E");
  g.fillStyle = gr; g.fillRect(0, 0, 512, 512);
  g.strokeStyle = "rgba(170,70,50,.55)"; g.lineWidth = 14; g.beginPath(); g.arc(256, 256, 200, 0, TAU); g.stroke();
  g.font = "900 300px BC"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillStyle = "rgba(255,240,230,.75)"; g.fillText("$", 262, 270); g.fillStyle = "rgba(170,70,50,.8)"; g.fillText("$", 256, 264);
  roseFace.map = tex(c); roseFace.needsUpdate = true;
}
drawReceipt(0, false);
phones.forEach((p) => paint(p, { views: "0K", vs: 0.36, vy: 0.45, money: "$200", ma: 0, ms: 1, my: 0.78, mz: 0.32 }));
paint(bigPhone, { top: "1 VIRAL CLIP", views: "1M", vs: 0.42, vy: 0.5, money: "$225", ma: 1, ms: 1, my: 0.8, mz: 0.3 });
renderer.compile(scene, camera);
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
renderAt(window.__hfThreeTime || 0);
resolveReady();
const shown = (o) => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
function textBoxes() {
  const out = [], box = new THREE.Box3(), v = new THREE.Vector3();
  for (const it of TEXTS) {
    const obj = it.label || it.g, name = it.label ? it.label.userData.text : it.str;
    if (!name || !shown(obj)) continue;
    if (it.label && it.label.material.opacity < 0.05) continue;
    box.makeEmpty();
    obj.updateWorldMatrix(true, true);
    obj.traverseVisible((o) => { if (o.isMesh) box.expandByObject(o, true); });
    if (box.isEmpty()) continue;
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (let k = 0; k < 8; k++) { v.set(k & 1 ? box.max.x : box.min.x, k & 2 ? box.max.y : box.min.y, k & 4 ? box.max.z : box.min.z).project(camera); const px = (v.x + 1) * 540, py = (1 - v.y) * 960; x0 = Math.min(x0, px); x1 = Math.max(x1, px); y0 = Math.min(y0, py); y1 = Math.max(y1, py); }
    out.push({ name, x0, y0, x1, y1 });
  }
  return out;
}
window.SCENE3D = { renderAt, ready, textBoxes };
