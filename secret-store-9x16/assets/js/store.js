// The Secret Free Store (ai.nxtlvl reel). Toy-like blocky 3D in the house engine: Nxtlvl Bot, an orange robot with a
// cyan visor, sneaks through a glossy mall where every shop is a paid app with a giant price tag, finds a hidden door
// marked GitHub and opens six loot chests in a golden vault, rarer and rarer (rare, epic, legendary, mythic), each one a
// free repo that replaces a paid app. Three more chests stay locked behind bars: they open in the DMs.
// Everything is a pure function of time t (seconds), drawn on HyperFrames' hf-seek; cue times come from the voice
// (window.CT, written by build/generate.py). Post: depth of field from the depth buffer, bloom, then the grade.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const C = window.CT, K = C.k;
const W = 1080, H = 1920, DUR = C.end;
const SPEAK = C.ph.flat ? C.ph.map((l, i) => l.map((s, j) => [s, C.pe[i][j]])).flat() : [];

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ramp = (t, a, b) => clamp((t - a) / (b - a));
const sm = (x) => x * x * (3 - 2 * x);
const ss = (t, a, b) => sm(ramp(t, a, b));
const lerp = (a, b, x) => a + (b - a) * x;
const hash = (i) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const pulse = (t, a, w = .35) => Math.exp(-(((t - a) / w) ** 2));
const backOut = (x, s = 1.9) => { x = clamp(x); const c = s + 1; return 1 + c * (x - 1) ** 3 + s * (x - 1) ** 2; };
const after = (t, a) => Math.max(0, t - a);
const tmpC = new THREE.Color();
const V = new THREE.Vector3(), V2 = new THREE.Vector3(), Q = new THREE.Quaternion(), M4 = new THREE.Matrix4(), S3 = new THREE.Vector3(), EU = new THREE.Euler();
const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
const speaking = (t) => SPEAK.some(([a, b]) => t > a + .02 && t < b - .03);
const ORANGE = 0xD97757, CREAM = 0xF3E9DC, JOINT = 0x3A3442, CYAN = 0x45F3FF;
const RAR = { rare: 0x3D8BFF, epic: 0xB45CFF, legendary: 0xFFC233, mythic: 0xFF2E4D, secret: 0x8F7BFF };

// ---------------------------------------------------------------- renderer, scene, post (DOF -> bloom -> output -> grade)
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
const ENV = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.fog = new THREE.Fog(0xF2E6DA, 30, 90);
const NEAR = .05, FAR = 400;
const camera = new THREE.PerspectiveCamera(45, W / H, NEAR, FAR);
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
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .5, .55, .86);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1.08 }, uVig: { value: .3 }, uFlash: { value: 0 }, uFlashC: { value: new THREE.Color(1, .97, .9) },
    uWarm: { value: 0 }, uCool: { value: 0 }, uCA: { value: 0 }, uCon: { value: .04 }, uDark: { value: 0 }, uTop: { value: 0 } },
  vertexShader: VS,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uWarm, uCool, uCA, uCon, uDark, uTop; uniform vec3 uFlashC; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 d = vec2(.5) - vUv;
      vec3 c = vec3(texture2D(tDiffuse, vUv + d * uCA).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - d * uCA).b);
      float g = dot(c, vec3(.299, .587, .114));
      c = mix(vec3(g), c, uSat);
      c = mix(c, c * vec3(1.07, 1.0, .86), uWarm);
      c = mix(c, c * vec3(.86, .97, 1.14), uCool);
      c = (c - .5) * (1. + uCon) + .5;
      vec2 q = vUv - .5; float r = dot(q, q);
      c *= 1. - r * uVig * 2.2;
      c *= 1. - uTop * smoothstep(.45, .92, vUv.y) * .6;
      vec2 px = vUv * vec2(1080., 1920.);
      c += (h(floor(px) + fract(uTime * 7.13) * 97.) - .5) * .018;
      c = mix(c, uFlashC, uFlash);
      c *= 1. - uDark;
      gl_FragColor = vec4(max(c, 0.), 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- lights: one shadow-casting key, a pool of point lights
const hemi = new THREE.HemisphereLight(0xFFF4E8, 0xC9B8A6, 1.0);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xFFF1E0, 2.0);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -.0004;
sun.shadow.normalBias = .03;
sun.shadow.radius = 4;
scene.add(sun, sun.target);
const PL = Array.from({ length: 8 }, () => { const l = new THREE.PointLight(0xffffff, 0, 8, 1.8); scene.add(l); return l; });

// ---------------------------------------------------------------- materials and primitives
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .8, metalness: 0, ...o });
const plastic = (c, o = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: .38, clearcoat: .9, clearcoatRoughness: .12, envMap: ENV, envMapIntensity: .55, ...o });
const metal = (c, r = .28, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: .9, envMap: ENV, envMapIntensity: 1.1, ...o });
const glow = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false, ...o });
const additive = (c, op = 1) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false, transparent: true, opacity: op, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
let PARENT = scene;
const add = (m, cast = true, recv = true, parent) => { m.castShadow = cast; m.receiveShadow = recv; (parent || PARENT).add(m); return m; };
const MATC = new Map();
const cm = (c) => { if (c && (c.isMaterial || Array.isArray(c))) return c; let m = MATC.get(c); if (!m) { m = mat(c); MATC.set(c, m); } return m; };
const BOXG = new THREE.BoxGeometry(1, 1, 1);
const RBG = new Map();
const rbox = (w, h, d, r) => { const k = [w, h, d, r].join(); let g = RBG.get(k); if (!g) { g = new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2, h / 2, d / 2)); RBG.set(k, g); } return g; };
const box = (w, h, d, c, x, y, z, o = {}) => {
  const g = o.round ? rbox(w, h, d, o.round) : BOXG;
  const m = add(new THREE.Mesh(g, cm(c)), o.cast ?? true, o.recv ?? true, o.parent);
  if (g === BOXG) m.scale.set(w, h, d);
  m.position.set(x, y, z); if (o.ry) m.rotation.y = o.ry; if (o.rx) m.rotation.x = o.rx; if (o.rz) m.rotation.z = o.rz;
  return m;
};
const cyl = (r1, r2, h, c, x, y, z, seg = 20, o = {}) => { const m = add(new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg, 1, !!o.open, o.ts ?? 0, o.tl ?? Math.PI * 2), cm(c)), o.cast ?? true, o.recv ?? true, o.parent); m.position.set(x, y, z); if (o.rx) m.rotation.x = o.rx; if (o.rz) m.rotation.z = o.rz; if (o.ry) m.rotation.y = o.ry; return m; };
const sph = (r, c, x, y, z, o = {}) => { const m = add(new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), cm(c)), o.cast ?? true, true, o.parent); m.position.set(x, y, z); return m; };
const plane = (w, h, m, x, y, z, ry = 0, parent) => { const p = add(new THREE.Mesh(new THREE.PlaneGeometry(w, h), m), false, false, parent); p.position.set(x, y, z); p.rotation.y = ry; return p; };
function cvs(w, h, draw) { const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d"); draw(g, w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; }
const rr = (g, x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
const FT = (w, f) => `${w} ${f}px Manrope, sans-serif`, MONO = (f) => `700 ${f}px JBMono, monospace`;
const LATE = [];     // [material, key]: textures drawn after the fonts and logos load
const TEX = {};
const texMat = (key, o = {}) => { const m = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, ...o }); LATE.push([m, key]); return m; };
const texStd = (key, o = {}) => { const m = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .5, ...o }); LATE.push([m, key]); return m; };
const noise = (base, n, amp, sz = 128, rep = 1) => { const t = cvs(sz, sz, (g) => { g.fillStyle = base; g.fillRect(0, 0, sz, sz); for (let i = 0; i < sz * sz * .3; i++) { const h = hash(i * 1.37 + n); g.fillStyle = h > .5 ? `rgba(255,255,255,${amp})` : `rgba(0,0,0,${amp})`; g.fillRect(Math.floor(hash(i * 3.1 + n) * sz), Math.floor(hash(i * 7.7 + n) * sz), 2, 2); } }); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep, rep); return t; };

const SET = {};
const mkSet = (k) => { const g = new THREE.Group(); scene.add(g); SET[k] = g; PARENT = g; return g; };

// ================================================================= NXTLVL BOT
// feet at the root; hips 0.42; body 0.5 x 0.46; neck; head 0.56 x 0.46 with a dark visor and cyan eyes; antenna
const BOT = {};
{
  const g = new THREE.Group(); scene.add(g); BOT.root = g;
  const body = plastic(ORANGE), cream = plastic(CREAM), joint = plastic(JOINT, { roughness: .5 }), visorM = new THREE.MeshPhysicalMaterial({ color: 0x0E1220, roughness: .12, clearcoat: 1, clearcoatRoughness: .05, envMap: ENV, envMapIntensity: .9 });
  const mk = (geo, m, parent, x, y, z) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = true; o.receiveShadow = true; parent.add(o); return o; };
  const hips = new THREE.Group(); hips.position.y = .42; g.add(hips); BOT.hips = hips;
  mk(rbox(.4, .14, .27, .05), joint, hips, 0, -.02, 0);
  const torso = new THREE.Group(); torso.position.y = .04; hips.add(torso); BOT.torso = torso;
  mk(rbox(.52, .48, .37, .1), body, torso, 0, .25, 0);
  mk(rbox(.3, .2, .04, .04), cream, torso, 0, .27, .18);
  BOT.core = mk(new THREE.CylinderGeometry(.045, .045, .03, 20), glow(CYAN), torso, 0, .27, .205); BOT.core.rotation.x = Math.PI / 2;
  mk(new THREE.CylinderGeometry(.075, .085, .14, 18), joint, torso, 0, .52, 0);
  const neck = new THREE.Group(); neck.position.y = .55; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head); BOT.head = head;
  mk(rbox(.58, .48, .48, .12), body, head, 0, .23, 0);
  mk(rbox(.48, .3, .05, .06), visorM, head, 0, .24, .225);
  BOT.faceM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, depthWrite: false });
  const face = new THREE.Mesh(new THREE.PlaneGeometry(.44, .27), BOT.faceM); face.position.set(0, .24, .252); head.add(face);
  for (const s of [-1, 1]) { const e = mk(new THREE.CylinderGeometry(.06, .06, .05, 18), cream, head, s * .3, .24, 0); e.rotation.z = Math.PI / 2; }
  mk(new THREE.CylinderGeometry(.014, .014, .17, 8), joint, head, .1, .55, -.02);
  BOT.ant = mk(new THREE.SphereGeometry(.045, 16, 12), glow(CYAN), head, .1, .65, -.02);
  BOT.sh = []; BOT.el = []; BOT.hip = []; BOT.knee = []; BOT.hand = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * .31, .4, 0); torso.add(a); BOT.sh.push(a);
    mk(new THREE.SphereGeometry(.085, 16, 12), joint, a, 0, 0, 0);
    mk(rbox(.15, .22, .15, .05), body, a, 0, -.12, 0);
    const e = new THREE.Group(); e.position.y = -.23; a.add(e); BOT.el.push(e);
    mk(new THREE.SphereGeometry(.065, 14, 10), joint, e, 0, 0, 0);
    mk(rbox(.15, .19, .15, .05), cream, e, 0, -.1, 0);
    BOT.hand.push(mk(rbox(.19, .15, .19, .06), joint, e, 0, -.25, .01));
    const h = new THREE.Group(); h.position.set(s * .12, 0, 0); hips.add(h); BOT.hip.push(h);
    mk(rbox(.16, .22, .18, .05), joint, h, 0, -.1, 0);
    const kn = new THREE.Group(); kn.position.y = -.2; h.add(kn); BOT.knee.push(kn);
    mk(rbox(.17, .17, .19, .05), body, kn, 0, -.08, 0);
    mk(rbox(.21, .1, .29, .045), cream, kn, 0, -.19, .04);
  }
}
// the face: cyan eyes and a small mouth on the visor, 256 x 160
const FACES = new Map();
function faceTex(eyes, mouth, look = 0) {
  const k = eyes + "|" + mouth + "|" + look; let t = FACES.get(k); if (t) return t;
  t = cvs(256, 160, (g, w, h) => {
    g.clearRect(0, 0, w, h);
    g.strokeStyle = g.fillStyle = "#6FF7FF"; g.shadowColor = "#45F3FF"; g.shadowBlur = 14; g.lineCap = "round"; g.lineWidth = 13;
    const eye = (cx, kind) => {
      const x = cx + look * 16, y = 64;
      if (kind === "open") { rr(g, x - 17, y - 27, 34, 54, 17); g.fill(); }
      else if (kind === "wide") { g.beginPath(); g.arc(x, y, 30, 0, 7); g.fill(); g.fillStyle = "#0E1220"; g.beginPath(); g.arc(x + 8, y - 9, 8, 0, 7); g.fill(); g.fillStyle = "#6FF7FF"; }
      else if (kind === "happy") { g.beginPath(); g.arc(x, y + 14, 24, Math.PI * 1.12, Math.PI * 1.88); g.stroke(); }
      else if (kind === "closed") { g.beginPath(); g.moveTo(x - 20, y + 4); g.lineTo(x + 20, y + 4); g.stroke(); }
      else if (kind === "sly") { rr(g, x - 20, y - 6, 40, 22, 11); g.fill(); }
      else if (kind === "star") { g.beginPath(); for (let i = 0; i < 10; i++) { const r = i % 2 ? 13 : 32, a = -Math.PI / 2 + i * Math.PI / 5; g.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); } g.closePath(); g.fill(); }
    };
    const [l, r] = eyes.includes(",") ? eyes.split(",") : [eyes, eyes];
    eye(78, l); eye(178, r);
    g.lineWidth = 9;
    const mx = 128 + look * 10, my = 128;
    if (mouth === "smile") { g.beginPath(); g.arc(mx, my - 14, 18, Math.PI * .2, Math.PI * .8); g.stroke(); }
    else if (mouth === "grin") { g.beginPath(); g.moveTo(mx - 26, my - 6); g.quadraticCurveTo(mx, my + 22, mx + 26, my - 6); g.closePath(); g.fill(); }
    else if (mouth === "o") { g.beginPath(); g.ellipse(mx, my - 2, 11, 13, 0, 0, 7); g.fill(); }
    else if (mouth === "talk") { rr(g, mx - 16, my - 10, 32, 16, 8); g.fill(); }
    else if (mouth === "flat") { g.beginPath(); g.moveTo(mx - 14, my - 2); g.lineTo(mx + 14, my - 2); g.stroke(); }
    else if (mouth === "smirk") { g.beginPath(); g.moveTo(mx - 14, my - 2); g.quadraticCurveTo(mx + 6, my + 4, mx + 18, my - 10); g.stroke(); }
  });
  FACES.set(k, t); return t;
}
const pose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, crouch: 0, lean: 0, tw: 0, hy: 0, hp: 0, hr: 0, a: [[.1, .12, .2], [.1, .12, .2]], l: [[0, 0], [0, 0]], ...o });
function mixP(p, q, u) {
  if (u <= 0) return p; if (u >= 1) return q;
  const r = {};
  for (const k in p) { const a = p[k], b = q[k]; r[k] = Array.isArray(a) ? a.map((v, i) => v.map((w, j) => lerp(w, b[i][j], u))) : lerp(a, b, u); }
  return r;
}
function applyPose(p) {
  BOT.root.position.set(p.x, p.y, p.z); BOT.root.rotation.y = p.ry;
  BOT.hips.position.y = .42 - p.crouch;
  BOT.torso.rotation.set(p.lean, p.tw, 0);
  BOT.head.rotation.set(p.hp, p.hy, p.hr);
  for (let k = 0; k < 2; k++) {
    BOT.sh[k].rotation.set(-p.a[k][0], 0, (k ? 1 : -1) * p.a[k][1]);
    BOT.el[k].rotation.x = -p.a[k][2];
    BOT.hip[k].rotation.x = -p.l[k][0];
    BOT.knee[k].rotation.x = p.l[k][1];
  }
}
// a tiptoe sneak: knees bent, high careful steps, hands up by the chest
function sneak(p, ph, amp = 1) {
  const s = Math.sin(ph), c = Math.cos(ph);
  return { ...p, crouch: p.crouch + .05 + .02 * Math.abs(c), y: p.y + .025 * Math.abs(s), lean: p.lean + .12,
    l: [[.55 + .45 * s * amp, .7 + .35 * Math.max(0, s) * amp], [.55 - .45 * s * amp, .7 + .35 * Math.max(0, -s) * amp]],
    a: [[1.05 + .15 * s, .25, 1.9], [1.05 - .15 * s, .25, 1.9]], hy: p.hy + .35 * Math.sin(ph * .5) };
}
function walk(p, ph, amp = 1) {
  const s = Math.sin(ph), c = Math.cos(ph);
  return { ...p, y: p.y + .03 * Math.abs(c) * amp, l: [[.5 * s * amp, (.3 + .35 * Math.max(0, -c)) * amp * (s < 0 ? 1 : .3)], [-.5 * s * amp, (.3 + .35 * Math.max(0, c)) * amp * (s > 0 ? 1 : .3)]],
    a: [[-.45 * s * amp, .14, .35], [.45 * s * amp, .14, .35]] };
}
const idle = (p, t) => ({ ...p, lean: p.lean + .02 * Math.sin(t * 1.7), hr: p.hr + .04 * Math.sin(t * 1.1), y: p.y + .008 * Math.sin(t * 3.4) });
const CHEER = [[2.9, .45, .2], [2.9, .45, .2]], WOW = [[1.3, .5, 1.6], [1.3, .5, 1.6]];
let NOW = 0;
function setFace(f) {
  let eyes = f.eyes || "open", mouth = f.mouth || "smile";
  if (eyes === "open" && !f.noblink) { const u = (NOW + 1.3) % 3.1; if (u < .11) eyes = "closed"; }
  if (f.talk !== false && speaking(NOW)) mouth = ["talk", "o", "talk", mouth === "smile" ? "smile" : mouth][Math.floor(NOW * 11) % 4];
  const tx = faceTex(eyes, mouth, f.look || 0);
  if (BOT.faceM.map !== tx) { BOT.faceM.map = tx; BOT.faceM.needsUpdate = true; }
}

// ================================================================= THE MALL (z: +8 .. -40, x: -6 .. 6)
const SHOPS = [   // [side, z, key, brand colour, price, sub]
  [-1, 4.0, "pro2", "#E84D8A", "$49", "/mo"],
  [1, 4.0, "pro3", "#00A884", "$24", "/mo"],
  [-1, -2.5, "typeform", "#262627", "$39", "/mo"],
  [1, -4.5, "zapier", "#FF4F00", "$29.99", "/mo"],
  [-1, -9.0, "mailchimp", "#FFE01B", "$13", "/mo"],
  [1, -11.0, "docusign", "#4C00FF", "$15", "/mo"],
  [-1, -17.5, "otter", "#2D5BFF", "$16.99", "/mo"],
  [1, -17.5, "ga", "#E37400", "$0*", "your data"],
  [-1, -24.0, "figma", "#A259FF", "$20", "/mo"],
  [1, -24.0, "capcut", "#111111", "$19.99", "/mo"],
  [-1, -30.5, "buffer", "#2C4BFF", "$6", "/mo"],
  [1, -30.5, "pro", "#888888", "$$$", "/mo"],
];
const MALL = { tags: [], signs: [] };
{
  mkSet("mall");
  const tile = cvs(256, 256, (g, w, h) => { g.fillStyle = "#EFE5D8"; g.fillRect(0, 0, w, h); for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) { g.fillStyle = (i + j) % 2 ? "#F7EFE6" : "#E9DDCF"; g.fillRect(i * 128 + 3, j * 128 + 3, 122, 122); } for (let k = 0; k < 400; k++) { g.fillStyle = `rgba(160,130,110,${hash(k) * .08})`; g.fillRect(hash(k * 3) * w, hash(k * 5) * h, 3, 1); } });
  tile.wrapS = tile.wrapT = THREE.RepeatWrapping; tile.repeat.set(6, 26);
  const floorM = new THREE.MeshPhysicalMaterial({ map: tile, roughness: .16, clearcoat: 1, clearcoatRoughness: .06, envMap: ENV, envMapIntensity: .8 });
  const fl = add(new THREE.Mesh(new THREE.PlaneGeometry(14, 60), floorM), false, true); fl.rotation.x = -Math.PI / 2; fl.position.set(0, 0, -16);
  // ceiling with light strips
  box(14, .3, 60, 0xF7F1EA, 0, 6.6, -16, { cast: false });
  for (let z = 6; z > -44; z -= 4) box(9, .06, .5, glow(0xFFF6E6), 0, 6.43, z, { cast: false, recv: false });
  // storefronts
  const wallM = plastic(0xF4EEE6, { roughness: .6, clearcoat: .3 });
  for (const [side, z, key, col, price, sub] of SHOPS) {
    const x = side * 6.2;
    box(.3, 6.6, 5.6, wallM, x + side * .6, 3.3, z, { cast: false });          // back wall
    box(1.6, 6.6, .4, wallM, x, 3.3, z + 2.9, { cast: false });                 // pillars
    box(1.6, 6.6, .4, wallM, x, 3.3, z - 2.9, { cast: false });
    box(1.6, 1.4, 5.4, wallM, x, 5.9, z, { cast: false });                       // header
    box(1.8, .08, 5.8, plastic(col, { roughness: .4 }), x - side * .05, 5.15, z, { cast: false });
    const sign = plane(4.6, 1.1, texMat("sign_" + key), x - side * .82, 5.85, z, side < 0 ? Math.PI / 2 : -Math.PI / 2); MALL.signs.push(sign);
    // the window: interior glow and shelves of glossy app boxes
    plane(5.2, 4.6, glow(new THREE.Color(col).lerp(new THREE.Color(0xffffff), .72)), x + side * .4, 2.4, z, side < 0 ? Math.PI / 2 : -Math.PI / 2);
    for (let r = 0; r < 3; r++) {
      box(.5, .08, 4.6, wallM, x + side * .15, .9 + r * 1.2, z, { cast: false });
      for (let q = 0; q < 5; q++) box(.34, .5, .62, plastic(new THREE.Color(col).lerp(new THREE.Color(0xffffff), hash(q + r * 7 + z) * .5)), x + side * .1, 1.2 + r * 1.2, z - 1.9 + q * .95, { cast: false });
    }
    const glass = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .02, transmission: 0, transparent: true, opacity: .14, envMap: ENV, envMapIntensity: 1.6, clearcoat: 1 });
    plane(5.4, 4.6, glass, x - side * .75, 2.3, z, side < 0 ? Math.PI / 2 : -Math.PI / 2);
    // the giant price tag hanging over the walkway in front of the shop
    const tg = new THREE.Group(); tg.position.set(side * 1.55, 6.45, z + .2); PARENT.add(tg);
    cyl(.012, .012, 2.2, 0x9A8F84, 0, -1.1, 0, 6, { parent: tg, cast: false });
    const tagM = texStd("tag_" + key, { roughness: .45 });
    const tag = new THREE.Group(); tag.position.y = -3.05; tg.add(tag); tag.rotation.y = side < 0 ? .35 : -.35;
    for (const r of [0, Math.PI]) { const q = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 1.82), tagM); q.rotation.y = r; q.position.z = r ? -.004 : .004; q.castShadow = true; tag.add(q); }
    MALL.tags.push({ g: tg, seed: z * 1.7 + side });
  }
  // the hero standee: a giant price tag on the floor at the front (the bot hides behind it in the first shot)
  MALL.standee = new THREE.Group(); MALL.standee.position.set(-.62, 0, 2.6); MALL.standee.rotation.y = .3; PARENT.add(MALL.standee);
  const st = new THREE.Mesh(new THREE.PlaneGeometry(1.35, 1.9), texStd("tag_zapier", { roughness: .45 })); st.position.y = 1.08; st.castShadow = true; MALL.standee.add(st);
  box(1.4, .06, .5, 0x3A3442, 0, .03, 0, { parent: MALL.standee });
  box(.06, .3, .06, 0x3A3442, 0, .18, -.05, { parent: MALL.standee });
  box(14, 6.6, .3, wallM, 0, 3.3, 8.2, { cast: false });
  plane(5, 4.4, glow(0xFFFBF2), 0, 2.2, 8.0, Math.PI);
  // planters with blocky trees and benches down the middle
  for (const z of [-7, -14, -21, -28]) {
    box(1.4, .6, 1.4, plastic(0xE8DCCD), 0, .3, z, {});
    box(1.1, .1, 1.1, 0x5A3E2A, 0, .62, z, {});
    cyl(.08, .1, 1.4, 0x6B4A2E, 0, 1.3, z, 8);
    for (let k = 0; k < 4; k++) box(.7 - k * .1, .5, .7 - k * .1, plastic(k % 2 ? 0x4FA36A : 0x3E8F5A, { roughness: .6 }), (hash(k + z) - .5) * .3, 1.9 + k * .32, (hash(k * 3 + z) - .5) * .3, {});
  }
}
{
  mkSet("passage");
  // the side passage on the left between Mailchimp and Otter, to the door (x -6.4 .. -11, z -13.2 +- .9)
  const darkM = mat(0x232634, { roughness: .9 });
  box(4.8, 3.2, .3, darkM, -8.6, 1.6, -12.05, { cast: false });
  box(4.8, 3.2, .3, darkM, -8.6, 1.6, -14.35, { cast: false });
  box(4.8, .3, 2.6, darkM, -8.6, 3.2, -13.2, { cast: false });
  const pf = add(new THREE.Mesh(new THREE.PlaneGeometry(4.8, 2.4), mat(0x2A2D3C, { roughness: .5 })), false, true); pf.rotation.x = -Math.PI / 2; pf.position.set(-8.6, .002, -13.2);
}

// ================================================================= THE DOOR (x = -11, facing +x; hinge at z -12.45, opens into the vault)
const DOOR = {};
{
  mkSet("door");
  const stone = mat(0x3B3F52, { roughness: .85 });
  box(.6, 3.4, 1.0, stone, -11.1, 1.7, -11.85, { cast: false });
  box(.6, 3.4, 1.0, stone, -11.1, 1.7, -14.55, { cast: false });
  box(.6, .9, 3.7, stone, -11.1, 2.95, -13.2, { cast: false });
  DOOR.pivot = new THREE.Group(); DOOR.pivot.position.set(-11.0, 0, -12.45); PARENT.add(DOOR.pivot);
  const slab = new THREE.MeshStandardMaterial({ color: 0x2E3346, roughness: .55, metalness: .4, envMap: ENV, envMapIntensity: .5 });
  box(.16, 2.5, 1.5, slab, 0, 1.25, -.75, { parent: DOOR.pivot });
  for (const y of [.5, 1.25, 2.0]) box(.04, .12, 1.4, metal(0x8C93A8, .4), .1, y, -.75, { parent: DOOR.pivot });
  DOOR.seamM = additive(CYAN, 1);
  // glowing seams: a frame of thin bars just in front of the opening
  for (const [w, h, y, z] of [[.05, 2.6, 1.3, -12.42], [.05, 2.6, 1.3, -13.98], [.05, .05, 2.52, -13.2], [.05, .05, .02, -13.2]]) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(.05, h, z === -13.2 ? 1.6 : .05), DOOR.seamM); m.position.set(-10.84, y, z); PARENT.add(m);
  }
  DOOR.plate = plane(1.5, .42, texMat("github"), -10.78, 2.95, -13.2, Math.PI / 2);
  DOOR.key = new THREE.Mesh(new THREE.CircleGeometry(.07, 20), DOOR.seamM); DOOR.key.position.set(.09, 1.2, -1.25); DOOR.key.rotation.y = Math.PI / 2; DOOR.pivot.add(DOOR.key);
  // the gold light that pours out when it opens: a fan of additive planes
  DOOR.spillM = additive(0xFFC86A, 0);
  DOOR.spill = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 2.6), DOOR.spillM); DOOR.spill.position.set(-10.9, 1.3, -13.2); DOOR.spill.rotation.y = Math.PI / 2; PARENT.add(DOOR.spill);
  const floorSpill = new THREE.Mesh(new THREE.PlaneGeometry(4, 1.8), DOOR.spillM); floorSpill.rotation.x = -Math.PI / 2; floorSpill.position.set(-8.9, .01, -13.2); PARENT.add(floorSpill);
}

// ================================================================= THE VAULT (x -11 .. -30, z -21 .. -5, ceiling 7.5)
const VAULT = {};
{
  mkSet("vault");
  const goldTile = cvs(256, 256, (g, w, h) => { g.fillStyle = "#3A2A1C"; g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { g.fillStyle = (i + j) % 2 ? "#4A3522" : "#43301F"; g.fillRect(i * 64 + 2, j * 64 + 2, 60, 60); } g.strokeStyle = "#C9932F"; g.lineWidth = 3; g.strokeRect(1, 1, w - 2, h - 2); g.beginPath(); g.moveTo(w / 2, 0); g.lineTo(w / 2, h); g.moveTo(0, h / 2); g.lineTo(w, h / 2); g.stroke(); });
  goldTile.wrapS = goldTile.wrapT = THREE.RepeatWrapping; goldTile.repeat.set(5, 4);
  const fl = add(new THREE.Mesh(new THREE.PlaneGeometry(20, 17), new THREE.MeshPhysicalMaterial({ map: goldTile, roughness: .3, clearcoat: .8, clearcoatRoughness: .2, envMap: ENV, envMapIntensity: .6 })), false, true);
  fl.rotation.x = -Math.PI / 2; fl.position.set(-20.5, 0, -13);
  // a red carpet down the aisle
  const carpet = add(new THREE.Mesh(new THREE.PlaneGeometry(14, 1.6), mat(0x8E1F2B, { roughness: .9 })), false, true); carpet.rotation.x = -Math.PI / 2; carpet.position.set(-18.5, .006, -13);
  const stone = mat(0x4A3B33, { roughness: .9 }), trim = metal(0xD9A441, .3);
  box(.4, 7.5, 17, stone, -30.2, 3.75, -13, { cast: false });                            // back wall
  box(19, 7.5, .4, stone, -20.5, 3.75, -21.2, { cast: false });                          // left wall (z -21)
  box(19, 7.5, .4, stone, -20.5, 3.75, -4.8, { cast: false });                           // right wall
  box(.4, 7.5, 6.6, stone, -11.2, 3.75, -18.1, { cast: false });                         // entrance wall, both sides of the door
  box(.4, 7.5, 6.6, stone, -11.2, 3.75, -8.0, { cast: false });
  box(.4, 4.1, 3.7, stone, -11.2, 5.45, -13.2, { cast: false });
  box(20, .4, 17, mat(0x2A1E18), -20.5, 7.6, -13, { cast: false });
  for (const z of [-20.9, -5.1]) box(19, .14, .1, trim, -20.5, 4.6, z, { cast: false });
  // pillars with glowing crystals
  VAULT.crystals = [];
  for (const x of [-13.5, -17.2, -20.9, -24.6]) for (const z of [-19.6, -6.4]) {
    if (z < -13 && x < -20) continue;     // the secret alcove stands there
    box(1.0, 7.5, 1.0, mat(0x5A4638, { roughness: .8 }), x, 3.75, z, { cast: false });
    box(1.2, .3, 1.2, trim, x, 4.4, z, { cast: false });
    const cr = add(new THREE.Mesh(new THREE.OctahedronGeometry(.28), glow(0xFFD27A)), false, false); cr.position.set(x, 4.9, z + (z < -13 ? .7 : -.7)); VAULT.crystals.push(cr);
  }
  // gold: coin piles along the walls (instanced) and stacks of bars
  const coinG = new THREE.CylinderGeometry(.11, .11, .025, 12);
  const N = 1400, coins = new THREE.InstancedMesh(coinG, metal(0xF2C14E, .25, { emissive: 0x5A3A00, emissiveIntensity: .35 }), N);
  let n = 0;
  const pile = (cx, cz, r, hgt, cnt) => { for (let i = 0; i < cnt && n < N; i++, n++) { const a = hash(n * 1.3) * 6.283, d = Math.sqrt(hash(n * 2.7)) * r, x = cx + Math.cos(a) * d, z = cz + Math.sin(a) * d, y = Math.max(0, hgt * (1 - (d / r) ** 1.6)) * hash(n * 5.1) + .015; M4.compose(V.set(x, y, z), Q.setFromEuler(EU.set((hash(n * 7) - .5) * .9, 0, (hash(n * 9) - .5) * .9)), S3.set(1, 1, 1)); coins.setMatrixAt(n, M4); } };
  for (const [cx, cz, r, h] of [[-14, -20, 1.6, .8], [-17.6, -20.1, 1.4, .9], [-27.6, -19.4, 1.8, 1.1], [-28.6, -16.5, 1.6, .9], [-28.6, -9.5, 1.6, .9], [-25.5, -6.4, 2.4, 1.3], [-19, -5.8, 1.8, 1.0], [-14, -6.0, 1.6, .8]]) pile(cx, cz, r, h, 170);
  coins.count = n; coins.castShadow = false; coins.receiveShadow = true; PARENT.add(coins);
  for (const [x, z] of [[-16, -19.8], [-16, -6.2], [-22.5, -6.2]]) for (let r = 0; r < 3; r++) for (let q = 0; q < 4 - r; q++) box(.5, .18, .24, metal(0xF0BE45, .22), x + (q - (3 - r) / 2) * .52, .09 + r * .18, z, { cast: false });
  // the mythic dais at the back and its steps
  box(4.2, .5, 4.2, mat(0x3A2B25), -26.2, .25, -13, {});
  box(3.6, .5, 3.6, mat(0x43322A), -26.2, .75, -13, {});
  box(3.0, .5, 3.0, mat(0x4D3A30), -26.2, 1.25, -13, {});
  VAULT.ringM = additive(0xFF2E4D, .0);
  VAULT.ring = new THREE.Mesh(new THREE.RingGeometry(1.15, 1.35, 48), VAULT.ringM); VAULT.ring.rotation.x = -Math.PI / 2; VAULT.ring.position.set(-26.2, 1.52, -13); PARENT.add(VAULT.ring);
  // the legendary step
  box(2.2, .25, 2.2, mat(0x4D3A30), -21.6, .125, -13, {});
  // the secret alcove in the left wall: three chests behind bars
  box(5.4, .9, 2.0, mat(0x2A2030), -22.2, .45, -19.9, {});
  box(5.8, .3, 2.2, mat(0x2A2030), -22.2, 4.2, -19.9, { cast: false });
  VAULT.barsM = metal(0x55525E, .45);
  for (let i = 0; i < 15; i++) cyl(.04, .04, 3.3, VAULT.barsM, -24.9 + i * .385, 2.55, -18.75, 8);
  box(5.6, .12, .12, VAULT.barsM, -22.2, 4.05, -18.75, {}); box(5.6, .12, .12, VAULT.barsM, -22.2, 1.05, -18.75, {});
  // dust motes in the gold light
  const MOTES = 220;
  VAULT.motes = new THREE.InstancedMesh(new THREE.OctahedronGeometry(.018), glow(0xFFE2A0), MOTES); VAULT.motes.frustumCulled = false; PARENT.add(VAULT.motes);
}

// ================================================================= CHESTS
// [rarity, x, y, z, ry, scale]
const CH = [
  ["rare", -14.4, 0, -11.2, Math.PI, 1],
  ["rare", -14.4, 0, -14.8, 0, 1],
  ["epic", -18.0, 0, -11.2, Math.PI, 1.08],
  ["epic", -18.0, 0, -14.8, 0, 1.08],
  ["legendary", -21.6, .25, -13, Math.PI / 2, 1.22],
  ["mythic", -26.2, 1.5, -13, Math.PI / 2, 1.38],
  ["secret", -23.9, .9, -19.9, 0, .9],
  ["secret", -22.2, .9, -19.9, 0, .9],
  ["secret", -20.5, .9, -19.9, 0, .9],
];
const STYLE = {
  rare: { wood: 0x7A5233, trim: 0x3D8BFF, glowC: RAR.rare },
  epic: { wood: 0x3E2556, trim: 0xC07BFF, glowC: RAR.epic },
  legendary: { wood: 0xE8B544, trim: 0xFFF1C4, glowC: RAR.legendary, metalWood: true },
  mythic: { wood: 0x1C1218, trim: 0xFF3A55, glowC: RAR.mythic },
  secret: { wood: 0x2B2A36, trim: 0x8C8A99, glowC: RAR.secret },
};
const CHESTS = [];
function makeChest(rar, x, y, z, ry, s) {
  PARENT = SET.vault;
  const st = STYLE[rar];
  const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; g.scale.setScalar(s); PARENT.add(g);
  const inner = new THREE.Group(); g.add(inner);     // shakes and hops
  const woodM = st.metalWood ? metal(st.wood, .25, { emissive: 0x3A2400, emissiveIntensity: .3 }) : plastic(st.wood, { roughness: .55, clearcoat: .4 });
  const trimM = rar === "mythic" ? glow(st.trim) : metal(st.trim, .25, { emissive: st.trim, emissiveIntensity: rar === "secret" ? 0 : .25 });
  const P0 = PARENT; PARENT = inner;
  box(1.0, .55, .66, woodM, 0, .275, 0, { round: .04 });
  for (const xx of [-.38, .38]) box(.08, .57, .68, trimM, xx, .275, 0, {});
  box(1.02, .07, .68, trimM, 0, .52, 0, {});
  // the inner glow, seen when the lid opens
  const glowIn = new THREE.Mesh(new THREE.PlaneGeometry(.86, .54), additive(st.glowC, 0)); glowIn.rotation.x = -Math.PI / 2; glowIn.position.y = .56; inner.add(glowIn);
  const lid = new THREE.Group(); lid.position.set(0, .55, -.33); inner.add(lid);
  PARENT = lid;
  const top = new THREE.Mesh(new THREE.CylinderGeometry(.33, .33, 1.0, 10, 1, false, 0, Math.PI), woodM); top.rotation.set(0, 0, Math.PI / 2); top.position.set(0, 0, .33); top.castShadow = true; lid.add(top);
  for (const xx of [-.38, .38]) { const b = new THREE.Mesh(new THREE.CylinderGeometry(.345, .345, .08, 10, 1, false, 0, Math.PI), trimM); b.position.set(xx, 0, .33); b.rotation.set(0, 0, Math.PI / 2); lid.add(b); }
  const lock = box(.18, .22, .06, rar === "mythic" ? glow(0xFF8A9A) : metal(0xFFD36B, .2), 0, -.02, .68, {});
  PARENT = inner;
  let pad = null, chains = [];
  if (rar === "secret") {
    pad = new THREE.Group(); pad.position.set(0, .42, .4); inner.add(pad);
    box(.24, .22, .1, metal(0xC9A23A, .3), 0, 0, 0, { parent: pad });
    const sh = new THREE.Mesh(new THREE.TorusGeometry(.08, .025, 8, 16, Math.PI), metal(0xBFC3CC, .3)); sh.position.y = .11; pad.add(sh);
    for (const a of [-.55, .55]) { const c = box(1.15, .05, .05, metal(0x7A7C88, .4), 0, .32, .34, { rz: a }); chains.push(c); }
  }
  if (rar === "mythic") { for (let i = 0; i < 6; i++) box(.02, .3 + hash(i) * .2, .01, glow(0xFF4A63), -.4 + i * .16, .28, .335, { rz: (hash(i * 3) - .5) * .8 }); }
  PARENT = P0;
  // the beam, the burst, the item
  const beamM = additive(st.glowC, 0);
  const beam = new THREE.Mesh(new THREE.CylinderGeometry(.3, .52, 7, 24, 1, true), beamM); beam.position.y = 3.9; inner.add(beam);
  const NB = rar === "mythic" ? 160 : rar === "legendary" ? 120 : 60;
  const burst = new THREE.InstancedMesh(new THREE.BoxGeometry(.06, .06, .06), glow(new THREE.Color(st.glowC).lerp(new THREE.Color(0xffffff), .25)), NB); burst.frustumCulled = false; g.add(burst);
  const coinsB = rar === "legendary" || rar === "mythic" ? new THREE.InstancedMesh(new THREE.CylinderGeometry(.07, .07, .016, 10), metal(0xFFD15C, .2, { emissive: 0x6A4200, emissiveIntensity: .5 }), 90) : null;
  if (coinsB) { coinsB.frustumCulled = false; g.add(coinsB); }
  const gem = new THREE.Group(); inner.add(gem);
  const gm = new THREE.Mesh(new THREE.OctahedronGeometry(.17), new THREE.MeshPhysicalMaterial({ color: st.glowC, emissive: st.glowC, emissiveIntensity: 1.4, roughness: .1, clearcoat: 1, toneMapped: false })); gem.add(gm);
  const halo = new THREE.Mesh(new THREE.RingGeometry(.24, .29, 40), additive(st.glowC, .8)); gem.add(halo);
  const holo = rar === "secret" ? new THREE.Mesh(new THREE.PlaneGeometry(.5, .5), texMat("q", { transparent: true, depthWrite: false })) : null;
  if (holo) { holo.position.set(0, 1.15, 0); inner.add(holo); }
  const o = { rar, g, inner, lid, glowIn, beam, beamM, burst, coinsB, gem, halo, pad, chains, holo, s, base: v3(x, y, z) };
  CHESTS.push(o); return o;
}
for (const c of CH) makeChest(...c);

// chest timeline: shake from a, open at b (lid flips, burst, beam, gem rises)
function updChest(o, t, a, b, o2 = {}) {
  const shake = a == null ? 0 : ss(t, a, a + .25) * (b == null ? 1 : 1 - ss(t, b, b + .05));
  const amp = (o.rar === "mythic" ? 2.2 : o.rar === "legendary" ? 1.5 : 1) * shake * (o2.shakeAmp ?? 1);
  o.inner.rotation.z = .07 * amp * Math.sin(t * 43) ; o.inner.rotation.x = .04 * amp * Math.sin(t * 37 + 1);
  o.inner.position.y = .05 * amp * Math.abs(Math.sin(t * 19)) + (o2.lev ?? 0);
  const u = b == null ? 0 : ramp(t, b, b + .42);
  const crack = shake * (.06 + .05 * Math.sin(t * 31));
  o.lid.rotation.x = -(u > 0 ? 1.95 * backOut(u, 2.2) : crack);
  o.glowIn.material.opacity = Math.max(shake * .4, u > 0 ? .55 : 0);
  const k = b == null ? -1 : t - b;
  o.beamM.opacity = k < 0 ? shake * .03 : (.38 * Math.exp(-k * 2.5) + .08) * (o2.beamHold ?? 1);
  o.beam.scale.set(1 + .4 * Math.exp(-k * 3), k < 0 ? .2 : Math.min(1, .2 + k * 5), 1 + .4 * Math.exp(-k * 3));
  // burst: cubes fly out and fall
  const NB = o.burst.count;
  for (let i = 0; i < NB; i++) {
    if (k < 0 || k > 2.6) { M4.makeScale(0, 0, 0); o.burst.setMatrixAt(i, M4); continue; }
    const a1 = hash(i * 3.3 + o.base.x) * 6.283, sp = 1.2 + hash(i * 1.9) * 2.4 * (o.rar === "mythic" ? 1.8 : 1), up = 2.5 + hash(i * 4.7) * 3.5;
    const x = Math.cos(a1) * sp * k, z = Math.sin(a1) * sp * k, y = .6 + up * k - 4.9 * k * k;
    const sc = Math.max(0, 1 - k / 2.4) * (y < 0 ? 0 : 1) * (.6 + hash(i) * .9);
    M4.compose(V.set(x, Math.max(0, y), z), Q.setFromEuler(EU.set(k * 7 + i, k * 5, 0)), S3.setScalar(sc)); o.burst.setMatrixAt(i, M4);
  }
  o.burst.instanceMatrix.needsUpdate = true;
  if (o.coinsB) {
    for (let i = 0; i < o.coinsB.count; i++) {
      const kk = k - hash(i * 2.1) * .9;
      if (k < 0 || kk < 0 || kk > 3) { M4.makeScale(0, 0, 0); o.coinsB.setMatrixAt(i, M4); continue; }
      const a1 = hash(i * 5.3) * 6.283, sp = .5 + hash(i * 7.1) * 1.6, up = 4 + hash(i * 1.1) * 2.5;
      const y = .7 + up * kk - 4.9 * kk * kk;
      M4.compose(V.set(Math.cos(a1) * sp * kk, Math.max(.01, y), Math.sin(a1) * sp * kk), Q.setFromEuler(EU.set(kk * 9 + i, 0, kk * 6)), S3.setScalar(y < 0 ? .9 : 1)); o.coinsB.setMatrixAt(i, M4);
    }
    o.coinsB.instanceMatrix.needsUpdate = true;
  }
  // the gem rises out of the chest and hovers, spinning
  const gu = k < 0 ? 0 : backOut(ramp(k, .05, .7), 1.4);
  o.gem.visible = k > 0;
  o.gem.position.set(0, .45 + gu * 1.05 + .05 * Math.sin(t * 2.6), 0);
  o.gem.rotation.y = t * 2.4; o.gem.scale.setScalar(.2 + .8 * gu);
  o.halo.lookAt(camera.position);
}

// ================================================================= TEXTURES (after the fonts and the logos load)
const IMG = {};
const loadImg = (k, src) => new Promise((res) => { const i = new Image(); i.onload = () => { IMG[k] = i; res(); }; i.onerror = () => res(); i.src = src; });
function cover(g, img, x, y, w, h, crop) { if (!img) return; const [sx, sy, sw, sh] = crop || [0, 0, img.width, img.height]; g.drawImage(img, sx, sy, sw, sh, x, y, w, h); }
function signTex(key) {
  return cvs(1024, 245, (g, w, h) => {
    g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h);
    const name = { typeform: "Typeform", zapier: "Zapier", mailchimp: "Mailchimp", docusign: "DocuSign", otter: "Otter.ai", ga: "Google Analytics", figma: "Figma", capcut: "CapCut Pro", buffer: "Buffer", pro: "PRO PLAN", pro2: "PREMIUM+", pro3: "PRO MAX" }[key];
    const iw = IMG.typeform ? IMG.typeform.width : 1;
    if (key === "typeform" && IMG.typeform) { const ih = IMG.typeform.height; cover(g, IMG.typeform, 0, 0, w, h, [iw * .22, ih * .36, iw * .56, ih * .28]); }
    else if (key === "zapier" && IMG.zapier) { cover(g, IMG.zapier, 40, 0, w - 80, h, [0, IMG.zapier.height * .26, IMG.zapier.width, IMG.zapier.height * .48]); }
    else {
      let x0 = 60;
      if (key === "mailchimp" && IMG.mailchimp) { cover(g, IMG.mailchimp, 40, 20, 205, 205); x0 = 280; }
      if (key === "otter" && IMG.otter) { g.save(); rr(g, 40, 22, 200, 200, 40); g.clip(); cover(g, IMG.otter, 40, 22, 200, 200); g.restore(); x0 = 280; }
      g.fillStyle = key === "mailchimp" ? "#241C15" : key === "docusign" ? "#130032" : key === "otter" ? "#1A2B6B" : "#202124"; g.textBaseline = "middle";
      let f = 120; g.font = FT(800, f); while (g.measureText(name).width > w - x0 - 50 && f > 40) { f -= 4; g.font = FT(800, f); }
      g.fillText(name, x0, h / 2 + 6);
    }
    g.strokeStyle = "rgba(0,0,0,.08)"; g.lineWidth = 8; g.strokeRect(4, 4, w - 8, h - 8);
  });
}
function tagTex(key) {
  const s = SHOPS.find((q) => q[2] === key) || SHOPS[1];
  return cvs(600, 840, (g, w, h) => {
    g.fillStyle = "#FFF9F0"; rr(g, 10, 10, w - 20, h - 20, 46); g.fill();
    g.fillStyle = s[3]; rr(g, 10, 10, w - 20, 170, 46); g.fill(); g.fillRect(10, 120, w - 20, 60);
    g.fillStyle = "#FFF9F0"; g.beginPath(); g.arc(w / 2, 82, 30, 0, 7); g.fill();
    g.strokeStyle = "#C9B9A6"; g.lineWidth = 8; g.beginPath(); g.arc(w / 2, 82, 30, 0, 7); g.stroke();
    const name = { typeform: "TYPEFORM", zapier: "ZAPIER", mailchimp: "MAILCHIMP", docusign: "DOCUSIGN", otter: "OTTER.AI", ga: "G. ANALYTICS", figma: "FIGMA", capcut: "CAPCUT PRO", buffer: "BUFFER", pro: "PRO PLAN", pro2: "PREMIUM+", pro3: "PRO MAX" }[key];
    g.fillStyle = "#1E1B18"; g.textAlign = "center"; g.font = FT(800, 54); g.fillText(name, w / 2, 270);
    g.font = FT(800, 38); g.fillStyle = "#8A7F74"; g.fillText(key === "ga" ? "PRICE" : "FROM", w / 2, 360);
    let f = 210; g.font = FT(800, f); while (g.measureText(s[4]).width > w - 70) { f -= 6; g.font = FT(800, f); }
    g.fillStyle = key === "ga" ? "#1E1B18" : "#D92D20"; g.fillText(s[4], w / 2, 560);
    g.font = FT(800, key === "ga" ? 46 : 64); g.fillStyle = "#1E1B18"; g.fillText(key === "ga" ? "*you pay with" : "PER MONTH", w / 2, 660);
    if (key === "ga") g.fillText("your data", w / 2, 718);
    g.textAlign = "left";
  });
}
async function buildTextures() {
  await Promise.all([loadImg("typeform", "assets/img/typeform.webp"), loadImg("mailchimp", "assets/img/mailchimp.png"), loadImg("otter", "assets/img/otter.png"), loadImg("zapier", "assets/img/zapier.png")]);
  for (const s of SHOPS) { TEX["sign_" + s[2]] = signTex(s[2]); TEX["tag_" + s[2]] = tagTex(s[2]); }
  TEX.github = cvs(768, 215, (g, w, h) => {
    g.fillStyle = "#11141C"; rr(g, 4, 4, w - 8, h - 8, 30); g.fill(); g.strokeStyle = "#45F3FF"; g.lineWidth = 6; rr(g, 10, 10, w - 20, h - 20, 26); g.stroke();
    g.fillStyle = "#EFFFFF"; g.font = FT(800, 118); g.textAlign = "center"; g.textBaseline = "middle"; g.shadowColor = "#45F3FF"; g.shadowBlur = 24; g.fillText("GitHub", w / 2, h / 2 + 6);
  });
  TEX.q = cvs(256, 256, (g, w, h) => { g.fillStyle = "#B9A8FF"; g.shadowColor = "#8F7BFF"; g.shadowBlur = 30; g.font = FT(800, 220); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("?", w / 2, h / 2 + 10); });
  for (const [m, key] of LATE) { if (TEX[key]) { m.map = TEX[key]; m.needsUpdate = true; } }
}

// ================================================================= SHOTS
// a chest shot: a high three-quarter game angle, the chest left of centre and the bot beside it on the right
function chestFrame(ci, o = {}) {
  const [, x, y, z, ry, s] = CH[ci];
  const F = v3(Math.sin(ry), 0, Math.cos(ry)), R = v3(F.z, 0, -F.x), P = v3(x, y, z);
  const d = o.d ?? 3.4, hgt = o.h ?? 2.05, side = o.side ?? 1;
  const cam = P.clone().addScaledVector(F, d).addScaledVector(R, -.35 * side); cam.y = hgt;
  const lk = P.clone().addScaledVector(R, .42 * side); lk.y = (o.ly ?? 1.0) + y;
  const bot = P.clone().addScaledVector(R, (1.0 + .1 * s) * side).addScaledVector(F, -.12);
  return { cam, lk, bot, R, F };
}
const CF = [0, 1, 2, 3].map((i) => chestFrame(i)).concat([chestFrame(4, { d: 3.6, h: 2.2, ly: 1.1 })]);
const shotC = (i, push = .25, rise = -.08, fov = 58) => { const f = CF[i]; return { p0: f.cam.clone(), p1: f.cam.clone().addScaledVector(f.F, -push).add(v3(0, rise, 0)), l0: f.lk.clone(), l1: f.lk.clone().add(v3(0, .06, 0)), fov, ap: .16 }; };
// [start, {p0, p1, l0, l1, fov, fov1, ap, f}]  (positions and look targets lerp over the shot, eased)
const SHOTS = [
  [0, { p0: v3(1.45, 1.2, 7.0), p1: v3(1.3, 1.15, 6.4), l0: v3(.05, 1.12, 2.4), l1: v3(.05, 1.1, 2.4), fov: 44, ap: .35 }],
  [K.cB, { p0: v3(1.15, .75, 3.7), p1: v3(1.1, .85, .1), l0: v3(.5, 2.1, -8), l1: v3(.4, 2.2, -12), fov: 60, ap: .16 }],
  [K.cC, { p0: v3(-1.5, 1.4, -12.45), p1: v3(-3.6, 1.3, -12.85), l0: v3(-11, 1.25, -13.2), l1: v3(-11, 1.3, -13.2), fov: 40, ap: .25 }],
  [K.cD, { p0: v3(-13.6, .85, -13.6), p1: v3(-13.3, .9, -13.5), l0: v3(-9.4, 1.0, -13.2), l1: v3(-9.4, 1.0, -13.2), fov: 36, ap: .3 }],
  [K.cE, { p0: v3(-11.65, 2.6, -13.95), p1: v3(-11.9, 2.25, -14.1), l0: v3(-19.5, .45, -13.0), l1: v3(-19.5, .4, -13.0), fov: 56, ap: .12 }],
  [K.cF, shotC(0)],
  [K.cG, shotC(1)],
  [K.cH1, shotC(2)],
  [K.cH2, shotC(3)],
  [K.cI1, shotC(4, .45, -.15, 58)],
  [K.cI2, { p0: v3(-18.6, 1.75, -11.3), p1: v3(-18.7, 1.85, -14.6), l0: v3(-21.9, 1.2, -13.5), l1: v3(-21.9, 1.25, -13.6), fov: 56, ap: .18 }],
  [K.cJ1, { p0: v3(-19.2, 1.1, -10.0), p1: v3(-19.6, 1.15, -10.2), l0: v3(-26.2, 2.25, -13.0), l1: v3(-26.2, 2.35, -13.0), fov: 50, ap: .14 }],
  [K.cJ2, { p0: v3(-21.7, 2.05, -13.5), p1: v3(-22.6, 2.1, -13.35), l0: v3(-26.2, 2.95, -13.0), l1: v3(-26.2, 3.0, -13.0), fov: 58, ap: .2 }],
  [K.cK, { p0: v3(-19.4, 1.1, -15.2), p1: v3(-19.7, 1.05, -14.9), l0: v3(-25.8, 3.0, -13.0), l1: v3(-25.8, 3.1, -13.0), fov: 60, ap: .1 }],
  [K.cL, { p0: v3(-18.3, 2.55, -9.7), p1: v3(-18.6, 2.45, -9.95), l0: v3(-24.2, 1.3, -12.8), l1: v3(-24.2, 1.35, -12.8), fov: 52, ap: .12 }],
  [K.cM, { p0: v3(-19.9, 1.85, -14.7), p1: v3(-23.0, 1.8, -14.9), l0: v3(-21.0, 1.45, -19.6), l1: v3(-22.6, 1.45, -19.6), fov: 52, ap: .18 }],
  [K.cN, { p0: v3(-22.15, 1.25, -14.85), p1: v3(-22.15, 1.22, -15.1), l0: v3(-22.2, 1.33, -17.6), l1: v3(-22.2, 1.33, -17.6), fov: 50, ap: .3 }],
  [K.cO, { p0: v3(-22.2, 1.2, -14.3), p1: v3(-22.2, 1.18, -14.55), l0: v3(-22.2, 1.62, -17.6), l1: v3(-22.2, 1.62, -17.6), fov: 52, ap: .25 }],
];
function shotAt(t) {
  let i = 0; while (i + 1 < SHOTS.length && t >= SHOTS[i + 1][0]) i++;
  const [a, s] = SHOTS[i], b = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR;
  const u = sm(clamp((t - a) / Math.max(.1, b - a)));
  const p = s.p1 ? V.lerpVectors(s.p0, s.p1, u).clone() : s.p0.clone();
  const l = s.l1 ? V2.lerpVectors(s.l0, s.l1, u).clone() : s.l0.clone();
  return { i, a, b, u, p, l, fov: lerp(s.fov, s.fov1 ?? s.fov, u), ap: s.ap, f: s.f ?? null };
}

// ================================================================= THE BOT'S PERFORMANCE
const ry2 = (fx, fz, tx, tz) => Math.atan2(tx - fx, tz - fz);
function botAt(t, sh) {
  const i = sh.i;
  let p, f = { eyes: "open", mouth: "smile" };
  if (i === 0) {        // peeking out from behind the giant price tag, whispering to camera
    const lean = ss(t, .0, .35);
    p = pose({ x: .45, z: 2.35, ry: .32, crouch: .06, lean: .1, tw: .25 * lean, hr: -.18 * lean, hy: .1, a: [[.9, .2, 1.7], [1.5, .3, 2.1]], l: [[.25, .3], [.1, .2]] });
    p.a[1] = [1.65 + .1 * Math.sin(t * 3), .1, 2.35];   // a hand to the mouth: psst
    if (t > .55) p.a[1] = [lerp(1.65, .8, ss(t, .55, .9)), .3, lerp(2.35, 1.6, ss(t, .55, .9))];
    f = { eyes: t < 1.0 ? "open" : "sly", mouth: "smirk", look: t < .7 ? .4 : -.2 };
    p = idle(p, t);
  } else if (i === 1) { // tiptoeing down the mall, past the price tags
    const u = ramp(t, K.cB, K.cC);
    p = sneak(pose({ x: .95, z: lerp(1.3, -2.6, u), ry: Math.PI }), (t - K.cB) * 7.5);
    p.hy = .45 * Math.sin((t - K.cB) * 2.6); f = { eyes: "open", mouth: "smile", look: Math.sin((t - K.cB) * 2.6) > 0 ? .6 : -.6 };
  } else if (i === 2) { // into the dark passage, towards the glowing door
    const u = ramp(t, K.cC, K.door - .25);
    p = sneak(pose({ x: lerp(-4.7, -9.55, u), z: -13.2, ry: -Math.PI / 2 }), (t - K.cC) * 7.0, .8 * (1 - ss(t, K.door - .4, K.door - .2)));
    p.hy = 0; f = { eyes: "wide", mouth: "o" };
    if (t > K.door - .4) p.a[0] = [lerp(1.05, 1.45, ss(t, K.door - .4, K.door)), .1, lerp(1.9, .35, ss(t, K.door - .4, K.door))];
  } else if (i === 3) { // the door opens: gold light on its face
    const u = ss(t, K.door, K.door + .5);
    p = pose({ x: -9.15, z: -13.15, ry: -Math.PI / 2 - .12, crouch: .02, lean: -.12 * u, hp: -.12 * u, a: mixP(pose(), pose({ a: WOW }), u).a });
    f = { eyes: u > .3 ? "star" : "wide", mouth: u > .3 ? "grin" : "o" };
  } else if (i === 4) { // steps into the vault
    const u = ramp(t, K.cE - .1, K.cF + .3);
    p = walk(pose({ x: lerp(-14.3, -16.2, u), z: -13.0, ry: -Math.PI / 2 }), (t - K.cE) * 9, .9);
    p.hy = .3 * Math.sin((t - K.cE) * 3); f = { eyes: "star", mouth: "grin" };
  } else if (i >= 5 && i <= 8) {     // behind each rare and epic chest, peering over it at the camera
    const bx = CF[i - 5].bot.x, bz = CF[i - 5].bot.z;
    const ta = [K.openR1, K.openR2, K.openE1, K.openE2][i - 5], cam = SHOTS[i][1].p0, cx = CH[i - 5][1], cz = CH[i - 5][3];
    const u = ss(t, ta, ta + .3);
    const toCam = ry2(bx, bz, cam.x, cam.z), toChest = ry2(bx, bz, cx, cz);
    p = pose({ x: bx, z: bz, ry: toCam, hy: lerp(clamp(toChest - toCam, -.9, .9), 0, u), hp: lerp(.25, -.05, u), lean: lerp(.12, -.05, u), a: mixP(pose({ a: WOW }), pose({ a: CHEER }), u).a, crouch: .04 * (1 - u) });
    p.y = .14 * Math.max(0, Math.sin((t - ta) * 9)) * (t > ta && t < ta + .7 ? 1 : 0);
    f = { eyes: u > .5 ? "happy" : "wide", mouth: u > .5 ? "grin" : "o" };
    p = idle(p, t);
  } else if (i === 9 || i === 10) {  // the legendary chest: awe, then a dance in the coin rain
    const u = ss(t, K.openG, K.openG + .3), cam = SHOTS[i][1].p0;
    const bx = CF[4].bot.x, bz = CF[4].bot.z;
    p = pose({ x: bx, z: bz, ry: ry2(bx, bz, cam.x, cam.z), hy: -.5 * (1 - u), hp: -.12, a: mixP(pose({ a: WOW }), pose({ a: CHEER }), u).a });
    if (t > K.openG + .4) { const d = t - K.openG; p.y = .1 * Math.abs(Math.sin(d * 7)); p.tw = .25 * Math.sin(d * 7); p.a = [[2.6 + .3 * Math.sin(d * 7), .5, .4], [2.6 - .3 * Math.sin(d * 7), .5, .4]]; }
    f = { eyes: u > .5 ? "star" : "wide", mouth: u > .5 ? "grin" : "o" };
    p = idle(p, t);
  } else if (i === 11 || i === 12) { // the dark: looking up at the mythic chest
    p = pose({ x: -23.4, z: -12.15, ry: -Math.PI / 2 + .1, hp: -.32, hy: -.15, crouch: .05, a: [[.6, .25, 1.3], [.6, .25, 1.3]] });
    f = { eyes: "wide", mouth: "o", noblink: true };
    p = idle(p, t);
  } else if (i === 13 || i === 14) { // blown back by the blast, then a victory jump
    const d = t - K.myth;
    const knock = d > 0 && d < .8 ? Math.sin(Math.min(1, d / .8) * Math.PI) : 0;
    p = pose({ x: -23.4 + .55 * ss(d, 0, .35), z: -12.15, ry: -Math.PI / 2 + (d > .9 ? 1.3 : .3), lean: -.35 * knock, hp: -.2, a: knock > .1 ? [[1.6, .9, .4], [1.6, .9, .4]] : CHEER });
    if (d > .9) { const j = d - .9; p.y = .2 * Math.abs(Math.sin(j * 5.5)); p.l = [[.3 * Math.abs(Math.sin(j * 5.5)), .6 * Math.abs(Math.sin(j * 5.5))], [.3 * Math.abs(Math.sin(j * 5.5)), .6 * Math.abs(Math.sin(j * 5.5))]]; p.a = [[2.8, .3 + .2 * Math.sin(j * 11), .3], [2.8, .3 + .2 * Math.sin(j * 11 + 1), .3]]; }
    f = { eyes: knock > .2 ? "closed" : "star", mouth: knock > .2 ? "o" : "grin" };
  } else if (i === 15) {             // walks to the secret alcove
    const u = ramp(t, K.cM, K.cN - .3);
    p = walk(pose({ x: lerp(-19.6, -20.5, u), z: lerp(-16.9, -17.4, u), ry: -Math.PI / 2 - .5 }), (t - K.cM) * 8, 1 - ss(t, K.cN - .5, K.cN - .2));
    p.hy = -.5;
    f = { eyes: "open", mouth: "smile", look: .3 };
  } else if (i === 16) {             // turns to camera, leans in: only in DMs (a wink)
    const u = ss(t, K.cN, K.cN + .4);
    p = pose({ x: -22.2, z: -17.6, ry: lerp(Math.PI, 0, u), lean: .18 * u, hr: .1 * u, a: [[.3, .2, .6], [lerp(.3, 1.5, u), .3, lerp(.6, 1.9, u)]] });
    const w = t > K.wink && t < K.wink + .55;
    f = { eyes: w ? "happy,open" : u > .5 ? "sly" : "open", mouth: "smirk" };
    p = idle(p, t);
  } else {                           // the CTA: holds up the golden key and points at the viewer
    const u = ss(t, K.cO, K.cO + .4);
    p = pose({ x: -22.2, z: -17.6, ry: 0, lean: .08, a: [[lerp(.3, 2.7, u), .25, .2], [lerp(.3, 1.5, u), .1, .05]], hp: .05 });
    if (t > K.endc) { const d = t - K.endc; p.a[1][0] = 1.5 + .12 * Math.sin(d * 6); }
    f = { eyes: "happy", mouth: "grin" };
    p = idle(p, t);
  }
  return [p, f];
}
// the golden key in the bot's raised hand at the end
const KEY = new THREE.Group(); scene.add(KEY);
{
  const km = metal(0xFFCC4D, .2, { emissive: 0x6A4500, emissiveIntensity: .6 });
  const r = new THREE.Mesh(new THREE.TorusGeometry(.09, .03, 10, 24), km); r.position.y = .18; KEY.add(r);
  const sh = new THREE.Mesh(new THREE.BoxGeometry(.04, .26, .04), km); sh.position.y = 0; KEY.add(sh);
  for (const y of [-.08, -.12]) { const b = new THREE.Mesh(new THREE.BoxGeometry(.08, .03, .04), km); b.position.set(.04, y, 0); KEY.add(b); }
  KEY.traverse((o) => { if (o.isMesh) o.castShadow = true; });
}

// ================================================================= LOOKS per stretch
function look(t) {
  if (t < K.cC) return { bg: 0xF2E6DA, fog: [0xF2E6DA, 18, 60], hs: 0xFFF6EA, hg: 0xD9C6B2, hi: .95, sun: 0xFFF1E0, si: 1.9, sd: [3, 10, 4], warm: .06, cool: 0, sat: 1.15, vig: .26, bloom: .3, exp: .92, set: "mall" };
  if (t < K.cD) return { bg: 0x0B0D16, fog: [0x0B0D16, 6, 22], hs: 0x6A7CC8, hg: 0x1A1A2A, hi: .45, sun: 0x9FB4FF, si: .3, sd: [4, 10, 2], warm: 0, cool: .2, sat: 1.05, vig: .45, bloom: .42, exp: 1.0, set: "door" };
  if (t < K.cE) return { bg: 0x120A06, fog: [0x1A0E08, 6, 26], hs: 0xFFD9A0, hg: 0x3A2414, hi: .55, sun: 0xFFD08A, si: .6, sd: [3, 10, 2], warm: .3, cool: 0, sat: 1.1, vig: .45, bloom: .45, exp: 1.0, set: "door" };
  if (t < K.cJ1) return { bg: 0x1A100A, fog: [0x2A180C, 14, 40], hs: 0xFFD9A0, hg: 0x4A2E1A, hi: .85, sun: 0xFFD08A, si: 1.6, sd: [3, 10, 2], warm: .28, cool: 0, sat: 1.12, vig: .36, bloom: .42, exp: 1.0, set: "vault" };
  if (t < K.cM) return { bg: 0x0A0406, fog: [0x12060A, 8, 30], hs: 0xFF8A8A, hg: 0x200608, hi: .22, sun: 0xFF6A6A, si: .25, sd: [3, 10, 2], warm: .1, cool: 0, sat: 1.15, vig: .55, bloom: .75, exp: 1.0, set: "vault" };
  return { bg: 0x0E0A16, fog: [0x140E20, 8, 30], hs: 0xC8B4FF, hg: 0x2A1A30, hi: .55, sun: 0xFFD08A, si: .9, sd: [3, 10, 2], warm: .12, cool: .05, sat: 1.1, vig: .42, bloom: .6, exp: 1.0, set: "vault" };
}

// ================================================================= THE FRAME
let SHAKE = 0;
function renderAt(t) {
  NOW = t; SHAKE = 0;
  const lk = look(t), sh = shotAt(t);
  const inMall = t < K.cE;   // the passage and the door belong to both sides
  SET.mall.visible = inMall; SET.door.visible = true; SET.passage.visible = t < K.cE; SET.vault.visible = !inMall || t >= K.cC;
  scene.background = tmpC.set(lk.bg).clone();
  scene.fog.color.set(lk.fog[0]); scene.fog.near = lk.fog[1]; scene.fog.far = lk.fog[2];
  hemi.color.set(lk.hs); hemi.groundColor.set(lk.hg); hemi.intensity = lk.hi;
  sun.color.set(lk.sun); sun.intensity = lk.si;
  renderer.toneMappingExposure = lk.exp;
  for (const l of PL) { l.intensity = 0; l.distance = 8; }
  let flash = 0; const flashC = grade.uniforms.uFlashC.value.setRGB(1, .97, .9);

  // ---- the mall: tags sway
  for (const tg of MALL.tags) { tg.g.rotation.z = .07 * Math.sin(t * 1.3 + tg.seed); tg.g.rotation.y = .1 * Math.sin(t * .8 + tg.seed * 2); }
  MALL.standee.rotation.z = .01 * Math.sin(t * 2);
  // ---- the door
  const du = ss(t, K.door, K.door + .55);
  DOOR.pivot.rotation.y = 1.7 * du;
  DOOR.seamM.opacity = (.75 + .25 * Math.sin(t * 6)) * (1 - du * .6);
  DOOR.spillM.opacity = .22 * du + .2 * pulse(t, K.door + .35, .25);
  DOOR.key.visible = du < .5;
  DOOR.spill.visible = t < K.cD;
  if (t > K.cC && t < K.cF) {
    PL[0].position.set(-10.3, 1.4, -13.2); PL[0].color.set(CYAN); PL[0].intensity = 3.2 * (1 - du) + .6; PL[0].distance = 6;
    PL[1].position.set(-11.8, 1.7, -13.2); PL[1].color.set(0xFFC060); PL[1].intensity = 3.2 * du; PL[1].distance = 6;
  }
  flash = Math.max(flash, .3 * pulse(t, K.door + .38, .12));
  // ---- the vault
  const vt = t - K.cE;
  for (let k = 0; k < VAULT.crystals.length; k++) { const c = VAULT.crystals[k]; c.rotation.y = t * 1.2 + k; c.position.y = 4.9 + .06 * Math.sin(t * 2 + k); }
  for (let i = 0; i < VAULT.motes.count; i++) {
    const x = -12 - hash(i * 1.7) * 17, z = -6 - hash(i * 2.9) * 14, y = ((hash(i * 4.3) * 6 + t * (.08 + hash(i) * .1)) % 6) + .2;
    M4.compose(V.set(x + .3 * Math.sin(t * .5 + i), y, z + .3 * Math.cos(t * .4 + i)), Q.identity(), S3.setScalar(.6 + hash(i * 6) * .8)); VAULT.motes.setMatrixAt(i, M4);
  }
  VAULT.motes.instanceMatrix.needsUpdate = true;
  if (lk.set === "vault") {
    PL[2].position.set(-14.4, 1.4, -13); PL[2].color.set(0xFFC680); PL[2].intensity = 2.0; PL[2].distance = 7;
    PL[3].position.set(-21, 3.5, -13); PL[3].color.set(0xFFC680); PL[3].intensity = 2.5; PL[3].distance = 10;
  }
  // chests: each one's rim light and timeline
  const [R1, R2, E1, E2, G, M, S1, S2, S3_] = CHESTS;
  updChest(R1, t, K.shakeR1, K.openR1);
  updChest(R2, t, K.shakeR2, K.openR2);
  updChest(E1, t, K.shakeE, K.openE1);
  updChest(E2, t, K.shakeE, K.openE2);
  updChest(G, t, K.shakeG, K.openG, { beamHold: 1 - .85 * ss(t, K.cJ1 - .1, K.cJ1 + .3) });
  if (t > K.cJ1 - .1) G.glowIn.material.opacity *= 1 - .8 * ss(t, K.cJ1 - .1, K.cJ1 + .3);
  const lev = .45 * ss(t, K.lev, K.lev + 1.2) * (1 - ss(t, K.myth + .1, K.myth + .5)) + .03 * Math.sin(t * 3);
  updChest(M, t, K.lev, K.myth, { lev, shakeAmp: .6 + 1.4 * ss(t, K.lev + .5, K.myth) });
  for (const [k, s] of [[0, S1], [1, S2], [2, S3_]]) {
    updChest(s, t, null, null);
    const rat = t > K.rattle + k * .12 && t < K.rattle + k * .12 + .7 ? 1 : 0;
    s.inner.rotation.z = .05 * rat * Math.sin(t * 50); s.pad.rotation.z = .4 * rat * Math.sin(t * 30) + .05 * Math.sin(t * 2 + k);
    s.holo.position.y = 1.15 + .05 * Math.sin(t * 2.2 + k); s.holo.lookAt(camera.position); s.holo.material.opacity = .9 * ss(t, K.cM - .3, K.cM + .3);
  }
  // per-chest lights while each is on camera
  const chestLight = (o, a, b, i0, boost = 1) => {
    if (t < a - .4 || t > b) return;
    const k = Math.max(0, t - (o === M ? K.myth : o === G ? K.openG : o === E2 ? K.openE2 : o === E1 ? K.openE1 : o === R2 ? K.openR2 : K.openR1));
    const L = PL[i0]; o.g.getWorldPosition(V); L.position.copy(V).add(V2.set(0, 1.2, 0)); L.color.set(RAR[o.rar]);
    L.intensity = (2.2 + (k > 0 ? 6 * Math.exp(-k * 2.5) + 2.5 : 0)) * boost; L.distance = 5;
  };
  chestLight(R1, K.cF, K.cG, 4); chestLight(R2, K.cG, K.cH1, 4); chestLight(E1, K.cH1, K.cI1, 4); chestLight(E2, K.cH1, K.cI1, 5);
  chestLight(G, K.cI1 - .2, K.cJ1, 4, 1.3); chestLight(M, K.cJ1, K.cM, 4, 1.5);
  if (t > K.cJ1 && t < K.cM) { PL[2].intensity = 0; PL[3].intensity = .2; }
  if (t > K.cM) { PL[5].position.set(-22.2, 2.2, -18.2); PL[5].color.set(RAR.secret); PL[5].intensity = 4; PL[5].distance = 6; PL[6].position.set(-22.2, 2.4, -15.2); PL[6].color.set(0xFFD08A); PL[6].intensity = 3; PL[6].distance = 6; }
  VAULT.ringM.opacity = .8 * ss(t, K.cJ1, K.lev) * (1 - .5 * ss(t, K.myth + .5, K.myth + 1.5)) * (.75 + .25 * Math.sin(t * 8));
  // the mythic blast: flash, shockwave, shake
  flash = Math.max(flash, .9 * pulse(t, K.myth + .03, .12));
  if (pulse(t, K.myth + .03, .12) > .05) flashC.setRGB(1, .55, .55);
  SHAKE = Math.max(SHAKE, 1.2 * Math.exp(-Math.max(0, t - K.myth) * 2.2) * (t > K.myth ? 1 : 0), .35 * ss(t, K.lev + .5, K.myth) * (t < K.myth ? 1 : 0));
  // small shakes on each open
  for (const k of [K.openR1, K.openR2, K.openE1, K.openE2]) SHAKE = Math.max(SHAKE, .25 * Math.exp(-Math.max(0, t - k) * 6) * (t > k ? 1 : 0));
  SHAKE = Math.max(SHAKE, .5 * Math.exp(-Math.max(0, t - K.openG) * 4) * (t > K.openG ? 1 : 0));
  flash = Math.max(flash, .25 * pulse(t, K.openG + .05, .1));

  // ---- the bot
  const [bp, bf] = botAt(t, sh);
  applyPose(bp); setFace(bf);
  BOT.ant.material.color.set(CYAN).multiplyScalar(.7 + .3 * Math.sin(t * 5));
  BOT.root.visible = true;
  // the key in its right hand at the end
  KEY.visible = t > K.cO;
  if (KEY.visible) { BOT.root.updateMatrixWorld(true); BOT.hand[0].getWorldPosition(KEY.position); KEY.position.y += .2; KEY.rotation.set(0, t * .8, .25 * Math.sin(t * 2)); }

  // ---- camera
  const hand = .004, shk = SHAKE;
  camera.position.copy(sh.p).add(V.set(Math.sin(t * .9) * hand + shk * .04 * Math.sin(t * 61), Math.sin(t * 1.3 + 1) * hand + shk * .04 * Math.sin(t * 53), 0));
  camera.fov = sh.fov;
  const cv = window.STORE_COVER;
  if (cv && cv.cam) { camera.position.set(...cv.cam); sh.l.set(...cv.look); camera.fov = cv.fov ?? camera.fov; }
  camera.updateProjectionMatrix();
  camera.up.set(0, 1, 0); camera.lookAt(sh.l);
  if (shk) camera.rotateZ(shk * .018 * Math.sin(t * 47));
  scene.updateMatrixWorld(true);
  for (const o of CHESTS) o.halo.lookAt(camera.position);
  cocPass.uniforms.uF.value = sh.f ?? sh.p.distanceTo(sh.l); cocPass.uniforms.uAp.value = sh.ap;
  if (cv) { cocPass.uniforms.uAp.value = cv.ap ?? sh.ap; if (cv.focus) cocPass.uniforms.uF.value = cv.focus; }
  const gu = grade.uniforms;
  gu.uTime.value = t; gu.uWarm.value = lk.warm; gu.uCool.value = lk.cool; gu.uSat.value = lk.sat; gu.uVig.value = lk.vig;
  gu.uFlash.value = flash; gu.uCA.value = .0012 + shk * .005;
  gu.uTop.value = cv ? 0 : ss(t, K.endc - .2, K.endc + .4) * .9;
  gu.uDark.value = 0;
  bloom.strength = lk.bloom;
  // the key light follows the set
  const tgt = lk.set === "mall" ? V.set(0, 0, -2) : lk.set === "door" ? V.set(-9.5, 0, -13.2) : V.set(sh.l.x, 0, sh.l.z);
  sun.target.position.copy(tgt); sun.position.copy(tgt).add(S3.set(...lk.sd).normalize().multiplyScalar(25));
  Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 1, far: 60 });
  sun.shadow.camera.updateProjectionMatrix();
  renderer.setRenderTarget(sceneRT);
  renderer.render(scene, camera);
  renderer.setRenderTarget(null);
  composer.render();
}

const ready = (async () => {
  try { const jb = new FontFace("JBMono", "url(assets/fonts/jbmono-bold.ttf)", { weight: "700" }); document.fonts.add(await jb.load()); } catch (e) { /* fall back */ }
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 40px Manrope")]); } catch (e) { /* fall back */ }
  await buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh) o.frustumCulled = false; if (o.isMesh && o.parent && o.parent !== scene) o.frustumCulled = false; });
  for (const k in SET) SET[k].visible = true;
  renderer.compile(scene, camera);
  renderAt(window.STORE_COVER ? window.STORE_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["store"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.STORE_COVER ? window.STORE_COVER.t : e.detail.time));
window.STORE_DEBUG = { renderAt, SET, camera, C, BOT, CHESTS };
