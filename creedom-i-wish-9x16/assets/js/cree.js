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

// ================================================================= THE BEDROOM STUDIO (soft, rounded, like the reference stills)
// The desk faces the camera side (+z), the creator's chair behind it (z = -.7). Back wall z = -2.3 with the big window
// (left of centre) framed by fairy lights; the bed along the right; posters and a plant shelf on the right wall.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const RM = mkSet("room");
const SEAT = v3(-.1, 0, -.75), SITY = .52 - .71;
const DESKY = .8;
const rbox = (w, h, d, c, x, y, z, r = .03, o = {}) => box(w, h, d, c, x, y, z, { round: r, ...o });
const soft = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .7, sheen: .6, sheenColor: new THREE.Color(0xffffff), sheenRoughness: .6, ...o });
{
  const plank = pix(256, 256, (g) => { px(g, "#7C5236", 0, 0, 256, 256); for (let j = 0; j < 8; j++) { const c = ["#80553A", "#764D33", "#86593C", "#7A5136"][j % 4]; px(g, c, 0, j * 32, 256, 32); px(g, "#5E3C27", 0, j * 32, 256, 2); px(g, "#5E3C27", (j * 97) % 256, j * 32, 2, 32); for (let k = 0; k < 6; k++) { g.fillStyle = "rgba(0,0,0,.05)"; g.fillRect((j * 37 + k * 41) % 256, j * 32 + 6 + k * 4, 60, 1); } } }, false);
  flat(9, 8, new THREE.MeshStandardMaterial({ map: rep(plank, 4, 4), roughness: .45, envMap: ENV, envMapIntensity: .15 }), 0, 0, 0);
  const wallM = mat(0xC9BBDD, { roughness: .95 }), trim = mat(0xEDE6F2, { roughness: .6 });
  // back wall with a window opening (centre x -1.05, y 1.8; 1.84 x 1.44)
  { const x0 = -1.05 - .92, x1 = -1.05 + .92, y0 = 1.8 - .72, y1 = 1.8 + .72;
    box(x0 + 4.5, 3.2, .2, wallM, (-4.5 + x0) / 2, 1.6, -2.4); box(4.5 - x1, 3.2, .2, wallM, (x1 + 4.5) / 2, 1.6, -2.4);
    box(x1 - x0, y0, .2, wallM, -1.05, y0 / 2, -2.4); box(x1 - x0, 3.2 - y1, .2, wallM, -1.05, (y1 + 3.2) / 2, -2.4); }
  box(.2, 3.2, 8, wallM, -3.4, 1.6, 1.5); box(.2, 3.2, 8, wallM, 3.5, 1.6, 1.5);
  box(9, .1, 8, mat(0xD6CCE6, { roughness: .95 }), 0, 3.2, 1.5, { cast: false });
  box(9, .1, .05, trim, 0, .05, -2.29); box(.05, .1, 8, trim, 3.39, .05, 1.5);
  // the window: two panes (they swing open for the entrance), frame, sill; the sky plane sits behind it
  RM.skyM = texMat("sky", { transparent: false }); RM.sky = plane(5.4, 4.0, RM.skyM, -1.0, 1.9, -3.9, 0);
  RM.clouds = []; for (let i = 0; i < 3; i++) { const m = texMat("cloud" + i); const p = plane(1.6, .5, m, -2 + i * 1.4, 2.4 - i * .25, -3.8 + i * .01, 0); p.material.opacity = .8; RM.clouds.push(p); }
  RM.win = new THREE.Group(); RM.win.position.set(-1.05, 1.8, -2.3); RM.add(RM.win);
  const wf = mat(0xF4F0F8, { roughness: .5 });
  for (const [w, h, x, y] of [[1.9, .07, 0, .72], [1.9, .07, 0, -.72], [.07, 1.5, -.92, 0], [.07, 1.5, .92, 0]]) box(w, h, .12, wf, x, y, 0, { parent: RM.win });
  box(2.1, .06, .26, wf, 0, -.78, .08, { parent: RM.win });
  RM.panes = [];
  for (const s of [-1, 1]) {
    const hinge = new THREE.Group(); hinge.position.set(s * .9, 0, .02); RM.win.add(hinge);
    const pane = new THREE.Group(); hinge.add(pane);
    for (const [w, h, x, y] of [[.9, .05, -s * .45, .69], [.9, .05, -s * .45, -.69], [.05, 1.4, 0, 0], [.05, 1.4, -s * .88, 0]]) box(w, h, .05, wf, x, y, 0, { parent: pane });
    const gl = new THREE.Mesh(new THREE.PlaneGeometry(.86, 1.36), new THREE.MeshPhysicalMaterial({ color: 0x8090B0, roughness: .05, transparent: true, opacity: .05, envMap: ENV, envMapIntensity: .08, depthWrite: false })); gl.position.x = -s * .45; pane.add(gl);
    RM.panes.push(hinge);
  }
  // sheer curtains (they blow in on the teasers)
  RM.curt = [];
  for (const s of [-1, 1]) { const g = new THREE.Group(); g.position.set(-1.05 + s * 1.12, 2.55, -2.2); RM.add(g); const cm2 = new THREE.MeshStandardMaterial({ color: 0xF6F0FA, roughness: .9, transparent: true, opacity: .55, side: THREE.DoubleSide }); const c = new THREE.Mesh(new THREE.PlaneGeometry(.45, 1.7, 1, 8), cm2); c.position.y = -.85; g.add(c); RM.curt.push(g); }
  // fairy lights around the window
  RM.fairy = [];
  const bulbM = [new THREE.MeshBasicMaterial({ color: 0xFFE2A8, toneMapped: false }), new THREE.MeshBasicMaterial({ color: 0xFFD08A, toneMapped: false })];
  const path = []; for (let i = 0; i <= 24; i++) { const u = i / 24; path.push(v3(-2.05 + 2.0 * u, 2.62 - .07 * Math.sin(u * Math.PI * 3) ** 2, -2.27)); }
  for (let i = 0; i <= 10; i++) { path.push(v3(-2.08, 2.55 - i * .15, -2.27)); path.push(v3(-.02 + .02, 2.55 - i * .15, -2.27)); }
  const wire = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(path.slice(0, 25)), 80, .004, 4), mat(0x3A3A3A)); RM.add(wire);
  path.forEach((p, i) => { const b = new THREE.Mesh(new THREE.SphereGeometry(.028, 12, 10), bulbM[i % 2]); b.position.copy(p).add(v3(0, -.03, .01)); RM.add(b); RM.fairy.push(b); });
  // posters, the plant shelf (right wall)
  RM.posterM = texMat("posters", { transparent: false }); const pp = plane(1.3, .95, RM.posterM, 3.38, 1.9, -1.2, -Math.PI / 2);
  rbox(.24, .04, .9, mat(0xC9A27A), 3.27, 1.55, -.1, .01);
  for (let k = 0; k < 3; k++) { cyl(.07, .055, .1, soft(0xF4F0EC), 3.27, 1.62, -.4 + k * .3, 16); for (let j = 0; j < 5; j++) { const l = new THREE.Mesh(new THREE.SphereGeometry(.05, 10, 8), mat(0x5E9C52)); l.position.set(3.27 + (hash(k * 7 + j) - .5) * .1, 1.7 + j * .03, -.4 + k * .3 + (hash(j * 3 + k) - .5) * .1); l.scale.set(1, 1.4, 1); add(l); } }
  // the desk: rounded top and legs, a drawer unit on the left
  rbox(1.9, .07, .9, mat(0x8A6044, { roughness: .45, envMap: ENV, envMapIntensity: .2 }), 0, DESKY - .035, 0, .02);
  for (const [x, z] of [[.88, .38], [.88, -.38], [-.2, .38], [-.2, -.38]]) rbox(.06, DESKY - .07, .06, mat(0x7A5238), x, (DESKY - .07) / 2, z, .015);
  rbox(.62, DESKY - .1, .8, mat(0x7A5238), -.6, (DESKY - .1) / 2 + .02, 0, .02);
  // laptop (plain lid), the pink lamp, the mug, the gorilla tripod with the phone
  const lap = new THREE.Group(); lap.position.set(-.25, DESKY, -.05); RM.add(lap);
  rbox(.44, .018, .3, metal(0x5A5A62, .35), 0, .009, 0, .006, { parent: lap });
  const lid = new THREE.Group(); lid.position.set(0, .015, -.15); lid.rotation.x = -.35; lap.add(lid); rbox(.44, .29, .014, metal(0x5A5A62, .35), 0, .145, 0, .006, { parent: lid });
  RM.lapScr = new THREE.MeshBasicMaterial({ color: 0x9FB2D8, toneMapped: false }); const ls = new THREE.Mesh(new THREE.PlaneGeometry(.4, .25), RM.lapScr); ls.position.set(0, .145, .008); lid.add(ls);
  RM.lampShade = new THREE.MeshPhysicalMaterial({ color: 0xF0B8C6, roughness: .45, clearcoat: .3 });
  { const L = new THREE.Group(); L.position.set(-.72, DESKY, -.15); RM.add(L); cyl(.09, .1, .025, soft(0xF0B8C6), 0, .012, 0, 24, { parent: L });
    const a1 = new THREE.Group(); a1.position.y = .03; a1.rotation.z = -.35; L.add(a1); cyl(.011, .011, .3, soft(0xF0B8C6), 0, .15, 0, 10, { parent: a1 });
    const a2 = new THREE.Group(); a2.position.y = .3; a2.rotation.z = 1.25; a1.add(a2); cyl(.011, .011, .26, soft(0xF0B8C6), 0, .13, 0, 10, { parent: a2 });
    const hd = new THREE.Group(); hd.position.y = .26; hd.rotation.z = -1.9; a2.add(hd); const sh = new THREE.Mesh(new THREE.CylinderGeometry(.04, .1, .13, 24, 1, true), RM.lampShade); sh.material.side = THREE.DoubleSide; hd.add(sh);
    RM.bulb = new THREE.Mesh(new THREE.SphereGeometry(.03, 12, 10), new THREE.MeshBasicMaterial({ color: 0xFFE6C8, toneMapped: false })); RM.bulb.position.y = -.04; hd.add(RM.bulb); RM.lampHead = hd; }
  { const m = new THREE.Group(); m.position.set(.62, DESKY, .2); RM.add(m); const mm = new THREE.MeshPhysicalMaterial({ color: 0xF6F2EC, roughness: .3, clearcoat: .6 }); cyl(.045, .042, .1, mm, 0, .05, 0, 24, { parent: m }); const hdl = new THREE.Mesh(new THREE.TorusGeometry(.027, .008, 8, 20), mm); hdl.position.set(.05, .055, 0); m.add(hdl); cyl(.04, .04, .005, mat(0x5A3A24), 0, .095, 0, 20, { parent: m }); }
  RM.tri = new THREE.Group(); RM.tri.position.set(.25, DESKY, .05); RM.add(RM.tri);
  for (let k = 0; k < 3; k++) { const a = k * 2.09 + .3; for (let j = 0; j < 6; j++) { const b = new THREE.Mesh(new THREE.SphereGeometry(.012, 8, 6), mat(0x1E1E22, { roughness: .4 })); b.position.set(Math.sin(a) * (.07 - j * .011), .01 + j * .022, Math.cos(a) * (.07 - j * .011)); RM.tri.add(b); } }
  RM.triPhone = new THREE.Group(); RM.triPhone.position.y = .2; RM.tri.add(RM.triPhone); rbox(.075, .15, .01, mat(0x2A2A30, { roughness: .3 }), 0, 0, 0, .008, { parent: RM.triPhone });
  RM.triScr = new THREE.MeshBasicMaterial({ color: 0xFFE3F1, toneMapped: false }); { const s = new THREE.Mesh(new THREE.PlaneGeometry(.066, .138), RM.triScr); s.position.z = -.006; s.rotation.y = Math.PI; RM.triPhone.add(s); }
  // the chair: white shell on a star base with wheels
  { const C2 = new THREE.Group(); C2.position.set(SEAT.x, 0, SEAT.z); RM.add(C2); const cw = soft(0xF4F2F6); rbox(.52, .07, .5, cw, 0, .5, -.02, .03, { parent: C2 }); rbox(.5, .5, .06, cw, 0, .8, -.27, .05, { parent: C2 }); cyl(.025, .025, .38, metal(0xC8C8D0, .3), 0, .3, 0, 10, { parent: C2 });
    for (let k = 0; k < 5; k++) { const a = k * 1.2566; const leg = rbox(.24, .025, .04, cw, Math.sin(a) * .12, .07, Math.cos(a) * .12, .012, { parent: C2 }); leg.rotation.y = a + Math.PI / 2; const w = new THREE.Mesh(new THREE.SphereGeometry(.03, 10, 8), mat(0x2A2A30)); w.position.set(Math.sin(a) * .24, .03, Math.cos(a) * .24); C2.add(w); } RM.chair = C2; }
  // the ring light, front left
  RM.ring = new THREE.Group(); RM.ring.position.set(-1.3, 0, .6); RM.ring.rotation.y = -.55; RM.add(RM.ring);
  cyl(.014, .014, 1.45, mat(0x1E1E22, { roughness: .4 }), 0, .72, 0, 10, { parent: RM.ring });
  for (let k = 0; k < 3; k++) { const l = cyl(.011, .011, .5, mat(0x1E1E22), Math.sin(k * 2.1) * .16, .18, Math.cos(k * 2.1) * .16, 8, { parent: RM.ring }); l.rotation.set(Math.cos(k * 2.1) * .75, 0, -Math.sin(k * 2.1) * .75); }
  const rh = new THREE.Mesh(new THREE.TorusGeometry(.25, .035, 12, 64), mat(0x1E1E22, { roughness: .4 })); rh.position.y = 1.58; RM.ring.add(rh);
  RM.ringM = new THREE.MeshBasicMaterial({ color: 0xFFF4EA, toneMapped: false }); const rg = new THREE.Mesh(new THREE.TorusGeometry(.25, .018, 10, 64), RM.ringM); rg.position.set(0, 1.58, .02); RM.ring.add(rg);
  // the bed along the right: frame, mattress, pink knitted blanket, pillows
  rbox(1.35, .3, 2.2, mat(0xD9C6A8), 2.75, .15, -1.15, .04); rbox(1.3, .2, 2.12, soft(0xF6F2F4), 2.75, .4, -1.15, .08);
  rbox(1.35, .7, .1, mat(0xD9C6A8), 2.75, .5, -2.28, .04);
  RM.knitM = texMat("knit", { transparent: false }); RM.knitM.toneMapped = true;
  { const kn = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .95 }); LATE.push([kn, "knit"]); rbox(1.38, .1, 1.3, kn, 2.75, .52, -.62, .05); rbox(.08, .45, 1.3, kn, 2.08, .32, -.62, .04); }
  rbox(.6, .16, .36, soft(0xF0B8C6), 2.55, .58, -1.95, .07); rbox(.55, .15, .34, soft(0xD8D2E4), 3.05, .58, -1.97, .07);
  // a rug, crumpled paper balls, a cable on the floor, a bin
  { const rug = new THREE.Mesh(new THREE.CircleGeometry(1.1, 48), soft(0xDCD4E4, { roughness: .95 })); rug.rotation.x = -Math.PI / 2; rug.scale.set(1.3, .8, 1); rug.position.set(1.4, .006, .2); add(rug, false, true); }
  for (let k = 0; k < 7; k++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(.05, 1), soft(0xF8F6F2)); b.geometry.attributes.position.array.forEach((_, i, a) => { a[i] *= .8 + .4 * hash(i * 1.7 + k); }); b.geometry.computeVertexNormals(); b.position.set(.6 + hash(k) * 1.6, .045, -.1 + hash(k * 3) * 1.0); b.rotation.set(k, k * 2, k * 3); add(b); }
  { const pts = [v3(-1.3, .01, .6), v3(-.9, .01, .9), v3(-.2, .01, .75), v3(.5, .01, .95), v3(1.0, .01, .6)]; add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 60, .008, 6), mat(0xEDEDF0))); }
  // lights: warm lamp key, cool moon fill from the window, a soft violet fill, the ring light, rims for the characters
  RM.lamp = new THREE.PointLight(0xFFD2B0, 0, 4, 1.6); RM.lamp.position.set(-.55, 1.15, -.05); scene.add(RM.lamp);
  RM.moon = new THREE.PointLight(0x9DB8FF, 0, 7, 1.3); RM.moon.position.set(-1.05, 1.9, -1.9); scene.add(RM.moon);
  RM.fill = new THREE.PointLight(0xC8B0FF, 0, 10, 1.2); RM.fill.position.set(1.0, 2.6, 2.8); scene.add(RM.fill);
  RM.key = new THREE.PointLight(0xFFF0E6, 0, 5, 1.6); RM.key.position.set(-1.2, 1.55, .5); scene.add(RM.key);
  RM.rim = new THREE.PointLight(0xFF8CC6, 0, 3, 1.6); scene.add(RM.rim);
  RM.rim2 = new THREE.PointLight(0xFFE8D0, 0, 3, 1.6); scene.add(RM.rim2);
}
// ---------------------------------------------------------------- the reel-world props: film strip, reel cards, the DM machine, paper planes, papers, speed lines
const FX = {};
{
  FX.strip = new THREE.Group(); RM.add(FX.strip); FX.frames = [];
  for (let i = 0; i < 7; i++) {
    const f = new THREE.Group(); f.position.set(-.45 + i * .15, DESKY + .42, -.1 - .06 * Math.sin(i / 6 * Math.PI)); f.rotation.y = (3 - i) * .06; FX.strip.add(f);
    const fm = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .95 }); LATE.push([fm, "thumb" + (i % 4)]);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.12, .2), fm); f.add(p);
    const edge = new THREE.Mesh(new THREE.PlaneGeometry(.135, .215), new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: .7 })); edge.position.z = -.002; f.add(edge);
    f.edge = edge; FX.frames.push(f);
  }
  FX.cards = new THREE.Group(); RM.add(FX.cards); FX.cardL = [];
  for (let i = 0; i < 5; i++) {
    const c = new THREE.Group(); FX.cards.add(c);
    const cmat = new THREE.MeshPhysicalMaterial({ color: i === 3 ? 0xFFE4A0 : 0xFFF2F8, roughness: .3, transparent: true, opacity: .9, emissive: i === 3 ? 0x8A5A00 : 0x000000, emissiveIntensity: 0, side: THREE.DoubleSide });
    c.add(new THREE.Mesh(new RoundedBoxGeometry(.17, .27, .008, 2, .015), cmat));
    const im = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .95 }); LATE.push([im, "thumb" + ((i + 1) % 4)]);
    const ip = new THREE.Mesh(new THREE.PlaneGeometry(.14, .19), im); ip.position.set(0, .02, .006); c.add(ip);
    c.cmat = cmat; FX.cardL.push(c);
  }
  FX.mach = new THREE.Group(); FX.mach.position.set(.42, DESKY, .2); RM.add(FX.mach);
  rbox(.22, .14, .16, new THREE.MeshPhysicalMaterial({ color: 0xF06BB4, roughness: .35, clearcoat: .6 }), 0, .07, 0, .035, { parent: FX.mach });
  rbox(.12, .016, .02, mat(0x5A1A3E), 0, .1, .081, .006, { parent: FX.mach });
  const piv = new THREE.Group(); piv.position.set(.115, .09, 0); FX.mach.add(piv); FX.lever = piv;
  cyl(.007, .007, .14, metal(0xD9D9DE, .3), 0, .07, 0, 8, { parent: piv }); const kn = new THREE.Mesh(new THREE.SphereGeometry(.022, 16, 12), new THREE.MeshPhysicalMaterial({ color: 0xFFC21A, roughness: .3, clearcoat: .7 })); kn.position.y = .15; piv.add(kn);
  FX.machLight = new THREE.Mesh(new THREE.SphereGeometry(.013, 10, 8), new THREE.MeshBasicMaterial({ color: 0x3A3A3A })); FX.machLight.position.set(-.07, .145, .05); FX.mach.add(FX.machLight);
  FX.planes = [];
  const pg = new THREE.BufferGeometry(); pg.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, .06, -.04, 0, -.035, 0, .005, -.025, 0, 0, .06, .04, 0, -.035, 0, .005, -.025, 0, 0, .06, 0, -.018, -.03, 0, .005, -.025], 3)); pg.computeVertexNormals();
  for (let i = 0; i < 14; i++) { const p = new THREE.Mesh(pg, new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: .8, side: THREE.DoubleSide })); RM.add(p); FX.planes.push(p); }
  // loose papers that blow about on the teasers and the entrance
  FX.papers = [];
  for (let i = 0; i < 8; i++) { const p = new THREE.Mesh(new THREE.PlaneGeometry(.16, .21), new THREE.MeshStandardMaterial({ color: 0xFBFAF6, roughness: .9, side: THREE.DoubleSide, emissive: 0x8A8496, emissiveIntensity: .6 })); RM.add(p); FX.papers.push(p); }
  // speed lines behind Cree when he flies (thin, soft white, no glow)
  const slT = pix(16, 256, (g) => { const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "rgba(255,255,255,0)"); gr.addColorStop(.5, "rgba(255,255,255,.85)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(6, 0, 4, 256); }, false);
  FX.speed = new THREE.Group(); scene.add(FX.speed);
  for (let i = 0; i < 10; i++) { const s = new THREE.Mesh(new THREE.PlaneGeometry(.05, 1), new THREE.MeshBasicMaterial({ map: slT, transparent: true, depthWrite: false, opacity: .7 })); s.position.set((hash(i) - .5) * .6, (hash(i * 3) - .5) * .5, -.4 - hash(i * 5) * .6); s.rotation.x = Math.PI / 2; s.scale.y = .5 + hash(i * 7); FX.speed.add(s); }
  // a soft pink trail ribbon for the far-off flyby (thin, matte)
  FX.trail = new THREE.Mesh(new THREE.PlaneGeometry(1, .04), new THREE.MeshBasicMaterial({ color: 0xFF9BCF, transparent: true, opacity: .7, depthWrite: false })); scene.add(FX.trail);
  // the landing shockwave: a thin ring of dust on the desk
  FX.ring = new THREE.Mesh(new THREE.RingGeometry(.9, 1, 64), new THREE.MeshBasicMaterial({ color: 0xFFF4FA, transparent: true, opacity: .6, depthWrite: false, side: THREE.DoubleSide })); FX.ring.rotation.x = -Math.PI / 2; scene.add(FX.ring);
  FX.puffs = []; for (let i = 0; i < 10; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(.03, 10, 8), new THREE.MeshStandardMaterial({ color: 0xF4ECF4, roughness: 1, transparent: true, opacity: .7 })); scene.add(p); FX.puffs.push(p); }
  // a soft shadow sweep (the flying shadow passing over the room)
  FX.shadow = new THREE.Mesh(new THREE.CircleGeometry(.6, 32), new THREE.MeshBasicMaterial({ color: 0x0A0614, transparent: true, opacity: .35, depthWrite: false })); FX.shadow.rotation.x = -Math.PI / 2; scene.add(FX.shadow);
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

// ---------------------------------------------------------------- Cree, to his model sheet (refs/cree_reference.png): a soft pink egg,
// big glossy eyes set INTO the body (slightly domed, a pale pink rim), a rounded yellow beak with a red mouth, short mitten
// wings, big orange feet. Face rig: plush eyelids (upper and lower, tilting for emotion), pupils that look, dilate and dart,
// a hinged lower beak, blush. Built 1 unit tall; CREE.root is scaled to his size in the room.
const CREE = { root: new THREE.Group() };
scene.add(CREE.root);
{
  const R = CREE.root;
  const plush = CREE.plush = new THREE.MeshPhysicalMaterial({ color: 0xF75AAE, roughness: .62, sheen: .55, sheenColor: new THREE.Color(0xFFA6D4), sheenRoughness: .5, envMap: ENV, envMapIntensity: .15 });
  // the model sheet's "light subsurface scattering so the pink glows at the edges": a soft view-angle rim on the plush
  CREE.rimU = { value: .3 };
  plush.onBeforeCompile = (sh) => { sh.uniforms.uRim = CREE.rimU; sh.fragmentShader = "uniform float uRim;\n" + sh.fragmentShader.replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n  { float rimF = pow(1.0 - clamp(dot(normalize(vViewPosition), normal), 0.0, 1.0), 3.0); totalEmissiveRadiance += vec3(1.0, .3, .62) * rimF * uRim; }"); };
  const bod = new THREE.Group(); R.add(bod); CREE.bod = bod;
  // egg body: fuller at the bottom, a softly rounded crown
  const BW = (y) => .94 * (1 + .08 * (-y) - .015 * Math.max(0, y) ** 2);
  const g = new THREE.SphereGeometry(.5, 96, 72); const pa = g.attributes.position;
  for (let i = 0; i < pa.count; i++) { const y = pa.getY(i) / .5; const w = BW(y); pa.setX(i, pa.getX(i) * w); pa.setZ(i, pa.getZ(i) * w * .95); pa.setY(i, pa.getY(i) * .92); }
  g.computeVertexNormals();
  const body = new THREE.Mesh(g, plush); body.position.y = .53; body.castShadow = true; body.receiveShadow = true; bod.add(body);
  // a point on the body's surface (local to bod) at height y, sideways x, and its outward normal
  const surf = (x, y) => { const yr = (y - .53) / .47, w = BW(yr), ax = .5 * w * Math.sqrt(1 - yr * yr), az = ax * .95;
    const z = az * Math.sqrt(Math.max(0, 1 - (x / ax) ** 2)); const n = new THREE.Vector3(x / (ax * ax), yr * .9, z / (az * az)).normalize(); return [new THREE.Vector3(x, y, z), n]; };
  const sclM = CREE.sclM = new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .3, clearcoat: .5, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .15 });
  const pupM = CREE.pupM = new THREE.MeshPhysicalMaterial({ color: 0x0E080C, roughness: .25, clearcoat: .6, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .12 });
  const catM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF, toneMapped: false });
  const rimM = CREE.rimM = new THREE.MeshStandardMaterial({ color: 0xFFC7DF, roughness: .55 });
  const lashM = new THREE.MeshStandardMaterial({ color: 0xC2287A, roughness: .6 }), lashLoM = new THREE.MeshStandardMaterial({ color: 0xE8479C, roughness: .6 });
  const ER = .142;                                                  // eyeball radius: a sphere set into the body, the front domes out
  CREE.eyes = []; CREE.pupils = []; CREE.cats = []; CREE.lids = []; CREE.arcs = [];
  for (const s of [-1, 1]) {
    const [P, n] = surf(s * .178, .665);
    const eg = new THREE.Group(); eg.position.copy(P).addScaledVector(n, -(ER - .05)); eg.rotation.set(-Math.asin(n.y) * .8, Math.atan2(n.x, n.z), 0, "YXZ"); bod.add(eg);
    const rim = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.06, 40, 30), rimM); rim.position.z = -.022; eg.add(rim);
    const ball = new THREE.Group(); eg.add(ball);                    // scaled up for "wide" (surprised)
    ball.add(new THREE.Mesh(new THREE.SphereGeometry(ER, 48, 36), sclM));
    // the pupil: a cap on the eyeball that turns with it (real eye rotation); catchlights stay put (they are reflections)
    const pg = new THREE.Group(); ball.add(pg);
    const cap = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.004, 40, 16, 0, Math.PI * 2, 0, .9), pupM); cap.rotation.x = Math.PI / 2; pg.add(cap);
    const capS = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.005, 40, 16, 0, Math.PI * 2, 0, .7), pupM); capS.rotation.x = Math.PI / 2; capS.visible = false; pg.add(capS); pg.cap = cap; pg.capS = capS;
    const iris = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.002, 40, 16, 0, Math.PI * 2, 0, .98), new THREE.MeshPhysicalMaterial({ color: 0x4A1A34, roughness: .1, clearcoat: 1 })); iris.rotation.x = Math.PI / 2; pg.add(iris); pg.iris = iris;
    const cg = new THREE.Group(); ball.add(cg);
    const onEye = (dx, dy, r) => { const d = new THREE.Vector3(dx, dy, 1).normalize().multiplyScalar(ER * 1.012); const m = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 12), catM); m.position.copy(d); m.lookAt(d.clone().multiplyScalar(2)); m.scale.z = .3; cg.add(m); return m; };
    const c1 = onEye(.3, .32, .036), c2 = onEye(-.28, -.3, .018); onEye(.05, .42, .01);
    // eyelids: plush shells just outside the eyeball; upper (top hemisphere) and lower, each on a tilt pivot, with a darker lash line
    const mkLid = (upper) => {
      const tilt = new THREE.Group(); eg.add(tilt);
      const hinge = new THREE.Group(); tilt.add(hinge);
      const sh = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.075, 44, 22, 0, Math.PI * 2, upper ? 0 : Math.PI / 2, Math.PI / 2), plush); hinge.add(sh);
      if (upper) { const lash = new THREE.Mesh(new THREE.TorusGeometry(ER * 1.075, .0045, 8, 56), lashM); lash.rotation.x = Math.PI / 2; hinge.add(lash); }
      return { tilt, hinge };
    };
    const up = mkLid(true), lo = mkLid(false);
    // the closed-happy arc (a curved line over shut lids)
    const arc = new THREE.Mesh(new THREE.TorusGeometry(.08, .015, 10, 32, Math.PI), new THREE.MeshStandardMaterial({ color: 0x3A0A22, roughness: .5 }));
    arc.position.set(0, -.035, ER - .03); arc.visible = false; eg.add(arc);
    eg.ball = ball;
    CREE.eyes.push(eg); CREE.pupils.push(pg); CREE.cats.push([c1, c2]); CREE.lids.push([up, lo]); CREE.arcs.push(arc);
  }
  // blush: soft pink-red discs under the eyes (only for joy and the hug)
  CREE.blush = [];
  const blM = new THREE.MeshBasicMaterial({ color: 0xFF2E6E, transparent: true, opacity: 0, depthWrite: false });
  for (const s of [-1, 1]) { const [P, n] = surf(s * .265, .55); const b = new THREE.Mesh(new THREE.CircleGeometry(.055, 24), blM); b.position.copy(P).addScaledVector(n, .004); b.lookAt(b.position.clone().add(n)); b.scale.y = .62; bod.add(b); CREE.blush.push(b); }
  CREE.blM = blM;
  // beak: a rounded upper half and a hinged lower half, a red mouth with a little tongue between them
  const beakM = new THREE.MeshPhysicalMaterial({ color: 0xFFC21A, roughness: .3, clearcoat: .5, clearcoatRoughness: .25, envMap: ENV, envMapIntensity: .3 });
  const beakM2 = CREE.beakM2 = new THREE.MeshPhysicalMaterial({ color: 0xF2A516, roughness: .35, clearcoat: .4, envMap: ENV, envMapIntensity: .25 });
  const [BP] = surf(0, .565);
  const bk = new THREE.Group(); bk.position.set(0, .565, BP.z); bk.scale.setScalar(1.12); bod.add(bk);
  const up = new THREE.Mesh(new THREE.SphereGeometry(.072, 32, 20, 0, Math.PI * 2, 0, Math.PI / 2), beakM); up.scale.set(1.08, .8, 1.3); up.position.set(0, .004, .014); up.rotation.x = .42; bk.add(up);
  const mouth = new THREE.Mesh(new THREE.SphereGeometry(.056, 22, 16), new THREE.MeshStandardMaterial({ color: 0xB80E2C, roughness: .75 })); mouth.scale.set(1.0, .78, .62); mouth.position.set(0, -.012, .006); bk.add(mouth);
  const tongue = new THREE.Mesh(new THREE.SphereGeometry(.028, 16, 10), new THREE.MeshStandardMaterial({ color: 0xFF6A8A, roughness: .6 })); tongue.scale.set(1.15, .42, .95); tongue.position.set(0, -.024, .03); bk.add(tongue);
  const lowG = new THREE.Group(); lowG.position.set(0, -.004, .006); bk.add(lowG);
  const low = new THREE.Mesh(new THREE.SphereGeometry(.06, 28, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), beakM2); low.scale.set(1.0, .72, 1.2); low.position.set(0, 0, .016); lowG.add(low);
  CREE.jaw = lowG;
  // wings: short rounded mittens from the sides, pivoting at the shoulder; the tip curls a little on the flap
  CREE.wings = [];
  for (const s of [-1, 1]) {
    const pv = new THREE.Group(); pv.position.set(s * .43, .5, .05); bod.add(pv);
    const w = new THREE.Mesh(new THREE.SphereGeometry(.14, 28, 20), plush); w.scale.set(.62, 1.0, .85); w.position.set(s * .03, -.1, 0); w.castShadow = true; pv.add(w);
    const tip = new THREE.Group(); tip.position.set(s * .06, -.24, .02); pv.add(tip); pv.tip = tip;
    CREE.wings.push(pv);
  }
  CREE.feet = [];
  for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.SphereGeometry(.112, 26, 16), beakM2); f.scale.set(1.12, .56, 1.6); const fg = new THREE.Group(); fg.position.set(s * .165, .052, .12); fg.add(f); f.castShadow = true; R.add(fg); CREE.feet.push(fg); }
  const mg = new THREE.Group(); CREE.mag = mg;
  mg.add(new THREE.Mesh(new THREE.TorusGeometry(.11, .012, 10, 40), goldM));
  mg.add(new THREE.Mesh(new THREE.CircleGeometry(.105, 36), new THREE.MeshPhysicalMaterial({ color: 0xEAF6FF, roughness: 0, transparent: true, opacity: .2, envMap: ENV, envMapIntensity: 1.2, side: THREE.DoubleSide })));
  const hd = new THREE.Mesh(new THREE.CylinderGeometry(.016, .02, .17, 12), mat(0x8A5A34, { roughness: .5 })); hd.position.y = -.2; mg.add(hd);
  const fer = new THREE.Mesh(new THREE.CylinderGeometry(.019, .019, .025, 12), goldM); fer.position.y = -.115; mg.add(fer);
  scene.add(mg);
}
// expressions: upper lid (0 open .. 1 shut), lower lid, lid tilt (+ = inner corners down: determined; - = sad/soft), pupil size
const EXPR = {
  open:       { lu: -.04, ll: 0,   tilt: 0,    pup: 1, blush: .28 },
  wide:       { lu: -.08, ll: 0,   tilt: 0,    pup: .85, wide: 1, blush: .2 },
  joy:        { lu: .04, ll: .3,   tilt: -.1,  pup: 1, blush: .55 },
  proud:      { lu: .14, ll: .26,  tilt: -.12, pup: 1, blush: .4 },
  determined: { lu: .18, ll: .1,   tilt: .14,  pup: 1, blush: .25 },
  focus:      { lu: .1,  ll: .14,  tilt: .06,  pup: 1, blush: .25 },
  curious:    { lu: -.04, ll: .02, tilt: -.08, pup: 1, asym: .1, blush: .3 },
  soft:       { lu: .12, ll: .18,  tilt: -.16, pup: 1, blush: .5 },
  squint:     { lu: .3,  ll: .3,   tilt: 0,    pup: 1, blush: .4 },
  closed:     { lu: 1.0, ll: .2,   tilt: 0,    pup: 1, blush: .3 },
  happy:      { lu: 1.0, ll: .55,  tilt: 0,    pup: 1, arcs: 1, blush: .6 },
};
// a natural blink: about every 2.4-3.6 s, sometimes a double blink; 0..1 lid closure
const creeBlink = (t) => { const P = 3.0, k = Math.floor(t / P), ph = t - k * P - hash(k * 1.3) * 1.2; const b = (x) => x > 0 && x < .17 ? Math.sin(x / .17 * Math.PI) : 0; return Math.max(b(ph), hash(k * 7.7) > .65 ? b(ph - .25) : 0); };
// state -> pose. s: {x, y, z, ry, rx (pitch), roll, sc, sq (+ squash / - stretch), wl/wr: [rz, rx], flap: [amp, hz], eyes (an EXPR key),
//   look: [x, y], jaw, mag, magAt, step, feetBack, wink (0/1: his left eye), still (no idle), noblink, glow}
function placeCree(vis, s) {
  CREE.root.visible = !!vis; CREE.mag.visible = !!(vis && s.mag);
  if (!vis) return;
  const R = CREE.root, sc = s.sc ?? .34, sq = s.sq ?? 0, t = NOW;
  const dk = !!CREE.dark;
  CREE.plush.envMapIntensity = dk ? 0 : .22; CREE.rimU.value = dk ? .22 : (s.glow ?? .3); CREE.sclM.color.set(dk ? 0x2A1A26 : 0xFFFFFF); CREE.rimM.color.set(dk ? 0x2A1424 : 0xFFC7DF);
  // idle life: breathing, a little sway (unless he is mid-move)
  const still = !!s.still, br = still ? 0 : Math.sin(t * 5.6) * .012, sway = still ? 0 : Math.sin(t * 1.3 + .7) * .025;
  R.position.set(s.x, s.y, s.z); R.rotation.set(s.rx ?? 0, s.ry ?? 0, (s.roll ?? 0) + sway, "YXZ"); R.scale.setScalar(sc);
  CREE.bod.scale.set(1 + sq * .5 - br * .5, 1 - sq + br, 1 + sq * .5 - br * .5);
  const ex = EXPR[s.eyes || "open"] || EXPR.open;
  const blink = (s.noblink || ex.arcs || ex.lu >= 1) ? 0 : creeBlink(t);
  // pupils dart a little when he is not looking at something on purpose
  const dart = s.look ? [0, 0] : [(hash(Math.floor(t / .9)) - .5) * .5, (hash(Math.floor(t / .9) + 9) - .5) * .3];
  const lk = s.look || [0, 0];
  const fl = s.flap ? Math.sin(t * Math.PI * 2 * s.flap[1]) * s.flap[0] : 0;
  for (let k = 0; k < 2; k++) {
    const sgn = k ? 1 : -1, w = k ? s.wr : s.wl;
    CREE.wings[k].rotation.set(w ? w[1] : 0, 0, sgn * ((w ? w[0] : .26) + fl + (still ? 0 : Math.sin(t * 5.6 + k) * .03)));
    const eg = CREE.eyes[k], [up, lo] = CREE.lids[k];
    const winkK = s.wink && k === 0 ? 1 : 0;
    let lu = ex.lu + (ex.asym ? (k ? ex.asym : -ex.asym * .3) : 0); lu = lerp(lu, 1, Math.max(blink, winkK)); lu = Math.min(1, lu);
    const ll = winkK ? .45 : ex.ll;
    up.hinge.rotation.x = -Math.PI / 2 + Math.PI * 1.03 * clamp(lu, -.05, 1);     // 0: tucked behind the eye .. 1: shut
    lo.hinge.rotation.x = Math.PI / 2 - Math.PI * clamp(ll, 0, 1);                // 0: tucked .. .5: covers the lower half
    up.tilt.rotation.z = -sgn * ex.tilt; lo.tilt.rotation.z = sgn * ex.tilt * .4;
    eg.ball.scale.setScalar(ex.wide ? 1.08 : 1);
    const pg = CREE.pupils[k]; pg.rotation.set(-(lk[1] + dart[1]) * .32, (lk[0] + dart[0]) * .38, 0); const small = (s.pup ?? ex.pup) < .9; pg.cap.visible = !small; pg.capS.visible = small; pg.iris.visible = !small;
    for (const c of CREE.cats[k]) c.visible = !dk;
    const arcs = !!ex.arcs && !winkK; CREE.arcs[k].visible = arcs; for (const c of eg.children) if (c !== CREE.arcs[k]) c.visible = !arcs;
  }
  CREE.blM.opacity = dk ? 0 : (s.blush ?? ex.blush ?? 0);
  CREE.jaw.rotation.x = (s.jaw ?? .32) * .95;
  for (let k = 0; k < 2; k++) { const f = CREE.feet[k]; f.position.y = .048 + (s.step && (k ? s.step > 0 : s.step < 0) ? Math.abs(s.step) * .07 : 0); f.position.z = .11 - (s.feetBack ?? 0) * .12; f.rotation.x = (s.feetBack ?? 0) * 1.0; f.rotation.z = (k ? -1 : 1) * (s.feetSplay ?? 0); }
  R.updateMatrixWorld(true);
  if (s.mag === "hand") { CREE.wings[1].tip.getWorldPosition(V); CREE.mag.position.copy(V).add(V2.set(0, .04 * sc / .34, .02)); CREE.mag.rotation.set(s.magRx ?? 0, s.ry ?? 0, s.magRz ?? .25); CREE.mag.scale.setScalar(sc / .34 * .55); }
  if (s.mag === "desk") { CREE.mag.position.copy(s.magAt); CREE.mag.rotation.set(-Math.PI / 2 + .1, 0, .6); CREE.mag.scale.setScalar(.55); }
}
// Cree "talks" in chirps: the beak follows the loudness of his chirps (CT.creeEnv, 30 values per second)
const envAt = (arr, t) => { if (!arr) return 0; const i = t * 30, a = Math.floor(i), f = i - a; return lerp(arr[Math.min(arr.length - 1, Math.max(0, a))] || 0, arr[Math.min(arr.length - 1, Math.max(0, a + 1))] || 0, f); };
const creeJaw = (t) => .18 + .85 * envAt(C.creeEnv, t);

// ================================================================= THE CREATOR: a soft designer-toy figure with a face rig
// Same skeleton and pivots as the house characters (pose() / applyPose() drive him), but smooth: capsule limbs, a big round
// head, sphere eyes with lids, brows, a mouth that opens with the loudness of his voice, tears.
function makeToy(parent = scene) {
  const skinM = new THREE.MeshPhysicalMaterial({ color: 0xF2C7A6, roughness: .55, sheen: .4, sheenColor: new THREE.Color(0xFFD8C8), sheenRoughness: .5, envMap: ENV, envMapIntensity: .15 });
  const hoodM = new THREE.MeshPhysicalMaterial({ color: 0xEFE7D8, roughness: .85, sheen: 1, sheenColor: new THREE.Color(0xFFFFFF), sheenRoughness: .7 });
  const pantM = new THREE.MeshPhysicalMaterial({ color: 0x8C8A8E, roughness: .85, sheen: .8, sheenColor: new THREE.Color(0xD8D8DC), sheenRoughness: .7 });
  const shoeM = new THREE.MeshPhysicalMaterial({ color: 0xF6F6F4, roughness: .45, clearcoat: .2 });
  const hairM = new THREE.MeshPhysicalMaterial({ color: 0x1E1A1C, roughness: .5, sheen: .5, sheenColor: new THREE.Color(0x5A5060), sheenRoughness: .4 });
  const root = new THREE.Group(); parent.add(root);
  const hips = new THREE.Group(); hips.position.y = HIP; root.add(hips);
  const mk = (geo, m, par, x, y, z, sx = 1, sy = 1, sz = 1) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.scale.set(sx, sy, sz); o.castShadow = true; o.receiveShadow = true; par.add(o); return o; };
  const SPH = new THREE.SphereGeometry(1, 40, 30);
  const torso = new THREE.Group(); hips.add(torso);
  // hoodie: a soft rounded body, a hem band, the hood around the neck, two drawstrings
  mk(new THREE.CapsuleGeometry(.27, .2, 10, 24), hoodM, torso, 0, .33, 0, 1.08, 1, .7);
  const hood = mk(new THREE.TorusGeometry(.17, .05, 14, 32), hoodM, torso, 0, .6, -.07); hood.rotation.x = Math.PI / 2 - .35; hood.scale.set(1.15, 1, 1);
  for (const s of [-1, 1]) { const d = mk(new THREE.CylinderGeometry(.008, .008, .16, 6), mat(0xF6F2EA), torso, s * .05, .52, .2); }
  mk(new RoundedBoxGeometry(.54, .16, .3, 3, .07), pantM, hips, 0, -.04, 0);
  mk(new THREE.CylinderGeometry(.07, .075, .1, 16), skinM, torso, 0, .64, 0);
  const neck = new THREE.Group(); neck.position.y = .66; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head);
  const HR = .255, HC = .28;          // head radius, centre height above the neck pivot
  { const hg = new THREE.SphereGeometry(1, 48, 36); const ha = hg.attributes.position; for (let i = 0; i < ha.count; i++) { const y = ha.getY(i); if (y < 0) { const k = 1 - .1 * (-y) ** 1.5; ha.setX(i, ha.getX(i) * k); ha.setZ(i, ha.getZ(i) * (1 - .04 * (-y))); } } hg.computeVertexNormals(); mk(hg, skinM, head, 0, HC, 0, HR, HR * 1.06, HR * .98); }
  const surfZ = (x, y) => HR * .98 * Math.sqrt(Math.max(0, 1 - (x / HR) ** 2 - ((y - HC) / (HR * 1.06)) ** 2));
  for (const s of [-1, 1]) mk(SPH, skinM, head, s * HR * .98, HC - .02, -.01, .045, .07, .055);
  mk(SPH, skinM, head, 0, HC - .06, surfZ(0, HC - .06) - .005, .034, .03, .03);
  // eyes: sclera, brown iris, pupil, a catchlight; skin lids that close over them; brows above
  const sclM = new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .2, clearcoat: .8, envMap: ENV, envMapIntensity: .3 });
  const irisM = new THREE.MeshPhysicalMaterial({ color: 0x6A3A1E, roughness: .2, clearcoat: 1, envMap: ENV, envMapIntensity: .5 });
  const pupM = new THREE.MeshBasicMaterial({ color: 0x0A0606 }), catM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
  const eyes = [], irises = [], lidsU = [], lidsL = [], brows = [], tears = [], lashes = [];
  for (const s of [-1, 1]) {
    const ex = s * .095, ey = HC + .02, ez = surfZ(ex, ey) - .03;
    const eg = new THREE.Group(); eg.position.set(ex, ey, ez); eg.rotation.y = s * .22; head.add(eg);
    mk(SPH, sclM, eg, 0, 0, 0, .062, .07, .045);
    const ig = new THREE.Group(); ig.position.z = .03; eg.add(ig);
    mk(SPH, irisM, ig, 0, 0, 0, .042, .046, .018); mk(SPH, pupM, ig, 0, 0, .008, .022, .024, .012); mk(SPH, catM, ig, .014, .016, .018, .01, .01, .005);
    const lu = new THREE.Group(); eg.add(lu); const lum = mk(new THREE.SphereGeometry(1, 28, 16, 0, Math.PI * 2, 0, Math.PI / 2), skinM, lu, 0, 0, 0, .064, .072, .062); lu.rotation.x = -1.35;
    const ll = new THREE.Group(); eg.add(ll); mk(new THREE.SphereGeometry(1, 28, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), skinM, ll, 0, 0, 0, .063, .071, .06); ll.rotation.x = 1.45;
    const bg = new THREE.Group(); bg.position.set(s * .1, HC + .12, surfZ(s * .1, HC + .12) + .004); bg.rotation.y = s * .22; head.add(bg);
    const br = mk(new THREE.CapsuleGeometry(.017, .075, 4, 10), hairM, bg, 0, 0, 0); br.rotation.z = Math.PI / 2; br.scale.set(1, 1, .6);
    const tg = new THREE.Group(); tg.position.set(ex + s * .01, ey - .07, surfZ(ex, ey - .07) + .004); head.add(tg);
    const tmM = new THREE.MeshPhysicalMaterial({ color: 0x6CC0F5, roughness: .05, transparent: true, opacity: .85, clearcoat: 1, envMap: ENV, envMapIntensity: .6 });
    const tm = mk(new THREE.CapsuleGeometry(.007, .05, 4, 8), tmM, tg, 0, -.025, 0, 1, 1, .5); tm.castShadow = false; const td = mk(SPH, tmM, tg, 0, -.062, .003, .013, .017, .009); td.castShadow = false;
    const ck = mk(SPH, new THREE.MeshStandardMaterial({ color: 0xF59AA0, roughness: .8, transparent: true, opacity: .45 }), head, s * .14, HC - .08, surfZ(s * .14, HC - .08) - .006, .045, .028, .012); ck.castShadow = false;
    const lash = new THREE.Group(); lash.position.set(ex, ey, ez + .066); lash.rotation.y = s * .22; head.add(lash);
    const la = mk(new THREE.TorusGeometry(.046, .0075, 8, 24, Math.PI), new THREE.MeshStandardMaterial({ color: 0x2A1A18, roughness: .6 }), lash, 0, 0, 0); la.castShadow = false;
    lashes.push(lash);
    eyes.push(eg); irises.push(ig); lidsU.push(lu); lidsL.push(ll); brows.push(bg); tears.push(tg);
  }
  // the mouth: closed lines (smile / flat / frown / wobble) and an open mouth (dark, tongue, teeth) scaled by the voice
  const mY = HC - .135, mZ = surfZ(0, HC - .135);
  const mouthG = new THREE.Group(); mouthG.position.set(0, mY, mZ - .006); head.add(mouthG);
  const lipM = new THREE.MeshStandardMaterial({ color: 0x7A3A30, roughness: .6 });
  const curve = (k) => new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(v3(-.045, k, 0), v3(0, -k, .006), v3(.045, k, 0)), 16, .0065, 6);
  const lines = { smile: mk(curve(.014), lipM, mouthG, 0, 0, 0), flat: mk(curve(0), lipM, mouthG, 0, 0, 0), sad: mk(curve(-.014), lipM, mouthG, 0, 0, 0) };
  const wob = new THREE.TubeGeometry(new THREE.CatmullRomCurve3([v3(-.045, -.006, 0), v3(-.022, .004, .004), v3(0, -.004, .006), v3(.022, .004, .004), v3(.045, -.006, 0)]), 20, .0065, 6); lines.wavy = mk(wob, lipM, mouthG, 0, 0, 0);
  const open = new THREE.Group(); mouthG.add(open);
  mk(SPH, new THREE.MeshStandardMaterial({ color: 0x3A0E14, roughness: .8 }), open, 0, 0, 0, .045, .03, .012);
  mk(SPH, new THREE.MeshStandardMaterial({ color: 0xD8616A, roughness: .7 }), open, 0, -.014, .004, .028, .012, .008);
  const teeth = mk(SPH, new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: .4 }), open, 0, .021, .006, .034, .007, .006);
  // hair: soft wavy clumps on top and at the back, a swept fringe
  const HP = [[0, .5, -.02, .2, .1, .19], [-.13, .46, .02, .13, .1, .15], [.13, .47, .0, .13, .1, .15], [-.2, .37, -.04, .09, .12, .15], [.2, .38, -.05, .09, .12, .15], [0, .4, -.17, .2, .14, .12], [-.12, .33, -.2, .14, .12, .1], [.12, .33, -.2, .14, .12, .1],
    [-.06, .47, .15, .14, .065, .08], [.08, .46, .16, .12, .06, .07], [.17, .43, .12, .07, .06, .07], [-.18, .42, .1, .07, .07, .07], [0, .52, .05, .15, .06, .14], [.05, .55, -.08, .1, .05, .1]];
  for (const [x, y, z, sx, sy, sz] of HP) { const h = mk(SPH, hairM, head, x, y, z, sx, sy, sz); h.rotation.set(hash(x * 9 + y) * .6 - .3, hash(z * 7 + x) * .8, hash(y * 5) * .5 - .25); }
  // arms (hoodie sleeves with cuffs, soft hands) and legs (joggers with cuffs, white sneakers)
  const sh = [], el = [], hand = [], hip = [], knee = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * .31, .52, 0); torso.add(a); sh.push(a);
    mk(new THREE.CapsuleGeometry(.09, .2, 6, 16), hoodM, a, 0, -.13, 0);
    const e = new THREE.Group(); e.position.y = -.29; a.add(e); el.push(e);
    mk(new THREE.CapsuleGeometry(.082, .16, 6, 16), hoodM, e, 0, -.12, 0);
    mk(new THREE.CylinderGeometry(.075, .078, .05, 16), hoodM, e, 0, -.24, 0);
    const hd = new THREE.Group(); hd.position.y = -.31; e.add(hd);
    mk(SPH, skinM, hd, 0, -.01, 0, .062, .072, .042); mk(SPH, skinM, hd, s * -.045, .005, .02, .022, .032, .02);
    hand.push(hd);
    const h = new THREE.Group(); h.position.set(s * .13, 0, 0); hips.add(h); hip.push(h);
    mk(new THREE.CapsuleGeometry(.115, .24, 6, 16), pantM, h, 0, -.19, 0);
    const kn = new THREE.Group(); kn.position.y = -.4; h.add(kn); knee.push(kn);
    mk(new THREE.CapsuleGeometry(.098, .2, 6, 16), pantM, kn, 0, -.16, 0);
    mk(new THREE.CylinderGeometry(.085, .09, .05, 16), pantM, kn, 0, -.29, 0);
    mk(new RoundedBoxGeometry(.2, .12, .33, 4, .055), shoeM, kn, 0, -.37, .05);
    mk(new RoundedBoxGeometry(.21, .035, .34, 3, .015), mat(0xDCDCDA), kn, 0, -.425, .05);
  }
  return { root, hips, torso, head, sh, el, hand, hip, knee, eyes, irises, lidsU, lidsL, brows, tears, lashes, lines, open, teeth, seed: 1.7, toy: true };
}
// face: eyes 'open'|'wide'|'half'|'closed'|'happy'|'teary'|'cry'|'sob'; brows 'flat'|'up'|'high'|'worry'|'despair'|'angry'|'raise1';
// mouth 'smile'|'flat'|'sad'|'wavy'|'o'|'gasp'|'wail'|'rant'|'laugh'|'grin'; talk: the mouth opens with the voice (CT.voiceEnv)
function setToyFace(P, f) {
  let eyes = f.eyes || "open";
  const blink = (eyes === "open" || eyes === "wide" || eyes === "teary") && !f.noblink && blinkAt(P.seed, NOW);
  const LID = { open: [-1.35, 1.45], wide: [-1.6, 1.6], half: [-.55, 1.45], closed: [.14, -.06], happy: [.14, -.06], teary: [-1.2, 1.25], cry: [.14, -.06], sob: [.14, -.06] }[eyes] || [-1.35, 1.45];
  for (let k = 0; k < 2; k++) {
    P.lidsU[k].rotation.x = blink ? .14 : LID[0]; P.lidsL[k].rotation.x = blink ? -.06 : LID[1];
    const shut = blink || eyes === "closed" || eyes === "cry" || eyes === "happy" || eyes === "sob";
    P.lashes[k].visible = shut; P.lashes[k].rotation.z = (eyes === "happy" || eyes === "sob") ? 0 : Math.PI;    // up-curved when happy, down when crying
    P.lashes[k].position.y = .28 + .02 + ((eyes === "happy" || eyes === "sob") ? -.012 : .012);
    P.irises[k].scale.setScalar(1);
    const lk = f.look || [0, 0]; P.irises[k].position.set(lk[0] * .012, lk[1] * .012, .03);
    P.tears[k].visible = eyes === "teary" || eyes === "cry" || eyes === "sob";
    P.tears[k].scale.y = eyes === "teary" ? .35 : 1;
    const s = k ? 1 : -1, b = P.brows[k];
    const BR = { flat: [0, 0], up: [.02, 0], high: [.035, .05], worry: [.012, .35], despair: [.02, .55], angry: [-.012, -.45], raise1: [k ? 0 : .035, 0] }[f.brows || "flat"];
    b.position.y = .29 + .12 + BR[0]; b.rotation.z = s * -BR[1];
  }
  let mouth = f.mouth || "smile", amt = 0;
  if (f.talk) { amt = envAt(C.voiceEnv, NOW); }
  const OPEN = { o: [.55, .55], gasp: [.7, .9], wail: [1.2, 1.1], rant: [1.1, .8], laugh: [1.15, .75], grin: [1.0, .35] };
  let os = null;
  if (OPEN[mouth]) os = OPEN[mouth];
  if (f.talk && amt > .06) { const base = os || [.9, .5]; os = [base[0] * (.75 + .25 * amt), Math.max(.18, base[1] * (.3 + amt))]; }
  for (const k in P.lines) P.lines[k].visible = !os && k === (P.lines[mouth] ? mouth : "flat");
  P.open.visible = !!os;
  if (os) { P.open.scale.set(os[0], os[1], 1); P.teeth.visible = mouth !== "o" && mouth !== "gasp"; }
}
// v4: the creator is back in the house blocky style (makeChar); his pixel mouth follows the loudness of his voice
const LEO = makeChar({ id: "leo", skin: "#E2AE86", hair: "#2A1A12", style: "short", top: "#EFE6D6", topStyle: "hoodie", pants: "#6A6660", shoe: "#FFFDF8", brow: "#2A1A12" }, scene);
LEO.seed = 1.7;
function placeToy(P, vis, p, f) {
  f = { ...(f || {}) };
  if (f.talk) { const a = envAt(C.voiceEnv, NOW); f.talk = false; f.mouth = a < .08 ? (f.mouth || "flat") : (a < .4 ? "talk" : (f.big ? (a > .7 ? "wail" : "rant") : "o")); }
  placeChar(P, vis, p, f);
}
// his phone (in the right hand)
LEO.phone = new THREE.Group(); LEO.hand[1].add(LEO.phone); LEO.phone.position.set(0, -.02, .1);
rbox(.075, .15, .01, mat(0x2A2A30, { roughness: .3 }), 0, 0, 0, .008, { parent: LEO.phone, cast: false });
LEO.scr = new THREE.MeshBasicMaterial({ color: 0xDDE8FF, toneMapped: false }); { const sp = new THREE.Mesh(new THREE.PlaneGeometry(.066, .138), LEO.scr); sp.position.z = -.006; sp.rotation.y = Math.PI; LEO.phone.add(sp); }
const PEN = cyl(.007, .007, .13, mat(0xF343A2), 0, 0, 0, 8); PEN.rotation.z = Math.PI / 2;

// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const Ls = (k) => C.lines[k][0], Le = (k) => C.lines[k][1], Bs = (k) => C.beats[k][0], Be = (k) => C.beats[k][1];
const talking = (t, k) => t > Ls(k) - .03 && t < Le(k) + .05;
const wordT = (k, i) => { const ws = C.words.filter((w) => w.take === k); return ws[Math.min(i, ws.length - 1)].s; };
// a cut on (nearly) every line, as the skits guide says; the rant is cut into three angles
const SHOTS = [
  ["phone", 0], ["rantA", Ls("02") - .1], ["rantB", wordT("02", 4) - .08], ["rantC", wordT("02", 9) - .08], ["thud", Bs("thud")],
  ["window", Ls("04") - .1], ["teaser1", Bs("teaser1")], ["bed", Ls("05") - .1], ["teaser2", Bs("teaser2")], ["pillow", Ls("06") - .1],
  ["hush", Bs("hero")], ["rise", Bs("hero") + .7], ["burst", Bs("hero") + 1.55], ["dive", Bs("hero") + 2.45], ["landing", Bs("hero") + 2.9], ["whoa", Ls("07") - .1], ["say", Bs("say")],
  ["fix1", Bs("fix1")], ["fix2", Bs("fix2")], ["fix3", Bs("fix3")], ["hug", Ls("10") - .15], ["end", Bs("endin")],
];
const shotAt = (t) => { let k = 0; for (let i = 0; i < SHOTS.length; i++) if (t >= SHOTS[i][1]) k = i; return [SHOTS[k][0], t - SHOTS[k][1], (SHOTS[k + 1] ? SHOTS[k + 1][1] : DUR) - SHOTS[k][1]]; };
const DESKC = v(.05, DESKY, .14);
const seated = (o = {}) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .08, ...o });
const standing = (o = {}) => pose({ a: [[.1, .1, .15], [.1, .1, .15]], ...o });
// ---------------------------------------------------------------- flight: he flies head-first along a curve, banking into turns,
// wings beating, feet tucked; a sparkle ribbon and sparks trail behind him
const curve = (pts) => new THREE.CatmullRomCurve3(pts.map((p) => v(...p)), false, "catmullrom", .5);
const PATH = {
  t1: curve([[-2.6, 1.7, -3.45], [-1.6, 2.15, -3.4], [-.9, 1.9, -3.35], [-.2, 2.25, -3.4], [.6, 2.0, -3.45]]),
  t2: curve([[-2.7, 1.75, -2.75], [-1.5, 1.95, -2.7], [-.4, 1.8, -2.72], [.9, 2.0, -2.78]]),
  in: curve([[-1.05, 1.85, -2.95], [-.95, 1.95, -2.15], [-.35, 2.15, -1.3], [.75, 2.1, -.75], [1.35, 1.85, .05], [.95, 2.0, .7], [.28, 2.12, .42]]),
};
function flyState(cv, k, o = {}) {
  const p = cv.getPointAt(clamp(k)), tg = cv.getTangentAt(clamp(k)), tg2 = cv.getTangentAt(clamp(k + .03));
  const hd = Math.atan2(tg.x, tg.z), el = Math.asin(clamp(tg.y, -1, 1));
  let dh = Math.atan2(tg2.x, tg2.z) - hd; dh = Math.atan2(Math.sin(dh), Math.cos(dh));
  return { x: p.x, y: p.y, z: p.z, ry: hd, rx: 1.25 - el * .7, roll: clamp(-dh * 9, -1, 1), still: true, noblink: true, feetBack: 1,
    wl: [.9, .2], wr: [.9, .2], flap: [.7, 6.5], eyes: "determined", look: [0, .6], jaw: .25, sq: -.08, ...o };
}
function trail(cv, k, span, camP, w, sparkN = 46) {
  const pts = []; for (let j = 0; j <= 30; j++) { const kk = k - span * (1 - j / 30); if (kk >= 0) pts.push(cv.getPointAt(clamp(kk))); }
  if (pts.length > 1) ribbon(pts, camP, w);
  for (let i = 0; i < Math.min(sparkN, FX.sparks.length); i++) {
    const sp = FX.sparks[i], ke = (i + hash(i * 1.7)) / sparkN, age = (k - ke) / (span * 1.6);
    sp.visible = age > 0 && age < 1; if (!sp.visible) continue;
    const p = cv.getPointAt(clamp(ke)); sp.position.set(p.x + (hash(i * 3) - .5) * .25 * age, p.y + (hash(i * 5) - .5) * .2 * age - .12 * age * age, p.z + (hash(i * 7) - .5) * .25 * age);
    const sz = (i % 5 ? .06 : .12) * (1 - age * .7) * Math.max(.6, w / .05); sp.scale.set(sz, sz, 1); sp.material.opacity = (1 - age) * .9; sp.material.rotation = i + age * 3;
  }
}
const POST = [];   // things that need his posed body (eye glints): run after placeCree
const ease = (x) => x < .5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2;
function papers(t0, t, origin, push, n = 8) {          // loose papers lifting and drifting (deterministic)
  for (let i = 0; i < FX.papers.length; i++) {
    const p = FX.papers[i], a = t - t0 - i * .05; p.visible = i < n && a > 0;
    if (!p.visible) continue;
    const k = Math.min(a, 2.5);
    p.position.set(origin.x + (hash(i) - .5) * .5 + push.x * k * (.6 + .5 * hash(i * 3)), origin.y + push.y * k - .25 * Math.max(0, k - .6) ** 2 + .05 * Math.sin(k * 6 + i), origin.z + (hash(i * 5) - .5) * .3 + push.z * k * (.6 + .5 * hash(i * 7)));
    p.rotation.set(-Math.PI / 2 + k * (2 + hash(i) * 3), k * (1 + hash(i * 2) * 2), k * (hash(i * 9) - .5) * 4);
    if (p.position.y < .01) p.position.y = .01;
  }
}

// ---------------------------------------------------------------- one frame
const CAM = { p: v(0, 1.5, 3), l: v(0, 1, 0), fov: 40, focus: 3, ap: .03 };
function shoot(t) {
  const [sh, u, len] = shotAt(t);
  RM.visible = true; CREE.dark = false;
  for (const k of ["strip", "cards", "mach", "speed", "trail", "shadow", "ring", "ribbon", "rays", "blast", "glint", "halo"]) FX[k].visible = false;
  for (const a of [FX.sparks, FX.shards, FX.dust]) for (const o of a) o.visible = false;
  POST.length = 0; let flash = 0;
  for (const p of FX.planes) p.visible = false; for (const p of FX.papers) p.visible = false; for (const p of FX.puffs) p.visible = false;
  PEN.visible = false; LEO.phone.visible = false;
  for (const h of RM.panes) h.rotation.y = 0; for (const c of RM.curt) c.rotation.set(0, 0, 0);
  for (let i = 0; i < RM.clouds.length; i++) RM.clouds[i].position.x = -2.2 + i * 1.4 + ((t * .05 + i * .3) % 1.2);
  scene.background = tmpC.set(0x14102A).clone(); scene.fog.color.set(0x14102A); scene.fog.near = 30; scene.fog.far = 90;
  hemi.color.set(0xB8A8E8); hemi.groundColor.set(0x3A2A3A); hemi.intensity = .55;
  sun.color.set(0xA8C0FF); sun.intensity = .5; sun.target.position.set(0, 0, -.5); sun.position.set(-2.5, 5, 3);
  const LAND = Bs("hero") + 2.75 + .3;
  const dim = ss(t, Ls("04") - .5, Bs("hero")) * (1 - ss(t, LAND + .1, LAND + .6));        // tension: 0 -> 1 through the wishes
  const warm = ss(t, LAND + .1, LAND + .6);                                                  // relief after the landing
  RM.lamp.intensity = 2.6 - 1.4 * dim + .8 * warm; RM.moon.intensity = 2.0 + .4 * dim; RM.fill.intensity = 1.3 - .6 * dim + .3 * warm; RM.key.intensity = 1.8 - 1.0 * dim + .4 * warm;
  hemi.intensity = .55 - .2 * dim + .1 * warm; RM.lamp.color.set(warm > .5 ? 0xFFD8B8 : 0xFFD2B0); RM.rim.intensity = 0; RM.rim2.intensity = 0;
  phoneL.intensity = 0; RM.triScr.color.set(0xFFE3F1); RM.lapScr.color.set(0x9FB2D8);
  for (const b of RM.fairy) b.visible = true; RM.bulb.visible = true;
  // the fairy lights twinkle gently
  RM.fairy.forEach((b, i) => b.scale.setScalar(.85 + .25 * (.5 + .5 * Math.sin(t * 2.2 + i * 1.7))));
  let bloomS = .12, vig = .3, dark = 0;
  let cree = null, leo = null, leoF = {}, leoRot = null;
  const cam = CAM; cam.ap = .03;

  if (sh === "phone") {             // 1. his phone's glow on his face: 42 views; he slumps
    const slump = ss(t, Le("01") - .2, Le("01") + .35);
    leo = seated({ lean: .05 + .12 * slump, hp: .12 + .15 * slump, hy: -.12, a: [[.4, .2, .5], [1.35, -.15, 1.85]] });
    leoF = { eyes: "teary", mouth: "wavy", brows: "despair", talk: talking(t, "01"), look: [-.4, -.3] };
    LEO.phone.visible = true; LEO.scr.color.set(0xDDE8FF);
    cam.p.set(.32, 1.68, 2.4 - .2 * ss(u, 0, len)); cam.l.set(.02, 1.48, -.7); cam.fov = 34; cam.focus = 3.0;
    RM.key.intensity = 1.1; phoneL.intensity = .45;
  } else if (sh === "rantA" || sh === "rantB" || sh === "rantC") {   // 2. the rant, three angles: arms up, counting, hands in his hair
    const x = .3 + .35 * Math.sin(t * 1.2), walkA = sh === "rantC" ? 0 : .6;
    let p = walk(standing({ x, z: .95, ry: Math.cos(t * 1.2) * .45 }), t * 3.2, walkA);
    if (sh === "rantA") p.a = [[2.9, .4, .25], [2.9, .4, .25]];
    if (sh === "rantB") p.a = [[.35, .2, .4], [1.55, .05, .45 + .25 * Math.sin(t * 9)]];
    if (sh === "rantC") { p.a = [[2.65, .75, 2.2], [2.65, .75, 2.2]]; p.hp = .12; }
    p.lean = -.06; leo = p;
    leoF = { eyes: "wide", mouth: "rant", brows: sh === "rantC" ? "despair" : "angry", talk: talking(t, "02"), noblink: true };
    if (sh === "rantA") { cam.p.set(.3, 1.4, 4.6 - .2 * u); cam.l.set(.3, 1.3, .9); cam.fov = 42; cam.focus = 3.7; }
    if (sh === "rantB") { cam.p.set(1.9, 1.55, 3.9); cam.l.set(.35, 1.35, .9); cam.fov = 38; cam.focus = 3.4; }
    if (sh === "rantC") { cam.p.set(.15, 1.7, 4.1 - .25 * ss(u, 0, len)); cam.l.set(.25, 1.5, .9); cam.fov = 34; cam.focus = 3.2; }
  } else if (sh === "thud") {     // 3. cheek on his arms on the desk, sobbing
    const drop = ss(u, 0, .25), bnc = .05 * Math.sin(clamp((u - .25) / .3) * Math.PI) * (u > .25 && u < .55 ? 1 : 0);
    leo = seated({ lean: .55 * drop - bnc, hp: -.05 * drop, hr: 1.05 * drop, hy: .05, a: [[.1 + 1.0 * drop, .55 * drop, 1.7 * drop], [.1 + 1.0 * drop, .55 * drop, 1.7 * drop]] });
    leoF = { eyes: u > .3 ? "cry" : "closed", mouth: talking(t, "03") ? "wail" : "sad", brows: "despair", talk: talking(t, "03") };
    PEN.visible = true; const pr = ramp(u, .25, 1.2), fall = Math.max(0, u - 1.2);
    PEN.position.set(.1 + .78 * pr + .2 * fall, Math.max(.008, DESKY + .008 - 2 * fall * fall), .28); PEN.rotation.set(u * 9, 0, Math.PI / 2);
    cam.p.set(.15, 1.3, 3.1); cam.l.set(-.2, .98, -.4); cam.fov = 30; cam.focus = 3.4;
  } else if (sh === "window") {   // 4. WISH 1: at the window, hands clasped, looking up at the moon
    leo = standing({ x: -.68, z: -1.35, ry: Math.PI, hp: -.3, hy: 0, a: [[1.45, -.25, 2.05], [1.45, -.25, 2.05]] });
    leoF = { eyes: "teary", mouth: talking(t, "04") ? "flat" : "smile", brows: "worry", talk: talking(t, "04"), look: [0, .8] };
    cam.p.set(-.66, 1.55, -3.6 + .15 * ss(u, 0, len)); cam.l.set(-.68, 1.62, -1.3); cam.fov = 48; cam.focus = 2.25;
    RM.moon.intensity = 3.2; RM.key.intensity = .8;
  } else if (sh === "teaser1") {  // 5. TEASER 1: the sky turns dramatic; a tiny pink hero arcs across it, rolls, and is gone (sparkle trail)
    const k = ramp(u, .15, 2.1);
    cam.p.set(-.55, 1.5, .2); cam.l.set(-1.0, 1.95, -3.0); cam.fov = 38 - 3 * ss(u, 0, len); cam.focus = 3.4;
    if (k > 0 && k < 1) { cree = flyState(PATH.t1, k, { sc: .2, eyes: "determined" }); cree.roll += Math.PI * 2 * ss(k, .45, .7); trail(PATH.t1, k, .22, cam.p, .035, 30); }
    for (let i = 0; i < RM.clouds.length; i++) RM.clouds[i].position.x = -2.4 + i * 1.4 + u * .9;
    for (const c of RM.curt) c.rotation.z = .06 * Math.sin(u * 3);
    RM.lamp.intensity = 1.2; RM.key.intensity = .5; hemi.intensity = .35; RM.moon.intensity = 1.5;
  } else if (sh === "bed") {      // 6. WISH 2: hugging his knees on the bed
    leo = pose({ x: 2.35, y: -.17, z: -1.0, ry: -Math.PI / 2 + .4, l: [[2.15, 2.45], [2.15, 2.45]], a: [[1.2, .3, 1.5], [1.25, .25, 1.45]], lean: .12, hp: .1, hy: .25 });
    leoF = { eyes: "teary", mouth: talking(t, "05") ? "flat" : "sad", brows: "despair", talk: talking(t, "05"), look: [.3, 0] };
    LEO.phone.visible = true;
    cam.p.set(.05 + .1 * ss(u, 0, len), 1.42, 1.35); cam.l.set(2.3, 1.05, -1.0); cam.fov = 36; cam.focus = 3.2;
  } else if (sh === "teaser2") {  // 7. TEASER 2: closer: he streaks past the window in a blur of pink; curtains blow in, papers lift
    const k = ease(ramp(u, .25, 1.05));
    cam.p.set(.6, 1.35, 1.6); cam.l.set(-.8, 1.55, -2.3); cam.fov = 44; cam.focus = 3.4;
    if (k > 0 && k < 1) { cree = flyState(PATH.t2, k, { sc: .42, eyes: "determined", flap: [.8, 7] }); trail(PATH.t2, k, .3, cam.p, .07, 26);
      FX.speed.visible = true; FX.speed.position.set(cree.x - .3, cree.y, cree.z); FX.speed.rotation.set(0, Math.PI / 2, 0); }
    const gust = ss(u, .5, .8) * (1 - ss(u, 1.6, 2.2));
    RM.curt[0].rotation.x = -.6 * gust; RM.curt[1].rotation.x = -.5 * gust; RM.curt[0].rotation.z = .15 * gust;
    papers(Bs("teaser2") + .6, t, v(-.1, DESKY + .02, .0), v(.3, .35, .4), 5);
    FX.shadow.visible = k > 0 && k < 1; FX.shadow.position.set(lerp(-2.0, 1.5, k), .01, -.6); FX.shadow.scale.set(1.4, .6, 1);
    RM.lamp.intensity = 1.6; RM.key.intensity = .9;
  } else if (sh === "pillow") {   // 8. WISH 3: peeking over the pillow, pleading
    leo = pose({ x: 2.7, y: .72, z: -2.25, l: [[0, .1], [0, .1]], a: [[2.7, .35, .5], [2.7, .35, .5]], hp: -1.05, hy: .12 });
    leoRot = [Math.PI / 2, 0, 0];
    leoF = { eyes: "teary", mouth: talking(t, "06") ? "flat" : "sad", brows: "despair", talk: talking(t, "06") };
    RM.lamp.intensity = 3.0; RM.lamp.position.set(2.65, 1.25, .75);
    cam.p.set(2.6, 1.45, 2.3); cam.l.set(2.7, .82, -.6); cam.fov = 36; cam.focus = 2.7;
  } else if (sh === "hush") {     // 9. the hush: the lights flicker and die, one by one; a pink glow starts to rise outside
    leo = pose({ x: 2.7, y: .72, z: -2.25, l: [[0, .1], [0, .1]], a: [[2.7, .35, .5], [2.7, .35, .5]], hp: -1.05 - .2 * ss(u, .2, .6), hy: .12 + .3 * ss(u, .3, .7) });
    leoRot = [Math.PI / 2, 0, 0]; leoF = { eyes: "wide", mouth: "o", brows: "high", noblink: true };
    const fl = u < .45 ? (Math.floor(u * 40) % 3 === 0 ? .3 : 1) : 0;
    RM.lamp.intensity *= fl; RM.key.intensity *= fl * .6; RM.fill.intensity *= .5; hemi.intensity *= .5; RM.bulb.visible = fl > .5;
    RM.fairy.forEach((b, i) => b.visible = u < .1 + (i % 7) * .07);
    RM.rim.intensity = 2.2 * ss(u, .35, .7); RM.rim.color.set(0xFF7AC0); RM.rim.position.set(-1.05, 1.2, -2.9);
    cam.p.set(.55, 1.85, 2.7); cam.l.set(2.4, .85, -1.0); cam.fov = 44; cam.focus = 3.6;
    dark = .15 * ss(u, .4, .8);
  } else if (sh === "rise") {     // 10. his silhouette rises in the window against the moon, wings spread; his eyes glint; he tucks to launch
    for (const b of RM.fairy) b.visible = false;
    const up2 = ease(ramp(u, 0, .55)), tuck = ss(u, .62, .95);
    cree = { x: -1.05, y: 1.05 + .8 * up2 + .03 * Math.sin(u * 7), z: -2.95, ry: 0, sc: .36, still: true, noblink: true, eyes: tuck > .3 ? "determined" : "open", look: [0, -.15],
      wl: [lerp(1.35, -.15, tuck), lerp(0, .7, tuck)], wr: [lerp(1.35, -.15, tuck), lerp(0, .7, tuck)], flap: [.28 * (1 - tuck), 2.4], sq: .16 * tuck, rx: -.12 * tuck, jaw: .2 };
    CREE.dark = true;
    FX.rays.visible = true; FX.rays.position.set(-1.05, cree.y + .15, -3.15); FX.rays.rotation.z = u * .25; FX.rays.children.forEach((r, i) => r.material.opacity = (.1 + .05 * Math.sin(u * 5 + i)) * ss(u, 0, .4));
    FX.halo.visible = true; FX.halo.position.set(-1.05, cree.y + .17, -3.05); FX.halo.scale.setScalar(.9 + .1 * Math.sin(u * 4)); FX.halo.material.opacity = .45 * ss(u, 0, .4);
    const gl = pulse(u, .5, .12);
    if (gl > .02) POST.push(() => { for (let k2 = 0; k2 < 2; k2++) { const sp = FX.sparks[k2]; CREE.eyes[k2].localToWorld(V.set(.03, .04, .16)); sp.visible = true; sp.position.copy(V); sp.scale.setScalar(.1 * gl); sp.material.opacity = gl; sp.material.rotation = u * 2; } });
    RM.bulb.visible = false; RM.lamp.intensity = 0; RM.key.intensity = 0; RM.fill.intensity = .3; hemi.intensity = .2; RM.moon.intensity = 2.6; RM.moon.position.set(-1.05, 2.2, -3.4);
    RM.rim.intensity = 3.0; RM.rim.color.set(0xBFD0FF); RM.rim.position.set(-1.05, 2.3, -3.3);
    cam.p.set(-1.6, 1.0 + .12 * u, .3 - .3 * ss(u, 0, len)); cam.l.set(-1.05, 1.75, -2.7); cam.fov = 40 - 4 * ss(u, 0, len); cam.focus = 3.3;
  } else if (sh === "burst") {    // 11. the window blows open (flash, glass glints) and he rockets through the room: a climb, a barrel roll, a turn
    const open = ease(ramp(u, 0, .12));
    RM.panes[0].rotation.y = -1.85 * open; RM.panes[1].rotation.y = 1.85 * open;
    RM.curt[0].rotation.x = -.5 * open * (1 - .2 * Math.sin(u * 9)); RM.curt[1].rotation.x = -.45 * open * (1 - .2 * Math.sin(u * 8 + 1));
    for (const b of RM.fairy) b.visible = false;
    flash = .55 * Math.exp(-u * 9) * (u > 0 ? 1 : 0);
    FX.shards.forEach((sh2, i) => { const a = u - .02 * hash(i); sh2.visible = a > 0 && a < .7; if (!sh2.visible) return;
      sh2.position.set(-1.05 + (hash(i) - .5) * 1.5 + (hash(i * 2) - .5) * a * 1.6, 1.8 + (hash(i * 3) - .5) * 1.2 + a * (hash(i * 4) - .3) * 1.4 - 1.6 * a * a, -2.3 + a * (1.2 + 2.2 * hash(i * 5)));
      sh2.rotation.set(a * 9 * hash(i * 6), a * 7, a * 5); sh2.material.opacity = .9 * (1 - a / .7) * (.5 + .5 * Math.sin(a * 40 + i)); });
    const k = ease(ramp(u, .02, 1.0) * .92 + ramp(u, .02, 1.0) * .08);
    cam.p.set(.95 + .25 * u, 1.15 + .1 * u, 2.55); cam.fov = 52; cam.focus = 2.6;
    cree = flyState(PATH.in, k, { sc: .3, eyes: "determined", flap: [.75, 6.5] });
    cree.roll += Math.PI * 2 * ss(k, .42, .62);
    const lk = PATH.in.getPointAt(clamp(k - .05)); cam.l.set(lerp(-1.05, lk.x, ss(u, .05, .3)), lerp(1.8, lk.y - .35, ss(u, .05, .3)), lerp(-2.3, lk.z, ss(u, .05, .3)));
    trail(PATH.in, k, .2, cam.p, .06);
    papers(Bs("hero") + 1.7, t, v(-.3, DESKY + .02, -.1), v(.35, .45, .5), 8);
    RM.bulb.visible = false; RM.lamp.intensity = 0; RM.key.intensity = 0; RM.moon.intensity = 4.0; RM.fill.intensity = .55; hemi.intensity = .3;
    RM.rim.intensity = .6; RM.rim.color.set(0xFF8CC6); RM.rim.position.set(cree.x, cree.y - .3, cree.z + .2);
  } else if (sh === "dive") {     // 12. at the top he swings upright facing us and hangs (slow motion, wings flared, eyes on the desk)... then drops
    for (const b of RM.fairy) b.visible = false;
    const hang = ramp(u, 0, .3), drop = ramp(u, .3, .45), flip = ease(ramp(u, 0, .14));
    const top = v(.25, 2.0, .38), y = lerp(top.y + .05 * Math.sin(hang * Math.PI), DESKY + .55, drop * drop);
    cree = { x: lerp(top.x, DESKC.x + .05, ease(drop)), y, z: lerp(top.z, DESKC.z, ease(drop)), ry: lerp(-.9, .1, flip), rx: lerp(1.0, .3, flip) + .1 * drop, roll: 0, sc: .32, still: true, noblink: true,
      eyes: "determined", look: [0, -.8], wl: [lerp(.9, 2.0, flip), lerp(.2, -.3, flip)], wr: [lerp(.9, 2.0, flip), lerp(.2, -.3, flip)], flap: [.22 * (1 - drop), 3], feetBack: 1 - flip, sq: -.14 * drop, jaw: .2 };
    FX.speed.visible = drop > 0; FX.speed.position.set(cree.x, cree.y + .35, cree.z); FX.speed.rotation.set(-Math.PI / 2, 0, 0);
    const pts = []; for (let j = 0; j <= 16; j++) { const q = j / 16; pts.push(v(lerp(top.x, cree.x, q), lerp(top.y + .2, cree.y + .08, q), lerp(top.z, cree.z, q))); }
    if (drop > 0) ribbon(pts, v(.1, 1.2, 1.75), .045);
    RM.bulb.visible = false; RM.lamp.intensity = 0; RM.key.intensity = .5; RM.moon.intensity = 3.6; RM.fill.intensity = .6; hemi.intensity = .32;
    RM.rim.intensity = .8; RM.rim.color.set(0xFF8CC6); RM.rim.position.set(cree.x, cree.y - .3, cree.z + .3);
    cam.p.set(.1, lerp(1.55, DESKY + .3, ss(u, .28, .45)), 1.75); cam.l.set(lerp(.24, .08, ss(u, .28, .45)), lerp(1.95, DESKY + .3, ss(u, .28, .45)), lerp(.38, .1, ss(u, .28, .45))); cam.fov = 42; cam.focus = 1.5;
  } else if (sh === "landing") {  // 13. the superhero landing: impact (flash, air blast, dust, shake), the lights come back in a wave; he rises proud
    const I = .13;                                                         // impact at Bs("hero") + 3.03, on the music's drop
    const fall = ramp(u, 0, I), crouch = u < I ? 0 : 1 - ss(u, .62, 1.0), rise = ss(u, .62, 1.0);
    const sqI = u > I ? .2 * Math.exp(-(u - I) * 8) * Math.cos((u - I) * 16) : -.14;
    cree = { x: DESKC.x + .05, y: lerp(DESKY + .55, DESKY, fall * fall), z: DESKC.z, ry: lerp(.1, -.08, rise), sc: .34, still: u < .9, noblink: u < .8,
      sq: u < I ? -.14 : sqI + .08 * crouch, rx: .42 * crouch - .1 * rise, roll: .05 * crouch,
      wl: [lerp(2.2, .5, rise), lerp(.75, .5, rise)], wr: [lerp(.15, .5, rise), lerp(-1.15, .5, rise)],
      eyes: u < .55 ? "determined" : (u < .95 ? "proud" : "joy"), look: [lerp(0, .25, rise), lerp(-.5, .25, rise)], jaw: u < .62 ? .2 : .2 + .5 * pulse(u, 1.0, .15), feetSplay: .25 * crouch };
    if (u > I) { const r = ramp(u, I, I + .6);
      FX.ring.visible = r < 1; FX.ring.position.set(DESKC.x + .05, DESKY + .005, DESKC.z); FX.ring.scale.setScalar(.05 + .75 * ease(r)); FX.ring.material.opacity = .75 * (1 - r);
      const rb = ramp(u, I, I + .35); FX.blast.visible = rb < 1; FX.blast.position.set(DESKC.x + .05, DESKY + .14, DESKC.z + .05); FX.blast.lookAt(cam.p); FX.blast.scale.setScalar(.06 + .9 * ease(rb)); FX.blast.material.opacity = .7 * (1 - rb);
      FX.dust.forEach((d, i) => { const a = i / FX.dust.length * 6.283, rr2 = .1 + .55 * ease(r) * (.7 + .3 * hash(i)); d.visible = r < 1; d.position.set(DESKC.x + .05 + Math.cos(a) * rr2, DESKY + .04 + .1 * r * hash(i * 3), DESKC.z + Math.sin(a) * rr2 * .6); d.scale.setScalar(.08 + .22 * r); d.material.opacity = .55 * (1 - r); });
      flash = .45 * Math.exp(-(u - I) * 14); }
    papers(Bs("hero") + 3.03, t, v(DESKC.x + .4, DESKY + .02, DESKC.z - .25), v(.6, .35, -.1), 6);
    // the lights come back in a wave: fairy lights left to right, then the lamp pops on
    const wave = ramp(u, .2, .55); RM.fairy.forEach((b, i) => b.visible = wave > i / RM.fairy.length);
    const lampOn = u > .42 ? 1 : 0; RM.bulb.visible = lampOn > 0; RM.lamp.intensity *= lampOn;
    RM.rim.intensity = 2.6; RM.rim.color.set(0xFF8CC6); RM.rim.position.set(DESKC.x, DESKY + .5, DESKC.z - .45); RM.rim2.intensity = 1.3; RM.rim2.position.set(DESKC.x + .4, DESKY + .3, DESKC.z + .3);
    if (u < I + .02) { RM.key.intensity = .2; hemi.intensity = .3; }
    const sh2 = u > I && u < .55 ? .022 * (1 - ramp(u, I, .55)) : 0;
    const orb = ss(u, .55, len);
    cam.p.set(.05 + .25 * orb + sh2 * Math.sin(u * 90), DESKY + .1 - .02 * orb + sh2 * Math.cos(u * 77), 2.15 - .45 * ss(u, .45, len)); cam.l.set(.06, DESKY + .2 + .04 * rise, DESKC.z); cam.fov = 34; cam.focus = 1.6;
    bloomS = .12 + .25 * Math.exp(-Math.max(0, u - I) * 6) * (u > I ? 1 : 0);
    const gl = pulse(u, 1.08, .09);
    if (gl > .02) POST.push(() => { CREE.eyes[1].localToWorld(V.set(.035, .045, .16)); FX.glint.visible = true; FX.glint.position.copy(V); FX.glint.scale.setScalar(.12 * gl); FX.glint.material.rotation = u * 1.5; FX.glint.material.opacity = gl; });
  } else if (sh === "whoa") {     // 9b. the creator turns: jaw drop
    const turn = ss(u, 0, .3);
    leo = pose({ x: 2.3, y: -.17, z: -1.0, ry: -Math.PI / 2 - .25 + .3 * turn, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.45, .55, .3], [.45, .55, .3]], lean: -.15 * turn, hp: -.1, hy: .35 * turn });
    leoF = { eyes: "wide", mouth: talking(t, "07") ? "wail" : "gasp", brows: "high", noblink: true };
    cam.p.set(.6, 1.62, .1); cam.l.set(2.3, 1.42, -1.0); cam.fov = 34 - 4 * ss(u, 0, len); cam.focus = 2.0;
  } else if (sh === "say") {      // 11. "Say no more."
    const hopS = Math.max(0, Math.sin(clamp((u - 1.05) / .32) * Math.PI)) * .05;
    cree = { x: DESKC.x, y: DESKY + hopS, z: DESKC.z, ry: .2, sc: .34, rx: -.08, eyes: u < 1.0 ? "proud" : "joy", wink: u > 1.0 && u < 1.45 ? 1 : 0,
      wl: [.45, .5], wr: [lerp(.45, 1.6, ss(u, .1, .3)) - .9 * ss(u, .95, 1.1), lerp(.5, -.9, ss(u, .1, .3))], jaw: creeJaw(t), look: [.4, .15], sq: hopS > 0 ? -.06 : .05 * pulse(u, .55, .1) };
    RM.rim.intensity = 2.0; RM.rim.position.set(DESKC.x, DESKY + .45, DESKC.z - .45);
    cam.p.set(-.4, DESKY + .42, 2.25); cam.l.set(DESKC.x, DESKY + .22, DESKC.z); cam.fov = 30; cam.focus = 2.25;
  } else if (sh === "fix1") {     // 12. the film strip: he walks it with his magnifier, taps second three
    FX.strip.visible = true;
    const walkU = ramp(u, .2, 1.6), x = lerp(.42, -.28, sm(walkU));
    const tap = ss(u, 1.65, 1.85) * (1 - ss(u, 2.3, 2.6));
    cree = { x, y: DESKY, z: .2, ry: -.35 + .35 * ss(u, 1.5, 1.7), sc: .3, eyes: tap > .5 ? (u > 2.1 ? "joy" : "wide") : (walkU > 0 && walkU < 1 ? "focus" : "curious"), wl: [.15 + 2.2 * tap, .3 * tap], wr: [1.9, .5], jaw: creeJaw(t), look: [-.3, .9], mag: "hand", magRz: .2, step: walkU > 0 && walkU < 1 ? Math.sin(u * 14) : 0, roll: walkU > 0 && walkU < 1 ? .08 * Math.sin(u * 14) : 0 };
    for (let i = 0; i < FX.frames.length; i++) { const f = FX.frames[i], hot = i === 1 ? ss(u, 1.8, 2.0) : 0; f.position.y = DESKY + .42 + .012 * Math.sin(u * 2 + i); f.edge.material.color.set(hot > 0 ? 0xFF6A5A : 0xFFFFFF); f.scale.setScalar(1 + .2 * hot); }
    leo = standing({ x: -.35, z: -.8, ry: .1, lean: .3, hp: .22, hy: -.12, a: [[.5, .15, .9], [.5, .15, .9]] });
    leoF = { eyes: "wide", mouth: talking(t, "08") ? "o" : "o", brows: "high", talk: talking(t, "08") };
    cam.p.set(-.08, 1.36, 2.6 - .2 * ss(u, 0, len)); cam.l.set(-.12, 1.15, -.1); cam.fov = 40; cam.focus = 2.6;
  } else if (sh === "fix2") {     // 13. the reel cards: one glows gold
    FX.cards.visible = true;
    for (let i = 0; i < 5; i++) {
      const c = FX.cardL[i], a = (i - 2) * .42 * ss(u, .1, .7), flip = ss(u, .5 + i * .18, .75 + i * .18);
      c.position.set(DESKC.x + Math.sin(a) * .36, DESKY + .42 + Math.cos(a) * .1 - .08, DESKC.z - .12); c.rotation.set(0, Math.PI * (1 - flip) + a * -.3, -a * .5);
      const gold = i === 3 ? ss(u, 1.5, 1.8) : 0; c.cmat.emissiveIntensity = .5 * gold; c.scale.setScalar(1 + .2 * gold);
    }
    const hop2 = u > 1.6 ? Math.max(0, Math.sin((u - 1.6) * 10)) * .045 * (1 - ss(u, 2.2, 2.5)) : 0;
    cree = { x: DESKC.x, y: DESKY + hop2, z: DESKC.z + .05, ry: 0, sc: .3, eyes: u > 1.6 ? "happy" : "joy", wl: [.4 + (u > 1.6 ? 1.8 : 0), 0], wr: [1.2 + .9 * Math.sin(u * 4) * (u < 1.6 ? 1 : 0) + (u > 1.6 ? 1.0 : 0), .3], flap: u > 1.6 ? [.25, 5] : null, jaw: creeJaw(t), look: [0, .8], sq: hop2 > 0 ? -.06 : 0 };
    leo = standing({ x: -.45, z: -.8, ry: .2, lean: .15, hp: .1, a: [[.3, .12, .3], [1.55 * ss(t, Ls("09") - .3, Ls("09")), .05, .1]] });
    leoF = { eyes: "wide", mouth: talking(t, "09") ? "laugh" : "o", brows: "high", talk: talking(t, "09") };
    cam.p.set(-.55, 1.42, 2.3); cam.l.set(.0, 1.15, -.1); cam.fov = 40; cam.focus = 2.35;
  } else if (sh === "fix3") {     // 14. the DM machine: he pulls the lever, paper planes stream out of the phone
    FX.mach.visible = true;
    const pull = ss(u, .7, .95);
    FX.lever.rotation.z = .5 - 1.1 * pull; FX.machLight.material.color.set(pull > .5 ? 0x5BE3B0 : 0x3A3A3A);
    const cheer = ss(u, 1.3, 1.5); const hop3 = cheer * Math.max(0, Math.sin((u - 1.3) * 9)) * .04;
    cree = { x: DESKC.x + .05, y: DESKY + hop3, z: .2, ry: .6 - .4 * cheer, sc: .3, eyes: cheer > .3 ? "happy" : (u < .95 ? "determined" : "joy"), flap: cheer > .3 ? [.3, 6] : null, wl: [lerp(.3, 2.6, cheer), 0], wr: [lerp(1.4 - .5 * pull, 2.6, cheer), lerp(.6 + .4 * pull, 0, cheer)], jaw: creeJaw(t), look: [.6, .2], sq: .05 * Math.sin(u * 9) * (1 - pull) };
    RM.triScr.color.set(0xFFFFFF);
    for (let i = 0; i < FX.planes.length; i++) {
      const p = FX.planes[i], a = u - .95 - i * .13; p.visible = a > 0 && a < 1.6;
      if (!p.visible) continue;
      const k = a / 1.6, o = v(.25, DESKY + .2, .05);
      p.position.set(o.x - .35 * k + .25 * Math.sin(i * 1.7) * k, o.y + .5 * k + .1 * Math.sin(k * 6 + i), o.z + 1.6 * k * (.7 + .3 * hash(i)));
      p.lookAt(p.position.x - .35, p.position.y + .4, p.position.z + 1.6); p.scale.setScalar(1.5);
    }
    leo = standing({ x: -.4, z: -.8, ry: .1, lean: -.05, hp: -.1, a: u > 1.1 ? [[2.6, .75, 2.2], [2.6, .75, 2.2]] : [[.4, .4, .4], [.4, .4, .4]] });
    leoF = { eyes: u > 1.1 ? "happy" : "wide", mouth: u > 1.1 ? "laugh" : "gasp", brows: "high", noblink: true };
    cam.p.set(.85, 1.36, 2.3); cam.l.set(.1, 1.1, -.2); cam.fov = 42; cam.focus = 2.3;
  } else if (sh === "hug") {      // 15. he scoops Cree up: happy tears; Cree pats his head
    leo = standing({ x: -.1, z: .8, ry: .15, lean: .08, hp: .2, hr: .18, a: [[1.0, -.2, 1.95], [1.0, -.2, 1.95]] });
    leoF = { eyes: "sob", mouth: talking(t, "10") ? "laugh" : "grin", brows: "worry", talk: talking(t, "10") };
    cree = { x: 0, y: 0, z: 0, ry: -.3, sc: .34, eyes: talking(t, "10") || u < .6 ? "happy" : "soft", blush: .7, wl: [.4, .2], wr: [2.7, .3 + .35 * Math.sin(u * 9)], jaw: creeJaw(t), noblink: true, attach: true, roll: .12 * Math.sin(u * 2.2) };
    cam.p.set(.3, 1.6, 3.4); cam.l.set(-.05, 1.42, .8); cam.fov = 36; cam.focus = 2.65;
  } else if (sh === "end") {      // 16. end card plate: Cree alone in a soft pink space, pointing up at the wordmark
    RM.visible = false; for (const b of RM.fairy) b.visible = false;
    scene.background = tmpC.set(0x3A1430).clone();
    const hop = Math.max(0, Math.sin(clamp((u - 1.2) / .45) * Math.PI)) * .06;
    cree = { x: 0, y: hop, z: 0, ry: -.15, sc: .34, eyes: u > 1.5 ? "happy" : "joy", wl: [.3, 0], wr: [2.75 + .25 * Math.sin(u * 8) * (u < 1.2 ? 1 : 0), -.25], jaw: creeJaw(t), look: [.3, .9], sq: hop > 0 ? -.05 : .04 * pulse(u, 1.67, .08) };
    hemi.color.set(0xFFC8E4); hemi.groundColor.set(0x6A2050); hemi.intensity = .55; sun.intensity = .75; sun.color.set(0xFFF0F6); sun.position.set(1.5, 4, 3); sun.target.position.set(0, 0, 0);
    RM.lamp.intensity = 0; RM.moon.intensity = 0; RM.fill.intensity = 0; RM.key.intensity = 0; RM.rim.intensity = 3; RM.rim.position.set(0, .45, -.4);
    cam.p.set(0, .34, 2.1); cam.l.set(0, .5, 0); cam.fov = 32; cam.focus = 2.1;
  }

  if (leo) { placeToy(LEO, true, idle(leo, t, LEO.seed), leoF); if (leoRot) LEO.root.rotation.set(...leoRot); else LEO.root.rotation.x = LEO.root.rotation.z = 0; }
  else placeToy(LEO, false);
  LEO.root.updateMatrixWorld(true);
  if (cree && cree.attach) { LEO.torso.localToWorld(V.set(0, .32, .3)); cree.x = V.x; cree.y = V.y - .02; cree.z = V.z; }
  if (window.CREE_TEST) cree = { ...(cree || {}), ...window.CREE_TEST };     // portrait tests only (never set in the video)
  placeCree(!!cree, cree || {});
  for (const f of POST) f();
  if (LEO.phone.visible) { LEO.phone.getWorldPosition(V); phoneL.position.copy(V).add(V2.set(0, .05, .25)); }
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
  gu.uTime.value = t; gu.uWarm.value = .05; gu.uCool.value = 0; gu.uSat.value = 1.04; gu.uCon.value = .04; gu.uVig.value = r.vig; gu.uTint.value = 0;
  gu.uFlash.value = r.flash || 0; gu.uCA.value = 0; gu.uKeep.value = 0; gu.uGrain.value = 0; gu.uTop.value = 0; gu.uDark.value = r.dark;
  bloom.strength = r.bloomS;
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 30 }); sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures (no words anywhere in the 3D world; words live in the HTML layer)
const text = (w, h, draw) => pix(w, h, draw, false);
function buildTextures() {
  TEX.sky = text(1024, 768, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#0B1440"); gr.addColorStop(.6, "#1D2C6E"); gr.addColorStop(1, "#33407E"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 220; i++) { const x = hash(i * 3.1) * w, y = hash(i * 7.7) * h * .85, r = hash(i * 1.9) * 1.8 + .5; g.fillStyle = `rgba(255,250,240,${.35 + hash(i) * .65})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
    const mx = 640, my = 220; const mg = g.createRadialGradient(mx, my, 20, mx, my, 110); mg.addColorStop(0, "rgba(255,248,230,.35)"); mg.addColorStop(1, "rgba(255,248,230,0)"); g.fillStyle = mg; g.fillRect(mx - 120, my - 120, 240, 240);
    g.fillStyle = "#FFF6E2"; g.beginPath(); g.arc(mx, my, 46, 0, 7); g.fill(); g.fillStyle = "#1D2C6E"; g.beginPath(); g.arc(mx + 20, my - 12, 42, 0, 7); g.fill();
  });
  for (let k = 0; k < 3; k++) TEX["cloud" + k] = text(512, 160, (g, w, h) => { g.clearRect(0, 0, w, h); for (let i = 0; i < 9; i++) { const x = 60 + i * 48 + hash(i + k * 9) * 30, y = 90 + Math.sin(i) * 14, r = 34 + hash(i * 3 + k) * 26; const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, "rgba(120,130,190,.55)"); gr.addColorStop(1, "rgba(120,130,190,0)"); g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); } });
  TEX.posters = text(600, 440, (g, w, h) => {
    g.clearRect(0, 0, w, h); g.fillStyle = "#C9BBDD"; g.fillRect(0, 0, w, h);
    const art = (x, y, ww, hh, c1, c2, k) => { g.fillStyle = "#FFFFFF"; g.fillRect(x - 8, y - 8, ww + 16, hh + 16); const gr = g.createLinearGradient(x, y, x + ww, y + hh); gr.addColorStop(0, c1); gr.addColorStop(1, c2); g.fillStyle = gr; g.fillRect(x, y, ww, hh);
      g.fillStyle = "rgba(255,255,255,.7)"; if (k === 0) { g.beginPath(); g.arc(x + ww / 2, y + hh * .45, ww * .26, 0, 7); g.fill(); } else if (k === 1) { g.beginPath(); g.moveTo(x + ww * .2, y + hh * .8); g.lineTo(x + ww * .5, y + hh * .3); g.lineTo(x + ww * .8, y + hh * .8); g.fill(); } else { for (let i = 0; i < 4; i++) g.fillRect(x + ww * .2 + i * ww * .16, y + hh * (.75 - i * .12), ww * .1, hh * (.1 + i * .12)); } };
    art(30, 40, 170, 230, "#2A1E5A", "#E8577E", 0); art(240, 70, 130, 170, "#F2C94C", "#F38BA0", 1); art(410, 30, 150, 220, "#5B7FC4", "#B79CFF", 2); art(260, 280, 110, 120, "#7FC8A9", "#3E7CB1", 0);
  });
  for (let k = 0; k < 4; k++) TEX["thumb" + k] = text(160, 260, (g, w, h) => {
    const P = [["#F343A2", "#FF9A6A"], ["#7A5CFF", "#FF8CC6"], ["#F2C94C", "#E8735A"], ["#3EC6C0", "#7A5CFF"]][k];
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, P[0]); gr.addColorStop(1, P[1]); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,.88)"; g.beginPath(); g.arc(w / 2, h * .42, 30, 0, 7); g.fill();
    g.fillStyle = P[0]; g.beginPath(); g.moveTo(w / 2 - 9, h * .42 - 15); g.lineTo(w / 2 - 9, h * .42 + 15); g.lineTo(w / 2 + 15, h * .42); g.fill();
    g.fillStyle = "rgba(255,255,255,.7)"; rr(g, 16, h - 50, w - 32, 12, 6); g.fill(); rr(g, 16, h - 30, w * .5, 12, 6); g.fill();
  });
  TEX.knit = text(256, 256, (g, w, h) => { g.fillStyle = "#E9A0B8"; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 16) for (let x = 0; x < w; x += 16) { g.fillStyle = (x / 16 + y / 16) % 2 ? "#E393AE" : "#EEADC2"; g.beginPath(); g.ellipse(x + 4, y + 8, 4, 7, -.5, 0, 7); g.fill(); g.beginPath(); g.ellipse(x + 12, y + 8, 4, 7, .5, 0, 7); g.fill(); } });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; if (key === "knit") { m.map.wrapS = m.map.wrapT = THREE.RepeatWrapping; m.map.repeat.set(3, 3); } m.needsUpdate = true; } }
  TEX.ready = true;
}

const ready = (async () => {
  buildTextures();
  scene.traverse((o) => { if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  RM.visible = true;
  renderer.compile(scene, camera);
  renderAt(window.CR_COVER ? window.CR_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["cree"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.CR_COVER ? window.CR_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C };
