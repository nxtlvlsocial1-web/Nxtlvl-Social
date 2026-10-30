// The 3D layer of the "Continue?" Reel: a bright Y2K game stage (soft lavender-white backdrop with drifting colour
// blobs, a scrolling grid floor, floating particles) and the 3D props of each scene: chrome countdown numerals, the
// P1 and P2 gamepads, the chrome CONSOLE SKILL title, the disc-to-PC stream, the power-up items, the voxel crash boss,
// the New Game+ world map, the rubber stamp and the confetti. Everything is a pure function of time t, rendered on
// HyperFrames' hf-seek. Scene windows and word times come from window.CS_T (written by build/generate.py).
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";
import { TTFLoader } from "three/addons/loaders/TTFLoader.js";
import { Font } from "three/addons/loaders/FontLoader.js";

const T = window.CS_T, S = T.S, w = T.w;
const W = 1080, H = 1920;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => cl((t - a) / (b - a));
const eOut = (x) => 1 - Math.pow(1 - x, 3);
const eIn = (x) => x * x * x;
const eInOut = (x) => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const eBack = (x) => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const inS = (t, k) => t >= S[k][0] && t < S[k][1];
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
// screen pixels to the z=0 plane of the base camera (z=10, fov 32): 334.8 px per unit
const K = 960 / (10 * Math.tan(THREE.MathUtils.degToRad(16)));
const px = (x, y) => V((x - 540) / K, (960 - y) / K, 0);

// WebGL draws off-screen and each frame is copied into the page's 2D canvas (HyperFrames' software compositing can drop
// a band of an in-page WebGL canvas)
const glEl = document.getElementById("gl"); glEl.width = W; glEl.height = H;
const out2d = glEl.getContext("2d");
const canvas = document.createElement("canvas"); canvas.width = W; canvas.height = H;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance", preserveDrawingBuffer: true });
renderer.setClearColor(0x000000, 0);
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(32, W / H, .1, 120);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = 1.0;
const BG = new THREE.Color("#F1EEF4");
scene.fog = new THREE.Fog(BG, 40, 120);   // effectively off: the colour fields behind are dark/saturated

// the canvas is transparent: the gameplay and the lavender wash behind it are DOM layers (build/generate.py)

// lights
scene.add(new THREE.HemisphereLight(0xffffff, 0xd9d2ee, .9));
const key = new THREE.DirectionalLight(0xffffff, 2.2);
key.position.set(3, 7, 6); key.castShadow = true;
key.shadow.mapSize.set(1024, 1024);
Object.assign(key.shadow.camera, { left: -6, right: 6, top: 6, bottom: -6, near: 1, far: 30 });
key.shadow.radius = 6;
scene.add(key);
const sweep = new THREE.PointLight(0xffffff, 0, 8, 1.5); scene.add(sweep);

// floor: shadow catcher plus a scrolling grid
const FLOOR_Y = -2.15;
const shadowPlane = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), new THREE.ShadowMaterial({ opacity: .14 }));
shadowPlane.rotation.x = -Math.PI / 2; shadowPlane.position.y = FLOOR_Y; shadowPlane.receiveShadow = true;
scene.add(shadowPlane);
const grid = new THREE.GridHelper(80, 80, 0xc9c0e6, 0xd8d1ee);
grid.position.y = FLOOR_Y + .002; grid.material.transparent = true; grid.material.opacity = .85;
scene.add(grid);

// floating particles (little plus-cubes and octahedra) at many depths
const NP = 70;
const parts = new THREE.InstancedMesh(new THREE.OctahedronGeometry(.07, 0),
  new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .3, metalness: .2 }), NP);
const PCOL = ["#ffb36b", "#ff7a45", "#ffd38a", "#ffffff", "#ff9ad0"];
for (let i = 0; i < NP; i++) parts.setColorAt(i, new THREE.Color(PCOL[i % PCOL.length]));
scene.add(parts);
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _s = new THREE.Vector3(), _p = new THREE.Vector3();
function updParticles(t) {
  for (let i = 0; i < NP; i++) {
    const z = -2 - hash(i) * 14, x = (hash(i + 9) - .5) * (8 + -z * .8);
    const y = ((hash(i + 3) * 12 + t * (.12 + hash(i + 5) * .2)) % 12) - 5;
    _p.set(x + Math.sin(t * .5 + i) * .2, y, z);
    _e.set(t * (.4 + hash(i + 1)), t * (.6 + hash(i + 2)), 0); _q.setFromEuler(_e);
    const s = .6 + hash(i + 7) * 1.2; _s.set(s, s, s);
    parts.setMatrixAt(i, _m.compose(_p, _q, _s));
  }
  parts.instanceMatrix.needsUpdate = true;
}

// ------------------------------------------------------------------ materials
const M = {
  chrome: new THREE.MeshPhysicalMaterial({ color: 0xdcdfe8, metalness: 1, roughness: .14, clearcoat: 1, clearcoatRoughness: .1 }),
  violet: new THREE.MeshPhysicalMaterial({ color: 0x7a2ffb, metalness: .65, roughness: .22, clearcoat: 1, clearcoatRoughness: .15, emissive: 0x3a0f99, emissiveIntensity: .25 }),
  plastic: new THREE.MeshPhysicalMaterial({ color: 0xeceaf2, metalness: .05, roughness: .35, clearcoat: .6 }),
  ink: new THREE.MeshPhysicalMaterial({ color: 0x1d1a26, metalness: .2, roughness: .4, clearcoat: .5 }),
  iri: new THREE.MeshPhysicalMaterial({ color: 0xf2f2ff, metalness: .9, roughness: .12, iridescence: 1, iridescenceIOR: 1.6, iridescenceThicknessRange: [200, 900] }),
  claude: new THREE.MeshPhysicalMaterial({ color: 0xd97757, metalness: .35, roughness: .24, clearcoat: 1, clearcoatRoughness: .12, emissive: 0x8a3216, emissiveIntensity: .2 }),
  gem: new THREE.MeshPhysicalMaterial({ color: 0x9fd4ff, metalness: .2, roughness: .05, transmission: .0, iridescence: 1, iridescenceIOR: 1.8, clearcoat: 1, flatShading: true }),
};
const pastel = (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .35, metalness: .05, clearcoat: .7 });

function mesh(geo, mat, parent, x = 0, y = 0, z = 0) {
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; (parent || scene).add(m); return m;
}
function group(parent) { const g = new THREE.Group(); (parent || scene).add(g); return g; }

function canvasTex(w_, h_, draw) {
  const c = document.createElement("canvas"); c.width = w_; c.height = h_;
  draw(c.getContext("2d"), w_, h_);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4;
  tx.userData.canvas = c; return tx;
}

// ------------------------------------------------------------------ builders
function gamepad(bodyMat, accent) {
  const g = new THREE.Group();
  mesh(new RoundedBoxGeometry(1.7, .62, .42, 5, .2), bodyMat, g, 0, .05, 0);
  for (const s of [-1, 1]) {
    const grip = mesh(new THREE.CapsuleGeometry(.28, .5, 6, 16), bodyMat, g, s * .66, -.32, 0);
    grip.rotation.z = s * .5;
    const stick = mesh(new THREE.CylinderGeometry(.13, .15, .16, 24), M.ink, g, s * .32, -.17, .26);
    stick.rotation.x = Math.PI / 2;
  }
  for (const [x, y] of [[.5, .2], [.62, .08], [.5, -.04], [.38, .08]]) mesh(new THREE.SphereGeometry(.065, 16, 12), accent, g, x, y, .22);
  mesh(new THREE.BoxGeometry(.3, .09, .08), M.ink, g, -.5, .08, .22);
  mesh(new THREE.BoxGeometry(.09, .3, .08), M.ink, g, -.5, .08, .22);
  mesh(new THREE.BoxGeometry(.16, .06, .05), accent, g, -.1, .2, .21);
  mesh(new THREE.BoxGeometry(.16, .06, .05), accent, g, .1, .2, .21);
  return g;
}

function starGeo(r1 = 1, r2 = .45, depth = .3, n = 5) {
  const sh = new THREE.Shape();
  for (let i = 0; i < n * 2; i++) {
    const a = Math.PI / 2 + i * Math.PI / n, r = i % 2 ? r2 : r1;
    const x = Math.cos(a) * r, y = Math.sin(a) * r;
    i ? sh.lineTo(x, y) : sh.moveTo(x, y);
  }
  const g = new THREE.ExtrudeGeometry(sh, { depth, bevelEnabled: true, bevelThickness: .06, bevelSize: .05, bevelSegments: 4 });
  g.center(); return g;
}

function textGeo(font, str, size, depth = .22) {
  const g = new TextGeometry(str, { font, size, depth, curveSegments: 8, bevelEnabled: true, bevelThickness: .035, bevelSize: .022, bevelSegments: 4 });
  g.computeBoundingBox(); g.center(); return g;
}

async function loadFont(url) {
  const json = await new Promise((res, rej) => new TTFLoader().load(url, res, undefined, rej));
  return new Font(json);
}
function loadImg(src) { return new Promise((res) => { const im = new Image(); im.onload = () => res(im); im.src = src; }); }

// ------------------------------------------------------------------ the props
let P = null;
async function build() {
  const [lilita, apple, deck, win, tux] = await Promise.all([loadFont("assets/fonts/LilitaOne.ttf"),
    loadImg("assets/img/apple.png"), loadImg("assets/img/deck-logo.png"), loadImg("assets/img/windows-logo.png"), loadImg("assets/img/linux-logo.png")]);
  // glossy toy-like type: white or violet faces with deeper violet sides (TextGeometry group 0 = faces, 1 = sides)
  const gFace = new THREE.MeshPhysicalMaterial({ color: 0xfbfaff, roughness: .16, metalness: .05, clearcoat: 1, clearcoatRoughness: .08 });
  const gSide = new THREE.MeshPhysicalMaterial({ color: 0x6a22e8, roughness: .3, metalness: .2, clearcoat: .8 });
  const vface = new THREE.MeshPhysicalMaterial({ color: 0x8a46ff, roughness: .18, metalness: .1, clearcoat: 1, clearcoatRoughness: .08 });
  const vside = new THREE.MeshPhysicalMaterial({ color: 0x3d1294, roughness: .3, metalness: .2, clearcoat: .8 });
  P = {};
  // countdown digits (scenes A and H)
  P.digits = {};
  for (const d of "123456789") {
    const m = mesh(textGeo(lilita, d, 1.7, .42), [gFace, gSide]); m.visible = false; P.digits[d] = m;
  }
  // gamepads (B), and a white one for the inventory (D)
  P.p1 = gamepad(M.plastic, pastel(0x8fb8ff)); scene.add(P.p1);
  P.p2 = gamepad(M.claude, pastel(0xffffff)); scene.add(P.p2);
  // Claude's spark mark in 3D: twelve rounded rays of uneven length
  P.spark = group();
  [1, .78, .95, .72, 1, .82, .9, .7, .98, .8, .88, .74].forEach((r, i) => {
    const ray = mesh(new RoundedBoxGeometry(.11, .46 * r, .1, 3, .05), M.claude, P.spark);
    const a = i * Math.PI / 6 + (i % 2 ? .12 : 0);
    ray.position.set(-Math.sin(a) * .23 * r, Math.cos(a) * .23 * r, 0); ray.rotation.z = a;
  });
  mesh(new THREE.SphereGeometry(.09, 24, 16), M.claude, P.spark);
  P.padItem = gamepad(M.plastic, M.violet); scene.add(P.padItem);
  // title (C1)
  P.t1 = mesh(textGeo(lilita, "CONSOLE", .44, .22), [gFace, gSide]);
  P.t2 = mesh(textGeo(lilita, "SKILL", .5, .24), [vface, vside]);
  // disc, monitor, bit stream (C2)
  P.disc = group();
  const dm = mesh(new THREE.CylinderGeometry(.6, .6, .035, 96), M.iri, P.disc); dm.rotation.x = Math.PI / 2;
  const hole = mesh(new THREE.CylinderGeometry(.12, .12, .05, 48), pastel(0xf1eef4), P.disc); hole.rotation.x = Math.PI / 2;
  const hub = mesh(new THREE.TorusGeometry(.2, .03, 12, 48), M.chrome, P.disc); hub.position.z = .02;
  P.mon = group();
  mesh(new RoundedBoxGeometry(1.45, 1.0, .14, 4, .06), M.plastic, P.mon);
  mesh(new THREE.CylinderGeometry(.05, .05, .5, 16), M.chrome, P.mon, 0, -.68, -.05);
  mesh(new RoundedBoxGeometry(.6, .06, .3, 3, .03), M.plastic, P.mon, 0, -.93, -.05);
  P.screenTex = canvasTex(512, 340, () => {});
  P.screen = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .86), new THREE.MeshBasicMaterial({ map: P.screenTex, toneMapped: false }));
  P.screen.position.z = .075; P.mon.add(P.screen);
  P.screenState = -1;
  P.bits = new THREE.InstancedMesh(new RoundedBoxGeometry(.07, .07, .07, 2, .015), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .25, metalness: .3, emissive: 0x7a2ffb, emissiveIntensity: .35 }), 48);
  for (let i = 0; i < 48; i++) P.bits.setColorAt(i, new THREE.Color(["#7a2ffb", "#8fb8ff", "#ff9ccf", "#b9a2ff"][i % 4]));
  scene.add(P.bits);
  // power-up items (D)
  P.star = mesh(starGeo(.66, .3, .24), pastel(0xffd36e));
  P.star.material.metalness = .55; P.star.material.roughness = .2;
  P.gem = mesh(new THREE.IcosahedronGeometry(.48, 0), M.gem);
  P.blocks = group();
  [[0, 0, 0, 0x8fb8ff], [.34, .34, 0, 0xffd36e], [.68, .68, 0, 0xff9ccf], [-.34, 0, 0, 0xb9a2ff]].forEach(([x, y, z, c]) =>
    mesh(new RoundedBoxGeometry(.32, .32, .32, 3, .05), pastel(c), P.blocks, x - .17, y - .34, z));
  // the boss (E): a voxel blob
  const vox = [];
  for (let x = -7; x <= 7; x++) for (let y = -8; y <= 8; y++) for (let z = -5; z <= 5; z++) {
    const r = Math.sqrt((x / 7) ** 2 + (y / 8) ** 2 + (z / 5) ** 2);
    if (r < 1 && r > .72) vox.push([x, y, z]);
  }
  P.vox = vox;
  P.boss = new THREE.InstancedMesh(new THREE.BoxGeometry(.085, .085, .085), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .5, metalness: .1, emissive: 0xffffff, emissiveIntensity: 0 }), vox.length);
  P.boss.castShadow = true;
  vox.forEach(([x, y, z], i) => {
    const eye = z > 3 && y > 1 && y < 4 && (Math.abs(x + 3) < 2 || Math.abs(x - 3) < 2);
    const c = eye ? "#ff3355" : hash(i) < .12 ? "#7a2ffb" : hash(i + 1) < .1 ? "#ff3355" : "#26222f";
    P.boss.setColorAt(i, new THREE.Color(c));
  });
  scene.add(P.boss);
  P.shots = [0, 1, 2, 3].map(() => mesh(new THREE.OctahedronGeometry(.13, 0), M.claude));
  // world map (F)
  const tiles = [[-.65, -.8, .2, .5, 0xbcd6ff], [.65, -.45, -1.6, .5, 0xffd9ec], [-.55, -.1, -3.3, .5, 0xd9ccff], [.45, .2, -4.9, .62, 0xfff0b8]];
  P.tiles = tiles.map(([x, y, z, r, c], i) => {
    const g = group(); g.position.set(x, y, z);
    mesh(new THREE.CylinderGeometry(r, r * .78, .34, 6), pastel(c), g);
    mesh(new THREE.CylinderGeometry(r * .92, r * .92, .04, 6), pastel(0xffffff), g, 0, .18, 0);
    mesh(new THREE.CylinderGeometry(.025, .025, 1.0, 12), M.chrome, g, -r * .45, .68, 0);
    const label = ["WINDOWS", "MAC", "LINUX", "STEAM DECK"][i];
    const tx = canvasTex(512, 300, (g2, W2, H2) => {
      g2.fillStyle = i === 3 ? "#7a2ffb" : "#ffffff"; g2.fillRect(0, 0, W2, H2);
      g2.strokeStyle = "#1d1a26"; g2.lineWidth = 14; g2.strokeRect(7, 7, W2 - 14, H2 - 14);
      g2.fillStyle = i === 3 ? "#ffffff" : "#1d1a26"; g2.textAlign = "center"; g2.textBaseline = "middle";
      if (i === 0) g2.drawImage(win, W2 / 2 - 80, 30, 160, 160);
      if (i === 1) g2.drawImage(apple, W2 / 2 - 95, 28, 190, 190);
      if (i === 2) g2.drawImage(tux, 40, 40, 432, 432 * tux.height / tux.width);
      if (i === 3) g2.drawImage(deck, W2 / 2 - 80, 22, 160, 160);
      g2.font = `${i === 3 ? 62 : 64}px "Lilita One"`;
      if (i !== 2) g2.fillText(label, W2 / 2, i === 3 ? 240 : 255);
    });
    const flag = new THREE.Mesh(new THREE.PlaneGeometry(.78, .46), new THREE.MeshStandardMaterial({ map: tx, roughness: .5, side: THREE.DoubleSide }));
    flag.position.set(-r * .45 + .41, .95, 0); flag.castShadow = true; g.add(flag);
    g.userData.flag = flag;
    return g;
  });
  P.pearls = [];
  for (let k = 0; k < 3; k++) for (let j = 1; j <= 4; j++) {
    const a = tiles[k], b = tiles[k + 1], f = j / 5;
    P.pearls.push(mesh(new THREE.SphereGeometry(.06, 16, 12), pastel(0xffffff), scene, a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f + .2, a[2] + (b[2] - a[2]) * f));
  }
  // status card and the rubber stamp (G)
  P.card = group();
  const cardTex = canvasTex(800, 900, (g2, W2, H2) => {
    g2.fillStyle = "#ffffff"; g2.fillRect(0, 0, W2, H2);
    g2.fillStyle = "#1d1a26"; g2.font = '44px "Russo One"'; g2.fillText("BUILD STATUS", 60, 110);
    g2.fillStyle = "#7a2ffb"; g2.fillRect(60, 140, 120, 10);
    const rows = [["PORT TO PC", "READY"], ["MODS", "READY"], ["BOOTS EVERY GAME", "NOT YET"]];
    rows.forEach(([a, b], i) => {
      const y = 250 + i * 110;
      g2.fillStyle = "#efecf6"; g2.fillRect(60, y - 60, 680, 88);
      g2.fillStyle = "#1d1a26"; g2.font = '600 36px "Chakra Petch"'; g2.fillText(a, 90, y);
      g2.fillStyle = i === 2 ? "#e0335a" : "#7a2ffb"; g2.textAlign = "right"; g2.fillText(b, 710, y); g2.textAlign = "left";
    });
  });
  const cm = mesh(new RoundedBoxGeometry(2.0, 2.25, .06, 3, .04), [M.plastic], P.card);
  const face = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 2.14), new THREE.MeshStandardMaterial({ map: cardTex, roughness: .6 }));
  face.position.z = .032; P.card.add(face);
  P.ink = new THREE.Mesh(new THREE.PlaneGeometry(1.75, .62), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false,
    map: canvasTex(700, 250, (g2, W2, H2) => {
      g2.strokeStyle = "#e0335a"; g2.lineWidth = 16; g2.strokeRect(14, 14, W2 - 28, H2 - 28);
      g2.fillStyle = "#e0335a"; g2.font = '80px "Russo One"'; g2.textAlign = "center"; g2.textBaseline = "middle"; g2.fillText("EARLY ACCESS", W2 / 2, H2 / 2 + 6);
    }) }));
  P.ink.position.set(0, -.52, .04); P.ink.rotation.z = .12; P.card.add(P.ink);
  P.stamp = group();
  mesh(new RoundedBoxGeometry(1.8, .5, .7, 4, .08), pastel(0xe0335a), P.stamp, 0, 0, 0);
  mesh(new THREE.CylinderGeometry(.16, .2, 1.1, 24), pastel(0xf4efe6), P.stamp, 0, .8, 0);
  mesh(new THREE.SphereGeometry(.32, 24, 16), pastel(0x1d1a26), P.stamp, 0, 1.45, 0);
  // confetti (H)
  P.conf = new THREE.InstancedMesh(new THREE.PlaneGeometry(.09, .13), new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: .5 }), 160);
  for (let i = 0; i < 160; i++) P.conf.setColorAt(i, new THREE.Color(["#7a2ffb", "#8fb8ff", "#ffd36e", "#ff9ccf", "#1d1a26", "#b9a2ff"][i % 6]));
  scene.add(P.conf);
  // the end card's "press to continue" button: a glossy violet arcade button with a white play arrow
  P.btn = group();
  mesh(new THREE.CylinderGeometry(1.0, 1.08, .32, 64), pastel(0xf4f2fa), P.btn, 0, -.16, 0);
  P.cap = mesh(new THREE.CylinderGeometry(.82, .86, .3, 64), M.violet, P.btn, 0, .1, 0);
  const tri = new THREE.Shape(); tri.moveTo(-.22, -.3); tri.lineTo(-.22, .3); tri.lineTo(.32, 0); tri.closePath();
  const arrow = mesh(new THREE.ExtrudeGeometry(tri, { depth: .06, bevelEnabled: true, bevelThickness: .02, bevelSize: .02, bevelSegments: 3 }), pastel(0xffffff), P.cap);
  arrow.rotation.x = -Math.PI / 2; arrow.position.y = .16;
  renderer.compile(scene, camera);
}

function hideAll() {
  for (const d in P.digits) P.digits[d].visible = false;
  for (const o of [P.p1, P.p2, P.padItem, P.t1, P.t2, P.disc, P.mon, P.bits, P.star, P.gem, P.blocks, P.boss, P.card, P.stamp, P.conf, P.btn, P.spark, ...P.shots, ...P.tiles, ...P.pearls])
    o.visible = false;
}

function drawScreen(state) {
  if (P.screenState === state) return;
  P.screenState = state;
  const c = P.screenTex.userData.canvas, g = c.getContext("2d");
  if (state === 0) {
    g.fillStyle = "#26222f"; g.fillRect(0, 0, 512, 340);
    g.fillStyle = "#6f6a80"; g.font = '600 34px "Chakra Petch"'; g.textAlign = "center"; g.fillText("NO SIGNAL", 256, 182);
  } else {
    const gr = g.createLinearGradient(0, 0, 512, 340); gr.addColorStop(0, "#f7f5ff"); gr.addColorStop(1, "#dcd2ff");
    g.fillStyle = gr; g.fillRect(0, 0, 512, 340);
    g.fillStyle = "#7a2ffb"; g.beginPath(); g.moveTo(206, 104); g.lineTo(206, 220); g.lineTo(306, 162); g.closePath(); g.fill();
    g.fillStyle = "#1d1a26"; g.font = '40px "Russo One"'; g.textAlign = "center"; g.fillText("GAME.EXE", 256, 280);
    g.fillStyle = "#7a2ffb"; g.fillRect(156, 300, 200, 8);
  }
  P.screenTex.needsUpdate = true;
}

// countdown digit: visible inside [a, b), spins in on entry
function digit(t, d, a, b, pos, s = 1) {
  if (t < a || t >= b) return;
  const m = P.digits[d]; m.visible = true;
  const k = eBack(lin(t, a, a + .3));
  m.position.copy(pos);
  m.rotation.set(.12 * Math.sin(t * 1.3), -1.4 * (1 - k) + .22 * Math.sin(t * 1.7), 0);
  m.scale.setScalar(s * (.55 + .45 * k));
}

function place(o, pos, s = 1) { o.visible = true; o.position.copy(pos); o.scale.setScalar(s); }

const _a = new THREE.Vector3(), _b = new THREE.Vector3();
function renderAt(t) {
  if (!P) return;
  hideAll();
  let tint = 0;
  // camera: a slow drift everywhere; scene F flies over the world map
  let cpos = V(Math.sin(t * .37) * .14, Math.cos(t * .29) * .1, 10), look = V(Math.sin(t * .37) * .05, 0, 0);
  updParticles(t * 1.6);
  // the camera pulses on the music's beat
  let pulse = 0;
  for (const b of T.beats) { if (t >= b && t < b + .4) pulse = Math.max(pulse, Math.exp(-(t - b) * 9)); }
  grid.position.z = (t * 1.1) % 1;
  grid.visible = t >= T.count[0][1] - .3 && t < S.B[0];   // not over the opening gameplay   // the floor grid only belongs to the lavender GAME OVER stage
  sweep.intensity = 0;

  if (inS(t, "A")) {
    const pos = px(540, 820);
    const seq = T.count;   // [[digit, start], ...]
    seq.forEach(([d, a], i) => digit(t, d, a, i + 1 < seq.length ? seq[i + 1][1] : S.A[1], pos, .68));
    // after "forever" the stage cools: numerals shrink a touch
  }
  if (inS(t, "B")) {
    tint = .6;
    const l = px(300, 880), r = px(780, 880);
    place(P.p1, l, .62); P.p1.rotation.set(.55, .25 + .08 * Math.sin(t * 1.4), 0); P.p1.position.y += .05 * Math.sin(t * 2);
    if (t >= w[11]) {
      const k = lin(t, w[11], w[14]);
      const e = eOut(k);
      P.p2.visible = true;
      P.p2.position.set(r.x + (4.5 - r.x) * (1 - e), r.y + (3.5 - r.y) * (1 - e) + (k >= 1 ? .06 * Math.sin(t * 2.2) : 0), -2 * (1 - e));
      const pop = t >= w[16] ? 1 + .16 * Math.max(0, 1 - (t - w[16]) / .35) : 1;
      const land = k >= 1 ? 1 + .1 * Math.exp(-(t - w[14]) * 9) * Math.cos((t - w[14]) * 30) : 1;
      P.p2.scale.setScalar(.62 * pop * land);
      P.p2.rotation.set(.55, -.25 + (1 - e) * Math.PI * 4, (1 - e) * .8);
      M.claude.emissiveIntensity = t >= w[16] ? .2 + .9 * Math.max(0, 1 - (t - w[16]) / .6) + .15 * Math.sin(t * 8) ** 2 : .2;
      // "It's Claude!": the spark mark pops out of the pad and spins above it
      if (t >= w[16]) {
        const e = eBack(lin(t, w[16], w[16] + .4));
        place(P.spark, px(780, 700), 1.15 * e); P.spark.rotation.set(.15 * Math.sin(t * 2), .4 * Math.sin(t * 1.6), -(t - w[16]) * 2.4);
      }
    }
  } else M.claude.emissiveIntensity = .2;
  if (inS(t, "C1")) {
    const a1 = w[19], a2 = w[20];
    if (t >= a1) {
      const e = eOut(lin(t, a1, a1 + .5));
      place(P.t1, px(540, 690)); P.t1.position.z = -9 * (1 - e); P.t1.rotation.set(1.3 * (1 - e) + .05 * Math.sin(t), .1 * Math.sin(t * .8), 0);
    }
    if (t >= a2) {
      const e = eOut(lin(t, a2, a2 + .45));
      place(P.t2, px(540, 880)); P.t2.position.z = -9 * (1 - e); P.t2.rotation.set(-1.3 * (1 - e) - .05 * Math.sin(t), -.1 * Math.sin(t * .8), 0);
    }
    sweep.intensity = 60 * Math.sin(Math.PI * lin(t, a2 + .2, a2 + 1.4));
    sweep.position.set(-4 + 8 * lin(t, a2 + .2, a2 + 1.4), .9, 2);
    cpos = V(Math.sin(t * .6) * .35, .1 + Math.cos(t * .4) * .1, 10); look = V(0, .3, 0);
  }
  if (inS(t, "C2")) {
    // the disc spins above the GAME.EXE window (a DOM layer) and streams bits down into it
    const d = px(540, 740), m = px(540, 1040);
    place(P.disc, d, .55); P.disc.rotation.set(-.35, .2 * Math.sin(t), t * 3.5);
    // bits flow from the disc to the screen while the game is rebuilt
    const a = w[25], b = w[33] + .2;
    if (t >= a && t < b + .6) {
      P.bits.visible = true;
      for (let i = 0; i < 48; i++) {
        const ph = ((t - a) * .9 + i / 48) % 1;
        const on = t < b || ph > (t - b) / .6;
        _a.lerpVectors(d, m, ph); _a.x += Math.sin(ph * Math.PI) * (i % 2 ? 1.1 : -1.1) * (.6 + .4 * hash(i)); _a.z += Math.sin(ph * Math.PI) * .6;
        _e.set(t * 3 + i, t * 2 + i, 0); _q.setFromEuler(_e);
        const s = on ? Math.sin(ph * Math.PI) * 1.4 : 0; _s.set(s, s, s);
        P.bits.setMatrixAt(i, _m.compose(_a, _q, _s));
      }
      P.bits.instanceMatrix.needsUpdate = true;
    }
  }
  if (inS(t, "D")) {
    tint = .3;
    const show = px(540, 900);
    const slots = [px(250, 1240), px(540, 1240), px(830, 1240)];
    // power-up star: in on "Grab", out when the chat starts
    if (t >= w[37] && t < w[40] + .25) {
      const k = eBack(lin(t, w[37], w[37] + .35)), o = 1 - eIn(lin(t, w[40], w[40] + .25));
      place(P.star, show, .95 * k * o); P.star.rotation.set(.2 * Math.sin(t), t * 2.4, 0);
    }
    // each power-up spins in at the demo card's corner, then drops into its slot
    const corner = px(900, 680);
    const items = [[P.gem, w[45], w[47] - .05, 0, .6], [P.blocks, w[47], w[49] - .05, 1, .6], [P.padItem, w[49], S.D[1] - .55, 2, .42]];
    for (const [o, a, b, si, sc] of items) {
      if (t < a) continue;
      const k = eBack(lin(t, a, a + .35)), f = eInOut(lin(t, b, b + .3));
      _b.lerpVectors(corner, slots[si], f);
      place(o, _b, sc * k * (1 - .35 * f));
      o.rotation.set(.35 + .1 * Math.sin(t), t * (f > .99 ? 1.2 : 2.2) + si, 0);
    }
  }
  if (inS(t, "E")) {
    tint = -.2;
    const c = px(540, 930);
    if (t >= w[54]) {
      P.boss.visible = true;
      const rise = eOut(lin(t, w[54], w[54] + .5));
      const boom = t >= T.ko ? t - T.ko : -1;
      let flash = 0;
      T.hits.forEach((h) => { if (t >= h + .2 && t < h + .3) flash = 1; });
      P.boss.material.emissiveIntensity = flash * .9;
      for (let i = 0; i < P.vox.length; i++) {
        const [x, y, z] = P.vox[i];
        const jit = hash(i + Math.floor(t * 12) * 13) < .06 ? .08 : 0;
        _a.set(c.x + x * .08 + jit, c.y - 3 * (1 - rise) + y * .08 + .05 * Math.sin(t * 3), z * .08);
        let s = 1;
        if (boom >= 0) {
          const dir = _b.set(x + hash(i) - .5, y + 2, z + hash(i + 3)).normalize();
          _a.addScaledVector(dir, boom * (3 + hash(i + 5) * 4)); _a.y -= 4 * boom * boom;
          s = Math.max(0, 1 - boom * 1.8);
        }
        _e.set(boom >= 0 ? boom * 9 * hash(i) : 0, boom >= 0 ? boom * 7 : 0, 0); _q.setFromEuler(_e);
        _s.set(s, s, s);
        P.boss.setMatrixAt(i, _m.compose(_a, _q, _s));
      }
      P.boss.instanceMatrix.needsUpdate = true;
      P.boss.rotation.set(0, .3 * Math.sin(t * 1.5), 0);
      P.boss.position.set(0, 0, 0);
      // P2's shots
      T.hits.forEach((h, i) => {
        if (t >= h && t < h + .22) {
          const k = lin(t, h, h + .2);
          const from = px(140, 1380);
          _a.lerpVectors(from, c, eIn(k)); _a.y += Math.sin(k * Math.PI) * .8;
          place(P.shots[i], _a, 1.4); P.shots[i].rotation.set(t * 9, t * 7, 0);
        }
      });
    }
  }
  if (inS(t, "F")) {
    tint = .4;
    const k = eInOut(lin(t, S.F[0], S.F[1]));
    cpos = V(.15 * Math.sin(t * .5), 1.7 + k * .5, 10.6 - k * 1.0); look = V(0, -.25 + k * .3, -1.8 - k * 1.0);
    const un = T.unlock;   // unlock times for the four platforms
    P.tiles.forEach((g, i) => {
      g.visible = true;
      const a = un[i] - .3, e = eBack(lin(t, a, a + .4)), on = t >= a;
      g.scale.setScalar(on ? .35 + .65 * e : .35);
      g.position.y = [-.8, -.45, -.1, .2][i] + (on ? .1 * Math.sin(t * 2 + i) : -.25);
      g.rotation.y = .25 * Math.sin(t * .7 + i);
      g.userData.flag.visible = t >= un[i];
      g.userData.flag.scale.setScalar(eBack(lin(t, un[i], un[i] + .3)) || .001);
      g.userData.flag.rotation.y = .25 * Math.sin(t * 3 + i);
    });
    P.pearls.forEach((p, j) => {
      p.visible = true;
      const seg = Math.floor(j / 4), f = (j % 4 + 1) / 5;
      const lit = t >= T.unlock[seg] + .1 + f * .35;
      p.material = lit ? M.violet : p.userData.off || (p.userData.off = pastel(0xffffff));
      p.scale.setScalar(lit ? 1.25 : .9);
    });
  }
  if (inS(t, "G")) {
    const c = px(540, 1000);
    place(P.card, c, 1); P.card.rotation.set(-.08, .12 * Math.sin(t * .8), -.03);
    const hit = w[78];
    P.ink.visible = t >= hit;
    P.ink.scale.setScalar(t >= hit ? 1 + .25 * Math.exp(-(t - hit) * 14) : 1);
    // the stamp comes down onto the card, then lifts away
    const down = eIn(lin(t, hit - .35, hit)), up = eOut(lin(t, hit + .25, hit + .75));
    const y = 3.4 * (1 - down) + 3.6 * up;
    if (y < 3.5) { place(P.stamp, V(c.x, c.y - .5 + .36 + y, .7 + y * .2), .9); P.stamp.rotation.set(.35, .12, .1 * (1 - down)); }
    if (t >= hit && t < hit + .2) cpos.y += .06 * Math.sin((t - hit) * 90);
  }
  if (inS(t, "H")) {
    tint = .5;
    const pos = px(540, 900);
    const seq = T.count2;
    seq.forEach(([d, a], i) => digit(t, d, a, i + 1 < seq.length ? seq[i + 1][1] : T.burst, pos, .62));
    if (t >= T.burst) {
      const e = eBack(lin(t, T.burst, T.burst + .4));
      place(P.btn, pos, .6 * e); P.btn.rotation.set(1.05 + .08 * Math.sin(t * 1.3), .25 * Math.sin(t * .9), 0);
      // pressed on "continue", springs back
      const pr = T.press;
      P.cap.position.y = .1 - (t >= pr ? .14 * Math.exp(-(t - pr) * 6) * Math.max(0, Math.cos((t - pr) * 14)) : 0);
      const dt = t - T.burst;
      P.conf.visible = true;
      for (let i = 0; i < 160; i++) {
        const an = hash(i) * Math.PI * 2, sp = 2.5 + hash(i + 1) * 4.5;
        _a.set(pos.x + Math.cos(an) * sp * dt * .9, pos.y + (Math.sin(an) * .6 + 1.4) * sp * dt * .9 - 2.4 * dt * dt, -1 + hash(i + 2) * 3);
        _e.set(dt * (4 + hash(i + 3) * 6), dt * (3 + hash(i + 4) * 5), hash(i) * 6); _q.setFromEuler(_e);
        const s = 1.2 * Math.min(1, dt * 6); _s.set(s, s, s);
        P.conf.setMatrixAt(i, _m.compose(_a, _q, _s));
      }
      P.conf.instanceMatrix.needsUpdate = true;
    }
  }
  cpos.z -= .22 * pulse;
  camera.position.copy(cpos); camera.lookAt(look);
  renderer.render(scene, camera);
  out2d.clearRect(0, 0, W, H);
  out2d.drawImage(canvas, 0, 0);
}

const ready = (async () => {
  await Promise.all(['44px "Russo One"', '64px "Lilita One"', '600 36px "Chakra Petch"'].map((f) => document.fonts.load(f)));
  await build();
  const qt = new URLSearchParams(location.search).get("t");
  renderAt(qt !== null ? +qt : (window.__hfThreeTime || 0));
  if (qt !== null) window.__done = true;
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["csworld"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
