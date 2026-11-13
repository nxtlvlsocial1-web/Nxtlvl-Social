// ChatGPT business skit (the tutorial skit format): Marcus, a real estate agent, at his desk with Byte, his floating AI
// sidekick, in one cozy office and one camera. The step-by-step app screen lives in the HTML layer above them; this file
// draws the 3D scene in the lower half of the frame. Everything is a pure function of time t, drawn on hf-seek.
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

// ================================================================= THE OFFICE (one room, one camera)
// Marcus sits behind his desk facing the camera (+z); Byte floats at his left shoulder (screen right). Back wall at z = -2.2
// with the listings wall and a window onto the evening street; the camera looks from z ~ 3.4.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const paperMat = (key) => { const m = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .8 }); LATE.push([m, key]); return m; };
const OF = mkSet("office");
const DESK = v3(0, 0, 0), MSEAT = v3(-.15, 0, -.7), BYTE0 = v3(.95, 1.55, -.35);
{
  const plank = pix(64, 64, (g) => { px(g, "#8E6440", 0, 0, 64, 64); for (let j = 0; j < 8; j++) { px(g, j % 2 ? "#865D3A" : "#966A44", 0, j * 8, 64, 8); px(g, "#6A4A2E", 0, j * 8, 64, 1); px(g, "#6A4A2E", (j * 23) % 64, j * 8, 1, 8); } }, false);
  flat(9, 7, new THREE.MeshStandardMaterial({ map: rep(plank, 5, 4), roughness: .6 }), 0, 0, 0);
  const wallM = mat(0xE7D8C4), trim = mat(0x5A3A26);
  box(9, 3.4, .2, wallM, 0, 1.7, -2.3); box(.2, 3.4, 7, wallM, -3.6, 1.7, .5); box(.2, 3.4, 7, wallM, 3.6, 1.7, .5); box(9, .12, 7, mat(0xF2E8DA), 0, 3.4, .5, { cast: false });
  box(9, .12, .06, trim, 0, .06, -2.18);
  // the listings wall (left) and a window onto the evening street (right)
  OF.wallP = paperMat("wall"); plane(2.6, 1.0, OF.wallP, -1.55, 1.95, -2.19, 0); box(2.7, 1.1, .03, trim, -1.55, 1.95, -2.2);
  box(1.7, 1.3, .05, trim, 1.8, 1.95, -2.18); OF.winM = texMat("windowEve", { transparent: false }); plane(1.55, 1.15, OF.winM, 1.8, 1.95, -2.15, 0);
  box(1.7, .06, .2, trim, 1.8, 1.27, -2.1);
  // the desk with Marcus's laptop, a lamp, a plant, a nameplate, a model house
  box(1.9, .07, .9, mat(0x6A4A30, { roughness: .4 }), DESK.x, .76, DESK.z); for (const s of [-1, 1]) box(.07, .73, .8, mat(0x4A3424), DESK.x + s * .9, .37, DESK.z);
  box(1.8, .55, .05, mat(0x4A3424), DESK.x, .45, DESK.z + .42);
  const lap = new THREE.Group(); lap.position.set(-.2, .8, .05); OF.add(lap);
  box(.4, .02, .27, metal(0xB8BCC4, .35), 0, .01, -.1, { parent: lap });
  const lid = new THREE.Group(); lid.position.z = .03; lid.rotation.x = .32; lap.add(lid); box(.4, .26, .012, metal(0xB8BCC4, .35), 0, .13, 0, { parent: lid });
  OF.lampShade = mat(0xF2C94C, { emissive: 0xFFC98A, emissiveIntensity: .9, roughness: .4 });
  cyl(.08, .1, .03, metal(0x2A2A2E, .4), .7, .8, -.15, 14); cyl(.012, .012, .34, metal(0x2A2A2E, .4), .7, .97, -.15, 8); cyl(.07, .15, .14, OF.lampShade, .7, 1.16, -.1, 16);
  cyl(.07, .06, .1, mat(0xC9644E), -.75, .84, .2, 10); box(.16, .2, .16, mat(0x4E8C48), -.75, 1.0, .2); box(.1, .12, .1, mat(0x5E9C52), -.73, 1.15, .22);
  box(.36, .09, .05, mat(0x1C2A4A), .25, .84, .38, { rx: -.3 }); OF.nameM = texMat("nameplate", { transparent: false }); plane(.34, .07, OF.nameM, .25, .845, .41, 0).rotation.x = -.3;
  { const h = new THREE.Group(); h.position.set(.35, .8, -.25); OF.add(h); box(.2, .14, .18, mat(0xF4F1EA), 0, .07, 0, { parent: h }); box(.24, .04, .21, mat(0xB5654A), 0, .16, 0, { parent: h }); }
  cyl(.045, .04, .09, mat(0xF4EFE6), .48, .845, .15, 12);
  // the chair, a shelf with binders, a floor plant, a rug
  box(.55, .08, .5, mat(0x23345E), MSEAT.x, .5, MSEAT.z - .05); box(.55, .7, .1, mat(0x23345E), MSEAT.x, .9, MSEAT.z - .32);
  box(1.2, .05, .3, trim, -2.6, 1.4, -2.05); for (let k = 0; k < 5; k++) box(.12, .32, .24, mat(["#2F6F5E", "#1C2A4A", "#B5654A", "#F2C94C", "#7A4A2A"][k]), -3.0 + k * .2, 1.6, -2.05);
  cyl(.22, .18, .4, mat(0xC9644E), 2.9, .2, -1.6, 12); for (let j = 0; j < 4; j++) box(.38 - j * .06, .34, .38 - j * .06, mat(j % 2 ? 0x4E7A3E : 0x5E8C48), 2.9, .55 + j * .3, -1.6);
  flat(3.2, 2.2, mat(0x7A2E2E, { roughness: .95 }), 0, .005, -.2);
  OF.warm = new THREE.PointLight(0xFFD9A0, 0, 6, 1.6); OF.warm.position.set(.7, 1.6, .2); scene.add(OF.warm);
  OF.fill = new THREE.PointLight(0xFFE9CC, 0, 9, 1.4); OF.fill.position.set(-1.2, 2.8, 2.0); scene.add(OF.fill);
  OF.rim = new THREE.PointLight(0xB9A6FF, 0, 4, 1.8); scene.add(OF.rim);
}
// ---------------------------------------------------------------- Byte: a floating violet robot with a screen face
const BYTE = new THREE.Group(); OF.add(BYTE);
{
  const shell = new THREE.MeshPhysicalMaterial({ color: 0x8B5CF6, roughness: .3, clearcoat: .8, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .6 });
  const head = new THREE.Mesh(new RoundedBoxGeometry(.5, .42, .42, 4, .1), shell); head.castShadow = true; BYTE.add(head);
  box(.42, .32, .01, mat(0x0B0D12, { roughness: .2 }), 0, 0, .209, { parent: BYTE });
  BYTE.faceM = new THREE.MeshBasicMaterial({ color: 0xB8B8B8 });       // tone-mapped and a little dim, so the glow doesn't swallow the face
  const face = new THREE.Mesh(new THREE.PlaneGeometry(.4, .3), BYTE.faceM); face.position.z = .222; BYTE.add(face);
  for (const s of [-1, 1]) { cyl(.07, .07, .05, mat(0xE9E4DA, { roughness: .4 }), s * .27, 0, 0, 16, { parent: BYTE }).rotation.z = Math.PI / 2; }
  cyl(.012, .012, .16, metal(0xD9D9DE, .3), 0, .29, 0, 8, { parent: BYTE });
  BYTE.tip = new THREE.Mesh(new THREE.SphereGeometry(.035, 12, 10), glow(0x5BE3B0)); BYTE.tip.position.y = .38; BYTE.add(BYTE.tip);
  BYTE.ring = new THREE.Mesh(new THREE.TorusGeometry(.2, .012, 8, 40), new THREE.MeshBasicMaterial({ color: 0x5BE3B0, transparent: true, opacity: .55, toneMapped: false })); BYTE.ring.rotation.x = Math.PI / 2; BYTE.ring.position.y = -.33; BYTE.add(BYTE.ring);
}
PARENT = scene;

// ---------------------------------------------------------------- Marcus
const MARCUS = makeChar({ id: "marcus", skin: "#8E5E40", hair: "#1E1B18", style: "short", beard: "#1E1B18", top: "#23345E", topStyle: "blazer", pants: "#2E3A55", shoe: "#1E1B18" }, OF);
MARCUS.seed = 2.4;

// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
const who = (t, name) => C.who.some((w, k) => w === name && t > L[k] - .05 && t < E[k] + .02);
const lineAt = (t) => C.who.findIndex((w, k) => t > L[k] - .05 && t < E[k] + .05);
const v = (x, y, z) => new THREE.Vector3(x, y, z);
const SITY = .52 - .71;

// ---------------------------------------------------------------- the cast
function updMarcus(t) {
  const k = lineAt(t), byteTalks = who(t, "byte"), meTalks = who(t, "marcus");
  const p = pose({ x: MSEAT.x, y: SITY, z: MSEAT.z, ry: .12, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.95, .18, 1.25], [.95, .18, 1.25]], hp: .12 });
  let f = { eyes: "open", mouth: "flat", brows: "flat", talk: meTalks };
  if (byteTalks || (k < 0 && t > L[C.tk["04"]])) { p.hy = -.55; p.hp = .05; f = { eyes: "open", mouth: "flat", brows: "raise1" }; }   // listening to Byte
  if (meTalks) { p.hy = -.35; p.hp = 0; }
  if (k === 0) { p.a = [[1.6, .55, 1.0 + .2 * Math.sin(t * 6)], [1.6, .55, 1.0 + .2 * Math.sin(t * 6 + 1)]]; f = { eyes: "wide", mouth: "o", brows: "angry", talk: true, noblink: true }; }
  if (k === C.tk["15"]) { p.a[1] = [2.0, .1, 2.2]; f = { eyes: "closed", mouth: "sad", brows: "worry", talk: true }; }   // a hand over his face
  if (k === C.tk["17"]) f = { eyes: "open", mouth: "smile", brows: "up", talk: true };
  if (k >= C.tk["19"] || t > E[C.tk["19"]]) { f = { eyes: "happy", mouth: "grin", brows: "up", talk: meTalks }; p.a[0] = [1.3, .3, .5]; }
  // typing while Byte walks through a step
  if (byteTalks && C.stepLines.includes(k)) { p.a = [[1.1, .12, 1.05 + .08 * Math.sin(t * 13)], [1.1, .12, 1.05 + .08 * Math.sin(t * 11 + 1)]]; p.hy = -.15; p.hp = .22; }
  placeChar(MARCUS, true, idle(p, t, MARCUS.seed), f);
}
function updByte(t) {
  const talks = who(t, "byte"), listen = who(t, "marcus"), k = lineAt(t);
  BYTE.position.set(BYTE0.x + .03 * Math.sin(t * .7), BYTE0.y + .05 * Math.sin(t * 1.9), BYTE0.z);
  const yaw = listen ? -.75 : (talks ? -.12 : -.35);
  BYTE.rotation.set(.04 * Math.sin(t * 1.3), lerp(BYTE.rotation.y || yaw, yaw, .5), .04 * Math.sin(t * 1.1));
  BYTE.rotation.y = yaw + .04 * Math.sin(t * .9);
  BYTE.ring.rotation.z = t * 1.5; BYTE.ring.material.opacity = .4 + .2 * Math.sin(t * 4);
  BYTE.tip.scale.setScalar(1 + (talks ? .25 * Math.abs(Math.sin(t * 9)) : .08 * Math.sin(t * 3)));
  const eyes = k === C.tk["20"] || k === C.tk["16"] ? "smug" : (k === C.tk["18"] ? "open" : (listen ? "open" : "calm"));
  const lv = talks ? Math.floor(t * 12) % 6 : -1;
  setMap(BYTE.faceM, DYN.byteFace(eyes, lv, Math.floor(t * 2.4 + 1) % 9 === 0 ? 1 : 0));
}

// ---------------------------------------------------------------- one camera, a slow push; it leans in on Marcus when he talks
const CAM = { p0: v(.25, 1.8, 3.9), p1: v(.2, 1.74, 3.45), l0: v(.35, 2.38, -.5), dM: v(-.16, -.03, -.38), lM: v(-.2, -.05, 0) };
const sst = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const marcusW = (t) => C.who.reduce((w, n, k) => n === "marcus" ? Math.max(w, sst((t - L[k] + .15) / .5) * sst((E[k] + .35 - t) / .5)) : w, 0);
function renderAt(t) {
  if (!TEX.ready) return;
  NOW = t;
  for (const kk in SET) SET[kk].visible = true;
  for (const l of PL) l.intensity = 0;
  scene.background = tmpC.set(0x2A1E16).clone(); scene.fog.color.set(0x2A1E16); scene.fog.near = 20; scene.fog.far = 60;
  hemi.color.set(0xFFE9CC); hemi.groundColor.set(0x5A3A26); hemi.intensity = .75;
  sun.color.set(0xFFD9A0); sun.intensity = 1.2;
  OF.warm.intensity = 3.2; OF.fill.intensity = 3.0;
  OF.rim.position.copy(BYTE.position).add(v(0, .1, .4)); OF.rim.intensity = 1.2;
  updMarcus(t); updByte(t);
  const u = sm(clamp(t / DUR));
  const cv = window.SK_COVER;
  const wm = t < E[0] + .3 ? 0 : marcusW(t);
  camera.position.lerpVectors(CAM.p0, CAM.p1, u).addScaledVector(CAM.dM, wm).add(V.set(Math.sin(t * .8) * .004, Math.sin(t * 1.2) * .004, 0));
  camera.fov = 50;
  const look = CAM.l0.clone().addScaledVector(CAM.lM, wm);
  if (cv && cv.cam) { camera.position.set(...cv.cam); look.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix(); camera.up.set(0, 1, 0); camera.lookAt(look);
  scene.updateMatrixWorld(true);
  cocPass.uniforms.uF.value = camera.position.distanceTo(v(.2, 1.4, -.5)); cocPass.uniforms.uAp.value = .05;
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = .18; gu.uCool.value = 0; gu.uSat.value = 1.02; gu.uCon.value = .06; gu.uVig.value = .42; gu.uTint.value = 0;
  gu.uFlash.value = 0; gu.uCA.value = .0008; gu.uKeep.value = 0; gu.uGrain.value = .02; gu.uTop.value = cv ? 0 : .35; gu.uDark.value = 0;
  bloom.strength = .3;
  sun.target.position.set(0, 0, -1); sun.position.copy(sun.target.position).add(S.set(.5, 1.6, 1.2).normalize().multiplyScalar(20));
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 50 });
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures that need the fonts
const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, SERIF = (w, f, it = false) => `${it ? "italic " : ""}${w} ${f}px Garamond, serif`;
const text = (w, h, draw) => pix(w, h, draw, false);
const label = (g, s, x, y, f, c, al = "left", wt = 800) => { g.font = FT(wt, f); g.fillStyle = c; g.textAlign = al; g.fillText(s, x, y); g.textAlign = "left"; };
const DYN = {};
function dyn(key, w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  let last = null;
  DYN[key] = (...a) => { const k = a.join("|"); if (k !== last) { last = k; draw(g, w, h, ...a); tx.needsUpdate = true; } return tx; };
}
function buildTextures() {
  const house = (g, x, y, w, h, k) => { const roof = ["#B5654A", "#5E6470", "#7A4A2A", "#2F6F5E", "#8C3B3B", "#4A5A7A"][k % 6], wall = ["#F4EFE6", "#E8D9BE", "#DCE6EE", "#F2E3C9", "#E9E4DA", "#F7F1E3"][k % 6];
    g.fillStyle = "#BFE0F7"; g.fillRect(x, y, w, h * .62); g.fillStyle = "#7DBA6A"; g.fillRect(x, y + h * .62, w, h * .38);
    g.fillStyle = wall; g.fillRect(x + w * .2, y + h * .34, w * .6, h * .38); g.fillStyle = roof; g.beginPath(); g.moveTo(x + w * .14, y + h * .36); g.lineTo(x + w * .5, y + h * .12); g.lineTo(x + w * .86, y + h * .36); g.fill();
    g.fillStyle = "#3A3A3A"; g.fillRect(x + w * .45, y + h * .52, w * .1, h * .2); };
  TEX.wall = text(920, 340, (g, w, h) => { g.fillStyle = "#F4F1EA"; g.fillRect(0, 0, w, h); label(g, "OUR LISTINGS", 24, 44, 32, "#1C2A4A"); for (let k = 0; k < 8; k++) { const x = 24 + (k % 4) * 224, y = 64 + Math.floor(k / 4) * 136; g.fillStyle = "#FFFFFF"; g.fillRect(x, y, 208, 124); house(g, x + 6, y + 6, 196, 90, k); label(g, k % 3 ? "FOR SALE" : "SOLD", x + 10, y + 116, 18, k % 3 ? "#1C2A4A" : "#D9483B"); } });
  TEX.windowEve = text(512, 384, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#3B4A7A"); gr.addColorStop(.6, "#E8956A"); gr.addColorStop(1, "#F2C27A"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let b = 0; b < 6; b++) { const x0 = b * 90 - 10, top = 140 + (b * 37 % 90); g.fillStyle = ["#2A2440", "#352C4E", "#2E2846"][b % 3]; g.fillRect(x0, top, 80, h - top); for (let i = 0; i < 3; i++) for (let j = 0; j < 6; j++) { g.fillStyle = (b * 7 + i * 3 + j) % 3 ? "#FFD9A0" : "#4A4266"; g.fillRect(x0 + 10 + i * 22, top + 14 + j * 30, 12, 16); } }
    g.fillStyle = "rgba(255,255,255,.15)"; g.fillRect(w / 2 - 3, 0, 6, h); g.fillRect(0, h / 2 - 3, w, 6); });
  TEX.nameplate = text(340, 70, (g, w, h) => { g.fillStyle = "#1C2A4A"; g.fillRect(0, 0, w, h); label(g, "MARCUS · KEYSTONE REALTY", w / 2, 46, 24, "#F2C94C", "center"); });
  // Byte's face: two eyes and a row of mouth bars that bounce while it talks
  dyn("byteFace", 256, 192, (g, w, h, eyes, lv, blink) => {
    g.fillStyle = "#0B0D12"; g.fillRect(0, 0, w, h);
    g.shadowColor = "#5BE3B0"; g.shadowBlur = 16; g.fillStyle = "#7CF2C8"; g.strokeStyle = "#7CF2C8"; g.lineWidth = 12; g.lineCap = "round";
    for (const ex of [82, 174]) {
      if (blink) { g.beginPath(); g.moveTo(ex - 18, 70); g.lineTo(ex + 18, 70); g.stroke(); }
      else if (eyes === "smug") { g.beginPath(); g.moveTo(ex - 20, 66); g.lineTo(ex + 20, 66); g.stroke(); g.fillRect(ex - 20, 66, 40, 12); }
      else if (eyes === "calm") { g.beginPath(); g.ellipse(ex, 70, 18, 12, 0, 0, 7); g.fill(); }
      else { g.beginPath(); g.ellipse(ex, 68, 16, 22, 0, 0, 7); g.fill(); }
    }
    const bars = [.35, .7, 1, .6, .3];
    for (let i = 0; i < 5; i++) {
      const hh = lv < 0 ? 6 : 8 + 34 * bars[(i + lv) % 5] * (.6 + .4 * ((lv * 7 + i * 3) % 5) / 4);
      g.fillRect(84 + i * 20, 140 - hh / 2, 10, hh);
    }
    g.shadowBlur = 0;
  });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  TEX.ready = true;
}

const ready = (async () => {
  try { const jb = new FontFace("JBMono", "url(assets/fonts/jbmono-bold.ttf)", { weight: "700" }); document.fonts.add(await jb.load()); } catch (e) { /* fall back */ }
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 40px Garamond")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  for (const k in SET) SET[k].visible = true;
  renderer.compile(scene, camera);
  renderAt(window.SK_COVER ? window.SK_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["skit"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.SK_COVER ? window.SK_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C };
