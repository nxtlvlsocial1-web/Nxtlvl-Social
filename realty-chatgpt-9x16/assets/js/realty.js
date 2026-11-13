// Real estate what-if: "What if ChatGPT sent all your clients to your competitor?" A what-if in the house voxel style, in
// full colour on a bright town morning. Keystone Realty is empty while every house hunter asks ChatGPT for an agent and a
// floating answer card says Prime Nest. Junior agent Lena claims the agency in Business Hub (the four steps float up as
// holograms over the front desk); a blue check snaps onto the sign, the answer cards flip, and the crowd crosses back.
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

// ================================================================= THE STREET AND THE OFFICE
// The street runs along x. Keystone Realty is on the north side (front at z = -4.3, facing +z) with a deep office behind its
// window (to z = -8.6); Prime Nest Realty is across the road (front at z = 4.3, facing -z). Sidewalks at z = +-3.6.
const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); g.visible = false; scene.add(g); SET[k] = g; PARENT = g; return g; };
function v3(x, y, z) { return new THREE.Vector3(x, y, z); }
const paperMat = (key) => { const m = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .8 }); LATE.push([m, key]); return m; };
const FX = -1.0, BX = 1.2;                       // the two shops' centres along x
const FDOOR = v3(FX - 2.7, 0, -4.3), BDOOR = v3(BX - 2.6, 0, 4.3);
const COUNTER = v3(FX + 2.6, 0, -7.6), LAPP = v3(FX + 2.45, 1.06, -7.55);
const ST = mkSet("street");
{
  const road = new THREE.MeshStandardMaterial({ map: rep(ASPH, 12, 4), color: 0xB8BCC4, roughness: .85 });
  flat(44, 5.6, road, 0, -.04, 0);
  for (let k = -7; k < 8; k++) box(1.2, .01, .12, mat(0xF4EFE6), k * 3, -.03, 0, { cast: false });
  for (const s of [-1, 1]) { flat(44, 1.6, groundMat(CONC, 16, 1), 0, .1, s * 3.6); box(44, .14, .16, mat(0xA8A39A), 0, .05, s * 2.82); }
  const brick = (c1, c2, c3) => pix(64, 64, (g) => { px(g, c1, 0, 0, 64, 64); for (let j = 0; j < 8; j++) for (let i = 0; i < 4; i++) px(g, [c1, c2, c3][(i + j) % 3], i * 16 + (j % 2) * 8, j * 8, 15, 7); }, false);
  const brickA = new THREE.MeshStandardMaterial({ map: rep(brick("#B5654A", "#A85A42", "#C27056"), 8, 4), roughness: .9 });
  const brickB = new THREE.MeshStandardMaterial({ map: rep(brick("#5E6470", "#555B66", "#686E7A"), 8, 4), roughness: .9 });
  const winM = new THREE.MeshStandardMaterial({ color: 0x9FC4DE, roughness: .15, metalness: .3, envMap: ENV, envMapIntensity: .9 });
  // a shopfront: brick above, a big window, a door, an awning and the sign
  const front = (side, x0, bm, signKey, awnKey, deep) => {
    const z = side * 4.3, f = -side;
    box(9, 5.6, .3, bm, x0, 6.2, z + side * .15);
    for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) box(1.0, 1.2, .05, winM, x0 - 3.2 + c * 2.1, 4.6 + r * 1.6, z + f * .02);
    box(9, .5, .3, mat(0x2A2622), x0, .25, z); box(9, .35, .32, mat(0x2A2622), x0, 3.2, z);
    const glass = new THREE.MeshPhysicalMaterial({ color: 0xCFE2EE, roughness: .04, transparent: true, opacity: .1, envMap: ENV, envMapIntensity: 1, depthWrite: false });
    plane(5.6, 2.5, glass, x0 + .9, 1.75, z + f * .01, side < 0 ? 0 : Math.PI);
    for (const dx of [-2.0, .9, 3.8]) box(.1, 2.6, .2, mat(0x2A2622), x0 + dx, 1.75, z);
    box(1.3, 3.0, .3, bm, x0 - 3.85, 1.5, z + side * .15);                                    // wall beside the doorway (x0-3.2 .. x0-2.0 is the open door)
    const sign = texMat(signKey); plane(4.6, .9, sign, x0, 2.75, z + f * .2, side < 0 ? 0 : Math.PI);
    const awn = texMat(awnKey, { transparent: false }); const a = plane(5.8, 1.0, awn, x0 + .9, 3.1, z + f * .55, side < 0 ? 0 : Math.PI); a.rotation.x = side < 0 ? -.75 : .75;
    const inM = mat(0xE9E2D3), d = deep;
    box(9, 3.4, .2, inM, x0, 1.7, z - f * d); for (const dx of [-4.5, 4.5]) box(.2, 3.4, d, inM, x0 + dx, 1.7, z - f * d / 2); box(9, .1, d, mat(0xF4EFE6), x0, 3.4, z - f * d / 2);
    const tile = pix(32, 32, (g) => { for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) px(g, (i + j) % 2 ? "#1E1B18" : "#F4F1EA", i * 8, j * 8, 8, 8); });
    flat(9, d, new THREE.MeshStandardMaterial({ map: rep(tile, 9, d), roughness: .4 }), x0, .02, z - f * d / 2);
    // a FOR SALE yard sign by the door, and listing posters in the window
    const ys = new THREE.Group(); ys.position.set(x0 - 3.45, 0, z + f * .55); ST.add(ys);
    box(.07, 1.5, .07, mat(0xF4F1EA), 0, .75, 0, { parent: ys }); box(.8, .06, .06, mat(0xF4F1EA), .35, 1.45, 0, { parent: ys });
    const sale = new THREE.Group(); sale.position.set(.4, 1.12, 0); ys.add(sale); const sm = paperMat(side < 0 ? "saleKey" : "salePrime");
    const sp = new THREE.Mesh(new THREE.PlaneGeometry(.7, .5), sm); sp.rotation.y = side < 0 ? 0 : Math.PI; sale.add(sp);
    for (let q = 0; q < 3; q++) { const pm = paperMat("listing" + ((q + (side < 0 ? 0 : 3)) % 6)); plane(.8, 1.0, pm, x0 - .9 + q * 1.5, 1.55, z - f * .06, side < 0 ? 0 : Math.PI); }
    return { sale, sign };
  };
  ST.f = front(-1, FX, brickA, "signKey", "awnKey", 4.3);
  ST.b = front(1, BX, brickB, "signPrime", "awnPrime", 2.3);
  // the blue check that snaps onto Keystone's sign
  ST.checkM = texMat("check"); ST.check = plane(.62, .62, ST.checkM, FX + 2.55, 2.78, -4.08, 0);
  ST.checkB = plane(.5, .5, texMat("check"), BX - 2.5, 2.78, 4.08, Math.PI);
  // neighbours, sky, trees, lamps
  for (const [x, z, s] of [[-14.5, -4.5, -1], [14, -4.5, -1], [-13.8, 4.5, 1], [14.5, 4.5, 1]]) box(19, 12, .3, s < 0 ? brickB : brickA, x, 6, z);
  for (const x of [-9, 6.5]) for (const s of [-1, 1]) { const zz = s * 3.15; cyl(.07, .09, 1.6, mat(0x5A4030), x, .8, zz, 8); box(1.1, 1.0, 1.1, mat(0x4E8C48), x, 2.0, zz); box(.8, .7, .8, mat(0x5E9C52), x + .1, 2.7, zz + .05); }
  ST.sky = new THREE.Mesh(new THREE.SphereGeometry(120, 24, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.BackSide, fog: false, toneMapped: false })); ST.add(ST.sky); LATE.push([ST.sky.material, "sky"]);
  // inside Keystone Realty: two agent desks with monitors, a wall of listings, the front desk with Lena's laptop, a sofa
  const BW = -8.5;
  plane(4.6, 1.7, paperMat("wall"), FX - 1.3, 1.85, BW + .02, 0);                               // the listings wall
  for (let k = 0; k < 2; k++) {
    const x = FX - 2.6 + k * 2.4, z = -6.6;
    box(1.4, .06, .7, mat(0xF4F1EA, { roughness: .4 }), x, .76, z); for (const s of [-1, 1]) box(.06, .73, .6, mat(0x2A2622), x + s * .65, .37, z);
    box(.6, .38, .04, mat(0x15171C), x, 1.08, z - .2); box(.08, .14, .08, mat(0x15171C), x, .85, z - .2); box(.54, .32, .01, glow(0x9FC4DE), x, 1.08, z - .177);
    box(.5, .08, .5, mat(0x23345E), x, .5, z + .55); box(.5, .55, .08, mat(0x23345E), x, .8, z + .78);
  }
  box(1.6, 1.0, .7, mat(0x2A2622), COUNTER.x, .5, COUNTER.z); box(1.7, .06, .8, mat(0xD9CDB6, { roughness: .4 }), COUNTER.x, 1.03, COUNTER.z);
  const lap = new THREE.Group(); lap.position.copy(LAPP); lap.rotation.y = Math.PI - .5; ST.add(lap);
  box(.38, .018, .26, metal(0xB8BCC4, .35), 0, .009, .13, { parent: lap });
  const lid = new THREE.Group(); lid.rotation.x = -.3; lap.add(lid); box(.38, .25, .012, metal(0xB8BCC4, .35), 0, .125, -.007, { parent: lid });
  ST.lapM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }); const ls = new THREE.Mesh(new THREE.PlaneGeometry(.35, .22), ST.lapM); ls.position.set(0, .128, 0); lid.add(ls);
  box(2.4, .45, .55, mat(0x2E4057), FX - 1.0, .23, -5.1); box(2.4, .5, .1, mat(0x2E4057), FX - 1.0, .7, -5.36);   // the sofa by the window
  // a little model house on the front desk
  { const h = new THREE.Group(); h.position.set(COUNTER.x - .5, 1.06, COUNTER.z + .1); ST.add(h); box(.3, .2, .26, mat(0xF4F1EA), 0, .1, 0, { parent: h }); box(.34, .05, .3, mat(0xB5654A), 0, .24, 0, { parent: h, rz: .0 }); box(.08, .1, .02, mat(0x23345E), 0, .05, .135, { parent: h }); }
  for (let k = 0; k < 2; k++) cyl(.18, .14, .3, mat(0xC9644E), FX + 3.7 - k * 8.2, .15, -5.0, 12), box(.3, .6, .3, mat(0x4E8C48), FX + 3.7 - k * 8.2, .6, -5.0);
  ST.inL = new THREE.PointLight(0xFFF2DC, 0, 9, 1.4); ST.inL.position.set(FX, 3.0, -6.4); scene.add(ST.inL);
  ST.inL2 = new THREE.PointLight(0xFFF2DC, 0, 7, 1.4); ST.inL2.position.set(FX + 2.5, 2.6, -7.0); scene.add(ST.inL2);
  // the four steps as holograms over the counter
  ST.holo = [0, 1, 2, 3].map((k) => { const m = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, toneMapped: false, depthWrite: false, side: THREE.DoubleSide }); LATE.push([m, "holo" + k]); const p = new THREE.Mesh(new THREE.PlaneGeometry(.95, .6), m); ST.add(p); return p; });
  // the crowd, and the ChatGPT answer card floating over each phone
  ST.crowd = Array.from({ length: 12 }, (_, i) => npc(60 + i * 5, ST));
  ST.phones = ST.crowd.map(() => { const g = new THREE.Group(); ST.add(g); box(.07, .14, .012, mat(0x15171C), 0, 0, 0, { parent: g }); return g; });
  ST.cardMs = [], ST.cards = ST.crowd.map((_, i) => { const m = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, depthWrite: false }); ST.cardMs.push(m); const p = new THREE.Mesh(new THREE.PlaneGeometry(1.1, .5), m); ST.add(p); return p; });
}
PARENT = scene;

// ---------------------------------------------------------------- the cast
const MARCUS = makeChar({ id: "marcus", skin: "#8E5E40", hair: "#1E1B18", style: "short", beard: "#1E1B18", top: "#23345E", topStyle: "blazer", pants: "#2E3A55", shoe: "#1E1B18" }, ST);
MARCUS.seed = 2.4;
const LENA = makeChar({ id: "lena", skin: "#C68E68", hair: "#2A1A12", style: "bob", top: "#2F6F5E", topStyle: "blazer", pants: "#3A3A3A", shoe: "#1E1B18", lash: true, earring: true }, ST);
LENA.seed = 4.1;
const RIVAL = makeChar({ id: "rival", skin: "#F0C49C", hair: "#B88A4A", style: "short", top: "#3A3A3A", topStyle: "blazer", pants: "#1E1B18", shoe: "#1E1B18", glasses: "#1E1B18" }, ST);
RIVAL.seed = 6.6;
const INS = [npc(140, ST), npc(147, ST)];                                         // two customers inside at the end
const LPHONE = new THREE.Group(); ST.add(LPHONE); box(.075, .15, .012, mat(0x15171C), 0, 0, 0, { parent: LPHONE });

// ---------------------------------------------------------------- cue times (window.CT, from build/generate.py)
// lines: 0 Marcus "my phone is dead silent" | 1 Lena "they're all asking ChatGPT" | 2 Marcus "Prime Nest?!" | 3 Lena "we didn't. Watch."
//        4 Lena the four steps | 5 Marcus "a blue check?" | 6 Lena "launched Nov 10, free" | 7 Marcus "who's buying?" | 8 Lena CTA
const IN0 = C.inside, CK = C.check, FL = C.flip, NX = C.next;
const who = (t, name) => C.who.some((w, k) => w === name && t > L[k] - .05 && t < E[k] + .02);
// 0 the street, an empty office | 1 inside, the fix | 2 the blue check | 3 the crowd crosses back | 4 a full office
const sceneOf = (t) => (t < IN0 ? 0 : t < CK ? 1 : t < FL ? 2 : t < NX ? 3 : 4);
const v = (x, y, z) => new THREE.Vector3(x, y, z);

// ---------------------------------------------------------------- the cast
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
const PHONEUP = [[1.45, .05, 1.55], [.15, .1, .25]];
const CROSS = [[.9, .55, 2.1], [.9, .55, 2.1]];                // arms folded
const BQ = (i) => [BDOOR.x + .7 + i * .72, 3.3];                // the queue outside Prime Nest
const FQ = (i) => [FDOOR.x + .9 + i * .74, -3.3];               // the queue outside Keystone
const CARDFLIP = (i) => FL + .25 + i * .07;
function updCrowd(t, s, cam) {
  ST.crowd.forEach((P, i) => {
    const ph = ST.phones[i], card = ST.cards[i];
    let x, z, ry, walking = false, phoneUp = true;
    if (t < FL) {
      const u = clamp((t + 1.5 - i * .42) / 7.5), x0 = -15 + i * 1.1, [qx, qz] = BQ(i);
      const a = along([[x0, -3.25], [x0 + 5.5, -3.25], [qx - .4, .4], [qx, qz]], u); x = a.x; z = a.z; ry = u < 1 ? a.ry : -Math.PI / 2; walking = u < 1;
    } else {
      const u = clamp((t - FL - .45 - i * .16) / 3.0), [bx, bz] = BQ(i), [fx, fz] = FQ(i);
      const a = along([[bx, bz], [bx - .2, 1.0], [fx + .3, -2.0], [fx, fz]], u); x = a.x; z = a.z; ry = u > 0 && u < 1 ? a.ry : (u <= 0 ? -Math.PI / 2 : -Math.PI / 2); walking = u > 0 && u < 1;
      if (s === 4) phoneUp = false;
    }
    let p = pose({ x, z, ry, a: phoneUp ? PHONEUP : [[.12, .1, .2], [.12, .1, .2]], hp: phoneUp ? .25 : 0 });
    if (walking) { const a0 = p.a; p = walk(p, t * 8.5 + i * 1.3, .9); if (phoneUp) p.a = [a0[0], p.a[1]]; }
    placeChar(P, true, idle(p, t, P.seed), { eyes: "open", mouth: s >= 3 && t > CARDFLIP(i) ? "smile" : "flat", brows: "flat" });
    ph.visible = phoneUp; if (phoneUp) holdAt(P, 0, ph, [0, -.06, .07]);
    // the answer card floats over the phone and faces the camera; it flips from Prime Nest to Keystone
    const flip = CARDFLIP(i), fu = clamp((t - flip) / .3);
    card.visible = phoneUp && s !== 1;
    if (card.visible) {
      card.position.set(x, 2.45 + .03 * Math.sin(t * 2 + i), z); card.quaternion.copy(cam.quaternion);
      card.scale.set(Math.max(.02, Math.abs(Math.cos(fu * Math.PI))), 1, 1);
      setMap(ST.cardMs[i], TEX[fu < .5 ? "cardPrime" : "cardKey"]);
    }
  });
  INS.forEach((P, k) => {
    if (s !== 4) { P.root.visible = false; return; }
    placeChar(P, true, idle(pose({ x: FX - 1.6 + k * .9, y: .52 - .71 - .25, z: -5.0, ry: Math.PI, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.4, .1, .6], [.4, .1, .6]] }), t, P.seed), { eyes: "open", mouth: "smile", brows: "up" });
  });
}
function updCast(t, s) {
  LPHONE.visible = false;
  // Dev
  if (s === 0) placeChar(MARCUS, true, idle(pose({ x: FDOOR.x + .1, z: FDOOR.z + .55, ry: .35, a: t > L[2] - .1 && t < E[2] + .2 ? [[1.4, .5, 1.2], [1.4, .5, 1.2]] : CROSS }), t, MARCUS.seed),
    t > L[2] - .2 && t < E[2] + .3 ? { eyes: "wide", mouth: "o", brows: "angry", talk: who(t, "marcus"), noblink: true } : { eyes: "half", mouth: "flat", brows: "worry", talk: who(t, "marcus") });
  else if (s === 1) placeChar(MARCUS, true, idle(pose({ x: COUNTER.x - 1.5, z: COUNTER.z + 1.3, ry: 2.4, a: CROSS, hp: -.05 }), t, MARCUS.seed), { eyes: "open", mouth: "flat", brows: "raise1" });
  else if (s === 2 || s === 3) placeChar(MARCUS, true, idle(pose({ x: FDOOR.x + .1, z: FDOOR.z + .55, ry: s === 2 ? -.4 : .2, hp: s === 2 ? -.35 : 0, a: s === 3 ? [[2.3, .2, .3], [.2, .1, .3]] : [[.3, .2, .5], [.3, .2, .5]] }), t, MARCUS.seed),
    { eyes: s === 2 ? "wide" : "happy", mouth: s === 2 ? "o" : "grin", brows: "up", talk: who(t, "marcus"), noblink: s === 2 });
  else placeChar(MARCUS, true, idle(pose({ x: FX - 1.3, z: -7.45, ry: .45, a: t > L[7] - .1 ? [[1.3, .3, .2], [.3, .1, .4]] : [[.3, .1, .4], [.3, .1, .4]] }), t, MARCUS.seed), { eyes: "happy", mouth: "grin", brows: "up", talk: who(t, "marcus") });
  // Zara
  if (s === 0) {
    placeChar(LENA, true, idle(pose({ x: FDOOR.x + 1.4, z: FDOOR.z + 1.0, ry: 1.1, a: PHONEUP, hp: .2 }), t, LENA.seed), { eyes: "open", mouth: "flat", brows: "worry", talk: who(t, "lena") });
    LPHONE.visible = true; holdAt(LENA, 0, LPHONE, [0, -.06, .07]);
  } else if (s === 1) placeChar(LENA, true, idle(pose({ x: COUNTER.x, z: COUNTER.z - .58, ry: 0, a: t > L[4] ? [[1.2, .2, 1.1 + .1 * Math.sin(t * 12)], [1.2, .2, 1.1 + .1 * Math.sin(t * 11)]] : [[.5, .2, .8], [.5, .2, .8]] }), t, LENA.seed),
    { eyes: t < L[4] ? "half" : "open", mouth: "smirk", brows: t < L[4] ? "raise1" : "flat", talk: who(t, "lena") });
  else if (s === 3) placeChar(LENA, true, idle(pose({ x: FDOOR.x + 1.0, z: FDOOR.z + .95, ry: .1, a: [[.3, .1, .4], [.3, .1, .4]] }), t, LENA.seed), { eyes: "happy", mouth: "grin", brows: "up", talk: who(t, "lena") });
  else if (s === 4) placeChar(LENA, true, idle(pose({ x: COUNTER.x, z: COUNTER.z - .58, ry: 0, a: t > C.endc + .3 ? [[.3, .1, .4], [2.2, .1 + .22 * Math.sin(t * 8), 1.5]] : [[.5, .2, .8], [.5, .2, .8]] }), t, LENA.seed), { eyes: "happy", mouth: "smile", brows: "up", talk: who(t, "lena") });
  else LENA.root.visible = false;
  // the rival: smug before, deflated after
  if (s === 0 || s === 3) placeChar(RIVAL, true, idle(pose({ x: BDOOR.x - .3, z: BDOOR.z - .6, ry: Math.PI - .3, a: s === 0 ? CROSS : [[.15, .1, .2], [.15, .1, .2]], hp: s === 3 ? .15 : -.05 }), t, RIVAL.seed),
    s === 0 ? { eyes: "half", mouth: "smirk", brows: "flat" } : { eyes: "open", mouth: "sad", brows: "worry" });
  else RIVAL.root.visible = false;
}

// ---------------------------------------------------------------- shots: [start, {p0, p1, l0, l1, fov, ap, roll, track}]
const MARCUSHEAD = v(FDOOR.x + .1, 1.55, FDOOR.z + .55), LHEAD = v(COUNTER.x, 1.5, COUNTER.z - .58);
const SHOTS = [
  [0, { p0: v(6.2, 4.4, 1.4), p1: v(3.6, 2.1, .7), l0: v(-1.8, 1.9, -3.6), l1: v(-2.6, 1.5, -3.8), fov: 56, ap: .01 }],
  [L[1] - .3, { track: 4, off: v(1.5, 2.0, 1.9), look: v(0, 2.15, 0), fov: 50, ap: .1 }],
  [L[2] - .25, { p0: v(FDOOR.x + .75, 1.6, -1.65), p1: v(FDOOR.x + .65, 1.58, -1.85), l0: MARCUSHEAD, fov: 52, ap: .12 }],
  [IN0, { p0: v(COUNTER.x + .5, 1.6, -5.2), p1: v(COUNTER.x + .3, 1.58, -5.45), l0: LHEAD, fov: 52, ap: .12 }],
  [L[4] - .3, { p0: v(FX + .1, 1.8, -4.85), p1: v(FX + 1.0, 1.75, -5.1), l0: v(COUNTER.x - 1.0, 1.85, -7.5), fov: 58, ap: .03 }],
  [CK, { p0: v(FX + 2.0, 1.9, -1.3), p1: v(FX + 2.3, 2.25, -1.9), l0: v(FX + 2.2, 2.75, -4.2), fov: 46, ap: .05 }],
  [L[5] - .2, { p0: v(FDOOR.x + .55, 1.1, -1.95), p1: v(FDOOR.x + .5, 1.15, -2.1), l0: MARCUSHEAD.clone().add(v(0, .1, 0)), fov: 54, ap: .12 }],
  [FL, { p0: v(8.2, 5.6, 1.2), p1: v(6.6, 4.7, .7), l0: v(-1, .9, -1.2), fov: 58, ap: .005 }],
  [FL + 2.7, { p0: v(BDOOR.x + .9, 1.6, 2.0), p1: v(BDOOR.x + .8, 1.58, 2.2), l0: v(BDOOR.x - .3, 1.5, BDOOR.z - .6), fov: 52, ap: .1 }],
  [NX, { p0: v(FX + 2.9, 1.85, -4.95), p1: v(FX + 2.6, 1.8, -5.1), l0: v(FX - 1.3, 1.45, -7.0), fov: 58, ap: .04 }],
  [C.endc - .1, { p0: v(FX + 1.6, 2.3, 2.5), p1: v(FX + 1.2, 2.15, 1.9), l0: v(FX - .4, 1.8, -4.2), fov: 58, ap: .01 }],
];
function shotAt(t) {
  let i = 0; while (i + 1 < SHOTS.length && t >= SHOTS[i + 1][0]) i++;
  const [a, s] = SHOTS[i], b = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR;
  const u = sm(clamp((t - a) / Math.max(.1, b - a)));
  let p, l;
  if (s.track != null) { const P = ST.crowd[s.track].root.position; l = P.clone().add(s.look); p = P.clone().add(s.off); }
  else { p = (s.p1 ? V.lerpVectors(s.p0, s.p1, u) : V.copy(s.p0)).clone(); l = s.l1 ? V2.lerpVectors(s.l0, s.l1, u).clone() : s.l0.clone(); }
  return { p, l, fov: s.fov, ap: s.ap, roll: s.roll || 0, f: p.distanceTo(l) };
}

// ---------------------------------------------------------------- per frame
function updShop(t, s) {
  ST.f.sale.rotation.x = .06 * Math.sin(t * 1.7); ST.b.sale.rotation.x = .06 * Math.sin(t * 1.5 + 1);   // the FOR SALE signs sway
  const cu = s >= 2 ? ss(t, CK + .35, CK + .7) : 0;
  ST.check.visible = cu > 0; ST.check.scale.setScalar(cu > 0 ? lerp(2.2, 1, cu) + .15 * pulse(t, CK + .8, .2) : .01);
  ST.inL.intensity = 6; ST.inL2.intensity = 4;
  // the hologram steps over the counter, one per step as Zara says it
  ST.holo.forEach((h, k) => {
    const on = s === 1 ? ss(t, C.steps[k] - .1, C.steps[k] + .25) : 0;
    h.visible = on > 0; h.material.opacity = .92 * on;
    h.position.set(COUNTER.x - 1.95 + (k % 2) * 1.0, 2.25 - Math.floor(k / 2) * .7 + .03 * Math.sin(t * 2 + k), COUNTER.z + .25 + (k % 2) * .1);
    h.rotation.set(0, .35, 0); h.scale.setScalar(lerp(.6, 1, on));
  });
  const k = C.steps.findLastIndex((x) => t > x - .1);
  setMap(ST.lapM, DYN.lap(s === 1 ? Math.max(0, k) : (s >= 2 ? 4 : 0)));
}
const LOOK = { bg: 0xBFD9F2, hs: 0xEAF4FF, hg: 0xC9B79A, hi: 1.05, sun: 0xFFE9C8, si: 2.6, sd: [.55, .8, .55], sat: 1.04, con: .06, vig: .3 };
function renderAt(t) {
  if (!TEX.ready) return;
  NOW = t;
  const s = sceneOf(t);
  for (const kk in SET) SET[kk].visible = true;
  for (const l of PL) l.intensity = 0;
  scene.background = tmpC.set(LOOK.bg).clone();
  scene.fog.color.set(LOOK.bg); scene.fog.near = 26; scene.fog.far = 110;
  hemi.color.set(LOOK.hs); hemi.groundColor.set(LOOK.hg); hemi.intensity = LOOK.hi;
  sun.color.set(LOOK.sun); sun.intensity = LOOK.si;
  updCast(t, s);
  updCrowd(t, s, camera);                 // first pass so the tracked walker has moved before the camera follows
  const sh = shotAt(t);
  const cv = window.RE_COVER;
  camera.position.copy(sh.p).add(V.set(Math.sin(t * .9) * .004, Math.sin(t * 1.3 + 1) * .004, 0));
  camera.fov = sh.fov;
  if (cv && cv.cam) { camera.position.set(...cv.cam); sh.l.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix(); camera.up.set(0, 1, 0); camera.lookAt(sh.l); camera.rotateZ(sh.roll);
  camera.updateMatrixWorld(true);
  updCrowd(t, s, camera);                 // second pass: the answer cards face the final camera
  updShop(t, s);
  scene.updateMatrixWorld(true);
  cocPass.uniforms.uF.value = sh.f; cocPass.uniforms.uAp.value = cv ? (cv.ap ?? sh.ap) : sh.ap;
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = .08; gu.uCool.value = 0; gu.uSat.value = LOOK.sat; gu.uCon.value = LOOK.con; gu.uVig.value = LOOK.vig; gu.uTint.value = 0;
  gu.uFlash.value = s === 2 ? .18 * pulse(t, CK + .7, .15) : 0; gu.uCA.value = .001; gu.uKeep.value = 0; gu.uGrain.value = .018;
  gu.uTop.value = cv ? 0 : Math.max(1 - ss(t, 2.4, 2.9), ss(t, C.endc, C.endc + .6) * .9, C.cards.some(([a, b]) => t > a - .1 && t < b + .1) ? .5 : 0);
  gu.uDark.value = 0;
  bloom.strength = .28;
  sun.target.position.set(0, 0, -2); sun.position.copy(sun.target.position).add(S.set(...LOOK.sd).normalize().multiplyScalar(30));
  Object.assign(sun.shadow.camera, { left: -13, right: 13, top: 13, bottom: -13, near: 1, far: 80 });
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures that need the fonts
const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`, SERIF = (w, f, it = false) => `${it ? "italic " : ""}${w} ${f}px Garamond, serif`;
const text = (w, h, draw) => pix(w, h, draw, false);
const block = (g, x, y, w, h, c, r = 14) => { g.fillStyle = c; rr(g, x, y, w, h, r); g.fill(); };
const label = (g, s, x, y, f, c, al = "left", wt = 800) => { g.font = FT(wt, f); g.fillStyle = c; g.textAlign = al; g.fillText(s, x, y); g.textAlign = "left"; };
const BLUE = "#2F7BF6";
const tick = (g, cx, cy, r, c = BLUE) => { g.fillStyle = c; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.fill(); g.strokeStyle = "#fff"; g.lineWidth = r * .24; g.lineCap = "round"; g.lineJoin = "round"; g.beginPath(); g.moveTo(cx - r * .42, cy + r * .02); g.lineTo(cx - r * .1, cy + r * .34); g.lineTo(cx + r * .45, cy - r * .3); g.stroke(); };
const DYN = {};
function dyn(key, w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  let last = null;
  DYN[key] = (...a) => { const k = a.join("|"); if (k !== last) { last = k; draw(g, w, h, ...a); tx.needsUpdate = true; } return tx; };
}
function buildTextures() {
  TEX.signKey = text(920, 180, (g, w, h) => { g.clearRect(0, 0, w, h); block(g, 6, 14, w - 12, h - 28, "#1C2A4A", 20); g.textAlign = "center"; g.fillStyle = "#F2C94C"; g.font = FT(800, 84); g.fillText("KEYSTONE REALTY", w / 2 - 40, 120); });
  TEX.signPrime = text(920, 180, (g, w, h) => { g.clearRect(0, 0, w, h); block(g, 6, 14, w - 12, h - 28, "#F4F1EA", 20); g.textAlign = "center"; g.fillStyle = "#1F7A4D"; g.font = FT(800, 76); g.fillText("PRIME NEST REALTY", w / 2 + 40, 118); });
  const awn = (a, b) => text(256, 64, (g, w, h) => { for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? a : b; g.fillRect(i * 32, 0, 32, h); } g.fillStyle = "rgba(0,0,0,.2)"; g.fillRect(0, h - 8, w, 8); });
  TEX.awnKey = awn("#F4F1EA", "#1C2A4A"); TEX.awnPrime = awn("#F4F1EA", "#1F7A4D");
  const house = (g, x, y, w, h, k) => { const roof = ["#B5654A", "#5E6470", "#7A4A2A", "#2F6F5E", "#8C3B3B", "#4A5A7A"][k % 6], wall = ["#F4EFE6", "#E8D9BE", "#DCE6EE", "#F2E3C9", "#E9E4DA", "#F7F1E3"][k % 6];
    g.fillStyle = "#BFE0F7"; g.fillRect(x, y, w, h * .62); g.fillStyle = "#7DBA6A"; g.fillRect(x, y + h * .62, w, h * .38);
    g.fillStyle = wall; g.fillRect(x + w * .2, y + h * .34, w * .6, h * .38); g.fillStyle = roof; g.beginPath(); g.moveTo(x + w * .14, y + h * .36); g.lineTo(x + w * .5, y + h * .12); g.lineTo(x + w * .86, y + h * .36); g.fill();
    g.fillStyle = "#3A3A3A"; g.fillRect(x + w * .45, y + h * .52, w * .1, h * .2); g.fillStyle = "#9FC4DE"; g.fillRect(x + w * .27, y + h * .44, w * .12, h * .1); g.fillRect(x + w * .61, y + h * .44, w * .12, h * .1); };
  for (let k = 0; k < 6; k++) TEX["listing" + k] = text(320, 400, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); house(g, 14, 14, w - 28, 250, k); label(g, ["$420,000", "$389,000", "$515,000", "$298,000", "$460,000", "$352,000"][k], 20, 316, 40, "#14161C"); label(g, ["3 bed · 2 bath", "2 bed · 2 bath", "4 bed · 3 bath", "2 bed · 1 bath", "3 bed · 3 bath", "3 bed · 2 bath"][k], 20, 360, 26, "#6A6878", "left", 700); });
  TEX.wall = text(920, 340, (g, w, h) => { g.fillStyle = "#F4F1EA"; g.fillRect(0, 0, w, h); label(g, "OUR LISTINGS", 24, 44, 32, "#1C2A4A"); for (let k = 0; k < 8; k++) { const x = 24 + (k % 4) * 224, y = 64 + Math.floor(k / 4) * 136; g.fillStyle = "#FFFFFF"; g.fillRect(x, y, 208, 124); house(g, x + 6, y + 6, 196, 90, k); label(g, k % 3 ? "FOR SALE" : "SOLD", x + 10, y + 116, 18, k % 3 ? "#1C2A4A" : "#D9483B"); } });
  const sale = (who, c) => text(280, 200, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = c; g.fillRect(0, 0, w, 70); label(g, "FOR SALE", w / 2, 50, 40, "#FFFFFF", "center"); label(g, who, w / 2, 124, 30, c, "center"); label(g, "555-0142", w / 2, 172, 26, "#3A3A3A", "center", 700); });
  TEX.saleKey = sale("KEYSTONE", "#1C2A4A"); TEX.salePrime = sale("PRIME NEST", "#1F7A4D");
  TEX.check = text(256, 256, (g, w, h) => { g.clearRect(0, 0, w, h); g.shadowColor = "rgba(47,123,246,.8)"; g.shadowBlur = 24; tick(g, 128, 128, 100); });
  TEX.sky = text(16, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#5FA6E8"); gr.addColorStop(.45, "#A9D2F2"); gr.addColorStop(.55, "#E4F1FA"); gr.addColorStop(1, "#E4F1FA"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  // the ChatGPT answer card over every phone
  const card = (name, sub, isFade) => text(560, 256, (g, w, h) => {
    g.clearRect(0, 0, w, h); block(g, 6, 6, w - 12, h - 12, "rgba(255,255,255,.96)", 28);
    label(g, "ChatGPT · best real estate agent near me?", 34, 56, 24, "#6A6878", "left", 700);
    block(g, 28, 84, w - 56, 140, isFade ? "#FFF6D8" : "#EEF7F1", 20);
    block(g, 44, 104, 100, 100, isFade ? "#1C2A4A" : "#1F7A4D", 16); label(g, isFade ? "KR" : "PN", 94, 168, 40, isFade ? "#F2C94C" : "#F4F1EA", "center");
    g.font = FT(800, name.length > 14 ? 34 : 40); g.fillStyle = "#14161C"; g.fillText(name, 166, 148); tick(g, 166 + g.measureText(name).width + 30, 135, 20);
    label(g, sub, 166, 194, 26, isFade ? "#B7791F" : "#6A6878", "left", 700);
  });
  TEX.cardPrime = card("Prime Nest Realty", "open now · 4.6", false);
  TEX.cardKey = card("Keystone Realty", "open now · showings today", true);
  // the four steps as holograms
  const STEPS = [["1", "Business Hub", "chatgpt.com/business-hub"], ["2", "Search + Get Started", "Keystone Realty"], ["3", "Verify", "office phone"], ["4", "ID check", "blue check"]];
  STEPS.forEach(([n, a, b], k) => {
    TEX["holo" + k] = text(512, 320, (g, w, h) => {
      g.clearRect(0, 0, w, h); g.shadowColor = "rgba(120,200,255,.9)"; g.shadowBlur = 22; g.strokeStyle = "#8FE3FF"; g.lineWidth = 6; rr(g, 14, 14, w - 28, h - 28, 26); g.stroke();
      g.shadowBlur = 0; g.fillStyle = "rgba(60,150,230,.28)"; rr(g, 14, 14, w - 28, h - 28, 26); g.fill();
      g.fillStyle = "#E8FBFF"; g.font = FT(800, 96); g.fillText(n, 44, 132); label(g, a, 130, 112, a.length > 14 ? 34 : 44, "#FFFFFF");
      label(g, b, 44, 220, b.length > 16 ? 28 : 34, "#BFEFFF", "left", 700);
      if (k === 3) tick(g, w - 80, 230, 34);
    });
  });
  // Zara's laptop: Business Hub at each step
  dyn("lap", 640, 400, (g, w, h, k) => {
    g.fillStyle = "#F7F7F9"; g.fillRect(0, 0, w, h); g.fillStyle = "#1E1B18"; g.fillRect(0, 0, w, 50); label(g, "chatgpt.com/business-hub", 24, 34, 24, "#E9E4DA", "left", 700);
    label(g, ["Business Hub", "Business Hub", "Verify your business", "Identity check", "Keystone Realty"][k], 30, 110, 38, "#14161C");
    if (k === 0) { block(g, 30, 140, w - 60, 64, "#FFFFFF", 12); g.strokeStyle = "#C9C9D2"; g.lineWidth = 2; rr(g, 30, 140, w - 60, 64, 12); g.stroke(); label(g, "Search your business", 50, 182, 26, "#9A9AA6", "left", 600); }
    if (k === 1) { block(g, 30, 140, w - 60, 64, "#FFFFFF", 12); label(g, "Keystone Realty", 50, 182, 28, "#14161C", "left", 700); block(g, 30, 230, w - 60, 70, "#14161C", 35); label(g, "Get Started", w / 2, 276, 30, "#FFFFFF", "center"); }
    if (k === 2) ["Business phone", "Business email", "Website domain"].forEach((s, j) => { block(g, 30, 140 + j * 74, w - 60, 62, j === 0 ? "#E7F7EC" : "#FFFFFF", 12); label(g, s, 50, 180 + j * 74, 26, "#14161C", "left", 700); if (j === 0) tick(g, w - 70, 171, 20, "#22C55E"); });
    if (k === 3) { block(g, 30, 140, 180, 120, "#E5E7EB", 12); block(g, 230, 160, 300, 18, "#D1D5DB", 9); block(g, 230, 200, 220, 18, "#D1D5DB", 9); label(g, "Verified", 230, 250, 30, "#22C55E"); }
    if (k === 4) { label(g, "Keystone Realty", 30, 180, 44, "#14161C"); tick(g, 420, 165, 24); label(g, "Verified business", 30, 230, 26, "#6A6878", "left", 700); }
  });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
  TEX.ready = true;
}

const ready = (async () => {
  try { const jb = new FontFace("JBMono", "url(assets/fonts/jbmono-bold.ttf)", { weight: "700" }); document.fonts.add(await jb.load()); } catch (e) { /* fall back */ }
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 40px Manrope"), document.fonts.load("700 40px Garamond")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  for (const k in SET) SET[k].visible = true;
  renderer.compile(scene, camera);
  renderAt(window.RE_COVER ? window.RE_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["realty"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.RE_COVER ? window.RE_COVER.t : e.detail.time));
window.STACK_DEBUG = { renderAt, SET, camera, C };
