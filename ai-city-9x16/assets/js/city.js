// AI City reel: the 3D diorama. A low-poly cream city on a floating tile, run by one AI (the coral orb above it) for
// 24 hours. Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek. Cue times come from the
// voice (window.CT, written by build/generate.py).
//   hook      pre-dawn city, the orb wakes, the camera pulls back from it to the whole tile
//   6 AM      every traffic light syncs in one green wave from the orb, buses stop only where people wait
//   noon      drones run deliveries, energy pulses flow from the plant, the hospital lights up before the ambulance
//   4 PM      one sensor flags a flooded street, every car is rerouted onto the one bridge
//   chaos     the bridge jams red, drones stall, the grid cuts power district by district, then everything freezes
//   midnight  the orb sends one ring across the city and fixes it all, then glitches: nobody knows why
//   morning   the city from above, pulling away until it is small
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const C = window.CT;
const L = C.l, E = C.e, DUR = C.end;
const W = 1080, H = 1920;

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ramp = (t, a, b) => clamp((t - a) / (b - a));
const sm = (x) => x * x * (3 - 2 * x);
const ss = (t, a, b) => sm(ramp(t, a, b));
const lerp = (a, b, x) => a + (b - a) * x;
const hash = (i) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const col = (h) => new THREE.Color(h);
const tmpC = new THREE.Color(), tmpC2 = new THREE.Color();
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S = new THREE.Vector3(), UP = new THREE.Vector3(0, 1, 0);
const pulse = (t, a, w = .35) => Math.exp(-(((t - a) / w) ** 2));

// ---------------------------------------------------------------- renderer, scene, post
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NeutralToneMapping ?? THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
scene.background = col(0xF1E9DC);
scene.fog = new THREE.Fog(0xF1E9DC, 55, 120);
const camera = new THREE.PerspectiveCamera(38, W / H, .1, 300);

const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .3, .5, .9);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1 }, uTint: { value: new THREE.Vector3(1, 1, 1) },
    uVig: { value: .28 }, uFlash: { value: 0 }, uRed: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uRed; uniform vec3 uTint; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      float g = dot(c, vec3(.299, .587, .114));
      c = mix(vec3(g), c, uSat) * uTint;
      vec2 q = vUv - .5; float v = 1. - dot(q, q) * uVig * 2.2;
      c *= v;
      c = mix(c, c * vec3(1.15, .55, .5), uRed * smoothstep(.15, .75, length(q * vec2(1., .6))));
      c += (h(floor(vUv * vec2(1080., 1920.)) + fract(uTime * 7.13) * 97.) - .5) * .028;
      c = mix(c, vec3(1., .99, .96), uFlash);
      gl_FragColor = vec4(c, 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0xfff6ea, 0xcdbfa8, .9);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1dc, 2.2);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -24, right: 24, top: 24, bottom: -24, near: 1, far: 90 });
sun.shadow.bias = -.0006;
sun.shadow.normalBias = .03;
scene.add(sun, sun.target);

// ---------------------------------------------------------------- the city plan
// tile x -16..16, z -14..16; avenues (N-S) and streets (E-W) in the north city, a river at z 6.5..9.5 with one bridge
// at x = 0, a south district (power plant, wind turbines, homes) along the south road at z = 12.5.
const AV = [-10, -5, 0, 5, 10], ST = [-12, -7, -2, 3];
const ROAD = 1.5, INK = 0x1E1B18;
const PAL = [0xFFFDF8, 0xF4C9B4, 0xE9D8BD, 0xBFD8C2, 0xC9D9EE, 0xD8CDE8, 0xF2DCC0, 0xFFFDF8, 0xE8735A];

const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .88, metalness: 0, ...o });
const add = (m, cast = true, recv = true) => { m.castShadow = cast; m.receiveShadow = recv; scene.add(m); return m; };

// the tile
const tile = add(new THREE.Mesh(new RoundedBoxGeometry(33, 1.4, 31, 4, .6), mat(0xEADFCB)), false, true);
tile.position.set(0, -.7, 1);
const tileEdge = new THREE.Mesh(new RoundedBoxGeometry(33.3, .5, 31.3, 4, .25), mat(INK, { roughness: .6 }));
tileEdge.position.set(0, -1.3, 1);
scene.add(tileEdge);
const groundSoft = add(new THREE.Mesh(new THREE.PlaneGeometry(32.4, 30.4), mat(0xE6DAC4)), false, true);
groundSoft.rotation.x = -Math.PI / 2;
groundSoft.position.set(0, .002, 1);

// roads
const roadM = mat(0x9A9187, { roughness: .95 });
const roads = new THREE.Group();
scene.add(roads);
function roadBox(x0, z0, x1, z1) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(Math.abs(x1 - x0) || ROAD, .06, Math.abs(z1 - z0) || ROAD), roadM);
  m.position.set((x0 + x1) / 2, .03, (z0 + z1) / 2);
  m.receiveShadow = true;
  roads.add(m);
}
for (const x of AV) roadBox(x, -12.75, x, 5.8);
for (const z of ST) roadBox(-10.75, z, 10.75, z);
roadBox(-14.5, 12.5, 14.5, 12.5);
roadBox(0, 9.8, 0, 12.5);
// dashed centre lines
const dashG = new THREE.BoxGeometry(.5, .02, .09);
const dashes = [];
for (const x of AV) for (let z = -12; z < 5.6; z += 1.1) dashes.push([x, z, Math.PI / 2]);
for (const z of ST) for (let x = -10.4; x < 10.5; x += 1.1) if (!AV.some((a) => Math.abs(a - x) < 1)) dashes.push([x, z, 0]);
for (let x = -14; x < 14.2; x += 1.1) if (Math.abs(x) > .9) dashes.push([x, 12.5, 0]);
const dashM = new THREE.InstancedMesh(dashG, new THREE.MeshBasicMaterial({ color: 0xFFFDF8 }), dashes.length);
dashes.forEach(([x, z, r], i) => { M4.compose(V.set(x, .07, z), Q.setFromAxisAngle(UP, r), S.set(1, 1, 1)); dashM.setMatrixAt(i, M4); });
scene.add(dashM);

// river and bridge
const river = new THREE.Mesh(new THREE.BoxGeometry(32.4, .3, 3.2), new THREE.MeshStandardMaterial({ color: 0x8FB8E0, roughness: .25, metalness: .05 }));
river.position.set(0, -.08, 8);
river.receiveShadow = true;
scene.add(river);
const bankM = mat(0xD9CBB2);
for (const z of [6.3, 9.7]) { const b = add(new THREE.Mesh(new THREE.BoxGeometry(32.4, .25, .35), bankM)); b.position.set(0, .05, z); }
const bridge = new THREE.Group();
scene.add(bridge);
const deck = add(new THREE.Mesh(new THREE.BoxGeometry(2.4, .22, 5.2), mat(0x9A9187)));
deck.position.set(0, .35, 8);
bridge.add(deck);
for (const sx of [-1.25, 1.25]) {
  const rail = add(new THREE.Mesh(new THREE.BoxGeometry(.12, .3, 5.2), mat(0xFFFDF8)));
  rail.position.set(sx, .6, 8);
  bridge.add(rail);
  const arch = add(new THREE.Mesh(new THREE.TorusGeometry(2.4, .09, 6, 28, Math.PI), mat(0xE8735A)));
  arch.position.set(sx, .45, 8);
  arch.rotation.y = Math.PI / 2;
  bridge.add(arch);
}
for (const z of [6.2, 9.8]) { const p = add(new THREE.Mesh(new THREE.BoxGeometry(2.6, .5, .4), mat(0xD9CBB2))); p.position.set(0, .2, z); }

// ---------------------------------------------------------------- buildings, windows and their ink edges
const blocksX = [[-15.2, -10.8], [-9.2, -5.8], [-4.2, -.8], [.8, 4.2], [5.8, 9.2], [10.8, 15.2]];
const blocksZ = [[-13.2, -12.8], [-11.2, -7.8], [-6.2, -2.8], [-1.2, 2.2]];
const B = [];   // {x, z, w, d, h, c, dist}
const reserved = (x, z) => (x < -10.5 && z > -7 && z < -2.2) || (x > 4.5 && x < 10 && z > 2) ;   // hospital lot, flood street
let bi = 0;
for (const [x0, x1] of blocksX) for (const [z0, z1] of blocksZ.slice(1)) {
  const nx = Math.max(1, Math.round((x1 - x0) / 1.75)), nz = Math.max(1, Math.round((z1 - z0) / 1.75));
  for (let i = 0; i < nx; i++) for (let k = 0; k < nz; k++) {
    bi++;
    const cx = x0 + (i + .5) * (x1 - x0) / nx, cz = z0 + (k + .5) * (z1 - z0) / nz;
    if (reserved(cx, cz) || hash(bi * 7) < .18) continue;
    const centre = 1 - clamp(Math.hypot(cx, cz + 3) / 15);
    const w = (x1 - x0) / nx * (.56 + hash(bi) * .26), d = (z1 - z0) / nz * (.56 + hash(bi + 9) * .26);
    const h = .7 + hash(bi * 3) * 1.4 + centre * centre * 3.8 * (.5 + hash(bi * 5));
    B.push({ x: cx, z: cz, w, d, h, c: PAL[Math.floor(hash(bi * 11) * PAL.length)], dist: (cx < -5 ? 0 : cx < 0 ? 1 : cx < 5 ? 2 : 3) + (cz < -4.5 ? 0 : 4) });
  }
}
// south district homes (district 8 in the grid's bookkeeping: lit with the south)
for (let i = 0; i < 12; i++) {
  const x = -14 + i * 1.6 + (i > 5 ? 3.4 : 0); if (x > 3) continue;
  for (const z of [11, 14]) B.push({ x, z, w: 1.1, d: 1.1, h: .8 + hash(i * 13 + z) * .7, c: PAL[Math.floor(hash(i * 3 + z) * 7)], dist: 8, house: true });
}
const DIST_N = 9;
const boxG = new THREE.BoxGeometry(1, 1, 1);
boxG.translate(0, .5, 0);
const bldM = new THREE.InstancedMesh(boxG, mat(0xffffff), B.length);
bldM.castShadow = bldM.receiveShadow = true;
B.forEach((b, i) => { M4.compose(V.set(b.x, 0, b.z), Q.identity(), S.set(b.w, b.h, b.d)); bldM.setMatrixAt(i, M4); bldM.setColorAt(i, col(b.c)); });
scene.add(bldM);
// roofs on houses
const roofG = new THREE.ConeGeometry(.85, .6, 4); roofG.rotateY(Math.PI / 4);
const houses = B.filter((b) => b.house);
const roofM = new THREE.InstancedMesh(roofG, mat(0xE8735A), houses.length);
houses.forEach((b, i) => { M4.compose(V.set(b.x, b.h + .3, b.z), Q.identity(), S.set(1, 1, 1)); roofM.setMatrixAt(i, M4); });
roofM.castShadow = true;
scene.add(roofM);
// ink edges, one geometry for every box
{
  const p = [];
  for (const b of B) {
    const x0 = b.x - b.w / 2, x1 = b.x + b.w / 2, z0 = b.z - b.d / 2, z1 = b.z + b.d / 2, y1 = b.h;
    const c = [[x0, 0, z0], [x1, 0, z0], [x1, 0, z1], [x0, 0, z1], [x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]];
    for (const [a, q] of [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]) p.push(...c[a], ...c[q]);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
  scene.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: .55 })));
}
// window bands: thin rings around each tower, lit per district
const WB = [];
B.forEach((b, i) => { if (b.house) { WB.push({ b, y: b.h * .45 }); return; } for (let y = .6; y < b.h - .3; y += .78) WB.push({ b, y }); });
WB.forEach((w) => { w.day = col(w.b.c).lerp(col(0x8FA3B8), .3); });
const winM = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), WB.length);
WB.forEach((w, i) => { M4.compose(V.set(w.b.x, w.y, w.b.z), Q.identity(), S.set(w.b.w + .03, .11, w.b.d + .03)); winM.setMatrixAt(i, M4); });
scene.add(winM);

// trees
const TR = [];
for (let i = 0; i < 70; i++) {
  const a = hash(i * 17), r = hash(i * 23);
  let x = -15 + a * 30, z = -13.5 + r * 29.5;
  if (z > 5.6 && z < 10.3) continue;
  if (AV.some((v) => Math.abs(v - x) < 1.2) || ST.some((v) => Math.abs(v - z) < 1.2) || Math.abs(z - 12.5) < 1.1) continue;
  if (B.some((b) => Math.abs(b.x - x) < b.w / 2 + .35 && Math.abs(b.z - z) < b.d / 2 + .35)) continue;
  if (x > 4.6 && z > 10.3) continue;
  TR.push([x, z, .6 + hash(i * 31) * .5]);
}
const treeM = new THREE.InstancedMesh(new THREE.ConeGeometry(.45, 1.2, 7).translate(0, .85, 0), mat(0x8FBF8F), TR.length);
const trunkM = new THREE.InstancedMesh(new THREE.CylinderGeometry(.08, .1, .35, 5).translate(0, .17, 0), mat(0x9a7a5a), TR.length);
TR.forEach(([x, z, s], i) => { M4.compose(V.set(x, 0, z), Q.identity(), S.set(s, s, s)); treeM.setMatrixAt(i, M4); trunkM.setMatrixAt(i, M4); });
treeM.castShadow = true;
scene.add(treeM, trunkM);

// hospital: white block, red cross on the roof, a ready ring
const hosp = new THREE.Group();
hosp.position.set(-13, 0, -4.6);
scene.add(hosp);
{
  const body = add(new THREE.Mesh(new THREE.BoxGeometry(3.4, 2.6, 3.2).translate(0, 1.3, 0), mat(0xFFFDF8)));
  hosp.add(body);
  const crossM = mat(0xD9483B, { emissive: 0xD9483B, emissiveIntensity: .3 });
  const c1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, .12, .42), crossM), c2 = new THREE.Mesh(new THREE.BoxGeometry(.42, .12, 1.4), crossM);
  c1.position.y = c2.position.y = 2.67;
  hosp.add(c1, c2);
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(3.4, 2.6, 3.2).translate(0, 1.3, 0)), new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: .6 }));
  hosp.add(e);
}
const hospRing = new THREE.Mesh(new THREE.TorusGeometry(2.6, .09, 8, 48), new THREE.MeshBasicMaterial({ color: 0x3FA372, transparent: true, opacity: 0, toneMapped: false }));
hospRing.rotation.x = Math.PI / 2;
hospRing.position.set(-13, .15, -4.6);
scene.add(hospRing);

// power plant + turbines in the south-east, substations per district
const plant = new THREE.Group();
plant.position.set(9.5, 0, 13);
scene.add(plant);
{
  plant.add(add(new THREE.Mesh(new THREE.BoxGeometry(3.6, 1.4, 2.2).translate(0, .7, 0), mat(0xE9D8BD))));
  const stack = add(new THREE.Mesh(new THREE.CylinderGeometry(.35, .45, 3.4, 12).translate(1.1, 1.7, 0), mat(0xFFFDF8)));
  plant.add(stack);
  const band = new THREE.Mesh(new THREE.CylinderGeometry(.37, .37, .3, 12).translate(1.1, 3.0, 0), mat(0xE8735A));
  plant.add(band);
}
const blades = [];
for (let i = 0; i < 3; i++) {
  const g = new THREE.Group();
  g.position.set(5.5 + i * 2.6, 0, 15);
  g.add(add(new THREE.Mesh(new THREE.CylinderGeometry(.06, .1, 3.2, 6).translate(0, 1.6, 0), mat(0xFFFDF8))));
  const hub = new THREE.Group(); hub.position.set(0, 3.2, .12); g.add(hub);
  for (let k = 0; k < 3; k++) { const bl = new THREE.Mesh(new THREE.BoxGeometry(.12, 1.3, .03).translate(0, .65, 0), mat(0xFFFDF8)); bl.rotation.z = k * Math.PI * 2 / 3; hub.add(bl); }
  blades.push(hub);
  scene.add(g);
}
// grid lines: plant -> bridge -> each north district's substation
const SUB = [[-7.5, -9.5], [-2.5, -9.5], [2.5, -9.5], [7.5, -9.5], [-7.5, .5], [-2.5, .5], [2.5, .5], [7.5, .5]];
const gridCurves = SUB.map(([x, z], i) => new THREE.CatmullRomCurve3([
  new THREE.Vector3(9.5, 1.8, 13), new THREE.Vector3(4, 1.7, 10.5), new THREE.Vector3(1.6, 1.8, 8),
  new THREE.Vector3(lerp(1.6, x, .45), 2.0 + hash(i) * .4, lerp(6, z, .45)), new THREE.Vector3(x, 2.1, z)]));
const gridMats = [], gridLines = [];
gridCurves.forEach((cv) => {
  const m = new THREE.MeshBasicMaterial({ color: 0xF2B33D, transparent: true, opacity: .85, toneMapped: false });
  const tb = new THREE.Mesh(new THREE.TubeGeometry(cv, 48, .03, 5, false), m);
  scene.add(tb); gridMats.push(m); gridLines.push(tb);
});
const subM = new THREE.InstancedMesh(new THREE.BoxGeometry(.5, .5, .5).translate(0, 2.1, 0), mat(0xFFFDF8), SUB.length);
SUB.forEach(([x, z], i) => { M4.compose(V.set(x, 0, z), Q.identity(), S.set(1, 1, 1)); subM.setMatrixAt(i, M4); });
scene.add(subM);
const poleM = new THREE.InstancedMesh(new THREE.CylinderGeometry(.04, .04, 1.9).translate(0, .95, 0), mat(0x7a7268), SUB.length);
SUB.forEach(([x, z], i) => { M4.compose(V.set(x, 0, z), Q.identity(), S.set(1, 1, 1)); poleM.setMatrixAt(i, M4); });
scene.add(poleM);
const PULSE_N = 5;
const pulseM = new THREE.InstancedMesh(new THREE.SphereGeometry(.1, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), SUB.length * PULSE_N);
scene.add(pulseM);

// ---------------------------------------------------------------- the AI: an orb with two rings above the city
const ORB = new THREE.Vector3(0, 9.2, -2.5);
const orb = new THREE.Group();
orb.position.copy(ORB);
scene.add(orb);
const orbCoreM = new THREE.MeshStandardMaterial({ color: 0xE8735A, emissive: 0xE8735A, emissiveIntensity: 1.2, roughness: .35 });
const orbCore = new THREE.Mesh(new THREE.SphereGeometry(.85, 40, 28), orbCoreM);
orb.add(orbCore);
const orbShell = new THREE.Mesh(new THREE.SphereGeometry(1.05, 40, 28), new THREE.MeshStandardMaterial({ color: 0xFFFDF8, transparent: true, opacity: .25, roughness: .2 }));
orb.add(orbShell);
const ringM = new THREE.MeshStandardMaterial({ color: 0x1E1B18, roughness: .5 });
const ring1 = new THREE.Mesh(new THREE.TorusGeometry(1.55, .06, 8, 64), ringM), ring2 = new THREE.Mesh(new THREE.TorusGeometry(1.95, .045, 8, 64), mat(0xE8735A, { emissive: 0xE8735A, emissiveIntensity: .5 }));
orb.add(ring1, ring2);
const orbLight = new THREE.PointLight(0xE8735A, 0, 30, 1.6);
orb.add(orbLight);
// the fix wave: a flat ring spreading over the city from under the orb
const waveM = new THREE.MeshBasicMaterial({ color: 0xE8735A, transparent: true, opacity: 0, toneMapped: false, side: THREE.DoubleSide });
const wave = new THREE.Mesh(new THREE.RingGeometry(.92, 1, 96), waveM);
wave.rotation.x = -Math.PI / 2;
wave.position.set(0, .25, -2.5);
scene.add(wave);

// ---------------------------------------------------------------- traffic lights, and the orb's beams to them
const TL = [];
for (const x of AV) for (const z of ST) TL.push([x + .95, z + .95]);
TL.push([1.4, 5.4], [-1.4, 10.6]);
const tlPoleM = new THREE.InstancedMesh(new THREE.CylinderGeometry(.05, .06, 1.3).translate(0, .65, 0), mat(0x1E1B18), TL.length);
const tlLampM = new THREE.InstancedMesh(new THREE.SphereGeometry(.24, 12, 10), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), TL.length);
TL.forEach(([x, z], i) => { M4.compose(V.set(x, 0, z), Q.identity(), S.set(1, 1, 1)); tlPoleM.setMatrixAt(i, M4); M4.compose(V.set(x, 1.45, z), Q.identity(), S.set(1, 1, 1)); tlLampM.setMatrixAt(i, M4); });
scene.add(tlPoleM, tlLampM);
const beamPos = new Float32Array(TL.length * 6);
TL.forEach(([x, z], i) => beamPos.set([ORB.x, ORB.y - .9, ORB.z, x, 1.2, z], i * 6));
const beamG = new THREE.BufferGeometry();
beamG.setAttribute("position", new THREE.BufferAttribute(beamPos, 3));
const beamM = new THREE.LineBasicMaterial({ color: 0xE8735A, transparent: true, opacity: 0, toneMapped: false });
scene.add(new THREE.LineSegments(beamG, beamM));

// ---------------------------------------------------------------- traffic: cars on loops, then the jam
const LOOPS = [];   // rectangles along road centre lines, driven anticlockwise with a lane offset
const rect = (x0, z0, x1, z1) => [[x0, z0], [x1, z0], [x1, z1], [x0, z1]];
LOOPS.push(rect(-10, -12, 10, 3), rect(-5, -7, 5, 3), rect(-10, -7, 0, -2), rect(0, -12, 10, -2), rect(-5, -12, 5, -7),
  rect(5, -7, 10, 3), rect(-10, -2, -5, 3), rect(-10, -12, -5, -7), rect(0, -2, 5, 3), rect(-5, -2, 0, 3));
const loopInfo = LOOPS.map((pts) => {
  const seg = [];
  let len = 0;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i], b = pts[(i + 1) % pts.length];
    const l = Math.hypot(b[0] - a[0], b[1] - a[1]);
    seg.push({ a, b, l, s: len }); len += l;
  }
  return { seg, len };
});
function onLoop(li, s, out) {
  const { seg, len } = loopInfo[li];
  s = ((s % len) + len) % len;
  for (const g of seg) if (s <= g.s + g.l) {
    const u = (s - g.s) / g.l, dx = (g.b[0] - g.a[0]) / g.l, dz = (g.b[1] - g.a[1]) / g.l;
    out.x = g.a[0] + dx * g.l * u - dz * .38; out.z = g.a[1] + dz * g.l * u + dx * .38; out.r = Math.atan2(dx, dz); return out;
  }
  return out;
}
const CAR_N = 132;
const CARS = [];
for (let i = 0; i < CAR_N; i++) {
  const li = i % LOOPS.length;
  CARS.push({ li, off: hash(i * 5) * loopInfo[li].len, v: 1.6 + hash(i * 9) * 1.2, c: [0xFFFDF8, 0xE8735A, 0x8FB8E0, 0xF2B33D, 0x1E1B18, 0xBFD8C2, 0xD8CDE8][i % 7] });
}
// jam slots: two lanes on the bridge and down avenue x = 0, then along street z = 3 both ways
const SLOT = [];
for (let z = 10.2; z > -12 && SLOT.length < 70; z -= .82) for (const lx of [-.38, .38]) SLOT.push([lx, z, 0]);
for (let k = 1; SLOT.length < CAR_N; k++) for (const sx of [-1, 1]) for (const lz of [-.38, .38]) SLOT.push([sx * (1.2 + k * .82), 3 + lz, Math.PI / 2]);
const carG = new RoundedBoxGeometry(.42, .32, .78, 2, .08).translate(0, .23, 0);
const carM = new THREE.InstancedMesh(carG, mat(0xffffff, { roughness: .5 }), CAR_N);
carM.castShadow = true;
scene.add(carM);
// buses: three coral buses on the long loop, and the stops they serve
const BUS_N = 3;
const busM = new THREE.InstancedMesh(new RoundedBoxGeometry(.6, .58, 1.8, 2, .1).translate(0, .38, 0), mat(0xE8735A, { roughness: .5 }), BUS_N);
busM.castShadow = true;
scene.add(busM);
const STOPS = [[-10, -4.5, true], [-10, 0.5, false], [-4.5, 3, true], [3.5, 3, false], [10, -4.5, true], [10, -10, false], [-6, -12, true], [4, -12, false]];
const stopM = new THREE.InstancedMesh(new THREE.BoxGeometry(.9, .7, .35).translate(0, .35, 0), mat(0xFFFDF8), STOPS.length);
STOPS.forEach(([x, z], i) => { const vert = Math.abs(Math.abs(x) - 10) < .1; M4.compose(V.set(x + (vert ? (x < 0 ? -1.15 : 1.15) : 0), 0, z + (vert ? 0 : (z < 0 ? -1.15 : 1.15))), Q.setFromAxisAngle(UP, vert ? Math.PI / 2 : 0), S.set(1, 1, 1)); stopM.setMatrixAt(i, M4); });
scene.add(stopM);
const PPL = [];
STOPS.forEach(([x, z, busy], i) => { if (!busy) return; const vert = Math.abs(Math.abs(x) - 10) < .1; for (let k = 0; k < 4; k++) PPL.push({ stop: i, x: x + (vert ? (x < 0 ? -1.0 : 1.0) : (k - 1.5) * .28), z: z + (vert ? (k - 1.5) * .28 : (z < 0 ? -1.0 : 1.0)) }); });
const pplM = new THREE.InstancedMesh(new THREE.CapsuleGeometry(.09, .25, 4, 8).translate(0, .22, 0), mat(0x1E1B18), PPL.length);
scene.add(pplM);
const stopRingM = new THREE.InstancedMesh(new THREE.TorusGeometry(.75, .05, 6, 32).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xE8735A, transparent: true, opacity: .9, toneMapped: false }), STOPS.length);
scene.add(stopRingM);

// ambulance on street z = -2 heading west to the hospital
const amb = new THREE.Group();
scene.add(amb);
amb.add(add(new THREE.Mesh(new RoundedBoxGeometry(.5, .45, 1.0, 2, .08).translate(0, .3, 0), mat(0xFFFDF8))));
const ambStripe = new THREE.Mesh(new THREE.BoxGeometry(.52, .08, 1.02).translate(0, .32, 0), mat(0xD9483B));
amb.add(ambStripe);
const sirenM = new THREE.MeshBasicMaterial({ color: 0xD9483B, toneMapped: false });
const siren = new THREE.Mesh(new THREE.BoxGeometry(.2, .1, .14).translate(0, .58, 0), sirenM);
amb.add(siren);

// drones: a hub on the tallest tower, sixteen deliveries to rooftops
const hubB = B.reduce((a, b) => (b.h > a.h ? b : a));
const HUB = new THREE.Vector3(hubB.x, hubB.h + .3, hubB.z);
const DR_N = 16;
const DR = [];
const tall = B.filter((b) => !b.house && b !== hubB).sort((a, b) => hash(a.x * 3 + a.z) - hash(b.x * 3 + b.z)).slice(0, DR_N);
tall.forEach((b, i) => DR.push({ to: new THREE.Vector3(b.x, b.h + .25, b.z), t0: i * .19, dur: 2.4 + hash(i * 3) * 1.2 }));
const droneBody = new THREE.InstancedMesh(new RoundedBoxGeometry(.34, .1, .34, 2, .03), mat(0x1E1B18), DR_N);
const droneRot = new THREE.InstancedMesh(new THREE.CylinderGeometry(.13, .13, .015, 12), new THREE.MeshBasicMaterial({ color: 0xFFFDF8, transparent: true, opacity: .8 }), DR_N * 4);
const dronePkg = new THREE.InstancedMesh(new THREE.BoxGeometry(.18, .16, .18), mat(0xF2B33D), DR_N);
const droneLed = new THREE.InstancedMesh(new THREE.SphereGeometry(.05, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), DR_N);
scene.add(droneBody, droneRot, dronePkg, droneLed);

// the flooded street (z = 3, x 5..10), its sensor and the ping rings
const flood = new THREE.Mesh(new THREE.BoxGeometry(4.6, .1, 2.0), new THREE.MeshStandardMaterial({ color: 0x6FA3D8, roughness: .15, transparent: true, opacity: .85 }));
flood.position.set(7.5, .05, 3);
scene.add(flood);
const sensor = new THREE.Group();
sensor.position.set(7.4, 0, 4.4);
scene.add(sensor);
sensor.add(add(new THREE.Mesh(new THREE.CylinderGeometry(.05, .06, 1.4).translate(0, .7, 0), mat(0x1E1B18))));
const sensorLampM = new THREE.MeshBasicMaterial({ color: 0x3FA372, toneMapped: false });
sensor.add(new THREE.Mesh(new THREE.SphereGeometry(.16, 12, 10).translate(0, 1.5, 0), sensorLampM));
const pings = [0, 1, 2].map(() => { const m = new THREE.Mesh(new THREE.TorusGeometry(1, .05, 6, 48), new THREE.MeshBasicMaterial({ color: 0xD9483B, transparent: true, opacity: 0, toneMapped: false })); m.rotation.x = Math.PI / 2; m.position.set(7.4, .2, 4.4); scene.add(m); return m; });
// reroute arrows: chevrons streaming to the bridge along avenue x = 0 and street z = 3
const ARROW_N = 60;
const arrowM = new THREE.InstancedMesh(new THREE.ConeGeometry(.22, .5, 3).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xE8735A, toneMapped: false }), ARROW_N);
scene.add(arrowM);
const ARROW_PATHS = [[[0, -12], [0, 9]], [[-10.5, 3], [-.6, 3], [0, 6]], [[10.5, 3], [.6, 3], [0, 6]], [[-10, -7], [-.6, -7]], [[10, -7], [.6, -7]]];

// ---------------------------------------------------------------- simulation clock: city hours and car progress
// The hour advances slowly inside each line and spins over the first moments of the next one.
const HOURS = [[5.0, 5.8], [6.0, 7.4], [12.0, 12.9], [16.0, 16.3], [16.3, 17.0], [24.0, 24.15], [30.0, 30.5], [30.5, 30.7]];
function hourAt(t) {
  let h = HOURS[0][0];
  for (let k = 0; k < L.length; k++) {
    const [h0, h1] = HOURS[k];
    if (t < L[k] - .35) break;
    const prev = k ? HOURS[k - 1][1] : h0;
    h = lerp(prev, h0, ss(t, L[k] - .35, L[k] + .55)) + (h1 - h0) * ramp(t, L[k] + .55, E[k] + .2);
  }
  return h;
}
window.CITY_HOUR = hourAt;
// global traffic speed: hook slow, synced dawn quick and smooth, frozen from "freezes" until the fix
const FR = 60, NS = Math.ceil((DUR + 1) * FR);
const PROG = new Float32Array(NS + 1);
function speedAt(t) {
  if (t >= C.freezes && t < C.fixes + .6) return 0;
  if (t < C.syncs) return .45 + .35 * Math.abs(Math.sin(t * 1.7));
  if (t < L[2]) return lerp(.6, 1.25, ss(t, C.syncs, C.syncs + 1.2));
  return 1;
}
for (let i = 1; i <= NS; i++) PROG[i] = PROG[i - 1] + speedAt((i - .5) / FR) / FR;
const prog = (t) => { const f = clamp(t, 0, DUR) * FR, i = Math.floor(f); return lerp(PROG[i], PROG[Math.min(NS, i + 1)], f - i); };
const simT = (t) => (t >= C.freezes && t < C.fixes + .6 ? C.freezes : t);

// ---------------------------------------------------------------- sky and light by hour
const SKY = [[4.5, 0xCFC6D9], [6.0, 0xF4D9C8], [7.5, 0xF4E6D6], [12, 0xF1E9DC], [16, 0xF2DCC0], [17, 0xE9C3A6], [20, 0x7C7A99], [24, 0x3A3F5E], [24.5, 0x3A3F5E], [29.5, 0xE9D2C6], [31, 0xF1E9DC]];
function skyAt(h, out) {
  for (let i = 0; i < SKY.length - 1; i++) if (h <= SKY[i + 1][0]) return out.set(SKY[i][1]).lerp(tmpC2.set(SKY[i + 1][1]), sm(ramp(h, SKY[i][0], SKY[i + 1][0])));
  return out.set(SKY[SKY.length - 1][1]);
}
const night = (h) => { const x = ((h % 24) + 24) % 24; return x < 5.5 ? lerp(1, .55, ramp(x, 4.5, 5.5)) * (x < 4.5 ? 1 : 1) : x < 6.6 ? lerp(.55, 0, ramp(x, 5.5, 6.6)) : x > 18 ? ramp(x, 17.5, 20) : 0; };

// ---------------------------------------------------------------- camera keyframes
const K = [];
const key = (t, p, l, fov = 38) => K.push({ t, p: new THREE.Vector3(...p), l: new THREE.Vector3(...l), fov });
key(0, [0, 10.8, 3.6], [0, 8.6, -2.5], 42);
key(1.4, [1.4, 11.6, 6.5], [0, 7.4, -2.5], 42);
key(4.2, [13, 19, 27], [0, 1.5, 0], 38);
key(E[0], [-14, 17, 25], [0, 1, -.5], 38);
key(L[1] + .6, [4.5, 8.5, 13], [0, .4, -5], 40);
key(C.buses - .2, [-1, 10.5, 7], [-9.5, 0, -4], 40);
key(C.rush - .3, [-14, 12, 11], [-3, 0, -4], 40);
key(E[1] + .1, [-9, 14, 18], [0, 1, -2], 40);
key(L[2] + .5, [8, 13, 13], [1, 3.5, -4], 40);
key(C.grid - .2, [13, 11, 23], [3, 1, 6], 40);
key(C.hospitals - .3, [-21, 11, 8], [-11.5, 1, -4], 40);
key(E[2] + .1, [-21, 11.5, 5], [-11.5, 1, -4.5], 40);
key(L[3] + .5, [15, 8.5, 14], [7.4, .4, 3.4], 40);
key(C.reroutes - .3, [11, 12, 17], [5, .5, 3], 40);
key(C.ten, [0, 33, 15], [0, 0, -1], 40);
key(E[3], [0, 34, 16.5], [0, 0, 0], 40);
key(L[4] + .3, [5.5, 4.2, 15.5], [0, .6, 7], 42);
key(C.grid2 - .4, [7, 6, 17], [0, .6, 6], 42);
key(C.cuts + .2, [-15, 14, 21], [0, 0, 0], 40);
key(C.freezes + .2, [-14, 15, 22], [0, 0, 0], 40);
key(L[5] + .4, [0, 13.5, 15], [0, 6, -2.5], 40);
key(C.fixes + 1.4, [10, 15, 16], [0, 2, -2], 40);
key(C.nobody - .2, [1.8, 10.3, 2.4], [0, 9.1, -2.5], 40);
key(E[5] + .15, [2.2, 10.6, 3.4], [0, 9.1, -2.5], 40);
key(L[6] + .6, [3, 33, 10], [0, 0, 0], 40);
key(C.real - .2, [-6, 38, 14], [0, 0, 0], 40);
key(C.wrong + .4, [0, 58, 34], [0, 0, 1], 38);
key(DUR, [0, 62, 37], [0, 0, 1], 38);
const ease3 = (x) => (x < .5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);
function camAt(t) {
  let i = 0;
  while (i < K.length - 2 && t > K[i + 1].t) i++;
  const a = K[i], b = K[i + 1];
  const u = ease3(ramp(t, a.t, b.t));
  camera.position.lerpVectors(a.p, b.p, u);
  camera.position.y += Math.sin(Math.PI * u) * a.p.distanceTo(b.p) * .32;   // arc over the roofs between far keys
  const look = new THREE.Vector3().lerpVectors(a.l, b.l, u);
  camera.fov = lerp(a.fov, b.fov, u);
  // drift, and shake on the hard beats
  const sh = .22 * pulse(t, C.humansX ?? -9, .3) + .3 * pulse(t, C.bridge + .1, .35) + .38 * (ss(t, C.locks - .2, C.locks) - ss(t, C.freezes - .1, C.freezes)) * (.6 + .4 * Math.sin(t * 9)) + .25 * pulse(t, C.cuts, .4);
  camera.position.x += Math.sin(t * .37) * .15 + Math.sin(t * 31) * sh * .25;
  camera.position.y += Math.sin(t * .29 + 1) * .1 + Math.sin(t * 27 + 2) * sh * .2;
  camera.updateProjectionMatrix();
  camera.lookAt(look);
}

// ---------------------------------------------------------------- render at time t
const P = { x: 0, z: 0, r: 0 };
const WIN_DAY = col(0xB9C8D8), WIN_NIGHT = col(0xF0BE68), WIN_OFF = col(0x2A2D3E);
function renderAt(t) {
  const ts = simT(t);
  const h = hourAt(t), nt = night(h);
  const chaos = ss(t, C.locks - .2, C.locks + .4) * (1 - ss(t, C.fixes, C.fixes + 1.2));
  const frozen = t >= C.freezes && t < C.fixes + .6;
  // fix wave radius (0 at the orb, 26 beyond the far corner)
  const waveR = lerp(0, 26, ramp(t, C.fixes + .1, C.fixes + 2.1));
  const fixedAt = (x, z) => Math.hypot(x, z + 2.5) < waveR;

  // sky, fog, lights
  skyAt(h, tmpC);
  if (chaos > 0) tmpC.lerp(tmpC2.set(0xC98C78), chaos * .35);
  scene.background.copy(tmpC);
  scene.fog.color.copy(tmpC);
  const sunA = (((h % 24) + 24) % 24 - 6) / 12 * Math.PI;
  const day = clamp(Math.sin(sunA));
  sun.position.set(Math.cos(sunA) * 26 + 4, 6 + Math.max(day, .25) * 26, 14);
  sun.intensity = lerp(.35, 2.3, day) * (1 - nt * .6);
  sun.color.set(day < .4 ? 0xFFC9A0 : 0xFFF3E2).lerp(tmpC2.set(0xA9B4FF), nt);
  hemi.intensity = lerp(.95, .45, nt);
  hemi.color.set(0xFFF6EA).lerp(tmpC2.set(0x9DA6D8), nt);
  hemi.groundColor.set(0xCDBFA8).lerp(tmpC2.set(0x3A3F5E), nt);
  bloom.strength = lerp(.2, .42, nt);
  bloom.threshold = lerp(.92, .74, nt);

  // the orb: wakes in the hook, pulses on every command, glitches on "nobody"
  const wake = ss(t, .1, 1.3);
  const glitch = ss(t, C.nobody - .1, C.nobody + .2) * (1 - ss(t, E[5] + .3, E[5] + .6));
  const cmd = pulse(t, C.syncs, .3) + pulse(t, C.reroutes, .3) + pulse(t, C.fixes, .4) + pulse(t, C.grid, .3);
  orbCoreM.emissiveIntensity = (.25 + wake * 1.1 + cmd * 1.4) * (1 - glitch * .6 * (Math.sin(t * 47) > 0 ? 1 : 0));
  orb.scale.setScalar(lerp(.4, 1, sm(wake)) * (1 + cmd * .12));
  orb.position.set(ORB.x + glitch * Math.sin(t * 61) * .12, ORB.y + Math.sin(t * 1.3) * .18, ORB.z);
  ring1.rotation.set(Math.PI / 2 + Math.sin(t * .7) * .4, t * .9, 0);
  ring2.rotation.set(Math.PI / 2.6 + glitch * Math.sin(t * 40), -t * 1.3, t * .4);
  orbLight.intensity = (wake * 3 + cmd * 9) * (.4 + nt);
  orbCoreM.color.set(0xE8735A).lerp(tmpC2.set(0x8FB8E0), glitch * (Math.sin(t * 23) > .3 ? 1 : 0));
  orbCoreM.emissive.copy(orbCoreM.color);

  // fix wave
  waveM.opacity = .9 * (1 - ramp(t, C.fixes + 1.4, C.fixes + 2.3)) * (t > C.fixes + .1 ? 1 : 0);
  wave.scale.setScalar(Math.max(.01, waveR));

  // traffic lights: random cycling, the sync wave from the orb, red flashing in the chaos, green after the fix
  TL.forEach(([x, z], i) => {
    const d = Math.hypot(x, z + 2.5);
    const synced = t > C.syncs + d * .045;
    let c = (Math.floor(ts * .7 + hash(i * 3) * 4) % 2 === 0) ? 0xD9483B : 0x3FA372;
    if (synced) c = 0x3FA372;
    if (chaos > .3 && !fixedAt(x, z)) c = Math.sin(t * 9 + i) > 0 ? 0xD9483B : 0x5a2a24;
    if (t > C.fixes && fixedAt(x, z)) c = 0x3FA372;
    tmpC.set(c);
    if (nt > .3) tmpC.multiplyScalar(1.3);
    tlLampM.setColorAt(i, tmpC);
  });
  tlLampM.instanceColor.needsUpdate = true;
  beamM.opacity = .85 * (ss(t, C.syncs - .15, C.syncs + .1) * (1 - ss(t, C.syncs + 1.4, C.syncs + 2.2)) + ss(t, C.reroutes - .1, C.reroutes + .1) * (1 - ss(t, C.reroutes + 1, C.reroutes + 1.6)) * .7);

  // cars
  const pg = prog(t);
  CARS.forEach((c, i) => {
    onLoop(c.li, c.off + c.v * pg * 2.2 + (t < C.syncs ? Math.sin(ts * 1.1 + i) * .35 : 0), P);
    let x = P.x, z = P.z, r = P.r, y = 0;
    const jIn = ss(t, C.reroutes + .15 + (i % 40) * .03, C.reroutes + 1.5 + (i % 40) * .03);
    const fx = t > C.fixes ? ss(t, C.fixes + .2 + Math.hypot(P.x, P.z + 2.5) * .07, C.fixes + 1.3 + Math.hypot(P.x, P.z + 2.5) * .07) : 0;
    const j = jIn * (1 - fx);
    if (j > 0) {
      const [sx, sz, sr] = SLOT[i];
      const crawl = t < C.locks ? (1 - ramp(t, C.ten, C.locks)) * .0 : 0;
      x = lerp(x, sx, j); z = lerp(z, sz + crawl, j); r = j > .5 ? sr : r;
      y = Math.sin(Math.PI * clamp(j)) * .9 * (1 - fx);
      if (j > .98 && !frozen) { x += Math.sin(t * 13 + i) * .02; }
    }
    M4.compose(V.set(x, y, z), Q.setFromAxisAngle(UP, r), S.set(1, 1, 1));
    carM.setMatrixAt(i, M4);
    tmpC.set(c.c);
    if (j > .9) tmpC.lerp(tmpC2.set(0xD9483B), clamp((t - C.locks + .4) * 2) * .8);
    carM.setColorAt(i, tmpC);
  });
  carM.instanceMatrix.needsUpdate = true;
  carM.instanceColor.needsUpdate = true;

  // buses on the big loop; people board when a bus passes their stop
  for (let b = 0; b < BUS_N; b++) {
    onLoop(0, b * loopInfo[0].len / BUS_N + pg * 3.4, P);
    M4.compose(V.set(P.x, 0, P.z), Q.setFromAxisAngle(UP, P.r), S.set(1, 1, 1));
    busM.setMatrixAt(b, M4);
  }
  busM.instanceMatrix.needsUpdate = true;
  const showStops = ss(t, C.buses - .3, C.buses + .2) * (1 - ss(t, E[1], E[1] + .5));
  PPL.forEach((p, i) => {
    const board = ss(t, C.waiting + .2 + p.stop * .18 + (i % 4) * .05, C.waiting + .5 + p.stop * .18 + (i % 4) * .05);
    const vis = (t < L[2] ? 1 : ss(t, L[2] + 1, L[2] + 2)) * (1 - board * (t < L[2] ? 1 : 0));
    M4.compose(V.set(p.x, 0, p.z), Q.identity(), S.setScalar(Math.max(.001, vis)));
    pplM.setMatrixAt(i, M4);
  });
  pplM.instanceMatrix.needsUpdate = true;
  STOPS.forEach(([x, z, busy], i) => {
    const s = busy ? showStops * (1 + .15 * Math.sin(t * 6 + i)) : 0;
    M4.compose(V.set(x, .08, z), Q.identity(), S.setScalar(Math.max(.001, s)));
    stopRingM.setMatrixAt(i, M4);
  });
  stopRingM.instanceMatrix.needsUpdate = true;

  // ambulance: drives in along street z = -2 at noon; the hospital is ready before it arrives
  const au = ss(t, C.hospitals - .6, E[2] + .2);
  amb.position.set(lerp(6, -10.4, au), 0, -2 - .38);
  amb.rotation.y = -Math.PI / 2;
  amb.visible = t > C.hospitals - .8 && t < E[2] + 1.5;
  sirenM.color.set(Math.sin(t * 14) > 0 ? 0xD9483B : 0x8FB8E0);
  const ready = ss(t, C.hospitals - .2, C.hospitals + .3) * (1 - ss(t, E[2] + .6, E[2] + 1.2));
  hospRing.material.opacity = ready * (.6 + .4 * Math.sin(t * 5));
  hospRing.scale.setScalar(1 + .08 * Math.sin(t * 5));

  // drones: noon deliveries, stalled (hovering, red) in the chaos
  const drOn = ss(t, C.drones - .4, C.drones + .2) * (1 - ss(t, C.freezes + .1, C.freezes + .5)) + ss(t, C.fixes + .8, C.fixes + 1.4) * (1 - ss(t, E[5], E[5] + .4));
  DR.forEach((d, i) => {
    const tt = (t - C.drones - d.t0);
    let u = ((tt / d.dur) % 1 + 1) % 1;
    const stall = t > C.deliveries - .2 && t < C.fixes + .8;
    if (stall) u = (((C.deliveries - .2 - C.drones - d.t0) / d.dur) % 1 + 1) % 1;
    const out = u < .5, k = out ? sm(u * 2) : sm((1 - u) * 2);
    V.lerpVectors(HUB, d.to, k);
    V.y += Math.sin(Math.PI * k) * 2.4 + (stall ? Math.sin(t * 3 + i) * .08 : 0);
    const sc = Math.max(.001, drOn);
    M4.compose(V, Q.setFromAxisAngle(UP, i), S.setScalar(sc));
    droneBody.setMatrixAt(i, M4);
    for (let r = 0; r < 4; r++) {
      const a = r * Math.PI / 2 + Math.PI / 4;
      M4.compose(tmpV.set(V.x + Math.cos(a + i) * .22 * sc, V.y + .07 * sc, V.z + Math.sin(a + i) * .22 * sc), Q.identity(), S.setScalar(sc));
      droneRot.setMatrixAt(i * 4 + r, M4);
    }
    M4.compose(tmpV.set(V.x, V.y - .14 * sc, V.z), Q.identity(), S.setScalar(out && !stall ? sc : .001));
    dronePkg.setMatrixAt(i, M4);
    M4.compose(tmpV.set(V.x, V.y + .08 * sc, V.z), Q.identity(), S.setScalar(sc));
    droneLed.setMatrixAt(i, M4);
    droneLed.setColorAt(i, tmpC.set(stall ? (Math.sin(t * 10 + i) > 0 ? 0xD9483B : 0x401010) : 0x3FA372));
  });
  for (const m of [droneBody, droneRot, dronePkg, droneLed]) m.instanceMatrix.needsUpdate = true;
  droneLed.instanceColor.needsUpdate = true;

  // power: each district is on unless the chaos cut reached it and the fix wave has not
  const distOn = [];
  for (let d = 0; d < DIST_N; d++) {
    const cutT = C.cuts + .1 + [3, 1, 0, 2, 7, 5, 4, 6, 8][d] * .16;
    const cx = [-7.5, -2.5, 2.5, 7.5][d % 4] ?? 0, cz = d < 4 ? -9.5 : d < 8 ? .5 : 13;
    const back = t > C.fixes && fixedAt(d === 8 ? 0 : cx, d === 8 ? 12 : cz);
    distOn.push(t > cutT && !back ? 0 : 1);
  }
  WB.forEach((w, i) => {
    const on = distOn[w.b.dist];
    const flick = on && nt > .2 ? (hash(i * 7 + Math.floor(t * 2) * 13) > .93 ? .55 : 1) : 1;
    tmpC.copy(w.day).lerp(WIN_NIGHT, nt * (hash(i) > .25 ? 1 : .3) * flick);
    if (!on) tmpC.copy(WIN_OFF);
    winM.setColorAt(i, tmpC);
  });
  winM.instanceColor.needsUpdate = true;
  // grid lines and pulses: flowing at noon, red then dark in the cut, back after the fix
  const gridRed = ss(t, C.grid2 - .2, C.grid2 + .3);
  gridMats.forEach((m, i) => {
    const on = distOn[i];
    tmpC.set(0xF2B33D).lerp(tmpC2.set(0xD9483B), gridRed * (t < C.fixes ? 1 : 0));
    if (!on) tmpC.set(0x3a3530);
    if (i === 6) tmpC.lerp(tmpC2.set(0xFFF0A0), pulse(t, C.energy, .5));
    m.color.copy(tmpC);
    m.opacity = lerp(.1, .95, ss(t, C.grid - .5, C.grid) * (1 - ss(t, L[5] + 2, L[5] + 3)) + ss(t, C.grid2 - .5, C.grid2) * (1 - ss(t, C.fixes + 2, C.fixes + 3)));
  });
  const flowOn = ss(t, C.grid - .5, C.grid) ;
  for (let li = 0; li < SUB.length; li++) for (let k = 0; k < PULSE_N; k++) {
    const u = ((prog(t) * .35 + k / PULSE_N + hash(li) * .3) % 1);
    gridCurves[li].getPointAt(u, V);
    const s = flowOn * distOn[li] * (t >= C.freezes && t < C.fixes ? 0 : 1);
    M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, s * (li === 6 ? 1.4 : 1))));
    pulseM.setMatrixAt(li * PULSE_N + k, M4);
    pulseM.setColorAt(li * PULSE_N + k, tmpC.set(gridRed > .5 && t < C.fixes ? 0xD9483B : 0xFFE08A));
  }
  pulseM.instanceMatrix.needsUpdate = true;
  pulseM.instanceColor.needsUpdate = true;
  blades.forEach((b, i) => { b.rotation.z = (frozen ? C.freezes : t) * (1.4 + i * .2); });

  // flood, sensor, pings
  const fl = ss(t, C.flooded - .4, C.flooded + .6) * (1 - ss(t, C.fixes + .5, C.fixes + 1.5));
  flood.scale.set(Math.max(.01, fl), 1, Math.max(.01, fl));
  flood.visible = fl > .01;
  sensorLampM.color.set(t > C.sensor - .1 && t < C.fixes + .5 ? (Math.sin(t * 10) > 0 ? 0xD9483B : 0x6a1a14) : 0x3FA372);
  pings.forEach((p, k) => {
    const a = C.sensor + k * .35, u = ramp(t, a, a + 1.1);
    p.scale.setScalar(.3 + u * 3.2);
    p.material.opacity = t > a && u < 1 ? .9 * (1 - u) : 0;
  });
  // reroute chevrons
  const arOn = ss(t, C.reroutes - .1, C.reroutes + .3) * (1 - ss(t, C.locks + .4, C.locks + 1));
  for (let i = 0; i < ARROW_N; i++) {
    const path = ARROW_PATHS[i % ARROW_PATHS.length];
    const segs = path.length - 1;
    let u = ((t * .45 + hash(i * 3)) % 1);
    const si = Math.min(segs - 1, Math.floor(u * segs)), su = u * segs - si;
    const a = path[si], b = path[si + 1];
    const x = lerp(a[0], b[0], su), z = lerp(a[1], b[1], su);
    M4.compose(V.set(x, .45, z), Q.setFromAxisAngle(UP, Math.atan2(b[0] - a[0], b[1] - a[1])), S.setScalar(Math.max(.001, arOn)));
    arrowM.setMatrixAt(i, M4);
  }
  arrowM.instanceMatrix.needsUpdate = true;

  // grade: freeze desaturates, the chaos reddens the edges, small flashes on hard cuts
  const fz = t >= C.freezes ? ss(t, C.freezes, C.freezes + .25) * (1 - ss(t, L[5] - .2, L[5] + .3)) : 0;
  grade.uniforms.uSat.value = 1 - fz * .75;
  grade.uniforms.uTint.value.set(1 - fz * .08, 1 - fz * .02, 1 + fz * .06);
  grade.uniforms.uRed.value = chaos * .55 * (1 - fz);
  grade.uniforms.uFlash.value = .35 * pulse(t, C.humans ?? -9, .12) + .3 * pulse(t, C.freezes, .1) + .3 * pulse(t, C.fixes + .1, .12);
  grade.uniforms.uTime.value = t;

  camAt(t);
  composer.render();
}
const tmpV = new THREE.Vector3();

const ready = (async () => {
  renderer.compile(scene, camera);
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["city"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
window.CITY_RENDER = renderAt;
