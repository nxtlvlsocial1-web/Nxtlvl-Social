// openGym x Claude: the 3D world. Everything is a pure function of time t (seconds), rendered on HyperFrames' hf-seek.
// Set: a Delhi apartment corner at night turned home gym (bench, mat, dumbbells, mirror, plant, window with city
// bokeh, violet neon sparkle). Characters: NXT, the violet sphere robot with a "muscle mode" (shell splits, chrome
// arms and a chest plate extrude, the orbit ring snaps into a belt, comically tiny legs), and the human (a stylized
// young guy in a grey hoodie on the bench). Props per beat: the fake paywall card that shatters, the code hologram,
// the stamped chips, the Claude key card and coach orb, goal chips, the 3D week calendar, the +2.5 kg plate and the
// hologram muscle map. Cue times come from the voice timings (window.OG_T, written by build/generate.py).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const T = window.OG_T;
const ENV = window.OG_ENV;
const L = T.l, E = T.e;                    // line starts and ends (12 lines)
const W = 1080, H = 1920;

const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: "high-performance" });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x07050d);
scene.fog = new THREE.FogExp2(0x0d0818, .028);
const camera = new THREE.PerspectiveCamera(36, W / H, .05, 120);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = .32;

// ---------------------------------------------------------------- post: bloom, then grain / vignette / chroma
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .38, .42, .92);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uGrain: { value: .045 }, uVig: { value: .55 }, uChroma: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uGrain, uVig, uChroma; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 c = vUv - .5; vec2 off = c * uChroma * .02;
      vec3 col = vec3(texture2D(tDiffuse, vUv + off).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - off).b);
      col += (h(floor(vUv * vec2(1080., 1920.)) + fract(uTime * 7.13) * 97.) - .5) * uGrain;
      vec2 v = c * vec2(1., .78);
      col *= 1. - uVig * dot(v, v) * 1.5;
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
const backOut = (k, c = 1.7) => 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2);
const elastic = (k) => (k <= 0 ? 0 : k >= 1 ? 1 : Math.pow(2, -10 * k) * Math.sin((k * 10 - .75) * (2 * Math.PI / 3)) + 1);
const win = (t, a, b) => clamp((t - a) / (b - a));
const pulse = (t, at, up = .08, down = .35) => (t < at ? 0 : t < at + up ? (t - at) / up : Math.max(0, 1 - (t - at - up) / down));
const between = (t, a, b) => t >= a && t < b;
const rb = (w, h, d, r = .06, seg = 3) => new RoundedBoxGeometry(w, h, d, seg, Math.min(r, w / 2 - .001, h / 2 - .001, d / 2 - .001));
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: .6, metalness: 0, ...o });
const phys = (color, o = {}) => new THREE.MeshPhysicalMaterial({ color, roughness: .3, metalness: 0, ...o });
const glow = (color, k = 3, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(k), toneMapped: false, ...o });
function mesh(geo, m, cast = true, recv = true) { const x = new THREE.Mesh(geo, m); x.castShadow = cast; x.receiveShadow = recv; return x; }
function hash(i) { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
function grp(parent, x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); if (parent) parent.add(g); return g; }
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const at = (o, x, y, z) => { o.position.set(x, y, z); return o; };
const VIOLET = 0x7b2ffb, LVIOLET = 0xa98bff, LILAC = 0xd9ccff, GREEN = 0x3fd69b, AMBER = 0xffc24a, RED = 0xff6b6b;

// keyframed poses: keys [[time, pose], ...]; each key blends in over `dur` seconds from the previous one
function poseAt(keys, t, dur = .3) {
  let prev = keys[0][1], cur = keys[0][1], k = 1;
  for (let i = 1; i < keys.length; i++) {
    if (t < keys[i][0]) break;
    prev = keys[i - 1][1]; cur = keys[i][1];
    k = easeIO(clamp((t - keys[i][0]) / (keys[i][2] || dur)));
  }
  return mixPose(prev, cur, k);
}
function mixPose(a, b, k) {
  const o = {};
  for (const key of new Set([...Object.keys(a), ...Object.keys(b)])) {
    const x = a[key] ?? b[key], y = b[key] ?? a[key];
    o[key] = typeof x === "object" ? mixPose(x, y, k) : lerp(x, y, k);
  }
  return o;
}
function envAt(who, t) { const a = ENV[who]; const i = clamp(t * ENV.fps, 0, a.length - 1); const i0 = Math.floor(i); return lerp(a[i0], a[Math.min(a.length - 1, i0 + 1)], i - i0); }

// canvas textures (drawn once the fonts are loaded)
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d"); draw(g, w, h);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8; return tx;
}
function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
const glowTex = canvasTex(128, 128, (g, w) => {
  const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(.35, "rgba(255,255,255,.55)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr; g.fillRect(0, 0, w, w);
});
glowTex.colorSpace = THREE.NoColorSpace;

// the 4-point nxtlvl sparkle as a 2D shape
function sparkleShape(R = 1, r = .22) {
  const s = new THREE.Shape();
  for (let i = 0; i <= 4; i++) {
    const a = i * Math.PI / 2 + Math.PI / 2;
    const tip = [Math.cos(a) * R, Math.sin(a) * R];
    if (i === 0) { s.moveTo(...tip); continue; }
    const m = a - Math.PI / 4;
    s.quadraticCurveTo(Math.cos(m) * r, Math.sin(m) * r, ...tip);
  }
  return s;
}

// ---------------------------------------------------------------- lights
scene.add(new THREE.HemisphereLight(0x8d7fe0, 0x140b22, .38));
const key = new THREE.SpotLight(0xffb46b, 90, 22, .62, .55, 1.6);
key.position.set(-5.2, 5.4, 4.6); key.target.position.set(0, .9, .2);
key.castShadow = true; key.shadow.mapSize.set(1024, 1024); key.shadow.bias = -.0004; key.shadow.normalBias = .02;
scene.add(key, key.target);
const rim = new THREE.SpotLight(VIOLET, 55, 20, .7, .6, 1.4);
rim.position.set(2.6, 4.2, -3.2); rim.target.position.set(0, 1, .4); scene.add(rim, rim.target);
const fill = new THREE.PointLight(0xffd7b0, 2.2, 8, 1.6); fill.position.set(.4, 1.6, 3.2); scene.add(fill);
const fxLight = new THREE.PointLight(LVIOLET, 0, 6, 1.4); scene.add(fxLight);       // flashes on hits
const redLight = new THREE.PointLight(0xff3344, 0, 4, 1.5); scene.add(redLight);  // the paywall's glow

// ---------------------------------------------------------------- set
const set = grp(scene);
const floor = mesh(new THREE.PlaneGeometry(30, 30), std(0x1b1422, { roughness: .55, metalness: .05 }), false, true);
floor.rotation.x = -Math.PI / 2; set.add(floor);
// floor boards
for (let i = -12; i <= 12; i++) {
  const b = mesh(new THREE.PlaneGeometry(.012, 30), std(0x0f0b14), false, true); b.rotation.x = -Math.PI / 2; b.position.set(i * .42, .001, 0); set.add(b);
}
const wallMat = std(0x211830, { roughness: .92 });
const back = mesh(new THREE.PlaneGeometry(30, 12), wallMat, false, true); back.position.set(0, 6, -3); set.add(back);
const side = mesh(new THREE.PlaneGeometry(30, 12), wallMat, false, true); side.rotation.y = Math.PI / 2; side.position.set(-4.4, 6, 0); set.add(side);
const skirt = mesh(new THREE.BoxGeometry(30, .12, .03), std(0x2c2140)); skirt.position.set(0, .06, -2.985); set.add(skirt);
// rubber mat
const matPad = mesh(rb(3.0, .03, 1.7, .012, 2), std(0x0e0d12, { roughness: .95 }), false, true); matPad.position.set(-.6, .015, .55); set.add(matPad);
// window with city bokeh
const winG = grp(set, 2.3, 2.15, -2.97);
const glass = mesh(new THREE.PlaneGeometry(2.2, 1.9), new THREE.MeshBasicMaterial({ color: 0x0b1030 }), false, false); winG.add(glass);
const frameMat = std(0x120d1a, { roughness: .5 });
for (const [w, h, x, y] of [[2.36, .09, 0, .99], [2.36, .09, 0, -.99], [.09, 2.06, 1.14, 0], [.09, 2.06, -1.14, 0], [.05, 1.9, 0, 0], [2.2, .05, 0, .1]]) {
  const f = mesh(new THREE.BoxGeometry(w, h, .08), frameMat); f.position.set(x, y, .04); winG.add(f);
}
const bokehCols = [0xffb46b, 0xffd27a, 0xff8a5c, 0x7fd0ff, 0xa98bff, 0xfff1c8];
for (let i = 0; i < 70; i++) {
  const s = .05 + hash(i + 3) * .16;
  const b = new THREE.Mesh(new THREE.PlaneGeometry(s, s), new THREE.MeshBasicMaterial({
    map: glowTex, color: new THREE.Color(bokehCols[i % bokehCols.length]).multiplyScalar(.6 + hash(i + 9) * 1.4),
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false,
  }));
  b.position.set((hash(i) - .5) * 2.1, -.95 + Math.pow(hash(i + 5), 1.6) * 1.5, .01); winG.add(b);
}
// mirror
const mirG = grp(set, -2.15, 1.45, -2.96);
mirG.add(mesh(rb(1.15, 2.3, .06, .03, 2), std(0x0c0a10, { roughness: .4 })));
const mirror = mesh(new THREE.PlaneGeometry(1.03, 2.18), std(0x9aa0b8, { metalness: 1, roughness: .07 }), false, false);
mirror.position.z = .035; mirG.add(mirror);
// plant
const plant = grp(set, -3.5, 0, -2.35);
plant.add(mesh(new THREE.CylinderGeometry(.26, .2, .5, 20), std(0xb4613e, { roughness: .8 })));
plant.children[0].position.y = .25;
const leafMat = std(0x1f5a35, { roughness: .55, side: THREE.DoubleSide });
for (let i = 0; i < 11; i++) {
  const l = mesh(new THREE.SphereGeometry(.5, 12, 8), leafMat); l.scale.set(.12, .55 + hash(i) * .3, .035);
  const a = i / 11 * Math.PI * 2;
  l.position.set(Math.cos(a) * .12, .85 + hash(i + 2) * .2, Math.sin(a) * .12);
  l.rotation.set(Math.sin(a) * .7, 0, -Math.cos(a) * .7); plant.add(l);
}
// shelf with towels
const shelf = mesh(rb(1.1, .05, .3, .01, 2), std(0x2a1e38)); shelf.position.set(-3.1, 1.7, -2.84); set.add(shelf);
for (let i = 0; i < 3; i++) { const tw = mesh(rb(.3, .14, .24, .05, 2), std([0xd9ccff, 0x7b2ffb, 0xf4f1fa][i], { roughness: .95 })); tw.position.set(-3.45 + i * .34, 1.8, -2.84); set.add(tw); }
// neon sparkle sign
const neonG = grp(set, .5, 3.05, -2.9);
{
  const pts = sparkleShape(.42, .1).getSpacedPoints(120).map((p) => V(p.x, p.y, 0));
  const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, true), 240, .011, 8, true), glow(LVIOLET, 2.2));
  neonG.add(tube);
  const halo = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 1.9), new THREE.MeshBasicMaterial({ map: glowTex, color: new THREE.Color(VIOLET).multiplyScalar(.22), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
  halo.position.z = -.02; neonG.add(halo);
  const neonLight = new THREE.PointLight(VIOLET, 2.5, 5, 1.4); neonLight.position.z = .4; neonG.add(neonLight);
}
// bench
const bench = grp(set, -1.0, 0, .3);
bench.add(at(mesh(rb(1.75, .12, .48, .05, 3), phys(0x17161d, { roughness: .42, clearcoat: .4 })), 0, .44, 0));
for (const x of [-.65, .65]) {
  const leg = mesh(rb(.07, .4, .42, .02, 2), std(0x2b2b33, { metalness: .8, roughness: .35 })); leg.position.set(x, .2, 0); bench.add(leg);
  const foot = mesh(rb(.1, .04, .5, .015, 2), std(0x1a1a20, { metalness: .7, roughness: .4 })); foot.position.set(x, .02, 0); bench.add(foot);
}
// dumbbells
function dumbbell(s = 1, headMat = std(0x26232c, { roughness: .45, metalness: .3 })) {
  const g = new THREE.Group();
  const bar = mesh(new THREE.CylinderGeometry(.018 * s, .018 * s, .36 * s, 12), std(0xb9b6c4, { metalness: 1, roughness: .25 }));
  bar.rotation.z = Math.PI / 2; g.add(bar);
  for (const x of [-.14, .14]) {
    const h = mesh(new THREE.CylinderGeometry(.075 * s, .075 * s, .09 * s, 6), headMat); h.rotation.z = Math.PI / 2; h.position.x = x * s; g.add(h);
  }
  return g;
}
const floorBells = grp(set);
for (const [x, z, r] of [[.05, .95, .3], [.2, 1.15, -.2]]) { const d = dumbbell(); d.position.set(x, .085, z); d.rotation.y = r; d.traverse((o) => (o.castShadow = true)); floorBells.add(d); }

// ---------------------------------------------------------------- the human
const SKIN = 0xa8694a, HOOD = 0x8f9097, PANTS = 0x23263a, HAIR = 0x0e0c0d;
function human() {
  const root = grp(scene, -1.02, 0, .34); root.rotation.y = .42;
  const hips = grp(root, 0, .62, 0);
  const pantsMat = std(PANTS, { roughness: .75 }), hoodMat = std(HOOD, { roughness: .88 }), skinMat = std(SKIN, { roughness: .55 });
  hips.add(mesh(rb(.46, .22, .36, .1, 3), pantsMat));
  const legs = [];
  for (const s of [-1, 1]) {
    const hip = grp(hips, s * .12, -.02, .02);
    const thigh = mesh(rb(.19, .46, .21, .09, 3), pantsMat); thigh.position.y = -.2; hip.add(thigh);
    const stripe = mesh(rb(.02, .44, .215, .01, 1), std(0xe9e6f0)); stripe.position.set(s * .095, -.2, 0); hip.add(stripe);
    const knee = grp(hip, 0, -.43, 0);
    const shin = mesh(rb(.165, .46, .175, .075, 3), pantsMat); shin.position.y = -.21; knee.add(shin);
    const ankle = grp(knee, 0, -.45, 0);
    const shoe = mesh(rb(.16, .11, .3, .045, 3), std(0xf1eff6, { roughness: .5 })); shoe.position.set(0, -.02, .07); ankle.add(shoe);
    const sole = mesh(rb(.17, .04, .31, .015, 2), std(0x2a2830)); sole.position.set(0, -.08, .07); ankle.add(sole);
    const swoosh = mesh(rb(.005, .03, .14, .002, 1), std(VIOLET)); swoosh.position.set(s * .081, -.01, .06); ankle.add(swoosh);
    legs.push({ hip, knee });
  }
  const spine = grp(hips, 0, .06, 0);
  const torso = mesh(rb(.64, .6, .4, .17, 4), hoodMat); torso.position.y = .3; spine.add(torso);
  const band = mesh(rb(.62, .08, .39, .04, 2), std(0x7f8087, { roughness: .9 })); band.position.y = .03; spine.add(band);
  const pocket = mesh(rb(.34, .16, .04, .03, 2), std(0x85868d, { roughness: .9 })); pocket.position.set(0, .16, .19); spine.add(pocket);
  const hoodRing = mesh(new THREE.TorusGeometry(.16, .065, 10, 24), hoodMat); hoodRing.position.set(0, .6, -.06); hoodRing.rotation.x = Math.PI / 2 - .5; spine.add(hoodRing);
  for (const s of [-1, 1]) { const st = mesh(new THREE.CylinderGeometry(.008, .008, .16, 6), std(0xf4f1fa)); st.position.set(s * .05, .5, .2); spine.add(st); }
  const neck = grp(spine, 0, .6, 0);
  neck.add(at(mesh(new THREE.CylinderGeometry(.065, .07, .12, 12), skinMat), 0, .03, 0));
  const head = grp(neck, 0, .07, .01);
  const skull = mesh(new THREE.SphereGeometry(.19, 28, 22), skinMat); skull.scale.set(.95, 1.08, 1); skull.position.y = .17; head.add(skull);
  const hair = mesh(new THREE.SphereGeometry(.2, 28, 16, 0, Math.PI * 2, 0, Math.PI * .52), std(HAIR, { roughness: .8 }));
  hair.scale.set(.98, 1.06, 1.04); hair.position.set(0, .2, -.02); hair.rotation.x = -.42; head.add(hair);
  for (let i = 0; i < 5; i++) { const tuft = mesh(new THREE.SphereGeometry(.05, 10, 8), std(HAIR, { roughness: .8 })); tuft.scale.set(1, .55, 1); tuft.position.set((i - 2) * .06, .335 - Math.abs(i - 2) * .012, .1); tuft.rotation.x = .4; head.add(tuft); }
  for (const s of [-1, 1]) { const ear = mesh(new THREE.SphereGeometry(.04, 10, 8), skinMat); ear.scale.set(.5, 1, .8); ear.position.set(s * .18, .16, 0); head.add(ear); }
  const nose = mesh(new THREE.SphereGeometry(.026, 10, 8), std(0x95593c)); nose.position.set(0, .15, .19); head.add(nose);
  const eyes = [], brows = [];
  for (const s of [-1, 1]) {
    const ew = mesh(new THREE.SphereGeometry(.034, 14, 10), std(0xf7f4ee, { roughness: .3 }), false); ew.scale.z = .6; ew.position.set(s * .068, .2, .165); head.add(ew);
    const pupil = mesh(new THREE.SphereGeometry(.019, 12, 8), std(0x140e0c, { roughness: .2 }), false); pupil.position.z = .026; ew.add(pupil);
    const lid = mesh(new THREE.SphereGeometry(.036, 14, 10, 0, Math.PI * 2, 0, Math.PI / 2), skinMat, false); lid.scale.z = .66; lid.rotation.x = -.6; ew.add(lid);
    eyes.push({ ew, pupil, lid });
    const br = mesh(rb(.075, .02, .02, .008, 2), std(HAIR), false); br.position.set(s * .07, .258, .178); head.add(br); brows.push(br);
  }
  const mouthArc = mesh(new THREE.TorusGeometry(.042, .01, 8, 20, Math.PI), std(0x5a2a22), false); mouthArc.position.set(0, .09, .176); head.add(mouthArc);
  const mouthO = mesh(new THREE.SphereGeometry(.04, 16, 10), std(0x2a0d0b, { roughness: .6 }), false); mouthO.scale.set(1, .5, .35); mouthO.position.set(0, .085, .17); head.add(mouthO);
  const arms = [];
  for (const s of [-1, 1]) {
    const sh = grp(spine, s * .33, .5, 0);
    const up = mesh(rb(.16, .34, .16, .075, 3), hoodMat); up.position.y = -.14; sh.add(up);
    const el = grp(sh, 0, -.3, 0);
    const fo = mesh(rb(.14, .3, .14, .065, 3), hoodMat); fo.position.y = -.13; el.add(fo);
    const cuff = mesh(new THREE.CylinderGeometry(.062, .062, .05, 12), std(0x7f8087, { roughness: .9 })); cuff.position.y = -.27; el.add(cuff);
    const hand = grp(el, 0, -.32, 0);
    hand.add(mesh(new THREE.SphereGeometry(.062, 14, 10), skinMat));
    const fingers = [];
    for (let i = 0; i < 3; i++) {
      const f = mesh(new THREE.CapsuleGeometry(.014, .07, 4, 8), skinMat); f.position.set((i - 1) * .03, -.08, .02); hand.add(f); fingers.push(f);
    }
    arms.push({ sh, el, hand, fingers });
  }
  // props in the hands: phone (right hand, s = -1) and dumbbells
  const phone = grp(arms[0].hand, 0, -.04, .06);
  phone.add(mesh(rb(.09, .17, .014, .015, 2), std(0x111015, { roughness: .3, metalness: .4 })));
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(.078, .155), glow(0xff3344, 2.2)); screen.position.z = .0075; screen.rotation.y = 0; phone.add(screen);
  phone.rotation.set(-1.0, 0, 0);
  const bells = arms.map((a) => { const d = dumbbell(.9); d.rotation.y = Math.PI / 2; d.position.set(0, -.02, .02); a.hand.add(d); d.traverse((o) => (o.castShadow = true)); return d; });
  return { root, hips, spine, neck, head, eyes, brows, mouthArc, mouthO, arms, legs, phone, screen, bells };
}
const hu = human();

const HP = {
  base: { sx: .08, sz: 0, sy: 0, hx: .05, hy: .3, hz: 0, a0: { x: -.55, y: 0, z: .1, ex: -.7, ez: 0 }, a1: { x: -.45, y: 0, z: -.12, ex: -.6, ez: 0 },
    brow: 0, smile: .3, open: 0, wide: 0, lookX: .2, lookY: 0, fing: 0 },
};
HP.slump = { ...HP.base, sx: .38, hx: .38, hy: .05, a0: { x: -1.05, y: .25, z: .2, ex: -1.35, ez: 0 }, a1: { x: -.35, y: 0, z: -.12, ex: -.55, ez: 0 },
  brow: -.8, smile: -.6, lookX: 0, lookY: -.6 };
HP.sigh = { ...HP.slump, sx: .48, hx: .5, hz: .12, brow: -1 };
HP.lookUp = { ...HP.base, sx: .12, hx: -.12, hy: .62, brow: .5, smile: 0, wide: .3, lookX: .5, lookY: .3,
  a0: { x: -.85, y: .25, z: .15, ex: -1.1, ez: 0 } };
HP.gasp = { ...HP.base, sx: -.1, hx: -.18, hy: .35, brow: 1, smile: 0, open: .9, wide: 1, lookX: .1, lookY: .2,
  a0: { x: -.7, y: .3, z: .35, ex: -1.3, ez: 0 }, a1: { x: -.75, y: -.2, z: -.45, ex: -1.4, ez: 0 } };
HP.listen = { ...HP.base, hy: .6, lookX: .55, brow: .25, smile: .25, a0: { x: -.85, y: .25, z: .15, ex: -1.0, ez: 0 } };
HP.count = { ...HP.base, sx: 0, hx: -.08, hy: .25, brow: .4, smile: .35, lookX: .2, lookY: .25,
  a0: { x: -.85, y: .25, z: .15, ex: -1.0, ez: 0 }, a1: { x: -1.5, y: -.3, z: -.35, ex: -1.75, ez: 0 } };
HP.curl = { ...HP.base, sx: -.02, hx: 0, hy: .2, brow: .2, smile: .4, lookX: .2, a0: { x: -.25, y: 0, z: .18, ex: -.4, ez: 0 }, a1: { x: -.25, y: 0, z: -.18, ex: -.4, ez: 0 } };
HP.curious = { ...HP.base, sx: .04, hx: -.15, hy: .55, hz: -.12, brow: .7, smile: -.1, lookX: .4, lookY: .35,
  a0: { x: -.3, y: 0, z: .15, ex: -.5, ez: 0 }, a1: { x: -.6, y: 0, z: -.2, ex: -1.0, ez: 0 } };
HP.watch = { ...HP.curious, hy: .35, hx: -.3, lookY: .6, brow: .4, open: .2 };
HP.down = { ...HP.base, sx: .32, hx: .7, hy: .05, brow: -.3, smile: -.2, lookX: 0, lookY: -1,
  a0: { x: -.2, y: 0, z: .2, ex: -.3, ez: 0 }, a1: { x: -.2, y: 0, z: -.2, ex: -.3, ez: 0 } };
HP.shrug = { ...HP.base, sx: .02, hx: -.05, hy: .3, hz: .15, brow: .9, smile: .55, lookX: .45,
  a0: { x: -.55, y: -.5, z: .75, ex: -1.5, ez: 0 }, a1: { x: -.55, y: .5, z: -.75, ex: -1.5, ez: 0 } };
HP.laugh = { ...HP.shrug, sx: -.12, hx: -.35, brow: .6, smile: 1, open: .55 };
HP.happy = { ...HP.base, hy: .5, smile: .9, brow: .4, lookX: .5, a1: { x: -1.5, y: -.2, z: -.4, ex: -1.9, ez: 0 } };

function applyArm(a, p) { a.sh.rotation.set(p.x, p.y, p.z); a.el.rotation.set(p.ex, 0, p.ez); }

function animHuman(t) {
  const keys = [[0, HP.slump], [.05 + L[0], HP.sigh, .4], [L[0] + .9, HP.slump, .5], [L[1] - .15, HP.lookUp, .25], [L[2], HP.gasp, .12],
    [E[2] + .1, HP.listen, .4], [L[5], HP.count, .3], [E[5] + .1, HP.listen, .35], [L[7], HP.curl, .3], [L[8], HP.curious, .3],
    [L[9], HP.watch, .4], [L[10] - .15, HP.down, .25], [L[10] + .3, HP.shrug, .25], [L[10] + .55, HP.laugh, .2], [L[11], HP.listen, .4],
    [T.gym + .3, HP.happy, .4]];
  const p = poseAt(keys, t);
  // breathing, talking, curls, laughing
  const talk = envAt("human", t);
  const br = Math.sin(t * 2.1) * .012;
  hu.spine.rotation.set(p.sx + br, p.sy, p.sz);
  hu.head.rotation.set(p.hx + talk * .06 * Math.sin(t * 13), p.hy + Math.sin(t * .9) * .03, p.hz);
  hu.hips.position.y = .62 - (p.sx > .4 ? .015 : 0);
  if (between(t, L[0] + .05, L[0] + .7)) hu.spine.position.y = .06 - Math.sin(win(t, L[0] + .05, L[0] + .7) * Math.PI) * .03;
  else hu.spine.position.y = .06;
  const a0 = { ...p.a0 }, a1 = { ...p.a1 };
  if (between(t, L[7] + .2, L[8])) {                    // alternating curls on the beat (120 bpm)
    const ph = (t - T.beat0) / .5;
    const c0 = Math.max(0, Math.sin(ph * Math.PI)), c1 = Math.max(0, -Math.sin(ph * Math.PI));
    const k = win(t, L[7] + .2, L[7] + .5) * (1 - win(t, L[8] - .25, L[8]));
    a0.ex -= c0 * 1.9 * k; a1.ex -= c1 * 1.9 * k; a0.x -= c0 * .15 * k; a1.x -= c1 * .15 * k;
  }
  if (between(t, L[10] + .55, L[11] + .3)) { const b = Math.abs(Math.sin((t - L[10]) * 18)) * .03; hu.spine.position.y = .06 + b; }
  applyArm(hu.arms[0], a0); applyArm(hu.arms[1], a1);
  // legs: seated
  for (const l of hu.legs) { l.hip.rotation.set(-1.42, 0, 0); l.knee.rotation.set(1.5, 0, 0); }
  hu.legs[0].hip.rotation.y = -.08; hu.legs[1].hip.rotation.y = .1;
  if (between(t, L[10] - .1, L[11])) { const j = Math.sin((t - L[10]) * 30) * .04 * (1 - win(t, L[10] + .6, L[11])); hu.legs.forEach((l) => (l.knee.rotation.x += j)); }
  // face
  const blink = ((t + .7) % 3.4) < .12 ? 1 : 0;
  hu.eyes.forEach((e, i) => {
    const sc = 1 + p.wide * .35; e.ew.scale.set(sc, sc, .6 * sc);
    e.pupil.position.set(p.lookX * .012, p.lookY * .012, .026);
    e.lid.rotation.x = -.6 + (blink ? 1.5 : 0) - p.wide * .5 + (p.brow < 0 ? -p.brow * .35 : 0);
    hu.brows[i].position.y = .258 + p.brow * .022;
    hu.brows[i].rotation.z = (i ? 1 : -1) * p.brow * -.25;
  });
  const sm = p.smile;
  hu.mouthArc.rotation.z = sm >= 0 ? Math.PI : 0;
  hu.mouthArc.position.y = sm >= 0 ? .1 : .07;
  hu.mouthArc.scale.set(.8 + Math.abs(sm) * .5, .25 + Math.abs(sm) * .75, 1);
  const open = clamp(Math.max(p.open, talk * 1.3));
  hu.mouthO.scale.set(.7 + open * .3, .08 + open * .55, .35);
  hu.mouthO.visible = open > .04;
  hu.mouthArc.visible = open < .5;
  // fingers: counting 1-2-3 on the goal words
  const n = t < T.g[0] ? 0 : t < T.g[1] ? 1 : t < T.g[2] ? 2 : 3;
  hu.arms[1].fingers.forEach((f, i) => { f.scale.y = between(t, L[5], E[5] + .2) && i < n ? 1.25 : .45; });
  // props
  hu.phone.visible = t < L[7] - .1;
  hu.screen.material.color.setScalar(1).multiply(new THREE.Color(t < L[1] + .4 ? 0xff3344 : 0x7b2ffb)).multiplyScalar(2 + Math.sin(t * 20) * .3 * (t < .7));
  hu.bells.forEach((b) => (b.visible = between(t, L[7] - .1, L[8] + .1)));
  floorBells.visible = !between(t, L[7] - .1, L[8] + .1);
  // phone buzz
  const bz = between(t, 0, .7) || between(t, 1.1, 1.5) ? Math.sin(t * 160) * .012 : 0;
  hu.phone.position.x = bz;
}

// ---------------------------------------------------------------- NXT
const R = .42;
const NX = V(1.18, 1.32, .42);           // rest position
function nxtBuild() {
  const root = grp(scene, NX.x, NX.y, NX.z); root.rotation.y = -.42;
  const body = grp(root);
  const shellMat = phys(0xffffff, { vertexColors: true, roughness: .22, metalness: .08, clearcoat: 1, clearcoatRoughness: .08 });
  function hemi(top) {
    const g = new THREE.SphereGeometry(R, 64, 32, 0, Math.PI * 2, top ? 0 : Math.PI / 2, Math.PI / 2);
    const c = new THREE.Color(), a = new THREE.Color(VIOLET), b = new THREE.Color(0x4a0fc2), cols = [];
    const pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) { c.copy(a).lerp(b, clamp((R - pos.getY(i)) / (2 * R))); cols.push(c.r, c.g, c.b); }
    g.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3));
    return mesh(g, shellMat);
  }
  const top = hemi(true), bot = hemi(false); body.add(top, bot);
  const seam = new THREE.Mesh(new THREE.TorusGeometry(R * .985, .012, 8, 64), glow(LVIOLET, 5)); seam.rotation.x = Math.PI / 2; body.add(seam);
  // visor with LED eyes (texture swapped per expression)
  const visor = mesh(new THREE.SphereGeometry(R * 1.006, 48, 24, Math.PI / 2 - .8, 1.6, Math.PI / 2 - .86, .8),
    new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .1, metalness: .2, emissive: 0xffffff, emissiveIntensity: 2.4 }), false);
  top.add(visor);
  const mouth = new THREE.Mesh(rb(.09, .018, .01, .008, 2), glow(LILAC, 3.5)); mouth.position.set(0, .07, Math.sqrt(R * R - .07 * .07) + .012); top.add(mouth);
  // antenna with the sparkle
  const ant = grp(top, 0, R - .02, 0);
  ant.add(at(mesh(new THREE.CylinderGeometry(.012, .016, .14, 8), std(0xd6d3e6, { metalness: 1, roughness: .2 })), 0, .07, 0));
  const spark = new THREE.Mesh(new THREE.ExtrudeGeometry(sparkleShape(.075, .018), { depth: .02, bevelEnabled: true, bevelSize: .006, bevelThickness: .006, bevelSegments: 2 }), glow(LVIOLET, 3.4));
  spark.position.set(0, .2, -.01); ant.add(spark);
  // orbit ring (rest) that becomes the power belt
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1, .02, 12, 96), phys(0xd6d3e6, { metalness: 1, roughness: .15, clearcoat: 1 }));
  ring.castShadow = true; root.add(ring);
  const beltGlow = new THREE.Mesh(new THREE.TorusGeometry(1, .006, 6, 96), glow(LVIOLET, 5)); ring.add(beltGlow);
  // chest plate
  const chest = grp(bot, 0, -.06, R * .78);
  const chrome = phys(0xd9d6e8, { metalness: 1, roughness: .16, clearcoat: 1, clearcoatRoughness: .05 });
  const vio = phys(VIOLET, { roughness: .25, clearcoat: 1, metalness: .2 });
  for (const s of [-1, 1]) { const pec = mesh(new THREE.SphereGeometry(.15, 24, 16), chrome); pec.scale.set(1.1, .66, .5); pec.position.set(s * .115, 0, 0); pec.rotation.z = s * .12; chest.add(pec); }
  const chestBar = new THREE.Mesh(rb(.03, .12, .03, .01, 1), glow(LVIOLET, 4)); chestBar.position.set(0, -.01, .04); chest.add(chestBar);
  // muscle arms
  const bicep = new THREE.LatheGeometry([[0, .03], [.1, 0], [.15, -.06], [.178, -.15], [.16, -.25], [.11, -.32], [.085, -.35], [0, -.36]].map(([x, y]) => new THREE.Vector2(x, y)), 32);
  const fore = new THREE.LatheGeometry([[0, 0], [.09, -.01], [.122, -.07], [.112, -.16], [.08, -.27], [0, -.29]].map(([x, y]) => new THREE.Vector2(x, y)), 28);
  const arms = [];
  for (const s of [-1, 1]) {
    const mount = grp(body, s * R * .92, -.03, 0);
    const sh = grp(mount);
    sh.add(mesh(new THREE.SphereGeometry(.16, 24, 16), vio));
    const up = mesh(bicep, chrome); up.scale.set(1, 1, 1.18); sh.add(up);
    const peak = mesh(new THREE.SphereGeometry(.11, 20, 14), chrome); peak.scale.set(1, 1.3, .9); peak.position.set(0, -.15, .07); sh.add(peak);
    const band = new THREE.Mesh(new THREE.TorusGeometry(.115, .014, 8, 28), glow(LVIOLET, 4)); band.rotation.x = Math.PI / 2; band.position.y = -.27; sh.add(band);
    const el = grp(sh, 0, -.34, 0);
    el.add(mesh(new THREE.SphereGeometry(.095, 16, 12), vio));
    el.add(mesh(fore, chrome));
    const fist = mesh(rb(.19, .17, .19, .06, 3), vio); fist.position.y = -.32; el.add(fist);
    const thumb = mesh(new THREE.CapsuleGeometry(.025, .05, 4, 8), vio); thumb.position.set(-s * .06, -.27, .06); thumb.rotation.z = s * .4; el.add(thumb);
    const hand = grp(el, 0, -.33, 0);
    arms.push({ mount, sh, el, hand, thumb });
  }
  // tiny legs
  const legs = [];
  for (const s of [-1, 1]) {
    const hip = grp(body, s * .13, -R + .05, 0);
    const thigh = mesh(new THREE.CapsuleGeometry(.032, .035, 4, 10), chrome); thigh.position.y = -.035; hip.add(thigh);
    const knee = grp(hip, 0, -.065, 0);
    const shin = mesh(new THREE.CapsuleGeometry(.026, .03, 4, 10), chrome); shin.position.y = -.03; knee.add(shin);
    const foot = mesh(rb(.065, .035, .09, .015, 2), vio); foot.position.set(0, -.068, .015); knee.add(foot);
    legs.push({ hip, knee, thigh });
  }
  // glowing dumbbell for the curls (left hand)
  const gb = dumbbell(.8, glow(LVIOLET, 2.6)); gb.rotation.y = Math.PI / 2; arms[1].hand.add(gb);
  const stamp = grp(arms[0].hand, 0, -.02, 0);
  stamp.add(at(mesh(new THREE.CylinderGeometry(.03, .03, .12, 12), std(0x2b2238)), 0, .02, 0));
  stamp.add(at(mesh(rb(.18, .05, .18, .02, 2), phys(GREEN, { clearcoat: 1, roughness: .3 })), 0, -.06, 0));
  return { root, body, top, bot, seam, visor, mouth, ant, spark, ring, beltGlow, chest, arms, legs, gb, stamp };
}
const nx = nxtBuild();

// LED eye expressions, drawn on the visor texture (one canvas per expression)
const EYE = {};
function drawEyes() {
  const shapes = {
    calm: (x, y) => x * x / .3 + y * y / .64 < 1,
    confident: (x, y) => x * x / .36 + y * y / .64 < 1 && y < .28,
    playful: (x, y) => Math.abs(y - (.45 - 1.15 * Math.abs(x))) < .3 && Math.abs(x) < .78,
    serious: (x, y) => Math.abs(y) < .2 && Math.abs(x) < .8,
    friendly: (x, y) => Math.abs(y - (.25 - 1.0 * x * x)) < .24 && Math.abs(x) < .82,
    wide: (x, y) => x * x + y * y < .7,
    blink: (x, y) => Math.abs(y) < .1 && Math.abs(x) < .7,
    power: (x, y) => Math.abs(x) < .35 && Math.abs(y) < .35,
  };
  const draw = (fl, fr) => canvasTex(384, 256, (g, w, h) => {
    g.fillStyle = "#050308"; g.fillRect(0, 0, w, h);
    const px = 12;
    for (const [cx, f] of [[.33, fl], [.67, fr]]) {
      for (let gy = -7; gy <= 7; gy++) for (let gx = -6; gx <= 6; gx++) {
        const x = gx / 6, y = -gy / 7;
        if (!f(x, y)) continue;
        g.fillStyle = "#e6dcff"; rr(g, cx * w + gx * px - 4.5, .48 * h + gy * px - 4.5, 9, 9, 3); g.fill();
      }
    }
  });
  for (const k of Object.keys(shapes)) EYE[k] = draw(shapes[k], shapes[k]);
  EYE.mysterious = draw(shapes.calm, (x, y) => shapes.calm(x, y) && y < .05);
}
function moodAt(t) {
  const m = [[0, "calm"], [L[1], "confident"], [T.claude - .1, "playful"], [L[2], "calm"], [L[3], "confident"], [L[4], "friendly"],
    [L[5], "calm"], [L[6], "playful"], [L[7], "confident"], [L[8], "calm"], [L[9], "playful"], [T.untrained - .05, "mysterious"],
    [T.legs, "playful"], [L[10], "friendly"], [L[11], "friendly"], [T.end - 1.3, "power"], [T.end - .9, "friendly"]];
  let cur = "calm"; for (const [a, k] of m) if (t >= a) cur = k;
  if (((t + .3) % 2.9) < .1 && cur !== "power") cur = "blink";
  return cur;
}

const NP = {
  rest: { a0: { x: 0, y: 0, z: -.25, ex: -.3, ez: 0 }, a1: { x: 0, y: 0, z: .25, ex: -.3, ez: 0 }, lean: 0, yaw: -.42 },
};
NP.ready = { ...NP.rest, a0: { x: -.2, y: 0, z: -.45, ex: -.9, ez: 0 }, a1: { x: -.2, y: 0, z: .45, ex: -.9, ez: 0 } };
NP.flex = { ...NP.rest, a0: { x: -.15, y: 0, z: -2.1, ex: 0, ez: -1.5 }, a1: { x: -.15, y: 0, z: 2.1, ex: 0, ez: 1.5 }, lean: -.06, yaw: -.25 };
NP.present = { ...NP.rest, a0: { x: -1.1, y: -.3, z: -.35, ex: -.25, ez: 0 }, a1: { x: -.1, y: 0, z: .35, ex: -.5, ez: 0 }, yaw: -.55 };
NP.stampUp = { ...NP.present, a0: { x: -2.3, y: -.2, z: -.3, ex: -1.0, ez: 0 } };
NP.stampDown = { ...NP.present, a0: { x: -.95, y: -.35, z: -.45, ex: -.2, ez: 0 }, lean: .12 };
NP.thumbs = { ...NP.rest, a0: { x: -.9, y: 0, z: -.3, ex: -1.4, ez: 0 }, yaw: -.45 };
NP.curl = { ...NP.rest, a1: { x: -.15, y: 0, z: .3, ex: -.3, ez: 0 }, a0: { x: 0, y: 0, z: -.55, ex: -1.2, ez: 0 }, yaw: -.3 };
NP.look = { ...NP.ready, yaw: -.8 };
NP.point = { ...NP.rest, a0: { x: -.35, y: 0, z: -1.25, ex: 0, ez: 0 }, a1: { x: -.1, y: 0, z: .5, ex: -1.0, ez: 0 }, yaw: -.15 };
NP.hips = { ...NP.rest, a0: { x: .1, y: 0, z: -.75, ex: -2.0, ez: 0 }, a1: { x: .1, y: 0, z: .75, ex: -2.0, ez: 0 }, yaw: -.35 };
NP.wave = { ...NP.rest, a0: { x: -.1, y: 0, z: -2.5, ex: 0, ez: -.5 }, yaw: -.15 };

function animNxt(t) {
  const land = L[1] - .12;                 // NXT slams down just before "Delete it"
  nx.root.visible = t >= land - .45;
  if (!nx.root.visible) return;
  // drop and squash
  const fall = win(t, land - .45, land);
  const bob = Math.sin(t * Math.PI * 2 / 1.6) * .04 * win(t, land + .5, land + 1.2);
  nx.root.position.set(NX.x, NX.y + (1 - easeIn(fall)) * 5 + bob, NX.z);
  const sq = pulse(t, land, .03, .35);
  nx.body.scale.set(1 + sq * .22, 1 - sq * .25, 1 + sq * .22);
  // power-up progress (muscle mode) and power-down at the end
  const up = easeOut(win(t, land + .12, land + .75)) * (1 - easeIO(win(t, T.end - 1.35, T.end - .85)));
  const split = Math.sin(clamp(up) * Math.PI) * .06 + up * .012;
  nx.top.position.y = split; nx.bot.position.y = -split * .4;
  nx.seam.material.color.setScalar(1).multiply(new THREE.Color(LVIOLET)).multiplyScalar(1 + up * 5 + pulse(t, land + .3, .05, .4) * 6);
  // ring -> belt
  const ringR = lerp(R * 1.5, R * 1.035, up), tube = lerp(.02, .05, up);
  nx.ring.scale.set(ringR, ringR, lerp(1, tube / .02, up) * 1);
  nx.ring.rotation.set(lerp(Math.PI / 2 + .35, Math.PI / 2, up), lerp(t * .9, 0, up), lerp(.25, 0, up));
  nx.beltGlow.visible = up > .5;
  // arms, chest, legs extrude
  const armK = backOut(win(t, land + .3, land + .75), 2.2) * (1 - easeIn(win(t, T.end - 1.35, T.end - 1.0)));
  nx.arms.forEach((a) => { a.mount.scale.setScalar(Math.max(.001, armK)); a.mount.visible = armK > .01; });
  nx.chest.position.z = R * .78 - (1 - up) * .12; nx.chest.scale.setScalar(Math.max(.001, up)); nx.chest.visible = up > .01;
  const legK = backOut(win(t, land + .55, land + .85), 3) * (1 - easeIn(win(t, T.end - 1.35, T.end - 1.0)));
  nx.legs.forEach((l) => { l.hip.scale.setScalar(Math.max(.001, legK)); l.hip.visible = legK > .01; });
  // pose
  const keys = [[0, NP.rest], [land + .45, NP.ready, .25], [T.free - .2, NP.flex, .18], [L[2], NP.ready, .35], [L[3], NP.present, .3],
    [L[4], NP.present, .3], [L[5], NP.look, .4], [L[6], NP.present, .3], [T.approve - .35, NP.stampUp, .2], [T.approve - .05, NP.stampDown, .07],
    [T.approve + .35, NP.thumbs, .25], [L[7], NP.curl, .3], [L[8], NP.look, .35], [L[9], NP.ready, .35], [T.legs - .15, NP.point, .2], [T.legs + .4, NP.flex, .2],
    [L[10], NP.hips, .3], [L[11], NP.rest, .3], [L[11] + .3, NP.wave, .3], [T.gym + .2, NP.thumbs, .3], [T.end - 1.6, NP.rest, .3]];
  const p = poseAt(keys, t);
  const a0 = { ...p.a0 }, a1 = { ...p.a1 };
  if (between(t, L[7] + .1, L[8])) {        // curls on the beat, opposite phase to the human
    const c = Math.max(0, -Math.sin((t - T.beat0) / .5 * Math.PI)) * win(t, L[7] + .1, L[7] + .4) * (1 - win(t, L[8] - .25, L[8]));
    a1.ex -= c * 1.9;
  }
  if (between(t, L[11] + .3, T.gym + .2)) a0.ez += Math.sin((t - L[11]) * 12) * .45;   // wave
  if (between(t, T.free - .2, L[2])) { const f = Math.sin((t - T.free) * 9) * .06; a0.ez -= f; a1.ez += f; }       // flex pump
  nx.arms.forEach((a, i) => applyArm(a, i ? a1 : a0));
  nx.root.rotation.y = p.yaw + Math.sin(t * .7) * .05;
  nx.body.rotation.x = p.lean + pulse(t, T.approve, .05, .3) * .15;
  nx.gb.visible = between(t, L[7] - .1, L[8] + .1);
  nx.stamp.visible = between(t, T.approve - .5, T.approve + .3);
  // tiny legs: dangling, a squat-flex on "Legs, bro"
  const lf = between(t, T.legs + .4, L[10] + .2) ? Math.abs(Math.sin((t - T.legs) * 7)) : 0;
  nx.legs.forEach((l, i) => {
    l.hip.rotation.set(-.1 - lf * .5, 0, (i ? 1 : -1) * (.12 + lf * .25));
    l.knee.rotation.x = .15 + lf * .9;
    l.thigh.scale.set(1 + lf * .5, 1, 1 + lf * .5);
  });
  // face: eyes, mouth bar (follows the voice)
  const mood = moodAt(t);
  if (nx.visor.material.map !== EYE[mood]) { nx.visor.material.map = EYE[mood]; nx.visor.material.emissiveMap = EYE[mood]; nx.visor.material.needsUpdate = true; }
  const v = envAt("nxt", t);
  nx.mouth.scale.set(.4 + v * 1.6, 1 + v * 2.2, 1);
  nx.spark.rotation.y = t * 1.2; nx.spark.material.color.setScalar(1).multiply(new THREE.Color(LVIOLET)).multiplyScalar(3 + v * 3);
}

// ---------------------------------------------------------------- FX: dust ring, shards, puff, sparkles
const shockwave = new THREE.Mesh(new THREE.RingGeometry(.9, 1, 64), glow(LVIOLET, 3, { transparent: true, depthWrite: false, side: THREE.DoubleSide }));
shockwave.rotation.x = -Math.PI / 2; scene.add(shockwave);
// incoming: a violet beam and a target ring on the floor build up before NXT slams down (anticipation in the hook)
const beam = new THREE.Mesh(new THREE.CylinderGeometry(.34, .62, 6, 32, 1, true),
  new THREE.MeshBasicMaterial({ color: new THREE.Color(LVIOLET).multiplyScalar(1.6), transparent: true, opacity: 0, depthWrite: false,
    blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false }));
scene.add(beam);
const target = new THREE.Mesh(new THREE.RingGeometry(.5, .56, 64), glow(LVIOLET, 3, { transparent: true, depthWrite: false, side: THREE.DoubleSide }));
target.rotation.x = -Math.PI / 2; scene.add(target);
const DUST = 46;
const dust = new THREE.InstancedMesh(new THREE.SphereGeometry(.05, 8, 6), std(0x6a5a86, { roughness: 1, transparent: true, opacity: .55 }), DUST);
scene.add(dust);
const SHARDS = 80;
const shards = new THREE.InstancedMesh(new THREE.TetrahedronGeometry(.07), phys(0xffffff, { roughness: .1, metalness: .3, clearcoat: 1, emissive: 0x2a0a40 }), SHARDS);
for (let i = 0; i < SHARDS; i++) shards.setColorAt(i, new THREE.Color(i % 3 ? 0xff3a4c : LVIOLET));
scene.add(shards);
const PUFF = 40;
const puff = new THREE.InstancedMesh(new THREE.SphereGeometry(.09, 10, 8), std(0xe9e1ff, { roughness: 1, transparent: true, opacity: .7 }), PUFF);
scene.add(puff);
const SPARKS = 36;
const sparks = new THREE.InstancedMesh(new THREE.ShapeGeometry(sparkleShape(.06, .014)), glow(LVIOLET, 4, { side: THREE.DoubleSide }), SPARKS);
scene.add(sparks);
const tmpM = new THREE.Matrix4(), tmpP = new THREE.Vector3(), tmpQ = new THREE.Quaternion(), tmpS = new THREE.Vector3(), tmpE = new THREE.Euler();
function setInst(im, i, x, y, z, s, rx = 0, ry = 0, rz = 0) {
  tmpP.set(x, y, z); tmpQ.setFromEuler(tmpE.set(rx, ry, rz)); tmpS.setScalar(Math.max(1e-4, s)); tmpM.compose(tmpP, tmpQ, tmpS); im.setMatrixAt(i, tmpM);
}
function animFx(t) {
  const land = L[1] - .12;
  const inc = easeIn(win(t, land - 1.1, land - .05)) * (1 - win(t, land, land + .25));
  beam.visible = target.visible = inc > .01;
  beam.position.set(NX.x, 3 + .05, NX.z); beam.material.opacity = inc * (.32 + Math.sin(t * 40) * .05);
  target.position.set(NX.x, .015, NX.z); target.scale.setScalar(1.6 - inc * .9); target.material.opacity = inc;
  const k = win(t, land, land + .6);
  shockwave.visible = k > 0 && k < 1;
  shockwave.position.set(NX.x, .02, NX.z); shockwave.scale.setScalar(.2 + easeOut(k) * 2.4); shockwave.material.opacity = (1 - k) * .9;
  dust.visible = between(t, land, land + 1.4);
  for (let i = 0; i < DUST; i++) {
    const a = hash(i) * Math.PI * 2, sp = .8 + hash(i + 4) * 1.6, dk = clamp((t - land) * 1.2);
    setInst(dust, i, NX.x + Math.cos(a) * (.3 + easeOut(dk) * sp), .05 + Math.sin(dk * Math.PI) * hash(i + 7) * .45, NX.z + Math.sin(a) * (.3 + easeOut(dk) * sp) * .6, (1 - dk) * (.6 + hash(i + 2)));
  }
  dust.instanceMatrix.needsUpdate = true;
  // paywall shatter on the bicep
  const s0 = T.free - .02, sk = t - s0;
  shards.visible = between(t, s0, s0 + 1.6);
  const c0 = CARD_HIT;
  for (let i = 0; i < SHARDS; i++) {
    const vx = (hash(i) - .5) * 4.2, vy = (hash(i + 1) * 1.0 + .2) * 2.6, vz = (hash(i + 2) - .3) * 2.6;
    const x = c0.x + vx * sk * (.5 + .5 * Math.exp(-sk * 2)), y = c0.y + vy * sk - 4.2 * sk * sk, z = c0.z + vz * sk;
    setInst(shards, i, x, Math.max(.03, y), z, (1 - win(sk, .9, 1.6)) * (.6 + hash(i + 3) * 1.1), sk * (3 + hash(i) * 8), sk * 5 + i, sk * 4);
  }
  shards.instanceMatrix.needsUpdate = true;
  // power-down puff and the sparkle burst at the end
  const pk = t - (T.end - 1.15);
  puff.visible = between(pk, 0, 1.1);
  for (let i = 0; i < PUFF; i++) {
    const a = hash(i + 11) * Math.PI * 2, b = (hash(i + 12) - .5) * Math.PI;
    const r = .25 + easeOut(clamp(pk / .8)) * (.4 + hash(i + 13) * .5);
    setInst(puff, i, NX.x + Math.cos(a) * Math.cos(b) * r, NX.y + Math.sin(b) * r + pk * .2, NX.z + Math.sin(a) * Math.cos(b) * r, (1 - clamp(pk / 1.1)) * (.8 + hash(i) * .8));
  }
  puff.instanceMatrix.needsUpdate = true;
  const sb = t - (T.end - 1.0);
  sparks.visible = sb > 0;
  for (let i = 0; i < SPARKS; i++) {
    const a = i / SPARKS * Math.PI * 2 + hash(i) * .3, r = easeOut(clamp(sb / 1.0)) * (.6 + hash(i + 5) * .9);
    setInst(sparks, i, NX.x + Math.cos(a) * r, NX.y + .1 + Math.sin(a) * r * .9, NX.z + .2, (1 - win(sb, .6, 1.4)) * (.7 + hash(i + 1)), 0, 0, sb * 3 + i);
  }
  sparks.instanceMatrix.needsUpdate = true;
  // light flashes
  fxLight.position.set(NX.x, NX.y + .3, NX.z + .6);
  fxLight.intensity = pulse(t, land, .03, .4) * 18 + pulse(t, s0, .03, .45) * 14 + pulse(t, T.approve, .03, .4) * 10 + up8(t);
}
const up8 = (t) => pulse(t, L[1] + .55, .05, .5) * 14;

// ---------------------------------------------------------------- props: the paywall card and padlocks
const CARD_HIT = V(.62, 1.42, .78);
const card = grp(scene);
const cardFace = new THREE.Mesh(rb(.96, .62, .04, .06, 3), phys(0xffffff, { roughness: .35, clearcoat: .6 }));
card.add(cardFace);
const cardFront = new THREE.Mesh(new THREE.PlaneGeometry(.92, .58), new THREE.MeshBasicMaterial({ toneMapped: false })); cardFront.position.z = .021; card.add(cardFront);
const locks = [];
for (let i = 0; i < 3; i++) {
  const lk = grp(card);
  lk.add(mesh(rb(.13, .11, .06, .02, 2), phys(0xffc24a, { metalness: .9, roughness: .25 })));
  const shk = mesh(new THREE.TorusGeometry(.04, .012, 8, 20, Math.PI), std(0xd8d8e0, { metalness: 1, roughness: .2 })); shk.position.y = .055; lk.add(shk);
  locks.push(lk);
}
function animCard(t) {
  const hit = T.free - .02;
  card.visible = t < hit;
  if (!card.visible) return;
  // bursts out of the phone, hangs in front of the human, then drifts toward NXT's bicep
  const burst = backOut(win(t, -.25, .35), 2.4);
  const from = V(-.75, 1.05, .9), hang = V(-.1, 1.32, 1.25);
  const p = from.clone().lerp(hang, burst);
  const drift = easeIO(win(t, L[1] + .2, hit));
  p.lerp(CARD_HIT, drift);
  card.position.copy(p).add(V(0, Math.sin(t * 2.4) * .025, 0));
  card.rotation.set(-.08 + Math.sin(t * 1.7) * .05, .35 - drift * .7 + Math.sin(t * 1.3) * .06, Math.sin(t * 2.1) * .04 + pulse(t, 1.1, .03, .25) * .06);
  card.scale.setScalar(Math.max(.01, burst * .8));
  locks.forEach((lk, i) => {
    const a = t * 2.2 + i * Math.PI * 2 / 3;
    lk.position.set(Math.cos(a) * .62, Math.sin(a) * .42, .1 + Math.sin(a * 2) * .05);
    lk.rotation.set(t * 2 + i, t * 3 + i, 0);
  });
  redLight.position.copy(card.position).add(V(0, 0, .3));
  redLight.intensity = 3 * burst * (1 - drift * .5);
}

// ---------------------------------------------------------------- the code hologram (Claude helped build it)
const codeG = grp(scene, NX.x - .1, 1.95, NX.z - .9);
const codeTexH = 1024;
let codeTex;
const codeWin = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.05), new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, color: new THREE.Color(1.6, 1.4, 2.2) }));
codeG.add(codeWin);
const codeFrame = new THREE.Mesh(new THREE.PlaneGeometry(1.56, 1.11), new THREE.MeshBasicMaterial({ color: new THREE.Color(VIOLET).multiplyScalar(.35), transparent: true, opacity: .5, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
codeFrame.position.z = -.01; codeG.add(codeFrame);
function animCode(t) {
  const a = T.claude - .15, z = L[2] + .2;
  codeG.visible = between(t, a, z);
  if (!codeG.visible) return;
  const k = easeOut(win(t, a, a + .3)) * (1 - win(t, z - .25, z));
  const flick = t - a < .3 ? (Math.sin((t - a) * 90) > 0 ? 1 : .35) : 1;
  codeG.scale.set(k, k * flick, 1);
  codeG.rotation.y = -.25 + Math.sin(t * .8) * .04;
  codeTex.offset.y = -((t - a) * .55 % 1);
  codeWin.material.opacity = .9 * k;
}

// ---------------------------------------------------------------- the central hologram slot: chips, key, goals, calendar, plate
const SLOT = V(.12, 1.2, .8);
const slot = grp(scene, SLOT.x, SLOT.y, SLOT.z); slot.rotation.y = -.04;
const holoBase = (c, k = 1) => new THREE.MeshBasicMaterial({ map: c, transparent: true, depthWrite: false, toneMapped: false, color: new THREE.Color(k, k, k) });
function textCard(w, h, tex, k = .9) {
  const g = new THREE.Group();
  const face = new THREE.Mesh(new THREE.PlaneGeometry(w, h), holoBase(tex, k)); g.add(face);
  const back = new THREE.Mesh(rb(w + .02, h + .02, .02, Math.min(.05, h / 2), 2), phys(0x1a1030, { roughness: .3, clearcoat: 1, transparent: true, opacity: .85 }));
  back.position.z = -.015; g.add(back);
  return g;
}
const chips3 = [], xs3 = [], goals = [], routine = [];
let keyCard, orb, orbGlow, cal, approvedStamp, plateG, plateLbl, cable;
function buildSlot() {
  // "subscription / ads / account" chips with the red X
  ["SUBSCRIPTION", "ADS", "ACCOUNT"].forEach((s, i) => {
    const c = textCard(.86, .2, chipTex(s, "#d9ccff", "rgba(123,47,251,.55)")); c.position.set(0, .26 - i * .25, 0); slot.add(c); chips3.push(c);
    const x = new THREE.Mesh(new THREE.PlaneGeometry(.26, .26), holoBase(xTex, 1.6)); x.position.set(.3, 0, .03); c.add(x); xs3.push(x);
  });
  // key card + orb + cable
  keyCard = textCard(.92, .5, keyTex, 1.1); slot.add(keyCard);
  orb = mesh(new THREE.SphereGeometry(.075, 32, 20), glow(LVIOLET, 2.2), false, false); scene.add(orb);
  orbGlow = new THREE.Mesh(new THREE.PlaneGeometry(.38, .38), new THREE.MeshBasicMaterial({ map: glowTex, color: new THREE.Color(VIOLET).multiplyScalar(.7), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
  orb.add(orbGlow);
  // goal chips
  [["4 DAYS", "🗓"], ["DUMBBELLS", "🏋"], ["BUILD MUSCLE", "💪"]].forEach(([s], i) => {
    const c = textCard(.8, .19, chipTex(s, "#f4f1fa", "rgba(63,214,155,.0)", "#3fd69b")); c.position.set(0, .25 - i * .24, 0); slot.add(c); goals.push(c);
  });
  // week calendar with four routine cards
  cal = new THREE.Group(); slot.add(cal);
  const calBoard = textCard(1.25, .62, calTex, 1.0); cal.add(calBoard);
  const days = [0, 1, 3, 4];
  days.forEach((d, i) => {
    const c = textCard(.15, .3, routineTex[i], 1.25); c.userData.x = -.625 + .09 + d * .1714 + .0; c.userData.day = d; cal.add(c); routine.push(c);
  });
  approvedStamp = new THREE.Mesh(new THREE.PlaneGeometry(.9, .3), holoBase(approvedTex, 1.5)); approvedStamp.position.set(0, -.02, .06); cal.add(approvedStamp);
  // the plate sliding onto a bar (+2.5 kg)
  plateG = new THREE.Group(); slot.add(plateG);
  const bar = mesh(new THREE.CylinderGeometry(.022, .022, 1.15, 16), std(0xc9c6d6, { metalness: 1, roughness: .2 })); bar.rotation.z = Math.PI / 2; plateG.add(bar);
  for (const s of [-1, 1]) {
    for (let j = 0; j < 2; j++) { const pl = mesh(new THREE.CylinderGeometry(.17 - j * .03, .17 - j * .03, .045, 32), phys(0x221a30, { roughness: .35, clearcoat: .8 })); pl.rotation.z = Math.PI / 2; pl.position.x = s * (.3 + j * .05); plateG.add(pl); }
  }
  const newPlate = mesh(new THREE.CylinderGeometry(.11, .11, .04, 32), phys(VIOLET, { roughness: .2, clearcoat: 1, emissive: 0x3a1080 })); newPlate.rotation.z = Math.PI / 2; plateG.add(newPlate); plateG.userData.plate = newPlate;
  plateLbl = new THREE.Mesh(new THREE.PlaneGeometry(.62, .2), holoBase(plusTex, 1.4)); plateLbl.position.set(.36, .3, 0); plateG.add(plateLbl);
}
function show(o, t, a, z, dur = .25) {
  const k = backOut(win(t, a, a + dur), 2) * (1 - easeIn(win(t, z - .2, z)));
  o.visible = k > .002; o.scale.setScalar(Math.max(.001, k)); return k;
}
function animSlot(t) {
  slot.position.y = SLOT.y + Math.sin(t * 1.4) * .02;
  // chips + X stamps on the three words
  chips3.forEach((c, i) => {
    const a = L[3] + .15 + i * .12, z = L[4] - .05;
    show(c, t, a, z + 1);
    const hit = T.x[i];
    const fall = Math.max(0, t - hit - .25);
    c.position.y = .26 - i * .25 - fall * fall * 3.2;
    c.rotation.z = fall * (i - 1 + .5) * 1.4;
    c.visible = c.visible && t < z;
    const xk = backOut(win(t, hit, hit + .14), 3);
    xs3[i].visible = t >= hit; xs3[i].scale.setScalar(Math.max(.01, 2.2 - 1.2 * xk));
  });
  // key card, orb travels from NXT into it
  show(keyCard, t, L[4] - .05, L[5] + .05);
  keyCard.rotation.y = Math.sin(t * 1.1) * .12;
  const plug = win(t, L[4] + .15, L[4] + .85);
  orb.visible = between(t, L[4] + .1, L[5]);
  const start = V(NX.x, NX.y + .1, NX.z + .3), end = V(SLOT.x + .3, SLOT.y + slot.position.y - SLOT.y - .03, SLOT.z + .04);
  const mid = start.clone().lerp(end, .5).add(V(0, .45, .2));
  const e = easeIO(plug);
  orb.position.set(lerp(lerp(start.x, mid.x, e), lerp(mid.x, end.x, e), e), lerp(lerp(start.y, mid.y, e), lerp(mid.y, end.y, e), e), lerp(lerp(start.z, mid.z, e), lerp(mid.z, end.z, e), e));
  orb.scale.setScalar(1 + pulse(t, L[4] + .85, .05, .4) * .6 + Math.sin(t * 9) * .05);
  keyCard.children[0].material.color.setScalar(.9 + pulse(t, L[4] + .85, .05, .6) * .6);
  // goal chips on the counted words
  goals.forEach((c, i) => { show(c, t, T.g[i] - .05, L[6] + .1); c.rotation.y = Math.sin(t * 1.3 + i) * .1; });
  // calendar: routine cards fly in on "plans your whole week", then the APPROVED stamp
  show(cal, t, L[6] - .05, L[7] + .1, .3);
  routine.forEach((c, i) => {
    const a = L[6] + .35 + i * .22, k = easeOut(win(t, a, a + .32));
    c.visible = t >= a;
    c.position.set(lerp(-1.4 + i * .9, c.userData.x, k), lerp(.9, -.07, k), lerp(.6, .03, k));
    c.rotation.set(0, (1 - k) * 2.4, (1 - k) * .6);
  });
  const sk = win(t, T.approve - .02, T.approve + .12);
  approvedStamp.visible = t >= T.approve - .02;
  approvedStamp.scale.setScalar(Math.max(.01, 2.4 - 1.4 * easeOut(sk)));
  approvedStamp.rotation.z = -.12;
  approvedStamp.material.opacity = sk;
  // the plate slides on when it "adds weight"
  show(plateG, t, T.demos - .1, L[8] + .05, .3);
  plateG.rotation.set(.1, -.35 + Math.sin(t * .9) * .12, 0);
  const pk = easeOut(win(t, T.ready - .25, T.ready + .1));
  plateG.userData.plate.position.x = lerp(1.1, .4, pk) + pulse(t, T.ready + .1, .03, .2) * -.01;
  plateG.userData.plate.visible = t > T.ready - .5;
  plateLbl.visible = t > T.ready + .05; plateLbl.scale.setScalar(Math.max(.01, backOut(win(t, T.ready + .05, T.ready + .3), 3)));
}

// ---------------------------------------------------------------- the hologram muscle map
const holo = grp(scene, .08, 0, -.45);
const holoMats = [];
function holoMat(color) {
  const m = new THREE.ShaderMaterial({
    uniforms: { uColor: { value: new THREE.Color(color) }, uTime: { value: 0 }, uAmt: { value: 0 }, uFill: { value: 0 } },
    vertexShader: `varying vec3 vN; varying vec3 vV; varying float vY;
      void main(){ vec4 wp = modelMatrix * vec4(position, 1.); vY = wp.y; vN = normalize(mat3(modelMatrix) * normal);
        vV = normalize(cameraPosition - wp.xyz); gl_Position = projectionMatrix * viewMatrix * wp; }`,
    fragmentShader: `uniform vec3 uColor; uniform float uTime, uAmt, uFill; varying vec3 vN; varying vec3 vV; varying float vY;
      void main(){
        float f = pow(1. - abs(dot(normalize(vN), normalize(vV))), 2.);
        float scan = .62 + .38 * step(.45, fract(vY * 42. - uTime * 1.6));
        float a = (f * 1.15 + .1 + uFill * .55) * scan * uAmt;
        gl_FragColor = vec4(uColor * (1.2 + uFill * 2.2) * a, a);
      }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  holoMats.push(m); return m;
}
const HG = {};
function buildHolo() {
  const base = LVIOLET;
  const part = (name, geo, x, y, z, sx = 1, sy = 1, sz = 1, rz = 0) => {
    HG[name] = HG[name] || holoMat(base);
    const m = new THREE.Mesh(geo, HG[name]); m.position.set(x, y, z); m.scale.set(sx, sy, sz); m.rotation.z = rz; holo.add(m); return m;
  };
  const S = (r) => new THREE.SphereGeometry(r, 28, 18), C = (r, h) => new THREE.CapsuleGeometry(r, h, 6, 18);
  part("head", S(.12), 0, 1.66, 0, .9, 1.1, 1);
  part("neck", C(.05, .08), 0, 1.5, 0);
  part("chest", S(.15), -.1, 1.33, .05, 1, .7, .55); part("chest", S(.15), .1, 1.33, .05, 1, .7, .55);
  part("abs", C(.12, .2), 0, 1.1, .02, 1.1, 1, .7);
  part("shoulders", S(.09), -.27, 1.42, 0, 1, .9, 1); part("shoulders", S(.09), .27, 1.42, 0, 1, .9, 1);
  part("arms", C(.065, .2), -.34, 1.2, 0, 1, 1, 1, -.15); part("arms", C(.065, .2), .34, 1.2, 0, 1, 1, 1, .15);
  part("arms", C(.05, .2), -.39, .92, .03, 1, 1, 1, -.08); part("arms", C(.05, .2), .39, .92, .03, 1, 1, 1, .08);
  part("hips", S(.16), 0, .88, 0, 1.15, .6, .8);
  part("legs", C(.095, .3), -.1, .58, 0, 1, 1, 1, .03); part("legs", C(.095, .3), .1, .58, 0, 1, 1, 1, -.03);
  part("legs", C(.07, .3), -.11, .2, 0, 1, 1, 1); part("legs", C(.07, .3), .11, .2, 0, 1, 1, 1);
  // pedestal + scanning ring
  const ped = new THREE.Mesh(new THREE.RingGeometry(.34, .42, 64), glow(LVIOLET, 2.6, { transparent: true, side: THREE.DoubleSide, depthWrite: false }));
  ped.rotation.x = -Math.PI / 2; ped.position.y = .012; holo.add(ped); HG.ped = ped;
  const disc = new THREE.Mesh(new THREE.CircleGeometry(.34, 48), new THREE.MeshBasicMaterial({ map: glowTex, color: new THREE.Color(VIOLET).multiplyScalar(.9), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
  disc.rotation.x = -Math.PI / 2; disc.position.y = .01; holo.add(disc); HG.disc = disc;
  const scanR = new THREE.Mesh(new THREE.TorusGeometry(.36, .006, 6, 64), glow(LILAC, 3)); scanR.rotation.x = Math.PI / 2; holo.add(scanR); HG.scan = scanR;
  // three state labels
  HG.labels = [["WORKED", GREEN], ["RECOVERING", AMBER], ["UNTRAINED", RED]].map(([s, c], i) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(.62, .16), holoBase(labelTex[i], 1.5)); holo.add(m); return m;
  });
}
const cA = new THREE.Color(LVIOLET), cG = new THREE.Color(GREEN), cAm = new THREE.Color(AMBER), cR = new THREE.Color(RED);
function animHolo(t) {
  const a = L[8] + .35, z = L[10] + .02;
  holo.visible = between(t, a, z);
  if (!holo.visible) return;
  const on = easeOut(win(t, a, a + .45)) * (1 - win(t, z - .4, z));
  const flick = t - a < .45 ? (Math.sin((t - a) * 70) > -.3 ? 1 : .2) : 1;
  holo.rotation.y = window.OG_COVER?.holoYaw ?? (t - a) * .35;
  const grow = (k, c, at) => { const w = easeOut(win(t, at, at + .25)); return [cA.clone().lerp(c, w), w]; };
  const set_ = (names, col, fill) => names.forEach((n) => { HG[n].uniforms.uColor.value.copy(col); HG[n].uniforms.uFill.value = fill; });
  for (const m of holoMats) { m.uniforms.uTime.value = t; m.uniforms.uAmt.value = on * flick * .85; m.uniforms.uColor.value.copy(cA); m.uniforms.uFill.value = 0; }
  const [cw, fw] = grow(0, cG, T.worked); set_(["chest", "arms", "abs"], cw, fw * .8);
  const [ca, fa] = grow(0, cAm, T.recovering); set_(["shoulders"], ca, fa * .8);
  const [cr, fr] = grow(0, cR, T.untrained);
  const beat = fr * (.6 + .4 * Math.abs(Math.sin((t - T.untrained) * 6)));
  set_(["legs", "hips"], cr, beat);
  if (t > T.untrained) HG.legs.uniforms.uAmt.value = on * (1 + beat * .6);
  HG.scan.position.y = .05 + ((t - a) * .9 % 1.75);
  HG.ped.material.opacity = on; HG.disc.material.opacity = on;
  holo.scale.set(1, Math.max(.01, on), 1);
  // labels pop beside the body, facing the camera
  const at = [T.worked, T.recovering, T.untrained], ys = [1.32, 1.5, .5], xs = [-.62, .64, -.6];
  HG.labels.forEach((m, i) => {
    const k = backOut(win(t, at[i], at[i] + .2), 2.5) * on;
    m.visible = false; m.scale.setScalar(Math.max(.01, k));
    const ang = -holo.rotation.y;
    m.position.set(Math.cos(ang) * xs[i], ys[i], -Math.sin(ang) * xs[i]);
    m.rotation.y = ang;
  });
}

// ---------------------------------------------------------------- textures that need the fonts
let xTex, keyTex, calTex, approvedTex, plusTex;
const routineTex = [], labelTex = [];
function chipTex(s, fg, bg, dot) {
  return canvasTex(860, 200, (g, w, h) => {
    rr(g, 6, 6, w - 12, h - 12, 90); g.fillStyle = bg; g.fill(); g.lineWidth = 6; g.strokeStyle = dot || "#a98bff"; g.stroke();
    g.fillStyle = fg; g.font = "800 78px Poppins"; g.textAlign = "center"; g.textBaseline = "middle";
    if (dot) { g.fillStyle = dot; g.beginPath(); g.arc(90, h / 2, 22, 0, 7); g.fill(); g.fillStyle = fg; g.fillText(s, w / 2 + 30, h / 2 + 6); }
    else g.fillText(s, w / 2, h / 2 + 6);
  });
}
function drawTextures() {
  cardFront.material.map = canvasTex(920, 580, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#ff4458"); gr.addColorStop(1, "#b0122a");
    rr(g, 0, 0, w, h, 50); g.fillStyle = gr; g.fill();
    g.fillStyle = "rgba(255,255,255,.18)"; rr(g, 40, 40, 200, 56, 28); g.fill();
    g.fillStyle = "#fff"; g.font = "700 30px JBMono"; g.textAlign = "left"; g.fillText("FitPro", 72, 79);
    g.font = "800 104px Poppins"; g.fillText("UPGRADE", 52, 250); g.fillText("TO PRO", 52, 362);
    g.font = "600 40px Poppins"; g.fillStyle = "rgba(255,255,255,.9)"; g.fillText("Your free trial has ended.", 56, 440);
    rr(g, 52, 478, 330, 68, 34); g.fillStyle = "#fff"; g.fill(); g.fillStyle = "#c0142d"; g.font = "800 34px Poppins"; g.fillText("SUBSCRIBE", 104, 524);
    g.font = "120px sans-serif"; g.fillText("🔒", 690, 250);
  });
  cardFront.material.needsUpdate = true;
  codeTex = canvasTex(1024, codeTexH, (g, w, h) => {
    g.fillStyle = "rgba(10,4,24,.6)"; g.fillRect(0, 0, w, h);
    const lines = ["function planWeek(goal) {", "  const days = goal.daysPerWeek;", "  const split = pickSplit(days);", "  return split.map((d) => ({", "    day: d.name,", "    exercises: choose(d.muscles),", "    sets: 3, reps: [8, 12],", "  }));", "}", "", "export function nextLoad(last) {", "  if (last.missedReps) return last.kg;", "  return last.kg + 2.5;", "}", "", "test(\"adds weight when ready\", () => {", "  expect(nextLoad(hit)).toBe(15);", "});", "", "// muscle map: volume, recovery", "const state = mapMuscles(log);", "render(state);"];
    g.font = "600 34px JBMono"; g.textBaseline = "top";
    const col = ["#d9ccff", "#a98bff", "#3fd69b", "#ffc24a", "#f4f1fa"];
    lines.forEach((l, i) => {
      g.fillStyle = "rgba(169,139,255,.35)"; g.fillText(String(i + 1).padStart(2, " "), 22, 20 + i * 46);
      g.fillStyle = col[(i * 7 + l.length) % col.length]; g.fillText(l, 96, 20 + i * 46);
    });
    g.fillStyle = "rgba(255,255,255,.05)"; for (let y = 0; y < h; y += 6) g.fillRect(0, y, w, 2);
  });
  codeTex.wrapT = THREE.RepeatWrapping; codeTex.repeat.set(1, .75);
  codeWin.material.map = codeTex; codeWin.material.needsUpdate = true;
  xTex = canvasTex(256, 256, (g, w) => { g.strokeStyle = "#ff4a5e"; g.lineWidth = 34; g.lineCap = "round"; g.beginPath(); g.moveTo(50, 50); g.lineTo(w - 50, w - 50); g.moveTo(w - 50, 50); g.lineTo(50, w - 50); g.stroke(); });
  keyTex = canvasTex(920, 500, (g, w, h) => {
    rr(g, 6, 6, w - 12, h - 12, 46); g.fillStyle = "rgba(40,18,84,.9)"; g.fill(); g.lineWidth = 6; g.strokeStyle = "#a98bff"; g.stroke();
    // generic key icon
    g.strokeStyle = "#ffc24a"; g.lineWidth = 22; g.beginPath(); g.arc(170, 200, 62, 0, 7); g.stroke();
    g.beginPath(); g.moveTo(232, 200); g.lineTo(400, 200); g.moveTo(350, 200); g.lineTo(350, 250); g.moveTo(395, 200); g.lineTo(395, 240); g.stroke();
    g.fillStyle = "#fff"; g.font = "800 66px Poppins"; g.fillText("your own", 450, 190); g.fillText("Claude key", 450, 265);
    g.fillStyle = "#a98bff"; g.font = "700 34px JBMono"; g.fillText("AI COACH · PROVIDER", 110, 400);
    g.fillStyle = "#3fd69b"; g.beginPath(); g.arc(800, 388, 16, 0, 7); g.fill();
  });
  calTex = canvasTex(1250, 620, (g, w, h) => {
    rr(g, 6, 6, w - 12, h - 12, 40); g.fillStyle = "rgba(24,12,52,.92)"; g.fill(); g.lineWidth = 6; g.strokeStyle = "#a98bff"; g.stroke();
    g.fillStyle = "#d9ccff"; g.font = "800 40px JBMono"; g.textAlign = "center";
    ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"].forEach((d, i) => {
      g.fillText(d, 90 + i * 171.4, 92);
      g.strokeStyle = "rgba(169,139,255,.3)"; g.lineWidth = 3; rr(g, 20 + i * 171.4, 130, 140, 440, 20); g.stroke();
    });
  });
  ["UPPER", "LOWER", "UPPER", "LOWER"].forEach((s, i) => routineTex.push(canvasTex(150, 300, (g, w, h) => {
    rr(g, 4, 4, w - 8, h - 8, 18); g.fillStyle = i % 2 ? "#7b2ffb" : "#a98bff"; g.fill();
    g.save(); g.translate(w / 2, h / 2); g.rotate(-Math.PI / 2); g.fillStyle = "#fff"; g.font = "800 46px Poppins"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(s, 0, 4); g.restore();
  })));
  approvedTex = canvasTex(900, 300, (g, w, h) => {
    g.strokeStyle = "#3fd69b"; g.lineWidth = 16; rr(g, 14, 14, w - 28, h - 28, 30); g.stroke();
    g.fillStyle = "#3fd69b"; g.font = "800 132px Poppins"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("✓ APPROVED", w / 2, h / 2 + 8);
  });
  plusTex = canvasTex(620, 200, (g, w, h) => {
    rr(g, 6, 6, w - 12, h - 12, 90); g.fillStyle = "#3fd69b"; g.fill();
    g.fillStyle = "#07050d"; g.font = "800 104px Poppins"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("+2.5 kg", w / 2, h / 2 + 6);
  });
  [["WORKED", "#3fd69b"], ["RECOVERING", "#ffc24a"], ["UNTRAINED", "#ff6b6b"]].forEach(([s, c]) => labelTex.push(canvasTex(620, 160, (g, w, h) => {
    rr(g, 6, 6, w - 12, h - 12, 80); g.fillStyle = "rgba(7,5,13,.75)"; g.fill(); g.lineWidth = 6; g.strokeStyle = c; g.stroke();
    g.fillStyle = c; g.beginPath(); g.arc(70, h / 2, 20, 0, 7); g.fill();
    g.font = "800 64px Poppins"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(s, w / 2 + 28, h / 2 + 4);
  })));
  drawEyes();
  buildSlot();
  buildHolo();
}

// ---------------------------------------------------------------- camera
// each shot: [pos, look, fov, shift]; shift pushes the image down so the characters sit under the UI panel
const SHIFT = .2;
function panelUp(t) {
  const fold = (a, b) => easeIO(win(t, a, b));
  if (t < L[3]) return 0;                       // the hook and the gasp are full-bleed 3D (no panel)
  if (t < L[8]) return fold(L[3], L[3] + .35);
  if (t < T.gym) return 1 - fold(L[8] - .05, L[8] + .3);
  return .85;
}
function shot(t) {
  const d = (a, b, k) => a.map((x, i) => lerp(x, b[i], k));
  if (t < L[1] - .2) {
    const k = easeIO(win(t, 0, L[1]));
    const pan = easeIO(win(t, L[1] - 1.25, L[1] - .25));   // swing toward the beam where NXT is about to land
    return [d(d([-.15, 1.42, 4.8], [-.3, 1.36, 4.2], k), [.1, 1.5, 5.0], pan), d([-.55, 1.12, .4], [.35, 1.3, .4], pan), 36 + pan * 6];
  }
  if (t < T.free + .25) {                       // HERO: the slam and the power-up, wide and low
    const k = easeOut(win(t, L[1] - .2, T.free + .25));
    const pk = easeOut(win(t, T.free - .25, T.free + .1));
    return [d(d([-.1, .95, 6.4], [.3, 1.0, 5.7], k), [.62, 1.32, 4.5], pk), d([.35, 1.25, .4], [.98, 1.5, .5], pk), 40];
  }
  if (t < L[2]) {                               // code hologram behind NXT
    const k = easeIO(win(t, T.free + .25, L[2]));
    return [d([.72, 1.42, 4.9], [.85, 1.5, 4.5], k), [1.14, 1.58, -.2], 40];
  }
  if (t < L[3]) {                               // whip-pan punch-in on the human
    const k = easeOut(win(t, L[2], L[3]));
    const whip = (1 - easeOut(win(t, L[2], L[2] + .16))) * 1.6;
    return [d([-.3, 1.62, 4.6], [-.36, 1.6, 4.25], k), [-.78 + whip, 1.72, .4], 32];
  }
  if (t < L[8]) {                               // two-shot under the panel, a new angle per line
    const bases = { 3: [[.25, 1.55, 6.6], [.1, 1.2, .3]], 4: [[.55, 1.5, 6.3], [.15, 1.2, .3]], 5: [[-.25, 1.45, 5.9], [-.1, 1.2, .3]],
      6: [[.35, 1.6, 6.2], [.1, 1.25, .3]], 7: [[.05, 1.3, 6.0], [.08, 1.18, .3]] };
    let i = 3; for (let j = 3; j <= 7; j++) if (t >= L[j]) i = j;
    const [p, q] = bases[i];
    const k = win(t, L[i], i < 7 ? L[i + 1] : L[8]);
    return [[p[0] + k * .2, p[1] + Math.sin(t * .6) * .03, p[2] - k * .25], q, 36];
  }
  if (t < L[9]) {                               // arc toward the hologram
    const k = easeIO(win(t, L[8], L[9]));
    return [d([.0, 1.45, 5.8], [-1.1, 1.45, 4.2], k), d([.0, 1.15, .1], [.08, 1.05, -.45], k), 38];
  }
  if (t < T.legs) {                             // HERO orbit around the muscle map
    const k = easeIO(win(t, L[9], T.legs));
    const a = lerp(-.55, .22, k), r = lerp(3.6, 3.2, k);
    return [[.08 + Math.sin(a) * r, lerp(1.7, 1.35, k), -.45 + Math.cos(a) * r], [.08, lerp(1.1, .85, k), -.45], 40];
  }
  if (t < L[10]) {                              // NXT points at the legs, then flexes its own tiny ones
    const k = easeOut(win(t, T.legs, L[10]));
    return [d([.45, 1.1, 4.5], [.55, 1.05, 4.1], k), [.9, 1.0, .3], 38];
  }
  if (t < L[11]) {                              // the human looks down: "Fair."
    const k = easeOut(win(t, L[10], L[11]));
    return [d([-.4, 1.25, 3.1], [-.45, 1.22, 2.8], k), [-.9, .95, .35], 36];
  }
  const k = easeIO(win(t, L[11], T.end));       // wide two-shot for the CTA
  return [d([.1, 1.5, 5.8], [.1, 1.6, 6.8], k), [.1, 1.25, .3], 38];
}
function shake(t) { return pulse(t, L[1] - .12, .02, .35) * 1 + pulse(t, T.free - .02, .02, .4) * .8 + pulse(t, T.approve, .02, .25) * .4; }

function renderAt(t) {
  animHuman(t); animNxt(t); animFx(t); animCard(t); animCode(t); animSlot(t); animHolo(t);
  const [p, q, fov] = shot(t);
  const s = shake(t);
  camera.position.set(p[0] + Math.sin(t * 91) * .04 * s + Math.sin(t * .37) * .03, p[1] + Math.cos(t * 77) * .04 * s, p[2]);
  camera.lookAt(q[0], q[1] + Math.cos(t * .29) * .02, q[2]);
  camera.fov = fov - pulse(t, T.free - .02, .04, .5) * 4;
  // lens shift: content moves down under the panel
  const sh = SHIFT * panelUp(t);
  camera.setViewOffset(W, H, 0, -sh * H, W, H);
  camera.updateProjectionMatrix();
  grade.uniforms.uTime.value = Math.round(t * 30) / 30;
  grade.uniforms.uChroma.value = s * 1.2 + pulse(t, L[2], .02, .2);
  bloom.strength = .38 + pulse(t, T.free - .02, .03, .5) * .25 + (between(t, L[9], L[11]) ? .12 : 0);
  key.intensity = 90 * (between(t, L[9], L[10] + .4) ? .55 : 1);
  composer.render();
}

// ---------------------------------------------------------------- cover still (cover.html sets window.OG_COVER)
function renderCover(c) {
  renderAt(c.t);
  camera.position.set(...c.cam); camera.lookAt(...c.look); camera.fov = c.fov;
  camera.setViewOffset(W, H, 0, -(c.shift || 0) * H, W, H); camera.updateProjectionMatrix();
  composer.render();
}

const ready = (async () => {
  await Promise.all(["800 90px Poppins", "700 30px Poppins", "700 34px JBMono"].map((f) => document.fonts.load(f)));
  drawTextures();
  renderer.compile(scene, camera);
  if (window.OG_COVER) { renderCover(window.OG_COVER); window.__coverDone = true; return; }
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["opengym"] = ready;
window.addEventListener("hf-seek", (e) => { if (codeTex && !window.OG_COVER) renderAt(e.detail.time); });
