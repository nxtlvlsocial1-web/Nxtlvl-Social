// Creators 100X "AI wrote this reel": the soft-3D layer (three.js), a pure function of time.
// generate.py inlines this module after `const C = {...}` (word times) and the DOM/GSAP layer. The GSAP timeline calls
// window.__render3(t) through a tween setter on every seek, and the HyperFrames three adapter sends hf-seek too.
import * as THREE from "./assets/vendor/three.module.min.js";

const W = 1080, H = 1920;
const canvas = document.getElementById("gl3d");
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 200);
const Y0 = -0.45;                          // vertical centre of the action (below the headline band)

// ---------- tiny animation kit (deterministic) ----------
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const E = {
  lin: (x) => x,
  out: (x) => 1 - Math.pow(1 - x, 3),
  in: (x) => x * x * x,
  io: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  back: (x) => { const c = 2.0; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); },
  el: (x) => (x === 0 || x === 1 ? x : Math.pow(2, -9 * x) * Math.sin((x * 10 - 0.75) * (2 * Math.PI) / 3) + 1),
};
const lerp = (a, b, k) => a + (b - a) * k;
// p(t, t0, d, ease) -> 0..1
const p = (t, t0, d, e = "out") => E[e](clamp((t - t0) / d));
// keyframes: [[t, v, ease], ...] (ease = easing INTO that key); v number or array
function kf(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t1, v1, e = "io"] = keys[i];
    if (t <= t1) {
      const [t0, v0] = keys[i - 1];
      const k = E[e]((t - t0) / Math.max(1e-6, t1 - t0));
      return Array.isArray(v0) ? v0.map((a, j) => lerp(a, v1[j], k)) : lerp(v0, v1, k);
    }
  }
  return keys[keys.length - 1][1];
}
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let x = Math.imul(seed ^ (seed >>> 15), 1 | seed); x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; }; }
const wob = (t, f, a, ph = 0) => Math.sin(t * f + ph) * a;

// ---------- colours & materials ----------
const COL = { ink: 0x101111, pink: 0xfd0b68, lime: 0xccfb79, paper: 0xfdf4f4, grey: 0x8e9199 };
function glossy(color, o = {}) {
  return new THREE.MeshPhysicalMaterial({ color, roughness: o.r ?? 0.32, metalness: o.m ?? 0, clearcoat: o.cc ?? 1, clearcoatRoughness: o.ccr ?? 0.12, ...o.x });
}

// environment: a soft studio built from emissive panels, pre-filtered once
{
  const env = new THREE.Scene();
  env.background = new THREE.Color(0x2a2628);
  const panel = (w, h, c, pos, look) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: c, side: THREE.DoubleSide }));
    m.position.set(...pos); m.lookAt(...look); env.add(m);
  };
  panel(14, 8, 0xffffff, [-8, 9, 6], [0, 0, 0]);
  panel(10, 10, 0xffe4ef, [9, 3, 5], [0, 0, 0]);
  panel(16, 4, 0xe9ffd0, [0, -8, 4], [0, 0, 0]);
  panel(20, 12, 0xfff7f2, [0, 4, -12], [0, 0, 0]);
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(env, 0.035).texture;
  pm.dispose();
}
const hemi = new THREE.HemisphereLight(0xffffff, 0xffc7dc, 0.9);
const key = new THREE.DirectionalLight(0xffffff, 2.0); key.position.set(-5, 8, 10);
const rim = new THREE.DirectionalLight(0xff8fc0, 1.4); rim.position.set(6, 3, -6);
scene.add(hemi, key, rim);

// ---------- geometry helpers ----------
function rrShape(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}
function slabGeo(w, h, d, r, bevel = 0.12) {
  const g = new THREE.ExtrudeGeometry(rrShape(w - 2 * bevel, h - 2 * bevel, Math.max(0.02, r - bevel)),
    { depth: d - 2 * bevel, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 5, curveSegments: 12 });
  g.translate(0, 0, -(d - 2 * bevel) / 2);
  g.computeVertexNormals();
  return g;
}
// a canvas-textured face that sits on the front of a slab
function face(w, h, cw, ch) {
  const cv = document.createElement("canvas"); cv.width = cw; cv.height = ch;
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false }));
  return { cv, ctx: cv.getContext("2d"), tex, mesh, key: null };
}
function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
function wrap(ctx, text, x, y, maxW, lh) {
  const words = text.split(" "); let line = "", yy = y;
  for (const w of words) {
    const test = line ? line + " " + w : w;
    if (ctx.measureText(test).width > maxW && line) { ctx.fillText(line, x, yy); line = w; yy += lh; } else line = test;
  }
  if (line) ctx.fillText(line, x, yy);
  return yy;
}
// a soft contact shadow under an object
const shadowTex = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d");
  const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, "rgba(60,20,40,.55)"); gr.addColorStop(1, "rgba(60,20,40,0)");
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c);
})();
function shadow(w, h) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false, toneMapped: false }));
  return m;
}
const setOp = (obj, o) => obj.traverse((n) => { if (n.material) { n.material.transparent = true; n.material.opacity = o; } });

// =====================================================================================================
// 1. the chat window (robot grey -> Creators 100X white), reply typing word by word
// =====================================================================================================
const chat = new THREE.Group();
const chatBodyMat = glossy(0x3b3e45, { r: 0.35, m: 0.35 });
const chatBody = new THREE.Mesh(slabGeo(5.5, 4.4, 0.55, 0.5), chatBodyMat);
const chatFace = face(5.1, 4.0, 1020, 800); chatFace.mesh.position.z = 0.285;
const chatShadow = shadow(7.5, 2.2); chatShadow.rotation.x = -Math.PI / 2; chatShadow.position.set(0, -2.9, 0);
chat.add(chatBody, chatFace.mesh);
scene.add(chat);
const REPLY1 = C.reply1;        // [[word, t0], ...] "This reel was written by ChatGPT. And honestly, that's the point."
function drawChat(t) {
  const robot = t < C.sw;
  const n = REPLY1.filter(([, t0]) => t0 <= t + 0.04).length;
  const hl = robot ? 0 : Math.round(p(t, C.point, 0.45, "out") * 20) / 20;
  const k = `${robot}|${n}|${hl}|${Math.floor(t * 4) % 2}`;
  if (chatFace.key === k) return;
  chatFace.key = k;
  const g = chatFace.ctx, Wc = 1020, Hc = 800;
  g.clearRect(0, 0, Wc, Hc);
  rr(g, 0, 0, Wc, Hc, 56); g.fillStyle = robot ? "#16181c" : "#101111"; g.fill();
  // header
  g.fillStyle = robot ? "#2a2d33" : "#ccfb79"; g.beginPath(); g.arc(80, 78, 26, 0, 7); g.fill();
  g.font = robot ? "700 34px Mono" : "800 36px Inter"; g.fillStyle = robot ? "#9da1aa" : "#ffffff"; g.textBaseline = "middle";
  g.fillText("ChatGPT", 124, 80);
  g.font = "700 22px Mono"; g.fillStyle = robot ? "#5b5f68" : "#8a8f8a"; g.fillText(robot ? "GENERATING" : "REEL SCRIPT", 790, 80);
  g.fillStyle = robot ? "#22252a" : "#232525"; g.fillRect(48, 128, Wc - 96, 3);
  // the user's prompt (collapsed: five parts)
  const pr = ["ROLE", "AUDIENCE", "HOOK RULE", "FORMAT", "TONE"];
  g.font = "700 22px Mono"; let x = Wc - 56; const chips = [];
  for (let i = pr.length - 1; i >= 0; i--) { const w = g.measureText(pr[i]).width + 34; x -= w + 10; chips.unshift([pr[i], x, w]); }
  for (const [s, cx, w] of chips) { rr(g, cx, 160, w, 48, 24); g.fillStyle = robot ? "#26292f" : "#1f2121"; g.fill(); g.fillStyle = robot ? "#7d818a" : "#ccfb79"; g.fillText(s, cx + 17, 185); }
  // the reply, word by word
  const words = REPLY1.slice(0, n).map(([w]) => w).join(" ");
  g.textBaseline = "alphabetic";
  g.font = robot ? "700 66px Mono" : "800 76px Inter";
  const lh = robot ? 88 : 92, x0 = 64, y0 = 350;
  if (!robot && hl > 0) {           // lime highlighter over "written by ChatGPT."
    const full = REPLY1.map(([w]) => w).join(" ");
    g.save(); g.globalAlpha = 0.9; g.fillStyle = "#ccfb79";
    rr(g, x0 - 10, y0 - 70, (Wc - 2 * x0 + 20) * hl, 92, 14); g.fill(); g.restore();
    void full;
  }
  g.fillStyle = robot ? "#c9ccd2" : "#ffffff";
  const yEnd = wrap(g, words, x0, y0, Wc - 2 * x0, lh);
  if (!robot && hl > 0) {           // first line re-inked dark on the highlighter
    g.save(); g.beginPath(); g.rect(x0 - 10, y0 - 70, (Wc - 2 * x0 + 20) * hl, 92); g.clip();
    g.fillStyle = "#101111"; wrap(g, words, x0, y0, Wc - 2 * x0, lh); g.restore();
  }
  // caret
  if (Math.floor(t * 4) % 2 === 0) {
    const last = words.split(" ").slice(-1)[0] || "";
    g.fillStyle = robot ? "#c9ccd2" : "#ccfb79";
    const lineTxt = (() => { const ws = words.split(" "); let line = ""; for (const w of ws) { const tt = line ? line + " " + w : w; if (g.measureText(tt).width > Wc - 2 * x0 && line) line = w; else line = tt; } return line; })();
    g.fillRect(x0 + g.measureText(lineTxt).width + 10, yEnd - 62, 9, 74);
    void last;
  }
  chatFace.tex.needsUpdate = true;
}
const bodyGrey = new THREE.Color(0x3b3e45), bodyWhite = new THREE.Color(0xf6efef);
function poseChat(t) {
  const vis = t < C.r2 + 0.35;
  chat.visible = vis;
  if (!vis) return;
  drawChat(t);
  const k = p(t, C.sw, 0.4, "out");
  chatBodyMat.color.copy(bodyGrey).lerp(bodyWhite, k);
  chatBodyMat.metalness = lerp(0.35, 0, k); chatBodyMat.roughness = lerp(0.35, 0.28, k);
  const enter = p(t, -0.05, 0.6, "back");
  const out = p(t, C.r2 - 0.12, 0.3, "in");
  // glitch jitter around the switch
  const gl = t > C.sw - 0.32 && t < C.sw + 0.08 ? (rng(Math.floor(t * 30))() - 0.5) * 0.5 : 0;
  chat.position.set(gl + out * -9, Y0 + 0.2 + wob(t, 1.6, 0.06) + (1 - enter) * -1.5, 0);
  chat.rotation.set(-0.08 + wob(t, 1.1, 0.03), lerp(-0.22, 0.12, p(t, 0, 4.2, "io")) + out * -0.6, wob(t, 0.9, 0.015) + gl * 0.1);
  const s = lerp(0.85, 1, enter) * (1 + 0.06 * Math.sin(Math.PI * clamp((t - C.sw) / 0.35)));
  chat.scale.setScalar(s);
}

// =====================================================================================================
// 2. the lazy prompt: an input pill + the generic reply card; then the wall of identical cards
// =====================================================================================================
const lazy = new THREE.Group(); scene.add(lazy);
const pillMat = glossy(0xffffff, { r: 0.3 });
const pill = new THREE.Mesh(slabGeo(5.3, 0.95, 0.4, 0.47), pillMat);
const pillFace = face(5.1, 0.85, 1020, 170); pillFace.mesh.position.z = 0.205;
const pillG = new THREE.Group(); pillG.add(pill, pillFace.mesh); lazy.add(pillG);
const LAZY = "Write me a reel script";
function drawPill(t) {
  const n = Math.round(clamp((t - C.write) / Math.max(0.3, C.scriptEnd - C.write)) * LAZY.length);
  const sent = t > C.send;
  const k = `${n}|${sent}|${Math.floor(t * 4) % 2}`;
  if (pillFace.key === k) return; pillFace.key = k;
  const g = pillFace.ctx; g.clearRect(0, 0, 1020, 170);
  g.font = "600 50px Inter"; g.fillStyle = "#101111"; g.textBaseline = "middle";
  const s = LAZY.slice(0, n); g.fillText(s, 50, 88);
  if (!sent && Math.floor(t * 4) % 2 === 0) { g.fillStyle = "#fd0b68"; g.fillRect(56 + g.measureText(s).width, 60, 5, 56); }
  g.fillStyle = sent ? "#fd0b68" : "#101111"; g.beginPath(); g.arc(940, 85, 52, 0, 7); g.fill();
  g.strokeStyle = "#fff"; g.lineWidth = 9; g.lineCap = "round"; g.lineJoin = "round";
  g.beginPath(); g.moveTo(940, 112); g.lineTo(940, 60); g.moveTo(918, 82); g.lineTo(940, 60); g.lineTo(962, 82); g.stroke();
  pillFace.tex.needsUpdate = true;
}
const GENERIC = "Hey guys! In today's video, I'll share some amazing tips to boost your engagement and grow your page...";
const cardGeo = slabGeo(5.0, 2.7, 0.36, 0.34);
const cardMat = glossy(0xe9e9ec, { r: 0.45, cc: 0.4 });
const genFace = face(4.7, 2.45, 940, 490);
(function drawGeneric() {
  const g = genFace.ctx; g.clearRect(0, 0, 940, 490);
  g.fillStyle = "#c5c7cd"; g.beginPath(); g.arc(64, 64, 26, 0, 7); g.fill();
  g.font = "700 30px Inter"; g.fillStyle = "#8e9199"; g.textBaseline = "middle"; g.fillText("ChatGPT", 104, 66);
  g.textBaseline = "alphabetic"; g.font = "700 50px Inter"; g.fillStyle = "#6b6e76";
  wrap(g, GENERIC, 44, 170, 852, 66);
  genFace.tex.needsUpdate = true;
})();
genFace.mesh.position.z = 0.185;
const reply = new THREE.Group(); reply.add(new THREE.Mesh(cardGeo, cardMat), genFace.mesh); lazy.add(reply);
// sparkles that fizzle ("don't expect magic")
const SPN = 34, spR = rng(7);
const spark = new THREE.InstancedMesh(new THREE.OctahedronGeometry(0.09, 0), new THREE.MeshStandardMaterial({ color: 0xffd6ea, emissive: 0xfd0b68, emissiveIntensity: 0.6 }), SPN);
const SPD = Array.from({ length: SPN }, () => [spR() * Math.PI * 2, 1.2 + spR() * 1.8, spR() * 0.25, 0.5 + spR()]);
lazy.add(spark);
// the wall of identical generic cards
const WALL = []; const wr = rng(11);
for (let r = -3; r <= 3; r++) for (let c = -2; c <= 2; c++) { if (r === 0 && c === 0) continue; WALL.push([c * 5.6, r * 3.2, -wr() * 2.5, Math.hypot(c, r * 0.8) + wr() * 0.4]); }
const wallBody = new THREE.InstancedMesh(cardGeo, cardMat, WALL.length);
const wallFace = new THREE.InstancedMesh(genFace.mesh.geometry, genFace.mesh.material, WALL.length);
lazy.add(wallBody, wallFace);
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _v = new THREE.Vector3(), _s = new THREE.Vector3();
function poseLazy(t) {
  const vis = t > C.r2 + 0.1 && t < C.task + 0.6;
  lazy.visible = vis;
  if (!vis) return;
  drawPill(t);
  const inP = p(t, C.r2 + 0.12, 0.45, "back");
  const pillUp = p(t, C.dont - 0.2, 0.4, "io");
  pillG.visible = t < C.wall + 0.6;
  pillG.position.set(lerp(7, 0, inP), Y0 + lerp(0.2, 2.25, pillUp), 0.3);
  pillG.rotation.set(0, lerp(0.5, 0, inP) + wob(t, 1.3, 0.04), 0);
  pillG.scale.setScalar(1 + 0.08 * Math.sin(Math.PI * clamp((t - C.send) / 0.25)) - p(t, C.wall, 0.4, "in") * 0.5);
  // reply card pops out of the pill
  const rp = p(t, C.dont - 0.1, 0.55, "back");
  reply.visible = t > C.dont - 0.1 && t < C.mistake + 0.12;
  reply.position.set(0, Y0 + lerp(1.5, -0.35, rp) + wob(t, 1.4, 0.05), 0);
  reply.rotation.set(wob(t, 1.0, 0.04), wob(t, 0.8, 0.08), wob(t, 1.2, 0.02));
  const crumple = p(t, C.mistake, 0.16, "in");
  reply.scale.set(lerp(0.3, 1, rp) * (1 - crumple * 0.75), lerp(0.3, 1, rp) * (1 - crumple * 0.8), 1);
  // fizzling sparkles around "magic"
  const ts = t - C.magic;
  spark.visible = ts > -0.05 && ts < 1.3;
  for (let i = 0; i < SPN; i++) {
    const [a, sp, dl, sz] = SPD[i]; const tt = Math.max(0, ts - dl);
    const up = Math.min(tt, 0.35) * sp * 2.2; const fall = Math.max(0, tt - 0.35);
    _v.set(Math.cos(a) * (0.6 + up * 0.9), Y0 + 1.2 + Math.sin(a) * 0.6 + up - fall * fall * 7, 0.8);
    const sc = sz * (tt > 0 ? 1 : 0) * (1 - clamp((tt - 0.6) / 0.6));
    _e.set(tt * 6, tt * 4, 0); _q.setFromEuler(_e); _s.setScalar(Math.max(0.0001, sc));
    spark.setMatrixAt(i, _m.compose(_v, _q, _s));
  }
  spark.instanceMatrix.needsUpdate = true;
  spark.material.emissiveIntensity = lerp(0.9, 0, clamp(ts / 0.6));
  spark.material.color.set(ts < 0.4 ? 0xffd6ea : 0x9a9ca3);
  // the wall
  const wv = t > C.wall - 0.1 && t < C.mistake + 0.5;
  wallBody.visible = wallFace.visible = wv;
  if (wv) {
    WALL.forEach(([x, y, z, d], i) => {
      const a = p(t, C.wall + d * 0.32, 0.4, "back");
      const fall = p(t, C.r3 - 0.2 + d * 0.05, 0.6, "in");
      const flash = Math.max(0, 1 - Math.abs(t - (C.posting + d * 0.06)) / 0.15);
      _v.set(x, Y0 - 0.35 + y - fall * 14, z);
      _e.set(wob(t, 1 + i * 0.13, 0.05) + fall * 1.5, wob(t, 0.8 + i * 0.07, 0.08), fall * (i % 2 ? 1 : -1));
      _q.setFromEuler(_e); _s.setScalar(Math.max(0.0001, a * (1 + flash * 0.08)));
      _m.compose(_v, _q, _s); wallBody.setMatrixAt(i, _m);
      _v.z += 0.185 * a; _m.compose(_v, _q, _s); wallFace.setMatrixAt(i, _m);
    });
    wallBody.instanceMatrix.needsUpdate = wallFace.instanceMatrix.needsUpdate = true;
  }
}

// =====================================================================================================
// 3. the paper ball, the TASK block that cracks, the five glossy prompt blocks
// =====================================================================================================
const ballGeo = new THREE.IcosahedronGeometry(1, 3); { const r = rng(5), pos = ballGeo.attributes.position; for (let i = 0; i < pos.count; i++) { _v.fromBufferAttribute(pos, i); _v.multiplyScalar(0.78 + r() * 0.34); pos.setXYZ(i, _v.x, _v.y, _v.z); } ballGeo.computeVertexNormals(); }
const ball = new THREE.Mesh(ballGeo, new THREE.MeshStandardMaterial({ color: 0xe4e4e8, roughness: 0.85, flatShading: true }));
scene.add(ball);
function poseBall(t) {
  const t0 = C.mistake + 0.1;
  ball.visible = t > t0 && t < t0 + 0.9;
  if (!ball.visible) return;
  const k = clamp((t - t0) / 0.8), grow = p(t, t0, 0.12, "back");
  ball.position.set(k * 6.5, Y0 - 0.35 + 3.2 * k - 9 * k * k + 0.3, k * 2);
  ball.rotation.set(k * 9, k * 7, 0);
  ball.scale.setScalar(0.85 * grow);
}
const task = new THREE.Group(); scene.add(task);
const taskMat = glossy(0xb9bbc2, { r: 0.4, cc: 0.5 });
task.add(new THREE.Mesh(slabGeo(4.8, 2.3, 1.0, 0.28), taskMat));
const taskFace = face(4.5, 2.05, 900, 410); taskFace.mesh.position.z = 0.505; task.add(taskFace.mesh);
(function () {
  const g = taskFace.ctx; g.font = "700 30px Mono"; g.fillStyle = "#6b6e76"; g.textAlign = "center"; g.fillText("WHAT MOST PEOPLE GIVE IT", 450, 110);
  g.font = "800 170px Inter"; g.fillStyle = "#3d4047"; g.fillText("TASK", 450, 280); g.font = "600 40px Inter"; g.fillStyle = "#6b6e76"; g.fillText("\"write me a reel script\"", 450, 360);
  taskFace.tex.needsUpdate = true;
})();

// five blocks
const LABELS = [["ROLE", "Short-form scriptwriter"], ["AUDIENCE", "Creators under 10K"], ["HOOK RULE", "Stop the scroll, no greetings"], ["FORMAT", "28 s: problem, mistake, fix, CTA"], ["TONE", "Like a friend, not a teacher"]];
const BH = 0.84, GAP = 0.98;
const blockGeo = slabGeo(5.0, BH, 0.8, 0.24, 0.1);
const blocks = LABELS.map(([lab, sub], i) => {
  const g = new THREE.Group();
  const mat = glossy(COL.ink, { r: 0.25, cc: 1, ccr: 0.06, x: { emissive: new THREE.Color(COL.lime), emissiveIntensity: 0 } });
  const body = new THREE.Mesh(blockGeo, mat);
  const f = face(4.8, BH - 0.08, 1200, 190); f.mesh.position.z = 0.405;
  const draw = () => { const c = f.ctx; c.clearRect(0, 0, 1200, 190); c.fillStyle = "#101111"; rr(c, 0, 0, 1200, 190, 30); c.fill();
  c.fillStyle = "#ccfb79"; rr(c, 26, 38, 114, 114, 30); c.fill();
  c.fillStyle = "#101111"; c.font = "800 70px Inter"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(String(i + 1), 83, 98);
  c.textAlign = "left"; c.fillStyle = "#ffffff"; c.font = "800 66px Inter"; c.fillText(lab, 176, 76);
  c.fillStyle = "#9aa09a"; c.font = "600 38px Inter"; c.fillText(sub, 178, 140);
  f.tex.needsUpdate = true; }; draw();
  // a lime edge that lights up
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(5.16, BH + 0.16), new THREE.MeshBasicMaterial({ color: COL.lime, transparent: true, opacity: 0, depthWrite: false, toneMapped: false }));
  glow.position.z = -0.45;
  g.add(glow, body, f.mesh);
  scene.add(g);
  return { g, mat, glow, draw };
});
// ghost slots (shown on "five things")
const slotMat = new THREE.MeshBasicMaterial({ color: 0x101111, transparent: true, opacity: 0.0, depthWrite: false });
const slots = LABELS.map(() => { const m = new THREE.Mesh(new THREE.PlaneGeometry(5.0, BH), slotMat); scene.add(m); return m; });
const slotEdges = LABELS.map(() => { const l = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(5.0, BH)), new THREE.LineDashedMaterial({ color: 0x101111, dashSize: 0.12, gapSize: 0.08, transparent: true, opacity: 0 })); l.computeLineDistances(); scene.add(l); return l; });
const stack = new THREE.Group(); scene.add(stack);   // pivot for the orbit
function slotY(i) { return Y0 + 1.75 - i * GAP; }
function poseTaskAndBlocks(t) {
  // TASK block: drops in, shakes on "not", splits on "direction"
  const tv = t > C.task - 0.1 && t < C.direction + 0.05;
  task.visible = tv;
  if (tv) {
    const d = p(t, C.task, 0.55, "el");
    const sh = t > C.not - 0.1 && t < C.direction ? wob(t, 90, 0.08) : 0;
    task.position.set(sh, Y0 - 0.3 + (1 - d) * 7, 0);
    task.rotation.set(-0.12, -0.3 + wob(t, 1.0, 0.06) + p(t, C.task, 1.5) * 0.35, sh * 0.5);
  }
  // shards: the TASK block split into five slices that fly apart
  const ts = t - C.direction;
  const orbit = t > C.r4 ? lerp(-0.32, 0.28, p(t, C.r4, C.r5 - C.r4, "io")) : 0;
  const r5k = p(t, C.r5, 0.6, "io");
  for (let i = 0; i < 5; i++) {
    const b = blocks[i];
    const tin = C.items[i];                         // the spoken word of this block
    let vis = false, x = 0, y = slotY(i), z = 0, rx = 0, ry = 0, rz = 0, s = 1;
    if (ts > 0 && ts < 0.75) {                      // shard phase
      vis = true; const k = E.out(clamp(ts / 0.75));
      const sgn = i % 2 ? 1 : -1;
      x = sgn * k * 7.5; y = Y0 - 0.3 + 0.9 - i * 0.45 + (k * k) * -1.5; z = k * 1.5; rz = sgn * k * 0.8; ry = sgn * k * 1.2; s = lerp(0.95, 0.7, k);
      b.mat.color.set(0xb9bbc2);
    } else if (t > tin - 0.35) {                    // block slams into its slot on its word
      vis = true; const k = p(t, tin - 0.35, 0.38, "out"); const sgn = i % 2 ? 1 : -1;
      x = sgn * (1 - k) * 8; z = (1 - k) * 3; ry = sgn * (1 - k) * -1.1; rz = sgn * (1 - k) * 0.3;
      const land = Math.max(0, 1 - Math.abs(t - tin - 0.02) / 0.12);
      s = 1 + land * 0.06;
      b.mat.color.set(COL.ink);
      // r5: lift the blocks the voice names
      const lift = Math.max(...(C.hi[i] || []).map((th) => p(t, th, 0.25, "back") * (1 - p(t, th + 0.9, 0.3, "io"))), 0);
      z += lift * 0.9; x += lift * -0.25 * (i % 2 ? -1 : 1);
      b.mat.emissiveIntensity = lift * 0.5 + Math.max(0, 1 - Math.abs(t - (C.knows + i * 0.08)) / 0.18) * 0.5;
      b.glow.material.opacity = Math.min(1, lift + land * 0.8);
      y += wob(t, 1.5, 0.03, i);
      // end of r5: the stack whips away up into the CTA
      const away = p(t, C.r6 - 0.35 + i * 0.03, 0.35, "in");
      y += away * 9; s *= 1 - away * 0.5;
    }
    b.g.visible = vis;
    if (!vis) continue;
    b.g.position.set(x, y, z);
    b.g.rotation.set(rx - 0.06 * r5k, ry, rz);
    b.g.scale.setScalar(s);
    // orbit the whole stack in r4/r5 by rotating positions about the y axis
    if (t > C.r4 && ts >= 0.75) {
      const ca = Math.cos(orbit), sa = Math.sin(orbit), px = b.g.position.x, pz = b.g.position.z;
      b.g.position.x = px * ca + pz * sa; b.g.position.z = -px * sa + pz * ca; b.g.rotation.y += orbit;
    }
  }
  // ghost slots
  const so = p(t, C.five, 0.3, "out") * (1 - p(t, C.r5, 0.4));
  slots.forEach((m, i) => {
    const filled = t > C.items[i] - 0.05;
    m.visible = slotEdges[i].visible = so > 0.01 && !filled;
    const ca = Math.cos(orbit), sa = Math.sin(orbit);
    m.position.set(0, slotY(i), -0.4); m.rotation.set(0, orbit, 0);
    slotEdges[i].position.copy(m.position); slotEdges[i].rotation.copy(m.rotation);
    m.material.opacity = 0.06 * so; slotEdges[i].material.opacity = 0.45 * so * (0.7 + 0.3 * Math.sin(t * 8 + i));
    void ca; void sa;
  });
}

// =====================================================================================================
// 4. CTA: a comment bubble typing PROMPT, the DM with the PDF, nine more prompt cards fanning out
// =====================================================================================================
const cta = new THREE.Group(); scene.add(cta);
const bub = new THREE.Group();
{
  const s = rrShape(5.2, 1.3, 0.62);
  const tail = new THREE.Shape(); tail.moveTo(-1.9, -0.5); tail.lineTo(-2.35, -1.05); tail.lineTo(-1.3, -0.62);
  const g1 = new THREE.ExtrudeGeometry([s, tail], { depth: 0.2, bevelEnabled: true, bevelThickness: 0.12, bevelSize: 0.1, bevelSegments: 5, curveSegments: 14 });
  g1.translate(0, 0, -0.1);
  bub.add(new THREE.Mesh(g1, glossy(0xffffff, { r: 0.28 })));
}
const bubFace = face(5.0, 1.12, 1000, 224); bubFace.mesh.position.z = 0.235; bub.add(bubFace.mesh);
cta.add(bub);
const KW = "PROMPT";
function drawBubble(t) {
  const n = clamp(Math.floor((t - C.promptW) / 0.065) + 1, 0, KW.length);
  const posted = t > C.post;
  const k = `${n}|${posted}|${Math.floor(t * 4) % 2}`;
  if (bubFace.key === k) return; bubFace.key = k;
  const g = bubFace.ctx; g.clearRect(0, 0, 1000, 224);
  g.fillStyle = "#101111"; g.beginPath(); g.arc(82, 112, 46, 0, 7); g.fill();
  g.fillStyle = "#ccfb79"; g.beginPath(); g.moveTo(90, 74); g.lineTo(64, 120); g.lineTo(84, 120); g.lineTo(76, 152); g.lineTo(104, 102); g.lineTo(84, 102); g.closePath(); g.fill();
  g.font = "800 92px Inter"; g.fillStyle = "#101111"; g.textBaseline = "middle"; const s = KW.slice(0, n); g.fillText(s, 158, 118);
  if (!posted && Math.floor(t * 4) % 2 === 0) { g.fillStyle = "#fd0b68"; g.fillRect(166 + g.measureText(s).width, 70, 7, 92); }
  g.font = "800 46px Inter"; g.fillStyle = posted ? "#ffffff" : "#fd0b68";
  if (posted) { rr(g, 790, 74, 170, 78, 39); g.fillStyle = "#fd0b68"; g.fill(); g.fillStyle = "#fff"; }
  g.textAlign = "center"; g.fillText("Post", 875, 116); g.textAlign = "left";
  bubFace.tex.needsUpdate = true;
}
// the DM card with the PDF cover
const dm = new THREE.Group();
dm.add(new THREE.Mesh(slabGeo(4.6, 4.3, 0.36, 0.42), glossy(0xffffff, { r: 0.3 })));
const dmFace = face(4.36, 4.06, 872, 812); dmFace.mesh.position.z = 0.185; dm.add(dmFace.mesh);
function drawDM() {
  const g = dmFace.ctx; g.clearRect(0, 0, 872, 812);
  g.fillStyle = "#101111"; g.beginPath(); g.arc(60, 60, 30, 0, 7); g.fill();
  g.fillStyle = "#ccfb79"; g.beginPath(); g.moveTo(65, 38); g.lineTo(48, 66); g.lineTo(61, 66); g.lineTo(55, 86); g.lineTo(73, 55); g.lineTo(60, 55); g.closePath(); g.fill();
  g.font = "800 34px Inter"; g.fillStyle = "#101111"; g.textBaseline = "middle"; g.fillText("Creators 100X", 104, 50);
  g.font = "600 26px Inter"; g.fillStyle = "#7a7a7a"; g.fillText("sent you a file", 104, 84);
  // the PDF cover (brand: off-white, lime + pink glows, black type, one pink word)
  const x = 40, y = 128, w = 792, h = 640;
  g.save(); rr(g, x, y, w, h, 34); g.clip();
  g.fillStyle = "#fdf4f4"; g.fillRect(x, y, w, h);
  let gr = g.createRadialGradient(x, y, 0, x, y, 520); gr.addColorStop(0, "rgba(206,251,143,.95)"); gr.addColorStop(1, "rgba(206,251,143,0)"); g.fillStyle = gr; g.fillRect(x, y, w, h);
  gr = g.createRadialGradient(x + w, y + h, 0, x + w, y + h, 560); gr.addColorStop(0, "rgba(254,112,179,.85)"); gr.addColorStop(1, "rgba(254,112,179,0)"); g.fillStyle = gr; g.fillRect(x, y, w, h);
  g.fillStyle = "#101111"; rr(g, x + 50, y + 60, 250, 56, 28); g.fill(); g.fillStyle = "#ccfb79"; g.font = "700 26px Mono"; g.fillText("FREE PDF", x + 92, y + 89);
  g.fillStyle = "#101111"; g.font = "800 96px Inter"; g.fillText("10 AI prompts", x + 48, y + 210);
  g.fillText("that write", x + 48, y + 310); g.fillStyle = "#fd0b68"; g.fillText("your reels", x + 48, y + 410);
  g.fillStyle = "#101111"; g.font = "600 34px Inter"; g.fillText("Copy, fill the blanks, paste into ChatGPT.", x + 50, y + 500);
  g.fillStyle = "#101111"; rr(g, x + 50, y + 550, 300, 50, 25); g.fill(); g.fillStyle = "#ffffff"; g.font = "700 26px Inter"; g.fillText("#1  The 5-part prompt", x + 72, y + 576);
  g.restore();
  dmFace.tex.needsUpdate = true;
}
cta.add(dm);
const minis = Array.from({ length: 9 }, (_, i) => {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(slabGeo(1.5, 1.95, 0.18, 0.18, 0.05), glossy(i % 3 === 1 ? COL.lime : i % 3 === 2 ? 0xffc2dc : 0xffffff, { r: 0.3 })));
  const f = face(1.36, 1.8, 272, 360); f.mesh.position.z = 0.095;
  g.userData.draw = () => { const c = f.ctx; c.clearRect(0, 0, 272, 360); c.fillStyle = "#101111"; c.font = "800 96px Inter"; c.textAlign = "center"; c.fillText("#" + (i + 2), 136, 150);
  c.fillStyle = "rgba(16,17,17,.25)"; for (let k = 0; k < 4; k++) { rr(c, 40, 210 + k * 34, k === 3 ? 120 : 192, 16, 8); c.fill(); }
  f.tex.needsUpdate = true; }; g.userData.draw(); g.add(f.mesh); cta.add(g); return g;
});
function poseCTA(t) {
  const vis = t > C.r6 - 0.3;
  cta.visible = vis;
  if (!vis) return;
  drawBubble(t);
  const bi = p(t, C.r6 - 0.25, 0.5, "back"), bo = p(t, C.post + 0.12, 0.45, "in");
  bub.position.set(0, Y0 + lerp(-3, 0.4, bi) + bo * 4.2, bo * -1);
  bub.rotation.set(lerp(-1.2, -0.05, bi) + wob(t, 1.2, 0.04), wob(t, 0.9, 0.08), 0);
  bub.scale.setScalar((1 + 0.07 * Math.sin(Math.PI * clamp((t - C.post) / 0.2))) * (1 - bo * 0.55));
  bub.visible = bo < 0.999;
  const di = p(t, C.dmIn, 0.6, "back");
  dm.visible = t > C.dmIn - 0.02;
  dm.position.set(lerp(-6, 0, di), Y0 - 0.35 + wob(t, 1.3, 0.06), 0.4);
  dm.rotation.set(-0.05 + wob(t, 1.0, 0.03), lerp(0.9, -0.12, di) + p(t, C.dmIn, 3.2, "io") * 0.22, lerp(-0.25, 0, di));
  dm.scale.setScalar(lerp(0.6, 1, di));
  minis.forEach((m, i) => {
    const k = p(t, C.nine - 0.1 + i * 0.05, 0.5, "back");
    const a = lerp(-1.0, 1.0, i / 8);
    m.visible = k > 0.001;
    m.position.set(Math.sin(a) * 3.3 * k, Y0 - 0.35 + Math.cos(a) * 2.6 * k - 0.5, -0.9 - Math.abs(i - 4) * 0.05);
    m.rotation.set(0, -a * 0.25, -a * 0.55 * k + wob(t, 2 + i * 0.2, 0.03));
    m.scale.setScalar(Math.max(0.001, k * 0.92));
  });
}

// =====================================================================================================
// 5. the Creators 100X bolt tile: the brand character, bottom right, reacting
// =====================================================================================================
const bolt = new THREE.Group();
{
  const tile = new THREE.Mesh(slabGeo(1.25, 1.25, 0.42, 0.32, 0.1), glossy(COL.ink, { r: 0.22, ccr: 0.05 }));
  const bs = new THREE.Shape(); const P = [[0.08, 0.46], [-0.24, -0.03], [-0.02, -0.03], [-0.1, -0.46], [0.25, 0.08], [0.03, 0.08]];
  bs.moveTo(...P[0]); P.slice(1).forEach((q) => bs.lineTo(...q)); bs.closePath();
  const bg = new THREE.ExtrudeGeometry(bs, { depth: 0.12, bevelEnabled: true, bevelThickness: 0.04, bevelSize: 0.03, bevelSegments: 3 });
  const pos = bg.attributes.position, cols = [];
  for (let i = 0; i < pos.count; i++) { const yy = pos.getY(i); const c = new THREE.Color(yy > 0.02 ? 0xffffff : COL.lime); cols.push(c.r, c.g, c.b); }
  bg.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3));
  const bm = new THREE.Mesh(bg, new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.3, clearcoat: 1, emissive: 0x222222 }));
  bm.position.z = 0.2;
  bolt.add(tile, bm);
}
scene.add(bolt);
function poseBolt(t) {
  const inK = p(t, C.sw, 0.55, "back");
  bolt.visible = t > C.sw - 0.02;
  if (!bolt.visible) return;
  let hop = 0, spin = 0;
  for (const th of C.hops) { const k = clamp((t - th) / 0.42); hop += Math.sin(Math.PI * k) * 0.55 * (k > 0 && k < 1 ? 1 : 0); }
  for (const th of C.spins) spin += E.out(clamp((t - th) / 0.6)) * Math.PI * 2;
  bolt.position.set(2.25, -4.55 + hop + wob(t, 2.2, 0.06) + (1 - inK) * -2.5, 1.5);
  bolt.rotation.set(-0.1 + wob(t, 1.7, 0.08), -0.35 + wob(t, 1.3, 0.18) + spin + (1 - inK) * 3, wob(t, 1.9, 0.06));
  bolt.scale.setScalar(Math.max(0.001, inK) * (1 + 0.1 * Math.sin(Math.PI * clamp((t - C.sw) / 0.4))));
}

// =====================================================================================================
// camera: one move per beat (push-ins, the pull back for the wall, an orbit for the blocks, bumps on hits)
// =====================================================================================================
function poseCamera(t) {
  let z = kf(t, [[0, 21.5], [C.sw - 0.05, 19.8, "io"], [C.sw + 0.3, 22.5, "out"], [C.r2, 21.5, "io"], [C.wall - 0.05, 21, "io"], [C.wall + 1.6, 34, "io"],
    [C.r3 - 0.25, 36, "io"], [C.r3 + 0.35, 21.5, "io"], [C.r4, 21, "io"], [C.r5, 23.5, "io"], [C.r6 - 0.2, 22, "io"], [C.r6 + 0.4, 21.5, "out"], [C.end, 20.2, "io"]]);
  let x = kf(t, [[0, -0.4], [C.sw, 0.2, "io"], [C.r2, 0, "io"], [C.r4, 0.3, "io"], [C.r5, -0.3, "io"], [C.r6, 0, "io"], [C.end, 0.15, "io"]]);
  let y = kf(t, [[0, 0], [C.r4, 0, "io"], [C.r5, -0.15, "io"], [C.end, 0, "io"]]);
  // bumps on the hits
  for (const th of C.bumps) { const k = clamp((t - th) / 0.3); z -= Math.sin(Math.PI * k) * 0.9 * (k > 0 && k < 1 ? 1 : 0); }
  // glitch shake before the switch
  if (t > C.sw - 0.32 && t < C.sw + 0.1) { const r = rng(Math.floor(t * 30) + 3); x += (r() - 0.5) * 0.5; y += (r() - 0.5) * 0.4; }
  camera.position.set(x, y, z);
  camera.lookAt(x * 0.5, y + Y0 * 0.15, 0);
  camera.updateProjectionMatrix();
}

let ready = false;
function renderAt(t) {
  if (!ready) return;
  t = Math.max(0, t);
  poseCamera(t); poseChat(t); poseLazy(t); poseBall(t); poseTaskAndBlocks(t); poseCTA(t); poseBolt(t);
  renderer.render(scene, camera);
}
window.__render3 = renderAt;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));

(async () => {
  await Promise.all([document.fonts.load('800 60px Inter'), document.fonts.load('700 30px Inter'), document.fonts.load('600 30px Inter'), document.fonts.load('30px Mono')]);
  await document.fonts.ready;
  genFace.key = null; taskFace.key = null;
  // redraw the static faces now that the fonts are in
  (function () { const g = genFace.ctx; g.clearRect(0, 0, 940, 490); g.fillStyle = "#c5c7cd"; g.beginPath(); g.arc(64, 64, 26, 0, 7); g.fill();
    g.font = "700 30px Inter"; g.fillStyle = "#8e9199"; g.textBaseline = "middle"; g.fillText("ChatGPT", 104, 66);
    g.textBaseline = "alphabetic"; g.font = "700 50px Inter"; g.fillStyle = "#6b6e76"; wrap(g, GENERIC, 44, 170, 852, 66); genFace.tex.needsUpdate = true; })();
  (function () { const g = taskFace.ctx; g.clearRect(0, 0, 900, 410); g.textAlign = "center"; g.font = "700 30px Mono"; g.fillStyle = "#6b6e76"; g.fillText("WHAT MOST PEOPLE GIVE IT", 450, 110);
    g.font = "800 170px Inter"; g.fillStyle = "#3d4047"; g.fillText("TASK", 450, 280); g.font = "600 40px Inter"; g.fillStyle = "#6b6e76"; g.fillText("\"write me a reel script\"", 450, 360); taskFace.tex.needsUpdate = true; })();
  blocks.forEach((b) => b.draw()); minis.forEach((m) => m.userData.draw());
  drawDM();
  ready = true;
  renderer.compile(scene, camera);
  const tl = window.__timelines && window.__timelines.main;
  renderAt(tl ? tl.time() : window.__hfThreeTime || 0);
  window.__sceneReady && window.__sceneReady();
})();
