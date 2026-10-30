// The 3D world of the Ashke lyric edit, built from code and inspired by the music video's old-money English estate:
// a manor at dusk with lit windows, gold sunglasses, a silver vintage coupe, polo mallet and ball, a porcelain teacup,
// a wooden speedboat, an emerald-dial gold watch, a glass diamond, interlocking gold rings, a night road with stones,
// a gold chess king, a gold snake, the gold "Ashke" title and glass shards. One scene per lyric section; the camera
// cuts to a new angle every two beats. Pure function of time t on HyperFrames' hf-seek; timings come from window.AK_T.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";
import { TTFLoader } from "three/addons/loaders/TTFLoader.js";
import { Font } from "three/addons/loaders/FontLoader.js";

const T = window.AK_T;
const W = 1920, H = 1080;
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => cl((t - a) / (b - a));
const eOut = (x) => 1 - Math.pow(1 - x, 4);
const eIn = (x) => x * x * x;
const eInOut = (x) => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const eBack = (x) => { const c1 = 1.8, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const V = (x, y, z) => new THREE.Vector3(x, y, z);

const outEl = document.getElementById("gl3d"); outEl.width = W; outEl.height = H;
const out2d = outEl.getContext("2d");
const canvas = document.createElement("canvas"); canvas.width = W; canvas.height = H;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setClearColor(0x000000, 0);
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, W / H, .1, 300);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .03).texture;
const hemi = new THREE.HemisphereLight(0xfff1dc, 0x1a120a, .9); scene.add(hemi);
const key = new THREE.DirectionalLight(0xffe0b0, 2.6); key.position.set(5, 8, 7); key.castShadow = true;
key.shadow.mapSize.set(1024, 1024); Object.assign(key.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10, near: 1, far: 40 });
scene.add(key);
const rim = new THREE.DirectionalLight(0x9fd8ff, 1.4); rim.position.set(-6, 3, -6); scene.add(rim);
const sweep = new THREE.PointLight(0xffffff, 0, 16, 1.3); scene.add(sweep);

// ------------------------------------------------------------------ materials
const M = {
  gold: new THREE.MeshPhysicalMaterial({ color: 0xe0b04a, metalness: 1, roughness: .17, clearcoat: 1, clearcoatRoughness: .06 }),
  goldDark: new THREE.MeshPhysicalMaterial({ color: 0x8a5d1c, metalness: 1, roughness: .3, clearcoat: .6 }),
  silver: new THREE.MeshPhysicalMaterial({ color: 0xc9ced6, metalness: .9, roughness: .22, clearcoat: 1, clearcoatRoughness: .05 }),
  black: new THREE.MeshPhysicalMaterial({ color: 0x0c0c10, metalness: .4, roughness: .35, clearcoat: .5 }),
  darkGlass: new THREE.MeshPhysicalMaterial({ color: 0x0a0d12, metalness: .6, roughness: .04, clearcoat: 1, envMapIntensity: 2.2 }),
  glass: new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: .1, roughness: .03, transparent: true, opacity: .34, iridescence: 1,
    iridescenceIOR: 1.7, iridescenceThicknessRange: [180, 820], envMapIntensity: 2.6, side: THREE.DoubleSide, depthWrite: false }),
  gem: new THREE.MeshPhysicalMaterial({ color: 0xdcecff, metalness: 1, roughness: .02, iridescence: .8, iridescenceIOR: 2.2,
    envMapIntensity: 3.2, flatShading: true }),
  brick: new THREE.MeshStandardMaterial({ color: 0x7a3426, roughness: .82 }),
  stone: new THREE.MeshStandardMaterial({ color: 0xd8ccb4, roughness: .7 }),
  roof: new THREE.MeshStandardMaterial({ color: 0x2c2a33, roughness: .6, metalness: .2 }),
  window: new THREE.MeshStandardMaterial({ color: 0xffc777, emissive: 0xffb04a, emissiveIntensity: 2.2 }),
  lawn: new THREE.MeshStandardMaterial({ color: 0x1f4a2a, roughness: .9 }),
  porcelain: new THREE.MeshPhysicalMaterial({ color: 0xf7f3ea, roughness: .25, clearcoat: 1, clearcoatRoughness: .1 }),
  tea: new THREE.MeshPhysicalMaterial({ color: 0x5a2e12, roughness: .1, clearcoat: 1 }),
  wood: new THREE.MeshPhysicalMaterial({ color: 0x7a3f1c, roughness: .35, clearcoat: 1, clearcoatRoughness: .08 }),
  leatherRed: new THREE.MeshPhysicalMaterial({ color: 0x8c1d26, roughness: .45, clearcoat: .4 }),
  water: new THREE.MeshStandardMaterial({ color: 0x0f4652, metalness: .15, roughness: .28, envMapIntensity: .6 }),
  dial: new THREE.MeshPhysicalMaterial({ color: 0x0d4a35, metalness: .4, roughness: .28, clearcoat: 1 }),
  leather: new THREE.MeshPhysicalMaterial({ color: 0x4a2a16, roughness: .6, clearcoat: .2 }),
  red: new THREE.MeshPhysicalMaterial({ color: 0xc8202c, metalness: .3, roughness: .3 }),
  asphalt: new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: .9 }),
  lineW: new THREE.MeshStandardMaterial({ color: 0xf2efe6, emissive: 0x555555 }),
  head: new THREE.MeshStandardMaterial({ color: 0xfff3d0, emissive: 0xffe6a0, emissiveIntensity: 3 }),
  tail: new THREE.MeshStandardMaterial({ color: 0xff3030, emissive: 0xff2020, emissiveIntensity: 3 }),
  cream: new THREE.MeshPhysicalMaterial({ color: 0xefe6d2, roughness: .35, clearcoat: .6 }),
  emeraldEye: new THREE.MeshStandardMaterial({ color: 0x20ff9a, emissive: 0x10c070, emissiveIntensity: 2 }),
};

const G = {};   // one group per scene
function group(name) { const g = new THREE.Group(); g.visible = false; scene.add(g); G[name] = g; return g; }
function mesh(geo, mat, parent, x = 0, y = 0, z = 0) {
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; parent.add(m); return m;
}
function extrude(points, depth, bevel = .04) {
  const s = new THREE.Shape(points.map(([x, y]) => new THREE.Vector2(x, y)));
  const g = new THREE.ExtrudeGeometry(s, { depth, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 3, curveSegments: 16 });
  g.translate(0, 0, -depth / 2); return g;
}

// ------------------------------------------------------------------ builders
function buildManor() {
  const g = group("manor");
  mesh(new THREE.BoxGeometry(7, 2.4, 1.6), M.brick, g, 0, 1.2, 0);
  mesh(new THREE.BoxGeometry(2, 3.2, 1.9), M.brick, g, 0, 1.6, .2);          // entrance block
  for (const x of [-2.4, 0, 2.4]) {                                          // gables
    const gab = mesh(extrude([[-.9, 0], [.9, 0], [0, 1.1]], 1.6, .02), M.brick, g, x, x === 0 ? 3.2 : 2.4, x === 0 ? .2 : 0);
    gab.scale.z = x === 0 ? 1.18 : 1;
  }
  mesh(new THREE.BoxGeometry(7.2, .12, 1.8), M.stone, g, 0, 2.45, 0);
  for (const x of [-4, 4]) {                                                 // towers with gold-tipped domes
    mesh(new THREE.CylinderGeometry(.55, .6, 3.6, 8), M.brick, g, x, 1.8, 0);
    const dome = mesh(new THREE.SphereGeometry(.62, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2), M.roof, g, x, 3.6, 0);
    dome.scale.y = 1.4;
    mesh(new THREE.ConeGeometry(.12, .9, 8), M.gold, g, x, 4.85, 0);
  }
  for (const x of [-3.2, -1.4, 1.4, 3.2]) mesh(new THREE.BoxGeometry(.28, 1.1, .28), M.brick, g, x, 3.0, -.4);   // chimneys
  const win = new THREE.InstancedMesh(new THREE.PlaneGeometry(.34, .5), M.window, 40);
  let n = 0; const m4 = new THREE.Matrix4();
  for (const row of [.7, 1.75]) for (let i = 0; i < 14; i++) {
    const x = -3.2 + i * .49; if (Math.abs(x) < 1.1) continue;
    m4.makeTranslation(x, row, .81); win.setMatrixAt(n++, m4);
  }
  for (const row of [.8, 1.8, 2.7]) for (const x of [-.5, .5]) { m4.makeTranslation(x, row, 1.16); win.setMatrixAt(n++, m4); }
  win.count = n; g.add(win);
  const lawn = mesh(new THREE.CircleGeometry(30, 48), M.lawn, g, 0, 0, 0); lawn.rotation.x = -Math.PI / 2;
  return g;
}

function buildShades() {
  const g = group("shades");
  const lens = [[-1.05, .45], [1.05, .45], [1.0, -.25], [.6, -.62], [-.6, -.62], [-1.0, -.25]];
  for (const sx of [-1.25, 1.25]) {
    const l = mesh(extrude(lens.map(([x, y]) => [x * .95, y * .95]), .06, .03), M.darkGlass, g, sx, 0, 0);
    const rimShape = new THREE.Shape(lens.map(([x, y]) => new THREE.Vector2(x * 1.08, y * 1.08)));
    rimShape.holes.push(new THREE.Path(lens.map(([x, y]) => new THREE.Vector2(x * .95, y * .95)).reverse()));
    const rg = new THREE.ExtrudeGeometry(rimShape, { depth: .12, bevelEnabled: true, bevelThickness: .03, bevelSize: .02, bevelSegments: 2 });
    rg.translate(0, 0, -.06);
    mesh(rg, M.gold, g, sx, 0, 0);
    l.userData.lens = true;
  }
  const bridge = mesh(new THREE.TorusGeometry(.32, .05, 10, 24, Math.PI), M.gold, g, 0, .35, 0);
  for (const sx of [-1, 1]) {
    const tmp = mesh(new THREE.BoxGeometry(.08, .1, 2.6), M.gold, g, sx * 2.3, .3, -1.25);
    tmp.rotation.y = sx * .05;
  }
  return g;
}

function pathShape(cmds) {   // [["m",x,y], ["l",x,y], ["q",cx,cy,x,y]] -> Shape
  const s = new THREE.Shape();
  for (const [c, ...v] of cmds) { if (c === "m") s.moveTo(...v); else if (c === "l") s.lineTo(...v); else s.quadraticCurveTo(...v); }
  return s;
}
function extrudeShape(shape, depth, bevel, segs = 6) {
  const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: segs, curveSegments: 24 });
  g.translate(0, 0, -depth / 2); return g;
}

function buildCar(name) {
  // a classic 1960s grand tourer: long bonnet, raked screen, fastback
  const g = group(name);
  const body = pathShape([["m", -2.7, .32], ["l", 2.55, .32], ["q", 2.88, .34, 2.86, .62], ["q", 2.8, .88, 2.3, .92], ["l", .8, 1.02],
    ["q", .38, 1.06, .12, 1.44], ["q", -.2, 1.64, -.95, 1.6], ["q", -1.9, 1.52, -2.55, 1.02], ["q", -2.86, .86, -2.82, .56], ["q", -2.8, .34, -2.7, .32]]);
  mesh(extrudeShape(body, 1.3, .2), M.silver, g, 0, 0, 0);
  const win = pathShape([["m", .62, 1.06], ["q", .34, 1.12, .14, 1.4], ["q", -.15, 1.55, -.9, 1.52], ["q", -1.55, 1.46, -1.95, 1.12], ["l", .62, 1.06]]);
  mesh(extrudeShape(win, 1.76, .02, 2), M.darkGlass, g, 0, .03, 0);
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(14, 8), new THREE.ShadowMaterial({ opacity: .28 }));
  shadow.rotation.x = -Math.PI / 2; shadow.receiveShadow = true; g.add(shadow);
  for (const [x, z] of [[1.75, .74], [-1.75, .74], [1.75, -.74], [-1.75, -.74]]) {
    const w = mesh(new THREE.CylinderGeometry(.42, .42, .3, 24), M.black, g, x, .42, z); w.rotation.x = Math.PI / 2;
    const hub = mesh(new THREE.CylinderGeometry(.24, .24, .32, 16), M.silver, g, x, .42, z); hub.rotation.x = Math.PI / 2;
    w.userData.wheel = hub.userData.wheel = true;
  }
  for (const z of [-.5, .5]) {
    mesh(new THREE.SphereGeometry(.13, 12, 10), M.head, g, 2.72, .62, z);
    mesh(new THREE.BoxGeometry(.06, .1, .26), M.tail, g, -2.83, .7, z);
  }
  mesh(new THREE.BoxGeometry(.06, .08, 1.4), M.gold, g, 2.8, .4, 0);
  return g;
}

function buildPolo() {
  const g = group("polo");
  const ball = mesh(new THREE.SphereGeometry(.45, 32, 24), M.cream, g, 0, 0, 0); ball.name = "ball";
  const mallet = new THREE.Group(); g.add(mallet); mallet.name = "mallet";
  mesh(new THREE.CylinderGeometry(.05, .06, 5, 12), M.wood, mallet, 0, 2.5, 0);
  const headM = mesh(new THREE.CylinderGeometry(.22, .22, 1.2, 20), M.wood, mallet, 0, 0, 0); headM.rotation.z = Math.PI / 2;
  mesh(new THREE.CylinderGeometry(.08, .08, .5, 12), M.gold, mallet, 0, 4.9, 0);
  const lawn = mesh(new THREE.PlaneGeometry(60, 60), M.lawn, g, 0, -.45, 0); lawn.rotation.x = -Math.PI / 2;
  return g;
}

function buildTea() {
  const g = group("tea");
  const cup = [[0, 0], [.55, 0], [.62, .06], [.75, .3], [.98, .9], [1.08, 1.3], [1.04, 1.32], [.95, .95], [.72, .38], [0, .28]];
  mesh(new THREE.LatheGeometry(cup.map(([x, y]) => new THREE.Vector2(x, y)), 48), M.porcelain, g, 0, .1, 0);
  const rimT = mesh(new THREE.TorusGeometry(1.06, .025, 8, 64), M.gold, g, 0, 1.42, 0); rimT.rotation.x = Math.PI / 2;
  const tea = mesh(new THREE.CircleGeometry(.98, 48), M.tea, g, 0, 1.22, 0); tea.rotation.x = -Math.PI / 2;
  const handle = mesh(new THREE.TorusGeometry(.32, .07, 12, 24, Math.PI * 1.3), M.porcelain, g, 1.1, .85, 0); handle.rotation.z = -Math.PI * .65;
  const saucer = [[0, 0], [1.2, 0], [1.6, .08], [1.95, .22], [1.9, .26], [1.5, .14], [0, .1]];
  mesh(new THREE.LatheGeometry(saucer.map(([x, y]) => new THREE.Vector2(x, y)), 64), M.porcelain, g, 0, 0, 0);
  const rimS = mesh(new THREE.TorusGeometry(1.93, .025, 8, 80), M.gold, g, 0, .25, 0); rimS.rotation.x = Math.PI / 2;
  // steam: soft sprites rising
  const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d");
  const gr = x.createRadialGradient(64, 64, 4, 64, 64, 64); gr.addColorStop(0, "rgba(255,255,255,.55)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  x.fillStyle = gr; x.fillRect(0, 0, 128, 128);
  const smat = new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false });
  g.userData.steam = [];
  for (let i = 0; i < 10; i++) { const s = new THREE.Sprite(smat.clone()); g.add(s); g.userData.steam.push(s); }
  return g;
}

function buildBoat() {
  const g = group("boat");
  const hull = pathShape([["m", -3, .3], ["l", 2.1, .3], ["q", 3.2, .45, 3.55, 1.18], ["l", -3.05, 1.18], ["l", -3, .3]]);
  mesh(extrudeShape(hull, 1.6, .16), M.wood, g, 0, 0, 0);
  mesh(new THREE.BoxGeometry(5.4, .05, 1.7), M.cream, g, -.2, 1.22, 0);
  for (const x of [-2.1, -.9]) mesh(new THREE.BoxGeometry(.8, .5, 1.5), M.leatherRed, g, x, 1.45, 0);
  const ws = mesh(new THREE.BoxGeometry(.05, .55, 1.6), M.glass, g, .4, 1.5, 0); ws.rotation.z = .4;
  mesh(new THREE.BoxGeometry(.06, .06, 1.7), M.silver, g, .55, 1.78, 0);
  const water = mesh(new THREE.PlaneGeometry(80, 80, 60, 60), M.water, g, 0, .45, 0); water.rotation.x = -Math.PI / 2; water.name = "water";
  water.castShadow = false;
  return g;
}

function buildWatch() {
  const g = group("watch");
  const caseM = mesh(new THREE.CylinderGeometry(1.3, 1.3, .38, 64), M.gold, g); caseM.rotation.x = Math.PI / 2;
  const bezel = mesh(new THREE.TorusGeometry(1.25, .1, 16, 72), M.gold, g, 0, 0, .19);
  const dial = mesh(new THREE.CylinderGeometry(1.15, 1.15, .02, 64), M.dial, g, 0, 0, .2); dial.rotation.x = Math.PI / 2;
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * Math.PI * 2;
    const ix = mesh(new THREE.BoxGeometry(i % 3 ? .06 : .1, .24, .03), M.gold, g, Math.sin(a) * .92, Math.cos(a) * .92, .23);
    ix.rotation.z = -a;
  }
  const mk = (len, wid, mat, z) => { const p = new THREE.Group(); p.position.z = z; g.add(p); mesh(new THREE.BoxGeometry(wid, len, .02), mat, p, 0, len / 2 - .1, 0); return p; };
  g.userData.hh = mk(.6, .09, M.gold, .25); g.userData.mh = mk(.9, .06, M.gold, .27); g.userData.sh = mk(1.0, .02, M.red, .29);
  mesh(new THREE.CylinderGeometry(.06, .06, .05, 16), M.gold, g, 0, 0, .3).rotation.x = Math.PI / 2;
  const crystal = mesh(new THREE.CylinderGeometry(1.17, 1.17, .04, 64), M.glass, g, 0, 0, .32); crystal.rotation.x = Math.PI / 2;
  const crown = mesh(new THREE.CylinderGeometry(.13, .13, .22, 16), M.gold, g, 1.42, 0, 0); crown.rotation.z = Math.PI / 2;
  for (const s of [1, -1]) mesh(new THREE.BoxGeometry(1.1, 2.4, .14), M.leather, g, 0, s * 2.35, -.05);
  return g;
}

function buildDiamond() {
  const g = group("diamond");
  const crown = mesh(new THREE.CylinderGeometry(.72, 1.25, .5, 16, 1), M.gem, g, 0, .25, 0);
  const pav = mesh(new THREE.ConeGeometry(1.25, 1.5, 16, 1), M.gem, g, 0, -.75, 0); pav.rotation.x = Math.PI;
  crown.castShadow = pav.castShadow = false;
  return g;
}

function buildRings() {
  const g = group("rings");
  const a = mesh(new THREE.TorusGeometry(1.1, .16, 24, 80), M.gold, g, -.55, 0, 0);
  const b = mesh(new THREE.TorusGeometry(1.1, .16, 24, 80), M.gold, g, .55, 0, 0); b.rotation.y = Math.PI / 2.4;
  const st = mesh(new THREE.OctahedronGeometry(.28, 0), M.gem, b, 0, 1.3, 0); st.castShadow = false;
  return g;
}

function buildRoad() {
  const g = group("road");
  const road = mesh(new THREE.PlaneGeometry(8, 200), M.asphalt, g, 0, 0, -90); road.rotation.x = -Math.PI / 2;
  const dash = new THREE.InstancedMesh(new THREE.BoxGeometry(.18, .02, 2), M.lineW, 60);
  const m4 = new THREE.Matrix4();
  for (let i = 0; i < 60; i++) { m4.makeTranslation(0, .02, 8 - i * 3.5); dash.setMatrixAt(i, m4); }
  g.add(dash); g.userData.dash = dash;
  const stones = new THREE.InstancedMesh(new THREE.DodecahedronGeometry(.25, 0), M.stone, 80);
  for (let i = 0; i < 80; i++) {
    const s = .5 + hash(i) * 1.4;
    m4.compose(V((hash(i + 1) - .5) * 7.4, .1, 8 - hash(i + 2) * 190), new THREE.Quaternion().setFromEuler(new THREE.Euler(hash(i) * 3, hash(i + 3) * 3, 0)), V(s, s * .6, s));
    stones.setMatrixAt(i, m4);
  }
  stones.castShadow = true; g.add(stones); g.userData.stones = stones;
  return g;
}

function buildChess() {
  const g = group("chess");
  const prof = [[0, 0], [1.0, 0], [1.0, .22], [.8, .32], [.55, .5], [.42, 1.5], [.36, 2.6], [.62, 2.75], [.62, 2.9], [.4, 3.0], [.55, 3.5], [.3, 3.75], [0, 3.8]];
  const king = mesh(new THREE.LatheGeometry(prof.map(([x, y]) => new THREE.Vector2(x, y)), 48), M.gold, g, 0, 0, 0);
  mesh(new THREE.BoxGeometry(.14, .6, .14), M.gold, g, 0, 4.05, 0);
  mesh(new THREE.BoxGeometry(.45, .14, .14), M.gold, g, 0, 4.12, 0);
  const sq = new THREE.InstancedMesh(new THREE.BoxGeometry(1.2, .12, 1.2), M.cream, 64);
  const sqd = new THREE.InstancedMesh(new THREE.BoxGeometry(1.2, .12, 1.2), M.black, 64);
  const m4 = new THREE.Matrix4(); let a = 0, b = 0;
  for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) {
    m4.makeTranslation((i - 3.5) * 1.2, -.06, (j - 3.5) * 1.2);
    if ((i + j) % 2) sqd.setMatrixAt(b++, m4); else sq.setMatrixAt(a++, m4);
  }
  sq.count = a; sqd.count = b; sq.receiveShadow = sqd.receiveShadow = true; g.add(sq, sqd);
  g.userData.king = king;
  return g;
}

function buildSnake() {
  const g = group("snake");
  const pts = [];
  for (let i = 0; i <= 120; i++) {
    const u = i / 120, a = u * Math.PI * 5;
    pts.push(V(Math.cos(a) * (2.6 - u * 1.4), -1.6 + u * 3.4, Math.sin(a) * (2.6 - u * 1.4)));
  }
  const curve = new THREE.CatmullRomCurve3(pts);
  const geo = new THREE.TubeGeometry(curve, 600, .26, 16, false);
  const body = mesh(geo, M.gold, g); g.userData.body = body; g.userData.curve = curve;
  const headG = new THREE.Group(); g.add(headG); g.userData.head = headG;
  const hd = mesh(new THREE.SphereGeometry(.34, 20, 16), M.gold, headG); hd.scale.set(1.25, .8, 1.6);
  for (const s of [-1, 1]) mesh(new THREE.SphereGeometry(.07, 10, 8), M.emeraldEye, headG, s * .2, .14, .3);
  return g;
}

let title = null;
const N = 150, NG = 24;
const shards = new THREE.InstancedMesh(new THREE.CylinderGeometry(.34, .34, .03, 3), M.glass, N);
const golds = new THREE.InstancedMesh(new THREE.CylinderGeometry(.12, .12, .03, 3), M.gold, NG);
shards.castShadow = golds.castShadow = false;
scene.add(shards, golds);
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _s = new THREE.Vector3(), _p = new THREE.Vector3();

async function build() {
  const data = await new TTFLoader().loadAsync("assets/fonts/PlayfairDisplay/PlayfairDisplay-900Italic.ttf");
  const font = new Font(data);
  const geo = new TextGeometry("Ashke", { font, size: 1.55, depth: .34, curveSegments: 10, bevelEnabled: true, bevelThickness: .05, bevelSize: .035, bevelSegments: 5 });
  geo.computeBoundingBox();
  const bb = geo.boundingBox;
  geo.translate(-(bb.max.x + bb.min.x) / 2, -(bb.max.y + bb.min.y) / 2, -(bb.max.z + bb.min.z) / 2);
  title = new THREE.Mesh(geo, [M.gold, M.goldDark]);
  scene.add(title);
  buildManor(); buildShades(); buildCar("car"); buildPolo(); buildTea(); buildBoat(); buildWatch(); buildDiamond(); buildRings();
  buildRoad(); G.road.add(buildCar("roadcar")); G.roadcar.visible = true; buildChess(); buildSnake();
}

function burstPose(i, k, spread) {
  const a = hash(i) * Math.PI * 2, r = (.4 + hash(i + 3) * 1.2) * spread * eOut(k);
  _p.set(Math.cos(a) * r * 1.7, Math.sin(a) * r, -2 + 14 * eIn(k) * (.5 + hash(i + 5)));
  _e.set(k * 9 * hash(i + 1), k * 7 * hash(i + 2), hash(i) * 6); _q.setFromEuler(_e);
  const s = (.5 + hash(i + 7) * 1.4) * Math.min(1, k * 6) * (1 - lin(k, .75, 1)); _s.set(s, s, s);
  return _m.compose(_p, _q, _s);
}
function orbitPose(i, t, k, c = V(0, 0, 0)) {
  const a = hash(i) * Math.PI * 2 + t * (.35 + hash(i + 9) * .5), rr = 3.2 + hash(i + 4) * 3.4;
  _p.set(c.x + Math.cos(a) * rr * 1.25, c.y + Math.sin(a * 1.3) * 1.6 + (hash(i + 6) - .5) * 2.5, c.z + Math.sin(a) * rr - 1.5);
  _e.set(t * (.6 + hash(i + 1)), t * (.8 + hash(i + 2)), hash(i) * 6); _q.setFromEuler(_e);
  const s = (.4 + hash(i + 7) * 1.1) * k; _s.set(s, s, s);
  return _m.compose(_p, _q, _s);
}

// camera angles per scene: [position, look-at]; the camera cuts to the next one every two beats and dollies slowly
const CAMS = {
  manor: [[V(0, 2.2, 14), V(0, 2, 0)], [V(-9, 1.2, 8), V(0, 2.2, 0)], [V(6, .6, 5), V(2, 2.6, 0)], [V(0, 6, 9), V(0, 1.5, 0)]],
  shades: [[V(0, 0, 8), V(0, 0, 0)], [V(-4, 1.5, 5.5), V(0, 0, 0)], [V(3, -1, 5), V(0, .2, 0)]],
  car: [[V(0, 1.6, 10), V(0, .8, 0)], [V(7, .9, 4), V(0, .8, 0)], [V(-5, 3, 6), V(0, .6, 0)], [V(3.8, .5, 2.4), V(2.6, .6, 0)]],
  polo: [[V(0, .6, 7), V(0, .4, 0)], [V(-5, 1.2, 4), V(0, 1, 0)], [V(3, 3, 6), V(0, .5, 0)]],
  tea: [[V(0, 3, 7), V(0, .8, 0)], [V(3.5, 1.4, 4), V(0, 1, 0)], [V(-2.5, 4.5, 3), V(0, .8, 0)]],
  boat: [[V(-8, 3, 9), V(0, 1, 0)], [V(6, 1.6, 5), V(0, 1.2, 0)], [V(0, 6, 10), V(0, 1, 0)]],
  watch: [[V(0, 0, 6.5), V(0, 0, 0)], [V(-3, 2, 4), V(0, 0, 0)], [V(2.4, -1.4, 3.6), V(.2, .2, 0)]],
  diamond: [[V(0, 1, 6), V(0, 0, 0)], [V(-3, 2.5, 4), V(0, 0, 0)], [V(2.5, -1, 4), V(0, 0, 0)]],
  rings: [[V(0, .5, 6), V(0, 0, 0)], [V(-3.4, 2, 4), V(0, 0, 0)], [V(3, -1.5, 4.5), V(0, 0, 0)]],
  road: [[V(0, 1.4, 9), V(0, .8, -4)], [V(3.5, .6, 3), V(0, .8, -2)], [V(-2.4, 5, 7), V(0, .5, -3)]],
  chess: [[V(0, 3, 9), V(0, 2, 0)], [V(-4, 1, 5), V(0, 2.4, 0)], [V(3, 6, 6), V(0, 2, 0)]],
  snake: [[V(0, 1, 9), V(0, 0, 0)], [V(-5, 3, 5), V(0, .5, 0)], [V(4, -1, 6), V(0, .3, 0)]],
  title: [[V(0, 0, 12), V(0, 0, 0)]],
};

function sceneAt(t) { return T.scenes.find((s) => t >= s.a && t < s.b) || T.scenes[T.scenes.length - 1]; }

function renderAt(t) {
  if (!title) return;
  for (const k in G) if (k !== "roadcar") G[k].visible = false;
  title.visible = false; shards.visible = golds.visible = false; sweep.intensity = 0;
  const sc = sceneAt(t), k = sc.k;
  const local = t - sc.a;
  const step = 2 * T.period;
  let camK = k === "intro" || k === "finale" ? "title" : k;
  const cams = CAMS[camK];
  const ci = Math.floor(local / step) % cams.length;
  const cut = local - Math.floor(local / step) * step;
  const [cp, cl_] = cams[ci];
  const dolly = 1 - .06 * (cut / step);
  camera.position.copy(cl_).add(cp.clone().sub(cl_).multiplyScalar(dolly));
  camera.position.x += Math.sin(t * .7) * .08; camera.position.y += Math.cos(t * .6) * .05;
  camera.lookAt(cl_);
  // the beat nudges the camera forward a little
  for (const b of T.beats) if (t >= b && t < b + .25) { const d = .05 * Math.exp(-(t - b) * 14); camera.position.lerp(cl_, d); }
  const pop = eBack(lin(local, 0, .35));   // each scene's hero object pops in

  if (k === "intro" || k === "finale") {
    title.visible = true;
    if (k === "intro") {
      const kin = eOut(lin(t, sc.a, sc.a + .7)), kout = eIn(lin(t, sc.b - .35, sc.b + .1));
      title.position.set(0, .2, -26 * (1 - kin) + 13 * kout);
      title.rotation.set(.25 * (1 - kin), -.9 * (1 - kin) + .12 * Math.sin(t * 1.8), -.06);
      title.scale.setScalar(1.25);
    } else {
      const kk = eOut(lin(t, sc.a, sc.a + .6));
      title.position.set(0, .4, -30 * (1 - kk));
      title.rotation.set(.18 * (1 - kk), 1.4 * (1 - kk) + .1 * Math.sin(t * 1.5), -.05);
      title.scale.setScalar(1.15 + .05 * Math.sin(t * 2));
      shards.visible = golds.visible = true;
      const ko = eOut(lin(t, sc.a, sc.a + .8));
      for (let i = 0; i < N; i++) shards.setMatrixAt(i, orbitPose(i, t, ko));
      for (let i = 0; i < NG; i++) golds.setMatrixAt(i, orbitPose(i + 500, t, ko * 1.6));
      shards.instanceMatrix.needsUpdate = golds.instanceMatrix.needsUpdate = true;
    }
    sweep.intensity = 100 * Math.sin(Math.PI * lin(local, .3, 1.4)); sweep.position.set(-6 + 12 * lin(local, .3, 1.4), 1.5, 3);
  } else {
    const g = G[k]; g.visible = true;
    g.position.set(0, 0, 0); g.rotation.set(0, 0, 0); g.scale.setScalar(1);
    if (k === "manor") { g.scale.setScalar(.6 + .4 * pop); }
    if (k === "shades") { g.rotation.set(.1 * Math.sin(t), t * 1.1 + (1 - pop) * 4, .05 * Math.sin(t * 1.3)); g.scale.setScalar(pop); }
    if (k === "car") {
      const kk = eOut(lin(local, 0, .7)); g.position.x = -14 * (1 - kk);
      g.children.forEach((c) => { if (c.userData.wheel) c.rotation.y = -t * 12; });
    }
    if (k === "polo") {
      const mal = g.getObjectByName("mallet"), ball = g.getObjectByName("ball");
      const per = T.period * 2, ph = (local % per) / per;
      mal.position.set(-1.1, 0, 0); mal.rotation.z = -.9 + 1.6 * eInOut(cl(ph * 2.2));   // swing every two beats
      const hit = cl((ph - .45) / .55);
      ball.position.set(hit * 7, Math.sin(Math.PI * hit) * 1.6, -hit * 2); ball.rotation.set(t * 8, t * 6, 0);
    }
    if (k === "tea") {
      g.rotation.y = t * .25; g.scale.setScalar(pop);
      g.userData.steam.forEach((s, i) => {
        const u = ((t * .35 + i / 10) % 1);
        s.position.set(Math.sin(u * 6 + i) * .25, 1.4 + u * 2.4, Math.cos(u * 5 + i) * .2);
        s.scale.setScalar(.4 + u * 1.4); s.material.opacity = .5 * Math.sin(Math.PI * u);
      });
    }
    if (k === "boat") {
      g.children.forEach((c) => { if (c.name !== "water") c.position.y += 0; });
      g.rotation.y = -.25; g.position.y = .06 * Math.sin(t * 2.2);
      const water = g.getObjectByName("water"); water.position.x = (t * 3) % 2;
    }
    if (k === "watch") {
      g.rotation.set(-.15 + .1 * Math.sin(t * .8), .35 * Math.sin(t * .6) + (1 - pop) * 3, 0); g.scale.setScalar(pop);
      const sec = Math.floor(t * 2) / 2;
      g.userData.sh.rotation.z = -sec * Math.PI / 30; g.userData.mh.rotation.z = -t * .06 - 1.2; g.userData.hh.rotation.z = -t * .005 - 2.6;
    }
    if (k === "diamond") {
      g.rotation.set(.2, t * 1.4, .1 * Math.sin(t)); g.scale.setScalar(pop * (1 + .04 * Math.sin(t * 6)));
      if (t >= T.daaka) g.visible = false;   // it shatters on "daaka"
    }
    if (k === "rings") { g.rotation.set(.3 * Math.sin(t * .7), t * .9, .2); g.scale.setScalar(pop); }
    if (k === "road") {
      const car = G.roadcar; car.visible = true; car.rotation.y = Math.PI / 2; car.position.set(0, 0, 0);
      car.children.forEach((c) => { if (c.userData.wheel) c.rotation.y = -t * 16; });
      g.userData.dash.position.z = (t * 22) % 3.5;
      g.userData.stones.position.z = local * 22;
    }
    if (k === "chess") {
      const kk = eBack(lin(local, 0, .45)); g.userData.king.position.y = -4 * (1 - kk); g.userData.king.rotation.y = t * .6;
      g.rotation.y = .3;
    }
    if (k === "snake") {
      const grow = eOut(lin(local, 0, 2.2));
      const body = g.userData.body; body.geometry.setDrawRange(0, Math.floor(body.geometry.index.count * grow / 6) * 6);
      const p = g.userData.curve.getPointAt(Math.max(.001, grow * .999)), tg = g.userData.curve.getTangentAt(Math.max(.001, grow * .999));
      g.userData.head.position.copy(p); g.userData.head.lookAt(p.clone().add(tg));
      g.rotation.y = t * .4;
    }
  }
  // section changes: glass shards burst towards the camera
  for (const p of T.panes) {
    if (t >= p - .25 && t < p + 1.0) {
      const kk = lin(t, p - .25, p + 1.0);
      shards.visible = golds.visible = true;
      const c0 = camera.position.clone(), fwd = new THREE.Vector3(); camera.getWorldDirection(fwd);
      for (let i = 0; i < N; i++) { burstPose(i, kk, 7); _m.premultiply(new THREE.Matrix4().lookAt(V(0, 0, 0), fwd, V(0, 1, 0)).setPosition(c0.clone().add(fwd.clone().multiplyScalar(10)))); shards.setMatrixAt(i, _m); }
      for (let i = 0; i < NG; i++) { burstPose(i + 300, kk, 6); _m.premultiply(new THREE.Matrix4().lookAt(V(0, 0, 0), fwd, V(0, 1, 0)).setPosition(c0.clone().add(fwd.clone().multiplyScalar(10)))); golds.setMatrixAt(i, _m); }
      shards.instanceMatrix.needsUpdate = golds.instanceMatrix.needsUpdate = true;
    }
  }
  // a light sweep across each new hero object
  if (k !== "intro" && k !== "finale") { sweep.intensity = 70 * Math.sin(Math.PI * lin(local, .1, .9)); sweep.position.set(-5 + 10 * lin(local, .1, .9), 2, 4); }
  renderer.render(scene, camera);
  out2d.clearRect(0, 0, W, H);
  out2d.drawImage(canvas, 0, 0);
}

const ready = (async () => {
  await build();
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["akworld"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
