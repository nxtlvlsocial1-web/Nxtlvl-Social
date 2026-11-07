// AI Posts reel: the 3D world, in the soft low-poly, flat-shaded style of the AI Exam reel. YOU (a chibi creator in a
// teal hoodie) and LUMI (our own AI ring light: a ring light on a little tripod with a screen face and stick arms) at a
// creator's desk by a city window, at dusk, at night and the next morning. Everything is a pure function of time t,
// drawn on HyperFrames' hf-seek; cue times come from the dialogue (window.CT, written by build/generate.py).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const C = window.CT;
const L = C.l, E = C.e, DUR = C.end, CU = C.cuts, FOC = C.focus;
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
const v3 = (a) => new THREE.Vector3(...a);
const tmpC = new THREE.Color(), BLACK = new THREE.Color(0), WHITE = new THREE.Color(0xffffff);
const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), V2 = new THREE.Vector3(), S = new THREE.Vector3();
const INK = 0x1E1B18, CORAL = 0xE8735A, CREAM = 0xFFFDF8, GOLD = 0xF2B33D, CYAN = 0x7FE6FF;
const sceneOf = (t) => { let s = 0; while (s < CU.length && t >= CU[s]) s++; return s; };
const shc = (c, f) => { tmpC.set(c); tmpC.lerp(f < 0 ? BLACK : WHITE, Math.abs(f)); return "#" + tmpC.getHexString(); };

// ---------------------------------------------------------------- renderer, scene, post (DOF -> bloom -> output -> grade)
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NeutralToneMapping ?? THREE.ACESFilmicToneMapping;
renderer.localClippingEnabled = true;
const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
const ENV = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.fog = new THREE.Fog(0xD6E9F6, 80, 300);
const NEAR = .05, FAR = 700;
const camera = new THREE.PerspectiveCamera(40, W / H, NEAR, FAR);
const sceneRT = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
sceneRT.depthTexture = new THREE.DepthTexture(W, H);
sceneRT.depthTexture.type = THREE.UnsignedIntType;
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType }));
composer.setPixelRatio(1);
composer.setSize(W, H);
const VS = "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }";
// signed circle of confusion into alpha (negative in front of focus); monotonic in depth, so it orders samples too
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
  uniforms: { tDiffuse: { value: null }, uMaxR: { value: 16 }, uRes: { value: new THREE.Vector2(W, H) } },
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
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .32, .5, .86);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uSat: { value: 1 }, uVig: { value: .26 }, uFlash: { value: 0 }, uCool: { value: 0 }, uWarm: { value: 0 },
    uCA: { value: 0 }, uBars: { value: 0 }, uScan: { value: 0 }, uCon: { value: 0 } },
  vertexShader: VS,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uSat, uVig, uFlash, uCool, uWarm, uCA, uBars, uScan, uCon; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 d = vec2(.5) - vUv;
      vec3 c = vec3(texture2D(tDiffuse, vUv + d * uCA).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - d * uCA).b);
      float g = dot(c, vec3(.299, .587, .114));
      c = mix(vec3(g), c, uSat);
      c = mix(c, c * vec3(.88, .97, 1.12), uCool);
      c = mix(c, c * vec3(1.08, 1.0, .9), uWarm);
      c = (c - .5) * (1. + uCon) + .5;
      vec2 q = vUv - .5; float r = dot(q, q);
      c *= 1. - r * uVig * 2.2;
      vec2 px = vUv * vec2(1080., 1920.);
      float grid = max(step(.96, fract(px.x / 54.)), step(.96, fract(px.y / 54.)));
      float sweep = 1. - smoothstep(0., .012, abs(fract(-vUv.y - uTime * .45) - .5));
      c = mix(c, vec3(.45, .88, 1.), uScan * (.18 * grid + .45 * sweep));
      c += (h(floor(px) + fract(uTime * 7.13) * 97.) - .5) * .024;
      c = mix(c, vec3(1., .99, .96), uFlash);
      float bh = uBars * 150. / 1920.;
      if (vUv.y < bh || vUv.y > 1. - bh) c = vec3(.075, .065, .06);
      gl_FragColor = vec4(c, 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0xC9B8FF, 0x3A2E4A, .8);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xFFC9A0, 1.6);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -.0004;
sun.shadow.normalBias = .02;
scene.add(sun, sun.target);
const plight = (c, d = 4, decay = 1.6) => { const l = new THREE.PointLight(c, 0, d, decay); scene.add(l); return l; };
const lampL = plight(0xFFC98A, 3.2), screenL = plight(0xD8E4FF, 1.8), faceKey = plight(0xFFE2C8, 3, 1.4), rimL = plight(0xB9A6FF, 4), owlL = plight(0x7FFFD4, 1.2);
const busL1 = plight(0xFFE6C0, 3), busL2 = plight(0xFFE6C0, 3), hallL = plight(0xFFF4E0, 8);

// ---------------------------------------------------------------- materials: soft low-poly, flat shaded
const fm = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .78, metalness: 0, flatShading: true, ...o });
const glow = (c, o = {}) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false, ...o });
const ROOT3 = new THREE.Group(); scene.add(ROOT3);
const add = (m, cast = true, recv = true, parent = ROOT3) => { m.castShadow = cast; m.receiveShadow = recv; parent.add(m); return m; };
const mesh = (geo, m, x, y, z, parent = ROOT3, cast = true) => { const o = add(new THREE.Mesh(geo, m.isMaterial ? m : fm(m)), cast, true, parent); o.position.set(x, y, z); return o; };
const box = (w, h, d, c, x, y, z, parent, cast) => mesh(new THREE.BoxGeometry(w, h, d), c, x, y, z, parent, cast);
const rbox = (w, h, d, r, c, x, y, z, parent, cast) => mesh(new RoundedBoxGeometry(w, h, d, 1, r), c, x, y, z, parent, cast);
const cyl = (r1, r2, h, c, x, y, z, seg = 8, parent, cast) => mesh(new THREE.CylinderGeometry(r1, r2, h, seg), c, x, y, z, parent, cast);
const ico = (r, d, c, x, y, z, parent, cast) => mesh(new THREE.IcosahedronGeometry(r, d), c, x, y, z, parent, cast);
function pix(w, h, draw, nearest = false) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  if (nearest) t.magFilter = THREE.NearestFilter;
  return t;
}
const rr = (g, x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
const TEX = {};
const LATE = [];
const texMat = (key, o = {}) => { const m = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false, ...o }); LATE.push([m, key]); return m; };
const setMap = (m, tx) => { if (m.map !== tx) { m.map = tx || null; m.needsUpdate = true; } };
const FONT = (w, s) => `${w} ${s}px Manrope, sans-serif`, MONO = (s) => `700 ${s}px JBMono, monospace`;

// ---------------------------------------------------------------- the set: a creator's desk by the city window
const wallM = fm(0x4A3F5E), woodM = fm(0x8A5A3C), woodD = fm(0x6E452E), creamM = fm(0xF4EDE2);
box(8, .05, 6, fm(0x5A3E30), 0, -.025, -.5, ROOT3, false);                                   // floor
box(1.0, 3.2, .12, wallM, -2.3, 1.6, -1.65); box(1.0, 3.2, .12, wallM, 2.3, 1.6, -1.65);   // wall beside the window
box(5.6, .5, .12, wallM, 0, 2.95, -1.65); box(5.6, .42, .12, wallM, 0, .21, -1.65);         // above / below
for (const x of [-1.8, -.6, .6, 1.8]) box(.06, 2.3, .1, fm(0x2E2638), x, 1.57, -1.62);
box(3.7, .06, .1, fm(0x2E2638), 0, .45, -1.6); box(3.7, .06, .1, fm(0x2E2638), 0, 2.7, -1.6); box(3.7, .05, .08, fm(0x2E2638), 0, 1.6, -1.6);
box(3.8, .05, .3, fm(0x5E5070), 0, .44, -1.5);                                                // sill
// the city outside: a sky card and low-poly towers with lit windows
const skyM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, fog: false });
const sky = add(new THREE.Mesh(new THREE.PlaneGeometry(60, 30), skyM), false, false); sky.position.set(0, 8, -22);
const towers = [];
for (let k = 0; k < 26; k++) {
  const x = -9 + k * .75 + (Math.sin(k * 7.3) * .2), d = 4 + (k % 3) * 2.5 + Math.sin(k) * .5, h = 1.6 + Math.abs(Math.sin(k * 2.1)) * 3.2, w = .5 + Math.abs(Math.sin(k * 1.7)) * .4;
  const m = new THREE.MeshStandardMaterial({ color: 0x2A2340, roughness: .9, flatShading: true, emissive: 0xFFC27A, emissiveIntensity: 0 });
  LATE.push([m, "towerWin", "emissiveMap"]);
  towers.push(box(w, h, .4, m, x, h / 2 - .3, -1.65 - d, ROOT3, false));
}
box(1.7, .05, .72, woodM, 0, .6, 0); for (const sx of [-.8, .8]) for (const sz of [-.3, .3]) box(.05, .58, .05, woodD, sx, .29, sz);
box(1.6, .2, .04, woodD, 0, .47, .33);
const seat = rbox(.42, .06, .4, .02, 0x3A3550, 0, .3, -.58); rbox(.42, .5, .06, .03, 0x3A3550, 0, .58, -.8); cyl(.025, .025, .28, 0x222222, 0, .14, -.58, 6);
const lap = new THREE.Group(); lap.position.set(-.42, .625, -.1); lap.rotation.y = .6; ROOT3.add(lap);
rbox(.46, .02, .32, .01, 0xB8BCC6, 0, .01, 0, lap); box(.4, .004, .2, 0x2A2A33, 0, .021, -.02, lap);
const lid = new THREE.Group(); lid.position.set(0, .02, .16); lid.rotation.x = .22; lap.add(lid);
rbox(.46, .3, .015, .01, 0xB8BCC6, 0, .15, 0, lid);
const lapScrM = texMat("lapNotes", { transparent: false }); const lapScr = mesh(new THREE.PlaneGeometry(.42, .27), lapScrM, 0, .15, -.009, lid, false); lapScr.rotation.y = Math.PI;
box(.06, .06, .004, glow(0xEDE7FB), 0, .15, .009, lid, false);
cyl(.045, .04, .1, 0xEDE7FB, .25, .675, .2, 10); cyl(.035, .035, .005, 0x6B4A32, .25, .726, .2, 10);
cyl(.04, .035, .12, 0x6B5BD6, -.38, .685, -.22, 8); for (let k = 0; k < 4; k++) { const p = cyl(.007, .007, .16, [0xF2B33D, 0xE8735A, 0x3FA372, 0x6B5BD6][k], -.38 + (k - 1.5) * .012, .76, -.22 + (k % 2 - .5) * .015, 6); p.rotation.z = (k - 1.5) * .12; }
cyl(.06, .05, .08, 0xC9644E, .75, .665, -.25, 8); for (let k = 0; k < 6; k++) { const l = ico(.06, 0, 0x5E9A4C, .75 + Math.cos(k) * .05, .75 + (k % 3) * .04, -.25 + Math.sin(k) * .05); l.scale.set(.6, 1.2, .6); l.rotation.z = Math.cos(k * 2) * .6; }
for (const [x, y, c] of [[-1.15, 1.3, 0xF2E36B], [-1.0, 1.15, 0xF29BB8], [1.1, 1.25, 0x9FEFD4]]) { const s = box(.14, .14, .01, c, x, y, -1.58); s.rotation.z = (x > 0 ? .1 : -.08); }
// a purple LED strip along the window top and a little shelf with a cactus and a mini tripod
const ledM = glow(0x9C7BFF); box(3.7, .025, .03, ledM, 0, 2.74, -1.56, ROOT3, false);
const paperTex = pix(64, 64, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#E9E2D6"; for (let y = 2; y < h; y += 3) g.fillRect(0, y, w, 1); });
// the coffee mug's steam (the coffee rant)
const steam = []; for (let k = 0; k < 3; k++) { const m = add(new THREE.Mesh(new THREE.IcosahedronGeometry(.02, 0), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .35, depthWrite: false })), false, false); steam.push(m); }
const MUG = new THREE.Vector3(.25, .735, .2);

// ---------------------------------------------------------------- characters: soft low-poly chibi people
const HIP = .4;
const sitY = (seat) => seat + .07 - HIP;
const ZAX = new THREE.Vector3(0, 0, 1);
const onSphere = (m, dir, R, out = 0) => { const d = V.set(...dir).normalize(); m.position.copy(d).multiplyScalar(R + out); m.quaternion.setFromUnitVectors(ZAX, d); return m; };
function makeKid(sp) {
  const root = new THREE.Group(); ROOT3.add(root);
  const hips = new THREE.Group(); hips.position.y = HIP; root.add(hips);
  const parts = [];
  const P = (geo, m, parent, x, y, z, cast = true) => { const o = new THREE.Mesh(geo, m.isMaterial ? m : fm(m)); o.position.set(x, y, z); o.castShadow = cast; o.receiveShadow = true; parent.add(o); parts.push(o); return o; };
  const top = fm(sp.top), pants = fm(sp.pants), skin = fm(sp.skin), hair = fm(sp.hair), shoe = fm(sp.shoe), ink = fm(0x1E1B18, { roughness: .4 });
  P(new THREE.IcosahedronGeometry(.16, 1), pants, hips, 0, -.01, 0).scale.set(1.15, .55, .95);
  const torso = new THREE.Group(); hips.add(torso);
  P(new THREE.CylinderGeometry(.15, .2, .4, 7), top, torso, 0, .2, 0);
  P(new THREE.BoxGeometry(.08, .34, .02), fm(sp.inner), torso, 0, .2, .175).rotation.x = -.11;
  P(new THREE.TorusGeometry(.12, .045, 5, 8), top, torso, 0, .39, 0).rotation.x = Math.PI / 2;
  const neck = new THREE.Group(); neck.position.y = .4; torso.add(neck);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; neck.add(head);
  const R = .28;
  const face = new THREE.Group(); face.position.y = .25; head.add(face);
  P(new THREE.IcosahedronGeometry(R, 3), skin, face, 0, 0, 0);
  const eyes = [], hl = [], arcs = [];
  for (const s of [-1, 1]) {
    const e = P(new THREE.SphereGeometry(.036, 10, 8), fm(0x1A1520, { roughness: .25 }), face, 0, 0, 0, false); onSphere(e, [s * .34, -.02, .94], R, -.005); e.scale.set(1, 1.2, .45); eyes.push(e);
    const h = P(new THREE.SphereGeometry(.011, 6, 4), new THREE.MeshBasicMaterial({ color: 0xffffff }), face, 0, 0, 0, false); onSphere(h, [s * .34 + .045, .05, .94], R, .02); hl.push(h);
    const arc = P(new THREE.TorusGeometry(.03, .008, 5, 12, Math.PI), fm(0x1A1520, { roughness: .3 }), face, 0, 0, 0, false); onSphere(arc, [s * .34, -.04, .94], R, .004); arcs.push(arc);
    const bl = P(new THREE.CircleGeometry(.05, 10), new THREE.MeshBasicMaterial({ color: 0xF29B9B, transparent: true, opacity: .55, depthWrite: false }), face, 0, 0, 0, false); onSphere(bl, [s * .62, -.3, .73], R, .004); bl.scale.set(1.2, .75, 1);
    if (sp.glasses) {
      const rim = P(new THREE.TorusGeometry(.083, .01, 6, 22), ink, face, 0, 0, 0, false); onSphere(rim, [s * .34, -.02, .94], R, .035);
      const tmp = P(new THREE.BoxGeometry(.012, .012, .2), ink, face, s * .245, -.006, .06, false); tmp.rotation.y = s * .35;
    }
    const brow = P(new THREE.CapsuleGeometry(.009, .05, 2, 6), fm(sp.hair), face, 0, 0, 0, false); onSphere(brow, [s * .34, .38, .86], R, .01); brow.rotateZ(Math.PI / 2);
  }
  if (sp.glasses) { const br = P(new THREE.CylinderGeometry(.008, .008, .04, 6), ink, face, 0, -.006, R + .02, false); br.rotation.z = Math.PI / 2; }
  onSphere(P(new THREE.SphereGeometry(.014, 6, 4), fm(sp.skinD), face, 0, 0, 0, false), [0, -.2, .98], R, 0);
  // mouths: one visible at a time
  const mouth = new THREE.Group(); face.add(mouth); onSphere(mouth, [0, -.42, .9], R, -.002);
  const dark = fm(0x5A2A2A, { roughness: .5 }), red = fm(0xD9605A);
  const M = {};
  M.smile = P(new THREE.TorusGeometry(.035, .008, 5, 12, Math.PI), dark, mouth, 0, .015, 0, false); M.smile.rotation.z = Math.PI;
  M.grin = new THREE.Group(); mouth.add(M.grin); P(new THREE.CircleGeometry(.045, 14, Math.PI, Math.PI), dark, M.grin, 0, .012, 0, false); P(new THREE.CircleGeometry(.028, 10, Math.PI, Math.PI), red, M.grin, 0, -.006, .001, false);
  M.o = P(new THREE.SphereGeometry(.022, 10, 8), dark, mouth, 0, 0, 0, false); M.o.scale.set(.9, 1.15, .3);
  M.wide = P(new THREE.SphereGeometry(.03, 10, 8), dark, mouth, 0, -.004, 0, false); M.wide.scale.set(1, 1.3, .3);
  M.flat = P(new THREE.CapsuleGeometry(.006, .04, 2, 6), dark, mouth, 0, 0, 0, false); M.flat.rotation.z = Math.PI / 2;
  M.sad = P(new THREE.TorusGeometry(.03, .008, 5, 12, Math.PI), dark, mouth, 0, -.012, 0, false);
  M.smirk = P(new THREE.TorusGeometry(.03, .008, 5, 12, Math.PI * .6), dark, mouth, .01, .012, 0, false); M.smirk.rotation.z = Math.PI * 1.1;
  // hair: a cap over the top and back, side locks, bangs, long hair down the back
  const cap = P(new THREE.SphereGeometry(R + .03, 12, 8, 0, Math.PI * 2, 0, 1.28), hair, face, 0, 0, 0); cap.rotation.x = -.22;
  if (sp.short) P(new THREE.IcosahedronGeometry(.3, 1), hair, face, 0, -.02, -.1).scale.set(1.0, .82, .76); else P(new THREE.IcosahedronGeometry(.3, 1), hair, face, 0, -.1, -.1).scale.set(1.04, 1.12, .78);
  for (const s of [-1, 1]) { const lock = P(new THREE.IcosahedronGeometry(.12, 1), hair, face, s * .255, sp.short ? -.02 : -.12, .02); if (sp.short) lock.scale.set(.38, .75, .7); else lock.scale.set(.45, 1.35, .75); }
  for (const [x, rz] of [[-.12, .35], [.0, 0], [.13, -.35]]) { const b = P(new THREE.IcosahedronGeometry(.1, 1), hair, face, x, .19, .2); b.scale.set(1.05, .5, .55); b.rotation.z = rz; }
  if (sp.long) { const back = P(new THREE.IcosahedronGeometry(.22, 1), hair, face, 0, -.32, -.13); back.scale.set(1.25, 1.35, .55); }
  if (sp.bun) P(new THREE.IcosahedronGeometry(.1, 1), hair, face, 0, .3, -.12);
  // arms and legs
  const sh = [], el = [], hand = [], hip = [], knee = [];
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    const a = new THREE.Group(); a.position.set(s * .185, .34, 0); torso.add(a); sh.push(a);
    P(new THREE.CylinderGeometry(.062, .056, .2, 6), top, a, 0, -.09, 0);
    const e = new THREE.Group(); e.position.y = -.19; a.add(e); el.push(e);
    P(new THREE.CylinderGeometry(.056, .05, .17, 6), top, e, 0, -.08, 0);
    hand.push(P(new THREE.IcosahedronGeometry(.048, 1), skin, e, 0, -.2, 0));
    const h = new THREE.Group(); h.position.set(s * .085, 0, 0); hips.add(h); hip.push(h);
    P(new THREE.CylinderGeometry(.068, .062, .2, 6), pants, h, 0, -.1, 0);
    const kn = new THREE.Group(); kn.position.y = -.2; h.add(kn); knee.push(kn);
    P(new THREE.CylinderGeometry(.058, .052, .16, 6), pants, kn, 0, -.08, 0);
    P(new THREE.IcosahedronGeometry(.07, 1), shoe, kn, 0, -.175, .035).scale.set(.95, .6, 1.4);
  }
  return { sp, root, hips, torso, head, face, sh, el, hand, hip, knee, eyes, hl, arcs, M, parts, seed: sp.seed || 1 };
}
const pose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, lean: 0, tw: 0, hy: 0, hp: 0, hr: 0, a: [[.08, .12, .2], [.08, .12, .2]], l: [[0, 0], [0, 0]], ...o });
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
let NOW = 0;
const blinkAt = (seed, t) => { const p = 2.9 + hash(seed) * 1.6, u = (t + hash(seed * 3) * 7) % p; return u < .12 ? Math.sin(Math.PI * u / .12) : 0; };
function setFace(P, f) {
  let mouth = f.mouth || "smile";
  if (f.talk) { const k = Math.floor(NOW * 9 + P.seed) % 3; const low = f.mouth === "sad" || f.mouth === "flat"; mouth = k === 0 ? "o" : k === 1 ? (f.mouth === "wide" ? "wide" : low ? f.mouth : "grin") : (f.mouth || "smile"); }
  for (const k in P.M) P.M[k].visible = k === mouth;
  const happy = f.eyes === "happy";
  P.arcs.forEach((a) => (a.visible = happy));
  const close = happy ? 1 : Math.max(f.eyes === "closed" ? 1 : f.eyes === "half" ? .5 : 0, blinkAt(P.seed, NOW));
  const wide = f.eyes === "wide" ? 1.25 : 1;
  P.eyes.forEach((e) => { e.visible = !happy; e.scale.set(wide, 1.2 * wide * (1 - close * .9) + .001, .45); });
  P.hl.forEach((h) => (h.visible = close < .5));
}
const SP = {
  you: { top: 0x2FA59A, inner: 0xFFFDF8, pants: 0x2E2A3A, skin: 0xE8B48E, skinD: 0xD39B74, hair: 0x2A1E1A, shoe: 0xFFFDF8, short: true, seed: 3 },
};
const YOU = makeKid(SP.you);
// a hood on his back (a hoodie)
{ const hood = new THREE.Mesh(new THREE.TorusGeometry(.15, .06, 6, 10), fm(0x268C83)); hood.position.set(0, .36, -.08); hood.rotation.x = Math.PI / 2 + .5; hood.castShadow = true; YOU.torso.add(hood); }

// ---------------------------------------------------------------- LUMI: our AI ring light (a ring light with a screen face)
function makeLumi() {
  const root = new THREE.Group(); ROOT3.add(root);
  const parts = [];
  const P = (geo, m, parent, x, y, z, cast = true) => { const o = new THREE.Mesh(geo, m.isMaterial ? m : fm(m)); o.position.set(x, y, z); o.castShadow = cast; o.receiveShadow = true; parent.add(o); parts.push(o); return o; };
  const dark = fm(0x2E2A38, { roughness: .5 }), steel = fm(0x8A86A0, { roughness: .4, metalness: .2 });
  for (let k = 0; k < 3; k++) { const a = k * Math.PI * 2 / 3 + .3; const leg = P(new THREE.CylinderGeometry(.008, .008, .13, 5), dark, root, Math.cos(a) * .045, .05, Math.sin(a) * .045); leg.rotation.set(Math.sin(a) * .7, 0, -Math.cos(a) * .7); }
  P(new THREE.CylinderGeometry(.012, .012, .28, 6), steel, root, 0, .22, 0);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; head.position.y = .44; root.add(head);
  const ringM = glow(0xFFF2DC);
  P(new THREE.TorusGeometry(.15, .03, 8, 28), ringM, head, 0, 0, .01, false);
  P(new THREE.TorusGeometry(.155, .038, 6, 28), dark, head, 0, 0, -.012);
  P(new THREE.CylinderGeometry(.122, .122, .02, 24), dark, head, 0, 0, -.01).rotation.x = Math.PI / 2;
  const scr = P(new THREE.CircleGeometry(.118, 24), fm(0x17142A, { roughness: .25 }), head, 0, 0, .002, false);
  P(new THREE.BoxGeometry(.03, .03, .03), dark, head, 0, -.17, -.005);
  const eyeM = glow(0x9FF5FF), FZ = .006;
  const EY = { open: [], happy: [], closed: [], wide: [], smug: [] };
  for (const s of [-1, 1]) {
    const x = s * .045, y = .018;
    EY.open.push(P(new THREE.CapsuleGeometry(.014, .03, 3, 8), eyeM, head, x, y, FZ, false));
    const w = P(new THREE.CapsuleGeometry(.019, .036, 3, 8), eyeM, head, x, y, FZ, false); EY.wide.push(w);
    const hp = P(new THREE.TorusGeometry(.022, .006, 5, 12, Math.PI), eyeM, head, x, y - .008, FZ, false); EY.happy.push(hp);
    const cl = P(new THREE.BoxGeometry(.044, .009, .002), eyeM, head, x, y - .004, FZ, false); EY.closed.push(cl);
    const sg = new THREE.Group(); sg.position.set(x, y, FZ); head.add(sg);
    P(new THREE.CapsuleGeometry(.014, .012, 3, 8), eyeM, sg, 0, -.01, 0, false); P(new THREE.BoxGeometry(.044, .008, .002), eyeM, sg, 0, .012, 0, false); sg.rotation.z = -s * .03; EY.smug.push(sg);
  }
  const MO = {};
  MO.smile = P(new THREE.TorusGeometry(.024, .005, 5, 12, Math.PI), eyeM, head, 0, -.035, FZ, false); MO.smile.rotation.z = Math.PI;
  MO.o = P(new THREE.TorusGeometry(.014, .005, 5, 12), eyeM, head, 0, -.04, FZ, false);
  MO.flat = P(new THREE.BoxGeometry(.034, .007, .002), eyeM, head, 0, -.04, FZ, false);
  MO.smirk = P(new THREE.TorusGeometry(.02, .005, 5, 12, Math.PI * .6), eyeM, head, .008, -.032, FZ, false); MO.smirk.rotation.z = Math.PI * 1.1;
  const arms = [];
  for (const s of [-1, 1]) { const a = new THREE.Group(); a.position.set(s * .016, .32, 0); root.add(a); P(new THREE.CylinderGeometry(.008, .007, .12, 5), steel, a, 0, -.06, 0); P(new THREE.IcosahedronGeometry(.02, 1), dark, a, 0, -.125, 0); arms.push(a); }
  return { root, head, ringM, scr, EY, MO, arms, parts };
}
const LUMI = makeLumi();
const lpose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, s: 1, hy: 0, hp: 0, hr: 0, a: [.35, .35], hop: 0, glow: 1, ...o });
function applyLumi(p) {
  LUMI.root.position.set(p.x, p.y + p.hop, p.z); LUMI.root.rotation.y = p.ry; LUMI.root.scale.setScalar(p.s);
  LUMI.head.rotation.set(p.hp, p.hy, p.hr);
  LUMI.arms[0].rotation.z = -p.a[0]; LUMI.arms[1].rotation.z = p.a[1];
  LUMI.ringM.color.set(0xFFF2DC).multiplyScalar(p.glow);
}
function setLumi(f) {
  let eyes = f.eyes || "open";
  if (eyes === "open" && blinkAt(4.4, NOW) > .5) eyes = "closed";
  for (const k in LUMI.EY) for (const m of LUMI.EY[k]) m.visible = k === eyes;
  let mouth = f.mouth || "smile";
  if (f.talk) mouth = Math.floor(NOW * 9) % 2 ? "o" : (mouth === "flat" ? "flat" : mouth);
  for (const k in LUMI.MO) LUMI.MO[k].visible = k === mouth;
}

// ---------------------------------------------------------------- props: phone, transcript strips, sticky notes, slides, calendar, hearts, confetti
const phoneK = new THREE.Group(); ROOT3.add(phoneK);
rbox(.075, .15, .012, .01, 0x1E1B18, 0, 0, 0, phoneK); const phoneScrM = texMat("phoneMemo", { transparent: false }); mesh(new THREE.PlaneGeometry(.066, .135), phoneScrM, 0, 0, .0065, phoneK, false);
const PAGE_N = 40;
const pageM = new THREE.InstancedMesh(new THREE.PlaneGeometry(.13, .022), glow(0xEDE7FB, { side: THREE.DoubleSide }), PAGE_N); ROOT3.add(pageM);
const CARD_N = 30;
const cardM = new THREE.InstancedMesh(new RoundedBoxGeometry(.1, .1, .005, 1, .005), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6, emissive: 0x2a2a2a }), CARD_N); ROOT3.add(cardM);
const STICKY = [0xF7E36B, 0xFFB3C7, 0x9FEFD4, 0xCFC6F5];
for (let k = 0; k < CARD_N; k++) cardM.setColorAt(k, tmpC.set(STICKY[k % 4]));
const COFFEE_K = 13;
const SLIDE_N = 5, slides = [];
for (let k = 0; k < SLIDE_N; k++) { const m = mesh(new THREE.PlaneGeometry(.24, .3), texMat("slide" + k, { transparent: false, side: THREE.DoubleSide }), 0, 0, 0, ROOT3, false); slides.push(m); }
const TILE_N = 30;
const tileM = new THREE.InstancedMesh(new RoundedBoxGeometry(.085, .085, .01, 1, .008), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6, emissive: 0x2a2a2a }), TILE_N); ROOT3.add(tileM);
const TILE_ON = [0x6B5BD6, 0xE8735A, 0x3FA372, 0xF2B33D];
const heartShape = new THREE.Shape(); heartShape.moveTo(0, -.5); heartShape.bezierCurveTo(-.9, .1, -.5, .9, 0, .45); heartShape.bezierCurveTo(.5, .9, .9, .1, 0, -.5);
const HEART_N = 26;
const heartM = new THREE.InstancedMesh(new THREE.ShapeGeometry(heartShape, 6), glow(0xFF6B8A, { side: THREE.DoubleSide }), HEART_N); ROOT3.add(heartM);
const CONF_N = 90;
const confM = new THREE.InstancedMesh(new THREE.BoxGeometry(.025, .04, .004), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6, emissive: 0x333333 }), CONF_N); ROOT3.add(confM);
for (let k = 0; k < CONF_N; k++) confM.setColorAt(k, tmpC.set([0xE8735A, 0xF2B33D, 0x9FF5FF, 0x6B5BD6, 0xFFFDF8][k % 5]));
const BAR_N = 22;
const barM = new THREE.InstancedMesh(new THREE.BoxGeometry(.014, 1, .014), glow(0x9FF5FF), BAR_N); ROOT3.add(barM);
const ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
const hideAll = (m, n) => { for (let k = 0; k < n; k++) m.setMatrixAt(k, ZERO); };
const bez = (p0, p1, p2, u, out) => out.set((1 - u) ** 2 * p0.x + 2 * (1 - u) * u * p1.x + u * u * p2.x, (1 - u) ** 2 * p0.y + 2 * (1 - u) * u * p1.y + u * u * p2.y, (1 - u) ** 2 * p0.z + 2 * (1 - u) * u * p1.z + u * u * p2.z);

// ---------------------------------------------------------------- scenes, poses and faces
//   s0 lines 1-5 dusk: the panic   s1 line 6: voice memo   s2 lines 7-8 night: 30 ideas   s3 line 9: hook, caption, slides
//   s4 lines 10-11: schedule 30, a month in one night   s5 lines 12-13 morning: 80,000 views   s6 lines 14-16: "be me?" "No."
//   s7 line 17: your voice is the content   s8 line 18: the end card
const lineAt = (t) => { for (let i = 0; i < C.lines.length; i++) if (t >= C.lines[i].s - .05 && t <= C.lines[i].e + .05) return C.lines[i]; return null; };
const talking = (who, t) => { const ln = lineAt(t); return !!ln && ln.who === who; };
const SIT = (x, z, ry, seat = .33) => pose({ x, y: sitY(seat), z, ry, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.55, .1, .9], [.55, .1, .9]] });
const withArms = (p, a, o = {}) => ({ ...p, a, ...o });
const DESK_HANDS = [[.75, .05, .75], [.75, .05, .75]];
const CHEER = (t) => [[.3, 2.6 + .12 * Math.sin(t * 10), .25], [.3, 2.6 + .12 * Math.sin(t * 10 + 1.5), .25]];
const HOLD = [[.72, -.28, 1.2], [.72, -.28, 1.2]];
const PLEAD = [[1.05, -.38, 1.55], [1.05, -.38, 1.55]];
const SELFIE = [[.75, .05, .75], [2.05, .55, .35]];
const idle = (p, t, s) => ({ ...p, lean: p.lean + .015 * Math.sin(t * 1.4 + s), hr: p.hr + .03 * Math.sin(t * .9 + s * 2), hy: p.hy + .04 * Math.sin(t * .6 + s) });
const DESK = { x: 0, z: -.58 };
function youAt(t, s) {
  let p = idle(withArms(SIT(DESK.x, DESK.z, 0), DESK_HANDS), t, 1);
  let f = { mouth: "smile", eyes: "open" };
  let phone = null, talk = talking("you", t);
  if (s === 0) {
    if (t < C.l[1]) { p = { ...p, hp: -.05, hr: .06 * Math.sin(t * 7), lean: .05, a: [[1.0, -.2, 1.7], [1.0, -.2, 1.7]] }; f = { mouth: "wide", eyes: "wide" }; }
    else if (t < C.l[2]) { p = { ...p, hy: .5, hp: .05 }; f = { mouth: "flat", eyes: "half" }; }
    else if (t < C.l[3]) { const up = bump(t, C.l[2] - .1, C.e[2] + .2, .2); p = mixP(p, withArms(p, [[1.5, .45, .3], [1.5, .45, .3]], { lean: -.08, hp: -.12 }), up); f = { mouth: "wide", eyes: "wide" }; }
    else if (t < C.l[4]) { p = { ...p, hy: .45 }; f = { mouth: "flat", eyes: "open" }; }
    else { p = { ...p, hy: .3, hp: -.05, hr: .14 }; f = { mouth: "o", eyes: "open" }; }
  }
  if (s === 1) { p = withArms(p, HOLD, { hp: .22, hy: -.05 }); f = { mouth: "smile", eyes: "open" }; phone = "memo"; talk = false; }
  if (s === 2) {
    if (t < C.l[7]) { p = { ...p, hy: -.35, hp: .08 }; f = { mouth: "smile", eyes: "open" }; }
    else { p = mixP(p, withArms(p, [[1.1, .2, 1.9], [1.1, .2, 1.9]], { lean: -.08, hp: -.08 }), ss(t, C.l[7], C.l[7] + .3)); f = { mouth: "wide", eyes: "wide" }; }
  }
  if (s === 3) { p = withArms(p, [[.75, .05, .75], [1.25, -.1, 2.2]], { hp: -.18, hy: .1 }); f = { mouth: "smile", eyes: "open" }; }
  if (s === 4) {
    p = { ...p, hp: -.2, hy: .05 };
    if (t > C.l[10] - .2) { p = mixP(p, withArms(p, CHEER(t), { hp: -.15, lean: -.05, y: p.y + .02 * Math.abs(Math.sin(t * 8)) }), ss(t, C.l[10] - .2, C.l[10] + .15)); f = { mouth: "grin", eyes: "happy" }; }
  }
  if (s === 5) {
    p = withArms(p, HOLD, { hp: .28 }); phone = "stats";
    if (t > C.wait - .15) { p = { ...p, lean: -.12, hp: .05, hy: .05 * Math.sin(t * 8) * bump(t, C.wait, C.coffee12 + .4, .1) }; f = { mouth: "wide", eyes: "wide" }; }
    if (t > C.l[12] - .1) { p = { ...p, lean: -.04, hy: .35, hp: .1 }; f = { mouth: "grin", eyes: "happy" }; }
  }
  if (s === 6) {
    p = { ...p, hy: .3 };
    if (t < C.l[14]) { p = mixP(p, withArms(p, [[.9, -.35, 1.7], [.9, -.35, 1.7]], { hy: .3, lean: .06 }), ss(t, C.just - .3, C.just + .2)); f = { mouth: "smirk", eyes: "half" }; }
    else if (t < C.l[15]) { p = { ...p, hy: .32 }; f = { mouth: "o", eyes: "wide" }; }
    else { p = mixP(p, withArms(p, PLEAD, { hy: .25, hp: -.1, hr: .12 }), ss(t, C.why - .3, C.why)); f = { mouth: "sad", eyes: "wide" }; }
  }
  if (s === 7) { p = withArms(p, HOLD, { hy: .32, hp: .02, hr: -.05 }); f = { mouth: "grin", eyes: t > C.voice - .2 ? "happy" : "open" }; phone = "selfie"; }
  if (s === 8) { p = idle(withArms(SIT(DESK.x, DESK.z, 0), [[.95, .55, .55], [.3, 2.4 + .3 * Math.sin(t * 9), .5]]), t, 4); f = { mouth: "grin", eyes: t > C.postsk ? "happy" : "open" }; }
  return { vis: true, p, phone, f: { ...f, talk: talk && f.mouth !== "wide" } };
}
const LB = { x: .52, y: .625, z: .02, ry: -.5 };
function lumiAt(t, s) {
  const bob = .008 * Math.sin(t * 2.2);
  let p = lpose({ ...LB, hop: bob, hy: .06 * Math.sin(t * .7), glow: s >= 5 ? .95 : 1.05 });
  let f = { eyes: "open", mouth: "smile" };
  if (s === 0) {
    if (t > C.l[1] - .1 && t < C.l[2]) { p = { ...p, hr: .22, hp: .05 }; f = { eyes: "smug", mouth: "flat" }; }
    if (t > C.l[3] - .1) { p = { ...p, a: [1.4 + .1 * Math.sin(t * 6), 1.4 + .1 * Math.sin(t * 6 + 1)] }; f = { eyes: "happy", mouth: "smile" }; }
  }
  if (s === 1) { p = { ...p, a: [.35, 1.9], hy: .25 }; f = { eyes: "open" }; }
  if (s === 2) { p = { ...p, a: [2.2 + .2 * Math.sin(t * 5), 2.2 + .2 * Math.sin(t * 5 + 1)], hop: bob + .02 * Math.abs(Math.sin(t * 6)), glow: 1.15 }; f = { eyes: "happy" }; }
  if (s === 3) { p = { ...p, a: [.35, 1.6], hy: .3 }; f = { eyes: "open" }; }
  if (s === 4) { p = { ...p, a: [.6, 1.5] }; f = { eyes: t > C.l[10] ? "happy" : "open" }; if (t > C.l[10]) p.hop = .04 * Math.abs(Math.sin(t * 9)); }
  if (s === 5) { if (t > C.l[12] - .1) { p = { ...p, hr: .18, a: [2.6, 2.6] }; f = { eyes: "smug", mouth: "smirk" }; } }
  if (s === 6) {
    if (t < C.l[14]) { p = { ...p, hy: .3, hp: .1 }; f = { eyes: t > C.just ? "wide" : "open", mouth: "flat" }; }
    else if (t < C.l[15] + .1) { p = { ...p, hy: .5 * Math.sin((t - C.no) * 12) * bump(t, C.no - .05, C.no + .9, .1), a: [2.7, 2.7] }; f = { eyes: "closed", mouth: "flat" }; }
    else { p = { ...p, hy: .25, a: [2.7, 2.7] }; f = { eyes: "closed", mouth: "flat" }; }
  }
  if (s === 7) { p = { ...p, a: [.35, 1.2], glow: 1.15 + .1 * ss(t, C.voice - .3, C.voice + .3) }; f = { eyes: "happy", mouth: "smile" }; }
  if (s === 8) { p = { ...p, a: [.2, 2.2 + .4 * Math.sin(t * 9)], hop: bob + .02 * Math.abs(Math.sin(t * 5)) }; f = { eyes: t > C.postsk && t < C.postsk + 1.2 ? "closed" : "happy" }; }
  return { vis: true, p, f: { ...f, talk: talking("lumi", t) } };
}

// ---------------------------------------------------------------- camera shots
const SH = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40, ap: null };
const fixed = (p, l, fov = 40, ap = null) => () => { SH.p.set(...p); SH.l.set(...l); SH.fov = fov; SH.ap = ap; return SH; };
const move = (a, b, p0, p1, l0, l1, f0, f1, ap = null) => (t) => { const u = ss(t, a, b); SH.p.set(lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(p0[2], p1[2], u)); SH.l.set(lerp(l0[0], l1[0], u), lerp(l0[1], l1[1], u), lerp(l0[2], l1[2], u)); SH.fov = lerp(f0, f1, u); SH.ap = ap; return SH; };
const HEADW = { you: new THREE.Vector3(), lumi: new THREE.Vector3() }, HEADM = { you: new THREE.Matrix4(), lumi: new THREE.Matrix4() };
const FV = new THREE.Vector3(), UV = new THREE.Vector3(), RV = new THREE.Vector3();
const faceShot = (key, d, h, side, fov, lift = 0, push = 0, win = null) => (t) => {
  const M = HEADM[key];
  FV.set(0, 0, 1).transformDirection(M); UV.set(0, 1, 0).transformDirection(M); RV.set(1, 0, 0).transformDirection(M);
  FV.y *= .4; FV.normalize();
  const dd = d - (win ? push * ss(t, win[0], win[1]) : 0);
  SH.p.copy(HEADW[key]).addScaledVector(FV, dd).addScaledVector(UV, h).addScaledVector(RV, side);
  SH.l.copy(HEADW[key]).addScaledVector(UV, lift); SH.fov = fov; SH.ap = null; return SH;
};
const F = FOC;
const SHOTS = [
  { t: 0, f: faceShot("you", 3.1, .05, .25, 30, -.12, .4, [0, F[0].b]) },
  { t: F[1].a, f: faceShot("lumi", 2.5, .03, -.15, 30, .09) },
  { t: C.l[2] - .3, f: move(C.l[2] - .3, F[2].a, [-.25, 1.5, 3.4], [-.2, 1.45, 3.1], [.05, 1.25, -.2], [.05, 1.25, -.2], 38, 37) },
  { t: F[2].a, f: faceShot("lumi", 2.5, .03, .12, 30, .09) },
  { t: C.l[4] - .3, f: fixed([.3, 1.48, 3.1], [.18, 1.24, -.2], 38) },
  // step 1: the voice memo, the words fly into the laptop
  { t: CU[0], f: move(CU[0], CU[1], [-.95, 1.55, 2.7], [-.8, 1.5, 2.4], [-.1, 1.15, -.3], [-.1, 1.15, -.3], 38, 37) },
  // step 2: 30 sticky notes burst around him
  { t: CU[1], f: move(CU[1], F[3].a, [0, 1.6, 3.6], [0, 1.55, 3.3], [0, 1.35, -.45], [0, 1.35, -.45], 40, 39) },
  { t: F[3].a, f: faceShot("you", 3.2, .05, -.2, 30, .14) },
  // step 3: the carousel slides
  { t: CU[2], f: move(CU[2], CU[3], [.7, 1.55, 3.1], [.6, 1.52, 2.8], [0, 1.42, -.6], [0, 1.42, -.6], 40, 39) },
  // step 4: the month fills in, then the cheer
  { t: CU[3], f: move(CU[3], C.l[10] - .3, [0, 1.6, 3.9], [0, 1.56, 3.5], [0, 1.5, -.8], [0, 1.5, -.8], 42, 41) },
  { t: C.l[10] - .3, f: fixed([0, 1.45, 3.0], [0, 1.32, -.5], 38) },
  // the next morning
  { t: CU[4], f: faceShot("you", 3.2, .1, .2, 30, .14) },
  { t: C.l[12] - .15, f: faceShot("lumi", 2.5, .03, -.08, 30, .09) },
  // "just be me", "No.", "why not?"
  { t: CU[5], f: move(CU[5], F[5].a, [.3, 1.5, 3.2], [.28, 1.47, 2.9], [.22, 1.2, -.2], [.22, 1.2, -.2], 38, 36) },
  { t: F[5].a, f: faceShot("lumi", 2.4, .03, .06, 30, .09) },
  { t: C.why - .25, f: fixed([-.4, 1.3, 2.1], [-.04, 1.0, -.58], 30) },
  // your voice is the content
  { t: CU[6], f: move(CU[6], CU[7], [.25, 1.42, 2.7], [.2, 1.38, 2.3], [.12, 1.18, -.3], [.12, 1.18, -.3], 36, 35) },
  // close
  { t: CU[7], f: move(CU[7], DUR, [.1, 1.3, 3.8], [.1, 1.3, 3.5], [.18, 1.75, -.3], [.18, 1.75, -.3], 38, 38) },
];
const CAMP = new THREE.Vector3(), CAML = new THREE.Vector3();
let CAMAP = null;
function camAt(t) {
  let i = 0; while (i < SHOTS.length - 1 && t >= SHOTS[i + 1].t) i++;
  const r = SHOTS[i].f(t); CAMP.copy(r.p); CAML.copy(r.l); CAMAP = r.ap; return r.fov;
}
const SHOT_STARTS = SHOTS.map((s) => s.t);

// ---------------------------------------------------------------- looks
const SKY = {};
const LOOKS = {
  dusk: { sky: "dusk", fog: 0x3A2E4A, hs: 0xC9B4FF, hg: 0x3A2E4A, hi: .8, sun: 0xFFA868, si: 1.3, sp: [1.5, 3, -6], ring: .7, scr: .5, win: .9, bg: 0x2B2440 },
  night: { sky: "night", fog: 0x15132A, hs: 0x7D79C9, hg: 0x1E1A2E, hi: .45, sun: 0x9FB4FF, si: .35, sp: [2, 4, -6], ring: 1.3, scr: 1.0, win: 1.3, bg: 0x15132A },
  morning: { sky: "morning", fog: 0xE9DCF0, hs: 0xFFF1E6, hg: 0x8A6A58, hi: 1.0, sun: 0xFFD9A8, si: 1.8, sp: [1.5, 3, -6], ring: .35, scr: .2, win: 0, bg: 0xE9DCF0 },
};
const LOOK_OF = ["dusk", "dusk", "night", "night", "night", "morning", "morning", "morning", "morning"];

// ---------------------------------------------------------------- render at time t
const PP = new THREE.Vector3(), A0 = new THREE.Vector3(), A1 = new THREE.Vector3(), A2 = new THREE.Vector3();
const SCREEN = new THREE.Vector3();
function handsMid(P, out) { P.hand[0].getWorldPosition(A0); P.hand[1].getWorldPosition(A1); return out.lerpVectors(A0, A1, .5); }
function renderAt(t) {
  NOW = t;
  const s = sceneOf(t), Lk = LOOKS[LOOK_OF[s]];
  scene.background = tmpC.set(Lk.bg).clone(); scene.fog.color.set(Lk.fog);
  if (SKY[Lk.sky]) setMap(skyM, SKY[Lk.sky]);
  hemi.color.set(Lk.hs); hemi.groundColor.set(Lk.hg); hemi.intensity = Lk.hi;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  for (const tw of towers) tw.material.emissiveIntensity = Lk.win;
  ledM.color.set(0x9C7BFF).multiplyScalar(Lk === LOOKS.morning ? .5 : 1);
  screenL.position.copy(SCREEN).add(V.set(0, .05, -.25)); screenL.intensity = Lk.scr + (s === 2 || s === 3 ? .7 : 0);
  rimL.position.set(.6, 1.6, -1.2); rimL.intensity = Lk === LOOKS.morning ? .6 : 1.0;
  lapScr.getWorldPosition(SCREEN);
  if (TEX.lapIdle) setMap(lapScrM, TEX[s === 2 ? "lapChat" : s === 3 ? "lapSlides" : s >= 4 ? "lapPlanner" : "lapIdle"]);

  // characters
  const ys = youAt(t, s); YOU.root.visible = ys.vis; if (ys.vis) { applyPose(YOU, ys.p); setFace(YOU, ys.f); }
  const ls = lumiAt(t, s); applyLumi(ls.p); setLumi(ls.f);
  scene.updateMatrixWorld(true);
  YOU.face.updateMatrixWorld(); HEADM.you.copy(YOU.face.matrixWorld); HEADW.you.setFromMatrixPosition(YOU.face.matrixWorld);
  HEADM.lumi.copy(LUMI.head.matrixWorld); HEADW.lumi.setFromMatrixPosition(LUMI.head.matrixWorld);
  // LUMI is the room's key light: from its ring toward his face
  lampL.position.copy(HEADW.lumi).lerp(HEADW.you, .25); lampL.intensity = Lk.ring * (s === 7 ? 1 + .6 * ss(t, C.voice - .3, C.voice + .3) : 1);
  owlL.intensity = 0;

  // the coffee steam
  steam.forEach((m, k) => { const u = ((t * .35 + k / 3) % 1); m.position.set(MUG.x + Math.sin(t * 2 + k * 2) * .015, MUG.y + u * .14, MUG.z); m.scale.setScalar(.6 + u); m.material.opacity = .35 * Math.sin(u * Math.PI) * (s === 2 && t > C.coffee - .2 && t < C.e[7] + .2 ? 1.8 : 1); });

  // the phone in his hands
  phoneK.visible = !!ys.phone;
  if (phoneK.visible) {
    if (TEX.phoneMemo) setMap(phoneScrM, TEX[ys.phone === "memo" ? "phoneMemo" : ys.phone === "stats" ? "phoneStats" : "phoneSelfie"]);
    { handsMid(YOU, PP); phoneK.position.copy(PP).add(V.set(0, .05, .03)); phoneK.rotation.set(-.75, 0, 0); }
  }
  // step 1: a waveform by the phone, then his words fly into the laptop as lines of text
  hideAll(barM, BAR_N);
  if (s === 1 && t > C.record - .3) {
    const grow = ss(t, C.record - .3, C.record + .1);
    A0.set(-.52, .97, -.12);
    for (let k = 0; k < BAR_N; k++) { const hgt = (.02 + .08 * Math.abs(Math.sin(t * 8 + k * .8) * Math.sin(t * 2.7 + k * .3))) * grow; M4.compose(V.set(A0.x + (k - (BAR_N - 1) / 2) * .02, A0.y, A0.z), Q.identity(), S.set(1, Math.max(.001, hgt), 1)); barM.setMatrixAt(k, M4); }
  }
  hideAll(pageM, PAGE_N);
  if (s === 1) for (let k = 0; k < PAGE_N; k++) {
    const a = C.phone - .2 + k * (C.e[5] - C.phone) / PAGE_N, u = ramp(t, a, a + .8); if (u <= 0 || u >= 1) continue;
    A0.copy(phoneK.position); A2.copy(SCREEN); A1.lerpVectors(A0, A2, .5).add(V.set(0, -.02 + hash(k) * .06, .38));
    bez(A0, A1, A2, u, PP); Q.setFromEuler(new THREE.Euler(0, .6 * (1 - u), (hash(k) - .5) * .2)); M4.compose(PP, Q, S.setScalar(1 - .5 * u)); pageM.setMatrixAt(k, M4);
  }
  // step 2: 30 sticky notes out of the laptop into an arc around him; the coffee one comes forward
  hideAll(cardM, CARD_N);
  if (s === 2) for (let k = 0; k < CARD_N; k++) {
    const a = C.thirty7 - .25 + k * .035, u = ss(t, a, a + .6); if (u <= 0) continue;
    const ang = -1.3 + 2.6 * (k / (CARD_N - 1)), ring = k % 2 ? .95 : .8;
    A2.set(Math.sin(ang) * (ring + .1), 1.1 + Math.cos(ang) * .36 + (k % 3) * .06, -1.0 + Math.cos(ang) * .1);
    const cof = k === COFFEE_K, fwd = cof ? ss(t, C.coffee - .3, C.coffee + .25) : 0;
    bez(A0.copy(SCREEN), A1.set(-.2, 2.0, -.6), A2, u, PP);
    if (fwd > 0) PP.lerp(A1.set(.32, 1.18, -.1), fwd);
    const wig = C.thirty8 && t > C.thirty8 ? .25 * bump(t, C.thirty8, C.thirty8 + .7, .15) * Math.sin(t * 30 + k) : 0;
    Q.setFromEuler(new THREE.Euler(0, -ang * .4 * (1 - fwd), (hash(k) - .5) * .3 + wig + Math.sin(t * 1.5 + k) * .04));
    M4.compose(PP, Q, S.setScalar(cof && fwd > 0 ? 1 + .6 * fwd : 1)); cardM.setMatrixAt(k, M4);
    cardM.setColorAt(k, tmpC.set(cof && t > C.coffee - .3 ? 0xE8735A : STICKY[k % 4]));
  }
  cardM.instanceColor.needsUpdate = true;
  // step 3: five carousel slides fan out of the laptop into a row above him and slide like a carousel
  slides.forEach((m, k) => {
    m.visible = s === 3 && t > C.step3;
    if (!m.visible) return;
    const u = ss(t, C.hook - .2 + k * .12, C.hook + .4 + k * .12), slide = .12 * Math.sin((t - C.step3) * .9);
    const fan = k - (SLIDE_N - 1) / 2;
    A2.set(-.62 + fan * .13 + slide * .3, 1.36 + Math.abs(fan) * -.025 + .015 * Math.sin(t * 2 + k), -.5 - (SLIDE_N - 1 - k) * .03);
    PP.lerpVectors(SCREEN, A2, u); m.position.copy(PP); m.rotation.set(0, .35 * u, -fan * .1 * u); m.scale.setScalar((.3 + .7 * u) * .85);
  });
  // step 4: the month: 30 tiles fill in, one post a day
  hideAll(tileM, TILE_N);
  if (s === 4) for (let k = 0; k < TILE_N; k++) {
    const col = k % 15, row = Math.floor(k / 15), appear = ss(t, CU[3] + row * .05, CU[3] + .4 + row * .05);
    if (appear <= 0) continue;
    const on = ss(t, C.schedule + k * (1.3 / TILE_N), C.schedule + k * (1.3 / TILE_N) + .2);
    PP.set(-.735 + col * .105, 1.6 - row * .105, -1.15);
    const pop = t > C.l[10] ? .08 * Math.abs(Math.sin(t * 8 + k * .5)) * bump(t, C.l[10], C.l[10] + 1.6, .2) : 0;
    Q.setFromEuler(new THREE.Euler(0, Math.PI * (1 - on), 0)); M4.compose(PP, Q, S.setScalar(appear * (1 + pop))); tileM.setMatrixAt(k, M4);
    tileM.setColorAt(k, tmpC.set(on > .5 ? TILE_ON[k % 4] : 0xFFFDF8));
  }
  if (tileM.instanceColor) tileM.instanceColor.needsUpdate = true;
  // the morning: hearts float up from his phone
  hideAll(heartM, HEART_N);
  if (s === 5 && t > C.eighty - .2) for (let k = 0; k < HEART_N; k++) {
    const t0 = C.eighty - .2 + k * .09, u = ramp(t, t0, t0 + 1.6); if (u <= 0 || u >= 1) continue;
    PP.copy(phoneK.position).add(V.set(.42 + hash(k) * .35 + u * .15, .05 + u * .75, .1 + hash(k * 3) * .1));
    Q.setFromEuler(new THREE.Euler(0, 0, Math.sin(t * 3 + k) * .3)); M4.compose(PP, Q, S.setScalar(.06 * Math.sin(u * Math.PI) + .02)); heartM.setMatrixAt(k, M4);
  }
  hideAll(confM, CONF_N);
  const conf = (t0, o, n) => { for (let k = 0; k < n; k++) { const u = ramp(t, t0 + hash(k * 9) * .2, t0 + 2.2); if (u <= 0 || u >= 1) continue; const a = hash(k) * Math.PI * 2, sp = .5 + hash(k * 3) * .6; PP.set(o.x + Math.cos(a) * sp * u, o.y + (1.6 + hash(k * 7)) * u - 2.4 * u * u, o.z + Math.sin(a) * sp * u * .6); Q.setFromEuler(new THREE.Euler(t * 6 + k, t * 4 + k * 2, 0)); M4.compose(PP, Q, S.setScalar(1)); confM.setMatrixAt(k, M4); } };
  if (s === 4 && t > C.l[10] - .1) conf(C.l[10] - .1, A0.set(0, 1.4, -.4), CONF_N);
  if (s === 8 && t > CU[7] + .2) conf(CU[7] + .2, A0.set(.1, 1.5, -.3), 50);

  // the camera
  const fov = camAt(t);
  camera.position.copy(CAMP);
  camera.position.x += Math.sin(t * .37) * .006; camera.position.y += Math.sin(t * .29 + 1) * .005;
  camera.fov = fov;
  const look = CAML.clone();
  const cv = window.POSTS_COVER;
  if (cv) { camera.position.set(...cv.cam); camera.fov = cv.fov; look.set(...cv.look); }
  camera.updateProjectionMatrix(); camera.lookAt(look); camera.updateMatrixWorld();

  // grade
  let fl = 0; for (const ct of SHOT_STARTS) if (ct > 0) fl += .12 * Math.exp(-(((t - ct) / .06) ** 2)) * (t >= ct ? 1 : 0);
  for (const ct of CU) fl += .35 * Math.exp(-(((t - ct) / .07) ** 2)) * (t >= ct ? 1 : .2);
  fl += .3 * pulse(t, C.eighty, .08);
  let fb = 0; for (const f of FOC) fb = Math.max(fb, bump(t, f.a, f.b, .2));
  grade.uniforms.uFlash.value = cv ? 0 : fl;
  grade.uniforms.uSat.value = 1.05;
  grade.uniforms.uCool.value = Lk === LOOKS.night ? .15 : 0;
  grade.uniforms.uWarm.value = Lk === LOOKS.dusk ? .2 : Lk === LOOKS.morning ? .12 : 0;
  grade.uniforms.uBars.value = 0; grade.uniforms.uScan.value = 0; grade.uniforms.uCon.value = .04;
  grade.uniforms.uCA.value = .0008;
  grade.uniforms.uTime.value = t;
  grade.uniforms.uVig.value = .3 + .25 * fb;
  faceKey.position.copy(camera.position).add(V.set(.25, .35, 0)); faceKey.intensity = Lk === LOOKS.night ? 1.6 : 1.3;
  const fd = camera.position.distanceTo(look);
  cocPass.uniforms.uF.value = cv?.focus ?? fd;
  cocPass.uniforms.uAp.value = cv ? (cv.ap ?? .3) : (CAMAP ?? clamp(1.6 / fd, .15, .8));
  dofPass.uniforms.uMaxR.value = 22;
  const ext = clamp(fd * 1.1, 2.5, 10);
  sun.target.position.copy(look); sun.position.copy(look).add(V2.set(...Lk.sp).normalize().multiplyScalar(14));
  Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext, bottom: -ext, near: .5, far: 40 });
  sun.shadow.camera.updateProjectionMatrix();
  scene.fog.near = 12; scene.fog.far = 45;
  for (const m of [pageM, cardM, confM, barM, tileM, heartM]) m.instanceMatrix.needsUpdate = true;
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures (after the fonts), then the first frame
function buildTextures() {
  const grad = (stops, stars = false) => pix(64, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); if (stars) for (let k = 0; k < 40; k++) { g.fillStyle = "rgba(255,255,255,.8)"; g.fillRect(Math.floor(hash(k) * w), Math.floor(hash(k * 3) * h * .55), 1, 1); } });
  SKY.dusk = grad([[0, "#2B2350"], [.45, "#7A4F8E"], [.72, "#E9849A"], [1, "#F7B27A"]]);
  SKY.night = grad([[0, "#0B0A1E"], [.6, "#1E1A44"], [1, "#3A2E6A"]], true);
  SKY.morning = grad([[0, "#8FC4F0"], [.6, "#CFE4F5"], [1, "#FBE6C8"]]);
  TEX.towerWin = pix(64, 128, (g, w, h) => { g.fillStyle = "#000"; g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = 0; j < 10; j++) if (hash(i * 13 + j * 7) > .45) { g.fillStyle = hash(i + j) > .5 ? "#FFD08A" : "#FFE9C4"; g.fillRect(6 + i * 15, 6 + j * 12, 8, 7); } });
  const lap = (title, draw) => pix(420, 270, (g, w, h) => { g.fillStyle = "#F7F3FF"; g.fillRect(0, 0, w, h); g.fillStyle = "#6B5BD6"; g.fillRect(0, 0, w, 34); g.fillStyle = "#fff"; g.font = FONT(800, 18); g.fillText(title, 14, 23); draw(g, w, h); });
  TEX.lapIdle = lap("Post ideas.doc", (g, w) => { g.fillStyle = "#1E1B18"; g.font = FONT(800, 24); g.fillText("Post ideas:", 20, 78); g.fillStyle = "#6B5BD6"; g.fillRect(20, 96, 3, 26); g.fillStyle = "#B8B0CC"; g.font = FONT(700, 16); g.fillText("(nothing yet)", 30, 116); });
  TEX.lapChat = lap("ChatGPT", (g, w) => { g.fillStyle = "#EDE7FB"; rr(g, 120, 44, w - 136, 40, 12); g.fill(); g.fillStyle = "#1E1B18"; g.font = FONT(700, 13); g.fillText("Turn this transcript into 30 posts...", 132, 69); const ideas = ["My 6 AM coffee rule", "Phone-free first hour", "2-minute morning reset", "What I stopped buying", "The note I write daily"]; ideas.forEach((n, k) => { g.fillStyle = k === 0 ? "#FFD9CF" : "#FFFFFF"; rr(g, 16, 94 + k * 34, w - 32, 28, 8); g.fill(); g.fillStyle = "#6B5BD6"; g.font = MONO(14); g.fillText(String(k + 1).padStart(2, "0"), 26, 113 + k * 34); g.fillStyle = "#1E1B18"; g.font = FONT(800, 15); g.fillText(n, 60, 113 + k * 34); }); });
  TEX.lapSlides = lap("Carousel · post 1", (g, w) => { for (let k = 0; k < 5; k++) { g.fillStyle = k === 0 ? "#6B5BD6" : "#EDE7FB"; rr(g, 16 + k * 80, 60, 70, 88, 8); g.fill(); } g.fillStyle = "#fff"; g.font = FONT(800, 12); g.fillText("HOOK", 30, 108); g.fillStyle = "#1E1B18"; g.font = FONT(800, 16); g.fillText("I drank coffee wrong", 20, 186); g.fillText("for 10 years.", 20, 208); g.fillStyle = "#5b5650"; g.font = MONO(13); g.fillText("caption ✓   7 slides ✓", 20, 248); });
  TEX.lapPlanner = lap("Meta Business Suite · Planner", (g, w) => { for (let k = 0; k < 30; k++) { const c = k % 6, r = Math.floor(k / 6); g.fillStyle = ["#6B5BD6", "#E8735A", "#3FA372", "#F2B33D"][k % 4]; rr(g, 18 + c * 66, 46 + r * 42, 58, 34, 6); g.fill(); } });
  const phone = (draw) => pix(132, 270, (g, w, h) => { g.fillStyle = "#14121F"; g.fillRect(0, 0, w, h); draw(g, w, h); });
  TEX.phoneMemo = phone((g, w) => { g.fillStyle = "#fff"; g.font = FONT(800, 13); g.fillText("Voice Memos", 12, 30); g.fillStyle = "#E8735A"; g.beginPath(); g.arc(w / 2, 220, 18, 0, Math.PI * 2); g.fill(); g.fillStyle = "#9FF5FF"; for (let k = 0; k < 14; k++) { const hh = 8 + 40 * Math.abs(Math.sin(k * 1.4)); g.fillRect(12 + k * 8, 100 - hh / 2, 4, hh); } g.fillStyle = "#fff"; g.font = MONO(16); g.fillText("2:00", 44, 160); });
  TEX.phoneStats = phone((g, w) => { g.fillStyle = "#6B5BD6"; g.fillRect(10, 40, w - 20, 110); g.fillStyle = "#fff"; g.font = FONT(800, 13); g.fillText("I drank coffee", 16, 80); g.fillText("wrong for 10 yrs", 16, 98); g.fillStyle = "#fff"; g.font = FONT(800, 22); g.fillText("80K", 12, 190); g.font = FONT(700, 11); g.fillText("views", 12, 206); g.fillStyle = "#FF6B8A"; g.font = FONT(800, 22); g.fillText("♥ 6.2K", 12, 240); });
  TEX.phoneSelfie = phone((g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#F7C9A8"); gr.addColorStop(1, "#E9849A"); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "#E8735A"; g.beginPath(); g.arc(w / 2, h - 30, 16, 0, Math.PI * 2); g.fill(); g.strokeStyle = "#fff"; g.lineWidth = 3; g.beginPath(); g.arc(w / 2, h - 30, 20, 0, Math.PI * 2); g.stroke(); g.fillStyle = "#fff"; g.font = MONO(12); g.fillText("● REC", 10, 24); });
  const SL = [["HOOK", "I drank coffee wrong for 10 years", "#6B5BD6", "#fff"], ["1", "Coffee before water", "#FFFDF8", "#1E1B18"], ["2", "Phone in the first hour", "#FFFDF8", "#1E1B18"], ["3", "The 2-minute fix", "#FFFDF8", "#1E1B18"], ["SAVE", "Try it tomorrow", "#E8735A", "#fff"]];
  SL.forEach(([tag, txt, bg, fg], k) => { TEX["slide" + k] = pix(240, 300, (g, w, h) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.strokeStyle = "#1E1B18"; g.lineWidth = 8; g.strokeRect(4, 4, w - 8, h - 8); g.fillStyle = fg; g.font = MONO(22); g.fillText(tag, 20, 46); g.font = FONT(800, 30); const words = txt.split(" "); let line = "", y = 110; for (const wd of words) { const tst = line ? line + " " + wd : wd; if (g.measureText(tst).width > w - 40) { g.fillText(line, 20, y); line = wd; y += 36; } else line = tst; } g.fillText(line, 20, y); g.fillStyle = fg; g.globalAlpha = .5; g.font = MONO(14); g.fillText(`${k + 1}/5`, w - 54, h - 22); g.globalAlpha = 1; }); });
  for (const [m, key, prop] of LATE) { if (TEX[key]) { m[prop || "map"] = TEX[key]; m.needsUpdate = true; } }
}

const ready = (async () => {
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 30px JBMono")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh || o.isMesh) o.frustumCulled = false; });
  renderer.compile(scene, camera);
  renderAt(window.POSTS_COVER ? window.POSTS_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["posts"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.POSTS_COVER ? window.POSTS_COVER.t : e.detail.time));
window.POSTS_DEBUG = { renderAt, HEADW };
