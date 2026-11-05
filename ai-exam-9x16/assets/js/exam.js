// AI Exam reel: the 3D world, in the soft low-poly, flat-shaded style of the owner's reference. YOU (a chibi student
// with round glasses and a yellow jacket) and HOOT (our own AI study owl with glowing eyes and a tiny graduation cap)
// at a dusk desk by a city window, on a night bus, and in an exam hall. Everything is a pure function of time t,
// drawn on HyperFrames' hf-seek; cue times come from the dialogue (window.CT, written by build/generate.py).
//   close     you and your clone wave in front of the studio
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

// ---------------------------------------------------------------- SET 1: the study desk by the city window (x 0)
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
// the desk, chair, lamp, laptop, books, mug, pencils, plant, sticky notes, notes stack
box(1.7, .05, .72, woodM, 0, .6, 0); for (const sx of [-.8, .8]) for (const sz of [-.3, .3]) box(.05, .58, .05, woodD, sx, .29, sz);
box(1.6, .2, .04, woodD, 0, .47, .33);
const seat = rbox(.42, .06, .4, .02, 0x3A3550, 0, .3, -.58); rbox(.42, .5, .06, .03, 0x3A3550, 0, .58, -.8); cyl(.025, .025, .28, 0x222222, 0, .14, -.58, 6);
const lampG = new THREE.Group(); lampG.position.set(-.62, .625, -.12); ROOT3.add(lampG);
cyl(.08, .09, .025, 0x2E2638, 0, .012, 0, 10, lampG); const la = cyl(.012, .012, .36, 0x2E2638, 0, .19, 0, 6, lampG); la.rotation.z = -.25;
const shadeM = new THREE.MeshStandardMaterial({ color: 0xF2B33D, roughness: .6, flatShading: true, emissive: 0xFFB050, emissiveIntensity: .4, side: THREE.DoubleSide });
const shade = mesh(new THREE.ConeGeometry(.11, .14, 8, 1, true), shadeM, .1, .38, .02, lampG); shade.rotation.z = -.6;
const bulb = mesh(new THREE.IcosahedronGeometry(.035, 1), glow(0xFFE2A8), .12, .33, .02, lampG, false);
lampL.position.set(-.5, 1.0, -.05);
const lap = new THREE.Group(); lap.position.set(-.42, .625, -.1); lap.rotation.y = .6; ROOT3.add(lap);
rbox(.46, .02, .32, .01, 0xB8BCC6, 0, .01, 0, lap); box(.4, .004, .2, 0x2A2A33, 0, .021, -.02, lap);
const lid = new THREE.Group(); lid.position.set(0, .02, .16); lid.rotation.x = .22; lap.add(lid);
rbox(.46, .3, .015, .01, 0xB8BCC6, 0, .15, 0, lid);
const lapScrM = texMat("lapNotes", { transparent: false }); const lapScr = mesh(new THREE.PlaneGeometry(.42, .27), lapScrM, 0, .15, -.009, lid, false); lapScr.rotation.y = Math.PI;
box(.06, .06, .004, glow(0xEDE7FB), 0, .15, .009, lid, false);
// owl's book stack, a mug, pencil cup, plant, sticky notes, headphones
box(.36, .07, .26, 0x2F8F7A, .5, .66, .06); box(.34, .065, .25, 0xE8735A, .5, .725, .05); box(.33, .06, .245, creamM, .5, .67, .07);
cyl(.045, .04, .1, 0xEDE7FB, .25, .675, .2, 10); cyl(.035, .035, .005, 0x6B4A32, .25, .726, .2, 10);
cyl(.04, .035, .12, 0x6B5BD6, -.38, .685, -.22, 8); for (let k = 0; k < 4; k++) { const p = cyl(.007, .007, .16, [0xF2B33D, 0xE8735A, 0x3FA372, 0x6B5BD6][k], -.38 + (k - 1.5) * .012, .76, -.22 + (k % 2 - .5) * .015, 6); p.rotation.z = (k - 1.5) * .12; }
cyl(.06, .05, .08, 0xC9644E, .75, .665, -.25, 8); for (let k = 0; k < 6; k++) { const l = ico(.06, 0, 0x5E9A4C, .75 + Math.cos(k) * .05, .75 + (k % 3) * .04, -.25 + Math.sin(k) * .05); l.scale.set(.6, 1.2, .6); l.rotation.z = Math.cos(k * 2) * .6; }
for (const [x, y, c] of [[-1.15, 1.3, 0xF2E36B], [-1.0, 1.15, 0xF29BB8], [1.1, 1.25, 0x9FEFD4]]) { const s = box(.14, .14, .01, c, x, y, -1.58); s.rotation.z = (x > 0 ? .1 : -.08); }
// the 300-page notes stack (drops in, then flies into the laptop page by page)
const notesG = new THREE.Group(); ROOT3.add(notesG);
const paperTex = pix(64, 64, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#E9E2D6"; for (let y = 2; y < h; y += 3) g.fillRect(0, y, w, 1); });
const stackM = [fm(0xFFFDF8, { map: paperTex }), fm(0xFFFDF8, { map: paperTex }), fm(0xFFFDF8), fm(0xFFFDF8), fm(0xFFFDF8, { map: paperTex }), fm(0xFFFDF8, { map: paperTex })];
const stack = new THREE.Group(); notesG.add(stack);
for (let k = 0; k < 6; k++) { const sl = mesh(new THREE.BoxGeometry(.28, 1 / 6, .36), stackM, (hash(k) - .5) * .03, (k + .5) / 6, (hash(k * 3) - .5) * .03, stack); sl.rotation.y = (hash(k * 7) - .5) * .18; }
for (let k = 0; k < 5; k++) box(.05, .012, .04, [0xF2B33D, 0xE8735A, 0x7FD8B0, 0x6B5BD6, 0xF29BB8][k], .14 + .01, (k + .7) / 6, -.1 + k * .05, stack, false);
const stackTop = mesh(new THREE.PlaneGeometry(.26, .34), texMat("noteTop", { transparent: false }), 0, 0, 0, notesG, false); stackTop.rotation.x = -Math.PI / 2;
const NOTES = new THREE.Vector3(.17, .625, .16);

// ---------------------------------------------------------------- SET 2: the night bus (x 20)
const BUS = new THREE.Group(); BUS.position.set(20, 0, 0); ROOT3.add(BUS);
box(2.2, .05, 6, fm(0x3A3F4E), 0, -.025, 0, BUS, false);
box(.08, 2.2, 6, fm(0xD8D4E6), -1.1, 1.1, 0, BUS); box(2.2, .06, 6, fm(0xE6E2F0), 0, 2.2, 0, BUS);
const busWinM = new THREE.MeshBasicMaterial({ color: 0x1A1830, toneMapped: false });
box(.06, 1.0, 6, fm(0xD8D4E6), 1.1, .45, 0, BUS); box(.06, .45, 6, fm(0xD8D4E6), 1.1, 1.98, 0, BUS);
for (let k = 0; k < 5; k++) box(.07, .82, .06, fm(0xB8B2CC), 1.1, 1.36, -2.4 + k * 1.2, BUS);
for (let k = 0; k < 3; k++) { const z = -2.6 + k * 1.15; rbox(.62, .12, .5, .04, 0x3B5BA5, .55, .45, z, BUS); rbox(.62, .62, .1, .05, 0x3B5BA5, .55, .8, z - .22, BUS); cyl(.03, .03, .4, 0x555566, .55, .2, z, 6, BUS); }
for (const z of [-1.5, .9]) cyl(.022, .022, 2.2, 0xF2B33D, -.2, 1.1, z, 8, BUS);
const busLampM = glow(0xFFF1D6); for (const z of [-2, 0, 2]) box(.5, .03, .9, busLampM, 0, 2.165, z, BUS, false);
const passing = [];
for (let k = 0; k < 18; k++) { const m = add(new THREE.Mesh(new THREE.BoxGeometry(.3 + (k % 3) * .2, 1.2 + (k % 4) * .5, .3), new THREE.MeshBasicMaterial({ color: [0xFFC27A, 0xFF8AB0, 0x8AD8FF, 0xFFE9A8][k % 4], toneMapped: false })), false, false, BUS); passing.push(m); }
const streetGlow = add(new THREE.Mesh(new THREE.PlaneGeometry(30, 3), new THREE.MeshBasicMaterial({ color: 0x251E3A, toneMapped: false })), false, false, BUS); streetGlow.position.set(4.5, 1.2, 0); streetGlow.rotation.y = -Math.PI / 2;

// ---------------------------------------------------------------- SET 3: the exam hall, morning (x 40)
const HALL = new THREE.Group(); HALL.position.set(40, 0, 0); ROOT3.add(HALL);
box(9, .05, 9, fm(0xC9B49A), 0, -.025, -2, HALL, false);
box(9, 3.6, .12, fm(0xEDE4D6), 0, 1.8, -5.5, HALL); const hw = fm(0xE4DACB);
box(.12, .9, 9, hw, -4.5, .45, -2, HALL); box(.12, 1.1, 9, hw, -4.5, 3.05, -2, HALL);
for (const [z0, z1] of [[-6.5, -4.65], [-3.35, -2.75], [-1.45, -.85], [.45, 2.5]]) box(.12, 1.6, z1 - z0, hw, -4.5, 1.7, (z0 + z1) / 2, HALL);
const hallSkyM = new THREE.MeshPhysicalMaterial({ color: 0xEAF4FF, transparent: true, opacity: .18, roughness: .05, depthWrite: false });
const outSky = mesh(new THREE.PlaneGeometry(30, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, fog: false }), -9, 2, -2, HALL, false); outSky.rotation.y = Math.PI / 2; LATE.push([outSky.material, "skyMorning"]);
box(.05, 1.0, 3, fm(0xCDB89C), -4.85, .45, -2.1, HALL);
for (let k = 0; k < 3; k++) { box(.04, 1.6, 1.3, hallSkyM, -4.43, 1.7, -4 + k * 1.9, HALL, false); box(.06, 1.7, .06, fm(0xFFFDF8), -4.42, 1.7, -4 + k * 1.9, HALL); box(.06, .06, 1.4, fm(0xFFFDF8), -4.42, 1.7, -4 + k * 1.9, HALL); }
box(2.6, 1.0, .04, fm(0x2F4A3E), .3, 1.75, -5.42, HALL);
const boardTxt = mesh(new THREE.PlaneGeometry(2.4, .8), texMat("board", { transparent: false }), .3, 1.75, -5.39, HALL, false);
const clockFace = mesh(new THREE.CircleGeometry(.22, 16), texMat("clock", { transparent: false }), 2.4, 2.4, -5.42, HALL, false);
const HDESKS = [];
for (let i = 0; i < 3; i++) for (let j = 0; j < 4; j++) { const x = -1.6 + i * 1.6, z = -4.2 + j * 1.3; rbox(.8, .04, .5, .01, 0xB98E62, x, .6, z, HALL); for (const sx of [-.35, .35]) box(.035, .58, .035, 0x555566, x + sx, .29, z); rbox(.4, .05, .38, .02, 0x6B5BD6, x, .3, z + .55, HALL); HDESKS.push([x, z]); box(.32, .003, .42, 0xFFFDF8, x + .05, .622, z + .03, HALL, false); }
const examPaper = mesh(new THREE.PlaneGeometry(.32, .42), texMat("exam", { transparent: false }), 0, 0, 0, HALL, false); examPaper.rotation.x = -Math.PI / 2;
const pencil = cyl(.008, .008, .17, 0xF2B33D, 0, 0, 0, 6, ROOT3);
const resultPaper = mesh(new THREE.PlaneGeometry(.3, .4), texMat("result", { transparent: false }), 0, 0, 0, ROOT3, false);

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
  P(new THREE.IcosahedronGeometry(.3, 1), hair, face, 0, -.1, -.1).scale.set(1.04, 1.12, .78);
  for (const s of [-1, 1]) { const lock = P(new THREE.IcosahedronGeometry(.12, 1), hair, face, s * .255, -.12, .02); lock.scale.set(.45, 1.35, .75); }
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
  you: { top: 0xF2B33D, inner: 0x2E2A38, pants: 0x2E2A3A, skin: 0xF4D1B5, skinD: 0xE6B596, hair: 0x3A2C2A, shoe: 0xFFFDF8, glasses: true, long: true, seed: 2 },
  ex1: { top: 0x3FA372, inner: 0xFFFDF8, pants: 0x3A3550, skin: 0xC98E64, skinD: 0xB27650, hair: 0x1E1B18, shoe: 0x2E2A38, seed: 5 },
  ex2: { top: 0x6B5BD6, inner: 0xFFFDF8, pants: 0x2E2A3A, skin: 0xF0C8A8, skinD: 0xDDAE8C, hair: 0xA0522D, shoe: 0xFFFDF8, bun: true, seed: 7 },
  ex3: { top: 0xE8735A, inner: 0x2E2A38, pants: 0x3A5A8C, skin: 0x8E5E40, skinD: 0x784C32, hair: 0x1E1B18, shoe: 0x2E2A38, seed: 9 },
};
const YOU = makeKid(SP.you), EX1 = makeKid(SP.ex1), EX2 = makeKid(SP.ex2), EX3 = makeKid(SP.ex3);

// ---------------------------------------------------------------- HOOT: the AI study owl (our own mascot)
function makeOwl() {
  const root = new THREE.Group(); ROOT3.add(root);
  const body = new THREE.Group(); root.add(body);
  const parts = [];
  const P = (geo, m, parent, x, y, z, cast = true) => { const o = new THREE.Mesh(geo, m.isMaterial ? m : fm(m)); o.position.set(x, y, z); o.castShadow = cast; o.receiveShadow = true; parent.add(o); parts.push(o); return o; };
  const vio = fm(0x6B5BD6), vioD = fm(0x5446B8), lav = fm(0xCFC6F5), orange = fm(0xF2A33D);
  P(new THREE.IcosahedronGeometry(.17, 1), vio, body, 0, .17, 0).scale.set(1, 1.08, .9);
  P(new THREE.IcosahedronGeometry(.11, 1), lav, body, 0, .14, .07).scale.set(1, 1.1, .6);
  const head = new THREE.Group(); head.rotation.order = "YXZ"; head.position.y = .3; body.add(head);
  P(new THREE.IcosahedronGeometry(.15, 1), vio, head, 0, .06, 0).scale.set(1.2, .95, .95);
  const eyeM = glow(0x7FFFD4), pupM = new THREE.MeshBasicMaterial({ color: 0x1A1530 });
  const EY = { open: [], happy: [], closed: [], wide: [] };
  for (const s of [-1, 1]) {
    P(new THREE.CircleGeometry(.07, 10), lav, head, s * .065, .07, .135, false).rotation.y = s * .18;
    const ring = P(new THREE.CircleGeometry(.045, 14), eyeM, head, s * .065, .07, .14, false); ring.rotation.y = s * .18;
    const pup = P(new THREE.CircleGeometry(.02, 10), pupM, ring, 0, 0, .002, false);
    EY.open.push(ring);
    const hp = P(new THREE.TorusGeometry(.035, .011, 5, 12, Math.PI), eyeM, head, s * .065, .06, .142, false); hp.rotation.y = s * .18; EY.happy.push(hp);
    const cl = P(new THREE.BoxGeometry(.07, .014, .005), eyeM, head, s * .065, .07, .142, false); cl.rotation.y = s * .18; EY.closed.push(cl);
    const wd = P(new THREE.CircleGeometry(.055, 14), eyeM, head, s * .065, .07, .141, false); wd.rotation.y = s * .18; P(new THREE.CircleGeometry(.016, 10), pupM, wd, 0, 0, .002, false); EY.wide.push(wd);
    const tuft = P(new THREE.ConeGeometry(.04, .11, 4), vioD, head, s * .12, .17, -.01); tuft.rotation.z = -s * .45;
  }
  const beak = P(new THREE.ConeGeometry(.026, .06, 4), orange, head, 0, .02, .15); beak.rotation.x = Math.PI * .55;
  // a tiny graduation cap
  const capG = new THREE.Group(); capG.position.set(0, .2, -.01); capG.rotation.set(-.12, .2, .08); head.add(capG);
  P(new THREE.CylinderGeometry(.075, .085, .05, 8), fm(0x1E1B18), capG, 0, 0, 0); P(new THREE.BoxGeometry(.22, .014, .22), fm(0x1E1B18), capG, 0, .03, 0);
  const tassel = P(new THREE.CylinderGeometry(.006, .006, .08, 4), fm(0xF2B33D), capG, .1, -.01, .1);
  const wings = [];
  for (const s of [-1, 1]) { const w = new THREE.Group(); w.position.set(s * .16, .24, 0); body.add(w); P(new THREE.IcosahedronGeometry(.1, 0), vioD, w, 0, -.08, 0).scale.set(.35, 1, .8); wings.push(w); }
  for (const s of [-1, 1]) P(new THREE.IcosahedronGeometry(.03, 0), orange, root, s * .055, .015, .08).scale.set(1.2, .6, 1.3);
  return { root, body, head, wings, EY, parts, beak, tassel };
}
const OWL = makeOwl();
const opose = (o = {}) => ({ x: 0, y: 0, z: 0, ry: 0, s: 1, lean: 0, hy: 0, hp: 0, hr: 0, w: [.1, .1], hop: 0, ...o });
function applyOwl(p) {
  OWL.root.position.set(p.x, p.y + p.hop, p.z); OWL.root.rotation.y = p.ry; OWL.root.scale.setScalar(p.s);
  OWL.body.rotation.x = p.lean; OWL.head.rotation.set(p.hp, p.hy, p.hr);
  OWL.wings[0].rotation.z = -p.w[0]; OWL.wings[1].rotation.z = p.w[1];
}
function setOwl(f) {
  let eyes = f.eyes || "open";
  if (eyes === "open" && blinkAt(4.4, NOW) > .5) eyes = "closed";
  for (const k in OWL.EY) for (const m of OWL.EY[k]) m.visible = k === eyes;
}

// ---------------------------------------------------------------- props: headphones, backpack, phone, papers, cards, pages
const phonesK = new THREE.Group(); YOU.face.add(phonesK);
{ const band = new THREE.Mesh(new THREE.TorusGeometry(.31, .022, 6, 16, Math.PI), fm(0x2E2A38)); band.position.y = .02; phonesK.add(band); for (const s of [-1, 1]) { const c = new THREE.Mesh(new THREE.CylinderGeometry(.075, .075, .06, 10), fm(0x6B5BD6)); c.rotation.z = Math.PI / 2; c.position.set(s * .3, -.02, 0); phonesK.add(c); } }
const phonesO = new THREE.Group(); OWL.head.add(phonesO);
{ const band = new THREE.Mesh(new THREE.TorusGeometry(.18, .014, 6, 14, Math.PI), fm(0x2E2A38)); band.position.y = .06; phonesO.add(band); for (const s of [-1, 1]) { const c = new THREE.Mesh(new THREE.CylinderGeometry(.045, .045, .04, 10), fm(0xF2B33D)); c.rotation.z = Math.PI / 2; c.position.set(s * .18, .05, 0); phonesO.add(c); } }
const bag = new THREE.Group(); ROOT3.add(bag);
rbox(.34, .38, .2, .06, 0xE8735A, 0, 0, 0, bag); rbox(.3, .14, .04, .03, 0xC9644E, 0, -.06, .11, bag);
const bagOpen = rbox(.32, .04, .18, .02, 0x2E2A38, 0, .19, 0, bag);
const flap = new THREE.Group(); flap.position.set(0, .19, -.1); bag.add(flap); rbox(.34, .03, .22, .02, 0xC9644E, 0, 0, .11, flap);
const phoneK = new THREE.Group(); ROOT3.add(phoneK);
rbox(.07, .14, .012, .01, 0x1E1B18, 0, 0, 0, phoneK); mesh(new THREE.PlaneGeometry(.062, .125), texMat("phoneWave", { transparent: false }), 0, 0, .0065, phoneK, false);
const testPaper = mesh(new THREE.PlaneGeometry(.26, .34), texMat("test62", { transparent: false, side: THREE.DoubleSide }), 0, 0, 0, ROOT3, false);
// pages flying into the laptop, flashcards orbiting, confetti, glints
const PAGE_N = 70;
const pageM = new THREE.InstancedMesh(new THREE.PlaneGeometry(.12, .16), new THREE.MeshStandardMaterial({ map: paperTex, side: THREE.DoubleSide, roughness: .8, emissive: 0x332a22 }), PAGE_N); ROOT3.add(pageM);
const CARD_N = 50;
const cardM = new THREE.InstancedMesh(new RoundedBoxGeometry(.14, .09, .006, 1, .006), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6, emissive: 0x222222 }), CARD_N); ROOT3.add(cardM);
for (let k = 0; k < CARD_N; k++) cardM.setColorAt(k, tmpC.set([0xFFFDF8, 0xEDE7FB, 0xF7E3A6, 0xFFE0D6][k % 4]));
const CONF_N = 90;
const confM = new THREE.InstancedMesh(new THREE.BoxGeometry(.025, .04, .004), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6, emissive: 0x333333 }), CONF_N); ROOT3.add(confM);
for (let k = 0; k < CONF_N; k++) confM.setColorAt(k, tmpC.set([0xE8735A, 0xF2B33D, 0x7FFFD4, 0x6B5BD6, 0xFFFDF8][k % 5]));
const BAR_N = 24;
const barM = new THREE.InstancedMesh(new THREE.BoxGeometry(.018, 1, .018), glow(0x7FFFD4), BAR_N); ROOT3.add(barM);
const ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
const hideAll = (m, n) => { for (let k = 0; k < n; k++) m.setMatrixAt(k, ZERO); };
const bez = (p0, p1, p2, u, out) => out.set((1 - u) ** 2 * p0.x + 2 * (1 - u) * u * p1.x + u * u * p2.x, (1 - u) ** 2 * p0.y + 2 * (1 - u) * u * p1.y + u * u * p2.y, (1 - u) ** 2 * p0.z + 2 * (1 - u) * u * p1.z + u * u * p2.z);

// ---------------------------------------------------------------- scenes, poses and faces
const lineAt = (t) => { for (let i = 0; i < C.lines.length; i++) if (t >= C.lines[i].s - .05 && t <= C.lines[i].e + .05) return C.lines[i]; return null; };
const talking = (who, t) => { const ln = lineAt(t); return !!ln && ln.who === who; };
const SITD = sitY(.33);
const SIT = (x, z, ry, seat = .33) => pose({ x, y: sitY(seat), z, ry, l: [[1.5, 1.5], [1.5, 1.5]], a: [[.55, .1, .9], [.55, .1, .9]] });
const withArms = (p, a, o = {}) => ({ ...p, a, ...o });
const DESK_HANDS = [[.75, .05, .75], [.75, .05, .75]];
const CHEER = (t) => [[.3, 2.6 + .12 * Math.sin(t * 10), .25], [.3, 2.6 + .12 * Math.sin(t * 10 + 1.5), .25]];
const HOLD = [[.72, -.28, 1.2], [.72, -.28, 1.2]];
const PLEAD = [[1.05, -.38, 1.55], [1.05, -.38, 1.55]];
const WAVE_R = (t) => [[.3, 2.4 + .3 * Math.sin(t * 9), .5], [.9, -.2, 1.1]];
const idle = (p, t, s) => ({ ...p, lean: p.lean + .015 * Math.sin(t * 1.4 + s), hr: p.hr + .03 * Math.sin(t * .9 + s * 2), hy: p.hy + .04 * Math.sin(t * .6 + s) });
const DESK = { x: 0, z: -.58 };
function youAt(t, s) {
  if (s <= 2 || s === 4 || s === 5) {
    let p = idle(withArms(SIT(DESK.x, DESK.z, 0), DESK_HANDS), t, 1);
    let f = { mouth: "smile", eyes: "open" };
    if (s === 0) {
      if (t < C.l[1]) { p = { ...p, hp: -.05, hr: .06 * Math.sin(t * 7), lean: .05 }; f = { mouth: "wide", eyes: "wide" }; }
      else if (t < C.l[2]) { p = { ...p, hy: .5, hp: .05 }; f = { mouth: "flat", eyes: "open" }; }
      else if (t < C.l[3]) { const throwA = bump(t, C.and3 - .2, C.notes, .25); p = mixP(p, withArms(p, [[1.6, .3, .2], [1.6, .3, .2]], { lean: .1, hp: -.1 }), throwA); f = { mouth: "wide", eyes: "wide" }; }
      else if (t < C.l[4]) { p = { ...p, hy: .45 }; f = { mouth: "flat", eyes: "open" }; }
      else { p = { ...p, hy: .35, hp: -.05, hr: .12 }; f = { mouth: "o", eyes: "wide" }; }
    }
    if (s === 1) { p = { ...p, hy: -.25, hp: .2 }; f = { mouth: t > C.drop ? "o" : "smile", eyes: t > C.drop ? "wide" : "open" }; }
    if (s === 2) {
      if (t < C.l[7]) { p = { ...p, hy: .2, hp: .05 }; f = { mouth: "smile", eyes: "open" }; }
      else { p = mixP(p, withArms(p, [[1.1, .2, 1.9], [1.1, .2, 1.9]], { lean: -.08, hp: -.08 }), ss(t, C.l[7], C.l[7] + .3)); f = { mouth: "wide", eyes: "wide" }; }
    }
    if (s === 4) {
      p = { ...p, hp: .12 };
      if (t > C.test - .3) p = mixP(p, withArms(p, HOLD, { hp: .3 }), ss(t, C.test - .3, C.test + .1));
      if (t > C.sixty - .2 && t < C.l[11]) f = { mouth: "sad", eyes: "half" };
      if (t > C.l[11]) p = withArms(p, HOLD, { hp: .35, lean: .1 });
      if (t > C.ninety - .25) { p = mixP(p, withArms(p, CHEER(t), { hp: -.15, lean: -.05, y: p.y + .02 * Math.abs(Math.sin(t * 8)) }), ss(t, C.ninety - .25, C.ninety + .1)); f = { mouth: "grin", eyes: "happy" }; }
      else if (t > C.l[11]) f = { mouth: "flat", eyes: "open" };
    }
    if (s === 5) {
      p = { ...p, hy: .22 };
      if (t < C.l[14]) { p = mixP(p, withArms(p, HOLD, { hy: .22, lean: .05 }), ss(t, C.small - .3, C.small + .2)); f = { mouth: "smirk", eyes: "half" }; }
      else if (t < C.l[15]) { p = withArms(p, HOLD, { hy: .25 }); f = { mouth: "o", eyes: "wide" }; }
      else { p = mixP(withArms(p, HOLD, { hy: .25 }), withArms(p, PLEAD, { hy: .05, hp: -.1, hr: .12 }), ss(t, C.please - .3, C.please)); f = { mouth: "sad", eyes: "wide" }; }
    }
    return { vis: true, p, f: { ...f, talk: talking("you", t) && f.mouth !== "wide" } };
  }
  if (s === 3) {
    const p = idle(withArms(SIT(20.45, -.3, 0, .51), [[.85, -.25, 1.6], [.8, -.2, 1.5]], { hp: .25, hy: -.1 }), t, 2);
    return { vis: true, p: { ...p, lean: p.lean + .01 * Math.sin(t * 13) }, f: { mouth: "smile", eyes: "happy" }, phones: true };
  }
  if (s === 6) {
    const p = idle(withArms(SIT(40, -3.65, Math.PI), [[.85, .05, 1.0], [.6, .1, .8]], { hp: .2 }), t, 3);
    p.a[0][2] += .08 * Math.sin(t * 12); p.a[0][1] += .05 * Math.sin(t * 7);
    return { vis: true, p, f: { mouth: "smile", eyes: "open" } };
  }
  if (s === 7) {
    let p = idle(withArms(SIT(DESK.x, DESK.z, 0), [[.95, .55, .55], [.3, 2.4 + .3 * Math.sin(t * 9), .5]]), t, 4);
    return { vis: true, p, f: { mouth: "grin", eyes: t > C.examk ? "happy" : "open" } };
  }
  return { vis: false };
}
const OWLB = { x: .5, y: .755, z: .05, ry: -.45 };
function owlAt(t, s) {
  const breathe = .015 * Math.sin(t * 2.2);
  if (s <= 2 || s === 4 || s === 5 || s === 7) {
    let p = opose({ ...OWLB, hop: breathe, hy: .1 * Math.sin(t * .7) });
    let f = { eyes: "open" };
    if (s === 0 && t > C.l[1] - .1 && t < C.l[1] + .8) { p = { ...p, hr: .2, hp: .1 }; f = { eyes: "open" }; }
    if (s === 0 && t > C.l[3] - .1) { p = { ...p, w: [.9 + .1 * Math.sin(t * 6), .1], hp: -.05 }; f = { eyes: "happy" }; }
    if (s === 1) { p = { ...p, w: [1.2, .2], hy: .4 }; f = { eyes: "open" }; }
    if (s === 2) { p = { ...p, w: [1.0 + .2 * Math.sin(t * 5), 1.0 + .2 * Math.sin(t * 5 + 1)], hop: breathe + .02 * Math.abs(Math.sin(t * 6)) }; f = { eyes: "happy" }; }
    if (s === 4) { p = { ...p, hy: .35, w: [.6, .1] }; f = { eyes: t > C.ninety ? "happy" : "open" }; if (t > C.ninety) p.hop = .05 * Math.abs(Math.sin(t * 9)); }
    if (s === 5) {
      if (t < C.l[14]) { p = { ...p, hy: .35, hp: .15 }; f = { eyes: t > C.bag ? "wide" : "open" }; }
      else if (t < C.l[15] + .1) { p = { ...p, hy: .5 * Math.sin((t - C.no) * 12) * bump(t, C.no - .05, C.no + .9, .1), w: [1.4, 1.4] }; f = { eyes: "closed" }; }
      else { p = { ...p, hy: .3, w: [1.4, 1.4] }; f = { eyes: "closed" }; }
    }
    if (s === 7) { p = { ...p, w: [.2, 1.6 + .4 * Math.sin(t * 9)], hop: breathe + .03 * Math.abs(Math.sin(t * 5)) }; f = { eyes: t > C.examk && t < C.examk + 1.2 ? "closed" : "happy" }; }
    return { vis: true, p, f, phones: false };
  }
  if (s === 3) return { vis: true, p: opose({ x: 20.78, y: .51, z: -.25, ry: -.2, s: .8, hop: .015 * Math.abs(Math.sin(t * 5)), hy: .15 * Math.sin(t * 2.5) }), f: { eyes: "happy" }, phones: true };
  if (s === 6) return { vis: t > C.every - .5, p: opose({ x: 40 - 4.85, y: .95, z: -2.45, ry: Math.PI / 2, w: [.2, 1.5 + .4 * Math.sin(t * 9)] }), f: { eyes: "happy" }, phones: false };
  return { vis: false };
}
function extraAt(P, t, s, k) {
  if (s !== 6) return { vis: false };
  const [x, z] = [[-1.6, -4.2], [1.6, -4.2], [1.6, -2.9]][k];
  const p = idle(withArms(SIT(40 + x, z + .55, Math.PI), [[.85, .05, 1.0 + .08 * Math.sin(t * 11 + k)], [.6, .1, .8]], { hp: .4 }), t, k + 5);
  return { vis: true, p, f: { mouth: "flat", eyes: "half" } };
}

// ---------------------------------------------------------------- camera shots
const SH = { p: new THREE.Vector3(), l: new THREE.Vector3(), fov: 40, ap: null };
const fixed = (p, l, fov = 40, ap = null) => () => { SH.p.set(...p); SH.l.set(...l); SH.fov = fov; SH.ap = ap; return SH; };
const move = (a, b, p0, p1, l0, l1, f0, f1, ap = null) => (t) => { const u = ss(t, a, b); SH.p.set(lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(p0[2], p1[2], u)); SH.l.set(lerp(l0[0], l1[0], u), lerp(l0[1], l1[1], u), lerp(l0[2], l1[2], u)); SH.fov = lerp(f0, f1, u); SH.ap = ap; return SH; };
const HEADW = { you: new THREE.Vector3(), owl: new THREE.Vector3() }, HEADM = { you: new THREE.Matrix4(), owl: new THREE.Matrix4() };
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
  { t: 0, tr: 0, f: faceShot("you", 3.1, .05, .25, 30, -.12, .4, [0, F[0].b]) },
  { t: F[1].a, tr: 0, f: faceShot("owl", 2.0, .05, -.15, 30, -.04) },
  { t: C.and3 - .3, tr: 0, f: move(C.and3 - .3, F[2].a, [-.25, 1.5, 3.4], [-.2, 1.45, 3.1], [.02, 1.25, -.2], [.02, 1.25, -.2], 38, 37) },
  { t: F[2].a, tr: 0, f: faceShot("owl", 1.9, .05, .1, 30, -.04) },
  { t: C.all - .3, tr: 0, f: fixed([.3, 1.48, 3.1], [.18, 1.24, -.2], 38) },
  // step 1: the pages fly into the laptop
  { t: CU[0], tr: 0, f: move(CU[0], CU[1], [-1.0, 1.6, 2.8], [-.85, 1.55, 2.5], [-.12, 1.22, -.1], [-.12, 1.22, -.1], 38, 37) },
  // step 2: the podcast
  { t: CU[1], tr: 0, f: move(CU[1], F[3].a, [.7, 1.55, 3.0], [.6, 1.52, 2.7], [.0, 1.28, -.2], [.0, 1.28, -.2], 38, 37) },
  { t: F[3].a, tr: 0, f: faceShot("you", 3.2, .05, -.2, 30, .14) },
  // the bus
  { t: CU[2], tr: 0, f: move(CU[2], CU[3], [20.3, 1.45, 3.2], [20.35, 1.42, 2.8], [20.55, 1.28, -.3], [20.55, 1.28, -.3], 36, 34) },
  // step 3 + 4: flashcards, the test, chapter 7, 91
  { t: CU[3], tr: 0, f: move(CU[3], C.test - .1, [0, 1.55, 3.6], [0, 1.52, 3.3], [0, 1.33, -.4], [0, 1.33, -.4], 40, 39) },
  { t: C.test - .1, tr: 0, f: fixed([.12, 1.5, .5], [0, .8, -.32], 34) },
  { t: F[4].a, tr: 0, f: faceShot("you", 3.2, .1, .2, 30, .14) },
  { t: C.step4 - .25, tr: 0, f: move(C.step4 - .25, C.ninety - .3, [.5, 1.55, 3.3], [.4, 1.52, 3.0], [0, 1.3, -.4], [0, 1.3, -.4], 38, 37) },
  { t: C.ninety - .3, tr: 0, f: fixed([0, 1.45, 3.0], [0, 1.32, -.5], 38) },
  // the bag
  { t: CU[4], tr: 0, f: move(CU[4], F[5].a, [.3, 1.5, 3.2], [.28, 1.47, 2.9], [.22, 1.2, -.2], [.22, 1.2, -.2], 38, 36) },
  { t: F[5].a, tr: 0, f: faceShot("owl", 1.8, .03, .05, 30, -.04) },
  { t: C.please - .25, tr: 0, f: fixed([-.4, 1.3, 2.1], [-.04, 1.0, -.58], 30) },
  // exam day
  { t: CU[5], tr: 0, f: move(CU[5], C.every - .3, [40.95, 1.6, -5.4], [40.8, 1.55, -5.3], [40, 1.0, -3.75], [40, 1.0, -3.75], 52, 48) },
  { t: C.every - .3, tr: 0, f: move(C.every - .3, CU[6], [40 - 1.3, 1.35, -3.0], [40 - 1.6, 1.35, -2.9], [40 - 4.7, 1.3, -2.45], [40 - 4.7, 1.3, -2.45], 34, 32) },
  // close
  { t: CU[6], tr: 0, f: move(CU[6], DUR, [.1, 1.3, 3.8], [.1, 1.3, 3.5], [.18, 1.75, -.3], [.18, 1.75, -.3], 38, 38) },
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
  dusk: { sky: "dusk", fog: 0x3A2E4A, hs: 0xC9B4FF, hg: 0x3A2E4A, hi: .8, sun: 0xFFA868, si: 1.3, sp: [1.5, 3, -6], lamp: .7, scr: .5, win: .9, bg: 0x2B2440 },
  night: { sky: "night", fog: 0x15132A, hs: 0x7D79C9, hg: 0x1E1A2E, hi: .45, sun: 0x9FB4FF, si: .35, sp: [2, 4, -6], lamp: 1.6, scr: 1.0, win: 1.3, bg: 0x15132A },
  bus: { sky: "night", fog: 0x15132A, hs: 0x9C95D6, hg: 0x2E2A3A, hi: .55, sun: 0x9FB4FF, si: .3, sp: [4, 5, 2], lamp: 0, scr: 0, win: 1.3, bg: 0x15132A },
  hall: { sky: "morning", fog: 0xF2E6D6, hs: 0xFFF6EA, hg: 0xC9B49A, hi: 1.0, sun: 0xFFF0D8, si: 2.4, sp: [-8, 6, 2], lamp: 0, scr: 0, win: 0, bg: 0xF2E6D6 },
  morning: { sky: "morning", fog: 0xE9DCF0, hs: 0xFFF1E6, hg: 0x8A6A58, hi: 1.0, sun: 0xFFD9A8, si: 1.8, sp: [1.5, 3, -6], lamp: 0, scr: .2, win: 0, bg: 0xE9DCF0 },
};
const LOOK_OF = ["dusk", "dusk", "dusk", "bus", "night", "night", "hall", "morning"];

// ---------------------------------------------------------------- render at time t
const PP = new THREE.Vector3(), A0 = new THREE.Vector3(), A1 = new THREE.Vector3(), A2 = new THREE.Vector3();
const SCREEN = new THREE.Vector3();
function handsMid(P, out) { P.hand[0].getWorldPosition(A0); P.hand[1].getWorldPosition(A1); return out.lerpVectors(A0, A1, .5); }
const facing = (m, q) => m.quaternion.copy(q);
function renderAt(t) {
  NOW = t;
  const s = sceneOf(t), Lk = LOOKS[LOOK_OF[s]];
  scene.background = tmpC.set(Lk.bg).clone(); scene.fog.color.set(Lk.fog);
  if (SKY[Lk.sky]) setMap(skyM, SKY[Lk.sky]);
  hemi.color.set(Lk.hs); hemi.groundColor.set(Lk.hg); hemi.intensity = Lk.hi;
  sun.color.set(Lk.sun); sun.intensity = Lk.si;
  for (const tw of towers) tw.material.emissiveIntensity = Lk.win;
  const deskSet = s <= 2 || s === 4 || s === 5 || s === 7;
  const close62 = s === 4 && t >= FOC[4].a && t < C.step4 - .25;
  lampL.intensity = deskSet ? Lk.lamp * (close62 ? .45 : 1) : 0; shadeM.emissiveIntensity = deskSet && Lk.lamp > 0 ? .5 : .05; bulb.visible = Lk.lamp > 0;
  screenL.position.copy(SCREEN).add(V.set(0, .05, -.25)); screenL.intensity = deskSet ? Lk.scr + (s === 1 || s === 2 ? .8 : 0) : 0;
  busL1.position.set(20.2, 1.9, -.9); busL2.position.set(20.1, 1.6, .9); busL1.intensity = busL2.intensity = s === 3 ? 1.6 : 0;
  hallL.position.set(40, 3.0, -2.5); hallL.intensity = s === 6 ? 1.0 : 0;
  rimL.position.set(.6, 1.6, -1.2); rimL.intensity = deskSet ? (Lk === LOOKS.morning ? .6 : 1.0) : 0;
  lapScr.getWorldPosition(SCREEN);
  if (TEX.lapNotes) setMap(lapScrM, TEX[s === 1 ? "lapUpload" : s === 2 ? "lapAudio" : s === 4 ? "lapCards" : "lapNotes"]);

  // characters
  const ys = youAt(t, s); YOU.root.visible = ys.vis; if (ys.vis) { applyPose(YOU, ys.p); setFace(YOU, ys.f); }
  phonesK.visible = !!ys.phones;
  [EX1, EX2, EX3].forEach((P, k) => { const st = extraAt(P, t, s, k); P.root.visible = st.vis; if (st.vis) { applyPose(P, st.p); setFace(P, st.f); } });
  const os = owlAt(t, s); OWL.root.visible = os.vis; if (os.vis) { applyOwl(os.p); setOwl(os.f); } phonesO.visible = !!os.phones;
  OWL.tassel.rotation.z = .2 * Math.sin(t * 3);
  scene.updateMatrixWorld(true);
  YOU.face.updateMatrixWorld(); HEADM.you.copy(YOU.face.matrixWorld); HEADW.you.setFromMatrixPosition(YOU.face.matrixWorld);
  HEADM.owl.copy(OWL.head.matrixWorld); HEADW.owl.set(0, .06, 0).applyMatrix4(OWL.head.matrixWorld);
  owlL.position.copy(HEADW.owl).add(V.set(0, 0, .25)); owlL.intensity = os.vis ? .08 : 0;

  // the notes: drop in, then fly into the laptop page by page
  const h0 = .32, left = 1 - ss(t, C.drop - .2, C.everything + .7);
  notesG.visible = (s === 0 && t > C.and3 - .25) || (s === 1 && left > .01);
  if (notesG.visible) {
    const fall = s === 0 ? 1 - ss(t, C.and3 - .25, C.three) : 0;
    const bounce = s === 0 ? .03 * Math.sin(Math.min(1, ramp(t, C.three, C.three + .35)) * Math.PI) : 0;
    const hh = h0 * (s === 1 ? left : 1);
    stack.scale.y = Math.max(.001, hh); stack.position.set(0, 0, 0); stackTop.position.set(0, hh + .002, 0); stackTop.rotation.z = (hash(5 * 7) - .5) * .18;
    notesG.position.set(NOTES.x, NOTES.y + fall * 1.2 + bounce, NOTES.z); notesG.rotation.set(0, .15 + fall * .5, fall * .3);
  }
  hideAll(pageM, PAGE_N);
  if (s === 1) for (let k = 0; k < PAGE_N; k++) {
    const a = C.drop - .2 + k * (C.everything + .7 - C.drop) / PAGE_N, u = ramp(t, a, a + .7); if (u <= 0 || u >= 1) continue;
    A0.set(NOTES.x, NOTES.y + h0 * (1 - k / PAGE_N), NOTES.z); A2.copy(SCREEN); A1.lerpVectors(A0, A2, .5).add(V.set(0, .08 + hash(k) * .08, .32));
    bez(A0, A1, A2, u, PP); Q.setFromEuler(new THREE.Euler(-1.2 + u * 1.3 + hash(k) * .5, u * 3 + k, hash(k * 3) * .6)); M4.compose(PP, Q, S.setScalar(1 - .6 * u)); pageM.setMatrixAt(k, M4);
  }
  // the podcast: a glowing waveform over the laptop; on the bus, over the phone
  hideAll(barM, BAR_N);
  if (s === 2 && t > C.podcast - .3) {
    const base = s === 2 ? A0.set(-.5, 1.12, .05) : (PP.copy(phoneK.position).add(V.set(0, .14, .05)), A0.copy(PP));
    const sc = s === 2 ? 1 : .45, grow = s === 2 ? ss(t, C.podcast - .3, C.podcast + .2) : 1;
    for (let k = 0; k < BAR_N; k++) { const hgt = (.04 + .16 * Math.abs(Math.sin(t * 7 + k * .8) * Math.sin(t * 2.3 + k * .3))) * grow * sc; M4.compose(V.set(A0.x + (k - (BAR_N - 1) / 2) * .024 * sc, A0.y, A0.z), Q.identity(), S.set(sc, Math.max(.001, hgt), sc)); barM.setMatrixAt(k, M4); }
  }
  // flashcards: out of the laptop into an arc around her; chapter 7 comes forward
  hideAll(cardM, CARD_N);
  if (s === 4) for (let k = 0; k < CARD_N; k++) {
    const a = C.flashcards - .2 + k * .03, u = ss(t, a, a + .6); if (u <= 0) continue;
    const ang = -1.25 + 2.5 * (k / (CARD_N - 1)), ring = k % 2 ? .95 : .78;
    A2.set(Math.sin(ang) * (ring + .12), 1.22 + Math.cos(ang) * .38 + (k % 3) * .06, -1.0 + Math.cos(ang) * .1);
    const ch7 = k % 8 === 3, fwd = ch7 ? ss(t, C.seven - .3 + (k % 5) * .05, C.seven + .3) : 0, fade = !ch7 ? ss(t, C.seven - .2, C.seven + .4) * (1 - ss(t, C.ninety - .2, C.ninety + .2)) : 0;
    bez(A0.copy(SCREEN), A1.set(-.2, 2.0, -.6), A2, u, PP);
    if (fwd > 0) PP.lerp(A1.set(-.15 + (k % 5) * .07, .64 + (k % 5) * .006, .14), fwd);
    Q.setFromEuler(new THREE.Euler(fwd * -1.5, -ang * .4 * (1 - fwd), (hash(k) - .5) * .3 * (1 - fwd) + Math.sin(t * 1.5 + k) * .04));
    M4.compose(PP, Q, S.setScalar((1 - .65 * fade) * (ch7 && fwd > 0 ? 1.15 : 1))); cardM.setMatrixAt(k, M4);
    cardM.setColorAt(k, tmpC.set(ch7 && t > C.seven - .3 ? 0xFFB09C : [0xFFFDF8, 0xEDE7FB, 0xF7E3A6, 0xFFE0D6][k % 4]));
  }
  cardM.instanceColor.needsUpdate = true;
  hideAll(confM, CONF_N);
  const conf = (t0, o, n) => { for (let k = 0; k < n; k++) { const u = ramp(t, t0 + hash(k * 9) * .2, t0 + 2.2); if (u <= 0 || u >= 1) continue; const a = hash(k) * Math.PI * 2, sp = .5 + hash(k * 3) * .6; PP.set(o.x + Math.cos(a) * sp * u, o.y + (1.6 + hash(k * 7)) * u - 2.4 * u * u, o.z + Math.sin(a) * sp * u * .6); Q.setFromEuler(new THREE.Euler(t * 6 + k, t * 4 + k * 2, 0)); M4.compose(PP, Q, S.setScalar(1)); confM.setMatrixAt(k, M4); } };
  if (s === 4 && t > C.ninety - .1) conf(C.ninety - .1, A0.set(0, 1.4, -.4), CONF_N);
  if (s === 7 && t > CU[6] + .2) conf(CU[6] + .2, A0.set(.1, 1.5, -.3), 50);
  // things in her hands
  testPaper.visible = (s === 4 && t > C.test - .15) || s === 7;
  if (testPaper.visible) {
    if (TEX.test62) setMap(testPaper.material, TEX[(s === 4 && t < C.ninety - .1) ? "test62" : "test91"]);
    if (s === 4) { handsMid(YOU, PP); testPaper.position.copy(PP).add(V.set(0, -.03, .07)); testPaper.rotation.set(-1.0, 0, 0); }
    else { YOU.hand[0].getWorldPosition(PP); testPaper.position.copy(PP).add(V.set(-.1, .1, .05)); testPaper.rotation.set(-.15, .35, .12); }
  }
  bag.visible = s === 5 && t > C.small - .35;
  if (bag.visible) { handsMid(YOU, PP); bag.scale.setScalar(.6); bag.position.copy(PP).add(V.set(.12, -.08, .14)); bag.rotation.set(-.2, -.5, 0); flap.rotation.x = -1.6; }
  phoneK.visible = s === 3;
  if (phoneK.visible) { handsMid(YOU, PP); phoneK.position.copy(PP).add(V.set(0, .06, .02)); phoneK.rotation.set(-.6, 0, 0); }
  pencil.visible = s === 6;
  if (pencil.visible) { YOU.hand[0].getWorldPosition(PP); pencil.position.copy(PP).add(V.set(0, .02, -.03)); pencil.rotation.set(-.9, 0, .3); examPaper.position.set(0, .623, -4.12); }
  examPaper.visible = s === 6; resultPaper.visible = false;
  // the bus world rolls past
  passing.forEach((m, k) => { const zz = ((k * 1.7 - t * 5.5) % 30 + 30) % 30 - 15; m.position.set(2.6 + (k % 3) * 1.1, .4 + (k % 4) * .35, zz); });

  // the camera
  const fov = camAt(t);
  camera.position.copy(CAMP);
  camera.position.x += Math.sin(t * .37) * .006; camera.position.y += Math.sin(t * .29 + 1) * .005;
  camera.fov = fov;
  const look = CAML.clone();
  const cv = window.EXAM_COVER;
  if (cv) { camera.position.set(...cv.cam); camera.fov = cv.fov; look.set(...cv.look); }
  camera.updateProjectionMatrix(); camera.lookAt(look); camera.updateMatrixWorld();

  // grade
  let fl = 0; for (const ct of SHOT_STARTS) if (ct > 0) fl += .12 * Math.exp(-(((t - ct) / .06) ** 2)) * (t >= ct ? 1 : 0);
  for (const ct of CU) fl += .35 * Math.exp(-(((t - ct) / .07) ** 2)) * (t >= ct ? 1 : .2);
  fl += .3 * pulse(t, C.ninety, .08);
  let fb = 0; for (const f of FOC) fb = Math.max(fb, bump(t, f.a, f.b, .2));
  grade.uniforms.uFlash.value = cv ? 0 : fl;
  grade.uniforms.uSat.value = 1.05;
  grade.uniforms.uCool.value = s === 3 || s === 4 || s === 5 ? .2 : 0;
  grade.uniforms.uWarm.value = s === 0 || s === 1 || s === 2 ? .2 : s === 6 || s === 7 ? .15 : 0;
  grade.uniforms.uBars.value = 0; grade.uniforms.uScan.value = 0; grade.uniforms.uCon.value = .04;
  grade.uniforms.uCA.value = .0008;
  grade.uniforms.uTime.value = t;
  grade.uniforms.uVig.value = .3 + .25 * fb;
  faceKey.position.copy(camera.position).add(V.set(.25, .35, 0)); faceKey.intensity = deskSet ? (s >= 4 ? 1.7 : 1.3) : s === 3 ? 1.4 : .6;
  const fd = camera.position.distanceTo(look);
  cocPass.uniforms.uF.value = cv?.focus ?? fd;
  cocPass.uniforms.uAp.value = cv ? (cv.ap ?? .3) : (CAMAP ?? clamp(1.6 / fd, .15, .8));
  dofPass.uniforms.uMaxR.value = 22;
  const ext = clamp(fd * 1.1, 2.5, 10);
  sun.target.position.copy(look); sun.position.copy(look).add(V2.set(...Lk.sp).normalize().multiplyScalar(14));
  Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext, bottom: -ext, near: .5, far: 40 });
  sun.shadow.camera.updateProjectionMatrix();
  scene.fog.near = 12; scene.fog.far = 45;
  for (const m of [pageM, cardM, confM, barM]) m.instanceMatrix.needsUpdate = true;
  renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); renderer.setRenderTarget(null);
  composer.render();
}

// ---------------------------------------------------------------- textures (after the fonts), then the first frame
function buildTextures() {
  const grad = (stops, stars = false) => pix(64, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); if (stars) for (let k = 0; k < 40; k++) { g.fillStyle = "rgba(255,255,255,.8)"; g.fillRect(Math.floor(hash(k) * w), Math.floor(hash(k * 3) * h * .55), 1, 1); } });
  SKY.dusk = grad([[0, "#2B2350"], [.45, "#7A4F8E"], [.72, "#E9849A"], [1, "#F7B27A"]]);
  SKY.night = grad([[0, "#0B0A1E"], [.6, "#1E1A44"], [1, "#3A2E6A"]], true);
  SKY.morning = grad([[0, "#8FC4F0"], [.6, "#CFE4F5"], [1, "#FBE6C8"]]); TEX.skyMorning = SKY.morning;
  TEX.towerWin = pix(64, 128, (g, w, h) => { g.fillStyle = "#000"; g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = 0; j < 10; j++) if (hash(i * 13 + j * 7) > .45) { g.fillStyle = hash(i + j) > .5 ? "#FFD08A" : "#FFE9C4"; g.fillRect(6 + i * 15, 6 + j * 12, 8, 7); } });
  const lap = (draw) => pix(420, 270, (g, w, h) => { g.fillStyle = "#F7F3FF"; g.fillRect(0, 0, w, h); g.fillStyle = "#6B5BD6"; g.fillRect(0, 0, w, 34); g.fillStyle = "#fff"; g.font = FONT(800, 18); g.fillText("NotebookLM", 14, 23); draw(g, w, h); });
  TEX.lapNotes = lap((g, w) => { g.fillStyle = "#1E1B18"; g.font = FONT(800, 22); g.fillText("Biology final", 20, 74); g.fillStyle = "#DCD3EE"; for (let k = 0; k < 6; k++) g.fillRect(20, 96 + k * 26, w - 40 - (k * 30) % 90, 10); });
  TEX.lapUpload = lap((g, w) => { ["Lecture notes.pdf", "Slides 1-12.pdf", "Notebook photos"].forEach((n, k) => { g.fillStyle = "#EDE7FB"; rr(g, 16, 50 + k * 56, w - 32, 46, 10); g.fill(); g.fillStyle = "#6B5BD6"; g.fillRect(28, 60 + k * 56, 18, 24); g.fillStyle = "#1E1B18"; g.font = FONT(800, 18); g.fillText(n, 58, 79 + k * 56); g.fillStyle = "#3FA372"; g.font = FONT(800, 22); g.fillText("✓", w - 46, 81 + k * 56); }); g.fillStyle = "#1E1B18"; g.font = MONO(18); g.fillText("300 pages added", 20, 250); });
  TEX.lapAudio = lap((g, w) => { g.fillStyle = "#1E1B18"; g.font = FONT(800, 22); g.fillText("Audio Overview", 20, 74); g.fillStyle = "#6B5BD6"; g.beginPath(); g.moveTo(30, 110); g.lineTo(30, 160); g.lineTo(72, 135); g.fill(); for (let k = 0; k < 26; k++) { const hh = 10 + 50 * Math.abs(Math.sin(k * 1.3)); g.fillRect(96 + k * 11, 135 - hh / 2, 6, hh); } g.fillStyle = "#5b5650"; g.font = MONO(16); g.fillText("Deep dive · 20 min", 20, 230); });
  TEX.lapCards = lap((g, w) => { for (let k = 0; k < 6; k++) { g.fillStyle = k === 3 ? "#FFB09C" : "#EDE7FB"; rr(g, 18 + (k % 3) * 132, 50 + Math.floor(k / 3) * 100, 120, 86, 10); g.fill(); } g.fillStyle = "#1E1B18"; g.font = MONO(16); g.fillText("50 flashcards · practice test", 20, 258); });
  TEX.noteTop = pix(256, 320, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.strokeStyle = "#B9CCE8"; g.lineWidth = 2; for (let y = 40; y < h; y += 22) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); } g.strokeStyle = "#3A3550"; g.lineWidth = 3; for (let k = 0; k < 10; k++) { g.beginPath(); let x = 20; g.moveTo(x, 36 + k * 22); while (x < w - 30 - (k * 37) % 80) { x += 8; g.lineTo(x, 36 + k * 22 + Math.sin(x * .7 + k) * 3); } g.stroke(); } g.fillStyle = "#E8735A"; g.font = FONT(800, 26); g.fillText("CH. 1-12", 20, 26); });
  const test = (score, good) => pix(260, 340, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#1E1B18"; g.font = FONT(800, 22); g.fillText("Practice test", 18, 36); g.fillStyle = "#E4D9C7"; for (let k = 0; k < 8; k++) g.fillRect(18, 60 + k * 26, w - 36 - (k * 40) % 90, 9); g.strokeStyle = good ? "#3FA372" : "#D9483B"; g.lineWidth = 7; g.beginPath(); g.arc(w / 2, 268, 56, 0, Math.PI * 2); g.stroke(); g.fillStyle = good ? "#3FA372" : "#D9483B"; g.font = FONT(800, 50); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(score, w / 2, 270); });
  TEX.test62 = test("62%", false); TEX.test91 = test("91%", true); TEX.result = TEX.test91;
  TEX.exam = pix(260, 340, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.fillRect(0, 0, w, h); g.fillStyle = "#1E1B18"; g.font = FONT(800, 22); g.fillText("FINAL EXAM", 18, 34); g.fillStyle = "#E4D9C7"; for (let k = 0; k < 10; k++) g.fillRect(18, 56 + k * 26, w - 36, 8); g.strokeStyle = "#3A3550"; g.lineWidth = 2.5; for (let k = 0; k < 5; k++) { g.beginPath(); let x = 20; g.moveTo(x, 68 + k * 52); while (x < w - 40) { x += 7; g.lineTo(x, 68 + k * 52 + Math.sin(x * .6 + k) * 2.5); } g.stroke(); } });
  TEX.board = pix(720, 240, (g, w, h) => { g.fillStyle = "#2F4A3E"; g.fillRect(0, 0, w, h); g.fillStyle = "#F4EDE2"; g.font = FONT(800, 64); g.textAlign = "center"; g.fillText("FINAL EXAM", w / 2, 100); g.font = FONT(700, 40); g.fillText("Biology · Chapters 1-12", w / 2, 170); });
  TEX.clock = pix(128, 128, (g, w, h) => { g.fillStyle = "#FFFDF8"; g.beginPath(); g.arc(64, 64, 62, 0, Math.PI * 2); g.fill(); g.strokeStyle = "#1E1B18"; g.lineWidth = 6; g.stroke(); g.lineWidth = 5; g.beginPath(); g.moveTo(64, 64); g.lineTo(64, 24); g.moveTo(64, 64); g.lineTo(92, 70); g.stroke(); });
  TEX.phoneWave = pix(124, 250, (g, w, h) => { g.fillStyle = "#14121F"; g.fillRect(0, 0, w, h); g.fillStyle = "#6B5BD6"; rr(g, 10, 70, w - 20, 110, 14); g.fill(); g.fillStyle = "#fff"; for (let k = 0; k < 12; k++) { const hh = 10 + 40 * Math.abs(Math.sin(k * 1.5)); g.fillRect(18 + k * 7.5, 125 - hh / 2, 4, hh); } g.font = FONT(800, 13); g.fillText("Biology · 20 min", 12, 210); });
  for (const [m, key, prop] of LATE) { if (TEX[key]) { m[prop || "map"] = TEX[key]; m.needsUpdate = true; } }
}

const ready = (async () => {
  try { await Promise.all([document.fonts.load("800 40px Manrope"), document.fonts.load("700 30px JBMono")]); } catch (e) { /* fall back */ }
  buildTextures();
  scene.traverse((o) => { if (o.isInstancedMesh || o.isMesh) o.frustumCulled = false; });
  renderer.compile(scene, camera);
  renderAt(window.EXAM_COVER ? window.EXAM_COVER.t : (window.__hfThreeTime || 0));
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["exam"] = ready;
window.addEventListener("hf-seek", (e) => renderAt(window.EXAM_COVER ? window.EXAM_COVER.t : e.detail.time));
window.EXAM_DEBUG = { renderAt, HEADW };
