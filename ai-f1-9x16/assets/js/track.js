// AI F1 reel: the 3D circuit. A cream low-poly racetrack on a floating tile, run for one race by an AI race engineer
// (the coral orb above the infield). Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek.
// Cue times come from the voice (window.CT, written by build/generate.py). Story, beat by beat:
//   hook      lap 1: the pack, the orb, the radio call, car #7 dives into the pits and the field streams past (P20)
//   rain      the sky turns, rain and spray; slicks slide, #7 on blue wets carves past six cars
//   listening sound rings off the engine, then the AI marks the hairpin and #7 dives up the inside
//   crash     lap 40: the AI's predicted crash paths, #7 lifts, the two leaders collide, #7 threads through in slow motion
//   final lap the flag, both coral cars nose to tail, "let him through": #11 passes before the line
//   title     dusk, fireworks, #11 celebrates; #7 nods
//   real      thousands of ghost simulations stream round the circuit, from above
//   close     the whole circuit, small, under the orb
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

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
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), V2 = new THREE.Vector3(), V3 = new THREE.Vector3(), S = new THREE.Vector3();
const UP = new THREE.Vector3(0, 1, 0);
const pulse = (t, a, w = .35) => Math.exp(-(((t - a) / w) ** 2));
const bump = (t, a, b, e = .35) => ss(t, a, a + e) * (1 - ss(t, b - e, b));
const INK = 0x1E1B18, CORAL = 0xE8735A, NAVY = 0x34508F, CREAM = 0xFFFDF8, GOLD = 0xF2B33D, RED = 0xD9483B, BLUE = 0x3A7BD5;
// monotone piecewise-cubic through (x, y) points
function pchip(pts) {
  const n = pts.length, xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  const dl = [], m = new Array(n).fill(0);
  for (let i = 0; i < n - 1; i++) dl.push((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]));
  m[0] = dl[0]; m[n - 1] = dl[n - 2];
  for (let i = 1; i < n - 1; i++) m[i] = dl[i - 1] * dl[i] <= 0 ? 0 : (dl[i - 1] + dl[i]) / 2;
  return (x) => {
    if (x <= xs[0]) return ys[0] + m[0] * (x - xs[0]);
    if (x >= xs[n - 1]) return ys[n - 1] + m[n - 1] * (x - xs[n - 1]);
    let i = 0; while (x > xs[i + 1]) i++;
    const h = xs[i + 1] - xs[i], u = (x - xs[i]) / h;
    return (2 * u ** 3 - 3 * u * u + 1) * ys[i] + (u ** 3 - 2 * u * u + u) * h * m[i] + (-2 * u ** 3 + 3 * u * u) * ys[i + 1] + (u ** 3 - u * u) * h * m[i + 1];
  };
}

// ---------------------------------------------------------------- renderer, scene, post
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NeutralToneMapping ?? THREE.ACESFilmicToneMapping;

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
const ENV = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.background = col(0xF1E9DC);
scene.fog = new THREE.Fog(0xF1E9DC, 80, 260);
const camera = new THREE.PerspectiveCamera(40, W / H, .05, 600);

const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .25, .5, .9);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1 }, uVig: { value: .28 }, uFlash: { value: 0 }, uCool: { value: 0 }, uRed: { value: 0 },
    uBlur: { value: 0 }, uCA: { value: 0 }, uBars: { value: 0 }, uScan: { value: 0 }, uCon: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uCool, uRed, uBlur, uCA, uBars, uScan, uCon; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 uv = vUv, d = vec2(.5, .5) - uv;
      vec3 c = vec3(0.);
      for (int i = 0; i < 8; i++) {                      // radial speed blur + chromatic fringes
        vec2 o = d * uBlur * float(i) / 7.;
        c.r += texture2D(tDiffuse, uv + o + d * uCA).r;
        c.g += texture2D(tDiffuse, uv + o).g;
        c.b += texture2D(tDiffuse, uv + o - d * uCA).b;
      }
      c /= 8.;
      float g = dot(c, vec3(.299, .587, .114));
      c = mix(vec3(g), c, uSat);
      c = mix(c, c * vec3(.92, .98, 1.08), uCool);
      c = (c - .5) * (1. + uCon) + .5;
      vec2 q = vUv - .5; float r = dot(q, q);
      c *= 1. - r * uVig * 2.2;
      c = mix(c, c * vec3(1.25, .55, .5), uRed * smoothstep(.05, .32, r));
      // AI vision: a coral grid and a scan line sweeping down
      vec2 px = vUv * vec2(1080., 1920.);
      float grid = max(step(.96, fract(px.x / 54.)), step(.96, fract(px.y / 54.)));
      float sweep = 1. - smoothstep(0., .012, abs(fract(-vUv.y - uTime * .45) - .5));
      c = mix(c, vec3(.91, .45, .35), uScan * (.22 * grid + .5 * sweep));
      c += (h(floor(px) + fract(uTime * 7.13) * 97.) - .5) * .026;
      c = mix(c, vec3(1., .99, .96), uFlash);
      float bh = uBars * 150. / 1920.;
      if (vUv.y < bh || vUv.y > 1. - bh) c = vec3(.075, .065, .06);
      gl_FragColor = vec4(c, 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0xfff6ea, 0xcdbfa8, .95);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff1dc, 2.1);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -.0005;
sun.shadow.normalBias = .02;
scene.add(sun, sun.target);
// a soft key light that rides with the camera for the face close-ups
const faceKey = new THREE.PointLight(0xfff0e0, 0, 5, 1.2);
scene.add(faceKey);
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .88, metalness: 0, ...o });
const add = (m, cast = true, recv = true) => { m.castShadow = cast; m.receiveShadow = recv; scene.add(m); return m; };

// ---------------------------------------------------------------- the circuit
// a tall loop that fits the 9:16 frame: main straight on the right (x = 20, run towards -z), turn 1 at the top,
// a back section down the left, an infield S, the hairpin at the bottom left, a sweeping return
const CP = [[20, 26], [20, 0], [20, -26], [18.5, -36], [10, -42], [-4, -42], [-15, -38], [-20, -28], [-20, -12], [-15, -4],
  [-6, -2], [-3, 6], [-10, 12], [-19, 18], [-21, 30], [-14, 40], [-3, 38], [3, 30], [10, 32], [16, 38], [20, 34]];
const curve = new THREE.CatmullRomCurve3(CP.map(([x, z]) => new THREE.Vector3(x, 0, z)), true, "centripetal");
const NS = 1600;
const SP = curve.getSpacedPoints(NS);
const TL = curve.getLength();
const TX = new Float32Array(NS + 1), TZ = new Float32Array(NS + 1), KAP = new Float32Array(NS + 1);
for (let i = 0; i <= NS; i++) {
  const a = SP[(i - 1 + NS) % NS], b = SP[(i + 1) % NS];
  const dx = b.x - a.x, dz = b.z - a.z, l = Math.hypot(dx, dz);
  TX[i] = dx / l; TZ[i] = dz / l;
}
for (let i = 0; i <= NS; i++) {
  const j = (i + 1) % NS;
  KAP[i] = (TX[i] * TZ[j] - TZ[i] * TX[j]) / (TL / NS);
}
const KS = new Float32Array(NS + 1);          // smoothed curvature
for (let i = 0; i < NS; i++) { let s = 0; for (let k = -6; k <= 6; k++) s += KAP[(i + k + NS) % NS]; KS[i] = s / 13; }
KS[NS] = KS[0];
const HW = 2.0;                               // track half width
const wrap = (d) => ((d % TL) + TL) % TL;
// position on the track at distance d with lateral offset lane (lane > 0: towards the normal (tz, -tx))
function trackAt(d, lane, out) {
  const f = wrap(d) / TL * NS, i = Math.floor(f) % NS, u = f - Math.floor(f), j = (i + 1) % NS;
  const x = lerp(SP[i].x, SP[j].x, u), z = lerp(SP[i].z, SP[j].z, u);
  const tx = lerp(TX[i], TX[j], u), tz = lerp(TZ[i], TZ[j], u);
  out.x = x + tz * lane; out.z = z - tx * lane; out.tx = tx; out.tz = tz; out.k = lerp(KS[i], KS[j], u);
  return out;
}
const nearestD = (x, z) => { let bi = 0, bd = 1e9; for (let i = 0; i < NS; i++) { const d = (SP[i].x - x) ** 2 + (SP[i].z - z) ** 2; if (d < bd) { bd = d; bi = i; } } return bi / NS * TL; };
const D_SS = nearestD(20, 24), D_SE = nearestD(20, -24), D_SF = nearestD(20, -10);
const D_PIN = D_SS + 1, D_BOX = D_PIN + 20, D_POUT = D_BOX + 24;
const D_CRASH = D_SE + 7;
let D_ATT = 0; { let bk = 0; for (let i = 0; i < NS; i++) { const p = SP[i]; if (p.z > 10 && p.x < -12 && Math.abs(KS[i]) > bk) { bk = Math.abs(KS[i]); D_ATT = i / NS * TL; } } }
const PITLAT = -4.7;                           // the pit lane runs on the outside of the main straight (+x)
const pitLane = (d) => PITLAT * (ss(d, D_PIN, D_PIN + 9) - ss(d, D_POUT - 9, D_POUT));
const TA = { x: 0, z: 0, tx: 0, tz: 0, k: 0 }, TB = { x: 0, z: 0, tx: 0, tz: 0, k: 0 };

// a ribbon along the track between lateral offsets a(d) and b(d), from d0 to d1, at height y, with a colour per segment
function ribbon(d0, d1, a, b, y, colorAt, step = TL / NS) {
  const pos = [], cols = [], idx = [];
  let n = 0;
  for (let d = d0; d <= d1 + 1e-6; d += step) {
    trackAt(d, a(d), TA); trackAt(d, b(d), TB);
    pos.push(TA.x, y, TA.z, TB.x, y, TB.z);
    const c = colorAt(d); cols.push(c.r, c.g, c.b, c.r, c.g, c.b);
    if (n) { const k = 2 * n; idx.push(k - 2, k, k - 1, k - 1, k, k + 1); }
    n++;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}
const vcol = (o = {}) => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .9, ...o });
const cst = (h) => { const c = col(h); return () => c; };
// tile and grass
const tile = add(new THREE.Mesh(new RoundedBoxGeometry(66, 1.6, 104, 4, .7), mat(0xEADFCB)), false, true);
tile.position.set(2, -.8, -1);
const grass = add(new THREE.Mesh(new RoundedBoxGeometry(63, .1, 101, 2, .05), mat(0xB4C99B)), false, true);
grass.position.set(2, .0, -1);
const edge = new THREE.Mesh(new RoundedBoxGeometry(66.4, .5, 104.4, 4, .25), mat(INK, { roughness: .6 }));
edge.position.set(2, -1.45, -1); scene.add(edge);
// verge, asphalt, white edge lines, kerbs on the corners
add(new THREE.Mesh(ribbon(0, TL, () => -HW - 1.3, () => HW + 1.3, .055, cst(0xE6DCC8)), vcol()), false, true);
const asphaltM = new THREE.MeshStandardMaterial({ color: 0x7E7872, roughness: .85 });
add(new THREE.Mesh(ribbon(0, TL, () => -HW, () => HW, .07, cst(0xffffff)), asphaltM), false, true);
const lineM = new THREE.MeshBasicMaterial({ color: 0xF6F1E7 });
for (const s of [-1, 1]) add(new THREE.Mesh(ribbon(0, TL, () => s * (HW - .16), () => s * (HW - .08), .078, cst(0xffffff)), lineM), false, false);
{
  const red = col(RED), wht = col(0xF6F1E7);
  for (const s of [-1, 1]) {
    // kerb where the smoothed curvature is high (both sides of the corner), striped every ~.5
    let start = -1;
    for (let i = 0; i <= NS; i++) {
      const on = i < NS && Math.abs(KS[i]) > .05;
      if (on && start < 0) start = i;
      if (!on && start >= 0) {
        const d0 = Math.max(0, start - 8) / NS * TL, d1 = Math.min(NS, i + 8) / NS * TL;
        add(new THREE.Mesh(ribbon(d0, d1, () => s * HW, () => s * (HW + .5), .085, (d) => (Math.floor(d / .55) % 2 ? red : wht)), vcol({ roughness: .7 })), false, true);
        start = -1;
      }
    }
  }
}
// gravel trap round turn 1 (where the crash happens) and at the hairpin
add(new THREE.Mesh(ribbon(D_SE - 2, D_SE + 26, () => HW + .55, (d) => HW + 1.2 + 4.2 * bump(d, D_SE - 2, D_SE + 26, 8), .06, cst(0xE3CFA6)), vcol({ roughness: 1 })), false, true);
add(new THREE.Mesh(ribbon(D_ATT - 12, D_ATT + 12, (d) => -HW - .55, (d) => -HW - 1.2 - 3.5 * bump(d, D_ATT - 12, D_ATT + 12, 6), .06, cst(0xE3CFA6)), vcol({ roughness: 1 })), false, true);
// start / finish: chequered strip across the track
const checkTex = (nx, ny) => { const c = document.createElement("canvas"); c.width = nx * 16; c.height = ny * 16; const g = c.getContext("2d");
  for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) { g.fillStyle = (i + j) % 2 ? "#1E1B18" : "#FFFDF8"; g.fillRect(i * 16, j * 16, 16, 16); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.magFilter = THREE.NearestFilter; return t; };
{
  trackAt(D_SF, 0, TA);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(2 * HW, .7), new THREE.MeshBasicMaterial({ map: checkTex(12, 2) }));
  m.rotation.x = -Math.PI / 2; m.rotation.z = Math.atan2(TA.tx, TA.tz) + Math.PI / 2; m.position.set(TA.x, .082, TA.z); scene.add(m);
}
// pit lane, pit wall, garages
add(new THREE.Mesh(ribbon(D_PIN, D_POUT, (d) => pitLane(d) - 1.2 * ss(d, D_PIN, D_PIN + 9) * (1 - ss(d, D_POUT - 9, D_POUT)), (d) => pitLane(d) + 1.2, .065, cst(0xffffff)), asphaltM), false, true);
add(new THREE.Mesh(ribbon(D_PIN + 2, D_POUT - 2, (d) => pitLane(d) * .5 - .6 + 0 * d, (d) => pitLane(d) * .5 - .5, .07, cst(0xF2B33D)), new THREE.MeshBasicMaterial({ color: GOLD })), false, false);
{
  const z0 = SP[Math.round(D_PIN / TL * NS)].z, z1 = SP[Math.round(D_POUT / TL * NS)].z;
  const wall = add(new THREE.Mesh(new THREE.BoxGeometry(.25, .45, Math.abs(z0 - z1) - 18), mat(CREAM)));
  wall.position.set(20 + HW + .85, .22, (z0 + z1) / 2);
  const stripe = new THREE.Mesh(new THREE.BoxGeometry(.27, .1, Math.abs(z0 - z1) - 18), mat(CORAL)); stripe.position.set(20 + HW + .85, .36, (z0 + z1) / 2); scene.add(stripe);
  const garage = add(new THREE.Mesh(new THREE.BoxGeometry(3.4, 2.4, 50).translate(0, 1.2, 0), mat(0xF4E9D8)));
  garage.position.set(20 + 4.7 + 3.1, 0, 0);
  const roof = add(new THREE.Mesh(new THREE.BoxGeometry(3.9, .25, 50.6), mat(CREAM))); roof.position.set(20 + 4.7 + 3.0, 2.5, 0);
  for (let k = 0; k < 11; k++) {
    const z = -20 + k * 4;
    const ours = Math.abs(z - SP[Math.round(D_BOX / TL * NS)].z) < 2;
    const door = new THREE.Mesh(new THREE.PlaneGeometry(3, 1.7), new THREE.MeshBasicMaterial({ color: ours ? 0x3a2a24 : 0x2c2825 }));
    door.rotation.y = -Math.PI / 2; door.position.set(20 + 4.7 + 1.38, .86, z); scene.add(door);
    const frame = new THREE.Mesh(new THREE.BoxGeometry(.1, .28, 3.3), mat(ours ? CORAL : [NAVY, 0x3FA372, 0xF08A3C, 0x2E9AA6, 0x7E5BB0][k % 5]));
    frame.position.set(20 + 4.7 + 1.36, 1.86, z); scene.add(frame);
  }
}
// grandstand on the inside of the main straight, a second one at the hairpin
const FANS = [];
function stand(x0, z0, len, rows, dirX) {
  for (let s = 0; s < rows; s++) {
    const b = add(new THREE.Mesh(new THREE.BoxGeometry(.8, .5 + s * .55, len).translate(0, (.5 + s * .55) / 2, 0), mat(s % 2 ? 0xF2DCC0 : 0xE9D3B3)));
    b.position.set(x0 - dirX * s * .8, 0, z0);
    for (let u = -len / 2 + .3; u < len / 2 - .2; u += .36) FANS.push({ x: x0 - dirX * s * .8, z: z0 + u, y: .5 + s * .55 + .13 });
  }
  const r = add(new THREE.Mesh(new THREE.BoxGeometry(rows * .8 + .6, .14, len + .4), mat(CREAM)));
  r.position.set(x0 - dirX * (rows - 1) * .4, .5 + rows * .55 + 1.1, z0);
  for (const sz of [-1, 1]) { const p = add(new THREE.Mesh(new THREE.CylinderGeometry(.07, .07, .5 + rows * .55 + 1.1).translate(0, (.5 + rows * .55 + 1.1) / 2, 0), mat(0xd9cbb2))); p.position.set(x0 - dirX * (rows - 1) * .8, 0, z0 + sz * len / 2); }
}
stand(15.6, 0, 40, 5, 1);
{ trackAt(D_ATT, 0, TA); }
const fanM = new THREE.InstancedMesh(new THREE.SphereGeometry(.13, 12, 9), mat(0xffffff, { roughness: .7 }), FANS.length);
scene.add(fanM);
const fanBase = FANS.map((f, i) => (hash(i) < .45 ? CORAL : hash(i * 3) < .4 ? CREAM : hash(i * 5) < .5 ? NAVY : hash(i * 7) < .5 ? GOLD : INK));
// start gantry over the finish line with five lights, and the flag
const GANTRY = (() => {
  trackAt(D_SF, 0, TA);
  const g = new THREE.Group(); g.position.set(TA.x, 0, TA.z); g.rotation.y = Math.atan2(TA.tx, TA.tz); scene.add(g);
  for (const s of [-1, 1]) { const p = add(new THREE.Mesh(new THREE.BoxGeometry(.25, 4.2, .25).translate(0, 2.1, 0), mat(CREAM))); p.position.x = s * (HW + 1.1); g.add(p); }
  const beam = add(new THREE.Mesh(new THREE.BoxGeometry(2 * HW + 2.6, .5, .4), mat(INK, { roughness: .5 }))); beam.position.y = 4.2; g.add(beam);
  const lights = [];
  for (let k = 0; k < 5; k++) { const m = new THREE.MeshBasicMaterial({ color: 0x3a1a16, toneMapped: false }); const l = new THREE.Mesh(new THREE.CircleGeometry(.17, 20), m); l.position.set(-1.2 + k * .6, 4.2, .21); g.add(l); lights.push(m); }
  return { g, lights };
})();
const FLAG = (() => {
  const geo = new THREE.PlaneGeometry(1.8, 1.2, 14, 8);
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: checkTex(9, 6), side: THREE.DoubleSide, roughness: .8 }));
  m.castShadow = true;
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, 2.6), mat(CREAM)); pole.position.set(0, -.6, 0);
  const g = new THREE.Group(); g.add(m, pole); GANTRY.g.add(g);
  g.position.set(HW + 1.1, 4.8, 0);
  const base = geo.attributes.position.array.slice();
  return { g, m, geo, base };
})();
// trees and tyre walls
const TREES = [];
for (let k = 0; TREES.length < 140 && k < 4000; k++) {
  const x = -29 + hash(k * 3.1) * 62, z = -50 + hash(k * 7.7) * 98;
  let ok = true;
  for (let i = 0; i < NS; i += 8) if ((SP[i].x - x) ** 2 + (SP[i].z - z) ** 2 < 30) { ok = false; break; }
  if (x > 13 && x < 31 && Math.abs(z) < 27) ok = false;
  if (ok) TREES.push({ x, z, s: .8 + hash(k * 11) * .7 });
}
const treeTop = new THREE.InstancedMesh(new THREE.ConeGeometry(.9, 2.2, 7).translate(0, 2.0, 0), mat(0x7FA36B, { roughness: .9 }), TREES.length);
const treeTop2 = new THREE.InstancedMesh(new THREE.ConeGeometry(.7, 1.6, 7).translate(0, 2.9, 0), mat(0x8DB178, { roughness: .9 }), TREES.length);
const trunk = new THREE.InstancedMesh(new THREE.CylinderGeometry(.12, .16, 1.0).translate(0, .5, 0), mat(0x9a7a5a), TREES.length);
TREES.forEach((tr, i) => { M4.compose(V.set(tr.x, 0, tr.z), Q.identity(), S.setScalar(tr.s)); treeTop.setMatrixAt(i, M4); treeTop2.setMatrixAt(i, M4); trunk.setMatrixAt(i, M4); });
for (const m_ of [treeTop, treeTop2, trunk]) { m_.castShadow = true; m_.receiveShadow = true; scene.add(m_); }
{
  const tyres = [];
  for (let i = 0; i < NS; i += 5) if (Math.abs(KS[i]) > .06) {
    const s = KS[i] > 0 ? -1 : 1;                                   // the outside of the corner
    trackAt(i / NS * TL, s * (HW + (i / NS * TL > D_SE - 2 && i / NS * TL < D_SE + 26 ? 6.4 : 2.3)), TA);
    for (let h = 0; h < 2; h++) tyres.push([TA.x, .1 + h * .17, TA.z]);
  }
  const tw = new THREE.InstancedMesh(new THREE.TorusGeometry(.2, .09, 6, 12).rotateX(Math.PI / 2), mat(0x2b2724, { roughness: .8 }), tyres.length);
  tyres.forEach(([x, y, z], i) => { M4.compose(V.set(x, y, z), Q.identity(), S.setScalar(1)); tw.setMatrixAt(i, M4); tw.setColorAt(i, tmpC.set(i % 4 < 2 ? 0x2b2724 : (Math.floor(i / 4) % 2 ? RED : CREAM))); });
  tw.castShadow = true; scene.add(tw);
}

// ---------------------------------------------------------------- the AI: orb and rings above the infield
const ORB = new THREE.Vector3(-2, 15, 2);
const orb = new THREE.Group(); orb.position.copy(ORB); scene.add(orb);
const orbCoreM = new THREE.MeshStandardMaterial({ color: CORAL, emissive: CORAL, emissiveIntensity: 1.1, roughness: .35 });
orb.add(new THREE.Mesh(new THREE.SphereGeometry(1.1, 40, 28), orbCoreM));
orb.add(new THREE.Mesh(new THREE.SphereGeometry(1.35, 40, 28), new THREE.MeshStandardMaterial({ color: CREAM, transparent: true, opacity: .25, roughness: .2 })));
const ring1 = new THREE.Mesh(new THREE.TorusGeometry(2.0, .08, 8, 64), mat(INK, { roughness: .5 }));
const ring2 = new THREE.Mesh(new THREE.TorusGeometry(2.5, .06, 8, 64), mat(CORAL, { emissive: CORAL, emissiveIntensity: .5 }));
orb.add(ring1, ring2);
// the radio link: a line from the orb to car #7 and pulses running along it
const beamPos = new Float32Array(6);
const beamG = new THREE.BufferGeometry(); beamG.setAttribute("position", new THREE.BufferAttribute(beamPos, 3));
const beamM = new THREE.LineBasicMaterial({ color: CORAL, transparent: true, opacity: 0, toneMapped: false });
scene.add(new THREE.LineSegments(beamG, beamM));
const pulseM = new THREE.InstancedMesh(new THREE.SphereGeometry(.16, 10, 8), new THREE.MeshBasicMaterial({ color: CORAL, toneMapped: false }), 10);
scene.add(pulseM);

// ---------------------------------------------------------------- cars
// car ids: 0 = #7 (the driver), 1 = #11 (his teammate), 2..19 the field, two cars per team. Each car is built from
// ~40 instanced parts: floor, tapered tub, nose, sidepods with inlets, engine cover and shark fin, airbox, a three-
// element front wing, rear wing with DRS flap and beam wing, diffuser, mirrors, wishbones, rounded tyres on spoked rims,
// the halo, the driver (shoulders, HANS collar, arms, gloves on a steering wheel) and his open-face helmet and face.
// Paint is clear-coated and reflects a studio environment.
const NC = 20, HERO = 0, MATE = 1;
const TEAM = [CORAL, CORAL, NAVY, NAVY, 0x3FA372, 0x3FA372, 0xF08A3C, 0xF08A3C, 0x2A2623, 0x2A2623, 0xF4EFE6, 0xF4EFE6, 0x2E9AA6, 0x2E9AA6, 0x7E5BB0, 0x7E5BB0, 0xE36FA6, 0xE36FA6, 0xA9B1BA, 0xA9B1BA];
const ACC = TEAM.map((c, i) => (i === HERO ? CREAM : i === MATE ? GOLD : c === 0xF4EFE6 || c === 0xA9B1BA ? INK : i % 2 ? CREAM : INK));
const HELM = TEAM.map((c, i) => (i === HERO ? CREAM : i === MATE ? GOLD : [0xF4EFE6, GOLD, 0xD9483B, 0x3FA372, NAVY, 0xF08A3C][Math.floor(hash(i * 5) * 6)]));
const HTOP = TEAM.map((c, i) => (i === HERO ? CORAL : i === MATE ? INK : c));
const SKIN = [0xF1C9A5, 0xE3B28E, 0xC68863, 0xA06D4B, 0x7A4E34, 0xF6D7BF];
const SKINC = TEAM.map((c, i) => (i === HERO ? 0xE3B28E : i === MATE ? 0xA06D4B : SKIN[Math.floor(hash(i * 13) * 6)]));
const BROWC = TEAM.map((c, i) => (i === HERO ? 0x4A3222 : i === MATE ? 0x1E1B18 : [0x1E1B18, 0x4A3222, 0x7A5230, 0xB8572E][Math.floor(hash(i * 17) * 4)]));
const NUM = [7, 11, 1, 4, 16, 55, 44, 63, 14, 18, 10, 31, 22, 3, 23, 2, 77, 24, 20, 27];
const IM = (geo, m, n = NC, cast = true) => { const x = new THREE.InstancedMesh(geo, m, n); x.castShadow = cast; x.receiveShadow = true; scene.add(x); return x; };
const taper = (g, f, fy = .5) => { const p = g.attributes.position; for (let i = 0; i < p.count; i++) { const z = p.getZ(i), k = f(z); p.setX(i, p.getX(i) * k); p.setY(i, p.getY(i) * (1 - fy + fy * k)); } if (!g.index) return g; g.computeVertexNormals(); return g; };
const paint = () => new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .36, metalness: .04, clearcoat: .8, clearcoatRoughness: .12, envMap: ENV, envMapIntensity: .32 });
const carbon = () => new THREE.MeshStandardMaterial({ color: 0x24211f, roughness: .42, metalness: .35, envMap: ENV, envMapIntensity: .55 });
const metalM = (c) => new THREE.MeshStandardMaterial({ color: c, roughness: .28, metalness: .85, envMap: ENV, envMapIntensity: 1 });
const floorM = IM(new RoundedBoxGeometry(.88, .035, 1.95, 1, .015), carbon());
const tubM = IM(taper(new RoundedBoxGeometry(.42, .22, 1.3, 2, .08), (z) => lerp(1, .68, clamp((z + .2) / .85))), paint());
const noseM = IM(taper(new THREE.BoxGeometry(.24, .13, .82, 2, 2, 6), (z) => lerp(1, .38, (z + .41) / .82)), paint());
const podM = IM(taper(new RoundedBoxGeometry(.88, .21, .78, 3, .09), (z) => lerp(.66, 1, clamp((z + .39) / .6)), .35), paint());
const inletM = IM(new RoundedBoxGeometry(.12, .12, .05, 1, .03), new THREE.MeshBasicMaterial({ color: 0x14110f }), NC * 2, false);
const coverM = IM(taper(new RoundedBoxGeometry(.3, .27, .95, 3, .11), (z) => lerp(.38, 1, clamp((z + .47) / .8)), .65), paint());
const airboxM = IM(new RoundedBoxGeometry(.13, .1, .06, 1, .03), new THREE.MeshBasicMaterial({ color: 0x14110f }), NC, false);
const finM = IM(taper(new THREE.BoxGeometry(.018, .2, .6, 1, 1, 3), (z) => lerp(.6, 1, (z + .3) / .6), 1), paint());
const lineTopM = IM(new THREE.BoxGeometry(.07, .012, .95), paint());
const lineSideM = IM(new THREE.BoxGeometry(.012, .035, .62), paint(), NC * 2);
const cockpitM = IM(new THREE.TorusGeometry(.15, .024, 6, 24).rotateX(Math.PI / 2).scale(1, 1, 1.45), carbon());
const fwM = IM(new RoundedBoxGeometry(1.08, .024, .25, 1, .01), carbon());
const fwfM = IM(new RoundedBoxGeometry(1.0, .02, .12, 1, .008), paint(), NC * 2);
const plateM = IM(new RoundedBoxGeometry(.024, .3, .3, 1, .01), paint(), NC * 4);
const rwM = IM(new RoundedBoxGeometry(.82, .05, .2, 1, .02), paint());
const drsM = IM(new RoundedBoxGeometry(.8, .028, .13, 1, .01), paint());
const pylonM = IM(new THREE.BoxGeometry(.035, .3, .07), carbon());
const beamWM = IM(new THREE.BoxGeometry(.62, .03, .1), carbon());
const diffM = IM(new THREE.BoxGeometry(.74, .09, .24, 4, 1, 1), carbon());
const mirrorM = IM(new RoundedBoxGeometry(.11, .055, .035, 1, .015), paint(), NC * 2);
const stalkM = IM(new THREE.BoxGeometry(.02, .02, .1), carbon(), NC * 2);
const susM = IM(new THREE.CylinderGeometry(.009, .009, 1, 5), carbon(), NC * 8);
const TP = [[.112, -.098], [.15, -.1], [.172, -.094], [.183, -.075], [.187, -.04], [.187, .04], [.183, .075], [.172, .094], [.15, .1], [.112, .098]].map(([x, y]) => new THREE.Vector2(x, y));
const wheelM = IM(new THREE.LatheGeometry(TP, 32).rotateZ(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x262321, roughness: .72, side: THREE.DoubleSide }), NC * 4);
const stripeM = IM(new THREE.TorusGeometry(.136, .014, 6, 32).rotateY(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), NC * 4, false);
const rimM = IM(new THREE.CylinderGeometry(.112, .112, .185, 18).rotateZ(Math.PI / 2), metalM(0x4a4642), NC * 4, false);
const spokeM = IM(new THREE.BoxGeometry(.192, .2, .022), metalM(0x8c8780), NC * 8, false);
const capWM = IM(new THREE.CylinderGeometry(.034, .034, .2, 10).rotateZ(Math.PI / 2), paint(), NC * 4, false);
const haloM = IM(new THREE.TorusGeometry(.2, .015, 6, 28, Math.PI * 1.25).rotateX(Math.PI / 2).rotateY(Math.PI * .125), carbon());
const haloPM = IM(new THREE.BoxGeometry(.022, .24, .022), carbon());
const lightM = IM(new THREE.BoxGeometry(.09, .055, .02), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), NC, false);
// the driver in the cockpit
const suitM = IM(new RoundedBoxGeometry(.3, .13, .2, 2, .06), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .85 }));
const hansM = IM(new THREE.TorusGeometry(.085, .026, 6, 16, Math.PI * 1.3).rotateX(Math.PI / 2).rotateY(-Math.PI * .85), carbon());
const swM = IM(new RoundedBoxGeometry(.2, .085, .03, 1, .02), carbon());
const swDispM = IM(new THREE.BoxGeometry(.07, .035, .005), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }));
const armDM = IM(new THREE.CapsuleGeometry(.03, .16, 3, 8), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .85 }), NC * 2);
const gloveM = IM(new THREE.SphereGeometry(.036, 10, 8), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .7 }), NC * 2);
// the open-face helmet: shell with a face opening, top cap, chin bar, visor (up), foam rim, stripe, rear spoiler
const HR = .125;
const dbl = (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .3, clearcoat: .8, clearcoatRoughness: .1, side: THREE.DoubleSide, envMap: ENV, envMapIntensity: .35 });
const shellM = IM(new THREE.SphereGeometry(HR, 30, 18, Math.PI / 2 + .78, Math.PI * 2 - 1.56, .9, 1.3), dbl(0xffffff));
const capM = IM(new THREE.SphereGeometry(HR * 1.01, 30, 8, 0, Math.PI * 2, 0, .95), dbl(0xffffff));
const chinM = IM(new THREE.SphereGeometry(HR, 30, 8, 0, Math.PI * 2, 2.15, Math.PI - 2.15), dbl(0xffffff));
const visorM = IM(new THREE.SphereGeometry(HR * 1.045, 22, 6, Math.PI / 2 - .86, 1.72, .6, .32), new THREE.MeshPhysicalMaterial({ color: 0x3a3f6a, roughness: .05, metalness: .6, iridescence: 1, iridescenceIOR: 1.6, side: THREE.DoubleSide, envMap: ENV, envMapIntensity: 1.4 }));
const foamM = IM(new THREE.TorusGeometry(.088, .0065, 6, 28).scale(1.12, 1.08, 1), new THREE.MeshStandardMaterial({ color: 0x4a4440, roughness: 1 }), NC, false);
const hStripeM = IM(new THREE.TorusGeometry(HR * 1.012, .011, 6, 32, Math.PI * 2 - 1.75).rotateX(Math.PI / 2).rotateY(-(Math.PI / 2 + .875)), dbl(0xffffff), NC, false);
const spoilerM = IM(new RoundedBoxGeometry(.11, .02, .055, 1, .008), dbl(0xffffff), NC, false);
// the face: skin, eye whites, pupils, highlights, lids (they blink), brows, nose, cheeks, mouth (arc / o / gritted teeth), sweat
const faceM = IM(new THREE.SphereGeometry(.1, 26, 20), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6 }), NC, false);
const basic = (c) => new THREE.MeshBasicMaterial({ color: c });
const whiteM = IM(new THREE.SphereGeometry(.019, 14, 12), new THREE.MeshStandardMaterial({ color: 0xFFFDF8, roughness: .35, emissive: 0x2a2826 }), NC * 2, false);
const pupilM = IM(new THREE.SphereGeometry(.0105, 12, 10), basic(0x1E1B18), NC * 2, false);
const eyeHiM = IM(new THREE.SphereGeometry(.0038, 8, 6), basic(0xD8D2C8), NC * 2, false);
const lidM = IM(new THREE.SphereGeometry(.0205, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6 }), NC * 2, false);
const browM = IM(new RoundedBoxGeometry(.05, .014, .012, 1, .005), basic(0xffffff), NC * 2, false);
const noseFM = IM(new THREE.SphereGeometry(.013, 10, 8), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6 }), NC, false);
const cheekM = IM(new THREE.SphereGeometry(.014, 10, 8), new THREE.MeshBasicMaterial({ color: 0xE88C78, transparent: true, opacity: .45 }), NC * 2, false);
const mouthArcM = IM(new THREE.TorusGeometry(.026, .0075, 6, 16, Math.PI), basic(0x6a2a20), NC, false);
const mouthOM = IM(new THREE.TorusGeometry(.017, .0085, 8, 16), basic(0x6a2a20), NC, false);
const mouthInM = IM(new THREE.CircleGeometry(.016, 16), basic(0x3a1612), NC, false);
const teethM = IM(new RoundedBoxGeometry(.05, .018, .008, 1, .004), new THREE.MeshStandardMaterial({ color: 0xFFFDF8, roughness: .4, emissive: 0x2a2826 }), NC, false);
const lipLineM = IM(new THREE.BoxGeometry(.052, .003, .009), basic(0x6a2a20), NC, false);
const sweatM = IM(new THREE.SphereGeometry(.008, 10, 8).scale(1, 1.4, 1), new THREE.MeshStandardMaterial({ color: 0xBFE3F2, roughness: .05, metalness: .1, envMap: ENV }), NC, false);
const CARPARTS = [floorM, tubM, noseM, podM, inletM, coverM, airboxM, finM, lineTopM, lineSideM, cockpitM, fwM, fwfM, plateM, rwM, drsM, pylonM, beamWM, diffM, mirrorM, stalkM, susM,
  wheelM, stripeM, rimM, spokeM, capWM, haloM, haloPM, lightM, suitM, hansM, swM, swDispM, armDM, gloveM, shellM, capM, chinM, visorM, foamM, hStripeM, spoilerM,
  faceM, whiteM, pupilM, eyeHiM, lidM, browM, noseFM, cheekM, mouthArcM, mouthOM, mouthInM, teethM, lipLineM, sweatM];
// race numbers: decals on the nose and on both sides of the shark fin (their own small textures, so plain meshes)
const numTex = (n, fg, bg) => { const c = document.createElement("canvas"); c.width = 128; c.height = 128; const g = c.getContext("2d");
  g.fillStyle = bg; g.beginPath(); g.arc(64, 64, 60, 0, Math.PI * 2); g.fill();
  g.fillStyle = fg; g.font = "800 78px Manrope, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(String(n), 64, 70);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
const hex = (c) => "#" + col(c).getHexString();
const DECALS = [];
const decalGeo = new THREE.PlaneGeometry(.16, .16);
for (let id = 0; id < NC; id++) {
  const m = new THREE.MeshBasicMaterial({ map: numTex(NUM[id], hex(TEAM[id] === 0x2A2623 ? CREAM : INK), hex(ACC[id] === INK ? CREAM : ACC[id])), transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 });
  const ds = [0, 1, 2].map(() => { const d = new THREE.Mesh(decalGeo, m); d.matrixAutoUpdate = false; scene.add(d); return d; });
  DECALS.push(ds);
}
// #11's second arm for the title celebration comes from the same instanced arms (both hands leave the wheel)
// floating markers over #7 (coral) and #11 (gold), so they can be followed from far away
function marker(c) {
  const g = new THREE.Group();
  const cone = new THREE.Mesh(new THREE.ConeGeometry(.4, .8, 4).rotateX(Math.PI), new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: .5, roughness: .4 }));
  const ringm = new THREE.Mesh(new THREE.TorusGeometry(.6, .08, 6, 32).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: c, toneMapped: false }));
  ringm.position.y = -1.3;
  g.add(cone, ringm); scene.add(g); return g;
}
const MK = [marker(CORAL), marker(GOLD)];
// pit crew round #7's box: articulated figures (torso, legs, arms, helmet with visor), wheel guns, two jacks, the lollipop
const NCREW = 9;
const crewTorsoM = IM(new THREE.CapsuleGeometry(.11, .22, 4, 10), new THREE.MeshStandardMaterial({ color: CORAL, roughness: .8 }), NCREW);
const crewLegM = IM(new THREE.CapsuleGeometry(.055, .3, 3, 8), new THREE.MeshStandardMaterial({ color: 0x2A2623, roughness: .8 }), NCREW * 2);
const crewArmM = IM(new THREE.CapsuleGeometry(.042, .22, 3, 8), new THREE.MeshStandardMaterial({ color: CORAL, roughness: .8 }), NCREW * 2);
const crewHeadM = IM(new THREE.SphereGeometry(.105, 16, 12), dbl(CREAM), NCREW);
const crewVisorM = IM(new THREE.SphereGeometry(.108, 16, 6, Math.PI / 2 - .9, 1.8, 1.2, .5), new THREE.MeshStandardMaterial({ color: 0x23262e, roughness: .1, metalness: .5 }), NCREW, false);
const gunM = IM(new THREE.CylinderGeometry(.035, .045, .22, 10).rotateX(Math.PI / 2), metalM(0x8c8780), NCREW);
const jackM = IM(new THREE.CylinderGeometry(.02, .02, 1, 6), metalM(0xF2B33D), NCREW);
const lolliM = IM(new THREE.CylinderGeometry(.13, .13, .02, 20).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xffffff }), 1, false);
const CREWP = [[.98, .82], [-.98, .82], [.98, -.62], [-.98, -.62], [0, 2.0], [0, -1.6], [1.45, .1], [-1.45, .1], [0, 2.7]];
const CREWPARTS = [crewTorsoM, crewLegM, crewArmM, crewHeadM, crewVisorM, gunM, jackM, lolliM];

// effects: rain, spray, sound rings, prediction dots, smoke, debris, fireworks, ghost simulations
const RAIN_N = 1600;
const rainM = new THREE.InstancedMesh(new THREE.BoxGeometry(.014, .5, .014), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .55, toneMapped: false }), RAIN_N);
scene.add(rainM);
const SPRAY_K = 9;
const sprayM = new THREE.InstancedMesh(new THREE.SphereGeometry(.3, 10, 8), new THREE.MeshBasicMaterial({ color: 0xF4F2EE, transparent: true, opacity: .24, depthWrite: false }), NC * SPRAY_K);
scene.add(sprayM);
const RINGS = Array.from({ length: 6 }, () => { const m = new THREE.Mesh(new THREE.TorusGeometry(1, .05, 6, 48).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: CORAL, transparent: true, opacity: 0, toneMapped: false, depthWrite: false })); scene.add(m); return m; });
const PRED_N = 2 * 26;
const predM = new THREE.InstancedMesh(new THREE.SphereGeometry(.13, 10, 8), new THREE.MeshBasicMaterial({ color: RED, toneMapped: false }), PRED_N);
scene.add(predM);
const predRing = new THREE.Mesh(new THREE.RingGeometry(1.0, 1.25, 48).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: RED, transparent: true, opacity: 0, toneMapped: false, depthWrite: false }));
scene.add(predRing);
const attRing = new THREE.Mesh(new THREE.RingGeometry(1.4, 1.7, 48).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: CORAL, transparent: true, opacity: 0, toneMapped: false, depthWrite: false }));
scene.add(attRing);
const CHEV_N = 7;
const chevM = new THREE.InstancedMesh(new THREE.ConeGeometry(.45, .6, 3).rotateX(Math.PI / 2).scale(1, .15, 1), new THREE.MeshBasicMaterial({ color: CORAL, toneMapped: false }), CHEV_N);
scene.add(chevM);
const SMOKE_N = 70;
const smokeM = new THREE.InstancedMesh(new THREE.SphereGeometry(.4, 10, 8), new THREE.MeshStandardMaterial({ color: 0xDCD6CE, transparent: true, opacity: .38, depthWrite: false, roughness: 1 }), SMOKE_N);
scene.add(smokeM);
const DEB_N = 34;
const debM = new THREE.InstancedMesh(new THREE.BoxGeometry(.12, .04, .2), mat(0xffffff, { roughness: .5 }), DEB_N);
debM.castShadow = true; scene.add(debM);
const FW_N = 6 * 70;
const fwkM = new THREE.InstancedMesh(new THREE.SphereGeometry(.09, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), FW_N);
scene.add(fwkM);
const SPK_K = 5;
const sparkM = new THREE.InstancedMesh(new THREE.BoxGeometry(.014, .014, .2), new THREE.MeshBasicMaterial({ color: 0xFFC26A, toneMapped: false }), NC * SPK_K);
scene.add(sparkM);
const GH_N = 900;
const ghostM = new THREE.InstancedMesh(new THREE.CapsuleGeometry(.1, .5, 3, 6).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .75, toneMapped: false, depthWrite: false }), GH_N);
scene.add(ghostM);
const GHC = [CORAL, GOLD, NAVY, 0x3FA372, 0x2E9AA6, CREAM];
for (let k = 0; k < GH_N; k++) ghostM.setColorAt(k, tmpC.set(GHC[k % GHC.length]));

// ---------------------------------------------------------------- the race script
// real time t -> race time w (slow motion while #7 drives through the crash)
const SLOW = C.slowmo;
const FR = 120, NT = Math.ceil((DUR + 2) * FR);
const SCN = [0, C.cuts[0], C.cuts[1], C.cuts[2], C.cuts[3], C.cuts[4], 1e9];   // A hook, B rain, C listen, D crash, E final + title, G real + close
const sceneOf = (t) => { let s = 0; while (t >= SCN[s + 1]) s++; return s; };
const RAIN0 = C.rain - .1;
function vbase(t) {
  const s = sceneOf(t);
  if (s === 1) return lerp(30, 18, ss(t, RAIN0, RAIN0 + 1.2));
  if (s === 4) return lerp(30, 11, ss(t, C.finish + .3, C.finish + 2.8));
  return 30;
}
const WA = new Float64Array(NT + 1), DA = new Float64Array(NT + 1);
for (let i = 1; i <= NT; i++) {
  const t = (i - .5) / FR;
  let k = 1; for (const [a, b, f] of C.slowwin) if (t > a && t < b) k = Math.min(k, lerp(1, f, ss(t, a, a + .15) * (1 - ss(t, b - .15, b))));
  WA[i] = WA[i - 1] + k / FR;
  DA[i] = DA[i - 1] + k * vbase(t) / FR;
}
const sample = (A, t) => { const f = clamp(t, -1, DUR + 1.9) * FR; if (f < 0) return A[0] + f / FR * 30; const i = Math.floor(f); return lerp(A[i], A[Math.min(NT, i + 1)], f - i); };
const Wt = (t) => sample(WA, t), Dt = (t) => sample(DA, t);
const GP = (p) => 4 + 5.2 * p;
const ORD_A = [2, 4, 1, 6, 0, 8, 3, 10, 12, 5, 14, 7, 16, 9, 18, 11, 13, 15, 17, 19];
const ORD_B = ORD_A.filter((i) => i !== HERO);
const ORD_C = [2, 4, 6, 8, 3, 10, 12, 0, 1, 5, 14, 7, 16, 9, 18, 11, 13, 15, 17, 19];
const ORD_D = [2, 4, 0, 1, 6, 8, 3, 10, 12, 5, 14, 7, 16, 9, 18, 11, 13, 15, 17, 19];
const posIn = (ord, id) => ord.indexOf(id);
// scene B: #7 starts far behind and passes the last six cars at the cue times
const PB = C.pb;
const gB = pchip([[C.cuts[0], GP(18) + 30], [RAIN0 + .2, GP(18) + 32], ...PB.map((t, j) => [t, GP(18 - j)]), [PB[5] + .6, GP(13) - 6.9]]);
// scene C: #7 closes on car 12 and passes it at the hairpin
const XC = 12, ATT = C.att;
const gC = pchip([[C.cuts[1], GP(6) + 4.6], [ATT - .7, GP(6) + 1.3], [ATT, GP(6)], [ATT + .8, GP(6) - 3.6]]);
// scene D: the two leaders (2, 4) collide at TC; #7 lifts one second early
const TC = C.tc, A_ = 2, B_ = 4;
const gDB = pchip([[C.cuts[2], 9.2], [TC - 1.6, 8.6], [TC, 4.6]]);
const gDH = pchip([[C.cuts[2], 14.4], [C.slows, 14.4], [C.slows + 1.7, 46], [C.slows + 4, 46.2]]);
// scene E: #7 leads, #11 behind; #7 lets him through before the line
const FIN = C.finish;
const gEH = pchip([[C.cuts[3], 4], [C.let - .2, 4], [C.let + .9, 9.6], [FIN + .6, 15], [C.cuts[4], 17]]);
const gET = pchip([[C.cuts[3], 12], [C.leading + 1.6, 9.0], [C.let - .2, 7.6], [C.cuts[4], 7.6]]);
// distance offsets per scene so that each beat lands where it should on the circuit
const OFF = [
  D_PIN + GP(4) - Dt(2.9),
  nearestD(20, 0) + gB(14.0) - Dt(14.0),
  D_ATT + GP(6) - Dt(ATT),
  D_CRASH + GP(0) - Dt(TC),
  D_SF + gET(FIN) + TL * 3 - Dt(FIN),
  0,
];
// #7's pit stop in the hook: into the pit lane at 2.9 s, stopped 4.3-6.1 s, back out
const herm = (u, m0, S_, m1) => (u ** 3 - 2 * u * u + u) * m0 + (-2 * u ** 3 + 3 * u * u) * S_ + (u ** 3 - u * u) * m1;
function pitD(t) {
  if (t < 4.3) return D_PIN + herm(ramp(t, 2.9, 4.3), 42, 20, 0);
  if (t < 6.1) return D_BOX;
  if (t < 7.6) return D_BOX + herm(ramp(t, 6.1, 7.6), 0, 22, 45);
  return D_BOX + 22 + 30 * (t - 7.6);
}
const CS = { d: 0, lane: 0, spin: 0, wob: 0 };
// the state of car id at time t, computed with the rules of scene s (default: the scene t falls in)
function carState(id, t, s = sceneOf(t), out = CS) {
  const D = Dt(t) + OFF[s], w = Wt(t);
  let g = 0, lane = 0, spin = 0, wob = Math.sin(w * .8 + id * 2.1) * .45;
  if (s === 0) {
    g = GP(posIn(ORD_A, id)) + wob;
    lane = Math.sin(w * .9 + id) * .35;
    if (id === HERO && t > 2.9) { out.d = pitD(t); out.lane = pitLane(wrap(out.d)); out.spin = 0; out.wob = 0; return out; }
    if (id === HERO) lane = pitLane(wrap(D - g)) + lane * (1 - ss(t, 2.2, 2.9));
  } else if (s === 1) {
    if (id === HERO) { g = gB(t); lane = 0; for (const tp of PB) lane += .95 * bump(t, tp - .45, tp + .35, .2); }
    else { const p = posIn(ORD_B, id); g = GP(p) + wob; lane = Math.sin(w * .9 + id) * .3; const j = 18 - p; if (j >= 0 && j < 6) lane -= .5 * bump(t, PB[j] - .45, PB[j] + .35, .2); }
    const r = ss(t, RAIN0, RAIN0 + 1.2);
    if (id !== HERO) { lane += r * Math.sin(w * 3.1 + id * 1.7) * .22; spin = r * Math.sin(w * 4.3 + id * 2.3) * .1; }
  } else if (s === 2) {
    if (id === HERO) g = gC(t); else g = GP(posIn(ORD_C, id)) + wob;
    lane = Math.sin(w * .9 + id) * .3;
    trackAt(D - GP(6), 0, TA);
    const inside = TA.k > 0 ? 1 : -1;
    if (id === HERO) lane = inside * 1.0 * bump(t, ATT - 1.0, ATT + .6, .3);
    if (id === XC) lane = -inside * .45 * bump(t, ATT - 1.0, ATT + .6, .3);
  } else if (s === 3) {
    const p = posIn(ORD_D, id);
    if (id === A_) g = GP(0);
    else if (id === B_) g = gDB(t);
    else if (id === HERO) g = gDH(t);
    else if (id === MATE) g = gDH(t) + 6;
    else g = 62 + 5.2 * (p - 4) + wob;
    lane = id === HERO || id === MATE ? 0 : Math.sin(w * .9 + id) * .3;
    if (id === A_ || id === B_) {
      trackAt(D_CRASH, 0, TA);
      const inside = TA.k > 0 ? 1 : -1;
      lane = id === B_ ? inside * .95 * ss(t, TC - 1.4, TC - .2) : -inside * .25 * ss(t, TC - 1.4, TC - .2);
      if (t > TC) {
        const u = w - Wt(TC), dc = Dt(TC) + OFF[3] - g;
        const k = id === A_ ? 2.2 : 2.7;
        out.d = dc + 30 * (1 - Math.exp(-k * u)) / k;
        out.lane = lane + (id === A_ ? -inside * 4.1 : inside * 3.6) * ss(u, 0, 1.3);
        out.spin = (id === A_ ? 1 : -1) * Math.PI * 2 * (id === A_ ? 1.3 : 1.0) * (1 - Math.exp(-2.1 * u));
        out.wob = 0; return out;
      }
    }
  } else if (s === 4) {
    if (id === HERO) g = gEH(t);
    else if (id === MATE) g = gET(t);
    else g = 80 + GP(posIn(ORD_A, id)) + wob;
    lane = Math.sin(w * .9 + id) * .3;
    if (id === HERO) lane = 1.05 * ss(t, C.let - .25, C.let + .25) * (1 - ss(t, FIN + 1.5, FIN + 3)) + .25 * Math.sin(w * .7);
    if (id === MATE) lane = -.45 * bump(t, C.let - .2, FIN + .6) + .85 * Math.sin(w * 3.2) * ss(t, C.wins - 1.0, C.wins);
  } else {
    g = GP(posIn(ORD_A, id)) + wob;
    lane = Math.sin(w * .9 + id) * .4;
  }
  out.d = D - g; out.lane = lane; out.spin = spin; out.wob = wob;
  return out;
}
const PO = { x: 0, z: 0, tx: 0, tz: 0, k: 0 };
function carXZ(id, t, s, out) { carState(id, t, s); trackAt(CS.d, CS.lane, out); out.d = CS.d; out.spin = CS.spin; out.lane = CS.lane; return out; }
// pose of every car at the current frame
const POSE = Array.from({ length: NC }, () => ({ x: 0, z: 0, yaw: 0, d: 0, spd: 0, brake: 0, k: 0, steer: 0 }));
const P1 = { x: 0, z: 0, tx: 0, tz: 0, k: 0 }, P2 = { x: 0, z: 0, tx: 0, tz: 0, k: 0 };
function poseAt(id, t, s, out) {
  carXZ(id, t, s, P1); const d1 = P1.d, sp = P1.spin;
  carXZ(id, t - .06, s, P2);
  const dx = P1.x - P2.x, dz = P1.z - P2.z, l = Math.hypot(dx, dz);
  let yaw = l > .03 ? Math.atan2(dx, dz) : Math.atan2(P1.tx, P1.tz);
  if (l > .03) { const ty = Math.atan2(P1.tx, P1.tz); let dy = yaw - ty; dy = Math.atan2(Math.sin(dy), Math.cos(dy)); yaw = ty + clamp(dy, -.5, .5); }
  const spd = l / .06;
  carXZ(id, t - .16, s, P2); const spd0 = Math.hypot(P2.x - (P1.x - dx), P2.z - (P1.z - dz)) / .1;
  out.x = P1.x; out.z = P1.z; out.yaw = yaw + sp; out.d = d1; out.spd = spd; out.brake = spd0 - spd > 1.2 ? 1 : 0; out.k = P1.k;
  out.steer = clamp(P1.k * 2.2, -.45, .45);
  return out;
}

// the face for car id at time t: mouth (smile / frown / flat / o / grit), brows (left, right tilt: + angry), brow lift,
// eye size, lids (0 open .. 1 shut; they blink), where the eyes look (lx, ly), sweat, head nod / shake / tilt
const FOC = C.focus;
const blinkAt = (id, t) => { const p = 2.4 + hash(id * 3) * 1.8, u = (t + hash(id) * 7) % p; return u < .14 ? Math.sin(Math.PI * u / .14) : 0; };
function expression(id, t) {
  const ex = { mouth: "flat", bl: .25, br: .25, lift: 0, eyes: 1, lid: .3, lx: 0, ly: 0, sweat: 0, nod: 0, shake: 0, tilt: 0 };
  ex.lx = Math.sin(t * .9 + id) * .25 + (Math.sin(t * 2.3 + id * 3) > .9 ? .7 : 0);
  ex.ly = Math.sin(t * .7 + id * 2) * .15;
  const tense = bump(t, C.crash - .3, TC + 1.2, .3);
  if (tense > .5 && (id === HERO || id === MATE)) { ex.mouth = "grit"; ex.bl = ex.br = -.2; ex.eyes = 1.12; ex.lid = .12; ex.sweat = 1; ex.lx = 0; }
  if (id === HERO) {
    if (t > FOC[0].a - .3 && t < FOC[0].b + .2) { ex.mouth = "frown"; ex.bl = ex.br = .5; ex.lid = .42; ex.lx = Math.sin(t * 2) > 0 ? -.8 : .3; ex.shake = Math.sin(t * 9) * .2 * bump(t, 4.85, 5.75, .15); }
    if (t > FOC[1].a - .2 && t < FOC[1].b) { ex.mouth = "smile"; ex.bl = ex.br = -.05; ex.lid = .3; ex.lx = .1; }
    if (t > FOC[3].a - .2 && t < FOC[3].b + .3) { ex.mouth = "o"; ex.eyes = 1.3; ex.lid = 0; ex.lift = .014; ex.bl = ex.br = -.35; ex.sweat = 1; ex.lx = 0; ex.ly = .2; }
    if (t > FOC[4].a - .2 && t < C.obeys - .25) { ex.mouth = "frown"; ex.bl = -.45; ex.br = .35; ex.lift = .006; ex.tilt = .2; ex.eyes = 1.08; ex.lid = .18; ex.lx = .75; ex.shake = Math.sin(t * 3) * .08; }
    if (t >= C.obeys - .25 && t < FOC[4].b + .2) { ex.mouth = "flat"; ex.bl = ex.br = -.15; ex.lid = .58; ex.ly = -.8; ex.lx = 0; ex.nod = Math.max(0, Math.sin((t - C.obeys + .25) * 7)) * .32 * (1 - ramp(t, C.obeys + 1.1, C.obeys + 1.5)); }
  }
  if (id === MATE) {
    if (t > FOC[2].a - .2 && t < FOC[2].b) { ex.mouth = "grit"; ex.bl = ex.br = .45; ex.lid = .5; ex.ly = .25; ex.lx = -.2; }
    if (t > C.wins - .3) { ex.mouth = Math.sin(t * 5) > -.3 ? "o" : "smile"; ex.bl = ex.br = -.3; ex.lift = .012; ex.lid = .45; ex.ly = .3; ex.nod = Math.abs(Math.sin(t * 6)) * .12; }
  }
  ex.lid = Math.max(ex.lid, blinkAt(id, t));
  return ex;
}

// ---------------------------------------------------------------- camera shots
// each shot is a function of t returning a camera position, a look-at point and a fov; a shot blends in from the
// previous one over `tr` seconds (0 = a hard cut, hidden by a white flash in the grade)
const CAMP = new THREE.Vector3(), CAML = new THREE.Vector3();
const SH = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40 };
const fixed = (p, l, fov = 40) => () => { SH.p.set(...p); SH.l.set(...l); SH.fov = fov; return SH; };
const CX = { x: 0, z: 0, tx: 0, tz: 0, k: 0 }, CY = { x: 0, z: 0, tx: 0, tz: 0, k: 0 };
// chase: on the car's own line, `lag` s behind it, looking `lead` s ahead
const chase = (id, lag, up, side, lead, fov = 50) => (t) => {
  const s = sceneOf(t);
  carXZ(id, t - lag, s, CX); carXZ(id, t + lead, s, CY);
  const ang = Math.atan2(CY.x - CX.x, CY.z - CX.z);
  SH.p.set(CX.x + Math.cos(ang) * side, up, CX.z - Math.sin(ang) * side);
  SH.l.set(CY.x, .45, CY.z); SH.fov = fov; return SH;
};
// heli: a world offset from the car, looking at it
const heli = (id, off, lookUp = .3, fov = 40) => (t) => { const P = POSE[id]; SH.p.set(P.x + off[0], off[1], P.z + off[2]); SH.l.set(P.x, lookUp, P.z); SH.fov = fov; return SH; };
// rigid: an offset in the car's own frame (x right, y up, z forward), looking at a point in the car's frame
const rigid = (id, off, look, fov = 40) => (t) => {
  const P = POSE[id], c = Math.cos(P.yaw - (P.spinOnly || 0)), s_ = Math.sin(P.yaw - (P.spinOnly || 0));
  const tf = (o, out) => out.set(P.x + o[0] * c + o[2] * s_, o[1], P.z - o[0] * s_ + o[2] * c);
  tf(off, SH.p); tf(look, SH.l); SH.fov = fov; return SH;
};
const HELMET = [0, .52, -.02];
const face = (id, d, h, side, fov) => rigid(id, [side + HELMET[0], HELMET[1] + h, HELMET[2] + d], [HELMET[0], HELMET[1] - .085, HELMET[2]], fov);
const orbShot = (dx, dy, dz, fov = 34) => (t) => { SH.p.set(ORB.x + dx, ORB.y + dy, ORB.z + dz); SH.l.set(ORB.x, ORB.y - .6, ORB.z); SH.fov = fov; return SH; };
trackAt(D_ATT, 0, TA); const ATTP = [TA.x, TA.z];
trackAt(D_CRASH + 6, 0, TA); const CRP = [TA.x, TA.z];
trackAt(D_SF, 0, TA); const SFP = [TA.x, TA.z];
trackAt(D_CRASH - 16, -1.5, TA); const CRV = { x: TA.x, z: TA.z };
trackAt(D_CRASH + 13, 0, TA); const THRU = { x: TA.x, z: TA.z, tx: TA.tx, tz: TA.tz };
const focusShot = (k, d = 1.75, h = .07, side = .36, fov = 27) => face(FOC[k].id, d, h, side, fov);
// dolly zoom on a face: the lens widens while the camera moves in, so the face holds its size and the world stretches
const vertigo = (k, d0, f0, f1, h = .05, side = .3) => (t) => {
  const f = FOC[k], u = ss(t, f.a + .1, f.b), fov = lerp(f0, f1, u);
  return face(f.id, d0 * Math.tan(f0 * Math.PI / 360) / Math.tan(fov * Math.PI / 360), h, side, fov)(t);
};
// a slow push in on a face
const push = (k, d0, d1, fov = 27, h = .07, side = .36) => (t) => { const f = FOC[k]; return face(f.id, lerp(d0, d1, ss(t, f.a, f.b)), h, side, fov)(t); };
const SHOTS = [
  { t: 0, tr: 0, f: rigid(HERO, [.5, 1.25, -3.4], [0, .45, 3.5], 50) },
  { t: C.ai - .35, tr: .45, f: orbShot(5.5, 1.2, 7.5, 32) },
  { t: C.called - .1, tr: .55, f: heli(HERO, [-6.5, 7.5, -8], .3, 42) },
  { t: FOC[0].a, tr: .4, f: focusShot(0, 1.9, .14, .36, 21) },
  { t: FOC[0].b, tr: .45, f: fixed([10, 15, D_BOX > 0 ? 9 : 9], [21.5, 0, -2], 44) },
  { t: C.cuts[0], tr: 0, f: heli(10, [9, 9, 11], .3, 44) },
  { t: C.every - .2, tr: .5, f: rigid(5, [3.4, 1.1, 1.6], [0, .3, .2], 42) },
  { t: C.only - .25, tr: .45, f: rigid(HERO, [1.7, .5, 2.3], [.4, .2, .7], 36) },
  { t: C.six - .45, tr: .4, f: chase(HERO, .19, 1.7, .35, .3, 54) },
  { t: C.cuts[1], tr: 0, f: heli(HERO, [6, 9, 9], .3, 42) },
  { t: C.tyre - .35, tr: .45, f: rigid(HERO, [3.2, 2.2, -1.2], [0, .2, -.4], 40) },
  { t: C.exactly - .5, tr: .6, f: fixed([ATTP[0] + 9, 21, ATTP[1] - 6], [ATTP[0], 0, ATTP[1]], 42) },
  { t: C.cuts[2], tr: 0, f: chase(HERO, .2, 2.6, .5, .55, 52) },
  { t: C.crash - .2, tr: .55, f: (t) => { const u = ramp(t, C.crash - .2, C.slows - .2), a = -.35 + u * .7; SH.p.set(CRP[0] - 2 + Math.sin(a) * 25, 32 - u * 7, CRP[1] + 1 + Math.cos(a) * 25); SH.l.set(CRP[0] - 2, 0, CRP[1] + 1); SH.fov = 40; return SH; } },
  { t: C.slows - .2, tr: .5, f: chase(HERO, .3, 4.0, .3, 1.0, 50) },
  { t: TC - .45, tr: .4, f: fixed([CRV.x, 6.5, CRV.z], [CRP[0], .3, CRP[1] - 2], 44) },
  { t: SLOW[0] - .05, tr: .35, f: (t) => { const P = POSE[HERO]; SH.p.set(THRU.x + THRU.tx * 5 + THRU.tz * 1.2, 1.1, THRU.z + THRU.tz * 5 - THRU.tx * 1.2); SH.l.set(P.x, .5, P.z); SH.fov = 46; return SH; } },
  { t: C.cuts[3], tr: 0, f: heli(HERO, [-5, 3.6, -8], .4, 44) },
  { t: FOC[1].a, tr: .4, f: focusShot(1) },
  { t: FOC[2].a, tr: .4, f: focusShot(2, 1.75, .12, -.3, 27) },
  { t: FOC[2].b, tr: .45, f: rigid(HERO, [-2.8, 4.6, -12.5], [0, .3, -1.2], 44) },
  { t: C.says - .75, tr: .45, f: orbShot(-6, 1.5, 7, 32) },
  { t: FOC[3].a, tr: .3, f: vertigo(3, 2.1, 17, 42, .05, .3) },
  { t: FOC[3].b, tr: .3, f: fixed([SFP[0] + 1.2, 3.0, SFP[1] - 9], [SFP[0], 1.3, SFP[1] + 3], 46) },
  { t: FOC[4].a, tr: .35, f: push(4, 2.3, 1.45, 27, .07, .36) },
  { t: FOC[4].b, tr: .5, f: heli(MATE, [-13, 9, 13], 2.5, 44) },
  { t: FOC[5].a, tr: .4, f: focusShot(5, 1.55, .08, -.24, 28) },
  { t: C.cuts[4], tr: 0, f: (t) => { const u = ramp(t, C.cuts[4], C.e[6]); SH.p.set(2 + Math.sin(u * .6) * 6, 125 - u * 18, 34 - u * 6); SH.l.set(1, 0, -2); SH.fov = 40; return SH; } },
  { t: C.l[7] - .1, tr: 1.2, f: (t) => { const u = ramp(t, C.l[7], DUR); SH.p.set(-8 + u * 10, 70 + u * 22, 62 + u * 6); SH.l.set(0, 2, -4); SH.fov = 40; return SH; } },
];
const ease3 = (x) => (x < .5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);
const PREV = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40 };
function camAt(t) {
  let i = 0;
  while (i < SHOTS.length - 1 && t >= SHOTS[i + 1].t) i++;
  const cur = SHOTS[i];
  let r = cur.f(t);
  CAMP.copy(r.p); CAML.copy(r.l); let fov = r.fov;
  if (cur.tr > 0 && i > 0 && t < cur.t + cur.tr) {
    const pr = SHOTS[i - 1].f(t);
    PREV.p.copy(pr.p); PREV.l.copy(pr.l); PREV.fov = pr.fov;
    const u = ease3(ramp(t, cur.t, cur.t + cur.tr));
    const dist = PREV.p.distanceTo(CAMP);
    CAMP.lerpVectors(PREV.p, CAMP, u);
    CAMP.y += Math.sin(Math.PI * u) * Math.min(dist * .15, 6);
    CAML.lerpVectors(PREV.l, CAML, u);
    fov = lerp(PREV.fov, fov, u);
  }
  return fov;
}

// ---------------------------------------------------------------- render at time t
const MC = new THREE.Matrix4(), MHD = new THREE.Matrix4(), MP = new THREE.Matrix4(), MR = new THREE.Matrix4(), MOUT = new THREE.Matrix4(), EU = new THREE.Euler(), EUQ = new THREE.Euler();
const MBC = new THREE.Matrix4();
let BASEM = MC;
// a limb (or rod) from local point a to b: the mesh's long axis is y, `baseLen` its length at scale 1
const Q2 = new THREE.Quaternion(), S2 = new THREE.Vector3(), VA = new THREE.Vector3(), VB = new THREE.Vector3();
function seg(mesh, idx, a, b, baseLen) {
  VA.set(b[0] - a[0], b[1] - a[1], b[2] - a[2]); const len = Math.max(1e-4, VA.length()); VA.divideScalar(len);
  Q2.setFromUnitVectors(UP, VA);
  MP.compose(VB.set((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2), Q2, S2.set(1, len / baseLen, 1));
  MOUT.multiplyMatrices(BASEM, MP); mesh.setMatrixAt(idx, MOUT);
}
function part(mesh, idx, x, y, z, rx = 0, ry = 0, rz = 0, sx = 1, sy = 1, sz = 1) {
  MP.makeTranslation(x, y, z);
  if (rx || ry || rz) MP.multiply(MR.makeRotationFromEuler(EU.set(rx, ry, rz, "YXZ")));
  if (sx !== 1 || sy !== 1 || sz !== 1) MP.multiply(MR.makeScale(sx, sy, sz));
  MOUT.multiplyMatrices(BASEM, MP);
  if (mesh) mesh.setMatrixAt(idx, MOUT);
}
const CMP = { soft: RED, med: GOLD, wet: BLUE };
function compound(id, t) {
  if (id === HERO) {
    const s = sceneOf(t);
    if (s === 0) return t < 4.95 ? CMP.soft : CMP.wet;
    if (s === 1) return CMP.wet;
    return CMP.med;
  }
  return hash(id * 3.3) < .55 ? CMP.soft : CMP.med;
}
const posEl = document.getElementById("pos"), tyreEl = document.getElementById("tyre"), tyreDot = document.getElementById("tdot");
const WHEELS = [[.47, .187, .84, 1], [-.47, .187, .84, 1], [.47, .187, -.62, 1.22], [-.47, .187, -.62, 1.22]];
function renderAt(t) {
  const s = sceneOf(t), w = Wt(t);
  // weather and light: rain in scene B (wet track lingers), dusk for the title
  const rain = ss(t, RAIN0, RAIN0 + .8) * (1 - ss(t, C.cuts[1] - .3, C.cuts[1]));
  const wet = ss(t, RAIN0, RAIN0 + 1.5) * (1 - ss(t, C.cuts[1] + 2, C.cuts[1] + 6));
  const dusk = ss(t, FIN + .2, FIN + 1.6) * (1 - ss(t, C.cuts[4] - .2, C.cuts[4]));
  tmpC.set(0xF1E9DC).lerp(tmpC2.set(0xBFC2C4), rain * .9).lerp(tmpC2.set(0x6A5C8A), dusk * .85);
  scene.background.copy(tmpC); scene.fog.color.copy(tmpC);
  sun.intensity = lerp(2.1, .7, rain) * lerp(1, .8, dusk);
  sun.color.set(0xfff1dc).lerp(tmpC2.set(0xffb48a), dusk);
  hemi.intensity = lerp(.95, .8, rain) * lerp(1, 1.25, dusk);
  hemi.color.set(0xFFF6EA).lerp(tmpC2.set(0xdde3ea), rain).lerp(tmpC2.set(0xA9A6D8), dusk);
  hemi.groundColor.set(0xCDBFA8).lerp(tmpC2.set(0x4a4260), dusk);
  asphaltM.color.set(0x7E7872).lerp(tmpC2.set(0x56524f), wet);
  asphaltM.roughness = lerp(.85, .3, wet);
  bloom.strength = lerp(.22, .6, dusk); bloom.threshold = lerp(.92, .65, dusk);

  // the orb: brighter whenever it speaks on the radio
  const RADIO = C.radio;
  let talk = 0; for (const [a, b] of RADIO) talk = Math.max(talk, bump(t, a, b, .25));
  orbCoreM.emissiveIntensity = .9 + talk * 1.3 + dusk * .5 + Math.sin(t * 20) * .2 * talk;
  orb.scale.setScalar(1 + talk * .1);
  orb.position.set(ORB.x, ORB.y + Math.sin(t * 1.3) * .2, ORB.z);
  ring1.rotation.set(Math.PI / 2 + Math.sin(t * .7) * .4, t * .9, 0);
  ring2.rotation.set(Math.PI / 2.6, -t * 1.3 * (1 + talk), t * .4);

  // cars
  for (let id = 0; id < NC; id++) poseAt(id, t, s, POSE[id]);
  const liftHero = s === 0 ? .07 * ss(t, 4.38, 4.55) * (1 - ss(t, 5.85, 6.0)) : 0;
  const setc = (m, i, c) => m.setColorAt(i, tmpC.set(c));
  for (let id = 0; id < NC; id++) {
    const P = POSE[id], fast = clamp(P.spd / 30);
    // chassis: vibration at speed, nose dive under braking, roll in corners, on the jacks in the pit stop
    const vib = Math.sin(t * 61 + id * 3) * .004 * fast;
    const pitch = .035 * P.brake + .008 * Math.sin(t * 13 + id) * fast;
    const roll = clamp(P.k * P.spd * .0035, -.06, .06);
    MC.compose(V.set(P.x, vib + (id === HERO ? liftHero : 0), P.z), Q.setFromEuler(EUQ.set(pitch, P.yaw, roll, "YXZ")), S.set(1, 1, 1));
    BASEM = MC;
    const tc = TEAM[id], ac = ACC[id];
    const drs = Math.abs(P.k) < .006 && P.spd > 24 ? 1 : 0;
    part(floorM, id, 0, .052, -.05);
    part(tubM, id, 0, .21, .12); setc(tubM, id, tc);
    part(noseM, id, 0, .165, 1.15, .05); setc(noseM, id, id === HERO ? ac : tc);
    part(podM, id, 0, .2, -.16); setc(podM, id, tc);
    for (let k = 0; k < 2; k++) {
      const sx = k ? -1 : 1, i2 = id * 2 + k;
      part(inletM, i2, sx * .33, .23, .22);
      part(lineSideM, i2, sx * .446, .21, -.16); setc(lineSideM, i2, ac);
      part(mirrorM, i2, sx * .3, .38, .3); setc(mirrorM, i2, tc);
      part(stalkM, i2, sx * .245, .355, .3, 0, 0, sx * .35);
      part(fwfM, i2, 0, .082 + k * .03, 1.42 - k * .04, -.32 - k * .26, 0, 0, 1 - k * .07, 1, 1); setc(fwfM, i2, k ? tc : ac);
    }
    part(coverM, id, 0, .37, -.42); setc(coverM, id, tc);
    part(airboxM, id, 0, .53, -.12);
    part(finM, id, 0, .56, -.62); setc(finM, id, ac);
    part(lineTopM, id, 0, .326, .5); setc(lineTopM, id, ac);
    part(cockpitM, id, 0, .326, .0);
    part(fwM, id, 0, .055, 1.46);
    for (let k = 0; k < 4; k++) {
      const front = k < 2, sx = k % 2 ? -1 : 1;
      part(plateM, id * 4 + k, sx * (front ? .55 : .425), front ? .1 : .55, front ? 1.43 : -.88, 0, 0, 0, 1, front ? .42 : 1.05, front ? .88 : 1.05);
      setc(plateM, id * 4 + k, ac);
    }
    part(rwM, id, 0, .64, -.92); setc(rwM, id, ac);
    part(drsM, id, 0, .72 + .015 * drs, -.86, -.5 + .42 * drs); setc(drsM, id, tc);
    part(pylonM, id, 0, .47, -.92);
    part(beamWM, id, 0, .31, -1.0);
    part(diffM, id, 0, .1, -1.02, .38);
    for (let k = 0; k < 4; k++) {
      const [, wy, wz] = WHEELS[k], sx = Math.sign(WHEELS[k][0]);
      for (let j = 0; j < 2; j++) seg(susM, id * 8 + k * 2 + j, [sx * .18, .19 + j * .07, wz + (j ? .07 : -.07)], [sx * .37, wy + (j ? .05 : -.04), wz], 1);
    }
    // wheels roll with distance, the fronts steer; in the hook #7's wheels come off and go back on (wets)
    const rollA = -P.d / .186;
    for (let k = 0; k < 4; k++) {
      const [wx, wy, wz, ws] = WHEELS[k], i4 = id * 4 + k;
      let ox = 0;
      if (id === HERO && s === 0) ox = Math.sign(wx) * (.55 * bump(t, 4.55, 5.35, .2));
      const st = k < 2 ? P.steer : 0;
      part(wheelM, i4, wx + ox, wy, wz, rollA, st, 0, ws, 1, 1);
      part(stripeM, i4, wx + ox + Math.sign(wx) * .1 * ws, wy, wz, rollA, st, 0); setc(stripeM, i4, compound(id, t));
      part(rimM, i4, wx + ox, wy, wz, rollA, st, 0, ws, 1, 1);
      part(spokeM, id * 8 + k * 2, wx + ox, wy, wz, rollA, st, 0, ws, 1, 1);
      part(spokeM, id * 8 + k * 2 + 1, wx + ox, wy, wz, rollA + Math.PI / 2, st, 0, ws, 1, 1);
      part(capWM, i4, wx + ox, wy, wz, rollA, st, 0, ws, 1, 1); setc(capWM, i4, ac);
    }
    let hide = 0; for (const f of FOC) if (f.id === id) hide = Math.max(hide, bump(t, f.a - .35, f.b + .35, .05));
    const hs = hide > .5 ? .001 : 1;
    part(haloM, id, 0, .6, -.01, 0, 0, 0, hs, hs, hs);
    part(haloPM, id, 0, .49, .2, -.42, 0, 0, hs, hs, hs);
    // rear light: on when braking, blinking in the rain
    const lt = Math.max(P.brake, rain * (Math.sin(t * 22 + id) > 0 ? 1 : 0));
    part(lightM, id, 0, .27, -1.0); lightM.setColorAt(id, tmpC.set(0x5a1a14).lerp(tmpC2.set(0xff4030), lt));
    // race numbers
    part(null, 0, 0, .236, .98, -Math.PI / 2 + .1, 0, 0, .8, .8, .8); DECALS[id][0].matrix.copy(MOUT);
    part(null, 0, .011, .575, -.64, 0, Math.PI / 2, 0, .82, .82, .82); DECALS[id][1].matrix.copy(MOUT);
    part(null, 0, -.011, .575, -.64, 0, -Math.PI / 2, 0, .82, .82, .82); DECALS[id][2].matrix.copy(MOUT);
    // the driver: shoulders, HANS, hands on the wheel (it turns with the steering); #11 throws both arms up for the title
    const up = id === MATE ? ss(t, C.wins - .2, C.wins + .3) * (1 - ss(t, C.cuts[4] - .4, C.cuts[4])) : 0;
    const sw = P.steer * 1.7 * (1 - up) + (id === HERO && s === 0 && t > 4.4 && t < 6 ? Math.sin(t * 3) * .1 : 0);
    part(suitM, id, 0, .4, -.05); setc(suitM, id, tc);
    part(hansM, id, 0, .45, -.04);
    part(swM, id, 0, .375, .2, -.45, 0, sw);
    part(swDispM, id, 0, .383, .216, -.45, 0, sw); swDispM.setColorAt(id, tmpC.set(talk > .3 && id === HERO && Math.sin(t * 16) > 0 ? 0xF2B33D : 0x7FE0A8));
    for (let k = 0; k < 2; k++) {
      const sx = k ? -1 : 1, i2 = id * 2 + k;
      const gx = sx * .095 * Math.cos(sw), gy = .375 - sx * .095 * Math.sin(sw) + .01;
      const wave = Math.sin(t * 9 + k * 1.7) * .07;
      const hand = [lerp(gx, sx * .24 + wave * .5, up), lerp(gy, .9 + wave, up), lerp(.185, .03, up)];
      seg(armDM, i2, [sx * .13, .435, -.05], hand, .22); setc(armDM, i2, tc);
      part(gloveM, i2, hand[0], hand[1], hand[2]); setc(gloveM, i2, ac === INK ? 0x3a3532 : ac);
    }
    // the head: expression, G-force lean in the corners, buzz at speed
    const ex = expression(id, t);
    const lean = clamp(-P.k * P.spd * .006, -.2, .2) * (1 - up);
    const hv = Math.sin(t * 47 + id) * .012 * fast;
    MHD.copy(MC).multiply(MR.makeTranslation(...HELMET)).multiply(MP.makeRotationFromEuler(EU.set(ex.nod + hv, ex.shake + ex.lx * .12, ex.tilt + lean, "YXZ")));
    BASEM = MHD;
    part(shellM, id, 0, 0, 0); setc(shellM, id, HELM[id]);
    part(capM, id, 0, 0, 0); setc(capM, id, HTOP[id]);
    part(chinM, id, 0, 0, 0); setc(chinM, id, HELM[id]);
    part(visorM, id, 0, .004, 0, -.06);
    part(foamM, id, 0, -.004, .099);
    part(hStripeM, id, 0, .045, 0); setc(hStripeM, id, id === HERO ? GOLD : id === MATE ? CREAM : ac);
    part(spoilerM, id, 0, .116, -.075, .25); setc(spoilerM, id, HTOP[id]);
    const skin = SKINC[id];
    part(faceM, id, 0, -.005, .012); setc(faceM, id, skin);
    for (let k = 0; k < 2; k++) {
      const sx = k ? .036 : -.036, i2 = id * 2 + k, b = k ? ex.br : ex.bl;
      const ey = .016, ez = .099;
      part(whiteM, i2, sx, ey, ez, 0, 0, 0, 1, 1.12 * ex.eyes, .55);
      const px = sx + ex.lx * .0065, py = ey + ex.ly * .006;
      const pz = ex.eyes > 1.2 ? .82 : 1;
      part(pupilM, i2, px, py, .1065, 0, 0, 0, pz, pz, .6);
      part(eyeHiM, i2, px + .004, py + .0045, .1125);
      part(lidM, i2, sx, ey, ez, (ex.lid - .5) * Math.PI, 0, 0, 1.08, 1.15 * ex.eyes, .62); setc(lidM, i2, skin);
      part(browM, i2, sx, .05 + ex.lift + (k === 0 && ex.bl < -.3 ? .008 : 0), .094, 0, 0, (k ? -1 : 1) * b); setc(browM, i2, BROWC[id]);
      part(cheekM, i2, sx * 1.55, -.024, .092, 0, 0, 0, 1, .65, .4);
    }
    part(noseFM, id, 0, -.007, .111); noseFM.setColorAt(id, tmpC.set(skin).multiplyScalar(.9));
    const mo = ex.mouth, o = mo === "o", g = mo === "grit", arc = !o && !g;
    part(mouthArcM, id, 0, -.038 + (mo === "smile" ? .017 : 0), .1, 0, 0, mo === "smile" ? Math.PI : 0, arc ? 1 : .001, mo === "flat" ? .2 : arc ? 1 : .001, 1);
    part(mouthOM, id, 0, -.036, .1, 0, 0, 0, o ? 1 : .001, o ? 1.15 : .001, 1);
    part(mouthInM, id, 0, -.036, .1035, 0, 0, 0, o ? 1 : .001, o ? 1.15 : .001, 1);
    part(teethM, id, 0, -.038, .1, 0, 0, 0, g ? 1 : .001, g ? 1 : .001, 1);
    part(lipLineM, id, 0, -.038, .1045, 0, 0, 0, g ? 1 : .001, g ? 1 : .001, 1);
    part(sweatM, id, .06, .056 - (t * .03) % .03, .073, 0, 0, 0, ex.sweat ? 1 : .001, ex.sweat ? 1 : .001, ex.sweat ? 1 : .001);
    BASEM = MC;
  }
  for (const m_ of CARPARTS) { m_.instanceMatrix.needsUpdate = true; if (m_.instanceColor) m_.instanceColor.needsUpdate = true; }

  // HUD (#7's position, his tyres) written straight into the page
  if (posEl) {
    const dH = POSE[HERO].d; let p = 1;
    for (let id = 1; id < NC; id++) if (POSE[id].d > dH + .01) p++;
    if (s === 3 && t < TC) p = Math.min(p, 3);
    posEl.textContent = String(p);
    const c = compound(HERO, t);
    tyreEl.textContent = c === CMP.wet ? "WET" : c === CMP.soft ? "SOFT" : "MEDIUM";
    tyreDot.style.background = "#" + col(c).getHexString();
  }

  // pit crew (hook): they run out of the garage, crouch at the wheels with the guns, the jacks lift the car, the
  // lollipop flips from red to green, and they run back
  const crewIn = s === 0 ? ss(t, 3.95, 4.38) * (1 - ss(t, 6.05, 6.5)) : 0;
  const crewVis = s === 0 && t > 3.2 && t < 7.4;
  trackAt(D_BOX, PITLAT, TA);
  const byaw = Math.atan2(TA.tx, TA.tz), bc = Math.cos(byaw), bsn = Math.sin(byaw);
  const guns = bump(t, 4.5, 5.4, .08);
  for (let k = 0; k < NCREW; k++) {
    const [lx, lz] = CREWP[k];
    const gx = TA.x + 2.4 + (k % 3) * .4, gz = TA.z + (k - 4) * .55;
    const px = TA.x + lx * bc + lz * bsn, pz = TA.z - lx * bsn + lz * bc;
    const x = lerp(gx, px, crewIn), z = lerp(gz, pz, crewIn);
    const moving = clamp(bump(t, 3.95, 4.4, .1) + bump(t, 6.05, 6.5, .1));
    const runYaw = Math.atan2(px - gx, pz - gz) + (t > 5 ? Math.PI : 0);
    const carYaw = Math.atan2(TA.x - x + (k === 8 ? 0 : 0), TA.z - z);
    let dy = carYaw - runYaw; dy = Math.atan2(Math.sin(dy), Math.cos(dy));
    const yawC = runYaw + dy * (1 - moving);
    MBC.compose(V.set(x, 0, z), Q.setFromAxisAngle(UP, yawC), S.setScalar(crewVis ? 1 : .001));
    BASEM = MBC;
    const c = (k < 4 ? 1 : k < 6 ? .45 : k < 8 ? .25 : 0) * ss(t, 4.3, 4.5) * (1 - ss(t, 5.9, 6.1));
    const hipY = .62 - .27 * c, shY = 1.06 - .4 * c, fw = .14 * c;
    const ph = t * 15 + k * 1.3, swing = Math.sin(ph) * moving;
    seg(crewTorsoM, k, [0, hipY, -.02], [0, shY, fw + .02], .44);
    for (let j = 0; j < 2; j++) {
      const sx = j ? -.09 : .09, sgn = j ? -1 : 1;
      const foot = [sx * (1 + .5 * c), .07 + Math.max(0, swing * sgn) * .12, swing * sgn * .28 + .22 * c];
      seg(crewLegM, k * 2 + j, [sx, hipY, 0], foot, .41);
      const sh = [sx * 1.7, shY - .04, fw];
      let hand;
      if (k < 4) hand = [sx * .5, shY - .3 - .08 * c, fw + .36];
      else if (k < 6) hand = [sx * .7, shY - .36, fw + .34];
      else if (k < 8) hand = [sx * .8, .5, .42];
      else hand = j ? [-.2, shY - .45, 0] : [.12, shY + .32, .1];
      const runHand = [sx * 2, shY - .42, -swing * sgn * .24];
      const hh = [lerp(hand[0], runHand[0], moving), lerp(hand[1], runHand[1], moving), lerp(hand[2], runHand[2], moving)];
      seg(crewArmM, k * 2 + j, sh, hh, .304);
    }
    part(crewHeadM, k, 0, shY + .17, fw + .03);
    part(crewVisorM, k, 0, shY + .17, fw + .03);
    const has = (b) => (b ? 1 : .001);
    part(gunM, k, 0, shY - .32 - .08 * c, fw + .46, 0, 0, t * 60 * guns, has(k < 4 && moving < .5), has(k < 4 && moving < .5), has(k < 4 && moving < .5));
    if (k >= 4 && k < 6 && moving < .5) seg(jackM, k, [0, shY - .36, fw + .34], [0, .1 + liftHero * 1.2, 1.0], 1);
    else if (k === 8) seg(jackM, k, [.12, shY + .3, .1], [.12, shY + 1.0, .1], 1);
    else part(jackM, k, 0, 0, 0, 0, 0, 0, .001, .001, .001);
    if (k === 8) { part(lolliM, 0, .12, shY + 1.08, .1); lolliM.setColorAt(0, tmpC.set(t < 5.95 ? RED : 0x3FA372)); }
  }
  BASEM = MC;
  for (const m_ of CREWPARTS) { m_.instanceMatrix.needsUpdate = true; if (m_.instanceColor) m_.instanceColor.needsUpdate = true; }

  // markers over #7 and #11 (scaled with distance; hidden up close)
  const look = new THREE.Vector3();
  let fov = camAt(t);
  for (let k = 0; k < 2; k++) {
    const P = POSE[k];
    const dist = CAMP.distanceTo(V.set(P.x, .5, P.z));
    const show = k === 0 ? 1 : (s >= 3 && s <= 4 ? 1 : 0);
    const sc = show * clamp((dist - 9) / 8) * clamp(dist / 20, .6, 4.5);
    MK[k].position.set(P.x, 1.9 + sc * .9 + Math.sin(t * 4 + k) * .12 * sc, P.z);
    MK[k].scale.setScalar(Math.max(.001, sc));
    MK[k].rotation.y = t * 1.5;
  }

  // the radio link from the orb to #7
  const P0 = POSE[HERO];
  beamPos.set([ORB.x, ORB.y - 1.1, ORB.z, P0.x, .9, P0.z]);
  beamG.attributes.position.needsUpdate = true;
  const listen = bump(t, C.listening - .5, C.tyre + .2, .3);
  beamM.opacity = .85 * Math.max(talk, listen);
  for (let k = 0; k < 10; k++) {
    let u = (t * 1.6 + k / 10) % 1;
    if (listen > talk) u = 1 - u;                                    // listening: data flows up from the car
    V.set(lerp(ORB.x, P0.x, u), lerp(ORB.y - 1.1, .9, u), lerp(ORB.z, P0.z, u));
    M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, Math.max(talk, listen) * (1 + .5 * Math.sin(u * Math.PI)))));
    pulseM.setMatrixAt(k, M4);
  }
  pulseM.instanceMatrix.needsUpdate = true;
  // sound rings off #7's engine while the AI listens
  const lr = bump(t, C.listening - .3, C.exactly, .3);
  RINGS.forEach((m, k) => {
    const u = ((t - C.listening) * 1.4 + k / RINGS.length) % 1;
    const c = Math.cos(P0.yaw), sn = Math.sin(P0.yaw);
    m.position.set(P0.x - .7 * sn, .45, P0.z - .7 * c);
    m.scale.setScalar(.3 + u * 2.2);
    m.material.opacity = lr * (1 - u) * .65;
  });
  // the hairpin the AI tells him to attack: a ring on the apex and chevrons along the inside line
  const at = bump(t, C.corner - .4, ATT + .5, .3);
  attRing.position.set(ATTP[0], .1, ATTP[1]); attRing.material.opacity = at * (.6 + .4 * Math.sin(t * 9));
  attRing.scale.setScalar(1 + .15 * Math.sin(t * 9));
  {
    trackAt(D_ATT, 0, TA); const inside = TA.k > 0 ? 1 : -1;
    for (let k = 0; k < CHEV_N; k++) {
      const d = D_ATT - 9 + k * 2.4;
      trackAt(d, inside * 1.0, TB);
      const on = at * ss(t, C.corner - .3 + k * .07, C.corner + k * .07);
      M4.compose(V.set(TB.x, .12, TB.z), Q.setFromAxisAngle(UP, Math.atan2(TB.tx, TB.tz)), S.setScalar(Math.max(.001, on * (1 + .2 * Math.sin(t * 10 - k)))));
      chevM.setMatrixAt(k, M4);
    }
    chevM.instanceMatrix.needsUpdate = true;
  }
  // the crash prediction: dotted paths where the two leaders will spin, a ring where they meet
  const pr = s === 3 ? bump(t, C.crash - .3, TC + .2, .3) : 0;
  for (let j = 0; j < 2; j++) for (let k = 0; k < 26; k++) {
    carXZ(j ? B_ : A_, TC + k * .09, 3, PO);
    const on = pr * ss(t, C.crash - .1 + k * .04, C.crash + k * .04);
    M4.compose(V.set(PO.x, .16, PO.z), Q.identity(), S.setScalar(Math.max(.001, on * (k % 2 ? .7 : 1))));
    predM.setMatrixAt(j * 26 + k, M4);
  }
  predM.instanceMatrix.needsUpdate = true;
  carXZ(A_, TC, 3, PO);
  predRing.position.set(PO.x, .12, PO.z); predRing.material.opacity = pr * (.55 + .45 * Math.sin(t * 12)); predRing.scale.setScalar(1 + .2 * Math.sin(t * 12));
  // smoke and debris after the contact
  const wc = Wt(TC), age = s === 3 ? w - wc : -1;
  for (let k = 0; k < SMOKE_N; k++) {
    let sc = .001;
    if (age > 0) {
      const who = k % 2 ? B_ : A_, born = (k >> 1) * .035;
      const a2 = age - born;
      if (a2 > 0 && a2 < 2.2) {
        carXZ(who, TC + born, 3, PO);
        V.set(PO.x + (hash(k) - .5) * .8, .3 + a2 * .7, PO.z + (hash(k * 3) - .5) * .8);
        sc = (.3 + a2 * .8) * (1 - a2 / 2.2) * (born < 1.1 ? 1 : 0);
      }
    }
    M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, sc)));
    smokeM.setMatrixAt(k, M4);
  }
  smokeM.instanceMatrix.needsUpdate = true;
  carXZ(A_, TC, 3, PO);
  for (let k = 0; k < DEB_N; k++) {
    let sc = .001;
    if (age > 0) {
      const a = hash(k) * Math.PI * 2, sp = 2 + hash(k * 3) * 5, vy = 2 + hash(k * 7) * 3;
      const tt = Math.min(age, vy / 4.9);
      V.set(PO.x + Math.cos(a) * sp * tt, Math.max(.06, vy * tt - 4.9 * tt * tt + .3), PO.z + Math.sin(a) * sp * tt);
      sc = 1;
      debM.setColorAt(k, tmpC.set(k % 3 ? TEAM[A_] : TEAM[B_]));
    }
    M4.compose(V, Q.setFromEuler(EU.set(age * 9 + k, k, age * 7, "XYZ")), S.setScalar(sc));
    debM.setMatrixAt(k, M4);
  }
  debM.instanceMatrix.needsUpdate = true; if (debM.instanceColor) debM.instanceColor.needsUpdate = true;

  // rain round the camera, spray behind every car
  for (let k = 0; k < RAIN_N; k++) {
    const fall = ((hash(k * 3) * 14 - t * 16) % 14 + 14) % 14;
    V.set(CAML.x + (hash(k) - .5) * 36, fall, CAML.z + (hash(k * 5) - .5) * 36);
    M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, rain)));
    rainM.setMatrixAt(k, M4);
  }
  rainM.instanceMatrix.needsUpdate = true;
  for (let id = 0; id < NC; id++) for (let k = 0; k < SPRAY_K; k++) {
    carXZ(id, t - k * .03, s, PO);
    const sp = POSE[id].spd / 30;
    V.set(PO.x - PO.tx * 1.1 + (hash(id * 9 + k) - .5) * .5, .2 + k * .07, PO.z - PO.tz * 1.1 + (hash(id * 7 + k) - .5) * .5);
    M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, rain * clamp(sp) * (.25 + k * .09))));
    sprayM.setMatrixAt(id * SPRAY_K + k, M4);
  }
  sprayM.instanceMatrix.needsUpdate = true;

  // titanium sparks off the plank on the straights
  for (let id = 0; id < NC; id++) for (let k = 0; k < SPK_K; k++) {
    const per = .3 + hash(id * 7 + k) * .45, ph = hash(id * 13 + k * 3) * per;
    const te = Math.floor((t + ph) / per) * per - ph, age = t - te;
    let sc = .001;
    if (age < .2 && rain < .05 && POSE[id].spd > 20) {
      carXZ(id, te, s, PO);
      if (Math.abs(PO.k) < .015) {
        const lat = (hash(id * 31 + k * 7 + Math.floor(te * 10)) - .5) * 2;
        V.set(PO.x - PO.tx * (1.0 + age * 5) + PO.tz * lat * age * 1.4, .05 + age * 1.6 - 9 * age * age, PO.z - PO.tz * (1.0 + age * 5) - PO.tx * lat * age * 1.4);
        sc = 1 - age / .2;
      }
    }
    M4.compose(V, Q.setFromAxisAngle(UP, Math.atan2(PO.tx, PO.tz)), S.setScalar(Math.max(.001, sc)));
    sparkM.setMatrixAt(id * SPK_K + k, M4);
  }
  sparkM.instanceMatrix.needsUpdate = true;

  // fireworks over the circuit when #11 wins the title
  for (let b = 0; b < 6; b++) {
    const tb = C.wins - .2 + b * .45;
    const u = t - tb;
    carXZ(MATE, tb + .6, 4, PO);
    const cx = PO.x + 5 + hash(b * 3) * 9, cz = PO.z - 4 - hash(b * 5) * 9, cy = 6.5 + hash(b * 7) * 3;
    for (let k = 0; k < 70; k++) {
      let sc = .001;
      if (s === 4 && u > 0 && u < 1.8) {
        const th = hash(k * 1.3 + b) * Math.PI * 2, ph = Math.acos(2 * hash(k * 2.7 + b * 9) - 1), sp = 7 + hash(k) * 2;
        V.set(cx + Math.sin(ph) * Math.cos(th) * sp * u * (1 - u * .25), cy + Math.cos(ph) * sp * u * (1 - u * .25) - 2.2 * u * u, cz + Math.sin(ph) * Math.sin(th) * sp * u * (1 - u * .25));
        sc = (2.2 - u * 1.1) * (u < 1.5 ? 1 : 1 - (u - 1.5) / .3);
        fwkM.setColorAt(b * 70 + k, tmpC.set([GOLD, CORAL, CREAM, GOLD, 0xff9a7a, CREAM][b]));
      }
      M4.compose(V, Q.identity(), S.setScalar(Math.max(.001, sc)));
      fwkM.setMatrixAt(b * 70 + k, M4);
    }
  }
  fwkM.instanceMatrix.needsUpdate = true; if (fwkM.instanceColor) fwkM.instanceColor.needsUpdate = true;

  // the real-world beat: thousands of simulated races streaming round the circuit
  const gh = ss(t, C.formula - .4, C.formula + .6) * (1 - ss(t, C.l[7], C.l[7] + 1.2));
  for (let k = 0; k < GH_N; k++) {
    const d = hash(k * 1.7) * TL + w * (24 + hash(k * 3.1) * 18) * (1 + .6 * ss(t, C.billions, C.simulations + .8));
    trackAt(d, (hash(k * 5.3) - .5) * 3.4, PO);
    const on = gh * ss(t, C.formula - .4 + hash(k * 9) * 2.2, C.formula + .2 + hash(k * 9) * 2.2);
    M4.compose(V.set(PO.x, .25 + hash(k * 2) * .3, PO.z), Q.setFromAxisAngle(UP, Math.atan2(PO.tx, PO.tz)), S.setScalar(Math.max(.001, on * 1.6)));
    ghostM.setMatrixAt(k, M4);
  }
  ghostM.instanceMatrix.needsUpdate = true; if (ghostM.instanceColor) ghostM.instanceColor.needsUpdate = true;

  // crowd: jumps on the overtakes, the crash, the finish
  const roar = pulse(t, C.passed, .8) + pulse(t, ATT, .5) + pulse(t, TC + .3, .6) + pulse(t, FIN, .9) * 1.5 + ss(t, C.wins - .3, C.wins) * (1 - ss(t, C.cuts[4] - .5, C.cuts[4]));
  FANS.forEach((f, i) => {
    const y = f.y + Math.min(1, roar) * Math.abs(Math.sin(t * 9 + i)) * .25;
    M4.compose(V.set(f.x, y, f.z), Q.identity(), S.setScalar(1));
    fanM.setMatrixAt(i, M4); fanM.setColorAt(i, tmpC.set(fanBase[i]));
  });
  fanM.instanceMatrix.needsUpdate = true; fanM.instanceColor.needsUpdate = true;

  // start lights go out at the very start; the flag waves on the final lap
  GANTRY.lights.forEach((m, k) => m.color.set(t < .25 ? 0xff3020 : 0x3a1a16));
  const flagOn = s === 4 ? 1 : 0;
  FLAG.g.visible = flagOn > 0;
  if (flagOn) {
    const p = FLAG.geo.attributes.position, b = FLAG.base;
    for (let i = 0; i < p.count; i++) { const x = b[i * 3], y = b[i * 3 + 1], u = (x + .9) / 1.8; p.setZ(i, Math.sin(x * 3.2 - t * 9) * .22 * u + Math.sin(y * 2 + t * 5) * .05 * u); }
    p.needsUpdate = true; FLAG.geo.computeVertexNormals();
    FLAG.g.rotation.z = Math.sin(t * 4.5) * .35;
  }

  // grade: flashes on the cuts, the lightning, the crash; red edges while the crash is predicted
  let fl = 0;
  for (const ct of C.cuts) fl += .7 * Math.exp(-(((t - ct) / .07) ** 2)) * (t >= ct ? 1 : .2);
  fl += .55 * pulse(t, C.rain, .07) + .3 * pulse(t, C.rain + .25, .05) + .35 * pulse(t, TC, .1);
  // tension: letterbox bars, more contrast, fringes and a handheld camera while the crash is coming and on the call;
  // AI vision while it listens and predicts; radial speed blur in the chases and on the hits
  const bars = Math.max(bump(t, C.crash - .35, C.drives + .7, .4), bump(t, C.says - 1.0, FIN + .8, .4));
  const scan = Math.max(.7 * bump(t, C.listening - .3, C.tyre + .3, .3), bump(t, C.crash - .1, C.slows - .3, .2));
  let chaseB = 0;
  for (const [a, b] of [[0, C.ai - .35], [C.six - .45, C.cuts[1]], [C.cuts[2], C.crash - .2], [C.slows - .2, TC - .45]]) chaseB = Math.max(chaseB, bump(t, a, b, .2));
  let slowB = 0; for (const [a, b] of C.slowwin) slowB = Math.max(slowB, bump(t, a, b, .15));
  grade.uniforms.uFlash.value = fl;
  grade.uniforms.uSat.value = 1 - rain * .25 - scan * .35;
  grade.uniforms.uCool.value = rain * .8;
  grade.uniforms.uRed.value = pr * .55;
  grade.uniforms.uBars.value = bars;
  grade.uniforms.uScan.value = scan;
  grade.uniforms.uCon.value = .12 * bars;
  grade.uniforms.uBlur.value = .012 * chaseB + .02 * slowB + .05 * pulse(t, TC, .12) + .03 * pulse(t, C.through + .2, .12) + .03 * pulse(t, ATT, .12);
  grade.uniforms.uCA.value = .0012 + .0035 * bars + .008 * pulse(t, TC, .15) + .006 * pulse(t, C.rain, .1);
  grade.uniforms.uTime.value = t;

  // camera
  let fb = 0;
  for (const f of FOC) fb = Math.max(fb, bump(t, f.a, f.b, .3));
  look.copy(CAML);
  let sh = .25 * pulse(t, TC, .25) + .12 * pulse(t, C.passed, .5) + .1 * pulse(t, ATT, .3);
  camera.position.copy(CAMP);
  camera.position.x += Math.sin(t * .37) * .06 + Math.sin(t * 31) * sh * .3;
  camera.position.y += Math.sin(t * .29 + 1) * .04 + Math.sin(t * 27 + 2) * sh * .2;
  const hand = .035 * bars * Math.min(1, CAMP.distanceTo(CAML) / 3);
  camera.position.x += (Math.sin(t * 3.1) + Math.sin(t * 7.3 + 1) * .5) * hand;
  camera.position.y += (Math.sin(t * 2.7 + 2) + Math.sin(t * 6.1) * .5) * hand;
  camera.fov = fov;
  grade.uniforms.uVig.value = .28 + .5 * fb;
  faceKey.position.copy(camera.position).add(V.set(.3, .5, 0));
  faceKey.intensity = fb * (1.1 + 1.6 * dusk);
  const cv = window.F1_COVER;
  if (cv) { camera.position.set(...cv.cam); camera.fov = cv.fov; look.set(...cv.look); for (const u of ['uBars', 'uBlur', 'uScan', 'uFlash']) grade.uniforms[u].value = 0; grade.uniforms.uCA.value = .001; grade.uniforms.uCon.value = 0; grade.uniforms.uSat.value = 1 - rain * .25; MK.forEach((m) => m.scale.setScalar(.001)); }
  camera.updateProjectionMatrix();
  camera.lookAt(look);
  // shadows follow what the camera looks at
  const cd = camera.position.distanceTo(look), ext = clamp(cd * .7, 8, 62);
  sun.target.position.copy(look); sun.position.set(look.x + 14, 30, look.z + 12);
  Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext, bottom: -ext, near: 1, far: 90 });
  sun.shadow.camera.updateProjectionMatrix();
  scene.fog.near = cd * 1.3 + 20; scene.fog.far = cd * 3 + 80;
  composer.render();
}

const ready = (async () => {
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; });
  renderer.compile(scene, camera);
  renderAt(window.F1_COVER ? window.F1_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["track"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.F1_COVER ? window.F1_COVER.t : e.detail.time));
window.F1_DEBUG = { TL, D_SF, D_ATT, D_CRASH, D_BOX };
