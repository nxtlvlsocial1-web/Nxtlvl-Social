// Creedom "I Wish..." reel: a stressed creator in his bedroom studio at night makes three wishes, and Cree, Creedom's pink
// mascot, answers each one, half revealed, then in a full hero entrance. Fourteen shots with hard cuts; everything is a
// pure function of time t, drawn on hf-seek. The speech clouds, tags, captions and end card live in the HTML layer.
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
      c *= 1. + .025 * sin(uTime * 23.) * sin(uTime * 7.1);        // a faint projector flicker
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

// ================================================================= THE BEDROOM STUDIO (one room at night)
// The desk faces the camera side (+z) with the creator's chair behind it (z = -.7). Back wall z = -2.3 with the window
// (left) and fairy lights; the bed in the back-right corner; a doorway in the left wall onto a dark hall.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const RM = mkSet("room");
const SEAT = v3(-.15, 0, -.7), SITY = .52 - .71;
const DESKY = .8;
{
  const plank = pix(64, 64, (g) => { px(g, "#7A5238", 0, 0, 64, 64); for (let j = 0; j < 8; j++) { px(g, j % 2 ? "#71492F" : "#83583C", 0, j * 8, 64, 8); px(g, "#5A3A26", 0, j * 8, 64, 1); px(g, "#5A3A26", (j * 23) % 64, j * 8, 1, 8); } }, false);
  flat(9, 8, new THREE.MeshStandardMaterial({ map: rep(plank, 5, 4), roughness: .55 }), 0, 0, 0);
  const wallM = mat(0x6E5A86), trim = mat(0x3A2C4A);
  box(9, 3.2, .2, wallM, 0, 1.6, -2.4);
  // left wall with a doorway (1 m wide, 2.1 m tall) at z = -1.0
  box(.2, 3.2, 2.9, wallM, -3.4, 1.6, 1.95); box(.2, 3.2, 1.0, wallM, -3.4, 1.6, -2.0); box(.2, 1.1, 1.0, wallM, -3.4, 2.65, -1.0);
  box(.24, 2.12, .08, trim, -3.36, 1.06, -1.52); box(.24, 2.12, .08, trim, -3.36, 1.06, -.48); box(.24, .08, 1.12, trim, -3.36, 2.12, -1.0);
  box(.2, 3.2, 8, wallM, 3.5, 1.6, 1.5);
  box(9, .12, 8, mat(0x4A3A5C), 0, 3.2, 1.5, { cast: false });
  box(9, .1, .05, trim, 0, .05, -2.29);
  // the hall behind the doorway: dark, with a pink glow far down it
  RM.hall = new THREE.Group(); RM.add(RM.hall);
  box(3, .05, 1.2, mat(0x2A2236), -4.9, .0, -1.0, { parent: RM.hall }); box(3, 2.4, .1, mat(0x2A2236), -4.9, 1.2, -1.6, { parent: RM.hall }); box(3, 2.4, .1, mat(0x2A2236), -4.9, 1.2, -.4, { parent: RM.hall });
  box(.1, 2.4, 1.2, mat(0x2A2236), -6.3, 1.2, -1.0, { parent: RM.hall });
  // window onto the night (back wall, left), with a sill
  box(1.5, 1.4, .06, trim, -1.55, 1.75, -2.28); RM.winM = texMat("night", { transparent: false }); plane(1.36, 1.26, RM.winM, -1.55, 1.75, -2.24, 0);
  box(.04, 1.26, .04, trim, -1.55, 1.75, -2.22); box(1.36, .04, .04, trim, -1.55, 1.75, -2.22); box(1.6, .06, .2, trim, -1.55, 1.02, -2.2);
  // fairy lights along the back wall, sagging between pins
  RM.fairy = [];
  const FC = [0xFFD27A, 0xFF8CC6, 0xFFE9B0, 0xF9A8D4];
  for (let i = 0; i < 46; i++) { const x = -3.2 + i * .1; const sag = .12 * Math.sin((i % 10) / 10 * Math.PI); const b = new THREE.Mesh(new THREE.SphereGeometry(.022, 8, 6), glow(FC[i % 4])); b.position.set(x, 2.55 - sag, -2.27); RM.add(b); RM.fairy.push(b); }
  // posters and a shelf
  RM.posterM = texMat("posters", { transparent: false }); plane(1.0, .7, RM.posterM, .45, 2.0, -2.28, 0);
  box(1.0, .04, .25, trim, .45, 1.45, -2.2); for (let k = 0; k < 4; k++) box(.1, .26, .18, mat(["#F343A2", "#F2C94C", "#5B7FC4", "#E8735A"][k]), .05 + k * .14, 1.6, -2.2);
  cyl(.07, .06, .12, mat(0xE8735A), .82, 1.53, -2.2, 12); for (let j = 0; j < 3; j++) box(.12 - j * .02, .12, .12 - j * .02, mat(0x5E9C52), .82, 1.65 + j * .09, -2.2);
  // the desk (laptop closed, a lamp, a mug, a plant, the phone on a mini tripod) and the chair
  box(1.9, .07, .9, mat(0x5A3E2A, { roughness: .4 }), 0, DESKY - .035, 0); for (const s of [-1, 1]) box(.07, .73, .8, mat(0x3E2A1E), s * .9, .37, 0);
  box(1.8, .55, .05, mat(0x3E2A1E), 0, .45, .42);
  box(.42, .03, .3, metal(0x9C9CA6, .35), -.35, DESKY + .015, -.05);
  RM.lampShade = mat(0xFFB8DA, { emissive: 0xFFB8DA, emissiveIntensity: .8, roughness: .4 });
  cyl(.08, .1, .03, metal(0x2A2A2E, .4), -.78, DESKY + .015, -.2, 14); cyl(.012, .012, .34, metal(0x2A2A2E, .4), -.78, DESKY + .19, -.2, 8); cyl(.07, .15, .14, RM.lampShade, -.78, DESKY + .38, -.15, 16);
  cyl(.045, .04, .1, mat(0xF4EFE6), .78, DESKY + .05, .2, 12);
  cyl(.06, .05, .09, mat(0xC9644E), .8, DESKY + .045, -.25, 10); box(.13, .15, .13, mat(0x4E8C48), .8, DESKY + .17, -.25);
  // the phone on its mini tripod (screen faces the chair)
  RM.tri = new THREE.Group(); RM.tri.position.set(.55, DESKY, -.05); RM.add(RM.tri);
  for (let k = 0; k < 3; k++) { const l = cyl(.006, .006, .16, metal(0x2A2A2E, .4), Math.sin(k * 2.1) * .04, .07, Math.cos(k * 2.1) * .04, 6, { parent: RM.tri }); l.rotation.set(Math.cos(k * 2.1) * .35, 0, -Math.sin(k * 2.1) * .35); }
  box(.09, .17, .012, mat(0x16141A, { roughness: .3 }), 0, .23, 0, { parent: RM.tri });
  RM.triScr = new THREE.MeshBasicMaterial({ color: 0xFFE3F1, toneMapped: false }); const ts = new THREE.Mesh(new THREE.PlaneGeometry(.08, .155), RM.triScr); ts.position.set(0, .23, -.007); ts.rotation.y = Math.PI; RM.tri.add(ts);
  box(.55, .08, .5, mat(0x2A2236), SEAT.x, .5, SEAT.z - .05); box(.55, .7, .1, mat(0x2A2236), SEAT.x, .9, SEAT.z - .32);
  // ring light on a stand, front-left of the desk, facing the chair
  RM.ring = new THREE.Group(); RM.ring.position.set(-1.25, 0, .55); RM.ring.rotation.y = -.75; RM.add(RM.ring);
  cyl(.012, .012, 1.45, metal(0x2A2A2E, .4), 0, .72, 0, 8, { parent: RM.ring }); for (let k = 0; k < 3; k++) { const l = cyl(.01, .01, .45, metal(0x2A2A2E, .4), Math.sin(k * 2.1) * .14, .17, Math.cos(k * 2.1) * .14, 6, { parent: RM.ring }); l.rotation.set(Math.cos(k * 2.1) * .7, 0, -Math.sin(k * 2.1) * .7); }
  RM.ringM = new THREE.MeshBasicMaterial({ color: 0xFFF1E6, toneMapped: false });
  const rg = new THREE.Mesh(new THREE.TorusGeometry(.22, .025, 10, 48), RM.ringM); rg.position.y = 1.55; RM.ring.add(rg);
  // the bed (back-right corner), pillow, blanket, a plant, a rug
  box(1.4, .32, 2.1, mat(0x3A2C4A), 2.7, .16, -1.25); box(1.36, .2, 2.04, mat(0xF4ECF4, { roughness: .9 }), 2.7, .42, -1.25);
  box(1.4, .9, .1, mat(0x3A2C4A), 2.7, .45, -2.3);
  box(.8, .14, .42, mat(0xFFF6FA, { roughness: .95 }), 2.7, .6, -1.98, { round: .06 }); box(.7, .14, .4, mat(0xFFE3F1, { roughness: .95 }), 2.7, .69, -.42, { round: .06 });
  box(1.38, .12, 1.25, mat(0xD9468F, { roughness: .95 }), 2.7, .56, -.8, { round: .05 });
  RM.bedPhone = new THREE.Group(); RM.bedPhone.position.set(2.25, .63, -1.35); RM.add(RM.bedPhone); box(.09, .012, .17, mat(0x16141A, { roughness: .3 }), 0, 0, 0, { parent: RM.bedPhone });
  RM.bedScr = new THREE.MeshBasicMaterial({ color: 0xFFE3F1, toneMapped: false }); const bs = new THREE.Mesh(new THREE.PlaneGeometry(.08, .155), RM.bedScr); bs.rotation.x = -Math.PI / 2; bs.position.y = .007; RM.bedPhone.add(bs);
  cyl(.22, .18, .4, mat(0xE8735A), -2.9, .2, -1.9, 12); for (let j = 0; j < 4; j++) box(.38 - j * .06, .34, .38 - j * .06, mat(j % 2 ? 0x4E7A3E : 0x5E8C48), -2.9, .55 + j * .3, -1.9);
  flat(3.2, 2.4, mat(0xB84A86, { roughness: .95 }), .3, .005, .2);
  // crumpled paper balls around the bin
  cyl(.15, .12, .32, mat(0x2A2236), 1.25, .16, -.5, 14); for (let k = 0; k < 6; k++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(.05, 0), mat(0xF4F1EA)); b.position.set(1.0 + hash(k) * .5, .045, -.2 + hash(k * 3) * .5); b.rotation.set(k, k * 2, k * 3); add(b); }
  RM.key = new THREE.PointLight(0xFFE7F0, 0, 6, 1.5); RM.key.position.set(-1.1, 1.6, .4); scene.add(RM.key);      // the ring light
  RM.fill = new THREE.PointLight(0xB89CFF, 0, 9, 1.4); RM.fill.position.set(1.2, 2.6, 2.4); scene.add(RM.fill);
  RM.lamp = new THREE.PointLight(0xFFB8DA, 0, 3, 1.8); RM.lamp.position.set(-.78, 1.3, -.1); scene.add(RM.lamp);
  RM.moon = new THREE.PointLight(0x9CC4FF, 0, 4, 1.6); RM.moon.position.set(-1.55, 1.8, -1.6); scene.add(RM.moon);
  RM.hallL = new THREE.PointLight(0xFF4FAE, 0, 4, 1.4); RM.hallL.position.set(-5.4, .7, -1.0); scene.add(RM.hallL);
  RM.hero = new THREE.PointLight(0xFFB0D8, 0, 4, 1.5); scene.add(RM.hero);
  RM.gold = new THREE.PointLight(0xFFD27A, 0, 3, 1.6); scene.add(RM.gold);
}
// ---------------------------------------------------------------- the reel-world props: a glowing film strip, reel cards, the DM machine, paper planes
const glowTex = (inner, outer) => pix(128, 128, (g) => { const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, inner); gr.addColorStop(.35, outer); gr.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }, false);
const addM = (tx, c = 0xffffff) => new THREE.MeshBasicMaterial({ map: tx, color: c, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false });
const FX = {};
{
  // the film strip: 8 frames floating over the desk in an arc
  FX.strip = new THREE.Group(); RM.add(FX.strip);
  FX.frames = [];
  for (let i = 0; i < 8; i++) {
    const f = new THREE.Group(); f.position.set(-.85 + i * .24, DESKY + .42, -.12 - .1 * Math.sin(i / 7 * Math.PI)); f.rotation.y = (3.5 - i) * .05; FX.strip.add(f);
    const fm = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .92, toneMapped: false }); LATE.push([fm, "thumb" + (i % 4)]);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.18, .3), fm); f.add(p);
    const edge = new THREE.Mesh(new THREE.PlaneGeometry(.21, .33), new THREE.MeshBasicMaterial({ color: 0xFFC7E3, transparent: true, opacity: .55, toneMapped: false })); edge.position.z = -.002; f.add(edge);
    f.edge = edge; f.pm = fm; FX.frames.push(f);
  }
  FX.track = new THREE.Mesh(new THREE.PlaneGeometry(2.0, .012), new THREE.MeshBasicMaterial({ color: 0xFF8CC6, toneMapped: false })); FX.track.position.set(0, DESKY + .22, -.16); FX.strip.add(FX.track);
  // reel cards: frosted glass, fanned out
  FX.cards = new THREE.Group(); RM.add(FX.cards); FX.cardL = [];
  for (let i = 0; i < 5; i++) {
    const c = new THREE.Group(); FX.cards.add(c);
    const cmat = new THREE.MeshPhysicalMaterial({ color: i === 3 ? 0xFFE7A8 : 0xFFE3F1, roughness: .25, transparent: true, opacity: .82, emissive: i === 3 ? 0xFFC24A : 0xFF8CC6, emissiveIntensity: i === 3 ? .9 : .25, side: THREE.DoubleSide });
    const m = new THREE.Mesh(new RoundedBoxGeometry(.2, .32, .01, 2, .02), cmat); c.add(m);
    const im = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .9, toneMapped: false }); LATE.push([im, "thumb" + ((i + 1) % 4)]);
    const ip = new THREE.Mesh(new THREE.PlaneGeometry(.16, .22), im); ip.position.set(0, .03, .007); c.add(ip);
    c.cmat = cmat; FX.cardL.push(c);
  }
  // the DM machine: a small pink box with a lever and a slot
  FX.mach = new THREE.Group(); FX.mach.position.set(.3, DESKY, .15); RM.add(FX.mach);
  box(.26, .16, .18, gloss(0xF06BB4), 0, .08, 0, { parent: FX.mach, round: .03 }); box(.14, .02, .02, mat(0x3A1A2E), 0, .12, .091, { parent: FX.mach });
  const piv = new THREE.Group(); piv.position.set(.135, .1, 0); FX.mach.add(piv); FX.lever = piv;
  cyl(.008, .008, .16, metal(0xD9D9DE, .3), 0, .08, 0, 8, { parent: piv }); const kn = new THREE.Mesh(new THREE.SphereGeometry(.025, 14, 10), gloss(0xF2C94C)); kn.position.y = .17; piv.add(kn);
  FX.machLight = new THREE.Mesh(new THREE.SphereGeometry(.015, 10, 8), glow(0x5BE3B0)); FX.machLight.position.set(-.08, .17, .05); FX.mach.add(FX.machLight);
  // paper planes
  FX.planes = [];
  const pg = new THREE.BufferGeometry(); pg.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, .07, -.045, 0, -.04, 0, .006, -.03, 0, 0, .07, .045, 0, -.04, 0, .006, -.03, 0, 0, .07, 0, -.02, -.035, 0, .006, -.03], 3)); pg.computeVertexNormals();
  for (let i = 0; i < 12; i++) { const p = new THREE.Mesh(pg, new THREE.MeshBasicMaterial({ color: i % 3 ? 0xFFF4FA : 0xFFD6EC, side: THREE.DoubleSide, toneMapped: false })); RM.add(p); FX.planes.push(p); }
  // light: glow sprites and god rays for the hero entrance and the end card; dust motes
  FX.glow = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), addM(glowTex("rgba(255,214,236,1)", "rgba(243,67,162,.55)"))); scene.add(FX.glow);
  FX.glow2 = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), addM(glowTex("rgba(255,236,190,1)", "rgba(255,190,90,.4)"))); scene.add(FX.glow2);
  const rayT = pix(64, 256, (g) => { const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "rgba(255,220,240,0)"); gr.addColorStop(.25, "rgba(255,200,230,.7)"); gr.addColorStop(1, "rgba(255,200,230,0)"); g.fillStyle = gr; g.beginPath(); g.moveTo(26, 256); g.lineTo(38, 256); g.lineTo(64, 0); g.lineTo(0, 0); g.fill(); }, false);
  FX.rays = new THREE.Group(); scene.add(FX.rays);
  for (let i = 0; i < 9; i++) { const r = new THREE.Mesh(new THREE.PlaneGeometry(.5, 2.4), addM(rayT)); r.geometry.translate(0, 1.2, 0); r.rotation.z = (i - 4) * .33; r.ray = i; FX.rays.add(r); }
  const dg = new THREE.BufferGeometry(); const dp = [];
  for (let i = 0; i < 220; i++) dp.push(hash(i * 1.3) - .5, hash(i * 2.7), hash(i * 4.1) - .5);
  dg.setAttribute("position", new THREE.Float32BufferAttribute(dp, 3));
  FX.dust = new THREE.Points(dg, new THREE.PointsMaterial({ size: .012, map: glowTex("rgba(255,255,255,1)", "rgba(255,170,215,.6)"), color: 0xFFC2E2, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); scene.add(FX.dust);
  FX.base = dp;
  // the doorway glow (reveal 1)
  FX.door = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), addM(glowTex("rgba(255,120,200,1)", "rgba(243,67,162,.5)"))); scene.add(FX.door);
}
PARENT = scene;

// ---------------------------------------------------------------- Cree: Creedom's mascot, a soft magenta plush egg (to the character sheet)
// Built at 1 unit tall; CREE.root is scaled to his size in the room. Pivots: bod (squash), eyes, brows, beak, wings, feet.
const CREE = { root: new THREE.Group() };
scene.add(CREE.root);
{
  const R = CREE.root;
  const plush = new THREE.MeshPhysicalMaterial({ color: 0xF343A2, roughness: .62, sheen: 1, sheenColor: new THREE.Color(0xFF8CC6), sheenRoughness: .35, envMap: ENV, envMapIntensity: .35 });
  CREE.plush = plush;
  const bod = new THREE.Group(); R.add(bod); CREE.bod = bod;
  const g = new THREE.SphereGeometry(.5, 72, 54); const pa = g.attributes.position;
  for (let i = 0; i < pa.count; i++) { const y = pa.getY(i); const w = 1 + .12 * (-y / .5) - .04 * Math.max(0, y / .5) ** 2; pa.setX(i, pa.getX(i) * w); pa.setZ(i, pa.getZ(i) * w * .96); pa.setY(i, y * 1.02); }
  g.computeVertexNormals();
  const body = new THREE.Mesh(g, plush); body.position.y = .52; body.castShadow = true; body.receiveShadow = true; bod.add(body);
  // eyes: glossy white, big black pupils, two catchlights; a soft pink rim around each
  const sclM = CREE.sclM = new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, roughness: .15, clearcoat: 1, clearcoatRoughness: .05, envMap: ENV, envMapIntensity: .5 });
  const pupM = CREE.pupM = new THREE.MeshPhysicalMaterial({ color: 0x0B0B10, roughness: .08, clearcoat: 1, clearcoatRoughness: .03, envMap: ENV, envMapIntensity: .9 });
  const catM = new THREE.MeshBasicMaterial({ color: 0xFFFFFF, toneMapped: false });
  const rimM = CREE.rimM = new THREE.MeshStandardMaterial({ color: 0xFFC2DE, roughness: .6 });
  CREE.eyes = []; CREE.pupils = []; CREE.cats = [];
  for (const s of [-1, 1]) {
    const eg = new THREE.Group(); eg.position.set(s * .175, .62, .395); eg.rotation.y = s * .32; bod.add(eg);
    const rim = new THREE.Mesh(new THREE.SphereGeometry(.165, 32, 24), rimM); rim.scale.set(1, 1.1, .45); eg.add(rim);
    const scl = new THREE.Mesh(new THREE.SphereGeometry(.15, 32, 24), sclM); scl.scale.set(1, 1.1, .55); scl.position.z = .015; eg.add(scl);
    const pg = new THREE.Group(); pg.position.z = .06; eg.add(pg);
    const pup = new THREE.Mesh(new THREE.SphereGeometry(.105, 28, 20), pupM); pup.scale.set(1, 1.08, .5); pg.add(pup);
    const c1 = new THREE.Mesh(new THREE.SphereGeometry(.03, 12, 10), catM); c1.position.set(.035, .045, .05); c1.scale.z = .4; pg.add(c1);
    const c2 = new THREE.Mesh(new THREE.SphereGeometry(.014, 10, 8), catM); c2.position.set(-.035, -.04, .05); c2.scale.z = .4; pg.add(c2);
    const arc = new THREE.Mesh(new THREE.TorusGeometry(.085, .022, 10, 28, Math.PI), new THREE.MeshStandardMaterial({ color: 0x1A0A14, roughness: .5 })); arc.position.set(s * .175, .64, .445); arc.rotation.y = s * .32; arc.visible = false; bod.add(arc);
    eg.arc = arc;
    CREE.eyes.push(eg); CREE.pupils.push(pg); CREE.cats.push([c1, c2]);
  }
  // brows: thin darker pink arcs
  CREE.brows = [];
  for (const s of [-1, 1]) { const b = new THREE.Mesh(new THREE.CapsuleGeometry(.014, .1, 4, 10), new THREE.MeshStandardMaterial({ color: 0xB0106A, roughness: .6 })); b.rotation.z = Math.PI / 2; const bg = new THREE.Group(); bg.position.set(s * .175, .82, .405); bg.add(b); bod.add(bg); CREE.brows.push(bg); }
  // beak: upper and lower halves, yellow-orange, red inside; the lower half hinges open
  const beakM = new THREE.MeshPhysicalMaterial({ color: 0xFFC21A, roughness: .35, clearcoat: .6, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .4 });
  const beakM2 = new THREE.MeshPhysicalMaterial({ color: 0xF2A516, roughness: .4, clearcoat: .5, envMap: ENV, envMapIntensity: .3 });
  const up = new THREE.Mesh(new THREE.SphereGeometry(.085, 28, 18, 0, Math.PI * 2, 0, Math.PI / 2), beakM); up.scale.set(1.15, .7, 1.05); up.position.set(0, .495, .485); up.rotation.x = .25; bod.add(up);
  const mouth = new THREE.Mesh(new THREE.SphereGeometry(.06, 18, 12), new THREE.MeshStandardMaterial({ color: 0x9E1B2E, roughness: .7 })); mouth.scale.set(1.1, .6, .6); mouth.position.set(0, .48, .47); bod.add(mouth);
  const lowG = new THREE.Group(); lowG.position.set(0, .49, .46); bod.add(lowG);
  const low = new THREE.Mesh(new THREE.SphereGeometry(.07, 24, 14, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), beakM2); low.scale.set(1.05, .75, 1.0); low.position.set(0, 0, .02); lowG.add(low);
  CREE.jaw = lowG;
  // wings: short rounded arms, pivoting at the shoulder
  CREE.wings = [];
  for (const s of [-1, 1]) {
    const pv = new THREE.Group(); pv.position.set(s * .45, .5, .02); bod.add(pv);
    const w = new THREE.Mesh(new THREE.SphereGeometry(.13, 24, 18), plush); w.scale.set(.6, 1.15, .78); w.position.set(s * .03, -.11, 0); w.castShadow = true; pv.add(w);
    const tip = new THREE.Group(); tip.position.set(s * .04, -.24, .02); pv.add(tip); pv.tip = tip;
    CREE.wings.push(pv);
  }
  // feet: stubby yellow-orange ovals
  CREE.feet = [];
  for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.SphereGeometry(.1, 22, 14), beakM2); f.scale.set(1.05, .5, 1.5); const fg = new THREE.Group(); fg.position.set(s * .15, .04, .14); fg.add(f); f.castShadow = true; R.add(fg); CREE.feet.push(fg); }
  // the magnifier: a clear lens, thin gold rim, wooden handle (held in the right wing, or lying on the desk)
  const mg = new THREE.Group(); CREE.mag = mg;
  const rim = new THREE.Mesh(new THREE.TorusGeometry(.11, .012, 10, 40), goldM); mg.add(rim);
  const lens = new THREE.Mesh(new THREE.CircleGeometry(.105, 36), new THREE.MeshPhysicalMaterial({ color: 0xEAF6FF, roughness: 0, transparent: true, opacity: .22, envMap: ENV, envMapIntensity: 1.5, side: THREE.DoubleSide })); mg.add(lens);
  const hd = new THREE.Mesh(new THREE.CylinderGeometry(.016, .02, .17, 12), mat(0x8A5A34, { roughness: .5 })); hd.position.y = -.2; mg.add(hd);
  const fer = new THREE.Mesh(new THREE.CylinderGeometry(.019, .019, .025, 12), goldM); fer.position.y = -.115; mg.add(fer);
  scene.add(mg);
}
// state -> pose. s: {x, y, z, ry, sc, sq (squash), lean, wl/wr: [rz, rx] wing angles, eyes ('open'|'happy'|'wide'|'squint'|'closed'),
// look: [x, y], jaw (0..1), brow (tilt), browY, mag ('hand'|'desk'|null), magAt (desk position), oneEye}
function placeCree(vis, s) {
  CREE.root.visible = !!vis; CREE.mag.visible = !!(vis && s.mag);
  if (!vis) return;
  const R = CREE.root, sc = s.sc ?? .34, sq = s.sq ?? 0;
  const dk = !!CREE.dark;      // silhouette: no environment light, dark eyes
  CREE.plush.envMapIntensity = dk ? 0 : .35; CREE.sclM.envMapIntensity = dk ? 0 : .5; CREE.sclM.color.set(dk ? 0x2A1A26 : 0xFFFFFF); CREE.rimM.color.set(dk ? 0x2A1424 : 0xFFC2DE); CREE.pupM.envMapIntensity = dk ? 0 : .9;
  R.position.set(s.x, s.y, s.z); R.rotation.set(s.lean ?? 0, s.ry ?? 0, s.roll ?? 0); R.scale.setScalar(sc);
  CREE.bod.scale.set(1 + sq * .5, 1 - sq, 1 + sq * .5);
  for (let k = 0; k < 2; k++) {
    const w = k ? s.wr : s.wl, sgn = k ? 1 : -1;
    CREE.wings[k].rotation.set(w ? w[1] : 0, 0, sgn * (w ? w[0] : .15));
    const e = s.eyes || "open", eg = CREE.eyes[k];
    let ey = 1; if (e === "closed") ey = .08; else if (e === "squint") ey = .5; else if (e === "wide") ey = 1.12;
    if (e === "open" && !s.noblink && blinkAt(3.3, NOW)) ey = .08;
    eg.scale.set(e === "wide" ? 1.1 : 1, ey, 1);
    const pg = CREE.pupils[k]; const lk = s.look || [0, 0];
    pg.position.set(lk[0] * .035, lk[1] * .035, .06); pg.scale.setScalar(e === "wide" ? .82 : (e === "happy" ? .01 : 1));
    for (const c of CREE.cats[k]) c.visible = !(s.oneEye && k === 0);
    const b = CREE.brows[k]; b.rotation.z = sgn * (s.brow ?? 0); b.position.y = .82 + (s.browY ?? 0) + (e === "wide" ? .04 : 0);
  }
  // happy eyes: the eyes close into dark upturned arcs
  for (const eg of CREE.eyes) { const h = s.eyes === "happy"; eg.visible = !h; eg.arc.visible = h; }
  CREE.jaw.rotation.x = (s.jaw ?? .25) * .9;
  for (let k = 0; k < 2; k++) { const f = CREE.feet[k]; f.position.y = .04 + (s.step && (k ? s.step > 0 : s.step < 0) ? Math.abs(s.step) * .08 : 0); f.rotation.x = 0; }
  R.updateMatrixWorld(true);
  if (s.mag === "hand") { const tip = CREE.wings[1].tip; tip.getWorldPosition(V); CREE.mag.position.copy(V).add(V2.set(0, .035 * sc / .34, .02)); CREE.mag.rotation.set(s.magRx ?? 0, s.ry ?? 0, s.magRz ?? .25); CREE.mag.scale.setScalar(sc / .34 * .55); }
  if (s.mag === "desk") { CREE.mag.position.copy(s.magAt); CREE.mag.rotation.set(-Math.PI / 2 + .1, 0, .6); CREE.mag.scale.setScalar(.55); }
}
// gibberish talk: the beak flaps while Cree "speaks" (times from CT.chirps)
const chirpAt = (t) => C.chirps.some(([a, b]) => t > a && t < b);
const creeJaw = (t) => chirpAt(t) ? .25 + .75 * Math.abs(Math.sin(t * 19)) * (.6 + .4 * Math.sin(t * 7.3)) : .2;

// ---------------------------------------------------------------- the creator
const LEO = makeChar({ id: "leo", skin: "#E2AE86", hair: "#2A1A12", style: "short", top: "#EFE6D6", topStyle: "hoodie", pants: "#6A6660", shoe: "#FFFDF8", brow: "#2A1A12" }, scene);
LEO.seed = 1.7;
// a phone in his right hand (shown when he's holding it)
LEO.phone = new THREE.Group(); LEO.hand[1].add(LEO.phone); LEO.phone.position.set(0, -.08, .1);
box(.1, .18, .014, mat(0x16141A, { roughness: .3 }), 0, 0, 0, { parent: LEO.phone, cast: false });
LEO.scr = new THREE.MeshBasicMaterial({ color: 0xDDE8FF, toneMapped: false }); { const sp = new THREE.Mesh(new THREE.PlaneGeometry(.088, .165), LEO.scr); sp.position.z = -.008; sp.rotation.y = Math.PI; LEO.phone.add(sp); }
// a pen that rolls off the desk on the thud
const PEN = cyl(.008, .008, .14, mat(0xF343A2), 0, 0, 0, 8); PEN.rotation.z = Math.PI / 2;

// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const Ls = (k) => C.lines[k][0], Le = (k) => C.lines[k][1], Bs = (k) => C.beats[k][0], Be = (k) => C.beats[k][1];
const talking = (t, k) => t > Ls(k) - .03 && t < Le(k) + .03;
const wordT = (k, i) => { const ws = C.words.filter((w) => w.take === k); return ws[Math.min(i, ws.length - 1)].s; };
const SHOTS = [
  ["phone", 0], ["rant", Ls("02") - .15], ["thud", Bs("thud")], ["window", Ls("04") - .1], ["reveal1", Bs("reveal1")],
  ["bed", Ls("05") - .1], ["reveal2", Bs("reveal2")], ["pillow", Ls("06") - .1], ["hero", Bs("hero")], ["whoa", Ls("07") - .08],
  ["say", Bs("say")], ["fix1", Bs("fix1")], ["fix2", Bs("fix2")], ["fix3", Bs("fix3")], ["hug", Ls("10") - .15], ["end", Bs("endin")],
];
const shotAt = (t) => { let k = 0; for (let i = 0; i < SHOTS.length; i++) if (t >= SHOTS[i][1]) k = i; return [SHOTS[k][0], t - SHOTS[k][1], (SHOTS[k + 1] ? SHOTS[k + 1][1] : DUR) - SHOTS[k][1]]; };
const DESKC = v(.05, DESKY, .12);          // where Cree stands on the desk
const seated = (o = {}) => pose({ x: SEAT.x, y: SITY, z: SEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .1, ...o });
const standing = (o = {}) => pose({ a: [[.1, .12, .15], [.1, .12, .15]], ...o });

// ---------------------------------------------------------------- one frame
const CAM = { p: v(0, 1.5, 3), l: v(0, 1, 0), fov: 40, focus: 3, ap: .05 };
function shoot(t) {
  const [sh, u, len] = shotAt(t);
  // defaults: the room at night, nothing special on
  CREE.dark = false;
  RM.visible = true; RM.hall.visible = true;
  for (const k of ["strip", "cards", "mach", "glow", "glow2", "rays", "dust", "door"]) FX[k].visible = false;
  for (const p of FX.planes) p.visible = false;
  PEN.visible = false; LEO.phone.visible = false;
  scene.background = tmpC.set(0x1A1224).clone(); scene.fog.color.set(0x1A1224); scene.fog.near = 30; scene.fog.far = 80;
  hemi.color.set(0x9C88D6); hemi.groundColor.set(0x2E1E2E); hemi.intensity = .55;
  sun.color.set(0x9CC4FF); sun.intensity = .45; sun.target.position.set(0, 0, -.5); sun.position.set(-3.2, 5, 3.5);
  RM.key.intensity = 3.2; RM.fill.intensity = 1.6; RM.lamp.intensity = 1.4; RM.lamp.color.set(0xFFB8DA); RM.lamp.position.set(-.78, 1.3, -.1); RM.moon.intensity = 0; RM.hallL.intensity = .6; RM.hero.intensity = 0; RM.gold.intensity = 0;
  phoneL.intensity = 0; RM.triScr.color.set(0xFFE3F1); RM.bedScr.color.set(0xFFE3F1); RM.lampShade.emissiveIntensity = .8;
  for (const b of RM.fairy) b.visible = true;
  let bloomS = .42, sat = 1.06, vig = .42, dark = 0;
  let cree = null, leo = null, leoF = {}, leoRot = null;
  const cam = CAM;

  if (sh === "phone") {             // 1. extreme close-up: the phone's glow on his face; then he slides off the chair
    const slide = ss(t, Le("01") + .05, Ls("02") - .2);
    leo = seated({ y: SITY - .75 * slide, z: SEAT.z + .1 * slide, hp: -.05 - .25 * slide, hy: -.18, a: [[.3, .15, .3], [1.55, -.15, 1.75]], lean: -.06 + .1 * slide });
    leoF = { eyes: "wide", mouth: talking(t, "01") ? (Math.floor(t * 7) % 2 ? "wavy" : "gasp") : "wavy", brows: "despair", noblink: true };
    LEO.phone.visible = true; LEO.scr.color.set(0xDDE8FF);
    cam.p.set(.05, 1.7, 1.75 - .2 * ss(u, 0, 3.2)); cam.l.set(-.02, 1.45 - .12 * slide, -.62); cam.fov = 36; cam.focus = 2.3; cam.ap = .06;
    RM.key.intensity = .9; RM.fill.intensity = .5; hemi.intensity = .3;
    phoneL.intensity = 1.4;
  } else if (sh === "rant") {     // 2. the rant: pacing, arms up, counting, hands in his hair
    const ph = u * 3.4, x = .3 + .55 * Math.sin(u * 1.1);
    const w1 = wordT("02", 1), w2 = wordT("02", 5), w3 = wordT("02", 9);
    const arms = kf(t, [[w1 - .5, { a0: .55, a1: .55, s0: .55, e0: .5 }], [w1 - .05, { a0: 2.9, a1: 2.9, s0: .35, e0: .2 }], [w2 - .3, { a0: 2.7, a1: 2.7, s0: .35, e0: .2 }],
      [w2, { a0: .4, a1: 1.6, s0: .2, e0: .5 }], [w3 - .3, { a0: .4, a1: 1.6, s0: .2, e0: .5 }], [w3, { a0: 2.6, a1: 2.6, s0: .75, e0: 2.25 }]]);
    const walkA = clamp(1 - ss(t, w3 - .1, w3 + .3)) * .8;
    let p = walk(standing({ x, z: 1.05, ry: Math.cos(u * 1.1) * .55 }), ph, walkA);
    p.a = [[arms.a0, arms.s0, arms.e0], [arms.a1, arms.s0, arms.e0]];
    p.hp = -.1; p.lean = -.05;
    leo = p; leoF = { eyes: "wide", mouth: "rant", brows: t > w3 ? "despair" : "angry", talk: talking(t, "02"), big: true, noblink: true };
    cam.p.set(.3 + .15 * Math.sin(u * .9), 1.45, 5.0 - .3 * ss(u, 0, len)); cam.l.set(.3 + .2 * Math.sin(u * 1.1), 1.25, .8); cam.fov = 44; cam.focus = 3.3; cam.ap = .04;
  } else if (sh === "thud") {     // 3. face-down on the desk, a pen rolls away
    const drop = ss(u, 0, .22), bnc = .06 * Math.sin(clamp((u - .22) / .3) * Math.PI) * (u > .22 && u < .52 ? 1 : 0);
    leo = seated({ lean: .5 * drop - bnc, hp: -.08 * drop, hy: .1 * Math.sin(u * .8) * drop, hr: 1.2 * drop, a: [[.05 + 1.0 * drop, .55 * drop, 1.6 * drop], [.05 + 1.0 * drop, .55 * drop, 1.6 * drop]] });
    leoF = { eyes: u > .3 ? "cry" : "closed", mouth: talking(t, "03") ? "wail" : "sad", brows: "despair", talk: talking(t, "03") };
    PEN.visible = true; const pr = ramp(u, .25, 1.4), fall = Math.max(0, u - 1.4);
    PEN.position.set(.15 + .75 * pr + .25 * fall, DESKY + .008 - 1.8 * fall * fall, .25); PEN.rotation.set(0, 0, Math.PI / 2); PEN.rotation.x = u * 9;
    cam.p.set(-.05, 1.12, 1.85); cam.l.set(-.25, 1.02, -.45); cam.fov = 32; cam.focus = 2.4; cam.ap = .05;
  } else if (sh === "window") {   // 4. at the window, looking up: the first wish
    leo = standing({ x: -1.5, z: -1.72, ry: Math.PI - .6, hp: -.28, hy: .6, a: [[1.75, .05, .5], [.1, .12, .15]] });
    leoF = { eyes: "teary", mouth: talking(t, "04") ? "talk" : "sad", brows: "worry", talk: talking(t, "04") };
    cam.p.set(.45 - .15 * ss(u, 0, len), 1.8, .55 - .15 * ss(u, 0, len)); cam.l.set(-1.45, 1.72, -2.0); cam.fov = 40; cam.focus = 3.1; cam.ap = .04;
    RM.moon.intensity = 2.2; RM.key.intensity = 1.6; hemi.intensity = .4;
  } else if (sh === "reveal1") {  // 5. HALF REVEAL: a small silhouette in the dark doorway, one eye catching the light
    cree = { x: -3.62, y: 0, z: -1.0, ry: Math.PI / 2 - .25, sc: .34, eyes: "open", oneEye: true, noblink: true, wl: [.12, 0], wr: [.12, 0], jaw: .1, look: [0, 0], roll: .12 * ss(u, 1.1, 1.6) * (1 - ss(u, 2.0, 2.4)) };
    CREE.dark = true;
    FX.door.visible = true; FX.door.position.set(-4.4, .55, -1.0); FX.door.lookAt(v(.6, .5, .2)); FX.door.scale.setScalar(1.8 + .1 * Math.sin(u * 2));
    RM.key.intensity = .12; RM.fill.intensity = .15; RM.lamp.intensity = .2; hemi.intensity = .06; sun.intensity = .08; RM.hallL.intensity = 4.5; RM.hallL.position.set(-4.4, .5, -1.0);
    RM.lampShade.emissiveIntensity = .1; for (const b of RM.fairy) b.visible = false;
    cam.p.set(1.5, .32, -.95); cam.l.set(-3.62, .3, -1.0); cam.fov = 27 - 4 * ss(u, 0, len); cam.focus = 5.1; cam.ap = .025;
    bloomS = .7; vig = .6;
  } else if (sh === "bed") {      // 6. hugging his knees on the bed: the second wish
    leo = pose({ x: 2.45, y: -.17, z: -1.05, ry: -Math.PI / 2 + .35, l: [[2.15, 2.5], [2.15, 2.5]], a: [[1.25, .28, 1.55], [1.25, .28, 1.55]], lean: .15, hp: .12, hy: .2 });
    leoF = { eyes: "teary", mouth: talking(t, "05") ? "talk" : "sad", brows: "despair", talk: talking(t, "05") };
    cam.p.set(-.1 + .15 * ss(u, 0, len), 1.45, 1.15); cam.l.set(2.45, 1.0, -1.08); cam.fov = 36; cam.focus = 3.4; cam.ap = .04;
  } else if (sh === "reveal2") {  // 7. HALF REVEAL: two feet land on the desk, dust, the magnifier glints; his face stays out of frame
    const land = ramp(u, 0, .35), y = DESKY + .9 * (1 - land) ** 2;
    const sq = u > .35 ? .22 * Math.exp(-(u - .35) * 7) * Math.cos((u - .35) * 22) : -.08 * land;
    cree = { x: DESKC.x, y, z: DESKC.z, ry: -.15, sc: .34, sq, eyes: "open", wl: [.2, 0], wr: [.2, 0], jaw: creeJaw(t), mag: "desk", magAt: v(.28, DESKY + .012, .26) };
    FX.dust.visible = true; FX.dust.position.set(DESKC.x, DESKY + .01, DESKC.z); const db = ramp(u, .33, 1.6); FX.dust.scale.set(.25 + .5 * db, .12 + .25 * db, .25 + .5 * db); FX.dust.material.opacity = (u > .33 ? 1 : 0) * (1 - db * .7);
    FX.glow2.visible = u > .8; FX.glow2.position.set(.28, DESKY + .03, .3); FX.glow2.lookAt(cam.p); FX.glow2.scale.setScalar(.06 * pulse(u, 1.0, .18) + .001);
    RM.hero.intensity = 2.5; RM.hero.position.set(DESKC.x, DESKY + .5, DESKC.z - .5);
    RM.key.intensity = 1.2; hemi.intensity = .3;
    cam.p.set(.22, DESKY + .01, 1.05); cam.l.set(.06, DESKY - .05, .12); cam.fov = 30; cam.focus = .93; cam.ap = .09;
  } else if (sh === "pillow") {   // 8. face-down in the pillow, the phone buzzing: the third wish
    const lift = .7 + .3 * ss(t, Ls("06") + .1, Ls("06") + .6);
    leo = pose({ x: 2.7, y: .72, z: -2.25, l: [[0, .1], [0, .1]], a: [[2.7, .35, .5], [2.7, .35, .5]], hp: -1.05 * lift, hy: .15 * lift });
    leoRot = [Math.PI / 2, 0, 0];
    leoF = { eyes: lift > .5 ? "teary" : "closed", mouth: talking(t, "06") ? "talk" : "sad", brows: "despair", talk: talking(t, "06") };
    RM.bedPhone.rotation.y = .06 * Math.sin(t * 60) * (Math.floor(t * 1.5) % 2); RM.bedScr.color.set(0xFFF4FA);
    phoneL.intensity = .35; phoneL.position.set(2.25, .8, -1.35);
    RM.lamp.intensity = 3.2; RM.lamp.color.set(0xFFD6EA); RM.lamp.position.set(2.65, 1.25, .75);
    cam.p.set(2.64, 1.3, 1.85); cam.l.set(2.7, .82, -.5); cam.fov = 38; cam.focus = 2.1; cam.ap = .05;
  } else if (sh === "hero") {     // 9. HERO REVEAL: Cree on the desk, light flooding in behind him
    const fl = ss(u, 0, .9);
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z, ry: 0, sc: .34, lean: -.06, eyes: "open", wl: [-.35, -.35], wr: [2.5 * ss(u, .6, 1.2), -.1], jaw: .3, brow: -.18, browY: -.02, look: [0, .1], mag: "hand", magRz: -.1 };
    FX.glow.visible = FX.rays.visible = FX.dust.visible = true;
    FX.glow.position.set(DESKC.x, DESKY + .2, DESKC.z - .35); FX.glow.lookAt(cam.p); FX.glow.scale.setScalar(.05 + .7 * fl);
    FX.rays.position.set(DESKC.x, DESKY + .1, DESKC.z - .5); FX.rays.lookAt(cam.p); FX.rays.rotation.z = u * .12; FX.rays.scale.setScalar(.35 * fl);
    for (const r of FX.rays.children) r.material.opacity = (.35 + .25 * Math.sin(u * 1.7 + r.ray * 1.9)) * fl;
    FX.dust.position.set(DESKC.x, DESKY, DESKC.z - .2); FX.dust.scale.set(1.2, .9, .6); FX.dust.rotation.y = u * .15; FX.dust.material.opacity = .8 * fl;
    RM.hero.intensity = 2.4 * fl; RM.hero.position.set(DESKC.x, DESKY + .35, DESKC.z - .35); RM.gold.intensity = 2 * fl; RM.gold.position.set(DESKC.x + .3, DESKY + .3, DESKC.z + .2);
    RM.key.intensity = 1.0; RM.fill.intensity = .6; hemi.intensity = .25;
    cam.p.set(.05, DESKY + .08 + .04 * ss(u, 0, len), 1.95 - .35 * ss(u, 0, len)); cam.l.set(.05, DESKY + .26, DESKC.z); cam.fov = 34; cam.focus = 1.4; cam.ap = .06;
    bloomS = .42 + .2 * fl;
  } else if (sh === "whoa") {     // 9b. he turns: jaw drop
    const turn = ss(u, 0, .3);
    leo = pose({ x: 2.3, y: -.17, z: -1.0, ry: -Math.PI / 2 - .2 + .25 * turn, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.4, .5, .3], [.4, .5, .3]], lean: -.15 * turn, hp: -.12, hy: .3 * turn });
    leoF = { eyes: "wide", mouth: talking(t, "07") ? "wail" : "gasp", brows: "high", noblink: true };
    RM.hero.intensity = 3.5; RM.hero.position.set(1.4, 1.2, -.9);
    cam.p.set(.45, 1.6, .25); cam.l.set(2.3, 1.3, -1.0); cam.fov = 36 - 4 * ss(u, 0, len); cam.focus = 2.2; cam.ap = .05;
  } else if (sh === "say") {      // 9c. "Say no more."
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z, ry: .25, sc: .34, eyes: u > 1.1 ? "happy" : "open", wl: [-.35, -.35], wr: [.4 + .3 * Math.sin(u * 5), .9], jaw: creeJaw(t), brow: -.1, look: [.4, .1], mag: "hand", magRz: -.4 };
    FX.glow.visible = true; FX.glow.position.set(DESKC.x, DESKY + .25, DESKC.z - .4); FX.glow.lookAt(cam.p); FX.glow.scale.setScalar(1.2);
    RM.hero.intensity = 3; RM.hero.position.set(DESKC.x, DESKY + .35, DESKC.z - .35);
    cam.p.set(-.3, DESKY + .36, 1.75); cam.l.set(DESKC.x, DESKY + .2, DESKC.z); cam.fov = 30; cam.focus = 1.7; cam.ap = .05;
  } else if (sh === "fix1") {     // 10. the film strip: Cree walks it with his magnifier, taps second three
    FX.strip.visible = true;
    const walkU = ramp(u, .2, 1.6), x = lerp(.5, -.36, sm(walkU));
    const tap = ss(u, 1.65, 1.85) * (1 - ss(u, 2.3, 2.6));
    cree = { x, y: DESKY, z: .18, ry: -.35 + .35 * ss(u, 1.5, 1.7), sc: .3, eyes: tap > .5 ? "wide" : "open", wl: [.15 + 2.2 * tap, .3 * tap], wr: [1.9, .5], jaw: creeJaw(t), look: [-.3, .9], mag: "hand", magRz: .2, step: walkU > 0 && walkU < 1 ? Math.sin(u * 14) : 0, roll: walkU > 0 && walkU < 1 ? .08 * Math.sin(u * 14) : 0 };
    for (let i = 0; i < FX.frames.length; i++) { const f = FX.frames[i], hot = i === 1 ? ss(u, 1.8, 2.0) : 0; f.position.y = DESKY + .42 + .015 * Math.sin(u * 2 + i); f.edge.material.color.set(hot > 0 ? 0xFF6A5A : 0xFFC7E3); f.edge.material.opacity = .55 + .45 * hot * (.6 + .4 * Math.sin(u * 12)); f.scale.setScalar(1 + .25 * hot); }
    leo = standing({ x: -.4, z: -.75, ry: .1, lean: .32, hp: .25, hy: -.15, a: [[.5, .15, .9], [.5, .15, .9]] });
    leoF = { eyes: "wide", mouth: talking(t, "08") ? "talk" : "o", brows: "high", talk: talking(t, "08") };
    RM.hero.intensity = 1.5; RM.hero.position.set(-.3, DESKY + .45, .2);
    cam.p.set(-.1, 1.35, 2.6 - .2 * ss(u, 0, len)); cam.l.set(-.16, 1.15, -.1); cam.fov = 40; cam.focus = 2.4; cam.ap = .04;
  } else if (sh === "fix2") {     // 11. the reel cards: one glows gold
    FX.cards.visible = true;
    for (let i = 0; i < 5; i++) {
      const c = FX.cardL[i], a = (i - 2) * .42 * ss(u, .1, .7), flip = ss(u, .5 + i * .18, .75 + i * .18);
      c.position.set(DESKC.x + Math.sin(a) * .38, DESKY + .42 + Math.cos(a) * .12 - .1, DESKC.z - .12); c.rotation.set(0, Math.PI * (1 - flip) + a * -.3, -a * .5);
      const gold = i === 3 ? ss(u, 1.5, 1.8) : 0; c.cmat.emissiveIntensity = i === 3 ? .25 + 1.4 * gold : .25; c.scale.setScalar(1 + .25 * gold);
    }
    cree = { x: DESKC.x, y: DESKY, z: DESKC.z + .05, ry: 0, sc: .3, eyes: u > 1.6 ? "happy" : "open", wl: [.4, 0], wr: [1.2 + .9 * Math.sin(u * 4) * (u < 1.6 ? 1 : 0), .3], jaw: creeJaw(t), look: [0, .8] };
    RM.gold.intensity = 2.5 * ss(u, 1.5, 1.8); RM.gold.position.set(DESKC.x + .2, DESKY + .5, DESKC.z);
    leo = standing({ x: -.45, z: -.75, ry: .2, lean: .15, hp: .1, a: [[.3, .12, .3], [1.55 * ss(t, Ls("09") - .3, Ls("09")), .05, .1]] });
    leoF = { eyes: "wide", mouth: talking(t, "09") ? "laugh" : "o", brows: "high", talk: talking(t, "09") };
    cam.p.set(-.55, 1.42, 2.25); cam.l.set(.0, 1.15, -.1); cam.fov = 40; cam.focus = 2.3; cam.ap = .04;
  } else if (sh === "fix3") {     // 12. the DM machine: Cree pulls the lever, paper planes stream out of the phone
    FX.mach.visible = true;
    const pull = ss(u, .7, .95);
    FX.lever.rotation.z = .5 - 1.1 * pull; FX.machLight.material.color.set(pull > .5 ? 0x5BE3B0 : 0x3A3A3A);
    cree = { x: DESKC.x - .02, y: DESKY, z: .17, ry: .65, sc: .3, eyes: pull > .5 ? "happy" : "open", wl: [.3, 0], wr: [1.4 - .5 * pull, .6 + .4 * pull], jaw: creeJaw(t), look: [.6, .2], sq: .06 * Math.sin(u * 9) * (1 - pull) };
    RM.triScr.color.set(0xFFFFFF);
    for (let i = 0; i < FX.planes.length; i++) {
      const p = FX.planes[i], a = u - .95 - i * .14; p.visible = a > 0 && a < 1.6;
      if (!p.visible) continue;
      const k = a / 1.6, o = v(.55, DESKY + .23, -.05);
      p.position.set(o.x - .4 * k + .25 * Math.sin(i * 1.7) * k, o.y + .55 * k + .12 * Math.sin(k * 6 + i), o.z + 1.6 * k * (.7 + .3 * hash(i)));
      p.lookAt(p.position.x - .4, p.position.y + .4, p.position.z + 1.6); p.scale.setScalar(1.6);
    }
    leo = standing({ x: -.4, z: -.75, ry: .1, lean: -.05, hp: -.1, a: u > 1.1 ? [[2.6, .75, 2.25], [2.6, .75, 2.25]] : [[.4, .4, .4], [.4, .4, .4]] });
    leoF = { eyes: u > 1.1 ? "happy" : "wide", mouth: u > 1.1 ? "laugh" : "gasp", brows: "high", noblink: true };
    cam.p.set(.85, 1.35, 2.3); cam.l.set(.15, 1.1, -.2); cam.fov = 42; cam.focus = 2.25; cam.ap = .04;
  } else if (sh === "hug") {      // 13. he scoops Cree up: happy tears; Cree pats his head
    leo = standing({ x: -.1, z: .75, ry: .15, lean: .05, hp: .18, hr: .2, a: [[1.25, .5, 1.75], [1.25, .5, 1.75]] });
    leoF = { eyes: "sob", mouth: talking(t, "10") ? "laugh" : "grin", brows: "worry", talk: talking(t, "10") };
    cree = { x: 0, y: 0, z: 0, ry: -.3, sc: .34, eyes: "happy", wl: [.4, .2], wr: [2.7, .3 + .35 * Math.sin(u * 9)], jaw: creeJaw(t), noblink: true, attach: true };
    cam.p.set(.35, 1.6, 3.75); cam.l.set(-.05, 1.35, .75); cam.fov = 36; cam.focus = 3.0; cam.ap = .04;
  } else if (sh === "end") {      // 14. end card plate: Cree alone in a pink glow, pointing up at the wordmark
    RM.visible = false; for (const b of RM.fairy) b.visible = false;
    scene.background = tmpC.set(0x2A0C22).clone();
    const hop = Math.max(0, Math.sin(clamp((u - 1.2) / .45) * Math.PI)) * .06;
    cree = { x: 0, y: hop, z: 0, ry: -.15, sc: .34, eyes: u > 1.5 ? "happy" : "open", wl: [.2, 0], wr: [2.75, -.25], jaw: creeJaw(t), look: [.3, .9], sq: hop > 0 ? -.05 : .04 * pulse(u, 1.67, .08) };
    FX.glow.visible = true; FX.glow.position.set(0, .3, -.4); FX.glow.lookAt(cam.p); FX.glow.scale.setScalar(1.5);
    FX.dust.visible = true; FX.dust.position.set(0, -.05, -.3); FX.dust.scale.set(1.6, .9, .4); FX.dust.material.opacity = .6;
    hemi.color.set(0xFFC2E2); hemi.groundColor.set(0x5A1A40); hemi.intensity = .9; sun.intensity = 0; RM.key.intensity = 0; RM.fill.intensity = 0; RM.lamp.intensity = 0; RM.hallL.intensity = 0;
    RM.hero.intensity = 4; RM.hero.position.set(0, .45, -.35); RM.gold.intensity = 1.5; RM.gold.position.set(.4, .5, .5);
    cam.p.set(0, .34, 2.1); cam.l.set(0, .5, 0); cam.fov = 32; cam.focus = 2.1; cam.ap = .03;
  }

  // the creator
  if (leo) { placeChar(LEO, true, idle(leo, t, LEO.seed), leoF); if (leoRot) LEO.root.rotation.set(...leoRot); else LEO.root.rotation.x = LEO.root.rotation.z = 0; }
  else placeChar(LEO, false);
  LEO.root.updateMatrixWorld(true);
  // Cree (in the hug he sits against the creator's chest)
  if (cree && cree.attach) { LEO.torso.localToWorld(V.set(0, .3, .34)); cree.x = V.x; cree.y = V.y - .02; cree.z = V.z; }
  placeCree(!!cree, cree || {});
  if (LEO.phone.visible) { LEO.phone.getWorldPosition(V); phoneL.position.copy(V).add(V2.set(0, .03, -.12)); }
  return { cam, bloomS, sat, vig, dark };
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
  for (const k of ["glow", "glow2", "door"]) if (FX[k].visible) FX[k].lookAt(camera.position);
  cocPass.uniforms.uF.value = cam.focus; cocPass.uniforms.uAp.value = cam.ap;
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = .08; gu.uCool.value = 0; gu.uSat.value = r.sat; gu.uCon.value = .06; gu.uVig.value = r.vig; gu.uTint.value = 0;
  gu.uFlash.value = 0; gu.uCA.value = .0008; gu.uKeep.value = 0; gu.uGrain.value = .02; gu.uTop.value = 0; gu.uDark.value = r.dark;
  bloom.strength = r.bloomS;
  sun.shadow.camera.left = -5; sun.shadow.camera.right = 5; sun.shadow.camera.top = 5; sun.shadow.camera.bottom = -5; sun.shadow.camera.near = 1; sun.shadow.camera.far = 30;
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures (no text anywhere in the 3D world; words live in the HTML layer)
const text = (w, h, draw) => pix(w, h, draw, false);
function buildTextures() {
  TEX.night = text(512, 512, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#0E0A2A"); gr.addColorStop(.7, "#2A1A4A"); gr.addColorStop(1, "#4A2456"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 90; i++) { const x = hash(i * 3.1) * w, y = hash(i * 7.7) * h * .7, r = hash(i * 1.9) * 1.6 + .4; g.fillStyle = `rgba(255,240,250,${.4 + hash(i) * .6})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
    const mg = g.createRadialGradient(360, 120, 10, 360, 120, 120); mg.addColorStop(0, "rgba(255,240,220,.55)"); mg.addColorStop(1, "rgba(255,240,220,0)"); g.fillStyle = mg; g.fillRect(200, 0, 312, 260);
    g.fillStyle = "#FFF4E2"; g.beginPath(); g.arc(360, 120, 42, 0, 7); g.fill(); g.fillStyle = "rgba(220,200,190,.5)"; g.beginPath(); g.arc(348, 110, 9, 0, 7); g.arc(372, 132, 6, 0, 7); g.fill();
    for (let b = 0; b < 7; b++) { const x0 = b * 78 - 8, top = 330 + (b * 41 % 110); g.fillStyle = ["#1A1230", "#22183A", "#1E1534"][b % 3]; g.fillRect(x0, top, 72, h - top); for (let i = 0; i < 3; i++) for (let j = 0; j < 6; j++) { g.fillStyle = (b * 7 + i * 3 + j) % 4 ? "#FFC98A" : "#3A2A50"; g.fillRect(x0 + 10 + i * 20, top + 14 + j * 26, 10, 13); } }
  });
  TEX.posters = text(512, 360, (g, w, h) => {
    g.fillStyle = "#6E5A86"; g.fillRect(0, 0, w, h);
    const art = (x, y, ww, hh, c1, c2, k) => { const gr = g.createLinearGradient(x, y, x + ww, y + hh); gr.addColorStop(0, c1); gr.addColorStop(1, c2); g.fillStyle = "#FFF8F2"; g.fillRect(x - 8, y - 8, ww + 16, hh + 16); g.fillStyle = gr; g.fillRect(x, y, ww, hh);
      g.fillStyle = "rgba(255,255,255,.75)"; if (k === 0) { g.beginPath(); g.arc(x + ww / 2, y + hh / 2, ww * .28, 0, 7); g.fill(); } else if (k === 1) { g.beginPath(); g.moveTo(x + ww * .38, y + hh * .3); g.lineTo(x + ww * .38, y + hh * .7); g.lineTo(x + ww * .7, y + hh * .5); g.fill(); } else { for (let i = 0; i < 4; i++) g.fillRect(x + ww * .2 + i * ww * .16, y + hh * (.7 - i * .12), ww * .1, hh * (.12 + i * .12)); } };
    art(30, 40, 140, 190, "#F343A2", "#FF9A6A", 0); art(200, 70, 120, 150, "#5B7FC4", "#B79CFF", 1); art(352, 30, 130, 200, "#F2C94C", "#F343A2", 2);
  });
  for (let k = 0; k < 4; k++) TEX["thumb" + k] = text(128, 220, (g, w, h) => {
    const P = [["#F343A2", "#FF9A6A"], ["#7A5CFF", "#FF8CC6"], ["#F2C94C", "#E8735A"], ["#3EC6C0", "#7A5CFF"]][k];
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, P[0]); gr.addColorStop(1, P[1]); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(255,255,255,.85)"; g.beginPath(); g.arc(w / 2, h * .42, 26, 0, 7); g.fill();
    g.fillStyle = P[0]; g.beginPath(); g.moveTo(w / 2 - 8, h * .42 - 13); g.lineTo(w / 2 - 8, h * .42 + 13); g.lineTo(w / 2 + 13, h * .42); g.fill();
    g.fillStyle = "rgba(255,255,255,.7)"; rr(g, 14, h - 44, w - 28, 10, 5); g.fill(); rr(g, 14, h - 26, w * .5, 10, 5); g.fill();
  });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
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
