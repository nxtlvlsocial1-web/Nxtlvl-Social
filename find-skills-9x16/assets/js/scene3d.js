// find-skills-9x16: the 3D layer. A dark studio with warm rim light, extruded 3D type (Barlow Condensed Black) and
// one hero object per beat, shot with a moving camera. Headlines, captions and the comment box are HTML (index.html).
// Every time comes from the voiceover (window.TIMING, written by build/voice.py): scene starts and named spoken words,
// so a new take re-times the reel. Objects sit in the resting camera's pixel coordinates (helpers X, Y, L).
//   scene 0  hook: skill cards drop onto a pile one by one        scene 1  a galaxy of 2,400 cards, counter to 1,528,982
//   scene 2  the galaxy dims, the right four cards light up       scene 3  the find-skills card spins in
//   scene 4  a prompt types "find a skill for my content reel"    scene 5  a scan ring searches, picks four, installs
//   scene 6  3D leaderboard: find-skills #1, 4.5M installs        scene 7  SKILLS drops in letter by letter, a heart
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

// scene 0: a 3x3 grid filled one card at a time ("installing one by one"); each lands face-on and gets its check
const GRID = 9, DROP = 0.27, FIRST = -0.66; // card k lands at FIRST + k * DROP: three are in at frame 0, the fourth is mid-flight
const GX = [225, 505, 785], GY = [690, 850, 1010];
window.HOOK_LANDS = Array.from({ length: GRID }, (_, k) => FIRST + k * DROP); // the HTML tally counts the same landings
function pileAt(t) {
  if (t >= SC[1]) return;
  const ex = i3(seg(t, SC[1] - 0.24, SC[1])); // the grid blasts toward the lens into the galaxy
  for (let k = 0; k < GRID; k++) {
    const c = cards[k], land = FIRST + k * DROP, u = seg(t, land - 0.32, land);
    c.grp.visible = t >= land - 0.32;
    if (!c.grp.visible) continue;
    setCardOn(c, t >= land + 0.04);
    const e = bOut(u, 1.5), x = X(GX[k % 3]), y = Y(GY[Math.floor(k / 3)]);
    const dirx = (k % 3) - 1, diry = 1 - Math.floor(k / 3);
    c.grp.position.set(x + L(260) * (1 - e) * (k % 2 ? 1 : -1) + ex * dirx * 6, y - L(900) * (1 - e) + ex * diry * 4, 4 * (1 - e) + ex * 14);
    c.grp.rotation.set(-1.1 * (1 - e) + (hash(k) - 0.5) * 0.08 + ex * 2 * hash(k), (k % 2 ? -1 : 1) * 2.2 * (1 - e) + (hash(k * 3) - 0.5) * 0.12, (hash(k * 5) - 0.5) * 0.06 + ex * hash(k * 7));
    c.grp.scale.setScalar(0.85 * (1 + 0.06 * bump(t, land, 0.08)));
  }
}

// ---------------------------------------------------------------- the galaxy: 2,400 tiny cards
const NG = 2400;
const gTex = (() => { const c = cnv(128, 64), g = c.getContext("2d"); rr(g, 2, 2, 124, 60, 12); g.fillStyle = "#ffffff"; g.fill(); g.fillStyle = "rgba(0,0,0,.35)"; rr(g, 12, 12, 26, 26, 6); g.fill(); rr(g, 46, 16, 64, 8, 4); g.fill(); rr(g, 46, 32, 44, 8, 4); g.fill(); return tex(c); })();
const galaxy = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.62, 0.31), new THREE.MeshBasicMaterial({ map: gTex, transparent: true, toneMapped: false, side: THREE.DoubleSide, depthWrite: false, fog: true }), NG);
const GP = [], GC = [new THREE.Color("#2b3348"), new THREE.Color("#3a4560"), new THREE.Color("#5a4630"), new THREE.Color("#2f3b5e")];
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S3 = new THREE.Vector3(), E = new THREE.Euler(), COL = new THREE.Color();
for (let i = 0; i < NG; i++) {
  const r = 4 + Math.pow(hash(i * 1.7), 0.7) * 34, th = hash(i * 2.3) * TAU, ph = Math.acos(2 * hash(i * 3.1) - 1);
  GP.push({ p: new THREE.Vector3(r * Math.sin(ph) * Math.cos(th), r * Math.cos(ph) * 0.8, -6 - r * Math.sin(ph) * Math.sin(th) * 0.9), r, rot: [(hash(i) - 0.5) * 0.8, (hash(i * 5) - 0.5) * 1.2, (hash(i * 9) - 0.5) * 0.6], c: GC[i % GC.length], ph: hash(i * 11) * TAU });
}
galaxy.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(NG * 3), 3);
galaxy.frustumCulled = false; scene.add(galaxy);
const counter = new T3({ size: 172, style: "white" });
const ringScan = new THREE.Mesh(new THREE.TorusGeometry(1, 0.035, 8, 160), neonO); ringScan.rotation.x = Math.PI / 2; scene.add(ringScan);
function galaxyAt(t) {
  const on = t >= SC[1] && t < SC[6];
  galaxy.visible = on;
  counter.g.visible = t >= SC[1] && t < SC[2];
  ringScan.visible = false;
  if (!on) return;
  const appear = o3(seg(t, SC[1], SC[1] + 0.8));
  const dim = seg(t, Wd(2, "the"), Wd(2, "right"));               // scene 2: everything else fades back
  const scan0 = Wd(5, "searches"), scanR = 2 + seg(t, scan0, scan0 + 1.6) * 30; // scene 5: the scan ring sweeps out through the cards
  const scanning = t >= scan0 && t < scan0 + 1.7;
  for (let i = 0; i < NG; i++) {
    const g = GP[i], drift = 0.25 * Math.sin(t * 0.6 + g.ph);
    const s = appear * (0.85 + 0.3 * hash(i * 13));
    V.copy(g.p).multiplyScalar(lerp(0.15, 1, appear)); V.y += drift;
    E.set(g.rot[0] + t * 0.05, g.rot[1] + t * 0.08, g.rot[2]); Q.setFromEuler(E); S3.set(s, s, s);
    M4.compose(V, Q, S3); galaxy.setMatrixAt(i, M4);
    COL.copy(g.c);
    if (t >= SC[2]) COL.multiplyScalar(lerp(1, 0.35, dim));
    if (scanning) { const dd = Math.abs(g.r - scanR); if (dd < 2.2) COL.lerp(new THREE.Color(ORANGE), (1 - dd / 2.2) * 0.7); }
    galaxy.setColorAt(i, COL);
  }
  galaxy.instanceMatrix.needsUpdate = true; galaxy.instanceColor.needsUpdate = true;
  if (scanning) { const rr2 = Math.min(scanR, 13); ringScan.visible = scanR < 14; ringScan.scale.setScalar(rr2); ringScan.position.set(0, Y(760), -18); }
  if (counter.g.visible) {
    const c = io3(seg(t, SC[1] + 0.1, Wd(1, "million") + 0.3));
    counter.set(fmt(1528982 * c)).at(505, 770, lerp(-2, 0, o3(seg(t, SC[1], SC[1] + 0.5))));
    counter.g.rotation.set(0, 0.08 * Math.sin((t - SC[1]) * 1.6), 0);
    counter.g.scale.setScalar(1 + 0.06 * bump(t, Wd(1, "million") + 0.3, 0.12));
  }
}

// scene 2: the right four light up and come forward; scene 5: the same four are picked and installed
const RIGHT = [0, 1, 2, 3]; // captions, video editing, thumbnails, hook writing
function rightFourAt(t) {
  const s2 = t >= SC[2] && t < SC[3];
  const s5 = t >= SC[5] && t < SC[6];
  RIGHT.forEach((k, i) => {
    const c = cards[k];
    if (!(s2 || s5)) { if (t >= SC[1]) c.grp.visible = false; return; }
    c.grp.visible = true;
    if (s2) {
      const a = Wd(2, "right") - 0.1 + i * 0.09, u = bOut(seg(t, a, a + 0.42), 1.6);
      c.grp.visible = t >= a;
      const px = [300, 710][i % 2], py = [720, 910][i >> 1];
      c.grp.position.set(lerp(X(px) * 2.2, X(px), u), lerp(Y(py) + 3, Y(py), u), lerp(-14, 0, u));
      c.grp.rotation.set(0, (1 - u) * 1.5 + 0.06 * Math.sin(t * 2 + i), (i % 2 ? 0.03 : -0.03));
      c.grp.scale.setScalar(1.1);
      setCardOn(c, t >= a + 0.3);
    } else {
      const a = Wd(5, "picks") + i * 0.12, u = o3(seg(t, a, a + 0.45));
      const inst = Wd(5, "installs") + i * 0.14;
      c.grp.visible = t >= a - 0.05;
      const from = new THREE.Vector3((hash(k * 4) - 0.5) * 16, (hash(k * 6) - 0.2) * 9, -18);
      const to = new THREE.Vector3(X(200), Y(918 + i * 88), 0.3);
      c.grp.visible = t >= a - 0.05 && u < 1; // it lands in its checklist row, which takes over showing the name
      c.grp.position.lerpVectors(from, to, u);
      c.grp.rotation.set(0, (1 - u) * 3, 0);
      c.grp.scale.setScalar(lerp(0.9, 0.25, u));
      setCardOn(c, true);
      void inst;
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
  hero.position.set(X(505), Y(800) + L(10) * Math.sin((t - a) * 2.2), lerp(-30, 0, eo(u)));
  hero.rotation.set(lerp(0.6, -0.05, eo(u)), lerp(-TAU, 0, eo(u)) + 0.1 * Math.sin((t - a) * 1.4) * u, 0);
  hero.scale.setScalar(1 + 0.04 * bump(t, Wd(3, "vercel"), 0.15));
}

// ---------------------------------------------------------------- scenes 4-5: the prompt and the install checklist
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
listG.add(new THREE.Mesh(new RoundedBoxGeometry(L(880), L(460), L(24), 4, L(44)), physical({ color: 0x131722, metalness: 0.4, roughness: 0.3 })));
const lC = cnv(1760, 920), lT = tex(lC); let lKey = "";
const lFace = new THREE.Mesh(new THREE.PlaneGeometry(L(880) * 0.985, L(460) * 0.98), new THREE.MeshBasicMaterial({ map: lT, transparent: true, toneMapped: false }));
lFace.position.z = L(12) + 0.004; listG.add(lFace);
function drawList(found, done) {
  const k = found + "|" + done; if (k === lKey) return; lKey = k;
  const g = lC.getContext("2d"); g.clearRect(0, 0, 1760, 920);
  rr(g, 0, 0, 1760, 920, 88); g.fillStyle = "#131722"; g.fill();
  g.fillStyle = MUTED; g.font = "700 38px IN"; g.letterSpacing = "6px"; g.fillText(done >= 4 ? "INSTALLED · 4 OF 4" : found ? `INSTALLING · ${done} OF 4` : "SEARCHING 1,528,982 SKILLS", 80, 104); g.letterSpacing = "0px";
  RIGHT.forEach((ci, i) => {
    const y = 186 + i * 176;
    g.fillStyle = "rgba(255,255,255,.05)"; rr(g, 60, y, 1640, 140, 30); g.fill();
    if (i < done) { g.fillStyle = GREEN; g.beginPath(); g.arc(1600, y + 70, 42, 0, TAU); g.fill(); g.strokeStyle = "#0b0d14"; g.lineWidth = 12; g.beginPath(); g.moveTo(1580, y + 70); g.lineTo(1596, y + 88); g.lineTo(1624, y + 54); g.stroke(); g.fillStyle = GREEN; g.font = "800 44px IN"; g.textAlign = "right"; g.fillText("installed", 1530, y + 86); g.textAlign = "left"; }
    else if (i < found) { g.fillStyle = AMBER; g.font = "800 44px IN"; g.textAlign = "right"; g.fillText("found", 1640, y + 86); g.textAlign = "left"; }
    if (i < found) { rr(g, 96, y + 26, 88, 88, 20); g.fillStyle = ICON[ci % ICON.length]; g.fill(); g.fillStyle = "#0b0d14"; g.font = "900 60px BC"; g.textAlign = "center"; g.fillText(NAMES[ci][0].toUpperCase(), 140, y + 92); g.textAlign = "left"; g.fillStyle = INK; g.font = "800 62px IN"; g.fillText(NAMES[ci], 222, y + 92); }
  });
  g.fillStyle = "rgba(255,255,255,.08)"; rr(g, 80, 880 - 30, 1600, 16, 8); g.fill();
  g.fillStyle = done >= 4 ? GREEN : ORANGE; rr(g, 80, 880 - 30, 1600 * (done / 4), 16, 8); g.fill();
  lT.needsUpdate = true;
}
function promptAt(t) {
  const on = t >= SC[4] && t < SC[6];
  promptG.visible = on;
  listG.visible = t >= SC[5] && t < SC[6];
  if (!on) return;
  const u = bOut(seg(t, SC[4], SC[4] + 0.45), 1.5);
  const up = o3(seg(t, SC[5], SC[5] + 0.5));
  promptG.position.set(X(505), lerp(Y(1400), Y(740), u) + (Y(660) - Y(740)) * up, 0);
  promptG.rotation.set(lerp(-0.9, 0.04, u), 0.05 * Math.sin(t * 1.3), 0);
  const t0 = Wd(4, "tell"), t1 = Wd(4, "reel") + 0.25;
  const n = Math.round(PROMPT.length * clamp((t - t0) / (t1 - t0)));
  const sent = t >= Wd(4, "reel") + 0.45;
  drawPrompt(t < t0 ? 0 : n, !sent && Math.floor(t * 3.2) % 2 === 0, sent);
  if (listG.visible) {
    const lu = bOut(seg(t, SC[5] + 0.15, SC[5] + 0.6), 1.4);
    listG.position.set(X(505), lerp(Y(1500), Y(1020), lu), 0);
    listG.rotation.set(lerp(-0.7, 0.03, lu), -0.04 * Math.sin(t * 1.1), 0);
    const found = RIGHT.filter((_, i) => t >= Wd(5, "picks") + i * 0.12 + 0.45).length;
    const done = RIGHT.filter((_, i) => t >= Wd(5, "installs") + i * 0.14).length;
    drawList(found, done);
  }
}

// ---------------------------------------------------------------- scene 6: leaderboard
const lbG = new THREE.Group(); scene.add(lbG);
const LB = [["find-skills", 4.5], ["hyperframes-cli", 1.7], ["agent-browser", 1.7], ["hyperframes", 1.7]];
const BX0 = 376, BMAX = 460;
const bars = LB.map(([name, v], i) => {
  const mat = i === 0 ? physical({ color: 0xff7a2f, emissive: 0xff7a2f, emissiveIntensity: 0.35, roughness: 0.18 }) : physical({ color: 0x3a4157, roughness: 0.35 });
  const geo = new RoundedBoxGeometry(1, L(64), L(64), 3, L(16)); geo.translate(0.5, 0, 0);
  const m = new THREE.Mesh(geo, mat); lbG.add(m);
  const nm = label(`${i + 1}  ${name}`, 26, i === 0 ? INK : "#C3C7D4", { track: 0.02, weight: 800, parent: lbG });
  const val = label(`${v}M`, 30, i === 0 ? AMBER : "#C3C7D4", { family: "BC", weight: 900, track: 0.02, parent: lbG });
  return { m, nm, val, v, i };
});
const big = new T3({ size: 230, style: "money", tab: false });
const bigLbl = label("INSTALLS", 28, "#C3C7D4", { parent: lbG });
const badge = label("#1", 44, "#0B0D14", { family: "BC", weight: 900, track: 0.02, pill: true, fill: AMBER, stroke: AMBER, parent: lbG });
const lbDate = label("skills.sh all-time installs · 23 Nov 2026", 22, "#8E94A8", { weight: 600, track: 0.02, parent: lbG });
function boardAt(t) {
  const on = t >= SC[6] && t < SC[7];
  lbG.visible = big.g.visible = on;
  if (!on) return;
  bars.forEach((b) => {
    const a = SC[6] + 0.15 + b.i * 0.1, u = o3(seg(t, a, a + 0.7));
    const w = L(BMAX * (b.v / 4.5)) * Math.max(0.001, u);
    const y = Y(860 + b.i * 92);
    b.m.scale.set(w, 1, 1); b.m.position.set(X(BX0), y, 0);
    b.nm.position.set(X(BX0 - 18) - L(b.nm.userData.w) / 2, y, 0.05); b.nm.material.opacity = seg(t, a, a + 0.25);
    b.val.position.set(X(BX0) + w + L(b.val.userData.w) / 2 + L(8), y, 0.05); b.val.material.opacity = seg(t, a + 0.4, a + 0.6);
  });
  const nb = Wd(6, "number"), bu = seg(t, nb, nb + 0.25);
  badge.visible = t >= nb; badge.position.set(X(BX0 + 30) + L(badge.userData.w) / 2, Y(860) + L(70), lerp(4, 0.3, i3(bu)));
  badge.scale.setScalar(lerp(2.2, 1, i3(bu)) * (1 + 0.1 * bump(t, nb + 0.25, 0.1)));
  const m0 = Wd(6, "four") - 0.1, mc = io3(seg(t, SC[6] + 0.2, m0 + 0.75));
  big.set((4.5 * mc).toFixed(1) + "M").at(505, 590, 0);
  big.g.visible = t >= SC[6] + 0.1;
  big.g.rotation.set(0, 0.07 * Math.sin((t - SC[6]) * 1.4), 0);
  big.g.scale.setScalar((0.7 + 0.3 * bOut(seg(t, SC[6] + 0.1, SC[6] + 0.45), 2)) * (1 + 0.07 * bump(t, m0 + 0.75, 0.12)));
  bigLbl.position.set(X(505), Y(708), 0); bigLbl.material.opacity = seg(t, SC[6] + 0.3, SC[6] + 0.5);
  lbDate.position.set(X(505), Y(1222), 0); lbDate.material.opacity = seg(t, SC[6] + 0.8, SC[6] + 1.0);
}

// ---------------------------------------------------------------- scene 7: SKILLS, letter by letter, and a heart
const word = new T3({ size: 250, style: "money", tab: false, track: 0.03 }); word.set("SKILLS");
const heart = new THREE.Group(); scene.add(heart);
{
  const s = new THREE.Shape(), k = L(80) / 30;
  s.moveTo(0, -24 * k); s.bezierCurveTo(-18 * k, -10 * k, -30 * k, 0, -30 * k, 12 * k); s.bezierCurveTo(-30 * k, 22 * k, -22 * k, 28 * k, -15 * k, 28 * k); s.bezierCurveTo(-8 * k, 28 * k, -3 * k, 24 * k, 0, 18 * k);
  s.bezierCurveTo(3 * k, 24 * k, 8 * k, 28 * k, 15 * k, 28 * k); s.bezierCurveTo(22 * k, 28 * k, 30 * k, 22 * k, 30 * k, 12 * k); s.bezierCurveTo(30 * k, 0, 18 * k, -10 * k, 0, -24 * k);
  const g = new THREE.ExtrudeGeometry(s, { depth: L(30), bevelEnabled: true, bevelThickness: L(14), bevelSize: L(12), bevelSegments: 6, curveSegments: 18 }); g.center();
  heart.add(new THREE.Mesh(g, physical({ color: 0xff5c5c, emissive: 0xff3b3b, emissiveIntensity: 0.25, roughness: 0.2 })));
}
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
    heart.scale.setScalar(Math.max(0.001, bOut(u, 4)));
    heart.position.set(X(850), Y(1190) + L(16) * u, 0.3);
    heart.rotation.set(0.1, (t - Wd(7, "send")) * 2.2 - 0.6, -0.12);
  }
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
  cameraAt(t);
  GLOWS.forEach(({ s, o }) => { const ph = (TAU * t) / o.per; s.position.set(o.p[0] + o.m[0] * Math.sin(ph), o.p[1] + o.m[1] * Math.sin(ph * 0.5 + 1), o.p[2]); });
  cards.forEach((c, k) => { if (k >= GRID || t >= SC[1]) c.grp.visible = false; });
  pileAt(t); galaxyAt(t); rightFourAt(t); heroAt(t); promptAt(t); boardAt(t); ctaAt(t);
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

if (COVER) { /* cover.html sets the frame it wants */ }
"0123456789,.M#SKILNw".split("").forEach(glyph);
drawPrompt(0, true, false); drawList(0, 0);
renderer.compile(scene, camera);
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
renderAt(window.__hfThreeTime || 0);
resolveReady();
window.SCENE3D = { renderAt, ready, textBoxes };
