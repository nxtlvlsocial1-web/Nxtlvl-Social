// NXTLVLSOCIAL.AI "5 free Claude Code plugins" v2 (owner: "make it 3D, more motion graphics"). The stage is a pure function
// of time t (rendered on HyperFrames' hf-seek). Data from window.PL (build/generate.py): beat times, the page sequence
// (our own captures, plan/targets.json boxes) and label ids. Layout, all centred: headline band (HTML, y 320-480), the 3D
// browser window (~y 520-1220), the desk props in front of it (~y 1180-1390), captions (HTML, y 1440).
//   window  a white 3D slab with a bar, three dots and the real URL; the page inside zooms onto the proof line, a violet
//           selection frame with handles lands on it; between plugins the window flips over to the next page
//   props   hook: a gold star on a pedestal | Ponytail: a code bar and a coin stack shrink | Unslop: purple "slop" blobs
//           snap into clean tiles | Elephant-Goldfish: three reviewer orbs scan a plan | Agent Reach: a globe with three
//           platform tiles | Setup: a codebase of file cubes swept by a scanner, three tiles rise | share: a carousel of
//           all five pages | CTA: the comet-star mark
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const W = 1080, H = 1920, FY = -0.78;   // FY: the floor / desk height (keeps the desk above the captions)
const D = window.PL, T = D.T;
const INK = 0x140a2e, VIOLET = 0x6516c7, ORCHID = 0xa75bfc, GOLD = 0xffc23d, PAPER = 0xf4f2f8, GREEN = 0x22b35e;
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene(); scene.background = new THREE.Color(PAPER); scene.fog = new THREE.Fog(PAPER, 14, 30);
const camera = new THREE.PerspectiveCamera(30, W / H, .1, 100);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture; scene.environmentIntensity = .9;
scene.add(new THREE.HemisphereLight(0xffffff, 0xd9d0ee, 1.0));
const key = new THREE.DirectionalLight(0xffffff, 1.4); key.position.set(-3, 6, 7); scene.add(key);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const easeIO = (x) => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;
const rnd = (i, k = 1) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };
const life = (t, a, b) => easeIO(win(t, a - .05, a + .4)) * (1 - easeIO(win(t, b - .3, b)));
const $ = (id) => document.getElementById(id);
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const v3 = new THREE.Vector3();
const S = (g, s) => g.scale.setScalar(Math.max(.001, s));
function project(obj, local, el, a = null, s = 1) {
  if (!el) return;
  v3.copy(local); if (obj) obj.localToWorld(v3); v3.project(camera);
  el.style.transform = `translate(${(v3.x * .5 + .5) * W}px, ${(-v3.y * .5 + .5) * H}px) translate(-50%, -50%) scale(${Math.max(.001, s)})`;
  if (a !== null) el.style.opacity = clamp(a);
}
function keyed(t, keys, d = .6) {
  let p = keys[0][1].clone();
  for (let k = 1; k < keys.length; k++) { const u = easeIO(win(t, keys[k][0], keys[k][0] + d)); if (u <= 0) break; p.lerp(keys[k][1], u); }
  return p;
}
const plastic = (c, r = .35) => new THREE.MeshPhysicalMaterial({ color: c, roughness: r, clearcoat: .8, clearcoatRoughness: .2 });
function textTex(txt, { w = 512, h = 128, bg = "#ffffff", fg = "#140a2e", font = "700 64px Inter", radius = 28 } = {}) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  if (bg) { g.fillStyle = bg; g.beginPath(); g.roundRect(0, 0, w, h, radius); g.fill(); }
  g.fillStyle = fg; g.font = font; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(txt, w / 2, h / 2 + 4);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8; return tx;
}
function drawTex(fn, w = 128, h = 128) { const c = document.createElement("canvas"); c.width = w; c.height = h; fn(c.getContext("2d"), w, h);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; return tx; }
const checkTex = (bg) => drawTex((g, w, h) => { g.fillStyle = bg; g.beginPath(); g.roundRect(0, 0, w, h, 30); g.fill();
  g.strokeStyle = "#fff"; g.lineWidth = 16; g.lineCap = g.lineJoin = "round"; g.beginPath(); g.moveTo(30, 66); g.lineTo(54, 90); g.lineTo(98, 40); g.stroke(); });
const faceTex = (i) => drawTex((g, w, h) => { g.fillStyle = "#fff"; g.beginPath(); g.arc(44, 52, 9, 0, 7); g.arc(84, 52, 9, 0, 7); g.fill();
  g.strokeStyle = "#fff"; g.lineWidth = 9; g.lineCap = "round"; g.beginPath(); i % 2 ? g.arc(64, 70, 26, .15 * Math.PI, .85 * Math.PI) : g.arc(64, 98, 22, 1.2 * Math.PI, 1.8 * Math.PI); g.stroke(); });
function checkTile(w) { const g = new THREE.Group(); g.add(new THREE.Mesh(new RoundedBoxGeometry(w, w, .06, 4, .04), plastic(GREEN, .3)));
  const f = new THREE.Mesh(new THREE.PlaneGeometry(w * .92, w * .92), new THREE.MeshBasicMaterial({ map: checkTex("#22b35e"), transparent: true, toneMapped: false })); f.position.z = .035; g.add(f); return g; }
const TEXTS = [];   // [mesh, txt, opts]: faces re-drawn after the fonts load
function tile(txt, w, h, opts) {  // a rounded slab with a text face
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new RoundedBoxGeometry(w, h, .08, 4, .05), plastic(opts && opts.slab || 0xffffff, .3)));
  const f = new THREE.Mesh(new THREE.PlaneGeometry(w * .96, h * .9), new THREE.MeshBasicMaterial({ map: textTex(txt, opts), transparent: true, toneMapped: false }));
  f.position.z = .045; g.add(f); TEXTS.push([f, txt, opts]); return g;
}

// ---------------------------------------------------------------- the floor: a grid that recedes, and soft contact shadows
const gridTex = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 512; const g = c.getContext("2d");
  g.fillStyle = "#f4f2f8"; g.fillRect(0, 0, 512, 512);
  g.strokeStyle = "rgba(101,22,199,.16)"; g.lineWidth = 3; g.strokeRect(0, 0, 512, 512);
  g.strokeStyle = "rgba(101,22,199,.07)"; g.lineWidth = 2; for (let i = 128; i < 512; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.moveTo(0, i); g.lineTo(512, i); g.stroke(); }
  const tx = new THREE.CanvasTexture(c); tx.wrapS = tx.wrapT = THREE.RepeatWrapping; tx.repeat.set(12, 12); tx.anisotropy = 8; tx.colorSpace = THREE.SRGBColorSpace; return tx;
})();
const floor = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshBasicMaterial({ map: gridTex, toneMapped: false }));
floor.rotation.x = -Math.PI / 2; floor.position.y = FY; scene.add(floor);
const shadowTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d");
  const r = g.createRadialGradient(128, 128, 10, 128, 128, 128); r.addColorStop(0, "rgba(40,20,90,.35)"); r.addColorStop(1, "rgba(40,20,90,0)");
  g.fillStyle = r; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c); })();
function shadow(w, d) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; m.position.y = FY + .005; scene.add(m); return m; }

// ---------------------------------------------------------------- the browser window
const WW = 2.6, WH = 2.12, BAR = .17, VWU = WW - .08, VHU = WH - BAR - .08;
const winG = new THREE.Group(); scene.add(winG);
const winIn = new THREE.Group(); winG.add(winIn);
winIn.add(new THREE.Mesh(new RoundedBoxGeometry(WW, WH, .1, 5, .07), plastic(0xffffff, .25)));
{ const bar = new THREE.Mesh(new THREE.PlaneGeometry(WW - .02, BAR), new THREE.MeshBasicMaterial({ color: 0xefecf5, toneMapped: false })); bar.position.set(0, WH / 2 - BAR / 2 - .01, .052); winIn.add(bar);
  [0xff5f57, 0xfebc2e, 0x28c840].forEach((c, k) => { const d = new THREE.Mesh(new THREE.CircleGeometry(.028, 20), new THREE.MeshBasicMaterial({ color: c, toneMapped: false })); d.position.set(-WW / 2 + .1 + k * .085, WH / 2 - BAR / 2 - .01, .055); winIn.add(d); }); }
const urlMesh = new THREE.Mesh(new THREE.PlaneGeometry(1.9, .115), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false })); urlMesh.position.set(.18, WH / 2 - BAR / 2 - .01, .056); winIn.add(urlMesh);
const urlTex = {}; const makeUrls = () => { for (const s of D.seq) urlTex[s.url] = textTex(s.url, { w: 1200, h: 72, bg: "#ffffff", fg: "#5b5470", font: "600 38px Inter", radius: 18 }); }; makeUrls();
const scrY = WH / 2 - BAR - .04 - VHU / 2;
const screens = [0, 1].map((k) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(VWU, VHU), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false }));
  m.position.set(0, scrY, .053 + k * .001); winIn.add(m); return m; });
const winShadow = shadow(3.6, 1.4);
// the selection frame (violet edges + handles) on the page
const frame = new THREE.Group(); frame.position.z = .056; winIn.add(frame);
const fM = new THREE.MeshBasicMaterial({ color: VIOLET, toneMapped: false, transparent: true });
const fEdges = [0, 1, 2, 3].map(() => { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), fM); frame.add(m); return m; });
const fHandles = [0, 1, 2, 3].map(() => { const g = new THREE.Group(); const o = new THREE.Mesh(new THREE.PlaneGeometry(.06, .06), fM); const i = new THREE.Mesh(new THREE.PlaneGeometry(.036, .036), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, transparent: true })); i.position.z = .001; g.add(o, i); frame.add(g); return g; });
const fDim = new THREE.Mesh(new THREE.PlaneGeometry(VWU, VHU), new THREE.MeshBasicMaterial({ color: INK, transparent: true, opacity: 0, toneMapped: false })); fDim.position.set(0, scrY, .0545); winIn.add(fDim);
const tex = [], caroTex = [];   // filled on load (the carousel gets its own copies: different crops)
function crop(s, u) {  // the page region on screen: from the opening view to the zoom on the box (image pixels)
  const ar = VWU / VHU, Wd = s.w, Hd = s.h;
  const c0 = { w: Wd, h: Wd / ar, x: 0, y: 0 };
  if (!s.box) { c0.y = (Hd - c0.h) * .3 * u; return c0; }
  const b = s.box, cw = clamp(Math.max(b.w / .86, Wd / 2.1), 0, Wd / 1.05), ch = cw / ar;
  const cx = b.x + b.w / 2, cy = b.y + b.h / 2;
  const c1 = { w: cw, h: ch, x: clamp(cx - cw / 2, 0, Wd - cw), y: clamp(cy - ch / 2, 0, Hd - ch) };
  const a0 = { w: Wd * .98, h: Wd * .98 / ar }; a0.x = clamp(cx - a0.w / 2, 0, Wd - a0.w); a0.y = clamp(cy - a0.h / 2, 0, Hd - a0.h);
  const e = easeIO(u); return { w: lerp(a0.w, c1.w, e), h: lerp(a0.h, c1.h, e), x: lerp(a0.x, c1.x, e), y: lerp(a0.y, c1.y, e) };
}
function showPage(m, k, c, op) {
  const s = D.seq[k], tx = tex[k]; if (!tx) return;
  m.material.map = tx; m.material.opacity = op; m.visible = op > .01;
  tx.repeat.set(c.w / s.w, c.h / s.h); tx.offset.set(c.x / s.w, 1 - (c.y + c.h) / s.h); m.material.needsUpdate = true;
}

// ---------------------------------------------------------------- desk props
const props = new THREE.Group(); scene.add(props);
// hook: a gold star on a pedestal
const starShape = new THREE.Shape(); for (let k = 0; k < 10; k++) { const r = k % 2 ? .13 : .3, a = Math.PI / 2 + k * Math.PI / 5; k ? starShape.lineTo(Math.cos(a) * r, Math.sin(a) * r) : starShape.moveTo(Math.cos(a) * r, Math.sin(a) * r); }
const gStar = new THREE.Group(); props.add(gStar);
const starM = new THREE.Mesh(new THREE.ExtrudeGeometry(starShape, { depth: .08, bevelEnabled: true, bevelThickness: .03, bevelSize: .025, bevelSegments: 3 }), new THREE.MeshPhysicalMaterial({ color: GOLD, metalness: .85, roughness: .22, clearcoat: 1 }));
starM.geometry.center(); gStar.add(starM);
const ped = new THREE.Mesh(new THREE.CylinderGeometry(.32, .36, .14, 48), plastic(INK, .3)); gStar.add(ped);
const SPN = 60, sparks = new THREE.InstancedMesh(new THREE.ExtrudeGeometry(starShape, { depth: .02, bevelEnabled: false }), new THREE.MeshPhysicalMaterial({ color: GOLD, metalness: .7, roughness: .3 }), SPN); scene.add(sparks);
// Ponytail: a code bar (violet) and a coin stack
const gPony = new THREE.Group(); props.add(gPony);
const codeBar = new THREE.Mesh(new RoundedBoxGeometry(.42, 1, .42, 4, .05), plastic(VIOLET, .25)); codeBar.geometry.translate(0, .5, 0); codeBar.position.x = -.45; gPony.add(codeBar);
const codeLines = [...Array(6)].map((_, i) => { const l = new THREE.Mesh(new THREE.PlaneGeometry(.26 - rnd(i) * .1, .03), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false })); codeBar.add(l); return l; });
const CN = 10, coins = new THREE.InstancedMesh(new THREE.CylinderGeometry(.19, .19, .055, 40), new THREE.MeshPhysicalMaterial({ color: GOLD, metalness: .9, roughness: .25 }), CN); gPony.add(coins);
const tick = checkTile(.28); gPony.add(tick);
// Unslop: four glossy purple blobs with faces, then four clean tiles
const gUns = new THREE.Group(); props.add(gUns);
const blobM = new THREE.MeshPhysicalMaterial({ color: 0xa04dff, emissive: 0x5a17c9, emissiveIntensity: .45, roughness: .15, clearcoat: 1, iridescence: .7 });
const blobs = [0, 1, 2, 3].map((i) => { const g = new THREE.Group(); const b = new THREE.Mesh(new THREE.SphereGeometry(.17, 32, 20), blobM); g.add(b);
  const face = new THREE.Mesh(new THREE.PlaneGeometry(.2, .2), new THREE.MeshBasicMaterial({ map: faceTex(i), transparent: true, toneMapped: false })); face.position.z = .172; g.add(face);
  gUns.add(g); return g; });
const cleanT = ["Type", "Space", "Color", "Layout"].map((s) => { const g = tile(s, .52, .22, { w: 256, h: 108, bg: "#ffffff", fg: "#140a2e", font: "700 50px Inter", radius: 24 }); gUns.add(g); return g; });
// Elephant-Goldfish: a plan document and three reviewer orbs
const gEgm = new THREE.Group(); props.add(gEgm);
const doc = tile("PLAN", .8, .5, { w: 320, h: 200, bg: "#ffffff", fg: "#140a2e", font: "800 72px Inter", radius: 20 }); gEgm.add(doc);
const orbs = [0, 1, 2].map(() => { const g = new THREE.Group(); const o = new THREE.Mesh(new THREE.SphereGeometry(.1, 24, 16), plastic(0xffffff, .2)); g.add(o);
  const iris = new THREE.Mesh(new THREE.CircleGeometry(.05, 20), new THREE.MeshBasicMaterial({ color: VIOLET, toneMapped: false })); iris.position.z = .095; g.add(iris);
  const beam = new THREE.Mesh(new THREE.ConeGeometry(.12, .5, 24, 1, true), new THREE.MeshBasicMaterial({ color: ORCHID, transparent: true, opacity: .22, side: THREE.DoubleSide, depthWrite: false, toneMapped: false }));
  beam.rotation.x = Math.PI / 2; beam.position.z = .3; g.add(beam); g.userData.beam = beam; gEgm.add(g); return g; });
const docTicks = [0, 1, 2].map(() => { const g = checkTile(.14); doc.add(g); return g; });
// Agent Reach: a wireframe globe and three platform tiles (names as text, no logos)
const gReach = new THREE.Group(); props.add(gReach);
const globe = new THREE.Mesh(new THREE.SphereGeometry(.34, 20, 14), new THREE.MeshBasicMaterial({ color: VIOLET, wireframe: true, transparent: true, opacity: .55, toneMapped: false })); gReach.add(globe);
const globeCore = new THREE.Mesh(new THREE.SphereGeometry(.31, 32, 20), plastic(0xffffff, .3)); gReach.add(globeCore);
const plat = ["YouTube", "GitHub", "Reddit"].map((s) => { const g = tile(s, .5, .2, { w: 256, h: 100, bg: "#140a2e", fg: "#ffffff", font: "700 48px Inter", radius: 24, slab: INK }); gReach.add(g); return g; });
// Setup: a codebase of file cubes, a scanner plane, three recommendation tiles
const gSet = new THREE.Group(); props.add(gSet);
const FN = 24, files = new THREE.InstancedMesh(new RoundedBoxGeometry(.13, .17, .03, 2, .01), plastic(0xffffff, .35), FN); gSet.add(files);
const scanner = new THREE.Mesh(new THREE.PlaneGeometry(.06, .7), new THREE.MeshBasicMaterial({ color: ORCHID, transparent: true, opacity: .75, toneMapped: false, depthWrite: false })); gSet.add(scanner);
const recs = ["hooks", "skills", "MCP"].map((s) => { const g = tile(s, .42, .2, { w: 256, h: 120, bg: "#6516c7", fg: "#ffffff", font: "700 56px Inter", radius: 26, slab: VIOLET }); gSet.add(g); return g; });
// share: a carousel of the five pages
const caro = new THREE.Group(); scene.add(caro);
const caroCards = [0, 1, 2, 3, 4].map(() => { const g = new THREE.Group(); g.add(new THREE.Mesh(new RoundedBoxGeometry(1.1, .8, .05, 4, .04), plastic(0xffffff, .3)));
  const p = new THREE.Mesh(new THREE.PlaneGeometry(1.04, .74), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false })); p.position.z = .028; g.add(p); g.userData.p = p; caro.add(g); return g; });
// CTA: the comet-star mark on a dark tile
const markG = new THREE.Group(); scene.add(markG);
markG.add(new THREE.Mesh(new RoundedBoxGeometry(.9, .9, .16, 6, .16), plastic(INK, .25)));
const markFace = new THREE.Mesh(new THREE.PlaneGeometry(.66, .66), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false })); markFace.position.z = .085; markG.add(markFace);

const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3();
const DESK = V(0, FY, .95);

// ---------------------------------------------------------------- per frame
function renderAt(t) {
  const B = [0, T.b1, T.b2, T.b3, T.b4, T.b5, T.b6, T.b7, 999];
  const beat = B.findIndex((b, i) => t >= b && t < B[i + 1]);

  // camera: a slow drift, a push-in while a frame is on, a pull-back for the carousel
  let k = 0; for (let i = 0; i < D.seq.length; i++) if (t >= D.seq[i].t0) k = i;
  const s = D.seq[k], zoomU = s.box ? (k === 0 ? 1 : win(t, s.t0 + .4, s.t0 + 1.15)) : 0;
  const push = s.box ? easeIO(zoomU) * .35 : 0, pull = easeIO(win(t, T.b6 - .3, T.b6 + .4));
  const camZ = 10.2 - push + pull * 1.2, yaw = Math.sin(t * .31) * .05;
  camera.position.set(Math.sin(yaw) * camZ, .55 + Math.sin(t * .23) * .05, Math.cos(yaw) * camZ); camera.lookAt(0, .25, 0); camera.updateMatrixWorld(true);

  // ------------------------------------------------ the window: spots per beat, a flip between plugins
  const winOn = 1 - easeIO(win(t, T.b6 - .3, T.b6 + .2));
  const spot = keyed(t, [[-1, V(0, .38, 0)], [T.b6, V(0, .9, -3)]], .5);
  const tiltK = [[-1, V(-.08, .18, 0)], [T.b1, V(-.05, -.16, 0)], [T.b2, V(-.06, .15, 0)], [T.b3, V(-.05, -.14, 0)], [T.b4, V(-.06, .14, 0)], [T.b5, V(-.05, -.15, 0)]];
  const tilt = keyed(t, tiltK, .7);
  const enter = back(win(t, 0, .55));
  winG.position.copy(spot).add(V(0, Math.sin(t * 1.1) * .03 + (1 - enter) * -.4, (1 - ease(win(t, 0, .55))) * -2));
  let flipA = 0;
  for (const b of [T.b1, T.b2, T.b3, T.b4, T.b5]) { const u = win(t, b - .22, b + .3); if (u > 0 && u < 1) flipA = u < .5 ? Math.PI * easeIO(u) : Math.PI * (easeIO(u) - 1); }
  winG.rotation.set(tilt.x * (1 - push * .8), tilt.y * (1 - push * .9) + flipA, 0);
  S(winG, winOn * (.9 + .02 * enter)); winG.visible = winOn > .01;
  winShadow.position.set(winG.position.x, FY + .005, winG.position.z + .2); winShadow.material.opacity = winOn * .8;
  // pages: the current one, cross-fading from the previous inside a plugin (between plugins the flip hides the swap)
  const prevSame = k > 0 && !D.seq[k].flip;
  const fadeU = prevSame ? win(t, s.t0, s.t0 + .35) : 1;
  showPage(screens[1], k, crop(s, zoomU || win(t, s.t0, (D.seq[k + 1] || { t0: T.b6 }).t0) * (s.box ? 0 : 1)), fadeU);
  if (prevSame && fadeU < 1) { const p = D.seq[k - 1]; showPage(screens[0], k - 1, crop(p, p.box ? 1 : 1), 1); } else screens[0].visible = false;
  urlMesh.material.map = urlTex[s.url]; urlMesh.material.needsUpdate = true;
  // the selection frame
  const fOn = k === 0 ? .25 : s.t0 + 1.1;
  const fa = s.box ? win(t, fOn, fOn + .25) * (1 - win(t, (D.seq[k + 1] || { t0: T.b6 }).t0 - .25, (D.seq[k + 1] || { t0: T.b6 }).t0 - .05)) : 0;
  frame.visible = fa > .01; fDim.material.opacity = fa * .1;
  if (s.box) {
    const c = crop(s, 1), b = s.box, pad = 10;
    const x0 = -VWU / 2 + (b.x - pad - c.x) / c.w * VWU, x1 = -VWU / 2 + (b.x + b.w + pad - c.x) / c.w * VWU;
    const y0 = scrY + VHU / 2 - (b.y - pad - c.y) / c.h * VHU, y1 = scrY + VHU / 2 - (b.y + b.h + pad - c.y) / c.h * VHU;
    const X0 = clamp(x0, -VWU / 2 + .03, VWU / 2 - .03), X1 = clamp(x1, -VWU / 2 + .03, VWU / 2 - .03), Y0 = clamp(y0, scrY - VHU / 2 + .03, scrY + VHU / 2 - .03), Y1 = clamp(y1, scrY - VHU / 2 + .03, scrY + VHU / 2 - .03);
    const th = .012, sp = back(win(t, fOn, fOn + .3)), cx = (X0 + X1) / 2, cy = (Y0 + Y1) / 2;
    frame.position.set(cx, cy, .056); frame.scale.setScalar(.85 + .15 * sp);
    const hw = (X1 - X0) / 2, hh = (Y0 - Y1) / 2;
    fEdges[0].position.set(0, hh, 0); fEdges[0].scale.set(hw * 2, th, 1); fEdges[1].position.set(0, -hh, 0); fEdges[1].scale.set(hw * 2, th, 1);
    fEdges[2].position.set(-hw, 0, 0); fEdges[2].scale.set(th, hh * 2, 1); fEdges[3].position.set(hw, 0, 0); fEdges[3].scale.set(th, hh * 2, 1);
    [[-hw, hh], [hw, hh], [-hw, -hh], [hw, -hh]].forEach(([x, y], i) => fHandles[i].position.set(x, y, .001));
    fM.opacity = fa;
  }

  // ------------------------------------------------ desk props (one group per beat, popping up from the desk)
  const pk = (g, b0, b1) => { const a = life(t, b0 + .15, b1); g.visible = a > .01; return a; };
  // hook star
  const aS = pk(gStar, -1, T.b1); gStar.position.copy(DESK).add(V(0, .07 + back(win(t, .1, .6)) * .0, 0)); S(gStar, back(win(t, .05, .55)) * aS);
  starM.position.y = .45 + Math.sin(t * 2) * .04; starM.rotation.y = t * 1.6;
  for (let i = 0; i < SPN; i++) { const u = win(t, T.stars - .05 + rnd(i) * .25, T.stars + 1.2 + rnd(i) * .5), a = rnd(i, 2) * Math.PI * 2, r = .3 + ease(u) * (1.2 + rnd(i, 3));
    m4.compose(V(Math.cos(a) * r, -.6 + ease(u) * (1.5 + rnd(i, 4) * 1.2) - u * u * 1.2, .9 + Math.sin(a) * r * .5), q.setFromEuler(new THREE.Euler(0, t * 3 + i, t * 2)), sc.setScalar(u > 0 && u < 1 && i % 2 === 0 ? .2 * (1 - u * .6) : 0)); sparks.setMatrixAt(i, m4); }
  sparks.instanceMatrix.needsUpdate = true;
  project(gStar, V(.95, .55, 0), $("lbl0"), aS * win(t, T.stars - .1, T.stars + .1));
  // Ponytail
  const aP = pk(gPony, T.b1, T.b2); gPony.position.copy(DESK); S(gPony, back(win(t, T.b1 + .2, T.b1 + .7)) * aP);
  const hC = lerp(.62, .62 * .47, easeIO(win(t, T.half - .1, T.half + .6))); codeBar.scale.y = hC;
  codeLines.forEach((l, i) => { l.position.set(-.02, (.88 - i * .14), .215); l.scale.y = 1 / Math.max(.2, hC); l.visible = (.88 - i * .14) < 1; });
  const nC = Math.round(lerp(10, 7.4, easeIO(win(t, T.quarter - .1, T.quarter + .6))));
  for (let i = 0; i < CN; i++) { m4.compose(V(.45, .03 + i * .058, 0), q.identity(), sc.setScalar(i < nC ? 1 : 0)); coins.setMatrixAt(i, m4); }
  coins.instanceMatrix.needsUpdate = true;
  tick.position.set(0, .3, .25); S(tick, back(win(t, T.same - .1, T.same + .25)) * (t > T.same - .1 ? 1 : 0)); tick.rotation.y = Math.sin(t * 2) * .2;
  project(codeBar, V(0, 1.15, 0), $("lbl1a"), aP * win(t, T.half - .1, T.half + .1));
  project(null, V(.45, FY + .03 + nC * .058 + .17, .95), $("lbl1b"), aP * win(t, T.quarter - .1, T.quarter + .1));
  project(null, V(0, FY + .1, 1.4), $("lbl1c"), aP * win(t, T.same - .1, T.same + .1));
  // Unslop
  const aU = pk(gUns, T.b2, T.b3); gUns.position.copy(DESK); S(gUns, back(win(t, T.b2 + .2, T.b2 + .7)) * aU);
  const snap = easeIO(win(t, T.designed - .9, T.designed - .2));
  blobs.forEach((g, i) => { g.position.set(-.75 + i * .5, .3 + Math.sin(t * 3 + i) * .06, 0); g.rotation.y = Math.sin(t * 2 + i) * .4; S(g, (1 - snap) * back(win(t, T.b2 + .25 + i * .08, T.b2 + .6 + i * .08))); });
  cleanT.forEach((g, i) => { g.position.set((i % 2 ? .3 : -.3), .16 + (i < 2 ? .27 : 0), 0); S(g, back(win(t, T.designed - .6 + i * .07, T.designed - .2 + i * .07))); g.rotation.y = (1 - snap) * 1.2; });
  project(null, V(0, FY + .1, 1.4), $("lbl2a"), aU * win(t, T.purple - .1, T.purple + .1) * (1 - snap));
  project(null, V(0, FY + .1, 1.4), $("lbl2b"), aU * snap);
  // Elephant-Goldfish
  const aE = pk(gEgm, T.b3, T.b4); gEgm.position.copy(DESK).add(V(0, .32, 0)); S(gEgm, back(win(t, T.b3 + .2, T.b3 + .7)) * aE);
  doc.rotation.set(-.2, Math.sin(t * .8) * .15, 0);
  orbs.forEach((g, i) => { const a = t * 1.4 + i * 2.09, on = win(t, T.fresh - .2 + i * .12, T.fresh + .2 + i * .12);
    g.position.set(Math.cos(a) * .62, .15 + Math.sin(a * 1.3) * .08, Math.sin(a) * .3 + .25); g.lookAt(gEgm.localToWorld(V(0, 0, 0))); S(g, back(on)); g.userData.beam.material.opacity = .22 * on; });
  docTicks.forEach((g, i) => { g.position.set(-.22 + i * .22, -.32, .06); S(g, back(win(t, T.fresh + .7 + i * .2, T.fresh + 1.0 + i * .2))); });
  project(null, V(0, FY + .1, 1.4), $("lbl3a"), aE * win(t, T.fresh - .1, T.fresh + .1) * (1 - win(t, T.thousands - .2, T.thousands)));
  project(null, V(0, FY + .1, 1.4), $("lbl3b"), aE * win(t, T.thousands - .1, T.thousands + .1));
  // Agent Reach
  const aR = pk(gReach, T.b4, T.b5); gReach.position.copy(DESK).add(V(0, .4, 0)); S(gReach, back(win(t, T.b4 + .2, T.b4 + .7)) * aR);
  globe.rotation.y = globeCore.rotation.y = t * .6;
  plat.forEach((g, i) => { const a = t * 1.1 + i * 2.09, on = win(t, T.read + i * .25, T.read + .3 + i * .25);
    g.position.set(Math.cos(a) * .78, .05 + Math.sin(a * 2) * .06, Math.sin(a) * .35); g.rotation.y = Math.sin(a) * .35; S(g, back(on)); });
  project(null, V(0, FY + .1, 1.4), $("lbl4"), aR * win(t, T.never - .1, T.never + .1));
  // Setup
  const aT = pk(gSet, T.b5, T.b6); gSet.position.copy(DESK).add(V(0, .12, 0)); S(gSet, back(win(t, T.b5 + .2, T.b5 + .7)) * aT);
  const sweep = win(t, T.scans - .1, T.scans + 1.2);
  for (let i = 0; i < FN; i++) { const c = i % 8, r = Math.floor(i / 8), x = -.7 + c * .2, lit = sweep > (c + .5) / 8 ? 1 : 0;
    m4.compose(V(x, .1 + r * .02, -r * .2), q.setFromEuler(new THREE.Euler(-.4, 0, 0)), sc.setScalar(1)); files.setMatrixAt(i, m4);
    files.setColorAt(i, new THREE.Color(lit ? 0xe9dcff : 0xffffff)); }
  files.instanceMatrix.needsUpdate = true; if (files.instanceColor) files.instanceColor.needsUpdate = true;
  scanner.position.set(-.8 + sweep * 1.6, .25, .05); scanner.visible = sweep > 0 && sweep < 1;
  recs.forEach((g, i) => { const u = back(win(t, T.hooks - .1 + i * .3, T.hooks + .25 + i * .3)); g.position.set(-.5 + i * .5, .35 + u * .25, .25); S(g, u); g.rotation.y = Math.sin(t * 2 + i) * .15; });
  project(null, V(0, FY + .1, 1.4), $("lbl5"), aT * win(t, T.b5 + .5, T.b5 + .8));
  // share carousel
  const aC = life(t, T.b6, T.b7); caro.visible = aC > .01; caro.position.set(0, .45, 0); S(caro, back(win(t, T.b6, T.b6 + .6)) * aC * 1.3);
  caroCards.forEach((g, i) => { const a = i / 5 * Math.PI * 2 + t * .7; g.position.set(Math.sin(a) * 1.25, Math.sin(t + i) * .06, Math.cos(a) * 1.0); g.rotation.y = a;
    const p = g.userData.p; if (caroTex[i]) p.material.map = caroTex[i]; });
  [0, 1, 2, 3, 4].forEach((i) => { const a = i / 5 * Math.PI * 2 + t * .7;   // a name only while its card faces the front
    project(caroCards[i], V(0, -.52, 0), $("cn" + i), aC * win(t, T.b6 + .2 + i * .08, T.b6 + .4 + i * .08) * clamp((Math.cos(a) - .55) / .3)); });
  // CTA mark
  const aM = life(t, T.b7, 999); markG.visible = aM > .01; markG.position.set(0, -.55, .5); S(markG, back(win(t, T.kw + .2, T.kw + .7)) * aM); markG.rotation.y = Math.sin(t * 1.5) * .5;
  renderer.render(scene, camera);
}

const loader = new THREE.TextureLoader();
const ready = (async () => {
  try { await Promise.all(["700 40px Inter", "600 40px Inter", "800 40px Mont"].map((f) => document.fonts.load(f))); } catch (e) { /* fallback */ }
  makeUrls(); for (const [m, txt, o] of TEXTS) { m.material.map = textTex(txt, o); m.material.needsUpdate = true; }
  const imgs = await Promise.all(D.seq.map((s) => loader.loadAsync(s.src)));
  imgs.forEach((tx, i) => { tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 16; tx.minFilter = THREE.LinearMipmapLinearFilter; tex[i] = tx; });
  D.caro.forEach((idx, i) => { const sd = D.seq[idx], c = tex[idx].clone(); c.needsUpdate = true; const r = (sd.w * .74 / 1.04) / sd.h; c.repeat.set(1, r); c.offset.set(0, 1 - r); caroTex[i] = c; });
  const mk = await loader.loadAsync("assets/img/logo-mark.svg"); mk.colorSpace = THREE.SRGBColorSpace; markFace.material.map = mk;
  renderer.compile(scene, camera); renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["scene"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
