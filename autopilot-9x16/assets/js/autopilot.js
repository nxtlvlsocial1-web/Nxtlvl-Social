// Autopilot reel: "What if your marketing ran itself while you slept?" A cinematic what-if in the house voxel style.
// Rosa's café, 11 PM: 200 unanswered messages. Theo sets up six open-source automations and tells her to sleep. Through
// the night six neon signs light up on the café wall, one per tool, while streams of light fly from her phone and the
// clock races; at 4:12 AM a post goes viral and the system handles it; at dawn she wakes to every message answered.
// Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek; cue times come from window.CT.
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

// ================================================================= ROSA'S CAFÉ: one room on a city street, 11 PM to 7 AM
// x: -4 .. 4; z: -3.5 (the neon wall, behind the counter) .. 3.0 (the shop window onto the street); ceiling 3.2.
// Rosa's table is by the window; she sits facing the street (+z), so the neon wall glows behind her.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
const R = mkSet("cafe");
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const TABLE = v3(0, 0, 1.25), SEAT = v3(0, 0, .62), PHONE = v3(.4, .772, 1.5), LAP = v3(-.2, .77, 1.5);
const NEON = [v3(-2.3, 2.62, -3.38), v3(0, 2.62, -3.38), v3(2.3, 2.62, -3.38), v3(-2.3, 1.82, -3.38), v3(0, 1.82, -3.38), v3(2.3, 1.82, -3.38)];
const DOORX = 2.95;
{
  const plankTex = pix(64, 64, (g) => { px(g, "#8E6440", 0, 0, 64, 64); for (let j = 0; j < 8; j++) { px(g, j % 2 ? "#865D3A" : "#966A44", 0, j * 8, 64, 8); px(g, "#6A4A2E", 0, j * 8, 64, 1); px(g, "#6A4A2E", (j * 23) % 64, j * 8, 1, 8); } }, false);
  const checker = pix(32, 32, (g) => { for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) px(g, (i + j) % 2 ? "#2B2A33" : "#E9E2D3", i * 8, j * 8, 8, 8); });
  flat(8.2, 3.2, new THREE.MeshStandardMaterial({ map: rep(checker, 8, 3), roughness: .5 }), 0, 0, -1.9);
  flat(8.2, 3.6, new THREE.MeshStandardMaterial({ map: rep(plankTex, 5, 2), roughness: .7 }), 0, 0, 1.2);
  const brick = pix(64, 64, (g) => { px(g, "#7A3B2E", 0, 0, 64, 64); for (let j = 0; j < 8; j++) for (let i = 0; i < 4; i++) { px(g, ["#8A4434", "#7E3D2F", "#934A38"][(i + j) % 3], i * 16 + (j % 2) * 8, j * 8, 15, 7); } }, false);
  const brickM = new THREE.MeshStandardMaterial({ map: rep(brick, 4, 2), roughness: .9 });
  const wallM = mat(0x2E3A3A), trim = mat(0x1E1B18), ceilM = mat(0x22201E);
  box(8.4, .12, 6.7, ceilM, 0, 3.26, -.25, { cast: false });
  box(8.4, 3.3, .2, brickM, 0, 1.6, -3.6);                                     // the neon wall
  box(.2, 3.3, 6.7, wallM, -4.1, 1.6, -.25); box(.2, 3.3, 6.7, wallM, 4.1, 1.6, -.25);
  // the front: a low wall, the big window, the glass door on the right, a frame
  box(8.4, .5, .2, trim, 0, .25, 3.05); box(8.4, .45, .2, trim, 0, 3.05, 3.05);
  for (const x of [-4.05, -1.4, 1.3, 2.35, 3.55, 4.05]) box(.12, 2.6, .24, trim, x, 1.55, 3.04);
  R.glassM = new THREE.MeshPhysicalMaterial({ color: 0xBFD6E6, roughness: .05, transparent: true, opacity: .08, envMap: ENV, envMapIntensity: .8, depthWrite: false });
  plane(7.9, 2.35, R.glassM, -.2, 1.68, 3.06, Math.PI);
  R.windowText = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, depthWrite: false }); LATE.push([R.windowText, "windowText"]);
  plane(2.2, .7, R.windowText, -2.7, 2.15, 3.07, Math.PI);                   // "ROSA'S" painted on the glass, read from the street
  const door = new THREE.Group(); door.position.set(DOORX - .6, 0, 3.02); R.add(door); R.door = door;
  box(1.15, 2.4, .06, mat(0x1E1B18), .6, 1.2, 0, { parent: door }); R.signM = texMat("openSign"); plane(.42, .26, R.signM, .6, 1.55, .04, 0, door);
  R.bell = new THREE.Group(); R.bell.position.set(DOORX, 2.5, 2.9); R.add(R.bell); cyl(.04, .07, .09, goldM, 0, -.06, 0, 12, { parent: R.bell });
  // the counter, the espresso machine, a cake case, the chalkboard menu
  box(5.2, 1.0, .7, mat(0x5A3A26), -.6, .5, -2.55); box(5.3, .06, .8, mat(0xD9CDB6, { roughness: .4 }), -.6, 1.03, -2.55);
  box(.8, .55, .5, metal(0xC9CDD4, .25), -2.4, 1.33, -2.6); box(.5, .12, .3, metal(0x2A2A2E), -2.4, 1.0 + .12, -2.35);
  box(1.0, .45, .6, R.glassM, .6, 1.29, -2.55); for (let k = 0; k < 3; k++) cyl(.12, .12, .12, mat(["#F4E6C8", "#D9607A", "#7A4A2A"][k]), .3 + k * .3, 1.12, -2.55, 16);
  R.chalkM = texMat("chalk", { transparent: false }); plane(1.4, 1.0, R.chalkM, -3.98, 1.9, -1.6, Math.PI / 2);
  for (let k = 0; k < 6; k++) box(.18, .26, .12, mat(["#3FA372", "#D9483B", "#F2B33D"][k % 3]), -3.2 + k * .25, 1.2, -3.42);
  box(1.8, .04, .3, mat(0x5A3A26), -2.4, 1.05, -3.42);
  // the neon signs: a dark backing board and the tube texture (dim when off)
  R.neon = NEON.map((p, k) => {
    const g = new THREE.Group(); g.position.copy(p); R.add(g);
    box(1.9, .62, .04, mat(0x101014, { roughness: .4 }), 0, 0, -.02, { parent: g });
    const m = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, depthWrite: false }); LATE.push([m, "neon" + k]);
    const pl = new THREE.Mesh(new THREE.PlaneGeometry(1.8, .56), m); pl.position.z = .006; g.add(pl);
    return { g, m };
  });
  // Rosa's table by the window, her laptop and phone; the other tables closed for the night (chairs up)
  cyl(.55, .55, .05, mat(0xB08A62, { roughness: .5 }), TABLE.x, .75, TABLE.z, 28); cyl(.05, .05, .72, metal(0x2A2A2E), TABLE.x, .37, TABLE.z, 10); cyl(.3, .3, .03, metal(0x2A2A2E), TABLE.x, .02, TABLE.z, 18);
  const stool = (x, z, up = false) => { const g = new THREE.Group(); g.position.set(x, up ? .78 : 0, z); if (up) g.rotation.x = Math.PI; R.add(g); box(.42, .05, .42, mat(0x7A4A2A), 0, .47, 0, { parent: g }); for (const [dx, dz] of [[-.17, -.17], [.17, -.17], [-.17, .17], [.17, .17]]) box(.04, .45, .04, mat(0x1E1B18), dx, .225, dz, { parent: g }); box(.42, .4, .04, mat(0x7A4A2A), 0, .75, -.19, { parent: g }); return g; };
  R.chair = stool(SEAT.x, SEAT.z);
  for (const [x, z] of [[-2.6, 1.3], [2.0, 1.0], [-2.6, -.6], [1.4, -1.0]]) { cyl(.5, .5, .05, mat(0xE9E2D3, { roughness: .4 }), x, .75, z, 28); cyl(.05, .05, .72, metal(0x2A2A2E), x, .37, z, 10); stool(x - .2, z, true).position.y = .8; stool(x + .25, z, true).position.y = .8; }
  const lap = new THREE.Group(); lap.position.copy(LAP); lap.rotation.y = Math.PI; R.add(lap);
  box(.34, .018, .24, metal(0xB8BCC4, .35), 0, .009, .12, { parent: lap });
  const lid = new THREE.Group(); lid.rotation.x = -.28; lap.add(lid); R.lid = lid;
  box(.34, .23, .012, metal(0xB8BCC4, .35), 0, .115, -.007, { parent: lid });
  R.lapM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const ls = new THREE.Mesh(new THREE.PlaneGeometry(.31, .2), R.lapM); ls.position.set(0, .118, 0); lid.add(ls);
  R.phone = new THREE.Group(); R.phone.position.copy(PHONE); R.phone.rotation.y = .4; R.add(R.phone);
  box(.08, .012, .16, mat(0x15171C), 0, 0, 0, { parent: R.phone });
  R.phoneM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const ps = new THREE.Mesh(new THREE.PlaneGeometry(.072, .15), R.phoneM); ps.rotation.x = -Math.PI / 2; ps.position.y = .007; R.phone.add(ps);
  cyl(.045, .04, .09, mat(0xF2F2F2), -.3, .82, 1.0, 14);                          // her cold coffee
  // pendant lamps over the tables
  R.pendants = [[0, 1.25], [-2.6, 1.3], [2.0, 1.0], [-1.0, -2.5], [1.0, -2.5]].map(([x, z]) => { cyl(.008, .008, .6, mat(INK), x, 2.95, z, 6); const m = mat(0xF4E6C8, { emissive: 0xFFC98A, emissiveIntensity: 0 }); cyl(.08, .2, .2, m, x, 2.55, z, 16); return m; });
  // plants, a shelf of coffee bags, the wall clock (left wall)
  for (const [x, z] of [[-3.6, 2.5], [3.6, -1.5]]) { cyl(.2, .16, .35, mat(0xC9644E), x, .18, z, 12); for (let j = 0; j < 4; j++) box(.34 - j * .05, .32, .34 - j * .05, mat(j % 2 ? 0x4E7A3E : 0x5E8C48), x, .5 + j * .28, z); }
  R.clockM = texMat("clock"); const ck = new THREE.Mesh(new THREE.CircleGeometry(.32, 40), R.clockM); ck.position.set(-3.98, 2.35, .6); ck.rotation.y = Math.PI / 2; R.add(ck);
  R.hands = [0, 1].map((k) => { const g = new THREE.Group(); g.position.set(-3.96, 2.35, .6); g.rotation.y = Math.PI / 2; R.add(g); const hnd = new THREE.Mesh(new THREE.BoxGeometry(.022, k ? .26 : .18, .01), mat(0x1E1B18)); hnd.position.y = (k ? .26 : .18) / 2 - .02; g.add(hnd); return g; });
  // ---- outside: the sidewalk, the street, lamps, the buildings across the road, the sky, a cat
  flat(30, 2.4, groundMat(CONC, 10, 1), 0, -.02, 4.3); flat(30, 7, groundMat(ASPH, 10, 3), 0, -.05, 9.0);
  for (let k = -6; k < 7; k++) box(1.2, .01, .14, mat(0xE9E2D3), k * 2.5, -.035, 9.0, { cast: false });
  box(30, .14, .2, mat(0x9E9A92), 0, .02, 5.5);
  R.lampM = mat(0xFFE2B0, { emissive: 0xFFC98A, emissiveIntensity: 0 });
  R.lamps = [-4.5, 4.5].map((x) => { cyl(.06, .08, 4.2, metal(0x2A2A2E, .5), x, 2.1, 5.2, 10); box(.7, .08, .12, metal(0x2A2A2E, .5), x, 4.2, 5.0); const h = cyl(.16, .22, .2, R.lampM, x, 4.08, 4.75, 14); return h; });
  R.storefront = texMat("frontSign"); plane(3.2, .7, R.storefront, -.2, 3.4, 3.2, 0);   // ROSA'S CAFÉ over the window, facing the street
  box(8.6, 1.0, .25, mat(0x1E1B18), 0, 3.4, 3.12);
  box(8.6, 6, .3, brickM, 0, 6.3, 3.2);
  R.bldM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .8, emissive: 0xFFD9A0, emissiveIntensity: 0 }); LATE.push([R.bldM, "bld"]);
  R.bldLitTex = null;
  for (let k = -3; k <= 3; k++) { const w = 4 + hash(k * 3.1) * 2, h = 6 + hash(k * 7.7) * 9; const b = box(w, h, 3, R.bldM, k * 5.2 + (hash(k) - .5), h / 2, 14.5, { uv: true }); b.material = R.bldM; }
  R.sky = new THREE.Mesh(new THREE.SphereGeometry(120, 32, 16), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, side: THREE.BackSide, depthWrite: false, fog: false })); R.add(R.sky); LATE.push([R.sky.material, "skyNight"]);
  R.skyDawn = new THREE.Mesh(new THREE.SphereGeometry(119, 32, 16), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, side: THREE.BackSide, transparent: true, opacity: 0, depthWrite: false, fog: false })); R.add(R.skyDawn); LATE.push([R.skyDawn.material, "skyDawn"]);
  R.moon = new THREE.Mesh(new THREE.CircleGeometry(2.2, 32), new THREE.MeshBasicMaterial({ color: 0xF4F1E6, toneMapped: false, fog: false })); R.add(R.moon);
  R.sunDisc = new THREE.Mesh(new THREE.CircleGeometry(3.2, 32), new THREE.MeshBasicMaterial({ color: 0xFFD9A0, toneMapped: false, fog: false })); R.add(R.sunDisc);
  for (let k = -4; k <= 4; k++) { const h = 9 + hash(k * 5.1) * 14; const b = box(5.5, h, 5, R.bldM, k * 6.2, h / 2, -12 - hash(k) * 4, { uv: true }); b.material = R.bldM; }   // the blocks behind the café
  R.streetL = [-4.5, 4.5].map((x) => { const l = new THREE.PointLight(0xFFC98A, 0, 9, 1.6); l.position.set(x, 3.9, 4.6); scene.add(l); return l; });
  R.spill = new THREE.PointLight(0xFFB070, 0, 7, 1.6); R.spill.position.set(0, 1.6, 3.8); scene.add(R.spill);
  // the cat: body, head, ears, tail, four legs
  const cat = new THREE.Group(); cat.scale.setScalar(1.5); R.add(cat); R.cat = cat; const cm_ = mat(0xD9823A);
  box(.42, .16, .16, cm_, 0, .2, 0, { parent: cat }); const hd = box(.15, .14, .14, cm_, .25, .3, 0, { parent: cat });
  for (const s of [-1, 1]) box(.04, .06, .04, cm_, .27, .4, s * .04, { parent: cat });
  for (const s of [-1, 1]) box(.02, .02, .005, glow(0xC8F07A), .325, .32, s * .035, { parent: cat });
  R.catTail = new THREE.Group(); R.catTail.position.set(-.2, .25, 0); cat.add(R.catTail); box(.04, .28, .04, cm_, 0, .14, 0, { parent: R.catTail });
  R.catLegs = [[-.14, -.05], [-.14, .05], [.14, -.05], [.14, .05]].map(([x, z]) => { const g = new THREE.Group(); g.position.set(x, .13, z); cat.add(g); box(.04, .13, .04, cm_, 0, -.065, 0, { parent: g }); return g; });
  // the automation streams: glowing cubes that fly from her phone to a neon sign
  R.flow = new THREE.InstancedMesh(new THREE.BoxGeometry(.035, .035, .035), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), 6 * 26);
  R.flow.frustumCulled = false; R.add(R.flow);
  for (let i = 0; i < 6 * 26; i++) R.flow.setColorAt(i, tmpC.set(0xffffff));
}
PARENT = scene;

// ---------------------------------------------------------------- the cast: Rosa (the owner), Theo (her developer friend)
const ROSA = makeChar({ id: "rosa", skin: "#A8714C", hair: "#1E1B18", style: "long", top: "#D9483B", topStyle: "cardigan", pants: "#2E3A55", shoe: "#F4EFE6", lash: true, earring: true }, R);
ROSA.seed = 2.1;
const THEO = makeChar({ id: "theo", skin: "#F0C49C", hair: "#8A4A2A", style: "short", beard: "#8A4A2A", top: "#4A5A3A", topStyle: "hoodie", pants: "#3A3A3A", shoe: "#1E1B18" }, R);
THEO.seed = 5.3;
const CUPS = [0, 1].map(() => { const g = new THREE.Group(); R.add(g); cyl(.045, .04, .11, mat(0xF4EFE6), 0, 0, 0, 12, { parent: g }); cyl(.047, .047, .02, mat(0x7A4A2A), 0, .065, 0, 12, { parent: g }); return g; });

// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const NT = C.neon;                    // when each neon sign lights
const V0 = C.viral, D0 = C.dawn, M0 = C.montage;
const who = (t, name) => C.who.some((w, k) => w === name && t > L[k] - .05 && t < E[k] + .02);
const sceneOf = (t) => (t < M0 ? 0 : t < V0 ? 1 : t < D0 ? 2 : 3);
// the story clock: minutes past midnight (wraps), as a function of film time
function clockMin(t) {
  const K = C.clock; let i = 0; while (i + 1 < K.length && t >= K[i + 1][0]) i++;
  const [a, ma] = K[i], [b, mb] = K[Math.min(i + 1, K.length - 1)];
  return b > a ? lerp(ma, mb, clamp((t - a) / (b - a))) : ma;
}

// ---------------------------------------------------------------- shots: [start, {p0, p1, l0, l1, fov, fov1, ap, d, d1}]
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const HEAD = v(SEAT.x, 1.5, SEAT.z);
const FACE = { p0: v(.45, 1.58, 2.7), p1: v(.4, 1.56, 2.55), l0: v(SEAT.x, 1.55, SEAT.z), fov: 52, ap: .22 };
const signShot = (k) => ({ p0: NEON[k].clone().add(v(.6, -.5, 4.3)), p1: NEON[k].clone().add(v(.3, -.45, 3.8)), l0: NEON[k].clone().add(v(0, -.15, 0)), fov: 46, ap: .1 });
const CUTAWAY = [
  { p0: v(3.3, .95, 2.6), p1: v(3.0, 1.05, 2.4), l0: v(-.5, 1.5, -1.6), fov: 58, ap: .02 },          // wide from the window corner, low
  { p0: v(-4.2, .9, 7.6), p1: v(-2.6, .95, 7.6), l0: v(-.6, 1.0, 4.2), l1: v(.6, 1.0, 4.2), fov: 50, ap: .01 },   // the street: the cat walks past the glowing window
  { p0: v(1.7, 2.6, 3.0), p1: v(1.45, 2.5, 2.75), l0: v(0, 1.0, .6), fov: 54, ap: .04 },           // high angle: her head on her arms, the phone lighting up
  { p0: v(-2.4, 1.55, 2.4), p1: v(-1.6, 1.6, 2.7), l0: v(0, 1.25, .7), fov: 52, ap: .03 },           // a slow orbit round the table
  { p0: v(5.5, 2.4, 11.5), p1: v(4.5, 2.6, 11.0), l0: v(0, 4.0, 0), fov: 56, ap: .005 },              // outside: the moon crosses the sky over the café
  { p0: v(-2.7, 2.3, .55), p1: v(-2.95, 2.33, .6), l0: v(-3.98, 2.35, .6), fov: 40, ap: .2 },        // the wall clock racing
];
const SHOTS = [
  // night: a crane down from the café sign to the window; Rosa and her phone; Theo
  [0, { p0: v(.7, 3.9, 9.8), p1: v(.3, 1.9, 6.6), l0: v(0, 2.6, 0), l1: v(0, 1.4, 1.0), fov: 54, ap: .008 }],
  [2.75, FACE],
  [L[1] - .2, { p0: v(1.2, 1.78, 2.75), l0: v(.62, 1.72, .15), fov: 50, ap: .22 }],
  // the montage: each sign lights in close-up, then a cutaway of the night passing
  ...NT.flatMap((n, k) => [[n - .9, signShot(k)], [n + 1.4, CUTAWAY[k]]]),
  // 4:12 AM: her phone explodes; every sign pulses; the whole café glows from the street; she smiles in her sleep
  [V0, { p0: v(1.0, 1.4, 2.35), p1: v(.66, 1.08, 1.86), l0: PHONE, fov: 44, fov1: 36, ap: .3 }],
  [V0 + 1.7, { p0: v(-1.2, 2.1, 2.75), p1: v(-.9, 1.9, 2.4), l0: v(0, 1.75, -2.6), fov: 62, ap: .02 }],
  [V0 + 3.6, { p0: v(2.6, 1.6, 8.6), p1: v(1.4, 1.85, 7.4), l0: v(0, 1.8, 3), fov: 52, ap: .005 }],
  [V0 + 5.0, { p0: v(2.8, 1.1, 2.4), p1: v(2.4, 1.2, 2.1), l0: v(-.3, 1.6, -1.8), fov: 58, ap: .02 }],
  // dawn: the sun comes up; she wakes; Theo with two coffees; she turns to us
  [D0, { p0: v(-1.6, .9, 9.6), p1: v(0, 2.2, 8.2), l0: v(0, 2.6, 2), l1: v(0, 1.6, 3), fov: 52, ap: .005 }],
  [L[2] - .35, FACE],
  [L[3] - .3, { p0: v(.4, 1.78, .1), p1: v(.55, 1.78, .25), l0: v(2.3, 1.92, 2.05), fov: 52, ap: .2 }],
  [L[4] - .3, { p0: v(0, 1.62, 2.75), p1: v(0, 1.6, 2.5), l0: v(SEAT.x, 1.66, SEAT.z), fov: 48, ap: .42 }],
];
function shotAt(t) {
  let i = 0; while (i + 1 < SHOTS.length && t >= SHOTS[i + 1][0]) i++;
  const [a, s] = SHOTS[i], b = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR;
  const u = sm(clamp((t - a) / Math.max(.1, b - a)));
  let p = (s.p1 ? V.lerpVectors(s.p0, s.p1, u) : V.copy(s.p0)).clone(); const l = s.l1 ? V2.lerpVectors(s.l0, s.l1, u).clone() : s.l0.clone();
  if (s.d) { const d = lerp(s.d, s.d1 ?? s.d, u); p = l.clone().add(p.sub(l).normalize().multiplyScalar(d)); }
  return { i, a, b, u, p, l, fov: lerp(s.fov, s.fov1 ?? s.fov, u), ap: s.ap, f: s.f ?? p.distanceTo(l) };
}

// ---------------------------------------------------------------- the cast
const SITY = .52 - .71;
const along = (pts, u) => {
  const seg = []; let tot = 0; for (let q = 0; q < pts.length - 1; q++) { const ll = Math.hypot(pts[q + 1][0] - pts[q][0], pts[q + 1][1] - pts[q][1]); seg.push(ll); tot += ll; }
  let d = tot * clamp(u), q = 0; while (q < seg.length - 1 && d > seg[q]) { d -= seg[q]; q++; }
  const f = clamp(d / seg[q]), A = pts[q], B = pts[q + 1];
  return { x: lerp(A[0], B[0], f), z: lerp(A[1], B[1], f), ry: Math.atan2(B[0] - A[0], B[1] - A[1]) };
};
function holdAt(P, k, obj, off = [0, -.1, .04]) {
  P.root.updateMatrixWorld(true); P.hand[k].getWorldPosition(obj.position);
  obj.quaternion.setFromEuler(EU.set(0, P.root.rotation.y, 0)); obj.position.add(V.set(...off).applyQuaternion(obj.quaternion));
}
const PHONEUP = [[1.45, .05, 1.55], [.5, .15, .6]];          // holding her phone up to her face (right hand)
const SLEEP = (t) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], lean: .98 + .015 * Math.sin(t * 1.6), a: [[1.3, -.32, 1.95], [1.3, -.32, 1.95]], hp: .25, hy: .35, hr: .12 });
function updRosa(t, s) {
  const sit = pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: PHONEUP, hp: .22 });
  let p, f;
  if (s === 0) {
    const doze = ss(t, E[1] - .2, M0);
    p = mixP(sit, SLEEP(t), doze);
    f = doze > .5 ? { eyes: "closed", mouth: "flat", noblink: true } : { eyes: "half", mouth: who(t, "rosa") ? "flat" : "sad", brows: "worry", talk: who(t, "rosa") };
    if (t > L[1] - .2 && doze < .5) { p.hy = -.45; f = { eyes: "half", mouth: "smile", brows: "flat" }; }
  } else if (s === 1 || s === 2) {
    p = SLEEP(t);
    f = { eyes: "closed", mouth: s === 2 && t > V0 + 1 ? "smile" : "flat", noblink: true };
  } else {
    const up = ss(t, D0 + .5, D0 + 1.3);
    const toTheo = ss(t, L[3] - .5, L[3] + .1) * (1 - ss(t, E[3] + .1, E[3] + .5));
    p = mixP(SLEEP(t), sit, up);
    if (up > .5) { p.hy = lerp(0, -.75, toTheo); p.hp = lerp(.22, -.02, Math.max(toTheo, ss(t, E[3], E[3] + .4))); }
    if (t > E[3] + .3) { p.a = [[.4, .12, .7], [2.2, -.2, 1.5]]; p.a[1][1] = .1 + .22 * Math.sin(t * 8); p.hp = 0; }   // a small wave to us
    f = up < .5 ? { eyes: "closed", mouth: "flat", noblink: true } : t < L[2] ? { eyes: "half", mouth: "o", brows: "up" } : t < E[2] + .2 ? { eyes: "wide", mouth: "o", brows: "up", talk: who(t, "rosa"), noblink: true } : { eyes: t < L[4] ? "happy" : "open", mouth: "smile", brows: "up", talk: who(t, "rosa") };
  }
  placeChar(ROSA, true, idle(p, t, ROSA.seed), f);
}
function updTheo(t, s) {
  CUPS.forEach((c) => { c.visible = false; });
  if (s === 0 && t < M0) {
    const p = pose({ x: .62, z: .15, ry: -.25, a: [[.15, .2, .35], [.15, .2, .35]], hy: -.5, hp: .12 });
    placeChar(THEO, true, idle(p, t, THEO.seed), { eyes: "open", mouth: "smile", brows: "flat", talk: who(t, "theo") });
  } else if (s === 3 && t > L[3] - 1.6) {
    const u = clamp((t - (L[3] - 1.6)) / 1.5), a = along([[DOORX - .05, 3.7], [DOORX - .25, 2.6], [2.15, 1.75]], u);
    let p = pose({ x: a.x, z: a.z, ry: u < 1 ? a.ry : -2.3, a: [[1.05, .1, .9], [1.05, .1, .9]] });
    if (u < 1) { p = walk(p, t * 8.5, 1); p.a = [[1.05, .1, .9], [1.05, .1, .9]]; }
    placeChar(THEO, true, idle(p, t, THEO.seed), { eyes: "open", mouth: t > E[3] ? "grin" : "smirk", brows: "up", talk: who(t, "theo") });
    CUPS.forEach((c, k) => { c.visible = true; holdAt(THEO, k, c, [0, -.12, .07]); });
  } else THEO.root.visible = false;
}

// ---------------------------------------------------------------- the automation streams and the neon
const SPEED = .55, PER = 26;
function signOn(k, t) { return t < NT[k] ? 0 : t < NT[k] + .5 ? (hash(Math.floor(t * 24) + k * 7) > .45 ? 1 : .15) : 1; }
function updFlow(t, s) {
  const pu = new THREE.Vector3(), mid = new THREE.Vector3();
  for (let k = 0; k < 6; k++) {
    const start = NT[k] - .8, active = s > 0 && t > start && t < DUR;
    const surge = s === 2 ? 1 + 1.6 * ss(t, V0 + .2, V0 + 1.0) : 1;
    const to = NEON[k].clone().add(v(0, -.15, .08));
    mid.set((PHONE.x + to.x) / 2 + (k - 2.5) * .15, 3.0 + (k % 3) * .08, (PHONE.z + to.z) / 2);
    for (let i = 0; i < PER; i++) {
      const idx = k * PER + i;
      let sc = 0;
      if (active) {
        const age = t - start, dens = s === 3 ? .35 : (age < 2.5 ? 1 : .45) * surge;
        const u = ((t - start) * SPEED * (s === 2 ? 1.8 : 1) + i / PER) % 1;
        const born = u * (1 / SPEED) <= age + .01;
        if (born && hash(i * 3.3 + k) < dens) {
          const a = (1 - u) * (1 - u), b = 2 * u * (1 - u), c = u * u;
          pu.set(PHONE.x * a + mid.x * b + to.x * c, (PHONE.y + .05) * a + mid.y * b + to.y * c, PHONE.z * a + mid.z * b + to.z * c);
          pu.x += .05 * Math.sin(t * 3 + i * 1.7); pu.y += .04 * Math.cos(t * 2.6 + i);
          sc = Math.min(1, u * 8, (1 - u) * 6) * (s === 3 ? .7 : 1);
          V.copy(pu); EU.set(t * 2 + i, t * 1.5 + i * .5, 0); Q.setFromEuler(EU); M4.compose(V, Q, S.set(sc, sc, sc)); R.flow.setMatrixAt(idx, M4);
          continue;
        }
      }
      M4.compose(V.set(0, -10, 0), Q.identity(), S.set(0, 0, 0)); R.flow.setMatrixAt(idx, M4);
    }
  }
  R.flow.instanceMatrix.needsUpdate = true;
}
let flowColored = false;
function colorFlow() { if (flowColored) return; flowColored = true; for (let k = 0; k < 6; k++) for (let i = 0; i < PER; i++) R.flow.setColorAt(k * PER + i, tmpC.set(C.neonCol[k]).offsetHSL(0, 0, (hash(i * 2.1) - .5) * .15)); R.flow.instanceColor.needsUpdate = true; }

// ---------------------------------------------------------------- per frame
let SHAKE = 0;
function updCafe(t, s) {
  colorFlow();
  const night = s < 3, dawn = ss(t, D0 - .1, D0 + 2.5);
  const min = clockMin(t), hrs = (min / 60) % 12;
  R.hands[0].rotation.x = -hrs / 12 * Math.PI * 2; R.hands[1].rotation.x = -(min % 60) / 60 * Math.PI * 2;
  // neon signs
  let vp = s === 2 ? .5 + .5 * Math.sin(t * 9) : 0;
  NEON.forEach((p, k) => {
    const on = signOn(k, t);
    setMap(R.neon[k].m, TEX[on > .5 ? "neon" + k : "neonOff" + k]);
    R.neon[k].m.opacity = s === 3 ? 1 - .75 * ss(t, C.endc - .2, C.endc + .5) : 1;
    PL[k].position.copy(p).add(v(0, -.2, .9)); PL[k].color.set(C.neonCol[k]); PL[k].intensity = on * (night ? 2.4 : .6) * (1 + .8 * vp); PL[k].distance = 5.5;
  });
  // lamps inside and out, the phone, the sky, the street
  R.pendants.forEach((m, k) => { m.emissiveIntensity = night ? (k === 0 ? .8 : (t < M0 ? .6 : 0)) : 0; });
  PL[6].position.set(TABLE.x, 2.3, TABLE.z); PL[6].color.set(0xFFC98A); PL[6].intensity = night ? 3.2 : 0; PL[6].distance = 6;
  R.streetL.forEach((l) => { l.intensity = night ? 6 : 0; }); R.spill.intensity = night ? 3 : 0;
  R.clockM.color.setScalar(night ? .55 : .9);
  const phoneLit = s === 2 || (t < M0) || (s === 1 && NT.some((n) => t > n - .8 && t < n + .6)) || (s === 3 && t > L[2] - .5 && t < E[2] + .5);
  PL[7].position.set(PHONE.x, PHONE.y + .35, PHONE.z); PL[7].color.set(0xCFE0FF); PL[7].intensity = phoneLit ? (s === 2 ? .7 + .4 * vp : .7) : .15; PL[7].distance = 1.6;
  if (!night) { PL[6].position.set(.2, 1.9, 2.6); PL[6].color.set(0xFFC890); PL[6].intensity = 2.4; PL[6].distance = 7; }
  R.lampM.emissiveIntensity = night ? 1.6 : 0; R.bldM.emissiveIntensity = night ? 1.0 : .05 * (1 - dawn);
  R.skyDawn.material.opacity = dawn;
  const mu = clamp((t - M0) / (V0 + 3 - M0));                                   // the moon crosses the sky during the montage
  R.moon.position.set(lerp(-26, 22, mu), 24 + 10 * Math.sin(mu * Math.PI), -60); R.moon.lookAt(0, 2, 6); R.moon.visible = night;
  R.sunDisc.position.set(-14, lerp(6, 14, ss(t, D0, DUR)), -60); R.sunDisc.lookAt(0, 2, 6); R.sunDisc.visible = !night;
  setMap(R.signM, TEX[night ? "closed" : "open"]);
  // the cat walks past during sign 1's cutaway
  const cu = clamp((t - (NT[1] + 1.2)) / 4.2);
  R.cat.visible = s === 1 && cu > 0 && cu < 1; R.cat.position.set(lerp(-5.5, 4.5, cu), .02, 3.75); R.cat.rotation.y = 0;
  R.catLegs.forEach((g, k) => { g.rotation.z = .6 * Math.sin(t * 12 + (k % 2) * Math.PI + (k > 1 ? Math.PI : 0)); });
  R.catTail.rotation.z = .5 + .2 * Math.sin(t * 3);
  // the door: Theo comes in at dawn
  const dOpen = s === 3 ? bump(t, L[3] - 1.7, L[3] - .5, .35) : 0;
  R.door.rotation.y = -1.25 * dOpen; R.bell.rotation.z = .4 * Math.sin(t * 30) * bump(t, L[3] - 1.7, L[3] - .9, .1);
  // screens
  if (s === 0) setMap(R.lapM, DYN.lapFlow(clamp((t - L[1]) / 2.5)));
  else setMap(R.lapM, DYN.lapFlow(1));
  const handled = C.handledAt(t), booked = C.bookedAt(t);
  setMap(R.phoneM, s === 0 ? TEX.phoneUnread : s === 2 && t < V0 + 4.5 ? DYN.phoneViral(clamp((t - V0) / 3)) : DYN.phoneCount(Math.round(handled), Math.round(booked)));
  SHAKE = s === 2 ? .35 * pulse(t, V0 + 1.0, .3) : 0;
  updRosa(t, s); updTheo(t, s); updFlow(t, s);
  return { night, dawn, vp };
}
C.handledAt = (t) => { const K = C.handled; let i = 0; while (i + 1 < K.length && t >= K[i + 1][0]) i++; const [a, x] = K[i], [b, y] = K[Math.min(i + 1, K.length - 1)]; return b > a ? lerp(x, y, clamp((t - a) / (b - a))) : x; };
C.bookedAt = (t) => { const K = C.booked; let i = 0; while (i + 1 < K.length && t >= K[i + 1][0]) i++; const [a, x] = K[i], [b, y] = K[Math.min(i + 1, K.length - 1)]; return b > a ? lerp(x, y, clamp((t - a) / (b - a))) : x; };

const LOOK_NIGHT = { bg: 0x070A16, hs: 0x6478B0, hg: 0x2A2430, hi: .85, sun: 0x9FB8FF, si: .45, sd: [.4, .9, 1.0], warm: .05, cool: .3, sat: .95, con: .1, vig: .5 };
const LOOK_DAWN = { bg: 0xF2B98A, hs: 0xFFE6C8, hg: 0xC9A27A, hi: 1.1, sun: 0xFFC890, si: 3.0, sd: [-.45, .42, 1.0], warm: .28, cool: 0, sat: 1.08, con: .07, vig: .36 };
function renderAt(t) {
  if (!TEX.ready) return;
  NOW = t; SHAKE = 0;
  const s = sceneOf(t);
  for (const k in SET) SET[k].visible = true;
  for (const l of PL) l.intensity = 0;
  const Lk = s < 3 ? LOOK_NIGHT : LOOK_DAWN;
  scene.background = tmpC.set(Lk.bg).clone();
  scene.fog.color.set(Lk.bg); scene.fog.near = 30; scene.fog.far = 140;
  hemi.color.set(Lk.hs); hemi.groundColor.set(Lk.hg); hemi.intensity = Lk.hi;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  const sh = shotAt(t);
  const st = updCafe(t, s);
  const shk = SHAKE, hand = .003;
  camera.position.copy(sh.p).add(V.set(Math.sin(t * .9) * hand + shk * .03 * Math.sin(t * 61), Math.sin(t * 1.3 + 1) * hand + shk * .03 * Math.sin(t * 53), 0));
  camera.fov = sh.fov;
  const cv = window.AP_COVER;
  if (cv && cv.cam) { camera.position.set(...cv.cam); sh.l.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix(); camera.up.set(0, 1, 0); camera.lookAt(sh.l);
  if (shk) camera.rotateZ(shk * .015 * Math.sin(t * 47));
  scene.updateMatrixWorld(true);
  cocPass.uniforms.uF.value = sh.f; cocPass.uniforms.uAp.value = sh.ap;
  if (cv) { cocPass.uniforms.uAp.value = cv.ap ?? sh.ap; if (cv.focus) cocPass.uniforms.uF.value = cv.focus; }
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = Lk.warm; gu.uCool.value = Lk.cool; gu.uSat.value = Lk.sat; gu.uCon.value = Lk.con; gu.uVig.value = Lk.vig;
  gu.uFlash.value = s === 2 ? .12 * pulse(t, V0 + 1.0, .25) : 0; gu.uCA.value = .0012 + shk * .004;
  gu.uTop.value = cv ? 0 : Math.max(1 - ss(t, 2.4, 3.1), ss(t, C.endc, C.endc + .6) * .9);
  gu.uDark.value = 0;
  bloom.strength = s < 3 ? .62 : .3;
  sun.target.position.set(0, 0, 0); sun.position.copy(sun.target.position).add(S.set(...Lk.sd).normalize().multiplyScalar(30));
  Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 1, far: 70 });
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures that need the fonts
const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`, SERIF = (w, f, it = false) => `${it ? "italic " : ""}${w} ${f}px Garamond, serif`;
const text = (w, h, draw) => pix(w, h, draw, false);
const block = (g, x, y, w, h, c, r = 14) => { g.fillStyle = c; rr(g, x, y, w, h, r); g.fill(); };
const label = (g, s, x, y, f, c, al = "left", wt = 800) => { g.font = FT(wt, f); g.fillStyle = c; g.textAlign = al; g.fillText(s, x, y); g.textAlign = "left"; };
const DYN = {};
function dyn(key, w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  let last = null;
  DYN[key] = (...a) => { const k = a.join("|"); if (k !== last) { last = k; draw(g, w, h, ...a); tx.needsUpdate = true; } return tx; };
}
function buildTextures() {
  // ---- the neon signs: the tool's name in glowing tubes, and the same tubes unlit
  C.neonNames.forEach((nm, k) => {
    const col = C.neonCol[k];
    const draw = (lit) => text(720, 224, (g, w, h) => {
      g.clearRect(0, 0, w, h);
      g.textAlign = "center"; g.textBaseline = "middle"; g.lineJoin = "round"; let fs = 104; g.font = FT(800, fs); while (g.measureText(nm).width > 640 && fs > 40) { fs -= 4; g.font = FT(800, fs); }
      if (lit) {
        g.shadowColor = col; g.shadowBlur = 34; g.strokeStyle = col; g.lineWidth = 12; g.strokeText(nm, w / 2, h / 2 - 8);
        g.shadowBlur = 12; g.strokeStyle = "#FFFFFF"; g.lineWidth = 4; g.strokeText(nm, w / 2, h / 2 - 8);
        g.shadowBlur = 0; g.font = FT(800, 26); g.fillStyle = col; g.fillText(C.neonSub[k], w / 2, h - 26);
      } else {
        g.strokeStyle = "rgba(170,170,190,.28)"; g.lineWidth = 8; g.strokeText(nm, w / 2, h / 2 - 8);
      }
    });
    TEX["neon" + k] = draw(true); TEX["neonOff" + k] = draw(false);
  });
  TEX.windowText = text(660, 210, (g, w, h) => { g.clearRect(0, 0, w, h); g.textAlign = "center"; g.fillStyle = "rgba(242,201,76,.9)"; g.font = SERIF(700, 120, true); g.fillText("Rosa's", w / 2, 128); g.font = FT(800, 30); g.fillText("COFFEE · BAKERY", w / 2, 186); });
  TEX.frontSign = text(960, 210, (g, w, h) => { g.fillStyle = "#1E1B18"; g.fillRect(0, 0, w, h); g.textAlign = "center"; g.shadowColor = "#FFB547"; g.shadowBlur = 26; g.fillStyle = "#FFD9A0"; g.font = SERIF(700, 132, true); g.fillText("Rosa's Café", w / 2, 150); });
  TEX.closed = text(256, 160, (g, w, h) => { g.fillStyle = "#1E1B18"; g.fillRect(0, 0, w, h); g.strokeStyle = "#E5484D"; g.lineWidth = 8; g.strokeRect(10, 10, w - 20, h - 20); label(g, "CLOSED", w / 2, 104, 54, "#E5484D", "center"); });
  TEX.open = text(256, 160, (g, w, h) => { g.fillStyle = "#1E1B18"; g.fillRect(0, 0, w, h); g.strokeStyle = "#5BE38A"; g.lineWidth = 8; g.strokeRect(10, 10, w - 20, h - 20); label(g, "OPEN", w / 2, 104, 64, "#5BE38A", "center"); });
  TEX.chalk = text(560, 400, (g, w, h) => { g.fillStyle = "#202622"; g.fillRect(0, 0, w, h); g.strokeStyle = "#7A4A2A"; g.lineWidth = 18; g.strokeRect(0, 0, w, h); g.fillStyle = "#F4F1E6"; g.font = SERIF(700, 50, true); g.textAlign = "center"; g.fillText("Today", w / 2, 70); g.font = FT(700, 30); g.textAlign = "left"; [["Flat white", "4.5"], ["Iced latte", "5"], ["Croissant", "3.5"], ["Banana bread", "4"]].forEach(([a, b], k) => { g.fillText(a, 50, 140 + k * 60); g.textAlign = "right"; g.fillText(b, w - 50, 140 + k * 60); g.textAlign = "left"; }); });
  TEX.clock = text(256, 256, (g) => { g.fillStyle = "#FFFDF8"; g.beginPath(); g.arc(128, 128, 124, 0, 7); g.fill(); g.strokeStyle = "#1E1B18"; g.lineWidth = 10; g.stroke(); for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; g.fillStyle = "#1E1B18"; g.fillRect(128 + Math.sin(a) * 100 - 5, 128 - Math.cos(a) * 100 - 5, 10, 10); } });
  TEX.bld = text(128, 256, (g, w, h) => { g.fillStyle = "#3A3E52"; g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = 0; j < 8; j++) { g.fillStyle = hash(i * 7 + j * 3) > .45 ? "#FFD9A0" : "#1E2236"; g.fillRect(10 + i * 30, 12 + j * 30, 18, 20); } });
  R.bldM.emissiveMap = TEX.bld; R.bldM.needsUpdate = true;
  const sky = (stops, stars) => text(512, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); for (let k = 0; k < stars; k++) px(g, "rgba(255,255,255,.85)", Math.floor(hash(k) * 512), Math.floor(hash(k * 3) * 230), 1.5, 1.5); });
  TEX.skyNight = sky([[0, "#05081A"], [.42, "#0E1636"], [.52, "#26325E"], [1, "#1A1A24"]], 400);
  TEX.skyDawn = sky([[0, "#5B7FC4"], [.36, "#F2A57A"], [.5, "#FFD9A0"], [1, "#C9A27A"]], 0);
  // ---- her phone: 200 unread; the night's tally; the viral flood
  TEX.phoneUnread = text(144, 300, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#2A1A30"); gr.addColorStop(1, "#0C0F1A"); g.fillStyle = gr; g.fillRect(0, 0, w, h); label(g, "11:04", w / 2, 50, 30, "#FFFFFF", "center"); block(g, 22, 90, 100, 100, "#E5484D", 50); label(g, "200", w / 2, 155, 46, "#FFFFFF", "center"); label(g, "unread", w / 2, 222, 20, "#FFB4AE", "center"); });
  dyn("phoneCount", 144, 300, (g, w, h, n, b) => { g.fillStyle = "#0C1410"; g.fillRect(0, 0, w, h); label(g, "AUTOPILOT", w / 2, 40, 16, "#5BE38A", "center"); label(g, String(n), w / 2, 120, 44, "#FFFFFF", "center"); label(g, "handled", w / 2, 146, 16, "#9AA0AC", "center"); label(g, String(b), w / 2, 214, 40, "#5BE38A", "center"); label(g, "bookings", w / 2, 240, 16, "#9AA0AC", "center"); });
  dyn("phoneViral", 144, 300, (g, w, h, u) => { g.fillStyle = "#14081A"; g.fillRect(0, 0, w, h); const n = Math.min(7, Math.floor(u * 9)); for (let k = 0; k < n; k++) { block(g, 8, 18 + k * 38, w - 16, 32, "rgba(255,255,255,.92)", 8); block(g, 13, 23 + k * 38, 22, 22, ["#E1306C", "#5BE38A", "#4FC3FF"][k % 3], 6); block(g, 42, 28 + k * 38, 80, 6, "#14161C", 3); block(g, 42, 38 + k * 38, 54, 5, "#9AA0AC", 3); } label(g, "+" + Math.round(900 * u), w / 2, h - 18, 30, "#FFD34A", "center"); });
  // ---- the laptop: the automation canvas Theo sets up (nodes appear, then wires)
  dyn("lapFlow", 620, 400, (g, w, h, u) => {
    g.fillStyle = "#14121C"; g.fillRect(0, 0, w, h); label(g, "Autopilot · 6 flows", 24, 40, 24, "#FFFFFF");
    const N = [[90, 130, "New DM"], [300, 130, "Inbox"], [510, 130, "Reply"], [90, 280, "Book"], [300, 280, "Email"], [510, 280, "CRM"]];
    const k = Math.round(u * 6);
    for (let i = 0; i < Math.min(k, 5); i++) { const [x1, y1] = N[i], [x2, y2] = N[i + 1]; g.strokeStyle = "#B987FF"; g.lineWidth = 5; g.beginPath(); g.moveTo(x1 + 55, y1); g.lineTo(x2 - 55, y2); g.stroke(); }
    N.forEach(([x, y, s], i) => { const on = i < k; block(g, x - 80, y - 34, 160, 68, on ? C.neonCol[i] : "#2A2836", 14); label(g, s, x, y + 9, 24, on ? "#0B0D12" : "#6A6878", "center"); });
  });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  TEX.ready = true;
}

const ready = (async () => {
  try { const jb = new FontFace("JBMono", "url(assets/fonts/jbmono-bold.ttf)", { weight: "700" }); document.fonts.add(await jb.load()); } catch (e) { /* fall back */ }
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 40px Manrope"), document.fonts.load("700 40px Garamond"), document.fonts.load("italic 700 40px Garamond")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  for (const k in SET) SET[k].visible = true;
  renderer.compile(scene, camera);
  renderAt(window.AP_COVER ? window.AP_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["autopilot"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.AP_COVER ? window.AP_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C, R };
