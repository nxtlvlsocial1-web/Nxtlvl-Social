// AI Future reel: "What if your phone could see 24 hours into the future for 30 days?" A first-person POV what-if in the
// voxel style of the owner's reference: your blocky hands (the left one holds the phone), dense blocky cities, game-like
// light. Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek; cue times come from the voice
// (window.CT, written by build/generate.py). Post: depth of field from the depth buffer, bloom, then the grade.
//   s0  New York, morning     the phone shows tomorrow; 9:14 AM, the man across the street drops his coffee
//   s1  Las Vegas casino      the wheel; black 17; the board counts to $2,000,000; you walk out to the Strip
//   s2  Miami, a storm        the warning; you block the road and the drivers yell; at noon the middle span falls, empty
//   s3  home, night, day 21   a message from your own number: don't open the door; a knock
//   s4  home, dawn, day 30    you check tomorrow; the screen is black
//   s5  a rooftop, day        the real part: an AI weather model, ten days ahead
//   s6  the rooftop, dusk     the end card
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const C = window.CT;
const L = C.l, E = C.e, DUR = C.end, CU = C.cuts;
const W = 1080, H = 1920;

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ramp = (t, a, b) => clamp((t - a) / (b - a));
const sm = (x) => x * x * (3 - 2 * x);
const ss = (t, a, b) => sm(ramp(t, a, b));
const lerp = (a, b, x) => a + (b - a) * x;
const hash = (i) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const pulse = (t, a, w = .35) => Math.exp(-(((t - a) / w) ** 2));
const bump = (t, a, b, e = .35) => ss(t, a, a + e) * (1 - ss(t, b - e, b));
const tmpC = new THREE.Color(), BLACK = new THREE.Color(0), WHITE = new THREE.Color(0xffffff);
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), V2 = new THREE.Vector3(), S = new THREE.Vector3(), EU = new THREE.Euler();
const INK = 0x1E1B18, GOLD = 0xF2C94C;
const sceneOf = (t) => { let s = 0; while (s < CU.length && t >= CU[s]) s++; return s; };
const shc = (c, f) => { tmpC.set(c); tmpC.lerp(f < 0 ? BLACK : WHITE, Math.abs(f)); return "#" + tmpC.getHexString(); };
// keyframes: [[t, {k: v}], ...] -> eased values at t (each key holds until the next; smoothstep between)
function kf(t, keys) {
  if (t <= keys[0][0]) return { ...keys[0][1] };
  for (let i = 0; i < keys.length - 1; i++) {
    const [a, p] = keys[i], [b, q] = keys[i + 1];
    if (t < b) { const u = sm(clamp((t - a) / Math.max(1e-4, b - a))); const r = {}; for (const k in p) r[k] = typeof p[k] === "number" && typeof q[k] === "number" ? lerp(p[k], q[k], u) : (u < .5 ? p[k] : q[k] ?? p[k]); for (const k in q) if (!(k in r)) r[k] = q[k]; return r; }
  }
  return { ...keys[keys.length - 1][1] };
}
// hold-and-move keys: [time, duration, values]: the move runs from time to time + duration, holding before and after
function moves(t, base, list) { const cur = { ...base }; for (const [a, d, v] of list) { const u = sm(clamp((t - a) / d)); if (u <= 0) break; for (const k in v) cur[k] = typeof v[k] === "number" ? lerp(cur[k] ?? v[k], v[k], u) : (u < .5 ? cur[k] : v[k]); if (u < 1) break; } return cur; }

// ---------------------------------------------------------------- renderer, scene, post (DOF -> bloom -> output -> grade)
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
scene.fog = new THREE.Fog(0xD6E9F6, 80, 300);
const NEAR = .03, FAR = 900;
const camera = new THREE.PerspectiveCamera(70, W / H, NEAR, FAR);
camera.rotation.order = "YXZ";
scene.add(camera);
const sceneRT = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
sceneRT.depthTexture = new THREE.DepthTexture(W, H);
sceneRT.depthTexture.type = THREE.UnsignedIntType;
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType }));
composer.setPixelRatio(1);
composer.setSize(W, H);
const VS = "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }";
const cocPass = new ShaderPass({
  uniforms: { tScene: { value: null }, tDepth: { value: null }, uF: { value: 5 }, uAp: { value: .3 }, cn: { value: NEAR }, cf: { value: FAR } },
  vertexShader: VS,
  fragmentShader: `uniform sampler2D tScene, tDepth; uniform float uF, uAp, cn, cf; varying vec2 vUv;
    void main(){ vec4 c = texture2D(tScene, vUv); float d = texture2D(tDepth, vUv).x; float z = cn * cf / (cf - d * (cf - cn));
      gl_FragColor = vec4(c.rgb, clamp(uAp * (z - uF) / z, -1., 1.)); }`,
}, "tNone");
cocPass.uniforms.tScene.value = sceneRT.texture;
cocPass.uniforms.tDepth.value = sceneRT.depthTexture;
composer.addPass(cocPass);
const dofPass = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uMaxR: { value: 14 }, uRes: { value: new THREE.Vector2(W, H) } },
  vertexShader: VS,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uMaxR; uniform vec2 uRes; varying vec2 vUv;
    void main(){
      vec4 c0 = texture2D(tDiffuse, vUv); float s0 = c0.a, r0 = abs(s0) * uMaxR;
      vec3 acc = c0.rgb; float ws = 1.;
      for (int i = 0; i < 30; i++) {
        float fi = float(i) + .5; float r = sqrt(fi / 30.) * uMaxR; float a = fi * 2.39996323;
        vec4 c = texture2D(tDiffuse, vUv + vec2(cos(a), sin(a)) * r / uRes);
        float rs = abs(c.a) * uMaxR; if (c.a > s0) rs = min(rs, r0);
        float w = smoothstep(r - 1.5, r + .5, rs); acc += c.rgb * w; ws += w;
      }
      gl_FragColor = vec4(acc / ws, 1.);
    }`,
});
composer.addPass(dofPass);
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .35, .55, .85);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1 }, uVig: { value: .26 }, uFlash: { value: 0 }, uCool: { value: 0 }, uWarm: { value: 0 },
    uCA: { value: 0 }, uCon: { value: 0 }, uDark: { value: 0 }, uTop: { value: 0 } },
  vertexShader: VS,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uCool, uWarm, uCA, uCon, uDark, uTop; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 d = vec2(.5) - vUv;
      vec3 c = vec3(texture2D(tDiffuse, vUv + d * uCA).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - d * uCA).b);
      float g = dot(c, vec3(.299, .587, .114));
      c = mix(vec3(g), c, uSat);
      c = mix(c, c * vec3(.86, .97, 1.14), uCool);
      c = mix(c, c * vec3(1.08, 1.0, .88), uWarm);
      c = (c - .5) * (1. + uCon) + .5;
      vec2 q = vUv - .5; float r = dot(q, q);
      c *= 1. - r * uVig * 2.2;
      c *= 1. - uTop * smoothstep(.2, .75, vUv.y) * .55;        // darker upper half under the title and end card
      vec2 px = vUv * vec2(1080., 1920.);
      c += (h(floor(px) + fract(uTime * 7.13) * 97.) - .5) * .022;
      c = mix(c, vec3(1., .99, .97), uFlash);
      c *= 1. - uDark;
      gl_FragColor = vec4(max(c, 0.), 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- lights (one shadow-casting sun; point lights moved per set)
const hemi = new THREE.HemisphereLight(0xEAF4FF, 0xD6C9B0, 1.0);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xFFF2DC, 2.2);
sun.castShadow = true;
sun.shadow.mapSize.set(4096, 4096);
sun.shadow.bias = -.0004;
sun.shadow.normalBias = .03;
scene.add(sun, sun.target);
const PL = Array.from({ length: 8 }, () => { const l = new THREE.PointLight(0xffffff, 0, 10, 1.6); scene.add(l); return l; });
const phoneL = new THREE.PointLight(0xBFD8FF, 0, 1.2, 2); scene.add(phoneL);

// ---------------------------------------------------------------- materials, primitives, textures
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .85, metalness: 0, ...o });
const gloss = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .3, clearcoat: .7, clearcoatRoughness: .15, envMap: ENV, envMapIntensity: .5, ...o });
const metal = (c, r = .3) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: .85, envMap: ENV, envMapIntensity: 1 });
const glow = (c) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false });
const goldM = new THREE.MeshStandardMaterial({ color: 0xE9B949, roughness: .25, metalness: .9, envMap: ENV, envMapIntensity: 1.3, emissive: 0x4a2a00, emissiveIntensity: .3 });
let PARENT = scene;
const add = (m, cast = true, recv = true, parent) => { m.castShadow = cast; m.receiveShadow = recv; (parent || PARENT).add(m); return m; };
const MATC = new Map();
const cm = (c) => { if (c && (c.isMaterial || Array.isArray(c))) return c; let m = MATC.get(c); if (!m) { m = mat(c); MATC.set(c, m); } return m; };
const BOXG = new THREE.BoxGeometry(1, 1, 1);
const box = (w, h, d, c, x, y, z, o = {}) => {
  const g = o.round ? new RoundedBoxGeometry(w, h, d, 2, Math.min(o.round, w / 2, h / 2, d / 2)) : (Array.isArray(c) || o.uv ? new THREE.BoxGeometry(w, h, d) : BOXG);
  const m = add(new THREE.Mesh(g, cm(c)), o.cast ?? true, o.recv ?? true, o.parent);
  if (g === BOXG) m.scale.set(w, h, d);
  m.position.set(x, y, z); if (o.ry) m.rotation.y = o.ry; if (o.rx) m.rotation.x = o.rx; if (o.rz) m.rotation.z = o.rz;
  return m;
};
const cyl = (r1, r2, h, c, x, y, z, seg = 20, o = {}) => { const m = add(new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), cm(c)), o.cast ?? true, true, o.parent); m.position.set(x, y, z); return m; };
const plane = (w, h, m, x, y, z, ry = 0, parent) => { const p = add(new THREE.Mesh(new THREE.PlaneGeometry(w, h), m), false, false, parent); p.position.set(x, y, z); p.rotation.y = ry; return p; };
function pix(w, h, draw, nearest = true) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); g.imageSmoothingEnabled = false; draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (nearest) t.magFilter = THREE.NearestFilter;
  return t;
}
const px = (g, c, x, y, w = 1, h = 1) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
const rr = (g, x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
const TEX = {};
const LATE = [];     // [material, key, {emissive?}]: textures drawn after the fonts load
const texMat = (key, o = {}) => { const m = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, ...o }); LATE.push([m, key]); return m; };
const setMap = (m, tx) => { if (m.map !== tx) { m.map = tx || null; m.needsUpdate = true; } };
const NIGHTM = [];   // materials whose window mask glows at night: [material, strength]
const rep = (t, x, y) => { const c = t.clone(); c.wrapS = c.wrapT = THREE.RepeatWrapping; c.repeat.set(x, y); c.needsUpdate = true; return c; };

// ---------------------------------------------------------------- characters: blocky figures with pixel faces (from the house voxel engine)
const HIP = .82;
// pixel art, 24 x 24: fringe rows 0-4, brows row 8, eyes rows 10-12 at x 6 and 16, nose 13-14, mouth 16-18
function drawFace(g, sp, eyes, mouth, brows) {
  const S = sp.skin, Hc = sp.hair, D = "#1E1B18", Mo = "#5A2A22", Rd = "#C8483A", Wt = "#FFFDF8";
  px(g, S, 0, 0, 24, 24);
  if (sp.style === "cap") { px(g, sp.cap, 0, 0, 24, 5); px(g, shc(sp.cap, -.3), 0, 4, 24, 1); px(g, Hc, 0, 5, 2, 4); px(g, Hc, 22, 5, 2, 4); }
  else {
    px(g, Hc, 0, 0, 24, 4);
    if (sp.style === "short") { px(g, Hc, 0, 4, 3, 3); px(g, Hc, 21, 4, 3, 3); px(g, Hc, 4, 4, 7, 1); px(g, Hc, 14, 4, 4, 1); }
    if (sp.style === "long" || sp.style === "bun") { px(g, Hc, 0, 4, 24, 1); px(g, Hc, 0, 5, 9, 1); px(g, Hc, 15, 5, 9, 1); px(g, Hc, 0, 6, 3, 10); px(g, Hc, 21, 6, 3, 10); }
    if (sp.style === "bob") { px(g, Hc, 0, 4, 24, 2); px(g, Hc, 0, 6, 3, 11); px(g, Hc, 21, 6, 3, 11); px(g, Hc, 10, 6, 4, 0); }
    if (sp.style === "puff") { px(g, Hc, 0, 4, 2, 5); px(g, Hc, 22, 4, 2, 5); px(g, Hc, 5, 4, 14, 1); }
  }
  px(g, shc(S, -.1), 11, 13, 2, 2);
  if (!sp.beard) { px(g, "#EC9A86", 4, 15, 2, 1); px(g, "#EC9A86", 18, 15, 2, 1); }
  if (sp.beard) { const B = sp.beard; px(g, B, 3, 17, 18, 7); px(g, B, 2, 12, 2, 9); px(g, B, 20, 12, 2, 9); px(g, B, 7, 15, 10, 1); px(g, S, 9, 16, 6, 2); }
  if (sp.stache) px(g, sp.stache, 8, 15, 8, 1);
  const eye = (ex, kind) => {
    if (kind === "open") { px(g, D, ex, 10, 2, 3); px(g, Wt, ex, 10, 1, 1); }
    else if (kind === "closed") px(g, D, ex - 1, 11, 4, 1);
    else if (kind === "happy") { px(g, D, ex - 1, 11, 1, 1); px(g, D, ex, 10, 2, 1); px(g, D, ex + 2, 11, 1, 1); }
    else if (kind === "wide") { px(g, Wt, ex - 1, 10, 4, 3); px(g, D, ex, 10, 2, 2); px(g, Wt, ex, 10, 1, 1); }
    else if (kind === "half") { px(g, shc(S, -.18), ex - 1, 10, 4, 1); px(g, D, ex, 11, 2, 2); }
    else if (kind === "side") { px(g, D, ex + 1, 10, 2, 3); px(g, Wt, ex + 1, 10, 1, 1); }
    if (sp.lash && kind !== "closed" && kind !== "happy") px(g, D, ex + (ex < 12 ? -1 : 2), 9, 1, 1);
  };
  eye(6, eyes === "wink" ? "open" : eyes); eye(16, eyes === "wink" ? "happy" : eyes);
  const Bc = sp.brow || Hc;
  if (brows === "flat") { px(g, Bc, 5, 8, 4, 1); px(g, Bc, 15, 8, 4, 1); }
  if (brows === "up") { px(g, Bc, 5, 7, 4, 1); px(g, Bc, 15, 7, 4, 1); }
  if (brows === "worry") { px(g, Bc, 5, 8, 2, 1); px(g, Bc, 7, 7, 2, 1); px(g, Bc, 15, 7, 2, 1); px(g, Bc, 17, 8, 2, 1); }
  if (brows === "angry") { px(g, Bc, 5, 7, 2, 1); px(g, Bc, 7, 8, 2, 1); px(g, Bc, 15, 8, 2, 1); px(g, Bc, 17, 7, 2, 1); }
  if (brows === "raise1") { px(g, Bc, 5, 6, 4, 1); px(g, Bc, 15, 8, 4, 1); }
  if (mouth === "smile") { px(g, Mo, 10, 17, 4, 1); px(g, Mo, 9, 16, 1, 1); px(g, Mo, 14, 16, 1, 1); }
  if (mouth === "grin") { px(g, Mo, 9, 16, 6, 2); px(g, Wt, 10, 16, 4, 1); px(g, Mo, 8, 15, 1, 1); px(g, Mo, 15, 15, 1, 1); }
  if (mouth === "talk") { px(g, Mo, 10, 16, 4, 2); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "o") { px(g, Mo, 11, 16, 2, 1); px(g, Mo, 10, 17, 1, 1); px(g, Mo, 13, 17, 1, 1); px(g, Mo, 11, 18, 2, 1); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "flat") px(g, Mo, 10, 17, 4, 1);
  if (mouth === "wavy") { px(g, Mo, 9, 17, 1, 1); px(g, Mo, 10, 16, 2, 1); px(g, Mo, 12, 17, 1, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "sad") { px(g, Mo, 10, 16, 4, 1); px(g, Mo, 9, 17, 1, 1); px(g, Mo, 14, 17, 1, 1); }
  if (mouth === "smirk") { px(g, Mo, 10, 17, 3, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "laugh") { px(g, Mo, 9, 16, 6, 3); px(g, Wt, 10, 16, 4, 1); px(g, Rd, 10, 17, 4, 2); }
  if (sp.glasses) {
    const G = sp.glasses;
    for (const x0 of [4, 14]) { px(g, G, x0, 9, 6, 1); px(g, G, x0, 13, 6, 1); px(g, G, x0, 9, 1, 5); px(g, G, x0 + 5, 9, 1, 5); }
    px(g, G, 10, 10, 4, 1); px(g, G, 0, 10, 4, 1); px(g, G, 20, 10, 4, 1);
  }
}
const FACES = new Map(), CHM = new Map();
function faceTex(sp, eyes, mouth, brows) {
  const k = sp.id + "|" + eyes + "|" + mouth + "|" + brows;
  let t = FACES.get(k);
  if (!t) { t = pix(24, 24, (g) => drawFace(g, sp, eyes, mouth, brows)); t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; FACES.set(k, t); }
  return t;
}
const headSide = (sp) => pix(24, 24, (g) => {
  px(g, sp.skin, 0, 0, 24, 24);
  const long = sp.style === "long" || sp.style === "bun" || sp.style === "bob";
  if (sp.style === "cap") { px(g, sp.cap, 0, 0, 24, 5); px(g, sp.hair, 0, 5, 24, 4); }
  else px(g, sp.hair, 0, 0, 24, long ? 16 : 7);
  px(g, shc(sp.skin, -.12), 10, 10, 3, 4);
  if (sp.beard) px(g, sp.beard, 0, 14, 24, 10);
  if (sp.glasses) px(g, sp.glasses, 0, 10, 24, 1);
  if (sp.earring) px(g, "#F2B33D", 10, 15, 3, 3);
});
const headBack = (sp) => pix(24, 24, (g) => { px(g, sp.skin, 0, 0, 24, 24); px(g, sp.style === "cap" ? sp.cap : sp.hair, 0, 0, 24, sp.style === "short" || sp.style === "puff" ? 18 : 24); if (sp.style === "cap") px(g, sp.hair, 0, 8, 24, 10); });
const solidTex = (c) => pix(4, 4, (g) => px(g, c, 0, 0, 4, 4));
function torsoTex(sp, back) {
  return pix(16, 20, (g) => {
    const T = sp.top, Dk = shc(T, -.22), Lt = shc(T, .25);
    px(g, T, 0, 0, 16, 20);
    if (sp.topStyle === "hoodie") { px(g, Dk, 0, 0, 16, 2); px(g, Dk, 0, 18, 16, 2); if (back) px(g, Dk, 3, 1, 10, 5); else { px(g, "#FFFDF8", 6, 2, 1, 6); px(g, "#FFFDF8", 9, 2, 1, 6); px(g, Dk, 3, 12, 10, 5); px(g, T, 4, 13, 8, 3); } }
    if (sp.topStyle === "blazer" && !back) { px(g, "#FFFDF8", 6, 0, 4, 12); px(g, "#FFFDF8", 7, 12, 2, 2); px(g, Dk, 5, 0, 1, 12); px(g, Dk, 10, 0, 1, 12); px(g, "#F2B33D", 7, 14, 2, 1); px(g, "#F2B33D", 7, 17, 2, 1); px(g, "#E8735A", 12, 5, 2, 1); }
    if (sp.topStyle === "tee") { if (!back) { px(g, Dk, 5, 0, 6, 1); px(g, Dk, 6, 1, 4, 1); px(g, Lt, 9, 5, 3, 3); } px(g, Dk, 0, 19, 16, 1); }
    if (sp.topStyle === "cardigan" && !back) { px(g, Dk, 7, 0, 2, 20); for (let k = 0; k < 4; k++) px(g, "#FFFDF8", 7, 4 + k * 4, 1, 1); px(g, "#FFFDF8", 6, 0, 4, 2); }
  });
}
function makeChar(sp, parent = PARENT) {
  const holo = false;
  const M = (c, map = null) => { const k = map ? null : "c" + c; if (k && CHM.has(k)) return CHM.get(k); const m = new THREE.MeshStandardMaterial({ color: map ? 0xffffff : c, map, roughness: .85 }); if (k) CHM.set(k, m); return m; };
  const root = new THREE.Group(); parent.add(root);
  const hips = new THREE.Group(); hips.position.y = HIP; root.add(hips);
  const parts = [];
  const mk = (geo, m, parent, x, y, z) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = !holo; o.receiveShadow = !holo; parent.add(o); parts.push(o); return o; };
  const Bx = (w, h, d) => new THREE.BoxGeometry(w, h, d);
  const topM = M(sp.top), pantsM = M(sp.pants), skinM = M(sp.skin), shoeM = M(sp.shoe), hairM = M(sp.hair);
  const torso = new THREE.Group(); hips.add(torso);
  mk(Bx(.56, .62, .3), [topM, topM, topM, topM, M(0xffffff, torsoTex(sp, false)), M(0xffffff, torsoTex(sp, true))], torso, 0, .31, 0);
  mk(Bx(.55, .14, .29), pantsM, hips, 0, -.04, 0);
  if (sp.topStyle === "hoodie") mk(Bx(.42, .14, .12), M(shc(sp.top, -.15)), torso, 0, .58, -.18);
  mk(Bx(.22, .08, .2), skinM, torso, 0, .64, 0);
  const neck = new THREE.Group(); neck.position.y = .66; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head);
  const faceM = M(0xffffff, faceTex(sp, "open", "smile", "flat"));
  const sideM = M(0xffffff, headSide(sp));
  const capC = sp.style === "cap" ? sp.cap : sp.hair;
  mk(Bx(.52, .52, .52), [sideM, sideM, M(capC), skinM, faceM, M(0xffffff, headBack(sp))], head, 0, .26, 0);
  const hm = M(capC);
  if (sp.style === "cap") { mk(Bx(.56, .17, .56), hm, head, 0, .5, 0); mk(Bx(.5, .04, .24), M(shc(sp.cap, -.15)), head, 0, .425, .36); }
  else {
    mk(Bx(.56, .13, .56), hairM, head, 0, .475, 0);
    if (sp.style === "short") mk(Bx(.22, .07, .2), hairM, head, .07, .57, .06);
    if (sp.style === "long" || sp.style === "bun") { mk(Bx(.58, .7, .08), hairM, head, 0, .18, -.3); for (const s of [-1, 1]) mk(Bx(.06, .5, .24), hairM, head, s * .29, .22, -.12); }
    if (sp.style === "bun") mk(Bx(.22, .2, .22), hairM, head, 0, .63, -.1);
    if (sp.style === "bob") { for (const s of [-1, 1]) mk(Bx(.06, .36, .44), hairM, head, s * .29, .3, -.03); mk(Bx(.58, .4, .08), hairM, head, 0, .3, -.3); }
    if (sp.style === "puff") mk(Bx(.44, .3, .4), hairM, head, 0, .66, -.04);
  }
  if (sp.earring) for (const s of [-1, 1]) mk(Bx(.04, .06, .04), holo ? M(GOLD) : goldM, head, s * .275, .12, .04);
  const sh = [], el = [], hand = [], hip = [], knee = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * .37, .56, 0); torso.add(a); sh.push(a);
    mk(Bx(.17, .32, .18), topM, a, 0, -.13, 0);
    const e = new THREE.Group(); e.position.y = -.29; a.add(e); el.push(e);
    mk(Bx(.16, .27, .17), sp.topStyle === "tee" ? skinM : topM, e, 0, -.13, 0);
    hand.push(mk(Bx(.15, .13, .16), skinM, e, 0, -.32, 0));
    const h = new THREE.Group(); h.position.set(s * .135, 0, 0); hips.add(h); hip.push(h);
    mk(Bx(.23, .42, .25), pantsM, h, 0, -.19, 0);
    const kn = new THREE.Group(); kn.position.y = -.4; h.add(kn); knee.push(kn);
    mk(Bx(.22, .34, .24), pantsM, kn, 0, -.17, 0);
    mk(Bx(.24, .09, .32), shoeM, kn, 0, -.37, .04);
  }
  return { sp, holo, root, hips, torso, head, sh, el, hand, hip, knee, faceM, parts, seed: hash(sp.id.length * 7.3 + sp.skin.charCodeAt(2)) * 10 };
}
const pose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, lean: 0, tw: 0, hy: 0, hp: 0, hr: 0, a: [[.05, .1, .12], [.05, .1, .12]], l: [[0, 0], [0, 0]], ...o });
function mixP(p, q, u) {
  if (u <= 0) return p; if (u >= 1) return q;
  const r = {};
  for (const k in p) { const a = p[k], b = q[k]; r[k] = Array.isArray(a) ? a.map((v, i) => v.map((w, j) => lerp(w, b[i][j], u))) : lerp(a, b, u); }
  return r;
}
function applyPose(P, p) {
  P.root.position.set(p.x, p.y, p.z); P.root.rotation.y = p.ry;
  P.torso.rotation.set(p.lean, p.tw, 0);
  P.head.rotation.set(p.hp, p.hy, p.hr);
  for (let k = 0; k < 2; k++) {
    P.sh[k].rotation.set(-p.a[k][0], 0, (k ? 1 : -1) * p.a[k][1]);
    P.el[k].rotation.x = -p.a[k][2];
    P.hip[k].rotation.x = -p.l[k][0];
    P.knee[k].rotation.x = p.l[k][1];
  }
}
const blinkAt = (seed, t) => { const p = 2.8 + hash(seed) * 1.7, u = (t + hash(seed * 3) * 7) % p; return u < .13; };
let NOW = 0;
function setFace(P, f) {
  let eyes = f.eyes || "open";
  if ((eyes === "open" || eyes === "side") && !f.noblink && blinkAt(P.seed, NOW)) eyes = "closed";
  let mouth = f.mouth || "smile";
  if (f.talk) mouth = Math.floor(NOW * 8.5 + P.seed) % 3 === 0 ? (f.mouth || "smile") : (Math.floor(NOW * 8.5 + P.seed) % 3 === 1 ? "talk" : "o");
  const tx = faceTex(P.sp, eyes, mouth, f.brows || "flat");
  if (P.faceM.map !== tx) { P.faceM.map = tx; if (P.holo) P.faceM.emissiveMap = tx; P.faceM.needsUpdate = true; }
}
function walk(p, ph, amp = 1) {
  const s = Math.sin(ph), c = Math.cos(ph);
  return { ...p, y: p.y + .035 * Math.abs(c) * amp, l: [[.42 * s * amp, (.35 + .3 * Math.max(0, -c)) * amp * (s < 0 ? 1 : .3)], [-.42 * s * amp, (.35 + .3 * Math.max(0, c)) * amp * (s > 0 ? 1 : .3)]],
    a: [[-.38 * s * amp, .1, .25], [.38 * s * amp, .1, .25]] };
}
const idle = (p, t, seed) => ({ ...p, lean: p.lean + .015 * Math.sin(t * 1.3 + seed), hr: p.hr + .03 * Math.sin(t * .9 + seed * 2), hy: p.hy + .05 * Math.sin(t * .6 + seed) });

// ---------------------------------------------------------------- crowd: random blocky people
const PAL = {
  skin: ["#F3CBA5", "#E2AE86", "#C68E68", "#A8714C", "#8E5E40", "#6E4A34", "#F0C49C", "#B57D58"],
  hair: ["#1E1B18", "#3B2A1E", "#8A4A2A", "#B88A4A", "#D8D4CC", "#2A1A12", "#6B3A22", "#1E1B18"],
  style: ["short", "long", "bob", "puff", "cap", "bun", "short", "long"],
  top: ["#23345E", "#7A2E2E", "#3A3A3A", "#C9A27A", "#2F6F5E", "#E8735A", "#5B7FC4", "#F2B33D", "#EFE6D6", "#7E5BB0", "#D9483B", "#4A5A3A", "#8C6A4F", "#2E4057"],
  tstyle: ["blazer", "hoodie", "tee", "cardigan", "blazer", "tee"],
  pants: ["#2E3A55", "#3A3A3A", "#5B5650", "#1E1B18", "#8FB6E0", "#C9B79A", "#3A5A8C"],
  shoe: ["#1E1B18", "#FFFDF8", "#3A2618", "#7A2E2E", "#E8735A"],
};
const pick = (a, k) => a[Math.floor(hash(k) * a.length) % a.length];
function npcSp(i, o = {}) {
  const st = pick(PAL.style, i * 1.7 + .3), sp = { id: "n" + i, skin: pick(PAL.skin, i * 2.3 + .1), hair: pick(PAL.hair, i * 3.1 + .7), style: st, cap: pick(PAL.top, i * 5.3 + .2),
    top: pick(PAL.top, i * 4.7 + .9), topStyle: pick(PAL.tstyle, i * 6.1 + .4), pants: pick(PAL.pants, i * 7.9 + .5), shoe: pick(PAL.shoe, i * 8.3 + .6) };
  if (st === "long" || st === "bun" || st === "bob" || st === "puff") sp.lash = true;
  else if (hash(i * 9.7) > .6) sp.beard = sp.hair;
  if (hash(i * 11.3) > .78) sp.glasses = "#1E1B18";
  return { ...sp, ...o };
}
function npc(i, parent, o = {}) { const P = makeChar(npcSp(i, o), parent); P.seed = hash(i * 13.37) * 10; return P; }
function placeChar(P, vis, p, f) { P.root.visible = !!vis; if (!vis) return; applyPose(P, p); setFace(P, f || {}); }

// ---------------------------------------------------------------- you: blocky hands in front of the camera; the left one holds the phone
const SKIN = "#E0A97E", SLEEVE = "#2E3A55", CUFF = "#46557A";
const handM = mat(SKIN, { roughness: .7 }), sleeveM = mat(SLEEVE, { roughness: .9 }), cuffM = mat(CUFF, { roughness: .9 });
const HANDS = new THREE.Group(); camera.add(HANDS);
function hmesh(w, h, d, m, parent, x, y, z) { const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); o.position.set(x, y, z); o.castShadow = false; o.receiveShadow = true; parent.add(o); return o; }
// a hand pointing up (+y) with the palm facing -z; side -1 left, +1 right; the arm runs down (-y) from the wrist
function makeHand(side) {
  const g = new THREE.Group(); g.rotation.order = "YXZ"; HANDS.add(g);
  hmesh(.096, .1, .042, handM, g, 0, 0, 0);
  const fing = [];
  for (let k = 0; k < 4; k++) { const f = new THREE.Group(); f.position.set((k - 1.5) * .0235, .05, 0); g.add(f); hmesh(.021, .062 - Math.abs(k - 1.2) * .006, .036, handM, f, 0, .03, 0); fing.push(f); }
  const th = new THREE.Group(); th.position.set(-side * .048, -.01, .006); th.rotation.z = -side * .5; g.add(th); hmesh(.026, .056, .032, handM, th, 0, .026, 0);
  hmesh(.112, .03, .062, cuffM, g, 0, -.062, .002);
  const arm = new THREE.Group(); arm.position.set(0, -.07, 0); g.add(arm);
  hmesh(.104, .7, .06, sleeveM, arm, 0, -.35, 0);
  return { g, fing, th, arm };
}
const RH = makeHand(1);
// the phone in the left hand: screen faces +z (the camera); the hand grips it from behind and the sides
const PHONE = new THREE.Group(); PHONE.rotation.order = "YXZ"; HANDS.add(PHONE);
const phBody = new THREE.Mesh(new RoundedBoxGeometry(.078, .162, .009, 2, .008), new THREE.MeshPhysicalMaterial({ color: 0x15171C, roughness: .3, metalness: .4, clearcoat: 1, envMap: ENV, envMapIntensity: .6 }));
PHONE.add(phBody);
const phScrM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
const phScr = new THREE.Mesh(new THREE.PlaneGeometry(.0715, .1545), phScrM); phScr.position.z = .0049; PHONE.add(phScr);
const phGlass = new THREE.Mesh(new THREE.PlaneGeometry(.0715, .1545), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: .07, roughness: .05, envMap: ENV, envMapIntensity: 1.2, depthWrite: false }));
phGlass.position.z = .0052;
const LH = { g: new THREE.Group() }; PHONE.add(LH.g);
hmesh(.064, .1, .034, handM, LH.g, .006, -.05, -.024);                        // palm behind the phone
for (let k = 0; k < 3; k++) hmesh(.012, .018, .026, handM, LH.g, .044, -.025 - k * .024, -.012);   // fingertips round the right edge
hmesh(.011, .03, .02, handM, LH.g, -.0425, -.062, -.012);    // thumb on the left edge
hmesh(.08, .032, .056, cuffM, LH.g, .006, -.11, -.024);
const lArm = new THREE.Group(); lArm.position.set(.004, -.115, -.026); lArm.rotation.x = .55; LH.g.add(lArm);
hmesh(.086, .7, .054, sleeveM, lArm, 0, -.35, 0);
// poses in camera space: the phone (p*) and the free right hand (r*); f = finger curl
const HP = {
  phDown: { px: -.17, py: -.42, pz: -.36, prx: -.5, pry: .25, prz: .15 },
  phLow: { px: -.075, py: -.235, pz: -.34, prx: -.42, pry: .12, prz: .06 },
  phRead: { px: .03, py: .004, pz: -.3, prx: -.08, pry: 0, prz: 0 },
  phHalf: { px: -.03, py: -.12, pz: -.3, prx: -.22, pry: .06, prz: .03 },
  rDown: { rx: .2, ry: -.5, rz: -.36, rrx: -1.15, rry: .2, rrz: .2, f: .9 },
  rRest: { rx: .16, ry: -.29, rz: -.34, rrx: -1.0, rry: .15, rrz: .15, f: .8 },
  rStop: { rx: .17, ry: -.05, rz: -.56, rrx: .08, rry: -.12, rrz: -.08, f: 0 },
};
const LSTOP = { px: -.17, py: -.06, pz: -.56, prx: .08, pry: .12, prz: .08 };
function setHands(h) {
  PHONE.visible = h.phone !== false;
  PHONE.position.set(h.px, h.py, h.pz); PHONE.rotation.set(h.prx, h.pry, h.prz);
  RH.g.visible = h.right !== false;
  RH.g.position.set(h.rx, h.ry, h.rz); RH.g.rotation.set(h.rrx, h.rry, h.rrz);
  for (const f of RH.fing) f.rotation.x = (h.f ?? 0) * 1.3;
  RH.arm.rotation.x = .5 * (h.f ?? 0) - .15;
}
// the left hand without the phone (blocking the road): a mirrored copy of the right hand
const LHF = makeHand(-1); LHF.g.visible = false;

// ---------------------------------------------------------------- the cast: Alex (the navy hoodie matches the POV sleeves), Jay, the driver
const SP_ALEX = { id: "alex", skin: "#E2AE86", hair: "#2A1A12", style: "short", top: "#2E3A55", topStyle: "hoodie", pants: "#3A3A3A", shoe: "#F4EFE6" };
const SP_JAY = { id: "jay", skin: "#B57D58", hair: "#1E1B18", style: "cap", cap: "#D9483B", top: "#F2B33D", topStyle: "tee", pants: "#2E3A55", shoe: "#FFFDF8", beard: "#1E1B18" };
const SP_DRIVER = { id: "driver", skin: "#C68E68", hair: "#3B2A1E", style: "cap", cap: "#7A2E2E", beard: "#3B2A1E", top: "#3A5A8C", topStyle: "tee", pants: "#2E3A55", shoe: "#1E1B18" };
// the phone in Alex's hand when the camera sees him (third person)
const APH = new THREE.Group(); scene.add(APH); APH.visible = false;
APH.add(new THREE.Mesh(new RoundedBoxGeometry(.1, .2, .016, 2, .012), new THREE.MeshPhysicalMaterial({ color: 0x15171C, roughness: .3, metalness: .4, clearcoat: 1, envMap: ENV })));
const aphM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
const aphS = new THREE.Mesh(new THREE.PlaneGeometry(.09, .188), aphM); aphS.position.z = .0085; APH.add(aphS);

// ---------------------------------------------------------------- cars: blocky sedans and taxis, front at -z
const glassM = new THREE.MeshPhysicalMaterial({ color: 0x1C2836, roughness: .08, metalness: .2, transparent: true, opacity: .3, envMap: ENV, envMapIntensity: 1.2 });
const tireM = mat(0x1A1A1C, { roughness: .9 }), hubM = metal(0xB8BCC4, .35), chromeM = metal(0xD8DCE2, .2);
function car(col, o = {}) {
  const g = new THREE.Group(); (o.parent || PARENT).add(g);
  const P = { parent: g }, bodyM = gloss(col, { roughness: .35 });
  box(2.1, .62, 4.6, bodyM, 0, .66, 0, P);
  box(2.0, .2, 1.3, bodyM, 0, 1.05, -1.6, P);
  box(2.0, .2, 1.0, bodyM, 0, 1.05, 1.75, P);
  box(1.96, .1, 2.35, bodyM, 0, 2.08, .2, P);
  for (const sx of [-.93, .93]) for (const sz of [-.95, 1.35]) box(.1, .95, .1, bodyM, sx, 1.6, sz, P);
  box(2.0, .12, 2.3, bodyM, 0, 1.1, .2, P);
  const wf = box(1.84, .95, .04, glassM, 0, 1.6, -1.0, { parent: g, cast: false }); wf.rotation.x = -.42;
  const wb = box(1.84, .9, .04, glassM, 0, 1.6, 1.38, { parent: g, cast: false }); wb.rotation.x = .3;
  box(1.7, .5, .5, mat(0x2A2420), 0, 1.2, .9, P);      // the back seat
  box(2.16, .2, .2, chromeM, 0, .5, -2.32, P); box(2.16, .2, .2, chromeM, 0, .5, 2.32, P);
  for (const sx of [-.72, .72]) { box(.38, .16, .06, glow(0xFFF6DA), sx, .78, -2.31, { parent: g, cast: false }); box(.36, .14, .06, glow(0xFF3B30), sx, .8, 2.31, { parent: g, cast: false }); }
  box(.9, .12, .05, mat(0x15151A), 0, .62, -2.32, P);
  for (const sx of [-1.02, 1.02]) for (const sz of [-1.5, 1.5]) {
    const w = new THREE.Mesh(new THREE.CylinderGeometry(.37, .37, .28, 18), tireM); w.rotation.z = Math.PI / 2; w.position.set(sx, .37, sz); w.castShadow = true; g.add(w);
    const hb = new THREE.Mesh(new THREE.CylinderGeometry(.2, .2, .3, 12), hubM); hb.rotation.z = Math.PI / 2; hb.position.set(sx, .37, sz); g.add(hb);
  }
  if (o.taxi) { box(.7, .2, .3, glow(0xFFF3C0), 0, 2.24, .2, P); for (const sx of [-1.06, 1.06]) box(.02, .14, 2.8, mat(INK), sx, .9, 0, P); }
  return g;
}
const CARCOL = [0xF4F1EA, 0x23345E, 0xB8BCC4, 0x7A2E2E, 0x2F6F5E, 0x1E1B18, 0x5B7FC4, 0xC9A27A];

// ---------------------------------------------------------------- city facades: one floor bay tile, repeated (and its night window mask)
const BAYW = 2, BAYH = 3;
function bayTex(style, lit = false) {
  const S = { brick: ["#9C4A3A", "#8A3F31"], brown: ["#7A5040", "#6B4436"], stone: ["#CDBB9C", "#BFAD8E"], grey: ["#A7ABB0", "#979BA1"], cream: ["#E6DCC8", "#D6CCB8"], glass: ["#5D7E99", "#4F6E88"], pink: ["#F2C4C8", "#E6B2B8"], mint: ["#BFE3D3", "#AED3C2"], peach: ["#F6D2B0", "#EBC39F"], white: ["#F1EEE6", "#E3DFD5"] }[style];
  return pix(64, 96, (g) => {
    if (lit) { px(g, "#000", 0, 0, 64, 96); if (style !== "glass") { px(g, "#FFD9A0", 14, 26, 36, 44); } else px(g, "#FFE2B0", 2, 6, 60, 80); return; }
    px(g, S[0], 0, 0, 64, 96);
    if (style === "brick" || style === "brown") for (let y = 0; y < 96; y += 4) for (let x = ((y / 4) % 2) * 4 - 4; x < 64; x += 8) { g.fillStyle = hash(x * .37 + y * 1.3 + 7) > .5 ? "rgba(255,255,255,.06)" : "rgba(0,0,0,.07)"; g.fillRect(x, y, 7, 3); }
    if (style === "glass") { px(g, "#7FA4C2", 2, 4, 60, 84); px(g, "#9FC0DA", 2, 4, 60, 18); px(g, "#4F6E88", 0, 88, 64, 8); px(g, "#3E5A72", 31, 4, 2, 84); return; }
    px(g, S[1], 0, 88, 64, 8);                       // floor band
    px(g, shc(S[0], .35), 12, 70, 40, 4);            // sill
    px(g, shc(S[0], .25), 12, 22, 40, 4);            // lintel
    px(g, "#2B3442", 14, 26, 36, 44);                // window
    px(g, "#6E8CA8", 16, 28, 32, 40); px(g, "#93B0CA", 16, 28, 32, 10); px(g, "#58748E", 16, 48, 32, 2);
    px(g, shc(S[0], .2), 31, 26, 2, 44);
  }, false);
}
const BAY = {}, BAYL = {};
const STYLES = ["brick", "brown", "stone", "grey", "cream", "glass", "pink", "mint", "peach", "white"];
for (const s of STYLES) { BAY[s] = bayTex(s); BAYL[s] = bayTex(s, true); }
const STORE = ["#2F6F5E", "#7A2E2E", "#23345E", "#1E1B18", "#C9932E", "#D9607A", "#3A6FC4"];
function storeTex(c) {
  return pix(96, 64, (g) => {
    px(g, "#3A3330", 0, 0, 96, 64); px(g, c, 0, 0, 96, 12);
    px(g, "#E8DCC4", 0, 12, 96, 3);
    for (let k = 0; k < 2; k++) { const x = 6 + k * 50; px(g, "#1C2430", x, 20, 34, 40); px(g, "#7FA0BC", x + 2, 22, 30, 34); px(g, "#A9C4DA", x + 2, 22, 30, 8); px(g, "#FFE7B8", x + 4, 46, 26, 6); }
    px(g, "#1E1B18", 41, 22, 14, 42); px(g, "#6E8CA8", 43, 25, 10, 16); px(g, "#C9A27A", 51, 44, 2, 2);
  }, false);
}
const STT = STORE.map(storeTex);
// a building block: tile facade on the street side, a storefront band, a cornice; side = +1 (faces -x) or -1 (faces +x)
function tower(o) {
  const { x0, z0, len, h, depth = 12, style, side } = o, P = o.parent ? { parent: o.parent } : {};
  const cx = x0 + side * depth / 2, cz = z0 - len / 2, wall = mat(shc(bayColor(style), -.08));
  const ft = rep(BAY[style], len / BAYW, (h - 4.2) / BAYH), fl = rep(BAYL[style], len / BAYW, (h - 4.2) / BAYH);
  const fm = new THREE.MeshStandardMaterial({ map: ft, emissiveMap: fl, emissive: 0xFFD9A0, emissiveIntensity: 0, roughness: style === "glass" ? .3 : .85, metalness: style === "glass" ? .3 : 0, envMap: style === "glass" ? ENV : null, envMapIntensity: .8 });
  NIGHTM.push([fm, 1]);
  const mats = [wall, wall, mat(0x8E8A84), wall, wall, wall]; mats[side > 0 ? 1 : 0] = fm;
  box(depth, h - 4.2, len, mats, cx, 4.2 + (h - 4.2) / 2, cz, { ...P, uv: 1 });
  const sm_ = new THREE.MeshStandardMaterial({ map: rep(STT[o.store ?? 0], len / 3, 1), roughness: .8 });
  const smats = [wall, wall, wall, wall, wall, wall]; smats[side > 0 ? 1 : 0] = sm_;
  box(depth, 4.2, len, smats, cx, 2.1, cz, { ...P, uv: 1 });
  box(.5, .6, len + .02, shc(bayColor(style), .3), x0 - side * .15, h - .3, cz, P);
  box(.3, .3, len, shc(bayColor(style), .2), x0 - side * .1, 4.25, cz, P);
  return { cx, cz };
}
const bayColor = (s) => ({ brick: "#9C4A3A", brown: "#7A5040", stone: "#CDBB9C", grey: "#A7ABB0", cream: "#E6DCC8", glass: "#5D7E99", pink: "#F2C4C8", mint: "#BFE3D3", peach: "#F6D2B0", white: "#F1EEE6" }[s]);

// ---------------------------------------------------------------- shared ground textures
const noiseTex = (base, n, amp, sz = 64) => pix(sz, sz, (g) => { px(g, base, 0, 0, sz, sz); for (let i = 0; i < sz; i++) for (let j = 0; j < sz; j++) { const h = hash(i * 31.7 + j * 7.3 + n); if (h > .7) { g.fillStyle = `rgba(${h > .85 ? "255,255,255" : "0,0,0"},${amp})`; g.fillRect(i, j, 1, 1); } } }, false);
const ASPH = noiseTex("#4A4C52", 1, .07), SAND = noiseTex("#C9B48A", 2, .08), GRAVEL = noiseTex("#8E8A84", 3, .1), CONC = noiseTex("#B9B4AA", 4, .05);
const tileTex = pix(64, 64, (g) => { px(g, "#C4BFB6", 0, 0, 64, 64); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { g.fillStyle = hash(i * 5 + j * 3) > .5 ? "rgba(255,255,255,.05)" : "rgba(0,0,0,.04)"; g.fillRect(i * 16, j * 16, 16, 16); } for (let k = 0; k < 4; k++) { px(g, "#A9A39A", k * 16, 0, 1, 64); px(g, "#A9A39A", 0, k * 16, 64, 1); } }, false);
const groundMat = (t, x, y, o = {}) => new THREE.MeshStandardMaterial({ map: rep(t, x, y), roughness: .92, ...o });
function flat(w, d, m, x, y, z, parent) { const p = add(new THREE.Mesh(new THREE.PlaneGeometry(w, d), m), false, true, parent); p.rotation.x = -Math.PI / 2; p.position.set(x, y, z); return p; }
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };

// ================================================================= s0 NEW YORK: an avenue, morning
mkSet("ny");
{
  flat(10, 280, groundMat(ASPH, 4, 110), 0, 0, -110);
  const lineM = mat(0xF2EEE4), yelM = mat(0xE9B949);
  for (let z = 14; z > -240; z -= 6) for (const x of [-2.5, 2.5]) box(.14, .02, 2.6, lineM, x, .012, z, { cast: false });
  for (const x of [-.12, .12]) box(.1, .02, 280, yelM, x, .012, -110, { cast: false });
  for (let k = 0; k < 9; k++) box(.7, .02, 3.2, lineM, -4 + k * 1.0, .013, -16.5, { cast: false });   // crosswalk
  for (let k = 0; k < 9; k++) box(.7, .02, 3.2, lineM, -4 + k * 1.0, .013, -22.5, { cast: false });
  for (const sx of [-1, 1]) {
    box(5, .15, 280, groundMat(tileTex, 2.5, 140), sx * 7.5, .075, -110, { cast: false, uv: 1 });
    box(.22, .17, 280, mat(0x9C978E), sx * 5.05, .085, -110, { cast: false });
  }
  flat(40, 8, groundMat(ASPH, 16, 3), 0, .005, -19.5);
  // buildings: blocks down both sides, a cross street at z -14..-25
  const blocks = [];
  for (const side of [1, -1]) {
    let z = 14, k = side > 0 ? 0 : 50;
    while (z > -260) {
      if (z <= -14 && z > -25) { z = -25; continue; }
      let len = 7 + hash(k * 1.3) * 9; if (z > -14 && z - len < -14) len = z + 14;
      const h = 16 + hash(k * 2.7) * (side > 0 ? 30 : 46) + (z < -60 ? 20 * hash(k * .9) : 0);
      const style = ["brick", "brown", "stone", "grey", "cream", "glass", "brick", "stone"][Math.floor(hash(k * 3.9) * 8)];
      const T = tower({ x0: side * 10, z0: z, len, h, style, side, store: Math.floor(hash(k * 5.1) * STORE.length) });
      blocks.push({ side, z, len, h, style, k });
      if (hash(k * 7.7) > .5 && h < 40) {                     // a water tower on the roof
        const wx = side * (13 + hash(k) * 4), wz = z - len / 2;
        for (const dx of [-.8, .8]) for (const dz of [-.8, .8]) box(.15, 2.2, .15, mat(0x3A3330), wx + dx, h + 1.1, wz + dz);
        cyl(1.25, 1.25, 2.4, mat(0x8A6A4A), wx, h + 3.4, wz, 16); const cone = new THREE.Mesh(new THREE.ConeGeometry(1.35, 1, 16), mat(0x5A4434)); cone.position.set(wx, h + 5.1, wz); add(cone);
      }
      if ((style === "brick" || style === "brown") && h > 18) {   // fire escape
        const fx = side * 10 - side * .55, fz = z - len * .35;
        for (let f = 0; f < Math.floor((h - 6) / BAYH); f++) { const y = 4.2 + BAYH * (f + 1) - .1; box(.9, .06, 2.6, mat(0x222326), fx, y, fz); box(.04, .5, 2.6, mat(0x222326), fx - side * .43, y + .25, fz); }
      }
      z -= len; k++;
    }
  }
  // the skyline beyond
  for (let k = 0; k < 18; k++) { const x = (hash(k * 4.1) - .5) * 160, z = -170 - hash(k * 2.2) * 140, h = 80 + hash(k * 6.6) * 150, w = 12 + hash(k) * 14; if (Math.abs(x) < 14) continue; tower({ x0: x - w / 2, z0: z + w / 2, len: w, h, depth: w, style: k % 3 ? "glass" : "grey", side: 1 }); }
  // street furniture
  const poleM = mat(0x2F3D33, { roughness: .6 });
  const lamp = (x, z, s) => { box(.16, 6.4, .16, poleM, x, 3.2, z); box(1.5, .1, .12, poleM, x - s * .7, 6.35, z); box(.5, .14, .3, mat(0xD8D4CC), x - s * 1.4, 6.24, z); };
  for (let z = 6; z > -200; z -= 16) { lamp(5.6, z, 1); lamp(-5.6, z - 8, -1); }
  const tlight = (x, z, s) => { box(.18, 5.2, .18, mat(0x2A2A2E), x, 2.6, z); box(2.6, .12, .12, mat(0x2A2A2E), x - s * 1.3, 5.1, z); const hb = box(.38, 1.0, .34, mat(0xC9A227), x - s * 2.4, 4.6, z); box(.2, .2, .05, glow(0x42F59B), x - s * 2.4, 4.3, z + .18, { cast: false }); box(.2, .2, .05, mat(0x3A1A1A), x - s * 2.4, 4.85, z + .18, { cast: false }); };
  tlight(5.6, -13.5, 1); tlight(-5.6, -25.5, -1);
  box(.36, .7, .36, mat(0xC8372D), 5.9, .5, -11.5); box(.5, .14, .2, mat(0xC8372D), 5.9, .55, -11.5);          // hydrant
  box(.7, 1.0, .7, mat(0x2F5F3A), 9.3, .65, 2.4); box(.8, .1, .8, mat(0x24492D), 9.3, 1.2, 2.4);            // bin
  box(.9, 1.4, .6, mat(0x2C4E9A), -9.2, .85, -6.0); box(.9, .25, .6, mat(0x24407E), -9.2, 1.62, -6.0);     // mailbox
  // newsstand
  box(3.2, 2.6, 1.8, mat(0x2F6F5E), -8.6, 1.45, -34); box(3.5, .14, 2.3, mat(0x24574A), -8.6, 2.82, -33.8);
  for (let k = 0; k < 6; k++) box(.4, .5, .04, mat(["#F4F1EA", "#E8735A", "#F2B33D", "#5B7FC4"][k % 4]), -9.8 + k * .45, 1.3, -33.08);
  // trees in pits on the left sidewalk
  for (let z = -4; z > -90; z -= 13) { box(.3, 3.2, .3, mat(0x5A4434), -8.9, 1.75, z); for (let j = 0; j < 5; j++) box(1.6 - j * .15, 1.0, 1.6 - j * .15, mat(j % 2 ? 0x5E8A44 : 0x6F9E52), -8.9 + (hash(z + j) - .5) * .5, 3.4 + j * .55, z + (hash(z * 2 + j) - .5) * .5); }
  // billboards: angled on the left, blades on the right
  const bb = (key, x, y, z, w, h, ry) => { const g = box(w + .4, h + .4, .3, mat(0x2A2A2E), x, y, z, { ry }); plane(w, h, texMat(key, { transparent: false }), x + Math.sin(ry) * .16, y, z + Math.cos(ry) * .16, ry); box(.3, y - 1, .3, mat(0x2A2A2E), x, (y - h / 2) / 2, z - .6, { ry }); };
  bb("bbCoffee", -9.4, 15, -30, 9, 5, .7);
  bb("bbShow", -9.6, 21, -58, 11, 6, .62);
  bb("bbRun", -9.6, 16, -88, 10, 5.4, .55);
  const blade = (key, x, y, z, h) => { box(.25, h + .3, 1.5, mat(0x2A2A2E), x, y, z); plane(1.3, h, texMat(key, { transparent: false }), x - .14, y, z, -Math.PI / 2); plane(1.3, h, texMat(key, { transparent: false }), x, y, z + .76, 0); };
  blade("blHotel", 9.6, 11, -44, 6); blade("blTheatre", 9.6, 9, -74, 5);
  // the LED time sign by the man (9:13 -> 9:14)
  box(2.5, 1.15, .3, mat(0x1A1A1E), 8.55, 5.0, -9.3); box(.9, .12, .12, mat(0x2A2A2E), 9.6, 5.0, -9.3);
  SET.ny.ledM = texMat("led913", { transparent: false }); plane(2.3, .95, SET.ny.ledM, 8.55, 5.0, -9.14, 0);
  // the man's coffee cup, a puddle and drops
  const cup = new THREE.Group(); SET.ny.add(cup); SET.ny.cup = cup;
  const cw = new THREE.Mesh(new THREE.CylinderGeometry(.075, .058, .2, 14), mat(0xF4F1EA)); cw.castShadow = true; cup.add(cw);
  const cs = new THREE.Mesh(new THREE.CylinderGeometry(.078, .07, .08, 14), mat(0x9A6A3E)); cup.add(cs);
  const cl = new THREE.Mesh(new THREE.CylinderGeometry(.08, .08, .025, 14), mat(0x2A2A2E)); cl.position.y = .11; cup.add(cl);
  const pud = new THREE.Mesh(new THREE.CircleGeometry(.6, 20), new THREE.MeshStandardMaterial({ color: 0x5A3418, roughness: .15, metalness: .1, envMap: ENV, envMapIntensity: .5 }));
  pud.rotation.x = -Math.PI / 2; pud.receiveShadow = true; SET.ny.add(pud); SET.ny.pud = pud;
  SET.ny.drops = Array.from({ length: 14 }, (_, k) => { const m = new THREE.Mesh(BOXG, mat(0x6B3E1E)); m.scale.setScalar(.05 + hash(k) * .03); SET.ny.add(m); return m; });
  // traffic: taxis and cars on both directions
  SET.ny.cars = [];
  for (let k = 0; k < 10; k++) { const taxi = k % 3 !== 2; const g = car(taxi ? 0xF2C230 : CARCOL[k % CARCOL.length], { taxi }); g.userData = { lane: [-3.6, -1.2, 1.2, 3.6][k % 4], z0: -k * 23 - hash(k) * 8, v: 6 + hash(k * 3) * 3 }; SET.ny.cars.push(g); }
  // people: walkers on both sidewalks, a few standing, and the man with the coffee
  SET.ny.walk = [];
  for (let k = 0; k < 18; k++) {
    const P = npc(k, SET.ny), lane = [9.2, -7.0, -8.7, 9.2, -7.0, -8.7][k % 6], dir = lane > 0 ? -1 : (lane > -8 ? 1 : -1);
    P.u = { lane, dir, z0: -hash(k * 1.9) * 70, v: 1.05 + hash(k * 2.3) * .35, ph: hash(k) * 6 };
    SET.ny.walk.push(P);
  }
  SET.ny.stand = [[-7.8, -12, 1.2], [-8.4, -12.6, -2.0], [6.3, -15.2, 3.0], [8.6, -20, -1.6]].map(([x, z, ry], k) => { const P = npc(40 + k, SET.ny); P.u = { x, z, ry }; return P; });
  SET.ny.man = makeChar({ id: "coffee", skin: "#E8B894", hair: "#3B2A1E", style: "short", beard: "#3B2A1E", top: "#8A8F98", topStyle: "blazer", pants: "#2E3A55", shoe: "#3A2618" }, SET.ny);
  SET.ny.alex = makeChar(SP_ALEX, SET.ny); SET.ny.alex.seed = 1.3;
  SET.ny.man.seed = 4.2;
}

// ================================================================= s1 LAS VEGAS: a casino floor, the roulette table
const WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26];
const REDS = new Set([1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]);
const WIN = 17, WINI = WHEEL.indexOf(WIN), WC = new THREE.Vector3(0, 1.1, -3.95);
const cellZ = (n) => -2.45 + (Math.ceil(n / 3) - 1) * .33, cellX = (n) => ((n - 1) % 3 - 1) * .55;
mkSet("vegas");
{
  const carpet = pix(64, 64, (g) => { px(g, "#5A1420", 0, 0, 64, 64); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const x = i * 16 + 8, y = j * 16 + 8; px(g, "#C9932E", x - 1, y - 5, 2, 10); px(g, "#C9932E", x - 5, y - 1, 10, 2); px(g, "#2A0A12", x - 2, y - 2, 4, 4); px(g, "#8A2A36", i * 16, j * 16, 3, 3); } });
  flat(40, 40, groundMat(carpet, 14, 14, { roughness: 1 }), 0, 0, 0);
  flat(40, 40, mat(0x170D10), 0, 5.2, 0).rotation.x = Math.PI / 2;
  const dl = new THREE.InstancedMesh(new THREE.BoxGeometry(.35, .04, .35), glow(0xFFE2B0), 120); let n = 0;
  for (let i = -5; i <= 5; i++) for (let j = -5; j <= 5; j++) if (n < 120) { M4.makeTranslation(i * 3.2, 5.17, j * 2.6); dl.setMatrixAt(n++, M4); }
  dl.count = n; add(dl, false, false);
  // walls
  const wallM = mat(0x2A1418), panelM = mat(0x3A1E20);
  box(40, 5.2, .3, wallM, 0, 2.6, -13);
  box(.3, 5.2, 26, wallM, -10, 2.6, 0); box(.3, 5.2, 26, wallM, 10, 2.6, 0);
  box(16, 5.2, .3, wallM, -12, 2.6, 11.5); box(16, 5.2, .3, wallM, 12, 2.6, 11.5); box(8, 1.6, .3, wallM, 0, 4.4, 11.5);
  for (const sx of [-1, 1]) for (let z = -10; z < 11; z += 5) box(.1, 3.5, 2.6, panelM, sx * 9.8, 2.2, z);
  plane(7, 2.2, texMat("neonCasino"), 0, 3.6, -12.8, 0);
  plane(3.6, 1.2, texMat("neonJackpot"), -6.5, 3.4, -12.8, 0); plane(3.6, 1.2, texMat("neonJackpot"), 6.5, 3.4, -12.8, 0);
  // the doors to the Strip (behind you), and the Strip itself
  for (const sx of [-1, 1]) box(.25, 3.6, .4, goldM, sx * 4, 1.8, 11.5);
  box(8.2, .25, .4, goldM, 0, 3.6, 11.5);
  for (const sx of [-1.95, 1.95]) { const d = box(1.9, 3.3, .06, new THREE.MeshPhysicalMaterial({ color: 0x9FB8D0, transparent: true, opacity: .18, roughness: .05, envMap: ENV }), sx, 1.65, 11.4, { cast: false }); }
  plane(1.4, .45, texMat("exitSign"), 0, 4.0, 11.3, Math.PI);
  plane(60, 26, texMat("strip", { transparent: false }), 0, 10, 26, Math.PI);
  flat(60, 16, mat(0x1A1A22, { roughness: .4, metalness: .2 }), 0, .01, 19);
  // pillars and chandeliers
  for (const [x, z] of [[-3.4, -7], [3.4, -7], [-3.4, 6.5], [3.4, 6.5]]) { box(.8, 5.2, .8, mat(0x3A1E20), x, 2.6, z); box(.9, .2, .9, goldM, x, 4.9, z); box(.9, .2, .9, goldM, x, .1, z); }
  const chand = (x, z) => { const g = new THREE.Group(); g.position.set(x, 4.4, z); SET.vegas.add(g); box(1.6, .08, 1.6, goldM, 0, .3, 0, { parent: g }); for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8, r = k % 2 ? .75 : .5; box(.07, .3 + (k % 3) * .12, .07, glow(0xC9A46E), Math.cos(a) * r, 0, Math.sin(a) * r, { parent: g, cast: false }); } box(.2, .8, .2, goldM, 0, .65, 0, { parent: g }); };
  chand(0, -1); chand(0, -8.5); chand(-6.5, 3); chand(6.5, 3);
  // slot machines along both sides, facing the aisle
  for (const sx of [-1, 1]) for (const row of [0, 1]) for (let k = 0; k < 7; k++) {
    const x = sx * (5.0 + row * 2.4), z = -9 + k * 2.6, ry = sx > 0 ? -Math.PI / 2 : Math.PI / 2, g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry + (row ? Math.PI : 0); SET.vegas.add(g);
    const c = [0x7A1A26, 0x23345E, 0x2A2A2E, 0x5A1A6A][(k + row) % 4], P = { parent: g };
    box(.9, 1.1, .8, gloss(c), 0, .55, 0, P); box(.9, .9, .55, gloss(c), 0, 1.5, -.12, P);
    plane(.7, .55, texMat("slot" + ((k + row * 3 + (sx > 0 ? 1 : 0)) % 4), { transparent: false }), 0, 1.5, .16, 0, g);
    box(.92, .3, .6, glow([0xFF4FA0, 0x4FD8FF, 0xFFC94F, 0x9F6BFF][(k * 3 + row) % 4]), 0, 2.1, -.12, { parent: g, cast: false });
    box(.8, .06, .3, goldM, 0, 1.12, .4, P);
    cyl(.22, .22, .08, mat(0x7A1A26), 0, .7, .8, 14, P); cyl(.05, .05, .65, metal(0x888888), 0, .35, .8, 8, P);
  }
  // the roulette table: wood, felt, padded rail
  const woodM = mat(0x4A2414, { roughness: .5 }), railM = mat(0x2A1612, { roughness: .45 });
  box(2.9, .88, 5.0, woodM, 0, .44, -.55);
  box(2.6, .88, 2.6, woodM, 0, .44, -3.95);
  SET.vegas.feltM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .95 }); LATE.push([SET.vegas.feltM, "felt"]);
  flat(2.6, 4.6, SET.vegas.feltM, 0, .885, -.7);
  box(2.66, .1, 2.6, mat(0x1F5A36), 0, .84, -3.95, { cast: false });
  for (const sx of [-1, 1]) box(.2, .14, 7.4, railM, sx * 1.45, .95, -1.75, { round: .05 });
  box(3.1, .14, .2, railM, 0, .95, 1.95, { round: .05 }); box(3.1, .14, .2, railM, 0, .95, -5.25, { round: .05 });
  // the wheel: bowl, track, the spinning disk with 37 pockets, turret; and the ball
  cyl(1.08, 1.0, .3, woodM, WC.x, .98, WC.z, 48);
  cyl(.98, .98, .02, mat(0xE8DCC4, { roughness: .4 }), WC.x, 1.135, WC.z, 48);
  const disk = new THREE.Group(); disk.position.set(WC.x, 1.15, WC.z); SET.vegas.add(disk); SET.vegas.disk = disk;
  SET.vegas.diskM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .35, metalness: .1 }); LATE.push([SET.vegas.diskM, "wheel"]);
  const dm = new THREE.Mesh(new THREE.CircleGeometry(.8, 74), SET.vegas.diskM); dm.rotation.x = -Math.PI / 2; dm.receiveShadow = true; disk.add(dm);
  for (let i = 0; i < 37; i++) { const a = (i + .5) * Math.PI * 2 / 37, f = new THREE.Mesh(new THREE.BoxGeometry(.012, .035, .12), goldM); f.position.set(Math.cos(a) * .6, .017, -Math.sin(a) * .6); f.rotation.y = a; disk.add(f); }
  const tur = new THREE.Mesh(new THREE.CylinderGeometry(.08, .16, .16, 16), goldM); tur.position.y = .08; disk.add(tur);
  for (let k = 0; k < 4; k++) { const ar = new THREE.Mesh(new THREE.BoxGeometry(.4, .025, .025), goldM); ar.position.y = .15; ar.rotation.y = k * Math.PI / 4; disk.add(ar); }
  const ball = new THREE.Mesh(new THREE.SphereGeometry(.03, 16, 12), new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .15, clearcoat: 1, envMap: ENV })); ball.castShadow = true; SET.vegas.add(ball); SET.vegas.ball = ball;
  // chips: your stack on 17, the stacks you win, a rack in your hand; the board; confetti
  const chipG = new THREE.CylinderGeometry(.075, .075, .03, 18);
  const chipM = [0xE8473A, 0x2F6FDB, 0x1F9A55, 0x1E1B18, 0xF4F1EA, 0x7E3FB8].map((c) => new THREE.MeshStandardMaterial({ color: c, roughness: .5 }));
  const stack = (n, c, parent) => { const g = new THREE.Group(); (parent || SET.vegas).add(g); for (let k = 0; k < n; k++) { const m = new THREE.Mesh(chipG, chipM[(c + (k % 5 === 4 ? 1 : 0)) % 6]); m.position.y = .015 + k * .031; m.rotation.y = k * .7; m.castShadow = true; g.add(m); } return g; };
  SET.vegas.my = stack(6, 0);
  SET.vegas.won = Array.from({ length: 14 }, (_, k) => { const g = stack(8 + (k % 4) * 2, k % 6); g.userData = { x: (k % 7 - 3) * .2, z: -1.85 - Math.floor(k / 7) * .2 }; return g; });
  SET.vegas.boardM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  box(4.4, 1.6, .3, mat(0x1A1012), 0, 3.6, -5.8); box(4.6, .1, .32, goldM, 0, 4.42, -5.8); box(4.6, .1, .32, goldM, 0, 2.78, -5.8);
  plane(4.2, 1.4, SET.vegas.boardM, 0, 3.6, -5.64, 0);
  for (const sx of [-1, 1]) box(.12, 2.8, .12, goldM, sx * 2.1, 1.4, -5.8);
  const cf = new THREE.InstancedMesh(new THREE.PlaneGeometry(.06, .1), new THREE.MeshStandardMaterial({ color: 0xffffff, side: THREE.DoubleSide, emissive: 0x332200, roughness: .4, metalness: .6 }), 260);
  for (let k = 0; k < 260; k++) cf.setColorAt(k, tmpC.set([0xF2C94C, 0xFFE9A0, 0xE8473A, 0xF4F1EA][k % 4]));
  SET.vegas.add(cf); SET.vegas.conf = cf;
  // the dealer and the other players
  SET.vegas.dealer = makeChar({ id: "dealer", skin: "#C68E68", hair: "#1E1B18", style: "short", top: "#1E1B18", topStyle: "blazer", pants: "#1E1B18", shoe: "#1E1B18", glasses: null }, SET.vegas); SET.vegas.dealer.seed = 2.2;
  SET.vegas.alex = makeChar(SP_ALEX, SET.vegas); SET.vegas.alex.seed = 1.3;
  SET.vegas.jay = makeChar(SP_JAY, SET.vegas); SET.vegas.jay.seed = 5.1;
  SET.vegas.players = [[-2.0, -.6, Math.PI / 2], [2.05, -.2, -Math.PI / 2], [-2.0, .7, Math.PI / 2], [2.05, -1.5, -Math.PI / 2]].map(([x, z, ry], k) => { const P = npc(60 + k, SET.vegas); P.u = { x, z, ry }; return P; });
  SET.vegas.crowd = [[-6.2, -5, 0], [6.4, -2, 3.14], [-3.8, 8.2, 2.6], [4.6, 7.8, -2.8], [-7.6, 4, 1.6]].map(([x, z, ry], k) => { const P = npc(70 + k, SET.vegas); P.u = { x, z, ry }; return P; });
}

// ================================================================= s2 MIAMI: a storm, the bridge across the bay
const BR0 = new THREE.Vector3(2, 0, -6), BRY = -.78;         // where the bridge starts, its heading
const brAt = (d) => new THREE.Vector3(BR0.x - Math.sin(BRY) * d, 0, BR0.z - Math.cos(BRY) * d);
const SPAN0 = 38, SPAN1 = 62;
mkSet("miami");
{
  // land, road, plaza, seawall; the water
  box(170, 3, 90, mat(0x6F7A5A), 0, -1.5, 39, { cast: false });
  flat(160, 86, groundMat(SAND, 40, 22), 0, .005, 39);
  flat(9, 80, groundMat(ASPH, 4, 32), 0, .02, 34);
  flat(22, 12, groundMat(ASPH, 9, 5), 4, .021, -.5);
  for (let z = 72; z > -4; z -= 6) box(.14, .02, 2.6, mat(0xF2EEE4), 0, .03, z, { cast: false });
  for (const sx of [-1, 1]) { box(2.6, .15, 76, groundMat(tileTex, 1.3, 38), sx * 5.8, .075, 36, { cast: false, uv: 1 }); box(.2, .17, 76, mat(0x9C978E), sx * 4.55, .085, 36, { cast: false }); }
  box(170, 10, .8, groundMat(CONC, 40, 3), 0, -4.6, -6.2);
  box(470, 9, 130, mat(0x6F7A5A), 30, -4.5, -205, { cast: false });
  const waterTex = pix(64, 64, (g) => { px(g, "#2E4852", 0, 0, 64, 64); for (let k = 0; k < 90; k++) px(g, hash(k) > .5 ? "#4A6670" : "#243C45", Math.floor(hash(k * 3.3) * 64), Math.floor(hash(k * 7.1) * 64), 3 + Math.floor(hash(k * 2) * 6), 1); }, false);
  SET.miami.waterT = rep(waterTex, 60, 60);
  flat(900, 900, new THREE.MeshStandardMaterial({ map: SET.miami.waterT, roughness: .22, metalness: .15, envMap: ENV, envMapIntensity: .5 }), 0, -8, -300);
  // the bridge: deck, railings, lamps, piers; the middle span is two halves that hinge down and fall
  const br = new THREE.Group(); br.position.copy(BR0); br.rotation.y = BRY; SET.miami.add(br); SET.miami.br = br;
  const deckM = groundMat(ASPH, 4, 10), concM = mat(0xB9B4AA), railM = mat(0xD8D4CC);
  const deck = (z0, z1, parent, off = 0) => { const L = z1 - z0, cz = -(z0 + z1) / 2 - off; box(10, .9, L, concM, 0, -.45, cz, { parent }); flat(9.6, L, deckM, 0, .005, cz, parent); for (const sx of [-1, 1]) { box(.3, .9, L, railM, sx * 4.85, .45, cz, { parent }); box(.2, .06, L, mat(0xE9B949), sx * 3.6, .012, cz, { parent, cast: false }); } for (let z = z0 + 6; z < z1; z += 12) { box(.16, 4.5, .16, mat(0x8A8E94), 4.85, 2.7, -z - off, { parent }); box(1.0, .14, .34, mat(0x8A8E94), 4.4, 4.95, -z - off, { parent }); box(.5, .08, .26, glow(0xFFE6B8), 4.15, 4.86, -z - off, { parent, cast: false }); } };
  const trussM = mat(0xD9541E, { roughness: .6 });
  const truss = (L, parent) => { for (const sx of [-4.85, 4.85]) { box(.4, .4, L, trussM, sx, 4.2, -L / 2, { parent }); for (let z = 0; z <= L + .01; z += 3) box(.32, 4.2, .32, trussM, sx, 2.1, -z, { parent }); for (let z = 0; z < L - .01; z += 3) box(.22, 5.1, .22, trussM, sx, 2.1, -z - 1.5, { parent, rx: (Math.floor(z / 3) % 2 ? 1 : -1) * .62 }); } for (let z = 1.5; z < L; z += 3) box(9.7, .3, .3, trussM, 0, 4.2, -z, { parent }); };
  deck(0, SPAN0, br); deck(SPAN1, 196, br);
  for (const z of [12, 25, SPAN0, SPAN1, 75, 88, 101, 114, 127, 140, 153, 166, 179, 192]) box(2.4, 11.5, 3, concM, 0, -6.6, -z, { parent: br });
  SET.miami.halves = [0, 1].map((k) => { const piv = new THREE.Group(); piv.position.set(0, 0, k ? -SPAN1 : -SPAN0); br.add(piv); const half = (SPAN1 - SPAN0) / 2; const g = new THREE.Group(); piv.add(g); deck(0, half, g, 0); truss(half, g); g.rotation.y = k ? Math.PI : 0; return piv; });
  // the far shore skyline (art deco low-rise and towers), in the storm haze
  for (let k = 0; k < 26; k++) { const d = 160 + hash(k * 3.7) * 60, a = -.3 + hash(k * 1.3) * 1.2, x = Math.sin(a) * d * 1.2 - 20, z = -Math.cos(a) * d - 40, h = 14 + hash(k * 5.5) * 80, w = 10 + hash(k * 2) * 12; tower({ x0: x + w / 2, z0: z + w / 2, len: w, h, depth: w, style: ["glass", "white", "grey", "peach"][k % 4], side: -1 }); }
  // the near side: pastel art deco along the road, palms
  let z = 70, k = 0;
  for (const side of [1, -1]) { z = 72; k = side > 0 ? 0 : 20; while (z > 6) { const len = 8 + hash(k * 2.1) * 6, h = 9 + hash(k * 3.3) * 8; tower({ x0: side * 12, z0: z, len, h, style: ["pink", "mint", "peach", "white", "mint"][Math.floor(hash(k * 4.4) * 5)], side, store: k % STORE.length }); z -= len + 1.5; k++; } }
  SET.miami.palms = [];
  const palm = (x, zz, s, lean) => { const g = new THREE.Group(); g.position.set(x, 0, zz); g.scale.setScalar(s); SET.miami.add(g); const P = { parent: g }; for (let j = 0; j < 12; j++) box(.36, .5, .36, j % 2 ? 0xA9825C : 0x94704C, Math.sin(j * .25) * lean * j * .5, .25 + j * .5, 0, P); const top = new THREE.Group(); top.position.set(Math.sin(3) * lean * 6, 6.1, 0); g.add(top); for (let f = 0; f < 8; f++) { const fr = new THREE.Group(); fr.rotation.y = f * Math.PI / 4; top.add(fr); for (let j = 0; j < 5; j++) box(.5, .1, .4, j % 2 ? 0x4E7A3E : 0x5E8C48, 0, -j * j * .07, .35 + j * .45, { parent: fr }); } box(.5, .4, .5, 0x5E8C48, 0, .1, 0, { parent: top }); SET.miami.palms.push({ g, top, ph: hash(x + zz) * 6 }); };
  for (let zz = 2; zz < 70; zz += 7.5) { palm(8.2, zz + hash(zz) * 2, 1, .1); palm(-8.2, zz + 3.5, 1.05, -.1); }
  for (let xx = -40; xx < 60; xx += 9) if (Math.abs(xx - 4) > 9) palm(xx, -4.6, .95, .08);
  // the queue of cars behind you, with their drivers; people on the sidewalk; your cones
  SET.miami.cars = []; SET.miami.drivers = [];
  [[-2.1, 11], [2.1, 10.2], [-2.1, 17.6], [2.1, 17], [-2.1, 24.2], [2.1, 23.8], [-2.1, 31], [2.1, 30.4]].forEach(([x, zz], k) => {
    const g = car(CARCOL[(k * 3 + 1) % CARCOL.length], { taxi: false }); g.position.set(x, 0, zz); SET.miami.cars.push(g);
    if (k < 6) { const P = k === 0 ? makeChar(SP_DRIVER, g) : npc(80 + k, g); P.root.scale.setScalar(.9); P.u = { k }; SET.miami.drivers.push(P); }
  });
  SET.miami.alex = makeChar(SP_ALEX, SET.miami); SET.miami.alex.seed = 1.3;
  SET.miami.peds = [[5.6, 8.6, -2.6], [6.4, 12.4, -2.9], [-5.8, 9.5, 2.7]].map(([x, zz, ry], k) => { const P = npc(90 + k, SET.miami); P.u = { x, z: zz, ry }; return P; });
  for (let j = 0; j < 6; j++) { const c = new THREE.Group(); c.position.set(-3.4 + j * 1.36, 0, 4.2); SET.miami.add(c); box(.5, .06, .5, mat(0x1E1B18), 0, .03, 0, { parent: c }); const cone = new THREE.Mesh(new THREE.ConeGeometry(.22, .8, 12), mat(0xF26B1D)); cone.position.y = .45; cone.castShadow = true; c.add(cone); box(.3, .1, .3, mat(0xF4F1EA), 0, .5, 0, { parent: c }); }
  // rain, a lightning bolt, the splash
  SET.miami.rain = new THREE.InstancedMesh(new THREE.BoxGeometry(.012, .55, .012), new THREE.MeshBasicMaterial({ color: 0xC8D8E8, transparent: true, opacity: .42, depthWrite: false }), 2400);
  SET.miami.rain.frustumCulled = false; SET.miami.add(SET.miami.rain);
  const bolt = new THREE.Group(); SET.miami.add(bolt); SET.miami.bolt = bolt;
  let p = new THREE.Vector3(0, 60, 0); for (let j = 0; j < 9; j++) { const q = p.clone().add(new THREE.Vector3((hash(j * 3.1) - .5) * 9, -7, (hash(j * 1.7) - .5) * 3)); const m = new THREE.Mesh(new THREE.BoxGeometry(.5, p.distanceTo(q), .5), glow(0xE8F0FF)); m.position.copy(p).add(q).multiplyScalar(.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), q.clone().sub(p).normalize()); bolt.add(m); p = q; }
  SET.miami.splash = new THREE.InstancedMesh(BOXG, new THREE.MeshStandardMaterial({ color: 0xF4FAFC, emissive: 0x3A4650, roughness: .6, transparent: true, opacity: .85 }), 180);
  SET.miami.splash.frustumCulled = false; SET.miami.add(SET.miami.splash);
}

// ================================================================= s3/s4 HOME: your apartment, the front door
mkSet("apt");
{
  const plank = pix(64, 64, (g) => { for (let k = 0; k < 8; k++) { px(g, k % 2 ? "#8A6446" : "#7E5A3E", 0, k * 8, 64, 8); px(g, "#6A4A32", (k * 23) % 64, k * 8, 1, 8); px(g, "#5E422C", 0, k * 8 + 7, 64, 1); } });
  flat(6.4, 7, groundMat(plank, 3.2, 3.5, { roughness: .6 }), 0, 0, .25);
  const wallM = mat(0xC9CED6), trim = mat(0xF1EEE6);
  box(6.4, .2, 7, mat(0xD6D9DE), 0, 3.3, .25, { cast: false });
  // the door wall (z -3), with the doorway
  box(2.55, 3.2, .2, wallM, -1.88, 1.6, -3.1); box(2.55, 3.2, .2, wallM, 1.88, 1.6, -3.1); box(1.2, .8, .2, wallM, 0, 2.8, -3.1);
  box(.1, 2.42, .26, trim, -.62, 1.21, -3.06); box(.1, 2.42, .26, trim, .62, 1.21, -3.06); box(1.34, .1, .26, trim, 0, 2.43, -3.06);
  const door = new THREE.Group(); door.position.set(-.56, 0, -3.02); SET.apt.add(door); SET.apt.door = door;
  const dm = mat(0x5A4A3E, { roughness: .6 }), P = { parent: door };
  box(1.12, 2.36, .06, dm, .56, 1.2, 0, P);
  for (const y of [.62, 1.72]) { box(.86, .8, .012, mat(0x4E4034, { roughness: .6 }), .56, y, .036, P); }
  const lever = new THREE.Group(); lever.position.set(1.0, 1.05, .05); door.add(lever); SET.apt.lever = lever;
  cyl(.035, .035, .04, goldM, 0, 0, 0, 14, { parent: lever }).rotation.x = Math.PI / 2;
  box(.17, .032, .036, goldM, -.08, 0, .035, { parent: lever });
  box(.06, .12, .02, goldM, 1.0, 1.26, .04, P);
  box(.035, .035, .02, mat(0x111111), .56, 1.62, .04, P);
  for (let k = 0; k < 5; k++) box(.03, .02, .02, goldM, 1.0 - k * .05, 1.38 - (k % 2) * .015, .045, P);   // the chain
  // light under the door, and the shadow of feet when someone is there
  box(1.1, .02, .04, glow(0xFFC98A), 0, .012, -3.05, { cast: false });
  SET.apt.spill = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending }); LATE.push([SET.apt.spill, "spill"]);
  flat(1.3, .9, SET.apt.spill, 0, .004, -2.6);
  SET.apt.feet = [-.2, .2].map((x) => box(.22, .022, .06, mat(0x050505), x, .013, -3.02, { cast: false }));
  SET.apt.feetS = [-.2, .2].map((x) => { const m = flat(.24, .85, new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: .85, depthWrite: false }), x, .006, -2.62); return m; });
  // side walls; the window on the left (x -3.2) looking out on the city at night
  box(.2, 3.2, 2.4, wallM, -3.2, 1.6, -1.95); box(.2, 3.2, 2.9, wallM, -3.2, 1.6, 2.3); box(.2, .8, 1.7, wallM, -3.2, .4, .0); box(.2, .9, 1.7, wallM, -3.2, 2.75, .0);
  box(.2, 3.2, 7, wallM, 3.2, 1.6, .25); box(6.4, 3.2, .2, wallM, 0, 1.6, 3.8);
  for (const zz of [-.85, .85]) box(.22, 1.5, .08, trim, -3.18, 1.55, zz); box(.22, .08, 1.78, trim, -3.18, 2.3, 0); box(.3, .08, 1.9, trim, -3.12, .8, 0); box(.12, 1.5, .05, trim, -3.18, 1.55, 0);
  plane(26, 16, texMat("nightCity", { transparent: false }), -9, 2.5, 0, Math.PI / 2);
  // furniture: couch, table, floor lamp, shelf, plant, rug, coat hooks, the wall clock
  const couchM = mat(0x3E5A7A);
  box(1.0, .45, 2.4, couchM, 2.6, .35, .3); box(.3, .6, 2.4, couchM, 2.95, .85, .3); for (const zz of [-.95, 1.55]) box(.9, .35, .25, couchM, 2.6, .65, zz);
  box(.8, .08, 1.3, mat(0x7E5A3E), 1.5, .45, .3); for (const [dx, dz] of [[-.35, -.6], [.35, -.6], [-.35, .6], [.35, .6]]) box(.05, .42, .05, mat(0x3A2A1E), 1.5 + dx, .21, .3 + dz);
  box(2.4, .015, 3.0, mat(0xB86A4A), .6, .008, .5, { cast: false });
  cyl(.03, .03, 1.6, mat(INK), 2.65, .8, -2.3, 8); cyl(.18, .24, .3, mat(0xF4E6C8, { emissive: 0xFFC98A, emissiveIntensity: 0 }), 2.65, 1.7, -2.3, 16); SET.apt.shade = SET.apt.children[SET.apt.children.length - 1];
  box(.4, 2.0, 1.4, mat(0x6A4A32), -2.9, 1.0, 2.6); for (let k = 0; k < 4; k++) for (let j = 0; j < 6; j++) box(.25, .3, .08, mat(["#D9483B", "#3A6FC4", "#3FA372", "#F2B33D"][(k + j) % 4]), -2.85, .35 + k * .48, 2.05 + j * .2);
  box(.4, .4, .4, mat(0xC9644E), 2.6, .2, 2.9); for (let j = 0; j < 5; j++) box(.35, .35, .35, mat(j % 2 ? 0x4E7A3E : 0x5E8C48), 2.6 + (hash(j) - .5) * .3, .6 + j * .25, 2.9 + (hash(j * 2) - .5) * .3);
  for (const zz of [-2.6, -2.3]) box(.06, .06, .14, goldM, -3.06, 1.8, zz); box(.5, .9, .2, mat(0x7A2E2E), -2.98, 1.4, -2.45);
  box(.8, .02, .5, mat(0x4A4A4A), 0, .01, -2.55, { cast: false });
  SET.apt.alex = makeChar(SP_ALEX, SET.apt); SET.apt.alex.seed = 1.3;
  SET.apt.clockM = texMat("clock"); const ck = new THREE.Mesh(new THREE.CircleGeometry(.24, 32), SET.apt.clockM); ck.position.set(0, 2.85, -2.99); SET.apt.add(ck);
}

// ================================================================= s5/s6 a ROOFTOP over the city: the real part and the end
mkSet("roof");
{
  flat(22, 22, groundMat(GRAVEL, 8, 8), 0, 0, 0);
  box(22, 40, 22, mat(0xA9A39A), 0, -20.05, 0, { cast: false });
  const pm = mat(0xB9B4AA);
  for (const sx of [-1, 1]) { box(.4, 1.1, 22, pm, sx * 11, .55, 0); box(22, 1.1, .4, pm, 0, .55, sx * 11); }
  box(.6, .12, 22.4, mat(0xCFC9BE), 0, 1.16, -11);
  for (const dx of [-.9, .9]) for (const dz of [-.9, .9]) box(.16, 2.6, .16, mat(0x3A3330), -6 + dx, 1.3, 6 + dz);
  cyl(1.4, 1.4, 2.8, mat(0x8A6A4A), -6, 4.0, 6, 16); const cone = new THREE.Mesh(new THREE.ConeGeometry(1.5, 1.1, 16), mat(0x5A4434)); cone.position.set(-6, 5.95, 6); add(cone);
  box(1.8, 1.1, 1.2, mat(0xC9C3B9), 5, .55, 5); box(1.8, 1.1, 1.2, mat(0xC9C3B9), 7.2, .55, 5); box(3, 2.8, 2.6, mat(0xB0A89C), 6, 1.4, 8.6);
  box(.08, 6, .08, mat(0x777777), 8.5, 3, -8); box(.6, .04, .04, mat(0x777777), 8.5, 5.2, -8);
  // the city all around: instanced towers with a window mask
  const blockTex = pix(32, 64, (g) => { px(g, "#FFFFFF", 0, 0, 32, 64); for (let i = 0; i < 3; i++) for (let j = 0; j < 7; j++) px(g, "#9DB6CC", 3 + i * 10, 3 + j * 9, 6, 6); });
  const blockLit = pix(32, 64, (g) => { px(g, "#000", 0, 0, 32, 64); for (let i = 0; i < 3; i++) for (let j = 0; j < 7; j++) if (hash(i * 7 + j * 3) > .4) px(g, "#FFD9A0", 3 + i * 10, 3 + j * 9, 6, 6); });
  const cityMat = new THREE.MeshStandardMaterial({ map: rep(blockTex, 1, 3), emissiveMap: rep(blockLit, 1, 3), emissive: 0xFFD9A0, emissiveIntensity: 0, roughness: .8 }); NIGHTM.push([cityMat, 1.2]);
  const G = [];
  for (let gx = -16; gx <= 16; gx++) for (let gz = -22; gz <= 10; gz++) { const x = gx * 15, z = gz * 15, r = Math.hypot(x, z); if (r < 20 || r > 330) continue; G.push({ x: x + (hash(gx * 3 + gz) - .5) * 4, z: z + (hash(gx + gz * 7) - .5) * 4, w: 8 + hash(gx * 7 + gz * 3) * 4, d: 8 + hash(gx + gz * 11) * 4, h: (r < 90 ? 12 + hash(gx * 13 + gz * 17) * 26 : 30 + hash(gx * 13 + gz * 17) * 60) + (r < 160 ? 0 : 30 * hash(gx * gz)), c: ["#D9DEE4", "#C9B79A", "#B8A08A", "#E6E1D6", "#A7ABB0", "#9C4A3A", "#7FA4C2"][(gx * 3 + gz * 5 + 99) % 7] }); }
  const city = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1).translate(0, .5, 0), cityMat, G.length);
  G.forEach((b, i) => { M4.compose(V.set(b.x, -42, b.z), Q.identity(), S.set(b.w, b.h, b.d)); city.setMatrixAt(i, M4); city.setColorAt(i, tmpC.set(b.c)); });
  city.castShadow = true; city.receiveShadow = true; SET.roof.add(city);
  flat(900, 900, mat(0x5A5E64), 0, -42, -100);
  // the AI weather model: a holographic globe with storms on it, a grid, a ring, and the ten-day cards
  const globe = new THREE.Group(); globe.position.set(6, 24, -70); SET.roof.add(globe); SET.roof.globe = globe;
  SET.roof.earthM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .92, toneMapped: false }); LATE.push([SET.roof.earthM, "earth"]);
  globe.add(new THREE.Mesh(new THREE.SphereGeometry(15, 64, 40), SET.roof.earthM));
  SET.roof.cloudM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .85, toneMapped: false, depthWrite: false }); LATE.push([SET.roof.cloudM, "clouds"]);
  const cl = new THREE.Mesh(new THREE.SphereGeometry(15.4, 64, 40), SET.roof.cloudM); globe.add(cl); SET.roof.cloud = cl;
  globe.add(new THREE.Mesh(new THREE.SphereGeometry(15.9, 24, 16), new THREE.MeshBasicMaterial({ color: 0x8FE6FF, wireframe: true, transparent: true, opacity: .16, toneMapped: false, depthWrite: false })));
  const ring = new THREE.Mesh(new THREE.TorusGeometry(21, .12, 6, 120), glow(0x8FE6FF)); ring.rotation.x = 1.25; globe.add(ring); SET.roof.ring = ring;
  SET.roof.cards = Array.from({ length: 10 }, (_, k) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(5.2, 7), texMat("day" + k, { depthWrite: false, depthTest: false })); m.renderOrder = 10; SET.roof.add(m); return m; });
}
PARENT = scene;

// ---------------------------------------------------------------- looks per scene (0 NY morning, 1 casino, 2 storm, 3 night, 4 dawn, 5 NY night)
const LOOKS = [
  { set: "ny", sky: "ny", fog: 0xE6D6C0, fn: 70, ff: 340, hs: 0xEAF0FF, hg: 0xC9B79A, hi: 1.0, sun: 0xFFE0B4, si: 2.8, sd: [-.5, .62, .6], ext: 46, warm: .3, cool: 0, sat: 1.06, con: .08, vig: .38, night: 0 },
  { set: "vegas", sky: null, bg: 0x0E0809, fog: 0x140A0C, fn: 16, ff: 46, hs: 0xFFD9B0, hg: 0x3A1A12, hi: .5, sun: 0xFFE6C4, si: 1.1, sd: [.25, 1, .35], ext: 12, warm: .22, cool: 0, sat: 1.12, con: .12, vig: .55, night: 0 },
  { set: "miami", sky: "storm", fog: 0x68717A, fn: 50, ff: 320, hs: 0xB4C0CE, hg: 0x4A5058, hi: 1.3, sun: 0xD0DAE6, si: 1.3, sd: [.3, .8, .5], ext: 60, warm: 0, cool: .5, sat: .74, con: .12, vig: .5, night: 0 },
  { set: "apt", sky: null, bg: 0x05070C, fog: 0x0A0E18, fn: 40, ff: 120, hs: 0x5468A0, hg: 0x1A1A24, hi: .42, sun: 0x9FB8FF, si: 1.0, sd: [-1, .55, .25], ext: 7, warm: 0, cool: .45, sat: .86, con: .12, vig: .6, night: 0 },
  { set: "apt", sky: null, bg: 0x0A0C12, fog: 0x0A0E18, fn: 40, ff: 120, hs: 0x7486A8, hg: 0x2A2A33, hi: .5, sun: 0xBCCBEA, si: .9, sd: [-1, .4, .1], ext: 7, warm: 0, cool: .3, sat: .78, con: .1, vig: .55, night: 0 },
  { set: "ny", sky: "nynight", fog: 0x1A2240, fn: 60, ff: 300, hs: 0x3A4C80, hg: 0x1A1A24, hi: .42, sun: 0x9FB0E0, si: .45, sd: [-.5, .7, .6], ext: 46, warm: .1, cool: .15, sat: 1.0, con: .1, vig: .45, night: 1 },
];
const SKY = {};

// ---------------------------------------------------------------- the shot list: [start, {p0, p1 (camera), l0, l1 (look at), fov, fov1, ap, pov, hp}]
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const tl0 = () => E[5] + 1.6;            // the ball lands
const TR = () => E[1] + 1.35;            // the man lets go of the cup
const TC = () => E[10] + .6;             // the span starts to fall
const KN = () => [0, .28, .56].map((a) => E[12] + .4 + a);   // three knocks
const SIDE = { p0: v(60, 2.2, -5.4), l0: v(36, -.5, -41), fov: 66, ap: .006 };
const SHOTS = [
  // New York
  [0, { p0: v(2.8, 11, 10), p1: v(4.6, 4.2, 6.5), l0: v(7, 2, -14), l1: v(7, 1.7, -6), fov: 60, ap: .008 }],
  [L[0] - .15, { p0: v(7.0, 1.93, .5), l0: v(7.0, 1.72, -1.0), fov: 70, ap: .22, f: .3, pov: 1 }],
  [L[0] + 3.2, { p0: v(6.6, 1.95, -1.6), p1: v(6.8, 1.9, -1.4), l0: v(7.0, 1.72, .5), fov: 40, ap: .2, d: 2.6, d1: 2.2 }],
  [E[1] + .2, { p0: v(7.4, 3.9, -4.6), p1: v(7.7, 4.1, -5.6), l0: v(8.55, 5.0, -9.3), fov: 45, ap: .05 }],
  [E[1] + 1.3, { p0: v(7.0, 1.15, -3.1), p1: v(7.1, .95, -3.5), l0: v(7.9, 1.0, -6.1), l1: v(7.95, .6, -6.0), fov: 50, ap: .12 }],
  [L[2] - .1, { p0: v(6.85, 1.95, -.6), l0: v(7.0, 1.86, .5), fov: 36, ap: .3, d: 2.1, d1: 1.75 }],
  // Las Vegas
  [CU[0], { p0: v(.1, 2.3, -.6), p1: v(.15, 2.15, -.2), l0: v(.15, 1.55, 2.25), fov: 44, ap: .08 }],
  [L[4] - .1, { p0: v(-.4, 1.9, 1.45), l0: v(-.25, 1.78, 2.35), fov: 36, ap: .3, d: 2.2, d1: 1.95 }],
  [E[4] + .1, { p0: v(.8, 2.0, -1.1), p1: v(.95, 1.95, -1.4), l0: v(1.9, 1.75, -2.6), fov: 40, ap: .15 }],
  [E[5] + .25, { p0: v(0, 2.6, -2.3), p1: v(0, 2.25, -2.8), l0: v(0, 1.12, -3.95), fov: 42, ap: .1 }],
  [tl0() + .6, { p0: v(0, 2.4, -4.4), p1: v(0, 2.2, -4.0), l0: v(.1, 1.6, 2.2), fov: 50, ap: .02 }],
  [L[6] + .15, { p0: v(.9, 2.0, 1.3), l0: v(.55, 1.8, 2.15), fov: 40, ap: .3, d: 2.6, d1: 2.3 }],
  [E[6] + .1, { p0: v(-.5, 1.55, 1.4), l0: v(-.25, 1.75, 2.35), fov: 36, ap: .3, d: 2.1, d1: 1.9 }],
  // Miami
  [CU[1], { ...SIDE, p1: v(60, 2.2, -5.4), l1: v(34, -.5, -42) }],
  [L[8] + 2.2, { p0: v(.3, 1.93, 6.0), l0: v(-.2, 1.62, 3.0), fov: 70, ap: .22, f: .3, pov: 1 }],
  [E[8] + .25, { p0: v(-4.6, 1.75, 9.4), l0: v(-3.05, 1.68, 11.1), fov: 40, ap: .2, d: 2.4, d1: 2.1 }],
  [E[9] + .1, { p0: v(-.3, 1.6, 8.6), l0: v(.3, 1.85, 6.0), fov: 48, ap: .12, d: 3.6, d1: 3.1 }],
  [E[10] + .3, { ...SIDE, l1: v(36, -2, -41), fov1: 56 }],
  [L[11] - .1, { p0: v(-4.4, 1.7, 9.7), l0: v(-3.05, 1.66, 11.1), fov: 38, ap: .25, d: 2.1, d1: 1.9 }],
  // home, night
  [CU[2], { p0: v(.25, 1.93, 1.0), l0: v(.2, 1.55, -1.0), fov: 70, ap: .25, f: .3, pov: 1 }],
  [E[12] + .15, { p0: v(.25, 1.93, 1.0), p1: v(.25, 1.9, 1.3), l0: v(0, 1.25, -3), fov: 54, fov1: 48, ap: .03, pov: 2 }],
  [L[13] - .1, { p0: v(.55, 1.15, -.1), p1: v(.4, 1.0, -.6), l0: v(0, .55, -3.0), fov: 50, ap: .08 }],
  [E[13] + .2, { p0: v(.25, 1.93, 1.0), l0: v(.2, 1.55, -1.0), fov: 70, ap: .25, f: .3, pov: 1 }],
  [E[13] + 1.3, { p0: v(.78, 1.13, -2.3), p1: v(.7, 1.1, -2.45), l0: v(.44, 1.05, -2.95), fov: 40, ap: .25 }],
  // home, day 30
  [CU[3], { p0: v(1.05, 1.55, .0), l0: v(2.3, 1.3, .3), fov: 40, ap: .25, d: 2.3, d1: 2.0 }],
  [E[14] + .15, { p0: v(2.3, 1.42, .3), l0: v(1.2, 1.12, .3), fov: 70, ap: .25, f: .3, pov: 1 }],
  [E[15] - .3, { p0: v(1.6, 1.45, .2), l0: v(2.3, 1.38, .3), fov: 34, ap: .3, d: 1.9, d1: 1.6 }],
  // the end: New York at night, the crane goes up
  [CU[4], { p0: v(5.4, 3.0, 6.5), p1: v(3.6, 10, 11), l0: v(7, 1.7, -4), l1: v(7, 3, -18), fov: 56, ap: .006 }],
];
function shotAt(t) {
  let i = 0; while (i + 1 < SHOTS.length && t >= SHOTS[i + 1][0]) i++;
  const [a, s] = SHOTS[i], b = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR;
  const u = sm(clamp((t - a) / Math.max(.1, b - a)));
  let p = (s.p1 ? V.lerpVectors(s.p0, s.p1, u) : V.copy(s.p0)).clone(); const l = s.l1 ? V2.lerpVectors(s.l0, s.l1, u).clone() : s.l0.clone();
  if (s.d) { const d = lerp(s.d, s.d1 ?? s.d, u); p = l.clone().add(p.sub(l).normalize().multiplyScalar(d)); }
  return { i, a, b, u, p, l, fov: lerp(s.fov, s.fov1 ?? s.fov, u), ap: s.ap, f: s.f ?? p.distanceTo(l), pov: !!s.pov, hands: s.pov === 1 };
}
const HP_READ = { ...HP.phRead, ...HP.rDown, phone: true, right: false };
const who = (t, name) => C.who.some((w, k) => w === name && t > L[k] - .05 && t < E[k] + .02);
function phoneKey(t, s) {
  if (s === 0 || s === 5) return "phNY";
  if (s === 1) return "phVegas";
  if (s === 2) return "phMiami";
  if (s === 3) return t < E[13] + .2 ? "phMsg" : "phNotJay";
  if (t < L[15] + .3) return "phLoad" + (Math.floor(t * 8) % 4);
  if (t < E[15] - .3) return "phGlitch" + (Math.floor(t * 14) % 3);
  return "phBlack";
}

// ---------------------------------------------------------------- per set, per frame
const wrap = (x, a, b) => a + ((((x - a) % (b - a)) + (b - a)) % (b - a));
const PP = new THREE.Vector3();
let SHAKE = 0;
// Alex holding his phone up at his chest, looking at it (hp = head pitch)
const HOLD = (o = {}) => pose({ a: [[1.15, .12, 1.65], [.35, .1, .5]], hp: .42, ...o });
function holdPhone(P, key, vis = true) {
  APH.visible = vis && P.root.visible; if (!APH.visible) return;
  P.root.updateMatrixWorld(true);
  P.hand[0].getWorldPosition(PP); P.head.getWorldPosition(V2); V2.y += .26;
  APH.position.copy(PP).addScaledVector(V.subVectors(V2, PP).normalize(), .06); APH.position.y += .06;
  APH.lookAt(V2);
  if (TEX[key]) setMap(aphM, TEX[key]);
}
function manPose(t) {
  const tr = TR();
  let p = idle(pose({ x: 8.0, y: .15, z: -6.2, ry: -.5, hy: .28, hp: .06, a: [[.95, .12, 1.4], [.08, .12, .15]] }), t, 4.2);
  if (t > tr) { const u = ss(t, tr, tr + .5); p.a = [[lerp(.95, .45, u), lerp(.12, .35, u), lerp(1.4, .4, u)], p.a[1]]; }
  const u2 = ss(t, tr + .7, tr + 1.4);
  if (u2 > 0) p = mixP(p, { ...p, lean: -.06, hp: .38, hy: .1, a: [[1.1, .55, 2.0], [1.1, .55, 2.0]] }, u2);
  return p;
}
function updNY(t, sh, s) {
  const S0 = SET.ny;
  for (const g of S0.cars) { const u = g.userData, toward = u.lane < 0; const z = toward ? wrap(u.z0 + u.v * t, -238, 12) : wrap(u.z0 - u.v * t, -238, 12); g.position.set(u.lane, 0, z); g.rotation.y = toward ? Math.PI : 0; }
  for (const P of S0.walk) { const u = P.u, z = u.dir < 0 ? wrap(u.z0 - u.v * t, -76, -1.5) : wrap(u.z0 + u.v * t, -76, 4); const near = Math.abs(u.lane - 7) < 2.5 && Math.abs(z - .5) < 1.6; placeChar(P, !near, walk(pose({ x: u.lane, y: .15, z, ry: u.dir < 0 ? Math.PI : 0 }), u.ph + t * u.v * 4.2), { mouth: "smile" }); }
  S0.stand.forEach((P, k) => { const u = P.u; placeChar(P, true, idle(pose({ x: u.x, y: .15, z: u.z, ry: u.ry, a: k === 2 ? [[.9, .1, 1.5], [.05, .1, .1]] : [[.05, .1, .15], [.05, .1, .15]] }), t, k * 2), k < 2 ? { talk: Math.sin(t * 1.3 + k * 3) > 0, mouth: "smile" } : { mouth: "smile" }); });
  // Alex: reading, puzzled, then stunned (hidden in his own POV)
  const A = S0.alex, night = s === 5;
  let ap = HOLD({ x: 7.0, y: .15, z: .5, ry: Math.PI });
  if (!night && t > L[0] + 3.4) ap = mixP(ap, { ...ap, hp: .05, hy: .08 }, ss(t, L[0] + 3.4, L[0] + 4.0));
  if (!night && t > L[2] - .2) ap = { ...ap, hp: -.04, hy: -.12, a: [[.6, .15, .9], [.3, .1, .5]] };
  const af = night ? { mouth: "flat", eyes: "half" } : t > L[2] - .2 ? { eyes: "wide", mouth: "o", brows: "up", talk: who(t, "alex"), noblink: true } : t > L[0] + 3.4 ? { brows: "raise1", mouth: "smirk", talk: who(t, "alex") } : { mouth: "flat", brows: "flat" };
  placeChar(A, !sh.pov, idle(ap, t, 1.3), af);
  holdPhone(A, "phNY", t < L[2] - .2 || night);
  // the man and his coffee, in slow motion
  const M = S0.man, tr = TR(), K = .45;
  applyPose(M, manPose(Math.min(t, tr))); M.root.updateMatrixWorld(true); M.hand[0].getWorldPosition(PP);
  const p0 = PP.clone().add(V.set(0, -.03, 0));
  placeChar(M, !night, manPose(t), t < tr ? { mouth: "smile", eyes: "half" } : { eyes: "wide", mouth: "o", brows: "up", noblink: true });
  const cup = S0.cup, G = 5.75, gy = .15 + .06, ti = Math.sqrt(Math.max(0, p0.y - gy) / G), d = (t - tr) * K;
  const land = V2.set(p0.x + .25 * ti, gy, p0.z - .1 * ti).clone();
  cup.visible = !night;
  if (t < tr) { M.hand[0].getWorldPosition(PP); cup.position.copy(PP).add(V.set(0, .02, .02)); cup.rotation.set(0, 0, 0); }
  else if (d < ti) { cup.position.set(p0.x + .25 * d, p0.y - G * d * d, p0.z - .1 * d); cup.rotation.set(d * 3, 0, -d * 9); }
  else { const e = d - ti; cup.position.set(land.x + .25 * (1 - Math.exp(-e * 3)), gy - .02, land.z); cup.rotation.set(.3, 0, -Math.PI / 2 - (1 - Math.exp(-e * 3)) * 2); }
  const de = d - ti, pu = clamp(de / .35);
  S0.pud.visible = pu > 0 && !night; S0.pud.position.set(land.x + .1, .157, land.z + .05); S0.pud.scale.setScalar(.05 + .85 * sm(pu));
  S0.drops.forEach((m, k) => { m.visible = de > 0 && de < .9 && !night; if (!m.visible) return; const a = hash(k * 3.7) * Math.PI * 2, sp = 1 + hash(k) * 1.4, up = 1.8 + hash(k * 5) * 1.6; const y = Math.max(.16, gy + up * de - G * de * de); m.position.set(land.x + Math.cos(a) * sp * Math.min(de, .5), y, land.z + Math.sin(a) * sp * Math.min(de, .5)); m.scale.setScalar((.04 + hash(k) * .03) * (y <= .16 ? .6 : 1)); });
  if (TEX.led914) setMap(S0.ledM, t > E[1] + .85 ? TEX.led914 : TEX.led913);
  if (night) { [[5.6, 6.2, 6], [5.6, 6.2, -10], [-5.6, 6.2, -2], [-5.6, 6.2, -18]].forEach(([x, y, z], k) => { PL[k].position.set(x - Math.sign(x) * 1.4, y - .3, z); PL[k].color.set(0xFFD9A0); PL[k].intensity = 9; PL[k].distance = 14; }); }
}
function updVegas(t, sh) {
  const S1 = SET.vegas, t0 = CU[0], tl = tl0();
  const th = 3.0 * (t - t0) + 1.0; S1.disk.rotation.y = th;
  const aWin = WINI * Math.PI * 2 / 37;
  let rel = aWin, r = .66, y = 1.18;
  if (t < tl) { const dd = tl - t; rel = aWin + 7.5 * dd + 2.2 * dd * dd; r = lerp(.9, .66, ss(t, tl - 1.4, tl)); y = lerp(1.17, 1.18, ss(t, tl - 1.4, tl)); }
  if (t > tl - .6 && t < tl + .2) y += .035 * Math.abs(Math.sin((t - tl + .6) * 15)) * (1 - ramp(t, tl - .6, tl + .2));
  const psi = th + rel; S1.ball.position.set(WC.x + Math.cos(psi) * r, y, WC.z - Math.sin(psi) * r);
  S1.my.position.set(cellX(WIN), .9, cellZ(WIN));
  S1.won.forEach((g, k) => { const a = tl + .55 + k * .04, u = ss(t, a, a + .7); g.visible = t > a; g.position.set(lerp(-.2 + k * .03, g.userData.x, u), .9, lerp(-3.0, g.userData.z, u)); });
  const amt = t < tl + .3 ? 0 : 2e6 * ss(t, tl + .35, L[6] + .6);
  drawBoard(t < tl ? 0 : 1, Math.round(amt / 1000) * 1000, t > tl && Math.floor(t * 5) % 2 === 0);
  const cfT = t - tl - .35; S1.conf.visible = cfT > 0;
  if (cfT > 0) for (let k = 0; k < 260; k++) { const yy = Math.max(.02, 5.3 + hash(k * 2.1) * 2.5 - cfT * (1.2 + hash(k) * .6)); EU.set(cfT * (3 + hash(k * 5) * 4) + k, k, cfT * 2 + k * .3); Q.setFromEuler(EU); M4.compose(V.set((hash(k * 1.7) - .5) * 7 + .25 * Math.sin(cfT * 3 + k), yy, -5 + hash(k * 3.3) * 8), Q, S.set(1, 1, 1)); S1.conf.setMatrixAt(k, M4); }
  S1.conf.instanceMatrix.needsUpdate = true;
  const win = t > tl;
  // Alex: calm, phone in hand; Jay: panicking, then cheering
  const A = S1.alex, J = S1.jay;
  let ap = HOLD({ x: -.25, z: 2.35, ry: Math.PI, hp: .1 });
  if (t > E[6]) ap = { ...ap, hp: .35, hy: .15 };
  placeChar(A, true, idle(ap, t, 1.3), t > E[6] ? { mouth: "smirk", brows: "flat", talk: who(t, "alex"), eyes: "half" } : win ? { mouth: "smile" } : { mouth: "smirk", brows: "flat", talk: who(t, "alex") });
  holdPhone(A, "phVegas");
  let jp = idle(pose({ x: .55, z: 2.15, ry: Math.PI + .45, a: [[.9, .85, .7], [.9, .85, .7]], hy: .35 }), t, 5.1);
  if (t < L[3] + .1 || (t > E[3] + .3 && !win)) jp = { ...jp, a: [[.5, .2, 1.4], [.5, .2, 1.4]], hy: .1 };
  const c = win ? ss(t, tl + .05, tl + .35) : 0;
  if (c > 0) jp = mixP(jp, { ...jp, y: .08 * Math.abs(Math.sin(t * 8)), a: [[2.9, .35, .25], [2.9, .35, .25]], hp: -.2, hy: .2 }, c);
  placeChar(J, true, jp, win ? { mouth: "laugh", eyes: c > .5 && !who(t, "jay") ? "happy" : "wide", talk: who(t, "jay") } : { mouth: "o", brows: "worry", eyes: "wide", talk: who(t, "jay") });
  placeChar(S1.dealer, true, idle(pose({ x: 1.9, z: -2.6, ry: -.95, a: who(t, "dealer") ? [[1.2, .2, .3], [.5, .1, .9]] : win ? [[1.2, .2, .3], [.3, .1, .6]] : [[.5, .1, .9], [.5, .1, .9]] }), t, 2), { mouth: win ? "grin" : "smile", talk: who(t, "dealer") });
  S1.players.forEach((P, k) => { const u = P.u, cc = win ? ss(t, tl + .1 + k * .08, tl + .4 + k * .08) : 0; let p = idle(pose({ x: u.x, z: u.z, ry: u.ry, a: [[.6, .1, 1.0], [.6, .1, 1.0]] }), t, k * 3); if (cc > 0) p = mixP(p, { ...p, y: .06 * Math.abs(Math.sin(t * 7 + k)), a: [[2.9, .3, .25], [2.9, .3, .25]], hp: -.15 }, cc); placeChar(P, true, p, cc > .5 ? { mouth: "laugh", eyes: "happy" } : { mouth: "smile", eyes: "open" }); });
  S1.crowd.forEach((P, k) => { const u = P.u; placeChar(P, true, idle(pose({ x: u.x, z: u.z, ry: u.ry, a: [[.7, .1, 1.2], [.2, .1, .3]] }), t, k), { mouth: "smile" }); });
  [[0, 3.3, -.4, 0xFFD9A0, 7, 9], [0, 3.0, -3.95, 0xFFD9A0, 2.5, 7], [-5.6, 2.2, 0, 0xFF4FA0, 4, 8], [5.6, 2.2, 0, 0x4FD8FF, 4, 8], [0, 2.4, 10.4, 0xFF5FD0, 6, 9], [0, 4.0, -8.5, 0xFFE2B0, 5, 9], [0, 2.6, 3.4, 0xFFD9A0, 3.5, 5]].forEach(([x, yy, z, cl, i, dd], k) => { PL[k].position.set(x, yy, z); PL[k].color.set(cl); PL[k].intensity = i; PL[k].distance = dd; });
}
const FL = () => [CU[1] + .5, L[8] + 1.6, E[9] - .2, TC() + .55];
const BOLTP = [[-20, -140], [90, -160], [-30, 150], [0, -150]];
function flashAt(t) { let f = 0, idx = -1, best = 0; FL().forEach((a, k) => { const vv = pulse(t, a, .05) + .6 * pulse(t, a + .17, .04); f += vv; if (vv > best) { best = vv; idx = k; } }); return { f: clamp(f), idx }; }
function updMiami(t, cam, sh) {
  const S2 = SET.miami;
  S2.waterT.offset.set(t * .02, t * .045);
  for (const p of S2.palms) { p.top.rotation.z = .14 * Math.sin(t * 2.2 + p.ph) + .1; p.top.rotation.x = .08 * Math.sin(t * 1.7 + p.ph); p.g.rotation.z = .03 * Math.sin(t * 1.1 + p.ph); }
  const R = S2.rain;
  for (let k = 0; k < 2400; k++) { const top = cam.y + 9, yy = top - wrap(t * 15 + hash(k * 1.3) * 18, 0, 18); let dx = (hash(k * 2.7) - .5) * 26, dz = (hash(k * 5.1) - .5) * 26; if (Math.abs(dx) < 2.2 && Math.abs(dz) < 2.2) dx += (dx < 0 ? -2.2 : 2.2); M4.makeRotationZ(.12); M4.setPosition(cam.x + dx + (yy - top) * .12, yy, cam.z + dz); R.setMatrixAt(k, M4); }
  R.instanceMatrix.needsUpdate = true;
  const fl = flashAt(t); S2.bolt.visible = fl.f > .25; if (fl.idx >= 0) { const [bx, bz] = BOLTP[fl.idx]; S2.bolt.position.set(bx, -6, bz); }
  const tc = TC(), u = clamp((t - tc) / .95), ph = 1.3 * u * u, drop = 14 * ss(t, tc + .6, tc + 1.8);
  S2.halves[0].rotation.x = -ph; S2.halves[1].rotation.x = ph;
  for (const h of S2.halves) h.position.y = -drop;
  const ti = tc + .72, dt0 = t - ti, perp = V.set(Math.cos(BRY), 0, -Math.sin(BRY));
  S2.splash.visible = dt0 > 0 && dt0 < 2.6;
  if (S2.splash.visible) for (let j = 0; j < 180; j++) { const h1 = hash(j * 1.7), h2 = hash(j * 3.1), h3 = hash(j * 5.3), d = dt0 - (j % 3) * .07; const b = brAt(SPAN0 + h1 * (SPAN1 - SPAN0)); const vy = 7 + h2 * 13, yy = -8 + vy * d - 9 * d * d, lat = (h3 - .5) * 9 + (h3 - .5) * 5 * d; const sc = d < 0 || yy < -8.6 ? 0 : (.18 + h2 * .55) * (1 - ramp(d, 1.5, 2.5)); M4.compose(V2.set(b.x + perp.x * lat, yy, b.z + perp.z * lat), Q.identity(), S.setScalar(sc)); S2.splash.setMatrixAt(j, M4); }
  S2.splash.instanceMatrix.needsUpdate = true;
  SHAKE = Math.max(SHAKE, .5 * pulse(t, ti + .1, .35));
  // the drivers get angry when Alex blocks the road; the first one yells, then goes quiet
  const angry = ss(t, E[8] - .2, E[8] + .3), after = t > L[11] - .3;
  S2.drivers.forEach((P, k) => { let p = pose({ x: -.5, y: .02, z: .25, ry: Math.PI, l: [[1.45, 1.5], [1.45, 1.5]], a: [[.8, .1, .9], [.8, .1, .9]] }); if (angry > 0 && !after) p = mixP(p, { ...p, x: -1.0, tw: .3, hy: .55, a: [[.8, .1, .9], [.5, 1.45 + .25 * Math.sin(t * 9 + k), 1.0 + .5 * Math.sin(t * 9 + k)]] }, angry); if (after) p = { ...p, x: -1.0, tw: .3, hy: .6, hp: -.05 }; const yell = k === 0 ? who(t, "driver") : angry > .5 && !after && Math.sin(t * 3 + k) > 0; placeChar(P, true, p, after ? { eyes: "wide", mouth: "o", brows: "worry", talk: k === 0 && who(t, "driver"), noblink: true } : angry > .5 ? { brows: "angry", mouth: "talk", talk: yell, eyes: "open" } : { brows: "flat", mouth: "flat" }); });
  S2.peds.forEach((P, k) => { const u2 = P.u; let p = idle(pose({ x: u2.x, y: .15, z: u2.z, ry: u2.ry }), t, k * 2); if (angry > 0 && !after) p = mixP(p, { ...p, a: [[2.3 + .3 * Math.sin(t * 8 + k), .45, 1.0], [.7, .2, 1.7]] }, angry); placeChar(P, true, p, after ? { eyes: "wide", mouth: "o" } : angry > .5 ? { brows: "angry", talk: true, mouth: "talk" } : { mouth: "flat" }); });
  // Alex in the road, arms up, shouting
  const A = S2.alex, up = ss(t, E[9] - .1, E[9] + .25);
  let ap = pose({ x: .3, z: 6.0, ry: 0, a: [[.3, .15, .3], [.3, .15, .3]] });
  if (up > 0) ap = mixP(ap, { ...ap, a: [[2.5 + .15 * Math.sin(t * 6), .5, .35], [2.5 + .15 * Math.sin(t * 6 + 1), .5, .35]], lean: .08 }, up);
  if (t > E[10] + .3) ap = { ...ap, ry: Math.PI, a: [[.3, .15, .3], [.3, .15, .3]] };
  placeChar(A, !sh.pov, ap, up > 0 ? { brows: "worry", eyes: "wide", mouth: "talk", talk: who(t, "alex"), noblink: true } : { mouth: "flat", brows: "worry" });
  APH.visible = false;
  return fl.f;
}
function updApt(t, s, sh) {
  const S3 = SET.apt, night = s === 3;
  PL[0].position.set(2.65, 1.6, -2.3); PL[0].color.set(0xFFC98A); PL[0].intensity = night ? 2.4 : 0; PL[0].distance = 7;
  PL[1].position.set(0, .2, -2.75); PL[1].color.set(0xFFC98A); PL[1].intensity = 1.0; PL[1].distance = 2.6;
  S3.shade.material.emissiveIntensity = night ? 1.1 : 0;
  const feet = night && t > KN()[0] - .5;
  for (const m of S3.feet) m.visible = feet; for (const m of S3.feetS) m.visible = feet;
  let k = 0; if (night) for (const a of KN()) k += pulse(t, a, .045);
  S3.door.rotation.y = -.01 * k; S3.door.position.z = -3.02 + .006 * k;
  SHAKE = Math.max(SHAKE, .12 * k);
  S3.lever.rotation.z = night ? -.7 * ss(t, E[13] + 1.5, CU[3] - .1) : 0;
  const A = S3.alex;
  if (night) {
    let ap = HOLD({ x: .25, z: 1.0, ry: Math.PI });
    const back = ss(t, KN()[0], KN()[0] + .5);
    ap = mixP(ap, { ...ap, z: 1.25, hp: 0, lean: -.05 }, back);
    placeChar(A, !sh.pov, idle(ap, t, 1.3), back > .5 ? { eyes: "wide", mouth: "o", brows: "worry", noblink: true } : { eyes: "open", mouth: "flat", brows: "worry", talk: who(t, "alex") });
    holdPhone(A, t < E[13] + .2 ? "phMsg" : "phNotJay");
  } else {
    // day 30: sitting on the couch edge with the phone
    const ap = pose({ x: 2.35, y: -.145, z: .3, ry: -Math.PI / 2, l: [[1.5, 1.5], [1.5, 1.5]], a: [[1.25, .12, 1.7], [1.0, .15, 1.5]], hp: .4 });
    const dead = t > E[15] - .3;
    placeChar(A, !sh.pov, idle(ap, t, 1.3), dead ? { eyes: "wide", mouth: "o", brows: "worry", noblink: true } : { eyes: "half", mouth: "flat", brows: "worry", talk: who(t, "alex") });
    holdPhone(A, phoneKey(t, 4));
  }
}

// ---------------------------------------------------------------- the frame
function renderAt(t) {
  NOW = t; SHAKE = 0;
  const s = sceneOf(t), Lk = LOOKS[s];
  for (const k in SET) SET[k].visible = k === Lk.set;
  scene.background = Lk.sky ? SKY[Lk.sky] : tmpC.set(Lk.bg).clone();
  scene.fog.color.set(Lk.fog); scene.fog.near = Lk.fn; scene.fog.far = Lk.ff;
  hemi.color.set(Lk.hs); hemi.groundColor.set(Lk.hg); hemi.intensity = Lk.hi;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  for (const [m, k] of NIGHTM) m.emissiveIntensity = Lk.night * k;
  for (const l of PL) l.intensity = 0;
  APH.visible = false;
  const sh = shotAt(t);
  let flash = 0;
  if (s === 0 || s === 5) updNY(t, sh, s);
  else if (s === 1) updVegas(t, sh);
  else if (s === 2) { flash = updMiami(t, sh.p, sh); hemi.intensity += flash * 2.5; sun.intensity += flash * 3; }
  else updApt(t, s, sh);
  // the camera: the shot, a breath of handheld drift, shake on hits
  const hand = sh.pov ? .006 : .003, shk = SHAKE;
  camera.position.copy(sh.p).add(V.set(Math.sin(t * .9) * hand + shk * .03 * Math.sin(t * 61), Math.sin(t * 1.3 + 1) * hand + shk * .03 * Math.sin(t * 53), 0));
  camera.fov = sh.fov;
  const cv = window.FUTURE_COVER;
  if (cv && cv.cam) { camera.position.set(...cv.cam); sh.l.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix();
  camera.up.set(0, 1, 0); camera.lookAt(sh.l);
  if (shk) camera.rotateZ(shk * .015 * Math.sin(t * 47));
  // the hands and the phone, only in Alex's own POV
  HANDS.visible = sh.hands;
  if (sh.hands) {
    const h = { ...HP_READ, px: HP_READ.px + .004 * Math.sin(t * 1.1), py: HP_READ.py + .003 * Math.sin(t * 1.7) };
    setHands(h); LHF.g.visible = false;
    const pk = phoneKey(t, s); if (TEX[pk]) setMap(phScrM, TEX[pk]);
  }
  scene.updateMatrixWorld(true);
  const dark = s === 3 || s === 4;
  phoneL.intensity = 0;
  const lit = sh.hands ? PHONE : APH;
  if (lit.visible && phoneKey(t, s) !== "phBlack" && dark) { lit.getWorldPosition(phoneL.position); if (sh.hands) { camera.getWorldDirection(V); phoneL.position.addScaledVector(V, -.12); } else { V.set(0, 0, 1).applyQuaternion(APH.quaternion); phoneL.position.addScaledVector(V, .14); } phoneL.intensity = sh.hands ? .12 : .3; phoneL.distance = sh.hands ? 1.2 : .9; }
  // depth of field, grade
  cocPass.uniforms.uF.value = sh.f; cocPass.uniforms.uAp.value = sh.ap;
  if (cv) { cocPass.uniforms.uAp.value = cv.ap ?? sh.ap; if (cv.focus) cocPass.uniforms.uF.value = cv.focus; }
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = Lk.warm; gu.uCool.value = Lk.cool; gu.uSat.value = Lk.sat; gu.uCon.value = Lk.con; gu.uVig.value = Lk.vig;
  gu.uFlash.value = flash * .45; gu.uCA.value = .0012 + shk * .004;
  gu.uTop.value = cv ? 0 : Math.max(s === 0 ? 1 - ss(t, L[0] - .6, L[0] + .1) : 0, s === 5 ? ss(t, CU[4], CU[4] + .6) : 0);
  gu.uDark.value = s === 4 ? .45 * ss(t, E[15] - .3, CU[4]) : 0;
  bloom.strength = s === 1 ? .55 : s === 5 ? .6 : s === 2 ? .3 : .32;
  // the sun follows the camera
  camera.getWorldDirection(V); V.y = 0; V.normalize();
  const tg = V2.copy(camera.position).addScaledVector(V, Lk.ext * .55); tg.y = 0;
  sun.target.position.copy(tg); sun.position.copy(tg).add(S.set(...Lk.sd).normalize().multiplyScalar(90));
  Object.assign(sun.shadow.camera, { left: -Lk.ext, right: Lk.ext, top: Lk.ext, bottom: -Lk.ext, near: 1, far: 220 });
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT);
  renderer.render(scene, camera);
  renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures that need the fonts
const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`, SERIF = (w, f, it = false) => `${it ? "italic " : ""}${w} ${f}px Garamond, serif`;
const text = (w, h, draw) => pix(w, h, draw, false);
function vnoise(x, y, seed) { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi; const h = (a, b) => hash(a * 57.1 + b * 113.3 + seed * 7.7); const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf); return lerp(lerp(h(xi, yi), h(xi + 1, yi), u), lerp(h(xi, yi + 1), h(xi + 1, yi + 1), u), v); }
const fbm = (x, y, s) => vnoise(x, y, s) * .5 + vnoise(x * 2, y * 2, s + 1) * .25 + vnoise(x * 4, y * 4, s + 2) * .125 + vnoise(x * 8, y * 8, s + 3) * .0625;
// the phone: dark UI, 540 x 1166
const PW = 540, PH_ = 1166;
function phoneScreen(draw, o = {}) {
  return text(PW, PH_, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, o.bg0 || "#121722"); gr.addColorStop(1, o.bg1 || "#07090E"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "#EDEFF5"; g.font = FT(700, 26); g.textAlign = "left"; g.fillText(o.clock || "9:02", 40, 56);
    g.textAlign = "right"; g.fillText("5G", w - 96, 56); g.strokeStyle = "#EDEFF5"; g.lineWidth = 3; rr(g, w - 82, 36, 42, 22, 6); g.stroke(); g.fillRect(w - 78, 40, 28, 14);
    g.fillStyle = "#000"; rr(g, w / 2 - 70, 22, 140, 40, 20); g.fill();
    if (o.app !== false) {
      g.textAlign = "left"; g.fillStyle = "#F2C94C"; g.beginPath(); g.ellipse(64, 134, 22, 13, 0, 0, Math.PI * 2); g.fill(); g.fillStyle = "#121722"; g.beginPath(); g.arc(64, 134, 7, 0, Math.PI * 2); g.fill();
      g.fillStyle = "#F2C94C"; g.font = FT(800, 36); g.fillText("TOMORROW", 100, 147);
      g.fillStyle = "#8A93A8"; g.font = FT(600, 25); g.fillText(o.sub || "24 hours ahead", 42, 196);
    }
    draw(g, w, h);
    g.fillStyle = "rgba(255,255,255,.5)"; rr(g, w / 2 - 80, h - 26, 160, 8, 4); g.fill();
  });
}
const card = (g, x, y, w, h, c = "#1B2130") => { g.fillStyle = c; rr(g, x, y, w, h, 30); g.fill(); };
function wrapText(g, s, x, y, maxW, lh) { const ws = s.split(" "); let line = ""; for (const wd of ws) { const tst = line ? line + " " + wd : wd; if (g.measureText(tst).width > maxW && line) { g.fillText(line, x, y); line = wd; y += lh; } else line = tst; } g.fillText(line, x, y); return y; }
function pxArt(g, rows, x0, y0, s, pal) { rows.forEach((r, j) => { for (let i = 0; i < r.length; i++) if (r[i] !== ".") { g.fillStyle = pal[r[i]]; g.fillRect(x0 + i * s, y0 + j * s, s, s); } }); }
function buildTextures() {
  // skies
  const grad = (stops, stars = 0) => text(16, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); for (let k = 0; k < stars; k++) px(g, "rgba(255,255,255,.8)", Math.floor(hash(k) * 16), Math.floor(hash(k * 3) * 200), 1, 1); });
  SKY.ny = grad([[0, "#7FB2E2"], [.5, "#B9D4EC"], [1, "#F4DEC2"]]);
  SKY.storm = grad([[0, "#3A424E"], [.55, "#5E6872"], [1, "#858E97"]]);
  SKY.day = grad([[0, "#5E9FE0"], [.6, "#A8CDEE"], [1, "#E2EEF6"]]);
  SKY.nynight = grad([[0, "#070B1E"], [.6, "#18224A"], [1, "#2E3A6A"]], 30);
  SKY.dusk = grad([[0, "#1E2452"], [.45, "#5E4A82"], [.75, "#C9707A"], [1, "#F4A56A"]], 14);
  // New York signs
  const led = (tm) => text(512, 212, (g, w, h) => { g.fillStyle = "#0B0A0A"; g.fillRect(0, 0, w, h); g.fillStyle = "#FFB238"; g.shadowColor = "#FF9A1F"; g.shadowBlur = 16; g.font = MONO(118); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(tm, w / 2, 92); g.shadowBlur = 6; g.font = MONO(36); g.fillText("AM   72°F", w / 2, 178); g.shadowBlur = 0; g.fillStyle = "rgba(0,0,0,.35)"; for (let y = 0; y < h; y += 6) g.fillRect(0, y, w, 2); for (let x = 0; x < w; x += 6) g.fillRect(x, 0, 2, h); });
  TEX.led913 = led("9:13"); TEX.led914 = led("9:14");
  const board = (bg, l1, c1, l2, c2, deco) => text(900, 500, (g, w, h) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); if (deco) deco(g, w, h); g.textAlign = "left"; g.fillStyle = c1; g.font = FT(800, 104); g.fillText(l1, 54, 210); g.fillStyle = c2; g.font = FT(800, 54); g.fillText(l2, 58, 300); });
  TEX.bbCoffee = board("#3A2418", "ICED COFFEE", "#F4E6C8", "$2 · ALL DAY", "#F2C94C", (g) => { pxArt(g, ["..wwwww..", ".wcccccw.", ".wbbbbbw.", ".wcccccw.", "..wcccw..", "..wcccw..", "...www..."], 650, 120, 26, { w: "#F4F1EA", c: "#C98A5A", b: "#7A4A2A" }); });
  TEX.bbShow = board("#2A1450", "BROADWAY", "#F2C94C", "TONIGHT · 8 PM", "#FFFFFF", (g, w, h) => { for (let k = 0; k < 30; k++) { g.fillStyle = k % 2 ? "#FFE9A0" : "#F2C94C"; g.beginPath(); g.arc(20 + k * 30, 20, 8, 0, 7); g.fill(); g.beginPath(); g.arc(20 + k * 30, h - 20, 8, 0, 7); g.fill(); } });
  TEX.bbRun = board("#1E4E9A", "CITY MARATHON", "#FFFFFF", "SUNDAY · RUN WITH US", "#9FD8FF");
  const vblade = (txt, bg, fg) => text(130, 600, (g, w, h) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.strokeStyle = fg; g.lineWidth = 6; g.strokeRect(8, 8, w - 16, h - 16); g.fillStyle = fg; g.font = FT(800, 80); g.textAlign = "center"; g.textBaseline = "middle"; const n = txt.length; for (let k = 0; k < n; k++) g.fillText(txt[k], w / 2, 60 + k * (480 / Math.max(1, n - 1))); });
  TEX.blHotel = vblade("HOTEL", "#7A1A1A", "#FFE2B0"); TEX.blTheatre = vblade("THEATRE", "#1E1B18", "#F2C94C");
  // Las Vegas
  const neon = (txt, col, glowc, w = 700, h = 220, f = 150) => text(w, h, (g) => { g.clearRect(0, 0, w, h); g.textAlign = "center"; g.textBaseline = "middle"; g.font = FT(800, f); g.shadowColor = glowc; g.shadowBlur = 30; g.fillStyle = col; g.fillText(txt, w / 2, h / 2 + 6); g.shadowBlur = 8; g.fillText(txt, w / 2, h / 2 + 6); });
  TEX.neonCasino = neon("CASINO", "#FFD6EC", "#FF3FA0"); TEX.neonJackpot = neon("JACKPOT", "#FFF0B0", "#F2B33D", 600, 200, 110); TEX.exitSign = neon("EXIT", "#FFD0D0", "#FF3030", 280, 90, 70);
  const SYM = { 7: ["rrrrr", "....r", "...r.", "..r..", ".r...", ".r..."], c: ["...g.", "..g..", ".rr.r", "rrrrr", "rr.rr", ".r..."], b: ["yyyyy", "y...y", "yyyyy", "y...y", "yyyyy", "....."], d: ["..c..", ".ccc.", "ccccc", ".ccc.", "..c..", "....."] };
  for (let k = 0; k < 4; k++) TEX["slot" + k] = text(280, 220, (g, w, h) => { g.fillStyle = "#14101A"; g.fillRect(0, 0, w, h); const sy = [["7", "7", "7"], ["c", "b", "c"], ["d", "7", "b"], ["b", "b", "d"]][k]; for (let i = 0; i < 3; i++) { g.fillStyle = "#F4F1EA"; g.fillRect(14 + i * 88, 40, 76, 120); pxArt(g, SYM[sy[i]], 22 + i * 88, 64, 12, { r: "#D9302A", g: "#3FA372", y: "#C9932E", c: "#3FA0D9" }); } g.fillStyle = ["#FF4FA0", "#4FD8FF", "#FFC94F", "#9F6BFF"][k]; g.font = FT(800, 30); g.textAlign = "center"; g.fillText(["777", "LUCKY", "WIN", "BONUS"][k], w / 2, 200); });
  TEX.strip = text(1536, 660, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#0A0820"); gr.addColorStop(.7, "#2A1450"); gr.addColorStop(1, "#5A2A6A"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let k = 0; k < 60; k++) px(g, "rgba(255,255,255,.7)", hash(k) * w, hash(k * 3) * 200, 2, 2);
    for (let k = 0; k < 11; k++) { const x = k * 140 - 20, bh = 220 + hash(k * 2.2) * 330, bw = 110 + hash(k) * 50; g.fillStyle = "#120C24"; g.fillRect(x, h - bh, bw, bh); for (let i = 0; i < 5; i++) for (let j = 0; j < Math.floor(bh / 26); j++) if (hash(k * 31 + i * 7 + j) > .45) px(g, "#FFD98A", x + 10 + i * 20, h - bh + 14 + j * 26, 10, 12); g.strokeStyle = ["#FF3FA0", "#3FD8FF", "#F2C94C", "#9F6BFF"][k % 4]; g.lineWidth = 5; g.shadowColor = g.strokeStyle; g.shadowBlur = 18; g.strokeRect(x + 3, h - bh + 3, bw - 6, bh - 6); g.shadowBlur = 0; }
    const sgn = (t, x, y, c, f) => { g.font = FT(800, f); g.textAlign = "center"; g.shadowColor = c; g.shadowBlur = 26; g.fillStyle = "#FFF4F8"; g.fillText(t, x, y); g.shadowBlur = 0; };
    sgn("HOTEL", 300, 230, "#FF3FA0", 90); sgn("LUCKY 7", 800, 170, "#F2C94C", 110); sgn("OPEN 24H", 1240, 260, "#3FD8FF", 80);
    g.fillStyle = "#050308"; g.fillRect(0, h - 70, w, 70); for (let k = 0; k < 40; k++) { g.fillStyle = k % 2 ? "rgba(255,240,200,.9)" : "rgba(255,60,60,.9)"; g.fillRect(hash(k * 5) * w, h - 50 + (k % 2) * 16, 40 + hash(k) * 80, 4); }
    for (const x of [120, 560, 1020, 1420]) { g.fillStyle = "#08060C"; g.fillRect(x, h - 300, 14, 240); for (let k = 0; k < 7; k++) { g.save(); g.translate(x + 7, h - 300); g.rotate(-Math.PI / 2 + (k - 3) * .45); g.fillRect(0, -6, 90, 12); g.restore(); } }
  });
  TEX.felt = text(520, 920, (g, w, h) => {
    g.fillStyle = "#1F6B3E"; g.fillRect(0, 0, w, h); for (let k = 0; k < 4000; k++) px(g, hash(k * 1.3) > .5 ? "rgba(255,255,255,.035)" : "rgba(0,0,0,.05)", hash(k * 2.1) * w, hash(k * 3.7) * h, 2, 2);
    g.strokeStyle = "#F4F1EA"; g.lineWidth = 3; g.textAlign = "center"; g.textBaseline = "middle";
    g.fillStyle = "#1F8A4A"; g.fillRect(95, 23, 330, 54); g.strokeRect(95, 23, 330, 54); g.fillStyle = "#FFFFFF"; g.font = FT(800, 38); g.fillText("0", 260, 52);
    for (let n = 1; n <= 36; n++) { const r = Math.ceil(n / 3) - 1, c = (n - 1) % 3, x = 95 + c * 110, y = 77 + r * 66; g.fillStyle = REDS.has(n) ? "#C8372D" : "#1E1B18"; g.fillRect(x + 6, y + 6, 98, 54); g.strokeRect(x, y, 110, 66); g.fillStyle = "#FFFFFF"; g.font = FT(800, 34); g.fillText(String(n), x + 55, y + 35); }
    for (let k = 0; k < 3; k++) { g.strokeRect(5, 77 + k * 264, 85, 264); g.save(); g.translate(48, 77 + k * 264 + 132); g.rotate(-Math.PI / 2); g.fillStyle = "#F4F1EA"; g.font = FT(800, 30); g.fillText(["1st 12", "2nd 12", "3rd 12"][k], 0, 0); g.restore(); }
    ["1-18", "EVEN", "RED", "BLACK", "ODD", "19-36"].forEach((s, k) => { const y = 77 + k * 132; g.strokeRect(430, y, 85, 132); g.save(); g.translate(472, y + 66); if (s === "RED" || s === "BLACK") { g.fillStyle = s === "RED" ? "#C8372D" : "#1E1B18"; g.beginPath(); g.moveTo(0, -46); g.lineTo(26, 0); g.lineTo(0, 46); g.lineTo(-26, 0); g.closePath(); g.fill(); g.stroke(); } else { g.rotate(-Math.PI / 2); g.fillStyle = "#F4F1EA"; g.font = FT(800, 28); g.fillText(s, 0, 0); } g.restore(); });
    for (let c = 0; c < 3; c++) { g.strokeRect(95 + c * 110, 869, 110, 46); g.fillStyle = "#F4F1EA"; g.font = FT(800, 22); g.fillText("2 to 1", 150 + c * 110, 893); }
  });
  TEX.wheel = text(1024, 1024, (g, w, h) => {
    const c = 512, gr = g.createRadialGradient(c, c, 40, c, c, 384); gr.addColorStop(0, "#5A3420"); gr.addColorStop(1, "#8A5A34"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    const hw = Math.PI / 37;
    for (let i = 0; i < 37; i++) { const a = i * Math.PI * 2 / 37, n = WHEEL[i]; g.fillStyle = n === 0 ? "#1F8A4A" : REDS.has(n) ? "#C8372D" : "#15151A"; g.beginPath(); g.arc(c, c, 506, -a - hw, -a + hw); g.arc(c, c, 380, -a + hw, -a - hw, true); g.closePath(); g.fill();
      g.save(); g.translate(c + Math.cos(-a) * 470, c + Math.sin(-a) * 470); g.rotate(-a + Math.PI / 2); g.fillStyle = "#FFFFFF"; g.font = FT(800, 30); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(String(n), 0, 0); g.restore(); }
    g.strokeStyle = "#E9B949"; g.lineWidth = 8; g.beginPath(); g.arc(c, c, 380, 0, 7); g.stroke(); g.beginPath(); g.arc(c, c, 432, 0, 7); g.lineWidth = 3; g.stroke();
    for (let k = 0; k < 8; k++) { g.save(); g.translate(c, c); g.rotate(k * Math.PI / 4); g.fillStyle = "rgba(233,185,73,.55)"; g.fillRect(60, -6, 300, 12); g.restore(); }
  });
  // the apartment
  TEX.nightCity = text(1024, 640, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#070B1C"); gr.addColorStop(1, "#1C2650"); g.fillStyle = gr; g.fillRect(0, 0, w, h); for (let k = 0; k < 80; k++) px(g, "rgba(255,255,255,.7)", hash(k) * w, hash(k * 3) * 260, 2, 2); g.fillStyle = "#EEF2FF"; g.shadowColor = "#BFD0FF"; g.shadowBlur = 30; g.beginPath(); g.arc(760, 120, 40, 0, 7); g.fill(); g.shadowBlur = 0; for (let k = 0; k < 16; k++) { const x = k * 68 - 10, bh = 150 + hash(k * 2.7) * 320; g.fillStyle = "#0E1430"; g.fillRect(x, h - bh, 62, bh); for (let i = 0; i < 4; i++) for (let j = 0; j < Math.floor(bh / 22); j++) if (hash(k * 41 + i * 5 + j * 3) > .55) px(g, "#FFD98A", x + 6 + i * 14, h - bh + 10 + j * 22, 8, 10); } });
  TEX.spill = text(128, 96, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "rgba(255,190,120,.55)"); gr.addColorStop(1, "rgba(255,190,120,0)"); g.fillStyle = gr; g.beginPath(); g.moveTo(24, 0); g.lineTo(104, 0); g.lineTo(128, h); g.lineTo(0, h); g.closePath(); g.fill(); });
  TEX.clock = text(128, 128, (g, w, h) => { g.fillStyle = "#F4F1EA"; g.beginPath(); g.arc(64, 64, 62, 0, 7); g.fill(); g.strokeStyle = "#1E1B18"; g.lineWidth = 6; g.stroke(); for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; g.fillStyle = "#1E1B18"; g.fillRect(64 + Math.cos(a) * 50 - 2, 64 + Math.sin(a) * 50 - 2, 5, 5); } const hand = (a, l, wd) => { g.save(); g.translate(64, 64); g.rotate(a); g.fillRect(-wd / 2, -l, wd, l); g.restore(); }; g.fillStyle = "#1E1B18"; hand((11.8 / 12) * Math.PI * 2, 30, 6); hand((48 / 60) * Math.PI * 2, 46, 4); });
  // the rooftop: the globe (land, storms) and the ten-day cards
  TEX.earth = text(1024, 512, (g, w, h) => { const id = g.createImageData(w, h); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const n = fbm(x / 120, y / 120, 5), lat = Math.abs(y / h - .5) * 2, land = n > .56 - lat * .04, i = (y * w + x) * 4; const c = land ? (lat > .82 ? [220, 235, 245] : [40 + n * 120, 150 + n * 60, 150 + n * 40]) : [12, 40 + n * 50, 90 + n * 90]; id.data[i] = c[0]; id.data[i + 1] = c[1]; id.data[i + 2] = c[2]; id.data[i + 3] = 255; } g.putImageData(id, 0, 0); g.strokeStyle = "rgba(143,230,255,.35)"; g.lineWidth = 1; for (let k = 1; k < 12; k++) { g.beginPath(); g.moveTo(0, k * h / 12); g.lineTo(w, k * h / 12); g.stroke(); } for (let k = 0; k < 24; k++) { g.beginPath(); g.moveTo(k * w / 24, 0); g.lineTo(k * w / 24, h); g.stroke(); } });
  TEX.clouds = text(1024, 512, (g, w, h) => { const id = g.createImageData(w, h); const sw = [[300, 170], [640, 330], [860, 140]]; for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let a = 0; for (const [cx, cy] of sw) { const dx = x - cx, dy = y - cy, r = Math.hypot(dx, dy); if (r < 90) { const th = Math.atan2(dy, dx) + r * .06; a = Math.max(a, (.5 + .5 * Math.sin(th * 3)) * (1 - r / 90) * 1.4); } } a = Math.max(a, clamp((fbm(x / 70, y / 40, 9) - .52) * 3.2) * .85); const i = (y * w + x) * 4; id.data[i] = 245; id.data[i + 1] = 250; id.data[i + 2] = 255; id.data[i + 3] = clamp(a) * 230; } g.putImageData(id, 0, 0); });
  const DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN", "MON", "TUE", "WED"], ICO = ["sun", "sun", "cloud", "rain", "storm", "cloud", "sun", "sun", "rain", "sun"], TMP = [81, 83, 79, 74, 72, 76, 80, 84, 77, 82];
  const icon = (g, k, x, y, s) => { const I = { sun: ["..y..y..", "y.yyyy.y", ".yyyyyy.", "yyyyyyyy", ".yyyyyy.", "y.yyyy.y", "..y..y.."], cloud: ["........", "...www..", "..wwwww.", ".wwwwwww", "wwwwwwww", ".wwwwww.", "........"], rain: ["...www..", "..wwwww.", ".wwwwwww", "wwwwwwww", ".b.b.b..", "b.b.b...", "........"], storm: ["...ggg..", "..ggggg.", ".ggggggg", "gggggggg", "...yy...", "..yy....", ".yy....."] }[k]; pxArt(g, I, x, y, s, { y: "#FFD34A", w: "#F4F8FF", b: "#6FC3FF", g: "#9AA6B8" }); };
  for (let k = 0; k < 10; k++) TEX["day" + k] = text(260, 350, (g, w, h) => { g.fillStyle = "rgba(20,60,90,.55)"; rr(g, 4, 4, w - 8, h - 8, 26); g.fill(); g.strokeStyle = "#8FE6FF"; g.lineWidth = 5; g.stroke(); g.fillStyle = "#EFFBFF"; g.textAlign = "center"; g.font = FT(800, 46); g.fillText(DAYS[k], w / 2, 70); g.fillStyle = "#8FE6FF"; g.font = FT(700, 26); g.fillText("DAY " + (k + 1), w / 2, 104); icon(g, ICO[k], 66, 134, 16); g.fillStyle = "#FFFFFF"; g.font = FT(800, 58); g.fillText(TMP[k] + "°", w / 2, 320); });
  // the phone screens
  TEX.phNY = phoneScreen((g, w) => {
    card(g, 30, 236, w - 60, 560); pxArt(g, [".....ww.....", "....wccw....", "....wbbw.....", "....wccw....", ".....ww.....", "............", "..b...b..b..", "bb.bbbbbb.bb", ".bbbbbbbbbb."], 150, 270, 20, { w: "#F4F1EA", c: "#C98A5A", b: "#7A4A2A" });
    g.fillStyle = "#FFFFFF"; g.textAlign = "left"; g.font = FT(800, 108); g.fillText("9:14 AM", 58, 590); g.font = FT(700, 50); g.fillStyle = "#EDEFF5"; wrapText(g, "The man in the grey coat drops his coffee", 60, 670, w - 120, 58);
    g.fillStyle = "#5C6578"; g.font = FT(700, 30); g.fillText("11:30 AM   Light rain", 52, 900); g.fillText("6:05 PM    Train delayed", 52, 960);
  }, { clock: "9:02", sub: "Day 1 · 24 hours ahead" });
  TEX.phVegas = phoneScreen((g, w) => {
    card(g, 30, 236, w - 60, 700); g.fillStyle = "#8A93A8"; g.font = FT(700, 30); g.textAlign = "center"; g.fillText("ROULETTE · 10:42 PM", w / 2, 300);
    g.fillStyle = "#0B0B0E"; g.beginPath(); g.arc(w / 2, 540, 180, 0, 7); g.fill(); g.strokeStyle = "#F2C94C"; g.lineWidth = 10; g.stroke(); g.fillStyle = "#FFFFFF"; g.font = FT(800, 200); g.textBaseline = "middle"; g.fillText("17", w / 2, 550); g.textBaseline = "alphabetic";
    g.fillStyle = "#EDEFF5"; g.font = FT(800, 60); g.fillText("BLACK", w / 2, 820); g.fillStyle = "#8A93A8"; g.font = FT(600, 30); g.fillText("Winning number", w / 2, 880);
  }, { clock: "10:11", sub: "Day 4 · 24 hours ahead" });
  TEX.phMiami = phoneScreen((g, w) => {
    g.fillStyle = "#C8372D"; rr(g, 30, 226, w - 60, 96, 26); g.fill(); g.fillStyle = "#FFFFFF"; g.font = FT(800, 42); g.textAlign = "center"; g.fillText("STORM WARNING", w / 2, 290);
    card(g, 30, 344, w - 60, 640); pxArt(g, ["............", "ggg......ggg", "ggg.y....ggg", "gg..yy....gg", "g....y.....g", "..b..y...b..", "..b......b..", "wwwwwwwwwwww"], 90, 380, 30, { g: "#B9B4AA", y: "#FFD34A", b: "#8A8E94", w: "#3F6E86" });
    g.fillStyle = "#FFFFFF"; g.textAlign = "left"; g.font = FT(800, 104); g.fillText("12:00 PM", 58, 760); g.fillStyle = "#FF6B5E"; g.font = FT(800, 54); g.fillText("Bridge collapses", 60, 840); g.fillStyle = "#EDEFF5"; g.font = FT(800, 40); g.fillText("14 cars on it", 60, 900);
  }, { clock: "7:48", sub: "Day 12 · 24 hours ahead" });
  const avatar = (g, x, y, r) => { g.fillStyle = "#3A6FC4"; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); g.fillStyle = "#FFFFFF"; g.font = FT(800, r * .8); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("ME", x, y + 2); g.textBaseline = "alphabetic"; };
  TEX.phMsgIn = phoneScreen((g, w) => {
    g.fillStyle = "#FFFFFF"; g.font = FT(800, 54); g.textAlign = "left"; g.fillText("Messages", 40, 160);
    card(g, 26, 220, w - 52, 330, "#232A3A"); avatar(g, 110, 330, 54); g.textAlign = "left"; g.fillStyle = "#FFFFFF"; g.font = FT(800, 44); g.fillText("You", 186, 316); g.fillStyle = "#AEB6C8"; g.font = FT(600, 30); g.fillText("+1 (305) 555-0142", 186, 362);
    g.fillStyle = "#F2C94C"; g.font = FT(800, 32); g.fillText("This is your own number", 52, 470); g.fillStyle = "#8A93A8"; g.font = FT(600, 28); g.fillText("1 new message · sent tomorrow", 52, 516);
  }, { clock: "11:47", app: false, bg0: "#0E1220", bg1: "#05060A" });
  TEX.phMsg = phoneScreen((g, w) => {
    g.fillStyle = "#1A1F2C"; g.fillRect(0, 84, w, 170); avatar(g, w / 2, 150, 40); g.fillStyle = "#FFFFFF"; g.font = FT(800, 34); g.textAlign = "center"; g.fillText("You", w / 2, 228);
    g.fillStyle = "#8A93A8"; g.font = FT(600, 26); g.fillText("Tomorrow · 11:48 PM", w / 2, 320);
    g.fillStyle = "#2E3546"; rr(g, 34, 360, w - 90, 280, 40); g.fill(); g.fillStyle = "#FFFFFF"; g.textAlign = "left"; g.font = FT(800, 64); wrapText(g, "Don't open the door.", 72, 470, w - 160, 80);
  }, { clock: "11:47", app: false, bg0: "#0E1220", bg1: "#05060A" });
  TEX.phNotJay = phoneScreen((g, w) => {
    g.fillStyle = "#1A1F2C"; g.fillRect(0, 84, w, 170); avatar(g, w / 2, 150, 40); g.fillStyle = "#FFFFFF"; g.font = FT(800, 34); g.textAlign = "center"; g.fillText("You", w / 2, 228);
    g.fillStyle = "#2E3546"; rr(g, 34, 300, w - 90, 150, 34); g.fill(); g.fillStyle = "#AEB6C8"; g.textAlign = "left"; g.font = FT(700, 40); g.fillText("Don't open the door.", 64, 390);
    g.fillStyle = "#8A93A8"; g.font = FT(600, 26); g.textAlign = "center"; g.fillText("Now", w / 2, 520);
    g.fillStyle = "#C8372D"; rr(g, 34, 560, w - 68, 300, 40); g.fill(); g.fillStyle = "#FFFFFF"; g.textAlign = "left"; g.font = FT(800, 78); wrapText(g, "That's not Jay.", 76, 690, w - 150, 92);
  }, { clock: "11:49", app: false, bg0: "#0E1220", bg1: "#05060A" });
  for (let k = 0; k < 3; k++) TEX["phGlitch" + k] = text(PW, PH_, (g, w, h) => { g.fillStyle = "#05060A"; g.fillRect(0, 0, w, h); for (let j = 0; j < 60; j++) { const y = hash(j * 7.1 + k * 13) * h, hh = 4 + hash(j * 3 + k) * 40; g.fillStyle = ["#F2C94C", "#7FE3FF", "#C8372D", "#FFFFFF", "#2E3546"][Math.floor(hash(j + k * 5) * 5)]; g.globalAlpha = .25 + hash(j * 2 + k) * .6; g.fillRect((hash(j * 5 + k) - .3) * w, y, w * (.3 + hash(j + 9 * k) * .9), hh); } g.globalAlpha = 1; g.fillStyle = "#FFFFFF"; g.font = FT(800, 110); g.textAlign = "center"; g.fillText(["DAY 3?", "D4Y 31", "NO DATA"][k], w / 2 + (k - 1) * 18, 560); g.font = FT(800, 40); g.fillStyle = "#C8372D"; g.fillText("TOMORROW NOT FOUND", w / 2, 680); });
  for (let k = 0; k < 4; k++) TEX["phLoad" + k] = phoneScreen((g, w) => {
    g.fillStyle = "#FFFFFF"; g.textAlign = "center"; g.font = FT(800, 120); g.fillText("DAY 31", w / 2, 520);
    for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4 + k * Math.PI / 8; g.fillStyle = `rgba(242,201,76,${.2 + .8 * ((i + 8 - k * 2) % 8) / 8})`; g.beginPath(); g.arc(w / 2 + Math.cos(a) * 70, 720 + Math.sin(a) * 70, 14, 0, 7); g.fill(); }
    g.fillStyle = "#8A93A8"; g.font = FT(700, 34); g.fillText("Loading tomorrow...", w / 2, 900);
  }, { clock: "6:02", sub: "Day 30 · 24 hours ahead" });
  TEX.phBlack = text(PW, PH_, (g, w, h) => { g.fillStyle = "#000"; g.fillRect(0, 0, w, h); const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "rgba(255,255,255,.06)"); gr.addColorStop(.4, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  TEX.phCast = phoneScreen((g, w) => {
    g.fillStyle = "#8FE6FF"; g.font = FT(800, 36); g.textAlign = "left"; g.fillText("AI FORECAST · 10 DAYS", 40, 280);
    for (let k = 0; k < 8; k++) { const y = 330 + k * 92; card(g, 30, y, w - 60, 80, "#18202E"); g.fillStyle = "#EDEFF5"; g.font = FT(800, 34); g.fillText(DAYS[k], 60, y + 52); icon(g, ICO[k], 220, y + 14, 7); g.textAlign = "right"; g.fillText(TMP[k] + "°", w - 60, y + 52); g.textAlign = "left"; }
  }, { clock: "2:15", sub: "Weather · 10 days ahead" });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  const bc = document.createElement("canvas"); bc.width = 840; bc.height = 280; TEX.boardC = bc; TEX.boardG = bc.getContext("2d");
  TEX.boardT = new THREE.CanvasTexture(bc); TEX.boardT.colorSpace = THREE.SRGBColorSpace; SET.vegas.boardM.map = TEX.boardT; SET.vegas.boardM.needsUpdate = true;
  drawBoard(0, 0, false);
  setMap(phScrM, TEX.phNY);
}
let boardK = "";
function drawBoard(phase, amt, blink) {
  if (!TEX.boardG) return; const k = phase + "|" + amt + "|" + blink; if (k === boardK) return; boardK = k;
  const g = TEX.boardG, w = 840, h = 280;
  g.fillStyle = "#0A0708"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 28; i++) for (const y of [12, h - 12]) { g.fillStyle = (i + (blink ? 1 : 0)) % 2 ? "#FFE9A0" : "#8A6A2A"; g.beginPath(); g.arc(18 + i * 29.4, y, 7, 0, 7); g.fill(); }
  g.textAlign = "center"; g.textBaseline = "middle";
  if (phase === 0) { g.fillStyle = "#F2C94C"; g.font = FT(800, 64); g.fillText("PLACE YOUR BETS", w / 2, h / 2); }
  else { g.fillStyle = "#FFFFFF"; g.font = FT(800, 54); g.fillText("17 BLACK · WINNER", w / 2, 82); g.shadowColor = "#F2B33D"; g.shadowBlur = 24; g.fillStyle = "#F2C94C"; g.font = FT(800, 110); g.fillText("$" + amt.toLocaleString("en-US"), w / 2, 182); g.shadowBlur = 0; }
  TEX.boardT.needsUpdate = true;
}

const ready = (async () => {
  try { const jb = new FontFace("JBMono", "url(assets/fonts/jbmono-bold.ttf)", { weight: "700" }); document.fonts.add(await jb.load()); } catch (e) { /* fall back */ }
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 40px Manrope"), document.fonts.load("600 40px Manrope"), document.fonts.load("500 40px Garamond")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  for (const k in SET) SET[k].visible = true;
  renderer.compile(scene, camera);
  renderAt(window.FUTURE_COVER ? window.FUTURE_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["future"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.FUTURE_COVER ? window.FUTURE_COVER.t : e.detail.time));
window.FUTURE_DEBUG = { renderAt, SET, camera, C };
