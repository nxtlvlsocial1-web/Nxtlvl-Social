// find-skills-9x16: the 3D layer. A dark studio with warm rim light, two voxel characters acting out the story (a
// creator in a yellow hoodie and the Skill Finder, an orange cube with a magnifier and a jetpack), extruded 3D type
// and one hero object per beat, shot with a moving camera. Headlines, captions and the comment box are HTML.
// Every time comes from the voiceover (window.TIMING, written by build/voice.py): scene starts and named spoken words,
// so a new take re-times the reel. Objects sit in the resting camera's pixel coordinates (helpers X, Y, L).
//   scene 0  hook: the creator types frantically; cards pop out of his laptop into a grid one by one
//   scene 1  he stares up at a galaxy of 2,400 cards; counter to 1,528,982
//   scene 2  the Skill Finder crash-lands and points out the right four    scene 3  the find-skills card; he claps, it waves
//   scene 4  he tells it what he's working on (the prompt types)           scene 5  it jetpacks through the galaxy, fetches
//            four skills and drops them into his laptop; the checklist ticks
//   scene 6  it stands on the #1 podium with a trophy, 4.5M, confetti      scene 7  SKILLS drops in; a high five, a heart
let resolveReady;
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
const ready = new Promise((r) => { resolveReady = r; });
window.__hf.buildReady["scene3d"] = ready;

import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { Font } from "three/addons/loaders/FontLoader.js";
import FONTDATA from "./bc900-font.js";

try { await Promise.all(["900 100px BC", "800 100px BC", "800 40px IN", "700 40px IN", "600 40px IN", "500 40px IN"].map((f) => document.fonts.load(f))); } catch (e) { /* fall back */ }

const TM = window.TIMING;
const COVER = !!window.COVER3D;
const W = 1080, H = 1920, FOV = 30, D = 20, END = TM.end, SC = TM.scenes, LOOP_AT = SC[SC.length - 1];
const U = H / (2 * D * Math.tan((FOV * Math.PI) / 360));
const X = (px) => (px - 540) / U, Y = (py) => (960 - py) / U, L = (px) => px / U;
// the time a spoken word starts: W(line, "word", occurrence)
const Wd = (line, word, occ = 0) => { const ws = TM.lines[line].words.filter((w) => w.w === word); return (ws[occ] || ws[ws.length - 1] || { s: TM.lines[line].start }).s; };

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const o3 = (p) => 1 - Math.pow(1 - p, 3);
const i3 = (p) => p * p * p;
const io3 = (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
const eo = (p) => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * p));
const bOut = (p, s = 1.70158) => { const q = p - 1; return 1 + (s + 1) * q * q * q + s * q * q; };
const lerp = (a, b, u) => a + (b - a) * u;
const hash = (i) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const bump = (t, a, d) => (t >= a && t < a + 2 * d ? Math.sin((Math.PI * (t - a)) / (2 * d)) : 0);
const TAU = Math.PI * 2, DEG = Math.PI / 180;
const fmt = (n) => Math.round(n).toLocaleString("en-US");

// ---------------------------------------------------------------- renderer, scene, post
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NeutralToneMapping;
const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.55;
const camera = new THREE.PerspectiveCamera(FOV, W / H, 0.1, 300);
camera.position.set(0, 0, D);
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 }));
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(W, H), 0.38, 0.5, 0.88));
composer.addPass(new OutputPass());

// ---------------------------------------------------------------- textures
function cnv(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
function tex(c) { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; }
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function glowTex(color, a = 1) {
  const c = cnv(256, 256), g = c.getContext("2d"), gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, color.replace("A", a)); gr.addColorStop(0.45, color.replace("A", a * 0.35)); gr.addColorStop(1, color.replace("A", 0));
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return tex(c);
}
const ORANGE = "#FF7A2F", AMBER = "#FFB547", GREEN = "#3DDC84", INK = "#F6F3EE", MUTED = "#9AA0B4";
{
  const c = cnv(4, 512), g = c.getContext("2d"), gr = g.createLinearGradient(0, 0, 0, 512);
  gr.addColorStop(0, "#06070C"); gr.addColorStop(0.45, "#0D1018"); gr.addColorStop(0.56, "#121622"); gr.addColorStop(1, "#1A1A24");
  g.fillStyle = gr; g.fillRect(0, 0, 4, 512); scene.background = tex(c);
}
scene.fog = new THREE.Fog(0x121622, 24, 70);

// ---------------------------------------------------------------- lights
scene.add(new THREE.AmbientLight(0x8890b0, 0.4));
const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(3, 6, 10); scene.add(key);
const rimA = new THREE.PointLight(0xff7a2f, 130, 40, 2); rimA.position.set(-6, 3.5, -1.5); scene.add(rimA);
const rimB = new THREE.PointLight(0x4f7cff, 70, 40, 2); rimB.position.set(6, -0.5, -1); scene.add(rimB);
const fill = new THREE.PointLight(0xffb547, 50, 40, 2); fill.position.set(0, -4, 7); scene.add(fill);

// ---------------------------------------------------------------- environment
const FLOOR_Y = Y(1279);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(260, 260), new THREE.MeshStandardMaterial({ color: 0x0b0d14, metalness: 0.35, roughness: 0.42, envMapIntensity: 0.1 }));
floor.rotation.x = -Math.PI / 2; floor.position.y = FLOOR_Y; scene.add(floor);
const GLOWS = [
  { c: "rgba(255,122,47,A)", a: 0.17, s: 26, p: [-8, 9, -26], m: [2.4, 1.4], per: 27.738 },
  { c: "rgba(79,124,255,A)", a: 0.13, s: 24, p: [8, -5, -28], m: [-2.6, 1.8], per: 27.738 / 2 },
].map((o) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(o.c, o.a), blending: THREE.AdditiveBlending, depthWrite: false, fog: false, transparent: true })); s.scale.set(o.s, o.s, 1); s.position.set(...o.p); scene.add(s); return { s, o }; });

// ---------------------------------------------------------------- materials
const physical = (o) => new THREE.MeshPhysicalMaterial(Object.assign({ metalness: 0.2, roughness: 0.2, clearcoat: 1, clearcoatRoughness: 0.07 }, o));
const STEPS = 6, MF = [], MS = [];
for (let k = 0; k < STEPS; k++) {
  const c = new THREE.Color(ORANGE).lerp(new THREE.Color(AMBER), k / (STEPS - 1));
  MF.push(physical({ color: c, emissive: c, emissiveIntensity: 0.28 }));
  MS.push(physical({ color: c.clone().multiplyScalar(0.4), emissive: c, emissiveIntensity: 0.08, roughness: 0.3 }));
}
const WF = physical({ color: 0xe9e4dc, emissive: 0xff7a2f, emissiveIntensity: 0.03, roughness: 0.24 });
const WS = physical({ color: 0x4a4f63, roughness: 0.3 });
const podMat = physical({ color: 0x161a26, metalness: 0.55, roughness: 0.25, clearcoatRoughness: 0.15 });
const neonO = new THREE.MeshBasicMaterial({ color: new THREE.Color(2.2, 0.9, 0.3), toneMapped: false });
const neonG = new THREE.MeshBasicMaterial({ color: new THREE.Color(0.5, 2.0, 0.9), toneMapped: false });

// ---------------------------------------------------------------- 3D type
const FONT = new Font(FONTDATA);
const RES = FONTDATA.resolution, CAPH = FONTDATA.capHeight / RES;
const DIGIT_HA = Math.max(...[..."0123456789"].map((d) => FONTDATA.glyphs[d].ha)) / RES;
const GLY = new Map();
function glyph(ch) {
  let g = GLY.get(ch); if (g) return g;
  const shapes = ch === " " ? [] : FONT.generateShapes(ch, 1);
  let geo = null;
  if (shapes.length) { geo = new THREE.ExtrudeGeometry(shapes, { depth: 0.13, bevelEnabled: true, bevelThickness: 0.028, bevelSize: 0.014, bevelSegments: 3, curveSegments: 7 }); geo.translate(0, 0, -0.065); }
  const raw = (FONTDATA.glyphs[ch] ? FONTDATA.glyphs[ch].ha : 250) / RES, dig = /[0-9]/.test(ch);
  g = { geo, ha: raw, tab: dig ? DIGIT_HA : raw, dx: dig ? (DIGIT_HA - raw) / 2 : 0 }; GLY.set(ch, g); return g;
}
const TEXTS = [];
class T3 {
  constructor(o, parent = scene) {
    this.o = Object.assign({ size: 100, style: "white", align: "center", track: 0.01 }, o);
    this.g = new THREE.Group(); this.inner = new THREE.Group(); this.g.add(this.inner); parent.add(this.g);
    this.pool = []; this.str = null; this.w = 0; TEXTS.push(this);
  }
  mats(i, n) { const s = this.o.style; if (s === "money") { const k = n > 1 ? Math.round((i / (n - 1)) * (STEPS - 1)) : 0; return [MF[k], MS[k]]; } if (s === "white") return [WF, WS]; return [s.face, s.side]; }
  set(str) {
    if (str === this.str) return this; this.str = str;
    const chars = Array.from(str), n = chars.length; let x = 0;
    chars.forEach((ch, i) => {
      const gl = glyph(ch); let m = this.pool[i];
      if (!m) { m = new THREE.Group(); const mesh = new THREE.Mesh(); m.add(mesh); m.userData.mesh = mesh; this.inner.add(m); this.pool[i] = m; }
      m.visible = !!gl.geo; if (gl.geo) { m.userData.mesh.geometry = gl.geo; m.userData.mesh.material = this.mats(i, n); }
      m.position.set(x + (this.o.tab === false ? 0 : gl.dx), 0, 0); x += (this.o.tab === false ? gl.ha : gl.tab) + this.o.track;
    });
    for (let i = n; i < this.pool.length; i++) this.pool[i].visible = false;
    this.w = x - this.o.track; const s = L(this.o.size); this.inner.scale.setScalar(s);
    this.inner.position.set(this.o.align === "center" ? (-this.w * s) / 2 : 0, (-CAPH * s) / 2, 0);
    return this;
  }
  at(px, py, z = 0) { this.g.position.set(X(px), Y(py), z); return this; }
}
function label(text, px, color, o = {}) {
  const S2 = 2, weight = o.weight || 800, family = o.family || "IN", track = o.track ?? 0.2;
  const c0 = cnv(8, 8), g0 = c0.getContext("2d"); g0.font = `${weight} ${px * S2}px ${family}`; g0.letterSpacing = `${px * S2 * track}px`;
  const tw = g0.measureText(text).width, padX = (o.pill ? 0.9 : 0.15) * px * S2, padY = (o.pill ? 0.6 : 0.3) * px * S2;
  const w = Math.ceil(tw + padX * 2), h = Math.ceil(px * S2 + padY * 2), c = cnv(w, h), g = c.getContext("2d");
  if (o.pill) { rr(g, 3, 3, w - 6, h - 6, (h - 6) / 2); g.fillStyle = o.fill || "rgba(255,122,47,.16)"; g.fill(); g.lineWidth = 4; g.strokeStyle = o.stroke || "rgba(255,122,47,.9)"; g.stroke(); }
  g.font = `${weight} ${px * S2}px ${family}`; g.letterSpacing = `${px * S2 * track}px`; g.textBaseline = "middle"; g.fillStyle = color;
  g.fillText(text, padX + px * S2 * track * 0.5, h / 2 + px * S2 * 0.04);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(L(w / S2), L(h / S2)), new THREE.MeshBasicMaterial({ map: tex(c), color: 0xe8e8e8, transparent: true, toneMapped: false, depthWrite: false }));
  m.userData.w = w / S2; m.userData.text = text; TEXTS.push({ label: m });
  (o.parent || scene).add(m); return m;
}

// ---------------------------------------------------------------- characters (the house voxel rig: blocky figures, pixel faces)
const tmpC = new THREE.Color(), BLACK = new THREE.Color(0), WHITE = new THREE.Color(0xffffff);
const shc = (c, f) => { tmpC.set(c); tmpC.lerp(f < 0 ? BLACK : WHITE, Math.abs(f)); return "#" + tmpC.getHexString(); };
const sm = (x) => x * x * (3 - 2 * x);
// keyframes [[t, {k: v}], ...] -> smoothstepped values at t
function kf(t, keys) {
  if (t <= keys[0][0]) return { ...keys[0][1] };
  for (let i = 0; i < keys.length - 1; i++) {
    const [a, p] = keys[i], [b, q] = keys[i + 1];
    if (t < b) { const u = sm(clamp((t - a) / Math.max(1e-4, b - a))); const r = {}; for (const k in p) r[k] = typeof p[k] === "number" && typeof q[k] === "number" ? lerp(p[k], q[k], u) : (u < 0.5 ? p[k] : q[k] ?? p[k]); for (const k in q) if (!(k in r)) r[k] = q[k]; return r; }
  }
  return { ...keys[keys.length - 1][1] };
}
function pix(w, h, draw) {
  const c = cnv(w, h), g = c.getContext("2d"); g.imageSmoothingEnabled = false; draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.magFilter = THREE.NearestFilter; t.minFilter = THREE.LinearFilter; t.generateMipmaps = false; return t;
}
const px = (g, c, x, y, w = 1, h = 1) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
// 24 x 24 face: brows row 7-8, eyes rows 10-12 at x 6 and 16, mouth 15-18
function drawFace(g, sp, eyes, mouth, brows) {
  const S = sp.skin, Hc = sp.hair, D = "#1E1B18", Mo = "#5A2A22", Rd = "#C8483A", Wt = "#FFFDF8";
  px(g, S, 0, 0, 24, 24);
  if (sp.style !== "none") {
    px(g, Hc, 0, 0, 24, 4);
    if (sp.style === "short") { px(g, Hc, 0, 4, 3, 3); px(g, Hc, 21, 4, 3, 3); px(g, Hc, 4, 4, 7, 1); px(g, Hc, 14, 4, 4, 1); }
  }
  if (!sp.bot) px(g, shc(S, -0.1), 11, 13, 2, 2);
  px(g, sp.cheek || "#EC9A86", 3, 15, 3, 1); px(g, sp.cheek || "#EC9A86", 18, 15, 3, 1);
  const eye = (ex, kind) => {
    if (kind === "open") { px(g, D, ex, 10, 2, 3); px(g, Wt, ex, 10, 1, 1); }
    else if (kind === "closed") px(g, D, ex - 1, 11, 4, 1);
    else if (kind === "happy") { px(g, D, ex - 1, 11, 1, 1); px(g, D, ex, 10, 2, 1); px(g, D, ex + 2, 11, 1, 1); }
    else if (kind === "wide") { px(g, Wt, ex - 1, 10, 4, 3); px(g, D, ex, 10, 2, 2); px(g, Wt, ex, 10, 1, 1); }
    else if (kind === "up") { px(g, D, ex, 9, 2, 3); px(g, Wt, ex, 9, 1, 1); }
    else if (kind === "side") { px(g, D, ex + 1, 10, 2, 3); px(g, Wt, ex + 1, 10, 1, 1); }
    else if (kind === "star") { px(g, "#FFD24A", ex - 1, 11, 4, 1); px(g, "#FFD24A", ex, 10, 2, 3); }
  };
  eye(6, eyes); eye(16, eyes);
  const Bc = sp.brow || Hc;
  if (brows === "flat") { px(g, Bc, 5, 8, 4, 1); px(g, Bc, 15, 8, 4, 1); }
  if (brows === "up") { px(g, Bc, 5, 7, 4, 1); px(g, Bc, 15, 7, 4, 1); }
  if (brows === "worry") { px(g, Bc, 5, 8, 2, 1); px(g, Bc, 7, 7, 2, 1); px(g, Bc, 15, 7, 2, 1); px(g, Bc, 17, 8, 2, 1); }
  if (brows === "focus") { px(g, Bc, 5, 7, 2, 1); px(g, Bc, 7, 8, 2, 1); px(g, Bc, 15, 8, 2, 1); px(g, Bc, 17, 7, 2, 1); }
  if (mouth === "smile") { px(g, Mo, 10, 17, 4, 1); px(g, Mo, 9, 16, 1, 1); px(g, Mo, 14, 16, 1, 1); }
  if (mouth === "grin") { px(g, Mo, 9, 16, 6, 2); px(g, Wt, 10, 16, 4, 1); px(g, Mo, 8, 15, 1, 1); px(g, Mo, 15, 15, 1, 1); }
  if (mouth === "talk") { px(g, Mo, 10, 16, 4, 2); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "o") { px(g, Mo, 11, 16, 2, 1); px(g, Mo, 10, 17, 1, 1); px(g, Mo, 13, 17, 1, 1); px(g, Mo, 11, 18, 2, 1); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "wavy") { px(g, Mo, 9, 17, 1, 1); px(g, Mo, 10, 16, 2, 1); px(g, Mo, 12, 17, 1, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "smirk") { px(g, Mo, 10, 17, 3, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "laugh") { px(g, Mo, 9, 16, 6, 3); px(g, Wt, 10, 16, 4, 1); px(g, Rd, 10, 17, 4, 2); }
}
const FACES = new Map();
function faceTex(sp, eyes, mouth, brows) {
  const k = sp.id + "|" + eyes + "|" + mouth + "|" + brows;
  let t = FACES.get(k); if (!t) { t = pix(24, 24, (g) => drawFace(g, sp, eyes, mouth, brows)); FACES.set(k, t); } return t;
}
const headSide = (sp) => pix(24, 24, (g) => { px(g, sp.skin, 0, 0, 24, 24); px(g, sp.hair, 0, 0, 24, 7); px(g, shc(sp.skin, -0.12), 10, 10, 3, 4); });
const headBack = (sp) => pix(24, 24, (g) => { px(g, sp.skin, 0, 0, 24, 24); px(g, sp.hair, 0, 0, 24, 18); });
function torsoTex(sp, back) {
  return pix(16, 20, (g) => {
    const T = sp.top, Dk = shc(T, -0.22);
    px(g, T, 0, 0, 16, 20); px(g, Dk, 0, 0, 16, 2); px(g, Dk, 0, 18, 16, 2);
    if (back) px(g, Dk, 3, 1, 10, 5); else { px(g, "#FFFDF8", 6, 2, 1, 6); px(g, "#FFFDF8", 9, 2, 1, 6); px(g, Dk, 3, 12, 10, 5); px(g, T, 4, 13, 8, 3); }
  });
}
const CHM = new Map();
const charMat = (c, map = null) => { const k = map ? null : "c" + c; if (k && CHM.has(k)) return CHM.get(k); const m = new THREE.MeshStandardMaterial({ color: map ? 0xffffff : c, map, roughness: 0.82 }); if (k) CHM.set(k, m); return m; };
const HIP = 0.82;
function makeChar(sp) {
  const M = charMat, root = new THREE.Group(); scene.add(root);
  const hips = new THREE.Group(); hips.position.y = HIP; root.add(hips);
  const mk = (geo, m, parent, x, y, z) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); parent.add(o); return o; };
  const Bx = (w, h, d) => new THREE.BoxGeometry(w, h, d);
  const topM = M(sp.top), pantsM = M(sp.pants), skinM = M(sp.skin), shoeM = M(sp.shoe), hairM = M(sp.hair);
  const torso = new THREE.Group(); hips.add(torso);
  mk(Bx(0.56, 0.62, 0.3), [topM, topM, topM, topM, M(0xffffff, torsoTex(sp, false)), M(0xffffff, torsoTex(sp, true))], torso, 0, 0.31, 0);
  mk(Bx(0.55, 0.14, 0.29), pantsM, hips, 0, -0.04, 0);
  mk(Bx(0.42, 0.14, 0.12), M(shc(sp.top, -0.15)), torso, 0, 0.58, -0.18);
  mk(Bx(0.22, 0.08, 0.2), skinM, torso, 0, 0.64, 0);
  const neck = new THREE.Group(); neck.position.y = 0.66; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head);
  const faceM = M(0xffffff, faceTex(sp, "open", "smile", "flat")), sideM = M(0xffffff, headSide(sp));
  mk(Bx(0.52, 0.52, 0.52), [sideM, sideM, M(sp.hair), skinM, faceM, M(0xffffff, headBack(sp))], head, 0, 0.26, 0);
  mk(Bx(0.56, 0.13, 0.56), hairM, head, 0, 0.475, 0);
  mk(Bx(0.22, 0.07, 0.2), hairM, head, 0.07, 0.57, 0.06);
  const sh = [], el = [], hand = [], hip = [], knee = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * 0.37, 0.56, 0); torso.add(a); sh.push(a);
    mk(Bx(0.17, 0.32, 0.18), topM, a, 0, -0.13, 0);
    const e = new THREE.Group(); e.position.y = -0.29; a.add(e); el.push(e);
    mk(Bx(0.16, 0.27, 0.17), topM, e, 0, -0.13, 0);
    hand.push(mk(Bx(0.15, 0.13, 0.16), skinM, e, 0, -0.32, 0));
    const h = new THREE.Group(); h.position.set(s * 0.135, 0, 0); hips.add(h); hip.push(h);
    mk(Bx(0.23, 0.42, 0.25), pantsM, h, 0, -0.19, 0);
    const kn = new THREE.Group(); kn.position.y = -0.4; h.add(kn); knee.push(kn);
    mk(Bx(0.22, 0.34, 0.24), pantsM, kn, 0, -0.17, 0);
    mk(Bx(0.24, 0.09, 0.32), shoeM, kn, 0, -0.37, 0.04);
  }
  return { sp, root, hips, torso, head, sh, el, hand, hip, knee, faceM, seed: 3.7 };
}
const pose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, lean: 0, tw: 0, hy: 0, hp: 0, hr: 0, s: 1, a: [[0.05, 0.1, 0.12], [0.05, 0.1, 0.12]], l: [[0, 0], [0, 0]], ...o });
function applyPose(P, p) {
  P.root.position.set(p.x, p.y, p.z); P.root.rotation.y = p.ry; P.root.scale.setScalar(p.s);
  P.torso.rotation.set(p.lean, p.tw, 0); P.head.rotation.set(p.hp, p.hy, p.hr);
  for (let k = 0; k < 2; k++) {
    P.sh[k].rotation.set(-p.a[k][0], 0, (k ? 1 : -1) * p.a[k][1]); P.el[k].rotation.x = -p.a[k][2];
    P.hip[k].rotation.x = -p.l[k][0]; P.knee[k].rotation.x = p.l[k][1];
  }
}
let NOW = 0;
const blinkAt = (seed, t) => { const p = 2.6 + hash(seed) * 1.5, u = (t + hash(seed * 3) * 7) % p; return u < 0.12; };
function setFace(P, f) {
  let eyes = f.eyes || "open";
  if ((eyes === "open" || eyes === "side" || eyes === "up") && !f.noblink && blinkAt(P.seed, NOW)) eyes = "closed";
  let mouth = f.mouth || "smile";
  if (f.talk) { const k = Math.floor(NOW * 8.5 + P.seed) % 3; mouth = k === 0 ? mouth : k === 1 ? "talk" : "o"; }
  const tx = faceTex(P.sp, eyes, mouth, f.brows || "flat");
  if (P.faceM.map !== tx) { P.faceM.map = tx; P.faceM.needsUpdate = true; }
}

// the creator: a generic voxel creator in a yellow hoodie
const CREATOR = makeChar({ id: "creator", skin: "#E2AE86", hair: "#2A1A12", style: "short", top: "#F2B33D", pants: "#2E3A55", shoe: "#FFFDF8" });
CREATOR.seed = 2.1;
const CS = 0.92; // creator scale: about 345 px tall standing at the floor line
// the Skill Finder: an orange cube with a pixel face, an antenna, a magnifier and a jetpack
const BOT_SP = { id: "bot", bot: true, skin: "#FF8A3D", hair: "#FF8A3D", style: "none", brow: "#5A2A12", cheek: "#FFB7A0" };
const BOT = (() => {
  const root = new THREE.Group(); scene.add(root);
  const body = new THREE.Group(); root.add(body);
  const orange = charMat("#FF7A2F"), dark = charMat("#2A2F3E"), white = charMat("#F6F3EE");
  const faceM = new THREE.MeshStandardMaterial({ map: faceTex(BOT_SP, "open", "smile", "flat"), roughness: 0.7 });
  const box = new THREE.Mesh(new THREE.BoxGeometry(0.92, 0.84, 0.8), [orange, orange, charMat("#FF9A55"), orange, faceM, orange]); box.position.y = 0.32 + 0.42; body.add(box);
  const band = new THREE.Mesh(new THREE.BoxGeometry(0.94, 0.08, 0.82), dark); band.position.y = 0.36; body.add(band);
  const ant = new THREE.Group(); ant.position.set(0.18, 1.16, 0); body.add(ant);
  { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.26, 8), dark); s.position.y = 0.13; ant.add(s); const b = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 12), neonO); b.position.y = 0.3; ant.add(b); }
  const arms = [], legs = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1, a = new THREE.Group(); a.position.set(s * 0.5, 0.86, 0); body.add(a); arms.push(a);
    const up = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.36, 0.15), orange); up.position.y = -0.16; a.add(up);
    const hnd = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.14, 0.17), white); hnd.position.y = -0.38; a.add(hnd);
    const l = new THREE.Group(); l.position.set(s * 0.22, 0.32, 0); root.add(l); legs.push(l);
    const lm = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.26, 0.22), dark); lm.position.y = -0.14; l.add(lm);
    const ft = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.08, 0.3), white); ft.position.set(0, -0.28, 0.04); l.add(ft);
  }
  // magnifier in the right hand
  const mag = new THREE.Group(); mag.position.set(0, -0.42, 0.06); arms[1].add(mag);
  { const r = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.035, 10, 32), dark); r.position.y = -0.24; mag.add(r); const gl = new THREE.Mesh(new THREE.CircleGeometry(0.15, 32), new THREE.MeshBasicMaterial({ color: new THREE.Color(0.6, 0.85, 1.1), transparent: true, opacity: 0.35, toneMapped: false })); gl.position.y = -0.24; mag.add(gl); const hd = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.16, 0.06), dark); hd.position.y = -0.04; mag.add(hd); }
  // jetpack and flames (scene 5)
  const jet = new THREE.Group(); jet.position.set(0, 0.7, -0.46); body.add(jet); const flames = [];
  for (const s of [-1, 1]) {
    const c = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.42, 16), charMat("#C9CCD6")); c.position.set(s * 0.18, 0, 0); jet.add(c);
    const f = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.42, 14), neonO); f.rotation.x = Math.PI; f.position.set(s * 0.18, -0.42, 0); jet.add(f); flames.push(f);
  }
  return { root, body, faceM, arms, legs, ant, mag, jet, flames, sp: BOT_SP, seed: 5.3 };
})();
const BS = 0.95;
const botPose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, s: 1, tilt: 0, sq: 1, aL: [0.1, 0.15], aR: [0.1, 0.15], lL: 0, lR: 0, jet: 0, mag: 1, ...o });
function applyBot(p, f) {
  const B = BOT;
  B.root.position.set(p.x, p.y, p.z); B.root.rotation.set(0, p.ry, p.tilt); B.root.scale.setScalar(p.s * BS);
  B.body.scale.set(1 / Math.sqrt(p.sq), p.sq, 1 / Math.sqrt(p.sq));
  B.arms[0].rotation.set(-p.aL[0], 0, -p.aL[1]); B.arms[1].rotation.set(-p.aR[0], 0, p.aR[1]);
  B.legs[0].rotation.x = -p.lL; B.legs[1].rotation.x = -p.lR;
  B.ant.rotation.z = 0.15 * Math.sin(NOW * 6);
  B.jet.visible = p.jet > 0.01; B.flames.forEach((fl, i) => fl.scale.set(1, Math.max(0.01, p.jet * (0.8 + 0.35 * Math.sin(NOW * 40 + i * 2))), 1));
  B.mag.visible = p.mag > 0.5;
  setFace(B, f);
}

// props: a desk with a laptop (the creator's), a sweat drop, a "?" above the bot, poof cubes, confetti, a trophy
const deskG = new THREE.Group(); scene.add(deskG);
{
  const top = new THREE.Mesh(new RoundedBoxGeometry(1.7, 0.08, 0.72, 2, 0.03), charMat("#3B4256")); top.position.y = 0.8; deskG.add(top);
  const front = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.66, 0.04), charMat("#2A2F3E")); front.position.set(0, 0.44, 0.32); deskG.add(front);
  const edge = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.02, 0.01), neonO); edge.position.set(0, 0.74, 0.345); deskG.add(edge);
  for (const sx of [-0.78, 0.78]) { const leg = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.78, 0.6), charMat("#2A2F3E")); leg.position.set(sx, 0.4, 0); deskG.add(leg); }
}
const laptop = new THREE.Group(); deskG.add(laptop); laptop.position.set(0, 0.84, 0.05);
const lapScreenC = cnv(512, 320), lapScreenT = tex(lapScreenC); let lapKey = "";
{
  const base = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.03, 0.42), charMat("#4A5064")); laptop.add(base);
  const lid = new THREE.Group(); lid.position.set(0, 0.015, -0.2); lid.rotation.x = -0.25; laptop.add(lid);
  const back = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.4, 0.025), charMat("#3A3F4E")); back.position.y = 0.2; lid.add(back);
  const dot = new THREE.Mesh(new THREE.CircleGeometry(0.05, 24), neonO); dot.position.set(0, 0.22, 0.014); lid.add(dot); // lid back faces the camera
  laptop.userData.lid = lid;
}
const sweat = new THREE.Mesh(new THREE.SphereGeometry(0.06, 14, 10), new THREE.MeshStandardMaterial({ color: 0x8fd3ff, roughness: 0.2, transparent: true, opacity: 0.9 })); sweat.scale.set(1, 1.4, 1); scene.add(sweat);
const qmark = new T3({ size: 90, style: "money", tab: false }); qmark.set("?");
const bang = new T3({ size: 90, style: "money", tab: false }); bang.set("!");
const poof = Array.from({ length: 16 }, (_, i) => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.11, 0.11), i % 3 ? charMat("#F6F3EE") : charMat("#FFB547")); scene.add(m); return m; });
const CONF_C = ["#FF7A2F", "#FFB547", "#3DDC84", "#4F7CFF", "#F6F3EE", "#FF5C8A"];
const confetti = Array.from({ length: 70 }, (_, i) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.09, 0.05), new THREE.MeshBasicMaterial({ color: CONF_C[i % CONF_C.length], side: THREE.DoubleSide, toneMapped: false })); scene.add(m); return m; });
const trophy = new THREE.Group(); scene.add(trophy);
{
  const gold = physical({ color: 0xffc24b, metalness: 0.9, roughness: 0.22, emissive: 0x6a4000, emissiveIntensity: 0.2 });
  const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.09, 0.26, 24, 1, true), gold); cup.position.y = 0.3; trophy.add(cup);
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.12, 12), gold); stem.position.y = 0.12; trophy.add(stem);
  const base = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.06, 0.14), gold); base.position.y = 0.04; trophy.add(base);
  for (const s of [-1, 1]) { const h = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.018, 8, 16, Math.PI), gold); h.position.set(s * 0.17, 0.32, 0); h.rotation.z = s * Math.PI / 2; trophy.add(h); }
}
const phone = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.18, 0.02), charMat("#14161C")); CREATOR.hand[1].add(phone); phone.position.set(0, -0.05, 0.1);
const heart = new THREE.Group(); scene.add(heart);
{
  const s = new THREE.Shape(), k = L(80) / 30;
  s.moveTo(0, -24 * k); s.bezierCurveTo(-18 * k, -10 * k, -30 * k, 0, -30 * k, 12 * k); s.bezierCurveTo(-30 * k, 22 * k, -22 * k, 28 * k, -15 * k, 28 * k); s.bezierCurveTo(-8 * k, 28 * k, -3 * k, 24 * k, 0, 18 * k);
  s.bezierCurveTo(3 * k, 24 * k, 8 * k, 28 * k, 15 * k, 28 * k); s.bezierCurveTo(22 * k, 28 * k, 30 * k, 22 * k, 30 * k, 12 * k); s.bezierCurveTo(30 * k, 0, 18 * k, -10 * k, 0, -24 * k);
  const g = new THREE.ExtrudeGeometry(s, { depth: L(30), bevelEnabled: true, bevelThickness: L(14), bevelSize: L(12), bevelSegments: 6, curveSegments: 18 }); g.center();
  heart.add(new THREE.Mesh(g, physical({ color: 0xff5c5c, emissive: 0xff3b3b, emissiveIntensity: 0.25, roughness: 0.2 })));
}
// world position of a point in px with feet on the floor line (z = 0 maps px exactly; characters stand slightly back)
const ZC = -0.4, FLOORZ = (z) => FLOOR_Y; // the floor is level, so standing height is the same at any depth
const stand = (pxX, z = ZC) => [X(pxX), FLOOR_Y, z];

// ---------------------------------------------------------------- skill cards (named, glossy)
const NAMES = ["captions", "video editing", "thumbnails", "hook writing", "b-roll search", "SEO", "copywriting", "web design",
  "testing", "databases", "charts", "voiceover", "slides", "emails", "music", "code review"];
const ICON = ["#FF7A2F", "#4F7CFF", "#3DDC84", "#FFB547", "#B07CFF", "#FF5C8A"];
const CW = L(300), CH = L(150), CD = L(16);
const cardGeo = new RoundedBoxGeometry(CW, CH, CD, 3, L(18));
const cardBody = physical({ color: 0x1a1f2e, metalness: 0.5, roughness: 0.28 });
function cardFace(name, i, state = "idle") {
  const c = cnv(600, 300), g = c.getContext("2d");
  rr(g, 0, 0, 600, 300, 34); g.fillStyle = state === "on" ? "#2a2116" : "#161b28"; g.fill();
  g.lineWidth = 6; g.strokeStyle = state === "on" ? ORANGE : "rgba(255,255,255,.12)"; rr(g, 3, 3, 594, 294, 32); g.stroke();
  rr(g, 40, 40, 92, 92, 22); g.fillStyle = ICON[i % ICON.length]; g.fill();
  g.fillStyle = "#0b0d14"; g.font = "900 64px BC"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(name[0].toUpperCase(), 86, 90);
  g.textAlign = "left"; g.fillStyle = INK; g.font = `800 ${name.length > 11 ? 50 : 58}px IN`; g.fillText(name, 160, 92);
  g.fillStyle = MUTED; g.font = "600 30px IN"; g.fillText("agent skill", 160, 150);
  g.fillStyle = "rgba(255,255,255,.08)"; rr(g, 40, 200, 520, 18, 9); g.fill(); rr(g, 40, 236, 360, 18, 9); g.fill();
  if (state === "on") { g.fillStyle = GREEN; g.beginPath(); g.arc(540, 70, 30, 0, TAU); g.fill(); g.strokeStyle = "#0b0d14"; g.lineWidth = 9; g.beginPath(); g.moveTo(525, 70); g.lineTo(537, 83); g.lineTo(557, 58); g.stroke(); }
  return tex(c);
}
const cards = NAMES.map((n, i) => {
  const grp = new THREE.Group(), body = new THREE.Mesh(cardGeo, cardBody);
  const faceIdle = cardFace(n, i), faceOn = cardFace(n, i, "on");
  const face = new THREE.Mesh(new THREE.PlaneGeometry(CW * 0.985, CH * 0.97), new THREE.MeshBasicMaterial({ map: faceIdle, transparent: true, toneMapped: false }));
  face.position.z = CD / 2 + 0.003; grp.add(body); grp.add(face); scene.add(grp);
  return { grp, face, faceIdle, faceOn, name: n };
});
const setCardOn = (c, on) => { const m = on ? c.faceOn : c.faceIdle; if (c.face.material.map !== m) { c.face.material.map = m; c.face.material.needsUpdate = true; } };

// scene 0: cards pop out of the creator's laptop and fill a 3x3 grid one at a time (installing one by one)
const GRID = 9, DROP = 0.27, FIRST = -0.66; // card k lands at FIRST + k * DROP: three are in at frame 0, the fourth is mid-flight
const GX = [225, 505, 785], GY = [648, 764, 880], GS = 0.72;
window.HOOK_LANDS = Array.from({ length: GRID }, (_, k) => FIRST + k * DROP);
const LAPTOP_PX = [505, 1110];
function gridAt(t) {
  if (t >= SC[1]) return;
  const ex = i3(seg(t, SC[1] - 0.24, SC[1]));
  for (let k = 0; k < GRID; k++) {
    const c = cards[k], land = FIRST + k * DROP, u = seg(t, land - 0.34, land);
    c.grp.visible = t >= land - 0.34;
    if (!c.grp.visible) continue;
    setCardOn(c, t >= land + 0.04);
    const e = bOut(u, 1.4), x = X(GX[k % 3]), y = Y(GY[Math.floor(k / 3)]);
    const fx = X(LAPTOP_PX[0]), fy = Y(LAPTOP_PX[1]);
    const dirx = (k % 3) - 1, diry = 1 - Math.floor(k / 3);
    // out of the laptop sideways first, then up (a curve that never crosses the creator's face)
    const cx = fx + (k % 2 ? 1 : -1) * L(360), cy = Y(1060), b0 = (1 - e) * (1 - e), b1 = 2 * (1 - e) * e, b2 = e * e;
    c.grp.position.set(b0 * fx + b1 * cx + b2 * x + ex * dirx * 6, b0 * fy + b1 * cy + b2 * y + ex * diry * 4, lerp(0.35, 0, e) + ex * 14);
    c.grp.rotation.set((1 - e) * -0.9 + ex * 2 * hash(k), (k % 2 ? -1 : 1) * 3.2 * (1 - e), (hash(k * 5) - 0.5) * 0.06 + ex * hash(k * 7));
    c.grp.scale.setScalar(GS * lerp(0.25, 1, e) * (1 + 0.07 * bump(t, land, 0.08)));
  }
}

// ---------------------------------------------------------------- the galaxy: 2,400 tiny cards
const NG = 2400;
const gTex = (() => { const c = cnv(128, 64), g = c.getContext("2d"); rr(g, 2, 2, 124, 60, 12); g.fillStyle = "#ffffff"; g.fill(); g.fillStyle = "rgba(0,0,0,.35)"; rr(g, 12, 12, 26, 26, 6); g.fill(); rr(g, 46, 16, 64, 8, 4); g.fill(); rr(g, 46, 32, 44, 8, 4); g.fill(); return tex(c); })();
const galaxy = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.62, 0.31), new THREE.MeshBasicMaterial({ map: gTex, transparent: true, toneMapped: false, side: THREE.DoubleSide, depthWrite: false, fog: true }), NG);
const GP = [], GC = [new THREE.Color("#2b3348"), new THREE.Color("#3a4560"), new THREE.Color("#5a4630"), new THREE.Color("#2f3b5e")];
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S3 = new THREE.Vector3(), E = new THREE.Euler(), COL = new THREE.Color(), ORANGE_C = new THREE.Color(ORANGE);
for (let i = 0; i < NG; i++) {
  const r = 4 + Math.pow(hash(i * 1.7), 0.7) * 34, th = hash(i * 2.3) * TAU, ph = Math.acos(2 * hash(i * 3.1) - 1);
  GP.push({ p: new THREE.Vector3(r * Math.sin(ph) * Math.cos(th), r * Math.cos(ph) * 0.8, -6 - r * Math.sin(ph) * Math.sin(th) * 0.9), r, rot: [(hash(i) - 0.5) * 0.8, (hash(i * 5) - 0.5) * 1.2, (hash(i * 9) - 0.5) * 0.6], c: GC[i % GC.length], ph: hash(i * 11) * TAU });
}
galaxy.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(NG * 3), 3);
galaxy.frustumCulled = false; scene.add(galaxy);
const counter = new T3({ size: 172, style: "white" });
const ringScan = new THREE.Mesh(new THREE.TorusGeometry(1, 0.03, 8, 120), new THREE.MeshBasicMaterial({ color: new THREE.Color(2.2, 0.9, 0.3), toneMapped: false, transparent: true })); scene.add(ringScan);
function galaxyAt(t) {
  const on = t >= SC[1] && t < SC[6];
  galaxy.visible = on;
  counter.g.visible = t >= SC[1] && t < SC[2];
  ringScan.visible = false;
  if (!on) return;
  const appear = o3(seg(t, SC[1], SC[1] + 0.8));
  const dim = seg(t, Wd(2, "the"), Wd(2, "right"));
  const scan0 = Wd(5, "searches"), scanR = 2 + seg(t, scan0, scan0 + 1.6) * 30;
  const scanning = t >= scan0 && t < scan0 + 1.7;
  for (let i = 0; i < NG; i++) {
    const g = GP[i], drift = 0.25 * Math.sin(t * 0.6 + g.ph), s = appear * (0.85 + 0.3 * hash(i * 13));
    V.copy(g.p).multiplyScalar(lerp(0.15, 1, appear)); V.y += drift;
    E.set(g.rot[0] + t * 0.05, g.rot[1] + t * 0.08, g.rot[2]); Q.setFromEuler(E); S3.set(s, s, s);
    M4.compose(V, Q, S3); galaxy.setMatrixAt(i, M4);
    COL.copy(g.c);
    if (t >= SC[2]) COL.multiplyScalar(lerp(1, 0.35, dim));
    if (scanning) { const dd = Math.abs(g.r - scanR); if (dd < 2.2) COL.lerp(ORANGE_C, (1 - dd / 2.2) * 0.7); }
    galaxy.setColorAt(i, COL);
  }
  galaxy.instanceMatrix.needsUpdate = true; galaxy.instanceColor.needsUpdate = true;
  if (scanning) { // two pulses ripple out from the bot
    const ph = ((t - scan0) / 0.8) % 1; ringScan.visible = true; ringScan.scale.setScalar(0.3 + ph * 1.4); ringScan.material.opacity = 0.8 * (1 - ph);
    BOT.root.getWorldPosition(V); ringScan.position.set(V.x, V.y + 0.7, V.z - 0.2);
  }
  if (counter.g.visible) {
    const c = io3(seg(t, SC[1] + 0.1, Wd(1, "million") + 0.3));
    counter.set(fmt(1528982 * c)).at(505, 720, lerp(-2, 0, o3(seg(t, SC[1], SC[1] + 0.5))));
    counter.g.rotation.set(0, 0.08 * Math.sin((t - SC[1]) * 1.6), 0);
    counter.g.scale.setScalar(1 + 0.06 * bump(t, Wd(1, "million") + 0.3, 0.12));
  }
}

// scene 2: the bot finds the right four and holds them up; scene 5: the bot fetches them and drops them into the laptop
const RIGHT = [0, 1, 2, 3];
const BOT_HAND = new THREE.Vector3();
function rightFourAt(t) {
  const s2 = t >= SC[2] && t < SC[3], s5 = t >= SC[5] && t < SC[6];
  RIGHT.forEach((k, i) => {
    const c = cards[k];
    if (!(s2 || s5)) { if (t >= SC[1]) c.grp.visible = false; return; }
    if (s2) {
      const a = Wd(2, "right") - 0.1 + i * 0.09, u = bOut(seg(t, a, a + 0.42), 1.6);
      c.grp.visible = t >= a;
      const px2 = [300, 710][i % 2], py = [640, 800][i >> 1];
      c.grp.position.set(lerp(X(780), X(px2), u), lerp(Y(950), Y(py), u), lerp(0.5, 0, u));
      c.grp.rotation.set(0, (1 - u) * 2.5 + 0.06 * Math.sin(t * 2 + i), (i % 2 ? 0.03 : -0.03));
      c.grp.scale.setScalar(lerp(0.2, 1.0, u));
      setCardOn(c, t >= a + 0.3);
    } else {
      const a = Wd(5, "picks") + i * 0.12, u = o3(seg(t, a, a + 0.42));            // galaxy -> the bot's hands
      const drop = Wd(5, "installs") + i * 0.14, du = seg(t, drop, drop + 0.28);   // the bot's hands -> the laptop
      c.grp.visible = t >= a - 0.05 && du < 1;
      const from = new THREE.Vector3((hash(k * 4) - 0.5) * 16, (hash(k * 6) - 0.2) * 9, -18);
      const held = BOT_HAND.clone().add(new THREE.Vector3(0, 0.12 * i, 0.15 + 0.02 * i));
      const lap = new THREE.Vector3(X(330), Y(1100), 0.1);
      if (du <= 0) c.grp.position.lerpVectors(from, held, u); else c.grp.position.lerpVectors(held, lap, i3(du));
      c.grp.rotation.set(0, (1 - u) * 3 + du * 2, 0);
      c.grp.scale.setScalar(du > 0 ? lerp(0.32, 0.05, du) : lerp(0.2, 0.32, u));
      setCardOn(c, true);
    }
  });
}

// ---------------------------------------------------------------- scene 3: the find-skills card
const HC = { w: L(660), h: L(400) };
const hero = new THREE.Group(); scene.add(hero);
{
  const frame = new THREE.Mesh(new RoundedBoxGeometry(HC.w * 1.02, HC.h * 1.03, L(18), 4, L(44)), neonO); frame.position.z = -L(12); hero.add(frame);
  hero.add(new THREE.Mesh(new RoundedBoxGeometry(HC.w, HC.h, L(36), 4, L(42)), physical({ color: 0x141824, metalness: 0.55, roughness: 0.24 })));
  const c = cnv(1320, 800), g = c.getContext("2d");
  rr(g, 0, 0, 1320, 800, 80); g.fillStyle = "#141824"; g.fill();
  const gl = g.createRadialGradient(300, 160, 0, 300, 160, 900); gl.addColorStop(0, "rgba(255,122,47,.28)"); gl.addColorStop(1, "rgba(255,122,47,0)"); g.fillStyle = gl; g.fill();
  rr(g, 84, 84, 150, 150, 36); g.fillStyle = ORANGE; g.fill();
  g.strokeStyle = "#141824"; g.lineWidth = 18; g.beginPath(); g.arc(150, 150, 38, 0, TAU); g.stroke(); g.beginPath(); g.moveTo(178, 178); g.lineTo(206, 206); g.stroke();
  g.fillStyle = MUTED; g.font = "700 40px IN"; g.letterSpacing = "8px"; g.fillText("AGENT SKILL", 270, 140); g.letterSpacing = "0px";
  g.fillStyle = INK; g.font = "800 46px IN"; g.fillText("#1 on skills.sh", 270, 205);
  g.fillStyle = INK; g.font = "900 220px BC"; g.fillText("find-skills", 84, 470);
  g.fillStyle = AMBER; g.font = "700 54px IN"; g.fillText("by Vercel Labs", 90, 560);
  [["FREE", 90], ["OPEN SOURCE", 300]].forEach(([s, x]) => { g.font = "800 40px IN"; const w = g.measureText(s).width + 64; rr(g, x, 620, w, 84, 42); g.fillStyle = "rgba(61,220,132,.16)"; g.fill(); g.lineWidth = 4; g.strokeStyle = GREEN; g.stroke(); g.fillStyle = GREEN; g.fillText(s, x + 32, 676); });
  const face = new THREE.Mesh(new THREE.PlaneGeometry(HC.w * 0.99, HC.h * 0.985), new THREE.MeshBasicMaterial({ map: tex(c), transparent: true, toneMapped: false }));
  face.position.z = L(18) + 0.004; hero.add(face);
}
function heroAt(t) {
  hero.visible = t >= SC[3] && t < SC[4];
  if (!hero.visible) return;
  const a = Wd(3, "find") - 0.18, u = seg(t, a, a + 0.6);
  hero.position.set(X(505), Y(700) + L(10) * Math.sin((t - a) * 2.2), lerp(-30, 0, eo(u)));
  hero.rotation.set(lerp(0.6, -0.05, eo(u)), lerp(-TAU, 0, eo(u)) + 0.1 * Math.sin((t - a) * 1.4) * u, 0);
  hero.scale.setScalar(0.88 * (1 + 0.04 * bump(t, Wd(3, "vercel"), 0.15)));
}

// ---------------------------------------------------------------- scenes 4-5: the prompt, then the install checklist
const PROMPT = "find a skill for my content reel";
const promptG = new THREE.Group(); scene.add(promptG);
const PW = L(880), PH = L(150);
promptG.add(new THREE.Mesh(new RoundedBoxGeometry(PW, PH, L(24), 4, L(48)), physical({ color: 0x161b28, metalness: 0.4, roughness: 0.3 })));
{ const m = new THREE.Mesh(new RoundedBoxGeometry(PW * 1.012, PH * 1.06, L(10), 4, L(50)), neonO); m.position.z = -L(9); promptG.add(m); }
const pC = cnv(1760, 300), pT = tex(pC); let pKey = "";
const pFace = new THREE.Mesh(new THREE.PlaneGeometry(PW * 0.985, PH * 0.94), new THREE.MeshBasicMaterial({ map: pT, transparent: true, toneMapped: false }));
pFace.position.z = L(12) + 0.004; promptG.add(pFace);
function drawPrompt(n, caret, sent) {
  const k = n + "|" + caret + "|" + sent; if (k === pKey) return; pKey = k;
  const g = pC.getContext("2d"); g.clearRect(0, 0, 1760, 300);
  rr(g, 0, 0, 1760, 300, 96); g.fillStyle = "#161b28"; g.fill();
  g.fillStyle = MUTED; g.font = "700 36px IN"; g.letterSpacing = "6px"; g.fillText("ASK YOUR AGENT", 80, 92); g.letterSpacing = "0px";
  g.font = "800 72px IN"; g.fillStyle = n ? INK : "rgba(246,243,238,.35)";
  const s = n ? PROMPT.slice(0, n) : "What are you working on?"; g.fillText(s, 80, 196);
  if (caret) { const w = g.measureText(s).width; g.fillStyle = ORANGE; g.fillRect(80 + (n ? w : 0) + 8, 136, 9, 76); }
  g.fillStyle = sent ? GREEN : ORANGE; g.beginPath(); g.arc(1630, 150, 76, 0, TAU); g.fill();
  g.fillStyle = "#0b0d14"; g.beginPath(); g.moveTo(1592, 150); g.lineTo(1672, 112); g.lineTo(1648, 196); g.lineTo(1632, 160); g.closePath(); g.fill();
  pT.needsUpdate = true;
}
const listG = new THREE.Group(); scene.add(listG);
listG.add(new THREE.Mesh(new RoundedBoxGeometry(L(880), L(400), L(24), 4, L(44)), physical({ color: 0x131722, metalness: 0.4, roughness: 0.3 })));
{ const m = new THREE.Mesh(new RoundedBoxGeometry(L(880) * 1.012, L(400) * 1.02, L(10), 4, L(46)), neonG); m.position.z = -L(9); listG.add(m); }
const lC = cnv(1760, 800), lT = tex(lC); let lKey = "";
const lFace = new THREE.Mesh(new THREE.PlaneGeometry(L(880) * 0.985, L(400) * 0.98), new THREE.MeshBasicMaterial({ map: lT, transparent: true, toneMapped: false }));
lFace.position.z = L(12) + 0.004; listG.add(lFace);
function drawList(found, done) {
  const k = found + "|" + done; if (k === lKey) return; lKey = k;
  const g = lC.getContext("2d"); g.clearRect(0, 0, 1760, 800);
  rr(g, 0, 0, 1760, 800, 88); g.fillStyle = "#131722"; g.fill();
  g.fillStyle = MUTED; g.font = "700 38px IN"; g.letterSpacing = "6px"; g.fillText(done >= 4 ? "INSTALLED · 4 OF 4" : done ? `INSTALLING · ${done} OF 4` : `FOUND · ${found} OF 4`, 80, 96); g.letterSpacing = "0px";
  RIGHT.forEach((ci, i) => {
    const y = 140 + i * 150;
    g.fillStyle = "rgba(255,255,255,.05)"; rr(g, 60, y, 1640, 124, 28); g.fill();
    if (i < found) {
      rr(g, 92, y + 20, 84, 84, 20); g.fillStyle = ICON[ci % ICON.length]; g.fill(); g.fillStyle = "#0b0d14"; g.font = "900 58px BC"; g.textAlign = "center"; g.fillText(NAMES[ci][0].toUpperCase(), 134, y + 82); g.textAlign = "left";
      g.fillStyle = INK; g.font = "800 60px IN"; g.fillText(NAMES[ci], 212, y + 82);
    }
    if (i < done) { g.fillStyle = GREEN; g.beginPath(); g.arc(1600, y + 62, 40, 0, TAU); g.fill(); g.strokeStyle = "#0b0d14"; g.lineWidth = 12; g.beginPath(); g.moveTo(1580, y + 62); g.lineTo(1596, y + 80); g.lineTo(1622, y + 46); g.stroke(); g.fillStyle = GREEN; g.font = "800 44px IN"; g.textAlign = "right"; g.fillText("installed", 1532, y + 78); g.textAlign = "left"; }
    else if (i < found) { g.fillStyle = AMBER; g.font = "800 44px IN"; g.textAlign = "right"; g.fillText("found", 1640, y + 78); g.textAlign = "left"; }
  });
  lT.needsUpdate = true;
}
function panelsAt(t) {
  const picks = Wd(5, "picks");
  promptG.visible = t >= SC[4] && t < picks + 0.35;
  listG.visible = t >= picks && t < SC[6];
  if (promptG.visible) {
    const u = bOut(seg(t, SC[4], SC[4] + 0.45), 1.5), up = o3(seg(t, SC[5], SC[5] + 0.5)), out = i3(seg(t, picks, picks + 0.35));
    promptG.position.set(X(505), lerp(Y(1400), Y(720), u) + (Y(630) - Y(720)) * up + 6 * out, 0);
    promptG.rotation.set(lerp(-0.9, 0.04, u) + out * 0.6, 0.05 * Math.sin(t * 1.3), 0);
    const t0 = Wd(4, "tell"), t1 = Wd(4, "reel") + 0.25;
    const n = Math.round(PROMPT.length * clamp((t - t0) / (t1 - t0)));
    const sent = t >= Wd(4, "reel") + 0.45;
    drawPrompt(t < t0 ? 0 : n, !sent && Math.floor(t * 3.2) % 2 === 0, sent);
  }
  if (listG.visible) {
    const lu = bOut(seg(t, picks, picks + 0.45), 1.4);
    listG.position.set(X(505), lerp(Y(-200), Y(648), lu), 0);
    listG.rotation.set(lerp(0.7, 0.03, lu), -0.04 * Math.sin(t * 1.1), 0);
    const found = RIGHT.filter((_, i) => t >= picks + i * 0.12 + 0.42).length;
    const done = RIGHT.filter((_, i) => t >= Wd(5, "installs") + i * 0.14 + 0.28).length;
    drawList(found, done);
  }
}

// ---------------------------------------------------------------- scene 6: the podium (find-skills #1 with 4.5M installs)
const podG = new THREE.Group(); scene.add(podG);
const PODS = [{ rank: 2, name: "hyperframes-cli", v: "1.7M", x: 245, top: 1066 }, { rank: 1, name: "find-skills", v: "4.5M", x: 505, top: 1000 }, { rank: 3, name: "agent-browser", v: "1.7M", x: 765, top: 1106 }];
const podMeshes = PODS.map((p) => {
  const h = 1279 - p.top, w = 250;
  const m = new THREE.Mesh(new RoundedBoxGeometry(L(w), L(h), L(230), 3, L(14)), p.rank === 1 ? physical({ color: 0xff7a2f, emissive: 0xff7a2f, emissiveIntensity: 0.25, roughness: 0.2 }) : physical({ color: 0x343b50, roughness: 0.32 }));
  const c = cnv(w * 2, h * 2), g = c.getContext("2d");
  g.textAlign = "center"; g.fillStyle = p.rank === 1 ? "#1a0e06" : INK;
  g.font = `900 ${p.rank === 1 ? 128 : 96}px BC`; g.fillText("#" + p.rank, w, p.rank === 1 ? 150 : 115);
  g.font = "800 40px IN"; g.fillStyle = p.rank === 1 ? "#1a0e06" : "#C3C7D4"; g.fillText(p.name, w, p.rank === 1 ? 228 : 182);
  g.font = "900 76px BC"; g.fillStyle = p.rank === 1 ? "#1a0e06" : AMBER; g.fillText(p.v, w, p.rank === 1 ? 322 : 262);
  const face = new THREE.Mesh(new THREE.PlaneGeometry(L(w) * 0.96, L(h) * 0.96), new THREE.MeshBasicMaterial({ map: tex(c), transparent: true, toneMapped: false }));
  face.position.z = L(115) + 0.004; m.add(face);
  podG.add(m); return { m, p, h };
});
const big = new T3({ size: 200, style: "money", tab: false });
const podLbl = label("ALL-TIME INSTALLS · SKILLS.SH · 23 NOV 2026", 22, "#C3C7D4", { parent: podG });
function podiumAt(t) {
  const on = t >= SC[6] && t < SC[7];
  podG.visible = big.g.visible = trophy.visible = on;
  confetti.forEach((c) => { c.visible = false; });
  if (!on) return;
  podMeshes.forEach((pm, i) => {
    const a = SC[6] + 0.1 + [0.12, 0, 0.24][i], u = bOut(seg(t, a, a + 0.5), 1.3);
    pm.m.position.set(X(pm.p.x), Y(1279) + L(pm.h) * u / 2 - L(pm.h) * (1 - u) / 2, -0.6);
    pm.m.scale.set(1, Math.max(0.01, u), 1);
  });
  const m0 = Wd(6, "four") - 0.1, mc = io3(seg(t, SC[6] + 0.2, m0 + 0.75));
  big.set((4.5 * mc).toFixed(1) + "M").at(505, 534, 0);
  big.g.rotation.set(0, 0.07 * Math.sin((t - SC[6]) * 1.4), 0);
  big.g.scale.setScalar((0.7 + 0.3 * bOut(seg(t, SC[6] + 0.1, SC[6] + 0.45), 2)) * (1 + 0.08 * bump(t, m0 + 0.75, 0.12)));
  podLbl.position.set(X(505), Y(422), 0); podLbl.material.opacity = seg(t, SC[6] + 0.4, SC[6] + 0.6);
  // confetti from the top when the number lands
  const c0 = m0 + 0.75;
  confetti.forEach((c, i) => {
    const dt = t - c0 - hash(i) * 0.25; c.visible = dt > 0;
    if (!c.visible) return;
    const x0 = (hash(i * 3) - 0.5) * 7, vy = 1.2 + hash(i * 5) * 1.4;
    c.position.set(x0 + 0.4 * Math.sin(dt * 3 + i), Y(420) - vy * dt - 0.5 * dt * dt, -0.2 + hash(i * 7) * 1.2);
    c.rotation.set(dt * (4 + hash(i) * 6), dt * 3, dt * (2 + hash(i * 2) * 5));
  });
}

// ---------------------------------------------------------------- scene 7: SKILLS, letter by letter
const word = new T3({ size: 250, style: "money", tab: false, track: 0.03 }); word.set("SKILLS");
function ctaAt(t) {
  const on = t >= SC[7] && t < LOOP_AT;
  word.g.visible = on;
  heart.visible = on && t >= Wd(7, "send");
  if (!on) return;
  const a0 = Wd(7, "word") - 0.05;
  word.at(505, 540);
  word.g.rotation.set(0, 0.08 * Math.sin((t - SC[7]) * 1.7), 0);
  word.g.scale.setScalar(1 + 0.06 * bump(t, Wd(7, "skills"), 0.12));
  word.pool.forEach((p, i) => {
    const a = a0 + i * 0.07, u = seg(t, a, a + 0.32);
    p.visible = t >= a; p.position.y = 1.6 * (1 - bOut(u, 2.2)); p.rotation.set((1 - u) * -1.1, 0, (1 - u) * (i % 2 ? 0.35 : -0.35));
  });
  if (heart.visible) {
    const u = seg(t, Wd(7, "send"), Wd(7, "send") + 0.3);
    heart.scale.setScalar(Math.max(0.001, bOut(u, 4)) * 0.6);
    heart.position.set(X(515), Y(965) + L(20) * u, 0.6);
    heart.rotation.set(0.1, (t - Wd(7, "send")) * 2.2 - 0.6, -0.12);
  }
}

// ---------------------------------------------------------------- the acting
const typing = (t, fast = 1) => { const s = Math.sin(t * 22 * fast), c = Math.sin(t * 22 * fast + 1.7); return [[1.05 + 0.12 * s, 0.18, 1.05 + 0.15 * s], [1.05 + 0.12 * c, 0.18, 1.05 + 0.15 * c]]; };
function creatorAt(t) {
  const P = CREATOR;
  let vis = true, p, f;
  sweat.visible = false; bang.g.visible = false;
  deskG.visible = (t < SC[1]) || (t >= SC[4] && t < SC[6]);
  if (t < SC[1]) { // hook: typing frantically behind the desk, sweating
    const [x, y, z] = stand(505, -0.75);
    deskG.position.set(X(505), FLOOR_Y, -0.35); deskG.rotation.y = 0;
    p = pose({ x, y, z, s: CS, hp: 0.32 + 0.04 * Math.sin(t * 9), hy: 0.12 * Math.sin(t * 2.4), lean: 0.12, a: typing(t, 1.3) });
    if (t > Wd(0, "one") - 0.1) { p.hy = 0.35 * Math.sin(t * 14); p.hp = 0.1; } // head shake on "one by one"
    f = { eyes: "open", mouth: "wavy", brows: "worry" };
    sweat.visible = true; sweat.position.set(x + 0.32 * CS, y + 1.95 * CS - 0.12 * ((t * 1.6) % 1), z + 0.3);
  } else if (t < SC[2]) { // dwarfed by the galaxy, looking up
    const [x, y, z] = stand(250, -0.2);
    p = pose({ x, y, z, s: CS, ry: 0.35, hp: -0.5, a: [[0.25, 0.25, 0.3], [0.25, 0.25, 0.3]] });
    f = { eyes: "up", mouth: "o", brows: "up", noblink: true };
  } else if (t < SC[3]) { // the bot arrives: surprise, then delight
    const [x, y, z] = stand(230, -0.2), land = Wd(2, "this") + 0.3;
    p = pose({ x, y, z, s: CS, ry: 0.55, hy: 0.2, a: t < land ? [[0.3, 0.3, 0.4], [0.3, 0.3, 0.4]] : [[0.6, 0.5, 1.2], [0.6, 0.5, 1.2]] });
    f = t < land + 0.25 ? { eyes: "wide", mouth: "o", brows: "up", noblink: true } : { eyes: "happy", mouth: "grin", brows: "up" };
    bang.g.visible = t >= land - 0.05 && t < land + 0.7; bang.at(230, 860, 0.3); bang.g.scale.setScalar(bOut(seg(t, land - 0.05, land + 0.2), 3));
  } else if (t < SC[4]) { // claps for find-skills
    const [x, y, z] = stand(200, -0.2), cl = Math.abs(Math.sin((t - SC[3]) * 9));
    p = pose({ x, y, z, s: CS, ry: 0.3, hp: -0.15, a: [[1.25, -0.25 - 0.35 * cl, 0.7], [1.25, -0.25 - 0.35 * cl, 0.7]] });
    f = { eyes: "happy", mouth: "grin", brows: "up" };
  } else if (t < SC[6]) { // tells it what he's working on; cheers when the skills land
    const [x, y, z] = stand(300, -0.75);
    deskG.position.set(X(300), FLOOR_Y, -0.35); deskG.rotation.y = 0.2;
    const inst = Wd(5, "installs") + 0.3, yay = t > inst;
    p = pose({ x, y, z, s: CS, ry: 0.2, hp: yay ? -0.2 : 0.22, lean: yay ? 0 : 0.1, a: yay ? [[2.7, 0.35, 0.25], [2.7, 0.35, 0.25]] : typing(t, 0.8) });
    if (t >= SC[5] && t < Wd(5, "picks") + 0.6 && !yay) { p.hp = -0.35; p.hy = -0.2 + 0.3 * Math.sin((t - SC[5]) * 1.5); p.a = [[0.3, 0.2, 0.4], [0.3, 0.2, 0.4]]; } // watches the bot fly
    if (yay) p.y += 0.08 * Math.abs(Math.sin((t - inst) * 9));
    f = yay ? { eyes: "happy", mouth: "laugh", brows: "up" } : { eyes: "open", mouth: "smile", brows: "flat", talk: t >= Wd(4, "tell") && t < TM.lines[4].end };
  } else if (t < SC[7]) { vis = false; }
  else { // CTA: phone up, then a high five with the bot
    const [x, y, z] = stand(390, -0.2), hf = Wd(7, "send");
    const reach = seg(t, hf - 0.25, hf);
    p = pose({ x, y, z, s: CS, ry: 0.35, a: [[0.2, 0.2, 0.3], [lerp(1.3, 2.7, reach), lerp(0.1, -0.3, reach), lerp(1.6, 0.2, reach)]], hp: -0.05 });
    f = t > hf ? { eyes: "happy", mouth: "grin", brows: "up" } : { eyes: "open", mouth: "smile", brows: "flat" };
  }
  phone.visible = t >= SC[7] && t < LOOP_AT;
  P.root.visible = vis;
  if (vis) { applyPose(P, p); setFace(P, f); }
}
function botAt(t) {
  let vis = true, p, f = { eyes: "open", mouth: "smile", brows: "flat" };
  qmark.g.visible = false;
  poof.forEach((m) => { m.visible = false; });
  const B = BOT;
  if (t < SC[2]) vis = false;
  else if (t < SC[3]) { // crash-lands with a poof, then points the right four out
    const land = Wd(2, "this") + 0.3, u = seg(t, land - 0.35, land);
    const [x, y, z] = stand(800, 0);
    const sq = t < land ? 1.08 : 1 - 0.28 * bump(t, land, 0.08);
    p = botPose({ x, y: y + 6 * (1 - i3(u)), z, ry: -0.35, sq, aL: [0.4, 0.5], aR: [0.4, 0.5] });
    const pt = Wd(2, "right") - 0.15;
    if (t > pt) p.aR = [2.4, 0.2];
    f = t < land + 0.2 ? { eyes: "wide", mouth: "o", brows: "up", noblink: true } : { eyes: "happy", mouth: "grin", brows: "up" };
    poof.forEach((m, i) => { const dt = t - land; m.visible = dt > 0 && dt < 0.6; if (!m.visible) return; const a = (i / poof.length) * TAU; m.position.set(x + Math.cos(a) * 2.2 * dt, y + 0.15 + Math.abs(Math.sin(a)) * 1.4 * dt, z + Math.sin(a) * 0.8 * dt); m.scale.setScalar(Math.max(0.01, 1 - dt / 0.6)); m.rotation.set(dt * 6, dt * 4, 0); });
  } else if (t < SC[4]) { // waves, jumps on "find-skills"
    const [x, y, z] = stand(830, 0), j = bump(t, Wd(3, "find"), 0.18);
    p = botPose({ x, y: y + 0.6 * j, z, ry: -0.3, sq: 1 + 0.12 * j, aL: [0.3, 0.3], aR: [2.6, 0.3 + 0.35 * Math.sin((t - SC[3]) * 12)] });
    f = { eyes: "happy", mouth: "grin", brows: "up" };
  } else if (t < SC[5]) { // reads along; "?" then a nod
    const [x, y, z] = stand(790, 0), nod = t > Wd(4, "reel") + 0.4;
    p = botPose({ x, y, z, ry: -0.5, tilt: nod ? 0.08 * Math.sin((t - Wd(4, "reel")) * 14) : 0.18, aL: [0.3, 0.3], aR: nod ? [1.6, 0.1] : [0.3, 0.3] });
    f = nod ? { eyes: "happy", mouth: "grin", brows: "up" } : { eyes: "side", mouth: "smile", brows: "flat" };
    qmark.g.visible = !nod && t > SC[4] + 0.3; qmark.at(840, 880, 0.3); qmark.g.rotation.y = 0.3 * Math.sin(t * 3);
  } else if (t < SC[6]) { // jetpacks through the galaxy, fetches four skills, drops them into the laptop
    const s = Wd(5, "searches"), pk = Wd(5, "picks"), inst = Wd(5, "installs");
    // the flight stays right of the creator and above his head, so it never crosses his face
    const k = kf(t, [[SC[5], { x: 790, y: 1279, z: 0, jet: 0 }], [SC[5] + 0.35, { x: 800, y: 980, z: 0.2, jet: 1 }], [s + 0.6, { x: 700, y: 900, z: -1.6, jet: 1 }], [pk - 0.1, { x: 830, y: 880, z: -1.0, jet: 1 }],
      [pk + 0.55, { x: 740, y: 1010, z: 0.3, jet: 1 }], [inst - 0.15, { x: 560, y: 1080, z: 0.4, jet: 1 }], [SC[6], { x: 570, y: 1070, z: 0.4, jet: 0.8 }]]);
    const bob = 0.06 * Math.sin(t * 7);
    p = botPose({ x: X(k.x), y: Y(k.y) + bob - (k.y >= 1270 ? 0 : 0.5), z: k.z, ry: k.x < 520 ? 0.4 : -0.4, tilt: 0.12 * Math.sin(t * 2.2), jet: k.jet, aL: [1.2, 0.3], aR: [1.2, 0.3], lL: 0.3, lR: 0.3 });
    if (t >= SC[6] - 0.5) { p.aR = [2.6, 0.2]; }
    f = t < pk ? { eyes: "open", mouth: "smirk", brows: "focus" } : { eyes: "happy", mouth: "grin", brows: "up" };
  } else if (t < SC[7]) { // on the #1 podium with the trophy
    const top = Y(1000), nb = Wd(6, "number"), up = t > nb;
    p = botPose({ x: X(505), y: top + 0.6 * bump(t, nb, 0.15), z: -0.6, ry: 0, aL: up ? [2.9, 0.2] : [0.4, 0.4], aR: up ? [2.9, 0.2] : [0.4, 0.4], mag: 0 });
    f = up ? { eyes: "star", mouth: "laugh", brows: "up", noblink: true } : { eyes: "happy", mouth: "grin", brows: "up" };
  } else { // CTA: high five
    const [x, y, z] = stand(640, -0.2), hf = Wd(7, "send"), reach = seg(t, hf - 0.25, hf), j = bump(t, hf - 0.05, 0.16);
    p = botPose({ x, y: y + 0.5 * j, z, ry: -0.4, aL: [0.3, 0.3], aR: [lerp(0.4, 2.7, reach), 0.2], mag: 0 });
    f = t > hf ? { eyes: "happy", mouth: "laugh", brows: "up" } : { eyes: "open", mouth: "smile", brows: "flat" };
  }
  B.root.visible = vis;
  if (!vis) return;
  applyBot(p, f);
  B.root.updateMatrixWorld(true);
  B.arms[1].children[1].getWorldPosition(BOT_HAND); // where held cards sit (scene 5)
  // the trophy sits in the raised hands on the podium
  if (t >= SC[6] && t < SC[7]) { trophy.position.set(X(505), Y(1000) + 1.78 * BS + 0.6 * bump(t, Wd(6, "number"), 0.15), -0.55); trophy.scale.setScalar(t > Wd(6, "number") ? 0.95 : 0.001); }
}

// ---------------------------------------------------------------- camera
// per scene: [whip yaw, whip pitch, roll]; a whip settles over 0.5 s at each cut; slow push within the scene
const SHOT = [[0, 0, 0], [0, 0.22, 0], [-0.18, 0, 0], [0.22, 0.05, 0], [-0.16, -0.04, 0], [0, 0.12, 0], [0.2, 0.04, 0], [-0.18, 0.04, 0]];
const PUNCH = [[Wd(0, "stop"), 0.025], [Wd(1, "million") + 0.3, 0.035], [Wd(3, "find"), 0.03], [Wd(5, "installs"), 0.025], [Wd(6, "number"), 0.03], [Wd(6, "four") + 0.75, 0.035], [Wd(7, "skills"), 0.03]];
const SHAKES = window.HF_SHAKES || [];
const TGT = new THREE.Vector3();
function cameraAt(t) {
  if (COVER) { camera.position.set(0, 0, D); camera.up.set(0, 1, 0); camera.lookAt(0, 0, 0); return; }
  let i = 0; while (i + 1 < SC.length - 1 && t >= SC[i + 1]) i++;
  const [wy, wp, wr] = SHOT[Math.min(i, SHOT.length - 1)], a = SC[i], b = SC[i + 1] ?? END;
  const w = i === 0 ? 0 : 1 - eo(seg(t, a, a + 0.5));
  let yaw = wy * w + 0.025 * Math.sin((TAU * t) / END * 3), pitch = wp * w + 0.012 * Math.sin((TAU * t) / END * 2), roll = wr;
  let dist = D * (1 + 0.08 * w) * (1 - 0.035 * io3(seg(t, a, b)));
  if (i === 1) dist *= 1 + 0.12 * (1 - o3(seg(t, a, a + 1.2))); // pull back to show the galaxy
  for (const [tp, k] of PUNCH) dist *= 1 - k * bump(t, tp, 0.12);
  let sx = 0, sy = 0;
  for (const [t0, amp, d] of SHAKES) { const dt = t - t0; if (dt >= 0 && dt < d) { const k = Math.exp(-dt * 7) * (1 - dt / d); sx += amp * k * Math.sin(dt * 90); sy += amp * 0.7 * k * Math.cos(dt * 73); } }
  TGT.set(-sx / U, sy / U, 0);
  camera.position.set(TGT.x + dist * Math.sin(yaw) * Math.cos(pitch), TGT.y + dist * Math.sin(pitch), dist * Math.cos(yaw) * Math.cos(pitch));
  camera.up.set(Math.sin(roll), Math.cos(roll), 0);
  camera.lookAt(TGT);
}

// ---------------------------------------------------------------- frame
function renderAt(time) {
  let t = clamp(time, 0, END);
  if (t >= LOOP_AT) t = 0; // the last frames repeat frame 0, so the reel loops cleanly
  NOW = t;
  cameraAt(t);
  GLOWS.forEach(({ s, o }) => { const ph = (TAU * t) / o.per; s.position.set(o.p[0] + o.m[0] * Math.sin(ph), o.p[1] + o.m[1] * Math.sin(ph * 0.5 + 1), o.p[2]); });
  cards.forEach((c, k) => { if (k >= GRID || t >= SC[1]) c.grp.visible = false; });
  creatorAt(t); botAt(t);
  gridAt(t); galaxyAt(t); rightFourAt(t); heroAt(t); panelsAt(t); podiumAt(t); ctaAt(t);
  composer.render();
}
const shown = (o) => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
function textBoxes() {
  const out = [], box = new THREE.Box3(), v = new THREE.Vector3();
  for (const it of TEXTS) {
    const obj = it.label || it.g, name = it.label ? it.label.userData.text : it.str;
    if (!name || !shown(obj) || (it.label && it.label.material.opacity < 0.05)) continue;
    box.makeEmpty(); obj.updateWorldMatrix(true, true); obj.traverseVisible((o) => { if (o.isMesh) box.expandByObject(o, true); });
    if (box.isEmpty()) continue;
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (let k = 0; k < 8; k++) { v.set(k & 1 ? box.max.x : box.min.x, k & 2 ? box.max.y : box.min.y, k & 4 ? box.max.z : box.min.z).project(camera); const px = (v.x + 1) * 540, py = (1 - v.y) * 960; x0 = Math.min(x0, px); x1 = Math.max(x1, px); y0 = Math.min(y0, py); y1 = Math.max(y1, py); }
    out.push({ name, x0, y0, x1, y1 });
  }
  return out;
}

"0123456789,.M#SKILNw?!".split("").forEach(glyph);
drawPrompt(0, true, false); drawList(0, 0);
renderer.compile(scene, camera);
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
renderAt(window.__hfThreeTime || 0);
resolveReady();
window.SCENE3D = { renderAt, ready, textBoxes };
