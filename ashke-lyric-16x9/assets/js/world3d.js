// The 3D layer of the Ashke lyric video, in the reference style: chunky 3D pixel icons (voxels with a dark outline in
// orange, cream, black and gold) that assemble from flying pixels, pop, spin, orbit in a ring, slide by in a row,
// drive, fly and explode; and big 3D serif words (Playfair Display italic) for the hero lines. Pure function of time
// t on HyperFrames' hf-seek. Schedules and icon maps come from window.AK_T (written by build/generate.py).
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";
import { TTFLoader } from "three/addons/loaders/TTFLoader.js";
import { Font } from "three/addons/loaders/FontLoader.js";

const T = window.AK_T;
const W = 1920, H = 1080;
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => cl((t - a) / (b - a));
const eOut = (x) => 1 - Math.pow(1 - x, 3);
const eIn = (x) => x * x * x;
const eBack = (x) => { const c1 = 2.0, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

const outEl = document.getElementById("gl3d"); outEl.width = W; outEl.height = H;
const out2d = outEl.getContext("2d");
const canvas = document.createElement("canvas"); canvas.width = W; canvas.height = H;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setClearColor(0x000000, 0);
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
const CAMZ = 40, FOV = 30;
const camera = new THREE.PerspectiveCamera(FOV, W / H, .1, 300);
camera.position.set(0, 0, CAMZ);
const K = 540 / (CAMZ * Math.tan(THREE.MathUtils.degToRad(FOV / 2)));    // screen px per world unit at z = 0
const px = (x, y) => new THREE.Vector3((x - 960) / K, (540 - y) / K, 0);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = .55;
scene.add(new THREE.HemisphereLight(0xfff4e6, 0x2a1a14, 1.3));
const key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(-6, 9, 14); scene.add(key);
const rim = new THREE.DirectionalLight(0xff8a50, 1.2); rim.position.set(8, -2, -6); scene.add(rim);

// ------------------------------------------------------------------ pixel icons as voxels
const vox = new RoundedBoxGeometry(1, 1, 1.4, 2, .1);
const voxMat = new THREE.MeshStandardMaterial({ roughness: .5, metalness: .05 });
const ICON = {};
for (const [name, ic] of Object.entries(T.iconMaps)) {
  const m = new THREE.InstancedMesh(vox, voxMat, ic.cells.length);
  ic.cells.forEach(([, , c], i) => m.setColorAt(i, new THREE.Color(c)));
  m.visible = false; m.frustumCulled = false; scene.add(m);
  ICON[name] = { mesh: m, ic };
}
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _s = new THREE.Vector3(), _p = new THREE.Vector3();
const _g = new THREE.Matrix4();

// place one icon: group transform (position, rotation, scale) plus per-voxel offsets (assemble / explode)
function drawIcon(name, pos, scale, rot, spread, explode, seed) {
  const I = ICON[name]; if (!I) return;
  const { mesh: m, ic } = I;
  m.visible = true;
  _e.set(rot.x, rot.y, rot.z); _q.setFromEuler(_e);
  _g.compose(pos, _q, _s.set(scale, scale, scale));
  ic.cells.forEach(([cx, cy], i) => {
    let x = cx - ic.w / 2 + .5, y = ic.h / 2 - cy - .5, z = 0, rs = 1, rx = 0, ry = 0;
    const amt = Math.max(spread, explode);
    if (amt > 0) {
      const a = hash(i + seed) * Math.PI * 2, b = (hash(i * 3 + seed) - .5) * 2;
      const d = (6 + 18 * hash(i * 7 + seed)) * amt;
      x += Math.cos(a) * d; y += Math.sin(a) * d * .8 - (explode > 0 ? 14 * explode * explode : 0); z += b * d;
      rx = amt * 8 * hash(i + 1); ry = amt * 6 * hash(i + 2);
      rs = 1 - .5 * amt;
    }
    _e.set(rx, ry, 0); _q.setFromEuler(_e);
    _m.compose(_p.set(x, y, z), _q, _s.set(rs, rs, rs));
    _m.premultiply(_g);
    m.setMatrixAt(i, _m);
  });
  m.instanceMatrix.needsUpdate = true;
}

function iconAt(it, t) {
  // it: {n, a, b, fx, x, y, s, t0, x2, y2, dur}
  const seed = it.a * 13.7;
  const local = t - it.a;
  const p = px(it.x, it.y), rot = new THREE.Vector3(0, 0, 0);
  let sc = it.s / K;
  let spread = 1 - eOut(lin(t, it.a, it.a + .38));          // pixels fly in
  spread = Math.max(spread, eIn(lin(t, it.b - .22, it.b)));   // and fly apart on the way out
  let explode = 0;
  const pop = eBack(lin(t, it.a, it.a + .45));
  rot.y = (1 - pop) * Math.PI * 1.5 + .45 * Math.sin(t * 1.4 + seed);
  rot.x = .12 * Math.sin(t * 1.1 + seed); rot.z = .05 * Math.sin(t * .9 + seed);
  p.y += .25 * Math.sin(t * 2.2 + seed);
  if (it.fx === "spin") rot.y = local * 3.2;
  if (it.fx === "roll") { rot.y = .3 * Math.sin(t * 1.2); rot.z = -local * 4; }
  if (it.fx === "drive" || it.fx === "slide" || it.fx === "fly") {
    const k = it.fx === "slide" ? lin(t, it.a, it.b) : eOut(lin(t, it.a, it.a + (it.dur || .6)));
    p.lerp(px(it.x2, it.y2), k);
    if (it.fx === "fly") { rot.z = .25 * Math.sin(t * 9); p.y += .5 * Math.sin(t * 9); rot.y = .3; }
    else rot.y = .15 * Math.sin(t * 2 + seed);
  }
  if (it.fx === "away" && t >= it.t0) { const k = eIn(lin(t, it.t0, it.t0 + .35)); p.x += 30 * k; rot.z = -.6 * k; }
  if (it.fx === "scatter" && t >= it.t0) explode = eOut(lin(t, it.t0, it.t0 + .9));
  const kb = T.beats.find((b) => t >= b && t < b + .2);
  if (kb !== undefined) sc *= 1 + .08 * Math.exp(-(t - kb) * 18);
  drawIcon(it.n, p, sc * Math.max(.001, pop), rot, spread, explode, seed);
}

function ringAt(r, t) {
  // a ring of icons orbiting a centre, tilted towards the camera; it assembles, spins, and spins up before leaving
  const c = px(r.x, r.y), R = r.r / K;
  const local = t - r.a, n = r.names.length;
  const spin = local * (r.speed || .6) + (r.fast && t > r.fast ? (t - r.fast) * 7 : 0);
  r.names.forEach((name, i) => {
    const a = i / n * Math.PI * 2 + spin;
    const k = eBack(lin(t, r.a + i * .03, r.a + i * .03 + .4));
    const out = eIn(lin(t, r.b - .25, r.b));
    const pos = new THREE.Vector3(c.x + Math.cos(a) * R * (1 + out * 1.5), c.y + Math.sin(a) * R * .62 * (1 + out * 1.5), Math.sin(a) * 2);
    drawIcon(name, pos, (r.s / K) * Math.max(.001, k), new THREE.Vector3(.1, .5 * Math.sin(t + i), 0),
      1 - eOut(lin(t, r.a + i * .03, r.a + i * .03 + .4)), out, i * 9 + r.a);
  });
}

// ------------------------------------------------------------------ 3D words
const WORD = {};
const faceMat = { cream: new THREE.MeshPhysicalMaterial({ color: 0xf3ede2, roughness: .32, clearcoat: .8, clearcoatRoughness: .2 }),
  orange: new THREE.MeshPhysicalMaterial({ color: 0xff5a1f, roughness: .3, clearcoat: .8 }),
  red: new THREE.MeshPhysicalMaterial({ color: 0xe2332d, roughness: .35, clearcoat: .6, emissive: 0x5a0808, emissiveIntensity: .6 }) };
const sideMat = { cream: new THREE.MeshStandardMaterial({ color: 0xb9ad98, roughness: .5 }), orange: new THREE.MeshStandardMaterial({ color: 0x9a3410, roughness: .5 }),
  red: new THREE.MeshStandardMaterial({ color: 0x6a0f0f, roughness: .5 }) };

async function buildWords() {
  const data = await new TTFLoader().loadAsync("assets/fonts/PlayfairDisplay/PlayfairDisplay-900Italic.ttf");
  const font = new Font(data);
  for (const w of T.words3d) {
    const key = w.text + w.color;
    if (WORD[key]) continue;
    const geo = new TextGeometry(w.text, { font, size: 4.2, depth: 1.1, curveSegments: 10, bevelEnabled: true, bevelThickness: .12, bevelSize: .08, bevelSegments: 4 });
    geo.computeBoundingBox(); const bb = geo.boundingBox;
    geo.translate(-(bb.max.x + bb.min.x) / 2, -(bb.max.y + bb.min.y) / 2, -(bb.max.z + bb.min.z) / 2);
    const mesh = new THREE.Mesh(geo, [faceMat[w.color], sideMat[w.color]]);
    mesh.visible = false; scene.add(mesh);
    // two ghost copies smear behind the word while it flies (motion blur)
    const ghosts = [.35, .18].map((o) => {
      const gm = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: faceMat[w.color].color, transparent: true, opacity: o, depthWrite: false }));
      gm.visible = false; scene.add(gm); return gm;
    });
    WORD[key] = { mesh, ghosts };
  }
}

function wordAt(w, t) {
  if (!WORD[w.text + w.color]) return;   // the font is still loading
  const { mesh, ghosts } = WORD[w.text + w.color];
  const zAt = (tt) => -60 * (1 - eOut(lin(tt, w.a, w.a + .45))) + 50 * eIn(lin(tt, w.b - .2, w.b));
  const k = eOut(lin(t, w.a, w.a + .45)), out = eIn(lin(t, w.b - .2, w.b));
  const p = px(w.x, w.y), sc = w.size || 1;
  mesh.visible = true;
  mesh.position.set(p.x, p.y, zAt(t));
  mesh.rotation.set(.35 * (1 - k) + .06 * Math.sin(t * 1.3), -.7 * (1 - k) + .18 * Math.sin(t * .9), -.04);
  mesh.scale.setScalar(sc);
  if (w.fx === "glitch") {
    const f = Math.floor(t * 24);
    if (hash(f) < .35) { mesh.position.x += (hash(f + 1) - .5) * 2.4; mesh.scale.x = sc * (1 + (hash(f + 2) - .5) * .3); }
  }
  ghosts.forEach((g, i) => {
    const lag = (i + 1) * .045;
    g.visible = k < .98 || out > 0;
    g.position.set(p.x, p.y, zAt(t - lag));
    g.rotation.copy(mesh.rotation); g.scale.copy(mesh.scale);
  });
}

function renderAt(t) {
  for (const k in ICON) ICON[k].mesh.visible = false;
  for (const k in WORD) { WORD[k].mesh.visible = false; WORD[k].ghosts.forEach((g) => (g.visible = false)); }
  camera.position.set(Math.sin(t * .5) * .3, Math.cos(t * .4) * .2, CAMZ);
  for (const b of T.beats) if (t >= b && t < b + .25) camera.position.z -= 1.2 * Math.exp(-(t - b) * 14);
  camera.lookAt(0, 0, 0);
  for (const it of T.icons) if (t >= it.a && t < it.b) iconAt(it, t);
  for (const r of T.rings) if (t >= r.a && t < r.b) ringAt(r, t);
  for (const w of T.words3d) if (t >= w.a && t < w.b) wordAt(w, t);
  renderer.render(scene, camera);
  out2d.clearRect(0, 0, W, H);
  out2d.drawImage(canvas, 0, 0);
}

const ready = (async () => {
  await buildWords();
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["akworld"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
