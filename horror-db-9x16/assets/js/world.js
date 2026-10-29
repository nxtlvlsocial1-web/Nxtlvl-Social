// 03:07 AM (horror short): the 3D world. Everything is a pure function of time t (seconds), rendered on HyperFrames'
// hf-seek. A developer alone on a dark office floor drops the production database; Claude answers from inside his
// monitor. The ceiling lights die row by row, the server room's LEDs bleed from green to red, the phone fills with
// 900 users; in the blackout two coral eyes open in the screen, and the snapshot Claude kept floats out of it. The
// restore brings the lights back, row by row; "I've revoked your production access" takes them away again.
// Shots are CCTV angles and close-ups, hard cuts; cue times come from the dialogue (window.HR_T, build/generate.py).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const T = window.HR_T;
const L = T.l, E = T.e;
const W = 1080, H = 1920;
const SRV_X = 40;                                    // the server room sits off to the side

const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x020306);
scene.fog = new THREE.FogExp2(0x030509, .085);
const camera = new THREE.PerspectiveCamera(40, W / H, .03, 120);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = .05;

// ---------------------------------------------------------------- post: bloom, then a CCTV grade (desaturation, grain, vignette, chroma, roll)
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .7, .55, .72);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uGrain: { value: .07 }, uVig: { value: .95 }, uChroma: { value: .3 },
    uSat: { value: .7 }, uTint: { value: new THREE.Vector3(.92, 1.0, 1.08) }, uRoll: { value: 0 }, uTear: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uGrain, uVig, uChroma, uSat, uRoll, uTear; uniform vec3 uTint; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 uv = vUv;
      float band = step(.5, fract(uv.y * 3. + uTime * .7)) * step(fract(uv.y * 3. + uTime * .7), .53);
      uv.x += (h(vec2(floor(uv.y * 240.), floor(uTime * 30.))) - .5) * .03 * uTear + band * .004 * uRoll;
      vec2 c = uv - .5; vec2 off = c * uChroma * .02;
      vec3 col = vec3(texture2D(tDiffuse, uv + off).r, texture2D(tDiffuse, uv).g, texture2D(tDiffuse, uv - off).b);
      float l = dot(col, vec3(.299, .587, .114));
      col = mix(vec3(l), col, uSat) * uTint;
      col += (h(floor(uv * vec2(540., 960.)) + fract(uTime * 7.13) * 97.) - .5) * uGrain;
      col += band * .03 * uRoll;
      vec2 v = c * vec2(1., .72);
      col *= 1. - uVig * dot(v, v) * 1.6;
      gl_FragColor = vec4(col, 1.);
    }`,
});
composer.addPass(grade);

// ---------------------------------------------------------------- helpers
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const easeIO = (k) => (k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const easeOut = (k) => 1 - Math.pow(1 - k, 3);
const easeIn = (k) => k * k * k;
const win = (t, a, b) => clamp((t - a) / (b - a));
const pulse = (t, at, up = .08, down = .35) => (t < at ? 0 : t < at + up ? (t - at) / up : Math.max(0, 1 - (t - at - up) / down));
const between = (t, a, b) => t >= a && t < b;
const rb = (w, h, d, r = .06, seg = 3) => new RoundedBoxGeometry(w, h, d, seg, Math.min(r, w / 2 - .001, h / 2 - .001, d / 2 - .001));
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .7, metalness: 0, ...o });
const glow = (color, k = 3, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(k), toneMapped: false, ...o });
function mesh(geo, m, cast = true, recv = true) { const x = new THREE.Mesh(geo, m); x.castShadow = cast; x.receiveShadow = recv; return x; }
function hash(i) { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
function grp(parent, x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); if (parent) parent.add(g); return g; }
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const at = (o, x, y, z) => { o.position.set(x, y, z); return o; };
const lerpV = (a, b, k) => a.map((x, i) => lerp(x, b[i], k));
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); draw(g, w, h);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8; return tx;
}
function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
const glowTex = canvasTex(128, 128, (g, w) => {
  const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(.35, "rgba(255,255,255,.45)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr; g.fillRect(0, 0, w, w);
});
glowTex.colorSpace = THREE.NoColorSpace;
const add = (c, k = 1, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), transparent: true, depthWrite: false,
  blending: THREE.AdditiveBlending, toneMapped: false, ...o });
function halo(size, color, k = .4) { return new THREE.Mesh(new THREE.PlaneGeometry(size, size), add(color, k, { map: glowTex })); }
function write(g, s, x, y, size, o = {}) {
  g.font = `${o.i ? "italic " : ""}${o.w || 700} ${size}px ${o.f || "JBMono"}`; g.fillStyle = o.c || "#d8e4ec"; g.textAlign = o.a || "left"; g.textBaseline = "middle";
  g.fillText(s, x, y, o.max);
}
const tM = new THREE.Matrix4(), tP = new THREE.Vector3(), tQ = new THREE.Quaternion(), tS = new THREE.Vector3(), tC = new THREE.Color();

const CORAL = 0xff6a4a, CORAL_L = 0xffa080, RED = 0xff2a2a, COLD = 0x9fc6ff, GREEN = 0x3dff8a;

// ---------------------------------------------------------------- lights: almost nothing; the screen, the ceiling rows, the racks
const hemi = new THREE.HemisphereLight(0x3a4a66, 0x050608, .05); scene.add(hemi);
const screenSpot = new THREE.SpotLight(COLD, 8, 7, 1.0, .7, 1.4);              // the monitor lighting his face and throwing his shadow
screenSpot.castShadow = true; screenSpot.shadow.mapSize.set(1024, 1024); screenSpot.shadow.bias = -.0005;
screenSpot.position.set(0, 1.2, -.2); screenSpot.target.position.set(0, 1.25, 2); scene.add(screenSpot, screenSpot.target);
const screenFill = new THREE.PointLight(COLD, 1.2, 3.5, 1.6); screenFill.position.set(0, 1.25, .1); scene.add(screenFill);
const eyeLight = new THREE.PointLight(CORAL, 0, 3, 1.6); eyeLight.position.set(0, 1.25, .2); scene.add(eyeLight);
const phoneLight = new THREE.PointLight(0xdfe8ff, 0, 1.2, 1.8); scene.add(phoneLight);
const CEIL_Z = [3.0, .4, -2.2, -4.8];
const ceilLights = CEIL_Z.map((z) => { const l = new THREE.PointLight(0xdfe9ff, 0, 7, 1.4); l.position.set(0, 2.75, z); scene.add(l); return l; });
const srvLights = [0, -4, -8].map((z) => { const l = new THREE.PointLight(GREEN, 0, 5, 1.6); l.position.set(SRV_X, 2.2, z); scene.add(l); return l; });

// ---------------------------------------------------------------- the office floor
const office = grp(scene);
office.add(at(mesh(new THREE.PlaneGeometry(14, 16).rotateX(-Math.PI / 2), std(0x15171c, { roughness: .95 }), false, true), 0, 0, -1));
office.add(at(mesh(new THREE.PlaneGeometry(14, 16).rotateX(Math.PI / 2), std(0x0d0e12, { roughness: 1 }), false, false), 0, 3.0, -1));
const backWall = mesh(new THREE.PlaneGeometry(14, 3.2), std(0x101218, { roughness: .95 }), false, true); backWall.position.set(0, 1.6, -7.5); office.add(backWall);
// the window strip on the back wall: a night city, out of focus
const cityTex = canvasTex(1024, 256, (g, w, h) => {
  const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#03050c"); gr.addColorStop(1, "#0a1222"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 260; i++) { const x = hash(i) * w, y = h * .35 + hash(i + 7) * h * .6, r = 1 + hash(i + 3) * 4;
    g.fillStyle = `rgba(${[255, 200, 140][i % 3]},${[220, 180, 160][i % 3]},${[170, 255, 200][i % 3]},${.2 + hash(i + 5) * .6})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
});
const windowStrip = new THREE.Mesh(new THREE.PlaneGeometry(13, 1.6), new THREE.MeshBasicMaterial({ map: cityTex, toneMapped: false, color: new THREE.Color(.5, .5, .5) }));
windowStrip.position.set(0, 1.9, -7.48); office.add(windowStrip);
for (let k = -6; k <= 6; k += 1.3) office.add(at(mesh(new THREE.BoxGeometry(.06, 1.7, .05), std(0x07080a)), k, 1.9, -7.45));
// the ceiling light panels, four rows of three
const PANELS = [];
CEIL_Z.forEach((z, r) => [-2.6, 0, 2.6].forEach((x) => {
  const p = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .5).rotateX(Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }));
  p.position.set(x, 2.99, z); office.add(p); PANELS.push({ p, r });
}));
// desks: the others' dark monitors, rows of them
function desk(parent, x, z, withMonitor = true) {
  const g = grp(parent, x, 0, z);
  g.add(at(mesh(rb(1.4, .05, .75, .015, 2), std(0x1c1e24, { roughness: .5 })), 0, .76, 0));
  for (const [dx, dz] of [[-.65, -.32], [.65, -.32], [-.65, .32], [.65, .32]]) g.add(at(mesh(new THREE.CylinderGeometry(.02, .02, .74, 8), std(0x0c0d10, { metalness: .7, roughness: .4 })), dx, .37, dz));
  if (withMonitor) {
    g.add(at(mesh(rb(.72, .44, .035, .012, 2), std(0x0a0b0e, { roughness: .35 })), 0, 1.16, -.25));
    g.add(at(mesh(new THREE.CylinderGeometry(.02, .02, .28, 8), std(0x0a0b0e)), 0, .92, -.28));
    g.add(at(mesh(new THREE.BoxGeometry(.5, .015, .17), std(0x111216)), 0, .79, .08));
  }
  return g;
}
for (const z of [2.6, -.0, -2.6, -5.2]) for (const x of [-3.2, -1.6, 1.6, 3.2]) desk(office, x, z);
desk(office, 0, -2.6); desk(office, 0, -5.2); desk(office, 0, 2.6);
// HIS desk (desk 12): the live monitor, a keyboard, a mug, the phone
const myDesk = desk(office, 0, 0, false);
const MON = V(0, 1.2, -.25);
myDesk.add(at(mesh(rb(.8, .5, .04, .015, 2), std(0x08090b, { roughness: .3, metalness: .3 })), 0, 1.2, -.27));
myDesk.add(at(mesh(new THREE.CylinderGeometry(.022, .022, .3, 8), std(0x0a0b0e)), 0, .93, -.3));
const SCR = document.createElement("canvas"); SCR.width = 1024; SCR.height = 616;
const screenTex = new THREE.CanvasTexture(SCR); screenTex.colorSpace = THREE.SRGBColorSpace; screenTex.anisotropy = 8;
const screenM = new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false });
const screen = new THREE.Mesh(new THREE.PlaneGeometry(.76, .457), screenM); screen.position.set(0, 1.2, -.248); myDesk.add(screen);
const kb = mesh(rb(.46, .02, .15, .006, 2), std(0x16171c, { roughness: .5 })); kb.position.set(0, .795, .05); myDesk.add(kb);
const enterKey = mesh(rb(.04, .014, .03, .004, 2), std(0x2a2c33)); enterKey.position.set(.17, .808, .05); myDesk.add(enterKey);
const mug = grp(myDesk, -.48, .785, -.05);
mug.add(at(mesh(new THREE.CylinderGeometry(.04, .036, .1, 16), std(0xd8d2c8, { roughness: .5 })), 0, .05, 0));
const phoneG = grp(myDesk, .42, .79, .02); phoneG.rotation.y = -.35;
phoneG.add(mesh(rb(.085, .01, .17, .012, 2), std(0x0b0b0e, { roughness: .3 })));
const PCAN = document.createElement("canvas"); PCAN.width = 360; PCAN.height = 720;
const phoneTex = new THREE.CanvasTexture(PCAN); phoneTex.colorSpace = THREE.SRGBColorSpace;
const phoneScreen = new THREE.Mesh(new THREE.PlaneGeometry(.076, .158), new THREE.MeshBasicMaterial({ map: phoneTex, toneMapped: false }));
phoneScreen.rotation.x = -Math.PI / 2; phoneScreen.position.y = .0055; phoneG.add(phoneScreen);
// the eyes that open in the dark screen, and the snapshot that floats out of it
const eyes = [-1, 1].map((s) => {
  const e = new THREE.Mesh(new THREE.CapsuleGeometry(.018, .022, 6, 12), glow(CORAL, 3.2)); e.rotation.z = Math.PI / 2 * 0; e.position.set(s * .085, 1.23, -.243); myDesk.add(e);
  const h = halo(.32, CORAL, .0); h.position.set(s * .085, 1.23, -.24); myDesk.add(h);
  return { e, h };
});
const snapCard = new THREE.Group();
const snapFace = new THREE.Mesh(new THREE.PlaneGeometry(.5, .3), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false }));
snapCard.add(snapFace); const snapHalo = halo(1.4, CORAL, 0); snapHalo.position.z = -.02; snapCard.add(snapHalo);
scene.add(snapCard); snapCard.visible = false;

// ---------------------------------------------------------------- him (stylised, in a hoodie, at desk 12, facing the screen)
const SKIN = 0x9c6448, HOOD = 0x3b3f4a, PANTS = 0x1c1f2a, HAIR = 0x0c0a0b;
function human() {
  const root = grp(office, 0, 0, .78); root.rotation.y = Math.PI;
  const hips = grp(root, 0, .62, 0);
  const pantsMat = std(PANTS, { roughness: .8 }), hoodMat = std(HOOD, { roughness: .9 }), skinMat = std(SKIN, { roughness: .55 });
  hips.add(mesh(rb(.46, .22, .36, .1, 3), pantsMat));
  for (const s of [-1, 1]) {
    const hip = grp(hips, s * .12, -.02, .02); hip.rotation.set(-1.42, s * -.06, 0);
    hip.add(at(mesh(rb(.19, .46, .21, .09, 3), pantsMat), 0, -.2, 0));
    const knee = grp(hip, 0, -.43, 0); knee.rotation.x = 1.5;
    knee.add(at(mesh(rb(.165, .46, .175, .075, 3), pantsMat), 0, -.21, 0));
  }
  const spine = grp(hips, 0, .06, 0);
  spine.add(at(mesh(rb(.64, .6, .4, .17, 4), hoodMat), 0, .3, 0));
  const hoodRing = mesh(new THREE.TorusGeometry(.16, .065, 10, 24), hoodMat); hoodRing.position.set(0, .6, -.06); hoodRing.rotation.x = Math.PI / 2 - .5; spine.add(hoodRing);
  const neck = grp(spine, 0, .6, 0);
  neck.add(at(mesh(new THREE.CylinderGeometry(.065, .07, .12, 12), skinMat), 0, .03, 0));
  const head = grp(neck, 0, .07, .01);
  const skull = mesh(new THREE.SphereGeometry(.19, 28, 22), skinMat); skull.scale.set(.95, 1.08, 1); skull.position.y = .17; head.add(skull);
  const hair = mesh(new THREE.SphereGeometry(.2, 28, 16, 0, Math.PI * 2, 0, Math.PI * .52), std(HAIR, { roughness: .8 }));
  hair.scale.set(.98, 1.06, 1.04); hair.position.set(0, .2, -.02); hair.rotation.x = -.42; head.add(hair);
  for (let i = 0; i < 5; i++) { const tuft = mesh(new THREE.SphereGeometry(.05, 10, 8), std(HAIR, { roughness: .8 })); tuft.scale.set(1, .55, 1); tuft.position.set((i - 2) * .06, .335 - Math.abs(i - 2) * .012, .1); tuft.rotation.x = .4; head.add(tuft); }
  for (const s of [-1, 1]) { const ear = mesh(new THREE.SphereGeometry(.04, 10, 8), skinMat); ear.scale.set(.5, 1, .8); ear.position.set(s * .18, .16, 0); head.add(ear); }
  head.add(at(mesh(new THREE.SphereGeometry(.026, 10, 8), std(0x8c5438)), 0, .15, .19));
  const eyesH = [], brows = [];
  for (const s of [-1, 1]) {
    const ew = mesh(new THREE.SphereGeometry(.034, 14, 10), std(0xf2efe8, { roughness: .25 }), false); ew.scale.z = .6; ew.position.set(s * .068, .2, .165); head.add(ew);
    const pupil = mesh(new THREE.SphereGeometry(.017, 12, 8), std(0x120c0a, { roughness: .2 }), false); pupil.position.z = .026; ew.add(pupil);
    const lid = mesh(new THREE.SphereGeometry(.036, 14, 10, 0, Math.PI * 2, 0, Math.PI / 2), skinMat, false); lid.scale.z = .66; lid.rotation.x = -.6; ew.add(lid);
    eyesH.push({ ew, pupil, lid });
    const br = mesh(rb(.075, .02, .02, .008, 2), std(HAIR), false); br.position.set(s * .07, .258, .178); head.add(br); brows.push(br);
  }
  const mouthArc = mesh(new THREE.TorusGeometry(.042, .01, 8, 20, Math.PI), std(0x4a2620), false); mouthArc.position.set(0, .09, .176); head.add(mouthArc);
  const mouthO = mesh(new THREE.SphereGeometry(.04, 16, 10), std(0x220a09, { roughness: .6 }), false); mouthO.scale.set(1, .5, .35); mouthO.position.set(0, .085, .17); head.add(mouthO);
  const arms = [];
  for (const s of [-1, 1]) {
    const sh = grp(spine, s * .33, .5, 0);
    sh.add(at(mesh(rb(.16, .34, .16, .075, 3), hoodMat), 0, -.14, 0));
    const el = grp(sh, 0, -.3, 0);
    el.add(at(mesh(rb(.14, .3, .14, .065, 3), hoodMat), 0, -.13, 0));
    const hand = grp(el, 0, -.32, 0);
    hand.add(mesh(new THREE.SphereGeometry(.062, 14, 10), skinMat));
    arms.push({ sh, el, hand });
  }
  return { root, hips, spine, neck, head, eyes: eyesH, brows, mouthArc, mouthO, arms };
}
const hu = human();
// poses: s = spine lean, h = head, arms (shoulder x/y/z, elbow), face
const P = {
  type: { s: .28, hx: .12, hy: 0, a0: [-1.25, .1, .2, -1.1], a1: [-1.25, -.1, -.2, -1.1], brow: .1, smile: 0, open: 0, wide: 0, shut: 0, look: [0, -.2] },
  frozen: { s: .18, hx: .02, hy: 0, a0: [-1.05, .1, .25, -1.25], a1: [-1.05, -.1, -.25, -1.25], brow: 1, smile: -.6, open: .35, wide: 1, shut: 0, look: [0, .05] },
  hands: { s: .38, hx: .2, hy: 0, a0: [-2.3, .2, .45, -2.2], a1: [-2.3, -.2, -.45, -2.2], brow: -.9, smile: -.9, open: .2, wide: .3, shut: .3, look: [0, -.4] },
  phone: { s: .3, hx: .45, hy: -.35, a0: [-1.2, .1, .2, -1.1], a1: [-1.5, -.4, -.1, -1.6], brow: .8, smile: -.8, open: .3, wide: .8, shut: 0, look: [.3, -.8] },
  stare: { s: .12, hx: -.05, hy: 0, a0: [-.8, .1, .3, -.9], a1: [-.8, -.1, -.3, -.9], brow: 1, smile: -.2, open: .6, wide: 1, shut: 0, look: [0, .1] },
  relief: { s: -.25, hx: -.35, hy: .1, a0: [-2.9, .2, .6, -1.6], a1: [-2.9, -.2, -.6, -1.6], brow: .3, smile: .7, open: .15, wide: 0, shut: .85, look: [0, .3] },
  doom: { s: .1, hx: 0, hy: 0, a0: [-1.0, .1, .3, -1.0], a1: [-1.0, -.1, -.3, -1.0], brow: 1, smile: -1, open: .45, wide: 1, shut: 0, look: [0, .1] },
};
function mixP(a, b, k) { const o = {}; for (const key in a) o[key] = Array.isArray(a[key]) ? a[key].map((v, i) => lerp(v, b[key][i], k)) : lerp(a[key], b[key], k); return o; }
function poseAt(keys, t) {
  let prev = keys[0][1], cur = keys[0][1], k = 1;
  for (let i = 1; i < keys.length; i++) { if (t < keys[i][0]) break; prev = keys[i - 1][1]; cur = keys[i][1]; k = easeIO(clamp((t - keys[i][0]) / (keys[i][2] || .3))); }
  return mixP(prev, cur, k);
}
function animHuman(t) {
  const p = poseAt([[0, P.type], [T.enter + .05, P.frozen, .25], [L[2] - .2, P.hands, .5], [L[4] - .1, P.frozen, .3], [L[6] - .1, P.phone, .4],
    [L[7], P.frozen, .4], [L[9] - .1, P.stare, .2], [T.done, P.relief, .9], [T.revoked - .05, P.doom, .25]], t);
  const talk = T.who.reduce((a, w, i) => a + (w === "dev" && between(t, L[i], E[i]) ? 1 : 0), 0);
  const breath = Math.sin(t * (t < T.done ? 5.5 : 2)) * (t < T.done ? .02 : .012);
  hu.spine.rotation.set(p.s + breath, 0, 0);
  hu.head.rotation.set(p.hx + talk * .05 * Math.sin(t * 14), p.hy + (t < T.done ? Math.sin(t * 21) * .006 : 0), 0);
  hu.arms[0].sh.rotation.set(p.a0[0], p.a0[1], p.a0[2]); hu.arms[0].el.rotation.set(p.a0[3], 0, 0);
  hu.arms[1].sh.rotation.set(p.a1[0], p.a1[1], p.a1[2]); hu.arms[1].el.rotation.set(p.a1[3], 0, 0);
  const blink = ((t + .4) % 3.1) < .1 && t > L[0] ? 1 : 0;
  hu.eyes.forEach((e, i) => {
    const sc = 1 + p.wide * .3; e.ew.scale.set(sc, sc, .6 * sc);
    e.pupil.position.set(p.look[0] * .012, p.look[1] * .012, .026);
    e.lid.rotation.x = -.6 + Math.max(blink, p.shut) * 1.5 - p.wide * .5;
    hu.brows[i].position.y = .258 + p.brow * .02; hu.brows[i].rotation.z = (i ? 1 : -1) * p.brow * -.28;
  });
  hu.mouthArc.rotation.z = p.smile >= 0 ? Math.PI : 0; hu.mouthArc.position.y = p.smile >= 0 ? .1 : .07;
  hu.mouthArc.scale.set(.8 + Math.abs(p.smile) * .4, .25 + Math.abs(p.smile) * .7, 1);
  const open = clamp(Math.max(p.open, talk * (.35 + .35 * Math.abs(Math.sin(t * 17)))));
  hu.mouthO.scale.set(.7 + open * .3, .08 + open * .55, .35); hu.mouthO.visible = open > .05; hu.mouthArc.visible = open < .5;
}

// ---------------------------------------------------------------- the server room: two rows of racks down a corridor
const srv = grp(scene, SRV_X, 0, 0);
srv.add(at(mesh(new THREE.PlaneGeometry(6, 20).rotateX(-Math.PI / 2), std(0x0e1014, { roughness: .35, metalness: .4 }), false, true), 0, 0, -6));
srv.add(at(mesh(new THREE.PlaneGeometry(6, 20).rotateX(Math.PI / 2), std(0x07080a), false, false), 0, 2.7, -6));
const RACKS = [];
for (let i = 0; i < 9; i++) for (const s of [-1, 1]) {
  const z = 1 - i * 1.25;
  const r = mesh(rb(.7, 2.3, 1.1, .02, 2), std(0x0d0e12, { roughness: .45, metalness: .5 }));
  r.position.set(s * 1.15, 1.15, z); srv.add(r); RACKS.push({ s, z });
}
const LED_N = RACKS.length * 24;
const leds = new THREE.InstancedMesh(new THREE.BoxGeometry(.03, .012, .006), new THREE.MeshBasicMaterial({ toneMapped: false }), LED_N);
leds.frustumCulled = false; srv.add(leds);
RACKS.forEach((r, k) => { for (let j = 0; j < 24; j++) {
  tP.set(r.s * (1.15 - .353), .35 + Math.floor(j / 3) * .23 + hash(k * 31 + j) * .02, r.z - .3 + (j % 3) * .2);
  tQ.setFromAxisAngle(V(0, 1, 0), Math.PI / 2 * r.s); leds.setMatrixAt(k * 24 + j, tM.compose(tP, tQ, tS.set(1, 1, 1)));
} });
const rackScreen = new THREE.Mesh(new THREE.PlaneGeometry(.5, .3), new THREE.MeshBasicMaterial({ toneMapped: false }));
rackScreen.position.set(-1.15 + .353 + .002, 1.55, -1.5); rackScreen.rotation.y = Math.PI / 2; srv.add(rackScreen);

// the same two eyes, far down the dark corridor once the racks die: Claude is already there
const srvEyes = [-1, 1].map((s) => {
  const e = new THREE.Mesh(new THREE.CapsuleGeometry(.045, .05, 6, 12), glow(CORAL, 3.2)); e.position.set(s * .2, 1.5, -11); srv.add(e);
  const h = halo(.9, CORAL, 0); h.position.set(s * .2, 1.5, -10.98); srv.add(h);
  return { e, h };
});

// floating dust in the monitor's light
const DUST_N = 140;
const dust = new THREE.InstancedMesh(new THREE.PlaneGeometry(.012, .012), add(0xcfe0ff, .6, { map: glowTex }), DUST_N); dust.frustumCulled = false; scene.add(dust);

// ---------------------------------------------------------------- textures: the monitor, the phone, the rack screen, the snapshot
const TX = {};
let screenKey = "";
function sparkGlyph(g, x, y, R, c) {
  g.fillStyle = c;
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2, l = R * (.75 + hash(i + 3) * .3); g.save(); g.translate(x, y); g.rotate(a); rr(g, -R * .13, R * .2, R * .26, l, R * .13); g.fill(); g.restore(); }
  g.beginPath(); g.arc(x, y, R * .42, 0, 7); g.fill();
}
function term(g, w, h, bg = "#04070c") { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,255,255,.035)"; for (let y = 0; y < h; y += 4) g.fillRect(0, y, w, 1); }
function drawScreen(k) {
  if (k === screenKey) return;
  screenKey = k;
  const g = SCR.getContext("2d"), w = SCR.width, h = SCR.height;
  const [kind, a] = k.split("|");
  if (kind === "cmd") {
    term(g, w, h);
    // the close-up sees the middle half of the screen: everything that matters sits in x 250..774
    write(g, "test-db", 330, 50, 30, { c: "#5d6e80", a: "center" });
    g.fillStyle = "#ff3030"; rr(g, 438, 22, 300, 58, 12); g.fill();
    write(g, "PRODUCTION", 588, 52, 34, { c: "#fff", a: "center", w: 800 });
    write(g, "connected to prod-db-01", 512, 128, 30, { c: "#ff8a8a", a: "center" });
    write(g, "DROP DATABASE", 512, 215, 62, { c: "#e8f1f8", a: "center", w: 800 });
    write(g, "app;", 512, 290, 62, { c: "#e8f1f8", a: "center", w: 800 });
    if (a === "c") { g.fillStyle = "#e8f1f8"; g.font = "800 62px JBMono"; g.fillRect(512 + g.measureText("app;").width / 2 + 10, 262, 30, 58); }
  } else if (kind === "deleted") {
    g.fillStyle = "#3a0606"; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,40,40,.08)"; for (let y = 0; y < h; y += 4) g.fillRect(0, y, w, 1);
    write(g, "PRODUCTION", 512, 80, 40, { c: "#ff8a8a", a: "center", w: 800 });
    write(g, "1,204,883", 512, 230, 118, { w: 800, c: "#ff4040", f: "Montserrat", a: "center" });
    write(g, "ROWS DELETED", 512, 350, 60, { c: "#ffd0d0", a: "center" });
    write(g, "database \"app\" does not exist", 512, 470, 30, { c: "#ff8a8a", a: "center" });
  } else if (kind === "claude") {
    term(g, w, h, "#07050a");
    sparkGlyph(g, 76, 76, 34, "#ff6a4a"); write(g, "claude", 130, 78, 34, { c: "#ff8a6a" });
    const lines = a.split("~");
    lines.forEach((s, i) => write(g, s, 50, 220 + i * 92, 66, { w: 700, c: "#ffb59c", max: w - 90 }));
  } else if (kind === "log") {
    term(g, w, h, "#07050a");
    write(g, "claude · activity log", 40, 60, 30, { c: "#ff8a6a" });
    [["FRI 17:58", "you: \"clean things up\"", "#e8f1f8"], ["FRI 17:59", "DROP SCHEMA staging;", "#ff6060"], ["FRI 18:03", "you: \"…oops\"", "#e8f1f8"],
      ["MON 09:00", "claude: snapshot before every", "#ffb59c"], ["", "\"clean things up\". always.", "#ffb59c"]].slice(0, +a).forEach(([d, s, c], i) => {
      write(g, d, 40, 150 + i * 92, 32, { c: "#6f8296" }); write(g, s, 250, 150 + i * 92, 36, { c, max: w - 280 });
    });
  } else if (kind === "restore") {
    term(g, w, h, "#05080a");
    write(g, "RESTORING production", 40, 90, 44, { c: "#e8f1f8" }); write(g, "from snapshot_0306.db", 40, 150, 34, { c: "#ff8a6a" });
    g.fillStyle = "rgba(255,255,255,.08)"; rr(g, 40, 260, w - 80, 70, 14); g.fill();
    const f = +a / 100; g.fillStyle = f < 1 ? "#ff6a4a" : "#3dff8a"; rr(g, 40, 260, (w - 80) * Math.max(.02, f), 70, 14); g.fill();
    write(g, `${a}%`, w / 2, 430, 110, { w: 800, a: "center", c: f < 1 ? "#ffb59c" : "#8affb8", f: "Montserrat" });
    if (f >= 1) write(g, "1,204,883 rows · back", w / 2, 540, 38, { a: "center", c: "#8affb8" });
  } else if (kind === "revoked") {
    g.fillStyle = "#170404"; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,60,40,.06)"; for (let y = 0; y < h; y += 4) g.fillRect(0, y, w, 1);
    sparkGlyph(g, 76, 76, 34, "#ff6a4a"); write(g, "claude", 130, 78, 34, { c: "#ff8a6a" });
    write(g, "PRODUCTION ACCESS", 50, 250, 60, { w: 800, c: "#ffd0c4", f: "Montserrat" });
    write(g, "REVOKED", 50, 370, 130, { w: 900, c: "#ff4a2a", f: "Montserrat" });
    write(g, "user: you", 54, 500, 36, { c: "#ff8a6a" });
  } else { g.fillStyle = "#010102"; g.fillRect(0, 0, w, h); }
  screenTex.needsUpdate = true;
}
let phoneKey = "";
function drawPhone(n) {
  const k = String(n); if (k === phoneKey) return; phoneKey = k;
  const g = PCAN.getContext("2d"), w = PCAN.width, h = PCAN.height;
  g.fillStyle = "#06070a"; g.fillRect(0, 0, w, h);
  write(g, "03:07", w / 2, 110, 84, { w: 300, a: "center", c: "#e8eef6", f: "Montserrat" });
  write(g, "Tuesday, 28 October", w / 2, 175, 22, { a: "center", c: "#9aa8b8", f: "Montserrat", w: 500 });
  const N = [["#ff3b3b", "PagerDuty", "CRITICAL: prod-db-01 down"], ["#ff8a3b", "Status", "900 users online · errors 100%"], ["#3b8bff", "Slack", "#incidents: is the site down??"],
    ["#ff3b3b", "PagerDuty", "CRITICAL: checkout failing"], ["#9b5bff", "Support", "37 new tickets"]];
  N.slice(0, n).forEach(([c, a, b], i) => {
    const y = 240 + i * 92;
    g.fillStyle = "rgba(40,44,54,.92)"; rr(g, 14, y, w - 28, 80, 16); g.fill();
    g.fillStyle = c; rr(g, 28, y + 16, 48, 48, 12); g.fill();
    write(g, a, 92, y + 26, 20, { c: "#cfd8e4", f: "Montserrat", w: 700 }); write(g, b, 92, y + 54, 19, { c: "#9aa8b8", f: "Montserrat", w: 500, max: w - 120 });
  });
  phoneTex.needsUpdate = true;
}
function drawTextures() {
  TX.rackOk = canvasTex(500, 300, (g, w, h) => { term(g, w, h, "#030806"); write(g, "BACKUP JOB", 24, 50, 30, { c: "#8affb8" }); write(g, "scheduled · nightly", 24, 100, 26, { c: "#6fbf8e" }); });
  TX.rackFail = canvasTex(500, 300, (g, w, h) => {
    term(g, w, h, "#120303"); write(g, "BACKUP JOB", 24, 50, 30, { c: "#ff8a8a" }); write(g, "LAST SUCCESS:", 24, 115, 28, { c: "#ff9a9a" });
    write(g, "03 MAR", 24, 190, 72, { w: 800, c: "#ff4040", f: "Montserrat" }); write(g, "status: FAILED · 239 days", 24, 262, 24, { c: "#ff8a8a" });
  });
  TX.snap = canvasTex(1000, 600, (g, w, h) => {
    rr(g, 6, 6, w - 12, h - 12, 40); g.fillStyle = "rgba(20,8,8,.92)"; g.fill(); g.strokeStyle = "#ff6a4a"; g.lineWidth = 8; g.stroke();
    g.fillStyle = "#ff6a4a"; rr(g, 60, 110, 170, 220, 18); g.fill(); g.fillStyle = "#200808"; g.fillRect(90, 160, 110, 14); g.fillRect(90, 200, 110, 14); g.fillRect(90, 240, 80, 14);
    write(g, "snapshot_0306.db", 270, 170, 58, { w: 800, c: "#ffd6c8" });
    write(g, "1,204,883 rows", 270, 250, 46, { c: "#ff9a7a" });
    write(g, "taken by claude · tue 21:40", 60, 440, 38, { c: "#ffb59c" });
    write(g, "before \"clean things up\"", 60, 510, 38, { c: "#ff8a6a" });
  });
  snapFace.material.map = TX.snap; snapFace.material.needsUpdate = true;
  rackScreen.material.map = TX.rackOk; rackScreen.material.needsUpdate = true;
}

// ---------------------------------------------------------------- the story at work
const TYPE = (s, a, cps = 22, t) => s.slice(0, clamp(Math.floor((t - a) * cps), 0, s.length));
function animScene(t) {
  // the monitor's content, through the night
  if (t < T.enter) drawScreen(`cmd|${Math.floor(t * 2.6) % 2 ? "c" : ""}`);
  else if (t < L[1] - .05) drawScreen("deleted|");
  else if (t < L[3] - .05) drawScreen(`claude|${TYPE("It ran.", L[1], 14, t)}`);
  else if (t < L[4] - .05) drawScreen("deleted|");
  else if (t < L[7] - .05) drawScreen("claude|" + (t > L[5] ? TYPE("Backup job: stopped~in March.", L[5], 20, t) : "…"));
  else if (t < E[7] + .35) drawScreen(`claude|${TYPE("I know.", L[7], 12, t)}`);
  else if (t < L[10] - .05) drawScreen("off|");
  else if (t < L[11] - .05) drawScreen(`log|${clamp(Math.floor((t - L[10] + .3) / .5) + 1, 1, 5)}`);
  else if (t < T.revoked - .3) drawScreen(`restore|${Math.round(100 * easeIO(win(t, L[11] + .2, T.done)))}`);
  else if (t < T.cut) drawScreen("revoked|");
  else drawScreen("off|");
  const mood = t < T.enter ? COLD : t < L[1] - .05 ? RED : between(t, L[3] - .05, L[4] - .05) ? RED : between(t, T.revoked - .3, T.cut) ? RED : t >= T.eyes && t < L[11] - .05 ? CORAL : between(t, L[11] - .05, T.revoked - .3) ? 0xffc0a8 : CORAL_L;
  const dark = screenKey.startsWith("off");
  const flick = 1 - .35 * pulse(t, T.enter, .02, .08) - .5 * (t > T.revoked - .05 && t < T.cut ? (Math.sin(t * 61) > .3 ? 1 : 0) : 0);
  screenSpot.color.set(mood); screenFill.color.set(mood);
  screenSpot.intensity = dark ? 0 : 7 * flick; screenFill.intensity = dark ? 0 : 1.3 * flick;
  // the ceiling: on at the start, off row by row on "rows", back on with the restore, all off on "revoked"
  const rowOn = (r) => {
    if (t < T.rows) return 1;
    if (t < L[11]) return 1 - win(t, T.rows + (3 - r) * .28, T.rows + (3 - r) * .28 + .06);
    if (t < T.cut) return win(t, L[11] + .4 + r * ((T.done - L[11] - .4) / 4), L[11] + .46 + r * ((T.done - L[11] - .4) / 4));
    return 0;
  };
  ceilLights.forEach((l, r) => { const on = rowOn(r) * (1 - .6 * (between(t, T.revoked - .05, T.cut) && Math.sin(t * 47 + r) > 0 ? 1 : 0)); l.intensity = on * 5; l.userData.on = on; });
  PANELS.forEach(({ p, r }) => p.material.color.setScalar(.03 + ceilLights[r].userData.on * 1.6));
  // the phone: dark, then the night's notifications on "Nine hundred"
  const nCount = t < L[6] - .3 ? 0 : clamp(Math.floor((t - L[6] + .3) / .38) + 1, 0, 5);
  drawPhone(nCount);
  const buzz = nCount > 0 && t < L[8] ? pulse((t - L[6] + .3) % .38, .0, .02, .15) : 0;
  phoneG.position.set(.42 + Math.sin(t * 90) * .003 * buzz, .79 + buzz * .002, .02);
  phoneScreen.material.color.setScalar(nCount ? 1 : .05);
  phoneLight.position.set(.42, .9, .02); phoneLight.intensity = nCount ? .8 + buzz * 1.5 : 0;
  // the eyes: open in the blackout, watch through the snapshot and the joke, close for the restore, return at the end
  const eyeK = t < T.eyes ? 0 : t < L[11] - .05 ? 1 : t < T.cut + .2 ? 0 : t < T.end ? 1 : 0;
  const blinkE = Math.min(easeOut(win(t, T.eyes, T.eyes + .35)), 1 - pulse(t, L[8] + 1.6, .05, .12), 1 - pulse(t, T.friday + .1, .05, .12), 1 - pulse(t, T.end - .7, .05, .12));
  eyes.forEach(({ e, h }, i) => {
    const k = eyeK * (t < L[11] ? blinkE : easeOut(win(t, T.cut + .2, T.cut + .6)) * (1 - pulse(t, T.end - .7, .05, .12)));
    e.visible = k > .01; e.scale.set(1, Math.max(.05, k), 1);
    e.position.x = (i ? 1 : -1) * .085 + (t > L[9] ? Math.sin(t * .7) * .01 : 0);
    h.material.color.set(CORAL).multiplyScalar(.5 * k);
  });
  eyeLight.intensity = eyeK * 1.6;
  // the snapshot: floats out of the screen on "snapshot", hangs in the dark, flies back in for the restore
  const sk = easeOut(win(t, T.snapshot - .15, T.snapshot + .6)), back = easeIn(win(t, L[11] - .2, L[11] + .25));
  snapCard.visible = sk > .01 && back < .99;
  snapCard.position.set(0, lerp(1.2, 1.38, sk) - back * .18, lerp(-.24, .2, sk) - back * .44 + Math.sin(t * 1.6) * .006);
  snapCard.scale.setScalar(Math.max(.001, lerp(.3, 1, sk) * (1 - back * .7)));
  snapCard.rotation.set(-.12, Math.sin(t * .8) * .06, 0);
  snapHalo.material.color.set(CORAL).multiplyScalar(.35 * sk * (1 - back));
  // the server room: LEDs blink green; on "March" the failure bleeds down the rows; on "checked" they die
  const bleed = win(t, T.march - .2, T.checked + .2);
  for (let k = 0; k < LED_N; k++) {
    const rack = Math.floor(k / 24), depth = Math.floor(rack / 2) / 8;
    const red = bleed > depth * .85 + .02, dead = t > T.checked + .25 + depth * .25;
    const on = ((t * (3 + hash(k) * 9) + hash(k + 3) * 10) % 1) > .35;
    tC.set(red ? RED : GREEN).multiplyScalar(dead ? .03 : on ? (red ? 2.4 : 1.6) : .15);
    leds.setColorAt(k, tC);
  }
  leds.instanceColor.needsUpdate = true;
  rackScreen.material.map = t < T.march ? TX.rackOk : TX.rackFail;
  const se = easeOut(win(t, T.checked + .3, T.checked + .55));
  srvEyes.forEach(({ e, h }) => { e.visible = se > .01; e.scale.set(1, Math.max(.05, se), 1); h.material.color.set(CORAL).multiplyScalar(.45 * se); });
  srvLights.forEach((l, i) => { l.color.set(bleed > i * .35 ? RED : GREEN); l.intensity = t > T.checked + .25 + i * .2 ? .2 : 2.2; });
  // the enter key goes down
  enterKey.position.y = .808 - pulse(t, T.enter - .04, .04, .12) * .006;
}

// ---------------------------------------------------------------- camera: CCTV angles and close-ups, hard cuts
const CCTV = [[3.6, 2.75, 4.4], [0, .95, -.6]];
const SHOTS = [
  { a: 0, b: T.enter, p: [[0, 1.29, .47], [0, 1.288, .39]], q: [[0, 1.287, -.25], [0, 1.287, -.25]], fov: 55, cctv: 0 },
  { a: T.enter, b: L[1] - .05, p: [[0, 1.287, .39], [0, 1.27, .34]], q: [[0, 1.287, -.25], [0, 1.25, -.25]], fov: [55, 64], cctv: 0 },
  { a: L[1] - .05, b: L[2] - .05, p: [CCTV[0], [3.5, 2.72, 4.25]], q: [CCTV[1], CCTV[1]], fov: [52, 49], cctv: 1 },
  { a: L[2] - .05, b: L[3] - .05, p: [[1.25, 1.55, -.4], [1.1, 1.52, -.3]], q: [[0, 1.33, .5], [0, 1.35, .5]], fov: [48, 42], cctv: 0 },
  { a: L[3] - .05, b: L[4] - .05, p: [CCTV[0], [3.45, 2.7, 4.1]], q: [CCTV[1], [0, .95, -.8]], fov: [50, 46], cctv: 1 },
  { a: L[4] - .05, b: L[6] - .05, p: [[SRV_X, 1.35, 4.2], [SRV_X - .1, 1.3, 1.2]], q: [[SRV_X, 1.25, -6], [SRV_X - .25, 1.3, -6]], fov: 46, cctv: .6 },
  { a: L[6] - .05, b: L[7] - .05, p: [[.62, 1.14, .14], [.58, 1.08, .12]], q: [[.42, .79, .02], [.42, .79, .02]], fov: [36, 32], cctv: 0 },
  { a: L[7] - .05, b: L[9] - .05, p: [[0, 1.25, .62], [0, 1.24, .38]], q: [[0, 1.22, -.25], [0, 1.24, -.25]], fov: 40, cctv: 0 },
  { a: L[9] - .05, b: L[10] - .05, p: [[.95, 1.52, -.45], [.85, 1.51, -.32]], q: [[0, 1.47, .68], [0, 1.47, .68]], fov: [46, 40], cctv: 0 },
  { a: L[10] - .05, b: L[11] - .05, p: [[.12, 1.23, .45], [.05, 1.22, .3]], q: [[0, 1.2, -.25], [0, 1.2, -.25]], fov: 38, cctv: 0 },
  { a: L[11] - .05, b: T.done + .5, p: [CCTV[0], [3.3, 2.6, 3.9]], q: [CCTV[1], CCTV[1]], fov: [52, 48], cctv: 1 },
  { a: T.done + .5, b: L[13] - .05, p: [[.9, 1.45, 1.9], [.75, 1.4, 1.75]], q: [[0, 1.1, .5], [0, 1.1, .5]], fov: 44, cctv: 0 },
  { a: L[13] - .05, b: T.end, p: [[0, 1.24, .5], [0, 1.24, .3]], q: [[0, 1.21, -.25], [0, 1.22, -.25]], fov: 40, cctv: 0 },
];
function shot(t) {
  let s = SHOTS[0]; for (const x of SHOTS) if (t >= x.a) s = x;
  const k = easeIO(win(t, s.a, s.b));
  return [lerpV(s.p[0], s.p[1], k), lerpV(s.q[0], s.q[1], k), Array.isArray(s.fov) ? lerp(s.fov[0], s.fov[1], k) : s.fov, s.cctv];
}

// ---------------------------------------------------------------- render
function renderAt(t) {
  const [p, q, fov, cctv] = shot(t);
  const hand = cctv ? .0 : .004, shake = pulse(t, T.enter, .02, .4) + pulse(t, T.cut - .02, .02, .3) * .5 + pulse(t, T.eyes, .02, .3) * .3;
  camera.position.set(p[0] + Math.sin(t * 1.3) * hand + Math.sin(t * 87) * .006 * shake, p[1] + Math.cos(t * 1.1) * hand + Math.cos(t * 71) * .006 * shake, p[2]);
  camera.lookAt(q[0], q[1], q[2]);
  camera.fov = fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  const inSrv = between(t, L[4] - .05, L[6] - .05);
  office.visible = !inSrv; srv.visible = inSrv; hu.root.visible = !inSrv;
  scene.fog.density = inSrv ? .12 : .085;
  animHuman(t); animScene(t);
  for (let i = 0; i < DUST_N; i++) {
    tP.set(((hash(i) * 2 + t * .02 * (hash(i + 2) - .5)) % 2) - 1 + (inSrv ? SRV_X : 0), .9 + ((hash(i + 1) * .9 + t * .015) % .9), -.2 + hash(i + 3) * (inSrv ? -6 : 1.6));
    tS.setScalar(.6 + hash(i + 4) * 1.4);
    dust.setMatrixAt(i, tM.compose(tP, camera.quaternion, tS));
  }
  dust.instanceMatrix.needsUpdate = true;
  const g = grade.uniforms;
  g.uTime.value = Math.round(t * 30) / 30;
  const relief = between(t, L[11] + .3, T.revoked - .1) ? easeIO(win(t, L[11] + .3, T.done)) : 0;
  g.uSat.value = cctv >= 1 ? .35 : lerp(.75, 1.0, relief);
  g.uGrain.value = cctv >= 1 ? .11 : .07;
  g.uVig.value = lerp(1.05, .7, relief);
  g.uTint.value.set(lerp(.9, 1.06, relief), lerp(1.0, 1.0, relief), lerp(1.1, .92, relief));
  g.uChroma.value = .3 + shake * 2.2 + pulse(t, T.eyes, .02, .5) * 2;
  g.uRoll.value = cctv >= 1 ? 1 : 0;
  g.uTear.value = pulse(t, L[1] - .05, .02, .2) + pulse(t, L[3] - .05, .02, .2) + pulse(t, L[11] - .05, .02, .2) + pulse(t, T.eyes - .02, .02, .35) * 1.5 +
    (between(t, T.revoked - .05, T.cut) ? .5 : 0) + pulse(t, T.enter, .02, .25);
  bloom.strength = t < L[1] - .05 ? .28 : lerp(.75, .45, relief);           // the opening screen has to stay readable
  composer.render();
}

// ---------------------------------------------------------------- cover still (cover.html sets window.HR_COVER)
function renderCover(c) {
  renderAt(c.t);
  camera.position.set(...c.cam); camera.lookAt(...c.look); camera.fov = c.fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  grade.uniforms.uTear.value = 0; grade.uniforms.uRoll.value = 0;
  composer.render();
}

const ready = (async () => {
  await Promise.all(["800 90px Montserrat", "700 30px Montserrat", "500 30px Montserrat", "700 34px JBMono"].map((f) => document.fonts.load(f)));
  drawTextures();
  drawScreen("cmd|c");
  drawPhone(0);
  renderer.compile(scene, camera);
  if (window.HR_COVER) { renderCover(window.HR_COVER); window.__coverDone = true; return; }
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["hrworld"] = ready;
window.addEventListener("hf-seek", (e) => { if (TX.snap) renderAt(e.detail.time); });
