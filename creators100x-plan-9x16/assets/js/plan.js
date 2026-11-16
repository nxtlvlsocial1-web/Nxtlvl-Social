// Creedom "I Wish..." reel, v3: a stressed creator in his bedroom studio at night makes three wishes, and Cree, Creedom's
// mascot, answers them like a flying superhero. Soft designer-toy 3D (a smooth toy-style creator with a face rig; Cree to
// his model sheet), clean light with no grain or heavy glow. Everything is a pure function of time t, drawn on hf-seek.
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
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
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
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .12, .4, .92);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1 }, uVig: { value: .26 }, uFlash: { value: 0 }, uCool: { value: 0 }, uWarm: { value: 0 },
    uCA: { value: 0 }, uCon: { value: 0 }, uDark: { value: 0 }, uTop: { value: 0 }, uKeep: { value: 1 }, uGrain: { value: .05 }, uTint: { value: 0 } },
  vertexShader: VS,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uCool, uWarm, uCA, uCon, uDark, uTop, uKeep, uGrain, uTint; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 d = vec2(.5) - vUv;
      vec3 c = vec3(texture2D(tDiffuse, vUv + d * uCA).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - d * uCA).b);
      float g = dot(c, vec3(.299, .587, .114));
      // noir: black and white, except strongly saturated light (the red string, alert screens, the lavender signs)
      float mx = max(c.r, max(c.g, c.b)), mn = min(c.r, min(c.g, c.b)), dd = mx - mn, sat = dd / (mx + 1e-4);
      float hu = 0.; if (dd > 1e-4) { if (mx == c.r) hu = mod((c.g - c.b) / dd, 6.); else if (mx == c.g) hu = (c.b - c.r) / dd + 2.; else hu = (c.r - c.g) / dd + 4.; } hu *= 60.;
      float redK = (1. - smoothstep(9., 20., min(hu, 360. - hu))) * smoothstep(.6, .8, sat) * smoothstep(.32, .5, mx);   // only the reds of the story
      float lavK = smoothstep(244., 260., hu) * (1. - smoothstep(298., 315., hu)) * smoothstep(.28, .46, sat) * smoothstep(.25, .42, mx);   // and lavender
      float keep = uKeep * max(redK, lavK);
      c = mix(vec3(g), c, max(uSat, keep));
      c = mix(c, c * vec3(1.04, 1.0, .9), uTint * (1. - keep));
      c = mix(c, c * vec3(.86, .97, 1.14), uCool);
      c = mix(c, c * vec3(1.08, 1.0, .88), uWarm);
      c = (c - .5) * (1. + uCon) + .5;
      vec2 q = vUv - .5; float r = dot(q, q);
      c *= 1. - r * uVig * 2.2;
      c *= 1. - uTop * smoothstep(.2, .75, vUv.y) * .55;        // darker upper half under the title and end card
      vec2 px = vUv * vec2(1080., 1920.);
      c += (h(floor(px * .5) + fract(uTime * 7.13) * 97.) - .5) * uGrain;
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

// ---------------------------------------------------------------- characters: blocky figures with pixel faces (from the house voxel engine), with extra big feelings
const HIP = .82;
// pixel art, 24 x 24: fringe rows 0-4, brows row 8, eyes rows 10-12 at x 6 and 16, nose 13-14, mouth 16-18
function drawFace(g, sp, eyes, mouth, brows) {
  const S = sp.skin, Hc = sp.hair, D = "#1E1B18", Mo = "#5A2A22", Rd = "#C8483A", Wt = "#FFFDF8";
  px(g, S, 0, 0, 24, 24);
  if (sp.style === "cap") { px(g, sp.cap, 0, 0, 24, 5); px(g, shc(sp.cap, -.3), 0, 4, 24, 1); px(g, Hc, 0, 5, 2, 4); px(g, Hc, 22, 5, 2, 4); }
  else {
    px(g, Hc, 0, 0, 24, 4);
    if (sp.style === "fedora") { px(g, sp.hat, 0, 0, 24, 3); px(g, Hc, 0, 3, 3, 4); px(g, Hc, 21, 3, 3, 4); }
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
  const TR = "#8FD3FF";
  if (eyes === "teary") { eye(6, "open"); eye(16, "open"); px(g, TR, 5, 13, 4, 1); px(g, TR, 15, 13, 4, 1); px(g, "#DDF3FF", 6, 11, 1, 1); px(g, "#DDF3FF", 16, 11, 1, 1); }
  else if (eyes === "cry" || eyes === "sob") {
    for (const ex of [6, 16]) {
      if (eyes === "cry") { px(g, D, ex - 1, 10, 1, 1); px(g, D, ex, 11, 2, 1); px(g, D, ex - 1, 12, 1, 1); px(g, D, ex + 2, 10, 1, 1); px(g, D, ex + 2, 12, 1, 1); }
      else { px(g, D, ex - 1, 11, 1, 1); px(g, D, ex, 10, 2, 1); px(g, D, ex + 2, 11, 1, 1); }
      px(g, TR, ex, 13, 2, 7); px(g, "#DDF3FF", ex, 14, 1, 2);
    }
  }
  else { eye(6, eyes === "wink" ? "open" : eyes); eye(16, eyes === "wink" ? "happy" : eyes); }
  const Bc = sp.brow || Hc;
  if (brows === "flat") { px(g, Bc, 5, 8, 4, 1); px(g, Bc, 15, 8, 4, 1); }
  if (brows === "up") { px(g, Bc, 5, 7, 4, 1); px(g, Bc, 15, 7, 4, 1); }
  if (brows === "worry") { px(g, Bc, 5, 8, 2, 1); px(g, Bc, 7, 7, 2, 1); px(g, Bc, 15, 7, 2, 1); px(g, Bc, 17, 8, 2, 1); }
  if (brows === "angry") { px(g, Bc, 5, 7, 2, 1); px(g, Bc, 7, 8, 2, 1); px(g, Bc, 15, 8, 2, 1); px(g, Bc, 17, 7, 2, 1); }
  if (brows === "raise1") { px(g, Bc, 5, 6, 4, 1); px(g, Bc, 15, 8, 4, 1); }
  if (brows === "despair") { px(g, Bc, 4, 9, 2, 1); px(g, Bc, 6, 8, 2, 1); px(g, Bc, 8, 7, 1, 1); px(g, Bc, 15, 7, 1, 1); px(g, Bc, 16, 8, 2, 1); px(g, Bc, 18, 9, 2, 1); }
  if (brows === "high") { px(g, Bc, 5, 6, 4, 1); px(g, Bc, 15, 6, 4, 1); }
  if (mouth === "smile") { px(g, Mo, 10, 17, 4, 1); px(g, Mo, 9, 16, 1, 1); px(g, Mo, 14, 16, 1, 1); }
  if (mouth === "grin") { px(g, Mo, 9, 16, 6, 2); px(g, Wt, 10, 16, 4, 1); px(g, Mo, 8, 15, 1, 1); px(g, Mo, 15, 15, 1, 1); }
  if (mouth === "talk") { px(g, Mo, 10, 16, 4, 2); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "o") { px(g, Mo, 11, 16, 2, 1); px(g, Mo, 10, 17, 1, 1); px(g, Mo, 13, 17, 1, 1); px(g, Mo, 11, 18, 2, 1); px(g, Rd, 11, 17, 2, 1); }
  if (mouth === "flat") px(g, Mo, 10, 17, 4, 1);
  if (mouth === "wavy") { px(g, Mo, 9, 17, 1, 1); px(g, Mo, 10, 16, 2, 1); px(g, Mo, 12, 17, 1, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "sad") { px(g, Mo, 10, 16, 4, 1); px(g, Mo, 9, 17, 1, 1); px(g, Mo, 14, 17, 1, 1); }
  if (mouth === "smirk") { px(g, Mo, 10, 17, 3, 1); px(g, Mo, 13, 16, 2, 1); }
  if (mouth === "laugh") { px(g, Mo, 9, 16, 6, 3); px(g, Wt, 10, 16, 4, 1); px(g, Rd, 10, 17, 4, 2); }
  if (mouth === "wail") { px(g, Mo, 8, 15, 8, 5); px(g, Rd, 9, 17, 6, 2); px(g, Wt, 9, 15, 6, 1); }
  if (mouth === "gasp") { px(g, Mo, 10, 15, 4, 4); px(g, Rd, 11, 16, 2, 2); }
  if (mouth === "rant") { px(g, Mo, 9, 15, 6, 4); px(g, Wt, 9, 15, 6, 1); px(g, Rd, 10, 17, 4, 1); }
  if (sp.glasses) {
    const G = sp.glasses;
    for (const x0 of [4, 14]) { px(g, G, x0, 9, 6, 1); px(g, G, x0, 13, 6, 1); px(g, G, x0, 9, 1, 5); px(g, G, x0 + 5, 9, 1, 5); }
    px(g, G, 10, 10, 4, 1); px(g, G, 0, 10, 4, 1); px(g, G, 20, 10, 4, 1);
  }
}
const FACES = new Map(), CHM = new Map(), P_COAT = new Map();
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
const headBack = (sp) => pix(24, 24, (g) => { px(g, sp.skin, 0, 0, 24, 24); px(g, sp.style === "cap" ? sp.cap : sp.hair, 0, 0, 24, sp.style === "short" || sp.style === "puff" || sp.style === "fedora" ? 18 : 24); if (sp.style === "cap") px(g, sp.hair, 0, 8, 24, 10); });
const solidTex = (c) => pix(4, 4, (g) => px(g, c, 0, 0, 4, 4));
function torsoTex(sp, back) {
  return pix(16, 20, (g) => {
    const T = sp.top, Dk = shc(T, -.22), Lt = shc(T, .25);
    px(g, T, 0, 0, 16, 20);
    if (sp.topStyle === "hoodie") { px(g, Dk, 0, 0, 16, 2); px(g, Dk, 0, 18, 16, 2); if (back) px(g, Dk, 3, 1, 10, 5); else { px(g, "#FFFDF8", 6, 2, 1, 6); px(g, "#FFFDF8", 9, 2, 1, 6); px(g, Dk, 3, 12, 10, 5); px(g, T, 4, 13, 8, 3); } }
    if (sp.topStyle === "blazer" && !back) { px(g, "#FFFDF8", 6, 0, 4, 12); px(g, "#FFFDF8", 7, 12, 2, 2); px(g, Dk, 5, 0, 1, 12); px(g, Dk, 10, 0, 1, 12); px(g, "#F2B33D", 7, 14, 2, 1); px(g, "#F2B33D", 7, 17, 2, 1); px(g, "#E8735A", 12, 5, 2, 1); }
    if (sp.topStyle === "tee") { if (!back) { px(g, Dk, 5, 0, 6, 1); px(g, Dk, 6, 1, 4, 1); px(g, Lt, 9, 5, 3, 3); } px(g, Dk, 0, 19, 16, 1); }
    if (sp.topStyle === "trench") { px(g, Dk, 0, 12, 16, 2); px(g, "#1E1B18", 7, 12, 2, 2); if (!back) { px(g, "#E9E4DA", 6, 0, 4, 5); px(g, Dk, 4, 0, 2, 9); px(g, Dk, 10, 0, 2, 9); px(g, Dk, 5, 9, 1, 2); px(g, Dk, 10, 9, 1, 2); for (const y of [6, 9, 15, 18]) { px(g, Lt, 4, y, 1, 1); px(g, Lt, 11, y, 1, 1); } } else px(g, Dk, 7, 14, 2, 6); }
    if (sp.topStyle === "apron") { if (!back) { px(g, "#F4F1EA", 3, 6, 10, 14); px(g, "#F4F1EA", 4, 0, 1, 6); px(g, "#F4F1EA", 11, 0, 1, 6); px(g, "#DDD6C8", 5, 13, 6, 3); } else { px(g, "#F4F1EA", 0, 12, 16, 1); px(g, "#F4F1EA", 4, 0, 1, 12); px(g, "#F4F1EA", 11, 0, 1, 12); } }
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
  if (sp.topStyle === "trench") { mk(Bx(.6, .16, .34), M(shc(sp.top, -.12)), torso, 0, .6, -.02); }    // the turned-up collar
  mk(Bx(.22, .08, .2), skinM, torso, 0, .64, 0);
  const neck = new THREE.Group(); neck.position.y = .66; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head);
  const faceM = M(0xffffff, faceTex(sp, "open", "smile", "flat"));
  const sideM = M(0xffffff, headSide(sp));
  const capC = sp.style === "cap" ? sp.cap : sp.hair;
  mk(Bx(.52, .52, .52), [sideM, sideM, M(capC), skinM, faceM, M(0xffffff, headBack(sp))], head, 0, .26, 0);
  const hm = M(capC);
  if (sp.style === "fedora") { const hatM = M(sp.hat), band = M("#141210"); mk(Bx(.56, .1, .56), hairM, head, 0, .47, 0); mk(Bx(.8, .035, .8), hatM, head, 0, .53, .02); mk(Bx(.54, .2, .52), hatM, head, 0, .64, 0); mk(Bx(.555, .06, .535), band, head, 0, .57, 0); mk(Bx(.3, .04, .5), M(shc(sp.hat, -.1)), head, 0, .75, 0); }
  else if (sp.style === "cap") { mk(Bx(.56, .17, .56), hm, head, 0, .5, 0); mk(Bx(.5, .04, .24), M(shc(sp.cap, -.15)), head, 0, .425, .36); }
  else {
    mk(Bx(.56, .13, .56), hairM, head, 0, .475, 0);
    if (sp.style === "short") mk(Bx(.22, .07, .2), hairM, head, .07, .57, .06);
    if (sp.style === "long" || sp.style === "bun") { mk(Bx(.58, .7, .08), hairM, head, 0, .18, -.3); for (const s of [-1, 1]) mk(Bx(.06, .5, .24), hairM, head, s * .29, .22, -.12); }
    if (sp.style === "bun") mk(Bx(.22, .2, .22), hairM, head, 0, .63, -.1);
    if (sp.style === "bob") { for (const s of [-1, 1]) mk(Bx(.06, .36, .44), hairM, head, s * .29, .3, -.03); mk(Bx(.58, .4, .08), hairM, head, 0, .3, -.3); }
    if (sp.style === "puff") mk(Bx(.44, .3, .4), hairM, head, 0, .66, -.04);
  }
  if (sp.earring) for (const s of [-1, 1]) mk(Bx(.04, .06, .04), holo ? M(GOLD) : goldM, head, s * .275, .12, .04);
  if (sp.topStyle === "trench") { const cm2 = M(sp.top); mk(Bx(.6, .5, .34), cm2, hips, 0, -.3, -.01); P_COAT.set(sp.id, true); }
  if (sp.topStyle === "apron") mk(Bx(.48, .5, .03), M("#F4F1EA"), hips, 0, -.25, .15);
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
  if (f.talk) { const ph = Math.floor(NOW * 8.5 + P.seed) % 3; mouth = ph === 0 ? (f.mouth || "smile") : (ph === 1 ? (f.big ? "rant" : "talk") : (f.big ? "wail" : "o")); }
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
// ================================================================= THE STUDIO (Creators 100X colours: warm off-white, lime, hot pink, ink)
// A bright creator studio. The back wall (z = -2.3) holds the 30-day calendar board (6 x 5 slots); the desk with the laptop
// is front left, Jules's chair behind it; the pink couch, the side table and the kettle are right; a window on the left wall.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const RM = mkSet("room");
const DESKY = .78, DESK = v3(-1.3, DESKY, -.55), SEAT = v3(-1.3, 0, -1.15), SITY = .52 - .71;
const INKC = 0x101111, PINK = 0xFD0B68, LIME = 0xCCFB79, OFF = 0xFDF4F4;
const rbox = (w, h, d, c, x, y, z, r = .03, o = {}) => box(w, h, d, c, x, y, z, { round: r, ...o });
const soft = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .7, sheen: .6, sheenColor: new THREE.Color(0xffffff), sheenRoughness: .6, ...o });
// the calendar board geometry (shared with the shots)
const CAL = { cx: .55, cy: 1.72, z: -2.22, cols: 6, rows: 5, sw: .48, sh: .36, gap: .06 };
CAL.x0 = CAL.cx - (CAL.cols * CAL.sw + (CAL.cols - 1) * CAL.gap) / 2 + CAL.sw / 2;
CAL.y0 = CAL.cy + (CAL.rows * CAL.sh + (CAL.rows - 1) * CAL.gap) / 2 - CAL.sh / 2;
const slotPos = (i) => v3(CAL.x0 + (i % CAL.cols) * (CAL.sw + CAL.gap), CAL.y0 - Math.floor(i / CAL.cols) * (CAL.sh + CAL.gap), CAL.z);
// the plan: which pillar each day gets (0 teach, 1 story, 2 proof), never more than twice in a row
const PLAN = [0, 1, 2, 0, 0, 1, 2, 1, 0, 2, 0, 1, 1, 2, 0, 2, 1, 0, 0, 2, 1, 0, 2, 2, 1, 0, 1, 2, 0, 1];
const PILLC = [LIME, PINK, INKC];
{
  const plank = pix(256, 256, (g) => { px(g, "#D9B38C", 0, 0, 256, 256); for (let j = 0; j < 8; j++) { const c = ["#DDB892", "#D4AD86", "#E0BC97", "#D7B089"][j % 4]; px(g, c, 0, j * 32, 256, 32); px(g, "#C19A73", 0, j * 32, 256, 2); px(g, "#C19A73", (j * 97) % 256, j * 32, 2, 32); } }, false);
  flat(10, 9, new THREE.MeshStandardMaterial({ map: rep(plank, 4, 4), roughness: .5, envMap: ENV, envMapIntensity: .15 }), 0, 0, 0);
  const wallM = mat(OFF, { roughness: .95 }), trim = mat(0xFFFFFF, { roughness: .6 });
  box(10, 3.4, .2, wallM, 0, 1.7, -2.4);                                                   // back wall
  // left wall with a window opening (centre z -.6, y 1.7; 1.5 x 1.3)
  { const z0 = -.6 - .75, z1 = -.6 + .75, y0 = 1.7 - .65, y1 = 1.7 + .65;
    box(.2, 3.4, z0 + 2.4, wallM, -3.2, 1.7, (-2.4 + z0) / 2); box(.2, 3.4, 4.5 - z1, wallM, -3.2, 1.7, (z1 + 4.5) / 2);
    box(.2, y0, z1 - z0, wallM, -3.2, y0 / 2, -.6); box(.2, 3.4 - y1, z1 - z0, wallM, -3.2, (y1 + 3.4) / 2, -.6);
    for (const [w, h, z, y] of [[.08, .08, 0, .65], [.08, .08, 0, -.65]]) box(.14, h, 1.56, trim, -3.12, 1.7 + y, -.6);
    box(.14, 1.38, .08, trim, -3.12, 1.7, -.6 - .76); box(.14, 1.38, .08, trim, -3.12, 1.7, -.6 + .76); box(.14, 1.38, .05, trim, -3.12, 1.7, -.6);
    RM.daylight = plane(1.5, 1.3, new THREE.MeshBasicMaterial({ color: 0xEAF6FF, toneMapped: false }), -3.3, 1.7, -.6, Math.PI / 2); }
  box(.2, 3.4, 9, wallM, 3.3, 1.7, 2);
  box(10, .1, 9, mat(0xFFFFFF, { roughness: .95 }), 0, 3.4, 2, { cast: false });
  box(10, .1, .04, trim, 0, .05, -2.29); box(.04, .1, 9, trim, 3.19, .05, 2);
  // a soft lime and pink glow painted on the back wall corners (the brand page look)
  { const gt = pix(256, 256, (g) => { const a = g.createRadialGradient(0, 0, 0, 0, 0, 256); a.addColorStop(0, "rgba(206,251,143,.85)"); a.addColorStop(1, "rgba(206,251,143,0)"); g.fillStyle = a; g.fillRect(0, 0, 256, 256); }, false);
    const pt = pix(256, 256, (g) => { const a = g.createRadialGradient(256, 0, 0, 256, 0, 256); a.addColorStop(0, "rgba(254,112,179,.7)"); a.addColorStop(1, "rgba(254,112,179,0)"); g.fillStyle = a; g.fillRect(0, 0, 256, 256); }, false);
    plane(3.2, 2.6, new THREE.MeshBasicMaterial({ map: gt, transparent: true, depthWrite: false }), -2.6, 2.3, -2.29);
    plane(3.2, 2.6, new THREE.MeshBasicMaterial({ map: pt, transparent: true, depthWrite: false }), 3.0, 2.3, -2.29); }
  // the calendar board: an ink frame, 30 empty slots with day numbers, a coloured block per slot that pops in
  rbox(3.42, 2.42, .06, gloss(INKC, { roughness: .4 }), CAL.cx, CAL.cy, CAL.z - .05, .05);
  rbox(3.42, .26, .07, gloss(INKC, { roughness: .4 }), CAL.cx, CAL.cy + 1.36, CAL.z - .04, .05);
  RM.slots = []; RM.blocks = [];
  RM.numM = texMat("calnums"); plane(3.3, 2.3, RM.numM, CAL.cx, CAL.cy, CAL.z + .021, 0);
  for (let i = 0; i < 30; i++) {
    const p = slotPos(i);
    RM.slots.push(rbox(CAL.sw, CAL.sh, .03, mat(0xF2ECEC, { roughness: .9 }), p.x, p.y, p.z, .025));
    const g = new THREE.Group(); g.position.set(p.x, p.y, p.z + .03); RM.add(g);
    const c = PILLC[PLAN[i]];
    const b = new THREE.Mesh(new RoundedBoxGeometry(CAL.sw - .02, CAL.sh - .02, .07, 3, .03), gloss(c, { roughness: .35, envMapIntensity: .35 })); b.castShadow = true; g.add(b);
    const icM = texMat("icon" + PLAN[i]); const ic = new THREE.Mesh(new THREE.PlaneGeometry(.22, .22), icM); ic.position.set(-.08, .02, .037); g.add(ic);
    const lnM = new THREE.MeshBasicMaterial({ color: PLAN[i] === 2 ? LIME : INKC, toneMapped: false }); for (let k = 0; k < 2; k++) { const ln = new THREE.Mesh(new THREE.PlaneGeometry(k ? .1 : .14, .025), lnM); ln.position.set(.1, .04 - k * .06, .037); g.add(ln); }
    g.visible = false; RM.blocks.push(g);
  }
  // three sticky notes on the board frame: the step cue (they light lime as each step starts)
  RM.notes = []; for (let k = 0; k < 3; k++) { const n = new THREE.Group(); n.position.set(CAL.cx + 1.95, CAL.cy + .7 - k * .55, CAL.z + .02); n.rotation.z = (k - 1) * .08; RM.add(n); const m = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: .8 }); const pm = new THREE.Mesh(new RoundedBoxGeometry(.4, .4, .015, 2, .01), m); n.add(pm); const nm = texMat("note" + k); const np = new THREE.Mesh(new THREE.PlaneGeometry(.36, .36), nm); np.position.z = .009; n.add(np); n.paper = m; RM.notes.push(n); }
  // the logo poster (right of the board)
  RM.logoM = texMat("logo"); plane(.9, .9, RM.logoM, 2.55, 1.75, -2.29, 0);
  // the desk: rounded white top, ink legs, a drawer unit
  rbox(1.6, .06, .72, mat(0xFFFFFF, { roughness: .45, envMap: ENV, envMapIntensity: .2 }), DESK.x, DESKY - .03, DESK.z, .02);
  for (const [x, z] of [[.74, .3], [.74, -.3], [-.74, .3], [-.74, -.3]]) rbox(.05, DESKY - .06, .05, mat(INKC), DESK.x + x, (DESKY - .06) / 2, DESK.z + z, .015);
  // laptop (lid open toward the chair), a mug, a phone tripod
  const lap = new THREE.Group(); lap.position.set(DESK.x + .05, DESKY, DESK.z - .02); lap.rotation.y = Math.PI; RM.add(lap); RM.lap = lap;
  rbox(.44, .018, .3, metal(0xC9C9CF, .35), 0, .009, 0, .006, { parent: lap });
  const lid = new THREE.Group(); lid.position.set(0, .015, -.15); lid.rotation.x = -.3; lap.add(lid); rbox(.44, .29, .014, metal(0xC9C9CF, .35), 0, .145, 0, .006, { parent: lid });
  RM.lapScr = new THREE.MeshBasicMaterial({ color: 0xF6FFE6, toneMapped: false }); { const ls = new THREE.Mesh(new THREE.PlaneGeometry(.4, .25), RM.lapScr); ls.position.set(0, .145, .008); lid.add(ls); }
  { const m = new THREE.Group(); m.position.set(DESK.x + .55, DESKY, DESK.z + .12); RM.add(m); cyl(.045, .042, .1, gloss(PINK), 0, .05, 0, 24, { parent: m }); }
  // the chair
  { const C2 = new THREE.Group(); C2.position.set(SEAT.x, 0, SEAT.z); RM.add(C2); const cw = soft(0x101111); rbox(.52, .07, .5, cw, 0, .5, -.02, .03, { parent: C2 }); rbox(.5, .55, .06, cw, 0, .82, -.27, .05, { parent: C2 }); cyl(.025, .025, .38, metal(0xC8C8D0, .3), 0, .3, 0, 10, { parent: C2 });
    for (let k = 0; k < 5; k++) { const a = k * 1.2566; const leg = rbox(.24, .025, .04, cw, Math.sin(a) * .12, .07, Math.cos(a) * .12, .012, { parent: C2 }); leg.rotation.y = a + Math.PI / 2; } }
  // the ring light, front left
  { const R = new THREE.Group(); R.position.set(-2.4, 0, .4); R.rotation.y = .6; RM.add(R); cyl(.014, .014, 1.45, mat(INKC), 0, .72, 0, 10, { parent: R });
    const rh = new THREE.Mesh(new THREE.TorusGeometry(.25, .035, 12, 64), mat(INKC)); rh.position.y = 1.58; R.add(rh); const rg = new THREE.Mesh(new THREE.TorusGeometry(.25, .018, 10, 64), glow(0xFFF6EA)); rg.position.set(0, 1.58, .02); R.add(rg); }
  // the pink couch, a side table with the kettle, a plant
  { const Cc = new THREE.Group(); Cc.position.set(1.85, 0, -.9); Cc.rotation.y = -.35; RM.add(Cc); RM.couch = Cc; const pm = soft(0xFF5FA2);
    rbox(1.6, .38, .8, pm, 0, .3, 0, .1, { parent: Cc }); rbox(1.6, .55, .2, pm, 0, .62, -.32, .1, { parent: Cc }); for (const s of [-1, 1]) rbox(.2, .5, .8, pm, s * .8, .42, 0, .09, { parent: Cc });
    for (const s of [-1, 1]) rbox(.62, .14, .62, soft(0xFF7DB4), s * .36, .54, .04, .07, { parent: Cc }); rbox(.36, .3, .12, soft(LIME), -.45, .74, -.18, .06, { parent: Cc }); }
  { const T = new THREE.Group(); T.position.set(2.75, 0, .1); RM.add(T); cyl(.26, .26, .04, mat(0xFFFFFF, { roughness: .4 }), 0, .6, 0, 32, { parent: T }); cyl(.03, .03, .58, mat(INKC), 0, .3, 0, 10, { parent: T });
    const K = new THREE.Group(); K.position.set(0, .62, 0); T.add(K); RM.kettle = K; cyl(.1, .12, .2, gloss(0xFFFFFF), 0, .1, 0, 24, { parent: K }); cyl(.04, .06, .03, gloss(INKC), 0, .215, 0, 16, { parent: K });
    const sp = cyl(.018, .024, .12, gloss(0xFFFFFF), .12, .12, 0, 10, { parent: K }); sp.rotation.z = -1; const hd = new THREE.Mesh(new THREE.TorusGeometry(.07, .015, 8, 20, Math.PI), gloss(INKC)); hd.position.set(-.1, .14, 0); hd.rotation.z = Math.PI / 2; K.add(hd); }
  { const P = new THREE.Group(); P.position.set(-2.6, 0, -1.7); RM.add(P); cyl(.17, .13, .32, gloss(0xFFFFFF), 0, .16, 0, 20, { parent: P }); for (let j = 0; j < 9; j++) { const l = new THREE.Mesh(new THREE.SphereGeometry(.13, 10, 8), mat(0x5FAE57)); l.position.set((hash(j) - .5) * .3, .45 + hash(j * 3) * .55, (hash(j * 5) - .5) * .3); l.scale.set(.7, 1.3, .7); P.add(l); } }
  // a round rug
  { const rug = new THREE.Mesh(new THREE.CircleGeometry(1.2, 48), soft(0xE7F9C9, { roughness: .95 })); rug.rotation.x = -Math.PI / 2; rug.scale.set(1.4, .85, 1); rug.position.set(.55, .006, -.5); add(rug, false, true); }
  // lights: bright daylight; the shots tune them
  RM.sunL = new THREE.PointLight(0xFFF2E0, 0, 9, 1.2); RM.sunL.position.set(-2.6, 2.2, -.6); scene.add(RM.sunL);
  RM.key = new THREE.PointLight(0xFFF6EE, 0, 7, 1.4); RM.key.position.set(.3, 2.2, 2.2); scene.add(RM.key);
  RM.fill = new THREE.PointLight(0xF2F6FF, 0, 9, 1.2); RM.fill.position.set(2.4, 2.4, 1.6); scene.add(RM.fill);
  RM.rim = new THREE.PointLight(0xCCFB79, 0, 3.5, 1.6); scene.add(RM.rim);
  RM.pinkL = new THREE.PointLight(0xFD0B68, 0, 3.5, 1.6); scene.add(RM.pinkL);
}
// ---------------------------------------------------------------- the story props: the prompt card and its three input cards, the
// pillars, the temple roof that flips into a menu board, the Day 9 card, the clapperboard, the posting ticks
const FX = {};
{
  const card = (w, h, key, c = 0xFFFFFF) => { const g = new THREE.Group(); const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, .02, 3, .025), gloss(c, { roughness: .4, envMapIntensity: .3 })); m.castShadow = true; g.add(m); const fm = texMat(key); const f = new THREE.Mesh(new THREE.PlaneGeometry(w - .02, h - .02), fm); f.position.z = .011; g.add(f); g.visible = false; RM.add(g); return g; };
  FX.prompt = card(1.0, .62, "prompt");
  FX.inputs = [card(.62, .2, "in0"), card(.62, .2, "in1"), card(.62, .2, "in2")];
  FX.day9 = card(1.15, .82, "day9");
  FX.cols = []; const colC = [LIME, PINK, INKC];
  for (let k = 0; k < 3; k++) { const g = new THREE.Group(); RM.add(g); const m = gloss(colC[k], { roughness: .35, envMapIntensity: .35 });
    const sh = new THREE.Mesh(new THREE.CylinderGeometry(.16, .16, 1.0, 16, 1), m); sh.position.y = .5; sh.castShadow = true; g.add(sh);
    for (const y of [.03, .97]) { const cap = new THREE.Mesh(new RoundedBoxGeometry(.44, .07, .44, 2, .02), m); cap.position.y = y; cap.castShadow = true; g.add(cap); }
    for (let f = 0; f < 8; f++) { const a = f / 8 * Math.PI * 2; const fl = new THREE.Mesh(new THREE.BoxGeometry(.02, .9, .02), mat(shc(colC[k], k === 2 ? .25 : -.12))); fl.position.set(Math.sin(a) * .16, .5, Math.cos(a) * .16); g.add(fl); }
    const lm = texMat("pill" + k); const lp = new THREE.Mesh(new THREE.PlaneGeometry(.46, .14), lm); lp.position.set(0, .62, .2); g.add(lp);
    g.visible = false; FX.cols.push(g); }
  // the temple roof (a pediment) and the menu board it flips into
  FX.roof = new THREE.Group(); RM.add(FX.roof);
  { const sh = new THREE.Shape(); sh.moveTo(-.9, 0); sh.lineTo(.9, 0); sh.lineTo(0, .38); sh.lineTo(-.9, 0); const g = new THREE.ExtrudeGeometry(sh, { depth: .4, bevelEnabled: true, bevelThickness: .02, bevelSize: .02, bevelSegments: 2 }); g.translate(0, 0, -.2);
    const pm = gloss(0xFFFFFF, { roughness: .45 }); const r = new THREE.Mesh(g, pm); r.castShadow = true; FX.roof.add(r); const base = new THREE.Mesh(new RoundedBoxGeometry(1.9, .08, .5, 2, .02), pm); base.position.y = -.04; FX.roof.add(base); }
  FX.roof.visible = false;
  FX.menu = card(1.7, .9, "menu", INKC);
  // the clapperboard
  FX.clap = new THREE.Group(); RM.add(FX.clap);
  { const bm = gloss(INKC, { roughness: .4 }); const b = new THREE.Mesh(new RoundedBoxGeometry(.5, .36, .03, 2, .015), bm); b.castShadow = true; FX.clap.add(b); const fm = texMat("clap"); const f = new THREE.Mesh(new THREE.PlaneGeometry(.46, .26), fm); f.position.set(0, -.03, .016); FX.clap.add(f);
    const hinge = new THREE.Group(); hinge.position.set(-.25, .18, 0); FX.clap.add(hinge); FX.clapTop = hinge; const tm = texMat("claptop"); const top = new THREE.Mesh(new RoundedBoxGeometry(.5, .07, .03, 2, .01), bm); top.position.set(.25, .035, 0); hinge.add(top); const tp = new THREE.Mesh(new THREE.PlaneGeometry(.48, .05), tm); tp.position.set(.25, .035, .016); hinge.add(tp); }
  FX.clap.visible = false;
  // the posting ticks (lime check bubbles that pop over the board on the punchline)
  FX.ticks = []; for (let i = 0; i < 7; i++) { const tm = texMat("tick"); const t = new THREE.Mesh(new THREE.PlaneGeometry(.2, .2), tm); t.visible = false; RM.add(t); FX.ticks.push(t); }
  // the kettle's steam puffs
  FX.steam = []; for (let i = 0; i < 6; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(.05, 10, 8), new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 1, transparent: true, opacity: .7 })); s.visible = false; RM.add(s); FX.steam.push(s); }
  // speed lines (reused from the house kit)
  const slT = pix(16, 256, (g) => { const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(.5, "rgba(255,255,255,.85)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(6, 0, 4, 256); }, false);
  FX.speed = new THREE.Group(); scene.add(FX.speed); FX.speed.visible = false;
  for (let i = 0; i < 10; i++) { const s = new THREE.Mesh(new THREE.PlaneGeometry(.05, 1), new THREE.MeshBasicMaterial({ map: slT, transparent: true, depthWrite: false, opacity: .7 })); s.position.set((hash(i) - .5) * .6, (hash(i * 3) - .5) * .5, -.4 - hash(i * 5) * .6); s.rotation.x = Math.PI / 2; s.scale.y = .5 + hash(i * 7); FX.speed.add(s); }
  FX.ring = new THREE.Mesh(new THREE.RingGeometry(.9, 1, 64), new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: .6, depthWrite: false, side: THREE.DoubleSide })); FX.ring.rotation.x = -Math.PI / 2; FX.ring.visible = false; scene.add(FX.ring);
}
// ---------------------------------------------------------------- the hero FX: a sparkle ribbon behind him in flight, sparks,
// glass glints from the burst window, moon rays behind his silhouette, an air blast and dust on the landing, an eye glint
{
  const glowT = pix(64, 64, (g) => { const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(.3, "rgba(255,225,242,.75)"); gr.addColorStop(1, "rgba(255,150,205,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); }, false);
  const starT = pix(128, 128, (g) => { g.translate(64, 64); for (const [L, W, a] of [[62, 5, 0], [62, 5, Math.PI / 2], [30, 3, Math.PI / 4], [30, 3, -Math.PI / 4]]) { g.save(); g.rotate(a); const gr = g.createLinearGradient(-L, 0, L, 0); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(.5, "rgba(255,255,255,1)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.beginPath(); g.moveTo(-L, 0); g.lineTo(0, -W); g.lineTo(L, 0); g.lineTo(0, W); g.closePath(); g.fill(); g.restore(); } const gr = g.createRadialGradient(0, 0, 0, 0, 0, 16); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(-16, -16, 32, 32); }, false);
  const add2 = (o) => { scene.add(o); o.visible = false; return o; };
  // the ribbon: 48 segments, rebuilt every frame from his flight path (see ribbon() in the shots)
  const RN = 48; const rg = new THREE.BufferGeometry();
  rg.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(RN * 2 * 3), 3));
  rg.setAttribute("color", new THREE.Float32BufferAttribute(new Float32Array(RN * 2 * 4), 4));
  const idx = []; for (let i = 0; i < RN - 1; i++) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } rg.setIndex(idx);
  FX.ribbon = add2(new THREE.Mesh(rg, new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false })));
  FX.ribbon.frustumCulled = false; FX.ribbonN = RN;
  FX.sparks = []; for (let i = 0; i < 46; i++) { const m = new THREE.SpriteMaterial({ map: i % 5 ? glowT : starT, color: i % 3 ? 0xFFD6EC : 0xFFFFFF, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }); FX.sparks.push(add2(new THREE.Sprite(m))); }
  // glass glints: small bright flecks thrown in from the window
  FX.shards = []; for (let i = 0; i < 26; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(.035, .05), new THREE.MeshBasicMaterial({ color: 0xDDEBFF, transparent: true, opacity: .85, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false })); FX.shards.push(add2(m)); }
  // moon rays: long soft wedges fanning out from behind him
  const rayT = pix(64, 256, (g) => { const gr = g.createLinearGradient(0, 256, 0, 0); gr.addColorStop(0, "rgba(220,230,255,.9)"); gr.addColorStop(1, "rgba(220,230,255,0)"); g.fillStyle = gr; g.beginPath(); g.moveTo(30, 256); g.lineTo(34, 256); g.lineTo(64, 0); g.lineTo(0, 0); g.closePath(); g.fill(); }, false);
  FX.rays = add2(new THREE.Group()); for (let i = 0; i < 9; i++) { const p = new THREE.Mesh(new THREE.PlaneGeometry(.55, 2.6), new THREE.MeshBasicMaterial({ map: rayT, transparent: true, opacity: .35, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); p.geometry.translate(0, 1.3, 0); p.rotation.z = (i - 4) * .36 + (hash(i) - .5) * .15; p.scale.x = .35 + hash(i * 3) * .5; FX.rays.add(p); }
  // the air blast: a bright ring that punches out from the landing, facing the camera
  FX.blast = add2(new THREE.Mesh(new THREE.RingGeometry(.86, 1, 72), new THREE.MeshBasicMaterial({ color: 0xFFE6F3, transparent: true, opacity: .6, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false })));
  // the eye glint (a four-point star) and a soft halo for the silhouette
  FX.glint = add2(new THREE.Sprite(new THREE.SpriteMaterial({ map: starT, color: 0xFFFFFF, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })));
  FX.halo = add2(new THREE.Sprite(new THREE.SpriteMaterial({ map: glowT, color: 0xFFB8DC, transparent: true, opacity: .5, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })));
  // bigger dust puffs for the landing (soft sprites)
  FX.dust = []; for (let i = 0; i < 16; i++) FX.dust.push(add2(new THREE.Sprite(new THREE.SpriteMaterial({ map: glowT, color: 0xF8EEF6, transparent: true, opacity: .5, depthWrite: false }))));
}
// fill the ribbon from points (oldest first), facing the camera; width tapers to the tail
function ribbon(pts, camP, w, col = [1, .42, .74]) {
  const g = FX.ribbon.geometry, P = g.attributes.position.array, C = g.attributes.color.array, N = FX.ribbonN;
  FX.ribbon.visible = pts.length > 1;
  for (let i = 0; i < N; i++) {
    const k = Math.min(pts.length - 1, Math.round(i / (N - 1) * (pts.length - 1))), p = pts[k], q = pts[Math.min(pts.length - 1, k + 1)], o = pts[Math.max(0, k - 1)];
    V.copy(q).sub(o).normalize(); V2.copy(camP).sub(p).normalize(); const side = V.clone().cross(V2).normalize();
    const u = i / (N - 1), ww = w * Math.pow(u, .7);
    for (let s = 0; s < 2; s++) { const j = (i * 2 + s); P[j * 3] = p.x + side.x * ww * (s ? 1 : -1); P[j * 3 + 1] = p.y + side.y * ww * (s ? 1 : -1); P[j * 3 + 2] = p.z + side.z * ww * (s ? 1 : -1);
      const a = Math.pow(u, 1.8) * .5 * (s ? 1 : 1); const wh = Math.pow(u, 6) * .6; C[j * 4] = lerp(col[0], 1, wh); C[j * 4 + 1] = lerp(col[1], 1, wh); C[j * 4 + 2] = lerp(col[2], 1, wh); C[j * 4 + 3] = a; }
  }
  g.attributes.position.needsUpdate = true; g.attributes.color.needsUpdate = true;
}
PARENT = scene;
// ---------------------------------------------------------------- VOLT, the AI sidekick: the Creators 100X tile come to life. A glossy
// ink rounded cube with a lime face screen (friendly dark oval eyes with two shines, a smile that talks, pink cheeks), the
// brand's lightning bolt as an antenna (top half white, bottom half lime), two floating hands; he hovers. Built ~.42 m tall.
const VOLT = { root: new THREE.Group() };
scene.add(VOLT.root);
{
  const R = VOLT.root;
  const bod = new THREE.Group(); R.add(bod); VOLT.bod = bod;
  const ink = new THREE.MeshPhysicalMaterial({ color: INKC, roughness: .32, clearcoat: .8, clearcoatRoughness: .15, envMap: ENV, envMapIntensity: .6 });
  const body = new THREE.Mesh(new RoundedBoxGeometry(.36, .34, .3, 4, .09), ink); body.castShadow = true; bod.add(body);
  const scrM = new THREE.MeshStandardMaterial({ color: LIME, emissive: LIME, emissiveIntensity: .25, roughness: .4 });
  const scr = new THREE.Mesh(new RoundedBoxGeometry(.28, .22, .02, 3, .05), scrM); scr.position.set(0, .01, .15); bod.add(scr);
  const eyeM = new THREE.MeshBasicMaterial({ color: 0x101111 }), shM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
  VOLT.eyes = []; VOLT.arcs = [];
  for (const s of [-1, 1]) {
    const eg = new THREE.Group(); eg.position.set(s * .058, .035, .162); bod.add(eg);
    const e = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 16), eyeM); e.scale.set(.027, .036, .006); eg.add(e);
    const c1 = new THREE.Mesh(new THREE.CircleGeometry(.009, 12), shM); c1.position.set(.008, .012, .007); eg.add(c1);
    const c2 = new THREE.Mesh(new THREE.CircleGeometry(.0045, 10), shM); c2.position.set(-.008, -.011, .007); eg.add(c2);
    const arc = new THREE.Mesh(new THREE.TorusGeometry(.022, .006, 8, 20, Math.PI), eyeM); arc.position.set(s * .058, .028, .164); arc.visible = false; bod.add(arc);
    VOLT.eyes.push(eg); VOLT.arcs.push(arc);
  }
  const ckM = new THREE.MeshBasicMaterial({ color: 0xFF7DB4, transparent: true, opacity: .75 });
  for (const s of [-1, 1]) { const c = new THREE.Mesh(new THREE.CircleGeometry(.018, 16), ckM); c.position.set(s * .1, -.022, .1615); c.scale.y = .6; bod.add(c); }
  // mouth: a smile line, and an open mouth that scales with his voice
  VOLT.smile = new THREE.Mesh(new THREE.TorusGeometry(.024, .005, 8, 20, Math.PI), eyeM); VOLT.smile.position.set(0, -.03, .163); VOLT.smile.rotation.z = Math.PI; bod.add(VOLT.smile);
  VOLT.mouth = new THREE.Group(); VOLT.mouth.position.set(0, -.04, .162); bod.add(VOLT.mouth);
  { const mo = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 14), eyeM); mo.scale.set(.028, .018, .004); VOLT.mouth.add(mo); const tg = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), new THREE.MeshBasicMaterial({ color: PINK })); tg.scale.set(.015, .007, .003); tg.position.set(0, -.008, .002); VOLT.mouth.add(tg); }
  // the bolt antenna: a short stem, the upper half white and the lower half lime
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(.012, .014, .06, 10), ink); stem.position.y = .2; bod.add(stem);
  const bolt = new THREE.Group(); bolt.position.set(0, .29, 0); bod.add(bolt); VOLT.bolt = bolt;
  const shp = (pts) => { const s = new THREE.Shape(); s.moveTo(pts[0][0], pts[0][1]); for (const p of pts.slice(1)) s.lineTo(p[0], p[1]); const g = new THREE.ExtrudeGeometry(s, { depth: .026, bevelEnabled: true, bevelThickness: .006, bevelSize: .006, bevelSegments: 2 }); g.translate(0, 0, -.013); return g; };
  const up = new THREE.Mesh(shp([[.012, .11], [-.06, .004], [.012, .004], [.05, .11]]), new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .25, clearcoat: .6 }));
  const lo = new THREE.Mesh(shp([[-.03, .014], [.064, .014], [-.02, -.1]]), new THREE.MeshPhysicalMaterial({ color: LIME, roughness: .25, clearcoat: .6, emissive: LIME, emissiveIntensity: .2 }));
  up.castShadow = lo.castShadow = true; bolt.add(up, lo);
  // floating hands
  VOLT.hands = []; for (const s of [-1, 1]) { const h = new THREE.Mesh(new THREE.SphereGeometry(.05, 18, 14), ink); h.castShadow = true; R.add(h); VOLT.hands.push(h); }
  // a soft contact shadow
  VOLT.shadow = new THREE.Mesh(new THREE.CircleGeometry(.16, 24), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: .22, depthWrite: false })); VOLT.shadow.rotation.x = -Math.PI / 2; scene.add(VOLT.shadow);
}
// s: {x, y, z (hover centre), ry, rx, roll, sc, eyes: open|happy|wide|closed|wink, look: [x, y], talk, hands: [[x,y,z],[x,y,z]] (body
//   space, metres at sc 1), sq, floorY (for the shadow), still}
function placeVolt(vis, s) {
  VOLT.root.visible = !!vis; VOLT.shadow.visible = !!vis && s.floorY !== undefined;
  if (!vis) return;
  const t = NOW, sc = s.sc ?? 1, still = !!s.still;
  const bob = still ? 0 : Math.sin(t * 2.6) * .025, tilt = still ? 0 : Math.sin(t * 1.7) * .05;
  const ta = s.talk ? envAt(C.voltEnv, t) : 0;
  VOLT.root.position.set(s.x, s.y + bob * sc + ta * .012 * sc, s.z); VOLT.root.rotation.set((s.rx ?? 0) - ta * .06, s.ry ?? 0, (s.roll ?? 0) + tilt + ta * .05 * Math.sin(t * 7), "YXZ"); VOLT.root.scale.setScalar(sc);
  const sq = (s.sq ?? 0) - ta * .05; VOLT.bod.scale.set(1 + sq * .5, 1 - sq, 1 + sq * .5);
  const e = s.eyes || "open", blink = (e === "open" || e === "wide") && !s.noblink && blinkAt(4.4, t);
  for (let k = 0; k < 2; k++) {
    const arcs = e === "happy" || (e === "wink" && k === 0);
    VOLT.eyes[k].visible = !arcs; VOLT.arcs[k].visible = arcs;
    const lk = s.look || [0, 0]; VOLT.eyes[k].position.x = (k ? 1 : -1) * .058 + lk[0] * .012; VOLT.eyes[k].position.y = .035 + lk[1] * .01;
    VOLT.eyes[k].scale.set(e === "wide" ? 1.18 : 1, blink || e === "closed" ? .12 : (e === "wide" ? 1.2 : 1), 1);
  }
  const open = ta > .06 || s.mouth === "o";
  VOLT.smile.visible = !open; VOLT.mouth.visible = open;
  if (open) VOLT.mouth.scale.set(.9 + .3 * ta, s.mouth === "o" ? 1.4 : .5 + 1.3 * ta, 1);
  VOLT.bolt.rotation.z = Math.sin(t * 3.1) * .08 + ta * .15 * Math.sin(t * 11);
  const hs = s.hands || [[-.27, -.06, .05], [.27, -.06, .05]];
  VOLT.root.updateMatrixWorld(true);
  for (let k = 0; k < 2; k++) { const h = hs[k]; V.set(h[0], h[1] + (still ? 0 : Math.sin(t * 2.6 + k * 1.3) * .015) + (s.talk ? ta * .04 * (k ? 1 : .6) * Math.sin(t * 8 + k) : 0), h[2]); VOLT.root.localToWorld(V); VOLT.hands[k].position.copy(V); VOLT.hands[k].scale.setScalar(sc); }
  if (s.floorY !== undefined) { VOLT.shadow.position.set(s.x, s.floorY + .005, s.z); const hgt = Math.max(.05, s.y - s.floorY); VOLT.shadow.scale.setScalar(sc * (1.1 - Math.min(.6, hgt * .25))); VOLT.shadow.material.opacity = .25 - Math.min(.15, hgt * .05); }
}
// lip sync: loudness envelopes per speaker, 30 values per second (build/audio.py -> CT.julesEnv, CT.voltEnv)
const envAt = (arr, t) => { if (!arr) return 0; const i = t * 30, a = Math.floor(i), f = i - a; return lerp(arr[Math.min(arr.length - 1, Math.max(0, a))] || 0, arr[Math.min(arr.length - 1, Math.max(0, a + 1))] || 0, f); };
// ================================================================= JULES, the creator (house blocky style): a fitness creator, hair in a bun,
// lime tee, ink leggings, white trainers; her pixel mouth follows the loudness of her voice
const JULES = makeChar({ id: "jules", skin: "#E7B48E", hair: "#3B2216", style: "bun", top: "#CCFB79", topStyle: "tee", pants: "#1A1A1C", shoe: "#FFFFFF", brow: "#3B2216" }, scene);
JULES.seed = 2.3;
function placeJules(vis, p, f) {
  f = { ...(f || {}) };
  if (f.talk) { const a = envAt(C.julesEnv, NOW); f.talk = false; f.mouth = a < .08 ? (f.mouth || "smile") : (a < .4 ? "talk" : (f.big ? (a > .7 ? "wail" : "rant") : "o")); }
  placeChar(JULES, vis, p, f);
}
// her phone (in the right hand)
JULES.phone = new THREE.Group(); JULES.hand[1].add(JULES.phone); JULES.phone.position.set(0, -.02, .1);
rbox(.075, .15, .01, mat(0x2A2A30, { roughness: .3 }), 0, 0, 0, .008, { parent: JULES.phone, cast: false });
JULES.scrM = texMat("phone"); { const sp = new THREE.Mesh(new THREE.PlaneGeometry(.066, .138), JULES.scrM); sp.position.z = -.006; sp.rotation.y = Math.PI; JULES.phone.add(sp); }
// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const Ls = (k) => C.lines[k][0], Le = (k) => C.lines[k][1];
const talking = (t, k) => t > Ls(k) - .03 && t < Le(k) + .05;
const wordT = (k, i) => { const ws = C.words.filter((w) => w.take === k); return ws[Math.min(i, ws.length - 1)].s; };
const wordAt = (k, txt) => { const w = C.words.find((x) => x.take === k && x.w.toLowerCase().replace(/[^a-z0-9]/g, "").startsWith(txt)); return w ? w.s : Ls(k); };
const SHOTS = [
  ["hook", 0], ["volt", Ls("02") - .12], ["react", Ls("03") - .1], ["step1", Ls("04") - .12], ["answer", Ls("05") - .1],
  ["step2", Ls("06") - .12], ["temple", Ls("07") - .1], ["menu", Ls("08") - .1], ["step3", Ls("09") - .12], ["day9", Ls("10") - .1],
  ["batch", Ls("11") - .12], ["couch", Ls("12") - .12], ["end", Ls("14") - .12],
];
const shotAt = (t) => { let k = 0; for (let i = 0; i < SHOTS.length; i++) if (t >= SHOTS[i][1]) k = i; return [SHOTS[k][0], t - SHOTS[k][1], (SHOTS[k + 1] ? SHOTS[k + 1][1] : DUR) - SHOTS[k][1]]; };
const ease = (x) => x < .5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2;
const back = (x) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2; };
const seated = (o = {}) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .08, ...o });
const standing = (o = {}) => pose({ a: [[.1, .1, .15], [.1, .1, .15]], ...o });
const STAND = v(-.75, 0, -1.0);                      // Jules's spot in front of the board, left
const CARDP = v(.3, 1.6, -1.75);                    // where the prompt card floats
const POST = [];

// ---------------------------------------------------------------- one frame
const CAM = { p: v(0, 1.5, 3), l: v(0, 1, 0), fov: 40, focus: 3, ap: .03 };
function shoot(t) {
  const [sh, u, len] = shotAt(t);
  RM.visible = true; POST.length = 0;
  for (const k of ["prompt", "day9", "roof", "menu", "clap", "speed", "ring"]) FX[k].visible = false;
  for (const a of [FX.inputs, FX.cols, FX.ticks, FX.steam]) for (const o of a) o.visible = false;
  for (const k of ["ribbon", "rays", "blast", "glint", "halo"]) if (FX[k]) FX[k].visible = false;
  for (const a of [FX.sparks || [], FX.shards || [], FX.dust || []]) for (const o of a) o.visible = false;
  JULES.phone.visible = false;
  scene.background = tmpC.set(0xFDF4F4).clone(); scene.fog.color.set(0xFDF4F4); scene.fog.near = 30; scene.fog.far = 90;
  hemi.color.set(0xFFF8F2); hemi.groundColor.set(0xE8D8CC); hemi.intensity = .9;
  sun.color.set(0xFFF4E4); sun.intensity = 1.1; sun.target.position.set(0, 0, -.6); sun.position.set(-3, 5, 3);
  RM.sunL.intensity = 1.6; RM.key.intensity = 1.5; RM.fill.intensity = 1.0; RM.rim.intensity = 0; RM.pinkL.intensity = 0;
  RM.lapScr.color.set(0xF6FFE6);
  for (const sl of RM.slots) sl.material.color.set(0xF2ECEC);
  // the board: which blocks are filled by now (step three fills them in a wave; the hook shows it empty)
  const S3 = Ls("09"), fillT = (i) => S3 + .35 + i * .075;
  for (let i = 0; i < 30; i++) {
    const b = RM.blocks[i], ft = fillT(i), k = clamp((t - ft) / .22);
    b.visible = k > 0; if (b.visible) { const s = back(k); b.scale.set(s, s, 1); b.position.z = CAL.z + .03 + .05 * (1 - k); }
  }
  // the step notes light up as each step starts
  const stepT = [Ls("04"), Ls("06"), Ls("09")];
  RM.notes.forEach((n, k) => { const on = t >= stepT[k] - .05; n.paper.color.set(on ? 0xCCFB79 : 0xFFFFFF); n.scale.setScalar(1 + .25 * pulse(t, stepT[k] + .1, .12)); });
  let bloomS = .1, vig = .18, dark = 0, flash = 0;
  let volt = null, jules = null, julesF = {}, julesRot = null;
  const cam = CAM; cam.ap = .025;
  const seatedTalk = (k) => ({ talk: talking(t, k) });

  if (sh === "hook") {           // 1. two weeks without posting: slumped at the desk, phone in hand, the board empty behind her
    const slump = ss(u, .2, 1.2);
    jules = seated({ lean: .08 + .1 * slump, hp: .22 + .1 * slump, hy: -.12, a: [[.45, .2, .6], [.9, -.18, 1.45]] });
    julesF = { eyes: u > 2.4 ? "teary" : "open", mouth: "sad", brows: "despair", talk: talking(t, "01"), look: [-.3, -.4] };
    JULES.phone.visible = true;
    RM.sunL.intensity = .9; RM.key.intensity = 1.0; hemi.intensity = .7;
    cam.p.set(-.95, 1.5, 1.15 - .2 * ss(u, 0, len)); cam.l.set(-1.3, 1.5, -1.15); cam.fov = 54; cam.focus = 2.2;
    dark = .06;
  } else if (sh === "volt") {    // 2. Volt zips out of the laptop in a burst of sparkle: "What if one prompt planned your next thirty days?"
    const pop = clamp(u / .45), thirty = wordAt("02", "thirty");
    const lp = v(DESK.x + .05, DESKY + .25, DESK.z - .1);
    volt = { x: lerp(lp.x, -.55, ease(pop)), y: lerp(lp.y, 1.45, ease(pop)), z: lerp(lp.z, -.6, ease(pop)), sc: .2 + .8 * back(pop), ry: -.35, eyes: u < .5 ? "wide" : "happy", talk: talking(t, "02"), floorY: 0,
      hands: [[-.27, .05 + .1 * pulse(u, .6, .2), .08], [.3, .12 + .08 * Math.sin(u * 5), .08]] };
    if (u < .7) for (let i = 0; i < 18; i++) { const sp = FX.sparks[i], a = u - i * .015; sp.visible = a > 0 && a < .6; if (!sp.visible) continue; const an = i * 2.4; sp.position.set(lp.x + Math.cos(an) * a * 1.2, lp.y + .1 + Math.sin(an * 1.3) * a * .8 + a * .4, lp.z + Math.sin(an) * a * .5); const s2 = .08 * (1 - a / .6); sp.scale.set(s2, s2, 1); sp.material.opacity = 1 - a / .6; }
    // the board shimmers on "thirty": a lime wave runs across the empty slots
    RM.slots.forEach((sl, i) => { const w = pulse(t, thirty + .05 + (i % 6) * .03 + Math.floor(i / 6) * .02, .1); sl.material.color.setRGB(lerp(.95, .8, w), lerp(.93, .98, w), lerp(.93, .47, w)); });
    jules = seated({ lean: -.05, hp: -.12, hy: .45, a: [[.4, .2, .5], [.5, .2, .6]] });
    julesF = { eyes: "wide", mouth: "o", brows: "high", noblink: true };
    RM.lapScr.color.set(0xCCFB79);
    cam.p.set(-.35, 1.4, 1.75); cam.l.set(-.85, 1.25, -.75); cam.fov = 50; cam.focus = 2.6;
    flash = .25 * pulse(u, .12, .08);
  } else if (sh === "react") {   // 3. "Thirty?! I can't even plan lunch."
    jules = seated({ lean: -.08, hp: -.05, hy: .2, a: [[2.4, .5, .4], [2.4, .5, .4]] });
    julesF = { eyes: "wide", mouth: talking(t, "03") ? "rant" : "gasp", brows: "high", talk: talking(t, "03"), big: true, noblink: true };
    volt = { x: -.55, y: 1.45, z: -.6, ry: -.6, eyes: "happy", floorY: 0 };
    cam.p.set(-.95, 1.4, .35); cam.l.set(-1.2, 1.3, -1.15); cam.fov = 46; cam.focus = 1.5;
  } else if (sh === "step1") {   // 4. STEP 1: the prompt card floats up; Volt points at its three blanks
    const ap = ss(u, 0, .45);
    FX.prompt.visible = true; FX.prompt.position.set(CARDP.x, CARDP.y - .4 * (1 - ap), CARDP.z); FX.prompt.rotation.set(0, -.12, 0); FX.prompt.scale.setScalar(.6 + .4 * back(ap));
    FX.prompt.children[1].material.map = TEX.prompt; FX.prompt.children[1].material.needsUpdate = true;
    volt = { x: -.35, y: 1.5, z: -1.55, ry: .35, eyes: "open", look: [.6, .1], talk: talking(t, "04"), floorY: 0, hands: [[-.25, -.05, .06], [.32, .1 + .05 * Math.sin(u * 6), .1]] };
    jules = standing({ x: STAND.x - .25, z: STAND.z + .25, ry: .5, lean: .05, a: [[.3, .15, .5], [.3, .15, .5]] });
    julesF = { eyes: "open", mouth: "smile", brows: "up", look: [.6, .2] };
    cam.p.set(.0, 1.5, 1.45); cam.l.set(.0, 1.45, -1.6); cam.fov = 54; cam.focus = 3.1;
  } else if (sh === "answer") {  // 5. "Home workouts. Busy moms. More clients." Each answer flies into its blank
    FX.prompt.visible = true; FX.prompt.position.copy(CARDP); FX.prompt.rotation.set(0, -.12, 0); FX.prompt.scale.setScalar(1);
    const ws = [wordAt("05", "home"), wordAt("05", "busy"), wordAt("05", "more")];
    const allIn = t > ws[2] + .5;
    FX.prompt.children[1].material.map = allIn ? TEX.promptFilled : TEX.prompt; FX.prompt.children[1].material.needsUpdate = true;
    FX.prompt.scale.setScalar(1 + .06 * pulse(t, ws[2] + .5, .08));
    for (let k = 0; k < 3; k++) {
      const c = FX.inputs[k], a = clamp((t - ws[k] + .05) / .55); c.visible = a > 0 && a < 1;
      const from = v(STAND.x + .2, 1.45, STAND.z + .3), to = v(CARDP.x - .2 + k * .15, CARDP.y + .05 - k * .12, CARDP.z + .05), e2 = ease(a);
      c.position.set(lerp(from.x, to.x, e2), lerp(from.y, to.y, e2) + Math.sin(e2 * Math.PI) * .35, lerp(from.z, to.z, e2)); c.rotation.set(0, -.12, (1 - e2) * .4); c.scale.setScalar(1 - .35 * e2);
    }
    const cnt = ws.filter((w) => t > w).length;
    jules = standing({ x: STAND.x, z: STAND.z, ry: .55, lean: .02, a: [[.4, .2, .7], [cnt ? 1.5 : .4, .25, cnt ? .4 : .7]] });
    julesF = { eyes: "open", mouth: "smile", brows: "flat", talk: talking(t, "05"), look: [.5, .2] };
    volt = { x: CARDP.x - .1, y: 2.12, z: CARDP.z + .15, ry: -.2, eyes: allIn ? "happy" : "open", look: [-.6, 0], floorY: 0 };
    if (allIn && t < ws[2] + .9) for (let i = 0; i < 12; i++) { const sp = FX.sparks[i], a = t - ws[2] - .5 - i * .01; sp.visible = a > 0 && a < .4; if (!sp.visible) continue; const an = i * .52; sp.position.set(CARDP.x + Math.cos(an) * (.55 + a), CARDP.y + Math.sin(an) * (.35 + a * .7), CARDP.z + .05); const s2 = .07 * (1 - a / .4); sp.scale.set(s2, s2, 1); sp.material.opacity = 1 - a / .4; }
    cam.p.set(-.25, 1.45, 1.75); cam.l.set(-.2, 1.45, -1.4); cam.fov = 58; cam.focus = 3.0;
  } else if (sh === "step2" || sh === "temple" || sh === "menu") {   // 6-8. STEP 2: three pillars rise; "a temple?" the roof slams on; "a menu" it flips
    const ws = [wordAt("06", "teach"), wordAt("06", "story"), wordAt("06", "proof")];
    const rTemple = Ls("07") + .55, rMenu = Ls("08") + .1;
    const sink = ss(t, rMenu + .1, rMenu + .5);
    for (let k = 0; k < 3; k++) { const c = FX.cols[k], r = clamp((t - ws[k] + .1) / .4); c.visible = r > 0 && sink < 1; c.position.set(.05 + k * .5, -1.05 * (1 - back(r)) - 1.1 * sink, -1.55); c.scale.set(1, 1, 1); c.rotation.y = -.1; }
    const slam = clamp((t - rTemple) / .22);
    if (t > rTemple && t < rMenu + .45) {
      FX.roof.visible = true; const flip = ss(t, rMenu, rMenu + .4);
      FX.roof.position.set(.55, lerp(2.5, 1.06, slam * slam) + .5 * flip, -1.55); FX.roof.rotation.set(flip * Math.PI * .5, -.1, 0); FX.roof.scale.setScalar(1 - .6 * flip);
      if (slam >= 1) { const r2 = clamp((t - rTemple - .22) / .5); FX.dust.forEach((d, i) => { const an = i / FX.dust.length * 6.283; d.visible = r2 < 1; d.position.set(.55 + Math.cos(an) * (.4 + .9 * r2), 1.08 + .15 * r2, -1.55 + Math.sin(an) * .3 * r2); d.scale.setScalar(.1 + .25 * r2); d.material.opacity = .5 * (1 - r2); }); }
    }
    if (t > rMenu + .15) { const m = ss(t, rMenu + .15, rMenu + .55); FX.menu.visible = true; FX.menu.position.set(.55, 1.65 - .3 * (1 - m), -1.6); FX.menu.rotation.set((1 - m) * -1.2, -.08, 0); FX.menu.scale.setScalar(.5 + .5 * back(m)); }
    if (sh === "step2") {
      volt = { x: -.3, y: 1.75, z: -1.35, ry: .45, eyes: "open", look: [.5, -.2], talk: talking(t, "06"), floorY: 0, hands: [[-.27, -.04, .06], [.3, .14, .1]] };
      jules = standing({ x: STAND.x - .3, z: STAND.z + .3, ry: .45, a: [[.2, .12, .3], [.2, .12, .3]] });
      julesF = { eyes: "open", mouth: "smile", look: [.5, .1] };
      cam.p.set(.4, 1.35, 1.75); cam.l.set(.4, 1.1, -1.5); cam.fov = 56; cam.focus = 3.2;
    } else if (sh === "temple") {
      jules = standing({ x: -.3, z: -.9, ry: .45, hr: .2, a: [[.35, .5, 1.6], [.2, .12, .3]] });
      julesF = { eyes: t > rTemple + .2 ? "wide" : "side", mouth: talking(t, "07") ? "talk" : "smirk", brows: "raise1", talk: talking(t, "07"), look: [.4, .3] };
      volt = { x: .55, y: 1.95, z: -1.45, ry: -.1, eyes: t > rTemple + .2 ? "closed" : "open", floorY: 0 };
      const shk = slam > 0 && slam < 1.6 ? .02 * Math.exp(-(t - rTemple) * 8) : 0;
      cam.p.set(.05 + shk * Math.sin(t * 90), 1.45 + shk * Math.cos(t * 80), 2.35); cam.l.set(.12, 1.3, -1.3); cam.fov = 58; cam.focus = 2.9;
    } else {
      volt = { x: 1.25, y: 1.25, z: -1.1, ry: -.55, eyes: t > Ls("08") + .9 ? "happy" : "open", look: [-.5, 0], talk: talking(t, "08"), floorY: 0, hands: [[-.3, .12 + .06 * Math.sin(u * 5), .1], [.27, -.04, .06]] };
      jules = standing({ x: STAND.x - .3, z: STAND.z + .3, ry: .4, a: [[.2, .12, .3], [.2, .12, .3]] });
      julesF = { eyes: t > Ls("08") + .9 ? "happy" : "open", mouth: "grin", look: [.5, .1] };
      cam.p.set(.55, 1.5, 1.85); cam.l.set(.55, 1.45, -1.6); cam.fov = 56; cam.focus = 3.4;
    }
  } else if (sh === "step3") {   // 9. STEP 3: thirty days, each with a hook and a format: the board fills in a wave; the camera sweeps along it
    const k = ss(u, 0, len);
    volt = { x: 2.15, y: 1.7, z: -1.6, ry: -.7, eyes: "happy", talk: talking(t, "09"), floorY: 0, hands: [[-.3, .2 + .08 * Math.sin(u * 7), .1], [.3, .2 + .08 * Math.sin(u * 7 + 1), .1]] };
    jules = standing({ x: STAND.x, z: STAND.z + .1, ry: .7, a: [[.3, .2, .4], [.3, .2, .4]], hp: -.15 });
    julesF = { eyes: "wide", mouth: "o", brows: "high", look: [.6, .4], noblink: true };
    RM.rim.intensity = 1.2; RM.rim.position.set(CAL.cx, CAL.cy, CAL.z + .8);
    cam.p.set(lerp(-.2, 1.05, k), 1.6, lerp(1.9, 1.6, k)); cam.l.set(lerp(.15, .9, k), 1.6, CAL.z); cam.fov = 60; cam.focus = 3.6;
  } else if (sh === "day9") {    // 10. Day nine flies out of its slot; the kettle steams; "I'd watch that!"
    const o = ss(u, .05, .6), p9 = slotPos(8);
    FX.day9.visible = true; FX.day9.position.set(lerp(p9.x, -.35, o), lerp(p9.y, 2.11, o), lerp(p9.z + .1, -.7, o)); FX.day9.rotation.set(0, lerp(0, .12, o), (1 - o) * .3); FX.day9.scale.setScalar(lerp(.35, .61, back(o)));
    RM.blocks[8].visible = u < .1;
    const watch = wordAt("10", "id");
    jules = standing({ x: -1.05, z: -.35, ry: .55, hp: -.1, a: t > watch - .1 ? [[2.6, .6, .4], [2.6, .6, .4]] : [[.6, .3, 1.2], [.6, .3, 1.2]], y: t > watch ? Math.max(0, Math.sin(clamp((t - watch) / .35) * Math.PI)) * .12 : 0 });
    julesF = { eyes: t > watch ? "happy" : "wide", mouth: talking(t, "10") ? "laugh" : "grin", brows: "high", talk: talking(t, "10"), big: true };
    volt = { x: -.2, y: 1.42, z: -.6, ry: -.35, eyes: "happy", floorY: 0 };
    RM.kettle.rotation.z = .03 * Math.sin(t * 40) * ss(u, .8, 1.2);
    FX.steam.forEach((s, i) => { const a = ((u * .9 + i / 6) % 1); s.visible = u > .6; s.position.set(2.75 + .14 + a * .1, .82 + a * .45, .1 + Math.sin(a * 6 + i) * .04); s.scale.setScalar(.6 + a * 1.4); s.material.opacity = .65 * (1 - a); });
    cam.p.set(-.65, 1.6, 2.2); cam.l.set(-.65, 1.6, -.6); cam.fov = 58; cam.focus = 2.6;
  } else if (sh === "batch") {   // 11. one rule: film the whole week in one afternoon. The clapperboard snaps; the first week glows
    const aft = wordAt("11", "afternoon");
    FX.clap.visible = true; FX.clap.position.set(-.35, 1.95, -1.0); FX.clap.rotation.set(0, .1, 0); FX.clapTop.rotation.z = t < aft - .15 ? .55 : lerp(.55, 0, clamp((t - aft + .15) / .1));
    FX.clap.scale.setScalar(1 + .08 * pulse(t, aft, .06));
    for (let i = 0; i < 7; i++) { const b = RM.blocks[i]; b.scale.setScalar(1 + .12 * pulse(t, aft + .15 + i * .05, .1)); }
    RM.rim.intensity = 1.5 * pulse(t, aft + .3, .5); RM.rim.position.set(CAL.cx - .9, CAL.y0, CAL.z + .6);
    volt = { x: -.1, y: 1.35, z: -.8, ry: -.15, eyes: "open", talk: talking(t, "11"), floorY: 0, hands: [[-.22, .0, .2], [.22, .12, .22]], still: true };
    jules = standing({ x: -.95, z: -.55, ry: .4, a: [[.25, .15, .3], [.25, .15, .3]] });
    julesF = { eyes: "open", mouth: "smile", brows: "up", look: [.4, 0] };
    cam.p.set(-.6, 1.55, 1.9); cam.l.set(-.6, 1.55, -1.0); cam.fov = 56; cam.focus = 2.5;
  } else if (sh === "couch") {   // 12-13. "So I'm busy for one afternoon..." "...and posting all week." Feet up on the couch; the week ticks
    const cc = RM.couch.position, ry = RM.couch.rotation.y;
    jules = pose({ x: cc.x - .05, y: .57 - .71, z: cc.z + .12, ry, lean: -.22, hp: -.05, hy: .15, l: [[1.45, 1.4], [1.35, 1.25]], a: [[.3, 1.1, 2.3], [.3, 1.1, 2.3]] });
    julesF = { eyes: talking(t, "12") ? "open" : "happy", mouth: talking(t, "12") ? "talk" : "grin", talk: talking(t, "12"), look: [-.3, 0] };
    volt = { x: cc.x - 1.0, y: 1.3, z: cc.z + .5, ry: .6, eyes: t > Ls("13") ? "wink" : "open", talk: talking(t, "13"), floorY: 0, hands: [[-.27, -.05, .06], [.3, .18, .1]] };
    for (let i = 0; i < 7; i++) { const tk = FX.ticks[i], ta = Ls("13") + .1 + i * .12, p = slotPos(i); tk.visible = t > ta; if (tk.visible) { const s2 = back(clamp((t - ta) / .2)); tk.position.set(p.x + .17, p.y + .12, p.z + .11); tk.scale.setScalar(s2); } }
    cam.p.set(1.0, 1.35, 1.7); cam.l.set(1.45, 1.02, -.9); cam.fov = 58; cam.focus = 2.6;
  } else if (sh === "end") {     // 14-15. the end card plate: both in front of the full board, waving
    jules = standing({ x: -.2, z: -1.1, ry: .2, a: [[.2, .12, .3], [2.7 + .2 * Math.sin(u * 7), .3, .3]] });
    julesF = { eyes: talking(t, "14") ? "open" : "happy", mouth: talking(t, "14") ? "talk" : "grin", talk: talking(t, "14") };
    volt = { x: .6, y: 1.3, z: -1.0, ry: -.2, eyes: talking(t, "15") ? "open" : "happy", talk: talking(t, "15"), floorY: 0, hands: [[-.27, -.04, .06], [.3, .2 + .06 * Math.sin(u * 8), .1]] };
    cam.p.set(.2, 1.65, 2.3); cam.l.set(.2, 1.95, -1.4); cam.fov = 48; cam.focus = 3.4;
  }

  if (jules) { placeJules(true, idle(jules, t, JULES.seed), julesF); if (julesRot) JULES.root.rotation.set(...julesRot); else JULES.root.rotation.x = JULES.root.rotation.z = 0; }
  else placeJules(false);
  JULES.root.updateMatrixWorld(true);
  placeVolt(!!volt, volt || {});
  for (const f of POST) f();
  return { cam, bloomS, vig, dark, flash };
}

function renderAt(t) {
  if (!TEX.ready) return;
  NOW = t;
  const cv = window.CR_COVER;
  const r = shoot(cv ? cv.t : t);
  const cam = r.cam;
  camera.position.copy(cam.p); camera.fov = cam.fov;
  const look = cam.l.clone();
  if (cv && cv.cam) { camera.position.set(...cv.cam); look.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix(); camera.up.set(0, 1, 0); camera.lookAt(look);
  scene.updateMatrixWorld(true);
  cocPass.uniforms.uF.value = cam.focus; cocPass.uniforms.uAp.value = cam.ap;
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = .03; gu.uCool.value = 0; gu.uSat.value = 1.06; gu.uCon.value = .03; gu.uVig.value = r.vig; gu.uTint.value = 0;
  gu.uFlash.value = r.flash || 0; gu.uCA.value = 0; gu.uKeep.value = 0; gu.uGrain.value = 0; gu.uTop.value = 0; gu.uDark.value = r.dark;
  bloom.strength = r.bloomS;
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 30 }); sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}
// ---------------------------------------------------------------- textures: the calendar numbers, pillar icons, sticky notes, the
// prompt card and the three answers, the Day 9 card, the menu board, the clapperboard, the phone screen, the logo poster.
// Inter (OFL), drawn after the fonts load. Colours from brands/creators-100x/brand.md.
const text = (w, h, draw) => pix(w, h, draw, false);
const INK_S = "#101111", PINK_S = "#FD0B68", LIME_S = "#CCFB79", OFF_S = "#FDF4F4";
const F = (wt, px2) => `${wt} ${px2}px Inter, sans-serif`;
function wrap(g, s, x, y, maxW, lh) { const words = s.split(" "); let line = "", yy = y; for (const w of words) { const t = line ? line + " " + w : w; if (g.measureText(t).width > maxW && line) { g.fillText(line, x, yy); line = w; yy += lh; } else line = t; } g.fillText(line, x, yy); return yy; }
function pillT(g, x, y, s, bg, fg, sz = 22) { g.font = F(800, sz); const w = g.measureText(s).width + sz * 1.2; g.fillStyle = bg; rr(g, x, y, w, sz * 1.7, sz * .85); g.fill(); g.fillStyle = fg; g.fillText(s, x + sz * .6, y + sz * 1.22); return w; }
function icon(g, k, cx, cy, s) {     // 0 teach: a lightbulb, 1 story: a speech bubble, 2 proof: a star
  g.save(); g.translate(cx, cy); g.scale(s, s); g.lineWidth = 7; g.lineJoin = "round"; g.lineCap = "round";
  const col = k === 2 ? LIME_S : INK_S; g.strokeStyle = col; g.fillStyle = col;
  if (k === 0) { g.beginPath(); g.arc(0, -8, 22, Math.PI * .8, Math.PI * 2.2); g.lineTo(9, 22); g.lineTo(-9, 22); g.closePath(); g.stroke(); g.fillRect(-10, 26, 20, 6); g.fillRect(-7, 35, 14, 5); }
  if (k === 1) { rr(g, -28, -24, 56, 40, 12); g.stroke(); g.beginPath(); g.moveTo(-10, 16); g.lineTo(-18, 30); g.lineTo(2, 16); g.stroke(); for (const x of [-12, 0, 12]) { g.beginPath(); g.arc(x, -4, 4, 0, 7); g.fill(); } }
  if (k === 2) { g.beginPath(); for (let i = 0; i < 10; i++) { const r = i % 2 ? 13 : 30, a = -Math.PI / 2 + i * Math.PI / 5; g.lineTo(Math.cos(a) * r, Math.sin(a) * r); } g.closePath(); g.fill(); }
  g.restore();
}
const PROMPT_BLANKS = ["your niche", "who it's for", "your goal"];
const ANSWERS = [["NICHE", "Home workouts"], ["FOR", "Busy moms"], ["GOAL", "More clients"]];
async function buildTextures() {
  try { await Promise.all([800, 700, 600].map((w) => document.fonts.load(`${w} 40px Inter`))); } catch (e) {}
  const logoImg = await new Promise((res) => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = "assets/img/logo.png"; });
  // the board's day numbers (1-30 in each slot's top-left corner)
  TEX.calnums = text(1650, 1150, (g, w, h) => { g.clearRect(0, 0, w, h); const sx = w / 3.3, sy = h / 2.3; g.font = F(700, 26); g.fillStyle = "#A9A2A2";
    for (let i = 0; i < 30; i++) { const p = slotPos(i); const x = (p.x - (CAL.cx - 1.65)) * sx, y = (CAL.cy + 1.15 - p.y) * sy; g.fillText(String(i + 1), x - CAL.sw / 2 * sx + 14, y - CAL.sh / 2 * sy + 34); } });
  for (let k = 0; k < 3; k++) TEX["icon" + k] = text(128, 128, (g, w, h) => { g.clearRect(0, 0, w, h); icon(g, k, 64, 60, 1.25); });
  for (let k = 0; k < 3; k++) TEX["note" + k] = text(256, 256, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = INK_S; g.font = F(800, 30); g.fillText("STEP", 28, 62); g.font = F(800, 150); g.fillText(String(k + 1), 28, 210); });
  TEX.logo = text(512, 512, (g, w, h) => { g.fillStyle = OFF_S; rr(g, 0, 0, w, h, 40); g.fill(); if (logoImg) { const s = Math.min((w - 60) / logoImg.width, (h - 60) / logoImg.height); g.drawImage(logoImg, (w - logoImg.width * s) / 2, (h - logoImg.height * s) / 2, logoImg.width * s, logoImg.height * s); } });
  // the prompt card: the one prompt with three blanks (they fill in lime as she answers)
  const promptCard = (filled) => text(1000, 620, (g, w, h) => {
    g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); pillT(g, 40, 34, "THE PROMPT", INK_S, LIME_S, 26);
    g.font = F(800, 50); g.fillStyle = INK_S; let y = 170;
    const parts = [["I make ", 0], [" content for ", 1], [". My goal is ", 2], [". Plan my next 30 days.", -1]];
    let x = 44; const lh = 74;
    const put = (s, bg) => { for (const word of s.split(/(\s+)/)) { if (!word) continue; const ww = g.measureText(word).width; if (x + ww > w - 40 && word.trim()) { x = 44; y += lh; } if (bg && word.trim()) { g.fillStyle = bg; rr(g, x - 6, y - 46, ww + 12, 62, 12); g.fill(); g.fillStyle = INK_S; } if (word.trim()) g.fillText(word, x, y); x += ww; } };
    put("I make", null); put(" ", null);
    put(filled ? ANSWERS[0][1].toLowerCase() : "[" + PROMPT_BLANKS[0] + "]", LIME_S); put(" content for ", null);
    put(filled ? ANSWERS[1][1].toLowerCase() : "[" + PROMPT_BLANKS[1] + "]", LIME_S); put(". My goal is ", null);
    put(filled ? ANSWERS[2][1].toLowerCase() : "[" + PROMPT_BLANKS[2] + "]", LIME_S); put(". Plan my next 30 days.", null);
  });
  TEX.prompt = promptCard(false); TEX.promptFilled = promptCard(true);
  for (let k = 0; k < 3; k++) TEX["in" + k] = text(620, 200, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); pillT(g, 28, 30, ANSWERS[k][0], INK_S, LIME_S, 26); g.font = F(800, 58); g.fillStyle = INK_S; g.fillText(ANSWERS[k][1], 30, 158); });
  for (let k = 0; k < 3; k++) TEX["pill" + k] = text(460, 140, (g, w, h) => { g.clearRect(0, 0, w, h); const lab = ["TEACH", "STORY", "PROOF"][k]; g.fillStyle = [INK_S, "#FFFFFF", LIME_S][k]; rr(g, 0, 0, w, h, 70); g.fill(); g.font = F(800, 70); g.fillStyle = [LIME_S, PINK_S, INK_S][k]; const tw = g.measureText(lab).width; g.fillText(lab, (w - tw) / 2, 96); });
  TEX.menu = text(1700, 900, (g, w, h) => { g.fillStyle = INK_S; g.fillRect(0, 0, w, h); g.font = F(800, 96); g.fillStyle = LIME_S; g.fillText("THE MENU", 70, 140);
    const items = [["TEACH", "how-to tips", LIME_S], ["STORY", "your journey", PINK_S], ["PROOF", "results, wins", "#FFFFFF"]];
    items.forEach(([a, b, c], i) => { const y = 300 + i * 200; g.fillStyle = c; g.beginPath(); g.arc(110, y - 30, 26, 0, 7); g.fill(); g.font = F(800, 92); g.fillStyle = "#FFFFFF"; g.fillText(a, 170, y); g.font = F(600, 64); g.fillStyle = "#B9B9B9"; g.fillText(b, 720, y); });
    g.font = F(700, 46); g.fillStyle = "#8A8A8A"; g.fillText("never run out of dishes", 70, 860); });
  TEX.day9 = text(1150, 820, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = LIME_S; g.fillRect(0, 0, w, 16);
    pillT(g, 50, 60, "DAY 9", INK_S, LIME_S, 34); pillT(g, 270, 60, "TEACH", LIME_S, INK_S, 34);
    g.font = F(800, 78); g.fillStyle = INK_S; const y = wrap(g, "The 4-minute workout you can do while the kettle boils", 50, 250, w - 100, 92);
    g.font = F(700, 44); g.fillStyle = "#6A6A6A"; g.fillText("Format: tutorial", 50, y + 110); g.fillStyle = PINK_S; g.fillText("Hook: under 12 words", 50, y + 175); });
  TEX.clap = text(460, 260, (g, w, h) => { g.fillStyle = INK_S; g.fillRect(0, 0, w, h); g.font = F(800, 44); g.fillStyle = "#FFFFFF"; g.fillText("BATCH DAY", 24, 70); g.font = F(700, 34); g.fillStyle = LIME_S; g.fillText("7 POSTS · 1 AFTERNOON", 24, 140); g.fillStyle = "#777"; g.font = F(600, 28); g.fillText("SCENE 1-7   TAKE 1", 24, 210); });
  TEX.claptop = text(480, 50, (g, w, h) => { for (let i = 0; i < 12; i++) { g.fillStyle = i % 2 ? "#FFFFFF" : INK_S; g.beginPath(); g.moveTo(i * 44, h); g.lineTo(i * 44 + 22, 0); g.lineTo(i * 44 + 44, 0); g.lineTo(i * 44 + 22, h); g.fill(); } });
  TEX.tick = text(128, 128, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = LIME_S; g.beginPath(); g.arc(64, 64, 58, 0, 7); g.fill(); g.strokeStyle = INK_S; g.lineWidth = 14; g.lineCap = "round"; g.lineJoin = "round"; g.beginPath(); g.moveTo(36, 66); g.lineTo(56, 86); g.lineTo(94, 44); g.stroke(); });
  TEX.phone = text(132, 276, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#EEE"; g.fillRect(0, 0, w, 40); g.font = F(700, 13); g.fillStyle = "#888"; g.fillText("Last post", 14, 90); g.font = F(800, 30); g.fillStyle = PINK_S; g.fillText("14 days", 14, 128); g.font = F(700, 13); g.fillStyle = "#888"; g.fillText("ago", 14, 150); for (let i = 0; i < 3; i++) { g.fillStyle = "#E4E4E4"; g.fillRect(10 + i * 40, 180, 34, 44); } });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  TEX.ready = true;
}

const ready = (async () => {
  await buildTextures();
  scene.traverse((o) => { if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  RM.visible = true;
  renderer.compile(scene, camera);
  renderAt(window.CR_COVER ? window.CR_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["plan"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.CR_COVER ? window.CR_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C };
