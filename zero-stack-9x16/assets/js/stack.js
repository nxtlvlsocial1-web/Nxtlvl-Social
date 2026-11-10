// Zero Stack reel: "What if every app you pay for vanished overnight?" A cinematic dialogue what-if in the house voxel
// style. Maya, a solo founder, wakes up to every paid app cancelled and locked for 30 days, a month before her launch.
// Noah, the developer next door, replaces each one with an open-source tool, day by day, until the bill reads $0.
// Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek; cue times come from the voice
// (window.CT, written by build/generate.py). Post: depth of field from the depth buffer, bloom, then the grade.
//   s0  the loft, dawn, day 1     the cancellations; locked for 30 days; Noah at the door
//   s1  the loft, day, days 1-8   Adobe, Canva, CapCut replaced (each app's tile bursts into voxels and re-forms)
//   s2  the loft, afternoon, 12-25 Mailchimp, Hootsuite, Linktree, Notion replaced
//   s3  the loft, night, storm, 29 no ChatGPT, then the internet dies; an AI on her own laptop, offline
//   s4  the loft, morning, day 30 launch day orders; the bill is $0; resubscribe? no thanks; the CTA
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
// ---------------------------------------------------------------- shared ground textures
const noiseTex = (base, n, amp, sz = 64) => pix(sz, sz, (g) => { px(g, base, 0, 0, sz, sz); for (let i = 0; i < sz; i++) for (let j = 0; j < sz; j++) { const h = hash(i * 31.7 + j * 7.3 + n); if (h > .7) { g.fillStyle = `rgba(${h > .85 ? "255,255,255" : "0,0,0"},${amp})`; g.fillRect(i, j, 1, 1); } } }, false);
const ASPH = noiseTex("#4A4C52", 1, .07), SAND = noiseTex("#C9B48A", 2, .08), GRAVEL = noiseTex("#8E8A84", 3, .1), CONC = noiseTex("#B9B4AA", 4, .05);
const tileTex = pix(64, 64, (g) => { px(g, "#C4BFB6", 0, 0, 64, 64); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { g.fillStyle = hash(i * 5 + j * 3) > .5 ? "rgba(255,255,255,.05)" : "rgba(0,0,0,.04)"; g.fillRect(i * 16, j * 16, 16, 16); } for (let k = 0; k < 4; k++) { px(g, "#A9A39A", k * 16, 0, 1, 64); px(g, "#A9A39A", 0, k * 16, 64, 1); } }, false);
const groundMat = (t, x, y, o = {}) => new THREE.MeshStandardMaterial({ map: rep(t, x, y), roughness: .92, ...o });
function flat(w, d, m, x, y, z, parent) { const p = add(new THREE.Mesh(new THREE.PlaneGeometry(w, d), m), false, true, parent); p.rotation.x = -Math.PI / 2; p.position.set(x, y, z); return p; }

// ================================================================= the LOFT: Maya's home studio (one room, five looks)
// x: -4 .. 4 (door wall); z: -4 (window wall) .. 4.5; ceiling 3.2. The desk stands in front of the window, Maya sits
// behind it facing the room (+z); the bed is in the back-right corner; the door on the right wall; the couch at the front.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
const R = mkSet("loft");
const DESK = { x: -1.3, y: .76, z: -2.0 };
const MON = v3(-.78, 1.22, -1.9);                 // monitor screen centre, facing her (-z)
const CHAIR = v3(-1.5, 0, -2.8);
const TILE = v3(-.62, 1.98, -1.8);                // where the app tiles float, above the monitor, facing the room
const LAP = v3(-2.05, .79, -1.82);                // laptop hinge
const BEDP = v3(2.85, 0, -2.55);
const DOORP = v3(3.98, 0, -.3);
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
{
  const plankTex = pix(64, 64, (g) => { px(g, "#B98A5E", 0, 0, 64, 64); for (let j = 0; j < 8; j++) { px(g, j % 2 ? "#B08154" : "#C29468", 0, j * 8, 64, 8); px(g, "#8E6440", 0, j * 8, 64, 1); px(g, "#8E6440", (j * 23) % 64, j * 8, 1, 8); } for (let k = 0; k < 90; k++) px(g, "rgba(0,0,0,.06)", Math.floor(hash(k) * 64), Math.floor(hash(k * 3) * 64), 2, 1); }, false);
  flat(8.2, 8.7, new THREE.MeshStandardMaterial({ map: rep(plankTex, 5, 5), roughness: .7 }), 0, 0, .25);
  const wallM = mat(0xE9E1D3), wallB = mat(0xD8CFC0), trim = mat(0xF4EFE6), ceilM = mat(0xF1ECE3);
  box(8.2, .12, 8.9, ceilM, 0, 3.26, .25, { cast: false });
  // back wall (z -4) with the big window on the left
  box(.5, 3.2, .2, wallM, -3.85, 1.6, -4.1); box(4.6, 3.2, .2, wallM, 1.9, 1.6, -4.1);
  box(3.3, .9, .2, wallM, -1.95, .45, -4.1); box(3.3, .5, .2, wallM, -1.95, 2.95, -4.1);
  for (const x of [-3.6, -.3]) box(.1, 1.8, .26, trim, x, 1.8, -4.04); for (const y of [.9, 2.7]) box(3.4, .1, .26, trim, -1.95, y, -4.04);
  box(.06, 1.8, .1, trim, -1.95, 1.8, -4.04); box(3.3, .06, .1, trim, -1.95, 1.8, -4.04);
  box(3.5, .06, .34, trim, -1.95, .88, -3.9);   // the sill
  R.glassM = new THREE.MeshPhysicalMaterial({ color: 0xBFD6E6, roughness: .05, transparent: true, opacity: .1, envMap: ENV, envMapIntensity: 1, depthWrite: false });
  plane(3.3, 1.8, R.glassM, -1.95, 1.8, -4.08);
  R.rainM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, toneMapped: false, depthWrite: false }); LATE.push([R.rainM, "rain"]);
  plane(3.3, 1.8, R.rainM, -1.95, 1.8, -4.06);
  // the city outside (a big painted plane), swapped per look
  R.cityM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }); LATE.push([R.cityM, "cityDay"]);
  plane(30, 17, R.cityM, -1.5, 3.2, -14);
  // left wall (desk wall) and right wall (door wall), front wall
  box(.2, 3.2, 8.9, wallB, -4.1, 1.6, .25);
  box(.2, 3.2, 3.2, wallM, 4.1, 1.6, -2.5); box(.2, 3.2, 3.8, wallM, 4.1, 1.6, 2.6); box(.2, .95, 1.1, wallM, 4.1, 2.72, -.3);
  for (const z of [-.88, .28]) box(.26, 2.26, .1, trim, 4.03, 1.13, z); box(.26, .1, 1.26, trim, 4.03, 2.25, -.3);
  const door = new THREE.Group(); door.position.set(4.02, 0, -.85); R.add(door); R.door = door;
  box(.06, 2.2, 1.1, mat(0x7A5A40, { roughness: .6 }), 0, 1.1, .55, { parent: door });
  for (const y of [.62, 1.62]) box(.02, .8, .8, mat(0x6A4C36, { roughness: .6 }), -.035, y, .55, { parent: door });
  box(.05, .04, .16, goldM, -.06, 1.05, .98, { parent: door });
  box(8.2, 3.2, .2, wallM, 0, 1.6, 4.6);
  for (const [w, d, x, z] of [[8.2, .2, 0, -3.97], [.2, 8.7, -3.97, .25], [.2, 8.7, 3.97, .25]]) box(w, .12, d, trim, x, .06, z, { cast: false });
  // the desk, chair, monitor, laptop, keyboard, desk lamp, ring light
  const deskM = mat(0xE8DCC6, { roughness: .5 }), legM = metal(0x2A2A2E, .4);
  box(2.2, .05, .8, deskM, DESK.x, DESK.y - .025, DESK.z);
  for (const [dx, dz] of [[-1.04, -.34], [1.04, -.34], [-1.04, .34], [1.04, .34]]) box(.05, .73, .05, legM, DESK.x + dx, .365, DESK.z + dz);
  box(2.1, .42, .03, mat(0xD9CDB6, { roughness: .5 }), DESK.x, .52, DESK.z + .38);   // the front panel
  const mon = new THREE.Group(); mon.position.copy(MON); R.add(mon);
  box(.84, .51, .04, mat(0x16171B, { roughness: .4 }), 0, 0, .025, { parent: mon });
  R.monM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const ms = new THREE.Mesh(new THREE.PlaneGeometry(.8, .465), R.monM); ms.rotation.y = Math.PI; ms.position.z = .004; mon.add(ms); R.monS = ms;
  box(.06, .32, .06, legM, 0, -.4, .06, { parent: mon }); box(.3, .02, .24, mat(0x2A2A2E), 0, -.45, .05, { parent: mon });
  // laptop: a hinge group; the lid tilts back, its screen faces her
  const lap = new THREE.Group(); lap.position.copy(LAP); lap.rotation.y = Math.PI; R.add(lap);
  box(.34, .018, .24, metal(0xB8BCC4, .35), 0, .009, .12, { parent: lap });
  box(.3, .002, .12, mat(0x2A2A2E), 0, .019, .1, { parent: lap });
  const lid = new THREE.Group(); lid.rotation.x = -.28; lap.add(lid);
  box(.34, .23, .012, metal(0xB8BCC4, .35), 0, .115, -.007, { parent: lid });
  R.lapM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const ls = new THREE.Mesh(new THREE.PlaneGeometry(.31, .2), R.lapM); ls.position.set(0, .118, .0); lid.add(ls); R.lapS = ls;
  box(.46, .02, .16, mat(0x2E2E33), -1.4, .77, -2.18); box(.08, .02, .12, mat(0x2E2E33), -1.0, .77, -2.2);   // keyboard, mouse
  box(.1, .02, .1, mat(0x3A3A40), -.25, .77, -2.32); cyl(.012, .012, .45, legM, -.25, 1.0, -2.32, 8);
  R.lampM = mat(0xF4E6C8, { emissive: 0xFFC98A, emissiveIntensity: 0 });
  const lh = cyl(.05, .11, .12, R.lampM, -.3, 1.22, -2.28, 16); lh.rotation.x = .6;
  cyl(.045, .045, .1, mat(0xF2F2F2), -.4, .81, -1.8, 14);     // a mug
  for (let k = 0; k < 3; k++) box(.28, .03, .2, mat(["#3A6FC4", "#D9483B", "#F2B33D"][k]), -2.2 + .03 * k, .79 + k * .03, -2.25);   // notebooks
  // the chair: a group so it swivels with her (its back is behind her, at -z)
  const chair = new THREE.Group(); chair.position.copy(CHAIR); R.add(chair); R.chair = chair;
  const chM = mat(0x2E3440, { roughness: .6 });
  box(.5, .08, .52, chM, 0, .46, 0, { parent: chair }); box(.48, .62, .07, chM, 0, .84, -.27, { parent: chair });
  cyl(.03, .03, .4, legM, 0, .23, 0, 8, { parent: chair });
  for (let k = 0; k < 5; k++) { const a = k * Math.PI * 2 / 5; box(.3, .03, .04, legM, Math.cos(a) * .15, .04, Math.sin(a) * .15, { parent: chair }).rotation.y = -a; }
  // ring light on a stand at her side, angled at her face
  const ring = new THREE.Group(); ring.position.set(-2.75, 1.55, -2.05); R.add(ring); ring.lookAt(-1.5, 1.52, -2.8);
  R.ringM = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xFFF4E0, emissiveIntensity: .2, roughness: .4 });
  ring.add(new THREE.Mesh(new THREE.TorusGeometry(.2, .025, 8, 40), R.ringM));
  cyl(.012, .012, 1.55, legM, -2.75, .775, -2.05, 8);
  // shelves on the back wall with Maya's product (candles in jars) and boxes
  const shM = mat(0xC9A27A, { roughness: .6 });
  for (const y of [1.2, 1.7, 2.2]) box(1.5, .04, .3, shM, 1.1, y, -3.84);
  for (let k = 0; k < 15; k++) { const sx = .5 + (k % 5) * .3, sy = 1.22 + Math.floor(k / 5) * .5; const jar = cyl(.07, .07, .14, gloss(["#E8735A", "#F2C94C", "#F4E6C8", "#7E5BB0", "#3FA372"][k % 5], { transmission: 0 }), sx, sy + .07, -3.82, 12); jar.castShadow = false; cyl(.072, .072, .03, mat(0x1E1B18), sx, sy + .155, -3.82, 12); }
  // the bed in the corner, a nightstand with her phone
  box(2.1, .32, 2.3, mat(0x7A5A40), BEDP.x, .16, -2.75); box(2.0, .2, 2.2, mat(0xF4EFE6), BEDP.x, .42, -2.75);
  box(2.1, .9, .1, mat(0x6A4C36), BEDP.x, .45, -3.9);
  box(.7, .12, .4, mat(0xFFFDF8), BEDP.x, .58, -3.45);
  R.blanket = box(2.04, .1, 1.3, mat(0x5B7FC4), BEDP.x, .56, -2.05);
  box(.5, .55, .45, mat(0x7A5A40), 1.4, .275, -3.6);
  R.phone = new THREE.Group(); R.phone.position.set(1.42, .565, -3.52); R.phone.rotation.y = .3; R.add(R.phone);
  box(.08, .012, .16, mat(0x15171C), 0, 0, 0, { parent: R.phone });
  R.phoneM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }); LATE.push([R.phoneM, "phoneOff"]);
  const pS = new THREE.Mesh(new THREE.PlaneGeometry(.072, .15), R.phoneM); pS.rotation.x = -Math.PI / 2; pS.position.y = .007; R.phone.add(pS);
  // couch at the front, a rug, a floor lamp, plants, a poster, a clock
  const couchM = mat(0x3E5A7A);
  box(2.2, .45, .9, couchM, 1.6, .3, 3.1); box(2.2, .6, .25, couchM, 1.6, .8, 3.45); for (const x of [.6, 2.6]) box(.25, .35, .9, couchM, x, .62, 3.1);
  box(3.2, .015, 2.4, mat(0xB86A4A), .2, .008, 1.4, { cast: false });
  box(1.0, .06, .55, mat(0x7E5A3E), 1.5, .42, 1.9); for (const [dx, dz] of [[-.42, -.22], [.42, -.22], [-.42, .22], [.42, .22]]) box(.05, .4, .05, mat(0x3A2A1E), 1.5 + dx, .2, 1.9 + dz);
  cyl(.02, .02, 1.6, mat(INK), 3.4, .8, 3.6, 8); R.flM = mat(0xF4E6C8, { emissive: 0xFFC98A, emissiveIntensity: 0 }); cyl(.16, .22, .28, R.flM, 3.4, 1.7, 3.6, 16);
  for (const [x, z, h] of [[-3.6, -3.55, 1.1], [3.55, -1.4, .8], [-.1, -3.6, .6]]) { cyl(.18, .14, .3, mat(0xC9644E), x, .15, z, 12); for (let j = 0; j < 4; j++) box(.3 - j * .04, .3, .3 - j * .04, mat(j % 2 ? 0x4E7A3E : 0x5E8C48), x + (hash(x + j) - .5) * .1, .4 + j * h * .25, z + (hash(z + j) - .5) * .1); }
  R.posterM = texMat("poster", { transparent: false }); plane(.8, 1.1, R.posterM, -4.0, 2.0, 1.7, Math.PI / 2);
  R.clockM = texMat("clock"); const ck = new THREE.Mesh(new THREE.CircleGeometry(.2, 32), R.clockM); ck.position.set(-4.0, 2.55, -.4); ck.rotation.y = Math.PI / 2; R.add(ck);
  // the app tile that bursts into voxels and re-forms as the open-source tool
  const tg = new THREE.Group(); tg.position.copy(TILE); R.add(tg); R.tileG = tg;
  const tgeo = new RoundedBoxGeometry(.56, .56, .08, 3, .06);
  R.oldM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .4, emissive: 0xffffff, emissiveIntensity: .35 });
  R.newM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .4, emissive: 0xffffff, emissiveIntensity: .35 });
  R.oldT = new THREE.Mesh(tgeo, R.oldM); R.newT = new THREE.Mesh(tgeo, R.newM); tg.add(R.oldT, R.newT);
  R.cubes = new THREE.InstancedMesh(new THREE.BoxGeometry(.06, .06, .06), new THREE.MeshStandardMaterial({ roughness: .5, emissive: 0x222222 }), 128);
  R.cubes.frustumCulled = false; tg.add(R.cubes);
  for (let i = 0; i < 128; i++) R.cubes.setColorAt(i, tmpC.set(0xffffff));
  R.tileGlow = new THREE.PointLight(0xffffff, 0, 3, 1.8); tg.add(R.tileGlow); R.tileGlow.position.z = .3;
}
PARENT = scene;

// ---------------------------------------------------------------- the cast: Maya (a new top every chapter), Noah
const MAYA_BASE = { skin: "#C68E68", hair: "#2A1A12", style: "bun", pants: "#2E3A55", shoe: "#F4EFE6", lash: true, earring: true, brow: "#2A1A12" };
const MAYA = [
  makeChar({ ...MAYA_BASE, id: "maya0", top: "#7E5BB0", topStyle: "hoodie", pants: "#5B5650" }, R),   // day 1-8: the purple hoodie
  makeChar({ ...MAYA_BASE, id: "maya1", top: "#E8735A", topStyle: "tee" }, R),                        // day 12-25
  makeChar({ ...MAYA_BASE, id: "maya2", top: "#2E4057", topStyle: "hoodie" }, R),                     // day 29, night
  makeChar({ ...MAYA_BASE, id: "maya3", top: "#F2B33D", topStyle: "blazer" }, R),                     // day 30, launch
];
MAYA.forEach((P, k) => { P.seed = 1.3 + k * .01; });
const NOAH = makeChar({ id: "noah", skin: "#8E5E40", hair: "#1E1B18", style: "short", beard: "#1E1B18", glasses: "#1E1B18", top: "#2F6F5E", topStyle: "hoodie", pants: "#3A3A3A", shoe: "#FFFDF8" }, R);
NOAH.seed = 4.7;
// props held: Noah's mug (day 1), his phone torch (day 29)
const MUG = new THREE.Group(); R.add(MUG); cyl(.05, .045, .1, mat(0xE8735A), 0, 0, 0, 12, { parent: MUG });
const TORCH = new THREE.Group(); R.add(TORCH); box(.07, .14, .01, mat(0x15171C), 0, 0, 0, { parent: TORCH }); box(.02, .02, .012, glow(0xFFFFFF), 0, .05, -.006, { parent: TORCH });
const torchL = new THREE.SpotLight(0xEAF2FF, 0, 7, .6, .5, 1.5); TORCH.add(torchL); TORCH.add(torchL.target); torchL.target.position.set(0, 0, -2);

// ---------------------------------------------------------------- looks per scene
const LOOKS = [
  { city: "cityDawn", bg: 0x0A0E18, fog: 0x0A0E18, hs: 0x5468A0, hg: 0x1A1A24, hi: 1.1, sun: 0x9FB8FF, si: .8, sd: [.3, .7, -.9], warm: 0, cool: .4, sat: .86, con: .1, vig: .55 },
  { city: "cityDay", bg: 0xBFD8F0, fog: 0xBFD8F0, hs: 0xEAF4FF, hg: 0xD6C9B0, hi: .95, sun: 0xFFF0D8, si: 2.6, sd: [.35, .8, -.9], warm: .1, cool: 0, sat: 1.06, con: .06, vig: .36 },
  { city: "cityGold", bg: 0xF0C890, fog: 0xF0C890, hs: 0xFFE6C8, hg: 0xC9A27A, hi: .85, sun: 0xFFC890, si: 2.4, sd: [-.25, .5, -.9], warm: .3, cool: 0, sat: 1.08, con: .08, vig: .4 },
  { city: "cityStorm", bg: 0x05070C, fog: 0x05070C, hs: 0x5A6A98, hg: 0x22222C, hi: .75, sun: 0x9FB0E0, si: .45, sd: [.3, .7, -.9], warm: 0, cool: .45, sat: .8, con: .12, vig: .62 },
  { city: "cityDay", bg: 0xCFE4F6, fog: 0xCFE4F6, hs: 0xF4FAFF, hg: 0xE0D2BA, hi: 1.05, sun: 0xFFF6E4, si: 2.9, sd: [.45, .85, -.85], warm: .12, cool: 0, sat: 1.1, con: .06, vig: .32 },
];

// ---------------------------------------------------------------- cue times
const SW = C.sw;                      // the eight app swaps (tile burst times)
const who = (t, name) => C.who.some((w, k) => w === name && t > L[k] - .05 && t < E[k] + .02);
const swapAt = (t) => { let k = -1; for (let i = 0; i < SW.length; i++) if (t > SW[i] - 1.0) k = i; return k; };

// ---------------------------------------------------------------- the shot list: [start, {p0, p1, l0, l1, fov, fov1, ap, d, d1}]
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const HEAD = v(CHAIR.x, 1.52, CHAIR.z);
const FACE = { p0: v(-1.85, 1.62, -.6), l0: HEAD, fov: 38, ap: .25, d: 2.83, d1: 2.54 };          // Maya at the desk, from the room
const OTS = { p0: v(-.72, 1.8, -3.62), p1: v(-.8, 1.76, -3.5), l0: v(-.78, 1.2, -1.9), fov: 38, ap: .12 };   // behind her, to the monitor
const TA = { p0: v(-1.05, 1.85, .95), p1: v(-1.05, 1.86, .6), l0: v(-1.05, 1.8, -2.1), fov: 54, ap: .05 };     // the tile and her face, from the room
const TB = { p0: v(-3.0, 1.7, .4), p1: v(-2.85, 1.72, .1), l0: v(-1.0, 1.78, -2.1), fov: 52, ap: .05 };   // the tile, from the left
const LAPS = { p0: v(-2.55, 1.48, -3.4), p1: v(-2.5, 1.42, -3.3), l0: v(-2.05, .9, -1.95), fov: 40, ap: .2 }; // behind her left shoulder, the laptop
const NOAH_T = (x, z) => ({ l0: v(x, 1.68, z), fov: 40, ap: .25 });
const SHOTS = [
  // s0, dawn: her phone lights up; she sits up; runs to the desk; the wall of cancellations; locked; Noah at the door
  [0, { p0: v(1.35, 1.7, -.8), p1: v(1.45, 1.6, -1.05), l0: v(2.6, .75, -3.0), fov: 46, ap: .05 }],
  [L[0] + .2, { p0: v(1.3, 1.0, -3.1), p1: v(1.33, .92, -3.2), l0: v(1.42, .565, -3.52), fov: 40, ap: .35 }],
  [L[1] - .15, { p0: v(2.4, 1.55, -.4), l0: v(2.85, 1.42, -2.45), fov: 40, ap: .2, d: 3.04, d1: 2.75 }],
  [L[2] - .25, { p0: v(2.6, 2.2, 2.6), p1: v(1.9, 2.0, 2.0), l0: v(.6, 1.0, -2.4), l1: v(-1.0, 1.1, -2.6), fov: 54, ap: .02 }],
  [L[2] + 3.1, OTS],
  [L[3] - .1, { ...OTS, p0: v(-.8, 1.76, -3.5), p1: v(-.85, 1.68, -3.3), fov: 34 }],
  [L[4] - .15, FACE],
  [E[4] + .25, { p0: v(-1.2, 1.7, -2.0), p1: v(-1.0, 1.7, -1.8), l0: v(3.9, 1.3, -.3), fov: 46, ap: .04 }],
  [L[5] - .15, { p0: v(2.3, 1.72, .3), ...NOAH_T(3.62, -.3), d: 2.90, d1: 2.61 }],
  [L[6] - .15, { p0: v(.6, 1.78, -1.05), l0: HEAD, fov: 40, ap: .25, d: 2.75, d1: 2.46 }],
  [L[7] - .2, { p0: v(2.7, 2.1, 2.7), p1: v(2.4, 2.0, 2.4), l0: v(.9, 1.2, -1.3), fov: 58, ap: .02 }],
  // s1, days 1-8: Adobe, Canva, CapCut
  [CU[0], TA], [SW[0] + 1.0, OTS],
  [SW[1] - .85, TB], [SW[1] + 1.0, OTS],
  [SW[2] - .85, TA], [SW[2] + 1.0, OTS],
  [L[8] - .1, FACE],
  // s2, days 12-25: Mailchimp, Hootsuite, Linktree, Notion
  [CU[1], { p0: v(3.0, 2.4, 3.6), p1: v(2.8, 2.3, 3.3), l0: v(-1.3, 1.1, -2.3), fov: 56, ap: .01 }],
  [L[9] + .5, { ...FACE, d: 2.61, d1: 2.39 }],
  [L[10] - .6, { p0: v(1.2, 1.5, 1.6), ...NOAH_T(1.3, 3.0), l0: v(1.3, 1.45, 3.0), d: 2.90, d1: 2.61 }],
  [SW[3] - .8, TB], [SW[3] + 1.05, OTS],
  [SW[4] - .85, TA], [SW[4] + .95, OTS],
  [SW[5] - .85, TB], [SW[5] + .95, OTS],
  [SW[6] - .85, TA], [SW[6] + .95, OTS],
  [L[11] - .1, { p0: v(-1.0, 1.65, -.4), l0: v(-1.35, 1.65, -2.55), fov: 42, ap: .2, d: 3.48, d1: 3.19 }],
  // s3, day 29, a storm: the night before launch; lightning; the power dies; an AI on her own laptop
  [CU[2], { p0: v(1.6, 2.2, 1.4), p1: v(1.2, 2.05, 1.0), l0: v(-1.3, 1.2, -2.6), fov: 50, ap: .02 }],
  [L[12] - .1, FACE],
  [E[12] + .35, { p0: v(.7, 1.6, -2.4), p1: v(.6, 1.62, -2.6), l0: v(-1.6, 1.85, -4.0), fov: 56, ap: .02 }],
  [E[12] + 1.0, LAPS],
  [L[13] + .35, { ...FACE, d: 2.54, d1: 2.32 }],
  [L[14] - .1, { p0: v(-1.75, 1.72, -1.95), ...NOAH_T(-.25, -2.5), d: 2.75, d1: 2.54 }],
  [SW[7] - .8, TA], [SW[7] + 1.0, LAPS],
  [L[15] - .15, { ...FACE, d: 2.46, d1: 2.25 }],
  // s4, day 30, launch: orders; "what did it cost?"; zero; resubscribe? no thanks; she turns to us
  [CU[3], { p0: v(-3.2, 2.3, 2.8), p1: v(-2.9, 2.2, 2.4), l0: v(-1.0, 1.1, -2.3), fov: 56, ap: .01 }],
  [CU[3] + 1.3, OTS],
  [L[16] - .1, { p0: v(.1, 1.75, .6), ...NOAH_T(-.4, -1.72), l0: v(-.4, 1.62, -1.72), d: 3.3, d1: 3.0 }],
  [L[17] - .1, { p0: v(-1.45, 1.65, -.3), l0: v(CHAIR.x, 1.66, CHAIR.z), fov: 40, ap: .25, d: 2.68, d1: 2.39 }],
  [L[18] - .15, OTS],
  [L[19] - .1, { p0: v(-1.45, 1.65, -.3), l0: HEAD, fov: 40, ap: .25, d: 2.61, d1: 2.39 }],
  [E[19] + .35, { p0: v(-1.5, 1.58, -.6), p1: v(-1.5, 1.56, -.9), l0: HEAD, fov: 40, ap: .2 }],
];
function shotAt(t) {
  let i = 0; while (i + 1 < SHOTS.length && t >= SHOTS[i + 1][0]) i++;
  const [a, s] = SHOTS[i], b = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR;
  const u = sm(clamp((t - a) / Math.max(.1, b - a)));
  let p = (s.p1 ? V.lerpVectors(s.p0, s.p1, u) : V.copy(s.p0)).clone(); const l = s.l1 ? V2.lerpVectors(s.l0, s.l1, u).clone() : s.l0.clone();
  if (s.d) { const d = lerp(s.d, s.d1 ?? s.d, u); p = l.clone().add(p.sub(l).normalize().multiplyScalar(d)); }
  return { i, a, b, u, p, l, fov: lerp(s.fov, s.fov1 ?? s.fov, u), ap: s.ap, f: s.f ?? p.distanceTo(l) };
}

// ---------------------------------------------------------------- poses
const ry2 = (fx, fz, tx, tz) => Math.atan2(tx - fx, tz - fz);       // heading from (fx,fz) towards (tx,tz)
const SITY = -.21;
const sitP = (ry, o = {}) => pose({ x: CHAIR.x, y: SITY, z: CHAIR.z, ry, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.35, .1, .5], [.35, .1, .5]], ...o });
const typeA = (t, k = 1) => [[1.22 + .05 * Math.sin(t * 15) * k, .14, .55 + .08 * Math.sin(t * 13 + 1) * k], [1.22 + .05 * Math.sin(t * 14 + 2) * k, .14, .55 + .08 * Math.sin(t * 12 + 3) * k]];
const PANIC = [[2.75, .62, 2.5], [2.75, .62, 2.5]], CHEER = [[2.95, .4, .25], [2.95, .4, .25]];
const FACING_DESK = 0;
function along(pts, u) {
  const seg = []; let tot = 0; for (let q = 0; q < pts.length - 1; q++) { const ll = Math.hypot(pts[q + 1][0] - pts[q][0], pts[q + 1][1] - pts[q][1]); seg.push(ll); tot += ll; }
  let d = tot * clamp(u), q = 0; while (q < seg.length - 1 && d > seg[q]) { d -= seg[q]; q++; }
  const f = clamp(d / seg[q]), A = pts[q], B = pts[q + 1];
  return { x: lerp(A[0], B[0], f), z: lerp(A[1], B[1], f), ry: Math.atan2(B[0] - A[0], B[1] - A[1]), len: tot };
}
const swivel = (P, ry) => { R.chair.rotation.y = ry; };
function holdAt(P, k, obj, off = [0, -.1, .02]) {
  P.root.updateMatrixWorld(true);
  P.hand[k].getWorldPosition(obj.position);
  obj.quaternion.setFromEuler(EU.set(0, P.root.rotation.y, 0));
  obj.position.add(V.set(...off).applyQuaternion(obj.quaternion));
}

function updMaya(t, s) {
  MAYA.forEach((P, k) => { P.root.visible = false; });
  const P = MAYA[s === 0 || s === 1 ? 0 : s === 2 ? 1 : s === 3 ? 2 : 3];
  let p, f = { eyes: "open", mouth: "smile", brows: "flat", talk: who(t, "maya") };
  let chairRy = FACING_DESK;
  if (s === 0) {
    const up = ss(t, L[1] - .5, L[1] + .1);                         // sits up in bed on "What?"
    if (t < L[2] - .25) {
      p = pose({ x: BEDP.x, y: -.16, z: -2.45, ry: 0, lean: lerp(-1.42, -.08, up), l: [[1.5, 0], [1.5, 0]], a: [[lerp(.2, .5, up), .12, lerp(.3, .9, up)], [lerp(.2, .5, up), .12, lerp(.3, .9, up)]], hp: lerp(-.05, .05, up) });
      f = t < .55 ? { eyes: "closed", mouth: "flat", noblink: true } : t < L[1] - .4 ? { eyes: "half", mouth: "flat", brows: "worry" } : { eyes: "wide", mouth: "o", brows: "worry", talk: who(t, "maya"), noblink: true };
    } else if (t < L[2] + 2.45) {                                   // she runs to the desk
      const u = clamp((t - (L[2] - .25)) / 2.7), a = along([[1.6, -2.3], [.6, -3.05], [-.4, -3.1], [-1.35, -3.05]], u);
      p = walk(pose({ x: a.x, z: a.z, ry: a.ry }), (t - L[2]) * 9.5, 1.15);
      f = { eyes: "wide", mouth: "o", brows: "worry", noblink: true };
    } else {
      const sit = ss(t, L[2] + 2.45, L[2] + 3.0);
      const turn = ss(t, L[6] - .6, L[6] - .1);                      // swivels to the door for "Free?"
      const ry = lerp(FACING_DESK, ry2(CHAIR.x, CHAIR.z, 3.62, -.3), turn); chairRy = ry;
      p = mixP(pose({ x: -1.35 - .15 * sit, z: -3.05 + .25 * sit, ry: -Math.PI / 2 }), sitP(ry, { a: turn > .5 ? [[.45, .15, .9], [.45, .15, .9]] : typeA(t, t < L[3] ? 1 : .3) }), sit);
      if (t > L[4] - .2 && t < E[4] + .4) p.a = [[1.25, -.12, 2.35], [1.25, -.12, 2.35]];   // hands to her mouth
      f = t < L[6] - .3 ? { eyes: "wide", mouth: t > L[4] - .2 ? "sad" : "flat", brows: "worry", talk: who(t, "maya") } : { eyes: "open", mouth: "smile", brows: "raise1", talk: who(t, "maya") };
      if (t > L[7] - .2) f = { eyes: "open", mouth: "smile", brows: "up" };
    }
  } else if (s === 1) {
    const look = bump(t, L[8] + .6, CU[1] + .5, .4);                 // turns to Noah, delighted
    p = sitP(FACING_DESK, { a: typeA(t, .8), hy: .9 * look, hp: -.05 });
    const yay = SW.slice(0, 3).some((b) => t > b + .6 && t < b + 1.6);
    if (yay) p.a = [[1.5, .2, .4], [1.5, .2, .4]];
    f = { eyes: yay || t > L[8] ? "happy" : "open", mouth: t > L[8] - .2 ? "grin" : yay ? "grin" : "smile", brows: "up", talk: who(t, "maya") };
  } else if (s === 2) {
    const stand = ss(t, L[11] - .6, L[11] + .1);
    const sat = sitP(FACING_DESK, { a: typeA(t, t < L[9] ? 1 : .4) });
    if (t > L[9] && t < E[9]) sat.a = [[1.9, .35, 2.2], [1.9, .35, 2.2]];       // head in hands
    const st = pose({ x: -1.35, z: -2.55, ry: .25, a: CHEER, hp: -.1 });
    p = mixP(sat, st, stand); chairRy = FACING_DESK;
    const yay = SW.slice(3, 7).some((b) => t > b + .6 && t < b + 1.5);
    if (yay && stand < .1) p.a = [[1.5, .2, .4], [1.5, .2, .4]];
    f = t < SW[3] ? { eyes: "half", mouth: "flat", brows: "angry", talk: who(t, "maya") } : { eyes: yay || stand > .5 ? "happy" : "open", mouth: stand > .5 ? "grin" : "smile", brows: "up", talk: who(t, "maya") };
  } else if (s === 3) {
    p = sitP(FACING_DESK, { a: typeA(t, t < C.cut ? .7 : 0) });
    if (t > C.cut + .2 && t < L[14] + .4) p.a = PANIC;
    if (t > L[14] + .4) { p.a = [[1.0, .12, .7], [1.0, .12, .7]]; p.hy = -.45; p.hp = .3; }   // leans to the laptop
    f = t < C.cut ? { eyes: "half", mouth: "flat", brows: "worry", talk: who(t, "maya") } : t < SW[7] + .6 ? { eyes: "wide", mouth: "o", brows: "worry", talk: who(t, "maya"), noblink: true } : { eyes: "wide", mouth: "smile", brows: "up", talk: who(t, "maya") };
  } else {
    const toN = ry2(CHAIR.x, CHAIR.z, -.4, -1.72);
    const toCam = 0;
    const tN = ss(t, L[16] - .3, L[16] + .3) * (1 - ss(t, L[18] - .5, L[18] - .1));
    const tC = ss(t, E[19] + .3, E[19] + 1.0);
    let ry = lerp(lerp(FACING_DESK, toN, tN), toCam, tC); chairRy = ry;
    p = sitP(ry, { a: tN > .5 || tC > .5 ? [[.45, .15, .9], [.45, .15, .9]] : typeA(t, .6) });
    if (t > CU[3] + .2 && t < L[16] - .4) p.a = CHEER;                          // the orders roll in
    if (t > L[19] + .1 && t < L[19] + .6) p.a = [[1.25, .12, .4], [.4, .1, .5]];  // the click
    if (tC > .5) { p.a = [[.4, .1, .6], [2.2, -.2, 1.6]]; p.a[1][1] = .1 + .25 * Math.sin(t * 8); }   // a small wave
    f = { eyes: t > L[17] && t < E[17] ? "happy" : "open", mouth: t > L[17] && t < E[17] + .3 ? "laugh" : "smile", brows: "up", talk: who(t, "maya") };
    if (t > CU[3] + .2 && t < L[16] - .4) f = { eyes: "happy", mouth: "laugh", brows: "up" };
  }
  swivel(P, chairRy);
  placeChar(P, true, idle(p, t, P.seed), f);
}

function updNoah(t, s) {
  let p, vis = true, f = { eyes: "open", mouth: "smile", brows: "flat", talk: who(t, "noah") };
  MUG.visible = false; TORCH.visible = false; torchL.intensity = 0;
  if (s === 0) {
    vis = t > E[4] + .6;
    if (t < L[7] - .2) p = pose({ x: 3.62, z: -.3, ry: -Math.PI / 2, tw: .12, a: [[.75, .1, 1.5], [.1, .15, .2]], hr: .06 });
    else { const u = clamp((t - (L[7] - .2)) / (CU[0] + .25 - (L[7] - .2))), a = along([[3.62, -.3], [1.6, -1.0], [.8, -2.2], [.4, -2.45]], u); p = walk(pose({ x: a.x, z: a.z, ry: a.ry, a: [[.75, .1, 1.5], [.1, .15, .2]] }), t * 9, 1); p.a[0] = [.75, .1, 1.5]; }
    f = { eyes: "open", mouth: t > L[7] - .2 ? "grin" : "smirk", brows: "flat", talk: who(t, "noah") };
    if (vis) { MUG.visible = true; }
  } else if (s === 1) {
    p = pose({ x: .4, z: -2.45, ry: -1.13, a: [[.75, .1, 1.5], [.1, .15, .2]] });
    if (SW.slice(0, 3).some((b) => t > b - .9 && t < b + .3)) { p.a[1] = [1.45, .05, .1]; }    // points at the screen
    MUG.visible = true; f = { eyes: "open", mouth: "smirk" };
  } else if (s === 2) {
    p = pose({ x: 1.3, y: -.185, z: 3.0, ry: Math.PI, l: [[1.5, 1.5], [1.5, 1.5]], a: typeA(t, .6), hp: .12 });
    if (t > L[10] - .4 && t < E[10] + .3) { p.hy = -.5; p.hp = 0; p.a = [[1.0, .12, .5], [.9, .12, .4]]; }   // looks over to her
    f = { eyes: "open", mouth: "smile", brows: "flat", talk: who(t, "noah") };
  } else if (s === 3) {
    vis = t > L[14] - 1.6;
    const inT = ss(t, L[14] - 1.6, L[14] - .5);
    p = walk(pose({ x: lerp(1.6, -.25, inT), z: lerp(-1.0, -2.5, inT), ry: -1.22, a: [[.2, .1, .3], [1.5, .1, .6]] }), t * 8.5, 1 - inT);
    p.a[1] = [1.5, .1, .6];
    TORCH.visible = vis; torchL.intensity = vis ? 3.5 : 0;
    f = { eyes: "open", mouth: "smile", brows: "flat", talk: who(t, "noah") };
  } else {
    p = pose({ x: -.4, y: .05, z: -1.72, ry: .15, l: [[1.45, 1.25], [1.45, 1.35]], a: [[.35, .3, .25], [.35, .3, .25]], hy: -.45 });
    if (t > CU[3] + .2 && t < L[16] - .4) p.a = CHEER;
    f = { eyes: t > L[17] && t < E[17] + .3 ? "happy" : "open", mouth: t > L[17] && t < E[17] + .3 ? "laugh" : "grin", brows: "up", talk: who(t, "noah") };
  }
  NOAH.root.visible = vis;
  if (!vis) return;
  placeChar(NOAH, true, idle(p, t, NOAH.seed), f);
  if (MUG.visible) holdAt(NOAH, 0, MUG, [0, -.08, .06]);
  if (TORCH.visible) { holdAt(NOAH, 1, TORCH, [0, -.05, .08]); TORCH.rotation.x -= .2; }
}

// ---------------------------------------------------------------- the app tile: burst into voxels, re-form as the open-source tool
const TILE_COL = C.tileCol;           // [[old hex, new hex], ...]
let tileK = -2;
const cubeHome = Array.from({ length: 64 }, (_, i) => v(((i % 8) - 3.5) * .066, (Math.floor(i / 8) - 3.5) * .066, 0));
function updTile(t) {
  const G = R.tileG; R.tileGlow.intensity = 0;
  const k = swapAt(t);
  if (k < 0 || t > SW[k] + 2.4) { G.visible = false; return; }
  const b = SW[k], nb = k + 1 < SW.length ? SW[k + 1] - 1.0 : b + 2.4;
  G.visible = true;
  if (k !== tileK) {
    tileK = k;
    setMap(R.oldM, TEX["tOld" + k]); setMap(R.newM, TEX["tNew" + k]);
    R.oldM.emissiveMap = TEX["tOld" + k] || null; R.newM.emissiveMap = TEX["tNew" + k] || null; R.oldM.needsUpdate = R.newM.needsUpdate = true;
    for (let i = 0; i < 128; i++) R.cubes.setColorAt(i, tmpC.set(TILE_COL[k][i < 64 ? 0 : 1]).offsetHSL(0, 0, (hash(i * 3.1) - .5) * .12));
    R.cubes.instanceColor.needsUpdate = true;
  }
  // the old tile pops in, shakes, then bursts
  const pop = clamp((t - (b - 1.0)) / .25), back = 1 + 2.2 * (pop - 1) ** 3 + 1.2 * (pop - 1) ** 2;
  R.oldT.visible = t < b; R.oldT.scale.setScalar(Math.max(.001, pop < 1 ? back : 1));
  const shk = ss(t, b - .45, b) * .03;
  R.oldT.position.set(shk * Math.sin(t * 70), shk * Math.sin(t * 61), 0); R.oldT.rotation.set(0, 0, shk * 2 * Math.sin(t * 50));
  R.oldM.emissiveIntensity = .35 + ss(t, b - .45, b) * .6;
  // the new tile, after its cubes arrive
  const pn = clamp((t - (b + .75)) / .25), backN = 1 + 2.2 * (pn - 1) ** 3 + 1.2 * (pn - 1) ** 2;
  const out = ss(t, Math.min(nb, b + 2.4) - .3, Math.min(nb, b + 2.4));
  R.newT.visible = t > b + .75 && out < 1; R.newT.scale.setScalar(Math.max(.001, (pn < 1 ? backN : 1) * (1 - out)));
  R.newT.rotation.y = .25 * Math.sin((t - b) * 2.2) * (1 - out);
  const dim = k === 7 ? .3 : 1; R.newM.emissiveIntensity = (.35 + .9 * pulse(t, b + .85, .18)) * dim;
  R.tileGlow.color.set(TILE_COL[k][1]); R.tileGlow.intensity = (3.5 * pulse(t, b + .85, .25) + 2.2 * pulse(t, b + .05, .15)) * (k === 7 ? .35 : 1);
  // the cubes: 0-63 fly out from the old tile, 64-127 converge into the new one
  for (let i = 0; i < 128; i++) {
    const old = i < 64, j = i % 64, h0 = cubeHome[j];
    let sc = 0;
    if (old) {
      const u = t - b;
      if (u > 0 && u < 1.1) {
        const vx = .15 + hash(j * 1.3) * .5, vy = (hash(j * 2.7) - .3) * 2.2, vz = (hash(j * 4.1) - .5) * 3.0;
        V.set(h0.x + vz * u * .9, h0.y + vy * u - 2.2 * u * u, h0.z + vx * u);
        sc = 1 - ss(u, .6, 1.1);
        EU.set(u * 9 * hash(j), u * 7 * hash(j * 5), 0);
      }
    } else {
      const u = clamp((t - (b + .1)) / .65);
      if (t > b + .1 && t < b + .85) {
        const e = 1 - (1 - u) ** 3;
        const sx = (hash(j * 5.3) - .5) * 1.8, sy = (hash(j * 6.1) - .5) * 1.4, sz = .1 + hash(j * 7.7) * .35;
        V.set(lerp(sx, h0.x, e), lerp(sy, h0.y, e), lerp(sz, h0.z, e));
        sc = ss(u, 0, .3);
        EU.set((1 - e) * 6 * hash(j), (1 - e) * 5, 0);
      }
    }
    Q.setFromEuler(EU); M4.compose(V, Q, S.set(sc, sc, sc)); R.cubes.setMatrixAt(i, M4);
  }
  R.cubes.instanceMatrix.needsUpdate = true;
}

// ---------------------------------------------------------------- screens
function monKey(t, s) {
  if (s === 0) return t < L[2] + 2.3 ? "off" : t < L[3] + .2 ? "cancel" : "locked";
  if (s === 1) return t < SW[0] + .2 ? "locked" : t < SW[1] + .2 ? "gimp" : t < SW[2] + .2 ? "penpot" : "shotcut";
  if (s === 2) return t < SW[3] + .2 ? "mailLocked" : t < SW[4] + .2 ? "listmonk" : t < SW[5] + .2 ? "postiz" : t < SW[6] + .2 ? "linkstack" : "appflowy";
  if (s === 3) return t < C.cut ? "doc" : "off";
  return t < L[18] - .3 ? "orders" : t < C.nothanks + .5 ? "resub" : "calm";
}
function lapKey(t, s) {
  if (s === 3) return t < C.cut ? "lapDoc" : t < SW[7] + .3 ? "nowifi" : "ollama";
  if (s === 4) return "lapWall";
  return s === 0 && t < L[2] + 2.3 ? "lapOff" : "lapWall";
}
function screens(t, s) {
  const mk = monKey(t, s), lk = lapKey(t, s);
  if (mk === "listmonk") setMap(R.monM, DYN.listmonk(clamp((t - (E[10] - .6)) / 2.2)));
  else if (mk === "postiz") setMap(R.monM, DYN.postiz(clamp((t - (SW[4] + .2)) / 1.6)));
  else if (mk === "orders") setMap(R.monM, DYN.orders(clamp((t - (CU[3] + .1)) / (L[16] - CU[3]))));
  else if (mk === "resub") setMap(R.monM, DYN.resub(t > C.nothanks ? 2 : t > L[19] - .3 ? 1 : 0));
  else if (TEX["m_" + mk]) setMap(R.monM, TEX["m_" + mk]);
  if (lk === "ollama") setMap(R.lapM, DYN.ollama(clamp((t - (SW[7] + .35)) / (CU[3] - SW[7] - .5))));
  else if (TEX["l_" + lk]) setMap(R.lapM, TEX["l_" + lk]);
  return { mk, lk };
}

// ---------------------------------------------------------------- per frame: the loft
let SHAKE = 0;
function updLoft(t, s) {
  const Lk = LOOKS[s];
  if (TEX[Lk.city]) setMap(R.cityM, TEX[Lk.city]);
  R.rainM.opacity = s === 3 ? .6 : 0;
  if (TEX.rain) TEX.rain.offset.set(0, -t * 1.4);
  R.blanket.scale.y = .36; R.blanket.position.y = .6;
  // the door: opens for Noah on day 1
  R.door.rotation.y = s === 0 ? -1.35 * ss(t, E[4] + .5, E[4] + 1.1) : 0;
  let kn = 0; if (s === 0) for (const a of [0, .26, .52]) kn += pulse(t, C.knock + a, .045);
  R.door.position.x = 4.02 - .006 * kn;
  PL[7].position.set(3.3, 2.0, -.3); PL[7].color.set(0xFFD9A8); PL[7].intensity = s === 0 ? 3.0 * ss(t, E[4] + .5, E[4] + 1.0) : 0; PL[7].distance = 5;
  // lights
  const { mk, lk } = screens(t, s);
  const monOn = mk !== "off", lapOn = lk !== "lapOff";
  PL[0].position.set(MON.x - .1, MON.y + .05, MON.z - .45); PL[0].color.set(mk === "cancel" || mk === "locked" || mk === "mailLocked" ? 0xFF6A5A : 0xCFE0FF);
  PL[0].intensity = monOn ? (s === 0 || s === 3 ? 2.2 : .8) : 0; PL[0].distance = 3.2;
  const lampOn = (s === 3 && t < C.cut) || s === 0 && t > L[2] + 2.4;
  let flick = 1; if (s === 3 && t > C.cut - .15 && t < C.cut + .25) flick = hash(Math.floor(t * 30)) > .5 ? 1 : 0;
  PL[1].position.set(-.32, 1.12, -2.4); PL[1].color.set(0xFFC98A); PL[1].intensity = lampOn ? 2.6 * flick : 0; PL[1].distance = 4.5;
  R.lampM.emissiveIntensity = lampOn ? 1.6 * flick : 0;
  const ringOn = s === 1 || s === 2 || s === 4;
  PL[2].position.set(-2.55, 1.55, -2.2); PL[2].color.set(0xFFF4E0); PL[2].intensity = ringOn ? 1.0 : 0; PL[2].distance = 3; R.ringM.emissiveIntensity = ringOn ? 1.2 : .1;
  PL[3].position.set(1.42, .75, -3.45); PL[3].color.set(0xBFD8FF); PL[3].intensity = s === 0 && t < L[2] ? 3.0 * (t > .2 ? 1 : 0) : 0; PL[3].distance = 3.5;
  setMap(R.phoneM, TEX[s === 0 && t > .2 && t < L[2] + 2 ? "phoneNote" : "phoneOff"]);
  // lightning on day 29
  let fl = 0; if (s === 3) for (const a of C.flash) fl = Math.max(fl, pulse(t, a, .05) + .6 * pulse(t, a + .16, .04));
  PL[4].position.set(-1.9, 2.0, -3.5); PL[4].color.set(0xDDE6FF); PL[4].intensity = 14 * fl; PL[4].distance = 9;
  if (fl > .1) setMap(R.cityM, TEX.cityFlash);
  PL[5].position.set(0, 2.9, .5); PL[5].color.set(0xFFE6C4); PL[5].intensity = s === 4 ? 1.2 : s === 1 || s === 2 ? .7 : s === 0 ? .7 : .35; if (s === 0 || s === 3) PL[5].color.set(0x8FA4D8); PL[5].distance = 9;
  R.flM.emissiveIntensity = s === 2 ? .8 : 0;
  PL[6].position.set(-1.95, 1.05, -2.25); PL[6].color.set(lk === "ollama" ? 0xBFF5D0 : 0xCFE0FF); PL[6].intensity = lapOn && (s === 3 || s === 0) ? 1.0 : 0; PL[6].distance = 2.2;
  if (s === 0 && t < L[2]) { PL[6].position.set(2.3, 1.9, -1.0); PL[6].color.set(0x9FB4E8); PL[6].intensity = 2.2; PL[6].distance = 4; }
  if (s === 3 && t > C.cut) { hemi.intensity *= .55; }
  if (s === 3 && t > L[14] - 1.6) { PL[3].position.set(-.9, 1.8, -1.7); PL[3].color.set(0xBFD4F0); PL[3].intensity = 1.6; PL[3].distance = 3; }
  SHAKE = Math.max(SHAKE, .1 * kn, s === 3 ? .5 * pulse(t, C.flash[1] + .1, .2) : 0);
  R.monM.color.setScalar(s === 1 || s === 2 || s === 4 ? .92 : .8); R.lapM.color.setScalar(.85);
  updMaya(t, s); updNoah(t, s); updTile(t);
  return fl;
}

// ---------------------------------------------------------------- the frame
function renderAt(t) {
  NOW = t; SHAKE = 0;
  const s = sceneOf(t), Lk = LOOKS[s];
  for (const k in SET) SET[k].visible = true;
  scene.background = tmpC.set(Lk.bg).clone();
  scene.fog.color.set(Lk.fog); scene.fog.near = 40; scene.fog.far = 200;
  hemi.color.set(Lk.hs); hemi.groundColor.set(Lk.hg); hemi.intensity = Lk.hi;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  for (const l of PL) l.intensity = 0;
  const sh = shotAt(t);
  const fl = updLoft(t, s);
  const hand = .003, shk = SHAKE;
  camera.position.copy(sh.p).add(V.set(Math.sin(t * .9) * hand + shk * .03 * Math.sin(t * 61), Math.sin(t * 1.3 + 1) * hand + shk * .03 * Math.sin(t * 53), 0));
  camera.fov = sh.fov;
  const cv = window.STACK_COVER;
  if (cv && cv.cam) { camera.position.set(...cv.cam); sh.l.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix();
  camera.up.set(0, 1, 0); camera.lookAt(sh.l);
  if (shk) camera.rotateZ(shk * .015 * Math.sin(t * 47));
  scene.updateMatrixWorld(true);
  cocPass.uniforms.uF.value = sh.f; cocPass.uniforms.uAp.value = sh.ap;
  if (cv) { cocPass.uniforms.uAp.value = cv.ap ?? sh.ap; if (cv.focus) cocPass.uniforms.uF.value = cv.focus; }
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = Lk.warm; gu.uCool.value = Lk.cool; gu.uSat.value = Lk.sat; gu.uCon.value = Lk.con; gu.uVig.value = Lk.vig;
  gu.uFlash.value = fl * .35; gu.uCA.value = .0012 + shk * .004;
  gu.uTop.value = cv ? 0 : Math.max(1 - ss(t, 2.2, 2.9), ss(t, C.endc, C.endc + .6) * .9);
  gu.uDark.value = 0;
  bloom.strength = s === 3 ? .4 : s === 0 ? .32 : .28;
  // the sun comes through the window
  sun.target.position.set(-1.0, 0, -1.0); sun.position.copy(sun.target.position).add(S.set(...Lk.sd).normalize().multiplyScalar(30));
  Object.assign(sun.shadow.camera, { left: -7, right: 7, top: 7, bottom: -7, near: 1, far: 70 });
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT);
  renderer.render(scene, camera);
  renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures that need the fonts
const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`, SERIF = (w, f, it = false) => `${it ? "italic " : ""}${w} ${f}px Garamond, serif`;
const text = (w, h, draw) => pix(w, h, draw, false);
function wrapText(g, s, x, y, maxW, lh) { const ws = s.split(" "); let line = ""; for (const wd of ws) { const tst = line ? line + " " + wd : wd; if (g.measureText(tst).width > maxW && line) { g.fillText(line, x, y); line = wd; y += lh; } else line = tst; } g.fillText(line, x, y); return y; }
const SW_ = 1280, SH_ = 744;
// an app window filling the monitor: a title bar with the app's name, then the content
function app(title, accent, draw, o = {}) {
  return text(o.w || SW_, o.h || SH_, (g, w, h) => {
    g.fillStyle = o.bg || "#F4F5F8"; g.fillRect(0, 0, w, h);
    g.fillStyle = o.bar || "#1E2230"; g.fillRect(0, 0, w, 64);
    for (let k = 0; k < 3; k++) { g.fillStyle = ["#FF5F57", "#FEBC2E", "#28C840"][k]; g.beginPath(); g.arc(30 + k * 26, 32, 8, 0, 7); g.fill(); }
    g.fillStyle = accent; rr(g, 120, 16, 32, 32, 8); g.fill();
    g.fillStyle = "#FFFFFF"; g.font = FT(800, 30); g.textAlign = "left"; g.textBaseline = "middle"; g.fillText(title, 166, 33);
    if (o.tag) { g.font = FT(800, 20); const tw = g.measureText(o.tag).width + 28; g.fillStyle = o.tagC || "#28C840"; rr(g, w - tw - 24, 18, tw, 30, 15); g.fill(); g.fillStyle = "#0B0D12"; g.textAlign = "center"; g.fillText(o.tag, w - tw / 2 - 24, 34); }
    g.textBaseline = "alphabetic"; g.textAlign = "left";
    draw(g, w, h);
  });
}
const block = (g, x, y, w, h, c, r = 14) => { g.fillStyle = c; rr(g, x, y, w, h, r); g.fill(); };
const label = (g, s, x, y, f, c, al = "left", wt = 800) => { g.font = FT(wt, f); g.fillStyle = c; g.textAlign = al; g.fillText(s, x, y); g.textAlign = "left"; };
function candle(g, x, y, s, c = "#E8735A") {   // Maya's product: a candle in a jar
  block(g, x - 60 * s, y - 120 * s, 120 * s, 150 * s, "rgba(255,255,255,.55)", 24 * s);
  block(g, x - 52 * s, y - 70 * s, 104 * s, 92 * s, c, 18 * s);
  block(g, x - 64 * s, y - 138 * s, 128 * s, 26 * s, "#1E1B18", 8 * s);
  block(g, x - 40 * s, y - 50 * s, 80 * s, 40 * s, "#FFFDF8", 8 * s); label(g, "MAYA", x, y - 22 * s, 22 * s, "#1E1B18", "center");
  g.fillStyle = "#F2B33D"; g.beginPath(); g.ellipse(x, y - 160 * s, 9 * s, 18 * s, 0, 0, 7); g.fill();
}
const DYN = {};
function dyn(key, w, h, steps, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  let last = null;
  DYN[key] = (u) => { const q = Math.round(u * steps) / steps; if (q !== last) { last = q; draw(g, w, h, q); tx.needsUpdate = true; } return tx; };
}
function buildTextures() {
  // ---- the window: the city outside, per look
  const city = (sky, body, lit, rain = false) => text(1024, 580, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); sky.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let layer = 0; layer < 2; layer++) for (let i = 0; i < 26; i++) {
      const bw = 40 + hash(i * 7 + layer) * 60, bx = i * 42 - 20 + layer * 18, bh = (layer ? 120 : 200) + hash(i * 3.3 + layer * 9) * (layer ? 160 : 230), by = h - bh;
      g.fillStyle = layer ? body[1] : body[0]; g.fillRect(bx, by, bw, bh);
      for (let yy = by + 12; yy < h - 10; yy += 18) for (let xx = bx + 6; xx < bx + bw - 8; xx += 13) { const on = hash(xx * .7 + yy * 1.3 + layer) > (lit ? .55 : 2); g.fillStyle = on ? lit : (layer ? "rgba(255,255,255,.12)" : "rgba(255,255,255,.18)"); g.fillRect(xx, yy, 7, 9); }
    }
    if (rain) { g.fillStyle = "rgba(10,14,24,.35)"; g.fillRect(0, 0, w, h); }
  });
  TEX.cityDawn = city([[0, "#14193A"], [.6, "#3A3E6A"], [1, "#7A6A8A"]], ["#1E2240", "#2A2E52"], "#FFD9A0");
  TEX.cityDay = city([[0, "#6FA8E0"], [.7, "#B4D4F0"], [1, "#E4EEF6"]], ["#9DB0C4", "#B8C6D4"], null);
  TEX.cityGold = city([[0, "#E8A86A"], [.6, "#F4C890"], [1, "#FBE2B8"]], ["#B08A6A", "#C9A07A"], null);
  TEX.cityStorm = city([[0, "#070A14"], [.6, "#141A2C"], [1, "#222A40"]], ["#0C1020", "#141A2E"], "#FFD9A0", true);
  TEX.cityFlash = city([[0, "#8A9AC8"], [.6, "#B4C0E0"], [1, "#D0D8F0"]], ["#2A3050", "#3A4060"], "#FFFFFF");
  TEX.rain = text(256, 256, (g, w, h) => { g.clearRect(0, 0, w, h); for (let k = 0; k < 160; k++) { const x = hash(k) * w, y = hash(k * 3) * h, l = 10 + hash(k * 5) * 26; g.strokeStyle = `rgba(200,215,240,${.25 + hash(k * 7) * .35})`; g.lineWidth = 1.3; g.beginPath(); g.moveTo(x, y); g.lineTo(x - 2, y + l); g.stroke(); } for (let k = 0; k < 40; k++) { g.fillStyle = "rgba(220,230,250,.4)"; g.beginPath(); g.arc(hash(k * 11) * w, hash(k * 13) * h, 1.5 + hash(k) * 2, 0, 7); g.fill(); } });
  TEX.rain.wrapS = TEX.rain.wrapT = THREE.RepeatWrapping; TEX.rain.repeat.set(3, 2);
  // ---- her phone on the nightstand
  TEX.phoneOff = text(144, 300, (g, w, h) => { g.fillStyle = "#06070A"; g.fillRect(0, 0, w, h); });
  TEX.phoneNote = text(144, 300, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#2A3150"); gr.addColorStop(1, "#0C0F1A"); g.fillStyle = gr; g.fillRect(0, 0, w, h); label(g, "6:02", w / 2, 60, 40, "#FFFFFF", "center"); for (let k = 0; k < 5; k++) { block(g, 10, 90 + k * 40, w - 20, 34, "rgba(255,255,255,.88)", 8); block(g, 16, 96 + k * 40, 22, 22, ["#E1251B", "#00B8C4", "#111", "#F2C11B", "#10A37F"][k], 5); block(g, 44, 100 + k * 40, 70, 6, "#C0392B", 3); block(g, 44, 112 + k * 40, 50, 5, "#9AA0AC", 3); } });
  TEX.poster = text(320, 440, (g, w, h) => { g.fillStyle = "#1E1B18"; g.fillRect(0, 0, w, h); candle(g, w / 2, 300, 1.2, "#E8735A"); label(g, "MAYA", w / 2, 70, 54, "#F2C94C", "center"); label(g, "HAND-POURED CANDLES", w / 2, 108, 18, "#FFFDF8", "center"); label(g, "LAUNCHING SOON", w / 2, 410, 22, "#F2C94C", "center"); });
  TEX.clock = text(256, 256, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.beginPath(); g.arc(128, 128, 124, 0, 7); g.fill(); g.strokeStyle = "#1E1B18"; g.lineWidth = 10; g.stroke(); for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; g.fillStyle = "#1E1B18"; g.fillRect(128 + Math.sin(a) * 100 - 4, 128 - Math.cos(a) * 100 - 4, 8, 8); } g.lineWidth = 9; g.beginPath(); g.moveTo(128, 128); g.lineTo(128 + 50, 128 - 20); g.stroke(); g.lineWidth = 6; g.beginPath(); g.moveTo(128, 128); g.lineTo(128 - 10, 128 - 85); g.stroke(); });
  // ---- the app tiles: the paid app (old) and its open-source replacement (new)
  const TN = C.tileNames;
  const tile = (name, bg, fg, sub) => text(512, 512, (g, w, h) => {
    g.fillStyle = bg; g.fillRect(0, 0, w, h);
    g.strokeStyle = "rgba(255,255,255,.25)"; g.lineWidth = 10; g.strokeRect(14, 14, w - 28, h - 28);
    g.fillStyle = fg; g.textAlign = "center"; g.textBaseline = "middle";
    const words = name.split("\n"); let f = 96; g.font = FT(800, f); while (Math.max(...words.map((x) => g.measureText(x).width)) > 430 && f > 40) { f -= 4; g.font = FT(800, f); }
    words.forEach((wd, k) => g.fillText(wd, w / 2, h / 2 - (words.length - 1) * f * .55 + k * f * 1.1 - (sub ? 26 : 0)));
    if (sub) { g.font = FT(800, 34); g.globalAlpha = .85; g.fillText(sub, w / 2, h - 90); g.globalAlpha = 1; }
  });
  TN.forEach(([o, n], k) => {
    const [oc, nc] = C.tileCol[k], fgO = C.tileFg[k][0], fgN = C.tileFg[k][1];
    TEX["tOld" + k] = tile(o, oc, fgO, "PAID"); TEX["tNew" + k] = tile(n, nc, fgN, "OPEN SOURCE");
  });
  // ---- the monitor
  TEX.m_off = text(64, 40, (g, w, h) => { g.fillStyle = "#050608"; g.fillRect(0, 0, w, h); });
  TEX.m_calm = text(SW_, SH_, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#F7C873"); gr.addColorStop(1, "#E8735A"); g.fillStyle = gr; g.fillRect(0, 0, w, h); label(g, "$0 / month", w / 2, h / 2 + 10, 120, "#FFFFFF", "center"); label(g, "every tool, still here", w / 2, h / 2 + 90, 40, "rgba(255,255,255,.9)", "center", 700); });
  TEX.m_cancel = app("Billing", "#E5484D", (g, w, h) => {
    label(g, "Your subscriptions", 60, 130, 44, "#14161C");
    TN.forEach(([o], k) => { const x = 60 + (k % 2) * 590, y = 170 + Math.floor(k / 2) * 132; block(g, x, y, 560, 110, "#FFFFFF"); block(g, x + 20, y + 22, 66, 66, C.tileCol[k][0], 14); label(g, o.replace("\n", " "), x + 106, y + 50, 30, "#14161C"); label(g, "Payment failed", x + 106, y + 86, 24, "#8A8F9C", "left", 600); block(g, x + 380, y + 34, 160, 42, "#FDE7E8", 21); label(g, "CANCELLED", x + 460, y + 64, 22, "#D92D20", "center"); });
  });
  TEX.m_locked = app("Account", "#E5484D", (g, w, h) => {
    g.fillStyle = "#14161C"; g.fillRect(0, 64, w, h - 64);
    const cx = w / 2, cy = 330; g.strokeStyle = "#E5484D"; g.lineWidth = 34; g.beginPath(); g.arc(cx, cy - 40, 86, Math.PI, 0); g.stroke(); block(g, cx - 140, cy - 40, 280, 210, "#E5484D", 26); block(g, cx - 18, cy + 30, 36, 70, "#14161C", 14);
    label(g, "LOCKED · 30 DAYS", cx, 640, 76, "#FFFFFF", "center");
  }, { bar: "#0B0C10" });
  TEX.m_gimp = app("GIMP", "#7A6E5E", (g, w, h) => {
    g.fillStyle = "#3A3A3E"; g.fillRect(0, 64, w, h - 64);
    g.fillStyle = "#2C2C30"; g.fillRect(0, 64, 110, h - 64); for (let k = 0; k < 9; k++) block(g, 22, 90 + k * 66, 66, 52, k === 2 ? "#F2B33D" : "#4A4A50", 8);
    g.fillStyle = "#2C2C30"; g.fillRect(w - 260, 64, 260, h - 64); label(g, "Layers", w - 236, 110, 26, "#E8E8EE"); for (let k = 0; k < 4; k++) { block(g, w - 240, 130 + k * 70, 220, 56, k === 0 ? "#4C6EF5" : "#3E3E44", 8); }
    const gr = g.createLinearGradient(170, 100, 170, 700); gr.addColorStop(0, "#F4E1C8"); gr.addColorStop(1, "#E8C29A"); g.fillStyle = gr; g.fillRect(170, 100, 790, 600);
    candle(g, 565, 560, 2.3, "#E8735A");
    g.strokeStyle = "#4C6EF5"; g.lineWidth = 4; g.setLineDash([16, 10]); g.strokeRect(370, 170, 390, 470); g.setLineDash([]);
  }, { tag: "OPEN SOURCE", bg: "#3A3A3E" });
  TEX.m_penpot = app("Penpot", "#31EFB8", (g, w, h) => {
    g.fillStyle = "#18181C"; g.fillRect(0, 64, w, h - 64);
    g.fillStyle = "#232328"; g.fillRect(0, 64, 220, h - 64); for (let k = 0; k < 7; k++) { block(g, 20, 100 + k * 60, 180, 40, k === 1 ? "#31EFB8" : "#2E2E34", 8); }
    block(g, 420, 96, 440, 620, "#1E1B18", 4); candle(g, 640, 520, 1.9, "#E8735A");
    label(g, "MAYA", 640, 210, 84, "#F2C94C", "center"); label(g, "LAUNCH · DAY 30", 640, 660, 40, "#FFFDF8", "center");
    g.strokeStyle = "#31EFB8"; g.lineWidth = 4; g.strokeRect(420, 96, 440, 620);
  }, { tag: "OPEN SOURCE", bg: "#18181C" });
  TEX.m_shotcut = app("Shotcut", "#2C7BD8", (g, w, h) => {
    g.fillStyle = "#26282E"; g.fillRect(0, 64, w, h - 64);
    block(g, 330, 90, 620, 350, "#000", 4); candle(g, 640, 380, 1.5, "#F2B33D"); label(g, "COMING SOON", 640, 170, 40, "#FFFFFF", "center");
    for (let r = 0; r < 3; r++) { g.fillStyle = "#1C1D22"; g.fillRect(40, 470 + r * 70, w - 80, 58); for (let k = 0; k < 6; k++) block(g, 60 + k * 190 + r * 30, 478 + r * 70, 170, 42, ["#2C7BD8", "#3FA372", "#7E5BB0"][r], 6); }
    g.fillStyle = "#E5484D"; g.fillRect(560, 460, 4, 230);
    block(g, w - 380, 92, 340, 70, "#3FA372", 12); label(g, "Export  100%", w - 210, 140, 32, "#FFFFFF", "center");
  }, { tag: "OPEN SOURCE", bg: "#26282E" });
  TEX.m_mailLocked = app("Mailchimp", "#F2C11B", (g, w, h) => {
    label(g, "Audience", 60, 140, 46, "#14161C"); label(g, "10,000 contacts", 60, 200, 34, "#8A8F9C", "left", 700);
    for (let k = 0; k < 6; k++) { block(g, 60, 240 + k * 70, w - 120, 56, "#FFFFFF", 10); block(g, 80, 256 + k * 70, 260, 24, "#E4E6EC", 8); block(g, 380, 256 + k * 70, 360, 24, "#EEF0F4", 8); }
    g.fillStyle = "rgba(20,22,28,.6)"; g.fillRect(0, 64, w, h - 64);
    block(g, w / 2 - 330, 250, 660, 260, "#FFFFFF", 26); label(g, "Account locked", w / 2, 350, 56, "#D92D20", "center"); label(g, "You can't send any emails.", w / 2, 420, 32, "#4A4F5C", "center", 700);
  });
  dyn("listmonk", SW_, SH_, 40, (g, w, h, u) => {
    g.fillStyle = "#F4F6FA"; g.fillRect(0, 0, w, h); g.fillStyle = "#0B1F3F"; g.fillRect(0, 0, w, 64);
    label(g, "listmonk", 60, 44, 32, "#FFFFFF"); block(g, w - 200, 18, 176, 30, "#28C840", 15); label(g, "OPEN SOURCE", w - 112, 40, 18, "#0B0D12", "center");
    label(g, "Campaign: The launch is coming", 60, 140, 40, "#0B1F3F"); label(g, "To: all subscribers (10,000)", 60, 192, 28, "#6A7080", "left", 700);
    block(g, 60, 250, w - 120, 46, "#E1E6EF", 23); block(g, 60, 250, (w - 120) * Math.max(.04, u), 46, "#0055D4", 23);
    const n = Math.round(10000 * u); label(g, n.toLocaleString("en-US"), w / 2, 450, 150, "#0055D4", "center"); label(g, u >= 1 ? "sent · delivered" : "sending...", w / 2, 520, 40, "#6A7080", "center", 700);
    if (u >= 1) { block(g, w / 2 - 170, 570, 340, 70, "#28C840", 35); label(g, "Done", w / 2, 618, 36, "#FFFFFF", "center"); }
  });
  dyn("postiz", SW_, SH_, 30, (g, w, h, u) => {
    g.fillStyle = "#141022"; g.fillRect(0, 0, w, h); g.fillStyle = "#1E1830"; g.fillRect(0, 0, w, 64);
    label(g, "Postiz", 60, 44, 32, "#FFFFFF"); block(g, w - 200, 18, 176, 30, "#28C840", 15); label(g, "OPEN SOURCE", w - 112, 40, 18, "#0B0D12", "center");
    label(g, "Launch month · 30 posts scheduled", 60, 130, 36, "#EDE8FF");
    const days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]; days.forEach((d, k) => label(g, d, 90 + k * 164, 180, 22, "#9A8FC0", "center"));
    const filled = Math.round(30 * u);
    for (let i = 0; i < 35; i++) { const x = 20 + (i % 7) * 164, y = 200 + Math.floor(i / 7) * 104; block(g, x, y, 150, 92, "#231C3A", 10); if (i < filled) { block(g, x + 10, y + 12, 130, 30, ["#612BD3", "#E1306C", "#1DA1F2", "#0A66C2"][i % 4], 8); block(g, x + 10, y + 50, 90, 24, "#3A3060", 6); } }
  });
  TEX.m_linkstack = app("LinkStack", "#2B2B6E", (g, w, h) => {
    g.fillStyle = "#E9E6FF"; g.fillRect(0, 64, w, h - 64);
    block(g, w / 2 - 230, 90, 460, 630, "#1E1B18", 40);
    g.fillStyle = "#E8735A"; g.beginPath(); g.arc(w / 2, 190, 60, 0, 7); g.fill(); label(g, "M", w / 2, 212, 64, "#FFFFFF", "center");
    label(g, "@maya.candles", w / 2, 300, 30, "#FFFFFF", "center");
    ["Shop the launch", "Join the list", "Watch the teaser", "Book a workshop"].forEach((s, k) => { block(g, w / 2 - 190, 340 + k * 88, 380, 68, k === 0 ? "#F2C94C" : "#FFFDF8", 34); label(g, s, w / 2, 384 + k * 88, 28, "#1E1B18", "center"); });
  }, { tag: "OPEN SOURCE" });
  TEX.m_appflowy = app("AppFlowy", "#6E3FF3", (g, w, h) => {
    label(g, "Launch plan", 50, 130, 46, "#14161C");
    const cols = [["To do", ["Product photos", "Email #2"]], ["Doing", ["Launch page", "Teaser cut"]], ["Done", ["Logo", "Pricing", "30 posts", "Link page"]]];
    cols.forEach(([nm, cards], c) => { const x = 50 + c * 400; block(g, x, 160, 370, 560, "#ECEEF3", 18); label(g, nm, x + 24, 206, 30, "#4A4F5C"); cards.forEach((s, k) => { block(g, x + 18, 232 + k * 112, 334, 96, "#FFFFFF", 14); block(g, x + 36, 250 + k * 112, 70, 10, ["#6E3FF3", "#E8735A", "#3FA372"][c], 5); label(g, s, x + 36, 300 + k * 112, 28, "#14161C"); }); });
  }, { tag: "OPEN SOURCE" });
  TEX.m_doc = app("Notes", "#F2B33D", (g, w, h) => {
    g.fillStyle = "#1A1C22"; g.fillRect(0, 64, w, h - 64);
    label(g, "Launch email: draft", 80, 150, 44, "#EDEFF5"); block(g, 80, 200, 6, 50, "#F2C94C", 2);
    label(g, "11:48 PM · 0 words", 80, 320, 28, "#6A7080", "left", 700);
  }, { bar: "#0E1014" });
  // ---- the laptop
  TEX.l_lapOff = text(64, 40, (g, w, h) => { g.fillStyle = "#050608"; g.fillRect(0, 0, w, h); });
  TEX.l_lapWall = text(620, 400, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#3A6FC4"); gr.addColorStop(1, "#7E5BB0"); g.fillStyle = gr; g.fillRect(0, 0, w, h); label(g, "MAYA", w / 2, h / 2 + 20, 80, "rgba(255,255,255,.85)", "center"); });
  TEX.l_lapDoc = text(620, 400, (g, w, h) => { g.fillStyle = "#1A1C22"; g.fillRect(0, 0, w, h); label(g, "Launch email: draft", 40, 80, 34, "#EDEFF5"); block(g, 40, 110, 5, 40, "#F2C94C", 2); });
  TEX.l_nowifi = text(620, 400, (g, w, h) => {
    g.fillStyle = "#14161C"; g.fillRect(0, 0, w, h);
    g.strokeStyle = "#8A8F9C"; g.lineWidth = 16; g.lineCap = "round"; for (let k = 0; k < 3; k++) { g.beginPath(); g.arc(w / 2, 220, 40 + k * 46, -2.4, -.74); g.stroke(); } g.fillStyle = "#8A8F9C"; g.beginPath(); g.arc(w / 2, 220, 14, 0, 7); g.fill();
    g.strokeStyle = "#E5484D"; g.lineWidth = 16; g.beginPath(); g.moveTo(w / 2 - 120, 70); g.lineTo(w / 2 + 120, 250); g.stroke();
    label(g, "No internet", w / 2, 330, 46, "#FFFFFF", "center");
  });
  const OL = ["Subject: It's here.", "", "After 30 days of building,", "the MAYA candle collection", "is live. Hand-poured, small", "batch, and only 200 jars.", "", "Shop the launch: link below."];
  dyn("ollama", 620, 400, 60, (g, w, h, u) => {
    g.fillStyle = "#0C0E12"; g.fillRect(0, 0, w, h);
    g.font = MONO(22); g.fillStyle = "#7CE0A0"; g.fillText("$ ollama run mistral", 24, 40);
    g.fillStyle = "#9AA0AC"; g.fillText(">>> write my launch email", 24, 76);
    const total = OL.join("").length; let n = Math.round(total * u);
    g.fillStyle = "#EDEFF5"; let y = 118;
    for (const ln of OL) { if (n <= 0) break; const s = ln.slice(0, n); g.fillText(s, 24, y); n -= ln.length; y += 32; }
    if (u < 1) { g.fillStyle = "#7CE0A0"; g.fillRect(24 + Math.min(560, (g.measureText(OL.find(() => true)).width)) * 0, y - 20, 0, 0); }
    block(g, w - 186, 14, 168, 34, "#1E3A28", 17); g.font = FT(800, 18); g.fillStyle = "#7CE0A0"; g.textAlign = "center"; g.fillText("OFFLINE · LOCAL", w - 102, 37); g.textAlign = "left";
  });
  dyn("orders", SW_, SH_, 50, (g, w, h, u) => {
    g.fillStyle = "#F6F7F9"; g.fillRect(0, 0, w, h); g.fillStyle = "#1E2230"; g.fillRect(0, 0, w, 64); label(g, "Launch day", 60, 44, 32, "#FFFFFF");
    const n = Math.round(112 * u), rev = Math.round(4368 * u);
    label(g, "$" + rev.toLocaleString("en-US"), 60, 220, 130, "#14161C"); label(g, n + " orders today", 64, 280, 34, "#3FA372");
    g.strokeStyle = "#3FA372"; g.lineWidth = 8; g.beginPath(); for (let k = 0; k <= 40 * u; k++) { const x = 60 + k * 18, y = 640 - Math.pow(k / 40, 1.6) * 300 - 20 * Math.sin(k * .9); k ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
    for (let k = 0; k < Math.min(6, n); k++) { block(g, 860, 110 + k * 100, 380, 84, "#FFFFFF", 14); block(g, 880, 128 + k * 100, 48, 48, "#E8735A", 10); label(g, "New order", 946, 150 + k * 100, 26, "#14161C"); label(g, "$" + [39, 78, 39, 117, 39, 78][k] + ".00", 946, 182 + k * 100, 22, "#3FA372", "left", 700); }
  });
  dyn("resub", SW_, SH_, 2, (g, w, h, u) => {
    const st = Math.round(u * 2);
    g.fillStyle = "#2A2E38"; g.fillRect(0, 0, w, h);
    block(g, w / 2 - 400, 130, 800, 480, "#FFFFFF", 30);
    label(g, "Your subscriptions are back", w / 2, 230, 46, "#14161C", "center");
    label(g, "Resubscribe to all 8 apps for $374.86 / month?", w / 2, 300, 30, "#4A4F5C", "center", 700);
    block(g, w / 2 - 340, 400, 320, 96, "#E5484D", 48); label(g, "Resubscribe", w / 2 - 180, 460, 34, "#FFFFFF", "center");
    block(g, w / 2 + 20, 400, 320, 96, st ? "#3FA372" : "#E8EBF0", 48); label(g, "No thanks", w / 2 + 180, 460, 34, st ? "#FFFFFF" : "#14161C", "center");
    if (st === 1) { g.fillStyle = "#14161C"; g.beginPath(); g.moveTo(w / 2 + 210, 470); g.lineTo(w / 2 + 210, 530); g.lineTo(w / 2 + 226, 516); g.lineTo(w / 2 + 240, 544); g.lineTo(w / 2 + 250, 538); g.lineTo(w / 2 + 236, 512); g.lineTo(w / 2 + 256, 510); g.closePath(); g.fill(); }
  });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
}

const ready = (async () => {
  try { const jb = new FontFace("JBMono", "url(assets/fonts/jbmono-bold.ttf)", { weight: "700" }); document.fonts.add(await jb.load()); } catch (e) { /* fall back */ }
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 40px Manrope"), document.fonts.load("600 40px Manrope"), document.fonts.load("500 40px Garamond")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  for (const k in SET) SET[k].visible = true;
  renderer.compile(scene, camera);
  renderAt(window.STACK_COVER ? window.STACK_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["stack"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.STACK_COVER ? window.STACK_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C, R };
