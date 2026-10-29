// The haunted-house explainer: the 3D world. Everything is a pure function of time t (seconds), rendered on HyperFrames'
// hf-seek. The production database is a Victorian house at 3:07 AM; every room is a table and its rows are candles.
// DROP DATABASE lets a sheet ghost loose: it drifts through the rooms and snuffs them out. The backups lie under a
// gravestone in the yard ("d. 3 MARCH"). In the attic, the pixel mascot's lantern finds the copy (a glowing chest).
// The three steps: a polaroid flash before the ghost reaches a room, a warded front door marked PRODUCTION, a
// grandfather clock that rings when the backup is stale. The twist boards and padlocks the house: read-only.
// Around it: rain, bats, lightning (a figure by the tree shows only in the flash), eyes in the windows that went dark.
// Cue times come from the voiceover (window.HH_T, build/generate.py); the 2D explainer layer sits over this canvas.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const T = window.HH_T;
const L = T.l, E = T.e, SC = T.scenes;
const W = 1080, H = 1920;

// WebGL draws off-screen and each frame is copied into the page's 2D canvas: under HyperFrames' software compositing a
// WebGL canvas in the page loses a band (the flipped rect of whatever 2D element repainted) in some frames
const glEl = document.getElementById("gl"); glEl.width = W; glEl.height = H;
const out2d = glEl.getContext("2d");
const canvas = document.createElement("canvas"); canvas.width = 1080; canvas.height = 1920;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance", preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.3;

const scene = new THREE.Scene();
const SKY = new THREE.Color(0x070a14);
scene.background = SKY.clone();
scene.fog = new THREE.FogExp2(0x0b1020, .035);
const camera = new THREE.PerspectiveCamera(45, W / H, .05, 200);

// ---------------------------------------------------------------- post: bloom, then a cold horror grade (grain, vignette)
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .8, .6, .62);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uGrain: { value: .06 }, uVig: { value: 1.1 }, uSat: { value: .8 },
    uTint: { value: new THREE.Vector3(.92, .98, 1.1) }, uFlash: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uGrain, uVig, uSat, uFlash; uniform vec3 uTint; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec3 col = texture2D(tDiffuse, vUv).rgb;
      float l = dot(col, vec3(.299, .587, .114));
      col = mix(vec3(l), col, uSat) * uTint;
      col += (h(floor(vUv * vec2(540., 960.)) + fract(uTime * 7.13) * 97.) - .5) * uGrain;
      vec2 c = (vUv - .5) * vec2(1., .72);
      col *= 1. - uVig * dot(c, c) * 1.5;
      col = mix(col, vec3(.85, .9, 1.), uFlash * .55);
      gl_FragColor = vec4(col, 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const easeIO = (k) => (k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const easeOut = (k) => 1 - Math.pow(1 - k, 3);
const win = (t, a, b) => clamp((t - a) / (b - a));
const pulse = (t, at, up = .08, down = .35) => (t < at ? 0 : t < at + up ? (t - at) / up : Math.max(0, 1 - (t - at - up) / down));
const between = (t, a, b) => t >= a && t < b;
const rb = (w, h, d, r = .04, seg = 2) => new RoundedBoxGeometry(w, h, d, seg, Math.min(r, w / 2 - .001, h / 2 - .001, d / 2 - .001));
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .85, metalness: 0, ...o });
const glow = (color, k = 3, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(k), toneMapped: false, ...o });
const mesh = (geo, m) => new THREE.Mesh(geo, m);
function hash(i) { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
function grp(parent, x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); if (parent) parent.add(g); return g; }
const at = (o, x, y, z) => { o.position.set(x, y, z); return o; };
const lerpV = (a, b, k) => a.map((x, i) => lerp(x, b[i], k));
function canvasTex(w, h, draw, nearest = false) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); draw(g, w, h);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  if (nearest) { tx.magFilter = THREE.NearestFilter; tx.minFilter = THREE.NearestFilter; tx.generateMipmaps = false; }
  return tx;
}
const glowTex = canvasTex(128, 128, (g, w) => {
  const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(.35, "rgba(255,255,255,.45)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr; g.fillRect(0, 0, w, w);
});
glowTex.colorSpace = THREE.NoColorSpace;
const addM = (c, k = 1, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), transparent: true, depthWrite: false,
  blending: THREE.AdditiveBlending, toneMapped: false, ...o });
function halo(size, color, k = .4) { return new THREE.Mesh(new THREE.PlaneGeometry(size, size), addM(color, k, { map: glowTex })); }
function write(g, s, x, y, size, o = {}) {
  g.font = `${o.i ? "italic " : ""}${o.w || 700} ${size}px ${o.f || "JBMono"}`; g.fillStyle = o.c || "#e8e0d0"; g.textAlign = o.a || "center"; g.textBaseline = "middle";
  g.fillText(s, x, y, o.max);
}
const tM = new THREE.Matrix4(), tP = new THREE.Vector3(), tQ = new THREE.Quaternion(), tS = new THREE.Vector3();
const CORAL = 0xff6a4a, CANDLE = 0xffb35c, MOON = 0x9fb8ff, GHOST = 0xdfe8ff;

// ---------------------------------------------------------------- light
const hemi = new THREE.HemisphereLight(0x6a7cae, 0x0c0c14, .7); scene.add(hemi);
const moonLight = new THREE.DirectionalLight(MOON, 2.0); moonLight.position.set(-8, 14, 10); scene.add(moonLight);
const flashLight = new THREE.DirectionalLight(0xdfe8ff, 0); flashLight.position.set(4, 12, 12); scene.add(flashLight);
const twistFill = new THREE.DirectionalLight(0x9fb0e0, 0); twistFill.position.set(2, 4, 12); scene.add(twistFill);

// ---------------------------------------------------------------- the yard: ground, moon, dead trees, fence, gravestone, fog
const ground = mesh(new THREE.PlaneGeometry(120, 120).rotateX(-Math.PI / 2), std(0x0d1016)); scene.add(ground);
const moon = mesh(new THREE.SphereGeometry(2.2, 32, 16), glow(0xdfe6ff, 1.6, { fog: false })); moon.position.set(9, 21, -40); scene.add(moon);
const moonHalo = halo(22, 0x8fa8ff, .45); moonHalo.material.fog = false; moonHalo.position.copy(moon.position).add(new THREE.Vector3(0, 0, .5)); scene.add(moonHalo);
const barkM = std(0x07080b);
const TREES = [];
function tree(x, z, s, seed) {
  const g = grp(scene, x, 0, z); g.scale.setScalar(s); TREES.push(g);
  const branch = (parent, len, rad, depth, sd) => {
    const b = mesh(new THREE.CylinderGeometry(rad * .6, rad, len, 5).translate(0, len / 2, 0), barkM); parent.add(b);
    if (depth > 0) for (let i = 0; i < 2 + (depth > 1 ? 1 : 0); i++) {
      const c = grp(b, 0, len * (.55 + hash(sd + i) * .4), 0);
      c.rotation.set((hash(sd + i * 3) - .5) * 1.6, hash(sd + i * 7) * 6.28, (hash(sd + i * 5) - .5) * 1.8);
      branch(c, len * .62, rad * .6, depth - 1, sd * 3 + i + 1);
    }
  };
  branch(g, 2.4, .16, 3, seed);
}
tree(-7.5, -1, 1.5, 3); tree(7.8, -2, 1.7, 9); tree(-10, 4, 1.2, 17); tree(10.5, 5, 1.1, 23);
const fenceM = std(0x050608);
for (let i = 0; i < 26; i++) {
  const x = -12.5 + i;
  if (Math.abs(x) < 1.6) continue;
  const p = mesh(new THREE.BoxGeometry(.06, 1.1, .06), fenceM); p.position.set(x, .55, 7.5); scene.add(p);
  const tip = mesh(new THREE.ConeGeometry(.07, .18, 4), fenceM); tip.position.set(x, 1.18, 7.5); scene.add(tip);
}
const rail = mesh(new THREE.BoxGeometry(25, .05, .05), fenceM); rail.position.set(0, .95, 7.5); scene.add(rail);
// the gravestone: the backups
const graveTex = canvasTex(512, 640, (g, w, h) => {
  g.fillStyle = "#4a4d55"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(${hash(i) > .5 ? 255 : 0},${hash(i) > .5 ? 255 : 0},${hash(i) > .5 ? 255 : 0},${.03 + hash(i + 9) * .05})`; g.fillRect(hash(i + 1) * w, hash(i + 2) * h, 6, 6); }
  write(g, "R.I.P.", w / 2, 150, 54, { f: "Manrope", w: 800, c: "#24262c" });
  write(g, "BACKUPS", w / 2, 290, 86, { f: "Manrope", w: 800, c: "#1a1c21" });
  write(g, "d. 3 MARCH", w / 2, 410, 58, { f: "JBMono", w: 700, c: "#24262c" });
  write(g, "nobody checked", w / 2, 510, 40, { f: "JBMono", w: 400, c: "#2c2f36" });
});
const grave = grp(scene, -4.6, 0, 3.4); grave.rotation.y = .35;
grave.add(at(mesh(new THREE.BoxGeometry(1.5, 1.6, .28), [std(0x5a5e68), std(0x5a5e68), std(0x5a5e68), std(0x5a5e68), std(0xffffff, { map: graveTex }), std(0x5a5e68)]), 0, .8, 0));
const graveLight = new THREE.PointLight(0xb8c8f0, 0, 7, 1.4); graveLight.position.set(-3.4, 2.4, 5.8); scene.add(graveLight);
const graveTop = mesh(new THREE.CylinderGeometry(.75, .75, .28, 24, 1, false, Math.PI / 2, Math.PI), std(0x5a5e68));
graveTop.rotation.x = Math.PI / 2; graveTop.position.set(0, 1.6, 0); grave.add(graveTop);
grave.add(at(mesh(new THREE.BoxGeometry(1.8, .12, 1.1), std(0x15171c)), 0, .06, .5));
const FOG_N = 34;
const fogM = addM(0x8ea0c8, .085, { map: glowTex });
const fogI = new THREE.InstancedMesh(new THREE.PlaneGeometry(1, 1), fogM, FOG_N); fogI.frustumCulled = false; scene.add(fogI);

// ---------------------------------------------------------------- the house: a Victorian cross-section, 3 floors and an attic
const HW = 6, HD = 3, FH = 2.6, ATT = 7.8, RIDGE = 10.6;
const house = grp(scene, 0, 0, 0);
const wallM = std(0x2a1f22), wallM2 = std(0x1f2a26), wallM3 = std(0x262033), floorM = std(0x1c1410), trimM = std(0x0b0a0d);
const ROOMS = [   // a table per room; the hall holds the clock
  { name: "hall", f: 0, s: -1, paper: 0x2b2420 }, { name: "users", f: 0, s: 1, paper: 0x2a1f22 },
  { name: "orders", f: 1, s: -1, paper: 0x1f2a26 }, { name: "payments", f: 1, s: 1, paper: 0x262033 },
  { name: "sessions", f: 2, s: -1, paper: 0x2c2218 }, { name: "invoices", f: 2, s: 1, paper: 0x1e2430 },
];
const roomC = (r) => [r.s * HW / 4, r.f * FH + FH / 2, -HD / 2];
// floors and inner walls
for (let f = 0; f <= 3; f++) house.add(at(mesh(new THREE.BoxGeometry(HW + .3, .16, HD + .2), floorM), 0, f * FH, -HD / 2));
for (const r of ROOMS) {
  const [cx, cy] = roomC(r);
  const paper = canvasTex(256, 256, (g, w, h) => {
    g.fillStyle = "#" + r.paper.toString(16).padStart(6, "0"); g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,230,200,.05)";
    for (let y = 0; y < h; y += 32) for (let x = (y / 32) % 2 * 16; x < w; x += 32) { g.beginPath(); g.arc(x, y, 5, 0, 7); g.fill(); }
  });
  paper.wrapS = paper.wrapT = THREE.RepeatWrapping; paper.repeat.set(3, 2.6);
  house.add(at(mesh(new THREE.PlaneGeometry(HW / 2, FH), std(0xffffff, { map: paper })), cx, cy, -HD + .01));
  r.light = new THREE.PointLight(CANDLE, 0, 6, 1.4); r.light.position.set(cx, cy + .4, -HD / 2 + .3); house.add(r.light);
  if (r.name !== "hall") {
    const sign = canvasTex(320, 96, (g, w, h) => {
      g.fillStyle = "#16100c"; g.beginPath(); g.roundRect(4, 4, w - 8, h - 8, 14); g.fill();
      g.strokeStyle = "#8a6a3c"; g.lineWidth = 5; g.stroke(); write(g, r.name, w / 2, h / 2 + 2, 46, { c: "#e8c890", w: 700 });
    });
    r.sign = at(mesh(new THREE.PlaneGeometry(.95, .29), std(0xffffff, { map: sign, emissive: 0x332211, emissiveMap: sign })), cx, cy + .95, -HD + .03);
    house.add(r.sign);
  }
}
for (let f = 0; f < 3; f++) house.add(at(mesh(new THREE.BoxGeometry(.14, FH, HD), trimM), 0, f * FH + FH / 2, -HD / 2));
for (const s of [-1, 1]) house.add(at(mesh(new THREE.BoxGeometry(.18, ATT, HD + .2), std(0x16121a)), s * (HW / 2 + .04), ATT / 2, -HD / 2));
house.add(at(mesh(new THREE.PlaneGeometry(HW, ATT), std(0x140f12)), 0, ATT / 2, -HD - .02));
// attic: two roof slopes and a back gable
const slope = Math.atan2(RIDGE - ATT, HW / 2 + .5);
const slopeLen = Math.hypot(RIDGE - ATT, HW / 2 + .5);
const roofM = std(0x1a1822, { side: THREE.DoubleSide });
for (const s of [-1, 1]) {
  const r = mesh(new THREE.BoxGeometry(slopeLen + .2, .12, HD + .6), roofM);
  r.position.set(s * (HW / 4 + .25), (ATT + RIDGE) / 2, -HD / 2); r.rotation.z = -s * slope; house.add(r);
}
const gableShape = new THREE.Shape(); gableShape.moveTo(-HW / 2 - .5, 0); gableShape.lineTo(HW / 2 + .5, 0); gableShape.lineTo(0, RIDGE - ATT); gableShape.closePath();
house.add(at(mesh(new THREE.ShapeGeometry(gableShape), std(0x120e14)), 0, ATT, -HD - .01));
const atticLight = new THREE.PointLight(CORAL, 0, 5, 1.6); atticLight.position.set(.4, ATT + .9, -1.2); house.add(atticLight);
// candles: the rows. Three shelves of 22 in every table room
const SHELF_N = 22, CANDLE_ROOMS = ROOMS.filter((r) => r.name !== "hall");
const CN = CANDLE_ROOMS.length * 3 * SHELF_N;
const candleBody = new THREE.InstancedMesh(new THREE.CylinderGeometry(.028, .03, .16, 6), std(0xe8dcc0), CN);
const flames = new THREE.InstancedMesh(new THREE.PlaneGeometry(.11, .16), addM(CANDLE, 2.2, { map: glowTex }), CN);
flames.frustumCulled = false; candleBody.frustumCulled = false; house.add(candleBody, flames);
const CANDLES = [];
CANDLE_ROOMS.forEach((r, ri) => {
  const [cx, cy] = roomC(r);
  for (let sh = 0; sh < 3; sh++) {
    const y = cy - .75 + sh * .55;
    house.add(at(mesh(new THREE.BoxGeometry(HW / 2 - .5, .04, .32), std(0x3a2618)), cx, y - .02, -HD + .2));
    for (let i = 0; i < SHELF_N; i++) {
      const u = (i + .5) / SHELF_N, x = cx - (HW / 2 - .7) / 2 + u * (HW / 2 - .7);
      const k = CANDLES.length;
      CANDLES.push({ room: r.name, u, x, y: y + .08, z: -HD + .2 + (hash(k) - .5) * .1, ph: hash(k + 7) * 6 });
      candleBody.setMatrixAt(k, tM.compose(tP.set(x, y + .08, CANDLES[k].z), tQ.identity(), tS.set(1, .7 + hash(k + 3) * .6, 1)));
    }
  }
});
candleBody.instanceMatrix.needsUpdate = true;

// the facade: shown from outside, cut away for the interior shots
const facade = grp(house, 0, 0, 0);
const sideWall = mesh(new THREE.BoxGeometry(HW + .3, ATT, .14), std(0x2e2638)); sideWall.position.set(0, ATT / 2, .05); facade.add(sideWall);
const fGable = mesh(new THREE.ShapeGeometry(gableShape), std(0x272030)); fGable.position.set(0, ATT, .12); facade.add(fGable);
const winM = [];
for (const r of ROOMS) {
  const [cx, cy] = roomC(r);
  if (r.name === "hall") continue;
  const m = glow(CANDLE, 0); winM.push([r, m]);
  facade.add(at(mesh(new THREE.PlaneGeometry(1.0, 1.35), m), cx, cy + .1, .13));
  facade.add(at(mesh(new THREE.BoxGeometry(1.2, .1, .1), trimM), cx, cy + .82, .16));
  facade.add(at(mesh(new THREE.BoxGeometry(1.2, .1, .14), trimM), cx, cy - .62, .18));
  facade.add(at(mesh(new THREE.BoxGeometry(.06, 1.35, .06), trimM), cx, cy + .1, .15));
  facade.add(at(mesh(new THREE.BoxGeometry(1.0, .06, .06), trimM), cx, cy + .2, .15));
}
// the attic's round window and the hall window
const roundWin = glow(CORAL, 0);
facade.add(at(mesh(new THREE.CircleGeometry(.55, 24), roundWin), 0, ATT + 1.1, .14));
facade.add(at(mesh(new THREE.TorusGeometry(.58, .07, 6, 24), trimM), 0, ATT + 1.1, .16));
const hallWin = glow(CANDLE, 0); facade.add(at(mesh(new THREE.PlaneGeometry(.8, 1.2), hallWin), -2.1, 1.5, .13));
// the front door, porch and its ward
const DOOR = [.0, 0, .14];
const doorTex = canvasTex(256, 512, (g, w, h) => {
  g.fillStyle = "#2a1610"; g.fillRect(0, 0, w, h);
  g.strokeStyle = "#140a07"; g.lineWidth = 10;
  for (const [x, y, ww, hh] of [[28, 40, 90, 170], [138, 40, 90, 170], [28, 260, 90, 200], [138, 260, 90, 200]]) g.strokeRect(x, y, ww, hh);
});
const door = mesh(new THREE.BoxGeometry(1.0, 2.0, .1), std(0xffffff, { map: doorTex })); door.position.set(DOOR[0], 1.0, .16); facade.add(door);
const plaqueTex = canvasTex(512, 128, (g, w, h) => {
  g.fillStyle = "#b8392a"; g.beginPath(); g.roundRect(6, 6, w - 12, h - 12, 18); g.fill();
  g.strokeStyle = "#f0d0a0"; g.lineWidth = 6; g.stroke(); write(g, "PRODUCTION", w / 2, h / 2 + 4, 66, { f: "JBMono", w: 700, c: "#fff3e0" });
});
facade.add(at(mesh(new THREE.PlaneGeometry(.9, .225), std(0xffffff, { map: plaqueTex, emissive: 0x551510, emissiveMap: plaqueTex })), 0, 2.25, .23));
const knob = mesh(new THREE.SphereGeometry(.05, 10, 8), std(0xc8a050, { metalness: .8, roughness: .3 })); knob.position.set(.35, 1.0, .24); facade.add(knob);
const porchLight = new THREE.PointLight(CANDLE, 1.6, 4, 1.8); porchLight.position.set(.9, 2.3, .9); facade.add(porchLight);
const lamp = mesh(new THREE.BoxGeometry(.14, .22, .14), glow(CANDLE, 1.6)); lamp.position.set(.85, 2.3, .3); facade.add(lamp);
facade.add(at(mesh(new THREE.BoxGeometry(2.6, .1, 1.5), roofM), 0, 2.75, .8));
for (const s of [-1, 1]) facade.add(at(mesh(new THREE.BoxGeometry(.1, 2.7, .1), trimM), s * 1.15, 1.35, 1.45));
facade.add(at(mesh(new THREE.BoxGeometry(2.6, .14, 1.5), std(0x16110e)), 0, .07, .8));
const chimney = mesh(new THREE.BoxGeometry(.6, 2.2, .6), std(0x221a1c)); chimney.position.set(1.7, 10.0, -1.6); house.add(chimney);
// the ward on the door (step 2): a glowing circle with a shield
const wardTex = canvasTex(512, 512, (g, w) => {
  g.strokeStyle = "#ff7a59"; g.lineWidth = 14; g.beginPath(); g.arc(w / 2, w / 2, 220, 0, 7); g.stroke();
  g.lineWidth = 6; g.beginPath(); g.arc(w / 2, w / 2, 190, 0, 7); g.stroke();
  for (let i = 0; i < 24; i++) { const a = i / 24 * 6.283; g.beginPath(); g.moveTo(w / 2 + Math.cos(a) * 192, w / 2 + Math.sin(a) * 192); g.lineTo(w / 2 + Math.cos(a) * 218, w / 2 + Math.sin(a) * 218); g.stroke(); }
  g.fillStyle = "#ff7a59"; g.beginPath(); g.moveTo(256, 120); g.lineTo(370, 165); g.lineTo(370, 260); g.quadraticCurveTo(370, 350, 256, 400); g.quadraticCurveTo(142, 350, 142, 260); g.lineTo(142, 165); g.closePath(); g.fill();
  g.strokeStyle = "#2a0d08"; g.lineWidth = 26; g.lineCap = "round"; g.beginPath(); g.moveTo(200, 262); g.lineTo(245, 305); g.lineTo(320, 215); g.stroke();
});
wardTex.colorSpace = THREE.NoColorSpace;
const ward = mesh(new THREE.PlaneGeometry(1.25, 1.25), new THREE.MeshBasicMaterial({ map: wardTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, opacity: 0 }));
ward.position.set(0, 1.25, .45); facade.add(ward);
const wardLight = new THREE.PointLight(CORAL, 0, 6, 1.5); wardLight.position.set(0, 1.3, 1.2); facade.add(wardLight);
// the twist: boards over the door and windows, a padlock and chain
const boardM = std(0x7a5636), BOARDS = [];
const boardAt = (x, y, rz, w = 1.5) => { const b = mesh(new THREE.BoxGeometry(w, .2, .08), boardM); b.position.set(x, y, .3); b.rotation.z = rz; facade.add(b); BOARDS.push({ b, y, rz }); };
boardAt(0, 1.45, .35, 1.6); boardAt(0, .75, -.3, 1.6);
for (const r of ROOMS) { if (r.name === "hall") continue; const [cx, cy] = roomC(r); boardAt(cx, cy + .3, .5); boardAt(cx, cy - .1, -.45); }
const lock = grp(facade, .0, 1.05, .42);
lock.add(mesh(rb(.34, .3, .14, .04), std(CORAL, { roughness: .4, metalness: .3, emissive: 0x401008 })));
lock.add(at(mesh(new THREE.TorusGeometry(.11, .035, 8, 16, Math.PI), std(0xb8bcc8, { metalness: .9, roughness: .3 })), 0, .15, 0));
const chain = grp(facade, 0, 1.05, .38);
for (let i = -6; i <= 6; i++) { if (Math.abs(i) < 2) continue; const l = mesh(new THREE.TorusGeometry(.06, .016, 6, 10), std(0x9aa0aa, { metalness: .9, roughness: .4 })); l.position.set(i * .1, -Math.abs(i) * .015, 0); l.rotation.y = i % 2 ? Math.PI / 2 : 0; chain.add(l); }

// ---------------------------------------------------------------- the attic: the chest with the copy
const chest = grp(house, .7, ATT + .08, -1.4);
chest.add(at(mesh(rb(1.1, .55, .62, .05), std(0x3b2414)), 0, .28, 0));
const lid = grp(chest, 0, .56, -.31);
lid.add(at(mesh(rb(1.12, .14, .64, .05), std(0x4a2c18)), 0, .07, .31));
for (const s of [-1, 1]) chest.add(at(mesh(new THREE.BoxGeometry(.06, .57, .64), std(0xb08a40, { metalness: .7, roughness: .4 })), s * .45, .28, 0));
const chestGlow = halo(2.6, CORAL, 0); chestGlow.position.set(0, .8, .2); chest.add(chestGlow);
const chestLight = new THREE.PointLight(CORAL, 0, 5, 1.5); chestLight.position.set(0, .9, .4); chest.add(chestLight);
const MOTE_N = 40;
const motes = new THREE.InstancedMesh(new THREE.PlaneGeometry(.05, .05), addM(0xffc0a0, 1.6, { map: glowTex }), MOTE_N); motes.frustumCulled = false; chest.add(motes);
// cobwebs in the attic corners
const webTex = canvasTex(256, 256, (g, w) => {
  g.strokeStyle = "rgba(220,225,235,.55)"; g.lineWidth = 2;
  for (let i = 0; i < 9; i++) { const a = i / 8 * Math.PI / 2; g.beginPath(); g.moveTo(0, 0); g.lineTo(Math.cos(a) * w, Math.sin(a) * w); g.stroke(); }
  for (let r = 30; r < w; r += 34) { g.beginPath(); for (let i = 0; i <= 8; i++) { const a = i / 8 * Math.PI / 2, rr2 = r * (1 - .1 * Math.sin(i * 1.7)); i ? g.lineTo(Math.cos(a) * rr2, Math.sin(a) * rr2) : g.moveTo(Math.cos(a) * rr2, Math.sin(a) * rr2); } g.stroke(); }
});
const WEBS = [];
for (const s of [-1, 1]) {
  const web = mesh(new THREE.PlaneGeometry(1.4, 1.4), new THREE.MeshBasicMaterial({ map: webTex, transparent: true, depthWrite: false, side: THREE.DoubleSide }));
  web.position.set(s * 1.9, ATT + 1.05, -2.0); web.rotation.z = s > 0 ? Math.PI / 2 : 0; web.scale.x = s; house.add(web); WEBS.push(web);
}

// ---------------------------------------------------------------- the hall: the grandfather clock
const clock = grp(house, -2.15, 0, -2.55);
clock.add(at(mesh(rb(.7, 2.4, .45, .05), std(0x2c1a10)), 0, 1.2, 0));
clock.add(at(mesh(rb(.8, .45, .5, .06), std(0x3a2214)), 0, 2.55, 0));
const faceTex = canvasTex(256, 256, (g, w) => {
  g.fillStyle = "#e8dcc0"; g.beginPath(); g.arc(w / 2, w / 2, 120, 0, 7); g.fill();
  g.strokeStyle = "#2a1a10"; g.lineWidth = 8; g.stroke();
  for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283; write(g, ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"][i], w / 2 + Math.sin(a) * 92, w / 2 - Math.cos(a) * 92, 22, { f: "serif", c: "#2a1a10" }); }
});
const cface = mesh(new THREE.CircleGeometry(.28, 32), std(0xb8b0a0, { map: faceTex })); cface.position.set(0, 2.1, .235); clock.add(cface);
const hands = grp(clock, 0, 2.1, .25);
const hourH = mesh(new THREE.BoxGeometry(.03, .14, .01).translate(0, .07, 0), std(0x100a06)); hourH.rotation.z = -(3 + 7 / 60) / 12 * 6.283; hands.add(hourH);
const minH = mesh(new THREE.BoxGeometry(.02, .22, .01).translate(0, .11, 0), std(0x100a06)); minH.rotation.z = -7 / 60 * 6.283; hands.add(minH);
const pend = grp(clock, 0, 1.75, .24);
pend.add(at(mesh(new THREE.BoxGeometry(.03, .8, .02), std(0xb08a40, { metalness: .8, roughness: .35 })), 0, -.4, 0));
pend.add(at(mesh(new THREE.CylinderGeometry(.11, .11, .03, 20).rotateX(Math.PI / 2), std(0xc8a050, { metalness: .8, roughness: .3 })), 0, -.82, 0));
const clockLight = new THREE.PointLight(0xffd080, 0, 3, 1.6); clockLight.position.set(-2.1, 2.2, -1.6); house.add(clockLight);
const bellHalo = halo(1.6, 0xffd38a, 0); bellHalo.position.set(0, 2.1, .3); clock.add(bellHalo);

// ---------------------------------------------------------------- the ghost: a sheet with a waving hem
const ghost = grp(scene, 0, 0, 0);
const prof = [];
for (let i = 0; i <= 16; i++) { const a = i / 16 * Math.PI / 2; prof.push(new THREE.Vector2(Math.sin(a) * .42 + 1e-3, .9 + Math.cos(a) * .42)); }
for (let i = 1; i <= 10; i++) prof.push(new THREE.Vector2(.42 + i * .022, .9 - i * .095));
const gGeo = new THREE.LatheGeometry(prof, 40);
const gBase = gGeo.attributes.position.array.slice();
const ghostM = new THREE.MeshStandardMaterial({ color: GHOST, emissive: 0x8fa5d0, emissiveIntensity: .85, roughness: .7, transparent: true, opacity: .9, side: THREE.DoubleSide });
const gBody = mesh(gGeo, ghostM); ghost.add(gBody);
const eyeM = new THREE.MeshBasicMaterial({ color: 0x05060a });
for (const s of [-1, 1]) { const e = mesh(new THREE.SphereGeometry(.07, 12, 8), eyeM); e.scale.set(1, 1.5, .4); e.position.set(s * .14, 1.32, .37); ghost.add(e); }
const mouth = mesh(new THREE.SphereGeometry(.07, 12, 8), eyeM); mouth.scale.set(.8, 1.2, .4); mouth.position.set(0, 1.1, .4); ghost.add(mouth);
const gHalo = halo(3.2, 0x8fb0ff, .3); gHalo.position.set(0, 1, -.2); ghost.add(gHalo);
const gLight = new THREE.PointLight(0x9fb8ff, 0, 5, 1.6); gLight.position.set(0, 1.1, .6); ghost.add(gLight);
function waveGhost(t) {
  const p = gGeo.attributes.position.array;
  for (let i = 0; i < p.length; i += 3) {
    const y = gBase[i + 1], x = gBase[i], z = gBase[i + 2];
    const k = clamp((.9 - y) / .95), a = Math.atan2(z, x);
    p[i] = x * (1 + k * .06 * Math.sin(a * 3 + t * 5)); p[i + 2] = z * (1 + k * .06 * Math.sin(a * 3 + t * 5));
    p[i + 1] = y + k * .08 * Math.sin(a * 6 + t * 6);
  }
  gGeo.attributes.position.needsUpdate = true; gGeo.computeVertexNormals();
}

// ---------------------------------------------------------------- the pixel mascot: a 2D sprite living in the 3D house, with a lantern
const SPR = ["..BBBBBBBBBB..", ".BBBBBBBBBBBB.", ".BBBBBBBBBBBB.", ".BBBBBBBBBBBB.", ".BBBBBBBBBBBB.", "BBBBBBBBBBBBBB", "BBBBBBBBBBBBBB",
  ".BBBBBBBBBBBB.", ".DDDDDDDDDDDD.", "..LL......LL..", "..LL......LL.."];
function spriteTex(eyes) {
  return canvasTex(16 * 10, 14 * 10, (g) => {
    const P = 10;
    g.fillStyle = "#f7c6b6"; g.fillRect(7 * P, 0, 2 * P, P); g.fillStyle = "#b9523d"; g.fillRect(7.5 * P, P, P, P);
    SPR.forEach((row, r) => [...row].forEach((ch, c) => {
      if (ch === ".") return; g.fillStyle = ch === "B" ? "#e8735a" : "#b9523d"; g.fillRect((c + 1) * P, (r + 2) * P, P, P);
    }));
    g.fillStyle = "#1e1b18";
    const E = { open: [[4, 5], [5, 5], [4, 6], [5, 6], [10, 5], [11, 5], [10, 6], [11, 6]], happy: [[4, 5], [5, 5], [3, 6], [6, 6], [10, 5], [11, 5], [9, 6], [12, 6]],
      wide: [[4, 4], [5, 4], [4, 5], [5, 5], [4, 6], [5, 6], [10, 4], [11, 4], [10, 5], [11, 5], [10, 6], [11, 6]] }[eyes];
    for (const [c, r] of E) g.fillRect(c * P, (r + 1) * P, P, P);
    if (eyes === "happy") for (const [c, r] of [[6, 8], [9, 8], [7, 9], [8, 9]]) g.fillRect(c * P, (r + 1) * P, P, P);
  }, true);
}
const SPRITES = { open: spriteTex("open"), happy: spriteTex("happy"), wide: spriteTex("wide") };
const mascot = grp(scene, 0, 0, 0);
const mascotM = new THREE.MeshBasicMaterial({ map: SPRITES.open, transparent: true, alphaTest: .5, toneMapped: false, fog: false, color: new THREE.Color(1.5, 1.15, 1.05) });
const mSprite = mesh(new THREE.PlaneGeometry(.8, .7), mascotM); mSprite.position.y = .35; mascot.add(mSprite);
const lantern = grp(mascot, .48, .3, .05);
lantern.add(mesh(new THREE.CylinderGeometry(.06, .07, .16, 8), glow(0xffb090, 2.4)));
lantern.add(at(mesh(new THREE.TorusGeometry(.05, .01, 6, 12, Math.PI), std(0x2a2a30)), 0, .1, 0));
const lHalo = halo(1.6, CORAL, .55); lantern.add(lHalo);
const lLight = new THREE.PointLight(CORAL, 2.2, 4.5, 1.5); lantern.add(lLight);
const camFlash = new THREE.PointLight(0xffffff, 0, 6, 1.4); mascot.add(camFlash); camFlash.position.set(0, .5, .5);

// ---------------------------------------------------------------- the weather and the things in the dark
// rain: thin streaks in a box around the house, only outside
const RAIN_N = 320;
const rain = new THREE.InstancedMesh(new THREE.PlaneGeometry(.012, .55), addM(0xaabbe0, .55), RAIN_N); rain.frustumCulled = false; scene.add(rain);
// bats: a body and two scalloped wings each, flapping
const wingShape = new THREE.Shape();
[[0, .05], [.22, .13], [.48, .1], [.64, 0], [.5, -.05], [.42, -.01], [.33, -.08], [.24, -.02], [.14, -.08], [0, -.05]].forEach(([x, y], i) => (i ? wingShape.lineTo(x, y) : wingShape.moveTo(x, y)));
const wingGeo = new THREE.ShapeGeometry(wingShape).rotateX(-Math.PI / 2);
const batM = new THREE.MeshBasicMaterial({ color: 0x030306, side: THREE.DoubleSide, fog: false });
const BAT_N = 9, BATS = [];
for (let i = 0; i < BAT_N; i++) {
  const b = grp(scene, 0, -50, 0);
  b.add(at(mesh(new THREE.SphereGeometry(.07, 8, 6), batM), 0, 0, 0)).children[0].scale.set(.8, .7, 1.6);
  const wl = grp(b, -.04, 0, 0), wr = grp(b, .04, 0, 0);
  wr.add(mesh(wingGeo, batM)); wl.add(mesh(wingGeo, batM)); wl.scale.x = -1;
  BATS.push({ b, wl, wr });
}
// glowing eyes: a pair of small lights that blink
function eyes(parent, x, y, z, size, color, k = 3) {
  const g = grp(parent, x, y, z);
  for (const s of [-1, 1]) {
    const e = mesh(new THREE.PlaneGeometry(size * 2.4, size * 2.4), addM(color, k, { map: glowTex })); e.position.x = s * size * 1.1; g.add(e);
    const core = mesh(new THREE.CircleGeometry(size * .35, 10), glow(color, k * 1.2)); core.position.set(s * size * 1.1, 0, .001); g.add(core);
  }
  g.visible = false; return g;
}
const roundEyes = eyes(facade, 0, ATT + 1.1, .2, .09, 0xffe9a0, 3.2);
const yardEyes = eyes(scene, -6.2, .55, 1.0, .07, 0xd8ff70, 3);
const winEyes = [];
for (const [r] of winM) { const [cx, cy] = roomC(r); winEyes.push([r, eyes(facade, cx + (hash(cx + cy) - .5) * .3, cy + .3, .2, .07, 0xff3a20, 3.5)]); }
// the figure by the tree, seen only while the lightning lasts
const figTex = canvasTex(160, 480, (g, w, h) => {
  g.fillStyle = "#020205";
  g.beginPath(); g.arc(w / 2, 62, 34, 0, 7); g.fill();
  g.beginPath(); g.moveTo(w / 2 - 30, 92); g.quadraticCurveTo(w / 2 - 70, 120, w / 2 - 62, 300); g.lineTo(w / 2 - 48, h); g.lineTo(w / 2 + 48, h);
  g.lineTo(w / 2 + 62, 300); g.quadraticCurveTo(w / 2 + 70, 120, w / 2 + 30, 92); g.closePath(); g.fill();
  g.fillStyle = "#fff4d8"; g.fillRect(w / 2 - 16, 58, 9, 5); g.fillRect(w / 2 + 7, 58, 9, 5);
});
const figure = mesh(new THREE.PlaneGeometry(.75, 2.25), new THREE.MeshBasicMaterial({ map: figTex, transparent: true, depthWrite: false }));
figure.position.set(1.4, 9.48 + 1.1, 0); house.add(figure);   // on the roof slope, against the sky

// ---------------------------------------------------------------- the story: when each room's candles live and die
// the ghost's sweep after Enter: top floor first, zig-zag down; then the step-1 demo relights "orders" and the ghost
// takes it again after the snapshot; everything relights for the CTA (restored)
const S1a = T.press + .4, S2z = T.gone + .1;
const SWEEP = ["sessions", "invoices", "payments", "orders", "users"];
const RT = {};
SWEEP.forEach((n, i) => { const a = lerp(S1a, S2z, i / 5), b = lerp(S1a, S2z, (i + 1) / 5); RT[n] = [["kill", a, b, i % 2 ? -1 : 1]]; });
RT.orders.push(["on", SC[3][0] + .1], ["kill", T.first - .1, T.first + .55, 1]);
for (const n of SWEEP) RT[n].push(["on", SC[7][0] + .3 + SWEEP.indexOf(n) * .12]);
function alive(c, t) {
  let st = 1;
  for (const ev of RT[c.room]) {
    const et = ev[0] === "on" ? ev[1] + c.u * .25 : lerp(ev[1], ev[2], ev[3] > 0 ? c.u : 1 - c.u);
    if (t >= et) st = ev[0] === "on" ? 1 : 0;
  }
  return st;
}
function roomLevel(name, t) {
  const cs = CANDLES.filter((c) => c.room === name);
  let n = 0; for (const c of cs) n += alive(c, t); return n / cs.length;
}
// the ghost's path: [time, x, y, z, face]
const ROOM_GH = (n, s) => { const r = ROOMS.find((q) => q.name === n); const [cx, cy] = roomC(r); return [cx + s * 1.1, cy - 1.0, -1.4]; };
const GPATH = [];
GPATH.push([T.press, 0, .2, 1.2], [T.press + .4, 0, 3.6, .5]);
SWEEP.forEach((n, i) => { const [, a, b, dir] = RT[n][0]; const p0 = ROOM_GH(n, -dir), p1 = ROOM_GH(n, dir); GPATH.push([a, ...p0], [b, ...p1]); });
GPATH.push([S2z + .4, 2.5, .2, 1.5]);
function ghostAt(t) {
  if (between(t, T.press - .01, S2z + .45)) {
    let i = 0; while (i < GPATH.length - 2 && t > GPATH[i + 1][0]) i++;
    const [ta, ...pa] = GPATH[i], [tb, ...pb] = GPATH[i + 1];
    const k = easeIO(win(t, ta, tb)); const p = lerpV(pa, pb, k); if (t < SC[1][0] && t > T.press + .35) p[2] = 1.0;
    return { p, dx: pb[0] - pa[0], s: 1.35, vis: 1 };
  }
  if (between(t, SC[3][0], SC[4][0])) {   // step 1: drifts into "orders" after the snapshot
    const k = win(t, T.first - .4, T.first + .7);
    return { p: lerpV([-3.6, 3.0, -1.0], [.2, 3.0, -1.4], easeIO(k)), dx: 1, s: .9, vis: k > 0 && k < 1 ? 1 : 0 };
  }
  if (between(t, SC[4][0], SC[5][0])) {   // step 2: rushes the warded door and is thrown back
    const a = T.destructive - .2, r = T.refused - .15;
    if (t < r) { const k = easeIO(win(t, a, r)); return { p: lerpV([-4.6, 1.8, 2.6], [-.35, 1.0, 1.05], k), dx: 1, s: 1.1, vis: t > a ? 1 : 0 }; }
    const k = easeOut(win(t, r, r + .7)); return { p: lerpV([-.35, 1.0, 1.05], [-5, 3.2, 3.5], k), dx: -1, s: 1.1 - k * .3, vis: k < 1 ? 1 : 0 };
  }
  return { p: [0, -20, 0], dx: 0, s: 1, vis: 0 };
}

// ---------------------------------------------------------------- shots: [start, end, cam from, cam to, look from, look to, fov]
const OUT = T.press - .05;
const SHOTS = [
  [0, SC[1][0], [0, 4.6, 19], [0, 4.2, 15], [0, 5.6, 0], [0, 5.2, 0], 50, "out"],
  [SC[1][0], T.backups - .12, [0, 4.4, 12.5], [0, 4.2, 11.5], [0, 4.4, -1.5], [0, 4.3, -1.5], 50, "in"],
  [T.backups - .12, SC[2][0], [-3.3, 1.3, 6.8], [-3.5, 1.2, 6.2], [-4.5, .9, 3.4], [-4.5, .9, 3.4], 40, "out"],
  [SC[2][0], SC[3][0], [.15, ATT + 1.2, 4.6], [.1, ATT + 1.1, 3.9], [.1, ATT + .45, -1.2], [.1, ATT + .45, -1.2], 45, "in"],
  [SC[3][0], SC[4][0], [-1.4, 3.9, 4.6], [-1.5, 3.85, 4.1], [-1.5, 3.7, -1.6], [-1.5, 3.7, -1.6], 47, "in"],
  [SC[4][0], SC[5][0], [1.0, 1.8, 7.0], [.8, 1.7, 6.3], [-.1, .95, 0], [-.1, .95, 0], 46, "out"],
  [SC[5][0], SC[6][0], [-1.2, 1.7, 2.7], [-1.3, 1.65, 2.3], [-2.15, 1.35, -2.5], [-2.15, 1.4, -2.5], 44, "in"],
  [SC[6][0], SC[7][0], [.5, 2.2, 7.4], [.3, 2.0, 6.4], [0, 1.65, 0], [0, 1.6, 0], 48, "out"],
  [SC[7][0], T.end + 1, [0, 4.4, 20], [0, 4.6, 21], [0, 3.4, 0], [0, 3.5, 0], 50, "out"],
];
function shot(t) {
  let s = SHOTS[0]; for (const x of SHOTS) if (t >= x[0]) s = x;
  const k = easeIO(win(t, s[0], s[1]));
  return { p: lerpV(s[2], s[3], k), q: lerpV(s[4], s[5], k), fov: s[6], out: s[7] === "out" };
}
const lightning = (t) => Math.max(...T.lightning.map(([at, k]) => pulse(t, at, .02, .22 + .18 * k) * k));
// bat flights, one per T.bats entry: [from, to, arc] per bat, or a circle round the moon for the CTA
function batAt(i, t) {
  for (let f = 0; f < T.bats.length; f++) {
    const a = T.bats[f] + hash(i * 3 + f) * .5, j = (q) => (hash(i * 11 + f * 5 + q) - .5);
    if (f === 3) {
      if (t < a) continue;
      // round the moon: it sits behind (4.5, 12.7, -10) from the CTA camera
      const ang = (t - a) * (.6 + hash(i) * .4) + i * .7, r = 2.4 + hash(i + 4) * 1.8;
      const at2 = (q) => [4.5 + Math.cos(q) * r, 12.4 + Math.sin(q) * r * .55 + j(1), -10 + Math.sin(q) * 1.2];
      return { p: at2(ang), n: at2(ang + .1), s: .9, flap: 15 };
    }
    const d = [3.6, 2.6, 1.6][f], k = (t - a) / d;
    if (k < 0 || k > 1) continue;
    const P = [
      [[14 + j(1) * 3, 15.5 + j(2) * 2, -21 + j(3) * 3], [-11, 13 + j(4) * 3, -9 + j(5) * 4], 1],
      [[1.7, 11.2, -1.6], [j(1) * 26, 14 + j(2) * 5, 6 + j(3) * 6], 2.5],
      [[-6, 2.4 + j(1) * 1.4, 3.6 + j(2) * 1.2], [6, 3.4 + j(3) * 1.4, 4.2 + j(4) * 1.4], 1.2],
    ][f];
    const pos = (q) => lerpV(P[0], P[1], q).map((v, ax) => v + (ax === 1 ? Math.sin(q * Math.PI) * P[2] : 0) + (ax === 1 ? Math.sin(q * 20 + i) * .12 : 0));
    return { p: pos(k), n: pos(Math.min(1, k + .02)), s: [1.1, .6, .7][f] + hash(i + 2) * .3, flap: 17 + hash(i) * 6 };
  }
  return null;
}

// ---------------------------------------------------------------- render
function renderAt(t) {
  const s = shot(t);
  const ln0 = lightning(t);
  const hand = .012;
  // shake: Enter, the big flashes, the clang at the ward, the boards
  let sh = pulse(t, T.press, .02, .6) * .09 + ln0 * .025 + pulse(t, T.refused - .15, .02, .35) * .05;
  for (let i = 0; i < 6; i++) sh += pulse(t, T.readonly - .15 + i * .09 + .1, .01, .12) * .02;
  camera.position.set(s.p[0] + Math.sin(t * .9) * hand + Math.sin(t * 83) * sh, s.p[1] + Math.cos(t * .7) * hand + Math.cos(t * 71) * sh, s.p[2]);
  camera.lookAt(s.q[0], s.q[1], s.q[2]);
  camera.fov = s.fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  facade.visible = s.out;
  const twist = between(t, SC[6][0], SC[7][0]);
  // rooms: candles, room light, window glow
  const fl = (i) => .85 + .15 * Math.sin(t * 13 + CANDLES[i].ph) * Math.sin(t * 7.3 + i);
  for (let i = 0; i < CANDLES.length; i++) {
    const c = CANDLES[i], a = alive(c, t);
    flames.setMatrixAt(i, tM.compose(tP.set(c.x, c.y + .12, c.z + .01), camera.quaternion, tS.setScalar(a ? fl(i) : 0)));
  }
  flames.instanceMatrix.needsUpdate = true;
  for (const r of ROOMS) {
    const lv = r.name === "hall" ? (twist ? .1 : .35) : roomLevel(r.name, t);
    r.lv = lv;
    r.light.intensity = lv * 6 * (.9 + .1 * Math.sin(t * 9 + r.f));
  }
  for (const [r, m] of winM) m.color.setRGB(1, .22, .04).multiplyScalar(r.lv * 1.1 * (twist ? .5 : 1));
  hallWin.color.setRGB(1, .22, .04).multiplyScalar(twist ? .15 : .8);
  roundWin.color.setRGB(1, .42, .3).multiplyScalar(t > SC[2][0] - .5 ? 1.4 : .15);
  // the ghost
  const g = ghostAt(t);
  ghost.visible = !!g.vis; ghost.position.set(g.p[0], g.p[1] + Math.sin(t * 2.4) * .08, g.p[2]); ghost.scale.setScalar(g.s);
  ghost.rotation.y = Math.atan2(g.dx, 1) * .6 + Math.sin(t * 1.3) * .1;
  ghost.lookAt(camera.position.x, ghost.position.y, camera.position.z); ghost.rotation.y += g.dx * .25;
  gLight.intensity = ghost.visible ? 2.2 : 0;
  if (ghost.visible) waveGhost(t);
  ghostM.opacity = .9 * (hash(Math.floor(t * 15)) > .9 ? .35 : 1);
  // the attic chest: opens on "copy"
  const op = easeOut(win(t, T.copy - .4, T.copy + .2)) * (t < SC[3][0] ? 1 : 0);
  lid.rotation.x = -op * 1.7;
  chestGlow.material.color.set(CORAL).multiplyScalar(op * .9);
  chestLight.intensity = op * 4.5;
  atticLight.intensity = between(t, SC[2][0], SC[3][0]) ? .6 : 0;
  for (let i = 0; i < MOTE_N; i++) {
    const ph = (hash(i) + t * .12 * (.5 + hash(i + 1))) % 1;
    tP.set((hash(i + 2) - .5) * .9, .5 + ph * 1.5, (hash(i + 3) - .5) * .5);
    motes.setMatrixAt(i, tM.compose(tP, camera.quaternion, tS.setScalar(op * (1 - ph) * (1.2 + hash(i + 4)))));
  }
  motes.instanceMatrix.needsUpdate = true;
  // the ward (step 2)
  const wk = easeOut(win(t, T.prod - .1, T.prod + .3)) * (between(t, SC[4][0], SC[5][0]) ? 1 : 0);
  ward.material.opacity = wk * (.85 + .15 * Math.sin(t * 12)) + pulse(t, T.refused - .15, .03, .3) * .5 * wk;
  ward.scale.setScalar(.6 + wk * .4 + pulse(t, T.refused - .15, .05, .3) * .15); ward.rotation.z = t * .5;
  wardLight.intensity = wk * 5 + pulse(t, T.refused - .15, .03, .3) * 10;
  // the clock (step 3): pendulum, rings on "alarm", calm on "backups"
  const ring = between(t, T.alarm - .05, T.fresh - .1);
  pend.rotation.z = Math.sin(t * 3.1) * .22;
  clock.rotation.z = ring ? Math.sin(t * 60) * .012 : 0;
  bellHalo.material.color.set(0xffd38a).multiplyScalar(ring ? .12 + .12 * Math.abs(Math.sin(t * 14)) : 0);
  clockLight.intensity = between(t, SC[5][0], SC[6][0]) ? (ring ? .7 + .3 * Math.sin(t * 28) : .45) : 0;
  twistFill.intensity = twist ? 1.4 + ln0 * 3 : 0;
  graveLight.intensity = between(t, T.backups - .15, SC[2][0]) ? 7 : 0;
  // the twist: boards slam on, the lock drops
  BOARDS.forEach((bd, i) => {
    const bt = T.readonly - .15 + (i % 6) * .09, k = twist || t > SC[7][0] ? easeOut(win(t, bt, bt + .12)) : 0;
    bd.b.visible = k > 0 && t < SC[7][0]; bd.b.position.z = .3 + (1 - k) * 1.5; bd.b.position.y = bd.y; bd.b.rotation.z = bd.rz;
  });
  const lk = between(t, SC[6][0], SC[7][0]) ? easeOut(win(t, T.readonly + .2, T.readonly + .45)) : 0;
  lock.visible = chain.visible = lk > 0; lock.position.y = 1.05 + (1 - lk) * 2.5; chain.scale.x = lk;
  // the mascot: where it stands in each scene
  const MP = [
    [SC[2][0], [-.55, ATT + .08, -1.0], "open"], [T.copy - .2, [-.55, ATT + .08, -1.0], "happy"],
    [SC[3][0], [-2.3, FH + .08, -1.0], "open"], [T.backs, [-2.3, FH + .08, -1.0], "happy"],
    [SC[4][0], [1.0, .08, 1.9], "open"], [T.refused, [1.0, .08, 1.9], "happy"],
    [SC[5][0], [-1.15, .08, -2.1], "wide"], [T.fresh, [-1.15, .08, -2.1], "happy"],
    [SC[6][0], [1.0, .08, 1.9], "open"], [T.touch, [1.0, .08, 1.9], "happy"],
    [SC[7][0], [-.9, .14, 1.0], "happy"],
  ];
  let mp = null; for (const m of MP) if (t >= m[0]) mp = m;
  mascot.visible = !!mp && t >= SC[2][0];
  if (mp) {
    mascot.position.set(mp[1][0], mp[1][1] + Math.abs(Math.sin(t * 4.2)) * .05, mp[1][2]);
    mascot.quaternion.copy(camera.quaternion);
    mascotM.map = SPRITES[mp[2]];
    mascot.scale.setScalar(between(t, SC[7][0], 999) ? 1.2 : .75);
  }
  lLight.intensity = 2.2 + Math.sin(t * 9) * .3;
  camFlash.intensity = pulse(t, T.backs - .1, .02, .25) * 40;
  // lightning, the porch light, the grade
  const ln = lightning(t);
  flashLight.intensity = ln * 6; hemi.intensity = .5 + ln * 1.5;
  scene.background.copy(SKY).lerp(new THREE.Color(0x5a6890), ln * .5);
  porchLight.intensity = twist ? .4 + (Math.sin(t * 37) > .2 ? .6 : 0) : 1.6;
  for (let i = 0; i < FOG_N; i++) {
    tP.set(((hash(i) * 26 + t * .25 * (hash(i + 1) - .3)) % 26) - 13, .25 + hash(i + 2) * .4, -3 + hash(i + 3) * 11);
    fogI.setMatrixAt(i, tM.compose(tP, camera.quaternion, tS.set(3 + hash(i + 4) * 3, 1.2 + hash(i + 5), 1)));
  }
  fogI.instanceMatrix.needsUpdate = true;
  // rain, swaying trees and webs
  rain.visible = s.out;
  for (let i = 0; i < RAIN_N; i++) {
    const y = 16 - ((hash(i) * 16 + t * (15 + hash(i + 1) * 4)) % 16);
    tP.set(-12 + hash(i + 2) * 24 - (16 - y) * .12, y, -4 + hash(i + 3) * 6.5);   // stays clear of the close shots (cameras at z 6+)
    tQ.setFromAxisAngle(new THREE.Vector3(0, 0, 1), -.12);
    rain.setMatrixAt(i, tM.compose(tP, tQ, tS.setScalar(.8 + hash(i + 4) * .5)));
  }
  rain.instanceMatrix.needsUpdate = true;
  TREES.forEach((g, i) => { g.rotation.z = Math.sin(t * .8 + i * 1.7) * .02 + Math.sin(t * 2.3 + i) * .006 + ln0 * .01; });
  WEBS.forEach((w, i) => { w.rotation.x = Math.sin(t * 1.4 + i * 2) * .12; });
  // bats
  BATS.forEach((bt, i) => {
    const st = batAt(i, t);
    bt.b.visible = !!st;
    if (!st) return;
    bt.b.position.set(...st.p); bt.b.lookAt(...st.n); bt.b.scale.setScalar(st.s);
    const fl = Math.sin(t * st.flap + i * 2.1) * .9;
    bt.wr.rotation.z = fl; bt.wl.rotation.z = -fl;
  });
  // eyes: in the attic window before Enter, in every window the ghost has darkened, in the yard by the grave
  const blink = (t2, ph) => (Math.sin(t2 * 1.3 + ph * 5) > .97 ? .1 : 1);
  roundEyes.visible = s.out && between(t, 1.0, T.press - .05) && ln0 < .3;
  roundEyes.scale.set(1, blink(t, 1), 1);
  for (const [r, e] of winEyes) {
    e.visible = s.out && t > T.press && t < SC[2][0] && r.lv < .05;
    e.scale.set(1, blink(t, r.f + r.s), 1);
  }
  yardEyes.visible = s.out && between(t, T.backups - .12, SC[2][0]);
  yardEyes.scale.set(1, blink(t + .5, 3), 1);
  figure.visible = s.out && ln0 > .25 && between(t, .5, 1.2);   // the first flash shows nothing; the second shows him
  figure.lookAt(camera.position.x, figure.position.y, camera.position.z);
  const gr = grade.uniforms;
  gr.uTime.value = Math.round(t * 30) / 30;
  gr.uFlash.value = ln * .6 + pulse(t, T.backs - .1, .02, .25) * .8;
  gr.uSat.value = twist ? .6 : .82;
  gr.uTint.value.set(twist ? .95 : .92, twist ? .9 : .98, twist ? 1.05 : 1.1);
  bloom.strength = twist ? .6 : .8;
  composer.render(); out2d.drawImage(canvas, 0, 0);
}

// ---------------------------------------------------------------- cover still (cover.html sets window.HH_COVER)
function renderCover(c) {
  renderAt(c.t);
  camera.position.set(...c.cam); camera.lookAt(...c.look); camera.fov = c.fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  facade.visible = c.out !== false;
  composer.render(); out2d.drawImage(canvas, 0, 0);
}

const ready = (async () => {
  await Promise.all(["800 90px Manrope", "700 34px JBMono", "400 34px JBMono"].map((f) => document.fonts.load(f)));
  renderer.compile(scene, camera);
  if (window.HH_COVER) { renderCover(window.HH_COVER); window.__coverDone = true; return; }
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["hhworld"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
