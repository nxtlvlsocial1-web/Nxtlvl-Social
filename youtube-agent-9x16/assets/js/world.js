// YouTube Agent Skill reel: the 3D world. Everything is a pure function of time t (seconds), rendered on HyperFrames'
// hf-seek. Story on one energy curve: BAD CHAOS (a creator at 3 AM, notifications swarming his desk), ORDER (Claude
// bursts out of the monitor in a producer headset, splits into eleven mini-Claudes, and five of them each switch off
// one fire: the blank script, the empty thumbnail, the messy timeline, the comment flood, the empty calendar), CALM
// (a clean studio, the creator asleep, Claude sipping tea; the whisper), GOOD CHAOS (the walls drop into a neon city
// of videos; the tallest one is X-rayed and a new one rises in the creator's voice), LANDING (sunrise, he wakes, one
// link to paste) and the CTA. Cue times come from the voice (window.YT_T, written by build/generate.py).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const T = window.YT_T;
const ENV = window.YT_ENV;
const L = T.l, E = T.e;
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
const BG_STUDIO = new THREE.Color(0x0b0710), BG_CITY = new THREE.Color(0x05030c);
scene.background = BG_STUDIO.clone();
scene.fog = new THREE.FogExp2(0x120a14, .02);
const camera = new THREE.PerspectiveCamera(38, W / H, .05, 200);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
scene.environmentIntensity = .35;

// ---------------------------------------------------------------- post: bloom, then grain / vignette / chroma / flash
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(1);
composer.setSize(W, H);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .45, .45, .88);
composer.addPass(bloom);
composer.addPass(new OutputPass());
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uGrain: { value: .05 }, uVig: { value: .6 }, uChroma: { value: 0 },
    uTint: { value: new THREE.Vector3(1, 1, 1) }, uBlack: { value: 0 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uGrain, uVig, uChroma, uBlack; uniform vec3 uTint; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main(){
      vec2 c = vUv - .5; vec2 off = c * uChroma * .02;
      vec3 col = vec3(texture2D(tDiffuse, vUv + off).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - off).b);
      col *= uTint;
      col += (h(floor(vUv * vec2(1080., 1920.)) + fract(uTime * 7.13) * 97.) - .5) * uGrain;
      vec2 v = c * vec2(1., .78);
      col *= 1. - uVig * dot(v, v) * 1.5;
      col *= 1. - uBlack;
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
const lerpV = (a, b, k) => a.map((x, i) => lerp(x, b[i], k));
function envAt(who, t) { const a = ENV[who]; const i = clamp(t * ENV.fps, 0, a.length - 1); const i0 = Math.floor(i); return lerp(a[i0], a[Math.min(a.length - 1, i0 + 1)], i - i0); }
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
const add = (c, k = 1, o = {}) => new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), transparent: true, depthWrite: false,
  blending: THREE.AdditiveBlending, toneMapped: false, ...o });
function halo(size, color, k = .4) { return new THREE.Mesh(new THREE.PlaneGeometry(size, size), add(color, k, { map: glowTex })); }
// a flat card showing a canvas texture, with a thin glossy back
function card(w, h, k = 1, back = 0x1a1424) {
  const g = new THREE.Group();
  const face = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false, color: new THREE.Color(k, k, k) }));
  g.add(face);
  if (back !== null) { const b = mesh(rb(w + .02, h + .02, .02, Math.min(.04, h / 2), 2), phys(back, { roughness: .35, clearcoat: 1 }), false, false); b.position.z = -.013; g.add(b); }
  g.userData.face = face;
  return g;
}

// palette
const CORAL = 0xd97757, CORAL_L = 0xf0a07c, CREAM = 0xf6efe4, VIOLET = 0x8b5cf6, CYAN = 0x38d6f5, GOLD = 0xffc24a,
  RED = 0xff3b46, GREEN = 0x3fd69b, AMBER = 0xffb46b, PINK = 0xff5fa2;

// ---------------------------------------------------------------- lights
const hemi = new THREE.HemisphereLight(0x9a8ad8, 0x150c18, .35); scene.add(hemi);
const key = new THREE.SpotLight(0xffb46b, 70, 20, .6, .55, 1.6);
key.position.set(2.6, 4.8, 3.2); key.target.position.set(0, 1, -1.1);
key.castShadow = true; key.shadow.mapSize.set(1024, 1024); key.shadow.bias = -.0004; key.shadow.normalBias = .02;
scene.add(key, key.target);
const rim = new THREE.SpotLight(VIOLET, 40, 18, .7, .6, 1.4); rim.position.set(-2.4, 3.8, -3.2); rim.target.position.set(0, 1.2, -1.4); scene.add(rim, rim.target);
const alarm = new THREE.PointLight(RED, 0, 9, 1.4); alarm.position.set(0, 2.6, .4); scene.add(alarm);              // the 3 AM red
const screenLight = new THREE.PointLight(0x9fc4ff, 3, 4, 1.6); screenLight.position.set(-.6, 1.3, -.8); scene.add(screenLight);
const coralLight = new THREE.PointLight(CORAL, 0, 5, 1.5); scene.add(coralLight);                                  // follows Claude
const fx = new THREE.PointLight(0xffffff, 0, 7, 1.4); scene.add(fx);                                               // flashes

// ---------------------------------------------------------------- the studio (3 AM bedroom creator setup)
const studio = grp(scene);
const floorM = std(0x1a1218, { roughness: .6 });
const floor = mesh(new THREE.PlaneGeometry(14, 14), floorM, false, true); floor.rotation.x = -Math.PI / 2; studio.add(floor);
const rug = mesh(new THREE.CircleGeometry(1.6, 48), std(0x2b1d2e, { roughness: .95 }), false, true); rug.rotation.x = -Math.PI / 2; rug.position.set(.1, .005, -.9); studio.add(rug);
const wallM = std(0x1d1520, { roughness: .92 });
const backW = mesh(new THREE.PlaneGeometry(14, 8), wallM, false, true); backW.position.set(0, 4, -2.6); studio.add(backW);
const leftW = mesh(new THREE.PlaneGeometry(10, 8), wallM, false, true); leftW.rotation.y = Math.PI / 2; leftW.position.set(-2.9, 4, 1); studio.add(leftW);
// acoustic foam: a grid of wedges on the back wall
{
  const foamM = std(0x241a2b, { roughness: 1 });
  const geo = rb(.26, .26, .06, .02, 2);
  for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) {
    const f = mesh(geo, foamM, false, true); f.position.set(-2.35 + c * .29, 1.75 + r * .29, -2.57); f.rotation.z = (r + c) % 2 ? 0 : Math.PI / 2; studio.add(f);
  }
}
// LED strip along the top of the back wall: its colour carries the mood (red chaos, warm calm, neon, sunrise)
const ledM = glow(RED, 2.5);
const led = mesh(new THREE.BoxGeometry(9, .03, .03), ledM, false, false); led.position.set(0, 3.15, -2.56); studio.add(led);
const ledHalo = new THREE.Mesh(new THREE.PlaneGeometry(9, 1.6), add(RED, .25, { map: glowTex })); ledHalo.position.set(0, 3.0, -2.55); studio.add(ledHalo);
// window with a city at night (and a sunrise for the landing)
const winG = grp(studio, 1.55, 2.0, -2.585);
const skyNight = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.3), new THREE.MeshBasicMaterial({ color: 0x0a0d2a })); winG.add(skyNight);
const skyDawn = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.3), new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, toneMapped: false }));
skyDawn.position.z = .002; winG.add(skyDawn);
for (const [w, h, x, y] of [[1.62, .07, 0, .68], [1.62, .07, 0, -.68], [.07, 1.42, .78, 0], [.07, 1.42, -.78, 0], [.04, 1.3, 0, 0]]) {
  const f = mesh(new THREE.BoxGeometry(w, h, .06), std(0x120c16, { roughness: .5 })); f.position.set(x, y, .03); winG.add(f);
}
const bokeh = [];
for (let i = 0; i < 46; i++) {
  const s = .04 + hash(i + 3) * .12;
  const b = new THREE.Mesh(new THREE.PlaneGeometry(s, s), add([AMBER, 0xffd27a, 0xff8a5c, 0x7fd0ff, VIOLET, 0xfff1c8][i % 6], .6 + hash(i + 9) * 1.2, { map: glowTex }));
  b.position.set((hash(i) - .5) * 1.4, -.62 + Math.pow(hash(i + 5), 1.6) * 1.1, .004); winG.add(b); bokeh.push(b);
}
// wall clock stuck at 3 AM
const clockG = grp(studio, -.55, 2.55, -2.57);
clockG.add(mesh(new THREE.CylinderGeometry(.2, .2, .04, 32).rotateX(Math.PI / 2), std(0xf2eee8, { roughness: .4 })));
clockG.add(at(mesh(new THREE.TorusGeometry(.2, .018, 8, 32), std(0x2a2230, { metalness: .5, roughness: .3 })), 0, 0, .01));
const hourH = grp(clockG, 0, 0, .03), minH = grp(clockG, 0, 0, .035);
hourH.add(at(mesh(new THREE.BoxGeometry(.018, .1, .01), std(0x15101a)), 0, .05, 0));
minH.add(at(mesh(new THREE.BoxGeometry(.012, .15, .01), std(0x15101a)), 0, .075, 0));
// shelf with props
const shelf = mesh(rb(1.0, .04, .26, .01, 2), std(0x2a1e30)); shelf.position.set(-1.9, 1.35, -2.46); studio.add(shelf);
for (let i = 0; i < 5; i++) {
  const b = mesh(rb(.06, .24 + hash(i) * .08, .18, .01, 1), std([0x7b2ffb, 0xd97757, 0xf6efe4, 0x38d6f5, 0xffc24a][i], { roughness: .7 }));
  b.position.set(-2.3 + i * .08, 1.49 + hash(i) * .04, -2.46); studio.add(b);
}
const award = mesh(new THREE.CylinderGeometry(.06, .08, .22, 16), std(0xd7d9e0, { metalness: 1, roughness: .2 })); award.position.set(-1.6, 1.48, -2.46); studio.add(award);
// desk
const desk = grp(studio, .05, 0, -1.15);
desk.add(at(mesh(rb(2.3, .06, .8, .02, 2), std(0x2a2024, { roughness: .45 })), 0, .78, 0));
for (const [x, z] of [[-1.05, -.3], [1.05, -.3], [-1.05, .3], [1.05, .3]]) desk.add(at(mesh(new THREE.CylinderGeometry(.025, .025, .76, 10), std(0x111015, { metalness: .8, roughness: .3 })), x, .38, z));
// big monitor (the chaos screen; Claude bursts out of it)
const monG = grp(desk, -.82, 1.25, -.18); monG.rotation.y = .5;
monG.add(mesh(rb(1.18, .7, .05, .02, 2), std(0x0d0c10, { roughness: .35, metalness: .3 })));
const monScreen = new THREE.Mesh(new THREE.PlaneGeometry(1.1, .62), new THREE.MeshBasicMaterial({ toneMapped: false })); monScreen.position.z = .027; monG.add(monScreen);
monG.add(at(mesh(new THREE.CylinderGeometry(.03, .03, .4, 10), std(0x111015, { metalness: .8 })), 0, -.42, -.05));
monG.add(at(mesh(rb(.34, .02, .2, .01, 1), std(0x111015, { metalness: .8 })), 0, -.46, -.05));
// laptop (screen faces the creator)
const lapG = grp(desk, .25, .81, .05); lapG.rotation.y = Math.PI;
lapG.add(mesh(rb(.5, .02, .34, .01, 2), std(0x9b9aa3, { metalness: .9, roughness: .3 })));
const lapLid = grp(lapG, 0, .01, .16); lapLid.rotation.x = -1.9;
lapLid.add(at(mesh(rb(.5, .34, .015, .01, 2), std(0x9b9aa3, { metalness: .9, roughness: .3 })), 0, .17, 0));
const lapScreen = new THREE.Mesh(new THREE.PlaneGeometry(.46, .3), glow(0x9fc4ff, 1.2)); lapScreen.position.set(0, .17, .009); lapLid.add(lapScreen);
// desk clutter: mugs, energy cans, a phone, a mic on a boom
const mugs = [];
for (const [x, z, c] of [[.85, .1, 0xf6efe4], [.98, -.12, 0xd97757], [-.2, .25, 0x2b2b33]]) {
  const m = grp(desk, x, .81, z);
  m.add(at(mesh(new THREE.CylinderGeometry(.045, .04, .1, 16), std(c, { roughness: .4 })), 0, .05, 0));
  m.add(at(mesh(new THREE.TorusGeometry(.03, .009, 8, 16), std(c, { roughness: .4 })), .05, .05, 0));
  mugs.push(m);
}
for (const [x, z, r] of [[.62, .28, 0], [.7, .22, 1.2]]) {
  const c = mesh(new THREE.CylinderGeometry(.033, .033, .13, 14), std(0x38d6f5, { metalness: .7, roughness: .3 })); c.position.set(x, .87, z); c.rotation.z = r * .0; desk.add(c);
}
const phoneG = grp(desk, -.25, .79, .22); phoneG.rotation.y = -.4;
phoneG.add(mesh(rb(.09, .012, .17, .01, 2), std(0x111015, { roughness: .3 })));
const phoneScreen = new THREE.Mesh(new THREE.PlaneGeometry(.078, .155), glow(RED, 2)); phoneScreen.rotation.x = -Math.PI / 2; phoneScreen.position.y = .007; phoneG.add(phoneScreen);
const micG = grp(desk, .75, .81, -.3);
micG.add(at(mesh(new THREE.CylinderGeometry(.012, .012, .5, 8), std(0x111015, { metalness: .8 })), 0, .25, 0));
micG.add(at(mesh(new THREE.CapsuleGeometry(.04, .09, 4, 12), std(0x24242c, { metalness: .6, roughness: .35 })), -.05, .55, .06));
// ring light and a camera on a tripod (the creator setup)
const ringG = grp(studio, 1.55, 1.55, -1.25); ringG.rotation.y = -.6;
const ringM = glow(0xfff4e8, 1.6);
ringG.add(mesh(new THREE.TorusGeometry(.3, .025, 12, 48), ringM, false, false));
ringG.add(at(mesh(new THREE.CylinderGeometry(.012, .012, 1.55, 8), std(0x111015, { metalness: .8 })), 0, -.8, -.02));
const camG = grp(studio, 1.25, 1.15, -.3); camG.rotation.y = -2.4;
camG.add(mesh(rb(.18, .12, .1, .02, 2), std(0x15141a, { roughness: .4 })));
camG.add(at(mesh(new THREE.CylinderGeometry(.035, .04, .1, 16).rotateX(Math.PI / 2), std(0x0a0a0d, { roughness: .2, metalness: .6 })), 0, 0, .09));
const recDot = mesh(new THREE.SphereGeometry(.01, 8, 6), glow(RED, 3)); recDot.position.set(.06, .045, .052); camG.add(recDot);
for (const a of [0, 2.1, 4.2]) { const l = mesh(new THREE.CylinderGeometry(.008, .008, 1.2, 6), std(0x111015, { metalness: .8 })); l.position.set(Math.sin(a) * .18, -.6, Math.cos(a) * .18); l.rotation.set(Math.cos(a) * .15, 0, -Math.sin(a) * .15); camG.add(l); }
// chair
const chair = grp(studio, .2, 0, -1.85);
chair.add(at(mesh(rb(.55, .08, .5, .04, 2), std(0x1c1a22, { roughness: .6 })), 0, .5, 0));
chair.add(at(mesh(rb(.55, .8, .08, .05, 2), std(0x1c1a22, { roughness: .6 })), 0, .95, -.26));
chair.add(at(mesh(rb(.4, .2, .09, .04, 2), std(CORAL, { roughness: .5 })), 0, 1.05, -.21));
chair.add(at(mesh(new THREE.CylinderGeometry(.03, .03, .45, 10), std(0x111015, { metalness: .8 })), 0, .25, 0));
// plant
const plant = grp(studio, -2.3, 0, -1.9);
plant.add(at(mesh(new THREE.CylinderGeometry(.2, .16, .4, 20), std(0xb4613e, { roughness: .8 })), 0, .2, 0));
for (let i = 0; i < 9; i++) {
  const l = mesh(new THREE.SphereGeometry(.42, 12, 8), std(0x1f5a35, { roughness: .55, side: THREE.DoubleSide })); l.scale.set(.11, .5 + hash(i) * .3, .03);
  const a = i / 9 * Math.PI * 2; l.position.set(Math.cos(a) * .1, .7 + hash(i + 2) * .2, Math.sin(a) * .1); l.rotation.set(Math.sin(a) * .7, 0, -Math.cos(a) * .7); plant.add(l);
}

// ---------------------------------------------------------------- the creator (stylized young guy, grey hoodie, behind the desk)
const SKIN = 0xa8694a, HOOD = 0x8f9097, PANTS = 0x23263a, HAIR = 0x0e0c0d;
function human() {
  const root = grp(scene, .2, 0, -1.78);
  const hips = grp(root, 0, .62, 0);
  const pantsMat = std(PANTS, { roughness: .75 }), hoodMat = std(HOOD, { roughness: .88 }), skinMat = std(SKIN, { roughness: .55 });
  hips.add(mesh(rb(.46, .22, .36, .1, 3), pantsMat));
  for (const s of [-1, 1]) {
    const hip = grp(hips, s * .12, -.02, .02); hip.rotation.set(-1.42, s * -.06, 0);
    hip.add(at(mesh(rb(.19, .46, .21, .09, 3), pantsMat), 0, -.2, 0));
    const knee = grp(hip, 0, -.43, 0); knee.rotation.x = 1.5;
    knee.add(at(mesh(rb(.165, .46, .175, .075, 3), pantsMat), 0, -.21, 0));
  }
  const spine = grp(hips, 0, .06, 0);
  spine.add(at(mesh(rb(.64, .6, .4, .17, 4), hoodMat), 0, .3, 0));
  spine.add(at(mesh(rb(.62, .08, .39, .04, 2), std(0x7f8087, { roughness: .9 })), 0, .03, 0));
  spine.add(at(mesh(rb(.34, .16, .04, .03, 2), std(0x85868d, { roughness: .9 })), 0, .16, .19));
  const hoodRing = mesh(new THREE.TorusGeometry(.16, .065, 10, 24), hoodMat); hoodRing.position.set(0, .6, -.06); hoodRing.rotation.x = Math.PI / 2 - .5; spine.add(hoodRing);
  for (const s of [-1, 1]) spine.add(at(mesh(new THREE.CylinderGeometry(.008, .008, .16, 6), std(0xf4f1fa)), s * .05, .5, .2));
  const neck = grp(spine, 0, .6, 0);
  neck.add(at(mesh(new THREE.CylinderGeometry(.065, .07, .12, 12), skinMat), 0, .03, 0));
  const head = grp(neck, 0, .07, .01);
  const skull = mesh(new THREE.SphereGeometry(.19, 28, 22), skinMat); skull.scale.set(.95, 1.08, 1); skull.position.y = .17; head.add(skull);
  const hair = mesh(new THREE.SphereGeometry(.2, 28, 16, 0, Math.PI * 2, 0, Math.PI * .52), std(HAIR, { roughness: .8 }));
  hair.scale.set(.98, 1.06, 1.04); hair.position.set(0, .2, -.02); hair.rotation.x = -.42; head.add(hair);
  for (let i = 0; i < 5; i++) { const tuft = mesh(new THREE.SphereGeometry(.05, 10, 8), std(HAIR, { roughness: .8 })); tuft.scale.set(1, .55, 1); tuft.position.set((i - 2) * .06, .335 - Math.abs(i - 2) * .012, .1); tuft.rotation.x = .4; head.add(tuft); }
  for (const s of [-1, 1]) { const ear = mesh(new THREE.SphereGeometry(.04, 10, 8), skinMat); ear.scale.set(.5, 1, .8); ear.position.set(s * .18, .16, 0); head.add(ear); }
  head.add(at(mesh(new THREE.SphereGeometry(.026, 10, 8), std(0x95593c)), 0, .15, .19));
  // headphones round his neck (creator detail)
  const hp = mesh(new THREE.TorusGeometry(.16, .02, 8, 24, Math.PI), std(0x1a1a22, { roughness: .4 })); hp.position.set(0, .52, .02); hp.rotation.set(Math.PI / 2 + .3, 0, 0); spine.add(hp);
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
    sh.add(at(mesh(rb(.16, .34, .16, .075, 3), hoodMat), 0, -.14, 0));
    const el = grp(sh, 0, -.3, 0);
    el.add(at(mesh(rb(.14, .3, .14, .065, 3), hoodMat), 0, -.13, 0));
    el.add(at(mesh(new THREE.CylinderGeometry(.062, .062, .05, 12), std(0x7f8087, { roughness: .9 })), 0, -.27, 0));
    const hand = grp(el, 0, -.32, 0);
    hand.add(mesh(new THREE.SphereGeometry(.062, 14, 10), skinMat));
    arms.push({ sh, el, hand });
  }
  return { root, hips, spine, neck, head, eyes, brows, mouthArc, mouthO, arms };
}
const hu = human();
const HP = {
  base: { sx: .1, sz: 0, sy: 0, hx: .05, hy: 0, hz: 0, a0: { x: -1.2, y: 0, z: .25, ex: -1.0, ez: 0 }, a1: { x: -1.2, y: 0, z: -.25, ex: -1.0, ez: 0 },
    brow: 0, smile: .2, open: 0, wide: 0, lookX: 0, lookY: 0, shut: 0 },
};
// face-down on the desk at 3 AM, arms around his head
HP.slump = { ...HP.base, sx: .95, hx: .35, hz: .1, a0: { x: -2.1, y: .2, z: .55, ex: -1.6, ez: 0 }, a1: { x: -2.1, y: -.2, z: -.55, ex: -1.6, ez: 0 },
  brow: -.9, smile: -.7, shut: .7 };
HP.groan = { ...HP.slump, sx: .7, hx: -.1, hz: -.12, brow: -1, smile: -.9, open: .45, shut: .35 };
HP.stare = { ...HP.base, sx: .25, hx: .05, brow: .9, smile: -.1, open: .5, wide: 1, lookX: -.4, lookY: .2,
  a0: { x: -1.0, y: .1, z: .35, ex: -.6, ez: 0 }, a1: { x: -1.0, y: -.1, z: -.35, ex: -.6, ez: 0 } };
HP.watch = { ...HP.base, sx: .15, hx: -.05, hy: -.25, brow: .5, smile: .35, lookX: -.5, lookY: .3 };
HP.asleep = { ...HP.base, sx: .9, hx: .25, hz: -.2, hy: .2, a0: { x: -2.0, y: .2, z: .5, ex: -1.7, ez: 0 }, a1: { x: -2.0, y: -.2, z: -.5, ex: -1.7, ez: 0 },
  brow: .2, smile: .45, shut: 1 };
HP.wake = { ...HP.base, sx: -.05, hx: -.2, brow: 1, smile: .1, open: .85, wide: 1, lookX: -.45, lookY: .15,
  a0: { x: -1.4, y: .3, z: .55, ex: -1.3, ez: 0 }, a1: { x: -1.4, y: -.3, z: -.55, ex: -1.3, ez: 0 } };
HP.happy = { ...HP.base, sx: 0, hx: -.12, brow: .6, smile: 1, open: .25, lookX: .05, lookY: .1,
  a0: { x: -2.6, y: .2, z: .7, ex: -.6, ez: 0 }, a1: { x: -2.6, y: -.2, z: -.7, ex: -.6, ez: 0 } };
function applyArm(a, p) { a.sh.rotation.set(p.x, p.y, p.z); a.el.rotation.set(p.ex, 0, p.ez); }
function animHuman(t) {
  const keys = [[0, HP.slump], [L[0] + .15, HP.groan, .35], [E[0] - .1, HP.slump, .4], [L[1] - .1, HP.stare, .2], [L[3], HP.watch, .5],
    [E[7] - .3, HP.asleep, .9], [L[10] - .05, HP.wake, .2], [L[11], HP.happy, .4]];
  const p = poseAt(keys, t);
  const talk = envAt("creator", t);
  const br = Math.sin(t * 2.2) * .015 * (between(t, E[7], L[10]) ? 1.8 : 1);
  hu.spine.rotation.set(p.sx + br, p.sy, p.sz);
  hu.head.rotation.set(p.hx + talk * .08 * Math.sin(t * 13), p.hy + Math.sin(t * .9) * .03, p.hz);
  // chaos twitch: the phone keeps buzzing him
  if (t < L[1]) { hu.head.rotation.z += Math.sin(t * 31) * .02 * pulse(t, 1.2, .05, .4); }
  const a0 = { ...p.a0 }, a1 = { ...p.a1 };
  if (t > L[11] + .4) { const w = Math.sin((t - L[11]) * 9) * .25; a0.z += w; a1.z -= w; }
  applyArm(hu.arms[0], a0); applyArm(hu.arms[1], a1);
  const blink = ((t + .7) % 3.4) < .12 ? 1 : 0;
  hu.eyes.forEach((e, i) => {
    const sc = 1 + p.wide * .35; e.ew.scale.set(sc, sc, .6 * sc);
    e.pupil.position.set(p.lookX * .012, p.lookY * .012, .026);
    e.lid.rotation.x = -.6 + Math.max(blink, p.shut) * 1.5 - p.wide * .5 + (p.brow < 0 ? -p.brow * .3 : 0);
    hu.brows[i].position.y = .258 + p.brow * .022;
    hu.brows[i].rotation.z = (i ? 1 : -1) * p.brow * -.25;
  });
  const sm = p.smile;
  hu.mouthArc.rotation.z = sm >= 0 ? Math.PI : 0;
  hu.mouthArc.position.y = sm >= 0 ? .1 : .07;
  hu.mouthArc.scale.set(.8 + Math.abs(sm) * .5, .25 + Math.abs(sm) * .75, 1);
  const open = clamp(Math.max(p.open, talk * 1.3));
  hu.mouthO.scale.set(.7 + open * .3, .08 + open * .55, .35);
  hu.mouthO.visible = open > .04; hu.mouthArc.visible = open < .5;
}

// ---------------------------------------------------------------- textures (drawn in drawTextures, once the fonts are in)
const TX = {};
const FACES = [];                                  // [mesh, texture key] pairs filled in after the fonts load
function face(m, k) { FACES.push([m, k]); return m; }
function setMap(m, k) { if (TX[k] && m.material.map !== TX[k]) { m.material.map = TX[k]; } }
function write(g, s, x, y, size, o = {}) {
  g.font = `${o.w || 700} ${size}px ${o.f || "Poppins"}`; g.fillStyle = o.c || "#fff"; g.textAlign = o.a || "left"; g.textBaseline = "middle";
  g.fillText(s, x, y, o.max);
}
function tick(g, x, y, s, c = "#3fd69b", lw = 0) {
  g.strokeStyle = c; g.lineWidth = lw || s * .2; g.lineCap = "round"; g.lineJoin = "round";
  g.beginPath(); g.moveTo(x - s * .45, y); g.lineTo(x - s * .12, y + s * .32); g.lineTo(x + s * .48, y - s * .36); g.stroke();
}
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
const faceMat = (k = 1, o = {}) => new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false, color: new THREE.Color(k, k, k), ...o });
// a two-sided card: front and back each show their own texture
function card2(w, h, k = 1) {
  const g = new THREE.Group();
  const f = new THREE.Mesh(new THREE.PlaneGeometry(w, h), faceMat(k)); f.position.z = .013; g.add(f);
  const b = new THREE.Mesh(new THREE.PlaneGeometry(w, h), faceMat(k)); b.rotation.y = Math.PI; b.position.z = -.013; g.add(b);
  g.userData.front = f; g.userData.back = b;
  return g;
}

// ---------------------------------------------------------------- Claude: the coral spark as-is, dressed as the producer
const CL_R = .2;
const clMat = phys(CORAL, { roughness: .38, clearcoat: .8, clearcoatRoughness: .25, emissive: CORAL, emissiveIntensity: .05 });
const inkM = std(0x2a120c, { roughness: .3 });
function rays(parent, n, R, len0, len1, seed, rad = .05, cast = true) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const arm = i === 0 || i === n / 2;
    const a = i / n * Math.PI * 2 + (arm ? 0 : (hash(i + seed) - .5) * .22);
    const l = arm ? (len0 + len1) / 2 : lerp(len0, len1, hash(i + seed + 17));
    const piv = grp(parent); piv.rotation.z = a - Math.PI / 2; piv.position.z = -.03;
    const r = mesh(new THREE.CapsuleGeometry(rad, l, 4, 10), clMat, cast, false); r.position.y = R * .55 + l / 2; piv.add(r);
    const tip = grp(piv, 0, R * .55 + l + rad, 0);
    out.push({ piv, r, base: a - Math.PI / 2, l, tip });
  }
  return out;
}
function claudeBuild() {
  const root = grp(scene);
  const body = grp(root);
  const core = mesh(new THREE.SphereGeometry(CL_R, 40, 28), clMat); core.scale.z = .72; body.add(core);
  const rs = rays(body, 12, CL_R, .2, .34, 3, .041);
  const halo0 = halo(1.7, CORAL, .2); halo0.position.z = -.12; body.add(halo0);
  // face
  const fc = grp(body, 0, 0, CL_R * .72 - .01);
  const eyes = [];
  for (const s of [-1, 1]) {
    const open = mesh(new THREE.SphereGeometry(.03, 16, 12), inkM, false, false); open.scale.set(.85, 1.35, .5); open.position.set(s * .066, .035, 0); fc.add(open);
    const hl = mesh(new THREE.SphereGeometry(.0095, 8, 6), glow(0xffffff, 1.4), false, false); hl.position.set(.011, .013, .022); open.add(hl);
    const shut = mesh(new THREE.TorusGeometry(.03, .008, 6, 14, Math.PI), inkM, false, false); shut.position.set(s * .066, .028, .006); fc.add(shut);
    eyes.push({ open, shut, hl, x: s * .066 });
  }
  const mouthArc = mesh(new THREE.TorusGeometry(.038, .009, 6, 16, Math.PI), inkM, false, false); mouthArc.position.set(0, -.045, .008); fc.add(mouthArc);
  const mouthO = mesh(new THREE.SphereGeometry(.034, 14, 10), std(0x3a0f0a, { roughness: .5 }), false, false); mouthO.scale.set(1, .5, .3); mouthO.position.set(0, -.05, .004); fc.add(mouthO);
  for (const s of [-1, 1]) { const ch = new THREE.Mesh(new THREE.CircleGeometry(.026, 16), add(0xff7a90, .32)); ch.position.set(s * .118, -.022, -.004); fc.add(ch); }
  // producer headset: band, ear cups with coral rings, a mic boom to the mouth
  const hsM = std(0x24202a, { roughness: .35, metalness: .6 });
  const band = mesh(new THREE.TorusGeometry(.214, .016, 8, 40, Math.PI), hsM); band.position.z = .03; body.add(band);
  for (const s of [-1, 1]) {
    const cup = mesh(new THREE.CylinderGeometry(.066, .066, .062, 24), hsM); cup.rotation.z = Math.PI / 2; cup.position.set(s * .207, -.005, .03); body.add(cup);
    const ring = mesh(new THREE.TorusGeometry(.066, .01, 8, 24), glow(CORAL_L, 1.6), false, false); ring.rotation.y = Math.PI / 2; ring.position.set(s * .24, -.005, .03); body.add(ring);
  }
  const boom = mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([V(-.215, -.03, .07), V(-.2, -.11, .13), V(-.12, -.135, .165), V(-.065, -.105, .17)]), 24, .008, 6), hsM);
  body.add(boom);
  const mic = mesh(new THREE.SphereGeometry(.021, 12, 10), hsM); mic.position.set(-.062, -.103, .172); body.add(mic);
  const micDot = new THREE.Mesh(new THREE.SphereGeometry(.007, 8, 6), glow(RED, 3)); micDot.position.set(-.05, -.09, .19); body.add(micDot);
  // lanyard and PRODUCER badge
  for (const s of [-1, 1]) {
    const st = mesh(new THREE.CylinderGeometry(.0055, .0055, .2, 6), std(CORAL_L, { roughness: .6 }), false, false);
    st.position.set(s * .065, -.2, .135); st.rotation.z = s * .32; st.rotation.x = .12; body.add(st);
  }
  const badge = card(.17, .105, 1.05, 0x1a1424); badge.position.set(0, -.33, .14); badge.rotation.x = -.08; body.add(badge);
  face(badge.userData.face, "badge");
  return { root, body, rs, armR: rs[0], armL: rs[6], eyes, mouthArc, mouthO, fc, halo: halo0, micDot };
}
const cl = claudeBuild();

// eleven mini-Claudes: the same spark at a third of the size, dot eyes and a grin
function miniBuild(i) {
  const root = grp(scene);
  const body = grp(root);
  const core = mesh(new THREE.SphereGeometry(CL_R, 24, 16), clMat, false, false); core.scale.z = .72; body.add(core);
  const rs = rays(body, 10, CL_R, .18, .3, 40 + i * 7, .05, false);
  const eyes = [];
  for (const s of [-1, 1]) { const e = mesh(new THREE.SphereGeometry(.034, 10, 8), inkM, false, false); e.scale.set(.85, 1.3, .5); e.position.set(s * .07, .03, .135); body.add(e); eyes.push(e); }
  const sm = mesh(new THREE.TorusGeometry(.045, .012, 6, 12, Math.PI), inkM, false, false); sm.rotation.z = Math.PI; sm.position.set(0, -.035, .14); body.add(sm);
  const h = halo(1.4, CORAL, .25); h.position.z = -.1; body.add(h);
  root.scale.setScalar(.001); root.visible = false;
  return { root, body, rs, eyes };
}
const minis = Array.from({ length: 11 }, (_, i) => miniBuild(i));

// ---------------------------------------------------------------- key places
scene.updateMatrixWorld(true);
const MONP = monScreen.getWorldPosition(new THREE.Vector3());
const HERO = V(-.1, 1.32, -.3);                     // where Claude lands after bursting out of the monitor
const CALM_P = V(.7, 1.2, -.75);                   // floating over the desk corner with a tea
// the five skill stations: panel centre, the camera that frames it (start, end) and where it looks
const ST = [
  { p: V(-1.25, 1.55, -.35), cam: [[-.6, 1.4, 2.85], [-.75, 1.38, 2.6]], look: [-1.18, 1.28, -.35], fov: 40, cl: V(-.92, 1.04, -.02) },
  { p: V(1.2, 1.62, -.25), cam: [[.62, 1.45, 2.85], [.75, 1.45, 2.6]], look: [1.15, 1.36, -.25], fov: 40, cl: V(.9, 1.1, .05) },
  { p: V(0, 2.2, -.7), cam: [[-.12, 2.05, 2.5], [.08, 2.05, 2.35]], look: [0, 1.95, -.7], fov: 40, cl: V(.4, 1.64, -.42) },
  { p: V(.75, 2.2, -1.95), cam: [[.45, 2.0, 1.0], [.55, 2.0, .8]], look: [.72, 1.93, -1.95], fov: 40, cl: V(.45, 1.68, -1.65) },
  { p: V(-.2, 1.88, -2.5), cam: [[-.5, 1.74, .4], [-.48, 1.75, .15]], look: [-.22, 1.62, -2.5], fov: 40, cl: V(-.55, 1.38, -2.1) },
];
for (const s of ST) s.T = [L[3], L[4], L[5], L[6], L[7]][ST.indexOf(s)];

// ---------------------------------------------------------------- the notification swarm (BAD chaos)
const NOTES = [
  { i: "S", c: "#ff3b46", h: "Script.doc", b: "0 words · due today", d: "Script · 5 hooks, scored" },
  { i: "T", c: "#ff8a3d", h: "Thumbnail", b: "thumbnail_FINAL_v7.png", d: "Title + thumbnail · linted" },
  { i: "E", c: "#ff3b46", h: "Edit", b: "2h 14m of raw footage", d: "Edit list · 4 cuts marked" },
  { i: "C", c: "#ff5fa2", h: "Comments", b: "99+ unread", d: "Replies drafted · 1 to pin" },
  { i: "P", c: "#ffb46b", h: "Calendar", b: "Nothing planned this week", d: "Week planned · 5 videos" },
  { i: "!", c: "#ff3b46", h: "Upload failed", b: "Tap to retry" },
  { i: "%", c: "#ff8a3d", h: "Render", b: "3% · 4h 12m left" },
  { i: "@", c: "#ff5fa2", h: "New comment", b: "\"upload when??\"" },
  { i: "9", c: "#ff3b46", h: "Deadline", b: "Tomorrow, 9:00 AM" },
  { i: "↓", c: "#ff8a3d", h: "Analytics", b: "Views down this week" },
];
// parked spots after Claude's shockwave: the five station ones next to their station, the rest high round the room
const PARK = [V(-1.05, 2.12, -.2), V(1.38, 2.2, -.1), V(.55, 2.62, -.65), V(1.2, 2.72, -1.8), V(-.62, 2.55, -2.3),
  V(-1.7, 2.6, -1.2), V(1.75, 2.45, -1.0), V(-.9, 2.9, -.9), V(.2, 2.95, -1.6), V(1.0, .95, .1)];
const notes = NOTES.map((n, i) => {
  const g = card2(.5, .125, 1.05); scene.add(g);
  face(g.userData.front, "note" + i); face(g.userData.back, i < 5 ? "done" + i : "note" + i);
  g.visible = false;
  return g;
});
const NOTE_IN = (i) => .05 + i * .27;               // they keep coming through the first line
const ZAP = (i) => T.eleven + .78 + (i - 5) * .07;  // the five extra minis catch the stray ones
const RESOLVE = (i) => ST[i].T + .35;               // a station's own card flips green as it starts
function notePos(i, t) {
  const r = .42 + hash(i) * .42, y = .95 + hash(i + 5) * 1.0;
  const th = hash(i + 9) * 6.28 + t * (.55 + hash(i + 2) * .6) * (i % 2 ? 1 : -1);
  const chaos = V(.3 + Math.cos(th) * r, y + Math.sin(t * 2 + i) * .05, -1.05 + Math.sin(th) * r * .62);
  const k = easeOut(win(t, L[1] - .05, L[1] + .55));
  return chaos.lerp(PARK[i], k);
}
function animNotes(t) {
  notes.forEach((g, i) => {
    const a = NOTE_IN(i);
    let s = backOut(win(t, a, a + .22), 2.2);
    let p = notePos(i, t), flip = 0;
    if (i >= 5) s *= 1 - easeIn(win(t, ZAP(i), ZAP(i) + .14));
    else {
      flip = easeIO(win(t, RESOLVE(i), RESOLVE(i) + .28));
      const go = easeIn(win(t, RESOLVE(i) + 1.0, RESOLVE(i) + 1.35));
      p = p.lerp(ST[i].p, go); s *= 1 - go;
    }
    g.visible = s > .002;
    if (!g.visible) return;
    // buzz: each card shakes as it lands and with the phone
    const bz = (pulse(t, a, .02, .35) + (t < L[1] ? pulse((t + i * .13) % 1.1, .05, .02, .25) * .6 : 0));
    g.position.set(p.x + Math.sin(t * 83 + i) * .012 * bz, p.y + Math.cos(t * 71 + i) * .008 * bz, p.z);
    g.quaternion.copy(camera.quaternion);
    g.rotateZ((hash(i + 30) - .5) * .25 * (1 - win(t, L[1], L[1] + .6)) + Math.sin(t * 1.3 + i) * .03);
    g.rotateY(flip * Math.PI);
    g.scale.setScalar(Math.max(.001, s) * (t < L[1] ? 1 : .9));
  });
}

// ---------------------------------------------------------------- the five stations (ORDER): each one switches off a fire
const FORMULAS = ["The Statistic", "Someone Else's Result", "The Mistake", "Contrarian Flip", "The Reveal", "The Superlative", "The Clock",
  "I Tried It", "The Question", "Before and After", "The Teardown", "The Stack", "The Warning", "The List", "The Receipt", "The Insider",
  "The Impossible Claim", "The Comparison", "The Origin", "The Deadline", "The Direct Address"];
const stations = ST.map((s) => { const g = grp(scene, s.p.x, s.p.y, s.p.z); g.lookAt(...s.cam[1]); g.visible = false; return g; });
function holo(parent, w, h, k, x, y, z = 0) { const c = card(w, h, k, 0x140f1e); c.position.set(x, y, z); parent.add(c); return c; }
const MINI_AT = [V(-.36, -.32, .22), V(.4, -.3, .16), null, V(.38, -.44, .14), V(.44, -.36, .16)];

// 0 /yt-script: the page writes itself while the 21 hook formulas fan out round it
const s0 = stations[0];
const page = holo(s0, .5, .66, 1, 0, 0); face(page.userData.face, "page");
const pageLines = [];
for (let k = 0; k < 9; k++) {
  const w = k === 0 ? .36 : .25 + hash(k + 70) * .15;
  const b = new THREE.Mesh(new THREE.PlaneGeometry(w, .022), new THREE.MeshBasicMaterial({ color: k === 0 ? 0xd97757 : 0x3a3346, toneMapped: false }));
  b.geometry.translate(w / 2, 0, 0); b.position.set(-.2, .14 - k * .052, .006); page.add(b); pageLines.push(b);
}
const fcards = FORMULAS.map((f, k) => { const c = holo(s0, .27, .066, 1.1, 0, 0, -.05); face(c.userData.face, "f" + k); return c; });
function animS0(t) {
  pageLines.forEach((b, k) => { b.scale.x = Math.max(.001, easeOut(win(t, L[3] + .12 + k * .14, L[3] + .3 + k * .14))); });
  fcards.forEach((c, k) => {
    const a = T.twentyone - .25 + k * .05;
    const kk = easeOut(win(t, a, a + .32));
    const th = Math.PI / 2 - k / 21 * Math.PI * 2 + (t - T.twentyone) * .14;
    const from = MINI_AT[0];
    c.position.set(lerp(from.x, Math.cos(th) * .42, kk), lerp(from.y, Math.sin(th) * .72, kk), lerp(.2, -.05, kk));
    c.scale.setScalar(Math.max(.001, backOut(win(t, a, a + .25), 2)));
    c.rotation.z = (1 - kk) * 1.2;
    c.visible = t > a;
  });
}

// 1 /yt-package: the thumbnail flips from the mess to one bold idea; the title is linted as its pair
const s1 = stations[1];
const thumb = card2(.72, .405, 1.05); thumb.position.set(0, .12, 0); s1.add(thumb);
face(thumb.userData.front, "thBefore"); face(thumb.userData.back, "thAfter");
const thBack = mesh(rb(.74, .425, .02, .03, 2), phys(0x140f1e, { roughness: .35, clearcoat: 1 }), false, false); thumb.add(thBack);
const tbar = holo(s1, .72, .1, 1.05, 0, -.17); face(tbar.userData.face, "tiBefore");
const lint = holo(s1, .72, .085, 1.05, 0, -.29, .01); face(lint.userData.face, "lint");
function animS1(t) {
  const f = easeIO(win(t, L[4] + .5, L[4] + .82));
  thumb.rotation.y = f * Math.PI; thumb.position.z = Math.sin(f * Math.PI) * .12;
  const swap = t > L[4] + .78 && !(t < L[4] + .9 && Math.floor(t * 30) % 2);
  setMap(tbar.userData.face, swap ? "tiAfter" : "tiBefore");
  lint.scale.setScalar(Math.max(.001, backOut(win(t, L[4] + .98, L[4] + 1.22), 2.4)));
}

// 2 /yt-edit: a playhead runs the timeline and flags every cut; the edit decision list comes out underneath
const s2 = stations[2];
const RIB = [];
{
  const ws = Array.from({ length: 10 }, (_, k) => .07 + hash(k + 90) * .07); const sum = ws.reduce((a, b) => a + b, 0);
  let x = -.5;
  ws.forEach((w0, k) => {
    const w = w0 / sum * .9;
    const flag = [1, 4, 6, 8].indexOf(k);
    const m = mesh(rb(w, .12, .03, .012, 2), std(0x3b2a6e, { emissive: [0x5b3bd0, 0x2f7fd0, 0x7b3bc0][k % 3], emissiveIntensity: .55, roughness: .4 }), false, false);
    m.position.set(x + w / 2 + .005, 0, 0); s2.add(m);
    const pin = flag >= 0 ? holo(s2, .19, .062, 1.1, x + w / 2, .15, .02) : null;
    if (pin) face(pin.userData.face, "flag" + flag);
    RIB.push({ m, x: x + w / 2, flag, pin });
    x += w + .01;
  });
}
const playhead = new THREE.Mesh(new THREE.BoxGeometry(.008, .2, .01), glow(0xffffff, 2.2)); s2.add(playhead);
const edl = holo(s2, .58, .34, 1.05, 0, -.3); face(edl.userData.face, "edl");
const PH = (t) => lerp(-.5, .5, easeIO(win(t, L[5] + .05, L[5] + 1.35)));
function animS2(t) {
  const ph = PH(t);
  playhead.position.set(ph, 0, .03); playhead.visible = between(t, L[5], L[5] + 1.5);
  RIB.forEach((r) => {
    if (r.flag < 0) return;
    const hit = t > L[5] + .05 && ph > r.x;
    r.m.material.emissive.set(hit ? RED : 0x5b3bd0); r.m.material.emissiveIntensity = hit ? 1.1 + pulse(t, L[5] + .05 + (r.x + .5) * 1.3, .03, .3) : .55;
    const tp = L[5] + .05 + win(r.x, -.5, .5) * 1.3;
    r.pin.scale.setScalar(Math.max(.001, backOut(win(t, tp, tp + .2), 2.6)));
  });
  edl.scale.setScalar(Math.max(.001, backOut(win(t, L[5] + 1.38, L[5] + 1.65), 1.8)));
}

// 3 /yt-comment: the comments pour in, the replies come back in coral, one gets the pin
const s3 = stations[3];
const bubbles = [], replies = [];
for (let k = 0; k < 4; k++) {
  const b = holo(s3, .54, .1, 1.05, -.08, .38 - k * .25); face(b.userData.face, "cm" + k); bubbles.push(b);
  const r = holo(s3, .5, .09, 1.1, .1, .38 - k * .25 - .11, .015); face(r.userData.face, "rp" + k); replies.push(r);
}
const pinC = holo(s3, .085, .085, 1.2, .2, .43 - 2 * .25, .04); face(pinC.userData.face, "pin");
function animS3(t) {
  bubbles.forEach((b, k) => { const a = L[6] - .2 + k * .08; b.scale.setScalar(Math.max(.001, backOut(win(t, a, a + .2), 2.2))); b.position.x = -.08 - (1 - easeOut(win(t, a, a + .25))) * .3; });
  replies.forEach((r, k) => { const a = L[6] + .3 + k * .17; r.scale.setScalar(Math.max(.001, backOut(win(t, a, a + .2), 2.2))); });
  const pa = L[6] + 1.08;
  pinC.position.y = .43 - .5 + (1 - easeIn(win(t, pa, pa + .18))) * .4; pinC.visible = t > pa;
  pinC.rotation.z = -.4 + easeOut(win(t, pa + .18, pa + .4)) * .4;
}

// 4 /yt-plan: one anchor, one cheap one, three Shorts drop into the week
const s4 = stations[4];
const calB = holo(s4, .78, .95, 1.02, 0, 0); face(calB.userData.face, "cal");
const PLAN = [[0, "anchor", .52], [1, "short", .3], [2, "cheap", .44], [3, "short", .3], [5, "short", .3]];
const blocks = PLAN.map(([row, k, w], i) => { const c = holo(s4, w, .072, 1.08, -.2 + w / 2 + .02, .29 - row * .1, .02); face(c.userData.face, "pl" + i); return c; });
const fits = holo(s4, .6, .07, 1.1, 0, -.53, .03); face(fits.userData.face, "fits");
function animS4(t) {
  blocks.forEach((b, i) => {
    const a = L[7] + .12 + i * .15;
    const y0 = .29 - PLAN[i][0] * .1;
    b.position.y = y0 + (1 - easeOut(win(t, a, a + .22))) * .5 + Math.sin(win(t, a + .22, a + .5) * Math.PI) * -.012;
    b.visible = t > a; b.scale.setScalar(Math.max(.001, easeOut(win(t, a, a + .12))));
  });
  fits.scale.setScalar(Math.max(.001, backOut(win(t, L[7] + .95, L[7] + 1.2), 2.4)));
}
function animStations(t) {
  stations.forEach((g, i) => {
    const z = i < 4 ? ST[i + 1].T - .32 : E[7] + .02;
    const s = backOut(win(t, ST[i].T - .32, ST[i].T + .04), 1.6) * (1 - easeIn(win(t, z, z + .3)));
    g.visible = s > .002; g.scale.setScalar(Math.max(.001, s));
  });
  if (stations[0].visible) animS0(t);
  if (stations[1].visible) animS1(t);
  if (stations[2].visible) animS2(t);
  if (stations[3].visible) animS3(t);
  if (stations[4].visible) animS4(t);
}

// the title card on "Not one skill... eleven"
const title = card(1.2, .6, 1.08, 0x1a1028); title.position.set(-.1, 2.12, -.75); scene.add(title); face(title.userData.face, "title");
title.visible = false;
function animTitle(t) {
  const a = L[2] - .05, z = L[3] - .1;
  const k = backOut(win(t, a, a + .38), 1.5) * (1 - easeIn(win(t, z, z + .25)));
  title.visible = k > .002;
  title.scale.setScalar(Math.max(.001, k));
  title.rotation.set((1 - easeOut(win(t, a, a + .45))) * -1.2, Math.sin(t * .8) * .05, 0);
  title.position.y = 2.12 + Math.sin(t * 1.4) * .015 + pulse(t, T.eleven, .04, .3) * .05;
}

// ---------------------------------------------------------------- tea for the calm
const mug = grp(scene);
mug.add(at(mesh(new THREE.CylinderGeometry(.034, .03, .07, 16), std(CREAM, { roughness: .35 })), 0, 0, 0));
mug.add(at(mesh(new THREE.TorusGeometry(.021, .007, 6, 14), std(CREAM, { roughness: .35 })), .036, 0, 0));
mug.add(at(mesh(new THREE.CircleGeometry(.028, 16).rotateX(-Math.PI / 2), std(0x7a3e1c, { roughness: .2 })), 0, .03, 0));
const steam = Array.from({ length: 6 }, (_, i) => { const s = halo(.09, 0xfff0e0, .18); mug.add(s); return s; });
const MUG_DESK = V(.92, .85, -.8);

// ---------------------------------------------------------------- the neon city of videos (GOOD chaos)
const C0 = V(0, 0, -60);
const city = grp(scene, C0.x, C0.y, C0.z); city.visible = false;
const cground = mesh(new THREE.PlaneGeometry(60, 60), std(0x07050e, { roughness: .28, metalness: .7 }), false, true); cground.rotation.x = -Math.PI / 2; city.add(cground);
const cgrid = new THREE.GridHelper(60, 75, VIOLET, 0x3a1f6e); cgrid.material.transparent = true; cgrid.material.opacity = .35; cgrid.position.y = .005; city.add(cgrid);
const facM = [0, 1, 2, 3].map(() => std(0x0b0814, { emissive: 0xffffff, emissiveIntensity: 1.0, roughness: .45, metalness: .35 }));
const NEWLOT = V(0, 0, -6.8);
// outliers: the videos that beat their own channel, with their multiple over the channel's median
const OUT = [[1.6, -3.6, 11, "31×"], [-1.6, 1.2, 8, "18×"], [3.2, -2.0, 9, "12×"], [-3.2, -6.8, 10, "22×"], [1.6, 4.4, 7, "9×"], [4.8, -8.4, 9.5, "14×"]];
const towers = [];
for (let gx = -4; gx <= 4; gx++) for (let gz = 0; gz < 11; gz++) {
  if (gx === 0) continue;
  const x = gx * 1.6, z = 6 - gz * 1.6;
  if (Math.abs(x - NEWLOT.x) < .1 && Math.abs(z - NEWLOT.z) < .1) continue;
  const o = OUT.findIndex((q) => Math.abs(q[0] - x) < .1 && Math.abs(q[1] - z) < .1);
  const id = (gx + 5) * 13 + gz;
  const h = o >= 0 ? OUT[o][2] : 1.1 + hash(id) * (2.2 + Math.abs(gx) * .5 + gz * .18);
  const w = .9 + hash(id + 3) * .3, d = .9 + hash(id + 5) * .3;
  const geo = new THREE.BoxGeometry(w, h, d); geo.translate(0, h / 2, 0);
  const uv = geo.attributes.uv; for (let k = 0; k < uv.count; k++) uv.setXY(k, uv.getX(k) * w / 1.0, uv.getY(k) * h / 1.25);
  const m = new THREE.Mesh(geo, o >= 0 ? std(0x0b0814, { emissive: 0xffffff, emissiveIntensity: 1.5, roughness: .4, metalness: .35, transparent: true }) : facM[id % 4]);
  m.position.set(x, 0, z); city.add(m);
  let edges = null;
  if (o >= 0) { edges = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({ color: new THREE.Color(o === 0 ? CYAN : GOLD).multiplyScalar(2), toneMapped: false, transparent: true })); m.add(edges); }
  towers.push({ m, x, z, h, o, edges, dist: Math.hypot(x, z - 7) });
}
const beams = OUT.map((q, k) => {
  const b = new THREE.Mesh(new THREE.CylinderGeometry(.5, .5, 30, 24, 1, true), add(k === 0 ? CYAN : GOLD, .25, { side: THREE.DoubleSide }));
  b.position.set(q[0], 15, q[1]); city.add(b); return b;
});
const chips = OUT.map((q, k) => { const c = card(.95, .24, 1.1, 0x1a1028); c.position.set(q[0], q[2] + .45, q[1]); city.add(c); face(c.userData.face, "chip" + k); return c; });
// the X-ray of the tallest one: what its title did, in words
const xray = card(2.0, .67, 1.12, 0x0c1a24); xray.position.set(OUT[0][0] - .2, OUT[0][2] * .62, OUT[0][1] + .9); city.add(xray); face(xray.userData.face, "xray");
const scan = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.6), add(CYAN, .55, { side: THREE.DoubleSide })); scan.rotation.x = -Math.PI / 2; city.add(scan);
const xTower = towers.find((tw) => tw.o === 0);
// the new one, built from a coral soundwave in the creator's voice
const NEWH = 7.5;
const newGeo = new THREE.BoxGeometry(1.1, NEWH, 1.1); newGeo.translate(0, NEWH / 2, 0);
{ const uv = newGeo.attributes.uv; for (let k = 0; k < uv.count; k++) uv.setXY(k, uv.getX(k), uv.getY(k) * NEWH / 1.25); }
const newT = new THREE.Mesh(newGeo, std(0x1a0c0a, { emissive: 0xffffff, emissiveIntensity: 1.4, roughness: .35, metalness: .3 })); newT.position.copy(NEWLOT); city.add(newT);
const newEdges = new THREE.LineSegments(new THREE.EdgesGeometry(newGeo), new THREE.LineBasicMaterial({ color: new THREE.Color(CORAL_L).multiplyScalar(2.5), toneMapped: false })); newT.add(newEdges);
const newChip = card(1.3, .32, 1.12, 0x2a1410); newChip.position.set(NEWLOT.x, NEWH * .5, NEWLOT.z + .9); city.add(newChip); face(newChip.userData.face, "newchip");
const WAVE = 90;
const wave = new THREE.InstancedMesh(new THREE.BoxGeometry(.05, 1, .05), glow(CORAL_L, 2.6), WAVE); wave.frustumCulled = false; city.add(wave);
const TRAIL = 36;
const trail = new THREE.InstancedMesh(new THREE.PlaneGeometry(1, 1), add(CORAL, .28, { map: glowTex }), TRAIL); trail.frustumCulled = false; scene.add(trail);

// ---------------------------------------------------------------- the landing: one link to paste
const linkC = card(.8, .32, 1.06, 0x1a1028); linkC.position.set(.7, 1.66, -.42); scene.add(linkC); face(linkC.userData.face, "link0");
linkC.lookAt(.66, 1.62, 2.0); linkC.visible = false;
const shafts = [0, 1, 2].map((k) => {
  const s = new THREE.Mesh(new THREE.PlaneGeometry(.5 + k * .2, 4.2), add(0xffb070, .12, { map: glowTex, side: THREE.DoubleSide }));
  s.position.set(1.1 - k * .35, 1.15, -1.3 + k * .15); s.rotation.set(.62, -.25, .55 + k * .05); scene.add(s); return s;
});

// ---------------------------------------------------------------- sparks and confetti (pure functions of t)
const BURSTS = [];
function burst(t, p, c, n, sp = 1.2, life = .7, size = 1) { BURSTS.push({ t, p, c: new THREE.Color(c), n, sp, life, size }); }
burst(L[1] - .06, MONP.clone().add(V(.15, 0, .3)), CORAL_L, 46, 2.2, .8, 1.3);
burst(T.eleven - .02, HERO, GOLD, 34, 1.6, .7);
for (let i = 5; i < 10; i++) burst(ZAP(i), PARK[i], GREEN, 12, .9, .5);
for (let i = 0; i < 5; i++) burst(RESOLVE(i) + 1.33, ST[i].p, GREEN, 16, 1.0, .55);
burst(T.link + .28, linkC.position.clone(), GREEN, 22, 1.1, .6);
burst(L[9] + .02, C0.clone().add(V(0, 5.6, 8.2)), VIOLET, 40, 2.4, .8, 1.5);
burst(T.blowing + .55, C0.clone().add(V(OUT[0][0], OUT[0][2], OUT[0][1])), CYAN, 26, 1.6, .7, 1.5);
burst(T.voice + .2, C0.clone().add(NEWLOT).add(V(0, NEWH, 0)), CORAL_L, 36, 1.9, .8, 1.7);
const SPARKN = BURSTS.reduce((a, b) => a + b.n, 0);
const sparks = new THREE.InstancedMesh(new THREE.ShapeGeometry(sparkleShape(.045, .011)), glow(0xffffff, 3, { side: THREE.DoubleSide }), SPARKN);
sparks.frustumCulled = false; scene.add(sparks);
{ let j = 0; for (const b of BURSTS) { b.i0 = j; for (let k = 0; k < b.n; k++) sparks.setColorAt(j++, b.c); } }
const CONF = 110, CONF_T = T.youtube - .05;
const confetti = new THREE.InstancedMesh(new THREE.PlaneGeometry(.03, .052), std(0xffffff, { side: THREE.DoubleSide, roughness: .5, emissive: 0xffffff, emissiveIntensity: .35 }), CONF);
confetti.frustumCulled = false; scene.add(confetti);
for (let k = 0; k < CONF; k++) confetti.setColorAt(k, new THREE.Color([CORAL, CORAL_L, VIOLET, GOLD, CYAN, PINK, CREAM][k % 7]));
const tM = new THREE.Matrix4(), tP = new THREE.Vector3(), tQ = new THREE.Quaternion(), tS = new THREE.Vector3(), tE = new THREE.Euler(), tV = new THREE.Vector3();
const ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
function dirOf(seed) { const u = hash(seed) * 2 - 1, a = hash(seed + 1.7) * Math.PI * 2, r = Math.sqrt(1 - u * u); return V(r * Math.cos(a), u, r * Math.sin(a)); }
function animParticles(t) {
  for (const b of BURSTS) for (let k = 0; k < b.n; k++) {
    const j = b.i0 + k, age = t - b.t;
    if (age < 0 || age > b.life) { sparks.setMatrixAt(j, ZERO); continue; }
    const d = dirOf(j * 3.1 + 5), sp = b.sp * (.45 + hash(j + 11) * .8);
    tP.copy(b.p).addScaledVector(d, sp * (age - age * age / (2 * b.life)));
    tQ.copy(camera.quaternion).multiply(new THREE.Quaternion().setFromAxisAngle(V(0, 0, 1), age * 6 + j));
    tS.setScalar(b.size * (1 - age / b.life) * (.6 + hash(j + 4) * .8));
    sparks.setMatrixAt(j, tM.compose(tP, tQ, tS));
  }
  sparks.instanceMatrix.needsUpdate = true;
  const org = cl.root.position;
  for (let k = 0; k < CONF; k++) {
    const age = t - CONF_T;
    if (age < 0 || age > 4) { confetti.setMatrixAt(k, ZERO); continue; }
    const d = dirOf(k * 5.3 + 99); d.y = Math.abs(d.y) * 1.4 + .3;
    const sp = 1.6 + hash(k + 21) * 1.6, drag = 1 - Math.exp(-age * 2.2);
    tP.set(org.x + d.x * sp * drag / 2.2 + Math.sin(age * 3 + k) * .05 * age, org.y + d.y * sp * drag / 2.2 - .55 * age * age * .5, org.z + d.z * sp * drag / 2.2 * .6);
    tQ.setFromEuler(tE.set(age * (3 + hash(k) * 5), age * 4 + k, age * (2 + hash(k + 2) * 4)));
    tS.setScalar(1);
    confetti.setMatrixAt(k, tM.compose(tP, tQ, tS));
  }
  confetti.instanceMatrix.needsUpdate = true;
}

// ---------------------------------------------------------------- Claude's performance
const CP = { eyeH: 1, happy: 0, wink: 0, smile: .45, open: 0, lx: 0, ly: 0, tilt: 0, lean: 0, aR: -.25, aL: -.25 };
const CPS = {
  rest: CP,
  burst: { ...CP, eyeH: 1.35, smile: 1, open: .55, aR: .9, aL: .9 },
  cheeky: { ...CP, wink: 1, smile: .85, tilt: .12, aR: .25, aL: -.3 },
  proud: { ...CP, happy: 1, smile: 1, aR: .7, aL: .7, tilt: -.05 },
  calm: { ...CP, eyeH: .6, smile: .55, aR: -.35, aL: -.4 },
  serious: { ...CP, eyeH: .75, smile: .1, aR: -.1, aL: -.1 },
  excited: { ...CP, eyeH: 1.3, smile: 1, open: .3, aR: .45, aL: .45 },
  presentL: { ...CP, eyeH: 1.1, smile: .8, aL: .45, aR: -.2, lx: -.6 },
  presentR: { ...CP, eyeH: 1.1, smile: .8, aR: .45, aL: -.2, lx: .6 },
  presentU: { ...CP, eyeH: 1.1, smile: .8, aR: .8, aL: -.1, ly: .7 },
  sip: { ...CP, eyeH: .35, smile: .5, aR: 1.05, aL: -.45, tilt: .08 },
  whisper: { ...CP, eyeH: .7, smile: .3, lean: .25, aR: .95, aL: -.4, lx: -.2, tilt: -.12 },
  fly: { ...CP, eyeH: 1.25, smile: 1, open: .2, aR: -.9, aL: -.9, lean: -.35 },
  wave: { ...CP, eyeH: 1.15, smile: 1, open: .15, aR: 1.25, aL: -.3 },
};
const clKeys = [[0, CPS.burst], [L[1] + .5, CPS.excited, .3], [L[1] + 1.3, CPS.cheeky, .25], [T.free - .15, CPS.proud, .2], [L[2], CPS.serious, .3],
  [T.eleven - .12, CPS.burst, .15], [L[3] - .2, CPS.presentL, .3], [L[4] - .2, CPS.presentR, .3], [L[5] - .2, CPS.presentU, .3], [L[6] - .2, CPS.cheeky, .3],
  [L[7] - .2, CPS.presentU, .3], [E[7] + .05, CPS.calm, .5], [E[7] + .55, CPS.sip, .45], [L[8] - .2, CPS.whisper, .35], [L[9] - .05, CPS.fly, .12],
  [T.writes - .1, CPS.excited, .25], [L[10], CPS.rest, .3], [T.paste - .2, CPS.presentL, .25], [T.link + .3, CPS.proud, .2], [L[11], CPS.wave, .3],
  [T.youtube + .5, CPS.cheeky, .2], [E[11], CPS.proud, .3], [E[11] + .6, CPS.wave, .3]];
// where Claude is (also used by the camera and the minis)
const CITY_PATH = [[L[9], [0, 6.2, 9.0]], [L[9] + 1.1, [0, 3.4, 6.2]], [T.blowing, [0, 3.2, 3.6]], [T.niche + .2, [.55, 4.4, .4]],
  [T.writes + .3, [.55, 4.0, -2.4]], [T.voice, [.5, 4.9, -3.0]], [L[10], [.3, 6.2, -4.0]]];
function cityClaude(t) {
  let i = 0; while (i < CITY_PATH.length - 2 && t >= CITY_PATH[i + 1][0]) i++;
  const [a, pa] = CITY_PATH[i], [b, pb] = CITY_PATH[i + 1];
  const k = easeIO(win(t, a, b));
  const p = lerpV(pa, pb, k);
  return V(C0.x + p[0] + Math.sin(t * 2.3) * .12, C0.y + p[1] + Math.sin(t * 3.1) * .08, C0.z + p[2]);
}
function clPos(t) {
  const bob = V(Math.sin(t * 1.1) * .02, Math.sin(t * Math.PI * 2 / 1.7) * .035, 0);
  if (t < L[1] + .32) { const k = easeOut(win(t, L[1] - .12, L[1] + .32)); const p = MONP.clone().lerp(HERO, k); p.y += Math.sin(k * Math.PI) * .25; return p; }
  if (t < L[3] - .3) return HERO.clone().add(bob);
  if (t < E[7] + .05) {
    let i = 0; for (let j = 0; j < 5; j++) if (t >= ST[j].T - .3) i = j;
    const from = i === 0 ? HERO : ST[i - 1].cl, k = easeIO(win(t, ST[i].T - .3, ST[i].T + .1));
    return from.clone().lerp(ST[i].cl, k).add(bob);
  }
  if (t < L[9] - .05) { const k = easeIO(win(t, E[7] + .05, E[7] + .65)); return ST[4].cl.clone().lerp(CALM_P, k).add(bob.multiplyScalar(.4)).add(V(0, 0, easeIO(win(t, L[8] - .2, L[8] + .4)) * .16)); }
  if (t < L[10] - .02) return cityClaude(t);
  const LINKSIDE = V(.5, 1.12, -.15), CTA = V(.02, 1.3, .25);
  const LAND = V(-.55, 2.0, -1.75);
  if (t < T.setup - .25) return LAND.clone().add(bob);
  if (t < L[11] - .2) return LAND.clone().lerp(LINKSIDE, easeIO(win(t, T.setup - .25, T.setup + .15))).add(bob);
  return LINKSIDE.clone().lerp(CTA, easeIO(win(t, L[11] - .2, L[11] + .25))).add(bob);
}
function animClaude(t) {
  const vis = t >= L[1] - .12;
  cl.root.visible = vis; coralLight.intensity = 0;
  if (!vis) return;
  const p = clPos(t);
  cl.root.position.copy(p);
  // grows out of the screen; a split flash on "eleven"
  const grow = easeOut(win(t, L[1] - .12, L[1] + .25));
  const sq = pulse(t, L[1] + .3, .03, .3) + pulse(t, T.eleven - .02, .03, .25) * .7;
  const inCity = between(t, L[9] - .05, L[10] - .02);
  const pres = win(t, L[3] - .3, L[3] + .1) * (1 - win(t, E[7], E[7] + .5));
  const sc = lerp(.18, 1, grow) * (inCity ? 1.25 : 1) * (1 - pres * .3);
  cl.body.scale.set(sc * (1 + sq * .2), sc * (1 - sq * .22), sc);
  // face the camera, with a little life
  cl.root.lookAt(camera.position);
  const ps = poseAt(clKeys, t);
  cl.root.rotateZ(ps.tilt + Math.sin(t * .9) * .04);
  cl.root.rotateX(-ps.lean);
  cl.root.rotateY(Math.sin(t * .7) * .08);
  // spin on the burst and while flying
  cl.body.rotation.z = (1 - grow) * 5 + (inCity ? Math.sin(t * 1.7) * .12 : 0);
  // rays breathe; the two arm rays gesture
  cl.rs.forEach((r, i) => { r.r.scale.y = 1 + Math.sin(t * 3 + i * 1.7) * .05 + (inCity ? .12 : 0); r.piv.rotation.z = r.base + Math.sin(t * 2 + i) * .03; });
  let aR = ps.aR, aL = ps.aL;
  if (between(t, L[11] - .1, T.youtube + .5) || t > E[11] + .6) aR += Math.sin(t * 11) * .35;      // wave
  if (between(t, T.link - .05, T.link + .2)) aL -= Math.sin(win(t, T.link - .05, T.link + .2) * Math.PI) * .5;   // press send
  cl.armR.piv.rotation.z = cl.armR.base + aR;
  cl.armL.piv.rotation.z = cl.armL.base - aL;
  // face
  const blink = ((t + .4) % 3.1) < .1 ? 1 : 0;
  const talk = envAt("claude", t);
  cl.eyes.forEach((e, i) => {
    const shut = ps.happy > .5 || (i === 0 && ps.wink > .5);
    e.open.visible = !shut; e.shut.visible = shut;
    e.open.scale.set(.85, Math.max(.06, 1.35 * ps.eyeH * (1 - blink)), .5);
    e.open.position.set(e.x + ps.lx * .012, .035 + ps.ly * .01, 0);
  });
  const sm = ps.smile;
  cl.mouthArc.rotation.z = sm >= 0 ? Math.PI : 0;
  cl.mouthArc.scale.set(.75 + Math.abs(sm) * .45, .25 + Math.abs(sm) * .8, 1);
  const open = clamp(Math.max(ps.open, talk * 1.25));
  cl.mouthO.scale.set(.75 + open * .3, .08 + open * .6, .3);
  cl.mouthO.visible = open > .05; cl.mouthArc.visible = open < .55;
  cl.micDot.material.color.setScalar(1).multiply(new THREE.Color(RED)).multiplyScalar(1 + talk * 4);
  cl.halo.material.color.set(CORAL).multiplyScalar(.16 + talk * .14 + pulse(t, L[1] + .1, .05, .6) * .8);
  coralLight.position.copy(p).add(V(0, .35, .9)); coralLight.intensity = (inCity ? .8 : 1.6) + talk * 1.2 + pulse(t, L[1] + .1, .05, .6) * 10;
  // the tea: in Claude's right hand through the calm, put down for the whisper
  mug.visible = between(t, E[7] + .2, L[9] - .05);
  if (mug.visible) {
    cl.root.updateMatrixWorld(true);
    const hand = cl.armR.tip.getWorldPosition(tV).add(V(0, -.05, .04));
    const down = easeIO(win(t, L[8] - .45, L[8] - .1));
    mug.position.copy(hand).lerp(MUG_DESK, down);
    mug.scale.setScalar(easeOut(win(t, E[7] + .2, E[7] + .5)));
    mug.rotation.set(0, -.4, 0);
    steam.forEach((s, i) => {
      const ph = ((t * .45 + i / 6) % 1);
      s.position.set(Math.sin(ph * 6 + i) * .015, .05 + ph * .2, 0);
      s.material.opacity = Math.sin(ph * Math.PI) * .9; s.scale.setScalar(.6 + ph * 1.2);
      s.quaternion.copy(camera.quaternion);
    });
  }
}

// ---------------------------------------------------------------- the minis' day
const stw = (i, o) => o.clone().applyQuaternion(stations[i].quaternion).add(ST[i].p);
function miniAt(i, t) {
  const th = Math.PI / 2 + i / 11 * Math.PI * 2 + (t - T.eleven) * .6;
  const ring = HERO.clone().add(V(Math.cos(th) * .8, Math.sin(th) * .76 + .03, .12));
  const out = easeOut(win(t, T.eleven - .04, T.eleven + .32));
  let p = clPos(t).lerp(ring, out);
  let dest = null, d0 = 0, d1 = 0;
  if (i < 5) {
    d0 = L[3] - .5 + i * .06; d1 = d0 + .5;
    dest = i === 2 ? stw(2, V(PH(t), .15, .1)) : stw(i, MINI_AT[i]);
    dest.y += Math.sin(t * (i === 0 ? 9 : 3) + i) * (between(t, ST[i].T, ST[i].T + 1.5) ? .02 : .03);
  } else if (i < 10) {
    d0 = T.eleven + .4 + (i - 5) * .07; d1 = ZAP(i);
    const idle = V(-1.65 + (i - 5) * .82, 2.78 + Math.sin(t * 1.3 + i) * .08, -2.0 + Math.cos(t * .9 + i) * .15);
    dest = PARK[i].clone().lerp(idle, easeIO(win(t, ZAP(i) + .12, ZAP(i) + .7)));
  } else {
    d0 = T.eleven + .45; d1 = d0 + .6;
    dest = V(.62 + Math.sin(t * 1.4) * .04, 1.62 + Math.sin(t * 2.2) * .03, -1.45);
  }
  p.lerp(dest, easeIO(win(t, d0, d1)));
  // home again: they all fly back into Claude for the calm
  p.lerp(clPos(t), easeIn(win(t, E[7] + .05 + i * .02, E[7] + .55 + i * .02)));
  return p;
}
function animMinis(t) {
  minis.forEach((m, i) => {
    const s = backOut(win(t, T.eleven - .04, T.eleven + .3), 2) * (1 - easeIn(win(t, E[7] + .25 + i * .02, E[7] + .55 + i * .02)));
    m.root.visible = s > .002;
    if (!m.root.visible) return;
    m.root.position.copy(miniAt(i, t));
    m.root.scale.setScalar(.34 * Math.max(.001, s));
    m.root.lookAt(camera.position);
    m.body.rotation.z = Math.sin(t * 2.6 + i * 1.3) * .25 + (i === 0 && between(t, L[3], E[3]) ? Math.sin(t * 18) * .12 : 0);
    m.rs.forEach((r, k) => { r.r.scale.y = 1 + Math.sin(t * 5 + k * 2 + i) * .08; });
    const bl = ((t + i * .37) % 2.7) < .09;
    m.eyes.forEach((e) => { e.scale.y = bl ? .1 : 1.3; });
  });
}

// ---------------------------------------------------------------- the room: light, screens, clock, sunrise
const cRed = new THREE.Color(RED), cCoral = new THREE.Color(CORAL), cAmber = new THREE.Color(AMBER), cViolet = new THREE.Color(VIOLET),
  cDawn = new THREE.Color(0xff9a5c), tmpC = new THREE.Color();
function animSet(t) {
  const chaos = t < L[1], calm = between(t, E[7], L[9]), dawn = t >= L[10] - .02;
  const toCalm = easeIO(win(t, E[7], E[7] + .8));
  // LED strip: the mood
  if (chaos) tmpC.copy(cRed).multiplyScalar(1.6 + Math.sin(t * 9) * .9 + pulse(t % 1.1, .05, .02, .2) * 1.5);
  else if (t < E[7]) tmpC.copy(cCoral).lerp(cViolet, .5 + .5 * Math.sin(t * 1.2)).multiplyScalar(2.2);
  else if (!dawn) tmpC.copy(cViolet).lerp(cAmber, toCalm).multiplyScalar(lerp(2.2, .9, toCalm));
  else tmpC.copy(cDawn).multiplyScalar(2.2);
  ledM.color.copy(tmpC); ledHalo.material.color.copy(tmpC).multiplyScalar(.14);
  alarm.intensity = chaos ? 7 * (.55 + .45 * Math.sin(t * 8)) : 0;
  key.color.set(dawn ? 0xffc078 : 0xffb46b);
  key.intensity = chaos ? 38 : calm ? lerp(70, 34, toCalm) : dawn ? 105 : 70;
  rim.intensity = chaos ? 50 : calm ? 22 : 40;
  hemi.intensity = dawn ? .7 : calm ? .28 : .35;
  fx.position.copy(MONP).add(V(.2, 0, .4)); fx.intensity = pulse(t, L[1] - .1, .04, .5) * 14;
  // monitor
  let ms = "monWork";
  if (t < L[1] - .08) ms = Math.floor(t * 12) % 7 === 0 ? "monErr2" : "monErr";
  else if (t < L[1] + .2) ms = "monBurst";
  else if (t >= E[7] + .3 && !dawn) ms = "monSleep";
  else if (dawn) ms = "monDone";
  setMap(monScreen, ms);
  monScreen.material.color.setScalar(ms === "monBurst" ? 1.6 : ms === "monSleep" ? .55 : 1.15);
  screenLight.color.set(t < L[1] - .15 ? 0xff5a5a : dawn ? 0xbfe8d4 : 0xffb59a);
  screenLight.intensity = calm ? 1 : 3 + pulse(t, L[1] - .1, .04, .4) * 5;
  lapScreen.material.color.set(chaos ? 0xff4050 : 0x9fc4ff).multiplyScalar(chaos ? 1.4 + Math.sin(t * 15) * .4 : calm ? .5 : 1.2);
  // phone buzzing through the hook
  const buzz = chaos ? pulse(t % 1.1, .05, .02, .3) : 0;
  phoneG.position.set(-.25 + Math.sin(t * 90) * .006 * buzz, .79 + buzz * .006, .22);
  phoneScreen.material.color.set(chaos ? RED : 0x101018).multiplyScalar(chaos ? 1.2 + buzz * 2.5 : 1);
  recDot.material.color.set(RED).multiplyScalar(Math.floor(t * 2) % 2 ? 3 : .3);
  // clock: stuck at 3:00 through the night, ticking in the calm, 7:00 at sunrise
  const sec = calm ? Math.floor(t - E[7]) : 0;
  hourH.rotation.z = dawn ? -7 / 12 * Math.PI * 2 : -Math.PI / 2 - sec * .002;
  minH.rotation.z = dawn ? 0 : -sec * Math.PI * 2 / 60;
  // sunrise
  const sun = easeOut(win(t, L[10] - .02, L[10] + 1.6));
  skyDawn.material.opacity = dawn ? sun : 0;
  bokeh.forEach((b, i) => { b.visible = !dawn || sun < .8; b.material.opacity = 1; });
  shafts.forEach((s, k) => { s.visible = dawn; s.material.color.set(0xffb070).multiplyScalar(.1 * sun * (1 + Math.sin(t * .8 + k) * .2)); });
  // the link card
  const la = T.setup - .2;
  const lk = backOut(win(t, la, la + .3), 1.8) * (1 - easeIn(win(t, L[11] - .15, L[11] + .15)));
  linkC.visible = dawn && lk > .002; linkC.scale.setScalar(Math.max(.001, lk));
  setMap(linkC.userData.face, t < T.paste - .02 ? "link0" : t < T.link + .25 ? "link1" : "link2");
  linkC.position.y = 1.66 + Math.sin(t * 1.3) * .012;
}

// ---------------------------------------------------------------- the city at work
function animCity(t) {
  towers.forEach((tw) => {
    const a = L[9] - .08 + tw.dist * .03;
    tw.m.scale.y = Math.max(.001, easeOut(win(t, a, a + .5)) + pulse(t, a + .5, .05, .3) * .04);
  });
  OUT.forEach((q, k) => {
    const a = T.blowing - .15 + k * .12;
    const on = easeOut(win(t, a, a + .3));
    beams[k].visible = on > 0;
    beams[k].material.color.set(k === 0 ? CYAN : GOLD).multiplyScalar(on * (.16 + .06 * Math.sin(t * 6 + k)));
    beams[k].scale.set(.4 + on * .6, 1, .4 + on * .6);
    const c = chips[k];
    const ck = backOut(win(t, a + .08, a + .35), 2);
    c.visible = ck > .002; c.scale.setScalar(Math.max(.001, ck));
    c.quaternion.copy(camera.quaternion);
    c.position.y = q[2] * Math.max(.001, easeOut(win(t, L[9] - .08 + Math.hypot(q[0], q[1] - 7) * .03, L[9] + .5 + Math.hypot(q[0], q[1] - 7) * .03))) + .45;
  });
  // X-ray of the tallest
  const xa = T.blowing + .45;
  const xk = easeIO(win(t, xa, xa + .3));
  xTower.m.material.opacity = 1 - xk * .78;
  xTower.edges.material.color.set(CYAN).multiplyScalar(1.6 + xk * 2.5);
  scan.visible = t > xa && t < L[10];
  scan.position.set(OUT[0][0], ((t - xa) / .9 % 1) * OUT[0][2], OUT[0][1]);
  scan.material.color.set(CYAN).multiplyScalar(.45 * xk);
  const xc = backOut(win(t, xa + .15, xa + .45), 1.8);
  xray.visible = xc > .002; xray.scale.setScalar(Math.max(.001, xc)); xray.quaternion.copy(camera.quaternion);
  // the new one rises out of the soundwave
  const b = easeIO(win(t, T.writes - .15, T.voice + .25));
  newT.visible = b > .002; newT.scale.y = Math.max(.001, b);
  newT.material.emissiveIntensity = 1.1 + pulse(t, T.voice + .2, .05, .5) * .8;
  const env = envAt("claude", t);
  for (let k = 0; k < WAVE; k++) {
    const y = k / WAVE * NEWH * 1.06;
    const show = t > T.writes - .25 && y < b * NEWH + .5 && t < T.voice + 1.0;
    if (!show) { wave.setMatrixAt(k, ZERO); continue; }
    const th = k * .42 + t * 2.4, r = .95 - (1 - win(y, b * NEWH - .6, b * NEWH + .5)) * .25;
    tP.set(NEWLOT.x + Math.cos(th) * r, y, NEWLOT.z + Math.sin(th) * r);
    tS.set(1, .08 + Math.abs(Math.sin(k * .9 + t * 9)) * (.18 + env * .5) * (1 - win(t, T.voice + .5, T.voice + 1.0)), 1);
    wave.setMatrixAt(k, tM.compose(tP, tQ.identity(), tS));
  }
  wave.instanceMatrix.needsUpdate = true;
  const nc = backOut(win(t, T.voice + .2, T.voice + .5), 1.8);
  newChip.visible = nc > .002; newChip.scale.setScalar(Math.max(.001, nc)); newChip.quaternion.copy(camera.quaternion);
  // Claude's coral trail
  for (let k = 0; k < TRAIL; k++) {
    const tt = t - (k + 5) * .03;
    if (tt < L[9]) { trail.setMatrixAt(k, ZERO); continue; }
    tP.copy(cityClaude(tt));
    tS.setScalar(Math.sin((k + 1) / (TRAIL + 1) * Math.PI) * .55);
    trail.setMatrixAt(k, tM.compose(tP, camera.quaternion, tS));
  }
  trail.instanceMatrix.needsUpdate = true;
}

// ---------------------------------------------------------------- camera: one shot list, blended at each cut that isn't hard
const C = (x, y, z) => [C0.x + x, C0.y + y, C0.z + z];
const SHOTS = [
  { a: 0, b: L[1] - .35, p: [[.8, 1.58, 1.4], [.55, 1.5, .9]], q: [[.15, 1.3, -1.5], [.05, 1.28, -1.5]], fov: 40 },
  { a: L[1] - .35, b: L[1], blend: .22, p: [[.45, 1.48, 1.15], [.3, 1.42, .85]], q: [MONP.toArray(), MONP.toArray()], fov: 38 },
  { a: L[1] - .02, b: L[2], p: [[.42, 1.12, 2.35], [.25, 1.2, 2.05]], q: [[-.18, 1.32, -.55], [-.15, 1.34, -.5]], fov: 42 },
  { a: L[2], b: L[3] - .3, blend: .35, p: [[0, 1.66, 3.05], [0, 1.62, 2.75]], q: [[-.1, 1.7, -.5], [-.1, 1.68, -.5]], fov: 42 },
  ...ST.map((s, i) => ({ a: s.T - .3, b: i < 4 ? ST[i + 1].T - .3 : E[7], blend: .32, p: s.cam, q: [s.look, s.look], fov: s.fov })),
  { a: E[7], b: L[8] + .55, blend: .6, p: [[.65, 1.52, 1.95], [.6, 1.5, 1.75]], q: [[.45, 1.2, -1.1], [.47, 1.2, -1.1]], fov: 38 },
  { a: L[8] + .55, b: L[9] - .2, blend: .7, p: [[.62, 1.36, .95], [.66, 1.3, .62]], q: [[.7, 1.2, -.75], [.7, 1.2, -.75]], fov: [36, 33] },
  { a: L[9], b: L[9] + 1.1, p: [C(0, 11, 13), C(0, 5.4, 9.6)], q: [C(0, 2.5, 2), C(0, 3.2, 5.6)], fov: 52 },
  { a: L[9] + 1.1, b: T.blowing - .1, blend: .3, follow: [[.75, .65, 2.6], [0, -.15, -2.5]], fov: 48 },
  { a: T.blowing - .1, b: T.writes - .1, blend: .4, p: [C(-.5, 3.6, 6.0), C(-.3, 4.4, 5.0)], q: [C(1.4, 5.6, -3.6), C(1.5, 6.3, -3.6)], fov: 50 },
  { a: T.writes - .1, b: L[10], blend: .45, p: [C(-.35, 3.0, 1.2), C(-.25, 4.4, .3)], q: [C(0, 3.0, -6.8), C(0, 5.4, -6.8)], fov: 50 },
  { a: L[10], b: T.setup - .15, p: [[1.25, 1.55, 1.4], [1.1, 1.5, 1.15]], q: [[-.32, 1.32, -1.45], [-.32, 1.32, -1.45]], fov: 40 },
  { a: T.setup - .15, b: L[11] - .1, blend: .35, p: [[.68, 1.6, 2.15], [.66, 1.58, 1.9]], q: [[.64, 1.5, -.42], [.64, 1.5, -.42]], fov: 40 },
  { a: L[11] - .1, b: T.end, blend: .45, p: [[.1, 1.45, 2.3], [.1, 1.5, 2.7]], q: [[.05, 1.45, -.6], [.05, 1.48, -.6]], fov: 40 },
];
function evalShot(s, t) {
  const k = easeIO(win(t, s.a, s.b));
  if (s.follow) { const c = cityClaude(t); return [c.toArray().map((v, i) => v + s.follow[0][i]), c.toArray().map((v, i) => v + s.follow[1][i]), s.fov]; }
  const fov = Array.isArray(s.fov) ? lerp(s.fov[0], s.fov[1], k) : s.fov;
  return [lerpV(s.p[0], s.p[1], k), lerpV(s.q[0], s.q[1], k), fov];
}
function shot(t) {
  let i = 0; for (let j = 0; j < SHOTS.length; j++) if (t >= SHOTS[j].a) i = j;
  const cur = evalShot(SHOTS[i], t), s = SHOTS[i];
  if (i > 0 && s.blend && t < s.a + s.blend) {
    const prev = evalShot(SHOTS[i - 1], t), k = easeIO(win(t, s.a, s.a + s.blend));
    return [lerpV(prev[0], cur[0], k), lerpV(prev[1], cur[1], k), lerp(prev[2], cur[2], k)];
  }
  return cur;
}
function shake(t) {
  const hand = t < L[1] ? .035 : between(t, E[7], L[9]) ? .0 : between(t, L[9], L[10]) ? .014 : .008;
  const hits = pulse(t, L[1] - .02, .02, .45) * 1.2 + pulse(t, T.free, .02, .3) * .5 + pulse(t, T.eleven, .02, .35) * .7 +
    pulse(t, L[9], .02, .5) * 1.4 + pulse(t, T.voice + .2, .02, .4) * .6 + pulse(t, T.youtube, .02, .3) * .5;
  return { hand, hits };
}

// ---------------------------------------------------------------- render
function renderAt(t) {
  const inCity = between(t, L[9] - .02, L[10] - .02);
  const [p, q, fov] = shot(t);
  const { hand, hits } = shake(t);
  camera.position.set(p[0] + Math.sin(t * 13.1) * hand + Math.sin(t * 91) * .03 * hits, p[1] + Math.cos(t * 11.7) * hand * .8 + Math.cos(t * 77) * .03 * hits, p[2]);
  camera.lookAt(q[0] + Math.sin(t * 7.3) * hand * .5, q[1] + Math.cos(t * 5.9) * hand * .5, q[2]);
  camera.rotateZ((t < L[1] ? Math.sin(t * 1.7) * .05 + .03 : 0) + Math.sin(t * 61) * .01 * hits);
  camera.fov = fov - pulse(t, L[1] - .02, .04, .5) * 5 - pulse(t, L[9], .04, .6) * 6 + pulse(t, T.youtube, .03, .3) * 2;
  camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  studio.visible = !inCity; hu.root.visible = !inCity; city.visible = inCity;
  scene.background.copy(inCity ? BG_CITY : BG_STUDIO);
  scene.fog.color.set(inCity ? 0x0c0620 : 0x120a14); scene.fog.density = inCity ? .045 : .02;
  if (!inCity) animHuman(t);
  animClaude(t); animMinis(t); animNotes(t); animStations(t); animTitle(t); animSet(t);
  if (inCity) animCity(t); else trail.count = 0;
  if (inCity) trail.count = TRAIL;
  animParticles(t);
  // grade per phase: red chaos, clean order, warm calm and the blackout, cool neon, golden dawn
  const g = grade.uniforms;
  g.uTime.value = Math.round(t * 30) / 30;
  const toCalm = easeIO(win(t, E[7], E[7] + .8));
  if (t < L[1]) g.uTint.value.set(1.1, .9, .94);
  else if (t < L[9]) g.uTint.value.set(lerp(1.02, 1.08, toCalm), lerp(.99, .95, toCalm), lerp(1.0, .86, toCalm));
  else if (inCity) g.uTint.value.set(.96, .98, 1.1);
  else g.uTint.value.set(1.07, 1.0, .92);
  g.uGrain.value = t < L[1] ? .075 : .05;
  g.uVig.value = t < L[1] ? .75 : between(t, E[7], L[9]) ? lerp(.6, .95, toCalm) : .6;
  g.uChroma.value = (t < L[1] ? .5 + Math.abs(Math.sin(t * 17)) * .6 * pulse(t % 1.1, .05, .02, .2) : 0) + hits * 1.4;
  g.uBlack.value = between(t, L[9] - .5, L[9]) ? easeIn(win(t, L[9] - .5, L[9] - .06)) : 0;
  bloom.strength = inCity ? .7 + pulse(t, T.voice + .2, .03, .5) * .15 : t < L[1] ? .55 : between(t, E[7], L[9]) ? .32 : .45;
  bloom.threshold = inCity ? .8 : .88;
  composer.render();
}

// ---------------------------------------------------------------- textures
function panel(g, w, h, o = {}) {
  rr(g, 2, 2, w - 4, h - 4, o.r ?? 22); g.fillStyle = o.bg || "rgba(24,18,38,.94)"; g.fill();
  if (o.line) { g.strokeStyle = o.line; g.lineWidth = o.lw || 3; g.stroke(); }
}
function sparkGlyph(g, x, y, R, c = "#d97757") {
  g.fillStyle = c;
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * Math.PI * 2 + (i % 2) * .05, l = R * (.75 + hash(i + 3) * .3);
    g.save(); g.translate(x, y); g.rotate(a); rr(g, -R * .13, R * .2, R * .26, l, R * .13); g.fill(); g.restore();
  }
  g.beginPath(); g.arc(x, y, R * .42, 0, Math.PI * 2); g.fill();
}
function drawTextures() {
  const ct = (k, w, h, f) => { TX[k] = canvasTex(w, h, f); };
  ct("badge", 256, 158, (g, w, h) => {
    panel(g, w, h, { bg: "#f6efe4", r: 18 }); g.fillStyle = "#d97757"; g.fillRect(2, 2, w - 4, 34);
    write(g, "ALL ACCESS", w / 2, 20, 20, { f: "JBMono", c: "#fff", a: "center" });
    write(g, "PRODUCER", w / 2, 82, 44, { w: 800, c: "#1a1028", a: "center", max: w - 24 });
    write(g, "@ai.nxtlvl", w / 2, 128, 22, { f: "JBMono", c: "#7b2ffb", a: "center" });
  });
  NOTES.forEach((n, i) => {
    const note = (k, ic, col, head, body, done) => ct(k, 512, 128, (g, w, h) => {
      panel(g, w, h, { bg: done ? "rgba(14,40,32,.95)" : "rgba(28,20,36,.95)", line: done ? "#3fd69b" : "rgba(255,255,255,.16)", r: 30 });
      rr(g, 18, 18, 92, 92, 22); g.fillStyle = col; g.fill();
      if (done) tick(g, 64, 66, 52, "#06140f", 11); else write(g, ic, 64, 66, 54, { w: 800, a: "center" });
      write(g, head, 128, 44, 32, { w: 700, max: 300 }); write(g, done ? "done" : "now", w - 26, 44, 24, { w: 600, c: "rgba(244,241,250,.55)", a: "right" });
      write(g, body, 128, 88, 28, { w: 600, c: done ? "#bdf3dc" : "#e4dcf5", max: 360 });
    });
    note("note" + i, n.i, n.c, n.h, n.b, false);
    if (n.d) note("done" + i, "", "#3fd69b", n.h, n.d, true);
  });
  ct("page", 512, 676, (g, w, h) => {
    panel(g, w, h, { bg: "#f6efe4", r: 26 });
    write(g, "SCRIPT.md", 44, 62, 40, { f: "JBMono", c: "#1a1028" });
    rr(g, 44, 104, 210, 44, 22); g.fillStyle = "#7b2ffb"; g.fill(); write(g, "HOOK · SCORED", 149, 127, 22, { f: "JBMono", a: "center" });
  });
  FORMULAS.forEach((f, k) => ct("f" + k, 256, 64, (g, w, h) => {
    panel(g, w, h, { bg: k % 3 === 0 ? "#d97757" : "rgba(30,20,52,.96)", line: "rgba(240,160,124,.8)", r: 30 });
    write(g, f, w / 2, h / 2 + 1, 25, { w: 700, a: "center", max: w - 26 });
  }));
  ct("thBefore", 640, 360, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#5b5560"); gr.addColorStop(1, "#8a7d6a"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    [["my new video", 40, 60, 34, "#ffef5a"], ["FINAL edit", 300, 110, 30, "#5af0ff"], ["vlog #47", 60, 190, 40, "#ff6ad5"], ["must watch!!!", 250, 260, 36, "#ffffff"], ["(v7)", 520, 320, 26, "#c0ff6a"]]
      .forEach(([s, x, y, z, c], i) => { g.save(); g.translate(x, y); g.rotate((hash(i) - .5) * .3); write(g, s, 0, 0, z, { w: 600, c }); g.restore(); });
    g.strokeStyle = "#ff3b46"; g.lineWidth = 6; g.beginPath(); g.arc(520, 150, 50, 0, 7); g.stroke();
  });
  ct("thAfter", 640, 360, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#2a0f5a"); gr.addColorStop(1, "#7b2ffb"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "#f6efe4"; g.beginPath(); g.arc(165, 180, 110, 0, 7); g.fill();
    g.strokeStyle = "#1a1028"; g.lineWidth = 14; g.lineCap = "round"; g.beginPath(); g.moveTo(165, 180); g.lineTo(165, 105); g.moveTo(165, 180); g.lineTo(225, 180); g.stroke();
    write(g, "FIXED", 470, 140, 104, { w: 800, a: "center" }); write(g, "IT.", 470, 245, 104, { w: 800, a: "center", c: "#ffc24a" });
  });
  ct("tiBefore", 640, 89, (g, w, h) => { panel(g, w, h, { bg: "rgba(40,14,22,.95)", line: "#ff3b46", r: 20 });
    write(g, "my new video (FINAL edit) | vlog #47 | must wat…", 24, h / 2, 27, { w: 600, c: "#ffb3bb", max: 540 }); write(g, "✕", w - 34, h / 2, 34, { w: 800, c: "#ff3b46", a: "center" }); });
  ct("tiAfter", 640, 89, (g, w, h) => { panel(g, w, h, { bg: "rgba(14,40,32,.95)", line: "#3fd69b", r: 20 });
    write(g, "My 3 AM Creator Routine", 24, h / 2, 34, { w: 700, max: 540 }); tick(g, w - 36, h / 2, 34); });
  ct("lint", 640, 76, (g, w, h) => {
    [["not cut off", 8], ["no repeat", 222], ["specific", 430]].forEach(([s, x]) => {
      rr(g, x, 8, 200, h - 16, 30); g.fillStyle = "rgba(63,214,155,.18)"; g.fill(); g.strokeStyle = "#3fd69b"; g.lineWidth = 3; g.stroke();
      tick(g, x + 32, h / 2, 26); write(g, s, x + 56, h / 2, 25, { w: 700, max: 136 });
    });
  });
  ["dead air", "\"umm\"", "retake", "dead air"].forEach((s, k) => ct("flag" + k, 192, 63, (g, w, h) => {
    panel(g, w, h, { bg: "#ff3b46", r: 28 }); write(g, s, w / 2, h / 2 + 1, 28, { w: 800, a: "center", max: w - 20 }); }));
  ct("edl", 512, 300, (g, w, h) => {
    panel(g, w, h, { line: "rgba(169,139,255,.5)", r: 26 });
    write(g, "EDIT DECISION LIST", 30, 40, 24, { f: "JBMono", c: "#a98bff" });
    [["00:42", "dead air · cut"], ["01:13", "\"umm\" · cut"], ["02:05", "retake · keep 2nd"], ["03:31", "dead air · cut"]].forEach(([tc, s], k) => {
      write(g, tc, 30, 92 + k * 52, 28, { f: "JBMono", c: "#ff7a82" }); write(g, s, 150, 92 + k * 52, 30, { w: 600 });
    });
  });
  const CM = [["@mia.films", "how do you edit so fast??"], ["@devonk", "part 2 please"], ["@aj_creates", "this fixed my whole week"], ["@noor", "what mic is that?"]];
  const RP = ["Batch it: one edit list per video", "Part 2 is planned for Friday", "That means a lot, thank you", "Linked it in the description"];
  CM.forEach(([n, s], k) => ct("cm" + k, 512, 95, (g, w, h) => {
    panel(g, w, h, { bg: "rgba(36,30,48,.96)", r: 30 });
    g.fillStyle = ["#5af0ff", "#ffc24a", "#ff5fa2", "#a98bff"][k]; g.beginPath(); g.arc(46, h / 2, 26, 0, 7); g.fill();
    write(g, n, 88, 30, 22, { f: "JBMono", c: "#a99fbd" }); write(g, s, 88, 64, 30, { w: 600, max: 400 });
  }));
  RP.forEach((s, k) => ct("rp" + k, 512, 92, (g, w, h) => {
    panel(g, w, h, { bg: "#d97757", r: 30 }); write(g, "YOU", 26, 30, 20, { f: "JBMono", c: "#3a140a" });
    write(g, s, 26, 62, 28, { w: 700, max: w - 52 });
  }));
  ct("pin", 96, 96, (g, w, h) => {
    g.fillStyle = "#ffc24a"; g.beginPath(); g.arc(48, 48, 44, 0, 7); g.fill();
    g.fillStyle = "#1a1028"; g.beginPath(); g.arc(48, 38, 16, 0, 7); g.fill(); g.fillRect(45, 40, 6, 36);
  });
  ct("cal", 512, 624, (g, w, h) => {
    panel(g, w, h, { line: "rgba(169,139,255,.45)", r: 28 });
    write(g, "THIS WEEK", 30, 50, 34, { w: 800 });
    ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"].forEach((d, k) => {
      const y = 121.5 + k * 65.7;
      g.fillStyle = "rgba(244,241,250,.06)"; rr(g, 20, y - 28, w - 40, 56, 14); g.fill();
      write(g, d, 34, y, 24, { f: "JBMono", c: "#a98bff" });
    });
  });
  PLAN.forEach(([row, k, wd], i) => ct("pl" + i, Math.round(wd * 900), 65, (g, w, h) => {
    const col = { anchor: "#ffc24a", cheap: "#38d6f5", short: "#ff5fa2" }[k];
    panel(g, w, h, { bg: col, r: 24 });
    write(g, { anchor: "ANCHOR · long video", cheap: "CHEAP ONE", short: "SHORT" }[k], 22, h / 2 + 1, 28, { w: 800, c: "#1a1028", max: w - 40 });
  }));
  ct("fits", 512, 60, (g, w, h) => { panel(g, w, h, { bg: "rgba(63,214,155,.2)", line: "#3fd69b", r: 28 }); tick(g, 40, h / 2, 26);
    write(g, "fits the hours you actually have", 66, h / 2, 25, { w: 700, max: w - 90 }); });
  ct("title", 1024, 512, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#2a1450"); gr.addColorStop(1, "#140a24");
    rr(g, 2, 2, w - 4, h - 4, 48); g.fillStyle = gr; g.fill(); g.strokeStyle = "rgba(240,160,124,.6)"; g.lineWidth = 4; g.stroke();
    write(g, "FREE · OPEN SOURCE · MIT", w / 2, 78, 34, { f: "JBMono", c: "#f0a07c", a: "center" });
    write(g, "YouTube Agent Skill", w / 2, 190, 92, { w: 800, a: "center", max: w - 80 });
    write(g, "11", 300, 340, 150, { w: 800, c: "#d97757", a: "center" });
    write(g, "skills that run", 390, 318, 44, { w: 700, c: "#f4f1fa" }); write(g, "your channel", 390, 370, 44, { w: 700, c: "#f4f1fa" });
    write(g, "github.com/Jakeschincariol", w / 2, 455, 30, { f: "JBMono", c: "#a98bff", a: "center" });
  });
  const fac = (k, hues, lum) => ct(k, 256, 256, (g, w, h) => {
    g.fillStyle = "#06040c"; g.fillRect(0, 0, w, h);
    for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) {
      const i = r * 3 + c + k.length * 7, hue = hues[Math.floor(hash(i + 1) * hues.length)], on = hash(i + 50) > .18;
      const gr = g.createLinearGradient(0, 0, 80, 60);
      gr.addColorStop(0, `hsla(${hue},85%,${lum * (on ? 1 : .35)}%,1)`); gr.addColorStop(1, `hsla(${hue + 30},80%,${lum * .45 * (on ? 1 : .35)}%,1)`);
      g.fillStyle = gr; rr(g, 8 + c * 82, 8 + r * 62, 74, 50, 6); g.fill();
      if (on) { g.fillStyle = "rgba(255,255,255,.75)"; g.beginPath(); const x = 45 + c * 82, y = 33 + r * 62; g.moveTo(x - 6, y - 8); g.lineTo(x + 9, y); g.lineTo(x - 6, y + 8); g.fill(); }
    }
  });
  fac("fac0", [265, 285, 220], 34); fac("fac1", [320, 340, 290], 32); fac("fac2", [190, 210, 250], 30); fac("fac3", [260, 15, 300], 30);
  fac("facHot", [40, 25, 50], 55); fac("facNew", [18, 25, 10], 62);
  for (const k of ["fac0", "fac1", "fac2", "fac3", "facHot", "facNew"]) { TX[k].wrapS = TX[k].wrapT = THREE.RepeatWrapping; }
  OUT.forEach((q, k) => ct("chip" + k, 512, 129, (g, w, h) => {
    panel(g, w, h, { bg: "rgba(20,12,34,.95)", line: k === 0 ? "#38d6f5" : "#ffc24a", lw: 4, r: 40 });
    write(g, q[3], 30, h / 2 + 2, 78, { w: 800, c: k === 0 ? "#38d6f5" : "#ffc24a" });
    write(g, "its channel's", 210, 46, 30, { w: 600, c: "#d9ccff" }); write(g, "median views", 210, 86, 30, { w: 700 });
  }));
  ct("xray", 640, 215, (g, w, h) => {
    panel(g, w, h, { bg: "rgba(6,22,30,.94)", line: "#38d6f5", lw: 4, r: 34 });
    write(g, "TITLE FORMULA", 34, 46, 28, { f: "JBMono", c: "#38d6f5" });
    write(g, "The Statistic", 34, 112, 66, { w: 800 });
    write(g, "read from the title's words", 34, 172, 26, { w: 600, c: "#9fdcec" });
  });
  ct("newchip", 640, 158, (g, w, h) => {
    panel(g, w, h, { bg: "rgba(42,16,10,.95)", line: "#f0a07c", lw: 4, r: 40 });
    write(g, "YOUR NEXT ONE", 36, 48, 28, { f: "JBMono", c: "#f0a07c" }); write(g, "written in your voice", 36, 106, 46, { w: 800, max: w - 70 });
  });
  const link = (k, state) => ct(k, 800, 320, (g, w, h) => {
    panel(g, w, h, { line: "rgba(240,160,124,.55)", r: 40 });
    write(g, "NEW CHAT", 40, 50, 24, { f: "JBMono", c: "#a99fbd" });
    rr(g, 30, 84, w - 60, 130, 30); g.fillStyle = "rgba(244,241,250,.07)"; g.fill();
    if (state === 0) { write(g, "Paste a link…", 64, 149, 38, { w: 600, c: "rgba(217,204,255,.5)" }); g.fillStyle = "#fff"; g.fillRect(62, 124, 4, 50); }
    else { write(g, "github.com/Jakeschincariol/", 64, 126, 32, { f: "JBMono", c: "#d9ccff" }); write(g, "youtube-agent-skill", 64, 176, 44, { w: 800 }); }
    g.fillStyle = state ? "#d97757" : "rgba(244,241,250,.2)"; g.beginPath(); g.arc(w - 92, 149, 36, 0, 7); g.fill();
    g.strokeStyle = "#fff"; g.lineWidth = 7; g.lineCap = "round"; g.beginPath(); g.moveTo(w - 92, 167); g.lineTo(w - 92, 132); g.moveTo(w - 106, 145); g.lineTo(w - 92, 131); g.lineTo(w - 78, 145); g.stroke();
    if (state === 2) { rr(g, 30, 236, w - 60, 62, 31); g.fillStyle = "rgba(63,214,155,.2)"; g.fill(); g.strokeStyle = "#3fd69b"; g.lineWidth = 3; g.stroke();
      tick(g, 68, 267, 30); write(g, "Installed · /yt-script works", 96, 268, 30, { w: 700 }); }
  });
  link("link0", 0); link("link1", 1); link("link2", 2);
  const mon = (k, f) => ct(k, 1024, 577, f);
  const errScreen = (shift) => (g, w, h) => {
    g.fillStyle = "#14070b"; g.fillRect(0, 0, w, h);
    for (let r = 0; r < 4; r++) for (let c = 0; c < 9; c++) { g.fillStyle = ["#5b3bd0", "#2f7fd0", "#7b3bc0", "#3a2a50"][(r + c) % 4]; g.fillRect(40 + c * 105 + (shift && r === 2 ? 60 : 0), 380 + r * 42, 95, 34); }
    g.fillStyle = "#ff3b46"; g.fillRect(0, 0, w, 64); write(g, "RENDER FAILED · export_final_v7.mp4", 30, 33, 30, { f: "JBMono" });
    write(g, "!", w / 2 + (shift ? -30 : 0), 200, 200, { w: 800, c: "#ff3b46", a: "center" });
    write(g, "0 words written · 99+ comments · 0 planned", w / 2, 320, 30, { w: 600, c: "#ffb3bb", a: "center" });
    if (shift) for (let i = 0; i < 6; i++) { g.fillStyle = `rgba(${i % 2 ? "56,214,245" : "255,59,70"},.5)`; g.fillRect(0, hash(i) * h, w, 10 + hash(i + 3) * 30); }
  };
  mon("monErr", errScreen(false)); mon("monErr2", errScreen(true));
  mon("monBurst", (g, w, h) => { const gr = g.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w * .6); gr.addColorStop(0, "#fff8f0"); gr.addColorStop(.5, "#f0a07c"); gr.addColorStop(1, "#d97757"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  mon("monWork", (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#1a0f24"); gr.addColorStop(1, "#2a1410"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    sparkGlyph(g, 190, h / 2, 110);
    write(g, "11 skills", 360, 210, 84, { w: 800 }); write(g, "on it.", 360, 300, 84, { w: 800, c: "#f0a07c" });
    write(g, "/yt-script  /yt-package  /yt-edit", 360, 390, 28, { f: "JBMono", c: "#a99fbd" });
  });
  mon("monSleep", (g, w, h) => { g.fillStyle = "#07050c"; g.fillRect(0, 0, w, h); sparkGlyph(g, w / 2, h / 2, 60, "rgba(217,119,87,.5)"); });
  mon("monDone", (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#0e1f1a"); gr.addColorStop(1, "#1a1028"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    write(g, "THIS WEEK · READY", 50, 64, 44, { w: 800 });
    ["Script · hooks scored", "Title + thumbnail · linted", "Edit list · 4 cuts", "Replies drafted", "Week planned"].forEach((s, k) => {
      tick(g, 78, 140 + k * 72, 40); write(g, s, 120, 140 + k * 72, 38, { w: 600 });
    });
    write(g, "Nothing goes live until you hit upload.", 50, 530, 28, { w: 600, c: "#9fe6c8" });
  });
  // hand them out
  for (const [m, k] of FACES) { m.material.map = TX[k]; m.material.needsUpdate = true; }
  facM.forEach((m, k) => { m.emissiveMap = TX["fac" + k]; m.needsUpdate = true; });
  towers.filter((tw) => tw.o >= 0).forEach((tw) => { tw.m.material.emissiveMap = TX.facHot; tw.m.material.needsUpdate = true; });
  newT.material.emissiveMap = TX.facNew; newT.material.needsUpdate = true;
  monScreen.material.map = TX.monErr; monScreen.material.needsUpdate = true;
  skyDawn.material.map = canvasTex(64, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#5a4a9a"); gr.addColorStop(.45, "#ff9a7a"); gr.addColorStop(.8, "#ffc27a"); gr.addColorStop(1, "#fff0c0"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  skyDawn.material.needsUpdate = true;
}

// ---------------------------------------------------------------- cover still (cover.html sets window.YT_COVER)
function renderCover(c) {
  renderAt(c.t);
  camera.position.set(...c.cam); camera.lookAt(...c.look); camera.fov = c.fov; camera.updateProjectionMatrix();
  composer.render();
}

const ready = (async () => {
  await Promise.all(["800 90px Poppins", "700 30px Poppins", "600 30px Poppins", "700 34px JBMono"].map((f) => document.fonts.load(f)));
  drawTextures();
  renderer.compile(scene, camera);
  if (window.YT_COVER) { renderCover(window.YT_COVER); window.__coverDone = true; return; }
  renderAt(window.__hfThreeTime || 0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["ytworld"] = ready;
window.addEventListener("hf-seek", (e) => { if (TX.badge && !window.YT_COVER) renderAt(e.detail.time); });
