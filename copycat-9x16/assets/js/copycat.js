// Copycat reel: "What if you could see every move your competitor makes?" A film-noir what-if in the house voxel style.
// Midnight, rain: June, a baker, walks into detective Kane's office. The bakery across the street copies every post she
// makes. Kane sets up five open-source tools (changedetection.io, RSSHub, Miniflux, Huginn, Ollama), pinned to his case
// board with red string; at 2 AM the rival changes her prices and they know in a minute; in the morning they see her
// "coming Friday" lavender croissant, so June launches hers on Thursday, and on Friday the rival's customers cross the street.
// Black and white with selective colour; everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek.
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

// ---------------------------------------------------------------- characters: blocky figures with pixel faces (from the house voxel engine)
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

// ================================================================= THE SETS
// OFFICE (around the origin): Kane's office. x -3.6 .. 3.6; z -3 (the window wall with the blinds, behind his desk) .. 3.2
// (the wall behind the client chair); ceiling 3.0. Kane sits behind the desk facing +z; the light from the street comes in
// through the blinds behind him. The door is on the left wall, the case board on the right wall.
// STREET (around x = SX): June's bakery on the north side (z = -4.2, facing +z) and Crumb & Co. across the road (z = 4.2).
const SET = {};
const paperMat = (key) => { const m = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .8 }); LATE.push([m, key]); return m; };   // paper takes the room's light
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const SX = 60;
const DESK = v3(0, 0, -1.4), KSEAT = v3(0, 0, -2.08), CSEAT = v3(.1, 0, .35), LAPP = v3(.28, .8, -1.22), KPHONE = v3(.72, .8, -1.0);
const BOARD = v3(3.48, 1.72, -.5);           // the case board's centre, on the right wall, facing -x
const CARDS = [v3(3.44, 2.2, -1.55), v3(3.44, 2.25, .55), v3(3.44, 1.2, -1.45), v3(3.44, 1.15, .5), v3(3.44, 1.72, -1.95)];
const PHOTO = v3(3.43, 1.72, -.5);
const DOORZ = 1.7;
const O = mkSet("office");
{
  const plank = pix(64, 64, (g) => { px(g, "#6E5A48", 0, 0, 64, 64); for (let j = 0; j < 8; j++) { px(g, j % 2 ? "#665342" : "#76604C", 0, j * 8, 64, 8); px(g, "#4A3C30", 0, j * 8, 64, 1); px(g, "#4A3C30", (j * 23) % 64, j * 8, 1, 8); } }, false);
  O.floorM = new THREE.MeshStandardMaterial({ map: rep(plank, 5, 4), roughness: .45, metalness: .05, envMap: ENV, envMapIntensity: .25 });
  flat(7.4, 6.4, O.floorM, 0, 0, .1);
  const paper = pix(64, 64, (g) => { px(g, "#8C877C", 0, 0, 64, 64); for (let i = 0; i < 8; i++) px(g, i % 2 ? "#87827A" : "#918C82", i * 8, 0, 8, 64); }, false);
  const wallM = new THREE.MeshStandardMaterial({ map: rep(paper, 3, 2), roughness: .9 }), trim = mat(0x2A2420), ceilM = mat(0x3A3632);
  box(7.4, .1, 6.4, ceilM, 0, 3.05, .1, { cast: false });
  // the window wall with an opening x -1.3 .. 1.3, y 1.0 .. 2.6
  box(2.3, 3.0, .2, wallM, -2.45, 1.5, -3.0); box(2.3, 3.0, .2, wallM, 2.45, 1.5, -3.0);
  box(2.6, 1.0, .2, wallM, 0, .5, -3.0); box(2.6, .4, .2, wallM, 0, 2.8, -3.0);
  box(2.8, .08, .3, trim, 0, 1.0, -2.95); box(2.8, .08, .26, trim, 0, 2.6, -2.95);
  for (const x of [-1.34, 0, 1.34]) box(.07, 1.6, .22, trim, x, 1.8, -2.98);
  // venetian blinds: slats tilted so the street light falls through in stripes
  O.slats = [];
  for (let k = 0; k < 19; k++) { const s = box(2.62, .012, .085, mat(0xCFC8BA, { roughness: .6 }), 0, 1.06 + k * .082, -2.86, { rx: .62 }); O.slats.push(s); }
  box(.008, 1.6, .008, mat(0x9A9488), -.9, 1.8, -2.84); box(.008, 1.6, .008, mat(0x9A9488), .9, 1.8, -2.84);
  // side walls; the door on the left wall with frosted glass
  box(.2, 3.0, 6.4, wallM, 3.65, 1.5, .1);
  box(.2, 3.0, 4.3, wallM, -3.65, 1.5, -1.05); box(.2, 3.0, 1.0, wallM, -3.65, 1.5, 2.8); box(.2, .65, 1.2, wallM, -3.65, 2.68, DOORZ);
  box(7.4, 3.0, .2, wallM, 0, 1.5, 3.3);
  for (const z of [-3.2, 3.2]) box(7.4, .12, .05, trim, 0, .06, z * .97);
  const door = new THREE.Group(); door.position.set(-3.6, 0, DOORZ - .6); O.add(door); O.door = door;
  box(.06, 2.35, 1.2, mat(0x3A322A), 0, 1.175, .6, { parent: door });
  O.glassM = texMat("doorGlass"); const gl_ = plane(.85, .9, O.glassM, .04, 1.62, .6, Math.PI / 2, door);
  box(.05, .06, .14, metal(0xB8B2A6, .3), .06, 1.05, 1.05, { parent: door });
  O.hallL = new THREE.PointLight(0xE8E0D0, 0, 6, 1.6); O.hallL.position.set(-4.6, 2.1, DOORZ); scene.add(O.hallL);
  // the desk, Kane's chair, the client chair
  box(2.1, .07, 1.05, mat(0x4A3A2C, { roughness: .35 }), DESK.x, .76, DESK.z);
  for (const sx of [-1, 1]) box(.55, .72, .95, mat(0x3E3024), DESK.x + sx * .74, .37, DESK.z);
  box(1.0, .5, .04, mat(0x3E3024), DESK.x, .45, DESK.z + .47);
  const chair = (x, z, ry, back = .62) => { const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; O.add(g); box(.5, .07, .5, mat(0x2E2622), 0, .47, 0, { parent: g }); for (const [dx, dz] of [[-.2, -.2], [.2, -.2], [-.2, .2], [.2, .2]]) box(.05, .45, .05, mat(0x1E1A16), dx, .225, dz, { parent: g }); box(.5, back, .06, mat(0x2E2622), 0, .5 + back / 2, -.23, { parent: g }); return g; };
  chair(KSEAT.x, KSEAT.z - .05, 0, .8); chair(CSEAT.x, CSEAT.z + .05, Math.PI);
  // on the desk: the banker's lamp, the laptop, his phone, a mug, a stack of files, a card file
  O.lampShade = mat(0x50604E, { roughness: .35, emissive: 0xFFE2B0, emissiveIntensity: 0 });
  cyl(.09, .11, .03, metal(0x9C8A60, .3), -.72, .8, -1.55, 16); cyl(.012, .012, .3, metal(0x9C8A60, .3), -.72, .95, -1.55, 8);
  box(.38, .09, .16, O.lampShade, -.72, 1.12, -1.48, { round: .04 });
  O.lampL = new THREE.PointLight(0xFFD9A0, 0, 4.5, 1.7); O.lampL.position.set(-.7, 1.02, -1.35); scene.add(O.lampL);
  const lap = new THREE.Group(); lap.position.copy(LAPP); lap.rotation.y = Math.PI; O.add(lap);
  box(.38, .018, .26, metal(0x8E9096, .35), 0, .009, .13, { parent: lap });
  const lid = new THREE.Group(); lid.rotation.x = -.3; lap.add(lid); O.lid = lid;
  box(.38, .25, .012, metal(0x8E9096, .35), 0, .125, -.007, { parent: lid });
  O.lapM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const ls = new THREE.Mesh(new THREE.PlaneGeometry(.35, .22), O.lapM); ls.position.set(0, .128, 0); lid.add(ls);
  O.lapL = new THREE.PointLight(0xCFE0FF, 0, 1.8, 2); scene.add(O.lapL);
  O.phone = new THREE.Group(); O.phone.position.copy(KPHONE); O.phone.rotation.y = -.35; O.add(O.phone);
  box(.085, .012, .17, mat(0x15171C), 0, .006, 0, { parent: O.phone });
  O.phoneM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const ps = new THREE.Mesh(new THREE.PlaneGeometry(.076, .156), O.phoneM); ps.rotation.x = -Math.PI / 2; ps.position.y = .013; O.phone.add(ps);
  O.phoneL = new THREE.PointLight(0xffffff, 0, 1.2, 2); scene.add(O.phoneL);
  cyl(.05, .045, .1, mat(0xE9E4DA), -.35, .845, -1.0, 14); cyl(.04, .04, .005, mat(0x2A1E16), -.35, .893, -1.0, 14);
  for (let k = 0; k < 4; k++) box(.36, .02, .26, mat(k % 2 ? 0xC9B98E : 0xBFAE84), .78, .81 + k * .021, -1.6, { ry: (hash(k) - .5) * .2 });
  // the case board on the right wall: cork, the photo of Crumb & Co., five case cards, red string
  O.cork = new THREE.MeshStandardMaterial({ map: pix(64, 64, (g) => { px(g, "#9A7A52", 0, 0, 64, 64); for (let i = 0; i < 900; i++) px(g, hash(i) > .5 ? "#86663F" : "#AE8C60", Math.floor(hash(i * 3.1) * 64), Math.floor(hash(i * 7.7) * 64), 1, 1); }, false), roughness: .95 });
  box(.05, 1.75, 3.0, O.cork, BOARD.x + .02, BOARD.y, BOARD.z); box(.06, 1.85, .05, trim, BOARD.x + .01, BOARD.y, BOARD.z - 1.52); box(.06, 1.85, .05, trim, BOARD.x + .01, BOARD.y, BOARD.z + 1.52);
  box(.06, .05, 3.08, trim, BOARD.x + .01, BOARD.y + .9, BOARD.z); box(.06, .05, 3.08, trim, BOARD.x + .01, BOARD.y - .9, BOARD.z);
  O.photoM = paperMat("photo"); plane(.62, .74, O.photoM, PHOTO.x, PHOTO.y, PHOTO.z, -Math.PI / 2);
  O.cards = CARDS.map((p, k) => { const g = new THREE.Group(); g.position.copy(p); g.rotation.y = -Math.PI / 2; g.rotation.z = (hash(k * 5) - .5) * .12; O.add(g); const m = paperMat("card" + k); const pl = new THREE.Mesh(new THREE.PlaneGeometry(.72, .46), m); g.add(pl); pl.castShadow = false; const pin = new THREE.Mesh(new THREE.SphereGeometry(.022, 10, 8), glow(0xFF2A1E)); pin.position.set(0, .19, .02); g.add(pin); return g; });
  O.strings = CARDS.map((p) => { const m = new THREE.Mesh(new THREE.BoxGeometry(1, .008, .008), new THREE.MeshBasicMaterial({ color: 0xFF2A1E, toneMapped: false })); O.add(m); return m; });
  // a filing cabinet, a coat stand, a wall clock, a bookshelf on the back wall, a ceiling fan
  box(.6, 1.3, .55, metal(0x6A6E70, .5), 3.2, .65, 1.9); for (let k = 0; k < 3; k++) box(.4, .02, .02, metal(0xC9CDD4, .2), 3.2, .3 + k * .42, 1.62);
  cyl(.025, .03, 1.8, mat(0x2A2420), -2.9, .9, -2.4, 8); cyl(.2, .2, .03, mat(0x2A2420), -2.9, .02, -2.4, 16);
  O.clockM = texMat("clock"); const ck = new THREE.Mesh(new THREE.CircleGeometry(.26, 40), O.clockM); ck.position.set(-2.3, 2.35, -2.88); O.add(ck);
  O.hands = [0, 1].map((k) => { const g = new THREE.Group(); g.position.set(-2.3, 2.35, -2.86); O.add(g); const hnd = new THREE.Mesh(new THREE.BoxGeometry(.018, k ? .22 : .15, .008), mat(0x1E1B18)); hnd.position.y = (k ? .22 : .15) / 2 - .02; g.add(hnd); return g; });
  box(2.4, 1.9, .35, mat(0x3A2E24), -1.2, .95, 3.08); for (let r = 0; r < 4; r++) { box(2.3, .03, .3, mat(0x2E241C), -1.2, .25 + r * .45, 3.06); for (let k = 0; k < 14; k++) box(.07 + hash(r * 9 + k) * .06, .3 + hash(k * 3 + r) * .08, .22, mat(["#4E4A44", "#6E665C", "#38342E", "#8A8274"][(k + r) % 4]), -2.25 + k * .155, .42 + r * .45, 3.02); }
  box(.9, .7, .04, mat(0x2A2420), 1.6, 1.9, 3.18); O.diplomaM = paperMat("license"); plane(.8, .6, O.diplomaM, 1.6, 1.9, 3.15, Math.PI);
  O.fan = new THREE.Group(); O.fan.position.set(0, 2.82, -.4); O.add(O.fan); cyl(.02, .02, .3, mat(0x2A2420), 0, .1, 0, 8, { parent: O.fan }); cyl(.1, .1, .08, metal(0x6A5A40, .4), 0, -.05, 0, 14, { parent: O.fan });
  for (let k = 0; k < 4; k++) { const b = box(.9, .015, .14, mat(0x4A3A2C), .5, -.07, 0, { parent: O.fan }); const g = new THREE.Group(); O.fan.add(g); g.rotation.y = k * Math.PI / 2; g.add(b); }
  // outside the window: the building across the road, rain, a streetlamp that throws the blinds' stripes into the room
  O.cityM = texMat("cityNight", { transparent: false, fog: false }); const city = plane(16, 10, O.cityM, 0, 2.5, -10, 0); city.material.fog = false;
  O.rainO = rainMesh(700, O);
  O.streetL = new THREE.PointLight(0xE8EEF8, 0, 9, 1.4); O.streetL.position.set(.8, 3.2, -5.2); scene.add(O.streetL);
}
// ---------------------------------------------------------------- rain: thin streaks falling through a box, wrapped in time
function rainMesh(n, parent) {
  const m = new THREE.InstancedMesh(new THREE.BoxGeometry(.006, .32, .006), new THREE.MeshBasicMaterial({ color: 0xDDE6F2, transparent: true, opacity: .42, toneMapped: false, depthWrite: false }), n);
  m.frustumCulled = false; m.castShadow = false; parent.add(m); m.userData.n = n; return m;
}
function rainAt(m, t, cx, cz, w, d, y0, y1, speed = 9) {
  const n = m.userData.n, hh = y1 - y0;
  for (let i = 0; i < n; i++) {
    const x = cx + (hash(i * 1.37) - .5) * w, z = cz + (hash(i * 2.91) - .5) * d;
    const y = y1 - (((t * speed) + hash(i * 4.13) * hh) % hh);
    M4.compose(V.set(x + .04 * Math.sin(i), y, z), Q.setFromEuler(EU.set(0, 0, .06)), S.set(1, 1, 1)); m.setMatrixAt(i, M4);
  }
  m.instanceMatrix.needsUpdate = true;
}

// ---------------------------------------------------------------- the street: June's and Crumb & Co. face each other
const ST = mkSet("street");
const JDOOR = v3(SX - 1.1, 0, -4.1), RDOOR = v3(SX + 1.0, 0, 4.1);
{
  const wet = ST.wet = new THREE.MeshPhysicalMaterial({ map: rep(ASPH, 12, 4), color: 0x9A9EA6, roughness: .28, metalness: .1, clearcoat: .55, clearcoatRoughness: .18, envMap: ENV, envMapIntensity: .7 });
  flat(40, 5.6, wet, SX, -.04, 0);
  for (let k = -6; k < 7; k++) box(1.2, .01, .12, mat(0xD8D4CC), SX + k * 3, -.03, 0, { cast: false });
  const sideM = new THREE.MeshPhysicalMaterial({ map: rep(CONC, 14, 1), roughness: .3, clearcoat: .6, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .5 });
  for (const s of [-1, 1]) { flat(40, 1.6, sideM, SX, .1, s * 3.6); box(40, .14, .16, mat(0x8E8A84), SX, .05, s * 2.82); }
  const brick = pix(64, 64, (g) => { px(g, "#5A5450", 0, 0, 64, 64); for (let j = 0; j < 8; j++) for (let i = 0; i < 4; i++) px(g, ["#625C57", "#57514C", "#6A635D"][(i + j) % 3], i * 16 + (j % 2) * 8, j * 8, 15, 7); }, false);
  const brickM = new THREE.MeshStandardMaterial({ map: rep(brick, 8, 4), roughness: .9 });
  ST.winM = new THREE.MeshStandardMaterial({ color: 0x1A1C22, emissive: 0xFFE2B0, emissiveIntensity: 0, roughness: .3 });
  // a shopfront: brick above, a big window, a door, an awning, the sign; side = -1 north (June's), +1 south (Crumb & Co.)
  const shop = (side, x0, signKey) => {
    const z = side * 4.3, f = -side;          // f: the direction the front faces
    box(9, 5.6, .3, brickM, x0, 6.2, z + side * .15);
    const inM = mat(0x8A7A66); box(9, 3.4, .2, inM, x0, 1.7, z - f * 2.3); for (const dx of [-4.5, 4.5]) box(.2, 3.4, 2.3, inM, x0 + dx, 1.7, z - f * 1.15); box(9, .1, 2.3, inM, x0, 3.4, z - f * 1.15);
    flat(9, 2.3, mat(0x6A5E52), x0, .02, z - f * 1.15);
    for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) box(1.0, 1.2, .05, ST.winM, x0 - 3.2 + c * 2.1, 4.6 + r * 1.6, z + f * .02);
    box(9, .5, .3, mat(0x2A2622), x0, .25, z); box(9, .35, .32, mat(0x2A2622), x0, 3.2, z);
    const glass = new THREE.MeshPhysicalMaterial({ color: 0xBFD0DA, roughness: .05, transparent: true, opacity: .12, envMap: ENV, envMapIntensity: 1, depthWrite: false });
    plane(5.6, 2.5, glass, x0 + .9, 1.75, z + f * .01, side < 0 ? 0 : Math.PI);
    for (const dx of [-2.0, .9, 3.8]) box(.1, 2.6, .2, mat(0x2A2622), x0 + dx, 1.75, z);
    box(1.1, 2.4, .08, mat(0x3A322A), x0 - 2.6, 1.2, z - f * .02);
    const sign = texMat(signKey); plane(4.6, .9, sign, x0, 2.75, z + f * .2, side < 0 ? 0 : Math.PI);
    const awn = texMat(side < 0 ? "awnJune" : "awnRival", { transparent: false }); const a = plane(5.8, 1.0, awn, x0 + .9, 3.1, z + f * .55, side < 0 ? 0 : Math.PI); a.rotation.x = side < 0 ? -.75 : .75;
    // a warm interior behind the glass: counter, shelves of bread
    box(5, 1.0, .5, mat(0x5A4A3A), x0 + .9, .5, z - f * .9); for (let k = 0; k < 10; k++) box(.3, .14, .2, mat(0xC9A27A), x0 - 1.2 + k * .45, 1.1, z - f * .85);
    const pl = new THREE.PointLight(0xFFD9A0, 0, 6, 1.6); pl.position.set(x0 + .9, 2.2, z - f * 1.4); scene.add(pl);
    return pl;
  };
  ST.jL = shop(-1, SX - .8, "signJune"); ST.rL = shop(1, SX + .6, "signRival");
  box(40, 12, .3, brickM, SX - 24.6, 6, -4.5); box(40, 12, .3, brickM, SX + 25.2, 6, 4.5); box(40, 12, .3, brickM, SX + 23.8, 6, -4.5); box(40, 12, .3, brickM, SX - 23.8, 6, 4.5);
  // the A-frame sign outside June's (Thursday) and the banner in Crumb & Co.'s window (Friday), both lavender
  ST.aframe = new THREE.Group(); ST.aframe.position.set(SX - 2.3, 0, -3.05); ST.add(ST.aframe);
  const af = texMat("aframe", { transparent: false });
  const p1 = plane(.7, 1.0, af, 0, .55, .12, 0, ST.aframe); p1.rotation.x = -.18;
  box(.74, 1.04, .03, mat(0x2A2420), 0, .55, .1, { parent: ST.aframe, rx: -.18 }); box(.74, 1.04, .03, mat(0x2A2420), 0, .55, -.1, { parent: ST.aframe, rx: .18 });
  ST.bannerM = texMat("bannerRival"); ST.banner = plane(2.4, .56, ST.bannerM, SX + 1.0, 1.5, 4.12, Math.PI);
  ST.soldM = texMat("soldOut"); ST.sold = plane(.8, .5, ST.soldM, SX - 3.4, 1.6, -4.05, 0);
  // street lamps, rain, the sky glow
  ST.lampM = mat(0xFFF2D8, { emissive: 0xFFE2B0, emissiveIntensity: 0 });
  ST.lamps = [SX - 6, SX + 6].map((x, k) => { const z = k ? 2.95 : -2.95; cyl(.06, .08, 4.4, metal(0x2A2A2E, .5), x, 2.2, z, 10); box(.6, .07, .1, metal(0x2A2A2E, .5), x, 4.4, z - Math.sign(z) * .25); cyl(.14, .2, .2, ST.lampM, x, 4.28, z - Math.sign(z) * .5, 14); const l = new THREE.PointLight(0xFFF0D8, 0, 12, 1.4); l.position.set(x, 4.1, z - Math.sign(z) * .5); scene.add(l); return l; });
  ST.rain = rainMesh(1500, ST);
  ST.sky = new THREE.Mesh(new THREE.SphereGeometry(120, 24, 12), new THREE.MeshBasicMaterial({ color: 0x1A1E28, side: THREE.BackSide, fog: false, toneMapped: false })); ST.sky.position.set(SX, 0, 0); ST.add(ST.sky);
  // the crowd: the Thursday queue outside June's; on Friday some of them cross from Crumb & Co.
  ST.crowd = Array.from({ length: 9 }, (_, i) => npc(40 + i * 3, ST));
}
PARENT = scene;

// ---------------------------------------------------------------- the cast: Kane (the detective), June (the baker), the rival
const KANE = makeChar({ id: "kane", skin: "#E2AE86", hair: "#2A1E16", style: "fedora", hat: "#3A3632", stache: "#2A1E16", brow: "#2A1E16", top: "#8C7D62", topStyle: "trench", pants: "#3A3836", shoe: "#1E1B18" }, O);
KANE.seed = 3.7;
const JUNE = makeChar({ id: "june", skin: "#8E5E40", hair: "#1E1B18", style: "bun", top: "#5B6F8C", topStyle: "apron", pants: "#2E3A55", shoe: "#F4EFE6", lash: true, earring: true }, O);
JUNE.seed = 1.3;
const JUNE2 = makeChar({ ...JUNE.sp, id: "june2" }, ST); JUNE2.seed = 1.3;
const KANE2 = makeChar({ ...KANE.sp, id: "kane2" }, ST); KANE2.seed = 3.7;
const CROIS = new THREE.Group(); ST.add(CROIS);
{ const cm3 = mat(0xC98A4A), lav = glow(0xB26BFF); [[-.07, .0, -.5], [-.035, .02, -.2], [0, .03, 0], [.035, .02, .2], [.07, 0, .5]].forEach(([x, y, r], i) => { const b = box(.05, .045, .05, cm3, x, y, 0, { parent: CROIS, rz: r }); b.scale.y *= i === 2 ? 1.25 : 1; }); box(.12, .008, .03, lav, 0, .045, 0, { parent: CROIS }); }
const RIVAL = makeChar({ id: "rival", skin: "#F3CBA5", hair: "#B88A4A", style: "bob", top: "#3A3A3A", topStyle: "apron", pants: "#1E1B18", shoe: "#1E1B18", lash: true }, ST);
RIVAL.seed = 6.1;
const JPHONE = new THREE.Group(); O.add(JPHONE); box(.08, .16, .012, mat(0x15171C), 0, 0, 0, { parent: JPHONE });
const jpM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }); { const s = new THREE.Mesh(new THREE.PlaneGeometry(.07, .145), jpM); s.position.z = .007; JPHONE.add(s); }
const JPL = new THREE.PointLight(0xffffff, 0, 1.2, 2); scene.add(JPL);


// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
// lines: 0 June's hook | 1 Kane "we watch her" | 2-4 the three clues | 5 June "on Friday?" | 6 Kane "you launch Thursday"
//        7 June "a day behind" | 8 Kane "case closed" | 9 June's CTA
const NT = C.tools;                    // when each clue card is pinned (just before its line)
const M0 = C.montage, D0 = C.morning, TH = C.thu, FR = C.fri;
const who = (t, name) => C.who.some((w, k) => w === name && t > L[k] - .05 && t < E[k] + .02);
// 1 the office at night | 2 the three clues | 4 7 AM | 5 Thursday | 6 Friday
const sceneOf = (t) => (t < M0 ? 1 : t < D0 ? 2 : t < TH ? 4 : t < FR ? 5 : 6);
function clockMin(t) {
  const K = C.clock; let i = 0; while (i + 1 < K.length && t >= K[i + 1][0]) i++;
  const [a, ma] = K[i], [b, mb] = K[Math.min(i + 1, K.length - 1)];
  return b > a ? lerp(ma, mb, clamp((t - a) / (b - a))) : ma;
}
const BOLTS = C.bolts;
const lightning = (t) => Math.max(0, ...BOLTS.map((b) => pulse(t, b, .05) + .7 * pulse(t, b + .16, .06)));

// ---------------------------------------------------------------- shots: [start, {p0, p1, l0, l1, fov, fov1, ap, roll, set}]
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const LAPS = LAPP.clone().add(v(0, .13, 0));
const KHEAD = v(KSEAT.x, 1.5, KSEAT.z + .05), JHEAD = v(CSEAT.x, 1.36, CSEAT.z);
const OVERK = { p0: v(-.78, 1.62, -2.3), p1: v(-.7, 1.6, -2.12), l0: JHEAD, fov: 54, ap: .14 };
const KANECU = (r) => ({ p0: v(1.05, 1.32, .02), p1: v(.92, 1.36, -.16), l0: KHEAD, fov: 52, ap: .14, roll: r });
const cardShot = (k) => { const c = CARDS[k], z = lerp(BOARD.z, c.z, .55); return { p0: v(.55, 1.78, z + .25), p1: v(.95, 1.74, z + .1), l0: v(BOARD.x, lerp(BOARD.y, c.y, .4), z), fov: 54, ap: .06, roll: (k % 2 ? 1 : -1) * .04 }; };
const LAPCU = (k) => [{ p0: v(1.45, 1.5, .35), p1: v(1.25, 1.46, .1), l0: v(.05, 1.22, -1.85) }, { p0: v(-1.35, 1.55, .3), p1: v(-1.15, 1.5, .05), l0: v(.05, 1.22, -1.85) }, { p0: v(.15, 1.85, .6), p1: v(.12, 1.7, .3), l0: v(0, 1.2, -1.8) }].map((q) => ({ ...q, fov: 50, ap: .08, roll: (k - 1) * .04 }))[k];   // Kane at work while the clue fills the screen
const SHOTS = [
  [0, { p0: v(2.85, 1.15, 2.95), p1: v(2.35, 1.2, 2.45), l0: v(-1.5, 1.3, -.4), l1: v(-.6, 1.3, -.4), fov: 60, ap: .02, roll: -.04 }],
  [L[1] - .2, KANECU(.06)],
  ...NT.map((n, k) => [n - .1, cardShot(k)]),                             // the card is pinned; the camera drifts on the board while the clue fills the screen
  [D0, { p0: v(2.65, 1.75, 2.65), p1: v(2.3, 1.62, 2.3), l0: v(-.3, 1.2, -1.1), fov: 54, ap: .02 }],
  [L[5] - .3, { ...OVERK, p0: v(-.62, 1.55, -2.15), p1: v(-.56, 1.52, -1.98), fov: 52 }],
  [L[6] - .2, KANECU(-.05)],
  [TH, { p0: v(SX + 5.2, 3.3, 1.6), p1: v(SX + 3.6, 2.0, 1.05), l0: v(SX - .6, 1.2, -3.6), fov: 52, ap: .01, set: "street" }],
  [TH + 1.25, { p0: v(SX - 1.45, 1.05, -.85), p1: v(SX - 1.6, .95, -1.2), l0: v(SX - 2.3, .75, -3.2), fov: 50, ap: .08, set: "street" }],
  [FR, { p0: v(SX - .5, 1.5, -1.9), p1: v(SX - .1, 1.58, -1.55), l0: v(SX + .4, 1.6, 4.1), fov: 60, ap: .02, set: "street" }],
  [FR + 1.3, { p0: v(SX + 6.2, 4.1, 2.35), p1: v(SX + 5.4, 3.6, 2.1), l0: v(SX - .8, .8, -2.4), fov: 56, ap: .005, set: "street" }],
  [L[7] - .3, { p0: v(SX - .25, 1.58, -.75), p1: v(SX - .32, 1.56, -.95), l0: v(SX - 1.0, 1.45, -3.3), fov: 52, ap: .12, set: "street" }],
  [L[8] - .35, { p0: v(SX + .5, 1.6, -.35), p1: v(SX + .4, 1.58, -.6), l0: v(SX - .45, 1.45, -3.2), fov: 54, ap: .1, set: "street" }],
  [C.endc - .1, { p0: v(SX + .6, 1.95, 2.5), p1: v(SX + .4, 1.9, 2.0), l0: v(SX - .6, 1.5, -3.2), fov: 54, ap: .08, set: "street" }],
];
function shotAt(t) {
  let i = 0; while (i + 1 < SHOTS.length && t >= SHOTS[i + 1][0]) i++;
  const [a, s] = SHOTS[i], b = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR;
  const u = sm(clamp((t - a) / Math.max(.1, b - a)));
  const p = (s.p1 ? V.lerpVectors(s.p0, s.p1, u) : V.copy(s.p0)).clone(); const l = s.l1 ? V2.lerpVectors(s.l0, s.l1, u).clone() : s.l0.clone();
  return { i, a, b, u, p, l, fov: lerp(s.fov, s.fov1 ?? s.fov, u), ap: s.ap, roll: s.roll || 0, set: s.set || "office", f: p.distanceTo(l) };
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
const TYPE = (t) => [[1.15, .12, 1.05 + .08 * Math.sin(t * 13)], [1.15, .12, 1.05 + .08 * Math.sin(t * 11 + 1)]];
function updKane(t, s) {
  if (s >= 5) { KANE.root.visible = false; return; }
  const p = pose({ x: KSEAT.x, y: SITY, z: KSEAT.z, ry: 0, l: [[1.5, 1.5], [1.5, 1.5]], a: [[1.0, .15, 1.2], [1.0, .15, 1.2]], hp: .05 });
  let f = { eyes: "half", mouth: "smirk", brows: "flat", talk: who(t, "kane") };
  if (s === 2) p.a = TYPE(t);
  if (s === 1 && t < L[1] - .3) f = { eyes: "open", mouth: "flat", brows: "raise1" };                 // June bursts in: he looks up
  if (s === 4) { p.hp = .02; f = { eyes: "half", mouth: "smirk", brows: "raise1", talk: who(t, "kane") }; }
  placeChar(KANE, true, idle(p, t, KANE.seed), f);
}
function updJune(t, s) {
  JPHONE.visible = false; JPL.intensity = 0;
  const sit = pose({ x: CSEAT.x, y: SITY, z: CSEAT.z, ry: Math.PI, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.6, .1, .9], [.6, .1, .9]], hp: .02 });
  if (s === 1) {
    // she bursts in, already talking, and drops into the chair
    const u = clamp((t - .15) / (L[1] - .9));
    const sitU = ss(t, L[1] - .55, L[1] - .1);
    const a = along([[-3.3, DOORZ], [-1.6, 1.35], [CSEAT.x + .1, CSEAT.z + .55]], u);
    let p = pose({ x: a.x, z: a.z, ry: a.ry, a: [[.25, .12, .4], [.25, .12, .4]] });
    if (u < 1) { p = walk(p, t * 9, 1.1); p.a[0] = [1.2 + .3 * Math.sin(t * 6), .3, 1.1]; } else p.ry = lerp(a.ry, Math.PI, ss(t, L[1] - .8, L[1] - .5));
    p = mixP(p, sit, sitU);
    placeChar(JUNE, true, idle(p, t, JUNE.seed), { eyes: "wide", mouth: "o", brows: "angry", talk: who(t, "june"), noblink: true });
  } else if (s === 2) {
    placeChar(JUNE, true, idle({ ...sit, hp: -.04, lean: .1 }, t, JUNE.seed), { eyes: "open", mouth: "flat", brows: "up" });
  } else if (s === 4) {
    const p = { ...sit, hp: .02 };
    const f = t < L[5] ? { eyes: "open", mouth: "flat", brows: "flat" } : t < E[5] + .3 ? { eyes: "wide", mouth: "o", brows: "up", talk: who(t, "june"), noblink: true } : { eyes: "happy", mouth: "grin", brows: "up" };
    if (t > L[5] && t < E[5] + .3) p.a = [[1.3, .2, 1.4], [1.3, .2, 1.4]];
    placeChar(JUNE, true, idle(p, t, JUNE.seed), f);
  } else JUNE.root.visible = false;
}
const QUEUE = (i) => [SX - .2 + i * .78, -3.25];
function updStreet(t, s) {
  const day = s >= 5;
  ST.crowd.forEach((P, i) => {
    if (!day) { P.root.visible = false; return; }
    let x, z, ry = -Math.PI / 2, walking = false;
    const crosser = s === 6 && i >= 5;
    if (crosser) {
      const u = clamp((t - (FR + 1.0 + (i - 5) * .35)) / 2.4); const [qx, qz] = QUEUE(i);
      const a = along([[SX + 3.6 + (i - 5) * 1.0, 3.35], [qx + .3, .2], [qx, qz]], u); x = a.x; z = a.z; ry = u < 1 ? a.ry : -Math.PI / 2; walking = u > 0 && u < 1;
    } else if (s === 5 && i >= 5) { P.root.visible = false; return; }
    else [x, z] = QUEUE(i);
    let p = pose({ x, z, ry, a: [[.12, .1, .2], [.12, .1, .2]] });
    if (walking) p = walk(p, t * 8.5 + i, 1);
    placeChar(P, true, idle(p, t, P.seed), { eyes: "open", mouth: i % 3 ? "smile" : "flat", brows: "flat" });
  });
  if (day) {
    const p = pose({ x: JDOOR.x + .1, z: JDOOR.z + .75, ry: .25, a: [[.3, .1, .5], [.3, .1, .5]] });
    if (t > C.endc + .3) { p.a[1] = [2.2, -.2, 1.5]; p.a[1][1] = .1 + .22 * Math.sin(t * 8); }
    placeChar(JUNE2, true, idle(p, t, JUNE2.seed), { eyes: s === 6 && t > L[7] - .3 && t < E[7] ? "happy" : "open", mouth: s === 6 ? "grin" : "smile", brows: "up", talk: who(t, "june") });
  } else JUNE2.root.visible = false;
  // Kane strolls in for the last line with a lavender croissant
  CROIS.visible = false;
  if (s === 6 && t > L[8] - 2.0) {
    const u = clamp((t - (L[8] - 2.0)) / 1.6), a = along([[JDOOR.x + 2.6, -2.2], [JDOOR.x + .95, -2.65]], u);
    let p = pose({ x: a.x, z: a.z, ry: u < 1 ? a.ry : -.35, a: [[.15, .1, .2], [1.3, .15, 1.3]] });
    if (u < 1) { p = walk(p, t * 8, 1); p.a[1] = [1.3, .15, 1.3]; }
    if (t > C.endc + .3) { p.a[0] = [2.6, .1, 2.1]; }                       // tips his hat
    placeChar(KANE2, true, idle(p, t, KANE2.seed), { eyes: t > E[8] ? "happy" : "half", mouth: "smirk", brows: "raise1", talk: who(t, "kane") });
    CROIS.visible = true; holdAt(KANE2, 1, CROIS, [0, -.09, .08]);
  } else KANE2.root.visible = false;
  if (s === 6) placeChar(RIVAL, true, idle(pose({ x: SX - .95, z: RDOOR.z - .8, ry: Math.PI - .2, a: [[.2, .1, .3], [.2, .1, .3]], hp: .12 }), t, RIVAL.seed), { eyes: "half", mouth: "sad", brows: "worry" });
  else RIVAL.root.visible = false;
  ST.banner.visible = s === 6; ST.banner.position.y = 1.62 + .45 * (1 - ss(t, FR + .15, FR + .5));
  ST.wet.roughness = day ? .5 : .28; ST.wet.clearcoat = day ? .2 : .55;
  ST.sold.visible = s === 6;
  ST.aframe.visible = day;
}

// ---------------------------------------------------------------- the case board: cards pinned, red string drawn to the photo
function updBoard(t) {
  O.cards.forEach((g, k) => { const u = k < NT.length ? ss(t, NT[k] - .05, NT[k] + .18) : 0; g.visible = u > 0; g.scale.setScalar(lerp(1.35, 1, u)); });
  O.strings.forEach((m, k) => {
    const u = k < NT.length ? ss(t, NT[k] + .2, NT[k] + .7) : 0;
    if (u <= 0) { m.visible = false; return; }
    m.visible = true;
    const a = PHOTO.clone().add(v(-.02, .28, 0)), b = CARDS[k].clone().add(v(-.02, .19, 0)), e = V.lerpVectors(a, b, u).clone();
    const d = e.clone().sub(a), len = d.length();
    m.position.copy(a).add(e).multiplyScalar(.5); m.scale.set(Math.max(.001, len), 1, 1);
    m.quaternion.setFromUnitVectors(V2.set(1, 0, 0), d.normalize());
  });
}

// ---------------------------------------------------------------- per frame
let SHAKE = 0;
function updOffice(t, s) {
  const night = s <= 2, lt = lightning(t);
  updBoard(t);
  const min = clockMin(t), hrs = (min / 60) % 12;
  O.hands[0].rotation.z = -hrs / 12 * Math.PI * 2; O.hands[1].rotation.z = -(min % 60) / 60 * Math.PI * 2;
  O.fan.rotation.y = t * 1.6;
  O.door.rotation.y = s === 1 ? 1.35 * (1 - ss(t, L[1] - .8, L[1] + .4)) : 0;          // the door flies open as she comes in
  O.hallL.intensity = s === 1 ? 5 * (1 - ss(t, L[1] - .8, L[1] + .2)) : 0;
  O.lampShade.emissiveIntensity = night ? .75 : .2; O.lampL.intensity = night ? 2.8 : .8;
  PL[0].position.set(2.2, 2.6, -.5); PL[0].color.set(0xF2EEE6); PL[0].intensity = night ? 2.4 : .6; PL[0].distance = 3.2;   // a light on the case board
  PL[1].position.set(-1.6, 2.6, 1.2); PL[1].color.set(0xDCE2EC); PL[1].intensity = night ? 2.2 : 0; PL[1].distance = 5.5;   // fill by the door
  PL[2].position.set(.6, 2.4, .2); PL[2].color.set(0xF2EEE6); PL[2].intensity = night ? 1.6 : 0; PL[2].distance = 4.5;      // a soft key on the faces
  O.streetL.intensity = night ? 9 + 40 * lt : 0;
  rainAt(O.rainO, t, 0, -5.2, 6, 3, -1, 5, night ? 9 : 7);
  O.rainO.visible = night || s === 4; O.rainO.material.opacity = night ? .42 : .16;
  // the laptop: a clue's page during its line, idle otherwise
  let mode = 5, u = 0;
  if (s === 2) { const k = Math.max(0, NT.findLastIndex((n) => t > n + .6)); mode = [0, 2, 3][k]; u = clamp((t - (NT[k] + .9)) / 2.6); }
  setMap(O.lapM, DYN.lap(mode, Math.round(u * 40) / 40, Math.floor(t * 2) % 2));
  O.lapL.position.copy(LAPP).add(v(0, .2, -.3)); O.lapL.color.set(0xCFE0FF); O.lapL.intensity = s === 2 ? .9 : .55; O.lapL.distance = 1.8;
  setMap(O.phoneM, DYN.kphone(0)); O.phoneL.intensity = 0;
  updKane(t, s); updJune(t, s);
}

const LOOK_NIGHT = { bg: 0x07080C, hs: 0x8C9AB8, hg: 0x24242A, hi: .8, sun: 0xE8EEF8, si: 2.8, sd: [.18, .5, -1.0], sat: 0, con: .12, vig: .45, tint: .12 };
const LOOK_MORN = { bg: 0xB8BCC4, hs: 0xE8ECF2, hg: 0x5A5650, hi: .9, sun: 0xF2F0EA, si: 3.4, sd: [.3, .42, -1.0], sat: 0, con: .14, vig: .46, tint: .25 };
const LOOK_STREETN = { bg: 0x0C0E14, hs: 0x7080A0, hg: 0x14141A, hi: .85, sun: 0xCAD4E6, si: 1.0, sd: [-.4, .8, .5], sat: 0, con: .2, vig: .6, tint: 0 };
const LOOK_DAY = { bg: 0xC9CDD4, hs: 0xF2F4F8, hg: 0x6A6660, hi: 1.25, sun: 0xFFF6E8, si: 1.6, sd: [-.5, .9, .6], sat: 0, con: .12, vig: .4, tint: .3 };
function renderAt(t) {
  if (!TEX.ready) return;
  NOW = t; SHAKE = 0;
  const s = sceneOf(t);
  for (const k in SET) SET[k].visible = true;
  for (const l of PL) l.intensity = 0;
  const sh = shotAt(t);
  const street = sh.set === "street", day = s >= 5;
  const Lk = street ? (day ? LOOK_DAY : LOOK_STREETN) : s === 4 ? LOOK_MORN : LOOK_NIGHT;
  const lt = lightning(t);
  scene.background = tmpC.set(Lk.bg).clone();
  scene.fog.color.set(Lk.bg); scene.fog.near = street ? 14 : 30; scene.fog.far = street ? 70 : 140;
  hemi.color.set(Lk.hs); hemi.groundColor.set(Lk.hg); hemi.intensity = Lk.hi + 1.6 * lt;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  updOffice(t, s);
  updStreet(t, s);
  // the street's own lights; rain on the street at night
  ST.lamps.forEach((l) => { l.intensity = day ? 0 : 26; l.distance = 14; }); ST.lampM.emissiveIntensity = day ? .1 : 2.2;
  ST.jL.intensity = day ? 2.5 : 11; ST.rL.intensity = day ? 2.5 : 9; ST.jL.distance = ST.rL.distance = 9; ST.winM.emissiveIntensity = day ? 0 : .7;
  ST.rain.visible = street && !day; if (ST.rain.visible) rainAt(ST.rain, t, sh.p.x + 2, sh.p.z, 16, 9, -.2, 7, 11);
  ST.sky.material.color.set(day ? 0xB9BEC6 : 0x14171F);
  const cv = window.CC_COVER;
  camera.position.copy(sh.p).add(V.set(Math.sin(t * .9) * .003 + SHAKE * .03 * Math.sin(t * 61), Math.sin(t * 1.3 + 1) * .003 + SHAKE * .03 * Math.sin(t * 53), 0));
  camera.fov = sh.fov;
  if (cv && cv.cam) { camera.position.set(...cv.cam); sh.l.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix(); camera.up.set(0, 1, 0); camera.lookAt(sh.l);
  camera.rotateZ(sh.roll + (SHAKE ? SHAKE * .015 * Math.sin(t * 47) : 0));
  scene.updateMatrixWorld(true);
  cocPass.uniforms.uF.value = sh.f; cocPass.uniforms.uAp.value = cv ? (cv.ap ?? sh.ap) : sh.ap;
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = 0; gu.uCool.value = street && !day ? .12 : 0; gu.uSat.value = Lk.sat; gu.uCon.value = Lk.con; gu.uVig.value = Lk.vig; gu.uTint.value = Lk.tint;
  gu.uFlash.value = .22 * lt; gu.uCA.value = .0012 + SHAKE * .004; gu.uKeep.value = 1; gu.uGrain.value = .04;
  gu.uTop.value = cv ? 0 : Math.max(1 - ss(t, 2.3, 2.8), ss(t, C.endc, C.endc + .6) * .9, C.screens.some(([a, b]) => t > a - .1 && t < b + .1) ? .55 : 0);
  gu.uDark.value = 0;
  bloom.strength = street && !day ? .55 : .42;
  const cx = street ? SX : 0;
  sun.target.position.set(cx, 0, 0); sun.position.copy(sun.target.position).add(S.set(...Lk.sd).normalize().multiplyScalar(30));
  Object.assign(sun.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10, near: 1, far: 70 });
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures that need the fonts
const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`, SERIF = (w, f, it = false) => `${it ? "italic " : ""}${w} ${f}px Garamond, serif`;
const text = (w, h, draw) => pix(w, h, draw, false);
const block = (g, x, y, w, h, c, r = 14) => { g.fillStyle = c; rr(g, x, y, w, h, r); g.fill(); };
const label = (g, s, x, y, f, c, al = "left", wt = 800) => { g.font = FT(wt, f); g.fillStyle = c; g.textAlign = al; g.fillText(s, x, y); g.textAlign = "left"; };
const mono = (g, s, x, y, f, c, al = "left") => { g.font = MONO(f); g.fillStyle = c; g.textAlign = al; g.fillText(s, x, y); g.textAlign = "left"; };
const RED = "#FF2A1E", LAV = "#B26BFF";
const DYN = {};
function dyn(key, w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  let last = null;
  DYN[key] = (...a) => { const k = a.join("|"); if (k !== last) { last = k; draw(g, w, h, ...a); tx.needsUpdate = true; } return tx; };
}
function buildTextures() {
  // ---- the five case cards: manila, a red EXHIBIT stamp, the tool in typewriter type
  C.toolNames.forEach((nm, k) => {
    TEX["card" + k] = text(576, 368, (g, w, h) => {
      g.fillStyle = "#E4D7B4"; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(120,90,40,.12)"; for (let i = 0; i < 260; i++) g.fillRect(hash(i + k * 99) * w, hash(i * 3 + k) * h, 2, 2);
      g.strokeStyle = "rgba(90,70,40,.35)"; g.lineWidth = 2; for (let y = 120; y < h - 20; y += 44) { g.beginPath(); g.moveTo(24, y); g.lineTo(w - 24, y); g.stroke(); }
      g.save(); g.translate(w - 150, 64); g.rotate(-.12); g.strokeStyle = RED; g.lineWidth = 5; g.strokeRect(-110, -34, 220, 62); mono(g, "EXHIBIT " + "ABCDE"[k], 0, 10, 30, RED, "center"); g.restore();
      let fs = 60; g.font = MONO(fs); while (g.measureText(nm).width > w - 60 && fs > 30) { fs -= 2; g.font = MONO(fs); }
      mono(g, nm, 30, 190, fs, "#1E1B18");
      mono(g, "instead of " + C.toolRep[k], 30, 246, 26, "#5A4A30");
      mono(g, C.toolTag[k], 30, 300, 26, "#1E1B18");
    });
  });
  TEX.photo = text(372, 444, (g, w, h) => {
    g.fillStyle = "#F4F1EA"; g.fillRect(0, 0, w, h); g.fillStyle = "#2A2A2E"; g.fillRect(22, 22, w - 44, 320);
    g.fillStyle = "#4A4A50"; g.fillRect(60, 120, w - 120, 222); g.fillStyle = "#8A8A90"; g.fillRect(80, 190, 120, 152); g.fillStyle = "#6A6A70"; g.fillRect(220, 190, 92, 100);
    g.fillStyle = "#1A1A1E"; g.fillRect(60, 80, w - 120, 44); label(g, "CRUMB & CO.", w / 2, 112, 32, "#E9E4DA", "center");
    g.font = SERIF(500, 46, true); g.fillStyle = "#1E1B18"; g.textAlign = "center"; g.fillText("the copycat?", w / 2, 404); g.textAlign = "left";
  });
  TEX.doorGlass = text(512, 540, (g, w, h) => {
    g.fillStyle = "rgba(220,224,226,.78)"; g.fillRect(0, 0, w, h); for (let i = 0; i < 2000; i++) { g.fillStyle = hash(i) > .5 ? "rgba(255,255,255,.18)" : "rgba(0,0,0,.05)"; g.fillRect(hash(i * 2.3) * w, hash(i * 5.1) * h, 3, 3); }
    g.save(); g.translate(w, 0); g.scale(-1, 1); g.textAlign = "center"; g.fillStyle = "#1E1B18"; g.font = SERIF(700, 64); g.fillText("J. KANE", w / 2, 200); g.font = FT(800, 30); g.fillText("PRIVATE INVESTIGATIONS", w / 2, 260); g.restore();
  });
  TEX.license = text(400, 300, (g, w, h) => { g.fillStyle = "#EFE8D8"; g.fillRect(0, 0, w, h); g.strokeStyle = "#8A7A5A"; g.lineWidth = 8; g.strokeRect(14, 14, w - 28, h - 28); g.textAlign = "center"; g.fillStyle = "#2A2420"; g.font = SERIF(700, 34); g.fillText("Licensed", w / 2, 100); g.font = SERIF(500, 26, true); g.fillText("Private Investigator", w / 2, 144); g.font = SERIF(700, 40); g.fillText("J. Kane", w / 2, 214); });
  TEX.clock = text(256, 256, (g) => { g.fillStyle = "#F4F1EA"; g.beginPath(); g.arc(128, 128, 124, 0, 7); g.fill(); g.strokeStyle = "#1E1B18"; g.lineWidth = 10; g.stroke(); for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; g.fillStyle = "#1E1B18"; g.fillRect(128 + Math.sin(a) * 100 - 5, 128 - Math.cos(a) * 100 - 5, 10, 10); } });
  TEX.cityNight = text(1024, 640, (g, w, h) => {
    g.fillStyle = "#0E1016"; g.fillRect(0, 0, w, h);
    for (let b = 0; b < 5; b++) { const x0 = b * 210 - 20, top = 60 + hash(b * 3.3) * 160; g.fillStyle = ["#1A1C24", "#22252E", "#181A20"][b % 3]; g.fillRect(x0, top, 200, h - top);
      for (let i = 0; i < 6; i++) for (let j = 0; j < 14; j++) { const lit = hash(b * 50 + i * 7 + j * 3) > .62; g.fillStyle = lit ? "rgba(255,240,215,.85)" : "rgba(60,64,72,.6)"; g.fillRect(x0 + 16 + i * 30, top + 20 + j * 34, 16, 20); } }
    g.save(); g.translate(720, 120); g.shadowColor = "#FFFFFF"; g.shadowBlur = 18; g.fillStyle = "#F4F4F4"; g.font = FT(800, 44); g.textAlign = "center"; "HOTEL".split("").forEach((c, i) => g.fillText(c, 0, i * 50)); g.restore();
  });
  TEX.signJune = text(920, 180, (g, w, h) => { g.clearRect(0, 0, w, h); g.textAlign = "center"; g.shadowColor = "#FFE9C8"; g.shadowBlur = 16; g.fillStyle = "#FFF4E2"; g.font = SERIF(700, 120, true); g.fillText("June's", w / 2 - 90, 125); g.shadowBlur = 0; g.font = FT(800, 40); g.fillText("BAKERY", w / 2 + 230, 118); });
  TEX.signRival = text(920, 180, (g, w, h) => { g.clearRect(0, 0, w, h); g.textAlign = "center"; g.fillStyle = "#F0F0F0"; g.font = FT(800, 104); g.fillText("CRUMB & CO.", w / 2, 128); });
  const awn = (a, b) => text(256, 64, (g, w, h) => { for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? a : b; g.fillRect(i * 32, 0, 32, h); } g.fillStyle = "rgba(0,0,0,.25)"; g.fillRect(0, h - 8, w, 8); });
  TEX.awnJune = awn("#E9E4DA", "#8C8880"); TEX.awnRival = awn("#3A3A3E", "#6A6A70");
  TEX.aframe = text(280, 400, (g, w, h) => { g.fillStyle = "#1E2422"; g.fillRect(0, 0, w, h); g.textAlign = "center"; g.fillStyle = "#F4F1E6"; g.font = SERIF(700, 46, true); g.fillText("June's", w / 2, 70); g.font = FT(800, 30); g.fillStyle = LAV; g.shadowColor = LAV; g.shadowBlur = 8; g.fillText("NEW TODAY", w / 2, 150); g.font = SERIF(700, 50, true); g.fillText("Lavender", w / 2, 220); g.fillText("croissant", w / 2, 276); g.shadowBlur = 0; g.fillStyle = "#F4F1E6"; g.font = FT(700, 26); g.fillText("Thursday", w / 2, 350); });
  TEX.bannerRival = text(1020, 240, (g, w, h) => { g.fillStyle = LAV; g.fillRect(0, 0, w, h); g.fillStyle = "#FFFFFF"; g.textAlign = "center"; g.font = FT(800, 92); g.fillText("NEW! LAVENDER", w / 2, 108); g.font = FT(800, 72); g.fillText("CROISSANT", w / 2, 196); });
  TEX.soldOut = text(320, 200, (g, w, h) => { g.fillStyle = "#F4F1EA"; g.fillRect(0, 0, w, h); g.strokeStyle = "#1E1B18"; g.lineWidth = 8; g.strokeRect(10, 10, w - 20, h - 20); label(g, "SOLD OUT", w / 2, 96, 52, "#1E1B18", "center"); label(g, "see you tomorrow", w / 2, 150, 26, "#3A3632", "center", 700); });
  jpM.map = text(140, 290, (g, w, h) => { g.fillStyle = "#120A1C"; g.fillRect(0, 0, w, h); block(g, 8, 40, w - 16, 200, LAV, 14); label(g, "CRUMB & CO.", w / 2, 78, 15, "#FFFFFF", "center"); label(g, "coming soon", w / 2, 108, 14, "#F2E6FF", "center", 700); label(g, "LAVENDER", w / 2, 150, 22, "#FFFFFF", "center"); label(g, "CROISSANT", w / 2, 178, 22, "#FFFFFF", "center"); label(g, "FRIDAY", w / 2, 222, 20, "#FFFFFF", "center"); });
  // ---- the laptop: 0 changedetection diff, 1 feeds, 2 reader, 3 Ollama briefing, 4 the 2 AM alert, 5 idle
  dyn("lap", 640, 400, (g, w, h, mode, u, blink) => {
    g.fillStyle = "#101114"; g.fillRect(0, 0, w, h);
    const bar = (s) => { g.fillStyle = "#1E2026"; g.fillRect(0, 0, w, 44); mono(g, s, 18, 30, 20, "#C9CDD4"); };
    if (mode === 0) {
      bar("changedetection.io  ·  crumbandco.com/menu");
      [["Croissant", "$4.25"], ["Pain au chocolat", "$4.00"], ["Cinnamon roll", "$4.50"], ["Sourdough loaf", "$8.00"], ["Coming soon page", "watched"]].forEach(([a, b], k) => {
        const y = 92 + k * 58; if (k === 0) { g.fillStyle = RED; g.fillRect(12, y - 34, w - 24, 50); }
        mono(g, a, 30, y, 26, "#FFFFFF"); mono(g, b, w - 30, y, 26, "#FFFFFF", "right"); });
      mono(g, "checks every 60 s  ·  5 pages", 30, h - 20, 20, "#8A8E96");
    } else if (mode === 1 || mode === 2) {
      bar(mode === 1 ? "RSSHub  ·  feeds" : "Miniflux  ·  12 unread");
      const items = mode === 1 ? ["Crumb & Co. · Instagram", "Crumb & Co. · blog", "Crumb & Co. · newsletter", "Crumb & Co. · menu page", "Crumb & Co. · reviews"] : ["New post: 'our new pastry'", "Menu page updated", "Blog: 'behind the counter'", "Newsletter: weekend special", "New post: storefront photo"];
      items.forEach((s, k) => { const y = 94 + k * 60; block(g, 18, y - 36, w - 36, 50, k === 0 && mode === 2 ? "#3A1A1A" : "#1A1C22", 8); g.fillStyle = k === 0 ? RED : "#5A5E66"; g.fillRect(30, y - 22, 14, 22); mono(g, s, 58, y - 4, 24, "#E9E4DA"); });
    } else if (mode === 3) {
      bar("Ollama  ·  local model");
      const L3 = ["7 AM BRIEFING", "1. Croissant price up 75 cents.", "2. Coming soon page, Friday:", "   LAVENDER CROISSANT"];
      const all = L3.join("\n"), n = Math.floor(all.length * u); let y = 96;
      all.slice(0, n).split("\n").forEach((s, i) => { mono(g, s, 24, y, 25, i === 3 ? LAV : "#E9E4DA"); y += 44; });
      if (blink) { g.fillStyle = "#E9E4DA"; g.fillRect(24 + g.measureText(all.slice(0, n).split("\n").pop()).width + 4, y - 74, 14, 26); }
    } else if (mode === 4) {
      g.fillStyle = blink ? "#C81E14" : "#A0140C"; g.fillRect(0, 0, w, h);
      mono(g, "ALERT  ·  2:00 AM", w / 2, 76, 34, "#FFFFFF", "center");
      mono(g, "Crumb & Co. changed prices", w / 2, 150, 30, "#FFFFFF", "center");
      g.fillStyle = "rgba(0,0,0,.25)"; g.fillRect(40, 186, w - 80, 86); mono(g, "Croissant  $3.50 -> $4.25", w / 2, 242, 34, "#FFFFFF", "center");
      mono(g, "detected in 58 seconds", w / 2, 334, 26, "#FFE0DC", "center");
    } else {
      g.fillStyle = "#16181E"; g.fillRect(0, 0, w, h); mono(g, "CASE 0417", w / 2, 180, 40, "#C9CDD4", "center"); mono(g, "CRUMB & CO.", w / 2, 232, 28, "#8A8E96", "center");
    }
  });
  dyn("kphone", 152, 312, (g, w, h, on) => {
    g.fillStyle = "#0E0F12"; g.fillRect(0, 0, w, h); label(g, "2:14", w / 2, 50, 30, "#C9CDD4", "center");
    if (on) { block(g, 8, 90, w - 16, 120, RED, 14); label(g, "HUGINN", w / 2, 122, 18, "#FFFFFF", "center"); label(g, "Crumb & Co.", w / 2, 156, 18, "#FFFFFF", "center"); label(g, "just posted", w / 2, 184, 16, "#FFE0DC", "center", 700); }
  });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  jpM.needsUpdate = true;
  TEX.ready = true;
}

const ready = (async () => {
  try { const jb = new FontFace("JBMono", "url(assets/fonts/jbmono-bold.ttf)", { weight: "700" }); document.fonts.add(await jb.load()); } catch (e) { /* fall back */ }
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 40px Manrope"), document.fonts.load("700 40px Garamond"), document.fonts.load("italic 700 40px Garamond")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  for (const k in SET) SET[k].visible = true;
  renderer.compile(scene, camera);
  renderAt(window.CC_COVER ? window.CC_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["copycat"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.CC_COVER ? window.CC_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C };
